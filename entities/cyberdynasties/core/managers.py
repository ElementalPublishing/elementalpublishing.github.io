from datetime import datetime
from typing import List, Dict, Any, Optional
import json
import os
from pathlib import Path

# Import integrated systems and association network
try:
    from memorymodule import MemoryModule
    from war_engine import WarEngine, load_dynasty_boss_traits
    from narrative_engine import ask_and_answer
    memory_module = MemoryModule()
    war_engine = WarEngine()
    
    # Load association network
    association_network_path = Path(__file__).parent / "archetype_association_network.json"
    if association_network_path.exists():
        with open(association_network_path, 'r', encoding='utf-8') as f:
            ASSOCIATION_NETWORK = json.load(f)
    else:
        ASSOCIATION_NETWORK = {}
        
except ImportError as e:
    print(f"Warning: Could not import required modules: {e}")
    memory_module = None
    war_engine = None
    ask_and_answer = lambda q, c, m: "Narrative engine not available"
    ASSOCIATION_NETWORK = {}

class AssociationManager:
    """
    Manages the spiderweb association network between all archetypes.
    Provides methods for finding connections, influences, and relationships.
    """
    def __init__(self, association_data=None):
        self.network = association_data or ASSOCIATION_NETWORK.get('association_network', {})
        self.archetype_list = ASSOCIATION_NETWORK.get('archetype_list', [])
        self.association_fields = ASSOCIATION_NETWORK.get('association_fields', [])
        
    def get_associations(self, archetype_name: str) -> Dict[str, Any]:
        """Get all associations for a specific archetype."""
        return self.network.get(archetype_name, {})
    
    def find_connected_archetypes(self, archetype_name: str, association_type: str = None) -> List[str]:
        """Find all archetypes connected to the given archetype."""
        connections = set()
        archetype_data = self.network.get(archetype_name, {})
        
        if association_type:
            # Find connections for specific association type
            for field, values in archetype_data.items():
                if association_type in field:
                    if isinstance(values, list):
                        connections.update(v for v in values if v in self.archetype_list)
                    elif values in self.archetype_list:
                        connections.add(values)
        else:
            # Find all connections
            for field, values in archetype_data.items():
                if field.startswith('associated_'):
                    if isinstance(values, list):
                        connections.update(v for v in values if v in self.archetype_list)
                    elif values in self.archetype_list:
                        connections.add(values)
        
        return list(connections)
    
    def find_mutual_associations(self, archetype1: str, archetype2: str) -> Dict[str, List[str]]:
        """Find mutual associations between two archetypes."""
        data1 = self.network.get(archetype1, {})
        data2 = self.network.get(archetype2, {})
        
        mutual = {}
        for field in self.association_fields:
            values1 = set(data1.get(field, []))
            values2 = set(data2.get(field, []))
            common = values1.intersection(values2)
            if common:
                mutual[field] = list(common)
        
        return mutual
    
    def calculate_affinity(self, archetype1: str, archetype2: str) -> float:
        """Calculate association affinity score between two archetypes."""
        mutual = self.find_mutual_associations(archetype1, archetype2)
        if not mutual:
            return 0.0
        
        total_score = 0
        for field, values in mutual.items():
            # Weight different association types differently
            if 'allies' in field or 'mentors' in field:
                total_score += len(values) * 2.0
            elif 'rivals' in field:
                total_score += len(values) * -1.0
            else:
                total_score += len(values) * 1.0
        
        # Normalize by total possible associations
        max_possible = len(self.association_fields)
        return total_score / max_possible if max_possible > 0 else 0.0
    
    def get_influence_network(self, archetype_name: str, depth: int = 2) -> Dict[str, float]:
        """Get influence network radiating from an archetype."""
        influence_map = {}
        visited = set()
        to_visit = [(archetype_name, 1.0, 0)]  # (name, influence, depth)
        
        while to_visit:
            current_name, current_influence, current_depth = to_visit.pop(0)
            
            if current_name in visited or current_depth > depth:
                continue
                
            visited.add(current_name)
            if current_name != archetype_name:
                influence_map[current_name] = current_influence
            
            if current_depth < depth:
                connected = self.find_connected_archetypes(current_name)
                for connected_archetype in connected:
                    if connected_archetype not in visited:
                        # Decay influence by distance
                        new_influence = current_influence * 0.7
                        to_visit.append((connected_archetype, new_influence, current_depth + 1))
        
        return influence_map
    
    def suggest_narrative_connections(self, archetype_name: str) -> Dict[str, List[str]]:
        """Suggest narrative connections based on associations."""
        associations = self.get_associations(archetype_name)
        suggestions = {
            'potential_allies': associations.get('associated_allies', [])[:3],
            'potential_rivals': associations.get('associated_rivals', [])[:3],
            'mentorship_opportunities': associations.get('associated_mentors', [])[:2],
            'symbolic_connections': associations.get('associated_symbols', [])[:5],
            'elemental_affinities': associations.get('associated_elements', [])[:3],
            'temporal_connections': associations.get('associated_times', [])[:3]
        }
        return suggestions

