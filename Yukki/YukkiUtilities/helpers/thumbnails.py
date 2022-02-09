import os
from os import path
import aiohttp
import aiofiles
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


async def gen_thumb(thumbnail, title, userid, theme, ctitle):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open(f"search/thumb{userid}.jpg", mode="wb")
                await f.write(await resp.read())
                await f.close()
    image1 = Image.open(f"search/thumb{userid}.jpg")
    image2 = Image.open(f"cache/{theme}.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save(f"search/temp{userid}.png")
    img = Image.open(f"search/temp{userid}.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("cache/regular.ttf", 50)
    font2 = ImageFont.truetype("cache/medium.ttf", 72)
    draw.text((27, 543), f"Playing on {ctitle[:12]}", fill="black", font=font)
    draw.text((25, 615), f"{title[:20]}...", fill= "black", font=font2)
    img.save(f"search/final{userid}.png")
    os.remove(f"search/temp{userid}.png")
    os.remove(f"search/thumb{userid}.jpg") 
    final = f"search/final{userid}.png"
    return final


async def down_thumb(thumbnail, userid):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open(f"search/thumb{userid}.jpg", mode="wb")
                await f.write(await resp.read())
                await f.close()
    final = f"search/thumb{userid}.jpg"
    return final
