"""
A NASA TV still frame viewer.

It allows to correct the aspect ratio of the frames and save them to disc. The
program downloads the latest frame automatically and gives the option to reload
manually, disable the automatic reload, or change the download frequency.
"""


from io import BytesIO
from datetime import datetime, timedelta
from pathlib import Path
import requests
from requests.exceptions import Timeout
from PIL import Image
import PySimpleGUI as sg


FEED_URL = 'https://science.ksc.nasa.gov/shuttle/countdown/video/chan2large.jpg'

# Frame size without and with 16:9 aspect ratio correction
WIDTH = 704
HEIGHT = 480
HEIGHT_16_9 = 396

# Minimum, default, and maximum autoreload interval in seconds
MIN_DELTA = 45
DELTA = MIN_DELTA
MAX_DELTA = 300


class StillFrame():
    """Holds a still frame.
    
    The image is stored as a PNG PIL.Image and kept in PNG format.

    Attributes
    ----------
        image : PIL.Image
            A still frame
        original : PIL.Image
            Original frame with wchich the instance is initialized, cached in case of
            resizing to the original size
    
    Methods
    -------
        bytes : Return the raw bytes
        resize : Resize the screenshot
        new_size : Calculate new aspect ratio
    """

    def __init__(self, image):
        """Convert the image to PNG and cache the converted original.

        Parameters
        ----------
            image : PIL.Image
                Image to store
        """
        self.image = image
        self._topng()
        self.original = self.image

    def _topng(self):
        """Convert image format of frame to PNG.

        Returns
        -------
            StillFrame
                Frame with image in PNG format
        """
        if not self.image.format == 'PNG':
            png_file = BytesIO()
            self.image.save(png_file, 'png')
            png_file.seek(0)
            png_image = Image.open(png_file)
            self.image = png_image
        return self

    def bytes(self):
        """Return raw bytes of a frame image.
        
        Returns
        -------
            bytes
                Byte stream of the frame image
        """
        file = BytesIO()
        self.image.save(file, 'png')
        file.seek(0)
        return file.read()

    def new_size(self):
        """Return image size toggled between original and 16:9.
        
        Returns
        -------
            2-tuple
                New size
        """
        size = self.image.size
        original_size = self.original.size
        new_size = (WIDTH, HEIGHT_16_9) if size == original_size else (WIDTH, HEIGHT)
        return new_size

    def resize(self, new_size):
        """Resize frame image.
        
        Parameters
        ----------
            new_size : 2-tuple
                New size

        Returns
        -------
            StillFrame
                Frame with image resized
        """
        if not(self.image.size == new_size):
            self.image = self.image.resize(new_size)
        return self
    

def make_blank_image(size=(WIDTH, HEIGHT)):
    """Create a blank image with a blue background.
    
    Parameters
    ----------
        size : 2-tuple
            Image size
    
    Returns
    -------
        PIL.Image
            Blank image
    """
    image = Image.new('RGB', size=size, color='blue')
    return image


def download_image(url):
    """Download current NASA TV image.

    Parameters
    ----------
        url : str
            URL to download the image from
    
    Returns
    -------
        PIL.Image
            Downloaded image if no errors, otherwise blank image
    """
    try:
        response = requests.get(url, timeout=(0.5, 0.5))
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
        else:
            image = make_blank_image()
    except Timeout:
        image = make_blank_image()
    return image


def refresh(window, resize=False, feed=FEED_URL):
    """Display the latest still frame in window.
    
    Parameters
    ----------
        window : sg.Window
            Window to display the still to
        feed : string
            Feed URL
    
    Returns
    -------
        StillFrame
            Refreshed screenshot
    """
    still = StillFrame(download_image(feed))
    if resize:
        still = change_aspect_ratio(window, still, new_size=(WIDTH, HEIGHT_16_9))
    else:
        window['-IMAGE-'].update(data=still.bytes())
    return still


