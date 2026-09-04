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

        // 1. Content Moderation (NSFW & Toxicity Filter)
        const nsfwKeywords = [
            'porn', 'hentai', 'xxx', 'sex', 'nude', 'erotic', 'nsfw', '18+', 'adult', 
            'dick', 'pussy', 'boobs', 'vagina', 'penis', 'порно', 'секс', 'хентай', 'сиськи', 'член'
        ];
        const textToCheck = `${theme.id} ${theme.name} ${theme.description || ''} ${(theme.tags || []).join(' ')}`.toLowerCase();
        for (const word of nsfwKeywords) {
            if (textToCheck.includes(word)) {
                console.error(`❌ Security/Moderation Violation in ${folder}: Prohibited NSFW keyword "${word}" detected.`);
                hasErrors = true;
            }
        }

        // 2. Strict Security: Block executable or dangerous files (.exe, .dll, .apk, .js, .sh, etc.)
        const allowedExtensions = ['.json', '.png', '.jpg', '.jpeg', '.webp', '.svg', '.mp4', '.webm', '.wav', '.mp3', '.ttf', '.otf'];
        function scanFiles(dir) {
            const files = fs.readdirSync(dir, { withFileTypes: true });
            for (const f of files) {
                const fullPath = path.join(dir, f.name);
                if (f.isDirectory()) {
                    scanFiles(fullPath);
                } else {
                    const ext = path.extname(f.name).toLowerCase();
                    if (!allowedExtensions.includes(ext)) {
                        console.error(`❌ Security Violation in ${folder}: Prohibited file extension "${ext}" (${f.name})!`);
                        hasErrors = true;
                    }
                    const stat = fs.statSync(fullPath);
                    if (stat.size > 15 * 1024 * 1024) {
                        console.error(`❌ Size Violation in ${folder}: File ${f.name} exceeds 15 MB limit!`);
                        hasErrors = true;
                    }
                }
            }
        }
        scanFiles(path.join(themesDir, folder));

        // 3. Schema & Required Fields Validation
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

let shouldWrite = true;
let existingGeneratedAt = new Date().toISOString();

if (fs.existsSync(catalogFile)) {
    try {
        const existing = JSON.parse(fs.readFileSync(catalogFile, 'utf8'));
        existingGeneratedAt = existing.generatedAt || existingGeneratedAt;
        if (JSON.stringify(existing.themes) === JSON.stringify(catalog)) {
            shouldWrite = false;
            console.log(`✨ catalog.json is already up to date (${catalog.length} themes).`);
        }
    } catch (e) {
        // overwrite on parse error
    }
}

if (shouldWrite) {
    const finalCatalog = {
        schemaVersion: '4.0.0',
        generatedAt: new Date().toISOString(),
        totalThemes: catalog.length,
        themes: catalog
    };
    fs.writeFileSync(catalogFile, JSON.stringify(finalCatalog, null, 2), 'utf8');
    console.log(`🎉 Successfully generated catalog.json with ${catalog.length} themes!`);
}
