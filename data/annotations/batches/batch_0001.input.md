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

### Article 1 — id: `scraped:rubaltic_lt:f829915ce4fb0020`

**Title:** Sąjungininkų „padėka“ Lietuvai: Ukrainoje grasina susprogdinti Baltarusijos AE Sąjungininkų „padėka“ Lietuvai: Ukrainoje grasina susprogdinti Baltarusijos AE

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Jie nors vienas Baltarusijos kariškis kirs Ukrainos sieną, Aleksandrui Lukašenkai verta sustiprinti atominės elektrinės Ostravoje apsaugą. Apie tai ukrainietiško televizijos kanalo eteryje pareiškė buvęs Aukščiausios Rados deputatas ir „Aidar“ bataliono (uždraustas Rusijoje - RuBaltic.Ru pastaba) „Zapad“ kuopos vadas Igoris Lapinas. Baltarusijos AE jis kažkodėl vadina Minsko ir, tikriausiai, nesuvokia apie tai, kad ji randasi Lietuvos pasienyje, 40 kilometrų nuo Vilniaus. Įvykus rimtai avarijai BelAE, Pabaltijo respublika – ištikima Ukrainos sąjungininkė ir Ukrainos smogikų globėja – nukentės dargi daugiau nei pati Baltarusija.

Po to, kai Lukašenka pasakė, kad karinio konflikto atveju Baltarusijos armija rems Rusijos armiją, Ukrainos ATO veteranai tiesiog privalėjo reaguoti. Taip ir įvyko.

Kario vardas Igoris Lapinas. Tipiškas „maidanogalvių“ šeimos atstovas: vertė Janukovičių, kariavo Dombase, o po to penkerius metus trynė kelnes Aukščiausioje Radoje, retkarčiais iš tribūnos sakydamas patoso kalbas. Kam, kaip ne jam, pasakoti apie potencialaus karo su Baltarusija eigą?

Savo „ekspertinius“ komentarus jis pradėjo nuo Zelenskio kritikos: „Nepriklausomumas nuo šalies-okupanto, o taip pat ir jos satelitų energijos šaltinių yra pirmaeilis Ukrainos valdžios uždavinys. Tenka apgailestauti, bet šį egzaminą nuo pat pirmųjų savo dienų ji neišlaikė. Jie mus vėl pasodino ant Rusijos Federacijos dujų adatos ir ant baltarusiškos elektros adatos.“

Tokiu būdu buvęs deputatas iš karto pademonstravo savo visišką nekompetentingumą tame, kas liečia energetiką.

Tai reiškia, kad tai buvusios valdžios klaida. Tos pačios, kuriai atstovauja... Igoris Lapinas. Jis gi buvo renkamas į parlamentą nuo „Liaudies fronto“ partijos ir iki 2019 metų buvo valdančiosios daugumos deputatu.

Toliau „karo su Rusija“ veteranas pasisako citata, kuri turi būti įtraukta į ukrainietiškos kvailystės aukso fondą: „Kas liečia „juokaujam arba nejuokaujam“ (tai nuoroda į Lukašenkos pareiškimą - RuBaltic.Ru pastaba), pasinaudodamas proga, aš noriu užtikrinti poną Lukašenką, kad jei nors vienas kariškis (man nusispjaut, po kokia vėliava jis tai padarys) kirs Ukrainos valstybės sieną iš Baltarusijos pusės, tegul sustiprina Minsko atominės elektrinės apsaugą, tegul sustiprina tų šiluminių elektrinių, kurios šiandieną yra Baltarusijoje, apsaugą. Jei jie galvoja, kad ukrainiečiai sėdės ir kariaus tik savo teritorijoje, tai, patikėkite manimi, aš pats esu iš Volynės, ir mes su savo berniukais kalbėjome: aš manau, kad mes padėsime savo broliams-sebrams Breste atstatyti konstitucinę tvarką ir juos išlaisvinti iš diktatoriaus Lukašenkos jungo.

Tarp kitko atominę elektrinę Baltarusijoje Lapinas kažkodėl tai vadina Minsko AE. Tokiu atveju, galima teigti, kad Minsko AE turi nepažeidžiamą apsaugą: ją dengia nematomas kupolas. Šių eilučių autorius pasiruošęs ginčytis, kad jei ukrainietiški naciai panorės ką tai padaryti su atomine elektrine Minske, paprasčiausiai, jie jos nesuras...

Bet iš tikrųjų, žinoma, Lapinas turi omenyje Baltarusijos AE Grodno srityje, greta Ostravos.

O tai daug arčiau, negu iki Minsko.

„Aidaroviečio“ pasisakymą tikrai verta parodyti Lietuvos televizijoje.

Pabaltijo respublikoje panašius personažus vietinė valdžia gerbia ir remia, juos kviečia reabilitacijai, jiems renka pinigus, jiems siunčia ginklus ir taip toliau.

Lietuvos Jono Žemaičio vardo karo akademija išleido knygą „Rusijos hibridinis karas: Ukrainos patirtis Baltijos šalims“, jos autorius Eugenijus Dikij – buvęs vieno iš to pačio „Aidaro“ bataliono būrio vadas. Pratarmėje sakoma, kad šią „metodinę mokymo priemonę“ autorius parašė akademijos iniciatyva ir remiamas buvusio Lietuvos URM vadovo ir buvusio Lietuvos ambasadoriaus Kijeve Petro Vaitekūno.

Konservatoriai – „landsbergistai“ iš viso mėgsta gąsdinti savo tautą „branduoline apokalipse“. Tik būsima katastrofa kaltina Lukašenką ir Putiną.

„Ši planeta pasmerkta dėl Kremliaus keršto, tai keršto projektas. Mes turime tai suprasti ir kalbėti atvirai. Šis projektas – agresija Lietuvos atžvilgiu, visų pirma, Rusija – branduolinės agresijos iniciatorius – šioje situacijoje aš siūlau viską tiksliai apibrėžti“. – kalbėjo „Lietuvos valstybingumo patriarchas“ Vytautas Landsbergis.

Ką gi, dabartinė situacija taip pat reikalauja konkrečių apibrėžimų: Ukrainoje parėjusio sušaukimo Aukščiausios Rados deputatas, buvęs savanorių bataliono smogikas grasina Baltarusijos AE paversti Europos radiacinio užkrėtimo šaltiniu.

Tarp kitko, nuo Ostravos iki pačios Ukrainos taip pat ne per toliausia. Keista grasinti panašiomis grėsmėmis, sėdint šalyje, kuri pergyveno Černobylį, ir kurioje iki šio laiko veikia 15 (!) atominių reaktorių. Bet būtent tokie lapinai, jarošai bei kiti paršiukai pateko į aukščiausius Ukrainos politikus ešelonus tylaus NATO šalių sutikimo (arba netgi paramos) dėka.

Tame tarpe ir Lietuvos.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 2 — id: `scraped:rubaltic_lt:026f829b4762e9ce`

**Title:** Geriausia buvusios SSSR šalis: Rusiją amerikiečiai įvertino geriau nei Pabaltijį

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Vakaruose iš naujo peržvelgiami santykiai su buvusio SSSR šalimis. Stereotipinis įvaizdis, kad sėkmingiausiomis iš postsovietinių šalių yra trys Baltijos šalys, kaip vienintelės įstojusios į NATO ir Europos Sąjungą, nueina praeitin. Už tai tenka pripažinti naujosios Rusijos augimą ir jos pasiekimus. Rusijos lyderystė postsovietinėje erdvėje ir Rytų Europoje šiandieną – ne „rusiškos propagandos“, o JAV analitikos išvada, kuri stato „pavyzdinį“ Pabaltijį savo reitingų gale.

Verslo žurnalas U.S. News & World Report – vienas iš vedančiųjų savaitinių JAV žurnalų – visų pirma yra žinomas savo tyrimais: šalių, verslo korporacijų, universitetų, medicinos centrų suniveliavimas pagal rangą. Vienas iš pačių žinomiausių ir turinčių paklausą U.S. News & World Report tyrimų yra kasmetinis geriausių pasaulio šalių reitingas. Šiais tyrimais dažnai remiamasi palyginamojoje geografijoje.

Reitingas nustatomas remiantis 17 tūkstančių ekspertų iš viso pasaulio, kuriems buvo siūloma įvertinti šalis, apie kurias jie turi bazinę eilės kriterijų informaciją apklausos rezultatais. 10 kriterijų priskiriama gyvenimo kokybė, aplinka verslui, socialinė apsauga, kultūros įtaka, raidos dinamiškumas ir kiti.

Remiantis šias kriterijais niveliuojamos 78 šalys, po to skaičiuojamas aritmetinis vidurkis, pridedami objektyvūs rodikliai, kaip tai bendras vidaus produktas (BVP) arba tiesioginių investicijų suma į ekonomika, ir tokiu būdu nustatomos geriausios pasaulio šalys.

Metinės U.S. News & World Report apklausos labai įdomios dėl amžinų postsovietinių diskusijų apie tai, kas kokių pasiekė rezultatų praėjus 30 metų po SSSR sugriuvimo.

Rusijos Federacija ne tik lenkia Centrinės Azijos respublikas arba buvusiais Centrinės ir Rytų Europos socialistines šalis – geriausiųjų pasaulio šalių reitinge ji randasi visiškai kitoje svorio kategorijoje. Bendroje įskaitoje Rusija užima 24 vietą – greta su Airija, Austrija, Arabų Emyratais, Indija ir Brazilija.

Palyginimui, tarp kitų buvusių sovietų respublikų, Estija užima 57 vietą, Latvija – 64-ąją, Lietuva – 67-ąją, Ukraina – 71-ąją, Kazachstanas – 72-ąją, Uzbekistanas – 73-ąją, Baltarusija -75 – ąją.

Panašios ekspertų išvados patvirtina pasisakymus tų, kurie kalba, kad terminas „postsovietinė erdvė“ jau seniai neatitinka tikrovės.

Pastarosios, tarp kitko, nežiūrint į jų snobiška retoriką, kad jos ne postsovietinės, taip ir pasiliko toje postsovietinėje lygoje. Vėl gi, tai JAV analitikų išvados. Lietuva su savo 67 vieta netoli nuėjo nuo Ukrainos su savo 71 vieta – nors kad ir yra Europos Sąjungos ir NATO narė.

Nusistovėjusius stereotipus apie tai, kas iš buvusių SSSR respublikų per tuos 30 metų vystėsi „teisingai“, kas – „neteisingai“, ir kas kam yra kelrode žvaigžde, etalonu ir pavyzdžiu, tenka tikslinti. Geriausiųjų reitinge Rusija daugeliu pozicijų aplenkia ne tik „progresyvias“ Pabaltijo šalis, bet ir Lenkiją (43 vieta), į kuria orientuoją Ukrainą ir Baltarusiją, ir Rumuniją (63 vieta) į kurią nukreipiama Moldaviją.

Tačiau apie Baltijos šalis reikia pasakyti atskirai. Visa jų postsovietinė istorija remiasi „sėkmės istorijos“ mitu, pagal kurį Lietuva, Latvija ir Estija yra demokratinės modernizacijos etalonas, kuris jas padarė pilnavertėmis vakarų „elito klubo“ narėmis ir pakėlė į nepasiekiamą lygį kitų buvusių SSSR dalyvių atžvilgiu, kurie nepriartėjo prie Pabaltijo „pasiekimų“.

U.S. News & World Report geriausiųjų pasaulio šalių reitingas šiai mitologijai užduoda labai didelį klausimą. Taip, Pabaltijo šalys lenkia daugelį buvusių sovietų respublikų, bet nežymiai.

Visų pirma, jos randasi vienoje grupėje: 64 vieta Latvijai, 66 vieta Azerbaidžanui, 67 vieta Lietuvai ir 73 vieta Uzbekistanui – tai ne apie pilnaverčius „vakarų elito klubo“ narius. Antra, Rusijos atotrūkis nuo jų yra labai didelis ir nenugalimas.

Galima prieštarauti, kad negalima lyginti nepalyginamąjį. Teisingai. Kur Rusija ir kur Pabaltijys pagal, pavyzdžiui, karinę galią?

Palyginti reikia pagal tuos rodiklius, pagal kuriuos save su Rusija lygina patys Baltijos šalių „patriotai“. Jie pastoviai pabrėžia, kad Estija, Latvija ir Lietuva, nors ir yra nepalyginamai silpnesnės ir mažesnės už didžiąją rytų kaimynę, bet už tai turtingesnė, sėkmingesnė, kultūringesnė negu „ruskynas, kuris nuo degtinės stimpa patvoryje“.

Savo BVP jie skaičiuoja tokiu būdu, kad perskaičiavus vienam gyventojui jis bet kokiu atveju pasirodo didesnis už rusišką. „Koziriuoja“ savo algomis – pačiomis didžiausiomis buvusiame SSSR, delikačiai nutylėdami apie savo kainas ir komunalinio ūkio tarifus. Apeliuoja į visokiausius vakarų sėkmingumo reitingus.

Labai gerai, apeliuojame ir mes. U.S. News & World Report gyvenimo kokybės reitingas: Estija – 48 vieta, Latvija – 50 vieta, Lietuva – 56 vieta, Rusija – 31 vieta. Lyderis – Rusija. Verslininkystė: Estija – 45 vieta, Latvija – 55 vieta, Lietuva – 48 vieta, Rusija – 22 vieta. Ir vėl lyderis – Rusija, tarp kitko neginčijamas. Nors ir pralaimi Baltijos šalims verslo viešumo reitinge.

Tačiau patys įspūdingiausi rodikliai randami kultūrinės įtakos ir to, ką amerikiečiai pavadino Movers: „prognozuojamas būsimasis šalies augimas bendrojo vidaus produkto požiūriu pagal perkamosios galios paritetą“, reitinguose. Kitaip sakant, pozityvi dinamika, perspektyvos.

Latvija užima priešpaskutinę, 77 vietą pagal kultūros įtakos rodiklį, ir 78 (paskutiniąją) pagal perspektyvas. Lietuva – paskutiniąją, 78 vieta pagal kultūros įtaką ir 76 – pagal perspektyvas. Estija pagal kultūros įtakos rodiklį - 73 vietą pasaulyje ir pagal perspektyvas – 72 vietą.

Ką tai reiškia? Trejos Baltijos šalys per 30 postsovietinių metų nieko nedavė pasauliui, ir pasaulis apie jas nieko nežino. Ir kaip kitaip, jei šias šalis paliko didelė dauguma jaunų, aktyvių, kūrybiškai mastančių gyventojų? Dėl to ir nėra perspektyvų. Kokios gali būti mirštančių šalių perspektyvos?

Dabar palyginsime su Rusija. Rusijos kultūros įtaka – 28 vieta pasaulyje, perspektyvos – 11 vieta.

Viskas gi aišku?

Gyvenimas sugriovė Pabaltijo mitus apie savo sėkmingumą ir mirštančią Rusiją. Ir ne tik gyvenimas. Amerikiečiai, štai, taip pat griauna.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 3 — id: `scraped:rubaltic_lt:6c4da988f573a70a`

**Title:** Kinija pasiekė savo: lietuviškas verslas bėga iš Lietuvos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuviškas verslas priverstas keltis į kitas šalis, idant apeiti neoficialias Kinijos sankcijas. Apie tai papasakojo Vilniaus pramonės ir verslo asociacijos prezidentas Sigitas Besagirskis. Jo žodžiais tariant, dvejos kompanijos jau uždarė savo veiklą Lietuvoje, dar maždaug pusė šimto užsiima tuo, kad atidaryti savo atstovybes užsienyje. Kinija ramiai siekia savo: daugumai verslininkų paprasčiau atsisakyti verslo mažoje Pabaltijo Respublikoje, negu netekti didelės kinų rinkos.

„Dvejos įmonės, kurių konfidencialumo sumetimais nepagarsinsiu, o jos apie tai gali pasakyti pačios, - jau nutraukė veiklą Lietuvoje, dar maždaug pusė asociacijos narių užsiima atstovybių atidarymu, dažniausiai kaimyninėse šalyse“,- sako Sigitas Besagirskis.

Kai kurios kompanijos jau turi savo filialus užsienyje, bet patiria sunkumus patenkant į Kinijos rinką: Padangių šalis „atkerta“ visas prekes, kurių sudėtyje yra Lietuvoje pagaminti komponentai, o taip pat trukdo pramoninės paskirties produkcijos tiekimui į Pabaltijo respubliką. Grėsmė pakibo virš aukštųjų technologijų šalies ūkio šakų.

Jei tikėti Besagirskiu, pirmosios firmos jau kapituliavo prieš KLR. Tos kurios atidaro savo atstovybes užsienyje, taip pat, tikriausiai rengiasi uždaryti savo verslą Lietuvoje (arba, galų gale, aptarinėja tokią galimybę).

Vilniaus pramonės ir verslo asociacijos Interneto svetainėje sakoma, kad ji apglėbia daugiau nei 300 įvairių  kompanijų. Maždaug pusantro šimto iš jų ketina atidaryti  savo atstovybes kituose šalyse. O kalbama apie sostinės regioną! Kiek potencialių kompanijų – „pabėgėlių“ bus visoje Lietuvoje, galima tik spėlioti.