class EpochManager:
    """
    Manages temporal epochs across past, present, and future worlds.
    Integrates with narrative engine, memory systems, and association networks for epoch transitions.
    """
    def __init__(self, epochs: Optional[List[str]] = None, association_manager=None):
        self.epochs = epochs or [
            "Ancient Days", "Pre-Flood", "Flood", "Post-Flood", "Babel",
            "Patriarchs", "Second Age", "Code Wars", "Cyber Dynasties", "Ascension"
        ]
        self.current_index = 0
        self.epoch_memories = {}  # Store epoch-specific memories
        self.epoch_events = {}    # Store epoch-specific events
        self.transition_callbacks = []  # Callbacks for epoch changes
        self.association_manager = association_manager or AssociationManager()
        
        # Track archetype associations per epoch
        self.epoch_associations = {}

    @property
    def current_epoch(self) -> str:
        return self.epochs[self.current_index]

    def register_transition_callback(self, callback):
        """Register callback for epoch transitions"""
        self.transition_callbacks.append(callback)

    def advance_epoch(self, world_system=None):
        """
        Advance to next epoch with full system integration.
        Triggers world changes, entity updates, and memory consolidation.
        """
        if self.current_index < len(self.epochs) - 1:
            old_epoch = self.current_epoch
            self.current_index += 1
            new_epoch = self.current_epoch
            
            # Trigger all registered callbacks
            for callback in self.transition_callbacks:
                callback(old_epoch, new_epoch)
            
            # Integrate with world system if provided
            if world_system:
                self.apply_epoch_transition(world_system, old_epoch, new_epoch)
                
        return self.current_epoch
    
    def apply_epoch_transition(self, world_system, old_epoch, new_epoch):
        """Apply epoch transition effects to world system"""
        # Archive current epoch state to past world
        if hasattr(world_system, 'past_world') and hasattr(world_system, 'present_world'):
            # Transfer some entities from present to past during major epoch changes
            major_transitions = ["Flood", "Code Wars", "Cyber Dynasties"]
            if new_epoch in major_transitions:
                entities_to_archive = world_system.present_world.entities[:2]  # Archive first 2 entities
                for entity in entities_to_archive:
                    world_system.present_world.archive_entity_to_past(entity)
        
        # Apply epoch-specific changes to nature and environment
        if hasattr(world_system, 'nature'):
            world_system.nature.apply_epoch_effects(new_epoch)

        # Update association network for the new epoch
        if hasattr(world_system, 'association_manager'):
            world_system.association_manager = AssociationManager()
            world_system.association_manager.network = world_system.association_manager.network.get(new_epoch, {})
            world_system.association_manager.archetype_list = ASSOCIATION_NETWORK.get('archetype_list', [])
            world_system.association_manager.association_fields = ASSOCIATION_NETWORK.get('association_fields', [])

    def get_epoch_summary(self) -> Dict[str, Any]:
        """Get comprehensive summary of current epoch state"""
        return {
            "current_epoch": self.current_epoch,
            "epoch_index": self.current_index,
            "total_epochs": len(self.epochs),
            "memories": self.epoch_memories.get(self.current_epoch, []),
            "events": self.epoch_events.get(self.current_epoch, [])
        }

    def reset(self):
        self.current_index = 0

