from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import time, sleep
import sys

if len(sys.argv < 5):
    sys.exit('python dobavlator.py login pass delay domain_num')

login, password, iteration_delay, domain_num = sys.argv[1:]
iteration_delay = float(iteration_delay)
domain_num = int(domain_num)

options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")

driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=options)
driver.get('https://<ip>:3443/#/login')


def click_elem(elem):
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located(elem))
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable(elem))
        driver.find_element(*elem).click()
    except:
        pass


click_elem((By.ID, 'mat-input-0'))
driver.find_element_by_id('mat-input-0').send_keys(login)

click_elem((By.ID, 'mat-input-1'))
driver.find_element_by_id('mat-input-1').send_keys(password)

click_elem((By.CLASS_NAME, 'mat-checkbox-inner-container'))
click_elem((By.CSS_SELECTOR, 'button[type=submit]'))
click_elem((By.XPATH, '//button[contains(text(), "Logout")]'))


def iteration(domain):
    print('Start processing ' + domain)
    sts = time()
    click_elem((By.XPATH, '//p[contains(text(), "Targets")]'))
    click_elem((By.XPATH, '//p[contains(text(), "Add Target")]'))
    click_elem((By.CSS_SELECTOR, 'input[formcontrolname="address"]'))
    driver.find_element_by_css_selector('input[formcontrolname="address"]').send_keys(domain)
    click_elem((By.XPATH, '//span[contains(text(), "Save")]'))
    click_elem((By.CSS_SELECTOR, 'button[mattooltip=Scan]'))
    driver.execute_script(
        'document.querySelector("button[mattooltip=Scan]").click();')
    click_elem((By.XPATH, '//button[contains(text(), "Yes")]'))
    click_elem((By.CSS_SELECTOR, 'mat-select[formcontrolname=scanType]'))
    driver.execute_script(
        'document.querySelector("mat-select[formcontrolname=scanType]").click();')
    click_elem((By.XPATH, '//span[contains(text(), "High Risk Vulnerabilities")]'))
    click_elem((By.XPATH, '//button[contains(text(), "Create Scan")]'))
    print('End processing | ' + str(round(time() - sts)) + ' sec')


with open('domains.txt', 'r') as f:
    domains = f.read().split('\n')
    for i in range(min(len(domains), domain_num)):
        iteration(domains[i])
        with open('domains.txt', 'w') as f2:
            f2.write('\n'.join(domains[i + 1:]))

        print('Sleeping...')
        sleep(iteration_delay)
