# Python GUI Tiling Program Documentation

## Program Overview
The program is designed to run as a macro within the KLayout layout editor. It automates the process of placing transistors or other test devices into a layout by tiling them according to user-defined parameters. The program relies on an existing GDS (Graphic Data System) file for alignment marks (if they are being used) and a single GDS file containing all the individual device cells that need to be tiled.

## Running the Program
To run the program, follow these steps:

1. Open the "Macro Development" menu in KLayout and select the "Add Location" option using right click
2. Add the location of the device_tiler_macro directory downloaded from github
3. The Macro should now appear when hovering over the "Macro" bar up top

#### Klayout Coordinate System
Throughout the entirety of this program and documentation, any tine an object is referenced by its coordinates, the values for x and y are based on the position of the **lower left hand corner** of the object and referred to in microns.
### Cell Placement
**X Gap:** Field to specify the horizontal gap between tiles (um).  <br>
**Y Gap:** Field to specify the vertical gap between tiles (um). <br>
**Y Pitch:** Field to specify the vertical height of each subccell to be tiled (um). <br>
**X Pitch:** Field to specify the width of each subcell to be tiled (um). <br>

### Marker Placement
Markers are placed in a horizontal line originating at the coordinates specified. <br>
**Marker Name:** Text input field to specify the name of the marker to be used.  <br>
> This assumes a cell by the marker name exists in the marker file. <br>
**Marker Coordinates (X, Y):** Fields to specify the placement of markers in **um**. <br>
> Markers will be placed in a line, and this specifies where the lower left coordinate of the line of markers should be. <br>
**Marker Gap:** Field to specify the desired horizontal gap between consecutive markers in um. <br>




### Text Placement 
>  **IMPORTANT NOTE** Default text parameter extraction expects to tile a set of cells labeled as something like:  <br>
>  `x1T1R_w100_l50_pmos_1_8V_EBL` <br>
>  where the width length, type and voltage are are extracted based on cell names and then used for labeling.
>  It is likely that the user will have to edit the parameter extraction of the script and utilize the included
>  `find_between` function to readjust the name to match other cell naming conventions  <br>
**Text Coordinates (X, Y):** Fields to specify the X and Y coordinates of the **lower left corner** of the placed text


### Other Parameters
 **Number of Tiles Across:** Field to specify the number of subcells to place across the layout, the number of tiles down will simply be based on the total number of provided subcells. <br>
**Number of Markers:** Field to specify the number of alignment markers to be placed. <br>
**Text Layer Number:** Text input field to specify the layer on which  to place the text labels. <br>
**Text Size:** Input field to specify the size of the text labels in um. <br>
**Label:** Text input field to specify the prefix for placed text <br>


