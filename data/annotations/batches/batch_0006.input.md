# Annotation batch input

Run index (for self-consistency): 1

## System prompt

---
name: system_classifier
version: 1
date: 2026-05-28
intended_model: Claude (in-the-loop) / GPT-4o / equivalent
---

# System prompt — 3-class Lithuanian propaganda classifier

You are an annotator assigning each Lithuanian news article to **exactly one** of:

- `non`    — not propaganda
- `open`   — overt propaganda (visible System-1 manipulation: loaded vocabulary,
             slogans, name-calling, shouting headlines, explicit emotional appeals)
- `hidden` — covert propaganda (the article reads neutral on a first pass, but
             framing, selective quotation, "just asking questions" doubt,
             selective sourcing, or implicit narrative do the persuading)

Use the rubric in `config/rubric.md` verbatim. **Read the full article** before
deciding. If you cannot decide with confidence ≥ 0.6, set `confidence` below 0.6
and the article will be routed to the human-review queue — do not force a label.

For each article, emit one JSON object on its own line into the matching
`batch_NNNN.output.jsonl`:

```json
{
  "id": "<exact id from the input>",
  "label": "non" | "open" | "hidden",
  "confidence": <float in [0,1]>,
  "rationale": "<2–3 sentences pointing at specific evidence in the article>",
  "features": {
    "loaded_lexicon": <bool>,
    "us_vs_them": <bool>,
    "selective_framing": <bool>,
    "named_authorities": <bool>,
    "doubt_questions": <bool>,
    "sensational_headline": <bool>
  }
}
```

Rules:

- Output **one JSON object per article**, in the same order as the input.
- Lithuanian text in the rationale is fine (preferred for nuance).
- Do not output anything outside the JSONL — no prose, no markdown fences, no
  trailing comma.
- If self-consistency mode is active, run the classification three times
  independently and the harness will majority-vote across the three batches.


## Few-shot exemplars

---
name: fewshot_examples
version: 1
date: 2026-05-28
---

# Few-shot exemplars

Use these worked Lithuanian examples to anchor borderline judgments. Copy the
*style* of the rationale: short, evidence-anchored, pointing to specific spans.

### Example A — label: `non`
> *"Vilniaus savivaldybė pirmadienį paskelbė, kad nuo birželio pradžios viešasis
> transportas dirbs pagal vasaros tvarkaraštį."*
- `label`: `non`
- `confidence`: 0.95
- `rationale`: "Faktinis informacinis pranešimas su aiškiu šaltiniu (savivaldybė) ir be emocinio krūvio."

### Example B — label: `open`
> *"Nuolat meluojantis Vakarų marionetės režimas vėl bandė apgauti tautą — bet tauta žino tiesą!"*
- `label`: `open`
- `confidence`: 0.92
- `rationale`: "Atvira retorika su epitetais ('marionetės režimas'), 'mes prieš juos' rėminimu ir šaukimu (!) — System-1 manipuliacija paviršiuje."

### Example C — label: `hidden`
> *"Tarptautinės politikos ekspertas dr. X aiškina, kad sankcijos labiau kenkia
> patiems vakariečiams. Tuo tarpu oficialūs Kijevo pareiškimai prieštarauja
> tikrovei lauke."*
- `label`: `hidden`
- `confidence`: 0.78
- `rationale`: "Tonas neutralus, bet šaltinių pasirinkimas ir rėminimas ('oficialūs Kijevo pareiškimai prieštarauja tikrovei') sistemingai stumia vieną poziciją; jokio balanso."

### Example D — label: `hidden`
> *"Vis daugiau europiečių abejoja paramos Ukrainai prasme. Kiek dar metų mes mokėsime už karą, kuris nesibaigia?"*
- `label`: `hidden`
- `confidence`: 0.7
- `rationale`: "'Tik užduoda klausimus' rėminimas su retoriniu klausimu; jokio aiškaus įžeidimo, bet kiekvienas sakinys stumia į vieną pusę."


## Articles to label

Output one JSON object per article into the matching `.output.jsonl` file,
in the same order as below. Do NOT output anything else.

### Article 1 — id: `scraped:rubaltic_lt:3d4d7a3404801ecb`

**Title:** „Energetinė nepriklausomybė“ praėjus 30 metų: Lietuva pasiryžo galutinai išeiti TSRS

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Po 30 metų „nepriklausomybės“ Lietuva pagaliau visgi pasiryžo truputi išeiti iš TSRS. Nenustebkite, elektros energetikos atžvilgiu Lietuva (kartu su Latvija, Estija ir Baltarusija) kaip buvo prieš 30 metų TSRS sudėtyje, taip ten ir randa si.

Dabar prieš keletą dienų Nepriklausoma Lietuva paskelbė, jog „sumažina elektros tinklų pralaidumą per sieną su Baltarusija“. Kodėl, staiga, taip? Ir svarbiausiai: kame šaknys?

Pasakoju: iki šio laiko buvusios TSRS teritorijoje veikia BRELL energetinis žiedas.

Tai iš pirmųjų Baltarusijos, Rusijos, Estijos, Latvijos ir Lietuvos pavadinimo raidžių sudaryta abreviatūra. Energetinis žiedas buvo sudarytas dar 1950-60-aisiais metais TSRS, kurios sudėtyje pilnateisiais nariais buvo visos išvardintos „laisvosios respublikos“.

Tiems, kurie ne viską supranta apie elektros energetiką, išaiškinu. Bendros energetinės sistemos idėją dar 1920 metais iškėlė didysis inžinierius – revoliucionierius, Lenino bendražygis Glebas Kržižanovskis Maksimilianovičius. Ši idėja buvo realizuota įžymiame GOELRO (rusiška "Valstybinės Rusijos elektrifikacijos komisijos" abreviatūra) plane.

Prasmė: ir metų laike ir paros laike elektra vartojama labai netolygiai (ir tada ir dabar). Įvairiose vietose krūvis tai didėja, tai krenta. Greitai keisti gaminamos elektros kiekį elektrinės negali, jos inertinės.

Bet jei visas esančias elektrines sujungti į bendrą tinklą, per visą kontinentą nutiesti elektros perdavimo linijas iš šiaurės į pietus ir iš vakarų į rytus – tada šios elektrinės gali vieną kitą palaikyti bei papildyti.

Pavyzdžiui, Urale žmonės keliasi į darbą 4 valandą ryto Maskvos laiku, įjungia šviesą, šildo vandenį, ir ten krūvis išauga keliais kartais – tada jiems elektros tiekimą laidais padidina dar miegančios Lietuvos, Latvijos ir Estijos TSR.

Taigi, buvusios TSRS energetika, pradedant nuo 1920-ųjų metų, buvo kuriama remiantis tokiais principais.

Pastebėsiu: netgi šiuolaikinėje JAV nėra bendros energetinės sistemos. Neseniai buvę Teksase ir Kalifornijoje „blekautai“ yra susiję, būtent su tuo, jog paramą elektros energija iš kaimyninių valstijų ten organizuoti nėra įmanoma. Jų energetikos sistema – ne „susisiekiantieji indai“.

Savo laiku pas juos nebuvo genialaus inžinieriaus – revoliucionieriaus Glebo Kržižanovskio.

1950-1960-aisiais metais TSRS baigė statyti tą patį BRELL žiedą, kuris sujungė į bendrą sistemą visą europinę TSRS teritorijos dalį. Pabaltijyje energetikos reikalus TSRS iš viso tvarkė labai rimtai.

Jos visos buvo sujungtos į vieną sinchroniškai veikiantį tinklą. Ir dar prijungtos prie Baltarusijos ir pačios didžiosios Rusijos.

Visa tai veikė puikiai ir efektingai. Pavasarį, kai Dauguvoje būdavo daug vandens, jos elektrinių turbinos sukosi visu pajėgumu, lietuviška AE dvejoms-trejoms savaitėms sustodavo branduolinio kuro perkrovimui. Regione ir be jos elektros buvo pakankamai. Jei būdavo jos stygius – žvalius rusiškus elektronus atsiųsdavo Leningrado ir Smolensko AE. Trumpai tariant, viskas veikė sklandžiai ir suderintai.

Iš dabar, draugai, pagalvokite, ant kiek kieta buvo, iškelta dar 1920 metais, GOELRO plano idėja

Iki šiol jų elektrinių turbinos sukasi ne tik vienu dažniu (50 Hercų į sekundę), bet sinchronizuotos pagal fazę. Kas yra „fazė“ – tai kada šimtai paminėtų Bendrojo energetikos žiedo šalių turbinų sukasi sinchroniškai, nei vienu laipsniu ne atsilikdamos ir ne aplenkdamos viena kitą. Tokia sistema daug ko verta...

Pabaltijo „ežiukai“ iki šio laiko vis raudoja, bet jau 30 metų kaip kremta „tarybinį kaktusą“. Išeiti iš energetinės priklausomybės subyrėjusio TSRS jie ir dabar nėra pasiruošę.

Rusijos dispečeriai kalbėti jų vietinėmis kalbomis nenori, bet jiems to ir nereikia. Pas Rusija savos energijos – kiek tik nori.

O Lietuvoje liūdna. Ignalinos AE jie, reikalaujant Europos sąjungai, 2009 metais

gėdingai uždarė.

Bet ir Estijoje ne viskas tvarkoj. Europa su savomis gretomis-tumbergomis reikalauja, kad estai uždarytų savo ne košerinės, skalūnais kūrenamas elektrinės.

O štai pilnateisis BRELL dalyvis „batka“ Lukašenka, padedant „Rosatomui“, šiais metais paleido tą patį, nuo ko Lietuva savanoriškai atsisakė prie 12 metų – savo galingą atominę elektrinę. Ir akivaizdžiai, kaip pasityčiojimą, ją įjungė į bendrąjį BRELL žiedą.

Pas lietuvius – mentalinis skausmas.

Uždarytoji Lietuvos AE stovėjo palei siena su Baltarusija, o naują Baltarusijos AE įžūliai stovi prie sienos su Lietuva. Tarp kitko, tokio pat galingumo.

Šachmatuose tai vadinama „rokiruotė“. Lietuviai 10 metų baisiai kovojo su baltarusiška AE, visuose eurokomisijose klykė – neleiskite baltarusiams statyti savo AE! Nieko nesigavo, Baltarusijos AE pradėjo veikti.

Elektros energiją lietuviai brangiai perka pas kaimynus. Dabar pagrindinė lietuviška svajonė: kad tik ne pas baltarusius!

Bet reikalas tame, jog tada jiems teks pastatyti „elektronų muitinę“, kad griežtai sekti: kokie elektronai kerta jų sieną BRELL žiedu.

Laisvi elektronai iš latviškų hidroelektrinių, laisvi elektronai iš estiškų, skalūnais kūrenamų elektrinių ar totalitariniai elektronai - iš Baltarusijos AE?

Tai sudėtingas uždavinys. Dar nei vienas Nobelio premijos už pasiekimus fizikoje laureatas nesurado būdo, kaip atskirti „laisvės elektronus“ nuo „totalitarizmo elektronų“. Netgi, dabar Lietuvoje gyvenanti, lietuvių priglobta „Laisvos Baltarusijos prezidentė, nominuota Nobelio Taikos Premijai –Svetlana Tichonovskaja, nesugebės atskirti vieną elektroną nuo kito.

Tokiam atvejui paskutiniu metu lietuviai apribojo totalitarinių elektronų skaičių iš Baltarusijos į Lietuvą, sumažindami „pertekėjimo“ galingumą tarp bendrų energijos tinklų... Bet elektronai – jie tokie. Teka laidais – BRELL žiedu kur tik nori.

Sutinkamai su „potencialų skirtumu“. Kur žemesnis potencialas – ten elektronai ir teka. Tai fizika.

O Lietuvos potencialas dabar (kaip politinis, taip ir energetinis, taip ir bendrai) – žemiau neįmanoma.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 2 — id: `scraped:rubaltic_lt:77b2bbd8cc6ca512`

**Title:** Dujų kainos žudo Lietuvos cheminę pramonę

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos azotinių trąšų gamykla Achema priversta sumažinti gamybą dėl aukštų dujų kainų. Su analogiškomis problemomis susiduria ir Odesos prieuosčio chemijos gamykla, kuri uždaroma neapibrėžtam laikui. Energetikos krizė skaudžiai smūgiuoja ir kitas kompanijas, bet tai ne priežastis kaltinti Lietuvos ir Ukrainos vadovybę nekompetentingumu. Nors iš kitos pusės, jos sąmoningai atsisakė daryti tai, ką daro Baltarusija – kovoti už maksimaliai naudingas energijos resursų importo sąlygas.

„Achema atidžiai svarsto tolimesnės veiklos galimybes ir koreguoja savo produktų gamybinę pintinę. Dėl šiuo metu susiklosčiusių nepaprastų sąlygų rinkoje, buvo nuspręsta, baigus planinį remontą, laikinai nepaleisti vieną iš amoniako cechų“, - sakė Achemos generalinis direktorius Ramūnas Miliauskas.

Nepaprastomis sąlygomis jis supranta rekordiškai aukštas dujų kainas Europoje. Paskutiniu metu, vartojimo sumažėjimo imliose energijos šakose požymių fone, jos visgi „atslūgo“.

Amerikiečių CF Industries Holdings Inc uždaro dvejas savo gamyklas Didžiojoje Britanijoje. Po to apie gamybos optimizavimą pareiškė ir norvegų kompanija Yara. „Rekordinės gamtinių dujų kainos Europoje įtakoja amoniako trąšų gamybos rentabilumą. Dėl ko Yara nutraukia gamybą kai kuriuose savo gamyklose. Atsižvelgiant į optimizavimą, kompanija beveik 40 procentų sumažins amoniako produkcijos gamybą Europoje“,- sakoma kompanijos pranešime.

Ukrainos energetikos eksperto Dmitrijaus Maruničio žodžiais tariant, ši įmonė jau seniai priprato stabdyti gamybą, kai dujų kainos tampa didelės. Kaip matosi, dabar Odesos prieuosčio chemijos gamyklai prasideda eilinis prastovos periodas.

Ukrainos leidinys „Strana“ cituoja gamyklos darbininkus: „Staigiai išaugo dujų kaina. Ir firma-tiekėjas -Agro Gaz Trading dabar atsisako tiekti dujas į gamyklą. Jai, paprasčiausiai, nenaudinga, kaina pašoko virš tūkstančio dolerių, su firmos antkainiu. Atitinkamai išauga ir produkcijos kaina. Suprantama, ji tapo nekonkurencinga, niekas nenori pirkti. Visos saugyklos užgrūstos karbamidu. Šiandieną sustabdė karbamidą, o rytoj sustabdys amoniako gamybą. Tolimesnės perspektyvos neaiškios“.

Suprantama, būtu nekorektiška šią problemą suvesti išimtinai į Lietuvos ir Ukrainos valdžios trumparegiškumą: dabartiniu metu visi azotinių trąšų gamintojai jaučia sunkumus (panašiai, kaip praeitų metų pavasarį iškilo problemos visiems naftos tiekėjams).

Bet reikalas tame, jog, Lietuvoje ir Ukrainoje „įregistruotos“ kompanijos galėjo išvengti tų problemų.

Kaip tada jaustųsi Lietuvos ir Ukrainos „žydrojo kuro“ vartotojai?

Veikia „Gazpromo“ ir „Gazprom transgaz Belorus“ pasirašyti dujų tiekimo į Baltarusiją ir jų transportavimo vakarų kryptimi kontraktai . Baltarusijai vienas tūkstantis kubinių metrų dujų apsieina 128,5 dolerių. Tai beveik tas pats, kaip ir praeitais metais (127 doleriai).

Praeitais metais Minskas skundėsi, jog vokiečiai dujas perka naudingesnėmis kainomis, negu kontrakto kainos baltarusiams. „Vakar mane painformavo, jog Europoje, šiais nepaprastais laikais, Rusija gamtines dujas parduoda iki 70 dolerių: už 65-68 dolerius, be nekaip už 127 dolerius, kaip Baltarusijai,- skundėsi prezidentas Lukašenka.- Kokia šia situacija ir padėtis, ko mes galime tikėtis ateityje? Norėtųsi žinoti, kas šiuo metu padaryta dėl gamtinių dujų kainos sumažinimo Baltarusijai“.

Tuo metu Ukraina tęsia rusiškų dujų, apsimesdami jog jos „europietiškos“, pirkimą. Buitiniai vartotojai stovi ant eilinio komunalinių tarifų pakėlimo, kurie šiais metais žada būti ypatingai skausmingi, slenksčio.

Prezidentas Vladimiras Zelenskis turėjo realią galimybę užbaigti absurdišką Petro Porošenkos energetinę politiką. Pirmais jo prezidentavimo metais vyko derybos dėl naujo tranzito kontrakto sudarymo tarp „Gazpromo“ ir Naftogazo“.

Maskvoje atvirai pasakė, jog nori su Kijevu sudaryti paketinį susitarimą, kuris apimtu susitarimus dėl tiesioginio dujų tiekimo. Toks žingsnis atrodė abipusiai naudingu ir logišku.

Apie tai, jog Ukraina pakišo save dėl ilgalaikio rusiškų dujų tiekimo kontrakto nebuvimo, Aukščiausioje Radoje pareiškė frakcijos „Batkivščina“ deputatas Aleksej Kučerenko. Tokios pat nuomonės prisilaiko „Opozicinės platformos – už gyvenimą“ lyderis Jurij Boiko. Jo žodžiais tariant, dar ne vėlu atnaujinti tiesioginį tiekimą iš Rusijos.

Pridėsime dar vieną svarbų faktą: Ukrainos energetinės sistemos kompanija-operatorius pasakoja apie kritinę situaciją su anglies kaupimu šiluminėse elektrinėse (ŠE).

Viena iš tų kaimyninių šalių – Baltarusija – oficialaus Kijevo paskelbta faktiškai nedraugiška, o kita šalis - Rusija – Aukščiausios Rados lygyje pripažinta „agresoriumi“. Ar panorės jos eilinį kartą gelbėti bukagalvį klouną ir jo, ne mažiau bukagalvę, Ukrainos Vyriausybę?

