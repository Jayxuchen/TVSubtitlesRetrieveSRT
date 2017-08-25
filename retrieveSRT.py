#!/bin/python
import urllib, sys, re, zipfile, os
from bs4 import BeautifulSoup

# Requirements:
# pip install urllib,bs4
# Running on Python 2.7.6

# downloads all subtitles for a season of a TV show
# e.g http://www.tvsubtitles.net/tvshow-32-28.html

# removes all zip files from subtitle directory
def removeZipFiles():
    files = os.listdir("subtitles")
    for theFile in files:
        if theFile.endswith(".zip"):
            os.remove(os.path.join("subtitles",theFile))



# Finds all links in the given url
# Looks for links with the /subtitle-{id}.html pattern
# Downloads zip file containing SRT from tvsubtitles.net/download-{id}.html
# Extracts zip file, placing SRT in the subtitle directory
def getSRT(soup):
    #create subtitle directory
    directory = 'subtitles'
    if not os.path.exists(directory):
        os.makedirs(directory)
    for link in soup.find_all('a', href=True):
        # finds all links to each subtitle download page
        match =re.match('subtitle-(\w*).html',link['href'])
        if match:
            prefix="http://www.tvsubtitles.net/download-"
            suffix=".html"
            # first capture group is the id corresponding to the subtitle
            url = prefix + match.group(1) + suffix
            # moves downloaded zip file to subdirectory
            urllib.urlretrieve(url, "subtitles/" + link['href'] + ".zip")
            # unzips file
            zip_ref = zipfile.ZipFile("subtitles/" + link['href']+ ".zip", 'r')
            # extracts the srt
            zip_ref.extractall("subtitles")
            zip_ref.close()
            print url

#Opens the URL
resp = urllib.urlopen(sys.argv[1],timeout=10)
soup = BeautifulSoup(resp,'html5lib')
getSRT(soup)
removeZipFiles()
