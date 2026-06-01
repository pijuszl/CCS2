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

### Article 1 — id: `scraped:rubaltic_lt:d3b39d7b0a2fc483`

**Title:** Numesti balastą: prezidentas Trampas atsisakys Pabaltijo

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Respublikonų partijos kandidatas Donaldas Trampas išrinktas JAV prezidentu. Savo priešrinkiminėje programoje Trampas pavadino NATO pasenusia organizacija, pasisakė prieš Amerikos pareigas ginti visus savo sąjungininkus ir už tiesiogines Vašingtono derybas su Kremliumi, žavėjosi Vladimiru Putinu bei žadėjo normalizuoti santykius su Rusija. Trampo išrinkimas JAV prezidentu — viena iš didžiausių Pabaltijo katastrofų potarybinėje istorijoje: į valdžią Amerikoje ateina politinis realizmas, kuris svarbiausiu uždaviniu mato JAV nacionalinius interesus, o ne jų „pasaulio žandaro“ funkcijas, globalų dominavimą ir NATO sąjungininkų ginimą. Pabaltijis, tarptautinėje plotmėje specializavęsis „Rusijos sulaikyme“, Donaldo Trampo Amerikai gali tapti nereikalingas.

„Aš skeptiškai žvelgiu į tarptautines sąjungas, kurios kausto mus ilgalaikiais įsipareigojimais,“ — taip apie NATO šių metų pavasarį pirminiuose rinkimuose kalbėjo tada dar kandidatas į Respublikonų partijos kandidatus Donaldas Trampas.

Trampas NATO vadino pasenusia organizacija, kuri naujomis tarptautinėmis sąlygomis nereikalinga ir neefektyvi. „Šiuo metu didžiausia grėsmė mums — „Islamo valstybė“. Ar ne taip? O NATO nepritaikyta kovoti su terorizmu, organizacija buvo suformuota kaip priešprieša Tarybų Sąjungai. O dabar Tarybų Sąjungos nėra,“ — kalbėjo būsimasis JAV prezidentas.

Donaldas Trampas suabejojo neliečiamos Amerikos užsienio politikos aksiomos teisingumu, kad JAV turi ginti savo NATO sąjungininkus: „Paminėdamas NATO, aš kalbėjau apie tai, jog mes išleidžiam daug pinigų, tačiau nematom, kad visos 28 valstybės, su kuriomis turime reikalą, deramai mus gerbtų“.

Kai Trampui buvo užduotas patikslinamasis klausimas konkrečiai apie Pabaltijį, jis nedavė tikslaus atsakymo, ar jo Amerika padės šioms šalims Rusijos agresijos atveju — jis pasakė, jog pirmiausia pažiūrės, kaip šio regiono partneriai vykdė Amerikai duotus įsipareigojimus. Respublikono bendražygiai žengė dar toliau. „Estija — Peterburgo pakraštys, — Respublikonų partijos kandidato nominacijos ceremonijos metu pareiškė buvęs JAV Kongreso Atstovų palatos vadovas Njutas Gringričius, — aš nesu tikras, kad branduolinio karo atveju rizikuočiau Peterburgo priemiestyje esančia vieta“.

„Jei JAV susitaikytų su Rusija, būtų visai neblogai,“ — kalbėjo rinkėjams naujas amerikiečių lyderis.

Trampas daugelį metų žavėjosi Putinu ir tuo, kaip Rusija išbrido iš katastrofos, į kurią ji buvo patekusi XX amžiaus paskutinio dešimtmečio metu. „Jei kalbėti apie Putiną, tai jis, neabejotinai, labai stiprus Rusijos lyderis. Jis daug stipresnis lyderis, nei mūsiškis,“ — kalbėjo Trampas pavasarį debatų su kitais respublikonais metu.

„Aš tikiuosi labai, labai gerų santykių su Putinu ir manau, kad labai geri santykiai susiklostys su Rusija,“ — pareiškė būsimasis JAV prezidentas susitikimo su karo Irake ir Afganistane amerikiečių veteranais metu. „Aš elgčiausi su Vladimiru Putinu tvirtai, tačiau aš negaliu net įsivaizduoti, ko norėčiau pasiekti daugiau, nei draugiškos, o ne tokios, kaip dabar, Rusijos,“ — kalbėjo rinkėjams respublikonų kandidatas. —

Trampas ne kartą kalbėjo apie tai, kuo reikėtų užsiimti. Pradedant pasisakymu 70-osios jubiliejinės JT Generalinės asamblėjos metu, jis daug kartų ragino Putiną: sukurti globalią koaliciją kovai prieš tarptautinį terorizmą ir Amerikai su Rusija kartu dalyvauti karinėje kampanijoje Sirijoje. „Jeigu Vladimiras Putinas nori eiti į Siriją ir išvyti iš ten „Islamo valstybę“, aš remiu tai 100 proc. Nesuprantu, kaip kažkas gali elgtis kitaip,“ — pareiškė Trampas vieno iš pirmųjų priešrinkiminių pasisakymų metu 2015 metų lapkričio mėnesį.

Taip pat netikėtai amerikiečių užsienio politikai nuskambėjo būsimojo prezidento pareiškimai Ukrainos klausimu. 2015 metų rugpjūtį savo interviu NBC Donaldas Trampas pareiškė, jog jam vis tiek, ar įstos Ukraina į NATO. „Man vis tiek. Jeigu Ukraina įstos — gerai, jei ne — taip pat puiku,“ — pasakė jis. Tapęs kandidatu į JAV prezidentus, Trampas ne kartą piktinosi, kad Europa nesugeba savarankiškai sureguliuoti ukrainietiškos krizės ir todėl Ukrainą kiša Amerikai. „Jūs žinote, jūs matote, Vokietija ir kitos šalys neatrodė įsivėlusios. Jos tik kartojo „Mes turime sustabdyti“ ir nieko neveikė. Viskas vyko tarp mūsų su Rusija. Kodėl? Faktiškai — dėl dujų, naftos ir kitų dalykų, kurių kitos šalys norėjo iš Rusijos,“ — pasakė Trampas šių metų kovą.

Vasarą Trampas dar labiau nugąsdino Rytų Europą, nei Pabaltijo šalių atveju, nepateikęs tikslaus atsakymo Krymo klausimu. „Kiek žinau, Krymo žmonės norėjo būti su Rusija, o ne su tais, su kuriais buvo. Ir į tai būtina atsižvelgti,“ — pareiškė būsimasis JAV prezidentas. Be to, Trampas ne kartą sakė, kad peržiūrės klausimą dėl sankcijų prieš Rusiją panaikinimo. Rudenį jis ignoravo Ukrainos prezidento Petro Porošenkos prašymą susitikti.

Palyginkim tai su tuo, ką šių rinkimų metu kalbėjo apie Rusiją pralaimėjusios kandidatės Hilari Klinton komanda. Rusija, Demokratinės partijos štabo ir Baltuosiuose rūmuose veikiančios demokratiškos administracijos dėka, šių rinkimų —metu pateko į amerikiečių politinio gyvenimo dėmesio centrą. Trampas — tai Putino kandidatas, Kremlius kišasi į amerikiečių rinkimus, rusų hakeriai pralaužė demokratų kandidatės elektroninį paštą, rusų stebėtojai nori diskredituoti šiuos rinkimus, rusų propagandistai nori įtakoti amerikiečių valios išreiškimą.

Rusija Sirijoje kelia grėsmę mūsų kariškiams, prieš Rusiją reikia pratęsti senąsias ir įvesti naujas sankcijas. Kijevui — tiekti ginklus, Maskvą — izoliuoti, o Donaldas Trampas — Putino žmogus.

Amerikiečiai — vis dėlto didi tauta. Įtikinėti rinkėjus, kad jų istorinį pasirinkimą įtakoja Vladimiras Putinas, būtų taip pat netoliaregiška, kaip, sakykim, įtikinėti rusų rinkėjus, kad jų istorinį pasirinkimą įtakoja Jaroslavas Kačinskis arba Dalia Grybauskaitė.

Sąmokslo teorija — paskutinis nevykėlio prieglobstis: nėra nieko labiau apgailėtino, nei teisinti savo klaidas ir nesėkmes „penktosios kolonos“ veikla arba klastinga „Maskvos ranka“. Tai gali atsitikti apgailėtiname Pabaltijyje, bet ne Amerikoje, kurios piliečiai nedvejodami pasirinko kandidatą, kurį lydi sėkmė, o ne tą, kuris prieš jį FST pradėtus tyrimus aiškino Kremliaus užmačiomis.

Ir tas faktas, kad amerikiečių elitas, tame tarpe ir jo respublikonų sparnas, daugumoje prisilaiko visai kitų santykiuose su Rusija pozicijų, šiuo atveju nieko nekeičia. Dauguma britų politinės klasės atstovų taip pat nenorėjo, kad Didžioji Britanija išstotų iš ES. Tačiau gyventojai prabalsavo už Brexit, ir nieko nepadarysi: dabar Terezos Mej vyriausybė (pasisakiusi už narystę ES) užtikrina Jungtinės Karalystės išstojimą iš ES. Taip nutarė dauguma, ir daugumos valiai elitas turi paklusti, nes priešingu atveju susilauks socialinio sprogimo.

Ir todėl respublikonų neokonservatoriams, propaguojantiems globalinį dominavimą ir amerikiečių geopolitinę viršenybę, geriausiu atveju pavyks pakoreguoti ir sušvelninti revoliucinę Donaldo Trampo užsienio politikos programą. Visiškai ją ignoruoti ir tęsti Rusijos „sulaikymą“ tiekiant ginklus Ukrainai ir militarizuojant Pabaltijį jie nepajėgs. Nes amerikiečių tauta nutarė kitaip.

Dauguma amerikiečių rinkėjų prabalsavo už tiesioginį dialogą su Kremliumi ir Rusija, už gerus santykius su rusais, prieš tai, kad Amerika pasaulyje būtų visur ir visur lietų savo kareivių kraują už „demokratines vertybes“, prieš globalizaciją, prieš transatlantinės ir Ramiojo vandenyno laisvosios prekybos zonas, prieš NATO ir „neįgalias tautas“ — savo vargingas sąjungininkes Europoje, — dėl kurių blogų santykių su Rusija Amerika gali būti įtraukta į Trečiojo pasaulinio karo girnas.

JAV rinkimuose laimėjo realizmo ir protingo izoliacionizmo užsienio politika. Jokios ideologijos, jokių „demokratijos eksportų“ ir „demokratiškų intervencijų“, globalaus mesionizmo ir „šventos Amerikos pareigos“ ginti griebiančius už jos skverno skaitlingus ir šimtą metų jai nereikalingus sąjungininkus. Tik nacionaliniai interesai, tik pragmatika ir tiesioginės stipriųjų su stipriaisiais derybos, kuriose vyrauja sveikas abiejų pusių protas, abipusė pagarba ir įsiklausymas į kitos pusės interesus. Amerika per ilgai užsiiminėjo svetimoms sienomis, nekreipdama dėmesio į savo sieną su Meksika. „Aš ne izoliacionistas, bet aš manau, jog pirmiausia — Amerika,“ — šia proga pasakė Donaldas Trampas.

Pabaltijis atidavė JAV viską, ką tik turėjo, kad tik taptų jų geopolitiniu paklotu. Visa Lietuvos, Latvijos ir Estijos egzistavimo politiniame pasaulio žemėlapyje esmė buvo — amerikiečių globalaus dominavimo mechanizmų aptarnavimas. Pabaltijis — už Ukrainos ir Gruzijos įstojimą į NATO, Pabaltijis — „Rytų partnerystės“ draiveris, Pabaltijis — placdarmas prieš „rusų grėsmę“, Pabaltijis pasirengęs būti NATO sudėtyje bet kokiomis sąlygomis, Pabaltijis siunčia savo kareivius į Afganistaną ir Iraką, Pabaltijis džiūgauja dėl Kadafio nužudymo, Pabaltijis palaiko JAV kėslus bombarduoti Siriją be JT mandato, Pabaltijis priima amerikiečių jūsų pėstininkus ir slaptuosius CŽV kalėjimus, Pabaltijis ragina tiekti ginklus Ukrainai, Pabaltijis inicijuoja prieš Rusiją 5-ojo NATO Įstatų straipsnio dėl kolektyvinio agresoriaus atrėmimo panaudojimą, Pabaltijis visada už sankcijų prieš Rusiją įvedimą, pratęsimą, išplėtimą.

O dabar viskas baigėsi. Vietoj „sulaikymo“ politikos — geri santykiai su Rusija. Vietoj diplomatinio izoliavimo ir išstūmimo iš visur, kur tik įmanoma, — tiesioginis Rusijos ir JAV prezidentų dialogas. Vietoj sankcijų — bendra kova su islamo terorizmu. Viskas. „Buferinės zonos“ paslaugos daugiau nereikalingos. Pabaltijis gali būti laisvas.

Pirmuoju tokiu esminiu poslinkiu tapo Brexit‘as: už išstojimą iš ES balsavę britai būtent nusimetė balastą, nes pagrindine balsavimo prieš narystę ES priežastimi tapo britų visuomenės nuovargis nuo pastoviai į jų šalį plaukiančių lenkų ir pabaltijiečių bedarbių. Akivaizdu, jog referendumo metu britai balsavo ir prieš Pabaltijį: prieš tai, kad jų gyvenimą įtakotų skurstanti Rytų Europa ir neveikli kažkokios ten Lietuvos vyriausybės, sugriovusi savo ekonomiką ir privertusi lietuvius emigruoti į Londoną.

Antruoju, ir kol kas pačiu stambiausiu poslinkiu, tapo Trampas. Akivaizdu, kad amerikiečiai lapkričio 8 dieną taip pat balsavo ir prieš Pabaltijį: prieš tai, kad Amerikai gresia Trečiasis pasaulinis karas dėl to, kad kažkokios Lietuvos prezidentė provokuoja Rusiją, vadina ją teroristine valstybe, o jos vadovą — paranojiku, o Amerikai paskui reikės tą Lietuvą ginti ir dėl jos kariauti su rusais.

Tokių poslinkių artimiausiais mėnesiais bus dar daug. Dar neįveikta europietiškos integracijos krizė, link pergalės rinkimuose Vakarų Europoje ryžtingai žengia euroskeptikai. Tikrosios, „senosios“ Europos gyventojai pergyvena aštrų nusivylimą šių dienų Vakarų pasauliu ir, žinoma, — ES. Tame tarpe, kad Europos Sąjungoje atsidūrė Pabaltijis ir kiti rytų europietiški parazitai.

Ir pirmiausia už borto išmes Pabaltijį. Trampo ir jo idėjų pergalė JAV rinkimuose leidžia tikėtis, kad Lietuvos, Latvijos ir Estijos pašalinimas iš NATO ir Europos Sąjungos — ne perdėtos, o realios, jau rezultatą matančios prognozės.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 2 — id: `scraped:rubaltic_lt:0a8fb3d40694f902`

**Title:** Pabaltijyje neišvengiami etniniai valymai

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Demokratiški institutai, kurių veiklos pagrindas — etninis nacionalizmas, galų gale užsiima tautinių mažumų naikinimu — mano iškilus amerikiečių mokslininkas Maiklas Manas. Esant tokiam dėsningumui Pabaltijo šalių etnokratiniai režimai anksčiau ar vėliau pradės etninius rusų ir lenkų valymus.

Kalifornijos universiteto sociologijos profesorius, Kembridžo universiteto garbės profesorius Maiklas Manas naujoje knygoje „Tamsioji demokratijos pusė“ pateikia savą genocido ir etninių valymų teoriją. Primindamas Amerikos indėnų naikinimo, Osmanų imperijos armėnų genocido, nacistinio Holokausto, buvusios Jugoslavijos respublikose ir Ruandoje etninių valymų pavyzdžius, amerikiečių sociologas daro išvadą, kad etninių grupių naikinimas nėra laukinis pirmykštės visuomenės arba viduramžių barbariškumas, o, priešingai, — visuomenių modernizavimo ir jų politinių sistemų demokratizavimo pasekmės.

Etniniai valymai ir genocidas labiausiai tikėtini demokratinių valstybių-nacijų formavimosi metu.

Tais atvejais, kai šiuolaikiški politiniai institutai kuriami nacijų formavimosi metu, atsiranda dirva tarpetniniams kivirčams, o esant demokratijos, kurios pagrindas — etninis nacionalizmas, formavimosi scenarijui, tautinių mažumų persekiojimas praktiškai neišvengiamas.

„Žinoma, situacija, kai į tą pačią teritoriją pretenduoja dvi tautos, pasitaiko nedažnai. Dažnesni atvejai, kai valstybės ribose dauguma daro spaudimą mažumai. Ir dažniausiai mažumos nesipriešina. Tačiau kai mažuma pradeda priešintis spaudimui ir siekti savos politinės autonomijos ar net valstybės, iškyla problemos. Ir tada gali prasidėti eskalacija,“ — sako Maiklas Manas.

Tokioje situacijoje demokratiški institutai — rinkimai, parlamentas, daugiapartiškumas — nemažina visuomenėje įtampos, nepašalina prieštaravimų ir netampa dialogo tarp socialinių grupių instrumentais — priešingai, skatina neapykantą, gilina kalbų ir regioninę priešpriešą. Galop, tai gali nusiristi iki genocido, kraštutiniu atveju — ne iki gaivališkų naikinimų, kurie atsiranda kaip apačių iniciatyvos rezultatas, o kaip sąmoningas ir suplanuotas ištisų tautų naikinimas, kurį vykdo politinė, ekonominė ir karinė valstybės mašina.

Klasikinis tokio genocido pavyzdys — Holokaustas. Adolfas Hitleris, kaip žinia, atėjo Vokietijoje į valdžią demokratiniu būdu. Tuomet, kai valdžią į savo rankas paėmė naciai, Vokietija buvo monolitinė etninė valstybė, tačiau hitlerininkai, siekdami įtvirtinti savo politines pozicijas, išrado vidinį priešą — žydus. Rezultatas — „Krištolinė naktis“ ir nacių „mirties stovyklos“.

Tačiau etninių grupių Europoje naikinimas nesibaigia ir po hitlerizmo pralaimėjimo. Etniniu nacionalizmu praskiestas demokratizavimas, kaip vyraujanti ideologija, tampa masiškų žmonių žudynių XX amžiaus pabaigoje ir net XXI amžiuje priežastimi.

„Atkūrusi nepriklausomybę Ukraina bandė žengti demokratizavimo keliu. Pagrindinės partijos virto etninėmis — sąlyginai „rusiška“ ir „ukrainietiška“, — sako Maiklas Manas. — Praėjo keli didelės konkurencijos tarp šių partijų elektoratų ciklai. „Ukrainietiška“ ir „rusiška“ partijos kovojo tarp savęs ir eilės tvarka kontroliavo valstybę. Abi šalys tikėjosi užsienio paramos. „Rusiška“ partija jos laukė iš Rusijos, „ukrainietiška“ — iš Vakarų. Eskalacija iššaukė karinius susirėmimus Rytų Ukrainoje. Nuo to momento tu turi būti arba rusas, arba ukrainietis — pradeda vyrauti identiškumas. Abi šalys — ukrainietiška ir rusiškas pasipriešinimas — radikalizuojasi“.

Šimtai tūkstančių bėglių ir tūkstančiai žuvusių Pietų-Rytų Ukrainoje — tai rezultatas veiksmo, kai antrojo Maidano metu Ukraina galutinai pasirinko Rytų Europos vystymosi modelį. Šis modelis — etninis provokuojantis nacionalizmas, pagal kurį pagrindinė nacija buvo amžiais žeminama, persekiojama, ją bandė sunaikinti visokiausi agresoriai ir okupantai, ir todėl ši nacija turi būti pati savo šalyje šeimininkė, visur įtvirtinanti savo (vienintelę valstybinę) kalbą ir vietinę archajišką kultūrą, o „kolonistų“ ir „okupantų“ palikuonys privalo arba asimiliuotis, arba nešti kailį ten, iš kur atkeliavo jų protėviai.

Toks nacijos formavimosi susiniekinimo modelis, sąmoningai žeminant save istorijoje, įsivaizduojant save buvusios kolonijos vaidmenyje, būdingas daugeliui buvusių tarybinių respublikų (išimtis — Rusija ir Baltarusija). Kartu su šiais procesais vyko vakarietiškų demokratiškų institutų persodinimas į vietinę dirvą.

Labiausiai prie amerikiečių sociologo aprašyto modelio šis procesas priartėjo Pabaltijo šalyse. Latvijoje ir Estijoje tarybiniai komunistiniai institutai buvo pakeisti 1990 metų pradžioje vakarietiškais, atimant pilietybę ir fundamentalias teises iš trečdalio gyventojų. Ir tada rinkimai, parlamentarizmas, daugiapartiškumas — visi šie demokratijos malonumai — dirbo tik latviams ir estams — saviems, „baltiesiems“. Rusakalbiai gyventojai nepiliečių instituto pagalba nuo pabaltijietiškos „demokratijos“ buvo nušalinti praktiškai visi.

Demokratija Pabaltijyje kūrėsi formuojant naciją pagal rytų europietišką etnolingvistinį modelį ir įtvirtinant etninį nacionalizmą kaip viešpataujančią ideologiją.

„Demokratija saviškiams“ uždraudė šimtams tūkstančių žmonių balsuoti rinkimų ir referendumų metu, dalyvauti privatizacijose, tikėtis valstybės paramos užsienyje ir socialinio gynimo tėvynėje.

Su nacionalizmu sukergta demokratija pagimdė kalbinį terorą ir kalbos policiją, dirbtinus filtrus, atstumiančius tautinių mažumų atstovus nuo darbo valstybinėje ir municipalinėje tarnyboje, draudimus mokytis gimtąja kalba, rašyti ir tarti savo vardus ir pavardes pagal gimtosios kalbos taisykles, likviduojant tautinėms mažumoms skirtas žiniasklaidos priemones ir mokyklas.

Tokia specifinė „demokratija“ pagimdė tautinių mažumų aukščiausiame valstybės lygyje šmeižtą, begalinius įtarimus nelojalumu, „penktosios kolonos“ įvardijimu ir šūkavimais „lagaminas, stotis, Rusija!“.

Maiklas Manas savo knygoje tokius politinius režimus nevadina demokratiškais: tie režimai, kurie užsiiminėja etniniais valymais ir diskriminuoja gyventojus kalbos ir kultūros atžvilgiu, negali būti demokratiški. Tai etnokratijos, prisilaikančios demokratinių standartų ir atliekančios demokratines procedūras tik vieno, „ypatingo“ etnoso labui.

Tokia situacija Lietuvoje, Latvijoje ir Estijoje egzistuoja iki šiol. Šių šalių politiniai režimai vis dar yra etnokratiniai, „nacijos“ sąvoka Pabaltijo šalyse vis dar reiškia etninę naciją — lietuvius, latvius ir estus, kurių labui ir gerbūviui egzistuoja Lietuva, Latvija ir Estija. Paskutinė tezė ryškiai atsispindi Pabaltijo respublikų konstitucijose.

Pabaltijo rusai, Lietuvos lenkai — visi jie vien tik „penktoji kolona“, apie kurios nelojalumą ir grėsmę iš jos pusės pastoviai savo viešosiose ataskaitose triūbina vietinės specialiosios tarnybos.

Pabaltijo nacionalistai vėl ir vėl ateina valdžion gąsdindami rusų ir kitomis „grėsmėmis“ ir žadėdami surengti pagreitintą prievartinę tautinių mažumų asimiliaciją — uždarinėti rusų ir lenkų mokyklas, sugriežtinti įstatymus, skirtus nevalstybine kalbama spausdinamiems leidiniams. Tautinių mažumų partijos (Latvijos „Santarvė“) lieka arba tampa (Lietuvos lenkų rinkiminė akcija) tomis politinėmis jėgomis, kurių nevalia prileisti prie dalyvavimo šalies valdyme.

Liekant tokiai situacijai, Pabaltijyje anksčiau ar vėliau prasidės rusų ir lenkų etniniai valymai.

Nieko neturi nuraminti ta aplinkybė, kad po TSRS subyrėjimo Pabaltijo respublikose nevyko tautinių mažumų žudynių ir masiškų nusikaltimų tautiniu pagrindu — čia buvo apribotos teisės ir diskriminuota kalba. Lietuvos, Latvijos ir Estijos valdantieji nacionalistai taip ir žengia Hitlerio ir nacių keliu, o siekdami sutvirtinti savo politines pozicijas, išradinėja vidaus ir išorės priešus. Išorės priešas — Rusija, vidaus — tautinės mažumos.

Šioms šalims degraduojant, tęsiasi vietinės kilmės gyventojų emigravimas, išmirimas, ekonomikos griūtis, Europos sąjungos dotacijų mažinimas, ir tada vadovaujantis viršūnėlis puola kurti priešo įvaizdį. Juk negali jis šalies pralaimėjimus aiškinti savo bukumu ir nekompetencija. O kas gali būti kaltas dėl Lietuvos, Latvijos ir Estijos nesėkmių bei problemų? Akivaizdu, tai vidinis priešas — „nelojalios mažumos“. Visi tie rusai, lenkai arba latgaliais save vardinantys latviai — Putino agentai ir priešo šnipai, kurie geria krikščionių kūdikių kraują! Visas problemas sukelia jie! Tegul tie kolonistų ir okupantų palikuonys neša kailį ten, iš kur atkeliavo!

Visa ši retorika transliuosis per visiškai demokratiškus institutus: partijas, žiniasklaidą, priešrinkiminę agitaciją, svarstymus parlamentuose. Ir tada etniniu nacionalizmu praskiesta demokratija pasisuks į Pabaltijo tautines mažumas savo tamsiąja puse.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 3 — id: `scraped:rubaltic_lt:677e17a029a4239c`

**Title:** „Lietuvos elitą gąsdina mano alternatyva proamerikietiškam kursui“

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Sekmadienį Lietuvoje praėjo antras Seimo rinkimų turas. Pagrindine nugalėtoja tapo palyginant nauja partija — Lietuvos valstiečių ir „žaliųjų“ sąjunga, iki šiol turėjusi Seime tik vieną atstovą. Didžiausia nesėkmė lydėjo socialdemokratus ir darbiečius. Balsavimo rezultatus RuBaltic.Ru aptarė su politiku ir politologu Algirdu Paleckiu.

– Pone Paleckis, ekspertai teigė, kad Naujoji Vilnia — proletariškas lenkiškai rusiškas rajonas, todėl kai kurie laikė Jus favoritu. VRK duomenimis, gyventojai daugiau balsų sumetė jaunai konservatorei Monikai Navickienei. Kuo tai paaiškintumėt?