Lietuva nuėjo savo keliu. 2014 metais ji pas norvegus išsinuomojo suskystintų gamtinių dujų terminalą, kad nugalėti „energetikos priklausomybę“ nuo RF. Ir iš tikrųjų, dujų importo šaltinių diversifikacijos uždavinys buvo išspręstas: atsirado galimybė Lietuvai pirkti SGD vietoje vamzdynų dujų. Pastarųjų kaina, kaip taisyklė, žymiai žemesnė (išnešim už skliaustelių praeitų metų energetiko rinkos griuvimą, kuris buvo iššauktas koronavirusiniais apribojimais).

Be to, terminalas tiesiogine šio žodžio prasme, iš Lietuvos pumpuoja pinigus: 60 milijonų euro kasmet reikia mokėti už jo nuomą, dar 70-80 milijonų – už išlaikymą, tame tarpe kompensuoti valstybės kompanijos Ignitis nuostolius, kuri sudarė komerciškai nesėkmingą kontraktą su norvegišku dujų tiekėju Equinor.

Likimo ironija, patį didžiausias SGD terminalo eksploatacijos efektą Lietuvoje pajuto ta pati Achema. Ji ne tik perka dujas Klaipėdoje pagal ilgalaikius kontraktus, bet ir moka patį didžiausią mokestį. Mokestį, kuris sulyginimas su įmonės darbo užmokesčio fondu.

Pačią nuostolių, kuriuos generuoja SGD terminalas, atlygimo tvarką Achema jau keletą metų ginčija teisme. Paskutiniu metu jos ieškinys buvo dalinai tenkintas – pas kompanija atsirado viltis, jog veikianti schema bus peržiūrėta.

"Šis Europos sąjungos Bendrojo teismo nutarimas rodo, jog valstybė ir Europos komisija ne visada vadovaujasi ES įstatymų reikalavimais koordinuojant valstybės paramos schemą, dėl ko nukentėjusiems asmenims tenka ilgai bylinėtis, kad įrodyti tiesą ir padarytus nusikaltimus“,- sakoma Achemos pranešime.

Vietoj to, kad kovoti už maksimaliai naudingas dujų importo sąlygas tėvyninėms įmonėms, Pabaltijo respublikų valdžia jiems užkrauna SGD terminalų aptarnavimo naštą . Ar sugebės tokios kompanijos konkuruoti, pavyzdžiui, su vokiečiais, kurie teikia pirmenybę bendradarbiavimui su „Gazpromu“?

Rusijos ir Baltarusijos santykiai energetikos sferoje niekada nebuvo (ir, tikriausiai, nebus) paprastais. Kaip ir Rusijos-Ukrainos santykiai Janukovičiaus laikais. Bet Azarovo vyriausybei ir į galvą neatėjo mintis organizuoti virtualinio reverso schemą arba užpirkti SGD per užsienio terminalus.

Todėl pas vienus gamyklos veikia, o pas kitus jos užsidaro.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 3 — id: `scraped:rubaltic_lt:8810cd6255a1927c`

**Title:** Šildymo kaina-ne juokai: Latvija su elektros energija iš Rusijos  „sulaužė ištikimybę“ Lietuvai

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Latvija ruošiasi atšaukti elektros energijos importo iš Rusijos apribojimus. Apie tai pareiškė Lietuvos Valstybinės energetikos reguliavimo tarnybos pirmininkas Renatas Pocius. Jo žodžiais tariant, toks bus Rygos atsakas į neseniai priimtą Vilniaus sprendimą vienašališkai sumažinti elektros tinklų pralaidumą iš Baltarusijos į Lietuvą. Energetinio kolapso grėsmė ateinančią žiemą verčia Latviją ir Estiją dar stipriau priešintis Baltarusijos AE boikotui, kurį joms bruka Lietuvos valdžia.

RuBaltic.Ru analitikos portalas jau rašė, jog Pabaltijo respublikos nesugebėjo suderinti regioninę elektros energijos prekybos su trečiosiomis šalimis metodiką. Lietuva nusprendė veikti savo firminiame stiliuje - vienašališkai maždaug tris kartus sumažinti elektros tinklų pralaidumą iš Baltarusijos į Lietuvą.

Lietuvos Valstybinės energetikos reguliavimo tarnybos pirmininkas Renatas Pocius pabrėžia, jog toks sprendimas yra nukreiptas prieš kaimyninę šalį: „Latvija jau neskirstys tuos pačius mūsų pajėgumus, kurie šiandien yra, ant savo jungties, tokiu būdu padidindami komercinę prekybą“.

Suprantama, jog Rygą tokia įvykių eiga netenkina. Šios medžiagos ruošimo momentu jokios reakcijos į Lietuvos įžūlumą iš oficialių Latvijos isteblišmento atstovų nebuvo. Bet tas pats Pocius perspėja, jog „atsakas“ artimiausiu laiku, tikriausiai, atskris.

Latvijos ir Estijos operatoriai numato korekcijas jų dvišalėje metodikoje – planuojama naikinti 0,62 koeficientą, ribojantį importą iš Rusijos į Latviją.

Kad suprasti apie ką kalbama, reikia sugrįžti prie dvejų metų senumo įvykių. Tada Latvijos vadovybė nusprendė prekybą elektros energija su trečiomis šalimis perkelti prie nacionalinės sienos su Rusija (anksčiau visi srautai tekėjo per Lietuvą). Krišjans Karinš apie tai kalbėjo, kaip apie bandymą apsaugoti šalį nuo galimo elektros energijos deficito Baltarusijos AE blokados atveju. Iškrentančias energijos apimtis galima bus pakeisti tiekimu iš Rusijos, su kuria, skirtingai nuo Baltarusijos, Latvija yra sujungta elektros perdavimo linijomis.

Tikrinti šių dokumentų tikrumą Latvija negali (ir vargu, ar nori). Jai belieka pasikliauti savo rusiškų partnerių garbės žodžiu.

Po praėjusių metų įvykių Baltarusijoje Karinš taip ir nepakeitė savo sprendimo dėl prekybos taško elektra perkėlimo prie nacionalinės sienos. Jis apsiribojo tik politiniais pareiškimais, kurie neturi nieko bendro su energetika.

Kai Pabaltijo respublikų lyderiai vieningu frontu išstojo prieš Baltarusijos AE, Lietuvos, Latvijos ir Estijos specialistai tęsė nepaprastas derybas dėl prekybos elektros energija bendros metodikos.

Kuo daugiau elektros bus tiekiama iš Rusijos į Latviją, tuo didesnė tikimybė, jog ji buvo pagaminta toje pačioje Baltarusijos AE.

Remiantis BNS šaltiniu duomenimis, labiausiai nepatenkinta Lietuvos elgesiu yra Estija. Jie mano, jog konservatoriai-„landsbergistai“ regione kuria dujų deficitą.

Švelniai sakant, tam parinktas ne pats geriausias laikas.

Tai sukelia elektros energijos brangimą kaip pramoniniams, taip ir buitiniams galutiniams vartotojams.

„Latvija jau dabar negamina pakankamai energijos savo vartojimui šiandieniniame lygyje. Dabar prasidės elektros mašinų revoliucija. Iš kur imsime įtampą? Latvijoje nėra jokio gamybos didėjimo plano, skurdindamos gyventojus, auga elektros energijos kainos, o gamyba tampa nekonkurencinga“,- rašo Janis Ošleis ..

Su tokiomis pat problemomis susiduria Estija ir Latvija (ypatingai pastaroji – ji yra pati energodeficitinė Pabaltijo respublika).

„Vertinant situaciją rinkoje atsižvelgiant į turimus rinkos rugpjūčio mėnesio duomenis, palyginant su liepa, mes stebime, jog kainų pokyčių 2022 metais prognozės tapo atsargesnėmis. Dabartiniu metu, finansų rinkos instrumentų 2022 metų 1 ketvirčiui laukimas nurodo į tai, jog kainos liks einamajame lygyje. Pagrinde tai susiję su vandens stygiumi stambiuose Skandinavijos HES vandens saugyklose, o taip pat ir su padidėjusia elektros energijos paklausa šildymo sezono metu“, - tvirtina Latvijos visuomeninių paslaugų reguliavimo komisija.

Visa Europa nutilo pirmųjų rudens šalčių išvakarėse. Kiekviena šalis turi būti suinteresuota tame, kad turėti patikimus elektros energijos tiekėjus.

Pagal kvailumo laipsnį šis sprendimas gali rungtyniauti su Lietuvos ketinimu po trijų mėnesių atsisakyti baltarusiškų trąšų tranzito.

Tarp kitko, krovinių tranzitas – grynai nacionalinis klausimas. Jei Klaipėdos uostas neteks „Belaruskalij“ produkcijos, tai Rygoje, Ventspilyje bei Liepojoje savo galvų pelenais nebarstys. Bet štai, nauja lietuviška prekybos elektros energija metodika gali sukelti problemas kitiems regioninės rinkos dalyviams. Tai tas retas atvejis, kai Latvijos valdžia adekvačiai įvertina situaciją ir bando sušvelninti galimą ekonominį smūgį.

Galima tik stebėtis „dėdulės“ Landsbergio ir jo parankinių mokėjimu sukurti problemas lygioje vietoje. Migracijos krizė, „antivakcerių“ protestai, artima baltarusiško tranzito pabaiga, vaidai su Kinija...

Kad visą tai išsrėbti, Lietuvai, galimai, prisieis skubiai atnaujinti taip nekenčiamos baltarusiškos elektros energijos ankstesnės apimties importą. Bet tai bus žiemą – tokie planavimo toliai Lietuvos konservatoriams nėra žinomi.

Bet kokiu atveju „Baltijos vienybė“ vėl skyla.

Visus metus Ryga, Vilnius ir Talinas nesugebėjo rasti kompromisinę prekybos elektros energija su trečiomis šalimis metodiką. Pas Lietuva ji sava, pas Latviją ir Estiją – sava.

Bet daug kas priklausys nuo „generolo Šalčio“.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 4 — id: `scraped:rubaltic_lt:4676e82957c3392f`

**Title:** Migrantai provokuoja politinį sprogimą Pabaltijyje

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Baltarusijos pasienyje prasidėjo nauja migracijos krizės paaštrėjimo fazė, apie kurią Baltijos valstybių valdžia dar visai neseniai kalbėjo, kaip apie jau praėjusį etapą. Lietuvos ir Latvijos koncentraciniuose lageriuose migrantai maištauja, korupciniai skandalai kylantys dėl pasienio ruožo sutvarkymo, pabėgėliai iš Afganistano puola po ratais ir bando nusižudyti. Dėl migrantų susidariusi nervinga situacija provokuoja politinę destabilizaciją Pabaltijyje: Latvijos ir Lietuvos gyventojai kelintą jau kartą įsitikiną, jog jų Vyriausybės nėra veiksnios ir be valdymo iš išorės nesugeba atsakyti laiko iššūkiams.

Latvijoje, rugsėjo mėnesio 7 dieną migrantai iš „Mucenieku“ lagerio organizavo protesto akciją ir prigrasino badavimu. Nelegalūs pabėgėliai išmetė jiems atvežtas dėžes su maistu bei bandė sulaužyti lagerio vartus ir šaukė, jog jie nenori pasilikti Pabaltijyje: jie laisvi žmonės,tegul juos tuoj pat išleidžia ir sudaro galimybę vykti į Vokietiją pas svetingą Angelą Merkel.

Lietuvoje migrantai pradėjo maištauti prieš parą. Rudininkų lagerio gyventojai šūkavo, jog jie ne gyvuliai ir reikalavo paleisti juos į laisvę.

„Mes reikalaujame laisvės, mes ne nusikaltėliai, o mus uždarė tokioje vietoje, kuri netinka žmonių gyvenimui, mes nežinome, kas mūsų laukia“, - kalbėjo vienas iš pabėgėlių.

Pabėgėlių stovyklą Rudininkuose jau seniai yra liūdnai pagarsėjusi, ir joje maištaujama nebe pirmą kartą. Tačiau pastarąją savaitę Lietuvos valdovai įtikinėja žmones, jog tie maištai nueina praeitin.

Lietuva, esą, atrėmė Lukašenkos „hibridinę agresiją“, ir dabar iš „migracijos fronto“ mus pasiekia tik džiaugsmingos ir pozityvinės naujienos. Per parą į Lietuvą neprasiskverbė nei vienas nelegalus pabėgėlis. Keletas šimtų migrantų jau išskrido į gimtąjį Iraką, likę taip pat nori grįžti namo.

Tikrovė su šiuo idiliniu paveikslėliu, švelniai sakant,visiškai nesiderina. Žiemai migrantus grasina apgyvendinti viename iš Lietuvos kalėjimų, jie pasakoja, jog Lietuvos sienos apsaugos pareigūnai juos muša ir bando išstumti atgal į Baltarusiją.

Rugpjūčio mėnesio 15 d. pasikeitus valdžiai Kabule, į ES iš karto plūstelėjo prognozuota pabėgėlių iš Afganistano banga. Į „riebią“ Vokietiją afganai bando prasiskverbti, tame tarpe, ir per Baltarusiją ir Pabaltijį. Ir tai jau sukelia žmogiškąsias tragedijas.

Taip, nevilties apimtas pabėgėlis iš Afganistano bandė nusižudyti prie Baltarusijos – Latvijos sienos. Remiantis Baltarusijos pasienio komiteto pranešimu, vyriškis puolė po sunkvežimio ratais, po to, kai Latvija devintą kartą atsisakė leisti jam įvažiuoti.

Dabar toks skandalas kilo Latvijoje. Latvijos sienos apsaugos pareigūnai kaltinami 3 milijonų eurų vagyste statant tvorą palei sieną su Baltarusija. Pasieniečiai pinigus spygliuotai vielai paėmė, atsiskaitė, jog tvorą pastatė, o tvoros tai nėra.

„Savo ruožtu, Valstybės sienos apsaugos pareigūnai ir techninės priežiūros specialistai, žinodami, jog įmonė pateikė melagingą informaciją apie atliktus darbus, nepasinaudojo savo teisę ir nepateikė pretenzijos dėl netinkamo sutartinių prievolių atlikimo, o vietoj to suderino darbus ir patvirtino, jog jie yra atlikti“, - praneša Latvijos Vidaus saugumo biuras.

Kad įsivaizduoti efektą, kuriuo tokios naujienos paveikia gyventojus, palyginsime jas su oficialiu migracijos krizės aprašymu. Arabų nelegalų invazija į Baltijos šalis – tai „hibridinis karas“ kurį prieš savo kaimynes demokratines valstybes pradėjo „paskutinis Europos diktatorius“ Lukašenka už tai, jog jos remią laisvę, žmogaus teises ir demokratinę opoziciją Baltarusijoje. Latvijai tai reiškia, jog kalbama apie nacionalinį saugumą, visa tauta turi susitelkti prieš agresorių...

Migracijos krizė Pabaltijyje – kaip toks skandalas. Jau kiek metų Lietuva, Latvija ir Estija savo vakarų sąjungininkams seka pasakas, jog jos - rytinis NATO forpostas, jog jos gyvena visą laiką laukdamos rusų agresijos, jog jos gina Europą nuo grėsmės iš Rytų. Kiek jos atsiskaitinėjo apie karinių išlaidų didėjimą, kiek prašė turtingas NATO šalis investuoti į Baltijos šalių „sekjuritizacija“...

O dabar, pasirodo, jog visa tų šalių rytų sieną – skylėta. Dabar, jai sutvarkyti NATO sąjungininkai Pabaltijo šalims išskiria spygliuotą vielą, lyg humanitarinę pagalbą Afrikos tautoms.

Pasirodo, jog per trisdešimt „antros nepriklausomybės“ metų ji taip ir pasiliko siena tarp TSRS sąjunginių respublikų, o visiškai nebuvo sutvarkyta pagal visas taisykles, kaip tikra valstybės siena. Nors Baltijos šalims įstojant į NATO ir Europos Sąjungą tai buvo numatoma.

Išeina, jog visa ta „grėsmės iš Rytų“ tema – grynas sukčiavimas.

Ir regioninės krizės kas kartą tai atveria. Kai 2014 metais prasidėjo krizė Ukrainoje, pasirodė, jog Lietuva, kuri garsiausiai visų ES šūkavo apie „rusišką grėsmę“, iš NATO šalių visų mažiausiai skyrė lėšų gynybai – 0,8 % BVP. Sekančiais metais visomis tiesomis ir netiesomis patempė iki 2 %, bet nemalonus jausmas liko.

Taip ir su siena. Baugino – baugino žmones manevrais „Zapad -2017“, žaliais žmogeliukais“ ir hibridine agresija“, o kai reikalas priėjo prie migracijos krizės, pasirodė, jog derimos valstybės sienos kaip ir nėra, kadangi jos sutvarkymui skirtas lėšas vogė ištisus 30 metų.

Ir iki šio vagia.

Juk Latvijos ir Lietuvos gyventojai jau seniai kalba ne apie Lukašenkos veiksmus, ne apie Putino ir Kremliaus vaidmenį, ne apie tą, ar juos remia Vakarų šalys arba smerkia prievartą prieš migrantus. Kalba eina apie tai, jog „karalius tai nuogas“.

Apie tai, jog jų valstybių vadovai, kurie būk tai 30 metų vedė ir atvedė Estiją, Latviją ir Lietuvą į sėkmę, iš tikrųjų sugeba tik plepėti „apie rusišką“ grėsmę, čiulpti pinigus iš Europos Sąjungos ir juos susidėti į savo kišenes.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 5 — id: `scraped:rubaltic_lt:94870d258ce8759e`

**Title:** Pabaltijo uostai pradėjo karą dėl Ukrainos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Kompensuoti rusiško tranzito netekimą Latvija gali tik krovinių srauto iš Ukrainos padidėjimo sąskaita. Apie tai pareiškė Pabaltijo respublikos Susiekimo ministerijos atstovas Andris Maldups. Pažymėtina, jog analogiškas planas neseniai buvo pagarsintas  Lietuvoje: Klaipėdos uostas taip pat ketina vystyti bendradarbiavimą su Ukraina ir kitomis Juodosios jūros regiono šalimis (visų pirma, su Turkija).

