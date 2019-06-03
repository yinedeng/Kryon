import numpy as np
import cv2
import sys

#----------------------------并行流水线法 FPGA Parallel Pipeline Method----------------------------
img = cv2.imread(sys.argv[1])
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ExampleImage = np.array(gray)      #重新加载示例图片. Load example image again

for y in range(0, gray.shape[0]):
    for x in range(0, gray.shape[1]):
        if ExampleImage[y, x] < 200: 
            ExampleImage[y, x] = 255 
        else:
            ExampleImage[y, x] = 0

LabelCount = 1  #标记数组初值为0,所以标记不能为从0开始. Can not be Zero, because init value of LabelArray is 0
LabelArray = np.zeros((ExampleImage.shape[0], ExampleImage.shape[1]), np.int8) #新建一个用来存放标记值的数组. New array for storing labels
ShapeInfoList = [[0, [0, 0], [0, 0],0,0]] #[Sum, [Xmax,Ymax],[Xmin,Ymin], RealLabel, XLmax]
Sum, XYmax, XYmin, RealLabel, XLmax  = 0, 1, 2, 3, 4

def LabelThisDot(x, y, ShapeInfo):
    LabelArray[y, x] = ShapeInfo[RealLabel]            #在标记数组上做标记. Label this dot in Label Array
    ShapeInfo[Sum] += 1                                #统计信息. Get Statistics  [Sum, [Xmax,Ymax],[Xmin,Ymin], color]
    ShapeInfo[XYmax][0] = max(ShapeInfo[XYmax][0], x)
    ShapeInfo[XYmax][1] = max(ShapeInfo[XYmax][1], y)
    ShapeInfo[XYmin][0] = min(ShapeInfo[XYmin][0], x)
    ShapeInfo[XYmin][1] = min(ShapeInfo[XYmin][1], y)
    ShapeInfo[XLmax] = x                               #记录该行的x最大值,用于判断形状结束 Use this value to tell if a shape's labeling has been completed

