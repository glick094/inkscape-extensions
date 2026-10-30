import random
import inkex
from inkex import Color

def interpolate_colors(c1, c2, t):
    """Linear RGB interpolation between two inkex.Color objects."""
    r = int(c1.red + t * (c2.red - c1.red))
    g = int(c1.green + t * (c2.green - c1.green))
    b = int(c1.blue + t * (c2.blue - c1.blue))
    return Color((r, g, b))

class RandomizeColors(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--target", type=str, default="fill")
        pars.add_argument("--mode", type=str, default="discrete")
        pars.add_argument("--palette_tab", type=str, default="tab_swatches")
        pars.add_argument("--num_colors", type=int, default=5)
        
        # Color swatches
        pars.add_argument("--color1", type=Color, default=Color("#ff5733"))
        pars.add_argument("--color2", type=Color, default=Color("#33ff57"))
        pars.add_argument("--color3", type=Color, default=Color("#3357ff"))
        pars.add_argument("--color4", type=Color, default=Color("#f0e68c"))
        pars.add_argument("--color5", type=Color, default=Color("#8a2be2"))
        pars.add_argument("--color6", type=Color, default=Color("#e63946"))
        
        # String list
        pars.add_argument("--palette", type=str, default="#ff5733,#33ff57,#3357ff")

    def effect(self):
        if not self.svg.selection:
            inkex.errormsg("Please select at least one object.")
            return

        parsed_colors = []

        # Automatically use whichever tab page was open when Apply was clicked
        if self.options.palette_tab == "tab_swatches":
            all_swatches = [
                self.options.color1,
                self.options.color2,
                self.options.color3,
                self.options.color4,
                self.options.color5,
                self.options.color6,
            ]
            parsed_colors = all_swatches[: self.options.num_colors]
        else:
            raw_colors = [c.strip() for c in self.options.palette.split(",") if c.strip()]
            for c_str in raw_colors:
                try:
                    parsed_colors.append(Color(c_str))
                except Exception:
                    pass

        if not parsed_colors:
            inkex.errormsg("No valid colors found in palette.")
            return

        for elem in self.svg.selection.values():
            if self.options.mode == "discrete" or len(parsed_colors) == 1:
                chosen = random.choice(parsed_colors)
            else:
                num_segments = len(parsed_colors) - 1
                seg_idx = random.randint(0, num_segments - 1)
                
                c1 = parsed_colors[seg_idx]
                c2 = parsed_colors[seg_idx + 1]
                t = random.random()
                
                chosen = interpolate_colors(c1, c2, t)

            hex_val = str(chosen)
            if self.options.target in ("fill", "both"):
                elem.style['fill'] = hex_val
            if self.options.target in ("stroke", "both"):
                elem.style['stroke'] = hex_val

if __name__ == '__main__':
    RandomizeColors().run()