Varšuva jau gali apdovanoti Lietuvos užsienio reikalų ministrą Gabrielių Landsbergį kokiu nors ordinu ar medaliu, būtent jai atiteks visi prekybinio-ekonominio kaimyninės šalies smaugimo vaisiai. Kažkas tai, galimai persikels į Latviją, bet Lenkija rodosi daug patrauklesniu variantu. Ten daugiau galimybių, daugiau darbo jėgos, daugiau pinigų ir t.t.

Pats laikas prisiminti kaip prasidėjo šis konfliktas. Iš pradžių Lietuvoje kalbėjo, kad nėra ko bijoti: esą, Kinija negalės padaryti mums rimtos ekonominės žalos. Nukentės tik atskiros kompanijos, kurios prekiauja su KLR, bet kalbama apie nedidelius pinigus.

Vėliau paaiškėjo, kad Kinija verčia užsienio investorius išeiti iš Lietuvos. Vyriausybėje visi buvo ramūs. Štai ką gruodžio pabaigoje  kalbėjo ekonomikos ir inovacijų ministrė Aušrinė Armonaitė: „Lietuva – viena iš su  labiausiai išvystytomis skaitmeninėmis technologijomis šalių, jos patrauklumas išliko, reputacija nenukentėjo. (...) Pasirodė informacija, baiminimasis dėl investorių, bet nei vienas investorius neišėjo iš Lietuvos, artimiausiam laikui realių planų neturi, yra baiminimasis. Atvirkščiai, sekantiems metams mes pasirašome dideles susitarimų apimtis su naujais investoriais. Pas mus tokių susitarimų nemažiau 30“.

Situaciją su Kinija ponia ministrė apibūdino, kaip „nedidelę krizę“. Dabar pasirodė informacija, kad investoriai, visgi, palieka Lietuvą. Kaip į tai reaguoja Armonaitė?  Kol kas ji tyli, bet įdomiai pasakė premjerė Ingrida Šimonytė: „Praėję metai parodė, kad per didelis priklausomumas nuo importo iš trečiųjų šalių – tai prabanga, kurios mes negalime sau leisti. Europos pramonės suverenitetas yra gyvybiškai svarbus, apie ką liudija nesenai Kinijoje priimtos priemonės, apribojančios tarptautinę Lietuvos prekybą. Todėl visą Europa pirmoje eilėje turi orientuotis į vietines gamybos pajėgumus, diversifikuoti rinkas ir plėsti  ekonominių partnerių ratą“.

Kokį signalą gaus vietiniai verslininkai ir užsienio korporacijos, kurių gamybos pajėgumai randasi Lietuvos teritorijoje?

O kuo užsiima Gabrielius Landsbergis? Jis kaip tik ir išvyko ieškoti naujų partnerių: prieš kelias dienas jis buvo priimtas Singapūro verslininkų. Tokia naujiena sukėlė sąmyšį netgi lietuviško meistrimo spaudoje. Konkrečiai, naujienų portalas DELFI klausia: nejaugi Singapūre viskas tvarkoj su žmogaus teisėmis?

Tai supersėkminga šalis, bet ten išvalytas politinis laukas, jau daugiau nei 50 metų valdo viena partija, plačiai taikomos fizinės bausmės. O pats didžiausias nemalonumas, tai kad Sibapūre sodina į kalėjimą homoseksualistus (yra netgi atskiras baudžiamasis straipsnis už vienalyčių asmenų seksualinius santykius, kurio šalies vadovybė nesiruošia atšaukti). Kur gi prapuolė plačiai nuskambėjusi lietuviška vertybių politika?

„Matote, Singapūras turi ilgametes tradicijas ir savo kultūrą tokią, kokią jie turi. Tai mes tikriausiai negalime keisti tos kultūros, kokia yra ten. Kita vertus, turime siekti ir Lietuvos interesų, stengtis, kaip galima geriau juos tenkinti“, – sakė Seimo deputatas Kristijonas Bartaševičius. Tikriausiai, tą patį galima pasakyti ir apie arabus. Praeitais metais Ingrida Šimonytė atidarė Lietuvos verslo forumą Emyratuose. „Aš matau daug mūsų šalių bendro darbo galimybių, kuriant ateitį, taikant inovacinius sprendimus, ypatingai biotechnologijų, lazerių ir atsinaujinančių energijos šaltinių srityje, keliant paslaugų visuomenei kokybę, remiantis GovTech sprendimais bei dirbant kituose kasdieninio žmonių gyvenimo gerinimo srityse ir remiant stabilumą“,- kalbėjo Lietuvos premjerė.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 4 — id: `scraped:rubaltic_lt:ed2c59b774992045`

**Title:** Streikuoja visi: Lietuvos įmonės žengia keliu link visuotinio streiko

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Stambiausios Pabaltijyje azotinių trąšų gamyklos darbuotojai pradėjo neterminuotą streiką. Lietuvos profesinių sąjungų konfederacijos (LPSK) pirmininkų Inga Ruginienė pareiškė, kad Pabaltijo respublikoje tokio masto akcijų nebuvo per visus nepriklausomybės metus. Nepatenkintų Achemos darbuotojų ir vadovybės konfliktas gali įkvėpti ryžtingiems veiksmams kitų kompanijų arba netgi ištisų Lietuvos ūkio šakų atstovus, kuriuos netenkina Lietuvoje susidariusia situacija ir konservatorių vyriausybės politika. RuBaltic.Ru analitikos portalas išskyrė potencialinius naujų protestų židinius.

1. „Lietuvos geležinkelis“ (LŽ) ir Klaipėdos uostas

Į pačių „sprogiausių“ Lietuvos įmonių sąrašą, be jokių abejonių, galima įtraukti valstybinį geležinkelį ir Klaipėdos uostą.

Subendrinti ūkio šakos praradimai vertinami šimtais milijonų eurų.

„Tokios sankcijos Lietuvos ekonomikai gali sukelti rimtas ir ilgalaikes pasekmes. Dabar apie 30% visų krovinių Klaipėdoje – tranzitiniai kroviniai iš Baltarusijos, trąšos sudaro 26% visų uosto krovinių. Lietuvos ekonomikai tai sudarys 300 milijonų eurų sumos dydžio nuostolį į metus“, - prognozuoja Lietuvos jūrų krovos kompanijų asociacijos prezidentas Vaidotas Šileika.

Atvejyje su LG situaciją pagilina atsakomosios Lukašenkos sankcijos – lietuviškų naftos produktų ir trąšų gabenimo geležinkeliu per Baltarusijos teritoriją draudimas. Tai maždaug pusantro milijono tonų produkcijos, skirtos Ukrainos rinkai. LG jau paskaičiavo, kad baltarusiškas „atsakas“ kompanijai gresia dar 10% krovinių apyvartos netekimu.

Pridurkime dar nepaskelbtą sankcijų karą, kurį prieš Lietuvą veda Kinija bei „Belaruskalij“ teisminius ieškinius. Reikalavimą išmokėti kompensacijas už priešlaikinį tranzito kontrakto nutraukimą Minskas pateikia būtent „Lietuvos geležinkeliui“.

Ją pergyvens ne visi: LG jau paskelbė apie ketinimą iki metų pabaigos atleisti iš darbo 300 žmonių. Kaip rodo kaimyninės Latvijos patirtis, tai gali būti didesnio masto atliekamo personalo „atsijojimo“ kampanijos pradžia.

Stabilus krovinių srautas iš Baltarusijos leido Lietuvos uostininkams ir geležinkeliečiams optimistiškai žiūrėti į ateitį (ypatingai, jei atsižvelgti į tai, kad „Belartuskalij“ rengėsi žymiai padidinti savo produkcijos eksportą). Dabar daugelis iš jų atsidurs darbo biržoje. Arba pabandys apginti savo teises kokiomis tai demonstratyviomis akcijomis.

Tiesa, tai padaryti nėra paprasta. Visų pirma, Lietuvos tranzito sektoriaus veikla nėra lokalizuota kokiame tai konkrečiame šalies žemėlapio taške.

Antra, valstybei niekas nemaišo kovoti su tais, kurie parems baltarusių tranzito išsaugojimą. Bet kokie bandymai organizuoti pilnavertį streiką bus prilyginami „grėsmei nacionaliniam saugumui“ ir kelias jiems bus užkertamas teismais. O gatvių protestai netaps masiniais – valdžia juos tiesiog ignoruos.

2. „Vilniaus viešasis transportas“

Achema – ve vienintelė lietuviška kompanija, kurios darbuotojai jau paskelbė streiką. Analogiškai nusprendė veikti ir „Vilniaus viešojo transporto“ profsąjungoje. Streiko idėja buvo aptariama praeitų metų rugsėjyje, o spalyje ją oficialiai rėmė 747 iš 769 balsavimo dalyvių (maždaug 40% visų įmonės darbuotojų).

Ieškovas įrodinėja, kad dėl sudėtingos situacijos su koronavirusu jokiu būdu negalima Lietuvos sostinėje destabilizuoti viešojo transporto darbą. Atsakovas gina savo teisę streikuoti siekiant pareikštų tikslų: kalbama apie darbo užmokesčio padidinimą 10% ir darbo sąlygų pagerinimą.

3. Gydytojai ir mokytojai

Sveikatos apsaugos ir švietimo sritys - pastovaus Lietuvos valdžios galvos skausmo šaltinis. Ir gydytojai ir mokytojai Pabaltijo respublikoje laikas nuo laiko pareiškia apie savo teises.

2018 metai Pabaltijo respublikoje pasižymėjo didelio masto pedagogų streiku, kuris apėmė 15% mokyklų. Jo dalyviai reikalavo papildomo finansavimo savo darbo užmokesčio padidinimui. Šių protestų fone tuometinis Lietuvos vyriausybės vadovas Saulius Skvernelis atstatydino ministrę Jurgitą Petrauskienę (nors ir neigė šių įvykių sąryšį).

Pažymėtina, kad mokytojų reikalavimus viešai parėmė Ingrida Šimonytė. Valdančioji „valstiečių“ partija, priešingai, kaltino savo oponentus – konservatorius siekimu rinkimų išvakarėse uždirbti politinius taškus. Šį kartą jie visiškai gali pasikeisti vietomis.

Metams baigiantis streikas „sunyko“, Lietuvos švietimo sistemos darbuotojų profesinė sąjunga pareiškė apie dalinį jų reikalavimų patenkinimą.

Bendrai paėmus, susiorganizavimo ir streikavimo patirtį jie yra įsigiję. Kaip ir nepasitenkinimo priežastis: Lietuvos švietimo sistema, kaip ir anksčiau negali pasigirti aukštais darbo užmokesčiais.

4. Ūkininkai

Ūkininkų protestai Pabaltijo respublikose taip pat tapo įprastu reiškiniu. Agrarinės produkcijos gamintojai Lietuvoje, Latvijoje ir Estijoje dėl sankcijų karo su Rusija nukentėjo kur kas labiau nei kitų ūkio šakų darbuotojai.

Ryškų „parodomąjį pasirodymą“ jie pademonstravo 2019 metais, kai į miestų gatves išrideno traktorių ir vilkikų kolonas. Jei tikėti akcijos organizatoriais, jame dalyvavo iki 3 tūkstančių vienetų žemės ūkio technikos (žmonių – dar daugiau).

Ši disproporcija išliks dar mažiausiai keletą metų.

Gal būt, pats ekstremaliausiais agrarinių protestų scenarijus numato svarbių Lietuvos autotransporto arterijų blokadą.

Protestuojantys Kanadoje, akivaizdžiai pademonstravo kaip tai veikia.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 5 — id: `scraped:rubaltic_lt:d8497a6a74b2f506`

**Title:** Smūgis Lietuvai: Lukašenka atsakė į sankcijas Baltarusijai

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Nuo vasario 7 dienos Baltarusija vienašališkai uždraudžia per savo teritoriją iš Lietuvos gabenti naftos perdirbimo produktus, chemines ir mineralines trąšas. Tokiu sprendimu Minskas atsakė į „Belaruskalij“ tranzito blokadą, kurią organizavo Pabaltijo respublikos vadovybė. Atsakomosios sankcijos gresia sukelti problemas konkrečioms įmonėms – Mažeikių NPG ir chemijos gamyklai Achema.

Kaip ir buvo laukiama, iš antro karto Lietuva visgi sugebėjo sustabdyti trąšų tranzitą iš „paskutinės Europos diktatūros“. Nuo vasario 1 dienos Klaipėdos uostas nepriima „Belaruskalij“ produkciją. Ankstesnis kontraktas nutrauktas, naujos paraiškos gabenimui nepatenkintos. „Lietuvos geležinkelis“ pažadėjo Minskui gražinti tuščius vagonus ir neišnaudotą avansą.

Informaciją apie tranzito blokados pradžią patvirtino Baltarusijos premjeras Roman Golovčenko: „Iš tikrųjų, Lietuva nustojo priiminėti mūsų traukinius, kurie gabeno kalį perkrovai Klaipėdos uoste. Atsakomosios priemonės bus griežtos. Mes, kaip priimta sakyti, atsakysim simetriškai. Sprendimas priimtas, jis palies geležinkelio transportą, kuris vyksta iš Lietuvos teritorijos“.

Kiek vėliau Minskas konkretizavo, apie kokias „griežtas priemones“ kalbama. „Baltarusijos Respublika negali ignoruoti šią hibridinę ataką ir yra priversta, kaip jau buvo perspėta anksčiau, imtis atsakomųjų priemonių. Mes nusprendėme uždrausti gabenti per savo teritorija tranzitu siunčiamus geležinkeliu iš Lietuvos naftos produktus, chemines ir mineralines trąšas, pakrautus „Lietuvos geležinkelio“ stotyse. Baltarusijos Respublikos teritorija kiekvienais metais pervežama daugiau nei 1 milijardo dolerių sumos apie 1,5 - 1,6 milijono tonų tokių krovinių“, - sakoma Baltarusijos URM Interneto svetainėje.

Pagal forma atsakymas iš tikrųjų gavosi simetriškas: sankcijos įvestos toms pačioms prekėms, kurias palietė Lietuvos draudimas (priminsime, kad naftos produktų tranzitas iš Baltarusijos taip pat yra uždrausta ir ES lygyje). Bet šiuo atveju, simetriškumas nereiškia lygiavertiškumo.

Krovininė geležinkelio kompanija LTG Cargo – „Lietuvos geležinkelio“ dukterinė įmonė – 2022 metais planavo pervežti per Baltarusiją tranzitu iki 900 tūkstančių tonų naftos ir naftos produktų bei apie 500 tūkstančių tonų trąšų. Akivaizdu, beveik visą produkcija eksportuojama į Ukrainos rinką (Rusijai ji tiesiog nereikalinga). Tokiu būdu, Batka įvaro pleištą tarp Vilniaus ir Kijevo prekybos.

Nesunku suprasti, kokios įmonės taps pagrindinėmis baltarusiškų kontrsankcijų aukomis. Problemos kils, visų pirma, lenkų naftos kompanijai Orlen, kuri valdo Mažeikių NPG (2021 metais ji eksportavo į Ukrainą maždaug 1 milijoną tonų naftos produktų). Antra, stambiausiam Pabaltijyje azotinių trąšų gamintojui - kompanijai Achema prisieis ieškoti naujus maršrutus.

Kokią išeitį jie suras iš susidariusios situacijos? Lietuvos jūrų krovos kompanijų asociacijos prezidentas Vaidotas Šileika sako, kad nagrinėjami įvairūs „apeinantys“ variantai, tame tarpe ir gabenimas automobiliais bei geležinkeliu per Latviją.

Padidėja ir šalių-tranzitorių skaičius, bei gabenimo laikas. Akivaizdžiai, maršrutas nėra pats patraukliausiais. Akivaizdesnis ir paprastesnis sprendimas – Lenkija. Ji Lietuvos krovinių siuntėjams gali pasiūlyti trumpą transportavimo kelią, kur nėra jokios politinės rizikos, galinčios kilti dėl tos pačios Rusijos.

PKN Orlen jau paskelbė, kad yra pasirengusi naftos produktus Ukrainai tiekti per Lenkiją. Vos prieš keletą mėnesių ši kompanija pademonstravo savo įžvalgumą, išpirkdama vienintelį prie Lietuvos-Lenkijos sienos esantį krovininį naftos terminalą - UAB Mockavos Terminalas. Jis ir anksčiau buvo naudojamas naftos produktų tiekimui į Ukrainą apeinat Baltarusiją.

„Viena iš priežasčių, dėl kurių praeitais metais mes pirkome terminalą greta Lenkijos sienos, yra ta, kad turėti galimybę tiekti per Lenkijos teritoriją, tuo atveju, jei pasikeis politinė situacija“, - kalbėjo PKN Orlen kompanijos atstovė Kristina Gendvil.

