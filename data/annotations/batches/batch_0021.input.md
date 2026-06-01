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

### Article 1 — id: `scraped:rubaltic_lt:d1847423222ac79c`

**Title:** Lietuva tapo „nepriklausomos“ energetinės politikos įkaite

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Parlamento rinkimams artėjant ekonominė padėtis Lietuvoje vis labiau virsta priešrinkiminio įvaizdžio sukūrimo įrankiu. Tačiau padėties energetinėje sferoje pablogėjimas ir Lietuvos viltys, sudėtos į suskystintas gamtines dujas, vargu ar pagelbės šalies valdančiųjų jėgų populiarumo augimui. Portalas RuBaltic.Ru įvertino Lietuvos energetinės politikos pasėkmes valstybės biudžetui ir išsiaiškino, ko tikisi Lietuvos vyriausybė iš Baltijos šalių „bendrų iniciatyvų“ šioje srityje.

Bendros ekonominės padėties šalyje pablogėjimo fone Lietuvos valdžia ieško būdų sumažinti suskystintųjų gamtinių dujų terminalo Klaipėdoje (SGD) aptarnavimo išlaidas.

Projektas, kuris turėjo užtikrinti šalies energetinę nepriklausomybę nuo Rusijos „politinių kainų“ ir kurio įgyvendinimas tapo pagrindine dabartinės Lietuvos prezidentės D.Grybauskaitės pirmos prezidento kadencijos metu užduotimi, priešrinkiminiais parlamento metais, panašu, virsta našta valstybės biudžetui.

Prieš keletą dienų Palangoje vyko neformalus Baltijos premjerų susitikimas, kurio metu Lietuvos ministrų kabineto vadovas A.Butkevičius bandė įtikinti savo kolegas bendrai eksploatuoti SGD Klaipėdoje, tai yra pasidalyti jo išlaikymo naštą. Visa tai labai primena netolimos praeities Visagino atominės elektrinės (VAES) statybos epopėją, kai Lietuvos valdžia taip pat piršo kaimynams bendrą dalyvavimą VAES statybos finansavime. Šių metų balandį energetikos ministras Rokas Masiulis įgarsino savo VAES viziją, pavadinęs ją „bendrų Baltijos šalių regionaliniu projektu“. Tuo pat metu ministro visai nesutrikdė latvių bei estų pareiškimai, kad jie pristatys savo pozicijas tik po to, kai gaus projekto ekonominius apskaičiavimus. Matyt, Lietuva jau viską nusprendė, sprendžiant iš energetikos institucijos vadovo pasisakymų, kuris pakvietė nevertinti Latvijos ir Estijos pareiškimus kaip atsisakymą. VAE projektas negyvybingas, nes, pirmiausia, jis nedomina Baltijos kaimynų. Estija turi didžiausią pasaulyje elektros energijos iš naftingųjų skalūnų gamyklą (9 TVt per metus – 7,5 mln žmonių, skaičiuojant po 1200 KVt per metus kiekvienam) ir yra neto eksportuotojas (virš 40% bendros gaminamos apimties 12 TVt), faktiškai regioninis monopolistas (pagrindinės pardavimo rinkos – Suomija ir Latvija). Antras faktorius – statoma Baltarusijoje Ostrovecko AES, kuri aprūpins elektros energijos perteklių regione, kurio tiekimui į Baltijos šalis gali būti naudojama elektros energijos sistema BRELL (Baltarusija, Rusija, Estija, Latvija, Lietuva).

Šiandien Lietuvos valdžia aktyviai prastumia sekančią „bendrąją“ iniciatyvą. Tuo pačiu Lietuvos premjeras A.Butkevičius neslepia, kad tikslas yra kaimynų pritraukimas „terminalo eksploatacijai pagreitinti, kas sumažintų infrastruktūrinę sudedamąją, t.y. jo išlaikymo išlaidas“. Lietuvos kabineto vadovas buvo tiek įsitikinęs, kad SGD-terminalas būtinas kaimynams, kad net kalbėdamas apie susitikimo rezultatus už savo estišką kaimyną suformulavo Talino poziciją šiuo klausimu, pareikšdamas, jog Talinas nusiteikęs pirkti daugiau dujų per terminalą Klaipėdoje. Kaip vėliau paaiškėjo, A.Butkevičius „neteisingai suprato kolegos žodžius“, į ką jam nurodė Estijos Ekonomikos ministerija, paaiškinusi, kad „ponas Ryivas, greičiausiai, turėjo omenyje, jog Estija palankiai žiūri į dujų rinkos plėtrą regione, taip pagerinant dujų pirkimo sąlygas kompanijoms iš didesnio skaičiaus pardavėjų. Kaip valstybė Estija neperka dujų rinkoje, tai daro dujų kompanijos“.

Iš tikrųjų, juk negalėjo Estijos premjeras, atstovaujantis valstybei, nuspręsti už privačius žaidėjus, kur jiems pirkti dujas. Iškyla pagrįstas klausimas: kam buvo surengtas dujų rinkos liberalizavimas Trečiojo ES protokolo rėmuose laisvai ir konkurencingai rinkai sukurti likviduojant vertikaliai integruotas kompanijas? Kodėl politikai nesuprato vienas kito? Galbūt, tai paaiškinama skirtingu Lietuvos ir Estijos požiūriu į verslo aplinkos formavimą vietinėje energetinėje rinkoje.

Lietuvoje valstybė, nepaisant neseniai užbaigto dujų rinkos liberalizavimo, priverstinai įpareigoja stambius vartotojus pirkti fiksuotas žydrojo kuro apimtis „rinkos“ kaina iš SGD, tuo pačiu pasidalinant su verslu finansine Europos kreditų jo statybai bei išlaikymui aptarnavimo našta. Tokia sąveikos tarp valstybės ir verslo forma ne tik neatitinka rinkos principų, bet ir pažeidžia Europos konkurencijos įstatymus. Dėl ko Lietuvos dujų asociacija (LDA) pateikė Europos komisijai skundą dėl vartotojų bei tiekėjų teisių pažeidimo. LDA nuomone, įstatymas „Dėl SGD terminalo“, o taip pat kiti dokumentai, susiję su jo realizavimu, prieštarauja ES įstatymams, kuriuose užfiksuota, jog „vartotojas turi teisę į laisvą savo tiekėjų pasirinkimą. Dar daugiau, tiekėjai turi teisę į laisvą vartotojų aprūpinimą“. Kaip pabrėžė LDA ekspertai, valstybei verčiant vartotojus pirkti per terminalą ne mažiau ketvirčio reikalingų dujų „riboja konkurenciją rinkoje, formuojant tam tikras teises tik vienam dujų rinkos atstovui – regazifikacinio terminalo operatoriui“.

Priešingai Lietuvoje veikiančiam administratyviniam komandiniam energetinės rinkos reguliavimo būdui, Estijoje, kur nėra elektros energijos stokos, o kasmetinis dujų sunaudojimas sudaro vos apie 0,6 mlrd. kubinių metrų (žema priklausomybė bendrajame šalies energijos balanse nuo išorinio importo), veikia rinkos principai. Dėl šios priežasties premjerai kalbėjo skirtingomis kalbomis.

Visai kas kita – Latvija, kuri kiekvienais metais sunaudoja 1,3 mlrd. kubinių metrų dujų (dvigubai daugiau, negu Estija). Bet ir čia Lietuvos premjero laukė nusivylimas. Papildomi susitikimai dviejų šalių energetikos ministrų lygmeniu parodė tam tikrą susilaikymą klausimuose dėl bendro SGD eksploatavimo. Latvijos ekonomikos ministrė Dana Reizniece-Ozola pareiškė, kad šalis pirks dujas per SGD terminalą tik tuo atveju, jei jų kaina bus konkurencinga. Apie tai, kad ministrė abejoja šio sumanymo perspektyva, liūdija jos pareiškimas rugpjūčio pradžioje BNS paskelbtame interviu apie tai, kad „iš SGD dujos bus 5-6 proc. brangesnės už Latvijas Gaze importuojamas Rusijos dujotiekio dujas“. Ir tai nestebina. Latvijos valdžia, galvodama pirmiausia apie ekonomiką, o ne politiką, atidėjo dujų rinkos liberalizavimą iki 2017 m. (baigiasi susitarimas su „Gazpromu“ dėl Inčukalnio dujų saugyklos nuomos), apsirūpinus tuo ilgalaikes Rusijos tiekėjo nuolaidas.

Taigi Pabaltijo kaimynai, puikiai suvokdami, kad norvegiško Statoil tiekiamų Lietuvai dujų kaina (25 proc. visos importuojamų dujų apimties – 2,4 mlrd. kubinių metrų) aukštesnė, nei Rusijos dujotiekio, neskuba prisijungti prie eilinio regioninio projekto, neturinčio perspektyvos.

Apie tai, kad SGD-terminalas bus nerentabilus, o importuojamos norvegiškos dujos – brangesnės už Rusijos dujotiekio, kalbėjo ir ekspertai. Šiandien ES bendras veikiančių SGD-terminalų galingumas sudaro maždaug 250 mlrd. kubinių metrų per metus („Gazprom“ tiekia Europos rinkai 30 proc. visų sunaudojamų dujų – maždaug 150 mlrd. kubinių metrų), 80 proc. kurių neveikia.

Tai, kad Lietuvos valdžia nežino, kaip sumažinti išlaidas jo išlaikymui, akivaizdu. Aiškios ekonominės politikos nebuvimas paaiškina visiškai priešingus valdžios pareiškimus: pradedant terminalo išpirkimo iš Norvegijos lizingo baigiant planais užkrauti savo kaimynams bendrą „energetinės nepriklausomybės“ naštą.

Pagal sutartį su Norvegijos Hoegh LNG laivo nuomos kaina sudaro 189 tūkst. JAV dolerių per dieną, per metus – 68,9 mln. JAV dolerių, o per 10 metų – 689 mln. JAV dolerių. Taip pat būtina prisiminti, kad kiekvienais metais šalis išmoka pagal Europos kreditus, suteiktus uosto infrastruktūros, o taip pat dujų transportavimo paskirstomosios sistemos statybai (100 mln. JAV dolerių).

Norvegijos kompanija Statoil penkių metų eigoje kasmet tiekia Lietuvos SGD-terminalui 540 tūkst. kubinių metrų dujų, kurių sutartinė kaina pririšta prie Britanijos dujų biržos NBP urminės kainos. Pavyzdžiui, per septynis mėnesius (2014 m. sausis – liepa) vidutinė 1 tūkst. kubinio metro kaina sudarė 303 JAV doleriai. Kai šis vidutinis rodiklis išsisaugojo per metus, neatsižvelgiant į sezoninį kainų kitimo faktorių, Lietuva gavo dujas už 303 JAV dolerius (neįskaitant tiekimo išlaidų). Kokia prasmė Latvijai, kuri pasirašė ilgalaikę sutartį su „Gazpromu“ iki 2017 m., pirkti 10-15 proc. brangesnes Norvegijos dujas, o taip pat apmokėti Lietuvai jų tranzitą? Nereikia pamiršti, kad pastaruoju metu dujų sunaudojimas šalyje sumažėjo 30 proc. (2010 m. – 1,8 mlrd. kubinių metrų, 2014 m. – 1,3 mlrd. kubinių metrų), todėl dabartinės Rusijos dujų koncerno, valdančio 34 proc. nacionalinėje dujų kompanijoje Latvijas Gaze, tiekiamos apimtys pilnai aprūpina šalies poreikius. Strateginis ir ilgalaikis bendrų santykių charakteris su Rusijos kompanija taip pat leidžia Latvijai lanksčiai spręsti klausimus, susijusius su mažėjančiu fiksuotų sutartyje numatytų dujų apimčių sunaudojimu.

Savo ruožtu Estija 2014 metais įsigyjo bandomąjį norvegiškų dujų kiekį, kurio apimtis siekė 100 tūkst. kubinių metrų, tuo eksperimentas ir pasibaigė.

Matomai, Lietuva turi nedidelę tikimybę, jog jai pavyks užkrauti savo kaimynams dar vieną „pelningą“ projektą.

Pačioje Lietuvoje, kur valdžia atkakliai tikino gyventojus, kad dėl terminalo naudojimo komunalinių paslaugų kainos neišaugs, kitą dieną po to, kai miesto šiluminiai tinklai pradėjo priverstinai pirkti dujas iš SGD-terminalo, Vilniuje šildymo kaina paaugo 7 procentais. Pasak miesto šiluminių tinklų „Vilniaus energijа“ atstovo Nerijaus Mikalajūno, „nuo kovo 1 dienos kainoje ėmė atsispindėti iš SGD terminalo perkamų dujų kaina. Kadangi tai brangiausios dujos rinkoje, jos šilumos kainą didino. Iš „Lietuvos dujų tiekimo“ perkamos pigesnės dujos šilumos kainą mažino. Kadangi iš SGD privaloma tvarka perkame apie 65 proc. dujų, o iš „Lietuvos dujų tiekimo“ - 35 proc., bendrai sudėjus, šilumos kaina kovo mėnesį augo“.

Šiandien, kai iki parlamento rinkimų Lietuvoje lieka mažiau vienerių metų, valdžia suka galvą, kaip sumažinti vidines dujų kainas gyventojams, kad pateisinti nepamatuojamą energetinės nepriklausomybės nuo Rusijos kainą, tuo pačiu išsaugojus gerą vardą pagal anksčiau duotus pažadus. Iš čia kyla įvairiausi ministerijų ir institucijų garsūs pranešimai, žadantys kitais metais sumažinti dujų, elektros bei šildymo kainas. Prieš keletą dienų Lietuvos Energetikos ministerija pasisakė už veikiančio vartotojų būtinų fiksuotų dujų apimčių pirkimų iš SGD modelio peržiūrą ir mokesčio įvedimą visiems vartotojams, pajungtiems prie dujotiekio. Toks žingsnis liūdija ne tiek apie altruizmą, kiek apie galimų nuobaudų suvokimą, gręsiančių po vykstančio Eurokomisijos nagrinėjimo Lietuvos atžvilgiu dėl konkurencijos pažeidimo, kurį inicijavo Lietuvos dujų asociacija.

Dabartinėje situacijoje, kai kaimynai neskuba prisiimti dalį SGD terminalo išlaikymo išlaidų, o „Gazprom“ po išėjimo iš Lietuvos aktyvų tapo tokiu pačiu užsienio žaidėju, kaip ir norvegiškas Statoil, galintis formuoti kainas remiantis išorine konjunktūra, tikėtis priešrinkiminei kampanijai palankių dujų kainų Lietuvos valdžia negali.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 2 — id: `scraped:rubaltic_lt:8e47b8a8ada76a37`

**Title:** Baltarusiškas nacionalizmas: „buferinė zina“ sukuria sau Golemą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Baltarusijoje prezidento rinkimams artėjant baltarusiškas nacionalizmas, nepaisant jo silpnumo ir marginalumo, vis dar laikomas vakarų kaimynų vienintele realia alternatyva Lukašenkos režimui. Istoriškai ir ideologiškai „baltos raudonos baltos vėliavos“ adeptai yra Pabaltijo bei Ukrainos nacionalistų broliai dvyniai, aktyviai palaikantys Baltarusijos bendraminčius, kad užpildyti esantį Baltijos – Juodosios jūrų „sanitarijos užkardoje“ nuo Rusijos tarpą. Tai daroma net nežiūrint į tai, kad jei etninis nacionalizmas taps valdančiaja ideologija Baltarusijoje, jis kels grėsmę pirmiausia jos antirusijos kaimynėms: Lenkijai, Ukrainai, Latvijai ir Lietuvai.

Įvairiose pasaulio šalyse požiūris į nacionalizmą skiriasi, kadangi kartais jis suvokiamas visiškai skirtingai. Didžiojoje Britanijoje arba Prancūzijoje nacionalizmas – tai patriotizmo sinonimas: Didžiajai Prancūzijos revoliucijai įtakojant sukurta pilietinė religija, kuri turi apjungti visuomenę meilės Tėvynei bei bendro visų piliečių likimo suvokimo pagrindu. Todėl ten tai išskirtinai pozityvi sąvoka: ką gali piktinti meilė Tėvynei?

Visai kas kita – Rytų Europos nacionalizmas. Šiuolaikinių Rytų bei Pietryčių Europos šalių titulinėse tautose jis gimė ir vystėsi pagal vienodą schemą. Iš pradžių atsirado tautų, įeinančių į Austrijos, Rusijos ar Osmanų imperijas, tautinė inteligentija – tam tikros vietovės senbuvių atstovai, kurie įsigijo išsilavinimą bei įsisavino intelektualias miesto profesijas. Po to iš tautinės šviesuomenės kilo taip vadinami „liaudies dvasios žadintojai“, kurie besiremdami kaimo dialektais kūrė savo protėvių literatūrinę kalbą. Vėliau ši kalba plito per periodinius leidinius, literatūriškai sutvarkytą ir pirmą kartą atspausdintą folklorą bei tautinių istorikų darbus apie savo tautos didingą praeitį (tokiai praeičiai nesant, ją išgalvodavo). Sekančiame etape vyko politinė saviorganizacija bendro tautinio priklausymo jausmo pagrindu ir prasidėdavo kova už tautinės valstybės sukūrimą.

Tokia schema tiko ir čekams, ir vengrams, ir latviams su estais. Daugeliui Rytų Europos tautoms pavyko sukurti savo tautines valstybes po Pirmojo pasaulinio karo, kai griuvo imperijos. Imperijų laikotarpio palikimas šioms tautoms – labai gilus nepilnavertiškumo kompleksas, iš ko kilo nepakantumas svetimtaučių atžvilgiu, savo tautinio pranašumo piršimas ir tautinių mažumų diskriminacija, ypač jei pastarieji imperijos laikotarpiu buvo „ponų tauta“.

Todėl po karo baltarusiškas nacionalizmas socialiniame lygyje išsigimė į marginalinį, nepopuliarų ir beveik sektantinį judėjimą. Skirtingai negu dauguma potarybinių respublikų, jam nepadėjo net TSRS suirimas. Pirmaisiais metais nepriklausomos Baltarusijos valdžia dar bandė remtis nacionalistine ideologija: kovojo prieš rusų kalbą, neigė tarybinę praeitį, bandydami net kalbėti apie okupaciją, prisimindavo Lietuvos didžiosios kunigaikštystės bei Reč Pospolitos vaizdus. Bet viskas užsibaigė jau 1994 metais, kai prezidento rinkimuose laimėjo Aleksandr Lukašenka, kuris suteikė rusų kalbai antrosios valstybinės kalbos statusą, sugrąžino Baltarusijos TSR simboliką ir atgaivino Didžiosios Pergalės kultą.

Ideologija, kuri ketvirtį amžiaus Pabaltijoje buvo valdančioji, o Ukrainoje po Maidano tiesiog akyse tampa valdančiaja, Baltarusijoje dabar yra politinio gyvenimo kelkraštyje. Nors baltarusiškas nacionalizmas visiškai toks pat, kaip ukrainietiškas bei Pabaltijo analogai. Tokios nacionalistinės organizacijos, kaip Baltarusijos liaudies frontas, Konservatyvi krikščionių partija ir kitos, siekia atsisakyti sąjunginės su Rusija valstybės bei rusų kalbos kaip antrosios valstybinės, siekia įstojimo į NATO ir ES, desovietizacijos, įstojimo į regiono kaimynų „buferinę zoną“ prieš Rusiją bei naujos istorinės politikos, kai atrama taptų Lietuvos didžiosios kunigaikštystės bei Reč Pospolitos vaizdai, o ne atmintis apie tarybinę praeitį bei Didįjį Tėvynės karą.

Lietuvos specializuotas leidinys Geopolitika.lt tikisi, kad įvykių Ukrainoje paveiktas Baltarusijos prezidentas apsigalvos ir priims į sąjungininkus baltarusišką nacionalizmą savo valdžiai stiprinti: „Kitas neapdairus Lukašenkos žingsnis – ilgametė antitautinė politika, dėl kurios baltarusų kalba tapo posūniu savo šalyje. Susiaurėjo ir socialinė istorinė atmintis, kurios pagrindu tapo tarybinis laikotarpis. Tačiau susidaro įspūdis, kad dabartinės geopolitinės padėties kontekste Lukošenka pradeda suvokti savo klaidą. Po įvykių Ukrainoje Baltarusijoje pastebimi bandymai apriboti Rusijos patriotinių Georgijaus juostelių naudojimą, o pats Lukošenka po ilgos pertraukos atvirai pradėjo kalbėti baltarusiškai“.

Tai – žodinis palaikymas. Yra ir palaikymas darbais.

Prieš kelias dienas Ukrainos „Pravyj sektor“ pareiškė, kad kuria baltarusišką padalinį. Neofašistinė organizacija planuoja sukurti taktinę grupę „Baltarusija“ baltarusiškiems sąjungininkams apmokyti kovos už savo tautos „išlaisvinimą“ metodams.

Baltarusijos vakaruose gyvena lenkų bendrija. Santykiuose tarp Varšuvos ir Minsko jau buvo daug konfliktų dėl baltarusiškų lenkų, bet jei Minske vadovaus nacionalistai, prasidės totalinė priverstinė lenkų kilmės gyventojų asimiliacija, kurios metu visi be išimčių lenkai pagal etninius požymius bus priskirti „penktajai kolonai“. Kai Baltarusijoje į valdžią ateis nacionalistiškai mąstantys bendraminčiai, Kijevas turės saugotis ne tik Rusijos pasikėsinimo į Ukrainos teritorijas: Baltarusijos nacionalistai lengvai pareikš savo teises į Ukrainos Polesę bei Volyn. Nukentės ir Latvija: šiuo metu Latvijai priklausanti Latgalija anksčiau priklausė Vitebsko gubernijai – tai dabartinė Baltarusijos Vitebsko sritis. Galiausiai, Lietuvos didžiosios kunigaikštystės bei Reč Pospolitos vaizdų atgimimas ir šiuolaikinės Baltarusijos teisių perėmimo idėja su šiais valstybiniais projektais neišvengiamai nuves prie bandymų nuginčyti Lietuvos teisę į Vilnių bei Vilniaus kraštą. Tarp kitko, nuo Baltarusijos sienos iki Vilniaus vos 18 kilometrų...

Nereikia kažkokio ypatingo strateginio mąstymo, kad suprasti, jog siekdami suduoti smūgį Rusijai flirtuojant su Baltarusijos marginalų nacionalistinėmis nuotaikomis, Lenkijos, Ukrainis bei Pabaltijo valdžia smogia sau. Kodėl gi jie vis tiek tai daro? Nejaugi noras eilinį kartą pakenkti Rusijai bei pasitarnauti Vakarų globėjams toks didelis, kad galima vadovautis principu „išdursiu sau akį, kad uošvienės žentas būtų vienakis“?

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 3 — id: `scraped:rubaltic_lt:148e1e9d6b632220`

**Title:** «Ką JAV ketina mokyti žurnalistikos Baltijos šalyse? Kadrų jau nebėra!»

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Pabaltyjoje planingai kuriama informacinės konfrontacijos Rusijai įvedimo infrastruktūra. Pavyzdžiui, Rygoje šiam tikslui Šiaurės tarybos ministrų sąskaita planuojama sukurti Žurnalistinio meistriškumo centrą, o Vilniuje – struktūrą, kuri specializuosis „žiniasklaidos tyrimuose“. Savo ruožtu JAV ambasada Lietuvoje šį mėnesį paskelbė žurnalistų kursų pradžią, kurių tikslas – konfrontacija „Rusijos propagandai“. O Amerikos senatorius John McCain Latvijoje atidarė NATO Strateginės komunikacijos centrą, kuris, anot politiko, „padės paskleisti tiesą“ kaip atsvara Rusijos „propagandos ir dezinformacijos programai“. Ką mano apie šį „vakarų įsiveržimą“ į Baltijos respublikų media lauką vietinės rusiškos žiniasklaidos atstovai, portalas RuBaltic.Ru paklausė portalo BALTNEWS.LT šefo redaktoriaus Anatolijaus IVANOVO:

- Pone Anatolijau, ar tikrai JAV valstybės departamentui apsimoka skirti 500 tūkst. dolerių Pabaltijo žurnalistų apmokymams, tiksliau – jų kvalifikacijos kėlimui?

- Man gaila naivių amerikiečių! Pinigus be jokios abejonės pasidalins reikalingi žmonės, rezultatas bus lygus nuliui, tačiau ataskaitose bus surašyta, kad atliktas darbas reikalauja, greičiausiai, net ir didesnių lėšų, negu buvo skirta.

Aš asmeniškai seniai norėčiau paklausti būvusio Lietuvos švietimo ministro, liberalo pono Gintaro Steponavičiaus, kuris daug kalba apie Kremliaus propagandą: o kur jis ėjo Lietuvos švietimo ir mokslo ministro pareigas? Kodėl jis nesiėmė jokių konkrečių veiksmų, kodėl nesuteikė žmonėms galimybės mokytis žurnalistikos rusų kalba? Būtent šie žmonės dabar dirbtų taip, kaip juos apmokytų Lietuvos aukštojoje mokykloje, pagal Lietuvos programas. Nieko panašaus nebuvo padaryta, todėl aš nesuprantu, ką dabar mokys jankiai. Kol nebus pritraukti profesionalai, rezultato nebus, bet juk nėra profesionalų.

- Prieš keletą metų Jūs steigėt savo mokyklą – Eurazijos media laboratoriją. Tam pastūmėjo būtent jaunų kadrų stoka?

- Taip, jokia struktūra neruošia kadrų Lietuvos rusakalbei žiniasklaidai, todėl atsirado būtinybė savarankiškai juos ruošti. Laikraščio „Lietuvos kurjeris“ bazėje, šio leidinio savininkui palaiminus, buvo atidaryta jaunųjų žurnalistų mokykla, kuri laikui bėgant transformavosi į „Eurazijos media laboratoriją“. Tuo metu visuose lygiuose, įskaitant aukščiausius, į Lietuvą buvo žiūrima kaip tradicinį tiltą tarp Rytų ir Vakarų, tad mes nusprendėme tapti būtent Eurazijos media laboratorija, tai yra media eksperimentų aikštele.