class EventManager:
    """
    Manages events across temporal worlds with full system integration.
    Events trigger memory formation, narrative updates, and world state changes.
    Now includes association-based event propagation and relationship effects.
    """
    def __init__(self, association_manager=None):
        self.events: List[Dict[str, Any]] = []
        self.on_event = None  # Callback for event triggers
        self.world_system = None  # Reference to world system
        self.memory_module = None  # Reference to memory system
        self.narrative_callbacks = []  # Callbacks for narrative updates
        self.association_manager = association_manager or AssociationManager()

    def initialize_system_integration(self, world_system, memory_module):
        """Initialize integration with world and memory systems"""
        self.world_system = world_system
        self.memory_module = memory_module

    def register_callback(self, callback):
        self.on_event = callback

    def register_narrative_callback(self, callback):
        """Register callback for narrative-driven events"""
        self.narrative_callbacks.append(callback)

    def log_event(self, epoch: str, description: str, entities: Optional[List[str]] = None, 
                  motif: Optional[str] = None, world_impact: str = "minor", 
                  emotional_weight: float = 0.5, propagate_associations: bool = True):
        """
        Log an event with association-based propagation to connected archetypes.
        """
        event = {
            "epoch": epoch,
            "description": description,
            "entities": entities or [],
            "timestamp": datetime.utcnow().isoformat(),
            "motif": motif,
            "world_impact": world_impact,
            "emotional_weight": emotional_weight,
            "event_id": len(self.events)
        }
        self.events.append(event)
        
        # Process event through integrated systems
        self._process_event_integration(event)
        
        # Trigger callback if set
        if self.on_event:
            self.on_event(event)

    def _process_event_integration(self, event):
        """Process event through all integrated systems including association propagation"""
        # 1. Create memories for involved entities
        if self.memory_module and self.world_system:
            self._create_event_memories(event)
        
        # 2. Process association-based event propagation
        if event.get("propagate_associations", True):
            self._propagate_event_through_associations(event)
        
        # 3. Apply world impact
        if self.world_system:
            self._apply_world_impact(event)
        
        # 4. Trigger narrative callbacks
        for callback in self.narrative_callbacks:
            callback(event)
    
    def _propagate_event_through_associations(self, event):
        """Propagate event effects through the association network"""
        primary_entities = event.get("entities", [])
        
        for entity_name in primary_entities:
            # Get connected archetypes
            connected = self.association_manager.find_connected_archetypes(entity_name)
            
            # Create secondary events for closely connected archetypes
            allies = self.association_manager.get_associations(entity_name).get('associated_allies', [])
            rivals = self.association_manager.get_associations(entity_name).get('associated_rivals', [])
            
            # Allies experience sympathetic effects
            for ally in allies[:3]:  # Limit to top 3 allies
                if ally in connected:
                    secondary_event = {
                        "epoch": event["epoch"],
                        "type": "association_resonance",
                        "description": f"{ally} feels the echoes of {entity_name}'s experience: {event['description']}",
                        "entities": [ally],
                        "motif": event.get("motif", "resonance"),
                        "world_impact": "minor",
                        "emotional_weight": event["emotional_weight"] * 0.5,
                        "primary_event": event["description"],
                        "association_type": "ally_resonance",
                        "propagate_associations": False  # Prevent infinite recursion
                    }
                    self.events.append(secondary_event)
            
            # Rivals experience opposing effects
            for rival in rivals[:2]:  # Limit to top 2 rivals
                if rival in connected:
                    opposing_weight = -event["emotional_weight"] * 0.3
                    secondary_event = {
                        "epoch": event["epoch"],
                        "type": "association_opposition",
                        "description": f"{rival} feels opposition to {entity_name}'s experience: {event['description']}",
                        "entities": [rival],
                        "motif": "rivalry",
                        "world_impact": "minor",
                        "emotional_weight": opposing_weight,
                        "primary_event": event["description"],
                        "association_type": "rival_opposition",
                        "propagate_associations": False
                    }
                    self.events.append(secondary_event)

    def _create_event_memories(self, event):
        """Create memories for entities involved in the event"""
        if not hasattr(self.world_system, 'present_world'):
            return
            
        for entity_name in event["entities"]:
            # Find entity in present world
            entity = None
            for e in self.world_system.present_world.entities:
                if e.get("name") == entity_name:
                    entity = e
                    break
            
            if entity:
                # Create memory using memory module
                memory_content = f"Event: {event['description']} during {event['epoch']}"
                if hasattr(self.memory_module, 'create_brain_memory'):
                    memory = self.memory_module.create_brain_memory(
                        content=memory_content,
                        emotional_weight=event["emotional_weight"],
                        memory_type="episodic"
                    )
                    
                    # Add to entity's memory if it has a brain
                    if entity.get("brain") and hasattr(entity["brain"], "memories"):
                        entity["brain"].memories.append(memory)

    def _apply_world_impact(self, event):
        """Apply event impact to world state"""
        impact = event["world_impact"]
        
        if impact == "major":
            # Major events affect all worlds
            worlds = [self.world_system.past_world, self.world_system.present_world]
            for world in worlds:
                if world:
                    world.record_pain(f"Major event: {event['description']}")
        elif impact == "moderate":
            # Moderate events affect present world
            if self.world_system.present_world:
                self.world_system.present_world.record_pain(f"Event: {event['description']}")

    def get_events(self, epoch: Optional[str] = None, entity: Optional[str] = None, 
                   motif: Optional[str] = None) -> List[Dict[str, Any]]:
        """Enhanced event filtering with multiple criteria"""
        filtered_events = self.events
        
        if epoch:
            filtered_events = [e for e in filtered_events if e["epoch"] == epoch]
        if entity:
            filtered_events = [e for e in filtered_events if entity in e["entities"]]
        if motif:
            filtered_events = [e for e in filtered_events if e["motif"] == motif]
            
        return filtered_events

    def get_narrative_summary(self, epoch: Optional[str] = None) -> str:
        """Generate narrative summary of events"""
        events = self.get_events(epoch=epoch)
        if not events:
            return "No significant events recorded."
        
        summary = [f"Chronicle of Events - {epoch or 'All Times'}:"]
        for event in events[-10:]:  # Last 10 events
            summary.append(f"- {event['epoch']}: {event['description']}")
            if event["motif"]:
                summary.append(f"  Motif: {event['motif']}")
        
        return "\n".join(summary)

    def clear(self):
        self.events.clear()

