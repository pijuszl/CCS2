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

### Article 1 — id: `scraped:rubaltic_lt:acda3c800de5710f`

**Title:** Diukovas: norėdamas išsilaikyti valdžioje, Pabaltijo elitas perrašinėja istoriją

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Pabaltijo veiksmuose, liečiančiuose istorinius politikos klausimus, įžvelgiama metodinė sistema: komunizmo ir nacizmo sulyginimas, reikalavimas organizuoti „antrąjį Niurnbergą“ ir išmokėti kompensacijas už „sovietinę okupaciją“. Kodėl pabaltijiečiai taip nuosekliai perrašinėja istoriją, analitiniui portalui RuBaltic.Ru papasakojo Rusijos mokslų akademijos Rusijos istorijos instituto mokslinis bendradarbis ALEKSANDRAS DIUKOVAS:

— Pone Diukovai, akivaizdu, jog Pabaltijo šalių valdžios dirba pagal sisteminį planą. Kame, Jūsų nuomone, glūdi Lietuvos, Latvijos ir Estijos istorinės politikos strateginis tikslas?

— Strateginis šių valstybių politikos tikslas — visų pirma, išsaugoti tą valdžios struktūrą, kuri įsitvirtino Pabaltijo šalyse. Esmė tame, kad be ideologinio pagrindo, be tarybinio laikotarpio istorijos pateikimo išorės okupacijos pavidalu dabartinė Pabaltijo respublikų valdžios struktūra nesugebėtų egzistuoti.

Pirmasis ir pagrindinis Pabaltijo šalių istorinės politikos uždavinys — remti ir išsaugoti ideologinius pateikimus. Būtent todėl ir laikosi dabartinės valdžios.

Antrasis uždavinys — užsienio politikos. Esmė tame, kad Pabaltijo šalys yra ES narės ir joms reikia kuo nors išsiskirti. Jos turi turėti kažkokią savą temą, kuria galėtų pasireikšti Europos Sąjungoje.

Jie negali pasireikšti ekonominėmis temomis, nes sprendimų ekonomikos klausimais centras yra toli nuo šių šalių ribų. Jie negali pasireikšti socialiniais klausimais. O ką jie gali? Lengviausia pasireikšti antirusiška tematika, tokiu būdu keliant savo autoritetą ir džiaugiantis, kad juos pastebėjo.

Taigi temos egzistuoja, ir Pabaltijo šalių valdžios dėl jų kaunasi. Jų deputatai Europos parlamente ir atstovai Europos komisijoje pastoviai šias temas kelia. Tokiu būdu matome savotišką pasiskirstymą darbu.

Akivaizdu, jog blogėjant santykiams tarp Pabaltijo šalių ir Rusijos, blogėja santykiai tarp Rusijos ir ES. Bet ar tai Pabaltijui rūpi? Šių šalių valdžios turi savo konkrečius vidaus politikos, vidaus europietinius ir užsienio politikos tikslus. Rusija šiuo atveju joms vien tik pabaisa.

Aš manau, jog niekas Pabaltijo elite nesitiki ko nors iš Rusijos išpešti (pvz. kompensacijos už okupaciją). Tai — deklaruojantys pareiškimai. Sukuriamos tam tikros pozicijos, jas naudojant viduje ES. Tai daroma sėkmingai ir mūsų — „rusų grėsmės“ — sąskaita.

— Pabaltijo šalių istorinė politika, kaip matome, labai aktyvi, tačiau nesavarankiška ir prikaustyta prie Rusijos. Jos neragina savęs atgailauti dėl Holokausto. Jos ragina Rusiją atgailauti. Ar Jums neatrodo, kad tokia politika yra smunkanti?

— Žinoma! Ir taip yra todėl, kad realizuojant tokius tikslus blogėja santykiai su Rusija, prarandamos ekonominės ir socialinės galimybės. Pasirinkdamas tokią savo vystymosi strategiją, Pabaltijo elitas, be abejonės, kaupia savo šalims didžiulį nuostolį.

— Kai Pabaltijo šalyse bandoma kitaip, ne mechaniškai, pažvelgti į savo istorinę praeitį, viskuo kaltinant Rusiją, tada tie bandymai susiduria su labai griežtu valdžios pasipriešinimu. Paskutinis pavyzdys — rašytoja Rūta Vanagaitė, kuri šiomis dienomis buvo priversta atgailauti dėl parašytų knygų. Kame, Jūsų manymu, čia esmė?

— Palaikyti ideologinę vienybę galima tik slopinant laisvamaniškumą ir įtvirtinant vienodą požiūrį į istorinius įvykius. Žinoma, tokie intelektualai, kaip Vanagaitė, šią ideologinę vienybę ardo. Ir kol Vanagaitė neperžengė Europos Sąjungos reikalavimų rėmų (pokalbiai apie Holokaustą), jos niekas nelietė. Nors jos paliesta tema elitui nebuvo maloni.

Vanagaitė sakė, jog lietuviai dalyvavo Holokauste, tačiau už šią temą jos nebuvo galima smerkti. Bet kai ji pasisakė apie „miško brolį“ Ramanauską–Vanagą, iškart suveikė represinis mechanizmas, verčiantis atgailauti.

Todėl kad „miško brolių“ siužetas — vienas svarbiausių dabartinės Lietuvos siužetų.

Norint atitrūkti nuo minties, jog Lietuvos valstybė žlugo natūraliu būdu, nes to pareikalavo įvykių eiga, dabartiniam elitui reikia didvyrių, kurie vėliau tęsė pasipriešinimą. Tie didvyriai, pirmiausia, neturi turėti tampraus ryšio su naciais ir nacių okupacija, jie turi būti kovotojai už tautos laisvę. Tokioms pareigoms buvo paskirti „miško broliai“ — Ramanauskas–Vanagas ir kiti.

Problema tame, jog „miško broliai“ pirmiausia žiauriai terorizavo taikius gyventojus. Dauguma šių teroro metu nužudytųjų buvo lietuviai.

O jei jau prasideda kalbos, jog „miško broliai“ bendradarbiavo su VRLK organais, tuomet kova dėl nepriklausomybės, kuri turėjo tęstis ir kuri simbolizuoja Lietuvos respublikos garbę, kažkur dingsta. Jei vyriausias vadas savo akademinės karjeros pabaigoje bendradarbiavo su VRLK ir todėl VSK pavyko likviduoti šį judėjimą – kalbėti apie efektyvų nacionalinį pasipriešinimą nėra jokios prasmės.

Tai vienas iš skausmingiausių Pabaltijo valdžių klausimų, ir būtent todėl Vanagaitė dabar koneveikiama daug žiauriau, negu tada, kai ji rašė apie lietuvių dalyvavimą Holokauste – nemalonu tai buvo, tačiau, įtakojant europiečiams, sugebėta nusiraminti.

O štai „miško brolių“ kritika Pabaltijo valdžioms visiškai nepriimtina. O europiečiai neketina įsikišti, nes ši tema jiems neįdomi ir jų neliečia. Na, žudė periferijoje kažkas kažką – jiems tai nė motais.

— Kokių dar priemonių imsis Pabaltijo elitas vėl aštrėjant istoriniams prieštaravimams?

— Aš nemanau, kad artimiausiu metu kils istoriniai paaštrėjimai. Esmė tame, jog istorinė politika 2000 metais išstūmė tikrąją politiką. Iškeldamos istorinius siužetus, Pabaltijo valdžios demonstravo priešiškumą Rusijai, į šią kovą bandė atkreipti JAV ir ES dėmesį. Dabar matome, kad, tame tarpe ir Pabaltijo bei Lenkijos valdžioms dedant pastangas, atsparumas Rusijai pasiekė visiškai kitą lygį. Mes matome, kad Pabaltijo respublikų teritorijose atsirado karinės formuotės.

Istoriniai siužetai liks žaidimų lauke, tačiau jie sudarys, kaip anksčiau, europietiškų šalių politikos pagrindinę esmę. Tai galima akivaizdžiai pamatyti, prisimenant siužetą apie Molotovo–Ribentropo paktą. 2009 metais sukako 70 metų nuo šio dokumento pasirašymo. Ta proga šurmuliavo visa Rytų Europa, o kalbos apie „sovietinę okupaciją“ sklido vos ne iš kiekvieno šaldytuvo. Mes tapome liudininkais didžiulės informacinės kampanijos.

2014 metais, kai Rusijos ir ES santykiai pablogėjo dėl krizės Ukrainoje, mes pastebėjome įdomų reiškinį: Molotovo–Ribentropo pakto istorija ir sovietų–nacių, kaip teigia mūsų oponentai, Europos padalinimo tema ėmė blėsti, praktiškai tapo nereikalinga. Visa tai pakeitė aktualesnis dalykas — šiuolaikinė priešprieša. Taigi praeities pelėsiais apaugusi priešprieša buvo pakeista dabartine ir reale.

Būtent todėl Lenkijoje bus tebeniekinami tarybiniai memorialai – kad sutelktų dešinę elektorato bazę. Dėl šios priežasties dar smarkiau koneveiks tokius žmones, kaip Vanagaitė, — ir tai siekiant išlaikyti ideologinį monolitą. Šios temos bus pareikalautos vidaus gyvenime. Išorei egzistuoja kiti, aktualesni siužetai — tiesioginė priešprieša, kuri bus dienotvarkėje dar daug metų.

— Kaip Rusija turi reaguoti į tarybinių paminklų griovimą, reikalavimus išmokėti kompensaciją už okupaciją ir panašius dalykus?

— Kad reikalavimas išmokėti kompensaciją yra visiškai nerealus dalykas, manau, supranta net tie žmonės, kurie šią idėją pagimdė. Rusija į tai visiškai neturi kreipti dėmesio.

Kas dėl tarybinių karių kapų ir memorialų, čia tikrai susidūrėme su rimta problema, kurios šiuo metu nepavyksta išspręsti. Tai rodo lenkų pavyzdys. Lenkijos valdžios veiksmai visiškai prieštarauja tarpvyriausybinėms sutartims, kurias pasirašė Rusija su Lenkija.

Taigi Lenkija atsisako pripažinti, jog pažeidžia sutartis. Atsakyti Lenkijai tuo pačiu būtų labai keista, nes atsakyti į barbariškus veiksmus ne tiesiogiai, o, sakykim, ekonomikos ar politikos sferose, susiejant tai su praeitimi, taip pat ne visai priimtina. Nes ir taip egzistuoja sankcijos, žemas santykių lygis. Rimtai paveikti juos, deja, nėra galimybių. Čia būtina ieškoti kažkokį kitokį sprendimą, tačiau jo aš kolkas nematau.

Dabar mes žinome, kad Pabaltijy ir Lenkijoje yra žmonių, kurie gerbia mūsų karių atminimą, prižiūri kapines. Man teko buvoti mažuose Lenkijos miesteliuose, jų gyventojai nuoširdžiai prižiūrėjo tarybinių karių, žuvusių vaduojant Lenkiją, memorialus. Šie žmonės neprarado atminties. Atsisakyti tokio išteklio, turbūt, būtų ne visai teisinga. Aš nematau išeities iš šios situacijos.

Ir čia mes matome rimtesnių Rusijos su Rytų Europa ir ES priešpriešos procesų atspindį. Europos Sąjunga Rytų Europos šalių įtakoje vis agresyviau užima antirusiškas pozicijas, nes Rytų Europa turi Europos Sąjungos valdymo akcijų. Kaip esančioje koordinačių sistemoje išeiti iš šios situacijos, aš nežinau.

— Jei atitrūkti nuo istorijos ir šiandieninės Pabaltijo šalių padėties ir prisiliesti prie tos Rusijos istorijos, kuri liečia Pabaltijy, Lenkiją, Vokietiją ir Ukrainą, — prie tų šalių, su kuriomis turime istorinius nesutapimus, — ar yra, Jūsų nuomone, reiškinių, dėl kurių Rusija turėtų atgailauti ir pripažinti savo istorinę kaltę?

— Aš nepritariu samprotavimams apie atgailą todėl, kad atgaila — individualus dalykas, kuris egzistuoja individualiame lygyje. Valstybė negali atgailauti, nes ji nėra žmogus. Egzistuoja kertiniai religiniai įvaizdžiai, ir kalbėti šiuo atveju apie atgailą reiškia primityviai manipuliuoti.

Bet ar tai reiškia, kad reikia pradėti mokėti kompensacijas? Rusija turi įstatymus neteisėtai represuotų žmonių atžvilgiu, kuriuose šie klausimai numatyti. Tai, kas yra už šių įstatymų ribų — tai jau tarpvyriausybinių santykių klausimai. Noriu priminti, kad kompensacijos, kurias Vokietija 1990 metais išmokėjo koncentracijos stovyklų aukoms, atsirado pasirašius tarpvyriausybinius susitarimus.

Jei pabaltijiečių politika kada nors taps tokia, kad Rusija galės tartis su veiksniais žmonėmis, jei Rusija sugebės suprasti, kad šie žmonės, šios valdžios, šios šalys atsisako provokacinių akcijų, kad joms nepriimtina antirusiška politika, esu įsitikinęs, kad kai kurie (toli gražu ne visi) klausimai gali būti išspręsti. Tačiau aš netikiu, kad artimiausioje ateityje tokia galimybė galėtų atsirasti.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 2 — id: `scraped:rubaltic_lt:7498271cd6ec4e7c`

**Title:** Lietuvos  socialdemokratai pripažino: šalyje vyksta „raganų  medžioklė“

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos socialdemokratų partijos (LSDP) pirmininkas Gintautas Paluckas palygino šių dienų situaciją Lietuvoje su makartizmo epocha JAV, kai bet kuris kitaip mąstantis ir simpatizuojantis TSRS buvo persekiojamas ir kaltinamas tėvynės išdavyste.

„Ponas Statkevičius, kaip ir ponia Vanagaitė, švelniai tariant, šauniai pasivaikščiojo po šalį savo pareiškimais. Tačiau reakcija mūsų elito, ypač reakcija visuomenės nuomonės kūrėjo, taip pat šiek tiek neadekvati“, — pasakė Gintautas Paluckas spalio 27 d. Žinių radijo stočiai.

„Istorijai tokios situacijos žinomos. Ypač Amerikoje. Prisiminkime makartizmo laikus, kai senatorius Makartis (50-aisiais XX a. metais — RuBaltic.Ru pastaba) sukūrė ištisą „raudonųjų“ persekiojimo sistemą. Tai reiškė, jog už menkiausią įtarimą bendradarbiaujant su komunistais, o tada vyko Šaltasis karas, žmones kišo į kalėjimus, dėl menkiausio įtarimo varė iš darbo. Tada nukentėjo kelios dešimtys tūkstančių žmonių.

Todėl kai šiandien Statkevičių už jo nuomonę siūloma išsiųsti į Čečėniją — esą, lai ten padirbės ties Kadyrovo įvaizdžiu (galimai turint omeny seksualinę orientaciją) — tai, žinote, jau per daug. Perlenkė lazdą. Tai skaldo visuomenę, ir tai neadekvatu (... )“, — konstatuoja LSDP lyderis.

Dviem dienom anksčiau Statkevičius davė interviu rusų agentūrai Sputnik, kuriame labai kritiškai įvertino tai, kas vyksta Lietuvoje, pareikšdamas, kad valdžia demonizuoja Rusiją ir visiškai nesirūpina savo piliečiais.

Rūtą Vanagaitę pasmerkė už jos pasisakymą apie „miško brolį“ Adolfą Ramanauską-Vanagą, kovojusį prieš Raudonąją armiją. Rašytoja pareiškė, jog, archyvų duomenimis, Ramanauskas-Vanagas bendradarbiavo su VSK ir VRLK. Faktiškai, jos žodžiais, jis išdavė tėvynę ir savo bendrininkus, pakišdamas juos tarybinėms specialiosioms tarnyboms.

Tie, kurie nesutinka su kritiškais vertinimais, pavadino Statkevičių ir Vanagaitę „Kremliaus agentais“. Skandalą išpūtė vedančios žiniasklaidos priemonės, deputatai konservatoriai Arvydas Anušauskas ir Laurynas Kasčiūnas, o taip pat kai kurie visuomenės veikėjai. Jų tarpe — vienas pagrindinių visuomenės nuomonių „formuotojų“ žurnalistas propagandistas Andrius Tapinas.

Šios situacijos apogėjus — viena stambiausių leidyklų „Alma littera“ atsisakė pristatyti naują Rūtos Vanagaitės knygą. Leidykla pareiškė nutraukianti bet kokį bendradarbiavimą su žinoma rašytoja ir išimanti jos egzempliorius iš visų šalies knygynų. Panašiai pareiškė vadovas stambiausio maisto produktų parduotuvių tinklo „Maxima“, kur taip pat buvo galima rasti Vanagaitės knygą.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 3 — id: `scraped:rubaltic_lt:9681acef7c345995`

**Title:** Kova dėl tranzito sugriaus Lietuvos ir Latvijos santykius

**Source:** rubaltic_lt (propaganda)

**Text:**

