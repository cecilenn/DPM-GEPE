import os
import sys
import time
import re
import random
import subprocess
import socket
import shutil
import importlib.util
from datetime import datetime
from urllib.parse import urlparse, unquote, urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed

# === ✅ 自动环境配置 & 依赖检测 ===
if os.name == 'nt':
    try:
        os.system('chcp 65001 >nul')
        os.system('mode con: cols=120 lines=40')
    except: pass

def check_requirements():
    """自动检测并安装缺失的库 (已修复 PIL/Pillow 问题)"""
    required = {
        'rich': 'rich', 
        'yt-dlp': 'yt_dlp', 
        'selenium': 'selenium', 
        'beautifulsoup4': 'bs4',
        'piexif': 'piexif',
        'Pillow': 'PIL',
        'webdriver-manager': 'webdriver_manager'
    }
    
    missing = []
    for pkg, imp in required.items():
        if importlib.util.find_spec(imp) is None:
            missing.append(pkg)

    if missing:
        print(f"系统初始化: 正在部署核心组件 [{', '.join(missing)}]...")
        for pkg in missing: 
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
            except subprocess.CalledProcessError:
                sys.exit(1)
        print("系统就绪。启动中...")
        time.sleep(1)

check_requirements()

# --- 核心库导入 ---
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
# 🎨 视觉风格定义 (The Royal Palette)
# ==========================================
C_GOLD = "#D4AF37"      # 帝王金
C_BG = "#080808"        # 深空黑
C_ACCENT = "#F4E29E"    # 象牙白
C_BRONZE = "#8C7853"    # 古铜色
C_ERROR = "#FF4500"     # 警示红
C_SUCCESS = "#00FF7F"   # 荧光绿
C_INFO = "#00BFFF"      # 科技蓝

console = Console(style=f"{C_ACCENT} on {C_BG}", width=118)

