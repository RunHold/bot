import bs4 as bs4
import requests
from bs4 import BeautifulSoup

class VkBot:

    def __init__(self, user_id):
        print("\nСоздан объект бота!")

        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)

        self._COMMANDS = ["ПРИВЕТ", "ПОГОДА", "ВРЕМЯ", "ПОКА", "ОСК"]

    def _get_user_name_from_vk_id(self, user_id):
        request = requests.get("https://vk.com/id"+str(user_id))
        bs = bs4.BeautifulSoup(request.text, "html.parser")

        user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])

        return user_name.split()[0]

    def new_message(self, message):

        # Привет
        if message.upper() == self._COMMANDS[0]:
            return f"Привет-привет, {self._USERNAME}!"

        # Погода
        elif message.upper() == self._COMMANDS[1]:
            return self._get_weather()

        # Время
        elif message.upper() == self._COMMANDS[2]:
            return self._get_time()

        # Пока
        elif message.upper() == self._COMMANDS[3]:
            return f"Пока-пока, {self._USERNAME}!"

        # Оск
        elif message.upper() == self._COMMANDS[4]:
            return f"Ну и пошёл на хуй, {self._USERNAME}!"

        else:
            return "Не понимаю о чем вы..."

    def _get_time(self):
        request = requests.get("https://my-calend.ru/date-and-time-today")
        b = bs4.BeautifulSoup(request.text, "html.parser")
        return self._clean_all_tag_from_str(str(b.select(".page")[0].findAll("h2")[1])).split()[1]

    @staticmethod
    def _clean_all_tag_from_str(string_line):

        """
        Очистка строки stringLine от тэгов и их содержимых
        :param string_line: Очищаемая строка
        :return: очищенная строка
        """

        result = ""
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += i
            else:
                if i == ">":
                    not_skip = True

        return result

    @staticmethod



    def _get_weather(city: str = "simferopol") -> str:
        request = requests.get("https://sinoptik.com.ru/pogoda/-" + str(city))
        soap = BeautifulSoup(request.text, "html.parser")

        # block with temperature
        temperature_block = soap.find('ul', {
            'class': 'weather__article_main_right-table clearfix'
        })

        # columns
        columns_data = temperature_block.find_all('li')

        # night
        night_from = columns_data[0].find('div', {'class': 'table__temp'}).text
        night_to = columns_data[1].find('div', {'class': 'table__temp'}).text

        # morning
        morning_from = columns_data[2].find('div', {'class': 'table__temp'}).text
        morning_to = columns_data[3].find('div', {'class': 'table__temp'}).text

        # day
        day_from = columns_data[4].find('div', {'class': 'table__temp'}).text
        day_to = columns_data[5].find('div', {'class': 'table__temp'}).text

        # evening
        evening_from = columns_data[6].find('div', {'class': 'table__temp'}).text
        evening_to = columns_data[7].find('div', {'class': 'table__temp'}).text

        # result row
        result = 'Ночью: {} {}\n'.format(night_from, night_to)
        result += 'Утром: {} {}\n'.format(morning_from, morning_to)
        result += 'Днем: {} {}\n'.format(day_from, day_to)
        result += 'Вечером: {} {}\n'.format(evening_from, evening_to)

        return result
