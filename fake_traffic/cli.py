import argparse

from fake_traffic import fake_traffic


parser = argparse.ArgumentParser(
    description="fake_traffic. Imitating an Internet user by mimicking popular web traffic (internet traffic generator)."
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
    "-ca",
    "--category",
    default="h",
    help="default=h. Variants: 'all' (all), 'b' (business), 'e' (entertainment), 'm' (health), 's' (sports), 't' (sci/tech), 'h' (top stories)",
    choices=["all", "b", "e", "m", "s", "t", "h"],
    required=False,
)
parser.add_argument(
    "-t", "--threads", default=2, help="default=2. Number of threads.", required=False
)
parser.add_argument(
    "-min_w",
    "--min_wait",
    default=1,
    help="default=1. Minimum wait time between requests.",
    required=False,
)
parser.add_argument(
    "-max_w",
    "--max_wait",
    default=60,
    help="default=60. Maximum wait time between requests.",
    required=False,
)
parser.add_argument(
    "-d", "--debug", action="store_true", help="Print debug information(requests)", required=False
)
args = parser.parse_args()

country = args.country.upper()
language_split = args.language.split("-")
language = f"{language_split[0]}-{language_split[1].upper()}"

fake_traffic(
    country=country,
    language=language,
    category=args.category,
    threads=args.threads,
    min_wait=args.min_wait,
    max_wait=args.max_wait,
    debug=args.debug,
)
