# Klayout Tiling Program

## Program Overview
The program is designed to run as a macro within the KLayout layout editor. It automates the process of placing transistors or other test devices into a layout by tiling them according to user-defined parameters. The program relies on an existing GDS (Graphic Data System) file for alignment marks (if they are being used) and a single GDS file containing all the individual device cells that need to be tiled.

---

## Running the Program
To run the program, follow these steps:

1. Open the "Macro Development" menu in KLayout and select the "Add Location" option using right-click.
2. Add the location of the `device_tiler_macro` directory downloaded from GitHub.
3. The Macro should now appear when hovering over the "Macro" bar at the top.

![alt text](https://github.com/hen900/klayout_macros/blob/main/img_docs/importing_macro.jpg?raw=true)


> **Note on KLayout Coordinate System**  
> Throughout the entirety of this program and documentation, whenever an object is referenced by its coordinates, the values for x and y are based on the position of the **lower left-hand corner** of the object and referred to in microns.

---
### Example GUI Dialog

![alt text](https://github.com/hen900/klayout_macros/blob/main/img_docs/input_params.jpg?raw=true)
> Above is an example of the parameter dialog and the corresponding output generated

### Cell Placement

**X Gap:** Field to specify the horizontal gap between tiles (um).  

**Y Gap:** Field to specify the vertical gap between tiles (um).  

**Y Pitch:** Field to specify the vertical height of each subcell to be tiled (um).  

**X Pitch:** Field to specify the width of each subcell to be tiled (um).
![alt text](https://github.com/hen900/klayout_macros/blob/main/img_docs/ez_cell_params.jpg?raw=true)

---

### Marker Placement

**Marker Name:** Text input field to specify the name of the marker to be used.
* This assumes a cell with the marker name exists in the marker file.

**Marker Coordinates (X, Y):** Fields to specify the placement of markers in **um**.

* Markers will be placed in a line, and this specifies where the lower left coordinate of the line of markers should be.

**Marker Gap:** Field to specify the desired horizontal gap between consecutive markers in um.
![alt text](https://github.com/hen900/klayout_macros/blob/main/img_docs/marker_placement.jpg?raw=true)

### Marker Movement In Output

![alt text](https://github.com/hen900/klayout_macros/blob/main/img_docs/marker_movement.jpg?raw=true)

---

### Text Placement
**Text Coordinates (X, Y):** Fields to specify the X and Y coordinates of the **lower left corner** of the placed text.

**IMPORTANT NOTE:**
> Default text parameter extraction expects to tile a set of cells labeled as something like:  
> `x1T1R_w100_l50_pmos_1_8V_EBL`  
> where the width length, type, and voltage are extracted based on cell names and then used for labeling. It is likely that the user will have to edit the parameter extraction of the script and utilize the included `find_between` function to readjust the name to match other cell naming conventions.

---

### Other Parameters

**Number of Tiles Across:** Field to specify the number of subcells to place across the layout. The number of tiles down will simply be based on the total number of provided subcells.  

**Number of Markers:** Field to specify the number of alignment markers to be placed.  

**Text Layer Number:** Text input field to specify the layer on which to place the text labels.  

**Text Size:** Input field to specify the size of the text labels in um.  

**Label:** Text input field to specify the prefix for placed text.
