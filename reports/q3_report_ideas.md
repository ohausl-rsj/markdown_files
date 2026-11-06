# CEO reporting IT, Data & AI Automation

Hlavním požadavkem CEO na začátku roku bylo, aby proběhl tzv. tuning aktuální infrastruktury a aplikací. Není třeba vymýšlet nové projekty, ale spíše vyladit to, co už máme.

## Hlavní body

- **Vývoj IT týmu** přes obnovu týmu, až po nové rozdělení [budeme ihned navazovat na nové rozdělení týmu, nebo až na konci]
- **Projekty** aktuální stav projektů od myšlenky až po produkci [projekty jsou rozdělené na Core IT, AI, development, reporting]
- **Budget** stav k Q2 a vyhodnocení vzhledem plánu, případně doplnění výhledu
- **Strategie** jaký je výhled jak ve složení IT týmu, tak v projektech. Jaký je ideální cílový stav, kam bychom chtěli směrovat v dalších obdobích.

> celá prezentace bude propojena i se stavem projektů, které má na starosti tým IS oddělení Tomáše Málka z RSJ Custody. Musí být vidět provázanost a to, že společně na projektech pracujeme a úspěšne posouváme dále.

## Profil společnosti

Jedná se o investiční skupinu, která čítá několik společností. Naše IT oddělení působí napříč dvěma společnostmi ze skupiny:

1. **RSJ Investments a. s.** - hlavní společnost, jelikož se jedná o regulovaný subjekt, který spadá pod ČNB (DORA)
2. **RSJ Services s. r. o.** - jedná se o servisní společnost, která působí jako dodavatel (třetí strana) pro RSJ Investments. IT oddělení je téměř celé aktuálně pouze na RSJ Services. Pouze já mám úvazek i na RSJ Investments a. s. (80%)

