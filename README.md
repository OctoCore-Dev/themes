# 🎨 OctoCore Themes Hub (Universal Community Theme Hub)

Открытый репозиторий тем оформления для всей экосистемы приложений **OctoCore** (VPN `obxodka`, Карты и туризм, Чат, B2B SaaS).

[![Validate Themes & Build Catalog](https://github.com/OctoCore-Dev/themes/actions/workflows/validate-and-catalog.yml/badge.svg)](https://github.com/OctoCore-Dev/themes/actions/workflows/validate-and-catalog.yml)
[![Catalog](https://img.shields.io/badge/Catalog-v4.0.0-blueviolet)](catalog.json)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 🌟 Возможности кастомизации

Движок поддерживает **полный спектр мультимедиа**:
* 🎨 **Цвета и авто-градиенты** (`Primary`, `BgBase`, `Accent`, `SolidBorderDark`).
* 🎬 **Живые видео-фоны** (`mp4`), анимированные WebP/GIF или статичные арты.
* 🌟 **Интерактивные кнопки-персонажи / айдолы** с состояниями:
  * `idle` (в покое)
  * `connecting` (подключение)
  * `connected` (улыбка / салют)
* 🖼️ **Прозрачные декоративные PNG-рамки** (кружева, золото, винтаж, киберпанк HUD) поверх экрана и карточек (с `InputTransparent="True"` — 0 помех для кликов!).
* 🎵 **Звуковые паки** (звуки клика, подключения и отключения).
* 🗺️ **Стили карт** для приложений с навигацией и туризмом.
* 🌸 **VFX-частицы** (лепестки сакуры, неоновые искры, матричный дождь, снег).

---

## 🚀 Как создать и опубликовать свою тему

1. **Форкните этот репозиторий**: `https://github.com/OctoCore-Dev/themes`
2. **Создайте папку** в `themes/<your-theme-id>/` (только строчные буквы, цифры и дефис).
3. **Создайте манифест `theme.json`** по спецификации [schemas/theme.v4.json](schemas/theme.v4.json).
4. **Положите обложку `preview.png`** (рекомендуемый размер 600x400).
5. **Положите ассеты** в подпапку `assets/` (фоны, звуки, рамки, фото персонажей).
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
