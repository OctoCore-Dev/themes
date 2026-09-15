import os
import math
import struct
import wave
from PIL import Image, ImageDraw, ImageFilter

def create_dirs(base_dir):
    os.makedirs(os.path.join(base_dir, "assets", "frames"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "assets", "buttons"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "assets", "particles"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "assets", "sounds"), exist_ok=True)

def write_wav(filename, duration_sec, notes, sample_rate=44100):
    # notes is list of (freq, start_ratio, end_ratio, amplitude)
    num_samples = int(duration_sec * sample_rate)
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        frames = bytearray()
        for i in range(num_samples):
            t = i / sample_rate
            val = 0.0
            for (f, start, end, amp) in notes:
                t_start = start * duration_sec
                t_end = end * duration_sec
                if t_start <= t <= t_end:
                    local_t = t - t_start
                    dur = max(0.001, t_end - t_start)
                    env = math.exp(-4.5 * local_t / dur) * min(1.0, local_t / 0.015)
                    val += amp * math.sin(2.0 * math.pi * f * local_t) * env
            val = max(-1.0, min(1.0, val))
            sample = int(val * 28000.0)
            frames.extend(struct.pack('<hh', sample, sample))
        wav_file.writeframes(frames)

# =========================================================================
# 1. CYBER NEON GENERATOR
# =========================================================================
def generate_cyber_neon(theme_dir):
    create_dirs(theme_dir)
    print("Generating Cyber Neon assets...")

    # Sounds
    write_wav(os.path.join(theme_dir, "assets", "sounds", "click.wav"), 0.07, [
        (1800, 0.0, 1.0, 0.5), (2800, 0.0, 0.5, 0.3)
    ])
    write_wav(os.path.join(theme_dir, "assets", "sounds", "connect.wav"), 0.75, [
        (440.0, 0.0, 0.5, 0.4),
        (554.37, 0.15, 0.65, 0.45),
        (659.25, 0.30, 0.80, 0.5),
        (880.0, 0.45, 1.0, 0.6)
    ])
    write_wav(os.path.join(theme_dir, "assets", "sounds", "disconnect.wav"), 0.5, [
        (659.25, 0.0, 0.6, 0.45),
        (440.0, 0.25, 1.0, 0.5)
    ])

    # Background (1920x1080)
    bg = Image.new("RGB", (1920, 1080), (10, 9, 21))
    draw = ImageDraw.Draw(bg)
    # Vertical gradient
    for y in range(1080):
        factor = y / 1080.0
        r = int(10 + factor * 14)
        g = int(9 + factor * 8)
        b = int(21 + factor * 35)
        draw.line([(0, y), (1920, y)], fill=(r, g, b))
    
    # Cyber grid at bottom
    horizon_y = 620
    for x in range(-500, 2420, 90):
        # Vanishing lines
        draw.line([(960, horizon_y), (x, 1080)], fill=(35, 25, 75), width=2)
    for gy in range(horizon_y + 20, 1080, 35):
        alpha_factor = (gy - horizon_y) / (1080.0 - horizon_y)
        col = (int(0 + alpha_factor * 0), int(200 * alpha_factor), int(240 * alpha_factor))
        draw.line([(0, gy), (1920, gy)], fill=col, width=1)
    
    # Ambient glows
    bloom = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(bloom)
    bdraw.ellipse([700, 300, 1220, 820], fill=(0, 240, 255, 30))
    bdraw.ellipse([900, 450, 1500, 950], fill=(255, 0, 85, 25))
    bloom = bloom.filter(ImageFilter.GaussianBlur(100))
    bg.paste(bloom, (0, 0), bloom)
    bg.save(os.path.join(theme_dir, "assets", "bg.jpg"), quality=92)

    # Frame (1920x1080 RGBA 9-Slice)
    frame = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    fdraw = ImageDraw.Draw(frame)
    # Outer thin border
    fdraw.rectangle([10, 10, 1909, 1069], outline=(0, 240, 255, 120), width=2)
    fdraw.rectangle([14, 14, 1905, 1065], outline=(255, 0, 85, 80), width=1)

    # Corner brackets (80x80)
    # Top-Left
    fdraw.polygon([(10, 10), (70, 10), (70, 22), (22, 22), (22, 70), (10, 70)], fill=(0, 240, 255, 240))
    fdraw.line([(10, 10), (35, 10)], fill=(255, 255, 255, 255), width=3)
    fdraw.line([(10, 10), (10, 35)], fill=(255, 255, 255, 255), width=3)
    # Top-Right
    fdraw.polygon([(1909, 10), (1849, 10), (1849, 22), (1897, 22), (1897, 70), (1909, 70)], fill=(255, 0, 85, 240))
    # Bottom-Left
    fdraw.polygon([(10, 1069), (70, 1069), (70, 1057), (22, 1057), (22, 1009), (10, 1009)], fill=(255, 0, 85, 240))
    # Bottom-Right
    fdraw.polygon([(1909, 1069), (1849, 1069), (1849, 1057), (1897, 1057), (1897, 1009), (1909, 1009)], fill=(0, 240, 255, 240))
    frame.save(os.path.join(theme_dir, "assets", "frames", "cyber_frame.png"))

    # Particle (64x64)
    spark = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(spark)
    sdraw.polygon([(32, 2), (38, 26), (62, 32), (38, 38), (32, 62), (26, 38), (2, 32), (26, 26)], fill=(0, 240, 255, 230))
    sdraw.ellipse([26, 26, 38, 38], fill=(255, 255, 255, 255))
    spark.save(os.path.join(theme_dir, "assets", "particles", "cyber_spark.png"))

    # Buttons (256x256 RGBA)
    for state in ["idle", "connecting", "active", "error"]:
        btn = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
        bdraw = ImageDraw.Draw(btn)
        cx, cy = 128, 128

        if state == "idle":
            bdraw.ellipse([28, 28, 228, 228], outline=(0, 240, 255, 140), width=4)
            bdraw.ellipse([45, 45, 211, 211], outline=(35, 30, 65, 200), width=8)
            bdraw.ellipse([80, 80, 176, 176], fill=(18, 16, 36, 240), outline=(0, 240, 255, 220), width=3)
            # Power symbol
            bdraw.arc([98, 98, 158, 158], start=310, end=230, fill=(0, 240, 255, 255), width=5)
            bdraw.line([(128, 92), (128, 122)], fill=(0, 240, 255, 255), width=5)
        elif state == "connecting":
            bdraw.ellipse([28, 28, 228, 228], outline=(255, 0, 85, 140), width=4)
            bdraw.arc([36, 36, 220, 220], start=45, end=210, fill=(0, 240, 255, 255), width=6)
            bdraw.arc([36, 36, 220, 220], start=225, end=390, fill=(255, 0, 85, 255), width=6)
            bdraw.ellipse([80, 80, 176, 176], fill=(22, 18, 45, 250), outline=(255, 0, 85, 220), width=3)
            # Spinner center
            bdraw.polygon([(128, 95), (145, 138), (111, 138)], fill=(0, 240, 255, 255))
        elif state == "active":
            # Glow aura
            bdraw.ellipse([20, 20, 236, 236], fill=(0, 240, 255, 45))
            bdraw.ellipse([28, 28, 228, 228], outline=(0, 240, 255, 255), width=6)
            bdraw.ellipse([45, 45, 211, 211], outline=(255, 0, 85, 180), width=4)
            bdraw.ellipse([70, 70, 186, 186], fill=(0, 240, 255, 230))
            bdraw.ellipse([88, 88, 168, 168], fill=(255, 255, 255, 255))
            # Shield icon
            bdraw.polygon([(128, 102), (150, 112), (150, 138), (128, 154), (106, 138), (106, 112)], fill=(15, 12, 30, 255))
        else: # error
            bdraw.ellipse([28, 28, 228, 228], outline=(255, 0, 85, 255), width=6)
            bdraw.ellipse([75, 75, 181, 181], fill=(45, 12, 22, 240), outline=(255, 0, 85, 220), width=4)
            # Exclamation
            bdraw.line([(128, 98), (128, 135)], fill=(255, 255, 255, 255), width=6)
            bdraw.ellipse([124, 145, 132, 153], fill=(255, 255, 255, 255))
        
        btn.save(os.path.join(theme_dir, "assets", "buttons", f"btn_{state}.png"))

    # Icon (256x256)
    icon = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    idraw = ImageDraw.Draw(icon)
    idraw.rounded_rectangle([12, 12, 244, 244], radius=48, fill=(16, 14, 32, 255), outline=(0, 240, 255, 240), width=4)
    idraw.polygon([(128, 48), (198, 88), (198, 168), (128, 208), (58, 168), (58, 88)], outline=(255, 0, 85, 255), width=5)
    idraw.ellipse([98, 98, 158, 158], fill=(0, 240, 255, 240))
    icon.save(os.path.join(theme_dir, "icon.png"))

    # Preview (600x400 JPG)
    prev = Image.new("RGB", (600, 400), (10, 9, 21))
    pdraw = ImageDraw.Draw(prev)
    # Background mini gradient
    for y in range(400):
        factor = y / 400.0
        pdraw.line([(0, y), (600, y)], fill=(int(10 + factor * 14), int(9 + factor * 8), int(21 + factor * 35)))
    # Neon card preview
    pdraw.rounded_rectangle([40, 40, 560, 360], radius=24, fill=(18, 16, 36), outline=(0, 240, 255), width=2)
    # Title
    pdraw.text((70, 70), "CYBER NEON 2077", fill=(0, 240, 255))
    pdraw.text((70, 100), "Futuristic Synthwave Experience", fill=(150, 161, 196))
    # Color swatches
    swatches = [(0, 240, 255), (255, 0, 85), (0, 255, 157), (255, 184, 0)]
    for i, c in enumerate(swatches):
        pdraw.rounded_rectangle([70 + i * 40, 140, 100 + i * 40, 170], radius=8, fill=c)
    # Center button mockup
    pdraw.ellipse([370, 120, 510, 260], fill=(0, 240, 255, 40), outline=(0, 240, 255), width=4)
    pdraw.ellipse([400, 150, 480, 230], fill=(0, 240, 255))
    pdraw.polygon([(440, 175), (455, 185), (455, 205), (440, 215), (425, 205), (425, 185)], fill=(18, 16, 36))
    prev.save(os.path.join(theme_dir, "preview.jpg"), quality=90)

    # theme.json
    manifest_json = """{
  "$schema": "../../schemas/theme.v4.json",
  "id": "cyber-neon",
  "name": "Cyber Neon 2077",
  "author": "OctoCore",
  "version": "1.0.0",
  "description": "Футуристическая неоновая тема: киберпанк-ночь, электро-бирюзовый и неоново-пурпурный контраст, светящееся ядро реактора и искры кибернетической энергии",
  "tags": [
    "cyberpunk",
    "neon",
    "synthwave",
    "dark",
    "cyan",
    "magenta",
    "live"
  ],
  "supportedApps": [
    "*"
  ],
  "core": {
    "colors": {
      "BgBase": "#0A0915",
      "BgSurface": "#131126",
      "BgElevated": "#1C1836",
      "BgInput": "#18142E",
      "Primary": "#00F0FF",
      "PrimaryBright": "#5CFFFF",
      "PrimaryDim": "#00A3B5",
      "Accent": "#FF0055",
      "TextPrimary": "#F0F4FF",
      "TextSecondary": "#96A1C4",
      "TextMuted": "#576182",
      "SolidBorderDark": "#2A224D",
      "BorderSubtle": "#1E1838",
      "BorderMedium": "#392F66",
      "Success": "#00FF9D",
      "Warning": "#FFB800",
      "Error": "#FF0055"
    },
    "gradients": {
      "PrimaryGradient": {
        "angle": 45,
        "stops": [
          "#00F0FF",
          "#FF0055"
        ]
      },
      "SurfaceGradient": {
        "angle": 135,
        "stops": [
          "#1C1636",
          "#0D0A1C"
        ]
      }
    },
    "ui": {
      "CornerRadius": 16,
      "BlurIntensity": 25,
      "BorderThickness": 1.5,
      "CardOpacity": 0.85
    },
    "sounds": {
      "click": "assets/sounds/click.wav",
      "notification": "assets/sounds/click.wav"
    }
  },
  "background": {
    "type": "image",
    "imageSource": "assets/bg.jpg",
    "opacity": 0.45
  },
  "decorations": {
    "screenFrame": "assets/frames/cyber_frame.png",
    "frameSlice": {
      "top": 80,
      "right": 80,
      "bottom": 80,
      "left": 80
    },
    "buttonImageIdle": "assets/buttons/btn_idle.png",
    "buttonImageConnecting": "assets/buttons/btn_connecting.png",
    "buttonImageActive": "assets/buttons/btn_active.png",
    "buttonImageError": "assets/buttons/btn_error.png"
  },
  "layout": {
    "buttonPosition": "center",
    "speedWidget": "graph",
    "serverCardStyle": "glass",
    "showQuickToggles": true
  },
  "vfx": {
    "particles": "neon_sparks",
    "particleSprite": "assets/particles/cyber_spark.png",
    "intensity": 0.75,
    "speed": 1.2
  },
  "apps": {
    "obxodka": {
      "tunnelButton": {
        "style": "glow_icon",
        "borderGlow": "#00F0FF",
        "pulseSpeed": 1.2
      },
      "sounds": {
        "connect": "assets/sounds/connect.wav",
        "disconnect": "assets/sounds/disconnect.wav"
      }
    }
  }
}
"""
    with open(os.path.join(theme_dir, "theme.json"), "w", encoding="utf-8") as f:
        f.write(manifest_json)
    print("Cyber Neon generated successfully!")

