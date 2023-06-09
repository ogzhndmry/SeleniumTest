from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from constants import globalConstants

class Test_Kodlamaio:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.maximize_window()
        self.driver.get(globalConstants.URL)

    def test_invalid_login(self):
        # En fazla 5 saniye olacak şekilde user-name ID'li elementin görünmesini bekle
        WebDriverWait(self.driver,5).until(ec.visibility_of_all_elements_located((By.ID,globalConstants.username)))
        userNameInput = self.driver.find_element(By.ID,globalConstants.username)
        passWord = self.driver.find_element(By.ID,globalConstants.password)
        userNameInput.send_keys("1")
        passWord.send_keys("1")
        sleep(2)
        loginBtn = self.driver.find_element(By.ID,globalConstants.loginButton)
        loginBtn.click()   
        errorMessage = self.driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div[1]/div/div/form/div[3]/h3")
        testResult = errorMessage.text == "Hatalı Giriş"
        print(f"Test Sonucu: {testResult}")

    def test_valid_login(self):
        self.driver.get(globalConstants.URL)
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,globalConstants.username)))
        usernameInput = self.driver.find_element(By.ID,globalConstants.username)
        passWord = self.driver.find_element(By.ID,globalConstants.password)
        # Action Chains
        actions = ActionChains(self.driver)
        actions.send_keys_to_element(usernameInput,"standart_user")
        actions.send_keys_to_element(passWord,"secret_sauce")
        actions.perform()
        loginBtn = self.driver.find_element(By.ID,globalConstants.loginButton)
        loginBtn.click()





testClass = Test_Kodlamaio()
testClass.test_invalid_login()
testClass.test_valid_login()