# ==========================================
# ⚙️ 核心配置 (CONFIG)
# ==========================================
CONFIG = {
    "BASE_SAVE_FOLDER": "Galaxy_Reaper_Archive",
    "DEBUG_PORT": 9222,
    "DEBUG_HOST": "127.0.0.1",
    
    # 默认参数 (会被启动菜单覆盖)
    "MAX_WORKERS": 1,           
    "TIMEOUT": 25,              
    "DELAY_MIN": 1.5,
    "DELAY_MAX": 3.0,
    "PAGE_REST_MIN": 5.0,
    "PAGE_REST_MAX": 10.0,
    
    "MIN_IMAGE_SIZE_KB": 30,
    "USER_DATA_DIR_NAME": "Chrome_Crawler_Profile",
    "VIDEO_EXTS": ('.mp4', '.mov', '.webm', '.mkv', '.avi', '.m4v')
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# ==========================================
# 🎩 UI 呈现层 (修正版：纯文本徽章)
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
        subtitle = "R E A P E R   P R O T O C O L   v 1 6 . 2"
        
        info_text = Text()
        info_text.append(title_art, style=f"bold {C_GOLD}")
        info_text.append(f"\n{subtitle.center(56)}", style=f"bold {C_ACCENT}")
        
        panel = Panel(
            info_text,
            box=DOUBLE,
            border_style=C_GOLD,
            padding=(1, 2),
            title=f"[{C_BRONZE}] EST. 2026 [/]",
            subtitle=f"[{C_BRONZE}] OMNI-COLLECTOR EDITION [/]"
        )
        console.print(panel)

    @staticmethod
    def strategy_menu():
        """战术选择菜单 (修正图标)"""
        console.print(f"\n[{C_GOLD}]:: TACTICAL SELECTION :: (战术选择)[/]")
        
        table = Table(box=HEAVY_EDGE, border_style=C_BRONZE, show_header=True, header_style=f"bold {C_BG} on {C_GOLD}", expand=True)
        table.add_column("ID", justify="center", width=6, style=f"bold {C_GOLD}")
        table.add_column("MODE", style=f"bold {C_ACCENT}", width=15)
        table.add_column("DETAILS", style=f"{C_BRONZE}")

        table.add_row("1", "极速收割", "并发: 5 | 延迟: 0s | 适合: 普通画廊/建筑网")
        # ✨ 修改：更新文案，反映新的极慢速度
        table.add_row("2", "潜行防封", "并发: 1 | 延迟: 10-20s | 翻页: 1-2分钟 (超安全)")
        table.add_row("3", "手动调校", "自定义所有参数")
        
        console.print(table)
        
        choice = Prompt.ask(f"[{C_GOLD}]Command >[/]", choices=["1", "2", "3"], default="2")
        
        if choice == '1':
            CONFIG["MAX_WORKERS"] = 5
            CONFIG["DELAY_MIN"] = 0.1
            CONFIG["DELAY_MAX"] = 0.5
            CONFIG["PAGE_REST_MIN"] = 2.0
            CONFIG["PAGE_REST_MAX"] = 4.0
            GalaxyUI.log("SYS", "极速模式已装载。引擎全开。", "warn")
            
        elif choice == '2':
            # ✨ 修改：应用用户要求的超慢参数
            CONFIG["MAX_WORKERS"] = 1
            CONFIG["DELAY_MIN"] = 10.0
            CONFIG["DELAY_MAX"] = 20.0
            CONFIG["PAGE_REST_MIN"] = 60.0
            CONFIG["PAGE_REST_MAX"] = 120.0
            GalaxyUI.log("SYS", "潜行模式已激活。慢速隐蔽运行。", "success")
            
        elif choice == '3':
            CONFIG["MAX_WORKERS"] = IntPrompt.ask(f"[{C_BRONZE}]并发数[/]", default=2)
            CONFIG["DELAY_MIN"] = FloatPrompt.ask(f"[{C_BRONZE}]最小延迟(s)[/]", default=1.5)
            CONFIG["DELAY_MAX"] = FloatPrompt.ask(f"[{C_BRONZE}]最大延迟(s)[/]", default=3.0)
            CONFIG["PAGE_REST_MIN"] = FloatPrompt.ask(f"[{C_BRONZE}]翻页最小休息(s)[/]", default=10.0)
            CONFIG["PAGE_REST_MAX"] = FloatPrompt.ask(f"[{C_BRONZE}]翻页最大休息(s)[/]", default=20.0)
            GalaxyUI.log("SYS", "自定义参数已应用。", "info")

    @staticmethod
    def log(tag, message, level="info"):
        """日志系统 (修正：使用纯文本徽章代替 Emoji，防止乱码)"""
        time_str = datetime.now().strftime("%H:%M:%S")
        if level == "success":
            color, badge = C_SUCCESS, "[OK]"
        elif level == "error":
            color, badge = C_ERROR, "[!!]"
        elif level == "warn":
            color, badge = C_GOLD, "[WARN]"
        elif level == "skip":
            color, badge = C_BRONZE, "[SKIP]"
        else:
            color, badge = C_INFO, "[INFO]"
            
        # 使用对齐的格式
        console.print(f"[{C_BRONZE}]{time_str}[/] [{color} bold]{badge:<6}[/] [{C_GOLD}]{tag:<8}[/] {message}")

# ==========================================
# 🛠️ 浏览器控制层
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
    try:
        s.settimeout(1)
        s.connect((host, port))
        s.close()
        return True
    except: return False

def ensure_chrome_debugger():
    if is_port_open(CONFIG["DEBUG_HOST"], CONFIG["DEBUG_PORT"]):
        GalaxyUI.log("LINK", "Browser Connected.", "success")
        return

    GalaxyUI.log("INIT", "Launching Chrome...", "info")
    chrome_path = find_chrome_path()
    if not chrome_path:
        GalaxyUI.log("FATAL", "Chrome Not Found!", "error")
        sys.exit(1)

    user_data_dir = os.path.expandvars(fr"%USERPROFILE%\{CONFIG['USER_DATA_DIR_NAME']}")
    if not os.path.exists(user_data_dir): os.makedirs(user_data_dir)

    cmd = [chrome_path, f"--remote-debugging-port={CONFIG['DEBUG_PORT']}", f"--user-data-dir={user_data_dir}"]
    try: subprocess.Popen(cmd)
    except Exception as e:
        GalaxyUI.log("FATAL", f"Launch Failed: {e}", "error")
        sys.exit(1)

    with console.status(f"[{C_GOLD}]Waiting for port {CONFIG['DEBUG_PORT']}...[/]"):
        for i in range(10):
            if is_port_open(CONFIG["DEBUG_HOST"], CONFIG["DEBUG_PORT"]): return
            time.sleep(1)
    sys.exit(1)

def connect_to_chrome():
    ensure_chrome_debugger()
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", f"{CONFIG['DEBUG_HOST']}:{CONFIG['DEBUG_PORT']}")
    try:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        GalaxyUI.log("FATAL", f"Connection Error: {e}", "error")
        sys.exit(1)

def check_and_reconnect(driver):
    try:
        _ = driver.window_handles
        return driver
    except (InvalidSessionIdException, WebDriverException):
        GalaxyUI.log("WARN", "Signal Lost. Re-establishing...", "warn")
        try: return connect_to_chrome()
        except: sys.exit(1)

def smart_sleep(driver, duration):
    """带心跳的睡眠"""
    # 修正图标为心形符号或简单的 (+)
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
# 📥 核心下载逻辑
# ==========================================
def get_session_cookies(driver):
    selenium_cookies = driver.get_cookies()
    session = requests.Session()
    session.headers.update(HEADERS)
    adapter = requests.adapters.HTTPAdapter(max_retries=3)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    for cookie in selenium_cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    return session

def scroll_page(driver):
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, 0);") 
    except: pass

