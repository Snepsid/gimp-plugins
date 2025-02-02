#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Batch Progressive Crop Plugin for GIMP
# Author: Snepsid (https://github.com/snepsid)
# Description: Creates progressively smaller cropped versions of images
# License: CC0 1.0 Universal

from gimpfu import *
import os

# File type definitions
MAGIC_NUMBERS = {
    b'\x89PNG\r\n\x1a\n': 'png',
    b'\xFF\xD8\xFF': 'jpeg',
    b'II*\x00': 'tiff',
    b'MM\x00*': 'tiff',
    b'BM': 'bmp',
    b'RIFF': 'webp'  # Additional check for WEBP needed
}

def get_file_type(filepath):
    """Determine file type by reading magic numbers."""
    try:
        with open(filepath, 'rb') as f:
            header = f.read(12)
            
            # Check magic numbers
            for magic, filetype in MAGIC_NUMBERS.items():
                if header.startswith(magic):
                    # Additional check for WebP
                    if filetype == 'webp' and header[8:12] != b'WEBP':
                        continue
                    return filetype
            return None
    except:
        return None

def load_image(filepath, filetype):
    """Load image based on detected file type."""
    if filetype == 'jpeg':
        return pdb.file_jpeg_load(filepath, filepath)
    elif filetype == 'tiff':
        return pdb.file_tiff_load(filepath, filepath)
    elif filetype == 'bmp':
        return pdb.file_bmp_load(filepath, filepath)
    elif filetype == 'webp':
        return pdb.file_webp_load(filepath, filepath)
    else:  # PNG or fallback
        return pdb.file_png_load(filepath, filepath)

def save_image(img, drawable, output_path, output_ext):
    """Save image with appropriate format and settings."""
    if output_ext == '.tiff':
        pdb.file_tiff_save(img, drawable, output_path, output_path, 1)
    elif output_ext == '.bmp':
        pdb.file_bmp_save(img, drawable, output_path, output_path)
    else:
        pdb.file_png_save(img, drawable, output_path, output_path, 0, 9, 1, 1, 1, 1, 1)

def is_valid_image(filepath):
    """Check if the file is a valid image that can be processed."""
    try:
        filetype = get_file_type(filepath)
        if not filetype:
            return False
            
        img = load_image(filepath, filetype)
        pdb.gimp_image_delete(img)
        return True
    except:
        return False

def batch_progressive_crop(input_folder, start_percentage, step_percentage):
    # Create output folder inside input folder
    output_folder = os.path.join(input_folder, "batch-progressive-crop-output")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
    files.sort()  # Sort files for consistent processing

    for index, f in enumerate(files):
        input_path = os.path.join(input_folder, f)
        output_path = os.path.join(output_folder, f)

        try:
            # Skip invalid images early
            if not is_valid_image(input_path):
                continue

            # Load image based on actual file type
            filetype = get_file_type(input_path)
            img = load_image(input_path, filetype)
            drawable = img.active_layer

            # Convert lossy formats to PNG
            if filetype in ('jpeg', 'webp'):
                output_path = os.path.splitext(output_path)[0] + '.png'

            width = img.width
            height = img.height

            # Calculate the current percentage to keep
            current_percentage = start_percentage - (index * step_percentage)
            
            # Calculate new dimensions
            crop_width = int((width * current_percentage) / 100)
            crop_height = int((height * current_percentage) / 100)
            
            # Calculate the offset to keep the crop centered
            x_offset = (width - crop_width) // 2
            y_offset = (height - crop_height) // 2

            # Perform the crop
            pdb.gimp_image_crop(img, crop_width, crop_height, x_offset, y_offset)
            
            # Save with appropriate format
            save_image(img, drawable, output_path, os.path.splitext(output_path)[1].lower())
            pdb.gimp_image_delete(img)
            
        except Exception as e:
            continue

    return

register(
    "python_fu_batch_progressive_crop",
    "Batch Progressive Crop",
    "Crops a series of images from an input folder progressively to smaller dimensions",
    "Snepsid",
    "CC0 1.0 Universal",
    "2023",
    "Batch Progressive Crop...",
    "",
    [
        (PF_DIRNAME, "input_folder", "Input folder", ""),
        (PF_FLOAT, "start_percentage", "Start percentage (0-100)", 100),
        (PF_FLOAT, "step_percentage", "Step percentage (0-100)", 5),
    ],
    [],
    batch_progressive_crop,
    menu="<Image>/File")

main()