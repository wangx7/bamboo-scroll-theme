# 水墨 Theme

一个包含 4 款风格化 VS Code 主题的配色集合，强调「意象 + 长时可读」，灵感来自水墨画、丹青与竹简。

## 主题列表

- **竹简（浅色）** - _棕色系列_：传统色体系 + WCAG AA 对比度，适合白天长时编码。
- **水墨丹青（浅色）** - _水墨风系列_：淡雅柔和，降低浅色环境下的视觉负担。
- **竹简墨夜（深色）** - _棕色系列_：玄墨底色搭配赭石与竹青语义分层，适合夜间专注。
- **月涌大江流（深色）** - _深蓝夜江系列_：深蓝底色配银蓝点缀，层级清晰、对比充足。

## 主题特色

- **传统色护眼配色**：基于传统色冷暖搭配，长时阅读更舒适。
- **扩展语义高亮**：完善 TS/JS/Vue/Python/Java/Go 等语义 Token 映射。
- **全方位 UI 适配**：统一优化终端、Git、侧边栏、状态栏和搜索面板。

## 使用方式

1. 在 VS Code 扩展市场搜索并安装 `水墨 Theme`。
2. 打开命令面板（快捷键：`Cmd/Ctrl + Shift + P`）并执行 `Preferences: Color Theme`（首选项：颜色主题）。
3. 选择您需要的主题：**竹简**、**水墨丹青**、**竹简墨夜** 或 **月涌大江流**。

_快捷路径：`Cmd/Ctrl + K` -> `Cmd/Ctrl + T`。_

## 预览

- [竹简（浅色） - 效果预览](https://raw.githack.com/wangx7/shuimo-theme/main/previews/bamboo-scroll-paper-preview.html)
- [水墨丹青（浅色） - 效果预览](https://raw.githack.com/wangx7/shuimo-theme/main/previews/ink-wash-light-preview.html)
- [竹简墨夜（深色） - 效果预览](https://raw.githack.com/wangx7/shuimo-theme/main/previews/bamboo-scroll-dark-preview.html)
- [月涌大江流（深色） - 效果预览](https://raw.githack.com/wangx7/shuimo-theme/main/previews/moon-river-dark-preview.html)

## 🎨 进阶 — 背景装饰

> VS Code 原生主题不支持背景图案，但可以搭配第三方扩展实现。我们为每款主题准备了匹配风格的水墨背景素材。

### 素材预览

| 主题 | 背景风格 | 文件 |
| --- | --- | --- |
| 竹简（浅色） | 水墨竹影 | `backgrounds/bamboo-light.png` |
| 水墨丹青（浅色） | 水墨山水 | `backgrounds/inkwash-light.png` |
| 竹简墨夜（深色） | 暗夜竹影 | `backgrounds/bamboo-dark.png` |
| 月涌大江流（深色） | 月夜江流 | `backgrounds/moonriver-dark.png` |

### 配置步骤

**方式一：使用 [Background](https://marketplace.visualstudio.com/items?itemName=Katsute.code-background) 扩展（推荐）**

1. 在扩展市场安装 **Background** (by Katsute)
2. 打开 VS Code 设置（`Cmd/Ctrl + ,`），搜索 `background`
3. 在 **Background: Editor Backgrounds** 栏点击「添加项」，填入图片**绝对路径**（注意不要有多余引号）：

```
/Users/你的用户名/路径/shuimo-theme/backgrounds/bamboo-light.png
```

4. （可选）调整透明度：在设置中搜索 `background.opacity`，建议设为 `0.1` ~ `0.15`
5. **⚡ 关键步骤**：`Cmd/Ctrl + Shift + P` 打开命令面板，执行 **`Background: Install`**
6. VS Code 提示重启，点击 **Restart** 即可生效

> 💡 **提示**：如果修改了配置，每次都需要重新执行 `Background: Install` 才能生效。

> ⚠️ **注意**：Background 扩展会修改 VS Code 内部文件，首次使用后会出现 "Your Code installation appears to be corrupt" 提示，点击齿轮图标选择 "Don't Show Again" 即可，**不影响正常使用**。VS Code 更新后需要重新执行 `Background: Install`。
