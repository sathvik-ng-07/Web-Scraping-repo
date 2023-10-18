from urllib.request import urlopen  # Import the urlopen function from the urllib.request module
from bs4 import BeautifulSoup  # Import BeautifulSoup from the bs4 module
import datetime
import random
import re

# Set the seed for the random number generator based on the current datetime
random.seed()


# Define a function to get all the Wikipedia links from a given article URL
def getLinks(articleUrl):
    # Open the URL and create a BeautifulSoup object
    html = urlopen("http://en.wikipedia.org" + articleUrl)
    bsObj = BeautifulSoup(html, "html.parser")

    # Find the div with id "bodyContent" and get all the 'a' elements with 'href' attributes matching the provided regex
    return bsObj.find("div", {"id": "bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))


# Define a function to get the IP addresses from the revision history page of a Wikipedia article
def getHistoryIPs(pageUrl):
    # Modify the page URL to create the history URL
    pageUrl = pageUrl.replace("/wiki/", "")
    historyUrl = "http://en.wikipedia.org/w/index.php?title=" + pageUrl + "&action=history"
    print("history url is: " + historyUrl)

    # Open the history URL and create a BeautifulSoup object
    html = urlopen(historyUrl)
    bsObj = BeautifulSoup(html, "html.parser")

    # Find all the links with class "mw-anonuserlink" (IP addresses instead of usernames)
    ipAddresses = bsObj.findAll("a", {"class": "mw-anonuserlink"})

    # Create a set to store the unique IP addresses
    addressList = set()

    # Iterate through the IP addresses and add them to the set
    for ipAddress in ipAddresses:
        addressList.add(ipAddress.get_text())

    return addressList


# Start with the initial article URL
links = getLinks("/wiki/Python_(programming_language)")

# Continue until there are no more links to follow
while len(links) > 0:
    for link in links:
        print("-------------------")
        historyIPs = getHistoryIPs(link.attrs["href"])
        for historyIP in historyIPs:
            print(historyIP)

    # Choose a random link to follow next
    newLink = links[random.randint(0, len(links) - 1)].attrs["href"]
    links = getLinks(newLink)

