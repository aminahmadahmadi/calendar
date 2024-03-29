﻿def perNo(txt):
    txt = str(txt)

    perTxt = [
        ['0', '۰'],
        ['1', '۱'],
        ['2', '۲'],
        ['3', '۳'],
        ['4', '۴'],
        ['5', '۵'],
        ['6', '۶'],
        ['7', '۷'],
        ['8', '۸'],
        ['9', '۹'],
        ['٤', '۴'],
        ['٥', '۵'],
        ['٦', '۶'],
    ]
    for a, b in perTxt:
        txt = txt.replace(a, b)
    return txt


def arbNo(txt):
    txt = str(txt)

    arbTxt = [
        ['0', '٠'],
        ['1', '١'],
        ['2', '٢'],
        ['3', '٣'],
        ['4', '٤'],
        ['5', '٥'],
        ['6', '٦'],
        ['7', '٧'],
        ['8', '٨'],
        ['9', '٩'],
        ['۴', '٤'],
        ['۵', '٥'],
        ['۶', '٦'],
    ]
    for a, b in arbTxt:
        txt = txt.replace(a, b)
    return txt


def engNo(txt):
    txt = str(txt)

    engTxt = [
        ['0', '٠'],
        ['1', '١'],
        ['2', '٢'],
        ['3', '٣'],
        ['4', '٤'],
        ['5', '٥'],
        ['6', '٦'],
        ['7', '٧'],
        ['8', '٨'],
        ['9', '٩'],
        ['0', '۰'],
        ['1', '۱'],
        ['2', '۲'],
        ['3', '۳'],
        ['4', '۴'],
        ['5', '۵'],
        ['6', '۶'],
        ['7', '۷'],
        ['8', '۸'],
        ['9', '۹']
    ]
    for a, b in engTxt:
        txt = txt.replace(b, a)

    return txt


def flatText(txt):
    txt = str(txt)
    txt = txt.strip()

    engTxt = [
        ['  ', ' '],
        ['\n', ' '],
    ]
    for _ in range(10):
        for a, b in engTxt:
            txt = txt.replace(a, b)

    return txt
