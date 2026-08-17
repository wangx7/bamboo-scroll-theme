package main

import (
	"context"
	"encoding/json"
	"fmt"
	"sync"
	"time"
)

// 结构体与标签测试 (焦墨 #2A2D33 & 赭石 #845438)
type ShuimoPoem struct {
	ID        int64     `json:"id" db:"id"`
	Title     string    `json:"title" db:"title"`
	Author    string    `json:"author" db:"author"`
	Content   string    `json:"content" db:"content"`
	CreatedAt time.Time `json:"created_at"`
}

// 接口定义 (焦墨粗体)
type PoemRenderer interface {
	Render(ctx context.Context, poem *ShuimoPoem) (string, error)
}

type CanvasEngine struct {
	canvasName string
	mu         sync.RWMutex
}

func NewCanvasEngine(name string) *CanvasEngine {
	return &CanvasEngine{
		canvasName: name,
	}
}

// 方法与控制流 (黛蓝 #20526F & 朱砂 #983029)
func (e *CanvasEngine) Render(ctx context.Context, p *ShuimoPoem) (string, error) {
	e.mu.Lock()
	defer e.mu.Unlock()

	select {
	case <-ctx.Done():
		return "", ctx.Err()
	default:
		if p == nil {
			return "", fmt.Errorf("诗词数据不能为空")
		}
	}

	output := fmt.Sprintf("[%s] %s · %s: %s", e.canvasName, p.Title, p.Author, p.Content)
	return output, nil
}

func main() {
	poem := &ShuimoPoem{
		ID:        1,
		Title:     "滕王阁序",
		Author:    "王勃",
		Content:   "秋水共长天一色",
		CreatedAt: time.Now(),
	}

	engine := NewCanvasEngine("宋代澄心堂宣纸")
	res, err := engine.Render(context.Background(), poem)
	if err != nil {
		panic(err)
	}

	bytes, _ := json.MarshalIndent(poem, "", "  ")
	fmt.Println(res)
	fmt.Println(string(bytes))
}
