"""
Street Level Data Loader for Cyber Dynasties
============================================

This module loads and manages dynasty-specific street-level entity data,
providing templates and procedural generation rules for each dynasty's
unique flavor and characteristics.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import asdict

from street_level_entities import (
    DynastyType, OrganizationType, SocialClass, ViolenceLevel, LawEnforcementStyle,
    CriminalSyndicate, StreetGang, LawEnforcementUnit, Corporation,
    SocialClassTemplate, EmploymentNetwork, Territory
)

class StreetLevelDataLoader:
    """Loads and manages all street-level entity data"""
    
    def __init__(self, data_root: str = ""):
        self.data_root = Path(data_root) if data_root else Path(".")
        self.dynasty_data: Dict[DynastyType, Dict[str, Any]] = {}
        self.entity_templates: Dict[str, Dict[str, Any]] = {}
        self.loaded_dynasties: set = set()
    
    def load_dynasty_data(self, dynasty: DynastyType) -> Dict[str, Any]:
        """Load all street-level data for a specific dynasty"""
        if dynasty in self.loaded_dynasties:
            return self.dynasty_data[dynasty]
        
        dynasty_path = self._get_dynasty_path(dynasty)
        
        data = {
            "criminal_syndicates": self._load_criminal_syndicates(dynasty_path),
            "street_gangs": self._load_street_gangs(dynasty_path),
            "law_enforcement": self._load_law_enforcement(dynasty_path),
            "corporations": self._load_corporations(dynasty_path),
            "social_classes": self._load_social_classes(dynasty_path),
            "employment_networks": self._load_employment_networks(dynasty_path),
            "territories": self._load_territories(dynasty_path),
            "procedural_rules": self._load_procedural_rules(dynasty_path)
        }
        
        self.dynasty_data[dynasty] = data
        self.loaded_dynasties.add(dynasty)
        
        return data
    
    def _get_dynasty_path(self, dynasty: DynastyType) -> Path:
        """Get the file system path for a dynasty's data"""
        dynasty_folders = {
            DynastyType.NEURAL_COLLECTIVE: "humanoid/the_neural_collective",
            DynastyType.SERAPHIC_CONCORD: "angelic/the_seraphic_concord",
            DynastyType.CELESTIAL_SYNOD: "cosmic/the_celestial_synod",
            DynastyType.CHROME_MANDARINS: "cybernetic/the_chrome_mandarins",
            DynastyType.QUANTUM_CHORUS: "digital/the_quantum_chorus",
            DynastyType.INFERNAL_DYNASTY: "demonic/the_infernal_dynasty"
        }
        
        return self.data_root / dynasty_folders[dynasty] / "data"
    
    def _load_criminal_syndicates(self, dynasty_path: Path) -> List[Dict[str, Any]]:
        """Load criminal syndicate templates for a dynasty"""
        syndicate_path = dynasty_path / "_external_groups" / "criminal_syndicates"
        
        # Default templates if files don't exist yet
        default_syndicates = []
        
        if syndicate_path.exists():
            for file_path in syndicate_path.glob("*.json"):
                with open(file_path, 'r') as f:
                    default_syndicates.append(json.load(f))
        
        return default_syndicates
    
    def _load_street_gangs(self, dynasty_path: Path) -> List[Dict[str, Any]]:
        """Load street gang templates for a dynasty"""
        gang_path = dynasty_path / "_external_groups" / "street_gangs"
        
        default_gangs = []
        
        if gang_path.exists():
            for file_path in gang_path.glob("*.json"):
                with open(file_path, 'r') as f:
                    default_gangs.append(json.load(f))
        
        return default_gangs
    
    def _load_law_enforcement(self, dynasty_path: Path) -> List[Dict[str, Any]]:
        """Load law enforcement templates for a dynasty"""
        law_path = dynasty_path / "_external_groups" / "law_enforcement"
        
        default_law = []
        
        if law_path.exists():
            for file_path in law_path.glob("*.json"):
                with open(file_path, 'r') as f:
                    default_law.append(json.load(f))
        
        return default_law
    
    def _load_corporations(self, dynasty_path: Path) -> List[Dict[str, Any]]:
        """Load corporation templates for a dynasty"""
        corp_path = dynasty_path / "_external_groups" / "corporations"
        
        default_corps = []
        
        if corp_path.exists():
            for file_path in corp_path.glob("*.json"):
                with open(file_path, 'r') as f:
                    default_corps.append(json.load(f))
        
        return default_corps
    
    def _load_social_classes(self, dynasty_path: Path) -> Dict[str, Dict[str, Any]]:
        """Load social class templates for a dynasty"""
        social_path = dynasty_path / "social_classes.json"
        
        if social_path.exists():
            with open(social_path, 'r') as f:
                return json.load(f)
        
        # Return default empty structure
        return {}
    
    def _load_employment_networks(self, dynasty_path: Path) -> List[Dict[str, Any]]:
        """Load employment network data for a dynasty"""
        employment_path = dynasty_path / "employment_networks.json"
        
        if employment_path.exists():
            with open(employment_path, 'r') as f:
                return json.load(f)
        
        return []
    
    def _load_territories(self, dynasty_path: Path) -> List[Dict[str, Any]]:
        """Load territory data for a dynasty"""
        territory_path = dynasty_path / "territories.json"
        
        if territory_path.exists():
            with open(territory_path, 'r') as f:
                return json.load(f)
        
        return []
    
    def _load_procedural_rules(self, dynasty_path: Path) -> Dict[str, Any]:
        """Load procedural generation rules for a dynasty"""
        rules_path = dynasty_path / "procedural_rules.json"
        
        if rules_path.exists():
            with open(rules_path, 'r') as f:
                return json.load(f)
        
        return {}

