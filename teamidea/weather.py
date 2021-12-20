import requests
from datetime import date, datetime


APPID = '5654307fe8aead8863b821302a4ef5d9'
UNITS = 'metric'
LAT = 59.9854
LON = 30.3008
EXCLUDES = 'current,minutely,hourly,alerts'


# Запрос на получение суточного прогноза на 7 дней
# LAT, LON - ширина и долгота ст. метро "Черная речка", СПб
def getForecast(lat: float, lon: float, exclude: str = EXCLUDES, appid: str = APPID, units: str = UNITS) -> dict:
    return requests.get('https://api.openweathermap.org/data/2.5/onecall', params=locals()).json()


def parseForecast(forecast: dict) -> list[dict]:
    parse = []

    # Для каждого дня в прогнозе считаем разницу температур и продолжительность дня
    for day in forecast['daily']:
        parse.append({
            'day': date.fromtimestamp(float(day['dt'])).strftime("%d %b %Y"),
            'temp_diff': round(abs(float(day['feels_like']['night']) - float(day['temp']['night'])), 1),
            'daylight': float(day['sunset']) - float(day['sunrise'])
        })

    return parse


def getResult(parse: list[dict]) -> tuple[dict]:
    answer1 = {
        'day': '',
        'min_temp_diff': 99.9
    }
    
    # Поиск минимальной разницы
    for day in parse:
        if day['temp_diff'] < answer1['min_temp_diff']:
            answer1 = {
                'day': day['day'],
                'min_temp_diff': day['temp_diff']
            }

    answer2 = {
        'day': '',
        'max_daylight': 0
    }

    # Поиск максимальной продолжительности
    for i, day in enumerate(parse):
        # По условию за ближайшие 5 дней
        if i >= 5:
            break
        
        if day['daylight'] > answer2['max_daylight']:
            answer2 = {
                'day': day['day'],
                'max_daylight': day['daylight']
            }

    answer2['max_daylight'] = datetime.utcfromtimestamp(answer2['max_daylight']).strftime('%H:%M:%S')

    return answer1, answer2


if __name__ == '__main__':
    forecast = getForecast(lat=LAT, lon=LON)
    parse = parseForecast(forecast)
    answer1, answer2 = getResult(parse)

    print('День, с минимальной разницей "ощущаемой" и фактической температуры ночью:')
    print(answer1['day'], '(Разница: ' + str(answer1['min_temp_diff']) + ')\n')

    print('Максимальная продолжительность светового дня за ближайшие 5 дней:')
    print(answer2['max_daylight'], '(' + answer2['day'] + ')')
