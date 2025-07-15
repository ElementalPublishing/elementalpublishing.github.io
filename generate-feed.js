const fs = require('fs');
const path = require('path');

// Directory containing your HTML files
const htmlDir = path.join(__dirname, 'html');

// Output RSS file
const outputFeed = path.join(__dirname, 'feed.xml');

// Your site base URL
const siteUrl = 'https://elementalpublishing.org/html/';

function extractTitle(html) {
  const match = html.match(/<title>([^<]*)<\/title>/i);
  return match ? match[1] : 'Untitled Page';
}

function formatDate(date) {
  // Returns RFC-822 formatted date
  return new Date(date).toUTCString();
}

function main() {
  const files = fs.readdirSync(htmlDir).filter(f => f.endsWith('.html'));
  let items = [];

  files.forEach(file => {
    const filePath = path.join(htmlDir, file);
    const html = fs.readFileSync(filePath, 'utf8');
    const title = extractTitle(html);
    const stat = fs.statSync(filePath);
    const url = siteUrl + encodeURIComponent(file);
    const pubDate = formatDate(stat.mtime);

    // Custom description: extract entity-name, entity-archetype, entity-status, entity-role
    function extractEntityField(html, selector) {
      const regex = new RegExp(`<${selector}[^>]*>([\\s\\S]*?)<\\/${selector}>`, 'i');
      const divRegex = new RegExp(`<div class=["']${selector}["'][^>]*>([\\s\\S]*?)<\\/div>`, 'i');
      const h1Regex = new RegExp(`<h1 class=["']${selector}["'][^>]*>([\\s\\S]*?)<\\/h1>`, 'i');
      let match = divRegex.exec(html) || h1Regex.exec(html);
      return match ? match[1].trim() : '';
    }

    const entityName = extractEntityField(html, 'entity-name');
    const entityArchetype = extractEntityField(html, 'entity-archetype');
    const entityStatus = extractEntityField(html, 'entity-status');
    const entityRole = extractEntityField(html, 'entity-role');
    let description = [entityName, entityArchetype, entityStatus, entityRole].filter(Boolean).join(' | ');
    if (!description) {
      // fallback to old method if not found
      const descMatch = html.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
      description = descMatch ? descMatch[1].replace(/<[^>]+>/g, '').trim() : '';
      description = description.substring(0, 200) + (description.length > 200 ? '...' : '');
    }

    items.push({ title, url, pubDate, description });
  });

  // Build RSS XML
  const feed =
`<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>Elemental Publishing</title>
  <link>https://elementalpublishing.org/</link>
  <description>Latest updates from Elemental Publishing</description>
  <language>en</language>
  <lastBuildDate>${formatDate(new Date())}</lastBuildDate>
${items.map(item => `
  <item>
    <title>${item.title}</title>
    <link>${item.url}</link>
    <pubDate>${item.pubDate}</pubDate>
    <description>${item.description.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')}</description>
    <guid>${item.url}</guid>
  </item>
`).join('')}
</channel>
</rss>
`;

  fs.writeFileSync(outputFeed, feed, 'utf8');
  console.log(`✅ RSS feed generated: feed.xml (${items.length} items)`);
}

main();