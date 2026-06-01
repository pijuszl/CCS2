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

### Article 1 — id: `scraped:rubaltic_lt:a8c80198e0ef01a2`

**Title:** Afganistane JAV parodė Pabaltijui sąjungininkų  išdavystės meistriškumo klasę

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Pabaltijyje formuojasi reagavimo į JAV krachą Afganistane, kaip į bendrąjį Vakarų pasaulio, įskaitant ir Baltijos šalių krachą, koncepcija. Panašiu savęs plakimu Estija, Latvija ir Lietuva bando išvengti nemalonaus fakto, jog amerikiečiai metė, išdavė ir paliko savo sąjungininkus Afganistane konstatavimo ir, vadinasi, gali tiksliai taip pat išduoti savo sąjungininkus Rytų Europoje.

„Mes norėjome tikėti, jog Afganistano karinės pajėgos, policija ir valstybės aparatas, kuriuos mes išmokėme, nori ginti savo šalį ir laisvę, Deja, to neatsitiko. Žinoma, nesėkmė buvo laukiama, kaip sąjungininkai, taip Afganistano valdžia tam buvo pasiruošusi balandžio mėnesį, kai aš Kabule susitikau su ja. Tačiau, toks veržlus žlugimas tapo netikėtų“,- pareiškė Estijos prezidentė Kersti Kaljulaid dėl įvykiu Afganistane.

Kaljulaid pasisakyme įdomiausiu – tai, žinoma, įvardis „mes“ .

Ir tokią taktiką pasirinko ne viena Kersti Kaljulaid. Pabaltijo valstybėms sakyti „Afganistane sužlugome mes“, vietoj „Afganistane sužlugo amerikiečiai“ tampa savotiška psichologinio apsigynimo priemone.

Viso pasaulio žiniasklaida užpildyta panikos Kabulo oro uoste kadrais, po to kai Afganistano sostinę užgrobė talibai (Rusijoje uždrausta terorizmo organizacija - RuBaltic.Ru pastaba). Apimti siaubo stengiasi išskristi iš Afganistano žmones, kurie 20 metų rėmė okupacinį amerikiečių režimą, kuris ten statė demokratiją. Ir negali išskristi, kadangi amerikiečiai gelbėjasi patys, o juos palieka.

Į istorija, tikriausiai, įeis video su afganistaniečiais, kurie įsikabino į amerikiečių orlaivio šasi ir tokiu būdu bandė išskristi, todėl kad salone jiems neliko vietos. Vietas lėktuve skyrė amerikiečių tarnybiniams šunims, bet ne vietiniams pagalbininkams, kurie paskutiniųjų 20 metų laiku pasirinko „laisvą pasaulį“. Dėl to ypatingą įspūdį sukelia afganistaniečių kūdikio, išmesto ant pakilimo tako krepšelyje asmeniniams daiktams tikrinimo metu fotografiją.

Komentuodama šias siaubingas scenas amerikiečiu žiniasklaida viską vadina savo vardais. Viskas kas vyksta – ant Amerikos sąžinės. Pats dažniausias žodis – išdavystė. Amerika išdavė tuos, kurie ja tikėjo.

Tai pats tas atvejis, kai satelitai Rytų Europoje paprasčiausiai organiškai nesugeba lygiuotis į Ameriką, kaip darė visada. Dabar jų pirštai ant klaviatūrų nepakils parašyti tą patį, ką rašo amerikiečiai.

Ukrainos socialiniuose tinkluose plinta isteriška kampanija, reikalaujanti jau baigti naudoti tą žodį - „išdavystė. Esą, tokiu būdu jūs propaguojate „Kremliaus propagandai“ naudingą naratyvą.

Pagarsinami įvairūs „gudrūs planai“, jog tai kas įvyko Kabule – „peremoga“(pergalė), o ne „zrada“(pralaimėjimas). Amerika, esą, sudavė mirtiną smūgį Rusijos ir Kinijos „autokratijai“, vietoje vesternizuotos demokratijos greta jų sienų sukūrusi terorizmo valstybę. Logiškas argumentas, kad, tokiu atveju, Amerika jau išdavė Ukrainą, kadangi tokios šalies kaip Afganistanas chaotizavimas atsilieps visai Eurazijai nuo Vladivostoko iki Lisabonos, iššaukia naują psichozę.

Pabaltijo šalyse truputi kita situacija: jos NATO narės ir „tarptautinės koalicijos“ Afganistane dalyvės. Todėl jos gali sau leisti pasakyti „sąjungininkus išdavėme mes“. Taip pasakyti galima, skirtingai nuo „sąjungininkus išdavė JAV“.

Lietuvoje, pavyzdžiui, vystomas siužetas dėl afgano vertėjų, kurie ilgą laiko padėjo Lietuvos kariškiams bendradarbiauti su vietiniais gyventojais. Lietuva ir norėtų juos išgelbėti nuo gyvenimo baisybių su „Talibanu“ (Rusijoje uždrausta terorizmo organizacija - RuBaltic.Ru pastaba), bet negali vertėjus išgabenti iš Kabulo. Gėda nors verk, nors Vilnius ir daro viską kas įmanoma.

Tokie komunikaciniai fokusai dabar taikomi, kad nukreipti dėmesį nuo to, kas Pabaltijui, neabejotinai, šioje istorijoje yra svarbiausia.

Estija, Latvija ir ypatingai Lietuva 30 metų vykdė savo ir savo pačių interesų atžvilgiu beprotišką proamerikietišką užsienio politiką, absoliučiai įsitikinę, jog Amerika juos visada apgins. Dabar prieš Pabaltijo politikus atsivėrė bedugnė, kurioje jie griebiasi amerikiečių orlaivio šasi, kadangi sprunkantys amerikiečiai jų vietas salone atidavė tarnybiniams šunims.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 2 — id: `scraped:rubaltic_lt:fc6a26dd7d2f466e`

**Title:** „Energetinės nepriklausomybės“ žlugimas: Lietuva pripažino SGD terminalo bereikalingumą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Dėl staigaus dujų ir biokuro kainų augimo ateinantis šildymo sezonas Lietuvoje bus maždaug ketvirtadaliu brangesnis negu praėjęs. Tokią išvadą padarė valstybinės energetikos reguliavimo tarybos specialistai. Įdomu tai, kad prieš metus Pabaltijo respublikos valdžia gyrėsi Klaipėdos SGD terminalo pasiekimais, kuris, esą, atpigino gamtines dujas galutiniam vartotojui. Kodėl gi šis stebuklingas „energetinės nepriklausomybės “ nuo Rusijos efektas taip greitai pasibaigė?

Analitinis RuBaltic.Ru portalas jau pasakojo, kodėl Europoje dujų kainos pasiekė rekordines aukštumas. Jei prieš metus pasaulio angliavandenilių rinkoje situacija vartotojams buvo palanki (tarp kitko, visiems be išimties), tai dabar viskas diametraliai pasikeitė.

Pirma, energijos šaltinių paklausa visame pasaulyje auga pasaulio ekonomikos išėjimo iš „koronakrizės“ tempu. Antra, taip pat įtakoja orai. 2020/2021 šildymo sezonas ES šalyse pasižymėjo smarkiais šalčiais. Po anomaliai šiltos praėjusios žiemos europiečiai tam pasiruošę nebuvo, pavasarį pažeminės dujų saugyklos pasirodė stipriai nualintos. Po to atėjo anomalinė vasara: liepa tapo pačiu karščiausiu mėnesiu ant žemės per visą meteorologinių stebėjimų istoriją. Dėl to pramonė išeikvoja dideles elektros energijos apimtis kondicionavimui.

Prioritetinėmis rinkomis jiems tapo Azijos - Ramiojo vandenyno regiono šalys, kur angliavandenilių kainos tapo dar didesnės. Palyginus su praėjusias metai, Europos SGD terminalų apkrova stipriai „nusėdo“. Jau kurie metai iš eilės stagnuoja vidaus gavyba.

Išeina, jog augančią dujų paklausą Europoje gali patenkinti tik Rusijos „Gazpromas“.

Vykdydama savo kontraktinius įsipareigojimus Rusija per Ukrainą netiekia papildomas „žydrojo kuro“ apimtis. Tiksliau, ne tiekė. Rugsėjui „Gazpromas“ jau užrezervavo papildomas Ukrainos dujų tiekimo sistemos galias, kurios pasirodė tokios žemos, kad dujų kaina Europoje vėl atnaujino istorinį maksimumą (585 doleriai už tūkstantį kubinių metrų).

Iš kitos pusės, Rusijos dujų holdingo ataskaitos liudija apie tai, kad jo kaltinimas bandymu šantažuoti Europos energetiką, mažiausiai, nėra korektiškas. Sausio – birželio mėn. „Gazpromas“, lyginant su analogišku praeitų metų periodu, 28,52% padidino dujų tiekimą į Vakarų Europos šalis. Dujų tiekimas į Centrinę Europą pasiliko maždaug tokio pat lygio, o eksportas į Turkiją išaugo daugiau kaip tris kartus.

Finansų universiteto prie RF vyriausybės eksperto Igorio Juškovo vertinimu, išsilaikius dabartiniai dinamikai, „Gazpromas“, remiantis metų rezultatu, į Europą gali eksportuoti rekordines dujų apimtis (daugiau 200 milijardų kubų). Bet ir to, pasirodo, nepakanka.

„Europiečiai mums pastoviai pasakojo, kad ten pas juos, esą, stovi SGD tiekėjų eilė, kad „tai vartotojo rinka, ir mes rinksimės“. O dabar, pasirodo, Azijoje aukštos kainos – ten apie $600 už tūkstantį kubų, ir ten perėjo visi SGD tiekėjai – į kinų, japonų, korėjiečių rinkas,-paaiškina Juškovas.

Chrestomatinis pavyzdys – Lietuva. Koronaviruso pandemija tapo tikra dovana jos SGD terminalui Klaipėdoje. Jis ne tik pasiekė rekordines kuro regazifikavimo apimtis, bet leido vartotojams įsigyti gamtines dujas rinkos kaina, Taip tvirtino terminalo Klaipėdos nafta kompanijos operatoriaus direktorius Darius Šilenskis.

Be SGD terminalo – vamzdyno dujų iš Rusijos alternatyvos, tai būtų neįmanoma. Mūsų skaičiavimai rodo, kad per 2020 dujų metų laiką Lietuvos gamtinių dujų vartotojams iš SGD terminalo patiekta daugiau kaip 70% bendros gamtinių dujų vartojimos apimties“,-sakė Šilenskis.

Kartu su tuo Lietuvoje nenorėjo kalbėti, jog dujos visur tapo pigesnės. Kodėl, pavyzdžiui, Vokietija pirko po 70 dolerių už tūkstantį kubų, nors neturėjo ir neturi jokio SGD terminalo? Koks terminalas padėjo sumažinti komunalinius tarifus Ukrainos vartotojams? Joks. Ukrainoje „stebuklas“, esą, įvyko dėka valstybės vadovybės su Vladimiru Zelenskij priešakyje išminties...

Po to atsitiko tai, kas turėjo atsitikti: rinkos konjunktūra pasikeitė.

Lietuvoje dujos ir elektros energija brangsta visą vasarą. Remiantis valstybinės energetikos reguliavimo tarybos prognozėmis, ateinantis šildymo sezonas bus maždaug ketvirtadaliu brangesnis. Viena iš priežasčių – biokuro iš Baltarusijos deficitas, kurį išperka baldų gamintojai. Bet pagrindinis vaidmuo čia, žinoma, tenka dujoms.

«Pabrango žaliava», - taip apibūdina situaciją Lietuvos valstybinės energetikos reguliavimo taryboje. Nei vieno žodžio apie tai, kad respublika turi savo SGD terminalą! Tą patį, kuris praėjusiais metais,esą, padėjo šaliai sukaupti didėlę dujų apimtį už žemą kainą. Kur prapuolė jo stebuklinga jėga? Kodėl dabar jis nepadeda sulaikyti dujų kainas?

Iki 2020 metų Klaipėdos terminalas buvo „mokesčių mokėtojų našta“ ( taip jį apibūdino buvęs Lietuvos ministras primininkas Saulius Skvernelis). Konvidinių apribojimų metų iškilo jo žvaigždės valanda, bet greitai viskas grižo į savo vietas.

Istorija, kurią Lietuvos valdžia, paprasčiausiai išsigalvojo, ir apie kurią dabar kažkodėl tai ne užsimena.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 3 — id: `scraped:rubaltic_lt:7f76e82a98c7285d`

**Title:** JAV sprukimas iš Afganistano sukels naują migracinę krizė  Lietuvoje

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Išėjus amerikiečių kariuomenei, Afganistano valdžia istoriškai rekordiniu laiko tarpu griuvo į islamistų judėjimo „Taliban“ (uždrausta Rusijoje teroristinė organizacija - RuBaltic.Ru pastaba) rankas. JAV likimo valiai paliko ne tik savo marionetes Kabule, bet ir visus sąjungininkus Eurazijoje, kurioms – nuo pietryčių Azijos iki ES šalių – dabar gresia nauja nelegalios migracijos ir terorizmo banga. Šios vasaros migracinė krizė Pabaltijo šalims gali pasirodyti vaikelio vapaliojimu, po krizės, kurią išprovokavo jų, esantis už vandenyno patronas dėl kurio jie 30 metų griovė santykius su Rusija.

JAV Prezidentas Džozefas Baidenas nusprendė iki rugsėjo 11 d. išvesti visus amerikiečių kariuomenės padalinius iš Irako. Šiame sprendime buvo ypatingas politinis simbolizmas. Į Afganistaną JAV įėjo po 2001 m. rugsėjo mėn. 11 dienos terorizmo aktų, tam kad sutriuškinti tarptautinį terorizmą jo paties urve.

Per 20 metų amerikiečiai padarė viską ką norėjo: atkeršijo, sutriuškino, atnešė į Afganistaną liberalines vertybes, pastatė ten demokratiją, ir teroristinės JAV atakos jubiliejaus dieną išeina namo su atliktos pareigos jausmu.

Ir iš tikrųjų, simbolizmas pasisekė, ko atimti negalima.

Išėjus JAV kariuomenei, proamerikietiškos vyriausybės žlugimas buvo išspęstas reikalas – tai suprato visi, kaip suprato ir tai, jog valdžios vakuumą Afganistane po amerikiečių išėjimo gali užpildyti tik talibai (uždrausta Rusijoje teroristinė organizacija - RuBaltic.Ru pastaba). Tačiau, mažai kas numatė, jog amerikiečių marionečių režimas Kabule sugrius per tokį istoriškai rekordinį laiko tarpą.

Prosovietinis Nadžibulos režimas po sovietų kariuomenės išvedimo iš Afganistano išsilaikė trejus metus. Proamerikietiškas režimas po dalies amerikiečių kariuomenės išvedimo iš Afganistano neišsilaikė ir trejus mėnesius.

Visas Afganistanas visiškai kapituliavo prieš talibus rugpjūčio 15-ąją. Ryte talibai tik ruošėsi šturmuoti Kabulą, o po pietų prezidento rūmuose jau priėmė besąlyginę kapituliaciją ir valdžią.

Iš afgano sostinės ištisą dieną vyko masinis sprukimas visų tų, kurie 20 metų centrinės Azijos respubliką mokė demokratijos ir žmogaus teisių. Šiuolaikinės technologijos suteikė galimybę visam pasauliui stebėti šį žavingą procesą tiesiogiai.

Ypatingai plačiai išplito JAV ambasados evakuacijos iš Kabulo kadrai. Amerikiečių diplomatai glaudžiasi ant stogo, o kariškių sraigtasparniai paeiliui jus kelią į orą.

JAV prezidentas Džozefas Baidenas prigrasino islamistams „greitu ir galingu“ kariniu atsaku, jei jie užpuls JAV ambasadą arba vis dar šalyje liekančius amerikiečių kariškius. Šie grasinimai paprasčiausiai yra graudūs. Koks „greitumas ir galingumas“, jei „Talibanas“ jau užėmė Kabulą, priėmė amerikiečių statytinio kapituliaciją ir kontroliuoja beveik visą Afganistano teritoriją?

Afganistane JAV visiškai apsigėdijo. Po savęs jie palieka skurdą, nualinimą, terorizmą, šimtus tūkstančių heroino narkomanų, prekeivių narkotikais. Savo civilizuota misija JAV su sąjungininkais padarė taip, jog Afganistane pasidarė blogiau , nei buvo. Dabar „Talibanas“ kontroliuoja didesnę teritoriją, negu 2001 metais, kada amerikiečiai ten įlindo su demokratijos eksportu.

JAV krachą dabar lygina su amerikiečių sprukimu iš Saigono 1975 metais. Tačiau ši analogija teisinga tik pačių JAV atžvilgiu. Eurazijos kontinentui JAV pralaimėjimas Afganistane yra nepalyginimas su tais padariniais kurie kilo po JAV pralaimėjimo Vietname.

Ypatingai įdomu dabar sulaukti, taip vadinamos „tarptautinės koalicijos“ šalių, JAV sąjungininkių, kurios siuntė į Afganistaną savo karius paremti amerikiečius, komentarų dėl situacijos. Dėl ko visą tai buvo daroma?

Klausimas nėra tuščias. Afganistane per 20 amerikiečių okupacijos metų žuvo, pavyzdžiui, vienas Lietuvos, keturi Latvijos, devyni Estijos ir keturiasdešimt keturi Lenkijos kariškiai.

Už ką toje tolimoje Azijos šalyje žuvo žmonės nuo Baltijos krantų? Už demokratiją ir žmogaus teises? Jie pralaimi netgi jų šalyse, jau nekalbant apie Afganistaną. Už savo valstybių interesus ir nacionalinį saugumą? Jie taip pat pralaimėjo.

Todėl, kad paskutiniu metu tik iš vieno daugiamilijoninio Kabulo lėktuvai, nesustodami, išskrenda į vieną galą.

