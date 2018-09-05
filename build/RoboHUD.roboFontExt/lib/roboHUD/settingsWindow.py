import vanilla
from roboHUD import RoboHUDController

class RoboHUDSettingsWindowController(object):

    def __init__(self):
        self.controller = RoboHUDController()
        self.classNames = ["None"] + self.controller.getAvailableControlNames()

        self.w = vanilla.Window((400, 370), "RoboHUD Settings")

        self.w.marginTitle = vanilla.TextBox(
            (15, 15, 100, 17),
            "Margin:",
            alignment="right"
        )
        self.w.marginSlider = vanilla.Slider(
            (120, 20, -15, 23),
            value=self.controller.getMargin(),
            minValue=0,
            maxValue=200,
            tickMarkCount=41,
            stopOnTickMarks=True,
            callback=self.marginSliderCallback
        )

        self.w.inactiveOpacityTitle = vanilla.TextBox(
            (15, 45, 100, 17),
            "Dim Level:",
            alignment="right"
        )
        self.w.inactiveOpacitySlider = vanilla.Slider(
            (120, 50, -15, 23),
            value=self.controller.getMargin(),
            minValue=0,
            maxValue=1.0,
            tickMarkCount=11,
            stopOnTickMarks=False,
            callback=self.inactiveOpacitySliderCallback
        )

        positions = [
            ("left", "top"),
            ("center", "top"),
            ("right", "top"),
            ("left", "center"),
            ("center", "center"),
            ("right", "center"),
            ("left", "bottom"),
            ("center", "bottom"),
            ("right", "bottom")
        ]
        defined = self.controller.getControlPositions()

        top = 90
        for position in positions:
            index = 0
            if position in defined:
                index = self.classNames.index(defined[position])
            title = " ".join(position).title() + ":"
            tag = "".join(position)
            attr = "%sTitle" % tag
            tb = vanilla.TextBox((15, top, 100, 17), title, alignment="right")
            setattr(self.w, attr, tb)
            attr = "%sPopUpButton" % tag
            pb = vanilla.PopUpButton((120, top, -15, 17), self.classNames, callback=self.positionPopUpButtonCallback)
            pb.positionName = position
            pb.set(index)
            setattr(self.w, attr, pb)
            top += 30

        self.w.open()

    def marginSliderCallback(self, sender):
        value = sender.get()
        self.controller.setMargin(value)

    def inactiveOpacitySliderCallback(self, sender):
        value = sender.get()
        self.controller.setInactiveOpacity(value)

    def positionPopUpButtonCallback(self, sender):
        position = sender.positionName
        index = sender.get()
        name = self.classNames[index]
        if name == "None":
            name = None
        self.controller.setControlForPosition(position, name)