– Sausio mėnesį pasikeitė apygardos ribos. Iš jos teritorijos iškrito Naujininkų rajonas, kurio gyventojų daugumą pagrindinai sudaro neturtingi įvairių tautybių žmonės. Vietoj šio buvo prijungtas Filaretų rajonas, kuris laikomas turtingu ir kurio gyventojų dauguma — lietuviai. Dar į apygardą buvo įtraukti Liepkalnio ir Markučių rajonai, kurie turi nemažai panašumų į Filaretų. Tokiu būdu apygarda ženkliai pasikeitė. Tai ir galėjo nulemti balsavimo rezultatus, nes skirtumas — 900 balsų. Už mane balsavo 6500, už oponentę — 7400 rinkėjų. Skirtumą ženkliai įtakojo naujieji rajonai. Iš kitos pusės — rinkėjų aktyvumas. Naujojoje Vilnioje jie visada mažiau aktyvūs, nei kituose rajonuose. Vargingai gyvenančių ten daugiau, jie nusivylę Lietuvos valdžios politika ir nededa vilčių į rinkimus. Todėl ir aktyvumas čia 7-8 proc. mažesnis, nei kitose Vilniaus vietovėse. Be to, prieš mane dirbo propaganda. Mane ne tik pastoviai juodino valstybės ir privatūs kanalai (juodino realiai: šmeižė esą aš esu labai turtingas), bet dar ir paskutinę priešrinkiminę savaitę išleido anoniminį laikraštį. Būtent Naujojoje Vilnioje.

– Prieš metus renkant Vilniaus merą apklausų metu ryškėjo Valdemaro Tomaševskio populiarumas, tačiau išrinktas buvo liberalas Remigijus Šimašius. Ar galima teigti, kad sociologai ir ekspertai neadekvačiai vertina rinkėjų nuotaikas?

– Dalis sociologų ir ekspertų tikrai nedraugauja su realybe. Pavyzdžiui, prieš pusmetį jie Naujojoje Vilnioje apklausė politologus. Šie prognozavo arba lenkų, arba Darbo partijos kandidato pergalę. Abu net į antrą turą nepateko.

– Prieš Jus buvo organizuota aktyvi propagandinė kampanija — vadino „koloradu“, Kremliaus agentu. Net populiarus LRT žurnalistas Edmundas Jakilaitis oficialiai agitavo už Navickienę. Kaip pakomentuotumėte tokį siautėjimą prieš Jus?

– Čia įžvelgiu keletą faktorių. Pirma, pasireiškia didesnės elito dalies nepakantumas kitaip mąstančių atžvilgiu. Jei tavo nuomonė skiriasi — patenki į priešų sąrašą. Elitas nepajėgus diskutuoti su realia, o ne su tariama alternatyva, kaip, pavyzdžiui, Darbo partija. Antras momentas — pasireiškia alternatyvos bijojimas. Už mane realiai balsuoja daug žmonių. Aš pasisakau už kitokią Lietuvos vystymosi kryptį — ne už liberalią proamerikietišką, o už centrinės valstybės, palaikančios draugiškus ryšius su visais kaimynais, vystymąsi. Tai ir yra elitą gąsdinanti reali alternatyva. Tokios alternatyvos nebuvo Seime kelių paskutinių kadencijų metu. Todėl ir ėmė siautėti.

– Vilniaus meras Šimašius gąsdino, kad Jūs galite įnešti į Seimą „Kremliaus propagandą“. Ar nemanote, kad kai kurios Jūsų pozicijos iš tikrųjų gali turėti prorusišką kvapą?

– Aš visada sakau: Amerika ne visada teisi, o Rusija ne visada klysta. O Lietuvoje manoma antraip: Amerika visada teisi, Rusija visada neteisi. Visada reikia matyti konkrečias situacijas. Jeigu kažkokiu klausimu mano pozicija sutampa su Rusijos, visiškai nereiškia, kad aš — Maskvos ruporas. Aš — prolietuviškas politikas ir Lietuvos patriotas. Tik mano patriotiškumas ir meilė Lietuvai skiriasi nuo dominuojančių Lietuvos elite — jie visa tai mato būtinai keliaklupsčiaujant prieš JAV, neigiant Rusiją ir plėtojant rusofobiją.

– Lietuvos žurnalistai pažymi, kad pergalę Jūs galėjote prarasti dėl pasisakymų apie 1991 metų įvykius prie Vilniaus televizijos bokšto ir dėl jų kilusių bylinėjimųsi teismuose. Ar nesigailite, kad kadaise įsivėlėte į istorines diskusijas minėtų įvykių tema?

– Mano žodžiai apie sausio 13 d. [1991 metų – RuBaltic.Ru pastaba] pastoviai pateikiami be interviu konteksto. Labai jau dažnai jie iškraipomi tikslu pateikti juos kaip pačios tendencijos fakto neigimą, norą pažeminti Lietuvą ir t.t. Iš tikrųjų nebuvo jokio noro pažeminti arba neigti tragediją — juk žuvo žmonės. Buvo vien tik noras išsiaiškinti kai kuriuos vis dar atsakymų neturinčius klausimus. Tačiau oponentai įsikibo į mano žodžius ir pastoviai stengiasi juos panaudoti. Ką gi, kol kas tai jiems pavyksta. Tačiau, kartoju, tai ne visai padoru.

– Kai kurie balsavę už Jūsų oponentę konservatorę savo pasirinkimą aiškino tuo, kad Navickienei bus lengviau dirbti, nes už jos nugaros — galinga partija. Jūs ėjote kaip nepartinis. Ar gali nepartinis, nepriklausomas deputatas dirbti sėkmingai, būti naudingi Seime?

– Seimą lydi įvairios darbo istorijos. Kai kurie didžiųjų partijų atstovai nieko nenuveikė apygardose, o mažų partijų atstovai arba nepriklausomi, priešingai, pasireiškė aktyviai. Teoriškai, taip, didelės partijos atstovai turi daugiau svertų. Tačiau viskas priklauso nuo konkretaus žmogaus, konkrečios asmenybės. Manau, jog ir nebūdamas deputatu aš nemažai nuveikiau savo apygardoje, atkreipdamas į ją komunalinių tarnybų ir kitų organizacijų dėmesį.

– Rinkimai tapo Lietuvos valstiečių ir „žaliųjų“ sąjungos triumfu. Jos lyderį Ramūną Karbauskį žymūs Lietuvos politologai taip pat likus savaitei iki rinkimų kaltino ryšiais su Rusija. Priminė, kad jis turėjo su Rusija biznį, Maskvoje gyvena ir dirba jo brolis ir panašiai. Kame slypi šios sąjungos sėkmė?

– Pastaruosius aštuonerius metus partija sėkmingai augo. Partija iš Karbauskio pusės sulaukė rimtos finansinės paramos, ji pasižymi rimta materialine baze. Sąjunga gerai organizavo kampaniją, neįsivėlė į jokius skandalus, sumaniai išnaudojo „naujos partijos“ fenomeną. Visų rinkimų Lietuvoje metu nauja partija sušluoja protestuojančių ir tų rinkėjų balsus, kurie nusivylė valdančiosiomis partijomis — šį kartą socialdemokratais. Be to, „valstiečiai“ įtraukė į savo gretas aukšto reitingo asmenybes — pavyzdžiui, naują Lietuvos politikos „žvaigždę“, buvusį policijos vadovą Saulių Skvernelį. Tokiu būdu lietuviškasis „naujos partijos“ fenomenas kartu su rimtu politiku Karbauskiu ir jo finansinėmis galimybėmis užsitikrino pergalę. Ir vis dėlto prognozuoju, kad artimiausiais metais ar kiek vėliau ši sąjunga gali skilti.

– Prezidentė Dalia Grybauskaitė jau pasakė, kodėl pralaimėjo socialdemokratai. Tai — masiškas nepasitenkinimas vyriausybės veikla. Ar galima su tuo sutikti?

– Socialdemokratų, Darbo partijos bei „Tvarkos ir teisingumo“ pralaimėjimas — nusivylimas valdančiąja dauguma. Vyriausybė nepateisino vilčių. Žmonės nepamiršo, kaip, įvedus eurą, šoktelėjo kainos. Buvo ir korupcijos skandalų. Labiausiai nuskambėjęs — Krašto apsaugos ministerijos pirkiniai [kariuomenei ženkliai padidintomis kainomis buvo įsigyti valgyklų reikmenys — RuBaltic.Ru pastaba]. Valdantieji įvėlė daug klaidų, menki buvo ryšiai su žmonėmis. Nesimatė ryškaus lyderio. Vyriausybė veikė prezidentės šešėlyje, neturėjo savo aiškios pozicijos. Žmonės pastebėjo prezidentės įtaką ir atitinkamai įvertino.

– Dabar svarstomas naujos koalicijos formavimo klausimas. Ko tikitės iš naujos Seimo sudėties?

– Koalicijoje, manau, bus Valstiečių ir „žaliųjų“ sąjunga. Tokie signalai jau yra, ir prezidentė apie tai kalba. Apie artimiausius žingsnius sunku kalbėti, nes kol kas vyksta derybos. Prognozuoti sunku, nes daug ginčų Seime gali sukelti nauji žmonės, o jų nemažai. Ko laukti iš konservatorių, mes jau žinome: griežtos ekonomijos priemonių ir antirusiškos politikos. Apie „valstiečius“ kalbėti sunku — partijoje dar vyks rimtos vidaus diskusijos. Valstiečiai ir „žalieji“ dar neturi nusistovėjusios ideologijos. Stebėti visa tai bus įdomu.

– Ar sugebės naujas Seimas ištaisyti senojo klaidas? Pavyzdžiui, priimti Darbo kodekso prezidentės pataisas, kurias blokavo socialdemokratai?

– Manau, sugebės. Juk žadėjo politikai. Priklausys nuo koalicijos partnerių. Jeigu jais bus konservatoriai, galimybės sumažės.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 4 — id: `scraped:rubaltic_lt:14c9ccf6433f763c`

**Title:** Pabaltijo gyventojų kišenes tuštins depopuliacija

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Rekordinis Pabaltijo šalių gyventojų skaičiaus mažėjimas neišvengiamai sukels mokesčių didinimą Lietuvos, Latvijos ir Estijos gyventojams. Likę savo šalyse pabaltijiečiai bus priversti mokėti mokesčius ne tik už save, bet ir už išvykusius. Tokia situacija pavers Pabaltijo šalių demografinę katastrofą dar labiau dramatiška: dėl vis didėjančios mokesčių naštos bėgti iš Lietuvos, Latvijos ir Estijos bus priversti net tie gyventojai, kurie iki šiol apie tai negalvojo; to pasėkoje jau artimiausią dešimtmetį Pabaltijyje liks tik savo paskutinius metelius stumiantys pensininkai.

Metinėje latvių verslo 2016 metų apžvalgoje buvo paviešinti informacinės agentūros LETA, tyrimų kompanijos Oxford Research ir kompanijos Firmas.lv bendromis jėgomis atlikti tyrimai, liečiantys Latvijos Respublikos mokesčių sistemą. Pagrindinė tyrimų išvada: mokesčiai šalies gyventojams artimiausiais metais bus vien tik didinami, o priežastis — katastrofiškas gyventojų skaičiaus mažėjimas.

„Pažvelgus į šalies demografinę situaciją tampa aišku, kodėl neišvengiamas mokesčių didinimas, — rašo Oxford Research analitikai. — Skaičius gyventojų, t.y. dabartinių ir būsimų mokesčių mokėtojų, tebemažėja. Tačiau norint išlaikyti šalį su jos infrastruktūra, keliais, mokyklomis, ligoninėmis ir t.t., neturi proporcingai gyventojų skaičiui mažėti finansavimas — jis turi didėti, nes būtina kompensuoti infliaciją ir tenkinti didėjančius poreikius kokybinėms valstybinėms paslaugoms“.

Kitaip sakant, nenaudojamą infrastruktūrą būtina prižiūrėti taip pat, kaip ir prižiūrimą. Komunalinio ūkio sistema — neišardoma, ir prižiūrima ji turi būti pastoviai, nors mažiausiai ketvirtadalis Latvijos būstų liko be gyventojų.

Kas dėl valstybinių paslaugų (visų pirma sveikatos ir socialinės apsaugos), tai jų poreikis aštrėjant demografinei krizei ne mažės, o vien tik didės. Gyventojų amžiaus struktūros deformacija veda prie kritiško pagyvenusių žmonių skaičiaus didėjimo — jiems reikalingi gydymas ir priežiūra, o tuo metu mažėja skaičius darbuotojų, galinčių rūpintis pensininkais. Ir todėl artimiausiais metais kartu augs valstybinių paslaugų poreikis, jų deficitas, eilės paslaugoms ir būtinai — poreikis didinti jų valstybinį finansavimą.

Bendra šių pavijų keliančių tendencijų priežastis — neišvengiamai artėjanti prie Latvijos demografinė katastrofa. Atsižvelgiant į tai, kad panaši katastrofa neišvengiamai pasieks ir Lietuvą su Estija, galima daryti bendrą Pabaltijo respublikoms išvadą.

TSRS subyrėjimo metu Lietuvoje gyveno 3,7 milijono, o Latvijoje — 2,6 milijono žmonių. Šiuo metu jos jau neturi trečdalio gyventojų, o artimiausiais dešimtmečiais, kaip prognozuoja europietiškos statistinės tarnybos, praras dar trečdalį. Likusiems Pabaltijyje gyventojams, priverstiems palaikyti miesto, socialinę ir komunalinio ūkio infrastruktūrą, teks mokėti ne tik už save ir aną vaikiną, bet dar už du vaikinus.

Nenorintys atsisveikinti su gimtuoju Pabaltiju bus priversti iš savo atlyginimų mokėti pensijoms skirtus mokesčius. Pensininkų ir darbingų mokesčių mokėtojų skaičius Lietuvoje, Latvijoje ir Estijoje atvirkščiai proporcingas: augant pirmųjų skaičiui ir mažėjant antrųjų, teks arba pastoviai mažinti pensijas, arba pastoviai didinti mokesčius.

Pabaltijo šalių demografai ir ekonomistai ne kartą kalbėjo apie šią besiformuojančią pavojingai negatyvią tendenciją.

Gilėjant „demografinei duobei“, išeinant į pensiją gausiausiai, 1960-1970 metais gimusiai darbuotojų kartai, pensijos vis labiau mažės. Alternatyvus variantas — vis labiau didės mokesčiai dar neišbėgusiems iš Lietuvos, Latvijos ir Estijos darbuotojams. Ir tada jau artimiausiais 5-10 metų Pabaltijyje nebus įmanoma pragyventi nei iš pensijų, nei iš atlyginimo.

Oxford Research analitikai daro logišką išvadą: pastovus mokesčių didinimas neskatins Latvijos gyventojų gyventi joje, dirbti ir gimdyti vaikų. Ta pati išvada liečia ir Lietuvą su Estija.

O ar jie turi kitokią išeitį? Maža to, kad Europoje, kuri priima Pabaltijo bedarbius, uždarbiai 5-6 kartus didesni. Gimtajame Pabaltijyje realus uždarbis visą laiką mažės.

Kokia iš šios situacijos, išskyrus emigraciją, gali būti išeitis? Pabaltijietiškas humoras: „Paskutinis išskrendantysis, neužmirškite aerouoste išjungti elektrą“, — pamažu tampa realybe. Iki šiol iš Pabaltijo —skuodė jauni, aktyvūs, ambicingi — netrukus iš šių nepriklausomų valstybių bus priversti bėgti visi. Įskaitant tuos, kurie neketino bėgti, kurie visa širdimi myli savo Lietuvą, Latviją arba Estiją, kuriuos, tik ne profesionalius, vietinius politikus, galima pavadinti tikrais patriotais.

Taigi jau netolimoje ateityje dar kažko šviesesnio belaukiančiam Pabaltijo gyventojui teks nusipirkti bilietą į lėktuvą viena kryptimi ir išskristi, paliekant profesionalius „patriotus“ — Pabaltijo valdovus — vienus su vargšais senukais, kuriuos jiems teks išlaikyti iš neaiškių šaltinių gautomis lėšomis.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 5 — id: `scraped:rubaltic_lt:9690f8b97ffde8b7`

**Title:** Rusijos strategija Pabaltijyje: netrukdykite jiems išnykti

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Rusijos vadovybė iškėlė stambiausiems pervežėjams politinį uždavinį: nuo 2020 metų visi be išimties Rusijos kroviniai turi aplenkti Pabaltijo uostus. Po to, kai Pabaltijis liks be Rusijos krovinių, Lietuva, Latvija ir Estija pilnumoje patirs demografinės katastrofos pasekmes: jaunimo ir kvalifikuotų specialistų emigracijos, gimstamumo mažėjimo ir kritiško pagyvenusių žmonių skaičiaus augimo. Už demonstratyvaus oficialios Maskvos abejingumo Pabaltijo atžvilgiu slypi paprasta ir konkreti strategija Lietuvos, Latvijos ir Estijos atžvilgiu: nesikišti į Pabaltijo įvykius, netrukdyti vietinėms viršūnėlėms žudyti šias šalis savo beprotiška politika ir neduoti lietuviams, latviams ir estams galimybės išsigelbėti Rusijos išteklių sąskaita.

Buvęs Rusijos prezidento Administracijos vadovas, specialus Vladimiro Putino atstovas ekologijos ir transporto klausimais Sergejus Ivanovas, kalbėdamas stambiausių Rusijos pervežėjų pasitarime, iškėlė valstybinės svarbos uždavinį: visi šalies kroviniai, perkraunami Pabaltijo uostuose, nuo 2020 metų turi juos aplenkti. Nė vienas rusų krovinys šio dešimtmečio pabaigoje neturi pasiekti Lietuvos, Latvijos ir Estijos.

Prieš savaitę kompanijos „Transneft“ prezidentas pranešė Rusijos prezidentui Vladimirui Putinui, jog Rusija tęsia eksportuojamų naftos produktų perorientavimą iš Pabaltijo į savo krovininius uostus Leningrado srityje. „Vykdydami vyriausybės pavedimą, mes perorientuojame krovinių srautus iš Pabaltijo uostų: Ventspilio, Rygos — į mūsų Baltijos uostus — tai Ust-Luga ir Primorskas, o taip pat Novorosijskas, — pranešė Tokarevas. — Jeigu pernai ten (Pabaltijyje — RuBaltic.Ru pastaba) buvo perkrauta apie 9 mln tonų naftos produktų, tai šiemet — 5 mln tonų. Iki 2018 metų, artimiausiais metais, mes sumažinsim krovinių į Pabaltijį srautą iki nulio. Apkrausime savo uostus, tam yra visos galimybės“.

Anksčiau šiuos ryšius naikino Pabaltijis, dabar juos sąmoningai ir kryptingai naikina Rusija. Po kelerių metų (o gal ir mėnesių) valdantysis Lietuvos, Latvijos ir Estijos elitas su nuostaba suvoks, kad pats paruošė Kremliui kovos su juo metodologiją. Pabaltijo remiamas sankcijų prieš Rusiją įvedimas netrukus gali tapti efektyviu rusų užsienio politikos instrumentu.

Nors buvo tikėtasi, sankcijos nesunaikino Rusijos, nesugriovė rusų ekonomikos ir neprivertė rusų vadovybės atšliaužti pas „vakarietiškus partnerius“, puolus ant kelių su virve ant kaklo atgailauti, kad atsisakė pripažinti globalią politinę hierarchiją. Rusija atlaikė sankcijų smūgį, rusų ekonomika nesuklupo krizės metu, lenkėsi, bet nesulūžo nuo sankcijų, rusų visuomenė lengvai prisitaikė ir išmoko gyventi sankcijų sąlygomis, o „kruvinas režimas“ nesubyrėjo — išorės spaudžiama Rusijos politinė sistema net sustiprėjo.

Humoristinis tostas „Už sankcijas!“ Rusijoje tapo realybe. Sankcijinis  iššūkis verčia rusų vyriausybę užsiimti savo ekonomikos modernizavimu. Rusija pamažu realizuoja importuojamų prekių gamybos politiką, tame tarpe ir aukštų technologijų srityse. Antrame 2016 metų ketvirtyje apie mašinų ir įrenginių gamybai importo sumažinimą pareiškė kas trečia Rusijos įmonė, o 6 proc. įmonių visiškai atsisakė įrengimų importo.

Kas dėl žemės ūkio produkcijos, tai per dvejus maisto produktų embargo metus Rusija sugebėjo pilnai apsirūpinti savais produktais ir tapo viena stambiausių pasaulyje grūdų ir mėsos eksportuotojų. Dabartinėmis sąlygomis Rusija suinteresuota jai sankcijų taikymu: kol nebus galutinai restruktūrizuota jos ekonomika, sankcijos jai naudingos. Todėl apie būtinybę atsisakyti sankcijų vis garsiau kalbama vakarų šalių sostinėse, o ne Maskvoje. Todėl Europos Sąjunga šių metų vasarą pratęsė sankcijas prieš Rusiją pusmečiui, o Rusija atsakė kontrsankcijomis pusantriems metams.

Kai bus užbaigtas ekonomikos restruktūrizavimas ir atsiras galimybė atnaujinti ekonominius kontraktus su Europos Sąjungos šalimis, Rusija tai galės daryti savo sąlygomis. Kaip visiškai teisingai visus šiuos metus kalbėjo Pabaltijo politikai ir ekspertai, sugrįžti Rusijos-Europos santykiuose prie business as usual, prie prieškrizinės būklės, daugiau nebus įmanoma.

Sankcijos, kitaip išdėsčius jėgas, gali tapti efektyviu rusų užsienio politikos instrumentu.

Politinė konjunktūra, realizuojant tokį užsienio politikos uždavinį, klostosi puikiai. Europietiška integracija pergyvena didžiausią savo istorijoje krizę. „Naujieji europiečiai“, atsisakydami priimti bėglius, ardo „europietišką solidarumą“, „senieji europiečiai“ vis labiau nusivilia „Vieninga Europa“ ir siekia savo šalių išstojimo iš ES. Brexit‘as įrodė, jog išcentrinės nuotaikos didžiausiose Europos šalyse — tai ne momentinis reiškinys, jos gali turėti labai rimtas ir labai pavojingas eurointegracijai pasekmes.

Svarbiausias ES dezintegracijos rizikos įveikimo instrumentas, kurį siūlo dauguma ekspertų, — Europos Sąjungos decentralizavimas ir sugrįžimas prie ES šalių narių suvereniteto, perskirstant įgaliojimus tarp Briuselio biurokratijos ir nacionalinių vyriausybių pastarųjų naudai. Tame tarpe Europos šalių sostinėms sugrąžinant ekonominės veiklos su užsieniu laisvę ir teisę savarankiškai vystyti prekybos-ekonominius ryšius su bet kuria šalimi — taip pat ir su Rusija.

Jeigu nugalės alternatyvus eurointegracijos krizės įveikimo scenarijus, numatantis ES centralizaciją ir jos pavertimą de-fakto federaline valstybe, kuriai vadovaus Vokietija ir Prancūzija, jis ir Rusiją tenkins. Skirtingai nei Lietuvai ir Latvijai, Vokietijos ir Prancūzijos egzistavimas tarptautinėje arenoje nesutapatinamas su šūkavimais apie „rusų grėsmę“ ir Rusijos Europoje „sulaikymą“. Abiejose šalyse, siekdamos valdžios kitų metų didžiųjų rinkimų metu, eina draugiškos Maskvai politinės jėgos. Vokietijoje — kairieji socialdemokratai, kurių lyderis Frankas Valteris Štainmajeris ne kartą pasisakė už sankcijų atsisakymą ir strateginę partnerystę su Rusija. Prancūzijoje — dešinieji „respublikonai“, kurių lyderis Nikolia Sarkozi padėjo įveikti krizę tarp Rusijos ir Europos Sąjungos 2008-2009 metais, ir kraštutinioji dešinioji Marin Le Pen, kuri pasižymi kaip didelė Putino garbintoja.

Ir su vienais, ir su kitais Kremlius lengvai ras bendrą kalbą. Po to, kai Vokietijoje ir Prancūzijoje pasikeis valdžia, Maskvai nebus svarbi JAV prezidento rinkimuose izoliacionisto Donaldo Trampo pergalė. Nors jo pergalė teigiamai atsilieptų Rusijos užsienio politikai.

Pabaltijo šalims visiems laikams turi būti nuleistas šlagbaumas išėjimui į rusų rinką. Politine prasme jų daugiametis buvimas rusų rinkoje buvo nenatūralus reiškinys. Dalis tų pinigų, kuriuos rusai mokėjo Latvijos valstybei ir oligarchams už savo krovinių geležinkeliu pervežimą arba latvių bankams už finansinių operacijų aptarnavimą, buvo skiriama latvių ultra dešiniesiems, raginusiems deportuoti iš Latvijos visus be pilietybės rusus užplombuotuose vagonuose. Dalis tų pinigų, kuriuos uždirbo Lietuvos pienininkystės įmonės realizuodamos savo produkciją Maskvoje ir Sankt-Peterburge, buvo skirta „lansbergininkų“ partijai, kurios nariai reikalavo izoliuoti Rusiją nuo Europos ir blokuoti bevizio režimo įvedimą tarp Rusijos ir Europos Sąjungos.

Negi sugrįžimas prie tokio business as usual gali duoti naudos Rusijai? Būtent todėl rusų diplomatija nuosekliai siekia bendradarbiavimo su Europos Sąjungos šalimis prekybos-ekonomikos srityje ne per Briuselį, o tiesiogiai per nacionalines vyriausybes. Todėl valstybinių korporacijų vadovai praneša Rusijos prezidentui, kaip vyksta logistinio srauto perorientavimas iš Pabaltijo uostų į Rusijos. Todėl artimiausias Putino bendražygis ir specialusis atstovas transporto klausimais kelia uždavinį visiškai atsisakyti rusų krovinių tranzito per Pabaltijį iki 2020 metų.

Už demonstratyvaus Maskvos abejingumo Lietuvos, Latvijos ir Estijos atžvilgiu, kurios pastaraisiais metais beveik neminimos rusų vadovybės pareiškimuose, kuriose beveik niekada nesilanko oficialūs asmenys ir kurios nepateko į paskutinę rusų užsienio politikos doktriną, slypi aiški ir paprasta Rusijos strategija Pabaltijo atžvilgiu.

Jeigu prieš ketvirtį šimtmečio strateginė partnerystė su Rusija galėjo padėti Pabaltijo respublikoms pakilti iki svajonių Skandinavijos lygio, tai sekančiais 5-10 metais rankų įkišimas į galingus rusų išteklius tiesiog išgelbėtų jas nuo žūties.

Šiandien Pabaltijo šalis vis labiau slegia demografinė katastrofa. Gyventojai iš šių šalių bėga vis sparčiau. Vien tik iš Lietuvos kas valandą (!) išskrenda 4-5 žmonės. Per dieną — 100, per metus — 35 tūkstančiai. Kasmet Lietuva praranda pusantro procento gyventojų. Praktiškai visi sugrįžę emigrantai netrukus vėl išvyksta iš Lietuvos. „Sugrįžęs emigrantas bando užsikabinti, tačiau egzistuoja šimtaprocentinė garantija, kad jis vėl išvyks į užsienį. Sistema neveikia,“ — taip aprašo katastrofišką situaciją lietuvių demografas Domantas Jasilionis.

