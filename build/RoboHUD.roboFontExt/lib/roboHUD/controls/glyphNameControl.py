from AppKit import NSFont
import vanilla
from mojo import events
from roboHUD import RoboHUDController, BaseRoboHUDControl

class GlyphNameHUDControl(BaseRoboHUDControl):

    name = "Glyph Name and Character"
    size = (300, 30)

    def start(self):
        super(GlyphNameHUDControl, self).start()
        events.addObserver(self, "currentGlyphChangedCallback", "currentGlyphChanged")
        self.view.textBox = vanilla.TextBox((0, 0, 0, 0), "")
        textField = self.view.textBox.getNSTextField()
        font = NSFont.systemFontOfSize_(20)
        textField.setFont_(font)
        textField.setTextColor_(RoboHUDController().getForegroundColor())

    def stop(self):
        super(GlyphNameHUDControl, self).stop()
        events.removeObserver(self, "currentGlyphChanged")

    def currentGlyphChangedCallback(self, info):
        text = ""
        glyph = info["glyph"]
        if glyph is not None:
            name = glyph.name
            text = name
            uni = glyph.font.naked().unicodeData.pseudoUnicodeForGlyphName(name)
            if uni is not None:
                c = chr(uni)
                if c != name:
                    text += " | " + c
        self.view.textBox.set(text)
