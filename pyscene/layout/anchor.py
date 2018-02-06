from ..arrays import Point

class AnchorX:
    LEFT = 1
    RIGHT = 2
    CENTER = 3

class AnchorY:
    TOP = 1
    BOTTOM = 2
    CENTER = 3

class Anchor:
    MID_RIGHT        =  Point(AnchorX.RIGHT,    AnchorY.CENTER)
    MID_LEFT         =  Point(AnchorX.LEFT,     AnchorY.CENTER)
    MID_BOTTOM       =  Point(AnchorX.CENTER,   AnchorY.BOTTOM)
    MID_TOP          =  Point(AnchorX.CENTER,   AnchorY.TOP)
    CENTER           =  Point(AnchorX.CENTER,   AnchorY.CENTER)
    RIGHT            =  Point(AnchorX.RIGHT,    AnchorY.TOP)
    LEFT             =  Point(AnchorX.LEFT,     AnchorY.TOP)
    BOTTOM           =  Point(AnchorX.LEFT,     AnchorY.BOTTOM)
    TOP              =  Point(AnchorX.LEFT,     AnchorY.TOP)