```
„Lietuvos geležinkeliai“ pripažino, kad Latvija konkuruoja su Lietuva kovoje dėl tranzito: „Baltijos vienybė“ — šaunu, tačiau kaunantis su konkurentais visos priemonės tinka. Bylinėjimaisi teismuose su Latvijos uostais ir „Latvijos geležinkeliais“, reikalavimai atstatyti geležinkelį ir išmokėti Eurokomisijos skirtą baudą, tolimesnė kova dėl tranzito — visa tai gali sukelti Lietuvai konfliktą su paskutiniu iš keturių kaimynų, su kuriuo dar neseniai buvo geri santykiai.

Po daug metų trukusių aiškinimųsi Eurokomisija įpareigojo Lietuvą sumokėti 28 milijonų eurų baudą už išardytą geležinkelį, einantį nuo Mažeikių naftos perdirbimo įmonės link Latvijos. Veiksmai Lietuvos geležinkelių monopolininko „Lietuvos geležinkeliai“, nuardžiusio bėgius, nes esą ten reikėjo atlikti remonto darbus, ir privertusio lenkus — tos įmonės savininkus eksportuoti savo produkciją tik per Klaipėdos uostą, Briuselyje buvo įvardinti nesąžininga konkurencija.

Iškart po Eurokomisijos verdikto paskelbimo į Vilnių atskrido ES komisarė konkurencijos klausimais Margret Vestager, paraginusi Lietuvos vadovybę neaštrinti susiklosčiusios situacijos ir atstatyti geležinkelį. Lietuviai bandė parodyti dantis ir teigti, jog apie tai, jog šiam geležinkeliui būtinas remontas, Eurokomisijai buvo pranešta dar kovą, tad ta komisija, jei ji tokia principinga, lai pareikalauja kompensacijos iš „Gazpromo“ dėl jo „energetinės monopolijos“. Tačiau, eurokomisarei pagrąsinus, pasistengė aprimti.

Lietuvos prezidentė Dalia Grybauskaitė po derybų su eurokomisare konkurencijos klausimais pareiškė, kad geležinkelio atstatymas iki Latvijos stoties Renge „turbūt, neišvengiamas“, o sumažinti baudą gal bus galima tik teisme.

Pagal jai būdingą įprotį, visą kaltę dėl politinio konfūzo Grybauskaitė bandė suversti vyriausybei. „Deja, mes matome, kad ir ši vyriausybė neskuba ieškoti sprendimų, tačiau jų prireiks. Neigti, bandyti kratytis buvusios vyriausybės palikimo ir viešai meluoti, kad viskas tvarkoj, kad darbai vyksta ir viskas bus gerai, — mes daugiau negalime naudotis tokiais metodais“, — pareiškė ponia prezidentė.

Tačiau išvykus reikliai eurokomisarei Lietuvos vadovybė mikliai sutelkė jėgas ir pradėjo kontrpuolimą.

Mantas Bartuška

„Mes kruopščiai išanalizavome EK sprendimą ir turime du mėnesius, kad paruoštume galutinę strategiją kokiais argumentais naudotis. Mums svarbu, kad geri santykiai susiklostė su Orlen (lenkų naftos perdirbimo kompanija, kuriai priklauso Mažeikių NPĮ — RuBaltic.Ru pastaba), mes tebesvarstome, kaip neutralizuoti konfliktą, nes Orlen kroviniai mums labai svarbūs“, — pasakė Bartuška.

Generalinis „Lietuvos geležinkelių“ direktorius paskaičiavo, kad ginčai su Eurokomisija gali pareikalauti iš kompanijos pusę milijono dolerių.

Pirma, 28 milijonų eurų bauda.

Antra, geležinkelio į Lietuvą atstatymas, kuris pareikalautų apie 20 milijonų eurų. (Ir dėl ko? Dėl to, kad tranzitas iš Klaipėdos nukryptų link konkurentų?).

Trečia, remiantis Eurokomisijos sprendimu, Latvija gali pateikti Lietuvai ieškinį dėl nuostolio atlyginimo. Sprendžiant iš Bartuškos žodžių, Vilnius jau laukia „Latvijos geležinkelių“ ir Rygos laisvo uosto ieškinių.

„Verta suprasti, kad latviai — ir broliai, ir konkurentai. Jie gali įvardinti įvairias sumas, mes girdėjome jas labai dideles, bet jei nėra pagrindo, tai ta ieškinių kaina — nulis. Kalbėtis su latviais planuojame artimiausiu metu. Ar padės susitikimai, matysime, tačiau mums svarbu turėti partnerystės, gerus santykius ne tik su Orlen, bet ir su kolegomis latviais“, — pranešė Mantas Bartuška.

Už šių žodžių slypi aštrus Lietuvos transportininkų konfliktas su šiaurės kaimynais. Jei konflikto su lenkais išvengta, sutarus sumažinti naftos produktų tranzito tarifus Lietuvos geležinkeliais, tai konfliktas su latviais dėl šios sutarties paaštrėjo: Latvijoje galutinai suprasta, kad geležinkelis iš Mažeikių buvo išardytas ne dėl remonto, o siekiant atimti iš „Latvijos geležinkelių“ ir uostų krovinių srautą.

Visa tai netiesiogiai pripažino ir „Lietuvos geležinkelių“ vadovas, pasakęs, jog latviai — konkurentai. O konkurencijoje, kaip žinia, visos priemonės tinka. Šiuo atveju Lietuvai. Kiti kaimynai tai žinojo ir anksčiau: Lietuva dešimtmečiais kėlė tarifus krovinių pervežimui į Kaliningrado sritį, kad baltarusių kroviniai būtų nukreipti į Klaipėdą, o ne į Kaliningrado jūrų uostą. Ir štai išaiškėjo, jog nuo nesąžiningos konkurencijos Vilniaus negelbsti ir latvių su lietuviais „Baltijos vienybė“.

„Lietuvos geležinkelių“ vadovybė žadėjo artimiausiu metu imtis beveik prieš dešimt metų išardyto geležinkelio ruožo atstatymo (nuo Mažeikių iki Renge — 19 km), tačiau sprendžiant iš ketinimo teistis su Eurokomisija ir pasiruošimo kautis su latvių kompanija, šis pažadas liks neįvykdytas.

Teistis dėl baudos, atrodo, taip pat rimtai ruošiamasi. „Tai analogo neturintis atvejis, kai byla svarstoma 9 metus. Matosi akivaizdi galimybė sumažinti šią sumą arba visiškai anuliuoti“, — pareiškė „Lietuvos geležinkelių“ generalinis direktorius.

Su Rusija, Baltarusija ir Lenkija Vilniui seniai nėra ko prarasti, tačiau santykiai su Latvija rietenas mėgstančiai Lietuvos vadovybei klostėsi nenormaliai gerai. Bylinėjimaisi teismuose su Latvijos uostais ir Latvijas dzelzceļš, reikalavimai atstatyti geležinkelį ir sumokėti baudą šią „nenormalią“ situaciją ištaisys.

Žodis po žodžio, ir Latvija bus apkaltinta bendradarbiavimu su „Gazpromu“, nes ji nenori pirkti Klaipėdos SGD terminalo produkcijos. O dar ir reikalavimai, kad Ryga prisijungtų prie Lietuvos vadovybės kovos prieš Ostroveco AE ir kad aštrintų santykius su Baltarusija. Beje, dar paistoma, kad Latvijos vadovybė turi ryšių su Kremliumi.

Žiauriai susipykti su ketvirtu iš keturių kaimynų — būtų pelnyta Dalios Grybauskaitės veiklos pabaiga Lietuvos prezidentės poste!

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 4 — id: `scraped:rubaltic_lt:d34d7030d3640d41`

**Title:** Paleckis: dvigubos pilietybės įstatymas nesustabdys emigracijos iš Lietuvos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Dvigubos pilietybės tema Lietuvoje šiandien vėl dienotvarkėje. Premjeras Saulius Skvernelis spalio 17 dieną pareiškė, kad klausimas dėl pilietybės tiems žmonėms, kurie išvyko iš Lietuvos į ES ir NATO šalis, suteikimo bus svarstomas referendume. Dvigubos pilietybės suteikimo emigrantams iš Lietuvos perspektyvas ir demografines  Pabaltijo respublikoje tendencijas analitinio portalo RuBaltic.Ru korespondentas aptarė su Lietuvos politiku, diplomatu, politologu Algirdu PALECKIU:

— Pone Palecki, kaip vertinate valdančiųjų sluoksnių siekį suteikti lietuviams teisę turėti dvigubą pilietybę?

— Panašūs bandymai vyko ir anksčiau. Mano nuomone, to siekiama dėl didžiulės emigracijos iš Lietuvos. Tačiau pats emigracijos neutralizavimo metodas ne visai adekvatus (turiu omeny siūlymus suteikti dvigubą pilietybę).

Ko siekia dvigubos pilietybės įstatymo projekto iniciatoriai? Kad milijonas Lietuvos piliečių, išvykusių iš tėvynės per pastaruosius 20–25 metus, nenutrauktų ryšių su šalimi. O, galbūt, net suskubtų grįžti. Tai galima suprasti. Tauta mūsų nedidelė: apie 3 milijonai visame pasaulyje.

Faktiškai tai reiškia iniciatyvos pabaigą, nes pagal įstatymą dėl referendumo prabalsuoti turi daugiau nei pusė Lietuvos piliečių. O mes gi žinom, jog ketvirtadalis ar net trečdalis šalies gyventojų jau įsikūrė užsienyje — jiems bus labai sunku dalyvauti referendume. Dar daugiau — kad referendumo rezultatai būtų priimti, už įstatymą turi prabalsuoti daugiau nei pusė atėjusių, be to, balsavę „už“ turi sudaryti ne mažiau trečdalio turinčių balso teisę. Ši daugiasluoksnė formuluotė praktiškai neleidžia įsigalioti dvigubos pilietybės įstatymui.

Įstatymo projekte įžvelgiamas ir diskriminacijos elementas. Kuo lietuviai arba Lietuvos rusai ir baltarusiai, kurie išvyko į rytus, — įsikūrė Rusijoje, Baltarusijoje, Ukrainoje – blogesni už išvykusius į vakarus (įstatymo projektas dvigubos pilietybės teisę numato tik su ES ir NATO šalimis — RuBaltic.Ru pastaba)?

— Ar šiuo metu visuomenėje labai aktuali dvigubos pilietybės tema? Ar visuomenėje egzistuoja paklausa?

— Mano manymu, šiuo metu tai ne svarbiausias Lietuvai klausimas. Jis aktualus ne visiems emigrantams. Dviguba pilietybė neišspręs aktualių šalies problemų. Pasaulinė praktika rodo, kad į tėvynę grįžta tik keli procentai išvykusių piliečių.

Kai kuriems žmonėms šalyje šis įstatymas — savotiška nauda. Įstatymo projektą stumiantys politikai, gali būti, tikisi pasipelnyti užsienyje gyvenančių rinkėjų balsais. Tai savotiškas pseudopatriotiškumas.

Būtina sudaryti tokias gyvenimo Lietuvoje sąlygas, kad žmonės nenorėtų iš jos išvykti. Tai būtų veiksmingiausia priemonė.

— Ar šiuo metu daug pastangų dedama, siekiant sumažinti gyventojų emigracijos iš Lietuvos srautą? Mažėja ar didėja šiuo metu migracija? Kas daugiausia išvyksta?

— Žmonės išvyksta bet kurios tautybės. Emigracijos struktūra nacionaliniu principu maždaug atitinka gyventojų struktūrą: apie 80 proc. lietuvių ir 20 proc. kitataučių. Žinoma, emigrantai – jaunimas ir vidutinio amžiaus žmonės. Jiems lengviau išvykti ir pritapti naujoje vietoje.

Net didžiausi Lietuvos valdžios patriotai (jei galima pasinaudoti tokiu terminu) pripažįsta, kad situacija jau menkai kontroliuojama ir ji kelia pavojų lietuvių tautos egzistavimui.

Pagrindinė emigracijos priežastis – deramo pragyvenimo lygio stoka. Neseniai bendravau su savo gera pažįstama – vidutinio amžiaus moterimi. Ji pakankamai išsilavinusi, tačiau šiuo metu šluoja greta Londono vieno žuvų perdirbimo fabriko patalpas ir gauna gana rimtą sumą – apie 800 ar 1000 svarų per mėnesį. Lietuvoje ji uždirbtų keletą kartų mažiau. Tai pagrindinė priežastis.

„Pagrindinė emigracijos priežastis — deramo pragyvenimo lygio stoka“

— Lietuva, lyginant su kitomis šalimis, susikūrusiomis buvusios TSRS teritorijoje, pasižymi gana aukštu pragyvenimo lygiu. Neseniai bevizio su ES šalimis režimo teisė buvo sutekta Ukrainai. Ar galima sulaukti antplūdžio į Lietuvą dėka išorinės migracijos iš potarybinės erdvės? Ar gali lietuvius pakeisti migrantai, sakykim, iš Ukrainos?

— Mažai tikėtina. Šiuo metu Lietuvoje jau gyvena šimtai, o gal ir tūkstantis ukrainiečių ir baltarusių. Tačiau žmonės kaip taisyklė ieško didesnio komforto. Ir tai liudija likimai tų migrantų, kuriuos pagal kvotą atsiuntė į Lietuvą Europos Sąjunga. Šie žmonės neužtrunka Lietuvoje. Paskui jie atsiduria Vokietijoje, Švedijoje. Migrantai naudojasi Lietuva kaip aikštele,  o paskui išvyksta.

Panašiai elgiasi ukrainiečiai, baltarusiai ir moldavai. Nors civilizacijos atžvilgiu jiems čia geriau, nei, pavyzdžiui, atvykusiems iš Afganistano.

Tačiau ukrainiečiai gali įvažiuoti ir į Lenkiją. Lenkų kalba jiems nelabai sudėtinga, o per Lenkiją jie gali važiuoti toliau į vakarus. Vargu ar Lietuva taps masiškos migracijos kryptimi. Nors tam tikrą nišą šie žmonės užpildys. Jie sutinka dirbti už tą atlyginimą, už kurį kai kurie lietuviai jau nenori dirbti.

— Jūs paminėjote kvotas migrantams, kurios egzistuoja daugelyje ES šalių. Ar šiuo metu yra Lietuvoje migrantų iš Artimųjų Rytų, ar jie į Lietuvą nevažiuoja?

— Migrantų yra, tačiau kvota neužpildyta. Lietuva buvo įsipareigojusi priimti apie 1200 žmonių. Buvo priimti keli šimtai, tačiau dauguma šių žmonių išvyko iš Lietuvos. Ir kolkas nėra jokių mechanizmų, sulaikančių migrantus. Bet ar jie reikalingi?..

Vėlgi — materialinės sąlygos. Žmonės jaučia, kad jiems bus geriau ten, kur pragyvenimas aukštesnis, — pavyzdžiui, Skandinavijos šalyse. Tikėtina, jog migrantų srautas didės. Jauni Afrikos žmonės, neturintys darbo, keliaus šiaurėn per Pietų Europą. Dalis jų, žinoma, atvyks ir į Lietuvą.

— Į kurias šalis emigruoja lietuviai? Kur jie dabar pagrindinai dirba?

— Prieš Antrąjį pasaulinį karą lietuviai pagrindinai vyko į JAV ir į Pietų Ameriką, kartais — į Australiją. 1990-ųjų pradžioje populiariomis tapo tos šalys, kuriose pragyvenimo lygis stabiliai aukštas ir kalba nesudėtinga. Dabar, kai paplito anglų kalba, pagrindinės kryptys — Airija ir Didžioji Britanija. Dublinas ir Londonas — tai du miestai, kuriuose lietuvių, manau, daugiau, nei kai kuriuose mažuose ir vidutiniuose pačios Lietuvos miestuose.

Didelis emigracijos srautas pasiekė Švediją ir Norvegiją, kur aukšti atlyginimai. Norvegijoje Lietuvos statybininkai sėkmingai darbuojasi kaip samdomi darbininkai ir kaip statybinių firmų savininkai.

Prieš trejetą ketvertą metų Vokietija susilpnino apribojimus, ir lietuviai ėmė važiuoti ten. 2000-aisiais daugelis emigravo į Ispaniją, tačiau po krizės ten nevažiuoja.

Lietuvos rusai išvyksta ir į Rusiją. Mūsų, taip sakant, „kolonijos“ yra Maskvoje, Sankt-Peterburge, Kaliningrade. Tačiau lyginant su emigracija į vakarus, į rytus išvyksta ženkliai mažiau.

— Žmonės vyksta į Rusiją uždarbiauti?

— Uždarbiauti, mokytis, pas gimines. Žmonės išvyksta į Rusiją dėl materialinių arba psichologinių priežasčių. Ypač po paskutinio rusofobijos protrūkio, tačiau tai nedidelis procentas. Reikia pripažinti, kad dauguma žmonių išvyksta į Vakarus dėl aukšto uždarbio.

— Ar gali rusofobija įtakoti tolimesnį rusų gyventojų skaičiaus Lietuvoje mažėjimą? Ar jis dabar šalyje turi reikšmingą svorį, ar užleidžia antrą pagal tautybę vietą lenkams?

— 1990 metais rusai sudarė Lietuvoje 10 proc. gyventojų, dabar — apie 5 proc., o lenkų — 7 proc. Rusofobija Lietuvoje, ypač po Krymo įvykių, deja, sustiprėjo ir sulaukė valstybinio palaikymo. Valstybinės informacijos priemonės, politikai ir net kai kurie valstybės vadovai remia rusofobiją ir kuria iš Rusijos priešo įvaizdį, o tai padeda sutelkti lietuvišką elektoratą. Tačiau tai pavyksta tik dalinai.

„Laukinė“ rusofobija palietė apie 25 proc. lietuvių protų ir širdžių. Tiek pat žmonių mąsto visiškai kitaip, jie atsparūs propagandai. Ir dar trečdalis gyventojų balansuoja kažkokiame vidurėlyje ir nereiškia jokių ypatingų siekių: lūkuriuoja arba tokiais dalykais nesidomi.

— Ar rusų tautybės gyventojai turi Lietuvoje politinį svorį?

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 5 — id: `scraped:rubaltic_lt:7617196f79c27c3f`

**Title:** Lietuva gavo Klaipėdą taip, kaip Rusija Krymą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Rusijos–Baltarusijos kariniai mokymai „Vakarai-2017“ užsibaigė sėkmingai. Apokaliptiniai visokiausių analitikų, „ekspertų“ ir į prezidentę Dalią Grybauskaitę, Lietuvos krašto apsaugos ministrą Raimundą Karoblį ir jų konservatorišką svitą panašių politikos rėksnių scenarijai apie galimą Pabaltijo šalių užgrobimą, Pabaltijo teritorijų „aneksiją“ ir „karo su Vakarais pradžią“ nepasiteisino, tačiau užmiršti viso to neverta.

Grybauskaitės, Karoblio, buvusios krašto apsaugos ministrės Rasos Juknevičienės, konservatorių Landsbergio, Kaškonio, Kubiliaus, Pavilionio ir daugelio kitų pareiškimus galima vertinti tik kaip melą. Kurstant antirusiškos isterijos aistras ypač pasižymėjo prokonservatoriški žurnalistai ir analitikai. Tarp jų — portalo Delfi karinis korespondentas Saldžiūnas ir „karinis ekspertas“ Karolis Zikaras.

Klaipėdos užgrobimas?

Pastarieji savo publikacijose sausio mėn. iškėlė visiškai kvailą idėją apie galimą užgrobimą lietuviškosios Klaipėdos, nes nemažą dalį jos gyventojų sudaro rusakalbiai. Būtent šis faktorius ir turėtų viską nulemti, nes esą klaipėdiečiai, kaip ir Ukrainos Donbaso gyventojai, karinio įsiveržimo atveju pasiduotų „okupantams“ ir paskelbtų „separatinę nepriklausomybę“.

Žurnalistą Saldžiūną labiausiai pykino tai, jog „Rusijos propagandistai“ pastoviai pabrėžia, kad Klaipėdą su Pajūrio regionu Lietuva savo sudėtyje turi todėl, kad šias žemes Lietuvai padovanojo Tarybų Sąjunga, nors miestas iš esmės niekada nepriklausė Lietuvos Respublikai.

1923 m. vietiniai lietuviai organizavo taip vadinamą sukilimą ir jėga prisijungė miestą. Tuo metu Mėmelis priklausė Tautų sąjungai, o valdė jį prancūzų administracija. Faktiškai miestas buvo Prancūzijos dalis. 1939 metais Hitleris pareikalavo, kad Lietuva grąžintų miestą Vokietijai. Lietuviai pakluso, o po karo Stalinas perdavė miestą Lietuvos TSR.

Ir būtent šie faktai labiausiai erzina „patriotiškai“ nusiteikusius Lietuvos žurnalistus. Ypač jiems nepriimtina mintis, jog Lietuvai kažką galėjo „padovanoti“ TSRS ir Stalinas. Dar labiau jie niršta girdėdami, kai „Kremliaus propagandistai“ tvirtina, jog ir 1923 m. Lietuva prisijungė Klaipėdą ne teisėtai, o karinio įsiveržimo būdu.

Kadangi šiandien oficialusis Vilnius laiko save pasauliniu kovotoju už teisingumą ir tautų nepriklausomybę, o taip pat pagrindiniu „agresyviosios Rusijos, įsiveržusios į Ukrainą“, kaltintoju, pripažinti faktą, jog patys lietuviai mažiau nei prieš šimtmetį pažeidė visas tarptautinės teisės normas ir užgrobė visą regioną, prisidengdami vietinių gyventojų noru prisijungti prie Lietuvos, jam labai sunku.

Rusijos istorikai, žinantys prieškarinio Pabaltijo istoriją, pastoviai primena lietuviams apie ne visai teisėtą Klaipėdos prijungimą, tačiau atsakymą girdi visada vienodą: „Jūs — Kremliaus propagandistai!“

Lietuviškasis krymas

Nepaisant to, Lietuvoje dar yra žmonių, kurie nebijo žvelgti tiesai į akis ir atvirai reikšti, jog Klaipėda buvo prijungta karinio įsiveržimo būdu.

Dauguma taip vadinamo elito atstovų, kaip ir „patriotai istorikai“, šį faktą neigia ir nutyli, tačiau Klaipėdos klausimą netikėtai palietė lietuvių dramaturgas, rašytojas, aktyvus kovotojas už nepriklausomybę, Sąjūdžio narys Arvydas Juozaitis. Neseniai jis pristatė savo knygą „Klaipėdos — Mėmelio paslaptis“. Portalo RuBaltic.Ru korespondentas dalyvavo šiame pristatyme.

Tuos lietuvius, kurie dalyvavo Klaipėdos prijungimo prie Lietuvos operacijoje, Arvydas Juozaitis vadina „žaliaisiais žmogeliukais“ arba „mandagiais žmonėmis“ ir lygina juos su Rusijos kariškiais, kurie 2014 metais užtikrino Krymo prijungimą prie Rusijos.

Dramaturgas paragino Lietuvos visuomenę pripažinti tai, kas tikra, ir nebijoti žvelgti tiesai į akis.

„Klaipėdos sukilimas — ryžtingas manevras lietuvių, susigrąžinusių prarastas baltų žemes. Jei būčiau tuo metu gyvenęs, būčiau taip pat prisijungęs prie tų „žaliųjų“, tiksliau — „rudųjų žmogeliukų“ — tuo metu, kai taip vadinamieji sukilėliai, kuriems vadovavo kadrinis lietuvių kontržvalgybininkas Budrys Polovinskas, slėpė savo, šaulių, mundurus po pilkais kaimiečių rūbais“, — konstatavo Juozaitis, labai nustebinęs klaipėdiečių publiką savo požiūriu ne tiek į Lietuvos istoriją, kiek į šių dienų įvykius Kryme ir Donbase.

Na, o rimti istorikai apie anuos įvykius štai ką sako: Mėmelio arba Klaipėdos sukilimas įvyko 1923 metais Klaipėdos krašte, kuris nuo seno priklausė Prūsijai, o vėliau — Vokietijai. Šio regiono gyventojų daugumą tradiciškai sudarė vokiečiai. Pasibaigus Pirmajam pasauliniam karui, kuriame Vokietijos imperija pralaimėjo, pagal Versalio sutartį kraštas su sostine Mėmeliu atsidūrė Tautų sąjungos žinioje. Trejus metus miestą valdė prancūzų administracija ir faktiškai jis buvo Prancūzijos dalis.

Po Lietuvos Respublikos nepriklausomybės 1918 metais paskelbimo šalies valdžia ilgai mąstė, kaip prijungti šį regioną prie Lietuvos ir įgyti miestą uostą, kuris jaunai valstybei buvo labai reikalingas.

Taip vadinamas sukilimas nesulaukė rimto prancūzų kontingento, vokiečių policijos ir vietinių vokiečių pasipriešinimo. Prancūzų kariškių mieste buvo tik 250, o vokiečiai neketino padėti Prancūzijai: „prolietuvišką“ sukilimą jie vertino kaip puikią galimybę įtvirtinti savo pozicijas, susigrąžinti miestą Vokietijos sudėtin, kadangi Lietuva politine prasme buvo daug silpnesnė nei Prancūzija.

Šiuolaikiniai Lietuvos istorikai stengiasi nutylėti tą faktą, jog sukilimą aktyviai parėmė Tarybų Sąjunga, kuri buvo suinteresuota palaikyti nepriklausomos Lietuvos pozicijas santykiuose su Lenkija. Būtent todėl Prancūzija ir Didžioji Britanija susilaikė nuo karinės operacijos ir grubaus sukilimo numalšinimo, nes TSRS, gindama lietuvius, galėjo įsivelti į konfliktą.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 6 — id: `scraped:rubaltic_lt:d35e2953c19e57ac`

**Title:** Energetinė priklausomybė lietuviškai: Klaipėdos SGD terminalas oficialiai pripažintas nerentabiliu

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvoje oficialiame lygyje pripažinta, jog Klaipėdos plaukiojantis suskystintų dujų terminalas yra nerentabilus. Premjeras Saulius Skvernelis, komentuodamas žlugusias trijų Pabaltijo valstybių derybas dėl bendros regioninės rinkos sukūrimo  dujų klausimu, paragino ieškoti kitų „terminalo naštos sumažinimo būdų mokesčių mokėtojams“.

Premjero pareiškimas tapo disonansu Lietuvos prezidentės Dalios Grybauskaitės interviu, kurį ji davė Delfi portalui – šalies vadovė pavadino plaukiojantį terminalą „laimėjimo istorija, ekonominiu pasiekimu, dėka kurio Lietuva įgijo savą energetinę nepriklausomybę“.

Trijų Pabaltijo valstybių — Lietuvos, Latvijos ir Estijos — derybos dėl bendros rinkos dujų klausimu sukūrimo, kaip buvo tikėtasi, nepasiekė jokio rezultato — labai jau skirtingi šių šalių ekonominiai interesai. Lietuvos premjeras Saulius Skvernelis buvo priverstas pripažinti, jog ta iniciatyva, kurią pastaraisiais metais Vilnius įkyriai piršo savo kaimynams, žlugo.

Pirmuoju atveju Lietuvos valdžia tikėjosi užkrauti kaimynams tą naštą, kuri gulė ant jos pečių išsinuomavus iš Norvegijos plaukiojantį SGD terminalą. Žinoma, tai padaryti reikėjo kaip galima greičiau. Šalyje kasmet mažėja pramoninės gamybos apimtys, o tai įtakoja ir vartojamų dujų apimčių mažėjimą vidaus rinkoje. Ir tai tuo metu, kai Lietuva, pasirašiusi sutartį su norvegų tiekėju Statoil, naudojasi minimaliu į šalį eksportuojamų dujų kiekiu.

Premjeras Skvernelis, komentuodamas situaciją, apgailestavo, kad Latvija šiuo klausimu pasinaudojo pauze, kuri sužlugdė paraiškų EK padavimo terminus. Kaip jis pabrėžė, „norint gauti europietišką paramą, būtina pateikti bendrą trijų Pabaltijo šalių projektą, priešingu atveju mes turime ieškoti kitų būdų, kaip sumažinti naštą mūsų mokesčių mokėtojams“.

Jau praėjus metams po terminalo įvedimo rikiuotėn Lietuvos valdžia sumažino jo apkrovą iki 20 proc. (minimali technologinė apimtis). Valstybė net bandė, pasitelkdama nerinkos mechanizmus, skatinti vidaus rinkoje brangesnių, nei rusiškų, tiekiamų vamzdžiais, dujų naudojimo augimą. Buvo priimtas įstatymas „Dėl suskystintų gamtinių dujų terminalo“, įstatymiškai įpareigojantis stambius pramoninius vartotojus ir komunalines kompanijas pirkti iš SGD terminalo trečdalį reikalingų dujų. Nepadėjo.

Vilniui tapo aišku, kad nepanaudojimas pagal kontraktą numatytų dujų apimčių gresia didelėmis baudomis. Ir ne tik. Dar buvo galima sulaukti bylinėjimosi Europos teismuose. Juk lietuviškasis įstatymas terminalo klausimu pažeidė Europos Sąjungos įstatymą, pirmiausia — pagrindinį konkurencijos principą: „Vartotojas turi teisę laisvai pasirinkti sau tiekėjus, o tiekėjai savo ruožtu turi teisę laisvai aprūpinti vartotojus“. Atitinkamą skundą Eurokomisijai padavė Lietuvos dujininkų asociacija.

Praėjus metams nuo terminalo nuomos pradžios lietuviams teko maldauti, kad norvegai peržiūrėtų sutarties sąlygas, nes šalyje sumažėjo paklausa dujoms. Tada Norvegija pareikalavo, kad Lietuva įsipareigotų pirkti dujas ne penkerius metus, o dešimt — viso 3,7 milijardo kūb. m. (anksčiau — 2,7 mlj). Kilpa užsiveržė dar stipriau.

Energetinis Lietuvos prezidentės Dalios Grybauskaitės „kūdikis“ ne tik atsidūrė agonijos būklėje, bet ir atnešė šalies ekonomikai realų nuostolį. Sandoris su Norvegija iš pat pradžių buvo nuostolingas visais parametrais, tačiau jį sankcionavo pati prezidentė. Kaip pastebėjo Lietuvos Seimo narys socialdemokratas Artūras Skardžius, šios situacijos absurdiškumas tame, jog „nuoma triskart brangesnė nei pats laivas“.

Kaip pažymėjo politikas, „sutarties sąlygos nenumato išankstinio terminalo pirkimo, už kurio nuomą iki 2024 metų teks sumokėti apie 720 milijonų JAV dolerių. Tik tada bus galima tartis dėl jo pirkimo už sutartyje užfiksuotą kainą“. Ir todėl politikas prieina išvados: „šalis galėjo pati pasistatyti tokį laivą, o ne pirkti jį iš pardavėjo, atiduodant jam iš anksto numatytą sumą, tačiau valdžia kažkodėl to nepadarė“.

Ir kaip nustatyti tą nuostolį, kurį patyrė Lietuva dėl prezidentės Dalios Grybauskaitės ambicijų? Jei atsižvelgti į iš anksto pareikštus tikslus, kai buvo tariamasi dėl plaukiojančio SGD terminalo nuomos, — energetinė nepriklausomybė nuo Rusijos — jie nepasiekti.

Beje, Lietuva „pasidžiaugė“, kad ši dalis dabar siekia tik 60 proc., o ne 80 proc. (kaip anksčiau — „Gazpromo“ viešpatavimo metu).

Prapylė Lietuva 2016 metais ginčą su „Gazpromu“ Stokholmo arbitrų teisme, kai reikalavo išieškoti iš šio dujų milžino 1,4 milijono eurų, nes esą 2004–2012 metais permokėjo už pirktas dujas. Beje, lietuviams teisme buvo nurodyta, jog terminas „teisinga kaina“ yra abstraktus, o reikalauti tiekti dujas „žemiausia kaina — beprasmiška“.

Taigi Dalios Grybauskaitės pareiškimai apie terminalo „laimėjimo istoriją“ ir jau pasiektą energetinę nepriklausomybę nuo Rusijos Federacijos neturi pagrindo, jie turi populizmo kvapą. Premjeras Saulius Skvernelis paneigia jos pareiškimus.

Per aštuonerius savo prezidentavimo metus Grybauskaitė sugebėjo įstumti Lietuvos–Rusijos santykius į aklavietę, atimdama iš šalies ekonomikos rusiškas investicijas ir krovinių eksporto srautus. Jos vadovavimo rezultatas — užsitęsęs ekonominis sąstingis, ryškiausias šalies istorijoje atotrūkis tarp turtingųjų ir skurstančiųjų, neregėtas ES mastais gyventojų emigravimas, keliantis realią grėsmę nacionaliniam saugumui, o taip pat visiška priklausomybė nuo ES finansinės adatos. Štai tokia ji, Lietuvos „laimėjimų istorija“.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 7 — id: `scraped:rubaltic_lt:e67ac566514263fc`

**Title:** Lietuvos valdžia kartoja Smetonos klaidas

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuva sparčiai perorientuoja savo ekonomiką karinėms reikmėms. Kitais metais išlaidos gynybai sudarys 2 proc. BVP. Ir provalstybinė žiniasklaida džiūgauja, jog tai toli gražu ne riba: karinis biudžetas gali būti išplėstas ir iki 3 proc. BVP.

Krašto apsaugos ministras Raimundas Karoblis jau anonsavo panašius planus. 2020 metais karinės išlaidos pasieks apie 2,35 proc. Tačiau ties šiais rodikliais Lietuvos valdžia neketina sustoti. Militaristinis Lietuvos elito siekis jau palietė visas visuomeninio gyvenimo sritis.Savo sprendimus motyvuodama rusų grėsme įsiveržti, šalies vadovybė pasiruošusi paaukoti viską: švietimą, mediciną, socialines išmokas ir t.t. Visos lėšos turi gulti ant karo altoriaus.

Pagrindinis valdžios argumentas, pateisinantis jos veiksmus, — 1940 metų įvykiai. Pasak valdančiųjų, tada Lietuva pasidavė Tarybų Sąjungai per keletą dienų visiškai nepasipriešinusi.

Nepaisant to, jog praktiškai visos karinės struktūros tada tapo pavaldžios tarybiniams kariškiams,  o dauguma karininkų su Lietuvos kariuomenės vadu generolu Stasiu Raštikiu priešakyje savo noru įsiliejo į Raudonosios armijos gretas, dabartinė Lietuvos vadovybė kultivuoja mitą, jog Lietuvos kariuomenė tiesiog neturėjo galimybės pasipriešinti, todėl ir buvo išvengta karinio susidūrimo. Tačiau tai visiškai prasilenkia su tiesa.

Melas vardan melo

Lietuvos politinis elitas dieną naktį kartoja: „1940 metų birželio 15-oji neturi pasikartoti“. Kitaip sakant, dabartinė Lietuva turi padaryti viską, kad neįvyktų naujo „įsiveržimo“ ir „okupacijos“. Už žodžių „padaryti viską“ slypi visapusiškas gynybinės sistemos tvirtinimas ir maksimalus kariškių skaičiaus didinimas. Pagal lietuviškųjų „viršūnėlių“ logiką, visa tai ne tik išgąsdins potencialų priešą — Rusiją, bet ir ateityje apsaugos ją nuo staigaus pralaimėjimo, ko Lietuvai nepavyko padaryti prieš 77 metus.

Paradoksas tame, jog Lietuvos valdžia samoningai meluoja savo žmonėms, nes tarpukario Lietuva ( 1918–1940 ) nestokojo kareivių ir karinės technikos.

Šalis gyveno pastovioje įtampoje dėl konflikto su Lenkija. Valdant Antanui Smetonai (1926–1940) Lietuva skyrė karinėms reikmėms didžiulius pinigus. Praktiškai visi mokesčių mokėtojai aptarnavo kariškius, policiją ir kitas saugos struktūras.

Kaip rašo istorikas Algimantas Kasparavičius, tarpukario Lietuva eikvojo gynybai virš 20 proc. valstybės lėšų. O jei kalbėti apie 1935–1936 metų situaciją, o tai buvo smetoniško autoritarizmo apogėjus, išlaidos karinėms reikmėms siekė 25–30 proc. viso valstybės biudžeto. Žvelgiant iš šių dienų pozicijų, tai visiškai neįtikėtina suma.

Ir vis dėlto tokia politika leido šio to pasiekti. Lietuvos kariuomenė buvo skaitlinga ir neblogai apmokyta. Šalis turėjo neblogas oro pajėgas ir savus lėktuvus ANBO, kuriuos konstravo ir statė Lietuvos specialistai.

Prieš įstojimą į TSRS Lietuva buvo pajėgi mobilizuoti apie 150–200 tūkstančių kariškių, kurie esant norui galėjo pasipriešinti „okupantui“, tačiau kažkodėl to nepadarė. Beje, valdžia atsisakė net mobilizacijos.

„Jeigu mes jau ėmėme lyginti šių dienų ir tarpukario Lietuvos karines pajėgas, tai Antano Smetonos laikais Lietuva buvo apginkluota iki dantų ir šių dienų kariuomenę lenkė visais aspektais“, — rašo istorikas.

Taigi teigti, jog „okupacija“ įvyko todėl, jog nebuvo kariuomenės, negalima. Tačiau dabartinė Lietuvos valdžia įkyriai meluoja savo piliečiams, vėl ragina ginkluotis ir, kaip prie Smetonos, atima iš šalies galimybę vystytis todėl, kad esą ekonomika privalo aptarnauti karines struktūras.

Nenorėjo gintis

Kitas Lietuvos istorikas Vytautas Jokubauskas tvirtina, kad Lietuvos valdžia, kaip ir žmonės, nepanoro gintis, nors ir galėjo tai padaryti. Jo žodžiais, Tarybų Sąjungai šalis pasidavė beveik savo noru.

„Tuo metu mes turėjome pakankamą kiekį ginklų, kad apginkluotume 5–6 pėstininkų divizijas, ir turėjome galimybę sutelkti apie 150 tūkstančių kariškių. Neabejotina, jog Lietuva turėjo nemažai rezervistų. Šie duomenys leidžia daryti išvadą, kad Lietuva vienam kariškiui turėjo tiek pat amunicijos, kaip ir Suomija karo su TSRS išvakarėse (1939–1940). Todėl negalima pateisinti mūsų kapituliaciją amunicijos stoka“, — konstatuoja mokslininkas.

Neišmoktos pamokos

Dabartiniai Lietuvos vadovai daro tas pačias klaidas, kaip ir anie, ir naiviai mano, kad didinamas karinis biudžetas ir valstybės militarizavimas apsaugos ją nuo „antrosios okupacijos“. Kaip matome, taip nėra.

Istorikų duomenys išsklaido mitą, kad šalis tada negalėjo gintis. Galėjo. Tik niekam tos gynybos nereikėjo.

Kodėl Smetonos statytiniai ir jis pats atsisakė priešintis – rimta tema diskusijoms. Daug kas laiko tai asmenine prezidento ir kariškių išdavyste, kiti pateikia labiau logišką versiją, kad tauta nebūtų gynusi korumpuotos sistemos, apvaginėjusios gyventojus.

Jis gi atėjo valdžion po valstybinio perversmo ir pastoviai jautė pavojų, kad ir pats panašiai gali jos netekti.

Lietuvos žurnalistas Algirdas Plukys savo laiku išleido publikaciją, kurioje citavo „miško brolio“ Justino Lelešiaus memuarus. Šis rašė:

„Mūsų vyriausybei buvo būdingas paniekinantis požiūris į socialinę padėtį, nes visą kapitalą buvo sukaupusi saujelė žmonių, o visi kiti tuo metu kentė skurdą, mūsų tėvynainiams teko ieškoti laimės už jūrų marių, ir tai tuo metu, kai danai, švedai, olandai, vokiečiai ir kiti Lietuvoje prisigrobė milijonus.

Mažai tarp mūsų buvo idealistų, galinčių aukoti save Tėvynės ir visuomenės labui, visi stengėsi iš bet kurio aruodo griebti auksą (materialines ir kitas gėrybes), linksmai leisti laiką... Visi valdininkai rėkė, kad per menki jų atlyginimai, o valstiečiai ir darbininkai tuo metu skurdo ir kaupė neapykantą.

Šiandien aš noriu paklausti: kur dabar tie, kurie, gerdami šampaną, rėkė, jog Tėvynės nelaimėje nepaliks, o priešo, jeigu jis išdrįs užpulti, mirtis lauks kiekvienoje troboje? Ir vėl jie Tėvynės gynimą paliko tamsiam kaimui, į kurį visada žvelgė su panieka. Šiandien mes savo gretose nematome ir karininkų, kurie puikavosi kavinėse ir gatvėse“.

Panašios nuomonės prisilaiko ir respublikinės Antrojo pasaulinio karo dalyvių, kovojusių antihitlerinės koalicijos gretose, organizacijos pirmininkas, Didžiojo Tėvynės karo veteranas Julius Deksnys. Jis pamena, kaip lietuvių šeimos, gelbėdamosi nuo skurdo ir nedarbo, masiškai bėgo į užsienį. Ana situacija labai primena dabartinę.

„Nedarbas ir nusivylimas. Šiandien valdžia seka tautai pasakas apie esą iki 1940 metų klestėjusią ekonomiką. Tikrovėje tai buvo visą šalį apėmęs skurdas, ir ateityje nesimatė jokių prošvaisčių“, — sako J.Deksnys.

Mokykitės istorijos

Visi šie pavyzdžiai ir ekskursai į praeitį sako, jog dabartinė Lietuvos valdžia nežino arba samoningai ignoruoja savo šalies istoriją. Militaristinis užtaisas, didžiulės išlaidos karinėms reikmėms nedavė teigiamų rezultatų tada, neduos ir šiandien.

Neverta užmiršti, kad tarpukario metais karinėms reikmėms buvo eikvojamas beveik trečdalis BVP. Ir tai neapsaugojo šalies nuo „užgrobimo“.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 8 — id: `scraped:rubaltic_lt:ae71074737be9dc9`

**Title:** Algirdas Paleckis: „Landsbergis — politikas su minuso ženklu”

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos Seimo pirmininkas pasiūlė suteikti idėjiniam konservatorių lyderiui Vytautui Landsbergiui šalies prezidento statusą. Premjeras pripažino, kad Landsbergis tikrai užsitarnavo bent jau prezidentinių privilegijų. Apie Landsbergių dinastijos fenomeną ir tą vaidmenį, kurį jo atstovai atlieka dabartinėje Lietuvos politikoje, analitinis portalas RuBaltic.Ru kalbasi su politologu Algirdu PALECKIU:

— Pone Palecki, idėja suteikti Vytautui Landsbergiui prezidento statusą ir privilegijas iššaukė prieštaringas nuomones. Kas čia ne taip?

— 1990 metais pagal Lietuvos TSR įstatymus buvo išrinkta Aukščiausioji Taryba. Faktiškai tai buvo tarybinis Lietuvos organas, o Vytautas Landsbergis — jo vadovas. Būtent Aukščiausioji Taryba 1990 metų kovo 11 dieną paskelbė nepriklausomybę. Prasidėjo pereinamasis laikotarpis. Todėl naujausia Lietuvos istoriografija nepajėgia atsakyti į klausimą, kas gi tada vadovavo Lietuvai. Buvo dvivaldystė. Maskvoje — Gorbačiovas, Lietuvoje — Aukščiausioji Taryba ir jos paskirta vyriausybė, kurios vadove tapo Kazimira Prunskienė — pirmoji naujosios Lietuvos premjerė.

Prezidento tada nebuvo — tuo metu galiojusi Lietuvos TSR Konstitucija tokios pareigybės nebuvo numačiusi. Štai ir ginčijamasi, kas gi buvo valstybės vadovas. Aš net pasakyčiau, kad ūkinius, o kartais ir politinius klausimus sprendė Prunskienė. Ji pasižymėjo kaip daug įtakingesnė, nei Landsbergis, politikė. Taip kad ginčytis šiuo klausimu galima iki užkimimo.

Jokių kalbų nebūtų, jei jis pasakytų, jog jam nereikia naujų regalijų. Tačiau jis gudriai tyli, paduodamas ženklą, kad mielai dar ko nors garbinančio sulauktų. Štai ir perrašinėjama istorija atbuline data. Prezidento tada nebuvo...

Vėlgi galima ilgai ginčytis, sakyti, pavyzdžiui, kad Aukščiausioji Taryba buvo viršesnė už vyriausybę, nes ji ją patvirtino savo balsais. Iš kitos pusės, reali valdžia buvo premjerės rankose. Šia prasme klausimas įsiremia į Landsbergio išdidumą ir jo aplinkos šokinėjimą aplink jį.

— Vytauto Landsbergio tėvas buvo ministras Laikinosios Lietuvos vyriausybės, suformuotos nacių okupacijos metu. Jo senelis buvo žinomas visuomenės veikėjas, lietuvių nacionalinio judėjimo caro laikais ideologas. Kaip susiklostė, kad Landsbergių dinastija taip tampriai įsipynė į Lietuvos valdžią ir visuomeninį gyvenimą?

— Tai svarbus momentas. Iš vienos pusės, be abejonės, Landsbergiai — inteligentų, visuomenės veikėjų dinastija. Iš kitos, kyla daug klausimų, į kuriuos iki šiol nėra atsakymų. Antai Vytauto Landsbergio tėvas Vytautas Landsbergis-Žemkalnis užėmė aukštas pareigas antitarybinėje vyriausybėje nacių okupacijos metu, po to atsidūrė Vakarų Europoje, iš kurios persikėlė į Australiją ir 1959 metais sėkmingai grįžo į Tarybų Lietuvą.

Jam buvo suteiktas Nusipelniusio Lietuvos TSR architekto vardas, jis gavo greta Kauno namą. Apie tai net Lietuvos TSR enciklopedijose parašyta.

Visa tai verčia manyti, jog Vytauto Landsbergio tėvas vykdė kažkokią užduotį. Kieno? Tiesioginių įrodymų nėra, vien tik spėlionės. Todėl ir dėl sūnaus karjeros kyla klausimai. Sąjūdis Lietuvoje kūrėsi visiškai palaikant Komunistų partijai ir Saugumo komitetui. Iš dalies tai vyko savaime, tačiau nurodinėjant ir leidžiant Tarybų valdžios organams.

— Ir todėl pasklido gandai, jog Landsbergius siejo ryšiai su VSK (KGB). Šie gandai iki šiol neišnyko.

— Tokie gandai tikrai egzistuoja. Tiesioginių įrodymų aš nemačiau. Tačiau pasikartosiu: Landsbergio-Žemkalnio biografijos žmogus 1959 metais grįžti į Tarybų Sąjungą be specialiųjų tarnybų sutikimo ir žinios negalėjo.

— „Dėdulės“ pravardė, kuri buvo suteikta agentui, taip pat iš ten atėjo?

— Ji ne pirmi metai pasirodo spaudos puslapiuose, tačiau nesant dokumentų sunku teigti šimtu procentų.

— Landsbergį kai kas vadina dabartinės Lietuvos tėvu, Lietuvos politikos patriarchu. Ar tikrai, objektyviai vertinant, jis atliko didelį vaidmenį kovoje už nepriklausomybės atkūrimą?

— Be abejonės, Vytautas Landsbergis – vienas iš dabartinės Lietuvos tėvų pradininkų. Aš dar pridurčiau, kad jis buvo pagrindinis naujosios Lietuvos ideologas ir, kaip nebūtų keista, juo lieka iki šiol. Tačiau svarbu nepaklysti terminuose.

Landsbergis iškilo kaip politikierius ir taktikas: jis realiai įėjo į istoriją, pelnė įvariausias privilegijas, gavo daugybę premijų, tame tarpe ir pinigais. Bet politikas jis menkas. Pastarųjų 25 metų rezultatai šokiruojantys: demografinė krizė, didžiulė emigracija, lietuviai tapo išnykstančia tauta, sugriauta pramonė ir t.t. Apklausų metu pagal populiarumą Landsbergis visada atsiduria paskutinėje arba priešpaskutinėje vietoje.

Jam pavyko 80-ųjų pabaigoje tapti tautos vedliu, tačiau jau 1990-ųjų vasarą jo reitingas ėmė sparčiai kristi. Nuo tada jam tik beliko didinti įtampą, ką jis sėkmingai daro iki šiol. Daug kas jo nemėgsta ir nemėgsta teisėtai: pragyvenimo lygis krito.

Landsbergis arogantiškas, ir žmonės tai jaučia. Ir svarbiausia bei liūdniausia – jis nepripažįsta pozityvios darbotvarkės.

Landsbergis savo ilgaamžiškumu aplenkė Algirdą Brazauską ir daugelį kitų, ir, manau, likimas padiktavo, kad jis pamatytų savo kurso griūtį. Net nepriklausomybės, dėl kurios jis kovojo, šiandien nėra: viską sprendžia Vašingtonas ir Briuselis.

— Tačiau lietuviškoji spauda, kaip taisyklė, pagarbiai mini Landsbergį.

— Atotrūkis tarp to, ką galvoja žmonės ir rašo spauda, Lietuvoje primena situaciją Amerikoje su Trampu. Elitui visada reikalinga konkreti, tautą vienijanti asmenybė. Lietuvos elitui Landsbergis šiam vaidmeniui tinka. Jis patriarchas ir statusu, ir amžiumi, be to, nenuskriaustas talentais. Jis kalba vaizdžiai, moka išreikšti mintis.

Elitui jis didvyris. Tautos daugumai ir elitas tokio vardo nevertas. Juolab — Landsbergis. Jis mirguliuoja žiniasklaidoje. Tačiau jei peržvelgti komentarus po jo straipsniais arba straipsnius apie jį, — Landsbergis ten nekaip atrodo.

— Ar jo įvaizdis padeda konservatoriams?

— Sutelkiant branduolinį lektoratą — taip. Bet ne daugiau. Jeigu konservatoriai nori išplėsti lektorato bazę (o jie nori), tai Landsbergio įvaizdis ne padeda, o, priešingai, atstumia.

Bet tuo metu branduolinis lektoratas pastoviai mobilizuojasi ir drausmingai ateina balsuoti. Taigi svarbu pasinaudoti seneliu Landsbergiu. Tačiau virš 20 proc. balsų konservatoriai pastaraisiais metais negavo ir, manau, artimiausiais metais negaus.

— Gabrielis Landsbergis vadovauja Tėvynės sąjungai — krikščionims demokratams. Kokias Jūs matote jo politines perspektyvas? Kiek panašus jis į savo senelį?

— Jis vis dėlto neturi nei patirties, nei talantų, kuo pasižymėjo senelis. Senelis — šachmatininkas, jis moka numatyti ėjimus, ypač intrigų atžvilgiu. Anūkas dar jaunas, nesukaupęs patirties. Iš jo kalbos galima spręsti, kad jis neturi literatūrinio talento, kas, pripažinkime, charakterizuoja senelį Landsbergį. Šis liežuvį puikiai valdo, jis net poezija užsiiminėja, jau nekalbant apie publicistiką. Iš kitos pusės, anūkas dinamiškas, sparčiai mokosi. Ir mokosi iš paties senelio, nors matosi, jog jis neturi senelio polinkio intriguoti.

— Spaudoje pasitaiko nuomonė, kad senelis Landsbergis iki šiol valdo Lietuvą per neformalius įtakos svertus. Ar taip yra?

— Iš dalies sutinku. Senelis Landsbergis turi puikią atmintį pavardėms ir informacijai.

Vytautas Landsbergis ir Dalia Grybauskaite

Jis disponuoja įvairia informacija, o, kaip žinia, kas disponuoja informacija, tas ir valdo. Landsbergis dabartinę Lietuvos politiką įtakoja savo patarimais, pastabomis. Net buvęs prezidentas Valdas Adamkus savo memuaruose neseniai parašė, kad Landsbergis, net ir neužimdamas politiškai reikšmingų postų, ateidavo pas jį ir palikdavo raštelius, nurodančius, kaip ir ką daryti, ką kur paskirti. Anglų kalboje yra toks išsireiškimas — political animal („politinis gyvulys“, „gamtos sukurtas politikas“ — RuBaltic.Ru pastaba).

Politika — jo gyvenimo būdas. Troškimas valdžios, ėjimas valdžion ir jos realizavimas — tai jo esmė. Jis sukaupė didžiulę patirtį, kadrinį potencialą, į svarbiausius postus pasodino savus žmones, ir tai pasireiškia. Įmėgį valdyti jis realizuoja gana sėkmingai, nepaisant garbaus amžiaus.

— Dėl nepriklausomybės kovojo daug žmonių. Buvo Atkuriamasis Seimas, daug signatarų. Kodėl Sąjūdis ir nepriklausomybės atkūrimas dabar dažniausiai asocijuojasi būtent su Landsbergiu?

— Čia pasireiškia tam tikras asmenybės kultas, kuris net ir šiandien būdingas mūsų sistemai. Iki karo egzistavo diktatoriaus Antano Smetonos kultas, ir kažkas panašaus išliko mentalitete. Tautos noras atsirinkti figūrą ir ją dievinti. Arba, tiksliau, ne tautos — tauta seniai nusivylė Landsbergiu, — o elito.

Istorija dabar pateikiama taip, kad buvo žmogus, kuris „pažadino“ tautą ir atnešė jai nepriklausomybę. Jis energingas, tiesiog pasionarijus. Istoriją kuria pasionarijai. Jie ir suteikė šiam žmogui erdvę. Kitos versijos atmetamos. Žinoma, ir ta, kad tada ne tik Landsbergis veikė. Juk be jo buvo ir kiti žmonės, kurie, ne kaip jis, tarybiniais laikais buvo disidentai. Tačiau mūsų žiniasklaida apsiginklavo ir gina kitą versiją — ir čia, beje, vėl pasireiškia Landsbergio valdžios įtaka. Taip kad yra kaip yra.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 9 — id: `scraped:rubaltic_lt:9258cbc10926141c`

**Title:** Putinas atims iš Pabaltijo baltarusišką tranzitą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Atsisakęs per Pabaltijį vežti savo krovinius Kremlius tariasi su Baltarusijos respublika dėl jos krovinių nukreipimo kitais keliais. Šį kursą numatė pats Rusijos prezidentas Putinas, iškėlęs uždavinį susitarti su Minsku, kad baltarusių naftos produktai, pagaminti iš rusų naftos, būtų transportuojami per Rusijos uostus ir Rusijos geležinkeliais. Rusijos strategija Pabaltijo atžvilgiu tapo dar ryškesnė: nepalikti priešiškai nusiteikusioms Pabaltijo šalims jokios galimybės vystytis ekonomiškai bendradarbiaujant ne tik su Rusija, bet ir su sąjungine jai Baltarusija.

Vizito į Kaliningrado sritį metu Rusijos prezidentas Vladimiras Putinas dalyvavo pasitarime sprendžiant Rusijos Šiaurės Vakarų transporto infrastruktūros vystymosi klausimą. Pasitarimo metu AAB „Rusijos geležinkeliai“ vadovas Olegas Beloziorovas pranešė prezidentui, jog baltarusių naftos perdirbimo gamyklos atsisako Rusijos geležinkelių paslaugų, pasirinkdamos Pabaltijo transporto infrastruktūras.

„Naftos produktų transportavimui mes taikome baltarusiams 50 proc. nuolaidą, tačiau jų gamyklos kolkas nepasinaudoja nei Ust-Lugos, nei Sankt-Peterburgo paslaugomis, jos vis dar naudojasi Pabaltijo respublikų infrastruktūra. Mes diskutuojam, o jie teigia, jog yra šiomis temomis sudaryti ilgalaikiai kontraktai, tačiau mes stengiamės vesti su jais dialogą“, — situaciją paaiškino Beloziorovas.

Atsakydamas į tai Vladimiras Putinas pareiškė, jog būtina siekti, kad baltarusių gamyklos, gaminančios produktus iš Rusijos tiekiamos naftos, juos transportuotų Rusijos teritorija.

„Visa tai būtina aptarti plačiame formate. Juk Baltarusijos gamyklos perdirba mūsų naftą, kitos ten nėra ir vargu ar atsiras, todėl reikia siekti, kad mūsų naftos gavėjai naudotųsi ir mūsų transporto infrastruktūra“, — pasakė Putinas.

Tokiu būdu sprendimas baltarusių tranzito klausimu priimtas ir paskelbtas valstybės vadovo lygyje.

Naftos tranzitas ne vienintelis, tačiau ryškiausias pavyzdys. Baltarusijos naftos perdirbimo industrija egzistuoja pagrindinai dėka Sąjunginės valstybės: baltarusių gamyklos gauna Rusijos naftą lengvatinėmis kainomis, perdirba ir parduoda Vakarams pasaulinėmis — ir gauto pelno sąskaita vystosi šaka. Ir tai todėl, jog egzistuoja Rusijos ir Baltarusijos sąjunga.

Todėl logiška siekti, kad Baltarusijoje pagaminti naftos produktai keliautų į Vakarus per Rusiją ir kad iš to tranzito pelnytų Rusijos uostai ir geležinkeliai.

Per Klaipėdą ir Ventspilį neturi būti vežama ne tik rusų nafta, bet ir iš jos pagaminti baltarusių produktai. Tai valstybinė nuostata, kurią dabar pagarsino pats Putinas.

Prieš metus „Transneft“ vadovas pranešė Rusijos prezidentui apie planingą rusų naftos tranzito perorientavimą iš Pabaltijo uostų į Leningrado sritį. Ir tada specialusis valstybės vadovo atstovas ekologijos ir transporto klausimais Sergejus Ivanovas pareikalavo, kad stambiausi rusų vežėjai nuo 2020 metų visiškai atsisakytų Pabaltijo uostų paslaugų ir savo krovinius transportuotų pasinaudodami tik sava infrastruktūra.

Tada visiškai paaiškėjo Rusijos strategija Pabaltijo šalių atžvilgiu: netrukdyti Pabaltijui merdėti, nesikišti į jo merdėjimo procesą ir net nebandyti jo sulėtinti, paduodant Lietuvai, Latvijai ir Estijai kriukį, padedantį joms patekti į 145 milijonų Rusijos rinką.

Pabaltijis — tai visiškai antirusiški politiniai režimai, springstantys rusofobija ir eksportuojantys tą rusofobiją pramoniniais mastais vakarietiškiems sąjungininkams. Antirusiška politika — šių šalių specializacija tarptautiniuose santykiuose, jų firminis patiekalas.

O strategija — pagreitinti demografinę katastrofą ir sisteminės krizės atsiradimą tose šalyse, kurios ėmė reikšti atvirą priešiškumą nuo pat savo atsiradimo 1991 metais.

Kaliningrade Vladimiras Putinas dar kartą patvirtino Rusijos valstybinę politiką, įpareigojęs pradėti statyti keleivinį terminalą Pioniersko uoste ir pabrėždamas, kad Rusijos kroviniai neturi būti perkraunami užsienio uostuose, kai yra galimybė naudotis sava infrastruktūra.

Bet ten ši politika buvo patikslinta ir papildyta. Lietuva, Latvija ir Estija neturi gauti nė cento ne tik iš Rusijos, bet ir iš Rusijos su Baltarusija sąjungos.

Nusimatantis naftos tranzito perorientavimas — pirmasis bandymas, o po to bus kiti ir vis ta pačia kryptimi. Anksčiau ar vėliau Klaipėda ir kiti Pabaltijo uostai visiškai liks be Baltarusijos užsakovų. Tai objektyvus Pabaltijo išdvejinimo procesas, kai viena regiono dalis vystosi griežtai Europos Sąjungos, kita — Euroazijos ekonominės sąjungos rėmuose ir šių integracijos procesų sąveika ritasi link nulio.

Ir būtent Lietuva, Latvija ir Estija  pavertė šį procesą negrįžtamu. Jų vadovai per 25 „antrosios nepriklausomybės“ metus iš kailio nėrėsi naikindami savo šalių potencialą — civilizuotą „tiltą“ tarp Rusijos ir Vakarų. Jie sutelkė prie Rusijos sienų NATO kareivius, atgabeno į savo teritoriją tankus ir bombonešius, o dabar reikalauja dar ir priešraketinės gynybos sistemos. Klykė, kad būtų įvestos prieš Rusiją sankcijos, bandė organizuoti „maidanus“ Baltarusijoje, rėmė bet kokias antirusiškas iniciatyvas, paskelbė karą Baltarusijos AE.

Ir todėl šiandien santykiai su Pabaltijo šalimis neturi jokios vertybės nei Rusijai, nei Baltarusijai. Jeigu Maskva nors kiek būtų suinteresuota bendradabiauti su Pabaltijo šalimis, ji būtinai rastų galimybę atskirti nuo galingos rusų tranzito upės, tekančios per Primorską ir Ust-Lugą, nedidelius upeliūkščius, kurie, kaip ir anksčiau, maitintų Ventspilį, Rygą, Taliną.

Pabaltijis gali džiaugtis savo unikalia geografine padėtimi, tačiau jo vadovybė niekada to nevertino. Be reikalo. Geografinė padėtis jau neišgelbės. Esant bendrai politinei trumparegystei neišgelbės jokia geografija.

Rusija įveikė Pabaltijo uostų monopoliją — pasistatė savus. Dabar ji siūlo Baltarusijai 50 proc. nuolaidą jos krovinių tranzitui, ir vėl Sąjunginės valstybės kūrimas ir euroazijietiška integracija pasireiškė kaip galingesnė jėga, nei Pabaltijo geografinė padėtis.

O ką, išskyrus patogią logistiką, gali Baltarusijai pasiūlyti Pabaltijis?

Nustoti loti link Baltarusijos AE? Užtarimą Briuselyje? Atsisakyti remti radikalią opoziciją? O gal, priešingai, „demokratijos eksportą“?

O ką savo strateginei sąjungininkei gali pasiūlyti Rusija? Kaip parodė pastarieji dešimtmečiai, daugiau negu NATO ir Europos Sąjunga.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 10 — id: `scraped:rubaltic_lt:ac8311e4f6ce8b43`

**Title:** Buvęs prezidentas Paksas: Lietuva turi statyti bendradarbiavimo su kaimynais tiltus

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Analitinis portalas RuBaltic.Ru tęsia interviu ciklą su Pabaltijo politikos veteranais. Jie, stovėję prie Lietuvos, Latvijos ir Estijos potarybinio kelio ištakų, bando susumuoti šių respublikų ketvirčio amžiaus tranzito rezultatus: kokias valstybes svajojo sukurti tėvai pradininkai ir kokio rezultato pavyko pasiekti. Šio ciklo pokalbio dalyvis Rolandas Paksas — Europos parlamento narys, buvęs Lietuvos respublikos prezidentas.

Prezidentu Paksui teko būti tik metus. 2004 metais Seimas inicijavo jo apkaltą. Tačiau šiandien Rolandas Paksas tapo oficialiu lyderiu tų jėgų, kurios nepritaria dabartinės valdžios kursui. Buvęs prezidentas pasisako gana aštriai, jis nebijo pagarsinti nepatogios informacijos, nesivaržydamas viską vardina tikrais vardais. Tačiau jis nesako nieko ypatingo, tik pabrėžia, kad šalyje vyrauja betvarkė. Lietuva sparčiai sensta, Lietuva lėtai miršta, Lietuvą masiškai palieka geriausi jos žmonės.

Ar galima pakeisti situaciją, išsaugoti tautą ir atkurti šalį? Apie tai analitinis portalas RuBaltic.Ru kalbasi su Europos parlamento nariu, buvusiu Lietuvos prezidentu Rolandu PAKSU.

— Pone Paksai, potarybinė Lietuva turėjo keletą vystymosi kelių, tame tarpe galėjo tapti savotišku tiltu tarp Vakarų ir Rytų. Lietuva yra pasirinkusi vieną kryptį -  proeuropietišką kelią,  atsisakė bendradarbiauti su savo Rytų kaimynu ir pradėjo jo sulaikymo politiką. Ar tai buvo labiausiai ekonomiškai ir politiškai pelningas kelias?

— Lietuvos nepriklausomybė buvo atkurta žlugus komunistiniam režimui Sovietų Sąjungoje. Kitaip tariant, praėjusio amžiaus pabaigoje lietuvių tauta kartu su kitomis Baltijos tautomis taikiai išėjo iš okupacijos ir įgavo galimybę tęsti savo valstybingumo tradiciją, kuri prievarta buvo nutraukta praėjusio amžiaus penktajame dešimtmetyje.

Vakarų kultūra ir krikščioniškoji tradicija visada buvo ta kryptis, kuri galėjo užtikrinti lietuvių tautos gyvybingumą, jos tęstinumą, nacionalinį tapatumą, išsaugoti moralines vertybes.

Vien to aiškiai nepakako: reikėjo išvesti visuomenę iš nevilties ir melo tikrovės, kurioje ji buvo priversta gyventi sovietmečiu, bei sukurti naujus demokratijos, visuomenės pilietiškumo ir politinio sąmoningumo ugdymo instrumentus, kad toji tautos laisvė įgautų naujos tikrovės pavidalus.

Komunistinės santvarkos išvarginti žmonės tam nebuvo pasiruošę.

Kita vertus, norėčiau pabrėžti, jog Europos Sąjunga, kurioje Lietuva siekė savo narystės praėjusiame dešimtmetyje,  taip pat dabar yra gerokai pasikeitusi pamatinių vertybių atžvilgiu ir išgyvena ne pačius geriausius savo laikus.

Visada laikiausi nuostatos, jog Lietuva turi tiesti bendradarbiavimo tiltus su savo kaimyninėmis šalimis ir būti jų patikima partnerė. Kita vertus, gera kaimynystė nėra tik vienos šalies rūpestis.

Turime kurti ne naujus grėsmių židinius, o privalome stengtis padaryti šį pasaulį saugesnį ir taikingesnį.

— Lietuva pirmauja Europos Sąjungoje alkoholio kiekio suvartojimu, savižudybių skaičiumi ir emigracijos lygiu. Vienas mažiausių atlyginimų ES užfiksuotas Lietuvoje. Kaip  atsitiko, kad gana klestinti valstybė nesugebėjo realizuoti savo potencialo?

— Nenorėčiau šiandien žongliruoti statistika, kuri daugeliu aspektų būtų nepalanki arba palanki. Nežiūrint to, lyginant su kitomis postsovietinės erdvės šalimis mūsų pažangos rodikliai yra neabejotinai geri. Tačiau ir dėl objektyvių, ir subjektyvių priežasčių dabartinė mūsų ekonominė bei socialinė raida vis dėlto neatitinka visuomenės lūkesčių.

Lietuva buvo gana klestinti Europos valstybė prieškariu, tačiau penkiasdešimt okupacijos metų paliko labai gilius randus, kuriuos užgydyti nėra lengva. Europinės integracijos procesai taip pat neatitinka daugumos žmonių interesų. Todėl galima suprasti, jog prastą visuomenės dvasinę būklę iš dalies sąlygoja įvairios socialinės negerovės, kurios skatina žalingus įpročius. Didžiausią intelektualų ir visuomenininkų, bet ne valdžios institucijų susirūpinimą kelia migracijos mastai. Manau, kad tai vienas didžiausių dvidešimt pirmojo amžiaus iššūkių, kuriam įveikti reikalingos ne tik nacionalinių vyriausybių pastangos, bet ir tarptautinės bendruomenės parama.

— Daugelis ekonominių ir socialinių rodiklių Lietuvoje vis prastėja. Kaip galvojate, ar Lietuva jau pasiekė "tašką, iš kurio nebegrįžtama", ar dar turi galimybę "pakilti"?

— Europos Sąjungoje Lietuvos ekonomika šiandien dar atsilieka, nors pagal BVP augimą skaičiuojant vienam gyventojui esame tarp pirmaujančių valstybių. Tačiau augimo tempai ir atlyginimų vidurkiai mūsų netenkina. To aiškiai nepakanka. Socialinė atskirtis ir pajamų nelygybė yra pernelyg didelė, kad galėtume kalbėti apie darnią plėtrą. Ką daryti? Visų pirma būtina pertvarkyti nacionalinę mokesčių sistemą, radikaliai sumažinti darbo jėgos apmokestinimą, sudaryti palankiausias sąlygas visame regione plėtotis verslui, užtikrinti saugias kapitalo investicijas bei sukurti bent pusę milijono naujų  darbo vietų. Manau, kad žemės ūkis ir aukščiausios kokybės maisto produktų gamyba yra tik viena iš sričių, kurioje Lietuva gali „pakilti“ pirmiausiai. Tam reikalinga nauja žemės reforma. Aukštosios technologijos, turizmo paslaugos ir didelę pridėtinę vertę kurianti pramonė yra tos sritys, kurias valstybė turėtų skatinti.

— Nuo 1991 metų šalis neteko apie 800 000 žmonių, yra prognozių, kad 2050 metais lietuviai kaip tauta išnyks, o, pavyzdžiui, socialinių mokslų daktarė Vlada Stankūnienė tvirtina, kad Lietuvą palaipsniui apgyvendins azijiečiai. Kokia tokios prognozės tikimybė? Ar yra būdų emigracijos proceso sustabdymui ir emigrantų grąžinimui?

— Lietuvių tauta neišnyks kol bus gyvas bent vienas lietuvis.

Pirmiausiai turėtume sudaryti sąlygas kurti savo ateitį tėvynėje čia gyvenančioms bendruomenėms, nepriklausomai nuo jų tautybės, pažiūrų ir įsitikinimų. Ypatingai turime remti  vaikus auginančias šeimas, sudaryti palankiausias sąlygas ugdyti jaunimo kūrybiškumą, kurti socialiai saugią senatvę ir švarią patikimą aplinką. Esu prieš Briuselio pabėgėlių integracijos politiką ir nenorėčiau, kad Europos tautų kultūrinei tapatybei kiltų grėsmė ištirpti kitų kultūrų maišatyje. Lietuvoje turi būti visapusiškai susirūpinta demografija: remiama „trijų vaikų“ politika ir sudarytos palankiausios sąlygos grįžtantiems emigrantams vėl naujai įsikurti.

— Kokie, Jūsų nuomone, yra pagrindiniai pasiekimai nepriklausomoje Lietuvoje, kuriais galima didžiuotis?

— Šiandien Lietuva gali didžiuotis savo žmonių kūrybiškumu ir pasiekimais meno, mokslo bei verslo pasaulyje. Farmacija, biotechnologijos, pasiekimai telekomunikacijų srityje  stulbina: sparčiausias interneto ryšys, informacinės sistemos ir skaitmeninės technologijos praktiškai veikia daugelyje sričių visoje šalyje.

Lietuvos gydytojai sėkmingai dirba Norvegijoje, Didžiojoje Britanijoje ar Jungtinėse Amerikos Valstijose, ir pacientų nusiskundimų iš ten neteko išgirsti (juokauju, žinoma).

— Ar yra dalykų, dėl kurių turėtų būti gėda nepriklausomai Lietuvai ir valdantiesiems?

— Manau, gėda turėtų būti tiems, kurie šiandien manipuliuoja mūsų tėvų ir senelių per krizę sumažintomis pensijomis, kokiu nors būdu yra prisidėję prie nacionalinės valiutos lito sunaikinimo ir valstybės turto išparceliavimo.

Turėtų būti neramu politinius užsakymus vykdančiai teisėsaugai, kuri tik deklaratyviai yra nepriklausoma. Sveiko proto ribas baigia peržengti propagandinės žiniasklaidos balsai, kurie „atidirbinėja“ valdžiai.

— Straipsnyje " Iš baimės nukentėti žmonės nebeišdrįsta pasakyti to, kas visiems yra žinoma " Jūs kalbate apie būtinybę priešintis nūdienos pasaulio įtakai: atsilaikyti nuo šiandien mums brukamo „pliuralizmo“ ir visokiausios santykių „lygybės“. Ką Jūs turėjote omenyje?

— Pirmiausiai turiu omenyje unikalaus mūsų tautos dvasinio paveldo puoselėjimą nūdienos kultūros kontekste. Tai nėra paprasta pasaulyje, kuriame progresuoja materializmas, daiktų, vartojimo, pinigų kultas, vyrauja sėkmės, begalinio pasitikėjimo savimi ir egoizmo „normos“. Lietuvių tauta turi savus istorinius raidos ypatumus, katalikišką tikėjimą ir tas moralinių vertybių gelmes, kurios niekaip negali „įsipiešti“ materializmo apraiškose ir naujausiose reliatyvizmo ideologijose. Žmogus nėra socialinių eksperimentų objektas, ką dažnai pamiršta neoliberalizmo kaukėmis prisidengę vakarykščiai marksistai, teigę, jog „religija yra opiumas liaudžiai“.

Todėl šviesuomenei yra iškilęs labai rimtas uždavinys – iš naujo atrasti svarbiausias mūsų tautos  vertybes, susiformavusias per šimtmečius mūsų katalikiškos istorijos, kurios padėtų apsisaugoti nuo brukamo svetimo kultūrinio šlamšto ir gyvenimo būdo be jokių moralinių dimensijų.

— Jūs kuriate naują Nacionalinį Sąjūdį, nes manote, kad Landsbergio Sąjūdis nesusidorojo su užduotimi?

— Lietuvos valstybingumo raidos ir tautos praradimo grėsmė tebėra esminis klausimas, į kurį neatsakę šiandien prarasime bet kokias galimybes sugrįžti prie tikros valstybės, kurios taip ir nesukūrėme, buvę išduoti naujosios (senosios) nomenklatūros ir įvairiausių jos šiuolaikinių atmainų.

Kaip nebūtų keista, negaliu nepastebėti žvelgdamas į netolimą praeitį, jog kažkam užtenka akiplėšiškumo savintis tai, kas pagrįstai priklauso visai lietuvių tautai.

— Kuo Naujasis Sąjūdis skiriasi nuo kitų politinių organizacijų ir partijų? Kokie jo tikslai?

— Pagrindinis Naujojo Sąjūdžio tikslas – laisva tauta ir klestinti valstybė. Tautos atkūrimo sąjūdis -respublika piliečiams bus vienijantis nacionalinis pakilimas kurti Lietuvą – tikrai nepriklausomą, demokratiniais pagrindais sutvarkytą, socialiai jautrią ir solidarią, teisingumu bei žmogiškumu grindžiamą valstybę. Tikiu, jog mes tai padarysime. Dievas mums padės.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 11 — id: `scraped:rubaltic_lt:39e1906bba3c015b`

**Title:** Putinas ir Grybauskaitė tolimi kaip „taip“ ir „ne“

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Žinomas Lietuvos žurnalistas Vytas Tomkus parašė, kad Rusijos ir Lietuvos prezidentai Putinas ir Grybauskaitė panašūs kaip du vandens lašai. Tačiau akivaizdu, jog negalima lyginti tai, kas visiškai nelygintina. Rusijos ir Lietuvos prezidentai skiriasi vienas nuo kito net ne visiškai skirtingais mastais, o savo veiklos prasme. Putinas tarptautinėje arenoje gina Rusijos suverenitetą ir nepriklausomybę nuo pasaulinio hegemono, Amerikos. Grybauskaitei Lietuva — instrumentas tenkinant savo karjeros ambicijas ir padedant amerikiečiams įtvirtinti geopolitinius interesus.

„Kodėl man patinka Putinas? Todėl kad, mano manymu, Rusijos prezidentas Vladimiras Putinas labai panašus į mano numylėtąją prezidentę Dalią Grybauskaitę. Ir visiškai ne todėl, kad abu savo politinę karjerą kadaise pradėjo Leningrade ir abu meistrai kovinėse rungtyse, net dėvi vienos spalvos, juodus, diržus  (jis — dziudoistas, ji — karatistė), — rašo Respublikos media grupės vadovas ir vienas iš informacijos agentūros ELTA vadovų Vytas Tomkus. — Ir Vladimiras Putinas, ir Dalia Grybauskaitė pasireiškė kaip vienvaldžiai šalies vadovai, tiksliau valdovai, kurių reitingas kyla blogėjant  žmonių pragyvenimo lygiui“.

Vyto Tomkaus straipsnis šiuolaikinės Lietuvos mastais labai drąsus. Net įžūlus. Net pavadinimu: „O man patinka Putinas“. Ir palyginimu: jis — „žmonijos priešas“, ji — Jos Didenybė. Ir ypač užuomina apie ponios Dalios Polikarpovnos karjeros pradžią legendiniame Leningrado mieste.

Publicistinio paaštrinimo prasmė aiški. Sulygindamas Grybauskaitę su Putinu ir imituodamas gėrėjimąsį juo, autorius bando pasakyti, jog ponia prezidentė naudoja neleistinus autoritarinio valdymo metodus. Lyg ir giria, tačiau iš tiesų kritikuoja savo valstybės vadovę. Lietuvos patriotus varo į logikos pinkles: jei tau, patriote, patinka Grybauskaitė, tai turi patikti ir Putinas. Juk jų veiklos stilius ir metodai vienodi.

Tačiau paleista strėlė lekia pro šalį. Nesiseka supanašinti Putino su Grybauskaite. Ir esmė ne tame, kad bandoma lyginti tai, kas visiškai nelygintina: vadovus mažytės rytų europietiškos šalies ir didžiulės branduolinės, apie kurią net amerikiečių elitas kalba, kad ji įtakojo JAV prezidento rinkimus. Ir ne tame, kad pagal stilistiką tarp Putino ir Grybauskaitės ne taip daug bendro: Rusijos prezidentas, įteikdamas ambasadoriams įgaliojamuosius raštus, niekada nesisvaidė įžeidinėjimais ir nesidomėjo, ar nepaspringo jie gerdami pieną.

Svarbiausia — Putino ir Grybauskaitės veiklos prasmė dirbant šalies vadovais.

Ir ieškoti tarp jų panašumo bruožų, kai tikslai visiškai priešingi, — užsiėmimas beprasmiškas. Vytas Tomkus rašo: „Gerai, kad ir Putinas, ir Grybauskaitė nekreipia dėmesio į jokius autoritetus. Volodia Miuncheno konferencijoje pasiuntė Obamą velniop, o mūsų Dalytė net atsisakė sėdėti su Obama prie vieno stalo su vaišėmis, kai šis, keliaudamas Rytų Europa, surengė Pabaltijo šalių prezidentams vakarienę“. Autorius lygina tai, kas nelygintina.

Patikslinsime: Vladimiras Putinas pasakė savo garsiąją Miuncheno kalbą 2007 metais, kai Barakas Obama buvo Ilinois valstijos senatorius ir apie JAV prezidento postą galėjo tik svajoti. Putino kalba Miunchene nebuvo nukreipta prieš Baraką Obamą ar prieš bet kurį kitą JAV prezidentą. Tai buvo vienpoliško pasaulio tvarkymo kritika.

„Šiuolaikiškam pasauliui vienpoliškas modelis ne tik nepriimtinas, bet ir išvis neįmanomas“, — sakė Rusijos prezidentas. Visa vienos valstybės, JAV, teisės sistema peržengė nacionalines sienas ir peršama kitoms valstybėms. Tarptautinė teisė pakeista stipresnio teise. Savo politika Vakarai ne įtakoja progresą globaliais mastais, o tik konservuoja „trečiųjų pasaulio šalių“ ekonominį atsilikimą. Pagaliau, Rusija — šalis, turinti daugiau nei tūkstantmečio istoriją, ji visada naudojosi nepriklausomos užsienio politikos privilegija ir neketina tos privilegijos  atsisakyti.

Miuncheno kalba tapo Rusijos suvereniteto deklaravimu ir jos vadovybės atsisakymu įsilieti į globalinę politinę hierarchiją, vadovaujant Amerikai. Už šį pasirinkimą savarankiškumo naudai Rusija dabar skelbiama pasaulio blogiu ir globalia grėsme su visur apsireiškiančiais „žaliais žmogeliukais“ ir „rusų chakeriais“.

Argi galima su visu tuo lyginti banalią Dalios Grybauskaitės moterišką isteriką dėl to, kad jos viltys ir svajonės nesulaukė tinkamo dėmesio? Dėl ko prezidentė metė Barakui Obamai akibrokštą, atsisakydama dalyvauti vakarienėje, kurią JAV prezidentas organizavo Centrinės ir Rytų Europos lyderiams? Dėl to, kad JAV tada pasirašė su Rusija naują sutartį dėl strateginės puolamosios ginkluotės, pamiršdamos savo be galo ištikimą sąjungininkę Lietuvą.

O juk Lietuvai Jungtinės Amerikos Valstijos — pagrindinės partnerės tarptautinėje arenoje, o sąjungininkės pareiga — dalykas šventas, vykdydama šią pareigą Lietuva siuntė savo kareivius į Iraką ir Afganistaną, aukojo savo nacionalinius interesus, nes svarbiausia — visom keturiom remti amerikiečių „Rusijos sulaikymo“ strategiją. O JAV prezidentas už tokią šunišką ištikimybę net dėmesio neskiria. Negi tokiu atveju neįsižeis ir nepasipūs?

Ir todėl Putinas, nepriklausant nuo to, kam jis patinka arba ne, žinomiausias ir labiausiai aptarinėjamas pasaulyje žmogus, o apie Grybauskaitę už jos regiono ribų žino tik vis tos pačios Rusijos ir artimiausių šalių specialistai. Ir tai ne todėl, kad Rusija didžiausia šalis pasaulyje, o Lietuvą visi painioja su Latvija ir nesugeba jos žemėlapyje parodyti. Singapūras mažesnis už Lietuvą, tačiau jo buvusį lyderį Li Kuan Ju daug kas žino kaip vieną iš įtakingiausių ХХ amžiaus valstybės veikėjų. Grybauskaitės niekas neprisimins, todėl kad tokių, kaip ji, amerikiečių tarnų pasaulyje šimtai tūkstančių.

Putinui Rusija — tikslas, o Lietuva Grybauskaitei — priemonė. Poniai Daliai nerūpi savo šalies interesai — ji naudojasi Lietuva kaip įrankiu, padedančiu vykdyti iškeltas politines užduotis ir, gražiai atsiskaičius vakarietiškiems šeimininkams, jog dirbo efektyviai ir naudingai, paprašyti paaukštinimo.

Putinui nereikia svajoti apie paaukštinimą — jis ir taip Rusijos prezidentas. O Grybauskaitei prezidentavimas — tremtis į kaimą. Ji svajoja tapti Europos komisijos vadove, Jungtinių Tautų generaline sekretore arba Europos Sąjungos tarybos pirmininke. Svarbiausia, nors baidyklės pavidalu ištrūkti iš savo provincijos prie jūros, apsireikšti transnacionalinės biurokratijos gretose ir dirbti kur nors Njujorke arba Briuselyje.

Toks fundamentalus Putino ir Grybauskaitės tikslų nesutapimas daro jų palyginimą visiškai absurdišku. Argi galima lyginti dievo dovaną su kiaušiniene? Nepasitenkinimą Lietuvos prezidentės veikla galima išreikšti ne ekscentriškai, o taip, kad dėmesio centre atsidurtų konkrečios pretenzijos Lietuvos valstybės vadovei. Originalios poleminės priemonės, kuriomis autorius stengiasi atkreipti dėmesį į jo išsakytą kritiką, šiuo atveju visiškai nepasiteisino.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 12 — id: `scraped:rubaltic_lt:fd734346d52750da`

**Title:** Rolandas Paulauskas: Lietuvos politika primena plekšnę — abi jos akys žiūri į vieną pusę

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Analitinis portalas RuBaltic.Ru pradeda interviu ciklą su Pabaltijo politikos veteranais. Žmonės, stovėję Lietuvos, Latvijos ir Estijos potarybinio kelio ištakose, apžvelgia šių respublikų ketvirtadalio amžiaus rezultatus: kokias valstybes svajojo sukurti tėvai-pradininkai ir ko buvo pasiekta. Pirmasis šio pokalbio ciklo dalyvis — Nepriklausomybės Akto signataras Rolandas PAULAUSKAS.

— Pone Paulauskai, šiandien Lietuvoje pradeda reikštis nauji visuomeniniai judėjimai. Įvairaus plauko politikai ragina žmones vienytis ir kovoti su „korumpuotu elitu“. Daugelis naudoja „Sąjūdžio“ pavadinimą. Jūsų manymu, ar reikia šaliai revoliucijos, kaip prieš 27 metus?

— Neabejotinai, mums reikia kažko naujo. Beveik 30 metų valdžioje tupi tie patys žmonės ir tos pačios partijos, todėl sulaukti iš jų ko nors naujo ir perspektyvaus mažai tikėtina. Tačiau visi tie atsirandantys visuomeniniai judėjimai nepajėgūs pakartoti „Sąjūdžio“ sėkmės, nes jie neturi idėjos.

Mes skirtingai žvelgėme į gyvenimą ir politiką, tačiau turėjome vieną tikslą, kurio siekėme bendromis jėgomis. Po to, kai tikslas buvo pasiektas, visi šie žmonės išsilakstė po įvairias partijas...

Šių dienų „Sąjūdis“, jei jam lemta atsirasti, turi remtis konkrečia idėja, tačiau čia ir išryškėja sudėtingumai, nes negali visi žmonės turėti vienodus požiūrius. Sakykim, praeitais metais turėjome rinkimus į Seimą. Juos laimėjo nauja partija „Valstiečių ir „žaliųjų“ sąjunga“, kurios atstovai labai nevieningi. Ir štai valdžioje atsidūrė žmonės, neturintys tarp savęs nieko bendro — jie skiriasi požiūriais, vertybėmis, todėl valdžioje šiandien apstu problemų.

Einant valdžion, būtina turėti konkrečius politinius įsitikinimus, savo šalininkus reikia rinktis ne pagal principą „patinka — nepatinka“, o pagal vertybes ir požiūrius į pasaulį.

— Norite pasakyti, jog Lietuvos žmonės nesuvokia, už ką balsuoja, o paskui kenčia dėl savo klaidų?

— Tai ne tik Lietuvos, tai viso pasaulio nelaimė. Pavyzdžiui, prancūzai prezidentu išrinko Makroną, bet kodėl žmonės už jį balsavo... Nemanau, jog rinkėjams patinka, kad jis didina darbo savaitę, lengvina darbininkų atleidimo procesą. Tai buvo jo programoje, jis to neslėpė, bet į tai niekas nekreipė dėmesio, nes prancūzai balsavo už „naują žmogų“.

Ir ką dabar matome? Po rinkimų jo reitingas ženkliai krito — tai didžiausias kritimas Prancūzijos istorijoje po prezidento rinkimų.

Kol Lietuvoje žmonės to nesuvoks, pareiškimai apie „Sąjūdžio“ atgimimą visiškai nieko nereikš. Reikalingi konkretūs žmonės, konkrečios mintys, būtina konkrečiai nubrėžti tai, ko mes norime ir už ką kovojame. Tik tokiu atveju panašūs judėjimai susilauks sėkmės. Šiandien visa tai abstraktu, tai kova su vėjo malūnais.

Visi naujų Lietuvos judėjimų šūkiai vienodi: „Mes kovojame už tai, kas gera, prieš tai, kas bloga“, tačiau realiame gyvenime taip nebūna.

— Šiandien Lietuva pergyvena ne geriausius laikus. Kasmet plečiasi problemų ratas, o žmonių mažėja. Kokia politinė jėga galėtų išgelbėti nykstančią valstybę, ko reikia visuomenei?

— Problema tame, kad vienai visuomenės daliai reikia nacionalinės vyriausybės, kitai — to nereikia. Pastarieji savo ateitį mato Europos Sąjungoje, jie visai ne prieš, kad Lietuva visiškai ištirptų toje Draugijoje. Tokie žodžiai, kaip tauta ir tautos interesai, jiems neturi reikšmės. Suvienyti šias dvi išskaidytas grupes beveik neįmanoma. Tai dar kartą patvirtina mintį, kad suburti visuotinį „Sąjūdį“ neįmanoma.

Sakyčiau, ir Rusijoje panaši situacija. Vieni žaidžia su Vakarais ir mato šalį Vakarų pasaulio dalimi, kiti ragina atsisakyti šios idėjos. Tai ir visuomenės, ir valdžios problema. Pavyzdžiui, Putinas — valdovo simbolis, jis siekia sukurti stiprią tautinę valstybę, o premjeras Medvedevas — klasikinis vakarietis ir liberalas.

— Ir kaip tada spręsti šią išsiskaidymo problemą?

— Žmonės skirtingi. Ir jiems reikia leisti būti skirtingais. Žiūrintys į šį pasaulį pro liberalius akinius visada jį matys kitokį, nei aš.

Žvelgdamas iš vertybių pozicijų, aš iškeliu liaudį ir tautą į pirmą vietą, nes žmogus — gyvūnas socialus.

Lietuvoje ši problema ypač aštri dėl masiškos emigracijos. Masiškos emigracijos problema — šalies išlikimo klausimas. Valstybė, kurioje žmonės blogai jaučiasi, valstybė, iš kurios žmonės bėga, negali egzistuoti. Ir iš čia išplaukia visos kitos problemos.

Todėl aš nesuprantu, kaip gali liberalai spjauti į tautos rūpesčius, toleruoti nuosmukio kultūrą, globalizacijos kultūrą, jeigu be tos tautos ir pačių liberalų nebūtų. Todėl aš žvelgiu į pasaulį per prizmę sveiko kolektyvizmo, kuriame tauta gali būti tik pirmoje vietoje.

— Pratęsiant neoliberalizmo ideologijos temą, noriu paliesti žiniasklaidos vaidmenį. Lietuvoje ji tiesiog persunkta neoliberalizmu, propaguojamos tam tikros vertybės ir įsitikinimai. Ar tai atsispindi mūsų visuomenėje?

— Žiniasklaidos vaidmuo didžiulis. Egzistuoja įvairūs tyrimai, įrodantys, jog informacija ir propaganda gerąja ir blogąja to žodžio prasme smarkiai įtakoja žmones. Neseniai amerikiečių mokslininkai pateikė tyrimų rezultatus, kuriuose teigiama, kad 85 proc. žmonių nepajėgūs turėti savo nuomonės. Jie lengvai pasiduoda įtakai.

Kas dar blogiau, mokslininkai tvirtina, kad 80 proc. žmonių, kuriems buvo primestos pozicijos ar požiūriai, atsisako keisti savo požiūrius, net jei jiems įrodoma, kad jie buvo suklaidinti.

Į visa tai atsižvelgiant nesunku suvokti, kad propagandos vaidmuo didžiulis ir pagrindinis. Ką žmogus girdi ir mato, tuo ir gyvena. Tik 15 – 20 proc. žmonių turi savo nuomonę ir nebijo jos ginti.

— Sugrįžkime prie politikos. Neseniai prezidentė Grybauskaitė paminėjo 8 metų buvimo šiose pareigose jubiliejų. Kaip per tą laikotarpį pasikeitė Lietuva? Kaip ją įtakojo įvykiai pasaulyje?

— Ir Lietuva, ir Europa, ir Rusija, ir visas pasaulis pergyvena pereinamąjį laikotarpį. Faktiškai mes atėjome prie civilizacijų susidūrimo ribos.

Dabartiniai pasaulio įvykiai turės didžiulių pasėkmių dešimtmečiams. Prie šalies vairo stovintys žmonės turi tai suvokti, bet, deja, mūsiškas elitas to nesuvokia. Lietuvos politinis elitas nėra tie 15 – 20 proc. žmonių, sugebančių savarankiškai mąstyti.

Šia liga pastaraisiais metais serga visi mūsų pirmieji asmenys. Jie nesuvokia pasaulyje vykstančio geopolitinio žaidimo esmės. Jie nesuvokia Lietuvoje ir Europoje susikertančių interesų. Jie mato pasaulį plokščią ir vienodą. Tai ne juodai baltas situacijos matymas, tai daug blogiau...

— O ką jūs galvojate sakydamas, kad mes gyvename pereinamuoju laikotarpiu?

— Aš neveltui pasakiau, kad mes gyvename labai sudėtingu istorijos laikotarpiu. Kažkas panašaus buvo prieš abu pasaulinius karus. Manau, šiandien jau vyksta Trečiasis pasaulinis karas, tik jis kitoks, nei anie. Būtina suprasti, kokie interesai susiduria regionuose ir sferose, o žmonės žvelgia į pasaulį labai primityviai. Jie neabejoja, kad egzistuoja ir geri, ir blogi vaikinai.

Būtina suprasti, jog nėra nei vienų, nei kitų. Yra valstybių interesai, interesai atskirų grupių, tautų ir valstybių, kurios dėl jų kaunasi.

Egzistuoja labai sudėtinga vakarietiška finansų sistema, gyvenanti skolų emisijos, niekuo neparemtų pinigų sąskaita. Ir tai būtina suprasti ir matyti, žvelgiant į dabartinį pasaulį ir į interesų susidūrimus — o Lietuvos lyderiai to nemato ir nesupranta.

O juk demokratija — tokia sistema, kuri atveda valdžion visiškai atsitiktinius žmones. Jie mirguliuoja televizoriuje, žaidžia žmonių jausmais, ateina valdžion, ir mes matome, kad jie neturi nei patirties, nei atitinkamos kompetencijos.

Neminėsiu konkrečių pavardžių. Galime be jų sumodeliuoti situaciją. Įsivaizduokime: žmogui jau apie 60, ir mes iki šiol nieko negirdėjom iš jo apie valstybę, apie jo požiūrį į pasaulį, apie jo vertybes... ir staiga, sulaukęs 60 metų, jis tampa labai svarbiu asmeniu. Sutikite, gana sunku tikėtis, jog jis staiga taps politikos filosofu...

Kaip sakė Čerčilis, „demokratija — blogiausia valdymo forma, jeigu nekreipsime dėmesio į visas kitas“.

Deja, dažniausiai demokratiški rinkimai įvairiose šalyse išmeta į politinę areną visiškai atsitiktinius žmones, kurie paskui sukelia labai daug problemų. Ir Lietuva čia nėra išimtis.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 13 — id: `scraped:rubaltic_lt:359f39781f8f2483`

**Title:** Girtuoklių, savižudžių ir emigrantų šalis: kodėl Lietuvoje viešpatauja pesimizmas?

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Du trečdaliai Lietuvos gyventojų mano, kad situacija šalyje blogėja. Amerikiečių sociologai tvirtina, jog lietuviai — mažiausiai linkusi teigiamas emocijas reikšti pasaulyje tauta. Nežiūrint šalies vadovybės tvirtinimų, jog ekonomika auga ir gyvenimas gerėja, Lietuvoje vyrauja socialinis pesimizmas, o jo išdava — rekordinis Europos ir pasaulio mastu alkoholizmas, savižudybės ir emigracija.

Kaip parodė praeitą mėnesį Baltijos tyrimų sociologinės kompanijos pravesti visuomenės nuomonės tyrimai, du trečdaliai lietuvių mano, kad situacija šalyje blogėja. Pesimistiškai į šiandieninę Lietuvą žvelgia 64 proc. gyventojų, ir tik 35 proc. lietuvių mano, kad reikalai šalyje gerėja.

Per pastarajį mėnesį skaičius lietuvių, manančių, kad reikalai Lietuvoje pastoviai blogėja, padidėjo trim procentais.

Tuo pačiu metu amerikiečių sociologijos institutas Gallup 142 pasaulio šalyse pravedė žmonių emocionalinės būklės tyrimus. Respondentų prašė atsakyti, ar jie patyrė praėjusią dieną 5 teigiamas ir 5 neigiamas emocijas. Neigiamos emocijos — pyktis, stresas, liūdesys, fizinis skausmas ir baimė.

Rezultatai parodė, jog lietuviai — nelaimingiausia pasaulio tauta. Kaip ir gruzinai, azerbaidžianiečiai, ukrainiečiai bei irakiečiai, lietuviai gyvenime mažiausiai patiria teigiamų emocijų.

Šio pesimizmo išraiška, įrodymas ir pasekmė — alkoholizmas, savižudybės ir emigracija. Šie Lietuvos rodikliai taip pat užima aukščiausias pozicijas.

Pasaulinė sveikatos apsaugos organizacija daug metų įvardina Lietuvą labiausiai geriančia šalimi. Pasak paskutinės jos ataskaitos, praeitais metais respublikoje buvo išgerta vidutiniškai 16 litrų alkoholio vienam asmeniui. „Tai, naujausiais paskaičiavimais, verčia ją laikyti didžiausia Europos girtuole, labiausiai geriančia šalimi pasaulyje“, — šių metų gegužę pareiškė Vilniuje Pasaulio sveikatos apsaugos Europos biuro Neinfekcinių chroninių susirgimų ir sveikos gyvensenos įtvirtinimo departamento direktorius Ganden Galea.

Šiuos PSA duomenis nenoromis patvirtino ir Lietuvos valdžia.

Be absoliutaus pirmavimo pasaulyje vartojant alkoholį Lietuva liūdnai garsėja ir savižudybių skaičiumi. Pasaulinės sveikatos apsaugos organizacijos, užsiimančios psichinių susirgimų profilaktika, ataskaita rodo, kad Lietuva pagal savižudybes pirmauja Europoje. Joje 100 tūkst. gyventojų tenka 32,7 savižudybių — tai europietiškas rekordas.

Be to, Lietuva yra pasaulio rekordininkių pagal savižudybių skaičių trejetuke. Labiausiai žudosi Šri-Lankos gyventojai — 35 šimtui tūkst. gyventojų. Lietuvos respublika nuo šios „čempionės“ mažai atsilieka.

Šiais metais bėgimas iš respublikos ūgtelėjo 1,5 karto. Jei per praeitų metų pirmąjį pusmetį iš šalies išvyko 21 248 žmonės, tai per tą patį šių metų laikotarpį — 31 713.

Tuo metu, kai šalies prezidentė ir vyriausybė giriasi gerėjančia socialine–ekonomine situacija, BVP ir pragyvenimo lygio augimu, emigracija iš šalies kasmet didėja. Nuo 1991 metų vien tik oficialiais duomenimis su Lietuva atsisveikino ne mažiau 700 tūkstančių gyventojų, o atsižvelgiant į tai, jog nemažai lietuvių neregistruoja savo išvykų, tikrieji emigracijos skaičiai gali viršyti milijoną.

Rekordinė emigracija veda prie rekordinio išmirimo. Europos statistinės tarnybos koreguoja Lietuvos išmirimo prognozes pablogėjimo link. Pasak šį pavasarį patikslintos Eurostato prognozės, 2050 metais Lietuvoje beliks 2 milijonai gyventojų, o 2080–aisiais — tik 1650 tūkstančių.

Ir taps ji senelių namais, nes vyresni nei 60 metų žmonės sudarys 85 proc. šalies gyventojų.

Jau dabar vyresni nei 65 metų Lietuvos žmonės sudaro 19 proc. (549 tūkst.). Senatvės koeficientas nuo 2001 metų išaugo 1,8 karto. Ir tuo metu kai Šiaurės šalyse (ir Lietuva save laiko tokia) pastebima teigiama kartų kaita (norma tapo trečias vaikas šeimoje), Lietuvoje mirtingumas lenkia gimstamumą, o vaikai joje apsireiškia daugiausia sezono metu — vasarą, kai tėvai juos iš užsienio atveža seneliams.

Tai tokios objektyvios Lietuvos realijos.

Tačiau subjektyvi realybė, kaip žinia, kita. Toje lygiagrečioje realybėje, kuri piešiama prezidentų pasisakymų metu ir transliuojama šaliai bei pasauliui, gaudžia Seimui ir vyriausybei skirti pergalių varpai, nes Lietuva — sėkminga europietiška šalis, besidžiaugianti nauju, laisvu ir sočiu gyvenimu, ištrūkusi iš „nepraustos Rusijos“ įtakos.

Tik su ta „neprausta Rusija“ ne viskas klostosi taip, kaip norėtųsi. Dėdulės Landsbergio sektos liudytojai vis dar įsitikinę, jog „Rusynas“ ne šiandien — ryt galutinai nusigers ir nugaiš patvory. Pats Landsbergis praeitą rudenį pareiškė neginčytiną verdiktą, jog Rusija „visa šūde“.

Bet vis dėlto čia kažkas ne taip: pagal alkoholio suvartojimą vienam gyventojui Lietuva užima pirmąją vietą pasaulyje, o Rusija — penktąją. Pagal savižudybes Lietuva puikuojasi pirmajame pasaulio trejetuke, o Rusija nepateko net į dvidešimtuką. Nepriklausomybe besidžiaugianti Lietuva prarado beveik trečdalį gyventojų, o Rusija — tik vieną procentą. Lietuva — gyventojų emigracijos rekordininkė, o Rusija — antroje po JAV vietoje pagal imigrantų skaičių. Lietuva išmiršta, o Rusijoje auga gyventojų skaičius.

O  serga rusofobija visų pirma valdančioji klasė, kurią slegia liguisti prisiminimai apie Didžiąją Lietuvos kunigaikštystę, kuri amžinai varžėsi su Moskovija dėl Rytų Europos kontrolės.

Eiliniai lietuviai liga dėl prarastos didžiausios Europoje valstybės neserga ir nelinkę konkuruoti su „Moskovija“. Lietuvos socialinių tyrimų centro apklausos rezultatai rodo, jog 90 proc. lietuvių jaudina dvi temos: emigracija ir nedarbas. Be to, didžiulė dauguma gyventojų įsitikinusi, kad Lietuvos saugumui visų pirma gresia nusikalstamumas, energetinė priklausomybė, skurdas, diskriminacija ir alkoholizmas.

Realiu gyvenimu gyvenančius Lietuvos žmones jaudina realios problemos. Lietuviai pakartojo tas pačias problemas, pagal kurias tarptautinės tyrimų organizacijos skiria Lietuvai pirmąsias pozicijas pasaulyje: alkoholizmas, emigracija, skurdas.

Tačiau valdantieji, nesugebantys išspręsti šių problemų, už sugebėjimą ryžtingai žengti pirmyn vis labiau nekenčia Rusijos ir gąsdina savo gyventojus tankais, „Kremliaus propaganda“, „imperiška agresija“ ir „hibridiniu karu“.

Pastoviai klausantis tokių „iškiliausių šalies žmonių“ paistalų ir matant, jog jie serga kolektyvinės šizofrenijos liga, iš tiesų eiliniam piliečiui belieka arba nusilakti, arba svetur išdumti, arba kilpą ant kaklo užsinerti.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 14 — id: `scraped:rubaltic_lt:62a9584bda27601e`

**Title:** Barselona — Kaunas — Doneckas: kodėl ispanas iš Lietuvos išvažiavo į Donecko liaudies respubliką?

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Analitinis portalas RuBaltic.Ru atnaujina specialųjį projektą apie „nuostabių emigrantų“ gyvenimą nauju pavadinimu „Lagaminas“. Tikrai neeilinę istoriją mums papasakojo Migelis Puertas — kilęs iš Barselonos, Europos Sąjungos pilietis, blogeris, gyvenęs Lietuvoje apie 10 metų.

Migracija antraip

Dauguma Pabaltijo šalių gyventojų emigruoja į Vakarų Europą. Mano migracija — priešinga kryptimi. Aš gimiau netoli Barselonos, ten mano šaknys, šeima. Būdamas 28 metų (2006 m.) išvykau iš Ispanijos į Lietuvą, kur gyvenau 10 metų, o dabar gyvenu DLR ir dirbu dėstytoju Donecko aukštojoje mokykloje. Teko gyventi ir kitose šalyse: Italijoj, Latvijoj, Estijoj ir t.t.

Pirmieji gyvenimo metai Lietuvoje

Dėstyti aukštojoje mokykloje pradėjau dar gyvendamas Ispanijoje. Darbas suteikė galimybę daug keliauti po Europą. Vieno projekto Estijoje metu susipažinau su mergina iš Lietuvos, įsimylėjau — ir po kiek laiko persikėliau gyventi į Kauną.

Bet man nieko nenutiko, nors iš pradžių nežinojau, kuo Lietuvoje užsiimsiu. Įsidarbinau po 5-6 mėnesių. Tačiau dviejų metų eigoje negalėjau suprasti šalies ir jaučiausi joje turistu, kol neišmokau lietuvių kalbos (užsieniečiui ši kalba gana sunki). Tik baigiantis savo gyvenimo Lietuvoje laikotarpiui pradėjau dėstyti lietuviškai.

Kodėl per 10 metų aš neišmokau rusų kalbos? Kaune, lyginant su kitais Lietuvos miestais, gyventojai beveik nekalba rusiškai. Jaunimas šios kalbos visai nežino ir nesupranta. Nors mokytis rusų kalbos praktiškiau, man nebuvo reikalo jos mokėti.

Pirmieji metai Lietuvoje buvo nuostabūs. Aš buvau jaunas, turėjau pinigų, aš jaučiausi lyg super žvaigždė: užsienietis lietuviškame Kaune (tuo metu užsieniečiai daugiausia vyko į Vilnių). Aš pamilau šią šalį.

Maidano šmėkla Lietuvoje

Iki ukrainiečių Maidano buvo gera gyventi Lietuvoje, tačiau paskui atsirado kažkas panašaus į diktatūrą.

2013 metais, gyvendamas Lietuvoje, aš pradėjau rašyti blogą apie konfliktą Ukrainoje. Tuo metu aš jau mokėjau lietuvių kalbą ir galėjau žiūrėti lietuviškas televizijos laidas, supratau, kas dedasi šalyje.

Net mano universitete buvo renkamos lėšos tikslu remti Maidano protestuotojus, o paskui — dešiniuosius radikaliuosius batalionus. Aš, buvęs katalonietis, stebėjausi: Lietuvos vyriausybė remia Ukrainos nacionalistus.

Būtina žinoti, kad beveik visas žiniasklaidos priemones Lietuvoje kontroliuoja valstybė. Ir žmonės tikrai tiki, kad „Aidaro“ ir „Azovo“ batalionai kovoja už Ukrainos laisvę. Savo bloge aš stengiausi demaskuoti šį melą. Kartą vienas mano studentas man parašė: „Migeli, tu kovoji prieš sistemą.“

Persekiojimų pradžia

Kai blogas tapo pakankamai populiarus, aš buvau žiniasklaidos pavaizduotas kaip Putino agentas, o mano studentams buvo pasakyta, kad aš — labai pavojingas žmogus. Jie patyrė šoką. Po to aš pradėjau gauti įžeidžiančius pranešimus.

Po to Lietuvos saugumo tarnyba apie tai informavo rektorių Vytauto Didžiojo Universiteto, kuriame aš dirbau. Rektorius išsikvietė mane į savo kabinetą ir pasakė — arba aš uždarau savo blogą Facebook‘e, arba būsiu atleistas.

Normalioje šalyje būtų galima apginti savo teises teisme, tačiau Lietuvoje teisinė sistema priklausoma, korumpuota, ją kontroliuoja valstybė. Aš teberašiau apie krizę Ukrainoje — ir už tai buvau atleistas. Aš kreipiausi į universiteto rektorių laišku  ( laiško tekstas anglų / lietuvių kalba), kuriame rašiau apie man taikytus represinius metodus. Jokio atsako negavau.

Aš išvykau iš Lietuvos dėl politinės situacijos šalyje

Po to, kai buvau atleistas, likau Lietuvoje. Turėjau pinigų, kitą darbą. Aš neatsisakiau savo blogo, ir jaučiau pastovų spaudimą. Pavyzdžiui, kartą kavinėje sutikau draugą.

Draugas dirbo miesto administracijoje. Po dviejų dienų jis buvo iškviestas saugumo organų, jam buvo pasakyta: „Kodėl tu susitikinėji su Lietuvos priešu? Jeigu ir ateityje su juo bendrausi, vadinasi, tu rusų propagandos pagalbininkas ir tavo karjera politikoje užsibaigs.“

Panaši istorija nutiko ir su mano buvusia mergina, su kuria aš tebepalaikiau draugiškus santykius. Mano merginos motina dirbo vieno mažo Lietuvos miestelio administracijoje. Lietuvos specialiosios tarnybos perspėjo, kad ji bus atleista, jei jos dukra tebesusitikinės su „Lietuvos priešu“. Tokiu būdu aš pamažu praradau savo draugus. Juos nugąsdino specialiosios tarnybos, ir jie nenorėjo patekti į „juodą sąrašą“. Lietuvoje tai reiškia prarasti darbą.

Po kiek laiko aš praradau vieną, o paskui ir kitą darbą. Daug žmonių buvo atleista politiniais sumetimais, net profesorių, ką jau kalbėti apie mane. Pavyzdžiui, Algirdas Degutis 30 metų dirbo filosofijos profesorium, tarybiniais laikais buvo politinis kalinys, ir jis taip pat buvo atleistas.

Prie mano namo net budėjo du agentai civiliai rūbais. Buvo atvejų, kai tokie agentai lindo į lietuvių namus, kurie smerkė Maidaną, NATO ir kritikavo Grybauskaitės vyriausybę. Iš piliečių buvo atiminėjami kompiuteriai ir kitos elektroninės priemonės, o paskui jie susilaukė kaltinimą esą Putino agentai. Lietuvos piliečiai — Putino agentai? Sutikite, tai juokinga!

Aš nelaikau savęs Lietuvos priešu. Aš mylėjau šią šalį. Ten turėjau mylimą merginą, draugų, darbą. Tačiau buvau priverstas išvykti. Ankstyvą 2016 metų birželio 3 dienos rytą (pamenu, tada lijo) aš atidaviau raktus savo nuomuotojui, pasiėmiau daiktus bei dokumentus ir išvykau net neatsisveikinęs su savo mergina.tiesiog nepajėgiau jai pasakyti: „Žinai, aš rytoj išvažiuoju“. Tai buvo labai sunku.

Aš norėjau pasakoti tiesą

Aš išvykau į DLR tikslu iš ten pasakoti žmonėms, na, ir savo studentams Lietuvoje, kas iš tikrųjų dedasi Donbase, demaskuoti tą propagandą, kurią skleidžia televizija.

Lietuvos televizija blogesnė už amerikiečių. Dėka televizijos ir vadovėlių Lietuvos vyriausybė užaugino kartą, kuri nekenčia Rusiją. Aš neabejoju — vyriausybė ruošia šalį karui.

Bet aš žinojau, kur važiuoju. Kai aš dar gyvenau Lietuvoje, viena Donecko aukštoji mokykla pasiūlė man darbą.

Donbasas ir Lietuva. Kas bendro?

Kai atvykau į DLR, supratau, kad tarp Donbaso ir Lietuvos gyventojų nėra didelio skirtumo. Pavyzdžiui, panašios virtuvės: abiejose šalyse žmonės mėgsta čeburekus, šašlykus, koldūnus, geria kefyrą. Tiesa, man atrodo, jog Donbase maistas skanesnis.

Žmonės jose mentaliai panašūs: vienodai neapkenčia alternatyvios nuomonės. Nors DLR gyventojai lankstesni, laisvai reiškia savo emocijas ir mėgsta kalbėti.

Donbasas ir Lietuva: skirtumai

Tačiau tarp Lietuvos ir DLR daug skirtumų: jie skirtingai interpretuoja istorinius faktus. Lietuviai save laiko Rusijos aukomis (nors tai netiesa) ir remia Ukrainos nacionalistus. DLR gyventojams nacionalistai ir Stepanas Bandera ne didvyriai, o nusikaltėliai. O dar Donbase išties mylima Rusija.

Donbase įvykęs sukilimas buvo nukreiptas prieš regiono integraciją į euroatlantinę ašį. DLR žmonės pasižymi savo vertybėmis, mąstymo būdais, tradicijomis. Gal jie ir žiūri amerikietiškus filmus, tačiau amerikietiško pasaulio kratosi. Jie jaučia komfortą būdami su Rusija ir nenori su ja kovoti, nes neįmanoma kovoti patiem su savimi. Donbasas pasižymi identiškumu, ko nėra Lietuvoje. Lietuvių identiškumas — būti rusofobu. Ir tai man nesuprantama!

Donbaso ir Lietuvos problemos

Lietuvoje vyrauja dvi pagrindinės problemos: nacionalistinė vyriausybė ir ekonomiškai prasta apdėtis. Šios dvi priežastys masiškai veja lietuvius iš šalies. Aš mačiau, kaip dešimties metų eigoje Lietuva keitėsi, ir ne gerąja prasme: žodžio laisvės nebuvimas, kainų augimas, blogas pensininkų socialinis aprūpinimas, emigracija iš šalies, lietuviškos kultūros išstūmimas Vakarų kultūros pastangoms.

O tuo metu valstybė rūpinasi ginklavimusi ir perka senus JAV tankus, palaiko antirusišką paranoją ir ruošia žmones karui. Lietuvoje gatvėse galima pamatyti daugiau jaunimo kariškomis uniformomis, nei Donbase. Tai mane stebina.

Man atrodo, jog pati rimčiausia Donbaso problema šiandien — karas. Tačiau turiu pasakyti, kad aš vis dar neįsiintegravau į visuomenę, nes nemoku rusų kalbos. Todėl įvykius stebiu lyg ir iš šono. Tikriausiai čia dar yra nemažai problemų.

Straipsnis kitomis kalbomis

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 15 — id: `scraped:rubaltic_lt:7e3c28984b1efd91`

**Title:** Rusija išreikalaus iš Pabaltijo tarybinių laikų skolas

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Rusijos ambasadorius Lietuvoje Aleksandras Udalcovas paskaičiavo, kad Lietuva už tarybinį laikotarpį turi išmokėti Rusijai 72 milijardų dolerių kompensaciją. Tokie oficialaus Rusijos atstovo pareiškimai negali būti asmenine nuomone — Maskvoje galvojama, kad Pabaltijui reikėtų pateikti tarybinių laikų skolų sąskaitą ir pareikalauti iš Lietuvos, Latvijos ir Estijos materialinės kompensacijos už visas sąjunginio Centro investicijas ir dotacijas į jų ekonomiką.

„Socializmo vitrina“ tarybinis Pabaltijis tapo dėka visiško sąjunginio Centro palaikymo. „Mūsų mažieji vakarai“, vartotojiškas vidutiniškai pasiturinčių tarybinių piliečių rojus prie Baltijos krantų buvo dirbtinai sukurtas visos didžiulės šalies donorės pastangomis.

Nafta, dujos, chemijos produkcija — visa tai buvo parduodama „Pabaltijo sesutėms“ dotavimo kainomis, daugiau kaip perpus mažesnėmis. Žemės buvo melioruojamos sąjunginio biudžeto sąskaita, o techniką ir trąšas Maskva tiekė Pabaltijui dotavimo kainomis, kurios sudarė 48 proc. realios vertės. Tuo metu, kai visoje TSRS buvo nusausinta 6,8 proc. žemės ūkio naudmenų, Pabaltijyje šis procentas siekė 80. Palyginimui: kaimyninėje su Latvijos TSR Pskovo srityje buvo nusausinta 2 proc. žemės ūkio naudmenų.

Tai yra, ta produkcija, kuria didžiavosi Pabaltijis, buvo gaminama svetimais pinigais.

Rusijos vidurio žmonės gyveno daug blogesnėse sąlygose, nei lietuviai, latviai ir estai. Tolimose Rusijos vietovėse vyravo aštrus deficitas. Nenusipirksi mėsos. Būtiniausio poreikio produktai buvo parduodami pagal korteles — „talonus“. O Pabaltijis buvo aprūpinamas pagal pirmą kategoriją — kaip Maskva ir Leningradas.

Keliai ir būstai Pabaltijyje buvo statomi žymiai geriau, nei RTFSR. Ir pinigai šioms statyboms keliavo būtent iš RTFSR, projektavo šiuos kelius ir būstus rusų inžinieriai, statė Rusijos darbininkai.

Tada buvo manoma, jog tai teisinga. Juk tas Pabaltijis — „Tarybinė Skandinavija“, „Europa“...

Pabaltijo respublikos TSRS sudėtyje gyvavo kaip išlaikytinės. Taip pat, kaip šiuo metu Europos Sąjungoje. Skirtumas tik tas, kad išlaidavo joms anuometinis Centras daugiau, o pats gyveno blogiau, nei jo pabaltijietiški pakraščiai.

Tarybų Lietuva gamino per metus produkcijos vienam gyventojui už 13 tūkst. dolerių, o eikvojo 23,3 tūkst. Iš kur ėmė tuos viršijančius 10,3 tūkstančių? Iš sąjunginio Centro investicijų į Lietuvos kelius, visuotiną dujofikaciją, elektrofikaciją, melioraciją ir atominę elektrinę.

BVP vienam Latvijos gyventojui sudarė 16,5 tūkst. dolerių, o eikvojimas — 26,9 tūkst. Iš kur viršijantys 13 tūkstančių dolerių? Iš tarybinės liaudies, dėka kurios ant Rygos prekystalių visada buvo rūkytos dešros, kai tuo metu Rusijos toliuose žmonės vargo ilgose eilėse dėl numėsintų kauliukų.

Estijos TSR gamino per metus produkcijos vienam žmogui už 15,8 tūkst. dolerių, o eikvojo 35,8 tūkst. — skirtumas didesnis daugiau nei du kartus. Viršijančią sumą užtikrino vis tie patys „sovietiniai okupantai“.

Nepaprastasis ir įgaliotasis Rusijos Federacijos ambasadorius Lietuvos Respublikoje Aleksandras Udalcovas pareiškė, kad Lietuva turi padengti tarybinių laikų skolą Rusijai, kuri sudaro 72 milijardus dolerių.

Rusijos ambasadorius priminė, kad 1940 metais įstojusi į Tarybų Sąjungą Lietuva buvo agrarinė šalis, turinti „nedidelį socialinį ekonominį potencialą“, kuris buvo sunaikintas Antrojo pasaulinio karo metu. „Būdama TSRS sudėtyje, Lietuva turėjo galimybę vystyti savo liaudies ūkį stambiu mastu, nors tuo metu gana menka buvo nacionalinių pajamų apimtis. Tai leido ne tik sparčiais tempais atkurti karo metu sugriautą ūkį, bet ir iš naujo sukurti pramoninę gamybą“, — pasakė Udalcovas.

Rusijos ambasadoriaus Lietuvoje duomenimis, į Lietuvos ekonomikos vystymąsi 1940–1990 metais buvo investuoti 72 milijardai dolerių. To pasekoje respublikoje buvo sukurtos chemijos ir naftos chemijos pramonės šakos, pastatytos stambios įmonės.

Lietuvos politikai į šiuos Udalcovo žodžius reagavo emocionaliai. „Tautos tėvas“ Vytautas Landsbergis pavadino Rusijos ambasadorių „kvaileliu“, su kuriuo jis net nesiginčys, nes jį ir taip „gamta nuskriaudė“.

Senantvišką „Dėdulės“ pyktį galima suprasti. Prityręs politikas, Landsbergis negali nesuvokti, jog žodžius apie 72 milijardų dolerių skolą diplomatas neištarė šiaip sau. Aleksandras Udalcovas — oficialus Rusijos atstovas, ir viešų pareiškimų metu negali išsakyti asmeninę nuomonę.

Jeigu ambasadorius kalba apie 72 milijardus  dolerių, tai ne šiaip žodžiai, o oficiali Rusijos pozicija, ir Udalcovo pareiškimas buvo suderintas su Maskva ir paviešintas Rusijos užsienio politikos rėmuose.

Rusijos ambasadoriaus Lietuvoje pareiškimas — netiesioginis to patvirtinimas. Beje, ne vienintelis. Rusijos archyvų darbuotojai pastaraisiais metais kruopščiai dirba siekdami nustatyti tikslią materialinių investicijų į Pabaltijį per tarybinį pusšimtį metų sumą. Pirmieji šio darbo vaisiai — prieš dvejus metus Rusijos mokslų akademijos Rusijos istorijos instituto išleistas dokumentų rinkinys „Tarybinės ekonomikos modelis. Sąjunginis Centras ir Pabaltijo respublikos. 1953–1966 metai“. Išspausdinti dokumentai aiškiai pasako, kas, kam ir kiek sumokėjo.

Ir juk šis rinkinys — tik ledkalnio viršūnė. Rusijos archyvų darbuotojai ir istorikai žada išplėsti savo darbo chronologinius rėmus ir suskaičiuoti, kiek iš viso sąjunginis Centras investavo į Pabaltijį tarybų valdžios metais. Kiek kainavo Ignalinos AE, Naujojo Talino uostas, hidroelektrinė prie Dauguvos, keliai, tiltai ir gyvenamieji kvartalai.

Galima prieštarauti, jog užsiimti tuo Rusijai neverta, nes trys išdidžios demokratijos prie Baltijos jūros nusususios kaip bažnyčios žiurkės, ir išpešti iš jų nėra ko. Bet tai ne visai taip.

Pirma, visada galima pareikalauti  kaip kompensaciją tai, ką dar jos turi. Pradžiai, konfiskuoti Pabaltijo nuosavybę užsienyje, pavyzdžiui, ambasadų pastatus ir kultūros centrus Rusijoje. Paskui paskelbti pirmųjų Pabaltijo asmenų tarptautinę paiešką. Kaip piktybiškai neatiduodančių skolų. Gaudyti juos po vieną ir tupdyti į „skolininkų duobę“. O jei jiems tai nepatinka, lai kaunasi su Rusija tarptautiniuose teismuose. Rusija, beje, taip pat turi kreiptis į teismą ir teisminiu būdu išieškoti skolas.

Antra, kalbėtis su paties Pabaltijo valdžiomis apie materialinės kompensacijos Rusijai už tarybinį laikotarpį išmokėjimą nėra prasmės. Šios valdžios vis tiek nieko nesprendžia: jos nesavarankiškos, o jų šalys seniai prarado suverenitetą.

Pateikti sąskaitą už Pabaltijo išlaikymą reikia jo realiems viršininkams Briuselyje ir Vašingtone.

Jie apie Krymą, o Putinas su Lavrovu — apie Pabaltijį.

Juk Lietuva, Latvija ir Estija egzistuoja ne pačios sau. Tai dalis Vakarų pasaulio, ir Vakarai atsako už jas. Ir todėl nereikia drovėtis — būtina išaiškinti vakarietiškiems lyderiams susidariusią keblią padėtį.

Esą  NATO  ir Europos Sąjungos sudėtyje egzistuoja trys valstybėlės, kurios pakilo ir gyvena šiandien dėka Rusijos sukurtos joms infrastruktūros. Atiduoti  skolų nepajėgios, todėl būkite geri — padenkite jas jūs kaip jų vyresnieji draugai ir globėjai.

Nes skaičiai akivaizdžiai byloja, kad Pabaltijis buvo okupavęs Rusiją ir apiplėšinėjo ją, o ne antraip.

Žinoma, JAV ir Europos Sąjunga ilgai nesutiks su Rusijos reikalavimais. Pabaltijo skolų „išmušinėjimas“ gali užsitęsti ne vienerius metus, o gal ir dešimtmečius.

Bet galų gale Vakarams šis ginčas įkyrės. Iš Pabaltijo vis tiek jiems jokios naudos, o draugauti su Rusija kuriame nors istoriniame posūkyje atsiras politinė būtinybė. Todėl, negadinant santykių su strategiškai svarbiu partneriu koalicijoje prieš kokią nors Kiniją, Pabaltijį paprasčiausiai  atiduos Rusijai.

Petras Pirmasis prieš tris šimtus metų nupirko Estliandiją ir Lifliandiją iš Švedijos už 2 milijonus jefimkų — dabar Rusija Pabaltijo žemes atgaus nemokamai. Skolų padengimo sąskaita. Ir tai taps Pabaltijo valstybėms pačiu geriausiu scenarijumi.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 16 — id: `scraped:rubaltic_lt:291673898bb42c3c`

**Title:** „Lietuvos nepriklausomybės tėvas“: šalyje visiškai nėra tvarkos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuva pergyvena negeriausius laikus. Masiška emigracija, sudėtinga ekonominė situacija, katastrofiška padėtis regionuose, eilinių piliečių skurdas ir valdžios žlugdanti politika veda šalį prie išmirimo. Tokios nuomonės yra Lietuvos Respublikos tėvas-pradininkas, Nepriklausomybės akto signataras Zigmas Vaišvila.

Duodamas interviu analitiniam portalui RuBaltic.Ru, signataras pasakė, jog „betvarkė“ ir valdžios „politinė trumparegystė“ pasiekė savo apogėjų. „Valdžią šalyje uzurpavo siauras asmenų ratas — taip vadinamas elitas, kuris atstumia visus su juo nesutinkančius. O tie, kurie nebijo pasisakyti prieš jų politiką, patenka į liaudies priešų sąrašą“, — konstatuoja jis.

Šiandien Lietuvoje kyla nauja „Atgimimo“ banga. Vienytis po atnaujinto „Sąjūdžio“ vėliavomis ragina buvęs prezidentas Rolandas Paksas ir kiti visuomenės veikėjai — „nepriklausomybės tėvai“, kurie prieš 29 metus išvedė tautą į gatves ir apgynė Lietuvos teisę būti laisva šalimi.

Vienas iš Lietuvos „nepriklausomybės tėvų“ Zigmas Vaišvila to nenorėdamas tapo disidentu. Vaišvila neslepia — politinis elitas pasistengė padaryti taip, kad jo vardas būtų užmirštas pastangomis konservatorių-„landsbergininkų“, uzurpavusių visuomeninės nuomonės monopoliją; šiandien jis paverstas „liaudies priešu“.

Praeitais metais Lietuvos specialiosios tarnybos pavadino Vaišvilą žmogumi, keliančiu grėsmę nacionaliniam saugumui. Paradoksas tame, jog signataras buvo tarp tų, kurie kūrė Lietuvos specialiąsias tarnybas. 1991–1992 metais jis vadovavo Valstybės saugumo departamentui. Likimo ironija: jo sukurta specialioji tarnyba ir jo išauklėti agentai dabar jį medžioja.

— Pone Vaišvila, kaip Jūs reaguojate į Jūsų kolegų ir prezidento Pakso raginimą organizuoti naują „Sąjūdį“? Jūsų manymu, ar gali Lietuvos gyventojai sukelti naują „revoliuciją“?

— Deja, šiandien aš nesu aktyvios politikos dalyvis, todėl negaliu tiksliai vertinti šio judėjimo. Pati idėja gera. Gerai, kad apie ją kalbama, gerai, jog dar yra žmonių, kuriuos jaudina padėtis šalyje ir kurie supranta, kad taip daugiau negalima gyventi. Įdomu ir tai, kad „Sąjūdžio“ atkūrimo idėją paskelbė Paksas: nors jis šiame judėjime nedalyvavo, tačiau jo vertybės, manau, jam artimos...

— Kai Jūs kalbate apie betvarkę, ar ne valdžios norą apriboti žodžio laisvę turite omenyje?

— Ir norą apriboti žodžio laisvę, ir persekiojimo formas, ir bendrą situaciją. Kur nepažvelgsi, visur pas mus didžiulės problemos. Tačiau žodžio laisvė ir kitaip mąstančių persekiojimas, žinoma, pagrindinė problema. Pas mus vyksta „raganų medžioklė“.

Ir aš tapau medžioklės objektu. Praeitais metais specialiosios tarnybos pavadino mane žmogumi, keliančiu grėsmę nacionaliniam saugumui. Mane, kuris stovėjo prie nepriklausomybės ištakų ir kūrė tas tarnybas.

— Šiandien Lietuvos valdžia pastoviai kalba apie ekonominius pasiekimus ir akcentuoja visišką atsiskyrimą nuo Rusijos. Jūsų manymu, tai normalu?

— Valdžia švaisto liaudies pinigus. Labiausiai mus jaudina energetinė nepriklausomybė nuo Rusijos, šiuo tikslu išleisti dideli valstybės biudžeto pinigai. Mes išsinuomavom plaukiojantį SGD terminalą Independence ir perkam dujas iš Norvegijos, kurios daug brangesnės už rusų.

Iš esmės, šis terminalas — labai brangus žaisliukas, kuris neatsiperka. Kasdien žmonės už jį moka po 150 tūkst. eurų! Ir tai todėl, kad niekam nerūpėjo praradimai, rizika. Tas laivas mažiausiai keturis kartus didesnis už tą, kuris buvo reikalingas Lietuvai. Jis mums neapsakomai nuostolingas, jis neatsiperka, ir projektas nerentabilus, bet apie tai niekas nekalba.

— Ir kas gi kaltas?

— Kalčiausias buvęs ekonomikos ministras Rokas Masiulis, aklai vykdęs visus prezidentės Grybauskaitės sumanymus. Jis istorikas, tad ką gali išmanyti tokiuose reikaluose? Kas padaryta — didžiausia klaida. Dėl to terminalo kasdien apiplėšinėjama liaudis. Tačiau niekas dėl to nenubaustas. Lyg nieko nebūtų atsitikę.

Jei tu suklydai, jei apsivogei — būk geras, atsakyk. Tai būtų logiška, bet Lietuvoje to nėra.

Net prie tarybų valdžios tai nebuvo įmanoma. Galų gale, jei kartą sužlugdei tau pavestą darbą, apie kokią karjerą vėl gali eiti kalba?

— Ar yra vilčių, kad situacija keisis, ar galima tą situaciją šalyje pagerinti?

— Velniai žino, kaip ją gerinti. Pirmiausia reikia kalbėti apie švietimą. Informacija ir informatyvumas — štai ko reikia mūsų visuomenei.

— Manote, jog pagrindinės Lietuvos žiniasklaidos priemonės nutyli realius faktus?

— Apie tai aš ir kalbu. Iš esmės, mūsų pagrindiniai leidiniai tapo propagandiniai, jie paklusnūs elitui, formuoja tą elitą ir kažkokia prasme verčia valdžią veikti tam tikra linkme.

Man labiausiai gaila jaunų žmonių, kurie jau mokykloje ruošiasi išvykti iš šalies, emigruoti. Žmonės mokosi todėl, jog nori išvažiuoti, — tai baisu. Padėtis šalyje labai bloga, tačiau mūsų žiniasklaida to neakcentuoja.

— Lietuvos žiniasklaidos propagandinis vaidmuo užima ypatingą vietą. Pagrindiniai naujienų leidiniai persunkti antirusiškos propagandos, jie net klykia šia tema labiau, nei Lietuvos vadovybė.

— Tikrai taip. Esmė tame, kad šią propagandą kontroliuoja žmonės, labai nutolę nuo liaudies. Sakyčiau, juos išugdė tas elitas, kurį dabar jie ir aptarnauja.

— Kaip Jūs vertinate prezidentės Grybauskaitės politiką ir neseniai nuskambėjusius jos pasisakymus, jog Rusija ir Baltarusija — pagrindinės grėsmės Lietuvai ir Vakarams?

— Lietuvos liaudis suklydo, Grybauskaitei suteikdama valdžią. Šalis iš jos nesulaukė nieko gero. Manau, šiandien dauguma lietuvių supranta savo klaidą. Tas pasirinkimas apnuogino visas gilumines mūsų politinio ir visuomeninio gyvenimo problemas.

Žmones su patirtim, su biografija, kurie ne žodžiais, o darbais įrodė, jog moka dirbti savo šalies labui.

Grybauskaitės elgesys užsienio politikoje Lietuvai kenksmingas. Per septynerius prezidentavimo metus mes įgijome per daug priešų, tarp jų ir artimiausios kaimynės — Rusija su Baltarusija. Man labai įdomu, kuo ji vadovaujasi, svaičiodamasi tokiais skambiais pareiškimais.

Neseniai ji pažeminančiai pasisakė apie Baltarusiją. Pasekmė: mūsų pasiuntinys buvo iškviestas į URM, įsivaizduoju, kaip jis raudonavo ir teisinosi dėl neatsargių savo prezidentės žodžių. Tai nenormalu. Reikia ieškoti draugų, o ne priešų, tačiau prezidentė, sprendžiant pagal jos elgesį, taip nemano.

— Tačiau Lietuva turi daug draugų Vakaruose, šalis orientuojasi į ES ir JAV...

— Europos Sąjunga šiandien ant subyrėjimo ribos. Pažiūrėkite, kas dedasi: visuomenė pasimetusi. Briuselyje nepajėgiama įveikti problemų, iškart atsiranda gilėjanti krizė. Ir tai todėl, kad ten sėdi žmonės, nesugebantys priimti sprendimų, tai būrys biurokratų, įpratusių vien tik vadovauti ir dalinti įsakymus. Šiandien iš ES išstoja Didžioji Britanija. Liaudis simpatizuoja euroskeptikams. Situaciją aštrina pabėgėliai.

Neseniai Europos komisija sukurpė bylas prieš Lenkiją, Čekiją ir Vengriją dėl to, kad jos atsisakė priimti migrantus. Tai dar kartą patvirtina, kad ES nesugeba spręsti problemų. Ji tik atstumia nuo savęs šalis. Sprendimas šioms šalims taikyti sankcijas — eilinė vinis į mirštančios ES karstą.

Aš tik viliuosi, kad ši sąjunga subyrės taip pat taikiai ir ramiai, kaip TSRS.

— Ko šiandien labiausiai reikia Lietuvai ir jos žmonėms?

— Tikros draugystės su kaimynais. Po neseniai įvykusio incidento dėl Grybauskaitės pareiškimo apie Baltarusiją šios šalies URM buvo ištarti nuostabūs žodžiai: kaimynus duoda Dievas. To neverta užmiršti, ir kurti abipusius santykius būtina remiantis šiuo faktu. Mes gi vaizduojame gyvenantys lygiagrečioje visatoje.

O žmonėms ir mūsų lyderiams patarčiau galvoti. Pagalvoti ir tik po to kalbėti arba priimti sprendimus. Kas dėl Grybauskaitės, tai čia jau beviltiška. Nuosavas politines ambicijas ji kelia aukščiau savo piliečių interesų. Labai liūdna, kad per septynerius metus ji taip ir neišmoko galvoti bei kontroliuoti savo emocijų.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 17 — id: `scraped:rubaltic_lt:ac293451d63489f5`

**Title:** „Kovokite prieš valdžią!“ — Lietuvos tėvai pradininkai ragina liaudį išeiti į gatves

**Source:** rubaltic_lt (propaganda)

**Text:**

```
„Lietuvos liaudis ant kraštutinumo ribos“. „Taip daugiau negalima gyventi“. „Lietuva tapo totalitarine valstybe“. Tokias mintis paviešino laisvės kovotojai – Nepriklausomybės Akto signatarai ir „Sąjūdžio“ veteranai. Jų manymu, lietuviai vėl turi vienytis po „Sąjūdžio“ vėliavomis kovoje prieš korumpuotą valdžią.