Reikėtų pasakyti, kad mūsų gautas rezultatas iki šiol mums atsiliepia. Žmonės, nedirbantys Lietuvos informacinės erdvės įvaizdžiui, media laboratorijoje įžvelgė potencialą, keliantį grėsmę jų gerovei. Šie žmonės nedaro nieko – pasižiūrėkite, prašom, į pasenusias informacijos pateikimo formas, kurios gyvuoja Lietuvos interneto segmente, Lietuvos televizijoje – ir „naujas kvėpavimas“ buvo jiems nereikalingas. Todėl ši struktūra buvo parodyta kaip „Kremliaus ruporas“, nors tarp jos ir Kremliaus toks pat ryšys kaip tarp jos ir Bekingemo rūmais ar Baltaisiais rūmais. Laboratorija nebuvo kieno nors finansuojama, tai buvo šimtaptocentinė entuziastų saviveikla, bet ją sunaikino, o kam nuo to palengvėjo?

- Reiškia šiandien projektas nebevykdomas?

- Nevykdomas. Nes kvaila vystyti projektą, kuris žmonėms pristatomas kaip grėsmė nacionaliniam saugumui. Sunkiai galiu įsivazduoti, kokią grėsmę kelia nacionaliniam saugumui aštuntokės ir aštuntokai arba devintokės ir devintokai. Bet oficialiai sakoma, kad dažasvydžio žaidėjai kelia grėsmę, nes naudoja nedraugiškų šalių taktiką. Žinote, į tą pačią komandą vertėtų įtraukti visas vairavimo mokyklas, kadangi jų mokinius galima pasodinti už priešo karinės technikos vairo; visus kirpėjus, nes jie gali padaryti šukuoseną a le military – baisiausia grėsmė!

- Jūs sakote, kad Lietuvoje trūksta rusakalbių žurnalistų, o esami laikomi „Kremliaus ranka“. Todėl kyla klausimas, ką gi mokys amerikiečiai?

- Kai aš klausiau Latvijos žurnalistės Olgos Dragilevos reportažą apie knygyną, kuriame parduodamos antilatviškos pakraipos knygos rusų kalba, mano akysbuvo pilnos ašarų. Merginos vardas ir pavardė rusiškos, o rusų kalba ji kalbėjo su tokiu baisiu akcentu, kad normalus žmogus jos nesiklausys. Kaip galima klausyti žurnalisto kalbos, kuris nesugeba net kirčiuoti teisingai. O juk į amerikiečių būrį ateis būtent tokie žmonės, į juos bus dedamos viltys, pagal juos dalins biudžetus, manydami, kad gerai atlieka savo darbą.

Šiais metais Lietuvos švietime paradoksalus ir netipiškas įvykis. Komunikacijų fakultetas, kurio dekanas ne kartą viešai demonstravo nepagarbą Lietuvos rusakalbei žiniasklaidai, netikėtai sudarė rusų mokyklų ar susijusiems su rusakalbe žurnalistika vaikams stojimo sąlygas – į šiuos vaikus dabar dedamos viltys. Rezultatą turėsim po keturių metų. O turėjome, privalėjome – „augančios Kremliaus propagandos“ sąlygose – kurti tokias galimybes prieš daug metų. Kas tai per šalies vadovai, kurie neapskaičiuoja galimos grėsmės iš anskto?

Tokie vadovai labai prasti, ir, tarp kitko, prasti jų globėjai. Aš ilgai juokiausi iš pretenduojančio valdyti pasaulį klouno pono McCain, kai Rygoje kovos su kažkokia propaganda centro atidarymo metu jis nesugebėjo atsakyti Rusijos žurnalistui, kas yra „propaganda“. Reiškia, jis nežino, kokį centrą atidaro, kam šis centras reikalingas – ir tai supervalstybės senatorius. Pas mus, Lietuvoje, tarp kitko, visi šitie kovotojai su propaganda taip pat neturi suvokimo, su kuo kovoja.

- O kaip Jūs suvokiate „propagandą“?

- Propagandos neegzistuoja. Manantys kitaip lai išverčia šį žodį iš lotynų kalbos – „tikėjimas, kurį reikia skleisti“. Nematau nieko blogo sveikos gyvensenos, krikščioniškų vertybių, tradicinės šeimos propagandoje... Pas mus propaganda suvokiama kaip „smegenų plovimas“. Kam plauti smegenis, jei, sprendžiant iš rinkimų į Trakų bei Širvintų rajonų vietos valdžios organus rezultatų, už 10 eurų galima nusipirkti bet kieno balsą. Kam užsiimti smegenų plovimu, kai galima atsivežti pinigų maišą, išdalinti po 10 eurų ir pasiekti geresnio rezultato mažesnėmis išlaidomis?

- Pavyzdžiui, sukurti priešo įvaizdį...

- Mes atlikome Lietuvos žiniasklaidos kvantitatyvinius tyrimus, kurie parodė, kad nėra tokios propagandinės ar kontrapropagandinės medžiagos, kurioje nebūtų apie 10 kartų paminėtas Putinas, Rusija „totalitarinės valstybės“ kontekste, „valstybė-agresorė“ – apie 20 kartų. Lai būna taip, bet štai rugpjūčio 20 Amerikos boksininkas Roy Jones pareiškė, kad nori gauti Rusijos pilietybę, ką besakytų apie totalitarinę valstybę – neeilinis faktas. Prieš šį amerikietį, kad ir sutrenktomis smegenimis, nes jis boksininkas, buvo Gerard Depardieu – nepaskutinis meno pasaulyje žmogus. Dabar – Amerikos mišraus stiliaus kovotojas Jeff Monson ir Italijos aktorė Ornella Muti išreiškė norą gauti Rusijos pilietybę. Jau ją gavo Amerikos snieglentininkas Vic Wild, žinomas Pietų Korėjos bėgikas Viktor An (Ahn Hyun-soo), Estijos čiuožėja Natalja Zabijako ir daug kitų – jie jau yra Rusijos piliečiai.

Todėl kai kalbame apie propagandą, mes turėtumėme suvokti, kad tai abipus aštrus ir labai taškinis ginklas. Baltijos respublikose, kaip ir kitose buvusiose Tarybų Sąjungos valstybėse, iš vis negalima užsiimti propaganda. Mes galime paskelbti herojumi kapitoną Norkų-Vėtrą, gerai žinomą Lietuvos partizaną, bet tiems, kurie žino, jog jis dalyvavo holokauste, didvyrio aureolė subyra, ir tokių pavyzdžių pas mus daug. Koks rimtas politikas dirbs su buvusiu Dnepropetrovsko srities komjaunimo komiteto ideologijos skyriaus darbuotoju Aleksandru Turčinovu? Tik tokie pat komjaunuoliai. Pavyzdžiui, manęs niekas neprivers bendradarbiauti su Irina Farion – gerai žinoma maidano, Kijevo veikėja, kadangi aš puikiai atsimenu teisingą komjaunuolę Irą Farion, Lvovo valstybinio universiteto studentę. Kodėl aš turėčiau tikėti persivertėliais? Kiek tokių žmonių mūsų teritorijose? Visi jie užsiima propaganda ir pamiršta, kad kiekvienas jų turi savo skeletą spintoje. Kai jie ką nors sako, jie agituoja paprastai ne už, o prieš.

- Kai kurie Pabaltijo ekspertai, ypač Lietuvoje, išgirdę, kad su jais nori kalbėtis rusakalbis leidinys, atsisako bendrauti, užleidžiami informacinę aikštelę kitam ekspertui, kurio nuomonė gali būti visiškai priešinga. Estijoje buvo netgi siūloma valdininkams derinti savo interviu Rusijos žiniasklaidai su vietinėmis specialiosiomis tarnybomis. Vėliau šie žmonės kaltina rusakalbę žiniasklaidą prorusiška propaganda, nors iš esmės šis ekspertas turėjo galimybę išreikšti savo nuomonę vienu ar kitu klausimu. Dėl ko taip atsitinka?

- Pradėkime nuo to, kad dalis Lietuvos parlamento narių tiesiog neturi, ką pasakyti. Ką gali papasakoti konservatorius Mantas Adomėnas? Jis skelbia save žmogumi, su kuriuo Vladimir Putin asmeniškai slapta kovoja. Žmogus baigė tarybinę mokyklą sidarbo medaliu, reiškia, jis nėra kvailas, nes tarybiniais laikais durniams medalių neduodavo, o dabar jis propaguoja kitus dalykus jam reikalinga linkme.

Man teko bendrauti su žinomu senosios, gal net seniausios kartos Lietuvos social-demokratu, kuris stovėjo prie Lietuvos nepriklausomybės ištakų, su Nikolaju Medvedevu. Jis pasakė tiesiai šviesiai, kad social-demokratų partijoje (o šiandien tai vedančioji politinė jėga, pagal prognozes ji gali laimėti parlamento rinkimuose 2016 metais) niekas nesuvokia, kas vyksta. Galbūt, supranta ponas Česlovas Juršėnas, tačiau niekada nepareikš savo nuomonės, nes jis geras šachmatininkas ir žino, ką ir kada reikia daryti. Galbūt, žino Aloyzas Sakalas, na ir viskas. Atleiskite, du ideologai vienai partijai – mažoka.

Konservatorių partijoje ideologų iš vis nėra, bet koks dokumentas ruošiamas komandos, kurią sudaro apie dešimt žmonių, kadangi nėra gerų smegenų. Ir tokia pati padėtis kitose partijose – čia jos visos panašios. Atstovai Seime – tai žmonės, kurie turi tam tikrų ryšių su viena ar kita partija, jie mokėsi, tiksliau – lankė kažkokius kursus Vokietijoje, JAV, bet tai nėra fundamentalus išsilavinimas. O kalbant apie išsilavinimo stoką, paaiškėja, kodėl yra visi šie paviršutiniai įvertinimai, kas yra propaganda ir kaip su ja kovoti.

Tarp kitko, visi pas mus sako „kovojame su propaganda“. Tai reiškia, mes kartu su propaganda kovojame prieš kažką trečią, o teisingai reikia sakyti „kovoti prieš propagandą“ . Net šiuose terminuose plaukioja, gėda klausyt.

- Ar Jūs stebite Baltijos politinio elito kova su Rusijos projektu „Sputnik“? Jūsų nuomone, kuo pasibaigs ši istorija?

- Su dideliu malonumu ir dideliu liūdesiu stebiu šią vietinio politinio elito kovą, neturinčią perspektyvų. Turiu omenyje, pirmiausia Lietuvos, Latvijos, Estijos elitus prieš projektą „Sputnik“. Aš įdėmiai išnagrinėjau dokumentus, kur sakoma, jog tai „bjaurus propagandinis projektas“, užduotis kuriam kelia „bjaurus Rusijos prezidentas“ Vladimir Putin su visais tolimesniais padariniais. Noriu paklausti šių žmonių: kam užsienio resursui skverbtis į Baltijos valstybės teritoriją, kad čia iš vidaus užsiimti kažkokia priešvalstybine veikla? Pavyzdžiui, Ašmenuose – 20 kilometrų nuo sienos tarp Lietuvos ir Baltarusijos – įkurkite centrą, susodinkite žmones, mokančius lietuvių kalbą, ir transliuokite savo programas – niekas pas jus neatvyks su kratomis, negrasins resurso uždarymu, kalėjimu ir t.t. Atvykti į valstybę ir kišti savo galvą į kilpą – tai sugalvotų tik žmogus, kuris nesuvokia, kas vyksta šiuolaikinėje media.

- Ar Jūs dalyvausite Amerikos projekte?

- Su malonumu. Nes man būtų įdomu pasižiūrėti, kaip žmonės, senu seniausiai išvažiavę iš Rusijos (gal net ir TSRS laikais), mokys „priešintis Kremliaus propagandai“. Kaip jie tai darys ir kuo argumentuos – šis momentas man įdomus. Smalsu.

Kita vertus, manau, kad ir pats galėčiau pamokyti šiuos instruktorius. Kaip žmogus, kuris yra informacinėje kryptyje, matau gal daugiau, negu matosi iš už vandenyno. Bet aš tuo neužsiimsiu, nes man atmušė norą. Mažai kas supranta, kaip pasiekti reikalingų rezultatų. Jei šie žmonės tikisi gauti rezultatą kas sekundę, jie stipriai klysta – duok Dieve, kad rezultatas būtų po 5-6, o gal net ir 10 metų. Pinigai sunaudojami dideli, bet niekas nepagimdys iš karto 25 metų žurnalisto, turinčio gerą išsilavinimą, vertybių sistemą, aukštą intelektą – viso to pasiekiama metų metais. Deja, šioje vietoje pas mus tuštuma.

Vilniuje nebeliko viešųjų pirčių, tik kažkokie židiniai, tą patį galima pasakyti ir apie žurnalistiką. Nors aš nemėgstu, kai stambios valstybės struktūros kišasi į žurnalistiką, nes nuo to pirmiausia nukenčia pati žurnalistika. Ir neturi reikšmės, kas įsikiša – Kremlius ar JAV valstybės departamentas.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 4 — id: `scraped:rubaltic_lt:fcab7b9d9d4f4506`

**Title:** Potarybinės Lietuvos gimimas: kaip buvo kuriama landsbergistų respublika? Dalis II

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Prieš keletą dienų pasirodęs interviu apie „perestroikos“ laikų Lietuvą su Valentinu Lazutka, kuris tais laikais ėjo Lietuvos TSR Mokslų Akademijos Filosofijos instituto direktoriaus pareigas ir kurį laiką vadovavo Vilniaus Aukštajai partinei mokyklai, sudomino skaitytojus, o tai parodo, jog įvykiai, kurie tapo dabartinės Lietuvos Respublikos pamatais, iki šiol rūpi. RuBaltic.Ru portalas nusprendė pratęsti pokalbių su žmonėmis, kurie gyveno ir stebėjo lūžį 1980-ais bei 1990-ais metais Lietuvoje, ciklą.

Lietuvos Komunistų partijoje buvo ne vien „persivertėliai“, kurie dabar sėdi Seime bei rūmuose Daukanto gatvėje. Buvo ir nemažai principingų komunistų, kurie liko ištikimi savo įsitikinimams, nepaisant nieko. Vienas jų – Vladislav Šved, kuris 1990 metais tapo antruoju Lietuvos KP sekretoriumi. Tokių žmonių šiuolaikinė Lietuvos Respublika bijojo ir bijo: 1992 metų gegužės mėnesį V.Šved buvo areštuotas. Jis buvo kaltinamas esąs Lietuvos „demokratinės“ valdžios nuvertimo plano autorius, tačiau nesurinkę jokių įrodymų jį turėjo paleisti. Gyvendamas šiuo metu Rusijoje ir 2004 metais išėjęs į pensiją, Vladislav Šved aktyviai tiria „perestroikos“ laikų įvykius Lietuvoje ir, dabartinės Lietuvos vadovybės nelaimei, žino tokius faktus, kuriuos Landsbergis ir jo pasekėjai norėtų visam laikui paslėpti nuo visuomenės. Jūsų dėmesiui pokalbio tęsinys, kurio pradžią skaitykite čia .

- Ar dabar Landsbergis globoja esamą Lietuvos prezidentę?

Taip. Jis mano esąs nepriklausomybės patriarchas ir elgiasi labai globojančiai. Kad Landsbergis sukūrė Grybauskaitės fenomeną – tai faktas, kuris niekam nekelia abejonių. Apie tai yra visa straipsnių serija Lietuvos spaudoje, kurią aš laisvai skaitau, kadangi lietuvių kalba – tai mano antroji gimtoji kalba.

Kad Landsbergis iki šiol valdo Lietuvą, nekelia abejonių. Tarp kitko, dar Brazauskas prisipažindavo, kad jis, pirmasis Kompartijos sekretorius bei LTSR Aukščiausiosios Tarybos Prezidiumo pirmininkas, o vėliau – Lietuvos prezidentas, turėjo savo veiksmus derinti su Landsbergiu. Kitas Lietuvos prezidentas Adamkus savo prisiminimuose rašė, kad dvi prezidento kadencijas jis dirbo po „gerbiamų žmonių grupės“ spaudimu, kuri vertė jį į tam tikras pareigas skirti „reikalingus žmones“ ir vykdyti tai, kas jų manymu turėjo būti padaryta. O jų nurodymus jis gaudavo faksu arba telefonu. Žinoma, kad tai buvo Landsbergis ir jo aplinka.

- Kodėl gi jis iki šiol išsaugojo tokią valdžią?

Šis žmogus stato už žmones, kieno biografijoje nemažai tamsių dėmių, kurios daro juos valdomais. Juk Grybauskaitė buvo ne šiaip Kompartijos narė, ji atstovavo partijos elitui – dėstytoja Aukštojoje partinėje mokykloje (APM). Jau nebėra kur toliau. Tai tie žmonės, kurie ruošė partijinius, tarybinius bei ūkinius kadrus. Tas pats Valentin Lazutka: jis profesorius bei mokslų daktaras, jis paruošė eilę rimtų mokslinių darbų. Kurį laiką jis ėjo APM rektoriaus pareigas. Ar galime lyginti Grybauskaitę su juo? Tačiau profesorius Lazutka yra Lietuvos ieškomas nusikaltėlis, o Grybauskaitė sėdi prezidentės kėdėje. O juk jos tarybinio laikotarpio biografija – ištisa tamsi dėmė.

- O Jūs prisimenate Grybauskaitę „perestroikos“ laikais?

O kodėl turėčiau? Grybauskaitė buvo eilinė partijos narė, viena iš 16 tūkstančių Spalio rajono komunistų, kur aš ėjau antrojo, o vėliau – pirmojo partijos rajoninio komiteto sekretoriaus pareigas. Ji niekuo neišsiskyrė. Aukštosios partinės mokyklos dėstytojai, su kuriais man teko bendrauti, taip pat sunkiai ją atsimena. Sako, buvo „pilka pėlytė“ ir skaitė paskaitas, gana silpnas. Apie tai liūdija jos disertacija, kur nerasta nei stilistikos, nei gramatikos. Jei Grybauskaitė nebūtų nacionalinis kadras, ji niekada neapgintų šios disertacijos TSKP CK Visuomeninių mokslų akademijoje.

Tačiau Grybauskaitė leidžia sau kritikuoti kitus, kurie įgijo išsilavinimą tarybiniais laikais. Praeitais metais ji pareiškė, kad reikia „pataisyti“ Lietuvos Aukščiausiojo teismo teisėjus, kadangi jie „sėdi ten su rusiškais diplomais“. Bet ji tai turi du rusiškus diplomus: aukštojo išsilavinimo ir mokslų kandidato laipsnio. Tarp kitko, visi kandidatai, apsiginę disertacijas Visuomeninių mokslų akademijoje, buvo įtraukiami į TSKP CK organizacinio partijinio darbo skyriaus nomenklatūrą kaip kadrų rezervas.

Šiandien Grybauskaitė įrodinėja, kad visada buvo už nepriklausomą Lietuvą ir neva 1990 metais „stumdėsi su desantininkais“ prie įėjimo į Aukštąją partinę mokyklą. Yra žinoma, kad iki 1990 metų rugpjūčio mėnesio Grybauskaitė ramiai praeidavo ten pagal leidimą, kurį išdavė Lietuvos KP / TSKP CK, ir gaudavo atlyginimą iš TSKP kasos. Tai trūko net keturis mėnesius po to, kai Lietuva paskelbė nepriklausomybę, ir pasibaigė tik po APM uždarymo TSKP CK nurodymu.

- Bet ji buvo dingusi – išvyko atostogų...

1990 metų pavasarį jai skyrė kelialapį į Lietuvos Ministrų Tarybos sanatoriją. Matyt, ji jo paprašę dar 1989 metais. Kur ji gaudavo atostoginius? Dar kartą pabrėšiu – iš TSKP CK iždo. Po 1990 metų kovo Aukštoji partinė mokykla buvo finansuojama tiesiogiai iš ten. Grybauskaitė puikiai tai žinojo, kadangi tuo metu ji ėjo mokslinės sekretorės pareigas, o tai ketvirtas žmogus Aukštosios partinės mokyklos vadovybėje. Kitaip tariant, po nepriklausomybės paskelbimo ji pradėjo kilti. O šiandien ji įrodinėja, kad kariavo prieš tarybinę valdžią.

Landsbergis taip pat skelbia save rezistentu numeris vienas – neva jis visą gyvenimą kovojo su Tarybų valdžia. Tačiau priešais mane guli knyga „Dinastija. Landsbergių išgyvenimo istorija“, kurią parašė žymi Lietuvos žurnalistė Rūta Janutienė. Tai pasakojimas apie tai, kaip Landsbergiai gyveno tarybiniais laikais. Knygoje Janutienė sugebėjo dokumentais įrodyti, kad Landsbergių dinastija (Janutienė neatsitiktinai pavadino juos „Landsbergais“, nes ši šeimynėlė neturi tautybės. Jų tėvynė ten, kur gerai maitina) Tarybų valdžios laikais turėjo ne vien sumuštinius su sviestų, bet ir su ikrais. Per 500 savo gyvavimo metų ši dinastija šešis kartus keitė tėviskę bei pavardę. Šiai dienai jie lietuviai ir neva visa širdimi atsidavę Lietuvai. O rytoj?

- Jūs sakote, kad Landsbergis faktiškai buvo KGB agentas. Tokiu atveju, ar Grybauskaitė, kurios globėjas yra Landsbergis, turėjo ryšių su KGB?

Bet kokią situaciją reikia vertinti Dalios Grybauskaitės biografijos įvykių kontekste. Pirma: baigus vidurinę mokyklą ji įstojo į Vilniaus universiteto ekonomikos fakultetą. Nebaigus pirmųjų metų ji staiga metė mokslus. Kodėl? O gi išėjo į Vilniaus valstybinės filharmonijos kadrų skyrių. Sakyčiau, tai buvo ypatingas KGB draustinis. Yra žinoma, kad tarybiniais laikais filharmonija buvo disidentų prieglobstis. Todėl natūralu, kad filharmonijos kadrų skyriuje žmogus galėjo įsidarbinti tik KGB kuratoriaus siuntimu bei jam leidus. Juolab, kad Grybauskaitė išdirbo ten tik 8 mėnesius, o po to išvažiavo mokytis į Leningradą. Kas davė kadrų skyriaus viršininkui bei filharmonijos direktoriui nurodymą priimti Dalią tokiam trumpam laikotarpiui? Ji vos įsivažiavo, kai reikia priimti naują žmogų.

Grybauskaitė atvažiavo į Leningradą, bet į Ždanovo universitetą neįstojo. Ir vėl staigmena. Ją apgyvendino bute, kuris priklausė Leningrado ir Leningrado apskrities KGB Ūkio skyriui. Tai išsiaiškino Rusijos žurnalistas Maksim Leonov.

Po to Grybauskaitė sugebėjo įsidarbinti režiminėje įstaigoje – kailių susivienijime „Rot-Front“. Šis, vienas iš nedaugelių TSRS, palaikė glaudžius ryšius su užsienio partneriais. Susivienijimo darbuotojai reguliariai vykdavo į komandiruotes užsienyje, o laboratorijose buvo naudojami užslaptinti reagentai. Asmeniniame kadrų apskaitos lape Grybauskaitė rašė, kad iš pradžių ji dirbo žaliavų priėmimo bare, o vėliau perėjo į laboratoriją – laborantės-chemikės pareigoms eiti. Tuo pačiu kilusiems iš Pabaltijo slapta susivienijimo laboratorija buvo du kart nepasiekiama. Tačiau neva ji ten dirbo. Po to Dalia gavo susivienijimo charakteristiką ir turėdama dviejų metų patirtį be jokių kliūčių įstojo į Ždanovo universiteto politekonomijos fakulteto vakarinį skyrių.

Po metų Grybauskaitė pateikė pareiškimą dėl stojimo į partiją ir susivienijimo partorganizacijos buvo priimta kandidatu į TSKP narius, kadangi atstovavo darbininkams. Atsižvelgiant į tai, kad ji mokėsi institute, reiškia, galėjo tapti inžinierijos-technikos darbuotoju, tačiau Dalia pasirinko likti darbininke. Kodėl? Tada buvo nuostata: priimant į TSKP gretas vieną ITD reikėjo priimti keturis darbininkus. Todėl 1979 metais Grybauskaitė tapo pilnaverte TSKP nare. Ir štai „vidutinė“ studentė tapo pirmūne. Nuo to laiko ji visus egzaminus išlaikydavo penketui ir gavo raudonąjį diplomą.

Kaip išsiaiškino Maksim Leonov, kai Dalia studentavo Leningrado universitete, ten lankėsi KGB pirmininko pavaduotojas Viktor Čebrikov. Jis kalbėjo su visais LVU studentais, atvykusiais iš respublikų. Tvirtinama, kad ilgiausiai jis bendravo su Grybauskaite, yra to liūdytojai.

Po to Grybauskaitė grįžo į Vilnių ir tuoj pat įsidarbino respublikinėje bendrijoje „Mokslas“. Ji buvo tiesiai prieš namą, kuriame gyveno Dalia su tėvais. Šios bendrijos darbuotojas įgaudavo respublikinio lygio darbuotojo statusą. Paprastai „Mokslui“ vadovavo Lietuvos akademikas, dažniausiai Lietuvos Kompartijos CK narys, o jo pavaduotojo pareigos atitiko Lietuvos Kompartijos CK darbuotojo, iš kur juos ir paskirdavo.

Toliau eilinė staigmena. Po trijų mėnesių Grybauskaitė sugebėjo pereiti iš „Mokslo“ į Aukštąją partinę mokyklą. Nors APM ir buvo regioninė partinė mokykla, bet daugelis dėstytojų ten buvo „ateiviai“, t.y. – iš kitų aukštųjų mokyklų. Vien tik tam, kad skaityti paskaitas APM, reikėjo turėti rimtą dėstymo patirtį. Taip paprastai dirbti APM nepriimdavo. O vakarykštė studentė, tris mėnesius atidirbusi „Moksle“, atėjo ten į žemės ūkio ekonomikos kabineto vedėjos pareigas. Tai tiesiog neįtikėtina.

