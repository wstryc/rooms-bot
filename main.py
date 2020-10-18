import smtplib, requests, datetime
import config, misc

from bs4 import BeautifulSoup
from time import sleep

class Bot:
    def __init__(self):
        """ Initialise the bot """
        # Clean the logs:
        for log in ['logs/olx.txt', 'logs/otodom.txt']:
            with open(log, 'w+') as f:
                f.write('Log started on ' +
                        misc.day_and_month() +
                        '\n'
                        )

        self.old_otodom = self.parse_otodom()
        self.old_olx = self.parse_olx()

    def parse_otodom(self):
        """ Web-scrap otodom.pl and get the results from the first page """
        url = 'https://www.otodom.pl/wynajem/pokoj/wroclaw/?search%5Bcity_id%5D=39&search%5Border%5D=created_at_first%3Adesc'
        request = requests.get(url).text
        soup = BeautifulSoup(request, 'lxml')
        
        rooms_list = []
        
        for offer in soup.find_all('div', class_='offer-item-details'):
            title = offer.find('span', class_='offer-item-title').text
            price_raw = offer.find('li', class_='offer-item-price').text.strip()
            price = price_raw[0:-3].strip()
            goto = offer.find('a').get('href')
            location = offer.p.text[18:-1] + offer.p.text[-1]
    
            rooms_list.append((title, price, location, goto))
            
        rooms_not_promoted = rooms_list[3:-1]
        rooms_not_promoted.append(rooms_list[-1])
        
        with open('logs/otodom.txt', 'a+') as f:
            f.write(misc.time() + '\n' + str(rooms_not_promoted) + '\n***\n')

        return rooms_not_promoted
        
    def parse_olx(self):
        """ Web-scrap olx.pl and get the results from the first page """
        url = "https://www.olx.pl/nieruchomosci/stancje-pokoje/wroclaw/?search%5Bfilter_enum_preferences%5D%5B0%5D=student"
        request = requests.get(url).text
        soup = BeautifulSoup(request, 'lxml')
        
        rooms_list = []
        
        for offer in soup.find_all('div', class_='offer-wrapper'):
            title = offer.find('div', class_='space rel').strong.text
            price = offer.find('p', class_='price').strong.text
            goto = offer.find('a').get('href')
            location = offer.find('td', class_='bottom-cell').span.text
    
            rooms_list.append((title, price, location, goto))
            
        rooms_not_promoted = rooms_list[5:-1]
        rooms_not_promoted.append(rooms_list[-1])
            
        with open('logs/olx.txt', 'a+') as f:
            f.write(misc.time() + '\n' + str(rooms_not_promoted) + '\n***\n')
            
        return rooms_not_promoted
        
    def check_diffs(self, old_list, new_list):
        """ Check if any new offer has been added """
        return list(set(new_list) - set(old_list))

    def send_mail(self, details):
        """
        Send an email with details of a room.
        
        Requires config.py file (look: README.md)
        
        
        Variables:
        details -- list-like; must be in [title, price, location, goto] format.
        """
        
        sender = config.SENDER
        receiver = config.RECEIVER

        subject = "Nowa oferta!"
        body = f"""\
        Cześć!
        Znalazłem nową ofertę, oto szczegóły:
        
        {details[0]}
        
        Cena: {details[1]}
        Lokalizacja: {details[2]}
        Link: {details[3]}
        
        Miłego dnia!
        """

        message = f'From: {sender}\r\nSubject: {subject}\r\n\r\n{body}'

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(config.USERNAME, config.PASSWORD)
            server.sendmail(sender, receiver, message.encode('utf-8'))
            
    def run(self):
        new_olx = self.parse_olx()
        new_otodom = self.parse_otodom()
        
        if (new_olx == self.old_olx) and (new_otodom == self.old_otodom):
            print(misc.time() + ' | Nothing...')
        else:
            print(misc.time() + ' | Mail has been sent!')
            diff_olx = self.check_diffs(self.old_olx, new_olx)
            diff_otodom = self.check_diffs(self.old_otodom, new_otodom)
        
            diff_total = diff_olx + diff_otodom
        
            for diff in diff_total:
                self.send_mail(diff)

        self.old_olx = new_olx
        self.old_otodom = new_otodom
        
if __name__ == "__main__":
    b = Bot()
    while True:
        if misc.day_of_the_week in [5,6]:
            sleep(180)
            b.run()
        else:
            sleep(120)
            b.run()