GANA  KENTĖTI

Lietuvoje kyla nauja protestų banga, galinti išjudinti visą šalį. Šį kartą visuomenės pasipriešinimą inicijuoja Antrosios Lietuvos Respublikos pradininkai. Tie patys, kurie beveik prieš 30 metų ragino tautą eiti į aikštes, kovoti prieš „sovietinius okupantus“ bei už teisę gyventi laisvoje ir nepriklausomoje šalyje.

Jų žodžiais, šiandien visa valdžios politika nukreipta prieš eilinius piliečius. „Valdžią šalyje užgrobė oligarchai ir korumpuoti politikai, aptarnaujantys tuos oligarchus“, — teigia protestų iniciatoriai. Lietuva — priklausoma valstybė. Lietuva — mirštanti šalis. Lietuva neturi ateities. Tai pagrindiniai signatarų ir nepriklausomų politikų skambių pareiškimų akcentai.

„Tautos tėvų“ logika visiškai suprantama. Praeito amžiaus pabaigoje jie geraširdiškai tikėjo laisvės idealais, šviesia ir laiminga nepriklausomos Lietuvos ateitimi. Jie ragino liaudį kilti į barikadas, jie gyveno viltimis, ir žmonės jais patikėjo.Tada šimtai tūkstančių lietuvių tapo jų pasekėjais ir išsikovojo teisę būti nepriklausomi.

