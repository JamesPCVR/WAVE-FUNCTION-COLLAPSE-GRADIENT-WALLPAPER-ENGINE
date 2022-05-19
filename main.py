from PIL import Image, ImageDraw, ImageFilter, ImageOps
import wave_function_collapse
import json
import os

SETTINGSSOURCE = None
if not SETTINGSSOURCE:
    SETTINGSSOURCE = f"settings/{input('settings .json source file name: ')}"

def HexToRGB(hex:str):
    rgb = []
    for i in (1, 3, 5):
        rgb.append(int(hex[i:i+2], 16))
    return tuple(rgb)

def RGBToHex(rgbtupl:tuple):
    r, g, b = rgbtupl
    return f"{r:x}{g:x}{b:x}"

def interpolate(f_co, t_co, interval):
    det_co =[(t - f) / interval for f , t in zip(f_co, t_co)]
    for i in range(interval):
        yield [round(f + det * i) for f, det in zip(f_co, det_co)]

f = open(f"{SETTINGSSOURCE}.json")
settings = json.load(f)
f.close()

IMAGEWIDTH = settings["wallpaper_size"]["width"]
IMAGEHEIGHT = settings["wallpaper_size"]["height"]

LINEENABLE = settings["foreground"]["lines"]["enabled"]
LINEORIENTATION = settings["foreground"]["lines"]["orientation"]
LINECOUNT = settings["foreground"]["lines"]["line_count"]
LINESPACING = settings["foreground"]["lines"]["line_spacing"]
LINEWIDTH = settings["foreground"]["lines"]["line_width"]
CENTERWIDTH = settings["foreground"]["lines"]["center_width"]

FOREGROUNDENABLE = settings["foreground"]["enabled"]
FORETOPGRADIENTENABLE = settings["foreground"]["top_gradient"]
FORETOPCOLORTL = HexToRGB(settings["foreground"]["top_color_tl"])
FORETOPCOLORBR = HexToRGB(settings["foreground"]["top_color_br"])
FOREBOTTOMENABLE = settings["foreground"]["bottom_enabled"]
FOREBOTTOMGRADIENTENABLE = settings["foreground"]["bottom_gradient"]
FOREBOTTOMCOLORTL = HexToRGB(settings["foreground"]["bottom_color_tl"])
FOREBOTTOMCOLORBR = HexToRGB(settings["foreground"]["bottom_color_br"])
TOPMASKSOURCE = settings["foreground"]["top_mask_source"]
BOTTOMMASKSOURCE = settings["foreground"]["bottom_mask_source"]

BACKGROUNDENABLE = settings["background"]["enabled"]
BACKTOPGRADIENTENABLE = settings["background"]["top_gradient"]
BACKTOPCOLORTL = HexToRGB(settings["background"]["top_color_tl"])
BACKTOPCOLORBR = HexToRGB(settings["background"]["top_color_br"])
BACKBOTTOMGRADIENTENABLE = settings["background"]["bottom_gradient"]
BACKBOTTOMCOLORTL = HexToRGB(settings["background"]["bottom_color_tl"])
BACKBOTTOMCOLORBR = HexToRGB(settings["background"]["bottom_color_br"])
BACKBLURSTRENGTH = settings["background"]["blur_strength"]

WAVEFUNCTIONCOLLAPSEENABLE = settings["background"]["wave_function_collapse"]["enabled"]

GRAYSCALEIMAGEENABLE = settings["background"]["grayscale_image"]["enabled"]
GRAYSCALEIMAGEINVERT = settings["background"]["grayscale_image"]["invert"]
GRAYSCALEIMAGESOURCE = settings["background"]["grayscale_image"]["file_source"]

BINARYIMAGEENABLE = settings["background"]["binary_image"]["enabled"]
BINARYIMAGETHRESHOLD = settings["background"]["binary_image"]["threshold"]
BINARYIMAGEINVERT = settings["background"]["binary_image"]["invert"]
BINARYIMAGESOURCE = settings["background"]["binary_image"]["file_source"]

SAVEPARTS = settings["save_parts"]
OUTPUTNAME = settings["output_name"]

