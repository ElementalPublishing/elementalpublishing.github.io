#!/usr/bin/env node

/**
 * Static Site Generator for Character Entities
 * Converts YAML-formatted .md files with [[wikilinks]] into beautiful HTML pages
 * 
 * Features:
 * - Preserves YAML structure and indentation as HTML blocks
 * - Converts [[wikilinks]] to clickable HTML links
 * - Creates stub pages for missing linked entities
 * - Uses existing spiderfox-styles.css for unified styling
 * - Includes placeholder image areas
 */

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

class EntityPageGenerator {
    constructor() {
        this.outputDir = path.join(__dirname, 'html');
        this.entitiesDir = path.join(__dirname, 'entities');
        this.cssPath = 'spiderfox-styles.css';
        this.generatedPages = new Set();
        this.linkedEntities = new Set();
    }

    /**
     * Initialize the generator - create output directory
     */
    init() {
        if (!fs.existsSync(this.outputDir)) {
            fs.mkdirSync(this.outputDir, { recursive: true });
        }
        console.log(`📁 Output directory ready: ${this.outputDir}`);
    }

    /**
     * Pre-process raw YAML content to extract wikilinks before YAML parsing strips them
     */
    extractWikilinksFromRaw(rawYaml) {
        // Store original raw content for later reference
        this.rawYamlContent = rawYaml;
        
        const wikilinkRegex = /\[\[([^\]]+)\]\]/g;
        let match;
        
