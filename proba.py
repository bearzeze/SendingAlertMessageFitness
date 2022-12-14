import datetime as dt
from load_data import BazaPodatakaClanova
import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup

FITNESS_SKENDERIJA_SHEETS_ENDPOINT = "https://api.sheety.co/ee1d18fbccc08c72a4afafaf64fefaa0/fitnessSkenderija/clanarine"
# fitness = BazaPodatakaClanova(FITNESS_SKENDERIJA_SHEETS_ENDPOINT)

danas = dt.datetime.now()

danas_str = danas.strftime('%d.%m.%Y %H:%Mh')

print(danas_str)

sutrasnji_datum = dt.datetime.now() + dt.timedelta(days=1)
sutrasnji_datum_string = str(sutrasnji_datum).split(' ')[0]


datum_isteka = dt.datetime.strptime("01.06.2022", '%d.%m.%Y')
datum_isteka_string = str(datum_isteka).split(' ')[0]



