#!/usr/bin/env python3

'''
weather_app.py - Program that takes a city name and returns weather infos.
'''

import json
import sys
import time
from datetime import datetime as dt
from progress.bar import FillingCirclesBar
from colorama import Fore, Style
import colorama
import requests


API_KEY = 'your_api_key'
colorama.init(autoreset=True)


def weather(city):
    '''Function to scrape weather infos for a given city name.'''

    if ' ' in city:
        city = city.replace(' ', '+')
    elif '-' in city:
        city = city.replace('-', '+')

    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?&q={city}&appid={API_KEY}')

    progress_bar = FillingCirclesBar(f'{Style.BRIGHT}{Fore.YELLOW}Getting Data...{Fore.GREEN}')
    for i in range(100):
        time.sleep(.01)
        progress_bar.next()
    progress_bar.finish()

    json_data = json.loads(response.text)

    return json_data


def main():
    '''Main program.'''

    line = '+' + '-' * 55 + '+'
    if len(sys.argv) < 2:
        print('Usage: ./weather_app.py [city_name]')
    elif len(sys.argv) == 2:
        arg = sys.argv[1]
        print()
        data = weather(arg)

        if data['cod'] != 404:
            print(f'{Style.BRIGHT}{Fore.CYAN}{line}')
            print(f'|\tData Source: https://openweathermap.org/\t|')
            print(f'{Style.BRIGHT}{Fore.CYAN}{line}')

            try:
                country_code = data['sys']['country']
            except KeyError:
                print(f"\tGiven City name '{arg}' not found.")
            else:
                with open('ISO3166-1.alpha2.json') as file_obj:
                    for line in file_obj.readlines():
                        if country_code in line:
                            country = line
                    country = country[6:].strip(': ",').replace('",', '')

                # OpenWeather gives temperature in °K
                # T(°C) = T(°K) - 273.15
                TEMP = data['main']['temp'] - 273.15
                TEMP = round(TEMP, 2)

                sunrise = time.ctime(data['sys']['sunrise'])
                sunset = time.ctime(data['sys']['sunset'])

                now = dt.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

                print(f'\t{Style.BRIGHT}Current Weather Data in {arg.title()}:')
                print(f'\tLast Update: {dt_string}')
                print(f'\tCountry: {country}')
                print(f"\tDescription: {data['weather'][0]['description']}")
                print(f"\tTemperature: {TEMP}°C")
                print(f'\tSunrise: {sunrise}')
                print(f'\tSunset: {sunset}')
        else:
            print(f"\tGiven City name '{arg}' not found.")

        print()
    else:
        print(f"Unknown arguments '{sys.argv[1:]}'")


if __name__ == '__main__':
    main()