O toliau kaip sviestu sutepta: jau po dviejų metų Grybauskaitė gavo siuntimą disertacijai rašyti TSKP CK Visuomeninių mokslų akademijoje. Žmonės tokio siuntimo laukdavo metų metais. Lietuvoje tokių buvo mažiau dešimties, o Grybauskaitė gavo siuntimą po dviejų metų. Vos per dviejus su puse metų ji apgynė disertaciją ir po gynybos keturis mėnesius kažką veikė Maskvoje. Šį laikotarpį Grybauskaitė kruopščiai slepia. Kaip matome, tarybinėje Lietuvos prezidentės autobiografijoje per daug neįtikėtinų „atsitiktinumų“, kas leidžia teigti, jog ją nuo jaunystės „šefavo“ įtakingi žmonės. Viskas vienareikšmiškai nurodo – KGB.

- Kiek pamenu, ją siuntė ne vien į Maskvą, bet ir į Vašingtoną?

Niekas negali pasakyti, kada ją nusiuntė į Vašingtoną. 1990 metų rugpjūtį Grybauskaitė tapo Lietuvos ekonomikos instituto moksline sekretore. Ir 1991 pabaigoje – 1992 pradžioje (tiksli data slepiama) nuvyko į pusmetinius mokamus vadovų kursus Džordžtauno universitete Vašingtone.

Teigiama, kad tik po mokslų JAV Grybauskaitė susipažino su Landsbergiu. Tuo pačiu, 1990-1991 metais anas kontroliavo bet kokį svarbų kadrų paskyrimą, o jau žmogaus, kuris ateityje vadovaus ekonominei politikai Lietuvoje, siuntimas į JAV negalėjo praeiti be jo žinios.

Buvęs prezidentas Adamkus 2010 metais pareiškė, kad jis prisidėjo prie Grybauskaitės siuntimo į Vašingtoną. Galbūt. Bet kaip jis susipažino su mažai žinomą buvusią APM dėstytoją? Manau, kad Adamkui, žinomam kaip KGB agentas slapyvardžiu „Fermeris“, kažkas iš buvusiųjų „kontoros kuratorių“ patarė atkreipti dėmesį į „įdomią merginą“, o vėliau Adamkus rekomendavo ją Landsbergiui. Matyt, po Landsbergio pritarimo Adamkus skyrė lėšas Grybauskaitės kelionei.

Iš Vašingtono Grybauskaitė grįžo kaip amerikietiško menedžmento atstovė. Šia kelione ji galutinai nukirto tarybinę „uodegą“. 1996-1999 metais Grybauskaitė vėl siunčiama į JAV, bet jau kaip einanti Lietuvos ambasados JAV įgaliotosios ministrės pareigas. Šis laikotarpis – vienas paslaptingiausių jos biografijoje. Yra žinoma, kad JAV Valstybės departamentas neoficialiai paprašė Lietuvos valdžios laikyti Grybauskaitę persona non grata ir atšaukti. Be ypatingo triukšmo ją atšaukė, ir visi susiję su šia istorija asmenys tyli.

- Bet dabar ji atvirkščiai palaiko glaudžius ryšius su Vašingtonu. Ar čia nėra prieštaravimų?

Jokių prieštaravimų, tai normali padėtis politikoje. 2009 metais, kai Grybauskaitė tapo prezidente, ji užėmė šiek tiek antiamerikietišką poziciją. Pavyzdžiui, ji liepė išsiaiškinti padėtį su slaptu CŽV kalėjimu netoli Vilniaus, kas nepatiko amerikiečiams. Po to Grybauskaitė atsisakė vykti į susitikimą su Obamą Prahoje, dėl ko tas įsiuto. Tada JAV pareiškė, kad Lietuvos prezidentė Baltuosiuose rūmuose gali apsilankyti nebent kaip turistė.

Bet kai amerikiečiai nusprendė spausti Rusiją per Pabaltijį bei Ukrainą, Grybauskaitė tapo reikalinga.

Prieš 10-15 metų šį vaidmenį atliko Lenkija. O dabar į priekį iššoko Lietuva su Grybauskaite, kuri tokiu būdu bando atmaldauti savo amerikietiškas bei tarybines „nuodėmes“. Priminsiu, taip pačiai elgėsi Mišiko Saakašvili. Tas taip pat bandė kariauti su Rusija. Na ir kur jis dabar?

1 dalis

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 5 — id: `scraped:rubaltic_lt:b857ae520e3896ee`

**Title:** Potarybinės Lietuvos gimimas: kaip buvo kuriama landsbergistų respublika? Dalis I

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Prieš keletą dienų pasirodęs interviu apie „perestroikos“ laikų Lietuvą su Valentinu Lazutka, kuris tais laikais ėjo Lietuvos TSR Mokslų Akademijos Filosofijos instituto direktoriaus pareigas ir kurį laiką vadovavo Vilniaus Aukštajai partinei mokyklai, sudomino skaitytojus, o tai parodo, jog įvykiai, kurie tapo dabartinės Lietuvos Respublikos pamatais, iki šiol rūpi. RuBaltic.Ru portalas nusprendė pratęsti pokalbių su žmonėmis, kurie gyveno ir stebėjo lūžį 1980-ais bei 1990-ais metais Lietuvoje, ciklą.

Lietuvos Komunistų partijoje buvo ne vien „persivertėliai“, kurie dabar sėdi Seime bei rūmuose Daukanto gatvėje. Buvo ir nemažai principingų komunistų, kurie liko ištikimi savo įsitikinimams, nepaisant nieko. Vienas jų – Vladislav Šved, kuris 1990 metais tapo antruoju Lietuvos KP sekretoriumi. Tokių žmonių šiuolaikinė Lietuvos Respublika bijojo ir bijo: 1992 metų gegužės mėnesį V.Šved buvo areštuotas. Jis buvo kaltinamas esąs Lietuvos „demokratinės“ valdžios nuvertimo plano autorius, tačiau nesurinkę jokių įrodymų jį turėjo paleisti. Gyvendamas šiuo metu Rusijoje ir 2004 metais išėjęs į pensiją, Vladislav Šved aktyviai tiria „perestroikos“ laikų įvykius Lietuvoje ir, dabartinės Lietuvos vadovybės nelaimei, žino tokius faktus, kuriuos Landsbergis ir jo pasekėjai norėtų visam laikui paslėpti nuo visuomenės:

- Pone Vladislavai, kokie prisiminimai apie „perestroikos“ pradžią išliko Jūsų atminty? Kaip Jūs suvokėt jos pradžią?

Visai teigiamai. Aš – inžinierius, komjaunime bei partijoje kuravau ekonomiką. Darbo gamyboje patirtis ir bendravimas su didžiausių respublikos pramonės įmonių direktoriais (dirbti pradėjau šaltkalviu, po to – institutas, po kurio – technologas konstruktorius, meistras ir eksporto baro viršininkas. Vilniuje aš iš pradžių kuravau Lenino, o vėliau Spalio rajono ekonomikas. Tai sudarė apie 70 procentų sostinės ekonomikos.) leido man iki 1985 metų prieiti aiškios išvados – tarybinė sistema turi būti rimtai pertvarkyta. Ir tai lietė ne vien ekonomikos, bet ir politikos. Ne griaunant iki pamatų, kaip tai padarė Gorbačiov, tačiau permainos buvo būtinos.

- Pradžioje Jūs pritarėte Gorbačiovo žodžiams?

Jo retorika niekada nebuvo konstruktyvi. Tik iš pradžių mes to nesupratome, nes Gorbačiov kalbėjo apie tai, ką žmonės aptardavo virtuvėse arba tarp patikimų žmonių. Dėl tos priežasties jo žodžiai buvo suprantami ir neva teisingi. Bet juk viena šnekėti...

Daug kas žino, kaip išvirti barščius, ir net rašo receptus. Bet leiskite tokiam žmogui, kuris gerai surašo receptūras, nors kartą pagaminti kokį patiekalą, ir paaiškės, kad jis nėra valgomas. Taip ir politikoje: viena pamokslauti, kita įgyvendinti. Bet pradžioje daugelis, ir aš jų tarpe, jį palaikėme, kadangi partijoje pribrendo klausimų, kuriuos reikėjo kažkokiu būdu spręsti.

- Reiškia, jis nesuvokė, ka šnekėjo? Ar sąmoningai kalbėjo viena, darė kita?

Esmė tame, kad kalbame apie žmones, kurie laiko save kone dievais. Gorbačiov jautėsi būtent taip. Ir jį palaikė Raisa. Pastaraisiais metais Gorbačiov ne kartą savo interviu pabrėždavo, jog gimė kaip Jėzus Kristus ant šiaudų ir kad jo senelis, Andrej Moisejevič, neatsitiktinai jį perkrikštino – iš pradžių Gorbačiovą pavadino Viktoru, tik vėliau Michailu. Viktor – tai „nugalėtojas“, o Michail – „lygus Dievui“. Miša nuo pat pradžių manė, kad jo pašaukimas – pakeisti susiklosčiusią TSRS padėtį. Kaip žinia, gerais norais nuklotas kelias pragaran. Reikia pasakyti, šiame kelyje jis nebuvo pirmas, panašu ir ne paskutinis.

- Kalbant apie Tarybų respublikas, Lietuva ir Pabaltijo respublikos visumoje buvo pažangios TSRS respublikos. Kaip ten, ypač Lietuvoje, priėmė „perestroiką“, kaip keitėsi šis požiūris?

Priėmė daugiausia normaliai. Tuo metu aš dar palaikiau ryšius su direktoriais, kadangi nuo 1987 metų pabaigos kuravau ekonomiką. Gorbačiov buvo atvažiavęs ten 1990 metų sausį, prieš tai, kai Lietuva paskelbė nepriklausomybę, kai nepriklausomybės idėja apsėdo visus. Juolab net Lietuvoje, kur gyvenimas nebuvo toks komplikuotas, reformų dėka pasijuto deficitas. Tada Gorbačiov Lietuvoje nieko nepešė.

Tarybinė Lietuva buvo viena pažangiausių TSRS respublikų. Kai kurie rodikliai siekė Danijos lygio. Bet jei pasižiūrėti, kokia buvo Lietuva 1940 metais, jokios kalbos apie „pažangumą“ negali būti – per 20 buržuazinio valdymo metų nieko nebuvo padaryta. Net nesugebėjo pastatyti elektrinės Nemune. Ji buvo pastatyta 1956 metais už sąjungos pinigus. Tarybiniais laikais didžiulės sumos buvo investuotos į tai, kad Pabaltijo respublikos taptų „socializmo vitrina“, tai ir buvo iš jų padaryta.

Turiu pasakyti, kad Gorbačiov TSKP ir, tikriausiai visoje TSRS vyriausybėje atstovavo grupei žmonių, kuri manė, jog Pabaltijis gyvena ne pagal savo galimybes ir reikėtų jį paleisti, kad prasimaitintų savarankiškai. Rusijoje tuo metu buvo daug problemų, o Lietuvoje niekada nesijautė mėsos, pieno produktų, kažko kitko trūkumas, kadangi buvo Maskvos sukurtas specialus Pabaltijo dotavimo ir finansavimo režimas.

Pavyzdžiui, mano mama kilusi iš Voronežo srities, kuri žymi savo juodžiemiu ir kuriai lėšų 100 žemės hektarų buvo skiriama daugiau nei tris kartus mažiau, negu Lietuvai. Arba dar kitas faktas. Baltarusijai 1975-85 metais melioracijai ir kelių statybai buvo skirta apie miliardą rublių. Tai buvo didžiuliai pinigai, tačiau tokia pati suma buvo skirta ir Lietuvai, kurios teritorija tris kartus mažesnė už Baltarusiją. Įsivaizduokite, ką buvo galima padaryti už tokius pinigus mažoje respublikoje.

Kita kalba, kad lietuviai mokėjo išnaudoti tarybinės valdžios pliusus ir juos išnaudojo. Jie mokėjo dirbti. Be to, aš esu šventai įsitikinęs, kad Lietuvoje tikrojo socializmo buvo daug daugiau, negu Rusijoje. Aš praleidau ten (Lietuvoje) 45 metus, todėl žinau, apie ką kalbu.

-Todėl ir Sąjudis, kuris buvo sukurtas kaip palaikantis „perestroiką“ judėjimas, tapo vienu iš pirmųjų liaudies frontų Tarybų Sąjungoje?

Taip, jis iš tikrųjų buvo vienas iš pirmųjų, bet tai nereiškia, kad Sąjūdžio sukūrimo 1988 metais iniciatyva ėjo iš apačios. Lietuvoje tai buvo ne pirmas, o ketvirtas Sąjūdis. Pirmasis – XIX amžiuje – palaikė tautinį lietuvių atgimimą, o sekantys – 1940 ir 1944 metais – buvo nacionalistiniai.

Tautinio judėjimo Tarybų Sąjūngoje idėjos autorius buvo TSKP CK sekretorius Jakovlev. Jis sugebėjo įtikinti Gorbačiovą, kad TSKP reikia pastumti politinėje arenoje: neva daugelis partijos kunigaikščių „apsiėdė“ ir dirba senais metodais. Ir tai buvo tiesa. Partijos bilietas ir pareigos TSKP daugeliui tapo savotiška „duonos kortele“, kuri parūpindavo ne vien duonos su sviestu...

- O kaip tai buvo pas jus?

Kai pas mane 1991 metų gruodį atėjo Lietuvos prokurorai atlikti kratą, jie nusistebėjo: „Jūs ką, turit tik trijų kambarių butą? Neturit mašinos, garažo, sodo? Kas gi jūs per antrasis sekretorius?“

Be abejo, tai iššaukdavo protestą liaudyje. Neatsitiktinai Jelcinui pavyko „pabalnoti“ liaudies mases, kai jis kalbėjo apie visų privilegijų panaikinimą. O kaip realybėje – ką mes matome dabar, ką mes matėme Jelcino laikais? Kur dingo šios privilegijos? Jų atsirado daug kart daugiau. Todėl aš priėjau išvadą, jog evoliucijos kelias geresnis už revoliucijos. Kaip sakė Bismarkas, revoliucijos vaisiais, kaip taisyklė, naudojasi pereivos. Ukrainoje mes kaip tik tą ir matome.

- „Perestroika“ iš pradžių buvo sugalvota kaip sistemos vystymosi evoliucijos kelias...

Taip, sumanymas buvo atsargiai pastumti TSKP visuomeniniame gyvenime, kad partijos vadai neužmigtų ant savo laurų. Kaip buvo iki tol: jei „pirmasis“ kažką pasakė, reiškia tai tiesa. Nebuvo net minties suabejoti TSKP „pirmojo“ nuomone.

Galbūt Gorbačiovo ir Jakovlevo idėja ir buvo gera. Bet aš iš principo netikiu nei vieno, nei kito idėjomis, juose niekada nebuvo nieko konstruktyvaus. Gorbačiov iš pradžių tikrai buvo įsitikinęs, kad kažką gali padaryti, bet po aibės klaidų suvokė, kad už jas reikės atsakyti, šito jis išsigando. 1990 metų gruodžio mėnesį, kai IV TSRS liaudies deputatų suvažiavime Saži Umalatova pareikalavo atšaukti jo prezidento statutą, o vėliau 1991 metais balandį plenume buvo iškeltas klausimas dėl Gorbačiovo nušalinimo, jis suprato, kad jam gręsia Chruščiovo likimas. Bet dar labiau jis bijojo Čaušesku likimo. Matyt, ne šiaip sau Gorbačiov sugalvojo rugpjūčio putčą, kuris nuo pat pradžios buvo pasmerktas žlugti ir kuriame jis atliko pagrindinį užkulisinį vaidmenį. Antrą vaidmenį atliko Kriučkov, jo bendražygis, kuris matė Prezidento išdavystę ir jo nesustabdė.

- Iš tikrųjų, Kriučkov prieštaringa asmenybė. Kartais jį net kaltina, kad jis buvo JAV agentas ir griovė TSRS.

Aš taip nemanau. Turiu keletą straipsnių, kurie skirti Kriučkovui ir TSRS „laidotojams“, kur aprašytas jų vaidmuo griaunant tarybinę šalį. Žinoma, kad Kriučkov, kalbėdamas su Pirmosios pagrindinės KGB valdybos viršininku Šebaršinu maždaug 1990 metų birželio mėnesį, pasakė, kad viltis reikia sudėti į Jelciną. Galbūt, tai paaiškina jo neryžtingumą pučo metu. Tačiau iškyla klausimas: nejaugi Kriučkov nesitikėjo tokios pučo pabaigos? Juk jis turėjo apskaičiuoti. Be to, šiandien jau įrodyta, kad Kriučkov Gorbačiovo nurodymu aprūpino Rusto nusileidimą Vasiljevskio nuokalnėje. Nereikėtų pamiršti, kad Kriučkov vadovavo šalies saugumui, tačiau jis nesusirūpino, kad pranešus Gobačiovui apie Jakovlevo tarnybą amerikiečiams tas tik paprašė su Jakovlevu pakalbėti. Kriučkov pakalbėjo, bet Gorbačiov pasistengė šį reikalą nutylėti. Po kelių mėnesių pagrindinis tarybinis čekistas vėl atvyko pas Generalinį sekretorių ir pasakė, kad Vakaruose žiniasklaida praneša, jog Gorbačiov susitikimo su Bušu Maltoje metu pažadėjo Amerikos prezidentui pakeisti visuomeninę TSRS santvarką, „paleisti“ Pabaltijį ir sujungti Vokietiją... Gorbačiov tik atsakė: „Maža ką ten rašo...“ Kriučkov išėjo, žodžio netaręs. Ką jo vietoj padarytų JAV CŽV ar FTB direktorius? Be abejonės, jis iškeltų šį klausimą JAV Kongrese. O Tarybų Sąjungoje Kriučkov ir toliau vykdė Gorbačiovo nurodymus, žinodamas, kad tas dirba amerikiečių vedamas. Tai verčia susimąstyti.

Tikriausiai, daugelis girdėjo apie Butkevičių, kuris 1991 metais vadovavo taip vadinamai Lietuvos apsaugai nuo TSRS. Na o Gorbačiovo „perestroikos“ laikais jis lankė Amerikos profesoriaus Džino Šarpo treningą ne JAV, bet Maskvoje. Galbūt, visai šalia Lubiankos.

- Sąjudžio formavimas vyko, galima sakyti, jūsų akyse. Ar galėtumėte papasakoti apie tai?

Tai tiesa. Sąjudį organizavo Lietuvos čekistai, kurie veikė TSRS KGB, vykdančio Gorbačiovo įsakymą, nurodymu. Pradžioje šio judėjimo pagrindiniu „varikliu“ Lietuvoje buvo mano geras pažįstamas, rašytojas Vytautas Petkevičius. O jis nebuvo KGB statytinis. Petkevičiaus Sąjudį aš tada vienareikšmiškai palaikiau, nes supratau „perestroikos“ būtinumą. O kas yra Sąjudis, jo istorijos aš tuo metu dar nežinojau. Žinojau, kad Petkevičius – Lietuvos patriotas, kuris niekada neleis respublikoje vadovauti nacionalistams.

Tačiau 1988 metų rugsėjį Lietuvos KGB pirmininkas Eismuntas Lietuvos Kompartijos CK Biuro slaptajame posėdyje pasiūlė vietoj Petkevičiaus Sąjūdžio lyderiu paskirti Vytautą Landsbergį, valstybinės konservatorijos profesorių ir tuo pačiu buvusį KGB informatorių, kurio slapyvardžiai buvo „Vytautas“ ir „Dėdulė“. Tas kilo iš „patikrintos tarybinės šeimos“.

Landsbergio tėvas nuo 1927 metų buvo NKVD agentu, bet karo metais bendradarbiavo su naciais. Po karo tarybinis tribunolas už akių pasmerkė jį sušaudymui. Tačiau 1959 metais jis grįžo iš Australijos į Tarybinę Lietuvą. Čia jis viską pilnumoje atgavo: jam grąžino konfiskuotą sodą, apdovanojo regalijomis ir t.t. Buvo teigiama, kad Landsbergis vyresnysis užsienyje padarė didžiulį įndėlį atskleidžiant tarybinės valdžios priešus. Jo sūnus taip pat buvo laikomas patikimu tarybiniu žmogumi, štai jam ir pavedė vadovauti Sąjudžiui.

KGB turėjo parinkti žmogų, kuris būtų valdomas ir turėjo kažkokį mokslinį statutą, pavyzdžiui, mokslų kandidato. Be to, Landsbergis buvo visai ne charizmatinė asmenybė, turėjo siaubingą tarseną. Kai jis pirmą kartą viešai kalbėjo išlydint XIX partinės konferencijos delegatus, jam iš minios šaukė: „Išsiimk šiaudus iš nosies!“ Todėl kiek Kompartijos CK, tiek ir KGB manė: kur dings šitas pilkas veikėjas? Dirbs kontroliuojamas ir vykdys nurodymus. Bet gavosi priešingai. Profesoriui Landsbergiui kovoje už valdžią išdygo „plieniniai“ dantys ir greitu laiku jis vadovavo respublikoje.

2 dalis

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 6 — id: `scraped:rubaltic_lt:7e2a7a0d67513f50`

**Title:** Kaip šiuolaikinė Lietuva atsikratė KGB munduro? 2 dalis

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Nepriklausomos Lietuvos gimimo istorija, tikroji, o ne „laimėtojų“ parašyta, iki šiol lieka paslaptimi. Visuomenei siūlomi iškilmingi pagal protokolą surašyti mitai apie tautos kovą su „sovietinės okupacijos“ jungu už laisvę, tačiau kaip gi „totalitarinės TSRS“ sąlygose į respublikos vadovybę galėjo patekti dabartiniai aršūs Tarybų valdžios niekintojai? Kieno vedami politiškai susidraugavo dabartiniai Lietuvos vadovai? Kokiame būtent „mažajame kare“ kariavo tais laikais žmonės, kurie dabar visais būdais stengiasi išnaikinti visą tarybinę praeitį iš Lietuvos istorijos? Atsakyti į šiuos klausimus gali šiuolaikinės Lietuvos susiformavimo liūdytojai, kurie dėl savo geros atminties turėjo bėgti iš šios demokratinės, europietiškos šalies. Vienas tokių žmonių – filosofijos mokslų daktaras Valentin LAZUTKA, perestroikos laikais – Filosofijos instituto direktorius, Lietuvos TSR Mokslų akademijos partinio komiteto sekretorius ir kurį laiką Aukštosios politinės mokyklos rektorius, kur tuo metu dirbo dabartinė Lietuvos prezidentė Dalia Grybauskaitė. Gresiant mirčiai 1991 metais Valentin Lazutka paliko naująją Lietuvą, iš pradžių išvyko į Vokietiją, o paskui apsigyveno Baltarusijoje. Nepaisant to, kad V. Lazutka dabar stengiasi vengti pašalinių kontaktų, po ilgų paieškų mums pavyko susitikti Minske. Jūsų dėmesiui šio pokalbio tęsinys (pradžia čia):

- Pone Valentinai, peršasi išvada, kad KGB atliko svarbų vaidmenį, naikinant TSRS ir kuriant naujas valstybes, tame tarpe ir Lietuvą?

Aš asmeniškai matau tokią struktūrą. Tarp dviejų organizacijų – Komunistinės partijos ir KGB – vyko kova už valdžią. O rezerve ir vieni, ir kiti turėjo kariuomenę, kuria galėjo pasinaudoti kiek Kompartija, tiek ir KGB. Kariuomenei sugriauti, diskredituoti buvo rengiamos tokios akcijos kaip lėktuvų skrydžiai ties Kremliaus ir kitos. Žūdavo maršalai, nutraukdavo savo gyvybes. Taip buvo nutolinta kariuomenė.

Pavyzdžiui, Brazauskas niekaip negalėjo priklausyti nuo KGB. Tačiau visai kas kitka, kiekvienas CK sekretorius ir kiti pastoviai turėjo reikalų su KGB. Sakykim, aš – instituto direktorius turėjau mane kuruojantį asmenį iš KGB. Aš negaudavau iš KGB nei informacijos, nei užduočių, tačiau turėjau bendradarbiauti su jais tam tikrais darbo klausimais. Tokio kuratoriaus nebuvo partinėje mokykloje, nebuvo jo ir CK arba rajonų komitetuose. Bet jie buvo Mokslų akademijoje.

Kai iškilo šis klausimas, aš pats pasiskambinau naujam respublikos KGB pirmininkui ir susitariau dėl susitikimo. Jis sutiko. Sutarėm. Aš susitikau su juo, ir mes labai atvirai pasikalbėjome. Aš sakau: „Kaip gi taip gali būti? Jūs, tarybiniai žmonės, dabar paklūstate Landsbergiui“. Jis man sako: „Įsimink: viskas, ką mes darome, mes darome Maskvos nurodymu. Aš gaunu įsakymus iš savo valdžios Maskvoje, o man įsakyta aptarnauti Landsbergį, su jumis iš vis jokių reikalų neturėti, jokios informacijos apie jus nerinkti“.

Aukščiausiuose valdžios sluoksniuose Maskvoje kūrėsi penktoji kolona, atėjo Kriučkov (1988 m. lapkričio 1 d. Vladimir Kriučkov tapo TSRS KGB pirmininku, o 1989 m. rugsėjo 20 d. – TSKP CK Politbiuro nariu – RuBaltic.ru past.). Viskas ėjo iš Maskvos – iš Jakovlevo, Gorbačiovo.

- Greičiausiai, po Komunistų partijos skilimo daug kas dvejojo, su kuo likti? Ta pati Grybauskaitė išėjo atostogų ir kuriam laikui dingo...

Ji taip pasiėlgė tam, kad nedalyvauti visuose riejimuose. Rektorius atsigulė į ligoninę, o ji neturėjo ką veikti ligoninėje – išvyko į sanatoriją.

- Tai buvo lietuviai-emigrantai?

Taip, iš tų, kurie 1944 metais paliko Lietuvą kartu su vokiečiais. Mes jau tada tiksliai žinojome, kad Landsbergis – Amerikos kadras. O Prunskienė, tarp kitko, Europos. Ji mokėsi Vokietijoje, ten apsigynė daktaro disertaciją. Ji turėjo savo ryšius.

