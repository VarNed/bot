import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from vk_api import VkUpload
import datetime
from towns import towns
import requests
import bs4


TOKEN = '5dcb58237536c05ade911b2a585b63324dc52e638e1f909aaba639eb2f77c5c308dad8bebafc6916b1a16'


vk = vk_api.VkApi(token=TOKEN)
longpoll = VkBotLongPoll(vk, 204049974)
upload = VkUpload(vk)
session = requests.Session()


def send_messages(id, text, attr=''):
    random_id = random.randint(0,1000000)
    if not attr:
        vk.method('messages.send', {'chat_id': id, 'message': text, 'random_id': random_id})
    else:
        vk.method('messages.send', {'chat_id': id, 'message': text, 'random_id': random_id, 'attachment': attr})


def _get_user_name(self, user_id):
    request = requests.get("https://vk.com/id" + str(user_id))
    bs = bs4.BeautifulSoup(request.text, "html.parser")
    user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])
    return user_name.split()[0]


def t_d(chat_id, msg):
    try:
        date1 = msg.lower()[16:]
        if date1.lower() == "лета" or date1.lower() == "лето":
            if 5 < datetime.date.today().month < 9:
                send_messages(chat_id, f'Уже лето!')
                date1 = datetime.date.today()
            elif datetime.date.today().month >= 9:
                d = datetime.date.today().year + 1
                date1 = datetime.date(d, 6, 1)
            else:
                d = datetime.date.today().year
                date1 = datetime.date(d, 6, 1)
        elif date1.lower() == "весны" or date1.lower() == "весна":
            if 2 < datetime.date.today().month < 6:
                send_messages(chat_id, f'Уже весна!')
                date1 = datetime.date.today()
            elif datetime.date.today().month >= 6:
                d = datetime.date.today().year + 1
                date1 = datetime.date(d, 3, 1)
            else:
                d = datetime.date.today().year
                date1 = datetime.date(d, 3, 1)
        elif date1.lower() == "осень" or date1.lower() == "осени":
            if 8 < datetime.date.today().month < 12:
                send_messages(chat_id, f'Уже осень!')
                date1 = datetime.date.today()
            elif datetime.date.today().month >= 12:
                d = datetime.date.today().year + 1
                date1 = datetime.date(d, 9, 1)
            else:
                d = datetime.date.today().year
                date1 = datetime.date(d, 9, 1)
        elif date1.lower() == "зима" or date1.lower() == "зимы":
            if (datetime.date.today().month < 3) or (datetime.date.today().month == 12):
                send_messages(chat_id, f'Уже зима!')
                date1 = datetime.date.today()
            else:
                d = datetime.date.today().year
                date1 = datetime.date(d, 12, 1)
        elif date1.lower() == "нового года" or date1.lower() == "новый год":
            pass
        else:
            date1 = [int(x) for x in date1.split('.')]
            date1 = datetime.date(date1[-1], date1[-2], date1[0])
        cur_date = datetime.date.today()
        delta = date1 - cur_date
        send_messages(chat_id, f'Вам осталось ждать: {delta.days} дней')
    except ValueError:
        send_messages(chat_id, f'Х')
        send_messages(chat_id, f'Неподходящий формат =(( введите дату в формате дд.мм.гггг')
    except TypeError:
        send_messages(chat_id, f'Ошибка типа')


def abirgame(chat_id, word):
    if word.lower() == 'ценок':
        return False
    else:
        send_messages(chat_id, word[::-1])
        return True


