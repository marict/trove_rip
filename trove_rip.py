import re
import requests
import os
import tqdm
import sys
from bs4 import BeautifulSoup

def write_images(site):
    print("Writing images for site: {}".format(site))
    storage_dir = site.split('/')[-2]
    if not os.path.exists(storage_dir):
        os.mkdir(storage_dir)

    response = requests.get(site)
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = [x.get('href') for x in soup.find_all('a')]

    for url in tqdm.tqdm(urls,unit="link"):
        if url == "./Bandit%201.png":
            import pdb; pdb.set_trace()
            
        filename = re.search(r'.+[.](jpg|gif|png)$', url)
        if not filename:
            print("Regex didn't match with the url: {}".format(url))
            continue
        with open(storage_dir + '/' + filename.group(0), 'wb') as f:
            print("\tWriting: {}".format(filename.group(0)))
            if 'http' not in url:
                # sometimes an image source can be relative 
                # if it is provide the base url which also happens 
                # to be the site variable atm. 
                url = '{}{}'.format(site, url)
            response = requests.get(url)
            f.write(response.content)

args = sys.argv
if args[1] is not None:
    site = args[1]
    import pdb; pdb.set_trace()
else:
    # Set default here
    site = "https://thetrove.net/Assets/Map%20Assets/Terrain%20-%20cover/Rubble/"
write_images(site)

print("FINISHED")
