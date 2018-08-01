from fontTools.misc.arrayTools import unionRect, rectCenter
from AppKit import NSImage, NSRectFillUsingOperation, NSCompositeSourceOver, NSBezierPath, NSColor
import vanilla
from mojo.roboFont import CurrentGlyph
from mojo.UI import UpdateCurrentGlyphView
from roboHUD import RoboHUDController, BaseRoboHUDControl


class AlignSelectionHUDControl(BaseRoboHUDControl):

    name = "Align Selection"
    size = (70, 120)
    dimWhenInactive = True

    def start(self):
        self.view.yt = vanilla.ImageButton((0, 0, 19, 19), bordered=False, callback=self.alignTop)
        self.view.yc = vanilla.ImageButton((25, 0, 19, 19), bordered=False, callback=self.alignYCenter)
        self.view.yb = vanilla.ImageButton((50, 0, 19, 19), bordered=False, callback=self.alignBottom)
        self.view.xl = vanilla.ImageButton((0, 25, 19, 19), bordered=False, callback=self.alignLeft)
        self.view.xc = vanilla.ImageButton((25, 25, 19, 19), bordered=False, callback=self.alignXCenter)
        self.view.xr = vanilla.ImageButton((50, 25, 19, 19), bordered=False, callback=self.alignRight)
        self.view.cc = vanilla.ImageButton((0, 50, 19, 19), bordered=False, callback=self.alignCenterCenter)
        self.view.dx = vanilla.ImageButton((25, 50, 19, 19), bordered=False, callback=self.distributeXSpacing)
        self.view.dy = vanilla.ImageButton((50, 50, 19, 19), bordered=False, callback=self.distributeYSpacing)
        self.view.dt = vanilla.ImageButton((0, 75, 19, 19), bordered=False, callback=self.distributeTop)
        self.view.dyc = vanilla.ImageButton((25, 75, 19, 19), bordered=False, callback=self.distributeYCenter)
        self.view.db = vanilla.ImageButton((50, 75, 19, 19), bordered=False, callback=self.distributeBottom)
        self.view.dl = vanilla.ImageButton((0, 100, 19, 19), bordered=False, callback=self.distributeLeft)
        self.view.dxc = vanilla.ImageButton((25, 100, 19, 19), bordered=False, callback=self.distributeXCenter)
        self.view.dr = vanilla.ImageButton((50, 100, 19, 19), bordered=False, callback=self.distributeRight)
        self.setImagesInButtons()

    def setImagesInButtons(self):
        images = makeImages()
        self.view.yt.setImage(imageObject=images["YT"])
        self.view.yc.setImage(imageObject=images["YC"])
        self.view.yb.setImage(imageObject=images["YB"])
        self.view.xl.setImage(imageObject=images["XL"])
        self.view.xc.setImage(imageObject=images["XC"])
        self.view.xr.setImage(imageObject=images["XR"])
        self.view.cc.setImage(imageObject=images["CC"])
        self.view.dx.setImage(imageObject=images["DX"])
        self.view.dy.setImage(imageObject=images["DY"])
        self.view.dt.setImage(imageObject=images["DT"])
        self.view.dyc.setImage(imageObject=images["DYC"])
        self.view.db.setImage(imageObject=images["DB"])
        self.view.dl.setImage(imageObject=images["DL"])
        self.view.dxc.setImage(imageObject=images["DXC"])
        self.view.dr.setImage(imageObject=images["DR"])

    # -----
    # Align
    # -----

    def alignBottom(self, sender):
        self._align([self._alignBottom], "Align Bottom")

    def alignYCenter(self, sender):
        self._align([self._alignYCenter], "Align Y Center")

    def alignTop(self, sender):
        self._align([self._alignTop], "Align Top")

    def alignLeft(self, sender):
        self._align([self._alignLeft], "Align Left")

    def alignXCenter(self, sender):
        self._align([self._alignXCenter], "Align X Center")

    def alignRight(self, sender):
        self._align([self._alignRight], "Align Right")

    def alignCenterCenter(self, sender):
        self._align([self._alignYCenter, self._alignXCenter], "Align Center Center")

    def _align(self, methods, title):
        glyph = CurrentGlyph()
        if glyph is None:
            return
        rects, selectedContours, selectedBPoints = getSelectionData(glyph)
        if len(rects) < 2:
            return
        glyph.prepareUndo(title)
        for method in methods:
            method(rects, selectedContours, selectedBPoints)
        for bPoint in selectedBPoints:
            bPoint.round()
        for contour in selectedContours:
            contour.round()
        glyph.performUndo()
        UpdateCurrentGlyphView()

    def _alignTop(self, rects, selectedContours, selectedBPoints):
        top = getEdgeCoordinate(rects, 3, max)
        for bPoint in selectedBPoints:
            d = top - bPoint.anchor[1]
            bPoint.move((0, d))
        for contour in selectedContours:
            d = top - contour.bounds[3]
            contour.move((0, d))

    def _alignBottom(self, rects, selectedContours, selectedBPoints):
        bottom = getEdgeCoordinate(rects, 1, min)
        for bPoint in selectedBPoints:
            d = bottom - bPoint.anchor[1]
            bPoint.move((0, d))
        for contour in selectedContours:
            d = bottom - contour.bounds[1]
            contour.move((0, d))

    def _alignYCenter(self, rects, selectedContours, selectedBPoints):
        y1 = getEdgeCoordinate(rects, 1, min)
        y2 = getEdgeCoordinate(rects, 3, max)
        center = (y1 + y2) / 2
        for bPoint in selectedBPoints:
            d = center - bPoint.anchor[1]
            bPoint.move((0, d))
        for contour in selectedContours:
            d = center - rectCenter(contour.bounds)[1]
            contour.move((0, d))

    def _alignLeft(self, rects, selectedContours, selectedBPoints):
        left = getEdgeCoordinate(rects, 0, min)
        for bPoint in selectedBPoints:
            d = left - bPoint.anchor[0]
            bPoint.move((d, 0))
        for contour in selectedContours:
            d = left - contour.bounds[0]
            contour.move((d, 0))

    def _alignRight(self, rects, selectedContours, selectedBPoints):
        right = getEdgeCoordinate(rects, 2, max)
        for bPoint in selectedBPoints:
            d = right - bPoint.anchor[0]
            bPoint.move((d, 0))
        for contour in selectedContours:
            d = right - contour.bounds[2]
            contour.move((d, 0))

    def _alignXCenter(self, rects, selectedContours, selectedBPoints):
        x1 = getEdgeCoordinate(rects, 0, min)
        x2 = getEdgeCoordinate(rects, 2, max)
        center = (x1 + x2) / 2
        for bPoint in selectedBPoints:
            d = center - bPoint.anchor[0]
            bPoint.move((d, 0))
        for contour in selectedContours:
            d = center - rectCenter(contour.bounds)[0]
            contour.move((d, 0))

    # ----------
    # Distribute
    # ----------

    def distributeBottom(self, sender):
        self._distribute([self._distributeBottom], "Distribute Bottom")

    def distributeYCenter(self, sender):
        self._distribute([self._distributeYCenter], "Distribute Y Center")

    def distributeTop(self, sender):
        self._distribute([self._distributeTop], "Distribute Top")

    def distributeLeft(self, sender):
        self._distribute([self._distributeLeft], "Distribute Left")

    def distributeXCenter(self, sender):
        self._distribute([self._distributeXCenter], "Distribute X Center")

    def distributeRight(self, sender):
        self._distribute([self._distributeRight], "Distribute Right")

    def _distribute(self, methods, title):
        glyph = CurrentGlyph()
        if glyph is None:
            return
        rects, selectedContours, selectedBPoints = getSelectionData(glyph)
        if len(rects) < 3:
            return
        glyph.prepareUndo(title)
        for method in methods:
            method(rects, selectedContours, selectedBPoints)
        for bPoint in selectedBPoints:
            bPoint.round()
        for contour in selectedContours:
            contour.round()
        glyph.performUndo()
        UpdateCurrentGlyphView()

    def _distributeTop(self, rects, selectedContours, selectedBPoints):
        self._distributeEdge(1, rects, selectedContours, selectedBPoints)

    def _distributeBottom(self, rects, selectedContours, selectedBPoints):
        self._distributeEdge(3, rects, selectedContours, selectedBPoints)

    def _distributeYCenter(self, rects, selectedContours, selectedBPoints):
        self._distributeCenter(1, rects, selectedContours, selectedBPoints)

    def _distributeLeft(self, rects, selectedContours, selectedBPoints):
        self._distributeEdge(0, rects, selectedContours, selectedBPoints)

    def _distributeRight(self, rects, selectedContours, selectedBPoints):
        self._distributeEdge(2, rects, selectedContours, selectedBPoints)

    def _distributeXCenter(self, rects, selectedContours, selectedBPoints):
        self._distributeCenter(0, rects, selectedContours, selectedBPoints)

    def _distributeEdge(self, index, rects, selectedContours, selectedBPoints):
        edge1 = getEdgeCoordinate(rects, index, min)
        edge2 = getEdgeCoordinate(rects, index, max)
        space = edge2 - edge1
        if space:
            ordered = [(bPoint.anchor[index % 2], bPoint.anchor, bPoint) for bPoint in selectedBPoints]
            ordered += [(contour.bounds[index], contour.bounds, contour) for contour in selectedContours]
            ordered.sort()
            interval = space / (len(ordered) - 1)
            for i, (pos, disambiguate, obj) in enumerate(ordered):
                e = edge1 + (i * interval)
                d = e - pos
                if index in (0, 2):
                    obj.move((d, 0))
                else:
                    obj.move((0, d))

    def _distributeCenter(self, index, rects, selectedContours, selectedBPoints):
        ordered = [(bPoint.anchor[index], (bPoint.anchor[0], bPoint.anchor[1], bPoint.anchor[0], bPoint.anchor[1]), bPoint) for bPoint in selectedBPoints]
        ordered += [(contour.bounds[index], contour.bounds, contour) for contour in selectedContours]
        ordered.sort()
        side1 = ordered[0]
        side2 = ordered[-1]
        center1 = rectCenter(side1[1])[index]
        center2 = rectCenter(side2[1])[index]
        space = center2 - center1
        if not space:
            return
        step = space / (len(ordered) - 1)
        prev = center1
        for pos, bounds, obj in ordered[1:-1]:
            alignTo = prev + step
            d = alignTo - rectCenter(bounds)[index]
            if index == 0:
                obj.move((d, 0))
            else:
                obj.move((0, d))
            prev = alignTo

    # -----
    # Space
    # -----

    def distributeXSpacing(self, sender):
        self._distributeSpacing(0)

    def distributeYSpacing(self, sender):
        self._distributeSpacing(1)

    def _distributeSpacing(self, index):
        glyph = CurrentGlyph()
        if glyph is None:
            return
        rects, selectedContours, selectedBPoints = getSelectionData(glyph)
        if len(rects) < 3:
            return
        widths = []
        heights = []
        edgeRect = None
        for rect in rects:
            xMin, yMin, xMax, yMax = rect
            widths.append(xMax - xMin)
            heights.append(yMax - yMin)
            if edgeRect is None:
                edgeRect = rect
            else:
                edgeRect = unionRect(edgeRect, rect)
        objectWidth = sum(widths)
        objectHeight = sum(heights)
        xMin, yMin, xMax, yMax = edgeRect
        overallWidth = xMax - xMin
        overallHeight = yMax - yMin
        availableXSpace = overallWidth - objectWidth
        availableYSpace = overallHeight - objectHeight
        xSpace = availableXSpace / (len(rects) - 1)
        ySpace = availableYSpace / (len(rects) - 1)
        spaceBetweenObjects = (xSpace, ySpace)[index]
        ordered = [(bPoint.anchor[index], (bPoint.anchor[0], bPoint.anchor[1], bPoint.anchor[0], bPoint.anchor[1]), bPoint) for bPoint in selectedBPoints]
        ordered += [(contour.bounds[index], contour.bounds, contour) for contour in selectedContours]
        ordered.sort()
        glyph.prepareUndo(title)
        prevEdge = None
        for pos, bounds, obj in ordered[:-1]:
            xMin, yMin, xMax, yMax = bounds
            width = xMax - xMin
            height = yMax - yMin
            size = (width, height)[index]
            if prevEdge is None:
                newPos = (xMin, yMin)[index]
            else:
                newPos = prevEdge + spaceBetweenObjects
            d = newPos - pos
            print(d)
            if d != 0:
                if index == 0:
                    obj.move((d, 0))
                else:
                    obj.move((0, d))
            prevEdge = newPos + size
        for bPoint in selectedBPoints:
            bPoint.round()
        for contour in selectedContours:
            contour.round()
        glyph.performUndo()
        UpdateCurrentGlyphView()


