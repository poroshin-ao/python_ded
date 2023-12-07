from vkbottle import Keyboard, KeyboardButtonColor, Text
from config import admins
from models import get_user_by_id

otmena_keyboard = Keyboard(one_time=True, inline=False).add(Text("Отмена"))

da_net_keyboard = Keyboard(one_time=True, inline=False).add(Text("Да")).row().add(Text("Нет"))

def get_user_keyboard(vk_id):
    keyboard = Keyboard(one_time=True, inline=False)
    keyboard.add(Text("Дед Мороз"))
    data = get_user_by_id(vk_id)
    if data is None:
        keyboard.row().add(Text("Участвую"))
    else:
        keyboard.row().add(Text("Кому дарить"))
        keyboard.row().add(Text("Изменить пожелание"))
        keyboard.row().add(Text("Не участвую"))
    if vk_id in admins:
        keyboard.row().add(Text("Я админ"))

    return keyboard

admin_keyboard = Keyboard(one_time=True, inline=False).add(Text("Посмотреть участников")).row().add(Text("Принес подарок")).row().add(Text("Удалить участника")).row().add(Text("Массовые уведомления")).row().add(Text("Дед мороз"))

mass_keyboard = Keyboard(one_time=True, inline=False).add(Text("Отмена")).row().add(Text("Игра началась")).row().add(Text("Осталось два дня")).row().add(Text("Время вручать подарки"))#.row().add(Text("Дед разносит подарки"))