Kas dabar gali išgelbėti Europą nuo pačio blogiausio scenarijaus? Visa tai, ką dešimtmečiais europiečių ir savo pačių akyse demonetizavo Lenkija ir Pabaltijys. Rusija, ODKB, Eurazijos integracija. Rusiškas „geras žodis su pistoletu“, kai, iš vienos šalies, Rusijos kariuomenė ir postsovietinės Vidurinės Azijos respublikos telkia pajėgas prie sienos su Afganistanu, o iš kitos šalies, rusiška diplomatija mandagiai ir aiškiai pareiškia talibams: jūs nelendate per sieną pas mus – tada ir mes nelendame per sieną pas jus.

Nedrąsus pagrindas tikėtis sėkmės yra. „Talibanas“ gerbia jėga, o Rusiją gerbia dar daugiau, negu amerikiečius. Rusijos ambasada iš Kabulo neevakuojama: Rusijos diplomatams „Talibanas“ užtikrino neliečiamumą.

Kyla įdomus klausimas: ar turi Rusija, kaip Europos dalis, dabar veikti kieno tai interesams ir saugumui, neskaitant savo interesų? Kaimynai iš Vakarų vis vien jai nepadėkos ir toliau vadins ją agresoriumi bei okupantu, kurį reikia „sulaikyti“.

Gal būt Pabaltijo šalims dirbti su „Talibanu“ savarankiškai? Tegul ir toliau tikisi pagalbos ir apgynimo iš JAV, kurios juos eilinį kartą paliko.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 4 — id: `scraped:rubaltic_lt:631856cf34d3d0ba`

**Title:** Lietuviai prieš politikus: tauta sugėdino   „kovotojus už demokratiją“ Rusijoje ir Baltarusijoje

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Masinė protesto akcija, rugpjūčio 10 užsiplėkusi Vilniuje, sunervino   Lietuvos isteblišmento atstovus. Tarp tų, kuriems atiteko porcija „tautos meilės“, atsidūrė nemaža žinomų „kovotojų už demokratiją“ Rusijoje ir Baltarusijoje. Su savo nuosavu demosu, tai yra tauta, pas juos, kaip tapo aišku susiformavo ne patys šilčiausi santykiai: lietuviai sutartinai įžeidinėjo ir žemino savo išrinktuosius.

Vienas iš pirmųjų Lietuvos Seimo pastatą, greta kurio susirinko nepatenkinti lietuviai, paliko gynybos ministras Arvydas Anušauskas. Būtent jis, 2020 metų rugpjūtyje, būdamas parlamento deputatu nuo partijos „Tėvynės sąjunga – Lietuvos krikščionių deputatai“ (TS-LKD), pasiūlė suformuoti delegaciją į Baltarusiją.

Ten jo niekas nekvietė, bet Anušausko tai nejaudino. Jau labai norėjosi padėti broliškai baltarusių tautai ir padalyvauti politinės krizės sureguliavime užsienio valstybės teritorijoje.

Su nepatenkinta minia gynybos ministras bendrauti nepanoro – skubiai sėdo į automobilį su personaliniu vairuotoju.

Pats laikas baltarusių deputatams pasiūlyti savo tarpininkavimą politinės krizės sureguliavimui Lietuvoje.

Vienu iš tų, kurį mitingo dalyviai sugėdino, tapo deputatas Tomas Tomilinas. Prieš metus jis taip pat buvo delegacijos, kurią suformavo Lietuvos Seimas politinės krizės Baltarusijoje sureguliavimui, nariu. Vėliau grupė Lietuvos deputatų pareikalavo nedelsiant paleisti sulaikytus baltarusius ir pravesti naujus laisvus rinkimus.

„Tai ne vidinis Baltarusijos reikalas. Kiekviena JTO valstybė savanoriškai prisiėmė tarptautinius įsipareigojimus gerbti ir laikytis žmogaus teisių. Šio įsipareigojimo nesilaikymo atveju tarptautinė bendrija turi teisę ir privalo reaguoti“ – buvo sakoma kreipimesi, kurį tarp kitų pasirašė ir Tomas Tomilinas. Įdomu, ar dabar jis reikalaus paleisti sulaikytus lietuvius ir pravesti pirmalaikius rinkimus Lietuvoje?

Visų garsiausiai minia „sveikino“ parlamento nacionalinio saugumo ir gynybos komiteto pirmininką, konservatorių Lauryną Kasčiūną.

Likimo ironija, prieš tai buvusiame parlamento sušaukime Kasčiūnas vadovavo visai deputatų grupei „Už demokratinę Baltarusiją“. Perrinkus Lukašenką, jis kalbėjo, jog Baltarusijos tauta laukia Lietuvos pagalbos, todėl kuo greičiau reikia įvesti sankcijas Baltarusijai.

Demokratijos būsena Rusijoje jis, suprantama, taip pat yra labai susirūpinęs. 2016 metais Kasčiūnas parašė straipsnį apie galimą Putino režimo žlugimą.

„Ar žlunga jo sistema? Ar yra „dvaro perversmo“ galimybė? Ar bręsta nepatenkintos Rusijos visuomenės revoliucija? Ar Rusijoje galima politinės sistemos pertvarka?“ – tokius klausimus kėlė Kasčiūnas.

Dvasinis Lietuvos konservatorių lyderis Vytautas Landsbergis prieš metus pasižymėjo tuo, jog įrašė patetišką video kreipimąsi į baltarusius, kuriame kvietė juos kuo greičiau nuversti Lukašenką ir įsteigti „tikrąjį parlamentą“.

„Broliai baltarusiai! Jūs stebinate pasaulį valingu visos tautos pareiškimu: „Mes esame! Mes-tauta! Mes-laisva tauta! Šalis! Mes ne kokios tai valstybės užkampis ir patys pasirinksime savo likimą. Mes ne kolchozas. Ir mums nereikalingas pirmininkas su lazda“, Štai, ką Jūs turite pasakyti“, - patarinėjo Landsbergis.

Komentuodamas rugpjūčio 10 d. įvykius Landsbergis pasakė: „Yra tikrai labai rimtų problemų, bet ne dėl jų maištaujama. Maištaujama dėl pamaištavimo ir galbūt dėl kokio nors prasibrovimo į valdžią. Ne be reikalo tokie šūkiai: šalin Seimą, šalin Vyriausybę, aš noriu būti valdžia. Bolševikiniai metodai“

Dėl paskutinio tvirtinimo nesiginčysime. Apie bolševikų metodus Landsbergis, praeityje pats būdamas KGB agentu Dėdulė, žino gerai. Tik nesuprantama: kodėl Baltarusijoje tokius metodus taikyti galima (netgi reikia!), o Lietuvoje – nevalia?

Dėdulės Vytauto anūkas – dabartinis užsienio reikalų ministras Gabrielius Landsbergis – iš vis nerizikavo pasirodyti publikai.

„Taisyklių laikymasis yra labai svarbus. Protestuoti visi Lietuvoje turi teisę – demonstruoti, piktintis, priekaištauti vyriausybei, valdžiai, bet kam. Tai yra pamatinis principas, tačiau taisyklių laikymasis irgi yra pamatinis principas dėl to, kad vakar, manau, buvo tam tikri principai pažeisti. Ypatingai, kas susiję su Seimo narių teise saugiai dirbti savo darbą“, – pasiskundė G. Landsbergis. Ką gi, rugpjūčio 10 įvykiai leido jam suprasti Ukrainos Euromaidano laikų valdininkus, kuriems nebuvo leidžiama dirbti „aktyvistų“ užgrobtuose pastatuose.

Bet jiems dar pasisekė. Nepasisekė techniniam „Regionų partijos“ biuro darbuotojui Vladimirui Zacharovui, kuris žuvo šio biuro šturmo metu sužvėrėjusiais maidaniečiais. Apie jo teisę į saugų darbą landsbergistai nieko nesakė – jie žavėjosi ukrainiečių tautos meile laisvei ir narsumu!

Tikriausiai, autobuse buvo dar nemaža žinomų kovotojų už demokratiją Rusijoje, Baltarusijoje ir Ukrainoje. Bet savo šalyje „maidano“ tipo demokratijai jie nepritaria. Ir į ją reaguoja tiksliai taip pat, kaip ir Lukašenka: skatina mitinguojančių išvaikymą, jų baudžiamąjį persekiojimą, užsienio įsikišimo paiešką.

„Situacija yra tokia, jog tai hibridinė ataka. Tie procesai kurie vyksta nelegalios migracijos kontekste, kai mūsų jėgos sutelktos ant sienos, kai kyla tokie iššūkiai, tokios nesankcionuotos iniciatyvos, o ne kokie tai civilinės pozicijos pasireiškimai, tai gerai organizuota antivalstybinė veikla“,- pareiškė Lietuvos vidaus reikalų ministrė Agnė Bilotaitė.

Taip pat ir bet kokia kita dingstimi.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 5 — id: `scraped:rubaltic_lt:057a352df724dc8e`

**Title:** Lietuva įžengia į revoliucinę situaciją

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Ryte, išvaikius protesto akciją prie Seimo rūmų, Ingridos Šimonytės vyriausybė visgi patvirtino skandalingus apribojimus dėl nepaskiepytų nuo COVID -19 lietuvių buvimo viešose vietose. Padarytos nuolaidos yra tokios nežymios, jog jos neleidžia sumažinti žmonių pasipiktinimo laipsnį. Opozicinės parlamento partijos kviečia žmones į visos tautos streiką, prie nepopuliarių vyriausybės sprendimų prisideda naujos riaušės pabėgėlių stovyklose – Lietuvoje vis aiškiau formuojasi revoliucinė situacija.

Tokiu būdu, nuo rugsėjo 13 dienos nevakcinuotiems lietuviams, be neigiamo koronaviruso testo ir „galimybių paso“  - priedo su vakcinacijos/antikūnų  liudijimu – draudžiama lankytis prekybos centruose, viešose priemonėse, grožio salonuose ir viešojo maitinimo centruose. Apsipirkti bus galima tik vaistinėse ir nedideliuose produktų parduotuvėse.

Anksčiau norėjo ir tai uždrausti, o dar neleisti neskiepytiems naudotis viešuoju transportu, neleisti jų į ligonines; neapmokėti jiems nedarbingumo pažymėjimų bei nemokėti bedarbio pašalpų. Toks „varžtų užveržimas“ galų gale „nuplėšė sriegius“: drakoniškos Šimonytės vyriausybės priemonės privedė prie pačių masiškiausių protesto akcijų Lietuvoje per paskutiniuosius 12 metų.

Lietuvos valdininkai, tikriausiai, mano, kad jų dabartinės nuolaidos – tai didelis kompromisas iš valdžios pusės. Taip rodo, kaip jie nutolę nuo tikrovės.

Lietuvos valdžia eilinės krizinės situacijos metu rodo, jau tapusia jos vizitine kortele, savo kvailystę. Lietuvoje visiems yra akivaizdžios rugpjūčio 10 politinio sprogimo priežastys, bet Lietuvos ministrai vis vieną bando įpinti sąmokslo teoriją bei išorės priešų intrigas.

Taip, Lietuvos VRM vadovė Agnė Bilotaitė protestus įvardija kaip antivalstybinę veiklą ir susieja neramumus prie Seimo su neramumais ant rytinės šalies sienos, kur vietiniai gyventojai, siekiant neleisti apgyvendinti savo žemėje migrantus iš Azijos ir Afrikos, bandė užbarikaduoti trasą. Sutapimas? Nemanau – tvirtai pareiškia Agnė Bilotaitė: tai „gerai suplanuota ir sukoordinuota akcija prieš mūsų valstybę ir hibridinio karo dalis“.

Bet kuriam normaliam žmogui šio ir kito tautos pasipiktinimo priežastys pakankamai aiškios. Vienu atveju žmonės išsigando, jog juos užrakins namuose, kur jie neturės teisės netgi apsilankyti pas gydytoją ir nueiti nusipirkti duonos. Kitu atveju -  jog į jų ramius merdinčius vienkiemius užveš tūkstančius kitataučių, apie kuriuos sostinės žiniasklaida rašo visokias baisenybes, kad ateiviai atsisako skiepytis ir lengvinasi į jiems išduotus termosus su maistu.

Valdantiems konservatoriams grubia propaganda naikinti nepasitenkinimą – tai tas pats kaip benzinu gesinti gaisrą.

Lietuviškas protestas valdančiam režimui yra pavojingesnis, negu gali pasirodyti iš pirmo žvilgsnio. Pagrindinė „landsbergistų“ problema –tame, jog jis nemarginalinis. Tai yra grynai ne apačios protestas: jei būtų taip, jis būtų užsiplėkęs ir užgesęs, kaip ir visi  skaitlingi „antikovidiniai maištai“ Europoje.

Tačiau už demonstrantų slepiasi opozicinės parlamento partijos, kurios išnaudoja žmonių nepasitenkinimą kovoje už valdžią su konservatoriais. Atitinkamai pas protestą atsiranda resursai ir politinė priedanga. Rugpjūčio 10 akcijos metu, pavyzdžiui, opozicijos deputatai pravedė mitinguojančius į Seimo pastatą.

Paskutiniais mėnesiais „landsbergistai“ jam kasė duobę, siekdami padaryti sekančiu Lietuvos prezidentu dėdulės Landsbergio „karališkąjį Anūką“ – URM vadovą Gabrielių Landsbergį. Dėl to norėjo atimti iš Nausėdos teisę   atstovauti Lietuvą Europos Sąjungoje: šia funkciją perduoti ministrei pirmininkei Ingridai Šimonytei, o vėliau jos vieton pastatyti Landsbergį, kuris Briuselyje apauga reikalingo lygio ryšiais ir galės drąsiai pretenduoti į pirmąjį postą valstybėje.

Todėl veikiančiam prezidentui išimtinai naudingas konservatorių vyriausybės diskreditavimas per masinius protestus. Idealiu atveju Nausėda netgi galės paleisti parlamentą ir paskirti priešlaikinius rinkimus. O tai ypatingai svarbu, už vandenyno sėdintys Vilniaus kuratoriai tokiam scenarijui neprieštaraus. Juk Lietuvos užsienio politika,  bet kokiu atveju, pakeitus vienas sistemines jėgas į kitas, principingai nepakis  - vadinasi, galima išleisti garą, pakeičiant tą patį į tą patį.

Opozicinės partijos parlamente jau pradėjo kelti visos tautos streiko temą. Aktyviai bandoma į protestą įtraukti profesines sąjungas.  Galutinai neišnaudotas migracinis šokas: sekančią po riaušių dieną Vilniaus centre, Rūdininkų stovykloje arabai pradėjo maištauti iš naujo.

Lietuviškam protestui įsibėgėti padeda fenomenali valdančiųjų konservatorių kvailystė, kurie paskutiniais mėnesiais tiesiog skrido į krizę ant tos kvailystės sparnų. Be to, dideliai daugumai sisteminių Lietuvos politikų įsibėgėjanti krizė yra naudinga, iš išorės valdantiems centrams Briuselyje ir Vašingtone ji nėra kritiška.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 6 — id: `scraped:rubaltic_lt:b0565ac8fbd9566b`

**Title:** «Maidanas» Vilniuje: Lietuva pasiekė socialinio sprogimo ribą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvoje prasidėjo protestai su gausiausiais dalyvių skaičiais  nuo 2009 metų pasaulinės ekonomikos krizės laikų. Tiesiogine žmonių nepasitenkinimo priežastimi įvardinami nauji Lietuvos valdžios sanitariniai epidemiologiniai suvaržymai, bet akivaizdu, jog protestų masiškumą užtikrino visa konservatorių vyriausybės veikla. Per pusmetį, būdami valdžioje, „landsbergistai“ sužlugdė kovą su antrąją COVID-19 banga, dėl užsienio politikos numojo ranka į vidaus situaciją ir savo geopolitinio avantiūrizmo dėka privedė Lietuvą iki karinio konflikto pasienyje ribos. Už tai jiems užtarnautai šaukia „Lauk!“

«Pagal policijos paskaičiavimus susirinko 4500 – 5000 žmonių. Dabartiniu momentu jokių incidentų užfiksuota nebuvo. Atrodo, kažkam tai pasidarė bloga, iškvietė greitąją“, - apie rugpjūčio 10 protesto akciją prie Lietuvos Seimo sako Vilniaus apygardos policijos pareigūnas.

Keletas tūkstančių protestuojančių – labai didelis skaičius nepertraukiamos migracijos dešimtmečiais ištuštėjusiai Lietuvai, kurios gyventojų daugumą sudaro senyvo amžiaus žmonės. Paskutinį kartą tokio masto protesto akcijos Lietuvoje buvo 2009 metų sausyje, kada tik Vilniuje atėjo mitinguoti 7 tūkstančiai gyventojų.

Tada sprogimą išprovokavo pasaulinė finansų krizė, atėmusi iš Lietuvos šeštadalį BVP bei konservatorių vyriausybės sprendimas išeiti iš krizės apkarpant socialines programas, drastiškos ekonomijos gyventojams sąskaita ir iš viso „užveržiant diržus“.

Priminsime, kad praėjusių metų pabaigoje Lietuva pagal New York Times versiją užėmė pirmąją vietą pasaulyje ir pagal Europos Sąjungos versiją pirmąją vietą Europoje pagal koronaviruso plitimo koeficientą 100 tūkstančių gyventojų. Operatyvaus ES vidaus sienų uždarymo dėka laimėtas laikas pasiruošti antrajai pandemijos bangai, buvo prarastas.

Pasodinusi Lietuvą į visišką „lokdauną“ ir uždraudusi lietuviams viską, netgi apsilankymą parduotuvėse, „landsbergistų“ vyriausybė grižo prie savo mėgstamos geopolitikos. Kova su pandemija taip pat buvo pašvęsta jai.

