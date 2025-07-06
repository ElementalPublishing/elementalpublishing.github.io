# SoundCloud Integration Setup

## Overview
The website now has a fully functional SoundCloud preview system! When visitors click "Preview" on any album, they'll see a modal with an embedded SoundCloud player.

## What You Need to Do

### 1. Get Your SoundCloud Playlist URLs
For each album, you need:
- The public SoundCloud playlist URL (e.g., `https://soundcloud.com/your-account/sets/album-name`)
- The playlist ID for embedding

### 2. Update the Album Data in script.js

Open `script.js` and find the `albumData` object (around line 134). Replace the placeholder URLs with your actual SoundCloud data:

```javascript
const albumData = {
    'type-1': {
        title: 'Type 1',
        soundcloudUrl: 'https://soundcloud.com/your-actual-account/sets/type-1',
        embedUrl: 'https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/playlists/YOUR_ACTUAL_PLAYLIST_ID&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true'
    },
    // ... repeat for other albums
};
```

### 3. How to Get SoundCloud Embed URLs

**Easy Method:**
1. Go to your SoundCloud playlist
2. Click "Share" 
3. Click "Embed"
4. Copy the `src` URL from the iframe code
5. Paste that URL as the `embedUrl` in the albumData

**Manual Method:**
1. Find your playlist ID: Go to `https://api.soundcloud.com/resolve?url=YOUR_PLAYLIST_URL&client_id=YOUR_CLIENT_ID`
2. Replace `YOUR_PLAYLIST_ID` in the embed URL template

## Current Features

✅ **Modal Preview System**: Clicking "Preview" opens a beautiful modal with SoundCloud player
✅ **Direct Purchase Links**: "Buy Direct - $15" buttons go straight to your PayPal
✅ **Mobile Responsive**: Works perfectly on all devices
✅ **Professional UI**: Gradient headers, smooth animations, clean design

## Testing the Integration

1. Open `index.html` in your browser (or use the "Launch Website" task)
2. Click any "Preview" button
3. You should see:
   - A modal overlay with dark background
   - SoundCloud player embedded
   - "Full Playlist on SoundCloud" link
   - "Buy Direct - $15" purchase button
   - Close button (×) or click outside to close

## Next Steps

1. **Replace placeholder URLs** with your actual SoundCloud links
2. **Test each album preview** to ensure they work
3. **Verify PayPal links** are working correctly
4. **Consider adding album descriptions** to the modal if desired

## Customization Options

You can easily customize:
- **Modal colors**: Edit the gradient in `.modal-header` in styles.css
- **Player size**: Change iframe height in the modal HTML
- **SoundCloud player options**: Modify the embed URL parameters:
  - `auto_play=false` - Don't auto-play
  - `color=%23ff5500` - SoundCloud orange theme
  - `show_comments=true` - Show comments
  - `show_user=true` - Show user info

## Benefits of This System

🎯 **Professional Experience**: Visitors can preview your music without leaving your site
💰 **Direct Sales Focus**: Preview leads directly to purchase buttons
📱 **Mobile Optimized**: Works perfectly on phones and tablets
🚀 **Fast Loading**: Lightweight modal system, no page redirects
🎵 **Full Control**: Your branding, your sales flow, your customers

The preview system is now ready! Just update those SoundCloud URLs and you'll have a complete direct-to-fan sales platform.
