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

### Article 1 — id: `scraped:rubaltic_lt:7f2cacbc7093c2ba`

**Title:** Už ką Rusija turi atlyginti Pabaltijui?

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Rusija turi atlyginti Latvijai už tuos ekonominius praradimus, kuriuos ši patirs dėl rusų karinių mokymų Baltijos jūroje, mano buvęs Latvijos gynybos ministras, Europos parlamento deputatas Artis Pabriks. Pabrikso iniciatyva gali tapti naujų pabaltijiečių reikalavimų Rusijai istorijos puslapiu — sąrašas Lietuvos, Latvijos ir Estijos ekonominių praradimų, dėl kurių esą kaltas rytų kaimynas, bus be galo. Analitinis portalas RuBaltic.Ru rekonstravo Pabaltijo mąstymo sistemą ir pabandė nustatyti, už ką dar Rusija „turi atlyginti“ Pabaltijui.

1.     SGD terminalas

Suskystintų gamtinių dujų terminalas Independence buvo atplukdytas į Lietuvą siekiant energetinės nuo Rusijos nepriklausomybės ir sukurti rusų dujoms rinkos konkurenciją.

Ir todėl dabar „Gazpromas“ turi dengti šias SGD terminalui skirtas išlaidas, nes Independence Lietuva išsinuomavo ant pykčio Rusijai.

2. Baltarusijos AE

Per tas isteriškas kovas su Ostrovecko AE Baltarusijoje statyba Lietuvos politikai išeikvojo visus savo nervus. Todėl „Rosatomas“ turi kompensuoti jų moralinius nuostolius.

„Tautos tėvas“ Landsbergis seniai pasakė, jog Baltarusijos AE statoma specialiai ant pykčio Lietuvai, kad pačiu egzistavimo faktu siutinti Lietuvos politikus, primenant jiems, jog Baltarusija dabar turi savą atominę, o Lietuva savąją sunaikino.

3. Karinės išlaidos

Rusija kalta, kad Pabaltijo šalys kasmet turi didinti karinį biudžetą, mažinant kitas biudžeto išlaidas.

Įrodinėti, jog Rusija pastaraisiais metais nekėlė Pabaltijui jokio pavojaus, beviltiška. Sykį jau bijo, vadinasi, yra dėl ko, net jeigu Rusija išvis nieko nedarė. Lai moka už tai, kad ji tokia didelė, baisi ir šalta, nes kaimynus gąsdina vien savo plotais ir geografine padėtimi.

4. Išstojimas iš BRELL

Pabaltijo išstojimą iš energetinio žiedo BRELL (Baltarusija, Rusija, Estija, Lietuva, Latvija) turi apmokėti Rusija. O kas daugiau? Jog išstojo Pabaltijo šalys iš BRELL dėl Rusijos — kad nesimuistyti su ja viename žiede. Todėl Rusija lai ir apmoka už šį išstojimą.

5. Infrastruktūros taisymas

Praktiškai visą dabartinę Lietuvos, Latvijos ir Estijos infrastruktūrą — kelius, uostus, tiltus, gyvenamuosius kvartalus — statė Tarybų Sąjunga. Todėl tvarkyti visa tai privalo Rusija kaip jos teisių perėmėja. Kodėl Lietuvos ir Latvijos kelius būtina rimtai tvarkyti? Todėl, kad Pabaltijo respublikos neprašė rusų juos statyti. Patys pastatė — lai dabar patys ir remontuoja.

O jei nenori remontuoti, lai atlygins Pabaltijo šalims ekonominius nuostolius dėl to, kad tie keliai blogi ir nesutaisyti.

6. „Minkštoji jėga“

Grėsmę Pabaltijui kelia ne tik rusų tankai, bey ir rusų „minkštoji jėga“, kuri veikia lietuvius, latvius ir estus per muzikantus, aktorius ir šiaip kultūros veikėjus.

Visa tai — Maskvos griaunamosios akcijos, todėl Maskva turi išmokėti Lietuvai, Latvijai ir Estijai materialines kompensacijas už visas tas akcijas.

7. Specialiųjų tarnybų veikla

Lietuvos, Latvijos ir Estijos saugumo tarnybos užimtos vien Rusija. Jų ataskaitos kasmet skiriamos beveik tik „rusų grėsmei“, jų veikla — rusų šnipų paieškos, Putino „penktosios kolonos“, veikiančios Pabaltijo šalyse, ir „Maskvos rankos“ demaskavimas.

Jei nebūtų Rusijos ir rusų, šioms šalims nebūtų reikalingos specialiosios tarnybos. Ir todėl Kremlius bei Pabaltijyje gyvenantys rusakalbiai privalo savo lėšomis išlaikyti Lietuvos valstybės saugumo departamentą, Latvijos saugumo policiją ir Estijos apsaugos policiją. Ir dengti toje kovoje šių organizacijų išlaidas.

8. „Pienelio...“

Dėl to, jog Rusija įvedė maisto produktų embargą, Lietuvos, Latvijos ir Estijos mėsos ir pieno pramonė patiria didžiulius nuostolius ir atsidūrė prie bankroto ribos. Pabaltijo šalių vyriausybės ne kartą šiuo klausimu kreipėsi į Europos komisiją prašydamos kompensuoti Maskvos veiksmų nuostolius. Tačiau kreiptis reikia ne su prašymu, o su reikalavimu, ir ne į Briuselį, o į pačią Maskvą. Juk tai Maskva uždraudė įvežti žemės ūkio produkciją iš Europos Sąjungos šalių ir tokiu būdu beveik sunaikino pabaltijiečių pienininkystę.

Bandymai pasiteisinti, jog šis draudimas atsirado dėl vakarietiškų sankcijų, nepraeina.

Taip ir čia: Vakarai gali taikyti Rusijai sankcijų kiek tik nori, tačiau atsakomosios sankcijos — ekonominis spaudimas, dėl kurio atsiradusius nuostolius privalo atlyginti Maskva.

9. Tranzitas

Pabaltijo uostai jau keletą metų iš eilės praranda užsakymus ir pinigus, todėl kad Rusija atsisako pervežti per juos savo krovinius ir perorientuoja krovinių srautą į specialiai prie Baltijos jūros pastatytus savo uostus. Ypač piktina demonstratyvus Maskvos siekis neturėti daugiau reikalų su Pabaltijo šalimis, neleisti joms misti Rusijos pinigais ir tuo metu užsiiminėti antirusiška politika.

Jei Rusija nenori nei atsiprašinėti, nei pripažinti savo kaltės (nesvarbu už ką), nemokėti Pabaltijui kompensacijų ir reparacijų ir net atima iš šių šalių pelną dėl jos tranzito, tegul nors padengia tuos nuostolius, kuriuos Lietuva, Latvija ir Estija patiria dėl to prarasto tranzito.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 2 — id: `scraped:rubaltic_lt:54b8381fd5cf7a75`

**Title:** Andrejus Konoplianikas: Pabaltijo šalis ir Lenkiją kamuoja nuoskauda dėl „Gazpromo“

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Šiomis dienomis analitinio centro KyivStratPro ekspertas ekonomikos klausimais Sergejus Lepeika spaudos konferencijoje Kijeve netikėtai pateikė patarimą Ukrainos valdžioms ne mažinti, bet didinti rusiškų dujų tiekimą. Priešingu atveju, teigia Lepeika, Ukrainos dujų transportavimo koridorius po įvedimo eksploatacijon „Šiaurės srauto–2“ gali būti apleistas. Kijevo eksperto nuomonė tuo metu, kai Vokietija davė sutikimą kloti dujotiekį, skamba pagrįstai. Beje, kova su rusiškomis dujomis Europoje nesibaigė. Apie šios kovos užkulisius ir „Naujosios Europos“ šalių vaidmenį joje analitinis portalas RuBaltic.Ru tęsia pokalbį su AB „Gazprom eksport“ generalinio direktoriaus patarėju, vienu iš rusų šalies Darbo grupės — 2 „Vidinės rinkos“ Konsultacinės tarybos Rusija — ES dujų klausimais pirmininkų, Rusijos I.Gubkino valstybinio naftos ir dujų universiteto „Tarptautinio naftos ir dujų biznio“ katedros profesoriumi Andrejumi Konoplianiku.

— Pone Konoplianikai, praeitoje mūsų interviu dalyje Jūs sakėte, kad kovą su „Šiaurės srautu–2“ sąlygoja būtent ekonominiai motyvai. Jūsų manymu, ar Rusijos išstūmimas iš europietiškos dujų rinkos — galutinis amerikiečių tikslas?

— Manau, jog ketinimai Europoje pakeisti rusiškas dujas amerikietiškomis SGD — tik pirmas žingsnis. Aš čia matau JAV bandymą išspręsti ir kitą globalią makroekonominę problemą. Akivaizdu, jog šiandien pasaulinėje rinkoje, ypač inovacinių technologijų rinkoje, sparčiai aštrėja konkurencija, nes arenoje reiškiasi ne tik šalys su evoliucinio vystymosi istorija, bet ir nauji  žaidėjai. Trijų tradicinių pirmaujančių technologijų kovos centrai (Šiaurės Amerika, Europa ir Japonija su „azijietiškais tigrais“ pietryčių kontinente) netikėtai susidūrė su oponentais: Kinija, Indija ir kai kuriomis kitomis šalimis. Visos jos kaunasi dėl globalių konkurencinių galimybių augimo ir dėl savo konkurencinės zonos pasauliniame ūkyje išplėtimo.

Kyla klausimas: kaip JAV išsaugoti savo dominuojančias pozicijas pasaulinėje ekonomikoje, kurias jos užėmė dėka palankiai šiai šaliai ХХ amžiuje susiklosčiusių vystymosi sąlygų?

Juk tai du Europą nusiaubę pasauliniai karai (abu už ribų JAV, kurios tada tiekė ginklus ir kitą produkciją kariaujančioms šalims, o tai užtikrino karo metais amerikiečių ekonomikos augimą) ir du pokario atkuriamieji laikotarpiai (kai karo nusiaubta Europa ir Azijos ekonomika buvo atstatomi daugiausia JAV lėšomis, tiksliau — pasinaudojant amerikiečių kreditais, įsigyjant amerikiečių mašinas ir įrengimus, kurių gamyba užtikrino pokario JAV ekonomikos augimą) paskatino amerikiečių ekonomikos ir finansinės sistemos ūgtelėjimą, išvedant šalį į pirmaujančių vietą pasaulio finansų ir ekonomikos erdvėje.

Mano prielaidą ne visi priima rimtai, tačiau aš surizikuosiu dar kartą ją pagarsinti: amerikiečiai tiesiog bando pašalinti konkurentą, išmesti silpnesnę grandį. O pati silpniausia grandis šiame naujame konkurencijos rinkinyje — Europa. Kaip sakoma, nieko asmeniško, tik biznis.

Šiandien Europos Sąjungą drąsko prieštaravimai; jų dalį inicijavo pačios JAV. Visokie „arabų pavasariai“, prie kurių prisidėjo mūsų amerikietiški draugai, galų gale smogė pačiai Europai (pabėgėlių krizė ir t.t.).

Paaštrėjo vidinio Europos Sąjungos sutvarkymo klausimas. Ji „prarijo“ per daug naujų šalių ir niekaip negali jų „suvirškyti“. Europa taip ir netapo vienalytė: yra „Senoji Europa“ ir „Naujoji Europa“. „Naujosios Europos“ šalys prieš įstojimą į ES lyg per penkiolika metų praėjo paruošiamuosius kursus, ruošėsi sklandžiai integracijai į europietišką ekonomiką, mokėsi gyventi pagal europietiškas taisykles.

Ir tai kūrė melagingą laukimą, jog Europos Sąjungoje jos taps lygiomis tarp lygių. Tikėtasi — dabar tai mes bent pagyvensim! Tačiau taip neatsitiko. Melagingi lūkesčiai gimdo skaudžius nusivylimus. Investicijų srautas iš Briuselio, kuris galėtų išlyginti ekonominio išsivystymo lygį, į šias šalis neplūstelėjo. Tada NATO rėmuose jos pradėjo tiesiogiai kreiptis į užjūrio kolegas ir ieškoti jų paramos (konvertuojamos į ekonominę pagalbą).

Naujų ES narių rytuose amerikietiškos SGD — papildomas elementas, kuris padeda spręsti konkrečius ekonominius uždavinius. Jos ieško sau naudos. Daugelis Lenkijos politikų, pavyzdžiui, neslepia, kad jie norėtų atsisakyti rusiškų dujų, pakeisti jas amerikietiškomis SGD ir reeksportuoti į tą pačią Ukrainą. Pasikartosiu, kalbama apie privataus ekonominio uždavinėlio sprendimą.

Tačiau jei jos sėkmingas sprendimas leidžia atsisakyti rusiškų dujų (pavyzdžiui, pakeičiant pigesnes rusiškas ir vamzdžiais tiekiamas dujas ženkliai brangesnėm suskystintom, amerikietiškom),tai skatina energetinio komponento pabrangimą europietiškos gamybos išlaidose ir menkina Europos konkurencijos galimybes pasaulinėje rinkoje tose pirmaujančiose „taikiose“ šalyse, kuriose šiandien vystosi pagrindinė konkurentų kova. O mūsų amerikietiškiems draugams atsiranda galimybė plėsti savą konkurencijų galimybių zoną.

Aš manau, jog problemų sprendimas energetikos sferoje – ne galutinis, o tarpinis JAV tikslas. Gaisras Ukrainoje skatinamas ir siekiant išspręsti uždavinių visumą. Tam skirtas įstatymas „Dėl pasipriešinimo Amerikos priešams sankcijomis“. 232 straipsnis numato galimybę įvesti sankcijas prieš tuos, kurie dalyvauja rusiškų eksportinių dujotiekių statyboje. O 257 straipsnyje amerikiečiai prasitarė: pasirodo, jiems reikia didinti eksporto srautus, nes tai JAV sukuria naujas darbo vietas.

Vėlgi, visa tai žinodamas, aš netvirtinčiau, kad einamoji kova su „Šiaurės srautu–2“ — lemiamas mūšis. Kaip numato minėtas straipsnis 257, kova su šiuo dujotiekiu yra dalis (elementas) JAV politikos. Tai yra ji tęsis nepaisant šio „mūšio“ rezultatų: tai tik grandis ilgoje virtinėje veiksmų, kurių imtasi kintant energetinio pasaulio ekonomikai. Iš dalies šie pakitimai — amerikiečių skalūninės revoliucijos rezultatas. Daugelis nemano, kad tai buvo revoliucija, o kai kurios karštos galvos ją sieja su CŽV užmačiomis.

Aš prisilaikau kitos nuomonės: amerikiečių skalūninė revoliucija išties įvyko ir apvertė pasaulį, o jos pasekmių virtinė tokia ilga ir įvairialypė, išeinanti už energetinės sferos ribų (pavyzdžiui, ji radikaliai „apsuko“ tiesioginių užsienio investicijų pasaulinius srautus apdorojamosiose energijos imliose šakose). Tokiomis sąlygomis JAV sprendžia savo praktinę problemą, mes — savo, ir mūsų interesai Europoje susikerta.

— Verta dėmesio tai, kad Valstybės departamentas skyrė „labai daug laiko deryboms su partneriais ir sąjungininkais, esančiais už vandenyno, siekiant išaiškinti jiems CAATSA pasekmes“, tai yra amerikiečių sankcinio įstatymo. Tai reiškia, kad „partneriai“ ir „sąjungininkai“ priešinasi.

— Taip yra. Bet kodėl jie priešinasi? Įvairūs ekspertai (pasakykim taip: žmonės su ekonomiškomis smegenimis) supranta: atsisakyti „Šiaurės srauto–2“ Europai nenaudinga, nes jis mažina rusiškų dujų tiekimo Europai išlaidas. Tai reiškia, jog išliks rusiškų dujų konkurencingumas net jeigu kris Europoje kainos. Amerikiečių SGD jau parduodamos Europoje nuostolingai. Vadinasi, JAV reikia, kad dujų kainos Europoje kiltų. Todėl „Šiaurės srautas–2“ joms neduoda ramybės. Vadinasi, reikia pašalinti konkurentą. Štai ir ieškoma būdo, kaip tai padaryti padoriai.

Bet kokia kooperacija turi būti abiem pusėm naudinga. Jeigu vienų pelnas kitiem duoda nuostolį, tai jau ne bendradarbiavimas.

— Ar europiečiai pasiryžę ryžtingai laikytis savų pozicijų ir veltis prekybinėn kovon su JAV?

— Nenoriu kartoti įsigaliojusios nuomonės, kad Europa — faktiškai okupuota teritorija, o tai reiškia, kad ji nepajėgi priimti savarankiškų sprendimų, tačiau bet kokiame ginče tai svarus argumentas. Prisiminkite, kiek metų Vokietija stengėsi gauti informaciją apie atsargas savo aukso, kurio dalis buvo saugojama JAV. ES šioje situacijoje pasireiškia kaip jaunesnioji partnerė. Todėl europiečiai priešinasi, tačiau tai daro tik savo svorio kategorijoje.

Pateiksiu pavyzdį. Jūs žinote, kad egzistuoja įvairios energetikos Europoje reguliavimo sistemos gairės — taip vadinami energetiniai paketai. Nuo 2003 metų, nuo Antrojo energetinio paketo, Europa ėmėsi kurti vieningą dujų vidaus rinką. Jei mes turime vieningą vidinę rinką, tai bet koks dujų tiekimas į bet kurią ES šalį yra tiekimas į ES. Nesvarbu, kur yra įvadas. Ši nuostata įtvirtinta Antrame energetikos pakete.

Tačiau kokia retorika mus pasiekia iš JAV ir daugelio Europos Sąjungos šalių, kurios pasisako prieš „Šiaurės srautą–2“? Esą dujos tiekiamos Vokietijai ir ši šalis taps dominuojančia Europos Sąjungoje. Vokietija esą taps dujų paskirstymo Europoje centru. Vokietija perpardavinės dujas... Tai yra Vokietija sustiprės. Šiuo klausimu man dažnai tenka įsivelti polemikon, ir aš sakau: „Vaikinai, studijuokite materialinę dalį, skaitykite savo įstatymus“.

Dujų tiekimas į bet kurią ES šalį yra tiekimas į ES. Jeigu jūs negalite savo teritorijoje užtikrinti nenutrūkstamą dujų, patenkančių į ES iš svetur, srauto padidėjimą, jeigu jūs investavote lėšas, siekiant sukurti tarp atskirų šalių vidinius dujotiekius — sandūras, tai čia jau ne mūsų problemos ir ne mūsų atsakomybė.

Daug ginčytinų situacijų iškyla dėl dviejų priežasčių: pirma, atleiskite, dėl kompetencijos stokos ir net savų įstatymų nežinojimo; antra, dėl vidinių prieštaravimų.

Bet yra dar vienas svarbus niuansas. Džordžas Fridmanas, kuris sukūrė ir tapo direktoriumi vedančiosios privačios žvalgybinės analitinės kompanijos  geopolitikos srityje Strategic Forecasting lnc. (STRATFOR), kuri JAV vadinama „šešėline ČŽV“, 2016 metų vasario 4 dieną kalbėdamas Čikagos taryboje globaliais klausimais paaiškino, jog galutinis JAV tikslas Europoje — sukurti teritoriją tarp Baltijos ir Juodosios jūrų — „Tarpjūrį“, „kurio koncepciją sugalvojo dar Pilsudskis“.

JAV, Fridmano žodžiais, „pirmasis tikslas — neleisti, kad vokiečių kapitalas ir technologijos susijungtų su rusų gamtiniais resursais ir darbo jėga ir sudarytų neįveikiamą kombinaciją.

<...> JAV šiuo klausimu triūsia jau visą amžių. <...> JAV koziris, mušantis šią kombinaciją, — atribojimo linija tarp Pabaltijo ir Juodosios jūros. Juk Vokietija — galinga ekonominė valstybė, tačiau tuo pat metu – labai žeidžiama ir geopolitiškai silpna“. Tokio „pylimo“ statyba, jei tikėti Fridmanu, Vašingtonui daug svarbesnė, nei kova su islamo radikalizmu, kurį pranešėjas pavadino „problema, tačiau ne itin grėsminga JAV“. Skirtingai nei Vokietijos ir Rusijos susivienijimas, kurios, veikdamos kartu, pagal Fridmaną, yra „vienintelė jėga, kelianti JAV rimtą pavojų“. Taigi Fridmanas mato amerikiečiams iškilusį uždavinį sukurti aplink Rusiją „sanitarinį kordoną“, kurio pagalba bus galima laikyti prie kojos Vokietiją ir visą Europos Sąjungą.

Buvo siūlomas tas pats variantas, tik dujotiekis turėjo eiti ne jūros dugnu, o per Pabaltijo ir Lenkijos teritorijas. Už tranzitą jie būtų gavę papildomų pajamų. Šiuo atveju žmonės paprasčiausiai skaičiuoja prarastą naudą. Dėl to, jog nenutiestas dujotiekis „Gintaras“, jie praranda pinigus. O kas kaltas? Rusija!

Apmaudu, kad Amerikos ir Europos „pasibadymo“ charakterį sąlygoja jaunesniojo partnerio vaidmuo, kurį atlieka pastaroji. Europiečiai sugebėjo atsisakyti naujo prekybinio susitarimo su JAV (greičiausiai sąlygos buvo visiškai nepriimtinos), tačiau kai kada jiems nepakanka ryžto ir galimybių ginti savo interesus, ypač esant rimtoms vidinėms problemoms. Naujų sprendimų paieškoms gali neužtekti net laiko, jog kalba eina apie ilgalaikius procesus.

— JAV savo ruožtu taip pat nelinkusios nusileisti?

— Jos visada stengiasi „prastumti“ savo interesus. Man teko daug dirbti su amerikiečiais, kai aš buvau Jegoro Gaidaro vyriausybėje (aš vadovavau Rusijos — Amerikos darbo grupei naftos ir dujų klausimais tarpvyriausybinėje komisijoje), o paskui dirbau Gaidaro patarėju antrojo jo atėjimo vyriausybėn metu.

Jis paskyrė velionį Aleksandrą Arbatovą ir mane vadovauti valstybinei ekspertizei vieno stambaus investicinio naftos ir dujų projekto, kurį buvo numatyta realizuoti kartu su mūsų užjūrio partneriais. Amerikiečių sutarties projektas, mūsų su Arbatovu nuomone, buvo visiškai nepriimtinas. Tačiau JAV partneriai turėjo aiškią poziciją: arba mes besąlygiškai priimam jų variantą, arba išvis nieko nebus. Viskas arba nieko.

Viso to išdavoje jie taip ir pasėdėjo šešerius metus su savo nepakeičiamu variantu ir nesulaukė sutikimo. Tokie žmonės kartais nesugeba susitarti. Jų politika grindžiama tikėjimu, kad jie sėja demokratiją, ir todėl jiems viskas galima. Ir kad jie visada teisūs. Ir kad America First.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 3 — id: `scraped:rubaltic_lt:6925401661bda36e`

**Title:** Skvernelis ir vaikai: kaip Lietuvos premjeras lankėsi Donbase

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos premjeras Saulius Skvernelis apsilankė Ukrainoje ir pažadėjo Kijevo sąjungininkams ir ateityje tiekti ukrainiečių kariuomenei ginklus karui Pietryčiuose. Labiausiai Skvernelio vizito metu įsiminė jo išvyka į Donbasą, kur neperšaunamą liemenę užsivilkusiam premjerui buvo atvesti vienmarškiniai vaikai. Šiame kontraste — Lietuvos pozicijos Ukrainos krizės klausimu esmė: pakišti taikius gyventojus smūgiams, o patiems gyventi saugiai.

Savo išvyką Lietuvos premjeras apibendrino Kijeve 11-ame Forume saugumo klausimais. Ten Skvernelis žadėjo ir ateityje tiekti Kijevui lietuviškus ginklus, amuniciją ir kitą karinę įrangą.

„Mes, žinoma, tai palaipsniui ir vykdome, ir vyriausybė jau priėmė sprendimą, — kalbėjo Skvernelis apie paramą Ukrainos kariuomenei ginklais. — Ukrainai belieka išspręsti techninius klausimus. Mes šiuo metu palaikome techninį aprūpinimą ir ateityje tuo užsiiminėsime“.

