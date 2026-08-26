# WebStorm / IntelliJ IDEA (JetBrains 平台) 主题与语法着色系统全景架构深度解析

> **官方参考源**: [JetBrains IntelliJ Platform SDK Docs](https://plugins.jetbrains.com/docs/intellij/themes-intro.html), [IntelliJ Community Core Repository (`JetBrains/intellij-community`)](https://github.com/JetBrains/intellij-community)  
> **核心源码模块**: `com.intellij.openapi.editor.colors.TextAttributesKey`, `com.intellij.openapi.editor.DefaultLanguageHighlighterColors`, `com.intellij.ide.ui.UITheme`, `com.intellij.lang.annotation.Annotator`  
> **核心机制**: JFlex 词法分词 + PSI 语法树语义着色 (Annotator / HighlightingPass) + `TextAttributesKey` 树状继承级联 + UI Theme JSON 控件样式渲染

---

## 目录
- [一、JetBrains IntelliJ 平台语法与主题全景架构](#一jetbrains-intellij-平台语法与主题全景架构)
  - [1. 双轨高亮引擎：词法分词与 PSI 语义渲染](#1-双轨高亮引擎词法分词与-psi-语义渲染)
  - [2. VS Code vs JetBrains 核心架构与机制深度对照表](#2-vs-code-vs-jetbrains-核心架构与机制深度对照表)
  - [3. 主题架构双层体系：UI Theme 与 Editor Color Scheme](#3-主题架构双层体系ui-theme-与-editor-color-scheme)
- [二、核心文本属性与层级继承机制 (`TextAttributesKey`)](#二核心文本属性与层级继承机制-textattributeskey)
  - [1. 树状继承与回退机制 (Fallback Hierarchy)](#1-树状继承与回退机制-fallback-hierarchy)
  - [2. `DefaultLanguageHighlighterColors` 核心标准根节点速查表](#2-defaultlanguagehighlightercolors-核心标准根节点速查表)
  - [3. 文本属性数据结构与样式定义 (Font Type & Effect Type)](#3-文本属性数据结构与样式定义-font-type--effect-type)
- [三、WebStorm 前端专精高亮规范 (JS / TS / Vue / HTML / CSS)](#三webstorm-前端专精高亮规范-js--ts--vue--html--css)
  - [1. JavaScript & TypeScript 专属高亮属性键](#1-javascript--typescript-专属高亮属性键)
  - [2. Vue SFC 在 WebStorm 中的高亮实现机制与特殊 Key](#2-vue-sfc-在-webstorm-中的高亮实现机制与特殊-key)
  - [3. HTML / XML 与 CSS / SCSS / Less 属性键](#3-html--xml-与-css--scss--less-属性键)
- [四、JetBrains UI 主题规范 (`*.theme.json`) 深度剖析](#四jetbrains-ui-主题规范-themejson-深度剖析)
  - [1. 主题清单与元数据规范](#1-主题清单与元数据规范)
  - [2. 核心 UI 组件色值规范矩阵](#2-核心-ui-组件色值规范矩阵)
  - [3. 图标色板覆盖与替换 (Icon Palettes)](#3-图标色板覆盖与替换-icon-palettes)
- [五、VS Code 到 WebStorm / IntelliJ IDEA 映射对照速查表](#五vs-code-到-webstorm--intellij-idea-映射对照速查表)
  - [1. 语法 Token 映射表 (TextMate / LSP -> JetBrains TextAttributesKey)](#1-语法-token-映射表-textmate--lsp---jetbrains-textattributeskey)
  - [2. UI 键值映射表 (VS Code Workbench -> JetBrains UI Theme)](#2-ui-键值映射表-vs-code-workbench---jetbrains-ui-theme)
- [六、实战落地：从零构建水墨主题 (Shuimo Theme) JetBrains 插件](#六实战落地从零构建水墨主题-shuimo-theme-jetbrains-插件)
  - [1. 插件项目结构范式](#1-插件项目结构范式)
  - [2. 插件清单 `plugin.xml` 声明](#2-插件清单-pluginxml-声明)
  - [3. 水墨·浅 与 水墨·深 完整 XML 配色方案范式](#3-水墨浅-与-水墨深-完整-xml-配色方案范式)
- [七、主题调试、验证与发布指南](#七主题调试验证与发布指南)
  - [1. 官方调试工具 (UI Inspector / PsiViewer / Scheme Preview)](#1-官方调试工具-ui-inspector--psiviewer--scheme-preview)
  - [2. 本地打包与安装验证](#2-本地打包与安装验证)
  - [3. 发布到 JetBrains Marketplace 流程](#3-发布到-jetbrains-marketplace-流程)

---

## 一、JetBrains IntelliJ 平台语法与主题全景架构

### 1. 双轨高亮引擎：词法分词与 PSI 语义渲染

与 VS Code 类似，JetBrains 平台（WebStorm、IntelliJ IDEA、PyCharm、GoLand 等）也采用双层递进式高亮架构，但底层建立在编译原理级别强大的 **PSI (Program Structure Interface)** 体系之上：

```
                           ┌───────────────────────────────┐
                           │      源码文本 (Source Code)    │
                           └───────────────┬───────────────┘
                                           │
                   ┌───────────────────────┴───────────────────────┐
                   ▼                                               ▼
     ┌───────────────────────────┐                   ┌───────────────────────────┐
     │ 第一层：Lexer 词法高亮    │                   │ 第二层：PSI 语义分析层    │
     │  (SyntaxHighlighter /     │                   │  (Annotator /             │
     │   JFlex Lexer)            │                   │   HighlightVisitor)       │
     ├───────────────────────────┤                   ├───────────────────────────┤
     │ • 基于 JFlex 状态机词法分析│                   │ • 基于完整 AST / PSI 树   │
     │ • 毫秒级即时分词 (无延迟) │                   │ • 跨文件引用解析与符号推导│
     │ • 识别关键字/字面量/注释/标点│                   │ • 异步后台 HighlightingPass│
     │ • 产生: IElementType 映射 │                   │ • 产生: 语义 TextAttributes│
     └─────────────┬─────────────┘                   └─────────────┬─────────────┘
                   │                                               │
                   │  基础属性 (如 DEFAULT_KEYWORD)                │  语义属性 (如 JS.GLOBAL_FUNCTION)
                   ▼                                               ▼
     ┌───────────────────────────────────────────────────────────────────────────┐
     │                EditorColorsScheme (文本样式层级合并与渲染器)               │
     │            (com.intellij.openapi.editor.colors.EditorColorsScheme)        │
     ├───────────────────────────────────────────────────────────────────────────┤
     │ 1. 优先读取当前激活方案针对该具体 `TextAttributesKey` 的显式配置         │
     │ 2. 若未显式配置，沿 `fallbackAttributeKey` 树向上查找父级通用规则        │
     │ 3. 若继承链均未配置，回退至 `DefaultLanguageHighlighterColors` 根节点     │
     │ 4. 计算并合成样式：FOREGROUND, BACKGROUND, FONT_TYPE, EFFECT_TYPE/COLOR    │
     └─────────────────────────────────────┬─────────────────────────────────────┘
                                           │
                                           ▼
                           ┌───────────────────────────────┐
                           │   EditorComponent 最终像素渲染 │
                           └───────────────────────────────┘
```

---

### 2. VS Code vs JetBrains 核心架构与机制深度对照表

| 维度 | VS Code 语法高亮体系 | JetBrains (WebStorm / IDEA) 语法高亮体系 |
| :--- | :--- | :--- |
| **词法分词引擎** | `vscode-textmate` (基于 Oniguruma 正则表达式) | `JFlex` (编译原理 DFA 状态机，超高性能) |
| **语义分析底座** | LSP (Language Server Protocol) 异步返回 Token 数组 | `PSI` (内存级强类型 AST + 实时符号索引服务) |
| **规则选择器语法** | 点分隔 Scope 字符串 (如 `entity.name.function`) | Java 强类型枚举/常量类 `TextAttributesKey` |
| **匹配与回退机制** | 最长前缀特异性得分算法 (Specificity Scoring) | 单继承/多重回退继承链 (`fallbackAttributeKey`) |
| **UI 主题定义格式** | 单个 JSON 文件 (`contributes.themes`) | `*.theme.json` (UI 控件) + `*.xml`/`.icls` (代码配色) |
| **组件/变量精准度** | 依赖 LSP 语义插件返回 | 原生深度索引（无论是否安装插件，类型推导与引用极其精准） |

---

### 3. 主题架构双层体系：UI Theme 与 Editor Color Scheme

JetBrains 将主题划分为两个解耦的核心部分：

1. **UI 主题定义文件 (`*.theme.json`)**：
   - 负责 IDE 工作台所有 Swing / Compose 控件的颜色（边框、窗口、树、标签页、按钮、滚动条、对话框、图标重着色等）。
2. **代码着色方案文件 (`*.xml` 或 `*.icls`)**：
   - 负责编辑器内部的所有文本属性、行号、光标、高亮行、语法高亮、Diff 对比、控制台 Terminal 着色等。
   - 在 `*.theme.json` 中通过 `"editorScheme": "/themes/my-theme.xml"` 进行关联绑定。

---

## 二、核心文本属性与层级继承机制 (`TextAttributesKey`)

### 1. 树状继承与回退机制 (Fallback Hierarchy)

在 JetBrains 平台中，每个具体语言的语法高亮键都继承自一个**通用的抽象根键**（定义于 `DefaultLanguageHighlighterColors` 或 `HighlighterColors`）。

**继承树范例**：
```
DEFAULT_IDENTIFIER (通用标识符)
  ├── DEFAULT_FUNCTION_DECLARATION (函数声明)
  │     ├── JS.GLOBAL_FUNCTION (JS全局函数)
  │     └── TS.FUNCTION_DECLARATION (TS函数声明)
  ├── DEFAULT_FUNCTION_CALL (函数调用)
  ├── DEFAULT_LOCAL_VARIABLE (局部变量)
  │     └── JS.LOCAL_VARIABLE (JS局部变量)
  └── DEFAULT_GLOBAL_VARIABLE (全局变量)
        └── JS.GLOBAL_VARIABLE (JS全局变量)
```

> **最佳实践原则**：主题作者**无需为每种语言的每个属性编写规则**。只需精心配置好 `DefaultLanguageHighlighterColors` 中的通用根键，所有语言（Java、JavaScript、TypeScript、Vue、Python、Go、Rust、HTML、CSS 等）就会自动获得协调一致的视觉风格；仅在需要对特定语言（如 Vue 指令、TS 泛型）进行特化强调时，再去覆盖具体的子键。

---

### 2. `DefaultLanguageHighlighterColors` 核心标准根节点速查表

| 标准通用根键 (`TextAttributesKey`) | 含义与适用范围 | 对应 VS Code 概念 |
| :--- | :--- | :--- |
| `DEFAULT_KEYWORD` | 核心控制流、声明关键字 (`if`, `for`, `const`, `return`) | `keyword.control`, `storage.type` |
| `DEFAULT_IDENTIFIER` | 默认标识符（未特化变量/符号） | `variable`, `source` |
| `DEFAULT_FUNCTION_DECLARATION`| 函数/方法定义与声明处的名称 | `entity.name.function` |
| `DEFAULT_FUNCTION_CALL` | 函数/方法的调用与执行 | `entity.name.function`, `variable.function` |
| `DEFAULT_CLASS_NAME` | 类声明及其实例化引用 | `entity.name.type.class` |
| `DEFAULT_INTERFACE_NAME` | 接口声明及类型注解 | `entity.name.type.interface` |
| `DEFAULT_CLASS_REFERENCE` | 类符号引用与静态访问 | `support.class` |
| `DEFAULT_LOCAL_VARIABLE` | 局部变量 | `variable.other.readwrite` |
| `DEFAULT_GLOBAL_VARIABLE` | 全局变量/顶层作用域变量 | `variable.other.readwrite.global` |
| `DEFAULT_PARAMETER` | 函数形参及解构参数 | `variable.parameter` |
| `DEFAULT_INSTANCE_FIELD` | 实例属性/对象字段 (`this.foo`, `user.name`) | `variable.other.property` |
| `DEFAULT_STATIC_FIELD` | 类的静态常量/静态属性 (`Math.PI`) | `variable.other.constant.property` |
| `DEFAULT_STATIC_METHOD` | 类的静态方法 (`Object.keys()`) | `entity.name.function.member.static` |
| `DEFAULT_STRING` | 普通字符串字面量 (`"hello"`, `'world'`) | `string.quoted` |
| `DEFAULT_VALID_STRING_ESCAPE` | 字符串合法转义序列 (`\n`, `\t`, `\u0020`) | `constant.character.escape` |
| `DEFAULT_INVALID_STRING_ESCAPE`| 非法/未识别的转义序列 | `invalid.illegal` |
| `DEFAULT_NUMBER` | 数值字面量（整数、浮点数、十六进制） | `constant.numeric` |
| `DEFAULT_CONSTANT` | 内置或只读常量 (`true`, `false`, `null`, `undefined`) | `constant.language` |
| `DEFAULT_LINE_COMMENT` | 单行注释 (`//`, `#`) | `comment.line` |
| `DEFAULT_BLOCK_COMMENT` | 多行块注释 (`/* ... */`) | `comment.block` |
| `DEFAULT_DOC_COMMENT` | 文档注释外层 (`/** ... */`) | `comment.block.documentation` |
| `DEFAULT_DOC_COMMENT_TAG` | 文档注释标签 (`@param`, `@returns`, `@type`) | `storage.type.class.jsdoc` |
| `DEFAULT_DOC_COMMENT_TAG_VALUE`| 文档注释标签参数名称 | `variable.parameter.documentation` |
| `DEFAULT_TAG` | 标记语言标签名 (`<div>`, `<template>`) | `entity.name.tag` |
| `DEFAULT_ATTRIBUTE` | 标记语言属性名 (`class`, `src`, `id`) | `entity.other.attribute-name` |
| `DEFAULT_SEMICOLON` | 分号界定符 (`;`) | `punctuation.terminator` |
| `DEFAULT_COMMA` | 逗号分隔符 (`,`) | `punctuation.separator.comma` |
| `DEFAULT_DOT` | 属性访问点号 (`.`) | `punctuation.accessor` |
| `DEFAULT_PARENTHS` | 圆括号 (`(`, `)`) | `punctuation.definition.parameters` |
| `DEFAULT_BRACKETS` | 方括号 (`[`, `]`) | `punctuation.definition.array` |
| `DEFAULT_BRACES` | 花括号 (`{`, `}`) | `punctuation.definition.block` |
| `DEFAULT_OPERATION_SIGN` | 运算符 (`+`, `-`, `*`, `===`, `&&`) | `keyword.operator` |

---

### 3. 文本属性数据结构与样式定义 (Font Type & Effect Type)

在 XML 配色方案中，每个 `<option name="...">` 对应一个 `TextAttributesKey` 的属性配置：

```xml
<option name="DEFAULT_KEYWORD">
  <value>
    <option name="FOREGROUND" value="9D2933" />
    <option name="BACKGROUND" value="F6F5E1" />
    <option name="FONT_TYPE" value="1" />
    <option name="EFFECT_TYPE" value="1" />
    <option name="EFFECT_COLOR" value="9D2933" />
  </value>
</option>
```

#### (1) `FONT_TYPE` 字体字重与样式取值
- `0`: **Plain**（常规正常文本）
- `1`: **Bold**（粗体）
- `2`: **Italic**（斜体）
- `3`: **Bold Italic**（粗斜体）

#### (2) `EFFECT_TYPE` 下划线与修饰效果取值
- `0`: **LINE_UNDERSCORE**（普通单下划线）
- `1`: **WAVE_UNDERSCORE**（波浪线，常用于警告/语法提示）
- `2`: **BOXED**（矩形线框）
- `3`: **STRIKEOUT**（中划线/删除线，用于 `@deprecated` 过时 API）
- `4`: **BOLD_DOTTED_LINE**（粗点状虚线）
- `5`: **SEARCH_RESULT**（搜索命中）
- `6`: **BOLD_LINE_UNDERSCORE**（粗单下划线）

---

## 三、WebStorm 前端专精高亮规范 (JS / TS / Vue / HTML / CSS)

### 1. JavaScript & TypeScript 专属高亮属性键

WebStorm 在 JavaScript 与 TypeScript 解析上具有极高的原生精准度，以下为常用特化键：

| 专属 Key (`TextAttributesKey`) | 作用场景与示例 | 推荐样式 |
| :--- | :--- | :--- |
| `JS.GLOBAL_VARIABLE` | 全局变量（如 `window`, `document`, `process`） | 斜体或深色墨色 |
| `JS.GLOBAL_FUNCTION` | 全局函数调用（如 `parseInt`, `setTimeout`） | 墨色 |
| `JS.LOCAL_VARIABLE` | 局部作用域变量 (`let count = 0`) | 墨玉深灰 |
| `JS.PARAMETER` | 函数形参及解构绑定参数 | 浅墨灰/斜体 |
| `JS.INSTANCE_MEMBER_VARIABLE` | 对象/实例属性访问 (`user.profile.age`) | 墨玉黑 |
| `JS.INSTANCE_MEMBER_FUNCTION` | 实例方法调用 (`arr.map()`, `list.filter()`) | 墨色 |
| `JS.PRIMITIVE.TYPE` | 基本类型关键字 (`string`, `number`, `boolean`, `any`) | 赭石/赤金 |
| `TS.TYPE_PARAMETER` | 泛型类型参数 (`<T, K extends keyof T>`) | 黛蓝/斜体 |
| `TS.INTERFACE` | TS 接口声明 (`interface UserItem`) | 浓墨/粗体 |
| `TS.TYPE_GUARD` | 类型保护与断言 (`is`, `as`, `keyof`, `typeof`) | 朱砂红/粗体 |
| `JSX_ATTRIBUTE` | JSX/TSX 标签属性 (`onClick={...}`) | 黛蓝/墨灰 |
| `PROMISES_RESOLVED_MEMBER` | Promise 链式解析成员 | 特殊标识高亮 |

---

### 2. Vue SFC 在 WebStorm 中的高亮实现机制与特殊 Key

WebStorm 原生内置官方 Vue 插件，基于 Vue 虚拟语法树分发高亮：

| Vue 专属 Key | 作用场景与示例 | 推荐水墨样式 |
| :--- | :--- | :--- |
| `VUE_DIRECTIVE` | Vue 核心指令名 (`v-if`, `v-for`, `v-model`, `v-show`) | 朱砂红 (`#9D2933`) / 粗体 |
| `VUE_INTERPOLATION_DELIMITERS` | 插值表达式双大括号界定符 (`{{`, `}}`) | 黛蓝 (`#315D8C`) / 粗体 |
| `VUE_SCRIPT_TAG` | `<script>` 标签本体 | 赭石/朱砂 |
| `VUE_TEMPLATE_TAG` | `<template>` 顶层标签本体 | 赭石/朱砂 |
| `VUE_STYLE_TAG` | `<style>` 顶层标签本体 | 赭石/朱砂 |
| `VUE_CUSTOM_TAG` | 自定义 SFC 块标签 (`<i18n>`, `<docs>`) | 苍翠绿 |

---

### 3. HTML / XML 与 CSS / SCSS / Less 属性键

| 属性键 | 说明 | 对应水墨配色 |
| :--- | :--- | :--- |
| `HTML_TAG_NAME`, `XML_TAG_NAME` | 标签名称 (`<div>`, `<span>`, `<button>`) | 浓墨 (`#1D1F21`) / 粗体 |
| `HTML_ATTRIBUTE_NAME` | HTML 属性名 (`class`, `id`, `src`, `href`) | 黛蓝 (`#2E59A7`) |
| `HTML_ATTRIBUTE_VALUE` | HTML 属性字符串值 (`"container"`) | 黛蓝/烟墨 |
| `CSS.PROPERTY_NAME` | CSS 样式属性名 (`color`, `display`, `padding`) | 墨玉黑 (`#3B3D42`) |
| `CSS.PROPERTY_VALUE` | CSS 属性具体值 (`flex`, `absolute`, `none`) | 赭石 (`#B05628`) |
| `CSS.FUNCTION` | CSS 内置函数 (`calc()`, `var()`, `rgba()`) | 黛蓝 (`#315D8C`) |
| `CSS.CLASS_NAME` | 类选择器 (`.title`, `.card`) | 浓墨 (`#1D1F21`) / 粗体 |
| `CSS.IDENT` / `CSS.HASH` | ID 选择器 (`#app`, `#header`) | 浓墨 / 粗体 |
| `CSS.PSEUDO` | 伪类与伪元素 (`:hover`, `::after`) | 朱砂红 (`#9D2933`) |
| `CSS.VARIABLE` | CSS 自定义变量 (`--primary-color`) | 黛青 (`#2A7078`) |

---

## 四、JetBrains UI 主题规范 (`*.theme.json`) 深度剖析

### 1. 主题清单与元数据规范

一个标准的 JetBrains UI 主题由 `*.theme.json` 文件定义，其顶层规范如下：

```json
{
  "name": "水墨·浅",
  "author": "wangx123",
  "dark": false,
  "editorScheme": "/themes/shuimo-qian.xml",
  "ui": {
    "*": {
      "background": "#F6F5E1",
      "foreground": "#2A2C30",
      "selectionBackground": "#315D8C2E",
      "selectionForeground": "#232527",
      "focusColor": "#9D2933",
      "borderColor": "#26262620",
      "separatorColor": "#26262618"
    }
  },
  "icons": {
    "ColorPalette": {
      "Actions.Red": "#9D2933",
      "Actions.Yellow": "#8A6D1F",
      "Actions.Green": "#4C7548",
      "Actions.Blue": "#315D8C",
      "Actions.Grey": "#5C5852"
    }
  }
}
```

---

### 2. 核心 UI 组件色值规范矩阵

JetBrains UI 规范采用分层键名定义各 Swing 控件与工作区容器样式：

```
┌─────────────────────────────────────────────────────────────┐
│ Window Header / MainToolbar (主工具栏与标题栏)               │
├──────────────┬──────────────────────────────┬───────────────┤
│ ToolWindow   │ EditorTabs (编辑器标签页栏)  │ ToolWindow    │
│ (左侧工具窗) │──────────────────────────────│ (右侧工具窗)  │
│              │ Editor Gutter (行号与断点槽) │               │
│ Project Tree │ ──────────────────────────── │ Structure     │
│ (项目树)     │ Editor Canvas (编辑器主画布) │ (代码大纲)    │
│              │                              │               │
├──────────────┴──────────────────────────────┴───────────────┤
│ StatusBar (底部状态栏)                                      │
└─────────────────────────────────────────────────────────────┘
```

| UI 模块分类 | JetBrains UI Key (`*.theme.json`) | 作用说明 |
| :--- | :--- | :--- |
| **通用全局** | `*.background`, `*.foreground` | 全局基础背景色与前景色 |
| | `*.focusColor`, `*.selectionBackground` | 焦点指示器边框色与选中态背景 |
| **主标题栏/工具栏** | `MainToolbar.background`, `TitlePane.background` | 顶层标题栏与主操作工具栏底色 |
| **侧边栏与工具窗口** | `ToolWindow.Header.background` | 工具窗口标签栏底色 |
| | `ToolWindow.Button.selectedBackground` | 激活工具窗口按钮背景 |
| | `Tree.background`, `Tree.foreground` | 项目文件树背景与文字颜色 |
| | `Tree.selectionBackground` | 项目树选中项背景高亮 |
| **编辑器选项卡** | `EditorTabs.background` | 编辑器标签栏底色 |
| | `EditorTabs.underlinedTabBackground` | 激活标签页的底色 |
| | `EditorTabs.underlineColor` | 激活标签页下方的强调指示条（如水墨朱砂红） |
| **弹出层与菜单** | `Popup.background`, `Popup.Border.color` | 智能提示补全浮窗、右键上下文菜单底色与边框 |
| | `List.selectionBackground` | 补全列表或查找结果高亮选中背景 |
| **输入控件** | `TextField.background`, `TextField.foreground` | 文本输入框底色与输入字色 |
| | `ComboBox.background`, `ComboBox.ArrowButton.iconColor`| 下拉选择框底色与箭头颜色 |
| | `Button.startBackground`, `Button.endBackground` | 按钮渐变底色（扁平化主题通常设为一致单色） |
| **滚动条** | `ScrollBar.thumb`, `ScrollBar.thumbHovered` | 滚动条滑块默认与悬浮态颜色 |
| **状态栏** | `StatusBar.background`, `StatusBar.borderColor` | 底部状态栏背景与分割线颜色 |

---

### 3. 图标色板覆盖与替换 (Icon Palettes)

JetBrains 新 UI (New UI) 支持在 `icons.ColorPalette` 中全局覆盖 SVG 图标色系，使 IDE 内置动作、文件夹、文件类型图标契合水墨风味：

```json
"icons": {
  "ColorPalette": {
    "Actions.Red": "#9D2933",
    "Actions.Yellow": "#8A6D1F",
    "Actions.Green": "#4C7548",
    "Actions.Blue": "#315D8C",
    "Actions.Grey": "#6E7278",
    "Actions.GreyInline.Dark": "#5C5852",
    "Objects.Red": "#9D2933",
    "Objects.Yellow": "#8A6D1F",
    "Objects.Green": "#4C7548",
    "Objects.Blue": "#315D8C",
    "Objects.Purple": "#7A5B8C",
    "Objects.Grey": "#5C5852"
  }
}
```

---

## 五、VS Code 到 WebStorm / IntelliJ IDEA 映射对照速查表

### 1. 语法 Token 映射表 (TextMate / LSP -> JetBrains TextAttributesKey)

| 语法分类 | VS Code (TextMate Scope / LSP Token) | JetBrains 核心属性 (`TextAttributesKey`) |
| :--- | :--- | :--- |
| **控制流关键字** | `keyword.control`, `keyword:keyword` | `DEFAULT_KEYWORD` |
| **声明存储修饰符**| `storage.type`, `storage.modifier` | `DEFAULT_KEYWORD` |
| **函数声明** | `entity.name.function`, `function.declaration` | `DEFAULT_FUNCTION_DECLARATION` |
| **函数/方法调用** | `entity.name.function.member`, `function`, `method`| `DEFAULT_FUNCTION_CALL` |
| **类名定义** | `entity.name.type.class`, `class` | `DEFAULT_CLASS_NAME` |
| **接口定义** | `entity.name.type.interface`, `interface` | `DEFAULT_INTERFACE_NAME` |
| **泛型类型参数** | `entity.name.type.parameter`, `typeParameter` | `TS.TYPE_PARAMETER`, `TYPE_PARAMETER_NAME` |
| **普通局部变量** | `variable.other.readwrite`, `variable` | `DEFAULT_LOCAL_VARIABLE` / `JS.LOCAL_VARIABLE` |
| **全局/只读常量** | `variable.other.constant`, `variable.readonly` | `DEFAULT_CONSTANT` / `JS.GLOBAL_VARIABLE` |
| **对象属性访问** | `variable.other.property`, `property` | `DEFAULT_INSTANCE_FIELD` |
| **静态类属性** | `variable.other.constant.property`, `*.static` | `DEFAULT_STATIC_FIELD` |
| **函数形参** | `variable.parameter`, `parameter` | `DEFAULT_PARAMETER` |
| **字符串字面量** | `string.quoted`, `string` | `DEFAULT_STRING` |
| **字符转义** | `constant.character.escape` | `DEFAULT_VALID_STRING_ESCAPE` |
| **数值字面量** | `constant.numeric`, `number` | `DEFAULT_NUMBER` |
| **布尔/空值常量** | `constant.language.boolean`, `constant.language.null`| `DEFAULT_KEYWORD` / `DEFAULT_CONSTANT` |
| **单行注释** | `comment.line`, `comment` | `DEFAULT_LINE_COMMENT` |
| **块注释/文档** | `comment.block.documentation` | `DEFAULT_DOC_COMMENT` |
| **文档注解标签** | `storage.type.class.comment`, `punctuation.tag` | `DEFAULT_DOC_COMMENT_TAG` |
| **Vue 指令** | `keyword.control.conditional.vue`, `directive` | `VUE_DIRECTIVE` |
| **Vue 模板插值** | `punctuation.definition.interpolation` | `VUE_INTERPOLATION_DELIMITERS` |
| **HTML 标签名** | `entity.name.tag.html`, `entity.name.tag` | `HTML_TAG_NAME`, `XML_TAG_NAME` |
| **HTML 属性名** | `entity.other.attribute-name.html` | `HTML_ATTRIBUTE_NAME` |
| **CSS 属性名** | `support.type.property-name.css` | `CSS.PROPERTY_NAME` |
| **CSS 属性值** | `support.constant.property-value.css` | `CSS.PROPERTY_VALUE` |

---

### 2. UI 键值映射表 (VS Code Workbench -> JetBrains UI Theme)

| VS Code Workbench Key (`themes/*.json`) | JetBrains UI Key (`*.theme.json`) |
| :--- | :--- |
| `editor.background` | `Editor.background` |
| `editor.foreground` | `Editor.foreground` |
| `editorLineNumber.foreground` | `EditorGutter.lineNumberColor` |
| `editorLineNumber.activeForeground` | `EditorGutter.currentLineNumberColor` |
| `editorCursor.foreground` | `Editor.caretColor` |
| `editor.lineHighlightBackground` | `Editor.caretRowColor` |
| `editor.selectionBackground` | `Editor.selectionBackground` |
| `sideBar.background`, `activityBar.background` | `ToolWindow.Header.background`, `ToolWindow.background` |
| `sideBar.foreground` | `ToolWindow.Header.foreground` |
| `list.hoverBackground` | `Tree.hoverBackground`, `List.hoverBackground` |
| `list.activeSelectionBackground` | `Tree.selectionBackground`, `List.selectionBackground` |
| `tab.activeBackground` | `EditorTabs.underlinedTabBackground` |
| `tab.activeBorderTop`, `activityBarBadge.background` | `EditorTabs.underlineColor`, `TabbedPane.underlineColor` |
| `statusBar.background` | `StatusBar.background` |
| `statusBar.foreground` | `StatusBar.foreground` |
| `input.background`, `dropdown.background` | `TextField.background`, `ComboBox.background` |
| `input.border`, `dropdown.border` | `TextField.borderColor`, `ComboBox.borderColor` |
| `focusBorder` | `*.focusColor`, `Component.focusColor` |

---

## 六、实战落地：从零构建水墨主题 (Shuimo Theme) JetBrains 插件

### 1. 插件项目结构范式

为 JetBrains 平台打包发布的水墨主题插件项目目录结构如下：

```
shuimo-theme-intellij/
├── src/
│   └── main/
│       └── resources/
│           ├── META-INF/
│           │   ├── plugin.xml             # 插件核心清单元数据与扩展点贡献
│           │   └── pluginIcon.svg         # 插件市场高清图标 (40x40 & 80x80)
│           ├── themes/
│           │   ├── shuimo-qian.theme.json # 水墨·浅 UI 主题定义
│           │   ├── shuimo-qian.xml        # 水墨·浅 编辑器代码着色方案
│           │   ├── shuimo-shen.theme.json # 水墨·深 UI 主题定义
│           │   └── shuimo-shen.xml        # 水墨·深 编辑器代码着色方案
├── build.gradle.kts                       # Gradle 构建脚本 (IntelliJ Gradle Plugin)
└── settings.gradle.kts
```

---

### 2. 插件清单 `plugin.xml` 声明

在 `src/main/resources/META-INF/plugin.xml` 中通过 `<themeProvider>` 注册主题：

```xml
<idea-plugin>
    <id>com.wangx.shuimo.theme</id>
    <name>Shuimo Theme (水墨)</name>
    <vendor email="36002218@qq.com" url="https://github.com/wangx7/shuimo-theme">wangx123</vendor>

    <description><![CDATA[
    <h1>水墨 Theme (Shuimo Theme)</h1>
    <p>几抹淡墨涵万象，一帧素宣蕴乾坤。</p>
    <p>一款基于中国传统水墨山水画意象打造的高雅配色主题，现已原生适配 WebStorm 与 IntelliJ IDEA 平台。</p>
    ]]></description>

    <!-- 声明兼容所有 IntelliJ 平台产品 (WebStorm, IDEA, PyCharm, GoLand 等) -->
    <depends>com.intellij.modules.platform</depends>

    <extensions defaultExtensionNs="com.intellij">
        <!-- 注册 水墨·浅 主题 -->
        <themeProvider id="shuimo-qian" path="/themes/shuimo-qian.theme.json" />
        <!-- 注册 水墨·深 主题 -->
        <themeProvider id="shuimo-shen" path="/themes/shuimo-shen.theme.json" />
    </extensions>
</idea-plugin>
```

---

### 3. 水墨·浅 与 水墨·深 完整 XML 配色方案范式

#### (1) `shuimo-qian.xml` (水墨·浅 编辑器配色方案)

```xml
<scheme name="水墨·浅" version="142" parent_scheme="Default">
  <metaInfo>
    <property name="created">2026-08-26</property>
    <property name="ide">WebStorm</property>
    <property name="ideVersion">2024.1.0.0</property>
    <property name="originalScheme">水墨·浅</property>
  </metaInfo>
  <colors>
    <option name="ADDED_LINES_COLOR" value="4C7548" />
    <option name="CARET_COLOR" value="9D2933" />
    <option name="CARET_ROW_COLOR" value="2626260D" />
    <option name="CONSOLE_BACKGROUND_KEY" value="F6F5E1" />
    <option name="DELETED_LINES_COLOR" value="A23B29" />
    <option name="DOCUMENTATION_COLOR" value="FAF9F0" />
    <option name="FILESTATUS_ADDED" value="4C7548" />
    <option name="FILESTATUS_MODIFIED" value="315D8C" />
    <option name="FILESTATUS_NOT_CHANGED_IMMEDIATE" value="315D8C" />
    <option name="GUTTER_BACKGROUND" value="F6F5E1" />
    <option name="INDENT_GUIDE" value="5A5F6614" />
    <option name="LINE_NUMBERS_COLOR" value="5C5852A0" />
    <option name="LINE_NUMBER_ON_CARET_ROW_COLOR" value="232527" />
    <option name="MODIFIED_LINES_COLOR" value="315D8C" />
    <option name="RIGHT_MARGIN_COLOR" value="5A5F6614" />
    <option name="SELECTED_INDENT_GUIDE" value="5A5F6673" />
    <option name="SELECTED_TEARLINE_COLOR" value="9D2933" />
    <option name="SELECTION_BACKGROUND" value="315D8C26" />
    <option name="SELECTION_FOREGROUND" value="232527" />
    <option name="TEARLINE_COLOR" value="26262618" />
    <option name="WHITESPACES" value="5A5F6636" />
  </colors>
  <attributes>
    <!-- 基础关键字：朱砂红粗体 -->
    <option name="DEFAULT_KEYWORD">
      <value>
        <option name="FOREGROUND" value="9D2933" />
        <option name="FONT_TYPE" value="1" />
      </value>
    </option>
    <!-- 通用标识符与基础前景色 -->
    <option name="DEFAULT_IDENTIFIER">
      <value>
        <option name="FOREGROUND" value="2A2C30" />
      </value>
    </option>
    <!-- 函数与方法：墨色 -->
    <option name="DEFAULT_FUNCTION_DECLARATION">
      <value>
        <option name="FOREGROUND" value="2A2C30" />
        <option name="FONT_TYPE" value="1" />
      </value>
    </option>
    <option name="DEFAULT_FUNCTION_CALL">
      <value>
        <option name="FOREGROUND" value="2A2C30" />
      </value>
    </option>
    <!-- 类与接口：浓墨黑粗体 -->
    <option name="DEFAULT_CLASS_NAME">
      <value>
        <option name="FOREGROUND" value="1D1F21" />
        <option name="FONT_TYPE" value="1" />
      </value>
    </option>
    <option name="DEFAULT_INTERFACE_NAME">
      <value>
        <option name="FOREGROUND" value="1D1F21" />
        <option name="FONT_TYPE" value="1" />
      </value>
    </option>
    <!-- 变量与属性：墨玉灰 -->
    <option name="DEFAULT_LOCAL_VARIABLE">
      <value>
        <option name="FOREGROUND" value="3B3D42" />
      </value>
    </option>
    <option name="DEFAULT_INSTANCE_FIELD">
      <value>
        <option name="FOREGROUND" value="3B3D42" />
      </value>
    </option>
    <option name="DEFAULT_PARAMETER">
      <value>
        <option name="FOREGROUND" value="3B3D42" />
        <option name="FONT_TYPE" value="2" />
      </value>
    </option>
    <!-- 常量与只读属性：黛蓝 -->
    <option name="DEFAULT_CONSTANT">
      <value>
        <option name="FOREGROUND" value="2E59A7" />
      </value>
    </option>
    <option name="DEFAULT_STATIC_FIELD">
      <value>
        <option name="FOREGROUND" value="2E59A7" />
      </value>
    </option>
    <!-- 字符串字面量：黛蓝 -->
    <option name="DEFAULT_STRING">
      <value>
        <option name="FOREGROUND" value="2E59A7" />
      </value>
    </option>
    <!-- 数值字面量：赭石 -->
    <option name="DEFAULT_NUMBER">
      <value>
        <option name="FOREGROUND" value="B05628" />
      </value>
    </option>
    <!-- 注释：苍翠绿斜体 -->
    <option name="DEFAULT_LINE_COMMENT">
      <value>
        <option name="FOREGROUND" value="4A7A42" />
        <option name="FONT_TYPE" value="2" />
      </value>
    </option>
    <option name="DEFAULT_BLOCK_COMMENT">
      <value>
        <option name="FOREGROUND" value="4A7A42" />
        <option name="FONT_TYPE" value="2" />
      </value>
    </option>
    <option name="DEFAULT_DOC_COMMENT">
      <value>
        <option name="FOREGROUND" value="4A7A42" />
        <option name="FONT_TYPE" value="2" />
      </value>
    </option>
    <option name="DEFAULT_DOC_COMMENT_TAG">
      <value>
        <option name="FOREGROUND" value="4A7A42" />
        <option name="FONT_TYPE" value="3" />
      </value>
    </option>
    <!-- 标点与运算符：烟灰 -->
    <option name="DEFAULT_OPERATION_SIGN">
      <value>
        <option name="FOREGROUND" value="6B6F76" />
      </value>
    </option>
    <option name="DEFAULT_SEMICOLON">
      <value>
        <option name="FOREGROUND" value="6B6F76" />
      </value>
    </option>
    <option name="DEFAULT_COMMA">
      <value>
        <option name="FOREGROUND" value="6B6F76" />
      </value>
    </option>
    <!-- HTML / XML 标签与属性 -->
    <option name="HTML_TAG_NAME">
      <value>
        <option name="FOREGROUND" value="1D1F21" />
        <option name="FONT_TYPE" value="1" />
      </value>
    </option>
    <option name="HTML_ATTRIBUTE_NAME">
      <value>
        <option name="FOREGROUND" value="2E59A7" />
      </value>
    </option>
    <!-- Vue 专属指令与插值 -->
    <option name="VUE_DIRECTIVE">
      <value>
        <option name="FOREGROUND" value="9D2933" />
        <option name="FONT_TYPE" value="1" />
      </value>
    </option>
    <option name="VUE_INTERPOLATION_DELIMITERS">
      <value>
        <option name="FOREGROUND" value="315D8C" />
        <option name="FONT_TYPE" value="1" />
      </value>
    </option>
  </attributes>
</scheme>
```

#### (2) `shuimo-shen.xml` (水墨·深 编辑器配色方案)

```xml
<scheme name="水墨·深" version="142" parent_scheme="Darcula">
  <metaInfo>
    <property name="created">2026-08-26</property>
    <property name="ide">WebStorm</property>
    <property name="ideVersion">2024.1.0.0</property>
    <property name="originalScheme">水墨·深</property>
  </metaInfo>
  <colors>
    <option name="ADDED_LINES_COLOR" value="507F49" />
    <option name="CARET_COLOR" value="E05A6A" />
    <option name="CARET_ROW_COLOR" value="D8D3BC0D" />
    <option name="CONSOLE_BACKGROUND_KEY" value="1C1B1A" />
    <option name="DELETED_LINES_COLOR" value="E05A6A" />
    <option name="DOCUMENTATION_COLOR" value="222120" />
    <option name="FILESTATUS_ADDED" value="507F49" />
    <option name="FILESTATUS_MODIFIED" value="6B9BD2" />
    <option name="FILESTATUS_NOT_CHANGED_IMMEDIATE" value="6B9BD2" />
    <option name="GUTTER_BACKGROUND" value="1C1B1A" />
    <option name="INDENT_GUIDE" value="D8D3BC14" />
    <option name="LINE_NUMBERS_COLOR" value="8E8A7FB0" />
    <option name="LINE_NUMBER_ON_CARET_ROW_COLOR" value="E5E1D4" />
    <option name="MODIFIED_LINES_COLOR" value="6B9BD2" />
    <option name="RIGHT_MARGIN_COLOR" value="D8D3BC14" />
    <option name="SELECTED_INDENT_GUIDE" value="D8D3BC73" />
    <option name="SELECTED_TEARLINE_COLOR" value="E05A6A" />
    <option name="SELECTION_BACKGROUND" value="6B9BD226" />
    <option name="SELECTION_FOREGROUND" value="E5E1D4" />
    <option name="TEARLINE_COLOR" value="D8D3BC18" />
    <option name="WHITESPACES" value="8A857836" />
  </colors>
  <attributes>
    <!-- 基础关键字：珊瑚红粗体 -->
    <option name="DEFAULT_KEYWORD">
      <value>
        <option name="FOREGROUND" value="E05A6A" />
        <option name="FONT_TYPE" value="1" />
      </value>
    </option>
    <!-- 通用标识符与基础前景色：素宣浅灰 -->
    <option name="DEFAULT_IDENTIFIER">
      <value>
        <option name="FOREGROUND" value="D5D0C4" />
      </value>
    </option>
    <!-- 函数与方法：月魄白 -->
    <option name="DEFAULT_FUNCTION_DECLARATION">
      <value>
        <option name="FOREGROUND" value="E5E1D4" />
        <option name="FONT_TYPE" value="1" />
      </value>
    </option>
    <option name="DEFAULT_FUNCTION_CALL">
      <value>
        <option name="FOREGROUND" value="E5E1D4" />
      </value>
    </option>
    <!-- 类与接口：素白粗体 -->
    <option name="DEFAULT_CLASS_NAME">
      <value>
        <option name="FOREGROUND" value="E5E1D4" />
        <option name="FONT_TYPE" value="1" />
      </value>
    </option>
    <option name="DEFAULT_INTERFACE_NAME">
      <value>
        <option name="FOREGROUND" value="E5E1D4" />
        <option name="FONT_TYPE" value="1" />
      </value>
    </option>
    <!-- 变量与属性：月光灰 -->
    <option name="DEFAULT_LOCAL_VARIABLE">
      <value>
        <option name="FOREGROUND" value="C8C3B6" />
      </value>
    </option>
    <option name="DEFAULT_INSTANCE_FIELD">
      <value>
        <option name="FOREGROUND" value="C8C3B6" />
      </value>
    </option>
    <option name="DEFAULT_PARAMETER">
      <value>
        <option name="FOREGROUND" value="C8C3B6" />
        <option name="FONT_TYPE" value="2" />
      </value>
    </option>
    <!-- 常量与只读属性：霁蓝 -->
    <option name="DEFAULT_CONSTANT">
      <value>
        <option name="FOREGROUND" value="6B9BD2" />
      </value>
    </option>
    <option name="DEFAULT_STATIC_FIELD">
      <value>
        <option name="FOREGROUND" value="6B9BD2" />
      </value>
    </option>
    <!-- 字符串字面量：霁蓝 -->
    <option name="DEFAULT_STRING">
      <value>
        <option name="FOREGROUND" value="6B9BD2" />
      </value>
    </option>
    <!-- 数值字面量：琥珀金 -->
    <option name="DEFAULT_NUMBER">
      <value>
        <option name="FOREGROUND" value="C4A24D" />
      </value>
    </option>
    <!-- 注释：松针绿斜体 -->
    <option name="DEFAULT_LINE_COMMENT">
      <value>
        <option name="FOREGROUND" value="7CAE72" />
        <option name="FONT_TYPE" value="2" />
      </value>
    </option>
    <option name="DEFAULT_BLOCK_COMMENT">
      <value>
        <option name="FOREGROUND" value="7CAE72" />
        <option name="FONT_TYPE" value="2" />
      </value>
    </option>
    <option name="DEFAULT_DOC_COMMENT">
      <value>
        <option name="FOREGROUND" value="7CAE72" />
        <option name="FONT_TYPE" value="2" />
      </value>
    </option>
    <!-- 标点与运算符：暗灰 -->
    <option name="DEFAULT_OPERATION_SIGN">
      <value>
        <option name="FOREGROUND" value="8A8578" />
      </value>
    </option>
    <!-- Vue 专属指令与插值 -->
    <option name="VUE_DIRECTIVE">
      <value>
        <option name="FOREGROUND" value="E05A6A" />
        <option name="FONT_TYPE" value="1" />
      </value>
    </option>
    <option name="VUE_INTERPOLATION_DELIMITERS">
      <value>
        <option name="FOREGROUND" value="6B9BD2" />
        <option name="FONT_TYPE" value="1" />
      </value>
    </option>
  </attributes>
</scheme>
```

---

## 七、主题调试、验证与发布指南

### 1. 官方调试工具 (UI Inspector / PsiViewer / Scheme Preview)

在调试 JetBrains 主题与高亮时，建议开启以下内置利器：

1. **UI Inspector (UI 审查器)**：
   - 开启 Internal Mode（在 `Help -> Edit Custom Properties...` 中添加 `idea.is.internal=true` 并重启）。
   - 按快捷键 `Ctrl + Alt + Click` (Mac: `Cmd + Option + Click`) 点击 IDE 任意 UI 控件，可直接查看该控件对应的 **Theme Key 键名** 及当前计算颜色。
2. **PsiViewer 插件**：
   - 在 Marketplace 安装 `PsiViewer` 插件，可实时查看当前文件的完整 PSI 语法树节点类型与 `TextAttributesKey`。
3. **Settings 配色即时预览**：
   - 进入 `Settings / Preferences -> Editor -> Color Scheme`，右侧具备全语言交互式代码预览器。

---

### 2. 本地打包与安装验证

1. **纯 Theme 打包方式（ZIP 格式）**：
   - 将 `META-INF/` 与 `themes/` 目录直接打包为 `.zip` 归档。
2. **本地安装测试**：
   - 打开 WebStorm / IntelliJ IDEA。
   - 进入 `Settings -> Plugins -> ⚙️ 齿轮图标 -> Install Plugin from Disk...`。
   - 选中生成的 ZIP 文件即可即时安装并切换主题验证。

---

### 3. 发布到 JetBrains Marketplace 流程

1. **注册开发者账号**：访问 [JetBrains Marketplace Hub](https://plugins.jetbrains.com/)。
2. **生成 API Token**：在 Profile -> My Tokens 中创建发布 Token。
3. **上传并审核**：
   - 点击 **Upload Plugin** 上传构建好的 ZIP 插件包。
   - 填写插件中英文介绍与高清预览图。
   - 自动化验证（Plugin Verifier）通过后，通常在 1~2 个工作日内通过官方审核并上架。

---

## 总结

至此，水墨主题（Shuimo Theme）已构建起完备的三大主题架构体系：
1. [VS Code 语法高亮规范与源码实现深度解析](file:///Users/wangx/%E6%88%91%E7%9A%84/github/vscode/shuimo-theme/docs/vscode-syntax-highlight-rules.md)
2. [Vue (Volar / Vue - Official) 语法高亮规则与源码深度解析](file:///Users/wangx/%E6%88%91%E7%9A%84/github/vscode/shuimo-theme/docs/vue-volar-highlight-rules.md)
3. [WebStorm / IntelliJ IDEA 主题与语法着色系统全景架构深度解析](file:///Users/wangx/%E6%88%91%E7%9A%84/github/vscode/shuimo-theme/docs/webstorm-intellij-theme-rules.md)

通过统一的东方水墨美学基调（素宣底色、浓淡水墨、朱砂红、黛蓝、苍翠绿、赭石金）与各 IDE 底层机制的无缝映射，为开发者提供极致的跨编辑器沉浸式编码美学体验。