Europiečių pozicija šiek tiek skirėsi nuo amerikiečių. Kiek Miteranas, tiek ir Kolis buvo skuboto Vokietijos susijungimo proceso priešininkais. Po susijungimo VFR jau pajuto, ką tai reiškia, todėl visai nenorėjo papildomo krūvio Pabaltijo pavidalu. O amerikiečiai skubėjo išspręsti užduotį – sugriauti TSRS. CŽV palaikė skubų sugriovimą, chaosą, nes jų planuose buvo ne tik TSRS sunaikinimas, bet ir Rusijos sugriovimas, jos išskaidymas. Štai kodėl viskas tai įvyko Lietuvoje, kuri atrodė mažu lopinėliu, veidrodžio skeveldra. Kai prasidėjo amerikiečių kova su europiečiais, be jokių abejonių Prunskienę nušalino (1990 metų kovo mėnesį Prunskienė pradėjo vadovauti Lietuvos vyriausybei, o 1991 metų sausio mėnesį atsistatydino – RuBaltic.ru past.). Valdžią visiškai perėmė landsbergistai.

- Prunskienė atsistatydino likus visai mažai laiko iki 1991 m. sausio 13 d. įvykių. Ką Jūs prisimenate iš tų įvykių prie televizijos bokšto?

Pradėsiu iš tolo. 1991 metų sausio 1 d. mūsų pirmasis sekretorius sušaukė CK Biuro posėdį. Pagrindinis klausimas buvo toks: skambino Gorbačiov ir kreipėsi su pasiūlymu įvesti Lietuvoje prezidento valdymą. Mes aptarėme.

Jokių konkrečių įvedimo rengimų ar užduočių mes negavome, šia tema kalbos pasibaigė. Tame pačiame Biuro mūsų pirmasis sekretorius pranešė, kad Maskvoje, TSKP CK, vyks pasitarimas, į kurį pakviesta mūsų partijos atstovų grupė, kuriai vadovauti paskirtas Lazutka, tai yra aš. Išvažiuoti turime jau rytoj, nes sausio 3 dieną privalome būti Maskvoje. Taip aš ir atsidūriau Maskvoje.

Pasitarimas įvyko. Išvykimo dieną – tai buvo sausio 6 – netikėtai man skambina prezidento padėjėjas ir sako, kad rytoj 11 valandą mane nori matyti Gorbačiov. „Gerai, tada aš šiandien nevažiuoju, grąžinu bilietą, ryt būsiu 11 valandą“. Ateinu pas padėjėją, jis man sako: „Mes laukiame, tuoj turi atvažiuoti jūsų Ministrų Tarybos pirmininkas. Kai jis atvažiuos, tada į šį pasitarimą pakvies ir tave. Reiškia, lauk“. Sėdėjau iki 15 valandos. Kas ten nutiko? Pirmininkas neatvažiavo. Vienu žodžiu, pas Gorbačiovą aš taip ir nepatekau.

Aš išvažiavau į Vilnių. Ateinu į miesto komitetą, ir man sako, kad prie Seimo vyksta demonstracija. Kame reikalas? Praneša: „Jūs žinote, kad vyriausybė išformuota, atleista? Prunskienė jau nebe ministrė pirmininkė“. Pagalvojau: „Na, tada aišku, kodėl ji neatvažiavo“. Reiškia, vakar atleido. O ką, Gorbačiov nežinojo? Niekam nepranešė? Kame reikalas? Pasirodo, Gorbačiov paskyrė susitikimą ne su Prunskiene, o su buvusiu paskutiniu Tarybų Lietuvos Ministrų Tarybos pirmininku Sakalausku, kuris tuo metu dirbo ambasadoje kažkur Afrikoje (Vytautas Sakalauskas ėjo Lietuvos TSR Ministrų Tarybos pirmininko pareigas nuo 1985 iki 1990 metų, 1990-1991 metais dirbo TSRS ambasadoje Mozambike patarėju-pasiuntiniu ekonomikos klausimams – RuBaltic.Ru past.). Buvo ištremtas ten.

Penktadienį, sausio 11, pas mane į miesto komitetą atvažiuoja Burokevičius (Lietuvos Komunistų partijos TSKP platformoje Pirmasis sekretorius 1990-1991 metais – RuBaltic.Ru past.). Mes išeiname iš kabineto į lauką, savo kabinetuose mes niekada nekalbėjome slaptomis temomis. Ir jis man sako: „Skambino Gorbačiov ir pasakė, kad Sąjungos Taryba pasisakė prieš prezidento valdymo įvedimą“. Aš sakau: „Na ką gi, reiškia šeštadienį-sekmadienį mes laisvi“. Mes seniai neturėjome išeiginių. Išvažiavau į savo sodą, kur buvau maždaug iki 4 valandos. Vėliau mes su žmona grįžome namo. Atvažiavome, o anyta man sako, kad skambino mūsų pirmojo sekretoriaus sekretorė – skubiai reikia atvykti į CK.

Žmona nuvežė mane į CK. Ateinu – tuščia, visiškai nieko nėra. Įeinu į priimamąjį. Sekretorė sėdi ir sako: „Burokevičiaus nėra, jūs pasėdėkite, palaukite, jis ateis“. Gerai, atsisėdau laukti. Laukiu. Gerai, ko aš sėdėsiu? Eisiu į savo kabinetą – sekančiame aukšte CK sekretoriaus kabinetas. Staiga iš kažkur išdygsta keturi vaikinai, gero sudėjimo, atsistoja prie durų ir kartoja tą patį: „Ne, prašome palaukti čia“. Nesimušti gi man su jais. Atsisėdau, sėdėjau 10 minučių, ryžtingai atsistojau, prašau „praleiskite!“. Tada mane iš priimamojo išleido, palydėjo į tuščią kambarį priešais ir uždarė. Maždaug nuo penktos valandos iki 22:30 sėdėjau ten. Telefono nėra. Aš prašiau leisti paskambinti į namus. Negalima. Neva viskas daroma Burokevičiaus įsakymu. Paskui apie 23:00 staiga įbėga sekretorė: „Skambino Burokevičius, pasakė, kad į CK neatvažiuos, jūs laisvas“. Kaip – laisvas, aš galiu eiti namo? O kur norite, ten ir eikite, sako.

Kai išėjau iš šio kalėjimo, prie manęs pribėgo visa mūsų darbuotojų minia. Pirmieji – mano miesto komiteto sekretoriai, antrasis ir trečiasis. Paskui rajonų komitetų sekretoriai. Visi puolė mane su žodžiais: „Ką jūs su mumis darote? Mus trečią valandą pasodino salėje, mes sėdim, mus neišleido iš salės!“. „Kas jus pasodino?“ – klausiu. „Na, sakė, kad jūs mus sukvietėt“, - atsako. Draugai, aš jūsų nekviečiau, neturiu supratimo, sakau. Pasirodo, miesto komitete taip pat salėje surinko partijos aktyvą. Daugiausia draugovininkus. Taip pat neva mano įsakymu. Aš visiškai nieko nežinojau. Susirinko, apsibarė. Burokevičių iškeikė visokiausiais žodžiais, nes visi sakė, kad tai jo įsakymu vyko.

1991 m. sausio 13. Atėjome mes į miesto komitetą, ten pilna žmonių. Nusiunčiau antrąjį sekretorių, lai aiškina, nes aš eiti nenoriu. Ateinu į savo kabinetą. Prie mano stalo sėdi pulkininkas Šurupov. „Nieko sau, mes jau turim pirmąjį sekretorių?“ Nesutinka. O ko jūs čia, klausiu. O mes, sako, ruošiamės įteikti peticiją Seimui ir ministrų kabinetui. Nustebau: „Išprotėjot? Ką jūs rasit ten vidurnaktį?“ Ne, sako, laikas suderintas su Landsbergiu. Landsbergis sakė ateiti 12 valandą.

Ir štai šitos dvi grupės iškeliavo – viena į Ministrų Tarybą, kita į Seimą. Ėjusi pas Landsbergį Seiman ramiai nuvyko ir įteikė. O kita, kuri ėjo į Ministrų Tarybą – dalį jų ten sučiupo, sumušė; kiti atbėgo pas mane į miesto komitetą. Keletą sumuštų žmonių nusiunčiau į karo ligoninę su „greitaja“, nes į miesto ligoninę siųsti bijojau. Jie buvo žiauriai sumušti. Pavyzdžiui, vienas, mano sektoriaus vedėjas, mokslų kandidatas net tris menėsius sirgo. Kitą 60-metį sumušė taip, kad jis išėjo į pensiją dėl sveikatos būklės.

Sėdime mes salėje, o tas pulkininkas sako, kad turi būti kreipimasis iš Maskvos dėl prezidento valdymo įvedimo. Kokio prezidento? Kas pasakė? Kol mes sėdėjome, pradėjo šaudyti patrankos. Aš nusiunčiau pirmą pasitaikiusį draugą sužinoti, kame reikalas. Jis ateina ir sako: „Tankai! Šaudo!” Ir iš vis neaišku: minia, kuri saugojo Seimą, nuskubėjo prie televizijos bokšto. Tik tada aš sužinojau apie taip vadinamus „sausio įvykius“. Iš partiečių niekas nedalyvavo, todėl nieko nežinojome.

Staiga man skambina mūsų CK sekretorius generolas majoras Naudžiūnas: „Klausyk, kur tu bivai? O kur Burokevičius?“. O aš nežinau. Kitą rytą aš paklausiau Burokevičiaus: „Kur tu buvai?“ Ten pat, kur buvai tu, atsako, ar ne tavo įsakymas buvo? Juokauji, klausiu, koks mano įsakymas?

Iš tikrųjų, net nežinau, kas sugalvojo tą Tautos gelbėjimo komitetą, kvaila išmonė buvo. O mums tada stipriai pakenkė – ir Burokevičiui, ir kitiems.

- O ką manote apie snaiperius, dėl kurių tiek ginčų?

Yra tikslūs duomenys, o ne vien spėliojimai. Kai buvo išspręstas klausimas dėl radijo ir televizijos, televizijos bokšto kontrolės, apie tai gerai žinojo šalies apsaugos departamento viršininkas Butkevičius. Jis išsikvietė taip vadinamų Lietuvos pasieniečių būrį, pasodino ant stogų – jie ir šaudė. Pats Butkevičius ne kartą tai pripažino. Tiesa, po dviejų metų kalėjime jis staiga prisimenė, kad nesodino. O iki to jis apie tai kalbėjo ne viename interviu. Taip buvo rašoma Lietuvos istorija.

1 dalis

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 7 — id: `scraped:rubaltic_lt:9f405bff0eec1b40`

**Title:** Kaip šiuolaikinė Lietuva atsikratė KGB munduro?

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Nepriklausomos Lietuvos gimimo istorija, tikroji, o ne „laimėtojų“ parašyta, iki šiol lieka paslaptimi. Visuomenei siūlomi iškilmingi pagal protokolą surašyti mitai apie tautos kovą su „sovietinės okupacijos“ jungu už laisvę, tačiau kaip gi „totalitarinės TSRS“ sąlygose į respublikos vadovybę galėjo patekti dabartiniai aršūs Tarybų valdžios niekintojai? Kieno vedami politiškai susidraugavo dabartiniai Lietuvos vadovai? Kokiame būtent „mažajame kare“ kariavo tais laikais žmonės, kurie dabar visais būdais stengiasi išnaikinti visą tarybinę praeitį iš Lietuvos istorijos? Atsakyti į šiuos klausimus gali šiuolaikinės Lietuvos susiformavimo liūdytojai, kurie dėl savo geros atminties turėjo bėgti iš šios demokratinės, europietiškos šalies. Vienas tokių žmonių – filosofijos mokslų daktaras Valentin LAZUTKA, perestroikos laikais – Filosofijos instituto direktorius, Lietuvos TSR Mokslų akademijos partinio komiteto sekretorius ir kurį laiką Aukštosios politinės mokyklos rektorius, kur tuo metu dirbo dabartinė Lietuvos prezidentė Dalia Grybauskaitė. Gresiant mirčiai 1991 metais Valentin Lazutka paliko naująją Lietuvą, iš pradžių išvyko į Vokietiją, o paskui apsigyveno Baltarusijoje. Nepaisant to, kad V. Lazutka dabar stengiasi vengti pašalinių kontaktų, po ilgų paieškų mums pavyko susitikti Minske:

Pone Valentinai, kaip Jūs priėmėt perestroikos pradžią TSRS? Kaip Jūs ją suvokėt?

- 1984 metais aš ėjau Lietuvos TSR Filosofijos, sociologijos ir teisės instituto direktoriaus pareigas. Daugelyje aspektų perestroiką aš priėmiau ganėtinai teigiamai. Pirmiausia, aš asmeniškai pažinojau Raisą Gorbačiovą. Mes kartu vienais metais baigėme MVU (МГУ). Mes mokėmės filosofijos fakultete. Be to, keturis metus mes gyvenome viename bendrabutyje. Su Raisa mane daug kas siejo – ten gyveno mano giminaitė, draugė. Tad buvo ir asmeninis faktorius.

Be to, tada pagaliau atėjo jaunimas, pagaliau visa, taip sakant, „gerontologija“ pasibaigė, ir atrodė, jog mes žengsime greičiau ir taisyklingiau, negu iki tol. Atrodė, kad mums pasibaidė asmenybės-suvienodijimo kultas, ateis nauja vadovybė, gabesnė ir aktyvesnė. O iš pat pradžių Gorbačiovas pasireiškė labai aktyviai.

Kaip aš suvokiau perestroiką? Kaip rašė Gorbačiovas savo knygoje „Naujas politinis mąstymas“: daugiau socializmo, socializmo tvirtinimas ir t.t. Neturėjau jokių minčių apie tautinę nepriklausomybę, atsiskirimą ir išėjimą iš TSRS. Man tai net į galvą neateidavo. Ir aš iki pabaigos laikiausi šių pozicijų. Kai 1988 metais prasidėjo visos šitos rietenos, tada tapo aišku, jog viskas yra labai blogai.

Aš ir tada kariavau už socializmą ir jo vystymąsi. Tai yra, aš nemačiau viso to blogio, kuris slėpėsi perestroikoje.

Perestroikos pradžia teikė daug vilčių. Iš Gorbačiovo girdėjome daug viltingų žodžių. Jau pašnekėti tai jis mokėjo, ir tik tą ir pripažindavo. O jei kalbėti apie veiksmus... Kai atėjo laikas veikti, iš tikrųjų pertvarkyti, čia paaiškėjo, kad visa valstybinė struktūra yra bejėgė, tame tarpe paaiškėjo partijos bejėgiškumas. Tapo aišku, kad mes patekome į labai sunkią padėtį, ir mūsų laukia labai liūdna ateitis. Aš tą pajutau 1988 metais.

1988 metais aš nepalaikiau mitingo, kuris buvo nukreiptas prieš Tarybų valdžią. Aš jame nebuvau. Po to mane kaltino už tai. Rajono komitetas netgi iškėlė klausimą dėl mano nušalinimo nuo Lietuvos Mokslų akademijos partijos komiteto sekretoriaus pareigų ir net dėl mano pašalinimo iš partijos. Tačiau aš laikiausi savo pozicijos, kad mitingas prieš Tarybų valdžią – tai nėra perestroikos palaikymas, o kaip tik atvirkščiai.

Ką Jūs manėte apie Sąjūdį?

- Jūs žinote, kad Sąjūdis buvo sukurtas 1988 metų birželio 3 dieną. Aš buvau tiesiogiai įtrauktas į šį procesą. O buvo taip: birželio 3 man paskambino vyriausias Mokslų akademijos mokslinis sekretorius ir pasakė: “11 valandą Mokslininkų namuose vyks pasitarimas, atvažiuok ten, 11 valandai”.  Šiek tiek nustebau, nes Mokslininkų namai buvo toli už miesto. Kai atvažiavau, ten sutikau vyriausią mokslinį sekretorių, po to visuomeninių mokslų mokslinį sekretorių ir Lietuvos Komunistų Partijos CK sekretorių ideologijai, o taip pat man pristatė vieną nepažįstamą – pristatė kaip TSKP CK Mokslų skyriaus vadovą. Pamaniau, kad pasitarime kalbėsime apie mokslus. Ir iš tikrųjų, keletas pokalbių šia tema buvo, o vėliau staiga viskas pasikeitė, buvo pasakyta, kad priimtas sprendimas įkurti Lietuvoje judėjimą perestroikai palaikyti. Ką gi, sutikau. Matėsi, kad perestroika ėjo ne ta linkme, jau ne perestroika, o “katastroika” prasidėjo. Palaikyti reikėjo perestroiką.

Sutarėm, kad 18 valandą Mokslų akademijoje, mūsų salėje vyks steigiamasis judėjimo susirinkimas. Vyriausiam moksliniam sekretoriui ir man buvo pavesta pirmininkauti susirinkime ir, iš tikrųjų, vadovauti bei kurti visus šitus organus ir kita.

Tačiau gavosi kitaip – aš paskambinau savo draugui ir pirmojo CK sekretoriaus padėjėjui, kuris nukreipė mane į KGB, į vadovybę. Tada kaip tik nebuvo pirmininko. Senasis išėjo, naujasis dar neatėjo.

Kai susisiekiau su kgbistais, po pokalbio supratau, kad iš tikrųjų Sąjūdis įkurtas KGB organais. CK juos taip pat kaip ir palaikį. Na o į visuomenę su šia idėja turėjome išeiti mes, Mokslų akademijos mokslininkai. Po šio pokalbio aš atsisakiau dalyvauti susirinkime ir apskritai tapau Sąjūdžio priešu. O pasipriešinimo Sąjūdžiui baze tapo Lietuvos komunistų partija, kurį skilo ir pasiliko TSKP pozicijose.

Partijos skilimas įvyko 1989 metais. Bet jau tada, 1988 metais, aš mačiau tą vidinį skilimą. Planavome, kad Sąjūdžio pirmininku taps rašytojas Petkevičius.

Pirmajame susirinkime Landsbergis nebuvo išrinktas, liko Petkevičius, tačiau vos praėjus mėnesiui-dviem Lietuvos Komunistų partijos CK Biure Landsbergis buvo paskirtas Sąjūdžio pirmininku.

Kokią tada buvo Landsbergio reputacija?

- Jis labai glaudžiai bendradarbiavo su Valstybinio saugumo departamentu. Tai aišku ir dėl to, kad jo tėvas – senas šios tarnybos darbuotojas. Landsbergis turėjo labai stiprų užnugarį, visą laiką buvo globojamas šios organizacijos, kai mokėsi, kai jį privertė dirbti. Bet kadangi visuomenės akyse tėvas gi buvo profašistinis, jaunesnysis Vytautas du kartus paduodavo prašymą dėl stojimo į partiją ir jo nepriėmė. Pirmą kartą jo kandidatūrą atmetė susirinkimas, antrą kartą susirinkimas pritarė, bet nepraleido Rajono komiteto Biuras. Taip jis ir netapo partijos nariu, nors buvo komjaunuoliu. Tokia vat sudėtinga jo biografija.

Mano brolis dirbo Lietuvos Kompartijos CK mokslų skyriaus vedėju. Jis pasakojo, kad kai iš Australijos atvyko Landsbergis-vyresnysis, KGB ėmėsi jį šefuoti ir planavo paskirti jį vyriausiuoju Vilniaus architektu.

O už kokius nuopelnus Landsbergį-vyresnįjį norėjo paskirti vyriausiuoju Vilniaus architektu?

- Jis neblogas architektas, be to, vis dėlto jis atvyko, turėdamas didelius nuopelnus: buvo KGB agentu Lietuvos Laikinojoje vyriausybėje, kuri iki vokiečių okupacijos valdė šalį mėnesį ar pusantro. Jis buvo šioje vyriausybėje. Jo parašas yra dviejuose padėkos laiškuose Hitleriui už Lietuvos išvadavimą, o vėliau jis su šeima išvažiavo ir grįžo. Karo metais jie iš Vienos persikėlė į Vokietiją. Kai jau prasidėjo karas, jie perėjo į amerikiečių sektorių, buvo Amerikoje, po to atsidūrė Australijoje. Jis dirbo KGB. Ne koks nors agentas, o etatinis darbuotojas. Jis turėjo laipsnį ne žemesnį už KGB pulkininko. Tarp kitko, jis dirbo ne Lietuvos KGB, bet centriniam. Jam vadovavo iš Maskvos. Kai jis jau sugrįžo, spaudimas ėjo būtent iš Maskvos.

Po to, be abejo, jo nepaskyrė vyriausiuoju architektu. Jis grįžo į Kauną, ten jam grąžino jo buvusį trijų aukštų namą-vasarinę pilnon nuosavybėn, skyrė didelę pensiją ir paskyrė architektūros instituto mokslo darbuotoju. Tai kas liečia tėvo.

O su Landsbergiu-jaunesniuoju aš dar buvau susidūręs. Aš pirmininkavau Vilniaus daktarų disertacijų gynybos mokslinėje taryboje, todėl turėjau ryšį su Aukščiausiaja atestacine komisija. Tuo metu skyriaus viršininku ten dirbo mano buvęs kursiokas ir studentavimo laikais labai geras draugas Grigorij Kvasov. Kartą susitikę pas jį namuose jis paklausė: „Klausyk, ar tu pažįsti tokį Landsbergį?“ Jis tada buvo visiškai nežinomas. Atsakiau, kad jo nepažįstu, bet žinau jo tėvą, na ir papasakojau, kas tėvas. Kad KGB darbuotojas, kuris didelę tarnybą praėjo, turi savo nuopelnus ir kita. Jis man ir sako: „A-a-a, tada aišku, kodėl ši organizacija taip mus spaudžia, kad suteiktumėm jam profesoriaus laipsnį“. Nes jis neturėjo jokio tam pagrindo. Jis buvo mokslų kandidatas. Jokių publikuotų mokslinių darbų jis neturėjo. Visiems kilo klausimas, kaip jis taip staiga gavo profesoriaus laipsnį?

Reiškia, iki Sąjūdžio įkurimo Landsbergis mokslinėje erdvėje ypatingo autoriteto neturėjo?

- Na jis labiau prisiplakė prie meno bohemos, buvo pianistu. Praktiškai jis ėjo docento pareigas konservatorijoje, vėliau marksistinės estetikos profesoriaus. Toks kursas buvo – marksistinė-lenininė estetika. Jis jį ir skaitė, vedė konservatorijoje.

Perestroika nuo to ir prasidėjo. Inteligentija, Petkevičius, žymus poetas Marcinkevičius, kurie iš pradžių entuziastingai, maždaug kaip aš, įsitraukė į perestroiką, paskui visiškai pasitraukė, tapo perestroikos priešais. Petkevičiaus romanas rodo jo požiūrį į Landsbergį ir Sąjūdį (Vytauto Petkevičiaus knygą „Durnių laivas“ galima perskaityti čia – RuBaltic.Ru past.)

Jūsų nuomone, ar perestroika nuo pat pradžios buvo sugalvota kaip „katastroika“?

- Manau, kad pradžioje Michail Gorbačiov ir Raisa Gorbačiova šventai tikėjo socializmu. Lūžis įvyko, kai tam tikros jėgos pradėjo labai aktyviai dirbti su Gorbačiovu. Pavyzdžiui, jo geriausias draugas ir kursiokas buvo Zdenek Mlynarž, čekas, kuris Dubčeko laikais buvo jo pagrindiniu ideologiniu ruporu, Tarybų valdžios priešu, jei norit. Visais laikais jis buvo geriausias Gorbačiovo draugas, atvažiuodavo pas jį į Stavropolį. Kai Gorbačiovas vedė Rają, jis buvo tamada jų vėstuvėse. Aršus toks Tarybų valdžios ir komunistų priešas, kuris ypatingai veikė Raisą. Toks tam tikras nusistatymas pas Gorbačiovus buvo nuo studentavimo laikų.

O šiaip tai Gorbačiov vos baigė mokyklą. Po jos baigimo net nebandė kur stoti. Bet vyko derliaus nuėmimo kampanija; jo tėvas dirbo rajono komitete ir nukreipė sūnų kombainininko padėjėju. Šio darbo dėka per vieną sezoną Gorbačiov užsitarnavo Garbės Ordiną. Kaip ordininką srities komitetas (obkomas) komandiravo jį studijuoti teisę Maskvos universitete. Reikia pabrėžti, kad Raisa atliko didžiulį darbą, keliant jo išsilavinimą. Ji dviem galvom aukščiau už jį buvo. Apsiskaitųsi mergaitė, pirmūnė visais atžvilgiais. Ji netgi mokė Gorbačiovą rašybos, nes jis rašydamas pridarydavo siaubingų klaidų. Raisa iš jo sulipdė tai, ką sulipdė. Kas ką besakytų, bet jis be Raisos negalėjo nei kur nuvažiuoti, nei nueiti. Ji jam pastoviai vadovavo. Pamenu, Vilniuje Brazauskas surengė jiems atsisveikinimo vakaronę. Štai pakėlė taures. Gorbačiov sako: „Na taip, dabar galime ir išgerti“. Tuoj pat Raisa: „Miša, tau negalima“. Jis be žodžių: viskas, negalima. (juokiasi) Toks pavyzdys. Ten daug žmonių buvo.

Įdomus gaunasi Jūsų Landsbergio portretas. Bet juk jis greičiausiai politinis prezidentės Grybauskaitės auklėtojas.

- Taip, jis ją paskyrė, jis ją prastūmė...

Iš pradžių Grybauskaitė atvyko į partinę mokyklą vadovaujama rektoriaus Sigizmundo Šimkaus. Ji atėjo kaip ekonomikos kabineto vedėja. Tuo pačiu Šimkus ją paskyrė mokyklos tarybos sekretore. Visa dokumentacija ėjo per jos rankas, į ją kreipėsi, bandė pagreitinti, spręsdavo, kur nusiųsti, ir t.t.

