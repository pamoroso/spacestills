# Spacestills

[Spacestills](https://github.com/pamoroso/spacestills) is a Python program for viewing NASA TV still frames. It periodically downloads the frames from a [web feed](https://science.ksc.nasa.gov/shuttle/countdown/video/chan2large.jpg) and displays them in a GUI.

![Spacestills main window](https://raw.githubusercontent.com/pamoroso/spacestills/master/spacestills.jpg)

The program allows to correct the aspect ratio of the frames and save them. It downloads the latest frame automatically and gives the option to reload manually, disable the automatic reload, or change the download frequency.

Spacestills has a GUI based on the [PySimpleGUI](https://pysimplegui.readthedocs.io/en/latest/) framework and relies on the [Pillow](https://pillow.readthedocs.io) and [Requests](https://docs.python-requests.org) libraries. More implementation details are in a blog post that discusses the [design of Spacestills](https://blog.paoloamoroso.com/2021/04/a-nasa-tv-still-frame-viewer-in-python.html).


## Installation 

Spacestills is available on PyPI, so to install the package execute the following shell command:

```
$ pip install spacestills
```


## Usage

### Running on Replit

To run the program online on Replit visit the [Spacestills REPL](https://replit.com/@PaoloAmoroso/spacestills) with a browser and click `Run`. If the program window is cropped, try marking the checkbox `Correct aspect ratio`.

You can also adjust the size of the X Window desktop pane when running Spacestills directly in a REPL. You may see screen redraw artifacts when dragging the window on the desktop. To force a refresh and fix the issue, restart the window manager by right-clicking on the X desktop and then clicking `Restart`.


### Running elsewhere

You can run Spacestills from the shell by executing the command:

```
$ spacestills
```


### Commands and options

The program window displays the current NASA TV still frame and automatically reloads it every 45 seconds.

The images are stretched vertically in the raw web feed. Mark the `Correct aspect ratio` checkbox to squeeze the image and get an undistorted view.

To manually refresh the image click the `Reload` button. Change the reload frequency by entering an integer number of seconds (from 45 to 300) in the text field and pressing `Set`. You can disable auto-reload by unmarking the `Auto-reload every (seconds):` checkbox.

Click the `Save` button to save the current image to the local file system in PNG format, or `Exit` to quit the program.


## Known issues

Typing a file name in the save dialog without first going through the file browse dialog doesn't add the default `.png` extension.


## Release history

See the [list of releases](https://github.com/pamoroso/spacestills/releases) for notes on the changes in each version.


## Author

[Paolo Amoroso](https://www.paoloamoroso.com) developed Spacestills as a Python learning exercise. Email: `info@paoloamoroso.com`


## License

This code is distributed under the MIT license, see the `LICENSE` file.
