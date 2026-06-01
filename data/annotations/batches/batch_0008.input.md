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

### Article 1 — id: `scraped:rubaltic_lt:ac173578250fe086`

**Title:** Lietuva prikaišioja Kinijai, kad įsiteikti Jungtinėms Valstijoms

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuva atsisakė krovinių rentgeno patikros įrangos užpirkimo pas kinų kompaniją Nuctech, kuri laimėjo tenderį. Anot vyriausybės komisijos įranga iš Kinijos yra pavojinga respublikos „nacionaliniam saugumui“: jos dėka Pekinas neva rinks duomenis apie Vilniaus, Kauno ir Palangos oro uostų keleivius. Šis atvejis žada sukomplikuoti Kinijos ir Lietuvos santykius, kurie pastaraisiais metais iš vis klostosi nelengvai.

Tenderis dėl keleivių bagažo skenerių įrengimo Lietuvos oro uostose buvo laikytas praėjusiais metais. Jį laimėjo Nuctech – kinų rentgeno patikros įrangos tiekėjas. Laimėjo – reiškia pasiūlė pačias palankias sąlygas. Viskas atitinka laisvosios rinkos dėsnius. Bet Lietuvoje šitie dėsniai kažkodėl neveikia.

Sudaryti sandorį kinų kompanijai neleidžia. Vyriausybės komisija padarė išvadą, kad Nuctech neatitinką nacionalinio saugumo reikalavimus. Bagažo rentgeno patikros įranga neva gali rinkti informaciją apie keleivius ir teikti ją kinų žvalgybai ir ypatingos paskirties tarnyboms. Tebelieka sulaukti, kol ministrų kabinetas pritars komisijos išvadoms – tai tik formalumas.

„Lietuva apsisprendė nebūti Kinijos kuriamos ir kontroliuojamos technosferos dalimi“, - tokį pareiškimą padarė Seimo nacionalinio saugumo ir gynybos komiteto pirmininkas Laurynas Kasčiūnas.

„JAV Nacionalinės saugumo agentūros ir amerikietiškų agentūrų saujelės vykdoma kampanija mėgina suvienyti Europos vyriausybes tam, kad išnaikinti Nuctech Co., kinų valstybinę kompaniją, turinčią platūs ryšius. Jos gaminama krovinių, bagažo bei keleivių patikros įranga tampa neatskiriama jūros bei oro uostų ir pasienio punktų dalimi visoje Europoje, - praėjusiais metais rašė The Wall Street Journal. – JAV pastangos, sustiprėjusios praeitą mėnesį, lydėjo analogišką antpuolį, kurio tikslas buvo pašalinti kinų telekomunikacijų milžiną Huawei Technologies Co. iš komunikacijos tinklų, bet kuris davė dviprasmiškus rezultatus. Kaip ir Huawei atveju, akcija prieš Nuctech yra patikra, ar JAV pajėgs įtikinti savo sąjungininkus vengti daugiau prieinamos įrangos gamintojo amerikietiškais saugumo sumetimais, kuriuos kompanijos laiko nepagrįstais“.

Lietuvą, žinoma, įtikinti visiškai nereikia. Jai užtenka vien nurodymų. Šalis juos mielai įvykdys, besivadovaudama seno tarybų laikų principo: «Partija pasakė „reikia“! Komsomolas atsakė „Taip“!»

Oficialūs Kinijos vyriausybės atstovai iškritikavo Lietuvos sprendimą atmesti bendradarbiavimą su Nuctech. „Lietuvos vyriausybės komisijos sprendimas blokuoti ją (kompaniją – RuBaltic.Ru pastaba) Lietuvos oro uostuose yra neabejotinai politinių motyvų nulemtas. Tai atneš nuostolių Lietuvai. Ir rinkos faktai tai pagrįs“, - sakoma Kinijos ambasados pranešime.

Užtat amerikiečių ambasadorius Lietuvoje Robertas Gilchristas pagyrė „Lietuvos vyriausybės žingsnius Lietuvos nacionalinio saugumo ir ypatingojo svarbumo infrastruktūros apsaugos užtikrinimui“.

Pats nuostabiausia, kad praeitais metais Suomija lygiai taip pat rinkdavosi rentgeno patikros įrangą pasienio punktams prie sienos su Rusija. Šalis nurodė labai žemą kainą ir vos tik viena kompanija pageidavo dalyvauti tenderyje. Atspėkite, kokia. Žinoma, Nuctech.

The Wall Street Journal rašo, kad amerikiečių diplomatai ragino suomius atsisakyti „pavojingos“ kinų įrangos. Bet suomiai vis tiek sandorį su Nuctech pasirašė. Tai kodėl Suomija – viena pažangiausių Europos valstybių technologijų srityje – neįžiūrėjo skeneriuose iš Kinijos „grėsmės nacionaliniam saugumui“?

Nuctech atvejis – vos tik aisbergo viršūnė. Vilniaus ir Pekino santykiai pastaraisiais metais klostėsi nelengvai. Kinija yra oficialiai paskelbta „grėsme Lietuvos nacionaliniam saugumui“, jos klastingi planai aprašyti Lietuvos Respublikos valstybės saugumo departamento bei karinės žvalgybos ataskaitose.

Prezidentas Gitanas Nausėda iškritikavo ketinimus statyti išorinį giliavandenį uostą Klaipėdoje už kinų investorių pinigus.

Dalai Lamos vizitas Lietuvoje – dalykas įprastas. Ypač šilti santykiai sieja Tibeto dvasinį lyderį su konservatorių lyderiu Vytautu Landsbergiu.

Kokios šalies deputatai drįso pasirašyti atvirą laišką Pasaulio sveikatos organizacijai su reikalavimu leisti dalyvauti tarptautinėje konferencijoje Taivano atstovams? Žinoma, Lietuvos.

Praeitais metais Baltijos respublikos valdžia žengė dar toliau ir sankcionavo Lietuvos-Taivano forumo įsteigimą. Jo paskelbtų tikslų sąraše – Taivano demokratijos, žmogaus teisių ir tautų apsisprendimo teisės siekimo parama.

„Panaši geografinė padėtis, kai saugumui gresia didysis agresyvus kaimynas, kova už laisvę ir demokratiją, pagarba žmogaus teisėms ir asmens orumui sieja mūsų tautas, nors esame toli vieni nuo kitų“, - sakė seimūnas Mantas Adomėnas.

Pagaliau, nereikia užmiršti, kad pastaruosius Seimo rinkimus Lietuvoje laimėjo „landsbergiečiai“ konservatoriai, kurie pažadėjo ginti demokratiją aplink visą pasaulį – „nuo Baltarusijos iki Taivano“. Tai yra pažodinė citata. O prieš kelias dienas valstybės užsienio reikalų ministras Gabrielius Lansbergis per susitikimą su savo kolegomis iš Europos padarė eilinį išpuolį prieš Kiniją.

„Lietuvos ir Latvijos vardu kalbėjęs G. Landsbergis išreiškė susirūpinimą Kinijos ir Rusijos itin artimu bendradarbiavimu ir keliamomis hibridinėmis grėsmėmis, pabrėžė balansuojantį ES-Japonijos bendradarbiavimo vaidmenį, užtikrinant regioninį saugumą, transatlantinio bendradarbiavimo svarbą“, - sakoma Lietuvos URM pranešime spaudai.

Dalia Grybauskaitė asmeniškai demonstravo Si Dzinpingui lietuviškas prekes ir aptarinėdavo su juo dvipusio ekonominio bendradarbiavimo klausimus vietoj žmogaus teisių laikymosi Taivane ir Honkonge.

Bet šitie laikai jau praėję. Dabar landsbergiečių klanas ir jų „prijaukintas“ prezidentas daro viską įmanomą, kad Lietuva negautų nei mažyčio trupinio nuo kinų „investicinio pyrago“.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 2 — id: `scraped:rubaltic_lt:9c7ff55552cb1502`

**Title:** Lietuvą įžeidė Ukrainos išdavystė dėl Astravo AE

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos ir Ukrainos santykiai gerokai įsitempė. Anksčiau Kijevas žadėjo paremti Baltarusijos Astravo atominės elektrinės boikotavimą, bet nuo pat naujų metų pradžios atnaujino pigios elektros importą iš Baltarusijos. Lietuvos politikai privačiuose pokalbiuose su kolegomis iš Ukrainos pasipiktindavo šiuo faktu.

2019 metų vidurį Ukrainoje pradėjo veikti naujas elektros rinkos modelis. Šiuo pasinaudojo valstybinis gamybinis susivienijimas „Belenergo“: vos per šešis mėnesius Baltarusija pardavė Ukrainos treideriams elektros 45,57 milijonams dolerių. Daugiau pirko tik Lietuva.

Bet jau 2020 metais Ukraina netikėtai ir sparčiai pakeitė energetikos politikos prioritetus, beje nutiko tai dar prieš Lukašenkos perrinkimą. Nuo sausio iki balandžio elektros importo iš Baltarusijos dydžiai mažėjo, o gegužės mėnesį komerciniai tiekimai iš vis liovėsi. Tuomet jau buvo paskelbtas moratoriumas elektros tiekimams iš Rusijos bei Baltarusijos iki koronaviruso epidemijos pabaigos.

Šita naujiena labai pradžiugino Lietuvą, kuri vis mėgindavo surengti Baltarusijos energetinę blokadą.

Ukraina buvo tikra, kad lengvai apsieis be baltarusių elektros, užteks nuosavų atominių bei šiluminių elektrinių galingumo.

Tuo pačiu metu gegužę Lietuvos energetikos ministras Žygimantas Vaičiūnas surengė derybas telefonu su Ukrainos energetikos ministro pareigas einančia Olga Buslavec. Jinai įtikindavo, kad kovoje su Astravo AE Vilnius gali tikėtis visiškos paramos iš Kijevo pusės.

„Nepaisant to, kad praėjusiais metais skambėdavo skirtingi pareiškimai, Ukrainos pozicija dabar vienprasmiška: šalis neketina pirkti ir nepirks elektros iš Astravo AE nei artimiausiu metu, nei ilgalaikėje perspektyvoje“, - savo tautiečius įtikino Vaičiūnas.

Galutinė detalė: lapkritį Buslavec surengė pasitarimą su šalies energetikos atstovais ir paskelbė, kad 2021 metais Ukraina neprekiaus elektra iš Baltarusijos – nei eksportuos, nei importuos.

Lietuvos bičiulių tai turėjo visiškai nuraminti. Bet paskui nutiko tai, ko jie net negalėjo tikėtis.

O jau sausį Ukrainos pramonė paskubėjo pasinaudoti šiomis nuolaidomis. Pirmuosius aukcionus dėl prieigos prie Baltarusijos ir Ukrainos tarpvalstybinių elektros tinklų laimėjo Viktoro Pinčiuko „Dneprostal-Energo“ ir Maksimo Jefimovo „Donbasenergo“.

Ukrainos žiniasklaidoje kai kurie paskelbė išdavystės požymius. Nejaugi Ukraina taps realizavimo rinka Putino pastatytai Baltarusijoje atominei elektrinei? O ką pasakys lietuviai?

Pažiūrėkime, ką sakė Ukrainos deputatas, buvęs Ukrainos Saugumo tarnybos vadovas Valentinas Nalivaičenka: „Kalbėjau su kolegomis iš Lietuvos ir Europos Komisijos. Pasakyti, kad mūsų partnerių iš Europos nusivylė Ukrainos valdžios sprendimas įsigyti elektrą iš Astravo AE, – nepasakyti nieko. Kaip tai atsitiko, kad jūsų prezidentas ir ministras-pirmininkas pradėjo metus nuo savo elektros rinkos suirimo visiškai nepaisant ES bendros pozicijos dėl sankcijų prieš Baltarusijos ir RF režimus?! Dar 2020-ųjų metų rudenį Ukrainos vyriausybė oficialiai įtikindavo ES partnerius, kad neketina bendradarbiauti su Putino AE Baltarusijoje, o nuo naujųjų metų pradžios pradėjo pirkti jos pagamintą elektrą“.

Paskui Nalivaičenka „piešia“ klaidingą įvykusios situacijos vaizdą: „Mūsų partnerių vieningumo dėka Astravo AE iš esmės prarado realizavimo rinką, kuriai buvo taikyta. Bet čia įvyko tai, ko europiečiai net negalėjo tikėtis: Lukašenkai ir Putinui į pagalbą atėjo Ukraina“.

Toks pareiškimas, žinoma, skirtas ne labai išsilavinusiai publikai. Visų pirma, kokios sankcijos prieš Astravo AE galioja Europos Sąjungoje? Jokių. Antrą, apie kokį tokį „partnerių vieningumą“ kalbama, kai Lietuvos energetikos ministras Dainius Kreivys viešai kaltina Latviją Astravo AE blokados žlugimu?

Vietoj to, kad užduoti savo kolegoms iš Lietuvos šituos klausimus, ponas Nalivaičenka pritarė jų nuomonei. Tą patį padarė ir kitas Ukrainos Aukščiausiosios Rados deputatas – plačiai žinomas kaip Petro Porošenkos šalininkas Aleksejus Gončarenka.

Laidos "Saviko Šusterio žodžio laisvė" eteryje Gončarenka skelbė, kad ir jam teko rausti iš gėdos prieš draugus iš Lietuvos: „Šiandien kalbėjau su kolega, Lietuvos Seimo tarptautinių reikalų komiteto vadovu. Jis sako: „Mes visada remiame Ukrainą. Bet šiandien mes atsisakome elektros iš Baltarusijos Astravo atominės elektrinės, esančios mūsų pasienyje, ir jus pradedat ją pirkti“.

Ir vėl, paminėtas lietuvių deputatas pamiršo pridėti, kad jo šalis atsisako Astravo AE produkcijos tik formaliai: prekyba neva yra vykdoma Latvijos biržoje, kadangi iš esmės elektra tiekiama tiesiai iš Baltarusijos.

Šita schema pradėjo veikti dar esant senai vyriausybei. Dabar gi Dainius Kreivys viešai pripažįsta, kad Astravo AE blokada žlugo. Niekas jos nesilaiko. Tuomet kodėl Ukraina privalo atsisakyti baltarusiškos elektros?

Bet realybėje viskas kur kas paprasčiau: pigi elektra reikalinga oligarcho Igorio Kolomojskio ferolydinių gamykloms (tai yra jo verslo imperijos pagrindas). Akivaizdu, kad būtent jis po Zelenskio pergalės lobavo vadinamąją „Geruso pataisą“, kuri leido Ukrainai atnaujinti baltarusiškos ir rusiškos elektros importą.

Bet šita schema visiškai netenkina Rinato Achmetovo, kuris valdo Ukrainos anglies gavybą bei šilumos generaciją. Konkurencija energetikos rinkoje jam nereikalinga.

Kol du įtakingiausi Ukrainos oligarchai kovoja dėl viešpatavimo, eiliniams gyventojams sekamos politinės pasakos. Tie, kas nori importuoti elektra – Kremliaus agentai. Tie, kas nenori – irgi Kremliaus agentai, nes neleidžia Ukrainos pramonei vystytis. Žodžiu, kaip ir visada: Putinas prieš Putiną...

Laikui bėgant Astravo AE gali žymiai sugadinti santykius tarp dviejų valstybių, kurie atrodo nepriekaištingi.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 3 — id: `scraped:rubaltic_lt:b6cc70ce263d3895`

**Title:** Lietuva patvirtino, kad Rusijos sprendimas atsisakyti tranzito pro Baltijos šalis yra teisingas

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Nauja bei sena Lietuvos vyriausybės remia buvusios Baltarusijos prezidento rinkimų dalyvės Svetlanos Tichanovskajos pasiūlymą taikyti sankcijas šalies įmonėms, kurios eksportuoja savo produkciją per Klaipėdos jūros uostą. Lietuvos valdančioji klasė leidžia sau baltarusiško tranzito blokados mintį, neatsižvelgdama į tai, kad tokia situacija gali virsti katastrofa Klaipėdai ir „Lietuvos geležinkeliams“. Šiuo Vilnius ne vien tik ragina nukreipti baltarusiškus krovus link Rusijos uostų, bet ir įrodo Rusijos, kuri ketina atsisakyti savo produkcijos tranzito per Baltijos šalių uostus, strateginio sprendimo teisingumą. Deja, Baltijos valstybėms geopolitika yra neprilyginamai svarbesnė už ekonomiką.

„Belaruskalij“ yra viena iš Baltarusijos valstybinių įmonių, esančių beveik Aleksandro Lukašenkos kišenėje. Šios įmonės darbuotojus gali atlesti iš pareigų už politinę poziciją, dėl to pradėjome aptarti sankcijų taikymą įmonei“, - pareiškė gavusi prieglaudą Vilniuje „tautinė Baltarusijos lyderė“ Svetlana Tichanovskaja.

Kuomet „Belaruskalij“ veikla yra labai priklausoma nuo Lietuvos, taikyti sankcijas Tichanovskaja ragina konkrečiai Lietuvą, nes „Belaruskalij“ naudoja Lietuvos geležinkelius ir Klaipėdos jūros uostą savo produkcijos eksportui“.

Kalio trąšos – pagrindinė Klaipėdos uosto pajamų šaltinis. Jų perkrovimui Baltarusija pastatė Klaipėdoje atskirą terminalą, kurį tęsia plėtoti ir gerinti paskutinio dešimtmečio bėgyje. Tuo Baltarusija investuoja pinigus į Lietuvą ir jos trečią pagal gyventojų skaičių miestą.

Per 10 metų vienas „Belaruskalij“ investavo į Klaipėdos jūros uostą 100 milijonų eurų. Ir vos praeitais metais įmonė eksportavo per Lietuvą 10 milijonų tonų krovinių, o baltarusiško terminalo Klaipėdoje pajamos sudarė 90,5 milijonų eurų.

Ir Tichanovskaja ragina atsisakyti štai šito vardan Baltarusijos „demokratizacijos“. Atsisakyti ne vien tik kalio trąšų. „Mes prašome nepirkti „Belaruskalij“ produkcijos tam, kad Lukašenkos režimas negautų šių įmonių pinigų. Tai yra susieta ne vien tik su „Belaruskalij“, bet taip pat ir su „Grodno Azot“, „Naftan“ bei kitomis režimui svarbiomis įmonėmis“, - skelbia Baltarusijos „tautinis lyderis“.