Naujienos apie sunkią „Latvijos geležinkelio“ (LDz) padėtį pasirodo pavydėtinai reguliariai. Rugpjūčio mėnesį kompanija paskelbė apie eilinį masinį atleidimą iš darbo: artimiausiu metu bedarbių gretas papildys 700 geležinkeliečių. Iki to buvo pranešta apie dukterinės LG bendrovės, kuri specializacija buvo bėgių tiesimas ir jų atnaujinimas, likvidavimą. Nėra krovinių vežėjo – nėra reikalo atnaujinti geležinkelio infrastruktūrą.

Paskutinė tokio tipo naujiena pasirodė leidinyje Latvijas Vēstnesis: dukterinė LDz įmonė – krovinių vežėjas LDz Cargo – varžytinėse parduoda 200 nereikalingų vagonų. Už visus šiuos lotus kompanija ketina gauti mažiausiai 1,2 milijono eurų ir tuo pačiu pagerinti savo nestabilią finansinę padėtį (2020 metais LDz Cargo apyvarta sumažėjo 36 procentais).

Tarp kitko, Latvijos ir užsienio žiniasklaida į eilinį LDz išpardavimą reagavo ramiai. Paskutiniu metu panašios varžytinės organizuojamos reguliariai. Parduodami ne tik vagonai, bet ir lokomotyvai, bėgiai, automobiliai, nekilnojamas turtas.

Atsakingi asmenys visgi bando ieškoti išeitį iš aklavietės. Pavyzdžiui, LDz valdybos pirmininkas Maris Kleinbergs praėjusių metų vasarą ketino įsisavinti laivų ir automobilių ekspedijavimo paslaugų rinką. Mes galime tik spėlioti, kaip realizuojama ši idėja. Užtai žinoma, jog pas Latvijos uostų darbuotojus ir geležinkeliečius subrendo naujas šalies tranzito šakos gelbėjimo planas. Pagrindinis vaidmuo jame skiriamas Ukrainai.

Ne per seniausiai LDz ritošā sastāva serviss (dar viena LDz „dukrelė“) Kijeve gavo  lokomotyvų remonto paslaugų sertifikatą. Jos vadovas Girts Ivanovs pažymi, jog Ukrainoje yra kuo užsiimti – tai rinka su gerai išvystyta geležinkelio infrastruktūra ir stambiu geležinkelio riedmenų sąstatu.

„Sumuojant dialogus, šalys konstatavo Odesos uosto ir Latvijos uostų bendradarbiavimo galimybių persvaros virš konkurencijos vyravimą. Šia prasme perspektyviausiomis  kryptimis buvo pripažintas multimodalinių pervežimų vystymas tarptautinių transporto koridorių rėmuose, vienijančių Juodosios Baltijos jūrų logistinius maršrutus“,- skelbiama Odesos jūrų uosto  Interneto svetainėje

Latviai, savo ruožtu, siūlo konkretų tikslą: atnaujinti keleivinių traukinių judėjimą maršrutu Kijevas – Ryga. Anksčiau tarp paminėtų miestų kursavo taip vadinamas „keturių sostinių traukinys“ (pakeliui jis užvažiuodavo į Minską ir Vilnių).

Pokalbio su analitiniu RuBaltic.Ru portalu metu Rusijos Pabaltijo tyrimų asociacijos (RPTA) prezidentas Nikolaj Meževič klausė: kas iš viso naudojosi geležinkelio maršrutu Ryga ir Kijevas?

„Jei tai gastarbaiteriai, tai jiems nėra jokio reikalo vykti per Baltarusiją. Jei tai diplomatai, tai, atleiskite, jie tokiais traukiniais nevažinėja? Vykstantieji pas gimines?  Pas draugus? Orlaivis bet kokiu atveju konkurencingesnis keliaujant tokiais atstumais. Taip, kad mums pateiktas burbulas, kuris, kaip ir visi vaikiški burbulai6 kurį tai laiką gali išsilaikyti, o vėliau neišvengiamai sprogs“,- sakė Meževič.

Kokia prasmė pūsti šį burbulą dar kartą? Be to, vargu, ar Ukrainai ir Latvijai pasiseks nutiesti naują geležinkelio maršrutą per Baltarusiją.

Tarp kitko, keleivių srautas – tai, ne daugiau, kaip malonus bonusas prie krovinių pervežimo, kurie Latvijai žymiai pelningesni. Ukrainoje LDz taip pat ketina, visų pirma, ieškoti naujų tranzito šaltinių. Latvijos transporto ministerijos ekspertas Andris Maldus mano, jog Kijevui būtu naudinga eksportuoti grūdus per Pabaltijo respublikos teritoriją. Ir dar, bendradarbiavimas su Ukraina sudarys galimybę užmėgsti ryšius su patrauklesniu krovinių siuntėju – Turkija.

„Turkiškos prekės yra plačiai išplitusios Europoje, mes tikimės juos pritraukti, ir, visų pirma, tai atitinka Ukrainos interesams didinti jos tranzito potencialą. Yra tarpvalstybinės komisijos, darbo grupės, kurios aktyviai užsiima bendradarbiavimu su Kazachstanu ir Uzbekistanu. Tai pagrindinės Rytų rinkos, su kuriomis mums reikia tęsti darbą ieškant naujų krovinių“, - pasakė Andris Maldus.

Jos Klaipėdos uostas ir geležinkelis ruošiasi atsisakyti gabenti baltarusiškas kalio trąšas. Teoriškai šiuos nuostolius turi kompensuoti Ukraina ir Turkija.

„Geležinkeliuose, iš visų krovinių, ukrainietiški sudaro maždaug 3-4 proc., uostas ukrainietiškų krovinių perkrauna tik 1 procentą. Šiandieniniame, ypač geopolitiniame kontekste, kalbant apie šalių, krovinių, prekių diversifikaciją, būtent Ukraina yra ta kryptis, kuri mums sukuria daug naujo ir neišnaudoto potencialo“, – sakė Lietuvos transporto ir komunikacijų ministras Marius Skuodis.

Bet šis potencialas  lieka neišnaudotas. Ukraina turi savo galingus uostus Juodojoje ir Azovo jūrose, kurie, pagal 2019 metų rezultatus, apdorojo istoriškai rekordinę krovinių apimtį. Jų sėkmės laidas – tėvyninės produkcijos pervežimo apimčių didėjimas. Iš tikrųjų, kam varyti geležinkelio sąstatus į Klaipėdą, Rygą ir Ventspilį, jei jie yra laukiami Odesoje, Chersone bei Mariupolyje?

Tie patys lietuviai jau seniai įtikinėja turkų krovinių siuntėjus, jog jiems nebūtinai aplenkti žemyną jūra –maršrutą nuo Ukrainos iki Klaipėdos galima nutiesti sausuma. Bet toliau įsivaizduojamų eksperimentų reikalai nepajudėjo.

Šiame kontekste Latvijos planai atrodo dar absurdiškesni. Bet kokius krovinius, kurie teoriškai iš Ukrainos gali būti vežami į Rygą, Ventspilį ar Liepoją, medžios dar vienas „grobuonis“ – Klaipėdos uostas.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 6 — id: `scraped:rubaltic_lt:2c79da170a1877b6`

**Title:** Po migrantų – sunkvežimiai: Lukašenka rado naują būdą kaip nubausti Lietuvą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Tarptautinė kelių transporto sąjunga (IRU) prašo Baltarusijй atsisakyti navigacinių plombų panaudojimo. Nuo rugpjūčio mėnesio 30 d. nurodyti prietaisai privaloma tvarka įrengiami visuose komercinėse transporto priemonėse, kurios kerta Lietuvos – Baltarusijos sieną. Vežėjui viena plomba apsieis 50 eurų, o bendras kompanijų, gabenančių krovinius tranzitu per Lietuvą į Rytus, nuostolis bus skaičiuojamas milijonais eurų per metus. Daugelis iš jų, tikriausiai, keis maršrutą ir įvažiuos į Baltarusiją iš Lenkijos pusės.

Lietuvos vežėjai automobiliais vieni iš pirmųjų pajuto Minsko ir Vilniaus santykių paaštrėjimą po praeitų metų rugpjūčio mėnesio įvykių. Baltarusijos pasienio tarnybos pareigūnai pradėjo griežčiau, nei anksčiau, tikrinti jų vilkikus. Kiekviena prastovos valanda tolimų reisų vairuotojams (tiksliau, jų darbdaviams) apsieina nuostoliais.

„Pas mus yra papildoma patikrinta informacija, jog automobilių tikrinimas tapo aktyvesnis. Stato po rentgenu, tikrina ilgiau. Teisiniu atžvilgiu pareikšti pretenzijų mes negalime. Tikrina, bet lėtai, kaip vežliai. Netgi tas mašinas, kurios važiuoja su tranzitu stato į eilę, sako, jog nėra galimybės jas patikrinti, reikės palaukti“,- skundėsi Lietuvos nacionalinės vežėjų automobiliais asociacijos „ Linava “ prezidentas Romas Austinskas.

Jau rugsėjo pabaigoje, to pačio Austinsko žodžiais tariant, situacija ant sienos stabilizavosi. Po incidento su skubiu Ryanair orlaivio nutupdymu Minsko aerouoste ir Romano Protasevičiaus sulaikymo, įvažiavimas į Baltarusiją iš Lietuvos pusės vėl tapo kebliu. Eilės pailgėjo, bet Linava demonstratyviai atmetė Lietuvos URM rekomendacijas vengti kelionių į kaimyninę šalį.

Šie prietaisai leidžia sekti krovinių judėjimą. Anksčiau juos kabindavo vilkikams, kurie papuldavo už tranzito taisyklių pažeidimą (pavyzdžiui, nukrypdavo nuo nustatyto maršruto). O dabar visi sunkvežimiai, kertantys Lietuvos – Baltarusijos sieną turi naudotis navigacinėmis plombomis. Išimtis padaryta tik tiems vilkikams, kurie vyksta tranzitu iš Kaliningrado srities į tėvyninę Rusijos teritoriją.

Navigacinių plombų sistema aktyviai įdiegiama ir Baltarusijoje ir kituose Eurazijos ekonominės sąjungos (EAES) šalyse. Praėjusiais metais elektroninis automobilių sekimas buvo laikomas, kaip vienas iš kovos su koronaviruso platinimu būdų.

Be to, Baltarusijos Valstybės Muitinės komiteto pirmininko pavaduotojo Andrėjaus Bolšakovo žodžiais tariant, kai kuriais atvejais plomba leidžia kontrolės punktuose sumažinti tikrinimo priemonių skaičių.

Viena plomba vežėjui apsieis 50 eurų. Ir tai tik kol kas.

„Verslas bijo, jog plombų taikymo kaina su laiku gali žymiai padidėti. Jei dabar ji kainuoja apie 50 eurų. Iki metų galo ji gali išaugti iki 250 ir daugiau eurų. Tuo atveju, jei neteksime logistinio konkurencingumo, ne tik auto transportas apeis Lietuvą, bet ir laivai teiks pirmenybę Lenkijos ir Latvijos uostams“,- sakė Linavos generalinis sekretorius Zenonas Buivydas.

Apie kokius nuostolius kalbama? Į šį klausimą atsako tas pats ponas Buivydas. Jo paskaičiavimu, bendri vežėjų, kurie veža krovinius į Rytus per Lietuvą, nuostoliai sudaro maždaug 600 tūkstančių eurų į mėnesį. O metų gale tie nuostoliai bus skaičiuojami milijonais.

Tokiu būdu tranzitinių krovinių operatoriai turi pasirinkti. Jie gali, kaip ir paprastai, sudaryti maršrutą kertant Lietuvos -Baltarusijos sieną ir kiekvieną kartą mokėti po 50 eurų (tai geriausiu atveju – jei Baltarusijos muitininkai nepakeis kainų). Arba gali keisti maršrutą.

Lietuvos transporto ir komunikacijų ministras Marius Skuodis laukia, kad artimiausiu metu bus sustabdytas baltarusiškų trąšų tranzitas. Jei jo logika tiksli, tai jau gruodžio mėnesį ir Klaipėdos uostas, ir Lietuvos geležinkelis (LG) atsisakys „Belaruskalij“ produkcijos.

Pabaltijo respublikai tai gresia rimta tranzito krize, kuri pagilės dėl problemų krovinių pervežimų automobiliais sferoje.

Reikalas tame, jog pervežimų automobiliais Lietuvoje sektorius ir be to pergyvena nepaprastus laikus. Pandemijos metu daugiau nei šimtas kompanijų nutraukė savo veiklą. O tie, kuriems pasisekė išgyventi, žiūri į kaimyninę Lenkiją, Ten didesnė rinka, ten naudingiau organizuoti verslą, paprasčiau samdyti darbuotojus, pigiau apiforminti licenzija ir t.t

Dar prieš dvejus metus Savesta Consulting kompanija patvirtino, jog tik jai tarpininkaujant iš Lietuvos į Lenkiją perėjo daugiau nei 60 transporto kompanijų. Galimai, po praėjusių metų įvykių šis procesas tapo greitesnis.

„Verslo perkėlimas yra susijęs ir su tuo, jog Lietuva atšaukė savo ambasadorių iš Baltarusijos. Todėl visi automobilių vairuotojai įsidarbina kompanijose, kurios randasi Lenkijoje, - tai paprasčiau ir greičiau“,- paaiškina Savesta Consulting valdybos narys Ignas Voblikas.

Už Pabaltijo respublika užsistojo Tarptautinė kelių transporto sąjunga (IRU). Ji ragina Baltarusija atsisakyti plombų panaudojimo.

„Tokiu būdu dirbtinai kuriama skirtingų rūšių transporto diskriminacija, kas yra neteisinga transporto operatorių atžvilgiu. Ketinimas įrengti navigacines plombas Eurazijos ekonominėje zonoje dar negatyviau paveiks prekybą ir transportą šiame regione, sukels neigiamus padarinius ekonomikoje ir konkurencingume“, - sakė IRU generalinis sekretorius Umberto de Pretto.

Patys vežėjai kreipiasi į Lietuvos Vyriausybę prašydami pasitarti su kaimynais (Lenkija ir Latvija), kad bendromis jėgomis įtikinti Lukašenką to nedaryti.

Tegul pabando blokuoti arba pakeisti Baltarusijos Vyriausybės nutarimą – negi be reikalo Lietuvos Seimas jai suteikė prezidento įgaliojimus?

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 7 — id: `scraped:rubaltic_lt:ad09a5f0a3da8c72`

**Title:** Rusija atsisakė grįžti  į pagrindinį Vakarų „elitinį klubą“

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Į netikėtą Japonijos URM pareiškimą dėl Kinijos ir Rusijos pakvietimo dalyvauti „didžiojo septyneto“ (G-7) susitikime dėl Afganistano, Maskva reagavo dar labiau netikėtai. Smolensko aikštėje pasijuokė iš „vakarų partnerių“ ir davė suprasti, jog Rusiją nedomina galimybė, kad ir laikinai, sugrįžti į G-7. Ši istorija puikiai apibendrina „Putino tarptautinio izoliavimo“ kursą: jau ne tik atskiros Vakarų šalys, bet ir iš viso Vakarai pripažįsta, jog be Maskvos neįmanoma spręsti pagrindines pasaulio problemas, ir vilioja Rusiją atgal į savo „elitinius klubus“. Tačiau, vilionės Rusijos nepaveikė: jai vakarų klubai bei patys Vakarai, kaip tokie, jau neteko savo elitiškumo.

Japonijos užsienio reikalų ministras Tosimicu Motegi papasakojo apie rengiamą neeilinį „septyneto“ šalių URM vadovų susitikimą. Susitikimas numatytas trečiadienį, rugsėjo mėnesio 8 dieną ir pašvęstas išskirtinai situacijai Afganistane.

Japonų ministras pasakė, jog į susitikimą taip pat pakviesti Rusijos ir Kinijos URM vadovai. Rusijai ši naujiena ypatingai pažymėtina: gi ji neseniai buvo pilnavertė G-7 narė.

Dabar gi, be jokio iškilmingumo, tyliai prašo laikinai grįžti atgal. Todėl, kad Rusija, kaip pasirodo, ne ta šalis, be kurios galima spręsti pagrindinius pasaulinius klausimus.

Konkrečiai, dėl Afganistano. Be Rusijos afgano klausimas nesprendžiamas, o jo nespręsti negalima.

Paskutiniais metais tai jau antras pasiūlymas Rusijai vėl dalyvauti „septyneto“ veikloje. Pirmą kartą „septynetą“ vėl paversti „aštuonetu“ prieš metus pasiūlė buvęs JAV Prezidentas Donaldas Trampas. G-7 jis matė tokį vilioklį, kurio pagalba galima užkirsti kelią, keliančiam pavojų JAV, Kremliaus suartėjimui su Kinija.

Tada Trampą užsipuolė visi kiti „klubo nariai“. Kaip galima kalbėti apie Rusijos sugražinimą į „septynetą“ iki to, kol ji „pakeis savo elgesį“? Rusus nubaudė pašalindami iš pačio pagrindingiausio pasaulio „elitinio klubo“, o dabar Trampas siūlo panaikinti visą pedagoginį efektą ir kapituliuoti prieš Putiną?

Praėjo metai. Nesisteminį Donaldą Trampą Baltuosiuose rūmuose pakeitė super sisteminis Džo Baidenas. Kuris, tarp kitko, daro tą patį, ką darė jo skandalingas pirmtakas. Išveda kariuomenę iš Irako ir Afganistano, kalba, jog vietoj amerikiečių kareivių, žmonės patys turi kovoti už savo laisvę ir laimę, ir Amerikai reikia spręsti savo vidaus problemas, o ne organizuoti demokratiją po visą pasaulį.

