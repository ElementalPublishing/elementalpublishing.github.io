"""
Street Level Entity Framework for Cyber Dynasties
=================================================

This module provides the core classes and data structures for all street-level
entities that interact with characters and the simulation engine.

All entities are designed to be:
- Programmatically accessible and modifiable
- Narratively rich with procedural generation hooks
- Compatible with character relationship systems
- Simulation-ready with clear interaction APIs
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple, Any, Union
from enum import Enum
import json
import random
from datetime import datetime

# ============================================================================
# CORE ENUMS AND TYPES
# ============================================================================

class DynastyType(Enum):
    NEURAL_COLLECTIVE = "neural_collective"
    SERAPHIC_CONCORD = "seraphic_concord"
    CELESTIAL_SYNOD = "celestial_synod"
    CHROME_MANDARINS = "chrome_mandarins"
    QUANTUM_CHORUS = "quantum_chorus"
    INFERNAL_DYNASTY = "infernal_dynasty"

class OrganizationType(Enum):
    CRIMINAL_SYNDICATE = "criminal_syndicate"
    LAW_ENFORCEMENT = "law_enforcement"
    CORPORATION = "corporation"
    POLITICAL_MOVEMENT = "political_movement"
    RESISTANCE_CELL = "resistance_cell"
    CULT = "cult"
    GANG = "gang"
    VIGILANTE_GROUP = "vigilante_group"

class SocialClass(Enum):
    EXECUTIVE = "executive"
    PROFESSIONAL = "professional"
    SKILLED_WORKER = "skilled_worker"
    SERVICE_WORKER = "service_worker"
    UNEMPLOYED = "unemployed"
    CRIMINAL = "criminal"
    ENHANCED = "enhanced"
    PURE_HUMAN = "pure_human"

class ViolenceLevel(Enum):
    PEACEFUL = 1
    INTIMIDATION = 2
    MINOR_VIOLENCE = 3
    SERIOUS_VIOLENCE = 4
    LETHAL = 5
    MASS_DESTRUCTION = 6

class LawEnforcementStyle(Enum):
    COMMUNITY_POLICING = "community_policing"
    AUTHORITARIAN = "authoritarian"
    CORPORATE_SECURITY = "corporate_security"
    JUDGE_DREDD = "judge_dredd"
    ANGELIC_GUIDANCE = "angelic_guidance"
    DIGITAL_SURVEILLANCE = "digital_surveillance"

# ============================================================================
# BASE ENTITY CLASSES
# ============================================================================

@dataclass
class EntityRelationship:
    """Represents relationship between any two entities"""
    target_id: str
    relationship_type: str
    strength: int  # -100 to 100
    since: datetime
    is_secret: bool = False
    notes: str = ""
    
    def is_hostile(self) -> bool:
        return self.strength < -30
    
    def is_allied(self) -> bool:
        return self.strength > 60

@dataclass
class Territory:
    """Geographic or jurisdictional area controlled by an entity"""
    name: str
    dynasty: DynastyType
    population: int
    economic_level: int  # 1-10 scale
    crime_level: int  # 1-10 scale
    enhancement_acceptance: int  # 1-10 scale
    controlling_organizations: List[str] = field(default_factory=list)
    contested_by: List[str] = field(default_factory=list)
    special_features: List[str] = field(default_factory=list)

@dataclass
class BaseEntity:
    """Base class for all street-level entities"""
    entity_id: str
    name: str
    dynasty: DynastyType
    organization_type: OrganizationType
    territories: List[str] = field(default_factory=list)
    relationships: List[EntityRelationship] = field(default_factory=list)
    reputation: int = 50  # 0-100 scale
    influence: int = 50  # 0-100 scale
    resources: int = 50  # 0-100 scale
    created_date: datetime = field(default_factory=datetime.now)
    
    # Character interaction hooks
    character_interactions: Dict[str, Any] = field(default_factory=dict)
    story_hooks: List[str] = field(default_factory=list)
    procedural_generation_tags: Set[str] = field(default_factory=set)
    
    def add_relationship(self, target_id: str, rel_type: str, strength: int, is_secret: bool = False):
        """Add or update relationship with another entity"""
        # Remove existing relationship if it exists
        self.relationships = [r for r in self.relationships if r.target_id != target_id]
        # Add new relationship
        self.relationships.append(EntityRelationship(
            target_id=target_id,
            relationship_type=rel_type,
            strength=strength,
            since=datetime.now(),
            is_secret=is_secret
        ))
    
    def get_relationship(self, target_id: str) -> Optional[EntityRelationship]:
        """Get relationship with specific entity"""
        for rel in self.relationships:
            if rel.target_id == target_id:
                return rel
        return None
    
    def get_allies(self) -> List[EntityRelationship]:
        """Get all allied relationships"""
        return [r for r in self.relationships if r.is_allied()]
    
    def get_enemies(self) -> List[EntityRelationship]:
        """Get all hostile relationships"""
        return [r for r in self.relationships if r.is_hostile()]

# ============================================================================
# CRIMINAL ORGANIZATIONS
# ============================================================================

@dataclass
class CriminalSyndicate(BaseEntity):
    """Large-scale criminal organization"""
    primary_activities: List[str] = field(default_factory=list)  # drug_trade, smuggling, protection_rackets, etc.
    violence_level: ViolenceLevel = ViolenceLevel.SERIOUS_VIOLENCE
    law_enforcement_corruption: int = 30  # 0-100 scale
    membership_size: int = 100
    hierarchy_levels: int = 4
    recruitment_style: str = "selective"
    
    # Dynasty-specific criminal focus
    enhancement_trafficking: bool = False
    data_crimes: bool = False
    spiritual_corruption: bool = False
    cosmic_smuggling: bool = False
    
    def can_recruit_character(self, character_background: Dict[str, Any]) -> bool:
        """Determine if this syndicate would recruit a character"""
        # Implementation would check character skills, reputation, etc.
        return True  # Placeholder
    
    def generate_mission_for_character(self, character_level: int) -> Dict[str, Any]:
        """Generate appropriate criminal mission based on character level"""
        missions = {
            1: ["courier_job", "lookout_duty", "collection_run"],
            2: ["protection_racket", "smuggling_operation", "intimidation_job"],
            3: ["heist_planning", "territory_expansion", "rival_elimination"],
            4: ["syndicate_war", "law_enforcement_infiltration", "boss_protection"],
            5: ["inter_dynasty_operations", "cosmic_entity_deals", "reality_crimes"]
        }
        
        available_missions = []
        for level in range(1, min(character_level + 1, 6)):
            available_missions.extend(missions.get(level, []))
        
        mission_type = random.choice(available_missions)
        return {
            "type": mission_type,
            "difficulty": character_level,
            "reward_reputation": character_level * 10,
            "reward_resources": character_level * 25,
            "risk_level": character_level * 15
        }

@dataclass
class StreetGang(BaseEntity):
    """Smaller, territorial criminal group"""
    territory_blocks: int = 5  # Number of city blocks controlled
    primary_racket: str = "protection"  # protection, drugs, smuggling, theft
    gang_colors: Tuple[str, str] = ("red", "black")
    initiation_requirements: List[str] = field(default_factory=list)
    rivalry_intensity: int = 50  # How aggressively they fight other gangs
    
    def get_daily_activities(self) -> List[str]:
        """Generate daily gang activities for simulation"""
        activities = [
            f"collecting_protection_money_on_{random.choice(['main_street', 'industrial_district', 'residential_area'])}",
            f"defending_territory_from_{random.choice(['rival_gang', 'law_enforcement', 'corporate_security'])}",
            f"recruiting_new_members_from_{random.choice(['youth_center', 'unemployment_office', 'underground_clubs'])}",
            f"planning_operation_against_{random.choice(['rival_territory', 'corporate_interests', 'law_enforcement'])}"
        ]
        return random.sample(activities, k=2)

# ============================================================================
# LAW ENFORCEMENT
# ============================================================================

@dataclass
class LawEnforcementUnit(BaseEntity):
    """Police, security, or peacekeeping organization"""
    jurisdiction_type: str = "municipal"  # municipal, corporate, federal, military
    enforcement_style: LawEnforcementStyle = LawEnforcementStyle.COMMUNITY_POLICING
    corruption_level: int = 20  # 0-100 scale
    budget_level: int = 50  # 0-100 scale
    public_trust: int = 60  # 0-100 scale
    
    # Specialized units
    has_enhanced_division: bool = False
    has_cybercrime_unit: bool = False
    has_supernatural_division: bool = False
    has_gang_task_force: bool = True
    
    # Equipment and capabilities
    surveillance_tech_level: int = 5  # 1-10 scale
    combat_readiness: int = 5  # 1-10 scale
    investigation_capability: int = 5  # 1-10 scale
    
    def respond_to_crime(self, crime_type: str, severity: int) -> Dict[str, Any]:
        """Generate law enforcement response to criminal activity"""
        response_time = max(1, 10 - self.budget_level // 10)  # Minutes
        officers_dispatched = min(severity * 2, self.resources // 10)
        
        response = {
            "response_time_minutes": response_time,
            "officers_dispatched": officers_dispatched,
            "equipment_used": self._get_equipment_for_severity(severity),
            "success_probability": self._calculate_success_probability(crime_type, severity)
        }
        
        return response
    
    def _get_equipment_for_severity(self, severity: int) -> List[str]:
        """Determine equipment used based on crime severity"""
        equipment = ["standard_patrol_gear"]
        if severity >= 3:
            equipment.append("tactical_gear")
        if severity >= 5:
            equipment.extend(["swat_team", "enhanced_surveillance"])
        if severity >= 7 and self.has_enhanced_division:
            equipment.append("enhancement_countermeasures")
        return equipment
    
    def _calculate_success_probability(self, crime_type: str, severity: int) -> float:
        """Calculate probability of successfully resolving crime"""
        base_probability = 0.7
        difficulty_modifier = -0.1 * severity
        budget_modifier = 0.003 * self.budget_level
        corruption_modifier = -0.002 * self.corruption_level
        
        return max(0.1, min(0.95, base_probability + difficulty_modifier + budget_modifier + corruption_modifier))

# ============================================================================
# CORPORATIONS
# ============================================================================

@dataclass
class Corporation(BaseEntity):
    """Business entity with varying levels of legitimacy"""
    industry_sector: str = "technology"  # technology, manufacturing, services, entertainment, etc.
    market_share: int = 15  # 0-100 percentage in their sector
    employee_count: int = 1000
    enhancement_policy: str = "optional"  # required, optional, prohibited, encouraged
    
    # Corporate culture and practices
    employee_treatment: int = 50  # 0-100 scale
    environmental_responsibility: int = 50  # 0-100 scale
    legal_compliance: int = 80  # 0-100 scale
    innovation_level: int = 50  # 0-100 scale
    
    # Criminal activities (if any)
    criminal_activities: List[str] = field(default_factory=list)
    shell_companies: List[str] = field(default_factory=list)
    bribery_budget: int = 0
    
    def generate_job_opportunities(self, character_skills: List[str]) -> List[Dict[str, Any]]:
        """Generate job opportunities based on character skills"""
        jobs = []
        
        if "technology" in character_skills:
            jobs.append({
                "position": "Systems Analyst",
                "salary": 75000,
                "requirements": ["technology", "problem_solving"],
                "advancement_potential": "high"
            })
        
        if "social" in character_skills:
            jobs.append({
                "position": "Corporate Relations",
                "salary": 65000,
                "requirements": ["social", "persuasion"],
                "advancement_potential": "medium"
            })
        
        # Always offer entry-level positions
        jobs.append({
            "position": "General Worker",
            "salary": 35000,
            "requirements": [],
            "advancement_potential": "low"
        })
        
        return jobs
    
    def assess_corruption_risk(self, character_morality: int) -> Dict[str, Any]:
        """Assess risk/opportunity for character involvement in corporate crimes"""
        if not self.criminal_activities:
            return {"risk": "none", "opportunities": []}
        
        risk_level = "low"
        if character_morality < 30:
            risk_level = "high"
        elif character_morality < 60:
            risk_level = "medium"
        
        opportunities = []
        if risk_level in ["medium", "high"]:
            opportunities = [
                "money_laundering_operation",
                "data_theft_assignment",
                "competitor_sabotage",
                "regulatory_bribery"
            ]
        
        return {
            "risk": risk_level,
            "opportunities": opportunities,
            "potential_reward": len(self.criminal_activities) * 10000,
            "legal_consequences": "severe" if self.legal_compliance < 40 else "moderate"
        }

# ============================================================================
# SOCIAL CLASS SYSTEM
# ============================================================================

@dataclass
class SocialClassTemplate:
    """Template for generating characters of specific social classes"""
    class_name: SocialClass
    dynasty: DynastyType
    
    # Economic characteristics
    income_range: Tuple[int, int]  # Min, max annual income
    typical_occupations: List[str]
    housing_type: str
    
    # Social characteristics
    education_level: str
    social_mobility: int  # 0-100 scale
    political_influence: int  # 0-100 scale
    
    # Enhancement characteristics
    enhancement_access: int  # 0-100 scale
    enhancement_pressure: int  # 0-100 scale (pressure to enhance)
    
    # Lifestyle and concerns
    daily_concerns: List[str]
    leisure_activities: List[str]
    social_networks: List[str]
    
    # Interaction with other systems
    crime_susceptibility: int  # 0-100 scale
    law_enforcement_trust: int  # 0-100 scale
    corporate_loyalty: int  # 0-100 scale
    
    def generate_character_background(self) -> Dict[str, Any]:
        """Generate background details for a character of this class"""
        income = random.randint(self.income_range[0], self.income_range[1])
        occupation = random.choice(self.typical_occupations)
        
        background = {
            "social_class": self.class_name.value,
            "dynasty": self.dynasty.value,
            "annual_income": income,
            "occupation": occupation,
            "housing": self.housing_type,
            "education": self.education_level,
            "enhancement_status": self._determine_enhancement_status(),
            "primary_concerns": random.sample(self.daily_concerns, k=min(3, len(self.daily_concerns))),
            "social_connections": random.sample(self.social_networks, k=min(2, len(self.social_networks)))
        }
        
        return background
    
    def _determine_enhancement_status(self) -> str:
        """Determine if character is enhanced based on class characteristics"""
        enhancement_roll = random.randint(1, 100)
        if enhancement_roll <= self.enhancement_access:
            return "enhanced"
        else:
            return "pure_human"
    
    def get_interaction_modifiers(self) -> Dict[str, int]:
        """Get modifiers for character interactions with various systems"""
        return {
            "crime_susceptibility": self.crime_susceptibility,
            "law_enforcement_trust": self.law_enforcement_trust,
            "corporate_loyalty": self.corporate_loyalty,
            "social_mobility": self.social_mobility,
            "political_influence": self.political_influence
        }

# ============================================================================
# EMPLOYMENT NETWORK
# ============================================================================

@dataclass
class EmploymentNetwork:
    """Network of job opportunities and career paths"""
    network_id: str
    dynasty: DynastyType
    industry_focus: str
    
    # Available positions by skill level
    entry_level_jobs: List[Dict[str, Any]] = field(default_factory=list)
    skilled_positions: List[Dict[str, Any]] = field(default_factory=list)
    executive_roles: List[Dict[str, Any]] = field(default_factory=list)
    
    # Network characteristics
    hiring_bias: Dict[str, int] = field(default_factory=dict)  # Bias toward certain backgrounds
    advancement_fairness: int = 70  # 0-100 scale
    job_security: int = 60  # 0-100 scale
    
    # Criminal connections
    criminal_infiltration: int = 10  # 0-100 scale
    underground_opportunities: List[str] = field(default_factory=list)
    
    def find_suitable_jobs(self, character_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find jobs suitable for character's skills and background"""
        suitable_jobs = []
        
        character_skills = character_profile.get("skills", [])
        character_education = character_profile.get("education_level", "basic")
        character_class = character_profile.get("social_class", "service_worker")
        
        # Check entry-level jobs
        for job in self.entry_level_jobs:
            if self._meets_requirements(character_skills, character_education, job):
                suitable_jobs.append(job)
        
        # Check skilled positions if qualified
        if character_education in ["advanced", "professional"]:
            for job in self.skilled_positions:
                if self._meets_requirements(character_skills, character_education, job):
                    suitable_jobs.append(job)
        
        # Check executive roles if qualified
        if character_class in ["executive", "professional"] and character_education == "professional":
            for job in self.executive_roles:
                if self._meets_requirements(character_skills, character_education, job):
                    suitable_jobs.append(job)
        
        return suitable_jobs
    
    def _meets_requirements(self, character_skills: List[str], education: str, job: Dict[str, Any]) -> bool:
        """Check if character meets job requirements"""
        required_skills = job.get("required_skills", [])
        required_education = job.get("required_education", "basic")
        
        # Check skill requirements
        skills_met = all(skill in character_skills for skill in required_skills)
        
        # Check education requirements
        education_levels = {"basic": 1, "advanced": 2, "professional": 3}
        education_met = education_levels.get(education, 1) >= education_levels.get(required_education, 1)
        
        return skills_met and education_met
    
    def get_criminal_opportunities(self, character_morality: int) -> List[Dict[str, Any]]:
        """Get criminal job opportunities if character is susceptible"""
        if character_morality > 60 or self.criminal_infiltration < 20:
            return []
        
        opportunities = []
        for opportunity in self.underground_opportunities:
            opportunities.append({
                "type": opportunity,
                "risk": random.randint(30, 80),
                "reward": random.randint(1000, 10000),
                "requirements": ["criminal_contacts", "moral_flexibility"]
            })
        
        return opportunities

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_dynasty_specific_entities(dynasty: DynastyType) -> Dict[str, List[BaseEntity]]:
    """Create dynasty-specific entities with appropriate flavoring"""
    entities = {
        "criminal_syndicates": [],
        "law_enforcement": [],
        "corporations": [],
        "gangs": []
    }
    
    # This would be populated with dynasty-specific templates
    # For now, just return the structure
    return entities