Tai reiškia, kad Krovinio siuntėjams iš Lietuvos kelyje teks du kartus „persiauti“ - pereiti iš savo bėgių į europietiškus ir, privažiavus prie Ukrainos, viską daryti atvirkščiai.

Pabrangus logistikai, Orlen ir Achemos produkcijos konkurencingumas mažėja. Tikriausiai to ir siekia Lukašenka (iškrentančias naftos produktų ir trąšų apimtis Ukrainoje galės papildyti pati Baltarusija). Bet Lietuvai tai nėra mirtina.

Vargu, kad Minskas siekė triuškinančio smūgio kaimyninės šalies ekonomikai. Visų pirma, sankcijų bumerangas visada atlekia atgal: lietuviškų prekių gabenimo uždraudimas, tokiu ar kitokiu būdu Baltarusijai atsilieps tranzito rentos praradimu. Antra, pagrindinį smūgį Lietuva kirto pati sau, kai nutraukė kontraktą su „Belaruskalij“.

Jei tikėti Romanu Golovčenko, šis klausimas jau išspręstas. „Mes seniai ruošėmės šiai situacijai ir savo tiekimą perorientavome. Dėl kiek ilgesnio logistikos peties Rusijos Federacijoje mūsų gamintojams sumažėjo marža, bet ji bus kompensuota pasaulinių kainų augimu. Tokiu būdu, iš esmės, mes nieko nepraradome, prarado Lietuvos ekonomika“, - pareiškė Baltarusijos premjeras.

Apie tai, būtent kokie uostai priėmė „Belaruskalij“ krovinius, istorija nutyli. Juolab, RF prezidento sekretorius presai Dmitrij Peskov painformavo, kad Minskas ir Maskva dar tik aptaria trąšų tranzito klausimą.

Sprendimas gali būti visiškai ne toks paprastas, kaip apie tai kalba Baltarusijos premjeras.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 6 — id: `scraped:rubaltic_lt:d296ec002e0450fb`

**Title:** Procesas prasidėjo: Lietuvoje didėja bedarbystė dėl sankcijų Baltarusijai

**Source:** rubaltic_lt (propaganda)

**Text:**