Taip, Lietuva tapo vienintelė šalimi pasaulyje, kuri oficialiai atsisakė nuo rusiškos vakcinos dėl ideologinių sumetimų. Šalies ministrė pirmininkė Ingrida Šimonytė pareiškė, jog Lietuva – europietiškos ir transatlantinės partnerystės dalis, todėl pirks sąjungininkų  pagamintas vakcinas; kas liečia „Sputnik V“, jis - grėsmė žmonijai, ir Putinas jį naudoja kaip hibridinį ginklą, o pačius Rusijos gyventojus juo neskiepija.

Jei Lietuvos valdžia su infekcija susidorotu efektingiau, į šį Šimonytės pareiškimą galima būtų nekreipti dėmesio. Bet, atsižvelgiant į Lietuvos pasaulio ir Europos  antirekordus, vyriausybės vadovės pasisakymai įsiliejo į bendrąją Lietuvos valstybės fenomenalaus neveiksnumo kanvą.

Naujuose apribojimuose, konkrečiai numatoma atsisakyti teikti medicinos pagalbą neskiepytiems nuo koronaviruso ir iš jų atimti bedarbystės pašalpa. Tapusi jau firmine, Šimonytės vyriausybės kvailystė pasireiškė ir čia:  konservatoriai elementariai nenumatė, jog toks drastiškumas gali pasireikšti žmonių nepasitenkinimu.

Mitingo Vilniuje organizatoriai lygina jį su Maidanu ir netgi su Vilniaus televizijos bokšto gynyba 1991 m. sausio mėnesio 13 d.                                                     „Tada [sausio 13], nesėkmės atveju, grėsė tik gyventi toliau kaip gyvenus Sovietų Sąjungoje, okupuotiems, be nepriklausomos valstybės; dabar, nesėkmės ir pasyvumo atveju, gresia gyventi naujo, paties tikriausio apartheido sąlygomis, nebe teisinėje valstybėje nebe kaip piliečiams, kur bet kurią akimirką gali nutikti bet kas, nebėra nė regimybės žmogaus teisių, negalioja nei LR Konstitucija, nei jokios tarptautinės teisinės normos ir įsipareigojimai“, - rašo rugpjūčio 10 organizatorė, Vilniaus Gedimino technikos universiteto docentė Nida Vasiliauskaitė, reikalaudama parlamento paleidimo ir vyriausybės atsistatydinimo.

Tokie epochiniai palyginimai Lietuvos vyriausybei – grėsmingas signalas. Kaip ir priešiškas mitinguojančių nusiteikimas žurnalistų atžvilgiu, jų nenoras bendrauti su valdžiai pavaldžia žiniasklaida: jūs galite tik valdžią palaikyti, o mūsų žodžius jūs vis vien iškraipysite.

Akivaizdu, jog nauji epidemiologiniai apribojimai – tai tik paskutinis lašas ir protestų katalizatorius.

Kuo per tuos mėnesius pasižymėjo Lietuva?  Atsidūrė ES  bedarbystės lygio  lyderių trejetuke,  tapo COVID-19 plitimo pasaulio ir Europos lyderiu, po konflikto su Minsku, konfliktas su Maskva, o dar ir su Kinija, migracijos krizė į krizę su Baltarusija.

Atrodė, jog rami taikinga šalis Lietuva, mieguista, nieko nevyksta, o atidžiau pažvelgus, pasirodo, kad Lietuvos visuomenė paskutinį pusmetį patiria šoką po šoko. Šokas dėl viruso plitimo mastų, šokas dėl apribojimų, šokas dėl kitataučių invazijos, kuris papildomai vos netampa kariniu konfliktu pasienyje su kaimynine Baltarusijos Respublika.

Lietuvos vadovų veiksmai migracijos krizės metu – tai tikra Kvailystės Odė. Ir taip jie veikia visur, savo neveiksnumu artindami  Lietuvos valdančio režimo teisėtumo krizę.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 7 — id: `scraped:rubaltic_lt:671374afcb43d037`

**Title:** TOP-5 Lietuvos kvailysčių migracinės krizės metu

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos valdžia dvejus migracinės krizės mėnesius elgėsi kaip višta nukirsta galva, lakstanti po kiemą. Savo elgesiu ji parodė fatalų nesugebėjimą valdyti krizės sąlygomis, o iš jų antikrizinių sprendimų kvatojosi visi stebėtojai. Analitinis portalas RuBaltic sudarė kvailysčių, kurias per praėjusią savaitę padarė Lietuvos vadovybė, reitingą.

5 vietą

Migrantų įkurdinimas slapta nuo vietinių gyventojų

Po to, kai vietiniai gyventojai, protestuodami prieš neprašytų „svečių“ iš Azijos ir Afrikos įkurdinimą, pradėjo mitinguoti ir blokuoti kelius, Lietuvos valdžia nesugalvojo nieko gudresnio, kaip užslaptinti migrantų buvimo vietas. Arabus ir afrikiečius susigalvojo pervežinėti į laikino įkurdinimo stovyklas naktimis, slepiant nuo vaizdo įrašų kamerų bei gyventojų.

Lietuvos valdžia tikėjosi nuslėpti nuo vietinių gyventojų ištisą naują rajono centrą, kartu su tuo, atsižvelgiant į šalies dydį, pakankamai stambų. Tikimybė, jog lietuviai tokį arabų miestą ne aptiks, buvo maždaug tokia pati, kaip ir tikimybė, jog pasiseks jame sulaikyti arabus.

Tai yra lygi nuliui.

4 vieta

Užuominos apie vietinių gyventojų nelojalumą

Apėmusios Lietuvos pietryčius panikos dėl svetimšalių invazijos sąlygomis šalies vadovybė susigalvojo aiškinti natūralų gyventojų pasipiktinimą jų nelojalumu ir antivalstybine veikla.

„Šie veiksmai yra gerai organizuoti. Kaip žinia, proteste dalyvaujančių žmonių didžioji dalis buvo ne vietos gyventojai, tai buvo ne bendruomenės atstovai. Gerai suplanuota, gerai suorganizuota akcija prieš valstybę“, – pareiškė Lietuvos Vidaus reikalų ministrė Agnė Bilotaitė apie vietinių gyventojų bandymus blokuoti kelius ir neleista pas save sunkvežimių su arabais.

Nežiūrint į akivaizdų tokių spėlionių kvailumą, jos iki šiol vyrauja. Kaip Lietuvos lenkų lyderis Valdemaras Tomaševskis nesiteisintu, jog jo partija jokių mitingų ne organizavo, jam vis viena primena Georgijaus juostelę gegužės 9 ir kartoja, jog Lietuvos lenkai gerbia Putiną ir Lukašenką labiau nei Lietuvą.

Įdomu, kodėl?

3 vieta

Siūlymas atsisakyti sankcijų Baltarusijai

Rugpjūčio pradžioje panika dėl migrantų skaičiaus padidėjimo iki tūkstančių ir užvilkinto laukimo Vilniuje Europos Sąjungos reakcijos pasiekė tokį mastą, jog Lietuvos vadovai pradėjo siūlyti tai, ko anksčiau nebuvo įmanoma įsivaizduoti. Taip, Užsienio reikalų ministras Gabrielius Landsbergis, pažadėjo, kad Lietuva ir ES neįves naujų sankcijų Minskui, jei Baltarusija sustabdys migracinį srautą. «Tam tikras dialogas [su Minsku] yra vedamas, ir mes pasakėme, jog nei Lietuva, nei Europos Sąjunga nesiūlys naujų sankcijų [Baltarusijai], jei nelegalių migrantų srautas sustos“ – patvirtino URM vadovas.

Pasirodo, Lietuva veda derybas su Lukašenkos vyriausybe, apie kurios neteisėtumą ji jau metai įtikinėja visą pasaulį, teisėtu Baltarusijos atstovu laikydami išskirtinai tik Svetlaną Tichonouskają. Pasirodo, Lietuvos vadovybė sugeba atsižadėti principų, ir Lietuvos nepalenkiama užsienio politika, ne tokia jau nepalenkiama, jei į ją kaip reikiant paspausti.

Šiuo metu oficialus Vilnius apskritai ir URM vadovas atskirai bando gelbėti reputaciją: Baltarusijai žada „pragariškas sankcijas“, Lukašenkos veiksmus įvardina valstybiniu terorizmu, netgi grasina

Batkai ant pykčio nusišaldyti ausis: užblokuoti baltarusiškų trąšų tranzitą, kuris sudaro pagrindinį Klaipėdos uosto ir „Lietuvos geležinkelio“ pajamų šaltinį (dar viena kvailystė, verta vietos šiame reitinge).

Bet žodis ne žvirblis, išlėks – nepagausi.

2 vieta

Pinigai migrantams už sugrįžimą

Kad greičiau atsikratyti migrantų, Lietuvos valdžia sugalvojo jiems mokėti pinigus už išvykimą iš Baltijos kranto į savo gimtinę. „Oro uoste sėdant į lėktuvą šiems asmenims bus įteikiama 300 eurų dydžio grynais vienkartinė parama“ – pažadėjo Lietuvos VRM Migracijos departamento direktorė Evelina Gudzinskaitė.

Verslo schema, kaip ir viskas kas genialu, paprasta: atskridai, pasirodei, kad čia tu esi, gavai 300 eurų, išskridai. Jei iš ten skristi loukosteriais, o atgal – Lietuvos sąskaita, išloši. Jei Lietuva neduoda pinigų arba duoda mažiau nei 300 eurų, galima pasilikti palapinių miestelyje, nusilengvinti į vietinių gyventojų termosus ir maištauti.

Toliau – gryna aritmetika: migrantų skaičių per mėnesį dauginam į 300 eurų ir gauname greitį, kurio iki cento bus išsemtas Lietuvos biudžetas. Biudžetas, kuriame ir be to nelabai kas: netgi tvorą atsitverti nuo Baltarusijos statys kreditu, o spygliuotą vielą tvorai gavo iš Estijos ir Ukrainos kaip humanitarinę pagalbą.

1 vieta

Perėjimas prie smurto

Paskutiniu metu Minskas sprendė Lietuvos kovos su Lukašenka ir veiksmų, nukreiptų į Baltarusijos opozicionierių palaikymą diskreditacijos klausimą tarptautinėje arenoje. Vilnius siekė tarptautinio tribunolo Baltarusijai steigimo, kuriame teisiamaisiais turi būti visa Baltarusijos valdžia.

Tarptautinis Lietuvos aktyvumas šiuo klausimu buvo grindžiamas kova už žmogaus teises Baltarusijoje. Atitinkamai, reikėjo pademonstruoti Vakarams, jog Lietuva ir žmogaus teisės – diametraliai priešingi dalykai, Lietuvos politikai – apsišaukėliai žmogaus teisių gynimo judėjime, ir   žmogaus teisių gynimo ideologija jiems svetima.

Migracijos krizė šį klausimą išsprendė.

Dabar į visas lietuviškas tiradas apie nusikaltimus asmenybei Baltarusijoje bus atsakoma sakramentaliu „jūs arba kryželį nusiimkite, arba trumpikes apsimaukite“. Todėl kad smurtą pabėgėlių atžvilgiu Vilnius pateisina lygiai tais pačiais argumentais, kuriais prieš metus Lukašenka teisino protesto akcijų išvaikymą.

Baltarusija šį argumentą jau naudoja, bet jei tik ji viena. Jungtinių Tautų organizacija (JTO), Tarptautinis Raudonasis kryžius – visi jie pasmerkė Lietuvos pasieniečių žiaurumą pabėgėlių atžvilgiu.

Sugebėjęs Vakarus atkreipti dėmesį į problemą, Vilnius atkreipė dėmesį ir į jos sprendimo priemones. Dabar, atsakydami įkyrius Lietuvos bandymus atkreipti dėmesį į savo geopolitinį aktyvumą kalbomis apie kovą už žmogaus teises sąjungininkai visada galės nusikratyti lietuvių klausimu: „Jūs juokaujat?“

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 8 — id: `scraped:rubaltic_lt:862f79feb9537bde`

**Title:** Šalin rankas nuo pabėgelių: Lietuva pateko į Lukašenkos spąstus

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuva jėga nuslopino neramumus, kurie kilo pabėgelių stovykloje. Minios išvaikymui specialios pajėgos panaudojo vandens patranką ir ašarines dujas. Lietuvos Vidaus reikalų ministerija (VRM) oficialiai leido naudoti prieš pabėgelius smurto veiksmus, gaudyti juos po miškus su šunimis ir prievarta gražinti į Baltarusiją. Tai, kad kilo stambaus masto migrantų krizė, galima laikyti Baltarusijos prezidento Aleksandro Lukašenkos politiniu triumfu: jis išmušė iš Vilniaus rankų žmogaus teisių gynimo kortą ir tuo pačiu visai sumenkino lietuviškos diplomatijos pastangas įsteigti tarptautinį tribunolą Baltarusijos valdžiai teisti. Šiame tribunole pirmuoju smuiku būtų griežusi Lietuva ir jos priglausti Baltarusijos opozicijos veikėjai.

,,Lietuvos policija panaudojo ašarines dujas ir vandens patranką, siekdama išvaikyti migrantų minias, kurie ėmė maištauti dėl blogų salygų stovykloje, įrengtoje Rūdninkų kaime. Pabėgeliai kalba, kas jų tėvynėje byvo geriau, ir atsisako nuo maisto, kuris jiems atvežamas, atsisako gerti vandenį, kurio spalva abejotina. Tačiau pagrindine neramumų priežastimi tapo palapinių skendimas vandenyje po liūties, taip pareiškė vietos valdžios atstovai“-pranešė televizijos kanalas Euronews.

Naujienos perpasakojimas šiuo atveju ne mažiau svarbus, nei pati naujiena. Iš vienos pusės, Euronews sutinka su Lietuva, kad migracijos krizės priežastis-,,Lukašenkos režimo provokacija“. Ir tuo pačiu Europos Sąjungos informacinis ruporas teigia, kad pabėgeliai tai nekaltos aukos, ir tikrai nepritaria Lietuvai, kurios jėgos struktūrų atstovai leido ašarinies dujas ir galinga vandens srove talžė tuos nekaltus žmones.

Ir toks svarbios nuomonės pasireiškimas-tai Vilniui tikrai nepalankios pozicijos išraiška.

Didelis straipsnis apie padėtį Baltarusijos-Lietuvos pasienyje pasirodė Vakarų spaudoje-stambiame New York Times reportaže-ir šioje publikacijoje dėstoma būten apie masinius žmogaus teisių pažeidimus. Liberalios ideologijos vedlys nuoširdžiai užjaučia pabėgelius, kurie ,,įtraukti į geopolitinę kovą“, ir smerkia Lietuvą, kurios atstovai vis žiauriai elgiasi su migrantais.

Apie ,,vis labiau žiauriai“ buvo parašyta gerokai iki tol, kol Vilnius nusprendė jėga deportuoti arabus atgal į Baltarusiją, leido naudoti prieš migrantus smurto veiksmus, ir įsakė pasieniečiams gaudyti juos po miškus su šunimis.

Lietuva virš 30 metų parazitavo tarptautinės politikos sferoje, kurdama aukos įvaizį ir vis reikalavo pagalbos iš sąjungininkų. Labai įvairios pagalbos. Ir štai dabar New York Times jau skambina pavojaus varpais ir įrodo, kad šiuo metu pagalbos reikia nelegaliems migrantams. Lietuvai gi paramos nereikia. Prieš Lietuvą reikia imtis konkrečių priemonių, nes oficialūs šalies pareigūnai itin agresyviai elgiasi su nekaltomis aukomis bei atvirai pažeidžia žmogaus teises.

Toks požiūris į Lietuvą bus tol, kol Vilnius naudos nuožmaus smurto priemones. Ir kol kas tokia pozicija dominuoja, nes ir Lietuvos VRM leido pabėgelių atžvilgiu naudoti fizinę jėgą ir psichologinio spaudimo priemones, ir net šalies prezidentas mano, kad reikia praplėsti Lietuvos kariuomenės įgaliojimus ir nukreipti karinius dalinius prieš pabėgelius, ir jau realiai vykdoma priverstinė arabų deportacija. Dar gerai, kad kol kas ne užplombuotuose vagonuose, kaip Stalino laikais.

Vakaruose dominuojanti liberali ideologija tokų metodų negali pateisinti. Tuo labiau –kai tokie metodai taikomi migrantų-musulmonų atžvilgiu, kurie dėl savo ,,nukentėjusių rolės“-privilegijuota socialinė grupė. Rytų Europos valstybei mušti ir pjudyti šunimis pabėgelius-tai tas pats , kaip išvaikyti gėjų paradą. Viskas, po tokių įvykių Vakarų šalių požiūriu tokia valstybė nebėra demokratinė, nebėra europietiška, ir nebėra toje pačioje ,,vertybių sistemoje“.

Ir tada visiškai aišku, kad tokia dabartinė situacija Baltarusijos-Lietuvos pasienyje: tai tikra taip vadinamo ,,paskutinio Europos diktatoriaus“ pergalė.

Tarp kitko, Lietuvos užsienio reikalų ministerija ir šalies prezidento administracija turėjo tikrai napaleoniškus planus dėl žmogaus teisių gynimo temos panaudojimo. Užtenka paminėti, kad lietuviškoji diplomatija paskutinių mėnesių bėgyje įvairiais būdais prastūminėjo idėją įkurti tarptautinį tribunolą Baltarusijos klausimu: pagal analogiją tarptautinio tribunolo buvusios Jugoslavijos klausimais. Lukašenka turėjo sėsti į teisiamujų suolą: jei ne tiesiogiai, tai bent už akių. Pagrindiniais kaltinimo liudininkais turėjo būti Lietuvos valdžios atstovai ir jos priglausti politiniai emigrantai iš Baltarusijos.