Per pirmą 2020-ųjų metų pusmetį LGŽ aptarnavo 24 milijonus tonų krovinių, iš jų 9 milijonai tonų sudarė kroviniai iš Baltarusijos. Tai yra jau paminėtos trąšos, naftos gaminiai, durpės ir kitos Baltarusijos eksporto prekės, kurios yra gabenamos per Klaipėdos uostą.

Atsisakyti šio reiškia, kad ir geležinkelių, ir Klaipėdos, kuriai uostas turį lemiamą reikšmę, laukia ekonominis žlugimas. Ir tai gali nutikti ekonominės krizės aplinkybėmis, kai Lietuva yra trečia pagal bedarbystės lygį Europos Sąjungoje.

Net oficiali statistika teigia, kad kas šeštas darbingo amžiaus lietuvis dabar sėdi be darbo. Šiomis aplinkybėmis „prezidentė Svetka“ siūlo panaikinti tūkstančius darbo vietų „Lietuvos Geležinkeliuose“ ir kur kas daugiau darbo vietų Klaipėdoje.

Kokia turėtų būti Lietuvos teisinga reakcija į panašų įžūlumą – kai gyvenantis Vilniuje už Lietuvos mokesčių mokėtojų lėšas žmogus ragina juos palikti be pragyvenimo šaltinio?

Mažiausiai – parodyti įžūliai opozicijos lyderei jos tikrą vietą, o kraštutiniu atveju – išvaryti iš Lietuvos. Tegul kepa savo kotletus Vokietijoje.

Bet čia prasideda pati įdomiausia dalis.

Tichanovskaja užtikrina, kad aptardavo sankcijas su Lietuvos vyriausybės atstovais, ir jie yra pasiruošę svarstyti Baltarusijos krovinių tranzito apribojimą ar net nutraukimą.

Šiuo atvejų kalbama apie „valstiečių“ vyriausybę, kuri dabar palieka politinę sceną. Bet sekanti paskui „valstiečius“ konservatorių vyriausybė pasisako net vienprasmiškiau.

„Manau, kad šitą klausimą [sankcijų taikymą prieš „Belaruskalij“ - RuBaltic.Ru pastaba] reikėtų apsvarstyti. Iš pradžių, kaip buvo sufalsifikuoti rinkimai Baltarusijoje ir prasidėjo represijos, aš pasakiau, kad nepaisant savo trumpalaikių ekonominių interesų, reikia padėti tiems žmonėms. Ir ekonominės sankcijos gali tapti tuo ginklu, kuris veikia“, - pareiškė būsima Lietuvos ekonomikos ministrė Aušrinė Armonaitė.

Įsiminsim šitą faktą.

Ekonominė padėtis Lietuvoje, būtinumas papildyti biudžetą ir atlikti socialines pareigas – viskas tai iš vis neturi reikšmės, kai reikia pasiekti didžiulį tikslą: pakeisti politinį režimą Baltarusijoje.

Koks skirtumas, koks Lietuvoje bedarbystės procentas? Koks skirtumas, kiek dar darbo vietų praras šalis, likusi be užsakovų iš Baltarusijos?

Ir be to, kodėl šitie lietuviai visą laiką trukdo ir kalba apie kažkokius uždarbio mokesčius, pensijas, darbo vietas? Tegul išvažiuoja plūkti į Airiją ir netrukdo savo valstybei atlikti istorinę misiją – „Rusijos nulaikymą“.

Tokiomis aplinkybėmis Minskui ir nebelieka nieko kito, kaip nukreipti tranzitą į Rusiją. Saugumo sumetimais, nes Baltijos šalių vadovams savo valstybių ekonominiai interesai nereiškia nieko palyginus su geopolitika.

Šiuo atžvilgiu Lietuva stoja ne vien tik rusiškos logistikos šalininku, bet ir Rusijos valdžios „advokatu“.

Šitas sprendimas buvo nulemtas ne tiek ekonominės naudos ir investavimo į savo regionus vietoj svetimų šalių sumetimais, kiek nacionalinio saugumo sumetimais. Jeigu Baltijos šalys išsaugotų monopoliją rusiškų krovinių tranzitui per Baltijos jūrą, neišvengiamai ateitų laikas, kai jie pradėtų išnaudoti šią monopoliją, tam kad šantažuoti.

Tokiu atveju rusiško eksporto blokada Baltijos šalyse 2014-2015 metais – Ukrainos krizės aštriausiu metu – taptų tikėtinu scenarijumi. Nuostoliai, kuriuos patirtų Latvijos ir Estijos ekonomikos, neturėtų jokios reikšmės palyginus su „Rusijos sulaikymu“.

Todėl naudotis jų uostų paslaugomis tiesiog pavojinga. Ir Rusijai, ir Baltarusijai.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 4 — id: `scraped:rubaltic_lt:4e7da20c5491bf34`

**Title:** Galas „okupacijos paveldui“: Lietuva „pribaigs“ tarybų laikų sveikatos apsaugos sistemą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos Seimas paskyrė dešiniosios koalicijos kandidatę Ingridą Šimonytę šalies ministre pirmininke. Nauja valdančioji komanda jau spėjo padaryti sau gėdos pasisakydama už visuotinį valstybinės nemokamos medicinos panaikinimą ir ketinimą patikėti tautos sveikatą rinkai. Tomis sąlygomis, kai visa Lietuva kovoja prieš koronaviruso antrąją bangą, „landsbergiečiai“ net neslepia, kad ketina „pribaigti“ tai, kas liko nuo tarybų laikų sveikatos apsaugos, kuri „okupuotoje“ Lietuvoje buvo tikrai visuotinė ir nemokama.

Koaliciniame susitaryme, kurį pasirašė Seimo daugumą sudarantys „Tėvynės sąjunga – Lietuvos krikščionys demokratai“ (konservatoriai), Liberalų judėjimas ir Laisvės partija, įdėmūs skaitytojai pastebėjo sekantį punktą: „Sveikatos apsaugos paslaugų kokybė ir prieinamumas. Kursime sveikatos apsaugos sistemą, kuri būtų patogi gydytojams, prieinama ir kokybiška, kuri teiktų paslaugas visoje šalyje, būtų atspari krizėms ir nediskriminuotų privačių įstaigų“.

Tai, kad dešiniosios partijos paminėjo privačią mediciną ir neva esančią jos diskriminaciją, sugąsdino daugelį Lietuvos gyventojų.

Konservatorių gretoms artima žiniasklaida ėmėsi plačiai įtikinėti, jog nemokamos medicinos iš esmės pasaulyje net neegzistuoja, ir už viską šiame gyvenimą, įskaitant patį gyvenimą, reikia sumokėti.

„Tokio reiškinio, kaip nemokama medicina, nėra. Sveikatos apsaugos paslaugos kainuoja pinigų. Jos kainuoja brangiai, ypač kokybiškos paslaugos. Taip pat reikia įsiminti, kad paklausa joms yra aukšta, bet finansavimas nėra užtenkamas. Pacientai dažnai sumoka „iš savo kišenės“. Tai nėra normalu“, - teigia Lietuvos Medikų Sąjūdžio vadovo pavaduotoja Jurgita Sejonienė, kuri pateko į naująjį Seimą pagal „Tėvynės sąjungos – Lietuvos krikščionių demokratų“ sąrašus.

„Gyventojai neturėtų galvoti, kad yra kažkokios nemokamos paslaugos. Neleistina naudoti žodžio „nemokamas“: kaip švietimas, taip ir sveikatos apsauga nėra nemokama. Kiekviena paslauga privalo turėti savo vertę. Kiekvieno apsilankymo pas gydytoją metu pacientas turi būti informuotas, kiek kainavo suteikta jam paslauga ir kiek buvo kompensuota“, - patvirtina Luminor banko ekonomistas Žygimantas Mauricas.

Tuo tarpu vyresnių kartų lietuviai puikiai atsimena laikus, kai medicina Lietuvoje buvo visuotinė ir nemokama. Tai buvo Tarybų Sąjungos laikais, kai Lietuvai buvo suteikta tikrai visuotinė ir prieinama visiems gyventojams sveikatos apsaugos sistema, o ne medicinos paslaugų rinka, kur sveikata apmokestinama vienetiniu atlyginimu.

„Landsbergiečiai“, kaip ir dera nesitaikstantiems tarybų laikų neapkentėjams, pradėjo griauti šią „okupantų“ sukurtą, sistemą iškart po TSRS suirimo. Centro-kairiųjų įsigalėjimas valdžioje (Algirdas Brazaukskas, socialdemokratai, Raimundo Karbauskio „valstiečiai“) šią procesą suslopino, bet kiekvienas „TS-LKD“ sugrįžimas į vyriausybę paleisdavo medicinos „optimizaciją“, kai jai buvo primetama rinkos tvarka, o sveikata virsdavo preke.

Konservatorių motyvai, visų pirma, yra ideologiški, dažnai mažai racionalūs. Į visus įtikinimus, jog likusi nuo Tarybų Sąjungos visuotinės sveikatos apsaugos sistema yra nacionalinis paveldas, prilyginti kuriam Lietuva jau niekada nebesugebės, jie atsakydavo šiurpiais pasakojimais, kaip neblaivūs sovietų odontologai šalino lietuviams be jokios anestezijos sveikus dantis vietoj nesveikų.

Neva, štai tokia yra nemokamos medicinos kaina!

Imti ginčytis ideologijos klausimais su kvailiais dogmatikais – iš anksto neabejotinas pralaimimas. Tiesiog įsiminsim faktą.

Koronaviruso pandemija įrodė, kad žmonių išgyvenimą masinių nelaimių aplinkybėmis užtikrina ne rinka, bet valstybė. Išsigelbėti leidžia ne smulkūs ir jaukūs „medicinos SPA-salonai“ su lanksčia nuolaidų sistema ir bonusais pastoviams klientams, bet milžiniškos ligoninės su lovų pertekliu.

Pagrindinis globalios pandemijos „luzeris“ – Jungtinės Valstijos, kurie nuolat atrodė „landsbergiečiams“ maksimalaus valstybės pasitraukimo iš socialinės srities idealu, kai mokamų paslaugų rinka nugali „sovietų“ valstybinę sveikatos apsaugą.

Šalis yra neabejotinas lyderis pasaulyje pagal COVID-19 užsikrėtimų skaičių, pagal mirties atvejų skaičių, pagal užsikrėtimų ir mirčių atvejų tūkstančiai žmonių skaičių. Niekas pasaulyje net negali priartėti amerikiečių antirekordų, jų patirtis – „išskirtinė“ ir beprecedentė.

Žiniasklaidoje pilna naujienų, kaip „COVID-19“ aukų lavonai guli Niujorko lavininėse dar nuo kovo mėnesio, nes nėra laiko juos palaiduoti, ir tai tęsiasi be galo ilgai. Legendinė amerikiečių privati medicina su šiuo iššūkiu akivaizdžiai negali susidoroti.

Atvirkščiai, koronavirusas yra beveik nugalėtas Rytų Azijos valstybėse, kur buvo masinė valstybinė mobilizacija. Antrosios bangos ten nėra išvis: naujų užsikrėtimo atvejų beveik neregistruojama. Galima save raminti mintimis, jog „kinų komunistai slepia tiesą“, bet lygiai tokia pat padėtis susiklostė Jungtinių Valstijų šalyse-sąjungininkėse – Japonijoje, Singapūre ir Pietų Korėjoje, kur, panašiai kaip ir Kinijoje, egzistuoja visuotinė mobilizavimosi sveikatos apsauga.

Tarpinė padėtis dabar matoma buvusiose socialistinėse šalyse ir postsovietinėse valstybėse. Bet visuotinės sveikatos apsaugos sistemos jose išliko, deja, gerokai nukentėjusios nuo rinkos „optimizacijos“ dešimtmečių. Jų tvirtumo užteko tam, kad sutikti pirmą koronaviruso bangą daug oriau, nei Amerika bei Senoji Europa, bet antrai bangai atėjus jėgos išseko.

Lietuva – akivaizdus pavyzdys. Pavasarį tarybų laikų disciplinos ir socialistinės medicinos likučiai leido Baltijos šalims sugalvoti eilinę „laimės istoriją“, neva jos susidorojo su pandemija geriau už visas likusias ES šalis. Bet po to rezervai išseko, Šengeno zonos sienos atsidarė, atėjo ruduo ir... voilà!

Pagal kvailumą ir nesąmoningumą šitas sprendimas net pralenks Ignalinos AE uždarymą, kurią „landsbergiečiai“ sustabdė ekonominės krizės metu, kai atėjo į vyriausybę praeitą kartą. Atominė elektrinė, lygiai kaip ir valstybinė sveikatos apsauga, irgi buvo „okupacijos paveldu“. Nuo vieno paveldo Sąjūdžio siekėjai išsivadavo – išsivaduos ir nuo antro.

Trečias „okupacijos paveldas“ – negalintys emigruoti iš Lietuvos pagyvenę Lietuviai – mirs patys save. Nes neatitiks medicinos paslaugų rinką.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 5 — id: `scraped:rubaltic_lt:785287f1ee843dba`

**Title:** Baltijos šalys įžengė į išgyvenimo po išėjimo į pensiją laikotarpį

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvių bendruomenės senėjimo rodiklis yra dukart didesnis, nei ES vidurkis, teigia Vyriausybės strateginės analizės centro darbuotojai. 2050-iems metams daugiau nei pusė Baltijos respublikos gyventojų bus vyresni kaip 50 metų žmonės. Su panašiomis problemomis susiduria Latvija, kur renkami parašai tam, kad paremti tėvų iš daugiavaikų šeimų teisę anksčiau išeiti į pensiją. Bet spręsti demografines problemas vyriausybė nesiruošia: pinigų tam turi atsirasti tik 2022 metais.

„Mes atlikome analizę ir matom, kad dabar valstybė neturi programos, kuri leistų susidoroti su būsimais iššūkiais ir pasinaudoti galimybėmis. Yra atskirų programų, priemonių, bet visos jos yra išskaldytos tarp skirtingo svarbumo programų, išskaldytas yra ir jų finansavimas. Valstybė turi būti suinteresuota tokios programos pasirinkimu ir įgyvendinimu“. – taip Vyriausybės strateginės analizės centro atstovė Indrė Pusevaitė komentuoja naujieną dėl spartaus lietuvių bendruomenės senėjimo.

Tačiau ar galima tai pavadinti naujieną? Demografinės problemos lydi Baltijos šalis nuo nepriklausomybės atgavimo, ir žurnalistai tik kartoja bendrai žinomus faktus: gimstamumas žemas, mirtingumas aukštas, emigracija – už leistinos ribos. Situacija nesikeičia metais ir net dešimtmečiais.

Naujiena galima, ko gero, pavadinti tik tai, kad Indrė Pusevaitė atrado kažkokias perspektyvas, kurias Lietuvos priešakyje atveria nacijos senėjimas: „Viešoje erdvėje visi per dažnai yra apimti nėrimų dėl finansinių apribojimų, bet skiria mažai dėmesio galimybėms“. Na žinoma! Senėjanti bendruomenė sukuria naują prekių ir paslaugų rinką. Kuo daugiau šalyje pagyvenusių žmonių, tuo daugiau pinigų čia gali užsidirbti vakarų farmacijos įmonės (nes organizmui senėjant, didėja žmogaus vaistų poreikis).

Be viso to Pusevaitė kalba apie kažkokią naujovišką darbo santykių modelį. Išvystysim jos mintį. Kuo senesnis tampa darbuotojas, tuo mažiau darbo jis gali atlikti kokybiškai, tuo dažniau jis serga, tuo aukštesnė yra rizika gauti gamybinę traumą. Čia Pusevaitė nemeluoja, tai iš tikrųjų yra naujas modelis. Tik pažengusios šalys daro viską įmanomą, kad įdiegti kitokį modelį: jaunimas dirba, senoliai gauna pensijas.

Nemenki yra pagunda apkaltinti Lietuvos tautos senėjimu „sovietų okupantus“, tačiau tam nėra nei menkesnio preteksto.

Šiandien šalies gyventojų pusė yra vyresni kaip 44 metų žmonės. Amžiaus viduriui, anot Europos komisijos prognozių, šitas rodiklis pasieks 51 metų. Vyresni už lietuvius bus tik italai, portugalai ir kroatai. Bet šitie apskaičiavimai yra labai apytiksliai: Lietuvą tikriausiai gali atsidurti „lyderių“ trejetuke...

Kaip šalies valdžia sprendžia demografinę problemą? Jų veiklos rezultatai kalba patys už save. Esant aukštam bedarbystės lygiui (14,9%), darbo rinkoje užfiksuotas atvirų vakansijų rekordinis skaičius. Žmonės tiesiog nenori ten įsidarbint ir renkasi gauti kuklias bedarbystės išmokas. Tokios taktikos greičiausiai laikosi lietuvių „sugrįžėliai“, kurie dėl koronaviruso pandemijos neteko darbo vakarų Europos šalyse. Tėvynėje jie ketina perlaukti, kol pasibaigs pandemija, - nėra jokios prasmės sunkiai dirbti už menką atlyginimą. Ir tuo labiau, kai pati vyriausybė duoda pinigų pragyvenimui.

Tėvynėje jų sulaikyti niekas nemėgina. Atvirkščiai, bedarbystės pašalpų sistema leidžia gyventi laukiant greitos emigracijos.

Latvijoje reikalai klostosi panašiai. Vietiniai demografai laukia, kad šiemet gimstamumas pražengs istorinį antirekordą. Anot turimos dinamikos metų pabaigai gali būti užregistruota vos 18 tūkstančių naujagimių. Tai bus pats žemiausias rodiklis nuo 1920-ųjų metų, kai Latvijoje buvo pradėta nagrinėti tokią statistiką.

Kuomet Latvijoje pašalpa šeimai, turinčiai tris vaikus, sudaro 134 eurus, kaimyninėje respublikoje išmokos dydis – 520 eurų. „Estijos biudžetas šiek tiek didesnis už Latvijos, bet ne triskart. Tai yra politinė valia“, - yra įsitikinęs Mežs.

Latvijos ministras pirmininkas Arturas Krišjanis Karinšas žado situaciją ištaisyti. Nuo 2022 metų šalyje anonsuojama šeimos paramos sistemos reforma, kurios dėka ketinama padidinti pašalpas šeimoms. Ilmars Mežs neabejoja, kad tai yra teisingas žingsnis, bet rezultatas nežada būti žymu: Latvija tiesiog sustabdys naujagimių skaičiaus mažinimą. Beje, nėra jokios garantijos, kad Karinšo paskelbtos pašalpų didžiai taps realybe.

