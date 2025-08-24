# Election scraper (Projekt 3)

Cilem tohoto projektu bylo vytvorit python script, ktery stahne vysledky voleb do Poslanecke snemovny z roku 2017  (z tohoto [odkazu](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ)) pro libovolny vybrany okres z weboveho odkazu a ulozi jej do csv souboru.

## Postup pro spuštění skriptu:
1) Nejprve je potřeba si vytvorit virtuální prostředí, např. venv_project3, ve Windows Powershell to bude takto:
   
```bash
python -m venv venv_project3
```

2) Do stejne slozky jako mame vytvorene virtualni prostredi je treba ulozit soubor main.py se zdrojovym kodem a taky soubor requirements.txt, ktery obsahuje seznam python knihoven, ktere jsou potrebne ke spravnemu fungovani kodu.

3) Nasledne pak spustime instalaci potrebnych knihoven pro fungovani kodu uvnitr naseho prostredi pomoci souboru requirements.txt:
   
```bash
pip install -r requirements.txt
```
4) Pak uz je mozne spustit skript prikazem ve tvaru:
 
```bash
python "webova_adresa_na_vysledky_voleb_v_danem okrese" nazev_souboru.csv
```
Prikaz obsahuje 2 argumenty - 1) URL v uvozovkach a 2) nazev csv souboru, do ktereho se vysledky voleb v danem okrese ulozi

konkretni priklad:

```bash
python "" Praha-zapad.csv
```
5) Vytvoreny csv soubor s volebnimi vysledky se automaticky ulozi do stejne slozky, ve ktere je i nase virtualni prostredi.


**Ukazka vysledneho csv souboru:**

<img width="1501" height="589" alt="image" src="https://github.com/user-attachments/assets/cbff80ba-d287-40b5-ac7b-4c92acdb645e" />

## Použité knihovny:

