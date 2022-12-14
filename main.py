import datetime as dt
from load_data import BazaPodatakaClanova
from bhTelecom import BHTelecom
import unidecode
from telekomPodaci import *

FITNESS_SKENDERIJA_SHEETS_ENDPOINT = "https://api.sheety.co/ee1d18fbccc08c72a4afafaf64fefaa0/fitnessSkenderija/clanarine"
BJJ_BROTHERHOOD_SHEETS_ENDPOINT = "https://api.sheety.co/ee1d18fbccc08c72a4afafaf64fefaa0/bjjBrotherhoodClanarine/clanarine"


def main_Fitness_Skenderija():
    # da li je proba ili slanje
    proba = "ne"
    # Koji se datum posmatra - uglavnom sutrasnji da se član napomene na vrijeme
    dan = 1
    datum_provjere = dt.datetime.now() + dt.timedelta(days=dan)

    # Formira se baza podataka članova skenderija
    fitnes_skenderija = BazaPodatakaClanova(FITNESS_SKENDERIJA_SHEETS_ENDPOINT)
    # Lista clanova kojima ce se slati sms - istekla im clanarina i imaju broj telefona upisan u Google Sheetsu
    lista_clanova_za_sms = fitnes_skenderija.get_isteknute_clanarine(datum_provjere)

    bh_telekom = BHTelecom()

    # Tekst kome ce pisati u history.txt fajlu
    kome = ""
    # Samo ako se ima kome poslati poruka (duzina liste clanova je veca od nule)
    if len(lista_clanova_za_sms) > 0:
        bh_telekom.user_login(BHT_BROJ_TELEFONA_FITNESS, BHT_PASSWORD_FITNESS)
        for clan_teretane in lista_clanova_za_sms:
            # Loginuje se na bh Telekom web stranicu
            # Šalje se poruka sljedećem članu
            bh_telekom.send_notification(clan_teretane, "fitness_skenderija", dan, proba)
            kome += f"{clan_teretane['imePrezime']}({clan_teretane['brojTelefona']})  "

        # Zatvaranje browsera
        bh_telekom.user_logout()

    # Historija izvršavanja programa spašeno u tekstualni fajl
    if proba == "ne":
        log_history(kome, "fajlovi/history_FSkenderija.txt")


def main_BJJ_Brotherhood():
    # Koji se datum posmatra - uglavnom sutrasnji da se napomene na vrijeme
    sutrasnji_datum = dt.datetime.now() + dt.timedelta(days=2)

    # Formira se baza podataka članova BJJ Brotherhood
    bjj_brotherhood = BazaPodatakaClanova(BJJ_BROTHERHOOD_SHEETS_ENDPOINT)
    # Lista clanova kojima ce se slati sms - istekla im clanarina i imaju broj telefona upisan u Google Sheetsu
    lista_clanova_za_sms = bjj_brotherhood.get_isteknute_clanarine(sutrasnji_datum)

    # Otvara se web BH Telekom u Chrome-u
    bh_telekom = BHTelecom()
    # Loginuje se na bh Telekom web stranicu i to sa brojem i passworda telefona sa kojeg ce se slat poruke
    bh_telekom.user_login(BHT_BROJ_TELEFONA_BROTHERHOOD, BHT_PASSWORD_BROTHERHOOD)

    kome = ""
    for clan_kluba in lista_clanova_za_sms:
        bh_telekom.send_notification(clan_kluba, "bjj_brotherhood")
        # Tekst kome ce pisati u history.txt fajlu
        kome += f"{clan_kluba['imePrezime']}({clan_kluba['brojTelefona']})  "

    # Zatvaranje browsera
    bh_telekom.user_logout()

    # Historija izvršavanja programa spašeno u tekstualni fajl
    log_history(kome, "fajlovi/history_BJJBrotherhood.txt")


# Metoda za spašavanje historije poziva u tekstualni fajl
def log_history(tekst, naziv_fajla):
    with open(naziv_fajla, mode='a') as file:
        danas = dt.datetime.now()
        file.write(f"{danas.strftime('%d.%m.%Y %H:%Mh')}        |      {unidecode.unidecode(tekst)}\n")



izbor = "fitness"
if izbor == "sve" or izbor == "fitness":
    main_Fitness_Skenderija()

if izbor == "sve" or izbor == "bjj":
    main_BJJ_Brotherhood()


