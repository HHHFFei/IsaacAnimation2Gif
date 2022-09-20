from DecodeXML2List import DecodeXML,GetAnimationInfo,GetAnimationFrame
from MergeFrameImg import MergeFrameImg
from ImgList2GIF import png_gif_pic

AnimationPath = "../gfx/001.000_player.anm2"
DOMTreeRoot = DecodeXML(AnimationPath)

AnimationInfo = GetAnimationInfo(DOMTreeRoot)
AnimaitionList = GetAnimationFrame(DOMTreeRoot)

for Animation in AnimaitionList:
# Animation = AnimaitionList[3]
    AnimationName = Animation["Name"]
    print(AnimaitionList.index(Animation) , AnimationName)
    LayerList = Animation["LayerAnimationList"]
    LayerInfo = AnimationInfo["LayerInfo"]
    FrameNum = Animation["FrameNum"]
    AnimationFrameImgList = MergeFrameImg(LayerList,LayerInfo,FrameNum)

png_gif_pic(AnimationFrameImgList,AnimationName)