for y in range(1, gray.shape[0] - 1):
    for x in range(1, gray.shape[1] - 1):
        if ExampleImage[y, x] == 0:  #black dot
            Left, UpLeft, Up, UpRight = LabelArray[y, x - 1], LabelArray[y - 1, x - 1], LabelArray[y - 1, x], LabelArray[y - 1, x + 1]  #左,左上,上,右上四点 4 dots: Left, Left Up, Up, Up Right
            Left, UpLeft, Up, UpRight = ShapeInfoList[Left][RealLabel], ShapeInfoList[UpLeft][RealLabel], ShapeInfoList[Up][RealLabel], ShapeInfoList[UpRight][RealLabel]
            NumOfLabeled = int(bool(Left)) + int(bool(UpLeft)) + int(bool(Up)) + int(bool(UpRight))  #统计这4点中有几个点是已经被标记了的. How many have already been Labeled in these 4 dots

            if NumOfLabeled == 0:
                ShapeInfo = [0, [x, y], [x, y], LabelCount, x]
                LabelThisDot(x, y, ShapeInfo)
                ShapeInfoList.append(ShapeInfo)
               #AddClip(bg_image, x, y, Neighbourhood3x3, LabelColor = ShapeInfo[Color], duration =ScanTime,
               #        注释1="黑点就来分析\nAnalise black dot\nNew Start Dot!",
               #        注释2="新黑点,周围没有已标记点\n用新标号标上\nNo Labeled dot around\nTag it with new Label: {}\n"
               #              "总点数Total Num of dots: {}\nXYmax: {} XYmin: {}".format(LabelCount, ShapeInfo[Sum], tuple(ShapeInfo[XYmax]), tuple(ShapeInfo[XYmin])))
                LabelCount += 1

            elif ((Left != UpRight and Left > 0) or (UpLeft != UpRight and UpLeft > 0)) and UpRight > 0:  #Two different labeled dot around
                ShapeInfoLater = ShapeInfoList[UpRight]
                ShapeInfo = []
                if Left != UpRight and  Left > 0:
                    ShapeInfoList[UpRight][RealLabel] = ShapeInfoList[Left][RealLabel]
                    ShapeInfo = ShapeInfoList[Left]
                else:
                    ShapeInfoList[UpRight][RealLabel] = ShapeInfoList[UpLeft][RealLabel]
                    ShapeInfo = ShapeInfoList[UpLeft]

                ShapeInfo[Sum] += ShapeInfoLater[Sum]                                      #当一个黑点的左上4邻域中有两个标号不同的标记点时,就要把后面的标号改为前面的标号,
                ShapeInfo[XYmax][0] = max(ShapeInfo[XYmax][0], ShapeInfoLater[XYmax][0])   #并合把后面的数据合并到前面去
                ShapeInfo[XYmax][1] = max(ShapeInfo[XYmax][1], ShapeInfoLater[XYmax][1])   #When there are Two different labeled dot around a black dot, it needs to change later Label to formal Label,
                ShapeInfo[XYmin][0] = min(ShapeInfo[XYmin][0], ShapeInfoLater[XYmin][0])   #and combine later data to formal ones. This is a Key Step.
                ShapeInfo[XYmin][1] = min(ShapeInfo[XYmin][1], ShapeInfoLater[XYmin][1])
                ShapeInfo[XLmax]    = max(ShapeInfo[XLmax], ShapeInfoLater[XLmax])
                LabelThisDot(x, y, ShapeInfo)
               #AddClip(bg_image, x, y, Neighbourhood3x3, LabelColor = ShapeInfo[Color], diff = True,
               #        duration=ScanTime,
               #        注释1="黑点就来分析\nAnalise black dot",
               #        注释2="周围有两个标号不同的已标记点\n需把后面的标号映射到前面的标号\n把统计数据也合并过去\n并把这个点标上前面的标号\n"
               #              "Two Labeled dot around\nNeeds map later label to\nprevious one and combine data\nand Tag it with pre label: {}\n"
               #              "总点数Total Num of dots: {}\nXYmax: {} XYmin: {}".format(ShapeInfo[RealLabel],ShapeInfo[Sum], tuple(ShapeInfo[XYmax]), tuple(ShapeInfo[XYmin])))

            else:  #Only One Label value around
                if Left != 0:     ShapeInfo = ShapeInfoList[Left]
                elif UpLeft != 0: ShapeInfo = ShapeInfoList[UpLeft]
                elif Up != 0:     ShapeInfo = ShapeInfoList[Up]
                else:             ShapeInfo = ShapeInfoList[UpRight]
                LabelThisDot(x, y, ShapeInfo)
               #AddClip(bg_image, x, y, Neighbourhood3x3, LabelColor = ShapeInfo[Color], duration= ScanTime,
               #        注释1="黑点就来分析\nAnalise black dot",
               #        注释2="该黑点周围只有一种已标标号\n用该标号标上\nOnly One Label value around\nTag it with this Label: {}\n"
               #              "总点数Total Num of dots: {}\nXYmax: {} XYmin: {}".format(ShapeInfo[RealLabel], ShapeInfo[Sum], tuple(ShapeInfo[XYmax]), tuple(ShapeInfo[XYmin])))

        else:  #white dot
            if ExampleImage[y, x - 1] == ExampleImage[y, x + 1] == ExampleImage[y - 1, x + 1] == 255 and ExampleImage[y - 1, x] == 0:   #该白点的左右两边和右上也是白点,上方不是白点. Left, right and up right dots are white too, and not white on top
                ShapeInfo = ShapeInfoList[ShapeInfoList[LabelArray[y - 1, x]][RealLabel]]  #取出正上方点的信息来判断它是不是一个连通域的最后结束点.
                                                                                           #Get the info of the dot on top and judge if it is the lass ending dot of a connected area
                if ShapeInfo[XLmax] == x and  ShapeInfo[XYmax][1] == y - 1:
                   #AddClip(bg_image, x, y, Neighbourhood3x3, LabelColor = "grey", Shape_info = ShapeInfo, duration = FinishTime,
                   #        注释1 = "白点时需要检查\n其上方的形状\n有无标记完成",
                   #        注释2 = "Check if any shape has\nfinished labeling\n"
                   #                "有形状完成啦!\nNo. {} has Finished: \n"
                   #                "总点数Total Num of dots: {}\nXYmax: {} XYmin: {}".format(ShapeInfo[RealLabel],ShapeInfo[Sum], tuple(ShapeInfo[XYmax]), tuple(ShapeInfo[XYmin])))
                    print("FPGA: Label:{} Sum: {} XYmax: {} XYmin: {}".format(LabelCount, ShapeInfo[Sum],ShapeInfo[XYmax], ShapeInfo[XYmin]))
                    cv2.rectangle(img, (ShapeInfo[XYmin][0], ShapeInfo[XYmin][1]), (ShapeInfo[XYmax][0], ShapeInfo[XYmax][1]), (255, 0, 255), 1)

cv2.imwrite("out.jpg", img)
