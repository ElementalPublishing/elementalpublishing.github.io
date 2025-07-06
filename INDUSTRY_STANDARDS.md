# Industry Standard Metadata & File Organization

## Industry Standard ID3 Tags (Critical)

### Required Fields:
```
ARTIST: Elemental Publishing (or artist name)
ALBUM: Type 1
TITLE: Track Name
TRACK: 01/10 (track number / total tracks)
YEAR: 2025
GENRE: Hip Hop / Electronic / etc.
```

### Professional Fields:
```
ALBUMARTIST: Elemental Publishing
COMPOSER: [Your Name]
PUBLISHER: Elemental Publishing
COPYRIGHT: © 2025 Elemental Publishing
ISRC: [International Standard Recording Code - if you have them]
UPC/EAN: [Universal Product Code for the album]
```

### Industry-Specific Fields:
```
BPM: [Beats per minute - important for sync/DJ use]
KEY: [Musical key - A minor, C major, etc.]
MOOD: [Aggressive, Chill, Dark, etc.]
COMMENT: Contact: houser2388@gmail.com
```

## File Naming Standards

### Track Files (Industry Standard):
```
01 Track Name.mp3
02 Track Name.mp3
...
10 Track Name.mp3
```
**OR**
```
Artist - Album - 01 - Track Name.mp3
Artist - Album - 02 - Track Name.mp3
```

### Technical Specs (Non-Negotiable):
- **320kbps CBR MP3** (industry minimum for digital sales)
- **44.1kHz/16-bit** (CD quality standard)
- **No clipping** (peaks under -0.1dB)
- **Consistent LUFS** (-14 LUFS for streaming, -9 to -12 for club/sync)

## Album Package Structure (Professional)

```
ELEMENTALPUBLISHING_TYPE1_MASTERS_V1/
├── 01 Track Name.mp3
├── 02 Track Name.mp3
├── ...
├── 10 Track Name.mp3
├── album_cover.jpg (1400x1400px minimum)
├── album_info.txt
├── credits.txt
└── metadata.csv (for industry use)
```

## Industry Metadata Standards

### ISRC Codes (International Standard Recording Code):
- **Format:** CC-XXX-YY-NNNNN
- **Example:** US-ABC-25-12345
- **Purpose:** Unique identifier for each track (used by PROs, streaming, radio)
- **Get them from:** Your local recording rights organization

### UPC/EAN Codes (Album identifiers):
- **Format:** 12-digit barcode
- **Purpose:** Album identification for sales/distribution
- **Get them from:** GS1 or your distributor

### Mechanical Rights Info:
```
PUBLISHER: Elemental Publishing
SONGWRITER: [Your Name]
PUBLISHING %: 100%
MASTER OWNER: Elemental Publishing
```

## Pro-Level Metadata Template

### metadata.csv (for industry submissions):
```csv
Track,Title,Artist,Album,ISRC,BPM,Key,Duration,Composer,Publisher
01,"Track Name","Elemental Publishing","Type 1","US-ABC-25-12345",120,"A minor","3:45","Your Name","Elemental Publishing"
02,"Track Name 2","Elemental Publishing","Type 1","US-ABC-25-12346",115,"C major","4:12","Your Name","Elemental Publishing"
```

### album_info.txt (industry format):
```
ALBUM: Type 1
ARTIST: Elemental Publishing
LABEL: Elemental Publishing
CATALOG #: EP001
RELEASE DATE: 2025
UPC: 123456789012
GENRE: Electronic/Hip Hop
TOTAL RUNTIME: 38:45
CONTACT: houser2388@gmail.com
WEBSITE: elementalpublishing.github.io/website

MASTERED FOR: Digital Release
SAMPLE RATE: 44.1kHz/16-bit
FORMAT: 320kbps MP3

PUBLISHING: 100% Elemental Publishing
MASTER OWNERSHIP: 100% Elemental Publishing
TERRITORY: Worldwide
```

## Automation Strategy

### Phase 1: Template System
1. **Excel/CSV template** with all your standard info
2. **MP3Tag action** to batch apply from CSV
3. **PowerShell script** to auto-organize files

### Phase 2: Full Pipeline
1. **Audio files in** → **Metadata applied** → **Files organized** → **ZIP created**
2. **One command** processes entire album

## Industry Benefits

### For Sync/Licensing:
- **BPM/Key tags** = easier music searches
- **ISRC codes** = proper royalty tracking
- **Professional metadata** = taken seriously by supervisors

### For A&Rs/Labels:
- **Consistent formatting** = shows professionalism
- **Complete rights info** = faster deal evaluation
- **Industry-standard files** = ready for distribution

### For Radio/DJ Use:
- **BPM tags** = DJ software compatibility
- **Consistent levels** = broadcast ready
- **Proper naming** = easy library management

## The Hard Truth

**Most independent artists skip this stuff** and it shows. Having industry-standard metadata and organization immediately signals that you're a professional operation, not a hobby project.

**This is what separates** artists who get sync deals, label attention, and radio play from those who don't.

**Investment required:**
- ISRC codes: ~$2-5 per track
- UPC code: ~$30 for the album
- Time to implement proper workflow: ~4-8 hours initially
- **Payoff:** Taken seriously by industry professionals

Want to tackle this systematically? We can build the automation around proper industry standards from day one.