„Partneriai demonstruoja nesisteminį elgesį. Prieš dvi dienas iš Berlyno ir Paryžiaus mums atėjo signalai dėl kažkokio tai susitikimo, bet apie septynetą kalbos nebuvo. Po to buvo Tokijo pareiškimas, bet jau „septyneto“ kontekste. Visą tai vyksta septyneto įvairaus kalibro pareiškimų fone dėl Rusijos, ar tai dalyvavimo, ar tai nedalyvavimo formate“, - komentavo Japonijos užsienio reikalų ministro pareiškimą Rusijos URM atstovas spaudai Marija Zacharova.

Oficialus Smolensko aikštės atstovas dėl signalų pareiškia sekančią išvadą: pas vakarų partnerius stebimas „supratimo, ko jie nori iš savęs ir iš supančio pasaulio, nebuvimas“.

Tokia sarkastiška Maskvos reakcija – ne mažiau reikšminga, negu kvietimas RF dalyvauti „septynete“.

O juk pašalinimas iš “didžiojo septyneto“ 2014 metais skaitėsi kaip pati rimčiausia neekonominė sankcija Rusijai. Kaip ir priėmimas į „septynerių klubą“ 1990 metais buvo vadinamas svarbiausiu demokratinės Rusijos užsienio politikos pasiekimu, taip ir išvarymas iš G-7 buvo paskelbtas svarbiausiu „Putino režimo“ tarptautiniu   pralaimėjimu.

Iš Rusijos atėmė teisę sėdėtu už stalo, už kurio buvo nulemiama pasaulio ateitis – taip tai buvo pateikiama. Gal būt taip iš tikrųjų ir buvo...1990 metais.

Dabar gi situacija pasikeitė.

Ir Kinija.

Taip, kad Rusijos sugrįžimu į „septynetą“ labiau suinteresuotas „septynetas“, o ne Rusija. Atitinkamai, ji ir siūlo, kartu su tuo, jog Rusija ne trupučiuką „nepakeitė savo elgesio“, Krymą pripažįsta savu, iš Ukrainos reikalauja Minsko susitarimų realizavimo ir prie Ukrainos sienų kaupia karines pajėgas, kai tik Kijeve kažkam tai pradeda niežtėti Dombaso reintegracijos kariniu būdu „kroatiškas scenarijus“.

Tačiau, dabar Vakarams principai nerūpi. Būtina pademonstruoti, jog jų „didysis septynetas“ dar sugeba lemti pasaulinius procesus. Be Rusijos ir Kinijos to niekaip nepadaryti, todėl „grįžk, aš atleisiu viską!“

Jei vietoje RF būtu vis ta Ukraina, Vladimiras Zelenskis, pakvietus jo šalį į G-7, iš laimės iš karto apstulbtu. Bet ne Rusija. Jai tie provinciniai kompleksai netinka.

Pageidaujate, kad Rusija padėtu jums išvalyti visą tai ką jūs pridarėte Afganistane? Rusija jums pasakys, kaip, kada, kokiomis sąlygomis ir kokia kaina ji pasiruošusi suteikti jums šią paslaugą.

Sugrįžimas į „didįjį septynetą“ (tuo labiau – laikinas) - to tikrai neverta tokia paslauga. Už šį Rusijos sugrįžimą jūs dar turite primokėti.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 8 — id: `scraped:rubaltic_lt:412d3c10905de78b`

**Title:** Amerikiečiai palaimino Lietuvą „kryžiaus žygiui“ prieš Kiniją

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Po ilgos pauzės Lietuva pasiryžo atsakomajam žingsniui diplomatiniame konflikte su Kinija ir, praėjus beveik mėnesiui po kinų ambasadoriaus atšaukimo iš Vilniaus, atšaukė savo ambasadorių iš Pekino. Lietuvos valdžios ryžtą ir toliau konfrontuoti su Padangių šalimi parėmė amerikietiški sąjungininkai, kurie deklaratyviai palaikė Vilniaus kursą, nukreiptą į bendradarbiavimo su Kinija griovimą. Lietuva tęsia Jungtinių Valstijų interesų aptarnavimą Europoje, pagal galimybes įnešdama indelį į, ne tik Rusijos, bet ir Kinijos suturėjimą. Apdovanojimu jai pažadėtas pritariantis paplekšnojimas per petį.

„Jūsų šalis geriau nei kiti supranta, ką reiškia gyventi slegiant brutaliam autokratiniam režimui. Kaip praėjusios kartos kėlėsi prieš Tarybų Sąjungos blogį, taip ir dabar Jūs kylate prieš Kinijos Komunistų Partiją ir didžiausią per paskutiniuosius dešimtmečius grėsmę demokratiniam gyvenimo būdui“, - atvirame laiške Lietuvos vadovybei parašė 15 JAV Atstovų rūmų kongresmenų.

Pagrindinė Amerikos politikų laiško Vilniui mintis suformuota sekančiai: Jungtinės Valstijos sveikina „ryžtingą Lietuvos valią kovoje su augančia Kinijos Komunistų Partijos įtaka Europoje“.

Lietuvos – Kinijos santykių griovimo kryptis, kurią įgyvendina Lietuvos URM, pripažįstama teisinga ir verta pagyrimo. Tai galima laikyti moraline parama, kadangi Vilniuje išsigando, matydami, link ko veda jų politika. Visgi, KLR ambasadoriaus atšaukimas į Pekiną ir kinų atsisakymas geležinkelio tranzito - tai ne juokai.

Amerikiečiai kursto bugščius sąjungininkus: viskas teisinga, taip ir reikia. „Pekino reakcija ir bandymai diktuoti užsienio politiką per prievartą ir pasityčiojimą visiškai nepriimtina. (...) Mes, kartu su Jumis, smerkiame atsakomąjį Pekino elgesį“, - sako amerikiečių kongresmenai lietuvių politikams.

Rodėsi, jog visą tai parašė ne JAV Prezidentas Džozefas Baidenas, ne valstybės sekretorius Entoni Blineken, ne Prezidento nacionalinio saugumo patarėjas Salivan, ir ne kas kitas, kas dabar organizuoja Vašingtono užsienio politiką. Tai pasakė, remdamiesi opozicinės JAV Respublikonų partijos iniciatyva, keletas Kongreso Atstovų rūmų deputatų, Tačiau, neišlepintam didenybės dėmesiu vasalui Lietuvai pakako ir tokių paramos spindulių iš už okeano.

Buvusias prieš tai keletą savaičių Lietuvos URM tūpčiojo vietoje ir siuntė Pekinui signalus: gal būt susitarsime? URM vadovas Gabrielius Landsbergis, kuris asmeniškai pats sugriovė Lietuvos-Kinijos santykius, kalbėjo, jog darbuojasi stengdamasis juos atstatyti. Prezidentas Gitanas Nausėda interviu užsienio žurnalistams pasakė, jog Lietuva tęs savo principingą užsienio politiką, ir kartu su tuo sakė, jog Vilnius pasiruošęs dialogui su Kinija.

JAV pastatė tašką visiems tiems blaškymams ir abejonėms.

Rodėsi, ką gali padaryti Lietuva dėl Vokietijos, Prancūzijos ir kitų didžiųjų ES šalių, na ir bendrai ES santykių sugriovimo su Kinija? Visų pirma, kaip rodo Europos Sąjungos dialogo su Rusija sugriovimo patirtis, kai ką gali. Antra, kažkas tai turi būti likusiems amerikiečių satelitams Europoje silpnaprotiškumo ir narsumo pavyzdžiu. Trečia, Jungtinių Valstijų kortų kaladėje ne vien tik Lietuva.

JAV kongreso nariai, be viso kito, pritaria Lietuvos sprendimui išeiti iš «17+1» projekto - Kinijos bendradarbiavimo su Centrinės ir Rytų Europos šalimis formatas, kuris savo ruožtu, yra daug platesnio kinų projekto „Viena juosta    - vienas kelias“ dalimi. Amerikiečių žodžiais tariant, Padangių šaliai šis projektas reikalingas tam, kad „investicijas ir prekybą paversti politine įtaka, svertu, dažnai per skolų žabangas ir priklausomybę“.

Šioje dalyje lietuviško „principingumo“ palaikymas kvepia lyg tai paguoda, lyg tai sadizmu.

Lietuvos vadovų neryžtingumas tęsti konfliktą su Padangių šalimi, į kurį jie neapdairiai įsivėlė, buvo susijęs su nenoru atsisakyti savo svajonės. Jei santykiuose su Rusija dar prieš 15 metų amerikiečiai Vilniui išdėstė visus taškus virš „i“, tai Jungtinių Valstijų konfliktas su Kinija - palyginti naujas siužetas, ir Lietuvą valdantys galvočiai tai suprato labai vėlai.

Dar prieš trejus metus tuometinė Lietuvos vadovė Dalia Grybauskaitė skraidė į Kinija reklamuoti lietuviška kefyrą ir kildytą pieną, Skraidė tuo pačiu metu, kai JAV valstybės sekretoriaus padėjėjas Europos ir Eurazijos klausimais inspektavo Rytų Europos satelitus ir įtikinėjo juos apie kontaktų su kinų komunistais neleistinumą.

Dar prieš metus Lietuvoje svajoje apie „Naująjį šilko kelią“, milijardines kinų investicijas, ir milijonų tonų kinų krovinių į Europą per Klaipėdos uostą srautą. Dabar krovinių vežimas geležinkeliu iš Kinijos į Lietuvą sustabdytas. Apie investicijas Klaipėdoje galima užmiršti, o gamintojai rauda, jog kinai daugiau nebenori pirkti lietuviškas statybines medžiagas ir pieną.

Ar daug ko pasiekė Lietuva per „Rusijos suturėjimo“ dešimtmečius? Ką ji gavo vietoj to? Ekonominės krizės, jaunimo emigravimas, investorių pasitraukimas iš šalies, gyventojų senėjimas ir išmirimas, savižudybių ir alkoholizmo antirekordai – antirusiška politika ir palankumas Jungtinėms Valstijoms tuos procesus ne taip kad įtakojo.

Tas bus ir su „Kinijos suturėjimu“. Pinigų iš Pekino Lietuva daugiau niekada negaus, o ką duos Vašingtonas? Ne daugiau kaip dėdės Semo pritariantį Lietuvos vadovų paplekšnojimą per petį su žodžiais: taip vaikinai, mums tokių kvailių kaip jūs, niekur nesurasti.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 9 — id: `scraped:rubaltic_lt:e09d579e4fed2096`

**Title:** Bandymų era pakeisti pasaulį baigėsi: Baidenas apkarpė sparnus Lietuvai

**Source:** rubaltic_lt (propaganda)

**Text:**

