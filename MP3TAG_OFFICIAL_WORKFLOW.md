# MP3Tag CSV Import - Official Documentation Summary

## The Correct Method (Based on Official MP3Tag Docs)

According to the official MP3Tag documentation at [docs.mp3tag.de](https://docs.mp3tag.de/converters/import-tags-from-text-files), the correct way to import CSV metadata is:

### Menu Path
**Convert → Text file - Tag (Import)**
- Keyboard shortcut: Alt+4
- NOT the File menu (which may not exist in newer versions)

### How It Works
1. **Sequential Matching**: MP3Tag matches files in your File List with CSV rows in order
   - First selected file gets first CSV row
   - Second selected file gets second CSV row
   - And so on...

2. **Header Handling**: The Convert → Text file - Tag method automatically handles CSV headers correctly
   - No need for "First line contains field names" checkbox
   - No data offset issues

3. **Format String**: Uses MP3Tag's format string syntax to map CSV columns to tag fields
   - `%dummy%` for columns to ignore
   - `%title%`, `%artist%`, etc. for tag fields
   - Comma-separated for CSV files

### Our Professional Setup
All three album CSVs are ready:
- `elemental_publishing_type1_mp3tag_ready.csv` (Type One album)
- `elemental_publishing_striptape_mp3tag_ready.csv` (Strip Tape album)  
- `elemental_publishing_newmatrix_mp3tag_ready.csv` (New Matrix album)

Each contains:
- Core metadata (title, artist, album, etc.)
- Professional identifiers (ISRC, copyright, publisher)
- AI-enhanced discovery data (genre, mood, BPM, key, energy)
- Industry-standard numbering (IPI, UPC in comments)

### Format String
```
%dummy%,%title%,%artist%,%albumartist%,%album%,%track%,%year%,%dummy%,%dummy%,%genre%,%dummy%,%dummy%,%dummy%,%mood%,%dummy%,%dummy%,%bpm%,%dummy%,%dummy%,%initialkey%,%dummy%,%dummy%,%dummy%,%dummy%,%dummy%,%energy%,%dummy%,%dummy%,%dummy%,%dummy%,%dummy%,%dummy%,%dummy%,%dummy%,%comment%,%copyright%,%publisher%,%isrc%,%dummy%,%dummy%,%dummy%
```

## Sources
- [MP3Tag Converters Documentation](https://docs.mp3tag.de/converters/import-tags-from-text-files)
- [MP3Tag Convert Menu](https://docs.mp3tag.de/menus/convert)
- [MP3Tag Format Strings](https://docs.mp3tag.de/format)

This method is the official, documented approach and should work reliably across all MP3Tag versions.