O tuo tarpu valdžia nuduoda nepastebinti problemų. Ji kalba apie laimėjimus, sugalvoja naujas rinkliavas, varo jaunimą į kariuomenę, parduoda šalį užsienio bankams, smaugia mažojo verslo atstovus ir vidutinę klasę.

Nepriklausomybės Akto kūrėjai, o su jais ir kovos dėl tautinio atgimimo pradininkai, ragina žmones nelaukti išmaldos iš valdžios rankų. Dėl savo teisių reikia patiems kovoti.

NAUJASIS  TOTALITARIZMAS

Pagrindiniai šios naujos „Atgimimo bangos“ šalininkai — Zigmas Vaišvila, Rolandas Paulauskas, Vytautas Radžvilas, Vytautas Čepas ir buvęs prezidentas Rolandas Paksas. Pastarasis atlieka pagrindinį vaidmenį. Būtent jis, neseniai kreipdamasis į tautą, pasakė, kad Lietuva tampa totalitarine valstybe, kurioje nėra vietos žodžio laisvei.

„Ar įmanoma šiandien mūsų šalyje vesti atvirą pokalbį apie politinius sprendimus, kurie yra reikšmingi visuomenei, jei didžioji visuomenės dalis privalo tenkintis pasyvaus stebėtojo vaidmenimi?

