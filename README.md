# Election scraper (projekt 3)

Cílem tohoto projektu bylo vytvořit python script, který stáhne výsledky voleb do Poslanecké sněmovny ČR z roku 2017  (z tohoto [odkazu](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ)) pro libovolný vybraný okres (po rozkliknutí jeho kódu nebo symbolu X ve sloupci "Výběr obce") z webového odkazu a uloží jej do csv souboru.


**Depozitář projektu obsahuje tyto soubory:**
1) main.py (exekuční skript)
2) requirements.txt (seznam potrebnych knihoven pro správné fungování kódu)
3) Praha-zapad.csv (ukazka vytvoreneho souboru se stazenymi výsledky voleb pro okres Praha-západ)
4) README.md (tento soubor s popisem projektu a postupem spuštění a fungování skriptu)

## Postup pro spuštění skriptu:
1) Nejprve je potřeba si vytvořit virtuální prostředí, např. venv_project3, ve Windows Powershell to bude takto:
   
```bash
python -m venv venv_project3
```

2) Do stejné složky jako máme vytvořené virtuální prostředí je třeba uložit soubor main.py se zdrojovým kódem a taky soubor requirements.txt, který obsahuje seznam python knihoven, které jsou potřebné ke správnému fungování kódu.

3) Následně pak spustíme instalaci potřebných knihoven pro fungování kódu uvnitř našeho prostředí pomocí souboru requirements.txt:
   
```bash
pip install -r requirements.txt
```
4) Pak už je možné spustit skript příkazem ve tvaru:
 
```bash
python "webova_adresa_s_vysledky_voleb_v_danem_okrese" nazev_souboru.csv
```
Je vidět, že příkaz obsahuje 2 argumenty - 1) URL v uvozovkách a 2) název csv souboru, do kterého se výsledky voleb v daném okrese uloží

**Konkrétni příklad:**

```bash
python "https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xnumnuts=2110" Praha-zapad.csv
```
5) Vytvořený csv soubor s volebními výsledky se automaticky uloží do stejné složky, ve které je i naše virtualní prostředí.


**Ukázka výsledného csv souboru:**

<img width="1501" height="589" alt="image" src="https://github.com/user-attachments/assets/cbff80ba-d287-40b5-ac7b-4c92acdb645e" />


## Použité knihovny:
beautifulsoup4==4.13.4

certifi==2025.4.26

charset-normalizer==3.4.2

idna==3.10

requests==2.32.4

soupsieve==2.7

urllib3==2.4.0
