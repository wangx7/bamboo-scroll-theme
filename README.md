# 水墨 Theme

一个包含多款风格化 VS Code 主题的配色集合，强调「意象 + 长时可读」，灵感来自水墨画、竹。

## 主题列表

- **水墨画** - _经典系列_：水墨风格，还原传统意境。
- **水墨丹青（浅）** - _水墨风系列_：淡雅柔和，降低浅色环境下的视觉负担。
- **竹林深处（浅）** - _护眼系列_：青竹底色搭配墨色文字，极致清晰且长时办公不疲劳。

## 主题特色

- **传统色护眼配色**：基于中国传统色冷暖搭配，长时阅读更舒适。
- **扩展语义高亮**：完善 TS/JS/Vue/Python/Java/Go 等语义 Token 映射。
- **全方位 UI 适配**：统一优化终端、Git、侧边栏、状态栏和搜索面板。

## 使用方式

1. 在 VS Code 扩展市场搜索并安装 `水墨 Theme`。
2. 打开命令面板（快捷键：`Cmd/Ctrl + Shift + P`）并执行 `Preferences: Color Theme`（首选项：颜色主题）。
3. 选择您需要的主题：**水墨丹青**、**竹林深处**。

_快捷路径：`Cmd/Ctrl + K` -> `Cmd/Ctrl + T`。_

## 预览

- [水墨画 - 效果预览](https://raw.githack.com/wangx7/shuimo-theme/main/previews/ink-wash-painting-preview.html)
- [水墨丹青（浅色） - 效果预览](https://raw.githack.com/wangx7/shuimo-theme/main/previews/ink-wash-light-preview.html)
- [竹林深处（浅色）- 效果预览](https://raw.githack.com/wangx7/shuimo-theme/main/previews/bamboo-green-light-preview.html)

## 进阶 — 背景装饰
> VS Code 原生主题不支持背景图案，但可以搭配第三方扩展实现。

### 配置步骤

**方式一：使用 [Background](https://marketplace.visualstudio.com/items?itemName=Katsute.code-background) 扩展（推荐）**

1. 在扩展市场安装 **Background** (by Katsute)
2. 打开 VS Code 设置（`Cmd/Ctrl + ,`），搜索 `background`
3. 在 **Background: Editor Backgrounds** 栏点击「添加项」，填入图片**绝对路径**（注意不要有多余引号）：
```
https://colors.ichuantong.cn/assets/bg.texture-Dnw-puWb.png
```
4. **⚡ 关键步骤**：`Cmd/Ctrl + Shift + P` 打开命令面板，执行 **`Background: Install`**