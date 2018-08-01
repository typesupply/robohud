from AppKit import NSView, CALayer
import vanilla
from mojo import events


class BaseRoboHUDControl(object):

    name = "Base Control"
    size = (100, 100)
    view = None
    dimWhenInactive = False

    def __init__(self):
        if self.dimWhenInactive:
            cls = RoboHUDDimmableGroup
        else:
            cls = vanilla.Group
        self.view = cls((0, 0, self.size[0], self.size[1]))

    def start(self):
        events.addObserver(self, "_drawNotificationCallback", "draw")
        events.addObserver(self, "_drawPreviewNotificationCallback", "drawPreview")

    def stop(self):
        events.removeObserver(self, "draw")
        events.removeObserver(self, "drawPreview")

    def _setInactiveOpacity(self, value):
        if isinstance(self.view, RoboHUDDimmableGroup):
            self.view.getNSView().setInactiveOpacity_(value)

    def _drawNotificationCallback(self, info):
        self.view.show(True)

    def _drawPreviewNotificationCallback(self, info):
        self.view.show(False)


# -------------
# Dimmable View
# -------------

class RoboHUDDimmableView(NSView):

    def init(self):
        self = super(RoboHUDDimmableView, self).init()
        self.fadeLayer = CALayer.layer()
        self._activeOpacity = 1.0
        self._inactiveOpacity = 0.2
        self.fadeLayer.setOpacity_(self._activeOpacity)
        self.setLayer_(self.fadeLayer)
        self.setWantsLayer_(True)
        return self

    def _setOpacity_(self, value):
        self.fadeLayer.setOpacity_(value)

    def setInactiveOpacity_(self, value):
        self._inactiveOpacity = value
        self._setOpacity_(value)

    def acceptsFirstResponder(self):
        return True

    def mouseEntered_(self, event):
        self._setOpacity_(self._activeOpacity)

    def mouseExited_(self, event):
        self._setOpacity_(self._inactiveOpacity)

    def updateTrackingAreas(self):
        self.removeTrackingRect_(self._trackingTag)
        b = self.bounds()
        self.addTrackingRect_owner_userData_assumeInside_(b, self, None, True)

    def viewDidMoveToWindow(self):
        b = self.bounds()
        self._trackingTag = self.addTrackingRect_owner_userData_assumeInside_(b, self, None, True)
        self._setOpacity_(self._inactiveOpacity)

        if hasattr(self, "vanillaWrapper"):
            wrapper = self.vanillaWrapper()
            if hasattr(wrapper, "subscribeToWindow"):
                wrapper.subscribeToWindow()


class RoboHUDDimmableGroup(vanilla.Group):

    nsViewClass = RoboHUDDimmableView
