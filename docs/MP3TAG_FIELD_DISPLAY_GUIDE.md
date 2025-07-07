# MP3Tag Musiio Field Display Setup Guide

## 🎯 Problem: MP3Tag doesn't show all imported Musiio fields by default

After importing your Musiio CSV, the data IS in your MP3 files, but MP3Tag only shows standard fields by default. Here's how to see everything:

## 🔧 Method 1: Use the Enhanced Template (Recommended)

### Step 1: Load the Enhanced Template
1. Open MP3Tag
2. Go to **View > Customize Columns**
3. Click **Load**
4. Select `ElementalPublishing_Complete_Enhanced.mte`
5. Click **Load**
6. ✅ **All 60+ Musiio fields are now visible!**

## 🔧 Method 2: Manual Column Configuration

### Add Individual Columns:
1. Right-click on any column header
2. Select **Customize Columns**
3. Click **New** to add custom columns
4. Add these key Musiio fields:

**Essential Musiio Fields to Add:**
```
Field Name: CONTENTTYPE     | Display Name: Content Type
Field Name: QUALITY         | Display Name: Quality  
Field Name: GENRESECONDARY  | Display Name: Genre 2
Field Name: MOOD            | Display Name: Mood
Field Name: MOODVALENCE     | Display Name: Valence
Field Name: ENERGY          | Display Name: Energy
Field Name: VOCALGENDER     | Display Name: Vocal
Field Name: KEY             | Display Name: Key
Field Name: BPMALT          | Display Name: BPM Alt
```

## 🔧 Method 3: Tag Panel Configuration

### Show Fields in the Tag Panel:
1. Go to **Tools > Options**
2. Select **Tag Panel** 
3. Click **New** to add fields
4. Add these custom fields:

```
CONTENTTYPE (Content Type)
CONTENTSCORE (Content Score)
QUALITY (Quality Level) 
QUALITYSCORE (Quality Score)
GENRESECONDARY (Secondary Genre)
GENREV3 (Genre V3)
MOOD (Primary Mood)
MOODSECONDARY (Secondary Mood)
MOODVALENCE (Mood Valence)
ENERGY (Energy Level)
VOCALPRESENCE (Vocal Presence)
VOCALGENDER (Vocal Gender)
KEY (Primary Key)
KEYSECONDARY (Secondary Key)
BPM (Tempo)
BPMALT (BPM Alternative)
INSTRUMENTATION (Instrumentation)
INSTRUMENT1 (Instrument 1)
```

## 🔍 Method 4: Extended Tags View

### See ALL tags in a file:
1. Select any MP3 file in MP3Tag
2. Go to **View > Extended Tags** (or press Alt+T)
3. ✅ **This shows EVERY tag in the file, including all Musiio data**

## 🧪 Method 5: Verification Tool

### Use our Python verification script:
```bash
# Install required library
pip install mutagen

# Check a single file
python verify_mp3_tags.py "path/to/your/song.mp3"

# Check entire folder
python verify_mp3_tags.py "path/to/your/music/folder"
```

This will show you exactly which Musiio fields are present and their values.

## 🎵 Expected Results After Import

After successful import, you should see:

### ✅ **Standard Fields:**
- Title, Artist, Album Artist, Album, Year
- Genre (from Musiio primary genre)

### ✅ **Musiio Analysis Fields:**
- **Content**: Content Type, Content Score, Quality, Quality Score
- **Genre**: Secondary Genre, Genre V3, Genre V3 Alt (with scores)
- **Mood**: Primary Mood, Secondary Mood, Mood Valence (with scores)
- **Tempo**: BPM, BPM Alt, BPM Variation (with scores)
- **Key**: Primary Key, Secondary Key, Sharp/Flat variants (with scores)
- **Energy**: Energy Level, Energy Variation (with scores)
- **Vocal**: Vocal Presence, Vocal Gender (with scores)
- **Instruments**: Instrumentation, Individual Instruments 1-4 (with scores)

## 🚨 Troubleshooting: If Fields Don't Show

### 1. Check CSV Import was Successful:
- Go to **View > Extended Tags**
- Look for fields starting with your Musiio data
- Should see 40+ custom TXXX fields

### 2. Verify CSV Format:
- Check that CSV has proper headers
- Ensure no empty rows at top
- Verify filename matching

### 3. Re-import Process:
```bash
# Regenerate CSV
python musiio_to_mp3tag_converter.py "your_musiio_file.csv"

# In MP3Tag:
# File > Import Tag Fields from CSV...
# Select the _mp3tag_ready.csv file
# Check "Import all columns"
```

### 4. Manual Field Check:
- Select an MP3 file
- Press **Ctrl+Q** to open Quick Actions
- Type field names to see if they exist

## 🎯 For Elemental Publishing Workflow

### Recommended View Setup:
1. **Main Columns**: Filename, Title, Artist, Album Artist, Genre, Mood, Energy, Key, BPM
2. **Extended View**: Use template for full analysis data
3. **Tag Panel**: Show key fields for editing

### Business Benefits:
- ✅ **Quality Control**: See Musiio quality scores
- ✅ **Genre Accuracy**: Multiple genre classifications
- ✅ **Mood Targeting**: Precise mood data for playlists
- ✅ **Professional Metadata**: Industry-standard comprehensive tagging
- ✅ **Fan Discovery**: Rich metadata improves searchability

## 💡 Pro Tips

1. **Save Custom Views**: After setup, save your column configuration
2. **Export Templates**: Share templates across multiple computers
3. **Batch Editing**: Use the Tag Panel to edit multiple files at once
4. **Search by Musiio Data**: Use filters to find songs by mood, energy, etc.

**Remember**: The data IS there after import - you just need to configure MP3Tag to show it!