def get_safe_dirname(title):
    clean = re.sub(r'[\\/*?:"<>|]', "", title).strip()
    return clean[:100]

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
        elif ext == '.png':
            target_image = Image.open(filepath)
            metadata = PngImagePlugin.PngInfo()
            metadata.add_text("parameters", tags_str)
            target_image.save(filepath, pnginfo=metadata)
            target_image.close()
    except: pass

def get_high_res_url(img_url):
    pattern = re.compile(r'-\d{3,4}x\d{3,4}(\.\w+)$')
    original_url = pattern.sub(r'\1', img_url)
    return original_url, img_url

def download_worker(args):
    post_url, save_dir, session = args
    time.sleep(random.uniform(CONFIG["DELAY_MIN"], CONFIG["DELAY_MAX"]))
    result = {"status": "fail", "msg": "", "file": "Unknown"}

    try:
        resp = session.get(post_url, timeout=CONFIG["TIMEOUT"])
        if resp.status_code == 429:
            result["msg"] = "RATE LIMIT (429)"
            return result
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # --- 智能归档文件夹 ---
        page_title = "Untitled"
        if soup.title and soup.title.string:
            page_title = soup.title.string.strip()
        else:
            path_segs = urlparse(post_url).path.strip('/').split('/')
            if path_segs: page_title = path_segs[-1]

        clean_title = get_safe_dirname(page_title)
        current_save_dir = os.path.join(save_dir, clean_title)
        if not os.path.exists(current_save_dir): os.makedirs(current_save_dir)

        # --- 万能资源提取 ---
        media_candidates = set()

        # 1. Rule34/Booru Original
        orig_link = soup.find('li', class_='linktype-original') 
        if orig_link: media_candidates.add(orig_link.find('a').get('href'))
        
        # 2. Img tags
        for img in soup.find_all('img'):
            if img.get('srcset'):
                try: media_candidates.add(img.get('srcset').split(',')[-1].strip().split(' ')[0])
                except: pass
            src = img.get('src') or img.get('data-src')
            if src: media_candidates.add(src)

        # 3. Direct Links
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.lower().endswith(('.jpg', '.jpeg', '.png', '.webp') + CONFIG["VIDEO_EXTS"]):
                if 'avatar' not in href and 'logo' not in href: media_candidates.add(href)

        # 4. Video tags
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
            
            if any(x in media_url.lower() for x in ['.svg', 'avatar', 'logo', 'icon', 'button']): continue

            # A. 视频下载
            if media_url.lower().endswith(CONFIG["VIDEO_EXTS"]):
                try:
                    v_name = os.path.basename(urlparse(media_url).path)
                    ydl_opts = {
                        'outtmpl': os.path.join(current_save_dir, unquote(v_name)),
                        'quiet': True, 'no_warnings': True, 'nocheckcertificate': True
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([media_url])
                    success_count += 1
                    continue
                except: pass

            # B. 图片下载
            high_res_url, original_url = get_high_res_url(media_url)
            target_url = high_res_url
            fname = os.path.basename(urlparse(target_url).path)
            fpath = os.path.join(current_save_dir, unquote(fname))
            
            if os.path.exists(fpath): continue

            try:
                img_resp = session.get(target_url, timeout=15)
                if img_resp.status_code == 404 and target_url != original_url:
                    target_url = original_url
                    img_resp = session.get(target_url, timeout=15)
                
                if img_resp.status_code == 200:
                    content = img_resp.content
                    if len(content) > CONFIG["MIN_IMAGE_SIZE_KB"] * 1024:
                        with open(fpath, 'wb') as f: f.write(content)
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
    
    # 策略选择
    GalaxyUI.strategy_menu()
    
    console.print(f"\n[{C_GOLD}]⚡ READY TO ENGAGE[/]")
    console.print(f"[{C_BRONZE}]1. 请在浏览器打开画廊列表页[/]")
    console.print(f"[{C_BRONZE}]2. 按下回车键开始自动收割[/]")
    Prompt.ask("")

    session = get_session_cookies(driver)
    
    # 智能归档逻辑
    try:
        page_title = driver.title.strip()
        if not page_title: page_title = f"Task_{int(time.time())}"
    except: page_title = f"Task_{int(time.time())}"

    safe_folder_name = get_safe_dirname(page_title)
    save_dir = os.path.join(CONFIG["BASE_SAVE_FOLDER"], safe_folder_name)
    if not os.path.exists(save_dir): os.makedirs(save_dir)
    
    GalaxyUI.log("ARCHIVE", f"档案库已锁定: [underline]{safe_folder_name}[/]", "success")

    page_count = 1
    
    while True:
        driver = check_and_reconnect(driver)
        console.rule(f"[{C_GOLD}] Scanning Sector {page_count} [/]")
        
        try:
            scroll_page(driver)
            # 1. 尝试 Rule34/Booru 标准
            links = driver.find_elements(By.CSS_SELECTOR, "span.thumb a, article.thumbnail-preview a, .post-preview a")
            # 2. 万能模式
            if not links:
                GalaxyUI.log("MODE", "Switching to Universal Gallery Mode...", "warn")
                links = driver.find_elements(By.XPATH, "//a[descendant::img]")
        except:
            driver = check_and_reconnect(driver)
            links = []

        post_urls = []
        current_host = urlparse(driver.current_url).netloc
        
        for l in links:
            try:
                href = l.get_attribute('href')
                if not href: continue
                if any(x in href for x in ['javascript:', 'login', 'register', 'contact', 'mailto']): continue
                if current_host in href or href.endswith(('.html', '.php', '/')):
                    if href not in post_urls: post_urls.append(href)
            except: pass
        
        if not post_urls:
            GalaxyUI.log("SCAN", "No targets found. Retrying in 3s...", "warn")
            time.sleep(3)
            driver = check_and_reconnect(driver)
            if not post_urls:
                GalaxyUI.log("END", "Sector Clear. No more targets.", "success")
                break
        
        total_imgs = len(post_urls)
        GalaxyUI.log("LOCK", f"Acquired {total_imgs} Targets. Engaging...", "info")
        
        # 进度条模式
        with Progress(
            SpinnerColumn(style=C_GOLD),
            TextColumn("[bold gold1]{task.description}"),
            BarColumn(complete_style=C_GOLD, finished_style=C_SUCCESS),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        ) as progress:
            task_id = progress.add_task("Downloading...", total=total_imgs)
            
            with ThreadPoolExecutor(max_workers=CONFIG["MAX_WORKERS"]) as executor:
                futures = [executor.submit(download_worker, (url, save_dir, session)) for url in post_urls]
                
                for future in as_completed(futures):
                    res = future.result()
                    progress.advance(task_id)
                    
                    if res["status"] == "success":
                        GalaxyUI.log("OK", f"{res['file']} ({res['msg']})", "success")
                    elif res["status"] == "skip":
                        GalaxyUI.log("SKIP", f"{res['file']}", "skip")
                    else:
                        GalaxyUI.log("FAIL", f"{res['msg']}", "error")

        GalaxyUI.log("STATUS", f"Sector {page_count} Complete.", "success")

        # 智能休眠
        rest_time = random.uniform(CONFIG["PAGE_REST_MIN"], CONFIG["PAGE_REST_MAX"])
        driver = smart_sleep(driver, rest_time)
        
        # 自动翻页
        try:
            next_btns = driver.find_elements(By.XPATH, "//a[contains(text(), 'Next')] | //a[contains(text(), 'next')] | //a[contains(text(), '>')] | //a[@rel='next'] | //a[contains(@class, 'next')]")
            target_btn = None
            if next_btns:
                for btn in next_btns:
                    if not btn.is_displayed(): continue
                    txt = btn.text.strip()
                    if '>>' in txt or '»' in txt or 'Last' in txt: continue
                    target_btn = btn; break
            
            if target_btn:
                GalaxyUI.log("NAV", "Jumping to next sector...", "info")
                old_url = driver.current_url
                driver.execute_script("arguments[0].click();", target_btn)
                try: WebDriverWait(driver, 15).until(lambda d: d.current_url != old_url)
                except: pass
                page_count += 1
            else:
                GalaxyUI.log("END", "Mission Accomplished. All sectors cleared.", "success")
                break
        except:
            driver = check_and_reconnect(driver)
            
    console.print(f"\n[{C_GOLD}]═════════ MISSION REPORT ═════════[/]")
    console.print(f"[{C_BRONZE}]Archive Location: {os.path.abspath(save_dir)}[/]")
    Prompt.ask(f"[{C_GOLD}]Press Enter to Exit[/]")

if __name__ == "__main__":
    main()
