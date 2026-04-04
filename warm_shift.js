/**
 * Night Shift 色温变换脚本
 * 
 * macOS Night Shift 的原理：基于黑体辐射的色温变换
 * 标准显示器白点为 D65 (6500K)，Night Shift 将色温降低到约 3500K-4500K
 * 
 * 核心方法：对 RGB 三通道应用乘法系数（color gain），而非加减固定值
 * 低色温 = 红色保持/增强，绿色略降，蓝色显著降低
 * 
 * 色温对应的 RGB 增益系数（基于 Planckian locus / 黑体辐射曲线）：
 * 6500K (标准): R=1.000, G=1.000, B=1.000
 * 5000K (微暖): R=1.000, G=0.932, B=0.834
 * 4500K (暖):   R=1.000, G=0.897, B=0.764
 * 4000K (较暖): R=1.000, G=0.855, B=0.685
 * 3500K (很暖): R=1.000, G=0.804, B=0.592
 * 2700K (极暖): R=1.000, G=0.718, B=0.442
 */

const fs = require('fs');
const path = require('path');

// 目标色温 (可调整: 3500-5000K 范围较自然)
const TARGET_TEMP = 5000; // K

/**
 * 基于 Tanner Helland 的黑体辐射算法计算色温对应 RGB 增益
 * 参考: https://tannerhelland.com/2012/09/18/convert-temperature-rgb-algorithm.html
 */
function colorTempToGain(tempK) {
  const temp = tempK / 100;
  let r, g, b;

  // Red
  if (temp <= 66) {
    r = 255;
  } else {
    r = 329.698727446 * Math.pow(temp - 60, -0.1332047592);
    r = Math.min(255, Math.max(0, r));
  }

  // Green
  if (temp <= 66) {
    g = 99.4708025861 * Math.log(temp) - 161.1195681661;
  } else {
    g = 288.1221695283 * Math.pow(temp - 60, -0.0755148492);
  }
  g = Math.min(255, Math.max(0, g));

  // Blue
  if (temp >= 66) {
    b = 255;
  } else if (temp <= 19) {
    b = 0;
  } else {
    b = 138.5177312231 * Math.log(temp - 10) - 305.0447927307;
    b = Math.min(255, Math.max(0, b));
  }

  return { r: r / 255, g: g / 255, b: b / 255 };
}

// 计算从 6500K -> 目标色温的增益比例
const gain6500 = colorTempToGain(6500);
const gainTarget = colorTempToGain(TARGET_TEMP);

const gainR = gainTarget.r / gain6500.r;
const gainG = gainTarget.g / gain6500.g;
const gainB = gainTarget.b / gain6500.b;

console.log(`色温变换: 6500K -> ${TARGET_TEMP}K`);
console.log(`RGB 增益: R=${gainR.toFixed(3)}, G=${gainG.toFixed(3)}, B=${gainB.toFixed(3)}`);

/**
 * sRGB gamma 解码 (sRGB -> 线性)
 */
function srgbToLinear(c) {
  c = c / 255;
  return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
}

/**
 * sRGB gamma 编码 (线性 -> sRGB)
 */
function linearToSrgb(c) {
  c = Math.max(0, Math.min(1, c));
  return c <= 0.0031308 ? Math.round(c * 12.92 * 255) : Math.round((1.055 * Math.pow(c, 1 / 2.4) - 0.055) * 255);
}

/**
 * 对一个 hex 颜色应用 Night Shift 色温变换
 */
function nightShift(hex) {
  if (!hex || typeof hex !== 'string') return hex;

  let clean = hex.replace('#', '');

  // 提取 alpha 通道
  let alpha = '';
  if (clean.length === 8) {
    alpha = clean.substring(6, 8);
    clean = clean.substring(0, 6);
  } else if (clean.length === 4) {
    alpha = clean[3] + clean[3];
    clean = clean[0] + clean[0] + clean[1] + clean[1] + clean[2] + clean[2];
  } else if (clean.length === 3) {
    clean = clean[0] + clean[0] + clean[1] + clean[1] + clean[2] + clean[2];
  } else if (clean.length !== 6) {
    return hex;
  }

  let r = parseInt(clean.substring(0, 2), 16);
  let g = parseInt(clean.substring(2, 4), 16);
  let b = parseInt(clean.substring(4, 6), 16);

  if (isNaN(r) || isNaN(g) || isNaN(b)) return hex;

  // 1. sRGB -> 线性空间
  let linR = srgbToLinear(r);
  let linG = srgbToLinear(g);
  let linB = srgbToLinear(b);

  // 2. 应用色温增益 (乘法变换，这是 Night Shift 的核心)
  linR *= gainR;
  linG *= gainG;
  linB *= gainB;

  // 3. 线性空间 -> sRGB
  let newR = linearToSrgb(linR);
  let newG = linearToSrgb(linG);
  let newB = linearToSrgb(linB);

  const toHex = (n) => n.toString(16).padStart(2, '0');

  // 保持原始大小写风格
  const hasUpper = /[A-F]/.test(hex);
  let result = `#${toHex(newR)}${toHex(newG)}${toHex(newB)}${alpha}`;
  if (hasUpper) {
    result = '#' + result.substring(1).toUpperCase();
  }

  return result;
}

/**
 * 处理主题文件
 */
function processThemeFile(filePath) {
  console.log(`\n处理: ${path.basename(filePath)}`);

  let content = fs.readFileSync(filePath, 'utf8');

  let count = 0;
  content = content.replace(/"(#[0-9a-fA-F]{3,8})"/g, (match, color) => {
    const shifted = nightShift(color);
    if (shifted !== color) count++;
    return `"${shifted}"`;
  });

  fs.writeFileSync(filePath, content, 'utf8');
  console.log(`  转换了 ${count} 个颜色值`);
}

// 只处理 solarized night shift 主题
const targetFile = path.join(__dirname, 'themes', 'koi-noir-solarized-night-shift-color-theme.json');
processThemeFile(targetFile);

console.log('\n✅ Night Shift 色温变换完成!');