„Apie demografiją daug pasakyta, daug dokumentų paruošta, bet šalyje yra vienas pagrindinis politikos dokumentas – biudžetas. Ir kai šeimos politika nėra tvirtinama indėliais 2021 metų biudžete, viskas, kas buvo pasakyta šia tema, telieka tuščiais plerpalais“, - konstatuoja Mežs.

Latvių žurnalistas ir rašytojas Otto Ozols ragina atkreipti dėmesį į kitą faktą: pagrindinė gyventojų skaičiaus mažėjimo priežastis yra ne „natūralus nykimas“, o migracija. Todėl disbalanso tarp mirusių ir naujagimių sulyginimas nieko iš esmės nepakeis. Padėti gali tik Latvijos darbo rinkos atidarymas trečiųjų šalių žmonėms.

„Iš Ukrainos, iš Baltarusijos darbo jėga gali atkeliauti, - spėlioja Ozols. – Nemanau, kad tai yra pavojus Latvijai, tai yra protingi, išsilavinę žmonės. Susirūpinimą kelia tai, kad jeigu jie atvažiuos čia, tai po vienos-dviejų kartų šių žmonių skaičius gali viršinti latvių skaičių. Aritmetiškai. Jeigu dabar Latvijoje apie 200 tūkstančių jaunų potencialių tėvų, o iš Ukrainos ir Baltarusijos kasmet atkeliaus 10-20 tūkstančių žmonių, rusakalbių skaičius čia greitai padidės. Ir kalbantis latvių kalba taps mažuma“.

Žodžiu, tai ne išeitis. Kam mums reikalinga Latvija, kuri nebebus latviška?

„Man liūdna tai sakyti, bet anot skaičių ir rodyklių po kelių kartų su latvių tauta galima bus atsisveikinti. Mes tapsime istorija, kaip lyvai ir kuršiai“, - sielvartauja Ozols.

Labiausiai stebina tai, kad „okupacijos“ metu, kai, neva, buvo įgyvendinamas Baltijos tautų genocidas, latvių išmirimą negalima buvo net įsivaizduoti. Tarybų valdžios dėka jų vis daugėjo.

Ir šiomis aplinkybėmis Nacionalinio aljanso pirmininkas Raivis Dzintars paskelbė konkursą „Latvių Latvija – 2040“: jaunimui siūloma raštu apsvarstyti, kokia bus jų šalis po 20 metų. Skamba lyg pasityčiojimas...

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 6 — id: `scraped:rubaltic_lt:689a267e8756da24`

**Title:** Lenkai ir rusai taps „Putino penktąja kolona“ Lietuvoje

**Source:** rubaltic_lt (propaganda)

**Text:**