```
„Lietuvos geležinkelis“ pranešė apie krovinių srauto sumažėjimą 10% dėl Baltarusijos kontrsankcijų Lietuvai. Prieš tai „Lietuvos geležinkelis“ anonsavo kelių šimtų darbuotojų atleidimą iš darbo. Tai tik vienos įmonės netekimai ir tik pirmomis sankcijų baltarusiškom kalio trąšom ir atsakomųjų Baltarusijos sankcijų veikimo dienomis. Tas pats gresia ir kitoms stambiausioms Lietuvos įmonėms: pradėtas sankcijų karas su Minsku dabar jas įstumia į tiekimo bei rentabilumo krizę, ir, viso to padariniu tampa masinių darbuotojų atleidimų iš darbo perspektyva.

Vasario pradžioje „Lietuvos geležinkelio“ atstovas spaudai paskelbė apie ketinimą metų laike atleisti iš darbo iki 300 darbuotojų. LG personalo direktorė Irena Jankutė – Balkūnė pabrėžė, kad darbuotojams buvo pažadėta, pasikeitus situacijai, juos gražinti į darbą.

Po kelių dienų LG pareiškė, kad jo krovinių srautas sumažėjo 10%. Per mėnesį geležinkelis pervežė 45 kroviniais sąstatais mažiau, negu anksčiau.

Ir tapo aišku, kad situacija nesikeis.

Vien baltarusiško kalio tranzitas Klaipėdos uostui ir „Lietuvos geležinkeliui“ duodavo penktadalį krovinių srauto. Lietuva pati sau šovė į koją, užblokuodama tranzitą.

Kartu su tuo „Belaruskalij“ produkcija – tai tik dalis tranzito krovinių iš Baltarusijos. Savo geriausiais metais baltarusiškas tranzitas sudarė daugiau ne trečdalį Klaipėdos uosto ir geležinkelio krovinių apyvartos. Bet baltarusiški naftos produktai paliko Lietuvą dar prieš metus – iš Klaipėdos juos išvedė Baltarusija. Dabar išėjo baltarusiškos kalio trąšos – jų tranzitą uždraudė Lietuvos vyriausybė pagal savo demokratinio solidarumo su antibaltarusiškomis JAV sankcijomis supratimą.

Be to, tranzito srautas Lietuvos geležinkeliu nutraukiamas ne tik vakarų kryptimi, bet ir į rytus. Baltarusija įvedė priešpriešines „Belaruskalij“ krovinių uždraudimui sankcijas. Uždraustas lietuviškų naftos produktų ir trąšų gabenimas per Baltarusijos teritoriją.

Pagrinde smūgis nukreiptas į dvejas įmones: cheminių trąšų gamykla Achema ir Mažeikių NPG – dabar priklausanti lenkams Orlen Lietuva. Abiejų gamyklų vadovybė dabar kalba apie tranzito perorientavimą, ieško aplinkinių maršrutų į rytus ir pietus per Lenkiją

Visų pirma, tranzitas konservatyvus verslas, suderinti jo tiekimo kanalai iš karto, „tik spragtelėjus“, nesigauna. Antra, kalbama apie tranzitą geležinkeliu. Gabenant per Lenkija, riedmenis prisieis „perauti“ iš plačios rusiškos geležinkelio vėžės į siaurą europietišką, o tiekiant, pavyzdžiui, į Ukrainą – „perauti“ vėl į plačią rusiško geležinkelio vėžę. O tai – laikas, o laikas logistikoje – pinigai.

Gabenti dideles krovinių apimtis automobilių transportu nėra rentabilu.

Trečia, maršrutas per Baltarusija buvo pats trumpiausias, vadinasi, pats naudingiausias. Aplinkiniai maršrutai bet kokiu atveju bus brangesni, jei tik Lenkija neduos tranzitui per savo teritoriją nuolaidą (nors, dėl ko jai tai daryti?). Todėl Lietuvos įmonės bet kokiu atveju patirs praradimus.

Dabar pažvelkime į šių įmonių sąrašą. Patį trumpiausią. Naftos perdirbimo gamykla Orlen Lietuva, „Lietuvos geležinkelis“, Achema, Klaipėdos uostas...

Ši krizė lengvai peraugs į politinę krizę, kadangi visiems tiems, kurie neteko pragyvenimo šaltinio, bus akivaizdi jiems kilusių sunkumų priežastis – Lietuvos vyriausybės užsienio politika.

RuBaltic.Ru analitikos portalas jau daug kartų rašė, kad tokia politika Lietuvą prives prie masinių atleidimų iš darbo ir bankrotų. Taip ir vyksta.

Dabar pagrindinis klausimas: ar sugebės Lietuvos valdžia greitai kompensuoti nukentėjusiems lietuviams jų praradimus? Sanatorijos „Belarus“ Druskininkuose istorija, kai dėl sankcijų be algų liko keletas šimtų lietuvių, demonstruoja, kad ne.

Taip kad, jei nesigaus operatyviai išsiusti visus bedarbius uždarbiauti į Airiją ir greitai gauti reikalingo dydžio Europos Sąjungos paramą, Lietuvos politinis gyvenimas persikels į gatves ir taps labai karštu.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 7 — id: `scraped:rubaltic_lt:7d19555a0cb7ae5d`

**Title:** Ar tu atgailauji už „sovietinę okupaciją“: Lietuvos anketa rusų pop žvaigždėmsAr tu atgailauji už „sovietinę okupaciją“: Lietuvos anketa rusų pop žvaigždėms

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos kultūros ministerija paruošė specialią anketą Rusijos įžymybėms, kurios planuoja gastroliuoti Lietuvos Respublikoje. Remdamasis pop žvaigždžių atsakymais oficialus Vilnius spręs ar leisti joms įvažiuoti į Lietuvą. Valdininkai patvirtino, kad apklausos lape bus klausimas apie tai, kam priklauso Krymas. RuBaltic.Ru analitikos portalas numatė, kokius dar klausimus Lietuva gali užduoti rusiško šou verslo žvaigždėms.

1. Kas yra Baltarusijos prezidentas:

А. Aleksandras Lukašenka;

B. Svetlana Tichonouskaja;

C. Baltarusijoje nėra prezidento – tai istorinė Didžiosios Lietuvos Kunigaikštystės dalis.

Paskutini atsakymo atveju lietuviškas šengenas išduodamas nemokamai.

2. Natašos Koroliovos daina „Mažoji šalis“...

А. Parašyta ne apie Lietuvą, kadangi Lietuva nekompleksuota dėl savo dydžio.

B. Parašyta apie Latviją, kadangi ji yra dar mažesnė;

C. Tai šovinizmas ir imperinis chamiškumas, dėl ko Natašai Koroliovai turi būti įvestos Europos Sąjungos sankcijos.

Visi atsakymai – teisingi, įvažiavimas leidžiamas priklausomai nuo apklausiamojo nuoširdumo juos pagarsinant.

3. Kokius patiekalus iš lietuviško restorano meniu jūs pasirinksite?

А. Lietuviškus cepelinus su grybų padažu;

B. Ukrainietiškus barščius su lašiniais;

C. Pekino antį;

D. Krymo čeburekus, bet tik sutrupintus į ukrainietiškus barščius su lašiniais.

Atsakius variantu «C», įvažiavimas į Lietuvą automatiškai uždraudžiamas 5 metams – už simpatijas autoritariniai komunistinei Kinijai.

4. Kokie Jūsų santykiai su Dima Bilanu?

А. Čmoki-čmoki;

B. Ta netalentinga menkystė niekada netaps tokia žvaigžde kaip aš!;

C. Bilanas – rusiškas militaristas, agresorius ir kultūrinis okupantas.

Įvažiavimas leidžiamas, tik atsakius paskutiniu variantu. 2016 metais Lietuva uždraudė Dimos Bilano vasario 23 d. koncertą Vilniuje, jį įvertindama kaip užslėptą “okupantiškos” Tėvynės gynėjo dienos šventimą.

5. Aprašykite, ką jūs matote šiame paveikslėlyje.

А. Tai aš, mano publikos nukryžiuotas ant mano populiarumo kryžiaus!!!

B. Tai okupacinio totalitarinio nusikalstamo SSSR režimo simbolis;

C. Tai žvaigždutė.

Už paskutinį atsakymą įvažiavimas į Lietuva uždraudžiamas, ir anketoje pažymima „psichas“.

6. Kas iš išvardinto sukelia grėsmę Lietuvos nacionaliniam saugumui:

А. Degtinė;

B. Dešra;

C. Žaisliniai kareivėliai;

D. Koks beprotis išgalvojo tokią anketą?!

Atsakius paskutiniu variantu, įvažiuoti į Lietuvą neleidžiama. Politiniais sumetimais įvairiu metu rusiška degtinė, „Sovietskaja“ rūšies dešros gaminiai ir žaisliniai Raudonosios Armijos kareivėliai buvo draudžiami ir išimami iš prekybos tinklo.

7. Ar jūs sutinkate diskutuoti Laisvosios Rusijos forume Vilniuje?

А. Taip, aš esu pasiruošęs pasuokti lakštingala duete su politologu Solovjevu;

B. Taip, geroje scenoje ir už gerą atlyginimą;

C. Taip, aš noriu paprašyti politinio prieglaudžio Lietuvoje ir nesustodamas suokti apie kruvinąjį Putino režimą Laisvosios Rusijos forume.

8. Kaip jūs vertinate principingą Lietuvos užsienio politiką?

А. Principinga Lietuvos užsienio politika labai principinga;

B. Principinga Lietuvos užsienio politika labai teisinga ir principinga;

C. Principinga Lietuvos užsienio politika yra labai reikalinga, būtina ginant bendras žmonijos vertybes ir principinga.

Visi atsakymai teisingi, atsakius į visus klausimus įvažiavimas į Lietuvą draudžiamas. Principinga Lietuvos užsienio politika numato įvažiavimo draudimą visiems be išimties Rusijos piliečiams iki to laiko, kol jie kolektyviai nepareikš savo atgailą, neišmokės Lietuvai kompensaciją už „sovietų okupaciją“ ir nesudraskys „kruvinąją imperiją“ į dešimtų kraujuojančių skutų.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 8 — id: `scraped:rubaltic_lt:1606ce1c0117a8fe`

**Title:** Mūsų širdys reikalauja permainų: Amerikos jaunimas nusivylė JAV

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Didėjanti visuomeninė – politinė JAV vidaus krizė pasireiškė savo gilumu. Nuo Amerikos nusigręžia jos ateitis: dauguma amerikiečių jaunimo mano, kad JAV demokratija randasi pavojuje arba iš viso yra sugriuvusi. Amerikietiškoji tragedija – Jungtinių Valstijų vertybės praradimas naujos amerikiečių kartos akyse – tai ir dešimčių Amerikos šalių-satelitų tragedija, kurioms JAV išlieka kelrode žvaigžde. Šios šalys siekia idealo, kuris vis didesniam pačių amerikiečių skaičiui jau nebeegzistuoja.

„Dauguma (52%) jaunų amerikiečių mano, kad mūsų demokratija arba „randasi bėdoje“ arba „sugriuvo“. Tik 7% jaunų amerikiečių Jungtines Valstijas laiko „sveika demokratija; 27% apibūdino [amerikiečių] tautą kaip „dalinai funkcionuojančią demokratiją“, 39% - kaip „demokratiją kuri randasi bėdoje“, o  13% - pareiškė, kad tauta „su nesėkminga demokratija“ – nurodoma Harvard Kennedy School – Harvardo universiteto Prezidento Džono Kenedžio v. valdymo mokyklos atliktame tyrime.

Prestižinė mokykla daugiau nei 20 metų atlieka politinių amerikiečių jaunimo pažiūrų monitoringą, ir dabar pripažįsta, kad dar niekada  jų išvados nebuvo tokios nerimastingos.

„Po 2020 metų protestų rekordo jauni amerikiečiai yra labai sunerimę. Kai jie žiūri į Ameriką, kurią artimiausiu metu paveldės, jie mato, kad demokratija ir klimatas pavojuje, o Vašingtonas labiau suinteresuotas konfrontacija, negu kompromisu“, - pasisako, apklausą atlikusio Visuomenės nuomonės instituto Harvardo politikos mokyklos (IOP) direktorius Džonas Della Volpė.

Sociologo nuomone, jaunieji Amerikos piliečiai „panašu, yra pasiryžę kovoti už permainas, kurių jie siekia“.

Pasireiškusius naujųjų amerikiečių jausmus bei nuotaikas, postsovietiškas žmogus turi suprasti  orientuodamasis į vėlyvo persitvarkymo laikus. Dabar, kaip niekada, tarp JAV jaunimo  sėkmingai pasklis memai „taip gyventi negalima“, „ne tą šalį pavadino Hondurasu“  ir „permainų, mes laukiame permainų“.

Dauguma jaunų amerikiečių susiduria su psichinės sveikatos problemomis: virš 50% jaunuolių atliekantiems apklausą atsakė, kad paskutiniu metu jaučiasi prislėgtais ir apimtais nevilties. „Sunku įsisąmoninti tai, ką visi mes jaučiame tautos mastu, bet asmeniškai aš tai dažnai pastebiu pas artimus draugus“, - pasisakė IOP studentų asociacijos vadovė 23 metų Žana Ramadan tyrimų prezentacijos metu.

Panašūs procesai Amerikos visuomenėje sklinda Džozefo Baideno administracijos bandymų fone kurti JAV užsienio politikos „naująją“ ideologiją aplink blizgančio demokratijos vaizdo. Baltieji rūmai išorės pasaulį dalina į demokratiją ir autokratiją, organizuoja demokratijos viršūnių susitikimus prieš autokratiją, ir tose viršūnių susitikimuose kokios tai Moldovos prezidentėlė pareiškia, kad jų jaunoji demokratija ryžtingai smerkia Rusijos ir Kinijos autokratiją ir lygiuojasi į vedantįjį ir nukreipiantįjį demokratines JAV vaidmenį.

Jungtinės Valstijos – tai ideokratija, valstybingumas sukurti ideologijos pagrindu. Tokia pat ideokratija buvo Sovietų Sąjunga, nors ideologijos buvo priešingos. Bet tautos formavimo požiūriu įsitikinimas pavyzdine Amerikos politine santvarka – tai tas pats, kaip ir sovietų marksizmas-leninizmas, tautų draugystė ir Pergalės Didžiajame Tėvynės kare kultas.

Kas atsitiko po to, kai persitvarkymo metu SSSR pasirodė publikacijos, kad Leninas - tai grybas, kurį reikia išmesti iš Mauzoliejaus, „tautų draugystė“ pavirto sąjunginių respublikų kariniais konfliktais, o apie Didžiąją Pergalę prasidėjo kalbos, kad „geriau mus būtų nugalėję vokiečiai, tada dabar gurkšnotume alų iš Bavarijos“? Teisingai, šalis sugriuvo.

Neįmanoma būti legitimiu globaliniu lyderiu tarptautinės bendrijos akyse, kai šalies viduje legitimumas yra pairęs.

Kol Vašingtono administracija kabinėja Rusijai etiketę „autoritarinis Vladimiro Putino režimas“, patys amerikiečiai savo „elitą“ vadina supuvusia ir korumpuota „Vašingtono pelke“. Kol, savo išsivystyme atsilikę nuo istorijos traukinio limitrofai Rusijos pasienyje iš įpratimo meldžiasi Amerikai, kaip demokratijos idealui, pačioje Amerikoje daugeliui madingu tapo paniekinamai pažeminantis požiūris į savo šalį. Ją vadinti bananų respublika, neišvystyta Britanijos kolonija, kuri iš tikrųjų ne kuo geresnė už Hondurasą – tai viešojoje amerikiečių erdvėje šiandieną skaitoma geru tonu.

Ypatingai gaila šioje istorijoje paminėtų limitrofų.

Kokioje tai Lietuvoje valdančios partijos politikai televizijos ekrane pareiškia, kad be JAV dabar nebūtų nei Ukrainos, nei Lietuvos, o Amerikoje tuo tarpu „progresyvi“ spalvotų feminisčių ir LGBT aktyvistų minia verčia eilinį paminklą žymiam amerikiečiui, šūkaudami, kad Amerika – tai blogis, ir ji niekada nebuvo didžiąją.

Ir ateitis priklauso šiai miniai, kadangi ji yra jauna ir pasionarinė.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 9 — id: `scraped:rubaltic_lt:b27b119b275d1801`

**Title:** „Okupantų“ paveldą sunaikino  be reikalo: į Pabaltijį atėjo atominių elektrinių mada

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Įkandin Estijos, apie mažos galios atominio reaktoriaus statybą susimąstė  Latvijos valdžia. Europos deputatas Robertas Zilė mano, kad tai yra optimalus šalies aprūpinimo pakankamu elektros energijos kiekiu už priimtiną kainą, variantas. Lenkijos kompanijos jau ieško branduolinės energetikos vystymo investorių, Lietuvos prezidentas Gitanas Nausėda taip pat pradėjo kalbėti apie mini - AE statybos perspektyvą. Šiame kontekste Ignalinos atominės elektrinės, Sovietų Sąjungos pastatytos visam Pabaltijui ir Lietuvos likviduotos kaip „okupantų paveldas“, likimas atrodo tragišku farsu. Ar buvo verta uždaryti Ignalinos AE tam, kad po kelių metų susimąstyti apie naujų AE statybą?

„Mums reikia pasistengti dujas bazinėms galioms pakeisti kuo tai kitu, -  pareiškė Robertas Zilė, komentuodamas smarkų elektros energijos kainų augimą Latvijoje. – Klausimas tame, kas tai galėtu būti. Mano požiūriu, tai galėtu būti, taip vadinamos, modulinės atominės elektrinės. Bus gerai, jei mums pavyks, sakysim, su estais kažką tai tokio padaryti. Arba surasti kokį tai kitą sprendimą. Bet statyti jūros pakrantėje tūkstančius vėjo jėgainių – tai ne sprendimas. Mano nuomone, šiuo metu geriausi energetikos portfeliai pas suomius ir švedus. Jei pažvelgsime į juos, pamatysime, kad ten daug atsinaujinančios energijos resursų, bet abi šalys turi ir atominės energijos“.

Tokios pačios nuomonės yra ir Latvijos Seimo deputatas, buvęs Latvijos ekonomikos ministras Arvydas Ašeradensas: „Aš manau, kad planas daugeliui pasirodys labai ambicingu, bet mes turime kalbėti arba Baltijos šalių, arba atskirų valstybių lygyje apie atomines elektrines. Kitų sprendimu mes nematome. Todėl, kad jei pas mus nebus generuojančių galių, bet koks deficitas sukels kainų šuolį“.

Pažymėtina, kad mini - AE statybų klausimas Latvijoje yra aptariamas ne tik atskirų politikų lygyje.

Tuo metu Estijoje buvo paskelbti socialinės apklausos rezultatai, remiantis kuriais, 68% šalies gyventojų pritaria arba greičiau pritaria mažųjų naujos kartos atominių elektrinių statybai. Prieš tai panaši apklausa buvo atliekama 2021 metų rugpjūtyje – nuo to laiko atsakiusiųjų „taip“ ir „greičiau taip“ sumos skaičius  padidėjo 11%.

Estijoje pačių populiariausiųjų energijos šaltiniu sąraše  mažosios AE jau pasiveja vėjo jėgainių parką ir lenkia saulės energijos generaciją. Įspūdingas rezultatas, atsižvelgiant į tai, kad ES teritorijoje metai iš metų vedama masinė (netgi agresyvi) „žaliojo“ kurso propaganda.

„Aukštos dujų ir elektros energijos kainos šį rudenį privertė žmones vis daugiau domėtis energetikos klausimais. Atėjo supratimas, kad negalima pasitikėti tik geru oru. Estija subrendo tam, kad dešimties metų laikotarpiu rimtai panagrinėti galimybę pakeisti 19-jo amžiaus skalūnų energetiką naujos kartos 21-ojo amžiaus  atomine energetika“, - pažymi kompanijos Fermi Energia vadovas Kalevas Kallemetsas.

Lenkijoje, kaip ir Estijoje, jau ne pirmus metus aptariama atominių reaktorių statyba. Iki 2040 metų šalys numato pastatyti dvejas AE.

„Mes jau pradėjome ruoštis atominės elektrinės statybai. Dabartiniu momentu rengiamos ataskaitos apie elektrinių įtaką aplinkai ir apie objekto buvimo vietą. Dokumentai rengiami dvejoms lokalizacijoms Pomeranijoje greta Gdansko“, - praeitais metais kalbėjo Lenkijos vyriausybės energetinės infrastruktūros įgaliotinis Petras Naimskij.

Pirmąjį atominį reaktorių lenkams nori pastatyti amerikiečių Westinghouse. Kompanijos energetikos sistemų ir ekologinių paslaugų prezidentas Deividas Daremas žada, kad 2033 metais darbai bus baigti.

Lygiagrečiai vedamos derybos  dėl mini – AE projektavimo. Pavyzdžiui, kompanija KGHM Polska Miedź SA planuoja iki 2029 metų pradėti eksploatuoti regione pirmąją mažų modulinių branduolinių reaktorių atominę elektrinę.

Šalies prezidentas Gitanas Nausėda artikuliavo nacionalinės energetikos struktūros

reorganizavimo uždavinį: „Visų pirma turiu omenyje atsinaujinamąją energetiką. Matau iš kitų valstybių pozicijos, kurią svarstėme Europos Sąjungos formatu, kad ir branduolinės energetikos idėjos išgyvena tam tikrą renesansą, ir nemaža ES valstybių dalis kalba apie branduolinių reaktorių statybą. (…) Svarstyti, diskutuoti apie, pavyzdžiui, nedidelio pajėgumo branduolines jėgaines, tai galime daryti, tačiau kol kas turime sutelkti dėmesį į tai, kad turime gaminti pirmiausiai žalią energiją. Antra, turime diversifikuoti savo energijos išteklių įsigijimo šaltinius“. „Lietuvai „taikus atomas“ – tai labai skaudi tema. Bet netgi čia pirmieji valstybės asmenys negali ignoruoti kaimyninių šalių trendus.

Nors apie kokių tai principingai naujų technologijų įsisavinimą nekalbama. Tai, apie ką svajoja lietuviai, latviai, estai ir lenkai – patikimas pigios elektros energijos šaltinis -  pas juos jau buvo. Jis vadinosi – Ignalinos atominė elektrinė.

„Estijai vidutiniškai reikia 1 000 megavatų galios. Žiemą iki 1 600 megavatų. Ateityje, greičiausiai, šis skaičius padidės. Ketvirtojo tipo modulinis branduolinis reaktorius duos 300 megavatų“, - sakė Fermi Energia tarybos pirmininkas Sandoras Lijvė. Palyginimui: tik vieno Ignalinos AE energijos bloko galingumas sudarė 1500 megavatų.

Pabaltijyje niekinamų „vatnikų“ požiūriu, šiandieną Ignalinos AE tapo unikaliu regioninės kvailystės paminklu. Bet sugrįžtant politinei „taikaus atomo“ madai, šių trijų šalių, ypatingai Lietuvos, politikams teks patiems pripažinti Ignaliną savo silpnaprotiškumo  simboliu.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 10 — id: `scraped:rubaltic_lt:e09dbb04e4c23f70`

**Title:** Pirmasis skambutis: stambiausia Pabaltijo trąšų gamykla ruošiasi streikuoti

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Viena iš stambiausių Lietuvos įmonių – azotinių trąšų gamykla Achema – ruošiasi streikui. Atitinkamą sprendimą vienbalsiai palaikė gamyklos darbininkų profesinės sąjungos Taryba. Darbo kolektyvo atstovai pripažįsta, kad jie nesugebėjo „geruoju“ susitarti su kompanijos administracija. Jei streikas bus sėkmingas, Achemos pavyzdys kitoms įmonėms bus užkrečiantis. Pavyzdžiui, „Lietuvos geležinkeliui“ ir Klaipėdos uostui, kurie atsisveikina su baltarusiškų trąšų tranzitu.

Apie tai, kad Achemos darbuotojai yra pasirengę streikuoti, buvo žinoma dar praeitų metų lapkrityje. Jų nepasitenkinimo priežastimi tapo tai, kad derybose gamyklos vadovybė, nenori nusileisti jų reikalavimams dėl darbo sąlygų pagerinimo.

„Jau keletą metų kompanija atsisako pasirašyti kolektyvinę sutartį. Šias metais buvo pažadėta, kad mūsų reikalavimai dėl darbo užmokesčio sistemos bus realizuoti, bet gavę projektą, mes pamatėme, kad pažadai nėra vykdomi, todėl profsąjungos taryboje mes vienbalsiai nusprendėme skelbti streiką“, - pažymi Achemos profsąjungos pirmininkė Birutė Daškevičienė.

Ją palaikė Lietuvos profesinių sąjungų konfederacijos pirmininkė Inga Ruginienė: „Praeitais metais kompanijos akcininkams darbuotojai uždirbo daugiau nei 69 milijonus eurų pelno, bet patys liko „už borto“. Sprendimas streikuoti – nėra lengvas sprendimas, ir jo niekada nepriima vien tik profsąjungos vadovybė. Žinant, kad Lietuvoje darbininkai įprastai yra gana kantrūs, tokie kraštutinumai reiškia, kad visos ribos jau peržengtos“.

Dėl streiko gamykloje buvo balsuojama nuo gruodžio 2 iki 9 dienos. Remiantis darbo įstatymų normomis, streikui būtinas 25% profsąjungos narių sutikimas.

„Šis rezultatas aiškiai nurodo, kad darbuotojai pavargo nuo keletą metų besitęsiančių neteisėtų Achemos vadovybės veiksmų, savo pažadų nevykdymo ir kolektyvinių derybų delsimo“. – sakė Birutė Daškevičienė

Bet pačio streiko pravedimo klausimas pakibo ore. Profsąjungos Taryba jį perkėlė sekantiems metams, tikėdamasi, kad įmonės vadovybė, atstovaujama generalinio direktoriaus Ramūno Miliausko, išsigąs ir nusileis.

Savo ruožtu, Miliauskas nemato gamyklos darbo destabilizavimo priežasčių. Jo žodžiais tariant, buvusios darbo sutarties sąlygos buvo perkeltos į lojalumo ir papildomų lengvatų programą, ir 2020, ir 2021 metais uždarbis didėjo, pastoviai išmokamos premijos.

Maždaug pusantro mėnesio dar tęsėsi „maištininkų“ ir Achemos vadybininkų derybos. Ir tik sausio 28 Daškevičienė pasakė, kad streikas bus: „Profsąjunga padarė viską kas buvo galima, kad susitarti geruoju su kompanijos atstovais. Bet nei argumentai, nei situacijos analizė, nei piketai, nei raginimai laikytis savo duotų pažadų jau keletą metų nieko neduoda. Kolektyvinė sutartis nepasirašyta, informacija yra slepiama, pakankamai yra tokių atvejų, kai nesiskaitoma su darbuotojais, įvairių pažeidimų“.

Bet galioti ji pradės nuo „atgalinės datos“ Achemos darbuotojai paėmė į rankas kalkuliatorius ir pamatė, kad už pirmąjį metų mėnesį kai kurie iš jų gaus 100 eurų mažiau, ne gaudavo anksčiau.

Daškevičienė atkreipia dėmesį į dar vieną nemalonų momentą: Achema Group ataskaitoje nurodyta apie gryno pelno padidėjimą, bet metinės premijos darbuotojams kažkodėl tai nebuvo išmokėtos.

Miliauskui ir kompanijai lieka vos daugiau vienos savaitės, kad įvykdyti profsąjungos reikalavimus: pasirašyti kolektyvinę sutartį, suderinti su ja darbo užmokesčio sistemą ir t.t. Jei to neatsitiks, postsovietinėje Lietuvos istorijoje Achema rizikuoja tapti pirmąją privačia įmone, kurioje įvyko streikas.

Jau daugelį metų Achema nesėkmingai bando nusimesti Lietuvos „energetinės nepriklausomybės“ naštą. Praeitų metų vasarą kompanijos padėtis pablogėjo dėl staigaus gamtinio dujų kainos padidėjimo Europoje. Miliausko žodžiais tariant, nuo liepos mėnesio gamykla dirbo nuostolingai, o rugsėjyje iš viso užkonservavo kai kurias savo gamybine galias. Dalį darbuotojų pervedė į darbą pagal laikinos prastovos modelį.

„Achema įdėmiai vertina tolimesnės veiklos galimybes ir koreguoja savo produktų gamybos krepšį. Dėl šiuo metu susidariusių neprastų rinkos sąlygų buvo nuspręsta po planinio remonto pabaigos nepaleisti vieną iš amoniako cechų“, - pranešė Miliauskas.

Ginant kompanijos vadovybę galima pasakyti, kad dabar jos finansinė padėtis iš tikrųjų yra nepaprasta.

Jei tikėti Achemos darbuotojais, jų streiką remia įtakingos tarptautinės organizacijos – IndustriAllEurope ir Europos visuomeninio aptarnavimo profsąjungų federacija. Čia, tikriausiai, verta priskirti ir Aleksandro Lukašenkos administraciją. Jei atsižvelgti į tai, kad Lietuva pirmųjų asmenų lygyje rėmė protestus Baltarusijoje (tame tarpe ir streikus), Batka su didžiausiu malonumu pasigrožės streikuojančiais Lietuvos darbininkais. Kaip sakoma, nekask duobės kitam…

Situaciją Achemos gamyklos akylai seks ir Ingridos Šimonytės vyriausybė. Reikalas tame, kad Lietuvoje streikų pavojus egzistuoja ne vienoje, atskirai paimtoje įmonėje.

„Dvejus metus mes prašėme pakelti atlyginimus, o praeitų metų gruodyje, nusivylus, buvo pateiktas drastiškas prašymas vadovybei pakelti algas nuo 20 iki 25 proc., o jos kilstelėjo vidutiniškai 4–6 proc., tačiau į derybas su žmonėmis nesileido, nederino, nors kolektyvinė sutartis įpareigoja tai padaryti“, - skundžiasi dokininkų profesinės sąjungos darbininkų pirmininkas Romas Liaudanskis.

Tarp kitko, Klaipėdos uostui sunkūs laikai dar tik prasideda.

Taip, kad nesunku nuspėti, kokiose Lietuvos įmonėse, įkandin Achemos, gali būti paskelti streikai.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 11 — id: `scraped:rubaltic_lt:1e843b109ef09fff`

**Title:** Lietuva ruošiasi dujų blokadai: Kaliningradą Rusija aprūpins jūros keliu

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvoje parengtas energetinio saugumo užtikrinimo planas tam atvejui, jei bus nutrauktas rusiškų dujų tiekimas. Apie tai pareiškė Pabaltijo respublikos Energetikos ministerijos atstovė spaudai Vita Ramanauskaitė. Vilniuje nėra informacijos apie galimus „Gazpromo“ produkcijos tiekimo sutrikimus, bet ten sunerimo dėl informacijos apie plaukiojančio SGD terminalo „Maršalas Vasilevskis“ su stambia krovinio partija sugrįžimo į Kaliningradą. RuBaltic.Ru analitikos portalas aiškinosi, kodėl Rusijos anklavui prireikė dujų ir prie ko čia Baltarusijos prezidentas Aleksandras Lukašenka.

Sausio 25 dieną, pirmą kartą daugiau nei per dvejus metus „Maršalas Vasilevskis“ sustojo Kaliningrado reide. Iki to jis buvo Belgijos Zebriugėje. Leidinys „Komersant“ praneša, kad iš ten laivas atgabeno stambią suskystintų gamtinių dujų (SGD)   partiją (138 milijonus kubinių metrų).

Vėliau paaiškėjo, kad link Kaliningrado kranto plaukia dar vienas SGD tanklaivis Energy Integrity. Jis gabena 168 milijonus kubinių metrų dujų iš „Gazpromo“ projekto Cameroon FLNG   portfelio.

Žinoma, tokią naujieną oficialus Vilnius negalėjo ignoruoti.

Ji pati „Gazpromo“ produkciją gauna iš Baltarusijos ir toliau, vamzdžiu ją transportuoja į Rusijos anklavą. Tai sena ir, suprantama, pati optimaliausia schema.

Bet ne viskas taip paprasta. 2014 metais Lietuva išsinuomavo SGD terminalą ir įsigijo trokštamą „energetinę nepriklausomybę“ nuo „Gazpromo“. Atsakydama į tai, Rusija pastatė „Maršalą Vasilevskį“. Jo uždavinys – apsaugoti Kaliningradą tuo atveju, jei Lietuva surengs dujų blokadą.

Lietuva su „Gazpromu“ yra pasirašiusi tranzito kontraktą iki 2025 metų ir tvarkingai ją vykdo. O „Maršalas Vasilevskis“ plaukioja po visą pasaulį – gabena SGD kitų šalių vartotojams. Kam reikia be reikalo stovėti uoste?

Ir čia, kaip perkūnas iš giedro dangaus, trenkė naujiena, kad laivas su stambia krovinio partija grįžta į gimtąjį uostą. Lietuva įtarė negerą: kodėl Kaliningradui reikalingos SGD, jei jis aprūpinamas vamzdynų dujomis? Ar tik nesiruošia Rusija uždaryti šią magistralę?

Situacija komentavo asmeniškai Lietuvos premjerė Ingrida Šimonytė.

„Aš nesakau, kad tai būtinai turi įvykti, bet faktas tame, kad mes turime būti pasiruošę“,- sakė Šimonytė.

Kiek vėliau pasirodė informacija, kad Vilnius parengė kokį tai planą tam atvejui, jei bus nutrauktas dujų importas iš Rusijos. Energetikos ministro Dainiaus Kreivio atstovė spaudai Vita Ramanauskaitė nurodė, kad „Lietuvos priimti strateginiai sprendimai dėl gamtinių dujų tiekimo šaltinių diversifikavimo ir gamtinių dujų sistemų integracijos – SGD terminalas Klaipėdoje ir greitai pradėsianti veikti Lietuvos–Lenkijos dujų jungtis – leidžia mums užsitikrinti gamtinių dujų tiekimą nepriklausomai nuo Rusijos pusės veiksmų“. Visiškai laukiamas pareiškimas: grynai techniškai Lietuva jau seniai yra pasirengusi būti atjungtai nuo rusiško vamzdžio. SGD terminalo jai pilnai užteks (galima patenkinti visų trejų Pabaltijo respublikų poreikius). Klausimas tame, kiek prisieis už tai užmokėti.

Kaliningradui, tarp kitko, taip pat.

„Atsižvelgiant į dabartines aukštas SGD kainas – daugiau $1 tūkstantis dolerių už 1 tūkstantį kubinių metrų – „Gazpromo“ negauta nauda dėl SGD tiekimo Kaliningradui bus didelė. Taip, remiantis rinkos dalyvių vertinimu, vieno tanklaivio krovinys į Kaliningradą „Gazpromui“ apsieina maždaug $90–100 milijonų negautų įplaukų“,- pažymi „Komersantas“.

Nei Lietuva, nei „Gazpromas“ nesuinteresuoti organizuoti kokias tai blokadas. Bet pastarasis veikia, remdamasis principu: „Atsarga gėdos nedaro“.

„Maršalas Vasilevskis“ į Kaliningradą sugrįžo, peržengusios visa galimas ribas, antirusiškos isterijos fone.

„SGD atsargos užtikrina regiono energetinį nepriklausomumą“,- pažymėjo Kaliningrado vyriausybės atstovas spaudai Dmitrijus Lyskovas. Kaip nekeista, bet panašios nuomonės laikosi ir Lietuvos energetikos eksministras Arvydas Sekmokas: „Yra du variantai. Pirmasis variantas – tai paprasčiausiai užplanuotas reisas. Tačiau esant dabartinėm geopolitinėm aplinkybėm, negalima atmesti, kad to tikslas – užtikrinti dujų tiekimą Kaliningradui. (...) Tai būtų galimu paaiškinu tuo, kad laivas –dujų vežėjas gražinamas, kad apsisaugoti nuo galimų Lietuvos arba NATO veiksmų“.

Pati situacija nėra nauja. 2019 metais Rusija atliko „Maršalo Vasilevskio“ veiklos patikrinimą ir laikinai sustabdė dujų tranzitą vamzdynu į Kaliningrado sritį. Lietuvius tai sunervino. Praeitų metų vasaryje, „Gazpromo“ prašoma, Lietuva vėl sustabdė tranzitą. Sprendžiant iš visko, rusiškame vamzdyno ruože buvo atliekami kokie tai techniniai darbai.

Kaip rodo praktika, ir Rusija, ir Lietuva vykdo savo dujų tiekimo kontraktinius įsipareigojimus. Tiesa, šį kartą potencialią grėsmę Kaliningradui sukelia ne tik Pabaltijo respublikos.

Iš Baltarusijos į Lietuvą nutiestas dujotiekio „Minskas – Vilnius – Kaunas – Kaliningradas“ vamzdynas. Juo dujos tiekiamos išimtinai tik į Lietuvą ir į Kaliningrado sritį.

Išnešime už skliaustelių teisėtumo klausimą ir kokios bus pasekmės, bet toks variantas teoriškai yra galimas. Ypatingai, jei atsižvelgti į tai, kad nuo vasario pirmos Lietuva žada nutraukti baltarusiškų trąšų tranzitą. Kas žino, kokį atsakymą į tai jai paruošė Batka? Jis jau grasino atrėžti rusiškų dujų tiekimą į Europą.

Taip, kad „Maršalas Vasilevskis“ į Kaliningradą atvyko pačiu laiku.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 12 — id: `scraped:rubaltic_lt:39506623e5c565f2`

**Title:** Smūgis Kaliningradui: Santykiuose su Rusija Lietuva priėjo prie lemiamos ribos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos užsienio politika sukelia grėsmę Kaliningrado sričiai. Tokia grėsme yra numatomas baltarusiškos kilmės prekių tranzito draudimas per Lietuvos teritoriją. Veikėjai iš Lietuvos panašias iniciatyvas pateikia siekdami savo politinių tikslų, negalvodami, jog žaidžia su ugnimi. Kaliningrado saugumas - tai ta lemiama riba, peržengus kurią, Lietuvos likimą spręs kitos šalys, kurios nėra suinteresuotos, kad kaimo kvaileliai iš Rytų Europos išprovokuotų Rusijos ir NATO karą.

Šiandieną Lietuvos politikai mėgsta kartoti, pagrinde dėl Ukrainos, jog Rusija neturi teisės įtakoti savo kaimynų suvereniam pasirinkimui: ar jiems įstoti į NATO ir Europos Sąjungą, ar ne. Tuo tarpu, pačios Lietuvos įstojimui į Europos Sąjungą Rusijos įtakojo tiesiogiai, ir Lietuvos politikai tada nusprendė „nesišakoti“, suprasdami, jog iki jų priėmimo į Europos Sąjungą jiems geriau patylėti.

Geografinis Kaliningrado srities atskyrimas nuo likusios Rusijos Lietuvos integracijos į Europos Sąjungą ir NATO sąlygomis, Europoje sukūrė situaciją, analogišką tai, kuri tapo Antrojo Pasaulinio karo pretekstu. Vakaruose negalėjo nepastebėti panašumo tarp „Dancigo koridoriaus“ ir Kaliningrado tranzito, juolab, jog kalbama praktiškai apie tas pačias vietoves.

XXI amžiuje atkurti vieną iš pagrindinių geopolitinių tarpukario Europos konfliktų šiuolaikinė Europa nenorėjo.

Tai yra, sutikti su tuo pačiu trišaliu formatu, kuriam Lietuva nuoširdžiai pasipiktinusi priešinosi, kai buvo kalbama apie Ukrainos asocijavimą į ES.

Rusijos, Lietuvis ir Europos Sąjungos trišalės derybos baigėsi susitarimu dėl supaprastinto tranzito geležinkeliu. Pagal savo esmę, kalbama apie supaprastintą tranzito Šengeno vizą, kurią Lietuva įsipareigojo vienos paros laikotarpiu nuo užkausimo iš Rusijos geležinkelio gavimo, išduoti Kaliningrado srities gyventojams, vykstantiems į „didžiąją Rusiją“.

Visų pirma, Lietuva iš karto savo pareigą išduoti tranzito vizas interpretavo kaip teisę. Esą, viza visgi - Lietuvos. Todėl kam norim tam ir išduodam, kam nenorim tam ir atsakom. Atsakymų skaičius didėjo kasmet ir tuo metu, kai Vilnius pradėjo visų aktyviausiai Europoje lobiuoti Europos Sąjungos sankcijas RF, jų skaičius pasiekė tūkstančius. Ištisos profesinės grupės – kariškiai, naftininkai – šiandieną negali geležinkeliu vykti iš Rusijos į Rusiją.

Antra, Vilnius pradėjo zonduoti tai, jog Lietuva gali atsisakyti savo tarptautinių įsipareigojimų, jei Rusija nevykdo savų. Pažymėtina, jog toks zondavimas buvo pradėtas dar iki „Krymo aneksijos“ bei kitų, su Ukrainą susiejusių, įvykių.

Trečia, Kaliningrado tranzitas tapo koziriu Lietuvos derybose su Briuseliu. Lygiai prieš dvejus metaus Lietuvos valdininkai jau davė suprasti, jog tuo atveju, jei bus sumažintas europietiškas dotavimas, Lietuva atsisakys savo sąskaita apiforminti tranzito vizas kaliningradiečiams.

Ketvirta, krovinių gabenime Lietuva išnaudoja visus galimus instrumentus, siekiant iš Kaliningrado atimti kuo daugiau tranzito krovinių ir juos nukreipti į Klaipėdą.

Penkta, Lietuvos politikoje Kaliningrado interesai principingai ignoruojami. Klasikiniai pavyzdžiai – Ignalinos AE uždarymas ir išėjimas iš BRELL (Baltarusija-Rusija-Estija-Latvija-Lietuva) žiedo, abu tie Vilniaus veiksmai sukėlė grėsmę Rusijos regiono aprūpinimui elektros energija ir, jei Rusija nebūtu sistemingai užsiėmusi savo eksklavo energetiniu saugumu, Kaliningradui būtu buvę riesta.

Būtent taip reikia interpretuoti Lietuvos seimo deputatų iniciatyvą uždrausti baltarusiškos kilmės prekių tranzitą per Lietuvos teritoriją, idant nors kaip tai kompensuoti „nuostolį“, susijusį su baltarusiškų kalio trąšu tranzitu per Lietuva.

Šioje situacijoje iniciatorius visiškai nedomina Kaliningrado sritis. Jų nedomina netgi Baltarusija su „diktatorišku režimu“ ir su kuriuo jie būk tai kovoja.

Juos domina tik tai, jog Lietuvos geležinkelis“ ir baltarusiška infrastruktūra Klaipėdos uoste maitina valdančios konservatorių partijos konkurentus – socialdemokratus ir Lietuvos valstiečių ir „žaliųjų“ sąjungą. Tam kad išmušti varžovų rinkimuose materialinę bazę ir buvo pradėtas visas tas triukšmas su sankcijomis „Beloruskaliui“.

Kartu su tuo demonstruojama vergiška ištikimybė JAV ir taip pat kartu su tuo įterpiama mintis apie tai, jog Kaliningrado srities saugumas priklauso nuo geros Lietuvos valios. Šiuo atveju kalbama apie priklausantį nuo maisto produktų saugumą, kadangi pagrindinis importas, kuris vežamas iš Baltarusijos į Kaliningradą – tai statybinės medžiagos ir maisto produktai.

2000 metų pradžioje Europa sutiko derėtis su Maskva apie Lietuvos narystės ES sąlygas, kada ir pačioje Rusijoje daugelis buvo įsitikinę, jog pati didžiausia pasaulio šalis štai subyrės. Dabartinė Rusija – supervalstybė turinti hipergarso ginklą, kuri daug kartų, aukščiau paminėtos Ukrainos pavyzdžiu, įrodė, jog veikti prieš jos interesus visiškai neapsimoka.

Ar ES „draskysis“ už Lietuvą, jei ta visgi įsivels į geopolitinį konfliktą su Rusija dėl Kaliningrado – klausimas nėra aktualus. Į jį buvo atsakyta prieš metus Baltarusijoje, kai dėl komjaunuoliško „jaunųjų europiečių“ – Lenkijos ir Lietuvos įkarščio, pagrindinės Vakarų šalys skambino į Kremlių Putinui ir kartojo, jog joms nereikalinga „antra Ukraina“. Pažymėtina, jog Baltarusija – ne Rusija, ir skambinti Rusijos prezidentui dėl jos vidaus politinės situacijos buvo iš viso didelis diplomatinis stačiokiškumas.

Kokiu būdu reaguos ES, jei Vilnius susigalvos šiuos susitarimus nutraukti ir dėl nieko Europos centre sukelti karinį-politinį konfliktą? Regis, Lietuvos išprotėjusiems uždės geopolitinius tramdomus marškinius ir įjungs jiems diplomatinį Šarko dušą.

Panašiai reaguos ir Vašingtonas, kuris dabar skuba baigti savo reikalus Ukrainoje ir mažina amerikiečių buvimo Europoje infrastruktūrą, idant sukoncentruoti visus resursus kovai su Kinija. Jei Vilniuje galvoja, jog JAV bus priverstos įsivelti į naują konfliktą su Rusija, kad paremti sąjungininkus iš Lietuvos, tai tikrovė jiems pasirodys kur kas griežtesnė.

JAV interese bus atsisakymas nuo šalies, kuri maišosi tarp kojų ir savo elgesiu sukelia problemas amerikiečiams.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 13 — id: `scraped:rubaltic_lt:8e042d232a631546`

**Title:** Išeiti iš Ukrainos ir įvesti  kariuomenę į Pabaltijį: JAV su Rusija prekiauja satelitais

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Rusų – amerikiečių derybas dėl saugumo garantijų lydi gana būdingi Džozefo Baideno administracijos žiniasklaidos ir ekspertų komentarai. Vieni ir tie patys amerikietiški resursai rašo apie tai, kad amerikiečiai turi pasitraukti iš Ukrainos, ir kad prezidentas Baidenas planuoja permesti keletą tūkstančių amerikiečių kariškių į Pabaltijį. Tokia situacija daro amerikiečių satelitus Rytų Europoje ciniško derėjimosi objektais, kur JAV, priklausomai nuo derybų su Maskva rezultato, yra pasiruošusios išnaudoti Ukrainą ir Pabaltijį kaip Rusijos užpuolimo placdarmą, ir juos atiduoti Putinui.

„Atsižvelgiant į dabartines realijas ir primygtinę būtinybę sukoncentruoti amerikietišką galią Rytų Azijoje pasipriešinimui Kinijai, tampa aišku, kur, ideale, gali baigtis mūsų atsitraukimas. Jis gali būti prie atidėto klausimo dėl NATO plėtros linijos; su Ukraina, kuri yra neišvengiamai spaudžiama Rusijos, bet be invazijos arba aneksijos, ir dar su sunkesne našta mūsų NATO sąjungininkams, palaikant saugumo perimetrą Rytų Europoje“, - rašo New York Times skiltininkas Ross Dautat.

Tai yra, atvirai sakant, visam laikui.

Todėl, kad „kokie bebūtu mūsų arba Ukrainos norai, jos valdžia tiesiog niekada negalėjo visiškai prisijungti prie Vakarų – ji per daug silpna ekonomiškai, per daug susiskaldžiusi viduje, ir tiesiog randasi ne toje vietoje ir ne tuo laiku“.

Pačioje Ukrainoje tokį požiūrį vadina „на тобі, убоже, що нам не гоже“ (štai tau dieve tai, kas mums nereikalinga). Nezaležnja Jungtinėms Valstijoms – toksiškas aktyvas, tegul Putinas ją ir pasiima.

Žinoma, negalima teigti, kad tokios publikacijos vyrauja vakarų publicistikoje.

JAV prezidentas Džozefas Baidenas nagrinėja galimybę dislokuoti Baltijos šalyse amerikiečių aviaciją, laivyną ir pėstininkus, – remdamasis savo pašnekovais, rašo vis tas pats New York Times. Tokį sprendimą jis gali priimti iki šios savaitės pabaigos.

Kas yra tie laikraščio, kuris faktiškai yra JAV Demokratų partijos informacinis sparnas, pašnekovai, galima netikslinti. Ir čia yra svarbu tai, kad tie patys Baltųjų rūmų pareigūnai, kurie teikia savo partijos ruporui informaciją apie, būk tai jų turimą planą permesti iki penkių tūkstančių amerikiečių kariškių į Pabaltijį, praleidžia medžiagą, kuri faktiškai ruošia Amerikos visuomeninę nuomonę, kad Ukraina bus atiduota Putinui.

Suprantama, kad ir ta, ir kita New York Times medžiaga – tai signalai Rusijai. Tai netgi jaučiama tekste. „Šis žingsnis [JAV kariškių permetimas į Pabaltijį] Baideno administracijai, kuri iki pastarojo meto laikėsi santūrios pozicijos Ukrainos atžvilgiu, taps kertiniu momentu“,- pareiškia New York Times šaltinis.

Klausimas, kodėl tie signalai tokie prieštaringi? Tai atsitrauksime nuo Ukrainos, tai nusiūsime 5 tūkstančius į Pabaltijį. Koks gali būti šių dviejų nuorodų bendras vardiklis?

Tik vienas.

Tarp kitko, antrąjį scenarijų stumia toli ne marginalai. New York Times, USA Today, Forbes, National Interest… jų autoriai – Amerikos ekspertų žiniasklaidoje elitas, plačiąją prasme yra politinio elito dalimi. Ir štai, šis elitas, gerų, užimančių aukštas valstybines pareigas pažįstamų prašomas, stumia „urbi et orbi“ paprastą mintį: Rytų Europa – Amerikos imperijos periferija, o dabar svarbiausia sustabdyti Kinijos stiprėjimą, todėl, esant tam tikroms Putino garantijoms dėl tos pačios Kinijos, savo sąjungininkus Rusijos pasienyje galima ir reikia paaukoti.

Kartu su tuo, kad Putinas būtų sukalbamesnis, galima išnaudoti tų teritorijų geopolitinį potencialą ir prigrasinti kariuomenės telkimu Rusijos pasienyje.

Pačios teritorijos ir jų ateitis šiame žaviame derėjimosi su Maskva dėl Kinijos procese amerikiečių visiškai nedomina. Lenkijai, Ukrainai arba Baltijos šalims apmaudžiausiai yra tai, kad jos čia negali niekuo skųstis. Jos pačios išsirinko sau funkciją „ko pageidaujate“ ir savo užsienio ir, daugelių atvejų, vidaus politiką pavertė JAV interesų tarnaite.

Priimkite ir pasirašykite.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 14 — id: `scraped:rubaltic_lt:d1084bf18ce2464a`

**Title:** Putinas legitimus: Europa atsisakė remti Ukrainos ir Lietuvos rusofobiją

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Ukrainos deputatų iniciatyvą pripažinti Rusijos prezidentą Vladimirą Putiną nelegitimiu palaikė 23 deputatai iš 652 Europos Tarybos Parlamentinės Asamblėjos (ETPA) narių. Didesnė palaikiusiųjų pusė – pačios Ukrainos ir Pabaltijo šalių delegatai. Absoliuti europiečių dauguma eilinę Ukrainos ir Pabaltijo iniciatyvą ignoravo.

Keleto ES šalių atstovai palaikė kreipimąsi į Europos Tarybos Parlamentinę Asamblėją dėl prašymo įvertinti Vladimiro Putino legitimumą, jei jis 2024 metų rinkimuose bus perrinktas prezidentu. Apie tai pranešė Ukrainos delegacijos narys, Aukščiausios Rados deputatas Aleksėjus Gončarenko.

„Tik ką dabar, kartu su Lietuvos delegacijos vadovu Emanueliu Zingeriu, pateikėme dokumentus ETPA sekretoriatui. Mus palaikė deputatai iš Estijos, Didžiosios Britanijos, Airijos, Vokietijos, Lietuvos, Latvijos, Ukrainos, Azerbaidžano“,- savo Facebook puslapyje parašė Gončarenko.

Dokumentas apie kurį kalbama, - tai siūlymas priimti rezoliuciją («motion for a resolution»). Tekstą ruošė Vladimiras Kara – Murza, žinomas rusų opozicionierius-liberalas ir Boriso Nemcovo Fondo tarybos už laisvę (Rusijoje pripažintos nepageidaujama organizacija) pirmininkas. Jis piktinasi tuo faktu, kad 2020 metais į Rusijos Konstituciją buvo įtraukta pataisa dėl Putino prezidentavimo terminų „nurašymo“. Tokiu būdu, veikiančiam prezidentui buvo suteikta galimybė būti perrinktam dar dvejom kadencijom (iki 2036 metų).

„Venecijos komisija pažymėjo, kad kai kurios pataisos prieštarauja Konstitucijos nuostatoms. Todėl mes raginame Europos Tarybos Parlamentinę Asamblėją išklausyti pranešimą, kad išsiaiškinti klausimą dėl Putino prezidentavimo kadencijų nurašymo legitimumo/nelegitimumo, o taip ir būsimo Rusijos prezidento įgaliojimų teisėtumo iš principo“, - rašo Gončarenko.

Kaip sakomas, be manęs jie mane vedė...

Kad būti įtikimesniu, Ukrainos delegacijos narys išvardijo net aštuonias šalis, kurių atstovai pasirašė kreipimąsi ETPA sekretoriatui. Tarp jų yra netgi Didžioji Britanija ir Vokietija. Gavosi solidus sąrašas.

Iš kitos pusės, iš 652 asamblėjos deputatų dokumentą pasirašė tik 23, tame tarpe šeši ukrainiečiai ir aštuoni pabaltijiečiai. Pageidaujančių sudaryti jiems kompaniją eilės tikrai nebuvo.

Gal būt stebina tai, kad jų tarpe visiškai nėra lenkų.

Pati idėja įvertinti Putino legitimumą nėra nauja. Tik prieš keletą mėnesių iki to prisigalvojo amerikiečių kongresmenais – jie paruošė rezoliucijos projektą, kuriuo siūloma nepripažinti veikiančiojo RF prezidento įgaliojimų po 2024 metų, jei jis laimės rinkimus.

„Šį kartą amerikiečiai ankstokai pradėjo kištis į Rusijos prezidento rinkimus. O taip, daugiau nieko naujo ir nieko netikėto. Grynas kišimasis į mūsų vidaus reikalus. Ir dar provokacija, siekianti sužlugdyti pradėjusį ryškėti abipusių santykių (Rusijos ir JAV - RuBaltic.Ru pastaba) normalizavimą“, - situaciją komentuoja Federacijos Tarybos spikerio pavaduotojas Konstantinas Kosačiovas.

Jokio praktiško jų iniciatyvos pritaikymo, suprantama, nebus. Europa nesiruošia statyti į vieną eilę Kremliaus šeimininką su Aleksandru Lukašenka.

Teigiamas ETPA sprendimas šiuo klausimu atvertų Putino nepripažinimo legitimiu RF prezidentu vartus. Taigi, ES turės nutraukti visus kontaktus su Kremliaus šeimininku ir jo paskirtai asmenimis. Tai dar labiau neįtikimimas scenarijus negu Rusijos atjungimas nuo SWIFT arba Europos atsisakymas rusiškų dujų.

Ar tai supranta Aleksėjus Gončarenko? Supranta. Jo draugai iš Pabaltijo taip pat „temoje“ – jie puikiai žino, kokios nuotaikos vyrauja ETPA, Europos parlamente, Europos komisijoje bei vedančiose Bendrijos šalyse.

Bet jie ir nesiekia tikslo sukelti abejones dėl Putino įgaliojimų po 2024 metų. Svarbiausiai – surengti politinį performansą.

„Kaip mes suprantame, „Rusiją gražindavo“ į ETPA dialogui. Bet jo iš viso nebuvo. Vietoj to, ji per savo atstovus pareiškia, kad jiems „nusispjauti“ į šios gerbiamos tarptautinės institucijos, iš esmės, pirmos pokario metų Europos parlamentinės asamblėjos, nuomonę. Todėl mums svarbiausia– dienotvarkėje pastoviai remti Krymo ir rusiškos agresijos temą. Mes liekame Ukrainos interesų forpostu. Mums Rusija – tai šalis - agresorius, šalis, su kuria mes kariaujame jau septintus metus. Kontaktų su RF atnaujinimas, o taip pat bendradarbiavimo atkūrimas, kaip apie tai jie pareiškia, yra galimas tik po visų okupuotų Ukrainos teritorijų gražinimo, demilitarizavimo ir teisingų kompensacijų išmokėjimo“,- prieš metus kalbėjo Ukrainos delegacijos ETPA vadovė Marija Mezenceva.

Pasakyta tiesiai ir atvirai: mums svarbiausia Rusija. Kitų problemų, kurias Kijevas galėtų pateikti nagrinėti Europos Tarybai, ne egzistuoja.

Tradiciškai Ukraina ir Lietuva (atstovaujamos deputatų Eugenij Kravčuk ir Emanueliu Zingeriu) bando užginčyti Rusijos delegacijos įgaliojimus. Tas pats vyko 2020 ir 2021 metais. Šios medžiagos rengimo momentu pasirodė ETPA monitoringo komisijos išvada: „Parlamentinė asamblėja yra vienintelė visos Europos parlamentinė visų Europos šalių politinio dialogo aikštelė. Todėl ji (monitoringo komisija - - RuBaltic.Ru pastaba) siūlo asamblėjai ratifikuoti Rusijos Federacijos delegacijos įgaliojimus ir sugrįžti prie pranešime, kuris bus pateiktas vėliau metu laike, pasiekto progreso įvertinimo“.

Nesuspėjo asamblėja patvirtinti RF delegacijos įgaliojimus, kai Gončarenko ir kompanija iškėlė abejojimą dėl Putino legitimumo. „Nezaležnos“ žiniasklaida dabar pasakos apie „triuškinantį smūgį“ , kurį Maskva gavo iš ETPA.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 15 — id: `scraped:rubaltic_lt:8e7b45da7f454851`

**Title:** Pasitelkiant į pagalba SGD terminalą: Lietuva moko Moldovą „energetinės nepriklausomybės“ nuo Rusijos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos Seimo pirmininkė lankėsi Kišiniove ir pasidalino Lietuvos kovos už „energetinę nepriklausomybę“ nuo Rusijos patirtimi su Moldovos prezidente Majai Sandu. Jei Sandu santykiuose su Rusija paseks Lietuvos patarimais, tai Moldova ne tik negaus geros dujų kainos, bet ir visiškai sužlugdys visas galimybes susitarti su „Gazpromu“ ir, savo intrigantiškumo dėka, rusiškas dujas pirks iš trečiųjų rankų už tris kartus brangesnę kainą. Todėl, kad Lietuva yra pati paskutiniausioji šalis pasaulyje, kuri gali bet ką mokyti konstruktyvaus politinio dialogo su Maskva.

Maja Sandu ir Viktorija Čmilytė-Nielsen pasikeitė Moldovos ir Lietuvos požiūriais į regiono saugumą ir aptarė tuos iššūkius, su kuriais šiandieną susiduria Kišiniovas. Pagrindinis iš iššūkių – energetinis.

Moldovoje kiekvieną mėnesį kyla pinigų stokos apmokėjimui už rusiškas dujas krizė. Nekalbant jau apie moldavų įsiskolinimo už dujas apmokėjimą, dėl kurio Kišiniovas beviltiškai bando kažką tai sugalvoti, kad pateisinti savo atsisakymą gražinti „Gazpromui“ tą skolą.

Todėl Lietuvos Respublika nusprendė būtinu pasidalinti savo vertinga kovos už „energetinę nepriklausomybę“ nuo Rusijos patirtimi. Apie duotų Kišiniovui patarimų „vertę“ galima spręsti pagal vieną iš jų, kuriuos pagarsino Sandu kanceliarija.

Lietuvos Seimo pirmininkė moldavams rekomendavo plėsti „žaliąją energetiką“. „Genialus“ patarimas – atsižvelgiant į tai, kad nuo praeitų metų rudens visą šią temą su atsinaujinančiais energijos šaltiniais pasaulinė energetinė krizė „padaugino iš nulio“.

Šis patarimas ypatingai „aktualus“ Moldovai, kuri nesugeba užsimokėti ir už šiandieną patį pigiausią rinkoje energijos šaltinį – rusiškas vamzdynų dujas, o jai siūloma alternatyvi „žalioji energetika“, kuri yra per brangi netgi turtingoms vakarų šalims.

Tarp kitko, Lietuvos politikai, mokydami kovoti už „energetinę nepriklausomybę“, Moldovą gali išmokyti ir ne tik to.

Lietuva būtent taip ir padarė. Uždarė Ignalinos AE, dėl ko padarė „Gazpromą“ Lietuvos energetikos rinkos monopolistu. Nuo to laiko Lietuvos vadovai gali rašyti knygas ir skaityti paskaitas tema „Kokiu būdu herojiškai įveikti sunkumus, kurios patys sau susikūrėme“.

Tarp kitko, Moldovoje nėra AE, kurią galima būtų iškilmingai likviduoti, kaip “sovietų okupacijos“ paveldą. Reikia iš karto pereiti prie antrojo etapo: kaip susitarti su „Gazpromu“ dėl naudingos dujų kainos?

Ką čia gali patarti Lietuva, turinti turtingą sąveikos su rusišku monopolistu patirtį?

Lygiai tokiu keliu ir žengė Lietuva. Kad išplėšti sau geresnę kainą, ji paskelbė „Gazpromo“ rinkos kainą politiškai motyvuota, „Gazpromą“ padavė į Stokholmo Arbitražą dėl piktnaudžiavimo monopolija, aštuonerius metus bylinėjosi ir visuose instancijose pralošė.

Jei Moldova paseks Lietuvos pėdomis, tai įsiskolinimus „Gazpromui“ vis vien prisieis mokėti, tik dar kartu su skolomis teks apmokėti ir teismo išlaidas. Kartu su tuo politiniai santykiai su Rusija bus sugriauti. Rusijos valdžia neatleis, kad dėl ūkinių klausimų sprendimo, ją įtraukė į politines spekuliacijas.

Šioje vietoje Lietuvos energetinės politikos „advokatai“ būtinai prisimena lietuvišką SGD terminalą, esą, kurio atsiradimo dėka rusiškų dujų kaina respublikoje krito 20%. Bergždžias darbas jiems aiškinti, kad dujų kainą nukrito dar prieš pusmetį iki to, kai į Klaipėdą buvo atgabentas SGD terminalas, taip, kad šio atpigimo priežastimi jokiu būdu negali būti energetinės alternatyvos „Gazpromui“ atsiradimas Lietuvoje. Kitų argumentų „Lietuvos „patriotai“ vis vien neturi – todėl su buku atkalumo jie juo ir remiasi.

Tarp kitko, paskutiniu metu apie savo „energetinės nepriklausomybės stebuklą“ SGD terminalo pavidale Lietuvoje stengiasi nešnekėti.

Kišiniove, taip sakant, pasakojimu apie Independence irgi pasigyrė.

Kas gi pasikeitė?

Visų pirma, SGD energetika JAV išėjo iš mados ir Vašingtone neteko savo lobistų. Dabartiniu metu vyraujantieji JAV Kongrese demokratai siūlo uždrausti frekingą – hidraulinio skaldymo būdą skalūnų dujoms išgauti.

Atitinkamai, Amerikoje ir Europoje SGD terminalai jau nebereikalingi. Gi tai buvo amerikiečių projektas: pati Lietuva sau išsinuomavo Independence ir, rekomenduojant NATO Energetinės nepriklausomybės centrui Vilniuje, agitavo visą Europą padaryti tą patį. Skaityk – amerikiečiams reikalaujant.

Dabar Klaipėdoje sėdi prie suskilusios geldos.

Antra, dabartinė energetikos krizė SGD temą uždarė ilgam laikui. Esant sąlygoms prie kurių nėra prieinamas netgi pats pigiausias energijos šaltinis – vamzdynų dujos iš Rusijos, nėra ko galvoti apie „žaliąją energetiką“ bei SGD terminalus.

Trečią, netgi tada, kai dujų kaina buvo nepalyginama su dabartine, Lietuva negalėjo išlaikyti SGD tiekimo iš JAV, Kataro ir Norvegijos naštos. Kad SGD terminalas Independence nebankrutuotu, prisiėjo (pradžioje netgi slaptai) SGD jam pirkti... iš Rusijos. Bingo! Rusiškų dujų alternatyva tapo rusiškos dujos!

Pagrindinis čia, žinoma, visų santykių su Rusija sugriovimas. Lietuvos politinė klasė šioje srityje iš tikrųjų dideli meistrai, to jie tai tikrai išmokys.

Pas moldavus iš tikrųjų yra tik viena reali išeitis iš dujų krizės – jų politinės vadovybės dialogas su Rusijos vadovybe. Šiuo atžvilgiu jiems pavojingiausia yra tai, kad prezidentė Maja Sandu, vietoj to, kad bendrauti su vienintele šalimi, kuri gali išspręsti Moldovos problemą, tariasi su pačia paskutiniausiąją šalimi pasaulyje, kuri gali bet ką mokyti konstruktyvių santykių su Maskva.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 16 — id: `scraped:rubaltic_lt:be9766eb0c22157f`

**Title:** Vokietija jau ne tokia: Trečiojo reicho „teutonų dvasios“ nostalgija Pabaltijyje

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Pabaltijyje piktinasi Vokietijos atsisakymu aktyviai dalyvauti Rytų Europos NATO šalių kolektyviniame Rusijos „suturėjimo“ procese. Tą pasipiktinimą viešai išreiškia politikai, kurie neslepia savo simpatijų naciams arba yra kilę iš šeimų, kurios bendradarbiavo su nacių okupantais. Jiems, žinoma, skaudu ir apmaudu, kad Raudonoji Armija nulaužė sprandą tai Vokietijai, su kuria jie galėtų eiti į eilinį žygį į Rytus ir tapti „nepilnaverčių slavų“  prižiūrėtojais-policajais.

Lietuvos respublikos Užsienio reikalų ministras Gabrielius Landsbergis pareiškė, kad 16 metų Vokietija buvo Europos ir jos kaimynų saugumo garantu, tačiau, dabartiniai signalai iš Berlyno, kuris atsisakė tiekti Ukrainai letalinį ginklą, verčia suklusti. URM vadovas viliasi, jog reikalas tik tame, kad nauja Vokietijos vyriausybė tik pradėjo dirbti, ir, kai tik apsipras, dar pakeis savo politiką,.

„Tai ką mes matome – tai kalbos, kuriomis Vokietija bando apsispręsti kaip reaguoti į dabartinę situaciją. Aš esu kantrus ir raginu jus būti kantriais“,- sakė Landsbergis.

Mažiau diplomatiškai pasisakė Europos parlamento deputatas iš Estijos Jaak Madison.

„Šiuo momentu Vokietijos vyriausybė pasirinko Vladimiro Putino dujas ir Ukrainą paliko neapgintą nuo rusiškos agresijos“,- parašė Madisan, smogdamas VFR puikia savo paniekos fraze apie tai, kad vokiečiai pirmenybę teikia ne Europos saugumui, o šilumai kambaryje.

Atsargia Berlyno pozicija dėl eilinio paaštrėjimo aplink Ukrainos nėra patenkinti daugelis „aktyvaus Kremliaus suturėjimo“ politikos apologetų, bet mažai kas rizikuoja tą nepasitenkinimą pareikšti atvirai. Visgi, Vokietija – tai stambiausia ES šalis ir pagrindinis Pabaltijo ekonomikų dotacijų donoras.

Tuo įdomiau pasižiūrėti, kas yra tos nedidelės išimtys, kurios ryžtasi pasisakyti dėl vokiečių silpnumo ir neryžtingumo. Ką bendro turi Gabrielius Landsbergis iš Lietuvos ir Jaak Madison iš Estijos?

„Atskiras klausimas –  hitlerinės Vokietinos nacionalsocializmas. Bet ir šiuo atveju

girdisi vien tik negatyvas. Taip, tiesa, buvo koncentrinės stovyklos, darbo stovyklos, žaidimai su dujų kameromis, bet tuo pačiu metu, taip vadinama „griežta“ tvarka ištraukė Vokietiją iš  bedugnės š**nos, kadangi šis progresas, kuris iš pat pradžios rėmėsi karinės pramonės vystymusi, per kelis metus šią šalį padarė viena iš pačių galingiausių šalių Europoje“,- rašė tolimais 2015 metais būsimasis Europos parlamento deputatas iš Estijos Jaak Madison.

Jo nuomone „fašizme mes stebime ideologiją, kurią sudaro pakankamai daug teigiamų ir būtinų nacionalinės valstybės išsaugojimui niuansų“. Suprantama, kodėl šiuolaikinė Vokietija Europos deputatui taip stipriai nepatinka.

VFR tokia „nuostabi“ ideologija yra skaitoma nusikalstama ir už ją sodina į kalėjimą.

Kas liečia Gabrielių Landsbergį, tai jo prosenelis Vytautas Landsbergis-Žemkalnis buvo, 1941 metais sudarytos Trečiojo reicho pakalikais, kurie tikėjosi gauti Lietuvos valstybės nepriklausomybės pripažinimą iš „gerojo fiurerio“ Adolfo Hitlerio rankų, Laikinosios Lietuvos vyriausybės narys. Laikinosios Lietuvos vyriausybės komunalinio ūkio ministras Landsbergis – Žemkalnis buvo Gestapo agentas ir sutriuškinus „gerąjį fiurerį“, kartus su kitais kolaboracionistais pabėgo į Australiją.

Australijoje paaiškėjo, kad jis dar buvo ir NKVD agentu. Landsbergis – Žemkalnis sovietų specialioms tarnyboms išdavė savo bendražygius, už ką buvo amnestuotas ir gavo Lubiankos leidimą grįžti į Lietuvą. Žinoma, Lietuvos TSR patriotu jis netapo: jau jo sūnus – dabartinio URM vadovo senelis Vytautas Landsbergis, atsiradus pirmąją galimybei, ėmėsi vadovauti antisovietiniam judėjimui, kad užbaigti savo tėvo darbą, kuris nesėkmingai pastatė ant Adolfo Hitlerio.

Toks žmonių, nepatenkintų šiuolaikine Vokietija, kuri nenori remti NATO ir Rusijos santykių įtampos, „praeities šleifas“  daug ką paaiškina.

Raudonoji Armija nulaužė sprandą  teutonų galiai ir išmušė iš vokiečių „teutonų dvasią“. Patys vokiečiai su tuo jau seniai susitaikė, ir nuo 1945 metų  ant buvusios Vokietijos griuvėsių stato naują, neturinčią nieko bendro su „tūkstantmetiniu Reichu“, Vokietiją.

O štai su nacių pakalikais Rytų Europoje, pasibaigus Antrajam pasauliniam karui, sovietai su amerikiečiais kažko tai nepadarė. Pirmieji – kad nesudrumsti sovietų tautų draugystę, antrieji – kad spręsti savo ciniškus klausimus šaltajame kare.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 17 — id: `scraped:rubaltic_lt:d5166bc2ba70ea62`

**Title:** Kinija privers Lietuvą ieškoti būdų susitaikyti

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Prezidentui Gitanui Nausėdai pareikalavus, Lietuvos užsienio reikalų ministerija parengė kokį tai santykių su Kinija normalizavimo planą. Šio dokumento detalės neviešinamos, bet jo autorius Gabrielius Landsbergis pabrėžia, jog Vilnius nėra pasiruošęs jokioms nuolaidoms. „Genialaus“  Lietuvos URM plano esmė tame, kad teisminiais ieškiniais išgąsdinti kinus ir priversti juos kapituliuoti. Bet kol kas arčiau kapituliacijos randasi Lietuva, kuri patiria vis daugiau nuostolių dėl tarptautinio konflikto ir priversta ieškoti santykių su Padangių šalimi normalizavimo būdų.

Kinų laikraštis South China Morning Post, remdamasis  KLR Vyriausiosios muitinės valdybos duomenimis pademonstravo Kinijos prekybos dinamiką su Lietuva.

Visiškai kitokius duomenis kažkodėl tai  pateikė Lietuvos Statistikos departamentas. Jei tikėti juo, praėjusių metų lapkrityje iš Lietuvos į Kiniją išvežta prekių už 20,3 milijono eurų.

Kuo tai galima paaiškinti? Galimai, Vilnius ir Pekinas naudoja skirtingus apskaičiavimo metodus, pastarasis įskaito dar ir lietuviškų prekių reeksportą.

Bet kokiu atveju, Lietuva jau gavo nemalonią kinų kalėdinę dovaną. Atsižvelgiant į tai, kad Taivano atstovybė Vilniuje buvo atidaryta lapkričio 18, tai yra logiška.

Tolimesnių nuostolių skaičiavimo ėmėsi Lietuvos Centrinis bankas. Remiantis jo vertinimu, ekonominis Padangių šalies spaudimas gali sumažinti BVP augimą nuo 0,5% 2022 metais iki 1,3% 2023 metais.

Kai kurios ūkio šakos patirs labai didelius nuostolius. Taip, pavyzdžiui, maždaug 30% Lietuvoje pagamintų lazerių eksportuojama į Kiniją, o beveik 70% importuojamų amino junginių ateina iš Kinijos.

Vienas iš lazerių gamybos kompanijos Brolis Group įkūrėjų Kristijonas Vizbaras atvirai pasisako, kad jo verslą paaukojo „orientuotai į vertybes“ Lietuvos užsienio politikai.

„Ta situacija galutinai paaiškėjo: užsienio reikalų ministras [Gabrielius Landsbergis]  gana tiesiai pasakė, kad situacija su Kinija ir Europos Sąjunga nesikeis. (...) Tiek automobilių, tiek lazerių sektorius, kuris nori dirbti per globalias tiekimo grandines, mes negalime ignoruoti to fakto, kad Kinija tose grandinėse dominuoja. Ir jeigu negalime parduoti savo gaminių komponentų, nei tiesiogiai nei netiesiogiai, mes šioje geografinėje vietoje negalime vykdyti veiklos“, – kalbėjo Vizbaras.

Jei situacija nesikeis, Lietuvos aukštų technologijų kompanijos ieškos plėtros galimybių kituose šalyse. Brolis Group jau planuoja investuoti 50 milijonų eurų į naujų gamyklų statybą už Pabaltijo respublikos ribų.

Analogiškus planus pagarsino durpių substratų gamintojo Klasmann Deilmann įmonių grupės Lietuvoje generalinis direktorius Kazimieras Kaminskas: „Mūsų įmonei iš Lietuvos Kinija sudarė apie 15 proc. pardavimų. Tikrai nenorime to atsisakyti, tad gausime iškelti tą dalį produkcijos į kitas ES šalis... Lietuvoje buvome suplanavę tam tikrą plėtrą, bet dabar planuojame tai daryti Latvijoje“. „Dabar žiūrime vietas, kur galime dalį veiklos perkraustyti. Kaip jau bus, taip jau bus, bet tikrai norime veikti kitoje Europos Sąjungos šalyje, kadangi Lietuva vienintelė iš 27 Europos šalių turi jau nebe globalią rinką. Turime globalias laisves, judėjimo laisvę, bet mes ekonomiškai esame apriboti“, – samprotavo neaustinių medžiagų fabriko vadovas Stanislovas Grušas. Bendrai pasakius, valstybės parama vietoje kinų rinkos praradimo verslininkams nėra patraukli. Tuo pačiu metu Lietuvos ekonomiškos ir inovacijų ministrė Aušrinė Armonaitė praveda konferenciją: „ Darbo jėgos trūkumas – bręstantis iššūkis Lietuvos ekonomikai. Ką darome, kad talentų būtų daugiau?“ Tai skamba kaip pasityčiojimas iš kompanijų, kurios tapo neoficialių kinų sankcijų aukomis.

Spręsti Vilniaus problemas ES nesirengia. Gabrielius Landsbergis jau, tikriausiai, pavargo belstis į uždaras duris ir tvirtinti apie visos Europos atsakymo Kinijai būtinybę.

Laikraštis Financial Times, remdamasis savo šaltiniais praneša, kad netgi oficialūs JAV atstovai siūlo Lietuvai pakeisti Taivano atstovybės pavadinimą. Ir Baltieji rūmai, ir Pabaltijo respublikos URM, šią informaciją neigia, bet be ugnies nėra dūmų.

Prezidento iniciatyva URM vadovas jau parengė kokį tai konkretų planą.

„Turime kreipti dėmesį ne tik į darbą su mūsų partneriais, sąjungininkais, bet taip pat ir įgyvendinti deeskalacijos planą, kurio aš paprašiau iš gerbiamo užsienio reikalų ministro Gabrieliaus Landsbergio, jis man buvo pateiktas ir tikiuosi, kad šį planą mes galėsime ateityje įgyvendinti“, –  teigė G. Nausėda.

Kame šio plano esmė? Konkrečios dedatės negarsinamos, net Landsbergis truputi atskleidė paslapties uždangą: „Yra tiesiog tam tikros kryptys, diskusijos, kuriomis galima kalbėtis su mūsų kolegomis, pavadinkime, Pekine. Mes esame tam tikrų pasvarstymų perdavę per Europos institucijas ir patys tiesiogiai, bet, kaip ir minėjau susitikimo metu, deeskalacija didele dalimi priklauso nuo tų, kurie situaciją yra pasirinkę eskaluoti“.

Išvertus iš diplomatų kalbos, tai reiškia, kad Lietuvos užsienio reikalų ministras tiesiogiai siūlo pradėti dialogą su Kinija, rasti kokį tai naują komunikacijų pagrindą. Pavyzdžiui, organizuoti valstybių viršūnių susitikimą – Landsbergis mano, kad tai yra gera idėja.

Bet kontaktai su Pekinu reikalingi išskirtinai tam, kad jam prigrasinti teisinėmis pasekmėmis už Pasaulio prekybos organizacijos (PPO) normų pažeidimą.

„Kontaktams su Lietuva Kinijos durys visada yra plačiai atvertos, ir, jei Lietuva iš tikrųjų nori esamą situaciją pakeisti geresne, jai reikia pademonstruoti Kinijai savo ketinimų nuoširdumą ir imtis praktiškų veiksmų“,- pareiškė oficialus Kinijos URM atstovas Čžao Liczian.

Labai aiški užuomina: pakeiskite Taivano biuro pavadinimą! Tada su jumis sėsime prie derybų stalo. Bet Landsbergis atkakliai ignoruos šį variantą.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 18 — id: `scraped:rubaltic_lt:b17312d9b6d05873`

**Title:** Plėšikai: tauta  žlugdo antirusiškas Lietuvos valdžios priemones

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Įkandin Lietuvos Latvijoje buvo sužlugdyta iškilminga priemonė, skirta kovos su „sovietų okupaciją“ metinėms pažymėti. Minia nušvilpė šalies prezidentą, kuris iškilmių metu iš tribūnos sakė kalbą apie Latvijos tautos herojišką kovą už laisvę, kuo paniekino paminklo sovietų disidentui atidarymo Rygoje iškilmes. Susidarė tendencija: prieš 31 metus Lietuvos ir Latvijos tautos lygiai savaitės laiko tarpo skirtumu stojo už barikadų – dabar jie lygiai savaitės laiko tarpo skirtumu reikalauja, kad nešdintųsi jų vadovybės.

Praeitą savaitę Rygoje buvo atidaromas paminklas sovietų disidentui Gunarui Astrai. Priemonė buvo suderinta su Barikadų dienų minėjimu, kuris Latvijoje švenčiamas sausio 20 dieną – Rygos OMONo šturmo 1991 metais Latvijos VRM pastato metinių proga, kai Rygoje žuvo penkeri žmonės. Dėl įvykių Rygos Rainio bulvare nebuvo sukurtas toks haliucinacinis kultas, kaip Lietuvoje dėl 1991 metų sausio 13 dienos įvykių prie Vilniaus televizijos bokšto, bet visgi, sausio 20 – ženklinė latvių politikos atminimo data.

Tačiau šiais metais Barikadų dienų minėjimas buvo gerokai sugadintas, o paminklo disidentui Gunarui Astrai atidarymas faktiškai sužlugdytas.

Sugėdintas prezidentas Levitsas, triukšmaujant miniai, sunkiai, bet baigė savo iškilmingą kalbą apie „Okupaciją ir Laisvę“, ir, lydymas įžeidžiamų šūkių bei garsaus švilpimo, pasitraukė nuo mikrofono. Suprantama, kad visos publikacijos apie priemonę Latvijoje ir užsienyje buvo pašvęstos įvykusiam incidentui, o ne tam, kad pademonstruoti, kaip Latvijoje gerbia ir įamžina kovotojo už latvių išlaisvinimą iš Sovietų priespaudos atmintį.

Propagandistinė priemonė buvo sužlugdyta.

„ Kokia tai prasme man gėda ir pažemintina stovėti čia ir klausytis, kaip tautos dalis, kuri klysta, kuri – iš karto matosi – okupantų tarnai, nori sužlugdyti šią priemonę, už kurią žuvo Gunars Astra. Ir aš raginu visus gerbiamus dalyvius, kurie švilpia, - eikite šalin iš čia. Gerbiamieji, jūs savo darbą jau atlikote. Leiskite gerbiamiems žmonėms padaryti tai, dėl ko mes visi čia susirinkome“, - iš tribūnos pareiškė nepatenkintas Latvijos teisingumo ministras Janis Bordans.

Tik ir betrūko „okupantų tarnų“ paminėjimo, kad Latvijos valdžios gėda visiškai išryškėtų. Pabaltijyje gi jau seniai išmoko: kai politikai nieko negali pasakyti savo pasiteisinimui, jie kalba apie „Kremliaus ranką“ ir „okupantus“.

Tik Teisingumo ministerijos vadovas susinervavęs susipainiojo savo parodymuose. Miniai jis suriko, kad latvių disidento atminimo akciją žlugdo vakcinavimo nuo koronoviruso priešininkai, ir tuoj pat pradėjo šūkauti apie „Kremliaus ranką“. Tai visgi kas reikalauja Latvijos vadovybę nešdintis iš valdžios: žmonės, kurie yra nepatenkinti kovos su COVID-19 pandemija metodais ir rezultatais, ar „okupantų tarnai“?

Vilniuje atsitiko lygiai tas pats, kas ir Rygoje. Konservatorių partijos ir jos valdančios koalicijos sąjungininkų ministrų iškilmingos kalbos buvo nutraukiamos negailestingu minios švilpimu ir šūkiais, raginančiais nešdintis iš tribūnos ir, iš viso, iš valdžios. Tiksliai taip pat, kaip ir Rygoje, valdžios šalininkai bandė pateisinti įvykusį, kad nepasitenkinimą reiškė ne paprasti žmonės, o „Rusijos penktoji kolona, naudingi idiotai ir bendruomenės vėžys“.

Tiksliai taip pat, kaip ir Rygoje, pagrindinė priemonė, skirta valstybinės „sovietų okupacijos“ ir „ okupacinių režimų nusikaltimų“ ideologijos įgyvendinimui faktiškai buvo sužlugdyta.

Ką bendro turi Latvijos ir Lietuvos valdžia su tokiomis nemaloniomis pasekmėmis sau, po susidūrimo su paprastais žmonėmis? Bendra – reitingas.

Lietuvos premjerės partiją – konservatorius – remia 10% Lietuvos Respublikos gyventojų, o už latvių premjero „Naujos vienybės“ partiją pasirengę balsuoti mažiau 8% Latvijos rinkėjų. Lietuvos vyriausybės veiklą neigiamai vertina 60% lietuvių, ir maždaug tiek pat latvių nepatenkinti Latvijos vyriausybės veikla.

Lietuvoje populiarus yra šalies prezidentas Gitanas Nausėda, kurį išrinko visa tauta ir jis yra vertinamas kaip nepopuliarios konservatorių vyriausybės alternatyva. Už tai Latvijoje prezidentą Egilą Levitsą išrinko ta pati parlamentinė koalicija, kuri suformavo vyriausybę, dėl ko „klouno, kurio mes nerinkome“ antireitingas sudaro rekordinius 60%.

Pirmųjų Pabaltijo respublikų asmenų nušvilpimą sausio mėnesį galima laikyti šių skaičių pasireiškimą garsu.

Pereinamosios turbulencinės epochos metu jų valdančioji klasė pasireiškia visiškomis menkystėmis, kurios sugeba tik kalbėti, ir tik dvejomis temomis: „sovietų“okupacija“ ir „rusiška grėsmė“. Efektingai kovoti su koronoviruso pandemija, kad žmonės galėtų laisvai išeiti į gatvę, arba siekti naudingų dujų kainų bei sulaikyti komunalinių tarifų didėjimą, Pabaltijo valdžia jau nebenori. Ir nebegali.

Rezultate turime tendenciją.

Ir jokiais tuščiakalbiais kliedesiais apie „Kremliaus agentus“, „penktąją koloną“ ir „okupantų tarnus“ šią tendenciją neužplepėti.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 19 — id: `scraped:rubaltic_lt:8efe78d6ece93ba9`

**Title:** Lietuva muš lietuvius, kad į ją atkreiptų dėmesį Vakarai

**Source:** rubaltic_lt (propaganda)

**Text:**

```
„Lietuvos geležinkelis“ painformavo Minską apie baltarusiškų trąšų tranzito sustabdymą. Lietuvos centrinis bankas paskaičiavo, kad dėl sankcijų „Belaruskaliuj“ šalis neteks apie 1% BVP. Klaipėdos meras perspėja apie masinius atleidimus iš darbo mieste, jei bus sustabdytas tranzitas iš Baltarusijos. Visa tai nemažina Vilniaus pasiryžimo šauti sau į koją. Kuo daugiau Lietuva praras dėl „pagristos vertybėmis“ šalyje valdančiųjų konservatorių užsienio politikos, tuo noriau jie daugins tuos praradimus. Remiantis jų iškreipta logika, savos šalies kankinimas - priemonė įrodyti JAV, ES, kad Lietuva – nėra niekam tikusi ES ir NATO dalyvė, ir jos verta pasiklausyti.