Dėl to Lukašenka ir nukreipė galingą migrantų srautą į Lietuvą. Ne į Latviją, kuri pirmoji iš Baltijos kraštų de facto nutraukė diplomatinius ryšius su Minsko, po to, kai atvirai paniekino Baltarusijos vėliavą. Ne į Lenkiją, kuri vaidino pagrindinį vaidmenį nuožmių ir maištingų baltarusiškų protesto akcijų organizavime. Tačiau į Lietuvą, kuri pristato save pasauliui kaip pagrindinę kovotoją už žmogaus teises Baltarusijoje.

Visiems, kas žino situaciją šioje šalyje, tai supranta, kad Lietuva ir žmogaus teisės-tai visai nesuderinami dalykai. Jei konkrečiai, tai užtenka pažvelgti į Algirdo Paleckio ir Jurijaus Melio persekiojimų istorijas. Aišku, kad tai tikrai liūdnos istorijos, tačiau JAV ir Europos Sąjungos su šiomis istorijomis paveikti neišeina. Reikia tūkstančių atvejų, kurie parodytų tikrajį Lietuvos valdžios veikėjų apsimetėlių veidą.

Ir Minske rado patikimą būdą.

Lietuvos įtakingieji veikėjai, sprendžiant pagal jų pirminę reakciją, suprato, koks gi yra gudrus Lukašenkos planas. Tačiau ilgai imituoti humanizmą bei vaidinti pažangius europiečius negalėjo.

Ir pateko į Batkos paspęstus spąstus.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 9 — id: `scraped:rubaltic_lt:72d46a80298e4496`

**Title:** Europos Sąjunga atlygins Lietuvai tuo pačiu už atsisakymą priimti  pabėgelius

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Sekmadienį, rupjūčio 1 dieną, Baltarusijos –Lietuvos sieną peržengė rekordinis nelegalių migrantų skaičius: beveik 300 žmonių. Jų apgyvendinimo galimybės pasieniečių patalpose jau išsemtos. Lietuva planuoja kreiptis į kitas Europos Sąjungos šalis su prašymu priimti dalį pabėgelių. Kitaip tariant, ši Pabaltijo respublika kreipsis į sąjungininkus palaikyti juos šios krizės akivaizdoje, nors 2015 metais Lietyvos valdžia atsisakė būti solidari, kai Vakarų Europa prašė ,,naujuosius europouečius“ priglausti dalį pabėgelių.

Kaip jau tapo įprasta, į Lietuvos teritoriją iš Baltarusijos pastoviai patenka virš šimto nelegalių migrantų per dieną. Nesunku paskaičiuoti, kad jau rudenį bendras jų skaičius viršys 10 tūkstančių-faktiškai atitiks nedidelio Lietuvos miesto skaičių. Tačiau aiškėja, kad tai tėra optimistinis scenarijus.

Aišku tokia tendencija tikrai grėsminga. Ir matosi kad puikiai veikia pabėgelių siuntimo per Baltaruiją į Europos Sąjungos erdvę schema. Lietuvos sieną ir toliau galima lengvai pereiti, o štai deportuoti nekviestus svečius kaip tik gana sudėtinga.

Irako ir Sirijos gyventojai mato, kad atsirado geras variantas patekti į Europos Sąjungą. Ir kodėl gi tuo nepasinaudojus, kol šita niša dar neužsidarė ?

Nuo šiol atvykti į Baltarusijos sostinę bus galima ne tik iš Bagdado-migrantai jau gali skristi iš Basros, Suleimanijos ir Erbilio.Tai labai populiarūs maršutai, nes bilietai lėktuvų reisams iš Basros į Minską išpirkti iki rugpjūčio 26 dienos, iš Erbilio-iki spalio pabaigos. Nesunku suvokti, koks gi irakiečių ,,turistų“ tikslas...

Vilniaus bandymai vesti savarankiškas darybas su Iraku buvo nesėkmingi. Ir štai dabar derybų estafetę perima Europos Sąjunga. Lietuvos premjerė Ingrida Šimonytė neslepia, kad Pabaltijo respublikos valdžia turi daug vilčių dėl europietiškos diplomatijos veiksmų, tikisi gerų rezultatų. Tačiau ir europietiška diplomatija kol kol nėra efektyvi.

Atsakyme į tiesioginę užklausą, gautą iš Europos komisijos, Irako Konsultacinė nacionalinio saugumo taryba pareiškė, kad Lietuvos politikų tvirtinimai, jog daugumas nelegalių migrantų, kurie atvyksta į Lietuvos teritoriją, tai Irako piliečiai, yra nepagristi. Be to, nepagristi ir tvirtinimai, kad nelegalus pabėgelių siuntimo į Europos Sąjungą verslas yra tiesiogiai susijęs su Irako tarptautiniais oro uostais.

Ir štai pabandykime įsivaizduoti, kad tūkstančiai pabėgelių bus deportuoti. Šie pabėgeliai-tai daugumoje jauni energingi vyrai, kurie daug kuo rizikavo. Ir jie pralaimėjo. Jų asmenyje šalies valdžia gaus potencialius nusikaltėlius ir teroristus. Dėl to Vilniui nereikia turėti didesnių vilčių, kad jiems pavyktų vykdyti masinę pabėgelių deportaciją į Iraką.

Tuo tarpu Lietuvos pasienio apsaugos tarnyba jau skelbia pavojaus signalą: jiems tiesiog jau nėra kur talpinti vis atvykstančius pabėgelius. ,,Visos pasienio užkardos šiuo metu užpildytos, ir šeštadienį bei sekmadienį teko spręsti klausimus dėl tų žmonių apgyvendinimo, matome kad kol kas nėra kur perkelti tų žmonių iš pasienio užkardų, dar bandėme visaip spręsti šiuos klausimus, tačiau šiuo metu mųsų galimybės jau išsemtos „-perspėjo tarnybos vadovas Rustamas Liubajevas.

Kai pabėgelių srauto neįmanoma sutalpinti pasienio užkardose-tada teks nukreipti nelegalių migrantų srautus į Lietuvos gilumą. Tokie procesai sukels vietinių gyventojų nepasitenkinimą, ir jie rengs vis naujas ( ir vis labiau radikalias) protesto akcijas.

Europos Sąjunga (ES) turi vesti derybas su Iraku. ES turi paskirti 500 milijonų eurų sienos su Baltarusija įtvirtinimui. Ir galu gale, Europos Sąjunga turi priglausti dalį pabėgelių, kurie šiuo metu yra susitelkę Lietuvoje. Šį paskutinį norą Šimonytė paviešino po susitikimo su ES komisare vidaus reikalų klausimais Ilva Johanson.

Tačiau lieka atviras klausimas-kas gi realiai padės Lietuvai ? Ar Latvija ir Estija vadovausis ,,Baltijos vienybės“ principu ir priims pas save nelegalius migrantus ? Ar sutiks juos priglausti Lenkija ? Visose paminėtose šalyse pabėgelių iš Afrikos ir Artimujų Rytų pasirodymas bus sutiktas nepalankiai ir kirs per valdančiujų partijų populiarymą.

,,Vokietija 2015 metais priėmė vir milijono pabėgelių faktiškai per kelias savaites, ir tikėjosi kad bus galima paskirstyti juos po visą Europos Sąjungą. Tačiau praėjo jau nemažai laiko, o tie pabėgeliai randasi Vokietijoje, kitos šalys neparodė aiškaus solidarumo vokiečių atžvilgiu.

Ypač tokios Rytų Europos šalys, kaip Lietuva, atsisakė ištiesti pagalbos ranką Vokietijai, ir vis teigė, neva tai jūsų problemos“-pažymėjo vokiečių politologas Aleksandras Raras.

Tada Lietuvos buvo prašoma priimti tik 710 pabėgelių. Tačiau šį prasymą dabar jau buvusi šalies prezidentė Dalia Grybauskaitė pavadino ,,neteisingu ir nereikalingu pabėgelių krizės sprendimo būdu“. Tuometinis premjeras Algirdas Butkevičius tada pareiškė, kad Lietuva gali priimti tik 30-40 migrantų. Ar tai ne pasityčiojimo ženklas didžiulės pabėgelių krizės akivaizdoje, kai nelegalių migrantų minios užplūdo Vokietiją, Italiją, Graikiją ir kai kurias kitas šalis?

Šiuo metu Lietuva atsidūrė padėtyje šalies, kuri imasi aktyviai įrodinėti, jog nelegalios migracijos problemas turi solidariai spręsti visa Europos Sąjunga. Vokiečiai tuo tarpu turi pilną teisę paklausti: kur buvo jūsų solidarumas 2015 metais, kai Grybauskaitė pareiškė: ,,visos Afrikos į Europą neperkelsime ?“

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 10 — id: `scraped:rubaltic_lt:7e28bbcccf9ffae5`

**Title:** Pasiruošę atsisakyti sankcijų: Lukašenka iškovojo pirmąją pergalę prieš Lietuvą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos URM pareiškė, jog Lietuva ir Europos Sąjunga yra pasiruošę atsisakyti naujų sankcijų Baltarusijai, jei Minskas sustabdys nelegalių migrantų srautą. Tai proveržis: patikinimus, jog principinė Lietuvos užsienio politika nesudaro jokių sandorių bei nesiekia jokių kompromisų su „diktatoriais“ paneigė pati Lietuvą. Baltarusijos Prezidentas Aleksandras Lukašenka gali švęsti pergalę ir už ją dėkoti Vilniaus sąjungininkams iš NATO ir ES, kurie, paprasčiausiai nepastebėjo Lietuvos nacionalinės nelaimės

«Tam tikras dialogas [su Minsku] yra vedamas, ir mes pasakėme, jog nei Lietuva, nei Europos Sąjunga nesiūlys naujų sankcijų [Baltarusijai], jei nelegalių migrantų srautas sustos“ – praeitą savaitę pareiškė Lietuvos užsienio reikalų ministras Gabrielius Landsbergis.

Šiame pareiškime ne viena sensacija, o iš karto kelios. Visų pirma, Vilnius veda dialogą su Minsku.

Tuo metu, kažkur tai pusiaukelėje iš Vašingtono į Vilnių, sunkiai atsiduso Baltarusijos „išrinktas prezidentas“ Svetlana Tichanovskaja, kurią Lietuva, atkakliausiai visų pasaulyje, vadino vieninteliu teisėtu respublikos ir jos liaudies atstovu. Būtent kaip tokia, Tichanovskaja buvo vežama į Vašingtoną piršlybų naujajai JAV administracijai ir netgi buvo išgautas jos susitikimas su Džozefu Baidenu

Bet Vilniaus geopolitinės fantazijos - tai viena, o negailestinga tikrovė – kita. Fantazijose Lietuva jau davė Baltarusijai savo prezidentą, kaimyninei šaliai tapo vyresniuoju broliu, draugu, „demokratizacijos“ mokytoju, paėmė ją savo globon

Tikrovėje prisieina turėti reikalą su „paskutiniuoju Europos diktatoriumi“

Antra, Landsbergio pasiūlymo esmė: atsisakymas nuo naujų sankcijų Baltarusijai mainais už migracinės krizės nutraukimą

Tai proveržis.

Lietuvos nepalenkiama užsienio politika, kaip pasirodė, dar kaip lenkiasi, jei į ją kaip reikiant paspausti.

Netgi geopolitinis mesianizmas ir patologinė praktika kištis į kitų šalių vidaus reikalus bei savo valia spręsti, kas ten yra teisėtas ar neteisėtas, atsiduria antrame plane, kai pačioje Lietuvoje kyla vidaus stabilumo klausimas.

URM vadovas graudus ne tuo, kad jis ramiai siūlo derėtis „diktatoriui“, apie santykių su kuriuo neįmanomumą jo žinyba jau beveik metus intensyviai įtikinėja visą pasaulį.

Netgi už tai juokingesnis Lietuvos politikams tradicinis apeliavimas į Europos Sąjungą.

Landsbergis kartoja prastą įprotį, už kurį jo kolegas postsovietinėje erdvėje paskelbia apsišaukėliais ir puola juos su kumščiais. Jis kalba ne vienos Lietuvos vardu, bet visos ES vardu. „Nei Lietuva, nei Europos Sąjunga nebesiūlys naujų sankcijų“

Ar Europos Sąjunga įgaliojo Lietuvos užsienio reikalų ministrą kalbėti jos vardu?

Ar Europos Sąjunga delegavo Gabrielių Landsbergį vesti derybas su Lukašenka visos Europos Bendrijos vardu? Ar Europos Sąjunga kažką tai sakė, jog sureguliavus migracinę krizę Lietuvoje, naujų sankcijų Baltarusijai nebus?

Dabartiniu metu šis komiškas lietuviškas apsišaukimas atrodo ypatingai juokingu.

Kartu su tuo, kad paskutinių savaičių bėgyje Lietuvos vadovybė įnirtingai signalizavo Briuseliui ir pagrindinėms Europos sostinėms: Lukašenkos veiksmai – tai iššūkis visai Europai, o ne vien tik Lietuvai. Beveik vienu metu su URM vadovo persilaužiamuoju pareiškimu tokį eilinį signalą pasiuntė ir Lietuvos prezidentas Gitanas Nausėda.

Europos sotinėse, atsižvelgiant į tai, jog nebuvo reakcijos, signalai iš Vilniaus buvo suvokti kaip eilinis periferijos inkštimas siekiant atkreipti dėmesį į save ir gauti naują pagalbos porciją iš išorės. Na juos, tegul tvarkosi patys! 2015 metai Vokietija priėmė milijoną nelegalų, o tie su dvejais tūkstančiais susitvarkyti negali? Tame ir reikalas, jog negali. Visos Europos mastelyje Lietuvos migraciniai srautai - tai juokingi skaičiai, bet mažos šalies su neefektyvia valstybe mastelyje jie – nacionalinė katastrofa

„Skausmo slenkstį“ Lietuva peržengė 2700 nelegalių migrantų skaičiumi. Po to skaičiaus šalyje prasidėjo protestai, ir netgi vietinių gyventojų maištai prieš pabėgėlių priėmimą, o esant perspektyvai rudenį priimti dar dešimtis tūkstančių arabų ir afrikiečių, jau nesirodo fantastišku tokie apokalipsiniai scenarijai, kaip Vilniaus šturmas pabėgėliais ir vyriausybės nuvertimas liaudies sukilimu.

Jei sprogimas įvyks, šaliai taip pat teks žūti vienatvėje. Kadangi nesuprantama, kuriame kritimo bedugnėn etape į Lietuvos negandus rimtai pažvelgs Vakarai. Ir ar iš viso pažvelgs. Ir ar bus suteikta pagalba, jei vis tik pažvelgs. Lietuvos politikai gerokai degradavo dėl įpročio galvoti, jog, jei kas atsitiks, didieji dėdės iš Briuselio, Berlyno, Londono ir Vašingtono iš karto puls šluostyti snarglius ir barti kaimyną-chuliganą, kad tas neskriaustų mūsų vaikelių. Iš čia ir kraštutinis Vilniaus neatsakingumo laipsnis. Kaip vidaus politikoje, taip ir užsienio politikoje.

Šiuo atžvilgiu Lukašenkos veiksmai turi pedagoginį pobūdį

Tad reikia įjungti smegenis ir patiems būti atsakingiems už savo likimą.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 11 — id: `scraped:rubaltic_lt:55f0812bbf601305`

**Title:** Pabaltijo kraštai vykdo hibridinę diplomatiją Lukašenkos vyriausybės atžvilgiu

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Talinas atsisakė siusti į Baltarusiją nauja ambasadoriu, kuris buvo paskirtas į šį postą liepos 6 d. Estijos prezidentės Kersti Kaljulaid nutarimu. Taigi, ir trečia Pabaltijo respublika pasuko Latvijo ir Lietuvos pasirinktu keliu, šios šalys jau prieš kurį laiką iki minimumo sumažino savo diplomatų skaičių Minske.

,,Siusti naują ambasadorių nėra tikslinga, nes Estija neskaito Lukašenkos teisėtu valstybės vadovu, tuo tarpu įgaliojimo raštų teikimas gali būti Estijos pozicijos pasikeitimo ženklas šiuo klausimu“-pareiškė šios Pabaltijo respublikos užsienio reikalų ministrė Eva Marija Limets.

Keletą dienų prieš tai Estijoje įvyko idomus įvykis: prezidentė Kersti Kaljulaid atšaukė ambasadirę Baltarudsijoje Merike Kokajev ir pasirašė įsaką dėl jos įpėdinio skyrimo- Jakas Lensmentas paskirtas oficialiu Estijos atsovu. Lieka atviras klausimas: ar jis tikrai vyks į Minską ir įteiks įgaliojimo raštus Lukašenkai ?

,,Reikia suprasti, kad oficialus įgaliojimo raštų įteikimas yra pagrindas ambasadoriui gyventi šalyje-be konkrečios akreditacijos diplomatas išvis negali būti tam tikroje šalyje.Taigi tam, kad ambasadorius galėtų oficialiai atstovauti Estijąm, jis turi užsienio valstybės vadovui įteikti įgaliojimo raštus, kuriuos gavo iš savo šalies prezidento“-tokią poziciją išsakė Užsienio reikalų ministerijos Ryšių su visuomene departamento direktorė Ari Lemmik.

Pats Lensmento paskyrimas į šį postą buvo sutiktas prieštaringai.Buvęs už reikalų ministras ir aktyvus opozicinės partijos ,,Tėvynė“ narys Urmas Reinsalu šį žingsnį pavadino kvailyste ir palankumo ženklu ,,nežmogiškam Lukašenkos režimui“. Kitas buvęs užsienio reikslų žinybos vadovas -Urmas Paetas- atkreipė dėmesį i tariamas ,,hibridrines atakas“, kurias anto jo, Baltarusija vykdo prieš Lietuvą. Ir štai, kaip esant tokiai situacijai, siusti naują ambasadorių į Minską...?

