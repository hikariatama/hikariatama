from time import time, sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

login, password = input('Login: '), input('Password: ')
iteration_delay = float(
    input('Delay IN MINUTES (Sample for 30 minutes delay: 30): ')) * 60
iter_count = int(input('Iterations quantity:'))

options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")

driver = webdriver.Chrome(
    executable_path="chromedriver.exe", chrome_options=options)
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


click_elem((By.ID, 'mat-input-0'))


def iteration():
    print('Start processing')
    sts = time()
    driver.get('https://45.146.166.147:3443')
    click_elem((By.XPATH, '//p[contains(text(), "Scans")]'))
    click_elem((By.XPATH, '//span[contains(text(), "Filter")]'))
    click_elem((By.XPATH, '//*[@id="cdk-overlay-1"]/div/div/button[4]'))
    click_elem((By.CLASS_NAME, 'mat-select-value'))
    click_elem((By.XPATH, '//span[contains(text(), "In Progress")]'))
    sleep(3)
    answ = driver.execute_script('''var rows = document.querySelectorAll('.mat-table tbody tr');
    var logdata = [];
    var counter = 0;
    for(let i = 0; i < rows.length; i++) {
        let cols = rows[i].querySelectorAll('td');
        let domain = cols[1].querySelector('a').innerHTML;
        let last_run = cols[3].querySelector('span').innerHTML;
        let vulnerabilites = cols[4].querySelector('.severity-high').innerHTML;
        if(Math.floor(Date.now() / 1000) - (new Date(last_run.substr(12)).getTime()/1000) >= (20 * 60)) {
            if(parseInt(vulnerabilites) > 0) {
                cols[0].querySelector('input').click();
                counter += 1;
            }
        }
    }
    document.querySelector('button[mattooltip="Stop Scans"]').click();
    return counter;''')
    click_elem((By.XPATH, '//button[contains(text(), "Yes")]'))
    print('Finished stopping | ' + str(answ) + ' scans stopped')

    sleep(3)
    answ = driver.execute_script('''var rows = document.querySelectorAll('.mat-table tbody tr');
    var logdata = [];
    var counter = 0;
    for(let i = 0; i < rows.length; i++) {
        let cols = rows[i].querySelectorAll('td');
        let domain = cols[1].querySelector('a').innerHTML;
        let last_run = cols[3].querySelector('span').innerHTML;
        let vulnerabilites = cols[4].querySelector('.severity-high').innerHTML;
        if(Math.floor(Date.now() / 1000) - (new Date(last_run.substr(12)).getTime()/1000) >= (20 * 60)) {
            if(parseInt(vulnerabilites) == 0) {
                cols[0].querySelector('input').click();
                counter += 1;
            }
        }
    }
    document.querySelector('button[mattooltip="Delete Scans"]').click();
    return counter;''')
    click_elem((By.XPATH, '//button[contains(text(), "Yes")]'))
    print('Finished deleting | ' + str(answ) + ' scans deleted')
    print('End processing | ' + str(round(time() - sts)) + ' sec')


for i in range(iter_count):
    print('Iteration #' + str(i + 1))
    iteration()
    print('Sleeping...')
    sleep(iteration_delay)
