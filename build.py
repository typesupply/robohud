import os
from mojo.extensions import ExtensionBundle

name = "RoboHUD"
version = "0.1a"
developer = "Type Supply"
developerURL = "http://typesupply.com"
roboFontVersion = "3.1"
pycOnly = False
menuItems = [
    dict(
        path="menu_toggleVisibility.py",
        preferredName="Toggle Visibility",
        shortKey=""
    ),
    dict(
        path="menu_showSettings.py",
        preferredName="Edit Settings…",
        shortKey=""
    )
]


basePath = os.path.dirname(__file__)
sourcePath = os.path.join(basePath, "source")
libPath = os.path.join(sourcePath, "code")
licensePath = os.path.join(basePath, "license.txt")
extensionFile = "%s.roboFontExt" % name
buildPath = os.path.join(basePath, "build")
extensionPath = os.path.join(buildPath, extensionFile)

B = ExtensionBundle()
B.name = name
B.developer = developer
B.developerURL = developerURL
B.version = version
B.launchAtStartUp = True
B.mainScript = "main.py"
B.html = os.path.exists(os.path.join(sourcePath, "documentation", "index.html"))
B.requiresVersionMajor = roboFontVersion.split(".")[0]
B.requiresVersionMinor = roboFontVersion.split(".")[1]
B.addToMenu = menuItems
with open(licensePath) as license:
    B.license = license.read()


print("building extension...", end=" ")
v = B.save(extensionPath, libPath=libPath, pycOnly=pycOnly)
print("done!")
print()
print(B.validationErrors())