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

// ─── Security Limits & Whitelists ───────────────────────────────────────────
const allowedExtensions = ['.json', '.png', '.jpg', '.jpeg', '.webp', '.mp4', '.webm', '.wav', '.mp3', '.ttf', '.otf'];

const sizeLimits = {
    '.mp4': 20 * 1024 * 1024,
    '.webm': 20 * 1024 * 1024,
    '.wav': 5 * 1024 * 1024,
    '.mp3': 5 * 1024 * 1024,
    '.png': 5 * 1024 * 1024,
    '.jpg': 5 * 1024 * 1024,
    '.jpeg': 5 * 1024 * 1024,
    '.webp': 5 * 1024 * 1024,
    '.ttf': 5 * 1024 * 1024,
    '.otf': 5 * 1024 * 1024,
    '.json': 512 * 1024
};

const MAX_THEME_TOTAL_SIZE = 35 * 1024 * 1024; // 35 MB

function checkMagicBytes(filePath, ext, buffer) {
    if (!buffer || buffer.length === 0) {
        return 'Empty file (0 bytes)';
    }

    // 1. Explicitly reject known dangerous / executable headers
    if (buffer.length >= 2 && buffer[0] === 0x4D && buffer[1] === 0x5A) {
        return 'Blocked executable header: DOS/Windows PE (MZ)';
    }
    if (buffer.length >= 4 && buffer[0] === 0x7F && buffer[1] === 0x45 && buffer[2] === 0x4C && buffer[3] === 0x46) {
        return 'Blocked executable header: Linux ELF';
    }
    if (buffer.length >= 4) {
        const m = buffer.readUInt32BE(0);
        if (m === 0xFEEDFACE || m === 0xFEEDFACF || m === 0xCEFAEDFE || m === 0xCFFAEDFE) {
            return 'Blocked executable header: macOS Mach-O';
        }
    }
    if (buffer.length >= 2 && buffer[0] === 0x23 && buffer[1] === 0x21) {
        return 'Blocked script header: Shebang (#!)';
    }
    if (buffer.length >= 4 && buffer[0] === 0xCA && buffer[1] === 0xFE && buffer[2] === 0xBA && buffer[3] === 0xBE) {
        return 'Blocked executable header: Java Class (CAFEBABE)';
    }
    if (buffer.length >= 4 && buffer[0] === 0x50 && buffer[1] === 0x4B && buffer[2] === 0x03 && buffer[3] === 0x04) {
        return 'Blocked archive: ZIP container disguised as media file';
    }
    if (buffer.length >= 4 && buffer[0] === 0x4C && buffer[1] === 0x00 && buffer[2] === 0x00 && buffer[3] === 0x00) {
        return 'Blocked shortcut: Windows LNK file';
    }

    // 2. Validate expected format signatures
    switch (ext) {
        case '.png':
            if (buffer.length < 8 ||
                buffer[0] !== 0x89 || buffer[1] !== 0x50 || buffer[2] !== 0x4E || buffer[3] !== 0x47 ||
                buffer[4] !== 0x0D || buffer[5] !== 0x0A || buffer[6] !== 0x1A || buffer[7] !== 0x0A) {
                return 'Invalid PNG signature (expected 89 50 4E 47 0D 0A 1A 0A)';
            }
            return null;

        case '.jpg':
        case '.jpeg':
            if (buffer.length < 3 || buffer[0] !== 0xFF || buffer[1] !== 0xD8 || buffer[2] !== 0xFF) {
                return 'Invalid JPEG signature (expected FF D8 FF)';
            }
            return null;

        case '.webp':
            if (buffer.length < 12 ||
                buffer[0] !== 0x52 || buffer[1] !== 0x49 || buffer[2] !== 0x46 || buffer[3] !== 0x46 ||
                buffer[8] !== 0x57 || buffer[9] !== 0x45 || buffer[10] !== 0x42 || buffer[11] !== 0x50) {
                return 'Invalid WebP signature (expected RIFF....WEBP)';
            }
            return null;

        case '.mp4':
            if (buffer.length < 8 ||
                buffer[4] !== 0x66 || buffer[5] !== 0x74 || buffer[6] !== 0x79 || buffer[7] !== 0x70) {
                return 'Invalid MP4 container: missing ftyp box at offset 4';
            }
            return null;

        case '.webm':
            if (buffer.length < 4 ||
                buffer[0] !== 0x1A || buffer[1] !== 0x45 || buffer[2] !== 0xDF || buffer[3] !== 0xA3) {
                return 'Invalid WebM/Matroska EBML header (expected 1A 45 DF A3)';
            }
            return null;

        case '.wav':
            if (buffer.length < 12 ||
                buffer[0] !== 0x52 || buffer[1] !== 0x49 || buffer[2] !== 0x46 || buffer[3] !== 0x46 ||
                buffer[8] !== 0x57 || buffer[9] !== 0x41 || buffer[10] !== 0x56 || buffer[11] !== 0x45) {
                return 'Invalid WAV signature (expected RIFF....WAVE)';
            }
            return null;

        case '.mp3':
            const isId3 = buffer.length >= 3 && buffer[0] === 0x49 && buffer[1] === 0x44 && buffer[2] === 0x33;
            const isMpegSync = buffer.length >= 2 && buffer[0] === 0xFF && (buffer[1] & 0xE0) === 0xE0;
            if (!isId3 && !isMpegSync) {
                return 'Invalid MP3 audio frame / ID3 signature';
            }
            return null;

        case '.ttf':
            const isTrueType = buffer.length >= 4 && (
                (buffer[0] === 0x00 && buffer[1] === 0x01 && buffer[2] === 0x00 && buffer[3] === 0x00) ||
                (buffer[0] === 0x74 && buffer[1] === 0x72 && buffer[2] === 0x75 && buffer[3] === 0x65)
            );
            if (!isTrueType) {
                return 'Invalid TrueType font signature';
            }
            return null;

        case '.otf':
            if (buffer.length < 4 ||
                buffer[0] !== 0x4F || buffer[1] !== 0x54 || buffer[2] !== 0x54 || buffer[3] !== 0x4F) {
                return 'Invalid OpenType font signature (missing OTTO)';
            }
            return null;

        case '.json':
            try {
                const str = buffer.toString('utf8');
                JSON.parse(str);
            } catch (e) {
                return `Invalid JSON syntax: ${e.message}`;
            }
            return null;

        default:
            return `Unsupported file format: ${ext}`;
    }
}

