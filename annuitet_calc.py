def annuitet_calculator(amount, percent, months):
    i = percent / (100 * 12)
    monthly_payment = round(((i * pow((1 + i), months)) / (pow((1 + i), months) - 1)) * amount, 2)
    s1 = round(amount * i, 2)
    payed_amount = round(monthly_payment - s1,2)
    total_percent = s1
    Text = "KREDIT MA'LUMOTLARI\n" \
           f"Kredit miqdori : {amount} so'm" \
           f"Muddati : {months} oy\n" \
           f"Yillik foiz stavkasi: {percent}%\n" \
           "HISOBLASH JADVALI\n" \
           f"1-oy\nKredit balansi:{amount} so'm\tAsosiy qarz: {payed_amount} so'm\n Foiz : {s1} so'm\tOylik to'lov: {monthly_payment} so'm\n"
    for j in range(2, months + 1):
        payed_value = round((amount - payed_amount) * i, 2)
        py_amount = round(monthly_payment - payed_value, 2)
        total_percent += payed_value
        Text += f"{j}-oy\nKredit balansi:{round(amount - payed_amount,2)} so'm\tAsosiy qarz: {py_amount} so'm\n" \
                f"Foiz : {payed_value} so'm\tOylik to'lov: {monthly_payment} so'm\n"
        payed_amount += round(py_amount, 2)
    Text += f"Kredit miqdori : {amount}\tJami Foiz : {round(total_percent,2)}\t Jami to'lov : {amount + total_percent}"

    return Text


print(annuitet_calculator(20000000, 12, 24))
