# Cyberdynasty Entity Structure Analysis

## Complete Entity Data Model

Based on analysis of CipherKing and IronSovereign, each entity has the following structure:

### File Structure per Entity State
```
{EntityName}/
├── states/
    ├── ascendant/
    │   ├── {entityname}.yaml           # Master entity file
    │   ├── {entityname}.md             # Narrative documentation
    │   ├── traits_{entityname}.yaml    # Just traits section
    │   ├── psyche_{entityname}.yaml    # Just psyche section
    │   └── persona_{entityname}.yaml   # Narrative templates
    ├── exiled/
    └── rising/
```

### Master YAML Structure
```yaml
name: String                 # Display name
archetype: String            # The Ascendant, The Returned, etc.
hybrid: String               # Cybernetic, Digital, etc.
subtype: String              # CipherKing, IronSovereign, etc.
state: String                # ascendant, exiled, rising
epoch: String                # Code Wars, Iron Renaissance, etc.
location: String             # The Neon Throne, The Reforged Citadel
role: String                 # Supreme Ruler, etc.
status: String               # Current status description

traits:                      # 40+ personality/skill traits
  willpower: String
  intellect: String
  charisma: String
  # ... (extensive trait list)
  obsession: String
  weakness: String

psyche:                      # Jungian psychology framework
  essence: String            # Core identity
  drive: String              # Primal motivation
  ideal: String              # Guiding principle
  shadow: String             # Hidden flaw
  anima: String              # Balancing force
  focus: String              # present/past/future
  clarity: Float             # 0-1+ mental clarity
  trauma: Float              # 0-1 trauma level
  obsession: String          # Current obsession
  ruminator: Boolean         # Tendency to dwell
  motifs: [String]           # 10+ thematic elements
  memories: [Object]         # Structured memory objects

memories:                    # Memory system
  - event: String            # What happened
    vividness: Float         # 0-1 clarity
    timestamp: ISO8601       # When it occurred
    tags: [String]           # Classification tags

deeds:                       # Achievement system
  - description: String      # What was accomplished
    timestamp: ISO8601       # When
    memory_linked: Boolean   # Links to memories

relationships:               # Social network
  - type: String             # lieutenant, rival, etc.
    target: String           # Who
    since: ISO8601           # Relationship start

memory_narrative: String     # Overall memory theme
prophecy: String             # Future prediction

memory_traits:               # Memory system parameters
  decay_rate: Float
  vividness_range: [Float, Float]
  ruminator_chance: Float
  forgetter_chance: Float
  memory_influence: Float
  obsession_chance: Float
  clarity_base: Float
  trauma_base: Float
  memory_focus: [String]
```

### Traits File Structure
- Extracted traits section only
- 40+ attributes covering personality, skills, style
- Signature moves and weaknesses included

### Psyche File Structure
- Core Jungian psychology framework
- Motifs and thematic elements
- Memory snippets as narrative quotes
- Focus and trauma metrics

### Persona File Structure
- Archetype classification
- 40+ narrative templates
- Action/achievement patterns
- Storytelling elements

## Dynasty Hierarchy Analysis

### Current Structure
```
cyberdynasties/
├── angelic/the_seraphic_concord/
├── cybernetic/the_chrome_mandarins/
├── cosmic/the_celestial_synod/
├── demonic/the_infernal_dynasty/
├── digital/the_quantum_chorus/
└── humanoid/the_neural_collective/

Each dynasty contains:
├── bosses/
│   ├── maximumboss/              # 1 per dynasty
│   └── regularbosses/            # 3-10 per dynasty
└── enforcers/                    # 8-12 per dynasty
```

### Rank Structure
1. **Maximum Boss** - Supreme leader (1 per dynasty)
2. **Regular Bosses** - Senior leadership (3-10 per dynasty) 
3. **Enforcers** - Elite operatives (8-12 per dynasty)
4. **Soldiers** - General population (universal pool)

### States System
All ranks support three states:
- **ascendant**: In power/rising
- **exiled**: Fallen from grace
- **rising**: Returning to power

## Universal Soldiers Pool Design

### Proposed Location
```
cyberdynasties/
├── _universal_soldiers/          # Cross-dynasty recruitment pool
│   ├── by_dynasty/              # Organized by current allegiance
│   │   ├── angelic/
│   │   ├── cybernetic/
│   │   ├── cosmic/
│   │   ├── demonic/
│   │   ├── digital/
│   │   ├── humanoid/
│   │   └── unaligned/           # Freelancers
│   ├── by_specialization/       # Organized by skill
│   │   ├── hackers/
│   │   ├── warriors/
│   │   ├── diplomats/
│   │   ├── infiltrators/
│   │   └── technicians/
│   └── recruitment_templates/    # Templates for new soldiers
└── [existing dynasty folders]
```

### Soldier Data Model
Simplified version of full entity model:
- Basic traits (10-15 key attributes)
- Simple psyche (essence, drive, focus)
- Recruitment history
- Current assignment/allegiance
- Promotion potential

### Mobility System
- Soldiers can be recruited between dynasties
- Promotion paths: soldier → enforcer → boss → maximumboss
- State transitions between ascendant/exiled/rising
- Cross-dynasty transfers based on politics/war

## Implementation Strategy

### Phase 1: Finalize Structure (Current)
- ✅ Analyze entity data model
- ✅ Design universal soldiers pool
- 🔄 Create soldier templates and recruitment system

### Phase 2: Population Generation
- Generate full entity files for all existing bosses/enforcers
- Create soldier population (100-500 entities)
- Implement recruitment/assignment logic

### Phase 3: Dynamic Systems
- State transition mechanics
- Cross-dynasty politics
- Promotion/demotion flows
- War/alliance systems

## Key Design Principles

1. **Scalability**: System supports massive entity populations
2. **Modularity**: Components can be generated independently
3. **Narrative Depth**: Rich psychological and social modeling
4. **Dynamic Evolution**: Entities change state and allegiance
5. **Cross-Dynasty Interaction**: Universal recruitment and politics
6. **Hierarchical Organization**: Clear rank and command structure

## Next Steps

1. Implement universal soldiers pool structure
2. Create soldier entity templates
3. Build recruitment/assignment system
4. Generate initial soldier population
5. Implement state transition mechanics
