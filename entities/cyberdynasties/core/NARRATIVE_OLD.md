# NARRATIVE.md

## Using Obsidian for Story and Memory Template Contribution

### 1. Writing in Obsidian

- Writers create or edit Markdown (`.md`) files in Obsidian.
- Use a clear structure for memory templates or story fragments, for example:

  ```markdown
  ## Angelic Memory Templates
  - Once, my wings shimmered with the dawn...
  - I sang in the choirs of heaven, but my voice is now a whisper in the void.

  ## Human Memory Templates
  - I walked the earth and tasted both joy and sorrow.
  - My days were numbered, but my dreams were infinite.
  ```

- Each section (with `## ... Memory Templates`) is for a different archetype or category.
- Each bullet point (`- ...`) is a memory template or story fragment.

---

### 2. How Obsidian Handles It

- Obsidian saves each note as a plain Markdown file (`.md`) in your vault (a folder on your computer).
- Writers can use Obsidian’s features (links, tags, search, etc.) to organize and cross-reference templates, stories, and lore.
- Markdown files are easy to read, edit, and version-control (e.g., with Git).

---

### 3. Where Do the Files Go?

- The `.md` files are stored in your Obsidian vault, which is just a folder (e.g., `C:\Users\storage\ObsidianVault\`).
- When you want to use the content in your system:
  1. **Copy or reference** the relevant `.md` file(s) from your vault.
  2. **Run your extraction script** (like `md_templates_to_yaml.py`) to convert the Markdown into YAML or CSV.
  3. **Place the generated YAML/CSV** in the appropriate location in your project (e.g., `God/memory_templates.yaml` or inside an archetype folder).
  4. **(Optional)** Convert YAML to JSON if your system needs it.

---

### 4. Workflow Summary Table

| Step                | What the Writer Does         | What Happens Next                        |
|---------------------|-----------------------------|------------------------------------------|
| Write in Obsidian   | Drafts templates in .md     | File saved in Obsidian vault             |
| Export/Extract      | (Dev runs script)           | Markdown converted to YAML/CSV           |
| Integrate           | Place YAML/CSV in project   | System loads new templates automatically |

---

**In short:**  
Writers use Obsidian for creative work.  
You (or a dev) extract and convert their Markdown to YAML/CSV, then drop it into your system—making collaboration seamless and empowering creative contributors!