Priešingu atveju, pareiškę, jog pilietiškai nepritaria politinei elito linijai, žmonės rizikuoja tapti specialiųjų tarnybų ir kitų teisėtvarkos įstaigų stebėjimo objektais. Jus pastoviai gali persekioti ikiteisminiais tyrimais arba kitomis procedūromis.

Kalbėti apie įstatymo viršenybę, nekaltumo prezumpciją arba prokurorų nepriklausomybę — beviltiškas lošimas kortomis“, — teigia Rolandas Paksas.

TEISĖ  BŪTI  NEPRIKLAUSOMU

Tokios nuomonės prisilaiko ir Zigmas Vaišvila. Prieš 30 metų jis stovėjo prie lietuviškosios nepriklausomybės ištakų ir atgimstančios Respublikos įtvirtinimo. Jis aktyviai kovojo prieš tarybų valdžią, o paskui tapo neparankus saviškiams.

Vaišvila neslepia, jog jis tapo užmirštas. Ir tai padarė konservatoriai — „landsbergininkai“, uzurpuojantys visuomenės nuomonės monopoliją. Jis paverstas liaudies priešu. Praeitais metais Lietuvos specialiosios tarnybos pavadino Vaišvilą žmogumi, keliančiu grėsmę nacionaliniam saugumui dėl jo aštrių pasisakymų „komunistės“ Dalios Grybauskaitės atžvilgiu, raginimų bendradarbiauti su Rusija ir prieštaravimo valdžios sprendimams dislokuoti NATO karines pajėgas.

