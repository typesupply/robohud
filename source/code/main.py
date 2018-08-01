from AppKit import NSApp
from roboHUD.controller import _RoboHUDController
from roboHUD.controls import registerStockControls

if __name__ == "__main__":
    NSApp().RoboHUD = _RoboHUDController()
    registerStockControls()