```
„Lietuvos lenkų rinkimų akcija-Krikščioniškų šeimų sąjunga“ (LLRA-KŠS) reikalauja pripažinti negaliojančiais Lietuvos Seimo rinkimus. Lietuvos tautinėms mažumoms atstovaujanti partija mano, kad valdžią remianti žiniasklaida prieš ją paskelbė informacinį karą, dėl ko sąjunga nesugebėjo įveikti 5% barjero. Lietuvos valdžios antipatija šalies lenkams ir rusams seniai pažįstama, o po frakcijos Seime praradimo šalies tautinės mažumos gali tapti „atpirkimo ožiu“, ypač jei sekančią vyriausybę sudarys konservatorių partija.

„Dėl šiurkštų įstatymo pažeidimų LLRA-KŠS nukreipė skundą į VRK, kad rinkimai daugiamandatėje rinkimų apygardoje būtų pripažinti negaliojančiais“, - paskelbė „Lietuvos lenkų rinkimų akcijos“ lyderis Valdemaras Tomaševskis. Anot Tomaševskio, jo partija neįveikė penkių procentų barjero per Seimo rinkimus spalio 11 dieną dėl persekiojimų, kuriuos prieš LLRA-KŠS skatino valdžią remiantys žurnalistai.

Tomaševskis persekiojimais apkaltina konkrečiai televizijos kompaniją Laisvės TV ir žurnalistą Andrių Tapiną.

Atidžiai išnagrinėjus, paaiškėja, kad šita tema neapsiriboja politiko ir žurnalisto konfliktu, nes Andrius Tapinas – ne vien tik žurnalistas, bet svarbus Lietuvos prezidentūros mediaprojektas, kuriam didelę įtaką turi konservatorių partija. Šitam „nuomonių lyderiui“ daugelį metų buvo skiriamos lėšos ir jėgos, kad tik sukurti XXI amžiaus informacinę aplinką atitinkantį Lietuvos valdžios propagandos ruporą.

Prieš tris metus buvo net labai ambicinga pastanga išgarsinti Tapiną tarp rusakalbės auditorijos ir padaryti „nuomonių lyderiu“ Rusijoje. Nesigavo, žinoma, bet valdžios propagandos ruporą pačioje Lietuvoje sukūrė.

Tokiu būdu turime ne vien tik Tapino ir Tomaševskio konfliktą.

Lietuvos tautinės mažumos buvo eilinį kartą suvoktos kaip grėsmė šalies oficialiam kursui po rugpjūčio įvykių Baltarusijoje. „Lietuvos lenkų rinkimų akcija“ pasižymėjo tapusi opozicija Vilniaus užsienio politikai, kai pasmerkė Baltarusijos vadovybės nepagrįstus kaltinimus ir paragino nesibarti su kaimynais.

LLRA-KŠS frakcija išvengė dalyvauti balsavime dėl Lietuvos Seimo antibaltarusiškos rezoliucijos, kuria Baltarusijos prezidentas Aleksandras Lukašenka buvo paskelbtas neteisėtu, o buvusi prezidento rinkimų kandidatė Svetlana Tichanovskaja – „Baltarusijos tautiniu lyderiu“. Atsižvelgiant į sekančius įvykius galima įspėti, kad nulemiančių užsienio politiką konservatorių kantrybė išseko. Nors konservatoriai ir atstovauja opozicijai, bet kontroliuoja visas valdymo sritis, už kurias atsako Lietuvos prezidentas.

Ne dievai žino kokia užduotis lietuviškai „demokratijai“, kuri pasižymėjo savo disciplina. Lietuvos politinėje istorijoje buvo atvejų, kai prezidentą rinkdavosi pagal JAV nurodymus, neatsižvelgdami net į daugybės rinkėjų balsus. Po tokių pokštų neleisti įveikti 5% barjero partijai, kuri ir anksčiau balansavo ant patekimo į Seimą slenksčio – niekniekis.

Toliau viskas žado būti dar smagiau. Pagal Seimo rinkimų pirmo turo rezultatus konservatoriai turi galimybių grįžti į valdžią ir vadovauti vyriausybei. „Landsbergiečių“ požiūris į tautines mažumas abejonių nesukelia.

Prieš dešimt metų, kai konservatoriai praeitą kartą vadovavo vyriausybei, taip jau buvo. Netitulines tautas tuomet ištiko priverstinis sulietuvinimas, buvo uždaromos lenkų ir rusų mokyklos, draudžiama vadinti tautinių mažumų kompaktiško gyvenimo vietas pavadinimais gimtąja kalba ir reikalaujama savo vardus ir pavardes pertvarkyti pagal lietuvių kalbos rašymo ir tarimo taisykles.

2012 metais nacionalinio konflikto įtemptumas pradėjo nykti, nes konservatoriai pasitraukė iš vyriausybės ir „Lietuvos lenkų rinkimų akcija“, kuri suvienijo lenkų ir rusų jėgas, įveikė penkių procentų barjerą, sukūrė savo frakciją Seime ir net pateko į vyriausybę. Valstybės politikai LLRA įtakos beveik neturėjo, bet lenkų buvimas valdančiojoje koalicijoje žymiai sumažino įtempimo laipsnį tarp Lietuvos ir Lenkijos, kas Vilniuje laikoma reikšmingu užsienio politikos laimėjimu.

Deja dabar lenkų ir rusų politikų aljansas iš sisteminių jėgų sąrašo buvo pašalintas, „landsbergiečiai“ su didele tikimybe grįžtą į ministerijų postus, o prielaidos sąlygoms, kai „neištikima penktoji kolona“ priverstinai yra paverčiama patriotiškais lietuviais, yra seniai susiklosčiusios.

Viskas, kam jų užtenka – atitraukti gyventojų dėmesį nuo realių problemų ir nukreipti į prisigalvotas. Lietuvos gyventojų daugumai būdingos ksenofobijos išnaudojimas ir lenkų ir rusų paskelbimas vidaus priešais puikiai tinka tokiam atitrūkimui.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 7 — id: `scraped:rubaltic_lt:f429058d396d7cda`

**Title:** Rinkimai Lietuvoje: konservatoriai švenčia pergalę

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos Vyriausioji rinkimų komisija (VRK) skelbia Seimo rinkimų rezultatus. Straipsnio paruošimo metu buvo suskaičiuoti beveik visų rinkimų apylinkių balsai. Rezultatus negalima pavadinti sensacingais, bet jų neišpranašavo nei viena sociologinių tyrimų tarnyba: per rinkimų pirmą turą neabejotinai nugali opozicinė partija „Tėvynės sąjunga - Lietuvos krikščionys demokratai“ (TS-LKD). Tuo labiau, konservatoriai pirmauja daugybėje vienmandatinių apygardų ir rimtai pretenduoja į valdančiosios daugumos formavimą.

Pagal pirmo rinkimų turo rezultatus TS-LKD surenka 24,80% balsų ir gauna Seime 23 mandatus. Toliau eina valdančioji „Lietuvos valstiečių ir žaliųjų sąjunga“ (LVŽS) su 17,50% balsų. Pačioje partijų dispozicijoje nėra nieko keisto, nes pastarieji sociologiniai tyrimai rodė, kad konservatoriai gali nugalėti. Bet „Vilmorus“ ir „Spinter tyrimai“ nurodydavo minimaliausią skirtumą tarp rinkimų lenktynės lyderių, o Baltijos tyrimai iš vis prognozavo „valstiečių“ neabejotiną pergalę.

Kitaip tariant, nei viena ori sociologinė tarnyba rinkimų išvakarėse nedavė maždaug tikslios prognozės.

Vis dėlto, šitas paradoksas turi logišką paaiškinimą. Tie patys lietuvių sociologai perspėdavo, kad jų apklausos gali būti nerelevantiškos dėl to, kad jos neatsižvelgia į skirtingų partijų elektorato mobilizaciją. „Vilmorus“ išaiškino, kad 61% TS-LKD šalininkų ketino atlikti savo pilietišką pareigą spalio 11 dieną. Tuomet, tarp „valstiečių“ šalininkų tokių buvo vos 42%.

Netiesiogiai tai įrodo faktą, kad pirmame rinkimų ture aktyvumas sudarė vos 47,6% - tai yra 3% mažiau, nei prieš keturis metus. Už visą Lietuvos nepriklausomybės istoriją tai yra vienas silpniausių rezultatų.

Ekspertai kaltina koronaviruso epidemiją, kuri atbaidė tam tikrą rinkėjų dalį nuo atvykimo į rinkimų apylinkes. „Reikia „pridėti“ kažkokį procentą, tiesiog [žmonės] bijodavo atvykti balsuoti, nes yra tam tikra baimė užsikrėsti“, - konstatavo Lietuvos karo akademijos profesorius Juratė Novagrockienė. Sunku su tuo nesusitikti.

„Stebuklų nėra. Buvo daug vilčių, bet bet kurioje valstybėje aktyvumas auga tuomet, kai žmonės galvoja, kad rinkimai yra svarbūs ir gali daug ką pakeisti. Pasirodė, kad šitie rinkimai lietuviams nebuvo svarbūs, gal paveikė ir tai, kad anksčiau rinkėjai per rinkimus ieškojo kažko naujo, o šitą kartą nebuvo jokios ryškios partijos“, - spėlioja Vilniaus Universiteto Tarptautinių santykių ir politinių mokslų instituto politologas Mažvydas Jastramskis.

„Ryškios partijos“ vaidmuo 2016 metais kaip tik ir atliko „Lietuvos valstiečių ir žaliųjų sąjunga“. Jai pasisekė sužlugdyti esamą dvipartinę sistemą, kurioje viešpatavo konservatoriai ir socialdemokratai. Deja, šalies vystymosi vektorius po šitos rinkimų revoliucijos nepasikeitė.

Praeitais metais Lietuvos Ministras Pirmininkas Saulius Skvernelis sakė, kad prezidento rinkimuose rinkėjas privalo įvertinti „valstiečių“ vyriausybės veiklą. Įvertinimas pasirodė nepatenkinamas: LVŽS kandidatas – pats Skvernelis – net nepasiekė antro turo. Dabar valdančioji partija gavo iš lietuvių eilinį „dvejetą“.

Nes „dėdulė“ Landsbergis savo partiją surengė pagal sektos principus. Jos adeptai visuomet yra mobilizuoti, motyvuoti ir tiksliai žino, kur reikia rašyti „paukščiuką“ biuletenyje. Į rinkimų apylinkes jie atvyks bet kuriuo oru ir bet kuriomis epidemiologinėmis aplinkybėmis.

Panašią partiją-sektą Ukrainoje renka ukrainiečių „tautos galva“ – Petras Porošenka. Po gėdingo pralaimėjimo Zelenskiui daugelis ekspertų pranašavo Porošenkai greitą politinę „mirtį“. Bet eks-prezidentas yra gyvesnis už gyvus. Jo partijos reitingai nesimažėja, nes jis sugebėjo „užcementuoti“ savo elektoratą. Tai leidžia Porošenkai tikėtis optimizmo iš ateities.

Dar viena mažytė Lietuvos rinkimų sensacija – Darbo partijos rezultatas, kuri užėmė trečią vietą (9,51%). Rinkimų išvakarėse buvo aišku, kad jinai lengvai įveiks 5% barjerą, bet vargu ar pretenduos į „bronzą“. Ir galų gale „darbiečiai“ per kelias procento dešimtąsias pralenkė socialdemokratus. Pastariesiems tai yra itin skaudus smūgis.

Penkių procentų ribą per pirmą turą taip pat įveikė Laisvės partiją (8,98%) ir Liberalų judėjimas (6,77%) – potencialūs konservatorių partneriai. Vis dėlto, kol kas nėra tikimybės, jog TS-LKD tikrai taps naujos Seimo daugumos branduoliu.

Centro-kairiąją koaliciją gali sudaryti „valstiečiai“, socialdemokratai ir Darbo partija. Tokį variantą, besiremdamas rinkimų rezultatais, paskelbė Saulius Skvernelis. Jis taip pat išreiškė viltį, kad į Seimą pateks ir dabartiniai „jaunesnieji“ LVŽS partneriai – „Lietuvos Lenkų rinkimų akcija – Krikščioniškų šeimų sąjunga“ (LLRA-KŠS) bei Lietuvos socialdemokratų darbo partija (LSDDP). Deja, nei viena nesurinko 5%. Tai objektyviai sukomplikuoja „valstiečių“ užduotį sukurti naują daugumą.

Rinkimų rezultatai vienmandatinėse apygardose Skverneliui ir kompanijai irgi nesukelia optimizmo. 68 apygardose vyks antras turas, 35 iš jų pirmauja konservatoriai. Matyt, TS-LKD vadovybėje padarė tinkamas išvadas po praeitos Seimo rinkimų kampanijos, kai „valstiečiai“ nugalėjo savo oponentus mažoritarinio atstovavimo dėka.

Dabar ta pati istorija gali pasikartoti bet visiškai atvirkščiai: pagal vienmandatines apygardas konservatoriai gaus daugiau vietų Seime, nei pagal sąrašus. Tuomet koalicijos formavimo iniciatyva priklausys jiems.

Kol kas tiksliai konstatuoti galima tai, kad vienoje komandoje nesusigyvens „valstiečiai“ ir konservatoriai.

Demokratija šiuo atveju apsiriboja galimybe pasirinkti politikus, kurie ves šalį iš anksto paskirta kryptimi.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 8 — id: `scraped:rubaltic_lt:92a328d9461b0e62`

**Title:** Rinkimai be pasirinkimo: Lietuva renkasi Seimą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvoje greit įvyks eiliniai Seimo rinkimai. Į pergalę pretenduoja dvi politinės jėgos: vyraujanti „Lietuvos valstiečių ir žaliųjų sąjunga“ (LVŽS) ir „Tėvynės sąjunga – Lietuvos krikščionys demokratai“ (TS-LKD). Lemiamos valandos išvakarėse intriga išlieka, o išprognozuoti naujos koalicijos formatą šiandien, greičiausia, nesugebės nei vienas ekspertas. Bet lietuviški rinkimai nebus dėl to mažiau nuobodūs.

Baltijos valstybės neseniai parengė kelius visuotines sociologines apklausas. Jų duomenys skiriasi.

„Baltijos tyrimai“, kurie nagrinėja rinką ir viešąją nuomonę, teigia, jog rinkimų lenktynės lyderis - LVŽS, už kurį yra pasiruošę balsuoti 21,2% rinkėjų. Opoziciją sudarantys konservatoriai surenka tik 16,3%, socialdemokratai - 12,8%. Penkių procentų ribą taip pat įveikia „Liberalų judėjimas“ (8,3%), „Darbo partija“ (8,1%), „Laisvė ir teisingumas“ (7,3%) ir „Lietuvos Lenkų rinkimų akcija – Krikščioniškų šeimų sąjunga“ (5,3%).

Jeigu „Baltijos tyrimų“ duomenys atitinka realybę, į Seimą pagal sąrašus pateks 7 politinės jėgos. Tiek pat partijų dabar sudaro kaimyninės Latvijos parlamentą. Ir tai yra ryškus šalies politinės sistemos susiskaldymo ir rinkėjų sumišimo požymis.

Kita ori sociologinių tyrimų tarnyba, „Vilmorus“, taip pat skiria pirmą vietą LVŽS, nors ir išpranašauja sąjungai kuklesnį rezultatą (15,1% balsų). Tuomet „Spinter tyrimai“ vaizduoja kitą padėtį: jų reitingui vadovauja TS-LKD su 14,5% balsų. LVŽS atsiliko vos 0,4%, po jų eina socialdemokratai (8,4%), „darbiečiai“ (7,2%) ir liberalai (6,7%).

Bet bendra tendencija vis tiek pastebima. Politinių jėgų išsidėstymas per keturis metus iš esmės nepasikeitė. Lyderių trejetuką kaip ir anksčiau sudaro „valstiečiai“, konservatoriai ir socdemai.

„Sprinter tyrimai“ lyg specialiai priderinti 2016 metų rezultatams: tais metais TS-LKD proporcingu atstovavimu su menkiausiu pranašumu aplenkė LVŽS (bet pastaroji atgavo savo pranašumą absoliučia dauguma). Trečioje vietoje lygiai taip pat buvo Lietuvos socialdemokratų partija.

Vis dėlto, praeitų Seimo rinkimų kontekstas buvo visiškai kitoks.

Panašiai, kaip JAV valdžią dalija demokratai ir respublikonai, nepriklausomoje Lietuvoje ją visada dalydavo konservatoriai it socialdemokratai. Dešinieji ir kairieji. Du politiniai ašigaliai, kurie viešpatavo tarp rinkėjų.

Kažkur tarp jų „kapstėsi“ likusios partijos. Atrodo, kad jų svajonių riba – atlikti jaunesnio partnerio vaidmenį koalicijoje (jeigu pasiseks, žinoma).

Bet „valstiečiai“ įrodė priešingą.

2012 metais jie surinko vos 2,3% balsų. LVŽS patekimas į Seimą per sekančius rinkimus buvo jau didžiuliu laimėjimu. Bet sąjunga ne vien tenai pateko – įsiveržė! Surinkę vos 0,1% procento mažiau už konservatorius, Karbauskis ir kompanija užėmė 35 iš 71 vienmandatės rinkimų apygardos. Tada paaiškėjo, kad jie taps naujos koalicijos branduoliu.

Daugumą vietų Seime gavo tie, kas neseniai turėjo ten vienintelį atstovą. Tai, žinoma, ne „Tautos tarno“ triumfas per rinkimus Ukrainoje, bet kažkas panašaus.

„Paukščiukas“ prie LVŽS rinkimų biuletenyje tapo „prieglobsčiu“ tiems rinkėjams, kam lygiai įgriso ir konservatoriai, ir socialdemokratai. Tokie rinkėjai sudarė reliatyvią daugumą.

Patenkinti šią užklausą tauta liepė „Lietuvos valstiečių ir žaliųjų sąjungai“, kuri šią užduotį sėkmingai sužlugdė.

Pirmiausia, LVŽS gavo stiprią opoziciją, kurią sudarė konservatoriai. Ko gero, net stipresnę už pačią valdžią. Panašiai kaip Vladimiras Zelenskis tapo Petro Porošenkos Ukrainos prezidentu, lietuvių „valstiečiai“ pradėjo vadovauti Vytauto Landsbergio šaliai.

Antra, vykdyti kažkokią „revoliuciją“ valdžioje jie net nemėgino. Užsienio politikoje LVŽS nuosekliai tęsė savo oponentų strategiją (konfrontacija su Rusija, Baltarusijos „demokratizacijos“ pastangos, strateginis bendradarbiavimas su Vašingtonu). Neabejotinu prioritetu jiems likdavo išlaidos gynybai ir Lietuvos „energetinės nepriklausomybės“ stiprinimas.

Rinkėjai tuoj įvertins sąjungos veiklą. Mažoritarinio atstovavimo apygardose „valstiečiams“ vargu ar verta tikėtis 2016 metų triumfo. Net jeigu jie gaus reliatyvią vietų daugumą Seime, tai neužtikrins jiems galimybės patekti į valdančiąją daugumą. Koalicija gali būti kaip centro-dešinioji, taip ir centro-kairioji.

Be to, „Vilmorus“ apklausos pažymėjo ganą žemą LVŽS rinkėjų motyvaciją vykti į rinkimus. 61% Landsbergio partijos šalininkų išreiškė pasiryžimą atlikti savo pilietinę pareigą. Tarp socialdemokratų šalininkų tokių buvo 53%, o „valstiečių“ rinkėjai yra dar labiau pasyvūs - 42%.

Tai ir yra atsakymas į klausimą, kokių rezultatų per keturis metus pasiekė Lietuvos Ministro Pirmininko partija. Daugiau nei pusė jos šalininkų abejoja, ar verta jiems atvykti į rinkimų apylinkes. 2016 metais nuvyko – ir kas?

Vėliau vyko prezidento rinkimai. Juose bepartinis Gitanas Nausėda per antrąjį turą sutriuškino TS-LKD kandidatę Ingridą Šimonytę. Konservatoriai norėjo pasirinkti Nausėdą savo atstovu, tačiau jis atsisakė. Suprasdavo, kad formaliai nepriklausomas save iškėlęs kandidatas partinės sistemos krizės aplinkybėmis tikriausiai aplenks ir „valstietį“, ir „landsbergietį“.

Beje, šitą įvaizdį Nausėda besistengia išsaugoti iki šiol. Ir jam neblogai sekasi: ekspertai iki šiol nesupranta, kam jis yra labiau palankus – valdžiai ar opozicijai? Bet Lietuvos prezidentui visai nubūtina sudėti vilčių į ką nors vieną. Kokia koalicija nesigautų po rinkimų, jis su ja susidraugaus.

Palyginus su 2016 metais, balsavimas Lietuvoje nežada jokių siurprizų. Įkvėpimo kupini dėdulės Landsbergio sektos liudytojai balsuos už TS-LKD ir tradiciškai užtikrins jai solidų atstovavimą Seime. Orų rezultatą gaus LVŽS, nes jos rinkėjai tiesiog nemato alternatyvos.

Socialdemokratai tęsia savo lipimą nuo politinio Olimpo žemyn. Jeigu būtų reikalinga aprašyti būsimus rinkimus vienu žodžiu, geriausiai tiktų žodis „nuobodybė“.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 9 — id: `scraped:rubaltic_lt:91c09c67dacce00b`

**Title:** Prieškario Lietuvoje tūkstančiui žmonių teko vos 2 žmonės, turintys aukštąjį išsilavinimą. „Sovietų okupantai“ pradėjo kovoti su neraštingumu

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Pirmi duomenys dėl Lietuvos gyventojų išsilavinimo lygio buvo gauti po 1923 metais atlikto gyventojų surašymo. Du trečdaliai gyventojų (neįskaitant Vilniaus bei Klaipėdos kraštų) buvo priskirti prie raštingų ir pusiau raštingų žmonių, o 32,6% lietuvių buvo laikomi neraštingi (raštingais buvo laikomi žmonės, kurie mokėjo skaityti ir rašyti, pusiau raštingais – mokantys tik skaityti, o taip pat tie, kas nemokėjo nei rašyti, nei skaityti, tačiau galėjo pasirašyti; visi likusieji buvo laikomi neraštingais).

Reikia pabrėžti, kad Lietuvoje nuo šalies valstybingumo atkūrimo pradžios veikė švietimo sistema, kuri buvo susidėta iš nemokamų pradinio ugdymo mokyklų 7-14 metų vaikams ir mokamų vidurinių ir aukštųjų mokyklų.

Mokamas vidurinis (nepilnas vidurinis) išsilavinimas pavertė jį sunkiai pasiekiamu mažaturčiams. Beveik pusė vidurinių mokyklų buvo išlaikoma dvasinių organizacijų dėka.

1933 metais „Lietuvos aidas“ rašė: „Vis tiek atrodo, kad švietimo srityje mes priartėjome tos ribos, peržengti kurią abejotina ar įmanoma... Todėl verta atkreipti dėmesį į susiklosčiusią nemalonią padėtį ir rasti būdą apriboti inteligencijos augimą“.

1939 metais neraštingų žmonių lyginamasis svoris šalyje buvo įvertintas lygus 15%. Pagal statistikos organų duomenis (o šituos duomenis buvo uždrausta viešinti atviroje spaudoje net 1960 metais) prieškario Lietuvoje vienam tūkstančiui žmonių teko vos 2 žmonės su aukštuoju išsilavinimu, 64 žmonės – su viduriniu ar nepilnu viduriniu išsilavinimu ir beveik 30% vyresnių kaip 9 metų gyventojų buvo neraštingi (taip pat Vilniaus krašte, kur neraštingų buvo daugiau nei likusioje Lietuvos dalyje).

Šalies 1939-1940 metų politiniai įvykiai nulėmė ryžtingus pakeitimus visų Lietuvos liaudies ūkio sričių ir institucijų veikloje. Žymi transformacija palietė ir respublikos mokyklinį ugdymą. Lietuvos gyventojai buvo informuoti apie vieną iš Stalino Konstitucijos teiginių, anot kurio kiekvienas TSRS pilietis turėjo teisę gauti išsilavinimą. Be to, mokyklinis išsilavinimas Lietuvoje tapo nemokamas (buvo panaikintas mokestis už studijas progimnazijose bei gimnazijų pradinėse klasėse).

Susidomėjimas išsilavinimu respublikoje kilo iškart, todėl reikėjo platinti mokyklų tinklą. 1940 metais bendrą mokyklų skaičių buvo ketinama padidinti 48 mokyklomis, o 1941 metais – dar 98 naujomis vidurinio ugdymo įstaigomis.

Pirmą kartą Lietuvoje buvo paskelbtas tikslas sukurti vidurines mokyklas suaugusiems.

1940 metais buvo įsteigta 11 tokių mokyklų, 1941 metais jų skaičius neišaugo, bet buvo numatytas jų klasių skaičiaus didinimas. Beje, tokiose mokyklose buvo ketinama įsteigti neraštingumo likvidacijos kursus.

Lietuvos TSR vokiečių kariuomenės okupacija sukėlė tarybinės mokyklinio ugdymo sistemos sustabdymą. Dalis mokyklų buvo uždaryta, o likusiose užsiėmimai vyko nereguliariai, studijos buvo nutraukiamos dėl materialinių sunkumų; daugelis vaikų negalėjo lankyti pradinių mokyklų.

Pagal lietuvių tyrinėtojų duomenis, už 3 vokiečių okupacijos metus buvo panaikintos 682 mokyklos.

Tarybų Lietuvos ekonomikos ir kultūros atstatymas buvo numatytas TSRS liaudies ūkio atstatymo ir vystymosi penkmečio plane (1946-1950). Anot šitą planą buvo žymiai platinamas respublikos mokyklų tinklas, be to omenyje buvo turimas ne vien tik mokyklinio amžiaus vaikų privalomas pradinis ugdymas, bet ir vidurinio ugdymo plėtrą tam, kad paruošti kuo daugiau jaunų žmonių studijoms specialiojo vidurinio išsilavinimo įstaigose ir aukštosiose mokyklose.

Pagal Lietuvos TSR liaudies ūkio 1946 metų plano įvykdymo rezultatus mokyklų skaičius viršijo prieškarinį 20%, be to vidurinių mokyklų (gimnazijų ir progimnazijų) skaičius padidėjo triskart palyginus su prieškario lygiu.

Tarybų valdžios pastangos neraštingumui likviduoti (palyginus su prieškario duomenimis) davė tam tikrus rezultatus. Bet sudėtingi respublikos plėtros socialiniai ir politiniai ypatumai 1940 metais – 1950-ųjų pradžioje vis dar turėjo įtakos, ką atspindi gyventojų surašymo materialai. Statistiniai duomenys liudija: 1959 metų Lietuvos miesto gyventojų, turinčių vidurinį ar nepilną vidurinį išsilavinimą, skaičius sudarė 303 žmonės vienam tūkstančiui gyventojų.

Pirmi šio darbo laimėjimai buvo pažymėti 1970 metais, kai mokyklinis ugdymas Lietuvos TSR pasiekė sąjunginio vidurkio. 1970 metais aštuntą klasę baigė 86,2% moksleivių (sąjunginis vidurkis – 85,5%) nuo įstojusių į pirmą klasę prieš aštuonerius metus; 81,9% (sąjunginis vidurkis – 82,1%) nuo dieninių mokyklų aštuntą klasę užbaigusių moksleivių bendro skaičiaus tęsė studijas (skirtingomis formomis), kurios suteiktų vidurinį išsilavinimą.

Anot lietuvių tyrinėtojus, dauguma respublikos gyventojų tam laikui suprato visuotinio ugdymo būtinumą, ypač kai tam buvo suteiktos visos palankios sąlygos.

Mokyklinio ugdymo vystymasis tarybų Lietuvoje iš didelės dalies skatino tą pagrindą, kurio dėka pavyko per palyginamai trumpą istorinį laikotarpį paversti atsilikusią agrarinę šalį pramonine-agrarine respublika su išplėstu žemės ūkiu ir šiuolaikine pramone, kurios pagrindinės sritys gamindavo produkciją atominėse ir kosminėse technologijose, aviacijoje bei jūrininkystėje. Ir šio progreso varomąja jėga taip lietuvių pokario mokyklos absolventai.

Šaltinis: Kretininas G.V. Mokyklinis ugdymas Lietuvoje ir Lietuvos TSR (20-ieji – 50-ieji XX amžiaus metai) // Baltijos regionas — 2010 — Nr.3.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 10 — id: `scraped:rubaltic_lt:7f16751d0f7062e1`

**Title:** Lietuva mirtinai įsižeidė ant Europos dėl Baltarusijos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos įslėpta skriauda dėl to, kad Europa visiškai ignoruoja Baltijos valstybės veiklą dėl Baltarusijos, galų gale išsiveržė. Lietuvos URM vadovas Linas Linkevičius apkaltino Europos Sąjungą neveiksnumu ir „Vieningosios Europos“ patikimumo suirimu. Baltarusijos krizė Lietuvai tapo priešinga Ukrainos krizei. Jei prieš 7 metus Europa pirmą ir, atrodo, vienintelį kartą savo istorijoje žengė Lietuvos politiniu farvateriu, tai dabar nuo Vilniaus stengiamasi laikytis toliau lyg nuo pašėlusio.

„Kartais reaguojame per lėtai, o mūsų pastangos yra fragmentiškos ir nedaro jokio įspūdžio visuomenei ar valdžioje esantiems žmonėms. Jei nesilaikysime savo nacionalinių įsipareigojimų, tai suskaldys mūsų pačių pamatą. Privalome tvirtai laikytis“, - teigė Lietuvos užsienio reikalų ministras Linas Linkevičius savo interviu britų leidiniui Financial Times, kur jis pasakojo apie ypatingą Lietuvos poziciją Baltarusijos atžvilgiu.

Priminsime, kokia yra tos ypatingos pozicijos esmė. Baltarusijos prezidentas Aleksandras Lukašenka yra nelegitimus, ir jo neteisėtumas yra toks, kad Linkevičius jį vadina buvusiu.

Šiam tikslui Vilniuje jau yra paruoštas laikinas prezidentas – Svetlana Tichanovskaja, kuriai Lietuvos valstybės dėka įrengtas pilnavertis politinis štabas ir suderinti tarptautiniai ryšiai. Tuo atveju, jei Lukašenka atsisakys taikiai perduoti valdžią Tichanovskajai Lietuvai ir Lenkijai tarpininkaujant, prieš jį turi būti skirtos sankcijos.

Lietuva savo sankcijas jau skyrė, pasiskelbusi „batką“ Persona non grata. Vilniaus tradicinis užsienio politikos metodas: parodyti neryžtingiems NATO sąjungininkams, kaip reikia. Lygiai taip pat prieš penkis metus Lietuva pirma pasaulyje oficialiai teikė Ukrainai ginklus tam, kad tęsti pilietinę kovą Donbase. Parodomosios akcijos tikslas buvo toli gražu ne pagalba šoviniais Kijevui, bet galimybė atsigręžti į vakarų šalis su klausiamuoju žvilgsniu: o ko jus laukiat?

„Baltarusijos žmonės neturi jaustis apleisti. Mes turime suteikti jiems perspektyvą būti tarp demokratinių valstybių. Jei jie vykdys reformas, jie tikrai gali tikėtis glaudesnio bendradarbiavimo su ES, kuris atneš naudos visuomenei“, - Lietuvos URM vadovas įtikina europiečius daug įnirtingesnės politikos Baltarusijos atžvilgiu būtinumu. Įtikina, be to, savo interviu Financial Times, tai yra – tos šalies leidiniui, kuri išstojo iš Europos Sąjungos.

Ir tai yra pirma priežastis, kodėl Europa atvirai neskuba apriboti Lukašenkai įvažiavimo galimybę, skelbti Svetlaną Tichanovskają Baltarusijos prezidente ir pradėti geopolitinį Rusijos nulaikymą, jeigu pastaroji nepadarys to pat. Senasis Pasaulis per daug išseko dėl koronaviruso, Brexito ir migrantų tam, kad įsivelti į konfliktą dėl Baltarusijos.

Antra ir pagrindinė europiečių apsimestinio abejingumo Lietuvos iniciatyvoms priežastis yra nulemta puikiai įsisavintos „ukrainietiškos“ patirties, kai 2013 metų antrajame pusmetyje Lietuva per trumpą pirmininkavimo ES tarybai laikotarpį turėjo tikros įtakos Europos Sąjungos užsienio politikai rytų valstybėms. Prisiminimai apie Europos „sėkmės istoriją“ Ukrainoje sukelia tokią pasibjaurėjimą Vakarų Europoje, kad ten atvirai sako: negalima leisti tokios „sėkmės“ pasikartojimą Minske!

Ir viską daro atvirkščiai.

2013 metais vakarų šalys priėmė Rytų Europos direktyvą, anot kurios spręsti Ukrainos ateitį galima tik su Ukraina. Lietuva garsiau už kitus skandavo prieš trišales derybas su Rusija dėl Ukrainos asociacijos su ES. Rusijos interesų per laisvosios prekybos zonos tarp Ukrainos bei ES buvo visiškai nepaisoma, bet ir Ukrainos interesų buvo irgi nepaisoma. Abiejų šalių ilgaamžiai ryšiai europiečių buvo visiškai paniekti, Donbase bei Kryme gyvenančių žmonių nuomonės, kuriems tie Ukrainos ryšiai su Rusija buvo gyvybiškai svarbi, buvo visiškai nepaisoma.

Galų gale gavo tai, ką gavo.

Visų pirma europiečiai aptaria Baltarusijos ir Rusijos ilgaamžių ryšių reikšmingumą, ekonominė sąjunga su Rusija pripažinta Baltarusijos ekonomikos pagrindu, o daugumos šalies gyventojų prorusiškos nuotaikos laikomos lemiančiu faktoriumi.

Po nesėkmingos patirties europiečiai tapo itin atidūs.

Per Ukrainos krizę Europa aiškiai parėmė opoziciją – nuo Ukrainos Aukščiausiosios Rados provakarinių partijų lyderių iki paskutinio eilinio „protestuojančio“. Europos pareigūnai aplankydavo juos Maidane, paskelbė Viktorą Janukovičią nelegitimu, užtat iškart pripažino susiklosčiusios po valstybinio perversmo valdžios teisėtumą.

Ir galų gale europiečiai gavo savo kolektyvinei atsakomybei pačią korumpuotą pasaulio šalį, kuriai neįmanoma vadovauti, nes ten kiekvienas, kas turi ginklą ir lėšų, laiko save vadu, o neadekvati vadovybė negali įgyvendinti nei vieno sprendimo. Tuo tarpu niekada nežinai, ko tikėtis iš šios vadovybės, nes Kijeve viskas yra įmanoma, kad tik paraginti Europą įnirtingiau padėti jiems kovoti prieš „rusišką agresiją“.

Prieš septynerius metus Lietuva su savo bendraminčiais įtikino ES ir NATO, kad reikia bet kokia kaina apginti Ukrainą nuo Rusijos.

Ir, lyg nuo pašėlusio, Europiečiai stengiasi laikytis kuo toliau nuo Vilniaus su jo eilinio „geopolitinio žaidimo“ eiliniu geopolitiniu įsikarščiavimu tam, kad „atriboti“ eilinę postsovietinę valstybę nuo Maskvos.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 11 — id: `scraped:rubaltic_lt:f676075002974920`

**Title:** Putinas prilygino Lietuvos „herojus“ naciams

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Rusijos prezidentas Vladimiras Putinas pasirašė įsakymą dėl piniginių pašalpų Didžiojo Tėvynės karo veteranams skirimo žmonėms, kovojusiems prieš Ukrainos ir Baltijos šalių pokario pogrindžio gaujas. Šiuo žingsniu S. Banderos šalininkai ir „miško broliai“ buvo Rusijos oficialiai prilyginti naciams. Ir tai yra svarbiausias pakitimas Rusijos istorijos politikoje palyginus su Tarybų Sąjunga.

„Pergalės 1941-1945 metų Didžiajame Tėvynės kare 75-mečio proga nutariu 2020 metais skirti vienkartinę 75 000 rublių pašalpą Rusijos Federacijos piliečiams, nuolat gyvenantiems Rusijos Federacijoje, Latvijos Respublikoje, Lietuvos Respublikoje ir Estijos Respublikoje, esantiems Didžiojo Tėvynės karo neįgaliaisiais ir Didžiojo Tėvynės karo dalyviais iš kareivių skaičiaus, vidaus reikalų ir valstybės saugumo organų eilinių ar vadovaujančių kadrų, kurie dalyvavo nacionalistinio pogrindžio likvidavimo operacijose Ukrainoje, Baltarusijoje, Lietuvoje, Latvijoje ir Estijoje nuo 1944 metų sausio 1 dienos iki 1951 metų gruodžio 31 dienos“, - teigiama Rusijos prezidento Vladimiro Putino įrodyme dėl asmenų, kuriems skiriamos Pergalės jubiliejaus progos piniginės pašalpos, sąrašo išsiplėtimo.

Toks sprendimas buvo priimtas pagal Užsienio žvalgybos tarnybos vadovo Sergejaus Naryškino bei kitų jėgos žinybų vadovų pasiūlymą, kurie laikė neteisinga padėtį, kai balandžio pašalpos Didžiojo Tėvynės karo veteranams nebuvo skiriamos kovojusiems prieš kolaboracionistus Tarybų respublikose. Nes pastarieji irgi rizikavo savo gyvybe ir kovojo prieš nacizmą TSRS teritorijoje.

Putinas pritarė tokiems argumentams.

Visi Sovietų Sąjungoje žinojo apie Chatynės tragediją, bet maža kas galėjo atsakyti, kas sudegino 149 baltarusiško kaimo gyventojus. Eilinis Tarybų pilietis žinojo tik tai, kad tai buvo naciai, ir jiems buvo „savaime suprantama„, kad tai reiškia vokiečius. Bet tiesioginiais nusikaltimo vykdytojais buvo Ukrainiečių nacionalistų organizacijos smogikai.

Pokario metais Ukrainos TSR vadovybė kreipėsi į TSKP Centro Komitetą su prašymu neviešinti to fakto, jog ukrainiečiai dalyvavo Chatynės naikinime, kad nepakirsti draugystės su broliška baltarusių tauta. Maskva Tarybų Ukrainos prašymą įvykdė.

Tokia istorija nebuvo išimties atveju.

Tarybinis žmogus, žinoma, žinojo, kad nacių okupuotose teritorijose buvo vykdomas žydų genocidas, bet buvo stengiamasi neviešinti tai, kad nuostatą „galutiniai išspręsti žydų klausymą“ vokiečiai įgyvendino vietos gyventojų „rankomis“. Kai kuriais atvejais Holokaustas išvis vyko be nacių dalyvavimo. Žydų pogromai Lvove bei Kaune įvyko tomis keliomis dienomis, kai miestus jau paliko Raudonoji armija, tačiau dar neužėmė Vermachto padaliniai.

Buvo viešai žinoma, kaip kankindavo ir žudydavo valstiečius, įtartus pagalba partizanams, bet tai, kad šimtus kaimų Rusijos TFSR, Baltarusijos TSR, ir Latvijos pasieniuose panaikino Latvių SS legiono savanoriai, buvo nedaugeliui žinovų atskleista paslaptimi. Leningrado blokados tragedija buvo bendru sielvartu, bet tai, kad marinti badu milijonus žmonių vokiečiams padėdavo estų nacionalistai, nebuvo viešinama.

Toks politinis korektiškumas buvo geranoriško tarptautinės taikos išsaugojimo tikslo nulemtas, bet galiausiai TSRS tai išėjo per pakaušį. Kai „perestroikos“ (TSRS vadovo M.Gorbačiovo pradėtos vykdyti reformos – RuBaltic.Ru pastaba) metu Baltijos šalių separatistai pradėjo kalbėti, kad „miško broliai“ – tai herojai ir kovotojai už nepriklausomybę, kuriuos kraujotroška Stalinas ištrėmė į Sibirą tik už tai, kad jie buvo už laisvę, tarybų bendruomenė net neįsivaizdavo, kaip tai vertinti. Jai niekas nepaaiškino, kad daugumai šių herojų – „kraujuotos rankos“, ir į mišką jie pabėgo nuo pelnytos bausmės.

Masinio TSRS piliečių bendradarbiavimo su nacių okupantais faktų skelbimas paspartino Tarybų Sąjungos skaldymą, nes tai buvo, visų pirma, ideologinis projektas. Kaip tai gali būti, kodėl prieš viešumos epochą mums visko to nepasakojo? Gal ir tiesa, kad per tą karą ne viskas buvo taip vienprasmiška? Gal Baltijos šalių nacionalistus iš tikrųjų represavo tik už tai, kad jie buvo prieš „sovietų okupaciją“? Gal, geriau jau vokiečiai būtų mus nugalėję? Dabar gertumėme Bavarijos alų...

Baltijos valstybėse nekenčia gegužės 9 dieną, ardo tarybų paminklus, surengia Rygoje Latvijos SS legiono maršus ir organizuoja Estijos SS divizijos veteranų suvažiavimus ant Sinimäed kalvų? Tai Estija ir Latvija užima pirmaujančias vietas Europoje pagal vietos gyventojų, per Antrąjį Pasaulinį karą kovojusių Trečiojo Reicho pusėje, dalį.

Ukrainos „patriotai“ sudegina gyvus žmones Odesos Profsąjungų rūmuose? Taigi jie patys laiko save Chatynę sudeginusių „patriotų“ įpėdiniais!

Dabartinių nacių pirmtakai atlikdavo visą „purviną darbą“ už Hitlerį. Tai yra, buvo tokie patys naciai.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 12 — id: `scraped:rubaltic_lt:c99bf93696bd798b`

**Title:** Lietuva išnaudoja protestus Baltarusijoje tam, kad skatinti Europos sankcijas prieš Astravo AE

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Į pirmąjį Astravo atominės elektrinės energobloką buvo pakrautas branduolinis kuras. Apie tai pranešė naujienų agentūra „BelTA“ besiremianti „Gosatomnadzor“ branduolinės saugos reguliavimo skyriaus vadovo Vigeno Maruchiano pranešimu. Masinės protestų akcijos neturėjo įtakos įmonės paleidimo paruošimo renginiams. Net Aleksandro Lukašenkos priešininkai šiandien vengia šitą temą. Ir tik Lietuva nepraranda vilties, kad politinis nestabilumas kaimyninėje šalyje patrukdys paleisti Astravo AE.

Lietuva, ko gero, yra vienintelė šalis, kuri akivaizdžiai turi savanaudišką interesą Lukašenkos pašalinimo nuo valdžios atveju. Nebe pirmus metus valstybė nesėkmingai tęsia kovą prieš Astravo AE. Prieš maždaug mėnesį analitikos portalas RuBaltic.Ru rašė, kad tokios mintys negali neaplankyti Lietuvos politikų: tam, kad nubausti Lukašenką už demokratinių vertybių pasmerkimą Europos Sąjunga privalo boikotuoti atominę elektrinę Astrave.

Prieš rinkimus niekas apie tai garsiai nekalbėjo, bet dabar nėra ko gėdytis.

Europos Sąjunga privalo išgauti iš Minsko sprendimą sustabdyti pirmojo Astravo AE bloko paleidimą dėl nestabilios padėties šalyje – tokią tezę pareiškė rugpjūčio 13 dieną Lietuvos Užsienio reikalų ministerija. Ministerijos vadovas Linas Linkevičius pažadėjo, kad per ES užsienio reikalų ministrų vaizdo konferenciją, skirtą Baltarusijos padėties aptarimui, stengsis atkreipti partnerių dėmesį į šitą problemą.

Nors jokios problemos nėra. Kaip jau buvo paminėta, Astravo elektrinėje protestai praėjo pro šalį. Pranešimai, kad joje prasidėjo maištai, buvo klastotėmis.

Rugpjūčio 14 dieną Lietuvos prezidentas Gitanas Nausėda susitiko su Estijos prezidente Kersti Kaljulaid. Daigiausia svarstė politinę padėtį Baltarusijoje. „Prezidentai sutarė, kad situacija reikalauja išskirtinio dėmesio bei būtinybės sutelkti pastangas, kad represijos prieš taikius piliečius būtų nutrauktos, visi suimtieji paleisti ir pradėtas dialogas su visuomene“, - praneša Lietuvos lyderio svetainė.

Čia pat sakoma apie prezidentų vieningumą pasisakant už sankcijų taikymą Baltarusijai, jeigu situacija valstybėje nepasikeis. Ir būtent šio susitikimo metu Nausėda įtikino Kaljulaid paremti Astravo AE boikotą: „Prezidentas padėkojo Estijai už bekompromisę paramą, vertinant Astravo AE grėsmę bei įsipareigojimą neįsileisti jos gaminamos elektros energijos į Estijos ar ES rinką“.

Įsidėmėtina, kad anksčiau Vilnius negalėjo priversti savo kaimynų atsisakyti prekybos elektra su tomis šalimis, kurios eksploatuoja „nesaugias“ atomines elektrines.

Kodėl būtų neverta pamėginti tai padaryti, jeigu politinė konjunktūra yra tam labai palanki? Anksčiau Lietuva atkreipdavo dėmesį į baltarusių „atominio monstro“ „nesaugumą“ ir kvietė Baltijos vieningumo. Dabar ji turi kitą pranašumą: negalima remti „Lukašenkos režimo“.

Per ES viršūnių nepaprastąjį susitikimą Nausėda iškėlė klausimą visu griežtumu: „Ar gali tokia atominė elektrinė būti priimtina Europos Sąjungai ir ar netraktuotumėme pagamintos tokioje elektrinėje elektros importą susiklosčiusiomis aplinkybėmis kaip savęs sukompromitavusio režimo paramą?“

Žinoma, prekyba su Baltarusija yra „režimo“ parama. Kuo mažiau pinigų turi režimas, tuo silpnesnis jis tampa. Neatsitiktinai Svetlanos Tichanovskajos štabe ragino padaryti Lukašenkai ekonominių nuostolių. Bet Lietuvoje to raginimo neparėmė. „Jeigu kalbame apie sankcijas, yra prasmė svarstyti sankcijas ES mastu. Svarstyti tikslines sankcijas, kurias reikėtų taikyti ne tiek šalies ekonomikai, kiek atskiriems asmenims, kurie yra susiję su rinkimų rezultatų falsifikavimu, su represijomis“, - skelbė Nausėda.

Pats laikas kreiptis į psichiatrą: akivaizdi asmenybės skilimo diagnozė.

Prie kovos su Astravo AE naujojo etapo prisidėjo ir Lietuvos Seimas. Į kaimyninės šalies prezidento rinkimų nepripažinimo rezoliuciją, kuri buvo priimta beveik vienbalsiai, buvo įtrauktas eilinis raginimas spręsti atominės elektrinės klausymą tarptautiniu lygiu.

Koks ryšis tarp atominės energetikos ir rinkimų Baltarusijoje? Lietuvos seimūnai sau šito klausimo neužduoda.

Ko gero pats tiesiakalbis pareiškimas dėl Astravo AE priklauso Lietuvos Ministrui Pirmininkui Sauliui Skverneliui. Iš pradžių jis pakartojo tezę neva situacija šalyje yra papildoma grėsmė atominės elektrinės saugumui, o paskui išreiškė viltį, kad naujoji Baltarusijos valdžia turės „daug racionalesnį“ požiūrį šiuo atžvilgiu.

Ir tam yra pagrindas.

„Aš, žinoma, galiu pasakyti vieną – atominės elektrinės statyba buvo didžiulė klaida. Buvo verta plėtoti alternatyvių energijos šaltinių kryptis – tai yra saulės bei vėjo energija, tai yra energija gaunama iš medienos perdirbimo atliekų deginimo, galų gale, tai galėtų būti turimų šiluminių elektrinių modernizavimas“, - skelbė Valerijus Cepkalo.

Viktoras Babaryka žengė toliau ir pasiūlė organizuoti tarptautinę komisiją, kuri nuspręstų Astravo AE ateitį. Priešpriešinis pasiūlymas – įtraukti į komisiją daugiau lietuvių!

Lietuvos politikai viešai sako išpūstas kalbas apie Baltarusijos tautos atgimimą, apie kovą už demokratiją, apie nepaprastą kelią prie laisvos visuomenės. Bet Baltijos valstybės Ministras Pirmininkas net neslepia, kad šios kovos rezultatais turi pasinaudoti jo šalis.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 13 — id: `scraped:rubaltic_lt:8e15121c37337aba`

**Title:** Antroji koronaviruso pandemijos banga užklups Lietuvą rinkimų laikotarpiu

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Seimo rinkimai Lietuvoje turi įvykti spalio 11 dieną. Vyriausioji rinkimų komisija (VRK) jau priėmė saugumo priemones balsavimo metu. Bet ar jų užteks, kad atlaikyti COVID-19 plitimą? Epidemiologinė būklė Baltijos šalyje nesigerina, o antroji koronaviruso banga, anot ekspertų, užklups Europą kaip tik rugsėjo-spalio mėnesį. Lietuvoje ji gali sukelti rinkimų datos perkėlimą ir paveikti gyventojų rinkimines pirmenybes.

Daugelyje šalių, kurios žengė karantino apribojimų silpninimo keliu, stebimas koronavirusu užsikretusių žmonių skaičiaus augimas. Visai neseniai Danijos sveikatos apsaugos ministras Magnus Heunicke, remiantis Valstybinio infekcinių ligų instituto duomenimis, teigė, kad jo šalį apėmė antroji koronaviruso banga. Beje, ar dera išvis kalbėt apie bangas?

Pasak Kento universiteto virusologijos eksperto Džeremio Rossmano, kol kas nepanašu, kad koronavirusas priklausytų nuo sezoniškumo. Ir pastarųjų mėnesių statistika tai liudija. Viltys į tai, kad saulėti vasaros orai užkirs kelią viruso plitimui, nepasiteisino.

Dėsninga reakcija – tam tikrų apribojimų grąžinimas.

Nuo rugpjūčio 10 dienos atvykusiems į Baltijos šalį iš Lenkijos, Olandijos, Islandijos, Kipro ir Turkijos vėl liepiama izoliuotis dviem savaitėms.

Turbūt, šituo Lietuvos vyriausybė neapsiribos. Eilinį COVID-19 susirgusių skaičiaus šuolį (nepriklausomai nuo to, ar tai antroji banga, ar pirmosios pratęsimas) virusologai prognozuoja jau šį rudenį, tai yra jau už 1-2 mėnesių. Europos šalių vadovybės ruošiasi tam.

„Noriu aiškiai pareikšti, kad antrosios bangos metu mes neketinome sustabdyti visos ekonomikos ar atskirų jos sektorių, - pažymi Lietuvos Ministras Pirmininkas Saulius Skvernelis. – Naujojoje realybėje mes žengsime „saugaus aktyvumo“ keliu – tai yra kaukių nešiojimas, dezinfekcija, saugaus atstumo laikymasis ir kitos priemonės, priklausančios kovos prieš COVID-19 strategijai. Pirmenybė suteikiama maksimaliam individualios apsaugos priemonių vartojimui, o ne apribojimams“.

Akivaizdu, kad Skvernelio „naujojoje realybėje“ Seimo rinkimai privalo įvykti pagal grafiką. Jų datos perkėlimas Lietuvoje net nesvarstomas, rinkimų komisija dirba įprastu grafiku.

Neseniai pasibaigė dokumentų priėmimas – prasideda kandidatų į Seimo deputatus atitinkamumo įstatymams patikra (galutiniai sąrašai bus paskelbti rugsėjo 11 dieną). Prieš tai VRK įtvirtino rekomendacijas bei nurodymus rinkimų dalyviams. Ir komisijos nariai, ir rinkimų stebėtojai, ir savanoriai, ir rinkėjai privalo naudotis individualios apsaugos priemonėmis, kiekvieną balsavimo apygardą ketinama aprūpinti kaukėmis.

Žodžiu, nieko ypatingo.

Galima, pavyzdžiui, sekti Rusijos Federacijos balsavimo dėl konstitucijos pataisų patirtimi, kai referendumas tesėsi kelias dienas. Arba žengti neseniai įvykusių prezidento rinkimų Lenkijoje keliu: gyvenvietėse, kur buvo daug užsikrėtusių, balsavimas vyko paštu. Kiti rinkėjai irgi galėjo pasinaudoti šia galimybe, iš anksto perspėdami rinkimų komisiją.

Rinkimų perkėlimo variantą atmesti, žinoma, negalima. Koronavirusas dar gali padaryti staigmenų Lietuvai ir kitoms šalims. Bet kol kas viskas įrodo, kad po spalio 11-os dienos Baltijos respublikoje susiformuos naujas Seimas.

Visų pirma, pats rinkimų įvykdymo pagal grafiką faktas pažymės tai, kad vyriausybė kontroliuoja padėtį. Valdančiajai partijai tai gali suteikti kelių rinkimų taškų. Antra, nauja sociologija yra palanki valdančiajai „Lietuvos valstiečių ir žaliųjų sąjungai“ (LVŽS).

Iki neseniai viešosios nuomonės apklausos fiksavo konservatorių, t.y. „landsbergiečių“, atstovaujamos opozicijos pirmavimą. Bet birželio mėnesį jų pranašumas prieš „valstiečius“ tapo minimalu (14,3% prieš 13,4%), o liepos mėnesį LVŽS užėmė pirmaujančią poziciją.

Vis dėlto, priešrinkiminė sociologija nėra tokia akivaizdi. Nurodytus tyrimus atliko „Vilmorus“ įmonė. Kitos įmonės – „Spinter tyrimai“ – birželį atliktų tyrimų rezultatai liudija 3,5% konservatorių pranašumą prieš „valstiečius“. Ta pati apklausa liudija, kad žmonių, pritariančių vyriausybės veiksmams, skaičius sumažėjo 6% paliginus su balandžio mėnesio rodikliu. Mes akivaizdžiai matom dvejų visuomenių grupių mažąjį sociologinį rungtyniavimą.

Net jeigu „Vilmorus“ duomenys atspindi realią jėgų išsidėstymą, mažytis „valstiečių“ pranašumas gali išnykti rinkimų dieną, nes jų oponentų šalininkai yra daug aktyvesni: 61% „Tėvynės Sąjungos – Lietuvos Krikščionių demokratų“ (TS-LKD) rinkėjų pareiškė įsitikinimą, kad spalio 11 dieną jie ateis į balsavimo apylinkes. Tarp LVŽS šalininkų tokie rinkėjai sudaro vos 42%. Taigi „valstiečiams“ teks kovoti ne tiek prieš konservatorius, kiek prieš savo rinkėjų pasyvumą.

Spalio 11 dieną Karbauskis ir kompanija sutinka būdami „geroj formoj“: pirmą išbandymą koronavirusu jie įveikė puikiai.

Bent jau geriau, nei Italijos, Ispanijos ar JAV vyriausybės. Kol kas sunku įvertinti Lietuvos ekonominio smukimo rimtumą, bet ir čia niekas nežada katastrofos. Laukiamas BVP sumažinimas 7-8% skaičiuojant metams – toli gražu ne blogiausias scenarijus.

Todėl šiomis aplinkybėmis konservatoriams nėra dėl ko priekaištauti oponentams. Tenka priešrinkiminiais tikslais išnaudoti skandalus aplink sveikatos apsaugos ministrą Aurelijų Verygą ir kovos su Astravo AE pralaimėjimą, už kurį neva yra atsakinga Lietuvos Energetikos ministerija. Jeigu rinkimai bus perkelti, „valstiečių“ kritika taps nuoseklesne.

Vos per kelius mėnesius prezidentas Andrzejus Duda iš priešrinkiminių varžybų favorito pavirto kandidatu, kuris beveik „iškando“ nugalėjimą rinkimuose iš savo oponento rankų. „Lietuvos valstiečių ir žaliųjų sąjunga tikrai nenorėtų kartoti tą patirtį.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 14 — id: `scraped:rubaltic_lt:66ef7d21d449afcd`

**Title:** Lietuva atsilygina riejimaisis ir ginčais už energetikos projektus

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuva padavė naują ieškinį prieš prancūzų energetikos įmonę „Veolia“. Vilniaus teisminiai ginčai su Prancūzijos energetikais tęsiasi jau daugelį metų iš eilės ir įrodo tai, kad Rusijos „Gazpromo“ konfliktas su Lietuva buvo tipinis o ne išskirtinis reiškinys. Visi didieji energetikos projektai Lietuvoje lydimi riejimųsi, korupcijos skandalų ir teisminių ginčų.

1990 metų pabaigoje – 2000 metų pradžioje Lietuva sumanė eilinį propagandinį verslo projektą „energetinei nepriklausomybei nuo Rusijos“ gauti. Respublikos vyriausybė sumanė įvykdyti šilumos tinklų neregėto masto modernizaciją ir nusprendė surasti šitiems tikslams plačiai žinomą vakarų įmonę, kuri pertvarkytų lietuvių šilumos teikimo sistemą nuo tarybinio tipo į europietišką.

Garbinga misija buvo patikėta Prancūzijos energetikos milžinui – „Veolia“ grupei, vienai iš stambiausių Europos įmonių, kuri specializuojasi komunalinių paslaugų ir energetikos srityse. Propagandos kampanija dėl „Veolia“ atvykimo į šalies rinką tapo būsimos SGD terminalo „Independence“ nuomos epopėjos repeticija. Nauja „sėkmės istorija“: atlydėjo į Lietuvą stambų investorių, pasiekė užsienio ekonomikos ryšių diversifikacijos toje ekonomikos srityje, kur nuo „tarybų okupacijos“ laikų vyravo Rusija.

Lietuvos energetikos „sėkmės istorija“ pasibaigė kaip įprasta.

Prancūzai Tarptautiniame investicijų arbitražo teisme Vašingtone pareiškė neva jų investicijos į Lietuvos energetiką nukentėjo dėl korumpuotų Baltijos šalies politikų ir valdžios įstaigų. Įmonė apkaltino Vilnių „nesąžiningu elgesiu ir užsienio investicijų pasisavinimu“.

Bendra nuostolio suma, kurią „Veolia“ patyrė Lietuvoje, pasak įmonės sudarė 118 milijonų eurų.

Lietuvos vyriausybė kreipėsi į teismą su priešieškiniu, įvertindama Lietuvos nuostolį dėl prancūzų veiksmų 200 milijonams eurų. Vilnius apkaltino Prancūzijos koncerną dirbtiniu kainų elektrai paaukštinimu (kai „sėkmės istorija“ su stambaus europiečių investoriaus atvykimu į šalį buvo pradedama įgyvendinti, lietuvius, žinoma, įtikindavo, kad šilumos tinklų modernizacija padės sumažinti sąskaitas už komunalines paslaugas).

Kalbama apie 2016-2017 metų įvykius.

Respublikos Energetikos ministerija priekaištauja buvusiems partneriams dėl piktnaudžiavimo Lietuvos energetikos rinkoje, kurie atsiėjo ne vien tik 240 milijonus eurų, bet ir smūgį reputacijai.

„Toks įvykis Lietuvoje yra beprecedentis, ir tai yra vienas pirmų atvejų, kai vyriausybė civiline tvarka siekia gauti iš užsienio investoriaus bei su juo susietų asmenų kompensacijos už padarytą visos šalies ekonomikai nuostolį. Korupciniai veiksmai, prekyba įtaka, nesąžiningos, ribojančios konkurenciją sutartys padaro didelę žalą valstybės ekonomikai ir reputacijai, todėl siekiama to, kad nuostolis padarytas tokiais veiksmais būtų atlygintas“, - teigiama Energetikos ministerijos pareiškime.

Oficialaus Vilniaus pretenzijos prancūzų įmonei labai primena Lietuvos ginčus su „Gazpromu“, kurie vyko tuo pačiu laiku, kaip ir ginčai su „Veolia“, ir pasibaigė šiais metais visuotiniu ir galutiniu pralaimėjimu Stokholmo arbitraže.

Tie patys pernelyg paaukštinti tarifai, konkurencijos apribojimas, piktnaudžiavimas monopolija. Nebent politiniu spaudimu neapkaltino. Užtat dabar pareiškė žalą reputacijai.

Aplink ginčus su „Gazpromu“ buvo kur kas daugiau triukšmo nei dėl skandalų su „Veolia“, todėl galėjo susidaryti įspūdis, kad Lietuvos ir Rusijos dujų monopolisto konfliktas yra išskirtinė situacija.

Iš tikrųjų Lietuvai toks elgesys yra visiškai būdingas.

Aukščiau paminėtas SGD-terminalas sukėlė teisminių ginčų tarp „Independence“ vadovybės ir jo stambiausio bet priverstinio produkcijos vartotojo – cheminių trąšų gamyklos „Achema“. Įmonė kreipėsi į Europos Sąjungos teisingumo teismą su skundu prieš „Independence“, kuriame teigė, kad gamykla nuniokojama priverstiniu suskystintų gamtinių dujų įsigijimu, kurios yra gerokai brangesnės už rusiškas dujas.

Tuo pačiu metu „Independence“ sukėlė nesantaiką Baltijos valstybių tarpusavio santykiuose. Latvija ir Estija atsisakė pirkti lietuvių plūduriuojančio SGD terminalo produkciją ir kartu su Suomija sukūrė bendrą energetikos rinką, į kurią nepakvietė Lietuvos.

Paskui paaiškėjo, kad šioje istorijoje Lietuva apgavo Latviją. Anot neformalaus Vilniaus ir Rygos susitarimo europiečių finansuojamas SGD-terminalas Baltijos regionui turėjo tekti latviams, o Lietuvai buvo suteikiamos elektros jungtys su Lenkija ir Švedija, kurioms irgi buvo skiriamos ES dotacijos. Deja, lietuviai nusprendė aplenkti „brolišką tautą“ ir pasigrobti ir elektros jungtis, ir SGD-terminalą. Ryga atsilygino Vilniui ta pačia moneta.

Ignalinos AE Lietuvoje buvo nuspręsta sustabdyti „energetinės nepriklausomybės“ nuo Rusijos vardan, kuomet tikrąja priežastimi buvo Prancūzijos branduolinės energetikos lobistų vyravimas Europos Sąjungoje, bet Vilnius nepasišlykštėjo išlikti ištikimas antirusiškai politikai ir sukėlė eilinį skandalą.

Visagino atominės elektrinės projektas, kurią buvo nuspręsta statyti Ignalinos jėgainės vietoje, pavirto nesibaigiančių priekaištavimų ir riejimųsi eile. Dalis politinių partijų rėmė elektrinės statybą, kitos – priešinosi jai. Europos Sąjunga pinigų atominei elektrinei neskyrė. Latvija ir Estija, susidėjus su kuriomis buvo ketinama statyti Visagino AE, iš projekto išstojo, nes taip ir nesusitarė su Lietuva kas ir kiek moka. Japonų įmonė-rangovas Hitachi, kurios dalyvavimas projekte tapo eiline „sėkmės istorija“, apsvarstė visą reikalą, nusispjovė ir išėjo.

Galų gale Visagino AE statyba nežengė toliau už darbo brėžinių rengimo. Užsitęsęs tų skandalų atgarsis yra dabartinė oficialaus Vilniaus „šventa kova“ su Astravo AE Baltarusijoje.

Besilieka tik spėlioti, kas bus dabar, kai Briuselis sumanė plėtoti savo „žaliąją sutartį“ ir nukreipti ES šalis atsinaujinančiųjų energijos šaltinių link. Lietuva iškart paskelbė, kad šalis „žaliajai energijai“ lėšų neturi, bet iš Europos Sąjungos jie šituos pinigus mielai paims! Ir tik išdrįskit jų mums neskirti!

Taigi pagrindinis tragikomedijos veiksmas dar lieka priešakyje.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 15 — id: `scraped:rubaltic_lt:7ff1fe6b0c11919c`

**Title:** Dalia Grybauskaitė apie Lietuvos tarybų laikotarpį

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Ištraukos iš Dalios Grybauskaitės disertacijos „Bendrosios (visuomeninės) ir privačios nuosavybės tarpusavio ryšis privataus pagalbinio ūkio veiklos atžvilgiu“. Ekonomikos mokslų kandidato laipsnio disertacija apginta 1988 metais Tarybų Sąjungos Kompartijos Centrinio Komiteto Socialinių mokslų akademijoje Maskvoje.

„Lietuvos įžengimas į socializmo statybos kelią 1940-ųjų metų pradžioje stambiam socialistiniam kaimynui padedant turėjo savo pranašumų. Respublika pradėjo žemės ūkio pertvarkymą tuo metu, kai kitose TSRS respublikose šitas procesas jau buvo pabaigtas. Žemės ūkio pertvarkymas vyko, kai TSRS materialinė ir techninė bazė jau buvo išvystyta ir nereikėjo pradėti viską nuo ekonomikos industrializacijos. [...]

Buržuazinės vadovybės propaganda atlikdavo klastingą darbą kolektyvizacijos atžvilgiu šalyje. Istoriškai susiformavęs smulkaus savininko požiūris į žemę buvo tai propagandai itin palankus pamatas. Prie šitos propagandos prisidėjo ir dvasininkijos atstovai, kurie turėjo didelę įtaką valstiečių masėms, nes Lietuvos gyventojai buvo entuziastingi katolicizmo šalininkai.

Kaimo socialistiniai pertvarkymai buvo sulaikyti kovos ir okupacijos, kurios tesėsi beveik tris metus. Okupacijos metu visi pertvarkymai buvo laikinai sustabdyti. Žemės buvo grąžintos buvusiems savininkams ir vokiečių kolonistams, kurie laikė Lietuvą galima gyvenviete. [...]

Po kovos situacija smarkiai pasikeičia. Reforma buvo įgyvendinama aršios klasių kovos sąlygomis beveik 4 metus – iki 1948 metų. Klasiniai priešai mėgindavo sustabdyti socialistinius pertvarkymus respublikoje drastišku teroru, grasinimais, šantažu, tarybinio ir partinio aktyvo, kolūkinio judėjimo organizatorių naikinimu. Nuo klasinio priešo rankų pokario metais žuvo virš 13 tūkstančių žmonių.

Tokia ilga klasių kova buvo gilinama dėl užsienio kišimosi, atlikdamos radijo propagandos, ginklų ir maisto produktų teikimo iš užsienio. Valstiečiai buvo įbauginti ir net atsisakė priimti žemę jau neminint vienijimosi į arteles arba kolūkius.

Buržuazijos klasė buvo visiškai sunaikinta, o kaime buvo kuriami socialistiniai gamybiniai santykiai. 1951 metais respublikoje nugalėjo kolūkinė santvarka. Žemės ūkio pertvarkymo sąlygų paruošimui esamomis aplinkybėmis tereikėjo 4-5 metų, kas yra beveik dukart mažiau, nei bendrai paėmus šalyje. [...]

Respublikoje pastaruoju metu žymima net gyventojų sugrįžimo atgal į kaimavietes tendencija. Čia tam tikras vaidmuo priklauso didesnėms galimybėms gauti pajamas už bendruomeninio sektoriaus ribų, socialinių ir buitinių sąlygų gerinimui, geriems keliams bei urbanizacijos procesų ypatumams respublikoje. Respublikoje vyksta aktyvus kaimaviečių socialinio tvarkymo procesas. Sparčiai statomos naujos gyvenvietės. Dabar gyvenvietėse gyvena beveik 48% žemės ūkiu besiverčiančių respublikos gyventojų, likusieji gyvena vienkiemiuose. [...]

Skirtumai tarp miesto ir kaimo išlieka, nors šitų skirtumų išnykimo greičiai vis spartėja. Kaip gyventojų pajamų augimo pasekmė augo ir pinigų sumos saugomos kaimaviečių gyventojų taupomosiose knygelėse.

Šitie duomenys liudija ir pajamų augimą, ir jų neužtenkamą apiprekinimą. Iš kitos pusės žiūrint, toks pajamų augimas suteikia kai kurį pranašumą kaimaviečių gyventojams prieš miesto gyventojus. [...]

Pagal mėsos gamybą vienam žmogui respublika užimdavo pirmaujančią vietą šalyje, gyvulininkystei tenka 65% bendrosios ir beveik 90% prekinės žemės ūkio produkcijos, pieno ir mėsos galvijininkystei bei bekoninei kiaulininkystei tenka 87% bendrosios bei 92% gyvulininkystės prekinės produkcijos. [...]

V. I. Leninas laikė, kad visaliaudinės nuosavybės žemei aplinkybėmis žemės sklypų išnaudojimas ir visokie smulkios nuosavybės rūšiai gali virsti spekuliacijos žemės ūkio produktais šaltiniu ir turėti kitų neigiamų pasekmių. Pati prekinių piniginių santykių forma kartais sudaro aplinkybių, palankių tokių santykių atsiradimui, kurie būtų svetimi ir priešiški socializmui: pavyzdžiui, gyvenamųjų patalpų išnuomojimas valstybiniuose namuose, bendruomeninės nuosavybės išnaudojimas savanaudiškais tikslais. [...]

Nepagrįstai aukštų pajamų gavimas pas tam tikrą gyventojų dalį sukelia rinkos santykių psichologiją bei ragina gobšiškumą“.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 16 — id: `scraped:rubaltic_lt:20991073de77959e`

**Title:** Lietuviška „demokratija“ nusivylė lietuvius

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Absoliučia Lietuvos gyventojų dauguma yra nepatenkinta demokratijos būsena savo šalyje. Tai liudija „Baltijos tyrimų“ atlikto sociologinio tyrimo rezultatai. Tokios tendencijos žymimos Baltijos šalyje nuo įstojimo į Europos Sąjungą. Tokiu būdu, šalį, kuri laiko save pagrindiniu demokratijos ir europietiškų vertybių skleidėju regione, nelaiko demokratiška jos gyventojai.

38% lietuvių laiko patenkinamu demokratijos funkcionavimą šalyje. Tų, kurie laikosi priešingos nuomonės, pagal tyrimo rezultatus yra žymiai daugiau – 52% (dar 10% nesugebėjo atsakyti į klausimą).

Kitaip tariant, birželį atliktas sociologinis tyrimas užfiksavo itin nemalonų Lietuvos vyriausybei reiškinį.

Pavadinti tai naujiena sunku. „Baltijos tyrimai“ jau nebe pirmus metus atlieka visuomeninės nuomonės tyrimus Lietuvoje ir jos dėka mes žinome, kad demokratijos troškimas Baltijos šalyje jaučiamas pastoviai. Ir jį numalšinti nepadėjo net įstojimas į ES, į kurią neva įleidžiamos tik šalys su aukščiausiu politinės kultūros lygiu.

2005 metais nepatenkintas demokratija Lietuvoje buvo 61% gyventojų. 2007-2008 metais jų skaičius taip pat sudarė labiau nei pusę, o 2010-ais rodiklis pašoko iki 74%.

Tiesą sakant, lietuvių nuomonė apie demokratiją jų šalyje žymiai pablogėjo per pastaruosius keturis mėnesius ir palyginus su praeitais metais. Nesunku atspėti, su kuo tai susieta.

Nuo kovo mėnesio Lietuvos gyventojai tikriausiai spėjo išgyventi neigiamas koronaviruso epidemijos pasekmes, o nepatenkinimo demokratija lygis čia (o tiesą sakant ir visur kitur) labai priklauso nuo ekonomikos būklės. Neatsitiktinai 2010 metų piko metu 90% respondentų žymėjo, kad reikalai šalyje klostosi vis prasčiau. Jokio loginio ryšio čia įsižiūrėti nereikia. Ryšis yra greičiau emocionalus: ekonomika grimzta į recesiją – kalta yra demokratija, kuri suteikė valdžią visokioms nedereivoms.

Kalbant apie nepatenkintų skaičiaus augimą už pastaruosius metus – čia irgi viskas pasidaro aišku. Užtenka atsiminti, koks svarbus įvykis atsitiko Lietuvoje praeitą vasarą.

Prezidento postas teko savarankiškai išsikėlusiam kandidatui Gitanui Nausėdai, kuris per antrąją rinkimų turą visiškai sutriuškino konservatorių partijos kandidatą Ingridą Šimonytę – Dalios Grybauskaitės „mažąją kopiją“. Nors Nausėda ir buvo laikomas „artimu“ landsbergiečių gretoms, rinkėjai matė jį kaip racionalesnį, blaivų ir diplomatišką politiką.

Valstybinės mašinos kapitaliniam remontui Nausėda nesiruošė iš pat pradžių, tačiau per metus Baltijos šalyje nenutiko jokių pasikeitimų (nebent normalizavosi santykiai su Lenkija, bet jie pradėjo gerėti dar Grybauskaitės kadencijos paskutiniais metais).

2019 metų rinkimų rezultatai liudijo tai, kad bendruomenėje subrendo poreikis pakeičiams, kuris taip ir liko nepatenkintas. Nors formaliai visos demokratinės procedūros buvo atliktos. Kaip gi tai gali būti?

Demokratijos įvertinimo situacija europietiškoje Lietuvoje jau 16 metų kaip iš esmės nesikeičia: nepatenkintų visada yra daugiau. Pasak Baltijos politinį naratyvą tai nepaaiškinama. Bet tuo atveju, jeigu atsižvelgtumėme į Lietuvos įstojimo į ES aplinkybes, viskas paaiškėja.

Dėl „europietiškos svajonės“ šaliai teko paaukoti vertingiausią „tarybų okupantų“ dovaną – Ignalinos atominę elektrinę (IAE).

„Europos Sąjungos reikalavimai buvo iš esmės politiniai – šalys-donorės neslėpė, kad jos tiesiog nenorėjo šalia savęs turėti valstybę, naudojančią Černobylio tipo reaktorius, kurie save susikompromitavo 1986 metais. Bet pradedant nuo 1992 ir iki 2008 metų mes pastoviai vystėme elektrinės saugumą. Ir šitiems projektams irgi buvo skiriama Europos Komisijos pagalba. Labai padėdavo Švedija ir keletas kitų valstybių. Mes darėme viską, kad saugumas būtų patikimas ir atitiktų Europos atominių reaktorių saugumą. Ir mes tai įrodėm! Deja, noras sustabdyti elektrinę buvo neįveikiamas“, - pažymi buvęs Ignalinos AE direktorius Viktoras Ševaldinas.

Ką apie tai galvojo Lietuvos gyventojai? Ignalinos AE klausimas buvo sprendžiamas per 2008 metų referendumą, kai elektrinę dar galima buvo išsaugoti. Dėl mažo rinkėjų aktyvumo referendumas buvo paskelbtas neįvykusiu, bet iš atlikusių savo pilietinę pareigą rinkėjų už Ignalinos atominės elektrinės darbo pratęsimą balsavo beveik 90%.

Atsisakyti patikimo pigios elektros šaltinio gyventojai nenorėjo, ir tai yra nenuginčytinas faktas. Net pats Lietuvos įstojimas į Europos Sąjungą iš esmės buvo išniekinantis demokratijos idealų sutrypimas.

Jeigu atšiaurus lyderis pradeda žaisti prieš taisykles, sistema jį „praryja“. Taip nutiko su buvusiu Lietuvos prezidentu Rolandu Paksu, kuriam ne vien tik buvo paskelbtas impičmentas, bet ir uždrausta vėl dalyvauti rinkimuose.

Tarptautiniai teismai pareikalavo iš Lietuvos šitą draudimą panaikinti, bet seimūnai vaizdingai atsisako įtraukti atitinkamas pataisas.

Pastarąjį kartą šis klausimas buvo nagrinėjamas birželio pabaigoj – balsų neužteko. Konservatoriai ciniškai siūlo nustatyti laikotarpį, po kurio buvęs prezidentas galės sugrįžti į politiką. Arba, atvirkščiai, negalės: Paksui jau 64...

Kaip tik „Baltijos tyrimų“ sociologinės apklausos rezultatų publikacijos išvakarėse Lietuvos Respublikos Užsienio reikalų ministerija apkaltino Baltarusiją atsitraukimu nuo „demokratijos standartų“. Gera, kad Lietuva niekur nepasitraukia!

Tuo pačiu metu Ministerijoje primena, kad „Baltarusijos vadovybė daug kartų viešai skelbė savo pasiryžimą įgyvendinti visas tarptautinių institucijų rekomendacijas“. Galbūt, iš pradžių pačiai Lietuvai būtų verta įtraukti į nacionalinį įstatymų leidimą Europos Žmogaus Teisių Teismo sprendimą pagal Rolando Pakso bylą?

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 17 — id: `scraped:rubaltic_lt:c871d89fdcccb308`

**Title:** „Atminties karas“ su Rusija tapo Baltijos šalims jų egzistavimo prasme

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Paskelbta Rusijoje atskiroji iniciatyva panaikinti įsakymą dėl tarybų ir vokiečių Nepuolimo sutarties pasmerkimą sukelia Baltijos šalyse reakciją, kuri artėja isterijos. Lietuvos prezidentas Gitanas Nausėda pažadėjo skirti savo kalbą ES valstybių pirmininkų susitikime Rusijos „istorinio revizionizmo“ politikai. Latvija ir Estija greičiausiai palaikys šią iniciatyvą – globalinės krizės sąlygomis jos neturi svarbesnio klausymo, nei Molotovo-Ribentropo paktas. Šalys, kurios neturi ateities, gyvena tuo, kad kariauja su Rusija dėl praeities.

Prieš keletą savaičių Rusijos Valstybės Dūmai buvo pasiūlytas įstatymo projektas dėl Pirmojo liaudies deputatų suvažiavimo, kuriame buvo pasmerktas tarybų-vokiečių nepuolimo sutarties pasirašymas 1939 metų rugpjūčio 23 dieną, nutarimo panaikinimas.

Įstatymo projekto autorius, deputatas Aleksejus Žuravliovas, aiškinamajame rašte nurodo, kad 1989 metų nutarimas „neatitinka istorinio sąžiningumo principus ir buvo priimtas tų metų vis smarkėjančio politinio nestabilumo, kurį skatino išorinių jėgų spaudimas, sąlygomis“.

„Slaptų protokolų pasirašymo praktika yra būdinga tų laikų diplomatijai, o valstybių ekonominiai ir politiniai interesai tam tikrame regione visada egzistuoja tarptautiniuose santykiuose. Beje, protokolas nenumatė kitų valstybių sienų pakeitimo bet kuriuo būdu, įskaitant karinį. Skirtingai nuo šiuolaikinės padėties, kai „demokratija“ yra eksportuojama „oranžinių revoliucijų dėka“, teisėtų vadovybių numetimo dėka“, - rašo Žuravliovas.

Iš esmės tai yra ne Rusijos valdžios nutarimas, bet mažai įtakos turinčios partijos „Rodina“ (Tėvynė) lyderio atskiroji iniciatyva. Šalies vadovybė nuo deputato Žuravliovo iniciatyvos atsiribojo. Rusijos prezidento spaudos sekretorius Dmitrijus Peskovas pareiškė, kad Kremliuje apie šitą įstatymo projektą nieko nežino.

Lietuvos Respublikos URM vadovas Linas Linkevičius pasirodė su Rusijos deputato pasmerkimu, apkaltinęs jį istorijos perrašimu. Lietuvos, Latvijos, Estijos ir Lenkijos parlamentų dalyviai kreipėsi į savo rusiškus kolegas su kolektyviniu prašymu nenagrinėti Žuravliovo pasiūlytą projektą.

“Tarybų sąjungos okupuotos valstybės susivienijo prieš mėginimus perrašyti istoriją ir pateisinti esamą agresyvią Rusijos Federacijos politiką prieš kaimynines valstybes”, - rašo Lenkijos ir Baltijos šalių atstovai ir baigia išvada, kad Žukovo įstatymo projekto registracijos atšaukimas bus pirmu žingsniu tam, kad atkurti jų gerus santykius su Rusija.

Kalbant apie nesąmonę, šioje situacijoje jinai yra štai tokia: visų pirma, visa šita audra kilo dėl visiškai vidinio Rusijos reikalo. Jeigu Valstybės Dūma priims sprendimą, tai 1989 metų nutarimas dėl Molotovo-Ribentropo pakto pasirašymo pasmerkimo nebegalios Rusijos teritorijoje, kas nekaip nepaliečia nei Lenkijos, nei Baltijos šalių.

Antra, šantažuoti Maskvą geranoriškais kaimyniniais santykiais - aukščiausias neadekvatumo laipsnis.

Rusija pastaraisiais metais puikiai gyveno, vystėsi ir tapo stipresnė be santykių su Rytų Europa.

Jokio ypatingo intereso šių santykių atkūrimui ji neturi. Tai Rytų Europa nesiliauna rodanti skausmingą interesą Rusijai. Dažniausiai – klyksmais apie „teroristinę valstybę“, „agresyvią kaimynystę“ ir „istorinį revizionizmą“, bet pasitaiko ir atsargių pastangų paliesti pragmatinio bendradarbiavimo ekonomikoje ir gerų kaimyninių santykių temas.

Dar juokingesniu gali būti pavadintas tik Lietuvos elgesys, kuri mėgina Rusijos vidines diskusijas istorijos temomis pavirsti visos Europos „reikalu“.

„Būtina atkreipti sąjungininkų ir tarptautinės bendruomenės dėmesį į tai, kad Rusija sistemiškai mėgina perrašyti istoriją tam, kad pateisinti savo politiką kaimyninių valstybių atžvilgiu, jų valstybingumo nuginčijimą bei Europos Sąjungos ir NATO skaldymą <...>. Prezidentas yra pasiryžęs iškelti šitą klausimą per Europos Tarybos posėdį liepos 17-18 dienomis“, - sakome Nausėdos administracijos pranešime.

„Istorinis sprendimas“ buvo priimtas Lietuvos gynybos Valstybinėje taryboje, kurios posėdis buvo skirtas būtent deputatui Žuravliovui. Nausėda ir kiti Lietuvos vadovai jo metu aptarė Rusijos valdžios (kokios valdžios?!) ketinimus reabilituoti tarybų ir nacių sąmokslą.

Galima gyvai stebėti, kaip kuriama Baltijos mitologija. „Baltijos šalys pasisako prieš Rusijos parlamente nagrinėjamą įstatymo projektą, kuriuo numatoma pripažinti negaliojančiu TSRS Liaudies deputatų priimtą 1989 metais sprendimą dėl slaptų Molotovo-Ribentropo pakto protokolų pasmerkimo ir paskelbimo nebegaliojančiais ir juridiniu atžvilgiu nepagrįstais“, - praneša pagrindinis Lietuvos žiniasklaidos valstybinis televizijos kanalas LRT.

Neišmanantis temą eilinis lietuvis iš šio straipsnio gali padaryti išvadą, kad Kremlius ketina grįžti prie susitarimo su Trečiuoju Reichu dėl įtakos sferų padalijimo Europoje ir vėl įvesti į Baltijos šalis rusiškus tankus.

Nesvarbu ar yra prasmė Maskvai įvesti kariuomenę į Baltijos šalis, ar ne. Svarbu, kad 1940 metais ji tenai įvedė tankus, o tai reiškia, kad vėl įves. Nesvarbu, ar Kremlius yra pasiruošęs paskelbti negaliojančiu nutarimą dėl Molotovo-Ribentropo pakto pasmerkimo ar ne. Svarbu, kad yra pretekstas pašnekėti apie naujos „okupacijos“ grėsmę.

Iš šalies tai, žinoma, atrodo žiauriai. Globalinės krizės metu, kai Europos Sąjunga neįsivaizduoja, kaip užlopyti vargšą septynerių metų ES biudžetą po Brexit‘o ir Europos ekonomikos žlugimo po koronaviruso, žodį per suvažiavimą prašo Lietuvos prezidentas ir pradeda pasakoti europiečiams apie 1930-ųjų metų įvykius ir įstatymų kūrimą Rusijos Valstybės Dūmoje.

Bet Baltijos šalims tokiame elgesyje nėra nieko keisto.

Nei esamuoju laiku, nei praeityje jos kovoti su Rusija negali. Todėl ir kovoja už istoriją.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 18 — id: `scraped:rubaltic_lt:475c77aad6f24650`

**Title:** Lietuva atsakė į Putino straipsnį Hitlerio šalininko šlovinimu

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvoje ketinama skirti 2021 metus Juozo Lukšos (Daumanto) – žinomo antisovietinio pogrindžio dalyvio, kaltinamo žydų genocidu – atminčiai. Prieš šitą sprendimą, kas buvo nenuostabu, pasisakė Lietuvos žydų bendruomenės pirmininkė Faina Kukliansky, po ko „Tėvynės sąjunga – Lietuvos krikščionys demokratai“ partiją atstovaujantis Seime deputatas Laurynas Kasčiūnas įkaltino ją „provokacija Rusijos režimo naudai“.

Birželio 23 dieną Lietuvos Seimo Švietimo ir mokslo komitetas pristatė rezoliucijos projektą, kurį pavadino „2021 metų paskelbimas Juozo Lukšos-Daumanto metais“. Baltijos šalyje jis laikomas vienu įžymiausių pasipriešinimo tarybų valdžiai dalyvių. Jo biografija tikrai yra išraiškinga.

1941 metais Lukša prisijungė prie nacionalistinio pogrindžio, buvo sulaikytas NKVD, bet išsigelbėjo nacių agresijos prieš TSRS dėka. Kovojo prieš sovietų valdžios atkūrimą gimtoje šalyje, su mūšiu prasiveržė į vakarus, gavo papildomą parengimą ir vėl grįžo į Lietuvą tam, kad tapti nedidelio partizanų būrio vadu.

Kai lietuvišką „Če Gevarą“ likvidavo, jam sukako vos 30 metų. Ar šita istorija neverta filmo? Matyt, tą patį klausymą iškėlė sau režisierius Jonas Vaitkus, kuris pagal Lukšos biografiją sukūrė filmą „Vienui Vieni“.

Pavyzdžiui, jį atpažino kaip vieną iš liūdnai pagarsėjusio Kauno pogromo – 1941 metų birželio 25-29 dienomis vykusių Lietūkio garažo žudynių – vykdytojų. „Miško brolių“ gerbėjai šiuos kaltinimus aršiai neigia.

„Partizanas Juozas Lukša-Daumantas buvo vienu pačių įžymiausių kovotojų už Lietuvos nepriklausomybę“, - teigiama jau paminėtame Seimo rezoliucijos projekte. Nacionalistai ją palaikė su entuziazmu.

Lietuvos žydų bendruomenėje reakcija taip pat ryški ir nedviprasmiška: Holokausto dalyvių šlovinimas demokratinėje Europos valstybėje nepriimtinas. Vietoj Lukšos „metų žmogumi“ turi tapti kas nors kitas – tokios nuomonės laikosi žinomas žydų mokslininkas ir rašytojas Dovydas Kacas.

Lietuvos žydų bendruomenės pirmininkė Faina Kukliansky žengė dar toliau ir kreipėsi į Seimą su raginimu atsisakyti Švietimo ir mokslo komiteto rezoliucijos.

Fainos Kukliansky oponento vaidmenį nusprendė atlikti konservatorių partiją atstovaujantis Seime deputatas Laurynas Kasčiūnas, kuris reikalauja iš LŽB pirmininkės viešai atsiprašyti už „miško brolio“ atminties išniekinimą.

Panaši kaltinimai Fainos Kukliansky atžvilgiu skamba jau nebe pirmą kartą. Praeitais metais „landsbergiečiai“ ir asmeniškai Vytautas Landsbergis jau įkaltino ją „Kremliaus parėmimu“. Tuomet Lietuvos bendruomenėje įkaito aistros dėl kito „herojaus“ – nacių kolaboracionisto Jono Noreikos – šlovinimo. Po metų asmenys pasikeitė, bet ginčo esmė išliko.

Vis dėl to yra vienas žymus skirtumas. Kai Faina Kukliansky po nacionalistų grasinimų laikinai sustabdė LŽB biuro ir sostinės choralinės sinagogos veiklą, Landsbergis kritikavo ją gana švelniai, beveik tėviškai, ir neįsižiūrėjo jos veiksmuose jokių blogų ketinimų: „Kaip [Vilniaus miesto meras Remigijus] Šimašius nesuvokdavo, ką darė, dabar, turbūt, ponia Kukliansky nesuvokia“.

Iš kur pasiėmė toks griežtumas? Iš vienos pusės, tarp Kasčiūno ir LŽB pirmininkės brenda asmeninio pobūdžio konfliktas. Prieš keletą mėnesių jis ragino ją paaiškinti, kodėl Rūtos Vanagaitės nauja „melagiška knyga“ apie Holokaustą Lietuvoje buvo finansuota iš “Geros valios kompensacijos už žydų religinių bendruomenių nekilnojamąjį turtą disponavimo fondo” lėšų.

Kukliansky į šitą išpuolį dėmesio neatkreipė – knyga buvo išleista ir pristatyta Vilniaus choralinėje sinagogoje. Nenuostabu, kad įžeistas Kasčiūnas nepraleidžia galimybės vėl apkaltinti Lietuvos žydų lyderę.

Deja, reikalas neapsiriboja vien tik asmenine antipatija. Kad suvokti tikrą žodžių apie „provokaciją Rusijos režimo naudai“ esmę, būtina suprasti ir užsienio politikos kontekstą, kuris nulėmė 2021 metų paskelbimą Juozo Lukšos metais.

Pirmiausiai, gegužės pabaigoje deputatas Aleksejus Žuravliovas pateikė Rusijos Valstybės Dūmos nagrinėjimui įstatymo projektą dėl TSRS Liaudies deputatų suvažiavimo nutarimo “Dėl Tarybų Sąjungos ir Vokietijos 1939 metų nepuolimo sutarties politinio ir teisinio įvertinimo“ paskelbimo nebegaliojančiu.

Kitaip tariant, pasiūlė Rusijai liautis atgailavusi dėl Molotovo-Ribentropo pakto pasirašymo. Baltijos šalys ir Lenkija į tai sureagavo bendru šaukimu Valstybės Dūmai atsisakyti Žuravliovo iniciatyvos nagrinėjimo.

Antra, birželio 18 dieną amerikiečių žurnalas National Interest išspausdino Vladimiro Putino straipsnį apie Antrąjį pasaulinį karą. Atskirą dėmesį Rusijos lyderis skyrė Lietuvai, Latvijai ir Estijai. „Jų įstojimas į TSRS buvo įgyvendintas remiantis sutartimi, valstybių gyventojų išrinktoms valdžioms pritarus. Tai atitiko tų laikų tarptautinės bei valstybinės teisės normas. Beje, Lietuvai 1939 metų spalio mėnesį buvo grąžinti Vilniaus miestas su apskritimi, kurie anksčiau priklausė Lenkijai. Baltijos respublikos būdamos TSRS sudėtyje išsaugojo savo valdžios organus, kalbą, turėjo savo atstovybes tarybinėse aukščiausiosiose valstybės struktūrose“, - teigia Putinas.

Žinoma, šiuo atveju Lietuvos, Latvijos ir Estijos reakcijos nereikėjo ilgai laukti. Jie nekantravo apkaltinti Rusijos prezidentą melu, istoriniu revizionizmu, mėginimais pateisinti „sovietų okupaciją“.

Šitą pasiūlymą galima laikyti dėsninga eiline Lietuvos kontrataka istorijos fronte. Ar ne todėl Kasčiūnas įkaltina Kukliansky „provokacija Rusijos režimo naudai“?

Nors LŽB pirmininkė Putino straipsnį irgi iškritikavo. Bet nuo konservatorių išpuolių tai jos neišgelbėjo.

O visi, kas pasisako prieš, neatidėliotinai bus priskirti prie Kremliaus agentų. Karinių laikų tvarka yra itin griežta. Todėl Lietuvos žydų bendruomenei verta ruoštis tam, kad kovoti su nacių nusikaltėlių šlovinimu jiems nuo šiol bus dar sudėtingiau.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 19 — id: `scraped:rubaltic_lt:b8e42c7e6e3e90ba`

**Title:** Lietuva reikalauja iš ES kompensacijos už išmirimą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvių konservatoriai siūlo sukurti Europos Sąjungoje naują Demografijos ir šeimos politikos fondą, kuris nulems sėkmingą gimstamumo kontrolės politiką. Jų idėja turi bendro u prezidento Gitano Nausėdos iniciatyva reikalauti iš Briuselio kompensacijos už darbo jėgos nutekėjimą iš Lietuvos. Abiem atvejais kalbama apie tą patį: nujausdama dotacijų iš Europos fondų mažinimą Baltijos šalis ieško naujų argumentų lėšų teikimo išsaugojimui.

Pasiūlymus dėl demografijos skatinimo Europos komisijai paruošė partijos „Tėvynės sąjunga – Lietuvos krikščionys demokratai“ (TS-LKD) deputatai Audronius Ažubalis ir Laurynas Kasčiūnas. Tokį jų sprendimą paskatino neseniai paskelbta Europos Komisijos ataskaita dėl demografinių pakeitimų regione.

Turbūt, viskas taip ir buvo: susirūpinę „lengvų“ pinigų paieška konservatoriai atrado sąjungos centro įnirtingą interesą dėl Europos kontinento išmirimo ir iškart nusprendė veikti.

Savo idėjas Ažubalis ir Kasčiūnas nukreipė tiesiai Europos Komisijos prezidentei Ursalai fon der Lejen, Europos Komisijos vice-prezidentei demokratijos ir demografijos klausimais Dubravkai Šuicai ir eurokomisarui Nicolui Schmitui.

„Europos Sąjunga visų pirma privalo spręsti demografines problemas, su kuriomis ji susiduria; be šių problemų sprendimo bet kuri tolimesnė valdymo ir Europos Sąjungos institucijų reforma bus beprasmiška. Imigracija, gyventojų senėjimas ir žemas gimstamumo lygis gali pasibaigti tuo, kad ateityje tam tikruose Europos Sąjungos regionuose mes turėsime Europą be Europiečių“, - teigia TS-LKD atstovas.

Lietuvos konservatoriams pats laikas nukeliauti į Jungtines Valstijas – ten jiems paaiškins, kieno gyvenimai turi reikšmę...

Juokai juokais, o Seimo deputatai nusiteikę rimtai. Demografinių problemų sprendimui jie siūlo sukurti atskirą fondą.

„Sėkminga gimstamumo politika – tai ne vien tik finansinis skatinimas. Tai taip pat privalo įtraukti palankių šeimai ir vaikams praktikų skatinimą, pavyzdžiui, galimybę šeimoms efektyviau derinti darbą ir auklėjimą, lengvesnį tėvų grąžinimą į darbo rinką, valstybinio vaikų auklėjimo stiprinimą“, - pabrėžia Kasčiūnas, lyg darydamas užuominą, kad pinigai – ne svarbiausia. Jus nepagalvokite, kad Lietuvos valdžios vėl kaulija iš Briuselio išmaldų, jokiu būdu!

„Lengvesnis tėvų grąžinimas į darbo rinką“ galimas tik tuo atveju, jeigu šita rinka aktyviai vystosi ir turi kadrų stygių. „Valstybinio vaikų auklėjimo stiprinimas“ tiesiogiai proporcionalus toms lėšoms, kurias valstybė yra pasiryžusi išleisti vaikų reikalams. Kaip lietuvių konservatoriai nemėgintų įrodyti priešingą, viskas priklauso nuo pinigų.

Kad suprasti tikrąją Kasčiūno ir Ažubalio motyvaciją užtenka atkreipti dėmesį vos į vienintelį faktą.

Lėšas Demografijos ir šeimos politikos fondui siūloma įtraukti į naująją Europos Sąjungos septynių metų finansinę perspektyvą, kuri bus įtvirtinta kelių mėnesių bėgyje.

Neatsitiktinai, pavyzdžiui, Lietuvoje įgyvendinama demografijos, migracijos ir integracijos strategija 2019-2021 metams, kuri turi padidinti gyventojų skaičių iki 3 milijonų žmonių. Ministras-pirmininkas Saulius Skvernelis gyrėsi, kad šis tarpinstitucinis planas numato apie 100 konkrečių priemonių ir žingsnių.

Tai ir įgyvendinkite savo planą. Kokiam veltui bendro Europos biudžeto įtvirtinimo išvakarėse Lietuvos konservatoriams prireikėjo atskiro demografijos fondo?

Sumanymas itin paprastas: eilinė „lesykla“ turi padengti Lietuvos įplaukas, kurių valstybė gali netekti dėl susibūrimo (kohezijos) politikos įgyvendinimo ir dotacijų mažinimo.

Iš kitos pusės, Lietuvoje šita problema įgauna nacionalinio mąsto tragedijos pobūdį.

2020 metų sausio 1 dienai čia oficialiai gyveno 2 milijonai 669 tūkstančiai žmonių, tai yra milijonu mažiau, nei TSRS suirimo momentui. Procentiniu santykiu Baltijos respublika prarado maždaug tiek pat, kaip ir Ukraina. Bet Lietuvos rezultatas atrodo daug įspūdingesnis, jeigu turėti omeny, kad Lietuvoj nebuvo nei „Krymo“, nei „Donbaso“.

Pašalinsim iš konservatorių pasiūlymo visas „lupenas“ ir gausime lakonišką ir aiškų lozungą: daugiau pinigų Lietuvai!

Briuselis nenori finansuoti mūsų energetikos, infrastruktūros, žemės ūkio? Tegul tada finansuoja kovą su demografine katastrofa. Kam bus taikomi pinigų srautai – nesvarbu. Svarbiausia, kad jie nesumenkėtų.

Pirmas buvo prezidentas Nausėda, kuris neseniai užsimanė reikalauti iš ES kompensacijų už darbo jėgos nutekėjimą iš Lietuvos.

„Kai kurios šalys – ES biudžeto donorės nėra pasiryžusios ambicingiems skaičiams. Bet Lietuva irgi yra ES biudžeto donorė, tik mes teikiame Europai ne pinigus, bet darbo jėgą. Už pastaruosius metus Lietuva prarado 10% savo darbo jėgos, žmonių, kurie persikėlė gyventi į Didžiąją Britaniją, į Vokietiją ir prisidėjo prie ekonomikos plėtros šiose valstybėse. Manome, kad nusipelnėme kompensaciją už tai“, - pareiškė Lietuvos lyderis.

Nepakenčiamas „sovokas“ suyrė, Baltijos šalys išsilaisvino ir grįžo į „europietiškų tautų šeimą“. Bet ir čia, kaip paaiškėjo, jas įžūliai eksploatuoja. Nausėdos ir „landsbergiečių“ iniciatyva žymi Lietuvos europietiškos integracijos sėkmės istorijos virsmo į labiau būdingo šaliai išnaudojamos, diskriminuojamos bei išplėšiamos aukos įvaizdžio pradžią.

Ir iš vis visi yra skolingi jai.

O ten ne už kalnų ir komisijos kompensacijai už Lietuvos „europietišką okupaciją“ apskaičiuoti sušaukimas.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 20 — id: `scraped:rubaltic_lt:5b6fea136b6ea3b6`

**Title:** Lietuva nusprendė taikytis su Rusija

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos Respublikos ambasadorius Rusijos Federacijoje Eitvydas Bajarūnas davė stebinančiai taikingą interviu, kuriame ragino Vilnių ir Maskvą palankiau vystyti savo santykius ir ieškoti tai, kas vienija, o ne skiria Rusiją ir Lietuvą. Prieš tai Lietuvos URM neprisijungė prie savo kolegų iš Lenkijos, Latvijos ir Estijos, kurie pačiais išraiškingais žodžiais smerkdavo Rusijos prezidento Vladimiro Putino straipsnį apie Antrąjį pasaulinį karą. Lietuva siunčia signalus apie savo pasiryžimą taikytis, deja, toliau tuščių bendrų frazių šalies diplomatija kol kas nepažengia.

„Geriau pradėkime nuo žmoniško, o ne nuo kažkokios geopolitikos, kas ten griežčiau pasakys. Reikia pradėti nuo to, kad esame kaimynai, gyvename kažkokioje bendroje geografinėje erdvėje. Supraskime vien kitą kaip nors. Mes vis tiek nepabėgsime vienas nuo kito. Taip, gyvensime čia. Lietuvos didysis kaimynas – Rusija. Mes turime čia savo vietą istorijoje bei geografijoje. Ieškokime ne tai, kas mus skiria, o tai, kas mus vienija – istorinius įvykius, kultūrą, kažkokias šviesias mūsų praeities akimirkas“, - pasakė Lietuvos Respublikos ambasadorius Rusijos Federacijoje Eitvydas Bajarūnas per savo interviu, duotą radijo stočiai „Echo Moskvy“.

Tokiais žodžiais ambasadorius atsakė į klausimą apie Rusijos prezidento Vladimiro Putino straipsnį dėl Antrojo pasaulinio karo. Šiame straipsnyje Putinas, pavyzdžiui, teigia, kad Baltijos šalių įstojimas į TSRS atitiko tarptautines teises.

Interviu su Lietuvos ambasadoriumi prasideda nuo klausimų apie šitą straipsnį. Radijo stotis „Echo Moskvy“, tikriausiai, tikėjosi sugauti hype‘a pačios antirusiškai nusiteikusios Rytų Europos šalies atstovo dėka, sakydama jam, kad jokios „sovietų okupacijos“ Baltijos šalyse nebuvo. Be to, oficialus Vilnius, ir tai yra keista, jokių komentarų apie Putino straipsnį nedavė. Skirtingai nuo kitų Baltijos valstybių.

Sensacija tas interviu iš tikrųjų virto, tačiau labiau lokaline prasme, nei buvo tikėta. Ta sensacija palietė tik labai mažą kiekį Rusijos politinių mokslų specialistų, kurie nagrinėja Baltijos regioną.

„Žinoma, aš tikiu, kad mes – Lietuva, Europa, Rusija – gyvensime vieningai, lyg tuose pačiuose namuose. Tai skamba labai patetiškai – vieni namai. Bet mes pradėjome nuo to, primenate – bendri Europos namai. Nors mes nesuprasdavome, kas tai yra“, - tokį atsakymą, pavyzdžiui, davė Eitvydas Bajarūnas į klausimą, kodėl per 30 metų taip ir nesusiklostė Lietuvos ir Rusijos santykiai.

Čia tiktų užduoti klausimą : ar gi ne Lietuva ardydavo tų bendrų Europos namų statybą? Kokios valstybės atstovai savo laiku užblokavo derybas dėl bevizio režimo tarp Rusijos ir Europos Sąjungos? Lietuvos. Šiomis aplinkybėmis Lietuvos diplomatas kalbantis apie bendrus Europos namus kartu su Rusija ypač susigraudina.

Dar įdomesniu atrodo straipsnis apie NATO. „NATO nėra karinė mašina, nukreipta prieš Rusią – tai, ką mes kartais girdim čia, Rusijoje. Dažnai girdim. Tai yra gynybinė sąjunga. Ji nėra nukreipta prieš Rusiją. Lietuva įstojo į NATO ne tam, kad būti prieš Rusiją, bet todėl, kad jautėmės: tai pavirs mus saugesne valstybe“, - sako Lietuvos ambasadorius Rusijoje ir tuoj pat prideda, kad įvykiai Ukrainoje patvirtina Vilniaus pasirinkimo teisingumą. Jeigu Lietuva 2014 metais nebūtų NATO sudėtyje, niekas nežino, kas su ja galėtų atsitikti.

Mes regiame unikalią situaciją. Lietuvos atstovas mėgina palikti įprastą šalies diplomatijai rusofobišką retoriką, bet jo valstybė prie tos retorikos taip priprato, kad išlipti iš ten jis nepajėgia. Tiek metų be perstojo trukę riekimai dėl „Rusijos pavojų“, „agresyvią kaimynystę“ ir artėjančią Rusijos agresiją“! Rusija buvo atvirai ir oficialiai vadinama NATO buvimo Lietuvoje priežastimi. Kaip čia būtų įmanoma iškart pasisukti 180 laipsnių kampu?

„Solidarumo su Ukraina“ minimumas, daugiau apie pozityvą ir laimingas akimirkas Lietuvos ir Rusijos santykių istorijoje. Taip, pasak Lietuvos atstovo tokios buvo.

Kartu su beveik išnikusiais pastaruoju metu antirusiškais pasisakymais iš Vilniaus pusės taikinamoji Bajarūno retorika signalizuoja Maskvai apie Lietuvos norą taikytis su Rusija.

Problema šituo atveju ne tame, kad be Lietuvos ambasadoriaus interviu kitų taikinamųjų žodžių arba net užuominų susitaikinimui iš Vilniaus kol kas nesuskambėjo. Problema tame, kad vienais žodžiais Lietuvos ir Rusijos santykiams jau nebepadėsi.

Už pastarąjį keletą metų foninio priešiškumo palaikymas ir dirbtinai įkurstoma konfrontacija Rusijos ir Lietuvos santykiuose atvedė pastarąją prie konkrečių antirusiškų žingsnių.

Taigi problema jau seniai susieta ne su žodžiais, bet su poelgiais ir veiksmais. Jeigu Lietuva pageidauja atgimti santykius su Rusija, vien tik antirusiškos reformos slopinimo bei bendrų frazių apie „šviesiuosius mūsų bendros praeities puslapius“ įmetinėjimo tam tikrai neužtenka.

Santykių su Rusija atgimdymui reikalingi ir dideli praktiniai žingsniai, tokio pat mąsto, kaip ir tie, kuriais šitie santykiai buvo ardami.

Akivaizdu žingsniu santykių su Rusija suirimui buvo nuteisti už „karinius nusikaltimus bei nusikaltimus žmoniškumui“ sunkiai sergantį karinį pensininką, kuris 1991 metų sausio 13-osios naktį, būdamas Tarybų armijos 23 metų leitenantu, įžiebė tanko žibintus prie Vilniaus televizijos bokšto ir šaudė tuščiais sviediniais iš nukreiptos aukštai į dangų patrankos. Tokiu pat akivaizdu žingsniu parodyti pasiryžimą atkurti santykius būtų jo išlaisvinimas.

Be šio akivaizdaus žingsnio iš Vilniaus pusės Rusijai net nėra jokios prasmės pradėti derėtis.

Post scriptum

Lietuvos URM visgi sureagavo į Rusijos prezidento straipsnį apie Antrąjį pasaulinį karą. „Prezidentas Putinas debiutavo kaip istorikas. Desperatiškai stengiasi reabilituoti senas nusikaltėliškas sutartis dėl pasaulio padalijimo į „įtakos sferas“. Tas, kas nėra pasiryžęs pakeisti ateitį, nusprendė perrašyti praeitį“, - parašė savo Twitter paskyroje Lietuvos Respublikos užsienio reikalų ministras Linas Linkevičius.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```
