from pathlib import Path
from PIL import Image
import pillow_heif
import argparse
import sys


def convert_folder(input_folder: Path, output_folder: Path):
    if not input_folder.exists():
        print(f"❌ Input folder not found: {input_folder}")
        sys.exit(1)

    output_folder.mkdir(parents=True, exist_ok=True)

    heic_files = list(input_folder.glob("*.heic")) + list(input_folder.glob("*.HEIC"))

    if not heic_files:
        print("⚠️ No HEIC files found.")
        return

    for heic_path in heic_files:
        try:
            heif = pillow_heif.read_heif(heic_path)
            img = Image.frombytes(
                heif.mode, heif.size, heif.data, "raw"
            )
            out_path = output_folder / (heic_path.stem + ".jpg")
            img.save(out_path, "JPEG")
            print(f"✔ Converted: {heic_path.name} -> {out_path.name}")

        except Exception as e:
            print(f"❌ Error converting {heic_path.name}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Convert HEIC to JPEG.")
    parser.add_argument("input_folder", type=str, help="Folder containing HEIC files")
    parser.add_argument("output_folder", type=str, help="Folder for JPEG output")

    args = parser.parse_args()
    convert_folder(Path(args.input_folder), Path(args.output_folder))
