<p align="center">
  <img src="logo.png" alt="水墨 Theme Logo" width="128" height="128">
</p>

<h1 align="center">水墨 Theme</h1>

<p align="center">
  <em>点墨成渊映竹影，化筠为简蕴幽香。指尖经纬裁风雨，且护明眸夜未央。</em>
</p>

<p align="center">
  <a href="https://marketplace.visualstudio.com/items?itemName=wangx123.shuimo-theme">
    <img src="https://img.shields.io/visual-studio-marketplace/v/wangx123.shuimo-theme?label=VS%20Code%20Marketplace&logo=visual-studio-code&color=A8432A&style=flat-square" alt="VS Code Marketplace Version">
  </a>
  <a href="https://marketplace.visualstudio.com/items?itemName=wangx123.shuimo-theme">
    <img src="https://img.shields.io/visual-studio-marketplace/i/wangx123.shuimo-theme?color=3D6E56&style=flat-square" alt="Installs">
  </a>
  <a href="./LICENSE.md">
    <img src="https://img.shields.io/badge/License-MIT-2B6CB0?style=flat-square" alt="License">
  </a>
</p>

---

## ✨ 简介

**水墨 Theme** 是一款以中国传统水墨画为灵感的 Visual Studio Code 浅色主题扩展。

取法于墨分五色、宣纸质感与文人画韵，将编辑器化作一方素净的宣纸——  
以朱砂为关键词，以靛蓝为函数，以竹青为类型，以墨绿为注释，以赭石为常量……  
每一种色彩都源自中国传统色谱，让代码在淡雅的底色中如行云流水般展开。

> **护眼 · 雅致 · 专注**  
> 低对比度设计呵护长时间编码的双眼，文人气质的配色让编程成为一种享受。

---

## 🎨 主题一览

本扩展包含 **两款** 精心调制的浅色主题，风格各异，各有千秋：

### 水墨 · 世界

> 明净素雅，如宣纸铺陈

- **底色**：温暖的宣纸色 `#F6F5E1`，仿佛触手可及的宣纸质感
- **墨色**：沉稳的深墨 `#2A2C30`，字字清晰如碑拓
- **点缀**：朱砂红 `#A8432A` 标记关键词，靛青 `#2B6CB0` 勾勒函数
- **风格**：淡雅留白，无边框干扰，专注于代码本身
- **活动栏**：深色侧栏搭配暖色主体，层次分明

### 水墨 · 竹韵

> 苍翠欲滴，如竹林深处

- **底色**：清新的竹绿 `#789262`，满目翠色令人心旷神怡
- **墨色**：浓郁的墨黑 `#0A0A0A`，对比鲜明而不刺眼
- **点缀**：银杏金 `#CCBA8A` 高亮匹配，翠竹绿 `#96AB81` 标记选区
- **风格**：浓墨重彩，如同置身于竹林书斋之中
- **活动栏**：深竹色 `#1A2616` 沉稳大气

---

## 🖌️ 色彩哲学

主题配色取法中国传统色谱，每一种颜色都有其意蕴：

| 语义角色 | 水墨·世界 | 色名 | 用意 |
|:---|:---|:---|:---|
| **关键词 / 控制流** | `#A8432A` | 朱砂 | 醒目如印章，标记代码骨架 |
| **函数 / 方法** | `#2B6CB0` | 靛青 | 沉静如深潭，勾勒逻辑脉络 |
| **类型 / 类** | `#3D6E56` | 竹青 | 苍翠如修竹，承载数据结构 |
| **字符串** | `#1A7A6D` | 青碧 | 清澈如溪涧，展现文本内容 |
| **注释** | `#7C9A72` | 苔绿 | 低调如苔痕，斜体吟唱旁注 |
| **常量 / 数字** | `#B5651D` | 赭石 | 温润如古砖，标记不变之值 |
| **修饰符 / 装饰器** | `#7B539E` | 紫藤 | 典雅如藤蔓，点缀元信息 |
| **参数** | `#8B6F4E` | 赭黄 | 朴实如泥土，斜体标记传参 |
| **属性名** | `#8C7A2B` | 秋香 | 沉稳如枯叶，标注属性特征 |
| **运算符 / 标点** | `#5A5F66` | 烟灰 | 淡然如远山，不争不抢 |

---

## 📦 安装

### 方式一：VS Code 扩展市场（推荐）

