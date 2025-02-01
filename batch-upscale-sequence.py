#!/usr/bin/env python

# Batch Upscale Sequence for GIMP
# Author: Snepsid (https://github.com/snepsid)
# Version: 1.0.0
# Description: Processes a sequence of images, progressively increasing their size.
# License: CC0 1.0 Universal

from gimpfu import *
import os

def batch_upscale_sequence(input_directory, output_directory, scale_step_percentage, interpolation_mode):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    images = [f for f in os.listdir(input_directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]
    images.sort()

    base_scale = 1 + scale_step_percentage / 100.0

    for index, image_name in enumerate(images):
        image_path = os.path.join(input_directory, image_name)
        image = pdb.gimp_file_load(image_path, image_path)
        
        # Calculate cumulative scale factor (each image scales up from the previous one)
        current_scale = base_scale ** (index + 1)  # Start from 1 instead of 0
        
        new_width = int(image.width * current_scale)
        new_height = int(image.height * current_scale)

        pdb.gimp_image_scale_full(image, new_width, new_height, interpolation_mode)

        output_image_path = os.path.join(output_directory, image_name)
        pdb.gimp_file_save(image, image.active_layer, output_image_path, output_image_path)

        pdb.gimp_image_delete(image)

    return

register(
    "python_fu_batch_upscale_sequence",
    "Batch Upscale Sequence",
    "Upscale a series of images with progressively increasing scale factors.",
    "Snepsid",
    "CC0 1.0 Universal",
    "2023",
    "Batch Upscale Sequence...",
    "",  # No image types since we're not working on an open image
    [
        (PF_DIRNAME, "input_directory", "Input directory", ""),
        (PF_DIRNAME, "output_directory", "Output directory", ""),
        (PF_FLOAT, "scale_step_percentage", "Scale step percentage", 1.0),
        (PF_OPTION, "interpolation_mode", "Interpolation mode", 3, ("None", "Linear", "Cubic", "Sinc (Lanczos3)")),
    ],
    [],
    batch_upscale_sequence,
    menu="<Image>/File"
)

main()