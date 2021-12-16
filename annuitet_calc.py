
# def annuitet_calculator(amount, percent, months):
#     i = percent / (100 * 12)
#     monthly_payment = round(((i * pow((1 + i), months)) / (pow((1 + i), months) - 1)) * amount, 2)
#     s1 = round(amount * i, 2)
#     payed_amount = round(monthly_payment - s1, 2)
#     total_percent = s1
#     for j in range(2, months + 1):
#         payed_value = round((amount - payed_amount) * i, 2)
#         py_amount = round(monthly_payment - payed_value, 2)
#         payed_amount += py_amount
#         total_percent += payed_value
#
#
#     Text = "KREDIT MA'LUMOTLARI\n" \
#            f"Kredit miqdori : {amount} so'm\n" \
#            f"Muddati : {months} oy\n" \
#            f"Yillik foiz stavkasi: {percent}%\n" \
#            f"Jami foiz : {round(total_percent,2)} so'm\n" \
#            f"Jami to'lov miqdori: {amount+total_percent} so'm"
#
#     return Text


def annuitet_calculator(amount, percent, months):
    i = percent / (100 * 12)
    monthly_payment = round(((i * pow((1 + i), months)) / (pow((1 + i), months) - 1)) * amount, 2)
    s1 = round(amount * i, 2)
    payed_amount = round(monthly_payment - s1, 2)
    total_percent = s1
    text_monthly = "HISOBLASH JADVALI\n" \
                   f"1-oy\nKredit balansi: {amount:,} so'm\nAsosiy qarz: {payed_amount:,} so'm\n" \
                   f"Foiz : {s1:,} so'm\nOylik to'lov: {monthly_payment:,} so'm\n"
    for j in range(2, months + 1):
        payed_value = round((amount - payed_amount) * i, 2)
        py_amount = round(monthly_payment - payed_value, 2)
        text_monthly += f"{j}-oy\nKredit balansi: {round(amount - payed_amount,2):,} so'm\nAsosiy qarz: {py_amount:,} so'm\n" \
                        f"Foiz : {payed_value:,} so'm\nOylik to'lov: {monthly_payment:,} so'm\n"
        payed_amount += py_amount
        total_percent += payed_value


    Text = "\nKREDIT MA'LUMOTLARI\n" \
           f"KREDIT MIQDORI : {amount:,} so'm\n" \
           f"MUDDATI : {months} oy\n" \
           f"YILLIK FOIZ STAVKASI : {percent}%\n" \
           f"JAMI FOIZ : {round(total_percent,2):,} so'm\n" \
           f"JAMI TO'LOV MIQDORI : {amount+total_percent:,} so'm\n"
    return text_monthly+Text

print(annuitet_calculator(10000000, 12, 24))
