# Election scraper (projekt 3)

Cílem tohoto projektu bylo vytvořit python script, který stáhne výsledky voleb do Poslanecke sněmovny z roku 2017  (z tohoto [odkazu](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ)) pro libovolný vybraný okres z webového odkazu a uloží jej do csv souboru.

**Depozitář projektu obsahuje tyto soubory:**
1) main.py (exekuční skript)
2) requirements.txt (seznam potrebnych knihoven pro správné fungování kódu)
3) Praha-zapad.csv (ukazka vytvoreneho souboru se stazenymi výsledky voleb pro okres Praha-západ)
4) README.md (tento soubor s popisem projektu a postupem spuštění a fungování skriptu)

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
Je vidět, že příkaz obsahuje 2 argumenty - 1) URL v uvozovkach a 2) nazev csv souboru, do ktereho se vysledky voleb v danem okrese ulozi

konkrétni příklad:

```bash
python "" Praha-zapad.csv
```
5) Vytvoreny csv soubor s volebnimi vysledky se automaticky ulozi do stejne slozky, ve ktere je i nase virtualni prostredi.


**Ukazka vysledneho csv souboru:**

<img width="1501" height="589" alt="image" src="https://github.com/user-attachments/assets/cbff80ba-d287-40b5-ac7b-4c92acdb645e" />


## Použité knihovny:
beautifulsoup4==4.13.4

certifi==2025.4.26

charset-normalizer==3.4.2

idna==3.10

requests==2.32.4

soupsieve==2.7

urllib3==2.4.0
