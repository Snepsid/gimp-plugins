#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Batch Zoom Effect Plugin for GIMP
# Author: Snepsid
# Version: 1.0.0
# Description: Creates zoom effect sequences with quality preservation
# License: CC0 1.0 Universal

from gimpfu import *
import os
from multiprocessing import Pool, cpu_count

# Global function definitions
def is_valid_image(filepath):
    """Check if the file is a valid image that can be processed."""
    try:
        img = pdb.file_png_load(filepath, filepath)
        pdb.gimp_image_delete(img)
        return True
    except:
        return False

def process_single_image(input_path, output_path, width, height, start_percentage, step_percentage, interpolation, index):
    """Process a single image with error handling."""
    try:
        if not is_valid_image(input_path):
            gimp.message("Skipping incompatible file: " + input_path)
            return False

        img = pdb.file_png_load(input_path, input_path)
        drawable = img.active_layer

        # Calculate crop percentage: start large and get smaller
        # The first frame (lowest number) will be the most zoomed out (100%)
        # and subsequent frames will get more zoomed in
        crop_percentage = max(start_percentage, 100 - (index * step_percentage))
        
        # Calculate dimensions based on the crop percentage
        crop_width = int(width * crop_percentage / 100)
        crop_height = int(height * crop_percentage / 100)

        # Center the crop
        x_offset = (width - crop_width) // 2
        y_offset = (height - crop_height) // 2

        # Crop and scale
        pdb.gimp_image_crop(img, crop_width, crop_height, x_offset, y_offset)
        pdb.gimp_context_set_interpolation(interpolation)
        pdb.gimp_image_scale(img, width, height)
        pdb.file_png_save(img, drawable, output_path, output_path, 0, 9, 1, 1, 1, 1, 1)

        pdb.gimp_image_delete(img)
        return True
    except Exception as e:
        gimp.message("Error processing " + input_path + ": " + str(e))
        return False

def batch_zoom_effect(input_folder, output_folder, start_percentage, step_percentage, interpolation):
    """Main function with improved error handling and file filtering."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get list of files
    all_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
    all_files.sort()  # Sort files by name

    # Process files sequentially
    successful = 0
    valid_count = 0

    for index, f in enumerate(all_files):
        input_path = os.path.join(input_folder, f)
        output_path = os.path.join(output_folder, f)

        try:
            if is_valid_image(input_path):
                valid_count += 1
                img = pdb.file_png_load(input_path, input_path)
                width, height = img.width, img.height
                pdb.gimp_image_delete(img)

                if process_single_image(input_path, output_path, width, height, 
                                     start_percentage, step_percentage, 
                                     interpolation, valid_count - 1):
                    successful += 1
        except Exception as e:
            gimp.message("Error validating " + f + ": " + str(e))
            continue

    if valid_count == 0:
        gimp.message("No valid images found in the input folder.")
    else:
        gimp.message("Successfully processed " + str(successful) + " out of " + 
                    str(valid_count) + " valid images.")

    return

register(
    "python_fu_batch_zoom_effect",
    "Batch Zoom Effect",
    "Crops and scales a series of images in a folder, progressively zooming in",
    "Snepsid",
    "CC0 1.0 Universal",
    "2023",
    "Batch Zoom Effect...",
    "",
    [
        (PF_DIRNAME, "input_folder", "Input Folder", ""),
        (PF_DIRNAME, "output_folder", "Output Folder", ""),
        (PF_INT, "start_percentage", "Start percentage (0-100)", 10),
        (PF_INT, "step_percentage", "Step percentage (0-100)", 5),
        (PF_OPTION, "interpolation_mode", "Interpolation mode", 3, ("None", "Linear", "Cubic", "Sinc (Lanczos3)")),
    ],
    [],
    batch_zoom_effect,
    menu="<Image>/File"
)

main()