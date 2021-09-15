# ComputerCraft NFP Image Converter
A Python program to convert images into NFP images for display on ComputerCraft monitors inside of Minecraft. Inspired by [this program.](https://old.reddit.com/r/feedthebeast/comments/1ee4xf/easy_image_to_computercraft_converter/c9zsevu) Feel free to open issues or PRs.

The `nfp.py` module can convert between standard image formats and NFP. When converting from image to NFP, it uses [Pillow](https://python-pillow.org/) to [quantize](https://en.wikipedia.org/wiki/Quantization_(image_processing)) the image, reducing its color palette to the 16 available ComputerCraft colors.

`convert_nfp.py` is a simple command-line utilty that uses this module, made because why not?

## NFP format
"NFP" is a simple text-based 16-color image format used by ComputerCraft's [paint](http://www.computercraft.info/wiki/Paint) program and the [paintutils](http://www.computercraft.info/wiki/Paintutils_(API)) API. Each pixel is represented by a one-digit hex value from 0-f (decimal 0-15) corresponding to an index into the 16-color [ComputerCraft color palette](http://www.computercraft.info/wiki/Colors_(API)#Colors). Each row is terminated by a newline.

A black/white 4x4 checkerboard NFP image looks like this:
```bash
f0f0
0f0f
f0f0
0f0f
```

## Installation
```bash
python3 -m pip install -r requirements.txt
```

## Usage and Example
Converting from image -> NFP:

```bash
python3 convert_nfp.py image.png
```
(Images are automatically resized to 164x81, the maximum resolution for 8 by 6 (max size) [scale 0.5](http://www.computercraft.info/wiki/Monitor.setTextScale) ComputerCraft monitors, before conversion, unless the `--skip-resize`, `--resize-width`, or `--resize-height` arguments are specified.)

Converting from NFP -> PNG:
```bash
python3 convert_nfp.py image.nfp
```

Converting from NFP -> JPEG:
```bash
python3 convert_nfp.py image.nfp --format=JPEG
```

Converting multiple files at once:
```bash
python3 convert_nfp.py image1.nfp image2.nfp [...]
```
(Special thanks to Commandcracker for this [feature](https://github.com/DownrightNifty/computercraft-stuff/pull/3)!)

See `convert_nfp.py -h` for full usage info. See the [Pillow docs](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#fully-supported-formats) for supported conversion formats.

After converting an image to NFP, you can upload it to pastebin, and use [`paintutils.drawImage()`](http://www.computercraft.info/wiki/Paintutils.drawImage) to fetch and display it in-game. Example program that downloads an NFP from pastebin (like [this one](https://pastebin.com/ku2jnU6X)) using the paste ID passed in as an argument and displays it on a connected monitor:

```lua
local args = {...}
local paste_id = args[1]
shell.run("delete image.nfp") --delete file if it already exists
shell.run("pastebin", "get", paste_id, "image.nfp") --fetch NFP image from pastebin at given paste_id
print("Drawing...")
local old_term = term.current()
local mon = peripheral.find("monitor") --find and attach to monitor
mon.setTextScale(0.5)
term.redirect(mon)
term.clear()
--draw image through paintutils
local image = paintutils.loadImage("image.nfp") 
paintutils.drawImage(image, 0, 0)
term.redirect(old_term)
print("Done")
```

This example program has been [posted to pastebin](https://pastebin.com/MuZxYKrQ), so you can just use the below to display an example image:

```bash
pastebin get MuZxYKrQ disp_nfp
disp_nfp yjXanZ0j
```

Tested on Python 3.
