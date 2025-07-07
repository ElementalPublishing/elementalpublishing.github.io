# Formspree Setup Guide - Elemental Publishing

## Step 1: Create Formspree Account
1. Go to https://formspree.io
2. Sign up with: houser2388@gmail.com
3. Verify your email

## Step 2: Create 3 Forms

### Form 1: Type 1 Album
- **Form Name**: "Type 1 Album Download"
- **Form ID**: You'll get something like `mwpejrkl`
- **Purpose**: Deliver Type 1 album download link

### Form 2: Strip Tape Album  
- **Form Name**: "Strip Tape Album Download"
- **Form ID**: You'll get something like `mkndslwp`
- **Purpose**: Deliver Strip Tape album download link

### Form 3: New Matrix Album
- **Form Name**: "New Matrix Album Download" 
- **Form ID**: You'll get something like `mbjdkslp`
- **Purpose**: Deliver New Matrix album download link

## Step 3: Update Download Pages

After creating forms, replace these in your download pages:

### download-type1.html:
```html
action="https://formspree.io/f/YOUR_TYPE1_FORM_ID"
```
**Replace `YOUR_TYPE1_FORM_ID` with actual Form ID**

### download-striptape.html:
```html  
action="https://formspree.io/f/YOUR_STRIPTAPE_FORM_ID"
```
**Replace `YOUR_STRIPTAPE_FORM_ID` with actual Form ID**

### download-newmatrix.html:
```html
action="https://formspree.io/f/YOUR_NEWMATRIX_FORM_ID"  
```
**Replace `YOUR_NEWMATRIX_FORM_ID` with actual Form ID**

## Step 4: Configure Auto-Response Emails

For each form in Formspree dashboard:

### Type 1 Auto-Response Email:
**Subject**: Your Type 1 Album Download - Elemental Publishing

**Message**:
```
Thanks for supporting Elemental Publishing!

Your Type 1 album download is ready:
📦 Download: [REPLACE_WITH_GITHUB_DOWNLOAD_URL]

What you get:
• 10 high-quality MP3 tracks (320kbps)
• Album artwork (1400x1400px)
• Professional packaging

Instructions:
1. Click the download link above
2. Save the ZIP file to your computer  
3. Extract/unzip the folder
4. Enjoy your music!

Works on: iPhone, Android, Windows, Mac, car stereos, and all MP3 players.

Questions? Reply to this email.

Thanks for buying direct!
- Elemental Publishing

🎵 More music: https://elementalpublishing.github.io/website
📧 Contact: houser2388@gmail.com
```

### Strip Tape Auto-Response Email:
**Subject**: Your Strip Tape Album Download - Elemental Publishing

**Message**:
```
Thanks for supporting Elemental Publishing!

Your Strip Tape album download is ready:
📦 Download: [REPLACE_WITH_GITHUB_DOWNLOAD_URL]

What you get:
• 10 high-quality MP3 tracks (320kbps)
• Album artwork (1400x1400px) 
• Professional packaging

Instructions:
1. Click the download link above
2. Save the ZIP file to your computer
3. Extract/unzip the folder
4. Enjoy your music!

Works on: iPhone, Android, Windows, Mac, car stereos, and all MP3 players.

Questions? Reply to this email.

Thanks for buying direct!
- Elemental Publishing

🎵 More music: https://elementalpublishing.github.io/website
📧 Contact: houser2388@gmail.com
```

### New Matrix Auto-Response Email:
**Subject**: Your New Matrix Album Download - Elemental Publishing

**Message**:
```
Thanks for supporting Elemental Publishing!

Your New Matrix album download is ready:
📦 Download: [REPLACE_WITH_GITHUB_DOWNLOAD_URL]

What you get:
• 10 high-quality MP3 tracks (320kbps)
• Album artwork (1400x1400px)
• Professional packaging

Instructions:
1. Click the download link above  
2. Save the ZIP file to your computer
3. Extract/unzip the folder
4. Enjoy your music!

Works on: iPhone, Android, Windows, Mac, car stereos, and all MP3 players.

Questions? Reply to this email.

Thanks for buying direct!
- Elemental Publishing

🎵 More music: https://elementalpublishing.github.io/website
📧 Contact: houser2388@gmail.com
```

## Step 5: Get GitHub Download URLs

After uploading your ZIP files to GitHub Releases:
1. Right-click each ZIP file in Releases
2. Copy download URL
3. Replace `[REPLACE_WITH_GITHUB_DOWNLOAD_URL]` in each auto-response email

## Step 6: Test Complete Flow

1. Buy album → PayPal → Download page
2. Enter test email → Submit form
3. Check email for auto-response with download link
4. Click download link → Test file extraction

## Notes:
- Formspree free plan: 50 submissions/month
- Upgrade to paid plan for unlimited submissions
- All customer emails will be saved in Formspree dashboard
- You can export customer emails for marketing
