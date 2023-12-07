from vkbottle.bot import Bot, Message
from vkbottle import BaseStateGroup
from decorators import *
from keyboards import get_user_keyboard, otmena_keyboard, da_net_keyboard, admin_keyboard, mass_keyboard
from models import get_alluser, set_user, get_user_by_id, delete_user_by_id, set_prefer, delete_prefer_by_id, get_present_by_id, get_prefer_by_id, set_present, get_frompresent_by_id
from models import set_giver, get_giver_by_id, delete_present_by_id
from vkbottle.dispatch.rules.base import StateRule
from config import org_time, format_string, admins
import datetime as dt
from threading import Timer
from config import text_ded_moroz, text_start_jereb, text_priem_podark, text_za_dva_dnya, text_prines_podarok

bot = Bot(token = "vk1.a.UMmiYPg5pzSOYMQ8oXFuj-7-2VktqMAGX15g0bivw7B6JaFBvCuLNj5Kp1tqRybs3qQdakpFkhjzcVco94vbXEZ0_wu-ju0rsogkHEi5ml7_GqYt1nDMlmZieCz1JU9qmsADyk76zyOoq4599Vn11oiwlAFVOnbhSr6UkC2RSy2ep4_Y0Rkazn3dt6RlaFpmz0P7UYQyFwjWieZp1Zplkg")



#######
#userы#
#######

@bot.on.message(Is_lower("Дед Мороз"))
async def start(message: Message):
    text = text_ded_moroz
    if dt.datetime.now() > dt.datetime.strptime(org_time["start_jereb"], format_string):
        user = get_user_by_id(message.from_id)
        if user is None:
            text = text + "\n\nЖеребьёвка уже прошла.\n\nК сожалению, ты не сможешь стать Тайным Дедом Морозом." 
        
    else:
        user = get_user_by_id(message.from_id)
        if user is None:
            text = text + "\n\nНу что, готов ли ты стать Тайным Дедом Морозом?\n\nЕсли готов, то нажимай кнопку \"Участвую\" " 
        else:
            text = text + "\n\nЖеребьёвка ещё не прошла.\n\nУ тебя есть возможность изменить своё пожелание."
            pref = get_prefer_by_id(message.from_id)
            if pref is None:
                text = text + "\n\nУ теюя пока нет пожелания"
            else:
                text = text + "\n\nТвоё пожелание: "+pref[0]
            
    await message.answer(text, keyboard=get_user_keyboard(message.from_id))

@bot.on.message(Is_lower("Участвую"))
async def it_partic(message: Message):
    if dt.datetime.now() > dt.datetime.strptime(org_time["start_jereb"], format_string):
        await message.answer("Жеребьёвка уже прошла.\n\nК сожалению, ты не сможешь поучаствовать", keyboard=get_user_keyboard(message.from_id))
        return
    
    if get_user_by_id(message.from_id) is None:
        user_data = await bot.api.users.get(message.from_id)
        set_user(vk_id= message.from_id, name=user_data[0].first_name, fam=user_data[0].last_name)
        await message.answer("Я знал, что ты сделаешь верный выбор! С этого момента мы вместе будем творить волшебство. Жди весточки от меня, друг✨", keyboard=get_user_keyboard(message.from_id))
    else:
        await message.answer("Ты уже участвуешь✨", keyboard=get_user_keyboard(message.from_id))

class ChangePartic(BaseStateGroup):
    CHANGE_PARTIC = "ChangePartic"
    

@bot.on.message(Is_lower("Не участвую"))
async def it_not_partic(message: Message):
    if not get_user_by_id(message.from_id) is None:
        await bot.state_dispenser.set(message.peer_id, ChangePartic.CHANGE_PARTIC)
        
        if dt.datetime.now() > dt.datetime.strptime(org_time["start_jereb"], format_string):
            await message.answer("Ого, дружок! Может быть ты ошибся с выбором команды? Как же можно отказаться от возможности стать частичкой новогоднего чуда!\n\nПодскажи, ты правда хочешь отказаться от участия в акции Тайного Деда Мороза математиков?\n\nЕсли вы откажетесь сейчас, то тому кому вы дарите подарок будет дарить уже ваш Тайный Дед Мороз.", keyboard=da_net_keyboard)
            return

        await message.answer("Ого, дружок! Может быть ты ошибся с выбором команды? Как же можно отказаться от возможности стать частичкой новогоднего чуда!\n\nПодскажи, ты правда хочешь отказаться от участия в акции Тайного Деда Мороза математиков?", keyboard=da_net_keyboard)
    else:
        await message.answer("Ты не участвовал", keyboard=get_user_keyboard(message.from_id))

