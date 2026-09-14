# 🔘 Руководство по кнопкам VPN (4 фазы соединения)

В приложениях OctoCore кнопка подключения поддерживает 4 полноценных фазы жизненного цикла туннеля, кинематографичные переходы Cross-Fade и видео с прозрачным альфа-каналом.

---

## 1. Четыре состояния кнопки

| Состояние | Ключ статики (PNG) | Ключ видео (WebP) | Описание поведения |
| :--- | :--- | :--- | :--- |
| **Idle** | `buttonImageIdle` | `buttonVideoIdle` | Ожидание. VPN выключен. Спокойная форма, мягкая пульсация. |
| **Connecting** | `buttonImageConnecting` | `buttonVideoConnecting` | Подключение. Рукопожатие ключей, раскручивающийся вихрь, зарядка энергии. |
| **Active** | `buttonImageActive` | `buttonVideoActive` | Защита включена. VPN активен. Яркое свечение, открытая форма. |
| **Error** | `buttonImageError` | `buttonVideoError` | Ошибка соединения. Сбой сети. Тревожное пламя или мигание. |

---

## 2. Бывают ли видео с прозрачным фоном? ДА!

Обычные видеофайлы MP4 не поддерживают прозрачность. Однако для кнопок используется формат **Animated WebP (`.webp`)** или **APNG (`.png`)**, имеющий полноценный 8-битный альфа-канал!

Движок **SkiaSharp** рендерит такие анимации на частоте 60 FPS прямо через видеокарту, сохраняя органичную форму кнопки (лепестки, огонь, неоновые сферы) без грубых черных или белых углов.

### Как перевести видео или секвенцию кадров в Animated WebP через `ffmpeg`:

```bash
# Из видео с прозрачным альфа-каналом (ProRes 4444 или MOV):
ffmpeg -i input.mov -vcodec libwebp -filter:v fps=fps=30 -lossless 0 -compression_level 4 -q:v 75 -loop 0 button_active.webp

# Из набора картинок frame_001.png, frame_002.png...:
ffmpeg -framerate 30 -i frame_%03d.png -vcodec libwebp -lossless 0 -q:v 80 -loop 0 button_idle.webp
```

---

## 3. Статичные кнопки (PNG)

Если вы не создаете видео-анимацию, можно использовать высококачественные статичные PNG с прозрачным фоном:

```json
"decorations": {
  "buttonImageIdle": "assets/buttons/btn_idle.png",
  "buttonImageConnecting": "assets/buttons/btn_connecting.png",
  "buttonImageActive": "assets/buttons/btn_active.png",
  "buttonImageError": "assets/buttons/btn_error.png"
}
```
Рекомендуемый размер графики кнопки: **512×512** или **256×256** пикселей.