Lietuvos vyriausybės vadovas ypatingai pabrėžė, kad Lietuva tiekia Ukrainai ginklus ne karui, o taikai. „Mes privalome ir ateityje padėti Ukrainai letaliais ginklais, tačiau siekiame parodyti visam pasauliui, kad nenorime skatinti karo. Nes mes privalome gintis. Todėl kad letalių ginklų tiekimas reiškia, jog mes galime išsaugoti gyvybes snaiperių, kitų kariškių, civilių žmonių“, — pareiškė Skvernelis ir, norėdamas įrodyti, kad jam artimos Ukrainos nelaimės, pridūrė, jog šio vizito metu jis aplankė Donbasą, kad „savo akimis pamatytų regioną, nukentėjusį nuo Rusijos agresijos“.

Lietuvos premjero išvyka į Donbasą tapo jo ukrainietiškos programos „vinimi“. Lietuvos žiniasklaida būtent jai skyrė daugiausia dėmesio, ir tai galima suprasti. Tie kadrai, kuriuose Skvernelis apsireiškia su juodais akiniais ir neperšaunama liemene, vaizdingesni nei protokolo filmavimas Skverneliui susitinkant su Ukrainos kolega Vladimiru Groismanu, kai jie vėl susitarė kartu kovoti prieš dujotiekį „Šiaurės srautas–2“ ir lietuviškoji šalis šimtas tūkstantinį kartą pareiškė remianti europietiškus Kijevo siekius.

Ukrainos kontroliuojamoje Donecko srities dalyje Lietuvos premjeras aplankė pafrontės Avdejevką, esančią prie skiriamojo ruožo tarp Ukrainos karinių pajėgų ir taip vadinamos Donecko liaudies respublikos.

Vienoje nuotraukoje jokių saugos priemonių neturintys ir prieš premjerą stovintys vaikai mojuoja vėliavėlėmis ir valstybine Lietuvos vėliava, o Skverneliui dėl visiško saugumo akivaizdžiai trūksta šalmo ir dujokaukės.

Kitoje nuotraukoje Lietuvos ir Ukrainos delegacijos stovi smėliadėžeje su neperšaunomis liemenėmis ir ištiesusios savo šalių vėliavas, o priešais stovi vaikai, kurie vėlgi vienmarškiniai.

Šios nuotraukos plačiai pasivaikščiojo internete ir „užmušė“ visą Skvernelio apsilankymo Ukrainos fronto linijoje patosą — Lietuvos premjeras po to galėjo ilgai pasakoti apie Lietuvos lėšomis suremontuotą Avdejevkos ambulatoriją, apie savanorių pagalbą įrengiant aikštelę vaikams — vis tiek prieš auditorijos akis pirmiausia iškyla vaizdai, kaip aukšto rango Kijevo ir Vilniaus valdininkai vaikščioja sugriautos Avdejevkos gatvėmis apsisaugodami neperšaunamomis liemenėmis, o vienmarškiniai vaikai toje pat Avdejevkoje žaidžia smėliadėžėse.

Lietuva iš pat pradžių rėmė Donbaso sukilimo malšinimą jėga ir buvo vienu iš esminių Kijevo „advokatų“, kai šis metė kariuomenę prieš taikius žmones, pareikalavusius Ukrainos Pietryčių sritims mokesčių, kultūros ir kalbų autonomijos. Donbaso teisės reikalauti savivaldos ir federalizavimo Kijevas nepripažino, lygybės ženklo tarp administracijų užgrobimo Donecke bei Luganske ir Lvove bei Ivano-Frankovske neįrašė, ir Vilnius visiškai solidarizavosi su juo šiais klausimais: „prorusiškieji“ lai nesvajoja apie lygybę, demokratiją ir žmogaus teises!

Kuo labiau ukrainietiško „maidano“ valdžios veiksmai dvelkė barbariškumu, tuo ryžtingiau ją rėmė Lietuvos valdžia. Ir net Lietuvos politikai tiesiogiai pritarė kruvinam smurtui Odesoje: europarlamentaras Petras Auštrevičius pavadino tuos, kurie Odesos profsąjungų rūmuose buvo sudeginti gyvi, „kolorado vabalais“ ir pasidžiaugė, jog jų „antplūdis sustabdytas“.

Ginklus kariaunančiai Ukrainos kariuomenei Lietuva pradėjo tiekti pirmoji pasaulyje. Tiekė atvirai ir demonstratyviai, rodydama pavyzdį „bailiams“ Vakarų sąjungininkams, neryžtingai kalbėjusiems, kad regioninius konfliktus neįmanoma išspręsti karinėmis priemonėmis, kad šalys turi sėsti prie derybų stalo. Lietuva iš pradžių nepripažino Minsko susitarimų ir iki vizito į Maskvą tuometinio JAV valstybės sekretoriaus Džono Keri 2015 metų gegužę, kai šis pareiškė, jog Donbaso konflikto neįmanoma išspręsti kariniu būdu, nelaikė Minsko proceso neturinčiu alternatyvos.

Ir fotografavimasis apsisaugojant neperšaunamomis liemenėmis, išrikiuojant prieš save bejėgius Donbaso vaikus, — tai kaip niekada išryškina.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 4 — id: `scraped:rubaltic_lt:c8c14eed0c6da3e3`

**Title:** Pabaltijis parėmė Sirijos bombardavimą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Pabaltijo šalys viena po kitos parėmė Sirijos bombardavimą. Pritardamos amerikiečių partneriams griaunant tarptautinę teisę ir pakeičiant ją stipriojo teise, Lietuva, Latvija ir Estija kasa sau duobę. Jos pritaria praktikai, kai branduolinės supervalstybės aiškinasi santykius kariniu būdu trečiųjų šalių teritorijose ir bet kuri kariniu atžvilgiu galinga šalis gali smogti raketomis silpnesniai šaliai apeidama JT Saugumo tarybą ir nesivargindama ieškant įrodymų šios šalies kaltei. Jei ši praktika taps tarptautinių santykių norma, Sirijos tautos likimo gali sulaukti ir Pabaltijo šalys.

„Ribotas JAV, Didžiosios Britanijos ir Prancūzijos jėgos panaudojimas — kraštutinė, tačiau reikalinga priemonė, siekiant sustabdyti panašius veiksmus, — taip Sirijos bombardavimą, atsakant į esą prezidento Bašaro Asado įsakymą panaudoti cheminį ginklą, pakomentavo Estijos premjeras Juri Ratas . — Tikimės, kad ateityje bus galimybė sulaikyti masiško naikinimo ginklo panaudojimą diplomatiniais metodais. Tai — būtina sąlyga prisilaikant tarptautinių sutarčių siekiant išvengti konfliktų“.

„Cheminio ginklo panaudojimas — šiurkštus tarptautinės teisės pažeidimas ir sunkus nusikaltimas, kurio neįmanoma pateisinti“, — pareiškė Latvijos užsienio reikalų ministras Edgar Rinkevič ir pabrėžė, kad raketų smūgius Sirijai vertina kaip „adekvačias priemones“.

Rinkevičiui ir Ratui antrina jų lietuviškasis kolega.

„Mes remiame tuos veiksmus, kurių ėmėsi JAV, Didžioji Britanija ir Prancūzija. Šios reakcijos buvo tikėtasi, nes Sirijos režimas peržengė ne vieną „raudoną liniją“ [iš tų], kurios buvo nubrėžtos anksčiau, — pasakė Linas Linkevičius. — Tik ryžtingi veiksmai galėtų pakoreguoti [Bašaro Asado] režimą ir pasiųsti visiškai aiškų signalą jam ir toms šalims, kurios beatodairiškai palaiko režimą — visų pirma tai Rusija ir Iranas“.

Kaip žinia, nieko nenustebino ši visiška Lietuvos, Latvijos ir Estijos vienybė. Būtent tokios reakcijos ir buvo laukta iš Pabaltijo. Juk tai ne pirmąsyk.

Šerchanai gali keistis, tačiau šakalų elgesys nekinta. Antrojo pasaulinio karo metais Lietuvos, Latvijos ir Estijos kolaborantai šliaužiojo prieš Hitlerį ir atliko šlykštų nacių darbą siekdami sau naudos. Žudė žydus ir grobstė jų turtą, apsigyveno jų namuose ir lupo iš lavonų burnų auksinius dantis.

Šaltojo karo metais būsimieji Paks Americana „vanagai“ smerkė amerikiečių imperializmą ir demaskavo NATO kariauną komjaunimo susirinkimuose ir kažkokios Vilniaus TSKP mokyklos auditorijose.

Pabaltijo šalys karštai pritarė Jugoslavijos bombardavimams. Už Belgrado bombardavimą jos pasisakė dar prieš tai, kai amerikiečiai nutarė jį bombarduoti. Ir už tai išsiderėjo sau teisę įstoti į NATO be priklausančių karinėms išlaidoms 2 BVP procentų.

Lietuva, Latvija ir Estija abiem rankom balsavo už karinį įsiveržimą į Iraką. Taip norėjo, kad ši nepriklausoma šalis būtų sunaikinta ir okupuota, kad nepabijojo prieš įstojimą į ES pasisakyti prieš Vokietiją ir Prancūziją, kurios nenorėjo tuo užsiimti.

Ir juk neapsiriko: JAV spaudžiant, Pabaltijis buvo priimtas į Europos Sąjungą ir pasodintas ant europietiškų fondų dotacijų net neatitinkant narystės ES Maastrichto kriterijams.

Amerikiečių specialiosios tarnybos sąmoningai užsiiminėjo dezinformacija. JAV valstybės sekretorius Kolin Pauel rodė JT Saugumo taryboje mėgintuvėlį su skalbimo milteliais. Buvusiam Didžiosios Britanijos premjerui Toni Blerui net teko atsiprašyti rinkėjų dėl karo Irake: pripažinti, kad žvalgybos duomenys buvo netikslūs, cheminio ginklo nebuvo, o Sadamo nuvertimas paskatino „Islamo valstybės“ (Rusijoje uždrausta organizacija — RuBaltic.Ru past.) atsiradimą.

Tačiau Pabaltijui šie demaskavimai kaip nuo žąsies vanduo. Po kelerių metų Lietuva, Latvija ir Estija lengvai pritaria Sirijos sunaikinimui. Priežastys tos pačios. Kai 2013 metais JAV prezidentas Barakas Obama suko galvą dėl Hamleto klausimo — ar bombarduoti (Damaską)? — Vilnius, Ryga ir Talinas pasisakė choru: bombarduoti!

Smūgis Sirijai — adekvatu! JT pritarimo nereikia, mes vertinam aktyvų JAV vaidmenį tarptautiniuose reikaluose — sakė tie patys žmonės, kurie po dvejų metų piktinosi, kad Europos Sąjunga verčia juos priimti bėglius iš Sirijos. Ir kuriuos dabar žavi Trampo „tomohavkai“.

Jei už skliaustų palikti etikos klausimus, tai pabaltijiečių taktika logiška ir pagrįsta. Ši taktika — remti amerikiečių avantiūras dar ryžtingiau, nei pati Amerika , — ne kartą pasiteisino. Tačiau naujomis sąlygomis tokios taktikos panaudojimas gali atsirūgti Pabaltijui pavojingomis pasekmėmis.

Pabaltijis galėjo gyventi saugiai vienapoliškame pasaulyje tol, kol JAV buvo tokios galingos ir stiprios, jog galėjo bombarduoti bet ką. Vardan demokratijos ir dėl naftos, nėkiek nebijodamos pasekmių. Naujame daugiapoliškame pasaulyje taip nebus. Dabar Amerika nepajėgia įveikti net mažos Šiaurės Korėjos. Trampas gali be galo gąsdinti Kim Čen Yną „dideliu raudonu mygtuku“ — galų gale jam tenka sutikti eiti derybų keliu.

Amerikiečių praktika „koubojiškai“ elgtis tarptautinėje arenoje atveria „Pandoro skrynią“ ne tik JAV priešams, bet ir jų sąjungininkams. Tai pradedama suprasti ir Vakaruose.

„Kai kokia nors šalis vienašališkai imasi priemonių įstatymiškai nepagrįstai, tai skatina kitas šalis veikti taip pat ir trukdo mums apskųsti tokius veiksmus“, — taip britų parlamente Sirijos bombardavimą komentavo opozicijos lyderis Džeremi Korbin. Leiboristų partijos pirmininko žodžiai — tiksliausia įvykių Sirijoje pasekmė.

Pavyzdžiui, Pabaltijui.

Ir dėl to jokio NATO susidūrimo su Rusija neįvyks. Sirijos pavyzdys parodė, kad branduolinės valstybės pasiruošusios pasitikrinti raumenis trečiųjų šalių teritorijose, stengdamosi nesužeisti viena kitos, kad neįvyktų tiesioginis karinis susidūrimas.

Visavertis karas tarp branduolinių šalių — visuotinas iki besąlygiškos kapituliacijos — neįmanomas, nes karinis sunaikinimas bus abipusis. Tačiau įmanomas šalutinis karas: ne priešo teritorijoje, nepanaudojant branduolinio ginklo ir ne tiesiogiai, o per sąjungininkus.

Toks karas šiandien faktiškai vyksta Sirijoje.

Niekas dėl Latvijos ir Lietuvos branduolinio karo su Rusija nepradės: negi raketos būtų skirtos Kalifornijai. Net sankcijų neįves: tuomet neliktų tokių sankcijų, kurių Vakarai dar Rusijai netaikė. Paprasčiausiai aiškinsis santykius neutraliose teritorijose „džiaugsmui“ Pabaltijo politikų, kurie patys pateks į tą duobę, kurią kasė kitiems.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 5 — id: `scraped:rubaltic_lt:971199e2c811107a`

**Title:** Rusija atjungia nuo savęs Pabaltijį

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Dviejų naujų šiluminių elektrinių Kaliningrado srityje eksploatavimo pradžia Lietuvoje buvo sutikta skausmingai: dabar Kaliningrado energetinė sistema pajėgi dirbti izoliuotame režime ir Rusija gali pasitraukti iš penkių buvusių tarybinių respublikų energetinio žiedo, nelaukdama, kol iš jo pasitrauks Pabaltijis. Jeigu anksčiau Pabaltijo šalys naikino ryšius su Rusija, tai dabar Rusija stengiasi atskirti savo infrastruktūrą nuo šių šalių. Ir nors Lietuva, Latvija ir Estija demonstruoja norą nutolti nuo savo rytų kaimyno, joms labai nepatinka, kad jūrų uostai, vamzdynai ir elektrinės išdygsta siekiant apeiti Pabaltijį.

Kaliningrado srities rytuose, Gusevo ir Sovetsko miestuose, pradėjo veikti Majakovskio ir Talachovskaja šiluminės elektrinės. Iškilmingame jų atidaryme dalyvavo Rusijos prezidentas Vladimiras Putinas, o tai pabrėžia aukščiausiai Rusijos valdžiai įvykio svarbą.

Tačiau dviejų šiluminių elektrinių srities rytuose įvedimu eksploatacijon Kaliningrado energetikos modernizavimas nesibaigia. Šių metų rudenį bus įvestas rikiuotėn pirmasis Pregulio šiluminės elektrinės prie Kaliningrado blokas. Sekančiais mėnesiais pradės dirbti kiti trys blokai, ir jau 2019 metų balandžio mėnesį 456 megavatų Pregulio elektrinė funkcionuos pilnu pajėgumu. O 2020 metų vasarą Svetloje veikti pilnu pajėgumu pradės rezervinė Primorsko šiluminė elektrinė.

Iki šiol Kaliningrado sritis buvo vienoje energetinėje Rusijos sistemoje per Lietuvos elektros tinklus. Lietuvos valdžios, planuodamos pasitraukimą iš elektros energijos žiedo, piktai džiūgavo, su kokiu galvos skausmu susidurs Maskva Kaliningrado srities aprūpinimo energija klausimu. O Lietuvos pozicija „kaimyniška“: nutraukiame su „okupantais“ infrastruktūrinius ryšius, o energijos tiekimas Kaliningradui — ne mūsų problema.

Tačiau naujiena, kad Rusija problemą išsprendė dar iki jos atsiradimo ir dabar gali pati pasitraukti iš žiedo, neerzindama Pabaltijo šalis naudojimuosi jų elektros tinklais, tų šalių kažkodėl nedžiugina.

„Po to, kai Pabaltijo šalys pradėjo diskusijas dėl atsijungimo nuo Rusijos elektros sistemos žiedo ir sinchronizavimo su Vakarais, Maskva iškėlė Kaliningrado klausimą, ir tai turėjo tapti vienu iš svarbiausių derybų klausimų. Tačiau dabar Rusijos pasiruošimas išsaugoti izoliuotą Kaliningrado srities energijos sistemą sako, jog diskusijų šiuo klausimu nebus“, — taip naujų elektrinių įvedimą rikiuotėn Kaliningrado srityje komentavo Lietuvos energetikos ministras Žygimantas Vaičiūnas.

Pareiškimas išties gluminantis.

Ar ne tame ir buvo Pabaltijo sumanymas trauktis iš energetinio žiedo, priverčiant Rusiją kalbėtis su Latvija, Lietuva ir Estija iš pozicijų silpno ir prašančio? Esą, mielieji, malonėkite suprasti ir mus, mes turime Kaliningrado sritį, ji bus palikta be elektros, jeigu jūs išeisite iš elektros žiedo. Galvokime kartu, kaip šią problemą spręsti, ir raskime kompromisą, skirkite mums dėmesį, mes pasiruošę nuolaidžiauti jums kitais klausimais.

Tačiau vietoj to Rusija vėl pademonstravo savo agresyvę imperinę esmę: per keletą metų pastatė naujas elektrines ir dabar bet kuriuo momentu gali išvyti Pabaltijį iš savo energosistemos, jei jis taip pageidauja iš jos ištrūkti. Skaudu? Žinoma, skaudu. Viena, kai tu sakai „lik sveika, Rusija nepraustoji“, išdidžiai pasisuki ir išeini link saulėlydžio, ir visiškai kitkas, kai pati Rusija apsuka tave ir siunčia link vakarų, dar ir spirdama į minkštą vietą.

„Tas žingsnis rodo, kad statomas naujas vidinis žiedas, kuris leis atskirti Pabaltijį nuo Rusijos kontinentinio tinklo“, — taip apie naujas elektrines Kaliningrado srityje, Ostroveco atominės statybą Baltarusijoje ir Rusijos su Baltarusija tinklų rekonstrukciją pasakė Lietuvos energetikos ministro patarėja Aurelija Vernickaitė. Negi tai nėra laimė? Rusija pati atsiskiria nuo Pabaltijo. „Imperija“ nutraukia infrastruktūrinius ryšius su „okupuotomis“ teritorijomis. Reikia džiaugtis. Tačiau ministro patarėja apie tai, kas vyksta, kalba ne su pasitenkinimu, o su pavojaus gaidele.

„Aš suprantu, viskas jau paruošta, o tai galima daryti, ministerija taip pat kalba, jog tai būtina daryti nedelsiant, juk mes jau pralaimėjome vieną panašų mūšį. Tai liečia atominę elektrinę. Ta pati analogija: Rusija aplenkė mus, ir Baltarusijos skatinimas statyti atominę elektrinę palaidojo viltis Pabaltijo šalyse statyti tokią elektrinę ir energiją pardavinėti kaimynams“, — taip Rusijos ir Baltarusijos energetinius projektus pakomentavo Lietuvos Seimo deputatas konservatorius Paulius Saudargas.

Šie Lietuvos veikėjų pareiškimai labai įdomūs ir atviri.

Dešimtmečiais deklaruojant norą neturėti reikalų su Rusija, laikytis nuo jos kuo toliau ir visais ketinimais būti Europoje, Pabaltijo šalys labai norėjo pokalbio su Kremliumi, bet tik savo sąlygomis. Jų idilija: Rusija — atgailaujantis agresorius, pripažįstantis „sovietinę okupaciją“, maldauja atleidimo už Pabaltijo tautų „genocidą“, raudoja ir moka Pabaltijui šimtus milijardų dolerių materialinių kompensacijų, iš kurių lietuviai, latviai ir estai gevena dar geriau, nei anuomet Tarybų Sąjungoje.

Vietoj to Maskva išvis atsisakė kalbėtis su Pabaltiju ir pastatė prie Baltijos jūros savo prekybos uostus, kad įveiktų tranzitinę priklausomybę nuo Pabaltijo respublikų. Ir dabar Lietuvos, Latvijos ir Estijos vadovams tenka iš pykčio sugniaužti kumštis: jų uostai ir geležinkeliai iš rusiško tranzito netrukus nepamatys nė vieno rublio, kalbėtis su jais apie „okupaciją“ niekas taip ir neketina, o uostų monopolijos ir, kaip matome, galimybės daryti poveikį Rusijai daugiau nėra.

Pabaltijo pasitraukimas iš energetinio žiedo — tos pačios istorijos tąsa. Pražiopsota puiki perspektyva pakalbėti su Rusija iš jėgos pozicijų dėl energijos tiekimo Kaliningradui. Pamatyti Putiną prašytojo vaidmenyje.

Juk Rusija sparčiai pašalino problemą, per keletą metų pastatydama kelias elektrines. O dar vos ne Lietuvos prezidento rinkimų proga „Rosatomas“ įves rikiuotėn Baltarusijos AE. Nauji rusų uostai prie Baltijos jūros didina krovinių apyvartą. Geležinkelis, apeinant Ukrainą, pastatytas per du metus ir jau eksploatuojamas.

Na, o Visagino AE projektas užsibaigs Power Point pristatymo stadijoje. Geležinkelio Rail Baltica Pabaltijo šalys nesugeba pastatyti per du dešimtmečius. Ventspilio naftotiekis tuščias. SGD terminalas Klaipėdoje — „lagaminas be rankenos“, kurį ir nešti neįmanoma, ir išmesti negalima. Latvijos ir Estijos uostai kasmet vis labiau praranda krovinius.

Ir jų pirmiesiems asmenims, besistengiantiems demonstruoti abejingumą ir nusišalinimą, nepavyksta nuslėpti savo pavydo ir pykčio. Didžiuliai resursai, kurie anksčiau keliavo per Pabaltijį, dabar jį apeina. Aplink juos kyla nauji objektai, o pabaltijiečių galingumai stovi be darbo ir rūdija.

Ir kalbėtis su jais Rusijoje niekas nenori. Ir jau nieko pakeisti neįmanoma. Belieka gniaužti kumštis ir griežti dantimis.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 6 — id: `scraped:rubaltic_lt:4bfd8a371fc70d0f`

**Title:** Kandidatai į Lietuvos prezidentus kritikuoja Dalią Grybauskaitę

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Potencialūs kandidatai į Lietuvos prezidentus kritikuoja šių dienų šalies realijas. Vieni po kitų girdisi raginimai normalizuoti santykius su Rusija ir kitais Lietuvos kaimynais. Norinčiųjų tapti Dalios Grybauskaitės įpėdiniu tarp pretendentų į šį postą nesimato. Prezidentinės kampanijos metu bus neigiamai vertinama tai, ko pasiekė šalis valdant Daliai Grybauskaitei.

„Nuo pat įstojimo į ES Lietuva sukūrė tikrą stebuklą. Lietuvos išsivystymo lygis per pirmuosius 10 narystės ES metų pašoko 50 proc. Tačiau jau keletą metų iš eilės matome, kad progreso nėra, — 2014–2016 metais mes nė kiek nepriartėjome prie europiečio vidutinio pragyvenimo lygio. Be ambicinių struktūrinių reformų nebus Lietuvos atgimimo ir augimo, mes nesukursime tokio stebuklo, kokį sukūrėme, stodami į ES“, — pasakė Lietuvos premjeras Saulius Skvernelis konferencijoje Lietuvos ekonomikos klausimais.

Šis Skvernelio pasisakymas — akmenukas į prezidentės Dalios Grybauskaitės daržą. Pasirodo, pastaraisiais metais Lietuva pergyvena „sąstingį“. Lietuvos premjeras pasirinko politiškai labai svarbų laiką, kad tai pasakytų. Dabartinė vyriausybė dirba vos ilgiau metų, todėl ant jos pečių negalima suversti atsakomybės už stagnaciją. Ir iki prezidento rinkimų liko vos daugiau metų, todėl vyriausybės vadovas gali pretenduoti į valstybės vadovo vietą kaip reformatorius.

