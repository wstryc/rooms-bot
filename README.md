# Polski

## Krótki kod, który automatycznie szuka ogłoszeń wynajmu pokoi we Wrocławiu i powiadamia użytkownika mailowo o nowych ofertach.

### 0. Kilka słów wstępu
Głównym zadaniem projektu jest web-scrapping dwóch najpopularniejszych stron internetowych z ofertami wynajmu i powiadamianie użytkownika o każdej nowej ofercie.

### 1. Plik `config.py`
Wymagany jest plik `config.py` w następującym formacie:
```
USERNAME = 'example@gmail.com'
PASSWORD = 'password'

SENDER ='Bot name <example@gmail.com>'
RECEIVER = 'Receiver's name <receiver@example.com>'
```
Domeną bota musi być <b> gmail! </b>

### 2. Inna specyfikacja
Oczywiście projekt można łatwo przerobić na szukanie innych ofert. Wystarczy w tym celu zmienić specyfikacje wyszukiwania w portalach aukcyjnych i podpiąc inny link `url` w metodach `parser_olx` oraz `parser_otodom`.

# English

## A short piece of code that automatically browses rental offers in Wrocław and notifies user of any new ones.

### 0. About
The main goal of this short project is to web-scrap two most popular Polish websites with rental offers and notify user of any new offer. 

### 1. `config.py` file
A `config.py` file in the following format is compulsory:
```
USERNAME = 'example@gmail.com'
PASSWORD = 'password'

SENDER ='Bot's name <example@gmail.com>'
RECEIVER = 'Receiver's name <receiver@example.com>'
```
Please note that the bot's domain must be <b> gmail! </b>

### 2. Other specification
Of course project's searching criteria can be easily modified. To do so, you need to change searching specification on the websites and change the `url` variables in `parser_olx` and `parser_otodom` methods.

