# RSJ – core kontext holdingu (pohled IT)

**Verze:** 0.1 (první draft) | **Datum:** 2026-10-13 | **Vlastník dokumentu:** Ondřej Hausl, vedoucí útvaru IT

## 0. Jak s dokumentem pracovat

Tento dokument je společný základ pro většinu notebooků (IT operating model, ITSM, projekty). Popisuje, jak je skupina RSJ uspořádána, kdo je kdo a které systémy kdo provozuje.

Pravidla pro Copilota:

- Informace označené **(k ověření)** nejsou potvrzený fakt. Nepoužívej je jako jistotu a nevyvozuj z nich další závěry. Pokud na nich závisí odpověď, upozorni na to.
- Pokud něco v dokumentu chybí, doptej se. Nedomýšlej si to.
- Složení IT týmu a detailní seznam osob jsou v samostatném dokumentu **Lidé a role**. Tento dokument obsahuje jen klíčové osoby.
- Dokument popisuje stav k uvedenému datu. Aktuální stav projektů a incidentů v něm není.

## 1. Skupina RSJ v kostce

RSJ je finanční skupina v modelu Friends & Family, regulovaná od roku 2010. Veřejný web ji popisuje jako dvě části: **RSJ s.r.o.** (obchodování na burzách, RSJ Securities) a **RSJ Investments investiční společnost a.s.** (portfolio nemovitostí a private equity). Zdroj: veřejný web rsj.com. Vlastnická struktura *(k ověření)*.

Pro tento dokument je důležité, že IT útvar slouží primárně **RSJ Investments**, a to prostřednictvím **RSJ Services**. Ostatní společnosti skupiny mají vlastní IT.

## 2. Společnosti a jejich role

| Společnost | Role | Vztah k našemu IT |
|---|---|---|
| **RSJ Investments investiční společnost a.s.** | Investiční společnost, obhospodařuje fondy a portfolio. Regulovaný subjekt (ČNB, DORA). Sídlo: Na Florenci 2116/15, Praha 1. | **Hlavní zákazník IT.** |
| **RSJ Services s.r.o.** | Servisní společnost skupiny. Zaměstnává IT tým a poskytuje IT služby pro RSJ Investments. Poskytovatel IKT služeb dle DORA posouzení. | **Poskytovatel IT služeb.** Tým je 100 % na RSJ Services. |
| **RSJ Custody s.r.o.** | Licencovaný obchodník s cennými papíry (ČNB). Administrátor a depozitář fondů, účetnictví, personalistika, back office. Má vývojový tým. | Dodává část IT služeb (vývoj). Je záložní poskytovatel pro případ výpadku celé RSJ Services. |
| **RSJ Securities** | Market maker na světových burzách (obchoduje pod RSJ s.r.o.). ČNB a DORA. | Vlastní IT. Spolupráce na konzultantské úrovni. |
| **RSJ s.r.o.** | Holding obchodní části skupiny. Struktura *(k ověření)*. | Vlastní IT. Konzultantská úroveň. |
| **RSJ Asset Management** | Obhospodařuje fond RSJ Prop SICAV (algoritmické obchodování). | Vlastní IT. Konzultantská úroveň. |
| **RSJ Foundation** | Nadace skupiny. | Vlastní IT. Konzultantská úroveň. |
| **SPV** (společnosti ve vlastnictví fondů RSJ Investments) | Projektové společnosti, každá funguje jinak. | Role IT se liší podle SPV, viz 2.2. |

### 2.1 Vztahy mezi společnostmi

- RSJ Investments a RSJ Services jsou **sesterské společnosti**. Vlastnická vazba *(k ověření)*. Starší informace z webu zmiňují holding RSJ Invest s.r.o. nad oběma společnostmi *(k ověření)*.
- RSJ Services poskytuje IT služby RSJ Investments.
- RSJ Custody je záložní poskytovatel IT služeb pro případ výpadku celé RSJ Services. Dodává také vývoj aplikací (viz sekce 4).
- Fondy s právní osobností obhospodařované RSJ Investments: RSJ Investments SICAV, RSJ PE SICAV, RSJ Estate SICAV (+ podílové fondy). Fondy RSJ Asset Management jsou samostatně, např. RSJ Prop SICAV.

### 2.2 Role IT u SPV

- SPV **s vlastním IT**: IT RSJ Investments pouze dohlíží, radí a kontroluje.
- SPV **bez vlastního IT**: IT pomáhá i s realizací některých věcí.
- Zatím jen v malé míře. Přístup se liší podle konkrétního SPV.

### 2.3 Regulace

