import random
import os
import yaml
import json
from pathlib import Path
from typing import Dict, List, Any

# Load association network for war dynamics
try:
    association_network_path = Path(__file__).parent / "archetype_association_network.json"
    if association_network_path.exists():
        with open(association_network_path, 'r', encoding='utf-8') as f:
            ASSOCIATION_NETWORK = json.load(f)
    else:
        ASSOCIATION_NETWORK = {}
except:
    ASSOCIATION_NETWORK = {}

class War:
    def __init__(self, name, factions, cause, epoch):
        self.name = name
        self.factions = factions  # List of faction/entity names
        self.cause = cause
        self.epoch = epoch
        self.status = "ongoing"
        self.history = []
        self.victor = None
        self.alliance_map = {}  # Track dynamic alliances based on associations

    def log_event(self, event):
        self.history.append(event)

    def end_war(self, victor):
        self.status = "ended"
        self.victor = victor
        self.log_event(f"War ended. Victor: {victor}")

class WarEngine:
    def __init__(self):
        self.active_wars = []
        self.past_wars = []
        self.association_data = ASSOCIATION_NETWORK.get('association_network', {})

    def declare_war(self, factions, cause, epoch):
        war_name = f"War of {cause} ({epoch})"
        war = War(war_name, factions, cause, epoch)
        
        # Analyze association-based war dynamics
        self._analyze_war_associations(war)
        
        war.log_event(f"War declared between {', '.join(factions)} over {cause}.")
        self.active_wars.append(war)
        return war
    
    def _analyze_war_associations(self, war):
        """Analyze how association networks affect war dynamics"""
        for faction in war.factions:
            if faction in self.association_data:
                associations = self.association_data[faction]
                
                # Check for allies who might join the war
                allies = associations.get('associated_allies', [])
                potential_allies = [ally for ally in allies if ally not in war.factions]
                if potential_allies:
                    war.alliance_map[faction] = potential_allies[:3]  # Limit to 3 potential allies
                
                # Check for rivals who might oppose
                rivals = associations.get('associated_rivals', [])
                for rival in rivals:
                    if rival in war.factions and rival != faction:
                        war.log_event(f"Ancient rivalry detected between {faction} and {rival}")

    def resolve_battle(self, war, traits_lookup):
        """Enhanced battle resolution with association network influences"""
        powers = {}
        
        for faction in war.factions:
            traits = traits_lookup.get(faction, {})
            base_power = traits.get("combat", 1) + traits.get("leadership", 1)
            
            # Add association bonuses
            association_bonus = self._calculate_association_bonus(faction, war)
            total_power = base_power + association_bonus + random.randint(0, 5)
            powers[faction] = total_power
            
        winner = max(powers, key=powers.get)
        loser = min(powers, key=powers.get)
        
        # Log association influences
        winner_bonus = self._calculate_association_bonus(winner, war)
        if winner_bonus > 0:
            war.log_event(f"{winner} gains advantage from alliance network (+{winner_bonus})")
        
        war.log_event(f"Battle fought. {winner} defeats {loser}. (Powers: {powers})")
        
        # Check for dynamic alliance shifts
        self._process_alliance_shifts(war, winner, loser)
        
        return winner
    
    def _calculate_association_bonus(self, faction: str, war) -> float:
        """Calculate power bonus from association network"""
        if faction not in self.association_data:
            return 0.0
        
        associations = self.association_data[faction]
        bonus = 0.0
        
        # Allies provide combat bonus
        allies = associations.get('associated_allies', [])
        for ally in allies:
            if ally in war.alliance_map.get(faction, []):
                bonus += 1.5  # Allied support
        
        # Virtues provide morale bonus
        virtues = associations.get('associated_virtues', [])
        if 'courage' in virtues or 'justice' in virtues:
            bonus += 1.0
        
        # Weapons and tools provide tactical advantage
        weapons = associations.get('associated_weapons', [])
        if weapons:
            bonus += 0.5 * len(weapons)
        
        return min(bonus, 5.0)  # Cap bonus at 5
    
    def _process_alliance_shifts(self, war, winner: str, loser: str):
        """Process dynamic alliance shifts based on battle outcomes"""
        # Potential allies might join the winning side
        if winner in war.alliance_map:
            for potential_ally in war.alliance_map[winner]:
                if random.random() < 0.3:  # 30% chance
                    war.log_event(f"{potential_ally} joins {winner} after their victory")
                    if potential_ally not in war.factions:
                        war.factions.append(potential_ally)
        
        # Losing faction might call in desperate allies
        if loser in war.alliance_map:
            for potential_ally in war.alliance_map[loser]:
                if random.random() < 0.2:  # 20% chance
                    war.log_event(f"{potential_ally} aids {loser} in their desperate hour")

    def tick(self, traits_lookup, epoch):
        # Advance all wars by one tick (frame)
        for war in list(self.active_wars):
            if war.status == "ongoing":
                victor = self.resolve_battle(war, traits_lookup)
                # 25% chance to end the war after each battle
                if random.random() < 0.25:
                    war.end_war(victor)
                    self.active_wars.remove(war)
                    self.past_wars.append(war)

    def get_active_wars(self):
        return self.active_wars

    def get_past_wars(self):
        return self.past_wars

def load_dynasty_boss_traits(folder_path):
    traits_lookup = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".yaml") and "traits" in file:
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    traits = yaml.safe_load(f)
                # Get boss name from folder structure or a 'name' field
                boss_name = os.path.basename(os.path.dirname(root))
                if "name" in traits:
                    boss_name = traits["name"]
                traits_lookup[boss_name] = traits
    return traits_lookup

def list_dynasty_boss_names(folder_path):
    names = set()
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".yaml") and "traits" in file:
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    traits = yaml.safe_load(f)
                boss_name = os.path.basename(os.path.dirname(root))
                if "name" in traits:
                    boss_name = traits["name"]
                names.add(boss_name)
    return sorted(names)

# Example usage:
if __name__ == "__main__":
    engine = WarEngine()
    # Example traits lookup (normally you'd pull from your entity system)
    traits_lookup = {
        "Cipher King": {"combat": 10, "leadership": 9},
        "Iron Sovereign": {"combat": 9, "leadership": 10},
    }
    war = engine.declare_war(["Cipher King", "Iron Sovereign"], "the Neon Throne", epoch=1)
    for _ in range(10):
        engine.tick(traits_lookup, epoch=1)
        for w in engine.get_active_wars():
            print(w.history[-1])
    for w in engine.get_past_wars():
        print(f"{w.name} ended. Victor: {w.victor}")