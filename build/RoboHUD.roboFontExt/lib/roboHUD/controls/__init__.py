from roboHUD import registerControlClass
from .glyphNameControl import GlyphNameHUDControl
from .alignControl import AlignSelectionHUDControl
from .spacingControl import SpacingHUDControl

def registerStockControls():
    registerControlClass(GlyphNameHUDControl)
    registerControlClass(AlignSelectionHUDControl)
    registerControlClass(SpacingHUDControl)