Jie susipažino KGB pagrindu, kadangi Grybauskaitės tėvas taip pat bendradarbiavo su šia organizacija, bet jis buvo gaisrininku. Jie tiesiog negalėjo nesusipažinti, nes iš KGB galėjo paprašyti: „Paimk tokį darbą, čia reikia sutvarkyti“. Ji grįžo iš Leningrado, o KGB užsiėmė jos įdarbinimu. Tokiu būdu ji ir perėjo į partinę mokyklą. Todėl, kai nuo 1988 metų prasidėjo sumaištis, ji dingo, o staiga mes sužinojome, kad mūsų Dalia kažkodėl dirba TSRS ambasadoje JAV. Bet ji dirbo ten trumpai – ją atšaukė. Po to staiga ji vėl pradingo. Paaiškėjo, jog ji mokosi viename Amerikos universitete. Šiame universitete veikė mokykla, kurioje mokėsi „sąjūdininkų“ valdančioji dalis – Butkevičius ir kiti. Taigi ji praktiškai baigė CŽV mokyklą.

Juk visas KGB koks buvo, toks ir liko. Atkreipkit dėmesį, niekas nelietė kgbistų. Jų nepersekiojo. Kai kuriuos, rusus, dar kažkaip nušalindavo, o pagrinde niekas nelietė. Miesto centre buvo namas, kuriame gyveno antrasis Lietuvos Kompartijos CK sekretorius. Po jo mirties name apsigyveno KGB pirmininkas, įkūręs Sąjūdį. Naujai valdžiai atėjus buvę ir dirbantys bendradarbiai dirbo kartu, klestėjo pilnumoj. Tie patys žmonės ir dabar.

Dar iki Leningrado KGB jau kuravo Grybauskaitę. Ji buvo konservatorijos personalo skyriaus darbuotoja, o personalo skyrius kartu ir specialusis skyrius. Atskiro specialiojo skyriaus nebuvo. Specialusis skyrius – tai KGB. Tai yra, ji jau tada dirbo KGB, ir jau tada jai vadovavo. Į Leningradą ji pateko atitinkamai KGB padedant bei rekomenduojant.

Beje, amerikiečiai buvo paskelbę Grybauskaitę persona non-grata kaip buvusę KGB darbuotoją. Be Valstybės saugumo departamento palaiminimo ji negalėjo dirbti Vašingtone. Čia jau jokių kalbų negali būti. Ji praėjo per KGB.

O vėliau, po TSRS, ji vėl atsidūrė Vašingtone. Ji ten dirbo ir tuo pačiu metu mokėsi – ėjo kursus, pasiruošimą. Manau, svarbiausi buvo kursai. O savo požiūrį į Grybauskaitę JAV pakeitė Landsbergiui rekomenduojant.

2 dalis

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 8 — id: `scraped:rubaltic_lt:94358f22e6a14d4d`

**Title:** Tarybų išpera: kokius TSRS paminklus Lietuvai būtina kuo skubiau sunaikinti

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Ryšium su tuo, kad Vilniuje neseniai demontavo Žaliojo tilto skulptūras, skambant Lietuvos sostinės mero Remigijaus Šimašiaus bravūrui apie tarybinius „balvonus“ feisbuke, analitinio portalo RuBaltic.Ru redakcija nusprendė pagelbėti kaimyninei Lietuvai ir parinkti TSRS paminklus, kuriuos artimiausiu metu būtina sunaikinti, sutrypti ir išjuokti, kaip Lietuvos valstybės grėsmę: Žaliasis tiltas Ačiū Dievui, skulptūras nuėmė. Bet Vilniaus gyventojų atmintyje vis tiek dar ilgam išliks šios bauginančios savo tarybine ideologija skulptūros, o grindinys ir likusieji skulptūrų pamatai kels prisiminimus apie jas. Tad tiltą reikėtų sugriauti ir pastatyti iš naujo. O idealiausia būtų dar ir perdažyti vaivorykštės spalvomis – jei jau modernizuoti, tai modernizuoti. Lietuvos Respublikos Seimo pastatas Seimo kompleksą sudaro trys pastatai, kurie buvo pastatyti XX amžiaus 7-ame dešimtmetyje vietoje būvusio jaunimo stadiono „Žalgiris“, t.y. dar TSRS laikais ir už tos šalies pinigus, todėl laisvuosius lietuvius giliai žeidžia faktas, kad nepriklausomos ir demokratinės Lietuvos parlamentarai posėdžiauja tarybiniame pastate. Galų gale, pati pastato atmosfera gali įtakoti parlamentarų sprendimams, jų darbui. Matyt, dėl to 2007 metais buvo pastatyta nauja posėdžių salė, o senąją naudoja šventinėmis, ženkliomis dienomis, o tai betvarkė. Todėl siūlome naujai išrinktajam merui parodyti iniciatyvos ir ištaisyti esamą padėtį. Operos ir baleto teatras Teatras pastatytas 1974 metais. Žmogus negali dvasiškai augti bei tobulėti teatre, kurį pastatė girti, vagiliaujantys statybininkai, kuriuos viršininkai varydavo į darbą. Jautri pono Šimašiaus nosis, kurią jis laiko visada pavėjui, greičiausiai jaučia esančią ten slogią atmosferą bei išgėrusių darbininkų kvapą, kuris iki šiol neišsisklaidė... Klaipėdos uostas Be abejo, jei įsigilinti į uosto istoriją, tai kažkas panašaus čia buvo dar XIII amžiuje. Tačiau tarptautinė perkėla buvo pastatyta 1986 metais, todėl šią uosto dalį teks sugriauti ir sulyginti su žeme. Kitaip šis tarybinis priminimas gali sužadinti darbininkams norą gerti ir vogti. Mikrorajonas Lazdynai Pradėsim nuo to, kad iš vis daugumą Vilniaus mikrorajonų pastatė Tarybinė valdžia ir jų reikėtų atsikratyti. O pradėti vertėtų nuo Lazdinų mikrorajono – reikia pakeisti jo pavadinimą ir sudeginti. Maža to, kad pats mikrorajono pavadinimas įtakotas lenkų (XIX amžiuje čia buvo lenkų kaimas), tai dar ir Tarybų valdžia pastatė šį mikrorajoną. Vėl gi, statė vagys-statybininkai, o projektavo, matyt, bailiai architektai, inžinieriai. Dar blogiau, 1974 metais rajonui suteikta Lenino premija, ir iki 1986 metų tai vienintelis gyvenamojo komplekso projektas, gavęs šią premiją. Taigi vėliau reikėtų išvalyti šios vietovės atmosferą. Televizijos bokštas Vilniaus televizijos bokštas pastatytas 1980 metais. Tikriausiai, tai vienas pavojingiausių Lietuvos statinių. Televizijos bokštas yra tokio aukščio, kad jį galima pamatyti praktiškai iš bet kurios Vilniaus vietos. Baisiausia, kad jis siejamas su laisvės simboliu, o tai melas, nes visi prisimena, kad tarybinių laikų statinys priimtas eksploatacijon taip pat TSRS piliečiais. O dar baisiau, tai dar ir turistų lankoma vieta, o kas bus, jei užsieniečiai asocijuos Lietuvą su tarybiniu projektu? Todėl būtina imtis tam tikrų priemonių nedelsiant. Ignalinos AES Negalima praleisti ir Ignalinos atominės stoties. Be abejo, didelis pliusas, kad imtasi priemonių uždaryti tarybinę AES, kuri yra Černobylio kopija. Bet dar liko 142 kelių kilometrai, 50 geležinkelio kilometrai, 390 ryšio linijų kilometrai, 334 elektros linijų kilometrai, 133 km kanalizacijos, 164 km šiluminių vamzdžių – ir visa tai padaryta Ignalinos AES statybos metu, todėl taip pat turi būti demontuota. Remigijus Šimašius Reikėtų prisiminti, kad Vilniaus meras ne tik gimė TSRS, bet dar ir gyveno ten, mokėsi. Jo tėvai buvo Tarybų Sąjungos piliečiai. O tai reiškia, kad ponas Šimašius užaugo toje atmosferoje, ir nori jis to, ar nenori, jame tebegyvuoja tarybinis mąstymas, ideologija. Jis gali numoti ranka, bet karas su senosios tvarkos šalies praeitimi, istoriniu paveldu – tai tikrai tarybinė atgyvena. Todėl sunku įsivaizduoti, ką su savimi darys meras, kai suvoks savo „tarybinę“ esmę...

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 9 — id: `scraped:rubaltic_lt:4f7f09fd219cedf4`

**Title:** Rusijos Ambasadorius Lietuvoje – apie Maskvos Namų projektą: «Vilniaus gyventojai turi atlikti savo vaidmenį šiame klausime»

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Neseniai naujas Vilniaus miesto meras Remigijus Šimašius Lietuvos žiniasklaidoje išreiškė savo abejones dėl Maskvos Namų statybos Vilniuje ir pažymėjo, kad Rusija neva vilkina Vilniaus Namų statybą Maskvoje. Rubaltic.Ru portalas kreipėsi į Nepaprastąjį ir Įgaliotąjį Rusijos Ambasadorių Lietuvoje Aleksandrą Udaltsovą su prašymu išaiškinti Rusijos poziciją šiuo klausimu: - Jūsų Prakilnybe, pone Ambasadoriau, papasakokite, kokia iš tikrųjų yra situacija su Vilniaus Namų Rusijoje klausimu ir analogišku Maskvos Namų projektu Lietuvos sostinėje? Kas apsunkina abiejų projektų realizaciją? - Aš skaičiau Remigijaus Šimašiaus interviu žiniasklaidoje, tačiau mūsų susitikimio metu, vykusio liepos 7 dieną, jis nepaviešino panašių skeptiškų pamąstymų. Remigijus Šimašius domėjosi mūsų šios situacijos vertinimu. Savo požiūrį aš jam išsakiau, nors ir pabrėžiau, kad vis dėlto tai – Vilniaus bei Maskvos namai, todėl čia tarpusavyje turėtų aiškintis merijos. Tuo pačiu aš pasiruošęs visapusiškai talkinti jų bendradarbiavimui. Iš tikrųjų, šiam projektui jau dešimt metų. Jo dviejų dalių realizavime skiriasi greičiai. Mes, turiu omenyje Rusiją, žengėm į priekį, nors ir buvo visokiausių sunkumų. Bet jau yra visas pastatas ir aiškiai nustatyti mėnesiai, kada bus baigti statybos darbai – blogiausiu atveju tai kitų metų vidurys. Lietuviškų namų projektas Maskvoje kolkas atsilieka. Sutinku, šioje situacijoje yra kiek objektyvių, tiek ir subjektyvių problemų, tai aš pabrėžiau kalbant su meru. Situacijos esmė yra ta, kad anksčiau Lietuvos pusė neskyrė šiam projektui ypatingo dėmesio. Todėl taip ir nutiko su rangovais, su žemės sklypo forminimu. Dabar padėtis pasikeitė, be to būtent Maskvos merija pradėjo įdėmiau stebėti šį procesą ir žengti žingsnius, kuriuos turėjo žengti. Šiandien mes matome, kad ir Lietuva susidomėjo šiuo projektu. Vilniaus Namai bus Chodynskaja gatvėje, tai centrinė administracinė Maskvos apygarda, mūsų supratimu tai – pats centras, vieta tikrai gera. Šiai dienai mes susitarėm taip: jie sprendžia visus klausimus, kuriuos turėjo išspręsti seniai, o mes įvykdysim savo įsipareigojimus. Manau, meras tai priėmė supratingai. Toliau mes kalbėjome apie tai, kad šią problemą reikia spręsti bendromis jėgomis, užbaigti iki galo, o ne trukdyti, nes tai neigiamai veikia abiejų sostinių gyventojų interesus. Aš papasakojau merui, kad man einant Rusijos Ambasadoriaus pareigas Latvijoje (1996-2001 m. – RuBaltic.Ru past .) Rygoje atsidarė Maskvos Namai. Jie puikiai veikia, žmonės lankosi koncertuose, parodose, vaikai lanko būrelius, yra biblioteka ir turizmo agentūra, o tai reiškia, kad tokio pobūdžio projektai tikrai reikalingi ir svarbūs. Visumoje keitimasis nuomonėmis su meru šiuo klausimu paliko man teigiamą įspūdį. Tie, kas šiandien vis politikuoja, vėliau turės atsakyti už savo sprendimus, kurie prieštarauja žmonių interesams. Mums svarbu nenueiti šiuo keliu. - Jūsų nuomone, iš Lietuvos pusės šis klausimas nėra politizuojamas? - Be abejo, politizuojamas. Šiandien mūsų santykiuose su Lietuva nebėra tokių klausimų, kurie nebūtų kieno nors politizuojami. Pavyzdžiui, mane stipriai nustebino mūsų su ponu Šimašiumi pokalbio rezultatų pateikimas Lietuvos žiniasklaidoje, tai kaip tik ir yra vienas iš to politizavimo pasireiškimų. - Ar Vilniaus vadovybės kaita turėjo įtakos projektui, ar atsirado naujų sunkumų, kai meru tapo Šimašius,o gal atvirkščiai jis pragmatiškesnis meras, negu jo pirmtakas Zuokas? - Dabar dar anksti apie tai kalbėti. Jis neseniai pradėjo eiti pareigas, ir aš palinkėjau jam sėkmės. Mano nuomone, jis labai perspektyvus politikas, draugingas ir malonus pašnekovas, stengiasi įsigilinti į klausimo esmę, ir man tai patinka. Mano pokalbis su meru – tai žingsnis tolimesnio bendradarbiavimo link, jis turi geriau suvokti mūsų požiūrį, o toliau jau merijos turi bendrauti tiesiogiai, kad užbaigti šį įdomų, abipusnaudungą ir, kaip man atrodo, abiem pusėm reikalingą projektą. - Šiandien tiesioginiai kontaktai tarp Vilniaus ir Maskvos merijų, kiek matau, nėra labai aktyvūs… - Tai atskiras klausimas. Čia Lietuva turi savaiminius ribotuvus kontaktuose su Rusijoje, pirmiausia – politiniame lygmenyje. Tokia dabar jų politinė kryptis, ir mes, be abejo, nenorime joje dalyvauti. Ir su meru mes apie tai taip pat kalbėjome, mes abu manome, kad sostinių ir kitų miestų merijų lygyje, kitų sferų darbo lygmeniuose reikia palaikyti kontaktus ir spręsti klausimus. Aš papasakojau ponui Šimašiui, kad net sankcijų sąlygose Rygos merija, pavyzdžiui, atranda tas sferas, kuriose gali bendradarbiauti su Maskva, ir jos yra nepaprastai naudingos Latvijos sostinėje. Politika yra viena, o miesto gyvenimas – tai žmonių gyvenimas. Ypač tokiuose dideliuose miestuose, kaip Maskva, didmiesčiuose. Tai – atskiras klausimas. Ji reikia spręsti, nes tai liečia pirmiausia žmonių poreikius – šių miestų gyventojus. Yra tokia sąvoka – Rusijos mokslų ir kultūros centras. Nuo Vašingtono iki Sidnėjaus mes jų turime daug, bet tokiam centrui atidaryti būtinas susitarimas tarp vyriausybių, atitinkamo lygio politinis sprendimas. O Maskvos ir Vilniaus Namai – tai regioniniai ryšiai, tai kitas lygmuo, ten nėra ir nebus politikos, tai bus ekonominiai bei kultūriniai ryšiai, vaikų būreliai, bibliotekos. Visa tai normalu ir neprieštarauja geros kaimynystės logikai. Prie Lietuvos Ambasados Maskvoje seniai veikia Jurgio Baltrušaičio Namai. Lietuvos Ambasadorius ponas Motuzas ne kartą kalbėjo apie tai, kad šiame centre 2-3 kartus per mėnesį jie organizuoja stambius renginius Rusijos visuomenei, tai nėra klumas, kurį aptarnauja tik ambasada, jis veikia visiems Maskvos gyventojams. Tai projektai, kuriuos Lietuvos pusė jau įgyvendina, kodėl gi mums nepadarius tai dvišaliu reiškiniu? - Reiškia, galime tikėtis, kad nugalės pragmatiškas požiūris. - Kaip diplomatas aš tik tuo ir viliuosi. Manau, Vilniaus gyventojai taip pat turi atlikti savo vaidmenį šiame klausime.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 10 — id: `scraped:rubaltic_lt:2961025f01569611`

**Title:** Kremlius Lietuvoje vykstančiuose rinkimuose dės viltis į Grybauskaitę

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Dalia Grybauskaitė prezidento rinkimų maratone išlaiko lyderės pozicijas, turėdama nepalenkiamo kovotojo su „Maskvos aštuonkoju“ įvaizdį. Visgi įdėmiau pažvelgus, tampa aišku, kad tai tėra propagandinė klišė. Iš tikrųjų Grybauskaitė ­ Kremliui naudingiausias dabartinių prezidento rinkimų nugalėtojas.

„Arba Grybauskaitė, arba Rusija sulygins su žeme mažą Lietuvą“,- su šiuo pagrindiniu šūkiu dabartinis Lietuvos prezidentas vykdo savo 2014 metų rinkimų kampaniją. Tiesa, tai labiau primena senelio Lansbergio, įstrigusio savo sąmone audringoje sajūdžio jaunystėje, pasakas. Vertinant politinį Grybauskaitės profilį pragmatiškai, pasirodo, kad viskas kaip tik atvirkščiai ­ „mėlynos damos“ perrinkimas pilnai atitinka Rusijos politikus interesus.

Jeigu neginčyti šios tezės, tai viskas stojasi į savo vietas. Pavyzdžiui, kompromato ir kitų „atakų“ prieš Lietuvos prezidentą nebuvimas. Nežiūrint į daugkartinius gąsdinimus apie Lubiankos koridoriuose ruošiamą melą ir purvą konkrečiai Grybauskaitei, jokių skandalingų jos gyvenimo smulkmenų nebuvo perteikta.

Tampa aiškiau suprantamas dujų kainos sumažinimas Lietuvai. Derybos vyko keletą metų, o baigėsi likus vos kelioms dienoms iki rinkimų – kaip tik liko laiko, kad Grybauskaitė išdidžiai įsirašytų į savo aktyvą naują pergalę prieš „priešą“, o visi likę gyventojai apsidžiaugtų sutaupę papildomą litą ir nueitų balsuoti. Nejaugi Aleksejus Mileris, „Kremliaus dujų žudikas“, negalėjo palaukti savaitę ir nedovanoti Grybauskaitei tokios dovanos prieš rinkimus?

Pagaliau, sunku paaiškinti šį faktą, kad prezidentei vos ne NATO aulu daužant per tribūną ir grasinant parodyti „Kuzkino motiną” kaimyninei Rusijai, Maskvoje tarsi nepastebi: nei atsakomo aštrumo, nei notos, nei pasiuntinio iškvietimo ant kilimėlio. Bijo? Na šis paaiškinimas irgi, greičiau, iš asmeninės dėdės Lansbergio „iliuzijų skrynios”. „Mėlyna dama“ tikrai naudinga Rusijai. Dėl daugybės priežasčių.

Paėmus net tą slidų Butkevičių ­ tai nestatysime AE, tai statysime, tai ne šitą, o kitą, tai pasiruošę

jau bet kokią, bet pinigų nėra nei vienai ir kt. O Grybauskaitė tiesi, kaip Vilniaus televizijos bokštas. Jos dvižingsnius gali atspėti bet koks politologijos fakulteto studentas ­ jos politinių įrankių rinkinys yra standartinis, o sprendimų priėmimo motyvacija paremta dviejų supratimų erdvės ­„šnipinėjimo manijos“ ir „rusofobijos“: jeigu Rusijoje pritarė ­ reiškia daryti nereikia; Rusijoje sukritikavo ­ tai puiki idėja. Kur dar Rusijai rasti tokį nuspėjamą kaimyną? Netgi pažvelgus į Lietuvos energetikos politiką. Kaip karštai Grybauskaitė palaikė Ignalinos AE uždarymą! Ir ką galiausiai turime? Lietuva padidino Rusijos dujų pirkimus. Ir kam galiausiai atnešė naudos „mėlynoji dama“?

Pas ką dar iš Lietuvos elito tiek daug tamsių dėmių biografijoje, kurios daro juos pažeidžiamus? Be to, neužtenka turėti nemalonių asmens bylos puslapių, reikia juos dar ir užsispyrusiai slėpti ir keisti prasmę, tuo pačiu brukant į rankas ginklus savo priešams. Dar šių metų balandžio mėnesį Raimundas Celencevičius publikavo straipsnį tiksliu pavadinimu „ Dalios Grybauskaitės Achilo kulnas : kol prezidentė išdidžiai tyli, apie jos praeitį pasakoja Leningrado šešėliai”, iš kurio tampa aišku, kad ponia prezidentė daug apie save nutyli. Tokiomis aplinkybėmis, kai daktarės Grybauskaitės slepiami sovietinės praeities pėdsakai vienaip ar kitaip liko Maskvoje, Peterburge ir esant būtinybei gali būti surasti, Lietuvos prezidentė tampa priklausoma nuo Rusijos ne mažiau, nei Mažeikių naftos perdirbimo įmonė.

Naujas lyderis galėtų su nauja jėga išnešioti po šiuos koridorius rusofobijos užkratą, kviesti taikyti sankcijas, antram Niurnberg ui , Trečiajam pasauliniam karui prieš Rusiją. Dabar tai vargu ar įmanoma. Kaip neįmanoma ir Grybauskaitei esant šiame poste efektyvi savarankiška diplomatinė Lietuvos priešprieša Rusijai ­ Vilnius, turėdamas tokią prezidentę net nesugeba pagauti išorinių politinių trendų: kvietė bombarduoti Siriją, o dėl jos susitarė; kvietė susitarti su Janukovičiumi, o jį gėdingai išvijo iš šalies; kvietė taikyti pačias griežčiausias sankcijas Rusijai, O Europa pristabdė; kvietė nesigėdinti panaudoti jėgas prieš pietryčių Ukrainą, O Merkel siūlo nesigėdyti Kijevo dialogo su protestuotojais. Kaip su tokiu politinės analizės efektyvumu galima sulaikyti Rusijos „imperines ambicijas“? Maskva su Berlynu sąjungą sudarys, o Vilnius ir nepastebės...

Laukti, kol naujas Grybauskaitės penkmetis virs stipriausiu skiepu nuo tos pačios rusofobijos. Per penkis metus visuomenė galutinai pavargs nuo karo su matrioškomis, nuo pasipiktinimą keliančių spjūvių į Antrojo pasaulinio karo veteranus, nuo kovos su sovietiniais paminklais, dešrelėmis ir vėliavomis, nuo pastovių isterijų dėl „Rusijos grėsmės“ ir kt. Ir visa tai ekonominės degradacijos fone, kurios negalima visą laiką priskirti „Kremliaus pinklėms”. Bendrai įmant, per šiuos penkis metus taps akivaizdžiu prie valdžios pripuolusių konservatorių galvų vakuumas, o reiškia jų mantros apie „Maskvos aštuonkojį” pačios savaime taps nereikšmingos.

Neabejotinai, naudingiausias Rusijai būtų išmintingas, pragmatiškas, nesitrankantis tribūnose su antirusiškomis isterijomis ir realizuojantis bendrus projektus su kaimynais lyderis, bent jau toks, kaip Vygaudas Ušackas 2008 metų „kirpimo“.

Taigi iš esmės per 25 metus Letuvoje taip ir nesusiformavo naujas sveikas elitas su strateginiu mąstymu ir nestandartiniais sprendimais, kuris vestų šalį į priekį. Galiausiai prie vairo stovinti grupė konjunktūrini ų persivertėlių be jokių Kremliaus „rankų” ir „žnyplių” marginalizuoja savo šalį, paversdama ją juokingu pulku, surinktu kovai su „Rusijos imperializmu” ir gyvenančiu „šaltojo karo” realijose. Tam, kad tuo persirgtų, iš tikrųjų verta dar penkeriems metams išrinkti daktarę Grybauskaitę.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 11 — id: `scraped:rubaltic_lt:5e55a753a08cdd60`

**Title:** Paksas: „Pirmą kartą neisiu balsuoti. Rinkimai yra nedemokratiški“

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Sekmadienį Lietuvoje vyks prezidento rinkimai. Bet nepanašu, kad rinkimų kampaniją galima vadinti pilnavertę, o rinkimus teisėtus bei laisvus be vienos personos dalyvavimo – Rolando Pakso. Jis spėjo per savo politinę karjerą užimti Vilniaus mero postą, premjero bei europarlamentaro postus. Jis visada likdavo savarankišku politiku su savo nuomone. Vienas iš nedaugelio. Kaip tik dėl tos nuomonės, kuri neatitiko ir dabar neatitinka „sistemai“, jis buvo pašalintas 2004 metais iš prezidento pareigų po Seime inicijuoto apkaltos proceso. R. Pakso priešai bandė uždrausti vadintis jam titulu „prezidentas“, kuris yra skiriamas iki gyvos galvos kiekvienam, kas buvo išrinktas į šį aukštą postą. Net po 10 metų Lietuvos elitas bijo R. Pakso dalyvavimo prezidento rinkimuose – jam tiesiog buvo neleista dalyvauti gegužės 11 d. rinkimuose. Visą situaciją mes aptarėme su Lietuvos eks-prezidentu, partijos Tvarka ir teisingumas vadovu Rolandu PAKSU:

- Ponas Prezidentas, kodėl Jūsų manymu, negavote leidimo dalyvauti prezidento rinkimuose?

- Matyt, vienos priežasties čia nėra. Kažkada sistema negalvojo, kad aš galiu tapti prezidentu. Politinė sistema arba tas valdantysis elitas prieš 11 metų ganėtinai ramiai stebėjo situaciją. Jie buvo nusprendė, kad nieko valstybėje keisti nereikia. Aš turiu omeny prieš 2003 metų rinkimus. Buvo sutarę, kad Valdas Adamkus turėtų likti prezidentu kitai kadencijai, ministras-pirmininkas ir Seimo pirmininkas – tie patys. Politinės partijos, valdantysis elitas nusprendė, bet su tuo nesutikau aš. Pasakiau, kad turėčiau pakeisti tą sistemą ir man pavyko tapti prezidentu. Tą sistemą aš pradėjau keisti. Supratęs valdantysis elitas, kad ir šį kartą gali įvykti panašūs dalykai, išdėstė daugiau apribojimų nei prieš 10 metų. Čia kaip yra žymiojo Vladimiro Vysockio daina «Идет охота на волков». Kai vilką aptveria raudonom vėlėm ir medžiotojai iš visų pusių šaudo i tą vilką, o jis šiepia dantis ir šoka per juos.

