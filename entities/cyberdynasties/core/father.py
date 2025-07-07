import os
import csv
import json
import logging
import datetime
from typing import List, Dict, Any, Optional, Callable
import hashlib
from transformers import pipeline
import random
from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
import yaml
from brains import Brain
from memorymodule import MemoryModule

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# --- Divine Constants ---
DEFAULT_REQUIRED_FIELDS = ['name', 'parent', 'role', 'status']

HISTORICAL_CLASSES = [
    "king", "queen", "prince", "princess", "duke", "duchess", "baron", "baroness",
    "knight", "squire", "merchant", "artisan", "laborer", "serf", "slave", "priest",
    "oracle", "scribe", "philosopher", "matriarch", "patriarch", "chieftain", "elder"
]

CYBER_DYNASTY_CLASSES = [
    "data lord", "neural baron", "quantum prince", "cyber samurai", "netrunner",
    "biohacker", "drone wrangler", "code prophet", "memory broker", "synth aristocrat",
    "nanite laborer", "holo entertainer", "black marketeer", "AI regent", "cloud sovereign",
    "blockchain vizier", "cybernetic enforcer", "street monarch", "guildmaster", "avatar priest",
    "reality forger", "soul miner", "dream architect", "info assassin"
]

SPIRITUAL_STATES = [
    "lost", "fallen", "blessed", "redeemed", "cursed", "wandering", "enlightened", "damned"
]

Base = declarative_base()

def create_dynamic_entity_orm(entity_map, base):
    """
    Dynamically create an ORM model based on all fields in entity_map.
    Each field is mapped to a SQLAlchemy column, inferring type from data.
    """
    all_fields = set()
    for entity in entity_map.values():
        all_fields.update(entity.keys())
    columns = {'barcode': Column(String, primary_key=True)}
    for field in all_fields:
        if field == 'barcode':
            continue
        value = next((e[field] for e in entity_map.values() if field in e and e[field] is not None), None)
        if isinstance(value, int):
            columns[field] = Column(Integer)
        elif isinstance(value, float):
            columns[field] = Column(Float)
        elif isinstance(value, bool):
            columns[field] = Column(Boolean)
        elif isinstance(value, (dict, list)):
            columns[field] = Column(JSON)
        else:
            columns[field] = Column(String)
    return type("DynamicEntityORM", (base,), columns)