Saulius Skvernelis nedviprasmiškai privedė auditoriją prie šios išvados. Premjeras pareiškė, kad vyriausybė ruošia mokesčių ir pensijų sistemų reformas, o taip pat reformas, skatinančias inovacijų politiką, kovos su šešėline ekonomika, švietimo, sveikatos apsaugos reformas ir t.t.

O tuo tarpu ponia prezidentė nuo pat pradžių kritikavo vyriausybės pensijų ir mokesčių reformas. Grybauskaitė paragino ministrus „negriauti to, kas veikia“. Štai ir darykite išvadą, kodėl Lietuva atsidūrė sąstingyje ir nesivysto.

Atviras vyriausybės vadovo šiuolaikinės Lietuvos „sėkmės istorijos“ neigimas — savaime įvykis.

Norint įgyvendinti „rokiruotės“ scenarijų, reikėtų, kad dabartinė prezidentė paremtų Skvernelio kandidatūrą, bet apie tokią paramą negali būti kalbos, nes Grybauskaitė vis dažniau puola vyriausybę, o premjeras vis dažniau kritikuoja prezidentės politiką.

Bet ir sociologai sufleruoja premjerui, jog skelbti save prezidentės kurso tęsėju nėra sėkminga politinė strategija. Absoliuti lietuvių dauguma palaikė Skvernelį jo konflikte su Grybauskaite dėl santykių su Rusija, kai premjeras pasiūlė atkurti dialogą su Maskva aukščiausiame politiniame lygyje, o prezidentė pasisakė kategoriškai prieš.

Sociologija ginče su Grybauskaite užsienio politikos klausimu pasinaudoja kitas galimas kandidatas į prezidentus — buvęs Lietuvos ambasadorius Rusijoje, dabar Europos instituto Kauno technologijos universitete direktorius Vygaudas Ušackas.

„Pagal mūsų universiteto užsakymą neseniai buvo pravesta apklausa aukšto emigracijos lygio priežasčių klausimu. Paaiškėjo, kad pagrindinės priežastys — ekonominės ir socialinės. Apklausa parodė: 64,2 proc. respondentų pagrindine emigracijos priežastimi laiko, lyginant su atlyginimais, aukštas kainas. 55,6 proc. — esant menkiems atlyginimams ir pensijoms, galimybių oriai gyventi stoką. O Rusijos agresijos bijo tik 2,4 proc. respondentų, ir tai 15-oji priežastis iš 16“, — neseniai pareiškė Ušackas ir, remdamasis šiais duomenimis, paragino nesąžiningus politikus nustoti naudotis „rusų korta“, nes dauguma lietuvių nerimtomis laiko kalbas apie artėjančią rusų agresiją.

Ušacko žodžiai panašūs į Skvernelio žodžius apie tai, kad nuo 2014 metų spartų Lietuvos augimą pakeitė sąstingis. Būtent nuo 2014 metų politinį Grybauskaitės kursą galima pavadinti „Priešas prie vartų“.

„Akivaizdu, jog iki šiol Lietuvoje nesukurta strategija, nėra struktūrinių pokyčių, kurie skatintų piliečius pozityviai mąstyti ir priimti šaliai perspektyvius sprendimus. Tam reikalinga skaidri politinė valia, kurios pagrindas — konkretūs darbai, politinė atsakomybė“, — taip aiškina Vygaudas Ušackas rekordinio gyventojų bėgimo iš Lietuvos masto priežastis.

Kitas žinomas ir įtakingas Briuselyje lietuvis — ES sveikatos apsaugos ir maisto produktų saugos komisaras Vytenis Andriukaitis lietuviškų nelaimių priežastį įžvelgia ponios prezidentės užsienio politikoje.

„Mūsų partijos atstovas vadovauja Užsienio reikalų ministerijai, tačiau šioje ministerijoje nesimato socialdemokratų politikos. Aš nematau arba sunkiai įžvelgiu kairiąją Linkevičiaus užsienio politiką, todėl kad užsienio politika šiandien — ryškiai dešinioji Dalios Grybauskaitės politika. Dešinioji ir pagal retoriką, ir pagal mechanizmus, ir pagal mąstymą: „Mes pavojuje, aplink priešai — priešas jau už tvoros“. Taigi visuomenėje tvyro pasėta baimė ir kažkam naudinga žaisti ta baime“, — mano Andriukaitis.

„Galiu jums pateikti daug pavyzdžių, kaip šalys — ES narės bendradarbiauja tose sferose, kurios atitinka ES Tarybos rėmus. Komisija užsiima tuo pat. Tai kodėl Lietuva negali to daryti, niekaip nesuprantu. Kodėl gali Vokietija, Suomija, Belgija, o Lietuva negali?“ — kelia klausimą Andriukaitis.

Vygaudas Ušackas savo ruožtu tvirtina, kad Maskva neketina pulti Pabaltijo šalių ir, priešingai, suintertesuota bendradarbiavimu su Lietuva. „...tokias išvadas darau ne tik remdamasis žiniomis, kurias įgijau dirbdamas Maskvoje. Man žinoma, kad Rusija siūlė organizuoti susitikimą URM departamentų direktorių lygyje. Tačiau mūsų Užsienio reikalų ministerija, kiek man žinoma, į tai visiškai neatsiliepė“.

Kiti žinomi Lietuvos politikai, kurie taip pat yra galimi kandidatai į prezidentus, tačiau nėra tokie įtakingi, kad galėtų tiesiogiai kritikuoti Dalios Grybauskaitės politiką, kol kas nesiryžta išsakyti komentarų jos adresu.

Lietuvos žurnalistai jau priekaištavo Kauno merui Visvaldui Matijošaičiui, kad jis stengiasi susilaikyti nuo kalbų užsienio politikos klausimais. Po to vienas iš populiariausių kandidatų į prezidentus labai švelniai pasisakė santykių su Rusija gerinimo klausimu.

„Šie santykiai — ne mano tema. Aš už tai, kad santykiai tarp šalių, ypač tarp kaimyninių, pasaulyje būtų geri; už tai, kad vienas kitam sakytų „labas rytas“. Aš už tai, kad jie gerėtų“, — pasakė Matijošaitis ir dėl visa ko pabėrė komplimentus Grybauskaitės adresu.

Suprantama, kodėl Kauno meras baiminasi. Jis neturi tokių resursų ir ryšių kaip Skvernelis, Ušackas ir Andriukaitis, kad galėtų tiesiogiai kritikuoti dirbančią prezidentę. Bet ir nenori rinkėjų akyse pasirodyti Grybauskaitei ištikimu politiku.

Dalia Grybauskaitė savo prezidentinio termino pabaigoje tapo „toksine politike“. Atsidūrę greta jos politikai rizikuoja pralaimėti rinkimus. Nes nepaisant aukštai vertinamų lietuvių simpatijų savo prezidentei, ką demonstruoja apklausos, į klausimą, ar norite dar 5–10 metų gyventi kaip prie Grybauskaitės esant aukštam emigracijos lygiui, augančioms kainoms, militarizavimui ir kilmingoms haliucinacijoms apie rusų tankus, dauguma lietuvių atsakys neigiamai.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 7 — id: `scraped:rubaltic_lt:9d488949a46743dc`

**Title:** Uspaskich: Lietuva gali tapti pasaulio centru, tačiau valdantieji to nemato

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Analitinis portalas RuBaltic.Ru tęsia interviu ciklą su Pabaltijo politikos veteranais. Žmonės, stovėję prie Latvijos, Lietuvos ir Estijos potarybinio kelio ištakų, sumuoja šių respublikų ketvirtadalio amžiaus politinio tranzito rezultatus: kokias valstybes tėvai įkūrėjai svajojo matyti ir kokių rezultatų pavyko pasiekti. Šios dienos pokalbio dalyvis šio ciklo rėmuose — Viktoras Uspaskich, Europos parlamentaras, Lietuvos verslininkas, politikas, Darbo partijos įkūrėjas.

Pirmą kartą Uspaskich atsidūrė Lietuvoje 1985 metais, atvykęs į šią Pabaltijo respubliką kloti dujotiekį Panevėžio rajone. Po Lietuvos išstojimo iš TSRS gavo Lietuvos respublikos pilietybę ir užsiėmė verslu. Įkūrė koncerną Vikonda, užsiiminėjusį maisto produktais. 2000 metais Viktoras Uspaskich pirmą kartą tapo Lietuvos Seimo nariu. 2003 metais įkūrė Darbo partiją ir tapo jos vadovu. 2004–2005 metais — Lietuvos ekonomikos ministras. 2009 metais Darbo partija delegavo jį į Europos parlamentą, 2014 metais jo įgaliojimai buvo pratęsti.

2015 metais pasitraukė iš Darbo partijos, 2017-aisiais sugrįžo į ją.

Apie tai, su kokiais iššūkiais susidūrė potarybinė Lietuva, kodėl jos politikoje tapo svarbi tautybė ir kuo gali didžiuotis šalis savo valstybingumo paskelbimo šimtmečio metais, analitiniam portalui RuBaltic.Ru papasakojo Viktoras Uspaskich.

— Pone Uspaskichai, su kokiais iššūkiais ir problemomis Lietuva susiduria šiandien?

— Svarbiausios ir pavojingiausios Lietuvos problemos šiandien — demografija ir emigracija. Tai nemokšiško valdymo ir nemokšiško ekonomikos vystymosi pasekmės.

— Kaip būtų galima tai ištaisyti? Lietuvos politikai pradeda kalbėti, jog reikia kurti nepriklausomybės aušros Sąjūdį primenančias naujas partijas, judėjimus, esą tai padėtų išspręsti problemas. Ką Jūs apie tai pasakytumėte?

— Naujų partijų, judėjimų, naujo Sąjūdžio sukūrimas niekuo nepadės. Būtina siūlyti ir daryti kažką konkretaus: turi būti rimta programa, galimybė ir noras ją įgyvendinti.

Žinoma, niekas nesako, kad nereikia vystyti aukštų technologijų. Tai — būtina. Tačiau aišku, kad mes nenugalėsime Amerikos Silikono slėnio. Kapitalo į jį investuojama maždaug milijonu procentų daugiau, negu sulaukiame mes. Mes privalome tai suvokti ir veikti racionaliai.

Siekiant tam tikruose rėmuose vystyti valstybės strategiją, būtina pasitelkti savo įstatymus, mokesčių reformą, modernizavimą. Būtina pasiekti, kad sąlygos Lietuvoje, ypač svarbiose strateginėse srityse, būtų geresnės nei kaimyninėse valstybėse. Tada investicijos bus nukreiptos link mūsų. Kito valstybės vystymosi ir išlaikymo varianto nėra. Gražbyliavimu žmonių nesugrąžinsi: jiems reikia gyventi, dirbti, rengtis, auginti vaikus. Todėl reikalingos gerai apmokamos darbo vietos.

Ar čia gali padėti naujos organizacijos, kuriose su savo idėjomis susiburs tie patys žmonės?!

— Be išorinės migracijos šalyje aukštas vidinės migracijos lygis. Sostinė išsunkia žmogiškąjį resursą iš mažų miestelių, kaimų...

— Na, taip. Būtinas naujas požiūris į regioninį vystymąsi, nes žmonės pagrindinai buriasi Kaune ir Vilniuje. Kad galėtų vystytis regionas, turi egzistuoti ir įstatyminė bazė.

Lietuvoje egzistuoja netikusi socialinė sistema. Socialinės pašalpos maždaug lygios minimaliam atlyginimui. Tad ar būtina žmonėms dirbti?! Kad žmonės norėtų dirbti, pašalpos neturėtų viršyti 40 proc. minimalaus atlyginimo. Akivaizdu, jog būtina didinti ir minimalų atlyginimą. Aš šiuo klausimu net kreipiausi į Europos Sąjungos komisiją. Minimalus atlyginimas šalies mastu turi būti ne mažesnis pusės vidutinio atlyginimo.

— Kad žmogus norėtų dirbti, turbūt, be materialinių gėrybių jam reikia ir kažkokių moralinių orientyrų, motyvacijos...

— Naujai kartai — taip. Maža jam pasakyti: „Tu turi pastatyti namą, užsidirbti pinigų“. Mes privalome aiškinti jaunimui, kam viso to reikia. Čia, be kita ko, kyla klausimai švietimo sistemai, kuri šiandien neatitinka dabarties pasaulio ir visuomenės poreikių. Dabar kitokie vaikai, kiti poreikiai, reikalingas kitoks požiūris. Šiandien nereikia mokyti vaikų, kaip iš punkto A pasiekti punktą B, šiandien reikia motyvuoti juos ten eiti.

Kad žmogus suvoktų savo atėjimo į šią žemę tikslą. Tada išsispręs daugelis problemų, tame tarpe ekonominės ir politinės.

Dar viena problema, kuri taip pat skatina emigraciją iš šalies, neteisinga Lietuvos užsienio politika. Aš manau, jog Lietuva provokuoja, net inicijuoja buferinės zonos savo teritorijoje sukūrimą tarp NATO ir Rusijos. Kodėl vykdomas toks pavojingas žaidimas, nesuprantama.

— Jūs pasisakote už tai, kad Lietuva taptų tiltu tarp Rytų ir Vakarų?

— Aš įsitikinęs, Lietuva egzistuoja tokioje geografinėje padėtyje, jog galėtų tapti pasaulio centru plačiąja šio žodžio prasme. Todėl, jog likimas jai lėmė būti tarp civilizacijų. Čia būtų galima susitikinėti ir aptarti taikias idėjas, o ne savo jėgomis badytis.

Geras pavyzdys — Lukašenka. Sugebėjo organizuoti susitikimą Minsko susitarimų klausimu, ir Baltarusija pateko į viso pasaulio ekranus. O juk kalba ėjo apie santykius tik dviejų anksčiau draugiškai sugyvenusių kaimyninių valstybių: Rusijos ir Ukrainos. Dabar įsivaizduokite, kad Rusija ir Amerika arba Rusija ir NATO Lietuvos teritorijoje atras kokius nors sąlyčio taškus. Tai būtų labai naudinga šaliai, tačiau tuo niekas nepasinaudoja. Todėl būtina keisti sistemą.

— Kaip Jūs manote, kodėl tuo niekas nepasinaudoja?

— Manau, jog pirmiausia čia pasireiškia politikų netoliaregiškumas.

— Pirmą kartą Lietuvoje Jūs atsidūrėte 1985 metais, paskui čia mokėtės, dirbote, 2003-iaisiais sukūrėte Darbo partiją. Kokiomis nuotaikomis ir viltimis tada gyveno Lietuvos žmonės?

— Kai buvo paskelbta nepriklausomybė, tauta pasijuto atgimusi, kunkuliavo patriotiškumas, ir tai buvo puiku. Bet valdžia pateko į diletantų rankas. Politikai nesugebėjo pasinaudoti esamais resursais. Po dešimties metų taip pat jautėsi teigiamas pagyvėjimas. Mes įstojome į ES, o tai davė mums daug naudos ir naujas galimybes. Bet čia vėl sušlubavo valdžią savo rankose laikantys žmonės.

— Bet juk ir Jūsų partija 2004-aisiais pateko į Seimą. Ir turėjo gana rimtą atstovybę...

— Mūsų partija tada negavo absoliučios daugumos. Mes turėjome 39 vietas iš 71 daugumos deputato. Viso parlamente 141 deputatas. Taigi mes neturėjome net trečdalio vietų. Todėl mes negalėjome patys formuoti vyriausybės, tačiau galėjome inicijuoti savo idėjas.

Tai, deja, čia nieko nedomina.

— Ir vis dėlto 39 vietos Seime partijai, kuri buvo įkurta tik prieš metus — rezultatas rimtas. Kuo galima paaiškinti tokią jaunos politinės jėgos sėkmę?

— Žinoma, viską nulemia patirtis. Mes įvėlėme kai kurių klaidų. Dabar, po tiek metų, suprantame, kad veikti reikėjo kitaip: ne žaisti kažkokiais ten įstatymų taisymais, o imtis darbo iš esmės. Kas dėl sėkmės rinkimuose, tai mes gana profesionaliai organizavome partinę struktūrą, ir tai patvirtino laikas. Daug buvo bandymų sudraskyti partiją, o ji laikosi ir dirba. Darbo partija ūgtelėjo, tapo protingesnė, ji pasiruošusi imti atsakomybę už šalį, tautą. Aš manau, jog partija turi ateitį.

— 2006 metais prasidėjo savotiška Jūsų medžioklė: Jus kaltino kyšininkavimu, ryšiais su Rusijos specialiosiomis tarnybomis. Buvo iškelta baudžiamoji byla. Galų gale 2016 metais Lietuvos Apeliacinis teismas Jus išteisino. Po visų šių bylinėjimųsi Jūs sakėte, jog pavargot ir neplanuojate grįžti politikon. Kas pasikeitė? Kodėl Jūs nutarėte grįžti ir vėl vadovauti partijai?

— Šiaip nelabai norėčiau tuo užsiimti. Aš turiu įdomesnių asmeninių užsiėmimų, reikalaujančių mano laiko ir dėmesio: verslas, asociacija „Už vieningą ir sveiką Europą“, psichologija. Man pasitraukus, partijai ėmė vadovauti žmonės, puolę ją apiplėšinėti, draskyti. Iš šalies stebint, darėsi gaila. Ir aš sugrįžau. Dabar šaliname tuos „tranzitininkus“, perbėgėlius ir naujomis jėgomis žengsime pirmyn.

— Kaip Jūs vertinate partijos galimybes?

— Vienareikšmiai — partija bus Seime. Mes dalyvausime visuose rinkimuose, ir aš esu tikras, jog vėl atvesiu Darbo partiją į Seimą. Dabar jame turime du atstovus, bet tai mažai. Mes turime aiškią pasiūlymų programą esančioms problemoms spręsti. Aš įsitikinęs, kad mes pajėgūs ne šiaip sau kalbėti, kas gerai, o kas blogai, bei ir imtis konkrečių veiksmų sprendžiant iškeltus uždavinius.

— 2015 metais savo interviu sakėte, kad iš politikos Jus stengiamasi išstumti dėl tautybės ir tiesmukiškumo. Tautybė lietuviškoje politikoje turi reikšmės?

— Žinoma, turi. Kai aš buvau stipriai taršomas, ką Jūs jau paminėjote, Ministrų kabineto nariai savo veiksmus derino su JAV ambasada Lietuvoje, o jos darbuotojai savo ruožtu konsultavosi su Vašingtonu. Visa tai paviešino Wikileaks, ir mano žodžius galima patikrinti. Neabejoju, mano tautybė čia atliko ne paskutinį vaidmenį. Jei yra stiprių žmonių, o dar ir kitos tautybės, į juos pradedama žiūrėti šališkai.

— Ar yra vilčių, kad šis požiūris kada nors Lietuvoje keisis?

— Artimiausiu metu — ne. Laikui bėgant, pasikeitus kartoms, rietenos tarp tautų nueis praeitin. Beje, net dabar jaunimas mažai dėmesio skiria tautybėms. Turi pasikeisti kelios kartos, kad tai nueitų praeitin. Yra reaktyvių jėgų, kurios toleruoja tokį nacionalistų nusiteikimą.

Neužmirškime, kad Lietuva neseniai įgijo nepriklausomybę. Pasakykime atvirai — nieko gero TSRS laikais Lietuvoje nebuvo. Dabar šalis šiek tiek vystosi. Aš ir pats vystausi, ko nebūčiau galėjęs Tarybų Sąjungoje.

— Jūsų manymu, kokiais pagrindiniais pasiekimais Lietuva gali didžiuotis valstybingumo paskelbimo šimtmečio metais?

— Dabar šalis turi tam tikrą kryptį, ji puikiai supranta, jog stovi ant nuosavų pamatų. Be to, tai, kad mes esame Europos Sąjungos nariai, — didžiulė vertybė, nes, be viso kito, tai dar ir didžiulė materialinė, struktūrinė, intelektualinė parama. Tai atveria beveik neribotas galimybes mūsų žmonėms ES teritorijoje. Pagerėjo šalies infrastruktūra. Lietuva tapo gražesnė.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 8 — id: `scraped:rubaltic_lt:6fc36dff929f6859`

**Title:** Grybauskaitė — KGB agentė: kaip „taršoma“ Lietuvos prezidentė

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos prezidentė Dalia Grybauskaitė pateko į sąrašą KGB agentų, prisipažinusių Liustravimo komisijai bendradarbiavus su tarybinėmis specialiosiomis tarnybomis. Informacija apie Grybauskaitę ir kitus agentus buvo užslaptinta, tačiau vyriausiasis laikraščio „Respublika“ redaktorius tvirtina, jog jam pavyko susipažinti su sąrašu atgailaujančių „bildukų“. Naujiena, jog „raudonoji Dalia“ bendradarbiavo su KGB , ne pirmoji Lietuvos prezidentę kompromituojanti informacija, pasirodžiusi pastaruoju metu. Baigiantis prezidentavimui, ponia Dalia tapo nuosekliai „taršoma“.

Laikraštis „Respublika“ išspausdino pirmąją dalį sąrašo asmenų, bendradarbiavusių su Lietuvos TSR KGB (VSK), — jame 1589 pavardės. 1990-ųjų metų pradžioje šie žmonės nuoširdžiai atgailavo Valstybinei Lietuvos liustravimo komisijai, jog turėjo ryšių su tarybiniais čekistais, tad sulaukė Komisijos garantijos, jog informacija apie jų, kaip skundikų, veiklą bus užslaptinta ir niekada nepasieks elektorato.

2015 m. Lietuvos Seimas priėmė nutarimą užslaptinti Liustracijos komisijos sąrašą 75 metams. Daugelis gandų teigia, jog tai buvo padaryta todėl, kad šiame sąraše apstu pavardžių Lietuvos Seimo narių, teisėjų, ministerijų, jėgos struktūrų darbuotojų ir (baisu pagalvoti!) net prezidentūroje įsikūrusių patriotų.

Ir štai dabar vyriausiasis redaktorius ir „Respublikos“ savininkas Vitas Tomkus tvirtina, jog jam pavyko pasiekti tą slaptą sąrašą, ir jis pasiruošęs pateikti Lietuvos visuomenei visus prisipažinusius bendradabiavus su tarybinėmis specialiosiomis struktūromis.

„Respublikos“ puslapiuose puikuojasi „tautos tėvas“ Vytautas Landsbergis ir jo tėvas Vytautas Landsbergis-Žemkalnis, buvęs prezidentas Valdas Adamkus, dabartinė prezidentė Dalia Grybauskaitė, buvę premjerai Andrius Kubilius ir Algirdas Butkevičius, dabartinis premjeras Saulius Skvernelis, buvę krašto apsaugos ministrai Rasa Juknevičienė ir Juozas Olekas, buvusi Seimo pirmininkė Irena Degutienė bei dar kai kurie ministrai ir deputatai.

Vitui Tomkui (kurio pavardė taip pat yra agentų sąraše) už šio sąrašo paviešinimą gresia baudžiamoji byla kaip pažeidusiam valstybinės paslapties straipsnį. Tačiau tuo atveju, jei Lietuvos valdžia iškels jam baudžamąją bylą, taps galutinai aišku, kad laikraštyje išspausdinta medžiaga atskleidžia tiesą ir kad Grybauskaitė, Landsbergis, Adamkus ir visi kiti išties bendradarbiavo su KGB.

O tokios informacijos patvirtinimo Lietuvos valstybingumas neištvers. Na, jei būtų egzistavęs vienas kitas „bildukas“ – būtų galima kentėti, bet situacija visiškai kita: pasirodo, visa Lietuvos valdančioji klasė, kuri koneveikia „sovietinę okupaciją“ ir ketvirtį amžiaus naikina komunizmo pėdsakus, tarybiniais metais veikė kaip „bildukai“. Nuo tokio žinojimo netoli ir iki revoliucijos, nes ji garantuoja įteisinimo krizę.

Todėl paprasčiau eiti kitu keliu: paskelbti, jog laikraščio „Respublika“ informacija – „geltono leidinio“ liguista fantazija ir jokio atgailavusių KGB agentų sąrašo jos leidėjas niekada nematė. Juolab, visa tai gali pasireikšti kaip tiesa: jokių dokumentinių įrodymų, kad laikraštyje paminėti žmonės – ne savavališkai paminėtų pavardžių ir vardų rinkinys, o Lietuvos valstybinės komisijos užslaptintas sąrašas, „Respublika“ nepateikia.

