# 水墨主题 (Shuimo Theme)

一款根植于东方美学的 VS Code 主题集合，以「意象留白」与「长时护眼」为核心设计理念。

---

## 主题

### 水墨·世界

> 大千一墨化鸿蒙，万象森罗指掌中。
> 代码纵横经纬里，山河入眼夜朦胧。

以宣纸暖白 `#F6F5E1` 为底，采用传统矿物颜料色系区分代码语义：

| 角色 | 色板 | 色值 | 字体 |
|---|---|---|---|
| 正文 / 变量 | 松烟墨 | `#2A2C30` | 常规 |
| 注释 | 竹青 | `#4C7548` | 斜体 |
| 字符串 / 正则 | 石青 | `#1F7A85` | 常规 |
| 函数 / 方法 | 花青 | `#315D8C` | 常规 |
| 关键字 / 流程控制 | 朱砂 | `#9A3B26` | 粗体 |
| 数字 / 只读量 | 赭石 | `#8A4B2F` | 常规 |
| 布尔 / 常量 / 警告金 | 藤黄 | `#846616` | 常规 |
| 类型 / 类 / 命名空间 | 焦墨 | `#232527` | 粗体 |
| 属性 / 标点 / 运算符 | 淡墨 | `#4A4F56` / `#5A5F66` | 常规 |
| 修饰符 / 装饰器 / 宏 | 紫墨 | `#7A5B8C` | 粗体 / 斜体 |

**v2.3 长时编程优化：**

- 注释改为独立竹青，与正文松烟墨可分辨性达 `2.63:1`，不再和内容粘在一起。
- 全部静态语法 Token 对比度达到 WCAG 2.1 AA（含注释在内均 `>= 4.5:1`）。
- 选择区、查找命中、缩进参考线、括号匹配等交互层更清晰，焦点边框与活动标签页采用朱砂提示。
- 语义高亮扩展至 36 项，并补充 C#、PHP、Ruby、Kotlin、Swift、Lua、Dockerfile 与 JSX/TSX 规则。
- Markdown H1-H6 采用阶梯墨色；终端 ANSI 16 色按矿彩重新校准。

### 水墨·竹韵

> 幽篁斜抱半窗风，碎叶交筛落翠空。
> 敲罢繁星织夜雨，绿荫长护眼瞳中。

以青竹为底色，搭配浓墨与黛绿文字。精心调优的对比度，适合长时间沉浸式开发。

---

## 背景

为达到极致体验，建议搭配背景图片。可使用 [Background](https://marketplace.visualstudio.com/items?itemName=Katsute.code-background) 扩展，参考壁纸见 [backgrounds 目录](https://github.com/wangx7/shuimo-theme/tree/main/backgrounds)。

---

## 推荐搭配

水墨主题已为以下扩展预设配色，安装后即可获得一致的视觉体验。

### Error Lens

错误 / 警告 / 提示的行内高亮已与主题色板对齐：朱砂红表错误、藤黄表警告、花青表信息、淡墨表提示。无需额外配置。

### Better Comments

将以下配置复制到 `settings.json`，让注释按语义着色，与水墨色板保持一致：

```jsonc
"betterComments.tags": [
  { "tag": "!",     "color": "#9A3B26", "strikethrough": false, "underline": false, "backgroundColor": "transparent", "bold": true,  "italic": false },
  { "tag": "?",     "color": "#315D8C", "strikethrough": false, "underline": false, "backgroundColor": "transparent", "bold": false, "italic": true  },
  { "tag": "TODO",  "color": "#8A4B2F", "strikethrough": false, "underline": false, "backgroundColor": "transparent", "bold": true,  "italic": false },
  { "tag": "*",     "color": "#5A5F66", "strikethrough": false, "underline": false, "backgroundColor": "transparent", "bold": false, "italic": true  },
  { "tag": "//",    "color": "#4C7548", "strikethrough": true,  "underline": false, "backgroundColor": "transparent", "bold": false, "italic": false }
]
```

| 标签 | 语义 | 颜色 | 字体 |
|---|---|---|---|
| `!` | 警示 | 朱砂红 | 粗体 |
| `?` | 疑问 | 花青蓝 | 斜体 |
| `TODO` | 待办 | 赭石 | 粗体 |
| `*` | 强调 | 淡墨 | 斜体 |
| `//` | 弃用 | 竹青 | 删除线 |

### Todo Tree / TODO Highlight

注释中的 `TODO` / `FIXME` / `XXX` / `HACK` / `NOTE` 关键字已通过 tokenColors 着色：`TODO` 朱砂红粗体、`FIXME`/`XXX` 赭石、`HACK`/`NOTE` 花青蓝斜体。

---

## 安装

VS Code 扩展市场搜索 `水墨 Theme` 安装。

🔗 [GitHub 仓库](https://github.com/wangx7/shuimo-theme)