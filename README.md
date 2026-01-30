# 🌌 Galaxy Reaper (银河收割者)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)[https://www.python.org/](https://www.python.org/)
![Selenium](https://img.shields.io/badge/Selenium-Automation-43B02A?style=for-the-badge&logo=selenium)[https://www.selenium.dev/](https://www.selenium.dev/)
![Rich](https://img.shields.io/badge/Rich-Terminal_UI-ff00ff?style=for-the-badge)[https://github.com/Textualize/rich](https://github.com/Textualize/rich)
![yt-dlp](https://img.shields.io/badge/yt--dlp-Video_Support-red?style=for-the-badge)[https://github.com/yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)[LICENSE](LICENSE)

> **[ Veni, Vidi, Cepi ] - The Ultimate Archive Protocol**
>
> 一个拥有赛博朋克风格终端界面、支持断点续传、智能防封的万能媒体爬虫。

---

## 📖 简介 | Introduction

**Galaxy Reaper** 是一个高度自动化的通用画廊/媒体下载器。它旨在解决传统爬虫“死板、易断线、无交互”的痛点。

无论你是想从 **Rule34/Booru** 等图站批量收藏插画，还是从 **建筑/设计事务所** 官网下载高清作品集，亦或是抓取网页中的 **视频流**，Galaxy Reaper 都能通过其独创的“万能感知引擎”自动识别并收割。

### ✨ 核心特性

- **🧠 万能感知**：自动识别 Booru 类标准结构；若不匹配，自动切换至“通用画廊模式”，扫描所有图片/视频。
- **🎥 混合媒体**：内置 `yt-dlp` 核心，支持下载 JPG/PNG 原图及 MP4/MOV/HLS 流媒体。
- **💾 断点续传**：基于网页标题自动归档。任务中断后重启，自动跳过已下载文件。
- **🛡️ 隐形战术**：独有的心跳保活机制 (`Smart Sleep`)，支持每页 120秒+ 的超长潜伏，彻底规避 429 限流。
- **🎨 极致终端**：黑金配色仪表盘、动态进度条、纯文本徽章系统，兼容所有终端环境。

---

## 🛠️ 安装 | Installation

### 1. 环境准备

确保你的电脑已安装 [Python 3.10+](https://www.python.org/) 和 [Google Chrome](https://www.google.com/chrome/) 浏览器。

### 2. 克隆仓库

```bash
git clone [https://github.com/你的用户名/Galaxy-Reaper.git](https://github.com/你的用户名/Galaxy-Reaper.git)
cd Galaxy-Reaper
```

### 3. 安装依赖

程序内置了自动依赖检测，也可以手动安装：

```
pip install -r requirements.txt
```

## 🚀 使用方法 | Usage

### 1. 启动程序

```
python dpm.py
```

*程序会自动启动一个独立的 Chrome 调试窗口，不会影响你原本的浏览器。*

### 2. 选择战术模式

启动后，终端会弹出战术选择菜单：

- **`1`**  **🚀 极速收割**：

  - **并发**: 5线程 | **延迟**: 0秒
  - **适用**: 普通摄影网站、建筑设计网、无反爬限制的站点。
- **`2`**  **🛡️ 潜行防封 (推荐)** ：

  - **并发**: 1线程 | **延迟**: 10-20秒 | **翻页休息**: 60-120秒
  - **适用**: Rule34, Gelbooru 等反爬严格的图站。
- **`3`**  **🔧 手动调校**：

  - 自定义并发数、延迟时间等参数。

### 3. 开始执行

1. 在弹出的 Chrome 窗口中，**手动登录**目标网站（如需要）。
2. 打开包含缩略图的**列表页**或**收藏夹**。
3. 回到终端，按下 `Enter` 键。
4. 程序将自动接管，开始翻页下载。

---

## ⚙️ 高级配置 | Configuration

你可以在 `dpm.py` 顶部的 `CONFIG` 字典中修改默认硬编码参数：

```
CONFIG = {
    "BASE_SAVE_FOLDER": "Galaxy_Reaper_Archive", # 默认下载根目录
    "DEBUG_PORT": 9222,                          # Chrome 调试端口
    "MIN_IMAGE_SIZE_KB": 30,                     # 过滤小于 30KB 的图片
    "VIDEO_EXTS": ('.mp4', '.mov', '.webm',...)  # 支持的视频格式
}
```

---

## ⚠️ 免责声明 | Disclaimer

> **请在使用前仔细阅读以下条款：**

1. **仅供学习**：本工具仅供个人学习 Python 爬虫技术与网络协议研究使用。
2. **版权尊重**：使用者应尊重目标网站的版权说明。请勿传播、售卖下载的有版权保护的内容。
3. **合规使用**：请遵守目标网站的 `robots.txt` 协议及服务条款。严禁将本工具用于 DDoS 攻击、恶意流量消耗或非法数据抓取。
4. **责任豁免**：开发者不对因使用本工具导致的账号封禁、IP 封锁或法律纠纷承担任何责任。**您需自行承担运行脚本的所有风险。**

---

## 📜 许可证 | License

本项目基于 [MIT License](https://www.google.com/search?q=LICENSE) 开源。