Bet net tuo atveju, jei Vito Tomkaus informacija bus pripažinta prieštaraujančia tiesai, vis tiek ji suvaidins informacinio smūgio Daliai Grybauskaitei vaidmenį.

Pirmiausia prezidentė atsidūrė nepatogioje padėtyje dėl ginčo su premjeru Saulium Skverneliu santykių su Rusija klausimu. Skvernelis pasisakė už politinio dialogo su Rusija atnaujinimą aukščiausiame lygyje ir pasiūlė reanimuoti Rusijos ir Lietuvos tarpvyriausybinės komisijos veiklą. Atsakydama, Grybauskaitė apkaltino vyriausybės vadovą neatsakingumu ir pareiškė, kad „su šia šalimi“ (t.y. su Rusija) negali būti jokių normalių santykių.

Tada informacinė BNS agentūra užsakė visuomenės apklausą santykių su Rusija klausimu. Ir absoliuti dauguma lietuvių palaikė Skvernelį jo konflikte su Grybauskaite. Sociologų duomenimis, 52 proc. Lietuvos piliečių pasisakė už Vilniaus ir Maskvos dialogo atkūrimą. Dar 22 proc. respondentų nebuvo apsisprendę.

Atsižvelgiant į tai, jog pastaraisiais metais Lietuvoje buvo isteriškai klykiama apie „rusų grėsmę“ ir „Kremliaus agentus“, reiškia, jog dauguma neapsisprendusių greičiausiai taip pat palaiko tarpvyriausybinės komisijos veiklos atkūrimą. Tai yra iki trijų ketvirtadalių lietuvių pasisako už santykių su Rusija normalizavimą.

Antrąjį smūgį sudavė buvęs URM vadovas Antanas Valionis. Jis išleido savo memuarų knygą „Politinės sūpuoklės“, kurioje papasakojo kaip Lietuva apgavo Latviją SGD terminalo klausimu.

Regioninis suskystintų gamtinių dujų terminalas turėjo būti pastatytas netoli Rygos, ir Lietuvos bei Latvijos vadovai sutarė, jog kartu stums šį projektą Europos komisijoje. Tačiau Lietuva apgavo Latviją ir pastatė savo SGD terminalą, galingumu viršijantį jos energijos poreikį. Buvo tikimasi, jog Latvija „prarys šią piliulę“, pradės pirkti iš Lietuvos suskystintas gamtines dujas, Briuselis suteiks šiam terminalui regioninį statusą ir į Vilnių ims plaukti jo išlaikymui skirti europietiški pinigai.

Tačiau taip neatsitiko. Pirkti lietuvių SGD Latvija su Estija atsisakė, terminalas Independence neįgavo regioninio statuso ir nesulaukė europietiškų pinigų, tad dabar Lietuvai tenka kloti iš savo biudžeto didžiules lėšas nuostolingo objekto išlaikymui, nesugalvojant, kaip juo atsikratyti.

O dar dalis Seimo deputatų ėmė maištauti prieš tolimesnį karinių išlaidų didinimą. Socialdemokratai paskelbė, jog 2 BVP procentų, skiriamų gynybai, visiškai pakanka šalies gynybinių pajėgumų išlaikymui. Įsipareigojimai NATO įvykdyti, formalių priežasčių nesuteikti Lietuvai pagalbos karinės agresijos atveju aljansas neturi, todėl vietoj tolimesnio karinių išlaidų didinimo geriau skirti lėšų socialinės atskirties ir nelygybės mažinimui.

Prieš keletą mėnesių nebuvo galima įsivaizduoti, jog viena iš sisteminių Lietuvos politinių jėgų išdrįs paprieštarauti ponios prezidentės „šventajai karvei“ – militarizavimui. Juk lėšų karinėms reikmėms negali būti skiriama per daug, o tas, kuris mano kitaip, – Kremliaus agentas! O dabar Lietuvos Seimo deputatai visiškai priartėjo prie tvirtinimo, kad gyventojų skurdo, nelygybės ir emigracijos iš šalies augimas tampriai siejasi su valstybės vadovės pozicija mesti visus resursus gynybinei politikai, spjaunant į socialinius klausimus.

Esant tokiai tendencijai netenka stebėtis, jog paviršiun iškilo amžinai žalia Dalios Grybauskaitės „griaučių spintos“ tema.

Apšaudomos skausmingiausios Grybauskaitės prezidentavimo pozicijos. Krizė santykiuose su Rusija, militarizavimas, SGD terminalas. Eilinis etapas — galimai ponios prezidentės atsakomybė už katastrofišką emigraciją ir Lietuvos tuštėjimą.

Lygiagrečiai su visu tuo vėl iškeliama „raudonosios Dalios“ tema. Apie agentės Magnolijos ryšį su KGB jau priminta, toliau „veikalo“ eigoje bus rikiuojamos tokios visada aktualios istorijos kaip Vilniaus TSKP mokykla, darbas TSRS ambasadoje Vašingtone 1991 metais, mokymasis Leningrado A.Ždanovo universitete bei Visuomeninių mokslų prie TSKP CK akademijoje ir taip toliau iki smulkmenų asmeniniame gyvenime.

Tapti savo didybėje figūra „bronzoje“ ir įeiti į Lietuvos istoriją iškilios valstybės veikėjos vaidmenyje D.Grybauskaitei nebus duota. „Šluba antis“ bus sutrypta dar iki jos prezidentavimo pabaigos.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 9 — id: `scraped:rubaltic_lt:ecb9742a0d64706b`

**Title:** Lietuvos ekonomikos vėliavnešys – chemijos koncernas Achema artėja prie agonijos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Pagrindinė Lietuvos įmonė, gaminanti chemines trąšas, Alchema pasiruošusi stabdyti gamybą. Vienas pagrindinių šalies mokesčių mokėtojų nepajėgia pakelti nuostolių naštos dėl nuo 2014 metų Lietuvos valdžios primestos politikos siekiant išlaikyti nerentabilų suskystintų gamtinių dujų terminalą Klaipėdoje.

Šios Lietuvos trąšų gamintojo problemos prasidėjo dar 2014 metais, kai šalies vadovybė priverstinai paskirstė stambiam verslui finansinius įpareigojimus išlaikyti nuostolingą SGD terminalą Indenpendent („Nepriklausomybė“). Politiniui projektui iš pat pradžių grėsė fiasko, tačiau tai nesutrukdė prezidentei Daliai Grybauskaitei ryšium su jo įvedimu 2014 metais rikiuotėn pareikšti, jog „pasiektas energetinis nuo Rusijos saugumas“.

O po to prasidėjo Lietuvos valdžių kančių keliai. Tuo metu, kai su norvegų kompanija Statoil buvo pasirašyta sutartis dėl SGD tiekimo Lietuvai, šalyje ženkliai smuko ekonomikos lygis, o tai privedė prie sumažėjusios dujų paklausos. Tačiau mokesčio už brangaus terminalo išlaikymą niekas neketino mažinti. Valdžiai tada beliko derėtis su Norvegija, kad būtų peržiūrėtos kontrakto sąlygos. Jas peržiūrėjus, Statoil užsitikrino dujų tiekimo garantiją ne penkeriems, o jau dešimčiai metų, Lietuvai įsipareigojant nusipirkti 3,7 milijardo kub. m. dujų (anksčiau — 2,7 mlj.). Naujasis kontraktas buvo susietas su rinkos kainomis.

Šia proga Norvegijos ES reikalų ir europietiškos ekonominės erdvės ministras Vidar Chelgesen nedviprasmiškai pareiškė Lietuvos valdžioms: „Norvegija neketina mažinti tiekiamų dujų kainų tuo atveju, jei rusų dujos bus pigesnės, nes mes prisilaikome nesikišimo į kainodarą principo“.

Nesėkmę Lietuva patyrė ir bandydama po savo sparnu sukurti regioninę dujų rinką, kas reiškė, jog kaimyninės Baltijos šalys — Latvija ir Estija — taip pat esą pirks dujas iš Klaipėdos terminalo. Rygoje ir Taline šis projektas buvo pripažintas ekonomiškai nenaudingu.

Ieškant išeičių, Vilniuje vienas po kito buvo gimdomi vis originalesni sprendimai. Vienu metu, matyt, dėl blaivaus mąstymo deficito arba nevilties buvo siūloma kloti dujotiekio vamzdžius į Klaipėdą iš Ukrainos. O dar Lietuvos valdininkai visiškai rimtai svarstė galimybę pasinaudoti Baltarusijos dujų tiekimo sistema tiekiant plaukiojančiojo terminalo dujas. O Lietuvos ekonomikos ministerijoje buvo ketinama iškelti šį klausimą aukštame lygyje — Lietuvos ir Baltarusijos tarpvalstybinėje komisijoje prekybos ir ekonomikos bendradabiavimo srityje. Nepasisekė.

Ir pagaliau kažkurio valdininko smegeninėje gimė geniali idėja: o priverskime savus verslininkus ir piliečius mokėti už „Nepriklausomybės“ išlaikymą. O juk kalbama apie nemažus pinigus: pagal sutartį su norvegų kompanija HoeghLNG už šią laivo paros nuomą reikia mokėti 189 tūkstančius JAV dolerių, o per 10 metų teks pakloti 689 milijonus. Kaip sakoma, pasakyta — padaryta.

Valstybė priėmė įstatymą „Dėl SGD terminalo“, įpareigojant stambiuosius dujų vartotojus trečdalį reikalingo dujų kiekio pirkti iš Klaipėdos „Nepriklausomybės“ tomis kainomis, kurias norvegai primetė dešimtmečiui į priekį. O Lietuvos Konstitucinis teismas savo ruožtu pripažino šiuos vyriausybės reikalavimus teisėtais.

Tokiu būdu Lietuvos valdžia prievartos būdu permetė šią finansinę naštą ant verslininkų ir savo piliečių pečių.

O tai ir paskatino Lietuvos dujų asociaciją (LDA) pateikti Europos komisijai skundą dėl vartotojų ir tiekėjų teisių suvaržymo. LDA manymu, įstatymas „Dėl SGD terminalo“, o taip pat kiti dokumentai jo realizavimo klausimu, prieštarauja ES įstatymams, kuriuose teigiama, jog „vartotojas turi teisę laisvai pasirinkti tiekėjus“. Ir dar: „tiekėjai turi teisę laisvai aprūpinti vartotojus“.

Kaip pabrėžė LDA ekspertai, vartotojams taikoma valstybinė prievarta pirkti per terminalą ne mažiau ketvirtadalio reikalingo dujų kiekio „apriboja rinkoje konkurenciją, tam tikras teises formuoja tik vienam dujų rinkos atstovui — SGD terminalo operatoriui“.

Po to, kai už šilumos tiekimą sostinei atsakanti kompanija „Vilniaus energija“ pradėjo pirkti „pačias brangiausias rinkoje norvegų dujas“, šildymas pabrango. Jeigu gyventojas dar sudurdavo galus, tai daugeliui Lietuvos verslo atstovų tokia našta faktiškai tapo nepakeliama.

Kaip paaiškino įmonės atstovė Gintarė Merkienė, nuo šių metų sausio teko ženkliai sumažinti gamybinius pajėgumus dėl „praktiškai visiškai Europai nereikalingų trąšų esant blogoms gamtinėms sąlygoms“.

Bet tai, kaip paaiškėjo iš Achemos atstovės parodymų, nėra pagrindinė problema. Galų gale būtų galima tęsti produkcijos gamybą, iki geresnių laikų laikant ją sandeliuose ir ieškant naujų realizavimo rinkų.

Beje, mokėti fiksuotą sumą tenka net tada, kai įmonei nereikalinga terminalo paslauga. Todėl šiandien gamykla dirba nuostolingai, o jos nuostoliai, atstovės žodžiais, „praktiškai tokie kaip ir išlaidos, kurios skiriamos SGD terminalo išlaikymui“.

O juk viską buvo galima daryti pagal kitokį scenarijų, jei ne Lietuvos lyderės Dalios Grybauskaitės įsikišimas į koncerno derybas su šveicarų choldingo EuroChem Group savininku Andrejumi Melničenka. Kaip parodė patirtis, parduoti privačią įmonę Lietuvoje, kuri yra ES narė, ne taip paprasta. O atskirais atvejais, jei tai prieštarauja šalies vadovybės logikai, visiškai neįmanoma. Taip ir atsitiko: valstybės vadovė pareikalavo, kad investorius atitiktų nacionalinio saugumo kriterijams ir būtų patvirtintas specialios komisijos“.

Dėl aiškių priežasčių, kai pirmasis šalies asmuo pastoviai kaltina Rusiją ruošiantis kariniam įsiveržimui, tos šalies investoriai automatiškai neatitinka iškeltam kriterijui. Tokia pozicija, švelniai tariant, stebina. Juk EuroChem Group valdo fosforo trąšų gamyklą Kėdainiuose...

Achemos atvejis ne vienintelis, yra ir kitų įmonių (jų liko nedaug), kurios susiduria su panašiais sunkumais. Lietuvos valdžia, stengdamasi įtikti geopolitikai, tebegriauna savo ekonomiką, priversdama verslą ieškoti prieglobsčio užsienyje.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 10 — id: `scraped:rubaltic_lt:c003a3c9b3906fab`

**Title:** Lietuva suveda sąskaitas su gyvenimu

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Nepriklausomybės metais Lietuvoje nusižudė 35 tūkstančiai žmonių. Lietuvos Respublika pastoviai pirmauja Europoje savižudybių skaičiumi, be to, pagal alkoholizmą muša pasaulio rekordus. Ir tuo pačiu metu Lietuvos valdžia nesiliauna šlovinus savo šalį kaip „europietiško pasirinkimo“ pavyzdį ir pavyzdį kitoms potarybinėms respublikoms, nekreipdama dėmesio į tai, kad jos šalis nenori gyvuoti ir užsiima fiziniu savęs likvidavimu.

Vilniaus universiteto tyrimų duomenimis, nuo 1990 iki 2016 metų Lietuvoje nusižudė 35 tūkstančiai žmonių. Kaip pabrėžia mokslininkai, vienai savižudybei tenka iki 20 nepasisekusių suicido atvejų.

Tai baisūs, fenomenalūs Europos ir pasaulio mastais skaičiai.

Pasaulinės sveikatos apsaugos organizacijos duomenimis, pagal savižudybių skaičių 100 tūkstančių gyventojų Lietuva užima pirmąją vietą Europoje ir aštuntąją pasaulyje. Šioje šalyje 100 tūkstančių gyventojų tenka 26,1 savižudybių. Pagal vyrų savižudybių skaičių (rodiklis 47,1) Lietuva atsiduria pasaulyje jau ketvirtoje vietoje.

Daugelyje Tropinės Afrikos, Centrinės Amerikos šalių ir kitose labiausiai skurstančiose vietovėse, kurias JAV prezidentas Donaldas Trampas neseniai pavadino „dvokiančiomis skylėmis“, tokių skaičių nėra.

Lietuvos politikai pastoviai bando aiškinti šiuos rodiklius taip, kad nediskredituotų šviesaus jaunos europietiškos demokratijos prie Baltijos jūros įvaizdžio, nes ši demokratija esą pravedė nuostabias reformas, tapo „Laisvojo pasaulio“ dalimi ir dabar „žaidžia vakarietiškuose klubuose“.

Žinoma, Lietuvos politikai viskuo kaltinti bandė „sovietinę okupaciją“, tačiau, susilaukę kandžių pašaipų, buvo priversti prikąsti liežuvį. Ir iš tiesų, kaipgi čia gali būti — „okupanto bato“ prispausti lietuviai kilpų sau nesinėrė ir Lietuvos gyventojų skaičius tarybiniais metais buvo rekordinis, o tapę laisvi ėmėsi susinaikinimo?

Lietuviškų savižudybių statistiką įtikinamiau nei politikai paaiškina kita statistika.

Tos pačios Pasaulinės sveikatos apsaugos organizacijos duomenimis, Lietuva labiausiai gerianti šalis. Jos pranešime sakoma, jog 2016 metais vienam Lietuvos gyventojui teko 16 išgerto alkoholio litrų. O šalies sveikatos apsaugos ministras Aurelijus Veryga prieš metus pareiškė, jog kas antras šalies gyventojas — alkoholikas.

Esant tokiems alkoholizmo ir savižudybių rodikliams, suprantama, kodėl iš Lietuvos skuodžia žmonės. Šalis kasmet atnaujina savo ir pasaulio gyventojų emigracijos rekordus. Praeitais metais Lietuva prarado 55 tūkstančius gyventojų, o per visą potarybinį laikotarpį — virš 700 tūkstančių. Na, o jei paskaičiuoti, kiek lietuvių nedeklaravo savo išvykimo, tas bendras skaičius pasiektų milijoną.

Gyventojų skaičius sumažėjo beveik trečdaliu ir tebemažėja. Depopuliacijos tempai — 2 proc. per metus. Nauja lietuvių karta nenori gyventi Lietuvoje: devyni iš dešimties jaunų žmonių nuo 15 iki 19 metų sako sociologams, jog atsiradus galimybei būtinai emigruos iš šalies.

Esant tokiems tempams, pagal Eurostato prognozes, 2080 metais Lietuvoje beliks 1650 tūkstančių gyventojų. 85 jų procentus sudarys virš 60 metų amžiaus žmonės. Čia teorija. O praktika rodo, kad šalis, kurios gyventojų daugumą sudaro nedarbingi senukai, negali egzistuoti. Ir todėl Lietuvos Respublika „užsidarys“ daug anksčiau.

Alkoholizmo, savižudybių ir psichinių nukrypimų rekordai, jaunimo bėgimas, karštligiškos isterijos apie „rusų grėsmę“, haliucinacijos su „žaliaisiais žmogeliukais“ Klaipėdoje ir prie Vilniaus — tai vis priešmirtinių kliedesių simptomai. Ir čia nėra nieko nuostabaus.

Ir todėl labai stebina, kai vadovybė šalies, kuri viso pasaulio akivaizdoje fiziškai žudosi, įkyriai raportuoja apie savo pasiekimus, moko kitas šalis, kaip reikia gyventi, ir Lietuvos „sėkmės istoriją“ parduoda kaip orientyrą ir nuorodą sekti jos pavyzdžiu. Iš čia ir skambūs pareiškimai likti „paskutiniąja Ukrainos viltimi“ Europoje, iki paskutiniųjų remti Kijevą. Iš čia ir „laisvos Rusijos forumai“ Vilniuje. Iš čia baltarusių nacionalistų apmokymai organizuoti „spalvotas revoliucijas“.

Taigi akivaizdi kažkokia klaiki scena. Savižudis guli šiltoje vonioje persipjovęs venas, iš jų bėga kraujas. Gęsta gyvybė, tačiau ir pusgyvis jis piršteliu vadina prie savęs aplinkinius ir moko juos gyventi. „Jūs gyvenate neteisingai, — sako sunkiai kvėpuojantis gyvas lavonas. — Jūs galite gyventi daug geriau.

Kaip aš“.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 11 — id: `scraped:rubaltic_lt:43ed7598c3527d0a`

**Title:** Dauguma lietuvių pasisako už santykių su Rusija gerinimą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Dauguma Lietuvos gyventojų palaiko santykių su Rusija gerinimą. Lietuviai pasisako už politinių kontaktų su kaimynine šalimi atkūrimą ir pritaria Lietuvos premjero iniciatyvai atkurti Rusijos — Lietuvos tarpvyriausybinės komisijos veiklą. Su tokia visuomenės nuomone neišvengiamai turės skaitytis kandidatai į Lietuvos prezidento postą, kurie kitų metų gegužę pretenduos į Dalios Grybauskaitės vietą.

Pasak kompanijos RAIT sociologinės apklausos, kuri buvo pravesta informacinės agentūros BNS užsakymu, 52 proc. Lietuvos gyventojų pasisako už santykių su Rusija gerinimą. Apklaustieji pasisakė už politinio Vilniaus dialogo su Maskva atkūrimą ir palaikė Lietuvos premjero Sauliaus Skvernelio pasiūlymą atkurti Rusijos – Lietuvos tarpvyriausybinės komisijos darbą.

Prieš premjero iniciatyvą pasisakė 26 proc. lietuvių. Politinio dialogo su Kremliumi klausimu nuomonės neturėjo 22 proc. apklaustųjų. Pastarasis skaičius įdomiausias. Bet kuris sociologas patvirtins, jog situacija, kai 22 proc. respondentų neturi nuomonės, yra nenormali ir liudija, jog visuomenėje tvyro didelė įtampa.

Negali būti, jog beveik ketvirtadalis Lietuvos piliečių nesugebėtų atsakyti į elementarų klausimą: ar jie palaiko santykių su Rusija gerinimą?

Ir tai nenuostabu, prisimenant, kas pastaraisiais metais dėjosi Lietuvos informacinėje erdvėje. „Maskvos rankos“ paieškos, „Kremliaus agentų“ išaiškinimas, iš pačių viršūnėlių sklindantis klyksmas apie „rusų grėsmę“, bet kuriam, pasisakančiam už gerus santykius su kaimynine Rusija, „vatniko“ etiketės klijavimas, nes jam, esą, „Kremliaus propaganda“ praplovė smegenis.

Po daugelio oficialios paranojos ir „raganų medžioklės“ metų žmonėms baisu gatvėse išgirsti, kad jie palaiko politinių santykių su Rusija atkūrimą. Todėl tuos 22 nuomonės neturtinčius procentus galima drąsiai pridėti prie minėtų 52 procentų, kurie pasisako už gerus santykius su Maskva.

Tokiu būdu, absoliuti lietuvių dauguma užima Lietuvos premjero Sauliaus Skvernelio poziciją ginče su prezidente Dalia Grybauskaite. Metų pradžioje Skvernelis pasiūlė atkurti Rusijos – Lietuvos tarpvyriausybinės komisijos darbą dėl prekybos – ekonomikos, mokslo – technikos, humanitarinio ir kultūrinio bendradarbiavimo. Premjero idėją iškart palaikė daugelis Lietuvos politikų, o štai Dalia Grybauskaitė pasisakė griežtai prieš, apkaltindama premjerą neatsakingumu.

„Būtų naivu manyti, jog su šia šalimi galimi nieko bendro su politika neturintys ekonominiai santykiai. Rusija visada panaudojo energetiką, prekybą ir kitus instrumentus kaip priemones politiškai spaudžiant ir įtakojant kitas šalis. Tai patvirtina mūsų patirtis“, — pasakė Lietuvos prezidentė, tuo smagiai nustebinusi visus, nes ji pati praėjusių metų pabaigoje pareiškė, jog su Rusija reikia bendradarbiauti, o ne kariauti.

Galimai Maskva Grybauskaitei po šios frazės nediplomatiškai pareiškė, jog su ja jokios kalbos nebus, nes jau netrukus ji vėl sugrįžo prie savo paistalų apie šalį agresorę, su kuria negali būti jokių dvišališkų kontaktų. Dabar gi Grybauskaitė atsidūrė nepavydėtinoje padėtyje.

Antirusišką Grybauskaitės poziciją remia mažuma. Tačiau iki jos atsisveikinimo su Lietuvos prezidento postu apie atsižvelgimą į lietuvių tautos norus ir santykių su Maskva gerinimą net kalbos negali būti. Ponia Dalia savo antrojo prezidentavimo metu tampa siaubo filmų „juodąja našle“, kuri su savimi į politinę smegduobę tempia visą Lietuvą. Tuo metu, kai visoje Rytų Europoje prasideda tarptautinio bendradarbiavimo atgimimas, Grybauskaitės vadovaujama Lietuva tebelieka apsuptyje atsidūrusia tvirtove, susiriejusia su visais kaimynais.

Ir todėl atsikratymas ponios Dalios politiniu palikimu taps viena svarbiausių 2019 metų prezidento rinkimų kampanijos temų ir pagrindiniu kito Lietuvos vadovo uždaviniu. Visi pretenduojantys į aukščiausią šalies postą politikai bus priversti vienaip ar kitaip skaitytis su nuomone Lietuvos visuomenės, kurioje vyrauja siekis normalizuoti santykius su Rusija.

