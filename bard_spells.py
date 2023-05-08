from writer import load_attribute
import librosa


class scale():
    def __init__(self,steps,f0 = 440):
        if "s" in list(steps) or "t" in list(steps):
            n = [0]
            for s in list(steps):
            
                s = s.lower()
                if s == "s":
                    n.append(n[-1] + 1)
                elif s == "t":
                    n.append(n[-1] + 2)
                else:
                    print("Only t and s allowed in steps")
        else:
            n = [0]
            for s in list(steps):
                n.append(n[-1] + s)
        self.n = n

        #default values
        self.f0 = f0
    def get_note(self,i):
        N = self.n[i%len(self.n)] + (i//len(self.n))*len(self.n)
        a = (2)**(1/12)
        f = self.f0*a**N
        return(f)


def chords_maker(rang,level,area,dtype,school,scale_steps = "ttsttts",f0 = 440):
    ranges = load_attribute("attributes/range.txt")
    levels = load_attribute("attributes/levels.txt")
    area_types = load_attribute("attributes/area_types.txt")
    dtypes = load_attribute("attributes/damage_types.txt")
    schools = load_attribute("attributes/school.txt")
    lens = [len(ranges),len(levels),len(area_types),len(dtypes),len(schools)]
    reference_scale = scale(scale_steps,f0 = f0)
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
    f = chords_maker('10-feet radius','0',"circle","fire","evocation")
    for f_ in f:
        print(librosa.hz_to_note(f_))
    
