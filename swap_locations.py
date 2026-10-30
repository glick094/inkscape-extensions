import inkex
from inkex import Transform

class SwapLocations(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--anchor", type=str, default="center")

    def get_anchor_point(self, bbox):
        anchor = self.options.anchor
        if anchor == "top_left":
            return bbox.x.minimum, bbox.y.minimum
        elif anchor == "top_right":
            return bbox.x.maximum, bbox.y.minimum
        elif anchor == "bottom_left":
            return bbox.x.minimum, bbox.y.maximum
        elif anchor == "bottom_right":
            return bbox.x.maximum, bbox.y.maximum
        # Default to bounding box center
        return bbox.center.x, bbox.center.y

    def effect(self):
        selection = list(self.svg.selection.values())
        
        # Require exactly 2 selected objects
        if len(selection) != 2:
            inkex.errormsg("Please select exactly two objects to swap locations.")
            return

        elem1, elem2 = selection[0], selection[1]

        bbox1 = elem1.bounding_box()
        bbox2 = elem2.bounding_box()

        if bbox1 is None or bbox2 is None:
            inkex.errormsg("Could not calculate bounding box for selected objects.")
            return

        # Calculate coordinates for selected reference points
        x1, y1 = self.get_anchor_point(bbox1)
        x2, y2 = self.get_anchor_point(bbox2)

        # Difference vector
        dx = x2 - x1
        dy = y2 - y1

        # Apply global translation transforms
        elem1.transform = Transform(f"translate({dx}, {dy})") @ elem1.transform
        elem2.transform = Transform(f"translate({-dx}, {-dy})") @ elem2.transform

if __name__ == '__main__':
    SwapLocations().run()