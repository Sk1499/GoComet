# -*- coding: utf-8 -*-
"""
Created on Sat May 28 20:04:39 2022

@author: shresht
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import os
import time

def flipkart_driver(search_term,num_prod=10,sort_by="1",price_min=0,price_max=-1,pin_code="400072"):
    print('~Initializing Flipkart Driver~')
    chrome_options = Options()             # Adding to bypass various bot detection techniques
    
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    
    chrome_prefs["profile.default_content_settings"] = { "popups": 1 }
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--disable-dev-shm-usage') 
    chrome_options.add_argument("window-size=1280, 800")
    #chrome_options.add_argument('start-maximized')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
    
    driver = webdriver.Chrome(options=chrome_options) # Might need to add path to chromedriver
    driver.set_window_size(1463, 792)
    driver.set_window_position(0, 0, windowHandle='current')
    
    
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
      "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })
    
    driver.get("https://www.flipkart.com/")                                      
    time.sleep(3)
    close_login = driver.find_element(By.XPATH,"/html/body/div[2]/div/div/button").click()
    time.sleep(3)
    search_bar = driver.find_element(By.XPATH,'//*[@id="container"]/div/div[1]/div[1]/div[2]/div[2]/form/div/div/input')
    search_bar.click()
    time.sleep(2)
    search_bar.send_keys(search_term)
    time.sleep(2)
    search_bar.send_keys(Keys.ENTER)
    print("~ Searching ~ ")
    time.sleep(3)
    
    if sort_by == "1":
        print("~ Sorting by Relevance ~")
        pass
    elif sort_by == "2":
        driver.find_element(By.XPATH,"//div[@class='_5THWM1']/div[contains(text(),'Popularity')]").click()
        print("~ Sort by Popularity ~")
    elif sort_by == "3":
        driver.find_element(By.XPATH,"//div[@class='_5THWM1']/div[contains(text(),'Price -- Low to High')]").click()
        print("~ Sort by Price- Low to High ~")
    elif sort_by == "4":
        driver.find_element(By.XPATH,"//div[@class='_5THWM1']/div[contains(text(),'Price -- High to Low')]").click()
        print("~ Sort by Price- High to Low ~")
    elif sort_by == "4":
        driver.find_element(By.XPATH,"//div[@class='_5THWM1']/div[contains(text(),'Newest First')]").click()
        print("~ Sort by Newest First ~")
    time.sleep(3)
    
    
    if price_max != -1:
        text = driver.find_element(By.XPATH,"//div[@class='_2b0bUo']/div[3]").text
        price_ranges = text.replace("₹","")
        price_ranges = price_ranges.replace("+","")
        price_ranges = price_ranges.splitlines()
        price_ranges = [int(x) for x in price_ranges]
        if price_max in price_ranges:
            pass
        else:
            price_max = min(price_ranges, key=lambda x:abs(x-price_max))
        try:
            select_max = Select(driver.find_element(By.XPATH,"//div[@class='_2b0bUo']/div[3]/select"))
            select_max.select_by_visible_text("₹" +str(price_max))
        except:
            select_max = Select(driver.find_element(By.XPATH,"//div[@class='_2b0bUo']/div[3]/select"))
            select_max.select_by_visible_text("₹" +str(price_max) + "+")
        print("~ Changed max price ~")
    time.sleep(3)
    if price_min != 0:
        if price_min in price_ranges:
            pass
        else:
            price_min = min(price_ranges, key=lambda x:abs(x-price_min))
        try:
            select_min = Select(driver.find_element(By.XPATH,"//div[@class='_2b0bUo']/div[1]/select"))
            select_min.select_by_visible_text("₹" + str(price_min))
        except:
            select_min = Select(driver.find_element(By.XPATH,"//div[@class='_2b0bUo']/div[1]/select"))
            select_min.select_by_visible_text("₹" + str(price_min)+ "+")
        print("~ Changed min price ~")
    time.sleep(3)
    prod_count = 0
    prod_name = []
    prod_link= []
    source = []
    price = []
    category = []
    model_number = []
    nav = driver.find_element(By.XPATH,"//nav[@class='yFHi8N']")
    nav_a = nav.find_elements(By.TAG_NAME,'a')
    page = 0
    zips = 0
    while prod_count < num_prod:                         
        main_div = driver.find_element(By.XPATH,"//div[@class='_1YokD2 _3Mn1Gg']")
        prod_containers = main_div.find_elements(By.TAG_NAME,"a")
        for container in prod_containers:
            if prod_count == num_prod:
                break
            attr = container.get_attribute('class')
            if attr != '_1fQZEK':
                continue
            else:
                # link = container.find_element(By.TAG_NAME,"a")
                # link.click()
                container.click()
                prod_link.append(container.get_attribute('href'))
                
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(3)
                
                name = driver.find_element(By.XPATH,"//*[@class='B_NuCI']").text
                prod_name.append(name)
                
                source.append("Flipkart")
                
                if zips == 0:
                    pincode = driver.find_element(By.XPATH,"//input[@class='_36yFo0']")
                    pincode.click()
                    pincode.send_keys(Keys.CONTROL,'a')
                    time.sleep(1)
                    pincode.send_keys(Keys.DELETE)
                    pincode.send_keys(pin_code)
                    time.sleep(0.5)
                    element = driver.find_element(By.XPATH,"//div[@class='_3Oikkn _3_ezix _3Hbb-8']")
                    driver.execute_script("arguments[0].click();", element)
                    time.sleep(3)
                    zips = zips +1
                
                cost = driver.find_element(By.XPATH,"//div[@class='_30jeq3 _16Jk6d']").text
                price.append(cost)
                
                cat = driver.find_element(By.XPATH,"//td[contains(text(),'Browse Type')]/following-sibling::td").text
                category.append(cat)
                
                mod = driver.find_element(By.XPATH,"//td[contains(text(),'Model Number')]/following-sibling::td").text
                model_number.append(mod)
                
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                prod_count = prod_count +1
        page = page + 1
        nav_a[page].click()
        time.sleep(5)
            
        
    
    time.sleep(5)
    driver.quit()
    print('~ Flipkart Driver complete ~')
    return prod_name,prod_link,source,price,category,model_number,