class ActionsManager:
    """
    Manages entity actions with full integration to brains, memory, narrative systems,
    and association networks. Actions now propagate through relationship webs and
    trigger cascading effects based on archetype connections.
    """
    def __init__(self, association_manager=None):
        self.actions: List[Dict[str, Any]] = []
        self.memory_module = None
        self.event_manager = None
        self.world_system = None
        self.association_manager = association_manager or AssociationManager()

    def initialize_system_integration(self, memory_module, event_manager, world_system):
        """Initialize integration with other managers and systems"""
        self.memory_module = memory_module
        self.event_manager = event_manager
        self.world_system = world_system

    def log_action(self, entity: dict, action: str, target: Optional[dict] = None, 
                   epoch: Optional[str] = None, details: Optional[dict] = None,
                   narrative_context: Optional[str] = None, propagate_associations: bool = True):
        """
        Enhanced action logging with full system integration and association propagation.
        Actions now trigger brain updates, memory formation, narrative responses, and
        relationship-based cascading effects throughout the association network.
        """
        entity_name = entity.get("name") if isinstance(entity, dict) else str(entity)
        target_name = target.get("name") if isinstance(target, dict) else (str(target) if target else None)
        
        act = {
            "entity": entity_name,
            "action": action,
            "target": target_name,
            "epoch": epoch,
            "details": details or {},
            "narrative_context": narrative_context,
            "timestamp": datetime.utcnow().isoformat(),
            "action_id": len(self.actions)
        }
        self.actions.append(act)

        # Process action through integrated systems
        self._process_action_integration(act, entity, target, propagate_associations)

    def _process_action_integration(self, action_record, entity, target, propagate_associations):
        """Process action through all integrated systems"""
        # 1. Motif Detection using memory module
        motifs = []
        if self.memory_module and hasattr(self.memory_module, 'extract_motifs_from_content'):
            action_content = f"{action_record['action']} {action_record.get('narrative_context', '')}"
            motifs = self.memory_module.extract_motifs_from_content(action_content)

        # 2. Brain and Memory Updates
        if isinstance(entity, dict):
            self._update_entity_from_action(entity, action_record, motifs)
        if isinstance(target, dict):
            self._update_entity_from_action(target, action_record, motifs, is_target=True)

        # 3. Log Related Event
        if self.event_manager:
            description = f"{action_record['entity']} performed {action_record['action']}"
            if action_record["target"]:
                description += f" on {action_record['target']}"
            
            emotional_weight = self._calculate_action_emotional_weight(action_record, motifs)
            
            self.event_manager.log_event(
                epoch=action_record["epoch"],
                description=description,
                entities=[action_record["entity"]] + ([action_record["target"]] if action_record["target"] else []),
                motif=",".join(motifs) if motifs else None,
                emotional_weight=emotional_weight
            )

        # 4. Apply Motif State Changes
        if self.memory_module and hasattr(self.memory_module, 'apply_motif_state_changes'):
            entities_to_update = [entity] + ([target] if target else [])
            for motif in motifs:
                self.memory_module.apply_motif_state_changes(motif, entities_to_update)

        # 5. Propagate Action Effects through Associations
        if propagate_associations:
            self._propagate_action_through_associations(action_record, entity, target, motifs)

    def _propagate_action_through_associations(self, action_record, entity, target, motifs):
        """Propagate action effects through the association network"""
        entity_name = action_record["entity"]
        target_name = action_record.get("target")
        
        # Get entity's associations
        associations = self.association_manager.get_associations(entity_name)
        
        # Propagate to allies (positive reinforcement)
        allies = associations.get('associated_allies', [])
        for ally in allies[:3]:  # Limit to top 3 allies
            self._create_association_action_effect(ally, entity_name, action_record, "ally_support", 0.6)
        
        # Propagate to rivals (competitive response)
        rivals = associations.get('associated_rivals', [])
        for rival in rivals[:2]:  # Limit to top 2 rivals
            self._create_association_action_effect(rival, entity_name, action_record, "rival_response", -0.4)
        
        # Propagate to mentors (approval/disapproval)
        mentors = associations.get('associated_mentors', [])
        for mentor in mentors[:2]:
            effect_type = "mentor_approval" if any(m in ["virtue", "wisdom", "justice"] for m in motifs) else "mentor_concern"
            strength = 0.8 if effect_type == "mentor_approval" else -0.3
            self._create_association_action_effect(mentor, entity_name, action_record, effect_type, strength)
        
        # Propagate to students (learning effect)
        students = associations.get('associated_students', [])
        for student in students[:3]:
            self._create_association_action_effect(student, entity_name, action_record, "student_learning", 0.5)
    
    def _create_association_action_effect(self, affected_entity, acting_entity, original_action, effect_type, strength):
        """Create a secondary action effect for an associated entity"""
        effect_action = {
            "entity": affected_entity,
            "action": f"responds to {acting_entity}'s {original_action['action']}",
            "target": None,
            "epoch": original_action.get("epoch"),
            "details": {
                "association_type": effect_type,
                "original_actor": acting_entity,
                "original_action": original_action["action"],
                "effect_strength": strength,
                "propagated": True
            },
            "timestamp": datetime.now().isoformat(),
            "narrative_context": f"Association-based response to {acting_entity}'s actions"
        }
        
        self.actions.append(effect_action)
        
        # Create memory for the affected entity if memory system is available
        if self.memory_module:
            memory_description = f"Felt the influence of {acting_entity}'s action: {original_action['action']}"
            emotional_weight = abs(strength)
            
            # This would require the entity object, simplified for now
            memory_record = {
                "event": memory_description,
                "motif": effect_type,
                "vividness": emotional_weight,
                "timestamp": effect_action["timestamp"],
                "association_triggered": True
            }
            
            # Note: Would need proper entity object to append memory
            # self.memory_module.append_memory(entity_object, memory_record)

    def _update_entity_from_action(self, entity, action_record, motifs, is_target=False):
        """Update entity's brain and memory from action"""
        # Create memory of the action
        if self.memory_module and hasattr(self.memory_module, 'create_brain_memory'):
            perspective = "witnessed" if is_target else "performed"
            memory_content = f"I {perspective} the action: {action_record['action']}"
            
            memory = self.memory_module.create_brain_memory(
                content=memory_content,
                emotional_weight=self._calculate_action_emotional_weight(action_record, motifs),
                memory_type="episodic"
            )
            
            # Add to entity's brain if it has one
            if entity.get("brain") and hasattr(entity["brain"], "memories"):
                entity["brain"].memories.append(memory)

        # Update brain's neural state based on action
        if entity.get("brain") and hasattr(entity["brain"], "mental_state"):
            self._update_brain_from_action(entity["brain"], action_record, motifs, is_target)

    def _update_brain_from_action(self, brain, action_record, motifs, is_target):
        """Update brain's mental state based on action performed or witnessed"""
        action = action_record["action"].lower()
        mental_state = brain.mental_state
        
        # Action-specific brain updates
        if "attack" in action or "fight" in action:
            if not is_target:
                mental_state["arousal"] = min(2.0, mental_state.get("arousal", 0.5) + 0.3)
                mental_state["stress_level"] = min(2.0, mental_state.get("stress_level", 0.5) + 0.2)
            else:
                mental_state["fear_response"] = min(2.0, mental_state.get("fear_response", 0.5) + 0.4)
                mental_state["stress_level"] = min(2.0, mental_state.get("stress_level", 0.5) + 0.3)
        
        elif "heal" in action or "help" in action:
            mental_state["mood"] = min(2.0, mental_state.get("mood", 0.5) + 0.2)
            mental_state["social_drive"] = min(2.0, mental_state.get("social_drive", 0.5) + 0.1)
        
        elif "learn" in action or "study" in action:
            mental_state["learning_rate"] = min(2.0, mental_state.get("learning_rate", 0.5) + 0.2)
            mental_state["attention_span"] = min(2.0, mental_state.get("attention_span", 0.5) + 0.1)

    def _calculate_action_emotional_weight(self, action_record, motifs):
        """Calculate emotional significance of an action"""
        base_weight = 0.5
        action = action_record["action"].lower()
        
        # High emotional weight actions
        if any(word in action for word in ["attack", "betray", "sacrifice", "love", "hate"]):
            base_weight += 0.3
        
        # Motif-based adjustments
        if motifs:
            if any(motif in ["trauma", "betrayal", "loss"] for motif in motifs):
                base_weight += 0.2
            elif any(motif in ["victory", "love", "redemption"] for motif in motifs):
                base_weight += 0.1
        
        return min(1.0, base_weight)

    def generate_action_narrative(self, entity, narrative_engine=None, context=None):
        """
        Generate narrative description of entity's recent actions.
        Integrates with narrative engine for philosophical reflection.
        """
        entity_name = entity.get("name") if isinstance(entity, dict) else str(entity)
        recent_actions = [a for a in self.actions[-10:] if a["entity"] == entity_name]
        
        if not recent_actions:
            return f"{entity_name} has taken no significant actions recently."
        
        narrative = [f"Recent actions of {entity_name}:"]
        for action in recent_actions:
            narrative.append(f"- {action['action']}")
            if action.get("narrative_context"):
                narrative.append(f"  Context: {action['narrative_context']}")
        
        # Add philosophical reflection if narrative engine available
        if narrative_engine and callable(narrative_engine):
            question = f"What do these actions reveal about {entity_name}'s character?"
            reflection = narrative_engine(question, {"entity": entity, "actions": recent_actions})
            narrative.append(f"\nReflection: {reflection}")
        
        return "\n".join(narrative)

    def get_actions(self, entity: Optional[str] = None, action_type: Optional[str] = None,
                    epoch: Optional[str] = None) -> List[Dict[str, Any]]:
        """Enhanced action filtering with multiple criteria"""
        filtered_actions = self.actions
        
        if entity:
            filtered_actions = [a for a in filtered_actions if a["entity"] == entity]
        if action_type:
            filtered_actions = [a for a in filtered_actions if action_type.lower() in a["action"].lower()]
        if epoch:
            filtered_actions = [a for a in filtered_actions if a["epoch"] == epoch]
            
        return filtered_actions
    
    def get_action_summary(self, entity: Optional[str] = None) -> Dict[str, Any]:
        """Get comprehensive summary of actions"""
        actions = self.get_actions(entity=entity)
        
        return {
            "total_actions": len(actions),
            "unique_entities": len(set(a["entity"] for a in actions)),
            "action_types": list(set(a["action"] for a in actions)),
            "recent_actions": actions[-5:],  # Last 5 actions
            "most_active_entity": max(set(a["entity"] for a in actions), 
                                    key=lambda x: sum(1 for a in actions if a["entity"] == x)) if actions else None
        }