Taigi keletą dienų Estijos politinio elito gretose vyko diskusijos. Ir galų gale, ši Pabaltijo šalis nesiryžo eiti prieš ,,generalinę liniją“, kurią vykdo Vakarai. Jakas Lensmentas į Baltarusiją nevyks. Tik vykdys ,,virtualaus ambasadoriaus“ funkcijas. Tokiu pat būdu dirba JAV ambasadorė Baltarusijoje Džiuli Fišer, kuri nėra įleidžiama į šią šalį ( tad tenka sedėti Lietuvoje ir ,,laukti režimo žlugimo“).

Vienas iš pavyzdžių: niekas netrukde Baltarusijos ambasadoriui Viačiaslavui Kačialovui gegužės 9-ają nešti gėles Taline prie Bronzinio kareivio ir duoti interviu Estijos valstybinei televizijai. Jam, kaip oficialiam Minsko atstovui šalyje, buvo įteikta protesto nota dėl Baltarusijos opozicijos veikėjo Romano Protasevičiaus sulaikymo.

Kačianovo statusas tarsi niekam nėkėlė jokių klausimų ir abejonių. Tačiau dabar klausimai gali iškilti. Jei Estijos ambasadorius realiai nebūna Minske, tai kodėl Baltarusijos ambasadorius vis dar dirba Taline??

Tuo tarpu Rygai ir Vilniui šie klausimai jau nekyla. Lietuvos diplomatinė atstovybė Baltarusijoje buvo sumažinta iki visiško minimumo atsakant į ,,nedraugiškas iniciatyvas, kuriomis keliamas priešiškumas“. Ir atsakymo laukti ilgai nereikėjo. Lietuvos užsienio reikalų žinyba kreipėsi į Baltarusijos diplomatus palikti ambasadoje tik vieną darbuotoją, kuris vykdys konsulines funkcijas( neskaitant trijų techninių darbuotojų).

Su Latvija Baltarusijos santykiai pašlijo gegužės 24 dieną.

Latvijos ambasadoriui Einarui Semaniui buvo pasiūlyta palikti Minską per 24 valandas, kiti diplomatai gavo truputį daugiau laiko palikti šalį. Leista palikti vieną techninį ambasados darbuotoją, kuris prižiūrėtų pastatą. Po to Latvija atsakė tokiomis pat priemonėmis.

Ir štai-ir Estiją pasiekė ši banga. Buvusi šalies ambasadorė Minske pasitraukia, o naujasis gauna nurodymą sedėti namuose. Tokiu būdu lygioje vietoje ši Pabaltijo valstybė faktiškai nutraukia diplomatinius ryšius su Baltarusija, kurie per stebuklą buvo išlaikyti po Lukašenkos perrinkimo.

,,Oficiali mūsų ambasadoriaus darbo pradžia, kuri numatyta nuo rugsėjo mėnesio, priklausys nuo to, kaip įvertinsime padėtį Baltarusijoje,-pareiškė Estijos užsienio reikalų ministrė.-Mes aišku tarsimės ir su mūsų partneriais bei sąjungininkais, kurie laikosi pozicijos koordinuoti veiksmus ir laikytis vieningos linijos šiuo klausimu“.

Taigi, ministrės žodžiai iš dalies pagrindžia hipotezę, kad Estija atsisakė siusti ambasadorių į Minską, nes patyrė spaudimą iš užsienio jėgų.

Nors toks žingsnis atrodytų logiškas.

Jakas Lensmentas nuo šio bus ,,Šredingerio ambasadorius“, kurio padėtis tikrai prieštaringa. Iš vienos pusės-jis oficialus Estijos atstovas Baltarusijoje, iš kitos-jis tokios šalies atstovas, kurios pozicija yra neigti Baltarusijos valdžios teisėtumą.

Matome visą ,,hibridinės diplomatijos“ grožį.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 12 — id: `scraped:rubaltic_lt:855c781dc5cfd6d7`

**Title:** Naujas Lukašenko ginklas: Lietuva išsigando branduolinių medžiagų kontrabandos iš Baltarusijos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Baltarusija gali panaudoti neteisėtą branduolinių medžiagų gabenimą kaip naują ,,hibridinės agresijos“ būdą prieš Lietuvą. Apie tai pareiškė šios Pabaltijo šalies užsienio reikalų ministras Gabrielius Landsbergis. Beveik neabejotina, kad kalba eina apie atominio kuro kontrabandą-to kuro, kurį Rusijos bendrovė TVELL tiekia Baltarusijije veikiančiai Astravo atominei elektrinei. Konkrečių argumentų, kurie pagristų šią versiją, Landsbergis nepateikia-pateikiamas tik įsitikinimas, kad kovoje su Vilniumi Lukašenko gali panaudoti pačius nuožmiausius metodus.

Apie Baltarusijos prezidento planus Lietuvos užsienio reikalų ministras pasakojo savo partijos tarybos posėdyje. Jo teigimu, Lukašenko kelią grėsmę kaimynams dėl radioktyvių medžiagų ir narkotikų kontrabandos. Visa tai-,,hibridinio karo“ būdai.

,,Prieš pusantro mėnesio panaudotas vienas tokių būdų- tai pagrobtas lektuvas, kurį privertė nusileisti Minske. Vėliau atsirado kitas būdas-migrantų banga. Jis ( Lukašenko-RuBaltic.ru pastaba) gali panaudoti ir kitas –naujas priemones“.

Su narkotikais viskas aišku. Artimieji Rytai-vienas iš pasauliniių narkotikų prekybos centrų, ir būtent iš šio regiono į Baltarusiją atvyksta žmonės, kurie po to nelegaliai kerta Lietuvos sieną. Bet prie ko čia radioktyvios medžiagos?

Reikalas tame, kad Baltarusijoje jau veikia Astravo atominė elektrinė. Rusija aprūpina ją atominiu kuru.

Ko gero, Lansbergis mano, kad šias brangias ir pavojingas medžiagas Lukašenko nukreips į Lietuvą.

Tokiu atveju Landsbergiui prireiks 1990-ujų metų metodinių knygelių bei kitos propagandinės medžiagos. Tada būtent Rusija buvo skaitoma neteisėtos branduoluolinių medžiagų apyvartos pagrindinių šaltiniu. Leidinys The New York Times tada rašė : Jei jūs norite pirkti reaktorių, prisodrintą uraną, taip vadinamą ,,sunkujį vandenį“, arba net kai kurias branduolinių užtaisų detales, tai jūs galite tai įsigyti Maskvoje. „

Tie kaltinimai turėjo konkretų pagrindą. Jelcino laikų Rusijoje tikrai buvo grobstomos radioktyvios medžiagos. Štai 1993 metais buvo užfiksuoti du grobstymo atvejai Šiaurės laivyne-dingo urano rinkiniai. Panašūs atvejai nustatyti ,,Majako“ gamykloje Ozerske, gamykloje ,,Luč“ Maskovos srityje, Rusijos moksliniame eksperimentinės fizikos institute.

Vakaruose daug triukšmo sukėlė taip vadinamas Miuncheno skandalas, kada lėktuvo reise iš Maskvos vokiečiai aptiko plutonį, tinkamą ginklų gamybai.

Nuo to laiko Rusija, bendradarbiaudama su užsienio partneriais, vykdė daug praktinių projektų, skirtų objektų, susijusių su branduolinių medžiagų laikymu, apsauga.

Ir neteisėta apyvarta tokiomis medžiagomis dabar griežtai užkardoma. Bendrovė TVELL( vienas iš ,,Rosatom“ padalinių) aprūpina branduoliniu kuru 75 reaktorius visame pasaulyje, bendrovės veikla prižiūrima Tarptautinės atominės energijos agentūros, ir niekas nekaltina šios agentūros tuo, kad ji sipnai kontroliuoja radioktyvių medžiagų apyvartą.

Tiesa, yra daug klausimų dėl Armėnijos-būtent ši šalis yra konkretus neteisėtos apyvartos radioktyviomis medžiagomis šaltinis. Tai pabrėžiama kasmetiėse Tarptautinės atominės energijos agentūros ataskaitose. Beje, Armėnijos kontrabandos veikėjus dažnai sulaiko pasienyje su Gruzija.

Azerbaidžanas laikosi pozicijos, kad tai yra Armėnijos valstybinės politikos dalis, o uranas gabenamas iš Mecamorsko atominės elektrinės, kurį gauna uraną iš Rusijos.

«,,Žinome, kad paskutiniu metu viena iš pagrindinių tarptautinio terorizmo ir ekstremizmo sričių- tai branduolinė grėsmė. Ir pastaruoju metu šiuos metodus įvaldę radikalios grupuotės grasina vykdyti radioktyvaus užkrėtimo aktus, bei pradėti atominį karą, panaudojant tikrus atominius užtaisus, tame tarpe įvairius tokių užtaisų tipus. Pažymėtina, kad radioktyvių medžiagų kontrabanda iš Armėnijos kontroliuojama valstybiniu lygiu. Iš kur gaunamos šios medžiagos ? Manau, kad jų šaltinis-Mecamorsko atominė elektrinė“-teigia Azerbaidžano parlamento deputatas Arzu Nagijevas.

Iš esmės tokius pat kaltinimus Lietuva pateikia Baltarusijai, ir tai nuskambėjo iš užsienio reikalų ministro lūpų.

Tačiau ar yra konkretūs duomenys, kurie tai patvirtintų ? ,,Duomenys“ labai migloti: Lukašenko-tikras blogis. Jis smaugia spaudos laisvę, jis žaloja ir uždaro į kalėjimus nekaltus žmones, jis ant savo pečių gabena pabėgelius iki Baltarusijos-Lietuvos sienos. O štai dabar kiekvienam nelegaliam migrantui dar bus išduodamas ir urano gabaliukas. Praeis keli mėnesiai ir Lietuva-o greitai ir visas Pabaltijo regionas-bus užkrėsta teritorija.

,,Hibridinis priešas“ bus pilnai apginkluotas sunaikinti Lietuvą Batkos nurodymu.

Kai Donbase vyko karas, jo pradžioje ukrauniečiai buvo gasdinami ,,Putino koviniais buriatais“. Tačiau jie ir iš toli nepritinka prie ,,Lušenkos radioktyvių arabų“, kurie užgrobs Lietuvą! Labiau klastingo užpuolimo plano parengti neįmanoma.

Bet žvelgiant iš oficialaus lietuviškos propagandos taško viskas logiška.

Užsienio reikalų ministro senelis Vytautas Landsbergis pabrėžia, kad tikrosios Astravo atominės elekrinės įsteigimo priežastis-nubausti Lietuvą.

Ir dėl šios idėjos Putinas nepagailėjo milijardų dolerių. Ir tada aišku, kad rusiško atominio kuro grobstymai jį nelabai nuliūdins. O kam jaudintis, jei tos medžiagos bus panaudotos prieš nemėgstama Pabaltijo respubliką ?

Tačiau iš šių nerimtų naujienų Baltarusijos vadovybei reikia padaryti rimtas išvadas.

Atominių medžiagų kontrolė Baltarusijoje turi būti vykdoma labai atsakingai, taip, kad grobstymo galimybė būtų arti nulio. Nes kitu atveju Vilnius turės labai rimtus kozyrius.

Lietuva pasinaudos tuo, kad pareikalauti naujų sankcijų prieš Baltarusiją ir primesti Europai astravo atominės elektrinės baikotą.

Aišku, kad tada ir ,,Rosatom“ gaus nemenką kritikos porciją. Rusijos valstybinį koncerną apkaltins aplaidumu talkinant Baltarusijos ,,terorizmui“.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 13 — id: `scraped:rubaltic_lt:3964133b50aa6c67`

**Title:** Mokslininkas: ,,Lietuva gauna solidžius pinigus už aviatranzitą į Kaliningradą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Gegužės mėnesį Lietuvoje priimtas sprendimasuždaryti oro erdvę lėktuvams, kurie skrenda iš Baltarusijos, iš naujo pakėlė klausimus apie Kaliningrado tranzitą bei apie Kaliningrado srities transporto saugumą. Rusijos anklavas ir toliau yra priklausomas nuo Lenkijos bei Lietuvos veiksmų. Apie tai, kaip paskutiniais metais klostėsi Rusijos-Lietuvos ir Rusijos-Lenkijos santykiai, pasakoja Rusijos ūkio ir valstybės tarnybos akademijos prie Rusijos prezidento administrasticijos šiaurės-vakarų filialo direktorius, praeityje buvęs Kaliningrado srities vice-gubernatorius Michailas Pliuchinas.

-Gerbiamas Pliuchinai, gegužės mėnesį pas mus kai kuriuose sluoksniuose buvo kilusi panika kad Lietuva uždarys oro erdvę Kaliningrado sričiai, lėktuvams, kurie skrenda per Baltarusijos teritoriją iš Kalingrado į pagrindinę Rusijos dalį. Jūs ilgą laiką dirbote valstybės tarnyboje kaip atsakingas regiono valdžios struktūrų darbuotojas. Ar kada nors ši tema buvo rimtai svarstoma, buvo tokie aptarimai, kad Lietuva gali uždaryti oro erdvę Kaliningrado sričiai ?

Visiškai niekad to nebuvo. Klausykite, lietuviai –labai pragmatiški žmonės, ir sugebantys gerai skaičiuoti. Štai eina geležinkelio transportas-jie gauna iš to pastovią tranzito dalį. Be abejo, jie gauna ir iš lėktuvų skrydžius virš šalies teritorijos: skrenda lėktuvas –ir jie gauna tranzito rentą. Bijau suklysti, tačiau kai mes tais dalykais užsiėmėm, tai atsiskaitymai kažkodėl vyko Šveicarijos frankais, kodėl taip buvo, nežinau.

Skrydžiai į mūsų teritoriją per Lietuvos oro erdvę-jokių klausimų dėl to niekada neiškildavo.

Yra buvę periodai, kai Lietuvos partneriai perlenkdavo lazdą su tranzito ribojimais.

Šiuo atveju ,,ribojimus“ įvardiju su kabutėmis.

Ir iš karto mūsų valdžios struktūrų atstovai tada teigdavo : ,,Kolegos, o pas jus ten kažkas iš kažkur vyksta ? Ar jūs iš kažkur kažką gaunate ?“

Kai pas tave už nugaros valstybė, tu visada jautiesi užtikrintas. Dėl to aš nemanau, kad jiems galėjo ateiti į galvą konkreti mintis apriboti skrydžius į Kalingradą.

Bet kuriuo atveju, ar saugi Kaliningrado sritis, žvelgiant iš transporto saugumo taško? Jei bus kokie netikėtumai, ar galima skristi į Rusiją per neutralių vandenų zoną ? Jei kada realiai kiltu tokia būtinybė ?

-Mūsų kariniai transporto lektuvai jau skrenda tokiais koridoriais, kurie neįeina i jokios valstybės jurisdikciją.

Gerai, galima ir taip! Juk tokiu būdu gali skristi ir civiliniai lėktuvai. Ir kam nuo to geriau ?

Gaunasi, kad skrydžiai ilgesni, reikia daugiau kuro, laiko atžvilgiu viskas užtrunka-ir tai jau visai kiti santykiai. Juk bet koks veiksmas, šalia to, kad jis lemia atoveiksmį, iššaukia ir tam tikrą santykį atžvilgiu to, kuris to veiksmo ėmėsi.

Tai būtų nesąmoningas dalykas, ir tikrai faktiškai atsisuktų prieš tą, kas tokiį sprendimą priimtų.

Šalia to, pre kitų problemų prisidėtų dar viena, buitiniame lygyje: kažkuo lėktuvas trukdė, arba dar kažkas.

-Mums tenka užsiimti tokiais samprotavimais dėl to, kad mūsų santykiuose su Lenkija ir Lietuva dominuoja negatyvus požiūris. Tačiau mes galime pasiūlyti lenkams ir lietuviams pozityvų požiūrį. Kaip jie į tai reaguos-jų reikalas, tačiau pasiūlyti mes galime. Modeliuojame situaciją: Jūsų akademijos platformoje vyksta apskritas stalas, į kurį sutinka atvykti Varmijos-Mozūrijos vaivadijos, Gdansko, Klaipėdos savivaldybių atstovai, ir mūsų- Kaliningrado srities atstovai, ir mes turime pateikti įvairius siūlymus dėl geranoriškos kaimynystės vystymo. Tokius siūlymus, kurie juos sudomintų. Ką galime pasiūlyti, kad juos tai realiai sudomintų, ir jie atsitrauktų nuo begalinių pokalbių apie istoriją, Antrajį pasaulinį karą ir panašiai ?

Man idomi lenkų patirtis municipalinės sandaros srityje. Aišku, kad lenkų savivaldoje irgi yra problemų, tačiau jie arčiau prie tokio modelio, kuris buvo suformuotas, kai buvo vykdomi įvairūs savivaldos reformos etapai. Pas juos matome įdomų pasiskyrstymą tarp federalinių, regioninių ir savivaldos įgaliojimų. Man atrodė, kad tai gana subalnsuotas modelis.

Dėl ko tai dėstau ? Juk mes svarstėme tokius klausimus ir su Lenkijos, ir su Lietuvos partneriais ir keitėmės patirtimi. Jiems buvo ne visai aišku, kodėl kai kurie dalykai egzistuoja pas mus, o mums buvo ne visai aišku, kodėl pas juos vyksta kai kurie procesai, ir viso to nagrinėjimas yra naudingas.

Kas liečia istorijos sritį. Komisija skirta spręsti sudėtingus Rusijos-Lietuvos istorijos klausimus, išleido knygą: Rusijos požiūris į problemą, Lenkijos požiūris į problemą. Ir praųom, ieškantis tegu randa, klausantis tegu išgirsta, ir pratęsiu-skaitantis perskaito. Tegul būna taip.

Patinka jums tai, ar nepatinka, bet tai buvo Tarybų Sąjunga, kurios indėlis toks-dėl Pergalės savo gyvybes paaukojo 28 milijonai žmonių.

