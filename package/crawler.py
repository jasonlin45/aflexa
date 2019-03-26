import mechanicalsoup
#import soupsieve as sv
#import getpass

class Crawler:
	def __init__(self):
		self.browser = mechanicalsoup.StatefulBrowser(
			soup_config={'features': 'html5lib'},
			raise_on_404=True
		)
		#print(self.browser)
		self.browser.open("https://cas.wm.edu/cas/login?service=https%3A%2F%2Ftribecard.wm.edu%2Flogin%2Fcas.php")
		print(self.browser.get_url())
	def login(self, username, password):
		#print(self.browser.get_current_page())
		self.browser.select_form('form[method="post"]')
		#self.browser.get_current_form().print_summary()
		self.browser["username"] = username
		self.browser["password"] = password
		self.browser["publicWorkstation"] = True
		#self.browser.launch_browser()
		response = self.browser.submit_selected()
		
		#verify login
		page = self.browser.get_current_page()
		#print(type(page))
		#self.browser.launch_browser()
		assert str(page.select("title")[0]) == "<title>Welcome</title>"
		print("/////////////LOGGED IN/////////////")
	def checkCash(self):
		page = self.resetBrowser()
		#print(type(page))
		tables = page.select("table[border=\"1\"]")
		#print(tables)
		results = []
		for table in tables:
			for row in table.findAll('tr'):
				#print(row)
				aux = row.findAll('td')
				#print(aux)
				if len(aux)!=0:
					aux[0] = aux[0].findAll('a')[0]
					results.append(aux[1].string.rstrip())
		#print(results)
		return results
	def checkLaundry(self):
		self.resetBrowser()
		self.browser.open("https://tribecard.wm.edu/student/laundry/room_summary_srv.php")
		page = self.browser.get_current_page()
		table = page.select("table")[1]
		results = []
		otpWash = None
		otpDry = None
		yWash = None
		yDry = None
		otp = False
		y = False
		
		for row in table.findAll('tr'):
			#print(row)
			location = []
			for col in row.findAll('td'):
				#print(col)
				if col.string == None:
					if len(col.select("input"))!=0:
						pass
					else:
						location.append(col.get_text().rstrip().replace(" ","").split("/")[0])
				else:
					if len(col.select("small"))==0:
						loc = col.string.replace(" ","").replace("Laundry","").replace("Room","").replace("Floor"," Floor")
						if loc == "JamestownNorth":
							loc = "Hardy"
						elif loc == "JamestownSouth":
							loc = "Lemon"
						location.append(loc)
			#print(location)
			
			
			if len(location)!=0:
				if location[0] == "OneTribePlaceWashers":
					otp = True
					otpWash = location[1]
				elif location[0] == "OneTribePlaceDryers":
					otp = True
					otpDry = location[2]
				elif location[0] == "YatesWashers":
					y = True
					yWash = location[1]
				elif location[0] == "YatesDryers":
					y = True
					yDry = location[2]
				if otpWash != None and otpDry != None:
					results.append(["OneTribePlace",otpWash,otpDry])
					otp = False
					otpWash = None
					otpDry = None
				elif yWash != None and yDry != None:
					results.append(["Yates",yWash,yDry])
					y = False
					yWash = None
					yDry = None
				elif not y and not otp:
					results.append(location)
		#print(table)
		#print(page)
			#print(location)
		return results
	def getLaundryData(self, data, building, location=""):
		if location == None:
			location = ""
		output = []
		for room in data:
			if building.lower() in room[0].lower():
				if location != "":
					if location in room[0]:
						room[0] = (building + " " + location).lower()
						output.append(room)
				else:
					room[0] = (building + " " + room[0].lower().replace(building.lower(),"")).strip()
					output.append(room)
		return output
	def resetBrowser(self):
		self.browser.open("https://tribecard.wm.edu/student/welcome.php")
		page = self.browser.get_current_page()
		#print(type(page))
		assert str(page.select("title")[0]) == "<title>Welcome</title>"
		return page
	
#if __name__ == "__main__":
#	crawl = Crawler()
	#username = input("Username: ")
	#password = getpass.getpass()
	#crawl.login(username,password)
	#print(crawl.checkCash())
#	print(crawl.checkLaundry())
#	print(crawl.getLaundryData(crawl.checkLaundry(), ""))
	#print(crawl.getLaundryData("Yates"))