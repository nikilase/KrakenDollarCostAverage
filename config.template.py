# This defines the schedule for how often the script will buy coins in a cron type of way
from apscheduler_classes import CronSchedule

schedule = CronSchedule(hour="18", minute="00")

# Insert your API Key and Secret Key here, but never share it with anyone
API_KEY = "API_KEY"
SECRET_KEY = "SECRET_KEY"

# This is your base fiat currency
BASE_CURRENCY = "ZEUR"
BASE_CURRENCY_SYMBOL = "€"

# List of buys that will get executed on each scheduled run
DCA = [
    {"pair": "XXBTZEUR", "amount_worth": 10, "symbol": "BTC"},
    {"pair": "XETHZEUR", "amount_worth": 10, "symbol": "ETH"},
]
