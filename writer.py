
import bases
import line_shapes
import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm.auto import tqdm

cmap = plt.get_cmap('viridis')
#---------Functions for creating unique binary numbers------
def cycle_list(l,loops = 1):
    n = len(l)
    for t in range(loops):
        l = [l[(i+1) % n] for i in range(n)]
    return(l)

def generate_unique_combinations(L):
    combinations = generate_binary_strings(L)
    non_repeating = [combinations[0]]
    for i in tqdm(range(len(combinations)),desc = "Genearting Unique Binary Numbers"):
        ref = list(combinations[i])
        N = len(ref)
        test = 0
        for j in range(len(non_repeating)):
            for n in range(N):
                
                if cycle_list(list(non_repeating[j]),loops = n+1) == ref:
                    test += 1
        
        if test == 0:
            non_repeating.append(combinations[i])
            
    for i in np.arange(len(non_repeating)):
        non_repeating[i] = [int(s) for s in list(non_repeating[i])]
    return(non_repeating)

def genbin(n, bs = ''):
    if n-1:
        genbin(n-1, bs + '0')
        genbin(n-1, bs + '1')
    else:
        print('1' + bs)

def generate_binary_strings(bit_count):
    binary_strings = []
    def genbin(n, bs=''):
        if len(bs) == n:
            binary_strings.append(bs)
        else:
            genbin(n, bs + '0')
            genbin(n, bs + '1')


    genbin(bit_count)
    return binary_strings

#-------Functions for drawing runes
def decode_shape(in_array,k=1,point_color = 'k',on_color = 'darkred',off_color = "grey",
                 label = None,base_fn = bases.polygon,base_kwargs = [],
                 shape_fn = line_shapes.straight,shape_kwargs = [],
                 plot_base = False):
    #decodes a single array into a given base, use plot_base = True if you are plotting it on its own
    n = len(in_array)
    x,y = base_fn(n,*base_kwargs)
    if plot_base == True:
        plt.scatter(x[1:],y[1:],s = 70,facecolors = 'none', edgecolors = point_color)
        plt.scatter(x[0],y[0],s = 70,facecolors = point_color, edgecolors = point_color)
        plt.axis('off')
        plt.axis('scaled')
    for i,elem in enumerate(in_array):
        P = [x[i],y[i]]
        Q = [x[(i+k)%n],y[(i+k)%n]]
        X,Y = shape_fn(P,Q,*shape_kwargs)
        if elem == 0:
            plt.plot(X,Y,color = off_color,ls = "--",linewidth=0.25)
        elif elem == 1:
            plt.plot(X,Y,color = on_color,ls = "-",label = label if i == np.where(in_array == 1)[0][0] else None,
                     linewidth = 2)
        else:
            print(f'elem {elem} at index {i} is not valid, input being skipped')
    

def draw_multiple_inputs(in_array,
                         base_fn = bases.polygon,base_kwargs = [],
                         shape_fn = line_shapes.straight,shape_kwargs = [],
                         point_color = 'k',labels = [],legend = False,colors = [],
                         legend_loc = "upper left"):
    
    #draws multiple inputs on a single base
    if isinstance(colors,list) and len(colors) == 0:
        colors = [point_color]*in_array.shape[0]
    elif isinstance(colors,str):
        colors = [colors]*in_array.shape[0]
    n = in_array.shape[1]
    x,y = base_fn(n,*base_kwargs)
    plt.scatter(x[1:],y[1:],s = 70,facecolors = 'none', edgecolors = point_color)
    plt.scatter(x[0],y[0],s = 70,facecolors = point_color, edgecolors = point_color)
    
    if len(labels) != in_array.shape[0]:
        labels = [None]*in_array.shape[0]

    for i,k in enumerate(range(in_array.shape[0])):

        decode_shape(in_array[i],k = k+1,base_fn = base_fn,base_kwargs = base_kwargs,
                     shape_fn = shape_fn,shape_kwargs = shape_kwargs,label = labels[i],on_color = colors[i])

    if labels[0] != None and legend == True:
        plt.legend(loc = legend_loc,fontsize = 10)
    plt.axis('off')
    plt.axis('scaled')
def load_attribute(fname):
    with open(fname,"r") as f:
        data = f.readlines()
        f.close()
    data = [d.replace("\n","").lower() for d in data]
    return(data)


