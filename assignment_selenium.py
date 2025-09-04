"""
Selenium Demo: Testing 5 features on https://the-internet.herokuapp.com/
- Runs in Incognito mode
- Suppresses ChromeDriver logs
- Confirms each test with ✅ message
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Setup Chrome in incognito + suppress logs ---
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_experimental_option("excludeSwitches", ["enable-logging"])  # suppress logs
driver = webdriver.Chrome(options=options)
driver.maximize_window()

wait = WebDriverWait(driver, 10)

driver.get("https://the-internet.herokuapp.com/")

# --- 1. Checkboxes ---
driver.find_element(By.LINK_TEXT, "Checkboxes").click()
checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")

# Toggle first checkbox
if not checkboxes[0].is_selected():
    checkboxes[0].click()
time.sleep(1)

# Untick second checkbox if ticked
if checkboxes[1].is_selected():
    checkboxes[1].click()
time.sleep(1)

print("✅ Test 1 (Checkboxes) completed successfully.")
time.sleep(2)
driver.back()

# --- 2. Dropdown ---
driver.find_element(By.LINK_TEXT, "Dropdown").click()
dropdown = driver.find_element(By.ID, "dropdown")
dropdown.click()
dropdown.find_element(By.XPATH, "//option[. = 'Option 2']").click()
print("✅ Test 2 (Dropdown) completed successfully.")
time.sleep(2)
driver.back()

# --- 3. Form Authentication ---
driver.get("https://the-internet.herokuapp.com/login")

username = wait.until(EC.presence_of_element_located((By.ID, "username")))
password = driver.find_element(By.ID, "password")

username.send_keys("tomsmith")
password.send_keys("SuperSecretPassword!")
driver.find_element(By.CSS_SELECTOR, "button.radius").click()

# Wait for success message
flash = wait.until(EC.visibility_of_element_located((By.ID, "flash")))
print("Login message:", flash.text.strip())
print("✅ Test 3 (Form Authentication) completed successfully.")

# Logout
driver.find_element(By.LINK_TEXT, "Logout").click()
time.sleep(2)

# Back to homepage
driver.get("https://the-internet.herokuapp.com/")

# --- 4. JavaScript Alerts ---
driver.find_element(By.LINK_TEXT, "JavaScript Alerts").click()
driver.find_element(By.XPATH, "//button[text()='Click for JS Alert']").click()

alert = driver.switch_to.alert
print("Alert text:", alert.text)
alert.accept()
print("✅ Test 4 (JavaScript Alerts) completed successfully.")
time.sleep(2)
driver.back()

# --- 5. Dynamic Loading ---
driver.find_element(By.LINK_TEXT, "Dynamic Loading").click()
driver.find_element(By.LINK_TEXT, "Example 2: Element rendered after the fact").click()
driver.find_element(By.CSS_SELECTOR, "div#start button").click()

hello_elem = wait.until(EC.visibility_of_element_located((By.ID, "finish")))
print("Dynamic loading text:", hello_elem.text.strip())
print("✅ Test 5 (Dynamic Loading) completed successfully.")
time.sleep(2)

# Cleanup
driver.quit()
print("🎉 All 5 tests completed successfully.")
