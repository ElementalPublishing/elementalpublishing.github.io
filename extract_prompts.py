import sys
import re
from pathlib import Path

def extract_sections(md_text, section_names):
    """
    Extracts sections from markdown text based on section headers (e.g., ## image_prompt).
    Returns a dict of section_name: content.
    """
    results = {name: None for name in section_names}
    # Regex for section headers (## image_prompt)
    pattern = re.compile(r"^##\s*({})\s*$".format("|".join(map(re.escape, section_names))), re.MULTILINE | re.IGNORECASE)
    matches = list(pattern.finditer(md_text))
    for i, match in enumerate(matches):
        section = match.group(1).lower()
        start = match.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(md_text)
        results[section] = md_text[start:end].strip()
    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_prompts.py <markdown_file>")
        sys.exit(1)
    md_path = Path(sys.argv[1])
    if not md_path.exists():
        print(f"File not found: {md_path}")
        sys.exit(1)
    md_text = md_path.read_text(encoding="utf-8")
    # Section names to extract
    section_names = ["image_prompt", "llm_prompt"]
    results = extract_sections(md_text, section_names)
    for name in section_names:
        print(f"===== {name.upper()} =====")
        if results[name]:
            print(results[name])
        else:
            print("(Section not found)")
        print()

if __name__ == "__main__":
    main()