Ir štai prasideda: ne 28, bet 27 milijonai. Klausykite, tai mūsų žmonės, ir tais apskaičiavimais mes užsiimsime patys.

Kai buvo vietinis pasienio judėjimas tarp valstybių, tai kas liečia Kaliningrado sritį, jei žvalgiant iš ekonominio taško, tai buvo reiškinys į minusą, o būtent lenkams tai buvo naudinga.

-Bet šią tvarką panaikino lenkai.

Tikrai taip !Mūsų valstybė, suprasdama projekto ekonominius kaštus Kalingradfo sričiai, vis tik ėmėsi vykkdyti projektą. Nes tai buvo naujas mexchsanizmas, kurį Rusija ir Europos Sąjunga galėjo sėkmingai vystyti. Ar suprantate, kokia tai patirtis ? tai davė postūmį vystytis labiau atsilikusioms Lenkijos sritims. Aš tikrai nemėgstu visko matuotis piniginiais santykiais, tačiau visa tai vyko mūsų sąskaita.

-Aišku kad taip.

-Štai ir viskas. Mes duodavom lenkams tuos pinigus, nes ši pasienio tvarka buvo susijusi su kelionėmis, su draugiškų ryšių užmezgimu, su apsikeitimu patirtimi. Ir vis tk kas gavosi su tuo pasienio judėjimu:, kas galų gale nukentėjo nuo jo uždraudimo ? Mes ėmėmė daugiau orientuotis į save, į savo rinką, daugiau gaminti įvairias vietines prekes, skristi į pagrindinę Rusijos teritoriją ir ten poilsiauti. Na? Štai ir viskas.

O Lenkijos pusė, kuri suprato taip, kad jau ėmė skaityti turizmo iš Kaliningrado srautą ilgalaikiu trendu, pastatė pasienio zonoje prekybos centrus. Ir kas gavosi ? Patys nuo savo politikos nukentėjo.

Buvo toks atvejis, kai mes su delegacija vykome į Lenkiją, į Varšuvą, ir reikėjo stengtis gerinti tarpusavio santykius, kurie eilinį kartą atsidūrė konkrečioje krizės būsenoje. Kiek pamenu, tada buvo mėsos skandalas, tiksliai detalių dabar nepamenu.

Ir tada kaip tada mes vykome, ir mums uždavė įvairius klausimus, ir mes palaipsniui ir radome išeitį iš tos sudėtingos padėties

Po to Rusijos-Lenkijos santykiai tapo stabilūs. Į Lenkiją vyko ir Rusijos prezidentas, Varšuvoje susitiko su šalies vadovais ir tai buvo normalūs santykiai. Manau, kad ir dabar tokią patirtį galime prisiminti ir taikyti, jei iš abiejų pusių bus gera valia ir noras formuoti normalius santykius.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 14 — id: `scraped:rubaltic_lt:16d80d86fc29afd4`

**Title:** Baltarusija randa fašistinius ,,skeletus“ Lietuvos eksprezidento spintoje

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Baltarusijos generalinis prokuroras Andrejus Švedas pareiškė, kad jo vadovaujama žinyba ir toliau planuoja apklausti buusį Lietuvos prezidentą Valdą Adamkų kaip liudininką baudžiomojoje byloje dėl genocido. Konkretų prašymas iš Minsko išsiustas dar gegužės pradžioje, tačiau atsakymo nėra iki šiol. Šios Pabaltijo šalies valdžia ir buvęs prezidentas atsidūrė labai nepatogioje padėtyje.

Baudžiamoji byla del Baltarusijos gyventojų genocido faktų Didžiojo Tėvynės karo metu pradėta šių metų balandžio mėnesį. ,,Byla pradėta siekiant istorinio teisingumo, dėl istorijos ,,baltujų dėmių“ atskleidimo, šalies konstitucinės santvarkos ir nacionalinio saugumo sustiprinimo“-tokius argumentus pateikė Andrejus Švedas, ir pridūrė, kad Minskas kels klausimus dėl karinių nusikaltėlių išdavimo bei atviro teisminio proceso jų atžvilgiu.

Tuo pačiu Baltarusijos Generalinė prokuratūra atsakė į klausimą: kodėl ji šio tyrimo ėmėsi tik dabar? Anksčiau tokio pobūdzio baudžiamosiios bylos neįėjo i Aleksandro Lukašenkos ,,daugiaplanės“ politikos rėmus. Reikalauti išduoti dar gyvus nacistinius nusikaltėlius tektų kreiptis į JAV bei Europos Sąjungos šalis, su kuriais Lukašenka ilgą laiką stengėsi palaikyti draugiškus santykius.

Kai kurie asmenys, artimai bendradarbiavę su okupacine vokiečių administracija, net labai pakilo ir užėmė aukštus postus potarybinėse Lietuvoje, Latvijoje ir Estijoje. Vieną iš jų Andrejus Švedas panoro apklausti genocido byloje.

Dėmesio centre atsidūrė Valdas Adamkus-tai buves Lietuvos prezidentas, šešiolikos universitetų garbės daktaras, gavęs daug Lietuvos ir įvairių užsienio šalių apdovanojimų. Lietuvos gyventojai du kartus jį išrinko į aukščiausią valstybinį postą, ir kas svarbu-antra kartą jis buvo išrinktas po rezidento Rolando Pakso nušalinimo. Tuomet buvo teigiama-neva labai reikalingas ryškus lyderis. Visa tai būtų puiku, tačiau Adamkaus biografijoje yra kai kurie nemalonūs faktai.

,,Kauno 9 forte buvo sušaudyta virš 5000 žydų iš Austrijos ir Čekijos. Juos čia atvežė neva paskiepyti-ir žydai ėjo į duobes atsiraitoję rankoves dėl skiepų. Lietuviai taip puikiai darbavosi, kad Impulevičiaus bataliones buvo nusiustas į Baltarusiją-ir ten bataliono kariai nužudė 15 000 žydų. Vokiečiai buvo labai patenkinti“-pasakojo Rūta Vanagaitė savo knygoje ,,Mūsiškiai“.

Ko gero Adamkus galėtų papildyti Vanagaitės pasakojimą vertingais asmeniniais liudijimais. Tačiau apie Impulevičiaus nusikaltimus savo memuaruose jis nerašė. Buvusio Lietuvos prezidento oficialioje biografijoje karo periodas apsiriboja dviem sakiniais: ,,Antrojo pasaulinio karo metu jis dalyvavo judėjime už Lietuvos nepriklausomybę. Valdas Adamkus kartu su savo tėvais pabėgo į Vokietiją 1944 metų liepą“.

Apie įvykius prieš šį pabėgimą Baltarusijos teisėsaugos atstovai panoro sužinoti išsamiau. Ir gegužės mėnesį jie kreipėsi į Lietuvos generalinę prokuratūrą su prašymu apklausti Adamkų.

,,Nacizmas ir genocidas neturi senaties termino, ir asmenys( prisidėję pe karinių nusikaltimų vykdymo-RuBaltic.ru pastaba), turi būti nubausti. Dėl to mes rengiame konkrečius duomenis, kuriuos išsiusime įvairių šalių teisėsaugos žinyboms, tikėdamiesi, kad šios žinybos imsis tam tikrų procesinių priemonių ir apklaus dar gyvus nacistinius nusikaltėlius. Toliau yra pasirinkimas : arba teisti juos tose šalyse, arba išduoti mums, arba perduoti bylų svarstymą tarptautiniam tribunolui“-tokią poziciją visai neseniai išsakė generalinis prokuroras A.Švedas.

Apklausti buvusį prezidentą pagal ,,neligitimaus režimo“ užklausą tiesiog neįmanoma. Tačiau visiskška atsiriboti nuo Minsko žvelgiant iš viešujų ryšių linijos vėlgi nenaudinga. Jei Adamkus be nuodėmių, tai kodėl gi jis negali pateikti Švedui atsakymų į konkrečius klausimus, kurie domina Baltarusijos prokuratūrą? Aišku, būtų gerai publikuoti apklausos stenogramą, tikrai tokia stenograma bus plačiai skatoma ir Lietuvoje, ir Baltarusijoje.

Kokius būtent klausimus norima užduoti Adamkui ? Generalinis prokuroras A. Švedas išvardijo klausimus neseniai duotame interviu : ar eks-prezidentass davė priesaiką fašistiniam Reichui? Ar jis savo noru įstojo į baudžiamojo SS bataliono gretas? Koks buvo jo bendravimo su ,,Minsko mėsininku“ pobūdis?

Žinoma, Adamkus gali vykdyti savo liniją, atsakydamas į klausimus. Tačiau bet kuriuo atveju jam teks prisiminti ,,tamsujį“ savo biografijos laikotarpį.

Be to, nesunku suvokti, kaip gali vystytis baudžiamosios bylos eiga. Bet kuriuo mementu buvęs Lietuvos prezidentas gali tapti įtariamuoju, o po to kaltinamuoju, gali būti nuteistas už akių.Ypač jei Baltarusijos teisėsaugos atstovai ras svarbius duomenis.

,,Liudininkų yra nemažai. Mes jau apklausėme virš keturis tūkstančius žmonių. Ir tyrimas tęsiasi.... Tai liudininkai Baltarusijos teritorijoje. Ir kitose valstybėse : tiek potarybinėje erdvėje, tiek ir dar kitose šalyse, tokių liudininkų yra nemažai. Tai jau sekantis mūsų tyrimo etapas“-pareiškė Andrejus Švedas.

Ir egzistuoja galimybė, kad kai kas iš tūkstančių liudininkų prisimena 18-metį Valdemarą Adamkevičių iš ,,Minsko mėsininko“ komandos.

Beveik nėra abejonių, kad krepimasis bus atmestas. Ir Generalinė prokuratūra tai puikiai supranta. Tačiau Švedas ir jo pavaldiniai ir nekelia uždavinio patraukti išgyvenusius budelius į realią baudžiamąją atsakomybę. Reikia kelti į viešumą koloborantų temą, priminti pasauliui apie tai, kokiose šalyse gyvena budeliai, tarnavę Hitleriui. Ir kas svarbu-kur jie sugebėjo iškilti ir tapti ryškiais politiniais lyderiais.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 15 — id: `scraped:rubaltic_lt:5e832a4ae0b693ae`

**Title:** Lietuva artėja suskaldymo „maro“ metu

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Pačiame COVID-19 pandemijos ir jos sukeltos ekonominės krizės įkarštyje Lietuvai gresia dar ir politinis suskaldymas. Tarp šalies prezidento Gitano Nausėdos ir „landsbergiečių“ klano, kurio dalyviai reklamuoja prezidento pareigoms jaunąjį atstovą Gebrielių, užsivirė žymus konfliktas. Artimiausiu metu šitas konfliktas gali tapti plačiai žinomas visuomenei.

Per pastarąsias dvi savaites tarp Daukanto aikštės (Nausėdos administracijos būstinės) ir Lietuvos vyriausybės, kuriai vadovauja Landsbergių partija, įsižiebė keli konfliktai.

„Landsbergiečiai“ siekia atimti iš Nausėdos pagrindinio asmens, kuris atstovauja šaliai tarptautinėje arenoje, vaidmenį. Pavyzdžiui, per Europos Sąjungos šalių-dalyvių viršūnių susitikimą Lietuvai turi atstovauti ne šalies prezidentas bet vyriausybės vadovas.

Ministrė-pirmininkė Ingrida Šimonytė – parlamentinės-prezidentinės respublikos pagrindinis oficialus atstovas.

Žinoma, Nausėda nenori prarasti nei savo vietos, nei galimybių, kurias ji suteikia. Todėl jis pradeda kontrataką. Net Europos tarybos klausymu Lietuvos prezidentas kategoriškai prieštarauja prieš bet kokius pakeitimus.

Taip, Vokietijai Europos taryboje atstovauja ne šalies prezidentas, o Angela Merkel. Bet Gitanas Nausėda – ne Vokietijos, o Lietuvos prezidentas. Lietuvoje prezidentą renka gyventojai, jis išreiškia tautos valią ir yra atsakingas už saugumo ir užsienio politikos klausymus. Tik jis ir niekas kitas gali skelbti Lietuvos poziciją Prancūzijos, Vokietijos ir kitų šalių-sąjungininkių lyderiams.

Anot RuBaltic.Ru šaltinius Vilniuje, tarp jaunesniojo Lansbergio ir Nausėdos jau įsižiebė pilnavertis konfliktas.

Linkevičius – pagrindinis Nausėdos taktikos elementas, kad blokuotis su kitomis politinėmis grupėmis prieš „landsbergiečių“ ataką. Šios grupės – po rudens rinkimų sudarę opoziciją centro kairės partijos.

Palyginus dabartinės konservatorių vyriausybės šnipštus kovoje prieš koronavirusą, buvusios „valstiečių“ vyriausybės nesėkmės jau pradeda atrodyti kaip laimėjimai. Atitinkamai, buvusio ministro-pirmininko Sauliaus Skvernelio reitingas auga, o dabartinės vyriausybės vadovės Šimonytės atvirkščiai krenta.

Šiomis aplinkybėmis šalies prezidentas akivaizdžiai remia „buvusius“.

Pastarasis pavyzdys: griežtas Nausėdos atsakymas sveikatos apsaugos ministrui, kuris pristabdė lietuvių vakcinaciją su švedų-britų gamintu preparatu AstraZeneca, nors prieš kelias valandas jis pažadėjo pasiskiepyti šia vakcina pats. Valstybės vadovas pasipiktino, kad atsisakymas naudoti reikšmingą masinei vakcinacijai preparatą pakirsta gyventojų pasitikimą vaistu ir stato į pavojų visą vakcinacijos kampaniją.

Galime net neabejoti, kad sveikatos apsaugos ministerijai pasiūlius naudoti vakcinacijai AstraZeneca Nausėda tuoj pat pasakytų, kad vyriausybė atmeta ES stambiausių ekspertų rekomendacijas ir visiškai nevertina eilinių gyventojų gyvybes.

Bet kuriuo atveju, tokia vyriausybė gal jeigu ir neturėtų atsistatydinti, bent jau turėtų patylėti apie savo įgaliojimų praplatinimą. Apie atstovavimą Lietuvai Europos Taryboje, tarkim, ir panašiai.

Nenuostabu, kad esant tokioms „malonybėms“ vyriausybės ir prezidentūros santykiai įsitempė. Visų pirma – prezidentūros santykiai su kilniausiuoju dėdulės Landsbergio anūku, kurio politinės karjeros vardan ir yra suskaldomas jėgų išsidėstymas tarp Lietuvos vykdomosios valdžios organų.

Naujo ambasadoriaus JAV kandidatūra tampa vis rimtesniu įtampos šaltiniu. Konservatoriai, žinoma, norėtų, kad tokias strategiškai svarbias Lietuvos atstovo pareigas eitų jų bendramintis. Žygimantas Pavilėnis, tarkim, ar dar koks nors diplomatijos genijus. Todėl jiems savaime aišku yra tai, kad ambasadorių turi rinktis URM vadovas o ne prezidentas.

Sanitarinės, epidemiologinės, socialinės bei ekonominės krizių aplinkybėmis tai bus ypač pikantiška. Lietuvos politikai niekaip negali įveikti pandemijos, baltarusių tranzitas akyse pabėga iš rankų, Latvija ir Estija nenori apginti Lietuvą nuo Astravo AE elektros, vakarų sąjungininkai pasibjaurina išgirsdami Lietuvos klyksmus Baltarusijos, Ukrainos ir kitais klausimais...

Paskutinis dalykas, likęs įvykdyti Lietuvos politinei klasei, kad parodyti savo visišką neveiksnumą – pradėti viešą ir garsų riejimąsi.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 16 — id: `scraped:rubaltic_lt:1093133dfe6ad5d2`

**Title:** Krovinių vežėjai bėga iš Lietuvos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Per metus Lietuva prarado daugiau už šimtą krovinius gabenančių įmonių. Lietuvos krovinių autovežėjų traukimosi grėsmė buvo suvokta dar 2019 metais, bet nuo tų laikų lietuvių valdžia nepadarė nieko, kad užkirsti jai kelią. Dėl to dabar Lietuva gali prarasti 1,6% nuo savo BVP, o šalies vadovybė vėl parodė savo visišką nepajėgumą susivaldyti su iškilusia problema.

2019 metų rudenį Sauliaus Skvernelio vyriausybė nusprendė padidinti tolimųjų reisų vairuotojų algos koeficientą iki 1,65 (skaičiuojant nuo minimaliosios mėnesinės algos). Sprendimas, žinoma, džiuginantis, deja tuoj pat paaiškėjo, kad jis irsta lietuvių krovinių vežimo automobiliais rinką.

Pasirodė, kad logistikos įmonių savininkai neturi tiek lėšų, kad padidinti vairuotojų uždarbio mokesčius ir tuo pačiu metu nepridirbti nuostolių. Jų verslas susidūrė su nusmukimo grėsme.

„Pagal išlaidas Lenkija – optimaliausias variantas: pati įstaiga, licencijos, išlaidos šiam daug žemesnės. Kai įmonė buvo įsteigta, ji turėjo galimybę gauti finansavimą iš pat pradžių. Čia ir mobilumo paketas: Lenkija yra geografijos atžvilgiu išsidėsčiusi daug palankiau; jeigu atsižvelgti į reikalavimą sugrįžti, bus mažiau „tuščių“ kilometrų palyginus su sugrįžimu į Lietuvą. Ir dienpinigiams nėra taikomas koeficientas. Beje, Lenkijoje yra gera konkurencija draudimo rinkoje“, - pasakodavo per posėdį Seime vienos transporto kompanijos vadovas apie Lietuvos logistikos problemas bei jų patį lengviausią sprendimo būdą.

