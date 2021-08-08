from PIL import Image
import nfp
import argparse
import os

# default resize width/height when converting image -> nfp
DEFAULT_WIDTH, DEFAULT_HEIGHT = 164, 81

desc = (
    "Convert standard image files to ComputerCraft nfp files, and vice "
    "versa. Input file type is identified by extension (.nfp, .jpg, etc.), "
    "and output files use the input filename with a new extension."
)
files_help = "input files, nfp or image (must have correct file extension)"
nfp_desc = "optional arguments when converting image -> nfp"
skip_help = "skip default behavior of resizing image before conversion"
width_help = "if resizing, new width (default: {})".format(DEFAULT_WIDTH)
height_help = "if resizing, new height (default: {})".format(DEFAULT_HEIGHT)
im_desc = "optional arguments when converting nfp -> image"
format_help = (
    "output format passed to Image.save() (also output file extension "
    "unless -e argument specified), see PIL docs for supported formats, "
    "default: PNG"
)
ext_help = (
    "if specified, will be used as the output file extension instead of "
    "FORMAT"
)
rm_help = "remove the original image after converting"

parser = argparse.ArgumentParser(description=desc)
parser.add_argument("files", help=files_help, nargs='+')
nfp_group = parser.add_argument_group("nfp arguments", description=nfp_desc)
nfp_group.add_argument("--skip-resize", "-s", help=skip_help,
                       action="store_true", default=False)
nfp_group.add_argument("--resize-width", "-w", help=width_help,
                       metavar="WIDTH", type=int, default=DEFAULT_WIDTH)
nfp_group.add_argument("--resize-height", "-H", help=height_help,
                       metavar="HEIGHT", type=int, default=DEFAULT_HEIGHT)
im_group = parser.add_argument_group("image arguments", description=im_desc)
im_group.add_argument("--format", "-f", help=format_help, metavar="FORMAT",
                      dest="f_format", default="PNG")
im_group.add_argument("--extension", "-e", help=ext_help)
im_group.add_argument("--remove", "-r", help=rm_help, action="store_true")

args = parser.parse_args()

for file in args.files:
    filename, ext = os.path.splitext(file)
    if not ext:
        parser.error("filename must have appropriate extension")
    if ext.upper() == ".NFP":
        with open(file, "rt") as f:
            nfp_file = f.read()
        im = nfp.nfp_to_img(nfp_file)
        new_ext = args.f_format.replace(" ", "").lower()
        if args.extension:
            new_ext = args.extension
        im.save("{}.{}".format(filename, new_ext), args.f_format)
    else:
        im = Image.open(file)
        if args.skip_resize:
            nfp_file = nfp.img_to_nfp(im)
        else:
            nfp_file = nfp.img_to_nfp(
                im, (args.resize_width, args.resize_height))
        with open("{}.nfp".format(filename), "wt") as f:
            f.write(nfp_file)
    if args.remove:
        os.remove(file)
