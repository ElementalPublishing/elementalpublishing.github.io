"""
Street Level Simulation Integration for Cyber Dynasties
=======================================================

This module provides the integration layer between street-level entities
and the broader simulation/character systems. It handles:

- Character-entity interactions
- Dynamic reputation and relationship systems
- Procedural story generation
- Economic and territorial simulation
- Violence escalation modeling
- Daily life simulation hooks
"""

import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum

from street_level_entities import (
    DynastyType, OrganizationType, ViolenceLevel, BaseEntity,
    CriminalSyndicate, StreetGang, LawEnforcementUnit, Corporation,
    SocialClassTemplate, EmploymentNetwork, Territory, EntityRelationship,
    CharacterInteractionSystem
)

from street_level_data_loader import StreetLevelDataLoader, DynastyEntityFactory

# ============================================================================
# SIMULATION STATES AND EVENTS
# ============================================================================

class SimulationEventType(Enum):
    CRIME_COMMITTED = "crime_committed"
    LAW_ENFORCEMENT_RESPONSE = "law_enforcement_response"
    GANG_CONFLICT = "gang_conflict"
    CORPORATE_MERGER = "corporate_merger"
    TERRITORY_CHANGE = "territory_change"
    CHARACTER_RECRUITMENT = "character_recruitment"
    REPUTATION_CHANGE = "reputation_change"
    VIOLENCE_ESCALATION = "violence_escalation"
    ECONOMIC_SHIFT = "economic_shift"
    POLITICAL_MOVEMENT = "political_movement"

@dataclass
class SimulationEvent:
    """Represents an event in the street-level simulation"""
    event_id: str
    event_type: SimulationEventType
    timestamp: datetime
    dynasty: DynastyType
    territory: str
    
    # Participants
    primary_entity: str  # Entity ID
    secondary_entities: List[str] = field(default_factory=list)
    affected_characters: List[str] = field(default_factory=list)
    
    # Event details
    description: str = ""
    severity: int = 5  # 1-10 scale
    publicity: int = 5  # 1-10 scale (how public/known the event is)
    
    # Consequences
    reputation_changes: Dict[str, int] = field(default_factory=dict)
    relationship_changes: List[Tuple[str, str, int]] = field(default_factory=list)  # (entity1, entity2, change)
    territory_changes: Dict[str, List[str]] = field(default_factory=dict)  # territory -> new controllers
    
    # Story hooks
    story_hooks: List[str] = field(default_factory=list)
    follow_up_events: List[str] = field(default_factory=list)

@dataclass
class TerritoryState:
    """Current state of a territory"""
    territory: Territory
    current_crime_level: int
    current_law_presence: int
    current_economic_activity: int
    
    # Active situations
    ongoing_conflicts: List[str] = field(default_factory=list)
    active_investigations: List[str] = field(default_factory=list)
    economic_opportunities: List[str] = field(default_factory=list)
    
    # Recent events
    recent_events: List[str] = field(default_factory=list)  # Event IDs
    last_major_incident: Optional[datetime] = None

# ============================================================================
# CORE SIMULATION ENGINE
# ============================================================================