def goroda(chat_id, text, raund1, word_bef):
    if raund1 >= 15:
        send_messages(chat_id, f'Победа!')
        return [False, 1, word_bef]
    if not set(text) & set('ауеоэыяию'):
        send_messages(chat_id, f'Такого слова нет! Как вам не стыдно =((')
        return [False, 1, word_bef]
    if text in cur_towns:
        send_messages(chat_id, f'Ошибка! Ваше слово уже называли. Вы проиграли =((')
        return [False, 1, word_bef]
    cur_towns.append(text)
    if word_bef != '' and text[0].lower() != word_bef[-1]:
        send_messages(chat_id, f'Ошибка! Ваше слово не подходит для {word_bef} Вы проиграли =((')
        return [False, 1, word_bef]
    else:
        raund1 += 1
        if text[-1] == 'ь':
            text += text[-2]
        town = list(filter(lambda word: word[0] == text[-1].upper(), towns))
        town = list(filter(lambda word: word not in cur_towns, town))
        cur_towns.append(town[0])
        send_messages(chat_id, town[0])
        return [True, raund1, town[0]]


def know_nomber(chat_id, text, num, knownumTrue, raund):
    if text == num:
        send_messages(chat_id, 'Верно! Победа =)) С ' + str(raund) + " попытки")
        return [False, 1]
    elif text < num:
        send_messages(chat_id, 'Больше бери!')
        raund += 1
    else:
        send_messages(chat_id, 'Много! Уменьшай')
        raund += 1
    return knownumTrue, raund


koms = f'Команды - перечень команд\nПрогноз - прогноз на день\nУгадайка - игра про угадывание чисел от 1 до 100\nГорода - игра в города' \
       f'\nАбырвалг - слова наоборот\nПосчитай - выводит значение выражения\nСейчас - дата и время' \
       f'\nСколько дней до дд.мм.гггг - выводит сколько дней до (кроме дд.мм.гггг можно узнать сколько дней до лета, весны, зимы или осени)' \
       f''
knownumTrue, gorodaTrue, abirTrue = False, False, False
raund, raund1 = 0, 0
word_b = ''
cur_towns = []
futurum = ['Вас ждет хороший день =)) ', 'Остерегайтесь кирпичей, летящих на голову', 'Спокойный скучный день, не отчаивайтесь',
           'День готовит вам много сюрпризов', 'Вы готовите много сюрпризов дню', 'Сегодня вас ожидает совершенно новое открытие',
           'Приложив должные усилия, вы сумеете решить множество давних проблем', 'Поберегите свое здоровье, отдыхотдыхотдых',
           'Полезный день']
global num
image_urls = ['https://images.unsplash.com/photo-1604699229817-27301bdfed68?ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTd8fGhhcHB5fGVufDB8fDB8fA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=60',
              'https://images.unsplash.com/photo-1498673394965-85cb14905c89?ixid=MnwxMjA3fDB8MHxzZWFyY2h8MjV8fGhhcHB5fGVufDB8fDB8fA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=60',
              'https://images.unsplash.com/photo-1513151233558-d860c5398176?ixid=MnwxMjA3fDB8MHxzZWFyY2h8NjR8fGhhcHB5fGVufDB8fDB8fA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=60',
              'https://images.unsplash.com/photo-1486485764572-92b96f21882a?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTAyfHxoYXBweXxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=400&q=60',
              'https://images.unsplash.com/photo-1601011850287-43e30b7db748?ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTYzfHxoYXBweXxlbnwwfHwwfHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=60',
              'https://images.unsplash.com/photo-1559740451-b895701fa4b5?ixid=MnwxMjA3fDB8MHxzZWFyY2h8MjQ2fHxoYXBweXxlbnwwfHwwfHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=60']