Antras dalykas, mes matavome tuos reitingus – tiek mūsų partijos, tiek asmeninius. Jie buvo tokie, kad antras ratas iš karto yra garantuojamas. O kaip viskas apsisuks antrame rate jau niekas nežino. Taigi, sistemai, kuri ir prieš 10 metų padarė neteisėtą veiksmą, ir dabar – jiems paprasčiausiai baisu. Baisu, kad įtaka gali išeiti iš jų rankų, iš kontrolės.

Trečia, tikriausiai bus tokiai, kad visi bijo konkurentų. Politinės partijos skaičiuoja, kaip joms būtų geriau ar blogiau. O valstybę nustumia į šoną.

Turime du sprendimus: Strasbūro žmogaus teisių, Jungtinių Tautų žmogaus teisių komiteto. Bet, visų pirma, skaičiuojama, kaip man ir partijai bus patogiau – įgyvendinti tą sprendimą ar ne?

- Kaip Jus galvojate, tai buvo tik Vyriausios rinkimų komisijos sprendimas ar kažkas prie to prisidėjo?

- Nemanau, kad Vyriausias administracinis teismas ir Vyriausioji rinkimų komisija buvo visiškai savarankiški šiuo atveju. Kažkada vienos valstybės vadovas sakydavo: „Laimi ne tas, kas balsuoja, o tas, kas balsus skaičiuoja“. Žinot apie ką aš kalbu. Panašu, kad Lietuva dar toliau nuėjo to nedemokratiniu keliu. Jau nebeleidžiama skaičiuoti balsų. Neradau argumentų nei Vyriausios rinkimo komisijos sprendime, nei Vyriausiojo administracinio teismo sprendime. Jų nėra, argumentai – juokingi.

Buvo du Vyriausiojo administracinio teismo sprendimai. Pirmas – neišduoti man parašų rinkimų lapo ir kad VRK buvo teisi. Visiems teisės studentams siūlyčiau perskaityti teismo sprendimus. Tai yra chrestomatija, kaip negalima daryti. Kaip pas mus teisė, demokratija ir politinis suinteresuotumas yra atskirti – viskas labai gražiai įrašyta. Aš kreipiuosi dėl to, kad yra pažeistas tarptautinis pilietinių teisių paktas. Tai yra 25-as straipsnis – teisė į laisvus rinkimus. Teismas man atsako: „Ar pažeistas tas 25-as straipsnis, gali nustatyti tik Jungtinių Tautų žmogaus teisių komitetas“.

Aš tada galvojau, o kaip gi dabar teisėjai išeis iš šios situacijos. O teismas prisidengė formalumais ir nepriėmė iš naujo svarstyti mano pareiškimo. Buvo du formalumai, kuriais jie prisidengė.

Vyriausias administracinis teismas gali iš naujo svarstyti reikalą, jeigu atsiranda naujos aplinkybes. Ir įstatyme yra įrašyta – kas yra naujos aplinkybės. Tai teismas man atrašo: „Pagal Lietuvos įstatymą i naujų aplinkybių sąrašą nėra įrašytas Jungtinių Tautų žmogaus teisių komiteto sprendimas“.

Tada aš nurodžiau kitą priežastį, dėl ko reikėtų atnaujinti svarstimą. Sužinojau, kad viena teisėja yra Konstitucinio teismo teisėjo Žalimo žmona, o jis atstovavo Vyriausybę Strasbūro žmogaus teisių teismo sprendime. Taigi žmona aiškiai buvo suinteresuota – tai yra šeima. Atsakymas vėl formalus – aš privalėjau anksčiau žinoti, kas yra kieno žmona.

Tai yra juokingi dalykai. Bet kai viskas darosi rinkėjų bei valstybės ateities sąskaita...

- Tai gal galima teigti, jog šiandienos Lietuvoje „demokratija“, „politinė laisvė“, „laisvė“- yra tik tušti žodžiai?

- Man labai patinka mūsų prezidento Aleksandro Stulginskio žodžiai: „Laisvės klausimą gali spręsti tik pati lietuvių tauta, tad toj kovoj tik ją ir remtis“.

Bet jie patys norėjo nuspręsti. Ir rodos, visi viską supranta: norės – ir balsuos už Paksą, nenorės – tai nebalsuos. Tuo labiau, kad praėjo jau 10 metų po tų įvykių. Dvi tarptautinės pačios solidžiausios institucijos pasakė – jūs pažeidinėjate žmogaus teises. Ne.

Bet įsivaizduoju, kad anksčiau ar vėliau tai baigsis socialiniu sprogimu. Kiek bendrauju su žmonėm, labai jaučiasi žmonių bei valdžios atitolimas. Iki sprogimo labai nedaug.

- Ar Jūs planuojate dalyvauti jau kituose prezidento rinkimuose?

- Niekada neslėpiau to. Kai kurie mano kolegos įsitikinę – tau nereikėjo sakyti, kad dalyvausi prezidento rinkimuose. Kai apie tave nieko nežinom, nieko nedarai ir nežadi – gal ir būtų pakeista Lietuvos Konstitucija. Bet man nepatinka tokie žaidimai. Visada sakau, kad aš sieksiu to. Postas reikalingas, kad įgyvendinti programą. Dėl to ir esu politikoje. Aš pasieksiu to. Šiandien jau, po Jungtinių Tautų komisijos komiteto sprendimo nebėra kur trauktis. Dienos suskaičiuotos per kiek reikia įgyvendinti tą sprendimą. Nebent Lietuva išstotų iš Europos tarybos, Jungtinių Tautų.

- Kodėl Jūs nusprendėte remti būtent Z. Balčytį? Ir ar dabar yra didelė antrojo turo galimybė?

- Yra toks filosofas Seneka. Man jis labai patinka. Ir kai žmogus nebežino, ką daryti, kartais labai sveika jį paskaityti. Filosofas rašo: „Visuomet kaukis už respubliką, už valstybę. Jeigu tave išmetė iš forumo – kaukis už forumo durų, netekai rankos ar kojos – kaukis be jų, netekai balso – kaukis akimis“. Įsivaizduoju, kad siekdamas prezidento posto, padariau viską. Bet praėjusią savaitę Vyriausias administracinis teismas pastatė tašką. Mes turim žmonių pasitikėjimą, jų palaikymą, savo programą, tarptautinių institucijų sprendimus.... Bet šiandien yra tokia situacija – taškas.

Bet lygiai taip pat suprantu, kad valstybė neliks be prezidento. Ir šiuo atveju, valstybėj geriausias variantas iš kandidatų yra Z. Balčytis.

Lygiai kaip prieš keletą mėnesių sakiau, kad valdančiajai koalicijai reika iškelti vieną kandidatą ir eiti su juo. Tikiu, kad Z. Balčytis gali patekti į antrą turą išvaldančios koalicijos partneriai palaikys jį. Ir tai bus rimtas įdarbis į prezidento rinkimus. Padariau viską, kaip partijos Tvarka ir teisingumas vadovas, nuoširdžiai pridedu ranką prie širdies. Bet dabar mes žiūrime, kas bus geriau Lietuvai. Valstybei geriau, kad žmonės balsuotų už Z. Balčytį.

- O ką būtent Jūs pakeistumėte šiuolaikinėje Lietuvoje?

- Laikiausi principo, net ir po 2004 metų, kada teko pereiti tą sumaišties etapą – niekada nekritikuoti prezidento. Tokios pat taktikos laikėsi ir Algirdas Brazauskas.

Daug ką daryčiau kitaip.

- Šią savaitę bus priimtas sprendimas dėl laikinos Seimo tyrimo komisijos sudarymo, kuri turės nustatyti dėl kokių priežasčių iki šiol nėra įgyvendintas Europos Žmogaus Teisių Teismo 2011 m. sausio 6 d. priimtas sprendimas dėl Jūsų teisių pažeidimų, ir kokiu būdu Lietuva turi įvykdyti Jungtinių Tautų žmogaus teisių komiteto konstatavimą dėl Jūsų politinių teisių atkūrimo nuo 2004 metų. Kokiu darbo rezultatu laukiate nuo šios komisijos ir ar jie bus objektyvus?

- Tikiuosi, kad ji bus sudaryta. Kaip tik dabar sprendžiamas tas klausimas Seime. Komisijos vien jau pavadinimas sako apie jos tikslus – pilietinių ir politinių prezidento Rolando Pakso atstatymas. Ką reikėtų daryti, kad pagaliau valdžia susitartų – kada ir kokiu būdu mes tai padarysime.

- Jūsų manymu, šiandienos Lietuvos politiniame gyvenime parija Tvarka ir teisingumas turi didelę įtaką? Kiek apskritai nuo jos priklauso valdančios koalicijos sprendimai?

- Be abejo, būtų daug smagiau turėti 71 atstovą. Tikiuosi, ateis toks laikas. Tada 100% Vyriausybės programa bus sudaryta iš Tvarkos ir teisingumo partijos programos.

O dabar mes esame koalicijos partneriai, turime 10 žmonių Parlamente, beveik 160 savivaldybių tarybų narių, atstovaujame Europos parlamente (2 asmenys). Pagal pozicijas ir vertinimus esame jau ilgą laiką antroji parija.

Nuo mūsų pozicijos daug kas priklauso valstybėje. Situacija šiandien nėra bloga.

- Kodėl, kaip Jūs galvojate, neįvyko Jūsų bei Darbo partijos susijungimas?

- Manau tai buvo geras žingsnis, kad pradėti procesą ir matyti tikslą. Galėtų atsirasti galinga didžiulė partija, su daug atstovų, pretenduojanti pagal politinį svorį į pirmą vietą. Kai pradėjome procesą, atsirado labai daug trukdžių. Ne tik iš tų 2 partijų, kurios norėjo susijungti.

Visi konkurentai pamatė, kad gali tekti skaitytis su šią jėgą. Deja, šiame maratone, kurį reikėjo nueiti nuo pirmos idėjos iki sujungimo, pavadinimo bei bendro pirmininko – mūsų kolegos darbiečiai neišlaikė. Pamačiau, kad jie dreifuoja, tai nebeduoda naudos nei vienai pusei, taigi nusprendžiau sustabdyti.

- Jūs nebijote, kad galite būti pašalintas, kaip kažkada JAV prezidentas D. Kenedi?

- Tokių klausimų esu girdėję labai daug. Nuo premjeravimo laikų, sprendimų dėl privatizacijos. Tada tai buvo labai karšta ir galėjo įvykti. O dabar jau nemanau. Tikrai nemanau.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 12 — id: `scraped:rubaltic_lt:4cac85ed5fe5c459`

**Title:** Ekspertas:  “Baltijos šalys kovojo už nepriklausomybę, o gavo CŽV kalėjimus”

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Kodėl per 20 nepriklausomybės metų Baltijos šalys taip ir nerado kitos bazės savo identiškumo konstravimui, išskyrus užpuolimus prieš Rusiją ir bendrą sovietinę praeitį, ir kokių technologijų pagalba visuomenė yra manipuliuojama, RuBaltic.ru portalui papasakojo RF visuomeninės palatos narė, Užsienio politikos tyrimų ir iniciatyvų instituto generalinė direktorė Veronika Krašennikova:

- Pone Veronika, šiandien mes gyvename simbolių pasaulyje, ir labai dažnai pasirodo, kad viskas kas nauja - tai gerai pamiršta sena. Tai, Jūsų nuomone, tiktai žmogaus atminties ypatumai arba kažkas daugiau? Ką Jūs galite pasakyti apie 1989 m. Baltijos šalių kelio ir šiuometinių įvykių grandinės Ukrainoje paraleles, apie neužmirštuolę, kaip vieną iš lėšų rinkimo nacistų armijai programos “Žiemos pagalba” simbolį, ir apie neužmirštuolę, kaip sausio 13-osios įvykių Lietuvoje atminties simbolį Lietuvos politinės elitos švarkų atlapuose? Ar tai atsitiktiniai sutapimai?

Jūs pateikiate labai gerus pavyzdžius, kurie rodo, kaip iš tikrųjų yra nesunku suorientuotis Vakarų įtakos vidinei situacijai šalyje veiksnių instrumentarijuje. Šis instrumentarijus yra ribotas, egzistuoja kelios dešimtys būdų, kurie gali būti panaudoti įvairiose kombinacijose. Jeigu Jūs perskaitysite Viljamo Bliumo knygą “Demokratijos nužudymas: CŽV ir Pentagono operacijos šaltojo karo laikais”, galėsite daug ką pasisemti, kad suvokti šiandieninius įvykius, ar tai būtų įvykiai Ukrainoje ar Baltijos valstybėse. Metodologija ir taktika pasikeitė mažai.

Jūsų pateiktus pavyzdžius galima papildyti dar vienu – manifestacijose vietinės merginos dovanojo geles vidinei kariuomenei: Kirgizijoje tai buvo tulpės, Gruzijoje tai buvo raudonos rožės, Rusijoje – baltos rožės. Viljamas Bliumas pateikia savo knygoje įdomų pavyzdį. 1960-1970 metais Čilėje ir Argentinoje moterys išeidavo į demonstracijas su tuščiais puodais – jos daužė puodų dangčiais, norėdamos parodyti, kad vyriausybė neduoda galimybės išmaitinti šeimą. Neseniai įvykusiuose rinkimuose Venesueloje 2012 m., kai buvo išrinktas Nicolas Maduro, vėl išėjo moterys su tuščiais puodais. Užtat, kai žinai Vakarų vyriausybinių ir nevyriausybinių agentūrų veiksnių instrumentarijų, iššifruoti dabartinę situaciją tampa taip lengvai, kad kartais net nuobodu.

- Ne taip seniai dėl ideologinių priežasčių Lietuvoje buvo sustabdytas Pirmojo Baltijos kanalo transliavimas, kuriame “Žmogus ir įstatymas” laidoje buvo pristatytas alternatyvus oficialiam požiūris į 1991 m. sausio 13-osios įvykius. Ką rodo šis faktas?

Baltijos valstybės kovojo neva už savo nepriklausomybę. Ir kas gi galiausiai išėjo? Uždaromi ne tik televizijos kanalai, bet ir žmonės, kurie tik siūlo ištirti tai, kas nutiko tada, prie Vilniaus televizijos bokšto, yra kaltinami išdavyste ir persekiojami pagal įstatymą. Pastaruosius kelerius metus Lietuvos įstatymų leidėjai ir teismų sistema persekiojo Algirdą Paleckį, kuris tiktai pakartojo tų įvykių dalyvio, pono Butkevičiaus, žodžius, ir pasakė, kad reikėtų atlikti tyrimą. Bet pagal naujus Lietuvos įstatymus tų įvykių peržiūra yra persekiojama pagal įstatymus. Atgavus nepriklausomybę Baltijos šalys įstojo į NATO esant pirmai galimybei, leido aljanso karinėms bazėms įsikurti savo teritorijose, ir šiandien iš šių bazių NATO patruliuoja oro erdvę palei Rusijos sieną.

Baltijos valstybės taip pat tapo CŽV slaptų kalėjimų vietomis, kur buvo kankinami įtariamieji terorizmu, nes JAV teritorijoje kankinimai yra uždrausti, todėl įtariamieji buvo išvežami į kitų valstybių teritorijas: Artimieji Rytai, Egiptas, o konkrečiai į Gvantanamo kalėjimą, ir štai – į Baltijos valstybes. Jeigu kalbėti apie ekoniminę šio klausimo pusę, nuo ketvirtadalio iki trečdalio, net iki 40% Lietuvos gyventojų paliko savo valstybes ir pabėgo į “seną” Europos Sąjungą, nors prieš 10 metų 2004 m. gegužės mėn. įvykęs įstojimas į ES žadėjo jiems europietišką gyvenimą savo namuose. Bet to neįvyko.

- Dar vienas įdomus faktas iš šiuolaikinės Lietuvos realybės – tai “Lietuvos demokratijos tėvo” Vytauto Landsbergio pasiūlymas lietuvių pasuose gimimo vietą pakeisti iš “Lietuvos TSR” į “okupuotą Lietuvą”. Tai yra planingas komunistinės praeities prilyginimas nacių okupacijai. Ką Jūs galite apie tai pasakyti?

Politikai, raginantys imtis tokių veiksmų, taip pat ir nedidelė Vakarų Ukrainos dalis bendradarbiauja su pačiomis nedemokratiškomis jėgomis pasaulyje. Galičina* kovojo Trečiojo Reicho pusėje. Per pastaruosius 20 metų Baltijos šalių lyderiais tapdavo išeiviai iš JAV ir Kanados – kolaborantų, sėkmingai pasislėpusių nuo teismo už vandenyno, vaikai.

- Gruodžio viduryje Lietuvoje kilo skandalas dėl Olego Gazmanovo per Rusijos konstitucijos 20-mečio koncertą nuskambėjusios dainos “Pagamintas SSRS “. Kai kurie Lietuvos politikai net siūlė uždrausti atlikėjui atvykti į Lietuvą ir paskelbti jį persona non grata. Ar tai irgi karo pasireiškimas kultūros fronte? Atkaklus noras įkaitinta geležimi išdeginti bet kokį užsiminimą apie sovietinį periodą iš savo biografijos – ką visa tai rodo?

Gruodžio 12 d. aš buvau tame koncerte Kremliaus rūmuose ir iš tikrųjų auditorija labai šiltai priėmė šią dainą, ir ES ambasadorius Rusijoje lietuvis Vygaudas Ušackas, nuo kurio ir prasidėjo skandalas, buvo turbūt vienintelis, kam šios dainos atlikimas buvo nemalonus. Ir tai dar vienas tos nesėkmingos ideologinės linijos pavyzdys, kurią pasirinko Baltijos valstybės. Žinote, aš ne taip seniai lankiausi Estijoje ir atvykau į Taliną vėlai vakare. Centrinėje aikštėje, kaip ideologinis monumentas, stovi fašistų stilistikos kryžius, švytintis mirtinai išblyškusia šviesa. Labai grėsmingas įspūdis.

Ne mažiau svarbus yra tas faktas, kad šitas kryžius buvo pastatytas vos už 100 metrų nuo tos vietos, kur anksčiau stovėjo Bronzinis kareivis – taip įsikūnija idealų ir orientyrų kaita. Mačiau mūsų rusų kolegų Estijoje dokumentinį filmą apie 2007 m. “bronzinės nakties” įvykius, kai buvo perkeliamas Bronzinis kareivis – tai buvo labai akivaizdi represyvaus NATO aparato demonstracija šalies žmonių atžvilgiu. Estijos policininkai, išvaikydami demonstrantus, areštuodami dalyvius, tiesiog praeivius, tarp kurių buvo ir kelis užsieniečių, elgėsi labai žiauriai. Tai yra labai ryškus pavyzdys, kaip kietai NATO šalyse kovoja prieš nesutinkančius su nacionaline politika ir su NATO politika.

- Latvijoje ir Lietuvoje buvo priimti įstatymai, draudžiantys sovietinės simbolikos naudojimą , Estijoje irgi jau ne pirmus metus vyksta nacizmo heroizavimas ir atvirkščiai - komunizmo pasmerkimas – ar Jūs matote čia konfrontacijos tęsimą tarp sovietinės ir amerikietiškos/europietiškos (jeigu tokia yra) kultūros? Gal tai naujas kovos už ateitį etapas? Tas, kas padės simbolikos pagrindus, suformuos tikslus, tas ir kontroliuos ateitį?

Komunizmo prilyginimas nacizmui ir Šaltojo karo laikais, ir šiandien, visada buvo vienu iš svarbiausių ideologinių propagandinės veiklos prieš Rusiją krypčių. Jiems svarbu ištrinti mūsų vertybes ir perrašyti istoriją žmonių sąmonėje. Įtikinti mus tuo, kad viskas, kas su mumis buvo – tai buvo klaida. Tai buvo bjauras laikas, o dabar mes turime šansą tapti tikrai gerais žmonėmis, kad Vakarai mums tuo padės, ir mums geriau eiti tokiu keliu. Jeigu pažvelgti į istoriją, matyti, kad JAV visada pasirinkdavo sąjungininkus iš kitų valstybių ultradešiniųjų ir ultranacionalistinių jėgų ir padedavo jiems. JAV reikalingi tarpininkai kitų valstybių teritorijose, kurie susidorotų su nesutinkančiais, o šie ultradešinieji savo šalyje susidoros su savo oponentais daug žiauriau, nei tai padarytų Amerikos kareiviai. Nesenas pavyzdys – Libija. Amierikietiški kareiviai nepasielgtų su Muamaru Gaddafi, jeigu jis patektų į jų rankas taip žiauriai, kaip tai padarė Libijos banditai. Būtent jiems padedavo JAV, siekiant nutraukti Gaddafi.

Todėl fašizmas ir nacizmas yra naudingi JAV fašistinėms ir ultradešiniosioms jėgoms kaip kovos prieš jų priešus instrumentai. Trečiąją Antrojo Pasaulinio karo dieną Haris Trumenas sakė: “Jeigu mes pamatysime, kad laimi Vokietija, tai mums reikėtų padėti Rusijai, o jeigu laimės Rusija, tai mums reikėtų padėti Vokietijai, tegu jie užmuš, kaip galima daugiau…”

- Kokias Jūsų nuomone savo įtakos išplėtimo pasaulyje galimybes turi Rusija?

Pirmiausia, mes esame teisybės pusėje. Pažiūrėkite, kokį repeticinį pranašumą mes gavome, neleidžiant įvykdyti karines atakas Sirijoje. Kaip ir anksčiau, dauguma žmonių pasaulyje ir net dauguma žmonių JAV ir Vakarų Europoje – prieš karą.

Jeigu kalbėti apie konkrečius veiklos instrumentus, tai pavyzdžiui, TV kanalas Russia Today daugeliui pasaulyje tapo alternatyviu naujienų šaltiniu. Jeigu Vašingtone jūs sėsite į taksi, o taksistas, kaip tai dažnai būna, nėra amerikietis, jis pasakys: “O, rusas, aš žiūriu Russia Today!”. Aš nežinau, kiek žmonių JAV isteblišmente žiūri Russia Today, bet jų tikslus ir pažiūras niekuo negalima pakeisti. Vokietijoje apie 70-80% vokiečių nuosekliai pasisako prieš šalies militarizaciją, prieš aktyvų Vokietijos dalyvavimą NATO operacijose, prieš vokiečių kontingento pasiuntimo į Afganistaną ir Iraką, bet vis dėlto vyriausybė priima kitus sprendimus, todėl kad vyriausybė įsipareigojo NATO. Bet visuomenė dažniausiai mūsų pusėje – teisybės pusėje.

- O kiek reikalinga aktyvi Rusijos kultūrinė politika? Nerėtai galima išgirsti, kad ta programa arba tas dainų atlikėjas – tai “švelni” Rusijos jėga, vos ne Kremliaus agentai, jūsų kultūra mums nereikalinga ir t.t. Kaip į tai reaguoti?

Mes turime tęsti šią veiklą, ir, jeigu oponentai piktinasi, reiškia, kad tai yra veiksmingas instrumentas.

RuBaltic.ru pastaba:

*SS divizija “Galičina” – karinė formuotė, susidedanti iš Ukrainos savanorių, Antrojo Pasaulinio karo metu. Viena iš nacių Vokietijos Waffen SS divizijų.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 13 — id: `scraped:rubaltic_lt:214af486f05946e5`

**Title:** Toli nuo Volgogrado: Baltijos šalys tarptautinio ekstremizmo žemėlapyje

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Teroro aktai Volgograde vėl iškėlė šiuolaikinės Rusijos tarptautinio terorizmo problemą į pirmą vietą. Tačiau kovoje su terorizmo grėsme išskyrus pirmaeilių priemonių svarbu blaiviai įvertinti dar ir išorinį kontekstą – teroristai mirtininkai juk neatsiranda iš oro, reikalinga maitinamoji terpė. Ir čia savo grašį primetė ir Baltijos šalys…

“O, sūnau! Jeigu šimtmečio kito sulauksi ir ant aukšto Kaukazo sustojęs dairysies aplink: neužmiršk, jog ir čia būta vyrų, pakėlusių tautą ir išėjusių laisvės – šventų idealų apgint”. Šie žodžiai iškalti pastatytame D. Dudajevo skvere Vilniuje paminkle Džocharui Dudajevui. Jų autorius – miręs Lietuvos poetas ir vertėjas Sigitas Geda, tipiškas savo epochos produktas: Lietuvos TSR Valstybinės premijos laureatas, pjesės “Komunarų gatvė” autorius. Jis pasižymėjo savo “virtuvine” laisvamanybe 70-aisiais, 80-aisiais metais tapo Sąjūdžio aktivistu, karštai smerkė viską sovietinį 90-aisiais. Poeto biografija baigėsi tuo, kad po dviejų savaičių girtavimo Sigitas Geda įsmeigė peilį dukrai į krūtinę, gavo trejus metus kalėjimo ir mirė.

Atrodo, lyg tai būtų atskira asmeninė istorija. Tačiau Lietuvos poeto ir jo šalies (o jeigu kalbėti plačiau – ir Baltijos šalių) biografijose yra kai ko bendro. Tas pats maištavimas, oficialiai deklaruojant lojalumą, kaip mokestis už dosnią paramą iš Sąjungos centro. Liaudies frontai ir kiti “Pertvarkos judėjimai”. Po to blaškymas iš vienos pusės į kitą, gyvenimo prasmės praradimo jausmas, vėliau užčiuopiamas kaip urvinė rusofobija su noru kaip galima stipriau, bet kokiu būdu pakenkti “šiai Rusijai”.

