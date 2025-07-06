# MP3Tag Action to Set Composer Field

After importing your CSV metadata, you can set the Composer field using MP3Tag Actions:

## Method 1: Manual Entry
1. Select all files in MP3Tag
2. In the Tag Panel, find the "Composer" field
3. Enter: `Wesley Alexander Houser`
4. Press Enter to apply to all selected files

## Method 2: Using Actions (Automated)
1. Go to Actions → New Action
2. Action type: Format value
3. Field: COMPOSER  
4. Format string: `Wesley Alexander Houser`
5. Save as "Set Composer to Wesley Alexander Houser"
6. Run this action on all imported files

## Method 3: Copy from Copyright
If you want to extract the composer from the copyright field:
1. Actions → New Action
2. Action type: Format value
3. Field: COMPOSER
4. Format string: `$regexp(%copyright%,© \d+ (.+),\1)`
5. This extracts "Wesley Alexander Houser" from "© 2025 Wesley Alexander Houser"

This ensures all your tracks have proper composer credits for royalty collection and professional metadata standards.