if SAVEPARTS:
    exists = os.path.exists("parts")
    if not exists:
        os.makedirs("parts")

imagefinal = None

if BACKGROUNDENABLE:
    if not imagefinal:
        imagefinal = Image.new("RGB", (IMAGEWIDTH, IMAGEHEIGHT), 0)
    
    backgroundmask = Image.new("RGB", (IMAGEWIDTH, IMAGEHEIGHT), 0)
    
    backgroundtopcolor = Image.new('RGB', (IMAGEWIDTH, IMAGEHEIGHT), BACKTOPCOLORTL)
    if BACKTOPGRADIENTENABLE:
        backgroundtopcolorcanvas = ImageDraw.Draw(backgroundtopcolor)
        for i, color in enumerate(interpolate(BACKTOPCOLORTL, BACKTOPCOLORBR, backgroundtopcolor.height + backgroundtopcolor.width - 1)):
            backgroundtopcolorcanvas.line([(i, 0), (0, i)], tuple(color), width=1)
    if SAVEPARTS:
        backgroundtopcolor.save("parts/background_top_color.png", "PNG")

    backgroundbottomcolor = Image.new('RGB', (IMAGEWIDTH, IMAGEHEIGHT), BACKBOTTOMCOLORTL)
    if BACKBOTTOMGRADIENTENABLE:
        backgroundbottomcolorcanvas = ImageDraw.Draw(backgroundbottomcolor)
        for i, color in enumerate(interpolate(BACKBOTTOMCOLORTL, BACKBOTTOMCOLORBR, backgroundbottomcolor.height + backgroundbottomcolor.width - 1)):
            backgroundbottomcolorcanvas.line([(i, 0), (0, i)], tuple(color), width=1)
    if SAVEPARTS:
        backgroundbottomcolor.save("parts/background_bottom_color.png", "PNG")

    if WAVEFUNCTIONCOLLAPSEENABLE:
        backgroundmask = wave_function_collapse.main(SETTINGSSOURCE).convert("L")

    if GRAYSCALEIMAGEENABLE:
        backgroundmask = Image.open(GRAYSCALEIMAGESOURCE)
        backgroundmask = backgroundmask.resize((IMAGEWIDTH, IMAGEHEIGHT), resample=Image.ANTIALIAS)
        backgroundmask = backgroundmask.convert("L")
        if not GRAYSCALEIMAGEINVERT:
            backgroundmask = ImageOps.invert(backgroundmask)
    
    if BINARYIMAGEENABLE:
        backgroundmask = Image.open(BINARYIMAGESOURCE)
        backgroundmask = backgroundmask.resize((IMAGEWIDTH, IMAGEHEIGHT), resample=Image.ANTIALIAS)
        backgroundmask = backgroundmask.convert("L")
        backgroundmask = backgroundmask.point(lambda p: (255 if BINARYIMAGEINVERT else 0) if p > BINARYIMAGETHRESHOLD else (0 if BINARYIMAGEINVERT else 255))
    
    if SAVEPARTS:
        backgroundmask.save("parts/background_mask.png", "PNG")
    imagefinal = backgroundbottomcolor
    imagefinal.paste(backgroundtopcolor, (0, 0), backgroundmask)
    imagefinal = imagefinal.filter(ImageFilter.BoxBlur(BACKBLURSTRENGTH))
    if SAVEPARTS:
        imagefinal.save("parts/image_background.png", "PNG")