Ne tik Dudajevo, bet ir ekstremistų herojizacija visiškai sutapo su šia nesveika logika. Būtent šiame klausime Lietuvos poetas ir jo šalis tapo vienas kito atgarsiu: paremti ekstremistus, paskelbti juos kovotojais dėl šviesių demokratijos idealų, statyti jiems paminklus ir vadinti aikštes jų garbei, o Rusija tegul vien savo jėgomis išsipainioja iš Nord-Ostų, Kaspijskįų, Nevskio ekspresų, Beslanų, Volgogradų ir t.t.

Tai galima pasakyti ne tik apie Lietuvą. Kosmonautikos aleja Rygoje nuo 1996 m. yra vadinama Džocharo Dudajevo vardu. 1997 m. memorialinė lenta atsirado ir Tartu mieste Estijoje. 2005 m. Varšuvos merija atmetė pasiūlymą pavadinti dviejų gatvių sankryžą vaikų, žuvusių Beslane, garbei, ir suteikė jai Džocharo Dudajevo Aikštės statusą. Į Rusijos URM, pavadinusios šį sprendimą “faktišku tarptautinio terorizmo pasireiškimu”, kreipimąsi tuometinis Varšuvos meras Lechas Kačinskis atsakė: “Tai ne jų reikalas”.

Atminimo vietos Varšuvoje, Vilniuje, Rygoje, Tartu, skirtos Dudajevui, – kam jos skirtos? Teisių gynėjui, švietėjui, mecenatui? Ne. Žmogui, kurio valdymo laiku, etniniai valymai, masiniai nužudymai, rusų persekiojimai tapo norma. Žmogui, kurio valdymo laiku, veikė žiauri šariato įstatymai – 1997 m. rugsėjo mėn. (Baltijos šalyse Dudajevas jau buvo paskelbtas kovotoju “už šventus idealus”) Grozno mieste viešai buvo sušaudyti šariato teismu nuteisti vyras ir moteris, Ar tai ir yra tos pačios “europietiškos vertybės”, apie kurias taip mėgsta padiskutuoti Baltijos šalių politikai? Ar statant Dudajevui paminklus, jo garbei pavadinant gatves, jie palaiko ir jo paveldėtojus – tuos, kurie žudo ir sprogdina šiandien?

Atsakymą į šį klausimą galima rasti visai nesenoje istorijoje – Lietuvos pilietės Eglės Kusaitės byloje. 2009 m. užverbuota teroristinės organizacijos “Kavkaz emirat” (lyderis – Doku Umarovas) ji buvo sulaikyta dieną prieš teroro aktus Maskvos metropolitene. Kaip vėliau išaiškins tardytojai, jos pagrindiniu taikyniu buvo bet koks karinis objektas, kuriame Kaune gimusi Kusaitė norėjo susisprogdinti, siekiant nužudyti kuo daugiau žmonių. Ją sulaikė ir nugabeno į Lietuvą, kur po kelerius metus trukusių tardymų jai skyrė ne 10 metų, o 10 mėnėsių laisvės atėmimą. Savo argumentose jos gynyba panaudojo Lietuvos valdžios oficialios politikos pavyzdžius, kai nužudyti per Čečėnijos karą Lietuvos samdiniai buvo heroizuoti (pvz. L.Vilavičius) ir labai iškilmingai palaidoti Lietuvoje. “Jeigu vienus kovo veiksmų dėl Čečėnijos nepriklausomybės dalyvius laiko herojais, tai kodėl kitus, kurie norėtų tapti tokiais pat dalyviais, laiko teroristais?” – teismas sutiko su šiuo argumentu. Nėra ko stebėtis, pasikartosime dar kartą - reikalinga maitinamoji terpė. O tokia terpė Baltijos šalyse yra.

Pavyzdžiui, žinomas faktas – “Kavkaz-Center” svetainė yra Šiaurės Kaukazo ekstremistinių organizacijų ruporas, kuri pozicionuoja save, kaip “Kaukazo nepriklausoma tarptautinė islamo internetinė agentūra”. Šioje svetainėje publikuojami radikalių islamistų - salafitų pamokslai, kviečiantys džihadui; pasakojama apie paskutinius teroro aktus, “kuriuos surengė patys neištikimieji, kad sukompromituoti taikų islamą”. Kurį laiką “Kavkaz-Center” štabas bazavosi Estijoje – 2003 m. Estijos saugumo policijos departamentas (KaPo) svetainės serverį konfiskavo. Tada “Kavkaz-Center” persikėlė… į Lietuvą ir daugiau nei metus dirbo ten. Lietuvos valdžia išjungė ekstremizmo svetainės serverį tik 2004 m. rugsėjo mėn. – po tragedijos Beslane buvo gana sunku pateisinti “kolektyvinio agitatoriaus ir organizatoriaus” veiksmus iš Lietuvos teritorijos.

O pirmo nepripažintos Ičkėrijos prezidento sūnūs Ovluras ir Degis – dėl ko jie persikraustė gyventi būtent į Lietuvą? 2001 m. Ovluras Dudajevas kreipėsi į prezidentą V.Adamkų su prašymu suteikti jiems Lietuvos Respublikos pilietybę, ir pridėjo žymų Lietuvos piliečių, įskaitant tuometinio sveikatos apsaugos ministro, dabartinio gynybos ministro Juozo Oleko ir to pačio poeto Sigito Gedos rekomendacinius laiškus. Ir Valdas Adamkus išimties tvarka Dudajevui jaunesniam suteikė Lietuvos pilietybę “už išskirtinius nuopelnus”. Ovluro Dudajevo natūralizacija buvo įvykdyta slaptai nuo visuomenės: kai istorija iškilo į paviršių, Lietuvoje kilo skandalas – kokius išskirtinius nuopelnus šaliai turi Dudajevo sūnus ir kodėl pilietybę jis gavo “Olego Davydovo” vardu?

O Degis Dudajevas - kaip išėjo taip, kad būtent Lietuvoje jis organizavo padirbtų Europos Sąjungos pasų gaminimą stambiu mastu? Įdomu, kam?

Beje, Dudajevo giminaičiai mėgino gauti Estijos pilietybę (taip pat “už išskirtinius nuopelnus”), o Riigikogu narys Olev Raju ant oficialaus deputato blanko per Estijos ambasadą pakvietė juos apsilankyti savo šalįyje.

Valdantis Baltijos šalių elitas klysta, jei mano, kad radikalaus ekstremizmo problema niekada jų nepasieks, o Rusijos Volgogradas kažkur labai toli, ir “jeigu kas atsitiktų”, bus galima išsisukti vien tik ritualiniu protokolinių užuojautų pareškimu.

Jiems reikėtų išsamiau susipažinti su bazavusios pas juos “Kavkaz-Center” svetainės materialais – ten daug rašoma apie tai, kaip “šventojoje džihado veikloje” yra naudingi taip vadinamieji useful idiots , kurie laiko “Alaho karius” nekaltomis aukomis. Dažniausia useful idiots – tai išprotėję miesto kairuoliai, kurie su entuziazmu įsijungia į bet kokią visuomeninę kampaniją prieš valstybę: už žalią energiją, už vegetarizmą, už pašalpas nelaimingiems migrantams. Tačiau nesveika rusofobija ir noras palaikyti net ekstremistus, kad tik pakenkti Rusijai, paverčia taip pat ir kraštutinius dešiniuosius Baltijos šalių politikus tokiais useful idiots .

Ir šiuo atveju tai ne Lietuvos, Latvijos, Estijos konkrečių politinių veikėjų, vakar lobuojančių Dudajevo interesus, o šiandien siuntinėjančių Kusaitę į Maskvą, asmeninis reikalas. Tai jau daug didesnio masto problema, rodanti, kokia iškrypusi ir supuvusi pasirodė režimo, susiformavusio šiose šalyse, esmė. Tai yra bendra Baltijos šalių problema, kurių elitas, bandantis meilikauti su ekstremistais, kad tik Rusiją įpykdyti, elgiasi taip, lyg nesupranta: vieną dieną šie mirtininkai gali ateiti jau ir į jų namus, stočius, traukinius, troleibusus. Nesenas pavyzdis – broliai Carnajevai Jungtinėse Amerikos Valstijose. Kam tada skirs savo eilėraščius Lietuvos poetai?

Lietuvos ekspertai, vertinami teroro aktus Volgograde, pritarė vienas kito nuomonei, kad sprogimų organizatorių tikslas – Olimpiada Sočyje. Ta pati, į kurią prezidentė Grybauskaitė nusprendė nevažiuoti, kaip ji pareiškė, “dėl politinių sumetimų”. Ką gi, kiekvienas turi savo instrumentus: vieni gali sau leisti politinius demaršus, kiti – teraktus. Bet jų tikslas (ir tai reikia aiškiai suprasti) bendras.

Перевод: Ольга Аксёнова.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 14 — id: `scraped:rubaltic_lt:3346df5b6e834dc2`

**Title:** Istorikas: Baltijos šalių kolaboracionistų  svajonės apie nepriklausomybę buvo naivūs

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Pastarosiomis savaitėmis Baltijos šalis vėl užplūdo “istorinių iniciatyvų banga”. Latvijoje eilinį kartą susiskaičiavo sovietinės okupacijos nuostolius, kurie, kaip pasirodė, yra lygūs metiniam Rusijos biudžetui. Lietuvoje įsteigė Sovietinės okupacijos tyrimo asociaciją, o Lietuvos politikos patriarchas Vytautas Landsbergis pasiūlė įstatymiškai įtvirtinti terminą “gimę okupuotoje Lietuvoje” ir priskirti jį visiems gimusiems Lietuvos TSR. Visų šių iniciatyvų ėmėsi po to, kai Vilniuje buvo inicijuotas “Komisijos nacių ir sovietų okupacinių režimų nusikaltimams” darbo atnaujinimas. Apskritai jau trečią dešimtmetį Baltijos šalių kolaborantų ideologinės reabilitacijos procesas eina ranka rankon su sisteminiu “sovietinės okupacijos” temos plėtojimu. Istorijos mokslų daktaro, Novgorodo Yaroslavo išmintingojo vardo valstybinio universiteto profesoriaus, Didžiojo Tevynės karo istorijos ir kolaboravimo Rusijoje (1941-1945 m.) specialisto Boriso Kovaliovo nuomone, visa tai yra sąmoningos savo praeities politizacijos apraiška, juk istoriniai faktai atkakliai rodo į tai, kad jėgų, palaikomų vietinių kolaborantų, pergalės atveju, Baltijos šalių nepriklausomybės atkūrimo perspektyva buvo neįvykdoma:

- Pone Kovaliovai, iš pradžių apsispresime dėl sąvokų apibrėžimo. Kaip Jūs galite apibrėžti terminą “kolaboravimas”?

- Vieningos nuomonės apie terminą “kolaboravimas” istorijos moksle kol kas nėra, nesusiformavo. Tarptautinių žodžių žodyne terminas “kolaboravimas” apibrėžiamas šitaip:

Vadinasi, nuo pat pradžių šis terminas turėjo tam tikrą geografinį pririšimą (Europa) ir chronologinį (Antrasis Pasaulinis karas). Sovietinės istorijos moksle žodis “kolaboravimas” labai dažnai buvo vartojamas Vakarų šalių atžvilgiu, TSRS atžvilgiu jis tapo vartojamu daug vėliau, nuo 1990-ųjų pradžios. Bendradarbiavimo dominantėje šis terminas dabar traktuojamas žymiai plačiau, nors šis bendradarbiavimas turi neigiamą konotaciją.

- Jeigu laikytis tokios kolaboravimo definicijos, ar galima kalbėti apie kolaboravimo egzistavimą Baltijos šalyse po 1941 m.? Ir jeigu kolaboravimas ten buvo, ar turėjo kokių nors skirtumų nuo kolaborantinių režimų likusioje TSRS teritorijoje?

- Vokietijoje ne taip seniai vyko konferencija, kurioje vienas kolega iš Ukrainos pareiškė, kad Ukrainoje Antrojo Pasaulinio karo metu jokio kolaboravimo nebuvo, nes nebuvo “nezaležnos” Ukrainos valstybės. Šis argumentas, žinoma, sukėlė sielos virpulį ne tik Rusijos, bet ir Vokietijos tyrinėtojams.

Kaip tik dabar rašau knygą apie ispanų Mėlynąją diviziją, kariavusią pas mus prie Novgorodo, vėlau prie Leningrado. Šioje knygoje pateikiu duomenis ne tik apie Rusijos teritoriją, bet ir apie kaimynines respublikas. Kaip žinoma, 1941-aisiais Gebelsas paskelbė suvienytos Europos civilizuotų tautų “kryžiaus žygio” prieš prakeiktą bolševizmą idėją. Ispanų žėmėlapiuose, atvirukuose, kuriuos mačiau, tame pačiame “Europos civilizuotų tautų” suvienytame fronte Estija, Latvija, Lietuva yra pažymėtos kaip nepriklausomos valstybės, Trečiojo reicho sąjungininkai.

Žiūrime toliau: 1941-1942-ųjų žiemos mūšių realijos. Šaltiniuose aiškiai rašoma, kad eina ispanai ir jems padeda Latvijos padaliniai, Belgijos padaliniai ir t.t. – suprantama, kolaborantiniai. Ir tai ant fronto linijos, o užnugario rajonuose jų buvo kur kas daugiau. Pabrėžiu, kad kalbama apie pačios karo pradžios įvykius. Jei kalbėti apie Baltijos šalių kolaborantines karines formuotes, tai, pagal ispanų šaltinius, jos atsirado Rusijos teritorijoje jau nuo 1941-ųjų pabaigos.

- Ar buvo Baltijos šalių teritorijoje tokių karinių formuočių, kurios kovojo prieš Sovietų valdžią, bet vis dėlto nesutiko bendradarbiauti su nacistais?

- Žinoma, istorija negali būti juodai balta, ji daugiaaspektė. Betgi karo realijuose, o ypač karo pradžioje, tai buvo praktiškai neįmanoma. Pas mus šiaurės vakaruose buvo tokia sąvoka, kaip “klajojantys partizanai”, t.y. žmonės, kurie išėjo į miškus, bandydami pasislėpti nuo karo; jie buvo pasiruošę kovoti su visais dėl savęs, dėl savo gyvybės.

Pavyzdžiui, 1941-ųjų vasarą nacionalistai iš Vakarų Ukrainos stengėsi įkūrti savo nepriklausomą valstybę – ji tiesiog buvo sunaikinta hitlerininkais.

Istorikas Aleksandras Sedunovas vienoje iš savo knygų pažymėjo įdomų epizodą. Pskove buvo įsikūrę Estijos policijos padaliniai. Per 1942-ųųj Kalėdas kartu su jais buvo ir Hjalmar Mäe – Estijos savivaldybės vadovas. Vaikinai truputį pasigėrė ir pradėjo samprotauti apie Didžiąją Estiją, jungiančią teritorijas iki pat Ilmenio ežero, t.y. Estijos valstybės teritorija turėjo padidėti 2-2.5 karto Rusijos teritorijų sąskaita.

- Šiuolaikiniams Baltijos šalių politikams dabar nenaudinga pozicionuoti kolaborantus kaip kovotojus ne tik prieš Sovietų valdžią, bet ir prieš nacizmą, kuriam tarnavo, neva, tik formaliai. Kokie šaltiniai gali atkurti tikras kolaborantų pažiūras?

- Klausimas labai platus, ir šaltinių yra gana daug, tarp jų ir archyvuose. Bet pastaruoju metu stengiuosi aktyviai tyrinėti “gyvą istoriją”. T.y. išskyrus archyvų dokumentų tyrimą, pvz., Ypatingosios valstybinės komisijos aktų apie nusikaltimus okupuotose teritorijose, aš dar važiuoju per kaimus ir renku interviu – žmonių, išgyvenusių okupaciją, prisiminimus.

Ir štai kas įsidėmėtina: šiuose interviu labai išryškėja nacijos sudaromoji dalis. Jeigu apie ispanus sako, kad tie buvo chuliganai, vagys, čigonai ir t.t., tai kažkodėl apie Estijos ir Latvijos karinių padalinių atstovus sako vienprasmiai – tai buvo sadistai, žvėrys, žmogžudžiai. Kalbu apie Rusijos kaimų realijas ir jų santykius su kolaborantais.

Iš pradžių galvojau, kad tai kažkoks fobijos pasireiškimas, kitos tautybės kaimyno nepriimtinumas (juk buvo Latvijos ir Estijos kaimų, kurie buvo praktiškai likviduoti prieš karą, 1937-1938-aisiais, dėl Stalino represijų), klausdavau apie tai, bet pasirodė, kad viskas buvo ne taip: 1943 m. daugybė Rusijos šiaurės-vakarų gyventojų buvo išvežta į Baltijos šalis, už “Panteros” linijos, ir šie evakuotieji pasakoja, kaip įvairiai jie ten bendravo su vietiniais gyventojais, kai kurie iš jų net padedavo evakuotiems, bet kareivius iš Baltijos šalių iki šiol prisimena kaip pačius pikčiausius okupantus.

Nemaloniai mane nustebino dar viena istorija. Sovietiniais laikais buvo sena gera dainelė apie tautų draugystę, dėlto kai kurie istorijos faktai išsitrindavo. Pas mus buvo mažas naikinimo lageris – kaimas Žestianaja Gorka (Skardinis Kalnas) ( kaimas Novgorodo srities vakaruose – RuBaltic.ru pastaba ), kur buvo sunaikinta kelis tūkstančių žmonių. Centro “Holokaustas” pagalba mes neseniai įrengėme ten memorialinį ženklą. Taigi dabar ten yra ir stačiatikių kryžius, ir raudona penkiakampė žvaigždė, ir žydų paminklinis akmuo. Iš pradžių šiais veiksmais kaltino vien tik vokiečius, juos apkaltino vadinamajame “Novgorodo Niurnberge” 1947 m. (Vokietijos karo nusikaltėlių teismas). Bet 1960-aisiais išaiškėjo, kad tarp šių baudėjų vokiečiai susidarė tik viršutinę dalį, o dauguma vykdytojų buvo iš Baltijos šalių. Bet kai pradėjo ieškoti karo nusikaltėlių, kad patrauktų juos atsakomybėn, pasirodė, kad beveik visi jų jau gyveno Vakaruose.

- Šiuolaikinėje Baltijos šalių istorinėje literatūroje galima rasti tokius gyventojų tarpusavio santykių su nacistais vertinimus. Istorikas, buvusis Rusijos ir Latvijos istorikų komisijos pirmininkas Inesis Feldmanas savo darbe “Latvija Antrajame pasauliniame kare (1939-1945): naujas konceptualus požiūris” rašo štai ką:

“Jei Vokietijos politika būtų nors truputį apgalvota ir atjaučianti, ypač valstybės nepriklausomybės atkūrimo klausimu, mažiau užsispyrusi arba ne tokia arogantiška ir represinė, tai, galbūt, Baltijos tautos daug plačiau palaikytų Vokietiją”.

Išeina, Latvijos istorikai pripažįsta, kad Latvijoje palaikė būtent hitlerinę Vokietiją, o “jeigu Vokietijos politika būtų nors truputį apgalvota”, tada palaikymas būtų visuotinis?

- Aš taip pat bendravau ir bendrauju su Latvijos istorikais, ir žinote, kas mane nustebino? Maniau, kad 1940-ųjų įvykių metu Latvijoje vyko bet koks pasipriešinimas – tegul ir ne ginkluotas, bet ideologinis: laikraščių, pokalbių lygmenyje. Aš klausiau Latvijos istorikų, ar buvo kokių nors žurnalistų, pasisakančių prieš tokį suartėjimą su Sovietų Sąjunga. Išaiškėjo, kad tai buvo traktuojama kaip apgalvota valdžios politika – ateina didelis karas, kurį reikia perlaukti po mūsų kaimyno sparneliu.

- Kaip Jūs vertinate, kiek reali būtų nepriklausomų (nors ir formaliai) valstybinių darinių atsiradimo Baltijos šalyse perspektyva po Trečiojo Reicho pergalės? Kas nutiktų su Baltijos šalimis TSRS ir visos antihitlerinės koalicijos pralaimėjimo atveju?

Nereikėtų pamiršti, kad mes visgi kalbame apie nacistinę Vokietiją, t.y. apie valstybę su puikiai paruoštu propagandiniu aparatu, ir, be abejo, pažadai apie nepriklausomas valstybes buvo dalijamos kairėn ir dešinėn. Bet kalbėti apie tolesnę perspektyvą, apie savo nepriklausomų valstybių atkūrimą – tai naivu, nes jeigu ketino germanizuoti ir ieškojo vokiečių pėdsakų net Rusijos šiaurės-vakaruose (pvz., žurnale “Rodina” (“Tėvynė”) straipsnyje “Riuriko auksinis herbas Volchovo džiunglėse” aš pasakoju, kaip vokiečių archeologai ieškojo čia ankstyvųjų viduramžių Vokietijos kultūros pėdsakų), tai ką gi jau pasakysi apie Baltijos šalis?

- Kokios buvo pasekmės žmonėms (ypač politikams), bendradarbiavusiems su fašistais, Vakarų Europos šalyse ir TSRS po Antrojo Pasaulinio karo pabaigos?

- Dėl to turiu tokį jausmą, kad Rusijoje Stalinas vykdė rimbo politiką, o Baltijos šalyse - riestainio bei rimbo politiką.

Žiūriu 1960-ųjų dokumentus apie baudėjus, žmones, dalyvavusius Rusijos gyventojų naikinime: netikėtai tardytojas atskleidžia, kad žmogus buvo “miško broliu”. Tardytojas rašo apie tai, o aukštesnisis tovarišius užrašo rezoliuciją su tokia prasme: taip, šitas žmogus buvo miško broliu, bet kadangi jis savarankiškai, savanoriškai išėjo iš miško (jiems reguliariai buvo suteikiama galymybė grįžti prie taikaus gyvenimo, buvo siūlyta sudėti ginklus), tai tardytojai negali laikyti nusikaltimu jo dalyvavimą toje ginkluotoje formuotėje.

Deja, mūsų geri draugai ir sąjungininkai, JAV ir Didžioji Britanija, TSRS atžvilgiu nuo pat pradžių vykdė fariziejišką politiką: iš pradžių jie bovo pasiruošę susitikti su Stalinu Teherane, Jaltoje, Potsdame, mus laikė sąjungininkais. Bet kaip tik karas pasibaigė, tuoj pat jų požiūris Baltijos šalių klausimu kiek pasikeitė: jie paskelbė apie gana didelį kvotų lengvatinėmis sąlygomis kiekį emigrantams – Lietuvos, Latvijos ir Estijos piliečiams (šių kvotų kiekis buvo tiek didelis, kad per kelerius metus pas juos į Vakarus galėtų persikraustyti beveik visi Baltijos šalių gyventojai).

Jei grįžtume prie istorijos apie Žestianają Gorką (Skardinį Kalną), tada Amerikoje, Vakarų Vokietijoje, Australijoje čekistai nustatė kelis žmones, dalyvusius taikių gyventojų naikinime, bet niekas iš jų nebuvo išduotas, ir nieko iš šių baudėtojų taip ir nepavyko patraukti baudžiamojon atsakomybėn. Atsidūrę Vakaruose, atsispirdami nuo teiginio, kad jų šalys 1940 m.buvo okupuotos Sovietų Sąjunga, šie žmonės sugebėjo legalizuotis už Sovietų įtakos ribų.

Tuo tarpu, Europoje kolaborantus visur traukdavo atsakomybėn, ir kuo geriau jautėsi vokiečiai toje ar kitoje teritorijoje, tuo grežtesnių priemonių kolaboravimo atžvilgiu ten ėmėsi po karo pabaigos. Prisiminkime, kad prancuzų, norvegų kolaborantų lyderiai buvo sušaudyti. T.y. Europa negailestingai susidorodavo su visais, kas bendradarbiaudavo su hitlerininkais, stengdamasi kartais pasirodyti uolesne katalike, negu pats Popiežius.

- Kaip žinome, Baltijos šalių vystymosi sovietinis laikotarpis vertinamas ten dabar, kaip “okupacija”. Atitinkamai, pagal šią teoriją, visi tų laikų valstybiniai organai, visa nomenklatūra, visi partijos, komjaunimo nariai ir t.t. yra kolaborantai, sovietinio režimo bendrininkai?

- Turiu tada priešpriešinį klausimą: jeigu sutiktume si šiuo teiginiu, tai visi sovietinio laikotarpio dokumentai turi būti pripažįstami neteisėtais. Jūs atsitiktinai negirdėjote, ar buvo Baltijos šalyse nors vienas atvejis, kai nors vienas iš mokslų kandidatų, mokslų daktarų, specialistų su aukštuoju išsilavinimu, pavyzdžiui, tas pats Landsbergis – atsisakė savo sovietinių diplomų, laikydami juos okupaciniais dokumentais?

- Sovietinių diplomų, kiek prisimenu, niekas neatsisakė, ir oficialiose biografijose informacija apie sovietines mokslo laipsnius būtinai nurodoma: pavyzdžiui, disertacijos, kurioje atvirai pripažįstami Sovietų valdžios Lietuvoje pasisekimai, dėka, prezidentė Grybauskaitė turi dabar Europos socialinių mokslų daktarės laipsnį. Beje, tuo pat metu, garbės donoro vardas, suteiktas sovietiniais metais, toje pačioje šalyje nebepripažįstamas…

- Žinote, tai net truputį juokinga. Kaip sakė vienas satyrikas: čia skaitome, čia neskaitome, o čia silkę suvyniodavome.

Terminas “kolaboravimas” numato, kad kažkas su okupantais bendradarbiauja, o kažkas stengiasi išgyventi. Jei pažiūrėtume, kiek žmonių Baltijos šalyse bendradarbiavo su “okupacine” valdžia, argi daug buvo atsisakymų tarnauti “okupacinėje” kariuomenėje, dirbti “okupaciniuose” valdžios organuose, partijoje?

