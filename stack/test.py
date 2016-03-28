from urllib2 import urlopen
id = 'BJ9O5B1400014AED'

url = "http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/" + id + "/comments/newList?offset=0&limit=30&showLevelThreshold=72&headLi    mit=1&tailLimit=2&callback=getData&ibc=newspc&_=1458939446003"
url = 'http://news.163.com/'
s = urlopen(url).read()
print '==> s <==', s
