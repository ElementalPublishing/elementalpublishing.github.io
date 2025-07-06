# Album Package Preparation Guide

## File Organization Checklist

### 1. Album Artwork Specifications

**Primary Album Cover:**
- **Size:** 1400x1400px (minimum) - 3000x3000px (ideal)
- **Format:** PNG or high-quality JPG
- **DPI:** 300 DPI for print quality
- **Color:** RGB color space
- **File name:** `album_cover.png` or `album_cover.jpg`

**Thumbnail/Web Version:**
- **Size:** 600x600px (for website display)
- **Format:** JPG (optimized for web)
- **File name:** `album_cover_web.jpg`

### 2. Audio File Standards

**MP3 Specifications:**
- **Bitrate:** 320kbps CBR (Constant Bit Rate)
- **Sample Rate:** 44.1kHz
- **Format:** MP3
- **Metadata:** Properly tagged (Artist, Album, Track Number, Title, Year)

**Optional FLAC (Premium):**
- **Format:** FLAC lossless
- **Sample Rate:** 44.1kHz or higher
- **Bit Depth:** 16-bit minimum, 24-bit preferred

### 3. File Naming Convention

**Album ZIP File:**
```
ELEMENTALPUBLISHING_[ALBUM_NAME]_MASTERS_V1.zip
```

**Examples:**
- `ELEMENTALPUBLISHING_TYPE1_MASTERS_V1.zip`
- `ELEMENTALPUBLISHING_STRIPTAPE_MASTERS_V1.zip`
- `ELEMENTALPUBLISHING_NEWMATRIX_MASTERS_V1.zip`

**Individual Track Naming:**
```
01_Track_Name.mp3
02_Track_Name.mp3
...
10_Track_Name.mp3
```

### 4. ZIP Package Structure

```
ELEMENTALPUBLISHING_TYPE1_MASTERS_V1/
├── album_cover.png              (1400x1400px+)
├── album_cover_web.jpg          (600x600px)
├── 01_Opening_Track.mp3         (320kbps)
├── 02_Second_Track.mp3          (320kbps)
├── 03_Third_Track.mp3           (320kbps)
├── ...
├── 10_Final_Track.mp3           (320kbps)
├── credits.txt                  (Optional: Credits, lyrics, notes)
└── README.txt                   (Instructions for the fan)
```

### 5. Additional Files (Optional but Professional)

**credits.txt Example:**
```
TYPE 1 - Credits

Produced by: [Your Name]
Mixed by: [Your Name]
Mastered by: [Your Name]
Artwork by: [Artist Name]

All tracks © 2025 Elemental Publishing
Contact: houser2388@gmail.com

Track Listing:
01. Opening Track
02. Second Track
...
10. Final Track

Thank you for supporting independent music!
```

**README.txt Example:**
```
Thank you for purchasing TYPE 1!

This package contains:
- 10 high-quality MP3 tracks (320kbps)
- Album artwork (high resolution)
- Credits and information

Instructions:
1. Extract this ZIP file to your desired location
2. Import tracks to your music library
3. Enjoy your music!

Support:
- Email: houser2388@gmail.com
- Website: elementalpublishing.github.io/website

Follow us:
- SoundCloud: soundcloud.com/elementalpublishing
- Instagram: @elementalpublishing

© 2025 Elemental Publishing. All rights reserved.
```

## Quick Checklist Before Packaging

### Audio Quality Check:
- [ ] All tracks are 320kbps MP3
- [ ] No clipping or distortion
- [ ] Consistent volume levels
- [ ] Proper fade-ins/fade-outs
- [ ] ID3 tags filled out completely

### Artwork Check:
- [ ] Album cover is high resolution (1400x1400px+)
- [ ] Web version created (600x600px)
- [ ] Colors look good on different screens
- [ ] Text is readable at small sizes
- [ ] File formats are correct (PNG/JPG)

### File Organization Check:
- [ ] All files named consistently
- [ ] Track numbers are correct (01, 02, 03...)
- [ ] No duplicate files
- [ ] ZIP file named according to convention
- [ ] All files work/open properly

### Professional Touch:
- [ ] Credits file included
- [ ] README with instructions
- [ ] Contact information provided
- [ ] Thank you message to fans
- [ ] Legal copyright notice

## Tools You Might Need

**For Audio:**
- Audacity (free) - for basic editing/export
- Adobe Audition - professional audio editing
- Any DAW with MP3 export at 320kbps

**For Artwork:**
- GIMP (free) - image editing
- Photoshop - professional image editing
- Canva - for simple designs
- Online image resizers for web versions

**For Metadata:**
- MP3Tag (free) - for editing ID3 tags
- Foobar2000 - music player with tag editing
- iTunes - can edit basic tags

## Ready to Package?

Once you have everything organized:
1. Create the folder structure above
2. ZIP the entire folder
3. Test the ZIP file (extract and verify)
4. Upload to GitHub Releases
5. Update download URLs in your website

**Take your time with this step - professional packaging makes a huge difference in perceived value!**
