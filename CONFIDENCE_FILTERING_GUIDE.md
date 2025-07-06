# Musiio Metadata Confidence Filtering Guide

This document explains the automatic confidence filtering feature in the Musiio to MP3Tag converter.

## Overview

The enhanced converter automatically filters Musiio metadata based on confidence scores, ensuring only reliable metadata is imported into MP3Tag. **Score fields are used for filtering but are NOT included in the final music metadata** - they remain as Musiio's internal confidence ratings and don't clutter your music files.

## How Confidence Filtering Works

### What are Musiio Scores?
Musiio provides a confidence score (0-100) for each metadata field it analyzes:
- **0-14**: Very low confidence - likely incorrect
- **15-29**: Low confidence - may be incorrect  
- **30-49**: Medium confidence - generally reliable
- **50-74**: High confidence - very reliable
- **75-100**: Highest confidence - extremely reliable

**Important Note**: Musiio tends to give lower scores for certain field types:
- **Energy/Vocal Presence**: Often scored 3-4 (very conservative)
- **BPM Variations**: Usually scored 1-2 (Musiio is uncertain about tempo variations)
- **Secondary Genres**: Often 20-30 range (alternative genre classifications)
- **Mood Variations**: Can be 15-25 (nuanced emotional analysis)

This is why a threshold of 30 works better than 50+ for most practical use cases.

### Automatic Filtering Process
1. **Score Analysis**: The converter examines each metadata field and its corresponding confidence score
2. **Threshold Filtering**: If the score is below your chosen threshold, that field is excluded from the final MP3Tag CSV
3. **Clean Output**: Only the actual metadata (not the scores) are included in the final CSV for music tagging

### What Gets Included vs. Excluded
**✅ Included in Music Metadata:**
- All music-relevant fields (genre, mood, key, BPM, etc.)
- Only fields that pass the confidence threshold
- Standard MP3 tag fields (title, artist, album, etc.)

**❌ Excluded from Music Metadata:**
- All score/confidence fields (these are just for filtering)
- Low-confidence metadata below your threshold
- Musiio's internal analysis ratings

## Usage Examples

### Command Line
```bash
# Use default threshold (50)
python musiio_to_mp3tag_converter.py musiio-export.csv

# Use high confidence threshold (75)
python musiio_to_mp3tag_converter.py musiio-export.csv --threshold 75

# Use very strict threshold (90)
python musiio_to_mp3tag_converter.py musiio-export.csv -t 90

# Custom output file
python musiio_to_mp3tag_converter.py musiio-export.csv -t 75 -o filtered_output.csv
```

### PowerShell Automation
```powershell
# Use default threshold (50)
.\Import-Musiio-Metadata.ps1

# Use high confidence threshold (75)
.\Import-Musiio-Metadata.ps1 -ScoreThreshold 75

# Specify CSV and threshold
.\Import-Musiio-Metadata.ps1 -MusiioCSV "path\to\file.csv" -ScoreThreshold 90
```

## Threshold Recommendations

### Balanced Approach (Recommended: 30-40)
For most use cases, a moderate threshold provides good quality while preserving useful metadata:
- **30**: Balanced default - filters obvious low-confidence data while keeping useful information
- **35**: Slightly more conservative 
- **40**: Good quality control without being too strict

### Professional Music Production (Recommended: 50-75)
For commercial releases where accuracy is critical:
- **50**: Professional quality threshold
- **60-65**: High standards for metadata accuracy
- **70-75**: Very strict quality control

### Permissive Approach (Recommended: 15-25)
For personal collections or when you want more complete metadata:
- **15**: Include most metadata, filter only obvious errors
- **20**: Light filtering
- **25**: Minimal quality control

### Research/Analysis (Recommended: 0-10)
For testing or research where you want to see all available data:
- **0**: No filtering, includes all metadata
- **5-10**: Remove only the most uncertain data

## Filtering Results

The converter provides detailed feedback about filtering:

```
📊 Filtering summary: 265 fields filtered out of 1036 total fields
   (25.6% filtered due to low confidence scores)
```

This tells you:
- How many fields were filtered out
- The total number of metadata fields analyzed
- The percentage of data that was filtered

## Real-World Examples

