# 🌌 Galaxy Reaper (银河收割者)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-Automation-43B02A?style=for-the-badge&logo=selenium)](https://www.selenium.dev/)
[![Rich](https://img.shields.io/badge/Rich-Terminal_UI-ff00ff?style=for-the-badge)](https://github.com/Textualize/rich)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-Video_Support-red?style=for-the-badge)](https://github.com/yt-dlp/yt-dlp)

> **[ Veni, Vidi, Cepi ] - The Ultimate Archive Protocol**
> 
> 一个拥有赛博朋克风格终端界面、支持断点续传、智能防封的万能媒体爬虫。

---

## 📖 简介 | Introduction

**Galaxy Reaper** 是一个高度自动化的通用画廊/媒体下载器。它旨在解决传统爬虫“死板、易断线、无交互”的痛点。

无论你是想从 **Rule34/Booru** 等图站批量收藏插画，还是从 **建筑/设计事务所** 官网下载高清作品集，亦或是抓取网页中的 **视频流**，Galaxy Reaper 都能通过其独创的“万能感知引擎”自动识别并收割。

## ✨ 核心特性 | Key Features

### 🧠 智能核心
* **万能感知模式**：自动识别 Booru 类标准图站结构；若不匹配，自动切换至“通用画廊模式”，扫描页面内所有图片和视频。
* **混合媒体支持**：不仅支持 JPG/PNG/WEBP，内置 `yt-dlp` 核心，可嗅探并下载 MP4/MOV/WEBM 及 HLS 流媒体。
* **断点续传**：基于网页标题自动创建归档目录。若任务中断，重启程序可自动跳过已下载文件，实现完美续传。

### 🛡️ 隐形与稳定
* **战术防封 (Stealth Mode)**：独有的心跳保活机制 (`Smart Sleep`)，支持超长间隔挂机（如每页休息 120秒），彻底规避 429 限流。
* **断线重连**：自动监测 Chrome 调试端口，若浏览器崩溃或断连，程序会自动尝试复活连接，无需人工干预。

### 🎨 极致体验
* **Rich UI 终端**：抛弃枯燥的黑白日志，采用黑金配色的仪表盘、动态进度条和文本徽章系统。
* **元数据注入**：自动将网页标题写入图片 Exif 信息（UserComment/XPKeywords），方便本地检索。

---

## 🛠️ 安装 | Installation

### 1. 环境准备
确保你的电脑已安装 [Python 3.10+](https://www.python.org/) 和 [Google Chrome](https://www.google.com/chrome/) 浏览器。

### 2. 克隆仓库
```bash
git clone [https://github.com/你的用户名/Galaxy-Reaper.git](https://github.com/你的用户名/Galaxy-Reaper.git)
cd Galaxy-Reaper
🚀 使用方法 | Usage1. 启动程序Bashpython dpm.py
程序会自动启动一个独立的 Chrome 调试窗口。2. 战术选择程序启动后，通过方向键或数字键选择下载模式：模式说明适用场景🚀 极速收割高并发 (5线程)，无延迟，翻页快普通摄影网站、建筑设计网、对爬虫限制宽松的站点🛡️ 潜行防封单线程，长延迟 (10-20s)，翻页长休眠Rule34, Gelbooru 等反爬严格的图站 (推荐)🔧 手动调校自定义所有参数高级用户3. 开始收割在弹出的 Chrome 窗口中，手动登录目标网站（如需要）。打开包含缩略图的列表页或收藏夹。回到终端，按下 Enter 键。坐和放宽，看着你的硬盘被填满。⚙️ 配置说明 | Configuration你可以在代码顶部的 CONFIG 字典中修改默认参数：PythonCONFIG = {
    "BASE_SAVE_FOLDER": "Galaxy_Reaper_Archive", # 下载根目录
    "MAX_WORKERS": 2,                            # 默认并发数
    "MIN_IMAGE_SIZE_KB": 30,                     # 过滤小于 30KB 的图片
    "VIDEO_EXTS": ('.mp4', '.mov',...)           # 支持的视频格式
}
⚠️ 免责声明 | Disclaimer本工具仅供个人学习与技术研究使用。使用者应对下载内容的版权归属负责。请遵守目标网站的 robots.txt 协议及服务条款。严禁将本工具用于DDoS攻击或非法数据抓取。开发者不对因使用本工具导致的账号封禁或法律纠纷承担任何责任。📜 许可证 | LicenseMIT License © 2026 Galaxy Reaper
