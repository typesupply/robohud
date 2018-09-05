import weakref
from AppKit import NSViewMinXMargin, NSViewMaxXMargin, NSViewMinYMargin, NSViewMaxYMargin, NSColor
from mojo import events
from mojo.UI import AllGlyphWindows
from mojo import extensions

defaultStub = "com.typesupply.RoboHUD."

defaults = {
    defaultStub + "margin" : 40,
    defaultStub + "positions" : {},
    defaultStub + "foregroundColor" : (0.3, 0.3, 0.3, 0.5),
    defaultStub + "backgroundColor" : (1.0, 1.0, 1.0, 0.2),
    defaultStub + "inactiveOpacity" : (0.4)
}

class _RoboHUDController(object):

    def __init__(self):
        extensions.registerExtensionDefaults(defaults)
        self._active = True
        self._classes = {}
        self._positions = {}
        self._displayed = {}
        self._margin = None
        self._foregroundColor = None
        self._backgroundColor = None
        self._inactiveOpacity = None
        self._loadDefaults()
        events.addObserver(self, "_glyphWindowWillCloseCallback", "glyphWindowWillClose")
        events.addObserver(self, "_glyphWindowWillOpenCallback", "glyphWindowWillOpen")
        self.addControlsToExistingWindows()

    # --------
    # Defaults
    # --------

    def _writeDefaults(self):
        extensions.setExtensionDefault(defaultStub + "margin", self._margin)
        extensions.setExtensionDefault(defaultStub + "inactiveOpacity", self._inactiveOpacity)
        positions = {}
        for position, name in self._positions.items():
            position = " ".join(position)
            positions[position] = name
        extensions.setExtensionDefault(defaultStub + "positions", positions)

    def _loadDefaults(self):
        self._positions = {}
        positions = extensions.getExtensionDefault(defaultStub + "positions")
        for position, name in positions.items():
            position = tuple(position.split(" "))
            self._positions[position] = name
        self._margin = extensions.getExtensionDefault(defaultStub + "margin")
        self._inactiveOpacity = extensions.getExtensionDefault(defaultStub + "inactiveOpacity")
        r, g, b, a = extensions.getExtensionDefault(defaultStub + "foregroundColor")
        self._foregroundColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, a)
        r, g, b, a = extensions.getExtensionDefault(defaultStub + "backgroundColor")
        self._backgroundColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, a)

    # -------------
    # Notifications
    # -------------

    def _glyphWindowWillOpenCallback(self, info):
        window = info["window"]
        self.addControlsToWindow(window)

    def _glyphWindowWillCloseCallback(self, info):
        window = info["window"]
        self.removeControlsFromWindow(window)

    # -----------
    # Positioning
    # -----------

    def addControlsToExistingWindows(self):
        if not self._active:
            return
        existingWindows = AllGlyphWindows()
        if existingWindows:
            for window in existingWindows:
                self.addControlsToWindow(window)

    def addControlsToWindow(self, window):
        if not self._active:
            return
        windowRef = weakref.ref(window)
        self._displayed[windowRef] = {}
        for position, name in self._positions.items():
            if name not in self._classes:
                continue
            self._addControlToWindow(windowRef, position, name)
        self._positionViewsInWindow(windowRef)

    def _addControlToWindow(self, windowRef, position, name):
        if not self._active:
            return
        window = windowRef()
        cls = self._classes[name]
        control = cls()
        control._window = windowRef
        control.start()
        window.addGlyphEditorSubview(control.view)
        self._displayed[windowRef][position] = control

    def removeControlsFromExistingWindows(self):
        for position in self._positions.keys():
            for windowRef in self._displayed.keys():
                self._removeControlFromWindow(windowRef, position)
        self._displayed = {}

    def removeControlsFromWindow(self, window):
        windowRef = weakref.ref(window)
        for position in self._positions.keys():
            self._removeControlFromWindow(windowRef, position)

    def _removeControlFromWindow(self, windowRef, position):
        window = windowRef()
        if position in self._displayed[windowRef]:
            control = self._displayed[windowRef][position]
            window.removeGlyphEditorSubview(control.view)
            control.stop()
            del self._displayed[windowRef][position]

    def updateControlPositions(self):
        if not self._active:
            return
        for windowRef in self._displayed.keys():
            self._positionViewsInWindow(windowRef)

    def _positionViewsInWindow(self, windowRef):
        if not self._active:
            return
        window = windowRef()
        editorView = window.editGlyphView.enclosingScrollView().superview()
        editorFrame = editorView.frame()
        editorWidth, editorHeight = editorFrame.size
        for position, control in self._displayed[windowRef].items():
            viewWidth, viewHeight = control.size
            xPosition, yPosition = position
            mask = 0
            if xPosition == "left":
                x = self._margin
                mask |= NSViewMaxXMargin
            elif xPosition == "right":
                x = editorWidth - viewWidth - self._margin
                mask |= NSViewMinXMargin
            else:
                x = int((editorWidth - viewWidth) / 2)
                mask |= NSViewMinXMargin | NSViewMaxXMargin
            if yPosition == "bottom":
                y = editorHeight - viewHeight - self._margin
                mask |= NSViewMaxYMargin
            elif yPosition == "top":
                y = self._margin
                mask |= NSViewMinYMargin
            else:
                y = int((editorHeight - viewHeight) / 2)
                mask |= NSViewMinYMargin | NSViewMaxYMargin
            control.view.setPosSize((x, y, viewWidth, viewHeight))
            control.view._nsObject.setAutoresizingMask_(mask)

    # -------------------
    # Activate/Deactivate
    # -------------------

    def toggleVisibility(self):
        if self._active:
            self._active = False
            self.removeControlsFromExistingWindows()
        else:
            self._active = True
            self.addControlsToExistingWindows()

    # ------------
    # Settings API
    # ------------

    def _tellControlsToReloadDefaults(self):
        for windowRef, positions in self._displayed.items():
            for position, control in positions.items():
                control._reloadDisplaySettings()

    def getForegroundColor(self):
        return self._foregroundColor

    def getBackgroundColor(self):
        return self._backgroundColor

    def getMargin(self):
        return self._margin

    def setMargin(self, value):
        self._margin = value
        self.updateControlPositions()
        self._writeDefaults()

    def getInactiveOpacity(self):
        return self._inactiveOpacity

    def setInactiveOpacity(self, value):
        self._inactiveOpacity = value
        self._writeDefaults()
        self._tellControlsToReloadDefaults()

    def getAvailableControlNames(self):
        return sorted(self._classes.keys())

    def getControlPositions(self):
        positions = {}
        for position, name in self._positions.items():
            if name not in self._classes:
                continue
            positions[position] = name
        return positions

    def registerControlClass(self, cls):
        self._classes[cls.name] = cls

    def setControlForPosition(self, position, name):
        if position in self._positions:
            for windowRef in self._displayed.keys():
                self._removeControlFromWindow(windowRef, position)
            del self._positions[position]
        if name is not None:
            self._positions[position] = name
            for windowRef in self._displayed.keys():
                self._addControlToWindow(windowRef, position, name)
            self.updateControlPositions()
        self._writeDefaults()