if FOREGROUNDENABLE:
    if not imagefinal:
        imagefinal = Image.new("RGB", (IMAGEWIDTH, IMAGEHEIGHT), 0)
    
    foregroundtopcolor = Image.new('RGB', (IMAGEWIDTH, IMAGEHEIGHT), FORETOPCOLORTL)
    if FORETOPGRADIENTENABLE:
        foregroundtopcolorcanvas = ImageDraw.Draw(foregroundtopcolor)
        for i, color in enumerate(interpolate(FORETOPCOLORTL, FORETOPCOLORBR, foregroundtopcolor.height + foregroundtopcolor.width - 1)):
            foregroundtopcolorcanvas.line([(i, 0), (0, i)], tuple(color), width=1)
    if SAVEPARTS:
        foregroundtopcolor.save("parts/foreground_top_color.png", "PNG")

    if FOREBOTTOMENABLE:
        foregroundbottomcolor = Image.new('RGB', (IMAGEWIDTH, IMAGEHEIGHT), FOREBOTTOMCOLORTL)
        if FOREBOTTOMGRADIENTENABLE:
            foregroundbottomcolorcanvas = ImageDraw.Draw(foregroundbottomcolor)
            for i, color in enumerate(interpolate(FOREBOTTOMCOLORTL, FOREBOTTOMCOLORBR, foregroundbottomcolor.height + foregroundbottomcolor.width - 1)):
                foregroundbottomcolorcanvas.line([(i, 0), (0, i)], tuple(color), width=1)
        if SAVEPARTS:
            foregroundbottomcolor.save("parts/foreground_bottom_color.png", "PNG")

    masktop = Image.new("L", (IMAGEWIDTH, IMAGEHEIGHT), 0)
    masktopfile = Image.open(TOPMASKSOURCE).convert('L')
    masktopfilewidth, masktopfileheight = masktopfile.size
    masktop.paste(masktopfile, ((IMAGEWIDTH - masktopfilewidth) // 2, (IMAGEHEIGHT - masktopfileheight) // 2))
    masktopcanvas = ImageDraw.Draw(masktop)
    if FOREBOTTOMENABLE:
        maskbottom = Image.new("L", (IMAGEWIDTH, IMAGEHEIGHT), 0)
        maskbottomfile = Image.open(BOTTOMMASKSOURCE).convert('L')
        maskbottomfilewidth, maskbottomfileheight = maskbottomfile.size
        maskbottom.paste(maskbottomfile, ((IMAGEWIDTH - maskbottomfilewidth) // 2, (IMAGEHEIGHT - maskbottomfileheight) // 2))
        maskbottomcanvas = ImageDraw.Draw(maskbottom)

    if LINEENABLE:
        barheight = (LINESPACING * (LINECOUNT - 1)) + LINEWIDTH
        if LINEORIENTATION == 'horizontal':
            verticaloffset = int(((LINECOUNT - 1) / 2) * LINESPACING)
            centeroffset = (IMAGEWIDTH - CENTERWIDTH) // 2
            for i in range((IMAGEHEIGHT // 2) - verticaloffset, (IMAGEHEIGHT // 2) + verticaloffset + 1, LINESPACING):
                masktopcanvas.line([(IMAGEWIDTH, i), (IMAGEWIDTH - centeroffset, i)], fill=255, width=LINEWIDTH)
                if FOREBOTTOMENABLE:
                    maskbottomcanvas.line([(0, i), (centeroffset, i)], fill=255, width=LINEWIDTH)
                else:
                    masktopcanvas.line([(0, i), (centeroffset, i)], fill=255, width=LINEWIDTH)
        elif LINEORIENTATION == "vertical":
            horizontaloffset = int(((LINECOUNT - 1) / 2) * LINESPACING)
            centeroffset = (IMAGEHEIGHT - CENTERWIDTH) // 2
            for i in range((IMAGEWIDTH // 2) - horizontaloffset, (IMAGEWIDTH // 2) + horizontaloffset + 1, LINESPACING):
                masktopcanvas.line([(i, IMAGEHEIGHT), (i, IMAGEHEIGHT - centeroffset)], fill=255, width=LINEWIDTH)
                if FOREBOTTOMENABLE:
                    maskbottomcanvas.line([(i, 0), (i, centeroffset)], fill=255, width=LINEWIDTH)
                else:
                    masktopcanvas.line([(i, 0), (i, centeroffset)], fill=255, width=LINEWIDTH)
    
    imagefinal.paste(foregroundtopcolor, (0, 0), masktop)
    if FOREBOTTOMENABLE:
        imagefinal.paste(foregroundbottomcolor, (0, 0), maskbottom)
    if SAVEPARTS:
        imagefinal.save("parts/image_final.png", "PNG")

imagefinal.save(f"{OUTPUTNAME}.png", "PNG")