"""
Street Level Systems Demo for Cyber Dynasties
=============================================

This script demonstrates how the street-level entity framework integrates
with character systems and simulation engines to create dynamic, emergent
storylines and interactions.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
import random
from datetime import datetime, timedelta

# Import our street-level systems
from street_level_entities import DynastyType, CharacterInteractionSystem
from street_level_data_loader import StreetLevelDataLoader, DynastyEntityFactory
from street_level_simulation import StreetLevelSimulation, CharacterStoryIntegration

def demo_entity_creation():
    """Demonstrate creating entities from data files"""
    print("=== ENTITY CREATION DEMO ===")
    
    # Initialize the data loader with the Cyber Dynasties root path
    data_loader = StreetLevelDataLoader("c:/Users/storage/Cyber Dynasties")
    
    # Create entity factory
    factory = DynastyEntityFactory(data_loader)
    
    # Load Neural Collective data
    print("Loading Neural Collective data...")
    dynasty_data = data_loader.load_dynasty_data(DynastyType.NEURAL_COLLECTIVE)
    
    print(f"Loaded {len(dynasty_data['criminal_syndicates'])} criminal syndicate templates")
    print(f"Loaded {len(dynasty_data['street_gangs'])} street gang templates")
    print(f"Loaded {len(dynasty_data['law_enforcement'])} law enforcement templates")
    print(f"Loaded {len(dynasty_data['territories'])} territories")
    print(f"Loaded {len(dynasty_data['employment_networks'])} employment networks")
    
    # Create entities from templates
    print("\nCreating entities from templates...")
    
    # Create the Consciousness Cartel
    cartel = factory.create_criminal_syndicate(DynastyType.NEURAL_COLLECTIVE, "The Consciousness Cartel")
    print(f"Created criminal syndicate: {cartel.name}")
    print(f"  - Primary activities: {cartel.primary_activities}")
    print(f"  - Violence level: {cartel.violence_level}")
    print(f"  - Membership: {cartel.membership_size}")
    
    # Create law enforcement
    law_unit = factory.create_law_enforcement_unit(DynastyType.NEURAL_COLLECTIVE, "Synapse Security Division")
    print(f"\nCreated law enforcement: {law_unit.name}")
    print(f"  - Enforcement style: {law_unit.enforcement_style}")
    print(f"  - Budget level: {law_unit.budget_level}")
    print(f"  - Public trust: {law_unit.public_trust}")
    
    # Create social class templates
    from street_level_entities import SocialClass
    executive_template = factory.create_social_class_template(DynastyType.NEURAL_COLLECTIVE, SocialClass.EXECUTIVE)
    print(f"\nCreated social class template: {executive_template.class_name.value}")
    print(f"  - Income range: {executive_template.income_range}")
    print(f"  - Enhancement access: {executive_template.enhancement_access}")
    
    return data_loader, factory

def demo_simulation_integration():
    """Demonstrate the simulation system in action"""
    print("\n=== SIMULATION INTEGRATION DEMO ===")
    
    # Initialize simulation
    data_loader = StreetLevelDataLoader("c:/Users/storage/Cyber Dynasties")
    simulation = StreetLevelSimulation(data_loader)
    
    # Initialize Neural Collective
    print("Initializing Neural Collective simulation...")
    simulation.initialize_dynasty(DynastyType.NEURAL_COLLECTIVE, territory_count=3)
    
    print(f"Created {len(simulation.entities)} entities")
    print(f"Created {len(simulation.territories)} territories")
    
    # List created entities
    print("\nCreated entities:")
    for entity_id, entity in simulation.entities.items():
        print(f"  - {entity.name} ({entity.organization_type.value}) in {len(entity.territories)} territories")
    
    # Run simulation for 24 hours
    print("\nRunning simulation for 24 hours...")
    simulation.advance_simulation(hours=24)
    
    print(f"Generated {len(simulation.events)} events")
    print(f"Active storylines: {len(simulation.active_storylines)}")
    
    # Show recent events
    if simulation.events:
        print("\nRecent events:")
        for event in simulation.events[-5:]:  # Last 5 events
            print(f"  - {event.description} (Severity: {event.severity})")
    
    # Show active storylines
    if simulation.active_storylines:
        print("\nActive storylines:")
        for storyline_id, storyline in simulation.active_storylines.items():
            print(f"  - {storyline['type']} involving {len(storyline.get('participants', []))} entities")
    
    return simulation

def demo_character_integration():
    """Demonstrate character interaction with street-level systems"""
    print("\n=== CHARACTER INTEGRATION DEMO ===")
    
    # Create simulation
    data_loader = StreetLevelDataLoader("c:/Users/storage/Cyber Dynasties")
    simulation = StreetLevelSimulation(data_loader)
    simulation.initialize_dynasty(DynastyType.NEURAL_COLLECTIVE, territory_count=3)
    
    # Create character integration system
    char_integration = CharacterStoryIntegration(simulation)
    
    # Create a sample character
    character_id = "demo_character_001"
    character_profile = {
        "name": "Alex Neural",
        "level": 2,
        "skills": ["technology", "social", "investigation"],
        "morality": 65,
        "enhancement_status": "enhanced",
        "social_class": "professional",
        "current_territory": list(simulation.territories.keys())[0],
        "reputation": {},
        "background": "former_neural_technician"
    }
    
    # Register character
    print(f"Registering character: {character_profile['name']}")
    char_integration.register_character(character_id, character_profile['current_territory'])
    
    # Get available opportunities
    print("\nGetting character opportunities...")
    opportunities = char_integration.get_character_opportunities(character_id, character_profile)
    
    print("Available opportunities:")
    for category, ops in opportunities.items():
        if ops:
            print(f"  {category.title()}:")
            for op in ops[:3]:  # Show first 3 opportunities
                if isinstance(op, dict):
                    print(f"    - {op.get('type', op.get('position', 'Unknown'))}")
                else:
                    print(f"    - {op}")
    
    # Simulate character action
    print("\nSimulating character action...")
    target_entity = list(simulation.entities.values())[0]
    
    action_result = char_integration.process_character_action(
        character_id=character_id,
        action_type="help",
        target_entity_id=target_entity.entity_id,
        success=True,
        consequences={"civilians_helped": True, "violence_used": False}
    )
    
    print(f"Action result:")
    print(f"  - Reputation change: {action_result['reputation_change']}")
    print(f"  - New reputation: {action_result['new_reputation']}")
    print(f"  - Story consequences: {len(action_result['story_consequences'])}")
    print(f"  - New storylines: {len(action_result['new_storylines'])}")
    
    # Show character reputation summary
    print("\nCharacter reputation summary:")
    rep_summary = char_integration.get_character_reputation_summary(character_id)
    for entity_id, rep_info in rep_summary.items():
        print(f"  - {rep_info['entity_name']}: {rep_info['reputation']} ({rep_info['standing']})")
    
    return char_integration

def demo_procedural_generation():
    """Demonstrate procedural story and mission generation"""
    print("\n=== PROCEDURAL GENERATION DEMO ===")
    
    # Create systems
    data_loader = StreetLevelDataLoader("c:/Users/storage/Cyber Dynasties")
    simulation = StreetLevelSimulation(data_loader)
    simulation.initialize_dynasty(DynastyType.NEURAL_COLLECTIVE, territory_count=4)
    
    # Run simulation to generate some events and storylines
    simulation.advance_simulation(hours=48)
    
    # Find a criminal organization
    from street_level_entities import OrganizationType
    criminal_orgs = [e for e in simulation.entities.values() 
                    if e.organization_type == OrganizationType.CRIMINAL_SYNDICATE or 
                       e.organization_type == OrganizationType.GANG]
    
    if criminal_orgs:
        criminal_org = criminal_orgs[0]
        print(f"Generating missions for {criminal_org.name}...")
        
        # Generate missions for different character levels
        for level in range(1, 6):
            if hasattr(criminal_org, 'generate_mission_for_character'):
                mission = criminal_org.generate_mission_for_character(level)
                print(f"  Level {level}: {mission['type']} (Reward: {mission['reward_resources']} credits)")
    
    # Show how territories change over time
    print("\nTerritory state changes:")
    for territory_id, territory_state in simulation.territories.items():
        print(f"  {territory_state.territory.name}:")
        print(f"    - Crime level: {territory_state.current_crime_level}")
        print(f"    - Law presence: {territory_state.current_law_presence}")
        print(f"    - Recent events: {len(territory_state.recent_events)}")
    
    # Show storyline detection
    if simulation.active_storylines:
        print("\nDetected storyline patterns:")
        for storyline_id, storyline in simulation.active_storylines.items():
            print(f"  {storyline['type']}:")
            print(f"    - Participants: {storyline.get('participants', [])}")
            print(f"    - Potential outcomes: {storyline.get('potential_outcomes', [])}")

def demo_data_export():
    """Demonstrate exporting entity data"""
    print("\n=== DATA EXPORT DEMO ===")
    
    # Create a sample entity
    data_loader = StreetLevelDataLoader("c:/Users/storage/Cyber Dynasties")
    factory = DynastyEntityFactory(data_loader)
    
    # Create an entity
    entity = factory.create_criminal_syndicate(DynastyType.NEURAL_COLLECTIVE)
    
    # Export to JSON
    output_file = "demo_entity_export.json"
    from street_level_data_loader import export_entity_to_json
    export_entity_to_json(entity, output_file)
    
    print(f"Exported entity to {output_file}")
    
    # Show the exported data
    with open(output_file, 'r') as f:
        exported_data = json.load(f)
    
    print("Exported entity structure:")
    for key, value in exported_data.items():
        if isinstance(value, (list, dict)):
            print(f"  {key}: {type(value).__name__} with {len(value)} items")
        else:
            print(f"  {key}: {value}")
    
    # Clean up
    os.remove(output_file)

def main():
    """Run all demonstrations"""
    print("CYBER DYNASTIES STREET-LEVEL SYSTEMS DEMONSTRATION")
    print("=" * 60)
    
    try:
        # Run all demos
        demo_entity_creation()
        demo_simulation_integration()
        demo_character_integration()
        demo_procedural_generation()
        demo_data_export()
        
        print("\n" + "=" * 60)
        print("DEMONSTRATION COMPLETE")
        print("\nThe street-level systems are now ready for integration with:")
        print("- Character creation and progression systems")
        print("- Narrative generation engines")
        print("- Game mechanics and simulation loops")
        print("- AI-driven story content")
        print("- Player choice and consequence systems")
        
    except Exception as e:
        print(f"\nError during demonstration: {e}")
        print("This may be due to missing data files or import issues.")
        print("Ensure all Python files are in the same directory.")

if __name__ == "__main__":
    main()
