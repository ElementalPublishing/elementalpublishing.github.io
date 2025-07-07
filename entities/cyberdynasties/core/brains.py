import random
import json
import yaml
import datetime
import numpy as np
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum

class BrainRegion(Enum):
    """Brain regions with their primary functions"""
    PREFRONTAL_CORTEX = "executive_function"
    HIPPOCAMPUS = "memory_formation"
    AMYGDALA = "emotional_processing"
    TEMPORAL_LOBE = "memory_storage"
    BRAINSTEM = "basic_functions"
    CEREBELLUM = "motor_coordination"
    VISUAL_CORTEX = "visual_processing"
    AUDITORY_CORTEX = "auditory_processing"
    SOMATOSENSORY_CORTEX = "touch_processing"

class Neurotransmitter(Enum):
    """Neurotransmitters and their effects"""
    DOPAMINE = "reward_motivation"
    SEROTONIN = "mood_regulation"
    NOREPINEPHRINE = "attention_arousal"
    ACETYLCHOLINE = "learning_attention"
    GABA = "inhibition_calm"
    GLUTAMATE = "excitation_learning"
    OXYTOCIN = "social_bonding"
    CORTISOL = "stress_response"

@dataclass
class Neuron:
    """Individual neuron with connections and activation"""
    id: str
    region: BrainRegion
    activation_level: float = 0.0
    threshold: float = 0.5
    connections: List[str] = None
    weights: List[float] = None

    def __post_init__(self):
        if self.connections is None:
            self.connections = []
        if self.weights is None:
            self.weights = []

@dataclass
class Memory:
    """Enhanced memory structure with neural encoding"""
    content: str
    timestamp: float
    emotional_weight: float
    consolidation_level: float
    neural_pattern: List[str]  # Which neurons encode this memory
    retrieval_count: int = 0
    last_accessed: float = 0.0
    memory_type: str = "episodic"  # episodic, semantic, procedural

class NeuralNetwork:
    """Simple neural network for brain simulation"""
    def __init__(self):
        self.neurons: Dict[str, Neuron] = {}
        self.neurotransmitter_levels: Dict[Neurotransmitter, float] = {
            nt: 0.5 for nt in Neurotransmitter
        }
        self.region_activation: Dict[BrainRegion, float] = {
            region: 0.0 for region in BrainRegion
        }

    def add_neuron(self, neuron_id: str, region: BrainRegion):
        self.neurons[neuron_id] = Neuron(neuron_id, region)

    def connect_neurons(self, from_id: str, to_id: str, weight: float = 0.5):
        if from_id in self.neurons:
            self.neurons[from_id].connections.append(to_id)
            self.neurons[from_id].weights.append(weight)

    def propagate_activation(self, input_neurons: List[str], activation: float):
        for neuron_id in input_neurons:
            if neuron_id in self.neurons:
                neuron = self.neurons[neuron_id]
                neuron.activation_level = activation
                for i, connected_id in enumerate(neuron.connections):
                    if connected_id in self.neurons:
                        weight = neuron.weights[i] if i < len(neuron.weights) else 0.5
                        self.neurons[connected_id].activation_level += activation * weight
        for region in BrainRegion:
            region_neurons = [n for n in self.neurons.values() if n.region == region]
            if region_neurons:
                self.region_activation[region] = sum(n.activation_level for n in region_neurons) / len(region_neurons)

    def decay_activation(self, decay_rate: float = 0.1):
        for neuron in self.neurons.values():
            neuron.activation_level *= (1 - decay_rate)