Krovinių vežimo automobiliais rinkos situacija buvo pripažinta kaip kelianti grėsmę Lietuvos nacionaliniam saugumui, valstybinė ekonomika susidūrė su pavojumi prarasti dešimčius tūkstančių darbo vietų. Taip pat buvo pripažinta, kad problemos priežastis yra susijusi ne su vyriausybės reikalavimais algos dydžiams bet su valstybės politika. Dėl negabaus administravimo, biurokratiško vilkinimo ir nepakeliamų fiskalinių reikalavimų lietuvių vežėjams daug paprasčiau tvarkyti verslą Lenkijoje.

Problemą buvo žadama išspręsti pačiame aukštame politiniame lygyje. Ir, pagaliau, atrodo, „išsprendė“.

„Vis daugiau transporto įmonių siekia tęsti savo veiklą užsienyje, ieškodamos būdų išgyventi su minimaliomis išlaidomis. Mūsų verslas konkuruoja su vežėjais iš Lenkijos, Bulgarijos ir Rumunijos, kur sąlygos verslo vystymuisi yra daug palankesnės“, - komentuoja susiklosčiusią rinkoje situaciją Linava prezidentas Romas Ostinskas.

Lietuvos mažosios logistikos įmonės yra prie pat bankrutavimo slenksčio. „Tai paaiškinama trimis faktoriais: priemonėmis, numatytomis mobilumo pakete, praeitais metais prasidėjusia COVID-19 pandemija bei naujų mokesčių, kurie padidino spaudimą vežėjams ir pablogino konkurencijos sąlygas, taikymu“, - paaiškina šakos krizes atsiradimo priežastis Linava generalinis sekretorius Zenonas Buivydas.

Pandemiją Lietuvoje dabar apkaltins viskuo, taip pat ir automobilių transporto šakos suirimu. Bet krizė joje prasidėjo dar prieš koronavirusą. Valstybiniu mastu šita krizė buvo paskelbta dar tais laikais, kai net žodžio COVID-19 neegzistavo.

Galų gale, ne koronavirusas nulėmė tai, kad Lietuvoje verslo vystymo sąlygos yra prastesnės už Lenkiją, Bulgariją bei Rumuniją. Visai ne dėl koronaviruso Lietuvos logistika priartėjo krizės po vairuotojų uždarbio mokesčio didžio nutarimo priėmimo. Ne virusas žadėjo išspręsti problemą ir savotiškai tai padarė. Viskas tai – valstybinio administravimo sistemos padariniai.

Ji turėjo tris metus tam, kad efektyviai išspręsti problemą, kurios egzistavimą šalies valdžia viešai pripažino ir su kuria pažadėjo susitvarkyti. Kokį rezultatą turime šiandienai? Pasak Baltijos tyrimų instituto (BIRD) ir Creditreform Lietuva įmonės apskaičiavimus, dėl lietuvių transporto įmonių pasitraukimo į kitas šalis Lietuvoje išaugs bedarbystė, padidės migracija, o respublikos BVP sumažės 1,6%.

Kuo gi užsiėminėdavo Lietuvos vadovybė per pusantrų metų laikotarpį, kad išsaugoti valstybinei ekonomikai tuos 1,6% nuo BVP? O! Vdovybė buvo iš tikrųjų labai užimta. Ji darė viską, kad sulaikyti Rusiją, dėstė „Rytų partnerystės“ šalims europietiškas vertybes, keliavo po vakarų sostines su Svetlana Tichanovskaja ir siekė sankcijų taikymo Baltarusijai. Matyt, tam, kad pridėti prie bankrutavusių mažųjų logistikos įmonių dar ir „Lietuvos geležinkelius“. Kad autovežėjams būtų ne taip skriaudu ir liūdna.

Valdžia turėjo kelius mėnesius pranašumo tam, kad paruošti Lietuvą COVID-19 pandemijos rudens bangai. Tokį pranašumą nulėmė tai, kad 2020 metų pavasarį Rytų Europos šalys spėjo laiku uždaryti valstybines sienas. Ir kaip buvo panaudotas šitas pranašumas? 2020 metų pabaigai Lietuva žengė į pirmą vietą pasaulyje pagal COVID-19 užsikrėtimų skaičių šimtui tūkstančių gyventojų, ištyrė nesėkmę su vakcinacija, o dabar pratęsė karantiną dar mėnesiui.

Vilniaus kova su Astravo AE pavirto blogu anekdotu. Iš pradžių Lietuvos Seimas priligino atominės elektrinės pagamintos elektros suvartojimą valstybės išdavystei, o dabar Lietuva nepaisant savo įstatymų ją vartoja – todėl, kad nevartoti jos negali. Nepajėgia kontroliuoti energetinę erdvę nuosavoje teritorijoje.

Ką gi tokiu atveju lietuvių valdytojai laiko sėkmingais savo politikos pavyzdžiais? Pasirodymus prestižinėse tarptautiniuose renginiuose, kur jie pristato gražias Power Point prezentacijas, pasakojančias apie Lietuvos postsovietinę „laimės istoriją“, ir pačiais ryžtingais žodžiais įtikina „rusų grėsmės“ egzistavimu.

Todėl uždrausti Filipui Kirkorovui įvažiuoti į Lietuvą – jų galimybių viršūnė. Kirkorovas – jų lygis. Nors Kirkorovas yra net pažangesnis už lietuvių politikus, dėl to kad yra doresnis. Jis dorai tenkina masinį „popso“ poreikį: dainuoja su fonogramomis, šoka išsipuošęs plunksnomis ir lateksu ir nevadina savęs aukštosios kultūros atstovu.

Užtat Kirkorovo kolegos iš Lietuvos yra įsitikinę, kad tai, ką jie daro, yra valstybės valdymas, o jie patys yra valstybiniai veikėjai, kurie iš tikrųjų pajėgia susitvarkyti su sunkumais.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 17 — id: `scraped:rubaltic_lt:b448d1e4e38fb0c4`

**Title:** Lietuvos valdžia apsigėdino priešais visą šalį

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos vyriausybei švedų ir britų gamintos vakcinos Astra Zeneca atsisakymas tapo moraline kančia ir Šekspyro verta drama, kurią bet kuris žmogus galėjo stebėti gyvai. Dar kovo 16-ą, dieną, vyriausybės vadovas ir sveikatos apsaugos ministras įtikindavo lietuvius, kad Astra Zeneca yra visiškai saugi, ir tam, kad tai įrodyti, jie yra pasiryžę pasiskiepyti viešai, visų Lietuvos gyventojų akyse. Tos pačios dienos vakarą jie sustabdė vakcinos taikymą po šūktelėjimo iš ES.

„Visi šitie sprendimai [dėl Astra Zeneca naudojimo ES šalyse bei kituose pasaulio regionuose sustabdymo – RuBaltic.Ru pastaba] skamba kaip profilaktikos priemonės, bet nėra geriausias sprendimas pačiai vakcinai ir jos reputacijai. Kasdien prarandame žmonių, kurie miršta nuo COVID-19, todėl pasakyčiau, kad Astra Zeneca vakcinacijos sustabdymas atneš daugiau blogio nei naudos“, - komentavo Europos šalių atsisakymą naudoti Astra Zeneca Lietuvos ministrė-pirmininkė Ingrida Šimonytė.

Tam laikui naudoti Astra Zeneca skiepams sustojo daugiau nei 20 Europos valstybių.

Austrija, Bulgarija, Danija, Vokietija, Islandija, Airija, Italija, Ispanija, Latvija, Prancūzija ir kiti pabūgo dėl šalutinio poveikio, kurį, kaip pasirodė, sukelia Astra Zeneca.

Tokiomis aplinkybėmis Lietuvos valdžia pasirodė esanti net karštesnė švedų farmacijos patriotė nei patys švedai: Vilniuje iš paskutiniųjų įtikindavo, kad nepaisant nieko vakcinuos gyventojus skandinavų kilmės vakcina.

Šimonytės komentaras čia – esmingiausias. Lietuvos vadovybei, visų pirma, rūpėjo ne lietuvių saugumas, bet vakarų vakcinos reputacija. Vyriausybės vadovė negalėjo net sau leisti minties, kad šita vakcina iš esmės bloga ir kad nuo Astra Zeneca naudojimo teks atsisakyti.

Todėl ir vakcinacijos sustabdymas šitu preparatu iki jo šalutinio poveikio išnagrinėjimo neleistinas. Nes į tai rodys „Kremliaus propaganda“!

Tuo tarpu lietuvių valdžia, kuri pralaimėjo kovą su pandemija, vos ne vienintelė pasaulyje iš anksto atsisakė naudoti rusišką „Sputnik V“ ideologiniais sumetimais.

Respublikos URM vadovas Gabrielius Landsbergis paskelbė, kad Lietuva rinks vakcinas, besivadovaudama transatlantinio solidariškumo sumetimais – t.y. kylančių iš šalių-sąjungininkų iš NATO bei ES. Jau paminėta Ingrida Šimonytė iš vis pavadino rusišką vakciną „Putino hibridiniu ginklu“ ir pasidalino savo nuojauta, jog nuo „Sputnik V“ žmonijai „nėra jokios naudos“.

Po tokios pozicijos skelbimo išprovokuoti trombozės sukeltą lietuvių mirštamumą po Astra Zeneca vakcinacijos būtų ne taip baisu, kaip pripažinti, kad vakarų vakcina, kurią aprobavo Vilnius, gali būti prastesnė ir pavojingesnė už rusišką. Nes net ukrainiečių prezidentas dėl „Sputnik V“ pramurmėjo kažką neaiškaus: neva, negalima vakcinuoti ukrainiečius „abejingos kokybės preparatu“, kuris neregistruotas Europos Sąjungoje. Pagrindine priežastimi atsisakyti rusiškos vakcinos buvo ne aiški ideologinė nuostata – „šalies-agresoriaus“ produkciją nenaudojame – bet tiesioginis įsakymas iš JAV ambasados Kijeve.

Latvija kartu su Estija iš vis išdavė „baltų vienybę“. Jų oficialūs atstovai patvirtino vakcinacijos rusišku preparatu galimybę tuo atveju, jei jį patvirtins Europos vaistų agentūra.

Tad tarptautinio masto skandalas dėl Astra Zeneca šalutinio poveikio Lietuvos vadovybę erzina ne tuo, kad dėl jo beveik žlugo gyventojų vakcinacijos kampanija, bet tuo, kad šis skandalas diskredituoja Lietuvos antirusišką nepalenkiamumą.

Pirmiausias Vilniaus prioritetas – informacinis efektas, o ne pandemijos nugalėjimas. Todėl į skandalą buvo nuspręsta atsakyti ne vakcinacijos stabdymu, bet... propagandos kampanija. Sveikatos apsaugos ministras Arūnas Dulkys tą pačią dieną, kovo 16-ą, kai visa Europa atsisakydavo Astra Zeneca, pažadėjo atlikti parodomąją žinomų žmonių, politikų, vadovų ir pačio savęs vakcinaciją.

Nors lietuviai abejoja skiepytis Astra Zeneca ne dėl to, kad juos išgąsdino „Kremliaus propaganda“, bet todėl, kad susirūpinimą vakcinos saugumu paskelbia daugelis valstybių.

Ir sukelti šitie susirūpinimai ne „Kremliaus agentų“ griaunamąja veikla, bet daugeliu skandalų.

Be trombozės sukeltų mirčių ir kraujo krešumo problemų po anglų-švedų vakcinos naudojimo, Astra Zeneca kūrėjai išgarsėjo tuo, kad netyrinėdavo savo preparato tarp vyresnio nei 55 metų amžiaus žmonių ir iš vis tikslioms išvadoms dėl vakcinos saugumo neužtenka paskiepytų žmonių skaičiaus.

Tęsti vakcinaciją su Astra Zeneca nepaisant realybės ir tam, kad įpykdyti Rusiją su jos siūloma alternatyva, galėjo sukelti Lietuvoje pilnaverčių vakcinacijos maištų, todėl šalies politinei klasei teko kapituliuoti prieš realybę.

Kaip tai atsitinka, visi domintis galėjo pamatyti gyvai. Kovo 16 dieną Ingrida Šimonytė paskelbė savo epišką komentarą „vakcinuosime su šita vakcina į patyčia visiems priešams, kad nesugadinti jos reputacijos“. O jau vakare Sveikatos apsaugos ministerijos vadovas, kuris prieš kelias valandas žadėjo pasiskiepyti Astra Zeneca visų lietuvių akyse, pranešė apie preparato naudojimo nutraukymą.

Elgesio pokytis aiškinamas labai įmantriai. „Šiandien gavau iš Valstybinės vaistų kontrolės tarnybos (VVKT) rekomendaciją, kurios tarnyba, kaip ir kitos Europos Sąjungos valstybės, atsargumo sumetimais rekomenduoja sustabdyti vakcinavimą COVID-19 vakcina „AstraZeneca“, - papasakojo Arūnas Dulkys.

Lietuvių politikai iš proto išėjo jau seniai, bet ignoruoti tiesioginio įsakymo iš „obkomo“ nedrįso. Lietuviai gali būti dėkingi užsienio vadovybei už išgelbėtas gyvybes, kurias jų pačių vadovai buvo pasiryžę paaukoti, kad tik rusų vakcina neatrodytų patrauklesnė palyginus su vakarų analogais.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 18 — id: `scraped:rubaltic_lt:63d38a1eee6e789f`

**Title:** „Belarus“ sanatorijos vyriausiasis gydytojas: Nausėda negirdi lietuvių, o Lukašenka išgirdo

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Į sanatorijos „Belarus“ Druskininkuose (Lietuva), kuriai buvo taikytos sankcijos, problemą atkreipė dėmesį Baltarusijos prezidentas Aleksandras Lukašenka. Savo pasirodymo metu per VI Visos Baltarusijos liaudies susirinkimą jis liepė vyriausybei neatidėliotinai išspręsti šią problemą. Lietuvos prezidentas Gitanas Nausėda tuo pačiu metu renkasi ignoruoti savo tautiečių – įmonės darbuotojų – kreipinius. Apie tai analitiniam portalui RuBaltic.Ru papasakojo „Belarus“ sanatorijos vyriausiasis gydytojas Ilja Jepifanovas.

— Pone Jepifanove, pradėti mūsų pokalbį norėtųsi nuo pačio opaus klausimo – nuo finansų. „Belarus“ sanatorija daugiau nei du mėnesius veikia sankcijų spaudimo aplinkybėmis. Kiek pamenu, jos sąskaitos buvo iš dalies atblokuotos, kad darbuotojai galėtų bent gauti algą už 2020 metų gruodį. O ką daryti su sausio ir vasario mėnesių darbo užmokesčiais?

— Vasario mėnesio darbo užmokesčiai bus pradėti mokėti kovo 4 dieną. Už sausį, žinoma, darbuotojai jau turėjo gauti pinigus tačiau dėl sankcijų veikimo tai nėra įmanoma.

Parašėm krūvą laiškų skirtingoms įstaigoms: į Užsienio reikalų ir Vidaus reikalų ministerijas, tiesiai į Swedbank. Bet kol kas mūsų kreipiniai lieka be atsakymo.

Manau, jiems tiesiog nėra, ką pasakyti. Ir belieka tik ignoruoti mus.

— Atsimenu, kad kai „Belarus“ sanatorijai buvo taikytos sankcijos, tam tikri lietuvių bičiuliai rašė: o prie ko čia Lietuva dėta? Tai gi švedų banko sprendimas. Formaliai respublikos vyriausybė nėra su juo susijusi. Jus patys sau atsakėt į klausimą, ar oficialaus Vilniaus pozicija turi ryšio su sanatorijos sąskaitų blokavimu?

— Manau, kad turi. Mes juk kreipėmės į kitus bankus, domėjomės, ar galime juose atidaryti sąskaitas. Tarp jų SEB Bankas, Medicinos Bankas ir kiti. Visi šitie bankai atmetė mūsų prašymus, teigdami, jog privaloma gauti mūsų padėties – neaiškios padėties – išaiškinimą iš atitinkančių Lietuvos Respublikos valdančiųjų įstaigų.

— Anot Jūsų, su kuo susieti šitie „neaiškumai“?

— Norėčiau pabrėžti vieną itin reikšmingą dalyką, kurį visą laiką apverčia aukštyn kojomis. Europos Sąjungos sankcijos buvo taikytos Baltarusijos prezidento administracijos Vyriausiajai ūkio valdybai. „Belarus“ sanatorija niekada nepriklausė, nepriklauso šitai žinybai ir nebus įtraukta į jos sudėtį.

Dabartiniu metu pareiškėme ieškinį prieš Swedbank: sieksime, kad šitas mūsų atžvilgiu neteisėtas sprendimas būtų atšauktas teismo tvarka. Laukiame, kol pasibaigs visos biurokratinės procedūros ir prasidės bylos nagrinėjimas.

— Irgi atkreipiau dėmesį į tai, kad sanatorija priklauso Baltarusijos prezidento administracijai, o sankcijos buvo taikytos atskirai Administracijos struktūrai. Matyt, kažkas Lietuvoje tiesiog pamatė pažįstamą žodžių junginį ir nepanorėjo leistis į smulkmenas...

— Matot, jeigu kreipsimės į ES sankcijų sąrašą anglų kalba, ten naudojamas prielinksnis „of“ (The Main Economic Office of the Administrative Affairs Office of the President of the Republic of Belarus). Prielinksnį galima išversti kaip „prie“. Tai yra, kalbama apie Vyriausiąją ūkio valdybą prie Prezidento administracijos. Bet vertimo metu prielinksnis kažkodėl buvo išmestas.

Nenusimanantis žmogus gali pagalvoti, kad viskas yra ta pati institucija. Iš tikrųjų, Baltarusijos prezidento Administracija yra didžiulė struktūra, kuriai priklauso dešimčiai valdančių subjektų, jų tarpe – sanatorija „Belarus“.

