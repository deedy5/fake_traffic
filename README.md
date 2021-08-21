[![Python >= 3.6](https://img.shields.io/badge/python->=3.6-red.svg)](https://www.python.org/downloads/) [![](https://badgen.net/github/release/deedy5/fake_traffic)](https://github.com/deedy5/fake_traffic/releases) [![](https://badge.fury.io/py/fake-traffic.svg)](https://pypi.org/project/fake-traffic) 
# fake_traffic
Imitating an Internet user by mimicking popular web traffic (internet traffic generator).

### How it works:
```python
1. you specify the country and language,
while True:
  2. from google trends script gets a list of popular keywords that in real time are searched 
     by people on google search in the specified country in the specified language,
  threads:
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
---
### Advanced usage
```python
from fake_traffic import fake_traffic

fake_traffic(country='US', language='en-US', threads=2, min_wait=1, max_wait=5, debug=True)
    """
    Imitating an Internet user by mimicking popular web traffic (internet traffic generator).
    
    country = country code ISO 3166-1 Alpha-2 code (https://www.iso.org/obp/ui/),
    language = country-language code ISO-639 and ISO-3166 (https://www.fincher.org/Utilities/CountryLanguageList.shtml),
    threads = number of threads (defaults to 1),
    min_wait = minimal delay between requests (defaults to 1),
    max_wait = maximum delay between requests (defaults to 30),
    debug = if True, then print the details of the requests (defaults to False).
    """
```
---
### Example
Mimic traffic of a user located in Turkey.

Find Turkey country code ([ISO 3166-1 Alpha-2 code](https://www.iso.org/obp/ui/)):</br>
  - country = "TR" </br>

Find Turkey country-language code ([ISO-639 and ISO-3166](https://www.fincher.org/Utilities/CountryLanguageList.shtml)): </br>
  - english  "en-TR", </br>
  - kurdish  "ku-TR", </br>
  - turkish  "tr-TR". </br>

Starting work in two threads:
  - threads=2
```python
from fake_traffic import fake_traffic

fake_traffic(country="TR", language="ku-TR", threads=2)
```
### Other examples
Country   | Language  | Function                                     |
----------|---------- | ---------------------------------------------|
Australia | English   | fake_traffic(country="AU", language="en-AU") |
Brazil    | English   | fake_traffic(country="BR", language="en-BR") |
Brazil    | Portuguese| fake_traffic(country="BR", language="pt-BR") |
Canada    | English   | fake_traffic(country="CA", language="en-CA") |
Canada    | French    | fake_traffic(country="CA", language="fr-CA") |
Canada    | Mohawk    | fake_traffic(country="CA", language="moh-CA")|
Chile     | English   | fake_traffic(country="CL", language="en-CL"  |
Chile     | Mapuche   | fake_traffic(country="CL", language="arn-CL" |
Chile     | Spanish   | fake_traffic(country="CL", language="en-CL"  |
France    | Algeria Arabic | fake_traffic(country="FR", language="ar-DZ") |
France    | Breton    | fake_traffic(country="FR", language="br-FR") |
France    | French    | fake_traffic(country="FR", language="fr-FR") |
Germany   | Syria Arabic | fake_traffic(country="DE", language="ar-SY") |
Germany   | Kenya Swahili | fake_traffic(country="DE", language="sw-KE") |
Germany   | Colognian | fake_traffic(country="DE", language="ksh-DE")|
Germany   | English   | fake_traffic(country="DE", language="en-DE") |
Germany   | German    | fake_traffic(country="DE", language="de-DE") |
Hong Kong | Chinese   | fake_traffic(country="HK", language="zh-HK") |
Hong Kong | English   | fake_traffic(country="HK", language="en-HK") |
India     | English   | fake_traffic(country="IN", language="en-IN") |
India     | Hindi     | fake_traffic(country="IN", language="hi-IN") |
India     | Tibetan   | fake_traffic(country="IN", language="bo-IN") |
Italy     | English   | fake_traffic(country="IT", language="en-IT") |
Italy     | German    | fake_traffic(country="IT", language="de-IT") |
Italy     | Italian   | fake_traffic(country="IT", language="it-IT") |
Kuwait    | Arabic    | fake_traffic(country="KW", language="ar-KW") |
Japan     | English   | fake_traffic(country="JP", language="en-JP") |
Japan     | Japanese  | fake_traffic(country="JP", language="ja-JP") |
Japan     | North Korea	Korean   | fake_traffic(country="JP", language="ko-KP") |
Mexico    | English   | fake_traffic(country="MX", language="en-MX") |
Mexico    | Spanish   | fake_traffic(country="MX", language="es-MX") |
Poland    | English   | fake_traffic(country="PL", language="en-PL") |
Poland    | Israel Hebrew    | fake_traffic(country="PL", language="he-IL") |
Poland    | Polish    | fake_traffic(country="PL", language="pl-PL") |
Russia    | English   | fake_traffic(country="RU", language="en-RU") |
Russia    | Romania Romanian  | fake_traffic(country="RU", language="ro-RO") |
Russia    | Russian   | fake_traffic(country="RU", language="ru-RU") |
Sweden    | Russia Bashkir   | fake_traffic(country="SE", language="ba-RU") |
Sweden    | English   | fake_traffic(country="SE", language="en-SE") |
Sweden    | Northern Sami   | fake_traffic(country="SE", language="se-SE") |
Sweden    | Swedish   | fake_traffic(country="SE", language="sv-SE") |
United Arab Emirates | Arabic | fake_traffic(country="AE", language="ar-AE") |
United Kingdom | South Sudan	Arabic | fake_traffic(country="GB", language="ar-SS") |
United Kingdom | Afghanistan	Pashto | fake_traffic(country="GB", language="ps-AF") |
United Kingdom | English   | fake_traffic(country="GB", language="en-GB") |
United Kingdom | Scottish Gaelic   | fake_traffic(country="GB", language="gd-GB") |
United States  | Oman Arabic    | fake_traffic(country="US", language="ar-OM"   |
United States  | Cherokee  | fake_traffic(country="US", language="chr-US") |
United States  | English   | fake_traffic(country="US", language="en-US") |
United States  | Israel Hebrew   | fake_traffic(country="US", language="he-IL") |
United States  | Russian   | fake_traffic(country="US", language="ru-RU") |




