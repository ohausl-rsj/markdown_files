---
name: pdf-to-word
description: Převede obsah PDF dokumentu do Wordu (DOCX) ve firemní grafické šabloně RSJ (template.docx). Použij, když uživatel chce převést PDF do Wordu, do firemní šablony nebo do firemního formátu.
argument-hint: <cesta ke zdrojovému PDF>
---

# Převod PDF do Wordu podle firemní šablony

## Vstupy

1. **Zdrojové PDF**: cesta je v argumentu `$ARGUMENTS`. Pokud argument chybí, zeptej se uživatele, které PDF má převést.
2. **Šablona**: soubor `template.docx` ve složce tohoto skillu. Je závaznou grafickou a formátovací šablonou výsledného dokumentu. Uživatel ji nepřikládá.

Vytvoř nový dokument DOCX s obsahem převzatým ze zdrojového PDF.

## Předpoklady

- **Python 3.13** s knihovnami `python-docx` a `pdfplumber` (hlavní způsob úpravy dokumentu),
- **Microsoft Word** (vizuální kontrola přes export do PDF, záložní způsob úpravy, pokud Python chybí).

Instalace (PowerShell):

```powershell
winget install Python.Python.3.13
# po instalaci zavřít a znovu otevřít terminál / VS Code
python -m pip install python-docx pdfplumber
```

Pokud příkaz `python` hlásí „Python nebyl nalezen“, vypni v Nastavení → Aplikace → Pokročilá nastavení aplikací → Aliasy spouštění aplikací položky `python.exe` a `python3.exe`.

Před začátkem práce ověř, že je Python dostupný (`python -c "import docx, pdfplumber"`). Pokud není, upozorni na to uživatele a pokračuj záložním způsobem přes Word.

## ZÁSADNÍ POŽADAVEK

Výsledný dokument nevytvářej jako nový dokument pouze vizuálně podobný šabloně. Jako technický základ použij přímo kopii souboru `template.docx`, v ní nahraď původní obsah obsahem ze zdrojového PDF a zachovej její existující styly, motiv, nastavení dokumentu, záhlaví, zápatí, číslování, oddíly a formátování.

`template.docx` je jediným zdrojem pravdy pro vzhled dokumentu. Zdrojové PDF je jediným zdrojem pravdy pro textový obsah a strukturu informací.

Původní `template.docx` ve složce skillu nikdy neupravuj, pracuj vždy jen s jeho kopií.

## Technický postup

1. Přečti zdrojové PDF (nástrojem Read, u delších dokumentů po částech přes parametr `pages`) a zmapuj jeho strukturu: kapitoly a úrovně nadpisů, seznamy, tabulky.
2. Zkopíruj `template.docx` na cílové místo (viz Výstup) pod výsledným názvem.
3. Zjisti, jaké styly šablona obsahuje (nadpisy, běžný text, seznamy, tabulky, obsah) a jak vypadá její titulní strana, záhlaví a zápatí.
4. Uprav kopii šablony:
   - Pokud je k dispozici Python s knihovnou pro práci s DOCX, postupuj podle skillu `docx`.
   - Jinak použij Microsoft Word přes COM automatizaci v PowerShellu (`New-Object -ComObject Word.Application`): otevři kopii, nahraď ukázkový obsah těla dokumentu obsahem z PDF, každému odstavci přiřaď existující styl šablony (`Range.Style`), aktualizuj obsah (`TablesOfContents(1).Update()`), dokument ulož a Word ukonči (`Quit()`), i když skript skončí chybou.
5. Pro vizuální kontrolu výsledek exportuj do PDF (ve Wordu `SaveAs2` s formátem PDF, tj. 17) do dočasné složky (scratchpad), projdi ho po stránkách a porovnej se šablonou. Pomocné PDF po kontrole smaž.

## Požadavky na formátování

1. Použij přesně stejné fonty jako v `template.docx`:
   - rodinu fontu,
   - řez písma,
   - velikosti,
   - barvy,
   - tučné písmo a kurzívu,
   - řádkování a mezery před a za odstavci.

2. Použij výhradně existující styly z `template.docx`:
   - běžný text,
   - hlavní nadpisy,
   - podnadpisy,
   - číslované nadpisy,
   - odrážkové a číslované seznamy,
   - názvy částí dokumentu,
   - obsah dokumentu.

   Nevytvářej nové vizuální varianty stylů a nepoužívej automatickou modrou barvu nadpisů jen proto, že jde o nadpis. Každé úrovni nadpisu přiřaď odpovídající existující styl ze šablony.

3. Zachovej přesně záhlaví a zápatí z `template.docx`:
   - jejich obsah,
   - výšku a umístění,
   - vodorovné čáry,
   - font a barvu textu,
   - označení společnosti,
   - název dokumentu,
   - čísla stran,
   - zarovnání a mezery.

   Záhlaví ani zápatí nevytvářej znovu. Převezmi je přímo ze šablony a změň pouze název dokumentu tam, kde je to nutné.

