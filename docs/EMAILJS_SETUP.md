# EmailJS Setup Guide - Automatic Download Emails

## Step 1: Create EmailJS Account
1. Go to https://www.emailjs.com/
2. Sign up with your email (houser2388@gmail.com)
3. Verify your email account

## Step 2: Add Email Service
1. Go to **Email Services** in dashboard
2. Click **Add New Service**
3. Choose **Gmail** (recommended)
4. Connect your Gmail account (houser2388@gmail.com)
5. Copy the **Service ID** (something like `service_abc123`)

## Step 3: Create Email Template
1. Go to **Email Templates** in dashboard
2. Click **Create New Template**
3. **Template Name**: "Album Download Email"
4. **Template Content**:

```
Subject: Your {{album_name}} Download - Elemental Publishing

Hi {{customer_name}},

Thanks for supporting Elemental Publishing!

Your {{album_name}} album download is ready:
📦 Download: {{download_link}}

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

5. Save template and copy the **Template ID** (something like `template_xyz789`)

## Step 4: Get Public Key
1. Go to **Account** → **General**
2. Copy your **Public Key** (something like `abc123xyz`)

## Step 5: Update Website Code

### Replace these placeholders in ALL download pages:

#### In download-type1.html, download-striptape.html, and download-newmatrix.html:
```javascript
emailjs.init("YOUR_EMAILJS_PUBLIC_KEY"); // Replace with your actual public key

emailjs.send("YOUR_SERVICE_ID", "YOUR_TEMPLATE_ID", {
```

#### Replace:
- `YOUR_EMAILJS_PUBLIC_KEY` → Your actual public key
- `YOUR_SERVICE_ID` → Your Gmail service ID  
- `YOUR_TEMPLATE_ID` → Your email template ID

### Example after replacement:
```javascript
emailjs.init("abc123xyz");

emailjs.send("service_abc123", "template_xyz789", {
```

## Step 6: Update Download URLs

### In thank you pages, replace:
- `[GITHUB_TYPE1_DOWNLOAD_URL]` → Actual GitHub download URL
- `[GITHUB_STRIPTAPE_DOWNLOAD_URL]` → Actual GitHub download URL
- `[GITHUB_NEWMATRIX_DOWNLOAD_URL]` → Actual GitHub download URL

### In download page JavaScript, replace:
- `[GITHUB_TYPE1_DOWNLOAD_URL]` → Actual GitHub download URL
- `[GITHUB_STRIPTAPE_DOWNLOAD_URL]` → Actual GitHub download URL  
- `[GITHUB_NEWMATRIX_DOWNLOAD_URL]` → Actual GitHub download URL

## Step 7: Test Complete Flow

1. Upload albums to GitHub Releases
2. Update all download URLs
3. Test form submission on download page
4. Verify thank you page shows
5. Check email is sent automatically

## EmailJS Free Plan
- **200 emails/month** (perfect for testing)
- Upgrade to paid plan for more emails
- Completely free to start

## Files That Need Updates
- ✅ `download-type1.html` (updated)
- 🔄 `download-striptape.html` (needs EmailJS integration)  
- 🔄 `download-newmatrix.html` (needs EmailJS integration)
- ✅ `thank-you-type1.html` (created)
- ✅ `thank-you-striptape.html` (created)
- ✅ `thank-you-newmatrix.html` (created)

## Complete Customer Flow
1. **Buy** → PayPal → Download page
2. **Enter email** → Submit form
3. **EmailJS sends email** automatically
4. **Redirect to thank you page** with download link
5. **Customer gets immediate access** + email backup

Perfect automated system! 🎉