| Společnost | Stav |
|---|---|
| RSJ Investments | ČNB, DORA (potvrzeno) |
| RSJ Securities | ČNB, DORA (potvrzeno) |
| RSJ Custody | Licencovaný obchodník s cennými papíry pod ČNB (web). Použitelnost DORA *(k ověření)* |
| RSJ Services | Poskytovatel IKT služeb v rámci skupiny. Regulatorní status *(k ověření)* |

## 3. Klíčové osoby (mimo IT tým)

| Osoba | Role |
|---|---|
| Libor Winkler | CEO RSJ Investments, předseda představenstva |
| Jan Dostálek | Člen představenstva RSJ Investments, vedoucí Risk managementu |
| Marek Capák | CFO |
| Jan Kubíček | IKT risk manažer |
| Petra Silhova | Compliance |
| Tomáš Málek | Vedoucí vývoje v RSJ Custody |
| Karel Horyna | Vedoucí IT v RSJ Securities |

Další osoby (vlastníci aplikací, asset manažeři, kontakty u dodavatelů) jsou v dokumentu **Lidé a role**.

## 4. Systémy a aplikace

| Systém | Účel | Vývoj / provoz | Pro koho |
|---|---|---|---|
| **BOSS** | Firemní systém s více moduly (např. HR BOSS). HR modul je zdrojem údajů o zaměstnancích, synchronizace BOSS → AD → Entra ID. | Vývoj RSJ Custody | Celá skupina. Z pohledu IT RSJ Investments. RSJ Services ho nepoužívá. |
| **Formic** | Aplikace klíčová pro identifikaci klienta. | Správa RSJ Custody | RSJ Investments |
| **Workflow zakládání fondů** | Schvalování a řízení kroků při založení nového fondu. Běží v rámci BOSS. | Vývoj RSJ Custody | k doplnění |
| **Helios (fondy)** | Účetnictví fondů. Umístění: Plzeň. | Provozuje IT RSJ Securities (tým Karla Horyny, jeden IT pracovník v Plzni). Formální vlastnictví Custody *(k ověření)* | Fondy |
| **Helios (SPV)** | Účetnictví SPV. SaaS od firmy Nesoss *(pravopis k ověření)*. | Zajišťuje RSJ Services. Řídí ho vedoucí účetního oddělení, IT dostává občasné požadavky. | SPV |
| **DMS** | k doplnění | Sharepoint Solutions s.r.o. | k doplnění |
| **Projects** | Investiční rozhodnutí | Sharepoint Solutions s.r.o. | k doplnění |
| **Invoices** | Schvalování faktur | Sharepoint Solutions s.r.o. | k doplnění |
| **MDM** (někdy označováno MDH) | Master data management | Interní vývoj napůl s RSJ Custody. Nově se zapojuje interní developer. | k doplnění |
| **Alvao** | Service desk (ITSM) | SaaS | k doplnění |
| **M365 a Azure** | Platforma, ve které běží aplikace a kolaborace. | IT útvar | viz sekce 5 |

## 5. Tenanty a propojení

| Tenant | Společnosti |
|---|---|
| **rsjinvest.com** | RSJ Investments, RSJ Services |
| **rsj.com** | RSJ Custody, RSJ Securities. RSJ Asset Management a další *(k ověření)* |

- Hosté B2B jsou nastaveni tak, aby se chovali jako členové.
- Cross-tenant access nastavujeme společně s druhou stranou. Stav: **rozpracováno**, nastavení se ještě dolaďuje.

## 6. Lokality

- **Praha, Florentinum (Na Florenci 2116/15):** většina skupiny včetně IT útvaru.
- **Plzeň:** depozitář, back office a účetnictví pro fondy. Sídlí tam také jeden IT pracovník z týmu RSJ Securities, který spravuje Helios (fondy).

## 7. Externí dodavatelé

| Dodavatel | Co dodává |
|---|---|
| **Sharepoint Solutions s.r.o.** | DMS, Projects, Invoices |
| **Nesoss** *(pravopis k ověření)* | Helios pro SPV (SaaS) |
| **Alvao** | Service desk (SaaS) |
| **ORBIT s.r.o.** | Externí konzultanti, dodavatel licencí Microsoft |
| **NWS** | Hardware |
| **Active24** | Doména |

*Seznam není úplný, bude doplňován.*

## 8. Otevřené body k ověření

1. Vlastnická vazba RSJ Investments a RSJ Services (případně RSJ Invest s.r.o.).
2. Struktura RSJ s.r.o. a vlastnictví Custody a Securities.
3. Tenant RSJ Asset Management a dalších společností.
4. Použitelnost DORA u RSJ Custody a RSJ Services (dotaz na compliance).
5. Vlastnictví Helios (fondy).
6. Pravopis Nesoss.
7. Stav cross-tenant nastavení.
8. Doplnit účel a uživatele u DMS, MDM, Alvao a Workflow zakládání fondů.
