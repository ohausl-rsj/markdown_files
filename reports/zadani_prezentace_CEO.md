# Zadání prezentace: CEO reporting IT, Data & AI Automation

Tento dokument popisuje, jak má prezentace vypadat. Obsah čerpej výhradně z podkladového dokumentu [`q3_report_ideas.md`](q3_report_ideas.md) (dále jen *podklad*), který je uložený ve stejné složce jako toto zadání. Nic nevymýšlej a nedoplňuj čísla, data ani fakta, která v podkladu nejsou.

## 1. Základní parametry

- **Výstup:** PowerPoint (.pptx), formát 16:9
- **Rozsah:** 13 slidů hlavní části + případná příloha (max. 15 slidů celkem)
- **Jazyk:** čeština, české uvozovky „ “
- **Publikum:** CEO investiční skupiny. Netechnický, ale zkušený manažer. Zajímá ho stav, přínosy pro byznys, rizika a směr, ne technické detaily.
- **Cíl:** informovat o stavu IT útvaru, projektů a o výhledu. Prezentace o nic nežádá ke schválení.
- **Prezentující:** Ondřej Hausl, vedoucí IT útvaru. Prezentace je psaná z jeho pohledu.

## 2. Hlavní sdělení

Celou prezentací se musí táhnout tato tři sdělení:

1. **Stabilizace a profesionalizace:** po obtížném startu (odchod 2 ze 3 techniků) je IT útvar stabilizovaný a pracuje řízeně.
2. **Tuning, ne nové hračky:** v souladu s požadavkem CEO ladíme a naplno využíváme stávající systémy. Nové projekty jen tam, kde stávající řešení nevyhovuje.
3. **AI jako hlavní směr:** AI zavádíme řízeně a stavíme pro ni kvalitní datový základ a moderní cloudové prostředí.

Zároveň musí být vidět **provázanost a spolupráce s IS útvarem RSJ Custody** (Tomáš Málek). To je výslovný požadavek z podkladu.

## 3. Struktura slidů

### Slide 1 – Titulní slide
- Název: „IT, Data & AI Automation“
- Podtitul: „Stav útvaru, projektů a výhled“
- Ondřej Hausl, vedoucí IT útvaru · listopad 2026

### Slide 2 – Shrnutí
- 3–4 klíčová sdělení z kapitoly 2 tohoto zadání, každé jednou větou.
- Volitelně 3 velká čísla, např. počet projektů v přehledu, počet projektů v provozu, počet AI projektů (spočítej z tabulky Přehled projektů v podkladu).

### Slide 3 – Výchozí stav a požadavek CEO
- Zdroj: úvod podkladu a kapitola *Vývoj IT týmu*.
- Požadavek CEO na tuning stávající infrastruktury a aplikací.
- Nástup 9/2025, odchod 2 ze 3 techniků, rychlé doplnění týmu.
- Formuluj věcně, bez hodnocení minulosti.

### Slide 4 – IT prostředí a bezpečnost
- Zdroj: *Technologický stack*, *Bezpečnost*, *Aplikace*.
- Princip **cloud first** jako hlavní sdělení slidu.
- Jednoduchý vizuál vrstev: on-premise (jen síť v kanceláři) → IaaS (Azure VM) → PaaS → SaaS (M365).
- Bezpečnost: Defender XDR + Sentinel a model tří linií obrany jako malý diagram (1. linie IT, 2. linie IKT risk a Compliance, 3. linie interní audit).
- Tabulku aplikací na slide nedávej, stačí zmínka o počtu klíčových aplikací. Tabulka může jít do přílohy.

### Slide 5 – Tým dnes
- Zdroj: *Aktuální složení*, *Data & reporting*, *Externí partneři*, *Oblasti odpovědnosti IT*.
- Jednoduchý organigram: Core IT, Data & reporting, AI automatizace, externí partneři (RSJ Custody, Orbit, Jakub Filip).
- Uveď jména a role, **bez osobního hodnocení lidí**.
- Zvýrazni hlavní riziko: security nemá vlastníka a některé oblasti stojí na jednom člověku.

### Slide 6 – Přehled projektů
- Zdroj: tabulka *Přehled projektů*.
- Klíčový slide prezentace. Vizuálně zobraz všechny projekty podle fáze na ose **Nápad → Analýza → PoC → Realizace → Pilot → Dokončení → Provoz**, barevně rozlišené podle oblasti (Core IT, AI automatizace, Development, Reporting).
- Projekty s RSJ Custody označ ikonou nebo štítkem, aby byla vidět spolupráce.

### Slide 7 – Core IT projekty
- MS Sentinel, Propojení HR modulu BOSS s AD, RBAC, IT service management v Alvao.
- U každého: název, fáze, jedna věta přínosu.
- Zdůrazni návaznost: HR data → AD/Entra ID → RBAC, vše pod dohledem Sentinelu.

