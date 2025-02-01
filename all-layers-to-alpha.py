#!/usr/bin/env python

# Add Alpha to All Layers Plugin for GIMP
# Author: Snepsid (https://github.com/snepsid)
# Version: 1.0.0
# Description: Adds alpha channel to all layers that don't have one
# License: CC0 1.0 Universal

from gimpfu import *

def add_alpha_to_all_layers(image, drawable):
    for layer in image.layers:
        if not layer.has_alpha:
            pdb.gimp_layer_add_alpha(layer)
    gimp.displays_flush()

register(
    "add_alpha_to_all_layers",
    "Add alpha channel to all layers",
    "Add alpha channel to all layers in the image",
    "Snepsid",
    "CC0 1.0 Universal",
    "2023",
    "<Image>/Layer/All Layers to Alpha",
    "RGB*, GRAY*",
    [],
    [],
    add_alpha_to_all_layers)

main()
