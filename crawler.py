import csv
# Function to retrieve the page

def get_page(url):
	try:
		import urllib.request
		return urllib.request.urlopen(url).read()
	except:
		return ""

# Function to extract the first link from the page

def get_next_target(page):
	start_link = page.find("<a href=")
	if start_link == -1:
		return None, 0
	start_quote = page.find('"', start_link)
	end_quote = page.find('"', start_quote + 1)
	url = page[start_quote + 1:end_quote]
	return url, end_quote

# Function to extract all the links on a page

def get_all_links(content,flag):
	links = []
	prefix = "https://en.wikipedia.org"
	if flag == True:
		start = content.find('a href="/wiki/Portal:Disease"')
		stop = content.find("Very early onset inflammatory bowel disease")
		content = content[start:stop]
	while True:
		url,endpos = get_next_target(content)
		
		# Add the url retrieved(if any) as link found
		if url:
			# If the url is relative, make it absolute and then add it to the links, otherwise add it to links simply
			if url[0:6] == "/wiki/":
				links.append(prefix + url)
			else:
				links.append(url)
			
			# Update the page to be searched for links
			content = content[endpos:]
		else:
			break
	return links

# Function to perform set union

def union(p,q):
	#Append all the elements in list q that are not already in list p to list p
	for e in q:
		if e not in p:
			p.append(e)
# Function to crawl

def crawl_web(seed):
	tocrawl = [seed]	# List of known pages to be crawled
	crawled = []		# List of pages already crawled
	linksDict = {}
	while tocrawl:
		flag = False	# Is page to be crawled a seed page
		
		# Select the page to crawl in FIFO order
		tocrawl.reverse()
		page = tocrawl.pop()
		tocrawl.reverse()
		
		# Crawl the pages that are on en.wikipedia.org but do not crawl pages that contain certain strings
		if page.find("en.wikipedia.org") != -1 and page.find("/wiki/Special") == -1 and page.find("/wiki/User") == -1:
			
			#Crawl the page if it has not been crawled already
			if page not in crawled:
				content = get_page(page)
				
				# If the page returned is a bytes object, try to decode using utf-8
				if type(content) == bytes:
					try:
						content = content.decode("utf-8")
					except:
						content = ""
				if page == seed:
					flag = True
				
				# Retrieve all the links from the page, add these to tocrawl list if they are not already added
				newlinks = get_all_links(content,flag)
				print("Number of newlinks: ", len(newlinks))
				union(tocrawl, newlinks)
				crawled.append(page)
				print("Page crawled: ", page)
	return crawled

if __name__ == "__main__":
	result = crawl_web("https://en.wikipedia.org/wiki/Category:Diseases_and_disorders")
	with open('./crawled.csv', "a") as fp:
		wr = csv.writer(fp, dialect= 'excel')
		wr.writerow(result)
	print(result)
