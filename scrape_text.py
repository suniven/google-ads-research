import os
import re
from selenium import webdriver
import datetime
import sys
import pandas as pd
import time
from bs4 import BeautifulSoup
import lxml


def visit(browser, url):
    # visit url
    try:
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        browser.get(url)
    except:
        with open('./log.txt', 'a', encoding="utf-8") as f:
            f.write("Failed to visit: " + url + '\n')
        return None
    try:
        timeout = time.time() + 10  # 10 seconds from now
        while time.time() <= timeout:
            try:
                loadingState = browser.execute_script("return document.readyState")
            except:
                loadingState = ''
            if loadingState == 'loading':
                time.sleep(1)
            elif loadingState == 'interactive' or loadingState == 'complete' or time.time() > timeout:
                break
    except:
        with open('./log.txt', 'a', encoding="utf-8") as f:
            f.write("Failed to visit: " + url + '\n')
        return None
    try:
        # # text
        # bs = BeautifulSoup(browser.page_source, "lxml")
        # text = bs.get_text()
        # return text
        return browser.page_source
    except Exception as error:
        with open('./log.txt', 'a', encoding="utf-8") as f:
            f.write("Failed to get text: " + url + '\n')
        return None


def main():
    # headless模式
    option = webdriver.ChromeOptions()
    # option.add_argument('--headless')
    option.add_argument("--window-size=1920,1080")
    browser = webdriver.Chrome(chrome_options=option)
    browser.implicitly_wait(15)
    df = pd.DataFrame(columns=['domain', 'text'])
    try:
        with open('./domain_list.txt', 'r', encoding='utf-8') as f:
            domain_list = f.readlines()
        domain_list = [x.strip() for x in domain_list]
        for index, domain in enumerate(domain_list):
            try:
                print("Index_{0}: {1}".format(index, domain))
                url = "https://" + domain
                text = visit(browser, url)
                if text:
                    df.loc[len(df)] = {
                        "domain": domain,
                        "text": text
                    }
            except Exception as error:
                print(error)
            finally:
                df.to_csv('./domain_html.csv', index=False)
    except Exception as error:
        print(error)
    finally:
        browser.close()
        browser.quit()


if __name__ == '__main__':
    main()
