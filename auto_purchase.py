"""
自动抢购助手 v2.0
功能：自动登录、监控库存、一键下单
"""

import sys
import os
import time
from datetime import datetime

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


class AutoPurchaseBot:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.print_header()
    
    def print_header(self):
        """打印标题"""
        print("\n" + "=" * 70)
        print(" " * 20 + "🤖 自动抢购助手 v2.0")
        print("=" * 70 + "\n")
    
    def check_dependencies(self):
        """检查依赖"""
        print("🔍 检查运行环境...\n")
        
        if not SELENIUM_AVAILABLE:
            print("❌ 缺少 Selenium 库！")
            print("\n请运行：pip install -r requirements.txt\n")
            return False
        
        # 检查 Chrome
        try:
            service = Service(ChromeDriverManager().install())
            print("✓ Chrome 浏览器检测成功")
            print("✓ ChromeDriver 准备就绪\n")
            return True
        except Exception as e:
            print(f"❌ Chrome 浏览器未安装或版本不兼容")
            print(f"   错误信息: {str(e)}\n")
            print("请安装 Chrome 浏览器：https://www.google.com/chrome/\n")
            return False
    
    def init_browser(self):
        """初始化浏览器"""
        try:
            print("📦 正在启动浏览器...\n")
            
            options = webdriver.ChromeOptions()
            # options.add_argument('--headless')  # 无头模式（后台运行）
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, 10)
            
            print("✓ 浏览器启动成功！\n")
            return True
            
        except Exception as e:
            print(f"❌ 浏览器启动失败: {str(e)}\n")
            return False
    
    def login(self, url, username, password):
        """登录网站"""
        try:
            print(f"🔐 正在登录 {url}...\n")
            self.driver.get(url)
            
            # 等待用户手动登录（或自动填充）
            print("⏳ 请在浏览器中完成登录...")
            print("   登录成功后，按 Enter 继续...\n")
            input()
            
            print("✓ 登录确认完成\n")
            return True
            
        except Exception as e:
            print(f"❌ 登录失败: {str(e)}\n")
            return False
    
    def monitor_stock(self, product_url, check_interval=2):
        """监控库存"""
        try:
            print(f"👀 开始监控商品: {product_url}\n")
            self.driver.get(product_url)
            
            attempt = 0
            while True:
                attempt += 1
                current_time = datetime.now().strftime("%H:%M:%S")
                
                try:
                    # 查找"立即购买"或"加入购物车"按钮
                    buy_button = self.driver.find_element(By.CSS_SELECTOR, 
                        "button[class*='buy'], button[class*='purchase'], button[class*='cart']")
                    
                    if buy_button.is_enabled():
                        print(f"✓ [{current_time}] 第 {attempt} 次检查 - 商品有货！\n")
                        return True
                    else:
                        print(f"⏳ [{current_time}] 第 {attempt} 次检查 - 暂无库存", end='\r')
                
                except:
                    print(f"⏳ [{current_time}] 第 {attempt} 次检查 - 暂无库存", end='\r')
                
                time.sleep(check_interval)
                self.driver.refresh()
            
        except Exception as e:
            print(f"\n❌ 监控出错: {str(e)}\n")
            return False
    
    def purchase(self):
        """执行购买"""
        try:
            print("🛒 开始下单流程...\n")
            
            # 点击购买按钮
            buy_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 
                    "button[class*='buy'], button[class*='purchase']"))
            )
            buy_button.click()
            print("✓ 已点击购买按钮")
            
            time.sleep(1)
            
            # 点击结算按钮
            checkout_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 
                    "button[class*='checkout'], button[class*='settlement']"))
            )
            checkout_button.click()
            print("✓ 已点击结算按钮")
            
            time.sleep(1)
            
            # 点击提交订单
            submit_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 
                    "button[class*='submit'], button[class*='confirm']"))
            )
            submit_button.click()
            print("✓ 已提交订单\n")
            
            print("🎉 购买流程完成！请检查订单状态\n")
            return True
            
        except Exception as e:
            print(f"❌ 购买失败: {str(e)}\n")
            return False
    
    def run(self):
        """主运行流程"""
        try:
            # 1. 检查依赖
            if not self.check_dependencies():
                input("\n按 Enter 退出...")
                return
            
            # 2. 初始化浏览器
            if not self.init_browser():
                input("\n按 Enter 退出...")
                return
            
            # 3. 获取用户输入
            print("=" * 70)
            print("请输入抢购信息")
            print("=" * 70 + "\n")
            
            login_url = input("登录页面 URL: ").strip()
            if not login_url:
                login_url = "https://www.taobao.com"
            
            product_url = input("商品页面 URL: ").strip()
            if not product_url:
                print("❌ 商品 URL 不能为空！")
                return
            
            check_interval = input("检查间隔(秒，默认2): ").strip()
            check_interval = int(check_interval) if check_interval else 2
            
            print("\n")
            
            # 4. 登录
            if not self.login(login_url, "", ""):
                return
            
            # 5. 监控库存
            if not self.monitor_stock(product_url, check_interval):
                return
            
            # 6. 执行购买
            self.purchase()
            
            # 7. 保持浏览器打开
            print("=" * 70)
            print("任务完成！浏览器将保持打开状态")
            print("=" * 70 + "\n")
            input("按 Enter 关闭浏览器...")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  用户中断操作\n")
        
        except Exception as e:
            print(f"\n❌ 程序出错: {str(e)}\n")
        
        finally:
            if self.driver:
                self.driver.quit()
                print("✓ 浏览器已关闭\n")


def main():
    """主函数"""
    bot = AutoPurchaseBot()
    bot.run()


if __name__ == "__main__":
    main()
