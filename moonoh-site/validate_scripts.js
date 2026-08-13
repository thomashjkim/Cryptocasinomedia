const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('🔍 Running automated codebase JS syntax & integrity check...');

const filesToValidate = ['explore.html', 'index.html', 'about.html', 'contact.html', 'press.html'];

let hasError = false;

filesToValidate.forEach(file => {
  const filePath = path.join(__dirname, file);
  if (!fs.existsSync(filePath)) return;

  const html = fs.readFileSync(filePath, 'utf8');
  
  // Extract all script blocks using regex
  const scriptRegex = /<script\b[^>]*>([\s\S]*?)<\/script>/gi;
  let match;
  let scriptCount = 0;

  while ((match = scriptRegex.exec(html)) !== null) {
    const fullTag = match[0];
    const scriptCode = match[1];

    // Ignore src scripts or JSON-LD scripts
    if (fullTag.includes('src=') || fullTag.includes('application/ld+json')) continue;
    if (!scriptCode.trim()) continue;

    scriptCount++;
    const tempFile = path.join('/tmp', `validate_${file}_${scriptCount}.js`);
    fs.writeFileSync(tempFile, scriptCode);

    try {
      execSync(`node -c "${tempFile}"`, { stdio: 'pipe' });
    } catch (e) {
      console.error(`❌ [SYNTAX ERROR] ${file} JS script block #${scriptCount}:`);
      console.error(e.stderr.toString());
      hasError = true;
    } finally {
      if (fs.existsSync(tempFile)) fs.unlinkSync(tempFile);
    }
  }
});

if (hasError) {
  console.error('❌ Validation failed! Fix syntax errors before committing/deploying.');
  process.exit(1);
} else {
  console.log('✅ All executable JS script blocks passed automated syntax validation with 0 errors!');
}
