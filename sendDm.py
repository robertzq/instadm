from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
import random

options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=C:\Users\admin\AppData\Local\Google\Chrome\User Data")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)

def send_dm(username, message):
    try:
        driver.get('https://www.instagram.com/direct/new/')
        time.sleep(2)
        
        # 改进的按钮定位逻辑
        try:
            # 主定位方案
            send_btn = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@role="button" and text()="Send message"]'))
            )
        except TimeoutException:
            # 备用定位方案
            send_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@role="button" and contains(., "Send message")]'))
            )
        
        # 添加点击动作链
        ActionChains(driver).move_to_element(send_btn).pause(0.5).click().perform()
        print("✅ 成功点击发送按钮")
        
       # 定位搜索框并输入（关键改进）
        search_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, 
                '//input[@autocomplete="off" and @placeholder="Search..."]'
            ))
        )
        # 模拟人类输入（防检测）
        ActionChains(driver).move_to_element(search_box).click().perform()
        for char in username:
            search_box.send_keys(char)
            time.sleep(0.15)  # 控制输入速度
        
        # 用户选择（新增延迟）
        time.sleep(2)
       # 修改用户选择部分的代码如下
        try:
            # 等待用户列表加载（新增显式等待）
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@role="dialog"]'))
            )

            # 精确匹配用户项（关键修改）
            user_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                    f'//div[contains(@class,"x1nhvcw1")]'
                    f'//span[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{username.lower()}")]'
                    f'/ancestor::div[contains(@class,"x9f619") and contains(@class,"xjbqb8w") and @role="button"]'
                ))
            )
            
            # 增强点击操作（新增滚动到视图和三次点击）
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user_element)
            ActionChains(driver)\
                .move_to_element(user_element)\
                .pause(0.3)\
                .click()\
                .pause(0.2)\
                .click()\
                .perform()
            print(f"✅ 精准选择用户：{username}")
            
        except Exception as e:
            print(f"❌ 用户选择失败：{str(e)}")
            driver.save_screenshot('user_selection_error.png')
            raise
        
        # 新增Chat按钮处理（关键代码）
        try:
            chat_xpath = '//div[@role="button" and ./div[text()="Chat"]]'  # 精确结构定位
            chat_btn = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, chat_xpath))
            )
            ActionChains(driver).move_to_element(chat_btn).click().perform()
            print("✅ 已激活消息输入框")
        except TimeoutException:
            print("ℹ️ 跳过Chat按钮（新版界面）")

        # 消息输入优化（新增完成检测）
        msg_box = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, 
                '//div[@role="textbox"][@aria-label="Message"]'
            ))
        )
        
        # 分段输入+发送确认
        for i, part in enumerate(message.split()):
            msg_box.send_keys(part + ' ')
            # 每3个词添加随机延迟（更自然）
            if i % 3 == 0:
                time.sleep(random.uniform(0.1, 0.3))
        
        # 最终发送
        msg_box.send_keys(Keys.ENTER)
        print("🔄 消息发送中...")
        
        # 显式等待发送成功标志
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, 
                '//div[contains(@class,"x1g8br2") and contains(.//text(), "Delivered")]'
            ))
        )
        print("✅ 消息确认已送达")
        
        time.sleep(2)  # 保持会话
        
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        driver.save_screenshot('error.png')
    finally:
        print('final')
        if driver.service.process:
            driver.quit()
        #driver.quit()

# 使用示例
send_dm("yqtwwjm", "自动化测试消息")