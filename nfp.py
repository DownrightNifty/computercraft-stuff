from PIL import Image
import numpy as np

# NFP is a simple text-based 16-color image format used by ComputerCraft's paint
# program. Each pixel is represented by a one-digit hex value from 0-f (decimal
# 0-15) corresponding to an index into the 16-color ComputerCraft color palette.
# Each row is terminated by a newline.
#
# Example of a 4x4 black/white checkerboard pattern NFP image:
# f0f0
# 0f0f
# f0f0
# 0f0f

# values come from http://www.computercraft.info/wiki/Colors_(API)
CC_COLORS = (
    (240, 240, 240), # white, 0
    (242, 178, 51),  # orange, 1
    (229, 127, 216), # magenta, 2
    (153, 178, 242), # lightBlue, 3
    (222, 222, 108), # yellow, 4
    (127, 204, 25),  # lime, 5
    (242, 178, 204), # pink, 6
    (76, 76, 76),    # gray, 7
    (153, 153, 153), # lightGray, 8
    (76, 153, 178),  # cyan, 9
    (178, 102, 229), # purple, a
    (51, 102, 204),  # blue, b
    (127, 102, 76),  # brown, c
    (87, 166, 78),   # green, d
    (204, 76, 76),   # red, e
    (25, 25, 25)     # black, f
)

# Takes a PIL image and converts to nfp. Returns nfp data as string.
# If new_size is provided, image will be resized before conversion.
# new_size should be a 2-tuple: (width, height).
# Recommended size for CC monitors at text scale 0.5 is (164, 81).
def img_to_nfp(im, new_size=None):
    if new_size:
        im = im.resize(new_size)
    # A technique called image quantization is used to reduce the input image's
    # color palette to only the 16 ComputerCraft colors.
    im = _quantize_with_colors(im, CC_COLORS)
    # After quantize, im is mode "P" (palletized), so im.getdata() returns a
    # sequence of ints representing indexes into the image's 16-color palette
    # from 0-15 (hex 0-f) for each pixel in the image. This is flattened, so
    # the values for image line two immediately follow image line one's values.
    # We use np.reshape() to turn it into a 2D numpy array whose values can be
    # accessed through arr[row][col] notation.
    data = im.getdata()
    width, height = im.size
    data_2d = np.reshape(np.array(data), (height, width))
    # convert from np array back to list for faster iteration
    data_2d = data_2d.tolist()
    nfp_im = ""
    for row in range(height):
        for col in range(width):
            # convert 0-15 decimal value to hex string (0-f)
            nfp_im += format(data_2d[row][col], "x")
        if row != len(data_2d) - 1:
            nfp_im += "\n"
    return nfp_im

# Takes nfp (as string data) and returns a PIL image.
def nfp_to_img(nfp):
    nfp = nfp.splitlines()
    height = len(nfp)
    width = len(nfp[0])
    im = Image.new("RGB", (width, height))
    px = im.load()
    for row in range(height):
        for col in range(width):
            nfp_pixel = nfp[row][col]
            color_idx = int(nfp_pixel, 16)
            pixel_color = CC_COLORS[color_idx]
            px[col, row] = pixel_color
    return im

# Colors is a list/tuple of 3-item (R, G, B) tuples.
def _quantize_with_colors(image, colors):
    pal_im = Image.new("P", (1, 1))
    color_vals = []
    for color in colors:
        for val in color:
            color_vals.append(val)
    color_vals = tuple(color_vals)
    pal_im.putpalette(color_vals + colors[-1] * (256 - len(colors)))
    image = image.convert("RGB")
    return image.quantize(palette=pal_im)
