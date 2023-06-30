## Tiling Script for KLayout
This Python script can be used to tile transistors or other test devices into one layout. The script relies on an existing gds for alignment marks (if they are being used) and all devices loaded into one gds. Instructions on importing individual device gds files into one file containing all devices as subcells can be found here:

https://www.klayout.de/doc/code/class_Cell.html



## Usage

The script takes the following user-editable parameters:

### GDS Path Parameters

* all_cells_file: The path to the gds file containing all devices to be tiled as subcells.
* created_containing_cell_name: The name of the topcell for the output gds.
* output_file: The path to the output gds file.
### Alignment Cross Parameters

* place_cross: Whether or not to place alignment crosses.
* marker_cell_file: The path to the gds file containing the alignment crosses.
* marker_name: The name of the cell with the alignment crosses.
* num_markers: The number of alignment crosses to place.
* marker_coords_x: A list of x coordinates for the alignment crosses.
* marker_coords_y: A list of y coordinates for the alignment crosses.
### General Subcell Parameters

* y_pitch: The pitch of the tiled subcells in the y direction, in nanometers.
* x_pitch: The pitch of the tiled subcells in the x direction, in nanometers.
* num_t_across: The number of tiled subcells to place across in the x direction.
* x_gap: The gap between tiled subcells in the x direction, in nanometers.
* y_gap: The gap between tiled subcells in the y direction, in nanometers.
### Text Parameters

add_text: Whether or not to add text labels to the tiled subcells.
custom_font: Whether or not to use a custom font for the text labels.
* font_file: The path to the custom font file, if custom_font is True.
* text_x: The x coordinate of the lower left corner of the text labels, in nanometers.
* text_y: The y coordinate of the lower left corner of the text labels, in nanometers.
* text_layer_n: The layer number of the text labels.
* txt_size: The size of the text labels, in pixels.
* label: The text label prefix.
