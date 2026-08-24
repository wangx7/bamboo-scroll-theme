# Vue (Volar / Vue - Official) 语法高亮规则与源码深度解析

> **插件名称**: Vue - Official (`Vue.volar`)  
> **源码仓库**: [vuejs/language-tools](https://github.com/vuejs/language-tools)  
> **核心机制**: TextMate 词法语法 + Grammar Injections 动态注入 + LSP Semantic Tokens 语义高亮

---

## 目录
- [一、高亮系统整体架构](#一高亮系统整体架构)
- [二、语法配置文件清单与注入机制](#二语法配置文件清单与注入机制)
- [三、TextMate Scope 完整规则对照表](#三textmate-scope-完整规则对照表)
  - [1. SFC 顶层块与嵌入语言分流](#1-sfc-顶层块与嵌入语言分流)
  - [2. Vue 模板指令系统 (Directives)](#2-vue-模板指令系统-directives)
  - [3. 模板插值表达式 (Interpolations)](#3-模板插值表达式-interpolations)
  - [4. Style 块内 CSS 变量绑定 (`v-bind(...)`)](#4-style-块内-css-变量绑定-v-bind)
  - [5. Script 泛型定义 (`generic="..."`)](#5-script-泛型定义-generic)
  - [6. SFC 注释与指令标记 (Comments & Directives Metadata)](#6-sfc-注释与指令标记-comments--directives-metadata)
  - [7. 组件与标签 (Tags & Components)](#7-组件与标签-tags--components)
- [四、LSP Semantic Tokens 语义高亮规则](#四lsp-semantic-tokens-语义高亮规则)
- [五、典型 SFC 代码逐行 Scope 分解示例](#五典型-sfc-代码逐行-scope-分解示例)
- [六、VS Code 主题定制推荐配置 (Theme Authoring Guide)](#六vs-code-主题定制推荐配置-theme-authoring-guide)

---

## 一、高亮系统整体架构

Volar（现官方更名为 **Vue - Official**）的高亮体系由三层协同构成：

```
┌─────────────────────────────────────────────────────────────┐
│                   Vue SFC (.vue 文件)                       │
└──────────────────────────────┬──────────────────────────────┘
                               │
       ┌───────────────────────┴───────────────────────┐
       ▼                                               ▼
┌──────────────────────────────┐        ┌──────────────────────────────┐
│  第一层: TextMate 语法分析   │        │   第二层: LSP 语义高亮       │
│  (即时正则分词 / 静态语法着色) │        │  (AST类型推导 / 语义动态标记) │
├──────────────────────────────┤        ├──────────────────────────────┤
│ • vue.tmLanguage.json        │        │ • @vue/language-server       │
│ • Grammar Injections (注入)   │        │ • TypeScript Server Plugin   │
│ • Embedded Languages (嵌入)  │        │ • support.class.component    │
└──────────────────────────────┘        └──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 VS Code 渲染器 (Theme Tokens)                │
└─────────────────────────────────────────────────────────────┘
```

1. **TextMate 语法层 (`text.html.vue`)**：
   - 负责秒级启动和基础词法分词。
   - 解析 SFC 顶层标签（`<template>`, `<script>`, `<style>`, 自定义 block）。
   - 解析模板语法（指令、插值、动态绑定、修饰符、事件等）。
   - 将不同代码块的内容委托给对应的子语言（如 `source.ts`, `source.css.scss`, `text.pug`）。
2. **语法注入层 (Grammar Injections)**：
   - 利用 VS Code 的 `injectTo` 机制，将 Vue 指令、双大括号插值、CSS `v-bind()` 等语法无缝注入到 HTML、Markdown、MDX、Pug 以及 CSS 预处理器中。
3. **LSP 语义分析层 (Semantic Tokens)**：
   - 利用 Vue 编译器 AST 和 TypeScript 类型推导，精确区分 **原生 HTML 元素** 与 **Vue 组件**（即使是 kebab-case 如 `<my-card>` 也可被识别为组件）。
   - 提供响应式变量（Ref unwrapping）、模板作用域变量等深层语义标记。

---

## 二、语法配置文件清单与注入机制

在 Volar 扩展包的 `syntaxes/` 目录下，包含以下核心语法文件：

| 语法文件 | Scope Name | 作用与注入目标 (`injectTo`) |
| :--- | :--- | :--- |
| `vue.tmLanguage.json` | `text.html.vue` | **主语法文件**。负责 `.vue` 文件顶层结构识别、嵌入语言块分发及模板主规则。 |
| `vue-directives.json` | `vue.directives` | **指令语法注入**。注入到 `text.html.vue`, `text.html.markdown`, `text.html.derivative`, `text.pug`。 |
| `vue-interpolations.json` | `vue.interpolations` | **插值语法注入**。注入到 `text.pug`, `text.html.derivative`, `text.html.markdown`。 |
| `vue-sfc-style-variable-injection.json` | `vue.sfc.style.variable.injection` | **CSS `v-bind()` 注入**。注入到 `source.css`, `source.postcss`, `source.sass`, `source.stylus`。 |
| `vue-sfc-script-leading-operator-fix.json` | `vue.sfc.script.leading-operator-fix` | **语法修补**。修复 script 块首行关系运算符与泛型冲突问题。 |
| `markdown-vue.json` | `markdown.vue.codeblock` | **Markdown 代码块注入**。在 `.md` 文件中解析 ````vue 代码块。 |
| `mdx-vue.json` | `mdx.vue.codeblock` | **MDX 代码块注入**。在 `.mdx` 文件中解析 ````vue 代码块。 |

---

## 三、TextMate Scope 完整规则对照表

### 1. SFC 顶层块与嵌入语言分流

#### 顶层标签识别
SFC 顶层标签由 `vue.tmLanguage.json` 中的模式根据标签名和 `lang="..."` 属性动态分配子语法：

| 语法结构 | 对应 Scope | 嵌入语言 Scope |
| :--- | :--- | :--- |
| `<template>` | `entity.name.tag.template.html.vue` | 默认 `text.html.derivative` |
| `<template lang="pug">` | `entity.name.tag.template.html.vue` | `text.pug` |
| `<template lang="html">`| `entity.name.tag.template.html.vue` | `text.html.derivative` |
| `<script>` | `entity.name.tag.script.html.vue` | 默认 `source.js` |
| `<script lang="ts">` | `entity.name.tag.script.html.vue` | `source.ts` |
| `<script lang="tsx">`| `entity.name.tag.script.html.vue` | `source.tsx` |
| `<script lang="jsx">`| `entity.name.tag.script.html.vue` | `source.js.jsx` |
| `<style>` | `entity.name.tag.style.html.vue` | 默认 `source.css` |
| `<style lang="scss">`| `entity.name.tag.style.html.vue` | `source.css.scss` |
| `<style lang="less">`| `entity.name.tag.style.html.vue` | `source.css.less` |
| `<style lang="sass">`| `entity.name.tag.style.html.vue` | `source.sass` |
| `<style lang="stylus">`| `entity.name.tag.style.html.vue` | `source.stylus` |
| `<style lang="postcss">`| `entity.name.tag.style.html.vue` | `source.postcss` |
| `<custom-block lang="json">` | `entity.name.tag.<name>.html.vue` | `source.json` |
| `<custom-block lang="yaml">` | `entity.name.tag.<name>.html.vue` | `source.yaml` |
| `<custom-block lang="graphql">` | `entity.name.tag.<name>.html.vue` | `source.graphql` |

#### 顶层标签界定符
- `<` / `>`: `punctuation.definition.tag.begin.html.vue` / `punctuation.definition.tag.end.html.vue`
- `</`: `punctuation.definition.tag.begin.html.vue`

---

### 2. Vue 模板指令系统 (Directives)

Vue 的指令由 `vue-directives-control` 和 `vue-directives-original` 解析：

#### (1) 控制流指令 (Control Flow Directives)
| 指令语法 | 匹配正则 | Scope |
| :--- | :--- | :--- |
| `v-for` | `\b(v-for)\b` | `keyword.control.loop.vue` |
| `v-if` / `v-else-if` / `v-else` | `\b(v-if\|v-else-if\|v-else)\b` | `keyword.control.conditional.vue` |
| 作用域包裹 | 整个指令属性块 | `meta.attribute.directive.control.vue` |

#### (2) 常见指令与属性绑定 (General Directives & Bindings)
| 指令语法/符号 | 示例 | Scope | 说明 |
| :--- | :--- | :--- | :--- |
| `v-bind` / `v-model` / `v-show` 等 | `v-model="..."` | `entity.other.attribute-name.html.vue` | 标准指令名 |
| `:` (作为指令参数前缀) | `v-bind:title` | `punctuation.separator.key-value.html.vue` | 指令与参数分隔符 |
| `:` (缩写绑定) | `:title="title"` | `punctuation.attribute-shorthand.bind.html.vue` | `v-bind` 缩写 `:` |
| `@` (事件缩写) | `@click="handleClick"` | `punctuation.attribute-shorthand.event.html.vue` | `v-on` 缩写 `@` |
| `#` (插槽缩写) | `#header="slotProps"` | `punctuation.attribute-shorthand.slot.html.vue` | `v-slot` 缩写 `#` |
| `.` (指令修饰符前缀) | `.prevent`, `.stop` | `punctuation.separator.key-value.html.vue` | 修饰符点号 |
| 修饰符名称 | `.prevent` 中的 `prevent` | `entity.other.attribute-name.html.vue` | 修饰符名 |
| 动态参数方括号 `[` / `]` | `:[dynamicKey]` | `punctuation.separator.key-value.html.vue` | 动态属性方括号 |
| 动态参数内部表达式 | `[item.id + 1]` | `source.ts.embedded.html.vue` (引入 `source.ts#expression`) | 动态参数内 TS 表达式 |

#### (3) 指令表达式求值区域 (Directive Expressions)
- 等号 `=`: `punctuation.separator.key-value.html.vue`
- 引号 `"` / `'`: `punctuation.definition.string.begin.html.vue` / `punctuation.definition.string.end.html.vue`
- 引号内的 JS/TS 表达式: `source.ts.embedded.html.vue` (包含完整的 `source.ts#expression` 语法高亮，支持解构、箭头函数、三元表达式等)

---

### 3. 模板插值表达式 (Interpolations)

由 `vue-interpolations.json` 和 `vue.tmLanguage.json#vue-interpolations` 处理：

| 语法结构 | 示例 | Scope |
| :--- | :--- | :--- |
| 插值开始界定符 | `{{` | `punctuation.definition.interpolation.begin.html.vue` |
| 插值结束界定符 | `}}` | `punctuation.definition.interpolation.end.html.vue` |
| 插值外层容器 | `{{ user.name }}` | `expression.embedded.vue` |
| 插值内部表达式 | `user.name` | `source.ts.embedded.html.vue` (内部嵌套 `source.ts#expression`) |

---

### 4. Style 块内 CSS 变量绑定 (`v-bind(...)`)

由 `vue-sfc-style-variable-injection.json` 处理，注入到所有 CSS 相关语法中：

```css
.card {
  color: v-bind(textColor);
  background: v-bind('theme.bg');
}
```

| 语法结构 | Scope |
| :--- | :--- |
| 外层容器 | `vue.sfc.style.variable.injection.v-bind` |
| 函数名 `v-bind` | `entity.name.function` |
| 字符串包裹引号 (`'` 或 `"`) | `punctuation.definition.tag.begin.html` / `punctuation.definition.tag.end.html` |
| 绑定的 JS 表达式 | `source.ts.embedded.html.vue` -> `source.js` |

---

### 5. Script 泛型定义 (`generic="..."`)

在 Vue 3.3+ 中支持 `<script setup lang="ts" generic="T, U extends Item">`：

由 `vue-directives-generic-attr` 专门解析：
| 语法结构 | Scope |
| :--- | :--- |
| 属性名 `generic` | `entity.other.attribute-name.html.vue` |
| 整个参数块 | `meta.attribute.generic.vue` -> `meta.type.parameters.vue` |
| 泛型关键字 `extends`, `in`, `out` | `storage.modifier.ts` |
| 类型表达式 | `source.ts#type` |
| 分隔逗号 `,` | `source.ts#punctuation-comma` |
| 默认类型赋值 `=` | `keyword.operator.assignment.ts` |

---

### 6. SFC 注释与指令标记 (Comments & Directives Metadata)

| 语法结构 | 示例 | Scope |
| :--- | :--- | :--- |
| 普通 HTML 注释 | `<!-- comment -->` | `comment.block.vue`, `punctuation.definition.comment.vue` |
| Vue 编译器特殊指令注释 | `<!-- @vue-ignore -->` | `comment.block.vue` |
| 注释中的 `@` 符号 | `@` | `punctuation.definition.block.tag.comment.vue` |
| 注释中的标记名 | `vue-ignore`, `vue-expect-error` | `storage.type.class.comment.vue` |
| 注释中的 JSON 键值对 | `<!-- @vue-data {"a": 1} -->` | `source.json#value` |

---

### 7. 组件与标签 (Tags & Components)

TextMate 层面无法静态推导自定义标签是否为全局/局部注册组件，但通过以下规则做基础区分：

| 标签形式 | 匹配规则 | Scope |
| :--- | :--- | :--- |
| 大写驼峰标签 (组件) | `<MyComponent ...>` | `meta.tag.structure.$2.start.html.vue` + `entity.name.tag.html.vue` |
| 小写标签 (原生或短横线组件) | `<div ...>`, `<my-component>` | `entity.name.tag.$1.html.vue` (其中 `$1` 为标签名) |
| 自闭合标签 | `<img />`, `<MyComponent />` | `self-closing-tag` |

---

## 四、LSP Semantic Tokens 语义高亮规则

Volar 在 Language Server（语言服务）层面提供了强大的 **Semantic Highlighting（语义高亮）**，这是超越传统 TextMate 正则语法的核心优势。

### 1. 组件识别 (Semantic Component Highlighting)
在 `package.json` 中配置的语义 Token 映射：
```json
"semanticTokenScopes": [
  {
    "language": "vue",
    "scopes": {
      "component": [
        "support.class.component.vue",
        "entity.name.type.class.vue"
      ]
    }
  }
]
```
- **作用**: 当你在模板中书写 `<custom-card>` 或 `<ElButton>` 时，Vue LSP 通过组件解析系统确认其为组件（而非未知 HTML 标签），并赋予语义 token `component`。
- **映射到的 TextMate 兼容 Scope**: `support.class.component.vue`, `entity.name.type.class.vue`。
- **编辑器高亮组**: 在 VS Code 中对应 `semanticTokenColors` 中的 `"component"` 或 `"*.component"`。

### 2. 模板与脚本上下文语义 Tokens (TypeScript Integration)
Volar 将 `<template>` 编译为虚拟 TypeScript AST，继承全部 TypeScript 语义着色：

| 语义 Token 类型 | 示例场景 | 语义 Scope / Token Type |
| :--- | :--- | :--- |
| `variable` | `ref()` / `reactive()` 变量 | `variable.other.readwrite` |
| `property` | 对象的属性访问 `user.name` | `variable.other.property` |
| `parameter` | `v-slot="{ row }"` 或事件参数 `($event)` | `variable.parameter` |
| `function` / `method` | 模板中调用的方法 `@click="handleSubmit"` | `entity.name.function` |
| `type` / `interface` | `<script lang="ts">` 中的类型 | `entity.name.type` |
| `enumMember` | 模板中引用的枚举常量 | `variable.other.enummember` |

---

## 五、典型 SFC 代码逐行 Scope 分解示例

```vue
1:  <script setup lang="ts" generic="T extends BaseItem">
2:  import { ref } from 'vue'
3:  const count = ref<number>(0)
4:  const themeColor = ref('#1890ff')
5:  </script>
6:  
7:  <template>
8:    <div class="container" v-if="count > 0">
9:      <CustomButton
10:       :item-id="item.id"
11:       @click.prevent="count++"
12:       #header="{ title }"
13:     >
14:       {{ title }} ({{ count }})
15:     </CustomButton>
16:   </div>
17: </template>
18: 
19: <style scoped lang="scss">
20: .container {
21:   color: v-bind(themeColor);
22: }
23: </style>
```

### 关键行语法 Scope 解析：

- **第 1 行 (`<script setup lang="ts" generic="T extends BaseItem">`)**:
  - `<` / `>`: `punctuation.definition.tag.begin.html.vue` / `punctuation.definition.tag.end.html.vue`
  - `script`: `entity.name.tag.script.html.vue`
  - `setup`: `entity.other.attribute-name.html.vue`
  - `generic`: `meta.attribute.generic.vue` -> `entity.other.attribute-name.html.vue`
  - `extends`: `storage.modifier.ts`
  - `BaseItem`: `entity.name.type.ts`
- **第 8 行 (`<div class="container" v-if="count > 0">`)**:
  - `div`: `entity.name.tag.div.html.vue`
  - `v-if`: `keyword.control.conditional.vue` (属于 `meta.attribute.directive.control.vue`)
  - `count > 0`: `source.ts.embedded.html.vue`
- **第 9 行 (`<CustomButton ...>`)**:
  - `CustomButton`: 
    - TextMate: `meta.tag.structure.CustomButton.start.html.vue` + `entity.name.tag.html.vue`
    - LSP Semantic: `support.class.component.vue` / `component`
- **第 10 行 (`:item-id="item.id"`)**:
  - `:`: `punctuation.attribute-shorthand.bind.html.vue`
  - `item-id`: `entity.other.attribute-name.html.vue`
  - `item.id`: `source.ts.embedded.html.vue` (属性访问 `id` 获得 `variable.other.property`)
- **第 11 行 (`@click.prevent="count++"`)**:
  - `@`: `punctuation.attribute-shorthand.event.html.vue`
  - `click`: `entity.other.attribute-name.html.vue`
  - `.`: `punctuation.separator.key-value.html.vue`
  - `prevent`: `entity.other.attribute-name.html.vue`
  - `count++`: `source.ts.embedded.html.vue`
- **第 12 行 (`#header="{ title }"`)**:
  - `#`: `punctuation.attribute-shorthand.slot.html.vue`
  - `header`: `entity.other.attribute-name.html.vue`
  - `{ title }`: `source.ts.embedded.html.vue`
- **第 14 行 (`{{ title }} ({{ count }})`)**:
  - `{{`: `punctuation.definition.interpolation.begin.html.vue`
  - `}}`: `punctuation.definition.interpolation.end.html.vue`
  - `title` / `count`: `expression.embedded.vue` -> `source.ts.embedded.html.vue`
- **第 21 行 (`color: v-bind(themeColor);`)**:
  - `v-bind`: `entity.name.function`
  - `themeColor`: `source.ts.embedded.html.vue` -> `source.js`

---

## 六、VS Code 主题定制推荐配置 (Theme Authoring Guide)

如果你正在开发或优化 VS Code 颜色主题（如 `shuimo-theme`），请参考以下标准配置建议以实现完美的 Vue 语法视觉体验：

### 1. `tokenColors` (TextMate Scopes)
```jsonc
{
  "tokenColors": [
    // 1. Vue 顶层 SFC 块标签 (template, script, style)
    {
      "name": "Vue SFC Block Tags",
      "scope": [
        "entity.name.tag.template.html.vue",
        "entity.name.tag.script.html.vue",
        "entity.name.tag.style.html.vue"
      ],
      "settings": {
        "foreground": "#D32F2F",
        "fontStyle": "bold"
      }
    },
    // 2. Vue 控制流指令 (v-if, v-else, v-for)
    {
      "name": "Vue Control Directives",
      "scope": [
        "keyword.control.conditional.vue",
        "keyword.control.loop.vue"
      ],
      "settings": {
        "foreground": "#E64A19",
        "fontStyle": "bold"
      }
    },
    // 3. Vue 指令前缀缩写 (: @ #)
    {
      "name": "Vue Directive Shorthands",
      "scope": [
        "punctuation.attribute-shorthand.bind.html.vue",
        "punctuation.attribute-shorthand.event.html.vue",
        "punctuation.attribute-shorthand.slot.html.vue"
      ],
      "settings": {
        "foreground": "#0097A7",
        "fontStyle": "bold"
      }
    },
    // 4. Vue 双大括号插值符号 {{ }}
    {
      "name": "Vue Interpolation Punctuation",
      "scope": [
        "punctuation.definition.interpolation.begin.html.vue",
        "punctuation.definition.interpolation.end.html.vue"
      ],
      "settings": {
        "foreground": "#7B1FA2",
        "fontStyle": "bold"
      }
    },
    // 5. Vue 组件类名 (TextMate 回退)
    {
      "name": "Vue Custom Component Tags",
      "scope": [
        "meta.tag.structure.start.html.vue",
        "support.class.component.vue"
      ],
      "settings": {
        "foreground": "#2E7D32",
        "fontStyle": "bold"
      }
    },
    // 6. Style 中的 v-bind() 变量绑定
    {
      "name": "Vue CSS v-bind Function",
      "scope": [
        "vue.sfc.style.variable.injection.v-bind entity.name.function"
      ],
      "settings": {
        "foreground": "#1976D2",
        "fontStyle": "bold"
      }
    },
    // 7. Vue 特殊注释指令 (如 @vue-ignore)
    {
      "name": "Vue Comment Tag Directives",
      "scope": [
        "punctuation.definition.block.tag.comment.vue",
        "storage.type.class.comment.vue"
      ],
      "settings": {
        "foreground": "#F57C00",
        "fontStyle": "italic bold"
      }
    }
  ]
}
```

### 2. `semanticTokenColors` (LSP 语义 Tokens)
```jsonc
{
  "semanticTokenColors": {
    // 识别并高亮 Vue 自定义组件（无论 PascalCase 或 kebab-case）
    "component": {
      "foreground": "#2E7D32",
      "fontStyle": "bold"
    },
    "*.component": {
      "foreground": "#2E7D32",
      "fontStyle": "bold"
    }
  }
}
```

---

## 总结
Volar / Vue - Official 的语法高亮设计体现了现代 IDE 扩展的演进趋势：
1. **词法层面**：通过 TextMate 语法树 + 7 组定向 Injection，精准切分指令、修饰符、动态参数、嵌入 TS/CSS；
2. **语义层面**：通过 LSP Language Server 注入虚拟 TS 文件与组件元数据，实现了即使在复杂模板中也能完美识别组件、属性与响应式变量。
