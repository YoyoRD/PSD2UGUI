# PSD2UGUI

## 说在前面

- 项目开发思路来源于 [quick_psd2UGUI](https://github.com/zs9024/quick_psd2ugui) ,是在此之上结合项目的扩展。
- 不得不说，PSD转Prefab的沟通成本是真的高，所以指望一套成熟的方案解决需求，大概率是不太行的。成本在美术那边没有程序思维。小厂大家都熟沟通起来方便还行，大厂简直要命，特别是流动的美术中心，真心推不动。
- 工程经历了小厂的一个项目开发，命名规则尽量简化了，自定义的内容基本上都抽成常量，方便修改。
- 本方案只做参考，除非用配套的[UI框架](https://gitee.com/Yoyo21/game-frame/tree/master/UGUIFrame)

---

## 解决问题

- 解决手动构建prefab的弊端，采用自动化处理psd文件生成prefab。
- 根据命名，生成图集。

---

## 自动化与半自动化

- 看项目组人员结构去选择，有时候工具化没法做全自动，实属无奈。

### 自动化

- 自动化的概念是指，处理PSD的统一入口是在发版机，也就是有一个集成CI。由发版机去打包模块的Psd文件，然后客户端在update，从而得到prefab。
- 自动化就把打包这个过程从本地机移植到发版机，就不用装PS，只需要提交模块打包的命令。
- 自动化代码由Python编写，不管是Jenkins 或者 TeamCity 都可以方便集成

### 半自动化

- 半自动化指手动管理图集，手动在ps里面导出需要的xml，手动生成Prefab。
- 基本上这个流程由程序执行，但是胜于可控性高，沟通成本就少很多。

---

## 如何开始

- 将脚本文件 Export PSDUI.jsx拷贝至“ps安装目录\Presets\Scripts”目录下，如：“E:\Program Files\PS\Adobe Photoshop CS6 (64 Bit)\Presets\Scripts”。
- 打开一个psd文件，在cs6中选择“文件->脚本->Export PSDUI”，会弹框选择一个目录，存放脚本运行时的切图和配置文件(xml)。
- 将上一步生成的切图和配置拷贝到unity中，在菜单栏选择quicktool/psdimport执行，弹框选择上一步导出的xml文件，将在hierarchy中生成ugui面板

### 提示

- 使用编辑器修改或调试ps脚本：找到或下载编辑器adobe extendscript toolkit，一般都在C盘，如C:\Program Files (x86)\Adobe\Adobe Utilities - CS6\ExtendScript Toolkit CS6， file/open打开文件“ps安装目录\Presets\Scripts\Export PSDUI.jsx”，目标应用选择“Adobe Photoshop CS6”，就可以断点调试运行了
- 如果运行ps脚本时出现错误“合并可见图层当前不可用”，可以检查是否有单个图片(比如背景图)位于根节点的最后，并将其移到某个图层组下面，具体见文档
- ps cc版本报错“错误8800...sceneData += "" + obj.textItem.color.rgb.hexValue + "";”时，可检查text是不是包含了多个色值，要用单色，多色在unity里自己用richtext的color实现
- 有问题或者建议、想法可以加QQ群654564220讨论
- 以上内容我就不改了，尊重原作者。

### 注意事项

- 在PSD文件内，最外层添加一个组，组名为 PSD文件名 + @ 模块名 。如下图：
- ![image-20210112150032947](https://gitee.com/Yoyo21/image-hosting/raw/master/img/image-20210112150032947.png)
- 两种情况下会分开 几个PSD文件
  - 1.存在列表(List)的时候，列表内的项 需要新建一个新的PSD文件
  - 2.存在切换页面，被切换的页面需要 新建一个PSD文件 
- 需要显示 但不需要导出的内容 则可以加入 @null
  - ![image-20210112150613236](https://gitee.com/Yoyo21/image-hosting/raw/master/img/image-20210112150613236.png)

---

## 命名规则

### 文本

- 不需要任何图层管理，直接放即可。
  - ![image-20210112150845517](https://gitee.com/Yoyo21/image-hosting/raw/master/img/image-20210112150845517.png)
- 如果文字是需要导出图片，则在后面加入_wztp （文字图片的拼音）
  - ![image-20210112151046946](https://gitee.com/Yoyo21/image-hosting/raw/master/img/image-20210112151046946.png)

### 按钮

- 按钮的内容 需要加入一个组， 组的名字为 btnA@an 
  - btnA 保证一个psd文件内不重复
  - @an(按钮的拼音) 代表是按钮
  - ![image-20210112151228639](https://gitee.com/Yoyo21/image-hosting/raw/master/img/image-20210112151228639.png)
  - imgBtn1可以随便命名
  - 如果是图片自带文字 ,Title 都可以不用有
  - 如果是2张图片 则建议合并图层
    - 如果不合 就在下面加一个图层即可

### 选中框

- 选中框的内容 需要加入一个组 ，组的名称为 xxxx@xzk
  - xxxx 保证一个psd文件内不重复
  - @xzk(选中框的拼音) 代表的是选中框
  - ![image-20210112152044302](https://gitee.com/Yoyo21/image-hosting/raw/master/img/image-20210112152044302.png)
  - 内部有一个xz 的组 ，这里面存选中状态的图片
  - 默认状态就放在bxz下

### 列表

- 列表的内容 需要加入一个组 。 组的名称为 xxxx@lb:H:1

  - xxxx 保证一个psd文件内不重复

  - @lb(列表的拼音) 代表的是一个列表

  - :H 与 :V  H 代表横着滑动 V 代表竖着滑动

  - 1 代表一行 或者 一列放几个

    ![image-20210112152335532](https://gitee.com/Yoyo21/image-hosting/raw/master/img/image-20210112152335532.png)

  - 如上图 1 代表 一列放1个 一行放几个 无所谓 因为可以滑动

- ![image-20210112152440954](https://gitee.com/Yoyo21/image-hosting/raw/master/img/image-20210112152440954.png)

  - @Size 就是这个列表的大小，一般给透明度 为1(不影响PSD内部的显示 透明不透明都行 但是不能为0)

- 如果是单行 或者 单列 需要放两个Item 来确定他们之间的间隔

- 如果是多行多列的列表 则 起码放 三个， 左上 右边 下面 来确定 列表项的 间隔

- **列表下的子项 名称为另外PSD的名称 ，图中的内容有错**



---

## 开发记录

### 2020.11.30

- psd2UGUI 进度(10%) 

  - 解析图片,子层级解析

  - 加入循环递归

- UI组件加入项目(50%)

  - 扩展Menu,解决组件报错。
  - 一键生成模块工具
  - UIBinder 规则修改
    - 全部替换成组件化

### 2020.12.1

- UI组件bug修复
- 优化模块加载(70%)
  - 去除UIControllerConfig , 加入ModuleManager
  - 加入LuaLoad分帧加载

### 2020.12.2

- 完成LuaLoad 并测试 (100%)
  - Main.lua 下的require 移动
- psd2UGUI(20%)
  - 命名的规定抽象方便修改
  - 熟悉API

### 2020.12.3 - 2020.12.4

- psd2UGUI 开发
  - 组件解析
    - Button (完成)
    - Sprite （完成）
    - Text(TMP) (完成)
    - Texture (完成)
    - Slider
    - Toggle
    - TabGroup
    - List

- TODO：
  - 资源自动加载项目
    - 自动九宫？
    - Texture 的格式
  - Sprite的Common图集 未处理
  - Button下挂子节点 有点问题



### 2020.12.7 

- 资源目录调整结构
  - 打包图集工具调整
  - 一键生成模块工具调整
- CText解析完成

### 2020.12.8

- PSD解析工具加入项目
- CList解析规则开发
- 增加一键生成预设目录



TODO ：

- 更改CToggleGroup 为 CTabBarGroup
- UIManager  BaseUI 修改
  - 废弃UIViewConfig
- 解析CTabBarGroup psd
- UIBinder  规则优化
- 预加载流程



###  2020.12.14

- 修改BaseUI BaseView BaseNode UIManager脚本
- todo : UIManager 管理 baseView

### 2020.12.15

- 修改 UIBinder 脚本文件
- BaseUI  完善
- UIManager 管理 baseView 完成

### 2020.12.16

- 准备下周分享的内容
  - 半自动化工具
    - List的解析
    - Button解析bug修复
  - 充值模块开发

### 2020.12.17

- 调整之后的框架代码适应当前的项目
-  调整CBaseView层级关系
- 加入SortOrder 关键参数