Tiesa, niekas negali garantuoti, kad tas peržiūrėjimas bus sėkmingas. Kiek jau buvo Lietuvos bandymų normalizuoti santykius su Rusija, Lenkija ir Baltarusija? Brazauskas, Paksas, Butkevičiaus socialdemokratai. Kiekvieną kartą pergalę šventė politinės „Dėdulės“ Landsbergio tradicijos: „agresyvi kaimynystė“, „imperijos ambicijos“, „didžiarusiškas šovinizmas“, „lenkiškas šovinizmas“, „paskutinioji Europos diktatūra“, „nesaugios atominės elektrinės“ ir taip toliau iki begalės. Visi kaimynai blogi, tik Lietuva gera.

Ir todėl visi kandidatai į Lietuvos prezidentus būtinai žadės rinkėjams gerinti santykius su kaimynais, tame tarpe ir su Rusija. Naujasis Lietuvos prezidentas net gali pabandyti sąžiningai vykdyti šiuos pažadus. Tačiau didelio optimizmo šia tema nėra.

Būtent tautos siekis ir skatino kaskart politinę Lietuvos klasę gerinti šiuos kaimyninius santykius. Tačiau kadangi Lietuvos politinė klasė geriausiai įvaldė meną rietis, veltis į skandalus, ieškoti priešų ir griauti, tuo didžiuojantis („Tarybų Sąjungą sugriovėme mes!“), visi šie bandymai nedavė rezultatų ir viršų ėmė Vytauto Landsbergio linija.

Nėra jokių garantijų, kad taip neatsitiks ir po to, kai su Daukanto aikšte atsisveikins jo ištikima mokinė Dalia Grybauskaitė.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 12 — id: `scraped:rubaltic_lt:35b31d614b68121a`

**Title:** Pabaltijo šalys pasitinka savo šimtmetį išmirdamos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Pabaltijo šalys sutinka savo šimtmečio jubiliejų naujais depopuliacijos rekordais. Esant ekonominiam augimui ir politiniam stabilumui Lietuvos, Latvijos ir Estijos gyventojai vis sparčiau bėga į Vakarus, nenorėdami gyventi jiems sukurtose šalyse, atimdami iš šių šalių ateitį ir „daugindami iš nulio“ pačią Pabaltijo valstybingumo idėją.

Nuo 2017 metų sausio iki gruodžio iš Lietuvos emigravo 55 tūkstančiai žmonių. Tai absoliutus Lietuvos istorijos rekordas. Tuo metu, kai vyriausybė deklaruoja ekonominį augimą ir beria pareiškimus apie pragyvenimo lygio bei BVP vienam gyventojui augimą, iš šalies išvyko daugiau žmonių, nei po 2008–2009 metų krizės.

Su Latvija 2017 metais kasdien atsisveikino po 30 žmonių. Per metus šalis prarado virš 19 tūkstančių žmonių — apie 1 proc. gyventojų. Emigracijos iš Latvijos tempai kasmet auga: ir čia esant ekonominiam augimui ir politiniam stabilumui gyventojai bėga tokiu greičiu, lyg juos persekiotų krizė, badas ir karas.

Mažėjo ir Estijos gyventojų skaičius. Pagal demografų prognozes, po kelių dešimtmečių iš 1,3 milijono gyventojų joje liks mažiau milijono, be to, būtent estų skaičius mažės įvažiuojant ukrainiečiams, moldavams ir kitų rytų šalių darbo migrantams.

Tai, kas šiandien Pabaltijy dedasi, neturi precedento. Galima suprasti ukrainiečius, kurie bėga iš Ukrainos dėl pastovaus nestabilumo, nesibaigiančių „maidanų“ ir pilietinio karo. Buvo galima suprasti šimtus tūkstančių lietuvių, latvių ir estų, kurie bėgo 2008–2009 metų krizės metu praradę darbą.

Bet dabar Pabaltijo vyriausybės skambiai raportuoja apie sparčiausią Europos Sąjungoje BVP augimą, o politinė situacija Pabaltijy esą net geresnė, nei Vakarų Europoje. Vokietijoje — vyriausybės krizė, Ispanijoj — Katalonija, Britanijoj — Olsteris ir valstybinės sienos su Airija problema po „brexit“o. Šiame fone tylus ir stabilus Pabaltijis — žemė pažadėtoji.

Ir vis tiek pabaltijiečiai vis sparčiau neria į tas problemines šalis. Ketvirti metai iš eilės absoliuti gyventojų skaičiaus mažėjimo tarp Europos šalių čempionė ne Vokietija, ne Ispanija ir ne Anglija, o Lietuva.

Tikroji Pabaltijo katastrofa tame, kad jo gyventojai pradeda nekęsti ir kratosi valstybių, kurios buvo sukurtos dėl jų gerovės ir saugumo. Apie tai, kad Pabaltijo valstybės nuo pat pradžių buvo kuriamos neteisingai ir kad tikroji gyventojų nenoro jose gyventi priežastis glūdi fundamentaliame viso valstybingumo pastato nuosmukyje, šimtmečio jubiliejaus išvakarėse prabilo žinomiausi Lietuvos, Latvijos ir Estijos politikai bei ekspertai.

„Akivaizdu, jog iki šiol Lietuvoje nesukurta strategija, nėra struktūrinių pokyčių, kurie skatintų piliečius priimti pozityvią nuostatą ir perspektyvius sprendimus savo šalių atžvilgiu. Tam reikalinga aiški politinė valia, kurios pagrindas — konkretūs veiksmai, politinė atsakomybė“, — sako buvęs Europos Sąjungos ambasadorius Rusijoje, o šiuo metu Kauno technologijos universiteto Europos instituto direktorius Vygandas Ušackas.

„Lyginant su tais metais, kai buvo atkurta Lietuvos nepriklausomybė, vaikų gimsta trečdaliu mažiau. Iki šiol egzistavusios gimdymą skatinančios priemonės neveikia. O pagal emigracijos tūkstančiui gyventojų rodiklius Lietuva virš dešimt metų pirmauja Europos Sąjungoje“, — teigia Ušackas.

Apie tai kalba ir konsultacinės kompanijos Glade partneris lietuvių filosofas Mindaugas Kubilius: „Daugelis piliečių paprasčiausiai netiki, kad Lietuva — perspektyvi erdvė, kurioje jų gyvenimas gali gerėti“.

Jo žodžiais, gyventojų skaičius katastrofiškai mažėja dėl menkų pajamų ir aukštų kainų, socialinės atskirties ir negatyvios emocianalios visuomenės būklės, neaprūpintos senatvės ir žemo gimstamumo — lietuvių tauta nustojo atgaminti save.

„Visa tai nuosekliai veda žmones prie suvokimo, jog jie čia nereikalingi“, — daro išvadą Mindaugas Kubilius. „Ką daryti? Vienintelė išeitis — sugrąžinti piliečiams pasitikėjimą savimi ir savo valstybe“, — įsitikinęs filosofas. Tačiau ar ne per vėlu užsiimti tuo sugrąžinimu, jei 9 iš 10 jaunų lietuvių sako, jog išvyks iš šalies, jei jiems užsienyje bus pasiūlytas darbas pagal specialybę?

Tokiu paprastu ir natūraliu būdu galima atkeršyti politinei klasei ir už eurofondų draskymą, ir už „geopolitinius žaidimus“, ir už realios politikos pakaitalą — „rusų grėsmės“ paranoją: pasiruošti lagaminą, nusipirkti bilietą į lėktuvą ir palinkėti šaliai perspektyvos mirti kančiose.

Levas Tolstojus „Kare ir taikoje“ rašė, jog 1812 metais eiliniai rusų žmonės sparčiau visų armijų ir partizanų artino Napoleono žūtį tuo, jog, daug negalvodami apie Tėvynės likimą, pasiėmę reikalingiausius daiktelius, traukė į Rusijos gilumą, palikdami prancūzų kariuomenei išdegintą žemę.

Visiškai taip dabartiniai lietuviai, latviai ir estai artina Pabaltijo mirtį tuo, jog, daug negalvodami apie savo šalių egzistavimo esmę, važiuoja į aerouostą ir išskrenda gyventi Anglijoje. Londone jų laukia naujas gyvenimas, o jų šalis be jų — neišvengiama mirtis.

„Jei mes kalbame apie socialinį aspektą, tai didžiausias valstybės turtas — jos gyventojai. Šalį kuria jos gyventojai, o šalis formuoja gyventojų požiūrį į save. Jei gyventojai bėga iš savo valstybės, tai reiškia, jog šalis ligonė. Tai yra kažkas joje netvarkoj, jei atsirado neatitikimas — gyventojų poreikiai neatitinka jų lūkesčius. Jei pajėgiausi gyventojai atsisveikina su valstybe, vadinasi ji pamažu miršta tiesiogine šio žodžio prasme“, — mano Rygos techninio universiteto profesorius, latvių ekonomistas Janis Vanags.

„Jau dabar būtina spręsti gyventojų emigracijos problemą, nes perspektyvoje — darbo rankų stygius ir tautos senėjimas. Kyla klausimas dėl šalies ateities“, — sako Estijos finansų ministerijos Regioninio vystymosi departamento vadovas Prijdu Rustkok.

Įsidėmėtina, jog apie mirties pavojų Lietuvai, Latvijai ir Estijai šiose šalyse garsiai prabilta jų šimtmečio išvakarėse.

„Mes patys šią šalį tokią sukūrėme, — sako apie Latviją Janis Vanags. — Jei mums tai nepatinka, tada prieiname išvados, kad nemokame valdyti savo šalies. Nemokame sukurti tokios valstybės, kurioje patys norėtume gyventi“.

Panašios mintys tikrų Lietuvos, Latvijos ir Estijos patriotų, kurie dar nespėjo atsisveikinti su savo šalimis ir nėra abejingi jų ateičiai, nuskamba vis dažniau ir dažniau.

Bet ar pakaks tam ryžto ir jėgų? Juk daug paprasčiau kalbėti apie „sėkmės istoriją“, „pabaltijietiškus žaidimus“ ir sparčiausią Europos Sąjungoje ekonomikos augimą.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 13 — id: `scraped:rubaltic_lt:1c2f80a3e919e53f`

**Title:** Tiesa apie sausio 13-osios įvykius nuvarys Lietuvos valdžią į teismą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Tiesa apie Vilniaus televizijos bokšto šturmą 1991 metų sausio 13 dieną gali sugriauti visą nepriklausomos Lietuvos idėjinį pamatą. Dabartinė Lietuvos valdžia akylai stebi, kad visuomenė neabejotų kalte tarybinių kariškių, kurie esą sušaudė nepriklausomybės šalininkus. Apie tai, jog nesiduria „sausio 13-osios bylos“ galai, analitiniam portalui RuBaltic.Ru papasakojo buvęs Lietuvos Aukščiausiosios Tarybos deputatas, antrasis LKP CK (TSKP platformoje) sekretorius Vladislavas Švedas:

— Praeitame interviu Jūs papasakojote apie tai, kaip buvo einama link kruvinų įvykių prie Vilniaus televizijos bokšto. O kas gi atsitiko Vilniuje 1991 metų sausio 13-ąją?

— Situaciją įkaitino sąmoningas Vytauto Landsbergio pritarimas kelis kartus pakelti maisto produktų kainas, kuris buvo perduotas premjerei Kazimirai Prunskienei. Priešais Aukščiausiąją Tarybą buvo parduotuvė „Talinas“, iš jos išėję žmonės piktinosi kainų pakėlimu, organizavo nedidelį mitingą. Nepasitenkinimas ritosi per Vilnių kaip gaisras. Sausio 8-osios rytą Kuro aparatūros gamyklos Sąjūdžio grupė pradėjo mitingą prieš kainų pakėlimą.

Po to, kai buvo pakeltos kainos, prasidėjo informacinė kampanija. Žiniasklaida triūbino, kad tai „Maskvos ranka“ primetė visus išbandymus ir nori nužudyti šalį. Iškilo būtinybė kokiu nors būdu neutralizuoti televiziją. Spaudos rūmai, kuriuos kontroliavo desantininkai, buvo pastatyti TSKP CK lėšomis, bet juos 1990 metų kovą užgrobė „sąjūdiečiai“ ir neleido juose spausdintis opozicijai. Jie spausdino tik savus laikraščius, kupinus antitarybinės retorikos. Tie laikraščiai, kurie rėmė Tarybų Sąjungą, buvo spausdinami Minske.

Deja, jėgos akcija Vilniuje vyko pagal keistą scenarijų, ir ji iš anksto buvo pasmerkta nesėkmei. Sakykim, buvo galimybė nutraukti elektros energijos tiekimą televizijai. Tačiau specialaus dalinio „Alfa“ kariams teko šturmuoti televizijos bokštą. Ir jis buvo užimtas be šūvių — apie tai Landsbergis pranešė 1991 metų sausio 16 dieną Aukščiausiosios Tarybos posėdyje. Tačiau jau kitą dieną tas pats Landsbergis tvirtino, kad „Alfos“ kariai — specialiai paruošti žudikai, susitepę rankas lietuvių krauju.

Įdomi informacija: praėjus penkioms minutėms po to, kai „Alfa“ užėmė Vilniaus televizijos bokštą, du bokštai prie Kauno su galinga radijo ir televizijos aparatūra ėmė transliuoti laidas Lietuvai. Jie kažkodėl nebuvo užimti. Įsivaizduojate, KGB profesionalai, kurie visada puikiai atlikdavo užduotis, o tai pripažindavo net JAV: užėmė Kabule Amino rūmus, surengė spec. operaciją Čekoslovakijoje, čia kažkodėl sugavo žioplį.

Keletas žodžių apie Vilniaus televizijos bokštą. Užimti jį buvo nutarta šturmuojant. O Landsbergis jau buvo pasiruošęs: buvo pastatytos barikados, atgabenta ir prie Aukščiausiosios Tarybos bei televizijos bokšto sutelkta statybinė technika. Tapo aišku, kad užimti objektus nebus lengva. Norint prasiskverbti pro visas šias užtvaras, reikėjo pasitelkti tankus. Aš kalbėjausi su karininkais, jie sakė, kad prie tankų rankenų sėdėjo tik karininkai.

Tokiu būdu tankai pasiekė televizijos bokštą, ten jie išblaškė užtvarus, tačiau penkiatūkstantinė minia neišsisklaidė. Audrius Butkevičius, tuometinis Krašto apsaugos departamento vadovas, rėkė, kad kareivių šoviniai tušti. Tankai iš tiesų šaudė tuščiais, jų sviediniai buvo užkimšti duonos kepaliukais, kad neišsiveržtų liepsnos ir degančios dujos. Ir desantininkų automatų šoviniai buvo tušti.

— Ir vis dėlto egzistuoja duomenys apie žuvusius, teismo medicinos ekspertų išvados, nukentėjusiųjų parodymai. Su objektyvia informacija sunku ginčytis!

— Dabar Lietuvos prokurorai tvirtina, kad buvo keturiolika lavonų, tarp jų tarybinis karininkas, ir 500 nukentėjusių. Keturi žuvę — esą sutraiškyti tankų, devyni nukauti šaunamaisiais ginklais.

Lietuvos teismo medicinos ekspertai nustatė, kad į daugumos žuvusiųjų kūnus kulkos smigo iš viršaus 40–60 laipsnių kampu. Vienas iš jų buvo nukautas 1908 metų tipo kulka, paleista iš 1891/1930 metų Mosino tipo šautuvo. Bet juk desantininkai nebuvo niekur įkopę, jie stovėjo prieš minią. Iš kur tada šūviai?

Priminsiu, kai tankų ir šarvuočių kolona dar tik slinko link televizijos bokšto, o iš Aukščiausiosios Tarybos pastato langų kunigas Algimantas Keina — artimas Landsbergio draugas laikė mišias už žuvusius nuo tarybinės armijos karių rankų. Jis rėkė, kad jau yra „sovietų aukų“. O tai vyko prieš pusvalandį iki technikos ir desantininkų atvykimo prie bokšto.

Iš keturių aukų, kurias esą sutraiškė 41 tonos svorio tankai, pagrindine laikoma Loreta Asanavičiūtė. Dokumentinėje medžiagoje nurodoma, jog tankas, kurio vikšro plotis 58 centimetrai, pervažiavo jai dubenį ir šlaunis. Žinoma, jog tokiu atveju žmogaus kūnas tampa panašus į popieriaus lapą. Vaizdo filme, pagamintame po Asanavičiūtės mirties, matosi, kad kūnas buvo anatomiškai sveikas.

Kai Loretą atvežė į ligoninę, ji dar buvo gyva, sąmonėje ir rišliai atsakinėjo į medicinos personalo klausimus. Tai užfiksuota režisieriaus Broniaus Talačkos vaizdo filme, kurį 1995 metais parodė Lietuvos televizija. O 1994 metų kovą jis buvo demonstruojamas Lietuvos respublikos Aukščiausiojo teismo posėdyje ir prijungtas prie baudžiamosios bylos medžiagos (taip vadinamoji „Vienybės“ byla).

Išaiškėjo, jog Asanavičiūtė nebuvo patekusi po tanku. Ji buvo išstumta iš minios link artėjančio bronetransporterio, kuris prispaudė ją prie tvoros iš vielų tinklo ir kuris toje vietoje buvo praplėštas. Aštrūs vielos galai smigo į dešinę merginos šlaunį, bet tai nebuvo mirtinos žaizdos. Ir vis dėlto po kelių valandų Asanavičiūtė staiga mirė.

L.Tručiliauskaitė ir A.Pladytė teisme sakė, kad jos parvirto ir ant jų kojų užvažiavo tankas. „Tankas pastovėjo, paskui pradėjo suktis. Kojos vis dar buvo po vikšrais“. Įsivaizduojate, kas būtų nutikę kojoms ir pačioms merginoms, jei tikrai ant jų kojų būtų užvažiavęs tankas. Tručiliauskaitė gi 1997 metais į teismo posėdį, kuriame buvo svarstoma byla Valerijaus Ivanovo, esą apšmeižusio sausio 13-osios aukas, atėjo net be lazdelės.

— Tai, ką Jūs pasakojate, sunku įsivaizduoti, be to, Lietuva pateikia teismo medicinos ekspertų patvirtinimus. Kaip priešpastatyti tikruosius faktus?

— O to medicinos ekspertizės akto, kurį 1991 metų vasario 26 dieną pasirašė vyriausiasis Lietuvos teismo medicinos ekspertas Antanas Garmus, tarp tų medžiagų, kurios yra baudžiamojoje sausio 13-osios byloje, nėra. Dingo. O byla tebenagrinėjama Vilniaus apygardos teisme.

Dabar egzistuoja visiškai kiti teismo medicinos ekspertų aktai. Kyla klausimas: ką visa tai reiškia? Tas aktas, kurį pasirašė Garmus, 20 metų buvo laikomas pagrindiniu oficialiu dokumentu, patvirtinančiu sausio aukų žūties priežastis, o dabar tvirtinama, jog negali būti kalbos apie kažkokio ten akto dingimą — jo išvis nebuvo.

Verta priminti tokį faktą. Kai vienas iš sausio 13-osios įvykių organizatorių, jau minėtas Audrius Butkevičius pabandė šiauštis prieš Landsbergį, jam tuoj pat buvo sukurpta kyšio byla ir vyras atsidūrė už grotų. Išėjęs laisvėn pasakė, jog Lietuvos teisėtvarka yra politinė mašina, vykdanti nurodymus iš viršaus.

— Kodėl iki šiol Landsbergis kontroliuoja Lietuvos politiką, kodėl niekas nesikeičia: tokia situacija visus tenkina ar jis turi labai stiprų užnugarį?

— Zigmas Vaišvila, buvęs aršus antitarybininkas, neseniai pareiškė, jog negalima taikstytis su Landsbergio ir dabartinės Lietuvos prezidentės Dalios Grybauskaitės režimu. 2018 metų sausio 3 dieną jis, Lietuvos nepriklausomybės akto signataras, vėliau vicepremjeras ir Valstybės saugumo departamento vadovas, t.y. gerai informuotas žmogus, Seimo rūmuose organizavo spaudos konferenciją. Joje Vaišvila papasakojo apie nusikalstamą veiklą grupės buvusio Lietuvos Aukščiausiosios Tarybos pirmininko Landsbergio, kurį jis pavadino „provokacijų meistru“. Ir būtent todėl provokacijų specialistas Landsbergis iki šiol valdo Lietuvą.

Vaišvila ypač akcentavo išvadas Lietuvos Seimo komisijos, kuri 2006 metais tyrė Lietuvos saugumo darbuotojo Juro Abromavičiaus  žūties aplinkybes — jis buvo susprogdintas savo mašinoje 1997 metų sausio 31 dieną. Vyriškis užsiiminėjo tyrimu nusikaltimų, kuriuose matėsi Landsbergio ir jo aplinkos pėdsakai.

Komisija, kurios išvadoms 2007 metų sausy pritarė Lietuvos respublikos Seimas, padarė savo išvadą: „J. Abromavičiaus nužudymą reikia vertinti kaip nusikaltimą, kurį įvykdė grupė žmonių ir organizacijos, turinčios terorizmo požymių ir kurias siejo ir tebesieja ryšiai su tuometine ir dabartine „Tėvynės sąjungos“ (Lietuvos konservatoriai), Krikščionių demokratų ir buvusios Lietuvos demokratų partijų vadovybėmis“.

Ypatingai pažymėsiu, jog Lietuvoje visi viską žino vienas apie kitą, bet visi tyli. Landsbergis 20 metų buvo KGB agentas. Žurnalistas ir televizijos vedantysis Algimantas Čekuolis vedė laidas, o žmonės jį vadino Algimantu Čekistu. Seimo deputatas Petras Gražulis neseniai užregistravo rezoliuciją, reikalaujančią Vytauto Landsbergio ir konservatorių psichikos patikrinimo.

Pavyzdžiui, Dalia Grybauskaitė bus teisiama kaip ir Saakašvilis. Jos nusikaltimų sąskaitoje „Snoro“ banko bankrotas, o tiksliau — išvogimas, dujų afera, kurios pasekoje žmonės už dujas moka daugiau, o pinigai plaukia į sukčių kišenes, Kauno pedofilų bylos marinimas. Šį sąrašą būtų galima lengvai pratęsti. Ir kitiems valdžioje tupintiems nusimato panašus likimas, kiekvienam gali būti pateiktas jo nusikaltimų sąrašas. Ne paslaptis, jog tas susidūrimas sausio 13-osios naktį vyko dėl TSKP CK nuosavybės. O kur ji dabar? Tik televizijos bokštas, kuris buvo pastatytas tarybiniais pinigais, liko. Viskas kitkas ne Lietuvos, o Landsbergio su jo aplinka rankose.

— Jeigu lietuviai žino tiesą, kodėl tyli?

— Žinoma, problema dar ir tame, kad Lietuvoje neliko protestuojančio elektorato. Nors kai kada pakanka 3–4 proc. nepatenkintų, kad būtų sukelta visuomenė. Be to, politikai pastoviai velia klaidas. Beje, Lietuva, pasitraukdama iš Tarybų Sąjungos sudėties, atkūrė 1938 metų Konstituciją, tad žvelgiant per teisinę prizmę Vilnių ir Klaipėdą turėtų prarasti.

Klaipėdos kraštas buvo prijungtas be jokių dokumentų. Vilniaus kraštas perduotas pagal 1939 metų TSRS ir Lietuvos sutartį, tačiau vėliau paaiškėjo, jog ją pasirašė neįgalioti asmenys, ir todėl lenkai gali skelbti, jog Vilno — jų miestas.

— Jau ketvirti metai Lietuvos kalėjime laikomas Jurijus Melis, nors pagal Europos Sąjungos normas žmogus negali būti už grotų ilgiau trejų metų, jei jis nenuteistas. Kodėl tyli Europos Sąjunga, juk procesas neabejotinai politinis?

— Aš esu Rusijos Federacijos 3-iosios klasės tikrasis valstybės patarėjas, tai lygu generolo majoro laipsniui. Taigi turiu nemažai įtakingų pažįstamų. Ir aš nesugebėjau pasiekti, kad Rusijos teismo medicinos ekspertai arba bent jau karo traumotologai paruoštų pažymą, kas nutinka po tanku patekusiam žmogui. Belieka apgailestauti, kad absurdu dvelkiančios sausio įvykių aukų traumų formuluotės, esančios sausio 13-osios įvykių baudžiamosios bylos Kaltinamajame akte, kol kas nedomina nei Tardymo komiteto, nei Rusijos Federacijos Generalinės prokuratūros.

