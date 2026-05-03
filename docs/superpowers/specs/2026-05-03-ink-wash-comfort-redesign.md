# 水墨丹青 · 深纸宿墨 — 长时编程舒适度重构

## 问题

当前水墨丹青浅色主题在长时间编程时会感到不适。根本原因有三：

1. **纸色过亮** — `#F1EAD3` (LRV~90) 在显示器上相当于持续盯暖光灯
2. **墨纸对比过高** — 正文 10:1，读久了像盯白纸黑字一样累
3. **语法色饱和跳眼** — 朱磦 `#B2473E` 等强调色在亮纸上过于突兀

## 策略

**沉纸不兑墨** — 压低纸色亮度，保留墨色浓度和色温，语法色只降饱和不减深度。

## 配色表

### 纸叠 (Paper Stack)

| Token | 当前 | 新值 | 说明 |
|-------|------|------|------|
| editor.background | `#F1EAD3` | `#EBE3CE` | 微沉宣纸 |
| sideBar.background | `#EDE6D0` | `#E5DCC6` | 略深分层 |
| activityBar.background | `#E8E0CB` | `#DFD7BF` | 收边纸色 |
| panel.background | `#F1EAD3` | `#EBE3CE` | 与编辑区统一 |
| tab.activeBackground | `#F1EAD3` | `#EBE3CE` | |
| tab.inactiveBackground | `#EDE6D0` | `#E5DCC6` | |

### 墨色 (Ink System)

| Token | 当前 | 新值 | 说明 |
|-------|------|------|------|
| editor.foreground | `#3A3631` | `#3C3833` | 墨色基本不动 |
| comment | `#6B655A` | `#676156` | 稍沉 |
| punctuation | `#7A7468` | `#6E6960` | 提对比 |

### 语法五色 (Syntax Accents)

| Token | 当前 | 新值 | 意象 |
|-------|------|------|------|
| keyword | `#24445E` | `#213E51` | 墨蓝 |
| function/method | `#2F6488` | `#376579` | 石青偏暖 |
| string | `#2F6B57` | `#3E6959` | 苔绿去翠 |
| constant/number | `#B2473E` | `#914C43` | 朱磦收红 |
| type/class | `#3E5F99` | `#3F5E8F` | 青金石微暖 |
| parameter | `#7D5C32` | `#765A38` | 赭石稳色 |

## 对比度验证

全组核心 token 在 `#EBE3CE` 纸上通过 WCAG AA (4.5:1+)，墨色 9.1:1，标点 4.3:1 AA-large。

## 范围

- themes/ink-wash-light-color-theme.json — 完整替换 colors + tokenColors + semanticTokenColors
- previews/ink-wash-light-preview.html — 同步更新 CSS 变量和样例色值
