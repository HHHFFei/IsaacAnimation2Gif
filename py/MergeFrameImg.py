# 合并图层
import cv2
from InterpolateFrame import Interpolate
from PreprocessImg import PreprocessImg

def MergeFrameImg(LayerList,LayerInfo,FrameNum):
    AnimationFrameImgList = []
    for Layer in LayerList:
        FrameList = Layer["FrameList"]
        ImgPath = "../gfx/" + LayerInfo[LayerList.index(Layer)]["Path"]
        img =  cv2.imread(ImgPath)
        FrameList = Interpolate(Layer["FrameList"],FrameNum)
        FrameImgList = PreprocessImg(FrameList,ImgPath)
        if AnimationFrameImgList == []:
            AnimationFrameImgList = FrameImgList
        else:
            for i in range(len(FrameImgList)):
                MergeImg = AnimationFrameImgList[i]
                FrameImg = FrameImgList[i]
                for x in range(FrameImg.shape[0]):
                    for y in range(FrameImg.shape[1]):
                        AlphaCannel = FrameImg[x,y][3]
                        if AlphaCannel != 0:
                            MergeImg[x,y] = FrameImg[x,y]
    return AnimationFrameImgList