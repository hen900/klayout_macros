
import pya
import os
import sys 
import re
from os.path import exists


#helper function used to extract parameters from subcells
def find_between(text, first, last):
  start = text.find(first) + len(first)
  end = text.find(last, start)
  return str(text[start:end]) if start != -1 and end != -1 else None




# This python script is meant to run as a macro in klayout 

####
#    Tiling script used to place transistors or other test devices into one layout
#    This script relies on an existing gds for alignment marks (if they are being 
#    used) and all devices loaded into one gds.Intructions on importing individual
#    device gds files into one file containing all devices as subcells can be found here:
#    

#    NOTE: 
#    All coordinates are in the form value_in_um*1000. This is for converting um 
#    measurements into database unites
####



###########---------------------- Begin User Editable Parameters------------------------------###########

##### GDS Path Parameters #####

all_cells_file="./example_tiling/1T1R_EBL_cells_ex.gds" #Gds containing all devices to be tiled as subcells
created_containing_cell_name="1T1R_EBL_placed_transistors" #Topcell name for output gds
output_file="./example_tiling/1T1R_EBL_tiled_example.gds" #Output file path


########## Alignment Cross Parameters ##########
  
place_cross=True
marker_cell_file="./example_tiling/markers.gds" #File for alignement cross, lower left corner should be placed at the origin
marker_name="Cross_!" # Name of the cell with the marker to use 
num_markers=3 # Number of markers to be placed
marker_coords_x = [0,10*1000,20*1000]  #coordinates for markers upon initial placement, 
marker_coords_y = [75*1000,75*1000,75*1000] 

########## General Subcell Parameters ##########
#Every tile cell should have the lower left corner at (0,0)
#Coordinates for alignement crosses are based on lower left corner of the cross cell


#length and width of tile subcell in nm
y_pitch=68 * 1000 
x_pitch=280 * 1000
num_t_across=7 #number of tiles to placed across 

#Gap between tiled subcells
x_gap=40*1000
y_gap=40*1000


########## Text Parameters ##########

add_text=True
custom_font=False
font_file="./example_tiling/block_via_font.gds"
# Where the lower left hand corner of the text is placed
text_x=0
text_y=68.01000*1000
#layer to create text on 
text_layer_n=255
#size of placed text
txt_size=16
label="1T1R" #label is used at the beginning of every text label ie "1T1R W32 L100 NMOS..." etc

#NOTE: When determining parameters for cell placement, the program excepts cells to named as such:
# label_w_l_type_voltage_
#ex: x1T1R_w100_l100_nmos_1_8V_
#    x1T1R_w100_l100_pmos_5V_

##################################### END PARAMS ##################################### 

def main():
 test= exists(all_cells_file)
 if not test:
   raise AttributeError("Fatal Error: Cell Source File " + all_cells_file + " Not Found")
 
 test= exists(cross_cell_file)
 if not test:
   raise AttributeError("Fatal Error: Cross Source File " + cross_cell_file + " Not Found")
 
 if custom_font:
   test= exists(font_file)
   if not test:
     raise AttributeError("Fatal Error: Cross Source File " + font_file + " Not Found")

 if (len(marker_coords_x) != len(marker_coords_y)):
   raise AttributeError("Fatal Error: marker_coords_x: \nnumber of marker x coords given != number marker y coords given")
 elif (len(marker_coords_x) != num_markers):
   raise AttributeError( str(len(marker_coords_x)) + " marker coordinate sets provided for " + str(num_markers) + " markers...")
 
 print("############################################")
 print("Importing cells ...")
 if (custom_font):
  print("Importing font ...")
 
 print("Starting Tiling ...") 
 
 
 #helper variables for placement 
 dx=0
 dy=0
 nx=0
 ny=0
 counter=0


 #Create KLayout object
 KLAYOUT = pya.Layout()
 
 # Create Top Cell Name & Obj of the GDS to be EXPORTED
 TOP_CELL = KLAYOUT.create_cell(created_containing_cell_name)
 
 # Read Top Cell for each GDS file
 KLAYOUT.read(all_cells_file)
 
 KLAYOUT.read(cross_cell_file)

 marker0 = KLAYOUT.cell(marker_name)
 marker_cells = [pya.Cell] * num_markers
 
 marker_cells[0] = marker0
 
 for m in range(1,num_markers):
   marker_cells[m] = marker0.dup()

 for top_cell_read in KLAYOUT.top_cells():
    

     if (top_cell_read.name != created_containing_cell_name and cross_name not in top_cell_read.name): # Don't insert TOP_CELL on itself
       counter=counter+1
       cell_index = top_cell_read.cell_index()
        
       if (nx == num_t_across):
         nx=0
         ny=ny+1
         dx=0
         dy=(y_pitch+y_gap)*ny

       
       nx=nx+1
       dx=(x_pitch+x_gap)*nx

  
       #new_instance = pya.CellInstArray( cell_index, pya.Trans(pya.Vector(dx,dy)), pya.Vector(x_pitch, 0), pya.Vector(0, y_pitch), 1, 0 )
       new_instance = pya.CellInstArray( cell_index, pya.Trans(pya.Point(dx,dy)))

       TOP_CELL.insert( new_instance)  
     
       for m in range(0,num_markers):
         top_cell_read.insert(pya.CellInstArray.new(marker_cells[m].cell_index(),  pya.Trans.new(pya.Point(marker_coords_x[m],marker_coords_y[m]))))
   
       if (add_text):
         name=top_cell_read.name
         try:
           width = str(find_between(name,"_w","_l"))
           length = str(find_between(name,str(width)+"_l","_"))
           typ = find_between(name,"l"+str(length)+"_","_")
           voltage=str(find_between(name,str(typ) + "_","V_"))
           typ=str(typ.upper())    
           lum_lib_txt = label + " " + "W" + width + " L" + length  +  " "+ typ+ " "+ voltage + "V"
          
         except AttributeError or TypeError:
           print("RUN FAILURE!")
           raise AttributeError("Error Extracting paramters from cell names..\nMake sure cells to be tiled are named according to the text finding function.")
    
         #Layer text is to be placed on 
         txt_layer = pya.LayerInfo(text_layer_n, 0)
         KLAYOUT.layer(txt_layer)

         #Instantiate and create text pcell

         param  = { "layer": txt_layer, "text": lum_lib_txt, "mag": txt_size }
         txtcell = KLAYOUT.create_cell("TEXT", "Basic", param)

         text_trans = pya.Trans(0, False, text_x,text_y)
         top_cell_read.insert(pya.CellInstArray.new(txtcell.cell_index(), text_trans))
          
 
 # Export GDS
 KLAYOUT.write(output_file)
 print("Output file located at " + output_file )
 print("Done!")
 
 
if __name__ == '__main__':
  main()