Pagal Eurostat‘o prognozę, jau praradusi trečdalį gyventojų Lietuva artimiausiais dešimtmečiais praras dar 38 proc. gyventojų. Panaši padėtis Latvijoje; šiek tiek geresnė, tačiau taip pat kritiška — Estijoje. Tačiau svarbesnės ne kiekybinės, o kokybinės pabaltijietiškos emigracijos charakteristikos. Į Londoną ir Dubliną išskrenda kvalifikuoti kadrai: Pabaltijis praranda gydytojus, inžinierius, mokslininkus, darbininkų profesijų specialistus. Masiškai emigruoja jaunimas — Pabaltijis praranda naują kartą, krenta gimstamumas, lietuviai, latviai ir estai tampa nykstančiomis tautomis.

Ar Rusijai naudinga tokia situacija? Žinoma. Pačios antirusiškiausios, rusofobija kliedinčios Europos Sąjungos valstybės savo noru šliaužia link susinaikinimo. Jos meta visas savo jėgas ir lėšas karinės technikos, o iš tikrųjų — kanadiečių metalo laužo, įsigijimui, pirkdamos kariuomenei „auksines šakutes“ alina biudžetą, skelbia  informacinį karą Baltarusijos AE. Ir tuo metu mano, jog nuo visų savo gyventojų problemų šalis išgelbės emigracija. Ir nepajėgia suvokti, jog strategiškai tokia politika — prorusiška.

Blogiausia, ką gali padaryti Rusija Pabaltijo kryptyje, — vėl atverti savo gailestingą rusišką sielą ir pulti gelbėti silpstančias nuo neregėtos istorijoje depopuliacijos Pabaltijo respublikas. Patirtis teigia, kad Pabaltijis tokios pagalbos nevertina, o į ištiestą ranką spjauna. Tuo geriau Rusijai.

Stebint praktinius rusų vadovybės žingsnius, peršasi išvada, kad Maskvą tenkina tokia padėtis, ir ji pasirenka Pabaltijo atžvilgiu strategiją „virstantį pastumk“. Niekas neketina naikinti sankcijų prieš Lietuvą, Latviją ir Estiją, prezidentas Putinas ir jo patikėtiniai kelia uždavinį artimiausiais metais visiškai atsisakyti rusų krovinių tranzito per Pabaltijo šalis.

Kaip tik tuo metu, kai Vilnius, Ryga ir Talinas praras tą skaičių mokesčių mokėtojų, kuris reikalingas savo senukų pensijų mokėjimui, jų uostų ir geležinkelių atsisakys paskutinioji rusų firma. Daugiau Maskvai nieko nereikia daryti. Tik nutraukti su Pabaltijo šalimis visus galimus ryšius, izoliuotis, nusišalinti, kad paskui nereikėtų spręsti jų problemų. Pabaltijis — tas atvejis, kai su oponentu nesiginčijama. Jis pats save naikina.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 6 — id: `scraped:rubaltic_lt:868a570b345fd5e2`

**Title:** Kodėl Vakarai niekada nebuvo civilizuoti

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Sąvokos „civilizacija“ ir „civilizuotas“ tampriai siejasi, tačiau reiškia skirtingus fenomenus. „Civilizacijos“ suprantamos kaip stabilūs sociokultūriniai transregionalinio masto sukūrimai, ir šia prasme Vakarai (Vakarų Europa + JAV) — vieni iš penkių-šešių dabarties civilizacijų. O štai sąvoka „civilizuotas“ per porą naudojimosi ja šimtmečių iš esmės kito, nemažu atstumu atsiplėšus nuo giminingos sąvokos „civilizuotas“.

„Necivilizuotas civilizacija“?

Vakarų civilizacijos atstovai privatizavo kategoriją „civilizuotas“ ir priešpastatė ją sąvokoms „atšiaurumas“ ir „barbariškumas“, klijuodami jas tiems, kurie nepriklauso Vakarams. Tačiau verta atidžiau pažvelgti, kurie civilizuotesni: Vakarai ar Rytai.

Taip, Vakarai ženkliai pasižymėjo technikos sferoje. Ir šiandien, kai žmonės braunasi į parduotuves ieškodami gadžetų su su programomis iš Silikono slėnio, eilinis miesčionis neabejoja, kad Vakarų civilizacija daug pranašesnė už visas kitas.

Tačiau techninis progresas — toli gražu ne viskas. Akivaizdu, jog civilizacija — visų pirma ypatinga kultūra, o ne ekonomikos išsivystymo lygis. Ir įvairios civilizacijos — vakarietiška, kinų konfucijiška, rusų pravoslavų, budų tibėtiška, induistiška, islamo arabų, šiitiška ir t.t. — charakterizuojamos tokiais pagrindiniais požymiais kaip kalba, religija, vertybės ir t.t., t.y. turinčiais sociokultūrines savybes.

Štai čia ir nevalia užmiršti, kad pretenduojantys savo civilizacija pirmauti Vakarai ne vieną šimtmetį pirmavo ne tik technologijomis, bet ir tais procesais, kuriuos niekaip negalima pavadinti „civilizuotais“.

Priminsiu, kad būtent Vakarų Europoje ir JAV buvo įvesta ir realizuota kolonizacija, kurios metu buvo masiškai naikinami „trečiųjų šalių“ senbuviai, kolonijose plėšikaujama, išvežant iš jų į metropoliją milijonus vergų.

Būtent Vakarai išrado inkviziciją, raganų medžioklę ir giljotiną, jie pirmieji pagamino ir praktikoje panaudojo cheminį ginklą (beje, prieš rusus) ir atominę bombą. Jie išrado fašizmą ir dujų kameras, organizavo koncentracijos stovyklas ir įvykdę Holokaustą.

„Civilizatorių“ nusikaltimų sąrašas didžiulis, ir vadinti Vakarus civilizuotais šiandien gali tik primityvios mąstysenos žmogus, gyvenantis tarp gadžetų ir prekybos centro.

Klaida kovoje dėl viešpatavimo

Tuo tarpu vakarietiškų ideologų niekada nedomino nusikalstamos euroamerikietiškų politikų veikos. JAV ir Europa pastaraisiais dviem šimtmečiais gyveno pakilimo stadijoje ir ryžtingai žengė link viešpatavimo pasaulyje, nekreipdamos dėmesio į išorinių ir vidaus (kairiųjų ir dešiniųjų) moralės sergėtojų kritiką. Po bet kurios nesėkmės: trockistų Rusijoje, Vietnamo, Irako, Libijos ir kitų projektų — vakarietiškiems elitams lengvai pavykdavo (ir dabar pavyksta) nekreipti dėmesį į kaltinimus ir iš naujo kopti į viešpatavimo pasaulyje aukštybes.

Šio kopimo kulminacija tapo valdomas Tarybų Sąjungos sugriovimas, paverčiant Rusijos Federaciją Vakarų pusiau kolonija. Atrodė: dar pora žingsniu, ir globalizacijos projektas pagal amerikiečių kurpalių bus sėkmingai realizuotas. Tačiau, deja, nutrūktgalviškai įsivėlusios į kovą su tarybine, o vėliau — su rusų „grėsme“, JAV nepastebėjo kaip kovą dėl viešpatavimo pasaulyje pralaimėjo Kinijai. Dar daugiau — nevaldoma šalimi tampa Indija, vis labiau nevaldomas tampa islamas.

Taigi: pralaimėjusi kovą dėl viešpatavimo pasaulyje Kinijai (apie tai pakalbėsime atskirai būsimuosiuose straipsniuose), JAV nutarė atsirevanšuoti puldamos Rusiją, kuri turi sienas su daugeliu mažų ir Vakarų manipuliuojamų šalių, o todėl — yra idealus taikinys.

Amerikiečių ideologai, t.y. žmonės, nurodantys, apie ką iš pačių aukščiausių tribūnų privalo kalbėti valstybės tarnautojai, tame tarpe ir veikiantys prezidentai, visada žinojo, kad JAV — uzurpatorės. Ir niekada vakarietiškiems politikams nebuvo keliamas uždavinys pritildyti euroamerikietiškų elitų rėkavimus, siekiant viešpatavimo pasaulyje. Uždavinys buvo vienas: užmaskuoti šį siekį, aprėdyti jį kuo švelnesniais („civilizuotais“) terminais ir formulėmis („laisvo pasaulio“ gynimas ir pan.), tokiu būdu įvairiais demagoginiais būdais legitimuoti savo teisę atsidurti politinėje ir kitokioje viršenybėje.

Teroristai = kovotojai su terorizmu?

XXI amžius, o tiksliau — interneto technologijų išsivystymas, sudarė sąlygas JAV monopolizuoti pasaulio informacinę erdvę: vakarietišką — visiškai, nevakarietišką — dalinai.

Pastaruoju metu buvo sunaikinti alternatyvūs informacijos šaltiniai: vargu ar kas iš žurnalistų nori sulaukti nužudymo arba Džuliano Assanžo likimo. Tie, kurių nepavyko sunaikinti (pvz., rusų žiniasklaida), apipilti melu arba pateko į marginalinį lauką. Visus informacinio lauko objektus seka NSA. Minia (masiškas naudotojas) taip patvarkyta, kad nepajėgia suvokti tekstų (t.y. dokumentų) ir prasmių, naudodamasi vien tik paveikslėliais.

Štai kodėl vakarietiška žiniasklaida labai domisi teroristinėmis grupuotėmis (pvz., RF uždraustomis „Al-Kaida“ ir „Islamo valstybe“) ir štai kodėl pasauliui demonstruojami profesionaliai paruošti vaizdo įrašai apie islamo teroro baisumus.

Pagal šio produkto režisierių sumanymą, pasaulis turi apsiginti nuo barbarų „civilizuotų“ JAV pagalba, nesuvokdamas, jog ir teroristai, ir vakarietiški „kovotojai su terorizmu“ — vien tik skirtingi to paties globalinio valdymo subjekto demonstravimai.

Melas — Pax Americana pagrindas

Prievarta, leidžianti JAV elitui uzurpuoti pasaulio valdymą, ir melas, kurio pagalba Valstybės departamentas įteisina tai, kas jam nepatinka, tampa (jau tapo) svarbiausiomis prasmingomis Pax Americana charakteristikomis.

Melas „ypatingoje“ šalyje (o paskui — visoje Vakarų Europoje) tapo sistema. Kalbant vaizdžiai, JAV ir Briuselyje tapo norma demonstruoti baltus miltelius. Vakarų šalyse meluoja (arba klysta) jau ne atskiri personažai (kaip Kolinas Pauelas arba Barakas Obama). Šiandien didžiojoje amerikiečių-europiečių politikoje meluoja visi arba beveik visi.

Jie meluoja giliai įsitikinę ir dažnai — nuoširdžiai pasipiktinę elgesiu žmonių, nepriimančių amerikietišką „tiesą“. Taip, pavyzdžiui, elgiasi JAV atstovė ST Samanta Pauer. Meluoja, apeliuodami ne tik į tiesą, bet ir į dorovę. Antai buvęs NATO generalinis sekretorius Anders Rasmusenas savo ką tik išleistoje knygoje „Lyderiavimo valia — nepakeičiamas Amerikos vaidmuo globalinėje kovoje už laisvę“ pareiškė, kad „tik Amerikai būdinga moralinė didybė, siekiant sustabdyti pasaulio šliaužimą į chaosą“.

Vakarų žmogaus melas neturi genetinio lemtingumo. Tačiau jis visada buvo vienu svarbiausių Amerikos vertybių sisteminių reikalavimų, o šiandien tampa — kartu su prievarta — visos vakarietiškos politikos kertiniu akmeniu.

„Amerika teisi, jei ir nėra teisi“

Neseniai iš ST tribūnos nuskambėjusiuose ir rusofobija dvelkiančiuose Obamos pareiškimuose, jo pasisakymuose naujojo valstybės vadovo rinkiminės kampanijos metu, o taip pat požiūryje į spaudą pastebima naujovė, kuri nesiejama su išeinančio prezidento įsižeidimu ir netoliaregiškumu.

Ir tai yra JAV politinės sistemos ypatumas, skatinantis ne tik valstybės vadovą, bet ir kitus amerikiečių politikus vis dažniau kalbėti parodijų pačių atžvilgiu kalba.

Ypatumas tame, jog rusofobija amerikiečių politikams nėra savitikslis. Jos ūgtelėjimas — žinomo amerikiečių politinės sistemos transformavimo pasekmė po to, kai žlugo TSRS — supervalstybė, su kuria komunizmo nekenčiančios JAV stengėsi neperžengti pagarbos ribų.

Šiandien JAV ne pasaulio lyderės (nors įrodyti savo lyderiavimą iš įvairių tribūnų bando Barakas Obama, sutikdamas pasišaipymus ir dažnai —tiesiog juoką), tačiau šeimininkės pagal save sukonstruotų Vakarų. Bet proamerikietiški Vakarai niekada (juolab, šiandien) nebuvo civilizuoti.

Pagal amerikietišką valdžios formulę, kaklas valdo galvą, o uodega kraipo šunį. Tokiu būdu amerikiečių lyderius ir visas nacionalinės sistemos informacijas pradeda kraipyti visokie nei abejonių, nei analizės nepripažįstantys štampai.

„Amerika visada teisi, net jei nėra teisi“ — štai pagrindinė nuostata, kuria vadovaujamasi rikiuojant (štampuojant) dabartinės amerikiečių politikos prasmės elementus.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 7 — id: `scraped:rubaltic_lt:77c66dcc98361c54`

**Title:** „Rusų grėsmė“ — korupcijos Pabaltijyje priedanga. Penki įrodymai.

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Pastaraisiais dvejais metais Pabaltijis ginkluojasi šūkaudamas apie „grėsmę iš rytų“. Auga kariniai biudžetai, Lietuvoje grąžinama privalomoji karinė tarnyba. Aktyvus militarizavimas neapsieina be skandalų: korupcijos šešėlis pirkimų metu, netinkamas naujokų aprūpinimas ir tarnybos sąlygos. RuBaltic.Ru pateikia penkis būdingus siužetus, kaip nesąžiningi Pabaltijo kariaunos atstovai ir jų vakarietiški draugai naudoja savo tikslais „rusų grėsmę“.

Nešaudančios kulkos

Latvių šauktinė kariuomenė — „Zemesardze“ gavo netinkamus šaudymui šovinius. Vietoj treniruočių zemesargai priversti valyti šautuvus. Nekokybiškus šaudmenis pateikė Slovėnijos kompanija. Šiuo metu šalys ieško kompromiso, — pranešė Nacionalinių karinių pajėgų (NKP) vadas Raimonds Graube.

Mokymų metu zemesargai privalėjo užgrobti patrulių bazę. Kai jie pradėjo kasti žemę, kastuvėliai ėmė lūžti. Iš 30 kastuvėlių per 5 minutes sulūžo 14. Netinkamus kovai su „rusų agresija“ kinų gamybos kastuvėlius latvių šauktiniams pateikė AB „Zommers“. Kodėl konkursą laimėjo nekokybišką produkciją gaminusi firma, taip ir liko paslaptimi.

Šarvuotas „sekond-chend“

Klykiant apie „rusų grėsmę“ galima nemažai uždirbti. 2014 metų rugsėjo mėnesį Didžioji Britanija ir Latvija, kurios politikai kasdien laukia agresijos iš rytų, pasirašė kontraktą dėl 123 vikšrinių šarvuotų transporterių įsigijimo ( Combat Vehicle Reconnaissance Tracked ). Kontrakte įrašyto sandėrio suma — 48,1 mln eurų. Į šią sumą įeina remonto ir modernizavimo išlaidos, ką patvirtina britų vyriausybės tinklalapio informacija.

Jungtinė Karalystė ne tik padėjo Pabaltijo sąjungininkams, bet ir neblogai sutaupė dėka brangiai kainuojančio utilizavimo, ką be jokios diplomatijos pakomentavo britų gynybos ministras Maiklas Felonas. Pagal britų normatyvus, ši technika 2020 metais turi būti nurašyta.

Iki 249,5 mln eurų. „Papildomai įsigyjame ryšių ir ugnies valdymo priemones, o taip pat prieštankinius ginklus. Tokiu būdu 123 karinės technikos vienetai kainuoja maždaug 108 milijonus eurų,“ — išlaidų augimą komentuoja Gynybos ministerijos sekretorė spaudai Vita Briže.

Likę 149 su kaupu milijonai eurų bus skirti techniniam aptarnavimui, šaudmenims, personalo apmokymui, simuliatorių įsigijimui ir „sukūrimui Adaži naujo kliūčių ruožo“. Suma pateisinama, jei vien tik kliūčių ruožui numatytas auksinis uždulkinimas. Bet ir šiaip kova prieš „rusų grėsmę“ — amatas ypatingas, tad ir Rygos, ir Londono „kovotojams“ vertėtų numatyti priedus prie atlyginimų.

Nugalėtojas žinomas iš anksto

Kaimyninėje Lietuvoje perkant pasipriešinimui agresijai iš rytų skirtą šarvuotą techniką taip pat šmėstelėjo korupcijos šešėlis. 2015 metų rugpjūčio mėnesį vyriausybė leido Krašto apsaugos ministerijai organizuoti konkursą dėl kovinių mašinų pėstininkams įsigijimo. valstybės gynimo taryba nutarė pradėti derybas su vokiečių konsorciumu Artec dėl šarvuočių „Boxer“ pirkimo. Tai didžiausias istorijoje Lietuvos kariuomenės sandėris. Kontrakto suma — 300 mln eurų.

Šarvuočių „Boxer“ kaina gali 35 proc. viršyti kitų kompanijų pasiūlymus, tvirtino Tutkus. Krašto apsaugos ministras Juozas Olekas ir kariuomenės vadas generolas leitenantas Jonas-Vytautas Žukas kaltinimus atmetė. Brangiai kainuojantis sandėris įvyko.

Šalta tarnyba

Praėjusiais metais oficialusis Vilnius grąžino šaukimus į savo reguliarią kariuomenę. Lietuvoje buvo įvestas mišrus karinių pajėgų modelis: tarnauja profesionalūs kariškiai, tarnauja naujokai. Būtent nuo tada Dalią Grybauskaitę lydi visokiausi skandalai. Pavyzdžiui, sausio mėnesį tie naujokai, kurie netoli Pabradės buvo mokomi „stabdyti“ Rusiją, pasiuntė į šalies žiniasklaidos priemones prašymą padėti. „Pas mus labai šalta, krosnis neveikia, kojos pamėlynavo, niekas nesiruošia sutvarkyti apšildymo. Vadovybė į mūsų prašymus nekreipia dėmesio. Naktį iš ketvirtadienio į penktadienį teko miegoti esant 20 laipsnių šalčio,“ — skundžiasi naujokai. Nieko nuostabaus: „kareiviškas“ patalpas nebuvo numatyta paversti gyvenamosiomis.

Naujokų aprūpinimo sąskaita, švelniai tariant, taupoma. Kariuomenė patiria sanitarinius praradimus. Apsinuodijimo maistu ir nekokybiškos medicininės pagalbos atvejai kariuomenėje ne kartą buvo atkreipę žiniasklaidos dėmesį, sulaukė visuomenės rezonanso. Kariuomenė — ne sanatorija, — taip į kritiką atsako jos vadovybė. Žinoma, ne sanatorija, jei mokymų metu kareiviai turi miegoti pigiose palapinėse be dugnų. O tokios nakvynės pasekmės — ne tik sloga. Gegužės mėnesį vienas iš Lietuvos naujokų sugebėjo sukaupti ant savo kūno virš 100 erkių. „Jei tiksliau, į jį įsisiurbė 201 erkė. Pats mačiau. Dvi medicinos seselės traukė 40 minučių,“ — pasakoja vargšo naujoko tarnybos draugas. „Erkės mėgsta šilumą ir drėgmę, jos lenda į palapines“.

Kitais metais Lietuvos karinis biudžetas padidės 150 mln eurų, jis sudarys 725 milijonus, arba 1,77 proc. šalies BVP. Gal bent tada kareivinėse bus šilčiau, o palapinėse atsiras dugnai? Priešingu atveju, erkės, apsinuodijimai ir kitokie Lietuvos kariuomenės buities „džiaugsmai“ „iššienaus“ jos karines pajėgas dar iki „rusų įsiveržimo“.

„Auksinis“ sietelis

Lietuvos kariuomenei skirtų lėšų naudojimas apgailėtinas. 2014 metais respublikos karinės pajėgos mokėjo už įvairius virtuvės reikmenis aštuonis kartus brangiau nei rinkos sąlygomis. Lentą produktams pjaustyti kariškiai pirko už 180 eurų, kai parduotuvėje tokia lenta kainuoja 28 eurus. Už peilį duonai buvo sumokėti 142 eurai, kai „Maksimoje“ jo kaina 13 eurų. ta kariuomenė, kuri neturi palapinių su dugnais ir privalo tenkintis netinkamomis kūrenimui krosnimis, naudojasi šakute kepsniams už 184 eurus, kiaurasamčiu už 70 eurų, galąstuvu peiliams už 103 eurus, peiliu mėsai už 250 eurų, sieteliu už 161 eurą, įvairių dydžių samteliais už 243 ir 258 eurus. „Auksinius“ brangiausių Europos restoranų virtuvės reikmenis Lietuvos krašto apsaugos ministerija pirko iš mažai žinomos firmos „Nota Bene“. Beje, firma spėjo atsižymėti ir Latvijoje, kurioje tarp kitko laimėjo konkursą dėl lėktuvų vilkiko tiekimo už beveik 200 tūkst. eurų.

Lietuvos kariuomenės „auksiniai“ indai sukėlė politinio atspalvio skandalą.įsikišo Dalia Grybauskaitė.

Susigriebę Lietuvos kariškiai pabandė atgal stumtelti keblią situaciją: „auksinius“ indus grąžinti „Nota Bene“. Bet pardavėjas sutiko priimti tik šaukštus už 4 tūkst. eurų. Anuliuoti 2014 metais pasirašytą ir 174 tūkst. eurų kainuojančią sutartį kompanija atsisakė.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 8 — id: `scraped:rubaltic_lt:0cc7f52d1ff9b891`

**Title:** Golovatovas: „Žudynių sausio 13-ąją prie televizijos bokšto kaltininkas — Landsbergis“

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Kaliningrade buvo pristatyta Galinos Sapožnikovos knyga „Kas ką išdavė. Kaip buvo žudoma Tarybų Sąjunga ir kaip susiklostė likimai bandžiusių ją gelbėti“. Knygoje pasakojama, kaip buvo atkuriama Lietuvos nepriklausomybė ir apie naujos valdžios organizuotus tarybų valdžios šalininkų teismus. Pristatyme dalyvavo buvęs „Alfos“ kariškis Michailas GOLOVATOVAS. Jis yra sąraše 65 asmenų, kuriuos Lietuva įtaria įvykdžius „nusikaltimus“ 1991 metų sausį susidūrimų prie Vilniaus televizijos bokšto metu. M.Golovatovas papasakojo RuBaltic.Ru portalui, kaip tą istorinę naktį vystėsi įvykiai.

– Michailas Vasiljevičiau, 1991 metų sausio 13-osios įvykių Vilniuje metu Jūs buvote TSRS VSK 7-osios Valdybos „A“ Grupės vado pavaduotojas, turėjote papulkininkio laipsnį. Ar galima teigti, kad Jūs vadovavote „Alfos“ veiksmams Vilniuje?

– Šiai operacijai vadovavo Ačalovas (Vladislavas, TSRS gynybos ministro pavaduotojas — RuBaltic.Ru pastaba). Aš vadovavau padaliniams, veikusiems prie televizijos centro ir bokšto.

– Kokiomis jėgomis vadovavote?

– 64 karininkams ir dviem tarnybiniams šunims.

– Ką Jūs galite pasakyti apie tų dienų padėtį Lietuvoje?

– Vilniuje buvau nuo sausio 7 iki 14-osios. Atvykau traukiniu, o savo darbuotojus oro uoste sutikau sausio 10 d. Prie televizijos centro ir bokšto atlikome žvalgybą. Ir pagal štabo sprendimą pasiruošėme pravesti operaciją atlaisvinant objektus nuo juos užgrobusių asmenų, kurie vedė televizijos laidas lietuvių kalba. Mums buvo įsakyta atlaisvinti televizijos centrą ir bokštą ir sudaryti galimybes tarybinės televizijos centrinių kanalų žurnalistams vesti laidas rusų kalba.

– Jei kalbėti maksimaliai aiškiai — Jums buvo įsakyta atlaisvinti televizijos bokštą. Ir viskas?

– Taip. Atlaisvinti nuo grobikų operatorių ir studijų kambarius. Ir jei kalbėti apie televizijos bokštą, tai jo viduje vaikštinėjo ginkluoti žmonės, kurie neleido įeiti retransliatorius aptarnaujančiam personalui.

– Kas įsakė Jums pradėti operaciją?

– Perdislokuotis į Vilnių įsakė mūsų Valdybos viršininkas generolas leitenantas Jevgenijus Michailovičius Rasščepovas. Jis seniai miręs. O iš viršaus komandą davė VSK pirmininkas Vladimiras Kriučkovas. Nes tik Kriučkovo nurodymu galėjo pradėti veikti mūsų padaliniai.

– Kas Jus informavo, kad televizijos bokštą užėmė ginkluoti žmonės?

– Lietuvoje šį klausimą kuravo VSK padaliniai. Kuravo televiziją, spaudą, radiją. Jie mus informavo. Vadovavo tuo metu Lietuvos TSR saugumui generolas majoras Stanislavas Caplinas. Savo vietoje buvo ir Lietuvos TSR VSK pirmininkas, bet jis nusišalino.

– Ar operacijos metu Jūs sąveikavote su kariuomenės daliniais?

– Žinoma. Mes privalėjome atlaisvinti televizijos bokštą, įleisti darbuotojus, po to perduoti apsaugą į Vilnių įvestiems padaliniams: Pskovo divizijos desantininkams ir vidaus kariuomenės konvojaus divizijos kariškiams.

– Žinodami, jog bokštą užėmė ginkluoti žmonės, Jūs tikėjotės karinio pasipriešinimo?

– Žinoma.

– Diskutuojant apie susidūrimus prie televizijos bokšto pastoviai keliamas klausimas: ar kariškiai turėjo tuščius šovinius?

– Tai vis žodžių žaismas, kuris, gali būti, atsirado po to, kai žuvo žmonės. Ko nesakytų apie tai, kas įsakė atlaisvinti bokštą, — mes dirbome prieš civilius žmones, kurie susitelkė aplink televizijos centrą ir bokštą komendanto valandos metu. Tai nuo 1.30 iki 4 val. nakties. Nuo 24 iki 6 ryto buvo įvesta komendanto valanda. Ją įvedė Vilniaus įgulos viršininkas generolas majoras Vladimiras Uschopčikas. Prisilaikyti komendanto valandos privalėjo visi. Kariškių perdislokavimas buvo leistinas tik naudojantis slaptažodžiu. Civiliai tuo metu priešinosi kariškiams išstatydami „gyvą priedangą“.

– Ar Jūs tikėjotės susidurti su miniomis beginklių žmonių, „gyva priedanga“? Kaip pagal instrukciją turėjote į tai reaguoti?