class StreetLevelSimulation:
    """Main simulation engine for street-level activities"""
    
    def __init__(self, data_loader: StreetLevelDataLoader):
        self.data_loader = data_loader
        self.entity_factory = DynastyEntityFactory(data_loader)
        self.character_system = CharacterInteractionSystem()
        
        # Simulation state
        self.current_time: datetime = datetime.now()
        self.entities: Dict[str, BaseEntity] = {}
        self.territories: Dict[str, TerritoryState] = {}
        self.events: List[SimulationEvent] = []
        self.active_storylines: Dict[str, Dict[str, Any]] = {}
        
        # Configuration
        self.simulation_speed = 1.0  # Real-time multiplier
        self.event_frequency = 0.1  # Events per simulation hour
        self.story_generation_enabled = True
        
    def initialize_dynasty(self, dynasty: DynastyType, territory_count: int = 5):
        """Initialize a dynasty's street-level entities and territories"""
        dynasty_data = self.data_loader.load_dynasty_data(dynasty)
        
        # Create territories
        for i in range(territory_count):
            territory_id = f"{dynasty.value}_territory_{i+1:02d}"
            territory = Territory(
                name=f"{dynasty.value.replace('_', ' ').title()} District {i+1}",
                dynasty=dynasty,
                population=random.randint(50000, 500000),
                economic_level=random.randint(3, 8),
                crime_level=random.randint(2, 7),
                enhancement_acceptance=self._get_dynasty_enhancement_acceptance(dynasty)
            )
            
            territory_state = TerritoryState(
                territory=territory,
                current_crime_level=territory.crime_level,
                current_law_presence=random.randint(3, 7),
                current_economic_activity=territory.economic_level
            )
            
            self.territories[territory_id] = territory_state
        
        # Create criminal organizations
        for i in range(random.randint(2, 4)):
            syndicate = self.entity_factory.create_criminal_syndicate(dynasty)
            syndicate.entity_id = f"{dynasty.value}_syndicate_{i+1:02d}"
            syndicate.territories = random.sample(list(self.territories.keys()), k=random.randint(1, 3))
            self.entities[syndicate.entity_id] = syndicate
            self.character_system.register_entity(syndicate)
        
        # Create law enforcement
        law_unit = self.entity_factory.create_law_enforcement_unit(dynasty)
        law_unit.entity_id = f"{dynasty.value}_law_001"
        law_unit.territories = list(self.territories.keys())  # Law enforcement covers all territories
        self.entities[law_unit.entity_id] = law_unit
        self.character_system.register_entity(law_unit)
        
        # Create corporations
        for i in range(random.randint(3, 6)):
            corp = self.entity_factory.create_corporation(dynasty)
            corp.entity_id = f"{dynasty.value}_corp_{i+1:02d}"
            corp.territories = random.sample(list(self.territories.keys()), k=random.randint(1, 2))
            self.entities[corp.entity_id] = corp
            self.character_system.register_entity(corp)
        
        # Establish initial relationships
        self._establish_initial_relationships(dynasty)
    
    def advance_simulation(self, hours: int = 1):
        """Advance the simulation by specified number of hours"""
        for _ in range(hours):
            self.current_time += timedelta(hours=1)
            self._process_hourly_events()
            self._update_territory_states()
            self._generate_storylines()
            self._cleanup_old_events()
    
    def _process_hourly_events(self):
        """Process events that occur each simulation hour"""
        # Check if any events should occur this hour
        if random.random() < self.event_frequency:
            event = self._generate_random_event()
            if event:
                self.events.append(event)
                self._process_event_consequences(event)
    
    def _generate_random_event(self) -> Optional[SimulationEvent]:
        """Generate a random event based on current simulation state"""
        if not self.territories:
            return None
        
        # Choose a random territory
        territory_id = random.choice(list(self.territories.keys()))
        territory_state = self.territories[territory_id]
        
        # Choose event type based on territory conditions
        event_weights = self._calculate_event_weights(territory_state)
        event_type = self._weighted_choice(event_weights)
        
        # Generate specific event
        return self._create_specific_event(event_type, territory_id, territory_state)
    
    def _calculate_event_weights(self, territory_state: TerritoryState) -> Dict[SimulationEventType, float]:
        """Calculate probability weights for different event types"""
        weights = {
            SimulationEventType.CRIME_COMMITTED: territory_state.current_crime_level * 0.1,
            SimulationEventType.LAW_ENFORCEMENT_RESPONSE: territory_state.current_law_presence * 0.08,
            SimulationEventType.GANG_CONFLICT: len(territory_state.ongoing_conflicts) * 0.15,
            SimulationEventType.CORPORATE_MERGER: territory_state.current_economic_activity * 0.05,
            SimulationEventType.TERRITORY_CHANGE: len(territory_state.ongoing_conflicts) * 0.1,
            SimulationEventType.REPUTATION_CHANGE: 0.2,
            SimulationEventType.VIOLENCE_ESCALATION: territory_state.current_crime_level * 0.06,
            SimulationEventType.ECONOMIC_SHIFT: 0.15,
            SimulationEventType.POLITICAL_MOVEMENT: 0.1
        }
        
        return weights
    
    def _weighted_choice(self, weights: Dict[SimulationEventType, float]) -> SimulationEventType:
        """Choose an item based on weights"""
        total = sum(weights.values())
        if total == 0:
            return random.choice(list(weights.keys()))
        
        r = random.uniform(0, total)
        for item, weight in weights.items():
            r -= weight
            if r <= 0:
                return item
        
        return list(weights.keys())[-1]
    
    def _create_specific_event(self, event_type: SimulationEventType, territory_id: str, territory_state: TerritoryState) -> SimulationEvent:
        """Create a specific event of the given type"""
        territory = territory_state.territory
        
        if event_type == SimulationEventType.CRIME_COMMITTED:
            return self._create_crime_event(territory_id, territory)
        elif event_type == SimulationEventType.LAW_ENFORCEMENT_RESPONSE:
            return self._create_law_enforcement_event(territory_id, territory)
        elif event_type == SimulationEventType.GANG_CONFLICT:
            return self._create_gang_conflict_event(territory_id, territory)
        elif event_type == SimulationEventType.CORPORATE_MERGER:
            return self._create_corporate_event(territory_id, territory)
        elif event_type == SimulationEventType.REPUTATION_CHANGE:
            return self._create_reputation_event(territory_id, territory)
        else:
            # Default generic event
            return self._create_generic_event(event_type, territory_id, territory)
    
    def _create_crime_event(self, territory_id: str, territory: Territory) -> SimulationEvent:
        """Create a crime event"""
        # Find criminal organizations in this territory
        criminals = [e for e in self.entities.values() 
                    if isinstance(e, (CriminalSyndicate, StreetGang)) and territory_id in e.territories]
        
        if not criminals:
            return self._create_generic_event(SimulationEventType.CRIME_COMMITTED, territory_id, territory)
        
        criminal_org = random.choice(criminals)
        
        # Choose crime type based on organization
        if isinstance(criminal_org, CriminalSyndicate):
            crime_types = criminal_org.primary_activities
        else:
            crime_types = ["theft", "assault", "vandalism", "drug_dealing"]
        
        crime_type = random.choice(crime_types)
        
        event = SimulationEvent(
            event_id=f"crime_{self.current_time.strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}",
            event_type=SimulationEventType.CRIME_COMMITTED,
            timestamp=self.current_time,
            dynasty=territory.dynasty,
            territory=territory_id,
            primary_entity=criminal_org.entity_id,
            description=f"{criminal_org.name} committed {crime_type} in {territory.name}",
            severity=random.randint(3, 8),
            publicity=random.randint(2, 7)
        )
        
        # Add story hooks
        event.story_hooks.extend([
            f"investigate_{crime_type}_in_{territory_id}",
            f"track_{criminal_org.entity_id}_activities",
            f"witness_protection_for_{crime_type}"
        ])
        
        return event
    
    def _create_law_enforcement_event(self, territory_id: str, territory: Territory) -> SimulationEvent:
        """Create a law enforcement response event"""
        # Find law enforcement in this territory
        law_enforcement = [e for e in self.entities.values() 
                          if isinstance(e, LawEnforcementUnit) and territory_id in e.territories]
        
        if not law_enforcement:
            return self._create_generic_event(SimulationEventType.LAW_ENFORCEMENT_RESPONSE, territory_id, territory)
        
        law_unit = random.choice(law_enforcement)
        
        response_types = ["patrol_increase", "investigation_launched", "arrest_made", "raid_conducted"]
        response_type = random.choice(response_types)
        
        event = SimulationEvent(
            event_id=f"law_{self.current_time.strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}",
            event_type=SimulationEventType.LAW_ENFORCEMENT_RESPONSE,
            timestamp=self.current_time,
            dynasty=territory.dynasty,
            territory=territory_id,
            primary_entity=law_unit.entity_id,
            description=f"{law_unit.name} conducted {response_type} in {territory.name}",
            severity=random.randint(2, 6),
            publicity=random.randint(4, 8)
        )
        
        # Add story hooks
        event.story_hooks.extend([
            f"assist_law_enforcement_{response_type}",
            f"avoid_law_enforcement_in_{territory_id}",
            f"investigate_law_enforcement_corruption"
        ])
        
        return event
    
    def _create_gang_conflict_event(self, territory_id: str, territory: Territory) -> SimulationEvent:
        """Create a gang conflict event"""
        # Find gangs in this territory
        gangs = [e for e in self.entities.values() 
                if isinstance(e, StreetGang) and territory_id in e.territories]
        
        if len(gangs) < 2:
            return self._create_generic_event(SimulationEventType.GANG_CONFLICT, territory_id, territory)
        
        gang1, gang2 = random.sample(gangs, 2)
        
        conflict_types = ["turf_war", "revenge_attack", "resource_dispute", "honor_conflict"]
        conflict_type = random.choice(conflict_types)
        
        event = SimulationEvent(
            event_id=f"conflict_{self.current_time.strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}",
            event_type=SimulationEventType.GANG_CONFLICT,
            timestamp=self.current_time,
            dynasty=territory.dynasty,
            territory=territory_id,
            primary_entity=gang1.entity_id,
            secondary_entities=[gang2.entity_id],
            description=f"{gang1.name} and {gang2.name} engaged in {conflict_type} in {territory.name}",
            severity=random.randint(5, 9),
            publicity=random.randint(3, 7)
        )
        
        # Add relationship changes
        event.relationship_changes.append((gang1.entity_id, gang2.entity_id, -random.randint(10, 30)))
        
        # Add story hooks
        event.story_hooks.extend([
            f"mediate_conflict_between_{gang1.entity_id}_and_{gang2.entity_id}",
            f"exploit_gang_war_in_{territory_id}",
            f"protect_civilians_from_gang_violence"
        ])
        
        return event
    
    def _create_corporate_event(self, territory_id: str, territory: Territory) -> SimulationEvent:
        """Create a corporate event"""
        # Find corporations in this territory
        corporations = [e for e in self.entities.values() 
                       if isinstance(e, Corporation) and territory_id in e.territories]
        
        if not corporations:
            return self._create_generic_event(SimulationEventType.CORPORATE_MERGER, territory_id, territory)
        
        corp = random.choice(corporations)
        
        corporate_events = ["expansion", "layoffs", "new_product_launch", "scandal_exposure", "merger_attempt"]
        corp_event_type = random.choice(corporate_events)
        
        event = SimulationEvent(
            event_id=f"corp_{self.current_time.strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}",
            event_type=SimulationEventType.CORPORATE_MERGER,
            timestamp=self.current_time,
            dynasty=territory.dynasty,
            territory=territory_id,
            primary_entity=corp.entity_id,
            description=f"{corp.name} announced {corp_event_type} in {territory.name}",
            severity=random.randint(2, 6),
            publicity=random.randint(5, 9)
        )
        
        # Add story hooks
        event.story_hooks.extend([
            f"investigate_corporate_{corp_event_type}",
            f"benefit_from_corporate_changes",
            f"expose_corporate_wrongdoing"
        ])
        
        return event
    
    def _create_reputation_event(self, territory_id: str, territory: Territory) -> SimulationEvent:
        """Create a reputation change event"""
        # Choose random entity in territory
        local_entities = [e for e in self.entities.values() if territory_id in e.territories]
        
        if not local_entities:
            return self._create_generic_event(SimulationEventType.REPUTATION_CHANGE, territory_id, territory)
        
        entity = random.choice(local_entities)
        
        rep_change = random.randint(-20, 20)
        direction = "gained" if rep_change > 0 else "lost"
        
        event = SimulationEvent(
            event_id=f"rep_{self.current_time.strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}",
            event_type=SimulationEventType.REPUTATION_CHANGE,
            timestamp=self.current_time,
            dynasty=territory.dynasty,
            territory=territory_id,
            primary_entity=entity.entity_id,
            description=f"{entity.name} {direction} reputation in {territory.name}",
            severity=abs(rep_change) // 5,
            publicity=random.randint(3, 7)
        )
        
        # Add reputation change
        event.reputation_changes[entity.entity_id] = rep_change
        
        return event
    
    def _create_generic_event(self, event_type: SimulationEventType, territory_id: str, territory: Territory) -> SimulationEvent:
        """Create a generic event when specific creation fails"""
        return SimulationEvent(
            event_id=f"generic_{self.current_time.strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}",
            event_type=event_type,
            timestamp=self.current_time,
            dynasty=territory.dynasty,
            territory=territory_id,
            primary_entity="unknown",
            description=f"Generic {event_type.value} occurred in {territory.name}",
            severity=random.randint(1, 5),
            publicity=random.randint(1, 5)
        )
    
    def _process_event_consequences(self, event: SimulationEvent):
        """Process the consequences of an event"""
        # Apply reputation changes
        for entity_id, change in event.reputation_changes.items():
            if entity_id in self.entities:
                self.entities[entity_id].reputation = max(0, min(100, self.entities[entity_id].reputation + change))
        
        # Apply relationship changes
        for entity1_id, entity2_id, change in event.relationship_changes:
            if entity1_id in self.entities and entity2_id in self.entities:
                entity1 = self.entities[entity1_id]
                entity2 = self.entities[entity2_id]
                
                # Update entity1's relationship with entity2
                existing_rel = entity1.get_relationship(entity2_id)
                if existing_rel:
                    existing_rel.strength = max(-100, min(100, existing_rel.strength + change))
                else:
                    entity1.add_relationship(entity2_id, "conflict", change)
                
                # Update entity2's relationship with entity1
                existing_rel = entity2.get_relationship(entity1_id)
                if existing_rel:
                    existing_rel.strength = max(-100, min(100, existing_rel.strength + change))
                else:
                    entity2.add_relationship(entity1_id, "conflict", change)
        
        # Update territory state
        if event.territory in self.territories:
            territory_state = self.territories[event.territory]
            territory_state.recent_events.append(event.event_id)
            
            # Adjust territory conditions based on event
            if event.event_type == SimulationEventType.CRIME_COMMITTED:
                territory_state.current_crime_level = min(10, territory_state.current_crime_level + 1)
            elif event.event_type == SimulationEventType.LAW_ENFORCEMENT_RESPONSE:
                territory_state.current_crime_level = max(1, territory_state.current_crime_level - 1)
                territory_state.current_law_presence = min(10, territory_state.current_law_presence + 1)
    
    def _update_territory_states(self):
        """Update territory states based on current conditions"""
        for territory_id, territory_state in self.territories.items():
            # Natural decay of elevated conditions
            if territory_state.current_crime_level > territory_state.territory.crime_level:
                territory_state.current_crime_level = max(
                    territory_state.territory.crime_level,
                    territory_state.current_crime_level - 0.1
                )
            
            if territory_state.current_law_presence > 5:
                territory_state.current_law_presence = max(5, territory_state.current_law_presence - 0.1)
            
            # Clean up old events
            if len(territory_state.recent_events) > 10:
                territory_state.recent_events = territory_state.recent_events[-10:]
    
    def _generate_storylines(self):
        """Generate persistent storylines from events and entity states"""
        if not self.story_generation_enabled:
            return
        
        # Look for patterns in recent events
        recent_events = [e for e in self.events if (self.current_time - e.timestamp).days < 7]
        
        # Generate storylines based on patterns
        storylines = self._detect_storyline_patterns(recent_events)
        
        for storyline in storylines:
            storyline_id = f"story_{self.current_time.strftime('%Y%m%d')}_{random.randint(1000, 9999)}"
            self.active_storylines[storyline_id] = storyline
    
    def _detect_storyline_patterns(self, events: List[SimulationEvent]) -> List[Dict[str, Any]]:
        """Detect patterns in events that could become storylines"""
        storylines = []
        
        # Pattern 1: Escalating gang war
        gang_conflicts = [e for e in events if e.event_type == SimulationEventType.GANG_CONFLICT]
        if len(gang_conflicts) >= 2:
            # Check if same gangs are involved
            gang_pairs = set()
            for event in gang_conflicts:
                if event.secondary_entities:
                    pair = tuple(sorted([event.primary_entity, event.secondary_entities[0]]))
                    gang_pairs.add(pair)
            
            for pair in gang_pairs:
                storylines.append({
                    "type": "gang_war",
                    "participants": list(pair),
                    "escalation_level": len([e for e in gang_conflicts if 
                                           e.primary_entity in pair or any(p in pair for p in e.secondary_entities)]),
                    "potential_outcomes": ["total_victory", "stalemate", "law_enforcement_intervention", "character_mediation"]
                })
        
        # Pattern 2: Corporate corruption
        corp_events = [e for e in events if e.event_type == SimulationEventType.CORPORATE_MERGER]
        crime_events = [e for e in events if e.event_type == SimulationEventType.CRIME_COMMITTED]
        
        for corp_event in corp_events:
            related_crimes = [e for e in crime_events if e.territory == corp_event.territory]
            if len(related_crimes) >= 2:
                storylines.append({
                    "type": "corporate_corruption",
                    "corporation": corp_event.primary_entity,
                    "territory": corp_event.territory,
                    "evidence_level": len(related_crimes),
                    "potential_outcomes": ["exposure", "cover_up", "whistleblower_protection", "character_investigation"]
                })
        
        # Pattern 3: Law enforcement corruption
        law_events = [e for e in events if e.event_type == SimulationEventType.LAW_ENFORCEMENT_RESPONSE]
        if len(law_events) >= 3:
            # Check for suspicious patterns
            low_crime_response = [e for e in law_events if e.severity < 4]
            if len(low_crime_response) > len(law_events) * 0.6:  # More than 60% low-severity responses
                storylines.append({
                    "type": "law_enforcement_corruption",
                    "law_unit": law_events[0].primary_entity,
                    "corruption_indicators": len(low_crime_response),
                    "potential_outcomes": ["internal_investigation", "cover_up", "character_exposure", "reform"]
                })
        
        return storylines
    
    def _cleanup_old_events(self):
        """Remove events older than a certain threshold"""
        cutoff_date = self.current_time - timedelta(days=30)
        self.events = [e for e in self.events if e.timestamp > cutoff_date]
        
        # Clean up old storylines
        storylines_to_remove = []
        for storyline_id, storyline in self.active_storylines.items():
            if random.random() < 0.1:  # 10% chance to resolve each hour
                storylines_to_remove.append(storyline_id)
        
        for storyline_id in storylines_to_remove:
            del self.active_storylines[storyline_id]
    
    def _establish_initial_relationships(self, dynasty: DynastyType):
        """Establish initial relationships between entities"""
        dynasty_entities = [e for e in self.entities.values() if e.dynasty == dynasty]
        
        for i, entity1 in enumerate(dynasty_entities):
            for entity2 in dynasty_entities[i+1:]:
                # Determine relationship based on entity types
                relationship_strength = self._calculate_initial_relationship(entity1, entity2)
                
                if relationship_strength != 0:
                    rel_type = "cooperation" if relationship_strength > 0 else "conflict"
                    entity1.add_relationship(entity2.entity_id, rel_type, relationship_strength)
                    entity2.add_relationship(entity1.entity_id, rel_type, relationship_strength)
    
    def _calculate_initial_relationship(self, entity1: BaseEntity, entity2: BaseEntity) -> int:
        """Calculate initial relationship strength between two entities"""
        # Law enforcement vs criminals
        if isinstance(entity1, LawEnforcementUnit) and isinstance(entity2, (CriminalSyndicate, StreetGang)):
            return -random.randint(60, 90)
        if isinstance(entity2, LawEnforcementUnit) and isinstance(entity1, (CriminalSyndicate, StreetGang)):
            return -random.randint(60, 90)
        
        # Criminal vs criminal (potential conflict)
        if isinstance(entity1, (CriminalSyndicate, StreetGang)) and isinstance(entity2, (CriminalSyndicate, StreetGang)):
            # Check for territory overlap
            overlap = len(set(entity1.territories) & set(entity2.territories))
            if overlap > 0:
                return -random.randint(30, 70)  # Territorial conflict
            else:
                return random.randint(-20, 20)  # Neutral to slight conflict
        
        # Corporation relationships
        if isinstance(entity1, Corporation) and isinstance(entity2, Corporation):
            return random.randint(-30, 50)  # Competitive to cooperative
        
        if isinstance(entity1, Corporation) and isinstance(entity2, LawEnforcementUnit):
            return random.randint(20, 60)  # Generally cooperative
        
        if isinstance(entity1, Corporation) and isinstance(entity2, (CriminalSyndicate, StreetGang)):
            return random.randint(-40, 10)  # Generally negative, some corruption
        
        return 0  # Neutral
    
    def _get_dynasty_enhancement_acceptance(self, dynasty: DynastyType) -> int:
        """Get dynasty-specific enhancement acceptance level"""
        acceptance_levels = {
            DynastyType.NEURAL_COLLECTIVE: 9,
            DynastyType.SERAPHIC_CONCORD: 4,
            DynastyType.CELESTIAL_SYNOD: 8,
            DynastyType.CHROME_MANDARINS: 10,
            DynastyType.QUANTUM_CHORUS: 7,
            DynastyType.INFERNAL_DYNASTY: 2
        }
        
        return acceptance_levels.get(dynasty, 5)

