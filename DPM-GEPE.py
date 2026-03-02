import os
import sys
import time
import re
import random
import subprocess
import socket
import importlib.util
import hashlib
from datetime import datetime
from urllib.parse import urlparse, unquote, urljoin, parse_qs
from concurrent.futures import ThreadPoolExecutor, as_completed

# === ✅ 自动环境配置 & 依赖检测 ===
if os.name == 'nt':
    try:
        os.system('chcp 65001 >nul')
        os.system('mode con: cols=120 lines=40')
    except: pass

def check_requirements():
    required = {
        'rich': 'rich', 
        'yt-dlp': 'yt_dlp', 
        'selenium': 'selenium', 
        'beautifulsoup4': 'bs4',
        'piexif': 'piexif',
        'Pillow': 'PIL',
        'webdriver-manager': 'webdriver_manager'
    }
    missing = [pkg for pkg, imp in required.items() if importlib.util.find_spec(imp) is None]
    if missing:
        print(f"系统初始化: 正在部署核心组件 [{', '.join(missing)}]...")
        for pkg in missing: 
            try: subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
            except: sys.exit(1)
        time.sleep(1)

check_requirements()

import requests
import piexif
import piexif.helper
from PIL import Image, PngImagePlugin
from bs4 import BeautifulSoup
import yt_dlp

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, FloatPrompt
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.text import Text
from rich.box import DOUBLE, HEAVY_EDGE

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException, InvalidSessionIdException

# ==========================================
# 🎨 视觉风格定义
# ==========================================
C_GOLD = "#D4AF37"
C_BG = "#080808"
C_ACCENT = "#F4E29E"
C_BRONZE = "#8C7853"
C_ERROR = "#FF4500"
C_SUCCESS = "#00FF7F"
C_INFO = "#00BFFF"

console = Console(style=f"{C_ACCENT} on {C_BG}", width=118)