def draw_spell(level,rang,area,dtype,school,title = None,
               savename = "output.png",legend = False,
                base_fn = bases.polygon,base_kwargs = [],
                shape_fn = line_shapes.straight,shape_kwargs = [],
                colors = [],legend_loc = "upper left",breakdown = False):
    
    #draws a spell given certain values by comparing it to input txt
    ranges = load_attribute("Attributes/range.txt")
    levels = load_attribute("Attributes/levels.txt")
    area_types = load_attribute("Attributes/area_types.txt")
    dtypes = load_attribute("Attributes/damage_types.txt")
    schools = load_attribute("Attributes/school.txt")
    i_range = ranges.index(rang)
    i_levels = levels.index(str(level))
    i_area = area_types.index(area)
    i_dtype = dtypes.index(dtype)
    i_school = schools.index(school)
    attributes = [i_levels,i_school,i_dtype,i_area,i_range]
    labels = [f"level: {level}",
              f"school: {school}",
              f"damage type: {dtype}",
              f"range: {rang}",
              f"area_type: {area}"]
    N = 2*len(attributes)+1
    
    if len(colors) == 0 and breakdown == True:
        colors = [cmap(i/len(attributes)) for i in range(len(attributes))]
    if not os.path.isdir("Uniques/"):
        os.makedirs("Uniques/")
    if os.path.isfile(f'Uniques/{N}.npy'):
        non_repeating = np.load(f'Uniques/{N}.npy')
    else:
        non_repeating = generate_unique_combinations(N)
        non_repeating = np.array(non_repeating)
        np.save(f"Uniques/{N}.npy",non_repeating)
    input_array = np.array([non_repeating[i] for i in attributes])#note +1 s.t. 0th option is always open for empty input
    #print(input_array)
    draw_multiple_inputs(input_array,labels = labels,legend = legend,
                         base_fn = base_fn,base_kwargs = base_kwargs,
                         shape_fn = shape_fn,shape_kwargs = shape_kwargs,
                         colors = colors,legend_loc = legend_loc)
    
    plt.title(title,fontsize = "80")
    
    if savename is not None:
        plt.savefig(savename,transparent = False, bbox_inches='tight')
        plt.clf()
    else:
        plt.show()

def draw_spell_2(level,rang,area,dtype,school,duration,concentration,ritual,title = None,
               savename = "output.png",legend = False,
                base_fn = bases.polygon,base_kwargs = [],
                shape_fn = line_shapes.straight,shape_kwargs = [],
                colors = [],legend_loc = "upper left",breakdown = False,
                base_dir = ""):
    
    #draws a spell given certain values by comparing it to input txt
    ranges = load_attribute(base_dir +"Attributes/range.txt")
    levels = load_attribute(base_dir +"Attributes/levels.txt")
    area_types = load_attribute(base_dir +"Attributes/area_types.txt")
    dtypes = load_attribute(base_dir +"Attributes/damage_types.txt")
    schools = load_attribute(base_dir +"Attributes/school.txt")
    durations = load_attribute(base_dir +"Attributes/duration.txt")
    i_range = ranges.index(rang)
    i_levels = levels.index(str(level))
    i_area = area_types.index(area)
    i_dtype = dtypes.index(dtype)
    i_school = schools.index(school)
    i_duration = durations.index(duration)
    attributes = [i_levels,i_school,i_dtype,i_area,i_range,i_duration]
    labels = [f"level: {level}",
              f"school: {school}",
              f"damage type: {dtype}",
              f"range: {rang}",
              f"area_type: {area}",
              f'duration: {duration}']
    N = 2*len(attributes)+1
    
    if len(colors) == 0 and breakdown == True:
        colors = [cmap(i/len(attributes)) for i in range(len(attributes))]
    if not os.path.isdir(base_dir +"Uniques/"):
        os.makedirs(base_dir +"Uniques/")
    if os.path.isfile(base_dir +f'Uniques/{N}.npy'):
        non_repeating = np.load(base_dir +f'Uniques/{N}.npy')
    else:
        non_repeating = generate_unique_combinations(N)
        non_repeating = np.array(non_repeating)
        np.save(base_dir +f"Uniques/{N}.npy",non_repeating)
    input_array = np.array([non_repeating[i] for i in attributes])#note +1 s.t. 0th option is always open for empty input
    
    draw_multiple_inputs(input_array,labels = labels,legend = legend,
                         base_fn = base_fn,base_kwargs = base_kwargs,
                         shape_fn = shape_fn,shape_kwargs = shape_kwargs,
                         colors = colors,legend_loc = legend_loc)
    
    if concentration:
        plt.plot(0,0,"",markersize = 10,marker = ".",color = colors)
    if ritual:
        
        plt.plot(0,0,"",markersize = 10,marker = ".",color= colors)
        plt.plot(0,0,"",markersize = 20,marker = "o",color=colors,mfc='none',linewidth = 10)
    
    plt.title(title)
    if savename is not None:
        plt.savefig(savename,transparent = True, bbox_inches='tight')
        plt.clf()
    else:
        plt.show()

