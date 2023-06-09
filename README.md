[![Python >= 3.6](https://img.shields.io/badge/python->=3.6-red.svg)](https://www.python.org/downloads/) [![](https://badgen.net/github/release/deedy5/fake_traffic)](https://github.com/deedy5/fake_traffic/releases) [![](https://badge.fury.io/py/fake-traffic.svg)](https://pypi.org/project/fake-traffic) 
# fake_traffic
Imitating an Internet user by mimicking popular web traffic (internet traffic generator).

### How it works:
```python3
1. you specify the country, language and category of interests of a user,
while True:
  2. from google trends the script gets a list of popular keywords that are searched in real time 
  on google by people with a given category of interest in a given country in a given language,
  threads:
    3. select a random trend, take from there the keywords and urls of related articles,
    4. the selected keywords are searched on google and duckduckgo, the found urls are added 
       to the existing ones,
    5. the script sequentially sends requests to a list of urls,
    6. in each open url, recursive queries to random links are performed to a random depth (1-5).
```
---
### Install

```python3
pip install -U fake_traffic
```
---
### CLI version
```python3
fake_traffic -h
```
CLI examples:
```python3
# user located in Turkey, who speaks Kurdish and is interested in hot stories
fake_traffic -c tr -l ku-tr -ca h -d
# user located in Brazil, who speaks Portuguese and is interested in sports
fake_traffic -c br -l pt-br -ca s -d

```
---
### Simple usage
```python3
from fake_traffic import fake_traffic

fake_traffic(country='US', language='en-US")
```
---
### Advanced usage
```python3
from fake_traffic import fake_traffic

fake_traffic(country='US', language='en-US', category='h', threads=2, min_wait=1, max_wait=5, debug=True)
    """ Imitating an Internet user by mimicking popular web traffic (internet traffic generator).    
    country = country code ISO 3166-1 Alpha-2 code (https://www.iso.org/obp/ui/),
    language = country-language code ISO-639 and ISO-3166 (https://www.fincher.org/Utilities/CountryLanguageList.shtml),
    category = сategory of interest of a user (defaults to 'h'):
               'all' (all), 'b' (business), 'e' (entertainment), 
               'm' (health), 's' (sports), 't' (sci/tech), 'h' (top stories);
    threads = number of threads (defaults to 2),
    min_wait = minimal delay between requests (defaults to 1),
    max_wait = maximum delay between requests (defaults to 60),
    debug = if True, then print the details of the requests (defaults to False).
    """
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

Starting work in two threads:
  - threads=2
```python3
from fake_traffic import fake_traffic

fake_traffic(country="TR", language="ku-TR", category='h', threads=2)
```
P.S. you can select language from other country. 
For example, such combinations are also correct:
```python3
fake_traffic(country="TR", language="ar-TR")
fake_traffic(country="US", language="he-IL")
fake_traffic(country="DE", language="hi-IN")
```
---
### Other examples
Country   | Language  | Function                                     |
----------|---------- | ---------------------------------------------|
France    | French    | fake_traffic(country="FR", language="fr-FR") |
Germany   | German    | fake_traffic(country="DE", language="de-DE", category='b') |
India     | English   | fake_traffic(country="IN", language="en-IN", category='all') |
India     | Hindi     | fake_traffic(country="IN", language="hi-IN", max_wait=10) |
Russia    | English   | fake_traffic(country="RU", language="en-US", category='b', threads=3, debug=True) |
Russia    | Russian   | fake_traffic(country="RU", language="ru-RU", min_wait=0.5, max_wait=3, threads=5) |
Brazil | Portuguese | fake_traffic(country="BR", language="pt-BR", category='s', threads=2,  max_wait=60, debug=True) |
United Kingdom | English   | fake_traffic(country="GB", language="en-GB") |
United States  | English   | fake_traffic(country="US", language="en-US", min_wait=60, max_wait=300) |
United States  | Hebrew Israel   | fake_traffic(country="US", language="he-IL") |

