# Opracowanie usługi sieciowej i klienta na urządzenie przenośne. 
## Usługa sieciowa musi pozwalać na:
* dodawanie pozycji bibliograficznej,
* listowanie pozycji bibliograficznych,
* usuwaniu pozycji bibliograficznych,
* podpinaniu i odpinaniu plików przy pozycji bibliograficznej,
* dodawanie, pobieranie i usuwanie plików.

## # Instruction

Żeby uruchomić aplikacje, musisz postępować dokładnie następującymi krokami:
1. `git clone https://github.com/ivanprokopets/Web-application.git`  
2. `cd Web-application/Aplikacja_Webowa_Etap_3`  
3. `sudo docker-compose -f docker-compose.yml up -d --build`  
    3.1 Musisz wprowadzić swoje haslo od super użytkownika  
    3.2 Może wystąpić następujący problem podczas budowania redisa:  
`Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.VerifiedHTTPSConnection object at 0x7fac9a377898>: Failed to establish a new connection: [Errno -3] Temporary failure in name resolution',)': /simple/uuid/`

Żeby uniknąc go, musisz podłaczyć się do innej sieci, naprzykład rozdać wi-fi za pomocą komórki.

4. W przegłądarkie proszę wejść pod adress:  
http://0.0.0.0/

## Simple app with 1 server for 2 applikation

Zeby uruchomic, po prostu napisz w katalogu test  
`sudo docker-compose up`  

W przeglądarkie proszę wejść pod adresy:  
http://localhost:8080/front  
http://localhost:8080/api  