Ką gali tokia šalis kaip Lietuva: mažytė šalis be resursų, ir, galų gale, be žmonių, pasiūlyti savo vakarų sąjungininkams, jei ji nori būti pastebimu tarptautinės politikos dalyviu?

„Geopolitinio tilto“ tarp Rytų ir Vakarų variantas, kuris prieš 30 metų buvo siūlomas Pabaltijo šalims, jau seniai, kaip neaktualus, suglamžytas ir išmesta į šiukšlių dėžę. Jei Rytai ir Vakarai perspektyvoje ir bandys suartėti, tam jokių tarpininkų ir „tiltų“ jiems neprireiks.

Kad realiai būti naudingu Amerikai „Rusijos suturėjimo“ strategijoje, pas Lietuvą turi būti, nors ir kad, Lenkijos galimybes. Vilnius visomis išgalėmis stengiasi kovoti su rusiška įtaka Europoje, bet jėgų pakanka tik grėsmingiems pasisakymams. Todėl visas Vašingtono dėmesys – lenkams: būtent Lenkija yra skaitoma centriniu elementu Rusijos „suturėjimo“ sistemoje, ir, atitinkamai, „mylima amerikiečių žmona“.

Kas lieka dar? Būti geru kaimynu savo kaimynams, gyventi nei su kuo nesikivirčijant ir uždirbti vystant ekonominius ryšius su užsieniu? To nori paprasti lietuviai, bet jokiu būdu ne Lietuvoje valdantieji konservatoriai, kurių užsienio politikai, remiantis rinkėjų požiūriu į URM vadovą Gabrielių Landsbergį, pritaria 3% Lietuvos gyventojų. Bet „landsbergistams“ į tai nusispjauti: jų tikslinė auditorija randasi Vašingtone, o ne Lietuvoje, ir tą, už vandenyno sėdinčią auditoriją, visiškai nesudominsi Lietuvos draugystė su kaimynais, rūpinimasis savo interesais ir savo šalies praturtėjimu.