„Valdžia — ne valstybė. Jeigu anksčiau galėjome kritikuoti valdžią, tai šiandien jau negalime? Dėl to tu tampi Lietuvos valstybės priešu. Nesąmonė! Kodėl, pavyzdžiui, Suomijos užsienio reikalų ministras turi teisę pareikšti, kad Suomija saugi todėl, kad ten nėra NATO bazių?

O Lietuvos URM vadovas Linas Linkevičius tokios teisės neturi. Jis kalba antraip ir be jokių argumentų. Tai tikra propaganda. Jis su prezidente Dalia Grybauskaite savo karingais pareiškimais varo Lietuvą pavojingon padėtin. Kodėl aš šia tema negaliu išsakyti savo nuomonės?

NATO bataliono dislokavimas Lietuvoje — provokacinis veiksmas. Tai siekis „pasirodyti“, pademonstruoti nerealią jėgą, kurios kaina — vienas šūvis. Menas išvengti karo mūsų elitui nesuvokiamas“, — pasakė savo interviu vienas iš Lietuvos tėvų  pradininkų.

Paradoksas tame, kad Zigmas Vaišvila buvo vienas iš Lietuvos specialiųjų tarnybų ir saugumo organų kūrėjų. 1991–1992 metais jis vadovavo Valstybės saugumo departamentui. Likimo ironija: praėjus trims dešimtmečiams, jo sukurtos tarnybos ir jo išauklėti agentai medžioja jį patį.

