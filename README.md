# HolidayTasks
The UMLS.txt file lists the points about UMLS

The Havoc.txt file lists points about HaVoc

The crawler.py is a Python script that crawles the page https://en.wikipedia.org/wiki/Category:Diseases_and_disorders extracting links from the wikipedia pages that can be reached from this page. After finishing execution, the links are written to a csv file named "Crawled"

The havoc.py is a Python script that collects mesh terms from the files of dataset ctgov2016_2017 and asks user about the information that the user wants. The scripts requests and retrieves that information using HaVoc API and displays it to the user