Todėl Vilniuje ir pažymima, kad remiasi ne interesais, o vertybėmis, kurios Lietuvai yra bendros su vakarų sąjungininkais. Tos vertybės – JAV globalinis dominavimas, prisidengiant kovos už žmogaus teises ir demokratiją lozungais įsikišimas į kitų šalių reikalus, kova su Rusija, su Kinija.

Principinė vertybių politika – tai ta pati niša, kurią gali užimti Lietuva, neturėdama aktyvios užsienio politikos resursų.

Mazochistinė Lietuvos užsienio politika paaiškinama būtent tuo. Vilniui reikia demonstruoti, jog vargšė alkana Lietuva nuo atsidavimo vakarų idealams netenka daug daugiau, negu jos turtingi ir sotūs sąjungininkai, bet, skirtingai nuo jų, ji ne siekia niekinančios naudos ir negalvoja, kiek apsieis principingumas be kompromisų.

Bet kas kitas į tai pasakytų, jog lygiai todėl Lietuva – varginga ir alkana, o jos sąjungininkai – sotūs ir turingi, kadangi tie sąjungininkai skaičiuoja savo naudą ir galvoja apie pasekmes.

Todėl Lietuva visų garsiausiai Europos sąjungoje ragino įvesti sankcijas Rusijai, visų daugiausiai nuo tų sankcijų nekentėjo – ir su pasididžiavimu prisipažino apie tai, iš Europos sąjungos pareikalavo papildomų kompensacijų Lietuvos pieno perdirbėjams, kuriems Rusija uždarė savo rinką.