#to run if the file is called
def draw_attribute(level = None,rang = None, area = None,
                   savename = "output.png",legend = False,
                    dtype = None, school = None,duration = None,
                    base_fn = bases.polygon,base_kwargs = [],
                shape_fn = line_shapes.straight,shape_kwargs = [],
                colors = [],legend_loc = "upper left",breakdown = False,
                title = None):
    ranges = load_attribute("Attributes/range.txt")
    levels = load_attribute("Attributes/levels.txt")
    area_types = load_attribute("Attributes/area_types.txt")
    dtypes = load_attribute("Attributes/damage_types.txt")
    schools = load_attribute("Attributes/school.txt")
    durations = load_attribute("Attributes/duration.txt")

    i_range,i_levels,i_school,i_dtype,i_area,i_duration = 0,0,0,0,0,0
    if rang is not None:
        i_range = ranges.index(rang)

    elif level is not None:
        i_levels = levels.index(str(level))

    elif area is not None:
        i_area = area_types.index(area)

    elif dtype is not None:
        i_dtype = dtypes.index(dtype)

    elif school is not None:
        i_school = schools.index(school)

    elif duration is not None:
        i_duration = durations.index(duration)
    attributes = [i_levels,i_school,i_dtype,i_area,i_range,i_duration]
    labels = [f"level: {level}",
            f"school: {school}",
            f"damage type: {dtype}",
            f"range: {rang}",
            f"area_type: {area}",
            f"duration: {duration}"]
    
    N = 2*len(attributes)+1
    
    if isinstance(colors,list) and len(colors) == 0 and breakdown == True:
        colors = [cmap(i/len(attributes)) for i in range(len(attributes))]
    if not os.path.isdir("Uniques/"):
        os.makedirs("Uniques/")
    if os.path.isfile(f'Uniques/{N}.npy'):
        non_repeating = np.load(f'Uniques/{N}.npy')
    else:
        non_repeating = generate_unique_combinations(N)
        non_repeating = np.array(non_repeating)
        np.save(f"Uniques/{N}.npy",non_repeating)
    
    input_array = []
    for j,i in enumerate(attributes):
        input_array.append(non_repeating[i])
    input_array = np.array(input_array)#note +1 s.t. 0th option is always open for empty input
    #print(input_array)
    draw_multiple_inputs(input_array,labels = labels,legend = legend,
                         base_fn = base_fn,base_kwargs = base_kwargs,
                         shape_fn = shape_fn,shape_kwargs = shape_kwargs,
                         colors = colors,legend_loc = legend_loc)
    plt.title(title,fontsize = 30)
    if savename is not None:
        plt.savefig(savename,dpi = 250,transparent = True, bbox_inches='tight')
        plt.clf()
    else:
        plt.show()
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-spell-name",help = "spell name")
    parser.add_argument("-level",help = "necessary input: level of the spell")
    parser.add_argument("-range",help = "necessary input: range of the spell")
    parser.add_argument("-area",help = "necessary input: area type of the spell")
    parser.add_argument("-dtype",help = "necessary input: dtype of the spell")
    parser.add_argument("-school",help = "necessary input: school of the spell")
    parser.add_argument("--title",help = "title in plot")
    parser.add_argument("--savename",help = "savename of file")
    parser.add_argument("--legend",help = "bool to print legend or not (0 = False,1 = True)")
    parser.add_argument("--breakdown",help = "bool to control whether to breakdown the lines with colour")
    parser.add_argument("-ah", "--arg_help",help = "Prints the available options for the chosen attributes",action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    if args.arg_help:
        if args.range:
            print("--------Range--------")
            print("\n".join(load_attribute("Attributes/range.txt")))
        if args.level:
            print("--------Level--------")
            print("\n".join(load_attribute("Attributes/levels.txt")))
        if args.area:
            print("--------Area--------")
            print("\n".join(load_attribute("Attributes/area_types.txt")))
        if args.dtype:
            print("--------Damage Types--------")
            print("\n".join(load_attribute("Attributes/damage_types.txt")))
        if args.school:
            print("--------School--------")
            print("\n".join(load_attribute("Attributes/school.txt")))
    else:
        if args.legend:
            if args.legend == 1:
                legend = False
            else:
                legend = True
        else:
            legend = False

        if args.breakdown:
            if args.breakdown == 1:
                breakdown = False
            else:
                breakdown = True
        else:
            breakdown= False

        if not args.title:
            title = None
        if not args.savename:
            savename = "output.png"

        if not args.level:
            level = "3"
        else:
            level = args.level
        
        if not args.range:
            rang = "150ft"
        else:
            rang = args.range
        
        if not args.area:
            area = "sphere30"
        else:
            area = args.area
        
        if not args.dtype:
            dtype = "fire"
        else:
            dtype = args.dtype

        if not args.school:
            school = "evocation"
        else:
            school = args.school

        draw_spell(level,rang,area,dtype,school,title = title,legend = legend,
                base_fn = bases.polygon,shape_fn = line_shapes.straight,
                breakdown = breakdown,savename = savename)
        plt.clf()
        
    