PO  29  METŲ

Tėvai  pradininkai ir atnaujinto „Sąjūdžio“ nariai ragina tautą eiti į gatves. Kol kas protestuojama visiškai taikiai. Protestuotojai nori su valdžios atstovais dialogo ir išgirsti atsakymus, tačiau pastarieji neskuba diskutuoti.

Šio pasipriešinimo dalyvių judėjimo veiklos pradžia jau akivaizdi. Gegužės pabaigoje „nepatenkintieji“ pirmą kartą po 29 metų išėjo į gatves. Anuomet jie ėjo protestuoti prieš tarybų valdžią ir reiškė lietuvių norą atkurti nepriklausomą valstybę, o šiandien jiems tenka kovoti prieš laisvos Lietuvos valdžios atstovus.

Organizacija atsiuntė į sostinę savo atstovus iš įvairių miestų, kad būtų pareikšta, jog jų netenkina dabartinė padėtis šalyje ir vyriausybės veiksmai. Taip šių metų gegužę buvo pradėta pastovi akcija „Atgimimo banga“, kurios pagrindinis tikslas, kaip ir prieš daugelį metų, — išvesti į gatves visuomenę ir kita linkme nukreipti šalies politiką.

Oficialiame visuomeninio judėjimo pareiškime sakoma: atnaujintas „Sąjūdis“ kviečia kovotojus už laisvę, inteligentiją, kaimo žmones, jaunimą, dvasininkus, profsąjungų aktyvistus ir visus, kuriems rūpi Lietuvos likimas, visuomeniškai diskutuoti.

Kaip buvo pasakyta RuBaltic.Ru korespondentui organizacijos Vilniaus skyriuje, „deja, lietuvių tautos sąžinės ir garbės neparėmė nei Seimo nariai, nei plačioji visuomenė, tačiau tai tik veiklos pradžia. Kad valdžia mus parems, nelabai tikimės, bet žmonės, kaip ir anksčiau, bus su mumis“.

KREIPIMASIS  Į  PREZIDENTĘ

„Sąjūdiečiai“ nori būti išgirsti. Jie pasirengę dialogui su valdžia. Jų tikslas — organizuoti plačią diskusiją skausmingiausiais klausimais. Lietuvos intelektualų vadovas — „Sąjūdžio“ lyderis filosofas ir profesorius Vytautas Radžvilas net pasiuntė oficialų kreipimąsi prezidentei Daliai Grybauskaitei. Jame jis reikalauja keisti Lietuvos ekonominės ir socialinės politikos vektorių, nes šiandien labiausiai kenčia eiliniai piliečiai.

Pats Vytautas Radžvilas pabrėžia, jog apie šį kreipimąsi mažai kas žino, nes žiniasklaida šio dokumento egzistavimą arba visiškai nutyli, arba pateikia tik ištraukas.

„Nors kai kurios žiniasklaidos priemonės ir paminėjo kreipimąsi, tačiau bendrai oligarchų valdoma spauda stengiasi nutylėti šį faktą arba sumenkinti jo reikšmę“, — sako profesorius Radžvilas.

Jis nepuola neviltin ir primena, jog informatorių tinklas savo laiku pradėjo pralaužti Lietuvos TSR informacinę blokadą ir cenzūrą, ir tikisi, jog panašus tinklas pramuš ir šių dienų informacinę blokadą.

SKAUDŪS  SKAIČIAI

Naujos „Atgimimo bangos“ aktyvistai ragina liaudį pabusti ir suprasti, kad pokyčiai šalyje galimi tik tuo atveju, jei žmonės nepabijos susivienyti ir atvirai išreikšti savo nepasitenkinimą. Valdantieji imsis ką nors veikti tik tuomet, kai pajus pavojų. Iki tol pokyčiai neįmanomi.

„Valdžion patekusios politinės partijos net nesusimąsto, kas pas mus dedasi... Žmonės bėga iš Lietuvos ne todėl, kad nėra darbo. Bėga nuo socialinės nelygybės, nuo žemo gyvenimo lygio, nuo valdžioje sėdinčių abejingumo jų atžvilgiu“, — teigia vienas iš „Sąjūdžio“ pradininkų Vytautas Čepas.

Kaip buvo skelbta anksčiau, pagrindinė Lietuvos gyventojų masiškos emigracijos priežastis — nedarbas ir menki atlyginimai. 2016 metais išvykimą iš šalies deklaravo 51 tūkst. žmonių — 6,4 tūkst. (14,5 proc.) daugiau, nei 2015 metais. Šių metų pradžioje Lietuvoje pastoviai gyveno 2 mln.849 tūkst. žmonių — tai 39,2 tūkst. (1,4 proc.) mažiau, nei prieš metus.

O tuo metu JT Ekonomikos ir socialinių klausimų departamentas prognozuoja, kad Lietuvos gyventojų išvykimo greitį 2017 metais sudarys 125 žmonės per dieną.

Paskutinieji Eurostato duomenys apie situaciją Lietuvoje liudija: 29 proc. gyventojų atsidūrė ant skurdo ribos — ir padėtis šalyje nesikeičia jau aštuoneri metai. Ir tuo metu Lietuva stabiliai laikosi tarp ES rekordininkių pagal skurdžius atlyginimus gaunančių darbuotojų skaičių.

Nepaisant to, kad minimalus atlyginimas jau pasiekė 380 eurų, jis yra vienas iš mažiausių Europoje, o tuo metu kainos auga sparčiau, nei atlyginimai. Visuomenės nuomonės apklausos rodo: 59 proc. lietuvių teigia, jog gyvenimo lygis šalyje nuolat blogėja.

Valdžia skelbia ekonomikos pasiekimus, tai kasmet argumentuodama BVP augimu. Tačiau kvalifikuoti ekonomistai ir analitikai prognozuoja Lietuvos ekonomikos griūtį. Neseniai apie tai atvirai pareiškė pats Centrinio banko vadovo pavaduotojas Raimondas Kuodys. Jo žodžiais, ekonomika atsidūrė agonijos stadijoje, o BVP augimas neatspindi realių tendencijų.

Atsižvelgdamas į masišką emigraciją, žemą gimstamumą ir regionų tuštėjimą, jis prognozuoja šalies išmirimą. Po 20-30 metų Lietuvoje liks tik trys miestai: Vilnius, Kaunas, dalinai Klaipėda. Didžioji Lietuvos teritorijų dalis taps dykviete be žmonių.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 18 — id: `scraped:rubaltic_lt:511f2dd3cf7f3f25`

**Title:** Žvilgsnis iš JAV: „Mūsų Lietuvą pavertė pikta pamote“

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Gegužės pabaigoje su kelių dienų pertrauka Vilniuje praėjo du Rusijos opozicijos forumai. Putino režimo kritikai diagnozę Rusijai labiau linkę nustatyti užsienyje, šiuo atveju Lietuvoje. Bet kaip atrodo pati Lietuva, žvelgiant į ją iš tolių? Apie tai, kaip klostosi reikalai Pabaltijo respublikoje, analitinis portalas RuBaltic.Ru pakalbėjo su Lietuvos disidentu JAV, publicistu Valdu Anelausku.

— Pone Anelauskai, jei leisite, norėtųsi pradėti pokalbį nuo Jūsų biografijos: kaip Jūs atsidūrėte JAV?

— JAV atsidūriau dar TSRS laikais. Mes čia atvykome 1988 metais. Vyko pertvarka. Į rytus jau nesiuntė, siuntė į vakarus. Tokia buvo valdžios taktika, o VSK rūpėjo atsikratyti tokiais, kaip aš. „Jeigu norite, važiuokite, jūs gi visuomet norėjote išvykti į Vakarus“. Išvažiavome. Viskas labai paprasta.

O aš tuomet su „Laisvės radiju“ bendradarbiavau. Buvo toks „atviras“ rusakalbis „Laisvės radijo“ redakcijos darbuotojas. Latvijoje buvo Miša Bombinas, ir jis man pasiūlė, kai aš į Rygą nuvažiavau. Galiu supažindinti su visais, sako. Savikas Šusteris dar ten buvo, kuris dabar Ukrainoje, jis juk vilnietis. Per jį ir pradėjau „Laisvėje“ dirbti.

Paskui atsidūriau Amerikoje. Visi keliai tada į Ameriką vedė. Niujorke padirbėjau tame pačiame radijuje.Ten jie jau pradėjo apgaudinėti, nemokėti. O paskui ir Tarybų Sąjunga sugriuvo. Tokia banali istorija.

— Ar Jūs jautėte, kad TSRS „baigiasi“? „Sąjūdžio“ įsigalėjimas, Wind of Change, kažko naujo laukimas — ar nesinorėjo likti?

— Mane jau tada kamavo nuojauta, kad visa tai, ta „dainuojanti revoliucija“ baigsis blogai.

— Sakoma, jog tai, kas didinga, geriau matoma iš toli. Lietuva — nedidelė respublika, tačiau per ketvirtį amžiaus joje vykę transformaciniai procesai didžiuliai. Kokia Jums atrodo šių dienų Lietuvos Respublika žvelgiant iš užjūrio?

— Viename savo straipsnyje rašiau: jeigu aš būčiau pabudęs po komos būklės ir perskaitęs, kas dedasi Lietuvoje, nebūčiau patikėjęs. Tai, kas atsitiko su Lietuva, — protu nesuvokiama. Tai katastrofa, genocidas.

Nuverstas prezidentas Rolandas Paksas prieš keletą mėnesių pasakė, kad blogiau, negu dabar, Lietuvoje dar nebuvo per visą jos tūkstantmečio istoriją.

Mano amžinąjį atilsį tėvas kartą pasakė man tą patį: „Niekas ir niekada taip nesityčiojo iš lietuvių Lietuvoje, kaip dabar“. O juk jis dešimt savo jaunystės metų praleido Sibiro tremtyje ir lageryje. Buvo nuteistas mirties bausme, vėliau nuosprendį pakeitė 25 metais lageryje, iš kurių beveik dešimt jame išbuvo. Tą patį sakė ir mano a.a dėdė, taip pat buvęs tremtinys, — kad jeigu lyginti su gyvenimu dabartinėje Lietuvoje, tai ir tremtis neatrodo labai bloga.

Man sunku įsivaizduoti didesnį lietuvių tautos priešą nei dabartinė panelė prezidentė dalia Grybauskaitė, kuri kadaise buvo karinga komunistė, o dabar tapo tokia pat aršia globaliste, pagrindine naujos pasaulio tvarkos Lietuvoje agente. Kaip Leninas kadaise pavadino rašytoją Levą Tolstojų „rusų revoliucijos veidrodžiu“, taip aš „Raudonąją Dalią“ galėčiau drąsiai pavadinti dabartinės betvarkės šalyje veidrodžiu.

Tai juk jie pavertė motiną Tėvynę pikta pamote, nuo kurios tūkstančiai lietuvių priversti bėgti lyg nuo karo arba maro.

— Ar Jūs bendraujate JAV su tėvynainiais, su senosios emigracijos atstovais? Kokios nuotaikos šių dienų Lietuvos atžvilgiu tarp jų vyrauja?

— Nebendrauju. O priežastys geografinės. Tame mieste, kuriame gyvenu, lietuvių beveik nėra. Ir rusų mažai. Beje, yra šiek tiek emigrantų iš Lietuvos, bendrauju skaipu, telefonu, laiškais.

Turiu keletą pažįstamų — aktyvių, teisingai mąstančių. Buvo Čikagoje lietuviškas laikraštis — jis, tiesa, bankrutavo. Aš jiems rašiau straipsnių ciklą. Jie tada jau buvo prie bankroto ribos, bijau, kad padėjau jiems bankrutuoti.

Ten tokia jauna mergina dirbo, žurnalistė, labai drąsi. Mes viską išspausdinsim, sakė, tik rašyk. Na, aš ir parašiau jiems 3–4 straipsnius apie rusofobiją. Su malonumu parašiau. Ir tada prasidėjo gąsdinimai ir kaltinimai: „Kaip jūs galite visa tai spausdinti?“ Tada laikraštis ir užsibaigė.

