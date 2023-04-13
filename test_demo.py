from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from pytest import mark
from pathlib import Path
from datetime import date

#prefix => ön ek test_
#postfix => 
class Test_DemoClass:
    #her testten önce çağrılır
    def setup_method(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.maximize_window()
        self.driver.get("https://www.saucedemo.com/")
        #günün tarihini al bu tarih ilebir klasör var mı kontrol et yoksa oluştur
        self.folderPath = str(date.today())
        Path(self.folderPath).mkdir(exist_ok=True)

    #her testten sonra çağrılır
    def teardown_method(self):
        self.driver.quit()

    #@mark.skip()
    @mark.parametrize("username,password",[("1","1"), ("kullaniciadim","sifrem")])
    def test_invalid_login(self,username,password):
        self.waitForElementVisible((By.ID,"user-name"))
        userNameInput = self.driver.find_element(By.ID,"user-name")
        passwordInput = self.driver.find_element(By.ID,"password")
        userNameInput.send_keys(username)
        passwordInput.send_keys(password)
        loginBtn = self.driver.find_element(By.ID,"login-button")
        loginBtn.click()   
        errorMessage = self.driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div[1]/div/div/form/div[3]/h3")
        self.driver.save_screenshot(f"{self.folderPath}/test-invalid-login-{username}-{password}.png")
        assert errorMessage.text == "Epic sadface: Username and password do not match any user in this service"

    @mark.parametrize("username,password",[("standard_user","secret_sauce"), ("locked_out_user", "secret_sauce"), ("problem_user","secret_sauce")])
    def test_valid_login(self,username,password):
        self.driver.get("https://www.saucedemo.com/")
        self.waitForElementVisible((By.ID,"user-name"))
        usernameInput = self.driver.find_element(By.ID,"user-name")
        passwordInput = self.driver.find_element(By.ID,"password")
        # Action Chains
        actions = ActionChains(self.driver)
        actions.send_keys_to_element(usernameInput,username)
        actions.send_keys_to_element(passwordInput,password)
        actions.perform()
        loginBtn = self.driver.find_element(By.ID,"login-button")
        loginBtn.click()

    def waitForElementVisible(self,locator,timeout=5):
        WebDriverWait(self.driver,timeout).until(ec.visibility_of_element_located(locator))  