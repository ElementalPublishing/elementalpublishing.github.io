# GitHub Pages Setup Guide for Elemental Publishing

## Quick Start (5 minutes to go live!)

### Step 1: Create GitHub Repository
1. Go to [GitHub.com](https://github.com) and create account (if needed)
2. Click "New Repository"
3. Name it: `yourusername.github.io` (replace with your actual username)
4. Make it **Public**
5. Check "Add a README file"
6. Click "Create repository"

### Step 2: Upload Your Website Files
**Option A: Web Interface (Easiest)**
1. In your new repository, click "Upload files"
2. Drag and drop ALL files from your `website` folder
3. Write commit message: "Initial website upload"
4. Click "Commit changes"

**Option B: Git Commands (If you have Git installed)**
```bash
git clone https://github.com/yourusername/yourusername.github.io.git
cd yourusername.github.io
# Copy all your website files here
git add .
git commit -m "Initial website upload"
git push origin main
```

### Step 3: Enable GitHub Pages
1. Go to repository Settings tab
2. Scroll down to "Pages" section
3. Under "Source", select "Deploy from a branch"
4. Choose "main" branch and "/ (root)" folder
5. Click "Save"

**Your site will be live at: `https://yourusername.github.io`**

### Step 4: Custom Domain (Optional but Recommended)
1. Buy domain (recommended: `elementalpublishing.com`)
2. In GitHub repo, go to Settings > Pages
3. Add your custom domain in "Custom domain" field
4. In your domain registrar, add these DNS records:
   ```
   Type: A
   Name: @
   Value: 185.199.108.153
   
   Type: A
   Name: @
   Value: 185.199.109.153
   
   Type: A
   Name: @
   Value: 185.199.110.153
   
   Type: A
   Name: @
   Value: 185.199.111.153
   
   Type: CNAME
   Name: www
   Value: yourusername.github.io
   ```

### Step 5: SSL Certificate (Automatic)
- GitHub Pages will automatically provide SSL certificate
- Your site will be accessible via `https://`
- May take a few minutes to activate

## Updating Your Website

### Method 1: GitHub Web Interface
1. Navigate to the file you want to edit
2. Click the pencil icon (Edit)
3. Make your changes
4. Scroll down and commit changes
5. Changes go live automatically!

### Method 2: Local Development
1. Clone your repository locally
2. Make changes to files
3. Push changes back to GitHub
4. Site updates automatically

## Content Updates You Should Make

### 1. Update _config.yml
- Replace "yourusername" with your actual GitHub username
- Add your social media handles
- Update title and description

### 2. Update index.html
- Replace placeholder content with your actual artist information
- Update music/album details
- Add your actual contact information
- Update social media links

### 3. Add Your Images
- Upload your album covers to `assets/images/`
- Replace logo files with your actual logos
- Update image paths in HTML

### 4. PayPal Integration
- Set up PayPal Business account
- Replace placeholder payment buttons with real PayPal buttons
- Test purchase flow

### 5. Email List Setup
- Choose email service (Mailchimp, ConvertKit, etc.)
- Replace contact form with actual email signup
- Set up automated welcome emails

## Performance Tips

### Image Optimization
- Keep images under 1MB each
- Use WebP format when possible
- Compress images before uploading

### Loading Speed
- Your site is already optimized
- GitHub Pages provides fast global CDN
- No additional optimization needed

## Analytics Setup

### Google Analytics (Free)
1. Create Google Analytics account
2. Get tracking code
3. Add to `<head>` section of index.html
4. Track visitor behavior and conversions

## Backup Strategy

- Your GitHub repository IS your backup
- All changes are version controlled
- You can revert to any previous version
- Download ZIP anytime from GitHub

## Troubleshooting

### Site Not Loading
- Check repository name is exactly `yourusername.github.io`
- Ensure repository is public
- Wait 10-15 minutes for first deployment

### Custom Domain Issues
- Verify DNS records are correct
- Wait 24-48 hours for DNS propagation
- Check domain registrar settings

### Images Not Showing
- Verify image paths are correct
- Use forward slashes in paths: `assets/images/logo.png`
- Ensure images are uploaded to repository

## Next Steps After Going Live

1. **Test Everything**
   - Check all links work
   - Test on mobile devices
   - Verify contact forms

2. **SEO Setup**
   - Submit to Google Search Console
   - Create XML sitemap
   - Optimize page titles and descriptions

3. **Social Media Integration**
   - Add social sharing buttons
   - Create social media posting schedule
   - Drive traffic from platforms to your site

4. **Email Marketing**
   - Set up welcome email sequence
   - Create content calendar
   - Plan exclusive offers for subscribers

## Cost Summary
- **GitHub Pages**: FREE
- **Domain**: $12/year
- **Total**: $1/month (vs $80+/month for music platforms)

## Support
- GitHub Pages Documentation: https://pages.github.com/
- GitHub Community: https://github.community/
- This README file for reference

---

**Remember**: Every visitor you convert to your email list is a fan you OWN, not rent from platforms!
