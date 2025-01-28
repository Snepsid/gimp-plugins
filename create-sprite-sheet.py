#!/usr/bin/env python

# Create Sprite Sheet Plugin for GIMP
# Author: Snepsid
# Version: 1.0.0
# Description: Creates a sprite sheet from all layers in an image
# License: CC0 1.0 Universal

from gimpfu import *
import math

def create_sprite_sheet(image, drawable, rows=0, columns=0):
    def get_layers(drawable, layers_list):
        if hasattr(drawable, 'layers'):  # Check if it's a group
            for subgroup in drawable.layers:
                get_layers(subgroup, layers_list)
        else:
            layers_list.append(drawable)

    all_layers = []
    for layer in image.layers:
        get_layers(layer, all_layers)

    num_layers = len(all_layers)

    auto_calculated = False
    if rows == 0 or columns == 0:
        columns = int(math.ceil(math.sqrt(num_layers)))
        rows = int(math.ceil(num_layers / float(columns)))
        auto_calculated = True

    sprite_width = drawable.width
    sprite_height = drawable.height
    sheet_width = sprite_width * columns
    sheet_height = sprite_height * rows

    sprite_sheet = gimp.Image(sheet_width, sheet_height, RGB)
    sprite_sheet.disable_undo()

    visibility_states = [layer.visible for layer in all_layers]
    for layer in all_layers:
        layer.visible = True

    for i, layer in enumerate(all_layers):
        sprite = pdb.gimp_layer_new_from_drawable(layer, sprite_sheet)
        sprite_sheet.add_layer(sprite, -1)

        row = i // columns
        col = i % columns
        x = col * sprite_width
        y = row * sprite_height

        sprite.set_offsets(x, y)

    for layer, state in zip(all_layers, visibility_states):
        layer.visible = state

    sprite_sheet.enable_undo()
    gimp.Display(sprite_sheet)
    gimp.displays_flush()

    if auto_calculated:
        gimp.message("Auto-calculated sprite sheet dimensions: {} rows x {} columns.".format(rows, columns))

register(
    "python_fu_create_sprite_sheet",
    "Create a Sprite Sheet",
    "Create a sprite sheet from all layers including hidden ones, automatically calculating rows and columns",
    "Snepsid",
    "CC0 1.0 Universal",
    "2023",
    "Create Sprite Sheet...",
    "*",      # Image types
    [
        (PF_IMAGE, "image", "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None),
        (PF_INT, "rows", "Rows (0 for auto)", 0),
        (PF_INT, "columns", "Columns (0 for auto)", 0)
    ],
    [],
    create_sprite_sheet,
    menu="<Image>/File"
)

main()
