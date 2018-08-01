from AppKit import NSCenterTextAlignment, NSFocusRingTypeNone
import vanilla
from mojo.roboFont import CurrentGlyph
from mojo import events
from roboHUD import RoboHUDController, BaseRoboHUDControl


class SpacingHUDControl(BaseRoboHUDControl):

    name = "Spacing Editor"
    size = (320, 20)
    dimWhenInactive = True

    def start(self):
        super(SpacingHUDControl, self).start()
        self.glyph = None
        events.addObserver(self, "currentGlyphChangedCallback", "currentGlyphChanged")
        self.view.leftEditText = vanilla.EditText((0, 0, 100, 19), "", callback=self.leftEditTextCallback, sizeStyle="small")
        self.view.rightEditText = vanilla.EditText((110, 0, 100, 19), "", callback=self.rightEditTextCallback, sizeStyle="small")
        self.view.widthEditText = vanilla.EditText((220, 0, 100, 19), "", callback=self.widthEditTextCallback, sizeStyle="small")

        foregroundColor = RoboHUDController().getForegroundColor()
        backgroundColor = RoboHUDController().getBackgroundColor()
        controls = [
            self.view.widthEditText,
            self.view.leftEditText,
            self.view.rightEditText
        ]
        for control in controls:
            textField = control.getNSTextField()
            textField.setBordered_(False)
            textField.setTextColor_(foregroundColor)
            textField.setBackgroundColor_(backgroundColor)
            textField.setAlignment_(NSCenterTextAlignment)
            textField.setFocusRingType_(NSFocusRingTypeNone)
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
            left = str(glyph.leftMargin)
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