# ==========================================
# ⚙️ 核心配置
# ==========================================
CONFIG = {
    "BASE_SAVE_FOLDER": "Galaxy_Reaper_Archive",
    "DEBUG_PORT": 9222,
    "DEBUG_HOST": "127.0.0.1",
    
    "MAX_WORKERS": 2,           
    "TIMEOUT": 25,              
    "DELAY_MIN": 1.0,
    "DELAY_MAX": 2.0,
    "PAGE_REST_MIN": 5.0,
    "PAGE_REST_MAX": 10.0,
    "MODE": "GALLERY",
    
    "MIN_IMAGE_SIZE_KB": 15,
    "USER_DATA_DIR_NAME": "Chrome_Crawler_Profile",
    "VIDEO_EXTS": ('.mp4', '.mov', '.webm', '.mkv', '.avi', '.m4v')
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# ==========================================
# 🎩 UI 呈现层
# ==========================================
class GalaxyUI:
    @staticmethod
    def header():
        console.clear()
        title_art = """
     ██████╗  █████╗ ██╗      █████╗ ██╗  ██╗██╗   ██╗
    ██╔════╝ ██╔══██╗██║     ██╔══██╗╚██╗██╔╝╚██╗ ██╔╝
    ██║  ███╗███████║██║     ███████║ ╚███╔╝  ╚████╔╝ 
    ██║   ██║██╔══██║██║     ██╔══██║ ██╔██╗   ╚██╔╝  
    ╚██████╔╝██║  ██║███████╗██║  ██║██╔╝ ██╗   ██║   
     ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
        """
        subtitle = "R E A P E R   P R O T O C O L   v 1 6 . 5"
        info_text = Text()
        info_text.append(title_art, style=f"bold {C_GOLD}")
        info_text.append(f"\n{subtitle.center(56)}", style=f"bold {C_ACCENT}")
        panel = Panel(info_text, box=DOUBLE, border_style=C_GOLD, padding=(1, 2), title=f"[{C_BRONZE}] EST. 2026 [/]")
        console.print(panel)

    @staticmethod
    def strategy_menu():
        console.print(f"\n[{C_GOLD}]:: TACTICAL SELECTION :: (战术选择)[/]")
        table = Table(box=HEAVY_EDGE, border_style=C_BRONZE, show_header=True, header_style=f"bold {C_BG} on {C_GOLD}", expand=True)
        table.add_column("ID", justify="center", width=6, style=f"bold {C_GOLD}")
        table.add_column("MODE", style=f"bold {C_ACCENT}", width=22)
        table.add_column("DETAILS", style=f"{C_BRONZE}")
        
        # ✨ 修复排版：使用战术文本徽章代替 Emoji，彻底解决 Windows 终端对齐问题
        table.add_row("1", "[ FAST ] 极速画廊", "点进链接下大图 | 适合: 普通图站/建筑网")
        table.add_row("2", "[ SAFE ] 潜行画廊", "点进链接下大图 (慢速防封) | 适合: Rule34")
        table.add_row("3", "[ FLOW ] 单页瀑布流", "不翻页，直接抓取当前页所有图 | 适合: 微信公众号/知乎")
        table.add_row("4", "[ EDIT ] 手动调校", "自定义参数")
        console.print(table)
        
        choice = Prompt.ask(f"[{C_GOLD}]Command >[/]", choices=["1", "2", "3", "4"], default="3")
        
        if choice == '1':
            CONFIG["MODE"] = "GALLERY"
            CONFIG["MAX_WORKERS"] = 5; CONFIG["DELAY_MIN"] = 0.1; CONFIG["DELAY_MAX"] = 0.5
            GalaxyUI.log("SYS", "极速画廊模式已装载。", "warn")
        elif choice == '2':
            CONFIG["MODE"] = "GALLERY"
            CONFIG["MAX_WORKERS"] = 1; CONFIG["DELAY_MIN"] = 10.0; CONFIG["DELAY_MAX"] = 20.0
            GalaxyUI.log("SYS", "潜行画廊模式已激活。", "success")
        elif choice == '3':
            CONFIG["MODE"] = "SINGLE"
            CONFIG["MAX_WORKERS"] = 3; CONFIG["DELAY_MIN"] = 0.5; CONFIG["DELAY_MAX"] = 1.5
            GalaxyUI.log("SYS", "单页瀑布流模式已锁定 (专杀微信)。", "info")
        elif choice == '4':
            CONFIG["MODE"] = "GALLERY"
            CONFIG["MAX_WORKERS"] = IntPrompt.ask(f"[{C_BRONZE}]并发数[/]", default=2)
            CONFIG["DELAY_MIN"] = FloatPrompt.ask(f"[{C_BRONZE}]最小延迟(s)[/]", default=1.5)

    @staticmethod
    def log(tag, message, level="info"):
        time_str = datetime.now().strftime("%H:%M:%S")
        if level == "success": color, badge = C_SUCCESS, "[OK]"
        elif level == "error": color, badge = C_ERROR, "[!!]"
        elif level == "warn": color, badge = C_GOLD, "[WARN]"
        elif level == "skip": color, badge = C_BRONZE, "[SKIP]"
        else: color, badge = C_INFO, "[INFO]"
        console.print(f"[{C_BRONZE}]{time_str}[/] [{color} bold]{badge:<6}[/] [{C_GOLD}]{tag:<8}[/] {message}")

# ==========================================
# 🛠️ 浏览器控制
# ==========================================
def find_chrome_path():
    possible_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%USERPROFILE%\AppData\Local\Google\Chrome\Application\chrome.exe")
    ]
    for path in possible_paths:
        if os.path.exists(path): return path
    return None

