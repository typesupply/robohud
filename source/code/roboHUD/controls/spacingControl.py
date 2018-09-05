from AppKit import NSImage, NSAffineTransform, NSBezierPath,\
    NSLeftTextAlignment, NSRightTextAlignment, NSCenterTextAlignment,\
    NSFocusRingTypeNone
import vanilla
from mojo.roboFont import CurrentGlyph
from mojo import events
from roboHUD import RoboHUDController, BaseRoboHUDControl

def drawLeftArrow(foregroundColor, backgroundColor):
    return _drawArrow(foregroundColor, backgroundColor)

def drawRightArrow(foregroundColor, backgroundColor):
    return _drawArrow(foregroundColor, backgroundColor, flip=True)

def _drawArrow(foregroundColor, backgroundColor, flip=False):
    image = NSImage.alloc().initWithSize_((30, 19))
    image.lockFocus()
    foregroundColor.set()
    if flip:
        transform = NSAffineTransform.transform()
        transform.scaleXBy_yBy_(-1, 1)
        transform.translateXBy_yBy_(-30, 0)
        transform.concat()
    path = NSBezierPath.bezierPath()
    path.moveToPoint_((5, 11))
    path.lineToPoint_((25, 11))
    path.moveToPoint_((10, 6))
    path.lineToPoint_((5, 11))
    path.lineToPoint_((10, 16))
    path.setLineWidth_(1.0)
    path.stroke()
    image.unlockFocus()
    return image


class SpacingHUDControl(BaseRoboHUDControl):

    name = "Spacing Editor"
    size = (320, 20)
    dimWhenInactive = False

    def start(self):
        super(SpacingHUDControl, self).start()
        events.addObserver(self, "currentGlyphChangedCallback", "currentGlyphChanged")
        self.glyph = None

        foregroundColor = RoboHUDController().getForegroundColor()
        backgroundColor = RoboHUDController().getBackgroundColor()

        self.view.leftEditText = vanilla.EditText(
            (0, 0, 40, 19),
            "",
            callback=self.leftEditTextCallback,
            continuous=False,
            sizeStyle="small"
        )
        self.view.widthEditText = vanilla.EditText(
            (70, 0, 40, 19),
            "",
            callback=self.widthEditTextCallback,
            continuous=False,
            sizeStyle="small"
        )
        self.view.rightEditText = vanilla.EditText(
            (140, 0, 40, 19),
            "",
            callback=self.rightEditTextCallback,
            continuous=False,
            sizeStyle="small"
        )
        self.view.leftIcon = vanilla.ImageButton(
            (40, 0, 30, 19),
            imageObject=drawLeftArrow(foregroundColor, backgroundColor),
            bordered=False
        )
        self.view.rightIcon = vanilla.ImageButton(
            (110, 0, 30, 19),
            imageObject=drawRightArrow(foregroundColor, backgroundColor),
            bordered=False
        )

        controls = [
            (self.view.widthEditText, NSCenterTextAlignment),
            (self.view.leftEditText, NSRightTextAlignment),
            (self.view.rightEditText, NSLeftTextAlignment)
        ]
        for control, alignment in controls:
            textField = control.getNSTextField()
            textField.setBordered_(False)
            textField.setTextColor_(foregroundColor)
            textField.setBackgroundColor_(backgroundColor)
            textField.setFocusRingType_(NSFocusRingTypeNone)
            textField.setAlignment_(alignment)
        controls = [
            self.view.leftEditText,
            self.view.rightEditText
        ]
        for index, control in enumerate(controls):
            next = index + 1
            if next == len(controls):
                next = 0
            next = controls[next].getNSTextField()
            control.getNSTextField().setNextKeyView_(next)

    def stop(self):
        super(SpacingHUDControl, self).stop()
        events.removeObserver(self, "currentGlyphChanged")
        self._stopObservingGlyph()

    def currentGlyphChangedCallback(self, info):
        self._stopObservingGlyph()
        self._beginObservingGlyph()
        self.populateControls()

    def glyphChangedChangedCallback(self, info):
        self.populateControls()

    def _beginObservingGlyph(self):
        glyph = CurrentGlyph()
        if glyph is not None:
            glyph.addObserver(self, "glyphChangedChangedCallback", "Glyph.Changed")
        self.glyph = glyph

    def _stopObservingGlyph(self):
        if self.glyph is not None:
            self.glyph.removeObserver(self, "Glyph.Changed")

    def populateControls(self):
        glyph = self.glyph
        width = left = right = ""
        if glyph is not None:
            width = str(glyph.width)
            if len(glyph) or len(glyph.components): # XXX RF < 3.2 fix
                left = glyph.leftMargin
                if left is None:
                    left = ""
                else:
                    left = str(left)
                right = glyph.rightMargin
                if right is None:
                    right = ""
                else:
                    right = str(glyph.rightMargin)
        self.view.widthEditText.set(width)
        self.view.leftEditText.set(left)
        self.view.rightEditText.set(right)

    # ---------
    # Callbacks
    # ---------

    def _setValue(self, field, attr):
        glyph = self.glyph
        if glyph is None:
            return
        font = glyph.font
        value = field.get().strip()
        # glyph name
        if value.startswith("="):
            value = value[1:].strip()
            if not value:
                return
        # number
        else:
            try:
                value = int(value)
            except:
                return
        if isinstance(value, str):
            if value not in font:
                return
            value = getattr(font[value], attr)
        glyph.prepareUndo("Spacing Change")
        setattr(glyph, attr, value)
        glyph.performUndo()

    def widthEditTextCallback(self, sender):
        self._setValue(sender, "width")

    def leftEditTextCallback(self, sender):
        self._setValue(sender, "leftMargin")

    def rightEditTextCallback(self, sender):
        self._setValue(sender, "rightMargin")
