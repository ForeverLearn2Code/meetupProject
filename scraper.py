from configparser import ConfigParser
from lxml import html
from constants import DATA_SETS, CONSULTANT_DATA_SETS
import requests

def getMarketData(user='loginResearcher'):
	POSTLOGINURL = 'https://www.worldquantvrc.com/login/process'
	REQUESTURL = 'https://www.worldquantvrc.com/en/cms/available-data-operator/available-market-data/'
	CONSULTANTDATAURL = 'https://www.worldquantvrc.com/en/cms/consultant/additional-dataset/'
	
	configFilePath = r'./loginConfig.ini'

	parser = ConfigParser()
	parser.read(configFilePath)

	usernameStr = parser.get(user, 'userName')
	passwordStr = parser.get(user, 'password')

	payload = {
	    'EmailAddress': usernameStr,
	    'Password': passwordStr,
	    'next': REQUESTURL
	}
	
	with requests.Session() as session:
	    post = session.post(POSTLOGINURL, data=payload, verify = False)
	    r = session.get(REQUESTURL, verify = False)
	    tree = html.fromstring(r.content)
	    instruments = tree.xpath("//tr/*//strong/text()")
	    boolFlag = tree.xpath("//tr/td[4]/p/text()")
	    marketData = parseInstruments(instruments, boolFlag)
	    return marketData


def parseInstruments(instruments, boolFlag):
	data_set_index, index = -1, 0
	marketData = {}
	skipLists = ['Data Name', 'Description', 'Python Usage', 'USA', 'EUR', 'ASI']
	while index in range(len(instruments)):
		if not instruments[index] in skipLists:
			if DATA_SETS[data_set_index] == 'fundamental':
				if not boolFlag[index-27] == "\u00A0":
					marketData.setdefault(DATA_SETS[data_set_index], []).append(instruments[index])
				index += 1
			else:
				marketData.setdefault(DATA_SETS[data_set_index], []).append(instruments[index])
				index += 1
		else:
			data_set_index += 1
			while instruments[index] in skipLists:
				index += 1
	return marketData

