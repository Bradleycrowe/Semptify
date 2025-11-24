"""
Generate Semptify Icon
Creates a simple but recognizable icon for the desktop shortcut
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Create 256x256 icon with Semptify colors
size = 256
img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Gradient background (blue to cyan)
for i in range(size):
    color = (
        int(74 + (i / size) * (0 - 74)),      # R: 74 -> 0
        int(144 + (i / size) * (200 - 144)),  # G: 144 -> 200
        int(226 + (i / size) * (255 - 226)),  # B: 226 -> 255
        255
    )
    draw.rectangle([(0, i), (size, i+1)], fill=color)

# Draw large "S" in center
try:
    # Try to use a system font
    font = ImageFont.truetype("arial.ttf", 160)
except:
    # Fallback to default font
    font = ImageFont.load_default()

# Draw "S" with shadow effect
text = "S"
# Shadow
draw.text((size//2, size//2), text, font=font, fill=(0, 0, 0, 128), anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0, 128))
# Main text
draw.text((size//2-2, size//2-2), text, font=font, fill=(255, 255, 255, 255), anchor="mm", stroke_width=3, stroke_fill=(74, 144, 226, 255))

# Save as ICO with multiple sizes
icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
icons = []
for icon_size in icon_sizes:
    icons.append(img.resize(icon_size, Image.Resampling.LANCZOS))

# Save ICO file
ico_path = "C:\\Semptify\\Semptify\\semptify_icon.ico"
icons[0].save(ico_path, format='ICO', sizes=[(s[0], s[1]) for s in icon_sizes])

print(f"✓ Icon created: {ico_path}")
print(f"✓ Sizes: {', '.join([f'{s[0]}x{s[1]}' for s in icon_sizes])}")