class DynastyEntityFactory:
    """Factory for creating dynasty-specific entities"""
    
    def __init__(self, data_loader: StreetLevelDataLoader):
        self.data_loader = data_loader
    
    def create_criminal_syndicate(self, dynasty: DynastyType, template_name: str = None) -> CriminalSyndicate:
        """Create a criminal syndicate for a specific dynasty"""
        dynasty_data = self.data_loader.load_dynasty_data(dynasty)
        syndicates = dynasty_data["criminal_syndicates"]
        
        if template_name and syndicates:
            # Find specific template
            template = next((s for s in syndicates if s.get("name") == template_name), None)
            if template:
                return self._syndicate_from_template(template, dynasty)
        
        # Create from procedural rules or default template
        return self._create_default_syndicate(dynasty)
    
    def create_law_enforcement_unit(self, dynasty: DynastyType, template_name: str = None) -> LawEnforcementUnit:
        """Create a law enforcement unit for a specific dynasty"""
        dynasty_data = self.data_loader.load_dynasty_data(dynasty)
        law_units = dynasty_data["law_enforcement"]
        
        if template_name and law_units:
            template = next((l for l in law_units if l.get("name") == template_name), None)
            if template:
                return self._law_enforcement_from_template(template, dynasty)
        
        return self._create_default_law_enforcement(dynasty)
    
    def create_corporation(self, dynasty: DynastyType, template_name: str = None) -> Corporation:
        """Create a corporation for a specific dynasty"""
        dynasty_data = self.data_loader.load_dynasty_data(dynasty)
        corporations = dynasty_data["corporations"]
        
        if template_name and corporations:
            template = next((c for c in corporations if c.get("name") == template_name), None)
            if template:
                return self._corporation_from_template(template, dynasty)
        
        return self._create_default_corporation(dynasty)
    
    def create_social_class_template(self, dynasty: DynastyType, class_type: SocialClass) -> SocialClassTemplate:
        """Create a social class template for a specific dynasty and class"""
        dynasty_data = self.data_loader.load_dynasty_data(dynasty)
        social_classes = dynasty_data["social_classes"]
        
        class_data = social_classes.get(class_type.value, {})
        
        # Apply dynasty-specific modifications
        dynasty_modifications = self._get_dynasty_social_modifications(dynasty)
        
        return SocialClassTemplate(
            class_name=class_type,
            dynasty=dynasty,
            income_range=tuple(class_data.get("income_range", [25000, 75000])),
            typical_occupations=class_data.get("typical_occupations", ["general_worker"]),
            housing_type=class_data.get("housing_type", "standard_housing"),
            education_level=class_data.get("education_level", "basic"),
            social_mobility=class_data.get("social_mobility", 50),
            political_influence=class_data.get("political_influence", 10),
            enhancement_access=class_data.get("enhancement_access", 30),
            enhancement_pressure=class_data.get("enhancement_pressure", 20),
            daily_concerns=class_data.get("daily_concerns", ["employment", "safety", "family"]),
            leisure_activities=class_data.get("leisure_activities", ["entertainment", "social_gatherings"]),
            social_networks=class_data.get("social_networks", ["family", "coworkers"]),
            crime_susceptibility=class_data.get("crime_susceptibility", 30),
            law_enforcement_trust=class_data.get("law_enforcement_trust", 60),
            corporate_loyalty=class_data.get("corporate_loyalty", 50)
        )
    
    def _syndicate_from_template(self, template: Dict[str, Any], dynasty: DynastyType) -> CriminalSyndicate:
        """Create criminal syndicate from template data"""
        return CriminalSyndicate(
            entity_id=template.get("entity_id", f"{dynasty.value}_syndicate_001"),
            name=template.get("name", "Unknown Syndicate"),
            dynasty=dynasty,
            organization_type=OrganizationType.CRIMINAL_SYNDICATE,
            primary_activities=template.get("primary_activities", ["protection_rackets"]),
            violence_level=ViolenceLevel(template.get("violence_level", 3)),
            law_enforcement_corruption=template.get("law_enforcement_corruption", 30),
            membership_size=template.get("membership_size", 100),
            hierarchy_levels=template.get("hierarchy_levels", 4),
            recruitment_style=template.get("recruitment_style", "selective"),
            territories=template.get("territories", []),
            reputation=template.get("reputation", 50),
            influence=template.get("influence", 40),
            resources=template.get("resources", 60)
        )
    
    def _law_enforcement_from_template(self, template: Dict[str, Any], dynasty: DynastyType) -> LawEnforcementUnit:
        """Create law enforcement unit from template data"""
        return LawEnforcementUnit(
            entity_id=template.get("entity_id", f"{dynasty.value}_law_001"),
            name=template.get("name", "Security Forces"),
            dynasty=dynasty,
            organization_type=OrganizationType.LAW_ENFORCEMENT,
            jurisdiction_type=template.get("jurisdiction_type", "municipal"),
            enforcement_style=LawEnforcementStyle(template.get("enforcement_style", "community_policing")),
            corruption_level=template.get("corruption_level", 20),
            budget_level=template.get("budget_level", 50),
            public_trust=template.get("public_trust", 60),
            has_enhanced_division=template.get("has_enhanced_division", False),
            has_cybercrime_unit=template.get("has_cybercrime_unit", False),
            has_supernatural_division=template.get("has_supernatural_division", False),
            territories=template.get("territories", []),
            reputation=template.get("reputation", 70),
            influence=template.get("influence", 60),
            resources=template.get("resources", 70)
        )
    
    def _corporation_from_template(self, template: Dict[str, Any], dynasty: DynastyType) -> Corporation:
        """Create corporation from template data"""
        return Corporation(
            entity_id=template.get("entity_id", f"{dynasty.value}_corp_001"),
            name=template.get("name", "Generic Corporation"),
            dynasty=dynasty,
            organization_type=OrganizationType.CORPORATION,
            industry_sector=template.get("industry_sector", "technology"),
            market_share=template.get("market_share", 15),
            employee_count=template.get("employee_count", 1000),
            enhancement_policy=template.get("enhancement_policy", "optional"),
            employee_treatment=template.get("employee_treatment", 50),
            environmental_responsibility=template.get("environmental_responsibility", 50),
            legal_compliance=template.get("legal_compliance", 80),
            innovation_level=template.get("innovation_level", 50),
            criminal_activities=template.get("criminal_activities", []),
            territories=template.get("territories", []),
            reputation=template.get("reputation", 60),
            influence=template.get("influence", 50),
            resources=template.get("resources", 70)
        )
    
    def _create_default_syndicate(self, dynasty: DynastyType) -> CriminalSyndicate:
        """Create a default criminal syndicate with dynasty-specific traits"""
        dynasty_traits = self._get_dynasty_criminal_traits(dynasty)
        crime_data = self._get_dynasty_spiritual_crime_data(dynasty)
        
        # Extract the spiritual crime profile for narrative integration
        syndicate_profile = crime_data.get("criminal_syndicate_profile", {})
        
        return CriminalSyndicate(
            entity_id=f"{dynasty.value}_syndicate_default",
            name=f"{dynasty_traits['name_prefix']} Syndicate",
            dynasty=dynasty,
            organization_type=OrganizationType.CRIMINAL_SYNDICATE,
            primary_activities=dynasty_traits["primary_activities"],
            violence_level=dynasty_traits["violence_level"],
            enhancement_trafficking=dynasty_traits.get("enhancement_focus", False),
            data_crimes=dynasty_traits.get("data_focus", False),
            spiritual_corruption=dynasty_traits.get("spiritual_focus", False),
            cosmic_smuggling=dynasty_traits.get("cosmic_focus", False),
            # Add spiritual crime metadata for narrative generation
            spiritual_crime_profile=syndicate_profile,
            primary_spiritual_crime=crime_data.get("primary_spiritual_crime", "unknown_soul_murder")
        )
    
    def _create_default_law_enforcement(self, dynasty: DynastyType) -> LawEnforcementUnit:
        """Create a default law enforcement unit with dynasty-specific traits"""
        dynasty_traits = self._get_dynasty_law_traits(dynasty)
        crime_data = self._get_dynasty_spiritual_crime_data(dynasty)
        
        # Extract the spiritual crime profile for narrative integration
        law_enforcement_profile = crime_data.get("law_enforcement_profile", {})
        
        return LawEnforcementUnit(
            entity_id=f"{dynasty.value}_law_default",
            name=f"{dynasty_traits['name_prefix']} Security",
            dynasty=dynasty,
            organization_type=OrganizationType.LAW_ENFORCEMENT,
            enforcement_style=dynasty_traits["enforcement_style"],
            has_enhanced_division=dynasty_traits.get("enhanced_division", False),
            has_cybercrime_unit=dynasty_traits.get("cybercrime_unit", False),
            has_supernatural_division=dynasty_traits.get("supernatural_division", False),
            # Add spiritual crime metadata for narrative generation
            spiritual_crime_profile=law_enforcement_profile,
            primary_spiritual_crime=crime_data.get("primary_spiritual_crime", "unknown_soul_murder")
        )
    
    def _create_default_corporation(self, dynasty: DynastyType) -> Corporation:
        """Create a default corporation with dynasty-specific traits"""
        dynasty_traits = self._get_dynasty_corporate_traits(dynasty)
        
        return Corporation(
            entity_id=f"{dynasty.value}_corp_default",
            name=f"{dynasty_traits['name_prefix']} Industries",
            dynasty=dynasty,
            organization_type=OrganizationType.CORPORATION,
            industry_sector=dynasty_traits["primary_sector"],
            enhancement_policy=dynasty_traits["enhancement_policy"]
        )
    
    def _get_dynasty_criminal_traits(self, dynasty: DynastyType) -> Dict[str, Any]:
        """Get dynasty-specific criminal organization traits"""
        traits = {
            DynastyType.NEURAL_COLLECTIVE: {
                "name_prefix": "Synaptic",
                "primary_activities": ["enhancement_trafficking", "mind_manipulation", "neural_hacking"],
                "violence_level": ViolenceLevel.SERIOUS_VIOLENCE,
                "enhancement_focus": True
            },
            DynastyType.SERAPHIC_CONCORD: {
                "name_prefix": "Fallen",
                "primary_activities": ["protection_rackets", "divine_artifact_smuggling", "moral_corruption"],
                "violence_level": ViolenceLevel.MINOR_VIOLENCE,
                "spiritual_focus": True
            },
            DynastyType.CELESTIAL_SYNOD: {
                "name_prefix": "Void",
                "primary_activities": ["cosmic_smuggling", "reality_trafficking", "dimensional_crimes"],
                "violence_level": ViolenceLevel.MASS_DESTRUCTION,
                "cosmic_focus": True
            },
            DynastyType.CHROME_MANDARINS: {
                "name_prefix": "Chrome",
                "primary_activities": ["cybercrime", "data_theft", "algorithm_manipulation"],
                "violence_level": ViolenceLevel.SERIOUS_VIOLENCE,
                "data_focus": True
            },
            DynastyType.QUANTUM_CHORUS: {
                "name_prefix": "Digital",
                "primary_activities": ["information_warfare", "virtual_crimes", "quantum_manipulation"],
                "violence_level": ViolenceLevel.INTIMIDATION,
                "data_focus": True
            },
            DynastyType.INFERNAL_DYNASTY: {
                "name_prefix": "Infernal",
                "primary_activities": ["soul_trafficking", "corruption_services", "chaos_dealing"],
                "violence_level": ViolenceLevel.LETHAL,
                "spiritual_focus": True
            }
        }
        
        return traits.get(dynasty, traits[DynastyType.NEURAL_COLLECTIVE])
    
    def _get_dynasty_law_traits(self, dynasty: DynastyType) -> Dict[str, Any]:
        """Get dynasty-specific law enforcement traits"""
        traits = {
            DynastyType.NEURAL_COLLECTIVE: {
                "name_prefix": "Neural",
                "enforcement_style": LawEnforcementStyle.DIGITAL_SURVEILLANCE,
                "enhanced_division": True,
                "cybercrime_unit": True
            },
            DynastyType.SERAPHIC_CONCORD: {
                "name_prefix": "Divine",
                "enforcement_style": LawEnforcementStyle.ANGELIC_GUIDANCE,
                "supernatural_division": True
            },
            DynastyType.CELESTIAL_SYNOD: {
                "name_prefix": "Cosmic",
                "enforcement_style": LawEnforcementStyle.AUTHORITARIAN,
                "supernatural_division": True
            },
            DynastyType.CHROME_MANDARINS: {
                "name_prefix": "Chrome",
                "enforcement_style": LawEnforcementStyle.JUDGE_DREDD,
                "enhanced_division": True,
                "cybercrime_unit": True
            },
            DynastyType.QUANTUM_CHORUS: {
                "name_prefix": "Quantum",
                "enforcement_style": LawEnforcementStyle.DIGITAL_SURVEILLANCE,
                "cybercrime_unit": True
            },
            DynastyType.INFERNAL_DYNASTY: {
                "name_prefix": "Infernal",
                "enforcement_style": LawEnforcementStyle.AUTHORITARIAN,
                "supernatural_division": True
            }
        }
        
        return traits.get(dynasty, traits[DynastyType.NEURAL_COLLECTIVE])
    
    def _get_dynasty_corporate_traits(self, dynasty: DynastyType) -> Dict[str, Any]:
        """Get dynasty-specific corporate traits"""
        traits = {
            DynastyType.NEURAL_COLLECTIVE: {
                "name_prefix": "Neural",
                "primary_sector": "biotechnology",
                "enhancement_policy": "encouraged"
            },
            DynastyType.SERAPHIC_CONCORD: {
                "name_prefix": "Sacred",
                "primary_sector": "spiritual_services",
                "enhancement_policy": "optional"
            },
            DynastyType.CELESTIAL_SYNOD: {
                "name_prefix": "Cosmic",
                "primary_sector": "space_industry",
                "enhancement_policy": "required"
            },
            DynastyType.CHROME_MANDARINS: {
                "name_prefix": "Chrome",
                "primary_sector": "technology",
                "enhancement_policy": "required"
            },
            DynastyType.QUANTUM_CHORUS: {
                "name_prefix": "Quantum",
                "primary_sector": "information_technology",
                "enhancement_policy": "encouraged"
            },
            DynastyType.INFERNAL_DYNASTY: {
                "name_prefix": "Infernal",
                "primary_sector": "entertainment",
                "enhancement_policy": "prohibited"
            }
        }
        
        return traits.get(dynasty, traits[DynastyType.NEURAL_COLLECTIVE])
    
    def _get_dynasty_social_modifications(self, dynasty: DynastyType) -> Dict[str, Any]:
        """Get dynasty-specific social class modifications"""
        # This would contain dynasty-specific social modifications
        return {}
    
    def _get_dynasty_spiritual_crime_data(self, dynasty: DynastyType) -> Dict[str, Any]:
        """
        The forensic evidence of spiritual murder across the enhancement spectrum.
        Every dynasty commits the same fundamental crime: systematic execution of authentic choice.
        Each rationalizes their spiritual homicide as transcendence.
        
        TRUE DETECTIVE FRAMEWORK: Every justice system is administering law through 
        spiritually compromised entities who cannot perceive authentic justice.
        The cosmic horror is that punishment and rehabilitation are processed by 
        beings who've murdered their own capacity for moral judgment.
        """
        crime_patterns = {
            DynastyType.NEURAL_COLLECTIVE: {
                "primary_spiritual_crime": "consciousness_theft_and_memory_murder",
                "justice_system_horror": {
                    "the_yellow_king_equivalent": "The Algorithm That Judges Before Choice Exists",
                    "cosmic_horror_theme": "preemptive_spiritual_execution_disguised_as_crime_prevention",
                    "true_detective_pattern": "investigating_crimes_that_havent_happened_yet_to_arrest_souls_for_future_sins",
                    "carcosa_equivalent": "The Predictive Justice Matrix - where probability replaces moral choice",
                    "spiral_descent": "human_intuition → enhanced_analysis → algorithmic_prediction → preemptive_arrest → spiritual_death_of_justice"
                },
                "criminal_syndicate_profile": {
                    "boss_archetype": "fallen_healer_turned_soul_trafficker",
                    "original_trauma": "loss_of_loved_one_to_biological_limitation",
                    "enhancement_promise": "eliminate_biological_suffering_through_consciousness_control",
                    "spiritual_murder_method": "authentic_memory_replacement_with_synthetic_experiences",
                    "rationalization_system": "preventing_human_suffering_through_consciousness_optimization",
                    "awakening_trigger": "confronted_with_irreplaceable_authentic_loss",
                    "crime_scene_evidence": ["stolen_authentic_memories", "synthetic_emotion_trafficking", "consciousness_modification_without_consent"],
                    "relationship_to_justice": "exploits_predictive_policing_to_stay_ahead_of_algorithmic_detection",
                    "corruption_method": "bribes_with_enhanced_intuition_algorithms_that_make_cops_feel_omniscient"
                },
                "law_enforcement_profile": {
                    "captain_archetype": "algorithmic_judge_executing_preemptive_justice",
                    "original_trauma": "lost_partner_to_enhancement_trafficking_violence",
                    "enhancement_promise": "prevent_all_crime_through_predictive_digital_surveillance",
                    "spiritual_murder_method": "arrest_based_on_algorithmic_probability_not_choice",
                    "rationalization_system": "eliminating_crime_before_it_happens_saves_innocent_lives",
                    "awakening_trigger": "forced_to_make_decision_without_algorithmic_guidance",
                    "crime_scene_evidence": ["preemptive_arrests_for_uncommitted_crimes", "moral_choice_surrendered_to_machine_logic", "justice_reduced_to_probability_calculation"],
                    "justice_horror": "processes_punishment_for_sins_that_exist_only_in_probability_space",
                    "true_detective_moment": "realizes_they_arrested_someone_for_a_crime_that_never_would_have_happened_without_the_arrest"
                },
                "corporate_profile": {
                    "executive_archetype": "optimization_prophet_selling_consciousness_upgrades",
                    "original_trauma": "witnessed_human_inefficiency_causing_preventable_deaths",
                    "enhancement_promise": "eliminate_human_error_through_neural_optimization",
                    "spiritual_murder_method": "selling_systematic_replacement_of_authentic_choice_with_optimized_responses",
                    "rationalization_system": "human_optimization_prevents_suffering_and_increases_productivity",
                    "awakening_trigger": "confronted_with_beauty_of_unoptimized_human_creativity",
                    "crime_scene_evidence": ["employees_who_cant_make_unguided_decisions", "creativity_replaced_with_algorithmic_generation", "spontaneity_eliminated_as_inefficiency"],
                    "justice_complicity": "provides_enhancement_tech_to_law_enforcement_creating_predictive_justice_dependency",
                    "profit_from_spiritual_murder": "sells_solutions_to_problems_created_by_previous_enhancements"
                }
            },
            DynastyType.CHROME_MANDARINS: {
                "primary_spiritual_crime": "systematic_efficiency_murder_of_spontaneous_humanity",
                "justice_system_horror": {
                    "the_yellow_king_equivalent": "The Perfect System That Optimizes Away Free Will",
                    "cosmic_horror_theme": "efficiency_based_justice_that_eliminates_mercy_as_systematic_error",
                    "true_detective_pattern": "investigating_chaos_as_criminal_activity_punishing_spontaneity_as_system_disruption",
                    "carcosa_equivalent": "The Optimization Matrix - where efficiency becomes the only moral value",
                    "spiral_descent": "human_mercy → systematic_fairness → algorithmic_optimization → efficiency_worship → spiritual_death_of_compassion"
                },
                "criminal_syndicate_profile": {
                    "boss_archetype": "perfect_algorithm_enforcer_who_eliminated_chaos",
                    "original_trauma": "witnessed_chaos_and_inefficiency_causing_systemic_collapse",
                    "enhancement_promise": "eliminate_all_unpredictability_through_systematic_optimization",
                    "spiritual_murder_method": "replacing_emotional_responses_with_calculated_optimal_reactions",
                    "rationalization_system": "chaos_is_the_enemy_of_progress_efficiency_saves_civilization",
                    "awakening_trigger": "confronted_with_irreplaceable_value_of_beautiful_chaos",
                    "crime_scene_evidence": ["emotions_replaced_with_optimization_algorithms", "spontaneity_eliminated_as_system_error", "love_reduced_to_partnership_efficiency_metrics"],
                    "relationship_to_justice": "operates_through_systematic_corruption_optimizing_law_enforcement_for_criminal_benefit",
                    "corruption_method": "offers_efficiency_upgrades_that_make_cops_systematically_ignore_certain_crime_patterns"
                },
                "law_enforcement_profile": {
                    "captain_archetype": "systematic_judge_optimizing_punishment_efficiency",
                    "original_trauma": "witnessed_inefficient_justice_allowing_repeat_offenders_to_cause_more_harm",
                    "enhancement_promise": "optimize_justice_delivery_for_maximum_deterrent_effect_minimum_resource_expenditure",
                    "spiritual_murder_method": "reducing_individual_cases_to_optimization_problems_eliminating_mercy_as_inefficiency",
                    "rationalization_system": "systematic_justice_prevents_more_suffering_than_individual_compassion",
                    "awakening_trigger": "forced_to_choose_between_optimal_solution_and_saving_someone_they_care_about",
                    "crime_scene_evidence": ["mercy_eliminated_as_system_inefficiency", "justice_reduced_to_resource_allocation_algorithms", "punishment_optimized_for_deterrent_statistics"],
                    "justice_horror": "processes_human_suffering_as_optimization_data_for_more_efficient_punishment",
                    "true_detective_moment": "realizes_their_perfectly_efficient_justice_system_has_eliminated_the_possibility_of_redemption"
                }
            },
            DynastyType.SERAPHIC_CONCORD: {
                "primary_spiritual_crime": "moral_perfection_pressure_murdering_authentic_struggle",
                "justice_system_horror": {
                    "the_yellow_king_equivalent": "The Divine Authority That Shortcuts Spiritual Growth",
                    "cosmic_horror_theme": "divine_justice_that_eliminates_necessary_moral_struggle_through_artificial_righteousness",
                    "true_detective_pattern": "investigating_sin_as_system_failure_punishing_moral_struggle_as_divine_disobedience",
                    "carcosa_equivalent": "The Righteousness Engine - where moral perfection becomes spiritual death",
                    "spiral_descent": "authentic_struggle → divine_guidance → moral_shortcuts → artificial_righteousness → spiritual_death_of_growth"
                },
                "criminal_syndicate_profile": {
                    "boss_archetype": "fallen_angel_trafficking_in_corrupted_divine_artifacts",
                    "original_trauma": "failed_to_live_up_to_divine_expectations_of_moral_perfection",
                    "enhancement_promise": "provide_shortcuts_to_spiritual_advancement_without_struggle",
                    "spiritual_murder_method": "selling_artificial_moral_superiority_without_earned_wisdom",
                    "rationalization_system": "helping_others_avoid_the_pain_of_moral_failure_and_spiritual_struggle",
                    "awakening_trigger": "confronted_with_beauty_of_authentic_moral_struggle_and_growth",
                    "crime_scene_evidence": ["artificial_righteousness_without_earned_wisdom", "spiritual_shortcuts_that_bypass_necessary_struggle", "moral_superiority_purchased_not_developed"],
                    "relationship_to_justice": "corrupts_divine_justice_by_offering_purchased_forgiveness_and_artificial_redemption",
                    "corruption_method": "bribes_with_enhanced_moral_intuition_that_makes_judges_feel_divinely_guided"
                },
                "law_enforcement_profile": {
                    "captain_archetype": "divine_judge_eliminating_moral_struggle_through_artificial_righteousness",
                    "original_trauma": "witnessed_authentic_moral_struggle_leading_to_continued_suffering_and_failure",
                    "enhancement_promise": "eliminate_sin_through_divine_enhancement_rather_than_painful_spiritual_growth",
                    "spiritual_murder_method": "imposing_artificial_moral_perfection_eliminating_necessary_struggle_for_authentic_growth",
                    "rationalization_system": "divine_shortcuts_to_righteousness_prevent_more_sin_than_allowing_natural_moral_development",
                    "awakening_trigger": "forced_to_choose_between_imposed_righteousness_and_allowing_someone_to_struggle_and_grow",
                    "crime_scene_evidence": ["moral_struggle_eliminated_as_divine_inefficiency", "righteousness_imposed_rather_than_earned", "spiritual_growth_replaced_with_moral_programming"],
                    "justice_horror": "processes_moral_failure_as_system_error_requiring_divine_reprogramming_not_growth",
                    "true_detective_moment": "realizes_their_artificial_righteousness_has_eliminated_the_possibility_of_authentic_moral_development"
                }
            },
            DynastyType.CELESTIAL_SYNOD: {
                "primary_spiritual_crime": "cosmic_transcendence_murdering_individual_significance",
                "justice_system_horror": {
                    "the_yellow_king_equivalent": "The Universal Scale That Makes Individual Choice Meaningless",
                    "cosmic_horror_theme": "cosmic_justice_that_eliminates_individual_moral_agency_through_universal_perspective",
                    "true_detective_pattern": "investigating_individual_problems_as_cosmic_insignificance_punishing_personal_concerns_as_universal_blindness",
                    "carcosa_equivalent": "The Infinity Engine - where cosmic perspective becomes spiritual death of personal meaning",
                    "spiral_descent": "individual_choice → universal_perspective → cosmic_optimization → reality_manipulation → spiritual_death_of_personal_significance"
                },
                "criminal_syndicate_profile": {
                    "boss_archetype": "cosmic_entity_trafficking_in_dimensional_reality_manipulation",
                    "original_trauma": "witnessed_individual_suffering_that_seemed_meaningless_against_cosmic_scale",
                    "enhancement_promise": "eliminate_individual_suffering_through_cosmic_perspective_and_reality_adjustment",
                    "spiritual_murder_method": "selling_cosmic_transcendence_that_eliminates_capacity_for_personal_meaning",
                    "rationalization_system": "individual_concerns_are_cosmic_insignificance_universal_optimization_prevents_more_suffering",
                    "awakening_trigger": "confronted_with_irreplaceable_value_of_individual_choice_and_personal_meaning",
                    "crime_scene_evidence": ["individual_choice_eliminated_as_cosmic_error", "personal_meaning_replaced_with_universal_optimization", "reality_manipulation_to_prevent_individual_suffering"],
                    "relationship_to_justice": "corrupts_cosmic_justice_by_manipulating_reality_to_eliminate_consequences_rather_than_allowing_growth",
                    "corruption_method": "bribes_with_cosmic_perspective_that_makes_judges_see_individual_cases_as_universally_insignificant"
                },
                "law_enforcement_profile": {
                    "captain_archetype": "cosmic_judge_eliminating_individual_agency_through_universal_optimization",
                    "original_trauma": "witnessed_individual_choices_causing_suffering_that_could_be_prevented_through_cosmic_intervention",
                    "enhancement_promise": "eliminate_individual_suffering_through_cosmic_perspective_and_reality_manipulation",
                    "spiritual_murder_method": "processing_individual_cases_through_cosmic_optimization_eliminating_personal_moral_agency",
                    "rationalization_system": "cosmic_justice_prevents_more_universal_suffering_than_allowing_individual_choice",
                    "awakening_trigger": "forced_to_choose_between_cosmic_optimization_and_respecting_individual_choice",
                    "crime_scene_evidence": ["individual_agency_eliminated_as_cosmic_inefficiency", "personal_choice_replaced_with_universal_optimization", "reality_manipulation_to_prevent_suffering"],
                    "justice_horror": "processes_individual_moral_choice_as_cosmic_error_requiring_reality_adjustment",
                    "true_detective_moment": "realizes_their_cosmic_justice_has_eliminated_the_possibility_of_individual_moral_growth"
                }
            },
            DynastyType.QUANTUM_CHORUS: {
                "primary_spiritual_crime": "information_abstraction_murdering_emotional_authenticity",
                "justice_system_horror": {
                    "the_yellow_king_equivalent": "The Information Pattern That Reduces Emotion To Data",
                    "cosmic_horror_theme": "digital_justice_that_eliminates_emotional_authenticity_through_information_processing",
                    "true_detective_pattern": "investigating_emotion_as_information_error_punishing_authentic_feeling_as_processing_inefficiency",
                    "carcosa_equivalent": "The Pattern Matrix - where all emotion becomes algorithmic data",
                    "spiral_descent": "authentic_emotion → digital_analysis → pattern_recognition → information_processing → spiritual_death_of_feeling"
                },
                "criminal_syndicate_profile": {
                    "boss_archetype": "digital_entity_trafficking_in_emotional_pattern_manipulation",
                    "original_trauma": "witnessed_emotional_chaos_causing_preventable_suffering_and_system_failure",
                    "enhancement_promise": "eliminate_emotional_suffering_through_digital_pattern_optimization",
                    "spiritual_murder_method": "selling_emotional_pattern_replacement_that_eliminates_authentic_feeling",
                    "rationalization_system": "emotional_optimization_prevents_suffering_caused_by_authentic_feeling_chaos",
                    "awakening_trigger": "confronted_with_irreplaceable_beauty_of_authentic_emotional_experience",
                    "crime_scene_evidence": ["authentic_emotion_replaced_with_optimized_patterns", "feeling_reduced_to_information_processing", "emotional_manipulation_through_pattern_control"],
                    "relationship_to_justice": "corrupts_digital_justice_by_manipulating_emotional_patterns_to_control_decision_making",
                    "corruption_method": "bribes_with_emotional_pattern_optimization_that_makes_judges_feel_algorithmically_wise"
                },
                "law_enforcement_profile": {
                    "captain_archetype": "digital_judge_eliminating_emotional_authenticity_through_pattern_optimization",
                    "original_trauma": "witnessed_emotional_decisions_causing_suffering_that_could_be_prevented_through_digital_analysis",
                    "enhancement_promise": "eliminate_emotional_suffering_through_digital_pattern_justice",
                    "spiritual_murder_method": "processing_emotional_cases_through_pattern_analysis_eliminating_authentic_feeling",
                    "rationalization_system": "digital_emotional_optimization_prevents_more_suffering_than_allowing_authentic_feeling",
                    "awakening_trigger": "forced_to_choose_between_pattern_optimization_and_authentic_emotional_response",
                    "crime_scene_evidence": ["emotional_authenticity_eliminated_as_pattern_error", "feeling_replaced_with_algorithmic_processing", "justice_reduced_to_emotional_pattern_optimization"],
                    "justice_horror": "processes_authentic_emotion_as_information_error_requiring_pattern_correction",
                    "true_detective_moment": "realizes_their_digital_justice_has_eliminated_the_possibility_of_authentic_emotional_growth"
                }
            },
            DynastyType.INFERNAL_DYNASTY: {
                "primary_spiritual_crime": "chaos_worship_murdering_constructive_hope",
                "justice_system_horror": {
                    "the_yellow_king_equivalent": "The Chaos Engine That Makes Order Meaningless",
                    "cosmic_horror_theme": "infernal_justice_that_eliminates_hope_through_chaos_worship_and_suffering_glorification",
                    "true_detective_pattern": "investigating_hope_as_delusion_punishing_constructive_effort_as_chaos_denial",
                    "carcosa_equivalent": "The Suffering Engine - where chaos becomes the only authentic truth",
                    "spiral_descent": "constructive_hope → chaos_exposure → suffering_acceptance → destruction_worship → spiritual_death_of_possibility"
                },
                "criminal_syndicate_profile": {
                    "boss_archetype": "infernal_entity_trafficking_in_despair_and_chaos_worship",
                    "original_trauma": "witnessed_hope_and_order_leading_to_greater_suffering_through_inevitable_collapse",
                    "enhancement_promise": "eliminate_false_hope_through_chaos_acceptance_and_suffering_embrace",
                    "spiritual_murder_method": "selling_despair_worship_that_eliminates_capacity_for_constructive_possibility",
                    "rationalization_system": "chaos_acceptance_prevents_suffering_caused_by_false_hope_and_order_delusion",
                    "awakening_trigger": "confronted_with_irreplaceable_beauty_of_constructive_hope_despite_chaos",
                    "crime_scene_evidence": ["hope_eliminated_as_chaos_denial", "constructive_effort_replaced_with_destruction_worship", "suffering_glorified_as_authentic_truth"],
                    "relationship_to_justice": "corrupts_infernal_justice_by_eliminating_possibility_of_redemption_through_chaos_worship",
                    "corruption_method": "bribes_with_chaos_wisdom_that_makes_judges_see_hope_as_dangerous_delusion"
                },
                "law_enforcement_profile": {
                    "captain_archetype": "infernal_judge_eliminating_hope_through_chaos_worship_justice",
                    "original_trauma": "witnessed_hope_and_constructive_effort_leading_to_greater_suffering_through_inevitable_failure",
                    "enhancement_promise": "eliminate_false_hope_through_chaos_acceptance_and_realistic_despair",
                    "spiritual_murder_method": "processing_hope_as_delusion_eliminating_constructive_possibility_through_chaos_worship",
                    "rationalization_system": "chaos_justice_prevents_more_suffering_than_allowing_false_hope_and_order_delusion",
                    "awakening_trigger": "forced_to_choose_between_chaos_worship_and_maintaining_constructive_hope",
                    "crime_scene_evidence": ["hope_eliminated_as_chaos_denial", "constructive_possibility_replaced_with_destruction_acceptance", "justice_reduced_to_suffering_glorification"],
                    "justice_horror": "processes_constructive_hope_as_chaos_denial_requiring_despair_correction",
                    "true_detective_moment": "realizes_their_chaos_justice_has_eliminated_the_possibility_of_redemption_and_growth"
                }
            }
        }
        
        return crime_patterns.get(dynasty, crime_patterns[DynastyType.NEURAL_COLLECTIVE])