# ---------------
# Glyph Selection
# ---------------

def getSelectionData(glyph):
    rects = []
    selectedContours = []
    selectedBPoints = []
    if glyph is not None:
        for contour in glyph:
            if len(contour) == len(contour.selectedSegments):
                rects.append(contour.bounds)
                selectedContours.append(contour)
            else:
                for bPoint in contour.selectedBPoints:
                    x, y = bPoint.anchor
                    rects.append((x, y, x, y))
                    selectedBPoints.append(bPoint)
    return rects, selectedContours, selectedBPoints

def getEdgeCoordinate(rects, index, func):
    l = [rect[index] for rect in rects]
    return func(l)

# -------------
# Button Images
# -------------

def drawImage(paths, foregroundColor, backgroundColor):
    image = NSImage.alloc().initWithSize_((19, 19))
    image.lockFocus()
    backgroundColor.set()
    NSRectFillUsingOperation(((0, 0), (19, 19)), NSCompositeSourceOver)
    foregroundColor.set()
    path = NSBezierPath.bezierPathWithRect_(((0.5, 0.5), (18, 18)))
    for (mT, lT) in paths:
        path.moveToPoint_(mT)
        path.lineToPoint_(lT)
    path.setLineWidth_(1.0)
    path.stroke()
    image.unlockFocus()
    return image