im_uri = ['https://images.unsplash.com/photo-1509909756405-be0199881695?ixid=MnwxMjA3fDB8MHxzZWFyY2h8M3x8aGFwcHl8ZW58MHx8MHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=60',
          'https://images.unsplash.com/photo-1509723169456-6eab9d45c612?ixid=MnwxMjA3fDB8MHxzZWFyY2h8ODF8fGFkdmVudHVyZXN8ZW58MHx8MHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=60',
          'https://images.unsplash.com/photo-1516571507564-ccfe0e735a7d?ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTIyfHxhZHZlbnR1cmVzfGVufDB8fDB8fA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=60',
          'https://images.unsplash.com/photo-1590797193025-07078d8de52d?ixid=MnwxMjA3fDB8MHxzZWFyY2h8NDF8fGNhbG1uZXNzfGVufDB8fDB8fA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=60',
          'https://images.unsplash.com/photo-1550007334-c5a59216c7b8?ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mzh8fGNhbG1uZXNzfGVufDB8fDB8fA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=60',
          'https://images.unsplash.com/photo-1596823878695-b4b5ee828913?ixid=MnwxMjA3fDB8MHxzZWFyY2h8NDl8fGNhbG1uZXNzfGVufDB8fDB8fA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=60',
          'https://images.unsplash.com/photo-1551364934-67b19db1e754?ixid=MnwxMjA3fDB8MHxzZWFyY2h8ODh8fGNhbG1uZXNzfGVufDB8fDB8fA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=60']

for event in longpoll.listen():
    print(event.type)
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.from_chat:
            chat_id = event.chat_id
            msg = event.object.message["text"].lower()
            bad_words = ['лень', "тоска", "уныние"]
            if msg == "привет":
                send_messages(chat_id, "Приветик")
            try:
                dey = event.message.action['type']
                invite_id = event.message.action['member_id']
            except:
                dey = ''
                invite_id = -100
            if dey == 'chat_invite_user':
                send_messages(chat_id, f"Приветик, @id{invite_id}!")
            elif set(msg.split()) & set(bad_words):
                send_messages(chat_id, 'не надо так =((')
            elif msg.lower() == "команды":
                attachments = []
                image_url = random.choice(image_urls)
                image = session.get(image_url, stream=True)
                photo = upload.photo_messages(photos=image.raw)[0]
                attachments.append(
                    'photo{}_{}'.format(photo['owner_id'], photo['id'])
                )
                send_messages(chat_id, koms, ','.join(attachments))
            elif msg.lower() == "грустно":
                send_messages(chat_id, f'Все будет хорошо =))')
            elif msg.lower() == "весело":
                send_messages(chat_id, f'Так держать! Полный вперед! На аборда-аж!')
            elif msg.lower() == "угадайка":
                send_messages(chat_id, f'Угадайка. Поехали')
                num = random.randint(1, 100)
                raund = 1
                knownumTrue = True
            elif knownumTrue and msg.isdigit():
                knownumTrue, raund = know_nomber(chat_id, int(msg), num, knownumTrue, raund)
            elif msg.lower() == "прогноз":
                attachments = []
                image_url = random.choice(im_uri)
                image = session.get(image_url, stream=True)
                photo = upload.photo_messages(photos=image.raw)[0]
                attachments.append(
                    'photo{}_{}'.format(photo['owner_id'], photo['id'])
                )
                send_messages(chat_id,  random.choice(futurum), ','.join(attachments))
            elif msg.lower() == "города":
                raund1 = 1
                gorodaTrue = True
                send_messages(chat_id, f'Города... Съезжаемся. Начинайте с "Мой город это - ...". Ваш ход =))')
                cur_towns = []
                word_b = ''
            elif msg.lower().count("сколько дней до"):
                t_d(chat_id, msg)
            elif msg.lower().count('мой город это - ') and gorodaTrue:
                t = msg[16:]
                gorodaTrue, raund1, word_b = goroda(chat_id, t, raund1, word_b)
            elif msg.lower() == "абырвалг":
                abirTrue = True
                send_messages(chat_id, f'Время пришельцев! Торобоан аволс мешип\n *ценок - конец')
            elif abirTrue:
                abirTrue = abirgame(chat_id, msg)
            elif msg.lower() == "сейчас":
                send_messages(chat_id, str(datetime.datetime.today().strftime("время: %H:%M:%S дата: %d.%m.%Y")))
            elif msg.lower().count('посчитай'):
                msg = msg[9:]
                send_messages(chat_id, f'Будет - {eval(msg)}')