# ============================================================================
# CHARACTER INTERACTION INTEGRATION
# ============================================================================

class CharacterStoryIntegration:
    """Integrates character actions with street-level simulation and story generation"""
    
    def __init__(self, simulation: StreetLevelSimulation):
        self.simulation = simulation
        self.character_reputations: Dict[str, Dict[str, int]] = {}  # character_id -> {entity_id: reputation}
        self.character_relationships: Dict[str, List[EntityRelationship]] = {}
        self.character_storylines: Dict[str, List[str]] = {}  # character_id -> [storyline_ids]
    
    def register_character(self, character_id: str, starting_territory: str):
        """Register a character in the street-level system"""
        self.character_reputations[character_id] = {}
        self.character_relationships[character_id] = []
        self.character_storylines[character_id] = []
        
        # Establish initial relationships with local entities
        local_entities = self.simulation.character_system.find_entities_in_territory(starting_territory)
        for entity in local_entities:
            initial_rep = random.randint(40, 60)  # Neutral starting reputation
            self.character_reputations[character_id][entity.entity_id] = initial_rep
    
    def process_character_action(self, character_id: str, action_type: str, target_entity_id: str, 
                                success: bool, consequences: Dict[str, Any]) -> Dict[str, Any]:
        """Process a character's action and its consequences"""
        if target_entity_id not in self.simulation.entities:
            return {"error": "Entity not found"}
        
        target_entity = self.simulation.entities[target_entity_id]
        
        # Calculate reputation changes
        reputation_change = self._calculate_reputation_change(action_type, success, consequences)
        
        # Update character's reputation with the entity
        if character_id not in self.character_reputations:
            self.character_reputations[character_id] = {}
        
        current_rep = self.character_reputations[character_id].get(target_entity_id, 50)
        new_rep = max(0, min(100, current_rep + reputation_change))
        self.character_reputations[character_id][target_entity_id] = new_rep
        
        # Update relationships with related entities
        self._propagate_reputation_changes(character_id, target_entity_id, reputation_change)
        
        # Generate story consequences
        story_consequences = self._generate_story_consequences(character_id, action_type, target_entity_id, success)
        
        # Check for new storyline opportunities
        new_storylines = self._check_storyline_opportunities(character_id, action_type, target_entity_id)
        
        return {
            "reputation_change": reputation_change,
            "new_reputation": new_rep,
            "story_consequences": story_consequences,
            "new_storylines": new_storylines,
            "related_entities_affected": len([e for e in target_entity.relationships if abs(e.strength) > 50])
        }
    
    def get_character_opportunities(self, character_id: str, character_profile: Dict[str, Any]) -> Dict[str, List]:
        """Get available opportunities for a character"""
        opportunities = self.simulation.character_system.get_character_opportunities(character_id, character_profile)
        
        # Add storyline-based opportunities
        character_storylines = self.character_storylines.get(character_id, [])
        storyline_opportunities = []
        
        for storyline_id in character_storylines:
            if storyline_id in self.simulation.active_storylines:
                storyline = self.simulation.active_storylines[storyline_id]
                storyline_opportunities.extend(self._generate_storyline_opportunities(storyline, character_profile))
        
        opportunities["storyline_missions"] = storyline_opportunities
        
        return opportunities
    
    def get_character_reputation_summary(self, character_id: str) -> Dict[str, Any]:
        """Get a summary of character's reputation with various entities"""
        if character_id not in self.character_reputations:
            return {}
        
        reputation_summary = {}
        reputations = self.character_reputations[character_id]
        
        for entity_id, reputation in reputations.items():
            if entity_id in self.simulation.entities:
                entity = self.simulation.entities[entity_id]
                reputation_summary[entity_id] = {
                    "entity_name": entity.name,
                    "entity_type": entity.organization_type.value,
                    "reputation": reputation,
                    "standing": self._get_reputation_standing(reputation),
                    "territories": entity.territories
                }
        
        return reputation_summary
    
    def _calculate_reputation_change(self, action_type: str, success: bool, consequences: Dict[str, Any]) -> int:
        """Calculate reputation change based on action"""
        base_change = 5 if success else -10
        
        action_modifiers = {
            "help": 15,
            "betray": -30,
            "complete_mission": 20,
            "fail_mission": -15,
            "protect": 25,
            "attack": -40,
            "negotiate": 10,
            "expose_corruption": -50,  # Negative with corrupt entity, positive with law enforcement
            "assist_law_enforcement": 30,
            "commit_crime": -20
        }
        
        modifier = action_modifiers.get(action_type, 0)
        
        # Additional modifiers based on consequences
        if consequences.get("violence_used", False):
            modifier -= 10
        if consequences.get("civilians_helped", False):
            modifier += 10
        if consequences.get("property_damage", 0) > 0:
            modifier -= consequences["property_damage"] // 1000  # Damage in credits
        
        return base_change + modifier
    
    def _propagate_reputation_changes(self, character_id: str, target_entity_id: str, reputation_change: int):
        """Propagate reputation changes to related entities"""
        if target_entity_id not in self.simulation.entities:
            return
        
        target_entity = self.simulation.entities[target_entity_id]
        
        # Propagate to allied entities (positive relationship)
        for relationship in target_entity.get_allies():
            related_entity_id = relationship.target_id
            if related_entity_id in self.simulation.entities:
                # Allies gain/lose reputation based on strength of alliance
                propagated_change = int(reputation_change * (relationship.strength / 100) * 0.5)
                
                current_rep = self.character_reputations[character_id].get(related_entity_id, 50)
                new_rep = max(0, min(100, current_rep + propagated_change))
                self.character_reputations[character_id][related_entity_id] = new_rep
        
        # Propagate to enemy entities (negative relationship)
        for relationship in target_entity.get_enemies():
            related_entity_id = relationship.target_id
            if related_entity_id in self.simulation.entities:
                # Enemies gain reputation when you lose it with their enemy, and vice versa
                propagated_change = int(-reputation_change * (abs(relationship.strength) / 100) * 0.3)
                
                current_rep = self.character_reputations[character_id].get(related_entity_id, 50)
                new_rep = max(0, min(100, current_rep + propagated_change))
                self.character_reputations[character_id][related_entity_id] = new_rep
    
    def _generate_story_consequences(self, character_id: str, action_type: str, target_entity_id: str, success: bool) -> List[str]:
        """Generate story consequences from character actions"""
        consequences = []
        
        if not success:
            consequences.append(f"Failed {action_type} may have long-term repercussions")
            consequences.append(f"Target entity {target_entity_id} now aware of character {character_id}")
        
        if action_type == "expose_corruption":
            if success:
                consequences.append("Media attention attracted")
                consequences.append("Other corrupt entities may target character")
                consequences.append("Law enforcement may offer protection")
            else:
                consequences.append("Cover-up attempt likely")
                consequences.append("Character marked for retaliation")
        
        elif action_type == "betray":
            consequences.append("Trust permanently damaged")
            consequences.append("Former allies may become enemies")
            consequences.append("New opportunities with rival factions")
        
        elif action_type == "protect":
            if success:
                consequences.append("Protected entity becomes ally")
                consequences.append("Enemies of protected entity become hostile")
                consequences.append("Reputation for reliability established")
        
        return consequences
    
    def _check_storyline_opportunities(self, character_id: str, action_type: str, target_entity_id: str) -> List[str]:
        """Check if character action opens new storyline opportunities"""
        opportunities = []
        
        # Check existing storylines for character involvement
        for storyline_id, storyline in self.simulation.active_storylines.items():
            if target_entity_id in storyline.get("participants", []):
                if storyline_id not in self.character_storylines.get(character_id, []):
                    # Character becomes involved in existing storyline
                    opportunities.append(f"Drawn into {storyline['type']} storyline")
                    if character_id not in self.character_storylines:
                        self.character_storylines[character_id] = []
                    self.character_storylines[character_id].append(storyline_id)
        
        # Action-specific storyline triggers
        if action_type == "expose_corruption":
            opportunities.append("Whistleblower protection storyline available")
            opportunities.append("Corruption investigation network accessible")
        
        elif action_type == "commit_crime":
            opportunities.append("Criminal underworld contacts opened")
            opportunities.append("Law enforcement investigation possible")
        
        elif action_type == "assist_law_enforcement":
            opportunities.append("Informant network access available")
            opportunities.append("Special operations recruitment possible")
        
        return opportunities
    
    def _generate_storyline_opportunities(self, storyline: Dict[str, Any], character_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate specific opportunities from a storyline"""
        opportunities = []
        
        storyline_type = storyline["type"]
        
        if storyline_type == "gang_war":
            opportunities.extend([
                {
                    "type": "mediate_gang_conflict",
                    "description": "Attempt to broker peace between warring gangs",
                    "requirements": ["social_skills", "neutral_reputation"],
                    "rewards": ["reputation_with_both_gangs", "territory_influence"],
                    "risks": ["violence", "betrayal"]
                },
                {
                    "type": "exploit_gang_war",
                    "description": "Take advantage of gang conflict for personal gain",
                    "requirements": ["combat_skills", "criminal_contacts"],
                    "rewards": ["resources", "territory_control"],
                    "risks": ["gang_retaliation", "law_enforcement_attention"]
                }
            ])
        
        elif storyline_type == "corporate_corruption":
            opportunities.extend([
                {
                    "type": "investigate_corruption",
                    "description": "Gather evidence of corporate wrongdoing",
                    "requirements": ["investigation_skills", "stealth"],
                    "rewards": ["evidence", "whistleblower_protection"],
                    "risks": ["corporate_retaliation", "frame_job"]
                },
                {
                    "type": "join_corruption",
                    "description": "Become part of the corrupt network",
                    "requirements": ["low_morality", "useful_skills"],
                    "rewards": ["money", "corporate_protection"],
                    "risks": ["legal_consequences", "moral_degradation"]
                }
            ])
        
        elif storyline_type == "law_enforcement_corruption":
            opportunities.extend([
                {
                    "type": "expose_corrupt_cops",
                    "description": "Gather evidence against corrupt law enforcement",
                    "requirements": ["investigation_skills", "courage"],
                    "rewards": ["justice", "clean_cop_allies"],
                    "risks": ["police_harassment", "frame_job"]
                },
                {
                    "type": "work_with_corruption",
                    "description": "Benefit from law enforcement corruption",
                    "requirements": ["criminal_contacts", "money"],
                    "rewards": ["protection", "information"],
                    "risks": ["deeper_corruption", "exposure"]
                }
            ])
        
        return opportunities
    
    def _get_reputation_standing(self, reputation: int) -> str:
        """Convert numeric reputation to descriptive standing"""
        if reputation >= 80:
            return "Highly Trusted"
        elif reputation >= 60:
            return "Trusted"
        elif reputation >= 40:
            return "Neutral"
        elif reputation >= 20:
            return "Distrusted"
        else:
            return "Hostile"

# ============================================================================
# EXPORT INTERFACE
# ============================================================================

__all__ = [
    'SimulationEventType',
    'SimulationEvent', 
    'TerritoryState',
    'StreetLevelSimulation',
    'CharacterStoryIntegration'
]
