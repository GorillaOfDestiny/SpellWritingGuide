from writer import load_attribute
import librosa

class scale():
    def __init__(self, steps, max_L, f0=440):
        n = [0]
        while len(n) < max_L:
            for s in list(steps):
                n.append(n[-1] + int(s))
        
        self.n = n
        self.f0 = f0  # default base frequency (A4)
    
    def get_note(self, i):
        N = self.n[i]
        a = (2) ** (1/12)
        f = self.f0 * a ** N
        return f

def cleric_chords_maker(rang, level, area, dtype, domain, scale_steps="2212221", f0=440):
    ranges = load_attribute("attributes/range.txt")
    levels = load_attribute("attributes/levels.txt")
    area_types = load_attribute("attributes/area_types.txt")
    dtypes = load_attribute("attributes/damage_types.txt")
    domains = load_attribute("attributes/domain.txt")

    lens = [len(ranges), len(levels), len(area_types), len(dtypes), len(domains)]
    reference_scale = scale(scale_steps, max_L=max(lens), f0=f0)
    i_range = ranges.index(rang)
    i_levels = levels.index(level)
    i_area = area_types.index(area)
    i_dtype = dtypes.index(dtype)
    i_domain = domains.index(domain)
    attr = [i_range, i_levels, i_area, i_dtype, i_domain]

    while len(set(attr)) != len(attr):
        seen = []
        for i, a in enumerate(attr):
            if a in seen:
                attr[i] += lens[i]
            else:
                seen.append(a)
    
    f = []
    for i in attr:
        f.append(reference_scale.get_note(i))
    
    return f

if __name__ == "__main__":
    major = "2212221"
    minor = "2122122"
    dorian = "2122212"
    phrygian = "1212212"
    locrian = "1221221"
    A4 = 440
    Middle_C = 264

    f = cleric_chords_maker('touch', '2', "cone", "radiant", "Life", scale_steps=dorian, f0=Middle_C)
    for f_ in f:
        print(librosa.hz_to_note(f_))