– Tai ne instrukcija, o specialaus padalinio veiksmai užimant pastatą, kurį užgrobė teroristai, ekstremistai arba ginkluoti asmenys, pareiškiantys kažkokius savo norus ir reikalavimus. Kai mes atvykome į vietą, aplink televizijos bokštą pamatėme apie 5 tūkstančius žmonių, keletą tarybinės kariuomenės tankų T-72 ir desantininkų BMP.

– Kas pirmas atidengė ugnį?

– Kaip buvo sumanyta štabe, norint prie televizijos bokšto praskinti praėjimą, tankai turėjo šauti tuščiais sviediniais ir priversti minią išsiskirstyti.

– Į orą?

– Taip. Ir tuščiais. Kaip suprasti šūvį tuščiais? Egzistuoja šaudybų ir fejerverkų organizavimo medicininės normos ir parodymai. Pagal jas leidžiama šauti tuščiais iki 140 decibelų, t.y. kad nepakenkti civiliams. Jei šauti 210 decibelų, gali plyšti ausų plėvelės. Tačiau dar ir iki 150 decibelų galima šauti.

Mes sėdėjome su radiofikuotais šalmais dengtoje mašinoje ZIL-131. Aš įsakiau pajudėti į televizijos bokšto užnugarį. Ir, pasinaudodami kirstynių mūšio veiksmais, mes galėjome išstumdyti minią ir prasiskverbti prie galinės objekto pusės.

– Paprasčiau tariant, minią nutarėte ne išvaikyti, o aplenkti?

– Tikrai taip.

– Jūs paminėjote kirstynių mūšio veiksmus. Ar teko kautis? Pavyzdžiui, mušti buožėmis?

– Ne. Aš jau sakiau, kad mes turėjome tarnybinius šunis. Minia nuo jų traukėsi. Mes dirbome pagal įkaitų išlaisvinimo taktiką, kai būtina kuo mažiau pakenkti greta esantiems žmonėms. Kai mes patekome į pirmą aukštą, besiginanti šalis — Sąjūdžio kovotojai įjungė gaisro gesinimo sistemą. Jie paleido inertines neono dujas. Mes neturėjome kuo kvėpuoti, bet turėjome dujokaukes. Mes jas užsidėjome — atsirado galimybė atidaryti langus, išvėdinti patalpą. Mes privalėjome neleisti jiems užgesinti „kontūrą“ — jo jungiklis buvo 31-ame aukšte. „Kontūras“ — tai spinduliuojanti retransliatorių sistema, iš Vilniaus išeinanti į Latviją ir Estiją. Jei „kontūras“ bus užgesintas, jo nepavyks sutaisyti per mėnesį, net per du. Tokios jo techninės savybės.

– Kai įėjote į vidų — ką pamatėte? Ar aptikote ginkluotus kovotojus?

– Net daugiau: paėmėme iš jų penkis PM pistoletus.

– Sajūdiečiai priešinosi?

– Šaudymu — ne. Jiems nebuvo kur dingti. Iššokti jie negalėjo. Mes juos nuginklavome ir perdavėme konvojaus daliniams.

– Jūs pasakėte, kad tankai dukart iššovė tuščiais. O Jūsų grupė panaudojo ginklą?

– Ne! Masiško žmonių susibūrimo vietose naudoti ginklą draudžiama.

– Taigi, jei teisingai suprantu, Jūsų grupė nė karto neiššovė?

– Nė karto.

– Į Jus šaudė?

– Apie 4 valandą ryto gavome žinią, kad televizijos centre žuvo „Alfos“ darbuotojas Viktoras Šatskichas. Jis žuvo tik todėl, kad vaikinai negalėjo iškviesti „Greitosios pagalbos“ ir nugabenti jį į gydymo įstaigą. 40 minučių negalėjo su juo prasimušti. Jam buvo peršauti plaučiai.

– Paskutinių televizijos bokšto šturmo metinių proga lietuviškojo portalo Delfi puslapiuose pasirodė reportažas, jog Šatskichą į nugarą nušovė saviškiai.

– Tai išmislas. Kaip gali žūti rikiuotės gale buvęs karininkas? Jis pas mus tarnavo šešis mėnesius. Priekyje ėjo labiau paruošti žmonės. Šatskichas buvo jaunas ir ėjo kraštutiniu. Pasiekęs antrą aukštą jis perspėjo skyriaus viršininką: „Jevgenijau Nikolajevičiau, man bloga“. Ir griuvo. Jeigu, sakykim, į nugarą šovė saviškis, tai jis ir turėjo eiti iš paskos. Teisingai?

– O 14 aukų iš lietuvių pusės?

– Štai Jūs klausiate, ar į mus buvo šaudoma. Šaudė! Kodėl? Todėl kad matėme blyksnius gretimuose namuose. Mes priėjome prie ZIL-o. Paprašiau štabo, kad kariškių pervežimui mums atsiųstų BTR-us. Kad būtų „šarvai“. Šaudoma buvo nuo gretimų namų stogų. Konvojaus kariai ir desantininkai slėpėsi už BMD ir BTR, kuriais artinosi prie bokšto.

Atleiskite, man teko kariauti ir aš galiu atskirti šūvius, paleistus iš medžioklinio šautuvo arba „mosino“, nuo automato. Iš automatų nešaudė. Šaudė iš visokių ginklų, net mažo kalibro. Matėme blyksnius. Štabas mums atsiuntė „šarvus“, mes pasikrovėme. Tačiau kai mes važiavome nuo televizijos bokšto link miesto karinio komisariato, nuo virš mūsų buvusių viadukų ant BTR-ų buvo mėtomi bordiūrų akmenys. Jei mes būtume važiavę dengtomis mašinomis, aukų nebūtų išvengta — ant brezento būtų kritę akmenys iki 300-400 kilogramų svorio.

– Vytautas Landsbergis sakė, kad Jūs dar ruošėtės šturmuoti Seimą, todėl kitą dieną jis pats tarėsi su kariškiais, kad šturmo nebūtų...

– Su kuo tarėsi? Nesąmonė, kad jis su kuo nors galėjo tartis. Mus kaltina siekusius jėga pakeisti konstitucinę santvarką. Mes ką — šturmavome parlamentą? Šturmavome Ministrų Tarybą? Ne. Mes vykdėme įsakymus, liečiančius sąjunginę nuosavybę. Televizijos centras ir bokštas priklausė sąjunginiam Centrui.

– Ar kraštutiniu atveju buvo planuota šturmuoti Seimą? Lietuviai labai bijojo, kad bus puolamas Seimas, statė barikadas.

– Ir vėl: pulti pastatus, kurie nekėlė... Negi mes bandėme atimti iš deputatų neliečiamybę? Mes juos išmetėme? Nesąmonė! Jie buvo dirbantys Seimo deputatai, kuriuos išrinko Lietuvos TSR piliečiai.

– Jūsų manymu, ar teisinga buvo įvesti į Vilnių tankus ir šiaip sunkiąją techniką?

– Egzistuoja su jokiais nusikaltimais sąlyčių neturinčios situacijos. Civiliai žmonės neturi vaikščioti mieste arba šiaip gyvenvietėse iš anksto paskelbtu laiku. Tokiu būdu buvo tikėtasi, kad šarvuotos technikos judėjimo metu gatvės bus laisvos. Bet Landsbergis ragino: išeikite, ginkite! Taigi kas kaltas?

– Kaip Jūs tada vertinote Lietuvos vadovybės politiką?

– Jei kas nors sako „Aš — karalius“, — priešinga pusė taip pat privalo suvokti, kad jis karalius. Būdamas kariškis aš žinojau, kad jeigu man Jazovas (Dmitrijus, TSRS gynybos ministras — RuBaltic.Ru pastaba) arba Kriučkovas įsakė, vadinasi, aš tikėjau, jog Lietuva — Tarybų Sąjunga. Kad nėra kažkokios ten respublikos, priėmusios 1938 metų konstituciją. Aš vykau su tarybiniu pasu, atsiskaičiau tarybiniais pinigais, apsistodavau Tarybų Sąjungos atributika papuoštuose viešbučiuose. Ir savo veiksmus vertinau kaip teisėtus.

– Į lietuvių argumentus nekreipėte dėmesio?

– Kaip aš galiu kreipti dėmesį sėdėdamas štabe pasitarime, kurį veda armijos generolas? Jis sako, jog ministras gavo vyriausiojo Tarybos Sąjungos kariuomenės vado nurodymą atlaisvinti televizijos centrą ir bokštą. Aš vykdžiau pagal karinius apskaičiavimus patvirtintus planus.

– Ar teko susidurti su Landsbergiu?

– Jis buvo atvykęs į Maskvą 1991-1992 metais. Kremliuje buvo susitikęs su Jelcinu. Koržakovas (Aleksandras, RF prezidento Saugumo tarnybos 1991-1996 m. vadovas — RuBaltic.Ru pastaba) sakė man, kad kiekvieno susitikimo metu klausė: „O kodėl Golovatovas iki šiol tarnauja?“ O šiaip Landsbergį aš tik per televizorių mačiau. Į pensiją išėjau 1992 metais būdamas 42 metų.

– Egzistuoja informacija, kad dabartinė Lietuvos prezidentė Dalia Grybauskaitė galėjo anais laikais turėti ryšių su VSK. Ar Jūs tada ką nors apie ją girdėjote?

– Neteko su ja susidurti. Tik girdėjau jos pasisakymus, jog Landsbergis iškovojo Lietuvai laisvę, o ji išplėš iš Rusijos kompensaciją už Lietuvos okupaciją.

– Neseniai Lietuva atnaujino „Sausio 13-osios bylos“ tyrimą. Jūsų manymu, ar turi Lietuvos visuomenė teisę reikalauti anų įvykių tyrimo?

– Ji turi reikalauti, suprantate? Jelcino nurodymu Lietuvai buvo perduoti 37 tomai baudžiamosios bylos, kurią tyrė tarybinė karo prokuratūra — ir nutraukė ją tarybinių kariškių atžvilgiu, nes nerado jų kaltės dėl žmonių žūties. Medžiagą perdavė TSRS generalinis prokuroras Nikolajus Trubinas. Vadovaudamasi šiais dokumentais Lietuva nuteisė šešis žmones, taip vadinamus „raudonuosius profesorius“ (buvusius lojalius Maskvai Lietuvos Kompartijos funkcionierius — RuBaltic.Ru pastaba). Vadovaudamasi tais pačiais dokumentais ir remdamasi neseniai priimtomis baudžiamųjų įstatymų pataisomis, Lietuva dabar mums inkriminuoja senaties terminų neturinčius karinius nusikaltimus. O kokie mano kariniai nusikaltimai arba nusikaltimai žmogiškumui? Aš ką nors nužudžiau? Suvažinėjau?

– Anksčiau buvo pastangos iškviesti Jus pas tardytojus, įvilioti į Lietuvą?

– Aš buvau apklaustas 1991-1992 metais. Daviau parodymus TSRS prokuratūrai. Daugiau jokių pranešimų negavau iki 2011 metų, kai Lietuvos reikalavimu buvau sulaikytas Austrijoje. Austrų teisinė sistema mane išlaisvino, aš išvykau į Maskvą. Austrai mano veiksmuose nerado nusikalstamos veikos.

– Šiuo metu Lietuvos teismai prisikabino prie dviejų žmonių: Genadijaus Ivanovo ir buvusio tankisto kaliningradiečio Jurijaus Melio. Jūsų manymu, ko jie sulauks? Ar yra šansų, kad bus išlaisvinti?

– Aš jaučiuosi panašiai, kaip jie. Tik Melis Vilniaus izoliatoriaus vienutėje kankinamas 2,5 metų, o aš gyvenu Rusijoje. Tačiau man apribojo teises: aš negaliu išvykti į užsienį todėl, kad Lietuvos generalinis prokuroras neteisėtai pasirašė mano arešto orderį. Man net pranešimo apie inkriminuojamus nusikaltimus neatsiuntė. Visiškai įsitikinęs, kad Ivanovas ir Melis bus išlaisvinti ir pastarasis sugrįš į tėvynę. Norite paklausti — kada?

– Jūs galite prognozuoti?

– Na, įlįsti į Dalios Grybauskaitės galvą negaliu. Visa tai politizuota. Grybauskaitė taip elgiasi todėl, kad privalo parodyti, kokia ji gera, o Rusija esą Lietuvai turi išmokėti dešimtis milijonų dolerių.

– Jūsų manymu, kas turi atsakyti už 1991 metų sausio 13-osios aukas prie Vilniaus televizijos bokšto?

– O aš galiu paklausti: ar Paleckis suklydo pasakęs, kad savi šaudė į savus? Aš patvirtinu: taip, šaudė. Aš tai mačiau. Baudžiamosios bylos tomuose yra filmavimo ir kitos medžiagos, patvirtinančios, jog žmonės žuvo nuo „mosino“ šautuvo šūvių. Kas iš mūsiškių galėjo iš tokių šautuvų pyškinti?

O kas dėl atsakomybės, tai Vilniuje veikė komendanto valanda. Kas ragino gyventojus išeiti į gatves, atvykti iš provincijos į miestą ir ginti demokratiją? Butkevičius ir Landsbergis. Ar mes galėjome žinoti, kad buvo priimtas sprendimas, jog Lietuva — nepriklausoma valstybė? Ne. TSRS kariškiai to nežinojo. Argi Lietuva turėjo savo pasus, valiutą? Ar turėjo savo kariuomenę? Lietuva naudojosi tarybiniu biudžetu iki 1992 metų. Landsbergis išstatė prieš reguliarią kariuomenę „gyvąją priedangą“. Kaltas jis. Kaip ir Butkevičius, organizavęs prie televizijos bokšto žudynes.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 9 — id: `scraped:rubaltic_lt:1c13978d752d0bef`

**Title:** Europos hospisas: Pabaltijis įžengė į gyvenimo užbaigimo amžių

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Pagrindinės santykių su Pabaltijo šalimis problemos slypi tame, jog Lietuva, Latvija ir Estija — senstančios ir mirštančios tautos. Optimalus bendravimo su jomis variantas — netrukdyti Pabaltijui mirti, nekreipti dėmesio į jo senatvišką barningumą ir neužsikrauti ant savo pečių atsakomybės už būsimų senelių namų išlaikymą.

Pagal neseniai paviešintą Eurostato pranešimą apie Europos Sąjungos demografinę padėtį, Pabaltijo šalys pirmauja gyventojų skaičiaus mažėjimo klausimu, o taip pat mirtingumas jose lenkia gimstamumą. Bendro mirtingumo rodiklis, nei Lietuvoje ir Latvijoje, tarp ES šalių aukštesnis tik Bulgarijoje.

Remdamasis šia dinamika Eurostatas skelbia katastrofiškas Pabaltijui prognozes apie jų tautų ateitį. Po 1991 metų praradusios trečdalį gyventojų Latvija ir Lietuva iki šio amžiaus vidurio dar praras: Latvija — 31 proc., Lietuva — 38 proc. gyventojų.

Pabaltijis vis labiau virsta senelių namais. Naujos kartos nenori gyventi šiame regione. Dauguma Lietuvos, Latvijos ir Estijos jaunimo pareiškia nenorinti atsisveikinti su savo šalimis. Ir išvyksta. Lietuvos statistikos departamento duomenimis, 52 procentai 2016 metų pirmoje pusėje išvykusių iš Lietuvos emigrantų — jauni, 18–35 metų žmonės. Daugumai Lietuvos, Latvijos ir Estijos jaunų gyventojų nėra kas veikti savo šalyse. Ką čia veikti į gyvenimą žengiančiam jaunimui, jei jų tėvynės virsta senelių namais?

Beliekančiųjų gyvenimo tikslas — rami, nors ir varginga senatvė. Po to, kai Pabaltijo šalys įstojo į Europos Sąjungą ir NATO, paplito kalbos apie jų nacionalinę idėją, ateitį, ir ta išsvajota ateitis — „sugrįžimas į Europą“ joms pagaliau nusišypsojo. Naujų švytinčių horizontų Pabaltijo politikai savo tautoms taip ir nepasiūlė, tačiau užslėpta nacionalinė idėja Lietuvoje, Latvijoje ir Estijoje vis dėlto egzistuoja.

Pabaltijis jau prieš keletą metų įžengė į gyvenimo užbaigimo amžių. Jis — pensininkas, „pensijines pašalpas“ gaunantis iš Europos socialinio fondo, regioninio ES vystymosi fondo, o taip pat įvairių lengvatų sulaukiantis iš Briuselio ir Vašingtono. Be šių „pensijų“, lengvatų ir priemokų Pabaltijis neišgyventų. Nuosavas mažytis darželis — kadaise išsivysčiusios ekonomikos likutis — jo neišmaitintų, o dirbti ir uždirbti savo jėgomis jau sveikata neleidžia: senstantis organizmas nusilpęs, jį nukraujavo emigracija — jeigu Pabaltijyje ir atsirastų darbo vietų, nebūtų kas jose dirbtų.

Pakeisti šią tendenciją jau neįmanoma. Gyvenimas iš Pabaltijo respublikų išskrenda lėktuvais su bedarbiais. Šios šalys neturi ateities, nes ateityje nesimato naujų kartų.

Žvelgiant iš šios varpinės tampa aiškios ir suprantamos bendravimo su Pabaltiju problemos. Vietinė valdančioji klasė kaulina iš Vakarų karinio NATO dalyvavimo ir regiono militarizavimo didinimo, visa tai aiškina „rusų grėsme“ laisvoms ir demokratinėms Lietuvai, Latvijai ir Estijai, tačiau įrodymui nesugeba surasti nė vieno fakto. Pabaltijiečiams labai reikalingas Vakarų sąjungininkų dėmesys, o priminti, kad jie dar gyvi, lengviausia klykiant apie „baisią ir klastingą Rusiją“.

Lietuvos diplomatija jau keletą metų reikalauja, kad į šalies teritoriją būtų įvežta sunkioji ginkluotė, kad joje dislokuotųsi amerikiečių, kanadiečių, lenkų ir t.t. kariškiai, kad būtų atsisakyta Fundamentalaus Rusijos ir NATO akto ir vyktų pastovių NATO sausumos kariuomenės bazių statyba. Ir tuo metu Lietuvos URM vadovas pareiškia, jog būtent Rusija provokuoja regione karinę įtampą ir skuba militarizuoti savo su NATO pasienį. Pabaltijis laiko save civilizuoto demokratiško vystymosi pavyzdžiu, į kurį turi lygiuotis kitos buvusios tarybinės respublikos, nors prasidėjo pabaltijietiška „demokratija“ tuo, jog Latvija ir Estija nesuteikė trečdaliui savo gyventojų elementariausių teisių ir galimybės balsuoti. Ir tai jau senatvės sklerozė: nepamena, kuo neseniai užsiiminėjo.

Lietuva paskelbė informacinį ir diplomatinį karą Baltarusijos AE, klykia visai Europai, reikalaudama sustabdyti naujos atominės elektrinės statybą, vis pikčiau reaguodama į TATENA ekspertų raminimus. Čia pasireiškia senatvės marazmas: aš čia sėdžiu ant suolelio, šildau savo senus kaulelius, savo atominę seniai pramiegojau, o mano kaimynas, man matant, drįsta statyti.

Pabaltijo politikai net ne sapnuose mato „žaliuosius žmogeliukus“, tvirtina, kad virš jų, radarų nepasiekiami, skraido rusų sraigtasparniai, mato Putino atsiųstus tautos priešus ir vasarą į Rusiją poilsiauti vykusių moksleivių penktąją koloną. Toks reiškinys medicinoje vadinamas „senatviška demencija“, o liaudyje — marazmu.

Iš čia begaliniai patirtų kančių ir pastovios priespaudos prisiminimai, o taip pat nesibaigiančios pretenzijos Rusijai už viską, o ypač — už „sovietinę okupaciją“. Taip elgiasi irzlus ir senstantis pensininkas, kuris jau nieko neplanuoja ir nesuvokia dabarties realijų, tačiau įsikibęs laiko atmintyje visas praeities nuoskaudas.

Lietuva, Latvija ir Estija — būtojo laiko tautos: jų oficialios ideologijos pagrindas — „jeigu“. Jeigu nebūtų žiauriai puldinėję kryžiuočiai, jeigu nebūtų egzistavusi Lietuvos ir Lenkijos Liublino unija, ir, svarbiausia, jei ne „sovietinė okupacija“... Tai būtų buvęs gyvenimėlis! Tada būtų gyventa kaip Skandinavija ir, žinoma, kaip Danija, Švedija ir Suomija.

Galima jų paklausti: kodėl gi dabar negyvenate kaip Švedija ir Suomija, o gyvenimo lygis jau be „sovietinės okupacijos“ vis labiau atsilieka nuo Skandinavijos? Galima paklausti: jeigu jūs norėjote gyventi kaip Suomija, tai kodėl nesielgėte kaip ši šalis? Turėdami ryšius su galinga Rusijos rinka jūs turėjote galimybę praturtėti, o būdami tarptautinėje arenoje neutralūs galėjote pelnyti ir Vakarų, ir Rytų pagarbą kaip tarpininkės tarp Rusijos, JAV ir Europos. Būtent taip elgdamasi Suomija, į kurią jūs norite lygiuotis, ir tapo viena turtingiausių ir gerbiamų pasaulio šalių.

Apie tai būtų galima paklausti, bet ar reikia klausti? Ar verta varginti senstantį ir ligotą žmogų? Jis vis tiek nenorės nieko girdėti.

Rusija pastaraisiais metais santykiuose su Lietuva, Latvija ir Estija taip ir elgiasi. Begalinius rytų kaimyno palyginimus su Trečiuoju reichu, jo vadinimus „teroristine valstybe“, pirmųjų Pabaltijo šalių asmenų pareiškimus, jog Rusijos prezidentas yra paranojikas — visą šį šunų prie Baltijos krantų lojimą Maskva paniekinamai ignoruoja. tik rusų kroviniai patyliukais persikelia iš Pabaltijo šalių uostų į savuosius, o pabaltijiečių pieno, mėsos ir žuvies konservų gamintojai bankrutuoja praradę rytų rinką.

Strategiškai Rusija, sąmoningai pamiršdama Pabaltijį ir išbraukdama Lietuvą, Latviją ir Estiją iš pasaulio užsienio politikos vaizdo, vien tik išlošia. Jeigu šiandien Maskva neturi rimtų santykių su Pabaltiju, vadinasi rytoj jai nereikės sodinti jį sau ant sprando ir maitinti, palaikant savo donoro krauju jo vargingą egzistavimą.

Lietuva, Latvija ir Estija katastrofiškai praranda ekonomiškai aktyvius gyventojus. Darbingi ir mokesčius mokantys piliečiai išvyksta iš šių šalių. Praeis keleri metai, ir Pabaltijyje beliks tik biudžetininkai ir pensininkai. O iš kokių šaltinių bus mokamos pensijos, jei dauguma mokesčių mokėtojų išvyks? Be to, regionas pajus paaštrėjusį deficitą specialistų, pajėgių palaikyti socialinės infrastruktūros egzistavimą: iš Pabaltijo rekordiniai tempais skuodžia kvalifikuoti darbuotojai, tame tarpe ir gydytojai.

Tokiai situacijai besiklostant, kai rekordinės depopuliacijos ir „demografinės duobės“ pasekmes Lietuva, Latvija ir Estija pajus visu pilnumu, šios šalys fiziškai nesugebės egzistuoti. Ir tada jau nepadės tuščių puodų eitynės, bado streikai, alkstančiųjų susideginimai ir praradusių medicininę pagalbą pensininkų maldavimai — prireiks ne dabartinių eurofondų dotacijų, sudarančių tik iki ketvirtadalio Pabaltijo respublikų BVP.

Ir kas gi užsiims tokia tarptautine labdarybe? Kas pasodins sau ant sprando milijoninę nuskurdusią teritoriją? Rusijos ir Baltarusijos laimei — ne jos. Pabaltijis per ketvirtį potarybinio amžiaus ryžtingai nutraukė visus ryšius su Rytais, paskelbė ten gyvenančius „juodnugariais“, o save — neatskiriama Vakarų dalimi. Na, o jei jis jų neatskiriama dalis, lai Vakarai jį ir gelbsti.

Lai Europos senelių prieglaudą maitina ir perpila jai kraują Vokietija, JAV, Lenkija, Suomija — bet kas, tik ne „okupantų palikuonys“. Tiesa, šios šalys gali pareikšti to nedarysiančios — jei esą Pabaltijis nepateko į globalią rinką ir nesugebėjo išgyventi jų liberaliniame laisvame pasaulyje, tai jo problemos. Tada mirti Pabaltijui teks ne ilgai ir be skausmo, o skausmingai ir greit. Orios ir tylios europietiškos senatvės nepavyks sulaukti.

Tačiau iš tiesų tai bus Pabaltijo problemos. Ne Europos, ne Amerikos ir jau tikrai ne Rusijos.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 10 — id: `scraped:rubaltic_lt:0fd09e79b45e2a8d`

**Title:** Pavydas ir neviltis: kodėl Pabaltijis nekenčia Rusijos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Beprotiška Pabaltijo politikų rusofobija aiškinama tuo, kad Rusija po TSRS subyrėjimo išgyveno ir vystosi, o Pabaltijo šalys degraduoja ir miršta. Tos buvusios TSRS respublikos, kurios pasirinko išsigelbėjimą ir senų integracijos ryšių atnaujinimą — Rusija, Baltarusija, Kazachstanas, — ramiai žvelgia į ateitį, o Pabaltijis neturi ateities: tai suvokdami vietiniai „patriotai“ bejėgiškai niršta ir vis dar skleidžia samanotą perestroikos laikų mitą, kad Rusija ne šiandien ryt nudvės patvory nuo degtinės.

Nė vienas žmogaus kūno organas negali egzistuoti be viso organizmo. Negali gyvuoti nuo kūno atskirta ranka, tik fantastikoje gali protauti nupjauta galva, tik Gogolio fantazijos nosis galėjo vaikštinėti Nevos prospektu.

Panašiai klostėsi reikalai Tarybų Sąjungoje, kurios ekonomiką sudarė vientisas sudėtingas organizmas — jame kiekvienos respublikos ekonomika atliko savas funkcijas, turėjo savą specializaciją, veikė kaip sudėtinė dalis ir buvo tūkstančiais struktūrinių ryšių integruota į bendrą tarybinę ekonomiką.

Ir todėl žlugus Tarybų Sąjungai atskiri bendro kūno organai negalėjo egzistuoti — potarybinę erdvę apėmė visuotinė ekonominė ir socialinė krizė, kurios pasekmės iki šiol galutinai neįveiktos. Tuo įdomiau palyginti, kuo buvusios tarybinės respublikos gyvena po vientisos ekonominės erdvės sunaikinimo — 25 metus kurdamos savas nacionalines ekonomikas.

Apie tai kalba neseniai paviešinta statistika, kuri Tarybų Sąjungoje buvo užslaptinta (turbūt nenorint diskredituoti socialistinę santvarką ir pakenkti tautų draugystei). Iš 15 tarybinių respublikų tik dvi — Rusija ir Baltarusija — daugiau gamino nei vartojo. Bendrasis vidaus produktas vienam gyventojui RTFSR siekė 17,5 tūkstančio dolerių, o vartojimas vienam žmogui metuose — 11,8 tūkstančio dolerių.