Rusijoje kalbama, jog kai Vilniuje bus paskelbtas nuosprendis 58 Rusijos piliečiams, tada ir bus  protestuojama. Tačiau įsivaizduokite — 709 tomai baudžiamosios bylos, tame tarpe 13 Kaltinamojo akto tomų. Viso 60 tūkstančių lapų, kas imsis juos peržiūrėti, tikrinti protokolus, iš naujo nagrinėti?

— Ar yra senaties terminas televizijos bokšto šturmo sausio 13-ąją mitui?

— Negalima užbaigti to, kam nėra atkirčio, Rusija turi įsikišti. O lietuviai turi suprasti, kad neegzistuoja rusų grėsmės. Viena, kas reikalinga Rusijai, kad Lietuva netrukdytų susisiekti su Kaliningradu.

Žinoma, Rusijai, 2003 metais pasirašant su Lietuva sutartį dėl sienų, gal ir reikėjo kažkokiu būdu paliesti klausimą dėl teritorijų, kurias ji gavo iš TSRS, pareikalaujant garantijų, jog nebus trukdoma susisiekti su Kaliningrado sritimi. Priminsiu — Lietuva pasirašė su Rusija sutartį dėl sienų, o paskui pradėjo kelti teritorines pretenzijas Kaliningrado srities atžvilgiu ir grąsinti, jog esant būtinybei nutrauks Rusijos susisiekimą su Kaliningradu geležinkeliu.

Taip kalbėta prieš pasirašant sutartį dėl sienų. Taip buvo ir 1990 metų biržely, siekiant priversti Michailą Gorbačiovą grąžinti pramoninį naftos ir dujų tiekimą Lietuvai. Apie tai Landsbergis savo knygoje „Lūžis prie Baltijos“ su pasitenkinimu parašė, kaip jis „apgavo Gorbačiovą ir bukagalvius oponentus“. Landsbergis pabrėžė, jog „karo mene svarbu, kas kam primes savo elgseną. Mes nenuolaidžiavome, nepasidavėm svetimam stiliui“. Tai gal pakas žaisti su Lietuva pakištynėmis, dar ir pagal jų taisykles?

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 14 — id: `scraped:rubaltic_lt:6461e193cd338f20`

**Title:** Landsbergis sausio 13-ąją siekė kraujo, kuris jam leistų tapti tautos didvyriu

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Kruvinieji 1991 metų sausio 13-osios įvykiai prie Vilniaus televizijos bokšto tapo vienu iš valstybės sukūrimo mitų. Dabartinė Lietuvos valdžia atidžiai seka, kad visuomenė neabejotų, jog kalti tik tarybiniai kariškiai, kurie esą nužudė nepriklausomybės šalininkus. Tačiau tų įvykių liudininkų parodymai atskleidžia tikrąjį jų vaizdą ir įrodo, jog prieš 26 metus sukurta ir iki šiol akylai saugojama versija yra melas. Apie tai, kas ir kodėl suplanavo kruviną sausio 13-osios akciją, analitiniam portalui RuBaltic.Ru papasakojo buvęs Lietuvos Aukščiausiosios Tarybos deputatas ir antrasis LKP CK (TSKP platformoje) sekretorius Vladislavas Švedas:

— 1990 metų kovo 11-osios naktį Lietuvos TSR Aukščiausioji Taryba, kuriai vadovavo Vytautas Landsbergis, paskelbė Lietuvos nepriklausomybę, tačiau daugiau kaip metus jos nepripažino pasaulio bendrija. Bet ir po tragiškų sausio 13-osios įvykių pasaulio lyderiai tylėjo. Ką visa tai reiškė?

— Nepriklausomybės paskelbimas — gana reikšmingas aktas, bet jis tik visiškos valstybės nepriklausomybės preliudija. Siekdama būti išties nepriklausoma, valstybė privalo: kontroliuoti visą savo teritoriją, sienas, turėti nuosavą, pasaulio pripažintą valiutą, karines pajėgas, sugebančias apginti nepriklausomybę, atstovavimą tarptautinėse organizacijose ir t.t. Antai Katalonija paskelbė nepriklausomybę, kaip ir Lietuva 1990 metais. Ir ką? Pareiškimas, jog atkuriama nepriklausomybė, respublikoje nebuvo paremtas realia situacija.

Be to, būtina, kad nepriklausomybės paskelbimas neprieštarautų teisės normoms. Norint priimti sprendimą dėl nepriklausomybės atkūrimo, už jį pagal tarybinius įstatymus turėjo pasisakyti ne mažiau 2/3 Lietuvos piliečių. Jei nebuvo norėta vadovautis TSRS įstatymais, bent jau reikėjo prisilaikyti tų demokratinių normų, kurias pripažįsta pasaulis. Jos reikalauja, kad priimant pagrįstą sprendimą valstybės likimo klausimu būtina turėti ne mažiau 50 proc. bendro rinkėjų skaičiaus balsų plius vienas balsas.

Lietuvoje iš 130 Aukščiausiosios Tarybos deputatų, išrinktų 1990 metų kovo 11-ąją, 123 deputatai pasisakė už Nepriklausomybės aktą, prieš balsų nebuvo, šeši lenkų deputatai susilaikė, vienas biuletenis buvo pripažintas negaliojančiu. Pažymėsiu, jog tiems 123 deputatams savo balsus atidavė tik 37,9 proc. Lietuvos rinkėjų.

Tačiau tada į tai niekas nekreipė dėmesio. Pasaulio bendriją labiau jaudino ultimatumo forma Lietuvos Aukščiausioje Taryboje paskelbta respublikos nepriklausomybė. Po to sekė ultimatumo forma vedamas naujos Lietuvos vadovybės dialogas su Maskva: prie derybų stalo sėsime tik su sąlyga, jei jūs pripažinsite mus nepriklausomais. Dėl to teko sunerimti Vakarams. Juk TSRS buvo galinga pasaulio valstybė ir su ja reikėjo skaitytis.

— Kodėl Lietuvai taip reikėjo nepriklausomybės, juk ji Vakarų akyse egzistavo kaip tarybinio socializmo vitrina ir jos žmonės neblogai gyveno?

— Priminsiu, jog Lietuva po karo 1944–1953 metais užėmė antrą pagal pasipriešinimo tarybų valdžiai mastus vietą. Pirmoje buvo benderininkų pasipriešinimas Ukrainoje. Lietuvoje antitarybiniame partizaniniame judėjime dalyvavo apie 30 tūkstančių žmonių, o tai tokioje mažoje šalyje gana daug.

Pasipriešinimas atsirado todėl, jog 1940 metais, kai Lietuva įstojo į TSRS, naujoji valdžia savo pozicijose įsitvirtino nepaisydama kitokių nuomonių, neatsižvelgdama į šios respublikos specifiką. 1941 metų pavasarį atsirado rimtų problemų aprūpinant gyventojus maisto produktais ir labiausiai reikalingomis prekėmis. Tai sukėlė daugelio gyventojų nepasitenkinimą. Todėl 1944 metais nemažai žmonių išėjo į miškus. Partizaninis judėjimas 1953 metais iš esmės buvo įveiktas, tačiau Maskva Lietuvą laikė problemine respublika, todėl ir elgėsi jos atžvilgiu savaip.

Mano mama kilusi iš Voronežo srities. Ten žemė — 1,5 metro juodžemio. Pavasarį įsmeik į žemę lazdą, o rudenį, jei nebuvo sausros, sulauksi derliaus. O parduotuvėse aš ten nemačiau nei pieno, nei mėsos, nei sviesto. Tai buvo pagrindinė priežastis, kad net buitiniame lygyje Rusijos gyventojai murmėjo: taukuose vartaliojasi pabaltijiečiai.

Kai 1990 metais patekau į TSKP CK, supratau, jog tokios nuotaikos buvo būdingos ir kai kuriems CK aparato darbuotojams. Jie manė, kad Pabaltijui per daug duodama ir jį reikia „nuimti nuo Rusijos sprando“. Iš esmės tai buvo teisinga: Rusija daug ką atiduodavo Pabaltijui nominaliomis kainomis. Gorbačiovas šias nuotaikas gerai žinojo. Konfidencialiai susitikęs su Reiganu 1986 metais, jis sutiko paleisti Pabaltijį iš Tarybų Sąjungos.

— Kame, Jūsų manymu, sausio 13-osios akcijos šaknys?

— Gorbačiovas manė, jog Pabaltijis iš Sąjungos pasitrauks ramiai ir nebus protestuojančių. Bet išėjo kitaip. Skilus Lietuvos Kompartijai, paaiškėjo, kad dauguma rusakalbių gyventojų, prisimindami, kaip Lietuvos nacionalistai 1941 metais žudė žydus ir rusus, nelabai norėjo nepriklausomybės.

Rusakalbiams Lietuvos gyventojams baimę kėlė tai, jog nuo 1989 metų sąjūdiečiai ėmė skelbti žydšaudžius didvyriais ir kovotojais už nepriklausomybę. Bet ir lietuviai ne visi siekė neaiškios nepriklausomybės. Kad nekalbėčiau nekonkrečiai, priminsiu lietuvių pulkininką Joną Gečą, kuris 1991 metų sausį vadovavo Aukščiausiosios Tarybos gynybai.

Duodamas interviu Delfi.lt kanalui, jis pranešė: „Gal pusė milijono ir laikėsi Lietuvoje už rankų (t. y. 1991 metų sausy tvirtai rėmė nepriklausomybę — V.Švedo pastaba), tačiau apie pusantro milijono lūkuriavo, stebėdami, kuo visa tai baigsis. Ir dar pusantro milijono gal ir nebuvo kategoriškai nusiteikę prieš, bet vis dėlto prieš. Taip buvo realiai vertinama Lietuvos situacija net praėjus 9,5 mėnesio po nepriklausomybės paskelbimo.

Daugelį Lietuvoje gąsdino nekompetetinga naujosios respublikos vadovybės socialinė ir ekonominė politika. Eilinio žmogaus gyvenimas kas mėnesį blogėjo. Be to, 1990 metų kovą patekę valdžion vyrukai pradėjo sparčiai turtėti. Pats Landsbergis, tapęs Sąjūdžio vadovu, pasikeitė butą, gavo importinius baldus, mašiną, o žmonės tuomet ilgus metus stovėjo eilėse, norėdami tai gauti. Visa tai kėlė pasipiktinimą.

1990 metų spaly buvo sukurtas Lietuvos ateities forumas (LAF), tapęs Landsbergio Sąjūdžiui visuomenine politine alternatyva. Ir tada nepasitenkinimas „landsbergininkų“ politika ėmė augti.

1991 metų pradžioje nepasitenkinimas Lietuvos Aukščiausiosios Tarybos politika tapo respublikoje masišku. Vis ryžtingiau buvo keliamas klausimas, jog būtina organizuoti naujo Seimo rinkimus. Valdžia slydo iš Landsbergio ir jo aplinkos rankų.

Tokio nusikalstamo sumanymo akto egzistavimą 2014 metais patvirtino Aloyzas Sakalas — buvęs aktyvus „sąjūdietis“ ir 1990–1992 metais Lietuvos Aukščiausiosios Tarybos Prezidiumo narys. Interviu Delfi.lt portalui jis pareiškė: „Negi kas iš mūsų galėjo pagalvoti, jog Visagalis Prezidiumo posėdyje 1990 metais kalbės savo ištikimo tarno Aleksandro Abišalos lūpomis. Jis pasakė, jog Nepriklausomybės nebus, kol nebus pralietas kraujas. Šie pranašystės žodžiai pasitvirtino po 1991 metų sausio 13-osios“.

— Kodėl „sąjūdiečiai“ nenorėjo taikiai spręsti klausimo?

— O kokiu būdu Landsbergis ir jo komanda galėjo susigrąžinti prarastą respublikoje autoritetą? Valdyti respublikos jie nemokėjo. Beje, priminsiu, jog Landsbergio Lietuvos Aukščiausioji Taryba dėl savo žlugusios socialinės ir ekonominės politikos subyrėjo 1992 metų spalio 11 dieną, taigi dvejais metais anksčiau numatyto termino. Todėl Landsbergis su aplinka ėmė aršiai šiauštis prieš Maskvą nepriklausomybės gynimo klausimais. Šiose pozicijose jie respublikoje reiškėsi didvyriais.

Politbiure visi rėmė Gorbačiovą, siekiantį „sutvarkyti“ Lietuvą. 1990 metų gruody jis įteikė TSRS gynybos ministrui Dmitrijui Jazovui keistą įsakymą: paskelbti Lietuvos teritorijoje šaukimą į kariuomenę. Taigi, respublikoje itin sudėtinga situacija, o Jazovas gauna tokį įsakymą. Jis siunčia į Lietuvą naujas karines pajėgas — desantininkus. Kaip žinia, respublikoje tai sukėlė naujo nepasitenkinimo bangą.

Beje, šauktiniai dažnai slėpėsi psichiatrinėse gydyklose arba šiaip ligoninėse. Ten ateidavo kariškiai ir juos išsivesdavo. Tai buvo pateikiama kaip „baisūs režimo nusikaltimai“.

Ypač pabrėšiu, kad Landsbergiui su Gorbačiovu reikėjo bet kokiu būdu sutriuškinti Lietuvos nepriklausomybės priešininkus ne tik Vilniuje, bet ir Maskvoje. Todėl ir buvo sumanytas nesėkmingas, išdavikiškas jėgos panaudojimas Vilniuje. Priminsiu, jog 1991 metų sausio 13-osios rytą Lietuvos Kompartijos CK (TSKP platformoje) pastate mane prie kabineto pasitiko TSRS filmavimo grupė, vadovaujama žinomo operatoriaus Romano Karmeno. Jis paklausė, ką aš manau apie įvykius prie televizijos bokšto. Aš atsakiau, jog „karinė akcija pasodino Landsbergį ant balto žirgo ir dabar Lietuvos išėjimo iš TSRS klausimas — laiko klausimas“.

— Lietuvos ir Rusijos žiniasklaida buvo rimtai užsiėmusi antitarybine propaganda?

— Pastoviai straipsniuose ir televizijoje buvo išradingai meluojama. Pavyzdžiui, 1990 metų rugsėjį Lietuvos generalinis prokuroras Artūras Paulauskas per centrinę TSRS televiziją pareiškė, jog Kaune tarybiniai karininkai su kareiviais įsiveržė į moters butą, išsivedė jos vyrą ir greta namo jų vaikų akivaizdoje sušaudė.

Paskui paaiškėjo, kad lietuvis vaikinas pabėgo iš tarybinės kariuomenės, atkeliavo į Kauną ir įsikūrė pas našlę su dviem vaikais. Jis savaitę meilinosi, o paskui suuostė kur ji slepia 10 tūkstančių rublių — tai dviejų „žigulių“ kaina. Apvogė patiklę našlę ir dingo. Ji kreipėsi į miliciją. Ten paaiškėjo, jog vaikinas — dezertyras. Tada buvo liepta jį surasti. Surado, sugavo ir vežė į karo ligoninę patikrinti sveikatos, bet jis iššoko iš mašinos.

Jį vežęs sargybinis iššovė į orą, perspėdamas, kad kitas šūvis bus kitoks. Antras šūvis vaikiną nukirto. O kaip šį faktą pateikė Paulauskas? Aš, TSKP CK narys, reikalavau, kad TSRS centrinė televizija jo pasisakymą paneigtų. Nepaneigė.

— Kokia priežastis lėmė sausio 13-osios įvykius?

— Situacija įkaito, kai Landsbergis davė premjerei Kazimirai Prunskienei specialų sutikimą kelis kartus pakelti maisto produktų kainas. Priešais Aukščiausiąją Tarybą buvo parduotuvė „Talinas“, iš jos išėję žmonės piktinosi kainų pakėlimu, organizavo nedidelį mitingą. Nepasitenkinimas ritosi per Vilnių kaip gaisras. Sausio 8-osios rytą Kuro aparatūros gamyklos Sąjūdžio grupė pradėjo mitingą prieš kainų pakėlimą.

Įdomiausia tai, jog teismo metu pateikus klausimą – kas pradėjo mitingą? – buvęs Lietuvos saugumo departamento vadovas Mečys Laurinkus pareiškė, jog tai valstybinė paslaptis. Vienu metu mitingo prie Aukščiausiosios Tarybos organizatore buvo įvardinta „Vienybė“ — internacionalinė organizacija, sutelkusi įvairių tautybių Lietuvos piliečius.

— O ką tai davė Landsbergiui ir jo komandai?

— Dabar teisme dėl sausio 13-osios įvykių pateikiami iškraipyti faktai. Sakoma, jog riaušes Lietuvoje 1991-ųjų sausį sukėlė komunistai, jie esą net bandė užgrobti valdžią. Tiesa, jie nesiryžo pulti Aukščiausiosios Tarybos — apsiribojo televizijos bokšto bei Radijo ir televizijos komiteto pastatais.

Šiandien visiškai aišku, kad kruviną akciją prie televizijos bokšto organizavo Landsbergis su savo aplinka. Pasikartosiu: jiems reikėjo išlikti valdžioje. Juk 1991-ųjų pradžioje Prunskienės reitingas buvo daug aukštesnis nei Landsbergio. Tuomet ji jau buvo aplankiusi daugelį šalių, ją visur priėmė ir net pavadino „Gintarine ledi“.

Akivaizdu – Landsbergis, nepriklausomybės paskelbimo iniciatorius, negalėjo susitaikyti, kad Prunskienė renka politinius taškus. 1991 metų pradžioje, visuomenės apklausos, kurią pravedė Lietuvos mokslų akademijos Filosofijos, sociologijos ir teisės institutas, duomenimis, 46 proc. respublikos gyventojų buvo nusivylę Aukščiausiosios Tarybos veikla. Teigiamai ją vertino tik 31 proc. Tuometinės premjerės Prunskienės reitingas siekė 49, Landsbergio — 34 proc.

Žodžiu, Landsbergiui reikėjo bet kokiu būdu užsidirbti politinių taškų ir pašalinti iš arenos Prunskienę. Tai ir buvo padaryta organizavus sausio įvykius.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 15 — id: `scraped:rubaltic_lt:7d9b5316c362bd83`

**Title:** Vietoj sviesto Pabaltijis pasirinko patrankas

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuva ir Latvija padidino savo karinius biudžetus iki 2 proc. BVP ir nuo 2018 metų šios išlaidos atitiks NATO reikalavimus. Tačiau ties šiais „pasiekimais“ Vilniuje ir Rygoje neketinama sustoti, ir artimiausiais metais gynybinius biudžetus numatoma didinti iki 2,5, o vėliau — ir iki 3 proc. BVP. Tokiu būdu Pabaltijo šalys muša tarp Europos šalių rekordus karinių išlaidų didinimo srityje. Ir tuo metu pagal išlaidas socialinėms reikmėms, skirtumą tarp turčių ir neturtingųjų bei gyventojų materialinę gerovę Pabaltijis liūdnai velkasi ES uodegoje ir nebando priartėti prie europietiškų sąjungininkų.

2018 metais Lietuvos biudžete karinės išlaidos sudaro 2,006 proc. BVP. Finansavimas padidintas ne tik kariuomenei, bet ir kitoms jėgos struktūroms. Vėl padidėjo Saugumo departamento, Specialiųjų bei Finansinių nusikaltimų tyrimų tarnybų ir prokuratūros biudžetai.

Kitiems Lietuvos biudžetininkams mažiau pasisekė. Nors dabartinė Lietuvos valstiečių ir „žaliųjų“ sąjungos vyriausybė paskelbė 2018 metų biudžetą socialiai orientuotu, išlaidas socialinėms reikmėms jei ir padidino, tai daug mažiau negu žadėjo.

Pavyzdžiui, mokslo vystymuisi valstybė skyrė 22 milijonus eurų vietoj mokslininkams žadėtų 34 milijonų. Papildomų 5 milijonų eurų, kuriuos buvo numatyta skirti studentų stipendijų didinimui, nepavyko rasti. Kovai su smurtu buityje vietoj planuotų 4 milijonų skirta 660 tūkstančių eurų. Nuskriausti liko Lietuvos medikai, gelbėtojai, gaisrininkai.

Kai kurių valstybės tarnautojų atlyginimai 2018-aisiais išaugs 70 proc., o pasieniečių — tik 5. Specialiųjų tyrimų tarnybos ir prokuratūros darbuotojai pagal biudžeto projektą turės gauti 30 proc. daugiau, o mokytojai ir gydytojai — tik 2 proc.

Po to, kai Seimas priėmė biudžetą, Lietuvos gydytojų sąjunga paskelbė, kad medikai protestuos. „Tai bus taikus mitingas. Mes manome, jog tai greičiausiai bus pirmoji sausio savaitė. Mes nenorime atkreipti į save deputatų ir gyventojų dėmesio tą savaitę, kai bus minimi Sausio 13-osios įvykiai: ši data netinka politiniams žaidimams. Mes planuojame, jog į gatves išeis daug rezidentų, visi Lietuvos gydytojų sąjungos nariai ir juos palaikantys piliečiai. Manome, susirinks apie 500 žmonių“, — pareiškė Lietuvos gydytojų sąjungos narė Urtė Builytė, teigianti, jog galutinis sprendimas nekelti jauniems gydytojams atlyginimų 30 proc. ir palikti juos „minimumo“ lygyje tapo profesionaliai bendrijai „paskutiniuoju lašu“.

Protestuoti ruošiasi ir mokytojai. Iškart trys Lietuvos pedagogų profesinės sąjungos paragino kolegas siekti atlyginimų didinimo protesto akcijų metu. „Garsiai skelbti apie proveržius Lietuvos švietimo sistemoje galima tik visa tai deklaruojant. Vyksta atviras jos naikinimas — uždaryta tūkstančiai mokyklų, Lietuva prarado 30 tūkstančių mokytojų ir virš 300 tūkstančių mokinių“, — teigiama mokytojų profsąjungų kreipimesi.

Karinis biudžetas didžiulis, visi pinigai ten plaukia. „Aš asmeniškai už tai, kad išlaidos gynybai būtų sumažintos“, — sako Vilniaus universiteto docentė Donata Petružytė.

Nuskriaustųjų protestai lydi Lietuvą su Latvija visus tuos metus, kai buvo siekiama 2 proc. BVP skirti karinėms reikmėms (Estija NATO normatyvą pasiekė iškart, tačiau ir ji didina savo gynybinį biudžetą). Latvijoje prieš du metus 2016-ųjų metų biudžeto projekto svarstymo metu vyko didžiausias per 15 metų mokytojų streikas. Jame dalyvavo 911 mokymo įstaigų. Latvijos švietimo ir mokslo dabuotojų profsąjunga į gatves išvedė 24,5 tūkst. žmonių.

Tai buvo didžiausios respublikoje protesto akcijos per daugelį metų. Išgąsdintas latvių Seimas buvo priverstas peržiūrėti biudžeto projektą: skirti 9 milijonus eurų mokytojų ir 10 milijonų eurų gydytojų atlyginimų didinimui.

Latvijos gydytojai streikuoja pastoviai. Paskutinį kartą jie streikavo 2017 metų vasarą, gydyti pacientus dėl menkų atlyginimų atsisakė šeimų gydytojai, ir tada Latvijos nacionalinė sveikatos tarnyba buvo priversta išleisti gyventojams instrukcijas, nurodančias, kur streiko metu kreiptis medicininės pagalbos.

Karinio biudžeto didinimas iki 2 proc. BVP,  gyventojų manymu, nereiškia gerovės, ir todėl Pabaltijo šalių vyriausybės priverstos kalbėti apie tai, jog socialinės sferos finansavimą didina lygiagrečiai su išlaidų didinimu karinėms reikmėms.

Apie dabartinių biudžetų socialinę orientaciją kalbama ir Lietuvoje, ir Latvijoje. „Jeigu 2017 metais prioritetinės šakos buvo švietimas ir gynyba, tai 2018-aisiais didesnis dėmesys skiriamas sveikatos apsaugai ir demografijai“, — pasakė Latvijos premjeras Maris Kučinskis. „2018-ųjų biudžetu siekiama, kad Latvijos gyventojai taptų stipresni ir sveikesni“, — sako Latvijos finansų ministrė Dana Reizniece-Ozola.