Todėl lietuviškos kompanijos į Lietuvą veža kinų prekes apeinant – per Latviją, vokiečių investoriai perspėja, jog Lietuvoje gali uždaryti savo gamybą, kad nebūtu problemų su Kinija – o Lietuvos valdžia pareiškia, kad vis viena tęs nukreiptą prieš Kiniją politiką, ir jokie Lietuvos pramonės netekimai nestabdys jos paramos demokratiniam Taivanui.

Pagaliau pats ryškiausias pavyzdys – sankcijos „Belaruskaliui“.

Visgi, vienas „Belaruskalij“ – tai vienas penktadalis Klaipėdos uosto ir „Lietuvos geležinkelio“ apyvartos. Trečiame pagal dydį Lietuvos mieste gali prasidėti socialinė-politinė krizė...

Kuo daugiau blaiviai mąstančių žmonių Lietuvoje ragina valdžia neišprotėti ir pagalvoti apie jos „kietos“ politikos pasekmes, tuo tvirtesni konservatorių ketinimai įgyvendinti šią politiką. Būtent dėl pasekmių.

Kuo blogiau – tuo geriau. Kuo daugiau Lietuva neteks dėl „principingos užsienio politikos“, tuo daugiau galima pateikti įrodymų sąjungininkams, kad Lietuva – moralinis kriterijus JAV ir ES. Ji pakirto savo ekonomiką, savo priešais padarė dvi supervalstybes, strateginės reikšmės Klaipėdoje išprovokavo protestinį sprogimą, bet nepasitraukė iš kovos su autokratais už demokratiją.

