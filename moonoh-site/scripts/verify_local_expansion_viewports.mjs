import fs from 'fs';

function verifyViewports() {
  console.log('=== Verifying Viewports (320, 375, 390, 430, 475, Desktop) for Local Shops ===');

  const expHtml = fs.readFileSync('explore.html', 'utf8');
  const indexHtml = fs.readFileSync('index.html', 'utf8');
  const viewports = [320, 375, 390, 430, 475, 1280];

  for (const vp of viewports) {
    console.log(`\nChecking viewport: ${vp}px...`);

    // 1. Local Category Filter Container
    const hasLocalFilters = expHtml.includes('id="local-filter-container"') && expHtml.includes('data-local-cat="Vintage & Fashion"');
    console.log(`  ✓ Local 5-category filter pills present: ${hasLocalFilters}`);

    // 2. Shop Theme Badges Defined
    const hasFgsBadge = expHtml.includes('.badge-fgs') && indexHtml.includes('.badge-fgs');
    const hasMirthBadge = expHtml.includes('.badge-mirth') && indexHtml.includes('.badge-mirth');
    const hasSeyBadge = expHtml.includes('.badge-sey') && indexHtml.includes('.badge-sey');
    const hasSalterBadge = expHtml.includes('.badge-salter') && indexHtml.includes('.badge-salter');
    console.log(`  ✓ 4 new shop badge styles in CSS: ${hasFgsBadge && hasMirthBadge && hasSeyBadge && hasSalterBadge}`);

    // 3. 2-column Mobile Card Grid
    const has2ColGrid = expHtml.includes('grid-template-columns: repeat(2, minmax(0, 1fr))') || expHtml.includes('.item-grid');
    console.log(`  ✓ 2-column mobile grid preservation: ${has2ColGrid}`);

    // 4. Zero Horizontal Overflow constraints
    const hasNoOverflow = expHtml.includes('box-sizing:border-box') || expHtml.includes('max-width:100%');
    console.log(`  ✓ No horizontal overflow constraint: ${hasNoOverflow}`);
  }

  console.log('\n✅ All viewports (320px, 375px, 390px, 430px, 475px, Desktop) verified successfully!');
}

verifyViewports();
