# 📋 Полный справочник параметров `theme.json`

Манифест `theme.json` является ядром темы и описывает палитру цветов, фоны, звуки, видео, рамки и эффекты частиц.

---

## 1. Метаданные темы (Root)

| Параметр | Тип | Обязательный? | Описание | Пример |
| :--- | :--- | :---: | :--- | :--- |
| `$schema` | `string` | Нет | Ссылка на JSON-схему для автодополнения в редакторе | `"../../schemas/theme.v4.json"` |
| `id` | `string` | **Да** | Уникальный ID в `kebab-case` (`^[a-z0-9-]+$`). Совпадает с именем папки темы! | `"cyber-neon"` |
| `name` | `string` | **Да** | Название темы для отображения в магазине | `"Cyber Neon 2077"` |
| `author` | `string` | **Да** | Автор или студия. Значение `"OctoCore"` получает знак `[✓ Официальная]` | `"OctoCore Community"` |
| `version` | `string` | **Да** | Версия темы по стандарту SemVer | `"1.0.0"` |
| `description` | `string` | Нет | Краткое описание стиля и атмосферы темы | `"Неоновая живая тема..."` |
| `tags` | `array<string>` | Нет | Теги поиска: `dark`, `neon`, `anime`, `live`, `video`, `nature` | `["dark", "neon"]` |
| `supportedApps` | `array<string>` | Нет | Список совместимых приложений (по умолчанию `["*"]`) | `["*"]` |

---

## 2. Цветовая палитра (`core.colors`)

Все цвета задаются в формате HEX: `#RRGGBB` или `#AARRGGBB`.

```json
"core": {
  "colors": {
    "BgBase": "#0E0E14",
    "BgSurface": "#181824",
    "BgElevated": "#222234",
    "BgInput": "#14141E",
    "Primary": "#0078D4",
    "PrimaryBright": "#2B88D8",
    "PrimaryDim": "#005A9E",
    "Accent": "#00E5FF",
    "TextPrimary": "#FFFFFF",
    "TextSecondary": "#A0A0B2",
    "TextMuted": "#606075",
    "SolidBorderDark": "#2E2E42",
    "BorderSubtle": "#252538",
    "BorderMedium": "#383852",
    "Success": "#10B981",
    "Warning": "#F59E0B",
    "Error": "#EF4444"
  }
}
```

- **`BgBase`** *(Обязательный)*: Цвет заднего фона приложения. По его яркости движок автоматически подбирает цвет системных кнопок окна Windows и статус-бара Android.
- **`BgSurface`** *(Обязательный)*: Цвет фона карточек и списков серверов.
- **`BgElevated`**: Цвет всплывающих окон, модальных карточек и выпадающих меню.
- **`BgInput`**: Цвет подложки полей ввода и ползунков.
- **`Primary`** *(Обязательный)*: Главный акцент темы (кнопки, активные чекбоксы, заголовки).
- **`PrimaryBright`**: Яркий акцент для подсветки при наведении (hover) и внешнего свечения (glow).
- **`PrimaryDim`**: Приглушенный цвет границ кнопок и неактивных элементов.
- **`Accent`**: Дополнительный цвет для неоновых искр, пинга и второстепенных действий.
- **`TextPrimary`** *(Обязательный)*: Основной контрастный текст.
- **`TextSecondary`**: Второстепенный текст подзаголовков и счетчиков.
- **`TextMuted`**: Подсказки и плейсхолдеры.
- **`SolidBorderDark`**: Темные контуры и линии разделения.
- **`BorderSubtle`**: Едва заметные контуры карточек.
- **`BorderMedium`**: Стандартная рамка выделенных карточек.
- **`Success`**: Индикатор успешного подключения VPN и отличного пинга (зеленый).
- **`Warning`**: Предупреждения, повторное подключение, низкий остаток тарифа (желтый).
- **`Error`**: Ошибки соединения, сбои связи (красный).

---

## 3. Градиенты (`core.gradients`)

```json
"gradients": {
  "PrimaryGradient": {
    "angle": 45,
    "stops": ["#0078D4", "#00E5FF"]
  },
  "SurfaceGradient": {
    "angle": 135,
    "stops": ["#1E1220", "#0D0912"]
  }
}
```

---

## 4. Параметры UI и шрифты (`core.ui`)

```json
"ui": {
  "CornerRadius": 16,
  "BlurIntensity": 20,
  "BorderThickness": 1.0,
  "CardOpacity": 0.85,
  "FontFile": "assets/fonts/CustomFont.ttf"
}
```
- **`CornerRadius`**: Радиус скругления карточек (по умолчанию `16`).
- **`BlurIntensity`**: Сила эффекта Glassmorphism (по умолчанию `20`).
- **`BorderThickness`**: Толщина контуров карточек (по умолчанию `1.0`).
- **`CardOpacity`**: Базовая прозрачность карточек поверх живого фона (от `0.20` до `1.00`).
- **`FontFile`**: Путь к кастомному шрифту `.ttf` или `.otf`.

---

## 5. Звуки (`core.sounds`)

```json
"sounds": {
  "click": "assets/sounds/click.wav",
  "notification": "assets/sounds/notify.wav",
  "connect": "assets/sounds/vpn_connected.wav",
  "disconnect": "assets/sounds/vpn_disconnected.wav"
}
```
Форматы: `.wav` (PCM 16-bit) или `.mp3` с объемом не более 1-2 МБ.

---

## 6. Задний фон (`background`)

```json
"background": {
  "type": "video",
  "videoSource": "assets/bg_loop.mp4",
  "imageSource": "assets/bg_poster.jpg",
  "fallbackImage": "assets/bg_poster.jpg",
  "loop": true,
  "muted": true,
  "opacity": 0.45
}
```
- `type`: `"video"`, `"image"`, или `"gradient"`.
- `videoSource`: файл бесшовного MP4/WebM видео.
- `imageSource` / `fallbackImage`: статичный постер.
- `opacity`: яркость фона (рекомендуется `0.35`–`0.55`).

---

## 7. Декорации (`decorations`)

Подробные руководства по декорациям:
- 🖼️ [[Настройка рамок 9-Slice|Nine-Patch-Frames]]
- 🔘 [[Кнопки VPN и Animated WebP|VPN-Buttons]]

---

## 8. Визуальные эффекты частиц (`vfx`)

```json
"vfx": {
  "particles": "sakura_petals",
  "particleSprite": "assets/particles/petal.png",
  "intensity": 0.6,
  "speed": 1.0,
  "size": 1.0,
  "color": "#FFB8D0"
}
```
**Встроенные пресеты (`particles`):**
`sakura_petals`, `crows_feathers`, `neon_sparks`, `snow`, `fireflies`, `bubbles`, `rain`, `none`, `custom`.
