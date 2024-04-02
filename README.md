# Kraken Dollar Cost Average
Simply copy `config.template.py` to file `config.py` and fill in required information.
Then set up a schedule with Windows Task Scheduler / Linux Systemd to start this script at boot.
It will use APScheduler to run the buying Requests at any schedule you might want to define.
