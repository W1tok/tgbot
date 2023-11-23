import telebot
import requests
from googletrans import Translator


API_KEY_WEATHER = '22931e9c29d71baa5a2e2f10818d8444'
API_KEY_NEWS = 'd0eeb33c50744a348758c750f63f30fb'
bot = telebot.TeleBot('6786523965:AAEK-NVDmwdS5TXPX1M9nX3-yDlHRtiMHGo')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет! Я - бот который будет тебе помогать')


@bot.message_handler(commands=['weather'])
def get_weather(message):
    if len(message.text.split()) > 1:
        city = ' '.join(message.text.split()[1:])
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY_WEATHER}&units=metric'

        response = requests.get(weather_url)
        weather_data = response.json()

        if weather_data['cod'] == '404':
            bot.send_message(message.chat.id, 'Город не найден')
        else:
            description = weather_data['weather'][0]['description']
            temperature = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']

            reply = f'Погода в {city}: {description}\nТемпература: {temperature}°C\nВлажность: {humidity}%'
            bot.send_message(message.chat.id, reply)
    else:
        bot.send_message(message.chat.id, 'Введите команду /weather с названием города')


@bot.message_handler(commands=['news'])
def get_news(message):
    news_url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY_NEWS}'

    response = requests.get(news_url)
    news_data = response.json()

    if news_data['status'] == 'ok':
        articles = news_data['articles']

        for article in articles:
            title = article['title']
            description = article['description']
            url = article['url']

            reply = f'Заголовок: {title}\nОписание: {description}\nСсылка: {url}'

            bot.send_message(message.chat.id, reply)
    else:
        bot.send_message(message.chat.id, 'Не удалось получить новости')


translator = Translator()


@bot.message_handler(commands=['translator'])
def translate_text(message):
    if len(message.text.split()) > 1:
        text = ' '.join(message.text.split()[1:])
        translation = translator.translate(text, dest='en')

        reply = f'Перевод: {translation.text}'
        bot.send_message(message.chat.id, reply)
    else:
        bot.send_message(message.chat.id, 'Введите команду /translator с текстом для перевода')


@bot.message_handler(commands=['valutes'])
def show_exchange_rate(message):
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response = requests.get(url)
    data = response.json()
    rates = {
        'EUR': data['Valute']['EUR']['Value'],
        'USD': data['Valute']['USD']['Value'],
        'CNY': data['Valute']['CNY']['Value']
    }
    reply = "Актуальный курс валют:\n\n"
    reply += f"1 EUR = {rates['EUR']} RUB\n"
    reply += f"1 USD = {rates['USD']} RUB\n"
    reply += f"1 CNY = {rates['CNY']} RUB\n"

    bot.send_message(message.chat.id, reply)


@bot.message_handler(commands=['numbers'])
def numbers(message):
    result = []
    a = None
    b = None
    text = ' '.join(message.text.split(" ")[1:])
    if len(text) == 0:
        bot.send_message(message.chat.id, 'Введите команду /numbers, затем число которое хотите перевести, далее число - систему  счислению в которую вы хотите сделать перевод')
    else:
        text = text.split()
        a = text[0]
        b = text[1]
        a = int(a)
        b = int(b)

        #Перевод
        while a > 0:
            result = [a % b] + result
            a = a // b

        try_result = ""
        for i in result:
            try_result += str(i)

        bot.send_message(message.chat.id, f"Вот переведенное число: {try_result}")


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,"/weather - узнать погоду,")
    bot.send_message(message.chat.id," /translator - перевести текст")
    bot.send_message(message.chat.id," /news - узнать новости")
    bot.send_message(message.chat.id, " /valutes - узнать курс валют")
    bot.send_message(message.chat.id, "/numbers - сделать перевод в сс")
    bot.send_message(message.chat.id, "/start - начать общение")


bot.polling()
