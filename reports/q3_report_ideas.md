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
2. **RSJ Services s. r. o.** - jedná se o servisní společnost, která působí jako dodavatel (třetí strana) pro RSJ Investments. IT oddělení je téměř celé aktuálně pouze na RSJ Services. Pouze já mám

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



## Budget

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
