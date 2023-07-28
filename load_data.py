import requests
import datetime as dt
import csv
import unidecode
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

GENDER_API_URL = "https://gender-api.com/get"
GENDER_API_KEY = "o2sK2NtlYZEhY5DXgRGJmUKjR8gcuWSAaXqf"

# Kreiranje baze podataka
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///imena.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = SQLAlchemy(app)


# Klasa vezana za .db tabelu
class Imena(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    ime = database.Column(database.String(60), unique=True, nullable=False)
    spol = database.Column(database.String(10), nullable=False)
    tacnost = database.Column(database.Integer, nullable=False)


class BazaPodatakaClanova:
    def __init__(self, google_sheets_url):
        response = requests.get(url=google_sheets_url)
        # Svi članovi sa google sheets-a se definisu kao json
        self.svi_clanovi = response.json()["clanarine"]
        self.isteknuti_clanovi_poznat_br_telefona = []

    def get_isteknute_clanarine(self, datum_provjere):
        for clan in self.svi_clanovi:
            datum_isteka = None
            # Prvo provjeriti ima li uopste podataka u liniji
            if "imePrezime" not in clan or "datumIstekaClanarine" not in clan:
                continue
            # Ako je slucajno unesen datum isteka clanarine pogresno nastavlja program da ne bi crashiro
            try:
                datum_isteka = dt.datetime.strptime(clan["datumIstekaClanarine"], '%d.%m.%Y.')
            except:
                print(f"Loše unesen datum za {clan['imePrezime']}. Uneseno je {clan['datumIstekaClanarine']}")
                continue
            finally:
                datum_provjere_string = str(datum_provjere).split(' ')[0]
                datum_isteka_string = str(datum_isteka).split(' ')[0]

                if datum_isteka_string == datum_provjere_string and clan['brojTelefona'] != '':
                    clan['spol'] = self.__odredjivanje_spola(clan)
                    clan['imePrezime'] = self.__korekrcija_imena_prezimena(clan)
                    self.isteknuti_clanovi_poznat_br_telefona.append(clan)

        # Vraca listu članova kojima treba i može poslat poruku tj. kome sutra ističe članarina, a imamo mu broj
        return self.isteknuti_clanovi_poznat_br_telefona

    def __odredjivanje_spola(self, clan):
        ime_clana = clan["imePrezime"].split(' ')[0]
        # Trazimo podatke u tabeli na osnovu imena clana
        data = Imena.query.filter_by(ime=ime_clana).first()
        # Ako ime se ne nalazi u bazi podataka data ce biti None i trazimo to ime na internetu i unosimo ga u databazu
        if data is None:
            data = self.__trazi_spol_preko_interneta(ime_clana)
            database.session.add(data)
            database.session.commit()

            # Sada ga imamo u bazi pa ga mozemo pozvat
            data = Imena.query.filter_by(ime=ime_clana).first()

        # Sada imamo podatke pa vracamo spol
        return data.spol

    def kreiranje_baze_imena_spol(self):
        # Kreiranje niza uniformnih imena
        uniformna_imena = []
        self.__imena_bez_duplikata()

        # Kreiranje SQL tabele
        database.create_all()

        for vlastito_ime in uniformna_imena:
            new_data = self.__trazi_spol_preko_interneta(vlastito_ime)
            database.session.add(new_data)

        database.session.commit()


    def __trazi_spol_preko_interneta(self, ime):
        parameters = {
            "name": ime,
            "key": GENDER_API_KEY,
        }
        # Na osnovu imena prepoznaje koji je spol to ime
        response = requests.get(url=GENDER_API_URL, params=parameters)
        data = response.json()
        # Ako je nepoznat spol ili je preciznost manja od 60 pita nas da mi kazemo kojeg je spola
        if data['gender'] == "unknown" or data['accuracy'] < 60:
            while True:
                spol = input(f"Kojeg je spola {ime}? -> ").lower()
                if spol in ["muski", "m", "male", "muški", "musko", "muško"]:
                    data['gender'] = "male"
                    data['accuracy'] = 100
                    break
                elif spol in ["zenski", "z", "female", "ženski", "ž", "žensko", "zensko"]:
                    data['gender'] = "female"
                    data['accuracy'] = 100
                    break

        return Imena(ime=ime, spol=data['gender'], tacnost=data['accuracy'])

    def __imena_bez_duplikata(self):
        # Imena bez duplikata
        for clan in self.svi_clanovi:
            ime = clan['imePrezime'].split(' ')[0]
            if ime not in self.uniformna_imena:
                self.uniformna_imena.append(ime)

    # Mijenja Đ sa Dj ako se nalazi kao prvi karakter imena i/li prezimena
    def __korekrcija_imena_prezimena(self, clan_teretane):
        ime_prezime = clan_teretane['imePrezime'].strip()
        ime_prezime = ime_prezime.replace("Đ", "Dj")
        ime_prezime = ime_prezime.replace("đ", "dj")

        return ime_prezime
