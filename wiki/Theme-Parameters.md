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
  "FontRegular": "Inter-Regular",
  "FontMedium": "Inter-Medium",
  "FontBold": "Inter-Bold",
  "FontTitle": "Creepster",
  "FontFile": "assets/fonts/CustomFont.ttf"
}
```
- **`CornerRadius`**: Радиус скругления карточек (по умолчанию `16`).
- **`BlurIntensity`**: Сила эффекта Glassmorphism (по умолчанию `20`).
- **`BorderThickness`**: Толщина контуров карточек (по умолчанию `1.0`).
- **`CardOpacity`**: Базовая прозрачность карточек поверх живого фона (от `0.0` до `1.0`).
- **`FontRegular` / `FontMedium` / `FontBold` / `FontTitle`**: Семейства или алиасы шрифтов для основного текста и заголовков.
- **`FontFile`**: Относительный путь к кастомному файлу шрифта `.ttf` или `.otf` внутри папки темы.

---

## 5. Звуки (`core.sounds`)

```json
"sounds": {
  "click": "assets/sounds/click.wav",
  "hover": "assets/sounds/hover.wav",
  "notification": "assets/sounds/notify.wav",
  "connect": "assets/sounds/vpn_connected.wav",
  "disconnect": "assets/sounds/vpn_disconnected.wav",
  "ambient": "assets/sounds/ambient_loop.ogg",
  "volume": 0.85
}
```
- Форматы: `.wav` (PCM 16-bit), `.mp3` или `.ogg` (`OggS`) объемом до 5 МБ.
- **`hover`**: Короткий тактильный отклик при наведении на карточки и кнопки.
- **`ambient`**: Бесшовная фоновая аудио-атмосфера при активном окне приложения.
- **`volume`**: Базовый уровень громкости звукового пака темы (`0.0`–`1.0`).

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

## 8. Визуальные эффекты частиц и физика (`vfx`)

```json
"vfx": {
  "particles": "custom",
  "particleSprite": "assets/particles/wisp.png",
  "particleSprites": [
    "assets/particles/wisp.png",
    "assets/particles/bat.png",
    "assets/particles/pumpkin_spark.png"
  ],
  "intensity": 0.75,
  "speed": 1.1,
  "size": 1.2,
  "color": "#39FF14",
  "interactiveParticles": true,
  "trafficReactive": true,
  "parallaxIntensity": 0.4
}
```
- **Встроенные пресеты (`particles`):**
  `none`, `snow`, `sakura_petals`, `crows_feathers`, `embers`, `sparks`, `neon_sparks`, `fireflies`, `bubbles`, `rain`, `twinkle`, `matrix`, `custom`.
- **`particleSprite`**: Одиночный кастомный PNG-спрайт частицы.
- **`particleSprites`**: Массив до **12** различных PNG-спрайтов, которые одновременно рендерятся в потоке частиц (например, летучие мыши, искры тыквы и призрачные огоньки в теме `halloween-2026`).
- **`interactiveParticles`**: Частицы мягко отталкиваются и закручиваются вокруг курсора мыши или точки касания.
- **`trafficReactive`**: Скорость и турбулентность частиц динамически растут пропорционально текущему сетевому трафику VPN.
- **`parallaxIntensity`**: Сила многослойного 3D-параллакса фона, рамок и частиц при движении курсора (`0.0`–`1.0`).

---

## 9. Экранные шейдеры, графики трафика, лоадеры и кастомные статусы (`vfx`)

```json
"vfx": {
  "screenOverlay": "cyber_hud",
  "trafficGraphStyle": "cyber_bars",
  "buttonLoaderStyle": "reactor",
  "glow": {
    "intensity": 1.2,
    "radius": 24.0,
    "coreColor": "#00F0FF",
    "bloomColor": "#FF0055"
  },
  "statusText": {
    "disconnected": "NETRUN: OFFLINE",
    "connecting": "BYPASSING ICE...",
    "connected": "NEURAL LINK ACTIVE",
    "error": "ICE BREACH FAILED",
    "buttonIdle": "JACK IN",
    "buttonConnecting": "SYNC",
    "buttonConnected": "ONLINE"
  },
  "activeOverrides": {
    "accentColor": "#00F0FF",
    "glowColor": "#FF0055",
    "particleSpeedMultiplier": 1.8,
    "screenOverlay": "cyber_hud"
  }
}
```

- **`screenOverlay`** *(полноэкранный процедурный шейдерный слой)*:
  - `"none"` — без оверлея.
  - `"cyber_hud"` — голографическая кибер-сетка и телеметрические уголки.
  - `"scanlines"` — CRT сканлайны в стиле ретро-вейва.
  - `"aurora"` — переливающееся северное сияние в верхней части экрана.
  - `"crimson_vignette"` — багровая виньетка чакры по краям экрана.
  - `"mystic_fog"` — клубящийся мистический туман у основания окна.
  - `"golden_rays"` — торжественные золотые лучи свечения сверху.
  - `"frost_vignette"` — морозная изморозь по краям стекла.
- **`trafficGraphStyle`** *(стиль виджета скорости трафика)*:
  - `"neon_wave"` — плавная неоновая кривая Бетье с градиентной заливкой.
  - `"cyber_bars"` — дискретные киберпанк-столбцы эквалайзера.
  - `"pulse_line"` — кардиограмма / импульсная линия с ярким фронтом.
  - `"aurora_ribbon"` — многослойная шелковая лента северного сияния.
- **`buttonLoaderStyle`** *(процедурная векторная анимация вокруг кнопки)*:
  - `"crystal"` — квантовый гипер-кристалл из вращающихся полигонов.
  - `"reactor"` — энергетическое ядро с фотонными искрами.
  - `"dual_arc"` — классические двойные неоновые дуги.
  - `"runes"` — вращающееся кольцо рунических символов.
  - `"none"` — отключить процедурный векторный лоадер.
- **`statusText`**: Переопределение заголовков состояния VPN (`disconnected`, `connecting`, `connected`, `error`) и текста внутри центральной кнопки (`buttonIdle`, `buttonConnecting`, `buttonConnected`).
- **`activeOverrides`**: Параметры, которые автоматически активируются при переходе VPN в состояние `Connected` (`accentColor`, `glowColor`, `particleSpeedMultiplier`, `screenOverlay`).

---

## 10. Пользовательские настройки темы и локальный импорт `.zip`

Пользователь приложения может индивидуально кастомизировать любую примененную тему в разделе «Магазин тем»:
1. **Прозрачность карточек (Card Opacity)**: от `20%` (сильный акцент на живой фон/видео) до `100%` (матовая контрастность).
2. **Интенсивность неона (Neon Glow Intensity)**: ползунок от `0%` до `200%`, влияющий на ауру кнопки, свечение гипер-кристалла и размах ударных волн при подключении.
3. **Фоновые частицы (Particles)**: тумблер включения/выключения физической симуляции частиц.
4. **Живое видео (Video)**: тумблер воспроизведения видео-фона (автоматически экономит ресурсы батареи).
5. **Звуковые эффекты (Sounds)**: тумблер звуков кликов, наведения, эмбиента и статусов соединения.
6. **Импорт локального `.zip` пакета**: авторы тем могут загрузить свой `.zip` архив прямо в клиент для мгновенного предпросмотра и отладки всех эффектов.

