[![Python >= 3.6](https://img.shields.io/badge/python->=3.6-red.svg)](https://www.python.org/downloads/) [![](https://badgen.net/github/release/deedy5/fake_traffic)](https://github.com/deedy5/fake_traffic/releases) [![](https://badge.fury.io/py/fake-traffic.svg)](https://pypi.org/project/fake-traffic) 
# fake_traffic
Imitating an Internet user by mimicking popular web traffic

### How it works:
```python
1. you specify the country and language,
while True:
  2. from google trends script gets a list of popular keywords that in real time are searched 
     by people on google search in the specified country in the specified language,
  3. select a random trend, take from there the keywords and urls of related articles,
  4. the selected keywords are searched on google and duckduckgo, the found urls are added 
     to the existing ones,
  5. the script sequentially sends requests to a list of urls,
  6. in each open url, recursive queries to random links are performed to a random depth (1-5).
```

### Install

```python
pip install -U fake_traffic
```

### Dependencies
```python
lxml
requests
google_trends
duckduckgo_search
google_searching
```
---
### Simple usage
```python
from fake_traffic import fake_traffic

fake_traffic(country='US', language='en-US")
```