Kur kasmet dingdavo likę 5,7 tūkstančio? Ieškant atsakymo į šį klausimą pakanka susipažinti su kitų respublikų duomenimis. Tarybų Lietuva per metus vienam gyventojui gamino produkcijos už 13 tūkst. dolerių, o vartojo už 23,3 tūkst. Iš kur buvo imami trūkstantieji 10,3 tūkst.? aišku, iš kur: iš sąjunginio Centro investicijų į Lietuvos kelius, visuotinį dujofikavimą, elektrifikavimą, melioraciją ir atominę stotį.

Panaši situacija klostėsi ir kaimyninėje Latvijoje: Latvijos TSR BVP sudarė 16,5 tūkst. dolerių, o vartojimas — 26,9 tūkst. Iš kur trūkstantieji 13 tūkst.? Aišku, iš kur: iš „rusiškų kiaulių“, dėka kurių pastangų ant Rygos prekystalių puikavosi rūkyta dešra, o tolimų Rusijos vietovių gyventojai stovėjo ilgose eilėse norėdami nusipirkti kremzlių.

Tokia situacija buvo susiklosčiusi visose tarybinėse respublikose, išskyrus Baltarusiją, kuri gamino daugiau, negu vartojo, ir iš dalies Ukrainoje, kuri turėjo beveik „nulį“. Ukrainos TSR buvo sukoncentruotas trečdalis TSRS pramonės potencialo, Ukrainos BVP sudarė apie trečdalį RTFSR BVP, o pragyvenimo lygis Ukrainoje buvo aukštesnis negu Rusijoje. Užtat šiandien Ukrainos ekonomika — 9 proc. Rusijos, o pragyvenimo lygis kelis kartus žemesnis nei Rusijoje. Vidutinis atlyginimas Ukrainoje — 156 eurai —mažiausias Europoje, o pagal BVP dabartinė Ukraina — viena iš vargingiausių pasaulio šalių.

Todėl subyrėjus Tarybų Sąjungai baigėsi ir dosnios Centro investicijos, kurių pagrindine „donore“ buvo RTFSR.

Tai visiškai nereiškia, kad Rusijai buvo naudingas TSRS subyrėjimas — dėl didžiulės bendros ekonomikos sunaikinimo Rusija patyrė tokią pat katastrofą kaip ir kitos respublikos. Tačiau jeigu Jelcino teiginyje „pakaks maitinti pakrančius“ buvo galima įžvelgti bent dalelę tiesos, tai kaip suprasti pakrančių separatistų argumentaciją, jog „jie valgo mūsų lašinius“?

Išcentriniai judėjimai tarybinėse respublikose vadovavosi paprastu šūkiu: „Lik sveika, nepraustoji Rusija“ — jų dauguma (visų pirma sočiai šertas ir save europietišku matantis Pabaltijis) 1991 metais paskelbė, jog jiems geriau išsiskirti su „šiais aptingusiais, amžinai girtais rusais“. Rusija vis tiek miršta ir ryt poryt numirs: geriau laikytis nuo jos kuo toliau ir tapti Vakarų dalimi — atiduoti tai, kas brangiausia, — nepriklausomybę — turtingiems ir veiksmingiems, o ne elgetoms ir girtuokliams.

Pasaulinio banko duomenimis, Rusijos BVP pagal pirkimo galimybes 2015 metais sudarė 2,5 trilijonų dolerių — tai sudaro 121,9 proc. 1991 metų RTFSR lygio. Rusijos BVP vienam gyventojui sudaro 25,4 tūkst. dolerių — tai pusantro karto daugiau nei RTFSR.

Kai Pabaltijis bėgo iš TSRS, Sąjūdžio ir Liaudies frontų lyderiai įtikinėjo gyventojus, jog netrukus jie gyvens kaip švedai, danai ir suomiai. Kaip tai atrodo dabar, prieš 25 metus išlindus iš po „okupanto bato“? Šiandien vartojimo lygis Lietuvoje, Latvijoje ir Estijoje lygus vidutiniam Rusijos. Bet juk tarybiniais laikais vartojimo lygis Lietuvoje ir Latvijoje buvo du kartus, o Estijoje — tris kartus didesnis nei RTFSR!

Kaip matome, Pabaltijo pragyvenimo lygis, lyginant su Rusija, per ketvirtį amžiaus beveik susilygino. O tuo metu Skandinavijos šalių BVP, vartojimas, vidutinis darbo užmokestis ir kiti socialinio gerbuvio rodikliai tapo vis labiau nepasiekiami. Lietuva manė, kad „be ruso“ gyvens kaip Danija? Šiandien vidutinis darbo užmokestis Danijoje keturis kartus didesnis negu Lietuvoje. Sąjūdžio vadai teigė, kad jų pastangomis žmonės gyvens kaip Suomijoje? Suomiai uždirba taip pat keturis kartus daugiau negu lietuviai. Latvių atlyginimai 4,5 karto mažesni nei švedų. Ir tai tik vidutiniai darbo užmokesčiai — kai kurių profesijų Skandinavijos ir Pabaltijo atlyginimai skiriasi šešis-septynis kartus. Ir tas skirtumas tarp regionų per ketvirtį amžiaus vien tik didėjo.

Jau kitame dešimtmetyje visa tai ims badyti akis, nes įsigalios naujas ES biudžetas, kuriame nebus Rytų Europą palaikančio Didžiosios Britanijos įnašo.

Be kiekybinių rodiklių egzistuoja ir kokybiniai. Rusija šiandien stato raketas ir lėktuvus, naujus kosmodromus, atveria naujus atominės energetikos panaudojimo galimybių horizontus. O kur „Baltijos tigrai“? Kur jų išgirtoji inovacinė ekonomika, praktikoje besilaikanti dėka Skandinavijos bankų kreditų? Kur jų tarybiniais laikais garsėjusi aukštų technologijų gamyba? Nieko neliko. Nėra elektros technikos gamyklų ir fabrikų, konstruktorių biurų. Tarybiniais metais veikė Rygos civilinės aviacijos inžinierių institutas. Ar galima įsivaizduoti, jog Latvija šiandien stato lėktuvus?

Visa tai ir gimdo liguistą rusofobiją, kuri pirma skleidė pasibjaurėjimą „girtiems tinginiams rusams“, o vėliau virto isteriška neapykanta „rusų agresoriams“.

Dabar Pabaltijo rusofobija — net komplimentas Rusijai, nes dabar rusai jau ne girtuokliai ir ne tinginiai, jie — grėsmė pasauliui; jei jų „nestabdyti“, jie užgrobs visą Europą.

Ši liguista rusofobija — svetimo ėjimo pirmyn ir savo trepsenimo vietoje derinys. „Lietuvos demokratijos tėvas“ ir Pabaltijo rusofobijos klasikas Vytautas Landsbergis po šių metų Olimpiados lygina Rusijos valstybinę sporto politiką su fašistinės Vokietijos sporto politika. Dėdulė pabrėžia, jog nežino kitos šalies, kurioje sportas būtų taip ideologizuotas, kaip Rusijoje, ir prieina išvados, kad tai reikalinga norint palaikyti „imperiškas ambicijas“.

Ir kodėl vėl „tautos tėvui“ pykčio paūmėjimas? Pirma, todėl, kad nepaisant „Rusijos stabdytojų“ pastangų ir psichologinio spaudimo šios šalies rinktinė puikiai pasirodė Olimpiadoje ir užėmė ketvirtąją vietą. Antra, todėl kad išdidi euroatlantinė Lietuva turėjo tenkintis tik 64-ąja vieta.

Gyventojų skaičiaus augimas, beveik nulinė emigracija ir aukštas gimstamumas šiandien lydi tik Rusiją, Baltarusiją ir Kazachstaną.

O tuomet „europietišką kelią“ pasirinkusios ir Lietuvos, Latvijos ir Estijos patirtimi besivadovaujančios Ukraina ir Moldavija miršta. Ir miršta ne perkeltine prasme, bet realiai, fiziškai. Todėl jos ir siunta, ir kliedi — Rusiją esą ryt poryt mirs.

Ir Pabaltijis, ir ypač jo virusu užsikrėtusi Ukraina gyvena iliuzija, jog Rusija stovi ant bedugnės krašto, jog ji miršta — žodį „miršta“ vietiniai patriotai kartoja per dieną šimtą kartų. Deja, kol kas jie dar nesugeba suvokti, kad iš tikrųjų miršta patys.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 11 — id: `scraped:rubaltic_lt:9dc0ebfad0db5deb`

**Title:** Maskvoje pristatyta tiesa apie Lietuvos «kovą už nepriklausomybę»

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Pagrindinė grėsmė dabartinei Lietuvai – ne politikos provincialumas, ne karinė įtampa regione ir net ne ekonominis sąstingis. Pagrindinė grėsmė – netolimos praeities tiesa, potarybinės Lietuvos gimimo istorija, kuri užbraukia visą šios Pabaltijo respublikos idėjinį pagrindą. Būtent tokia peršasi išvada perskaičius ką tik pristatytą Galinos Sapožnikovos knygą «Kas ką išdavė. Kaip buvo žudoma TSRS ir ko sulaukė ją bandę gelbėti žmonės».

«APLINK VISKAS LAUŽOMA, ŠOKINĖJAMA»

Knygos autorei Pabaltijis – ne atsitiktinis regionas. 1988 metais baigusi Leningrado valstybinio universiteto žurnalistikos fakultetą G.Sapožnikova buvo nukreipta dirbti «Molodiož Estoniji» laikraštyje, o jau po metų tapo etatine «Komsomolskaja pravda» korespondente Estijai, Suomijai ir Švedijai. Taigi tapo visų TSRS griūties Pabaltijyje įvykių liudininke. Ši knyga – ne pirmas G.Sapožnikovos darbas Pabaltijo respublikų istorijos tema – 2009 m. ji išleido knygą «Arnoldas Meris – paskutinis estų didvyris», skirtą žinomam tarybiniam politikui, pirmam estų tautybės Tarybų Sąjungos Didvyriui, kuris potarybiniu laikotarpiu, pritariant naujosios Estijos vadovybei, buvo žiauriai šmeižiamas.

Šį kartą Rusijos aukso plunksna (tokią Žurnalistų sąjungos premiją knygos autorė pelnė 2004 m.) po daugybės pokalbių su amžininkais išleido knygą apie kitus didvyrius – apie tuos, kurie neišdavė savo idealų ir šalies lemtingais 1990-aisiais pertvarkos metais. Ir, žinoma, apie antididvyrius, kurie 1980–1990 metais užėmė Lietuvoje aukštus postus (ir daugelis iš jų juose tebelieka).

«Kas ką išdavė. Kaip buvo žudoma TSRS ir ko sulaukė ją bandę gelbėti žmonės» – tai ne šiaip sau dėmesio vertas istorijų aprašymas. Tai dar ir nuosprendis «okupaciniams mitams» ir legendoms apie «didvyrišką nacionalinio išsivadavimo iš TSRS kovą» ne tik Lietuvoje, bet ir visame Pabaltijyje. Štai kelios knygos ištraukos.

Taip apie dramatiškus 1991 m. įvykius kalbėjo juose dalyvavęs profesorius, juridinių mokslų daktaras, o vėliau «demokratinės» Lietuvos politinis kalinys Ivanas Kučerovas.

O štai prisiminimai apie 1991 m. sausio įvykius prie Vilniaus televizijos bokšto pirmojo LKP CK (TSKP platformoje) sekretoriaus Mykolo Burokevičiaus.

«Reikia atkreipti dėmesį į tai, kad į tuos žmones, kurie žuvo, šaudė patys nacionalistai. Čia negalima visą kaltę suversti kariuomenei. Tai būtų nusikaltimas ir istorinės tiesos iškraipymas. Varenikovas ir Kuzminas stengėsi išsaugoti abiejų pusių žmones. Kaip viskas įvyko, dabar niekas negali atsakyti... Tačiau panaudoti ginklą garnizono vadas neįsakė. Tai aš jums patvirtinu. Aš turėjau telefoną VČ, kuriuo galėjau skambinti ir Maskvai, ir kariškiams, taigi – kariškiai patys man tuo telefonu skambino ir klausė, ką jiems daryti? Aplink laužo viską, šokinėja».

«TAI TAS PATS MAIDANAS»

«Šokinėja» – dabartinėmis sąlygomis simbolinė pastaba. Iš tikrųjų, įsimintini Ukrainos maidano įvykiai labai primena (visomis prasmėmis) 1991-ųjų įvykius Lietuvoje: tie patys mįslingi snaiperiai, ritualinės aukos, kaltinimai Maskvos adresu, Vakarų globa, teatrališkumas ir banali «kovos su imperija» rusofobija.

«Pirmoji knygos dalis skirta 1991 m. sausio įvykiams Vilniuje. Aš nepaliečiau to, kas iš tikrųjų vyko, technologijos. Aš pasistengiau suteikti maksimalią laisvę ir duoti žodį tų įvykių dalyviams bei stebėtojams, tačiau ką aš supratau be jokių abejonių – susidūriau su vienu iš bjauriausių istorijos falsifikavimų. Ypač tai tapo akivaizdu pamačius televizorių ekranuose Kijevo maidaną.

Kiti dalyviai sutiko su tokiu Vilniaus įvykių vertinimu, o dalyvavo aptarime praktiškai tik tų įvykių Lietuvoje liudytojai: buvęs «Alfos» grupės vadas Mochailas Golovatovas, kuris 2011 m. vasarą Lietuvos prašymu buvo areštuotas Vienoje ir apkaltintas dalyvavęs 1991 metų sausio 13 d. įvykiuose Vilniuje; vienas iš «raudonųjų» politkalinių profesorius Juozas Jermalavičius; paskutinis Lietuvos TSR prokuroras, justicijos generolas majoras Antanas Petrauskas; kosminės kariuomenės generolas majoras, pertvarkos metu dirbęs Lietuvos Kompartijos CK sekretoriumi Algimantas Naudžiūnas.

Beje, anuos Lietuvos įvykius vadinti «maidanu» – politinis simboliškumas. Ne todėl, kad nesimato lygiagretumo – sutapimas šimtaprocentinis. Tik va maidano įvykiai – pakartojimas to, kas vyko Vilniuje. «Praėjo 25 metai. Kol mes gyvi, norim įvertinti ir tai, kas vyksta šiandien. O tai tas pats maidanas», – pareiškė knygos pristatymo metu Maskvoje rugpjūčio 16 d. buvęs «Alfos» grupės vadas Michailas Golovatovas.

«BANDĖ VISKĄ DARYTI, KAD KNYGA NEPASIRODYTŲ»

Praktika – tiesos kriterijus. Marksizmas dabar laikomas pasenusiu, tačiau atėję į knygos pristatymą žmonės žino, kad ši marksizmo tezė aktuali ir šiandien. Žino ne tik todėl kad jų dauguma liko ištikimi TSKP idealams, o dar ir todėl, kad tiesą apie tuos įvykius Lietuvoje visomis jėgomis stengiamasi nuslėpti. Ir ar tai ne įrodymas, kad liudininkų parodymai nėra išgalvoti?

Prieš metus, kai vykau pasikalbėti su vienu iš knygos veikėjų Juozu Kuoleliu (taip pat buvusiu politiniu kaliniu), mane sulaikė kaimo kelyje ir deportavo iš Lietuvos. Be to, Lietuva bandė uždrausti šios knygos pristatymą italų kalba Romos parlamente», – pristatymo metu papasakojo G.Sapožnikova.

Žmones, žinančius kas dedasi Pabaltijyje, ši naujiena vargu ar nustebino – šiuolaikinėje Lietuvoje (ir Latvijoje su Estija) tai norma. Pristatymo metu buvo prisiminti ir kiti 1991 metų sausio 13-osios įvykius bandę komentuoti žmonės. Pavyzdžiui, Algirdas Paleckis, kuriam skyrė baudą ir atėmė valstybinius apdovanojimus už tai, kad jis viešai suabejojo oficialia tų įvykių versija ir pareiškė, jog «savi šaudė į savus».

Yra Lietuvoje ir politinių kalinių. Iki šiol kalėjime laikomas atsargos pulkininkas Jurijus Melis, šios Pabaltijo valdžios sulaikytas 2014 m. kovą. Už dalyvavimą sausio 13-osios įvykiuose jis kaltinamas nusikaltimu prieš žmogiškumą, nors tai yra visiškas absurdas.

Ryškiausias faktas, rodantis, kad oficialiam Vilniui reikalinga tik «distiliuota tiesa», – 2013 metų draudimas transliuoti Pirmąjį televizijos kanalą, parodžiusį programą «Žmogus ir įstatymas», kurioje buvo paviešinti faktai, vėl gi prieštaraujantys oficialiems apie «šventąjį karą prieš kruviną centrą».

Ne atsitiktinai pristatymo dalyviai juokavo, jog beveik visi pasisakę – Lietuvos personos non grata. Kaip žinia, demokratija demokratams. G.Sapožnikovos knygos istorija tai dar kartą patvirtina. Tačiau Lietuvos politikai vis tiek nesugebės šiuolaikiškame pasaulyje užkirsti kelią informacijai, ir šalies gyventojai sužinos, kas ką išdavė, kaip buvo žudoma TSRS ir ko sulaukė žmonės, bandę ją gelbėti.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 12 — id: `scraped:rubaltic_lt:1ccafe89ab3fc23a`

**Title:** Emigracija – mirties nuosprendis Pabaltijui

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Pabaltijo šalys šiemet demonstruoja emigraciją liečiančius šokiruojančius skaičius. Gyventojų bėgimas iš Pabaltijo įgauna pagreitį, Lietuva ir Latvija tapo europietiškomis emigracijos ir išmirimo rekordininkėmis, du trečdaliai emigrantų pareiškia, jog niekada negrįš į tėvynę. Dėl emigracijos Pabaltijo šalyse vis labiau jaučiamas specialistų deficitas, tame tarpe ir gydytojų, o liekantiems tėvynėje vidutinio ir vyresnio amžiaus gyventojams po kelerių metų nebus iš ko mokėti pensijų. Emigracija, kurią Pabaltijo valdžios laikė išsigelbėjimu nuo visų socialinių ir ekonominių sunkumų, tapo mirties nuosprendžiu Lietuvai, Latvijai ir Estijai: jei tokie depopuliacijos tempai išliks, šios šalys ateityje nesugebės egzistuoti .

Pasak Eurostato duomenis, Lietuva, Latvija, Estija, o dar ir Slovakija — vienintelės Centrinės ir Rytų Europos šalys, kurių gyventojai nenustojo iš jų bėgę. Emigracijos iš Pabaltijo srautas didėja. Triskart, lyginant su 2014-aisiais, praeitais metais padidėjo emigracija iš Estijos. Iš Latvijos pernai išvyko 5,7 proc. daugiau gyventojų, nei užpernai. Ir absoliuti rekordininkė šiuo klausimu yra Lietuva, kurios gyventojų skaičius 2015 metais sumažėjo 1,5 proc.: pernai iš Lietuvos išvyko gyventojų 21,6 proc. daugiau, nei užpernai.

«Naujoji Europa» tradiciškai Europos Sąjungoje buvo laikoma pigaus nekvalifikuoto darbo rinka turtingoms «senosioms» šalims — ES narėms. Tačiau pastaruoju metu šis įprastas teiginys reikalauja taisymo. Pasak minėto Eurostato, 2015 metais emigracija iš Čekijos sumažėjo 33,5, iš Vengrijos — 22,2 proc. Mažėja svetur darbo ieškančių srautas iš Lenkijos ir net iš Bulgarijos su Rumunija. Ir tik iš Pabaltijo žmonės vis labiau skuodžia.

Šiais metais emigracija iš Pabaltijo, lyginant su praėjusiais, ženkliai padidėjo. Iš Lietuvos per šių metų pirmąjį pusmetį, lyginant su pirmuoju 2015 metų pusmečiu, išvyko 6,5 proc. daugiau gyventojų. Lietuva ryžtingai pirmauja ES pagal gyventojų skaičiaus mažėjimą: oficialiai šalyje dabar gyvena 2,863 mln. žmonių, o 2015-aisiais gyveno 2,918 mln. Latvijos gyventojų skaičius per metus sumažėjo 1 proc., pagal depopuliaciją šalis pastoviai užima antrą vietą ES po Lietuvos; Latvijoje dabar gyvena 1,952 mln. žmonių. Iš Estijos per pastaruosius metus išvyko 13 tūkstančių.

Pačių emigrantų apklausa rodo, kad dauguma jų ne išvyko laikinai uždarbiauti, o būtent emigravo, pasirinkdami sau naują tėvynę. Latvijos universiteto tyrimai rodo: 62,7 proc. išvykusių iš šios šalies pareiškė, jog nenori grįžti, nes nusivylė Latvija kaip valstybe. Iš tų, kurie nutarė sugrįžti į Latviją, 40 proc. persigalvojo ir vėl išvyko. Panašūs tyrimai buvo atlikti ir Lietuvoje. Pagal 2011 metų apklausą, 60 proc. Lietuvos emigrantų atsisakė sugrįžti.

Sausą statistiką geriausiai iliustruoja konkretūs faktai. Pavyzdžiui, Pabaltijo politikų vaikai dažnai gyvena svetur. Žurnalistinį tyrimą šia tema atliko Latvijos laikraštis «Diena». Taigi Latvijos premjero Mariaus Kučinskio sūnus dirba Vokietijoje, premjero bendrapartiečio, «Žaliųjų» ir valstiečių sąjungos frakcijos parlamente pirmininko Andriaus Priebalgso vaikai gyvena Didžiojoje Britanijoje ir Austrijoje. Aukštus postus užimantys tėvai neketina raginti savo vaikų grįžti namo: premjeras Maris Kučinskis net prisipažino, jog pritarė sūnaus sprendimui negrįžti į Latviją.

Kaip matome, daugelis Pabaltijo gyventojų atsisako savo šalių. Vadinti šį reiškinį «išvykimu uždarbiauti» — veidmainystės viršūnė. Tokia pat veidmainystė — tvirtinti, jog gyventojų migracija ES ribose nereikšminga Lietuvai, Latvijai ir Estijai ir visiškai neatsispindi šių šalių gyvenime. Nes tikrovėje emigracija Lietuvai, Latvijai ir Estijai daug ką reiškia: ji nustato pabaltijiečių visuomenių gyvenimo būdą šiandien ir atima iš šių šalių ateitį.

Visas pabaltijiečių gyvenimas vienaip ar kitaip sukasi aplink depopuliaciją, moksleiviai svarsto, kas kur išvažiuos sulaukęs pilnametystės, senukai svarsto, kuriose šalyse dirba vaikai, kiek ten, lyginant su Lietuva, uždirba ir ar atveš vasarai iš Europos anūkus. Didieji miestai — Kaunas arba Daugpilis — atrodo lyg pusiau išmirę, kai kuriuose mažuose miesteliuose per maža gyventojų, kad galėtų tebevadintis miestais, o kaimiškos vietovės tiesiog dingsta. Iš Pabaltijo žemėlapio kasmet išnyksta geografiniai objektai, tačiau tuštėjančių vienkiemių gyventojai dažnai persikelia ne į Rygą ir Vilnių, o į Londoną ir Dubliną. Pabaltijyje nėra «augimo taškų», kurie viliotų provincijos gyventojus: vidinė migracija neturi didelės reikšmės, o sostinės praranda gyventojus taip pat, kaip ir provincija.

Lietuvos statistikos departamento duomenimis, virš pusės emigrantų — 52 proc. išvykusių iš Lietuvos šių metų pirmame pusmetyje — 18–35 metų jaunimas. Iš Lietuvos ieškoti Europoje darbo pagal specialybę išvyksta ką tik aukštojo mokslo diplomus gavę jaunuoliai. Iš Lietuvos išvyksta jau ne tik bedarbiai, bet ir darbo rinkoje paklausą turintys specialistai. Didžiausia bėda — emigruoja gydytojai.

«Po bandymų paskaičiuoti, kas ir kiek uždirba, kiek dirba, daugelis gydytojų pasirenka darbą užsienyje. Todėl emigruojančių skaičius didelis, išmokti kalbą jaunuoliams nesudėtinga. Jau katastrofiškai trūksta gydytojų–specialistų (neurologų, okulistų, kardiologų, traumatologų), ypač rajonuose, Biržuose, Pasvalyje, Pakruojyje, Šilutėje, Šilalėje. Trūksta medicinos seserų — mes jas puikiai paruošiame, o jos išvyksta», — sako Seimo Sveikatos apsaugos komiteto pirmininko pavaduotojas Antanas Matulas.

Panašios problemos slegia ir kitas Pabaltijo šalis. Estijoje daug metų šaipomasi: respublikoje pastovus medicinos darbuotojų deficitas, nes dauguma gydytojų, esant galimybei, išvyksta dirbti į Suomiją, kur atlyginimai didesni 6 kartus. Latvijoje dėl gydytojų deficito pacientai po 2 mėnesius laukia priėmimo.

Panaši problema — augantis darbininkiškų profesijų specialistų deficitas. Iš Lietuvos, Latvijos ir Estijos emigruoja vandentiekininkai, elektrikai, suvirintojai — jų atlyginimai Europoje ypač ženkliai skiriasi nuo pabaltijietiškų. Jei ir ateityje išliks tokie tempai, Pabaltijyje po kelerių metų triūs vien tik European studies magistrai, mokantys skirstyti eurofondus, tačiau jiems niekas nesugebės sutaisyti trūkusio vamzdžio.

Pagal praeitų metų Eurostato prognozę, artimiausiais 40 metų Lietuvos gyventojų skaičius sumažės 38, Latvijos — 31 proc. Atsižvelgiant jau į išvykusią depopuliaciją (per pastaruosius 25 metus Lietuva ir Latvija prarado apie trečdalį savo gyventojų), iki XXI amžiaus vidurio Pabaltijo respublikos neteks dviejų trečdalių gyventojų. Beje, nuo 2020 iki 2030 metų į pensiją išeis skaitlingiausia Pabaltijo gyventojų karta, o darbo rinkoje ją pakeis žemiausio gimstamumo karta. Atsižvelgiant į tai, Lietuvos respublikos Socialinės apsaugos ir darbo ministerija prognozuoja, jog nuo 2020 metų pensijos sudarys ne daugiau 24 proc. vidutinio atlyginimo. Tačiau neabejotina, jog ateityje, augant demografinei katastrofai, pensijų dydis Pabaltijo šalyse vis labiau mažės — nes vis mažiau jose gyvens žmonių, iš kurių uždarbio tos pensijos formuojamos.

Taigi Pabaltijo demografinė katastrofa šioms šalims neša šiaip katastrofą.

Tokia situacija — dėsningas rezultatas «mažiau žmonių, daugiau deguonies» politikos, kuria ketvirtį amžiaus vadovaujasi Pabaltijo valdžios. Vietiniai valdantieji elitai laikė emigraciją išsigelbėjimu nuo bet kokių nelaimių: socialinių, politinių, ekonominių. Visą potarybinį laikotarpį jiems buvo svetima ir nesuvokiama «gyventojų tausojimo» idėja; priešingai, jie visada lengvai „nuleisdavo kraują“, vardan savo problemų sprendimo prarasdami dar šiek tiek gyventojų.

