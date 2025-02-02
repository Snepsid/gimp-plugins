#!/usr/bin/env python

# Export Layers as PNG Plugin for GIMP
# Author: Snepsid (https://github.com/snepsid)
# Description: Exports all layers as individual PNG files
# License: CC0 1.0 Universal

from gimpfu import *
import os

def export_layers_as_png(image, directory):
    pdb.gimp_image_undo_group_start(image)

    # Iterate through all layers
    for layer in image.layers:
        # Duplicate the image to keep the original intact
        temp_image = pdb.gimp_image_duplicate(image)
        temp_layer = pdb.gimp_layer_new_from_drawable(layer, temp_image)
        pdb.gimp_image_add_layer(temp_image, temp_layer, 0)

        # Define file name and path
        layer_name = layer.name
        file_name = "{}.png".format(layer_name)
        full_path = os.path.join(directory, file_name)

        # Save the layer as PNG
        pdb.file_png_save_defaults(temp_image, temp_layer, full_path, file_name)

        # Delete the duplicated image
        pdb.gimp_image_delete(temp_image)

    pdb.gimp_image_undo_group_end(image)

# Registering the plugin in GIMP
register(
    "python_fu_export_layers_as_pngs",
    "Export all layers as PNGs",
    "Export all layers in the image to individual PNG files",
    "Snepsid",
    "CC0 1.0 Universal",
    "2023",
    "Export Layers as PNG...",
    "*",      # Image types
    [
        (PF_IMAGE, "image", "Input image", None),
        (PF_DIRNAME, "directory", "Output directory", "/")
    ],
    [],
    export_layers_as_png,
    menu="<Image>/File/Export/"
)

main()
