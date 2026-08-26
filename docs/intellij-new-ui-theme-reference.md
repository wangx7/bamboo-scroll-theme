# IntelliJ IDEA New UI 官方主题开发与定制参考指南

> **官方参考源索引**:
> - [JetBrains IntelliJ Platform SDK - Developing a Theme](https://plugins.jetbrains.com/docs/intellij/themes-intro.html)
> - [JetBrains IntelliJ Platform SDK - Customizing Themes](https://plugins.jetbrains.com/docs/intellij/themes-customize.html)
> - [JetBrains IntelliJ Platform SDK - Exposing Theme Metadata](https://plugins.jetbrains.com/docs/intellij/themes-metadata.html)
> - [JetBrains IntelliJ Platform SDK - Theme Icons & ColorPalette](https://plugins.jetbrains.com/docs/intellij/themes-icons.html)
> - [JetBrains IntelliJ Platform SDK - Internal UI Inspector](https://plugins.jetbrains.com/docs/intellij/internal-ui-inspector.html)
> - [JetBrains IntelliJ Platform SDK - LaF Defaults Dialog](https://plugins.jetbrains.com/docs/intellij/internal-ui-laf-defaults.html)
> - [JetBrains UI Guidelines & Design System](https://jetbrains.design/intellij/)
> - [JetBrains UI Guidelines - Platform Theme Colors](https://jetbrains.design/intellij/principles/platform_theme_colors/)
> - [JetBrains UI Guidelines - Icons List](https://jetbrains.design/intellij/resources/icons_list/)
> - [JetBrains Community 官方源码库 (GitHub)](https://github.com/JetBrains/intellij-community)
>   - New UI 官方主题定义: [`platform/platform-resources/src/themes/expUI/`](https://github.com/JetBrains/intellij-community/tree/master/platform/platform-resources/src/themes/expUI) (`expUI_dark.theme.json`, `expUI_light.theme.json`, `expUI_light_with_light_header.theme.json`)
>   - 平台主题元数据字典: [`IntelliJPlatform.themeMetadata.json`](https://github.com/JetBrains/intellij-community/blob/master/platform/platform-resources/src/themes/metadata/IntelliJPlatform.themeMetadata.json)
>   - Swing 组件元数据字典: [`JDK.themeMetadata.json`](https://github.com/JetBrains/intellij-community/blob/master/platform/platform-resources/src/themes/metadata/JDK.themeMetadata.json)

---

## 目录
- [一、IntelliJ New UI 架构与设计哲学](#一intellij-new-ui-架构与设计哲学)
  - [1. New UI 的核心演进与设计规范](#1-new-ui-的核心演进与设计规范)
  - [2. UI Theme 与 Editor Color Scheme 的分工关系](#2-ui-theme-与-editor-color-scheme-的分工关系)
  - [3. 官方主题继承机制 (parentTheme)](#3-官方主题继承机制-parenttheme)
- [二、主题描述文件 (`*.theme.json`) 格式规范](#二主题描述文件-themejson-格式规范)
  - [1. 顶级元数据规范](#1-顶级元数据规范)
  - [2. 色彩变量块 (`colors`) 与引用语法](#2-色彩变量块-colors-与引用语法)
  - [3. 键名命名模式 (Key Naming Scheme)](#3-键名命名模式-key-naming-scheme)
- [三、New UI 专属核心 UI Customization Keys 全景字典](#三new-ui-专属核心-ui-customization-keys-全景字典)
  - [1. 顶部主工具栏 (Main Toolbar / Header)](#1-顶部主工具栏-main-toolbar--header)
  - [2. 侧边栏与工具窗口 (Tool Window & Tool Window Stripes)](#2-侧边栏与工具窗口-tool-window--tool-window-stripes)
  - [3. 编辑器标签页与面包屑 (Editor Tabs & Breadcrumbs)](#3-编辑器标签页与面包屑-editor-tabs--breadcrumbs)
  - [4. 项目树、列表与表格 (Tree, List & Table)](#4-项目树列表与表格-tree-list--table)
  - [5. 弹窗、全局搜索与浮层 (Popup & Search Everywhere)](#5-弹窗全局搜索与浮层-popup--search-everywhere)
  - [6. 基础交互控件 (Button, TextField, ComboBox, CheckBox)](#6-基础交互控件-button-textfield-combobox-checkbox)
  - [7. 状态栏与内置终端 (StatusBar & Terminal)](#7-状态栏与内置终端-statusbar--terminal)
  - [8. 徽标、通知与横幅 (Badge, Banner & Notification)](#8-徽标通知与横幅-badge-banner--notification)
- [四、New UI 图标与调色板体系 (`icons` & `ColorPalette`)](#四new-ui-图标与调色板体系-icons--colorpalette)
  - [1. 全局图标色彩替换 (`ColorPalette`)](#1-全局图标色彩替换-colorpalette)
  - [2. 官方上下文色板 (Actions & Objects)](#2-官方上下文色板-actions--objects)
  - [3. 自定义 SVG 图标覆盖映射](#3-自定义-svg-图标覆盖映射)
- [五、官方主题调试与审查工具链 (Internal Mode)](#五官方主题调试与审查工具链-internal-mode)
  - [1. 开启 JetBrains 平台 Internal Mode](#1-开启-jetbrains-平台-internal-mode)
  - [2. 使用 UI Inspector 实时定位 UI Key](#2-使用-ui-inspector-实时定位-ui-key)
  - [3. 使用 UI Theme Color Picker & LaF Defaults](#3-使用-ui-theme-color-picker--laf-defaults)
- [六、从零构建并发布 New UI 主题插件工程](#六从零构建并发布-new-ui-主题插件工程)
  - [1. 推荐工程目录结构 (Gradle IntelliJ Platform Plugin)](#1-推荐工程目录结构-gradle-intellij-platform-plugin)
  - [2. `plugin.xml` 清单配置](#2-pluginxml-清单配置)
  - [3. `build.gradle.kts` 构建配置](#3-buildgradlekts-构建配置)
  - [4. 本地运行、打包 (zip) 与 Marketplace 发布](#4-本地运行打包-zip-与-marketplace-发布)
- [七、New UI 与 VS Code 主题色值快速映射表](#七new-ui-与-vs-code-主题色值快速映射表)

---

## 一、IntelliJ New UI 架构与设计哲学

### 1. New UI 的核心演进与设计规范

JetBrains 自 2022.3 开始推行、并在后续版本中作为默认界面的 **New UI**（内部代号 `expUI`），相比经典的 Classic UI（Darcula / IntelliJ Light），具备以下核心设计理念：

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Main Toolbar (主工具栏): 深度整合 VCS 分支、运行配置、Search Everywhere、窗口控制 │
├───────────┬─────────────────────────────────────────────┬───────────────────┤
│ Left      │ Editor Tabs (现代化下划线指示器 Tab / 融入背景) │ Right             │
│ Stripe    ├─────────────────────────────────────────────┤ Stripe            │
│ (单列纯图标)│                                             │ (单列纯图标)      │
│           │                                             │                   │
│ Project   │             Editor Area (代码编辑区)         │ Git / Database /  │
│ Tree      │                                             │ Maven / Gradle    │
│ (降噪高对比)│                                             │ 抽屉式侧边栏      │
│           ├─────────────────────────────────────────────┤                   │
│           │ Bottom ToolWindow (Terminal / Run / Debug)  │                   │
├───────────┴─────────────────────────────────────────────┴───────────────────┤
│  Status Bar (状态栏): 极简文字与状态指示，与底部边框优雅贴合                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

1. **界面降噪 (Visual Noise Reduction)**:
   - 移除了过多厚重突兀的浮雕立体边框与梯形 Tab 边角。
   - 使用统一的微妙单像素边框（如 `#1E1F22` / `#393B40`）划分主工作区。
2. **色块层次清晰 (Visual Hierarchy)**:
   - **深色模式 (Dark)**：标题栏/主工具栏 (`#2B2D30`)、侧边栏/工具窗口 (`#2B2D30` 或 `#1E1F22`)、代码编辑区 (`#1E1F22`) 形成明确的明暗景深。
   - **浅色模式 (Light / Light with Light Header)**：支持白色头部或经典深灰头部，工作区保持纯净透亮。
3. **圆角与现代控件 (Modern Components)**:
   - 按钮、输入框、标签页悬浮高亮均使用 `4px` ~ `8px` 现代圆角。
   - 激活选中态由旧版的“全高亮矩形块”演化为“高对比背景色 + 左侧/底部指示条 (Underline Indicator)”。

---

### 2. UI Theme 与 Editor Color Scheme 的分工关系

在 JetBrains 插件生态中，一个完整的主题通常由两个核心文件组成：

| 组成部分 | 文件格式 | 作用范畴 | 对应 Settings 入口 |
| :--- | :--- | :--- | :--- |
| **UI Theme (界面主题)** | `*.theme.json` | 负责 IDE 窗口外框、工具栏、侧边栏、菜单、按钮、弹窗、树控件、图标等一切 Swing/JComponent 控件的色彩与边框 | `Appearance & Behavior` > `Appearance` > `Theme` |
| **Editor Color Scheme (代码配色)** | `*.xml` 或 `*.icls` | 负责代码编辑器内部的语法高亮、语义着色、行号槽 (Gutter)、断点行、Diff 差异比对、控制台 ANSI 色彩等 | `Editor` > `Color Scheme` > `Scheme` |

在 `*.theme.json` 中，可以通过 `editorScheme` 字段将两者绑定：
```json
{
  "name": "Shuimo Dark",
  "dark": true,
  "author": "wangx",
  "editorScheme": "/themes/shuimo.xml",
  "ui": { ... }
}
```

---

### 3. 官方主题继承机制 (parentTheme)

自定义主题可以声明继承官方内建主题，只需覆盖特定的差异化键值：
- `parentTheme: "Darcula"`：继承官方经典 Darcula 深色底座。
- `parentTheme: "Light"`：继承官方经典浅色底座。
- `parentTheme: "ExpUI Dark"` / `parentTheme: "ExpUI Light"`：继承 New UI 官方底座。

---

## 二、主题描述文件 (`*.theme.json`) 格式规范

### 1. 顶级元数据规范

一个标准的 `*.theme.json` 顶级结构如下：

```json
{
  "name": "Shuimo IntelliJ New UI",
  "id": "com.shuimo.theme.newui.dark",
  "author": "wangx",
  "dark": true,
  "editorScheme": "/themes/shuimo-new-ui.xml",
  "colors": {
    "Background": "#2B2D30",
    "EditorBackground": "#1E1F22",
    "Border": "#393B40",
    "FocusBorder": "#3574F0",
    "AccentBlue": "#3574F0",
    "SelectionBackground": "#2E436E",
    "Foreground": "#DFE1E5"
  },
  "ui": {
    "*": {
      "background": "Background",
      "foreground": "Foreground"
    },
    "Component": {
      "focusColor": "FocusBorder",
      "borderColor": "Border"
    }
  },
  "icons": {
    "ColorPalette": {
      "#Actions.Grey": "#DFE1E5",
      "#Actions.Blue": "#3574F0"
    }
  }
}
```

#### 关键字段说明：
- `name` (String, 必填): 用户在 IDE 设置面板中看到的主题名称。
- `id` (String, 推荐): 主题全局唯一标识符（反向域名格式），避免同名冲突。
- `dark` (Boolean, 必填): 声明该主题是深色 (`true`) 还是浅色 (`false`)。
- `author` (String, 可选): 作者信息。
- `editorScheme` (String, 可选): 关联的代码配色方案 XML/ICLS 文件在 resources 中的绝对路径。
- `colors` (Object, 可选): 颜色变量定义字典，用于在 `ui` 与 `icons` 中复用。
- `ui` (Object, 必填): UI 控件与色值/边框映射字典。
- `icons` (Object, 可选): 图标调色板 (`ColorPalette`) 与自定义 SVG 路径映射。

---

### 2. 色彩变量块 (`colors`) 与引用语法

在 `colors` 块中定义的名称，可以直接在 `ui` 属性中作为值使用：

```json
{
  "colors": {
    "MainBg": "#2B2D30",
    "PanelBorder": "#1E1F22"
  },
  "ui": {
    "MainToolbar.background": "MainBg",
    "ToolWindow.Header.background": "MainBg",
    "ToolWindow.border": "PanelBorder"
  }
}
```

也可以通过追加两位 16 进制数表示 **Alpha 透明度通道**（如 `MainBg.80` 或 `#2B2D30CC`）。

---

### 3. 键名命名模式 (Key Naming Scheme)

JetBrains 官方 SDK 规范定义了严格的 UI 键名命名范式：

$$\text{Object}[.\text{SubObject}].[ \text{state} ][\text{Part}]\text{Property}$$

例如：`ToolWindow.HeaderTab.hoverInactiveBackground`
- **Object**: `ToolWindow` (大驼峰)
- **SubObject**: `HeaderTab` (大驼峰)
- **State**: `hoverInactive` (小驼峰前缀：`hover`, `selected`, `focused`, `pressed`, `disabled`, `inactive`)
- **Part**: 可选子部件（如 `Border`, `Caret`, `Icon`, `Separator`, `Shadow`）
- **Property**: `background` / `foreground` / `borderColor` / `underlineColor` (小驼峰)

---

## 三、New UI 专属核心 UI Customization Keys 全景字典

以下为 IntelliJ New UI 中最核心的 UI 控件键值与推荐深色/浅色搭配（以水墨/官方 New UI 体系为参考）：

### 1. 顶部主工具栏 (Main Toolbar / Header)

主工具栏是 New UI 最显著的视觉特征，整合了项目名称、Git 分支、运行配置与全局控制：

| UI Customization Key | 说明 | 推荐深色值 (Dark) | 推荐浅色值 (Light) |
| :--- | :--- | :--- | :--- |
| `MainToolbar.background` | 主工具栏背景色 (激活窗口) | `#2B2D30` | `#F7F8FA` / `#EBECF0` |
| `MainToolbar.inactiveBackground` | 主工具栏背景色 (未激活失焦窗口) | `#2B2D30` | `#F7F8FA` |
| `MainToolbar.border` | 主工具栏下边框 | `#1E1F22` | `#D5D7DA` |
| `MainToolbar.Dropdown.background` | 工具栏下拉框（如分支、运行配置）默认背景 | `#42454A` | `#E3E5E8` |
| `MainToolbar.Dropdown.hoverBackground` | 工具栏下拉框悬停背景 | `#4E5157` | `#D5D7DA` |
| `MainToolbar.Dropdown.pressedBackground`| 工具栏下拉框按下背景 | `#393B40` | `#C8CAD0` |
| `MainToolbar.Icon.hoverBackground` | 顶部操作纯图标悬停背景 | `#42454A` | `#E3E5E8` |
| `MainToolbar.Icon.pressedBackground` | 顶部操作纯图标按下背景 | `#393B40` | `#C8CAD0` |

---

### 2. 侧边栏与工具窗口 (Tool Window & Tool Window Stripes)

New UI 将侧边栏简化为两侧的纯图标条 (Stripe) 与滑出的工具窗口面板：

| UI Customization Key | 说明 | 推荐深色值 (Dark) | 推荐浅色值 (Light) |
| :--- | :--- | :--- | :--- |
| `ToolWindow.Stripe.background` | 侧边栏图标条根背景 | `#2B2D30` | `#F7F8FA` |
| `ToolWindow.Button.selectedBackground` | 激活工具窗口的侧边栏图标背景 | `#393B40` | `#E3E5E8` |
| `ToolWindow.Button.hoverBackground` | 侧边栏图标鼠标悬停背景 | `#393B40` | `#EBECF0` |
| `ToolWindow.Header.background` | 工具窗口标题栏背景 (激活状态) | `#2B2D30` | `#F7F8FA` |
| `ToolWindow.Header.inactiveBackground` | 工具窗口标题栏背景 (非激活状态) | `#2B2D30` | `#F7F8FA` |
| `ToolWindow.HeaderTab.selectedBackground` | 工具窗口多标签当前选中 Tab 背景 | `#393B40` | `#EBECF0` |
| `ToolWindow.HeaderTab.hoverBackground` | 工具窗口标签悬停背景 | `#393B40` | `#EBECF0` |
| `ToolWindow.HeaderTab.underlineColor` | 工具窗口选中标签底部高亮下划线颜色 | `#3574F0` | `#3574F0` |
| `ToolWindow.HeaderTab.underlineHeight` | 标签底部指示线高度 (像素值整数) | `2` | `2` |
| `ToolWindow.border` | 工具窗口外围分隔线 | `#1E1F22` | `#EBECF0` |

---

### 3. 编辑器标签页与面包屑 (Editor Tabs & Breadcrumbs)

New UI 采用了现代化的 Flat Underlined Tab 设计：

| UI Customization Key | 说明 | 推荐深色值 (Dark) | 推荐浅色值 (Light) |
| :--- | :--- | :--- | :--- |
| `EditorTabs.background` | 编辑器标签栏背景 | `#2B2D30` | `#F7F8FA` |
| `EditorTabs.underlinedTabBackground` | 当前激活标签页的背景色 | `#1E1F22` | `#FFFFFF` |
| `EditorTabs.underlineColor` | 激活标签页底部/顶部高亮指示线 | `#3574F0` | `#3574F0` |
| `EditorTabs.underlineHeight` | 指示线高度 (如 2 或 3) | `2` | `2` |
| `EditorTabs.inactiveUnderlineColor` | 失焦但选中状态的指示线颜色 | `#6F737A` | `#A8ADBD` |
| `EditorTabs.hoverBackground` | 鼠标悬停标签页背景色 | `#393B40` | `#EBECF0` |
| `EditorTabs.borderColor` | 标签栏与编辑区分割边框 | `#1E1F22` | `#EBECF0` |
| `EditorTabs.underlinedTabForeground` | 激活标签页文字颜色 | `#DFE1E5` | `#1E1F22` |
| `NavBar.background` | 导航栏 (Navigation Bar / Breadcrumbs) 背景 | `#1E1F22` | `#FFFFFF` |
| `NavBar.borderColor` | 导航栏分隔边框 | `#2B2D30` | `#EBECF0` |
| `Breadcrumbs.current` | 当前面包屑激活项文字高亮 | `#6A9BFA` | `#2463EB` |

---

### 4. 项目树、列表与表格 (Tree, List & Table)

用于工程目录树 (Project View)、类结构树 (Structure) 与各类列表：

| UI Customization Key | 说明 | 推荐深色值 (Dark) | 推荐浅色值 (Light) |
| :--- | :--- | :--- | :--- |
| `Tree.background` | 树控件背景色 | `#2B2D30` | `#F7F8FA` |
| `Tree.foreground` | 树节点文字默认颜色 | `#DFE1E5` | `#1E1F22` |
| `Tree.selectionBackground` | 树节点聚焦选中背景色 | `#2E436E` | `#D3E1FA` |
| `Tree.selectionForeground` | 树节点聚焦选中文字色 | `#FFFFFF` | `#1E1F22` |
| `Tree.selectionInactiveBackground` | 树节点失焦选中背景色 | `#393B40` | `#EBECF0` |
| `Tree.hoverBackground` | 树节点鼠标悬停背景色 | `#393B40` | `#EBECF0` |
| `Tree.modifiedItemForeground` | 文件已修改未提交高亮色 (Git Modified) | `#6897BB` | `#2463EB` |
| `List.background` | 下拉/常规列表背景色 | `#2B2D30` | `#FFFFFF` |
| `List.selectionBackground` | 列表项选中背景色 | `#2E436E` | `#D3E1FA` |
| `List.hoverBackground` | 列表项悬停背景色 | `#393B40` | `#EBECF0` |
| `Table.background` | 表格背景色 | `#2B2D30` | `#FFFFFF` |
| `Table.stripeBackground` | 表格斑马线交替背景色 | `#26282B` | `#F7F8FA` |

---

### 5. 弹窗、全局搜索与浮层 (Popup & Search Everywhere)

New UI 对双击 Shift 全局搜索 (`SearchEverywhere`) 与自动补全弹窗进行了大范围现代化圆角与轻量化重构：

| UI Customization Key | 说明 | 推荐深色值 (Dark) | 推荐浅色值 (Light) |
| :--- | :--- | :--- | :--- |
| `SearchEverywhere.Header.background` | 全局搜索窗口头部背景色 | `#2B2D30` | `#F7F8FA` |
| `SearchEverywhere.SearchField.background`| 全局搜索输入框背景色 | `#1E1F22` | `#FFFFFF` |
| `SearchEverywhere.SearchField.borderColor` | 全局搜索输入框边框 | `#393B40` | `#D5D7DA` |
| `SearchEverywhere.List.separatorColor` | 搜索结果分类分割线颜色 | `#393B40` | `#EBECF0` |
| `Popup.background` | 通用悬浮弹窗/气泡背景色 | `#2B2D30` | `#FFFFFF` |
| `Popup.borderColor` | 弹窗单像素边框颜色 | `#42454A` | `#D5D7DA` |
| `Popup.paintBorder` | 是否绘制弹窗边框 (Boolean) | `true` | `true` |
| `Popup.Header.activeBackground` | 弹窗头部激活背景色 | `#2B2D30` | `#F7F8FA` |
| `Popup.Advertiser.background` | 弹窗底部操作快捷键提示栏背景色 | `#26282B` | `#F7F8FA` |
| `Popup.Advertiser.foreground` | 弹窗底部提示文字色 | `#7A7E85` | `#818594` |
| `CompletionPopup.background` | 代码智能补全弹窗背景色 | `#2B2D30` | `#FFFFFF` |
| `CompletionPopup.selectionBackground` | 补全项选中高亮背景 | `#2E436E` | `#D3E1FA` |
| `CompletionPopup.infoForeground` | 补全类型/参数灰色辅助说明文字 | `#8C9099` | `#818594` |

---

### 6. 基础交互控件 (Button, TextField, ComboBox, CheckBox)

通用组件定义通常影响整个 IDE 弹窗和设置面板中的所有表单控件：

```json
{
  "ui": {
    "Component": {
      "focusColor": "#3574F0",
      "borderColor": "#393B40",
      "focusedBorderColor": "#3574F0",
      "disabledBorderColor": "#393B4080",
      "errorFocusColor": "#D64D5B",
      "warningFocusColor": "#C29E49"
    },
    "Button": {
      "startBackground": "#393B40",
      "endBackground": "#393B40",
      "startBorderColor": "#4F5156",
      "endBorderColor": "#4F5156",
      "focusedBorderColor": "#3574F0",
      "foreground": "#DFE1E5",
      "default": {
        "startBackground": "#3574F0",
        "endBackground": "#3574F0",
        "startBorderColor": "#3574F0",
        "endBorderColor": "#3574F0",
        "focusedBorderColor": "#6A9BFA",
        "foreground": "#FFFFFF"
      }
    },
    "TextField": {
      "background": "#1E1F22",
      "foreground": "#DFE1E5",
      "caretForeground": "#DFE1E5",
      "selectionBackground": "#2E436E",
      "selectionForeground": "#FFFFFF"
    },
    "ComboBox": {
      "background": "#1E1F22",
      "nonEditableBackground": "#1E1F22",
      "ArrowButton": {
        "iconColor": "#9EA0A8",
        "disabledIconColor": "#5A5D63"
      }
    },
    "CheckBox": {
      "background": "#2B2D30",
      "foreground": "#DFE1E5"
    }
  }
}
```

---

### 7. 状态栏与内置终端 (StatusBar & Terminal)

| UI Customization Key | 说明 | 推荐深色值 (Dark) | 推荐浅色值 (Light) |
| :--- | :--- | :--- | :--- |
| `StatusBar.background` | 状态栏背景色 | `#2B2D30` | `#F7F8FA` |
| `StatusBar.borderColor` | 状态栏上边框颜色 | `#1E1F22` | `#EBECF0` |
| `StatusBar.hoverBackground` | 状态栏小部件鼠标悬停高亮 | `#393B40` | `#EBECF0` |
| `StatusBar.Widget.hoverBackground` | 状态栏 Widget 悬停背景 | `#393B40` | `#EBECF0` |
| `Terminal.background` | 内置终端窗口背景色 | `#1E1F22` | `#FFFFFF` |
| `Terminal.foreground` | 内置终端标准文字色 | `#BCBEC3` | `#1E1F22` |
| `Terminal.selectionBackground` | 内置终端选中文本背景色 | `#2E436E` | `#D3E1FA` |

---

### 8. 徽标、通知与横幅 (Badge, Banner & Notification)

| UI Customization Key | 说明 | 推荐深色值 (Dark) | 推荐浅色值 (Light) |
| :--- | :--- | :--- | :--- |
| `Badge.background` | 数字提示徽标背景色 (如未读数) | `#4F5156` | `#D5D7DA` |
| `Badge.foreground` | 徽标文字色 | `#FFFFFF` | `#1E1F22` |
| `Notification.background` | 气泡通知窗口背景色 | `#2B2D30` | `#FFFFFF` |
| `Notification.borderColor` | 气泡通知边框颜色 | `#42454A` | `#D5D7DA` |
| `Editor.Notification.background` | 编辑器顶部横幅提示条 (Banner) 背景 | `#26282B` | `#F7F8FA` |
| `Editor.Notification.borderColor` | 编辑器顶部横幅边框 | `#393B40` | `#EBECF0` |

---

## 四、New UI 图标与调色板体系 (`icons` & `ColorPalette`)

在 IntelliJ New UI 中，所有官方图标均采用了 SVG 矢量格式，并内置了一套精准的色彩调色板系统（ColorPalette）。主题无需逐个替换数千个 SVG 文件，只需在 `icons.ColorPalette` 中映射关键色值即可全盘改变图标外观风格。

### 1. 全局图标色彩替换 (`ColorPalette`)

通过十六进制代码或官方语义命名键映射：

```json
{
  "icons": {
    "ColorPalette": {
      "#Actions.Grey": "#DFE1E5",
      "#Actions.GreyInline": "#7A7E85",
      "#Actions.Blue": "#3574F0",
      "#Actions.Green": "#629755",
      "#Actions.Red": "#D64D5B",
      "#Actions.Yellow": "#C29E49",
      
      "#Objects.Grey": "#DFE1E5",
      "#Objects.Blue": "#6A9BFA",
      "#Objects.Green": "#629755",
      "#Objects.Red": "#D64D5B",
      "#Objects.Yellow": "#C29E49",
      "#Objects.Purple": "#A276E8",
      "#Objects.Pink": "#F26E9C",
      "#Objects.BlackText": "#DFE1E5"
    }
  }
}
```

### 2. 官方上下文色板 (Actions & Objects)

- **`Actions.*` (工具栏操作图标类)**:
  - 用于顶部 Toolbar、运行/调试控制、Git Commit 按钮、编辑操作等高频交互图标。
  - 通常色彩更加克制，强调灰度与明确的单色动作高亮。
- **`Objects.*` (结构树/实体对象类)**:
  - 用于项目工程树中的文件类型图标（Java、TS、Vue、JSON）、类 (Class)、方法 (Method)、字段 (Field)、包 (Package)、数据库表 (Table) 等实体。
  - 色彩更丰富，帮助开发者一目了然区分类型。

### 3. 自定义 SVG 图标覆盖映射

若需要完全重绘并替换特定官方图标，可使用 `AllIcons.*` 键名指向插件内部自定义 SVG 路径：

```json
{
  "icons": {
    "AllIcons.General.GearPlain": "/icons/custom-gear.svg",
    "AllIcons.Nodes.Class": "/icons/nodes/custom-class.svg",
    "AllIcons.Toolwindows.ToolWindowProject": "/icons/toolwindows/custom-project.svg"
  }
}
```

---

## 五、官方主题调试与审查工具链 (Internal Mode)

JetBrains 官方在 IntelliJ Platform 中内置了极强的开发者调试工具。

### 1. 开启 JetBrains 平台 Internal Mode

1. 打开 IntelliJ IDEA / WebStorm / GoLand / PyCharm。
2. 点击菜单 **Help** > **Edit Custom Properties...**（若提示创建 `idea.properties`，点击 **Create**）。
3. 追加一行配置：
   ```properties
   idea.is.internal=true
   ```
4. 保存文件并 **重启 IDE**。

---

### 2. 使用 UI Inspector 实时定位 UI Key

开启 Internal Mode 后，菜单栏将出现 **Tools | Internal Actions** 选项：

1. 打开 **Tools | Internal Actions | UI | UI Inspector**（或按快捷键唤起）。
2. 在界面任意区域按住 <kbd>Ctrl</kbd> + <kbd>Alt</kbd>（macOS 上为 <kbd>Cmd</kbd> + <kbd>Option</kbd>）并 **点击目标 UI 控件**。
3. 弹出窗口将精确显示：
   - 目标组件的 Java Swing 完整类名（如 `com.intellij.openapi.wm.impl.headertoolbar.MainToolbar`）。
   - 当前使用的 `ColorKey` 或 `ThemeKey`（如 `MainToolbar.background`）。
   - 边框 `Insets`、尺寸 `Dimension` 与层级父子树。

---

### 3. 使用 UI Theme Color Picker & LaF Defaults

1. **UI Theme Color Picker**:
   - 路径：**Tools | Internal Actions | UI | Enable UI Theme Color Picker**。
   - 开启后鼠标悬停至任意界面元素即可显示当前使用的键值与 Hex 色值。
2. **LaF Defaults (Look and Feel 字典预览器)**:
   - 路径：**Tools | Internal Actions | UI | LaF Defaults**。
   - 提供了完整的当前平台激活 UI Key 列表，支持实时搜索（如 `ToolWindow`、`Tab`）、修改颜色并即时在界面上渲染生效。

---

## 六、从零构建并发布 New UI 主题插件工程

### 1. 推荐工程目录结构 (Gradle IntelliJ Platform Plugin)

官方推荐使用 **IntelliJ Platform Gradle Plugin 2.x** 构建主题插件：

```
shuimo-theme-intellij/
├── build.gradle.kts
├── settings.gradle.kts
├── gradle.properties
└── src/
    └── main/
        └── resources/
            ├── META-INF/
            │   ├── plugin.xml
            │   └── pluginIcon.svg
            └── themes/
                ├── shuimo-new-ui.theme.json
                └── shuimo-new-ui.xml
```

---

### 2. `plugin.xml` 清单配置

在 `src/main/resources/META-INF/plugin.xml` 中注册主题与代码配色：

```xml
<idea-plugin>
    <id>com.wangx.theme.shuimo</id>
    <name>Shuimo Theme (New UI)</name>
    <vendor email="wangx@example.com" url="https://github.com/wangx7/shuimo-theme">wangx</vendor>
    <description><![CDATA[
      Elegant Shuimo (水墨) New UI theme for IntelliJ IDEA, WebStorm, PyCharm, and GoLand.
    ]]></description>

    <depends>com.intellij.modules.platform</depends>

    <extensions defaultExtensionNs="com.intellij">
        <!-- 注册 UI 控件主题描述文件 -->
        <themeProvider id="com.wangx.theme.shuimo.newui" path="/themes/shuimo-new-ui.theme.json"/>
        <!-- 注册编辑器代码配色方案 -->
        <bundledColorScheme path="/themes/shuimo-new-ui.xml"/>
    </extensions>
</idea-plugin>
```

---

### 3. `build.gradle.kts` 构建配置

```kotlin
plugins {
    id("java")
    id("org.jetbrains.intellij.platform") version "2.1.0"
}

group = "com.wangx.theme"
version = "1.0.0"

repositories {
    mavenCentral()
    intellijPlatform {
        defaultRepositories()
    }
}

dependencies {
    intellijPlatform {
        intellijIdeaCommunity("2024.1.4")
    }
}

intellijPlatform {
    pluginConfiguration {
        id = "com.wangx.theme.shuimo"
        name = "Shuimo Theme (New UI)"
        version = project.version.toString()
    }
}
```

---

### 4. 本地运行、打包 (zip) 与 Marketplace 发布

1. **本地实时预览热运行**:
   ```bash
   ./gradlew runIde
   ```
   该命令会自动下载轻量级 IntelliJ IDEA 沙箱实例并安装主题插件供实时测试。

2. **构建打包离线安装包**:
   ```bash
   ./gradlew buildPlugin
   ```
   构建产物将在 `build/distributions/shuimo-theme-intellij-1.0.0.zip`，可直接在任意 JetBrains IDE 的 **Settings > Plugins > ⚙️ 齿轮 > Install Plugin from Disk...** 进行本地安装测试。

3. **发布到 JetBrains Marketplace**:
   - 登录 [JetBrains Marketplace Hub](https://plugins.jetbrains.com/)。
   - 点击 **Upload Plugin** 上传构建好的 `.zip` 文件。
   - 或配置 `publishPlugin { token.set("...") }` 通过 CI/CD 自动化流水线发布。

---

## 七、New UI 与 VS Code 主题色值快速映射表

若要将 VS Code 主题（如 `themes/shuimo-intellij-new-ui-theme.json`）移植或对照到 JetBrains New UI，可参考下表：

| VS Code Workbench Key | JetBrains New UI (`*.theme.json`) Key | 典型设计意图 |
| :--- | :--- | :--- |
| `titleBar.activeBackground` | `MainToolbar.background` | 顶部主工具栏/标题栏背景 |
| `titleBar.inactiveBackground`| `MainToolbar.inactiveBackground` | 失焦窗口顶部主工具栏背景 |
| `titleBar.border` | `MainToolbar.border` | 顶部工具栏下分割线 |
| `activityBar.background` | `ToolWindow.Stripe.background` | 侧边栏纯图标条背景 |
| `activityBar.activeBackground` | `ToolWindow.Button.selectedBackground` | 侧边栏当前激活面板的图标底色 |
| `activityBarBadge.background` | `Badge.background` | 未读数与徽标背景 |
| `sideBar.background` | `Tree.background` / `ToolWindow.Header.background` | 项目文件树与工具窗口面板背景 |
| `sideBar.border` | `ToolWindow.border` | 侧边栏与编辑区分割边框 |
| `editorGroupHeader.tabsBackground` | `EditorTabs.background` | 编辑器标签栏背景 |
| `tab.activeBackground` | `EditorTabs.underlinedTabBackground` | 当前激活标签页背景 |
| `tab.activeBorder` | `EditorTabs.underlineColor` | 当前激活标签页高亮指示线 |
| `tab.hoverBackground` | `EditorTabs.hoverBackground` | 标签页悬停背景 |
| `editor.background` | `Editor.background` (在 `.xml` 中定义) | 代码编辑区主底色 |
| `editorGutter.background` | `EditorGutter.background` (在 `.xml` 中定义) | 行号槽背景 |
| `quickInput.background` | `SearchEverywhere.Header.background` | 全局搜索与命令面板背景 |
| `input.background` | `TextField.background` | 输入框底色 |
| `button.background` | `Button.default.startBackground` / `Button.startBackground` | 主操作按钮底色 |
| `focusBorder` | `Component.focusColor` / `Component.focusedBorderColor` | 控件聚焦蓝色外发光边框 |
| `statusBar.background` | `StatusBar.background` | 底部状态栏背景 |
| `statusBar.border` | `StatusBar.borderColor` | 底部状态栏上边框 |
| `terminal.background` | `Terminal.background` | 内置终端底色 |
| `list.activeSelectionBackground`| `Tree.selectionBackground` / `List.selectionBackground` | 列表/树项选中背景色 |
| `list.hoverBackground` | `Tree.hoverBackground` / `List.hoverBackground` | 列表/树项悬停背景色 |