1990-aisiais Pabaltijo etnokratai siekė savo valdžios įtvirtinimo vydami «rusiškuosius okupantus»: formulė «Lagaminas, stotis, Rusija!» praktiškai tapo oficialia politika, visuomenėje sąmoningai buvo formuojama neapykantos rusakalbiams atmosfera, pirmieji Lietuvos, Latvijos ir Estijos asmenys nesivaržydami teigė, jog optimalus rusų gyventojų problemos sprendimas — priversti visus rusus išvykti į Rusiją.

Po Pabaltijo šalių įstojimo į Europos Sąjungą darbinė migracija išgelbėjo Pabaltijo elitą nuo būtinybės rimtai užsiimti ekonomika ir socialine sfera. Ar reikia išsaugoti pramonę? Ar reikia Briuselyje apginti Ignalinos AE? Ar būtina kautis dėl kiekvieno potencialaus investoriaus? Ar verta gelbėti nuo bankroto didžiausią Europoje Lietuvos žvejybos laivyną? Vardan ko padėti jaunoms šeimoms įsigyti būstą, remti jaunus specialistus, mokėti pašalpas šeimoms, sulaukusioms antro ir sekančio kūdikio?

Vietoj viso šio galima tarti: nepatinka — sienos atviros. Lagaminas, oro uostas, Londonas! Europoje atlyginimai 5 kartus didesni, o mums be jūsų mažiau galvos skaudės.

Ir štai jau sulaukta atpildo už tokią politiką savo gyventojų atžvilgiu, jos istoriškai neišvengiamo rezultato. Prieš akis — aklavietė, gyvatė įgėlė save ė uodegą, emigracija, kaip išsigelbėjimas nuo visų Pabaltijo problemų, tapo mirties nuosprendžiu Lietuvai, Latvijai ir Estijai.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 13 — id: `scraped:rubaltic_lt:2b4427e721a6bdda`

**Title:** Pabaltijis ir Ukraina kliedi spalvotomis haliucinacijomis

**Source:** rubaltic_lt (propaganda)

**Text:**