### Example 1: Strict Professional Use (Threshold 75)
```
Input: 1036 metadata fields
Filtered: 265 fields (25.6%)
Result: 771 high-confidence fields imported
```

Typical filtered fields:
- Alternative genre classifications with low scores
- Uncertain key signatures
- Low-confidence energy/mood variations
- Questionable vocal presence assessments

### Example 2: Balanced Personal Use (Threshold 50)
```
Input: 1036 metadata fields  
Filtered: 227 fields (21.9%)
Result: 809 reliable fields imported
```

Includes more metadata while still filtering obvious uncertainties.

### Example 3: Minimal Filtering (Threshold 25)
```
Input: 1036 metadata fields
Filtered: ~150 fields (14.5%)
Result: ~886 fields imported
```

Includes most metadata, only filtering the most uncertain data.

## Fields Always Included

These core fields are always included regardless of threshold:
- **Filename** - Required for MP3Tag import
- **Title** - Song title from Musiio
- **Artist** - Artist name from Musiio
- **Album Artist** - Set to "Elemental Publishing"
- **Album** - Set to "Elemental Publishing"
- **Year** - Set to "2025"

## Understanding Filtered Output

When the converter runs, you'll see filtered fields logged:
```
Filtered quality: medium (score: 69.0 < 75)
Filtered mood: angry (score: 64.0 < 75)
Filtered keysharp: C minor (score: 39.0 < 75)
```

This means:
- The quality was assessed as "medium" with 69% confidence (filtered out)
- The mood was "angry" with 64% confidence (filtered out)
- The key was "C minor" with only 39% confidence (filtered out)

## Best Practices

### 1. Start Conservative
Begin with a threshold of 75 for professional work, then adjust based on results.

### 2. Review Filtered Data
Check the filtered output to see what's being excluded. If important metadata is filtered, lower the threshold.

### 3. Different Thresholds for Different Uses
- **Master recordings**: Use 75-90
- **Work-in-progress**: Use 50-75
- **Experimental**: Use 25-50

### 4. Validate Results
Use the verification script to confirm tags are correctly applied:
```bash
python verify_mp3_tags.py "path\to\music\folder"
```

### 5. Test Different Thresholds
Use the test batch file to see how different thresholds affect your specific music:
```bash
test-filtering.bat
```

## Troubleshooting

### Too Little Metadata
If too much is being filtered:
- Lower the threshold (try 50 or 40)
- Check if your music style has inherently lower confidence scores
- Consider that some genres are harder for AI to analyze

### Too Much Uncertain Metadata
If questionable metadata is getting through:
- Raise the threshold (try 75 or 80)
- Review the filtered output logs to understand what's being excluded
- Remember that some uncertainty is normal in AI analysis

### No Metadata for Certain Fields
Some fields like vocal gender or specific instruments may have consistently low scores:
- This is normal for instrumental tracks (vocal fields)
- Complex instrumentation may have lower confidence
- Electronic music may have different confidence patterns than acoustic

## Technical Details

### Score Field Mapping
The converter automatically detects score fields by looking for pattern:
- Field: `GENRE` → Score: `GENRE SCORE`
- Field: `MOOD` → Score: `MOOD SCORE`
- Field: `INSTRUMENT` → Score: `INSTRUMENT SCORE`

### Score Validation
- Invalid scores (non-numeric) result in the field being included
- Missing score fields result in the field being included
- Only valid numeric scores 0-100 are used for filtering

### Field Processing Order
1. Parse CSV header to identify fields and their score columns
2. Process each row of metadata
3. For each field, check if it has a corresponding score
4. Apply threshold filter if score exists
5. Clean and include field if it passes the filter

## Technical Details

### Clean Metadata Output
The converter produces MP3Tag CSV files that contain **only music metadata** - no confidence scores or internal analysis data. This ensures:
- Clean music files without unnecessary technical data
- Standard MP3 metadata fields that work with all players
- Professional appearance in music library software

### Score Field Processing
- Score fields are parsed and used for filtering decisions
- They are never included in the final MP3Tag import CSV
- The filtering process is transparent with detailed logging

This filtering system ensures you get the most reliable metadata for your music production workflow while maintaining clean, professional music files without any Musiio analysis artifacts.
