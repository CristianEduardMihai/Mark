import os
import json
from PIL import Image
from tkinter import Tk
from tkinter import filedialog
import sys
import piexif

#TODO: Add Author and CopyRight to EXIF data

def load_config():
    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
        return config
    except FileNotFoundError:
        print("Config file not found. Please create a 'config.json' file.")
        exit()

def wait_for_keypress():
    print("Press any key to exit.")
    input()
    exit()

def print_progress_bar(iteration, total, length=50):
    progress = int(length * iteration // total)
    bar = ">" * progress + "-" * (length - progress)
    sys.stdout.write(f"\r[{bar}] {iteration}/{total}")
    sys.stdout.flush()

def get_image_paths():
    root = Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(title='Select photos to watermark', filetypes=[('Image files', '*.png;*.jpg;*.jpeg')])
    root.destroy()

    if not file_paths:
        print("No files selected.")
        wait_for_keypress()

    # Check if all images are from the same folder
    folders = set(os.path.dirname(path) for path in file_paths)
    if len(folders) > 1:
        print("Error: Photos are from different folders. Please select photos from the same folder.")
        exit()

    return file_paths

def watermark_image(image_path, output_folder, config):
    # Open the original image and get its format
    original_image = Image.open(image_path)
    original_format = original_image.format

    # Convert to RGBA for watermarking
    image = original_image.convert("RGBA")
    # Load watermark image and scale it
    watermark = Image.open(config["watermark_path"]).convert("RGBA")
    watermark = watermark.resize((int(watermark.width * config["scale"]), int(watermark.height * config["scale"])))
    # Calculate horizontal position (centered)
    x_position = (image.width - watermark.width) // 2
    # Calculate vertical position (taking into account vertical margin and scaled watermark height)
    y_position = image.height - config["vertical_margin"] - watermark.height
    # Paste watermark onto the image
    image.paste(watermark, (x_position, y_position), watermark)

    # Preserve original metadata using piexif
    original_exif = piexif.load(original_image.info["exif"] if "exif" in original_image.info else b"")
    exif_bytes = piexif.dump(original_exif)

    output_filename = os.path.basename(image_path)

    # Convert back to RGB if the original format is non-PNG
    if original_format == "JPEG":
        image = image.convert("RGB")
    # MPO format
    elif original_format == "MPO" and config["convert_MPO_to_JPG"] == False:
        print(f"\n Warning: Image {output_filename} is in MPO format. Data will be lost when converting to JPEG. Set 'convert_MPO_to_JPG' to True in config.json to convert MPO to JPEG.")
        return
    elif original_format == "MPO" and config["convert_MPO_to_JPG"] == True:
        print(f"\n Warning: Converted MPO image {output_filename} to JPEG.")
        image = image.convert("RGB")
        original_format = "JPEG"

    
    # Check if file already exists
    if os.path.exists(os.path.join(output_folder, output_filename)):
        print(f"\nError: File {output_filename} already exists. Please delete the file and try again.")
        return
    output_path = os.path.join(output_folder, output_filename)
    image.save(output_path, format=original_format, exif=exif_bytes)

def main():
    config = load_config()
    image_paths = get_image_paths()

    output_folder = os.path.join(os.path.dirname(image_paths[0]), "watermarked")
    os.makedirs(output_folder, exist_ok=True)

    total_images = len(image_paths)

    for i, image_path in enumerate(image_paths, start=1):
        watermark_image(image_path, output_folder, config)
        print_progress_bar(i, total_images)

    print("\nWatermarking complete. Check the 'watermarked' folder for the results.")
    wait_for_keypress()

if __name__ == "__main__":
    main()