class WorldSystemManager:
    """
    Master manager that orchestrates all systems and provides unified interface.
    Connects past/present/future worlds with all managers and systems.
    Now includes comprehensive association network integration.
    """
    def __init__(self):
        # Initialize association network first
        self.association_manager = AssociationManager()
        
        # Initialize all managers with association support
        self.epoch_manager = EpochManager(association_manager=self.association_manager)
        self.event_manager = EventManager(association_manager=self.association_manager)
        self.actions_manager = ActionsManager(association_manager=self.association_manager)
        self.war_engine = WarEngine()
        
        # System references
        self.memory_module = None
        self.past_world = None
        self.present_world = None
        self.future_world = None
        self.nature = None
        self.entities = []
        self.simulation_running = False

    def initialize_systems(self, memory_module, past_world, present_world, future_world=None, nature=None):
        """Initialize all system integrations"""
        self.memory_module = memory_module
        self.past_world = past_world
        self.present_world = present_world
        self.future_world = future_world
        self.nature = nature

        # Cross-wire all managers
        self.event_manager.initialize_system_integration(self, memory_module)
        self.actions_manager.initialize_system_integration(memory_module, self.event_manager, self)
        
        # Register epoch transition callbacks
        self.epoch_manager.register_transition_callback(self._on_epoch_transition)
        
        # Register narrative event callbacks
        self.event_manager.register_narrative_callback(self._on_narrative_event)

    def _on_epoch_transition(self, old_epoch, new_epoch):
        """Handle epoch transitions across all systems"""
        print(f"🌟 Epoch Transition: {old_epoch} → {new_epoch}")
        
        # Apply world changes
        if self.nature:
            self.nature.apply_epoch_effects(new_epoch)
        
        # Update all entity memories about the transition
        transition_event = f"The world has entered the epoch of {new_epoch}"
        for entity in self.entities:
            if self.memory_module:
                memory = self.memory_module.create_brain_memory(
                    content=transition_event,
                    emotional_weight=0.8,
                    memory_type="world"
                )
                if entity.get("brain") and hasattr(entity["brain"], "memories"):
                    entity["brain"].memories.append(memory)

    def _on_narrative_event(self, event):
        """Handle narrative-driven events"""
        # Generate narrative responses for major events
        if event.get("world_impact") == "major":
            print(f"📖 Major Event: {event['description']}")
            
            # Trigger philosophical reflections for involved entities
            for entity_name in event["entities"]:
                entity = self.find_entity(entity_name)
                if entity:
                    self._trigger_entity_reflection(entity, event)

    def _trigger_entity_reflection(self, entity, event):
        """Trigger philosophical reflection for an entity about an event"""
        try:
            question = f"How does this event change your understanding of existence?"
            context = {"entity": entity, "event": event}
            
            # Use narrative engine if available
            reflection = ask_and_answer(question, context, self.memory_module)
            
            # Store reflection as memory
            if self.memory_module:
                memory = self.memory_module.create_brain_memory(
                    content=f"Reflection on {event['description']}: {reflection}",
                    emotional_weight=event.get("emotional_weight", 0.7),
                    memory_type="philosophical"
                )
                if entity.get("brain") and hasattr(entity["brain"], "memories"):
                    entity["brain"].memories.append(memory)
                    
        except Exception as e:
            print(f"Error in entity reflection: {e}")

    def add_entity(self, entity):
        """Add entity to the world system with association network registration"""
        self.entities.append(entity)
        if self.present_world:
            self.present_world.add_entity(entity)
        
        # Register entity in association network if it exists
        entity_name = entity.get("name")
        if entity_name and entity_name in self.association_manager.archetype_list:
            print(f"✨ Registered {entity_name} with association network")

    def find_entity(self, name):
        """Find entity by name with association-aware lookup"""
        # Standard lookup
        for entity in self.entities:
            if entity.get("name") == name:
                return entity
        
        # Check if it's a known archetype for future spawning
        if name in self.association_manager.archetype_list:
            print(f"🔍 {name} is a known archetype but not currently active")
        
        return None
    
    def get_entity_associations(self, entity_name: str) -> Dict[str, Any]:
        """Get association data for an entity"""
        return self.association_manager.get_associations(entity_name)
    
    def get_entity_influence_network(self, entity_name: str, depth: int = 2) -> Dict[str, float]:
        """Get the influence network for an entity"""
        return self.association_manager.get_influence_network(entity_name, depth)
    
    def suggest_narrative_connections(self, entity_name: str) -> Dict[str, List[str]]:
        """Suggest narrative connections for an entity based on associations"""
        return self.association_manager.suggest_narrative_connections(entity_name)
    
    def calculate_relationship_strength(self, entity1: str, entity2: str) -> float:
        """Calculate relationship strength between two entities"""
        return self.association_manager.calculate_affinity(entity1, entity2)

    def simulate_tick(self):
        """Advance simulation by one tick"""
        if not self.simulation_running:
            return
        
        # Advance time in all worlds
        if self.present_world:
            self.present_world.advance_time()
        if self.past_world:
            self.past_world.advance_time()
        
        # Process war engine
        if hasattr(self.war_engine, 'tick'):
            try:
                traits_lookup = {}  # You might want to build this from entities
                self.war_engine.tick(traits_lookup, self.epoch_manager.current_epoch)
            except:
                pass  # Graceful handling if war engine isn't properly configured
        
        # Random events (10% chance per tick)
        if __import__('random').random() < 0.1:
            self._generate_random_event()

    def _generate_random_event(self):
        """Generate random world events"""
        import random
        
        event_types = [
            ("A mysterious phenomenon appears in the sky", "mystery", 0.6),
            ("Strange weather patterns emerge", "nature", 0.4),
            ("An ancient artifact is discovered", "discovery", 0.7),
            ("Tensions rise between factions", "conflict", 0.5),
            ("A prophet speaks of coming changes", "prophecy", 0.8)
        ]
        
        description, motif, emotional_weight = random.choice(event_types)
        
        self.event_manager.log_event(
            epoch=self.epoch_manager.current_epoch,
            description=description,
            entities=random.sample([e.get("name") for e in self.entities], 
                                 min(2, len(self.entities))),
            motif=motif,
            emotional_weight=emotional_weight,
            world_impact="moderate"
        )

    def get_system_state(self) -> Dict[str, Any]:
        """Get comprehensive state of all systems"""
        return {
            "epoch": self.epoch_manager.get_epoch_summary(),
            "events": {
                "total_events": len(self.event_manager.events),
                "recent_events": self.event_manager.events[-5:],
                "narrative_summary": self.event_manager.get_narrative_summary()
            },
            "actions": self.actions_manager.get_action_summary(),
            "entities": {
                "total_entities": len(self.entities),
                "present_world_entities": len(self.present_world.entities) if self.present_world else 0,
                "past_world_entities": len(self.past_world.entities) if self.past_world else 0
            },
            "worlds": {
                "present": self.present_world.get_narrative_summary() if self.present_world else "Not initialized",
                "past": self.past_world.get_narrative_summary() if self.past_world else "Not initialized"
            },
            "simulation_running": self.simulation_running
        }

    def start_simulation(self):
        """Start the world simulation"""
        self.simulation_running = True
        print("🌍 World simulation started!")

    def stop_simulation(self):
        """Stop the world simulation"""
        self.simulation_running = False
        print("⏸️ World simulation paused!")

    def clear(self):
        """Clear all managers"""
        self.epoch_manager.reset()
        self.event_manager.clear()
        self.actions_manager.clear()


