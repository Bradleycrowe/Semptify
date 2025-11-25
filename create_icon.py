"""
Convert Semptify logo JPG to ICO for desktop shortcut
"""
from PIL import Image
import sys

try:
    # Open the JPG
    img = Image.open('semptify_logo.jpg')
    
    # Convert to RGBA if needed
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Resize to standard icon sizes
    icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    
    # Save as ICO with multiple sizes
    img.save('semptify_logo.ico', format='ICO', sizes=icon_sizes)
    
    print("✅ Icon created: semptify_logo.ico")
    sys.exit(0)
    
except ImportError:
    print("⚠️  PIL/Pillow not installed. Installing now...")
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Pillow'])
    print("✅ Pillow installed. Please run this script again.")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Error creating icon: {e}")
    sys.exit(1)
