# Persona System Design

## Overview

The `persona` field represents the **subjective self-image, narrative role, and archetypal patterns** that an entity identifies with or projects to the world. This is distinct from objective `traits` (what the entity is) and `psyche` (the entity’s inner drives and fears). The `persona` system enables richer, more nuanced simulation and storytelling by modeling how an entity sees itself and wishes to be seen.

---

## Key Concepts

- **Traits:** Objective stats, abilities, and facts about the entity (e.g., strength, intellect, lineage).
- **Psyche:** Inner drives, fears, ideals, and psychological axes.
- **Persona:** Subjective self-image, narrative roles, or archetypes (e.g., “The Redeemer,” “The Exile,” “The Trickster”). Defines how the entity interprets its memories, expresses itself, and interacts with the world.

---

## Why Use Persona?

- **Psychological Depth:** Entities can act or react based on their self-image, not just raw stats.
- **Narrative Flexibility:** Entities can adopt different personas in different contexts or stories.
- **Emergent Behavior:** Conflicts between traits and persona can drive drama, transformation, or mythic arcs.
- **Separation of Concerns:** Clear distinction between what an entity is (`traits`) and what it thinks or presents (`persona`).

---

## Data Structure Example

```yaml
name: Cipher King
traits:                # Objective reality
  strength: 8
  intelligence: 10
  origin: Cyber Dynasty
psyche:                # Drives, fears, ideals
  drive: ascendancy
  shadow: isolation
persona:               # Subjective self-image/archetype
  archetype: The Exile
  motifs:
    - redemption
    - rebellion
  narrative_templates:
    - "Rose from the ashes of defeat."
    - "Guided the lost through the digital abyss."
memories:
  - timestamp: 2205-02-20T00:00:00Z
    vividness: 0.52
    text: Crushed the Protocol Rebellion
    motif: victory
```

---

## Implementation Guidelines

1. **Data Files**
    - Rename all `memory_templates` fields in YAML/JSON to `persona`.
    - Store persona data in its own section, separate from `traits` and `psyche`.

2. **Loader Code**
    - Update entity loader to merge `persona` from relevant files.
    - Ensure `persona` is a distinct field in the entity dictionary.

3. **Module Integration**
    - Update all modules (`memorymodule.py`, `bookkeeper.py`, `narrative_engine.py`, etc.) to use `persona` instead of `memory_templates`.
    - Use `persona` for narrative generation, memory interpretation, and self-reflection logic.

4. **Testing**
    - Test that entities load with correct `persona` data.
    - Verify that narrative and simulation modules use `persona` as intended.

5. **Documentation**
    - Maintain this file as the single source of truth for the persona system.
    - Document any changes or extensions to persona logic here.

---

## Example Use Cases

- **Story Generation:** The bookkeeper uses `persona` to select narrative templates and motifs for the entity’s story.
- **Behavior Simulation:** The brain module references `persona` to determine how the entity interprets events or memories.
- **Dynamic Persona:** Entities can change persona over time, reflecting growth, trauma, or transformation.

---

## Future Extensions

- **Multiple Personas:** Support for entities with layered or conflicting personas.
- **Persona Evolution:** Systems for persona change based on experiences or external influence.
- **Persona-Driven Mutation:** Use persona as a driver for procedural generation and mutation.

---

**This system enables a clear, robust separation between what an entity is and what it believes or presents itself to be, supporting richer simulation and mythic storytelling.**