- Šio mėnėsio pradžioje Lietuvoje buvo įkurta Sovietinės okupacijos tyrimo asociacija. Steigiamajame šios Asociacijos sisirinkime Lietuvos konservatorių patriarchas Vytautas Landsbergis pareiškė: “Problemos prasideda nuo pavadinimų ir nuo vartojamo žodyno, nes jau čia atspindi konceptualūs politinės istorijos klausimai (…) Eina ir eina įvairių dalykų, iš užsienio šalių nusistebėjimų, kur yra gimę žmonės, gimę, pavyzdžiui, 1950 metais. Kur nors Vakaruose nustato - gimę Sovietų Sąjungoj (…) Nusistatykime, įveskime, jei reikia, įstatyminę formulę, kad 1950 metais gimęs žmogus yra gimęs okupuotoj Lietuvoj. Ne Sovietų Sąjungoj, ne LTSR, o gimęs okupuotoj Lietuvoj. Jei mes įtvirtinome įstatymiškai pasipriešinimo statusą kaip vienintelės teisėtos valdžios Lietuvoje, tebesančios ir kovojančios prieš okupantą, (...) tai neturime nusižengti tiems principams. O esame įklimpę kažkur pusiaukelėje su tokiais savo sudėtingumais arba su stoka nuoseklumo.”

Kaip Jūs vertinate tokias iniciatyvas? Galbūt Lietuvoje tikrai reikėtų ne nusižengti principams ir pasmerkti visus kolaborantus, kaip tai buvo padaryta su fašistų bendrininkais Europoje?

- Žinote, buvusis komunistas Algirdas Brazauskas vis dėlto net buvo Lietuvos prezidentu. Tą patį galima pasakyti ir apie Estijos ministrą pirmininką Andrusą Ansipą, ir dar apie daugumą kitų Baltijos šalių aukštas postus užimančius politikus. Tai yra kažkoks akivaizdus atrinkimas.

- Lietuva pirminikauja Europos Sąjungai, ir šiomis dienomis sužinojome, kaip “seni” ES nariai supranta tokią Baltijos šalių retoriką. Europos Parlamento pirmininko pavaduotojas Migelis Martinezas įtarė Baltijos šalių europarlamentarus, agresyviai pasisakančius už nacizmo ir komunizmo sulyginimą, primityvu oportunizmu. Šiuo metu ES ribose būtent Baltijos šalyse yra didžiausio nepasitikėjimo šaltinis. O kaip atsimename, Europos Sąjunga juk buvo kuriama būtent savitarpio pagrindinių Europos šalių pasitikėjimo pagrindu. Kokias pasekmes tokios sąmoningos istorijos politizacijos Jūs įžiūrite? Kur tai nuves Baltijos šalis?

- Lengviausia visose savo bėdose kaltintinti kaimyną. Tarpukario Lietuvos, Latvijos, Estijos vystymosi laikotarpis – 20 metų. Jų pokarinis vystymosi laikotarpis – tai vos daugiau nei 40 metų. Ir jei galėjome 1980-ųjų pabaigoje kuo nors apkaltinti Sovietų Sąjungą, tai galėjome įsiklausyti į tai, bet praėjo jau daugiau nei ketvirtis amžiaus!

Tada kalbėjo apie okupaciją, Sovietų valdžios kaltę ir t.t., tikėdamasi sukurti rojų ant žemės (Rusijoje buvo panašių kalbų, bet Baltijos šalyse jų, turbūt, buvo daugiau), bet praėjo 25 metai, o rojaus ant žemės taip ir nebėra, visos Baltijos šalys turi savo rimtų problemų. Ir esant šioms problemoms politikai stengiasi groti senais nuvalkiotais instrumentais: “Ne mes esame dėl visko kalti, ne ta visuomenė, kurį sukurėme, o tai, kad prieš daug metų mus padarė tokiais vargšais ir nelaimingais”. Tuo metu į realias problemas niekas nekreipia jokio dėmėsio.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 15 — id: `scraped:rubaltic_lt:0b218594fe8005c7`

**Title:** Michailas Chazinas: Vilniaus viršūnių susitikimo žlugimas – ES krizės pasireiškimas

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos sostinėje buvo duotas atsakymas į paskutinių mėnėsių pagrindinę Europos politinę intrigą. Vilniaus Rytų partnerystės viršūnių susitikimas pasirodė nesekmingas - sutartis dėl Ukrainos asocijuotos narystės ES jame nebuvo pasirašyta, nepaisant daugybės pirmųjų ES asmenų kuluarinių derybų su prezidentu V.Janukoviciumi. Be to, dar prieš kurį laiką iki viršūnių susitikimo analogiško dokumento su ES parafavimo atsisakė Armenija. Visos šios diplomatinės Briuselio nesekmės tai yra visuotinės krizės pasireiškimas, kurį pergyvena ES, įsitikinęs žinomas Rusijos ekonomistas, konsultacinės kompanijos “Neokon” prezidentas Michailas Chazinas. Be to, eksperto nuomone, išeitimi iš šios krizės būtų ne ES plėtimasis, o jos “sugriuvimas” ir jungimasis naujomis sąlygomis, kurios būtų adekvačios pasaulio ekonomikos sunkumams.

- Michailas Leonodovičius, Vilniaus Rytų partnerystės viršūnių susitikimas baigėsi niekuo. Kijevas tęsia savo mėginimus sėdėti ant dviejų kėdžių, o Briuselis - palikti tik vieną Europos kedę. Kodėl, Jūsų nuomone, Europai taip reikalinga Ukraina?

- Reikia, kad Ukraina nebūtų susijusi su Rusija. Reikalas tas, kad visa šiuolaikinė Vakarų politinė kultūra gyvena tokių mitų kūrinių rėmuose, kurie buvo sukurti 1970-1990-aisiais. Ypač ryškiai tai aprašė Brzezinski, kuris iškėlė tezę, kad kol Rusija yra su Ukraina, tai pasaulinio masto politinis žaidėjas, o Rusija be Ukrainos – tai jau antraeilinė Azijos valstybė. Teisinga tai ar ne, šiuo atvieju, nėra principinga. Svarbu, kad tai yra politika, kurios laikosi šiuolaikinės Vakarų elitos.

Bet čia reikia pasakyti ir apie subtilesnius aspektus: daugelis toliaregių politikų, tarp jų ir Brzezinski, pastaruoju metu jau kalba apie tai, kad Vakarų uždavinys dabar – pakelti Rusiją, nes reikalinga natūrali geopolitinė atsvara Kinijai Eurazijoje. Indija dabar nėra tokia atsvara.

Remdamasis šiuo aspektu, galiu pamanyti, kad daugelis Amerikos politikų yra pasiruošę geopolitine prasme atiduoti Ukrainą Rusijai. Taip pat reikia suprasti, kad šiuolaikinė Europos Sąjunga savo politiniu mąstymu yra giliai provinciali, juk ji gyvena dešimties metų senumo realijomis. Tam yra kelios priežasčių. Tai susiję ir su Briuselio biurokratija – bet kuri biurokratija yra baisiai konservatyvi. Be to, tai susiję su tokiu dalyku: ateitis kuriama atskirais asmenimis, kurie paskui save patraukia mases, o Europoje viską sprendžia konsensusas, todėl šie atskiri asmenys yra priversti sekti paskui mases.

- Iš tiesų, net Timošenko klausimu buvo pastebimi skirtumai tarp JAV ir ES Rytų valstybių narių. Vašingtonas užėmė principingą poziciją, pagal kurią Sutarčio pasirašymas yra neįmanomas be opozicionierės paleidimo, o Lietuva kaip ES pirmininkaujanti šalis, sužlugdė analogišką rezoliuciją Seime ir net nusprendė, kad tai bus žalinga Ukrainos ateičiai Europoje. Pasak Jūsų, šios šalys jau atsilieka nuo JAV užsienio politikos?

- Visiškai teisinga. Yra daug dalykų, kuriuose JAV nubėgo nuo ES. Pavyzdžiui, Sirija. Kemeronas sako: “Mums reikalingas karas Sirijoje”. Net Chilari Klinton sako, kad karas Sirijoje reikalingas. O Obama sako, kad karas nereikalingas. Kodėl? Todėl, kad Obama žiūri į priekį ir supranta, kad JAV šįo karo jau neišlaikys. Dėl situacijos su Timošenko, norėčiau atkreipti jūsų dėmėsį: Vokietija iki paskutinės dienos nesakė, kad pasirašys sutartį.

Su Rytų Europa taip pat viskas aišku. Lenkai irgi, žinoma, kuluaruose sako: “Dešiniakrantė Ukraina – tai mūsų Lenkijos teritorija”. Užtat reikia priversti Ukrainą pasirašyti asociacijos sutartį, visiškai sugriauti ten ekonomiką, įstumti gyventojus į totalinį skurdą ir ramiai atgauti savo teritoriją - dešiniakrantę Ukrainą.

- Tai geopolitiniai motyvai, o kokie yra ekonominiai?

- Šiuolaikinė Europos Sąjunga turi baisių probemų, kurios nuostabiai primena TSRS 1980-ųjų pabaigos problemas. Užtat krizė jau tokia didelė, kad gyventi su senuoju taisyklių ir įstatymų sąvadu jau nebeįmanoma. ES neturi mechanizmų gyvenimui krentančios ekonomikos sąlygose, prasideda išcentrinės tendencijos. Todėl vienintelis dalykas, kuris gali sutvirtinti Europos Sąjungą, tai plėtimosi ideja.

Tuo pat metu jie nesuvokia, kad Ukraina dabar sunkiausioje ekonominėje padėtyje ir jos lokalinis atsisakymas nuo eurointegracijos buvo sąlyguotas tuo, kad Rusija aiškiai leido suprasti: lengvatos asocijuotiems Europos Sąjungos nariams netaikomos. Tai reiškia, kad Ukrainos niekas neketino nuskriausti, iš jos tiesiog norėjo atimti lengvatinį statusą, o tai jos dabartinėje ekonominėje padėtyje nepriimtina. Tas pats Janukovičius juk net neskaitė šios Sutarties, jis veikė vadovaujantis savo ideologine dogma, o Ukrainos elitos ideologinės dogmos yra susijusios su Europa. Bet kaip tik jam paaiškino realybę – atvažiavo Glazjevas, parodė jam pabrauktus geltonu konkrečius sutarties punktus, kurious jis ruošėsi pasirašyti, ir paaiškino, kas iš to išeis - Janukovičius atsisakė.

- Asociacijos sutartis taip ir nebuvo pasirašyta Vilniuje, o tai reiškia, kad nebuvo pasiekti nei ekonominiai, nei geopolitiniai Europos tikslai. Jūs įvertinate šį fakta, kaip Europos Sąjungos užsienio politikos krizės pasireiškimą?

- Žinoma. Bet ne tik pačios užsienio politikos krizės. Juk užsienio politikos krizė tai tik vienas iš Europos Sąjungos krizės išreiškimų kaip modelio: tai ekonomikos problema, tai santykių šalių viduje problema, tai skolų problema.

- Bet jeigu Ukraina pratęs eurointegracijos kelią, akivaizdu, kad šios šalies vadovybė nebus tokia nuolaidi, kaip, pavyzdžiui, Pabaltijos šalių politikai. Kijevo nenuspėjamumas aiškiai pasireiškė net ryšium su pačiu Rytų partnerystės susitikimu. Kaip Jūs manote, ES nesuvokia arba nebijo to, kad Europa gali būti užkrėsta politinio proceso ukrainizacijos virusu?

- Europos Sąjungoje jau yra problematiškų Briuseliui šalių. Lenkijoje yra reali nacionalinė elita, kovojanti už savo interesus. Dar yra Vengrija, kuri jau praktiškai pradeda gąsdinti atviru šantažu. Ir ten, tarp kitko, taip pat labai stipri nacionalinė elita.

Dar viena problematiška Briuseliui šalis – Graikija. Čia viskas aišku, Graikijoje tiesiog didžiausia skolų krizė. Problematiška šalis tap pat ir Ispanija su savo 60% jaunimo nedarbingumu.

Žinoma, yra dar Didžioji Britanija su savo problemomis, Škotija ir pastovi konfrontacija su kontinentinėmis elitomis.

- Ryšium su Ukrainos ir ES asociacija daugiausia svarstoma, kas iš politikų ką peržaidė. Bet būtų įdomiau sužinoti laimėjo ar pralaimėjo Ukrainos visuomenė dėl to, kad Sutartis taip ir nebuvo pasirašytas Vilniuje?

Bet problema yra kita, juk Sutartį galima perrašyti, kad ji nebūtų pavergianti. Šioje situacijoje pralaimėjo absoliučiai visi, nes negalima eiti į priekį, žiūrint atgal. Visos šios idėjos apie Europos Sąjungos plėtimąsi, asocijuotą narystę ir t.t. rodo, kad viskas bus taip, kaip anksčiau. O mes įžengėme į visiškai kitą būseną – ekonominė krizė tęsis, gyventojų gyvenimo lygis kris ir t.t.

Aš vos prieš kelias dienas parašiau straipsnį apie skirtumą tarp Europos Sąjungos ir Muitų Sąjungos. Jame aš parašiau, kad pagrindinė ES problema yra ta, kad per pastaruosius dešimtmečius buvo sukurtas įstatymų leidybos korpusas, reikalaujantis tam tikro resurso turėjimo, leidžiančio perskirstymą Sąjungos viduje.

Jeigu atlikti visą šią darbą, tada aš laikau galimu, kad į ES pateks tos šalys, kurios anksčiau nebuvo jos nariais. Bet taip pat įvyks ir tai, kas Briuseliui būtų žymiai baisiau – dings eurobiurokratija.

Muitų Sąjungos teritorijoje būtent toks darbas ir buvo įvykdytas 1988-1991-aisiais. Sužlugo ESPT, vėliau TSRS, o dabar vyksta “surinkimas”, bet visai kitomis sąlygomis. Štai Europos Sąjungai reikia, sąlygiškai tariant, sužlugti, o po to atsisėsti ir kartu parašyti naujus Europos Sąjungos principus, atsižvelgiant į dabartinę situaciją.

Перевод стать: Ольга Аксёнова.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 16 — id: `scraped:rubaltic_lt:14a714cd9391bd65`

**Title:** Elitinė neurozė: Lietuva ant vidaus politikos krizės slenksčio?

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Oficialų startą eilinės prezidentų rinkimo kampanijos Lietuvos elita sutiko būdama toli ne pačioje geriausioje būklėje. Valstybės vadovė pasiteisina dėl Rusijos žiniasklaidos “spėliojimų”, vyriausybė kritikuoja specialiąsias tarnybas už teisinį “beteisiškumą”, Seimo pirmininkė eina į beveik atvirą konfliktą su Grybauskaite. ES pirmininkaujančios šalies horizonte pasirodė politinė krizė.

ES Tarybai pirmininkavimas ir demokratinis “švietimas” Rytų partnerystės šalyse turbūt pasirodė Lietuvos politikams ne tokia lengva našta, kaip buvo manoma anksčiau. Atrodo, kad šalies vadovybė pasineria į politinę neurozę. Kaip kitaip dar galima paaiškinti daugelį paskutinių įvykių?

Negali nenustebinti jau tas faktas, kad Lietuvos prezidentė, juo labiau nuolat raginanti išsaugoti maksimalią distanciją santykiuose su Rusija, staiga komentuoja “mintis garsiai”, paskelbtas keliomis dienomis anksčiau mūsų nedideliame portale, be to jau gavusiame nuo Lietuvos specialiųjų tarnybų “Kremliaus ruporo” žymelę. Straipsnyje “Ko bijo Grybauskaitė arba VSD persišovimas” RuBaltic.Ru tik garbingai prisipažino, kad Lietuvos prezidentės baimės pastatė redakciją į keblią padėtį: juk atrodė, kad visi nepatrauklūs Lietuvos realijose faktai iš Dalios Grybauskaitės biografijos jau buvo iškelti viešumon, ir todėl liko tik spėlioti, ką gi dar labiau siaubingą galima paslėpti šioje situacijoje. Kaip paprasta prielaida buvo pažymėta, jog itin teoriškai šiuo “siaubingu” galėjo būti, pavyzdžiui, būsimos Lietuvos lyderės ryšiai su KGB studijavimo Leningrade metu. Portalas išvis neteigė, kad viskas buvo būtent taip; be to galima suprasti bet kurio žmogaus norą neišstatyti visuotinei apžvalgai kai kuriuos savo praeities momentus, bet vienas momentas taip ir lieka neaiškus, kaip nesuk:

Tai vis daugiau primena neurozę, sustiprinamą sąlygose, kai nelieka racionalių, blaivių argumentų. Panašiai jau buvo atsitikę Lietuvai ir anksčiau: 2008 m., kada laikraštis “Kurier Wilenski” buvo “nubaustas” vien už Lenkijos profesoriaus Kšištofo Bukovskio straipsnio “Lenkų ir lietuvių požiūris į laikotarpį tarp Pirmojo ir Antrojo pasaulinio karo” publikavimą. Tada laikraštis neteko valstybės finansinės paramos. 2012 m. kilo kitas skambus informacinis skandalas, kai Rūtos Janutienės laidos apie D.Grybauskaitės praeitį numatyto išėjimo dieną vaizdo įrašas nebuvo prileistas prie eterio, o jos autoriai po to neteko darbo. Dabar gi panaši atvejai vyksta “vorele” vienas po kito: uždrausti PBK, prispausti “Komsomolką”, padaryti kratas BNS žurnalistų namuose. Be to, jeigu pirmuosiuose dviejuose atvejuose Lietuvos politikai gali pasiteisinti “šventu karu” su Kremliaus propaganda, tai Baltic News Service atveju praranda prasmę net ir šis argumentas – ši agentūra priklauso skandinavų kapitalui.

Ir čia darosi aišku, kad VSD “slapta pažyma” tapo daugiau, negu paprasta pažyma, ji pažadino politinę stichiją, kurią Lietuvos vadovybei, matyt, nepasiseka sutramdyti. Šios stichijos simboliu jau tapo to pačio BNS žurnalistai, plojantys prie STT pastato, kaip 2011 m. Baltarusijos opozicija Minske, Lietuvos specialiųjų tarnybų “sėkmėms” kovoje su plunksnos ir klaviatūros darbuotojais. Įdomu tai, kad po susitikimo su Dalia Grybauskaite Specialiųjų tyrimų tarnybos direktoriaus pavaduotojas Židrūnas Bartkus visgi atsiprašė žurnalistų, o pati valstybės vadovė pareiškė, kad STT turi atlikti savo veiksmų tarnybinį patikrinimą. Labai keisti žingsniai, atsižvelgiant I tai, kad Lietuvos specialiosios tarnybos yra pavaldžios prezidentei, o šių struktūrų vadovai – D.Grybauskaitės statyniai.

Situaciją sustiprina dar ir akivaizdūs D.Grybauskaitės “geranoriai”, tokie, kaip naujoji Seimo pirmininkė Loreta Graužinienė. Artima Viktoro Uspaskicho bendražygė visais savo veiksmais tarsi primena prezidentei “juodosios buhalterijos” bylą, pridėdama savo absurdo žiupsnelį į situaciją, kuri susiklostė “viršuje”. Seimo pirmininkė nepraleidžia nė menkiausios progos įgelti D.Grybauskaitei: tai išbara ją už svarbių tarptautinių renginių “pravaikštas”, arba pavadins prezidentu patekusį į nemalonę Paksą. O išskyrus šių smagių “pokštų” L.Graužinienė atvirai veda Seimą į ataką prieš Lietuvos prezidentės kompetencijos sferą ir D.Grybauskaitės žmones: praeitą savaitę parlamente nepaisant konservatorių pastangų, buvo priimti įstatimų pakeitimai, kurie leis atleidinėti generalinį prokurorą, jeigu deputatai nepatvirtino jo metinės ataskaitos. Grybauskaitė jau pavadino šias pataisas nekonstitucinėmis, bet generalinio prokuroro D.Valio ataskaita dar anksčiau nebuvo patvirtinta tautos išrinktaisiais, ir Seime jau ruošiamas nutarimo projektas, kuriame prezidentei siūloma atleisti generalinį prokurorą iš darbo.

Bet netgi jeigu išeis, kad Lietuvos prezidentė iš tiesų “draugavo” su KGB, dangus nesugrius ant žemės: Džordžas Bušas vyresnysis - buvęs CŽV direktorius, V.Putinas – buvęs FSB direktorius. Ir niekas neslėpė šių prezidentų biografijų momentų. Net ir Lietuvai tokia praeitis ne naujiena: pavyzdžiui, KGB rezervistais buvo VSD ex-direktorius Arvydas Pocius ir buvęs VRM vadovas Antanas Valionis. O buvusių čekistų, kaip visi žino, nebūna. Laikas jau priprasti.

Перевод статьи: Ольга Аксёнова.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 17 — id: `scraped:rubaltic_lt:1ab26bf23dbcac15`

**Title:** Ko bijo Grybauskaitė arba VSD persišovimas

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Eilinins skandalas, dėl Rusijos grasinimo  Lietuvai ir klastingos RF prezidento administracijos, kuri esą nukreipia visas specialiųjų tarnybų jėgas prieš Vilnių, sukėlė daugiau klausimų negu davė atsakymų, akcija, planuojama kaip prevencinis smūgis, apginantis Lietuvos elitą, skaudžiausiai suduoda patiems politikams iš Vilniaus.

Informaciniuose pranešimuose, paskelbtuose delfi.lt svetainėje, nuo kurių ketvirtadienį ir prasidėjo skandalas, gausu prieštaravimų, lyg jie būtų parašyti paskubomis. Iš pradžių medžiagos autoriai, pasiremdami VSD, įtikinėja, jog “Rusijos specialiosios tarnybos gavo užduotį organizuoti archyvuose aktyvią paiešką informacijos , kompromituojančiios buvusius Sovietų Sąjungos tarnautojus, kurie dabar užėmia aukštus postus”. Po to nepastebimai (atrodo, netgi ir jiems patiems) žurnalistai keičia savo nuomonę ir pradeda tvirtinti, kad “Rusijos naudojami metodai vykdant atakas bus įprasti – dezinformavimas ir kompromitavimas per padirbtų dokumentų paskelbimą neva rastų Rusijos valstybiniame archive ir “atrastų” naujų liudininkų parodymus”.

„Matyt, net ir visur esantis Lietuvos Valstybės saugumo departamentas vis dar neapsisprendė iki galo, ar kruvini Rusijos “gebešnikai” privalo rasti netikrus liudininkus ir padirbtus dokumentus, arba iš tikrųjų rasti nepatrauklus Lietuvos politikų biografijos puslapius po archyvų dulkių karta? O jeigu vis dėlto reikalinga tam tikra archyvinė klastotė, tai kam tada jos siųsti spec.tarnybas?

Bet labiausiai stebina Vilniaus reakcija į ruošiamą „provokaciją“. Išėjo gana komiškai. Lietuvos politikai pasirodė kaip cirko artistai iš animacinio filmuko apie Funtiką, kurie, slėpdami paršelį, iš anksto pareiškė detektyvams : „Su nusikaltėliu Funtiku aš nepažįstamas!“ Taip pat Vilniuje staiga pasklido informacija, kad greitai apie prezidentę ir kitus Lietuvos politikus bus paskelbta informacijos apie jų sovietinę praeitį, bet tai esą vien melas ir provokacija! Kaip galima kaltinti sufabrikavus faktus, kurių dar net nėra?

Ir atrodo, ši paslaptis nėra tokia paprasta, kad jau kelia šitokią antirusišką isteriją dar jos neatskleidus. Ypač turint omeny, kad apie D.Grybauskaitę ir taip žinoma gana daug iš jos “sovietinės biografijos“ puslapių, kurie nepuošia jos Nepriklausomos Lietuvos gynėjos imidžą.

Vadinasi, tie faktai, kurių taip bijoma Vilniuje, kur kas įdomesni, negu, tarkim, visiems žinoma istorija, kad D.Grybauskaitė iki 1990 metų dėstė politinę ekonomiką Vilniaus aukštojoje partinėje mokykloje ir buvo aktyvi Komunistų partijos narė.

Matyt, tie faktai baisesni ir už informaciją, kad prezidentės tėvas dirbo NKVD. Kad ir paprastu milicininku, bet tai esą nelabai svarbų faktą prezidentė ilgai slėpė. Juk kaip nežiūrėsi Lietuvos elitos akimis, NKVD raidžių derinys yra tarsi „sovietinės okupacijos“ sinonimas.

Tikriausiai nauji Maskvos archyvų duomenys D.Grybauskaitei yra baisesni net už tai, ko Lietuvos žiūrovai taip ir nepamatė 2012 m. per TV3. Vos prieš metus Lietuvos ekranuose turėjo būti parodyta žurnalistės Rūtos Janutienės sukurta laida „Paskutinė instancija“. Šioje laidoje esą ketinta papasakoti apie tai, kad Lietuvos vadovė neva turi lenkiškas šaknis ir kad Lietuvai paliekant Sovietų Sąjungą D.Grybauskaitė ne tik nekovojo dėl šalies Nepriklausomybės, bet net ir nepritarė siekiui suformuoti nacionalinės pakraipos politinį elitą.

“Tai, ką jūs netrukus išgirsite, jau iš tikrųjų ne kartą stengėsi atskleisti”, - taip buvo anonsuota šita “Paskutinės instancijos” laida. Tačiau laidos taip ir nepasirodydavo eterije, straipsniai – laikraščių puslapiuose. Napasirodė eterije ir ši laida. Ji buvo uždrausta esą neetiška, o po to TV3 ir visai nutraukė sutartį su Rūtą Janutienę. Tačiau filmas pasirodė internete ir tapo visuomenės nuosavybe.

Galbūt tai bus, pavyzdžiui, apie įtartinai ilgą D.Grybauskaitės studijavimą universitete? Į Leningrado valstybinį A.Ždanovo universitetą, Ekonomikos fakultetą, ji įstojo 1976 m., o pabaigė jį tik po 7 metų 1983 m. Kas galėjo būsimąją Lietuvos kovotoją su viskuo, kas rusiška ir sovietiška, taip ilgai užlaikyti universitete? Gal KGB kursai, pavyzdžiui?

Lietuvos VSD moka intriguoti. Jeigu ne jų pastangos, dabar niekas nekeltų panašių klausimų. Ir dabar visai nesvarbu, atsiras ar ne tie kompromituojantys archyvo dokumentai.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```
