from PIL import Image
import os

input_folder = r'H:\ANTS\ants photos\2026\April 4 2026 Sports Day\photos\sorted\posting'
output_folder = r'H:\ANTS\ants photos\2026\April 4 2026 Sports Day\photos\sorted\posting\compressed'

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

processed = 0
for f in os.listdir(input_folder):
    if f.lower().endswith(('.jpg', '.jpeg', '.png')):
        input_path = os.path.join(input_folder, f)
        output_path = os.path.join(output_folder, f)
        
        img = Image.open(input_path)
        img.thumbnail((1200, 1200))
        img.save(output_path, quality=80, optimize=True)
        processed += 1
        print(f'✅ {f}')

print(f'\nDone! {processed} images saved to: {output_folder}')