import requests
import telebot
import sqlite3
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

BOT_TOKEN = ""

bot = telebot.TeleBot(BOT_TOKEN)
con = sqlite3.connect('bot_db.db', check_same_thread=False)
cur = con.cursor()
cur.execute('''CREATE TABLE  IF NOT EXISTS users 
               (id int(14),amount int(14), months int(14), perc float(3), step int(2))''')


def annuitet_calculator(amount, percent, months):
    i = percent / (100 * 12)
    monthly_payment = round(((i * pow((1 + i), months)) / (pow((1 + i), months) - 1)) * amount, 2)
    s1 = round(amount * i, 2)
    payed_amount = round(monthly_payment - s1, 2)
    total_percent = s1
    text_list = []
    text_monthly = "HISOBLASH JADVALI\n" \
                   f"1-oy\nKredit balansi: {amount:,} so'm\nAsosiy qarz: {payed_amount:,} so'm\n" \
                   f"Foiz : {s1:,} so'm\nOylik to'lov: {monthly_payment:,} so'm\n"

    for j in range(2, months + 1):
        payed_value = round((amount - payed_amount) * i, 2)
        py_amount = round(monthly_payment - payed_value, 2)
        text_monthly += f"{j}-oy\nKredit balansi: {round(amount - payed_amount, 2):,} so'm\nAsosiy qarz: {py_amount:,} so'm\n" \
                        f"Foiz : {payed_value:,} so'm\nOylik to'lov: {monthly_payment:,} so'm\n"
        payed_amount += py_amount
        total_percent += payed_value
        if j % 10 == 0:
            text_list.append(text_monthly)
            text_monthly = ""
    if months % 10 != 0:
        text_list.append(text_monthly)

    Text = "\nKREDIT MA'LUMOTLARI\n" \
           f"KREDIT MIQDORI : {amount:,} so'm\n" \
           f"MUDDATI : {months} oy\n" \
           f"YILLIK FOIZ STAVKASI : {percent}%\n" \
           f"JAMI FOIZ : {round(total_percent, 2):,} so'm\n" \
           f"JAMI TO'LOV MIQDORI : {round(amount + total_percent, 2):,} so'm\n"
    text_list.append(Text)
    return text_list


@bot.message_handler(commands=['start'])
def start_handler(message):
    cur.execute("""select * from users where id= ?""", [message.chat.id])
    users = cur.fetchall()
    if len(users) > 0:
        cur.execute("""update users set  step=1 where id=?""", [message.chat.id])
        con.commit()
    else:
        cur.execute("""insert into users (id, amount, months, perc, step) values (?,0,0,0,1)""", [message.chat.id])
        con.commit()

    btns = ReplyKeyboardMarkup(row_width=2)
    item1 = KeyboardButton("Kredit Kalkulyator")
    item2 = KeyboardButton("Valyuta kursi")
    btns.add(item1, item2)
    bot.send_message(message.chat.id, "Assalomu aleykum Kredit kalkulyator botiga xush kelibsiz!", reply_markup=btns)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == "Kredit Kalkulyator":
        cur.execute("""update users set  step=1 where id=?""", [message.chat.id])
        con.commit()
        bot.send_message(message.chat.id, "Kredit miqdorini kiriting:")
    elif message.text == "Valyuta kursi":
        cur.execute("""update users set step=1 where id=?""", [message.chat.id])
        con.commit()
        response = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/")
        if response.ok:
            res = response.json()
            curentcy_text = "Valyuta kurslari\n"
            for r in res[0:5]:
                curentcy_text += f"1 {r['Ccy']} = {r['Rate']} so'm\n"
        bot.send_message(message.chat.id, curentcy_text)
    else:
        cur.execute("""select * from users where id= ?""", [message.chat.id])
        user = cur.fetchone()
        if user is not None:
            if user[4] == 1:
                try:
                    amount = int(float(message.text))
                    cur.execute("""update users set amount=?, step=2 where id=?""", [amount, message.chat.id])
                    con.commit()
                    bot.send_message(message.chat.id, "Yillik foiz stavkasini kiriting:")
                except:
                    bot.send_message(message.chat.id, "Kredit miqdori xato kiritildi!")
            elif user[4] == 2:
                try:
                    perc = float(message.text)
                    cur.execute("""update users set perc=?, step=3 where id=?""", [perc, message.chat.id])
                    con.commit()
                    bot.send_message(message.chat.id, "Kredit muddatini kiriting:")
                except:
                    bot.send_message(message.chat.id, "Yillik foiz stavkasi xato kiritildi!")
            elif user[4] == 3:
                try:
                    months = int(float(message.text))
                    cur.execute("""update users set months=?, step=1 where id=?""", [months, message.chat.id])
                    con.commit()
                    cur.execute("""select * from users where id=?""", [message.chat.id])
                    user = cur.fetchone()
                    if user is not None:
                        text_lists = annuitet_calculator(user[1], user[3], user[2])
                        for txt in text_lists:
                            bot.send_message(message.chat.id, txt)
                    else:
                        bot.send_message(message.chat.id, "Iltimos start buyrug'ini qayta bosing!")
                except:
                    bot.send_message(message.chat.id, "Qandaydur xatolik yuz berdi!")
                    cur.execute("""update users set  step=1 where id=?""", [message.chat.id])
                    con.commit()
                    bot.send_message(message.chat.id, "Kredit miqdorini kiriting:")


bot.infinity_polling()
