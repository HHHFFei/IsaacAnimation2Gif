# 合成gif动图
import imageio
import os
import sys
def png_gif_imageio(path,ImgList):
    png_lst = os.listdir(path)
    imageio.mimsave("result_imgeio.gif", ImgList, 'GIF', duration=1/12)

from PIL import Image
import os
def png_gif_pic(ImgList,FileName):
    PicImgList = []

    for CV2Img in ImgList: 
        PicImg = Image.fromarray(CV2Img) # numpy 转 image类
        PicImgList.append(PicImg)
    PicImgList[0].save("../result/" + FileName+".gif", save_all=True, append_images=PicImgList[1:],duration=18,transparency=0,loop=0,disposal=2)