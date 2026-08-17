-- 水墨主题 SQL 语法高亮测试
-- 关键字 (焦墨粗体 #2A2D33) / 函数 (黛蓝 #20526F) / 表名与库名 (赭石 #845438)

CREATE DATABASE IF NOT EXISTS shuimo_db CHARACTER SET utf8mb4;
USE shuimo_db;

CREATE TABLE IF NOT EXISTS poems (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL COMMENT '诗题',
    author VARCHAR(100) NOT NULL COMMENT '作者',
    dynasty ENUM('唐', '宋', '元', '明', '清') NOT NULL DEFAULT '唐',
    content TEXT NOT NULL COMMENT '诗词正文',
    view_count INT UNSIGNED DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_author_dynasty (author, dynasty)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 复杂查询与聚合函数测试
SELECT 
    p.dynasty,
    p.author,
    COUNT(p.id) AS total_poems,
    SUM(p.view_count) AS total_views,
    GROUP_CONCAT(p.title ORDER BY p.id SEPARATOR '、') AS famous_works
FROM 
    shuimo_db.poems AS p
WHERE 
    p.dynasty IN ('唐', '宋')
    AND p.content LIKE '%秋水共长天一色%'
GROUP BY 
    p.dynasty, p.author
HAVING 
    total_poems > 0
ORDER BY 
    total_views DESC
LIMIT 10 OFFSET 0;