Tačiau visiškai neaišku, kokiu būdu, turint tokį 2018-ųjų metų biudžetą, vyriausybė gerins katastrofišką Latvijos demografinę situaciją. Todėl kad, pavyzdžiui, pašalpų šeimoms dydis nesikeis, toks pat liks ir jaunų šeimų rėmimo biudžetas. Užtat karinis biudžetas ūgtels dar 126 milijonais eurų ir pagaliau pasieks 2 proc. latvių BVP.

Ir tai ne riba.

Palyginimui — Vokietija pareiškė JAV administracijai, jog ji neturi pinigų karinių išlaidų didinimui iki tų 2 proc., kurių reikalauja Donaldas Trampas. O „karpyti“ kitus biudžeto straipsnius, siekiant įgyvendinti NATO rekomendacijas išlaidų gynybai klausimu, Bundestagas neketina.

Bet ar galima lyginti „turtingąsias“ Pabaltijo šalis su kažkokiais ten Vokietijos „vargšais“? Latvija ir Lietuva — ne Vokietija: jos ras lėšų ir pastoviam karinių išlaidų didinimui, ir dar gydytojams jų liks. Tiesa, patys Pabaltijo gydytojai taip nemano, o tai liudija jų mitingai ir streikai ir dar emigracija į tą „varganą“ Vokietiją.

Lietuvos ir Latvijos valdžios susikrimtusios dėl šios problemos, jos pripažįsta, kad jų šalių piliečių greit nebus kam gydyti, tačiau vis tiek didina išlaidas kariuomenei ir specialiosioms tarnyboms. Ir kaip jų neatjausti: jog kinkos dreba dėl „rusų grėsmės“ ir „rusų agresijos“, pasienyje variklius šildo rusų tankai, o Vilniuje, Taline ir Rygoje visur kyšo „Maskvos ranka“.

Todėl kad, jeigu Pabaltijo šalių valdančioji klasė ir toliau užsiiminės visų išlaidų straipsnių apkarpymu vardan nesibaigiančio karinių išlaidų didinimo, iš Pabaltijo išvyks visi pajėgūs išvykti, o nepajėgiantys išmirs. Ir tada atsilaisvinusias dykvietes Rusija galės užimti be jokio įsiveržimo.

Taigi logika neleidžia ginčytis ir tiesiai į akis sako: Pabaltijo valdantieji politikai ir e yra „Maskvos ranka“!

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 16 — id: `scraped:rubaltic_lt:c9f738297038ad7a`

**Title:** Baltarusija pradėjo eksportuoti naftos produktus aplenkdama Pabaltijį

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Baltarusių koncernas „Belneftechim“ pasirašė kontraktą dėl savo naftos produktų eksportavimo  per Rusijos jūrų uostus: pirmieji 72 tūkstančiai baltarusių naftos krovinių tonų jau iškeliavo eksportui ne per Pabaltijį, o per Rusiją. Taigi baltarusių naftos tranzito perorientavimo procesas prasidėjo. Pabaltijo šalys pradeda prarasti baltarusių krovinius.

„Belneftechim“ pirmininkas Igoris Liaščenka Sąjunginės Rusijos ir Baltarusijos valstybės Ministrų Tarybos posėdyje pareiškė, kad Baltarusija artimiausiu metu nukreips pirmąją savo produkcijos partiją per Rusijos uostus. Iki 2018 metų sausio per Rusiją buvo numatyta eksportuoti 72 tūkstančius tonų baltarusių naftos produktų. „Atitinkamas kontraktas dėl krovinių nukreipimo per Rusijos uostus jau yra“, — pasakė Liaščenka.

Kalbėdamas apie tai, ar baltarusių naftos perdirbimo pramonei naudinga perorientuoti savo krovinių srautą iš Pabaltijo į Rusiją, „Belneftechim“ vadovas pažymėjo,  kad gamybos, transportavimo ir energijos nešėjų pardavimas yra matematika. Jeigu paskaičiavimai rodo, kad nukreipti naftos produktus per Leningrado srities uostus naudinga, atitinkami kontraktai pasirašomi.

Igorio Liaščenkos žodžiais, pervežimai per Ust-Lugą — abipusis Rusijos ir Baltarusijos interesas. Kontraktas dėl baltarusių naftos produktų pervežimo per Rusijos uostus – pavyzdys normalaus, abiems pusėms naudingo bendradarbiavimo. Jei ši pirmoji patirtis bus sėkminga, tada 2018 metais Baltarusijos naftos perdirbimo įmonėse pagamintų produktų eksportas per Rusijos Šiaurės Vakarų uostus gali pasiekti milijoną tonų.

Šių metų rugpjūčio mėnesį Rusijos prezidentas Vladimiras Putinas pasakė, kad baltarusių naftos produktai, pagaminti iš Rusijos naftos, kuri Baltarusijos NPG tiekiama lengvatinėmis sąlygomis, turi būti eksportuojami ne per Pabaltijo, o per Rusijos uostus. „Tai aptarti būtina platesniu formatu. Juk baltarusių NPG perdirba mūsų naftą (Rusijos — RuBaltic.Ru pastaba), kitokios ten nėra ir vargu ar kada nors atsiras, todėl visa tai būtina įsisamoninti — mūsų nafta, mūsų infrastruktūros panaudojimas, — pasakė Putinas Kaliningrade. — Tai ne kažkokie politiniai sprendimai, nes privalome pilnu pajėgumu panaudoti savuosius galingumus, čia sukurti mokesčių bazę, nes turime darbo vietas kurti — būtent Rusijoje, o ne kažkokioje kitoje vietoje“.

Lietuvoje ir Latvijoje Rusijos prezidento žodžiai sulaukė reakcijos, kuri primena nemirtingą Čechovo frazę: „To negali būti, nes to negali būti niekada“. Esą Baltarusija neatsisakys tranzito per Pabaltijo šalis, nes kiti variantai nerealizuotini.

Ust-Luga, Primorskas ir kiti Leningrado srities uostai atitolę nuo Baltarusijos naftos perdirbimo gamyklų 800 kilometrų atstumu, tai daug toliau, nei iki Ventspilio, Rygos ir Klaipėdos uostų. Taigi transportavimo išlaidos daug didesnės, nei per Pabaltijį. Be to, baltarusių naftos produktų perkrovimas Pabaltijo uostuose kainavo 6–8 dolerius už toną, kai tuomet Rusijos — 12–18 dolerių.

Ir todėl tranzito perorientavimas buvo paskelbtas neįmanomu. Pabaltijyje, kaip visada, buvo užsiimta savęs įtikinėjimu ir įsitikinta, jog Minskas Putinui nenusileis, o kadangi baltarusių NPG krovinių srautų perorientavimas po to, kai tokį uždavinį pagarsino Vladimiras Putinas, tapo Rusijos prezidento politinės reputacijos klausimu, Kremlius vis labiau spaus baltarusių sąjungininkus. Tarp Maskvos ir Minsko neišvengiamai kils naujas konfliktas, kuris įgaus politinį charakterį. Lietuvos žiniasklaida prognozavo greitą Sąjunginės valstybės mirtį: „Sąjunga jau egzistuoja virš 17 metų, tačiau sunku pasakyti, ar ji įžengs į trečią dešimtmetį“.

Ir štai Pabaltijį pasiekė realybė.

Baltarusija į Rusijos prezidento žodžius sureagavo visiškai ne taip, kaip to buvo norėta Lietuvoje. Minske pareikšta, kad perorientuoti tranzitą į Rusiją bus galima, jei tai bus naudinga Baltarusijai ir nepakenks jos ekonominiams interesams. Baltarusijos vyriausybė atsisakė šį klausimą vertinti kaip politinį, juolab — perimti kaimynų politinius paistalus: kalbėti apie „energetinį šantažą“ ir dar kažką panašaus. Priešingai, oficialūs Minsko atstovai pasakė, kad Maskva nespaudžia baltarusių sąjungininkų ir „neišsukinėja rankų“ naftos krovinių perorientavimo klausimu.

Profilinių valstybinių įmonių darbuotojai, Rusijos ir Baltarusijos verslininkai keletą mėnesių analizavo tranzito problemą, vedė derybas, konsultavosi ir derino sąlygas. Be triukšmo, informacinės isterijos ir rezonansinių politinių pareiškimų.

Lapkričio mėnesį įvyko Rusijos ir Baltarusijos vice premjerų Arkadijaus Dvorkovičiaus ir Vladimiro Semaškos susitikimas. Baltarusiai tada pareiškė, jog jie neturi teisės dėl tranzito perorientavimo prarasti nė kapeikos, ir Rygą su Klaipėda jie keis į Ust-Lugą ir Sankt-Peterburgą tik tomis sąlygomis, kurios bus naudingos jų ekonomikai.

Tokios sąlygos, atrodo, buvo suteiktos, nes bandymas perorientuoti tranzitą „paleistas“ jau šiemet. Kitais, 2018 metais, per Rusiją nukreipiamų naftos produktų apimtį numatoma padidinti 12 kartų, o po 5 metų, ekspertų teigimu, pagrindinė baltarusių naftos tranzito dalis apeis Pabaltijį.

Būtent čia, o ne tame, kad geležinkeliai ir uostai praranda baltarusių klientus, ir glūdi didžiausias Pabaltijo pralaimėjimas. Juk Lietuvos politikai nesivaržydami kalbėjo, kad siekiant strateginių šalies užsienio politikos laimėjimų, galima paaukoti tranzito šaką.

Jie ir aukojo visus tuos metus, alindami Klaipėdą, kai sukėlė informacinį karą prieš Baltarusijos AE arba dalyvavo ruošiant Minske „demokratinę revoliuciją“ prieš „paskutinį Europos diktatorių“ Aleksandrą Lukašenką.

Šiems politikams rūpėjo ne nacionaliniai Lietuvos interesai, o jiems svetur iškeltas istorinis uždavinys visokeriopai skatinti visiško logiško Tarybų Sąjungos griūties proceso užbaigimą, galutinai dezintegruoti potarybinę erdvę, neleisti Rusijai sukurti naujų susivienijimų ir sąjungų, „pribaigti Imperiją“.

Ir štai rezultatas.

O Pabaltijis su savo Rusijos „sulaikymo“ politika nieko nepasiekė. Užtat prarado galimybę kartu su Rusija dalyvauti visuose stambiuose strateginiuose projektuose ir atstūmė nuo savęs Rusijos rinkas ir tranzitą.

Dabar praranda ir Baltarusijos tranzitą.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 17 — id: `scraped:rubaltic_lt:13f64f99749fed26`

**Title:** Europa neduos Pabaltijui pinigų „skyryboms“ su Rusija

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Nė viena Pabaltijo iniciatyva nepateko į sąrašą Europos Sąjungos prioritetinių projektų, kurie finansuojami bendro ES biudžeto lėšomis. Plataus užmojo nerentabilius Lietuvos, Latvijos ir Estijos ekonominius projektus transporto ir energetikos sferose, atsiribojant nuo Rusijos, Pabaltijo šalys finansuos savarankiškai. Europa daugiau neturi nei pinigų, nei noro dengti istorines Pabaltijo traumas ir kompleksus, kurie sudaro visų jo infrastruktūrinių iniciatyvų pagrindą.

Praėjusį rudenį Lietuvos premjeras Saulius Skvernelis paviešino „paslaptį“: suskystintų gamtinių dujų terminalas Klaipėdoje — „Lietuvos mokesčių mokėtojų našta“. Projektas nerentabilus: apkrauta tik 20 proc. terminalo pajėgumų, sumažinti plaukiojančiojo laivo nuomos sumos nepavyksta, terminalo produkcija pusantro karto brangesnė už rusiškas vamzdines dujas, Latvija ir Estija pirkti iš Klaipėdos suskystintų dujų nenori, ir Lietuvos vyriausybė vos duria galą su galu, kad kasmet šalies biudžete rastų pinigų „energetinės nepriklausomybės palaikymui“.

Kaip visada Pabaltijyje, pagrindinė absurdu kvepiančio lietuviškojo energijos projekto išsilaikymo viltis — Europos Sąjungos pinigai. Jeigu lietuviškasis SGD terminalas bus pripažintas regioniniu, t.y. ne tik Lietuvos, bet dar ir Latvijos bei Estijos avantiūra, Europos komisija ES biudžeto lėšomis padengs dalį jo išlaikymo išlaidų.

Norėdama, kad Independence būtų pripažintas regioniniu projektu ir SGD terminalo „našta“ nuo Lietuvos mokesčių mokėtojų pečių būtų permesta visai Europai, Lietuvos vyriausybė paruošė suktą planą — sukurti bendrą Pabaltijo šalių suskystintų gamtinių dujų rinką. Šioje rinkoje turi būti jau Lietuvoje veikiantis SGD terminalas, būsimasis Estijos SGD terminalas ir Inčukalio požeminė dujų saugykla Latvijoje. Jei Europos Sąjunga paremtų lietuvių iniciatyvą, Vilnius iš ES biudžeto galėtų gauti 150 milijonų eurų kompensaciją savo vargano Indenpendence išlaikymui.

Tačiau stebuklo neįvyko.

Tai reiškia, kad Klaipėdos SGD terminalui nebus suteiktas regioninis statusas ir finansuoti jį Lietuva turės be jokios Briuselio paramos. Lietuvos vyriausybės ministrai laiko šį Europos komisijos sprendimą Lietuvos pralaimėjimu.

Lietuvos energetikos ministras Žygimantas Vaičiūnas pripažino, jog lietuvių pastangomis buvo siekiama „optimizuoti SGD terminalo išlaidas“. „O kas dėl to, jog šiame sąraše nėra projektų (bendrų Europos Sąjungos PCI interesų projektų — RuBaltic. Ru pastaba), tai aš matau tame savotišką einamųjų realijų pripažinimą“, — pareiškė ministras.

Šio Europos komisijos sprendimo reikšmės tikrumas neduoti pinigų eilinei lietuviškai kvailystei puikiai matosi, pažvelgus į Europos Sąjungos požiūrį į Pabaltijo infrastruktūrinius projektus.

Europos Sąjungos transporto komisarė Violeta Bulc š.m. rugsėjo mėnesį pareiškė, kad projekto Rail Baltica finansavimas po 2020 metų priklausys nuo derybų dėl ES septynerių metų biudžeto. Dabartinėje finansinėje perspektyvoje Briuselis atliks savo įsipareigojimą padengti 85 proc. Rail Baltica biudžeto išlaidų, tačiau baigiamojo geležinkelio statybos etapo po 2020 metų perspektyvos atrodo miglotai.

Atsižvelgiant į „brexit“, įplaukų į Europos biudžetą mažėjimą ir bendrą nuostatą užbaigti išlyginimo programas ir uždaryti struktūrinius ES fondus „Naujosios Europos“ palaikymui, tokius žodžius galima suprasti kaip pareiškimą, kad po 2020 metų bus nutrauktas Rail Baltica projekto finansavimas.

Lietuviškoji SGD terminalo epopėja vystosi panašiai kaip didysis Lietuvos „energetinės nepriklausomybės“ projektas – Visagino AE. Šiose istorijose yra daug bendro. Ir vieną, ir kitą kartą specialistai vieningai skelbė, kad lietuviškasis projektas ekonomiškai nerealus ir niekada neatsipirks. Abiejais atvejais Lietuva tikėjosi įkinkyti į vieną vežimą dar ir Latviją su Estija, o šios atsisakė, nes joms buvo siūloma į svetimą objektą, esantį svetimoje teritorijoje, investuoti daug daugiau pinigų.

Pagaliau, pagrindinės Vilniaus viltys dėl AE ir SGD terminalo buvo siejamos su Europos Sąjungos pinigais. Tačiau pinigų Lietuvai Europos Sąjunga nedavė. Ir skirtumas tame, kad Visagino AE dėl to nebuvo pastatyta, o kas dėl SGD terminalo, tai dabar nežinoma kaip jo atsikratyti.

Tendencija matosi vienareikšmė.

Visagino AE, SGD terminalai, elektros kabeliai su Lenkija ir Švedija, geležinkelis Rail Baltica — tai visiškai ne siekis vystyti ekonomiką ir uždirbti pinigų, šie projektai neturi nieko bendro su bizniu. Juose vien tik ideologija ir politiniai šūkiai: „europietiškas pasirinkimas“, „skyrybos su Maskva“, „ okupacijos palikimo atsikratymas“, „sugrįžimas namo“.

Uždaryti Ignalinos AE ir statyti Visagino AE būtina ne tikslu uždirbti Lietuvai daug pinigų, o tikslu nutraukti ryšius su „Rosatomu“.

Pirkti suskystintas dujas iš SGD terminalų būtina ne todėl, kad jos pigesnės už rusiškas, o tikslu įgyti nuo Rusijos „energetinę nepriklausomybę“.

Geležinkelis su europietiškais siauraisiais bėgiais Letuvai reikalingas ne krovinių pervežimui, o tam, kad ji jaustųsi pilnaverte Europos dalimi.

Iš penkių šalių energetinio žiedo Pabaltijo šalys nori ištrūkti ne todėl, kad tiekiant elektros energiją pasitaiko sutrikimų, o todėl, kad negali „demokratinės“ Lietuva, Latvija ir Estija būti viename elektros tinkle su „autoritarinėmis“ Rusija ir Baltarusija.

Visi Pabaltijo infrastruktūriniai projektai, kuriems Vilnius, Ryga ir Talinas prašo Europos Sąjungos pinigų, grindžiami kompleksais ir skausminga istorine praeitimi. „Mes tikri europiečiai“, „mes nuėjome į Vakarus“, „mes skiriamės su Rusija“ — pinigai Pabaltijo šalims reikalingi politinių skaudulių toleravimui, o ne investicijoms į ekonomiką.

Prieš 10 – 15 metų, kai Europos Sąjunga, pasiekusi aukščiausią savo ekonominio ir politinio suklestėjimo tašką, priėmė į savo gretas Pabaltijį, ji galėjo finansuoti Lietuvos, Latvijos ir Estijos kvailiojimus. Dabar, kai krizių išvarginta Europos Sąjunga neturi pinigų, ji neturi ir noro remti pabaltijiečių haliucinacijas.

Ir todėl neaišku, kaip po 2020 metų bus užbaigta geležinkelio Rail Baltica statyba, nes Briuselis jau parodė Lietuvai „špygą taukuotą“ atominės elektrinės ir SGD terminalo klausimu, o kas dėl ištrūkimo iš penkių šalių energetinio žiedo, tai Europos komisija reikalauja pateikti rimtai pagrįstus paaiškinimus, kas netenkina Pabaltijo šalių be problemų veikiančiame tame žiede. Į „prakeiktos okupacinės praeities atsikratymą“ ir kitą „idėjiškai pagrįstą“ argumentaciją nekreipiama dėmesio: paaiškinkite konkrečiai, kodėl Europa vėl turi eikvoti jums savo laiką ir pinigus, padedant ištrūkti iš penkių šalių žiedo.

Europa duoda suprasti Pabaltijui: pinigų jums daugiau nebus. Ateityje savo kaprizus apmokėsite savarankiškai. Pasitraukimas iš penkių šalių žiedo, SGD terminalai, atominė elektrinė, siaurų bėgių geležinkelis — visa tai dengsite savo pinigais. Žinoma, jeigu jų turite.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 18 — id: `scraped:rubaltic_lt:b40e4712cc6120b0`

**Title:** Lūkesčiai ir realybė: kaip Europos Sąjunga apgavo Pabaltijį

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvoje baiminamasi, kad jai teks savo lėšomis likviduoti Ignalinos atominę elektrinę. Stojant į ES Europos komisija privertė Lietuvą atsisakyti Ignalinos AE, pažadėdama padengti visas atominės elektrinės uždarymo išlaidas. Dabar Briuselyje siūloma nutraukti atominės elektrinės uždarymo finansavimą — lai išlaidas padengia pati Lietuva. Tai ne vienintelis pažadas Pabaltijo šalims, kurį Briuselis neištesėjo: analitinis portalas RuBaltic.Ru pamena Pabaltijo šalių lūkesčius tapus ES narėmis — ta narystė Lietuvą, Latviją ir Estiją apgavo arba jos pačios save apgaudinėjo.

1. Ekonomikos vystymasis

Tikėtasi, jog, įstojus į ES, Pabaltijo šalys įgis naują geradarį — tokį pat, kokiu Tarybų Sąjungoje buvo Maskva, tačiau dar turtingesnį. Europos Sąjunga duos Pabaltijui pigius kreditus ir Europos fondų dotacijas, kurių nereikės grąžinti. Finansų srautas iš Briuselio ženkliai pagreitins Lietuvos, Latvijos ir Estijos ekonomikos vystymąsi ir jos per kelerius metus likviduos atsilikimą nuo Vakarų Europos šalių.

Lietuviai turėjo likviduoti savo atominę energetiką: į Europos Sąjungą juos priėmė su sąlyga kad uždarys Ignalinos AE — Lietuva vienintelė tarp kitų Rytų Europos šalių, 2014 metais įstojusių į ES, nesugebėjo apginti savo atominės elektrinės. Latvija stodama į ES turėjo likviduoti cukraus šaką — už narystę Europos Sąjungoje latvių vyriausybė savo noru atsisakė gaminti cukrų.

„Į Latviją įplaukę pinigai nebuvo panaudoti gamyboje, ir tai tapo didele klaida. Gamyba nebuvo modernizuota ir netapo labiau efektyvi“, — taip pasakė kompanijos Laima valdybos pirmininkas Ronald Gulbis.

Pirmųjų trejų narystės ES metų metu šalys džiaugėsi „muilo burbulų“ ekonomika ir išdidžiai vardino save „Baltijos tigrais“, bet vėliau 2008 metų krizė viską sudėliojo į savo vietas.

2.      Infrastruktūra

Pagrindinis Europos Sąjungos struktūrinių fondų sukūrimo tikslas — naujų šalių — ES narių infrastruktūros  vystymasis. „Senoji Europa“ skyrė „Naujajai Europai“ didžiules investicijas, siekdama sukurti „naujokėms“ savarankiško ekonomikos vystymosi infrastruktūros pagrindą, tuo įveikdama Europos šalių susiskirstymą į „donores“ ir „gavėjas“. Šiuo tikslu Europa investavo į Pabaltijį: kad keliai ten taptų kaip Vokietijoje, o verslo aktyvinimas suteiktų šioms šalims galimybę gyventi be išorinio palaikymo ir savo biudžetą formuoti be eurofondų pagalbos.

Briuselis privertė Lietuvą uždaryti Ignalinos AE ir net finansavo uždarymą, tačiau naujos, Visagino AE statybai Vilniui pinigų nedavė. Lietuvos vadovybė keletą metų maldauja, kad Europos Sąjunga finansuotų SGD terminalo Klaipėdoje išlaikymą, tačiau rezultatas nulinis.

Na, o tie infrastruktūriniai Pabaltijo projektai, kuriuos ES vis dėlto finansuoja, ekonomiškai nereikalingi ir negali sukurti pagrindo savarankiškam Lietuvos, Latvijos ir Estijos ekonomikų vystymuisi. Ryškiausi pavyzdžiai — Rail Baltica siaurukas ir „žalioji energetika“, kai visame Pabaltijyje buvo statomi nuostolingi kogeneraciniai įrenginiai, kurių produkcija buvo per brangi energijos naudotojams.

Vienintelis jų tikslas — pinigų įsisavinimas ir europietiškų subsidijų pasidalinimas tarp Europos biurokratų ir vietinių Pabaltijo valdininkų.

3.      Nepriklausomybė

Lietuvos, Latvijos ir Estijos nacionalistai ragino stoti į ES, įtikinėdami gyventojus, kad jų šalims tai vienintelė galimybė išsaugoti 1991 metais išsikovotą nepriklausomybę. Esą be narystės ES Pabaltijo šalys neišvengiamai praras savo suverenitetą ir sugrįš į Rusijos įtakos sferą.

Įstatymai šalims — ES narėms ruošiami Briuselyje. Kaip paskaičiavo Lietuvos Seimas, po įstojimo į ES ir iki 2008 metų 19 proc. visų priimtų Lietuvoje įstatymų  paruošė Europos Sąjunga.

