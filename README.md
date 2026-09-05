# 🎨 OctoCore Themes Hub (Universal Community Theme Hub)

Открытый репозиторий тем оформления для всей экосистемы приложений **OctoCore** (VPN `obxodka`, Карты и туризм, Чат, B2B SaaS).

[![Validate Themes & Build Catalog](https://github.com/OctoCore-Dev/themes/actions/workflows/validate-and-catalog.yml/badge.svg)](https://github.com/OctoCore-Dev/themes/actions/workflows/validate-and-catalog.yml)
[![Catalog](https://img.shields.io/badge/Catalog-v4.0.0-blueviolet)](catalog.json)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 🌟 Возможности кастомизации

Движок тем Obxodka & OctoCore поддерживает **полный спектр современного мультимедиа**:

* 🎬 **Живые видео-фоны приложения (`background.videoSource`):**
  * Поддерживаются форматы **MP4** и **WebM** (аппаратное ускорение, автоматическое бесшовное зацикливание, без звука).
  * Параметр `opacity` (0.0 — 1.0) позволяет отрегулировать яркость видеофона, чтобы интерфейс оставался контрастным.
  * Рекомендуется указывать и `imageSource` — он отображается как быстрый постер до старта видеопотока или на слабых устройствах.

* 🌸 **Живая кнопка с видео и прозрачным фоном (`decorations.buttonVideo...`):**
  * **Бывают ли видео с прозрачным фоном? ДА!** Обычный MP4 прозрачность не поддерживает, но форматы **Animated WebP (.webp)** и **APNG (.png)** имеют полноценный 8-битный альфа-канал.
  * Графический движок **SkiaSharp** (`SKAnimatedImage`) рендерит их на лету с сохранением всех полутеней и органичных краёв (лепесток сакуры, пламя, крутящаяся сфера, аниме-персонаж) — **никаких грубых квадратных или круглых обрезаний**!
  * **Раздельные состояния кнопки:**
    * `buttonVideoIdle` — живая анимация кнопки в режиме ожидания (VPN отключен).
    * `buttonVideoActive` — живая анимация кнопки в режиме защиты (VPN подключен).
  * **Статичные альтернативы:** `buttonImageIdle` и `buttonImageActive` (PNG/WebP).
  * При переключении VPN между состояниями срабатывает кинематографичный **Cross-Fade** с мягким пружинящим масштабированием, а неоновые кольца и аура светятся позади.

* 🖼️ **Дизайнерские рамки и угловые стикеры с умным скрытием:**
  * `screenFrame` — рамка на весь экран (заменяет системную рамку окна).
  * `cornerStickers` — независимые стикеры по углам экрана (`topLeft`, `topRight`, `bottomLeft`, `bottomRight`).
  * **Perimeter Proximity Fade:** при приближении курсора мыши к краям или углам окна рамка и стикеры мгновенно и плавно растворяются (fade-out за 120 мс), открывая доступ к кнопкам и карточкам.

* 🌸 **VFX-частицы (`vfx`):** Лепестки сакуры, неоновые искры, снег, дождь или кастомный спрайт (`particleSprite`).
* 🎵 **Звуковые паки (`core.sounds`):** Звуки кликов, подключения и отключения VPN.
* 🎨 **Цветовая палитра и градиенты:** Полный набор токенов `Primary`, `BgBase`, `BgSurface`, `Accent`.

* 🤖 **Умное автоопределение форматов движком:**
  * **Фон:** Клиент сам анализирует расширения файлов. Даже если автор темы указал видео в `imageSource` или фото в `videoSource`, код автоматически определит тип контента и направит его в нужный рендерер (видеоплеер `MediaElement` или фоновый постер `Image`).
  * **Кнопка:** Для кнопки **всегда требуется прозрачный фон** (альфа-канал), чтобы форма оставалась органичной, а не квадратной плашкой. Код сам проверяет, содержит ли файл анимацию (`.webp`, `.apng`, `.gif`), и мгновенно переключается между покадровым 60 FPS SkiaSharp-плеером и нативным статичным рендером, сохраняя свечение неоновой ауры сзади.

---

### 💡 Как сделать видео кнопки с прозрачным фоном (Animated WebP)

Любое видео или секвенцию кадров можно перевести в прозрачный **Animated WebP** одной командой через `ffmpeg`:
```bash
# Из видео с альфа-каналом (например, ProRes 4444 или QuickTime PNG):
ffmpeg -i input.mov -vcodec libwebp -filter:v fps=fps=30 -lossless 0 -compression_level 4 -q:v 75 -loop 0 button_active.webp

# Из серии прозрачных PNG-картинок:
ffmpeg -framerate 30 -i frame_%03d.png -vcodec libwebp -lossless 0 -q:v 80 -loop 0 button_idle.webp
```

---

## 📄 Пример манифеста темы с видео-фоном и анимированной кнопкой

```json
{
  "$schema": "../../schemas/theme.v4.json",
  "id": "sakura-live",
  "name": "Sakura Live Bloom",
  "author": "OctoCore Community",
  "version": "1.1.0",
  "description": "Живая тема с видео-фоном падающих лепестков, анимированной сакурой на кнопке и угловыми ветвями",
  "tags": ["anime", "sakura", "live", "video"],
  "core": {
    "colors": {
      "BgBase": "#100912",
      "BgSurface": "#1E1220",
      "Primary": "#FF94B8",
      "PrimaryBright": "#FFB8D0",
      "Accent": "#FF699E",
      "TextPrimary": "#FFF0F5",
      "TextSecondary": "#D8B4C8",
      "SolidBorderDark": "#422038"
    }
  },
  "background": {
    "type": "video",
    "videoSource": "assets/bg_cherry_loop.mp4",
    "imageSource": "assets/bg_poster.jpg",
    "opacity": 0.5
  },
  "decorations": {
    "screenFrame": "assets/frames/screen_branches.png",
    "buttonVideoIdle": "assets/buttons/sakura_bud_idle.webp",
    "buttonVideoActive": "assets/buttons/sakura_bloom_active.webp",
    "buttonImageIdle": "assets/buttons/sakura_idle.png",
    "buttonImageActive": "assets/buttons/sakura_active.png",
    "cornerStickers": {
      "topLeft": "assets/stickers/branch_left.png",
      "topRight": "assets/stickers/branch_right.png"
    }
  },
  "vfx": {
    "particles": "sakura_petals",
    "particleSprite": "assets/particles/petal.png"
  }
}
```

---

## 🚀 Как создать и опубликовать свою тему

1. **Форкните этот репозиторий**: `https://github.com/OctoCore-Dev/themes`
2. **Создайте папку** в `themes/<your-theme-id>/` (только строчные буквы, цифры и дефис).
3. **Создайте манифест `theme.json`** по спецификации [schemas/theme.v4.json](schemas/theme.v4.json).
4. **Положите обложку `preview.png`** (рекомендуемый размер 600x400).
5. **Положите ассеты** в подпапку `assets/` (видео, animated webp, рамки, звуки).
6. **Проверьте локально**:
   ```bash
   node scripts/build-catalog.js
   ```
7. **Откройте Pull Request** в ветку `main`. GitHub Action автоматически всё проверит и добавит вашу тему в каталог!

---

## 📦 Каталог тем API

Приложения и сайт скачивают актуальный каталог тем напрямую:
```text
https://raw.githubusercontent.com/OctoCore-Dev/themes/main/catalog.json
```

Лицензия: MIT. Создано с любовью сообществом OctoCore.
