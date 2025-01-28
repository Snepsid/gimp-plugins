#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Progressive Crop Plugin for GIMP
# Author: Snepsid
# Version: 1.0.0
# Description: Creates progressively smaller cropped versions of images
# License: CC0 1.0 Universal

from gimpfu import *
import os

def progressive_crop(input_folder, output_folder, start_percentage, step_percentage):
    # List of supported image extensions
    supported_formats = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif')
    files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

    for index, f in enumerate(files):
        input_path = os.path.join(input_folder, f)
        output_path = os.path.join(output_folder, f)

        try:
            # Check if file is a supported image format
            if not f.lower().endswith(supported_formats):
                continue
                
            # Load image based on file type
            img = pdb.gimp_file_load(input_path, input_path)
            drawable = img.active_layer
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
            
            # Save with original format
            pdb.gimp_file_save(img, drawable, output_path, output_path)
            pdb.gimp_image_delete(img)
            
        except Exception as e:
            continue

    return

register(
    "progressive_crop",
    "Progressively crop a series of images",
    "Crops a series of images from an input folder progressively to smaller dimensions",
    "Snepsid",
    "CC0 1.0 Universal",
    "2023",
    "Progressive Crop...",
    "",
    [
        (PF_DIRNAME, "input_folder", "Input folder", ""),
        (PF_DIRNAME, "output_folder", "Output folder", ""),
        (PF_FLOAT, "start_percentage", "Start percentage (0-100)", 100),
        (PF_FLOAT, "step_percentage", "Step percentage (0-100)", 5),
    ],
    [],
    progressive_crop,
    menu="<Image>/File")

main()