@bot.on.message(StateRule(ChangePartic.CHANGE_PARTIC))
async def realy_not_partic(message: Message):
    await bot.state_dispenser.delete(message.peer_id)
    if message.text.lower() == "да":
        if dt.datetime.now() > dt.datetime.strptime(org_time["start_jereb"], format_string):
            to_id = get_present_by_id(message.from_id)[0]
            from_id = get_frompresent_by_id(message.from_id)[0]
            delete_present_by_id(message.from_id)
            delete_present_by_id(from_id)
            set_present(from_id, to_id)
            user = get_user_by_id(to_id)
            try:
                await bot.api.messages.send(user_id=from_id, message = "К сожалению, твой подопечный по некоторым причинам отказался от участия.\n\nТеперь твой подопечный: [id"+str(to_id)+"|"+user[0]+" "+ user[1]+"]", random_id=random.randint(1,1000000))
            except Exception:
                print("Не смог отправить сообщение "+str(from_id))

        delete_user_by_id(message.from_id)
        await message.answer("Я очень опечален этим фактом! Но, надеюсь, ты проведешь этот праздник счастливо — с наступающим!", keyboard=get_user_keyboard(message.from_id))
    else:
        
        await message.answer("Ты не отказался от участия", keyboard=get_user_keyboard(message.from_id))


class ChangePref(BaseStateGroup):
    CHANGE_PREF = "ChangePref"
    
@bot.on.message(Is_lower("Изменить пожелание"))
async def go_change_pref(message: Message):
    if get_user_by_id(message.from_id) is None:
        await message.answer("Ты не участвуешь в Тайном Дед Морозе", keyboard=get_user_keyboard(message.from_id))
        return
    await bot.state_dispenser.set(message.peer_id, ChangePref.CHANGE_PREF)
    await message.answer("Введи своё новое пожелание", keyboard=otmena_keyboard)

@bot.on.message(StateRule(ChangePref.CHANGE_PREF))
async def state_change_pref(message: Message):
    await bot.state_dispenser.delete(message.peer_id)
    if message.text.lower() == "отмена":
        await message.answer("Ты оставил своё желание таким же", keyboard=get_user_keyboard(message.from_id))
        return
    delete_prefer_by_id(message.from_id)
    set_prefer(message.from_id, message.text)

    await message.answer("Теперь ваше желание: \n\n"+ message.text, keyboard=get_user_keyboard(message.from_id))

@bot.on.message(Is_lower("Кому дарить"))
async def gift_user(message: Message):
    if get_user_by_id(message.from_id) is None:
        await message.answer("Ты не участвуешь в Тайном Дед Морозе", keyboard=get_user_keyboard(message.from_id))
        return 
    
    if dt.datetime.now() < dt.datetime.strptime(org_time["start_jereb"], format_string):
        await message.answer("Ещё не время дарить подарки", keyboard=get_user_keyboard(message.from_id))
        return
    
    to_id = get_present_by_id(message.from_id)
    if to_id is None:
        await message.answer("Ты никому не даришь", keyboard=get_user_keyboard(message.from_id))
        return
    to_id = to_id[0]
    
    user_data = await bot.api.users.get(to_id)
    pref = get_prefer_by_id(to_id)
    if pref is None:
        pref = "Пожелания нет"
    else:
        pref = pref[0]
    await message.answer("Вы дарите [id"+str(to_id)+"|"+user_data[0].first_name+" "+user_data[0].last_name+"]\n\nЕго пожелание:\n "+ pref, keyboard=get_user_keyboard(message.from_id))

#########
#Adminка#
#########

class Admin(BaseStateGroup):
    ImAdmin = "Admin"
    DeleteUser = "userdelete"
    MassUved = "massuved"
    ViewUser = "viewuser"

@bot.on.message(Is_lower("Я Админ"))
async def admin_message(message: Message):
    if message.from_id not in admins:
        return
    
    await bot.state_dispenser.set(message.peer_id, Admin.ImAdmin)

    await message.answer("Вы в админке", keyboard=admin_keyboard)

