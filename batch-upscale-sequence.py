#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Batch Upscale Sequence for GIMP
# Author: Snepsid (https://github.com/snepsid)
# Description: Processes a sequence of images, progressively increasing their size.
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

def batch_upscale_sequence(input_directory, scale_step_percentage, interpolation_mode):
    # Create output folder inside input directory
    output_directory = os.path.join(input_directory, "batch-upscale-sequence-output")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Get and sort all files
    files = [f for f in os.listdir(input_directory) if os.path.isfile(os.path.join(input_directory, f))]
    files.sort()

    base_scale = 1 + scale_step_percentage / 100.0

    for index, f in enumerate(files):
        input_path = os.path.join(input_directory, f)
        output_path = os.path.join(output_directory, f)

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

            # Calculate cumulative scale factor (each image scales up from the previous one)
            current_scale = base_scale ** (index + 1)  # Start from 1 instead of 0
            
            new_width = int(img.width * current_scale)
            new_height = int(img.height * current_scale)

            # Set interpolation mode and scale
            pdb.gimp_context_set_interpolation(interpolation_mode)
            pdb.gimp_image_scale(img, new_width, new_height)
            
            # Save with appropriate format
            save_image(img, drawable, output_path, os.path.splitext(output_path)[1].lower())
            pdb.gimp_image_delete(img)
            
        except Exception as e:
            continue

    return

register(
    "python_fu_batch_upscale_sequence",
    "Batch Upscale Sequence",
    "Upscale a series of images with progressively increasing scale factors.",
    "Snepsid",
    "CC0 1.0 Universal",
    "2023",
    "Batch Upscale Sequence...",
    "",
    [
        (PF_DIRNAME, "input_directory", "Input directory", ""),
        (PF_FLOAT, "scale_step_percentage", "Scale step percentage", 1.0),
        (PF_OPTION, "interpolation_mode", "Interpolation mode", 0, ("None", "Linear", "Cubic", "Sinc (Lanczos3)")),
    ],
    [],
    batch_upscale_sequence,
    menu="<Image>/File"
)

main()