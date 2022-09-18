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
            if d == 0:
                break
            # 当1且Interpolated == false 的情况，循环赋值
            if Frame["Interpolated"] == "false":
                InterFrameList.append(Frame)
            else:
                FrameInsert = {}
                FrameNext = FrameList[f+1]
                for Key in Frame:
                    if(Key == "Visible")or(Key == "Interpolated"):
                        FrameInsert[Key] = Frame[Key]
                    elif(Frame[Key] == FrameNext[Key]):
                        FrameInsert[Key] = Frame[Key]
                    else:
                        if (Key == "XPosition") or (Key =="YPosition")or (Key =="XScale") or (Key =="YScale") or (Key =="RedTint") or (Key =="GreenTint") or (Key =="BlueTint") or (Key =="AlphaTint") or (Key =="RedOffset") or (Key =="GreenOffset") or (Key =="BlueOffset") or (Key =="Rotation"):
                            FrameInsert[Key] = int(Frame[Key]) + (int(FrameNext[Key])-int(Frame[Key]))/int(Frame['Delay'])
                        else:
                            FrameInsert[Key] = Frame[Key]
                InterFrameList.append(FrameInsert)

    while FrameNum > len(InterFrameList):
        InterFrameList.append(InterFrameList[-1])
    return InterFrameList

