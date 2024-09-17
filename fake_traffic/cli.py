import argparse
import logging

from .fake_traffic import FakeTraffic


parser = argparse.ArgumentParser(
    description="Internet traffic generator. Utilizes real-time google search trends by specified parameters."
)
parser.add_argument(
    "-c",
    "--country",
    default="US",
    help="default=US. ISO 3166-2 code. Examples:FR, RU, CN, ES. Link: https://en.wikipedia.org/wiki/ISO_3166-2",
    required=False,
)
parser.add_argument(
    "-l",
    "--language",
    default="en-US",
    help="default=en-US. ISO-639 and ISO-3166 codes. Examples: ru-RU, he-IL, el-GR. Link: https://www.fincher.org/Utilities/CountryLanguageList.shtml",
    required=False,
)
parser.add_argument(
    "-k",
    "--keywords",
    default=None,
    help="default=None. comma separated queries for Google searches, if not specified, Google trending is used",
    required=False,
)
parser.add_argument(
    "-nh",
    "--no-headless",
    dest="headless",
    action="store_false",
    help="Run the browser in non-headless mode",
    required=False,
)
parser.add_argument(
    "-t",
    "--tabs",
    default=3,
    type=int,
    help="Limit the number of tabs in browser. Defaults to 3",
    required=False,
)
parser.add_argument(
    "-lf",
    "--logfile",
    action="store_true",
    help="save the log into 'fake_traffic.log'",
    required=False,
)
args = parser.parse_args()

# logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    force=True,
    handlers=[logging.FileHandler("fake_traffic.log"), logging.StreamHandler()]
    if args.logfile
    else [logging.StreamHandler()],
)

country = args.country.upper()
language_split = args.language.split("-")
language = f"{language_split[0]}-{language_split[1].upper()}"
logging.info(
    f"Run crawl with: {country=}, {language=}, keywords={args.keywords}, headless={args.headless}, tabs={args.tabs}, logfile={args.logfile}"
)


fake_traffic = FakeTraffic(
    country=country,
    language=language,
    keywords=args.keywords,
    headless=args.headless,
    tabs=args.tabs,
)
