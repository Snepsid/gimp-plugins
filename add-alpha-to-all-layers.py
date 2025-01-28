#!/usr/bin/env python

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
    "Snepsid",
    "2023",
    "<Image>/Layer/Add Alpha to All Layers",
    "RGB*, GRAY*",
    [],
    [],
    add_alpha_to_all_layers)

main()
