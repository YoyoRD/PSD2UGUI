from psd_tools import PSDImage
from xml.dom.minidom import Document

psd = PSDImage.open('test.psd')

# 模块名 预设名
moduleName = "Test"
prefabName = "TestPanel"

AssetPath = "C:/Users/37/Documents/GitHub/game-frame/UGUIFrame/Assets/"
UIModulePath = AssetPath + "OriginalResource/UI/"

# 文件夹名字
spriteDir = "Sprite"
spriteFontDir = "Sprite_Font"
textureDir = "Texture"

TestPath = "C:/Users/37/Desktop/img/"

maxWigth = 499 # 最大宽度 超过了 就丢到纹理层
maxHeight = 499 # 最大高度 超过了 就丢到纹理层

# 名字定义列表
typeList = ["btn", "txt" , "img" ,"tex" ,"slider"]

# Font输出规则
fontType = "_f"

# 输出效果图
# psd.composite().save('example.png')


######################################## XML #####################################################
#最外层的管理List
docList = []

#创建一个文档对象
doc=Document()

#创建一个根节点Root对象
root = doc.createElement('PSDUI')

#将根节点添加到文档对象中
doc.appendChild(root)

# 特殊处理 PSD的长宽
psdSize = doc.createElement('psdSize')
psdWidth = doc.createElement('width')
psdWidthValue = doc.createTextNode(str(psd.width))
psdWidth.appendChild(psdWidthValue)
psdHeight = doc.createElement('height')
psdHeightValue = doc.createTextNode(str(psd.height))
psdHeight.appendChild(psdHeightValue)
psdSize.appendChild(psdWidth)
psdSize.appendChild(psdHeight)
root.appendChild(psdSize)

# 创建layerElement
def createLayer(parent):
    if parent :
        layerElement = doc.createElement("Layer")
        parent.appendChild(layerElement)
    return layerElement

####################################### 解析函数 ####################################################
def getTypeByName(name):
    for value in typeList:
        if value in name:
            return value
    return ""

# 设置子节点的xml
def setChildElement(typeName,layer):
    tempDic = {"name" : layer.name , "type" : typeName}
    docList.append(tempDic)
    return

# 根据类型分函数解析
def resolvingByType(typeName , layer):
    if typeName == "btn":
        resolvingBtn(layer)
    elif typeName == "tex":
        resolvingTex(layer)
    elif typeName == "slider":
        resolvingSlider(layer)

# 解析btn
def resolvingBtn(layer):
    # 保存图片
    for childs in layer:
        saveImg(childs)
    return

# 解析Tex
def resolvingTex(layer):
    tex = layer.composite()
    tex.save(TestPath + textureDir + '%s.png' % layer.name)
    return

def resolvingSlider(layer):
    
    return

############################################# 生成资源 ##############################################
def isTexture(layer):
    return layer.height > maxHeight or layer.width > maxWigth

def isSpriteFont(layer):
    return fontType in layer.name

# 保存图片
def saveImg(childs):
    if "img" in childs.name :
            addValue = ""
            if isTexture(childs):
                addValue = textureDir + "/"
            elif isSpriteFont(childs):
                addValue = spriteFontDir + "/"
            else:
                addValue = spriteDir + "/"
            childLayer = childs.composite()
            childLayer.save(TestPath + addValue + '%s.png' % childs.name)
    return

####################################################################################################

def loopResolving(layers):
    # layer 从下自上
    for layer in layers:
        # 判断图层是否显示
        if layer.is_visible() :
            typeName = getTypeByName(layer.name)
            if typeName != "":
                # 保存图片
                resolvingByType(typeName,layer)
                # 生成xml
                setChildElement(typeName,layer)
    return

# 最上层解析
loopResolving(psd)

# list<Dic> 转Xml 解析递归
def listToXMlByLoop(parentList,parentElemet):
    xmllayertemp = createLayer(parentElemet)
    for value in parentList:
        nodeName = doc.createElement(value)
        nodeName.appendChild(doc.createTextNode(str(parentList[value])))
        xmllayertemp.appendChild(nodeName) 
    return 

xmlChildren = doc.createElement('children')
root.appendChild(xmlChildren)

for element in docList:
    listToXMlByLoop(element,xmlChildren)

        
   
fp = open(prefabName+".xml", 'w')
fp.write(doc.toprettyxml(indent="\t", newl="\n", encoding="utf-8"))
fp.close()