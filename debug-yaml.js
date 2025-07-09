const yaml = require('js-yaml');

const testYaml = `
memory_focus: ["[[present]]", "[[past]]", "[[data_patterns]]", "[[information_flows]]"]
`;

try {
    const result = yaml.load(testYaml);
    console.log('SUCCESS:', result);
} catch (error) {
    console.log('ERROR:', error.message);
}
