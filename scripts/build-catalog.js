const fs = require('fs');
const path = require('path');

const rootDir = path.resolve(__dirname, '..');
const themesDir = path.join(rootDir, 'themes');
const catalogFile = path.join(rootDir, 'catalog.json');

if (!fs.existsSync(themesDir)) {
    console.error('Directory themes/ does not exist!');
    process.exit(1);
}

const themeFolders = fs.readdirSync(themesDir, { withFileTypes: true })
    .filter(dirent => dirent.isDirectory())
    .map(dirent => dirent.name);

const catalog = [];
let hasErrors = false;

for (const folder of themeFolders) {
    const themeJsonPath = path.join(themesDir, folder, 'theme.json');
    if (!fs.existsSync(themeJsonPath)) {
        console.warn(`⚠️ Skipping ${folder}: theme.json not found`);
        continue;
    }

    try {
        const raw = fs.readFileSync(themeJsonPath, 'utf8');
        const theme = JSON.parse(raw);

        // Validation
        if (!theme.id || theme.id !== folder) {
            console.error(`❌ Error in ${folder}: theme.id ("${theme.id}") must match folder name ("${folder}")`);
            hasErrors = true;
        }
        if (!theme.name || !theme.author || !theme.version) {
            console.error(`❌ Error in ${folder}: name, author, and version are required`);
            hasErrors = true;
        }
        if (!theme.core || !theme.core.colors || !theme.core.colors.Primary || !theme.core.colors.BgBase) {
            console.error(`❌ Error in ${folder}: core.colors.Primary and core.colors.BgBase are required`);
            hasErrors = true;
        }

        // Icon and Preview image check
        const iconPng = path.join(themesDir, folder, 'icon.png');
        const iconJpg = path.join(themesDir, folder, 'icon.jpg');
        const iconFile = fs.existsSync(iconPng) ? 'icon.png' : (fs.existsSync(iconJpg) ? 'icon.jpg' : null);

        const previewPng = path.join(themesDir, folder, 'preview.png');
        const previewJpg = path.join(themesDir, folder, 'preview.jpg');
        const previewFile = fs.existsSync(previewPng) ? 'preview.png' : (fs.existsSync(previewJpg) ? 'preview.jpg' : null);

        // Feature flags
        const hasSounds = !!(theme.core?.sounds || theme.apps?.obxodka?.sounds);
        const hasVideo = theme.background?.type === 'video';
        const hasFrames = !!(theme.decorations?.screenFrame || theme.decorations?.cardFrame);
        const hasIdolButton = theme.apps?.obxodka?.tunnelButton?.style === 'custom_image';

        const catalogItem = {
            id: theme.id,
            name: theme.name,
            author: theme.author,
            version: theme.version,
            description: theme.description || '',
            tags: theme.tags || [],
            supportedApps: theme.supportedApps || ['*'],
            iconUrl: iconFile ? `https://raw.githubusercontent.com/OctoCore-Dev/themes/main/themes/${folder}/${iconFile}` : null,
            previewUrl: previewFile ? `https://raw.githubusercontent.com/OctoCore-Dev/themes/main/themes/${folder}/${previewFile}` : null,
            primaryColor: theme.core.colors.Primary,
            backgroundColor: theme.core.colors.BgBase,
            accentColor: theme.core.colors.Accent || theme.core.colors.Primary,
            features: {
                hasSounds,
                hasVideo,
                hasFrames,
                hasIdolButton,
                hasParticles: !!(theme.vfx && theme.vfx.particles && theme.vfx.particles !== 'none')
            },
            updatedAt: new Date().toISOString()
        };

        catalog.push(catalogItem);
        console.log(`✅ Validated theme: ${theme.name} (${folder})`);
    } catch (err) {
        console.error(`❌ Failed to parse ${themeJsonPath}: ${err.message}`);
        hasErrors = true;
    }
}

if (hasErrors) {
    console.error('Validation failed. Aborting catalog generation.');
    process.exit(1);
}

const finalCatalog = {
    schemaVersion: '4.0.0',
    generatedAt: new Date().toISOString(),
    totalThemes: catalog.length,
    themes: catalog
};

fs.writeFileSync(catalogFile, JSON.stringify(finalCatalog, null, 2), 'utf8');
console.log(`🎉 Successfully generated catalog.json with ${catalog.length} themes!`);
