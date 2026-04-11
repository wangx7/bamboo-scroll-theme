# 水墨 Theme

一个包含多款风格化 VS Code 主题的配色集合，强调「意象 + 长时可读」，灵感来自水墨画、竹。

## 主题列表

- **竹林深处（深）** - _护眼系列_：如浓墨落于青竹，极致清晰且长时办公不疲劳。
- **水墨丹青（浅）** - _水墨风系列_：淡雅柔和，降低浅色环境下的视觉负担。
- **月涌大江流（深）** - _深蓝夜江系列_：深蓝底色配银蓝点缀，层级清晰、对比充足。
- **竹简（浅）** - _棕色系列_：传统色体系 + WCAG AA 对比度，适合白天长时编码。
- **竹简墨夜（深）** - _棕色系列_：玄墨底色搭配赭石与竹青语义分层，适合夜间专注。

## 主题特色

- **传统色护眼配色**：基于中国传统色冷暖搭配，长时阅读更舒适。
- **扩展语义高亮**：完善 TS/JS/Vue/Python/Java/Go 等语义 Token 映射。
- **全方位 UI 适配**：统一优化终端、Git、侧边栏、状态栏和搜索面板。

## 使用方式

1. 在 VS Code 扩展市场搜索并安装 `水墨 Theme`。
2. 打开命令面板（快捷键：`Cmd/Ctrl + Shift + P`）并执行 `Preferences: Color Theme`（首选项：颜色主题）。
3. 选择您需要的主题：**竹林深处**、**水墨丹青**、**月涌大江流**、**竹简**、**竹简墨夜**。

_快捷路径：`Cmd/Ctrl + K` -> `Cmd/Ctrl + T`。_

## 预览

- [竹林深处（浅色）- 效果预览](https://raw.githack.com/wangx7/shuimo-theme/main/previews/bamboo-green-light-preview.html)
- [竹简（浅色） - 效果预览](https://raw.githack.com/wangx7/shuimo-theme/main/previews/bamboo-scroll-paper-preview.html)
- [水墨丹青（浅色） - 效果预览](https://raw.githack.com/wangx7/shuimo-theme/main/previews/ink-wash-light-preview.html)
- [竹简墨夜（深色） - 效果预览](https://raw.githack.com/wangx7/shuimo-theme/main/previews/bamboo-scroll-dark-preview.html)
- [月涌大江流（深色） - 效果预览](https://raw.githack.com/wangx7/shuimo-theme/main/previews/moon-river-dark-preview.html)

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