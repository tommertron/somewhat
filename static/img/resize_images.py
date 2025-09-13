from pathlib import Path
from PIL import Image

# configure
SRC_DIR = Path("/Users/tommertron/coding/hugo/somewhat/static/img")
DST_DIR = SRC_DIR / "resized"
WIDTH = 1200  # target width in px

DST_DIR.mkdir(exist_ok=True)

for img_path in SRC_DIR.iterdir():
    if img_path.is_file() and img_path.suffix.lower() in [".jpg", ".jpeg", ".png"]:
        with Image.open(img_path) as im:
            # scale down preserving aspect ratio
            w_percent = WIDTH / float(im.size[0])
            h_size = int(float(im.size[1]) * w_percent)
            resized = im.resize((WIDTH, h_size), Image.LANCZOS)

            new_name = img_path.stem + "-resized" + img_path.suffix
            out_path = DST_DIR / new_name
            resized.save(out_path, optimize=True, quality=85)

            print(f"Saved {out_path}")