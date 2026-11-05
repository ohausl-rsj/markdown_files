# CEO reporting IT, Data & AI Automation

## Hlavní body

- **Vývoj IT týmu** přes obnovu týmu, až po nové rozdělení [budeme ihned navazovat na nové rozdělení týmu, nebo až na konci]
- **Projekty** aktuální stav projektů od myšlenky až po produkci [projekty jsou rozdělené na Core IT, AI, development, reporting]
- **Budget** stav k Q2 a vyhodnocení vzhledem plánu, případně doplnění výhledu
- **Strategie** jaký je výhled jak ve složení IT týmu, tak v projektech. Jaký je ideální cílový stav, kam bychom chtěli směrovat v dalších obdobích.

> celá prezentace bude propojena i se stavem projektů, které má na starosti tým IS oddělení Tomáše Málka z RSJ Custody. Musí být vidět provázanost a to, že společně na projektech pracujeme a úspěšne posouváme dále.

# Profil společnosti

Jedná se o investiční skupinu, která čítá několik společností. Naše IT oddělení působí napříč dvěma společnostmi ze skupiny:

1. **RSJ Investments a. s.** - hlavní společnost, jelikož se jedná o regulovaný subjekt, který spadá pod ČNB (DORA)
2. **RSJ Services s. r. o.** - jedná se o servisní společnost, která působí jako dodavatel (třetí strana) pro RSJ Investments. IT oddělení je téměř celé aktuálně pouze na RSJ Services. Pouze já mám

Dále v rámci skupiny spolupracujeme s další společností a to je **RSJ Custody a. s.**. Tato společnost je také regulovaná a pod tuto společnost spadá vývojové oddělení informačních systémů. Programují pro nás různé aplikace (BOSS, WF založení fondu aj.). Vedoucím tohoto oddělení je **Tomáš Málek** a má pod sebou několik programátorů. Zároveň pod něj organizačně spatá i **Dušan Marko**, ale zároveň 100% jeho FTE je alokováno právě pro nás jako pro RSJ Investments, jelikož pro nás dělá činnosti viz. [EDušan Marko](#dusan-marko).

## Technologický stack

> Společnost je razí fylozofii **cloud first**. 

- Lokální/on-premise infrastruktura - kancelář Praha, pouze Unifi UDM SE, switche, AP, kamery, senzory
- Azure VM - IaaS, celkem 14 VM's
- Azure App Service, Azure SQL Server, DB, Blob storage, VNET, apod. - PaaS
- M365 - SaaS

## Aplikace

zde je výpis námi vyvýjených a provozovaných aplikací. Případně aplikací, které jsou vyvýjené a provozované RSJ Custody IS týmem.

| Aplikace | Popis | Provozní model | Umístění | Správce | Vývoj/dodavatel |
|---|---|---|---|---|---|
| BOSS | Informační systém, pro RSJ Investments slouží jako evidence kovenantů, úvěrových smluv apod. | SaaS | ... | RSJ Custody | RSJ Custody |
| MDM | Master data management - zdroj pravdy pro data | PaaS | Azure | RSJ Services | Dušan Marko |
| DMS | Document management system, archiv smluv a ostatní dokumentace pro fondy a SPV | IaaS | Azure | RSJ Services | Sharepoin Solutions s. r. o. |

# Vývoj IT týmu

> Nebudeme hodnotit to, co bylo v loňském roce, ale důležitá informace je, že jsem nastoupil 1. 9. 2025 a ihned po mém nástupu, odešli 2 technici ze 3. Byly to navíc ještě ti, na kterých to stálo. Oba zkušení. Zbyl pouze L1 technik Jan Kridlo. Tyto techniky se mi podařilo velice rychle nahradit, nastoupl Frederik a Jiří.

## Aktuální složení

Níže je uvedeno aktuální složení IT týmu a jejich základní

1. **Ondřej Hausl** (Vedoucí IT oddělení) - moje pozice, nastoupil jsem 1. 9. 2025 jako vedoucí celého oddělení. Práci mi částečně předal bývalý kontraktor, který nadále působí jako externí projektový manažer.
2. **Jan Kridlo** (IT administrátor) - L1 support a DMS + související systémy (WF investičních rozhodnutí, Invoice, MDM). Je zodpovědný, věci dotahuje do konce, ale chybí mu tah na branku a nedokáže převzít zodpovědnost.
3. **Frederik Urban** (IT administrátor) - nastoupil 2. 2. 2026 jako IT administrator se zkušenostmi s programováním. Postupně se profiloval a od října 2026 je plně alokován na vývoj AI automatizací. Z Core IT týmu tak plně odešel.
4. **Jiří Severa** (IT administrátor) - nastoupil 1. 1. 2026 jako IT administrator. Vize byla, že tento technik bude postupně nabírat zkušenosti a stane se lídrem celého týmu. Bohužel, zhruba po 3 měsících, jeho výkon začal rapidně klesat. I přes neustálou práci s ním, nedošlo ke zlepšení a proto jsem se rozhodl v říjnu 2026, že mu neprodloužím smlouvu. 31. 12. 2026 tak končí.Měl mít na starosti kompletní cloudovou a lokální infrastrukturu.

> cílem není tým nijak navyšovat, ale profesionalizovat.

## Externí partneři

1. **Dušan Marko** <a id="dusan-marko"></a>
- formálně zaměstnancem RSJ Custody, proto je zde veden jako externí partner, ale je 100% alokován pouze pro RSJ Investments.
- celkový úvazek je ale pouze 80%. Úvazek snížil na začátku roku 2026.
- jeho primární odpovědnost je za MDM, Cashflow, DWH.
- formálně tak reportuje Tomášovi Málkovi, ale oficiálně mě, jelikož mám na starost řízení projektů v rámci RSJ Investments.

> tato roztříštěnost u Dušana není optimální, jelikož není silná páka na jeho řízení. Obecně to ale funguje.

2. **IS útvar RSJ Custody s. r. o.**
- 

# Projekty

# Budget

# Strategie