Išvertėme juos į lietuvių kalbą ir išsiuntėme visoms įstaigoms. Bet mūsų vis tiek niekas nenori klausyti.

— Sanatorijos temą Aleksandras Lukašenka pabrėžė per savo pasirodymą VI Visos Baltarusijos liaudies susirinkime, beje, jis buvo labai rimtai nusiteikęs. Citata: „Prašau vyriausybę nedelsiant imtis šios problemos ir priimti atitinkamą sprendimą. Arba pateikite ją svarstyti prezidentui“. Kas nors iš Baltarusijos valdininkų su jumis susisiekdavo?

— Žinoma. Šita situacija buvo atidžiai išnagrinėta Baltarusijos Prezidento administracijoje, vyriausybė skiria jai daug dėmesio. Minske, žinoma, bus priimami sprendimai dėl sanatorijos. Ir tikiuosi, kad jos padės nugalėti krizę.

Noriu pastebėti: sausio 20 dieną sanatorijos kolektyvas paruošė peticiją Lietuvos prezidentui, ministrui-pirmininkui, Seimo pirmininkui ir komisijoms. 371 darbuotojas pasirašė šioje peticijoje.

Iki šiol (interviu paimtas vasario 24 dieną - RuBaltic.Ru pastaba) mes gavome tik formalų atsakymą iš prezidento. Pabrėžiu: tai yra tik formalus atsakymas! Jame nėra jokios konkrečios informacijos, nėra atsakymų į mūsų klausymus.

— Beje, tai labai parodomasis atvejis: sanatorijos darbuotojus Lukašenka pavadino „mūsų žmonėmis“. Nors jų absoliučią daugumą sudaro lietuviai, ar ne?

— Mūsų žemės sklypas – 5 hektarai – išnuomoti 99 metams Baltarusijos Respublikai. Jai priklauso pastatai, kurie yra šitoje teritorijoje. Iš viso - beveik 22 tūkstančiai kvadratinių metrų. Tai yra Baltarusijos valstybinė nuosavybė. Bet tuo pačiu metu sanatorija yra Lietuvos Respublikos valdantis subjektas, yra pavaldi jos įstatymams, veikia Lietuvos jurisdikcijoje.

Iš vis, aš nesveikinu skirstymo pagal tautybę. Koks skirtumas, kas yra baltarusis, o kas – lietuvis?

— Prezidento ir vyriausybės požiūris į sanatorijos „Belarus“ darbuotojus yra suprantamas. Bet tuo pačiu metu, kiek suprantu, jus labai uoliai palaiko vietos valdžia? Jų tarpe Druskininkų meras Ričardas Malinauskas.

— Su meru turime bendrą tikslą – Druskininkų vystymąsi ir klestėjimą, miesto gyventojų gyvenimo sąlygų gerėjimą. Ir mums itin skaudu, kad „viršuje“ priimami sprendimai, kurie ketina pribaigti šitą nuostabią vietą.

Lietuvos žiniasklaidoje skambėjo klausimas: kokią įmonę reikėtų panaikinti Vilniuje, kad jos likvidavimas būtų lygiavertis sanatorijos „Belarus“ uždarymui Druskininkuose? Aš jums atsakysiu – šita įmonė privalo turėti beveik 12 tūkstančių darbuotojų!

Ir meras, ir miesto savivaldybė labai nerimauja ir jaudinasi. Jie supranta, kad reikia gelbėti sanatoriją ir, vadinasi, visą miestą.

Nes esame miestą formuojanti įmonė. Visus mokesčius mes mokame Lietuvoje. Ir iš dalies sanatorijos „Belarus“ dėka Druskininkai per pastaruosius metus grožėja ir keičiasi į gerąją pusę.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 19 — id: `scraped:rubaltic_lt:a22f065629109416`

**Title:** Lietuvos valdžia neišlaikys Vilniaus evakuacijos Astravo AE sprogimo atveju

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Ar reikalinga evakuoti Vilniaus gyventojus rimtos avarijos Astravo atominėje elektrinėje atveju? Lietuvos valdžia suka galvą šiuo klausimu, o Vidaus reikalų ministerija žada pasidalyti savo išvadomis. Tikriausiai sostinės evakuacijos planai bus pripažinti netikslingais: Lietuvai tokio mąsto operacija visiškai nepajėgiama.

Lietuvos sostinės evakuacijos sumanymas kovos su Astravo AE kontekste aptariamas jau seniai. 2016 metais „Tėvynės sąjungos – Lietuvos krikščionių demokratų“ (TS-LKD) rinkiminio štabo vadovas Dainius Kreivys pareiškė, kad šalies vadovybei reikia kuo greičiau sudaryti atitinkamą planą.

„Per pastarąjį pusmetį Astravo AE Baltarusijoje, kuri yra vos 50 kilometrų atstume nuo Vilniaus, įvyko trys rimti incidentai. Sprogimo atveju atominėje reikėtų evakuoti visą Vilnių, nors niekas nežino šiandien, kaip tai padaryti. Dabartinė valdžia sako, kad AE statybą reikią prižiūrėti. Bet kaip tai padaryti? Kai krito reaktoriaus korpusas, niekas neturėjo galimybės patikrinti, ar jis nebuvo sumontuotas atgal. Dar reikia nepamiršti apie baltarusių darbo atlikimo kultūrą, technologijas, apie tai, kad elektrinė yra statoma rusų įmonės „Rosatom““, – sielvartavo Kreivys.

Jei stato „Rosatom“, tai atominė elektrinė būtinai anksčiau ar vėliau susprogs. Ir Lietuva tokiam scenarijui yra visiškai nepasiruošusi. Į tai atkreipdavo dėmesį ir buvusi Seimo spikerė Loreta Graužinienė: „Civilinės priemonės šito saugumo užtikrinimui turi būti sudarytos: ir planai, ir priemonės, ir viskas kita. Šiandien esame visai nepasiruošę. Net neįsivaizduoju, jeigu dabartiniu metu prireiktų evakuoti Vilnių, kaip tai gali būti įvykdyta“.

Nuo tų laikų ir iki šiol aiškiau netapo: pilnavertis Lietuvos sostinės evakuacijos planas taip ir nebuvo parengtas.

Bet vyriausybė neįvertino vietos valdžios entuziazmo.

„Jie, atrodo, gąsdina Vilniaus miesto gyventojus, kelia paniką, nors, iš esmės, nėra net teorinio pagrindo tam“, - pareiškė šiuo atžvilgiu tuometinis Lietuvos vidaus reikalų ministras Eimutis Misiūnas. Anot jo, avarijos atveju gyventojai bus evakuojami iš 30 km atstumo zonos aplink elektrinę, o Baltijos respublikos sostinė yra žymiau nutolusi nuo Astravo AE. Ir jai numatytas kitas priemonių rinkinys.

Rugsėjo mokymai galų gale neįvyko – Vilnius „repetavo“ Astravo AE avariją lapkritį, kartu su kitais miestais. Be to, evakuacijos mokymuose dalyvavo vos 50 moksleivių-savanorių. Kitaip tariant, renginio mąstas nedaro įspūdžio.

Kas bus, jei vietoj 50 žmonių iš Vilniaus teks evakuoti šimtus tūkstančių? Atsakymas akivaizdus: Lietuvos valdžia nepajėgs įveikti šitos užduoties.

Jie atvirai pripažindavo, kad nežino, kaip veikti tokiu atveju. Tai yra, katastrofos Astravo AE atveju, apie kurią pastoviai tvirtina Vytautas Landsbergis ir jo svita, sostinėje prasidės chaosas ir nekontroliuojamas vietos gyventojų nutekėjimas kuo toliau nuo valstybinės sienos su Baltarusija. Tai gresia didžiulėmis aukomis (panika šiuo atveju siaubingesnė už radiaciją), ir Lietuvos valdžia provokuoja šitą paniką jau daugelį metų.

Formaliam atsiskaitymui gyventojams išdalinamos jodo tabletes ir rengiami parodomieji mokymai. Bet iš tikrųjų Lietuva neturi noro rimtai ruoštis technogeniniai katastrofai.

Todėl, kai Vilniaus miesto administracija pageidavo surepetuoti evakuaciją, VRM ryžtingai pasisakė prieš šiuos planus. Lietuvos žiniasklaida pranešdavo, kad ir krašto apsaugos ministerija irgi prieštaravo. Tai ir yra paaiškinama: kaip tik kariuomenė ir policija privalo atlikti pagrindinį vaidmenį šitoje operacijoje. Ir kas kitas už vidaus reikalų ministrą suvokia savo pavaldinių neparengtį tokiam įvykių išsidėstymui?

Vilniaus evakuacijos tikslingumo klausimas vėl aptariamas VRM. Ir tikriausiai atnaujinta institucijos vadovybė pritars Eimučio Misiūno pozicijai: nėra prasmės atidirbinėti tokius radikalius žingsnius, nes Vilnius yra gana nutolęs nuo Astravo AE.

Bet šiuo atveju susigriauna sąmokslo teorija, pasak kurios Putinas ir Lukašenka pastatė atominę elektrinę Astravo rajone tam, kad grėsti Lietuvos sostinei. Kas per grėsmė, jeigu respublikos valdžia nerengia miesto evakuacijos plano?

Lietuvoje jau buvo tokių atvejų. Analitinis portalas RuBaltic.Ru rašė apie tai, kaip Baltijos respublika atrėmė nedraugiškos valstybės „Udija“ įsivaizduojamų diversantų ataką.

Mokymų ypatumas buvo tai, kad VRM ir Valstybės sienos apsaugos tarnybos eiliniai darbuotojai apie juos nieko nežinojo (žinojo tik vadovybė). „Mes norėjome realiomis sąlygomis patikrinti, kaip į tokią ekstremalią situaciją sureaguos Lietuvos atsakingos institucijos“, - pasakojo jau mums pažįstamas Misiūnas.

Patikrino ir prasiverkė. Diversantai lengvai užėmė pasienio kontrolės punktą ir policijos komisariatą, daugiau už dešimt teisėsaugos pareigūnų buvo „nužudyti“. Institucijų sąveika krizės atveju, švelniai tariant, galėtų būti geresnė, inspektoriai nebuvo pasiryžę invazijai ir netaisyklingai įvertino situaciją. Žodžiu, visiškas fiasko: Udija gali drąsiai užgrobti Lietuvą!

Nenuostabu, kad Misiūnas po šitos istorijos nepageidavo užsiiminėti pilnaverte Vilniaus evakuacija. Rezultatas gi žinomas iš anksto: su įsivaizduojama radiacija policija susidoros ne geriau nei su įsivaizduojamais diversantais.

Nepamirškime, kad iki Misiūno Lietuvos vidaus reikalų ministro pareigas ėjo Saulius Skvernelis, kuris buvo priverstas atsistatydinti po žymaus skandalo, kai surakintas antrankiais 24 metų narkomanas sugebėjo pavogti iš policininkų Kalašnikovo automatą ir dingo. Pabėgėlį rado ir sulaikė tik po kelių valandų.

Koronaviruso pandemijos situacija Lietuvoje irgi akivaizdžiai parodė, kaip vietos valdžia įveikia ekstremalias situacijas.

Praėjusių metų gruodį Baltijos šalis užėmė pirmą vietą pasaulyje pagal COVID-19 sergamumą anot New York Times.

Šiuo faktu galima apriboti visus pokalbius apie Vilniaus evakuaciją.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 20 — id: `scraped:rubaltic_lt:257000e41a56669b`

**Title:** Šios valstybės yra toksiškos: Rusija ištarė nuosprendį santykiams su Baltijos šalimis

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Oficialus Rusijos Federacijos URM atstovas Marija Zacharova pavadino Baltijos šalis toksiškomis. Tai yra pirmas atvejis, kai Lietuva, Latvija ir Estija būna įvertintos taip griežtai ir atvirai Rusijos vadovybės įgaliotu asmenu. Baltijos valstybių toksiškumo pripažinimas yra viešas oficialus pareiškimas, kad Rusija atsisako plėtoti santykius su šio regiono šalimis. Baltijos regionas vis sparčiau praranda Rusijos rinkas, investorius bei tranzitą.

„Baltijos valstybėse valdžia bei specialiosios paskirties tarnybos naudoja skirtingas slopinimo metodikas prieš civilinės bendruomenės aktyvistus, teisių gynėjus, prieš žurnalistus, kurie gina skirtingas už oficialias nuomones apie užsienio ir vidaus politiką šalyje. Be abejo tai liečia ir istoriją. Į šių įtakos metodų arsenalą buvo įtraukti ir profilaktiniai pokalbiai, gyvenimo socialinių bei ekonominių sąlygų bloginimas patraukiant šiam tikslui bankus“, - pasakė Zacharova, įvertindama padėtį Estijoje, Latvijoje ir Lietuvoje.

Ypatingai Rusijos URM pabrėžė Jurijaus Melio tragediją. Pastarasis 1991 metų sausio 13 dieną švietė tanko žibintais prie Vilniaus televizijos bokšto ir paleido 3 tuščius šūvius aukštyn, dėl ko buvo Lietuvoje nuteistas 7 metams kalėjime ir apkaltintas “nusikaltimu žmoniškumui“. Čia viskas aišku. Jurijus Melis – Rusijos Federacijos pilietis ir Rusijos kariuomenės atsargos pulkininkas. Jeigu Lietuvoje vyrauja toks požiūris į rusus, tai kokie santykiai gali būti tarp dviejų valstybių?

„Toksiškos iš esmės atmosferos kūrimas“, - padarė išvadą Marija Zacharova dėl situacijos Baltijos valstybėse.

Prieš tai Rusijos valdžia laikėsi taktikos, kai demonstratyviai ignoravo atvirai priešiškus pareiškimus iš šių atvirai priešiškų valstybių. Buvo pripažinta, kad Baltijos šalys stengiasi išprovokuoti Rusiją tam, kad pateisinti NATO sąjungininkų akyse savo amžinus klyksmus apie karinę grėsmę, kylančią iš Rytų kaimyno, ir tuo laimėti vakarų šalių investicijų savo saugumui didinimo.

Šiuo atveju optimalus sprendimas „drambliui“ – ne reaguoti į lojančias „moskas“. Todėl Baltijos šalių, jų vidaus žmonių teisių laikymosi padėties bei požiūrio į Rusiją įvertinimai buvo žurnalistų bei ekspertų prievole.

Beveik visi iš jų daugybę kartų rašydavo ir sakydavo maždaug tą patį, ką ir dabar pasakė RF URM atstovas, o šio straipsnio autorius savo komentare naujienų agentūrai RIA „Novosti“ net minėjo toksiškumą: „Rusijoje eksperimentiniu būdu buvo nustatyta, kad vengti dialogo bei sąveikos su toksišku kaimynu, kurie gali pasibaigti skandalu ar problemomis, daug naudingiau už pastangas išlaikyti ryšius. Bet kurios investicijos į kontaktus su Baltijos šalimis neabejotinai veda į pralaimėjimą“, - įvertina situaciją Nosovičius.

Ką tai reiškia pastariesiems? Tai garantuoja rusiškos rinkos, investicijų bei tranzito tolimesnį praradimą. Besitęs tie procesai, kurie vyksta jau dabar, bet oficialus šių procesų patvirtinimas panaikina visas galimybes juos sustabdyti ir pasukti atgal.

Daugelis Baltijos šalių politinės klasės dalyvių iki šiol negali šiuo patikėti. Juose egzistuoja neišnaikinamas pasitikėjimas formule „verslas eina atskirai nuo politikos“, kai jie sako ir daro prieš Rusiją viską, ką tik pageidauja, bet tuo pačiu metu aptarnauja rusiškus krovinius.

Tai pagrindžia praėjusių metų „prašymas“ Maskvai iš Latvijos vyriausybės, kuriame Ryga prašė Rusijos Federacijos Transporto Ministerijos grąžinti rusiškos anglies tranzitą per Latvijos teritoriją. Susisiekimo ministerijos laiškas buvo suderintas su Latvijos URM vadovu Edgaru Rinkevičiu. Pastarasis pretenduoja vadintis Baltijos pirmuoju rusofobu, bet į savo bendraminčių pagrįstą nustebimą atsakė visai kaip siūlo populiarus memas „jūs nesuprantate, tai visiškai kita“.

„Eilinės „geležinės uždangos“ kūrimas su Rytais labai apribos mūsų ekonomines galimybes. Žinoma, yra atvejai, kai šalys sugebėjo pasiekti aukšto ekonominio vystymosi lygio nepaisant geografinės padėties. Pavyzdžiui, Švedija ir Suomija. Bet tai reikalavo ekstraordinarinių pastangų. O pas mus nėra nei ekonomikos strategijos, nei ekstraordinarinių pastangų ekonomikos vystymuisi. Iš vis jokių rimtų pastangų nematyt“, - komentuoja esamos strategijos Rusijos atžvilgiu padarinius Latvijos Seimo deputatas Viačeslavas Dombrovskis.

Šitie padariniai jau tapo realybe. „Latvijos geležinkeliai“, kurie taip ir nesulaukė Rusijos anglies, pardavinėja metalo laužui traukinių ratus ir bėgius – daug pats už save pasakantis faktas, kuriam nereikia komentarų.

Ir toliau situacija tiktai blogės.

Baltijos šalys tokia savo politika daro viską įmanomą tam, kad šita tezė taptų patvirtinta oficialiai ir įsigaliotų juridiškai. Šitos valstybės pirmos pasaulyje randa naujų pretekstų pasiūlyti naujas sankcijas prieš Maskvą, visada skatina Vakaruose patį įnirtingą antirusišką elgesį iš visų įmanomų, įteikia savo teritorijas NATO puolimo įrangos išdėstymui ir savo infrastruktūrą tam, kad skatinti Rusijoje lauko riaušes.

Ir jau dabar nėra jokių abejonių, kieno garbei gali būti priimtas toks įstatymas.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```