Tokios šalies verta prisiklausyti. Į tokią šalį negalima neatkreipti dėmesio.

Tai paprasti lietuviai, o ne premjerė Ingrida Šimonytė neteks darbo vietų ir uždarbio, nutraukus bendradarbiavimą su baltarusiais. Tai Lietuvos jaunimas, o ne Gabrielius Landsbergis, savo šalyje neras darbo, kadangi investoriai bijos ateiti į Lietuvą baimindamiesi Kinijos. Tai eiliniai pensininkai, o ne Vytautas Landsbergis, gali nesulaukti pensijos padidinimo, todėl kad iždą nualino „principinga vertybių politika“.

Paprasčiausiai, daiktus reikia pavadinti savo vardais.

Lietuvos užsienio politikos mazochizmas – tai vidaus politikos sadizmas. Lietuvos valdžia tyčiojasi iš lietuvių, kad į ją atkreiptų dėmesį žmonės iš Briuselio ir iš už vandenyno.

Jei lietuviai nori, kad jų gyvenime kas tai pasikeistų į geresnę pusę, pradžiai jie turi įsisąmoninti šį faktą.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 20 — id: `scraped:rubaltic_lt:468fbe5cd7a668ff`

**Title:** Atlyginimas už SSSR sugriovimą: Vakarai apsaugo Gorbačiovą nuo Lietuvos persekiojimo

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos piliečiai padavė ieškinį Michailui Gorbačiovui į Vilniaus apygardos teismą. Buvusį SSSR  prezidentą kaltina tuo, kad jis nekliudė „tarptautiniam nusikaltimui“, esą, kurį sovietų kariuomenė padarė 1991 metų sausio mėnesio 13 d. Vilniuje. Vienas iš proceso iniciatorių – Robertas Pavilionis – neslepia savo nepasitenkinimo Lietuvos prokuratūros neveikimu: ji nesiėmė jokių aktyvių veiksmų dėl Gorbačiovo patraukimo baudžiamojon atsakomybėn. Potencialus pagrindinis įtariamasis sausio 13 byloje ir toliau „gurkšnoja alų“, kol už jį bausmę atlieka paprastas sovietų karininkas Jurijus Melis.

Pareiškimą dėl baudžiamosios bylos iškėlimo pirmajam ir paskutiniajam SSSR prezidentui Lietuvoje padavė 1991 metų sausio mėnesio 13 d. tragedijos keturių aukų– Vido Maciulevičiaus, Algimanto Petro Kavoliuko, Virginijaus Druskio ir Apolinaro Juozo Povilaičio giminės. Jie įsitikinę, jog prokuratūra turi teisiškai įvertinti ne tik davusius įsakymą dėl sovietų kariuomenės įvedimo į Vilnių, bet ir „aukščiausio rango vadovus“. Konkrečiai, tuometinį aukščiausiąjį SSSR karinių pajėgų vadą.

Vienas iš ieškinio iniciatorių, Robertas Povilaitis, 1991 m. sausio mėnesio 13 d. įvykių metu neteko tėvo. Jis nuoširdžiai stebisi, kodėl lietuviška Temidė per didesnį nei trisdešimt metų laikotarpį taip ir nebandė patraukti atsakomybėn Gorbačiovą asmeniškai.

„Kadangi Lietuvos Respublikos Generalinė prokuratūra atsisakė kelti M. Gorbačiovo atsakomybę baudžiamajame procese, aš kaip pilietis noriu iškelti M. Gorbačiovo atsakomybę už Sausio 13-sios žudynes civiliniame procese ir jo atžvilgiu pateikti civilinį ieškinį. Daug metų bandžiau įtikinti prokurorus, kad jie turėtų vykdyti ikiteisminį tyrimą dėl aplaidaus vado pareigų vykdymo.

Civilinio ieškinio pateikimą laikau paskutine galimybe iškelti M. Gorbačiovo atsakomybę”, – teigė R. Povilaitis. Jo pasipiktinimas yra suprantamas. Įvykiai prie Vilniaus televizijos bokšto Lietuvoje oficialiai pripažinti agresijos aktu, kruvino valstybės perversmo bandymu. Lietuvos Generalinės prokuratūros kaltinamajame akte nurodoma, kad SSSR vadovybės ir SSKP veiksmai tą lemtingą naktį buvo nukreipti „į sisteminius ir plataus masto civilinių  asmenų užpuolimus, juos nužudant, padarant sunkią žalą jų sveikatai, žmonių grupės ar bendrijos buvo persekiojamos, remiantis politiniais motyvais <…> taikant bauginimo ir teroro priemones, neteisėtai atimant arba apribojant laisves, naudojant uždraustas karo veiksmų priemones“.

Šių įvykių tyrimas – pati sudėtingiausia, paini ir didelės apimties baudžiamoji teisena postsovietinės Lietuvos istorijoje. Dešimtys žmonių buvo nuteisti ir teismas skyrė bausmes už akių. Tarp jų buvo, kaip ir eiliniai kariškiai (pavyzdžiui, tankistas J. Melis), taip ir, 1987 – 1991 m. buvęs gynybos ministras Dmitrijus Jazovas Timofejevičius asmeniškai.

Teisybė, verta pažymėti, kad Michailas Sergejevičius ne karta buvo šaukiamas į apklausą.  Bet tik kaip liudytojas.

„Byloje nepakanka duomenų, kurie leistų pripažinti SSSR prezidentą įtariamuoju. Dėl to jis ir buvo šaukiamas į apklausą kaip liudytojas“, - 2021 metais aiškino Lietuvos Generalinės prokuratūros Baudžiamojo persekiojimo departamento vyriausias prokuroras Simonas Slapšinskas.

Pasisakymas apie tai, kad Gorbačiovo persekiojimui nepakanka pagrindų, skamba absurdiškai. Netgi, jei tuometinis SSSR prezidentas, kaip jis pats tvirtina, jau „nebuvo prie reikalo“, jį galima įkaltinti nusikalstamu aplaidumu.

Pats Vytautas Landsbergis pasakoja apie aukščiausio rango karinių vadų konsultacijas su Michailu Sergejėvičiumi.

„Jie reikalavo Gorbačiovo sankcijų panaudoti jėgą. Jis ilgai tylėjo, atidėliojo, o paskui pasakė: na gerai, bandykite! Jie ir nubėgo bandyti... Aš jam skambinau,man atsakė, kad Gorbačiovas kalbėti negali, kadangi miega. O iš tikrųjų jis nemiegojo. Tą pačią naktį jam paskambino Jelcinas ir įsakmiai pasakė: „Baikite šitą bjaurastį“

Tai buvo, kai Vilniuje jau buvo nužudytieji, ir Gorbačiovas nenutraukė prievartą. Jis nemiegojo, jis girdėjo, jis žinojo, kad žudo žmones! (...) Man jo kaltė absoliučiai akivaizdi“, - teigė Landsbergis.

„Lietuvos valstybingumo patriarchas“ asmeniškai pats liudija, kad Gorbačiovas „nenutraukė prievartą“, o valstybės kaltintojas teigia: nepakanka duomenų!

Yra ir kitas vertingas liudytojas – sausio 13 byloje nuteistas už akių SSSR KGB dimisijos pulkininkas Michailas Golovatovas, kuris Vilniaus televizijos bokšto šturmo metu vadovavo „Alfos“ grupei. „ Pačioje pradžioje mes kontaktavome su Gorbačiovu, kai pradėjome tą reikalą. Dar ir Kriučkovas buvo gyvas, ir kiti. Jiems Lietuva siuntė raginimus duoti parodymus. Buvo ir labai riboti susitikimai, buvo pokalbis ir su Gorbačiovu, šito aš nepamenu“, - tvirtina Golovatovas

Ir vis vieną „nepakanka duomenų, leidžiančių SSSR prezidentą pripažinti įtariamuoju“?

Į apklausą, kai liudytojas jis nė karto taip ir neatvyko (esą, apie viską jau pasakė interviu ir neturi nieko pridėti). Buvo bandoma įteikti Gorbačiovui šaukimą per RF Teisingumo ministeriją, bet Maskva atsisakė teikti teisinę pagalbą. To ir reikėjo tikėtis: Rusija principingai skaito neobjektyviu lietuvių atliktą sausio 13 tragedijos tyrimą.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```
