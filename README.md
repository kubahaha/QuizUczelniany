## Requirements

* pip3 install django-widget-tweaks psycopg2

# Backend

## Działa:

#### Użytkownik:

* Logowanie/wylogowywanie

* Rejestracja nowego użytkownika, walidacja

* Zmiana hasła i emaila

* Autentykacja użytkownika (niezalogowany ma dostep tylko do _/guest/*_ )

* Przeglądanie do jakich grup jest zapisany

* Przeszukiwanie grup do jakich jest zapisany

#### Grupy:

* Dodawanie grup (Nazwa, opis) wraz z tagami, walidacja

* Szukajka grup - po nazwie/opisie i tagach

* Globalne sprawdzanie czy grupa o podanym id istnieje

* Mechanizm dołączania

* Przeglądanie członków grupy w panelu (super)administratora

## TODO:

#### Użytkownik:

* Statystyki rozwiązywania quzów z poszczególnych grup

* ...

### Grupy:

* Panel administratora

  - usuwanie członków 
  
  - (_grupa zamknięta_) zatwierdzanie członkostwa
  
  - Przeglądanie niezatwierdzonych pytań, zatwierdzanie ich
  
  - Przeglądanie niezatwierdzonych quizów, zatwierdzanie ich

* Panel super administratora
  
  - zmienianie im praw członków grupy
  
  - zmienianie tagów i opisu grupy

  - usuwanie grupy
  
* ...
  
### System pytań