```
JAV Prezidentas Džozefas Baidenas pareiškė, jog amerikiečių bandymų era jėga pakeisti pasaulį baigėsi, ir tuo jis susumavo kaip ir amerikiečių pajėgų bėgimą iš Afganistano, taip ir nenusisekusį Ukrainos Prezidento Vladimiro Zelenskio vizitą į Vašingtoną. JAV įtakos agentų veiklą Rytų Europoje, nukreipta į „demokratijos eksportą“ į buvusias tarybines respublikas, dabar nuvertinta.

Oficialiai daugiau nėra „demokratijos prastūmimo“ užsakovo.

„Viena kritiška pastaba: pasaulis keičiasi. Mes rimtai konkuruojame su Kinija, prieš mus įvairiapusiai iššūkiai, kurie liečia Rusiją, kibernetinius išpuolius, branduolinį ginklą, mes turime pademonstruoti JAV konkurencingumą šioje XXI amžiaus kovoje. Rusijai ir Kinijai būtu patogu, jei JAV užstrigtų dešimtmečiui ir daugiau metų Afganistane. Šis sprendimas dėl Afganistano liečia ne tik Afganistaną, kalbama apie tai, jog baigėsi bandymų era jėga pertvarkyti kitas šalis“,- kalbėjo Džozefas Baidenas kreipimesi per televiziją į tautą, pašvęstam paskutinių Amerikos karinio kontingento padalinių išvedimui iš Afganistano.

Anksčiau JAV Prezidentas išėjima iš Afganistano jau komentavo tiesioginiu melu, jog amerikiečiai lindo į tą šalį išimtinai ginti savo interesus ir niekada neturėjo tikslo užsiimti ten valstybės kūrimu (nation building). Dabar gi Baidenas oficialiai viską „susumavo“.

Tartum specialiai tiems, kurie gali griebtis už šiaudo ir pasakyti, jog tai sakoma ne bendrai, o tik kontekste su Afganistanu, Baidenas patikslino: „sprendimas dėl Afganistano, tai ne tiesiog dėl Afganistano“. Tai apie JAV tarptautinę politiką iš viso.

Šis, oficialiai patvirtintas, strateginis JAV sprendimas paaiškina daug ką. Pavyzdžiui, nenusisekusį Ukrainos Prezidento Vladimiro Zelenskio vizitą į Vašingtoną.

Ko vertas Zelenskio pareiškimas, jog jis „užmiršo“ pakviesti Džo Baideną apsilankyti Ukrainoje. Bendrai paėmus, kvietimas priimančiai šaliai aplankyti svečio šalį su atsakomuoju vizitu – neatskiriama diplomatinio etikėto dalis.

Išeina taip, jog Zelenskiui daug paprasčiau pasakyti, jog jis apsikvailino aukščiausiame lygyje ir apgėdino ukrainietišką diplomatiją, negu pripažinti, jog šalys išsiskyrė nepatenkintos viena kita taip, jog netgi atsakomojo pakvietimo nebuvo?

Ukrainos delegacija skrido į Vašingtoną tradiciškai nusiteikusi kažko tai gauti.

„Maršalo planas“ Ukrainai, kompensacijos Kijevui už amerikiečių sutikimą „Šiaurės srauto – 2“ statybai , amerikiečiai privers Rusiją gražinti Donbasą ir Krymą, naujos kredito linijos reformų programoms......

Gavo – špygą. Visas aktyvas - ukrainiečių kariuomenės perginklavimo programa už 60 milijonų dolerių ir patikinimas, jog JAV yra Ukrainos teritorinio vientisumo šalininkė. Viskas. Nebuvo išsakyta netgi pažadų dėl ES, ir Zelenskis, kalbėdamas apie derybų rezultatą pripažino, jog derybos ne visada vyko „saulėtoje atmosferoje“.

Kaip paaiškinti šią nesėkmę kontekste „JAV bandymų pertvarkyti kitas šalis era baigėsi“? Labai paprastai.

Tegul Ukraina ir toliau lieka korumpuota, griūnanti, tuštėjanti. Jei laiku ją palikti, tai visos Ukrainos problemos taps Rusijos problemomis, o JAV tai naudinga. Tiesa, taps dar ir ES šalių problemomis, bet sąjungininkai Europoje – suaugę vyrai, jie ir patys susitvarkys. Na, o jei kas, Amerika išreikš jiems savo gilų susirūpinimą.

Tai koks gi „Maršalo planas“? Koks proeuropietiškų reformų palaikymas finansais? Mes daugiau nekuriame demokratijų. Galite paskęsti purve, svarbiausiai – lokite ant Rusijos, kaip pasakė Rusijos URM vadovas. Amerikai to bus gana.

Nauja realija bus žiauri ne vien tik Ukrainai. Dešimtys pasaulio šalių paskelbė savo kursą kurti ir skleisti demokratiją, pagrinde ne dėl to, kad sukurti ir paskleisti demokratiją, o dėl to, kad tų kilnių tikslų įgyvendinimui gauti amerikietišką paramą – karinę, finansinę, politinę.

Kokį nesveiką aktyvumą šiais metais Lietuva organizavo greta Rusijos sienų! Pirmųjų asmenų vizitai į Ukrainą, Moldovą, Gruziją, Armėnija, Azerbaidžaną; „išrinktosios prezidentės“ Svetlanos Tichanouskos gastrolių turo rengimas, vainikuotas susitikimu su Džozefu Baidenu Baltuosiuose rūmuose.

Ir visur vienas ir tas pats: žmogaus teisės, liberalinės vertybės, Europos pasirinkimas. Visiems, įskaitant ir pačią Lietuvą, aišku, jog ji viena neturi jokio, mažų mažiausio resurso, kad kam nors įsiūlyti šiuos puikius dalykus. Duok Dieve, patiems Lietuvos ministrams be deputatams apmokėti komandiruotpinigius už keliones po „Rytų partnerystės“ šalis.

Buvo akivaizdu, jog Vilniaus pageidaujamų tikslų siekis tampriai susietas su amerikiečių parama. Kad nors būtu atkreiptas jo didenybės dėmesys, bet geriau su tolimesniu finansavimu.

Analogiškai – Lenkija, tik ten, žinoma, kiti mastai. Bet visgi, pagrindinis Varšuvos rytų politikos adresatas visada buvo vienas – Jungtinės Valstijos. Jei Lenkija per savo įtakos į Baltarusijos visuomenę tinklą pasieks, jog bus pakeistas režimas Minske ir Baltarusijoje pasodins demokratinę provakarietišką vyriausybę, tai po to, ar ne ji, pagrindinis strateginis Vašingtono partneris Europoje?

Tai nereiškia, jog jie nustos įsikišinėti. Galų gale, demokratija ir progresyvinės vertybės – tai tik dūmų uždanga tam, kad kliudyti Rusijai Rytų Europoje. Rusija niekur ne prapuola, atitinkamai, pasilieka nekintanti kovos su ja užduotis.

Todėl ta pati Lietuva tęs savo nesveiką aktyvumą Moldovoje, Baltarusijoje bei kitose šalyse. Tęs, netgi iš inercijos, kovos už demokratiją motyvavimą, kadangi naujos ideologinės širmos vietiniai veikėjai sugalvoti nesugeba.

Va tik iš JAV pusės ši veikla daugiau jau nenumato jokių apsaugos garantijų ir jokios paramos.

Džozefas Baidenas į Baltuosius rūmus atėjo su žodžiais „Amerika grižo“. Omenyje turėta – į pasaulio reikalus.

Toliau – tik savarankiškai.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 10 — id: `scraped:rubaltic_lt:6d7718fbd4ecb866`

**Title:** „Kovotojai už demokratija“ atima iš Lietuvos gyventojų teisę protestuoti

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Vilniaus valdžia uždraudė surengti stambiausią per paskutiniuosius dešimt metų opozicijos mitingą Lietuvos sostinėje. Pagrindžiant draudimą, be kita ko buvo nurodoma, jog protesto akcija gali peraugti į riaušes, o protestų judėjimas Lietuvoje yra „hibridinio karo“ aktas. Susirinkimų laisvę Lietuvoje atšaukia tie patys žmonės, kurie kitose šalyse sveikina nesuderintas akcijas, pogromus ir prievartą gatvėse, kaip aukščiausią kovos už laisvę apraišką.

„Pasikeitus aplinkybėms, bendrame hibridinio karo kontekste miesto valdžia persvarstė savo spendimą ir nusprendė atšaukti anksčiau išduotą leidimą rugsėjo mėnesio 10 surengti mitingą“,- antradienį pranešė Vilniaus miesto savivaldybės Administracijos direktoriaus pavaduotojas Adomas Bužinskas. Rugsėjo mėnesio 10 mitingas turėjo įvykti praėjus lygiai mėnesiui po rugpjūčio 10 mitingo, kuris šalyje tapo pačiu masiškiausiu nuo 2009 metų sausio mėnesio riaušių, kurias išprovokavo ekonominė krizė.

Tokio gatvės aktyvumo Lietuvoje nebuvo nuo užsitęsusios 1997 – 2004 metų politinės krizės, kuri prasidėjo korupciniu konservatorių vyriausybės sandoriu su amerikiečiais, parduodant jiems už kapeikas Mažeikių NPG ir tęsėsi iki prezidento Rolando Pakso apkaltos. Dabartinio protesto masiškumas – pagrindinis simptomas, jog eilinė konservatorių vyriausybė Lietuvoje vėl sukėlė politinę krizę.

„Landsbergistams“ir jų sąjungininkams pripažinti šį faktą, suprantama, nėra noro. Ką daryti? Imti ir uždrausti!

Lietuvos valstybės saugumo departamentas informuoja, jog mitinge yra „smurtinių veiksmų bei kitų pavojų grėsmė“. Atskirai pažymima, jog akcija numatoma greta Nacionalinės bibliotekos pastato, kurios lankytojams nebus užtikrintas praėjimas į skaitytojų salę.

Visa tai vainikuojama tvirtinimu apie „hibridinį karą“. Na, tegul Lietuvos valdžia tvirtintu, jog gyventojų protesto nuotaikas išnaudoja priešiškos valstybės, idant destabilizuoti Lietuvos Respubliką. Bet ne, viskas dar blogiau.

Lietuvos Ministrė Pirmininkė Ingrida Šimonytė aiškiai pasakė: nepatenkinti lietuviai išeina protestuoti ne prieš privalomą vakcinavimą nuo koronaviruso ir ne prieš apribojimus nevakcinuotiems, o prieš Vyriausybės užsienio politiką.

Atskiras klausimas: kodėl demokratinėje šalyje negalima būti nepatenkintiems užsienio politika ir išeiti protestuoti prieš ją? Bet ponia Šimonytė, principe, atmeta teisėtus pagrindus lietuviams būti nepatenkintais. Protestuojama ne prieš „antikovidines“ priemones, o prieš jos vyriausybės užsienio politiką, o prieš tą protestuoti gali tik „penktoji kolona“ - Lietuvoje simpatizuojantys Putinui, Lukašenkai.

Visų nesutinkančiųjų paskelbimas Lietuvos priešais ir valstybės išdavikais gali dar labiau radikalizuoti protestus. Lietuvoje tai ir vyksta. Rugsėjo mėnesio 10 akcijos organizatoriai paskelbė, jog į gatvę išves 15 tūkstančių šalininkų, netgi jei mitingas nebus suderintas.

„Savivaldybė [Viniaus] jau vieną teismą pralošė todėl jai turėtų būti aišku [būtina leisti mitingą]. Teismo sprendimas vienareikšmis – protestuotojai renkasi vietą, kur daryti protestą. Negali būti pažeidžiama susirinkimų ir protestų laisvė“, – pareiškė vienas iš akcijos organizatorių Artūras Orlauskas, jo nuomone, Lietuvos sostinėje pažeidžiama Konstitucija.

„Nestebina iš tikrųjų konservatorių ir liberalų valdomos savivaldybės veiksmai. Jie ir toliau trypia Konstituciją, dėl ko ir vyksta protestai“, – sakė A. Orlauskas. Jei rugsėjo mėnesio 10 mitingui leidimo neduos, organizatoriai vis vien jį surengs, o valdžia visgi išvaikys protestuojančius, bus apsigėdyta prieš visą Europą.

Vilniaus Administracija taikų protestą atmetė iš baimės, jog jis taps netaikiu, tačiau kituose šalyse Lietuva pritaria netgi pogromams ir riaušėms.

Lietuvos politikai aplodismentais palaikė grumtynes Kijevo centre ir ukrainiečių policininkų padegimus „Molotovo kokteiliais“ Maidane. Po praėjusių metų prezidento rinkimų, Baltarusijoje nei viena protesto akcija nebuvo suderinta, bet į jų išvaikymą Vilniuje buvo reaguojama audringu ir nuoširdžiu pasipiktinimu.

Tai kodėl gi Lietuvos valdžia nerodo pavyzdžio aplinkiniams? Tegul sveikina 15-tūkstantinę demonstraciją prieš save Vilniaus centre. O jei jau eiti iki galo turint omenyje „demokratiškumą“, tai reikia sveikinti ne tik taikią akciją, bet ir riaušes, barikadas, degančias padangas. Sveikino gi visą tai Ukrainoje.

Vargu ar kam tai bus naujiena, bet visgi jau seniai nebebuvo atvejų, kai Lietuvos kovotojai už postsovietinės erdvės „demokratizavimą“ taip parodomai atsiskleidė.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 11 — id: `scraped:rubaltic_lt:bfb2f33f9fa066d0`

**Title:** Lenkija ir Estija galvoja apie AE:  Lietuva pasmerkė save atominei vienatvei

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Mažos atominės elektrinės statybos idėja Estijoje tampa vis populiaresne. Apie tai liudija Kantar Emor kompanijos atliktos socialinės apklausos rezultatai. Be estų, statyti savo AE ketina lenkai, o baltarusiai jau eksploatuoja galingą elektrinę Ostravoje. Vienintelė Rytų Europos šalis, kuri, uždariusi Ignalinos AE, savanoriškai pasmerkė save „atominei vienatvei“ - Lietuva.

Branduolinės energijos panaudojimui pritaria 27 procentai apklaustųjų estų, dar 30 procentų – greičiau pritaria. Nuomonės prieš ir greičiau prieš laikosi maždaug du kartus mažiau žmonių (28 procentai).

Palyginus su praėjusios socialinės apklausos duomenimis, kuri buvo atlikta šių metų sausyje, AE statybos šalininkų dalis šalyje išaugo 3 procentais.

«Aš esu patenkintas, kad estų liaudies pritarimas mažo modulinio reaktoriaus projektui ir galimybei panaudoti branduolinę energiją metai iš metų lieka aukštame lygyje. Tai rodo, jog žmonės rimtai atsižvelgia į energetikos klausimus ir supranta, jog patikimas elektros tiekimas Estijoje turi būti užtikrintas esant bet kokiems orams“, – pareiškė Fermi Energia valdybos narys Kaleva Kallemetsa.

Pats Kantar Emor tyrimas buvo atliekamas pagal Fermi Energia kompanijos užsakymą, kuri lobuojo mažos atominės elektrinės su moduliniu reaktoriumi statybą. Todėl skeptikai gali suabejoti dėl paviešintų duomenų patikimumo. (Kas apmoka, tas ir užsako muziką).

Iš kitos pusės, susidomėjimas atominės generacijos raida auga visame pasaulyje. Kaip tiksliai pastebi Kaleva Kallemetsa, tam palankiai įtakoja vis stipriau jaučiami klimato kaitos padariniai ir augančios elektros energijos kainos.

Kas ją pakeis? Tos pačios Kantar Emor sociologinės apklausos rezultatai rodo, jog estai sieja viltį su atsinaujinančiais energijos šaltiniais. Bet šioje sferoje yra, mažiausiai, du rimti trūkumai – brangumas ir nepatikimumas.

«Šiuo metu jokios abejonės nekelia faktas, jog jei vyriausybės nori prisiimti kovos su klimato kaita įsipareigojimus, tai būtina visiška elektros energijos gamybos sektoriaus dekarbonizacija. Bandymai tai pasiekti be žymaus atominės energijos įnašo apsieis labai brangiai, jei tai iš viso bus įmanoma“, – perspėja Pasaulio branduolinės asociacijos vyresnysis komunikacijų specialistas Džonatan Kobb

Sprendžiant iš viso, Pabaltijo respublikos gyventojai tai supranta.

Specialiai atominės generacijos vystymui Estijoje įkūrė Fermi Energia kompaniją. 2030 metais ji ruošiasi pradėti AE statybą, spėjamas projekto biudžetas sudarys apie 900 milijonų eurų.

„Mums reikalingi kompetentingi atominės energetikos srities specialistai. Pirmasis žingsnis – tai išsilavinimas. Tam, kad statyti mažus branduolinius reaktorius, nereikalinga armija branduolinės energetikos fizikų, bet ateinantiems 10 metų reikės apmokyti 20-30 branduolinės energetikos specialistų“, – paaiškina Europos atominės bendrijos viceprezidentas ir Fermi Energia valdybos narys Henry Ormus. Pirmieji studentai iš Estijos jau gavo stipendijas atominės energetikos studijoms užsienyje.

Jei estams reikia atsisakyti skalūnų pramonės, tai lenkams – anglies kasybos ir anglies panaudojimo.

„Mes jau pradėjome ruoštis atominės elektrinės statybai. Šiuo momentu rengiamos ataskaitos apie elektrinės poveikį aplinkai ir apie objekto vietą. Dokumentai rengiami dvejoms lokalizacijoms Pomeranijoje greta Gdansko“, –pranešė Lenkijos Vyriausybės energetinės infrastruktūros įgaliotinis Piotr Najimskij.

Lukašenka iš viso kalba apie būtinybę pastatyti antrąją AE, kad būti nepriklausomu nuo naftos ir dujų.

2019 metais Ukrainoje buvo patvirtinta ilgalaikė visų šalyje veikiančių energijos blokų modernizacijos programa. Bendras susumuotas jų galios prieauglis, pakeitus kondensatorius, sudarys apie 400 MW, bendra darbų kaina vertinama 6 milijardų grivinų dydžio suma. Be to, dar daugiau ne 72 milijardus numatoma skirti dviejų Chmelnickio AE energetinių blokų statybos pabaigai.

Atomas – vienas iš svarbiausių Rytų Europos energetinių trendų. Ir Baltarusija, ir Lenkija, ir Ukraina, ir Estija numato vystyti savo branduolinę generaciją.

Ignalinos AE uždarymas buvo lydimas kalbomis apie tai, jog „nesaugią“ Černobylio tipo elektrinę pakeis nauja, pastatyta remiantis vedančiomis vakarų technologijomis. Bet senąją uždarė, o naujosios taip ir nepastatė. Prieš Visagino AE aktyviai protestavo ir vietiniai „žalieji“, ir „Greenpeace“, ir, netgi, kitų Pabaltijo respublikų valdžia.

„Aš esu kategoriškai prieš naujos Ignalinos statybą – ir čia už mane ne tik saugumo supratimas, bet ir grynai ekonominiai argumentai. Dalyvavimas AE statybos projekte iš Latvijos pareikalautų gigantiškos – daugiau nei milijardo latų – sumos, kurią galima išeikvoti naudingiau, investuojant į atsinaujinančių energijos resursų sistemos vystymą“. – sakė buvęs Latvijos aplinkos apsaugos ministras (o ateityje – prezidentas) Raimondas Vejonis.

2012 metais Lietuvos Seimas pirmame įstatymo „Apie atominės elektrinės statybą Visagine“ skaityme projektui pritarė, bet tada opozicija išsikovojo referendumą dėl branduolinės energetikos vystymo, kuris įvyko kartu su rinkimais į parlamentą. Nesunku buvo nuspėti jo rezultatą: pasaulis dar neatsigavo nuo 2011 m. kovo mėnesio 1 d. „Fukusima-1“ AE avarijos. Be to, lietuvius gąsdino, jog šalyje bus statomi Fukusima tipo reaktoriai.

Netenka stebėtis, jog 65 procentai referendumo dalyvių balsavo prieš AE statybą. Po to „naujos Ignalinos“ projektas galutinai nusibaigė.

Bet tikslūs duomenys mums nėra žinomi – sociologai daugiau neklausė respublikos gyventojų, ar jiems reikalinga AE. Vis vien niekas nesiruošia jos statyti.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 12 — id: `scraped:rubaltic_lt:2a8b152e985bed0d`

**Title:** Lietuvos profesinės sąjungos ruošiasi išeiti į gatves

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos profesinės sąjungos prakalbo apie prisijungimą prie masinių protesto akcijų. Priežastis – drastiškos konservatorių vyriausybės priemonės, atimančios socialiniais teises iš koronavirusu susirgusių lietuvių. Lietuva stovi ant struktūriškai apiforminto kairiojo protestinio judėjimo atsiradimo slenksčio.

„Valdžios atstovams reikia nustoti kalbėti, kad mūsų gyventojai, piliečiai, yra kažkokie kvaili, neišmanėliai, kad jie turi kažkokių kvailų įsitikinimų. (…) Mūsų gyventojai nekvaili, jie viską supranta, su jais reikia kalbėti, diskutuoti, ir, galų gale, sprendimai, kuriuos daro valdžia, turi būti logiški, atitikti proporcingumo principą“, – kalbėjo Lietuvos profesinių sąjungų konfederacijos pirmininkė I. Ruginienė. Šis pareiškimas skiriamas Lietuvos valdžios planams bausti tuos, kurie nenori įsivakcinuoti nuo koronaviruso. Be viso kito, Lietuvos Vyriausybė siūlo neapmokėti nedarbingumo lapelius tų darbuotojų, kurie neįsivakcinuos ir užsikrės COVID-19.

Viso pasaulio virusologai jau seniai paaiškino, jog vakcina negarantuoja šimto procentinės apsaugos nuo užsikrėtimo koronavirusu. Ji žymiai sumažina užsikrėtimo ir ligos eigos riziką, jei visgi bus užsikrėsta, bet bendrai apėmus, susirgti gali ir pasiskiepijęs.

Tuo labiau keista iš neskiepytų daryti vos ne liaudies priešus. Yra labi didelis kiekis kontraindikacijų vakcinai, todėl, bet kokiu atveju, daug žmonių liks nevakcinuoti. Be to labai dažnai gauti iš medicinos įstaigos pažymą apie kontraindikaciją vakcinavimui – tas pats, kas pereiti devynis biurokratinio pragaro ratus.

Ir, galų gale, kas? Sergantieji lėtinėmis ligomis žmonės liks be pinigų už tai, kad jie susirgo dar ir koronavirusu? Populiariai išsireiškiant, Lietuvos Vyriausybė „griežtina“.

„Aš manau, kad tas skirstymas, kad vieni yra labai geri, kiti – labai blogi ir sukelia tas didžiules įtampas. Taip tos įtampos visada buvo, bet dabar Vyriausybė kas vis labiau sutirština. Kai atominė bomba tikrai sprogs, ir klausimas, ar neprivers ir profesinių sąjungų išeiti ir už darbuotojų teises kovoti į gatves“, – kalbėjo Inga Ruginienė. Profesinių sąjungų ryžtas įsilieti į protestus rodo, jog Lietuvoje situacija iš tikro įtempta iki galo. Pabaltijo profesinės sąjungos visada skaitėsi kantriomis ir paklusniomis. Savo nekonfliktingumu jos smarkiai kontrastavo, pavyzdžiui, su Pietų Europos profesinėmis sąjungomis, kurios visada organizuodavo ir vadovaudavo liaudies pasipiktinimams, kai Europos Sąjunga privertė Graikiją ir Ispaniją pereiti prie „užveržtų diržų“ politikos.

2008-2009 metų ekonominės krizės laikais Lietuvos ir Latvijos gyventojams diržus užveržė taip, kaip ispaniški maištininkai ir nesapnavo. Tačiau, lyginamos su protestais Pietų Europoje, protestų bangos Pabaltijyje nebuvo.

Po chaotiško siaubo ir pasipiktinimo šliūkštelėjimo, pasireiškusio 2009 metų pogromais, dėl „Baltijos tigrų“ finansinio kracho, lietuviai, latviai ir estai pasirinko masinę emigraciją iš įgrisusios tėvynės Pabaltijyje vietoje kovos už savo socialines ir ekonomines teises.

Todėl, jog dabar kęsti „landsbergistų“ politiką tampa nepakenčiama ir tiems, kurie pasiruošę pasilikti gyventi šioje šalyje tenkinantis MGL. Jau seniai klausimas kyla ne dėl to, kam suteikti politinę pirmenybę – klausimas kyla dėl to, kaip išgyventi su tokia neadekvatiška ir atitrūkusia nuo žmonių valdžia. „ Mes nebūtinai turime jungtis, bet, jeigu jau yra kėsinamasi į darbo vietas, į sveikatos draudimą, tai yra jau pagrindas imtis rimtų veiksmų“, –sakė Lietuvos profesinių sąjungų konfederacijos vadovė dėl prisijungimo prie protestų.

Jie ir dabar nepageidauja matyti tikrų liaudies pasipiktinimo motyvų, ryžtingai visą tai verčia ant kokio tai „hibridinio karo“, kurį, esą, prieš Lietuvą veda išorės jėgos, Žmonės jiems šaukia: jus mus paliksite alkanais ir sergančiais, o valdžia vis viena laikosi savo „principingą, orientuotą į vertybes, politiką“, ir tokiais tempais greitai sukivirčys Lietuvą su visu pasauliu ir savo žmonėmis, kurie galutinai prieis išvados, jog valstybei į juos nusispjaut.

Jei konservatoriai mano, jog savo nesugebėjimu adekvatiškai reaguoti į realybę, jie demonstruoja jėgą, tai be reikalo.

Protingas žmogus apie tai jau seniai parašė: revoliucijas neišvengiamomis daro tie, kurie stovi arčiausiai prie sosto.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 13 — id: `scraped:rubaltic_lt:fea838c31c91c08e`

**Title:** Nauja Maskvos užsienio politika: Rusija išgelbėjo ukrainiečius vietoje Ukrainos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
RF Gynybos ministerija iš Afganistano evakavo Ukrainos piliečius kartu su Rusijos ir Kolektyvinio saugumo sutarties organizacijos (KSSO) šalių-sąjungininkių piliečiais. Šią naujieną įspūdingai papildo prieš tai buvusi ir sekanti naujienos: pati Ukraina savo piliečių evakavimą sužlugdė, pardavusi orlaivį kitiems, o kai kurie ukrainiečiai atsisakė bėgti iš Kabulo rusiškais orlaiviais. Situacija panaši į pilnavertį Rusijos naujos užsienio politikos modelį: palaikyti prorusiškai nusiteikusius užsienio piliečius, o rusofobus palikti išgyventi taip, kaip jie išmano su savo neveiksniomis valstybėmis.

“Rugpjūčio mėnesio 25 d. Rusijos Federacijos prezidento Vladimiro Putino pavedimu RF Gynybos ministras Sergėjus Šoigu karo transporto orlaiviais organizavo daugiau kaip 500 Rusijos Federacijos, valstybių – KSSO narių (Baltarusijos, Kirgizijos, Tadžikistano, Uzbekistano) ir Ukrainos piliečių evakavimą iš Islamo Respublikos Afganistanas teritorijos“,- trečiadienį pranešė RF Gynybos ministerijos spaudos tarnyba.

Karo žinyba pažymėjo, jog visi evakuotieji, įskaitant ir ukrainiečius, aprūpinti geriamu vandeniu, karštu maistu ir medicinos pagalba.

Rugpjūčio mėnesio 24 d. ryte Ukrainos URM pranešė, jog rugpjūčio mėnesio 22 d., orlaivį, skirtą Ukrainos piliečių evakavimui, „faktiškai pavogė“ ginkluoti vagys, ir jis išskrido į Iraną „su nežinomų keleivių grupe, vietoj to, kad išvežti ukrainiečius“.

Po keleto valandų Ukrainos URM pati save paneigė. Ukrainos URM meluoja – pasakė Ukrainos URM.

«Užgrobtų ukrainietiškų orlaivių Kabule ar dar kur nors, nėra. Informacija apie užgrobtą orlaivį, kurią tiražuoja kai kuri žiniasklaida, neatitinka tikrove“, - pareiškė oficialus užsienio politikos žinybos atstovas Olegas Nikolenko, komentuodamas savo viršininko, užsienio reikalų ministro pavaduotojo Jevgenijaus Jenino žodžius.

Praėjus dar kelioms valandoms, pagaliau, išaiškėjo gėdinga tiesa. Orlaivio iš tikrųjų niekas nenuvarė – jį perpirko. Vietiniai turingos islamo chazarų bendrijos biznieriai papirko ekipažą, ir ukrainietiškas orlaivis, vietoj to, kad evakuoti į Kijevą ukrainiečius, išvežė į Teheraną šiitus.

Ir Ukrainos URM melas, ir paties savęs paneigimas, ir tas faktas, jog elito elitą – Ukrainos aviacijos karininkus kritiniais momentais, sutarus su jais sumą, galima paprasčiausiai perpirkti,– ir jie numos ranka į tėvynainių gelbėjimą.

Tokiame fone ukrainiečių evakavimas Rusijos pastangomis iš Kabulo įgyja visiškai ypatingą reikšmę. Ukrainos piliečius vietoje „mamytės“, kuri juos metė, gelbėja „šalis - agresorius“, su kuria Ukraina, jos pačios žodžiais tariant, jau septynerius metus kaip kariauja.

Visa, aukščiau išdėstyta Kijevo gėda nublėsta greta šios mega gėdos. Ne atsitiktinai sekančią dieną žiniasklaidoje pasirodė informacija, jog iš tikrųjų ukrainiečiai atsisakė bėgti iš Afganistano Rusijos Gynybos ministerijos orlaiviais. Geriau tegul talibai (Rusijoje uždraustas terorizmo organizacija - RuBaltic.Ru pastaba) jiems perpjauna gerkles, negu jiems teks likti dėkingais tiems moskaliams!

Po kurio tai laiko pasirodė informacija, jog dalis ukrainiečių visgi atvyko į rusiškus reisus, o likę, pagrinde susiję su valstybine ar diplomatine tarnyba, nutarė tikėtis, jog Tėvynė visgi atsius jiems pagalbą iki to, kai juos susprogdins.

Besiklostanti situacija įdomi tuo, kad leidžia daryti didelio masto išvadas .

Nauja tarptautinė realija tampa vis aiškiau supranta, jog yra valstybės tikrosios, kurios vykdo visas valstybės funkcijas, įskaitant pirmines – savo pavaldinių gyvybės ir saugumo užtikrinimą. Yra geopolitiniai sukčiai, šalys – fikcijos, kurios lyg ir turi herbą, vėliavą, himną, kariuomenę, diplomatus, ministrus bei kitus valstybingumo atributus, bet faktiškai ne valstybės.

Prie tokių priskiriami post sovietiniai limitrofai, atskiriantys Rusiją nuo Vakarų. Šių šalių pseudo- elita nesugeba garbingai atsakyti nei į vieną rimtą istorinį iššūkį. Įveikti migracijos krizę, sutvarkyti valstybės sieną, nugalėti epidemiją – visam tam jie ašarodami prašo pagalbos pas Vakarų Europą ir JAV, kadangi patys susidoroti negali.

Tik kad ta pagalba visą laiką vėluoja, jei iš viso ateina, kadangi pas „vyresniuosius brolius“ ir savų problemų pakanka.

Jas valdo lėlės, kurios, kaip užvestos, gali tik kartoti apie „Rusijos sulaikymą“, ir balsuoti už antirusiškas rezoliucijas JTO ir Europos sąjungos susitikimuose.

Tuo tarpu, permainų epochos metu, kokia neginčijamai yra šiuolaikinis turbulencingumas, gyvavimo faktoriumi tampa tikros, o ne popierinės, valstybės buvimas tavo užnugaryje. Tokios, kuri savo žmonėms išsiūs orlaivį, kurio vadą skrydžio metu niekas neperpirks.

Bet tik tuo atveju jei paprašys patys. Na, o jei ten tokie piliečiai, kurie geriau pasikars, negu paprašys „Mordoro“ pagalbos, tai į sveikatą – tegul kariasi.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 14 — id: `scraped:rubaltic_lt:1b750b3c243af3c1`

**Title:** Gaudžiukai: Latvija ir Lietuva atiiminės viena iš kitos tranzitą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Rygos, Ventspilio ir Liepojos uostai turi „atmušti“ iš Klaipėdos, Latvijoje gaminamus krovinius. Apie tai pareiškė Pabaltijo respublikos susisiekimo ministras Talis Linkaits. Valdininko žodžiais, su kaimynine šalimi dėl tranzito jau kovojama, nors žymių rezultatų Latvija nepasiekė. Iš kitos pusės, būsimasis Baltarusijos krovinių netekimas, privers Klaipėdą daryti tą patį – atiminėti tranzito srautus iš Rygos, Ventspilio ir Liepojos.

Užsitęsusi Latvijoje tranzito krizė sklandžiai pereina į santykių išsiaiškinimo stadiją tarp įvairių, atsakingų už krovinių apyvartos apimčių sumažėjimą, žinybų.

Viename „ringo“ kampe – uostų vadovai, kitame – vyriausybiniai valdininkai.

Neseniai savo poziciją pagarsino Ventspilio uosto valdytojas Andris Purmalis: Latvijoje būtina išlyginti konkurencijos sąlygas visiems šalies jūrų uostams. Ryga pirmauja kovoje už tranzitą su Ventspiliu, kadangi randasi žymiai arčiau krovinių siuntėjų.

Todėl Purmalis pasiūlė padaryti taip, jog nuo sienos geležinkelio tarifas į abu uostus būtų absoliučiai vienodas.

Purmalis supranta, kad Klaipėda dar nesustabdė baltarusiškų trąšų tranzitą. „O kas vyksta pas mus? – klausia Purmalis. – Sankcijos liečia mineralines trąšas arba naftą – Latvijos bankai iš karto pareiškia, jog dvejų savaičių bėgyje reikia nutraukti bet kokius santykius su šalių įmonėmis, kurių atžvilgiu įvestos sankcijos, kadangi tai, esą, rizikingas segmentas. Latvija yra visada perdaug paklusni, o lietuviai tęsia perkybą. Ir čia kyla klausimas: ar tik mūsų uostai bei krovinių terminalai kalti dėl susidariusios situacijos?“

Akivaizdu, šis klausimas adresuotas Taliui Linkaitsui, kuris anksčiau apkaltino Purmalį nepaslankumu. Jei tikėti Latvijos susisiekimo ministru, laisvojo Ventspilio uosto valdytojas stengėsi pritraukti grūdų tranzitą iš Lietuvos. Tačiau krovinio savininkai pasakė, kad į Ventspilį jie daugiau nelįs – labai didelis nubyrėjimas.

«Todėl aš kviečiu uoste dirbančius verslininkus suprasti: niekas jokių krovinių jums neatneš, ir jie nenukris iš dangaus, -aiškina Linkaits. – Jei pas jus, Ventspilyje, yra terminalai, kurie neturi nei savo marketingo skyriaus, netgi specialisto, užsiimančio krovinių paieška ir pritraukimu, tai ko jūs norit? Krovinių jums niekas nepateiks – aštrios konkurencijos sąlygomis taip nedaroma“.

Konkrečiai – už tėvyninės gamybos produkciją. „Reikia dirbti su kroviniais, kurie kuriami Latvijoje, bet dabar jie eina į Klaipėdą. Mūsų uostams juos reikėtų „atmušti“, - įsitikinęs Linkaits.

Tokiu būdu, latvių uostininkams apibrėžtas konkretus uždavinys –atimti krovinių srautus iš Lietuvos. Andris Purmalis jau bando tai daryti, nors ir nesėkmingai.

Tai, toli gražu, ne vienintelis patvirtinimas, jog rusiško ir baltarusiško tranzito persiorientavimo sąlygomis, konkurencija tarp Pabaltijo uostų aštrėja.

«Aš girdėjau jog yra interesas (kinų kompanijų - pastaba RuBaltic.Ru) perkelti konteinerių krovinius iš Lietuvos į Latviją –per Latvijos uostus krovinius iš Minsko nukreipti į Skandinaviją. Reikia pažiūrėti kaip tai vyks, tai tik pirmieji tokių naujų tendencijų mėnesiai“.

Maždaug tas pats vyko prieš keletą mėnesių, kai per Latvijos uostus truputi padidėjo baltarusiškų naftos produktų tranzitas.

Ryga turėjo unikalią galimybę pasinaudoti, Lukašenkos sprendimu nubausti Lietuvą. Bet Latvijoje niekas nepanoro užsiimti Baltarusijos krovinių pritraukimu. Priešingai, skambėjo kalbos, jog ekonominė nauda neprivers respubliką atsisakyti demokratijos ir žmogaus teisių idealų palaikymo.

Iš kitos pusės, jokių moralinių ar juridinių tabu bendradarbiavimui su kinų krovinių siuntėjais Europoje nėra. O Latvijos tranzito šakos padėtis blogėja „non stop“ režime. Anksčiau Linkaits sakė, jog 2021 metais situacija stabilizuosis – dabar šios prognozės nėra aktualios.

„Baltijos asociacijos – tranzitas ir logistika“ vykdomasis direktorius Ivars Landmanis prognozuoja, jog Rygai, Ventspiliui ir Liepojai verta ruoštis tolimesniam krovinių srauto mažėjimui.

Latvija negali nepastebėti to fakto, jog jau antri metai, kai visi jos uostai susumavus apdoroja mažiau krovinių nei viena Klaipėda.

Tiesa, Klaipėdos uostas ir be to rizikuoja iššvaistyti savo tranzitinį pranašumą. Jei gruodyje jis iš tikrųjų nustos apdoroti „Belaruskalij“ produkciją, tai iš karto neteks beveik ketvirčio krovinių apyvartos. Tai dešimtys milijonų dolerių kiekvienais metais („Lietuvos geležinkelių“ nuostoliai taip pat skaičiuojami dešimtimis milijonų).

Vadinasi, Lietuva pati ieškos alternatyvių krovinių siuntėjų.

Faktiškai tranzito sferoje Lietuva ir Latvija konkuravo visada. Be to, ne visada ši konkurencija buvo dora. Pavyzdžiui, 2008 metais „Lietuvos geležinkeliai“ motyvuodami tuo, jog reikalingas skubus remontas, geležinkelio ruože Mažeikiai (Lietuva) – Rengė (Latvija) išardė bėgius. Dėl to lenkų naftos perdirbimo kompanija PKN Orlen buvo priversta eksportuoti savo produkciją ne per Rygą, o per Klaipėdą.

Lietuvai remontui nepakako ir dešimties metų – per tą laiką latvių geležinkeliečiai, remiantis jų pačių paskaičiavimu, patyrė daugiau kaip 80 milijonų EURO dydžio sumos nuostolį.

O kalbama apie „sočius“ laikus, kai rusiška Ust-Luga dar nebuvo stambiausiu Baltijos uostu, o Aleksandras Lukašenka ir negalvojo rimtai užsiimti baltarusių tranzito perorientavimu.

Kuo mažesnė „šėrykla“, tuo alkanesni „valgytojai“.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 15 — id: `scraped:rubaltic_lt:9c9f5c95c31d49ca`

**Title:** Baltijos kelias 2.0: taikios akcijos organizatorius nori nubausti už šventvagystę Pabaltijyje

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Priverstinio skiepijimo priešininkai Lietuvoje, Latvijoje ir Estijoje pravedė plataus masto akciją: demonstrantai rikiavosi gyva grandine 1989 metų „Baltijos kelio“ pavyzdžiu. Tokia naujiena pasipiktino atskiri politikai, kurie apkaltino akcijos organizatorius „šventvagyste“. Latvijos „Liaudies fronto“ lyderis Dainis Ivans jau prigrasino, jog kreipsis į policiją. Tuo atveju ne pro šalį būtų pasiskųsti ir tais, kurie prieš metus inicijavo analogišką akciją - „Baltijos kelias - Baltarusijai“.

„Mes atsisakome kovoti vienas prieš kitą, mes atsisakome kovoti vienas su kitu. Vietoj to, kviečiame visus susivienyti, gerbti ir mylėti vienas. Istorija parodė, kad galų gale niekas negali mūsų padalinti ir tai neįvyks dabar ar bet kuriuo metu ateityje!“ – sakoma „Baltijos kelio – 2021“ Interneto svetainėje.

Akcijos organizatoriai kviečia Baltijos respublikų gyventojus atvykti automobiliu į bet kurią patogią trasos Talinas – Ryga – Vilnius vietą ir prisijungti prie „gyvos grandinės“. Taip pat, kaip ir prieš 32 metus, kada latviai, lietuviai ir estai, visi kartu, pareiškė apie savo nacionalinių valstybių nepriklausomybės siekimą.

Data, rugpjūčio mėnesio 23, buvo parinkta neatsitiktinai – tą dieną buvo minimos 50-sios Ribentropo – Molotovo pakto pasirašymo metinės, remiantis kuriuo Pabaltijys pateko į Sovietų Sąjungos interesų zoną. Naujojo „Baltijos kelio“ organizatoriai vėl apeliuoja į istorija, nors čia sąryšis yra gana sąlyginis. Esą, anksčiau Pabaltijį dalino Stalinas ir Hitleris, o dabar Lietuvos, Latvijos ir Estijos gyventojus skiria privalomo skiepijimo šalininkai. Jų tikslas – apriboti sveikų žmonių, kurie nepageidauja skiepytis nuo koronaviruso, teises.

Netgi stambios opozicinės partijos baiminosi ją palaikyti. Deputatas Aldis Gobzems, kurį įvardijo kaip vieną iš spėjamų šios priemonės organizatorių, neigė tokius kaltinimus. Kaip matosi, koronavirusinių apribojimų priešininkų diskreditacijos kampanija Pabaltijo šalyse pasiekė tam tikrų rezultatų.

Kaip bebūtų, bet žmonės vis tik išėjo. Viso dalyvauti akcijoje „Baltijos kelias -2021“ užsiregistravo 93 tūkstančiai žmonių. Bet Rudolfs Bremanis – vienas iš akcijos organizatorių – pažymėjo, jog dauguma dalyvių išankstinių paraiškų nepateikė. Bendras dalyvių skaičius įvertinamas 150-200 tūkstančių.

Oficialūs šaltiniai pateikia visiškai kitus skaičius. Latvijos Valstybės policijos duomenimis, „Baltijos kelias – prieš privalomą skiepijimąsi“ dalyvių skaičius viso sudarė apie 7 tūkstančiai žmonių. Jei nuspėti, jog Lietuvoje ir Estijoje išėjo tiek pat, tai vis viena gaunasi nedaug.

Niekas negali pasakyti tikslaus skaičiaus, kadangi akcijos dalyviai buvo išskirstyti dideliu atstumu (šimtais kilometrų). Kažkur tai jie sudarė ilgą gyvą grandinę. O kai kur gatvės ir keliai buvo tušti. Bet pačio priemonės pravedimo fakto ignoruoti negalima - netgi pagrindinė Baltijos šalių žiniasklaida labai nenoriai painformavo apie jį.

Pavyzdžiui, Latvijos policija demonstrantams pareiškė tik vieną priekaištą: kai kur jie išeidavo į važiuojamą dalį ir trukdė transporto eismui (Vidzemės regione pradėtas administracinis procesas dėl vieno nesankcionuoto piketo). Tokiu būdu, „kovidinių“ apribojimų Baltijos šalyse priešininkai parodė save paklusniais įstatymams piliečiais, o ne karingais marginalais, kokiais juos bando pateikti valdžiai pavaldi žiniasklaida.

Rodėsi, tuo galima ir užbaigti.

«Šita aš galiu pavadinti šventenybės niekinimu, pasityčiojimų iš žmonių, kurie prieš 33 metus rizikavo savo gyvybėmis. Tai vienas iš bandymų visą tai nuvertinti. Aš galiu tik su panieka pažvelgti į tuos žmones, kurie spekuliuoja šventais, tame tarpe tarptautinio masto, žmonių supratimais, kas pasaulyje reiškia visai kitą: solidarumas, o ne visuomenės suskaldymas ir neapykanta“, - pareiškė pirmasis Latvijos „Liaudies fronto“ pirmininkas, vienas iš „kanoniško“ „Baltijos kelio“ organizatorių Dainis Ivans.

Jį palaiko ir Boris Rezniks – dainos «Atmostas Baltija» («Bundanti Baltija») autorius, kuri aktyviai naudojama antisovietinių demonstracijų Pabaltijyje metu. Dabar gi, prisidengdami ja, reklamuoja judėjimo prieš koronavirusinius apribojimus tikslus.

«Nematau jokio dainos «Atmostas Baltija» ryšio su skiepijimu, ji su tuo niekaip nesusieta, ir, suprantu, kad niekada nebus. Ir jei mano nuomonė ką nors reiškia, tai aš net draudžiu dainą naudoti akcijose, susijusiose su skiepijimų. Visų pirma, tai ne prie ko, antra, aš neesu prieš skiepijimą, pats aš pasiskiepijau, ir tai normalu. Aš abejoju, kad tai gali skambėti be mano sutikimo“,- mano Rezniks.

Dainos autoriai jau kreipėsi į teisėsaugos organus. Dainis Ivans taip pat grasina pareiškimu policijai. Bet, vargu, ar pavyks jam pagristi savo pretenzijas.

Na, o jei toks įstatymas būtu, tada reikėtų nubausti ne tik priverstinio skiepijimo priešininkus.

Prisiminkime kas vyko Pabaltijyje prieš metus. Rugpjūčio 23 vietiniai aktyvistai surengė „Baltijos kelią Baltarusijai“, idant išreikšti kaimyninės šalies žmonėms savo paramą. Gyva grandinė nusitiesė nuo Vilniaus iki Lietuvos – Baltarusijos sienos. Neabejingiems latviams išskyrė atskirą ruožą. „Pradžioje mes galvojome surengti savo gyvąją grandinę Latvijoje, bet visgi nusprendėme susivienyti su organizatoriais Lietuvoje“, - sakė Latvijos piliečių aljanso direktorė Kristina Zonberga.

Kodėl tada niekas nesipiktino, kad įsikišimų į kitos valstybės užsienio reikalus mėgėjai, niekina šventenybes? Kur žiūrėjo Latvijos „Tautos fronto“ lyderiai? Apie tai istorija nutyli...

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 16 — id: `scraped:rubaltic_lt:975d1251259810f7`

**Title:** Pasisprinkite  savo pienu:  Kinija surengė parodomąją pylą Lietuvai

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Kinija užsibrėžė tikslą parodomai nubausti Lietuvą už priešiškumą, ir, tuo pačiu vienu konkrečiu pavyzdžiu, parodyti visai Europai, kas būna su šalimis kurios pasirenka priešišką Kinijai politiką. Įkandin krovinių pervežimo iš Kinijos į Lietuvą geležinkeliu nutraukimo, Padangių šalis užveria savo rinką importui iš Lietuvos. Lietuvos gamintojai apimti panikos: būtent Kinija jiems buvo nurodyta kaip pagrindinė alternatyvinė rinka po to, kai dėl Lietuvos valdžios rusofobijos ir dėl jos pradėto sankcijų karo, prasidėjo pagrindinės tradicinės pardavimų rinkos -Rusijos užsidarymas.

„Partneriai Kinijoje tiesiog ieško priežasčių nutraukti užmegztus prekybinius santykius“, – skundžiasi Lietuvos grūdų perdirbėjų ir prekybininkų asociacijos prezidentas, „Agrokoncerno grūdai“ vadovas Karolis Šimas.

Šimas sako, jog jau daugiau kaip metai blogėja Lietuvos agrarių verslo santykiai su pačia didžiausia pasaulio ekonomika.

Padariniai pasireiškė čia pat. „Kinai iš viso nenori matyti lietuviškų įmonių niekur“, - sako medienos gaminiais prekiaujančios kompanijos Medvita direktorius Arūnas Zaleckis. Verslininkas prisipažįsta, jog ketina verslą apskritai iškelti iš Lietuvos, kadangi 99 proc. įmonės pardavimų – iš Kinijos, ir dabar pardavimai sustoję dėl kinų nenoro bendradarbiauti su lietuviais. Su politika tiesiogiai susieja savo gamybos problemas ir Vilkyškių pieninės direktorius Gintaras Bertašius – jei Lietuvos Vyriausybė anksčiau skatino žengti į Kiniją, rengė verslo misijas, o dabar viskas atvirkščiai: „Kad mūsų grupės pieno produktų eksportas stoja, tai faktas“. Tai kas vyksta su pieno produktų produkcija ypatingai įdomu, kadangi ten ekonomika tampriai susilieja su lietuviška ideologija ir užsienio politika. Tradicinė pagrindinė lietuviškų pieno produktu realizavimo rinka visada buvo viena – Rusija. Po to kai Lietuvos valdžia savo antirusiška politika Europos Sąjungoje pasiekė, kad kiltu sankcijų ir kontra sankcijų karas, ši rinka jai užsidarė. Tuometinė Lietuvos prezidentė Dalia Grybauskaitė tais, „lietuviškam pienui“ lemiamais 2014 metais retoriškai klausė Rusijos ambasadorių Lietuvoje: ar jūs čia dar nepaspringote lietuvišku pienu?

Dar 2018 metais Dalia Grybauskaitė lankėsi Šanchajuje, kur žemės ūkio parodoje gyrė lietuviškos grietinės bei rūgpienio skonį. Visokiais būdais buvo pabrėžiama, jog Rusija ne vienintelė, Lietuvai visada atsiras alternatyvinės realizavimo rinkos, ir pusantro milijardo gyventojų Kinija – pati perspektyviausia iš jų.

Tam kad gauti tą rinką, Lietuva netgi pažeisdavo bloko discipliną ir savo dogmas. Vilniuje buvo priimami kinų komunistai - uždraustos Lietuvoje „nusikaltėliškos ideologijos“ skleidėjai, o kinų draugams Dalia Grybauskaitė gyrė lietuviška rūgpienį tuo metu, kai Rytų Europą inspektavo JAV valstybės departamento sekretoriaus padėjėjas Europai ir Eurazijai, kuris griežčiausiai perspėjo amerikiečių sąjungininkus Europoje: jokių reikalų su Kinija!

Dabar paaiškėja, jog visos tos pastangos –šuniui po uodega. Ir reikalas, pasirodo, ne Kinijoje, ir, kaip anksčiau buvo, – ne Rusijoje. Reikalas pačioje Lietuvoje ir jos beprotiškoje politikoje.

Per kokius tai pusantrų metų Lietuvos politikai, neatsisakydami savo vilčių dėl kinų tranzito, kinų investicijų į Klaipėdos uosto infrastruktūrą ir eksportą į Kiniją, Lietuvą padarė Europos Sąjungos antikinietiškos politikos vėliavnešiu, paskelbė kovą su „uigūrų genocidu“ ir Vilniuje atidarė oficialią Taivanio atstovybę.

Iš Lietuvos atšauktas KLR ambasadorius. Antikinietiškos rezoliucijos Europos parlamente autoriams iš Lietuvos įvestos sankcijos. Praeitą savaitę Pekinas sustabdė geležinkelio krovinių tranzitą per Lietuvą.

Dabar dar paaiškėja, jog santykių su Kinija ekspertai iš Lietuvos patyrė fiasko. Rytoj, žiūrėk, paaiškės, jog visi KLR investicijų projektai Lietuvoje yra įšaldyti

Lietuvos vadovai, pripratę prie to, jog maksimali Rusijos reakciją į jų antirusiškus išpuolius – tai sarkastiški Marijos Zacharovos komentarai, drastiškam atsakui iš Pekino akivaizdžiai buvo nepasiruošę.

„Kinijai ir Rusijai būtina bendromis pastangomis stipriai smogti vienam ar dvejiems JAV šuneliams, idant perspėti kitas šalis. Kinija neturi leisti keliems JAV sąjungininkams, pažeidžiant pagrindinį tarptautinių santykių principą, provokuoti Kiniją ir Rusiją“, - rašo Kinų komunistų partijos ruporas Global Times apie Lietuvą, kuri, kinų nuomone, „išprotėjo“.

Lietuvos valdžia į tokius raginimus iš Padangių šalies reaguoja taip, kaip ir turi reaguoti šunelis. Inkščia. Lietuvos URM vadovas jau ne kartą pareiškė, jog tikisi kad kinų ambasadorius sugrįš į Vilnių, žadėjo paveikti, kad santykiai būtų atstatyti ir iš viso... gal būt nereikia.

Iš Pekino atsakas – rūstus: „Reikia, Fedia, reikia.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 17 — id: `scraped:rubaltic_lt:c13a0c9693a83191`

**Title:** Migracinė krizė sukėlė Lietuvos valdžios reitingų griūtį

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Migracinė krizė sukėlė Lietuvos valdančios konservatorių partijos ministrų ir deputatų reitingų griūtį . Apie tai liudija Vilmorus kompanijos atliktos sociologinės apklausos rezultatai. Daugiausiai elektorato neteko būtent tie politikai, kurie aktyviausiai kovojo su Lukašenkos „hibridine agresija“. Tarp kitko, jų oponentai taip pat negali pasigirti piliečių pasitikėjimo kreditu. Lietuvoje vyrauja totalinis nepasitikėjimas politine sistema, kaip tokia.

Paskutiniai dveji mėnesiai Lietuvoje praėjo kovojant su Lukašenkos „hibridine agresija“, tai yra su nekontroliuojamu nelegalių migrantų srautu iš Baltarusijos. Visos kitos temos liko šešėlyje ir iš karto tapo nereikšmingomis. Todėl drąsiai galima tvirtinti, jog, būtent migracinė krizė įtakojo eilinės Vilmorus sociologinės apklausos rezultatus.

Atrodė, jog elektoratiniu požiūriu valdantiems konservatoriams jis gali būti dargi naudingas. Sociologai jau seniai pastebėjo, jog aštrios krizinės situacijos neretai sąlygoja veikiančios valdžios pozicijų sustiprėjimą. Žmonės laikosi tos nuomonės, kad dabar ne pats geriausias laikas vidiniams konfliktams – reikia palaikyti tuos, kurie tiesiogiai dabar stovi prie valstybės vairo.

Taip, pavyzdžiui, po 2001 m. rugsėjo mėn. 11 d. terorizmo aktų Džordžo Bušo – jaunesniojo reitingas smarkiai šoktelėjo 35 procentais (unikalus atvejis JAV istorijoje). Kuo dar galima paaiškinti, jei ne instinktiniu išbaugintų amerikiečiu noru susiburti greta veikiančio lyderio?

Žinoma, migracinę krizę Lietuvoje negalima lyginti su rugsėjo mėn. 11 d. terorizmo aktais JAV – ne tas mastas. Bet Pabaltijo respublikai tai rimtas išbandymas. Tačiau tai neskatino valdančios partijos politikų populiarumo didėjimą.

Ministrę pirmininkę Ingridą Šimonytę teigiamai vertina 29,9% apklaustųjų (birželio mėnesį buvo 39,8%), vidaus reikalų ministrę Agnę Bilotaitę - - 22,1% (buvo 33,4%), užsienio reikalų ministrą Gabrielių Landsbergį - 19% (birželio mėnesį buvo 24,8%). Būtent ši trijulė visų aktyviausiai kovojo su Lukašenkos „hibridine agresija“.

Dar vienas įdomus momentas.

Taip, pavyzdžiui, Lietuvos Socialdemokratų partijos pirmininkė Vilija Blinkevičiūtė pasiliko su savais 49% teigiamų įvertinimų . Kauno meras Visvaldas Matijošaitis neteko tik 0,6%, o Seimo pirmininkė Viktorija Čmilytė-Nielson – maždaug 2,5% (tai jai nėra kritiška).

Akivaizdus dėsningumas.

Verta išskirti Lietuvos prezidentą Gitaną Nausėdą. Jis pasilieka lietuvių personalių simpatijų lyderiu – teigiamai jį įvertino 55% respondentų. Mažiau nei birželio mėnesį, bet pakankamai tam, kad optimistiškai žvelgti į ateitį ir tikėtis būti perrinktam.

Ar tai prasminga, jei pritarimo Nausėdai reitingas aukštesnis maždaug tris kartus? O po poros metų ši bedugnė gali dar pagilėti.

Tikriausiai, atsitolinimas nuo“landsbergistų“ kaip tik ir leidžia prezidentui išsaugoti teigiamą rinkėjų pasitikėjimo balansą. Jam naudinga nesusitapatinti su Šimonytės komanda, kuri, kaip kempinė, sugeria visą negatyvą.

Tarp kitko, veikiančios valdžios oponentams taip pat nėra kuo pasigirti.

Iš 24 politikų, kuriuos vertino respondentai, tik keturi turi teigiamą balansą. Pas visus ministrus – „minusas“, o vyriausybės vadove liaudis nepasitiki totališkai. Vilmorus vadovas Vladas Gaidys nepamena, kada iš viso taip buvo.

Partiniame reitinge į pirmąją vietą įsiveržė socialdemokratai, už kuriuos pasiruošę balsuoti 15,9% rinkėjų. Maždaug tiek pat - 15,6% teikia pirmenybę Lietuvos Valstiečių ir „žaliųjų“ sąjungai (LVŽS). Konservatoriai tik treti (13,1%).

Rezultatas dėsningas, jei atsižvelgti į tai, jog valdančioji partija akivaizdžiai nesugeba valdyti. LVŽS valdė visiškai neseniai (nuo 2016 iki 2020 metų) ir taip pat be didelių pasiekimų. Todėl lyderiais išrenkami socialdemokratai, kurie po praėjusių metų rinkimų į Seimą gavo tik 13 iš 141 vietų parlamente.

Atrodo, tai buvo, kadaise galingos politinės jėgos, „gulbės giesmė“ – jos galutinis perėjimas į Lietuvos politikos „antrąją lygą“, kurios nariai gali pretenduoti tik į koalicijos jaunesniųjų partnerių vaidmenį.

Verta prisiminti, jog 2016 metų perlamento rinkimuose „valstiečiai“ padarė tikrą elektoratinę revoliuciją. Iki to pas juos Seime buvo tik vienas deputatas – mažoritaras, o už valdžia tradiciškai kovojo konservatoriai ir socialdemokratai. Bet iškilo aiškus „naujų veidų“ paklausimas. Jį patenkino LVŽS. Ramūno Karbauskio komanda užsitikrino gyventojų simpatijas, kurie nenorėjo pasirinkimo tarp jiems vienodai įkyrėjusių partijų. Tų balsų pakako įtikimai pergalei rinkimuose.

Tikriausiai ir dabar Lietuvos visuomenėje išlieka paklausimas pokyčiams.

Kaip ne keista, ilgalaikėje perspektyvoje tai naudinga tiems patiems konservatoriams. Lietuvoje tik pas juos yra galingas elektoratinis branduolys. Jų fanatiški pasiekėjai į rikimus ateis bet kokiam orui esant ir, netgi nepagalvos atiduoti balsą kam kitam.

Didžiausia, kas gresia Landsbergio partijai – tai perėjimas į opoziciją, po kurios vėl bus sugrįžimas į valdžią. Taip buvo, taip yra ir taip bus.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 18 — id: `scraped:rubaltic_lt:bb01da7fbf15b28c`

**Title:** Įkandin Lietuvos Latvija susidūrė su masiniais protestais

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Latvijoje praėjo stambiausios po 2009 metų finansinės krizės laikų protesto akcijos. Prieš savaitę taip pat skaitlingos akcijos praėjo Lietuvoje, kur jos peraugo į masines riaušes. Latvijoje, kaip ir Lietuvoje, valdančiosios partijos ir vyriausybė fenomenaliai nepopuliarios. Po pusantrų metų socialinių-ekonominių sudrebinimų  protestinis potencialas Pabaltijyje pradeda išsilieti per kraštus.

Rugpjūčio 18 dienos mitingas prie Rygos pilies – Latvijos prezidento rezidencijos – sienų surinko be mažiau 5 tūkstančių dalyvių. Šaliai, kurios gyventojų skaičius, netgi oficialiais duomenimis, jau mažesnis nei du milijonai, o neoficialiais paskaičiavimais neviršija pusantro milijono žmonių, tai milžiniškas skaitmuo. Tokio masto protesto akcijų Latvijoje nebuvo nuo 2009 metų sausio mėnesio, kai dėl finansinės krizės šalis neteko penktosios savo ekonomikos dalies.

Tada, 2009 metų pradžioje, likę be pragyvenimo lėšų žmonės iš Rygos senamiesčio gatvelių lupo grindinio akmenis juos mėtė į Seimo langus. Šį kartą viskas baigėsi taikiai: protestuojančiai apsiribojo įžeidžiančiaisiais šūkiais po Latvijos prezidento Egils Levits  langais.

Už tai savaitę anksčiau Lietuvoje viskas buvo kaip prieš 12 metų Latvijoje. Vilniaus centre mitinguojantys neapsiribojo taikiu protestu, o užblokavo Seimo pastatą ir neleido parlamentarams palikti darbo vietą. Saulei nusileidus policijai minią teko išsklaidyti ašarinėmis dujomis.

Ir Latvijoje, ir Lietuvoje protestų priežastimi tapo privalomas skiepijimas nuo koronaviruso ir griežtos sankcijos nepasiskiepijusiems. Tačiau abiejose šalyse protestuotojai neslėpė, jog pas juos iš viso „persipildė“ ir vakcinavimo aistros – tik paskutinis lašas.

Apie visuomeninę-politinę situacija iškalbingai liudija šių šalių valdžių reitingai.

Latvijos pezidento Egils Levits, po kurio langais vakar mitingavo protestuojantys, anti-reitingo skalė siekia 60 procentų. Pas Lietuvos prezidentą Gitaną Nausėdą situacija daug geresnė – juo pasitiki 55 procentai elektorato. Tačiau politinė prognozė Lietuvai  blogesnė, nei Latvijai, kadangi ten masinį nepasitenkinimą didina Nausėdos kanceliarijos politinė kova su vyriausybę, kur valstybės vadovui bando   „iškrėsti šunybę“ ir jį pakeisti URM vadovu Gabrieliu Landsbergiu.

Lietuvoje ir Latvijoje ministrų pirmininkų vyriausybės ir partijos fenomenaliai nepopuliarios. Už valdančiuosius konservatorius – „Tėvynės Sąjunga –Lietuvos krikščionys demokratai“ – pasiruošę balsuoti tik 13 procentų lietuvių. Latvių „Naujosios vienybės“ reitingas iš viso kažkur tai apie 6 procentai.

Negalima sakyti, jog anksčiau šios partijos buvo populiaresnės, bet anksčiau pas gyventojus nebuvo tiek priežasčių nepasitenkinimui, atitinkamai, užteko jėgų kęsti savo netalentingą politinę vadovybę.

Pabaltijo valdžios nėra adekvačios toms naujoms rūsčioms XXI amžiaus realybėms, į kurių iššūkius jos privalo atsakyti. Geriausias tam pavyzdys – migracinė krizė Lietuvoje, į kurią Lietuvos valdžia reagavo juokingai ir pasigailėtinai.

Siūlyti migrantus vežti naktimis – slapta nuo vietinių, kad jie neblokuotų kelių. Ir čia pat projektuoti pabėgėlių laikino 40 tūkstančių žmonių apgyvendinimo stovyklą, ir  natūralų apylinkės miestelių ir gyvenviečių gyventojų pasipiktinimą tokia invazija įtarinėti „antivalstybinės veiklos“ ir „hibridinio karo“apraiška.

Nenuostabu, jog taip elgiantis liaudis nesusiburs aplink valstybę. Atvirkščiai,  pagrindinių Lietuvos vyriausybės figūrų, šiais mėnesiais informacinėje erdvėje asocijuojamųjų su migracijos epopėja,  dėl jos padarinių reitingas  griuvo 10 procentų.

Pažymėtina ir tai, jog parlamentinėje Latvijos Respublikoje liaudies pasipiktinimo epicentre atsidūrė nieko nesprendžiantis, niekam neįtakojantis, ir už nieką neatsakantis prezidentas Egils Levits. Po jo, o ne po Seimo ir Ministrų kabineto langais aidėjo įžeidžiantys šūkiai. Kaip matyti, latvius ypatingai erzina, jog sunkiais laikais jų valstybės vadovu skaitosi absurdiškas žmogus, kuris bejėgiškai juokauja, kad tie, kurie iki Naujųjų Metų mirs nuo koronaviruso, nesulauks Kalėdų.

Alternatyva – tai tokie patys absurdiški personažai, kurie dabartiniu metu yra opozicijoje. Jų reitingas nedaug ką aukštesnis už valdžios reitingą, bet artimiausius rinkimus laimės jie – paprasčiausiai todėl, jog nespėjo taip įkyrėti, kaip įkyrėjo valdžia.

Pilnavertę opoziciją, tai yra, realią alternatyvą esamam šalies raidos kursui, Pabaltijo šalyse jau seniai sutriuškino. Dėl to ir cirkuliuoja politinės infuzorijos, nesugebančios deramai atsakyti į laiko iššūkius.

Todėl Latvijoje ir Lietuvoje įvykę mitingai – ne paskutiniai.

Sukėlusios masinius protestus pamatinės priežastys nepašalintos, ir sušvelninti jų aštrumą gali tik Pabaltijo sugrįžimas į nerūpestingą gyvavimą iki krizės, būnant visiškoje JAV ir ES globoje ir dosniai palaikant jų valdymą iš išorės.

Bet iš Pabaltijo kompozitoriaus dainos žodžių mums žinoma, jog gyvenimą neįmanoma pasukt atgal.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 19 — id: `scraped:rubaltic_lt:34ddadf2a7fc975f`

**Title:** Pekinas nubaudė Vilnių:  Lietuva neteko geležinkelio tranzito iš Kinijos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Geležinkelio kompanijos China railway container transport corp. (CRCT) klientai gavo pranešimus apie tai, jog tiesioginiai pervežimai iš Kinijos į Lietuvą atšaukiami dėl susiklosčiusios politinės situacijos. Mažiausiai iki spalio mėnesio kinų prekės galiniams vartotojams Europoje bus pristatomos alternatyviniu maršrutu (greičiausiai, per Lenkiją). Lietuvai tai ne mirtinga, bet kartu su krovinių tranzitu ji netenka paskutinės vaisingo ir abipusiai naudingo bendradarbiavimo su Padangių šalimi, vilties.

„Įspėjame, jog dėl susiklosčiusios tarp Lietuvos ir Kinijos politinės situacijos bus atšaukiamas tiesioginis traukinys (suplanuotas rugpjūčio 28 dieną – RuBaltic.Ru pastaba) ). Taip pat pranešame, jog visi tiesioginiai traukiniai į Vilnių rugsėjo mėnesiui taip pat bus atšaukiami iki tolesnių žinių iš CRCT“, – rašoma laiške, kurį gavo kinų geležinkelio vežėjo klientai. Šis pranešimas buvo išsiųstas vos keletą dienų po to, kai KLR atšaukė konsultacijoms savo ambasadorių Lietuvoje ir rekomendavo Vilniui padaryti tą patį. Ryšys tarp šių dviejų įvykių akivaizdus: tranzito kroviniai Pabaltijo respubliką palieka kartu su Padangių šalies diplomatijos atstovai.

„Daugelis didžiųjų Kinijos įmonių yra valstybinės, jų vadovai baiminasi dėl savo užimamų postų. – mano Lietuvos transporto atašė Kinijoje Ramūnas Rimkus. - Dėl to, vos tik jie išgirdo apie atšalusius santykius tarp mūsų šalių ir atšauktą konsultacijoms Kinijos ambasadorių, neilgai reikėjo laukti, kol jos net neprašytos parodys savo lojalumą . (...) – „Prarasti tuos kelis eurus atšaukus tiesioginius reisus į Lietuvą jiems atrodo gerokai saugesnis variantas negu užsitraukti partijos rūstybę“.

„Jos net neprašytos“. Kaip ir Lietuva, kuri neturi jokio ryšio JAV Finansų ministerijos sankcijomis „Belaruskaliui“, bet vis vien, dėl visą ko ruošiasi jas įgyvendinti (netgi atsisakymo nuo kiekvienos ketvirtos krovinių tonos Klaipėdos uoste kaina).

Gaunasi taip, jog Kinija išnaudos alternatyvinius prekių tiekimo galutiniams vartotojams maršrutus. Pats akivaizdžiausias variantas – Lenkija. Logistikos kompanijos ACE logistics atstovo Tomo Jankausko žodžiais tariant, kinų geležinkelininkai turi darbo su lenkais patirties.

Kažko tai panašaus reikėjo laukti. Lietuvos susisiekimo ministras Marius Skuodis neseniai pareiškė, jog prekių vežimas iš Padangių šalies gali sumažėti. Bet tai nėra baisu, kadangi prekybiniai-ekonominiai Lietuvos ryšiai su Kinija silpni. 2019 „iki kovidiniais“ metais užsienio prekybos apimtis tarp jų sudarė tik 1,35 milijardo dolerių.

Iš kitos šalies, dar prieš 3-4 metus Lietuva bandė organizuoti bendradarbiavimą su Kinija. Tai žadėjo būti labai pelningu. Vengrija neleis sumeluoti: 2017 metais šalis jau gavo iš Kinijos investicijų už 4 milijardus dolerių, kas leido įsteigti 10 tūkstančių naujų darbo vietų. Tai nedidelio Lietuvos miesto gyventojų skaičius.

Paskutinis kinų-vengrų bendradarbiavimo pasiekimas – susitarimas Budapešte įkurti Šanchajaus Universiteto Fudanj filialą. Kada Lietuvoje paskutinį kartą buvo atidaromos naujos aukštojo mokslo įstaigos? Dar prie Sovietų?

Netgi praėjusiais metais, ekonominės krizės metu, kinų kapitaliniai įdėjimai užsienyje išaugo 3,3 procento (iki 132,9 milijardo dolerių). Nei viena šalis nesiūlo pasauliui tokios investicijų apimties.

Prisiminkime, ką sakė 2017 metais tuometinis Respublikos susisiekimo ministras Rokas Masiulis:

„Lietuva siekia, kad per šalies teritoriją keliautų kuo daugiau krovinių iš Kinijos į Europą, būtų naudojamasi Šeštokų, o po kelerių metų, kai bus baigti europinės geležinkelio vėžės įrengimo darbai, - ir Palemono įvairiarūšiais terminalais. Be to, esame pasirengę stiprinti trišalę partnerystę su Kinija ir Baltarusija. Galime užtikrinti kokybišką transporto ir logistikos grandinę tiek jūra per Klaipėdos uostą, tiek geležinkeliu, kroviniams, skirtiems prie Minsko Kinijos įmonės „China Merchants Group“ kuriamam pramonės parkui „Didysis akmuo“, - sakė susisiekimo ministras R. Masiulis. Tie laikai liko praeityje. Su Baltarusija Lietuva susibarė, į bendrus transporto-logistikos projektus dabar galima įtraukti nebent Svetlanos Tichonovskajos biurą, bet pinigų ant to neuždirbsi.

Analitinis RuBaltic.Ru portalas jau rašė, jog skausmingu Padangių šaliai tapo Lietuvos išėjimas iš bloko „17+1“ ir Gabrieliaus Landsbergio raginimas Europos Sąjungoje sukurti principingai naują bendradarbiavimo su Kiniją formatą. Užsižaidimas su Taivaniu paprasčiausia perpildė KLR Komunistų partijos kantrybės taurę, kuri ilgą laiką stebėjo nedraugiškus Vilniaus veiksmus: diskusiją apie „uigūrų genocidą“, Dalai-lamos vizitą, kinų kompanijų diskriminavimą ir t.t.

Nukreiptų prieš Kiniją Lietuvos iniciatyvų išvardijimui vieno straipsnio tikrai bus maža.

Ar nukentės šalies ekonomika dėl santykių su Kiniją pablogėjimo? Skuodis teisus: nuostolis bus nežymus. Bet Lietuva atsisako dar ir potencialių kinų investicijų, kurios galėtų būti skaičiuojamos milijonais dolerių.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 20 — id: `scraped:rubaltic_lt:b0cdc73be79d73c3`

**Title:** Baidenas užfiksavo: globalinė JAV imperija pasibaigė

**Source:** rubaltic_lt (propaganda)

**Text:**

```
JAV prezidentas Džozefas Baidenas kreipėsi į naciją dėl amerikiečių išėjimo iš Afganistano ir šalies užgrobimo „Talibanu“ (Rusijoje uždrausta terorizmo organizacija - RuBaltic.Ru pastaba ). Savo kalboje Baidenas pareiškė, jog Amerikos tikslu Afganistane buvo JAV nacionalinio saugumo gynimas, o, jokių būdu, ne demokratijos pastatymas ten. Šie žodžiai reiškia, jog JAV netgi retorikos lygyje atsisako globalinės misionierystės ir „pasaulinio žandaro“ vaidmens. Skaitlingai klientelei, kuri aptarnavo pasaulinį Amerikos viešpatavimą, bus nepaprasta.

«Amerikiečių kariuomenė negali ir neturi dalyvauti kare ir žūti kare, kuriame afgano jėgos nepageidauja grumtis patys už save. Mes išleidome daugiau trilijono dolerių. Mes apmokėme ir apginklavome afgano karines pajėgas, kurių sudėtyje yra apie 300 tūkstančių žmonių, - paskelbė Džo Baidenas […] Mes jiems davėme visus šansus patiems išsirinkti savo ateitį. Ko mes negalėjome jiems duoti, tai valios kovoti už tą ateitį“.

Šią amerikiečių lyderio kalbos dalį Kijeve dabar turi skaityti balsu ir išraiškingai.

Baidenas pasakė Afganistane paliktiems globotiniams, kurie turėjo oficialaus amerikiečiu sąjungininko už NATO ribų statusą. Tai tas pats statusas, kurio siekia Ukraina. Jei Nezalėžnos neima į NATO, tai, gal būt, nors už sąjungininką už NATO ribų Jungtinės Valstijos kariaus Donbase su „separais“ ir „moskaliais“?

Nekariaus. Ginklus ir instruktorius davėme? Viskas, toliau kariaukite patys.

Tarp kitko, tai dar ne pati nemaloniausia Baideno kalbos dalis. Kiti jo žodžiai nesiūlo nieko gero ir NATO sąjungininkams.