def change_aspect_ratio(window, still, new_size=(WIDTH, HEIGHT_16_9)):
    """Change the aspect ratio of the still displayed in window.
    
    Parameters
    ----------
        window : sg.Window
            Window containing the still
        new_size : 2-tuple
            New size of the still
    
    Returns
    -------
        StillFrame
            Frame containing the resized image
    """
    resized_still = still.resize(new_size)
    window['-IMAGE-'].update(data=resized_still.bytes())
    return resized_still


def save(still, path):
    """Save still to a file.

    Parameters
    ----------
        still : StillFrame
            Still to save
        path : string
            File name
    
    Returns
    -------
        Boolean
            True if file saved with no errors
    """
    filename = Path(path)
    try:
        with open(filename, 'wb') as file:
            file.write(still.bytes())
        saved = True
    except OSError:
        saved = False
    return saved


def next_timeout(delta):
    """Return the moment in time right now + delta seconds from now.

    Parameters
    ----------
        delta : int
            Time in seconds until the next timeout
    
    Returns
    -------
        datetime.datetime
            Moment in time of the next timeout
    """
    rightnow = datetime.now()
    return rightnow + timedelta(seconds=delta)


def timeout_due(next_timeout):
    """Return True if the next timeout is due.

    Parameters
    ----------
        next_timeout : datetime.datetime
    
    Returns
    -------
        bool
            True if the next timeout is due
    """
    rightnow = datetime.now()
    return rightnow >= next_timeout


def validate_delta(value):
    """Check if value is an int within the proper range for a time delta.

    Parameters
    ----------
        value : int
            Time in seconds until the next timeout
    
    Returns
    -------
        int
            Time in seconds until the next timeout
        bool
            True if the argument is a valid time delta
    """
    isinteger = False
    try:
        isinteger = type(int(value)) is int
    except Exception:
        delta = DELTA
    delta = int(value) if isinteger else delta
    isvalid = MIN_DELTA <= delta <= MAX_DELTA
    delta = delta if isvalid else DELTA
    return delta, isinteger and isvalid


LAYOUT = [[sg.Image(key='-IMAGE-')],
          [sg.Checkbox('Correct aspect ratio', key='-RESIZE-', enable_events=True),
           sg.Button('Reload', key='-RELOAD-'),
           sg.Button('Save', key='-SAVE-'),
           sg.Exit()],
          [sg.Checkbox('Auto-reload every (seconds):', key='-AUTORELOAD-',
                       default=True),
           sg.Input(DELTA, key='-DELTA-', size=(3, 1), justification='right'),
           sg.Button('Set', key='-UPDATE_DELTA-')]]


def main():
    """Run event loop."""
    window = sg.Window('Spacestills', LAYOUT, finalize=True)
    current_still = refresh(window)

    delta = DELTA
    next_reload_time = datetime.now() + timedelta(seconds=delta)

    while True:
        event, values = window.read(timeout=100)
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif ((event == '-RELOAD-') or
                (values['-AUTORELOAD-'] and timeout_due(next_reload_time))):
            current_still = refresh(window, values['-RESIZE-'])
            if values['-AUTORELOAD-']:
                next_reload_time = next_timeout(delta)
        elif event == '-RESIZE-':
            current_still = change_aspect_ratio(
                window, current_still, current_still.new_size())
        elif event == '-SAVE-':
            filename = sg.popup_get_file(
                'File name', file_types=[('PNG', '*.png')], save_as=True,
                title='Save image', default_extension='.png')
            if filename:
                saved = save(current_still, filename)
                if not saved:
                    sg.popup_ok('Error while saving file:', filename, title='Error')
        elif event == '-UPDATE_DELTA-':
            # The current cycle should complete at the already scheduled time. So
            # don't update next_reload_time yet because it'll be taken care of at the
            # next -AUTORELOAD- or -RELOAD- event.
            delta, valid = validate_delta(values['-DELTA-'])
            if not valid:
                window['-DELTA-'].update(str(DELTA))

    window.close()
    del window
