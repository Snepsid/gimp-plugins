# GIMP Plugins Collection

A collection of Python plugins for GIMP to enhance your image editing workflow.

## Plugins

### All Layers to Alpha

Adds an alpha channel to all layers in the image that don't already have one. This is useful for ensuring all layers can handle transparency before performing operations that require an alpha channel.

### Batch Progressive Crop

Creates progressively smaller cropped versions of images in a sequence, maintaining center focus. Each subsequent image is cropped by a specified percentage, making the subject appear larger in each frame while maintaining original image quality.

### Batch Upscale Sequence

Processes a sequence of images, progressively increasing their size. Each subsequent image is scaled up by a compounding percentage, creating a smooth zoom effect when the sequence of output images is used in a video or animation.

### Batch Zoom Crop Sequence

Creates a sequence of progressively zoomed images with enhanced file format support. Automatically handles multiple image formats (PNG, JPEG, TIFF, BMP, WebP) and creates an output directory within the input folder. Converts lossy formats to PNG during processing to maintain quality.

### Create Sprite Sheet

Creates a sprite sheet from all layers in your image, with options for automatic or manual row/column configuration. Works with both regular layers and layer groups, preserving layer visibility states.

### Export Layers as PNGs

Exports each layer of the current image as individual PNG files in your chosen directory.

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

### All Layers to Alpha
1. Open your image in GIMP
2. Go to Layer > Add Alpha to All Layers
3. Alpha channels will be added to any layers that don't already have them

Note: The plugin processes all layers, including hidden ones, but preserves their visibility states.

### Batch Progressive Crop
1. Go to File > Batch Progressive Crop...
2. Set the following options:
   - Input folder: Directory containing your source images
   - Output folder: Where to save processed images
   - Start percentage (0-100): Initial crop size as percentage of original
   - Step percentage (0-100): How much to reduce each subsequent image
3. The plugin supports various formats including PNG, JPEG, GIF, BMP, and TIFF

### Batch Upscale Sequence
1. Go to File > Batch Upscale Sequence...
2. Set the following options:
   - Input directory: Folder containing your image sequence
   - Output directory: Where to save the upscaled images
   - Scale step percentage: The percentage to increase each subsequent image (compounds)
   - Interpolation mode: Choose the scaling algorithm:
     - None: Nearest neighbor (pixelated)
     - Linear: Basic smoothing
     - Cubic: Better quality
     - Sinc (Lanczos3): Highest quality
3. The plugin processes images in alphabetical order

### Batch Zoom Crop Sequence
1. Go to File > Batch Zoom Crop Sequence...
2. Set the following options:
   - Input Folder: Directory containing your source images
   - Start percentage (0-100): How zoomed in the sequence will end up
   - Step percentage (0-100): How much to change the zoom between frames
   - Interpolation mode:
     - None: Nearest neighbor (pixelated)
     - Linear: Basic smoothing
     - Cubic: Better quality
     - Sinc (Lanczos3): Highest quality
3. The plugin will:
   - Create a "batch-zoom-effect-output" folder in your input directory
   - Process all supported image formats
   - Automatically convert JPEG and WebP to PNG to prevent quality loss
   - Maintain original format for PNG, TIFF, and BMP files

### Export Layers as PNGs
1. Open your multi-layer image in GIMP
2. Go to File > Export > Export Layers as PNG...
3. Select a destination directory
4. The plugin will save each layer as a PNG file in the selected directory

### Create Sprite Sheet
1. Open your image with multiple layers in GIMP
2. Go to File > Create Sprite Sheet...
3. Options:
   - Rows: Number of rows (0 for automatic calculation)
   - Columns: Number of columns (0 for automatic calculation)
4. If both rows and columns are set to 0, the plugin will automatically calculate the most square-like arrangement

## Contributing

Feel free to open issues or submit pull requests with improvements!

## License

This work is dedicated to the public domain under CC0 1.0 Universal. See the LICENSE file for details.