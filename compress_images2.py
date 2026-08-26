from PIL import Image
import os

input_folder = r'E:\ANTS\ants photos\2026\AUG\photos\sorted'
output_folder = r'E:\ANTS\ants photos\2026\AUG\photos\sorted\compressed'

os.makedirs(output_folder, exist_ok=True)

MAX_SIZE = (1920, 1920)   # bump up from 1200 if you want more detail retained
JPEG_QUALITY = 90         # 80 was too aggressive

processed = 0
for f in os.listdir(input_folder):
    if f.lower().endswith(('.jpg', '.jpeg', '.png')):
        input_path = os.path.join(input_folder, f)
        output_path = os.path.join(output_folder, f)

        img = Image.open(input_path)

        # Convert PNG with transparency to RGB before saving as JPEG
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        img.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)
        img.save(
            output_path,
            quality=JPEG_QUALITY,
            optimize=True,
            subsampling=0,   # keep full chroma detail
            progressive=True # slightly better perceived quality at same size
        )
        processed += 1
        print(f'✅ {f}')

print(f'\nDone! {processed} images saved to: {output_folder}')