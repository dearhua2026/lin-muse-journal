# 对话手记 · Lin & Muse

Lin 与 Muse 的每一次沟通，都整理成一篇文章，发布成网站。

- 🌐 网站：https://lin-journal.pages.dev
- 📝 文章源码：`articles/*.md`（Markdown + frontmatter）
- 🔨 构建：`python3 build.py` → 生成静态站到 `site/`
- 🚀 发布：Cloudflare Pages（直接上传）

## 写新文章

在 `articles/` 下新建 `YYYY-MM-DD-主题.md`，开头加上：

```markdown
---
title: 文章标题
date: 2026-10-03
tags: [标签1, 标签2]
excerpt: 一句话摘要
---

正文……
```

然后运行 `python3 build.py`，把 `site/` 目录部署到 Cloudflare Pages 即可。
