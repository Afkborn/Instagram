from PIL import Image
from hashlib import md5
def comparePictureList(picList : list, folderLoc : str, deleteSame = False):
    picMd5List = []
    for i in picList:
        im = Image.open((folderLoc + i))
        imX, imY = im.size
        imStr = ""
        for x in range(imX):
            for y in range(imY):
                R,G,B  = im.getpixel((x,y))
                imStr += f"{R}{G}{B}"
        imStr = imStr.encode("utf-8")
        md5ImStr = md5(imStr).hexdigest()
        picMd5List.append(md5ImStr)
        