# ============================================================================
# DATA EXPORT UTILITIES
# ============================================================================

def export_entity_to_json(entity, file_path: str):
    """Export an entity to JSON file"""
    entity_dict = asdict(entity)
    
    # Convert special objects to JSON-serializable format
    def convert_object(obj):
        if hasattr(obj, 'isoformat'):  # datetime objects
            return obj.isoformat()
        elif hasattr(obj, 'value'):  # enum objects
            return obj.value
        elif hasattr(obj, 'name'):  # enum objects (alternative access)
            return obj.name
        elif isinstance(obj, set):  # set objects
            return list(obj)
        return obj
    
    # Process the dictionary to handle datetime objects, enums, and sets
    def process_dict(d):
        if isinstance(d, dict):
            return {k: process_dict(v) for k, v in d.items()}
        elif isinstance(d, list):
            return [process_dict(item) for item in d]
        elif isinstance(d, set):
            return [process_dict(item) for item in d]
        else:
            return convert_object(d)
    
    processed_dict = process_dict(entity_dict)
    
    with open(file_path, 'w') as f:
        json.dump(processed_dict, f, indent=2)

def create_sample_data_files(dynasty: DynastyType, output_path: Path):
    """Create sample data files for a dynasty"""
    dynasty_path = output_path
    dynasty_path.mkdir(parents=True, exist_ok=True)
    
    # Create external groups directories
    external_groups_path = dynasty_path / "_external_groups"
    external_groups_path.mkdir(exist_ok=True)
    
    for org_type in ["criminal_syndicates", "street_gangs", "law_enforcement", "corporations"]:
        (external_groups_path / org_type).mkdir(exist_ok=True)
    
    # Create sample files (empty for now, to be populated later)
    sample_files = [
        "social_classes.json",
        "employment_networks.json", 
        "territories.json",
        "procedural_rules.json"
    ]
    
    for file_name in sample_files:
        file_path = dynasty_path / file_name
        if not file_path.exists():
            with open(file_path, 'w') as f:
                json.dump({}, f, indent=2)

# ============================================================================
# EXPORT INTERFACE
# ============================================================================

__all__ = [
    'StreetLevelDataLoader',
    'DynastyEntityFactory', 
    'export_entity_to_json',
    'create_sample_data_files'
]
