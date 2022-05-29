# -*- coding: utf-8 -*-
"""
Created on Sun May 29 13:55:26 2022

@author: shresht
"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import os
import time


def amazon_driver(search_term,num_prod=10,sort_by="1",price_min=0,price_max=-1,pin_code="400072"):
    print('~Initializing Amazon Driver~')
    chrome_options = Options()
    
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
    
    driver.get("https://www.amazon.in/")
    time.sleep(5)
    
    pincode_btn = driver.find_element(By.XPATH,"//div[@id='glow-ingress-block']")
    pincode_btn.click()
    time.sleep(3)
    inpt = driver.find_element(By.XPATH,"//input[@class='GLUX_Full_Width a-declarative']")
    inpt.click()
    inpt.send_keys(pin_code)
    driver.find_element(By.XPATH,"//span[@data-action='GLUXPostalUpdateAction']").click()
    print('~ Changed Zip code ~')
    time.sleep(3)
    
    search_bar = driver.find_element(By.XPATH,"//input[@name='field-keywords']")
    search_bar.click()
    search_bar.send_keys(search_term)
    search_bar.send_keys(Keys.ENTER)
    print("~ Searching ~ ")
    
    time.sleep(3)
    
    depart_div = driver.find_element(By.XPATH,"//div[@id='departments']")
    cat = depart_div.find_element(By.XPATH,"./ul/li[2]")
    categ = cat.text
    try:
        element =  cat.find_element(By.XPATH,"./span/a")
        element.click()
    except:
        driver.execute_script("arguments[0].click();", element)
    
    time.sleep(3)
    
    select_sort = Select(driver.find_element(By.XPATH,"//select[@class='a-native-dropdown a-declarative']"))
    
    if sort_by == "1":
        print("~ Sorting by Featured ~")
        pass
    elif sort_by == "2":
        select_sort.select_by_visible_text('Avg. Customer Review')
        print("~ Sort by Avg. Customer Review ~")
    elif sort_by == "3":
        select_sort.select_by_visible_text('Price: Low to High')
        print("~ Sort by Price- Low to High ~")
    elif sort_by == "4":
        select_sort.select_by_visible_text('Price: High to Low')
        print("~ Sort by Price- High to Low ~")
    elif sort_by == "4":
        select_sort.select_by_visible_text('Newest Arrivals')
        print("~ Sort by Newest Arrivals ~")
    time.sleep(3)
    
    if price_max != -1:
        pricemax_input = driver.find_element(By.XPATH,"//input[@id='high-price']")
        pricemax_input.click()
        pricemax_input.send_keys(str(price_max))
        print("~ Changed max price ~")
        time.sleep(0.5)
    time.sleep(3)
    if price_min != 0:
        pricemin_input = driver.find_element(By.XPATH,"//input[@id='low-price']")
        pricemin_input.click()
        pricemin_input.send_keys(str(price_min))
        print("~ Changed min price ~")
        time.sleep(0.5)
    try:
        driver.find_element(By.XPATH,"//span[@class='a-button a-spacing-top-mini a-button-base s-small-margin-left']").click()
    except:
        element = driver.find_element(By.XPATH,"//span[@class='a-button a-spacing-top-mini a-button-base s-small-margin-left']")
        driver.execute_script("arguments[0].click();", element)
    time.sleep(3)
    
    names = []
    prices = []
    links = []
    model = []
    source = []
    category = []
    prod_count = 0
    while prod_count < num_prod:  
        main_div = driver.find_element(By.XPATH,'//div[@class="s-main-slot s-result-list s-search-results sg-row"]')
        
        prod_containers = main_div.find_elements(By.TAG_NAME,"div")
        
        for container in prod_containers:
            if prod_count == num_prod:
                break
            attr = container.get_attribute('class')
            if attr != 's-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16':
                continue
            else:
                a_tags = container.find_elements(By.TAG_NAME,'a')
                for k in a_tags:
                    if k.get_attribute('class') != 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal':
                        continue
                    else:
                        source.append('Amazon')
                        category.append(categ)
                        link = k.get_attribute('href')
                        links.append(link)
                        k.click()
                        
                        driver.switch_to.window(driver.window_handles[1])
                        time.sleep(3)
                        
                        name = driver.find_element(By.XPATH,"//span[@id='productTitle']").text
                        names.append(name)
                        
                        time.sleep(3)
                        try:
                            price = driver.find_element(By.XPATH,"//div[@class='a-section a-spacing-none aok-align-center']/span[2]/span[2]/span[2]").text
                            prices.append(price)
                        except:
                            try:
                                price = driver.find_element(By.XPATH,"//span[@class='a-price a-text-price a-size-medium apexPriceToPay']").text
                                price = price.splitlines()
                                prices.append(price[0])
                            except:
                                try:
                                    price = driver.find_element(By.XPATH,"//span[@class='a-size-base a-color-price']").text
                                    prices.append(price)
                                except:
                                    prices.append('-')
                        try:
                            see_more = driver.find_element(By.XPATH,"//a[@id='seeMoreDetailsLink']")
                            see_more.click()
                            time.sleep(3)
                        except:
                            try:
                                desc = driver.find_element(By.XPATH,"//div[@class='productDetails_feature_div']")
                                actions = ActionChains(driver)
                                actions.move_to_element(element).perform()
                            except:
                                pass

                        
                        try:
                            mod = driver.find_element(By.XPATH,"//th[contains(text(),' Item model number ')]/following-sibling::td").text
                            model.append(mod)
                        except:
                            model.append("-")
                        
                        
                        driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    prod_count = prod_count +1
        try:
            next_page = driver.find_element(By.LINK_TEXT,'Next')
            next_page.click()
            time.sleep(5)
        except:
            print("No next button")
            break
    time.sleep(5)
    driver.quit()
    print('~ Amazon Driver complete ~')
    return names,links,source,prices,category,model