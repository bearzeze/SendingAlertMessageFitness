from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
import unidecode

chromedriver_path = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
BH_TELEKOM_URL = "https://moj.bhtelecom.ba/"


class BHTelecom:
    def __init__(self):
        # Da se ne gasi svaki put chrome browser
        op = webdriver.ChromeOptions()
        op.add_experimental_option("detach", True)
        # Da ne čeka sve da se učita na stranici
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "none"
        self.driver = webdriver.Chrome(executable_path=chromedriver_path, options=op, desired_capabilities=caps)

    def user_login(self, BROJ_TELEFONA_ZA_LOGIN, PASSWORD_ZA_LOGIN):
        self.driver.get(url=BH_TELEKOM_URL)
        sleep(6)
        prijava = self.driver.find_element(By.XPATH,
                                           '//*[@id="portlet_portallandingpagemvc_INSTANCE_mJ5es4A86fRm"]/div/div/div/div[2]/a[1]')
        prijava.click()
        sleep(3)
        # Upisivanje username i passworda
        username = self.driver.find_element(By.ID, 'username_2')
        username.send_keys(BROJ_TELEFONA_ZA_LOGIN)
        sleep(1)

        password = self.driver.find_element(By.ID, 'password')
        password.send_keys(PASSWORD_ZA_LOGIN)
        sleep(1)

        # Prijavi se
        login_button = self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div[5]/div/button')
        login_button.click()
        sleep(4)

    def user_logout(self):
        self.driver.quit()

    def send_notification(self, clan, fitness_ili_bjj, dan, proba):
        self.driver.get(url="https://moj.bhtelecom.ba/web/guest/posalji-poruku")
        sleep(2)

        primatelj = self.driver.find_element(By.ID, 'primatelj')
        primatelj.send_keys(clan['brojTelefona'].strip())

        poruka_bht = self.driver.find_element(By.ID, 'poruka')

        # Različite su poruke za bjj članove, a razlicite za članove fitness Skenderije
        message = ""
        if fitness_ili_bjj == "fitness_skenderija":
            message = self.__odredjivanje_poruke_FitnessSkenderija(clan, dan)
        elif fitness_ili_bjj == "bjj_brotherhood":
            message = self.__odredjivanje_poruke_BJJBrotherhood(clan)

        # Pretvara sve ove nase karaktere u engleske č - c, ž - z, š - s
        message = unidecode.unidecode(message)
        poruka_bht.send_keys(message)
        sleep(1)

        posalji = self.driver.find_element(By.ID, 'btnposalji')

        # Ako se nije poruka kreirala nece se ni poslat članu
        if message != "" and proba == "ne":
            posalji.click()
        sleep(3)
        print(message + "\n================================================================")

    def __odredjivanje_poruke_FitnessSkenderija(self, clan_teretane, dan):
        if clan_teretane['spol'] == "male":
            prvi_dio = "Poštovani"
            ponuda = "mjesečna članarina 40 KM,\n- polugodišnja članarina 200 KM,\n- godišnja članarina 300 KM"

        else:
            prvi_dio = "Poštovana"
            ponuda = "mjesečna članarina 30 KM,\n- polugodišnja članarina 150 KM,\n- godišnja članarina 250 KM"

        if clan_teretane['napomena'].lower() == 'brotherhood':
            ponuda = "mjesečna članarina 20 KM,\n- polugodišnja članarina 120 KM,\n- godišnja članarina 240 KM"

        if dan == 1:
            danStr = "sutra"
        elif dan == 2:
            danStr = "prekosutra"

        return f"{prvi_dio} {clan_teretane['imePrezime'].strip()}, Vaša članarina ističe {danStr} " \
               f"({clan_teretane['datumIstekaClanarine'][:-1]}). Članarinu možete produžiti u prostorijama" \
               f" Fitness Skenderija prema sljedećoj ponudi:\n- {ponuda}.\n\nVaša Fitness Skenderija." \

    def __odredjivanje_poruke_BJJBrotherhood(self, clan_kluba):
        # Clanovi Brotherhood
        if clan_kluba['spol'] == "musko":
            prvi_dio = "Poštovani"

        elif clan_kluba['spol'] == "zensko":
            prvi_dio = "Poštovana"

        drugi_dio = "Vaša članarina"
        ponuda = "\n- mjesečna članarina 40 KM,\n- polugodišnja članarina 180 KM,\n- godišnja članarina 300 KM"

        # Roditeljima Kids Brotherhood-a
        if clan_kluba['napomena'].lower() == 'kids':
            drugi_dio = "članarina Vašeg djeteta"
            ponuda = "\n- mjesečna članarina 30 KM,\n- polugodišnja članarina 180 KM,\n- godišnja članarina 300 KM"

        return f"{prvi_dio} {clan_kluba['imePrezime'].strip()}, {drugi_dio} ističe sutra " \
               f"({clan_kluba['datumIstekaClanarine'][:-1]}). Članarinu možete produžiti u prostorijama" \
               f" BJJ Brotherhood Skenderija ili kod sekretara kluba prema sljedećoj ponudi:{ponuda}." \
               f"\n\nPlacanje clanarine je duznost svakog clana, te time doprinosite radu i rastu kluba." \
               f"\n\nVaš BJJ Brotherhood."
