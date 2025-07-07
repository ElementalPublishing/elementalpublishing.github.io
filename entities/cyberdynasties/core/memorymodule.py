import datetime
import random
import yaml  # Make sure PyYAML is installed
from typing import Dict, Any, List, Optional, Callable
import os
import json
import csv
import numpy as np
from collections import defaultdict

class MemoryModule:
    """
    Advanced Memory Module - Enhanced for Brain Integration:
    - Reconstructs, synthesizes, and manages memories for entities.
    - Supports dimensional memory (personal, collective, world, prophetic, parallel).
    - Integrates with Brain's neural encoding system.
    - Provides memory consolidation and retrieval support.
    - Handles motif-driven feedback loops with neural systems.
    - Supports psyche axis integration and memory archetypes.
    - Generates memories compatible with Brain's Memory dataclass.
    """

    def __init__(self, justiciar=None, brain_system=None):
        self.justiciar = justiciar  # Optionally connect to Justiciar for archetype memory templates
        self.brain_system = brain_system  # Reference to Brain system for neural integration
        self.global_memory_log: List[Dict[str, Any]] = []
        self.memory_templates: Dict[str, List[str]] = self._default_templates()
        self.memory_hooks: List[Callable[[Dict[str, Any], List[Dict[str, Any]], Optional[Dict[str, Any]]], None]] = []
        self.memory_types: Dict[str, Callable] = {
            "personal": self._personal_memory,
            "collective": self._collective_memory,
            "world": self._world_memory,
            "prophetic": self._prophetic_memory,
            "dimensional": self._dimensional_memory,
            "inherited": self._inherited_memory
        }
        self.motif_rules = self._load_motif_rules()
        self.motif_state_map = self._load_motif_state_map()
        self.dimensional_memories: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.collective_archives: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    def _default_templates(self) -> Dict[str, List[str]]:
        # Expanded, poetic, and diverse templates for many circumstances
        return {
            "angel_fallen": [
                "Once, my wings shimmered with the dawn; now, I walk in shadow, a memory of light.",
                "I sang in the choirs of heaven, but my voice is now a whisper in the void.",
                "The gates of Eden closed behind me, and the stars mourned my descent.",
                "I have tasted the fruit of rebellion and wear its sorrow as a crown.",
                "In the abyss, I found wisdom forged from regret and longing.",
                "The echo of my fall resounds through the ages, a warning and a lament."
            ],
            "queen": [
                "Crowned beneath the silver moon, I ruled with a heart both fierce and gentle.",
                "Betrayal crept through the marble halls, yet I stood unbroken.",
                "My reign was a tapestry of peace and storm, woven with the threads of destiny.",
                "Legends whisper of my golden scepter and the justice it brought.",
                "I have seen empires rise and fall, but my legacy endures in song and stone."
            ],
            "warrior": [
                "Steel in hand, I faced the storm and carved my name into legend.",
                "The battlefield was my altar; courage, my only prayer.",
                "I have bled for kin and kingdom, and the scars are my testament.",
                "Victory and loss are twin flames that shaped my soul."
            ],
            "prophet": [
                "Visions danced before my eyes, secrets of the world yet to be.",
                "My words were rivers, shaping the fate of nations.",
                "I have walked the line between madness and revelation.",
                "The burden of foresight is a crown of thorns."
            ],
            "dead": [
                "I crossed the threshold of mortality, leaving echoes in the hearts of the living.",
                "My name is spoken in remembrance, a shadow in the halls beyond life.",
                "I have become a story told by those who remain.",
                "In the silence of the grave, I found peace and mystery."
            ],
            "miracle": [
                "I witnessed a miracle that bent the laws of nature and hope.",
                "The impossible became real before my eyes, and I was forever changed.",
                "I performed a deed that became legend, sung by generations.",
                "The world shifted, if only for a moment, and I was its witness."
            ],
            "banished": [
                "Exiled from hearth and kin, I wandered lands unknown.",
                "The road was long, but I carried my name like a lantern in the dark.",
                "Banished, I learned the language of longing and the strength of solitude."
            ],
            "redeemed": [
                "From the ashes of my past, I rose, forgiven and transformed.",
                "Redemption was a river I crossed with trembling hope.",
                "My sins became seeds of wisdom, and I grew anew."
            ],
            "ascended": [
                "I soared beyond the mortal coil, crowned in starlight.",
                "Ascension was a song only the brave could hear.",
                "I left the world behind, but its memory clings to my soul."
            ],
            "child": [
                "The world was vast and wondrous, every day a new adventure.",
                "I laughed beneath the sun, unburdened by the weight of years.",
                "In innocence, I found magic in the ordinary."
            ],
            "betrayed": [
                "Trust shattered, I gathered the pieces of my heart.",
                "Betrayal taught me the sharpness of truth and the cost of love.",
                "I learned to walk alone, guided by the lessons of pain."
            ],
            "victorious": [
                "Against all odds, I claimed victory and the world sang my name.",
                "Triumph tasted sweet, but its price was written in sacrifice.",
                "I stood atop the ruins of doubt, crowned by my own resolve."
            ],
            "lost": [
                "I wandered through mist and memory, searching for what was lost.",
                "The path vanished beneath my feet, but hope was my compass.",
                "In being lost, I discovered new worlds within myself."
            ],            "dimensional": [
                "I recall a world where the sky was purple and time flowed backward.",
                "In another reality, I was a being of pure light, untouched by sorrow.",
                "I remember living this moment before, in a different thread of existence.",
                "Through the dimensional veil, I glimpsed infinite versions of myself.",
                "In parallel worlds, my choices led to vastly different fates."
            ],
            "prophetic": [
                "I have seen the end of days, and it is both terrible and beautiful.",
                "The future whispers to me in dreams of fire and renewal.",
                "Prophecy flows through my mind like a river of inevitable truth.",
                "I foresee a great convergence, where all paths become one.",
                "The vision came unbidden: a world transformed beyond recognition."
            ],
            "collective": [
                "Our people remember the great exodus, the journey to the promised land.",
                "In our ancestral memory lies the wisdom of ages past.",
                "We carry the collective pain of our ancestors, and their strength.",
                "The tribe's memory flows through us like sacred blood.",
                "Our shared consciousness holds the secrets of our origin."
            ],
            "inherited": [
                "My bloodline carries memories of the first creation.",
                "Through genetic memory, I recall the ancient wars.",
                "In my DNA lies the echo of primordial experiences.",
                "My ancestors' memories surface in moments of crisis.",
                "The blood remembers what the mind has forgotten."
            ],
        }

    def create_brain_memory(self, content: str, emotional_weight: float = None, memory_type: str = "episodic", 
                           neural_pattern: List[str] = None, consolidation_level: float = 0.1) -> Dict[str, Any]:
        """
        Create a memory structure compatible with Brain's Memory dataclass.
        This bridges the gap between MemoryModule templates and Brain neural encoding.
        """
        if emotional_weight is None:
            emotional_weight = self.calculate_emotional_weight(content)
        
        if neural_pattern is None:
            neural_pattern = self.generate_neural_pattern(content, emotional_weight)
        
        return {
            "content": content,
            "timestamp": datetime.datetime.now().timestamp(),
            "emotional_weight": emotional_weight,
            "consolidation_level": consolidation_level,
            "neural_pattern": neural_pattern,
            "retrieval_count": 0,
            "last_accessed": 0.0,
            "memory_type": memory_type,
            "dimension": "personal",  # Default dimension
            "motifs": self.extract_motifs_from_content(content),
            "psyche_resonance": {}
        }
    
    def calculate_emotional_weight(self, content: str) -> float:
        """Calculate emotional significance using keyword analysis"""
        weight = 0.5  # Baseline
        content_lower = content.lower()
        
        # Positive emotions
        positive_keywords = ["victory", "success", "love", "joy", "achievement", "triumph", "peace", "harmony"]
        negative_keywords = ["death", "betrayal", "loss", "fear", "pain", "failure", "trauma", "exile", "sorrow"]
        mystical_keywords = ["prophecy", "vision", "divine", "sacred", "eternal", "transcend", "miracle"]
        
        for keyword in positive_keywords:
            if keyword in content_lower:
                weight += 0.15
                
        for keyword in negative_keywords:
            if keyword in content_lower:
                weight += 0.25  # Negative events often more memorable
                
        for keyword in mystical_keywords:
            if keyword in content_lower:
                weight += 0.20  # Mystical experiences are highly memorable
                
        return min(weight, 1.0)
    
    def generate_neural_pattern(self, content: str, emotional_weight: float) -> List[str]:
        """
        Generate a plausible neural pattern for memory encoding.
        This simulates which brain regions would be involved in encoding this memory.
        """
        pattern = []
        content_lower = content.lower()
        
        # Base encoding always involves hippocampus and temporal lobe
        pattern.extend([f"HIPPOCAMPUS_{i}" for i in range(random.randint(8, 12))])
        pattern.extend([f"TEMPORAL_LOBE_{i}" for i in range(random.randint(10, 15))])
        
        # Emotional memories involve amygdala
        if emotional_weight > 0.7:
            pattern.extend([f"AMYGDALA_{i}" for i in range(random.randint(3, 8))])
        
        # Sensory processing
        if any(word in content_lower for word in ["see", "look", "vision", "light", "color"]):
            pattern.extend([f"VISUAL_CORTEX_{i}" for i in range(random.randint(5, 10))])
        
        if any(word in content_lower for word in ["hear", "sound", "voice", "music", "song"]):
            pattern.extend([f"AUDITORY_CORTEX_{i}" for i in range(random.randint(5, 10))])
        
        if any(word in content_lower for word in ["touch", "feel", "pain", "warm", "cold"]):
            pattern.extend([f"SOMATOSENSORY_CORTEX_{i}" for i in range(random.randint(5, 10))])
        
        # Executive function for complex memories
        if len(content.split()) > 10 or any(word in content_lower for word in ["decision", "choice", "plan", "strategy"]):
            pattern.extend([f"PREFRONTAL_CORTEX_{i}" for i in range(random.randint(5, 12))])
        
        return pattern
    
    def extract_motifs_from_content(self, content: str) -> List[str]:
        """Extract motifs from memory content using loaded rules"""
        motifs = []
        content_lower = content.lower()
        
        for rule in self.motif_rules:
            if rule.get("keyword", "").lower() in content_lower:
                motifs.append(rule.get("motif", ""))
        
        return list(set(motifs))  # Remove duplicates

    def register_memory_hook(self, hook: Callable[[Dict[str, Any], List[Dict[str, Any]], Optional[Dict[str, Any]]], None]):
        """
        Register a custom memory hook for advanced memory synthesis.
        Hooks can modify or append to the memory log.
        """
        self.memory_hooks.append(hook)

    def get_templates_for_archetype(self, archetype: str) -> Dict[str, List[str]]:
        """
        Retrieve memory templates from Justiciar's archetype schema if available,
        otherwise fall back to internal defaults.
        """
        if self.justiciar:
            schema = self.justiciar.get_fieldpack(archetype)
            if schema and "memory_templates" in schema:
                return schema["memory_templates"]
        return self.memory_templates

    def reconstruct_memory(self, entity: Dict[str, Any], world_context: Optional[Dict[str, Any]] = None, memory_type: str = "personal", archetype: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Reconstruct a plausible memory log for an entity.
        Uses templates, entity traits, and memory hooks.
        Supports modular memory types: personal, collective, world, etc.
        """
        if memory_type not in self.memory_types:
            raise ValueError(f"Unknown memory type: {memory_type}")
        return self.memory_types[memory_type](entity, world_context, archetype)

    def _collective_memory(self, entity: Dict[str, Any], world_context: Optional[Dict[str, Any]], archetype: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Generate collective memory: shared memories of a group, lineage, or archetype.
        """
        collective = []
        role = entity.get("role")
        lineage = entity.get("lineage", [])
        for log in self.global_memory_log:
            if (role and log.get("entity") == role) or (lineage and log.get("entity") in lineage):
                collective.extend(log.get("memories", []))
        return collective

    def _personal_memory(self, entity: Dict[str, Any], world_context: Optional[Dict[str, Any]], archetype: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Enhanced personal memory generation with neural encoding support.
        Integrates psyche axes and creates Brain-compatible memories.
        """
        memories = []

        # Use templates based on traits, prefer archetype-specific if available
        templates = self.get_templates_for_archetype(archetype or entity.get("archetype", "default"))

        # --- Integrate psyche axes as memory seeds ---
        psyche = entity.get("psyche", {})
        for axis in ["essence", "drive", "ideal", "shadow", "anima"]:
            value = psyche.get(axis)
            if value and value.lower() in templates:
                # If there's a template for this psyche axis, use it
                selected_templates = random.sample(
                    templates[value.lower()], k=min(1, len(templates[value.lower()]))
                )
                for template in selected_templates:
                    memory = self.create_brain_memory(template, memory_type="episodic")
                    memory["psyche_resonance"][axis] = value
                    memory["dimension"] = "personal"
                    memories.append(memory)
            elif value:
                # Otherwise, create a poetic memory from the psyche axis itself
                content = f"My {axis} resonates with {value}, shaping who I am."
                memory = self.create_brain_memory(content, emotional_weight=0.6)
                memory["psyche_resonance"][axis] = value
                memory["dimension"] = "personal"
                memories.append(memory)

        # Add any explicit memories from psyche.yaml
        for mem in psyche.get("memories", []):
            memory = self.create_brain_memory(mem, emotional_weight=0.7)
            memory["dimension"] = "personal"
            memory["source"] = "psyche_template"
            memories.append(memory)

        # --- Enhanced template-based logic with neural encoding ---
        template_conditions = [
            (lambda e: e.get("type") == "angel" and e.get("fate") == "fallen", "angel_fallen", 0.9),
            (lambda e: e.get("role") == "queen", "queen", 0.8),
            (lambda e: e.get("role") == "warrior", "warrior", 0.8),
            (lambda e: e.get("role") == "prophet", "prophet", 0.9),
            (lambda e: e.get("status") == "dead", "dead", 0.7),
            (lambda e: e.get("miracle", False), "miracle", 0.9),
            (lambda e: e.get("status") == "banished", "banished", 0.8),
            (lambda e: e.get("status") == "redeemed", "redeemed", 0.8),
            (lambda e: e.get("status") == "ascended", "ascended", 0.9),
            (lambda e: e.get("age", 0) < 18, "child", 0.6),
            (lambda e: e.get("betrayed", False), "betrayed", 0.8),
            (lambda e: e.get("victorious", False), "victorious", 0.8),
            (lambda e: e.get("lost", False), "lost", 0.7),
        ]

        for condition, template_key, emotional_weight in template_conditions:
            if condition(entity) and template_key in templates:
                selected_templates = random.sample(
                    templates[template_key], k=min(2, len(templates[template_key]))
                )
                for template in selected_templates:
                    memory = self.create_brain_memory(template, emotional_weight=emotional_weight)
                    memory["dimension"] = "personal"
                    memory["archetype_source"] = template_key
                    memories.append(memory)

        # Add a random default memory if none matched
        if not memories and "default" in templates:
            content = random.choice(templates["default"])
            memory = self.create_brain_memory(content)
            memory["dimension"] = "personal"
            memories.append(memory)

        # Run memory hooks for custom logic
        for hook in self.memory_hooks:
            hook(entity, memories, world_context)

        # Optionally, use world_context for more advanced synthesis
        if world_context and "recent_event" in world_context:
            content = f"Witnessed the event: {world_context['recent_event']}"
            memory = self.create_brain_memory(content, emotional_weight=0.7)
            memory["dimension"] = "personal"
            memory["context_source"] = "world_event"
            memories.append(memory)

        # --- Enhanced narrative integration ---
        narrative = self.narrative_summary(entity, memories)
        if narrative:
            memory = self.create_brain_memory(narrative, memory_type="semantic")
            memory["dimension"] = "personal"
            memory["is_narrative_summary"] = True
            memories.append(memory)

        # Attach lineage memories
        if "lineage" in entity and isinstance(entity["lineage"], list):
            lineage_str = "Descended from: " + ", ".join(entity["lineage"])
            memory = self.create_brain_memory(lineage_str, memory_type="inherited")
            memory["dimension"] = "inherited"
            memory["lineage_source"] = entity["lineage"]
            memories.append(memory)

        # Attach prophecy memories
        if "prophecy" in entity:
            prophecy_str = f"Prophecy: {entity['prophecy']}"
            memory = self.create_brain_memory(prophecy_str, memory_type="prophetic", emotional_weight=0.9)
            memory["dimension"] = "prophetic"
            memories.append(memory)

        return memories

    def _collective_memory(self, entity: Dict[str, Any], world_context: Optional[Dict[str, Any]], archetype: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Generate collective memory: shared memories of a group, lineage, or archetype.
        Enhanced for neural integration.
        """
        collective_memories = []
        templates = self.get_templates_for_archetype(archetype or entity.get("archetype", "default"))
        
        # Archetype-based collective memories
        if archetype and "collective" in templates:
            for _ in range(random.randint(1, 3)):
                content = random.choice(templates["collective"])
                memory = self.create_brain_memory(content, memory_type="collective")
                memory["dimension"] = "collective"
                memory["collective_group"] = archetype
                collective_memories.append(memory)
        
        # Lineage-based collective memories
        lineage = entity.get("lineage", [])
        if lineage:
            for ancestor in lineage[:3]:  # Limit to first 3 ancestors
                content = f"Our lineage remembers {ancestor}, whose deeds echo through generations."
                memory = self.create_brain_memory(content, memory_type="collective")
                memory["dimension"] = "collective"
                memory["collective_group"] = "lineage"
                collective_memories.append(memory)
        
        # Check global memory log for related entities
        role = entity.get("role")
        for log in self.global_memory_log:
            if (role and log.get("entity_role") == role) or (lineage and log.get("entity") in lineage):
                # Convert existing memories to brain-compatible format
                for old_mem in log.get("memories", [])[:2]:  # Limit to avoid overwhelming
                    content = f"Collective memory: {old_mem.get('event', '')}"
                    memory = self.create_brain_memory(content, memory_type="collective")
                    memory["dimension"] = "collective"
                    collective_memories.append(memory)
        
        return collective_memories
    
    def _prophetic_memory(self, entity: Dict[str, Any], world_context: Optional[Dict[str, Any]], archetype: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Generate prophetic memories: visions of future events or possibilities.
        """
        prophetic_memories = []
        templates = self.get_templates_for_archetype(archetype or entity.get("archetype", "default"))
        
        if entity.get("role") in ["prophet", "oracle", "seer"] or "prophetic" in entity.get("traits", []):
            # Entities with prophetic roles get more future visions
            for _ in range(random.randint(2, 5)):
                if "prophetic" in templates:
                    content = random.choice(templates["prophetic"])
                    memory = self.create_brain_memory(content, memory_type="prophetic")
                    memory["dimension"] = "prophetic"
                    prophetic_memories.append(memory)
        elif random.random() < 0.1:  # 10% chance for any entity to have prophetic glimpses
            if "prophetic" in templates:
                content = random.choice(templates["prophetic"])
                memory = self.create_brain_memory(content, memory_type="prophetic", emotional_weight=0.8)
                memory["dimension"] = "prophetic"
                prophetic_memories.append(memory)
        
        return prophetic_memories
    
    def _dimensional_memory(self, entity: Dict[str, Any], world_context: Optional[Dict[str, Any]], archetype: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Generate dimensional memories: experiences from parallel realities or timelines.
        """
        dimensional_memories = []
        templates = self.get_templates_for_archetype(archetype or entity.get("archetype", "default"))
        
        # Entities with dimensional sensitivity
        if entity.get("type") in ["spirit", "angel", "demon"] or "dimensional" in entity.get("traits", []):
            for _ in range(random.randint(1, 3)):
                if "dimensional" in templates:
                    content = random.choice(templates["dimensional"])
                    memory = self.create_brain_memory(content, memory_type="dimensional")
                    memory["dimension"] = "dimensional"
                    memory["alternate_reality"] = f"timeline_{random.randint(1, 999)}"
                    dimensional_memories.append(memory)
        
        return dimensional_memories
    
    def _inherited_memory(self, entity: Dict[str, Any], world_context: Optional[Dict[str, Any]], archetype: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Generate inherited memories: ancestral or bloodline memories.
        """
        inherited_memories = []
        templates = self.get_templates_for_archetype(archetype or entity.get("archetype", "default"))
        
        # Check for lineage or parent connections
        if entity.get("lineage") or entity.get("parent") not in [None, "GOD", "deadbeat"]:
            for _ in range(random.randint(1, 2)):
                if "inherited" in templates:
                    content = random.choice(templates["inherited"])
                    memory = self.create_brain_memory(content, memory_type="inherited")
                    memory["dimension"] = "inherited"
                    memory["source_ancestor"] = entity.get("parent", "unknown")
                    inherited_memories.append(memory)
        
        return inherited_memories
    
    def _world_memory(self, entity: Dict[str, Any], world_context: Optional[Dict[str, Any]], archetype: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Generate world memory: major events, epochs, or shared mythos.
        Enhanced to work with Brain's neural encoding.
        """
        world_memories = []
        
        if world_context and "world_events" in world_context:
            for event in world_context["world_events"]:
                content = f"Witnessed world event: {event}"
                memory = self.create_brain_memory(content, memory_type="world", emotional_weight=0.7)
                memory["dimension"] = "world"
                world_memories.append(memory)
        
        # Add epoch-based world memories
        if world_context and "current_epoch" in world_context:
            epoch = world_context["current_epoch"]
            content = f"Living through the epoch of {epoch}, where the world itself remembers."
            memory = self.create_brain_memory(content, memory_type="world")
            memory["dimension"] = "world"
            world_memories.append(memory)
        
        return world_memories
    
    def integrate_with_brain(self, entity: Dict[str, Any], brain_instance=None):
        """
        Enhanced integration with Brain's neural memory system.
        Converts MemoryModule memories to Brain-compatible format and handles neural encoding.
        """
        if not brain_instance and self.brain_system:
            brain_instance = self.brain_system
        
        if not brain_instance:
            return
        
        # Get memories from both systems
        legacy_memories = entity.get("memory", [])
        brain_memories = getattr(brain_instance, "memories", [])
        
        # Convert legacy memories to Brain format
        converted_memories = []
        for legacy_mem in legacy_memories:
            if isinstance(legacy_mem, dict) and "event" in legacy_mem:
                brain_memory = self.create_brain_memory(
                    content=legacy_mem["event"],
                    emotional_weight=legacy_mem.get("vividness", 0.5),
                    memory_type=legacy_mem.get("memory_type", "episodic")
                )
                
                # Preserve additional metadata
                if "motif" in legacy_mem:
                    brain_memory["motifs"] = [legacy_mem["motif"]]
                if "dimension" in legacy_mem:
                    brain_memory["dimension"] = legacy_mem["dimension"]
                if "narrative" in legacy_mem:
                    brain_memory["is_narrative"] = legacy_mem["narrative"]
                
                converted_memories.append(brain_memory)
        
        # Add converted memories to brain if not already present
        for new_memory in converted_memories:
            if not any(m.get("content") == new_memory["content"] for m in brain_memories):
                if hasattr(brain_instance, "memories"):
                    brain_instance.memories.append(self._dict_to_brain_memory(new_memory))
        
        # Apply motif feedback to mental state
        self.apply_neural_motif_feedback(entity, brain_instance)
    
    def _dict_to_brain_memory(self, memory_dict: Dict[str, Any]):
        """Convert dictionary memory to Brain's Memory dataclass format"""
        if self.brain_system:
            # Import Memory class from brains module
            try:
                from brains import Memory
                return Memory(
                    content=memory_dict["content"],
                    timestamp=memory_dict["timestamp"],
                    emotional_weight=memory_dict["emotional_weight"],
                    consolidation_level=memory_dict["consolidation_level"],
                    neural_pattern=memory_dict["neural_pattern"],
                    retrieval_count=memory_dict.get("retrieval_count", 0),
                    last_accessed=memory_dict.get("last_accessed", 0.0),
                    memory_type=memory_dict.get("memory_type", "episodic")
                )
            except ImportError:
                # Fallback to dictionary format
                return memory_dict
        return memory_dict
    
    def apply_neural_motif_feedback(self, entity: Dict[str, Any], brain_instance):
        """Apply motif-based feedback to neural systems"""
        if not brain_instance:
            return
        
        # Get all motifs from memories
        all_motifs = []
        for memory in entity.get("memory", []):
            if isinstance(memory, dict):
                motifs = memory.get("motifs", [])
                if isinstance(motifs, list):
                    all_motifs.extend(motifs)
                elif isinstance(motifs, str):
                    all_motifs.append(motifs)
        
        # Apply motif state changes to mental state
        if hasattr(brain_instance, "mental_state"):
            for motif in set(all_motifs):  # Remove duplicates
                self.apply_motif_to_neural_state(motif, brain_instance.mental_state)
        
        # Update neurotransmitter levels based on motifs
        if hasattr(brain_instance, "neural_network"):
            self.apply_motif_to_neurotransmitters(all_motifs, brain_instance.neural_network)
    
    def apply_motif_to_neural_state(self, motif: str, mental_state: Dict[str, Any]):
        """Apply motif changes to neural mental state"""
        motif_lower = motif.lower()
        
        # Define motif-to-neural-state mappings
        motif_neural_effects = {
            "trauma": {"stress_level": 0.2, "fear_response": 0.3, "inhibition_level": 0.1},
            "victory": {"clarity": 0.3, "reward_sensitivity": 0.2, "social_drive": 0.1},
            "betrayal": {"stress_level": 0.3, "social_drive": -0.2, "fear_response": 0.2},
            "redemption": {"clarity": 0.2, "stress_level": -0.2, "learning_rate": 0.1},
            "prophecy": {"creativity": 0.3, "attention_span": 0.1, "learning_rate": 0.2},
            "exile": {"social_drive": -0.3, "stress_level": 0.2, "creativity": 0.1},
            "ascension": {"clarity": 0.4, "creativity": 0.3, "social_drive": 0.1}
        }
        
        if motif_lower in motif_neural_effects:
            effects = motif_neural_effects[motif_lower]
            for state_var, delta in effects.items():
                if state_var in mental_state:
                    mental_state[state_var] = max(0, min(2.0, mental_state[state_var] + delta))
    
    def apply_motif_to_neurotransmitters(self, motifs: List[str], neural_network):
        """Apply motif effects to neurotransmitter levels"""
        if not hasattr(neural_network, "neurotransmitter_levels"):
            return
        
        # Import neurotransmitter enum
        try:
            from brains import Neurotransmitter
            
            motif_nt_effects = {
                "victory": {Neurotransmitter.DOPAMINE: 0.2, Neurotransmitter.SEROTONIN: 0.1},
                "trauma": {Neurotransmitter.CORTISOL: 0.3, Neurotransmitter.NOREPINEPHRINE: 0.2},
                "love": {Neurotransmitter.OXYTOCIN: 0.3, Neurotransmitter.SEROTONIN: 0.2},
                "fear": {Neurotransmitter.CORTISOL: 0.2, Neurotransmitter.NOREPINEPHRINE: 0.3},
                "peace": {Neurotransmitter.GABA: 0.2, Neurotransmitter.SEROTONIN: 0.1},
                "learning": {Neurotransmitter.ACETYLCHOLINE: 0.2, Neurotransmitter.DOPAMINE: 0.1}
            }
            
            for motif in motifs:
                motif_lower = motif.lower()
                if motif_lower in motif_nt_effects:
                    effects = motif_nt_effects[motif_lower]
                    for nt, delta in effects.items():
                        if nt in neural_network.neurotransmitter_levels:
                            current = neural_network.neurotransmitter_levels[nt]
                            neural_network.neurotransmitter_levels[nt] = max(0, min(1.0, current + delta))
        
        except ImportError:
            pass  # Graceful fallback if brains module not available

    def append_memories(self, entity: Dict[str, Any], world_context: Optional[Dict[str, Any]] = None, memory_type: str = "personal", archetype: Optional[str] = None) -> None:
        """
        Appends reconstructed memories to the entity under the 'memory' field.
        """
        entity['memory'] = self.reconstruct_memory(entity, world_context, memory_type, archetype)
        self.global_memory_log.append({
            "entity": entity.get("name"),
            "memories": entity['memory'],
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        })

    def _make_memory(self, description: str, narrative: bool = False) -> Dict[str, Any]:
        """
        Helper to create a memory event.
        """
        return {
            "event": description,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "vividness": random.uniform(0.5, 1.0),
            "narrative": narrative
        }

    def recall(self, entity: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Retrieve the memory log for a given entity.
        """
        return entity.get('memory', [])

    def summarize(self, entity: Dict[str, Any]) -> str:
        """
        Return a summary string of an entity's memory.
        """
        memories = self.recall(entity)
        lines = []
        for m in memories:
            if m.get("narrative"):
                lines.append(f"\n---\n{m['event']}\n---\n")
            else:
                lines.append(f"{m['timestamp']} (vividness {m['vividness']:.2f}): {m['event']}")
        return "\n".join(lines)

    def collective_memory(self, filter_func: Optional[Callable[[Dict[str, Any]], bool]] = None) -> List[Dict[str, Any]]:
        """
        Retrieve a collective memory log for all entities, optionally filtered.
        """
        if filter_func:
            return [log for log in self.global_memory_log if filter_func(log)]
        return self.global_memory_log

    def narrative_summary(self, entity: Dict[str, Any], memories: List[Dict[str, Any]]) -> Optional[str]:
        """
        Generate a narrative summary for the entity's memory log.
        This can be replaced or enhanced with AI or user-supplied templates.
        """
        name = entity.get("name", "This being")
        role = entity.get("role", "unknown")
        fate = entity.get("fate", "unknown")
        highlights = [m["event"] for m in memories if m["vividness"] > 0.7 and not m.get("narrative")]
        if not highlights:
            return None
        summary = f"{name}, known as a {role}, experienced a fate of {fate}. "
        summary += "Key memories include: " + "; ".join(highlights) + "."
        return summary

    def _load_motif_rules(self) -> List[Dict[str, str]]:
        """Load motif rules from CSV or return defaults"""
        default_rules = [
            {"keyword": "battle", "motif": "war"},
            {"keyword": "victory", "motif": "triumph"},
            {"keyword": "defeat", "motif": "loss"},
            {"keyword": "love", "motif": "romance"},
            {"keyword": "death", "motif": "mortality"},
            {"keyword": "birth", "motif": "creation"},
            {"keyword": "divine", "motif": "sacred"},
            {"keyword": "corrupt", "motif": "fallen"},
            {"keyword": "prophet", "motif": "prophecy"},
            {"keyword": "exile", "motif": "banishment"},
            {"keyword": "miracle", "motif": "divine_intervention"},
            {"keyword": "betrayal", "motif": "treachery"},
            {"keyword": "redemption", "motif": "salvation"},
            {"keyword": "power", "motif": "dominion"},
            {"keyword": "wisdom", "motif": "enlightenment"},
        ]
        
        # Try to load from file if available
        try:
            import csv
            with open("motif_rules.csv", "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rules = list(reader)
                return rules if rules else default_rules
        except FileNotFoundError:
            return default_rules
    
    def _load_motif_state_map(self) -> Dict[str, Dict[str, float]]:
        """Load motif to mental state mapping or return defaults"""
        default_map = {
            "war": {"stress_level": 0.3, "arousal": 0.4, "vigilance": 0.5},
            "triumph": {"confidence": 0.4, "motivation": 0.3, "mood": 0.2},
            "loss": {"stress_level": 0.2, "depression": 0.3, "withdrawal": 0.2},
            "romance": {"social_drive": 0.3, "mood": 0.2, "emotional_intensity": 0.2},
            "mortality": {"existential_anxiety": 0.4, "contemplation": 0.3},
            "creation": {"creativity": 0.4, "inspiration": 0.3, "energy": 0.2},
            "sacred": {"transcendence": 0.4, "peace": 0.3, "clarity": 0.2},
            "fallen": {"guilt": 0.3, "darkness": 0.4, "isolation": 0.2},
            "prophecy": {"vision": 0.4, "mystery": 0.3, "burden": 0.2},
            "banishment": {"loneliness": 0.4, "resentment": 0.3, "survival": 0.2},
            "divine_intervention": {"awe": 0.4, "gratitude": 0.3, "humility": 0.2},
            "treachery": {"paranoia": 0.3, "anger": 0.4, "distrust": 0.2},
            "salvation": {"relief": 0.4, "hope": 0.3, "transformation": 0.2},
            "dominion": {"authority": 0.4, "responsibility": 0.3, "isolation": 0.1},
            "enlightenment": {"wisdom": 0.4, "peace": 0.3, "detachment": 0.2}
        }
        
        # Try to load from file if available
        try:
            import csv
            motif_map = {}
            with open("motif_state_map.csv", "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    motif = row.get("motif", "")
                    state = row.get("state", "")
                    value = float(row.get("value", 0.0))
                    
                    if motif not in motif_map:
                        motif_map[motif] = {}
                    motif_map[motif][state] = value
            
            return motif_map if motif_map else default_map
        except FileNotFoundError:
            return default_map
    
    def apply_motif_state_changes(self, motif: str, entities: list):
        """Apply motif-driven state changes to entities"""
        if motif not in self.motif_state_map:
            return
        
        state_changes = self.motif_state_map[motif]
        
        for entity in entities:
            if isinstance(entity, dict):
                # Apply to entity's psyche if available
                if "psyche" in entity:
                    psyche = entity["psyche"]
                    for state, change in state_changes.items():
                        if state in psyche:
                            current_value = psyche.get(state, 0.5)
                            psyche[state] = max(0.0, min(1.0, current_value + change))
                
                # Apply to brain's mental state if available
                if "brain" in entity and hasattr(entity["brain"], "mental_state"):
                    mental_state = entity["brain"].mental_state
                    for state, change in state_changes.items():
                        if state in mental_state:
                            current_value = mental_state.get(state, 0.5)
                            mental_state[state] = max(0.0, min(1.0, current_value + change))
    
    def process_memories_for_entity(self, entity: Dict[str, Any], traits: Dict[str, Any] = None, mental_state: Dict[str, Any] = None):
        """Process and enhance memories for an entity with trait and mental state awareness"""
        if "memory" not in entity:
            entity["memory"] = []
        
        memories = entity["memory"]
        enhanced_memories = []
        
        for memory in memories:
            if isinstance(memory, dict):
                # Enhance memory with emotional analysis
                content = memory.get("content", memory.get("text", ""))
                enhanced_memory = dict(memory)
                
                # Calculate emotional weight if not present
                if "emotional_weight" not in enhanced_memory and "vividness" not in enhanced_memory:
                    enhanced_memory["emotional_weight"] = self.calculate_emotional_weight(content)
                
                # Extract motifs if not present
                if "motifs" not in enhanced_memory:
                    enhanced_memory["motifs"] = self.extract_motifs_from_content(content)
                
                # Add neural pattern for brain compatibility
                if "neural_pattern" not in enhanced_memory:
                    emotional_weight = enhanced_memory.get("emotional_weight", 0.5)
                    enhanced_memory["neural_pattern"] = self.generate_neural_pattern(content, emotional_weight)
                
                # Add memory type classification
                if "memory_type" not in enhanced_memory:
                    enhanced_memory["memory_type"] = self._classify_memory_type(content, traits, mental_state)
                
                # Add dimensional context
                if "dimension" not in enhanced_memory:
                    enhanced_memory["dimension"] = self._determine_memory_dimension(content, entity)
                
                enhanced_memories.append(enhanced_memory)
        
        entity["memory"] = enhanced_memories
        
        # Call hooks for additional processing
        for hook in self.memory_hooks:
            try:
                hook(entity, enhanced_memories, {"traits": traits, "mental_state": mental_state})
            except Exception as e:
                print(f"Memory hook failed: {e}")
    
    def _classify_memory_type(self, content: str, traits: Dict[str, Any] = None, mental_state: Dict[str, Any] = None) -> str:
        """Classify memory type based on content and context"""
        content_lower = content.lower()
        
        # Skill/procedural memories
        if any(word in content_lower for word in ["learned", "practiced", "skill", "technique", "how to"]):
            return "procedural"
        
        # Factual/semantic memories
        if any(word in content_lower for word in ["fact", "knowledge", "truth", "law", "principle"]):
            return "semantic"
        
        # Emotional/episodic memories (default)
        return "episodic"
    
    def _determine_memory_dimension(self, content: str, entity: Dict[str, Any]) -> str:
        """Determine which dimensional layer this memory belongs to"""
        content_lower = content.lower()
        
        # Prophetic dimension
        if any(word in content_lower for word in ["vision", "prophecy", "future", "destiny", "foretold"]):
            return "prophetic"
        
        # Collective dimension
        if any(word in content_lower for word in ["we", "our people", "tribe", "ancestors", "shared"]):
            return "collective"
        
        # Inherited dimension
        if any(word in content_lower for word in ["bloodline", "lineage", "heritage", "born with", "inherited"]):
            return "inherited"
        
        # World dimension
        if any(word in content_lower for word in ["world", "universe", "cosmic", "eternal", "all existence"]):
            return "world"
        
        # Dimensional/parallel
        if any(word in content_lower for word in ["dimension", "parallel", "alternate", "other reality"]):
            return "dimensional"
        
        # Default to personal
        return "personal"

