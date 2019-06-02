# ComputerCraft image stuff
## NFP format
"NFP" is a simple text-based 16-color image format used by ComputerCraft's [paint](http://www.computercraft.info/wiki/Paint) program and the [paintutils](http://www.computercraft.info/wiki/Paintutils_(API)) API. Each pixel is represented by a one-digit hex value from 0-f (decimal 0-15) corresponding to an index into the 16-color [ComputerCraft color palette](http://www.computercraft.info/wiki/Colors_(API)#Colors). Each row is terminated by a newline.

A black/white 4x4 checkerboard NFP image looks like this:
```
f0f0
0f0f
f0f0
0f0f
```

The `nfp.py` module can convert between standard image formats and NFP. When converting from image to NFP, it uses [Pillow](https://python-pillow.org/) to [quantize](https://en.wikipedia.org/wiki/Quantization_(image_processing)) the image, reducing its color palette to only the 16 available ComputerCraft colors.

`convert_nfp.py` is a simple command-line utilty that uses this module, made because why not?

Converting from image -> NFP:
```
convert_nfp.py image.png
```
(Images are automatically resized to 164x81, the maximum resolution for [scale 0.5](http://www.computercraft.info/wiki/Monitor.setTextScale) ComputerCraft monitors, before conversion, unless the `--skip-resize`, `--resize-width`, or `--resize-height` arguments are specified.)

Converting from NFP -> PNG:
```
convert_nfp.py image.nfp
```

Converting from NFP -> JPEG:
```
convert_nfp.py image.nfp --format=JPEG
```

See `convert_nfp.py -h` for full usage info. See the [Pillow docs](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#fully-supported-formats) for supported conversion formats.

After converting an image to NFP, you can upload it to pastebin, and use [`paintutils.drawImage()`](http://www.computercraft.info/wiki/Paintutils.drawImage) to display it in-game. Example program that downloads an NFP from pastebin (like [this one](https://pastebin.com/ku2jnU6X)) using the paste ID passed in as an argument and displays it on a connected monitor:
```lua
local args = {...}
local paste_id = args[1]
shell.run("pastebin", "get", paste_id, "image.nfp")
local mon = peripheral.find("monitor")
mon.setTextScale(0.5)
term.redirect(mon)
term.clear()
local image = paintutils.loadImage("image.nfp")
paintutils.drawImage(image, 0, 0)
```

This example program has been [posted to pastebin](https://pastebin.com/7YWBbCV1), so you can just use:
```
pastebin get 7YWBbCV1 disp_nfp
disp_nfp NFP_PASTE_ID_HERE
```

Python scripts were tested on Python 2.7, PIL/Pillow 1.1.7.
