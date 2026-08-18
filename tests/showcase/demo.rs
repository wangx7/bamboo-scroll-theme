//! 水墨主题 Rust 语法与宏高亮测试

use std::fmt::{self, Display, Formatter};

/// 纸张纹理枚举 (重墨常量 #3A3E43)
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PaperTexture {
    ShengXuan,
    ShuXuan,
    ChengXinTang,
}

/// 笔触特征特质 (焦墨 #232527)
pub trait CalligraphyStroke {
    fn stroke_name(&self) -> &'static str;
    fn draw<'a>(&'a self, canvas: &'a mut String) -> Result<(), fmt::Error>;
}

pub struct InkBrush<'a> {
    pub name: &'a str,
    pub texture: PaperTexture,
    pub thickness: f64,
}

impl<'a> InkBrush<'a> {
    pub fn new(name: &'a str, texture: PaperTexture) -> Self {
        Self {
            name,
            texture,
            thickness: 1.5,
        }
    }
}

impl<'a> CalligraphyStroke for InkBrush<'a> {
    fn stroke_name(&self) -> &'static str {
        "点墨成渊"
    }

    fn draw<'b>(&'b self, canvas: &'b mut String) -> Result<(), fmt::Error> {
        // 模式匹配与控制流 (朱砂 #8F3D2D)
        match self.texture {
            PaperTexture::ChengXinTang => {
                canvas.push_str("【澄心玉版宣】秋水共长天一色\n");
            }
            _ => {
                canvas.push_str("【宣纸】墨韵流淌\n");
            }
        }
        Ok(())
    }
}

impl<'a> Display for InkBrush<'a> {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        write!(f, "Brush(name: {}, texture: {:?})", self.name, self.texture)
    }
}

fn main() {
    let brush = InkBrush::new("狼毫中楷", PaperTexture::ChengXinTang);
    let mut canvas = String::new();
    if let Ok(()) = brush.draw(&mut canvas) {
        println!("{}", canvas);
    }
}
