# Aplikacja_Webowa

Realizacja kolejnych etapów projektów laboratoryjnych.

## Cel projektu

Napisanie systemu do zarządzania bibliografią.

## Etap 1 - Formularz rejestracyjny

Opracowanie formularza rejestracyjnego dla nowych użytkowników. Formularz musi pozwalać na **walidowanie wszystkich pól na bieżąco**. Kod JavaScript, HTML i CSS muszą być od siebie **odesparowane**. Komunikaty błędów muszą być tworzone dynamicznie przez kod JS. Polę login użytkownika będzie sprawdzane pod kątem dostępności **asynchronicznie**. Dane do rejestracji będą przesyłane do na zewnętrzny serwer. Kod HTML i CSS musi przechodzić walidację.

### Istotne elementy

* czy kod HTML posiada puste węzły na komunikaty (źle, powinny być one dodawane dynamicznie),
* czy wykorzystywane są elementy HTML5 zamiast generycznych, np. `<div class='menu'/>`, `<span id='footer'></span>`,
* jak analizowana jest odpowiedź o dostępności loginu (czy sprawdzany tylko tekst odpowiedzi, czy też kod statusu).

### Uruchomienie Formularza

Strona wymaga **połączenia z Internetem**, ponieważ sciąga węwnętrzy serwer **nginx** oraz sprawdza poprawność loginu na zewnętrznym serwerze. Uruchomiamy stronę za pomocą **Dockera**

#### Docker
Instalowanie Dockera.   
`sudo apt-get install docker`

Zbudowanie obrazu z pliku [Dockerfile](Aplikacja_Webowa_Etap_1/Dockerfile).  
`sudo docker build -t aplikacja .`

Uruchomienie kontenera.  
`sudo docker run --rm -p 8080:80 aplikacja`

Następnie strona powinna być dostępna pod adresem [http://localhost:8080](http://localhost:8080/).
Szybkie uruchomienie.
Jeżeli macie dockera to użyj    
`sudo chmod 755 rundocker.sh`   
`./rundocker.sh`

### Opis plików

Informacja o plikach składających się na projekt.

#### Pliki projektu

* **index.html** - Struktura strony logowania
* **css/style.css** - Wygląd strony logowania
* **imgage/** - Obrazy znajdujące się na stronie
* **js/script.js** - Skrypt bezpośrednio związany z walidacją logowania

#### Pliki konfiguracji (serwer)

* **Dockerfile** - Opis jak zbudować kontener serwujący stronę
* **rundocker.sh** - Skrypt, uruchomiający strone

----------------------

## Etap 2 - Formularz logowania
Opracowanie modułu służącego do bezpiecznego logowania i wylogowywania użytkownika. Moduł logowania otrzymuje od użytkownika hasło i login – w przypadku poprawnych danych generowany jest identyfikator sesji. Dane sesyjne przechowywane są w bazie danych Redis. Należy opracować formularz pozwalający na przechowywanie przez użytkownika plików PDF w systemie. Pliki PDF powinny być dostępne do pobrania i serwowane przez bezstanową aplikację. Należy wykorzystać JWT z krótką datą ważności.

### Istotne elementy
* czy w ciasteczku generowany jest identyfikator sesji czy bezterminowy JWT (to drugie nie pozwala wylogować),
* czy przy wylogowaniu usuwane są wpisy z Redis,
* czy w formularzu jestenctype=multipart/form-data
* czy aplikacja serwująca dostęp do pliku korzysta z sesji (czy innych informacji poza tymi w żetonie) - jeżeli tak, to źle,
* czy żeton do pobrania ma krótki czas ważności (kilka minut).

Prosze przejsc tutaj [Etap_2](./Aplikacja_Webowa_Etap_2)


## Etap 3 - Opracowanie usługi sieciowej i klienta na urządzenie przenośne.

Prosze przejsc tutaj [Etap_3](./Aplikacja_Webowa_Etap_3)
