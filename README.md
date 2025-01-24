# Twitter Monitor
Monitors X.com accounts for new tweets and sends SMS notifications.

## Installation
```bash
pip install requests
```

## Setup
1. Edit `twitter_monitor.py`:
```python
SMS_LOGIN = 'your_smsc_login'
SMS_PASSWORD = 'your_smsc_password' 
SMS_PHONE = 'your_phone'

PROXIES = [
    "http://login:password@ip:port",
    # add multiple proxies for rotation
]
```

## Usage
```bash
python twitter_monitor.py
```

## Features
- Monitors tweets every minute
- Proxy rotation
- SMS notifications via smsc.ru
- Automatic guest token refresh
- Logging to file and console
- Error notifications via SMS

## Logs
All activity logged to `twitter_monitor.log` and console output

## Requirements
- Python 3.6+
- requests library
- smsc.ru account
- Proxies (recommended)
