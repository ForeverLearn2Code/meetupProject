from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def navigateToSimulationPage(browser):
	alphasButton = WebDriverWait(browser, 15).until(
		EC.element_to_be_clickable((By.XPATH, '//*[@id="websim-navbar-left"]/ul/li[2]/span/a')))
	alphasButton.click()

	simulateButton = WebDriverWait(browser, 15).until(
		EC.element_to_be_clickable((By.XPATH, '//*[@id="websim-navbar-left"]/ul/li[2]/span/ul/li[1]/a')))
	simulateButton.click()