### Slide 8 – AI automatizace
- AI reporting pro PE/VC tým, AI posouzení LPA, AI vytěžování faktur.
- U každého: název, fáze, jedna věta přínosu pro byznys.
- Zmiň řízené zavádění: PoC → pilot → provoz, kontrola výstupů člověkem.

### Slide 9 – Development a Reporting
- MDM, Založení fondu, DMS, Auditní workflow, Projects, Invoices, Migrace DWH do Fabricu.
- Zvýrazni příběh **migrace z on-premise SharePointu**: DMS → Projects → Invoices → odstavení SharePointu a AD (2028).
- MDM jako jeden zdroj pravdy, na který se napojují další systémy.
- Pokud u projektu chybí údaje (Auditní workflow, Fabric), uveď jen to, co v podkladu je.

### Slide 10 – Spolupráce s RSJ Custody
- Projekty realizované společně s IS útvarem RSJ Custody: Propojení HR modulu BOSS s AD, MDM, Založení fondu, Auditní workflow.
- Sdělení: společně posouváme klíčové projekty skupiny, spolupráce funguje.

### Slide 11 – Budget
- Kapitola je v podkladu zatím nevyplněná. Pokud bude stále prázdná, vytvoř slide s nadpisem „Budget“ a strukturou připravenou k doplnění: plán vs. skutečnost k Q2 (tabulka nebo sloupcový graf s prázdnými hodnotami).
- **Nevymýšlej žádná čísla.**

### Slide 12 – Cílový model týmu
- Zdroj: *Cílový model IT týmu*.
- Princip: nenavyšovat, ale zajistit kompetence, kontinuitu a nezávislost na jednotlivcích.
- Vizuál 4 týmů (Provoz, Bezpečnost, Rozvoj, Data a reporting) s interní a externí kapacitou.
- Nové role (security & cloud administrátor, datový specialista) jako výhled, interní kapacita 6 → 8.
- Variantu s rozvojem Jana Kridla na slide **nedávej**, uveď ji jen v poznámkách pod slidem.

### Slide 13 – Strategie projektů a výhled
- Zdroj: *Strategie projektů*.
- Hlavní sdělení nahoře: AI jako hlavní směr.
- 4 pilíře jako 4 karty s ikonami: Ladění stávajících systémů, AI, Kvalitní data, Cloud first.
- Pod nimi časová osa z tabulky *Výhled*: do konce 2026 → 2027 → 2028 → dlouhodobě.

### Příloha (volitelně, max. 2 slidy)
- Tabulka aplikací.
- Detailní tabulka projektů (oblast, fáze, partner, termíny).

## 4. Vizuální styl

- Firemní šablona není k dispozici, navrhni čistý, profesionální vzhled vhodný pro finanční sektor.
- Barvy: tmavě modrá jako hlavní, šedé tóny, jedna akcentní barva pro zvýraznění. Barvy oblastí projektů drž konzistentní napříč všemi slidy.
- Nadpis každého slidu formuluj jako **sdělení**, ne jako téma (např. „Bezpečnost má nástroje, chybí jí vlastník“ místo „Bezpečnost“).
- Max. 5 odrážek na slide a krátké formulace. Detaily patří do poznámek.
- Preferuj vizuály před textem: časové osy, diagramy, karty, ikony, organigram.
- Číslování slidů a v zápatí „RSJ Investments · IT, Data & AI Automation“.

## 5. Poznámky pod slidy

Ke každému slidu napiš do poznámek pro řečníka 3–6 vět s detaily z podkladu, které se na slide nevešly. Poznámky jsou psané v první osobě (Ondřej).

## 6. Co nepřebírat z podkladu

- HTML komentáře (`<!-- -->`) a pracovní poznámky v hranatých závorkách.
- Zástupné texty `...`, `[doplnit]` a podobně. Pokud údaj chybí, vynech ho.
- **Osobní hodnocení lidí** (silné a slabé stránky, výkon jednotlivců). U personálních změn uveď jen fakt, např. „k 31. 12. 2026 končí jeden IT administrátor“.
- Hodnotící poznámky o organizačním zařazení Dušana Marka. Uveď jen věcně, že je formálně zaměstnancem RSJ Custody a je plně alokován pro RSJ Investments.
- Technické detaily, které CEO nepotřebuje (typy licencí, počty VM, názvy jednotlivých procesů ITSM). Pokud jsou důležité, dej je do poznámek.

## 7. Kontrola před odevzdáním

- Všechna data, názvy a fáze projektů odpovídají podkladu.
- Žádný slide nepřetéká textem.
- Barvy oblastí jsou konzistentní napříč slidy.
- Ke každému slidu existují poznámky pro řečníka.