1. 打开 VS Code
2. 进入扩展面板 (`Ctrl+Shift+X` / `Cmd+Shift+X`)
3. 搜索 **`水墨 Theme`** 或 **`shuimo-theme`**
4. 点击 **安装**
5. `Ctrl+K Ctrl+T` / `Cmd+K Cmd+T` 打开主题选择器
6. 选择 **水墨·世界** 或 **水墨·竹韵**

### 方式二：命令行安装

```bash
code --install-extension wangx123.shuimo-theme
```

### 方式三：手动安装

```bash
git clone https://github.com/wangx7/shuimo-theme.git
cd shuimo-theme
npx @vscode/vsce package
code --install-extension shuimo-theme-*.vsix
```

---

## 🌐 语言支持

主题为以下语言提供了 **精细调优的语法高亮**，确保每种语言的语义元素都有恰当的颜色表达：

<table>
<tr>
<td width="33%">

**前端**
- JavaScript / JSX
- TypeScript / TSX
- HTML
- CSS / SCSS / Less
- Vue
- JSON

</td>
<td width="33%">

**后端**
- Python
- Java
- Go
- Rust
- C / C++
- C#

</td>
<td width="33%">

**其他**
- PHP
- Ruby
- Kotlin
- Swift
- Lua
- SQL
- Shell / Bash
- YAML / TOML
- Markdown
- Dockerfile

</td>
</tr>
</table>

> 所有语言均支持 **语义高亮 (Semantic Highlighting)**，在支持 Language Server 的语言中可获得更精准的着色体验。

---

## ✅ 主题特性

- 🎨 **中国传统色谱** — 所有颜色均取材自传统色名，和谐统一
- 👁️ **护眼低对比度** — 浅色主题精心调校对比度，适合长时间编码
- 🖼️ **自定义背景纹理** — 内置宣纸纹理与水墨画背景，营造文人书斋氛围
- 🔤 **语义高亮** — 支持 VS Code Semantic Highlighting，精准区分语义
- 📝 **Markdown 标题层级** — H1 至 H6 标题使用渐变墨色，层次分明
- 🏷️ **TODO / FIXME 高亮** — 代码注释中的 `TODO`、`FIXME`、`NOTE`、`HACK` 等标记独立着色
- 🧩 **Vue / JSX 组件标签** — 大驼峰组件标签使用独特的醒目色彩 `#C05028`
- ⚙️ **完整 UI 主题化** — 从编辑器到终端，从侧边栏到状态栏，全方位统一风格

---

## 🏗️ 项目结构

```
shuimo-theme/
├── themes/
│   ├── shuimo-shijie-theme.json   # 水墨·世界 主题定义
│   └── shuimo-zhuyun-theme.json   # 水墨·竹韵 主题定义
├── backgrounds/
│   ├── editorBackgrounds.png      # 编辑器背景
│   ├── sidebarBackgrounds.png     # 侧边栏背景（水墨荷花）
│   ├── panelBackgrounds.png       # 面板背景
│   └── wenli.png                  # 宣纸纹理
├── logo.png                       # 扩展图标（水墨山竹）
├── package.json                   # 扩展清单
├── LICENSE.md                     # MIT 许可证
└── README.md                      # 本文件
```

---

## 🛠️ 本地开发

如果你想参与开发或自定义主题：

```bash
# 克隆仓库
git clone https://github.com/wangx7/shuimo-theme.git
cd shuimo-theme

# 安装依赖
npm install

# 在 VS Code 中调试
# 按 F5 启动扩展开发宿主窗口，实时预览主题效果

# 打包
npm run build
```

主题 JSON 文件结构：

- **`colors`** — UI 界面颜色（编辑器、侧边栏、状态栏等）
- **`tokenColors`** — 语法高亮规则（基于 TextMate 作用域）
- **`semanticTokenColors`** — 语义高亮规则（基于 Language Server）

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

- 🐛 **发现问题？** 请在 [GitHub Issues](https://github.com/wangx7/shuimo-theme/issues) 中反馈
- 💡 **有新想法？** 欢迎提交 Feature Request
- 🎨 **配色建议？** 欢迎讨论，但请保持中国传统色谱的整体风格

---

## 📜 许可证

本项目基于 [MIT License](./LICENSE.md) 开源。

---

<p align="center">
  <sub>墨落纸上，代码如诗。</sub>
</p>
