import os
import shutil
from selenium import webdriver
import time
from utils.kaggleEnums import  filePath
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

driver=None
#hides the console output for from webdriver_manager.chrome import

# seleniumPath="C:\Users\garyee\selenium"
# fireFoxProfilePath=seleniumPath+"profile/"

# if(not os.path.exists(seleniumPath)):
#   os.mkdir(seleniumPath)

# if(not os.path.exists(fireFoxProfilePath)):
#   os.mkdir(fireFoxProfilePath)

# def saveProfile(driver):
#     driver.execute_script("window.close()")
#     time.sleep(0.5)
#     currentProfilePath = driver.capabilities["moz:profile"]
#     profileStoragePath = seleniumPath
#     shutil.copytree(currentProfilePath,
#         profileStoragePath,
#         ignore_dangling_symlinks=True
#         )

# def getRealFireFoxProfile():
#     return webdriver.FirefoxProfile(r'C:\Users\garyee\AppData\Roaming\Mozilla\Firefox\Profiles\13e17tyu.default-release-1576269741335')

# # def acceptCompetitionRuleWrapper(dataSetRef):
# #     try:
# #         acceptCompetitionRules(dataSetRef)
# #     except NoSuchElementException:
def setupDriver():
    global driver
    os.environ['WDM_LOG_LEVEL'] = '0'
    if(driver is None):
        options = webdriver.ChromeOptions()
        options.add_argument('user-data-dir=C:\\Users\\garyee\AppData\\Local\\Google\\Chrome\\User Data')
        options.add_argument('profile-directory=Default')
        options.add_argument('--headless')
        options.add_argument('--log-level=3')
        driver = webdriver.Chrome(executable_path=filePath+'chromedriver.exe', options=options)
    return driver

def shutDownDriver():
    global driver
    if(driver is None):
        driver.close()

def acceptCompetitionRules(dataSetRef):
    kaggleRuleURL= 'https://www.kaggle.com/competitions/'+dataSetRef+'/rules'
    
    driver = setupDriver()
    driver.get(kaggleRuleURL)
    driver.implicitly_wait(3)
    pageSource = driver.page_source
    loggedIn=None
    buttonLoggedInVersion=None
    buttonNOTLoggedInVersion=None
    try:
        buttonLoggedInVersion = driver.find_element(By.CSS_SELECTOR , "div.competition-rules__acceptance-actions > button")
        loggedIn=True
    except NoSuchElementException:
        try:
            buttonNOTLoggedInVersion = driver.find_element(By.CSS_SELECTOR , "div.competition-rules__acceptance-actions > a")
            loggedIn=False
        except NoSuchElementException:  #spelling error making this code not work as expected
            raise Exception('Accept rules scraping error!')
    
    # button = driver.find_element_by_id('buttonID') //Or find button by ID.
    if(loggedIn and buttonLoggedInVersion):
        buttonLoggedInVersion.click()
        print("accepted rule to the competition: "+dataSetRef)
    else:
        print("Failed to accept rule of competition: "+dataSetRef)
    