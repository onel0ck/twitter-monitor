README для twitter_monitor.py
Установка
bashCopypip install requests
Настройка

Откройте twitter_monitor.py
Заполните данные:

pythonCopySMS_LOGIN = 'ваш_логин_smsc'
SMS_PASSWORD = 'ваш_пароль_smsc'
SMS_PHONE = 'ваш_номер'

PROXIES = [
    "http://login:password@ip:port",
    # добавьте несколько прокси для ротации
]
Запуск
bashCopypython twitter_monitor.py
Логи

Все действия записываются в twitter_monitor.log
Дублируются в консоль
При ошибках отправляется SMS уведомление

Функционал

Мониторит твиты @mcuban каждую минуту
Использует ротацию прокси
Отправляет SMS при новом твите
Автоматически получает guest token
