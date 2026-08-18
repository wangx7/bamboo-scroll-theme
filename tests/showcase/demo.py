"""
水墨主题 Python 语法高亮测试范例
"""
import math
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

# 常量定义 (重墨 #3A3E43)
MAX_BUFFER_SIZE: int = 4096
PI_CONSTANT: float = 3.1415926535

@dataclass
class InkStroke:
    x: float
    y: float
    pressure: float = 1.0
    color: str = "#232527"

    @property
    def is_heavy(self) -> bool:
        return self.pressure > 0.8

class CalligraphyCanvas:
    """宣纸水墨画布模拟器"""
    
    def __init__(self, name: str = "宋代澄心堂纸") -> None:
        self.name: str = name
        self._strokes: List[InkStroke] = []

    def add_stroke(self, stroke: InkStroke) -> None:
        # 控制流测试 (朱砂 #8F3D2D)
        if stroke.pressure <= 0:
            raise ValueError(f"笔压必须大于 0: {stroke.pressure}")
        
        self._strokes.append(stroke)
        # f-string 插值测试 (松烟绿与变量分层)
        print(f"[墨迹] 在 ({stroke.x:.1f}, {stroke.y:.1f}) 处落笔，笔力: {stroke.pressure}")

    def render(self) -> Dict[str, int]:
        heavy_count = sum(1 for s in self._strokes if s.is_heavy)
        return {
            "total_strokes": len(self._strokes),
            "heavy_strokes": heavy_count,
        }

if __name__ == "__main__":
    canvas = CalligraphyCanvas()
    canvas.add_stroke(InkStroke(10.0, 20.0, pressure=0.9))
    print(canvas.render())