```
«Maskvos rankos» paieškos ir isteriją dėl «rusų grėsmės» kelianti baimė Ukrainoje ir Pabaltijo šalyse tapo nacionalinio sporto šaka. Ukrainiečiai ir pabaltijiečiai ruošia bendrus «hibridinės agresijos» stebėjimo projektus ir vieni kitus moko teisingai bijoti Rusijos ir pelningai parduoti tą baimę Vakarų sąjungininkams.

Lietuvos Jono Žemaičio karo akademija išleido buvusio savanorių bataliono «Aidar» būrio vado Jevgenijaus Dikio knygą «Hibridinis Rusijos karas: Ukrainos patirtis Baltijos šalims». Knygos įžangoje autorius teigia, kad šią «metodinę priemonę hibridinio karo tema» jis parašė paskatintas Lietuvos karo akademijos ir paremtas buvusio Lietuvos URM vadovo bei pasiuntinio Kijeve Petro Vaitekūno.

Įdomūs ryšiai susiklostė Lietuvos kariniame ir diplomatiniame elite: apie «Aidaro» kovotojų nusikaltimus prieš taikius Donbaso gyventojus pastarųjų dvejų metų laikotarpyje kalbėta ESBO, Amnesty International ir net pačios Ukrainos valdžios. Savanorių batalionas užsiiminėjo vagystėmis, kankinimais, žudynėmis, prievartavimais ir plėšikavimais. 2014 metų spalį Ukrainos teisėsauga iškėlė 32 baudžiamąsias bylas, dokumentaliai įrodančias «Aidaro» karių nusikaltimus. 2015 metų kovą tuometinis Lugansko srities gubernatorius Genadijus Moskalis oficialiai kreipėsi į gynybos ministrą, Generalinio štabo viršininką, VRM vadovą ir generalinį Ukrainos prokurorą, įvardindamas «aidarininkų» nusikaltimus.

O 2015 metų sausį «Aidaro» būrio vadas Jevgenijus Dikis Vilniuje skaitė paskaitą «hibridinio karo» tema. Po metų šią daktaro Dikio (biologijos mokslų kandidato, Kijevo-Mogiliano akademijos dėstytojo, 1990-aisiais kariavusio Čečėnijoje Ukrainos nacionalistų gretose kartu su velioniu Saško Bilu) paskaitą organizavusi Lietuvos karo akademija išleido «rusų agresijos» «eksperto» knygą. Kaip sakoma, pasakyk, kas tavo draugas, ir aš pasakysiu, kas tu.

Putino Rusija kliedi permanentinio plėtimosi logika, kurios strateginis tikslas — plėsti «rusų pasaulį» viso žemės rutulio mastu. Šiuo metu Kremlius užsiėmęs dar tik buvusių tarybinių respublikų prarijimu — kuria jose marionetinius režimus, kurie vykdo Maskvos įsakymus. Bet tuo nesibaigia rusų imperialistų–šovinistų planai. Pasiglemžęs savo kontrolei buvusias tarybines respublikas, Kremlius neš «rusų pasaulį» į Centrinės ir Rytų Europos šalis, neš per visus Balkanus iki Graikijos, įtvirtins prorusiškus režimus arabų šalyse, o taip pat Turkijoje, Irane, Indijoje, Brazilijoje, Izraelyje. Po to Putinas spręs klausimą, kaip paglemžti Vakarų Europą, paversdamas Vokietiją, Austriją, Ispaniją, Portugaliją ir Skandinaviją «naudingais idiotais», kurie atliktų prorusiško tarptautinio padėjėjo vaidmenį Rusijos kovoje prieš JAV.

Tokie Lietuvos karo akademijos išleisti kūriniai turi glostyti rusų imperialistų–šovinistų savimeilę. Jie primena seną žydų anekdotą: «Izia, ar tiesa, kad jūs skaitote antisemitinius laikraščius? — Žinoma. Todėl kad žydų laikraščiuose — oi-vei, žydai tokie nelaimingi, žydus visi skriaudžia, nekenčia, engia. Užtat antisemitiniuose laikraščiuose viskas šaunu: žydai galingi, žydai visur, žydai valdo pasaulį».

Taip ir čia.

Tiesa, ukrainietiškas «hibridinio karo» «ekspertas», kalbėdamas apie rusų planus užvaldyti pasaulį, tuoj pat prognozuoja, jog elgetaujanti, degraduojanti ir mirštanti Rusija ryt-poryt subyrės, ir tuo įvelia savo kūrinyje prasmės klaidą. Visus pinigus Kremlius išeikvojo, rusų ekonomiką sugniuždė sankcijos. Ir kaip tada Kremlius pajėgs paversti visą žmoniją «rusų pasauliu», papirkdamas elitus nuo Lenkijos iki Portugalijos, nuo Švedijos iki Brazilijos ir įtraukdamas visas šalis į savo korupcijos schemas? Bet logika šiuo atveju — per griežtas reikalavimas liguisto žmogaus atžvilgiu.

Rusijos agresija savo kaimynų atžvilgiu neišvengiama visu pasienio perimetru, nes «Maskvos ranka» nuo pat 1990 metų pradžios reiškėsi visuose potarybinėje erdvėje vykusiuose kariniuose konfliktuose.

Putino «hibridinės agresijos» instrumentai buvo tobulinami Tadžikijoje, Karabache, Padniestrėje ir, žinoma, Čečėnijoje, kurioje, «siekiant įteisinti neteisėtus veiksmus» prieš «tarptautinės bendrijos nepripažintą, tačiau de-fakto nuo 1992 metų nepriklausomą Ičkerijos respubliką», Kremlius įžvelgė neteisėtų karinių formuočių savo šalyje veiksmus. O jokių neteisėtų karinių formuočių Rusijoje, kaip žinia, neegzistavo: vaidindami vachabitus 1999 metais į Dagestaną įsiveržė «žalieji žmogeliukai», o namus Maskvoje sprogdino Federalinė saugumo tarnyba.

O galutinai «hibridinio karo» technologija buvo paruošta ir pirmą kartą sistemingai praktiškai panaudota «Rusijos kare prieš Ukrainos liaudį».

O tai įrodyti nelengva: nuo 1990-ųjų metų pradžios dauguma Krymo gyventojų nenorėjo būti Ukrainos sudėtyje, beveik visi Donbaso gyventojai reikalavo įteisinti rusų kalbą kaip valstybinę, federalizuoti Ukrainą, ekonomiškai integruojant su Rusija ir kitomis NVS šalimis. Visa tai įrodo daugybė sociologinių apklausų ir ne kartą Kryme bei Donbase organizuoti referendumai. Iš Donecko srities buvo kilęs nuverstas Ukrainos prezidentas Viktoras Janukovičius, Donbasas davė Janukovičiui ištikimą elektoratą ir Regionų partiją ir per tris Maidano mėnesius Donbase (ir visoje Rytų ir Pietų Ukrainoje) niekas nebandė užgrobti srities administraciją ir neorganizavo «europietiško pasirinkimo» mitingų.

Ir kaip, žinant šiuos faktus, pavadinti Pietų ir Rytų Ukrainos įvykius užmaskuota rusų agresija, o ne pilietiniu karu? Ogi paprastai. Donbaso gyventojai — darbo jaučiai, kurie tupėjo namuose tuo metu, kai laisvės trokštanti ukrainiečių tauta grobė valstybinius pastatus Lvove ir Ivanovo-Frankovske. Vėliau tie FST ir Putino agentų bei provokatorių vadovaujami jaučiai Donecko ir Lugansko aikštėse ėmė organizuoti mitingus, reikalaudami federalizavimo, sąjungos su Rusija ir rusų kalbos, nes jie buvo apakinti «rusų propagandos».

Todėl išvada:

Ir jei «nelojalūs gyventojai» protestuoja prieš rusiškų mokyklų uždarymą, kalbą liečiančiuose įstatymuose įžvelgia diskriminaciją arba piktinasi kvailomis Pabaltijo nacionalistų iniciatyvomis (pvz., uždrausti suteikti naujagimiams rusiškus vardus), tai visiškai nėra protestas. Tai vandenį drumsčia «Maskvos ranka», tai jos agentai-provokatoriai ragina nepažeisti žmogaus teisių, tuo ruošdami dirvą kariniam įsiveržimui į Pabaltijį.

Tokiu būdu «hibridinę agresiją» Pabaltijo šalys privalo stabdyti pačioje jos pradžioje. Su «rusų propaganda» būtina kovoti spjaunant į kažkokią ten žodžio laisvę, atjungiant rusiškus televizijos kanalus (pasikartosime: Jevgenijaus Dikio «metodinė priemonė» buvo išleista Lietuvos valstybės biudžeto lėšomis). Bet kokius raginimus ieškoti konstruktyvaus dialogo su Maskva ignoruoti, o tokius raginimus pareiškiančius politikus be jokių kalbų ir įrodymų įtraukti į «Kremliaus agentų» sąrašus ir persekioti. Ir, žinoma, už bet kokias kalbas apie teisinę tautinių mažumų padėtį ir etninį nacionalizmą Lietuvoje, Latvijoje ir Estijoje — iškart vadinti «penktąja Putino kolona».

O jei «hibridinis karas» virs karine priešprieša, pagrindinė nacionalinės vyriausybės klaida — nepanaudoti jėgos prieš savus taikius gyventojus. «Separus» būtina naikinti iškart, nevedant su jais jokių derybų ir šalin vejant mintis apie pilietinį dialogą ir demokratiją.

Užbaigia savo paistalus apie «hibridinį karą» «ekspertas» kategorišku tvirtinimu, kad Kremlius Baltijos šalims jau ruošia ukrainietišką scenarijų. Autorius net tvirtina, kad rusų imperialistai-šovinistai jau paruošė projektą «Rusiškas pavasaris Baltijoje». Galima, žinoma, paprieštarauti, kad projekto tokiu pavadinimu negali būti net todėl, kad «rusiškieji imperialistai-šovinistai» nevartoja rusų kalboje nesančio žodžio «Baltija». Bet vėl gi, ar verta ginčytis su akivaizdžiai proto negale sergančiu žmogumi?

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 14 — id: `scraped:rubaltic_lt:810802bf7dbb47fe`

**Title:** «Lietuvos ateitis – nykstanti visuomenė»

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Rinkimų į Seimą išvakarėse Lietuvos valdžiai parūpo pastovios gyventojų emigracijos problema, ir ji pabandė eilinį kartą pademonstruoti šiame klausime savo kompetenciją. Reaguodama į eilinę nerimą keliančią Eurostato statistiką, vyriausybė skubos tvarka priėmė «Emigracijos mažinimo ir grįžtančių emigrantų skaičiaus didinimo planą».

Eurostato duomenimis, Lietuva pirmauja tarp ES šalių pagal gyventojų skaičiaus mažėjimą 1000-iui gyventojų (1,13%). Tas skaičius per metus (nuo 2015 m. sausio iki 2016 m. sausio) sumažėjo 32700 žmonėmis ir dabar sudaro 2,886 mln. (2015 m. — 2,918 mln.). Išvykusių per pastaruosius metus gyventojų skaičius stabiliai didelis (2014 m. — 36,6 tūkst. žmonių, 2013 m. — 38,8 tūkst., 2012 m. — 41,1 tūkst.). 2012–201 m. vidutiniškai per metus emigravo po 37 tūkst. gyventojų, o sugrįžo apie 8 tūkst. Per pastaruosius 14 metų šalies gyventojų skaičius sumažėjo 16% (Statistikos departamento duomenimis, 2001 m. šalyje gyveno 3,484 mln. žmonių).

Eurostatas prognozuoja, kad 2040 m. Lietuvoje gyvens mažiau nei 2 mln. žmonių (lyginant su 2011 m., skaičius sumažės daugiau nei 40%). Europietiška statistika fiksuoja pastovią Lietuvos visuomenės problemą, kurią valstybės mastu būtina spręsti kompleksiškai. Tęsiantis negatyviai dinamikai, iškils grėsmė ekonominiam saugumui ir kris socialinis–ekonominis žmonių gyvenimo lygis.

Tačiau vyriausybės iniciatyvą tuoj pat sukritikavo vietiniai ekonomistai, neįžvelgę joje nieko naujo, tačiau pastebėję buvusių planų teiginių pakartojimus. Taigi vyriausybė, daug nesivargindama, tiesiog perrašė didesnę senų planų dalį, tai pateikdama kaip naujai sukurtą planą. Pasak Nordea banko ekonomisto Ž.Maurico, planas nesiskiria nuo praeities versijų ir, būdamas «nepakankamas», siunčia prieštaringus signalus, kurie «dar labiau atstums emigrantus». Bankininkystės atstovas tarp pagrindinių imigraciją neskatinančių priežasčių įžvelgė žemą piliečių oficialių pajamų lygį, per didelį valstybės tarnautojų vidutinio atlyginimo «į rankas» lygį, korupciją, o taip pat valstybės ignoravimą tų veiklos sferų, kurioms reikalingi kvalifikuoti kadrai. Ekonomisto nuomone, norint taisyti situaciją, valstybė turėtų mažinti mokesčius (tai padėtų sumažinti pilkojo ekonomikos sektoriaus dalį), reformuoti socialinės apsaugos sistemą (jos išmokos turi atspindėti sumokėtus mokesčius), kovoti su korupcija, o taip pat investuoti į prioritetines ekonominės veiklos sferas.

Savo ruožtu DNB banko ekonomistė J.Rojaka planą vertina kaip neefektyvų, nes jis numato «trumpalaikius skylių lopymo sprendimus, bet ne struktūrinius pertvarkymus, kurie paskatintų žmones sugrįžti į šalį, — švietimo reformas ir valstybės finansavimo modelio pokyčius». Ekonomistė daro išvadą, jog vyriausybė nepajėgi išspręsti emigracijos problemos, ir rekomenduoja užsiimti investicijų į šalį atėjimo sąlygų sudarymu.

Tėvynainių sugrįžimo į tėviškę problema užsiiminėja nemažai valdžios institutų: Tautinių mažumų ir išeivių iš Lietuvos departamentas, Lietuvių į tėvynę sugrįžimo informacijos centras ir t.t. Tačiau, sprendžiant pagal oficialius duomenis, valstybės politika neefektyvi: šalies vadovybė apsiriboja vienkartiniais dalyvavimais formato «Atgal į Lietuvą!» užsienio konferencijose, kuriose dirbančius ir besimokančius lietuvius ragina grįžti į tėvynę. Po to, kai 2011 m. Lietuvos vyriausybė patvirtino programą «Globali Lietuva» (2011–2019 m.), įvyko keturi tokie renginiai. Paskutinis — 2014 m. gegužę Londone (Anglijoje gyvena virš 200 tūkst. lietuvių – RuBaltic.Ru pastaba) praėjo be anonsuoto valstybės vadovės D.Grybauskaitės dalyvavimo. Šiuo metu ji aktyviai reiškia susirūpinimą dėl padidėjusio po referendumo dėl Didžiosios Britanijos išstojimo iš ES agresyvumo emigrantų iš Lietuvos atžvilgiu, ragindama tautiečius grįžti į tėvynę.

Vargu ar ką nors suvilios tokie raginimai. Net po to, kai Brexit rezultatai 30% euro atžvilgiu sumažino svaro kursą, vidutinio užmokesčio Didžiojoje Britanijoje lygis (1180 eurų) dukart didesnis nei Lietuvoje (550 eurų). Visos vietinės valdžios kalbos, kad Didžiosios Britanijos išstojimas iš ES išprovokuos imigraciją į Lietuvą, neturi rimto pagrindo. Pirma, visais pastaraisiais metais valstybė neskyrė užsienyje gyvenantiems tautiečiams reikiamo dėmesio. Antra, ji nesugebės jų įdarbinti, nes, emigruodami, žmonės su laiku praranda reikalingą kvalifikaciją. Ir peršasi išvada, kad Lietuvos valdžiai emigrantai nereikalingi, ką patvirtina be saiko gimdomi ir vienas kitą kartojantys planai.

Antroji pagal svarbą ir pasekmes šalies ekonomikai tema — demografinė.

Tokias išvadas padarė Vytauto Didžiojo universiteto Demografinių tyrimų centro profesorė V.Stankūnienė. Pagal jos prognozes, Lietuvoje augs pagyvenusių žmonių su chroniniais susirgimais ir pastoviais sveikatos apsaugos paslaugų poreikiais skaičius, o kartu ir darbingų gyventojų krūvis. Ir todėl ji ragina Lietuvos valdžią suvokti, jog problema yra labai rimta, ir nustoti save raminus, kad «emigrantai sugrįš ir teigiama linkme pakeis situaciją». Demografė teigia, jog situacija krypsta link katastrofos: «Gimstamumas jau ketvirtį amžiaus neužtikrina kartų kaitos, o didelis emigruojančio jaunimo, kuris turi ilgai dirbti ir kurti gerovę, skaičius veda prie aštraus darbingo disbalanso». Demografinių tyrimų centro duomenimis, 45-54 metų amžiaus žmonių Lietuvoje šiandien dukart daugiau, nei 10-19 metų, o tai reiškia, jog egzistuoja rimta vienos kartos kita kartos disproporcija.

Analitikos centras daro liūdnas išvadas, kad artimiausią dešimtmetį nepasikeitus negatyviai tendencijai darbinga visuomenės dalis iki 2050 metų sumažės beveik dukart. JTO prognozė labiau optimistiška: 1,5 mln. 15-64 metų amžiaus žmonių skaičius iki amžiaus vidurio (šiuo metu darbingų žmonių yra apie 2 mln.), o pagal Eurostatą — iki amžiaus vidurio kas dešimtas šalies gyventojas bus 80-ties ir daugiau metų.

Ir į tai atsižvelgiant, Lietuvos valdžios deklaruojamus pareiškimus, jog iki 2020 m. gyventojų skaičius pasieks 3,5 mln., galima vertinti ne šiaip kaip populistinius, o kaip visiškai nekompetentingus. Kiek dar šimtų tūkstančių mūsų šalies gyventojų turi emigruoti ieškodami geresnio gyvenimo, kad valdžia pagaliau suvoktų situacijos grėsmingumą ir pabandytų realiai pagerinti šalies socialinę–ekonominę padėtį? Belieka tikėtis, kad šią nepatogia tema po spaly įvyksiančių Seimo rinkimų užsiims jau kita vyriausybė.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 15 — id: `scraped:rubaltic_lt:3166ab4c8fd86dd4`

**Title:** Europos komisija pripažino Lietuvą labiausiai nukentėjusia nuo sankcijų ES šalimi

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Eurokomisijos pirmininkas Žan-Klod Junkeris pripažino, kad nuo karo sankcijų su Rusija iš visų ES šalių labiausiai nukentėjo Lietuva. Apie tai pareiškė Lietuvos premjeras Algirdas Butkevičius, pranešęs, jog Briuselis skirs Lietuvos pienininkystei papildomą kompensaciją. Deja, šios kompensacijos nepakaks norint padengti tą nuostolį, kurį nuo sankcijų patyrė Lietuvos ekonomika.

Pasak Lietuvos premjero, Žan-Klod Junkeris pripažįsta, jog Lietuva, kurios politinė vadovybė aktyviausiai ES ragino taikyti Rusijai sankcijas, labiausiai kenčia nuo atsakomojo Rusijos embargo maisto produktų iš ES šalių įvežimui.

Birželį vyriausybės vadovas pabuvojo Briuselyje ir prašė ES vykdomosios valdžios išimties tvarka suteikti papildomą skubią pagalbą Lietuvos pieno gamintojams. Po dar vieno susitikimo su Eurokomisijos vadovu — Europos ir Azijos šalių Mongolijoje samite praeitą savaitę — Butkevičius pareiškė, jog Briuselis numato skirti Lietuvos pieno sektoriui papildomai 13,3 milijono eurų kompensacijos. «Šiandien mes kalbėjomės su EK pirmininku ir sutarėme, kad Lietuvos pieno sektoriui dabar reikalinga ypatinga parama. Aš dėkingas už konstruktyvų bendradarbiavimą tikslu padėti Lietuvos pieno gamintojams šiuo sudėtingu laikotarpiu», — pranešė spaudai Butkevičius.

Šią savaitę sužinojome, kad Vilniaus nevilties maldavimus Briuselis išgirdo: žemės ūkio ministrė Virginija Baltraitienė pareiškė, kad gautas Eurokomisijos patvirtinimas apie išskyrimą Lietuvai papildomų 13,3 milijono eurų finansinės paramos. Tiek pat pieno sektoriui iš Lietuvos valstybės biudžeto skirs vyriausybė. Tokiu būdu, Lietuvos pieno gamintojai rugpjūtį-rugsėjį gaus sankcijų nuostoliams padengti papildomai 26 milijonus eurų.

Kiekviena šios istorijos smulkmena paneigia oficialią Vilniaus poziciją sankcijų atžvilgiu.

Atitinkamai, ar gaus Lietuvos biudžetas Briuselio pinigų, priklauso nuo to, ar pripažins Eurokomisijos vadovybė ypatingus Lietuvos praradimus sankcijos kovos prieš Rusiją epopėjoje. Pripažino. Ir naujas kompensacijas skyrė — didesnes, nei priklauso Lietuvai proporcingai jos daliai Europos pieno rinkoje. Apie tai Lietuvos vyriausybės valdininkai dabar kalba kaip apie savo pasiekimą, vos nereklamuodami prieš rinkimus savo gabumų «išmušti» Briuselyje papildomą finansavimą. Tik va kaip po viso to jie vėl įtikinės gyventojus, kad Lietuvos vadovybė elgėsi teisingai, garsiausiai ES reikalaudama sankcijų prieš Rusiją, ir kad sankcijos ir kontrsankcijos niekaip neįtakoja Lietuvos ekonomikos? Juk tai, kad Lietuva iš ES šalių labiausiai nukentėjo nuo sankcijų, pripažino Eurokomisijos pirmininkas ir pripažino ne prisiklausęs «Kremliaus propagandos» Peterburgo ekonominiame forume, o spaudžiant Lietuvos vadovybei, kuri, liedama ašaras, maldavo skirti papildomų kompensacijų.

Kitas klausimas: kaip dabar Lietuvos diplomatai argumentuos savo reikalavimą tęsti ir plėsti sankcijas prieš Rusiją, kuo, kaip ir anksčiau, užsiiminėja ir ketina užsiiminėti prezidentė Dalia Grybauskaitė ir užsienio reikalų ministras Linas Linkevičius? Juk, pasak Butkevičiaus, EK vadovas Žan-Klod Junkeris tiesiai pareiškė jam, kad labiausiai ES nuo sankcijų nukentėjo garsiausiai jų reikalavusi Lietuva.

Ką gi, dabar taip ir bus atgaminamas absurdo ciklas:

Ir kaip Lietuvos ekonominės politikos rezultatas — nesugebėjimas kompensacijomis padengti tą nuostolį, kurį Lietuva patyrė dėl sankcijų. Lietuvos pieno pramonės nuostoliai nuo Rusijos maisto produktų embargo sudarė 76 milijonus eurų. Eurokomisija sutiko skirti Lietuvai 13 milijonų eurų, tiek pat pieno sektoriui iš valstybės biudžeto skirs šalies vyriausybė. Viso — 26 milijonai. Tai yra kompensacijos padengia tik trečdalį pieno gamintojų nuostolio. Be to, kompensacijos — taip pat nuostoliai. Tai ne investicijos į Lietuvos pieno pramonę, o pieno gamintojams metamas gelbėjimosi ratas, kad bent kurį laiką jie nenuskęstų. Tai tiesioginės Lietuvos ir ES biudžetų išlaidos, kurios niekada nebegrįš.

Pagrindinė problema — Rusijos maisto produktų embargas, kurį išprovokavo sankcijų prieš šią šalį taikymas. Ši problema neišspręsta ir nesprendžiama — priešingai, būtent Lietuvos vadovybė siekia, kad sankcijų karas niekada nesibaigtų. Tačiau saviems mokesčių mokėtojams — pieno ir pieno produktų eksportuotojams ta vadovybė taip ir nesurado alternatyvos Rusijai. Kur tos nuostabios naujos rinkos, apie kurių atsiradimą pastaruosius dvejus metus kalbėjo Lietuvos politikai? Jeigu jie surado tas naujas rinkas, tai kodėl Lietuvos pienininkams skiriamos kompensacijos iš valstybės biudžeto ir kaulinamos vis naujos kompensacijos iš ES biudžeto?

Ankstesnės ES kompensacijos neišėjo (ir negalėjo išeiti) Lietuvos pramonei į naudą. Po to, kai Rusija įvedė embargą, Lietuva paprašė Briuselio 46 milijonų eurų — tokia suma Lietuvos vyriausybė įvertino maisto pramonės sektoriaus nuostolius, patirtus per pirmuosius 3-4 rusų embargo mėnesius. Tada Vilnius sulaukė pirmojo nemalonaus siurprizo: Briuselis nutarė skirti žemės ūkio produktų gamintojų nuostoliams kompensuoti 25 milijonus eurų... visoms 28 ES šalims. Tai yra proporcingai savo daliai ES žemės ūkio rinkoje Lietuva vietoj 46 milijonų eurų sulaukė kapeikų.

Vėliau nemalonūs siurprizai lydėjo kiekvieną finansinės pagalbos atvejį. Praėjus metams po embargo įvedimo Lietuvos žemės ūkio ministrė pareiškė, kad prašys Briuselio Lietuvos pramonės paramai 32 milijonų eurų. Tokių pinigų Vilniui Eurokomisija neskyrė. Dabar Lietuvos valdininkai džiaugiasi sulaukę 13 milijonų eurų ES finansinės paramos. Tačiau Lietuvos pieno pramonė prarado 76 milijonus...

Ir jokios išeities iš šios aklavietės nenusimato. Apie tai, jog nuo sankcijų iš visų ES šalių labiausiai nukentėjo Lietuva, kalba premjeras Butkevičius ir Eurokomisijos pirmininkas Žan-Klod Junkeris. Žadėtų naujų rinkų nesimato ir už horizonto. Sena patikima Rusijos rinka lieka uždaryta, o svarbiausia — Lietuvos valdžia savo politika daro viską, kad ji šalies pieno gamintojams ir ateityje būtų uždaryta.

Vadinasi, Lietuvos pienininkystė sugebės išsilaikyti tol, kol eurobiurokratai turės kantrybės klausytis Lietuvos politikų kalbų — į vieną ausį, kad būtina tęsti ir plėsti sankcijas prieš Rusiją, į kitą — kad Lietuvai žūtbūt reikia papildomų kompensacijų, nes ji labiausiai iš ES šalių nukentėjo nuo sankcijų.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 16 — id: `scraped:rubaltic_lt:5dcd31cd1edab782`

**Title:** Lietuvos energetiniai projektai nedavė šaliai pigios elektros

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos energetinė politika ne vakar pakvipo propaganda. Energetinių tiltų su ES sukūrimas, santykiai su „Gazpromu“, SGD terminalas Klaipėdoje, Baltarusijos AE problemos — veikla šiomis kryptimis seniai įgavo aršios politinės propagandos tvaiką. Nenuostabu, kad oficialaus Vilniaus energetikos pseudo strategai nesugeba pademonstruoti nors šiek tiek efektyvių rezultatų. Nepaisant politikų saldžių pažadų, Lietuvos vartotojai taip ir nesulaukė juntamo kainų sumažinimo.

Lietuvos konservatoriai surinko parašus prieš Baltarusijos AE. Šios partijos funkcionieriai teigia, kad iniciatyvai boikotuoti Ostroveco atominę elektrinę dviejų mėnesių eigoje savo parašais pritarė beveik 65 tūkst. piliečių. Tikslas pasiektas: siekiant pateikti Seimui įstatymo projektą reikia surinkti 50 tūkst. parašų.

Energetinės nepriklausomybės idėja Lietuvos politikams ir „tautiškai mąstančiam“ rinkėjui turi ypač svarbią reikšmę. Būtent tokie rinkėjai ir sudaro konservatorių elektoratą. Mažų depresinių miestelių ir kaimo vietovių gyventojai lengvai tiki konservatorių kuriamais gąsdinančiais mitais ir atiduoda balsus „landsbergininkams“. Ir nenuostabu, kad kryžiaus karas prieš Baltarusijos AE tapo jų rinkiminės kampanijos pagrindu. Karas su baltarusių elektros energija sprendžia du klausimus. Pirma, sukuriamas eilinis mitas apie rusų grėsmę: „Mes puikiai žinom, kad, norėdamas pavergti Lietuvą, stotį stato Putinas“. Antra, formuojamas oponentų-socdemų atakos pretekstas. Konservatoriai jau suspėjo sukurpti pareiškimą , kuriame kaltina vyriausybę ir asmeniškai premjerą Butkevičių atiduodant Lietuvą „branduoliniam monstrui“ ir parduodant nacionalinius interesus „diktatoriui Lukašenkai“.

Eilinė energetiką liečianti konservatorių bakchanalija siekia tik politinių tikslų. Nepaisant Lietuvos ekspertų raminančių pasisakymų ir išvadų MAGATE, pavadinusių Baltarusijos AE vienu iš „ labiausiai sėkmingų branduolinės energetikos srityje projektų “, „landsbergininkai“ girdi tik tai, ką patys sako: statyba turi būti sustabdyta.

Oficialaus Vilniaus energetinė politika seniai lenkia proto ribas ir tapo aršia propaganda. Propaganda buvo Visagino AE statybos idėja. Nepaisant ekspertų pareiškimų, kad dabartinėmis sąlygomis projektas nerealizuotinas, politikai tebekartoja: „Pastatysim, pastatysim“. Nepastatė.

Propaganda tapo ir šių dienų energetinių tiltų su Varšuva ir Stokholmu kūrimas. Demonstruodamas eilinį rusų energetinių tiekimų atsisakymą, Vilnius trenkia durimis. Ateityje tautiškai mąstantys energetikos strategai prognozuoja visišką atsijungimą nuo BRELL energetikos sistemos, kuri dar tarybiniais laikais elektros tinklų linijomis jungė Lietuvą, Latviją ir Estiją su Baltarusija ir dalimi Rusijos.

Eidami šiuo keliu, 2015 metų gruodžio mėnesį Lietuvos funkcionieriai triukšmingai simboliškai prisijungia prie lenkų ir švedų elektros tinklų — LitPol Link ir NordBalt. Nuo šių metų sausio elektros tiekimo linijos ir jūros dugnu pakloti kabeliai turėjo pradėti tiekti Lietuvai pigią ir „demokratišką“ elektros energiją. „Jei mus dar kartą pavadins sala, teks pridurti, jog į salą galima patekti daugeliu tiltų“, — gyrėsi energetikos ministras Rokas Masiulis. Tačiau tie tiltai taip ir liko fantastikos srityje.

Du trečdalius laiko nebuvo galimybių tiekti Lietuvai elektros energijos, pranešė Energetikos ministerija. Sugalvojusi, jog „sistema rizikuoja patikimumu“, Varšuva paprasčiausiai riboja tinklo pajėgumo galimybes. Kai elektros energijos rinkos kaina tampa didesnė, nei Lenkijoje, Vilnius dažniausiai negali pasinaudoti sandūra, o tada prarandama visos sistemos egzistavimo prasmė.

Geriau šia prasme klostosi situacija su švedų-lietuvių energetikos tiltu. NordBalt pralaidumas naudojamas daugiau nei 90 proc. Problema slypi kitur: nuo pat sandūros įvedimo rikiuotėn ją lydi techniniai nesklandumai. Kiekvienas energetikos tilto gedimas reikalauja iš lietuvių praktiškai dvigubo tarifo. Bet ir tai ne svarbiausia. Vis dar be atsako lieka klausimas: ar energetinių tiltų statyba suteiks galimybę mažinti kainas ir atsisakyti „nedemokratinės“ elektros energijos? Pati energetinių tiltų statyba ir integravimas į Šiaurės Europos elektros biržą Nord Pool Spot neįtakoja vertės. Nord Pool Spot — save reguliuojanti ekonominė sistema, kur kaina priklauso nuo pasiūlos ir poreikio. Nė vienas jos dalyvis neapsaugotas nuo esminio vertės svyravimo. Lietuvos energetikos strategai įsitikino tuo savo patirtimi: pirmojo lenkų-lietuvių ir švedų-lietuvių sandūrų darbo mėnesio metu oficialus Vilnius netikėtai sulaukė rekordinio kainų pakilimo .

„Energetinė nepriklausomybė“, artėjanti žemų elektros kainų era, „branduolinis Baltarusijos AE monstras“ ir kitais pelėsiais apaugusiais štampais bus aktyviai maitinamas elektoratas. Lietuviškų svajonių trumpalaikiškumą liudija vienas paprastas faktas: elektros energijos vertė Lenkijoje ir Švedijoje, neįskaitant trumpo pavasario potvynio laikotarpio, lieka ženkliai didesnė, nei Rusijoje. Ir jau tuo labiau pas europietiškus partnerius ji bus daug didesnė nei pas tiesiog greta tos Lietuvos, kuri esą ieško pigios energijos, statančius atominę elektrinę baltarusius.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 17 — id: `scraped:rubaltic_lt:4a83c538d02001f4`

**Title:** Grybauskaitė pademonstravo politinį bejėgiškumą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos prezidentė Dalia Grybauskaitė atsisakė kalbėtis su rusų žurnalistais, viešai juos ignoruodama ir paprasčiausiai pabėgdama nuo televizijos kanalo „Rossija“ filmavimo grupės. Daugiau niekas iš Varšuvos NATO samito dalyvių, tame tarpe aršiausių antirusiškų politikų, neišsigando bendravimo su rusais. Jau ne pirmuoju savo atsisakymu nuo nesuderinto ir nesurepetuoto bendravimo su žiniasklaida Grybauskaitė eilinį kartą patvirtino, kad ji bejėgė kaip politikė ir nepajėgi dalyvauti sąžiningame, „gyvame“ ir atvirame pokalbyje.

Prieš metus Dalia Grybauskaitė jau sukėlė skandalą pabijojusi kalbėti su žurnalistais „be popierėlio“, kai atsisakė atsakinėti į nesuderintus Latvijos televizijos klausimus. Anas skandalas neturėjo nieko bendro su Putinu, „Rusijos sulaikymu“ ir „rusų propaganda“. Svarbiausio valstybinio Latvijos LTV1 televizijos kanalo vedantysis Gundars Reders paklausė Lietuvos prezidentės, kaip ji žiūri į vienalyčių santuokų savo šalyje legalizavimą. Grybauskaitė tada pareiškė neatsakinėsianti į iš anksto jai nepateiktus klausimus.

Gundars Reders bandė reikalauti atsakymo, tačiau Jos Didenybė, nervingai dairydamasi, paskubom pareiškė, kad šio klausimo jie nesuderino, ji atsakinės tik į tuos klausimus, kurie su Latvijos televizija buvo suderinti iš anksto, ir bendrai pokalbis baigtas.

LTV1 žurnalistas dar bandė gelbėti padėtį, paklausdamas apie Maximos Rygoje supermarketo stogo griūtį, tačiau, deja, ir šis klausimas nebuvo suderintas — susijaudinusi ponia prezidentė pareiškė, kad nesiruošė į jį atsakyti ir pareikalavo pašalinti iš interviu nesuderintą pokalbio dalį. Neviltin puolęs televizijos vedantysis paskutinį kartą pabandė gelbėti situaciją, paprašydamas Grybauskaitės išvardinti penkias pajėgiausias Lietuvos krepšinio komandas. Dievulėliau mano! Ir šis klausimas nebuvo suderintas: „Aš negaliu užbaigti interviu tokiais klausimais, mes užbaigėme“, — pareiškė Lietuvos Respublikos vadovė, pakilo ir išėjo.

„Nesuderinto“ pokalbio skandalas sukėlė žurnalistų pasipiktinimą. Ypač papiktino kaimyninės europietiškos ir demokratinės šalies prezidentės reikalavimas pašalinti jai nepatogią pokalbio dalį. „Jeigu mes pradėsime šalinti tai, kas prašoma, bus ne žurnalistika, o piaras“, — pareiškė LTV1 atstovė. „Vargšė Grybauskaitė, ji sugeba atsakinėti tik į iš anksto suderintus klausimus“, — Lietuvos prezidentės pagailėjo nacionalistinio Latvijos leidinio Ir darbuotoja, o Latvijos Eurokomisijos atstovybės spaudos tarnybos eksvadovė kategoriškai pareiškė, kad „žurnalistams nebūtina derinti klausimus, net tikslinti temas — tai geros valios gestas“.

Pabrėšime, kad anas skandalas buvo visiškai vidaus, net, galima sakyti, „šeimyninio“ pobūdžio — vystėsi tarp dviejų „Pabaltijo seserų“. Putinas, „hibridinė agresija“ ir „rusų propaganda“ čia nebuvo kuo dėti, o valstybinio Latvijos televizijos kanalo žurnalistas iki pabaigos stengėsi nesukelti skandalo.

Ir todėl juokingai atrodo Lietuvos oficialiosios propagandos bandymai paskutinį skandalą Varšuvos NATO samite, kilusį dėl Grybauskaitės atsisakymo bendrauti su televizijos kanalo „Rossija“ filmavimo grupe, aiškinti kažkokiu politiniu demonstravimu.

Tik viena Dalia Grybauskaitė, iš visų NATO samito dalyvių, atsisakė bendrauti su Rusijos žurnalistais. Daugiau niekas neatsisakė, net tokie pat, kaip Lietuvos prezidentė, profesionalūs rusofobai. Į tos pačios „Rossija“ televizijos kanalo filmavimo grupės, nuo kurios skuodė Grybauskaitė, klausimus atsakė du odioziškiausi savo antirusiška retorika Lenkijos valdančiojo elito atstovai: URM vadovas Vitoldas Vaščikovskis ir gynybos ministras Antonijus Macerevičius. Rusijos žurnalistai be jokių problemų galėjo užduoti klausimą Lenkijos prezidento Andžėjaus Dudos spaudos konferencijos metu. Su Rusijos žurnalistais laisvai bendravo NATO generalinis sekretorius Jens Stoltenbergas ir daugelio šio aljanso šalių vadovai. Ir tik Grybauskaitė nepajėgė.

Po šio (jau ne pirmo) atvejo, kai Dalia Polikarpovna demonstruoja savo visišką politinį bejėgiškumą, kvailai atrodo bandymai vaizduoti Lietuvos prezidentę įžymia politike ir kažkokiu unikaliu reiškiniu tarptautinėje politikoje. Esą visi Vakarų lyderiai slepia galvas smėlyje ir bijo apie Rusijos veiksmus sakyti visą tiesą. Ir tik lietuviškoji „geležinė ledi“ nebijo viską įvardinti tikriausiais vardais: tai Putiną sulyginti su Hitleriu, tai pavadinti jį paranoiku, tai paskelbti Rusiją teroristine valstybe.

1987 metais tikroji „geležinė ledi“, Didžiosios Britanijos premjerė Margaret Tetčer su istoriniu vizitu apsilankė TSRS. Maskvoje Tetčer ne tik susitiko su Gorbačiovu, apsilankė tarybinėje universa;inėje parduotuvėje ir viename sostinės rajone pabendravo su maskviečiais, bet ir davė interviu Centrinei televizijai, kurį žurnalistai pavadino istoriniu. To legendinio interviu metu „geležinė ledi“ tiesioginėje laidoje apie valandą atsakinėjo į tarybinės tarptautinės žurnalistikos meistrų klausimus, mandagiai ir su ironiška šypsenėle pasitikdama jų provokuojančius ir griežtus išpuolius. Po dešimtmečių patyrę „Pravdos“ ir „RIA Novosti“ politikos apžvalgininkai prisipažino, kad pokalbio su britų premjere metu ne ji, o jie liejo upelius prakaito.

Margaret Tetčer interviu Centrinei televizijai žiūrėjo visa šalis: po jo „geležinė ledi“ Tarybų Sąjungoje buvo pripažinta superžvaigžde. O tuo metu Tetčer pozicija TSRS atžvilgiu buvo panaši kaip šiandien Rusijos Grybauskaitės — tame interviu ji pasinaudojo galimybe išvardinti socialistinės santvarkos trūkumus, užčiaupdama tarybinį žurnalistą, pasakiusį, jog socializmas turi savo pranašumus, mandagiu klausimu, apie kokius pranašumus jis kalba.

Tačiau Tetčer intelektas ir asmenybės mastas iššaukė neregėtus pagarbą ir net gėrėjimąsi, ir tarybinė visuomenė atleido jai net antitarybinę poziciją. Tas interviu išties tapo legendiniu: tetčer nepabūgo dvikovos eteryje su tarybinės propagandinės mašinos meistrais ir nugalėjo juos jų teritorijoje.

Ar įmanoma šiandien įsivaizduoti Dalią Grybauskaitę Rusijos Pirmojo kanalo eteryje? Grybauskaitę Vladimiro Solovjovo studijoje? Grybauskaitę kaip politinio šou ekskliuzyvinę dalyvę NTV arba bet kuriame kitame Rusijos kanale, kuris Lietuvoje buvo uždraudžiamas? Ne. Ir ne todėl, kad Lietuvos prezidentė iš principo nenori turėti reikalų su „rusų propaganda“, o todėl, jog ji ne geležinė ir ne ledi — ji net bijo išsakyti filmavimo grupei nesuderintą komentarą.

JAV prezidentas Džordžas Bušas-jaunesnysis tęsė spaudos konferenciją su arabų žurnalistais po to, kai Egipto reporteris metė į jį batus. Rusijos prezidentas Vladimiras Putinas, kurį Grybauskaitė pavadino paranoiku, didelės tradicinės spaudos konferencijos metu suteikė žodį Ukrainos žurnalistui su užrašu „Ukrop“ (Krapas) ant vasarinukų ir atsakė į jo klausimą apie „baudžiamąją operaciją, kurią Jūs sukėlėte mūsų šalies rytuose“.

Galima savaip vertinti šiuos žmones, tačiau visi jie — Vladimiras Putinas, Margaret Tetčer, Džordžas Bušas — politiniai veikėjai. O Dalia Grybauskaitė — eilinė lėlė. Marionetė, kuri skaito iš popierėlio tai, ką jai parašė už siūlų tampantys žmonės, ir labai bijo, kad kada nors dėl nesuderintų klausimų laisvo bendravimo su žurnalistais metu taps akivaizdus jos politinis bejėgiškumas.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 18 — id: `scraped:rubaltic_lt:5e0242df37e74afa`

**Title:** Europa užtrenkia duris Pabaltijo imigrantams

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Dėsningas Brexit rezultatas: Didžioji Britanija užtrenkia duris Pabaltijo imigrantams . Pabaltijo bėgliai panikuoja ir, bijodami deportacijos, pasiruošę keisti savo lietuvišką arba latvišką pilietybę į britų. „Senosios Europos“ kontinentinės šalys taip pat nerodo noro priimti „angliškus tadžikus“ ir grąsina neįsileisti Londono į vieningą europietišką rinką, jeigu britai neleis įvažiuoti ES bėgliams. Rytų europietiška imigracija tampa ES ne mažesne problema, nei bėgliai iš Azijos ir Afrikos, ir prievartinis emigrantų grąžinimas į Pabaltijį sukels Estijai, Latvijai ir Lietuvai nacionalinę katastrofą.

Galimybė apriboti rytų europietišką imigraciją buvo pagrindinis Didžiojoje Britanijoje išstojimo iš ES šalininkų argumentas. Praktiškai būtent migracijos srauto apribojimu ragino Brexit šalininkai agitacijos metu balsuoti už pasitraukimą iš ES. Viena — bėgliai, antra — britai buvo raginami atsikratyti absurdiško Briuselio biurokratizmo, kuris ėmėsi reguliuoti viską: kvotas, apribojimus, techninius standartus, begalinį valdininkų vilkinimą ir popierizmą.

Tačiau šie raginimai buvo adresuoti atskiroms profesinėms grupėms: fermeriams, jūreiviams, britų pramonės darbuotojams. Visiems gyventojams Brexit šalininkai piršo migracijos temą — atkakliai naudojo vieną taikinį. Praktiškai raginimai įgyti pilnavertį suverenitetą ir „susigrąžinti nepriklausomybę“ ne tiek skambėjo kaip atsisakymas vykdyti Eurokomisijos direktyvas, kaip atstatyti savo sienų kontrolę ir įgyti garantuotiną galimybę nepraleisti per ją, pirma, Azijos ir Afrikos, antra, bulgarų, rumunų, lietuvių ir kitokių bėglių.

Panika dabar plečiasi Pabaltijo socialiniuose tinkluose, migrantų, atvykusių į Albioną nuo Baltijos pakrančių, bloguose ir forumuose. Daugelį metų Anglijoje gyvenę imigrantai nematė reikalo keisti latvių arba lietuvių pilietybę į britų („tai vieninga Europos Sąjunga“), dabar ketina skubiai tuo užsiimti, kol Didžioji Britanija galutinai neišstojo iš ES. Priešingu atveju po kelerių metų Estijos, Latvijos ir Lietuvos piliečiai sulauks deportacijos.

Atskiras panikos internete žanras — Pabaltijo imigrantų kalbos apie Britų salų senbuvių į juos požiūrį. Vis besikartojanti istorija — apie tai, kaip kitą rytą po referendumo pas kauniškį ar daugpilietį lankėsi anglų proletarai, „mėlynosios apykaklės“ (o dar ir visiškų miesto apačių atstovai) ir ragino ruošti lagaminus: „dabar tai jus visus tikrai išveš“. Latvijos ambasada Londone, prisiklausiusi tokių istorijų, net paragino kraštiečius pranešti jai apie tokius anglų senbuvių išpuolius. Likimo ironija: kovoti su ksenofobija kviečia šalis, kuri savo nepriklausomybės aušroje atėmė iš ne vietinės kilmės gyventojų pilietybę ir įtvirtino savo Konstitucijoje nuostatą, kad Latvija sukurta ir egzistuoja latviams.

Ką gi, baimės akys didelės — sunku įsivaizduoti, kad britų vyriausybė net po galutinio šalies išstojimo iš ES deportuos užplombuotuose vagonuose visus lietuvius ir latvius į gimtąjį Pabaltijį. Tačiau tarp pabaltijiečių besitęsianti šia proga panika reikšminga: apie galimą deportaciją latviai ir lietuviai rašo taip, lyg juos iš Londono norima išgabenti ne į mylimą šalelę, o tiesiai į Sibirą.

Tačiau ši panika — dar pusė bėdos.

Kaip jau buvo pasakyta, Brexit‘as sukelia rimtus sunkumus, tačiau netampa katastrofa Pabaltijui ir kitiems pigios darbo jėgos eksportuotojams — „angliškų tadžikų“ srautas vis tiek bus perorientuotas į Vokietiją, Prancūziją ir kitas Vakarų Europos darbo rinkas. Tačiau praeitą savaitę prasidėjusi europietiškų santykių krizė plečiasi tokiu greičiu, kad ši istorija jau įgavo tęsinį.

Pasirodo, romanų-germanų ES „branduolio“ šalys visiškai nedega noru paversti „angliškus tadžikus“ prancūziškais arba vokiškais „tadžikais“: Didžioji Britanija veikė kaip Rytų Europos problemų perkūnsargis — jos sparčiai auganti ekonomika „sugėrė“ didelę to krašto bedarbių dalį, ir tai tenkino Vokietiją su Prancūzija, kurios norėtų, kad viskas liktų savo vietose.

Pasak Prancūzijos prezidento, patekimas į vieningą europietišką rinką priklauso nuo keturių laisvių vykdymo: prekių, kapitalo, darbo jėgos ir paslaugų judėjimo laisvės. „Jei britams nereikia judėjimo laisvės, jie nepateks į laisvą rinką“, — pareiškė Fransua Olandas, pabrėždamas, kad Jungtinė Karalystė turės pamiršti laisvą europietišką rinką, o Londono vertybinių popierių birža Sityje daugiau negalės operacijų metu naudotis euru — jeigu britų vyriausybė apribos ES šalių darbuotojų įvažiavimą.

Toks tiesmukiškas ir atviras šantažas rodo, kad ES sukūrusioms šalims Rytų Europa su jos bėgliais reikalinga kaip pernykštis sniegas. Berlynui su Paryžiumi galimas rumunų su latviais priėmimas kelia tokią alergiją, kad jie pasiruošę grubiai išsukinėti rankas Londonui, tik kad šis neatsisakytų bėglių. Tačiau ir Londonas savo ruožtu prasidėjusiose kietose derybose su Briuseliu ir kitais kontinentiniais eurograndais gali pasukti nuolaidų keliu, bet tik ne migracijos srityje.

Pačia paprasčiausia ir stipriausia priežastimi balsuoti už Brexit buvo bulgarų su rumunais ir lenkų su pabaltijiečiais antplūdis britų salose. Jeigu Brexit su visais lydinčiais ir neišvengiamais dezintegracijos metu sunkumais vis dėlto pasieks logiškos pabaigos, o bėgliai vis tiek įvažiuos, iškils klausimas: kokiems velniams reikėjo to referendumo ir vardan ko buvo kovota su sunkumais? Demonstratyvūs ir maksimaliai paviešinti imigracijos apribojimai — pirmoji ir labiausiai tikėtina naujosios vyriausybės priemonė nuimant socialinę įtampą, kuri neišvengiamai augs išstojant iš ES.

Jeigu britų elitas nuspręs ignoruoti tiesioginę demokratiją ir ieškos pretekso kaip palikti Britaniją ES sudėtyje (paskelbs „itališką streiką“ ir išstojimą temps iki begalybės, prieš išstojimą nubalsuos parlamente, paskelbs, kad referendumas turėjo patariamąjį balsą), tokiu atveju teks kažką pametėti 17 milijonų už Brexit balsavusiems britams. Nes jei bus paprasčiausiai nusispjauta į daugumos rinkėjų nuomonę, seks legitymumo krizė, politinis sprogimas ir riaušės, nusiaubiant tuos pačius migrantus. Svarbiausia ir iš esmės vienintelė priemonė, kurią elitas pajėgus pametėti dalinai nuramindamas euroskeptikus — likti ES, demonstratyviai ir smarkiai sugriežtinant migracijos įstatymus.

Taip kad Londonas neturi nė mažiausios galimybės nuolaidžiauti migracijos klausimu derybose su Briuseliu ir eurograndais ir išsaugoti ankstesnį rytų europiečių bėglių srautą į Albioną.

Tačiau ir kontinentinė Vakarų Europa Prancūzijos prezidento lūpomis davė aiškiai suprasti, jog nenori priimti Jungtinės Karalystės atstumiamų Rytų Europos migrantų.

Iš visų Rytų Europos šalių ši perspektyva tragiškiausia pabaltijiečių elitui. Lenkijoje, nepaisant įvairių problemų, išlieka vystymosi ištekliai ir potencialas: ten vyriausybė tikrai žengia realius praktinius žingsnius, stabdant jaunimo emigraciją. Lenkijai būsimoji migracijos krizė, atsisakant Vakarų Europai priimti Rytų Europos migrantus, gali duoti net naudos. Tai bus rimtas iššūkis, į kurį Lenkija savo potencialo sąskaita galės duoti efektyvų atsaką, sutvirtindama savo ekonomiką ir pagerindama demografinę situaciją.

Galimybė išvengti nacionalinės katastrofos išlieka net skurstančiose Bulgarijoje ir Rumunijoje, kurios nors turi sąlyginai dideles teritorijas ir nenaudojamus, tačiau esančius gamtos resursus. Čia viskas priklauso nuo politinio elito kokybės — valdančiųjų kadrų.

Pabaltijis neturi jokių galimybių. Ketvirtį amžiaus Lietuva, Latvija, Estija naikino pramonę, pjaustė metalo laužui prekybos laivyną, atsisakė tranzito („okupacijos palikimas“), vertė žemdirbius mažinti galvijų skaičių, mesti į savartyną šprotus ir pilti į griovius pieną — vis dėl „švento reikalo“: sankcijų prieš Rusiją.

Visas šis ekonominis barbariškumas buvo pateisinamas tuo, kad Baltijos šalys pakilo į aukštesnę istorinio vystymosi pakopą — dabar tai postindustrinės valstybės, ekonomikos struktūroje dominuojančios paslaugų sferoje. Tačiau tam, kad egzistuotų toks „progresyvus“, kaip pas „Baltijos tigrus“, ekonomikos modelis, Lietuvoje, Latvijoje ir Estijoje gyveno neleistinai mažai žmonių. Jeigu „Baltijos tigrų“ gyventojų skaičius nuo 1991 metų iki šiol nebūtų mažėjęs istoriškai rekordiniais tempais, Pabaltijyje darbo neturėtų virš pusės darbingų gyventojų ir seniai būtų prasidėjusios bado riaušės.

Išstumdama perteklinius gyventojus uždarbiauti, Pabaltijo valdančioji klasė užtikrino sau socialinį ir politinį stabilumą. Tik rekordinėmis emigracijos sąlygomis galėjo egzistuoti ir „progresyvus“ postindustrinės Pabaltijo ekonomikos modelis, kai didžiulė biudžetininkų klasė valgo tiesiogines ar netiesiogines ES dotacijas, šios klasės poreikius tenkina bankų sektorius, mažmeninė prekyba, rieltoriai, draudimo agentai ir kita paslaugų sfera, o reali gamyba minimali, ir savarankiškai išsilaikyti Pabaltijo šalys seniai nepajėgės.

Naujų realijų sąlygomis teks atsisveikinti su tokiu „progresyviu“ ekonomikos modeliu. Didžioji Britanija buvo antroji stambiausia ES ekonomika ir davė 15-17 proc. bendro Europos BVP. Dabar bendras ES biudžetas ženkliai sumažės, tad ženkliai sumažės ir netiesioginių dotacijų Lietuvai, Latvijai ir Estijai iš ES fondų suma (o kas laukia dotacijų apimčių, jei Pabaltijo politikai sugebės įtraukti į ES Ukrainą, baisu ir pagalvoti).

Tačiau net eurofondų sumažejimas pradeda atrodyti menkniekiu, jeigu atkreipti dėmesį, kad prie šio sumažėjimo prisidės britų darbo rinkos uždarymas ir Vokietijos, Prancūzijos ir kitų kontinentinės Europos ES „donorų“ atsisakymas priimti vietoj britų Pabaltijo bėglius. Dalis išvykusių gyventojų turės sugrįžti į Pabaltijį, o nauja perteklinių gyventojų karta nepajėgs taip lengvai iš ten išvykti. Viso to rezultatas — dabartiniai Europos Sąjungos poslinkiai kelia Lietuvai, Latvijai ir Estijai didžiulės nacionalinės katastrofos grėsmę.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 19 — id: `scraped:rubaltic_lt:ac9b97e463c07b76`

**Title:** Norint išgelbėti ES reikės išvyti Rytų Europą su Pabaltiju

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Viena svarbiausių Didžiosios Britanijos pasitraukimo iš ES balsavimo priežasčių tapo Rytų Europos problema, su kuria britams teko susidurti daug dažniau, nei kitiems europiečiams. Jungtinei Karalystei atsisveikinus su Europos Sąjunga, ši problema dar labiau paaštrės. Pabaltijis ir kiti depresiški Europos pakraščiai dar labiau įtakos euroskepticizmo ir išcentrinių nuotaikų ES plėtrą, nei migrantų iš Azijos ir Afrikos kvotos ar eurozonos problemos. Sisteminės europietiškos integracijos krizės atveju Vokietijai ir kitiems Europos grandams, norint išgelbėti ES, liks viena išeitis: pašalinti iš jos Rytų Europą su Pabaltiju.

Po beveik pusės europietiškos integracijos amžiaus prasidėjo atvirkštinis procesas: dezintegracija. Atsitiko tai, ko dar praeitą savaitę nebuvo įmanoma įsivaizduoti: Didžioji Britanija prabalsavo už pasitraukimą iš ES. Brexit‘u netikėjovedantieji britų politikai ir ES valdininkai, proeuropietiškų Jungtinės Karalystės gyventojų nuotaikų viršenybę euroskeptikų atžvilgiu fiksavo visos sociologinės apklausos. Tačiau įvyko neįmanoma: už išstojimą iš ES pasisakė 52 proc. britų.

Pirmasis istorijoje referendumas dėl išstojimo iš ES įvyko būtent Didžiojoje Britanijoje: pastaraisiais keleriais metais ši šalis užtikrintai pirmavo tarp euroskeptikų. Alergiją Briuseliui plačiai jaučia daugelio Europos šalių elitas ir gyventojai, tačiau tik debesuotame Albione už išstojimą iš ES pasisakė virš 50 proc. gyventojų. Dėl kokios priežasties britams nereikia „europietiškos vienybės“? tą prie\astį nesunku įžvelgti pastudijavus priešrinkiminę britų politikų retoriką ir pagrindinius klausimus, dėl kurių Devido Kemerono kabinetas pastaraisiais dvejais metais derėjosi su Europos komisija, šantažuodamas eurobiurokratus Didžiosios Britanijos išstojimu iš ES. Šiose derybose — keturios svarbiausios temos: suteikti britų parlamentui teisę vetuoti Eurokomisijos direktyvas, atsisakyti plėsti Briuselio įgaliojimus ir riboti nacionalinių vyriausybių įgaliojimus, suteikti eurą įvedusioms šalims ir išsaugojusioms savo nacionalinę valiutą lygias teises sprendžiant ekonominius klausimus, o taip pat apriboti judėjimo laisvę, suteikiant Londonui teisę riboti rytų europietišką imigraciją, neįsileidžiant į Britų salas lenkų ir pabaltijiečių.

Jeigu pirmuosius tris derybų punktus gali pasirašyti daugumos ES šalių tautos ir vyriausybės, tai rytų europietiška imigracija — specifinė britų problema. Iš visų „senųjų europiečių“ anglai pirmieji savo kailiu patyrė „naujosios Europos“ problemą. Būdama geografiškai nutolusi nuo šio regiono, Didžioji Britanija labiausiai susidūrė su pasekmėmis skuboto priėmimo į savo gretas vis naujų rytų europiečių. Begalinis lenkų ir pabaltijiečių antplūdis tapo Albiono gyventojams nesibaigiančiu galvos skausmu.

Pirma, britams uždarius sieną nesibaigiantis rumunų, chorvatų, lietuvių ir latvių bedarbių srautas persiorientuos ir šliūkštels į kontinentinių Vakarų Europos šalių darbo rinką. Tos problemos, kurios iki šiol kamavo Birmingemą, Glazgą ir Mančesterį, persimes į Berlyną, Frankfurtą prie Mainos ir Marselį.

Beje, bėglių iš Azijos ir Afrikos antplūdis į Europą vis dėlto yra ypatinga situacija ir gali būti sustabdyta. Netekusių Rytų Europoje darbo ir nepajėgiančių tėvynėje išgyventi srautas bus neišsenkantis, nes jį pagimdė europietiška integracija. Tikėtina, kad netolimoje ateityje bėgliai iš rytų erzins vokiečius ir prancūzus mažiau nei afrikiečiai ir arabai, tačiau laikui bėgant rumunų, lenkų ir pabaltijiečių antplūdis pakenks „Vieningos Europos“ populiarumui Vokietijoje ir Prancūzijoje taip, kaip tai nutiko Anglijoje.

Antra, pasitraukus iš ES antrai stambiausiai Europos ekonomikai Didžiosios Britanijos dalis, papildant ES biudžetą, bus perskirstyta tarp likusių Europos Sąjungos „donorų“. T.y. be dotacijų ir savarankiškai finansiškai neišgyvenanti Rytų Europa taps „seniesiems europiečiams“ dar didesne našta. Neabėjotina, tai skatins išcentrinių nuotaikų plėtrą: toje pačioje Didžiojoje Britanijoje raginimai nustoti maitinti Rytų Europą, kasmet pervedant į ES biudžetą „nereikalingus“ du milijardus eurų, suvaidino agitacinėje Brexit šalininkų kampanijoje svarbų vaidmenį.

Pakanka peržvelgti pagrindines Pabaltijo respublikų diplomatinio aktyvumo kryptis, ir taps aišku, apie ką eina kalba. Beatodariškas pritarimas Transatlantiniam prekybos investicinės partnerystės (TPIP) projektui neleidžia net mintyse suabėjoti, kad europiečiai galėtų kur nors nepritarti amerikiečiams. Bandymas blokuoti statybą antrosios dujotiekio „Šiaurės srautas“ šakos, kurios projektas ne tik rusiškas, bet ir vokiškas (t.y. Pabaltijis įkyriai bando neduoti pinigų tai rankai, kuri jį maitina). Kova siekiant pratęsti sankcijas prieš Rusiją, kurios kenkia visiems pabaltijiečių rėmėjams ir, žinoma, pačių Lietuvos, Latvijos ir Estijos ekonomikoms.

Atskira pokalbio tema — aistringas „naujosios Europos“ elitų siekis plėsti ES šalių gretas.

Dauguma naujų šalių, tame tarpe ir Pabaltijo, neatitiko narystės ES Kopenhagos kriterius, tačiau buvo priimtos į „europietišką šeimą“. Dabar šių šalių vadovybės švyti eurooptimizmu, besiribojančia su euroidiotizmu, ir siekia tolimesnės ES plėtros priimant į ją dar vargingesnes, problemiškas ir nevaldomas šalis.

Prieš metus, tą dieną, kai „Dešiniojo sektoriaus“ kovotojai susirėmė su Ukrainos karinėmis pajėgomis dėl cigarečių kontrabandos lenkų-slovakų pasienyje, Latvijos URM vadovas Edgaras Rinkevičius ukrainiečių televizijoje džiaugsmingai palaikė Ukrainos siekį įstoti į ES. Kaip eiliniai europiečiai vertina perspektyvą papildyti savo gretas sąskaita 40 milijonų Ukrainos gyventojų su jos vargingumu, korupcija, „Dešiniuoju sektoriumi“, karu Donbase ir kita specifika, parodė balandžio mėnesį vykęs olandų referendumas, į kurį darbo dienos metu panoro ateiti apie trečdalį rinkėjų — jų dauguma pasisakė prieš Ukrainos priėmimą.

Tačiau jokia Europos visuomeninė nuomonė neprivers rytų europiečių atsisakyti „europietiško pasirinkimo“ eksporto: neatsitiktinai jau kitą rytą po olandų referendumo Lietuvos prezidentė Dalia Grybauskaitė įrašė telekreipimąsi ragindama nekreipti dėmesio į olandų balsą ir tebetempti Ukrainą į ES. Toks sveiko proto ir eilinių europiečių nuomonės nepaisymas ateityje tik stiprins „senosios Europos“ nepasitenkinimą.

Jungtinė Karalystė priėmė ant savo pečių darbą praradusių bėglių problemas ir buvo pagrindiniu antirusiškų išpuolių ir „naujosios Europos“ kompleksų advokatu. Be Londono pritarimo ir užuojautos Latvija ir Lietuva iškart būtų tapusios vietinėmis pamišėlėmis — Europos kiemų kaimo kvailelėmis, klejojančiomis „žaliais žmogeliukais“. Didžiosios Britanijos delegatų Briuselyje palaikymas padėjo Lietuvai, Latvijai ir Estijai pakelti rusofobijos retoriką į šiek tiek aukštesnį lygį — dabar net amerikiečių „vanagai“ pripažįsta, kad be Londono pabaltijiečiams bus daug sunkiau lenkti ES savo antirusišką liniją.

Tačiau tą penktadienį dauguma britų tarė „gana!“. Tąsykitės patys su latvių juodadarbiais, apmokėkite rumunams ir lenkams socialines pašalpas, siųskite į Briuselį pinigus Chorvatijos ir Slovakijos dotacijoms, dalyvaukite lietuvių geopolitiniuose žaidimuose, o mes kaip nors be to apsieisime.

Tokiu būdu Rytų Europos ir bėgančių iš jos gyventojų problemos nuo šiol gula ant ES sukūrusių šalių pečių. Ateityje šios problemos skatins „Vokietijos alternatyvos“, prancūzų „Nacionalinio fronto“, danų Laisvės partijos, italų „Šiaurės lygos“ ir kitų Europos Sąjungos išsivaikščiojimo euroskeptikų populiarumą. Jie sustiprins separatistų tendencijas turtingiausiuose Europos regionuose: ispanų Katalonijoje, beldų Flandrijoje, italų Venete — šių regionų gyventojai turės maitinti ne tik vargstančius savo pietinius tėvynainius, bet dar ir kažkokią Lietuvą, apie kurią jie nieko nežino, kas tai yra, net kur ji yra ir kaip tą žodį teisingai parašyti.

Sakysite, toks scenarijus pernelyg radikalus ir praktiškai neįgyvendinamas? Bet ar Didžiosios Britanijos pasitraukimas iš ES iki lemtingo penktadienio atrodė fantastiškas ir praktiškai neįmanomas. Dar prieš savaitę ES atrodė kaip aukščiausia žmonijos išsivystymo pakopa, visuomeninės-politinės statybos etalonas, klestintis miestas ant kalvos, kuris gali tik plėstis, bet ne siaurėti. Dabar gi po šešių europietiškos integracijos dešimtmečių prasidėjo europietiška dezintegracija: britų pavyzdžio įkvėpti „Vieningos Europos“ priešininkai vienas po kito gali inicijuoti išstojimo iš ES referendumus. Danija, Suomija, Olandija, Prancūzija — visose ES šalyse donorėse plečiasi antibriuseliškos nuotaikos, ir ES išsivaikščiojimo šalininkai gali ten sulaukti rimto palaikymo.

Europoje negalima tokio masto krizė, kai bus iškeltas ES išlikimo klausimas? Tačiau krizės tendencijos Europoje jaučiasi pastaruosius keletą metų, ir visiems prognozėms paprieštaravęs Brexit — ryškiausias jų indikatorius. Pagal kapitalistinės sistemos funkcionavimo ciklą perprodukcijos krizė prasideda kas 10-15 metų, tad kai eilinė ekonominė krizė guls ant neišspręstų ir apleistų ES problemų, tada ir sulauksime sisteminės ir sukrečiančios europietiškos integracijos krizės.

Netenka abejoti, kad sisteminės krizės metu ES sukūrusios šalys šalin nustums visus sentimentus ir rūpestį prijaukintais.

Tokiu sąjungininkų nesiskaitymu įžeista Lenkija net sukvietė alternatyvų tų ES šalių, kurios nebuvo pakviestos į Berlyną, URM vadovų susibėgimą. Tačiau suprantama, kad šis diplomatinis žingsnis nieko nereiškia. Bendras Vokietijos ir Prancūzijos kovos su krize planas gali įtakoti Europos likimą, tačiau eilinis garsus priminimas apie Lenkijos ir Pabaltijo egzistavimą neįtakos nieko ir niekada. Dabar ES įkūrėjai turi savą galvos skausmą, o ateityje, kai situacija galutinai spustels, jie gali juos išvyti iš ES.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 20 — id: `scraped:rubaltic_lt:6353c99c2b20ca66`

**Title:** Failed nations: latviams ir lietuviams nereikia Latvijos ir Lietuvos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Emigracija iš Latvijos ir Lietuvos pagal greitį viršija visas Rytų Europoje egzistuojančias tendencijas. Įgavusį pastaraisiais metais pagreitį baltų tautų bėgimą iš savo istorinės tėvynės jau neina charakterizuoti globalių įvykių arba regioninių dėsningumų įtaka: latviai ir lietuviai paprasčiausiai nenori gyventi jiems sukurtose nacionalinėse valstybėse ir atsisako Latvijos bei Lietuvos. Gali būti, jog priežastis slypi tame, kad iš tikrųjų Latvija ir Lietuva sukurtos ne tiems žmonėms, kurie jose gyvena.

Politikos moksle ir tarptautinėje praktikoje egzistuoja sąvoka failed state — neišsigalinti valstybė. T.y. valstybė, nesugebanti atlikti pagrindinių valstybės funkcijų, kurioje visiškai subyrėjo valstybės valdžia ir valdymo aparatas ir kuri negali egzistuoti be užsienio paramos.

Pabaltijo respublikų valdžioms galima pareikšti daug pretenzijų, tačiau vis dėlto negalima teigti, kad jos neišsigalinčios. Žinoma, atviras lieka klausimas, kaip gyvens šios šalys, jeigu staiga išnyks ES struktūrinių fondų dotacijos ir savo pabaltijietiškus satelitus tarptautinėje arenoje nustos rėmęs Vašingtonas. Tačiau kol tai neįvyko, Lietuva ir Latvija atrodo išsigalinčiomis. Gatvių gaujos jų miestų neužgrobia, namuose yra šviesa ir vanduo, nusikaltėliai gaudomi. Ir vis dėlto šių šalių gyventojai skuodžia svetur greičiau, nei iš kai kurių Afrikos „bananinių respublikų“.

Labiau paradoksali, nei Pabaltijyje, situacija Rytų Europoje ir potarybinėje erdvėje susiklostė tik Moldavijoje su jos antinacionalinio nacionalizmo fenomenu, kai daugelis moldavų laiko save rumunais, moldavų kalbą — rumunų dialektu, o Moldaviją — Rumunijos dalimi, į kurios sudėtį ji turi sugrįžti. Tačiau neigdami save kaip naciją moldavai vis dėlto mato save sudėtine didesnės nacijos dalimi. Emigruojantys latviai ir lietuviai nemato savęs kitos nacijos sudėtyje: jie tik perka bilietą į Londoną, išskrenda, įsilieja į naują visuomenę, užmiršta naujoje tėvynėje savo kalbą ir praranda (jei ne jie, tai jų palikuonys) pradinę priklausomybę konkrečiai tautai.

Tokio gyventojų išbėgimo, kaip pastaraisiais 25 metais, Pabaltijis dar nebuvo patyręs. Iki savojo valstybingumo atkūrimo, kai buvusi etninė grupė tapo privilegijuota pagrindine tauta, lietuviai ir latviai nebėgo svetur tokiu greičiu. Jokia „okupanto letena“ — vokiška, švediška, lenkiška ar rusiška — nesukūrė tokios emigracijos. Tokiu greičiu, kaip dabar iš Pabaltijo, bėgo nuo angliškųjų okupantų XIX amžiuje į Ameriką airiai, tačiau baltų tautos nuo Rusijos imperijos, lenkiškųjų ponų ir vokiškųjų baronų taip neskuodė. Nebėgo taip ir tarpukario metais. Dideliu greičiu jos ėmė bėgti tik dabar nuo dabartinių savų valdančiųjų.

Iki šiol Latvijos ir Lietuvos gyventojų bėgimo pasauliniai rekordai (beje, iš Estijos išvyko daug mažiau žmonių, kaip ir iš Lenkijos, ir pagal gyventojų skaičiaus mažėjimą ši Pabaltijo respublika nepatenka į vieną su Latvija ir Lietuva grupę) buvo aiškinami 2008-2009 metų pasaulinės krizės įtaka ir bendra Rytų Europai gyventojų emigravimo į Vakarus tendencija. Emigracija iš Latvijos ir Lietuvos ženkliai ūgtelėjo krizės metais, tačiau ji egzistavo iki jos ir neužsibaigė po jos. Visą „antrosios nepriklausomybės“ ketvirtį amžiaus baltų respublikų migracijos saldo atrodė neigiamai: bėgti iš Latvijos ir Lietuvos nenustota nei 90-aisiais, nei „riebiaisiais metais“, nei krizės laikotarpiu, nei po jos. Bėga ir dabar, nepaisant pirmųjų Pabaltijo šalių asmenų optimistinių pareiškimų, kad ekonomika ir pragyvenimo lygis jų šalyse auga sparčiau, nei vidutiniškai ES. Pabaltijo emigraciją jau neina paaiškinti bendra Rytų Europos tendencija. Vidurinėje ir Rytų Europoje praeitų metų emigracijos skaičiai be Pabaltijo ūgtelėjo tik Slovakijoje. Čekijos gyventojų emigracija 2015 metais sumažėjo 33,5 proc., Vengrijos — 22,2. Iš Lenkijos 2014 metais išvyko žmonių 3 proc. mažiau, nei 2013-aisiais.

Tuo pat metu iš Latvijos pernai išvyko 5,7 proc. žmonių daugiau, nei pernai. Vien tik per 2015 metus Latvija prarado 1 gyventojų proc. Absoliutaus europietiškos emigracijos rekordo pasiekė Lietuva, praeitais metais praradusi 1,5 gyventojų proc. — 2015 metais iš Lietuvos išvyko 21,6 proc. žmonių daugiau, nei 2014-aisiais. Triskart lyginant su 2014 metais padidėjo emigrantų skaičius iš Estijos.

Tačiau būtent prieš Lietuvą ir Latviją visų pirma liudija praeitis, dabartis ir ateitis. Praeitis — tas 25 metus nesibaigiantis gyventojų skaičiaus mažėjimas, dėl ko dvi respublikos prarado apie trečdalį savo žmonių. Dabartis — ūgtelėjusi emigracija esą ekonominio augimo, politinio stabilumo ir ženklios emigracijos kitose „naujosios Europos“ šalyse sąlygomis. Ateitis — pernykštis Eurostat pranešimas, pagal kurį Latvija ir Lietuva artimiausiais dešimtmečiais aplenks Bulgariją ir Rumuniją ir taps absoliučiomis Europos mirštamumo rekordininkėmis. Lietuvai Eurostat prognozuoja 38 gyventojų proc. praradimą, Latvijai — 31.

Šią prognozę patvirtina vidinės apklausos Latvijoje ir Lietuvoje, rodančios, kad virš ketvirtadalio dar likusio gyventojų skaičiaus ateityje ketina emigruoti. Į Angliją ir Airiją emigravusių apklausa rodo, kad grįžti į tėvynę ketina 10-20 jų proc.

Emigracija — pagrindinė visų šių baisių skaičių priežastis. Pabaltijis per 25 pastaruosius metus nepatyrė jokių karų, epidemijų, teritorijų praradimų, tačiau per tą taikos ir stabilumo laikotarpį emigracija jį nusiaubė labiau, nei Didysis Viduramžių maras. Ir tas gyventojų išnykimas startavo būtent susigrąžinus nacionalines valstybes, atkūrus savo etnines grupes pagrindinių tautų statuse ir ypač — savosios valstybės valdžios šaltinį. Visokeriopai buvo pabrėžiama (atsiverskite Latvijos konstitucijos įžangą), kad baltų šalys kuriamos latvių ir lietuvių gerovei ir klestėjimui, kad lietuvių ir latvių valstybių misija — išsaugoti neskaitlingas ir jaučiančias išnykimo pavojų tautas. Latvija ir Lietuva skelbėsi žmonių labui egzistuojančiomis valstybėmis. Ir ne šiaip sau kažkokių žmonių, o būtent latvių ir lietuvių.

To išdavoje susiklostė situacija, kai latviai ir lietuviai būriais bėga iš jiems sukurtų valstybių. Kodėl?

Yra Europoje tokia šalis — Islandija. Viena iš turinčių mažiausiai gyventojų — 320 tūkstančių. Praktiškai visi gyventojai pagal tautybę — islandai, mažytė šiaurės tauta, tikslu išsaugoti kurią ir sukurti kuriai gerovę ir buvo savo laiku sukurta Islandija. Ir štai etninių islandų bei Islandijos gyventojų skaičius auga rekordiniais tempais. Migracijos įstatymai tokie griežti, kad imigracija į Islandiją de-fakto uždrausta, todėl šalies demografinė situacija — Islandijos valstybės pasiaukojančio darbo rezultatas.

Gimstamumas Islandijoje viršija mirtingumą du kartus. Gimstamumo koeficientas — 2,2 kūdikio moteriai. Gyventojų skaičius vien tik gimstamumo dėka per metus auga 1,2 proc. Vidutinė gyvenimo trukmė — 81 metai. Emigracija iš šalies nulinė — net tie jauni žmonės, kurie išvyksta mokytis arba pažvelgti į didįjį pasaulį, praktiškai visada sugrįžta. Nėra grėsmės islandų tautai, ir tai rezultatas valstybės pastangų, kurios skiriamos savo gyventojų gerovės ir klestėjimo kūrimui.

Palyginkime šią idiliją su Baltijos šalimis, kurios esą taip pat sukurtos savo gyventojų, ypač — tituluotų, gerovės ir klestėjimo labui. Mirtingumas Lietuvoje ir Latvijoje stabiliai viršija gimstamumą. Vidutinė gyvenimo trukmė — 74 metai, o Lietuva pagal savižudybių skaičių vienam gyventojui pirmauja pasaulyje. O kuo tuo metu užsiiminėja abiejų respublikų valdžios? Demografine politika? Socialia? Sveikatos apsauga? Gal remia šeimą? Gina motiną ir vaiką? Laukite. Keliaklupčiavimas prieš užjūrio šeimininką, karjera Briuselyje, kariniai-politiniai žaidimai su NATO, „Rusijos stabdymas“, geopolitika — štai kas jas domina. Į žmones šioms valdžioms nusispjauti, todėl žmonės ir bėga.

„Dar ir dar kartą reikia pripažinti, kad pagrindinė emigracijos priežastis ekonominė: bėga iš ten, kur gerovės lygis žemesnis, kur mažesnės pajamos ir algos, bėga ten, kur aukštesni gerovė ir pajamos“, — sako Lietuvos demografė Vlada Stankūnienė.

„Ką galvoja kūdikį planuojanti šeima, girdėdama, kad vyriausybė daugiau nepadės toms šeimoms, kurioms neliko vietos municipaliniuose vaikų darželiuose? — klausia latvių demografas Ilmar Mežs. — Net jei vyriausybė rytoj ištaisys savo klaidą, atsakingos šeimos neskubės gimdyti žinodamos, kad valstybė bet kuriuo momentu gali sugalvoti „siurprizus“.

Lieka neišsiaiškintas dar vienas klausimas. Daugelyje kitų šalių, tame skaičiuje potarybinėse respublikose, ekonominė ir socialinė situacija nėra geresnė, o neretai ir blogesnė, nei Latvijoje ir Lietuvoje. Tačiau žmonės iš ten 25 metus tokiu greičiu nebėgo ir nebėga. Kodėl?

Ką pamatėme praktikoje? Latviai ir lietuviai ne tik negyvena kaip danai ir švedai, bet gyvena dabar blogiau negu TSRS. Kovotojai už jų laisvę ir valstybingumą pasireiškė kaip vagys, kuriuos domina ne „žmonių gerovė“, o Amerikoje ir Europoje sėdinčių šeimininkų požiūris į jų „geopolitinius žaidimus“. Tautos užmirštos. Socialinė sfera ir demografija — ne prioritetas ir niekada juo nebuvo. Kuo garsiau žmonės šaukia apie išmirimą, tuo labiau valdžios stengiasi nematyti šios problemos.

Štai jums ir emigracija iš melo Europos į Europą tikrąją. Esant tam tikrom sąlygom žmogus, tauta gali ilgai kentėti materialius nepriteklius ir apribojimus. Tačiau kai tavo valdžios tiesiai į akis meluoja 25 metus, atleisti neįmanoma.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```