class GodDataLoader:
    """
    GodDataLoader:
    - The divine architect and memory-keeper.
    - Discovers, loads, normalizes, merges, and manages all entities and their lineages.
    - Exports the Book of Life to JSON and a living database.
    - Every action is logged, every merge is auditable, every field is sacred.
    """

    def __init__(self, root_folder, recursive=True, strict=False, archetypes_folder=None, bookofmath_folder=None):
        self.root_folder = root_folder
        self.recursive = recursive
        self.strict = strict
        self.archetypes_folder = archetypes_folder or root_folder
        self.bookofmath_folder = bookofmath_folder
        self.csv_files: List[str] = []
        self.data: Dict[str, List[Dict[str, Any]]] = {}
        self.errors: List[str] = []
        self.required_fields: Dict[str, List[str]] = {}
        self.normalizers: Dict[str, Callable[[str, Any], Any]] = {}

    # --- Discovery & Loading ---
    def discover_csv_files(self) -> None:
        self.csv_files.clear()
        if self.recursive:
            for dirpath, _, filenames in os.walk(self.root_folder):
                for filename in filenames:
                    if filename.lower().endswith('.csv'):
                        self.csv_files.append(os.path.join(dirpath, filename))
        else:
            for filename in os.listdir(self.root_folder):
                if filename.lower().endswith('.csv'):
                    self.csv_files.append(os.path.join(self.root_folder, filename))
        logging.info(f"[GOD] Discovered {len(self.csv_files)} CSV files in {self.root_folder}")
        for file in self.csv_files:
            if os.path.getsize(file) == 0:
                logging.warning(f"[GOD] File {file} is empty!")

    def load_csv(self, csv_file: str) -> Optional[List[Dict[str, Any]]]:
        try:
            with open(csv_file, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = [dict((k.strip(), v.strip() if isinstance(v, str) else v) for k, v in row.items()) for row in reader]
            logging.info(f"[GOD] Loaded {len(data)} rows from {csv_file}")
            expected_fields = set(self.required_fields.get(csv_file, DEFAULT_REQUIRED_FIELDS))
            for row in data:
                if not expected_fields.issubset(row.keys()):
                    logging.warning(f"[GOD] Row missing fields in {csv_file}: {row}")
            return data
        except Exception as e:
            error_msg = f"[GOD] Error loading {csv_file}: {e}"
            logging.error(error_msg)
            self.errors.append(error_msg)
            return None

    def load_all_data(self) -> None:
        self.data.clear()
        for file in self.csv_files:
            loaded = self.load_csv(file)
            if loaded is not None:
                self.data[file] = loaded
        logging.info(f"[GOD] Loaded data from {len(self.data)} files.")

    # --- Validation & Normalization ---
    def validate_and_normalize(self) -> None:
        for file, rows in self.data.items():
            required = self.required_fields.get(file, DEFAULT_REQUIRED_FIELDS)
            for i, row in enumerate(rows):
                original_row = row.copy()
                normalized_row = {}
                for k, v in row.items():
                    key = k.strip().lower()
                    value = v.strip() if isinstance(v, str) else v
                    if key in self.normalizers:
                        value = self.normalizers[key](key, value)
                    normalized_row[key] = value

                # --- Ensure every entity has a valid parent ---
                if 'parent' not in normalized_row or not normalized_row['parent'] or normalized_row['parent'].strip().lower() in ('none', '', 'unknown'):
                    normalized_row['parent'] = 'GOD'  # or 'deadbeat'

                # --- FILL STATUS FROM RELATED FIELDS ---
                if 'status' not in normalized_row or not normalized_row['status'] or normalized_row['status'] == 'UNKNOWN':
                    if 'fallen' in normalized_row:
                        if normalized_row['fallen'].lower() == 'true':
                            normalized_row['status'] = 'fallen'
                        elif normalized_row['fallen'].lower() == 'false':
                            normalized_row['status'] = 'active'

                role_val = normalized_row.get('role', '').lower()
                type_val = normalized_row.get('type', '').lower()
                fallen_val = normalized_row.get('fallen', '').lower() if 'fallen' in normalized_row else ''
                status_val = normalized_row.get('status', '').lower() if 'status' in normalized_row else ''

                # Always lost if spirit
                if 'spirit' in role_val or 'spirit' in type_val:
                    normalized_row['status'] = 'lost'
                else:
                    rand = random.random()
                    if rand < 0.15:
                        normalized_row['status'] = 'blessed'
                    elif rand < 0.30:
                        normalized_row['status'] = 'fallen'
                    elif rand < 0.45:
                        normalized_row['status'] = 'lost'
                    else:
                        if 'human' in role_val or 'descendant' in role_val or 'patriarch' in role_val:
                            if not status_val or status_val == 'unknown':
                                normalized_row['status'] = 'blessed' if rand < 0.225 else ('fallen' if rand < 0.375 else 'lost')
                        elif 'angel' in role_val or 'watcher' in role_val or 'cherub' in role_val:
                            if not status_val or status_val == 'unknown':
                                normalized_row['status'] = 'fallen' if fallen_val == 'true' or rand < 0.30 else 'angel'
                        elif 'demon' in role_val:
                            if not status_val or status_val == 'unknown':
                                normalized_row['status'] = 'fallen' if rand < 0.5 else 'lost'
                        else:
                            if not status_val or status_val == 'unknown':
                                normalized_row['status'] = 'active'

                status_val = normalized_row.get('status', '').lower() if 'status' in normalized_row else ''
                if not status_val or status_val == 'unknown':
                    if 'death' in normalized_row or 'deceased' in normalized_row or normalized_row.get('is_alive', '').lower() == 'false':
                        normalized_row['status'] = 'dead'
                    elif normalized_row.get('is_alive', '').lower() == 'true':
                        normalized_row['status'] = 'alive'
                    else:
                        normalized_row['status'] = 'alive'

                # --- SOCIAL CLASS ---
                if 'cyber' in role_val or 'ai' in role_val or 'net' in role_val or 'quantum' in role_val or 'drone' in role_val:
                    normalized_row['social_class'] = random.choice(CYBER_DYNASTY_CLASSES)
                elif 'king' in role_val or 'queen' in role_val or 'prince' in role_val or 'duke' in role_val or 'baron' in role_val:
                    normalized_row['social_class'] = role_val
                elif 'angel' in role_val or 'watcher' in role_val or 'cherub' in role_val:
                    normalized_row['social_class'] = random.choice(["celestial herald", "guardian", "heavenly scribe", "choir leader"])
                elif 'demon' in role_val:
                    normalized_row['social_class'] = random.choice(["underworld baron", "tempter", "shadow broker", "abyssal lord"])
                elif 'priest' in role_val or 'oracle' in role_val or 'prophet' in role_val:
                    normalized_row['social_class'] = role_val
                elif 'human' in type_val or 'descendant' in role_val or 'patriarch' in role_val or 'matriarch' in role_val:
                    normalized_row['social_class'] = random.choice(HISTORICAL_CLASSES)
                else:
                    normalized_row['social_class'] = random.choice(HISTORICAL_CLASSES + CYBER_DYNASTY_CLASSES)

                # --- SPIRITUAL STATE ---
                if 'spirit' in role_val or 'spirit' in type_val:
                    normalized_row['spiritual_state'] = 'lost'
                else:
                    rand = random.random()
                    if rand < 0.15:
                        normalized_row['spiritual_state'] = 'blessed'
                    elif rand < 0.30:
                        normalized_row['spiritual_state'] = 'fallen'
                    elif rand < 0.45:
                        normalized_row['spiritual_state'] = 'lost'
                    else:
                        normalized_row['spiritual_state'] = random.choice(
                            [s for s in SPIRITUAL_STATES if s not in ('lost', 'fallen', 'blessed')]
                        )

                for field in required:
                    if field not in normalized_row or normalized_row[field] == '':
                        msg = f"[GOD] Missing required field '{field}' in {file}, row {i+1}."
                        if self.strict:
                            logging.error(msg + " Strict mode: aborting.")
                            raise ValueError(msg)
                        else:
                            logging.warning(msg + " Filling with 'UNKNOWN'.")
                            normalized_row[field] = 'UNKNOWN'
                            self.errors.append(msg)
                if 'status' in normalized_row:
                    normalized_row['status'] = normalized_row['status'].lower()
                if 'name' in normalized_row and not isinstance(normalized_row['name'], str):
                    msg = f"[GOD] Field 'name' is not a string in {file}, row {i+1}."
                    if self.strict:
                        logging.error(msg + " Strict mode: aborting.")
                        raise TypeError(msg)
                    else:
                        logging.warning(msg + " Converting to string.")
                        normalized_row['name'] = str(normalized_row['name'])
                        self.errors.append(msg)
                for key in ['power_level', 'age']:
                    if key in normalized_row:
                        try:
                            normalized_row[key] = float(normalized_row[key])
                        except Exception:
                            normalized_row[key] = 'UNKNOWN'
                rows[i] = normalized_row
        logging.info(f"[GOD] Validation and normalization complete.")

    def error_report(self) -> None:
        """Print a report of validation and normalization errors."""
        if self.errors:
            logging.info(f"[GOD] Validation/Normalization Errors:")
            for err in self.errors:
                logging.info(f"  {err}")
        with open("validation_errors.json", "w", encoding="utf-8") as f:
            json.dump(self.errors, f, indent=2)

    def summary(self) -> None:
        """Print a summary of loaded data for traceability."""
        logging.info(f"[GOD] Data summary:")
        total_rows = 0
        unique_names = set()
        for file, rows in self.data.items():
            logging.info(f"  {file}: {len(rows)} rows")
            total_rows += len(rows)
            unique_names.update(row['name'] for row in rows if 'name' in row)
        logging.info(f"[GOD] Total rows: {total_rows}")
        logging.info(f"[GOD] Unique entities: {len(unique_names)}")

    def build_lineage_map(self) -> None:
        """
        Build parent-child and ancestry relationships for all entities.
        Supports multiple parents (comma-separated or list).
        """
        self.entity_map: Dict[str, Dict[str, Any]] = {}
        for file, rows in self.data.items():
            for entity in rows:
                key = entity['name']
                if key in self.entity_map:
                    logging.warning(f"[GOD] Duplicate entity name '{key}' found. Overwriting previous entry.")
                self.entity_map[key] = entity
                entity['children'] = []
                entity['parent_refs'] = []

        # Link parents and children (support multiple parents)
        for entity in self.entity_map.values():
            parent_field = entity.get('parent', '')
            if isinstance(parent_field, str):
                parent_names = [p.strip() for p in parent_field.split(',') if p.strip() and p.strip() != 'UNKNOWN']
            elif isinstance(parent_field, list):
                parent_names = [p for p in parent_field if p and p != 'UNKNOWN']
            else:
                parent_names = []
            found_parent = False
            for parent_name in parent_names:
                if parent_name in self.entity_map:
                    parent = self.entity_map[parent_name]
                    entity['parent_refs'].append(parent)
                    parent['children'].append(entity)
                    found_parent = True
                else:
                    logging.warning(f"[GOD] Orphan entity '{entity['name']}' (parent '{parent_name}' not found).")
            # If no parent found, set parent to "deadbeat"
            if not found_parent and parent_names:
                entity['parent'] = "deadbeat"

        # Detect circular ancestry (advanced, for multiple parents)
        def has_circular_ancestry(ent, visited=None):
            if visited is None:
                visited = set()
            if ent['name'] in visited:
                return True
            visited.add(ent['name'])
            for parent in ent.get('parent_refs', []):
                if has_circular_ancestry(parent, visited):
                    return True
            return False

        for entity in self.entity_map.values():
            if has_circular_ancestry(entity):
                logging.error(f"[GOD] Circular ancestry detected for '{entity['name']}'.")

        # Calculate lineage depth
        def get_depth(entity, depth=0):
            if not entity.get('parent_refs'):
                return depth
            return max(get_depth(parent, depth+1) for parent in entity['parent_refs'])
        for entity in self.entity_map.values():
            entity['lineage_depth'] = get_depth(entity)

        logging.info(f"[GOD] Lineage mapping complete. Entities mapped: {len(self.entity_map)}")

    def get_ancestry(self, name: str) -> list:
        """Return the ancestry chain(s) for a given entity name (supports multiple parents)."""
        def ancestry_paths(entity, path=None):
            if path is None:
                path = []
            if not entity.get('parent_refs'):
                return [path + [entity['name']]]
            paths = []
            for parent in entity['parent_refs']:
                paths.extend(ancestry_paths(parent, path + [entity['name']]))
            return paths
        entity = self.entity_map.get(name)
        return ancestry_paths(entity) if entity else []

    def get_descendants(self, name: str) -> list:
        """Return all descendants for a given entity name."""
        descendants = set()
        def collect_descendants(entity):
            for child in entity.get('children', []):
                if child['name'] not in descendants:
                    descendants.add(child['name'])
                    collect_descendants(child)
        entity = self.entity_map.get(name)
        if entity:
            collect_descendants(entity)
        return list(descendants)

    def get_siblings(self, name: str) -> list:
        """Return all siblings for a given entity name."""
        entity = self.entity_map.get(name)
        if not entity or not entity.get('parent_refs'):
            return []
        siblings = set()
        for parent in entity['parent_refs']:
            for child in parent.get('children', []):
                if child['name'] != name:
                    siblings.add(child['name'])
        return list(siblings)

    def generate_barcode(self, entity: Dict[str, Any]) -> str:
        """
        Generate a unique, traceable barcode for an entity based on its lineage and attributes.
        Always traces back to the source ('FATHER').
        """
        # Gather parent barcodes
        parent_barcodes = []
        for parent in entity.get('parent_refs', []):
            # Recursively generate parent barcodes if not already present
            if 'barcode' not in parent:
                parent['barcode'] = self.generate_barcode(parent)
            parent_barcodes.append(parent['barcode'])
        if parent_barcodes:
            # Sort for determinism if multiple parents
            base = '|'.join(sorted(parent_barcodes))
        else:
            base = 'FATHER'
        barcode = f"{base}|{entity['name']}|{entity.get('role','')}|{entity.get('status','')}"
        entity['barcode'] = barcode
        # Optionally hash the barcode for privacy
        if getattr(self, "hash_barcodes", False):
            barcode = hashlib.sha256(barcode.encode()).hexdigest()[:12]
        return barcode

    def assign_barcodes(self):
        """
        Assign barcodes to all entities, using lineage.
        """
        for entity in self.entity_map.values():
            self.generate_barcode(entity)
        logging.info(f"[GOD] Barcode assignment complete.")

    def merge_entities(self):
        """
        Merge duplicate entities by barcode.
        - Uses field-specific merge strategies.
        - Annotates provenance and conflicts.
        - Updates all references to point to the merged entity.
        - Logs all merges and conflicts.
        """
        def merge_numbers(a, b):
            try:
                if a == 'UNKNOWN':
                    return b
                if b == 'UNKNOWN':
                    return a
                return str((float(a) + float(b)) / 2)
            except Exception:
                return merge_strings(a, b)

        def merge_lists(a, b):
            return list(set((a or []) + (b or [])))

        def merge_strings(a, b):
            if a == b:
                return a
            if a == 'UNKNOWN':
                return b
            if b == 'UNKNOWN':
                return a
            return f"{a};{b}"

        def merge_dates(a, b):
            try:
                if a == 'UNKNOWN':
                    return b
                if b == 'UNKNOWN':
                    return a
                da = datetime.datetime.fromisoformat(a)
                db = datetime.datetime.fromisoformat(b)
                return a if da < db else b  # Earliest birth
            except Exception:
                return merge_strings(a, b)

        def merge_booleans(a, b):
            if a == 'UNKNOWN':
                return b
            if b == 'UNKNOWN':
                return a
            return str(bool(a) or bool(b))

        def merge_dicts(a, b):
            result = dict(a or {})
            for k, v in (b or {}).items():
                if k in result:
                    if isinstance(result[k], list) or isinstance(v, list):
                        result[k] = merge_lists(result[k], v)
                    elif isinstance(result[k], dict) or isinstance(v, dict):
                        result[k] = merge_dicts(result[k], v)
                    else:
                        result[k] = merge_strings(result[k], v)
                else:
                    result[k] = v
            return result

        def merge_set(a, b):
            return list(set(a or set()).union(set(b or set())))

        merge_strategies = {
            'children': merge_lists,
            'parent_refs': merge_lists,
            'traits': merge_lists,
            'attributes': merge_dicts,
            'description': merge_strings,
            'status': merge_strings,
            'role': merge_strings,
            'power_level': merge_numbers,
            'created_at': merge_dates,
            'updated_at': merge_dates,
            'is_active': merge_booleans,
            'aliases': merge_set,
            'titles': merge_set,
            'lineage': merge_lists,
            'notes': merge_strings,
            'sources': merge_set,
        }

        barcode_map: Dict[str, Dict[str, Any]] = {}
        duplicates: Dict[str, List[Dict[str, Any]]] = {}

        # Group entities by barcode
        for entity in self.entity_map.values():
            barcode = entity['barcode']
            if barcode in barcode_map:
                if barcode not in duplicates:
                    duplicates[barcode] = [barcode_map[barcode]]
                duplicates[barcode].append(entity)
            else:
                barcode_map[barcode] = entity

        # Merge duplicates
        for barcode, entities in duplicates.items():
            merged = entities[0]
            merged.setdefault('provenance', []).append(merged.get('name'))
            merged.setdefault('conflicts', [])
            merged['merged_at'] = datetime.datetime.utcnow().isoformat() + 'Z'
            for dup in entities[1:]:
                dup.setdefault('provenance', []).append(dup.get('name'))
                for k, v in dup.items():
                    if k in ['children', 'parent_refs', 'provenance', 'conflicts', 'barcode', 'merged_into', 'merged_at']:
                        continue
                    strategy = merge_strategies.get(k, merge_strings)
                    old = merged.get(k, 'UNKNOWN')
                    new = strategy(old, v)
                    if old != new:
                        merged['conflicts'].append({'field': k, 'values': [old, v]})
                        logging.warning(f"[GOD] Conflict on '{k}' for barcode '{barcode}': '{old}' vs '{v}'. Using '{new}'.")
                        if self.strict:
                            input(f"Conflict on '{k}' for barcode '{barcode}': '{old}' vs '{v}'. Press Enter to continue...")
                        merged[k] = new
                merged['children'] = merge_lists(merged.get('children', []), dup.get('children', []))
                merged['parent_refs'] = merge_lists(merged.get('parent_refs', []), dup.get('parent_refs', []))
                for child in dup.get('children', []):
                    child['parent_refs'] = [merged if p == dup else p for p in child['parent_refs']]
                for parent in dup.get('parent_refs', []):
                    parent['children'] = [merged if c == dup else c for c in parent['children']]
                dup['merged_into'] = merged['name']
                merged['provenance'].extend(dup.get('provenance', []))
                logging.info(f"[GOD] Merged duplicate entity '{dup['name']}' into '{merged['name']}' (barcode: {barcode})")

        self.entity_map = {barcode: entity for barcode, entity in barcode_map.items()}
        logging.info(f"[GOD] Divine merging and deduplication complete. Unique entities: {len(self.entity_map)}")

    def initialize_prophet(self, model_name="gpt2"):
        """Initialize a Hugging Face text generation pipeline for prophecy."""
        self.prophet = pipeline("text-generation", model=model_name)

    def prophesy(self, prompt: str, context: Optional[Dict[str, Any]] = None, max_length: int = 120) -> str:
        """
        Generate a 'prophecy' (future prediction) based on the Book of Life and a prompt.
        Optionally include entity/system context for richer, more relevant predictions.
        """
        if not hasattr(self, "prophet"):
            self.initialize_prophet()
        context_str = ""
        if context:
            for k, v in context.items():
                context_str += f"{k}: {v}\n"
        full_prompt = f"{context_str}\n{prompt}".strip()
        result = self.prophet(full_prompt, max_length=max_length, num_return_sequences=1)
        return result[0]['generated_text']

    def batch_prophesy_for_entities(self, prompt_template: str, max_length: int = 120) -> None:
        """
        Generate and attach prophecies for all entities in the Book of Life.
        The prompt_template can use {name}, {role}, {status}, etc.
        """
        if not hasattr(self, "prophet"):
            self.initialize_prophet()
        for entity in self.entity_map.values():
            prompt = prompt_template.format(**entity)
            context = {
                "lineage": " > ".join([a for path in self.get_ancestry(entity['name']) for a in path]),
                "role": entity.get("role", ""),
                "status": entity.get("status", ""),
                "age": entity.get("age", ""),
            }
            prophecy = self.prophesy(prompt, context=context, max_length=max_length)
            entity["prophecy"] = prophecy

    def system_prophecy(self, prompt: str, max_length: int = 120) -> str:
        """
        Generate a system-wide prophecy using Book of Life metadata and summary.
        """
        summary = f"Entities: {len(self.entity_map)}\n"
        roles = set(e.get("role", "") for e in self.entity_map.values())
        summary += f"Roles: {', '.join(roles)}\n"
        return self.prophesy(prompt, context={"summary": summary}, max_length=max_length)

    def export_book_of_life(
        self,
        output_path: str,
        format: str = "json",
        fields: Optional[List[str]] = None,
        include_conflicts: bool = True,
        include_provenance: bool = True,
        compress: bool = False,
        version: Optional[str] = None,
        export_lineage: bool = False,
        post_export_hook: Optional[Callable[[str], None]] = None,
        include_prophecies: bool = False,
        prophecy_prompt_template: str = "Given the lineage and actions of {name}, the next event in their story will be",
        include_system_prophecy: bool = False,
        system_prophecy_prompt: str = "Given the current state of the Book of Life, the next major event will be"
    ):
        """
        Advanced export of the Book of Life.
        Supports multiple formats, field selection, conflict/provenance reporting, compression, and hooks.
        """
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        export_data = []
        for entity in self.entity_map.values():
            # Make a shallow copy for export
            record = entity.copy()
            # Replace object references with names only for export (do NOT modify the original entity)
            if 'parent_refs' in record:
                record['parent_refs'] = [p['name'] for p in record['parent_refs']]
            if 'children' in record:
                record['children'] = [c['name'] for c in record['children']]
            # Filter fields if specified
            if fields is not None:
                record = {k: v for k, v in record.items() if k in fields}
            if not include_conflicts:
                record.pop('conflicts', None)
            if not include_provenance:
                record.pop('provenance', None)
            export_data.append(record)

        # Add metadata
        metadata = {
            "exported_at": now,
            "entity_count": len(export_data),
            "version": version or now,
            "fields": fields or "all",
            "format": format,
        }

        # Write main export
        if format == "json":
            out_file = output_path
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump({"metadata": metadata, "entities": export_data}, f, ensure_ascii=False, indent=2)
        elif format == "csv":
            out_file = output_path
            fieldnames = fields or sorted({k for e in export_data for k in e.keys()})
            with open(out_file, "w", newline='', encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for entity in export_data:
                    row = {k: (json.dumps(v) if isinstance(v, (dict, list)) else v) for k, v in entity.items()}
                    writer.writerow(row)
        else:
            raise ValueError("Unsupported export format. Use 'json' or 'csv'.")

        # Export conflicts if requested
        if include_conflicts:
            conflicts = [
                {"entity": e.get("name"), "barcode": e.get("barcode"), "conflicts": e.get("conflicts", [])}
                for e in self.entity_map.values() if e.get("conflicts")
            ]
            if conflicts:
                conflicts_path = output_path.replace(".", "_conflicts.")
                with open(conflicts_path, "w", encoding="utf-8") as f:
                    json.dump(conflicts, f, ensure_ascii=False, indent=2)
                logging.info(f"[GOD] Conflict report written: {conflicts_path}")

        # Export provenance if requested
        if include_provenance:
            provenance = [
                {"entity": e.get("name"), "barcode": e.get("barcode"), "provenance": e.get("provenance", [])}
                for e in self.entity_map.values() if e.get("provenance")
            ]
            if provenance:
                provenance_path = output_path.replace(".", "_provenance.")
                with open(provenance_path, "w", encoding="utf-8") as f:
                    json.dump(provenance, f, ensure_ascii=False, indent=2)
                logging.info(f"[GOD] Provenance report written: {provenance_path}")

        # Export lineage/graph if requested
        if export_lineage:
            lineage = []
            for e in self.entity_map.values():
                for parent in e.get("parent_refs", []):
                    lineage.append({"child": e.get("name"), "parent": parent.get("name")})
            lineage_path = output_path.replace(".", "_lineage.")
            with open(lineage_path, "w", encoding="utf-8") as f:
                json.dump(lineage, f, ensure_ascii=False, indent=2)
            logging.info(f"[GOD] Lineage graph written: {lineage_path}")

        # Compression (optional)
        if compress:
            import shutil
            import gzip
            gz_path = out_file + ".gz"
            with open(out_file, "rb") as f_in, gzip.open(gz_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
            logging.info(f"[GOD] Compressed export written: {gz_path}")

        # Digital signature (optional)
        if getattr(self, "sign_exports", False):
            import hashlib
            with open(out_file, "rb") as f:
                signature = hashlib.sha256(f.read()).hexdigest()
            with open(out_file + ".sig", "w") as sigf:
                sigf.write(signature)

        # Post-export hook (optional)
        if post_export_hook:
            post_export_hook(out_file)

        logging.info(f"[GOD] Book of Life export complete: {out_file}")

    def export_lineage_graph(self, output_path: str):
        """Export lineage as a DOT file for visualization."""
        with open(output_path, "w") as f:
            f.write("digraph Lineage {\n")
            for entity in self.entity_map.values():
                for parent in entity.get('parent_refs', []):
                    f.write(f'"{parent["name"]}" -> "{entity["name"]}";\n')
            f.write("}\n")

    def decode_barcode(self, barcode: str) -> dict:
        """
        Decode a barcode into its components (lineage, name, role, status, etc.).
        Assumes the format: parent_barcode|name|role|status
        """
        parts = barcode.split("|")
        if len(parts) < 4:
            return {"error": "Invalid barcode format"}
        return {
            "parent_barcode": parts[0],
            "name": parts[1],
            "role": parts[2],
            "status": parts[3],
        }

    def export_to_database(self, db_path="book_of_life.db"):
        """
        Export all entities to a SQLite database using a dynamic SQLAlchemy ORM.
        """
        engine = create_engine(f"sqlite:///{db_path}")
        DynamicEntityORM = create_dynamic_entity_orm(self.entity_map, Base)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        for entity in self.entity_map.values():
            orm_entity = DynamicEntityORM(**entity)
            session.merge(orm_entity)
        session.commit()
        session.close()
        logging.info(f"[GOD] Book of Life exported to database: {db_path}")

    def convert_archetype_json_to_csv(self, archtypes_folder: str):
        """
        Discover all archetype_updated.json files in subfolders of archtypes_folder,
        and convert them to archetype_updated.csv in the same folder.
        """
        for subfolder in os.listdir(archtypes_folder):
            subfolder_path = os.path.join(archtypes_folder, subfolder)
            if os.path.isdir(subfolder_path):
                json_path = os.path.join(subfolder_path, "archetype_updated.json")
                if os.path.exists(json_path):
                    with open(json_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    # Try to get entities list, or treat as a single dict
                    entities = data.get("entities") if isinstance(data, dict) and "entities" in data else data
                    if isinstance(entities, dict):
                        entities = [entities]
                    if not isinstance(entities, list):
                        print(f"Skipping {json_path}: not a list of entities.")
                        continue
                    # Gather all unique fieldnames
                    fieldnames = set()
                    for entity in entities:
                        fieldnames.update(entity.keys())
                    fieldnames = list(fieldnames)
                    csv_path = os.path.join(subfolder_path, "archetype_updated.csv")
                    with open(csv_path, "w", newline='', encoding="utf-8") as f:
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                        for entity in entities:
                            writer.writerow(entity)
                    logging.info(f"[GOD] Converted {json_path} to {csv_path}")

    def load_entity_jsons(self, archtypes_folder: str):
        """
        Loads all .json entity files from each archetype subfolder (e.g., angelic, human, demonic).
        Stores them in self.entities[archetype_name] as lists.
        """
        self.entities = {}
        for subfolder in os.listdir(archtypes_folder):
            subfolder_path = os.path.join(archtypes_folder, subfolder)
            if os.path.isdir(subfolder_path):
                self.entities[subfolder] = []
                for filename in os.listdir(subfolder_path):
                    if filename.endswith(".json"):
                        json_path = os.path.join(subfolder_path, filename)
                        with open(json_path, "r", encoding="utf-8") as f:
                            try:
                                entity = json.load(f)
                                self.entities[subfolder].append(entity)
                            except Exception as e:
                                print(f"Error loading {json_path}: {e}")

    def load_entity_yaml(self, yaml_path):
        with open(yaml_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def discover_yaml_entities(self, root_folder):
        entities = []
        for dirpath, _, filenames in os.walk(root_folder):
            for filename in filenames:
                if filename.endswith(".yaml") or filename.endswith(".yml"):
                    entity = self.load_entity_yaml(os.path.join(dirpath, filename))
                    entities.append(entity)
        return entities

    def get_entities_list(self) -> list:
        """
        Return all unique entities as a list (for direct use in simulation).
        """
        if hasattr(self, "entity_map"):
            return list(self.entity_map.values())
        else:
            return []

    def get_entities_dict(self) -> dict:
        """
        Return all unique entities as a dict keyed by name (for direct use in simulation).
        """
        if hasattr(self, "entity_map"):
            return dict(self.entity_map)
        else:
            return {}

    def load_psyche_for_entity(self, entity):
        """
        Loads psyche.yaml for the entity's archetype (or subtype if present) and attaches it.
        Tries the most specific path first, then falls back to base.
        """
        archetype = entity.get("archetype", "humans")
        subtype = entity.get("subtype", None)
        name = entity.get("name", None)
        paths_to_try = []

        # Most specific: archetype/subtype/name/psyche.yaml
        if subtype and name:
            paths_to_try.append(
                os.path.join(self.archetypes_folder, archetype, subtype, name, "psyche.yaml")
            )
        # archetype/base/psyche.yaml
        paths_to_try.append(
            os.path.join(self.archetypes_folder, archetype, "base", "psyche.yaml")
        )
        # archetype/psyche.yaml (fallback)
        paths_to_try.append(
            os.path.join(self.archetypes_folder, archetype, "psyche.yaml")
        )

        for path in paths_to_try:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    entity["psyche"] = yaml.safe_load(f)
                return
        # If not found, attach an empty psyche
        entity["psyche"] = {}

    def attach_psyches(self):
        """
        Attach psyche.yaml data to every entity in the entity_map.
        """
        for entity in self.entity_map.values():
            self.load_psyche_for_entity(entity)

    def prompt_for_entity(archetypes_folder, existing_entities):
        name = input("Enter entity name: ").strip()
        # List available roles/archetypes
        roles = [d for d in os.listdir(archetypes_folder) if os.path.isdir(os.path.join(archetypes_folder, d))]
        print("Available roles/archetypes:")
        for idx, role in enumerate(roles):
            print(f"{idx+1}. {role}")
        role_idx = input("Pick a role by number: ").strip()
        try:
            role = roles[int(role_idx)-1]
        except (ValueError, IndexError):
            role = "base"

        # Parent selection
        print("Existing entities:", ", ".join(existing_entities.keys()))
        parent_input = input("Enter parent name(s) (comma-separated for two, leave blank for GOD/deadbeat): ").strip()
        if not parent_input:
            parent = "GOD" if name.lower() in ["adam", "eve", "progenitor"] else "deadbeat"
            parent_names = [parent]
        else:
            parent_names = [p.strip() for p in parent_input.split(",") if p.strip()]
            if not parent_names:
                parent_names = ["deadbeat"]

        entity = {
            "name": name,
            "role": role,
            "parent": ",".join(parent_names),
            "status": "active"
        }
        return entity, parent_names

# --- Main execution / wiring section ---

# 1. Initialize loader and discover/load all CSV data
loader = GodDataLoader(root_folder=r"C:\Users\storage\bookoflife\God\ancients", recursive=True, strict=True)
loader.discover_csv_files()
loader.load_all_data()

# 2. Validate and normalize all loaded data
loader.validate_and_normalize()

# 3. Build lineage map (parent/child relationships)
loader.build_lineage_map()

# 4. Attach psyche.yaml data to each entity
loader.attach_psyches()

# 5. Assign unique barcodes to all entities
loader.assign_barcodes()

# 6. Create a memory module (shared or per-entity)
memory_module = MemoryModule()
traits_config_path = "God/archetypes/humans/base/default_traits.yaml"  # Adjust as needed

# 7. Build entities dict and brains
entities_dict = loader.get_entities_dict()  # barcode → entity
entity_brains = {}

# 8. Build a name-to-barcode map for parent lookup
name_to_barcode = {entity['name']: barcode for barcode, entity in entities_dict.items()}

def amalgamate_brains(parent_brains):
    # Simple example: average numeric mental state values, merge traits
    if not parent_brains:
        return {}, {}
    base_state = {}
    count = len(parent_brains)
    keys = set().union(*(b.mental_state.keys() for b in parent_brains))
    for key in keys:
        vals = [b.mental_state.get(key) for b in parent_brains if isinstance(b.mental_state.get(key), (int, float))]
        if vals:
            base_state[key] = sum(vals) / len(vals)
        else:
            base_state[key] = parent_brains[0].mental_state.get(key)
    # For traits, you could merge or average as well
    base_traits = parent_brains[0].traits  # Or merge as needed
    return base_state, base_traits

# 9. Assign brains, with amalgamation if two parents exist
for barcode, entity in entities_dict.items():
    parent_names = [p.strip() for p in entity.get('parent', '').split(',') if p.strip()]
    parent_barcodes = [name_to_barcode[p] for p in parent_names if p in name_to_barcode]
    parent_brains = [entity_brains[b] for b in parent_barcodes if b in entity_brains]
    if len(parent_brains) == 2:
        amalgam_state, amalgam_traits = amalgamate_brains(parent_brains)
        brain = Brain(entity, memory_module, traits_config_path)
        brain.mental_state.update(amalgam_state)
        brain.traits.update(amalgam_traits)
    else:
        brain = Brain(entity, memory_module, traits_config_path)
    entity_brains[barcode] = brain
    entity["brain"] = brain

# 10. Export the Book of Life to JSON (after brains are assigned)
loader.export_book_of_life(
    "book_of_life.json",
    format="json",
    include_conflicts=True,
    include_provenance=True,
    compress=True
)
