# isaacAnimation2Gif
Decode The Binding of Isaac animation files ( .anm2 and .png ) .Composit animations (.gif and maybe .mp4)  
解析以撒的结合动画文件（.anm2和.png），合成动画（.gif和可能.mp4）

---

## 结果演示
![Pickup](https://github.com/hhhhfff/IsaacAnimation2Gif/blob/main/result/001.000_player/Pickup.gif)
![DeathTeleport](https://github.com/hhhhfff/IsaacAnimation2Gif/blob/main/result/001.000_player/DeathTeleport.gif)
![Jump](https://github.com/hhhhfff/IsaacAnimation2Gif/blob/main/result/001.000_player/Jump.gif)
![Happy](https://github.com/hhhhfff/IsaacAnimation2Gif/blob/main/result/001.000_player/Happy.gif)
![Sad](https://github.com/hhhhfff/IsaacAnimation2Gif/blob/main/result/001.000_player/Sad.gif)
![Hit](https://github.com/hhhhfff/IsaacAnimation2Gif/blob/main/result/001.000_player/Hit.gif)  
  
![Appear](https://github.com/hhhhfff/IsaacAnimation2Gif/blob/main/result/908.000_baby%20plum/Appear.gif)
![Attack2](https://github.com/hhhhfff/IsaacAnimation2Gif/blob/main/result/908.000_baby%20plum/Attack1.gif)
![Attack2](https://github.com/hhhhfff/IsaacAnimation2Gif/blob/main/result/908.000_baby%20plum/Attack2.gif)
![Idle](https://github.com/hhhhfff/IsaacAnimation2Gif/blob/main/result/908.000_baby%20plum/Idle.gif)
![Leave](https://github.com/hhhhfff/IsaacAnimation2Gif/tree/main/result/908.000_baby%20plum/Leave.gif)

---

## 代码说明
Python 3.10.7
代码放在**py**文件夹中  
主要是用的juypternotebook写的，但是感觉.ipynb不太方便版本控制，后面还是转成了python  
主文件是`IsaacAnimationEditor.py`   
转换所用到的.anm2 和 .png文件在**gfx**文件夹中，为了方便只上传了三个动画文件（以撒、梅糖宝宝、教条）。
转换的结果保存在**result**中，文件名为对应的动画名  
> 如果在steam中下载了以撒的结合，可以在`\steamapps\common\The Binding of Isaac Rebirth\resources\gfx` 中找到更多动画文件和图片。另外，`H:\Steam\steamapps\common\The Binding of Isaac Rebirth\tools\IsaacAnimationEditor\IsaacAnimationEditor.exe` 为官方的动画工具，可能是用来进行mod开发的，但是我似乎没找到导出gif或者mp4文件的地方。

### 1. 解析XML文件  
.am2文件其实是.xml文件，因此可以用解析XML文件的方法来解析该文件  

#### 1.1. 获取XML文件树
通过XML.DOM解析文件，获取该文件包含的数据树，返回根节点
```PYTHON
DecodeXML(file)
# 输入：XML文件路径  
# 输出：xml.dom的树状结构的根节点  
return DOMTreeRoot
```

#### 1.2. 获取动画信息
`<Info ...... />`中保存了该动画的一些信息，如作者、时间、帧率、版本等  
`<Spritesheets>...</Spritesheets>`中保存了将会使用的图片  
`<Layer>...</Layer>`保存了各图层的一些信息，如该层使用的图片、图层名、Id  
```PYTHON
GetAnimationInfo(DOMTreeRoot)
# 输入：xml.dom的树状结构的根节点  
# 输出：包含动画文件信息的字典
return AnimationInfo =
   {'Fps': '30', 'Version': '153', 'LayerInfo':
      [{'Id': '0', 'Name': 'glow', 'Path': 'characters/costumes/Character_001_Isaac.png'},
      {'Id': '1', 'Name': 'body', 'Path': 'characters/costumes/Character_001_Isaac.png'},
      ...
      {'Id': '14', 'Name': 'back', 'Path': 'characters/costumes/Character_001_Isaac.png'}
   ]}
```

#### 1.3. 获取动画帧信息
根据.anm2文件的层次结构，逐层解析，得到帧信息，可参考下文的return示例  
.anm2 文件框架  中对层次结构进行了一些分析，可供参考
```PYTHON
GetAnimationFrame(DOMTreeRoot) 
# 输入：xml.dom的树状结构的根节点
# 输出：包含动画帧信息的列表。帧信息包含在帧中，所有帧包含在关键帧列表中，关键帧列表是图层的一个元素，图层包含在图层列表中，图层列表是动画的一个元素，动画包含在动画列表中。
return AnimaitionList = 
   [{'Name': 'Pickup', 'FrameNum': '42', 'LayerAnimationList': [
      {'LayerId': '0', 'Visible': 'true', 'FrameList': []}
      {'LayerId': '1', 'Visible': 'true', 'FrameList': []}
      ...
      {'LayerId': '12', 'Visible': 'true', 'FrameList': [
         {'XPosition': '0', 'YPosition': '0', 'XPivot': '32', 'YPivot': '56', 'XCrop': '0', ... , 'Interpolated': 'true'}
         {'XPosition': '0', 'YPosition': '2', 'XPivot': '32', 'YPivot': '56', 'XCrop': '64', ... , 'Interpolated': 'true'}
         ...
      ]}
      {'LayerId': '14', 'Visible': 'true', 'FrameList': []}
   ]}, 
   {'Name': 'Hit', 'FrameNum': '8', 'LayerAnimationList': []},
   ...
   {'Name': 'DeathTeleport', 'FrameNum': '21', 'LayerAnimationList': []}]
```

### 2. 插入过度帧
.anm2中只记录了关键帧的信息，如果Frame中Delay的值大于1，说明需要插入过度帧  
Interpolated属性说明了插入帧的方法，如果值为false，则只需要将关键帧的内容复制到过度帧中 。如果值为true，则需要根据下一个关键帧中的属性的值计算过度帧中的属性值。  
* 某些属性不进行插值处理，如Position、Scale、Tint、ColorOffset、colorRotation等值，直接复制关键帧中的值  
* 某些图层虽然有关键帧但进行插值处理后的长度仍小于定义的帧长度，这说明剩余的帧中该图层的画面一直保持静止。因此需要将最后一帧的画面填充至剩下的所有空帧中
```PYTHON
Interpolate(FrameList,FrameNum)
# 输入：关键帧列表，帧长度（数量）
# 输出：插值后的帧列表`
return InterFrameList
```

### 3. 处理帧图片
根据读取图片，帧中的各属性值处理图片，得到图片列表  
```PYTHON
PreprocessImg(FrameList,path)
# 输入：帧列表，图像路径
# 输出：帧图像列表
return ImgFrameList
```

### 4. 合并图层图像
一个动画中是由多个图层中的图像堆叠形成的，因此需要将不同图层的图片列表进行堆叠合并。
对图层列表中的所有帧列表调用**插入过度帧** 、**处理帧图片** 得到包含所有帧图片列表的图层图片列表
依次将各帧图片列表（FrameList）堆叠到合并图片列表（AnimationFrameImgList）中
```PYTHON
MergeFrameImg(LayerList,LayerInfo,FrameNum)
# 输入：图层列表，图层信息，帧长度
# 输出：合并后的帧图片列表
return AnimationFrameImgList
```

### 5. 合成动画
将png图片列表合成gif动画文件  
分别尝试了用imageio和pic两个图像库进行合成。
目前只有用pic能够成功合成透明背景的gif，所以imageio就先不要用了。但是我也没删

---

## 待解决的问题（按严重性和解决时间排序）
1. 某些动画的不同图层之间出现了错位（如Dogma angel）  
2. 颜色属性的计算  
3. 循环生成多个动画时，只输出最后一个  
4. 无法选择动画文件以及动画  
5. 某些代码效率很低，需要改进  
6. 有的动画是由多个文件合成的，如Bethany其实是以撒的的动画再加上Bethany头发的动画，因此还需要把多个动画合并起来  
7. ~~画面也有问题，某些动画的画面被拉伸到了画面边界（如Glitch），应该是`PreprocessImg()`中的`cv2.copyMakeBorder` 某些参数的问题~~（20220920修正）  
8. ~~有的值是整型，有的值是浮点型，有的值是字符串，还需要整理一下~~（20220920修正）  
9. ~~动画帧似乎有问题，走路的动画可以明显地看出中间有一段不动。可能是`Interpolate()`中的问题~~（20220919修正）  

---

## 更新日志
### 20220921
本来想根据AlphaTint的值实现某些动画的透明度变化，试了很久都不行。原来gif没有alpha通道，只支持透明或者不透明。之后再想想怎么解决这个问题  	
~~添加对于颜色通道属性的解析：其中 `Color = Color * ColorTint` ； `Color = min( (Color + ColorOffset) , 255 )` （修改颜色通道搞死我了）~~  正准备提交的时候发现并没有写好，一堆bug  
修改了边界被拉伸的错误

### 20220920
修改了README中的一些错误
修改了插值错误的bug
学会了在vs中的jupyternotebook添加断点调试的方法
添加了对于visable属性的解析

### 20220919
整理代码
创建仓库，将代码上传到Github仓库中

### 20220918
完成了根据帧信息处理图片的方法。对图片进行各种变形各种处理，确定图片在画面中的位置。很多地方需要特殊判断否则会有意外的错误。  
合成出来了第一个动画。用的pic的方法，可以合成透明背景的gif。  
各种调整，比如插值方法，比如帧率等等。  
完成合并图层的代码。  
更换测试案例，改BUG。  

### 20220917
添加了获取动画文件额外信息（帧率、图片路径等）的函数  
遇到了一个坑：Info、Content这些虽然只有一个，但是调用getElementsByTagName("Info")返回的还是一个列表，所以还是要用for循环依次取里面的值.  

### 20220916
重构了代码，把所有动画都装进了一个AnimationList里。
完成了插帧的函数    

### 20220915
尝试合成带透明通道的图片，失败。但是导出了透明背景的png图像  
试图重构代码，失败  
突然发现delay不只是简单的延迟图像，某些变化的属性还要计算中间值。  
于是尝试插帧，完成了一半。主要是有些不该算的值，比如visible也被计算了  

### 20220914
读取图片，根据属性处理图片，生成关键帧图片和gif  
但是关键帧图片不透明  
gif由于图片尺寸不统一也不正常  

### 20220913
突发奇想，打算搞这个
配置python、juypternotebook环境  
了解 xml.dom  
尝试生成XML文件的树状数据结构  

---

## .anm2 文件框架
```xml
<Animations DefaultAnimation="WalkDown">
	<Animation Name="Pickup" FrameNum="42" Loop="false">
		<RootAnimation>
			<Frame XPosition="0" YPosition="0" Delay="42" Visible="true" XScale="100" YScale="100" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="false" />
		</RootAnimation>
		<LayerAnimations>
			<LayerAnimation LayerId="0" Visible="true" />
			<LayerAnimation LayerId="1" Visible="true" />
			<LayerAnimation LayerId="2" Visible="true" />
			<LayerAnimation LayerId="3" Visible="true" />
			<LayerAnimation LayerId="4" Visible="true" />
			<LayerAnimation LayerId="5" Visible="true" />
			<LayerAnimation LayerId="6" Visible="true" />
			<LayerAnimation LayerId="7" Visible="true" />
			<LayerAnimation LayerId="8" Visible="true" />
			<LayerAnimation LayerId="9" Visible="true" />
			<LayerAnimation LayerId="10" Visible="true" />
			<LayerAnimation LayerId="11" Visible="true" />
			<LayerAnimation LayerId="12" Visible="true" />
			<LayerAnimation LayerId="13" Visible="true" />
			<LayerAnimation LayerId="14" Visible="true" />
		</LayerAnimations>
		<NullAnimations>
			<NullAnimation NullId="0" Visible="true" />
			<NullAnimation NullId="1" Visible="true" />
			<NullAnimation NullId="2" Visible="true" />
			<NullAnimation NullId="3" Visible="true" />
			<NullAnimation NullId="4" Visible="true" />
			<NullAnimation NullId="5" Visible="true" />
			<NullAnimation NullId="6" Visible="true" />
			<NullAnimation NullId="7" Visible="true" />
			</NullAnimation>
		</NullAnimations>
		<Triggers />
	</Animation>
</Animation>
```

```XML
<Animations DefaultAnimation="WalkDown"></Animation>
```
设置默认动画为WalkDown


```XML
<Animation Name="Pickup" FrameNum="42" Loop="false"></Animation>
```
当前动画为Pickup，共42帧，不循环


### 1. 根动画 RootAnimation
```XML
		<RootAnimation>
			<Frame XPosition="0" YPosition="0" Delay="42" Visible="true" XScale="100" YScale="100" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="false" />
		</RootAnimation>
```

#### 1.1. 帧 Frame
```XML
			<Frame XPosition="0" YPosition="0" Delay="42" Visible="true" XScale="100" YScale="100" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="false" />
```
帧位置为 (0,0)；延迟？42；可见性为可见；缩放为 (0,0)；红绿蓝α色调为 (255,255,255,255)；红绿蓝偏移为 (0,0,0)；旋转为 0；插值为0；

### 2. 层动画组 LayerAnimations
```XML
<LayerAnimations>
			<LayerAnimation LayerId="0" Visible="true" />
			...
			<LayerAnimation LayerId="14" Visible="true" />
		</LayerAnimations>
```

#### 2.1. 层动画 LayerAnimation
```XML
			<LayerAnimation LayerId="12" Visible="true">
				<Frame XPosition="0" YPosition="0" XPivot="32" YPivot="56" XCrop="0"  YCrop="192" Width="64" Height="64" XScale="130" YScale="70"  Delay="2"  Visible="true" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="true"  />
				...
			</LayerAnimation>
```

##### 2.1.1 层动画帧 Frame
```XML
				<Frame XPosition="0" YPosition="0" XPivot="32" YPivot="56" XCrop="0"  YCrop="192" Width="64" Height="64" XScale="130" YScale="70"  Delay="2"  Visible="true" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="true"  />
```
1. XPosition="0" YPosition="0" 
位置，图像的原点在画面帧中的位置

2. XPivot="32" YPivot="56" 
中心点，图像的中心点在图像中的位置，以裁剪的图像左上角为 (0,0)

3. XCrop="0"  YCrop="192" 
裁切，从png文件中裁剪的图像的位置

4. Width="64" Height="64" 
尺寸，从png文件中裁剪的图像的大小，左上角为 (0,0)

5. XScale="130" YScale="70"  
缩放，图像在画面帧中以原点为中心的缩放，正常值为（100,100）

6. Delay="2"  
延迟，图像持续的帧长度

7. Visible="true" 
可见性

8. RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" 
淡色值（红绿蓝α）
改变图像的原点在画面帧中的颜色通道，正常值为 (255,255,255,255)

9. RedOffset="0" GreenOffset="0" BlueOffset="0" 
颜色偏移（红绿蓝）

10. Rotation="0" 
旋转

11. Interpolated="true"  
插值

> 某些属性在当插值Interpolated属性为true时，需要在后续的过渡帧中计算插值。其余不用插值的属性只需要与关键帧中的值相等即可
> 需要插值：Pivot、Scale、Position、ColorTint、colorOffset、Rotation
> 不用插值：Crop、Size、Delay、Visible、Interpolated


### 3. 零动画组 NullAnimations
```XML
		<NullAnimations>
			<NullAnimation NullId="0" Visible="true" />
			...
			<NullAnimation NullId="7" Visible="true" />
			</NullAnimation>
		</NullAnimations>
```
类似于空物体动画，用于后期绑定其他物品。如Pickup举起动作时，利用空物体动画确定各帧中物品的位置，使用该动画时将对应的Pickup物品绑定于空物体上即可让物品跟随动画在对应的位置运动。

### 4. 触发器 Triggers
```XML
		<Triggers />
```
用于触发其他事件，如死亡后在特定帧触发死亡音效

---

## 示例代码
```xml
<AnimatedActor>
	<Info CreatedBy="robot" CreatedOn="09.28.2020 18:50:13" Fps="30" Version="153" />
	<Content>
		<Spritesheets>
			<Spritesheet Id="0" Path="characters/costumes/Character_001_Isaac.png" />
			<Spritesheet Id="1" Path="Characters/costumes/ghost.png" />
		</Spritesheets>
		<Layers>
			<Layer Id="0" Name="glow" SpritesheetId="0" />
			<Layer Id="1" Name="body" SpritesheetId="0" />
			<Layer Id="2" Name="body0" SpritesheetId="0" />
			<Layer Id="3" Name="body1" SpritesheetId="0" />
			<Layer Id="4" Name="head" SpritesheetId="0" />
			<Layer Id="5" Name="head0" SpritesheetId="0" />
			<Layer Id="6" Name="head1" SpritesheetId="0" />
			<Layer Id="7" Name="head2" SpritesheetId="0" />
			<Layer Id="8" Name="head3" SpritesheetId="0" />
			<Layer Id="9" Name="head4" SpritesheetId="0" />
			<Layer Id="10" Name="head5" SpritesheetId="0" />
			<Layer Id="11" Name="top0" SpritesheetId="0" />
			<Layer Id="12" Name="extra" SpritesheetId="0" />
			<Layer Id="13" Name="ghost" SpritesheetId="1" />
			<Layer Id="14" Name="back" SpritesheetId="0" />
		</Layers>
		<Nulls>
			<Null Id="0" Name="pickup item" />
			<Null Id="1" Name="LeftEye" />
			<Null Id="2" Name="RightEye" />
			<Null Id="3" Name="Forehead" />
			<Null Id="4" Name="Mouth" />
			<Null Id="5" Name="MomsEye" />
			<Null Id="6" Name="Tractor" />
			<Null Id="7" Name="ItemWalk" />
		</Nulls>
		<Events>
			<Event Id="0" Name="FX" />
			<Event Id="1" Name="Poof" />
			<Event Id="2" Name="DeathSound" />
			<Event Id="3" Name="Hit" />
		</Events>
	</Content>
	<Animations DefaultAnimation="WalkDown">
		<Animation Name="Pickup" FrameNum="42" Loop="false">
			<RootAnimation>
				<Frame XPosition="0" YPosition="0" Delay="42" Visible="true" XScale="100" YScale="100" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="false" />
			</RootAnimation>
			<LayerAnimations>
				<LayerAnimation LayerId="0" Visible="true" />
				<LayerAnimation LayerId="1" Visible="true" />
				<LayerAnimation LayerId="2" Visible="true" />
				<LayerAnimation LayerId="3" Visible="true" />
				<LayerAnimation LayerId="4" Visible="true" />
				<LayerAnimation LayerId="5" Visible="true" />
				<LayerAnimation LayerId="6" Visible="true" />
				<LayerAnimation LayerId="7" Visible="true" />
				<LayerAnimation LayerId="8" Visible="true" />
				<LayerAnimation LayerId="9" Visible="true" />
				<LayerAnimation LayerId="10" Visible="true" />
				<LayerAnimation LayerId="11" Visible="true" />
				<LayerAnimation LayerId="12" Visible="true">
					<Frame XPosition="0" YPosition="0" XPivot="32" YPivot="56" XCrop="0"  YCrop="192" Width="64" Height="64" XScale="130" YScale="70"  Delay="2"  Visible="true" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="true"  />
					<Frame XPosition="0" YPosition="2" XPivot="32" YPivot="56" XCrop="64" YCrop="192" Width="64" Height="64" XScale="60"  YScale="140" Delay="2"  Visible="true" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="true"  />
					<Frame XPosition="0" YPosition="2" XPivot="32" YPivot="56" XCrop="64" YCrop="192" Width="64" Height="64" XScale="130" YScale="70"  Delay="2"  Visible="true" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="true"  />
					<Frame XPosition="0" YPosition="1" XPivot="32" YPivot="56" XCrop="64" YCrop="192" Width="64" Height="64" XScale="90"  YScale="110" Delay="2"  Visible="true" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="true"  />
					<Frame XPosition="0" YPosition="1" XPivot="32" YPivot="56" XCrop="64" YCrop="192" Width="64" Height="64" XScale="100" YScale="100" Delay="27" Visible="true" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="false" />
					<Frame XPosition="0" YPosition="2" XPivot="32" YPivot="56" XCrop="64" YCrop="192" Width="64" Height="64" XScale="80"  YScale="120" Delay="2"  Visible="true" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="true"  />
					<Frame XPosition="0" YPosition="2" XPivot="32" YPivot="56" XCrop="0"  YCrop="192" Width="64" Height="64" XScale="110" YScale="90"  Delay="2"  Visible="true" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="true"  />
					<Frame XPosition="0" YPosition="1" XPivot="32" YPivot="56" XCrop="0"  YCrop="192" Width="64" Height="64" XScale="94"  YScale="106" Delay="2"  Visible="true" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="true"  />
					<Frame XPosition="0" YPosition="1" XPivot="32" YPivot="56" XCrop="0"  YCrop="192" Width="64" Height="64" XScale="100" YScale="100" Delay="1"  Visible="true" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="false" />
				</LayerAnimation>
				<LayerAnimation LayerId="13" Visible="true" />
				<LayerAnimation LayerId="14" Visible="true" />
			</LayerAnimations>
			<NullAnimations>
				<NullAnimation NullId="0" Visible="true">
					<Frame XPosition="0" YPosition="-10" Delay="2"  Visible="false" XScale="100" YScale="100" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="true"  />
					<Frame XPosition="0" YPosition="-26" Delay="2"  Visible="true"  XScale="100" YScale="100" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="true"  />
					<Frame XPosition="0" YPosition="-14" Delay="2"  Visible="true"  XScale="100" YScale="100" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="true"  />
					<Frame XPosition="0" YPosition="-28" Delay="2"  Visible="true"  XScale="100" YScale="100" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="true"  />
					<Frame XPosition="0" YPosition="-25" Delay="27" Visible="true"  XScale="100" YScale="100" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="false" />
					<Frame XPosition="0" YPosition="-23" Delay="2"  Visible="true"  XScale="100" YScale="100" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="true"  />
					<Frame XPosition="0" YPosition="-10" Delay="2"  Visible="false" XScale="100" YScale="100" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="true"  />
					<Frame XPosition="0" YPosition="-10" Delay="2"  Visible="false" XScale="100" YScale="100" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="true"  />
					<Frame XPosition="0" YPosition="-10" Delay="1"  Visible="false" XScale="100" YScale="100" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="false" />
				</NullAnimation>
				<NullAnimation NullId="1" Visible="true" />
				<NullAnimation NullId="2" Visible="true" />
				<NullAnimation NullId="3" Visible="true" />
				<NullAnimation NullId="4" Visible="true" />
				<NullAnimation NullId="5" Visible="true" />
				<NullAnimation NullId="6" Visible="true" />
				<NullAnimation NullId="7" Visible="true">
					<Frame XPosition="0" YPosition="0" Delay="2"  Visible="true" XScale="130" YScale="70"  RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="true"  />
					<Frame XPosition="0" YPosition="2" Delay="2"  Visible="true" XScale="60"  YScale="140" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="true"  />
					<Frame XPosition="0" YPosition="2" Delay="2"  Visible="true" XScale="130" YScale="70"  RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="true"  />
					<Frame XPosition="0" YPosition="1" Delay="2"  Visible="true" XScale="90"  YScale="110" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="true"  />
					<Frame XPosition="0" YPosition="1" Delay="27" Visible="true" XScale="100" YScale="100" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="false" />
					<Frame XPosition="0" YPosition="2" Delay="2"  Visible="true" XScale="80"  YScale="120" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="true"  />
					<Frame XPosition="0" YPosition="2" Delay="2"  Visible="true" XScale="110" YScale="90"  RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="true"  />
					<Frame XPosition="0" YPosition="1" Delay="2"  Visible="true" XScale="94"  YScale="106" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="true"  />
					<Frame XPosition="0" YPosition="1" Delay="1"  Visible="true" XScale="100" YScale="100" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="false" />
				</NullAnimation>
			</NullAnimations>
			<Triggers />
		</Animation>
	</Animation>
</AnimatedActor>
```