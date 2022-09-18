# 读取并处理帧图片
import cv2
import numpy as np

def PreprocessImg(FrameList,path):
    if FrameList == []:
        return []
    ImgFrameList = []
    Img_BGRA = cv2.imread(path,cv2.IMREAD_UNCHANGED)# 读取BGR+alpha通道
    img_RGBA = cv2.cvtColor(Img_BGRA, cv2.COLOR_BGRA2RGBA)# BGRA转RGBA
    for Frame in FrameList:
        # 裁剪图片
        CropedImg = img_RGBA[ int(Frame['YCrop']) : (int(Frame['YCrop'])+int(Frame['Height'])) , int(Frame['XCrop']) : (int(Frame['XCrop'])+int(Frame['Width'])) ]
        # 拉伸变换
        NewWidth = int(int(Frame['XScale'])*int(Frame['Width'])/100)
        NewHeight =  int(int(Frame['YScale'])*int(Frame['Height'])/100)
        # !如果是负说明要发生翻转，然后再变为正数进行缩放，否则会报错
        if NewWidth < 0:
            CropedImg = cv2.flip(CropedImg, 1)
            NewWidth = -NewWidth
            Frame['XScale'] = -Frame['XScale']
        if NewHeight < 0:
            CropedImg = cv2.flip(CropedImg, 0)
            NewHeight = -NewHeight
            Frame['YScale'] = -Frame['YScale']
        NewSize =  (NewWidth,NewHeight)
        ResizedImg = cv2.resize(CropedImg,NewSize,interpolation=cv2.INTER_NEAREST)
        # 根据画布重新裁剪或扩充画面
        AddSizeList = []
        AddSizeList.append(46 + int(Frame["YPosition"]) - int(Frame["YPivot"]*Frame["YScale"]/100))
        AddSizeList.append(18 - int(Frame["YPosition"]) + int(Frame["YPivot"]*Frame["YScale"]/100) - int(Frame["Height"]*Frame["YScale"]/100))
        AddSizeList.append(32 + int(Frame["XPosition"]) - int(Frame["XPivot"]*Frame["XScale"]/100))
        AddSizeList.append(32 - int(Frame["XPosition"]) + int(Frame["XPivot"]*Frame["XScale"]/100) - int(Frame["Width"]*Frame["XScale"]/100))
        CropSizeList = []
        for i in range(len(AddSizeList)):
            AddSize = AddSizeList[i]
            if AddSize < 0:
                CropSizeList.append(int(-AddSize))
                AddSizeList[i] = 0
            else:
                CropSizeList.append(int(0))
        ImgSize = ResizedImg.shape
        preFullfillImg = ResizedImg[ CropSizeList[0] : ImgSize[0]-CropSizeList[1] , CropSizeList[2] : ImgSize[1]-CropSizeList[3] ]
        # 可能裁剪后图片的宽或者高为0，此时直接返回一张空白图片，否则继续执行会报错（好像裁剪后为负数会自动变为0）
        if preFullfillImg.size == 0:
            FullfillImg = np.zeros((400,400,4), np.uint8) # 不知道后面的格式具体内容
        else:
            FullfillImg = cv2.copyMakeBorder(preFullfillImg, AddSizeList[0], AddSizeList[1],  AddSizeList[2],  AddSizeList[3], borderType=cv2.BORDER_REPLICATE)
        ImgFrameList.append(FullfillImg)
    return ImgFrameList