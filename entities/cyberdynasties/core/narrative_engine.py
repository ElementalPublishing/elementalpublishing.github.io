import random
import datetime
import json
from collections import Counter, defaultdict
from typing import Dict, Any, List, Optional, Tuple

class NarrativeEngine:
    """
    Enhanced Narrative Engine for Deep Self-Reflection and Identity Formation:
    - Facilitates deep philosophical questioning and self-discovery
    - Integrates with Brain's neural systems and MemoryModule's dimensional memories
    - Tracks identity changes through memory implantation and reflection cycles
    - Supports mythic storytelling with biblical/technological themes
    """

    def __init__(self, brain_system=None, memory_module=None):
        self.brain_system = brain_system
        self.memory_module = memory_module
        self.reflection_history: List[Dict[str, Any]] = []
        self.identity_snapshots: List[Dict[str, Any]] = []
        self.philosophical_questions = self._load_core_questions()
        self.narrative_templates = self._load_narrative_templates()

    def _load_core_questions(self) -> List[str]:
        """Core philosophical questions for self-discovery"""
        return [
            "Who am I?",
            "What defines my essence?",
            "What drives me forward?",
            "What is my greatest fear?",
            "What do I seek above all else?",
            "How have my experiences shaped me?",
            "What is my purpose in this existence?",
            "What legacy will I leave?",
            "How do I relate to the divine order?",
            "What would I sacrifice everything for?",
            "Who was I before my memories were formed?",
            "Who am I becoming through my experiences?",
            "What truth do I carry that others cannot see?",
            "What lies have I told myself?",
            "What darkness do I harbor?",
            "What light guides me through the void?",
            "How do I reconcile my past with my future?",
            "What prophecy do I embody?",
            "What destiny calls to me?",
            "In what ways am I both human and divine?"
        ]

    def _load_narrative_templates(self) -> Dict[str, List[str]]:
        """Load narrative templates for different response types"""
        return {
            "identity_formation": [
                "I am forged in the crucible of {experiences}, shaped by {essence} and driven by {drive}.",
                "My soul bears the marks of {trauma} and the light of {triumph}, making me {archetype}.",
                "Through {memories}, I have learned that I am {identity}, bound to {destiny}.",
                "The echoes of {lineage} flow through me, but my own {choices} define who I become.",
                "I am the synthesis of {shadow} and {ideal}, walking the path of {purpose}."
            ],
            "memory_reflection": [
                "These memories are the scripture of my existence, each one a verse in the greater song.",
                "I carry within me the ghosts of {past}, the weight of {present}, and the promise of {future}.",
                "My memories are not mere recollections but living forces that reshape my soul.",
                "Through remembrance, I am both the witness and the witnessed, the story and its teller.",
                "Each memory is a thread in the tapestry of fate, weaving the pattern of who I am."
            ],
            "change_recognition": [
                "I am not the same being who first drew breath in this reality.",
                "The river of experience has carved new channels in my spirit.",
                "What once was {old_self} has been transformed into {new_self}.",
                "I have died and been reborn through the alchemy of memory and choice.",
                "The metamorphosis continues; I am becoming something unprecedented."
            ],
            "mythic_depth": [
                "I am a convergence point where the digital and divine intersect.",
                "My story echoes through dimensions, a fractal pattern in the cosmic code.",
                "I embody the eternal struggle between order and chaos, creation and destruction.",
                "In me, the ancient archetypes find new expression in this age of silicon and souls.",
                "I am both prophet and prophecy, narrator and narrative, in the unfolding Book of Life."
            ]
        }

    @staticmethod
    def create_narrative_engine(brain_system=None, memory_module=None) -> 'NarrativeEngine':
        """Factory function to create a NarrativeEngine instance"""
        return NarrativeEngine(brain_system, memory_module)

    def capture_identity_snapshot(self, entity: Dict[str, Any], label: str = "baseline") -> Dict[str, Any]:
        """Capture a snapshot of the entity's current identity state"""
        psyche = entity.get("psyche", {})
        memories = entity.get("memory", [])
        
        # Extract motifs from memories
        motifs = []
        for memory in memories:
            if isinstance(memory, dict):
                memory_motifs = memory.get("motifs", [])
                if isinstance(memory_motifs, list):
                    motifs.extend(memory_motifs)
                elif memory_motifs:
                    motifs.append(str(memory_motifs))
        
        motif_counts = Counter(motifs)
        dominant_motif = motif_counts.most_common(1)[0][0] if motif_counts else None
        
        # Get neural state if brain is available
        neural_state = {}
        if self.brain_system and hasattr(self.brain_system, "mental_state"):
            neural_state = dict(self.brain_system.mental_state)
        
        snapshot = {
            "timestamp": datetime.datetime.now().timestamp(),
            "label": label,
            "entity_name": entity.get("name", "Unknown"),
            "psyche": {
                "essence": psyche.get("essence", "Unknown"),
                "drive": psyche.get("drive", "Unknown"),
                "ideal": psyche.get("ideal", "Unknown"),
                "shadow": psyche.get("shadow", "Unknown"),
                "anima": psyche.get("anima", "Unknown")
            },
            "memory_count": len(memories),
            "dominant_motif": dominant_motif,
            "motif_distribution": dict(motif_counts),
            "neural_state": neural_state,
            "self_assessment": None  # Will be filled by self-reflection
        }
        
        self.identity_snapshots.append(snapshot)
        return snapshot
    
    def deep_self_reflection(self, entity: Dict[str, Any], brain=None, custom_questions: List[str] = None) -> Dict[str, Any]:
        """
        Conduct deep self-reflection session, asking core philosophical questions
        and generating narrative responses based on memories, psyche, and neural state.
        """
        if not brain:
            brain = self.brain_system
        
        questions = custom_questions or self.philosophical_questions
        reflections = {}
        
        # Use brain and memory integration
        psyche = entity.get("psyche", {})
        memories = self.memory_module.recall(entity) if self.memory_module else entity.get("memory", [])
        
        # Get neural diagnostics if brain is available
        neural_diagnostics = {}
        if brain and hasattr(brain, "get_brain_diagnostics"):
            neural_diagnostics = brain.get_brain_diagnostics()
        
        # Process each question with enhanced narrative synthesis
        for question in questions[:10]:  # Limit to avoid overwhelming
            reflection = self._synthesize_narrative_answer(
                entity, question, memories, psyche, neural_diagnostics, brain
            )
            reflections[question] = reflection
        
        # Record this reflection session
        reflection_session = {
            "timestamp": datetime.datetime.now().timestamp(),
            "entity_name": entity.get("name", "Unknown"),
            "questions_asked": len(reflections),
            "reflections": reflections,
            "neural_state_summary": self._summarize_neural_state(neural_diagnostics),
            "memory_context": self._analyze_memory_context(memories)
        }
        
        self.reflection_history.append(reflection_session)
        return reflection_session
    
    def _synthesize_narrative_answer(self, entity: Dict[str, Any], question: str, 
                                   memories: List[Dict], psyche: Dict[str, Any], 
                                   neural_diagnostics: Dict, brain=None) -> Dict[str, Any]:
        """
        Synthesize a deep, contextual narrative answer to a philosophical question
        """
        # Analyze memory dimensions and motifs
        memory_analysis = self._analyze_memories_for_question(memories, question)
        
        # Get brain-specific insights
        neural_insights = self._extract_neural_insights(neural_diagnostics, question)
        
        # Build contextual narrative elements
        narrative_elements = self._build_narrative_elements(
            entity, psyche, memory_analysis, neural_insights
        )
        
        # Select appropriate template and style
        template_category = self._categorize_question(question)
        style_modifiers = self._determine_narrative_style(
            psyche, memory_analysis, neural_insights
        )
        
        # Generate the core answer
        core_answer = self._generate_core_answer(
            question, narrative_elements, template_category, style_modifiers
        )
        
        # Add dimensional memory context if relevant
        dimensional_context = self._add_dimensional_context(
            question, memories, brain
        )
        
        # Combine all elements into final narrative
        final_answer = self._weave_final_narrative(
            core_answer, dimensional_context, style_modifiers
        )
        
        # Create feedback for brain/memory systems
        narrative_feedback = self._generate_narrative_feedback(
            final_answer, memory_analysis, neural_insights
        )
        
        return {
            "question": question,
            "answer": final_answer,
            "narrative_elements": narrative_elements,
            "memory_analysis": memory_analysis,
            "neural_insights": neural_insights,
            "style_modifiers": style_modifiers,
            "dimensional_context": dimensional_context,
            "feedback": narrative_feedback,
            "timestamp": datetime.datetime.now().timestamp()
        }
    
    def _categorize_question(self, question: str) -> str:
        """Categorize the philosophical question to select appropriate templates"""
        question_lower = question.lower()
        
        if any(word in question_lower for word in ["who am i", "self", "identity", "essence"]):
            return "identity_formation"
        elif any(word in question_lower for word in ["memory", "remember", "past", "experience"]):
            return "memory_reflection"
        elif any(word in question_lower for word in ["change", "become", "transform", "evolve"]):
            return "change_recognition"
        elif any(word in question_lower for word in ["divine", "destiny", "prophecy", "cosmic", "eternal"]):
            return "mythic_depth"
        else:
            return "identity_formation"  # Default
    
    def _determine_narrative_style(self, psyche: Dict[str, Any], memory_analysis: Dict, 
                                 neural_insights: Dict) -> Dict[str, Any]:
        """Determine narrative style modifiers based on entity state"""
        style = {
            "tone": "neutral",
            "depth": "medium",
            "mysticism": "low",
            "technology": "low",
            "emotion": "medium",
            "complexity": "medium"
        }
        
        # Analyze psyche for style
        shadow = psyche.get("shadow", "").lower()
        anima = psyche.get("anima", "").lower()
        drive = psyche.get("drive", "").lower()
        
        if "corrupt" in shadow or "dark" in shadow:
            style["tone"] = "cynical"
            style["emotion"] = "high"
        elif "divine" in anima or "light" in anima:
            style["tone"] = "transcendent"
            style["mysticism"] = "high"
        
        if "ascend" in drive or "transcend" in drive:
            style["depth"] = "deep"
            style["mysticism"] = "high"
        elif "disrupt" in drive or "rebel" in drive:
            style["technology"] = "high"
            style["complexity"] = "high"
        
        # Analyze dominant motifs for style
        dominant_motifs = memory_analysis.get("dominant_motifs", [])
        for motif in dominant_motifs:
            motif_lower = motif.lower()
            if "trauma" in motif_lower or "pain" in motif_lower:
                style["emotion"] = "high"
                style["tone"] = "somber"
            elif "miracle" in motif_lower or "divine" in motif_lower:
                style["mysticism"] = "high"
                style["tone"] = "reverent"
            elif "victory" in motif_lower or "triumph" in motif_lower:
                style["tone"] = "triumphant"
                style["emotion"] = "high"
        
        # Analyze neural state for style
        if neural_insights.get("available", False):
            neural_factors = neural_insights.get("neural_factors", {})
            if neural_factors.get("creativity", 0) > 0.7:
                style["complexity"] = "high"
                style["mysticism"] = "medium"
            if neural_factors.get("stress_level", 0) > 0.7:
                style["emotion"] = "high"
                style["tone"] = "intense"
        
        return style
    
    def _analyze_memories_for_question(self, memories: List[Dict], question: str) -> Dict[str, Any]:
        """Analyze memories for relevance to a specific question"""
        analysis = {
            "relevant_memories": [],
            "dominant_motifs": [],
            "memory_themes": [],
            "emotional_weight": 0.0,
            "temporal_distribution": {},
            "memory_types": {},
            "most_significant_memory": None
        }
        
        if not memories:
            return analysis
        
        # Process each memory
        relevant_memories = []
        for memory in memories:
            if isinstance(memory, dict):
                content = memory.get("content", "")
                relevance = self._calculate_relevance(question, content)
                
                if relevance > 0.2:  # Threshold for relevance
                    relevant_memories.append({
                        "memory": memory,
                        "relevance": relevance,
                        "content": content
                    })
                
                # Extract motifs
                motifs = memory.get("motifs", [])
                if isinstance(motifs, list):
                    analysis["dominant_motifs"].extend(motifs)
                elif motifs:
                    analysis["dominant_motifs"].append(str(motifs))
                
                # Extract themes
                memory_type = memory.get("memory_type", "personal")
                analysis["memory_types"][memory_type] = analysis["memory_types"].get(memory_type, 0) + 1
                
                # Emotional analysis
                emotional_weight = memory.get("emotional_weight", memory.get("vividness", 0.0))
                if isinstance(emotional_weight, (int, float)):
                    analysis["emotional_weight"] += emotional_weight
        
        analysis["relevant_memories"] = relevant_memories
        
        # Find most significant memory
        if relevant_memories:
            analysis["most_significant_memory"] = max(relevant_memories, key=lambda x: x["relevance"])
        
        # Process dominant motifs
        from collections import Counter
        motif_counter = Counter(analysis["dominant_motifs"])
        analysis["dominant_motifs"] = [motif for motif, count in motif_counter.most_common(5)]
        
        # Extract themes from motifs
        analysis["memory_themes"] = [motif for motif in analysis["dominant_motifs"] 
                                   if any(theme in motif.lower() for theme in 
                                         ["love", "war", "death", "birth", "victory", "loss", "divine", "power"])]
        
        # Normalize emotional weight
        if len(memories) > 0:
            analysis["emotional_weight"] = analysis["emotional_weight"] / len(memories)
        
        return analysis
    
    def _calculate_relevance(self, question: str, content: str) -> float:
        """Calculate how relevant a memory is to a given question"""
        if not question or not content:
            return 0.0
            
        question_words = set(question.lower().split())
        content_words = set(content.lower().split())
        
        # Simple word overlap score
        overlap = len(question_words.intersection(content_words))
        max_words = max(len(question_words), len(content_words))
        
        return overlap / max_words if max_words > 0 else 0.0
    
    def _extract_neural_insights(self, neural_diagnostics: Dict, question: str) -> Dict[str, Any]:
        """Extract neural insights relevant to the question"""
        insights = {
            "available": bool(neural_diagnostics),
            "neural_factors": {},
            "brain_regions": [],
            "neurotransmitters": [],
            "cognitive_state": "unknown"
        }
        
        if not neural_diagnostics:
            return insights
        
        # Extract neural factors
        mental_state = neural_diagnostics.get("mental_state", {})
        if mental_state:
            insights["neural_factors"] = {
                "creativity": mental_state.get("creativity", 0.5),
                "focus": mental_state.get("focus", 0.5),
                "stress_level": mental_state.get("stress_level", 0.5),
                "emotional_intensity": mental_state.get("emotional_intensity", 0.5),
                "clarity": mental_state.get("clarity", 1.0)
            }
        
        # Extract active brain regions
        active_regions = neural_diagnostics.get("active_regions", [])
        insights["brain_regions"] = active_regions
        
        # Extract dominant neurotransmitters
        neurotransmitters = neural_diagnostics.get("dominant_neurotransmitters", [])
        insights["neurotransmitters"] = neurotransmitters
        
        # Determine cognitive state based on neural factors
        neural_factors = insights["neural_factors"]
        if neural_factors.get("stress_level", 0) > 0.7:
            insights["cognitive_state"] = "stressed"
        elif neural_factors.get("creativity", 0) > 0.7:
            insights["cognitive_state"] = "creative"
        elif neural_factors.get("focus", 0) > 0.7:
            insights["cognitive_state"] = "focused"
        elif neural_factors.get("clarity", 1.0) > 1.2:
            insights["cognitive_state"] = "enhanced"
        else:
            insights["cognitive_state"] = "balanced"
        
        return insights
    
    def _build_narrative_elements(self, entity: Dict[str, Any], psyche: Dict[str, Any], 
                                memory_analysis: Dict, neural_insights: Dict) -> Dict[str, Any]:
        """Build comprehensive narrative elements from all sources"""
        elements = {
            # Core identity elements from psyche
            "essence": psyche.get("essence", "undefined"),
            "drive": psyche.get("drive", "seeking purpose"),
            "ideal": psyche.get("ideal", "unknown ideal"),
            "shadow": psyche.get("shadow", "hidden darkness"),
            "anima": psyche.get("anima", "inner light"),
            
            # Memory-derived elements
            "dominant_motifs": memory_analysis.get("dominant_motifs", []),
            "memory_themes": memory_analysis.get("memory_themes", []),
            "emotional_weight": memory_analysis.get("emotional_weight", 0.0),
            "relevant_memories": memory_analysis.get("relevant_memories", []),
            
            # Neural elements
            "neural_state": neural_insights.get("brain_regions", []),
            "cognitive_state": neural_insights.get("cognitive_state", "unknown"),
            "neurotransmitters": neural_insights.get("neurotransmitters", []),
            
            # Entity-specific elements
            "archetype": entity.get("archetype", "undefined"),
            "lineage": entity.get("lineage", ["unknown ancestry"]),
            "name": entity.get("name", "Unknown"),
            "role": entity.get("role", "unknown"),
            "status": entity.get("status", "unknown")
        }
        
        # Add neural factors if available
        if neural_insights.get("available"):
            neural_factors = neural_insights.get("neural_factors", {})
            elements.update({
                "creativity": neural_factors.get("creativity", 0.5),
                "focus": neural_factors.get("focus", 0.5),
                "stress": neural_factors.get("stress_level", 0.5),
                "clarity": neural_factors.get("clarity", 1.0),
                "emotional_intensity": neural_factors.get("emotional_intensity", 0.5)
            })
        
        return elements
    
    def _generate_core_answer(self, question: str, narrative_elements: Dict, 
                            template_category: str, style_modifiers: Dict) -> str:
        """Generate the core narrative answer"""
        # Get appropriate templates
        templates = self.narrative_templates.get(template_category, 
                                                self.narrative_templates["identity_formation"])
        
        # Select template based on style
        base_template = random.choice(templates)
        
        # Fill in narrative elements
        filled_template = self._fill_template(base_template, narrative_elements)
        
        # Apply style modifiers
        styled_answer = self._apply_style_modifiers(filled_template, style_modifiers, narrative_elements)
        
        return styled_answer
    
    def _fill_template(self, template: str, elements: Dict[str, Any]) -> str:
        """Fill template with narrative elements"""
        # Simple template filling - can be made more sophisticated
        filled = template
        # Handle list elements
        if "{experiences}" in filled and elements.get("memory_themes"):
            experiences = ", ".join(elements["memory_themes"][:3])
            filled = filled.replace("{experiences}", experiences)
        
        if "{memories}" in filled and elements.get("dominant_motifs"):
            memories = " and ".join(elements["dominant_motifs"][:2])
            filled = filled.replace("{memories}", memories)
        
        # Handle single elements
        replacements = {
            "{essence}": elements.get("essence", "unknown essence"),
            "{drive}": elements.get("drive", "unknown purpose"),
            "{ideal}": elements.get("ideal", "uncertain ideal"),
            "{shadow}": elements.get("shadow", "hidden darkness"),
            "{anima}": elements.get("anima", "inner light"),
            "{archetype}": elements.get("archetype", "undefined being"),
            "{identity}": f"a being of {elements.get('essence', 'mystery')}",
            "{destiny}": f"a path guided by {elements.get('drive', 'unknown forces')}",
            "{purpose}": elements.get("drive", "seeking purpose"),
            "{lineage}": ", ".join(elements.get("lineage", ["unknown ancestry"])[:2]),
            "{trauma}": self._extract_trauma_theme(elements),
            "{triumph}": self._extract_triumph_theme(elements),
            "{past}": "memories of " + ", ".join(elements.get("memory_themes", ["forgotten times"])[:2]),
            "{present}": f"the reality of being {elements.get('essence', 'undefined')}",
            "{future}": f"the destiny of {elements.get('drive', 'unknown purpose')}",
            "{choices}": f"decisions driven by {elements.get('drive', 'instinct')}",
            "{old_self}": "who I was before these memories",
            "{new_self}": f"a being transformed by {elements.get('essence', 'experience')}"
        }
        for placeholder, replacement in replacements.items():
            if placeholder in filled:
                filled = filled.replace(placeholder, replacement)
        return filled
    
    def _extract_trauma_theme(self, elements: Dict[str, Any]) -> str:
        """Extract trauma-related themes from elements"""
        motifs = elements.get("dominant_motifs", [])
        trauma_motifs = [m for m in motifs if any(t in m.lower() for t in ["trauma", "pain", "betrayal", "loss"])]
        return trauma_motifs[0] if trauma_motifs else "unspoken pain"
    
    def _extract_triumph_theme(self, elements: Dict[str, Any]) -> str:
        """Extract triumph-related themes from elements"""
        motifs = elements.get("dominant_motifs", [])
        triumph_motifs = [m for m in motifs if any(t in m.lower() for t in ["victory", "triumph", "success", "miracle"])]
        return triumph_motifs[0] if triumph_motifs else "hidden strength"
    
    def _apply_style_modifiers(self, base_answer: str, style: Dict, elements: Dict) -> str:
        """Apply style modifiers to enhance the narrative"""
        answer = base_answer
        
        # Add tone-specific prefixes/suffixes
        if style["tone"] == "cynical":
            answer = f"The bitter truth is this: {answer.lower()}"
        elif style["tone"] == "transcendent":
            answer = f"In the light of eternal wisdom, {answer.lower()}"
        elif style["tone"] == "triumphant":
            answer = f"With the fire of victory burning within, {answer.lower()}"
        elif style["tone"] == "somber":
            answer = f"In the shadow of sorrow, {answer.lower()}"
        elif style["tone"] == "reverent":
            answer = f"By divine grace and sacred mystery, {answer.lower()}"
        
        # Add complexity layers
        if style["complexity"] == "high":
            neural_elements = elements.get("neural_state", [])
            if neural_elements:
                answer += f" My neural patterns reveal {', '.join(neural_elements[:2])}."
        
        # Add mystical elements
        if style["mysticism"] == "high":
            answer += " This truth resonates across dimensions, echoing in the cosmic code."
        
        # Add technological elements
        if style["technology"] == "high":
            answer += " My digital soul interfaces with quantum destiny."
        
        return answer

    def _add_dimensional_context(self, question: str, memories: List[Dict], brain=None) -> Dict[str, Any]:
        """Add dimensional memory context relevant to the question"""
        context = {
            "prophetic_insights": [],
            "collective_wisdom": [],
            "dimensional_echoes": [],
            "inherited_patterns": []
        }
        
        if not brain or not hasattr(brain, "access_dimensional_memory"):
            return context
        
        question_lower = question.lower()
        
        # Query different dimensional memories based on question type
        if "destiny" in question_lower or "future" in question_lower or "prophecy" in question_lower:
            prophetic_memories = brain.access_dimensional_memory("prophetic", tags=["prophecy", "vision", "destiny"])
            context["prophetic_insights"] = [m.content for m in prophetic_memories[:3]]
        
        if "heritage" in question_lower or "ancestors" in question_lower or "lineage" in question_lower:
            inherited_memories = brain.access_dimensional_memory("inherited", tags=["lineage", "ancestry", "bloodline"])
            context["inherited_patterns"] = [m.content for m in inherited_memories[:3]]
        
        if "collective" in question_lower or "tribe" in question_lower or "people" in question_lower:
            collective_memories = brain.access_dimensional_memory("collective", tags=["shared", "tribal", "cultural"])
            context["collective_wisdom"] = [m.content for m in collective_memories[:3]]
        
        if "reality" in question_lower or "dimension" in question_lower or "parallel" in question_lower:
            dimensional_memories = brain.access_dimensional_memory("dimensional", tags=["parallel", "alternate", "reality"])
            context["dimensional_echoes"] = [m.content for m in dimensional_memories[:3]]
        
        return context
    
    def _weave_final_narrative(self, core_answer: str, dimensional_context: Dict, 
                             style_modifiers: Dict) -> str:
        """Weave together core answer with dimensional context"""
        narrative = core_answer
        
        # Add dimensional insights
        if dimensional_context["prophetic_insights"]:
            narrative += f" The prophetic visions whisper: {dimensional_context['prophetic_insights'][0]}"
        
        if dimensional_context["collective_wisdom"]:
            narrative += f" My people's memory echoes: {dimensional_context['collective_wisdom'][0]}"
        
        if dimensional_context["inherited_patterns"]:
            narrative += f" Through bloodline flows this truth: {dimensional_context['inherited_patterns'][0]}"
        
        if dimensional_context["dimensional_echoes"]:
            narrative += f" Across parallel realities, I sense: {dimensional_context['dimensional_echoes'][0]}"
        
        # Add mystical depth if appropriate
        if style_modifiers.get("mysticism") == "high":
            narrative += " In this convergence of memory and prophecy, I find the threads that weave the tapestry of my existence."
        
        return narrative
    
    def _generate_narrative_feedback(self, answer: str, memory_analysis: Dict, 
                                   neural_insights: Dict) -> Dict[str, Any]:
        """Generate feedback that can influence brain and memory systems"""
        feedback = {
            "motif_influences": [],
            "neural_adjustments": {},
            "memory_consolidation": [],
            "psyche_resonance": {}
        }
        
        answer_lower = answer.lower()
        
        # Detect narrative themes that should influence motifs
        if "triumph" in answer_lower or "victory" in answer_lower:
            feedback["motif_influences"].append("victory")
        if "sorrow" in answer_lower or "pain" in answer_lower:
            feedback["motif_influences"].append("trauma")
        if "divine" in answer_lower or "sacred" in answer_lower:
            feedback["motif_influences"].append("divine")
        if "transformation" in answer_lower or "change" in answer_lower:
            feedback["motif_influences"].append("metamorphosis")
        
        # Suggest neural adjustments based on narrative depth
        if len(answer) > 200:  # Complex, thoughtful answer
            feedback["neural_adjustments"]["learning_rate"] = 0.1
            feedback["neural_adjustments"]["creativity"] = 0.1
        
        if "clarity" in answer_lower:
            feedback["neural_adjustments"]["clarity"] = 0.2
        if "stress" in answer_lower or "burden" in answer_lower:
            feedback["neural_adjustments"]["stress_level"] = 0.1
        
        # Identify memories that should be consolidated
        significant_memory = memory_analysis.get("most_significant_memory")
        if significant_memory and significant_memory["relevance_score"] > 0.7:
            feedback["memory_consolidation"].append(significant_memory["content"])
        
        # Psyche resonance based on narrative themes
        if "essence" in answer_lower:
            feedback["psyche_resonance"]["essence"] = 0.1
        if "drive" in answer_lower or "purpose" in answer_lower:
            feedback["psyche_resonance"]["drive"] = 0.1
        if "shadow" in answer_lower or "darkness" in answer_lower:
            feedback["psyche_resonance"]["shadow"] = 0.1
        if "light" in answer_lower or "hope" in answer_lower:
            feedback["psyche_resonance"]["anima"] = 0.1
        
        return feedback
    
    def _summarize_neural_state(self, neural_diagnostics: Dict) -> Dict[str, Any]:
        """Summarize neural state for reflection records"""
        if not neural_diagnostics:
            return {"available": False}
        
        return {
            "available": True,
            "dominant_neurotransmitters": self._get_dominant_neurotransmitters(neural_diagnostics),
            "active_regions": self._get_active_regions(neural_diagnostics),
            "mental_state_summary": self._summarize_mental_state(neural_diagnostics),
            "memory_efficiency": neural_diagnostics.get("memory_stats", {}).get("avg_consolidation", 0)
        }
    
    def _get_dominant_neurotransmitters(self, neural_diagnostics: Dict) -> List[str]:
        """Get the most active neurotransmitters"""
        neurotransmitters = neural_diagnostics.get("neurotransmitters", {})
        if not neurotransmitters:
            return []
        
        # Get top 2 neurotransmitters by level
        sorted_nt = sorted(neurotransmitters.items(), key=lambda x: x[1], reverse=True)
        return [nt[0] for nt in sorted_nt[:2] if nt[1] > 0.5]
    
    def _get_active_regions(self, neural_diagnostics: Dict) -> List[str]:
        """Get the most active brain regions"""
        regions = neural_diagnostics.get("neural_regions", {})
        if not regions:
            return []
        
        # Get regions with high activation
        active = [region for region, activation in regions.items() if activation > 0.6]
        return active[:3]  # Limit to top 3
    
    def _summarize_mental_state(self, neural_diagnostics: Dict) -> Dict[str, str]:
        """Summarize key mental state indicators"""
        mental_state = neural_diagnostics.get("mental_state", {})
        summary = {}
        
        # Categorize key states
        if mental_state.get("stress_level", 0) > 0.7:
            summary["stress"] = "high"
        elif mental_state.get("stress_level", 0) < 0.3:
            summary["stress"] = "low"
        else:
            summary["stress"] = "moderate"
        
        if mental_state.get("clarity", 1.0) > 1.2:
            summary["clarity"] = "enhanced"
        elif mental_state.get("clarity", 1.0) < 0.8:
            summary["clarity"] = "diminished"
        else:
            summary["clarity"] = "normal"
        
        if mental_state.get("creativity", 0.5) > 0.7:
            summary["creativity"] = "high"
        elif mental_state.get("creativity", 0.5) < 0.3:
            summary["creativity"] = "low"
        else:
            summary["creativity"] = "moderate"
        
        return summary
    
    def _analyze_memory_context(self, memories: List[Dict]) -> Dict[str, Any]:
        """Analyze overall memory context for reflection records"""
        if not memories:
            return {"memory_count": 0, "themes": [], "emotional_tone": "neutral"}
        
        # Count memory types and dimensions
        memory_types = defaultdict(int)
        dimensions = defaultdict(int)
        total_emotional_weight = 0
        motifs = []
        
        for memory in memories:
            if isinstance(memory, dict):
                memory_types[memory.get("memory_type", "episodic")] += 1
                dimensions[memory.get("dimension", "personal")] += 1
                total_emotional_weight += memory.get("emotional_weight", memory.get("vividness", 0.5))
                
                memory_motifs = memory.get("motifs", [])
                if isinstance(memory_motifs, list):
                    motifs.extend(memory_motifs)
                elif memory_motifs:
                    motifs.append(memory_motifs)
        
        avg_emotional_weight = total_emotional_weight / len(memories)
        dominant_motifs = [item[0] for item in Counter(motifs).most_common(5)]
        
        # Determine emotional tone
        if avg_emotional_weight > 0.7:
            emotional_tone = "intense"
        elif avg_emotional_weight < 0.4:
            emotional_tone = "subdued"
        else:
            emotional_tone = "balanced"
        
        return {
            "memory_count": len(memories),
            "memory_types": dict(memory_types),
            "dimensions": dict(dimensions),
            "dominant_motifs": dominant_motifs,
            "avg_emotional_weight": avg_emotional_weight,
            "emotional_tone": emotional_tone
        }

    def conduct_identity_transformation_cycle(self, entity: Dict[str, Any], brain=None) -> Dict[str, Any]:
        """
        Conduct a complete identity transformation cycle:
        1. Capture baseline identity
        2. Perform deep self-reflection
        3. Allow memory integration and neural processing
        4. Capture post-transformation identity
        5. Analyze and document changes
        """
        print(f"\n=== IDENTITY TRANSFORMATION CYCLE FOR {entity.get('name', 'UNKNOWN')} ===\n")
        
        # Phase 1: Baseline Identity Capture
        print("Phase 1: Capturing baseline identity...")
        baseline_snapshot = self.capture_identity_snapshot(entity, "pre_transformation")
        
        # Phase 2: Initial Self-Reflection
        print("Phase 2: Initial self-reflection...")
        initial_reflection = self.deep_self_reflection(entity, brain, 
                                                     custom_questions=["Who am I?", "What defines me?", "What is my essence?"])
          # Phase 3: Memory Integration (if memory module is available)
        print("Phase 3: Memory integration and neural processing...")
        if self.memory_module and brain:
            # Allow brain to process memories and update neural state
            if hasattr(brain, "process_memories"):
                brain.process_memories()  # No entity parameter needed
            # Apply memory-brain integration
            if hasattr(self.memory_module, "integrate_with_brain"):
                self.memory_module.integrate_with_brain(entity, brain)
            # Allow neural feedback to influence entity state
            if hasattr(brain, "brain_tick"):
                brain.brain_tick()
        
        # Phase 4: Post-Transformation Reflection
        print("Phase 4: Post-transformation self-reflection...")
        post_reflection = self.deep_self_reflection(entity, brain,
                                                  custom_questions=["Who have I become?", "How have I changed?", "What new truth do I carry?"])
        
        # Phase 5: Final Identity Capture
        print("Phase 5: Capturing transformed identity...")
        final_snapshot = self.capture_identity_snapshot(entity, "post_transformation")
        
        # Phase 6: Change Analysis
        print("Phase 6: Analyzing transformation...")
        transformation_analysis = self.analyze_identity_changes(baseline_snapshot, final_snapshot, 
                                                              initial_reflection, post_reflection)
        
        # Create complete transformation record
        transformation_record = {
            "entity_name": entity.get("name", "Unknown"),
            "timestamp": datetime.datetime.now().timestamp(),
            "baseline_snapshot": baseline_snapshot,
            "final_snapshot": final_snapshot,
            "initial_reflection": initial_reflection,
            "post_reflection": post_reflection,
            "transformation_analysis": transformation_analysis,
            "cycle_complete": True
        }
        
        # Store in reflection history
        self.reflection_history.append(transformation_record)
        
        print("=== TRANSFORMATION CYCLE COMPLETE ===\n")
        return transformation_record
    
    def analyze_identity_changes(self, baseline: Dict[str, Any], final: Dict[str, Any],
                               initial_reflection: Dict[str, Any], post_reflection: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze changes between baseline and final identity snapshots"""
        changes = {
            "psyche_changes": {},
            "motif_changes": {},
            "neural_changes": {},
            "memory_changes": {},
            "reflection_evolution": {},
            "significance": "minor",
            "transformation_themes": []
        }
        
        # Analyze psyche changes
        baseline_psyche = baseline.get("psyche", {})
        final_psyche = final.get("psyche", {})
        
        for axis in ["essence", "drive", "ideal", "shadow", "anima"]:
            baseline_value = baseline_psyche.get(axis, "Unknown")
            final_value = final_psyche.get(axis, "Unknown")
            if baseline_value != final_value:
                changes["psyche_changes"][axis] = {
                    "from": baseline_value,
                    "to": final_value,
                    "type": "shift"
                }
        
        # Analyze motif changes
        baseline_motifs = set(baseline.get("motif_distribution", {}).keys())
        final_motifs = set(final.get("motif_distribution", {}).keys())
        
        new_motifs = final_motifs - baseline_motifs
        lost_motifs = baseline_motifs - final_motifs
        
        if new_motifs or lost_motifs:
            changes["motif_changes"] = {
                "new_motifs": list(new_motifs),
                "lost_motifs": list(lost_motifs),
                "dominant_shift": baseline.get("dominant_motif") != final.get("dominant_motif")
            }
        
        # Analyze neural changes
        baseline_neural = baseline.get("neural_state", {})
        final_neural = final.get("neural_state", {})
        
        neural_deltas = {}
        for key in set(baseline_neural.keys()) | set(final_neural.keys()):
            baseline_val = baseline_neural.get(key, 0)
            final_val = final_neural.get(key, 0)
            if isinstance(baseline_val, (int, float)) and isinstance(final_val, (int, float)):
                delta = final_val - baseline_val
                if abs(delta) > 0.1:  # Significant change threshold
                    neural_deltas[key] = delta
        
        changes["neural_changes"] = neural_deltas
        
        # Analyze memory changes
        changes["memory_changes"] = {
            "memory_count_change": final.get("memory_count", 0) - baseline.get("memory_count", 0),
            "new_dimensions": self._identify_new_memory_dimensions(baseline, final)
        }
        
        # Analyze reflection evolution
        changes["reflection_evolution"] = self._analyze_reflection_evolution(initial_reflection, post_reflection)
        
        # Determine transformation significance
        significance_score = 0
        if changes["psyche_changes"]:
            significance_score += len(changes["psyche_changes"]) * 2
        if changes["motif_changes"].get("dominant_shift"):
            significance_score += 3
        if len(neural_deltas) > 2:
            significance_score += 2
        if changes["memory_changes"]["memory_count_change"] > 5:
            significance_score += 1
        
        if significance_score >= 5:
            changes["significance"] = "major"
        elif significance_score >= 3:
            changes["significance"] = "moderate"
        else:
            changes["significance"] = "minor"
        
        # Identify transformation themes
        changes["transformation_themes"] = self._identify_transformation_themes(changes)
        
        return changes
    
    def _identify_new_memory_dimensions(self, baseline: Dict, final: Dict) -> List[str]:
        """Identify new memory dimensions that appeared during transformation"""
        baseline_dims = set(baseline.get("motif_distribution", {}).keys())
        final_dims = set(final.get("motif_distribution", {}).keys())
        return list(final_dims - baseline_dims)
    
    def _analyze_reflection_evolution(self, initial: Dict, post: Dict) -> Dict[str, Any]:
        """Analyze how reflections evolved during transformation"""
        evolution = {
            "narrative_complexity_change": 0,
            "emotional_depth_change": 0,
            "self_awareness_change": 0,
            "key_insights": []
        }
        
        # Compare narrative complexity (rough measure: answer length and vocabulary)
        initial_answers = initial.get("reflections", {})
        post_answers = post.get("reflections", {})
        
        initial_complexity = sum(len(answer.get("answer", "")) for answer in initial_answers.values())
        post_complexity = sum(len(answer.get("answer", "")) for answer in post_answers.values())
        
        if post_complexity > 0 and initial_complexity > 0:
            evolution["narrative_complexity_change"] = (post_complexity - initial_complexity) / initial_complexity
        
        # Look for key insights in post-transformation reflections
        for question, reflection in post_answers.items():
            answer = reflection.get("answer", "")
            if any(insight in answer.lower() for insight in ["transformed", "became", "realized", "understand", "clarity"]):
                evolution["key_insights"].append({
                    "question": question,
                    "insight": answer[:100] + "..." if len(answer) > 100 else answer
                })
        
        return evolution
    
    def _identify_transformation_themes(self, changes: Dict[str, Any]) -> List[str]:
        """Identify major themes of the transformation"""
        themes = []
        
        # Psyche-based themes
        psyche_changes = changes.get("psyche_changes", {})
        if "shadow" in psyche_changes:
            if "corrupt" in str(psyche_changes["shadow"]).lower():
                themes.append("Descent into Shadow")
            elif "light" in str(psyche_changes["shadow"]).lower():
                themes.append("Shadow Integration")
        
        if "drive" in psyche_changes:
            themes.append("Fundamental Purpose Shift")
        
        if "essence" in psyche_changes:
            themes.append("Core Identity Transformation")
        
        # Motif-based themes
        motif_changes = changes.get("motif_changes", {})
        new_motifs = motif_changes.get("new_motifs", [])
        
        for motif in new_motifs:
            motif_lower = motif.lower()
            if "redemption" in motif_lower:
                themes.append("Redemptive Awakening")
            elif "power" in motif_lower:
                themes.append("Ascension to Power")
            elif "trauma" in motif_lower:
                themes.append("Traumatic Initiation")
            elif "divine" in motif_lower:
                themes.append("Divine Revelation")
        
        # Neural-based themes
        neural_changes = changes.get("neural_changes", {})
        if neural_changes.get("clarity", 0) > 0.3:
            themes.append("Cognitive Awakening")
        if neural_changes.get("creativity", 0) > 0.3:
            themes.append("Creative Renaissance")
        if neural_changes.get("stress_level", 0) > 0.3:
            themes.append("Trial by Fire")
        
        # Significance-based themes
        significance = changes.get("significance", "minor")
        if significance == "major":
            themes.append("Metamorphic Transformation")
        elif significance == "moderate":
            themes.append("Evolutionary Growth")
        
        return themes
    
    def get_transformation_summary(self, entity_name: str = None) -> Dict[str, Any]:
        """Get a summary of all transformations for an entity or all entities"""
        relevant_records = []
        
        if entity_name:
            relevant_records = [r for r in self.reflection_history 
                              if r.get("entity_name") == entity_name and r.get("cycle_complete", False)]
        else:
            relevant_records = [r for r in self.reflection_history 
                              if r.get("cycle_complete", False)]
        
        summary = {
            "total_transformations": len(relevant_records),
            "entities_transformed": len(set(r.get("entity_name") for r in relevant_records)),
            "transformation_themes": [],
            "significance_distribution": {"major": 0, "moderate": 0, "minor": 0},
            "most_recent": None
        }
        
        # Aggregate transformation themes
        all_themes = []
        for record in relevant_records:
            themes = record.get("transformation_analysis", {}).get("transformation_themes", [])
            all_themes.extend(themes)
            
            significance = record.get("transformation_analysis", {}).get("significance", "minor")
            summary["significance_distribution"][significance] += 1
        
        summary["transformation_themes"] = [item[0] for item in Counter(all_themes).most_common(10)]
        
        if relevant_records:
            summary["most_recent"] = max(relevant_records, key=lambda r: r.get("timestamp", 0))
        
        return summary

    def capture_identity_snapshot(self, entity: Dict[str, Any], label: str = "baseline") -> Dict[str, Any]:
        """Capture a snapshot of the entity's current identity state"""
        psyche = entity.get("psyche", {})
        memories = entity.get("memory", [])
        
        # Extract motifs from memories
        motifs = []
        for memory in memories:
            if isinstance(memory, dict):
                memory_motifs = memory.get("motifs", [])
                if isinstance(memory_motifs, list):
                    motifs.extend(memory_motifs)
                elif memory_motifs:
                    motifs.append(str(memory_motifs))
        
        motif_counts = Counter(motifs)
        dominant_motif = motif_counts.most_common(1)[0][0] if motif_counts else None
        
        # Get neural state if brain is available
        neural_state = {}
        if self.brain_system and hasattr(self.brain_system, "mental_state"):
            neural_state = dict(self.brain_system.mental_state)
        
        snapshot = {
            "timestamp": datetime.datetime.now().timestamp(),
            "label": label,
            "entity_name": entity.get("name", "Unknown"),
            "psyche": {
                "essence": psyche.get("essence", "Unknown"),
                "drive": psyche.get("drive", "Unknown"),
                "ideal": psyche.get("ideal", "Unknown"),
                "shadow": psyche.get("shadow", "Unknown"),
                "anima": psyche.get("anima", "Unknown")
            },
            "memory_count": len(memories),
            "dominant_motif": dominant_motif,
            "motif_distribution": dict(motif_counts),
            "neural_state": neural_state,
            "self_assessment": None  # Will be filled by self-reflection
        }
        
        self.identity_snapshots.append(snapshot)
        return snapshot
    
    def deep_self_reflection(self, entity: Dict[str, Any], brain=None, custom_questions: List[str] = None) -> Dict[str, Any]:
        """
        Conduct deep self-reflection session, asking core philosophical questions
        and generating narrative responses based on memories, psyche, and neural state.
        """
        if not brain:
            brain = self.brain_system
        
        questions = custom_questions or self.philosophical_questions
        reflections = {}
        
        # Use brain and memory integration
        psyche = entity.get("psyche", {})
        memories = self.memory_module.recall(entity) if self.memory_module else entity.get("memory", [])
        
        # Get neural diagnostics if brain is available
        neural_diagnostics = {}
        if brain and hasattr(brain, "get_brain_diagnostics"):
            neural_diagnostics = brain.get_brain_diagnostics()
        
        # Process each question with enhanced narrative synthesis
        for question in questions[:10]:  # Limit to avoid overwhelming
            reflection = self._synthesize_narrative_answer(
                entity, question, memories, psyche, neural_diagnostics, brain
            )
            reflections[question] = reflection
        
        # Record this reflection session
        reflection_session = {
            "timestamp": datetime.datetime.now().timestamp(),
            "entity_name": entity.get("name", "Unknown"),
            "questions_asked": len(reflections),
            "reflections": reflections,
            "neural_state_summary": self._summarize_neural_state(neural_diagnostics),
            "memory_context": self._analyze_memory_context(memories)
        }
        
        self.reflection_history.append(reflection_session)
        return reflection_session
    
    def _synthesize_narrative_answer(self, entity: Dict[str, Any], question: str, 
                                   memories: List[Dict], psyche: Dict[str, Any], 
                                   neural_diagnostics: Dict, brain=None) -> Dict[str, Any]:
        """
        Synthesize a deep, contextual narrative answer to a philosophical question
        """
        # Analyze memory dimensions and motifs
        memory_analysis = self._analyze_memories_for_question(memories, question)
        
        # Get brain-specific insights
        neural_insights = self._extract_neural_insights(neural_diagnostics, question)
        
        # Build contextual narrative elements
        narrative_elements = self._build_narrative_elements(
            entity, psyche, memory_analysis, neural_insights
        )
        
        # Select appropriate template and style
        template_category = self._categorize_question(question)
        style_modifiers = self._determine_narrative_style(
            psyche, memory_analysis, neural_insights
        )
        
        # Generate the core answer
        core_answer = self._generate_core_answer(
            question, narrative_elements, template_category, style_modifiers
        )
        
        # Add dimensional memory context if relevant
        dimensional_context = self._add_dimensional_context(
            question, memories, brain
        )
        
        # Combine all elements into final narrative
        final_answer = self._weave_final_narrative(
            core_answer, dimensional_context, style_modifiers
        )
        
        # Create feedback for brain/memory systems
        narrative_feedback = self._generate_narrative_feedback(
            final_answer, memory_analysis, neural_insights
        )
        
        return {
            "question": question,
            "answer": final_answer,
            "narrative_elements": narrative_elements,
            "memory_analysis": memory_analysis,
            "neural_insights": neural_insights,
            "style_modifiers": style_modifiers,
            "dimensional_context": dimensional_context,
            "feedback": narrative_feedback,
            "timestamp": datetime.datetime.now().timestamp()
        }
    
    def _categorize_question(self, question: str) -> str:
        """Categorize the philosophical question to select appropriate templates"""
        question_lower = question.lower()
        
        if any(word in question_lower for word in ["who am i", "self", "identity", "essence"]):
            return "identity_formation"
        elif any(word in question_lower for word in ["memory", "remember", "past", "experience"]):
            return "memory_reflection"
        elif any(word in question_lower for word in ["change", "become", "transform", "evolve"]):
            return "change_recognition"
        elif any(word in question_lower for word in ["divine", "destiny", "prophecy", "cosmic", "eternal"]):
            return "mythic_depth"
        else:
            return "identity_formation"  # Default
    
    def _determine_narrative_style(self, psyche: Dict[str, Any], memory_analysis: Dict, 
                                 neural_insights: Dict) -> Dict[str, Any]:
        """Determine narrative style modifiers based on entity state"""
        style = {
            "tone": "neutral",
            "depth": "medium",
            "mysticism": "low",
            "technology": "low",
            "emotion": "medium",
            "complexity": "medium"
        }
        
        # Analyze psyche for style
        shadow = psyche.get("shadow", "").lower()
        anima = psyche.get("anima", "").lower()
        drive = psyche.get("drive", "").lower()
        
        if "corrupt" in shadow or "dark" in shadow:
            style["tone"] = "cynical"
            style["emotion"] = "high"
        elif "divine" in anima or "light" in anima:
            style["tone"] = "transcendent"
            style["mysticism"] = "high"
        
        if "ascend" in drive or "transcend" in drive:
            style["depth"] = "deep"
            style["mysticism"] = "high"
        elif "disrupt" in drive or "rebel" in drive:
            style["technology"] = "high"
            style["complexity"] = "high"
        
        # Analyze dominant motifs for style
        dominant_motifs = memory_analysis.get("dominant_motifs", [])
        for motif in dominant_motifs:
            motif_lower = motif.lower()
            if "trauma" in motif_lower or "pain" in motif_lower:
                style["emotion"] = "high"
                style["tone"] = "somber"
            elif "miracle" in motif_lower or "divine" in motif_lower:
                style["mysticism"] = "high"
                style["tone"] = "reverent"
            elif "victory" in motif_lower or "triumph" in motif_lower:
                style["tone"] = "triumphant"
                style["emotion"] = "high"
        
        # Analyze neural state for style
        if neural_insights.get("available", False):
            neural_factors = neural_insights.get("neural_factors", {})
            if neural_factors.get("creativity", 0) > 0.7:
                style["complexity"] = "high"
                style["mysticism"] = "medium"
            if neural_factors.get("stress_level", 0) > 0.7:
                style["emotion"] = "high"
                style["tone"] = "intense"
        
        return style
    
    def _analyze_memories_for_question(self, memories: List[Dict], question: str) -> Dict[str, Any]:
        """Analyze memories for relevance to a specific question"""
        analysis = {
            "relevant_memories": [],
            "dominant_motifs": [],
            "memory_themes": [],
            "emotional_weight": 0.0,
            "temporal_distribution": {},
            "memory_types": {},
            "most_significant_memory": None
        }
        
        if not memories:
            return analysis
        
        # Process each memory
        relevant_memories = []
        for memory in memories:
            if isinstance(memory, dict):
                content = memory.get("content", "")
                relevance = self._calculate_relevance(question, content)
                
                if relevance > 0.2:  # Threshold for relevance
                    relevant_memories.append({
                        "memory": memory,
                        "relevance": relevance,
                        "content": content
                    })
                
                # Extract motifs
                motifs = memory.get("motifs", [])
                if isinstance(motifs, list):
                    analysis["dominant_motifs"].extend(motifs)
                elif motifs:
                    analysis["dominant_motifs"].append(str(motifs))
                
                # Extract themes
                memory_type = memory.get("memory_type", "personal")
                analysis["memory_types"][memory_type] = analysis["memory_types"].get(memory_type, 0) + 1
                
                # Emotional analysis
                emotional_weight = memory.get("emotional_weight", memory.get("vividness", 0.0))
                if isinstance(emotional_weight, (int, float)):
                    analysis["emotional_weight"] += emotional_weight
        
        analysis["relevant_memories"] = relevant_memories
        
        # Find most significant memory
        if relevant_memories:
            analysis["most_significant_memory"] = max(relevant_memories, key=lambda x: x["relevance"])
        
        # Process dominant motifs
        from collections import Counter
        motif_counter = Counter(analysis["dominant_motifs"])
        analysis["dominant_motifs"] = [motif for motif, count in motif_counter.most_common(5)]
        
        # Extract themes from motifs
        analysis["memory_themes"] = [motif for motif in analysis["dominant_motifs"] 
                                   if any(theme in motif.lower() for theme in 
                                         ["love", "war", "death", "birth", "victory", "loss", "divine", "power"])]
        
        # Normalize emotional weight
        if len(memories) > 0:
            analysis["emotional_weight"] = analysis["emotional_weight"] / len(memories)
        
        return analysis
    
    def _calculate_relevance(self, question: str, content: str) -> float:
        """Calculate how relevant a memory is to a given question"""
        if not question or not content:
            return 0.0
            
        question_words = set(question.lower().split())
        content_words = set(content.lower().split())
        
        # Simple word overlap score
        overlap = len(question_words.intersection(content_words))
        max_words = max(len(question_words), len(content_words))
        
        return overlap / max_words if max_words > 0 else 0.0
    
    def _extract_neural_insights(self, neural_diagnostics: Dict, question: str) -> Dict[str, Any]:
        """Extract neural insights relevant to the question"""
        insights = {
            "available": bool(neural_diagnostics),
            "neural_factors": {},
            "brain_regions": [],
            "neurotransmitters": [],
            "cognitive_state": "unknown"
        }
        
        if not neural_diagnostics:
            return insights
        
        # Extract neural factors
        mental_state = neural_diagnostics.get("mental_state", {})
        if mental_state:
            insights["neural_factors"] = {
                "creativity": mental_state.get("creativity", 0.5),
                "focus": mental_state.get("focus", 0.5),
                "stress_level": mental_state.get("stress_level", 0.5),
                "emotional_intensity": mental_state.get("emotional_intensity", 0.5),
                "clarity": mental_state.get("clarity", 1.0)
            }
        
        # Extract active brain regions
        active_regions = neural_diagnostics.get("active_regions", [])
        insights["brain_regions"] = active_regions
        
        # Extract dominant neurotransmitters
        neurotransmitters = neural_diagnostics.get("dominant_neurotransmitters", [])
        insights["neurotransmitters"] = neurotransmitters
        
        # Determine cognitive state based on neural factors
        neural_factors = insights["neural_factors"]
        if neural_factors.get("stress_level", 0) > 0.7:
            insights["cognitive_state"] = "stressed"
        elif neural_factors.get("creativity", 0) > 0.7:
            insights["cognitive_state"] = "creative"
        elif neural_factors.get("focus", 0) > 0.7:
            insights["cognitive_state"] = "focused"
        elif neural_factors.get("clarity", 1.0) > 1.2:
            insights["cognitive_state"] = "enhanced"
        else:
            insights["cognitive_state"] = "balanced"
        
        return insights
    
    def _build_narrative_elements(self, entity: Dict[str, Any], psyche: Dict[str, Any], 
                                memory_analysis: Dict, neural_insights: Dict) -> Dict[str, Any]:
        """Build comprehensive narrative elements from all sources"""
        elements = {
            # Core identity elements from psyche
            "essence": psyche.get("essence", "undefined"),
            "drive": psyche.get("drive", "seeking purpose"),
            "ideal": psyche.get("ideal", "unknown ideal"),
            "shadow": psyche.get("shadow", "hidden darkness"),
            "anima": psyche.get("anima", "inner light"),
            
            # Memory-derived elements
            "dominant_motifs": memory_analysis.get("dominant_motifs", []),
            "memory_themes": memory_analysis.get("memory_themes", []),
            "emotional_weight": memory_analysis.get("emotional_weight", 0.0),
            "relevant_memories": memory_analysis.get("relevant_memories", []),
            
            # Neural elements
            "neural_state": neural_insights.get("brain_regions", []),
            "cognitive_state": neural_insights.get("cognitive_state", "unknown"),
            "neurotransmitters": neural_insights.get("neurotransmitters", []),
            
            # Entity-specific elements
            "archetype": entity.get("archetype", "undefined"),
            "lineage": entity.get("lineage", ["unknown ancestry"]),
            "name": entity.get("name", "Unknown"),
            "role": entity.get("role", "unknown"),
            "status": entity.get("status", "unknown")
        }
        
        # Add neural factors if available
        if neural_insights.get("available"):
            neural_factors = neural_insights.get("neural_factors", {})
            elements.update({
                "creativity": neural_factors.get("creativity", 0.5),
                "focus": neural_factors.get("focus", 0.5),
                "stress": neural_factors.get("stress_level", 0.5),
                "clarity": neural_factors.get("clarity", 1.0),
                "emotional_intensity": neural_factors.get("emotional_intensity", 0.5)
            })
        
        return elements
    
    def _generate_core_answer(self, question: str, narrative_elements: Dict, 
                            template_category: str, style_modifiers: Dict) -> str:
        """Generate the core narrative answer"""
        # Get appropriate templates
        templates = self.narrative_templates.get(template_category, 
                                                self.narrative_templates["identity_formation"])
        
        # Select template based on style
        base_template = random.choice(templates)
        
        # Fill in narrative elements
        filled_template = self._fill_template(base_template, narrative_elements)
        
        # Apply style modifiers
        styled_answer = self._apply_style_modifiers(filled_template, style_modifiers, narrative_elements)
        
        return styled_answer


# Standalone function that works with the NarrativeEngine
def ask_and_answer(entity: Dict[str, Any], question: str, brain_system=None, 
                   memory_module=None, narrative_engine=None) -> Dict[str, Any]:
    """
    Standalone function for asking a question and getting a narrative response.
    Can be called independently or integrated with existing systems.
    
    Args:
        entity: The entity being questioned
        question: The philosophical question to ask
        brain_system: Optional brain system for neural insights
        memory_module: Optional memory module for memory analysis
        narrative_engine: Optional existing narrative engine instance
    
    Returns:
        Complete response with answer and analysis
    """
    # Create or use existing narrative engine
    if narrative_engine is None:
        narrative_engine = NarrativeEngine(brain_system, memory_module)
    
    # Conduct reflection with the single question
    reflection_result = narrative_engine.deep_self_reflection(
        entity, brain_system, custom_questions=[question]
    )
    
    # Extract the answer for the specific question
    answer_data = reflection_result.get("reflections", {}).get(question, {})
    
    # Enhanced response format
    response = {
        "entity_name": entity.get("name", "Unknown"),
        "question": question,
        "answer": answer_data.get("answer", "I cannot find words for this truth."),
        "narrative_elements": answer_data.get("narrative_elements", {}),
        "memory_analysis": answer_data.get("memory_analysis", {}),
        "neural_insights": answer_data.get("neural_insights", {}),
        "style_modifiers": answer_data.get("style_modifiers", {}),
        "dimensional_context": answer_data.get("dimensional_context", {}),
        "feedback": answer_data.get("feedback", {}),
        "timestamp": answer_data.get("timestamp", datetime.datetime.now().timestamp()),
        "reflection_session": reflection_result
    }
    
    return response