def load_entity_templates(dynasty: DynastyType) -> Dict[str, Any]:
    """Load entity templates from data files"""
    # This would load from JSON/YAML files in the data directories
    # Return empty dict for now
    return {}

def generate_random_entity(entity_type: OrganizationType, dynasty: DynastyType) -> BaseEntity:
    """Generate a random entity of specified type for specified dynasty"""
    # This would use procedural generation rules
    # Return basic entity for now
    return BaseEntity(
        entity_id=f"{dynasty.value}_{entity_type.value}_{random.randint(1000, 9999)}",
        name=f"Generated {entity_type.value.replace('_', ' ').title()}",
        dynasty=dynasty,
        organization_type=entity_type
    )

# ============================================================================
# CHARACTER INTERACTION SYSTEM
# ============================================================================

class CharacterInteractionSystem:
    """System for managing character interactions with street-level entities"""
    
    def __init__(self):
        self.entities: Dict[str, BaseEntity] = {}
        self.territories: Dict[str, Territory] = {}
        self.employment_networks: Dict[str, EmploymentNetwork] = {}
        self.social_class_templates: Dict[str, SocialClassTemplate] = {}
    
    def register_entity(self, entity: BaseEntity):
        """Register an entity in the interaction system"""
        self.entities[entity.entity_id] = entity
    
    def find_entities_in_territory(self, territory_name: str) -> List[BaseEntity]:
        """Find all entities operating in a specific territory"""
        return [entity for entity in self.entities.values() 
                if territory_name in entity.territories]
    
    def get_character_opportunities(self, character_id: str, character_profile: Dict[str, Any]) -> Dict[str, List]:
        """Get all opportunities available to a character"""
        opportunities = {
            "jobs": [],
            "criminal_activities": [],
            "social_connections": [],
            "faction_recruitment": []
        }
        
        character_location = character_profile.get("current_territory", "")
        local_entities = self.find_entities_in_territory(character_location)
        
        for entity in local_entities:
            if isinstance(entity, Corporation):
                opportunities["jobs"].extend(entity.generate_job_opportunities(
                    character_profile.get("skills", [])
                ))
            elif isinstance(entity, CriminalSyndicate):
                if character_profile.get("morality", 50) < 60:
                    opportunities["criminal_activities"].append(
                        entity.generate_mission_for_character(
                            character_profile.get("level", 1)
                        )
                    )
        
        return opportunities
    
    def process_character_action(self, character_id: str, action: str, target_entity_id: str) -> Dict[str, Any]:
        """Process a character's action toward an entity"""
        if target_entity_id not in self.entities:
            return {"success": False, "message": "Entity not found"}
        
        target_entity = self.entities[target_entity_id]
        
        # This would implement the actual action processing logic
        result = {
            "success": True,
            "message": f"Character {character_id} performed {action} on {target_entity.name}",
            "reputation_change": 0,
            "relationship_change": 0,
            "consequences": []
        }
        
        return result

# ============================================================================
# EXPORT INTERFACE
# ============================================================================

__all__ = [
    # Enums
    'DynastyType', 'OrganizationType', 'SocialClass', 'ViolenceLevel', 'LawEnforcementStyle',
    
    # Core classes
    'BaseEntity', 'EntityRelationship', 'Territory',
    
    # Organization types
    'CriminalSyndicate', 'StreetGang', 'LawEnforcementUnit', 'Corporation',
    
    # Social systems
    'SocialClassTemplate', 'EmploymentNetwork',
    
    # Interaction system
    'CharacterInteractionSystem',
    
    # Utility functions
    'create_dynasty_specific_entities', 'load_entity_templates', 'generate_random_entity'
]
