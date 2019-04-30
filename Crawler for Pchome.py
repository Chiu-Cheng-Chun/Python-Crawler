"""
@author: Chiu-Cheng-Chung

*ATTENTION:
1. You can use it at will, but please mark the source if you quote it for commercial use. Thanks~
2. If you have any questions feel free to contact me: craigchiu0619@gmail.com
"""
import requests
import json
import urllib

name = input()#Enter keyword

code = urllib.parse.quote(name.encode('utf8'))#URL encode
i = 1 

for i in range(21): #default ten pages
    a = str(i) #
    index = ('http://ecshweb.pchome.com.tw/search/v3.3/all/results?q='+code+'&page='+a+'&sort=rnk/dc') #search URL

    res = requests.get(index) #REQUEST
    jd = json.loads(res.text) #change to json type

    for item in jd['prods']: #get information
        print(item['name'],item['price'],item['describe']) #print output