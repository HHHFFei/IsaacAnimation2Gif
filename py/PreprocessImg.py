# 读取并处理帧图片
import cv2
import numpy as np

def PreprocessImg(FrameList,path):
    FrameSize = [96,96] # width,height 未来可作为参数传入或根据图片尺寸自动计算
    if FrameList == []:
        return []
    ImgFrameList = []
    Img_BGRA = cv2.imread(path,cv2.IMREAD_UNCHANGED)# 读取BGR+alpha通道
    img_RGBA = cv2.cvtColor(Img_BGRA, cv2.COLOR_BGRA2RGBA)# BGRA转RGBA
    for Frame in FrameList:
        # 如果可见性（Visible）为fales，直接输出空白图像# gif没有alpha通道，只能显示透明或不透明，无法半透明
        if(Frame["Visible"] == "false") or (Frame["AlphaTint"] < 155):
            FullfillImg = np.zeros((FrameSize[0],FrameSize[1],4), np.uint8) # 不知道后面的格式具体内容
            ImgFrameList.append(FullfillImg)
            continue
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
        AddSizeList.append(int(FrameSize[1]*2/3 + int(Frame["YPosition"]) - int(Frame["YPivot"]*Frame["YScale"]/100)))
        AddSizeList.append(int(FrameSize[1]*1/3 - int(Frame["YPosition"]) + int(Frame["YPivot"]*Frame["YScale"]/100) - int(Frame["Height"]*Frame["YScale"]/100)))
        AddSizeList.append(int(FrameSize[0]/2 + int(Frame["XPosition"]) - int(Frame["XPivot"]*Frame["XScale"]/100)))
        AddSizeList.append(int(FrameSize[0]/2 - int(Frame["XPosition"]) + int(Frame["XPivot"]*Frame["XScale"]/100) - int(Frame["Width"]*Frame["XScale"]/100)))
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
            FullfillImg = np.zeros((FrameSize[0],FrameSize[1],4), np.uint8) # 不知道后面的格式具体内容
        else:
            # # 设置色彩通道的变化。gif没有alpha通道，只能显示透明或不透明，无法半透明
            # preFullfillImg[:,:,0] = preFullfillImg[:,:,0]*Frame["RedTint"]/255
            # preFullfillImg[:,:,1] = preFullfillImg[:,:,1]*Frame["GreenTint"]/255
            # preFullfillImg[:,:,2] = preFullfillImg[:,:,2]*Frame["BlueTint"]/255
            # AddImg = np.zeros((preFullfillImg.shape[0],preFullfillImg.shape[1],4), np.uint8)
            # AddImg[:,:,0] = AddImg[:,:,0]+Frame["RedOffset"]
            # AddImg[:,:,1] = AddImg[:,:,1]+Frame["GreenOffset"]
            # AddImg[:,:,2] = AddImg[:,:,2]+Frame["BlueOffset"]
            # AddImg = cv2.add(preFullfillImg,AddImg)
            FullfillImg = cv2.copyMakeBorder(preFullfillImg, AddSizeList[0], AddSizeList[1],  AddSizeList[2],  AddSizeList[3], borderType=cv2.BORDER_CONSTANT , value=(0,0,0,0) )
        ImgFrameList.append(FullfillImg)
    return ImgFrameList