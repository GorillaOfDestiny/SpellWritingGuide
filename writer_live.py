from writer import *
from bokeh.layouts import column,row
from bokeh.models import Button,CustomJS, Dropdown
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc,show

def create_dropdown(att,label = "Dropdown"):
    menu = [(l.capitalize(),l.lower()) for l in att]
    dropdown = Dropdown(label=label, menu=menu)
    dropdown.js_on_event("menu_item_click", CustomJS(code="console.log('dropdown: ' + this.item, this.toString())"))
    return(dropdown)

def callback(ddms):
    #!!!!!!!!!!!
    #This is where I've got to, need to collect drop down info and then 
    # find what arrays to use etc.
    # then plot them using the correct function
    # might be best to keep it to straight line behaviour for now
    pass

#define base function
base_fn = bases.polygon

#define number of points
n = 11
#get base
x,y = base_fn(n)

#load attributes
ranges = load_attribute("Attributes/range.txt")
levels = load_attribute("Attributes/levels.txt")
area_types = load_attribute("Attributes/area_types.txt")
dtypes = load_attribute("Attributes/damage_types.txt")
schools = load_attribute("Attributes/school.txt")

#initialise figure
fig_size = 750
p = figure(width = fig_size ,height = fig_size ,x_range = (-1.5,1.5), y_range = (-1.5,1.5),toolbar_location = None)
p.outline_line_color = None
p.grid.grid_line_color = None
p.scatter(x,y,size = 10,fill_color = "black",line_color = "navy")
p.axis.visible = False

#setup dropdowns
ranges_ddm = create_dropdown(ranges,"Range")
levels_ddm = create_dropdown(levels,"Level")
area_types_ddm = create_dropdown(area_types,"Area_type")
dtypes_ddm = create_dropdown(dtypes,"damage_type")
schools_ddm = create_dropdown(schools,"Schools")

button = Button(label="Press Me")
button.on_event('button_click', callback)
if __name__ == "__main__":
    show(p)

row1 = row(ranges_ddm,levels_ddm,area_types_ddm)
row2 = row(dtypes_ddm,schools_ddm)

curdoc().add_root(column(row1,row2,button, p))