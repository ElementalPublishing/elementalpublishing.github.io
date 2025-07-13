import re
from pathlib import Path

PROMPT_SECTIONS = ["image_prompt", "llm_prompt"]
ENTITY_HEADER = re.compile(r"^entity_id:\s*\"?(.*?)\"?$", re.MULTILINE)
NAME_HEADER = re.compile(r"^name:\s*\"?(.*?)\"?$", re.MULTILINE)
DYNASTY_PATTERN = re.compile(r"cyberdynasties\\([^\\]+)")


def extract_sections(md_text, section_names):
    results = {name: None for name in section_names}
    # Only consider headers with at least 2 #'s (##, ###, etc), but not single #
    header_pattern = re.compile(r"^(#{2,6})\s*([a-zA-Z0-9_]+)\s*$", re.MULTILINE)
    headers = list(header_pattern.finditer(md_text))
    section_indices = {h.group(2).lower(): i for i, h in enumerate(headers)}
    for section in section_names:
        idx = section_indices.get(section.lower())
        if idx is not None:
            start = headers[idx].end()
            # Find the next header of same or higher level (## or more)
            for j in range(idx + 1, len(headers)):
                if len(headers[j].group(1)) <= len(headers[idx].group(1)):
                    end = headers[j].start()
                    break
            else:
                end = len(md_text)
            # Only take the content up to the next header of same or higher level
            results[section] = md_text[start:end].strip()
    return results


def get_entity_info(md_text, file_path):
    name = None
    entity_id = None
    dynasty = None
    subfolder = None
    # Try to extract from file content
    m = NAME_HEADER.search(md_text)
    if m:
        name = m.group(1)
    m = ENTITY_HEADER.search(md_text)
    if m:
        entity_id = m.group(1)
    # Try to extract dynasty and subfolder from path
    path_str = str(file_path)
    m = DYNASTY_PATTERN.search(path_str)
    if m:
        dynasty = m.group(1).replace('_', ' ').title()
        # subfolder is next folder after dynasty
        parts = path_str.split('cyberdynasties'+"\\")[-1].split('\\')
        if len(parts) > 1:
            subfolder = parts[0].replace('_', ' ').title()
    return dynasty, subfolder, name, entity_id, path_str




def main():
    entities_dir = Path("entities")
    output_path = entities_dir / "PROMPTS.md"
    all_md_files = list(entities_dir.rglob("*.md"))
    output_lines = ["# PROMPTS\n", "This file contains extracted image and LLM prompts for all entities, grouped by dynasty, subfolder, and entity name. Maximum Bosses are listed first.\n\n"]
    # Structure: {dynasty: {subfolder: {"max_bosses": [..], "others": [..]}}}
    prompts_by_dynasty = {}

    for md_file in all_md_files:
        md_text = md_file.read_text(encoding="utf-8")
        sections = extract_sections(md_text, PROMPT_SECTIONS)
        if not any(sections.values()):
            continue  # skip files with no prompts
        dynasty, subfolder, name, entity_id, path_str = get_entity_info(md_text, md_file)
        if not dynasty:
            dynasty = "Unknown Dynasty"
        if not subfolder:
            subfolder = "Other"
        if not name:
            name = md_file.stem
        if dynasty not in prompts_by_dynasty:
            prompts_by_dynasty[dynasty] = {}
        if subfolder not in prompts_by_dynasty[dynasty]:
            prompts_by_dynasty[dynasty][subfolder] = {"max_bosses": [], "others": []}
        is_max_boss = "bosses\\maximumboss" in path_str.lower()
        entry = (name, sections)
        if is_max_boss:
            prompts_by_dynasty[dynasty][subfolder]["max_bosses"].append(entry)
        else:
            prompts_by_dynasty[dynasty][subfolder]["others"].append(entry)

    for dynasty in sorted(prompts_by_dynasty):
        output_lines.append(f"## {dynasty}\n")
        for subfolder in sorted(prompts_by_dynasty[dynasty]):
            output_lines.append(f"### {subfolder}\n")
            # Maximum Bosses first
            max_bosses = prompts_by_dynasty[dynasty][subfolder]["max_bosses"]
            if max_bosses:
                output_lines.append(f"#### Maximum Bosses\n")
                for name, sections in sorted(max_bosses, key=lambda x: x[0]):
                    output_lines.append(f"##### {name}\n")
                    for section in PROMPT_SECTIONS:
                        output_lines.append(f"###### {section}\n")
                        if sections[section]:
                            output_lines.append(sections[section] + "\n")
                        else:
                            output_lines.append("(Section not found)\n")
                    output_lines.append("\n")
            # Other entities
            others = prompts_by_dynasty[dynasty][subfolder]["others"]
            if others:
                output_lines.append(f"#### Other Entities\n")
                for name, sections in sorted(others, key=lambda x: x[0]):
                    output_lines.append(f"##### {name}\n")
                    for section in PROMPT_SECTIONS:
                        output_lines.append(f"###### {section}\n")
                        if sections[section]:
                            output_lines.append(sections[section] + "\n")
                        else:
                            output_lines.append("(Section not found)\n")
                    output_lines.append("\n")
    output_path.write_text("\n".join(output_lines), encoding="utf-8")
    print(f"Extracted prompts written to {output_path}")

if __name__ == "__main__":
    main()
