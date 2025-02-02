#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Batch Zoom Crop Sequence Plugin for GIMP
# Author: Snepsid (https://github.com/snepsid)
# Description: Creates zoom sequences with multi-format support
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

def batch_zoom_crop_sequence(input_folder, start_percentage, step_percentage, interpolation_mode):
    """Main function for batch processing images with zoom crop effect."""
    # Create output folder inside input folder
    output_folder = os.path.join(input_folder, "batch-zoom-crop-sequence-output")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Get list of valid files and sort them
    all_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
    all_files.sort()

    # Process files sequentially
    processed_count = 0
    for f in all_files:
        input_path = os.path.join(input_folder, f)
        
        # Skip invalid images
        if not is_valid_image(input_path):
            continue
            
        output_path = os.path.join(output_folder, f)

        try:
            # Load and process image
            filetype = get_file_type(input_path)
            img = load_image(input_path, filetype)
            drawable = img.active_layer

            # Convert lossy formats to PNG
            if filetype in ('jpeg', 'webp'):
                output_path = os.path.splitext(output_path)[0] + '.png'

            # Calculate crop percentage: start large and get smaller
            crop_percentage = max(start_percentage, 100 - (processed_count * step_percentage))
            
            # Calculate dimensions based on the crop percentage
            crop_width = int(img.width * crop_percentage / 100)
            crop_height = int(img.height * crop_percentage / 100)

            # Center the crop
            x_offset = (img.width - crop_width) // 2
            y_offset = (img.height - crop_height) // 2

            # Crop and scale
            pdb.gimp_image_crop(img, crop_width, crop_height, x_offset, y_offset)
            pdb.gimp_context_set_interpolation(interpolation_mode)
            pdb.gimp_image_scale(img, img.width, img.height)

            # Save processed image
            save_image(img, drawable, output_path, os.path.splitext(output_path)[1].lower())

            pdb.gimp_image_delete(img)
            processed_count += 1
        except:
            continue

register(
    "python_fu_batch_zoom_crop_sequence",
    "Batch Zoom Crop Sequence",
    "Creates a sequence of images with progressive zoom and crop effects",
    "Snepsid",
    "CC0 1.0 Universal",
    "2023",
    "Batch Zoom Crop Sequence...",
    "",
    [
        (PF_DIRNAME, "input_folder", "Input Folder", ""),
        (PF_INT, "start_percentage", "Start percentage (0-100)", 10),
        (PF_INT, "step_percentage", "Step percentage (0-100)", 5),
        (PF_OPTION, "interpolation_mode", "Interpolation mode", 0, ("None", "Linear", "Cubic", "Sinc (Lanczos3)")),
    ],
    [],
    batch_zoom_crop_sequence,
    menu="<Image>/File"
)

main()