# Global system manager instance for easy access
world_system_manager = WorldSystemManager()

# Association network integration functions
def get_association_manager():
    """Get the global association manager"""
    return world_system_manager.association_manager

def find_entity_connections(entity_name: str, connection_type: str = None) -> List[str]:
    """Find connections for an entity through the association network"""
    return world_system_manager.association_manager.find_connected_archetypes(entity_name, connection_type)

def get_entity_influence_map(entity_name: str, depth: int = 2) -> Dict[str, float]:
    """Get influence map for an entity"""
    return world_system_manager.get_entity_influence_network(entity_name, depth)

def suggest_entity_narrative_hooks(entity_name: str) -> Dict[str, List[str]]:
    """Suggest narrative hooks based on entity associations"""
    return world_system_manager.suggest_narrative_connections(entity_name)

def calculate_entity_relationship(entity1: str, entity2: str) -> float:
    """Calculate relationship strength between entities"""
    return world_system_manager.calculate_relationship_strength(entity1, entity2)

def declare_cyber_war(factions, cause="the Neon Throne", epoch=1):
    """Enhanced cyber war declaration with full system integration"""
    folder = r"c:\Users\storage\root\bookoflife\archetypes\cyberdynasties"
    try:
        traits_lookup = load_dynasty_boss_traits(folder)
        war = world_system_manager.war_engine.declare_war(factions, cause, epoch)
        
        # Log war declaration as major event
        world_system_manager.event_manager.log_event(
            epoch=world_system_manager.epoch_manager.current_epoch,
            description=f"War declared between {', '.join(factions)} over {cause}",
            entities=factions,
            motif="war",
            world_impact="major",
            emotional_weight=0.9
        )
        
        return war, traits_lookup
    except Exception as e:
        print(f"Error declaring cyber war: {e}")
        return None, {}

def advance_war_tick(traits_lookup=None, epoch=None):
    """Enhanced war advancement with system integration"""
    if not epoch:
        epoch = world_system_manager.epoch_manager.current_epoch
    
    try:
        world_system_manager.war_engine.tick(traits_lookup or {}, epoch)
    except Exception as e:
        print(f"Error advancing war: {e}")

# Convenience functions for external access
def get_epoch_manager():
    return world_system_manager.epoch_manager

def get_event_manager():
    return world_system_manager.event_manager

def get_actions_manager():
    return world_system_manager.actions_manager

def get_world_system():
    return world_system_manager