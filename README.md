# 🌌 Galaxy Reaper (银河收割者)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-Automation-43B02A?style=for-the-badge&logo=selenium)](https://www.selenium.dev/)
[![Rich](https://img.shields.io/badge/Rich-Terminal_UI-ff00ff?style=for-the-badge)](https://github.com/Textualize/rich)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-Video_Support-red?style=for-the-badge)](https://github.com/yt-dlp/yt-dlp)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

> **[ Veni, Vidi, Cepi ] - The Ultimate Archive Protocol**
> 
> 一个拥有赛博朋克风格终端界面、支持断点续传、智能防封的万能媒体爬虫。

---

## 📖 简介 | Introduction

**Galaxy Reaper** 是一个高度自动化的通用画廊/媒体下载器。它旨在解决传统爬虫“死板、易断线、无交互”的痛点。

无论你是想从 **Rule34/Booru** 等图站批量收藏插画，还是从 **建筑/设计事务所** 官网下载高清作品集，亦或是抓取网页中的 **视频流**，Galaxy Reaper 都能通过其独创的“万能感知引擎”自动识别并收割。

### ✨ 核心特性
* **🧠 万能感知**：自动识别 Booru 类标准结构；若不匹配，自动切换至“通用画廊模式”，扫描所有图片/视频。
* **🎥 混合媒体**：内置 `yt-dlp` 核心，支持下载 JPG/PNG 原图及 MP4/MOV/HLS 流媒体。
* **💾 断点续传**：基于网页标题自动归档。任务中断后重启，自动跳过已下载文件。
* **🛡️ 隐形战术**：独有的心跳保活机制 (`Smart Sleep`)，支持每页 120秒+ 的超长潜伏，彻底规避 429 限流。
* **🎨 极致终端**：黑金配色仪表盘、动态进度条、纯文本徽章系统，兼容所有终端环境。

---

## 🛠️ 安装 | Installation

### 1. 环境准备
确保你的电脑已安装 [Python 3.10+](https://www.python.org/) 和 [Google Chrome](https://www.google.com/chrome/) 浏览器。

### 2. 克隆仓库
```bash
git clone [https://github.com/你的用户名/Galaxy-Reaper.git](https://github.com/你的用户名/Galaxy-Reaper.git)
cd Galaxy-Reaper