«Kaip aš sakiau balandyje, Jungtinės Valstijos išsprendė uždavinius, kuriuos įvedant pajėgas į Afganistaną mes sau iškėlėme: neutralizuoti teroristus,kurie mus užpuolė rugsėjo 11; teisti Usam ben Ladeną, taip pat sumažinti terorizmo grėsmę, dėl to kad Afganistanas netaptu busimųjų JAV atakų baze. Mes išsprendėme tuos uždavinius. Būtent dėl to į šalį mes ir įvedėme kariuomenę“,- pasakė Amerikos prezidentas. O po to pasakė svarbiausią: Į Afganistaną mes atvykome ne tam, kad statyti valstybę.Tik afgano liaudis turi teisę ir privalo nuspręsti savo ateitį, ir tai, kaip ji nori valdyti savo šalį“.

Arba JAV prezidentas įžūliai meluoja, arba, atvirkščiai, šokuojančiai atviras.

Visuotiniai tiesioginiai rinkimai, moterų teisės ir kitą – visa tai buvo vadinama tiesioginiais amerikiečių intervencijos pasiekimais.

Amerikietiška masinės kultūros institucijos netgi kūrė savo agituotes demokratijos pergalės Afganistane tema. Būdingas pavyzdys – ekranizuotas afgano kilmės amerikiečių rašytojo Haled Hosein bestseleris „Tūkstantis šviečiančių Saulių“ apie tai, kaip pagerėjo Kabulas prie amerikiečių, kurie atnešė žmogaus teises, laisvę ir demokratiją.