# =========================================================================
# 2. NORDIC FROST GENERATOR
# =========================================================================
def generate_nordic_frost(theme_dir):
    create_dirs(theme_dir)
    print("Generating Nordic Frost assets...")

    # Sounds
    write_wav(os.path.join(theme_dir, "assets", "sounds", "click.wav"), 0.08, [
        (2200, 0.0, 1.0, 0.4), (3300, 0.0, 0.4, 0.25)
    ])
    write_wav(os.path.join(theme_dir, "assets", "sounds", "connect.wav"), 0.8, [
        (523.25, 0.0, 0.6, 0.45),
        (659.25, 0.18, 0.75, 0.5),
        (783.99, 0.36, 0.9, 0.55),
        (1046.50, 0.5, 1.0, 0.6)
    ])
    write_wav(os.path.join(theme_dir, "assets", "sounds", "disconnect.wav"), 0.55, [
        (783.99, 0.0, 0.5, 0.4),
        (523.25, 0.2, 1.0, 0.45)
    ])

    # Background (1920x1080)
    bg = Image.new("RGB", (1920, 1080), (11, 17, 24))
    draw = ImageDraw.Draw(bg)
    # Gradient night
    for y in range(1080):
        factor = y / 1080.0
        r = int(7 + factor * 11)
        g = int(13 + factor * 16)
        b = int(20 + factor * 22)
        draw.line([(0, y), (1920, y)], fill=(r, g, b))
    
    # Aurora wave
    aurora = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    adraw = ImageDraw.Draw(aurora)
    for x in range(0, 1920, 10):
        ay = 240 + int(math.sin(x * 0.005) * 80 + math.cos(x * 0.012) * 40)
        adraw.line([(x, ay - 90), (x, ay + 120)], fill=(52, 211, 153, 40), width=24)
        adraw.line([(x, ay - 40), (x, ay + 70)], fill=(56, 189, 248, 60), width=18)
    aurora = aurora.filter(ImageFilter.GaussianBlur(60))
    bg.paste(aurora, (0, 0), aurora)

    # Mountain silhouettes
    draw.polygon([(0, 1080), (0, 750), (320, 610), (680, 780), (1050, 560), (1450, 720), (1920, 600), (1920, 1080)], fill=(12, 20, 30))
    draw.polygon([(0, 1080), (160, 840), (510, 740), (920, 860), (1300, 720), (1720, 850), (1920, 780), (1920, 1080)], fill=(16, 26, 38))
    bg.save(os.path.join(theme_dir, "assets", "bg.jpg"), quality=92)

    # Frame (1920x1080 RGBA 9-Slice)
    frame = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    fdraw = ImageDraw.Draw(frame)
    # Frosted border line
    fdraw.rectangle([10, 10, 1909, 1069], outline=(56, 189, 248, 100), width=2)
    fdraw.rectangle([15, 15, 1904, 1064], outline=(165, 243, 252, 60), width=1)

    # Crystalline corner crossbars (75x75)
    def draw_corner(cx, cy, flip_x, flip_y):
        pts = [(cx, cy), (cx + flip_x * 65, cy), (cx + flip_x * 65, cy + flip_y * 18), (cx + flip_x * 18, cy + flip_y * 18), (cx + flip_x * 18, cy + flip_y * 65), (cx, cy + flip_y * 65)]
        fdraw.polygon(pts, fill=(56, 189, 248, 220))
        # Crystal diamond at corner node
        dx, dy = cx + flip_x * 28, cy + flip_y * 28
        fdraw.polygon([(dx, dy - 8), (dx + 8, dy), (dx, dy + 8), (dx - 8, dy)], fill=(165, 243, 252, 255))

    draw_corner(10, 10, 1, 1)
    draw_corner(1909, 10, -1, 1)
    draw_corner(10, 1069, 1, -1)
    draw_corner(1909, 1069, -1, -1)
    frame.save(os.path.join(theme_dir, "assets", "frames", "frost_frame.png"))

    # Particle (64x64)
    snow = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(snow)
    cx, cy = 32, 32
    for angle in range(0, 360, 60):
        rad = math.radians(angle)
        ex = cx + int(math.cos(rad) * 26)
        ey = cy + int(math.sin(rad) * 26)
        sdraw.line([(cx, cy), (ex, ey)], fill=(241, 245, 249, 240), width=2)
        # Branches
        bx = cx + int(math.cos(rad) * 16)
        by = cy + int(math.sin(rad) * 16)
        b_rad1 = math.radians(angle + 40)
        b_rad2 = math.radians(angle - 40)
        sdraw.line([(bx, by), (bx + int(math.cos(b_rad1) * 8), by + int(math.sin(b_rad1) * 8))], fill=(165, 243, 252, 230), width=1)
        sdraw.line([(bx, by), (bx + int(math.cos(b_rad2) * 8), by + int(math.sin(b_rad2) * 8))], fill=(165, 243, 252, 230), width=1)
    sdraw.ellipse([29, 29, 35, 35], fill=(255, 255, 255, 255))
    snow.save(os.path.join(theme_dir, "assets", "particles", "snowflake.png"))

    # Buttons (256x256 RGBA)
    for state in ["idle", "connecting", "active", "error"]:
        btn = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
        bdraw = ImageDraw.Draw(btn)
        cx, cy = 128, 128

        if state == "idle":
            bdraw.ellipse([28, 28, 228, 228], outline=(56, 189, 248, 140), width=4)
            bdraw.ellipse([45, 45, 211, 211], outline=(27, 40, 56, 200), width=8)
            bdraw.ellipse([80, 80, 176, 176], fill=(18, 28, 39, 240), outline=(56, 189, 248, 220), width=3)
            # Power symbol
            bdraw.arc([98, 98, 158, 158], start=310, end=230, fill=(56, 189, 248, 255), width=5)
            bdraw.line([(128, 92), (128, 122)], fill=(56, 189, 248, 255), width=5)
        elif state == "connecting":
            bdraw.ellipse([28, 28, 228, 228], outline=(165, 243, 252, 140), width=4)
            bdraw.arc([36, 36, 220, 220], start=45, end=210, fill=(56, 189, 248, 255), width=6)
            bdraw.arc([36, 36, 220, 220], start=225, end=390, fill=(52, 211, 153, 255), width=6)
            bdraw.ellipse([80, 80, 176, 176], fill=(21, 34, 48, 250), outline=(165, 243, 252, 220), width=3)
            # Ice crystal center
            bdraw.polygon([(128, 96), (144, 128), (128, 160), (112, 128)], fill=(56, 189, 248, 255))
        elif state == "active":
            bdraw.ellipse([20, 20, 236, 236], fill=(56, 189, 248, 45))
            bdraw.ellipse([28, 28, 228, 228], outline=(56, 189, 248, 255), width=6)
            bdraw.ellipse([45, 45, 211, 211], outline=(165, 243, 252, 180), width=4)
            bdraw.ellipse([70, 70, 186, 186], fill=(56, 189, 248, 230))
            bdraw.ellipse([88, 88, 168, 168], fill=(255, 255, 255, 255))
            # Snowflake compass center
            bdraw.polygon([(128, 98), (135, 121), (158, 128), (135, 135), (128, 158), (121, 135), (98, 128), (121, 121)], fill=(18, 28, 39, 255))
        else: # error
            bdraw.ellipse([28, 28, 228, 228], outline=(248, 113, 113, 255), width=6)
            bdraw.ellipse([75, 75, 181, 181], fill=(45, 20, 25, 240), outline=(248, 113, 113, 220), width=4)
            bdraw.line([(128, 98), (128, 135)], fill=(255, 255, 255, 255), width=6)
            bdraw.ellipse([124, 145, 132, 153], fill=(255, 255, 255, 255))
        
        btn.save(os.path.join(theme_dir, "assets", "buttons", f"btn_{state}.png"))

    # Icon (256x256)
    icon = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    idraw = ImageDraw.Draw(icon)
    idraw.rounded_rectangle([12, 12, 244, 244], radius=48, fill=(18, 28, 39, 255), outline=(56, 189, 248, 240), width=4)
    # Diamond crystal emblem
    idraw.polygon([(128, 45), (200, 128), (128, 211), (56, 128)], outline=(165, 243, 252, 255), width=5)
    idraw.polygon([(128, 75), (175, 128), (128, 181), (81, 128)], fill=(56, 189, 248, 240))
    idraw.ellipse([118, 118, 138, 138], fill=(255, 255, 255, 255))
    icon.save(os.path.join(theme_dir, "icon.png"))

    # Preview (600x400 JPG)
    prev = Image.new("RGB", (600, 400), (11, 17, 24))
    pdraw = ImageDraw.Draw(prev)
    for y in range(400):
        factor = y / 400.0
        pdraw.line([(0, y), (600, y)], fill=(int(7 + factor * 11), int(13 + factor * 16), int(20 + factor * 22)))
    # Frosted card
    pdraw.rounded_rectangle([40, 40, 560, 360], radius=24, fill=(18, 28, 39), outline=(56, 189, 248), width=2)
    pdraw.text((70, 70), "NORDIC FROST", fill=(56, 189, 248))
    pdraw.text((70, 100), "Arctic Minimalist Atmosphere", fill=(148, 163, 184))
    swatches = [(56, 189, 248), (165, 243, 252), (52, 211, 153), (251, 191, 36)]
    for i, c in enumerate(swatches):
        pdraw.rounded_rectangle([70 + i * 40, 140, 100 + i * 40, 170], radius=8, fill=c)
    # Center button mockup
    pdraw.ellipse([370, 120, 510, 260], fill=(56, 189, 248, 40), outline=(56, 189, 248), width=4)
    pdraw.ellipse([400, 150, 480, 230], fill=(56, 189, 248))
    pdraw.polygon([(440, 175), (455, 185), (455, 205), (440, 215), (425, 205), (425, 185)], fill=(18, 28, 39))
    prev.save(os.path.join(theme_dir, "preview.jpg"), quality=90)

    # theme.json
    manifest_json = """{
  "$schema": "../../schemas/theme.v4.json",
  "id": "nordic-frost",
  "name": "Nordic Frost",
  "author": "OctoCore",
  "version": "1.0.0",
  "description": "Элегантная северная тема: арктическая ночь, лазурный и ледниковый контраст, падающие кристаллы снега, матовое стекло и звон хрустального колокольчика",
  "tags": [
    "nordic",
    "frost",
    "ice",
    "minimal",
    "clean",
    "cold",
    "blue",
    "winter"
  ],
  "supportedApps": [
    "*"
  ],
  "core": {
    "colors": {
      "BgBase": "#0B1118",
      "BgSurface": "#121C27",
      "BgElevated": "#1B2838",
      "BgInput": "#152230",
      "Primary": "#38BDF8",
      "PrimaryBright": "#7DD3FC",
      "PrimaryDim": "#0284C7",
      "Accent": "#A5F3FC",
      "TextPrimary": "#F1F5F9",
      "TextSecondary": "#94A3B8",
      "TextMuted": "#475569",
      "SolidBorderDark": "#1E3A5F",
      "BorderSubtle": "#1B2B3F",
      "BorderMedium": "#294B73",
      "Success": "#34D399",
      "Warning": "#FBBF24",
      "Error": "#F87171"
    },
    "gradients": {
      "PrimaryGradient": {
        "angle": 45,
        "stops": [
          "#38BDF8",
          "#0284C7"
        ]
      },
      "SurfaceGradient": {
        "angle": 135,
        "stops": [
          "#1A2A3C",
          "#0D1622"
        ]
      }
    },
    "ui": {
      "CornerRadius": 16,
      "BlurIntensity": 25,
      "BorderThickness": 1.5,
      "CardOpacity": 0.85
    },
    "sounds": {
      "click": "assets/sounds/click.wav",
      "notification": "assets/sounds/click.wav"
    }
  },
  "background": {
    "type": "image",
    "imageSource": "assets/bg.jpg",
    "opacity": 0.45
  },
  "decorations": {
    "screenFrame": "assets/frames/frost_frame.png",
    "frameSlice": {
      "top": 75,
      "right": 75,
      "bottom": 75,
      "left": 75
    },
    "buttonImageIdle": "assets/buttons/btn_idle.png",
    "buttonImageConnecting": "assets/buttons/btn_connecting.png",
    "buttonImageActive": "assets/buttons/btn_active.png",
    "buttonImageError": "assets/buttons/btn_error.png"
  },
  "layout": {
    "buttonPosition": "center",
    "speedWidget": "graph",
    "serverCardStyle": "glass",
    "showQuickToggles": true
  },
  "vfx": {
    "particles": "snow",
    "particleSprite": "assets/particles/snowflake.png",
    "intensity": 0.65,
    "speed": 0.8
  },
  "apps": {
    "obxodka": {
      "tunnelButton": {
        "style": "glow_icon",
        "borderGlow": "#38BDF8",
        "pulseSpeed": 1.0
      },
      "sounds": {
        "connect": "assets/sounds/connect.wav",
        "disconnect": "assets/sounds/disconnect.wav"
      }
    }
  }
}
"""
    with open(os.path.join(theme_dir, "theme.json"), "w", encoding="utf-8") as f:
        f.write(manifest_json)
    print("Nordic Frost generated successfully!")

if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    generate_cyber_neon(os.path.join(base, "themes", "cyber-neon"))
    generate_nordic_frost(os.path.join(base, "themes", "nordic-frost"))
    print("All themes generated!")
