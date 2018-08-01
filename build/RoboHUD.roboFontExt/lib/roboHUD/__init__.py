from AppKit import NSApp
from .control import BaseRoboHUDControl

def RoboHUDController():
    return NSApp().RoboHUD

def registerControlClass(cls):
    RoboHUDController().registerControlClass(cls)
