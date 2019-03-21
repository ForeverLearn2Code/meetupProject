from configparser import ConfigParser

config = ConfigParser()

config['loginManyu'] = {
	'userName': 'randomusername@randomdomainname.org',
	'password': 'randompassword'
}

config['loginResearcher'] = {
	'userName': 'randomresearcher@randomcompany.com',
	'password': 'itsnotmybirthdate'
}

# add more Login infos here

with open('./loginConfig.ini', 'w') as file:
	config.write(file)