Dále v rámci skupiny spolupracujeme s další společností a to je **RSJ Custody a. s.**. Tato společnost je také regulovaná a pod tuto společnost spadá vývojové oddělení informačních systémů. Programují pro nás různé aplikace (BOSS, WF založení fondu aj.). Vedoucím tohoto oddělení je **Tomáš Málek** a má pod sebou několik programátorů. Zároveň pod něj organizačně spatá i **Dušan Marko**, ale zároveň 100% jeho FTE je alokováno právě pro nás jako pro RSJ Investments, jelikož pro nás dělá činnosti viz. [Dušan Marko](#dusan-marko).

## Technologický stack

> Společnost je razí fylozofii **cloud first**. 

- Lokální/on-premise infrastruktura - kancelář Praha, pouze Unifi UDM SE, switche, AP, kamery, senzory
- Azure VM - IaaS, celkem 14 VM's
- Azure App Service, Azure SQL Server, DB, Blob storage, VNET, apod. - PaaS
- M365 - SaaS

V rámci M365 využíváme téměř celé portfolio aplikací, které M365 nabízí, včetně Intune, Defender, apod.. Samozřejmostí je MS Exchange, Sharepoint Online, M365 Copilot, EntraID. Máme licence M365 E5 a někteří uživatelé dokonce M365 E7.

Na VM's v Azure stále provozujeme Active Directory, které je nezbytné pro provoz DMS aplikace, která není nic jiného, než upravený on-premise SharePoint. Aktuálně probíhá projekt, který všechny funkcionality z tohoto Sharepointu přesune do aplikací založených na PaaS, Active Directory se zruší a zůstane pouze EntraID.

> Strategie do budoucna je zbavit se lokálního AD a provozovat pouze EntraID identity.

### Bezpečnost

Jako primární bezpečnostní systém používáme MS Defender XDR a jako SIEM nástroj MS Sentinel v Azure. Samostatná security pozice aktuálně neexistuje, agenda je sdílená mezi IT administrátory a dohled supluje vedoucí IT.

Vzhledem k tomu, že RSJ Investments je regulovaná společnost, řídí se bezpečnost a IKT riziko modelem tří linií obrany:

| Linie | Kdo | Role |
|---|---|---|
| 1. linie – výkon | IT útvar (vedoucí IT, administrátoři) | provoz Sentinelu, Defenderu a Purview, reakce na incidenty, školení, podklady a data pro DORA |
| 2. linie – nezávislý dohled | IKT risk manažer **Jan Kubíček**, Compliance **Petra Šilhová** (mimo IT útvar) | metodika, hodnocení a klasifikace rizik, reporting vedení a ČNB, soulad s DORA |
| 3. linie – nezávislé ověření | Interní audit | ověřuje, že 1. a 2. linie fungují |

> Princip: IT jako 1. linie dodává data, 2. linie je nezávisle hodnotí. Security tak nehodnotí účinnost vlastních opatření.

## Aplikace

zde je výpis námi vyvýjených a provozovaných aplikací. Případně aplikací, které jsou vyvýjené a provozované RSJ Custody IS týmem.

| Aplikace | Popis | Provozní model | Umístění | Správce | Vývoj/dodavatel |
|---|---|---|---|---|---|
| BOSS | Informační systém pro RSJ Investments, slouží jako evidence kovenantů, úvěrových smluv apod., dále obsahuje modul HR | SaaS | ... | RSJ Custody | RSJ Custody |
| Založení fondu | Workflow aplikace na založení fondu | PaaS | Azure | RSJ Custody | RSJ Custody |
| MDM | Master data management – zdroj pravdy pro data | PaaS | Azure | RSJ Services (J. Kridlo) | Dušan Marko |
| Cashflow | Plánování budgetů na fondech, využívá MDM | PaaS | Azure | RSJ Services | Dušan Marko |
| DWH | Datový sklad, zdroj dat pro reporting | PaaS | Azure | RSJ Services (D. Marko) | Dušan Marko |
| Power BI | Reporting pro RSJ Investments a RSJ Services | SaaS | M365 | RSJ Services (M. Bartošová) | M. Bartošová |
| DMS | Document management system, archiv smluv a ostatní dokumentace pro fondy a SPV | IaaS | Azure | RSJ Services (J. Kridlo) | SharePoint Solutions s. r. o. |
| Projects | Workflow investičních rozhodnutí – fyzicky běží na on-premise SharePointu | IaaS | Azure | RSJ Services (J. Kridlo) | SharePoint Solutions s. r. o. |
| Invoices | Workflow na schvalování faktur – fyzicky běží na on-premise SharePointu | IaaS | Azure | RSJ Services (J. Kridlo) | SharePoint Solutions s. r. o. |
| Helios – Fondy | Účetnictví pro fondy | SaaS | ... | RSJ Custody | RSJ Custody |
| Helios – SPV | Účetnictví pro SPV | SaaS | ERPORT | RSJ Services | Nesos |
| Alvao | IT ServiceDesk a HelpDesk, finanční a legal helpdesk | SaaS | Azure | RSJ Services | Alvao |

## Oblasti odpovědnosti IT

Kromě správy aplikací (viz [Aplikace](#aplikace)) drží IT útvar tyto oblasti:

| Oblast | Co zahrnuje | Kdo dnes drží |
|---|---|---|
| Podpora uživatelů | L1, servisní požadavky, tiskárny, HW | J. Kridlo |
| Endpoint | stanice, Intune, správa zařízení | J. Kridlo, J. Severa, F. Urban |
| Cloud a identita | M365, Azure, Entra ID | J. Severa, F. Urban |
| Síť a infrastruktura | VPN, firewall, storage, backup | F. Urban |
| Security | Sentinel, Defender, incidenty | sdílená, **bez vlastníka** |
| Vývoj a AI automatizace | Power Automate, integrace, AI řešení | F. Urban, J. Filip (ext.) |
| Governance | pravidla, audit, dokumentace, DORA | O. Hausl |
| Projekty | koordinace, změny, migrace | O. Hausl, všichni |

## Vývoj IT týmu

> Nebudeme hodnotit to, co bylo v loňském roce, ale důležitá informace je, že jsem nastoupil 1. 9. 2025 a ihned po mém nástupu, odešli 2 technici ze 3. Byly to navíc ještě ti, na kterých to stálo. Oba zkušení. Zbyl pouze L1 technik Jan Kridlo. Tyto techniky se mi podařilo velice rychle nahradit, nastoupl Frederik a Jiří.

### Aktuální složení

#### Core IT tým

Níže je uvedeno aktuální složení IT týmu a jejich základní kompetence, znalosti, dovednosti a opovědnosti.

1. **Ondřej Hausl** (Vedoucí IT útvaru) - moje pozice, nastoupil jsem 1. 9. 2025 jako vedoucí celého oddělení. Práci mi částečně předal bývalý kontraktor, který nadále působí jako externí projektový manažer.
2. **Jan Kridlo** (IT administrátor) - L1 support a správa DMS, Projects, Invoices a MDM. Je zodpovědný, věci dotahuje do konce, ale chybí mu tah na branku a nedokáže převzít zodpovědnost.
3. **Frederik Urban** (IT administrátor) - nastoupil 2. 2. 2026 jako IT administrator se zkušenostmi s programováním. Postupně se profiloval a od října 2026 je plně alokován na vývoj AI automatizací. Z Core IT týmu tak plně odešel.
4. **Jiří Severa** (IT administrátor) - nastoupil 1. 1. 2026 jako IT administrator. Vize byla, že tento technik bude postupně nabírat zkušenosti a stane se lídrem celého týmu. Bohužel, zhruba po 3 měsících, jeho výkon začal rapidně klesat. I přes neustálou práci s ním, nedošlo ke zlepšení a proto jsem se rozhodl v říjnu 2026, že mu neprodloužím smlouvu. 31. 12. 2026 tak končí.Měl mít na starosti kompletní cloudovou a lokální infrastrukturu, hlavně z pohledu bezpečnosti.

> cílem není tým nijak navyšovat, ale profesionalizovat.

#### Data & reporting

Reporting byl při mém nástupu formálně i odpovědně zařazen pod Finanční útvar Marka Capáka (CFO). V průběhu roku jsme ale navázali úzkou spolupráci a aktuálně je domluveno s Markem, že si reporting převezmu také pod sebe do IT útvaru. Zatím ne formálně, ale jen organizačně. Níže je tedy uvedeno složení reporting týmu.

1. **Marina Bartošová** (Reportingový specialista) - tvoří a spravuje reporty pro RSJ Investments a RSJ Services. Data v rámci DWH připravuje Dušan Marko.

#### Externí partneři

1. **Dušan Marko** <a id="dusan-marko"></a>
   - formálně zaměstnancem RSJ Custody, proto je zde veden jako externí partner, ale je 100% alokován pouze pro RSJ Investments.
   - celkový úvazek je ale pouze 80%. Úvazek snížil na začátku roku 2026.
   - jeho primární odpovědnost je za vývoj MDM, Cashflow, DWH.
   - formálně tak reportuje Tomášovi Málkovi, ale oficiálně mě, jelikož mám na starost řízení projektů v rámci RSJ Investments.

   > tato roztříštěnost u Dušana není optimální, jelikož není silná páka na jeho řízení. Obecně to ale funguje.
2. **IS útvar RSJ Custody a. s.**
   - Odpovědná osoba je vedoucí Tomáš Málek - primární kontakt pro mě jako vedoucího IT útvaru
   - máme pravidelné schůzky a komunikace i spolupráce probíhá bez problémů
3. **Orbit s. r. o.**
   - partner, který nám dodáva licence, řeší Azure subscription a poskytuje jak konzultace, tak případné vykrytí kapacit
   - silný v security, M365 a Azure
4. **Jakub Filip**
   - spolupráci jsme začali až v srpnu 2026
   - externí konzultant na vývojové věci, primárně kolem AI automatizací
   - spolupracuje především s Frederikem, ale plánuji jeho využití i na Data governance

## Projekty

Projekty jsou rozdělené do čtyř oblastí: Core IT, AI automatizace, development a reporting. U každého je uvedena fáze od myšlenky až po produkci:

**Nápad → Analýza → PoC → Realizace → Pilot → Dokončení → Provoz**

### Přehled projektů

| Projekt | Oblast | Fáze | Partner | Zahájení | Plánované dokončení |
|---|---|---|---|---|---|
| [MS Sentinel](#ms-sentinel) | Core IT | Dokončení | Orbit | 5/2026 | 11/2026 |
| [Propojení HR modulu BOSS s AD](#propojení-hr-modulu-boss-s-ad) | Core IT | Provoz | RSJ Custody (IS útvar) | 03/2026 | 09/2026 |
| [RBAC](#rbac) | Core IT | Realizace | interně | 04/2026 | dlouhodobý |
| [IT service management v Alvao](#it-service-management-v-alvao) | Core IT | Provoz | interně | 9/2025 | 02/2026 |
| [AI reporting pro PE/VC tým](#ai-reporting-pro-pevc-tým) | AI automatizace | Pilot | interně | 06/2026 | ... |
| [AI posouzení LPA](#ai-posouzení-lpa) | AI automatizace | PoC | Jakub Filip | 09/2026 | ... |
| [AI vytěžování faktur](#ai-vytěžování-faktur) | AI automatizace | Analýza | Jakub Filip | 10/2026 | ... |
| [MDM](#mdm) | Development | Provoz, další rozvoj | D. Marko (RSJ Custody) | před 9/2025 | Průběžně |
| [Založení fondu](#založení-fondu) | Development | Pilot | RSJ Custody (IS útvar) | 03/2026 | 12/2026 |
| [DMS](#dms) | Development | Dokončení | SharePoint Solutions s. r. o. | 04/2026 | ... |
| [Auditní workflow](#auditní-workflow) | Development | PoC | RSJ Custody (IS útvar) | 11/2026 | ... |
| [Projects](#projects) | Development | Analýza | SharePoint Solutions s. r. o. | 09/2026 | 04/2027 |
| [Invoices](#invoices) | Development | Nápad | SharePoint Solutions s. r. o. | 2027 | 2027 |
| [Migrace DWH do Fabricu](#migrace-dwh-do-fabricu) | Reporting | Analýza | výběrové řízení | ... | ... |

### Core IT

#### MS Sentinel

- **Cíl:** vyladit stávající SIEM tak, aby pokrýval všechny klíčové systémy, spolehlivě odhaloval bezpečnostní hrozby a podezřelé aktivity a na vybrané situace automaticky reagoval.
- **Partner:** Orbit s. r. o.
- **Zahájení:** květen 2026
- **Fáze:** Dokončení
- **Přínos:** plný přehled o bezpečnosti celého prostředí, rychlejší odhalení hrozeb s menším počtem planých poplachů a automatická reakce na běžné situace. Zároveň máme podklady pro DORA a naplno využíváme nástroj, za který už platíme.

**Průběh:**

- [x] Napojení všech aplikací a systémů
- [x] Ladění detekčních pravidel
- [x] Playbooky (automatizovaná reakce na incidenty)
- [ ] Workbooky (přehledy a vizualizace) – *probíhá*
- [ ] Dokumentace
- [ ] Předání a ukončení projektu

**Další krok:** po ukončení projektu převezme Sentinel do vlastnictví nová role security & cloud administrátora (viz [Strategie](#strategie)) a bude ho dále rozvíjet.

#### Propojení HR modulu BOSS s AD

- **Cíl:** vytvořit jeden zdroj pravdy o zaměstnancích. Data vznikají na HR v modulu BOSS a automaticky se přenášejí do identit v AD a Entra ID.
- **Partner:** RSJ Custody (IS útvar)
- **Zahájení:** 03/2026
- **Fáze:** Provoz
- **Přínos:** údaje o zaměstnancích a jejich úvazcích na jednotlivých společnostech jsou ve všech systémech stejné a aktuální, bez ručního přepisování. Celý proces je auditovatelný a je základem pro zavedení řízení rolí a oprávnění (RBAC).

**Průběh:**

- [x] Export dat o zaměstnancích z HR modulu BOSS (RSJ Custody)
- [x] Skript a procedura pro přenos dat do AD (IT útvar)
- [x] Synchronizace z AD do Entra ID
- [x] Odesílání logů do MS Sentinel a workbook pro dohled nad synchronizací

**Návaznost:** projekt je předpokladem pro zavedení modelu řízení rolí a oprávnění (RBAC). Logy procedur jsou napojené do [MS Sentinel](#ms-sentinel), celé řešení je tak provázané od zdroje dat až po bezpečnostní dohled.

#### IT service management v Alvao

- **Cíl:** rozšířit Alvao z jednoduchého helpdesku na plnohodnotný IT service management s řízenými procesy a evidencí IT aktiv podle požadavků DORA.
- **Partner:** interně
- **Zahájení:** září 2025
- **Fáze:** Provoz, průběžné ladění procesů a doplňování CMDB
- **Přínos:** všechny požadavky, změny a incidenty procházejí jednotným řízeným procesem a jsou dohledatelné. V CMDB máme přehled o IT aktivech a jejich vazbách, takže u každé změny nebo incidentu víme, čeho se týká. Splňujeme tím požadavky DORA na řízení incidentů, změn a evidenci IKT aktiv a máme z Alvao data pro reporting a vyhodnocování vytížení týmu.

**Zavedené procesy:**

- [x] Request fulfillment (vyřizování požadavků)
- [x] Identity management (správa uživatelů a přístupů)
- [x] Change management (řízení změn)
- [x] Incident management (řízení incidentů)
- [x] Problem management (řešení příčin opakovaných problémů)
- [x] Threat management (řízení hrozeb)
- [x] CMDB – databáze konfiguračních položek (průběžně doplňována)

#### RBAC

- **Cíl:** zavést řízení oprávnění podle rolí místo nastavování přístupů jednotlivým uživatelům, napříč všemi systémy.
- **Partner:** interně
- **Zahájení:** 04/2026
- **Fáze:** Realizace (dlouhodobý projekt)
- **Přínos:** každý zaměstnanec má přesně ta oprávnění, která potřebuje pro svou roli. Nástup, změna pozice i odchod se řeší přiřazením role, ne ručním nastavováním v každém systému. Oprávnění jsou přehledná a auditovatelná, což je jeden z požadavků DORA na řízení přístupů.

**Průběh:**

- [ ] Zmapování všech systémů a jejich oprávnění – *probíhá*
- [ ] Definice rolí - *probíhá*
- [ ] Nastavení oprávnění podle rolí v jednotlivých systémech
- [ ] Pravidelná revize rolí a oprávnění

**Návaznost:** zdrojem informací o zaměstnancích, jejich pozicích a úvazcích je [Propojení HR modulu BOSS s AD](#propojení-hr-modulu-boss-s-ad).

### AI automatizace

#### AI reporting pro PE/VC tým

- **Cíl:** nahradit manuální zpracování dat pro PE/VC tým opakovatelným a auditovatelným procesem.
- **Partner:** interně
- **Zahájení:** 06/2026
- **Fáze:** Pilot
- **Přínos:** úspora času PE/VC týmu na ručním zpracování dat, menší riziko chyb díky automatické validaci a dohledatelnost každého kroku. Data jsou uložená strukturovaně a připravená pro reporting a vizualizace.

**Jak řešení funguje:**

1. zpracuje vstupní data,
2. pomocí AI z nich vytěží a strukturuje potřebné informace,
3. provede validaci,
4. uloží je do databáze pro další reporting a vizualizaci.

**Průběh:**

- [x] Vývoj řešení
- [ ] Pilotní provoz s PE/VC týmem – *probíhá*
- [ ] Napojení na MDM – *probíhá*
- [ ] Napojení výstupů na Power BI

**Návaznost:** řešení se napojuje na [MDM](#mdm) jako zdroj kmenových dat a výstupy budou postupně napojené na Power BI, tedy do oblasti [Data a reporting](#data--reporting).

#### AI posouzení LPA

- **Cíl:** pomocí AI posuzovat smlouvy LPA (Limited Partnership Agreement) podle definovaných pravidel a upozorňovat na odchylky.
- **Partner:** Jakub Filip
- **Zahájení:** 09/2026
- **Fáze:** PoC
- **Přínos:** rychlejší a konzistentní kontrola smluv podle jednotných pravidel, úspora času týmu při revizi a menší riziko přehlédnutí důležitých ustanovení.

**Průběh:**

- [x] Definice pravidel pro posouzení
- [ ] Proof of Concept – *probíhá*
- [ ] Vyhodnocení PoC a rozhodnutí o realizaci

#### AI vytěžování faktur

- **Cíl:** zefektivnit práci backoffice. Faktury budou programově a pomocí AI vytěžené na jednotlivé položky a do aplikace [Invoices](#aplikace) se zapíší správné údaje, které dnes ručně řeší backoffice, účetní nebo likvidátor.
- **Partner:** Jakub Filip
- **Zahájení:** 10/2026
- **Fáze:** Analýza
- **Přínos:** úspora času backoffice a účetních na ručním přepisování, méně chyb při zadávání a rychlejší zpracování faktur.

**Průběh:**

- [ ] Analýza – *probíhá*
- [ ] Vytěžení faktur na jednotlivé položky a zápis do Invoices
- [ ] Rozšíření: AI pomáhá s doplňováním zakázek a dalších informací k fakturám a položkám

**Návaznost:** projekt přímo navazuje na workflow schvalování faktur v aplikaci [Invoices](#invoices).

### Development

#### MDM

- **Cíl:** vytvořit jeden zdroj pravdy pro kmenová data (subjekty, společnosti a jejich vazby) a napojit na něj všechny klíčové systémy.
- **Partner:** Dušan Marko (RSJ Custody)
- **Zahájení:** před 9/2025 (projekt jsem převzal v běhu), v produkci od 7/2026
- **Fáze:** Provoz, další rozvoj
- **Přínos:** subjekty vznikají pouze v MDM, takže nevznikají duplicity a všechny napojené systémy pracují se stejnými daty. Ruční zakládání a opravy dat v jednotlivých systémech odpadají.

**Aktuálně řešené oblasti:** (***doladění detailů doplnit***)

**Průběh:**

- [x] Spuštění do produkce (7/2026)
- [x] Napojení na Helios – Fondy
- [x] Napojení na Helios – SPV
- [x] Zakládání subjektů výhradně v MDM
- [ ] ***doladění detailů doplnit*** – *probíhá*
- [ ] Napojení na ostatní klíčové systémy (dílčí projekty) – *probíhá*

**Návaznost:** MDM je zdrojem kmenových dat pro [Helios – Fondy a Helios – SPV](#aplikace) a pro [Cashflow](#aplikace). Napojuje se na něj i [AI reporting pro PE/VC tým](#ai-reporting-pro-pevc-tým).

#### Založení fondu

- **Cíl:** převést celý proces založení fondu do jednotné workflow aplikace.
- **Partner:** RSJ Custody (IS útvar, T. Málek)
- **Zahájení:** 03/2026
- **Fáze:** Pilot
- **Přínos:** založení fondu probíhá jednotným řízeným procesem, všichni zúčastnění vidí, v jakém je stavu, a každý krok je dohledatelný. Menší riziko, že se v procesu něco opomene.

**Průběh:**

- [x] Vývoj workflow aplikace (RSJ Custody)
- [ ] Pilot – *probíhá*: několik fondů založených starým procesem souběžně prochází i novou aplikací
- [ ] Vydání instrukcí pro uživatele
- [ ] Ostrý provoz

#### DMS

- **Cíl:** nahradit původní nevyhovující DMS novým systémem na PaaS a sjednotit do něj dokumentaci fondů i SPV.
- **Partner:** SharePoint Solutions s. r. o.
- **Zahájení:** 04/2026
- **Fáze:** Dokončení
- **Přínos:** moderní a udržitelný systém v souladu s cloud first strategií, veškerá dokumentace fondů i SPV na jednom místě. Zároveň jde o klíčový krok k odstavení on-premise SharePointu a lokálního AD.

**Průběh:**

- [x] Vývoj nového DMS
- [x] Testování
- [x] Akceptace (11/2026)
- [ ] Migrační matice a mapování metadat – *probíhá*
- [ ] Migrace dat SPV z původního DMS
- [ ] Migrace dat fondů ze SharePointu
- [ ] Ostrý provoz a odstavení původního DMS

**Výzva:** data se migrují ze dvou zdrojů (SPV z původního DMS, fondy ze SharePointu) a mapování metadat komplikuje nepořádek ve zdrojových datech. Migrace je tak zároveň příležitostí data vyčistit a sjednotit.

**Návaznost:** číselníky společností a subjektů se v DMS načítají z [MDM](#mdm). Subjekty tak vznikají na jednom místě a v MDM je může zakládat více uživatelů, čímž se snižuje závislost na IT týmu a rozkládá zátěž. Jan Kridlo tak získá prostor na jiné iniciativy.

#### Auditní workflow

<!-- K doplnění s Tomášem Málkem -->

- **Cíl:** ...
  <!-- Jaký proces workflow pokrývá? Co dnes backoffice dělá ručně? -->
- **Partner:** RSJ Custody (IS útvar, T. Málek)
- **Zahájení:** 11/2026
- **Fáze:** PoC
  <!-- Nápad / Analýza / PoC / Realizace / Pilot / Dokončení / Provoz -->
- **Přínos:** ...
  <!-- Úspora času? Dohledatelnost pro audit? Soulad s regulací? -->

**Průběh:**

- [ ] ...
- [ ] ...
  <!-- Jaké jsou hlavní kroky a co je už hotové? -->

**Návaznost:** ...
<!-- Napojení na MDM, DMS, Invoices, BOSS? Kdo jsou uživatelé? -->

#### Projects

- **Cíl:** přesunout workflow investičních rozhodnutí z on-premise SharePointu na novou platformu PaaS.
- **Partner:** SharePoint Solutions s. r. o.
- **Zahájení:** 09/2026
- **Fáze:** Analýza
- **Přínos:** moderní a udržitelné řešení v souladu s cloud first strategií. Po migraci DMS jde o další krok k odstavení on-premise SharePointu a lokálního AD.

**Průběh:**

- [ ] Analýza – *probíhá*
- [ ] Realizace
- [ ] Migrace dat
- [ ] Ostrý provoz a odstavení původního řešení

**Návaznost:** navazuje na [DMS](#dms). Po přesunu DMS, Projects a Invoices bude možné odstavit on-premise SharePoint a zrušit lokální AD.

#### Invoices

- **Cíl:** přesunout workflow schvalování faktur z on-premise SharePointu na novou platformu PaaS.
- **Partner:** SharePoint Solutions s. r. o.
- **Zahájení:** plánováno na 2027
- **Fáze:** Nápad
- **Přínos:** poslední krok migrace, po kterém bude možné odstavit on-premise SharePoint a zrušit lokální AD.

**Návaznost:** navazuje na [DMS](#dms) a [Projects](#projects). Nové řešení bude rovnou připravené pro napojení [AI vytěžování faktur](#ai-vytěžování-faktur).

### Reporting

#### Migrace DWH do Fabricu

- **Cíl:** převést stávající datový sklad a reporting na platformu Microsoft Fabric.
- **Partner:** probíhá výběrové řízení
- **Zahájení:** ...
- **Fáze:** Analýza
- **Očekávaný přínos:** moderní a škálovatelná datová platforma propojená s Power BI a M365, jednodušší správa dat a menší závislost na jednotlivcích. Konkrétní přínosy a náklady jsou předmětem výběrového řízení.

**Průběh:**

- [x] Oslovení partnerů
- [ ] Výběrové řízení: porovnání nabídek, nákladů a přínosů – *probíhá*
- [ ] Rozhodnutí o realizaci a výběr partnera
- [ ] Migrace DWH
- [ ] Převedení reportingu v Power BI

**Návaznost:** projekt navazuje na [DWH](#aplikace) a [Power BI](#aplikace). Zároveň je součástí cílového modelu týmu Data a reporting, včetně otázky přístupu partnera k datům a míry závislosti na něm (viz [Strategie](#strategie)).

## Budget

<!-- Bude doplněno následně, slide by měl sloužit pro přehled jaký byl plánovaný budget a jaký je aktuální stav k Q2, jelikož více dat nemám od účetních -->

## Strategie

### Cílový model IT týmu

> Cílem není navyšovat počet lidí, ale zajistit kompetence, kontinuitu a nezávislost na jednotlivcích.

#### Cílové rozdělení do 4 týmů

| Tým | Oblasti | Interně | Externě |
|---|---|---|---|
| Provoz | Podpora uživatelů, L1, HW, M365, endpoint, DMS a workflow | J. Kridlo, IT administrátor (M365, Intune, Exchange) | Orbit (L2/L3 expertíza) |
| Bezpečnost | Security, identita, Azure, síť, backup | Security & cloud administrátor (**nová role**) | Orbit, volitelně SOC/MDR služba |
| Rozvoj | AI automatizace, vývoj a integrace, MDM | F. Urban, D. Marko | J. Filip |
| Data a reporting | DWH, Power BI, migrace do Fabricu | M. Bartošová, datový specialista (**nová role**) | Fabric partner |

Governance a koordinaci projektů drží vedoucí IT jako partner businessu.

**Interní kapacita: 6 → 8 (+2 FTE)**, a to cíleně do oblastí, které dnes nikdo nevlastní nebo stojí na jednom člověku. Nová role security & cloud administrátora převezme cloudovou a bezpečnostní agendu po Frederikovi a dá bezpečnosti vlastníka. Datový specialista zajistí zastupitelnost v DWH a reportingu, kde dnes vše stojí na jednotlivcích. Náklad pozic poměřujeme s nákladem rizika: regulatorním a reputačním dopadem nezvládnutého incidentu nebo výpadkem nezastupitelného člověka.

#### Varianta k zvážení: rozvoj Jana Kridla

Místo náboru dalšího IT administrátora do Provozu je možné rozvinout stávajícího člověka. Jan Kridlo by si zvýšil kompetence a stal se IT administrátorem se zaměřením na cloud (M365 a Azure). L1 support by po něm převzal stážista.

| | Základní varianta | Varianta s rozvojem Jana |
|---|---|---|
| Provoz – cloud (M365, Intune, Exchange) | nový IT administrátor | J. Kridlo |
| Provoz – L1 support, HW | J. Kridlo | stážista |

**Přínosy:** nižší náklady, využití znalosti firmy, DMS a uživatelů, kterou Jan už má, a motivace a růst stávajícího člověka.

**Rizika:** rozvoj potřebuje čas a vyžaduje, aby Jan převzal větší odpovědnost, což je dnes jeho slabší stránka. Stážista má omezenou kapacitu i dostupnost, takže L1 bude potřebovat zástup.

### Strategie projektů

> Hlavním směrem je AI. Abychom ji mohli využívat naplno a bezpečně, zároveň ladíme stávající systémy, stavíme kvalitní datový základ a dokončujeme přechod do cloudu.

#### 1. Ladění stávajících systémů

V souladu s požadavkem nevymýšlíme zbytečně nové systémy, ale vylepšujeme a naplno využíváme to, co máme. Příkladem je [MS Sentinel](#ms-sentinel), [Alvao](#it-service-management-v-alvao) nebo napojování systémů na [MDM](#mdm). Nové projekty zakládáme jen tam, kde stávající řešení nevyhovuje (např. [DMS](#dms)).

#### 2. AI jako hlavní směr rozvoje

AI bude hrát v dalším období klíčovou roli. Zaměřujeme se na automatizaci opakované ruční práce v byznysu: zpracování dat pro PE/VC tým, kontrolu smluv nebo vytěžování faktur. Využíváme přitom i licence M365 E5/E7 včetně M365 Copilot, za které už platíme. Plánujeme nasazení RAG nad DMS a postupné propojování AI automatizací.

AI zavádíme řízeně: postupně přes PoC a pilot, s kontrolou výstupů člověkem a s posouzením IKT rizik ve spolupráci s 2. linií.

#### 3. Kvalitní data jako základ

AI a reporting potřebují spolehlivá data. Proto budujeme jeden zdroj pravdy pro kmenová data ([MDM](#mdm)) i pro zaměstnance ([HR modul BOSS](#propojení-hr-modulu-boss-s-ad)), řízení oprávnění podle rolí ([RBAC](#rbac)) a moderní datovou platformu ([Fabric](#migrace-dwh-do-fabricu)), zároveň musí vzniknout pozice Datového specialisty, která zajistí správnou kvalitu dat jako vstup pro AI.

#### 4. Cloud first: SaaS a PaaS

Postupně rušíme on-premise SharePoint, lokální Active Directory a virtuální servery v Azure. Cílem je provozovat vše jako SaaS a PaaS s identitami pouze v Entra ID. Méně vlastní infrastruktury znamená menší provozní zátěž týmu, vyšší bezpečnost a nižší riziko výpadků.

#### Výhled

| Období | Hlavní kroky |
|---|---|
| Do konce 2026 | dokončení Sentinelu a migrace DMS, ostrý provoz Založení fondu, vyhodnocení pilotů a PoC v AI, výběr partnera pro Fabric |
| 2027 | migrace Projects, migrace a nasazení Invoices, rozšíření AI automatizací do provozu, migrace DWH do Fabricu |
| 2028 | odstavení on-premise SharePointu a lokálního AD, rušení VM |
| Dlouhodobě | plně cloudové prostředí (SaaS/PaaS), AI jako běžná součást klíčových procesů, RBAC napříč všemi systémy |