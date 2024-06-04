from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from time import sleep
from selenium_stealth import stealth
from random import randint, choice, uniform
import sys
import json
from hide_me import create_tor_proxy, ip,user_agent
from random import randrange

# Constants for colored output
G = "\033[32m"    # Green
W = "\033[0m"     # White
RR = "\033[31;1m" # Red light 
YY = "\033[33;1m" # Yellow light
C = "\033[36m"    # Cyan
B = "\033[34m"    # Blue

def random_delay(min_delay=0.5, max_delay=2.0):
    sleep(uniform(min_delay, max_delay))

def save_used_user_agent(used_user_agent):
    with open('used_user_agents.txt', 'a') as file:
        file.write(used_user_agent + '\n')

def choose_random_user_agent():
    with open('user-agents.txt', 'r') as file:
        user_agents = file.readlines()
    try:
        with open('used_user_agents.txt', 'r') as file:
            used_user_agents = file.readlines()
    except FileNotFoundError:
        used_user_agents = []
    user_agents = [ua for ua in user_agents if ua not in used_user_agents]
    if len(user_agents) == 0:
        return "All user agents have been used."
    return choice(user_agents).strip()

def human_typing(element, text, min_delay=0.1, max_delay=0.3):
    for char in text:
        element.send_keys(char)
        sleep(uniform(min_delay, max_delay))

def human_mouse_move(driver, element):
    action = ActionChains(driver)
    action.move_to_element(element)
    action.perform()
    random_delay()

def find_element_with_retry(driver, by, value, retries=3):
    for _ in range(retries):
        try:
            element = driver.find_element(by, value)
            return element
        except :
            random_delay()
    return None

arguments = [
    "-no-first-run",
    "-force-color-profile=srgb",
    "-metrics-recording-only",
    "-password-store=basic",
    "-use-mock-keychain",
    "-export-tagged-pdf",
    "-no-default-browser-check",
    "-disable-background-mode",
    "-enable-features=NetworkService,NetworkServiceInProcess,LoadCryptoTokenExtension,PermuteTLSExtensions",
    "-disable-features=FlashDeprecationWarning,EnablePasswordsAccountStorage",
    "-deny-permission-prompts",
    "-disable-gpu"
]

control_port = randrange(8000,10000)
socks_port = randrange(4444,6000)
create_tor_proxy(socks_port,control_port)
ip(socks_port)
options = Options()
options.add_argument(f"--proxy-server=socks5://127.0.0.1:{socks_port}")
options.add_argument(f"user-agent={user_agent}")
options.add_extension('adgaurd.crx')
options.add_extension('urban.crx')
options.add_experimental_option("detach", True)
agent = choose_random_user_agent()
options.add_argument(f"user-agent={agent}")
# options.add_argument("--headless=new")
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

for argument in arguments:
    options.add_argument(argument)

driver = webdriver.Chrome(options=options)
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': '''
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
    '''
})

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

driver.get("chrome-extension://eppiocemhmnlbhjplcgkofciiegomcon/popup/index.html#/welcome-consent")
driver.maximize_window()

def waitforid(id):
    t = 0
    while True:
        if t == 8:
            driver.quit()
        try:
            driver.find_element(By.ID, value=id)
            print(G + "ID Found ")
            break
        except:
            print('waiting......')
            sleep(2)
            t += 1

def waitfor(path):
    t = 0
    while True:
        if t == 8:
            break
        try:
            driver.find_element(By.XPATH, value=path)
            break
        except :
            print('waiting......')
            sleep(2)
            t += 1

def vpn(driver):
    sleep(8)
    driver.switch_to.window(driver.window_handles[0])
    waitfor("/html/body/div/div/div[2]/div/div/div/button[2]")
    clickby_xpath(driver, "/html/body/div/div/div[2]/div/div/div/button[2]")
    clickby_xpath(driver, "/html/body/div/div/div[3]/div[2]/div/div[1]/input")
    search_box = driver.find_element(By.XPATH, value="/html/body/div/div/div[3]/div[2]/div/div[1]/input")
    human_typing(search_box, "United States (USA)")
    driver.implicitly_wait(5)
    i = 1
    clickby_xpath(driver, f"/html/body/div/div/div[3]/div[2]/div/div[2]/div/ul/li[{i}]")
    sleep(1)
    driver.switch_to.window(driver.window_handles[1])
    print(B + "VPN ACTIVATED" + YY)
    sleep(1)
    start(driver)

def new_tab():
    driver.execute_script("window.open('');")
    sleep(2)
    driver.switch_to.window(driver.window_handles[2])
    driver.get("https://droplink.co/Fs9rS")

def start(driver):
    sleep(2)
    driver.get("https://droplink.co/Fs9rS")
    l = 0
    while True:
        try:
            if driver.find_element(By.XPATH, value="/html/body/a/img"):
                break
        except :
            if l == 3:
                # driver.quit()
                sys.exit()
            new_tab()
            l = l+1
            
    if driver.find_element(By.XPATH, value="/html/body/a/img"):
        print(G + "Started Not")
    print(B + 'LINK SEARCHED' + YY)
    sleep(1)
    process(driver)

def clickby_id(id):
    while True:
        try:
            el = driver.find_element(By.ID, value=id)
            human_mouse_move(driver, el)
            el.click()
            print(G + "ID Success" + C)
            break
        except:
            print(RR + "ID error" + C)
            random_delay()

def clickby_xpath(driver, path, attempts=5):
    if attempts == 0:
        driver.quit()
        sys.exit()
    try:
        element = driver.find_element(By.XPATH, path)
        human_mouse_move(driver, element)
        element.click()
        print(G + "XPath Success" + C)
    except :
        print(RR + "XPath error:" + C)
        random_delay()
        clickby_xpath(driver, path, attempts - 1)

id = "go_d"
id_2 = "go_d2"
id_x = "t_modal_close_x"
get = '/html/body/div[1]/div/div/div/div[3]/a'

def process(driver):
    print(B + "PROCESS STARTED " + YY)
    print("5")
    waitforid(id)
    clickby_id(id)
    print("4")
    clickby_id(id_x)
    clickby_id(id_2)
    print("3")
    waitforid(id)
    clickby_id(id)
    clickby_id(id_x)
    print("2")
    clickby_id(id_2)
    clickby_xpath(driver, get)
    print("1")
    sleep(3)
    save_used_user_agent(agent)
    print("USER AGENT SAVED")
    driver.quit()

# vpn(driver)
start(driver)
