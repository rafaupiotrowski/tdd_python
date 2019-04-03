przygotowanie nowej witryny
===========================

##Wymagane pakiety:
*nginx
*Python 3
*Git
*pip
*virtualenv

Na przykład w systemie Ubuntu należy wydać polecenia:
	sudo apt-get install nginx git python3 python3-pip
	sudo pip3 install virtualenv

##Konfiguracja wirtualnych hostów w nginx

*Zobacz plik nginx.sites-available.template
*SITENAME należy zastąpić odpowiednią nazwą, na przykład rafalpiotrowski.com.pl

##Zadanie systemd

* Zobacz pliki gunicorn.template.socket i gunicorn.template.service
* Uruchomienie powyższych i ustawienie autostartu

## Struktura katalogów
Przyjmujemy założenie o istnieniu konta użytkownika w postaci /home/użytkownik.

/home/użytkownik
	sites
		SITENAME
			database
			source
			static
			virtualenv


