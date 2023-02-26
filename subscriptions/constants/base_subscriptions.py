from enum import Enum

from .base_img_sizes import Height200pxWidthUndefined, Height400pxWidthUndefined


class Basic(Enum):
    """
    Basic subscription with defined image sizes. Subscription does not allow to return a link to
    the original image to the user and to generate expiring links
    """
    SIZE = (Height200pxWidthUndefined,)
    ORIGINAL_FILE = False
    EXPIRING_LINKS = False


class Premium(Enum):
    """
    Premium subscription with defined image sizes. Subscription does allow to return a link to
    the original image to the user and does not allow to generate expiring links
    """
    SIZE = (Height200pxWidthUndefined, Height400pxWidthUndefined)
    ORIGINAL_FILE = True
    EXPIRING_LINKS = False


class Enterprise(Enum):
    """
    Enterprise subscription with defined image sizes. Subscription does allow to return a link to
    the original image to the user to generate expiring links
    """
    SIZE = (Height200pxWidthUndefined, Height400pxWidthUndefined)
    ORIGINAL_FILE = True
    EXPIRING_LINKS = True
