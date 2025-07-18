#!/usr/bin/env python3
"""
Generate simple placeholder icons for the PWA.
This creates basic icons with the restaurant emoji as a starting point.
For production, replace with proper app icons.
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("PIL/Pillow not available. Install with: pip install Pillow")

def create_simple_icon(size: int, filename: str):
    """Create a simple icon with restaurant emoji background."""
    if not PIL_AVAILABLE:
        print(f"Cannot create {filename} - PIL not available")
        return
    
    # Create image with blue background
    img = Image.new('RGB', (size, size), '#2563eb')
    draw = ImageDraw.Draw(img)
    
    # Add white circle background
    margin = size // 8
    draw.ellipse([margin, margin, size-margin, size-margin], fill='white')
    
    # Try to add text (emoji might not render properly)
    try:
        font_size = size // 3
        font = ImageFont.load_default()
        text = "🍽️"
        
        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center the text
        x = (size - text_width) // 2
        y = (size - text_height) // 2
        
        draw.text((x, y), text, font=font, fill='#2563eb')
    except:
        # Fallback: draw a simple shape
        center = size // 2
        radius = size // 6
        draw.ellipse([center-radius, center-radius, center+radius, center+radius], 
                    fill='#2563eb')
    
    # Save the image
    img.save(filename, 'PNG')
    print(f"Created {filename} ({size}x{size})")

def main():
    """Generate all required icon sizes."""
    if not PIL_AVAILABLE:
        print("To create icons automatically, install Pillow:")
        print("pip install Pillow")
        print("\nAlternatively, create these icon files manually:")
        sizes = [16, 32, 120, 152, 180, 192, 512]
        for size in sizes:
            print(f"  - icon-{size}.png ({size}x{size} pixels)")
        return
    
    # Icon sizes needed for PWA
    icon_sizes = [16, 32, 120, 152, 180, 192, 512]
    
    print("Generating PWA icons...")
    for size in icon_sizes:
        create_simple_icon(size, f'icon-{size}.png')
    
    print("\n✅ All icons generated!")
    print("💡 Replace these placeholder icons with your custom app icons for better branding.")

if __name__ == "__main__":
    main()