color1 = NSColor.blackColor()
color2 = NSColor.colorWithCalibratedWhite_alpha_(1, 0.5)

pathYT = [((6.5, 7.5), (6.5, 18.5)), ((12.5, 7.5), (12.5, 18.5))]
pathYC = [((6.5, 4.5), (6.5, 14.5)), ((12.5, 4.5), (12.5, 14.5))]
pathYB = [((6.5, 0.5), (6.5, 11.5)), ((12.5, 0.5), (12.5, 11.5))]

pathXL = [((0.5, 6.5), (11.5, 6.5)), ((0.5, 12.5), (11.5, 12.5))]
pathXC = [((4.5, 6.5), (14.5, 6.5)), ((4.5, 12.5), (14.5, 12.5))]
pathXR = [((7.5, 6.5), (18.5, 6.5)), ((7.5, 12.5), (18.5, 12.5))]

pathCC =[((9.5, 4.5), (9.5, 14.5)), ((4.5, 9.5), (14.5, 9.5))]
pathDX =[((6.5, 0.5), (6.5, 18.5)), ((12.5, 0.5), (12.5, 18.5))]
pathDY =[((0.5, 6.5), (18.5, 6.5)), ((0.5, 12.5), (18.5, 12.5))]

pathDT =[((0.5, 6.5), (18.5, 6.5)), ((0.5, 12.5), (18.5, 12.5)), ((6.5, 8.5), (6.5, 12.5)), ((12.5, 2.5), (12.5, 6.5))]
pathDYC =[((0.5, 6.5), (18.5, 6.5)), ((0.5, 12.5), (18.5, 12.5)), ((6.5, 9.5), (6.5, 15.5)), ((12.5, 3.5), (12.5, 9.5))]
pathDB =[((0.5, 6.5), (18.5, 6.5)), ((0.5, 12.5), (18.5, 12.5)), ((6.5, 12.5), (6.5, 16.5)), ((12.5, 6.5), (12.5, 10.5))]

