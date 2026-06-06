import os
import shutil
import glob
from PIL import Image, ImageDraw, ImageFont

# Define paths
ARTIFACT_DIR = r"C:\Users\HUAWEI\.gemini\antigravity\brain\72c584bd-61dd-4ca4-b41e-016d21e51a08"
PROJECT_DIR = r"c:\Users\HUAWEI\OneDrive\Escritorio\proyecto abram"
MEDIA_PROFILES_DIR = os.path.join(PROJECT_DIR, "media", "profiles")
MEDIA_POSTS_DIR = os.path.join(PROJECT_DIR, "media", "posts")

# Ensure target directories exist
os.makedirs(MEDIA_PROFILES_DIR, exist_ok=True)
os.makedirs(MEDIA_POSTS_DIR, exist_ok=True)

# 1. Copy the AI-generated images from artifacts
def copy_artifact_image(pattern, dest_dir, dest_name):
    matches = glob.glob(os.path.join(ARTIFACT_DIR, pattern))
    if matches:
        # Sort by creation/modification time descending to get the newest one if multiple
        matches.sort(key=os.path.getmtime, reverse=True)
        src = matches[0]
        dest = os.path.join(dest_dir, dest_name)
        shutil.copy2(src, dest)
        print(f"Copied {os.path.basename(src)} to {dest}")
        return True
    else:
        print(f"No match found for pattern: {pattern}")
        return False

# Copy profiles
copy_artifact_image("maslow_profile*.png", MEDIA_PROFILES_DIR, "maslow.png")
copy_artifact_image("skinner_profile*.png", MEDIA_PROFILES_DIR, "skinner.png")
copy_artifact_image("mcgregor_profile*.png", MEDIA_PROFILES_DIR, "mcgregor.png")

# Copy posts
copy_artifact_image("maslow_post*.png", MEDIA_POSTS_DIR, "maslow_post.png")
copy_artifact_image("skinner_post*.png", MEDIA_POSTS_DIR, "skinner_post.png")
copy_artifact_image("mcgregor_post*.png", MEDIA_POSTS_DIR, "mcgregor_post.png")


