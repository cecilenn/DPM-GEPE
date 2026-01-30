import os
import sys
import subprocess
import time

def install_package(package_name):
    """调用 pip 安装指定包"""
    print(f"📦 正在安装: {package_name} ...")
    try:
        # 使用 sys.executable 确保安装到当前 Python 环境
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"✅ {package_name} 安装成功！")
    except subprocess.CalledProcessError:
        print(f"❌ {package_name} 安装失败！请检查网络或权限。")
        return False
    return True

def main():
    # 强制设置控制台编码
    if os.name == 'nt':
        os.system('chcp 65001 >nul')
        
    print("\n  ╔══════════════════════════════════════╗")
    print("  ║   Galaxy Reaper 环境自动部署工具     ║")
    print("  ╚══════════════════════════════════════╝\n")

    # 核心依赖列表 (正确的 PyPI 包名)
    requirements = [
        "requests",
        "beautifulsoup4",  # 修正：不能写 bs4
        "selenium",
        "webdriver-manager",
        "yt-dlp",
        "rich",
        "Pillow",          # 修正：不能写 PIL
        "piexif"
    ]

    print(f"即将安装 {len(requirements)} 个核心组件...\n")
    
    success_count = 0
    for req in requirements:
        if install_package(req):
            success_count += 1
            
    print("-" * 40)
    if success_count == len(requirements):
        print("\n🎉 环境部署完美完成！")
        print("👉 现在可以直接运行 dpm.py 了。")
    else:
        print(f"\n⚠️ 部署完成，但有 {len(requirements) - success_count} 个组件安装失败。")
        print("请尝试手动运行: pip install -r requirements.txt")
        
    input("\n按回车键退出...")

if __name__ == "__main__":
    main()