@bot.on.message(StateRule(Admin.ImAdmin), Is_lower("Посмотреть участников"))
async def admin_view_users(message: Message):
    if dt.datetime.now() > dt.datetime.strptime(org_time["start_jereb"], format_string):
        text = ""
        data = get_alluser()
        
        i = 0
        for d in data:
            i = i + 1
            giver = get_giver_by_id(d[0])
            giv = "✅"
            if giver is None:
                giv = "⛔"
            text = text + str(i) +". [id"+ str(d[0])+"|"+d[1]+" "+d[2]+"] "+giv+str(d[0])+"\n"
            pres = get_present_by_id(d[0])[0]
            name = ""
            fam = ""
            for j in data:
                if j[0] == pres:
                    name = j[1]
                    fam = j[2]
            text = text + " => [id" + str(pres)+"|"+name+" "+ fam +"]\n"
    else: 
        text = ""
        data = get_alluser()
        
        i = 0
        for d in data:
            i = i + 1
            text = text + str(i) +". [id"+ str(d[0])+"|"+d[1]+" "+d[2]+"]"+str(d[0])+"\n"

    await message.answer(text, keyboard=admin_keyboard)


@bot.on.message(StateRule(Admin.ImAdmin), Is_lower("Принес подарок"))
async def admin_view_user(message: Message):
    if dt.datetime.now() < dt.datetime.strptime(org_time["start_jereb"], format_string):
        await bot.state_dispenser.set(message.peer_id, Admin.ImAdmin)
        await message.answer("Ещё не время!", keyboard=admin_keyboard)
        return
    await bot.state_dispenser.set(message.peer_id, Admin.ViewUser)
    await message.answer("Введите id человека", keyboard=otmena_keyboard)

@bot.on.message(StateRule(Admin.ViewUser))
async def admin_view_user_id(message: Message):
    await bot.state_dispenser.set(message.peer_id, Admin.ImAdmin)
    if message.text.lower() == "отмена":
        await message.answer("Админка", keyboard=admin_keyboard)
        return
    
    if not message.text.isdigit():
        await message.answer("Такого id нет", keyboard=admin_keyboard)
        return
    
    user = get_user_by_id(int(message.text))
    if user is None:
        await message.answer("Такого id нет", keyboard=admin_keyboard)
        return
    
    set_giver(int(message.text))
    try:
        await bot.api.messages.send(user_id=int(message.text), message = text_prines_podarok, random_id=random.randint(1,1000000))
    except Exception:
        print("Не смог отправить сообщение"+int(message.text))
    await message.answer("Админка", keyboard=admin_keyboard)





@bot.on.message(StateRule(Admin.ImAdmin), Is_lower("Удалить участника"))
async def admin_delete_user(message: Message):
    await bot.state_dispenser.set(message.peer_id, Admin.DeleteUser)
    await message.answer("Введите id человека", keyboard=otmena_keyboard)

@bot.on.message(StateRule(Admin.DeleteUser))
async def admin_realydelete_user(message: Message):
    if message.text.lower() == "отмена":
        await bot.state_dispenser.set(message.peer_id, Admin.ImAdmin)
        await message.answer("Админка", keyboard=admin_keyboard)
        return
    
    if not message.text.isdigit():
        await bot.state_dispenser.set(message.peer_id, Admin.ImAdmin)
        await message.answer("Такого id нет", keyboard=admin_keyboard)
        return
    
    user = get_user_by_id(int(message.text))
    if user is None:
        await bot.state_dispenser.set(message.peer_id, Admin.ImAdmin)
        await message.answer("Такого id нет", keyboard=admin_keyboard)
        return

    if dt.datetime.now() > dt.datetime.strptime(org_time["start_jereb"], format_string):
        to_id = get_present_by_id(int(message.text))[0]
        from_id = get_frompresent_by_id(int(message.text))[0]
        delete_present_by_id(int(message.text))
        delete_present_by_id(from_id)
        set_present(from_id, to_id)
        user = get_user_by_id(to_id)
        try:
            await bot.api.messages.send(user_id=from_id, message = "К сожалению, твой подопечный по некоторым причинам отказался от участия.\n\nТеперь твой подопечный: [id"+str(to_id)+"|"+user[0]+" "+ user[1]+"]", random_id=random.randint(1,1000000))
        except Exception:
            print("Не смог отправить сообщение "+str(from_id))

    delete_user_by_id(int(message.text))
    await bot.state_dispenser.set(message.peer_id, Admin.ImAdmin)
    await message.answer("текст не участвую", keyboard=admin_keyboard)

