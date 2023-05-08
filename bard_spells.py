from writer import load_attribute
import librosa


class scale():
    def __init__(self,steps,max_L,f0 = 440):
        n = [0]
        while len(n) < max_L:
            for s in list(steps):
                n.append(n[-1] + int(s))
        

        self.n = n
        
        #default values
        self.f0 = f0
    def get_note(self,i):
        N = self.n[i] #+(i//len(self.n))
        a = (2)**(1/12)
        f = self.f0*a**N
        return(f)


def chords_maker(rang,level,area,dtype,school,scale_steps = "2212221",f0 = 440):
    ranges = load_attribute("attributes/range.txt")
    levels = load_attribute("attributes/levels.txt")
    area_types = load_attribute("attributes/area_types.txt")
    dtypes = load_attribute("attributes/damage_types.txt")
    schools = load_attribute("attributes/school.txt")

    lens = [len(ranges),len(levels),len(area_types),len(dtypes),len(schools)]
    reference_scale = scale(scale_steps,max_L = max(lens),f0 = f0)
    i_range = ranges.index(rang)
    i_levels = levels.index(level)
    i_area = area_types.index(area)
    i_dtype = dtypes.index(dtype)
    i_school = schools.index(school)
    attr = [i_range,i_levels,i_area,i_dtype,i_school]

    while len(set(attr)) != len(attr):
        seen = []
        for i,a in enumerate(attr):
            if a in seen:
                attr[i] += lens[i]
            else:
                seen.append(a)
    
    f = []
    for i in attr:
        f.append(reference_scale.get_note(i))
    return(f)

if __name__ == "__main__":
    major = "2212221"
    minor = "2122122"
    blues = "321132"
    A4 = 440
    Middle_C = 264
    f = chords_maker('point (150 feet)','3',"sphere","fire","evocation",scale_steps = blues,f0 = Middle_C)
    for f_ in f:
        print(librosa.hz_to_note(f_))
    
