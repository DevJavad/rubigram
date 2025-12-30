#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from ..enum import Enum


class ButtonType(Enum):
    """
    **Represents the different types of interactive buttons available in a chat.**
        `from rubigram.enums import ButtonType`

    Attributes:
        SIMPLE (str): A simple button.
        SELECTION (str): A selection button.
        CALENDAR (str): A calendar picker button.
        NUMBER_PICKER (str): A number picker button.
        STRING_PICKER (str): A string picker button.
        LOCATION (str): A button to share location.
        PAYMENT (str): A payment button.
        CAMERA_IMAGE (str): A button to capture an image via camera.
        CAMERA_VIDEO (str): A button to record a video via camera.
        GALLERY_IMAGE (str): A button to select an image from gallery.
        GALLERY_VIDEO (str): A button to select a video from gallery.
        FILE (str): A button to send a file.
        AUDIO (str): A button to send an audio file.
        RECORD_AUDIO (str): A button to record audio.
        MY_PHONE_NUMBER (str): A button to share the user's phone number.
        MY_LOCATION (str): A button to share the user's location.
        TEXTBOX (str): A textbox input button.
        LINK (str): A button containing a link.
        ASK_MY_PHONE_NUMBER (str): A button that requests the user's phone number.
        ASK_LOCATION (str): A button that requests the user's location.
        BARCODE (str): A button to scan a barcode.
    """

    SIMPLE = "Simple"
    SELECTION = "Selection"
    CALENDAR = "Calendar"
    NUMBER_PICKER = "NumberPicker"
    STRING_PICKER = "StringPicker"
    LOCATION = "Location"
    PAYMENT = "Payment"
    CAMERA_IMAGE = "CameraImage"
    CAMERA_VIDEO = "CameraVideo"
    GALLERY_IMAGE = "GalleryImage"
    GALLERY_VIDEO = "GalleryVideo"
    FILE = "File"
    AUDIO = "Audio"
    RECORD_AUDIO = "RecordAudio"
    MY_PHONE_NUMBER = "MyPhoneNumber"
    MY_LOCATION = "MyLocation"
    TEXTBOX = "Textbox"
    LINK = "Link"
    ASK_MY_PHONE_NUMBER = "AskMyPhoneNumber"
    ASK_LOCATION = "AskLocation"
    BARCODE = "Barcode"