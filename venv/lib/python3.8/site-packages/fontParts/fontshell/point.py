import defcon
from fontParts.base import BasePoint, FontPartsError
from fontParts.fontshell.base import RBaseObject


class RPoint(RBaseObject, BasePoint):

    wrapClass = defcon.Point

    def _init(self, wrap=None):
        if wrap is None:
            wrap = self.wrapClass((0, 0))
        super(RPoint, self)._init(wrap=wrap)

    def _postChangeNotification(self):
        contour = self.contour
        if contour is None:
            return
        contour.naked().postNotification("Contour.PointsChanged")
        self.changed()
        
    def changed(self):
        self.contour.naked().dirty = True

    # ----------
    # Attributes
    # ----------

    # type

    def _get_type(self):
        value = self.naked().segmentType
        if value is None:
            value = "offcurve"
        return value

    def _set_type(self, value):
        if value == "offcurve":
            value = None
        self.naked().segmentType = value
        self._postChangeNotification()

    # smooth

    def _get_smooth(self):
        return self.naked().smooth

    def _set_smooth(self, value):
        self.naked().smooth = value
        self._postChangeNotification()

    # x

    def _get_x(self):
        return self.naked().x

    def _set_x(self, value):
        self.naked().x = value
        self._postChangeNotification()

    # y

    def _get_y(self):
        return self.naked().y

    def _set_y(self, value):
        self.naked().y = value
        self._postChangeNotification()

    # --------------
    # Identification
    # --------------

    # name

    def _get_name(self):
        return self.naked().name

    def _set_name(self, value):
        self.naked().name = value
        self._postChangeNotification()

    # identifier

    def _get_identifier(self):
        point = self.naked()
        return point.identifier

    def _getIdentifier(self):
        point = self.naked()
        value = point.identifier
        if value is not None:
            return value
        if self.contour is not None:
            contour = self.contour.naked()
            contour.generateIdentifierForPoint(point)
            value = point.identifier
        else:
            raise FontPartsError(("An identifier can not be generated "
                                  "for this point because it does not "
                                  "belong to a contour."))
        return value