def is_port_open(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try: s.settimeout(1); s.connect((host, port)); s.close(); return True
    except: return False

def ensure_chrome_debugger():
    if is_port_open(CONFIG["DEBUG_HOST"], CONFIG["DEBUG_PORT"]): return
    chrome_path = find_chrome_path()
    if not chrome_path: sys.exit(1)
    user_data_dir = os.path.expandvars(fr"%USERPROFILE%\{CONFIG['USER_DATA_DIR_NAME']}")
    if not os.path.exists(user_data_dir): os.makedirs(user_data_dir)
    try: subprocess.Popen([chrome_path, f"--remote-debugging-port={CONFIG['DEBUG_PORT']}", f"--user-data-dir={user_data_dir}"])
    except: sys.exit(1)
    for _ in range(10):
        if is_port_open(CONFIG["DEBUG_HOST"], CONFIG["DEBUG_PORT"]): return
        time.sleep(1)

def connect_to_chrome():
    ensure_chrome_debugger()
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", f"{CONFIG['DEBUG_HOST']}:{CONFIG['DEBUG_PORT']}")
    try: return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    except: sys.exit(1)

def check_and_reconnect(driver):
    try: _ = driver.window_handles; return driver
    except:
        try: return connect_to_chrome()
        except: sys.exit(1)

def smart_sleep(driver, duration):
    with console.status(f"[{C_BRONZE}]Tactical Rest ({duration:.1f}s)...[/]") as status:
        start_time = time.time()
        while True:
            elapsed = time.time() - start_time
            remaining = duration - elapsed
            if remaining <= 0: break
            time.sleep(min(5, remaining))
            driver = check_and_reconnect(driver)
            status.update(f"[{C_BRONZE}]Heartbeat Active (+) Remaining: {remaining:.1f}s[/]")
    return driver

# ==========================================
# 📥 辅助下载逻辑
# ==========================================
def get_session_cookies(driver):
    session = requests.Session()
    session.headers.update(HEADERS)
    for cookie in driver.get_cookies(): session.cookies.set(cookie['name'], cookie['value'])
    return session

def get_safe_dirname(title):
    clean = re.sub(r'[\\/*?:"<>|]', "", title).strip()
    return clean[:100]

def get_smart_filename(url):
    parsed = urlparse(url)
    path = parsed.path
    query = parse_qs(parsed.query)
    
    base_name = os.path.basename(path)
    
    if not base_name or base_name in ['640', '0', '']:
        base_name = hashlib.md5(url.encode('utf-8')).hexdigest()[:12]
        
    ext = os.path.splitext(base_name)[1]
    if not ext:
        if 'wx_fmt' in query: ext = f".{query['wx_fmt'][0]}"
        elif 'fmt' in query: ext = f".{query['fmt'][0]}"
        else: ext = ".jpg"
        base_name += ext

    return unquote(base_name)

def write_metadata(filepath, tags_list):
    if not tags_list: return
    try:
        ext = os.path.splitext(filepath)[1].lower()
        tags_str = ", ".join(tags_list)
        if ext in ['.jpg', '.jpeg', '.webp']:
            exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
            try: exif_dict = piexif.load(filepath)
            except: pass
            exif_dict["0th"][piexif.ImageIFD.XPKeywords] = tags_str.encode('utf-16le')
            piexif.insert(piexif.dump(exif_dict), filepath)
    except: pass

def get_high_res_url(img_url):
    pattern = re.compile(r'-\d{3,4}x\d{3,4}(\.\w+)$')
    return pattern.sub(r'\1', img_url), img_url

# ==========================================
# 📥 Worker A：直接下载器 (用于单页瀑布流)
# ==========================================
def direct_download_worker(args):
    media_url, save_dir, session, referer, clean_title = args
    time.sleep(random.uniform(CONFIG["DELAY_MIN"], CONFIG["DELAY_MAX"]))
    
    fname = get_smart_filename(media_url)
    fpath = os.path.join(save_dir, fname)
    
    if os.path.exists(fpath):
        return {"status": "skip", "msg": "已存在", "file": fname}
        
    req_headers = HEADERS.copy()
    req_headers['Referer'] = referer
    
    try:
        resp = session.get(media_url, headers=req_headers, timeout=15)
        if resp.status_code == 200:
            if len(resp.content) > CONFIG["MIN_IMAGE_SIZE_KB"] * 1024:
                with open(fpath, 'wb') as f: f.write(resp.content)
                write_metadata(fpath, [clean_title])
                return {"status": "success", "msg": "下载成功", "file": fname}
            else:
                return {"status": "skip", "msg": "图片过小", "file": fname}
        else:
            return {"status": "error", "msg": f"HTTP {resp.status_code}", "file": fname}
    except Exception as e:
        return {"status": "error", "msg": str(e)[:15], "file": fname}

# ==========================================
# 📥 Worker B：画廊下载器 (用于Rule34等)
# ==========================================
def gallery_download_worker(args):
    post_url, save_dir, session = args
    time.sleep(random.uniform(CONFIG["DELAY_MIN"], CONFIG["DELAY_MAX"]))
    result = {"status": "fail", "msg": "", "file": "Unknown"}

    try:
        resp = session.get(post_url, timeout=CONFIG["TIMEOUT"])
        if resp.status_code == 429:
            result["msg"] = "RATE LIMIT (429)"
            return result
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        page_title = soup.title.string.strip() if soup.title else "Untitled"
        clean_title = get_safe_dirname(page_title)
        current_save_dir = os.path.join(save_dir, clean_title)
        if not os.path.exists(current_save_dir): os.makedirs(current_save_dir)

        media_candidates = set()
        orig_link = soup.find('li', class_='linktype-original') 
        if orig_link: media_candidates.add(orig_link.find('a').get('href'))
        for img in soup.find_all('img'):
            if img.get('srcset'):
                try: media_candidates.add(img.get('srcset').split(',')[-1].strip().split(' ')[0])
                except: pass
            src = img.get('src') or img.get('data-src')
            if src: media_candidates.add(src)
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.lower().endswith(('.jpg', '.jpeg', '.png', '.webp') + CONFIG["VIDEO_EXTS"]):
                if 'avatar' not in href and 'logo' not in href: media_candidates.add(href)
        for v in soup.find_all('video'):
            if v.get('src'): media_candidates.add(v.get('src'))
            for s in v.find_all('source'):
                if s.get('src'): media_candidates.add(s.get('src'))

        if not media_candidates:
            result["msg"] = "NO ASSETS"
            return result

        success_count = 0
        for media_url in media_candidates:
            if not media_url: continue
            media_url = urljoin(post_url, media_url)
            if any(x in media_url.lower() for x in ['.svg', 'avatar', 'logo', 'icon']): continue

            fname = get_smart_filename(media_url)
            fpath = os.path.join(current_save_dir, fname)
            if os.path.exists(fpath): continue

            try:
                req_headers = HEADERS.copy()
                req_headers['Referer'] = post_url
                img_resp = session.get(media_url, headers=req_headers, timeout=15)
                
                if img_resp.status_code == 200:
                    if len(img_resp.content) > CONFIG["MIN_IMAGE_SIZE_KB"] * 1024:
                        with open(fpath, 'wb') as f: f.write(img_resp.content)
                        write_metadata(fpath, [clean_title])
                        success_count += 1
            except: pass

        if success_count > 0:
            result["status"] = "success"
            result["msg"] = f"{success_count} Files"
            result["file"] = clean_title
        else:
            result["msg"] = "FILTERED/FAILED"

    except Exception as e:
        result["msg"] = f"ERR: {str(e)[:10]}"
    return result

# ==========================================
# 🚀 主循环
# ==========================================
def main():
    GalaxyUI.header()
    driver = connect_to_chrome()
    GalaxyUI.strategy_menu()
    
    console.print(f"\n[{C_GOLD}]⚡ 准备就绪[/]")
    if CONFIG["MODE"] == "SINGLE":
        console.print(f"[{C_BRONZE}]请在浏览器打开【微信公众号文章】或【长图网页】。[/]")
    else:
        console.print(f"[{C_BRONZE}]请在浏览器打开【图站/画廊的列表页】。[/]")
    
    Prompt.ask(f"[{C_GOLD}]按回车键开始收割 >[/]")

    session = get_session_cookies(driver)
    current_url = driver.current_url
    
    try: page_title = driver.title.strip() or f"Task_{int(time.time())}"
    except: page_title = f"Task_{int(time.time())}"

    safe_folder_name = get_safe_dirname(page_title)
    save_dir = os.path.join(CONFIG["BASE_SAVE_FOLDER"], safe_folder_name)
    if not os.path.exists(save_dir): os.makedirs(save_dir)
    GalaxyUI.log("ARCHIVE", f"档案库已锁定: [underline]{safe_folder_name}[/]", "success")

    # ==========================================
    # 分支 A：单页瀑布流模式
    # ==========================================
    if CONFIG["MODE"] == "SINGLE":
        GalaxyUI.log("SCROLL", "正在自动向下滚动，加载隐藏图片...", "warn")
        for i in range(1, 11):
            driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * ({i}/10));")
            time.sleep(0.8)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        img_urls = set()
        
        for img in soup.find_all('img'):
            src = img.get('data-src') or img.get('src') or img.get('data-original')
            if src: img_urls.add(src)
            
        total_imgs = len(img_urls)
        GalaxyUI.log("SCAN", f"捕获页面内 {total_imgs} 张图片。", "info")
        
        if total_imgs == 0: return

        with Progress(SpinnerColumn(style=C_GOLD), TextColumn("[bold gold1]{task.description}"), BarColumn(complete_style=C_GOLD, finished_style=C_SUCCESS), console=console) as progress:
            task_id = progress.add_task("Downloading...", total=total_imgs)
            with ThreadPoolExecutor(max_workers=CONFIG["MAX_WORKERS"]) as executor:
                futures = [executor.submit(direct_download_worker, (url, save_dir, session, current_url, safe_folder_name)) for url in img_urls]
                for future in as_completed(futures):
                    res = future.result()
                    progress.advance(task_id)
                    if res["status"] == "success": GalaxyUI.log("OK", f"{res['file']}", "success")
                    elif res["status"] == "skip": GalaxyUI.log("SKIP", f"{res['file']} ({res['msg']})", "skip")
                    else: GalaxyUI.log("FAIL", f"{res['file']} ({res['msg']})", "error")
        
        GalaxyUI.log("END", "单页收割完毕！", "success")

    # ==========================================
    # 分支 B：画廊翻页模式
    # ==========================================
    else:
        page_count = 1
        while True:
            driver = check_and_reconnect(driver)
            console.rule(f"[{C_GOLD}] Scanning Sector {page_count} [/]")
            
            try:
                scroll_page(driver)
                links = driver.find_elements(By.CSS_SELECTOR, "span.thumb a, article.thumbnail-preview a, .post-preview a")
                if not links:
                    links = driver.find_elements(By.XPATH, "//a[descendant::img]")
            except:
                driver = check_and_reconnect(driver); links = []

            post_urls = []
            current_host = urlparse(driver.current_url).netloc
            for l in links:
                try:
                    href = l.get_attribute('href')
                    if href and current_host in href and not any(x in href for x in ['login', 'javascript']):
                        if href not in post_urls: post_urls.append(href)
                except: pass
            
            if not post_urls:
                GalaxyUI.log("SCAN", "No targets found. End of gallery.", "warn")
                break
            
            total_imgs = len(post_urls)
            GalaxyUI.log("LOCK", f"Acquired {total_imgs} Targets. Engaging...", "info")
            
            with Progress(SpinnerColumn(style=C_GOLD), TextColumn("[bold gold1]{task.description}"), BarColumn(complete_style=C_GOLD, finished_style=C_SUCCESS), console=console) as progress:
                task_id = progress.add_task("Downloading...", total=total_imgs)
                with ThreadPoolExecutor(max_workers=CONFIG["MAX_WORKERS"]) as executor:
                    futures = [executor.submit(gallery_download_worker, (url, save_dir, session)) for url in post_urls]
                    for future in as_completed(futures):
                        res = future.result()
                        progress.advance(task_id)
                        if res["status"] == "success": GalaxyUI.log("OK", f"{res['file']} ({res['msg']})", "success")
                        elif res["status"] == "skip": GalaxyUI.log("SKIP", f"{res['file']}", "skip")
                        else: GalaxyUI.log("FAIL", f"{res['msg']}", "error")

            rest_time = random.uniform(CONFIG["PAGE_REST_MIN"], CONFIG["PAGE_REST_MAX"])
            driver = smart_sleep(driver, rest_time)
            
            try:
                next_btns = driver.find_elements(By.XPATH, "//a[contains(text(), 'Next')] | //a[contains(text(), 'next')] | //a[contains(text(), '>')] | //a[@rel='next'] | //a[contains(@class, 'next')]")
                target_btn = None
                if next_btns:
                    for btn in next_btns:
                        if btn.is_displayed() and not any(x in btn.text.strip() for x in ['>>', '»', 'Last']):
                            target_btn = btn; break
                
                if target_btn:
                    GalaxyUI.log("NAV", "Jumping to next sector...", "info")
                    old_url = driver.current_url
                    driver.execute_script("arguments[0].click();", target_btn)
                    try: WebDriverWait(driver, 15).until(lambda d: d.current_url != old_url)
                    except: pass
                    page_count += 1
                else:
                    GalaxyUI.log("END", "Mission Accomplished.", "success")
                    break
            except: driver = check_and_reconnect(driver)

    console.print(f"\n[{C_GOLD}]═════════ MISSION REPORT ═════════[/]")
    console.print(f"[{C_BRONZE}]Archive Location: {os.path.abspath(save_dir)}[/]")
    Prompt.ask(f"[{C_GOLD}]Press Enter to Exit[/]")

if __name__ == "__main__":
    main()
