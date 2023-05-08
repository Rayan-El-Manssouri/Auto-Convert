from pdfminer.layout import (
    LTCurve,
    LTLine,
    LTRect,
    LTFigure,
)

def calculate_border_radius(element, scale_factor=0.1):
    if isinstance(element, (LTCurve, LTFigure, LTRect, LTLine)):
        if isinstance(element, LTCurve):
            if hasattr(element, "cap_style"):
                cap_style = element.cap_style
            else:
                cap_style = None

            if cap_style == 1:
                return element.linewidth * scale_factor
            elif cap_style == 2:
                return element.linewidth * 0.5
            else:
                return 0
        elif isinstance(element, LTLine):
            return element.linewidth * scale_factor
        else:
            return element.linewidth * scale_factor
    else:
        return 0
