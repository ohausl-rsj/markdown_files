Dokument popisuje, jak je sestaven budget na IT oddělení, resp. jaká je logika excelového souboru, který je předáván vedení jako budget. 

# Popis listů

## data

tento list představuje jednotlivé položky budgetu na daný rok. Níže je popis jednotlivých sloupců.

### Type

Sloupec A s názvem Type, popisuje typ položky.

### Order

Sloupec B s názvem Order, popisuje název objednávky. V datech dodávaných od účetního oddělení, nemusí být tato položka vždy uvedena, ale často ano. Problém nastává, pokud vznikne během roku např. nová objednávka, nebo pokud se nějaká přejmenuje, nebo se při likvidaci faktury nezapíše k položce.

### Supplier

Sloupec C, jedná se o dodavatele dané položky.

### Name_item

Sloupec D, jednotlivé položky. Ne vždy jsou v datech položky takto rozdělené. Např u Azure spotřeby tento detail určitě není. To je třeba do budoucna změnit, případně najít jiný způsob, jak to vyřešit, aby bylo možné rozdělit v konečném vyůčtování a spárovat s konečnými reálnými daty.

### Pcs

Sloupec E, je počet položek, jednotek za kalendářní měsíc. 

### Price_ppc_cur

Sloupec F je cena položky v měně, která je uvedena v sloupci G [Curr](curr). 

### Curr

Sloupec G je měna, v jaké je uvedena [cena položky](price_ppc_cur). Používá se primárně pro přepočet EUR na CZK, jelikož např spotřeba a licence jsou účtováýny v EUR.

### Price_ppc_czk

Ve sloupci H je pak přepočítaná cena z cizí měny na CZK. Pokud je tedy poločka v jiné měně, zde dojde k přepočtu. Vzorec kontroluje zda ve sloupci [Curr](curr) není jiná měna a případně použije vzorec pro přepočet. Výsledkem je, že je každá položka přepočtena na CZK.

### Amount_czk

Ve sloupci I pak doje k přepočítání celkové ceny za počet položek v jednom měsíci v CZK. Vzorec je jednoduchý:

[Pcs](pcs) x [Price_ppc_czk](price_ppc_czk) 

### C1-C12

Sloupce J až K, jsou sloupce které říkají, že tato položka jde v daném měsíci do nákladů, či nikoliv. Pokud je v této buňce 1, znamená to, že v daném měsíci jde položka do nákladů (COST). Pokud je prázdný, tak do nákladů nejde.

### Cost_Multiplication

<!-- tímto polem si teď nejsem jistý, budu muset zjistit, případně budu rád pokud zanalyzuješ a dáš mi vědět -->

### CA_1-CA_12

Sloupce W až AH, jsou na tom podobně jako [COST](c1-c12) s tím rozdílem, že tady se jedná o to, že daná položka vstupuje do budgetu jako CASH.

### Cash_Multiplication

<!-- tímto polem si teď nejsem jistý, budu muset zjistit, případně budu rád pokud zanalyzuješ a dáš mi vědět -->

### PCS_OR_%

Ve sloupci AJ je jen informace, zda se daná položka počítá jako % nebo jako pcs.

> Sloupce AL až CJ teď ignoruj, nejsou aktuálně třeba řešit, jelikož neřešíme finální vyúčtování, ale pouze big picture pro CEO reporting, kde je třeba zjistit, zda jsme s náklady v budgetu obecně.

### 1-12

Sloupce CK až CV znázorňují, kolik daná položka stojí v COST daném měsíci. Vzoreček si vyčteš přímo z tabulky. 

### Cost_RowTotal

sloupec CW je celkový coučet COST za celý rok. 

### CF_1-CF_12

Sloupce CX až DI znázorňují, kolik daná položka vstupuje do rozpočtu jako CASH, tzn. kolik firma reálně zaplatí.

### Cash_RowTotal

sloupec DJ je celkový součet CASH za celý rok.

## Services-%

<!-- tento list zatím nebudu popisovat, není potřeba pro CEO report, jedná se o přepočet na dílčí služby, zase není třeba v aktuální fázi řešit -->

## check

<!-- tímto polem si teď nejsem jistý, budu muset zjistit, případně budu rád pokud zanalyzuješ a dáš mi vědět -->

## Přefakturace

<!-- tímto polem si teď nejsem jistý, budu muset zjistit, případně budu rád pokud zanalyzuješ a dáš mi vědět -->

## WF-DMS-FA

<!-- tímto polem si teď nejsem jistý, budu muset zjistit, případně budu rád pokud zanalyzuješ a dáš mi vědět -->

## SetUp

Na tomto listu jsou pomocné informace pro přepočty. Zatím je zde jen měna a kurz a poměr uživatelů - ten je třeba pro přefakturaci, ale to zatím neřešíme jak je uvedeno výše.

