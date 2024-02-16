[![Python >= 3.8](https://img.shields.io/badge/python->=3.6-red.svg)](https://www.python.org/downloads/) [![](https://badgen.net/github/release/deedy5/fake_traffic)](https://github.com/deedy5/fake_traffic/releases) [![](https://badge.fury.io/py/fake-traffic.svg)](https://pypi.org/project/fake-traffic) 
# fake_traffic
Imitating an Internet user by mimicking popular web traffic (internet traffic generator).

---
### Install

```python3
pip install -U fake_traffic
```

⚠️ When FakeTraffic runs for the first time, playwright dowloads the chromium browser under the hood, which takes some time.

---
### CLI version
```python3
fake_traffic -h
```
CLI examples:
```python3
# user located in Turkey, who speaks Kurdish and is interested in hot stories
fake_traffic -c tr -l ku-tr -ca h
# user located in Brazil, who speaks Portuguese and is interested in sports
fake_traffic -c br -l pt-br -ca s
# save logs into 'fake_traffic.log'
fake_traffic -c ru -l ru-ru -ca s -lf
# define wait times between requests
fake_traffic -c fr -l fr-fr -ca b -min_w 1 -max_w 100 -lf
# use none-headless mode
fake_traffic -c en -l en-us -ca t -nh -lf
```
---
### Simple usage
```python3
from fake_traffic import FakeTraffic

FakeTraffic(country='US', language='en-US").crawl()
```
---
### Advanced usage
```python3
from fake_traffic import FakeTraffic

ft = FakeTraffic(country='US', language='en-US', category='h', min_wait=1, max_wait=5, headless=True)
    """ Imitating an Internet user by mimicking popular web traffic (internet traffic generator).    
    country = country code ISO 3166-1 Alpha-2 code (https://www.iso.org/obp/ui/),
    language = country-language code ISO-639 and ISO-3166 (https://www.fincher.org/Utilities/CountryLanguageList.shtml),
    category = сategory of interest of a user (defaults to 'h'):
               'all' (all), 'b' (business), 'e' (entertainment), 
               'm' (health), 's' (sports), 't' (sci/tech), 'h' (top stories);
    min_wait = minimal delay between requests (defaults to 1),
    max_wait = maximum delay between requests (defaults to 10),
    headless = True/False (defaults to True).
    """
ft.crawl()
```
---
### Example
Mimic traffic of a user located in Turkey, who speaks Kurdish and is interested in hot stories

Find Turkey country code ([ISO 3166-1 Alpha-2 code](https://www.iso.org/obp/ui/)):</br>
  - country = "TR" </br>

Find Turkey country-language code ([ISO-639 and ISO-3166](https://www.fincher.org/Utilities/CountryLanguageList.shtml)): </br>
  - english  "en-TR", </br>
  - kurdish  "ku-TR", </br>
  - turkish  "tr-TR". </br>

Set the category ('h', because the user in the example is interested in hot stories):
  - category = 'h'

Starting in none-headless mode:
  - headless=False
```python3
from fake_traffic import FakeTraffic

ft = FakeTraffic(country="TR", language="ku-TR", category='h', headless=False)
ft.crawl()
```
P.S. you can select language from other country. 
For example, such combinations are also correct:
```python3
FakeTraffic(country="TR", language="ar-TR").crawl()
FakeTraffic(country="US", language="he-IL").crawl()
FakeTraffic(country="DE", language="hi-IN").crawl()
```
---
### Other examples
Country   | Language  | Function                                     |
----------|---------- | ---------------------------------------------|
France    | French    | `FakeTraffic(country="FR", language="fr-FR")` |
Germany   | German    | `FakeTraffic(country="DE", language="de-DE", category='b')` |
India     | English   | `FakeTraffic(country="IN", language="en-IN", category='all')` |
India     | Hindi     | `FakeTraffic(country="IN", language="hi-IN", max_wait=10)` |
Russia    | English   | `FakeTraffic(country="RU", language="en-US", category='b', headless=False)` |
Russia    | Russian   | `FakeTraffic(country="RU", language="ru-RU", min_wait=0.5, max_wait=3)` |
Brazil | Portuguese | `FakeTraffic(country="BR", language="pt-BR", category='s', threads=2,  max_wait=60)` |
United Kingdom | English   | `FakeTraffic(country="GB", language="en-GB")` |
United States  | English   | `FakeTraffic(country="US", language="en-US", min_wait=60, max_wait=300)` |
United States  | Hebrew Israel   | `FakeTraffic(country="US", language="he-IL")` |

