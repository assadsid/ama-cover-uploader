import requests
from my_config import facebook_config

page_id = facebook_config.PAGE_ID
access_token = facebook_config.ACCESS_TOKEN

url = f"https://graph.facebook.com/v18.0/{page_id}?fields=tasks&access_token={access_token}"
res = requests.get(url)
print(res.json())