O šiaip, kai buvo atvykusi mūsų Grybauskaitė — Čikagoje NATO šalių vadovai rinkosi 2012 metais, — ji panoro susitikti su čia gyvenusiais lietuviais. Pasveikinti prezidentės atėjo pokario emigrantai, o dabartiniai emigrantai apmėtė ją prašvinkusiais kiaušiniais. Bėgo nuo tokio susitikimo per kažkokias šiukšlių dėžes, paskui skundėsi amerikiečių valdžioms, kad ją prastai nuo savų lietuvių gynė. Taip kad lietuviai čia nevienodi.

— Potarybinės nepriklausomybės aušroje „Sąjūdžio“ funkcionieriai žadėjo sukurti Lietuvoje demokratiją. Ar pavyko?

— Sukūrė dvokiančią demokratiją. Dabar jau atvirai rašo, kad nieko neišėjo. Ir taip kalba net tie, kurie žadėjo, - tas pats Audrius Butkevičius, „spalvotųjų revoliucijų“ specialistas. Jis gi tada buvo vienas iš svarbiausių. O dabar, nepaisant jo veiklos Ukrainoje, Gruzijoje, Kirgizijoje, pačioje Lietuvoje atsidūrė opozicijoje, kalėjime sėdėjo.

Demokratija? Kokia ten demokratija. Štai dabar Lietuvoje teisiamas vienas pagrindinių disidentų — Žilvinas Razminas. Nepriklausomybės akto signatarai Rolandas Paulauskas, Zigmas Vaišvila dabar taip pat disidentai. Vaišvila, pats kūręs ir pirmasis vadovavęs Lietuvos valstybės saugumo departamentui, dabar jų pačių persekiojamas, kasmet apie jį rašoma ataskaitose.

— Ironiška...

— Viskas blogiau, nei VSK laikais. Tada buvo galima skųstis, esą „okupantai“. O dabar ant ko versti kaltę? Tačiau tie, kurie proto neprarado, supranta: dabar ji, tikroji okupacija.

Dabar kaltinti nėra ką, vien tik save.

— Istorinis Rytų Europos komponentas Pabaltijo šalyse turi didžiulę reikšmę aktualiame politiniame procese. Naujas požiūris į netolimą ginčytiną praeitį tampa religija, alternatyvi interpretacija uždrausta. „Neteisingos“ istorinės laidos tampa televizijos kanalų blokavimo priežastimis, „nelojalūs“ ekspertai praranda galimybę išvykti, uždraudžiama neparanki literatūra. Ryškus pavyzdys — Galinos Sapožnikovos knygų konfiskavimas. Į Lietuvą sugrįžo tarybinė cenzūra?

— Aš pamenu tarybinę cenzūrą. Buvo logika. Štai komunistai, štai disidentai. Jie gali išjudinti komunizmą, ideologiją. O Lietuvoje ir Pabaltijyje dabar juk nėra ideologijos. Nei komunizmo, nei liberalizmo. Vienintelė „ideologija“ — „Rusija — priešas, Rusija užpuls“. Jei nebūtų Rusijos, ją reikėtų sugalvoti. Ką be jos „landsbergininkai“ darytų? Juk ir buvęs Estijos prezidentas (Toomas Chendrik Ulves — RuBaltic.Ru pastaba) sakė: jei ne Rusija, mes būtumėm mažoji Šveicarija.

Mūsų Lietuva: kur nenuvyktų prezidentas ir ministrai, viena, ką jie sugeba pasakyti, kokia bloga Rusija. O jei Rusijos nebūtų, ką jie galėtų pasakyti? Kad Lietuva pasaulyje pirmauja gerdama degtinę, emigruodama, kad muša rekordus savižudybėse? Pasigirti galima, bet vargu ar už tai pagirs.

Taip kad jei pajudinti šiuos bokštus, ant kurių laikosi taip vadinamoji dabartinė valstybė, teks rėkti. Dėl to ir cenzūra, todėl jie, įsikandę, ir laikosi „Sausio 13-osios mito“.

Jeigu jau draudžia apie tai kalbėti, draudžia alternatyvias nuomones, inicijuoja teisinę atsakomybę, mąstančiam žmogui kyla įtarimas: „Ten kažkas ne taip“.

Knygą išleido... na, gal 500 egzempliorių. Niekas jos negavo, neskaitė.

— Kol lietuviai jos neišreklamavo.

— Žinoma. Dabar skaito. Aš pats internete susiradau.

Ir būtent tie funkcionieriai, kurie per 25 metus savo mažą šalį pavertė klaikia vieta, kažką ir nuveikė Sausio 13-ąją. Ir net jei „savi šaudė į savus“, kaip sakė Paleckis, „smulkmena“, pažvelgus į tai, ką tie „savi“, tie „landsbergininkai“ padarė vėliau. Kiek žmogžudysčių, kiek išvažiavusių...

— „Kas ką išdavė“ — taip vadinasi Sapožnikovos knyga, apie kurią mes jau kalbėjome. Kaip Jūs pats atsakote į šį klausimą, stebėdamas 25-erių metų potarybinės Lietuvos vystymąsi iš už vandenyno?

— Kaip rašiau savo straipsnyje po to, kas nutiko su šia knyga, aš užimu neutralią poziciją. Aš Sausio 13 dieną Lietuvoje negyvenau, gyvenau Nju Džersi valstijoje, Amerikoje. Čia tuo įvykiu mažai kas domėjosi, tuo metu vyko karas Irake.

Bet visa tai, kas nutiko po Sausio 13-osios, kaip aš jau sakiau, — tai jau ne išdavystė, tai galima pavadinti genocidu, katastrofa.

Gercenas klausė: „Kas kaltas?“ Tie, kurie laimėjo, — „landsbergininkai“. Jie ne tik išdavė savo liaudį, savo tėvynę, jie ją sunaikino. Per 25 metus — būtent sunaikino. Ir jei tai tęsis, o tai, žinoma, tęsis, — tai baisu.

Čia aš sutinku su prezidentu Putinu: TSRS griūtis — didžiausia XX amžiaus geopolitinė katastrofa. Sakyčiau, ne tik XX amžiaus, tai didesnio laikotarpio katastrofa. Paprasčiausias palyginimas: jei kas buvo blogai, o paskui pasidarė dar blogiau, tai „blogai“ jau neatrodo taip blogai. Tarybų Sąjunga nebuvo geriausias gyvenimo variantas, todėl aš ir išvykau, bet jeigu lyginti su tuo, kas dabar dedasi Lietuvoje... Žmonės apie tai kalba, rašo, ir tai net ne nostalgija.

Antai samprotaujama, kad Pabaltijo gyventojai jaučia nostalgiją tarybinei praeičiai. O propaganda sako: „Jie patys jauni buvo ir ilgisi ne TSRS, o vien tik savo jaunystės“. Ir aš net sutinku su tuo. Bet iš kitos pusės, dabar iš ten bėga jaunimas, kuris tarybų valdžios laikais dar nebuvo gimęs.

— Leiskite užbaigti naivokai romantišku klausimu. Pono Anelausko projektas „Lietuva“? Kokia turi būti ši šalis? Kaip sulaukti permainų gerąja linkme?

— Kažką pakeisti, turbūt, per vėlu. Ten jau taip viskas sugriauta, taip užkrėsta. Suprantama, aš norėjau nepriklausomybės, aš ir dabar už nepriklausomybę. Bet kuri valstybė turi būti nepriklausoma. Turėti gerus santykius su kaimynais. Kaip buvo sakoma, „tiltas tarp Rytų ir Vakarų“. Iš vienos pusės Rusija, iš kitos — Europa. Idealus modelis.

O kokia turėtų būti Lietuva, net nežinau. Sunku pasakyti. Didžiausia kliūtis, siekiant permainų, — Europos sąjunga. Tačiau permainų Pabaltijyje ir Rytų Europoje nebus be permainų Amerikoje. Daug ko buvo tikėtasi iš Trampo, tačiau kolkas jam neduodama ką nors nuveikti. Nuo pačių Lietuvos, Latvijos, Estijos ir net Lenkijos mažai kas priklauso. Tačiau jei visa tai tęsis – net nenoriu kalbėti...

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 19 — id: `scraped:rubaltic_lt:cb4719df13cb2d73`

**Title:** Pabaltijis miršta, nes valdžioms nerūpi žmonių rūpesčiai

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Pabaltijis muša savo rekordus: pirmojo šių metų ketvirčio metu iš Lietuvos išvyko dvigubai daugiau gyventojų, nei pernai, o Latvijoje demografai prognozuoja latvių išnykimą po šimto metų. Trečdalis Pabaltijo šalių gyventojų ruošiasi emigruoti, liekantieji sensta, emigracija — daugumos jaunų žmonių strategija, o Eurostatas koreguoja savo prognozes pagal Pabaltijo išmirimo tempus augimo kryptimi. Pabaltijo šalių vadovai džiaugiasi, jog auga BVP, ir vadina savo šalis vienomis iš labiausiai išsivysčiusių pasaulyje, nenorėdami žinoti baisių statistikos duomenų. Pabaltijo valstybėms nusispjaut, kuo gyvena žmonės, ir šie joms atsako tuo pačiu, atsisakydami gyventi savo šalyse ir jas ginti.

Buvęs Latvijos prezidentas Valdis Zatlers laiko savo šalį viena iš labiausiai išsivysčiusių pasaulyje. Neseniai duodamas interviu Zatlers nesidrovėdamas pareiškė, kad ir jis įnešė indėlį į didžiulę šalies sėkmę bei klestėjimą.

„Aš didžiuojuos savo šalimi ir tuo, ką nuveikė jos žmonės per pastaruosius dvidešimt šešerius metus. Ne tik atkūriau Latviją, bet ir pasiekiau, jog ji tapo viena iš labiausiai išsivysčiusių pasaulio šalių. Žinoma, buvo galima pasiekti dar daugiau. Ir labai svarbu, kad neįvėlėme strateginių klaidų. Aš dažnai vardinu svarbius strateginius sprendimus — strateginių klaidų nebuvo!“ — gėrisi savimi ir bendražygiais buvęs prezidentas interviu „Latvijos radijui–4“.

Per pastaruosius penkerius metus Latvija prarado mirusiais ir išvykusiais 92 tūkstančius žmonių — 5 proc. gyventojų, o per ketvirtį amžiaus gyvenimo „ be strateginių klaidų“ šalis prarado kas trečią gyventoją. „Remiantis šiais duomenimis, galima prognozuoti, jog egzistuoti mums liko apie šimtą metų, — teigia Rygos tarptautinės migracijos organizacijos biuro demografas Ilmar Mežs. — Gimstamumo lygis buvo mažesnis nei mirtingumo visus pastaruosius dvidešimt penkerius metus, nuo tada, kai Latvija tapo nepriklausoma. Praeitais metais mirė žmonių septyniais tūkstančiais daugiau, nei gimė. Be to, apie 10 tūkstančių gyventojų emigravo“.

Kitas vietinis demografas, Latvijos universiteto profesorius akademikas Peteris Zvidrinš rašo, kad su šalimi kasdien atsisveikina 55 žmonės. Kas mėnesį Latvija praranda dviejų nedidelių miestų gyventojų skaičių.

Katastrofiška depopuliacija veda šalį prie socialinės krizės: Latvijoje nelieka gyvybingai svarbių šakų specialistų. Paskutinė naujiena: stambiausių Latvijos ligoninių medicinos personalas kreipėsi į vyriausybę prašydamas pagalbos — chirurgai pasitraukia iš darbo dėl menkų atlyginimų, uždarytos operacinės, nėra specialistų, sugebančių operuoti vidaus organus ir skydliaukę.

„Latvijoje kasdien miršta kūdikiai ir jaunos motinos, — neseniai pareiškė sveikatos apsaugos ministrė Anda Čakša. — Tai įvyksta todėl, kad atskiros mažos ligoninės nepajėgios apsirūpinti reikalingu kvalifikuotų specialistų skaičiumi. Žmonės miršta arba po operacijų patiria negalavimus todėl, kad juos operuoja patirties stokojantys chirurgai“.

Akivaizdi situacija be išeities. Specialistai išvyksta. Latvijoje pavojinga gimdyti vaikus: nėra kas priimtų gimdymus, nėra kas stebėtų kūdikį pirmaisiais jo gyvenimo metais. Mokyklos ir vaikų darželiai uždaromi, valstybės finansinės paramos nesulauksi, gero ir deramai apmokamo darbo nėra arba jis pasiekiamas tik dėka „blato“. Nenuostabu, kad tie žmonės, kurie lieka, nepageidauja turėti vaikų. Šalis pamažu miršta.

Tačiau tokia nykstanti Latvija neegzistuoja saulėtame politikų pasaulyje. Jokie baisūs šalies gyvenimo faktai nemažina jų džiūgaujančio optimizmo. Tačiau grįžkime prie buvusio prezidento Zatlers. „Bet juk žmonės išvyksta ir vėl sugrįžta. Klystame sakydami, kad po dešimties metų mes būsime tokie pat, kaip prieš dvidešimt metų. Pavyzdžiui, gyventi kaime ir niekur iš jo neišvykti. Mes gyvename atvirame ir laisvame pasaulyje, kuriame migracija — natūrali ateitis“, — mano buvęs Latvijos valstybės vadovas.

Kai buvęs lyderis lygina Latviją su kaimu, skamba gana įdomiai, tačiau po tokio emigracijos priežasčių aiškinimo vertėtų padidinti eks prezidentui apsauginių skaičių. Tų latvių, kurie Europoje pluša juodžiausiuose darbuose, giminės už kalbas apie tai, kad jų artimieji išvyko iš Latvijos paspoksoti į pasaulį ir išgerti Paryžiuje ypatingo skonio kavos, o dar ir pasigrožėti Eifelio bokštu, gali palikti daktarą Zatlers be dantų.

Lietuvos Sociologijos instituto Socialinių tyrimų centro tyrimų, kurie buvo atlikti Lietuvos Seimo Nacionalinio saugumo ir gynybos komiteto užsakymu, duomenimis, pusė gyventojų agresijos atveju tuoj pat pabėgs iš šalies. Ketvirtadalis gyventojų pasiliks tikslu užtikrinti saugumą savo šeimos nariams.

Tik 20 proc. apklaustųjų pareiškė, kad Lietuvą gins su ginklu rankose. Absoliuti gyventojų dauguma jos negins. O dėl ko jie turėtų ginti Lietuvos valstybę? Dėl to, kad dešimtmečiais vertė be darbo likusias „nereikalingas burnas“ emigruoti? Dėl ketvirtį amžiaus kabintų makaronų, kad bus gyvenama kaip Skandinavijoje, o iš tikrųjų lietuviai gyvena blogiau nei baltarusiai? Dėl siekių „demokratizuoti“ svetimą posttarybinę erdvę visiškai ignoruojant socialinę politiką ir nenorint matyti realios padėties savo šalyje? Dėl sugriautų uosto, geležinkelio, atominės elektrinės, fabrikų ir gamyklų, žvejybinio ir prekybos laivynų vardan „europietiško pasirinkimo“? Dėl visiškos politikų ir valdininkų korupcijos? O gal dėl dėdulės Landsbergio ir agentės „Magnolijos“-Grybauskaitės?

Pats gyvenimas patvirtina Lietuvos sociologų tyrimų teisingumą. Po to, kai buvo pradėta klykti apie „artėjančią rusų agresiją“ ir 2015 metais sugrąžinta visuotina karinė prievolė, emigracija iš Lietuvos ženkliai padidėjo ir ėmė mušti pasaulinius rekordus. Muša jau treti metai.

Šiais metais bėgimas iš respublikos ūgtelėjo beveik du kartus. Jei praeitų metų pirmojo ketvirčio eigoje išvyko 9823 žmonės, tai tokiu pat 2017 metų laikotarpiu — 18550 žmonių. Nuo 1991 metų iš Lietuvos vien tik oficialiais duomenimis išvyko ne mažiau 700 tūkstančių gyventojų; o atsižvelgiant į tai, kad ne visi lietuviai registruoja savo išvyką, realūs emigracijos skaičiai gali viršyti milijoną. Demografas Vidmantas Daugirdas lygina emigracijos sukeltą demografinę krizę su bado, karo ir epidemijos pasekmėmis.

Pasak šį pavasarį patikslintos prognozės, 2050 metais Lietuvoje liks 2 milijonai žmonių, o 2080-aisiais — 1650 tūkstančių gyventojų. Tokiu būdu, šimtąsias savo „antrosios nepriklausomybės“ metines Lietuvos Respublika švęs iš 3,5 milijono žmonių, kuriuos turėjo 1991 metais, praradusi 2 milijonus. Ir tuomet taps senelių namais, nes žmonės, perkopę 60 metų ribą, sudarys 85 proc. šalies gyventojų.

Jau dabar 65 metų ir vyresnių Lietuvos gyventojų skaičius sudaro 19 proc. (549 tūkst. žmonių). Senatvės koeficientas nuo 2001 metų išaugo 1,8 karto. O tuo metu, kai Skandinavijos šalyse, į kurias lygiuojasi Lietuva ir kurių gretose save mato, vyksta teigiama kartų kaita (norma tapo trečias vaikas šeimoje), mirtingumas Lietuvoje lenkia gimstamumą, o vaikai apsireiškia daugiausia sezono metu — vasarą, kai tėvai juos atveža iš užsienio pagloboti močiutėms ir seneliams.

Realios Lietuva ir Latvija jau atsidūrė ant socialinės griūties slenksčio. Tačiau išgalvotosios Pabaltijo šalys, kurių įvaizdį sukūrė vietinės valdžios, priklauso „labiausiai išsivysčiusioms pasaulio valstybėms“. Jos laimingos ir klestinčios.

Auga BVP vienam gyventojui (kaip neaugs, jei gyventojų skaičius vis mažėja, o eurofondų dotacijos, skirtos infrastruktūros vystymuisi, nekinta), gerėja pagrindiniai makroekonomikos rodikliai, mažėja nedarbo lygis (kaip nemažės, jei bedarbiai skuodžia į užsienį), didėja vakarietiškų kolegų teigiamų atsiliepimų apie ekonominį Pabaltijo vyriausybių drausmingumą skaičius.

Jos spjauna ir savo šalių, ir jose gyvenančių žmonių link.

Todėl Pabaltijis ir miršta — gyventojai savo vyriausybėms atsilygina tuo pačiu: taip pat spjauna savo šalių link, su lagaminais rankose skuodžia į aerouostus šaukdami „Gelbėkitės, kas gali!“

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 20 — id: `scraped:rubaltic_lt:7b600e35b45c62fd`

**Title:** Dauguma lietuvių neketina ginti nuo agresorių „supuvusios sistemos“

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Šiomis dienomis Lietuvos Seime buvo paskelbti duomenys tyrimų, skirtų skausmingiausiai lietuvių valdžios temai – piliečių pozicijai rusų grėsmės atžvilgiu. Tyrimas buvo atliktas Seimo Nacionalinio saugumo ir gynybos komiteto užsakymu. Rezultatas stulbinantis: dauguma lietuvių pareiškė, kad išorinio įsiveržimo atveju jie negins dabartinės valdžios.

Tyrimo duomenimis, tik penktadalis apklaustųjų pasiruošęs ginti Lietuvos sienas su ginklais rankose. Ši formuluotė reiškia pasiruošimą prisijungti prie karinių pajėgų ir saugos struktūrų. Kitaip sakant, ginti valdžios ir šalies vadovybės planuoja apie 20 proc. visų piliečių (pajėgių gintis su ginklais rankose).

Pagrindiniu tyrimo tikslu autoriai laikė „piliečių utėlėtumo“ patikrinimą. Labiausiai juos jaudino, ar nebėgs iš skęstančio laivo sąžiningi piliečiai, ar nedums svetur iš tėviškėlės.

Ketvirtadalis apklaustųjų pareiškė, jog iškilus užpuolimo grėsmei jie liktų Lietuvoje, tačiau faktiškai tik tikslu užtikrinti savo šeimos saugumą. Kitaip sakant, 50 proc. lietuvių pasiruošę pasipriešinti užpuolikui buitiniame lygyje, tačiau tik tuo atveju, jei iškils pavojus jų giminėms ir artimiesiems. Apie valstybės santvarkos ir valdžios struktūrų gynimą kalbos nėra.

Verta pažymėti, kad valdžia ir vyriausybei palanki spauda sėkmingai nutylėjo faktą, jog tyrimas neįmantriu akademiniu pavadinimu „Subjektyvus saugumas besikeičiančiame geopolitiniame kontekste: faktorius ir individualias strategijas formuojantys ypatumai“ buvo atliekamas pastarųjų dvejų metų eigoje. Ir kad jis būtų atliktas, tam teko skirti 104 tūkstančius eurų.

Tyrimą atliko Lietuvos socialinių tyrimų centro Sociologijos instituto darbuotojai. Vienintele ir visa apimančia rėmėja pasireiškė valstybės biudžeto finansuojama Lietuvos mokslinė taryba.

Kitaip sakant, už keletą dešimčių puslapių eilinių gąsdinimų „nedraugiškos Rusijos“ kėslais sumokėjo Lietuvos mokesčių mokėtojai. Iš jų kišenių buvo išpešta 104 tūkstančiai eurų. Tačiau tyrimas dar neužbaigtas. Numatyta jį tobulinti kelerių metų eigoje.

Seimo kareiva

Tyrinėtojų kuratoriaus vaidmenį atliko Seimo narys ir Nacionalinio saugumo ir gynybos komiteto pirmininkas Vytautas Bakas. Būtent jis ir pateikė šio mokslinio darbo rezultatus. Kalbėdamas apie galimą grėsmę, jis leido sau „pažaisti“ faktais ir terminais. Deputatas pareiškė, kad įsiveržimo į Lietuvą grėsmę jis mato, žinoma, tik iš Rusijos pusės.

„Padėtis regionalinio saugumo sferoje vis dar įtempta. Rusija lieka didžiausiu iššūkiu regiono ir euroatlantinės bendrijos saugumui, o jos agresyvumas ir karinis aktyvumas prie NATO sienų padidėjo. Mes turime kovoti su informacinėmis atakomis, kibernetiniu Rusijos šnipinėjimu ir galimais išpuoliais prieš Lietuvos informacines sistemas, nes tai labai kenkia nacionaliniams šalies saugumo interesams“,— taip jis pareiškė pokalbio su JAV pasiuntine Ana Chol metu.

Pataikė į tašką

Tyrime pabrėžiama, kad norą ginti savo šalį dažniausiai pareiškia jauni piliečiai, turintys gerą pajamų lygį. Jie patenkinti savo gyvenimu ir pritaria Lietuvos vadovybės pozicijai „demokratinių vertybių“ ir „agresyvios Rusijos“ politikai pasipriešinimo klausimais. Tačiau tokių gyventojų Lietuvoje labai nedaug.

O tuo metu situacija kasmet blogėja. Nepaisant valdžios džiūgavimų ekonominiais pasiekimais, žmonėms vis sunkiau ir sunkiau gyventi.

Pastaraisiais metais militarizavimas ir „žaidimai karu“ tapo valdžiai viliojančia idėja. 2015 metais šalyje buvo atnaujintas šaukimas kariuomenėn penkeriems metams. 2016 metais prezidentė Dalia Grybauskaitė pasirašė įstatymą dėl visuotinos karinės prievolės – tai numatyta vykdyti pastoviai. Iki 2018 metų Lietuva įsipareigojo padidinti karines išlaidas iki 2 proc. BVP – vieno milijardo eurų. 2020 metais šias išlaidas planuojama padidinti iki 2,5 proc. BVP.

Patys to nesitikėdami, tyrinėtojai sociologai ir Seimo kareivos pripažino, kad dauguma piliečių nepriklauso kategorijai pasiturinčių, aprūpintų ir situacija šalyje patenkintų žmonių.

Būtent tai ir sąlygoja patriotiškumo lygį – meilę savo Tėvynei. Pasirengimas ginti savo šalį ir nusistovėjusią sistemą, kuri vis labiau priešpastato save eilinių piliečių interesams, priklauso nuo jų gyvenimo kokybės. Kol šalies vadovybė nesuvoks šios elementarios tiesos, Lietuvos saugumo nepajėgs užtikrinti net patys rimčiausi tyrimai.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```
