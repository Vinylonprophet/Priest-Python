from urllib.request import urlretrieve, urlopen
from bs4 import BeautifulSoup
import os

downloadDirectory = "download"
baseUrl = "https://pythonscraping.com"


def getAbsoluteURL(baseUrl, source):
    if source.startswith("https://www."):
        url = "https://{}".format(source[12:])
    elif source.startswith("https://"):
        url = source
    elif source.startswith("www."):
        url = source[4:]
        url = "https://{}".format(source)
    else:
        url = "{}/{}".format(baseUrl, source)
    if baseUrl not in url:
        return None
    return url


def getDownloadPath(baseUrl, absoluteUrl, downloadDirectory):
    path = absoluteUrl.replace("www.", "")
    path = path.replace(baseUrl, "")
    path = downloadDirectory + path.split("?")[0]
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    return path


html = urlopen("https://pythonscraping.com")
bs = BeautifulSoup(html, "html.parser")
downloadList = bs.findAll(src=True)

for download in downloadList:
    fileUrl = getAbsoluteURL(baseUrl, download["src"])
    print(fileUrl)
    if fileUrl is not None:
        urlretrieve(fileUrl, getDownloadPath(baseUrl, fileUrl, downloadDirectory))