pathDL =[((6.5, 0.5), (6.5, 18.5)), ((12.5, 0.5), (12.5, 18.5)), ((12.5, 6.5), (16.5, 6.5)), ((6.5, 12.5), (10.5, 12.5))]
pathDXC =[((6.5, 0.5), (6.5, 18.5)), ((12.5, 0.5), (12.5, 18.5)), ((9.5, 6.5), (15.5, 6.5)), ((3.5, 12.5), (9.5, 12.5))]
pathDR =[((6.5, 0.5), (6.5, 18.5)), ((12.5, 0.5), (12.5, 18.5)), ((8.5, 6.5), (12.5, 6.5)), ((2.5, 12.5), (6.5, 12.5))]

def makeImages():
    color1 = RoboHUDController().getForegroundColor()
    color2 = RoboHUDController().getBackgroundColor()
    images = {}
    images["YT"] = drawImage(pathYT, color1, color2)
    images["YC"] = drawImage(pathYC, color1, color2)
    images["YB"] = drawImage(pathYB, color1, color2)
    images["XL"] = drawImage(pathXL, color1, color2)
    images["XC"] = drawImage(pathXC, color1, color2)
    images["XR"] = drawImage(pathXR, color1, color2)
    images["CC"] = drawImage(pathCC, color1, color2)
    images["DX"] = drawImage(pathDX, color1, color2)
    images["DY"] = drawImage(pathDY, color1, color2)
    images["DT"] = drawImage(pathDT, color1, color2)
    images["DYC"] = drawImage(pathDYC, color1, color2)
    images["DB"] = drawImage(pathDB, color1, color2)
    images["DL"] = drawImage(pathDL, color1, color2)
    images["DXC"] = drawImage(pathDXC, color1, color2)
    images["DR"] = drawImage(pathDR, color1, color2)
    return images
