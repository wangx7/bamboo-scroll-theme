const fs = require('fs');
const path = require('path');

const PREVIEW_DIR = path.join(__dirname, '../previews');

const files = [
  {
    name: 'ink-wash-light-preview.html',
    vars: `
        --paper-0: #F5F2ED;
        --paper-1: #EFECE8;
        --paper-2: #E2DFDB;
        --ink-900: #3a3631;
        --ink-700: #6b665e;
        --ink-500: #8e877a;
        --line: #d5d2ce;
        --focus: #2f6488;
        --tk-comment: #6B655A;
        --tk-keyword: #24445E;
        --tk-type: #3E5F99;
        --tk-function: #2F6488;
        --tk-string: #2F6B57;
        --tk-number: #B2473E;
        --tk-variable: #3A3631;
        --tk-operator: #24445E;
        --tk-json-prop: #7A5C38;
        --tk-parameter: #7D5C32;
        --tk-annotation: #3E5F99;
        --tk-boolean: #B2473E;
        --tk-null: #B2473E;
        --tk-punctuation: #7A7468;
        --line-focus: #EAE7E360;
        --shadow: rgba(58, 54, 49, 0.12);
    `
  },
  {
    name: 'bamboo-green-light-preview.html',
    vars: `
        --paper-0: #789262;
        --paper-1: #8DA272;
        --paper-2: #96AB81;
        --ink-900: #0A0A0A;
        --ink-700: #102610;
        --ink-500: #556B4C;
        --line: #556B4C;
        --focus: #001B42;
        --tk-comment: #102610;
        --tk-keyword: #001B42;
        --tk-type: #2E0033;
        --tk-function: #052616;
        --tk-string: #47000B;
        --tk-number: #361B00;
        --tk-variable: #0A0A0A;
        --tk-operator: #001B42;
        --tk-json-prop: #2E0033;
        --tk-parameter: #361B00;
        --tk-annotation: #2E0033;
        --tk-boolean: #361B00;
        --tk-null: #361B00;
        --tk-punctuation: #0A0A0A;
        --line-focus: #8DA27270;
        --shadow: rgba(10, 10, 10, 0.12);
    `
  },
  {
    name: 'ink-wash-painting-preview.html',
    vars: `
        --paper-0: #F5F2ED;
        --paper-1: #EFECE8;
        --paper-2: #E2DFDB;
        --ink-900: #1a1a1a;
        --ink-700: #3d3d3d;
        --ink-500: #8a8a8a;
        --line: #d5d2ce;
        --focus: #2a5f8a;
        --tk-comment: #C2C2C2;
        --tk-keyword: #1A1A1A;
        --tk-type: #3D3D3D;
        --tk-function: #2A5F8A;
        --tk-string: #3A7D44;
        --tk-number: #A93226;
        --tk-variable: #3D3D3D;
        --tk-operator: #1A1A1A;
        --tk-json-prop: #5C5C5C;
        --tk-parameter: #5C5C5C;
        --tk-annotation: #3D3D3D;
        --tk-boolean: #A93226;
        --tk-null: #A93226;
        --tk-punctuation: #8A8A8A;
        --line-focus: #EAE7E360;
        --shadow: rgba(26, 26, 26, 0.12);
    `
  }
];

files.forEach(fileDef => {
  const filePath = path.join(PREVIEW_DIR, fileDef.name);
  if (!fs.existsSync(filePath)) {
    console.log("File not found:", fileDef.name);
    return;
  }
  let content = fs.readFileSync(filePath, 'utf8');

  // Replace CSS :root vars
  content = content.replace(/:root\s*\{[^}]+\}/m, ':root {' + fileDef.vars + '}');

  fs.writeFileSync(filePath, content);
  console.log("Updated", fileDef.name);
});
