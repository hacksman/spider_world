

import requests

res = requests.get("https://www.zcool.com.cn/u/666812/profile")

print(res)
print(res.status_code)
print(res.content)
print(res.text)