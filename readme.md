# RoboHUD

This extension allows users to add custom controls *within* the glyph editor in RoboFont. The extension comes preloaded with three controls:

- Glyph Name and Character: a basic glyph name and character display.
- Spacing Editor: basic text fields for editing left margin, right margin and width.
- Align Selection: a fancy set of controls for aligning and distributing selected points and contours.

Open the settings with the "Edit Settings…" menu item and set the controls you want. There are nine slots. Hopefully that will be enough. If not, I'll add more.

## Developing HUD Controls

Sooooooooooo, you want to add your own control? Good. That's what I was hoping for. Here's what you do.

### Building your controls.

The controls are built with vanilla and anything that is compatible with vanilla (mojo.canvas, custom views, etc.). Anything you can put in a vanilla window can put into a control. Here's what you need to do:

```python
from roboHUD import BaseRoboHUDControl

# Subclass the base control. It implements some important
# stuff behind the scenes. 
class DemoHUDControl(BaseRoboHUDControl):

    # Each control needs a unique name. This name will be shown
    # to users and will be used in stored preferences, so make
    # it something nice.
    name = "Demo Control"

    # Each control needs to declare how big it is.
    size = (100, 17)

    # If you want your control to reduce in opacity when the
    # cursor is not over the control, set this to True. The
    # default is False.
    dimWhenInactive = False

    def start(self):
        """
        This method will be called before the control is to
        be added to the glyph editor. Use it to build your
        interface, start subscriptions, etc. All interface
        needs to be vanilla compatible objects assigned to
        self.view. This, self.view, is an instance of
        vanilla.Group.

        Implementing this method is optional, but if you do:
        ALWAYS CALL THE SUPERCLASS.
        """
        super(DemoHUDControl, self).start()
        self.view.textBox = vanilla.TextBox((0, 0, 0, 17), "Hello!")

    def stop(self):
        """
        This method will be called when the control is being
        removed from the glyph editor. Use this to unsubscribe
        from events, release any held data, etc. if you need to.

        Implementing this method is optional, but if you do:
        ALWAYS CALL THE SUPERCLASS.
        """
        super(DemoHUDControl, self).stop()
        self.view.textBox.set("Bye.")
```

A good way to build this without going through the rigamarole of interacting with RoboHUD's interface is to create a vanilla.Window, add a vanilla.Group named self.view and implement everything with that until it works. Then, switch to the control subclass, remove the window code and you'll be pretty close to done.

### Telling RoboHUD about your control.

Once you have your control ready, you need to register it with RoboHUD. You do that like this:

```python
from roboHUD import registerControlClass

registerControlClass(DemoHUDControl)
```

The name for your control will appear in the settings for the user to select. You'll need to have this execute as a startup script in an extension or something like that so that the declaration happens automatically.

_"Have a control in an extension!?"_ Yeah! Extensions that have their own UI can make the UI or other UI available as HUD controls!

### Keeping it copacetic.

The reason I made this is that I hate visual noise. If you are interested in this extension, you probably do too. So, how will controls from lots of developers not become a mess? I don't know, but I've given you two things to help:

```python
from roboHUD import RoboHUDController

foregroundColor = RoboHUDController().getForegroundColor()
backgroundColor = RoboHUDController().getBackgroundColor()
```

The main UI design goal is: Keep it simple.

## To Do:
- align selection needs to move contiguous selection within a contour as a group. maybe this should be handled with the option key + click or something like that.
- allow color customization in the settings editor.
- allow inactivity opacity customization in the settings editor.
- handle color changes in already displayed controls.