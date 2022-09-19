# 处理帧内容，主要是插帧
# 对于Delay > 1且Interpolated = true的关键帧，其中一些值如果相对于下一个关键帧发生了变化，需要均匀分布在中间帧
# 需要插值的值：Position、Scale、ColorTint、ColorOffset、Rotation
def Interpolate(FrameList,FrameNum):
    # 如果没有关键帧，就退出，要不然要出大问题
    if FrameList == []:
        return []
    InterFrameList = []
    for f in range(len(FrameList)):
        Frame = FrameList[f]
        InterFrameList.append(Frame)
        # 当Delay == 1的情况：直接跳过循环。顺便就可以把最后一个关键帧跳过了
        for d in range(Frame["Delay"]-1):
            if d < 0:
                break
            # 当Interpolated == false或没有下一个关键帧（f>=len(FrameList)），直接将关键帧的值赋值给过渡帧
            if (Frame["Interpolated"] == "false")or(f>=len(FrameList)-1):
                InterFrameList.append(Frame)
            else:
                FrameInsert = {}
                FrameNext = FrameList[f+1]
                for Key in Frame:
                    if(Key == "Visible")or(Key == "Interpolated")or(Key == "XCrop")or(Key == "YCrop")or(Key == "Width")or(Key == "Height")or(Key == "Delay"):
                        FrameInsert[Key] = Frame[Key]
                    elif(Frame[Key] == FrameNext[Key]):
                        FrameInsert[Key] = Frame[Key]
                    else:
                        FrameInsert[Key] = int(Frame[Key]) + (int(FrameNext[Key])-int(Frame[Key]))/int(Frame['Delay'])
                InterFrameList.append(FrameInsert)

    while FrameNum > len(InterFrameList):
        InterFrameList.append(InterFrameList[-1])
    return InterFrameList