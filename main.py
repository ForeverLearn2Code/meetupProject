import sys, getopt
import loginScript, navigateToSimulation, scraper, submitAlpha
from selenium import webdriver

def main(argv):
	user = 'loginResearcher'
	browser = webdriver.Chrome()
	browser.maximize_window()
	loginScript.login(user, browser)

	marketData = scraper.getMarketData(user)
	print(marketData)
	metaData = parseArguments(argv)
	navigateToSimulation.navigateToSimulationPage(browser)
	if not metaData['includeAll']:
		marketData = marketData[metaData['dataSet']]
	elif metaData['includeAll']:
		flattenList = []
		for k, v in marketData.items():
			flattenList.extend(v)
		marketData = flattenList
	if metaData['start']:
		startIndex = marketData.index(metaData['start'])
		marketData = marketData[startIndex:]
	submitAlpha.simulateAlpha(browser, marketData, metaData)

def parseArguments(argv):
	try:
		opts, args = getopt.getopt(argv, "ahn:d:e:s:")
	except getopt.GetoptError:
		print('main.py -n <nameOfAlpha> -d <dataSet>')
		sys.exit(2)
	metaData = {
		'includeAll': False,
		'start': False
	}
	for opt, arg in opts:
		if opt == '-h':
			print('main.py -n <nameOfAlpha> -d <dataSet>')
			sys.exit()
		elif opt == '-n':
			metaData['alphaName'] = arg
		elif opt == '-d':
			metaData['dataSet'] = arg
		elif opt == '-a':
			metaData['includeAll'] = True
		elif opt == '-s':
			metaData['start'] = arg
	return metaData

if __name__ == "__main__":
	main(sys.argv[1:])