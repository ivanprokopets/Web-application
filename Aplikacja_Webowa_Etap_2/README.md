# Instruction

Żeby uruchomić aplikacje, musisz postępować dokładnie następującymi krokami:
1. `git clone https://github.com/ivanprokopets/Web-application.git`  
2. `cd Web-application/Aplikacja_Webowa_Etap_2`  
3. `sudo docker-compose -f docker-compose.yml up -d --build`  
    3.1 Musisz wprowadzić swoje haslo od super użytkownika  
    3.2 Może wystąpić następujący problem podczas budowania redisa:  
`Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.VerifiedHTTPSConnection object at 0x7fac9a377898>: Failed to establish a new connection: [Errno -3] Temporary failure in name resolution',)': /simple/uuid/`

Żeby uniknąc go, musisz podłaczyć się do innej sieci, naprzykład rozdać wi-fi za pomocą komórki.

4. W przegłądarkie proszę wejść pod adress:  
http://localhost:5001/

## Baza użytkowników:

Baza uzytkowników:
1. Login: test,   password: test
2. Login: ivan,   password: ivan
3. Login: login,  password: password

Jeżeli chcesz dodać innych użytkowników po przez Pytonowski code, proszę usunąć plik [login](./client/static/script_login.js). Bo w tym pliku jest napisana walidacja użytkowników.

DONE!
=)
Przydatne linki: 
1) https://medium.com/@terrillowalls/python3-flask-and-docker-in-production-the-easy-way-2ce8080d4f14
2) https://bitbucket.org/zespoll/notes_from_classes/src/master/#markdown-header-lab-1-docker
3) https://github.com/bchaber/di1541/tree/master/L4
