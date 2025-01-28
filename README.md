# GIMP Plugins Collection

A collection of Python plugins for GIMP to enhance your image editing workflow.

## Plugins

### Create Sprite Sheet

Creates a sprite sheet from all layers in your image, with options for automatic or manual row/column configuration. Works with both regular layers and layer groups, preserving layer visibility states.

## Installation

1. Find your GIMP plugins directory:
   - Windows: `%APPDATA%\GIMP\2.10\plug-ins\`
   - Linux: `$HOME/.config/GIMP/2.10/plug-ins/`
   - macOS: `$HOME/Library/Application Support/GIMP/2.10/plug-ins/`
   
2. Copy the desired plugin(s) into this folder
3. Make sure the plugin files are executable:
   - Linux/macOS: `chmod +x plugin-name.py`
4. Restart GIMP

## Requirements

- GIMP 2.10 or later
- Python 2.7 (as required by GIMP 2.10)

## Usage

### Create Sprite Sheet
1. Open your image with multiple layers in GIMP
2. Go to File > Create Sprite Sheet...
3. Options:
   - Rows: Number of rows (0 for automatic calculation)
   - Columns: Number of columns (0 for automatic calculation)
4. If both rows and columns are set to 0, the plugin will automatically calculate the most square-like arrangement

Note: The plugin processes all layers, including hidden ones, but preserves their visibility states.

## Contributing

Feel free to open issues or submit pull requests with improvements!

## License

This work is dedicated to the public domain under CC0 1.0 Universal. See the LICENSE file for details.