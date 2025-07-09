const fs = require('fs');
const yaml = require('js-yaml');

// Test parsing one specific file
const filePath = "entities/cyberdynasties/cybernetic/the_chrome_mandarins/bosses/ByteEmperor/states/ascendant/byteemperor.md";

try {
    const content = fs.readFileSync(filePath, 'utf8');
    console.log("File length:", content.length);
    console.log("First 200 chars:", JSON.stringify(content.substring(0, 200)));
    
    const yamlMatch = content.match(/^---\n([\s\S]*?)\n---/);
    console.log("YAML match found:", !!yamlMatch);
    
    if (yamlMatch) {
        console.log("YAML content length:", yamlMatch[1].length);
        console.log("First 100 chars of YAML:", yamlMatch[1].substring(0, 100));
        
        const parsed = yaml.load(yamlMatch[1]);
        console.log("Parsed successfully! Name:", parsed.name);
    }
} catch (error) {
    console.error("Error:", error.message);
}
