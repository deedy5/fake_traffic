[![Python >= 3.8](https://img.shields.io/badge/python->=3.8-red.svg)](https://www.python.org/downloads/) [![](https://badgen.net/github/release/deedy5/fake_traffic)](https://github.com/deedy5/fake_traffic/releases) [![](https://badge.fury.io/py/fake-traffic.svg)](https://pypi.org/project/fake-traffic) 
# fake_traffic
Internet traffic generator. Utilizes real-time google search trends by specified parameters.

---
### Install

```python3
pip install -U fake_traffic
```
Install chromium browser with dependencies
```python3
playwright install --with-deps chromium
```

---
### CLI version
```python3
fake_traffic -h
```
CLI examples:
```python3
# user located in Austria, who speaks German, using comma separated keywords.
fake_traffic -c at -l de-at -k "Olympiade, Medaille, Beste Leistung"
# user located in Turkey, who speaks Kurdish, using google trends.
fake_traffic -c tr -l ku-tr
# save logs into 'fake_traffic.log'
fake_traffic -c ru -l ru-ru -lf
# use none-headless mode
fake_traffic -c en -l en-us -nh
# limit the number of tabs in the browser to 2 
fake_traffic -c en -l en-us -t 2
```
---
### Simple usage
```python3
from fake_traffic import FakeTraffic

FakeTraffic(country="US", language="en-US").crawl()
```
---
### Advanced usage
```python3
from fake_traffic import FakeTraffic

ft = FakeTraffic(country="US", language="en-US", category="h", headless=True)
    """Internet traffic generator. Utilizes real-time google search trends by specified parameters.
    country = country code ISO 3166-1 Alpha-2 code (https://www.iso.org/obp/ui/),
    language = country-language code ISO-639 and ISO-3166 (https://www.fincher.org/Utilities/CountryLanguageList.shtml),
    keywords = comma separated queries for Google searches, if not specified, Google trending is used,
    headless = True/False (defaults to True);
    tabs = limit the number of tabs in browser (defaults to 3).
    """
ft.crawl()
```
---
### Example
Using realtime search trends of a user located in Turkey, who speaks Kurdish

Find Turkey country code ([ISO 3166-1 Alpha-2 code](https://www.iso.org/obp/ui/)):</br>
  - country = "TR" </br>

Find Turkey country-language code ([ISO-639 and ISO-3166](https://www.fincher.org/Utilities/CountryLanguageList.shtml)): </br>
  - english  "en-TR", </br>
  - kurdish  "ku-TR", </br>
  - turkish  "tr-TR". </br>

Starting in none-headless mode:
  - headless=False
```python3
from fake_traffic import FakeTraffic

ft = FakeTraffic(country="TR", language="ku-TR", keywords=None, headless=False)
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
Germany   | German    | `FakeTraffic(country="DE", language="de-DE", keywords="Audi")` |
India     | English   | `FakeTraffic(country="IN", language="en-IN")` |
India     | Hindi     | `FakeTraffic(country="IN", language="hi-IN")` |
Russia    | English   | `FakeTraffic(country="RU", language="en-US", headless=False)` |
Russia    | Russian   | `FakeTraffic(country="RU", language="ru-RU")` |
Brazil | Portuguese | `FakeTraffic(country="BR", language="pt-BR")` |
United Kingdom | English   | `FakeTraffic(country="GB", language="en-GB")` |
United States  | English   | `FakeTraffic(country="US", language="en-US", tabs=4)` |
United States  | Hebrew Israel   | `FakeTraffic(country="US", language="he-IL")` |