@bot.on.message(StateRule(Admin.ImAdmin), Is_lower("Массовые уведомления"))
async def admin_delete_user(message: Message):
    await bot.state_dispenser.set(message.peer_id, Admin.MassUved)
    await message.answer("Выберайте уведмоление", keyboard=mass_keyboard)

@bot.on.message(StateRule(Admin.MassUved), Is_lower("Игра началась"))
async def admin_strat_game(message: Message):
    if dt.datetime.now() > dt.datetime.strptime(org_time["start_jereb"], format_string):
        data = get_alluser()
        for d in data:
            pres = get_present_by_id(d[0])[0]
            pref = get_prefer_by_id(pres)
            if pref is None:
                pref = "Пожелания нет"
            else:
                pref = pref[0]
            text = text_start_jereb + "\n\nВы дарите:\n"
            name = ""
            fam = ""
            for i in data:
                if i[0] == pres:
                    name = i[1]
                    fam = i[2]
            text = text + "[id"+str(pres)+"|"+name+" "+fam+"]\n\nЕго пожелание:\n"+pref
            try:
                await bot.api.messages.send(user_id=d[0], message = text, random_id=random.randint(1,1000000))
            except Exception:
                print("Не смог отправить сообщение"+d[0])


    await bot.state_dispenser.set(message.peer_id, Admin.ImAdmin)
    await message.answer("Админка", keyboard=admin_keyboard)

@bot.on.message(StateRule(Admin.MassUved), Is_lower("Осталось два дня"))
async def admin_dva_dnia(message: Message):
    data = get_alluser()
    text = text_za_dva_dnya
    for d in data:
        try:
            await bot.api.messages.send(user_id=d[0], message = text, random_id=random.randint(1,1000000))
        except Exception:
            print("Не смог отправить сообщение"+d[0])

    await bot.state_dispenser.set(message.peer_id, Admin.ImAdmin)
    await message.answer("Админка", keyboard=admin_keyboard)

@bot.on.message(StateRule(Admin.MassUved), Is_lower("Время вручать подарки"))
async def admin_samoe_vremia(message: Message):
    data = get_alluser()
    text = text_priem_podark
    for d in data:
        try:
            await bot.api.messages.send(user_id=d[0], message = text, random_id=random.randint(1,1000000))
        except Exception:
            print("Не смог отправить сообщение"+d[0])
    
    await bot.state_dispenser.set(message.peer_id, Admin.ImAdmin)
    await message.answer("Админка", keyboard=admin_keyboard)

@bot.on.message(StateRule(Admin.MassUved), Is_lower("Дед разносит подарки"))
async def admin_ded_podakri(message: Message):
    data = get_alluser()
    text = "Дедушка разносит подарки"
    for d in data:
        try:
            await bot.api.messages.send(user_id=d[0], message = text, random_id=random.randint(1,1000000))
        except Exception:
            print("Не смог отправить сообщение"+d[0])
    
    await bot.state_dispenser.set(message.peer_id, Admin.ImAdmin)
    await message.answer("Админка", keyboard=admin_keyboard)

@bot.on.message(StateRule(Admin.ImAdmin))
async def admin_otmena(message: Message):
    await bot.state_dispenser.delete(message.peer_id)
    await start(message)


    





############
#Ко времени#
############
import random 

def start_jereb():
    data = get_alluser()
    l = len(data)
    to_id, from_id= [0 for i in range(l)],[]
    for i in data:
        from_id.append(i[0])
    r0 = 0
    from_id[0] = 0
    for i in range(l-1):
        while True:
            r = int(random.random()*l)
            if data[r][0] not in to_id and from_id[r] != 0 :
                to_id[r0] = data[r][0]
                from_id[r] = 0
                r0 = r
                break
    
    m = min(to_id)
    ind = to_id.index(m)
    to_id[ind] = data[0][0]
    for i in range(l):
        set_present(data[i][0], to_id[i])
    

t = Timer( (dt.datetime.strptime(str(org_time["start_jereb"]), format_string)-dt.datetime.now() ).total_seconds(), start_jereb)

t.start()

print(dt.datetime.strftime(dt.datetime.now(), format_string))

bot.run_forever()