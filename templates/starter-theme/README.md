# Шаблон новой темы (Starter Theme Template)

Данная папка служит стартовым шаблоном для создания собственной темы оформления для экосистемы **OctoCore / Obxodka VPN**.

---

## 🚀 Пошаговая инструкция

1. Скопируйте папку `starter-theme` в каталог `themes/` с уникальным идентификатором вашей темы:
   ```bash
   cp -r templates/starter-theme themes/my-theme-id
   ```
   *(Идентификатор должен быть в нижнем регистре через дефис, например: `sunset-vapor`, `emerald-forest`, `tokyo-night`).*

2. Откройте `themes/my-theme-id/theme.json` и настройте параметры:
   - `id`: укажите имя папки темы (`my-theme-id`).
   - `name`: отображаемое название (например: "Emerald Forest").
   - `author`: ваше имя или никнейм.
   - `core.colors`: палитра цветов вашего дизайна.

3. Замените медиа-файлы своими артами:
   - `icon.png`: квадратная иконка темы для витрины каталога (512x512 PNG).
   - `preview.jpg`: снимок экрана с вашей темой для витрины (1280x720 JPG/WebP).
   - `assets/bg.jpg`: фоновое изображение (или постер для видео).
   - `assets/buttons/`: 4 состояния кнопки подключения (`btn_idle.png`, `btn_connecting.png`, `btn_active.png`, `btn_error.png`) с обязательным прозрачным альфа-каналом.

4. (Опционально) Добавьте живые эффекты:
   - `assets/bg.mp4`: зацикленное фоновое видео (60 FPS, H.264, без звука).
   - `assets/buttons/*.webp`: анимированные WebP кнопки с прозрачным фоном.
   - `assets/frames/screen_frame.png`: рамка экрана с настройкой `frameSlice` в `theme.json`.

5. Проверьте валидность темы:
   ```bash
   npm run validate
   ```

6. Создайте Pull Request в официальный репозиторий:
   [https://github.com/OctoCore-Dev/themes](https://github.com/OctoCore-Dev/themes)