4. Titulní a úvodní stranu vytvoř podle stejného principu jako v `template.docx`:
   - stejné umístění loga,
   - stejné odsazení,
   - stejný styl názvu dokumentu a podtitulu,
   - stejnou strukturu úvodních údajů,
   - stejné mezery mezi jednotlivými bloky.

5. Všechny tabulky formátuj přesně podle tabulek v `template.docx`:
   - stejné barvy záhlaví,
   - stejné stínování buněk,
   - stejné ohraničení a tloušťku čar,
   - stejné vnitřní okraje buněk,
   - stejný font, velikost a barvu textu,
   - stejné zarovnání textu,
   - stejné odsazení odstavců v buňkách,
   - stejné střídání barev řádků, pokud je v šabloně použito,
   - stejné chování při zalomení tabulky na další stránku,
   - opakování záhlaví tabulky na další stránce, pokud je to vhodné.

   Nepoužívej výchozí styl tabulek Wordu ani vlastní modrou tabulku. Vzhled tabulek musí být převzat přímo z `template.docx`.

6. Obsah dokumentu vytvoř jako skutečný automatický obsah Wordu založený na stylech nadpisů. Použij stejné formátování obsahu jako v `template.docx`.

7. Zachovej strukturu a význam textu ze zdrojového PDF:
   - nepřepisuj význam,
   - nezkracuj text,
   - nedoplňuj vlastní obsah,
   - neupravuj odborné formulace bez výslovného pokynu,
   - zachovej pořadí kapitol, seznamů a tabulek.

8. Odstraň pouze zjevné technické artefakty vzniklé převodem PDF, například:
   - zdvojené odrážky,
   - nesmyslné zalomení slov,
   - samostatné číslování řádků tabulek,
   - text typu „Add cover“, „Select date“ nebo jiné ovládací prvky,
   - prázdné stránky vzniklé převodem,
   - rozdělení jednoho slova mezerou.

   Pokud zdroj obsahuje zjevný překlep nebo nedokončenou větu, obsah svévolně neopravuj. Zachovej původní text a případnou nejasnost uveď pouze v závěrečném shrnutí.

9. Obrázky ze zdrojového PDF není nutné přenášet, pokud nejsou nezbytné pro pochopení obsahu. Logo a grafické prvky z `template.docx` však zachovej.

10. Orientaci stránky zvol podle obsahu:
    - primárně zachovej orientaci použitou v `template.docx`,
    - orientaci měň pouze u širokých tabulek, pokud je to nezbytné,
    - případnou změnu proveď pomocí samostatného oddílu,
    - záhlaví a zápatí musí zůstat konzistentní i v oddílu s jinou orientací.

## KONTROLA KVALITY

Po vytvoření dokumentu proveď vizuální kontrolu výsledku po jednotlivých stránkách. Porovnej dokument s `template.docx` a oprav všechny odchylky v následujících oblastech:

- fonty a řezy písma,
- barvy nadpisů,
- velikosti a úrovně nadpisů,
- odsazení a mezery,
- záhlaví a zápatí,
- číslování stran,
- šířky a vzhled tabulek,
- ohraničení a výplně buněk,
- zalomení stránek,
- osamocené nadpisy na konci stránky,
- překrývající se nebo oříznutý text,
- nekonzistentní seznamy a odrážky.

Dokument nepovažuj za dokončený, dokud nebude vizuální formátování odpovídat `template.docx`, nikoliv pouze přibližně, ale co nejpřesněji v rámci možností Wordu.

Před odevzdáním ověř také, že:

- celý dokument používá styly převzaté z `template.docx`,
- nikde nezůstaly výchozí styly Wordu nebo PDF převodu,
- tabulky nejsou formátovány odlišným stylem,
- záhlaví a zápatí odpovídají šabloně ve všech oddílech,
- v dokumentu nejsou nechtěné modré nadpisy,
- obsah odpovídá skutečným názvům a číslování kapitol.

## Výstup

Výsledný soubor DOCX ulož do stejné složky jako zdrojové PDF. Název výsledného souboru odvoď z názvu zdrojového PDF (stejný název, přípona `.docx`). Pokud soubor s tímto názvem už existuje, nepřepisuj ho a zeptej se uživatele.

Ve složce nenechávej pracovní PDF, náhledové obrázky ani pomocné soubory.

Na závěr uživateli stručně napiš, kam byl soubor uložen, a uveď případné nejasnosti ve zdrojovém textu (překlepy, nedokončené věty) nebo místa, kde se formátování nepodařilo plně sladit se šablonou.

## DŮLEŽITÉ TECHNICKÉ OMEZENÍ

Nevytvářej dokument od prázdné stránky a nesnaž se vzhled `template.docx` ručně napodobit. Otevři `template.docx`, vytvoř jeho kopii a pracuj uvnitř této kopie. Zachovej původní definice stylů a formátování v souboru. Text zdrojového PDF vlož do odpovídajících existujících prvků šablony a aplikuj na něj existující styly šablony. Ruční formátování používej pouze tam, kde v `template.docx` pro daný prvek neexistuje odpovídající styl.