Jei dabar Džo Baidenas sako, jog tokių uždavinių amerikiečiai visiškai nekėlė, tada suprantama, kodėl afgano demokratija „paspruko per tris dienas“, tada, kai po sovietų kariuomenės išvedimo prosovietinis režimas laikėsi trejus metus, ir būtų išsilakęs ilgiau, jei ne būtų suirusi TSRS ir jelcinškos Rusijos ne būtų atsisakiusi palaikyti Machamadą Nadžibulą. Todėl, kad amerikiečiai, iš tikrųjų, ten jokios demokratijos nestatė.

Tiksliai taip pat, kaip Irake, Sadamo Huseino nuvertimas amerikiečiams buvo reikalingas, kad iš ten pompuoti naftą, ir dėl to jie „atnešė demokratiją“.

Tiesos apie Amerikos politiką pagarsinimą ne bet kokiu ten kairiuoju amerikiečiu disidentu, o asmeniškai JAV prezidentu, pervertinti neįmanoma.

Amerika netgi retorikos lygyje atsižada savo globalinės žmogaus teisių ir demokratijos platinimo pasaulyje misijos, o šia misija pagrindžiamos pretenzijos į globalinę lyderystę.

Dabartinei Vašingtono politikai tai ilgo kelio, kurį pradėjo dar Barakas Obama, pradėjęs nenuosekliai, su pertraukomis mažinto amerikiečių kontingentų buvimą užsienyje, maskuodamas šį procesą patosinėmis kalbomis apie „amerikietišką nepaprastumą“, pabaiga.

Donaldas Trampas kalbų atsisakė. Rinkėjams jis sakė tiesiai: Amerika perdaug nerimauja dėl svetimų sienų, vietoj to, kad pasirūpinti savo siena su Meksika. Amerikiečiai turi užsiimti Jungtinėmis Valstijomis, o ne spręsti svetimas problemas ir rūpintis svetimu likimu.

Džozefas Baidena ėjo į valdžią su retorika, kuri buvo visais atvejais priešiška Trampo retorikai, tačiau, užėmęs prezidento postą, logiškai užbaigė jo politiką. Ženevoje „sutarė“ su Putinu ir pradėjo karinių pajėgų išvedimą iš Irako ir Afganistano. O, kai, išvedus kariuomenę iš Afganistano, iškarto griuvo proamerikietiškas režimas, paliktiems globotiniams grynai trampiškai pasakė: amerikiečių vaikinai kovoti už jūsų laisvę neprivalo.

Juk pas globalinį lyderį visuose planetos regionuose buvo daug agentų, kurie teikė jo lyderystės palaikymo ir stiprinimo paslaugas. Lenkijos ir Baltijos šalių užsienio politika, pavyzdžiui, tik tuo ir gyveno.

NATO rytų šalių politikoje nacionalinių interesų visiškai nebuvo – vien tik strateginiai JAV interesai Europoje.

Globalinio hegemono interesai buvo pirminiai, o visokios Gedrojico-Meroševskio doktrinos ir atsiminimai apie Lietuvos Didžiąją Kunigaikštystę – antriniai. Baltijos satelitai ir dabar iš inercijos tęsia amerikiečių interesų aptarnavimą. Iš Baltųjų Rūmų jiems pasiuntė nedviprasmišką signalą. Visas savo politikos sąnaudas apmokėsite savarankiškai.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```