function validateRelativeAssetPath(baseDir, relPath) {
    if (!relPath || typeof relPath !== 'string') return null;
    if (relPath.includes('..') || relPath.startsWith('/') || relPath.startsWith('\\') || relPath.includes(':')) {
        return `Unsafe relative path: "${relPath}"`;
    }
    const resolved = path.resolve(baseDir, relPath);
    if (!resolved.startsWith(baseDir)) {
        return `Path traversal detected: "${relPath}" escapes theme directory`;
    }
    if (!fs.existsSync(resolved)) {
        return `Referenced file does not exist: "${relPath}"`;
    }
    return null;
}

for (const folder of themeFolders) {
    const currentThemeDir = path.join(themesDir, folder);
    const themeJsonPath = path.join(currentThemeDir, 'theme.json');
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

        // 2. Strict Security: Block executable, dangerous, or unverified files
        let totalThemeBytes = 0;
        function scanFiles(dir) {
            const files = fs.readdirSync(dir, { withFileTypes: true });
            for (const f of files) {
                const fullPath = path.join(dir, f.name);
                if (f.isDirectory()) {
                    scanFiles(fullPath);
                } else {
                    if (f.name.startsWith('.')) {
                        console.error(`❌ Security Violation in ${folder}: Hidden file "${f.name}" is forbidden!`);
                        hasErrors = true;
                        continue;
                    }

                    const ext = path.extname(f.name).toLowerCase();
                    if (!allowedExtensions.includes(ext)) {
                        console.error(`❌ Security Violation in ${folder}: Prohibited file extension "${ext}" (${f.name})!`);
                        hasErrors = true;
                        continue;
                    }

                    const stat = fs.statSync(fullPath);
                    totalThemeBytes += stat.size;

                    const maxLimit = sizeLimits[ext] || (5 * 1024 * 1024);
                    if (stat.size > maxLimit) {
                        console.error(`❌ Size Violation in ${folder}: File ${f.name} (${(stat.size / 1024 / 1024).toFixed(2)} MB) exceeds limit of ${(maxLimit / 1024 / 1024).toFixed(2)} MB!`);
                        hasErrors = true;
                    }

                    const headerSize = Math.min(stat.size, 64);
                    const fd = fs.openSync(fullPath, 'r');
                    const buffer = Buffer.alloc(headerSize);
                    fs.readSync(fd, buffer, 0, headerSize, 0);
                    fs.closeSync(fd);

                    const fullBuf = ext === '.json' ? fs.readFileSync(fullPath) : buffer;
                    const magicError = checkMagicBytes(fullPath, ext, fullBuf);
                    if (magicError) {
                        console.error(`❌ Magic Bytes Security Failure in ${folder}/${f.name}: ${magicError}`);
                        hasErrors = true;
                    }
                }
            }
        }
        scanFiles(currentThemeDir);

        if (totalThemeBytes > MAX_THEME_TOTAL_SIZE) {
            console.error(`❌ Size Violation in ${folder}: Total theme size (${(totalThemeBytes / 1024 / 1024).toFixed(2)} MB) exceeds limit of ${(MAX_THEME_TOTAL_SIZE / 1024 / 1024).toFixed(2)} MB!`);
            hasErrors = true;
        }

        // 3. Schema & Required Fields Validation
        if (!theme.id || theme.id !== folder) {
            console.error(`❌ Error in ${folder}: theme.id ("${theme.id}") must match folder name ("${folder}")`);
            hasErrors = true;
        }
        if (!/^[a-z0-9\-_]+$/.test(theme.id)) {
            console.error(`❌ Error in ${folder}: theme.id must contain only lowercase letters, digits, dashes, and underscores`);
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

        // 4. Validate asset paths referenced in theme.json
        const pathsToVerify = [
            theme.background?.imageSource,
            theme.background?.videoSource,
            theme.background?.fallbackImage,
            theme.decorations?.screenFrame,
            theme.decorations?.cardFrame,
            theme.decorations?.buttonImageIdle,
            theme.decorations?.buttonImageActive,
            theme.decorations?.buttonVideoIdle,
            theme.decorations?.buttonVideoActive,
            theme.vfx?.particleSprite,
            theme.core?.sounds?.connect,
            theme.core?.sounds?.click,
            theme.core?.ui?.fontFile
        ];

        if (theme.decorations?.cornerStickers) {
            for (const rel of Object.values(theme.decorations.cornerStickers)) {
                pathsToVerify.push(rel);
            }
        }

        for (const p of pathsToVerify) {
            if (p) {
                const err = validateRelativeAssetPath(currentThemeDir, p);
                if (err) {
                    console.error(`❌ Path Violation in ${folder}: ${err}`);
                    hasErrors = true;
                }
            }
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
        const hasVideo = theme.background?.type === 'video' || !!theme.background?.videoSource;
        const hasFrames = !!(theme.decorations?.screenFrame || theme.decorations?.cardFrame || theme.decorations?.cornerStickers);
        const hasIdolButton = !!(theme.decorations?.buttonImageIdle || theme.decorations?.buttonImageConnecting || theme.decorations?.buttonImageActive || theme.decorations?.buttonImageError || theme.apps?.obxodka?.tunnelButton?.style === 'custom_image');
        const hasButtonVideo = !!(theme.decorations?.buttonVideoIdle || theme.decorations?.buttonVideoConnecting || theme.decorations?.buttonVideoActive || theme.decorations?.buttonVideoError);

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
                hasButtonVideo,
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