        while ((match = wikilinkRegex.exec(rawYaml)) !== null) {
            const linkText = match[1].trim();
            this.linkedEntities.add(linkText);
        }
    }

    /**
     * Check if a key was originally a wikilink in the raw YAML content
     */
    wasOriginallyWikilink(key) {
        return this.rawYamlContent && this.rawYamlContent.includes(`[[${key}]]:`);
    }

    /**
     * Parse a markdown file and extract YAML frontmatter + markdown content
     */
    parseMarkdownFile(filePath) {
        try {
            const content = fs.readFileSync(filePath, 'utf8');
            
            // Trim leading whitespace and check for YAML frontmatter
            const trimmedContent = content.trimStart();
            if (!trimmedContent.startsWith('---')) {
                console.log(`⚠️  No YAML frontmatter in: ${filePath}`);
                console.log(`   First 100 chars: ${content.substring(0, 100).replace(/\n/g, '\\n')}`);
                return null;
            }
            
            // Split content by --- markers (using multiline regex)
            const parts = trimmedContent.split(/^---$/m);
            
            let yamlContent = '';
            let markdownContent = '';
            
            if (parts.length >= 3) {
                // Proper YAML frontmatter with opening and closing ---
                yamlContent = parts[1];
                markdownContent = parts.slice(2).join('---').trim();
                console.log(`✓ Proper YAML frontmatter found in: ${path.basename(filePath)}`);
            } else if (parts.length === 2) {
                // Loose YAML - starts with --- but no closing marker
                console.log(`⚠️  Loose YAML format in: ${path.basename(filePath)} (no closing ---)`);
                
                const afterFirstDash = parts[1];
                
                // Look for a clear markdown section (lines that don't look like YAML)
                const lines = afterFirstDash.split('\n');
                let yamlEndIndex = lines.length;
                
                // Find where YAML ends and markdown begins
                // Look for lines that are clearly prose/narrative content
                for (let i = 0; i < lines.length; i++) {
                    const line = lines[i].trim();
                    
                    // Skip empty lines and YAML comments
                    if (!line || line.startsWith('#')) continue;
                    
                    // If we find a line that looks like markdown prose
                    if (line && 
                        !line.includes(':') && // Not YAML key-value
                        !line.match(/^\s+/) && // Not indented YAML
                        line.length > 50 && // Looks like paragraph text
                        !line.match(/^[a-z_]+:?$/i) && // Not YAML key
                        (line.includes(' ') && line.split(' ').length > 5)) { // Multiple words, paragraph-like
                        yamlEndIndex = i;
                        console.log(`   Found prose at line ${i}: "${line.substring(0, 50)}..."`);
                        break;
                    }
                }
                
                yamlContent = lines.slice(0, yamlEndIndex).join('\n');
                markdownContent = lines.slice(yamlEndIndex).join('\n').trim();
            } else {
                console.log(`❌ Malformed structure in: ${filePath}`);
                console.log(`   First 200 chars: ${content.substring(0, 200).replace(/\n/g, '\\n')}`);
                return null;
            }
            
            // Pre-extract wikilinks before YAML parsing strips the brackets
            this.extractWikilinksFromRaw(yamlContent);
            
            // Pre-process YAML to quote wikilink keys for valid YAML syntax
            const processedYamlContent = yamlContent.replace(/^(\s*)\[\[([^\]]+)\]\]:$/gm, '$1"[[$2]]":');
            
            let parsedYaml;
            try {
                parsedYaml = yaml.load(processedYamlContent, { 
                    schema: yaml.DEFAULT_SCHEMA 
                });
            } catch (yamlError) {
                console.error(`❌ YAML parsing error in ${path.basename(filePath)}: ${yamlError.message}`);
                console.log(`   Skipping this file due to YAML issues (likely duplicate keys)`);
                return null;
            }
            
            return {
                yaml: parsedYaml,
                rawYaml: yamlContent,
                markdownContent: markdownContent,
                filePath: filePath
            };
        } catch (error) {
            console.error(`❌ Error parsing ${filePath}:`, error.message);
            
            // Try to read content for debugging
            try {
                const content = fs.readFileSync(filePath, 'utf8');
                console.log(`   First 200 chars: ${content.substring(0, 200).replace(/\n/g, '\\n')}`);
            } catch (readError) {
                console.log(`   Could not read file for debugging: ${readError.message}`);
            }
            return null;
        }
    }

    /**
     * Convert [[wikilinks]] to HTML links and track linked entities
     */
    processWikilinks(text) {
        if (typeof text !== 'string') return text;
        
        return text.replace(/\[\[([^\]]+)\]\]/g, (match, linkText) => {
            // Clean up the link text
            const cleanLinkText = linkText.trim();
            const htmlFilename = this.sanitizeFilename(cleanLinkText) + '.html';
            
            // Track this as a linked entity
            this.linkedEntities.add(cleanLinkText);
            
            return `<a href="${htmlFilename}" class="wikilink">${cleanLinkText}</a>`;
        });
    }

    /**
     * Recursively process any value that might contain wikilinks
     */
    processValueForWikilinks(value) {
        if (typeof value === 'string') {
            return this.processWikilinks(value);
        } else if (Array.isArray(value)) {
            return value.map(item => this.processValueForWikilinks(item));
        } else if (typeof value === 'object' && value !== null) {
            const processed = {};
            for (const [key, val] of Object.entries(value)) {
                // Check if this key was originally a wikilink
                let processedKey = key;
                if (this.wasOriginallyWikilink(key)) {
                    // Convert it back to a wikilink for HTML processing
                    processedKey = this.processWikilinks(`[[${key}]]`);
                } else {
                    // Process any wikilinks that might be in the key itself
                    processedKey = this.processWikilinks(key);
                }
                processed[processedKey] = this.processValueForWikilinks(val);
            }
            return processed;
        }
        return value;
    }

    /**
     * Sanitize text for use as filename
     */
    sanitizeFilename(text) {
        return text.toLowerCase()
                  .replace(/[^a-z0-9]+/g, '-')
                  .replace(/^-+|-+$/g, '');
    }

    /**
     * Check if an object contains only simple values (no nested objects/arrays)
     */
    isSimpleObject(obj) {
        if (typeof obj !== 'object' || obj === null || Array.isArray(obj)) {
            return false;
        }
        
        return Object.values(obj).every(value => 
            typeof value === 'string' || 
            typeof value === 'number' || 
            typeof value === 'boolean'
        );
    }

    /**
     * Convert basic markdown to HTML
     */
    markdownToHtml(markdown) {
        if (!markdown || typeof markdown !== 'string') return '';
        
        return markdown
            // Convert headers
            .replace(/^### (.*$)/gm, '<h3>$1</h3>')
            .replace(/^## (.*$)/gm, '<h2>$1</h2>')
            .replace(/^# (.*$)/gm, '<h1>$1</h1>')
            // Convert bold and italic
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            // Convert line breaks to <br> and paragraphs
            .replace(/\n\s*\n/g, '</p><p>')
            .replace(/\n/g, '<br>')
            // Wrap in paragraph tags
            .replace(/^(.+)$/gm, '<p>$1</p>')
            // Clean up empty paragraphs
            .replace(/<p><\/p>/g, '')
            .replace(/<p>(<h[1-6]>.*<\/h[1-6]>)<\/p>/g, '$1');
    }

    /**
     * Separate simple and complex properties from a mixed object
     */
    separateSimpleAndComplex(obj) {
        const simple = {};
        const complex = {};
        
        for (const [key, value] of Object.entries(obj)) {
            if (typeof value === 'string' || typeof value === 'number' || typeof value === 'boolean') {
                simple[key] = value;
            } else {
                complex[key] = value;
            }
        }
        
        return { simple, complex };
    }

    /**
     * Generate compact HTML for simple objects
     */
    generateSimpleObjectHtml(obj) {
        const entries = Object.entries(obj).map(([key, value]) => {
            const valueClass = typeof value === 'number' || typeof value === 'boolean' ? `yaml-${typeof value}` : '';
            return `<span class="simple-pair"><strong>${key}:</strong> <span class="yaml-value ${valueClass}">${value}</span></span>`;
        }).join('');
        
        return `<div class="simple-object">${entries}</div>`;
    }

    /**
     * Generate HTML for a YAML object with proper indentation and structure
     */
    generateYamlHtml(obj, depth = 0) {
        if (typeof obj === 'string') {
            return `<span class="yaml-value">${obj}</span>`;
        }
        
        if (typeof obj === 'number' || typeof obj === 'boolean') {
            return `<span class="yaml-value yaml-${typeof obj}">${obj}</span>`;
        }
        
        if (Array.isArray(obj)) {
            const items = obj.map(item => 
                `<li class="yaml-array-item">${this.generateYamlHtml(item, depth + 1)}</li>`
            ).join('\n');
            return `<ul class="yaml-array">\n${items}\n</ul>`;
        }
        
        if (typeof obj === 'object' && obj !== null) {
            // Check if this is a simple object that can be rendered compactly
            if (this.isSimpleObject(obj)) {
                return this.generateSimpleObjectHtml(obj);
            }
            
            // For mixed objects, separate simple and complex properties
            const { simple, complex } = this.separateSimpleAndComplex(obj);
            
            let html = '<div class="yaml-object">\n';
            
            // First, render simple properties compactly if any exist
            if (Object.keys(simple).length > 0) {
                html += `
                    <div class="yaml-block simple-values-block" data-depth="${depth}">
                        <div class="yaml-value-container">
                            ${this.generateSimpleObjectHtml(simple)}
                        </div>
                    </div>
                `;
            }
            
            // Then render complex properties with full blocks
            const complexEntries = Object.entries(complex).map(([key, value]) => {
                const isSection = key.startsWith('[[') && key.endsWith(']]');
                const keyClass = isSection ? 'yaml-section-key' : 'yaml-key';
                const blockClass = isSection ? 'yaml-section-block' : 'yaml-block';
                
                return `
                    <div class="${blockClass}" data-depth="${depth}">
                        <div class="${keyClass}">${key}:</div>
                        <div class="yaml-value-container">
                            ${this.generateYamlHtml(value, depth + 1)}
                        </div>
                    </div>
                `;
            }).join('\n');
            
            html += complexEntries + '\n</div>';
            return html;
        }
        
        return `<span class="yaml-value">${obj}</span>`;
    }

    /**
     * Generate the complete HTML page for an entity
     */
    generateEntityPage(entityData) {
        const { yaml: entity, rawYaml, markdownContent } = entityData;
        
        // Process all wikilinks in the entity data
        const processedEntity = this.processValueForWikilinks(entity);
        
        // Extract key information
        const entityName = entity.name || 'Unknown Entity';
        const archetype = entity.archetype || '';
        const status = entity.status || '';
        const role = entity.role || '';
        
        // Generate the main content HTML
        const contentHtml = this.generateYamlHtml(processedEntity);
        
        // Process markdown content for wikilinks and convert to basic HTML
        let storyHtml = '';
        if (markdownContent) {
            // Process wikilinks in the markdown content
            const processedMarkdown = this.processWikilinks(markdownContent);
            
            // Convert basic markdown to HTML (simple conversion)
            storyHtml = this.markdownToHtml(processedMarkdown);
        }
        
        // Create the complete HTML page
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${entityName} - Character Entity</title>
    <link rel="stylesheet" href="../${this.cssPath}">
    <style>
        /* Entity-specific styles */
        .entity-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            background: var(--bg-primary, #1a1a1a);
            color: var(--text-primary, #ffffff);
            min-height: 100vh;
        }
        
        .entity-header {
            text-align: center;
            margin-bottom: 3rem;
            padding: 2rem;
            border: 2px solid var(--accent-color, #00ff88);
            border-radius: 10px;
            background: var(--bg-secondary, #2a2a2a);
        }
        
        .entity-name {
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            color: var(--accent-color, #00ff88);
            text-shadow: 0 0 20px var(--accent-color, #00ff88);
        }
        
        .entity-archetype {
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
            color: var(--text-secondary, #cccccc);
        }
        
        .entity-status {
            font-size: 1.2rem;
            color: var(--text-accent, #888888);
        }
        
        .image-placeholder {
            width: 300px;
            height: 300px;
            margin: 2rem auto;
            border: 2px dashed var(--accent-color, #00ff88);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-secondary, #cccccc);
            font-size: 1.1rem;
            background: var(--bg-tertiary, #333333);
        }
        
        .entity-content {
            margin-top: 3rem;
        }
        
        /* Story Section Styles */
        .story-section {
            margin: 3rem 0;
            padding: 2rem;
            background: var(--bg-secondary, #2a2a2a);
            border-radius: 10px;
            border-left: 4px solid var(--highlight-color, #ffaa00);
        }
        
        .story-title {
            font-size: 1.8rem;
            color: var(--highlight-color, #ffaa00);
            margin-bottom: 1.5rem;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .story-content {
            color: var(--text-primary, #ffffff);
            line-height: 1.8;
            font-size: 1.1rem;
        }
        
        .story-content h1, .story-content h2, .story-content h3 {
            color: var(--accent-color, #00ff88);
            margin: 1.5rem 0 1rem 0;
        }
        
        .story-content p {
            margin-bottom: 1.2rem;
        }
        
        .story-content strong {
            color: var(--highlight-color, #ffaa00);
        }
        
        .story-content em {
            color: var(--text-secondary, #cccccc);
            font-style: italic;
        }
        
        /* YAML Structure Styles */
        .yaml-object {
            margin: 1rem 0;
        }
        
        .yaml-block {
            margin: 1.5rem 0;
            padding: 1rem;
            border-left: 3px solid var(--accent-color, #00ff88);
            background: var(--bg-secondary, #2a2a2a);
            border-radius: 0 5px 5px 0;
        }
        
        .simple-values-block {
            background: var(--bg-tertiary, #333333);
            border-left: 3px solid var(--highlight-color, #ffaa00);
        }
        
        .simple-values-block .yaml-key {
            color: var(--highlight-color, #ffaa00);
            font-size: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .yaml-section-block {
            margin: 2rem 0;
            padding: 1.5rem;
            border: 1px solid var(--accent-color, #00ff88);
            border-radius: 8px;
            background: var(--bg-tertiary, #333333);
        }
        
        /* Simple Object Compact Styling */
        .simple-object {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            padding: 0.8rem;
            background: var(--bg-secondary, #2a2a2a);
            border-radius: 5px;
            border: 1px solid var(--accent-color, #00ff88);
        }
        
        .simple-pair {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.3rem 0.8rem;
            background: var(--bg-primary, #1a1a1a);
            border-radius: 3px;
            border-left: 2px solid var(--accent-color, #00ff88);
        }
        
        .simple-pair strong {
            color: var(--accent-color, #00ff88);
            font-size: 0.9rem;
        }
        
        .yaml-key {
            font-weight: bold;
            color: var(--accent-color, #00ff88);
            margin-bottom: 0.5rem;
            font-size: 1.1rem;
        }
        
        .yaml-section-key {
            font-weight: bold;
            color: var(--accent-color, #00ff88);
            margin-bottom: 1rem;
            font-size: 1.4rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            border-bottom: 2px solid var(--accent-color, #00ff88);
            padding-bottom: 0.5rem;
        }
        
        .yaml-value-container {
            margin-left: 1rem;
        }
        
        .yaml-value {
            color: var(--text-primary, #ffffff);
            line-height: 1.6;
        }
        
        .yaml-value.yaml-number {
            color: var(--highlight-color, #ffaa00);
        }
        
        .yaml-value.yaml-boolean {
            color: var(--highlight-color, #ffaa00);
        }
        
        .yaml-array {
            list-style: none;
            padding: 0;
            margin: 0.5rem 0;
        }
        
        .yaml-array-item {
            margin: 0.5rem 0;
            padding: 0.5rem;
            background: var(--bg-primary, #1a1a1a);
            border-radius: 3px;
            border-left: 2px solid var(--accent-color, #00ff88);
        }
        
        /* Wikilink Styles */
        .wikilink {
            color: var(--accent-color, #00ff88);
            text-decoration: none;
            border-bottom: 1px dashed var(--accent-color, #00ff88);
            transition: all 0.3s ease;
        }
        
        .wikilink:hover {
            color: var(--highlight-color, #ffaa00);
            border-bottom-color: var(--highlight-color, #ffaa00);
            text-shadow: 0 0 5px var(--highlight-color, #ffaa00);
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .entity-container {
                padding: 1rem;
            }
            
            .entity-name {
                font-size: 2rem;
            }
            
            .image-placeholder {
                width: 250px;
                height: 250px;
            }
            
            .yaml-value-container {
                margin-left: 0.5rem;
            }
            
            .simple-object {
                flex-direction: column;
                gap: 0.5rem;
            }
            
            .simple-pair {
                justify-content: space-between;
            }
        }
    </style>
</head>
<body>
    <div class="entity-container">
        <header class="entity-header">
            <h1 class="entity-name">${entityName}</h1>
            <div class="entity-archetype">${archetype}</div>
            <div class="entity-status">${status}</div>
            ${role ? `<div class="entity-role">${role}</div>` : ''}
            
            <div class="image-placeholder">
                <div>Character Image Placeholder</div>
            </div>
        </header>
        
        <main class="entity-content">
            ${contentHtml}
        </main>
        
        ${storyHtml ? `
        <section class="story-section">
            <h2 class="story-title">Story & Background</h2>
            <div class="story-content">
                ${storyHtml}
            </div>
        </section>
        ` : ''}
        
        <footer style="margin-top: 3rem; text-align: center; color: var(--text-secondary, #888888);">
            <p>Generated from: ${path.basename(entityData.filePath)}</p>
            <p>Part of the Cyberdynasties Entity System</p>
        </footer>
    </div>
</body>
</html>`;
    }

    /**
     * Generate a stub page for a linked entity that doesn't exist yet
     */
    generateStubPage(entityName) {
        const filename = this.sanitizeFilename(entityName);
        
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${entityName} - Entity Stub</title>
    <link rel="stylesheet" href="../${this.cssPath}">
    <style>
        .stub-container {
            max-width: 800px;
            margin: 5rem auto;
            padding: 3rem;
            text-align: center;
            background: var(--bg-secondary, #2a2a2a);
            border: 2px solid var(--accent-color, #00ff88);
            border-radius: 10px;
            color: var(--text-primary, #ffffff);
        }
        
        .stub-title {
            font-size: 2.5rem;
            color: var(--accent-color, #00ff88);
            margin-bottom: 1rem;
            text-shadow: 0 0 20px var(--accent-color, #00ff88);
        }
        
        .stub-message {
            font-size: 1.2rem;
            color: var(--text-secondary, #cccccc);
            margin-bottom: 2rem;
        }
        
        .stub-placeholder {
            width: 200px;
            height: 200px;
            margin: 2rem auto;
            border: 2px dashed var(--accent-color, #00ff88);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-secondary, #cccccc);
            background: var(--bg-tertiary, #333333);
        }
    </style>
</head>
<body>
    <div class="stub-container">
        <h1 class="stub-title">${entityName}</h1>
        <p class="stub-message">This entity page is coming soon...</p>
        <div class="stub-placeholder">
            <div>Entity<br>Placeholder</div>
        </div>
        <p style="color: var(--text-accent, #888888); margin-top: 2rem;">
            This page was automatically generated as a stub because it was referenced by another entity.
        </p>
    </div>
</body>
</html>`;
    }

    /**
     * Generate page for a single entity
     */
    async generateSingleEntity(filePath) {
        console.log(`🔧 Processing: ${filePath}`);
        
        const entityData = this.parseMarkdownFile(filePath);
        if (!entityData) return false;
        
        // Generate the HTML content
        const htmlContent = this.generateEntityPage(entityData);
        
        // Determine output filename
        const entityName = entityData.yaml.name || path.basename(filePath, '.md');
        const outputFilename = this.sanitizeFilename(entityName) + '.html';
        const outputPath = path.join(this.outputDir, outputFilename);
        
        // Write the HTML file
        fs.writeFileSync(outputPath, htmlContent, 'utf8');
        this.generatedPages.add(entityName);
        
        console.log(`✅ Generated: ${outputPath}`);
        return true;
    }

    /**
     * Generate stub pages for any linked entities that don't have pages yet
     */
    generateStubPages() {
        console.log(`🔗 Checking for linked entities to create stubs...`);
        
        for (const linkedEntity of this.linkedEntities) {
            if (!this.generatedPages.has(linkedEntity)) {
                const filename = this.sanitizeFilename(linkedEntity) + '.html';
                const outputPath = path.join(this.outputDir, filename);
                
                if (!fs.existsSync(outputPath)) {
                    const stubHtml = this.generateStubPage(linkedEntity);
                    fs.writeFileSync(outputPath, stubHtml, 'utf8');
                    console.log(`📝 Created stub: ${outputPath}`);
                }
            }
        }
    }

    /**
     * Find all boss character files (both regular bosses and maximum bosses)
     */
    findAllBossCharacters() {
        const bossFiles = [];
        
        try {
            // Look for boss directories under dynasties
            const dynastiesPath = path.join(this.entitiesDir, 'cyberdynasties');
            if (!fs.existsSync(dynastiesPath)) {
                console.log(`⚠️  Dynasties directory not found: ${dynastiesPath}`);
                return bossFiles;
            }
            
            // Recursively search for boss files
            this.searchForAllBosses(dynastiesPath, bossFiles);
            
        } catch (error) {
            console.error(`❌ Error searching for boss characters:`, error.message);
        }
        
        return bossFiles;
    }
    
    /**
     * Recursively search for all boss character files (regular + maximum)
     */
    searchForAllBosses(dir, bossFiles) {
        try {
            const items = fs.readdirSync(dir);
            
            for (const item of items) {
                const itemPath = path.join(dir, item);
                const stat = fs.statSync(itemPath);
                
                if (stat.isDirectory()) {
                    // If this is a "bosses" directory, look for all boss files
                    if (item === 'bosses') {
                        this.searchForBossFiles(itemPath, bossFiles);
                    } else {
                        // Continue searching recursively
                        this.searchForAllBosses(itemPath, bossFiles);
                    }
                }
            }
        } catch (error) {
            console.error(`❌ Error reading directory ${dir}:`, error.message);
        }
    }
    
    /**
     * Search for boss files in a bosses directory (handles both regular bosses and maximumboss)
     */
    searchForBossFiles(bossesDir, bossFiles) {
        try {
            const items = fs.readdirSync(bossesDir);
            
            for (const item of items) {
                const itemPath = path.join(bossesDir, item);
                const stat = fs.statSync(itemPath);
                
                if (stat.isDirectory()) {
                    if (item === 'maximumboss') {
                        // Handle maximum boss structure: maximumboss/BossName/states/state/file.md
                        this.searchMaximumBossFiles(itemPath, bossFiles, 'Maximum Boss');
                    } else {
                        // Handle regular boss structure: BossName/states/state/file.md
                        this.searchRegularBossFiles(itemPath, bossFiles, 'Regular Boss');
                    }
                } else if (item.endsWith('.md')) {
                    // Direct .md file in bosses directory
                    bossFiles.push({
                        path: itemPath,
                        type: 'Direct Boss',
                        name: path.basename(item, '.md')
                    });
                    console.log(`🎯 Found Direct Boss: ${item}`);
                }
            }
        } catch (error) {
            console.error(`❌ Error reading bosses directory ${bossesDir}:`, error.message);
        }
    }
    
    /**
     * Search for maximum boss files
     */
    searchMaximumBossFiles(maximumBossDir, bossFiles, type) {
        try {
            const bosses = fs.readdirSync(maximumBossDir);
            
            for (const bossName of bosses) {
                const bossPath = path.join(maximumBossDir, bossName);
                if (fs.statSync(bossPath).isDirectory()) {
                    this.searchBossStates(bossPath, bossFiles, `${type} - ${bossName}`);
                }
            }
        } catch (error) {
            console.error(`❌ Error reading maximum boss directory ${maximumBossDir}:`, error.message);
        }
    }
    
    /**
     * Search for regular boss files
     */
    searchRegularBossFiles(bossDir, bossFiles, type) {
        try {
            const bossName = path.basename(bossDir);
            this.searchBossStates(bossDir, bossFiles, `${type} - ${bossName}`);
        } catch (error) {
            console.error(`❌ Error reading regular boss directory ${bossDir}:`, error.message);
        }
    }
    
    /**
     * Search for markdown files in boss states
     */
    searchBossStates(bossDir, bossFiles, bossInfo) {
        try {
            const statesPath = path.join(bossDir, 'states');
            if (!fs.existsSync(statesPath)) {
                // Check if there are .md files directly in the boss directory
                this.searchDirectMarkdownFiles(bossDir, bossFiles, bossInfo);
                return;
            }
            
            const states = fs.readdirSync(statesPath);
            
            for (const state of states) {
                const statePath = path.join(statesPath, state);
                if (fs.statSync(statePath).isDirectory()) {
                    this.searchDirectMarkdownFiles(statePath, bossFiles, `${bossInfo} (${state})`);
                }
            }
        } catch (error) {
            console.error(`❌ Error reading boss states ${bossDir}:`, error.message);
        }
    }
    
    /**
     * Search for .md files directly in a directory
     */
    searchDirectMarkdownFiles(dir, bossFiles, bossInfo) {
        try {
            const items = fs.readdirSync(dir);
            
            for (const item of items) {
                if (item.endsWith('.md')) {
                    const filePath = path.join(dir, item);
                    bossFiles.push({
                        path: filePath,
                        type: bossInfo,
                        name: path.basename(item, '.md')
                    });
                    console.log(`🎯 Found ${bossInfo}: ${item}`);
                }
            }
        } catch (error) {
            console.error(`❌ Error reading directory ${dir}:`, error.message);
        }
    }

    /**
     * Main generation method - process all boss characters
     */
    async generateAllBossCharacters() {
        console.log(`🚀 Starting Entity Page Generator - All Boss Characters`);
        
        this.init();
        
        // Find all boss character files
        const bossFiles = this.findAllBossCharacters();
        
        if (bossFiles.length === 0) {
            console.error(`❌ No boss character files found in entities directory`);
            return false;
        }
        
        console.log(`\n📊 Found ${bossFiles.length} boss character(s) to process:`);
        bossFiles.forEach(boss => {
            console.log(`   📋 ${boss.type}: ${boss.name}`);
        });
        
        let successCount = 0;
        
        // Generate pages for each boss
        for (const bossFile of bossFiles) {
            const success = await this.generateSingleEntity(bossFile.path);
            if (success) {
                successCount++;
            }
        }
        
        if (successCount > 0) {
            // Generate stub pages for any linked entities
            this.generateStubPages();
            
            console.log(`\n🎉 SUCCESS! Generated entity pages:`);
            console.log(`📁 Output directory: ${this.outputDir}`);
            console.log(`👑 Boss characters processed: ${successCount}/${bossFiles.length}`);
            console.log(`🔗 Linked entities found: ${this.linkedEntities.size}`);
            console.log(`📄 Total pages generated: ${this.generatedPages.size + this.linkedEntities.size - this.generatedPages.size}`);
            
            return true;
        }
        
        return false;
    }
}

// Run the generator if called directly
if (require.main === module) {
    const generator = new EntityPageGenerator();
    generator.generateAllBossCharacters().then(success => {
        if (success) {
            console.log(`\n🌟 All boss character pages generated successfully!`);
            console.log(`\n🔗 Navigation tip: Open any HTML file in the html/ directory to start exploring your character universe!`);
        } else {
            console.error(`\n💥 Boss character generation failed.`);
            process.exit(1);
        }
    }).catch(error => {
        console.error(`\n💥 Error during generation:`, error);
        process.exit(1);
    });
}

module.exports = EntityPageGenerator;
