# Create KLayout object
import pya
import os
import re


def find_between(text, first, last):
  start = text.find(first) + len(first)
  end = text.find(last, start)
  return str(text[start:end]) if start != -1 and end != -1 else None



KLAYOUT = pya.Layout()

all_cells="/Users/Henry Mackay/Documents/1T1R_UPDATE/Large_Placement/all_EBL_cells.gds"
font="/Users/Henry Mackay/Documents/1T1R_UPDATE/Large_Placement/block_via_font.gds"
output="/Users/Henry Mackay/Documents/1T1R_UPDATE/Large_Placement/EBL_unit_4x10.gds"

created_containing_cell_name="EBL_placed_transistors"



#length and width of transistor cell in um 

l=70.9
w=280



x_pitch=l*1000
y_pitch=w*1000

x_gap=320*1000
y_gap=80*1000

x_gap=x_gap+90000
y_gap=(y_gap+90000)-(90*1000)

y_gap=y_gap+2100+1600


text_x_gap=0
text_y_gap=115116 -( 45.816*1000) + 1600*2 


#helper variables for placement 
dx=0
dy=0
nx=0
ny=0

num_t_across=10
num_t_down=4

# Create Top Cell Name & Obj of the GDS to be EXPORTED
TOP_CELL = KLAYOUT.create_cell(created_containing_cell_name)


KLAYOUT.read(all_cells)
#  # Read Top Cell for each GDS file
for top_cell_read in KLAYOUT.top_cells():

    if (top_cell_read.name != created_containing_cell_name): # Don't insert TOP_CELL on itself
        print(top_cell_read.name)
       
        
        nx=nx+1
        cell_index = top_cell_read.cell_index()

        dx=dx+x_gap
        if (dx >= (x_gap*num_t_across) ):
          dx=0;
          dy=dy+y_gap

  
        new_instance = pya.CellInstArray( cell_index, pya.Trans(pya.Vector(dx,dy)), pya.Vector(x_pitch, 0), pya.Vector(0, y_pitch), 1, 0 )
        
        TOP_CELL.insert( new_instance)
                  
        move_cross=True
        add_text=True
        
        if (add_text):
          name=top_cell_read.name
        
          #Based on file naming convention of transistor gds files, used to get parameters
          width = find_between(name,"_w","_l")
          length = find_between(name,str(width)+"_l","_")
          typ=find_between(name,"_l"+str(length)+"_","_")
          voltage=find_between(name,typ + "_","V_EBL")
          
          lum_lib_txt = "1T1R W" + str(width) + " L" + str(length) + " "+ typ.upper() + " " + voltage

          txt_layer = pya.LayerInfo(1, 0)
          KLAYOUT.layer(txt_layer)
          param  = { "layer": txt_layer, "text": lum_lib_txt, "mag": 16 }
          txtcell = KLAYOUT.create_cell("TEXT", "Basic", param)
         
          text_trans = pya.Trans(0, False, dx-text_x_gap, dy+text_y_gap)
          TOP_CELL.insert(pya.CellInstArray.new(txtcell.cell_index(), text_trans))
          
          
        if (move_cross):
          cross0_trans = pya.Trans(pya.Vector(0,0), pya.Vector(0,(-23.15-4.8)*1000))
          cross1_trans = pya.Trans(pya.Vector(0,0), pya.Vector(0,0))
          cross2_trans = pya.Trans(pya.Vector(0,0), pya.Vector(0,0))

          #iterate  through all subcells looking for cross
          for inst in  top_cell_read.each_inst():
            cell_n=KLAYOUT.cell(inst.cell_index).name
            
                       
            if cell_n.find("Cross") != -1:
            
              if cell_n.find("$1$") != -1:
                inst.transform(cross1_trans)

                
              if cell_n.find("$2$") != -1:
                inst.transform(cross2_trans)
                
              else:
                
                inst.transform(cross0_trans)

 
          
# Create layer #'s
outline = KLAYOUT.layer(4, 10) # 3x3 Outline

# Draw outline of all cells
#TOP_CELL.shapes(outline).insert( pya.Box(0, 0, 14.5*x_pitch-1000+792, 4.7*y_pitch+6.664*1000) ) 

# Export GDS
KLAYOUT.write(output)
