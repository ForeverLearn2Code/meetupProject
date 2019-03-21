import time
from constants import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

def simulateAlpha(browser, instrumentList, metaData):
	instrumentIndex = 0
	while instrumentIndex in range(len(instrumentList)):
		try:
			enterAlphaExpression(browser, instrumentList[instrumentIndex])
			clickBlankSpace(browser)
			WebDriverWait(browser, 10).until(
				EC.invisibility_of_element_located((By.CLASS_NAME, 'CodeMirror-hints')))
		except:
			browser.refresh()
		time.sleep(1)	
		clickSimulationButton(browser)
		time.sleep(3)
		simulationButton = browser.find_elements_by_class_name('sim-action-simulate')
		if len(simulationButton) > 0:
			clickSimulationButton(browser)
		try:
			WebDriverWait(browser, 20).until(
				EC.visibility_of_element_located((By.XPATH, '/html/body/main/article/div/div/div[2]/div/div/div/div')))
		except:
			try:
				WebDriverWait(browser, 625).until(
					EC.visibility_of_element_located((By.CLASS_NAME, 'highcharts-grid')))
			except:
				browser.refresh()
		try:
			setAlphaMetaData(browser, metaData, instrumentList[instrumentIndex])
		except:
			print('couldnt save metaData')
		deleteAlphaExpression(browser)
		clickBlankSpace(browser)
		clickResultsTab(browser)
		instrumentIndex += 1
		
def compareBanner(browser, succes_key, dictionary):
	bannerElement = WebDriverWait(browser, 10).until(
			EC.visibility_of_element_located((By.XPATH, '/html/body/main/article/div/div/div[2]/div/div/div/div')))
	bannerText = bannerElement.get_attribute('innerHTML')
	if dictionary[succes_key] == bannerText:
		return True
	else:
		return False

def clickBlankSpace(browser):
	actions = ActionChains(browser)
	blankSpace = WebDriverWait(browser, 10).until(
			EC.visibility_of_element_located((By.ID, 'test-flowsexprCode')))
	actions.move_to_element(blankSpace).click()
	actions.perform()

def returnActiveTab(browser):
	chartsTab = WebDriverWait(browser, 10).until(
		EC.visibility_of_element_located((By.CSS_SELECTOR, '.active.item')))
	return chartsTab.get_attribute('innerHTML')

def setAlphaMetaData(browser, metaData, instrument):
	time.sleep(0.3)
	metaDataTab = WebDriverWait(browser, 10).until(
			EC.visibility_of_element_located((By.XPATH, '//*[@id="resultTabPanel"]/div[1]/a[3]')))
	metaDataTab.click()
	inputBox = WebDriverWait(browser, 60).until(
			EC.visibility_of_element_located((By.XPATH, '//*[@id="metadataTab"]/div/form/div[1]/div[1]/input')))
	inputBox.clear()
	inputBox.send_keys(metaData['alphaName'] + instrument)
	submitButton = WebDriverWait(browser, 10).until(
			EC.visibility_of_element_located((By.ID, 'save-alpha-metadata')))
	try:
		submitButton.click()
	except WebDriverException as e:
		popOver = WebDriverWait(browser, 10).until(
			EC.visibility_of_element_located((By.CLASS_NAME, 'CodeMirror-hints')))
		popOver.click()
		submitButton = WebDriverWait(browser, 10).until(
			EC.visibility_of_element_located((By.ID, 'save-alpha-metadata')))
		submitButton.click()
	if compareBanner(browser, 'metadata_saved', SUCCESS_BANNER):
		return
	else:
		submitButton.click()
	time.sleep(1)

def clickResultsTab(browser):
	blankSpace = WebDriverWait(browser, 30).until(
			EC.visibility_of_element_located((By.XPATH, '/html/body/main/article/div/div/div[1]/div/div[3]/div/label[2]')))
	blankSpace.click()

def enterAlphaExpression(browser, instrument):
	try:
		actions = ActionChains(browser)
		inputBox = WebDriverWait(browser, 15).until(
				EC.element_to_be_clickable((By.CLASS_NAME, ' CodeMirror-line ')))
		time.sleep(0.5)
		actions.move_to_element(inputBox).click()
		time.sleep(0.5)
		actions.send_keys(generateAlpha(instrument))
		actions.perform()
	except:
		pass

def deleteAlphaExpression(browser):
	actions = ActionChains(browser)
	inputBox = WebDriverWait(browser, 15).until(
			EC.element_to_be_clickable((By.CLASS_NAME, ' CodeMirror-line ')))
	actions.move_to_element(inputBox).click()
	actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL)
	actions.send_keys(Keys.DELETE)
	actions.perform()

def clickSimulationButton(browser):
	simulateButton = WebDriverWait(browser, 60).until(
			EC.visibility_of_element_located((By.CLASS_NAME, 'sim-action-simulate')))
	simulateButton.click()

def generateAlpha(instrument):
	print('rank(-delta('+ instrument +', 5))')
	return '''rank(-delta('''+ instrument +''', 5))                                '''