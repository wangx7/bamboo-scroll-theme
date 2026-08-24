# VS Code 最新语法高亮规范与源码实现深度解析

> **官方参考源**: [VS Code Official Docs](https://code.visualstudio.com/api/language-extensions/syntax-highlight-guide), [VS Code Core Repository (`microsoft/vscode`)](https://github.com/microsoft/vscode)  
> **核心源码模块**: `src/vs/platform/theme/common/tokenClassificationRegistry.ts`, `src/vs/workbench/services/themes/common/tokenTheme.ts`, `vscode-textmate`  
> **核心机制**: TextMate 词法分词引擎 + 语法动态注入 (Injections) + LSP 语义高亮 (Semantic Tokens) + 特异性评分级联引擎

---

## 目录
- [一、VS Code 语法高亮全景架构](#一vs-code-语法高亮全景架构)
- [二、TextMate 词法语法系统规范](#二textmate-词法语法系统规范)
  - [1. 语法声明与贡献点配置 (`package.json`)](#1-语法声明与贡献点配置-packagejson)
  - [2. 标准 11 大 TextMate 顶层 Scope 全景速查表](#2-标准-11-大-textmate-顶层-scope-全景速查表)
  - [3. 语法注入机制 (`injectTo` 与 `injectionSelector`)](#3-语法注入机制-injectto-与-injectionselector)
  - [4. 嵌入语言处理与 Token 类型重置 (`embeddedLanguages` & `tokenTypes`)](#4-嵌入语言处理与-token-类型重置-embeddedlanguages--tokentypes)
  - [5. 括号匹配作用域控制 (`bracketScopes`)](#5-括号匹配作用域控制-bracketscopes)
- [三、LSP 语义高亮系统规范 (Semantic Highlighting)](#三lsp-语义高亮系统规范-semantic-highlighting)
  - [1. 架构与运行生命周期](#1-架构与运行生命周期)
  - [2. 官方标准 24 类 Semantic Token Types](#2-官方标准-24-类-semantic-token-types)
  - [3. 官方标准 10 类 Semantic Token Modifiers](#3-官方标准-10-类-semantic-token-modifiers)
  - [4. 语义 Token 到 TextMate Scope 的官方内置映射表 (Fallback Map)](#4-语义-token-到-textmate-scope-的官方内置映射表-fallback-map)
  - [5. 自定义 Token 类型与修饰符贡献 (`contributes.semanticTokenTypes`)](#5-自定义-token-类型与修饰符贡献-contributessemantictokentypes)
- [四、主题着色匹配与优先级算法深度剖析 (Scoring Engine)](#四主题着色匹配与优先级算法深度剖析-scoring-engine)
  - [1. 语义选择器语法与特异性等级矩阵](#1-语义选择器语法与特异性等级矩阵)
  - [2. TextMate Scope 权重计算与匹配规则](#2-textmate-scope-权重计算与匹配规则)
  - [3. 双层渲染回退级联流程图](#3-双层渲染回退级联流程图)
- [五、主题开发者实战配置模版 (Theme Authoring Best Practices)](#五主题开发者实战配置模版-theme-authoring-best-practices)
  - [1. 现代完整主题配置结构范式](#1-现代完整主题配置结构范式)
  - [2. 官方调试利器：Scope Inspector 使用指南](#2-官方调试利器scope-inspector-使用指南)

---

## 一、VS Code 语法高亮全景架构

在 VS Code 架构中，语法高亮经历了从单一 TextMate 正则分词到 **「TextMate 词法层 + LSP 语义层」双轨融合引擎** 的演进：

```
                           ┌───────────────────────────────┐
                           │      源码文本 (Source Code)    │
                           └───────────────┬───────────────┘
                                           │
                   ┌───────────────────────┴───────────────────────┐
                   ▼                                               ▼
     ┌───────────────────────────┐                   ┌───────────────────────────┐
     │ 第一层：TextMate 词法引擎 │                   │ 第二层：LSP 语义分析服务  │
     │     (vscode-textmate)     │                   │  (SemanticTokensProvider) │
     ├───────────────────────────┤                   ├───────────────────────────┤
     │ • 基于 Oniguruma 正则引擎 │                   │ • 基于 AST 语法树/类型推导│
     │ • 毫秒级即时分词（无延迟） │                   │ • 异步流式返回 (微延迟)   │
     │ • 单文件词法作用域识别    │                   │ • 跨文件符号/常量/类型解构│
     │ • 输出: TextMate Scopes   │                   │ • 输出: Semantic Legend   │
     └─────────────┬─────────────┘                   └─────────────┬─────────────┘
                   │                                               │
                   │  Scope 路径 (如 entity.name.function)         │  类型+修饰符 (如 variable.readonly)
                   ▼                                               ▼
     ┌───────────────────────────────────────────────────────────────────────────┐
     │                     VS Code TokenTheme 样式合成器                         │
     │           (src/vs/workbench/services/themes/common/tokenTheme.ts)         │
     ├───────────────────────────────────────────────────────────────────────────┤
     │ 1. 优先检索 `semanticTokenColors` 规则匹配                                 │
     │ 2. 若未匹配或未启用，依 `semanticTokenScopes` 回退到 TextMate Scope       │
     │ 3. 计算 `tokenColors` 中的最长前缀特异性得分（Specificity Score）         │
     │ 4. 合并样式属性：foreground, bold, italic, underline, strikethrough       │
     └─────────────────────────────────────┬─────────────────────────────────────┘
                                           │
                                           ▼
                           ┌───────────────────────────────┐
                           │   Monaco Editor 最终像素渲染  │
                           └───────────────────────────────┘
```

---

## 二、TextMate 词法语法系统规范

### 1. 语法声明与贡献点配置 (`package.json`)

在扩展的 `package.json` 中，通过 `contributes.grammars` 注册语法：

```jsonc
{
  "contributes": {
    "languages": [
      {
        "id": "myLang",
        "extensions": [".mylang"],
        "aliases": ["My Language", "mylang"]
      }
    ],
    "grammars": [
      {
        "language": "myLang",
        "scopeName": "source.mylang",
        "path": "./syntaxes/mylang.tmLanguage.json",
        // 声明嵌入语言，使嵌入代码块具备独立的括号匹配、注释语法等
        "embeddedLanguages": {
          "meta.embedded.block.javascript": "javascript",
          "meta.embedded.inline.css": "css"
        },
        // 排除非配对括号的作用域
        "unbalancedBracketScopes": [
          "keyword.operator.relational",
          "storage.type.function.arrow"
        ],
        // 覆写特定作用域的内容模式 (other | comment | string)
        "tokenTypes": {
          "meta.embedded.inline.sql": "other"
        }
      }
    ]
  }
}
```

---

### 2. 标准 11 大 TextMate 顶层 Scope 全景速查表

VS Code 完全遵循并扩展了 TextMate 标准命名约定。主题开发者应优先针对标准 Scope 编写规则，以确保通用跨语言兼容性：

| 顶层 Scope 分类 | 次级/标准命名结构 (Sub-scopes) | 含义与典型代表 |
| :--- | :--- | :--- |
| **`comment`** | `comment.line.double-slash`<br>`comment.line.number-sign`<br>`comment.block.documentation` | 单行注释、`#` 注释、多行文档块注释（JSDoc / TypeDoc 等） |
| **`constant`** | `constant.numeric.integer`<br>`constant.numeric.float`<br>`constant.numeric.hex`<br>`constant.language.boolean.true`<br>`constant.language.null`<br>`constant.character.escape`<br>`constant.other` | 数值常量（整数/浮点/十六进制）、语言内置常量（`true`, `false`, `null`, `undefined`, `nil`）、字符转义序列 `\n`, `\u0020` |
| **`entity`** | `entity.name.function`<br>`entity.name.function.member`<br>`entity.name.function.constructor`<br>`entity.name.type.class`<br>`entity.name.type.interface`<br>`entity.name.type.enum`<br>`entity.name.tag`<br>`entity.other.attribute-name` | 被定义或调用的实体：函数名、类方法、构造函数、类/接口/枚举类型名、HTML/XML 标签名、属性名 |
| **`invalid`** | `invalid.illegal`<br>`invalid.deprecated` | 语法非法错误、已废弃过时的语法构造 |
| **`keyword`** | `keyword.control.conditional`<br>`keyword.control.loop`<br>`keyword.control.flow`<br>`keyword.control.import`<br>`keyword.operator.assignment`<br>`keyword.operator.arithmetic`<br>`keyword.operator.comparison`<br>`keyword.operator.logical`<br>`keyword.operator.bitwise` | 控制流关键字（`if`, `else`, `while`, `for`, `return`, `import`）、各类运算符（赋值 `=`, 算术 `+`, 比较 `===`, 逻辑 `&&`, 位运算 `>>`） |
| **`markup`** | `markup.heading.1` ~ `markup.heading.6`<br>`markup.bold`<br>`markup.italic`<br>`markup.underline.link`<br>`markup.raw.inline`<br>`markup.raw.block`<br>`markup.quote`<br>`markup.list.numbered`<br>`markup.inserted`<br>`markup.deleted` | 标记文档内容（Markdown/HTML/Git Diff）：各级标题、粗体、斜体、链接、行内/块级代码、引用块、列表项、Diff 新增/删除 |
| **`meta`** | `meta.function`<br>`meta.class`<br>`meta.tag`<br>`meta.embedded.block`<br>`meta.type.parameters` | 结构化容器作用域（通常不直接赋予前景色，用于给内部子 token 提供嵌套层级与上下文限定） |
| **`punctuation`**| `punctuation.definition.tag.begin`<br>`punctuation.definition.tag.end`<br>`punctuation.definition.comment`<br>`punctuation.definition.string.begin`<br>`punctuation.separator.comma`<br>`punctuation.separator.key-value`<br>`punctuation.terminator.statement` | 标点界定符：标签括号 `<` `>`, 注释符 `//`, 引号 `"`, 逗号 `,`, 键值冒号 `:`, 语句分号 `;` |
| **`storage`** | `storage.type.function`<br>`storage.type.class`<br>`storage.type.interface`<br>`storage.modifier.async`<br>`storage.modifier.static`<br>`storage.modifier.readonly`<br>`storage.modifier.access` | 声明存储关键字（`function`, `class`, `const`, `let`, `var`）与修饰符（`async`, `static`, `readonly`, `public`, `private`） |
| **`string`** | `string.quoted.single`<br>`string.quoted.double`<br>`string.quoted.triple`<br>`string.template`<br>`string.regexp` | 字符串字面量：单引号、双引号、多行三引号、模板字符串反引号、正则表达式字面量 |
| **`support`** | `support.function.builtin`<br>`support.function.console`<br>`support.class.builtin`<br>`support.type.primitive`<br>`support.variable.property` | 框架/环境提供的内置支持：全局函数（`Math.sin`, `console.log`）、全局类（`Array`, `Promise`）、原生基本类型（`string`, `number`） |
| **`variable`** | `variable.other.readwrite`<br>`variable.other.constant`<br>`variable.other.property`<br>`variable.parameter`<br>`variable.language.this`<br>`variable.language.super` | 变量标识符：可读写变量、只读常量、对象属性访问、形参参数、特殊语言变量（`this`, `super`, `arguments`, `self`） |

---

### 3. 语法注入机制 (`injectTo` 与 `injectionSelector`)

注入语法允许一个扩展将其正则模式**无侵入地插入到已有语言的语法树中**：

```jsonc
// syntaxes/todo-injection.json
{
  "scopeName": "todo.comment.injection",
  // L: 表示 Left 优先注入，在目标 Scope 原有规则之前优先匹配
  "injectionSelector": "L:comment.line -comment.line.number-sign",
  "patterns": [
    {
      "match": "\\b(TODO|FIXME|NOTE|HACK)\\b",
      "name": "keyword.codetag.notation.todo"
    }
  ]
}
```

- **`injectTo`**: 指定目标宿主语言 Scope（如 `["source.js", "source.ts", "text.html.vue"]`）。
- **`L:` 标识**: 提升匹配优先级到宿主规则前，常用于 TODO 标签、嵌入微语法。
- **`-` 排除选择器**: 如 `L:comment -comment.block` 表示仅注入单行注释，避开块注释。

---

### 4. 嵌入语言处理与 Token 类型重置 (`embeddedLanguages` & `tokenTypes`)

VS Code 核心默认将包含在 `string` 或 `comment` Scope 下的内容禁用代码补全与括号配对。若在字符串中嵌入了其他语言（如 JS 模板字符串中的 SQL / GraphQL），必须进行上下文隔离：

1. **方式一 (推荐)**：在 TextMate 规则中使用 `meta.embedded.*` 包装子语法，VS Code 渲染器检测到 `meta.embedded` 会自动切换上下文模式。
2. **方式二**：在 `package.json` 的 `grammars` 声明中指定 `tokenTypes`:
   ```jsonc
   "tokenTypes": {
     "meta.embedded.inline.sql": "other"
   }
   ```
   可将该 Scope 的默认 `string` 行为覆写为普通源码模式（`other`）。

---

### 5. 括号匹配作用域控制 (`bracketScopes`)

在 VS Code 1.60+ 引入的纯性能级彩虹括号匹配算法中，可显式配置参与/排除的作用域：
- **`balancedBracketScopes`**: 声明哪些 Scope 允许括号匹配（默认全部启用）。
- **`unbalancedBracketScopes`**: 声明排除 Scope（如 Shell 中的 `case ... in 1)` 的单括号、箭头函数 `=>`、比较运算符 `<` `>` 等）。

---

## 三、LSP 语义高亮系统规范 (Semantic Highlighting)

### 1. 架构与运行生命周期

语义高亮通过 LSP（Language Server Protocol 3.16+）规范中的 `textDocument/semanticTokens` 请求交互：

```
[VS Code Client]                              [Language Server]
      │                                              │
      │── 1. textDocument/didOpen or didChange ─────>│ (更新虚拟 AST)
      │                                              │
      │── 2. textDocument/semanticTokens/full ──────>│
      │                                              │
      │<─ 3. SemanticTokens (Delta 压缩整数数组) ─────│ (包含 [line, char, len, typeIdx, modBits])
      │                                              │
      ▼                                              ▼
[本地解码为 TokenClassification]              [维持版本状态]
```

---

### 2. 官方标准 24 类 Semantic Token Types

定义在 VS Code 源码 `tokenClassificationRegistry.ts` 中的标准语义类型：

| 语义 Token Type | 说明 | 示例场景 |
| :--- | :--- | :--- |
| `namespace` | 命名空间、模块声明 | `namespace MySpace`, `module.exports` |
| `type` | 通用类型名称 | `type StringOrNum = string \| number;` |
| `class` | 类定义及其实例化引用 | `class UserService`, `new App()` |
| `enum` | 枚举类型 | `enum Direction { Up, Down }` |
| `interface` | 接口定义 | `interface UserPayload {}` |
| `struct` | 结构体 (C/C++/Rust/Go 等) | `struct Vector3 { x: f32 }` |
| `typeParameter` | 泛型参数名称 | `<T, K extends keyof T>` 中的 `T` 和 `K` |
| `parameter` | 函数或方法的参数 | `function sum(a, b)` 中的 `a`, `b` |
| `variable` | 通用局部/顶层变量 | `const userName = 'Alice'` |
| `property` | 对象属性、类字段 | `user.address`, `this.state` |
| `enumMember` | 枚举内部成员 | `Direction.Up` 中的 `Up` |
| `event` | 事件声明或事件对象 | `public event OnDataReceived;` |
| `function` | 独立函数声明与调用 | `function calculateTotal()` |
| `method` | 类/接口中的成员方法 | `userService.getUserById()` |
| `macro` | 预处理器宏命令 (C/Rust) | `#define BUFFER_SIZE 1024`, `println!` |
| `keyword` | 语法关键字 (语义阶段标记) | `yield`, `await`, `async` |
| `modifier` | 访问修饰符 (语义阶段标记) | `public`, `private`, `mut` |
| `comment` | 文档注释中的特殊符号 | JSDoc 注释中的 `@param` 标记 |
| `string` | 语义识别出的特定字符串 | SQL 语句字面量 |
| `number` | 语义推导出的特殊数字 | 单位数值字面量 |
| `regexp` | 语义分析确认的正规表达式 | `/^[a-z]+$/gi` |
| `operator` | 重载运算符或特殊操作符 | C++ `operator+`, Rust `impl Add` |
| `decorator` | 装饰器 / 注解 | `@Component()`, `@Injectable()` |
| `label` | 循环或语句标号 | `loopLabel: for (...)`, `goto end;` |

---

### 3. 官方标准 10 类 Semantic Token Modifiers

修饰符以位掩码（Bitmask）形式附加在 Token Type 上，支持多重组合（如 `variable.readonly.defaultLibrary`）：

| 语义 Token Modifier | 含义 | 典型触发场景 |
| :--- | :--- | :--- |
| `declaration` | 符号正在被声明/定义处（区别于后续使用处） | `const x = 1` 中的 `x` |
| `definition` | 符号实现的具体位置 | 接口实现的具体函数主体 |
| `readonly` | 不可变符号、常量、只读属性 | `const`, `readonly id: string` |
| `static` | 静态类成员、静态方法 | `Math.PI`, `ClassName.staticMethod()` |
| `deprecated` | 已废弃/过时的符号 (常配合中划线样式) | 被 `@deprecated` 注解标记的 API |
| `abstract` | 抽象类、抽象方法 | `abstract class BaseController` |
| `async` | 异步函数或返回 Promise 的方法 | `async function fetchData()` |
| `modification` | 变量在此处发生了修改/重赋值 | `count += 1`, `x++` 中的 `count`, `x` |
| `documentation` | 位于文档注释上下文内部的符号 | `@param name` 中的 `name` |
| `defaultLibrary` | 运行环境标准库/全局内置符号 | `window`, `document`, `console`, `setTimeout` |

---

### 4. 语义 Token 到 TextMate Scope 的官方内置映射表 (Fallback Map)

当主题**未直接配置**某个语义 Token 时，VS Code 会通过内置回退表检索对应的 TextMate Scope 样式：

```typescript
// 摘自 VS Code 源码: src/vs/platform/theme/common/tokenClassificationRegistry.ts
const standardTokenToScopeMap: Record<string, string[]> = {
  'namespace': ['entity.name.namespace'],
  'type': ['entity.name.type'],
  'type.defaultLibrary': ['support.type'],
  'struct': ['storage.type.struct'],
  'class': ['entity.name.type.class'],
  'class.defaultLibrary': ['support.class'],
  'interface': ['entity.name.type.interface'],
  'enum': ['entity.name.type.enum'],
  'typeParameter': ['entity.name.type.parameter', 'entity.name.type'],
  'function': ['entity.name.function'],
  'function.defaultLibrary': ['support.function'],
  'method': ['entity.name.function.member'],
  'macro': ['entity.name.function.preprocessor'],
  'variable': ['variable.other.readwrite', 'entity.name.variable'],
  'variable.readonly': ['variable.other.constant'],
  'variable.readonly.defaultLibrary': ['support.constant'],
  'parameter': ['variable.parameter'],
  'property': ['variable.other.property'],
  'property.readonly': ['variable.other.constant.property'],
  'enumMember': ['variable.other.enummember'],
  'event': ['variable.other.event'],
  'decorator': ['entity.name.decorator']
};
```

---

### 5. 自定义 Token 类型与修饰符贡献 (`contributes.semanticTokenTypes`)

扩展可自定义特定语言领域的专有 Token，并声明其继承的父类型及 TextMate 回退：

```jsonc
{
  "contributes": {
    "semanticTokenTypes": [
      {
        "id": "component",
        "superType": "class",
        "description": "Vue/React UI component tag or symbol"
      }
    ],
    "semanticTokenModifiers": [
      {
        "id": "reactive",
        "description": "Vue 3 Ref / Reactive Proxy state variable"
      }
    ],
    // 声明回退的 TextMate Scopes
    "semanticTokenScopes": [
      {
        "language": "vue",
        "scopes": {
          "component": ["support.class.component.vue", "entity.name.type.class.vue"]
        }
      }
    ]
  }
}
```

---

## 四、主题着色匹配与优先级算法深度剖析 (Scoring Engine)

### 1. 语义选择器语法与特异性等级矩阵

在主题的 `semanticTokenColors` 中，选择器遵循标准语法：
$$\text{Selector} = (* \mid \text{tokenType})(\text{.tokenModifier})*(\text{:tokenLanguage})?$$

当同一个 Token 被多个选择器命中时，VS Code 会根据 **源码特异性打分系统 (`tokenTheme.ts`)** 进行判决，优先级从高到低排列如下：

| 优先级 (Rank) | 匹配模式范例 | 说明与示例 |
| :---: | :--- | :--- |
| **1 (最高)** | `tokenType.mod1.mod2:language` | 指定了**语言 + 全部指定修饰符 + 精确类型**（如 `variable.readonly.defaultLibrary:typescript`） |
| **2** | `tokenType.mod1:language` | 指定了**语言 + 单个修饰符 + 精确类型**（如 `variable.readonly:typescript`） |
| **3** | `tokenType:language` | 指定了**语言 + 精确类型**（如 `class:csharp`） |
| **4** | `*.mod1.mod2:language` | 指定了**语言 + 通配符类型 + 多个修饰符**（如 `*.readonly.static:typescript`） |
| **5** | `*.mod1:language` | 指定了**语言 + 通配符类型 + 单个修饰符**（如 `*.deprecated:java`） |
| **6** | `tokenType.mod1.mod2` | **跨语言 + 全部指定修饰符 + 精确类型**（如 `variable.readonly.defaultLibrary`） |
| **7** | `tokenType.mod1` | **跨语言 + 单修饰符 + 精确类型**（如 `variable.readonly`） |
| **8** | `*.mod1.mod2` | **跨语言 + 通配符类型 + 多个修饰符**（如 `*.readonly.declaration`） |
| **9** | `*.mod1` | **跨语言 + 通配符类型 + 单修饰符**（如 `*.declaration`） |
| **10** | `tokenType` | **跨语言 + 基础类型**（如 `variable`, `property`） |
| **11 (最低)**| `superType` | **父级继承类型**（如 `component` 未命中时检索其 `superType: class`） |

---

### 2. TextMate Scope 权重计算与匹配规则

对于传统的 `tokenColors`，VS Code 使用标准的 TextMate 前缀特异性评分：
1. **最长前缀胜出 (Longest Prefix Match)**：`entity.name.function.member` 胜过 `entity.name.function` 胜过 `entity.name`。
2. **父级选择器权重 (Ancestor Specificity)**：`source.ts meta.class entity.name.type`（两层祖先限定）胜过 `source.ts entity.name.type` 胜过单纯的 `entity.name.type`。
3. **同分规则 (Tie-breaking)**：在选择器特异性完全相同的情况下，**文件后方出现的规则覆盖前方规则**。

---

### 3. 双层渲染回退级联流程图

```
                       一个具体的代码 Token 准备渲染
                                     │
                                     ▼
                ┌──────────────────────────────────────────┐
                │ 是否存在 LSP 语义 Token 且当前主题启用了  │
                │     "semanticHighlighting": true ?       │
                └────────────────────┬─────────────────────┘
                                     │
                  ┌──────────────────┴──────────────────┐
               YES│                                     │NO
                  ▼                                     │
    ┌───────────────────────────┐                       │
    │ 检索 `semanticTokenColors`│                       │
    │  是否存在精确/通配规则匹配? │                       │
    └─────────────┬─────────────┘                       │
                  │                                     │
           ┌──────┴──────┐                              │
        YES│             │NO                            │
           ▼             ▼                              │
    ┌────────────┐ ┌───────────────────────────┐        │
    │ 采用语义样式│ │ 通过 Fallback Map 转换为   │        │
    │ (Foreground│ │ 对应的 TextMate Scope 列表 │        │
    │  / Style)  │ └─────────────┬─────────────┘        │
    └────────────┘               │                      │
                                 └──────────┬───────────┘
                                            │
                                            ▼
                             ┌────────────────────────────┐
                             │ 检索主题 `tokenColors` 列表│
                             │  按特异性最高分规则合并样式 │
                             └──────────────┬─────────────┘
                                            │
                                            ▼
                             ┌────────────────────────────┐
                             │ 输出最终 RGB 颜色与字体字重 │
                             └────────────────────────────┘
```

---

## 五、主题开发者实战配置模版 (Theme Authoring Best Practices)

### 1. 现代完整主题配置结构范式

为确保主题在所有现代语言（TS、Vue、React、Rust、Go、Python）中均表现完美，建议在主题 JSON 中完整实现以下层次：

```jsonc
{
  "$schema": "vscode://schemas/color-theme",
  "name": "My Pro Theme",
  "type": "dark",
  // 必须显式开启语义高亮
  "semanticHighlighting": true,

  // 1. LSP 语义规则定义 (精准、高优先)
  "semanticTokenColors": {
    // 全局修饰符通用规则
    "*.declaration": { "fontStyle": "bold" },
    "*.deprecated": { "fontStyle": "strikethrough" },
    "*.defaultLibrary": { "fontStyle": "italic" },

    // 核心类型与组件
    "class": "#4EC9B0",
    "class.defaultLibrary": "#4EC9B0",
    "interface": "#9CDCFE",
    "enum": "#4EC9B0",
    "enumMember": "#4FC1FF",
    "typeParameter": "#20B2AA",
    "component": { "foreground": "#569CD6", "fontStyle": "bold" },

    // 变量与属性
    "variable": "#9CDCFE",
    "variable.readonly": "#4FC1FF",
    "variable.readonly.defaultLibrary": "#4FC1FF",
    "property": "#9CDCFE",
    "property.readonly": "#4FC1FF",
    "parameter": "#9CDCFE",

    // 函数与方法
    "function": "#DCDCAA",
    "function.defaultLibrary": "#DCDCAA",
    "method": "#DCDCAA",
    "macro": "#BD63C5",

    // 语言专属微调
    "variable.readonly:javascript": "#4FC1FF",
    "variable.readonly:typescript": "#4FC1FF"
  },

  // 2. TextMate 传统词法规则定义 (基础、跨编辑器兼容、回退底座)
  "tokenColors": [
    {
      "name": "Comments",
      "scope": ["comment", "punctuation.definition.comment"],
      "settings": { "foreground": "#6A9955", "fontStyle": "italic" }
    },
    {
      "name": "Keywords & Control Flow",
      "scope": [
        "keyword.control",
        "keyword.control.conditional",
        "keyword.control.loop",
        "keyword.operator.new",
        "keyword.operator.expression"
      ],
      "settings": { "foreground": "#C586C0", "fontStyle": "bold" }
    },
    {
      "name": "Operators",
      "scope": ["keyword.operator", "punctuation.separator.key-value"],
      "settings": { "foreground": "#D4D4D4" }
    },
    {
      "name": "Functions & Call Expressions",
      "scope": [
        "entity.name.function",
        "support.function",
        "entity.name.function.member"
      ],
      "settings": { "foreground": "#DCDCAA" }
    },
    {
      "name": "Types, Classes, Interfaces",
      "scope": [
        "entity.name.type",
        "entity.name.type.class",
        "entity.name.type.interface",
        "entity.name.type.enum",
        "support.type",
        "support.class"
      ],
      "settings": { "foreground": "#4EC9B0" }
    },
    {
      "name": "Strings & Characters",
      "scope": [
        "string",
        "string.quoted",
        "string.template",
        "punctuation.definition.string"
      ],
      "settings": { "foreground": "#CE9178" }
    },
    {
      "name": "Numbers & Booleans",
      "scope": ["constant.numeric", "constant.language.boolean"],
      "settings": { "foreground": "#B5CEA8" }
    },
    {
      "name": "HTML/XML Tags & Component Tags",
      "scope": [
        "entity.name.tag",
        "meta.tag.structure.start.html.vue",
        "support.class.component"
      ],
      "settings": { "foreground": "#569CD6" }
    },
    {
      "name": "Attributes & Props",
      "scope": [
        "entity.other.attribute-name",
        "entity.other.attribute-name.html"
      ],
      "settings": { "foreground": "#9CDCFE" }
    },
    {
      "name": "Punctuation & Delimiters",
      "scope": [
        "punctuation.definition.tag",
        "punctuation.separator.comma",
        "punctuation.terminator"
      ],
      "settings": { "foreground": "#808080" }
    }
  ]
}
```

---

### 2. 官方调试利器：Scope Inspector 使用指南

在调试语法高亮和编写主题规则时，VS Code 内置了 **Scope Inspector（作用域检查器）**：

1. **触发方式**：
   - 按 `F1` 或 `Ctrl+Shift+P` (Mac: `Cmd+Shift+P`) 打开命令面板。
   - 输入并执行：`Developer: Inspect Editor Tokens and Scopes`（中文环境：`开发人员: 检查编辑器标记和作用域`）。
   - 默认快捷键（Mac）：`Cmd + Option + Shift + I`。
2. **面板信息深度解读**：
   - **`language`**: 当前字符所归属的真实语言 ID（在嵌入语言中尤为重要，如 `javascript` vs `html`）。
   - **`token type`**: 词法分类（`other` / `comment` / `string`）。
   - **`semantic token type` & `modifiers`**: LSP 返回的实时语义类型（如 `class`, `readonly, defaultLibrary`）及匹配的主题规则。
   - **`textmate scopes`**: 从底层到顶层的完整 TextMate Scope 继承链（最具体作用域位于列表顶部）。
   - **`foreground`**: 最终生效的 Hex 色值与计算样式，并展示被击中的具体规则是来自 `semanticTokenColors` 还是 `tokenColors`。
