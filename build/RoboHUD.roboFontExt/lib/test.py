import vanilla
from roboHUD import RoboHUDController, BaseRoboHUDControl, registerControlClass

class TestControl(BaseRoboHUDControl):

    size = (100, 100)

    def start(self):
        super(TestControl, self).start()
        self.view.b = vanilla.SquareButton((0, 0, 0, 0), self.text)


class LTControl(TestControl):
    name = "LT"
    text = "LT"
registerControlClass(LTControl)
RoboHUDController().setControlForPosition(("left", "top"), "LT")

class LCControl(TestControl):
    name = "LC"
    text = "LC"
registerControlClass(LCControl)
RoboHUDController().setControlForPosition(("left", "center"), "LC")

class LBControl(TestControl):
    name = "LB"
    text = "LB"
registerControlClass(LBControl)
RoboHUDController().setControlForPosition(("left", "bottom"), "LB")

class CTControl(TestControl):
    name = "CT"
    text = "CT"
registerControlClass(CTControl)
RoboHUDController().setControlForPosition(("center", "top"), "CT")

class CCControl(TestControl):
    name = "CC"
    text = "CC"
registerControlClass(CCControl)
RoboHUDController().setControlForPosition(("center", "center"), "CC")

class CBControl(TestControl):
    name = "CB"
    text = "CB"
registerControlClass(CBControl)
RoboHUDController().setControlForPosition(("center", "bottom"), "CB")

class RTControl(TestControl):
    name = "RT"
    text = "RT"
registerControlClass(RTControl)
RoboHUDController().setControlForPosition(("right", "top"), "RT")

class RCControl(TestControl):
    name = "RC"
    text = "RC"
registerControlClass(RCControl)
RoboHUDController().setControlForPosition(("right", "center"), "RC")

class RBControl(TestControl):
    name = "RB"
    text = "RB"
registerControlClass(RBControl)
RoboHUDController().setControlForPosition(("right", "bottom"), "RB")