„Tų direktyvų taip daug, jos tokios suveltos, kad pačioms įmonėms labai sunku jose susigaudyti, — apie ES reikalavimus kalba buvęs Latvijos teisingumo ministras Guntars Grinvalds. — Kompanija kreipiasi į valdininkus, o šie sako: „Darykite štai taip“. O paskui išaiškėja, kad direktyva suprasta neteisingai. Pavyzdžiui, joje nenurodytas minkštas pereinamasis laikotarpis — iki 7 metų, o mūsų valdininkai reikalauja kažkokių naujų metinių normų. Arba pasakyta: „Norma nuo 0,5 iki 5 proc.“, — o mūsų valdininkai tiesiog rašo: „5 proc.“ Puolame aiškintis šusnyje įstatymų, ir išaiškėja, kad mes jų tiesiog nežinom“.

4.      Euras

Pabaltijo šalys aktyviau už daugelį kitų šalių — ES narių stengėsi pereiti prie bendros europietiškos valiutos. Pabaltijo politikai įtikinėjo tautas, kad euras priartins jas prie Europos, duos jų šalims konkurentinius pranašumus, o kainos po nacionalinės valiutos numarinimo nepadidės.

Latvijoje per kelis po euro įvedimo mėnesius maisto produktų ir kitų būtiniausių prekių kainos pašoko iki 20 proc. Lietuvoje po euro įvedimo žmonės pradėjo masiškai važiuoti apsipirkti į Lenkiją, nes ten maisto produktai ir kitos prekės kainuoja pusantro — du kartus pigiau, negu Lietuvos Respublikoje. Lenkija, skirtingai nei Pabaltijos šalys, pereiti prie euro atsisako: lenkų zloto išsaugojimas ten pripažintas ekonominio vystymosi ir nacionalinio prioriteto garantija.

5.      Pragyvenimo lygis

Stodamos į ES Pabaltijo šalys tikėjosi socialinio — ekonominio efekto „tramplino“. Narystė Europos Sąjungoje turėjo stumtelėti Lietuvą, Latviją ir Estiją  iki išsvajoto Skandinavijos lygio, sumažinti, o paskui ir visai likviduoti jų atsilikimą nuo turtingų Vakarų ir Šiaurės Europos šalių.

Norvegija ir Švedija, su kuriomis viename „klube“ norėtų būti Lietuva, Latvija ir Estija, užima pirmasias vietas pagal BVP vienam asmeniui ir pirmauja ES pagal gimstamumą.

Pabaltijo šalys pagal gyventojų gerovę užima paskutinias vietas, o dėl gyventojų skaičiaus mažėjimo tampa pirmaujančiomis tarp išmirštančių. Savo šalių „europietišku pasirinkimu“ nepatenkinti Lietuvos, Latvijos ir Estijos gyventojai naudojasi atsiradusia galimybe emigruoti ir kuria savą europietišką pasirinkimą: bėga iš Pabaltijo į Europą ir atgal negrįžta.

Štai toks jis, pagrindinis Pabaltijo europietiškos integracijos rezultatas.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 19 — id: `scraped:rubaltic_lt:67baa8713f88e0ac`

**Title:** Lietuviams verta žinoti: ten, kur deginamos knygos, paskui pradedama deginti žmones

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvoje vis dar kaitinama Rūtos Vanagaitės istorija. Jos knygos nepardavinėjamos, Alma littera leidykla suskubo nutraukti su autore kontraktą, dauguma kolegų pasmerkė rašytoją. Rūtos Vanagaitės „minčių nusikaltimo“ lietuvių visuomenei esmė: rašytoja pateikė nepatogius faktus apie tautos didvyrį, „miško brolį“ Adolfą Ramanauską–Vanagą. Kodėl bandymas peržiūrėti Ramanausko–Vanago biografiją sulaukė tokios aštrios reakcijos, analitiniam portalui RuBaltic.Ru paaiškino Rusijos žurnalistė Galina Sapožnikova, kurios knyga apie 1991 metų sausio 13-osios įvykius prie Vilniaus televizijos bokšto prieš devynis mėnesius buvo paimta ir uždrausta Lietuvoje.

— Galina, Alma littera leidykla nutraukė kontraktą su rašytoja Rūta Vanagaite jos naujos knygos pristatymo išvakarėse ir išėmė iš parduotuvių visas jos knygas. Kaip Jūs vertinate tokią situaciją, juolab, pati neseniai tapote tokios politikos auka?

— Įvertinimas absoliučiai vienareikšmis: „Kviečiame apsilankyti klube!“ Nesinori piktai džiūgauti, tačiau susilaikyti sudėtinga. Daugiau kaip prieš pusmetį Lietuvoje buvo konfiskuotas visas tiražas mano knygos   „Išdavystės kaina“ lietuvių kalba. 2017 metų kovo 8 dieną ginkluoti Lietuvos policininkai įsiveržė į „Politikos“ leidyklą (kai šios įstaigos vyrai sveikino moteris su Tarptautine Moterų diena — RuBaltic.Ru pastaba) ir paėmė visą tiražą.

Lietuvos žurnalistų bendrija šio įvykio lyg ir nepastebėjo. Tuomet, kai valstybės ideologija kuriama linijoje „savas — svetimas“, jokios kitokios reakcijos neverta laukti, ir vis dėlto aš tikėjausi, kad kas nors iš žurnalistų pareikš savo nuomonę. Pavyzdžiui, ta pati Rūta Vanagaitė. Deja...

Lietuvos visuomenė aną skandalą labai ramiai prarijo. Žinoma, ne visi lietuviai — buvo ir narsių žmonių, kaip mano knygos leidėjas Povilas Masilionis ir dar keli, kurie, nepaisant konfiskacijos, organizavo knygos pristatymą Kaune. Aktyvistai – visuomenininkai pasipiktino organų veikla, tačiau jų balsai nebuvo išgirsti, o tarp pasipiktinusių nebuvo žurnalistų ir politikų. Žinomas lietuvių poetas ir mąstytojas Tomas Venclova ta proga tada nepasakė nė žodžio.

Iš kitos pusės, aš žaviuosi drąsa Rūtos Vanagaitės, kuri parašė dvi nemalonias, oficialiai ideologijai prieštaraujančias knygas, nebijo jų pristatyti ir sakyti taip, kaip galvoja. Tai retas reliktas. Ji suteikia vilčių, kad Lietuvoje dar liko bebaimių ir drąsių žmonių – ne visi išvažiavo, ne visus pavyko prigasdinti.

Knygos patosas ne tame, kad žmogus galimai šaudė žydus arba, mažiausiai, siuntė juos miriop, ir ne tame, kad nevalia „miško brolius“ skelbti didvyriais, ką valstybinė ideologija daro jau ketvirtį amžiaus, o tame, kas šis „didvyris“ bendradarbiavo su VRLK (enkavedė). Tai yra šis „nusikaltimas“, kaip supranta Rūta Vanagaitė, daisesnis už žudynes, ar taip reikia suprasti? Čia jau kažkokia aukštyn kojom apversta visuomenė!

Pirmoji Vanagaitės knyga buvo „praryta“ todėl, kad ji ne tiek buvo pavojinga egzistuojančiai ideologijai, kurios pagrindinis principas — Lietuva ir lietuviai –XX amžiaus aukos, tad kuo jie, kentėdami, patys nusikalto, visiškai nesvarbu. Ir ko tada stebėtis? Paprasčiausias fašizmas, kuris jau nieko nestebina. Mūsų, Pabaltijo žurnalistų, plunksnos jau gerokai sudilo apie visa tai rašant.

Negalima pamiršti, kad visuomenėje, kurioje deginamos knygos, paskui pradedama deginti žmones...

Tačiau ir šioje situacijoje aš nematau, kad mano kolegė būtų šimtaprocentinė didvyrė. Tik pažiūrėkite, ką ji sako knygoje „Višta su strimėlės galva“: ji susidomėjo Adolfo Ramanausko–Vanago likimu ir atrado, kad šis bendradarbiavo su VRLK, sudarinėjo žydų sąrašus.

— Vanagaitė kaltinama ryšiais su Kremliumi. Žinomas lietuvių mąstytojas, vertėjas Tomas Venclova, kurį Jūs jau minėjote, pasakė: „Tie, kurie įnirtingai puola Vanagaitę ir naikina jos knygas, pateikia Putinui neįkainojamą medžiagą, padėdami jam įtikinti tarptautinę bendriją, kad Lietuva persunkta fašistinėmis nuotaikomis“. Ar Rusijoje tikrai yra žmonių, norinčių kad Lietuva būtų juodinama?

— Daugiau pakenkti Lietuvai, kaip tai daro pati Lietuva, niekas nepajėgia... Rusijos valstybei belieka sėdėti ir stebėti, kaip pro šalį praplaukia lavonas priešo, kuris neseniai buvo brolis. Aš sakau „brolis“ visiškai samoningai, nes ruošdama savo knygą susitikau su nuostabiais, sąžiningais, drąsiais ir nepalūžtančiais lietuviais. Aš iki šiol esu įsitikinusi, kad ir šalį mes turėjome vieną, ir praeitis buvo bendra, ir patys buvome broliai.

O kas dėl Venclovos, tokie žodžiai XX–XXI amžių mąstytojui neatleistini. Aš dabar net suabejojau, ar jis vertas tokio titulo...

— Viename interviu po to, kas įvyko, Rūta Vanagaitė pasakė, kad panašios „akcijos“ byloja, jog Lietuva nepasiruošusi priimti tiesos. Ar Jūs sutinkate su tokiu tvirtinimu?

— Šimtu procentų. Lietuva nepasiruošusi priimti tiesos. Ji dar 90-ųjų pradžioje „užbetonavo“ mitus ir dabar bijo nuo jų nutolti. Kai mane dar Lietuvon įleisdavo, aš buvau priblokšta matydama, kaip ten minima sausio 13-oji. Kiekvienoje mokykloje buvo organizuojama politinė akcija „Atmintis gyva, nes liudija“, kurios metu mokiniai uždegė ant palangių žvakutes, taip minėdami 1991-ųjų įvykių aukas.

Lietuvių vaikai minėjo gedulo dieną maždaug taip, kaip mes mūsų pionieriškoje vaikystėje — Pavliko Morozovo arba Zojos Kosmodemjanskajos žūties dienas. Tik Maskvoje nieko panašaus jau nėra, o Vilniuje išliko. Sakyčiau, Lietuva — tarybinių tradicijų draustinis.

Savo tyrimo metu susidūriau su įdomiais faktais. Pavyzdžiui, vieno iš sausio 13-ąją žuvusiųjų — Igno Šimulionio — kūnas buvo apšaudytas iš viršaus iš septynių rūšių ginklų. Argi galima to nepastebėti? Lietuvos valstybė 25 metus meluoja savo tautai, kad šis žmogus krito nuo Tarybinės armijos ir „Alfos“ grupės kulkų. Įsivaizduokite tokį vaizdą: specialusis VSK dalinys, kariuomenės elitas, pyškina į vargšelio kūną iš 1898 metų pavyzdžio muškietų.

Tokia politika liečia ne tik 1991-ųjų metų įvykius, bet ir visą tarybinį laikotarpį, „miško brolių“ veiklą ir pasakas apie tai, jog lietuviai nežudė žydų... Nors, kiek žinau, Vilniaus antikvariato parduotuvėse iki šiol galima aptikti daiktų iš žydų namų.

— Kaip manote, ar situacija gali pasikeisti?

— Kad pasikeistų situacija, turi žlugti „landsberginis“ ir „karo kurstytojos“ Dalios Grybauskaitės politinis kursas, tačiau vien to maža. Užaugo naujos kartos, kurioms šie mitai — neginčytina tiesa.

Tenykščiai visuomenei reikia labai rimtų sukrėtimų. Gal ne vienas milijonas, kaip dabar, turi išbėgti iš šalies, o dar du — ir tada pagaliau lietuviai pradės suprasti, kad pastarųjų 25 metų politika yra pagrindinis visos Lietuvos istorijos nusikaltimas.

— Kuo šiandien Lietuvoje pasireiškia atminties politika?

— Tai ne politika, o hipnozė ir dusinimas nuodingais garais, kad visuomenė neatsipeikėtų. Tauta dirbtinai įvaryta į komos būklę pagal technologiją, kurią paruošė nelietuviai. Tačiau aš turiu vilčių, kad vieną kartą visuomenė vis dėlto pabus, ir atsitikti tai gali staiga — panašiai, kaip po komos būklės atsipeikėja beviltiški pacientai.

P. S.

Po to, kai buvo užrašytas šis interviu, žiniasklaidoje pasirodė naujiena, kad Rūta Vanagaitė viešai pripažino, jog jos tvirtinimai apie „miško brolį“ Ramanauską–Vanagą buvo melagingi. „Aš labai gailiuosi dėl savo skubotų ir išdidžiai pareikštų viešųjų komentarų“, — cituoja rašytojos žodžius lietuvių Delfi. Analitinis portalas RuBaltic.Ru dar kartą susisiekė su Galina Sapožnikova ir paprašė jos pakomentuoti naujas aplinkybes, liečiančias Vanagaitės istoriją.

— Galina, Vanagaitė viešai išsižadėjo savo teiginių dėl „miško brolio“ Adolfo Ramanausko–Vanago. Kuo paaiškintumėt tokį elgesį? Rašytoja neatlaikė visuomenės spaudimo?

— Įdomu tai, kad vos prieš porą savaičių taip pat pasielgė modeliuotojas Juozas Statkevičius: pirma davė skandalingai kaltinamą interviu „Sputniko“ agentūrai, o paskui ėmė verkšlenti, kad esą ėjo gatve, nenugirdo, kažką galvojo, neapskaičiavo... Negi kažkas kankina juos visus toje Lietuvoje? Ką gi, leisti sau būti ne gaujoje gali tik labai narsus žmogus.

O šiaip — smulkmeniška visa tai. Dėl lietuvių ne gėda — skaudu. Tačiau bandyti jiems aiškinti, kodėl taip yra, beviltiška. Ateis laikai, ir jie viską patys supras.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 20 — id: `scraped:rubaltic_lt:379b238369ae64f2`

**Title:** Mokykis, Pabaltiji, kaip reikia ginti savo atominę energetiką

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuva vienintelė Europos šalis, kuri pasidavė Briuselio spaudimui ir, nepaisant tautos balsavimo referendume, visiškai uždarė savo atominę elektrinę. Kitos „Naujosios Europos“ šalys, kurias Europos Sąjunga taip pat spaudė, kaip ir atveju su Ignalinos AE, sugebėjo išsaugoti savo atominę energetiką. Pavyzdžiui, Čekija, kurią Briuselyje spaudė tuo suinteresuoti prancūzai ir kaimyninė Austrija, apgynė savo Temelino AE ir liko elektros energijos tiekėja, o ne pirkėja. Kaip čekai padarė tai, ko nesugebėjo padaryti Lietuva, analitiniui portalui RuBaltic.Ru papasakojo Centrinės Europos istorijos ir dabartinės politikos specialistas, Rusijos valstybinio humanitarinio universiteto Tarptautinių santykių ir užsienio regioninio valdymo fakulteto vyresnysis specialistas politologas Vadimas Truchačiovas.

— Pone Truchačiovai, Europos Sąjunga veda pastovią kovą su naujų ES narių šalių atomine energetika, ypač Centrinėje ir Rytų Europoje. Kame, Jūsų nuomone, slypi tikros šios kovos priežastys?

— Čia matome keletą sudėtinių dalių. Pragmatiška tai, jos Europos Sąjunga gina interesus savo atominės šakos, kurioje pagrindinis vaidmuo tenka Prancūzijai. O dauguma atominių elektrinių buvusiose socialistinėse šalyse (ir Suomijoje) pastatytos pagal tarybinius projektus. Ir todėl šioms valstybėms tiesiog lemta bendradarbiauti su Rusija, su „Rosatomu“. O prancūzams, neabejotinai, norėtųsi užimti svaresnę vietą ES rinkoje, kurią jie (tam yra rimtas pagrindas) laiko sava.

Tačiau ne viskas yra pragmatiška. Europiečiai žino, jog buvusių socialistinių šalių atominės elektrinės pastatytos pagal tokius pat projektus kaip ir liūdnai išgarsėjusi Černobylio AE. Egzistuoja dar vienas stereotipas: jeigu elektrinė „rusiška“, vadinasi, ji bloga, nepatikima ir bet kuriuo momentu gali išlėkti į orą. O jau po japonų Fukusimos AE avarijos, kuri įvyko prieš šešetą metų, „taikaus atomo“ baimė išvis paralyžavo daugelio europiečių mąstymą.

Tarp pagrindinių kovotojų su atominėmis elektrinėmis verta paminėti Europos „žaliųjų“ partiją, kuri kaunasi su jomis visur, kur tik jos yra. Jei kalbėti apie atskiras valstybes, tai labiausiai kaip „kovotoja su taikiu atomu“ pasireiškia Austrija, po 1978 metų referendumo atsisakiusi atominės energetikos. Joje apie būtinybę siekti, kad visa Europa taptų „nebranduoline“, vienaip ar kitaip kalba visų vedančiųjų politinių jėgų atstovai.

— Kuriose Europos šalyse nepavyko išsaugoti atominių elektrinių ir kurios šalys sugebėjo apginti savo atominę energetiką?

Lenkijoje AE statyba kolkas sustabdyta, tačiau elektrinė ten niekada ir neveikė. Daugelį savo blokų iš rikiuotės išvedė Bulgarija, energetinius blokus stabdė Slovakija. Vokietijoje veikia AE uždarymo programa, kuri buvo priimta po avarijos Japonijoje. Tačiau ar ji tikrai bus įgyvendinta iki 2022 metų, kaip buvo sumanyta, — klausimas. Esmė tame, kad Vokietijai jau trūksta elektros energijos, o tokios stabilios, kaip E.ON, kompanijos reikalauja padengti joms nuostolius, patirtus dėl atominių elektrinių uždarymo.

Apie ketinimą uždaryti AE ėjo kalba Šveicarijoje, tačiau ten tauta referendumo metu pasisakė prieš tikslius jų uždarymo terminus — kolkas nutarė nestatyti naujų. Planingai pasenusias atomines elektrines arba atskirus energoblokus išvedė iš rikiuotės Prancūzija. Austrija reikalavo, kad eksploatuoti AE baigtų (arba smarkiai sumažintų jų skaičių) Vengrija, Slovakija, Slovėnija, Čekija, Rumunija.

Tačiau atominės elektrinės šiose šalyse veikia. Dirba jos ir Belgijoje, nors daugelis Vokietijos ir Olandijos politikų bandė siekti belgų atominių elektrinių uždarymo. Dirba jos ir Suomijoje, nepaisant vietinių „žaliųjų“ reikalavimo jas uždaryti. AE dirba Didžiojoje Britanijoje, Olandijoje, Ispanijoje, Italijoje, Švedijoje. Ir kolkas nesijaučia, kad artimiausiais metais jos staiga būtų uždarytos, nes tokiu atveju visa europietiška ekonomika patirtų labai skaudų smūgį.

— Papasakokite apie tą kampaniją, kuri reikalauja Čekijos Temelino AE uždarymo. Kokias pretenzijas pateikė Briuselis ir kitos AE šalys Prahai, siekdamos čekų elektrinės uždarymo?

— Pretenzijų Europos Sąjunga nepateikė — iš čekų reikalavo pateikti saugumo garantijas. Bet štai Austrija – kita kalba. Nuo Temelino iki Austrijos sienos mažiau 50 kilometrų, ir austrų valdžia bei visuomenė dar nuo 1980 metų reikalavo užkonservuoti statybas, o po 2003 metų (kai stotis veikė) — sustabdyti AE. Austrų valdžia net grąsino dėl Temelino AE užblokuoti Čekijos įstojimą į Europos Sąjungą, tačiau, spaudžiant ES ir Vokietijai, 2001 metais persigalvojo tai daryti.

Reikia pripažinti, jog tokio pavojaus priežastys egzistuoja. 2006 metais šioje elektrinėje įvyko nedidelė avarija. O tai atsitiko todėl, jog pagal rusišką projektą pastatytoje elektrinėje buvo bandyta įmontuoti amerikietiškus strypus. Čekai padarė išvadas, sugrįžo prie rusiško kuro, ir tokių rimtų incidentų daugiau nepasitaikė.

— Kokių veiksmų ėmėsi oficiali Praha, siekdama išsaugoti Temelino AE?

— Čekija pateikė Europos Sąjungai apskaičiavimus, jog be AE nesugebės palaikyti savo energetinio balanso. Beje, čekų pragmatiškumo šiuo klausimu pavyzdys — Austrija, kuri priversta pirkti užsienyje daug elektros energijos (likimo ironija: ją perka iš to paties Temelino). Be to, Čekijoje veikia dar viena tarybinio projekto atominė elektrinė — Dukovanai. Austrija pastaruoju metu reiškia nepasitenkinimą jos darbu, tačiau uždaryti jos niekas neketina.

Žinoma, būtina pasakyti, kad Čekija vis dėlto sulaukė apribojimų. ES spaudžiant, šalis įsipareigojo pastoviai teikti Austrijai ir Briuseliui informaciją apie jos AE stovį. O po to, kai Temeline pradėjo veikti dar du blokai, čekai kolkas atsisakė plėsti elektrinę. Galimai čia jaučiasi kai kurių šalies politinių jėgų nenoras plėsti bendradarbiavimą su „Rosatomu“. Tačiau visiškai jis nenutrauktas.

— Kuo Čekijos veiksmai skyrėsi nuo veiksmų Lietuvos, kuri taip pat kovojo, norėdama išsaugoti savo atominę elektrinę? Kodėl Čekija galų gale sugebėjo apginti Temelino AE, o Lietuva buvo priversta uždaryti Ignalinos AE?

— Kovoje dėl AE išsaugojimo Čekijoje susitelkė beveik visos vedančiosios politinės jėgos — ir kairiosios, ir dešiniosios. Buvęs ir dabartinis prezidentai Vaclav Klaus ir Miloš Zeman nuo pat pradžių sakė, kad energijos šaltinių pasirinkimas — suvereni Čekijos, kaip nepriklausomos valstybės, teisė, ir visiška dauguma ir politikų, ir gyventojų jiems pritarė.

Ignalinos AE

O ta aplinkybė, kad AE uždarymo reikalavo ta šalis, su kuria Čekijai istoriškai susiklostė gana sudėtingi santykiai, tik pavertė Temelino AE čekų patriotiškumo simboliu.

Ši istorija vystėsi lygiagrečiai su derybomis dėl JAV PRG sistemos radaro montavimo šalyje. Tačiau tauta ir šiuo atveju tarė savo „ne“.

Skirtingai nei čekai, Lietuvos politikai (deja, ir dauguma eilinių lietuvių) mato savo šalies sėkmę aklai vykdant JAV, ES ir NATO nurodymus ir atsisakant nuo visko tarybinio bei rusiško. Ir štai rezultatas: spaudžiant Austrijai, kurios svoris Briuselio kabinetuose nepalyginamai didesnis, nei Lietuvos, lietuviai pasidavė.

O Čekija elektrą parduoda ir į svetimas nuostatas žvelgia ne besąlygiškai, kaip lietuviai, o pasirinktinai — atsižvelgiant į tikruosius nacionalinius interesus.

— Kodėl, Jūsų nuomone, Lietuva dabar taip aktyviai kaunasi su Baltarusijos AE statyba? Ar tai tąsa europietiškos nuorodos kovoti su Rytų Europos atomine energetika?

— Lietuvos politikai nori parodyti save didžiausiais kovotojais už „progresyvias europietiškas vertybes“. Be to, kova su AE Ostrovece — bandymas kaip nors išsaugoti savo įvaizdį po netoliaregiško Ignalinos AE uždarymo, pateisinti save.

Atviras Lietuvos vadovybės kvailumas čia atlieka ženkliai didesnį vaidmenį, nei Europos Sąjungoje egzistuojantis nusistatymas prieš tarybinių projektų atomines elektrines. Ir jei Lietuva ir toliau su dideliu ryžtu, kurį galėtų panaudoti blaiviai protaudama, kovos su Baltarusijos AE, ji rizikuoja tapti bendraeuropietišku pajuokos objektu.

Ir juoksis iš jos ne tik kur nors Olandijoje, bet ir toje pat Čekijoje arba Vengrijoje.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```
