import requests
import xml.etree.ElementTree as ET
import glob


#filename = glob.glob("./Downloads/Datasets/ctgov2016_2017/*.xml")
terms = []

# Function to create set of all terms found in dataset files
def collectTerms(filename):
	print("Collecting terms, please wait")
	for file in filename:
		tree = ET.parse(file)
		root = tree.getroot()
		tags = []
		for child in root:
			tags.append(child.tag)
		try:
			i = tags.index("condition_browse")
		except:
			i = None
		try:
			j = tags.index("intervention_browse")
		except:
			j = None
		childCondition = 0
		childIntervention = 0
		if i != None:
			for child in root[i]:
				childCondition += 1
		if j != None:
			for child in root[j]:
				childIntervention += 1
		for x in range(childCondition):
			terms.append(root[i][x].text)
		for x in range(childIntervention):
			terms.append(root[j][x].text)

	termSet = set(terms)
	return termSet

# Function to find CUI for a specific term
def findCui(user, token):
	print("Here is the set of terms: ", termSet)
	print()
	print()
	print("="*100)
	term = input("Enter the term from the set of terms displayed above for which to find CUI: ")
	url = "http://havoc.appliedinformaticsinc.com/concepts"
	parameters = {"term": term, "user": user, "token": token} 
	r = requests.get(url, params=parameters)
	cuis = []
	for element in r.json():
		cuis.append(element['cui'])
	print()
	print()
	print("="*100)
	print("Here is the list of CUIs associated with the term: ", cuis)

# Function to find synonyms for a specific CUI
def findSynonyms(user, token):
	cui = input("Enter the CUI for which to find synonyms: ")
	url =  "http://havoc.appliedinformaticsinc.com/concepts" + "/" + cui + "/synonyms"
	parameters = {"user": user, "token": token} 
	print("Here is the list of synonyms: ") 
	r = requests.get(url, params=parameters)
	print(r.json())

if __name__ == "__main__":
	#Create list of filenames of all dataset files
	path = input("Please specify the full path to where the files of dataset ctgov2016_2017 are present: ")
	path = path + "/*.xml"
	filename = glob.glob(path)
	termSet = collectTerms(filename)

	while(True):
		print()
		print()
		print()
		print("Enter the desired option from the following list of options: ")
		print()
		print("1 - Find CUI for concepts corresponding to a term")
		print()
		print("2 - Find synonyms for a given CUI:")
		print()
		print("3 - End the program")
		choice = input()
		
		if choice == "3":
			break
		else:
			user = input("Enter the user: ")
			token = input("Enter the token: ")
			if choice == "1":
				findCui(user,token)
			elif choice == "2":
				findSynonyms(user,token)