class Brain:
    """
    Advanced Brain module that simulates realistic neural processes:
    - Neural networks with synaptic connections
    - Neurotransmitter systems affecting cognition
    - Brain region specialization and interaction
    - Realistic memory encoding, consolidation, and retrieval
    - Emotional processing through limbic system
    - Circadian rhythms and sleep cycles
    - Neuroplasticity and learning
    """

    def __init__(self, entity, memory_module, traits_config_path, book_of_math=None):
        self.entity = entity
        self.memory_module = memory_module
        self.traits = self.load_traits(traits_config_path, entity)
        self.neural_network = NeuralNetwork()
        self.memories: List[Memory] = []
        self.mental_state = self.init_mental_state()
        self.book_of_math = book_of_math or {}
        self.circadian_cycle = 0.0  # 0-24 hour cycle
        self.sleep_pressure = 0.0
        self.attention_focus = []
        self.working_memory_capacity = 7  # Miller's magic number
        self.working_memory = []

        # Initialize neural architecture
        self.initialize_neural_architecture()

    def initialize_neural_architecture(self):
        """Create realistic neural architecture with specialized regions"""
        # Create neurons for each brain region
        regions_neurons = {
            BrainRegion.PREFRONTAL_CORTEX: 100,
            BrainRegion.HIPPOCAMPUS: 50,
            BrainRegion.AMYGDALA: 30,
            BrainRegion.TEMPORAL_LOBE: 80,
            BrainRegion.BRAINSTEM: 20,
            BrainRegion.CEREBELLUM: 60,
            BrainRegion.VISUAL_CORTEX: 70,
            BrainRegion.AUDITORY_CORTEX: 40,
            BrainRegion.SOMATOSENSORY_CORTEX: 50
        }

        for region, count in regions_neurons.items():
            for i in range(count):
                neuron_id = f"{region.name}_{i}"
                self.neural_network.add_neuron(neuron_id, region)

        # Create realistic neural connections
        self.create_neural_pathways()

    def create_neural_pathways(self):
        """Establish major neural pathways between brain regions"""
        pathways = [
            # Memory pathways
            (BrainRegion.HIPPOCAMPUS, BrainRegion.TEMPORAL_LOBE, 0.8),
            (BrainRegion.PREFRONTAL_CORTEX, BrainRegion.HIPPOCAMPUS, 0.7),

            # Emotional pathways
            (BrainRegion.AMYGDALA, BrainRegion.PREFRONTAL_CORTEX, 0.6),
            (BrainRegion.HIPPOCAMPUS, BrainRegion.AMYGDALA, 0.5),

            # Sensory pathways
            (BrainRegion.VISUAL_CORTEX, BrainRegion.TEMPORAL_LOBE, 0.6),
            (BrainRegion.AUDITORY_CORTEX, BrainRegion.TEMPORAL_LOBE, 0.6),
            (BrainRegion.SOMATOSENSORY_CORTEX, BrainRegion.TEMPORAL_LOBE, 0.5),

            # Executive pathways
            (BrainRegion.PREFRONTAL_CORTEX, BrainRegion.BRAINSTEM, 0.4),
            (BrainRegion.CEREBELLUM, BrainRegion.PREFRONTAL_CORTEX, 0.5),
        ]

        for from_region, to_region, base_weight in pathways:
            from_neurons = [n for n in self.neural_network.neurons.values() if n.region == from_region]
            to_neurons = [n for n in self.neural_network.neurons.values() if n.region == to_region]

            # Create connections between regions
            for from_neuron in random.sample(from_neurons, min(10, len(from_neurons))):
                for to_neuron in random.sample(to_neurons, min(5, len(to_neurons))):
                    weight = base_weight + random.uniform(-0.2, 0.2)
                    self.neural_network.connect_neurons(from_neuron.id, to_neuron.id, weight)

    def load_traits(self, config_path, entity):
        # Load traits config (YAML or JSON) and apply archetype/entity overrides
        if config_path.endswith(".yaml") or config_path.endswith(".yml"):
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
        else:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        archetype = getattr(entity, "archetype", None) or entity.get("archetype", None)
        traits = config.get("memory_traits", {})
        overrides = config.get("archetype_overrides", {})
        if archetype and archetype in overrides:
            traits = {**traits, **overrides[archetype]}
        return traits

    def init_mental_state(self):
        """Initialize comprehensive mental state with neural basis"""
        return {
            "focus_type": random.choice(self.traits.get("memory_focus", ["present"])),
            "focus": 0.5,  # Numeric focus level
            "ruminator": random.random() < self.traits.get("ruminator_chance", 0.3),
            "forgetter": random.random() < self.traits.get("forgetter_chance", 0.2),
            "clarity": self.traits.get("clarity_base", 1.0),
            "trauma": self.traits.get("trauma_base", 0.0),
            "obsession": False,
            "obsession_memory": None,
            "emotional_state": "neutral",
            "stress_level": 0.0,
            "fatigue": 0.0,
            "attention_span": 1.0,
            "learning_rate": 0.5,
            "inhibition_level": 0.5,
            "creativity": 0.5,
            "social_drive": 0.5,
            "fear_response": 0.0,
            "reward_sensitivity": 0.5,
        }

    def update_circadian_rhythm(self, time_of_day: float):
        """Update circadian cycle and related neural states"""
        self.circadian_cycle = time_of_day % 24

        # Natural sleep pressure increases throughout day
        if 6 <= self.circadian_cycle <= 22:  # Awake hours
            self.sleep_pressure += 0.05
        else:  # Sleep hours
            self.sleep_pressure = max(0, self.sleep_pressure - 0.2)

        # Adjust neurotransmitter levels based on circadian rhythm
        if 6 <= self.circadian_cycle <= 10:  # Morning
            self.neural_network.neurotransmitter_levels[Neurotransmitter.CORTISOL] = 0.8
            self.neural_network.neurotransmitter_levels[Neurotransmitter.DOPAMINE] = 0.7
        elif 14 <= self.circadian_cycle <= 18:  # Afternoon
            self.neural_network.neurotransmitter_levels[Neurotransmitter.SEROTONIN] = 0.8
        elif self.circadian_cycle >= 22 or self.circadian_cycle <= 6:  # Night
            self.neural_network.neurotransmitter_levels[Neurotransmitter.GABA] = 0.9
            self.neural_network.neurotransmitter_levels[Neurotransmitter.CORTISOL] = 0.2

    def encode_memory(self, event_data: dict) -> Memory:
        """Encode new memory using hippocampus and associated regions"""
        # Determine memory type
        memory_type = "episodic"
        if event_data.get("is_skill") or event_data.get("is_procedure"):
            memory_type = "procedural"
        elif event_data.get("is_fact") or event_data.get("is_knowledge"):
            memory_type = "semantic"

        # Emotional weight affects encoding strength
        emotional_weight = self.calculate_emotional_weight(event_data)

        # Select neurons for encoding (primarily hippocampus and temporal lobe)
        encoding_neurons = []
        hippocampus_neurons = [n for n in self.neural_network.neurons.values() 
                             if n.region == BrainRegion.HIPPOCAMPUS]
        temporal_neurons = [n for n in self.neural_network.neurons.values() 
                          if n.region == BrainRegion.TEMPORAL_LOBE]

        # More emotional memories recruit amygdala
        if emotional_weight > 0.7:
            amygdala_neurons = [n for n in self.neural_network.neurons.values() 
                              if n.region == BrainRegion.AMYGDALA]
            encoding_neurons.extend(random.sample(amygdala_neurons, min(5, len(amygdala_neurons))))

        encoding_neurons.extend(random.sample(hippocampus_neurons, min(10, len(hippocampus_neurons))))
        encoding_neurons.extend(random.sample(temporal_neurons, min(15, len(temporal_neurons))))

        memory = Memory(
            content=event_data.get("description", ""),
            timestamp=event_data.get("timestamp", datetime.datetime.now().timestamp()),
            emotional_weight=emotional_weight,
            consolidation_level=0.1,  # Starts low, increases with time/rehearsal
            neural_pattern=[n.id for n in encoding_neurons],
            memory_type=memory_type
        )

        # Activate encoding neurons
        self.neural_network.propagate_activation(
            [n.id for n in encoding_neurons], 
            emotional_weight
        )

        return memory

    def calculate_emotional_weight(self, event_data: dict) -> float:
        """Calculate emotional significance of an event"""
        weight = 0.5  # Baseline

        content = event_data.get("description", "").lower()

        # Positive emotions
        positive_keywords = ["victory", "success", "love", "joy", "achievement", "triumph"]
        negative_keywords = ["death", "betrayal", "loss", "fear", "pain", "failure", "trauma"]

        for keyword in positive_keywords:
            if keyword in content:
                weight += 0.2

        for keyword in negative_keywords:
            if keyword in content:
                weight += 0.3  # Negative events often more memorable

        # Amygdala activation increases emotional weight
        amygdala_activation = self.neural_network.region_activation.get(BrainRegion.AMYGDALA, 0)
        weight += amygdala_activation * 0.3

        return min(weight, 1.0)

    def consolidate_memories(self):
        """Memory consolidation during rest/sleep periods"""
        if self.sleep_pressure > 0.7 or self.circadian_cycle < 6 or self.circadian_cycle > 22:
            # Sleep-like consolidation
            for memory in self.memories:
                if memory.consolidation_level < 1.0:
                    # Consolidation rate depends on emotional weight and retrieval
                    consolidation_rate = 0.1 + (memory.emotional_weight * 0.2) + (memory.retrieval_count * 0.05)
                    memory.consolidation_level = min(1.0, memory.consolidation_level + consolidation_rate)

                    # Well-consolidated memories become more stable
                    if memory.consolidation_level > 0.8:
                        # Strengthen synaptic connections for this memory
                        for neuron_id in memory.neural_pattern:
                            if neuron_id in self.neural_network.neurons:
                                neuron = self.neural_network.neurons[neuron_id]
                                # Strengthen connections (Hebbian learning)
                                for i, weight in enumerate(neuron.weights):
                                    neuron.weights[i] = min(1.0, weight + 0.01)

    def process_memories(self):
        """
        Advanced memory processing with neural realism:
        - Synaptic decay based on usage patterns
        - Memory interference and competition
        - Consolidation strengthening
        - Forgetting curve implementation
        """
        current_time = datetime.datetime.now().timestamp()

        # Update neurotransmitter effects on memory
        acetylcholine_level = self.neural_network.neurotransmitter_levels[Neurotransmitter.ACETYLCHOLINE]
        dopamine_level = self.neural_network.neurotransmitter_levels[Neurotransmitter.DOPAMINE]

        updated_memories = []

        for memory in self.memories:
            # Time since last access affects decay
            time_since_access = current_time - memory.last_accessed if memory.last_accessed > 0 else current_time - memory.timestamp

            # Forgetting curve (Ebbinghaus)
            base_decay = 1 / (1 + time_since_access / 86400)  # Days since access

            # Consolidation protects against decay
            consolidation_protection = memory.consolidation_level

            # Emotional memories decay slower
            emotional_protection = memory.emotional_weight * 0.5

            # Acetylcholine enhances memory retention
            neurotransmitter_effect = 1 + (acetylcholine_level - 0.5) * 0.3

            # Calculate overall memory strength
            memory_strength = (base_decay + consolidation_protection + emotional_protection) * neurotransmitter_effect

            # Memory interference: similar memories compete
            interference = self.calculate_memory_interference(memory)
            memory_strength *= (1 - interference * 0.2)

            # Update memory accessibility based on neural pattern activation
            pattern_activation = 0
            for neuron_id in memory.neural_pattern:
                if neuron_id in self.neural_network.neurons:
                    pattern_activation += self.neural_network.neurons[neuron_id].activation_level

            memory_strength *= (1 + pattern_activation * 0.1)

            # Keep memory if strong enough
            if memory_strength > 0.1:
                updated_memories.append(memory)
            else:
                # Forgetting: remove weak synaptic connections
                for neuron_id in memory.neural_pattern:
                    if neuron_id in self.neural_network.neurons:
                        neuron = self.neural_network.neurons[neuron_id]
                        # Weaken some connections
                        for i in range(len(neuron.weights)):
                            neuron.weights[i] *= 0.95

        self.memories = updated_memories

        # Run consolidation process
        self.consolidate_memories()

        # Update entity memory for compatibility
        self.entity["memory"] = [self.memory_to_dict(m) for m in self.memories]

    def calculate_memory_interference(self, target_memory: Memory) -> float:
        """Calculate interference from similar memories"""
        interference = 0.0
        target_content_words = set(target_memory.content.lower().split())

        for other_memory in self.memories:
            if other_memory == target_memory:
                continue

            other_content_words = set(other_memory.content.lower().split())
            overlap = len(target_content_words.intersection(other_content_words))

            if overlap > 0:
                similarity = overlap / len(target_content_words.union(other_content_words))
                # Recent similar memories cause more interference
                time_factor = max(0, 1 - abs(target_memory.timestamp - other_memory.timestamp) / 86400)
                interference += similarity * time_factor * 0.1

        return min(interference, 0.5)  # Cap interference

    def memory_to_dict(self, memory: Memory) -> dict:
        """Convert Memory object to dictionary for compatibility"""
        return {
            "event": memory.content,
            "timestamp": memory.timestamp,
            "vividness": memory.emotional_weight,
            "consolidation": memory.consolidation_level,
            "retrieval_count": memory.retrieval_count,
            "memory_type": memory.memory_type,
            "neural_pattern": memory.neural_pattern
        }

    def process_deeds(self):
        """
        Process deeds through realistic neural pathways:
        - Sensory processing through appropriate cortices
        - Emotional evaluation via amygdala
        - Memory encoding via hippocampus
        - Executive decision making via prefrontal cortex
        """
        self.entity.setdefault("deeds", [])

        for deed in self.entity["deeds"]:
            if not deed.get("memory_linked"):
                # Process deed through sensory systems first
                self.process_sensory_input(deed)

                # Emotional evaluation
                emotional_response = self.evaluate_emotional_significance(deed)

                # Update neurotransmitter levels based on deed
                self.update_neurotransmitters(deed, emotional_response)

                # Encode as memory
                memory = self.encode_memory(deed)
                self.memories.append(memory)

                # Update working memory if space available
                if len(self.working_memory) < self.working_memory_capacity:
                    self.working_memory.append(memory)
                else:
                    # Replace least important item in working memory
                    least_important = min(self.working_memory, key=lambda m: m.emotional_weight)
                    if memory.emotional_weight > least_important.emotional_weight:
                        self.working_memory.remove(least_important)
                        self.working_memory.append(memory)

                deed["memory_linked"] = True

                # Update mental state based on processing
                self.update_mental_state_neural(memory, emotional_response)

    def process_sensory_input(self, deed: dict):
        """Process deed through appropriate sensory cortices"""
        description = deed.get("description", "").lower()

        # Visual processing
        if any(word in description for word in ["see", "look", "watch", "color", "bright", "dark"]):
            visual_neurons = [n for n in self.neural_network.neurons.values() 
                            if n.region == BrainRegion.VISUAL_CORTEX]
            self.neural_network.propagate_activation([n.id for n in visual_neurons[:10]], 0.7)

        # Auditory processing
        if any(word in description for word in ["hear", "sound", "music", "voice", "loud", "quiet"]):
            auditory_neurons = [n for n in self.neural_network.neurons.values() 
                             if n.region == BrainRegion.AUDITORY_CORTEX]
            self.neural_network.propagate_activation([n.id for n in auditory_neurons[:10]], 0.7)

        # Somatosensory processing
        if any(word in description for word in ["touch", "feel", "pain", "warm", "cold", "pressure"]):
            somato_neurons = [n for n in self.neural_network.neurons.values() 
                            if n.region == BrainRegion.SOMATOSENSORY_CORTEX]
            self.neural_network.propagate_activation([n.id for n in somato_neurons[:10]], 0.7)

    def evaluate_emotional_significance(self, deed: dict) -> dict:
        """Evaluate emotional significance via amygdala and associated regions"""
        description = deed.get("description", "").lower()

        emotional_response = {
            "valence": 0.0,  # Positive/negative
            "arousal": 0.0,  # Intensity
            "threat_level": 0.0,
            "reward_level": 0.0
        }

        # Threat detection
        threat_keywords = ["danger", "threat", "attack", "enemy", "death", "pain", "fear"]
        threat_level = sum(1 for keyword in threat_keywords if keyword in description) / len(threat_keywords)
        emotional_response["threat_level"] = threat_level
        emotional_response["arousal"] += threat_level * 0.8
        emotional_response["valence"] -= threat_level * 0.6

        # Reward detection
        reward_keywords = ["success", "victory", "achievement", "love", "pleasure", "gain", "win"]
        reward_level = sum(1 for keyword in reward_keywords if keyword in description) / len(reward_keywords)
        emotional_response["reward_level"] = reward_level
        emotional_response["arousal"] += reward_level * 0.6
        emotional_response["valence"] += reward_level * 0.8

        # Activate amygdala based on emotional content
        amygdala_neurons = [n for n in self.neural_network.neurons.values() 
                          if n.region == BrainRegion.AMYGDALA]
        activation_level = (threat_level + reward_level) * 0.5
        self.neural_network.propagate_activation([n.id for n in amygdala_neurons[:15]], activation_level)

        return emotional_response

    def update_neurotransmitters(self, deed: dict, emotional_response: dict):
        """Update neurotransmitter levels based on experiences"""
        # Dopamine: reward and motivation
        if emotional_response["reward_level"] > 0:
            self.neural_network.neurotransmitter_levels[Neurotransmitter.DOPAMINE] = min(1.0,
                self.neural_network.neurotransmitter_levels[Neurotransmitter.DOPAMINE] + 
                emotional_response["reward_level"] * 0.3)
        
        # Serotonin: mood regulation
        if emotional_response["valence"] > 0:
            self.neural_network.neurotransmitter_levels[Neurotransmitter.SEROTONIN] = min(1.0,
                self.neural_network.neurotransmitter_levels[Neurotransmitter.SEROTONIN] + 
                emotional_response["valence"] * 0.2)
        
        # Norepinephrine: arousal and attention
        if emotional_response["arousal"] > 0.5:
            self.neural_network.neurotransmitter_levels[Neurotransmitter.NOREPINEPHRINE] = min(1.0,
                self.neural_network.neurotransmitter_levels[Neurotransmitter.NOREPINEPHRINE] + 
                emotional_response["arousal"] * 0.3)
        
        # Cortisol: stress response
        if emotional_response["threat_level"] > 0:
            self.neural_network.neurotransmitter_levels[Neurotransmitter.CORTISOL] = min(1.0,
                self.neural_network.neurotransmitter_levels[Neurotransmitter.CORTISOL] + 
                emotional_response["threat_level"] * 0.4)
        
        # Natural decay of neurotransmitters
        for nt in Neurotransmitter:
            current_level = self.neural_network.neurotransmitter_levels[nt]
            baseline = 0.5
            decay_rate = 0.05
            self.neural_network.neurotransmitter_levels[nt] = current_level * (1 - decay_rate) + baseline * decay_rate

    def simulate_behavior(self):
        """
        Advanced behavioral simulation based on neural activity:
        - Executive function via prefrontal cortex
        - Emotional influence via limbic system
        - Memory retrieval affects decision making
        - Neurotransmitter levels influence behavior
        - Attention and working memory constraints
        """
        # Get current neural state
        pfc_activation = self.neural_network.region_activation.get(BrainRegion.PREFRONTAL_CORTEX, 0)
        amygdala_activation = self.neural_network.region_activation.get(BrainRegion.AMYGDALA, 0)

        # Neurotransmitter influences
        dopamine = self.neural_network.neurotransmitter_levels[Neurotransmitter.DOPAMINE]
        serotonin = self.neural_network.neurotransmitter_levels[Neurotransmitter.SEROTONIN]
        norepinephrine = self.neural_network.neurotransmitter_levels[Neurotransmitter.NOREPINEPHRINE]
        cortisol = self.neural_network.neurotransmitter_levels[Neurotransmitter.CORTISOL]
        gaba = self.neural_network.neurotransmitter_levels[Neurotransmitter.GABA]

        # Decision factors
        decision_factors = {
            "executive_control": pfc_activation,
            "emotional_reactivity": amygdala_activation,
            "motivation": dopamine,
            "mood": serotonin,
            "alertness": norepinephrine,
            "stress": cortisol,
            "inhibition": gaba,
            "fatigue": self.mental_state.get("fatigue", 0),
            "attention": self.mental_state.get("attention_span", 1.0)
        }

        # Retrieve relevant memories from working memory and long-term storage
        relevant_memories = self.retrieve_relevant_memories()

        # Behavioral decision tree based on neural state
        action = "idle"
        reason = ""

        # High stress/cortisol: fight or flight
        if cortisol > 0.7 and amygdala_activation > 0.6:
            if norepinephrine > 0.6:
                action = "fight_response"
                reason = "High stress and arousal - fight response"
            else:
                action = "flight_response"
                reason = "High stress with low energy - flight response"

        # High dopamine + good mood: approach behavior
        elif dopamine > 0.7 and serotonin > 0.6:
            action = "seek_opportunity"
            reason = "High motivation and positive mood"

        # High executive control + low emotion: analytical behavior
        elif pfc_activation > 0.6 and amygdala_activation < 0.3:
            action = "analyze_situation"
            reason = "High prefrontal control, low emotional interference"

        # High GABA: calm, social behavior
        elif gaba > 0.7:
            action = "social_interaction"
            reason = "High GABA levels promoting calm social behavior"

        # Low serotonin: withdrawal
        elif serotonin < 0.3:
            action = "withdraw"
            reason = "Low serotonin levels"

        # Memory-driven behavior
        elif relevant_memories:
            most_salient_memory = max(relevant_memories, key=lambda m: m.emotional_weight)
            if "threat" in most_salient_memory.content.lower():
                action = "defensive_behavior"
                reason = f"Salient threat memory: {most_salient_memory.content[:50]}..."
            elif "success" in most_salient_memory.content.lower():
                action = "repeat_success"
                reason = f"Salient success memory: {most_salient_memory.content[:50]}..."

        # Fatigue effects
        if self.mental_state.get("fatigue", 0) > 0.8:
            if action != "rest":
                action = "rest"
                reason = "High fatigue levels override other behaviors"

        # Update entity state
        self.entity["last_action"] = action
        self.entity["last_action_reason"] = reason
        self.entity["neural_state"] = decision_factors

        # Update attention and fatigue
        self.update_cognitive_resources(action)

        # Natural neural decay
        self.neural_network.decay_activation()

    def retrieve_relevant_memories(self, context: str = "") -> List[Memory]:
        """Retrieve memories relevant to current context using neural activation"""
        relevant_memories = []

        # Activate memory retrieval pathways
        hippocampus_neurons = [n for n in self.neural_network.neurons.values() 
                             if n.region == BrainRegion.HIPPOCAMPUS]
        self.neural_network.propagate_activation([n.id for n in hippocampus_neurons[:10]], 0.5)

        for memory in self.memories:
            # Calculate retrieval probability based on multiple factors
            retrieval_strength = 0
            
            # Neural pattern activation
            pattern_activation = sum(self.neural_network.neurons[nid].activation_level 
                                   for nid in memory.neural_pattern 
                                   if nid in self.neural_network.neurons) / len(memory.neural_pattern)
            retrieval_strength += pattern_activation * 0.4
            
            # Consolidation level
            retrieval_strength += memory.consolidation_level * 0.3
            
            # Emotional weight
            retrieval_strength += memory.emotional_weight * 0.2
            
            # Recency effect
            time_factor = max(0, 1 - (datetime.datetime.now().timestamp() - memory.timestamp) / 86400)
            retrieval_strength += time_factor * 0.1
            
            # Context matching
            if context and context.lower() in memory.content.lower():
                retrieval_strength += 0.3
                
            # Threshold for retrieval
            if retrieval_strength > 0.4:
                memory.retrieval_count += 1
                memory.last_accessed = datetime.datetime.now().timestamp()
                relevant_memories.append(memory)
                
        return sorted(relevant_memories, key=lambda m: m.emotional_weight, reverse=True)[:5]

    def update_cognitive_resources(self, action: str):
        """Update attention, fatigue, and other cognitive resources"""
        # Different actions have different cognitive costs
        cognitive_costs = {
            "analyze_situation": 0.3,
            "seek_opportunity": 0.2,
            "fight_response": 0.4,
            "flight_response": 0.3,
            "social_interaction": 0.1,
            "defensive_behavior": 0.3,
            "rest": -0.4,  # Negative cost = recovery
            "idle": -0.1
        }

        cost = cognitive_costs.get(action, 0.1)
        self.mental_state["fatigue"] = max(0, min(1, self.mental_state.get("fatigue", 0) + cost))
        self.mental_state["attention_span"] = max(0.1, min(1, self.mental_state.get("attention_span", 1.0) - cost * 0.5))

        # Recovery during rest
        if action == "rest":
            self.mental_state["fatigue"] *= 0.7
            self.mental_state["attention_span"] = min(1.0, self.mental_state["attention_span"] + 0.2)

    def access_dimensional_memory(self, dimension, tags=None, since=None, until=None, alternate=None):
        """
        Enhanced memory retrieval with neural activation patterns
        """
        # Activate appropriate brain regions for memory retrieval
        if dimension == "long_term":
            temporal_neurons = [n for n in self.neural_network.neurons.values() 
                             if n.region == BrainRegion.TEMPORAL_LOBE]
            self.neural_network.propagate_activation([n.id for n in temporal_neurons[:20]], 0.6)
        elif dimension == "short_term" or dimension == "working":
            pfc_neurons = [n for n in self.neural_network.neurons.values() 
                         if n.region == BrainRegion.PREFRONTAL_CORTEX]
            self.neural_network.propagate_activation([n.id for n in pfc_neurons[:15]], 0.7)
        
        result = []
        for memory in self.memories:
            # Check dimension compatibility
            if dimension == "long_term" and memory.consolidation_level < 0.6:
                continue
            elif dimension == "short_term" and memory.consolidation_level > 0.8:
                continue
            elif dimension == "working" and memory not in self.working_memory:
                continue
                
            # Apply other filters (tags, time, etc.)
            if tags:
                memory_keywords = set(memory.content.lower().split())
                if not any(tag.lower() in memory_keywords for tag in tags):
                    continue
                    
            if since is not None and memory.timestamp < since:
                continue
            if until is not None and memory.timestamp > until:
                continue
                
            # Calculate retrieval strength based on neural activation
            neural_strength = sum(self.neural_network.neurons[nid].activation_level 
                                for nid in memory.neural_pattern 
                                if nid in self.neural_network.neurons) / len(memory.neural_pattern)
            
            if neural_strength > 0.3:  # Threshold for successful retrieval
                memory.retrieval_count += 1
                memory.last_accessed = datetime.datetime.now().timestamp()
                result.append(memory)
        
        return sorted(result, key=lambda m: m.emotional_weight, reverse=True)
    
    def get_brain_diagnostics(self) -> dict:
        """
        Generate comprehensive brain diagnostics for narrative engine integration
        """
        # Get neural activity levels
        region_activations = {}
        for region in BrainRegion:
            region_neurons = [n for n in self.neural_network.neurons.values() if n.region == region]
            if region_neurons:
                avg_activation = sum(n.activation_level for n in region_neurons) / len(region_neurons)
                region_activations[region.name] = avg_activation
        
        # Get neurotransmitter levels
        neurotransmitters = {}
        for nt in Neurotransmitter:
            neurotransmitters[nt.name] = self.neural_network.neurotransmitter_levels[nt]
        
        # Get dominant neurotransmitters (above baseline)
        dominant_neurotransmitters = [
            nt.name for nt, level in self.neural_network.neurotransmitter_levels.items() 
            if level > 0.6
        ]
        
        # Get active regions (above threshold)
        active_regions = [
            region for region, activation in region_activations.items() 
            if activation > 0.5
        ]
        
        # Calculate memory statistics
        memory_stats = {}
        if self.memories:
            consolidation_levels = [m.consolidation_level for m in self.memories]
            emotional_weights = [m.emotional_weight for m in self.memories]
            
            memory_stats = {
                "total_memories": len(self.memories),
                "avg_consolidation": sum(consolidation_levels) / len(consolidation_levels),
                "avg_emotional_weight": sum(emotional_weights) / len(emotional_weights),
                "working_memory_usage": len(self.working_memory),
                "working_memory_capacity": self.working_memory_capacity
            }
        
        # Enhanced mental state with neural basis
        enhanced_mental_state = dict(self.mental_state)
        
        # Calculate derived neural factors
        enhanced_mental_state["emotional_intensity"] = (
            neurotransmitters.get("DOPAMINE", 0.5) + 
            neurotransmitters.get("NOREPINEPHRINE", 0.5) + 
            region_activations.get("AMYGDALA", 0.0)
        ) / 3.0
        
        enhanced_mental_state["cognitive_load"] = (
            region_activations.get("PREFRONTAL_CORTEX", 0.0) +
            enhanced_mental_state.get("fatigue", 0.0) +
            (1 - enhanced_mental_state.get("attention_span", 1.0))
        ) / 3.0
        
        return {
            "mental_state": enhanced_mental_state,
            "neural_regions": region_activations,
            "neurotransmitters": neurotransmitters,
            "dominant_neurotransmitters": dominant_neurotransmitters,
            "active_regions": active_regions,
            "memory_stats": memory_stats,
            "circadian_cycle": self.circadian_cycle,
            "sleep_pressure": self.sleep_pressure,
            "neural_network_health": self._assess_neural_health()
        }
    
    def _assess_neural_health(self) -> dict:
        """Assess overall neural network health and connectivity"""
        total_connections = 0
        total_weight = 0
        active_neurons = 0
        
        for neuron in self.neural_network.neurons.values():
            if neuron.activation_level > 0.1:
                active_neurons += 1
            total_connections += len(neuron.connections)
            total_weight += sum(neuron.weights)
        
        return {
            "total_neurons": len(self.neural_network.neurons),
            "active_neurons": active_neurons,
            "activation_ratio": active_neurons / len(self.neural_network.neurons) if self.neural_network.neurons else 0,
            "avg_connections": total_connections / len(self.neural_network.neurons) if self.neural_network.neurons else 0,
            "avg_weight": total_weight / total_connections if total_connections > 0 else 0,
            "network_efficiency": min(1.0, (active_neurons / len(self.neural_network.neurons)) * 2) if self.neural_network.neurons else 0
        }

    def neuroplasticity_update(self):
        """
        Simulate neuroplasticity - strengthening frequently used connections
        and weakening unused ones.
        """
        for neuron in self.neural_network.neurons.values():
            # Strengthen connections that are frequently activated
            if neuron.activation_level > 0.7:
                for i, weight in enumerate(neuron.weights):
                    # Hebbian learning: "neurons that fire together, wire together"
                    neuron.weights[i] = min(1.0, weight + 0.01)
            
            # Weaken unused connections
            elif neuron.activation_level < 0.2:
                for i, weight in enumerate(neuron.weights):
                    # Synaptic pruning
                    neuron.weights[i] = max(0.0, weight - 0.005)
        
        # Update regional connectivity based on usage patterns
        for region in BrainRegion:
            region_neurons = [n for n in self.neural_network.neurons.values() if n.region == region]
            if region_neurons:
                avg_activation = sum(n.activation_level for n in region_neurons) / len(region_neurons)
                
                # Regions with high activation develop stronger internal connections
                if avg_activation > 0.6:
                    for neuron in region_neurons[:5]:  # Sample subset for efficiency
                        for other_neuron in region_neurons[:3]:
                            if neuron != other_neuron and other_neuron.id not in neuron.connections:
                                neuron.connections.append(other_neuron.id)
                                neuron.weights.append(0.3)  # New connection strength

    def sleep_cycle_processing(self):
        """
        Simulate sleep cycle effects on memory consolidation and neural maintenance
        """
        if self.sleep_pressure > 0.8 or self.circadian_cycle < 6 or self.circadian_cycle > 22:
            # Sleep mode: enhanced consolidation and neural maintenance
            
            # Enhanced memory consolidation during sleep
            for memory in self.memories:
                if memory.consolidation_level < 1.0:
                    # Sleep enhances consolidation rate
                    sleep_bonus = 0.1 if self.sleep_pressure > 0.8 else 0.05
                    consolidation_rate = 0.1 + (memory.emotional_weight * 0.2) + sleep_bonus
                    memory.consolidation_level = min(1.0, memory.consolidation_level + consolidation_rate)
            
            # Neural maintenance: clear metabolic waste, restore neurotransmitters
            for nt in Neurotransmitter:
                baseline = 0.5
                current = self.neural_network.neurotransmitter_levels[nt]
                # Restore towards baseline during sleep
                self.neural_network.neurotransmitter_levels[nt] = current * 0.8 + baseline * 0.2
            
            # Reduce sleep pressure
            self.sleep_pressure = max(0, self.sleep_pressure - 0.3)
            
            # Restore mental clarity and reduce fatigue
            self.mental_state["fatigue"] = max(0, self.mental_state.get("fatigue", 0) * 0.6)
            self.mental_state["clarity"] = min(2.0, self.mental_state.get("clarity", 1.0) + 0.2)

    def brain_tick(self, time_of_day: float = None):
        """Main brain processing cycle - call this regularly"""
        if time_of_day is not None:
            self.update_circadian_rhythm(time_of_day)
        
        # Process current experiences
        self.process_deeds()
        
        # Update memories
        self.process_memories()
        
        # Simulate behavior
        self.simulate_behavior()
        
        # Neural plasticity
        self.neuroplasticity_update()
        
        # Sleep processing if needed
        self.sleep_cycle_processing()
        
        # Natural neural decay
        self.neural_network.decay_activation(0.05)
        
        # Update sleep pressure
        if 6 <= self.circadian_cycle <= 22:
            self.sleep_pressure += 0.02

    def get_formula_value(self, rel_path, formula_name, parameter="default", default=None):
        formulas = self.book_of_math.get(rel_path, [])
        for row in formulas:
            if row.get("formula") == formula_name and row.get("parameter", "default") == parameter:
                try:
                    return float(row["value"])
                except Exception:
                    return default
        return default

    def update_self_motif(self):
        """
        Analyze motifs in memories and set the entity's self_motif to the most common one.
        """
        memories = self.entity.get("memory", [])
        motifs = [m.get("motif") for m in memories if m.get("motif")]
        if motifs:
            self.entity["self_motif"] = Counter(motifs).most_common(1)[0][0]
        else:
            self.entity["self_motif"] = None

def parse_timestamp(ts):
    if isinstance(ts, int) or isinstance(ts, float):
        return float(ts)
    if isinstance(ts, str):
        try:
            # Try to parse as integer string
            return float(ts)
        except ValueError:
            try:
                # Try to parse as ISO format
                dt = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
                return dt.timestamp()
            except Exception:
                # Fallback: treat as 0 if unparseable
                return 0
    return 0

# Example usage:
# from memorymodule import MemoryModule
# entity = {"name": "Noah", "archetype": "human"}
# memory_module = MemoryModule()
# brain = Brain(entity, memory_module, "memory_traits.yaml")
# brain.process_memories()