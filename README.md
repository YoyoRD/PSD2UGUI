# PSD2UGUI(开发ing)
## 解决问题

- 解决手动构建prefab的弊端，采用自动化处理psd文件生成prefab。
- PSD2UGUI 的自定义很高，所以很难一套解析规则通用，本方案只做参考，除非配用同套[UI框架](https://gitee.com/Yoyo21/game-frame/tree/master/UGUIFrame)

## 如何处理

- 解析psd文件采用python库 [psd-tools](https://github.com/psd-tools/psd-tools)
  - 生成Prefab的XML
  - 解析图层到对于模块位置
- Unity解析XML到prefab对应的框架是封了一层的UGUI