# 2. Helper functions to generate high-fidelity gradients with Pillow
def draw_gradient(draw, width, height, color1, color2):
    # Draw linear gradient from top-left to bottom-right
    for y in range(height):
        # Interpolation ratio
        r_ratio = y / height
        r = int(color1[0] * (1 - r_ratio) + color2[0] * r_ratio)
        g = int(color1[1] * (1 - r_ratio) + color2[1] * r_ratio)
        b = int(color1[2] * (1 - r_ratio) + color2[2] * r_ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

def get_font(size):
    # Try to load a standard system font, otherwise fallback to default
    fonts_to_try = [
        "arial.ttf",      # Windows
        "calibri.ttf",    # Windows
        "segoeui.ttf",    # Windows
        "Helvetica.ttf",
        "LiberationSans-Regular.ttf"
    ]
    for font_name in fonts_to_try:
        try:
            return ImageFont.truetype(font_name, size)
        except IOError:
            continue
    return ImageFont.load_default()

# 3. Generate Victor Vroom's images
# Profile (Cyan-Blue Gradient with "VV" initials)
print("Generating Victor Vroom's profile picture...")
vroom_prof_img = Image.new("RGB", (300, 300))
draw = ImageDraw.Draw(vroom_prof_img)
draw_gradient(draw, 300, 300, (0, 150, 255), (0, 50, 150))
font = get_font(100)
# Draw text centered (approximate centering)
draw.text((150, 150), "VV", fill=(255, 255, 255), font=font, anchor="mm")
vroom_prof_img.save(os.path.join(MEDIA_PROFILES_DIR, "vroom.png"))

# Post (Expectancy Theory: Motivation = E * I * V)
print("Generating Victor Vroom's post image...")
vroom_post_img = Image.new("RGB", (1080, 1080))
draw = ImageDraw.Draw(vroom_post_img)
draw_gradient(draw, 1080, 1080, (0, 70, 160), (0, 20, 50))

font_title = get_font(64)
font_subtitle = get_font(40)
font_body = get_font(28)

# Title
draw.text((540, 150), "TEORÍA DE LAS EXPECTATIVAS", fill=(255, 255, 255), font=font_title, anchor="mm")
draw.text((540, 220), "Victor Vroom", fill=(0, 200, 255), font=font_subtitle, anchor="mm")

# Formula Box
draw.rectangle([140, 320, 940, 500], fill=(0, 40, 100), outline=(0, 200, 255), width=4)
draw.text((540, 410), "Motivación = E  x  I  x  V", fill=(255, 255, 255), font=font_title, anchor="mm")

# Details
draw.text((540, 580), "E = Expectativa (Esfuerzo -> Rendimiento)", fill=(255, 255, 255), font=font_body, anchor="mm")
draw.text((540, 660), "I = Instrumentalidad (Rendimiento -> Recompensa)", fill=(255, 255, 255), font=font_body, anchor="mm")
draw.text((540, 740), "V = Valencia (Valoración de la recompensa)", fill=(255, 255, 255), font=font_body, anchor="mm")

# Footer/Brand
draw.rounded_rectangle([200, 850, 880, 970], fill=(0, 150, 255), radius=15)
draw.text((540, 910), "La motivación depende de la expectativa de éxito", fill=(255, 255, 255), font=font_body, anchor="mm")

vroom_post_img.save(os.path.join(MEDIA_POSTS_DIR, "vroom_post.png"))


# 4. Generate Frederick Herzberg's images
# Profile (Coral-Purple Gradient with "FH" initials)
print("Generating Frederick Herzberg's profile picture...")
herzberg_prof_img = Image.new("RGB", (300, 300))
draw = ImageDraw.Draw(herzberg_prof_img)
draw_gradient(draw, 300, 300, (255, 90, 95), (120, 20, 120))
font = get_font(100)
draw.text((150, 150), "FH", fill=(255, 255, 255), font=font, anchor="mm")
herzberg_prof_img.save(os.path.join(MEDIA_PROFILES_DIR, "herzberg.png"))

# Post (Two-Factor Theory: Motivation vs Hygiene)
print("Generating Frederick Herzberg's post image...")
herzberg_post_img = Image.new("RGB", (1080, 1080))
draw = ImageDraw.Draw(herzberg_post_img)
draw_gradient(draw, 1080, 1080, (80, 15, 80), (30, 5, 40))

# Title
draw.text((540, 150), "TEORÍA DE LOS DOS FACTORES", fill=(255, 255, 255), font=font_title, anchor="mm")
draw.text((540, 220), "Frederick Herzberg", fill=(255, 120, 150), font=font_subtitle, anchor="mm")

# Split Layout boxes
# Left Box: Factores Higiénicos (Evitan la insatisfacción)
draw.rectangle([80, 300, 500, 850], fill=(60, 20, 50), outline=(255, 120, 150), width=3)
draw.text((290, 350), "FACTOR HIGIENE", fill=(255, 120, 150), font=font_subtitle, anchor="mm")
draw.text((290, 400), "(Entorno laboral)", fill=(200, 200, 200), font=font_body, anchor="mm")

hygiene_points = ["• Sueldo y beneficios", "• Condiciones de trabajo", "• Políticas de la empresa", "• Seguridad laboral", "• Relaciones con colegas"]
for idx, point in enumerate(hygiene_points):
    draw.text((120, 480 + idx*70), point, fill=(255, 255, 255), font=font_body)

# Right Box: Factores Motivacionales (Generan satisfacción)
draw.rectangle([580, 300, 1000, 850], fill=(30, 70, 50), outline=(0, 230, 150), width=3)
draw.text((790, 350), "FACTOR MOTIVACIÓN", fill=(0, 230, 150), font=font_subtitle, anchor="mm")
draw.text((790, 400), "(El trabajo en sí)", fill=(200, 200, 200), font=font_body, anchor="mm")

motivator_points = ["• Logro y reconocimiento", "• Trabajo desafiante", "• Responsabilidad", "• Crecimiento profesional", "• Progreso y ascenso"]
for idx, point in enumerate(motivator_points):
    draw.text((620, 480 + idx*70), point, fill=(255, 255, 255), font=font_body)

# Footer
draw.text((540, 940), "Lo opuesto a la insatisfacción no es la satisfacción, sino la no insatisfacción", fill=(200, 200, 200), font=font_body, anchor="mm")

herzberg_post_img.save(os.path.join(MEDIA_POSTS_DIR, "herzberg_post.png"))

print("All media assets have been successfully set up!")
