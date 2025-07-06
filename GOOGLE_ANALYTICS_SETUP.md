# Google Analytics 4 Setup Guide for Elemental Publishing

## Step 1: Create Google Analytics Account

1. **Go to:** https://analytics.google.com
2. **Sign in** with your Google account
3. **Click "Start measuring"**
4. **Create Account:** Name it "Elemental Publishing"
5. **Create Property:** Name it "Elemental Publishing Website"
6. **Choose Industry:** "Arts & Entertainment" 
7. **Select reporting time zone:** Your location
8. **Choose data stream:** "Web"
9. **Enter website URL:** https://elementalpublishing.github.io/website
10. **Enter stream name:** "Main Website"

## Step 2: Get Your Measurement ID

1. **Copy the Measurement ID** (format: G-XXXXXXXXXX)
2. **In your index.html file**, replace `GA_MEASUREMENT_ID` with your actual ID:

```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
    gtag('config', 'G-XXXXXXXXXX');
```

## Step 3: Configure Goals & Conversions

### **Email Signup Conversion:**
1. **Go to:** Admin → Events → Create Event
2. **Event name:** `email_signup`
3. **Mark as conversion:** Yes

### **Purchase Intent Conversion:**
1. **Event name:** `purchase_intent`
2. **Mark as conversion:** Yes

### **Download Complete Conversion:**
1. **Event name:** `download_complete`
2. **Mark as conversion:** Yes
3. **Set value:** $15 (revenue tracking)

## Step 4: Set Up Enhanced Ecommerce (Optional)

### **For Revenue Tracking:**
1. **Admin → Data Streams → Web → Enhanced measurement**
2. **Enable:** "Purchases" 
3. **Configure** purchase events with album data

## Step 5: Create Custom Dashboard

### **Music Business Metrics Dashboard:**
1. **Go to:** Reports → Library → Create Collection
2. **Add these reports:**
   - **Traffic Sources** (where fans come from)
   - **Album Performance** (which albums get views)
   - **Conversion Funnel** (visitors → email → purchase)
   - **Geographic Data** (where your fans are)
   - **Revenue Report** (album sales data)

### **Key Metrics to Track:**
- **Monthly Active Users**
- **Email Signup Rate** by traffic source
- **Purchase Conversion Rate** by album
- **Revenue by Geographic Location**
- **Customer Journey** (discovery to purchase)

## Step 6: Verify Installation

### **Real-Time Testing:**
1. **Go to:** Reports → Real-time
2. **Visit your website** in another tab
3. **Click album buttons** and forms
4. **Verify events** appear in Real-time report

### **Event Testing:**
1. **Click Preview button** on any album
2. **Check:** `album_view` event fires
3. **Click Test Download Flow**
4. **Check:** `purchase_intent` event fires
5. **Submit email form**
6. **Check:** `email_signup` event fires

## Step 7: Industry-Standard Reports

### **Monthly Reporting Package:**
Create automated reports showing:
- **Total website traffic** and sources
- **Album engagement metrics**
- **Email list growth rate**
- **Purchase conversion rates**
- **Revenue by traffic source**
- **Geographic fan distribution**

### **Export for Presentations:**
- **PDF reports** for label meetings
- **Data Studio dashboards** for real-time sharing
- **CSV exports** for detailed analysis

## Professional Benefits

### **For Industry Meetings:**
- **Verified traffic data** - no "trust me" metrics
- **Professional presentation** - industry recognizes GA4
- **Conversion tracking** - shows real business metrics
- **Audience insights** - geographic and demographic data

### **For Business Decisions:**
- **Marketing ROI** - which platforms drive sales
- **Product insights** - which albums resonate
- **Pricing optimization** - conversion rate by price point
- **Geographic expansion** - where to focus efforts

### **For Partnerships:**
- **Credible metrics** for label discussions
- **Audience data** for sync opportunities  
- **Growth trends** for investor conversations
- **Professional reporting** for collaborations

## Privacy & Compliance

### **GDPR Compliance:**
- **Enable** IP anonymization
- **Configure** data retention (14 months recommended)
- **Add** privacy policy link on website
- **Respect** user consent preferences

### **Industry Best Practices:**
- **Regular reporting** (monthly/quarterly)
- **Data backup** (export key metrics)
- **Cross-platform tracking** (social media integration)
- **Benchmarking** against industry standards

## Next Steps After Setup

1. **Install tracking** on all pages (download, thank-you pages)
2. **Set up weekly reports** for business monitoring
3. **Create custom segments** for different fan types
4. **Integrate with Google Ads** if you run advertising
5. **Connect social media** analytics for full picture

**Once GA4 is live, you'll have professional-grade analytics that industry professionals recognize and trust!**
