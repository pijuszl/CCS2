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

### Article 1 — id: `scraped:rubaltic_lt:23e4b9baf1008a10`

**Title:** ES atsisakė finansuoti Lietuvos kovą su  „Lukašenkos migrantais„

**Source:** rubaltic_lt (propaganda)

**Text:**

```
ES nefinansuos užtvarų statybą išilgai savo išorės sienų. Apie tai, po konsultacijų su šalių – bendrijos narių lyderiais, pareiškė Europos komisijos vadovė Ursula fon der Leyen. Lukašenkos „hibridinės agresijos“ aukoms siūloma įvairi parama - nuo Frontex agentūros darbuotojų paslaugų iki humanitarinės pagalbos nelegaliems migrantams. Bet tvoros tverimui išilgai viso „paskutinės Europos diktatūros“ perimetro pinigų niekas neduoda.

„Iš tikrųjų, šia tema (tvorų tvėrimas išilgai ES rytų sienų - RuBaltic.Ru pastaba) buvo diskutuojama. Kaip žinoma, yra finansavimas iš ES biudžeto, šis finansavimas liečia ne tik įrangą, tame tarpe elektroninę techniką, dalinai personalą, bet ir infrastruktūrą. Kalbama apie taip vadinamą fizinę infrastruktūrą. Mes, kaip ir Europos komisija, taip ir Europos parlamentas, sutinkame su tuo, jog tvorų ar užtvarų su spygliuota vielą tvėrimas neturi būti finansuojamas iš ES biudžeto“, - pareiškė Ursula fon der Leyen.

Nesunku suprasti būtent kas kėlė šį klausimą.

Dar prieš ketverius metus lietuviai pabandė tai padaryti. Tada Sauliaus Skvernelio vyriausybei kilo idėja užtverti 130 kilometrų ilgio tvorą išilgai sienos su Kaliningrado sritimi, bet Europos komisija pareiškė, jog ji „ne finansuoja tvorų ar barjerų tverimą išilgai išorės sienų“.

Panašu, jog valdantieji Lietuvos konservatoriai apie tai užmiršo. Paskubomis pradėdami tverti tvorą išilgai sienos su Baltarusija, jie akivaizdžiai vylėsi gauti papildomas dotacijas iš Europos fondų. Atsakymas buvo žaibiškas. „Europos komisija ne finansuoja tvoras. Mūsų finansavimas nukreiptas į integruotus sienų valdymo sprendimus, kurie garantuoja, jog neteisėti kirtimai neliks nepastebėti, ir kurie susiję su efektingu ir sparčiu migracijos ir prieglobsčio suteikimo valdymu“, - pranešė Europos komisijos spaudos tarnyba.

Europos Sąjungos atstovas vidaus reikalams Adalbert Janc dėl „smulkesnės informacijos apie barjerų idėją“ patarė kreiptis į Pabaltijo respublikų vadovybę, kadangi tai yra jų pačių iniciatyva. Kiek vėliau žurnalistai vėl paklausė jo, ar Europos Sąjunga skirs pinigų „didžiosios lietuviškos sienos“ statybai. Janc pakartojo anksčiau pagarsintą tezę: „Europos komisija nemano tikslingu finansuoti iš ES fondų užtvarų ir barjerų tverimą. Todėl šis infrastruktūrinis objektas neturi būti finansuojamas iš ES fondų“.

Lieka tik spėlioti, kodėl Vilnius nepasipiktino tokiu atsakymu. Juk tezę apie tai, kad „EK nefinansuoja tvoras“ galima lengvai paneigti. Už Europos pinigus, pavyzdžiui, buvo pastatyta Seutos siena. Ir visa tai atsitiko 1993 metais, pasibaigus „šaltajam karui“, kai Vakaruose triumfavo „atvirų sienų“ principas“...

Dar 2017 metais Latvija, tarp kitko, projektavo tvorą išilgai Baltarusijos sienos. Vėliau išaiškėjo, jog šiam projektui skirti pinigai buvo išvogti, bet Krišjano Karinšio ministrų kabinetas nusprendė ištaisyti pirmtakų klaidas.

„Dabar mes galime pradėti tvoros iš spygliuotos vielos tvėrimą išilgai Latvijos -Baltarusijos sienos. Tvoros ilgis 37 kilometrai, ja užtversime pačius kritiškiausius ruožus“, - rugsėjo mėnesį informavo Latvijos Vidaus reikalų ministrė Marija Golubeva.

Lenkai dar rugpjūčio mėnesį, pranešė, jog savo jėgomis tvora užtvėrė apie 100 kilometrų. Nacionalinės gynybos ministro apipublikuotose fotografijose jokios tvoros nematyti. Matosi tik dvi eilės spygliuotos vielos spiralių, žemesnių už žmogaus ūgį. Tvirtų afrikiečių ar arabų (kaip taisyklė, būtent tokie šturmuoja ES rytų sienas) šios kliūtys tiksliai nesustabdys.

„Didžiosios lietuviškos sienos“ statybos išilgai Baltarusijos sienos kaina pradžioje buvo vertinama 15 milijonų eurų suma. Vėliau ši suma išaugo iki 42 milijonų, o rugpjūčio mėnesį Lietuvos ministrė pirmininkė Ingrida Šimonytė pagarsino naują sąmatą: 150 milijonų eurų. Jei ES prisiims nors dalį šių išlaidų, tai po kurio laiko paaiškės, ginanti nuo Lukašenkos „hibridinės agresijos“ tvora turi būti aukštesnė, spygliuotoji viela – tvirtesnė, vaizdo kameros – galingesnės. Trumpai pasakius, reikia daugiau pinigų.

Briuselio reakcija dėsninga. Ursula fon der Leyen ne atsitiktinai pabrėžė, jog sprendimą atsakyti Lenkijai ir Lietuvai finansinės paramos priėmė ne kokie tai eurobiurokratai, o ES narių – šalių lyderiai. Išleisti šimtus milijonų eurų tvorų tvėrimui išilgai Baltarusijos valstybės sienos perimetro jie mano netikslingu.

Lietuvos prezidentas Gitanas Nausėda mano, jog tai didelė pergalė, esą, Europa parodė savo pasiruošimą gintis. Bet jis ir pridėjo: „Mes negalime išspręsti antrinę migracijos problemą, kol neišsprendėme pirminę, ir pirminė migracija – prie mūsų sienos“.

Kai reikalas liečia konkrečių Europos Sąjungos rytų sienų stiprinimo projektų finansavimą, Lukašenkos „hibridinių atakų“ liudytojai kažkodėl tai slepia savo galvas smėlyje. Kartu su tuo niekas nesako, jog tvora – blogas dalykas. Atvirkščiai, jau paminėtas Adalbert Janc pagyrė lietuvišką iniciatyvą: „Čia nėra nieko prieštaringo. Europa nefinansuoja barjerų tvėrimą, bet tai nereiškia, jog konkrečioje sienos atraižoje, atskiru laiko momentu toks infrastruktūrinis objektas negali būti efektyviu“.

Niekaip kitaip, kaip Lietuvos interesų nepaisymu tai nepavadinsi.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 2 — id: `scraped:rubaltic_lt:d290f1067620ab90`

**Title:** Tos sankcijos grynas juokas: Lietuva rekordiniais tempais didina importą iš Baltarusijos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Sausio – rugsėjo mėnesiais Lietuva importavo baltarusiškų prekių už beveik 800 milijonus eurų, tai yra 50 procentų daugiau nei per analogišką pareitų metų laikotarpį. Atitinkamus duomenis paviešino Pabaltijo respublikos Statistikos departamentas. Kaip tai bebūtu paradoksalu, bet Baltarusijos – Lietuvos prekybą pagyvino... sankcijos Lukašenkos režimui. Būtent jos prisideda prie produkcijos, kuri artimiausiu metu gali būti uždrausta, importo augimo į ES.

Į Baltarusijos importą Lietuvoje dėmesį atkreipė visuomeniniai aktyvistai, kurie pastebėjo, jog kiekvienas dešimtas alaus litras jų parduotuvių lentynose yra pagamintas Lukašenkos valstybės įmonėje "Krinitsa“.

To pačio, kurį „paskutinis Europos diktatorius gyrė dar 2003 metais. „Žigulinio“ receptams aš teikiu pirmenybę mūsų „Krinitsos“, ir taip toliau, mūsų markės, mūsų brendai“.

„Lietuvos parduotuvėse yra nemaža baltarusiško alaus. Gaspadorių, Brolijos, Tradicinis bei kitos, lietuviškomis etiketėmis pažymėtos rūšys iš tikrųjų pagamintos Baltarusijos valstybės įmonėje Krinitsa, kuriai vadovauja Lukašenka. Preliminariais duomenimis, kiekvienais metais Lietuvoje parduodama apie 20 milijonų litrų baltarusiško alaus, kas sudaro beveik 10 visos vidaus rinkos procentų. Režimui reikalinga valiuta, todėl alus parduodamas pigiai, vadinasi, Lietuvos aludariams sunku konkuruoti su tokia pigia produkcija“, - kalbama vienoje iš Facebook grupių, kurioje agituojama prieš baltarusišką produkciją.

Su tokiu požiūriu sutinka ir Lietuvos aludarių gildijos prezidentas Saulius Galadauskas.

Bet daugelis lietuvių, deja, yra įpratę parduotuvėse rinktis patį pigiausią alkoholį. Juk Lietuva – viena iš pačių geriančiųjų šalių pasaulyje.

Norfa prekybos tinklo atstovas spaudai Darius Ryliškis taip pat diskutuoja: „Šio alaus (baltarusiško - RuBaltic.Ru pastaba) nedaug, jį siūlo asortimento paįvairinimui. Pirkėjai jį perka. Jei žmonės nepirktų, jo nebūtų pardavime“.

Jis sudaro tik 1 procentą nuo visos bendrojo importo apimties. Ir jeigu baltarusiškos „Krinitsos“ priešininkai panorės sužinoti, kuo ir kaip jų šalis prekiauja su „paskutine Europos diktatūra“, tai jų laukia neįtikėtini atradimai.

Lietuvos Statistikos departamentas dar prieš dvejus mėnesius paviešino straipsnį pretenduojantį į sensaciją.

Pagal augimo tempus tai antras rezultatas po Jungtinių Amerikos Valstijų.

„Nepaisant Vakarų bandymų sankcijomis parklupdyti Baltarusijos režimą, prekių srautas iš šios šalies į Lietuvą kol kas ne tik nesulėtėjo, bet tapo rekordiniu: įmonės skubėjo užsipirkti baltarusiškų prekių, kol nesutriko jų tiekimas“, - tvirtina Lietuvos statistikos departamentas. Su šiuo įvertinimu sunku nesutikti. Pirmosios Europos sąjungos ekonominės sankcijos Lukašenkai buvo įvestos tik po Romano Protasevičiaus sulaikymo ir pasirodė gana švelnios. Jos neliečia pagrindinių Baltarusijos eksporto prekių. Bet Lietuvos verslas puikiai supranta, jog Lukašenkos režimo „smaugimas“ – tai gana ilgai besitęsiantis procesas. Tai, ką šiandieną galima pirkti, rytoj gali tapti „uždraustu vaisiu“.

Čia mes sau leisime pacituoti mūsų 2020 metų spalio mėnesio 2 d. straipsnį: „Kai personalinės sankcijos taps ne efektyviomis, Lietuvoje būtinai atsiras politikai, kurie pasiūlys „sudraskyti į skutus“ Baltarusijos ekonomiką. Tokios nuotaikos ypatingai būdingos opoziciniams konservatoriams. Jau po kelių dienų jie gali laimėti parlamento rinkimuose ir tapti valdančiosios koalicijos partneriu“.

Konservatoriai – landsbergistai iš tikrųjų atėjo į valdžią. Tapo aišku, jog sankcijų karas su Baltarusija stiprės. Ir kaip į tai reagavo lietuviškas verslas? Palaikė naująją vyriausybę bei jos siekį palikti Lukašenką be gyvavimo lėšų? Deja, viskas įvyko tiksliai taip, tik atvirkščiai.

SEB banko ekonomistas Tadas Poviluskas atkreipia dėmesį į tai, jog dėl korona viruso pandemijos praeitais metais prekyba tarp šalių smuko. Tai yra, Baltarusija Lietuvoje paprasčiausiai dalinai atstato savo eksportinius praradimus. Per 2019 metų sausio – rugsėjo mėnesius ji nusiuntė į Lietuvą produkcijos už 812,9 milijono eurų. Per šių metų sausio – rugsėjo mėnesius – beveik tiek pat (796,6 milijono eurų). Tai yra, iki kovidinis lygis jau viršytas, jokios JAV ir ES sankcijos tam netrukdė.

Komentuodamas pirmojo pusmečio rezultatus, Poviluskas prieina prie išvados, jog sekančių šešerių mėnesių rezultatas atrodys žymiai blogiau. Bet kol kas jo prognozės neišsipildo. Liepos ir rugpjūčio mėnesiais Lietuva išlaikė spartuolišką baltarusiškos produkcijos užpirkimo tempą.

Kokios prekės dėka Baltarusija gavo didžiausią pelną prekiaudama su Lietuva? Elektros energijos. Tos pačios elektros energijos, nuo kurios Pabaltijo respublika norėjo atsitverti, paleidus „nesaugią“ Baltarusijos AE (BelAE).

Prezidentas Gitanas Nausėda, ministrė pirmininkė Ingrida Šimonytė, URM vadovas Gabrielius Landsbergis bei kiti Lietuvos isteblišmento atstovai įkalbinėjo savo draugus užsieniečius (latvius, ukrainiečius) prisijungti prie Astravo „atominio monstro“ boikoto. Tuo metu paaiškėja, jog šių metų sausio – rugpjūčio mėnesiais Lietuva užmokėjo už baltarusišką elektros energiją 132,6 milijono eurų. Maždaug 46 milijonus eurų daugiau, negu už visus (!) 2020 metus.

Tiekimas ne tik tęsiamas – jo apimtys didėja lyginant su tuo periodu, kai BelAE dar neveikė.

Atmintyje iškyla žinomos iš sovietų kino filmo dainos žodžiai: „Ką jie bedarytu, niekas nesidaro“. Lobijavo sankcijas Baltarusijai – padidino baltarusiškos produkcijos importą. Paskelbė BelAE boikotą – padidino baltarusiškos elektros energijos importą.

Jei politikams įteikinėtų premijas už pačius absurdiškiausius „pasiekimus“, Lietuvos atstovai tiksliai būtų nominuoti pretendentais į Grand-prix.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 3 — id: `scraped:rubaltic_lt:b51d1d73a6d0f29c`

**Title:** Energetikos ekspertas: Putinas siekia pardavinėti dujas Europai Rusijos biržoje už rublius

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Rusijos „Gazpromas“ neužsiima dujų kainų manipuliacijomis ir pildo visus savo kontraktinius įsipareigojimus. Apie tai pareiškė Europos komisijos vadovo pavaduotojas Franc Timmermans. Su jo nuomone nesutinka daugelis vakarų politikų, kurie, kaip ir anksčiau, kaltina Rusiją „energetikos ginklo“ panaudojimu. Apie tai, kas išprovokavo dujų krizę Europoje, kaip Vladimiras Putinas išgąsdino spekuliantus ir kodėl „Gazpromui“ reikia vystyti savo biržą RuBaltic.Ru analitikos portalui papasakojo Rusijos energetikos ekspertas Aleksandr SOBKO.

- Aleksandrai, mes matėme, jog Europos biržoje dujų kainos jau visiškai priartėjo prie 2000 dolerių už tūkstantį kubinių metrų. Bet vėliau įvyko staigus nuosmukis (iki 1000 – 1200 dolerių). Be to, tai atsitiko po to, kai Rusijos prezidentas pasisakė pasitarime energetikos klausimais. Ar galima tai pavadinti „Putino efektu“?

- Kainų augimas beveik iki 2000 dolerių už tūkstantį kubinių metrų buvo sąlygotas tam tikromis spekuliacijomis. O spekuliantams visada įtakoja verbalinės intervencijos efektas. Šiuo atveju kalbama apie pasitarimą pas Putiną, kur jis pasisakė apie galimybę padidinti dujų tiekimą į Europą.

2000 dolerių – tai jau už sveiko proto ribų.

Jei Europos energetikos rinkoje situacija būtu normali, Putino pasisakymas nebūtų padaręs tokio stipraus efekto. Buvo pasisakyta tuo momentu, kai spekuliantai pakėlė kainas iki nesveiko lygio. Čia viskas sutapo. Nors, tikėtina, kainos būtu kritusios ir pačios.

- Dujų krizės Europoje kontekste mes dažnai girdime žodį „spekuliantai“. Bet mažai kas supranta, kas tie paslaptingi žmonės, ir būtent kaip jie veikia. Galite paaiškinti?

- Iš tikrųjų, tai tradiciškai uždara istorija. Bet kai ką mes galime suprati iš žiniasklaidos. Buvo pranešama, jog Europoje nukentėjo treideriai, kadangi atverdavo trumpas ateities (fjučerių) pozicijas (paprastai kalbant, pardavinėjo dujas, kurių pas juos fiziškai nebuvo). Jiems tai reikėja padaryti apribotos rizikos fondų (hedžingo) strategijų rėmuose, kurias jie vykdė globalinėje rinkoje.

Pastaba: Hedžingas – investicijų apsaugos instrumentas, sandorių sudarymas vienoje rinkoje siekiant kompensuoti kainų rizikos įtaką kitoje rinkoje.

Kai kainos pradėjo didėti, treideriai nusileido į minusą. Taip, jie turi užtikrinimą. Jie buvo pasiruošę didėjimui, kainos gali kristi arba didėti (svarbiausiai – palaukti kol baigsis didėjimo momentas). Bet kai didėjimas tampa beprotišku, finansinis treiderių užtikrinimas išsenka. Viso to rezultate bankų struktūros, per kurias vyksta tie kontraktai, privalo uždaryti poziciją ir išpirkti fjučerius. Dėl to kainos dar smarkiau didėja, kadangi fjučerio kontraktą reikia kažkur tai įsigyti – didėja paklausa. Vyksta taip vadinamas trumpas suspaudimas (short squeeze).

Kai visos fjučerių pozicijos yra uždarytos, rinka nurimsta. Labai didelė tikimybė, jog būtent tai ir atsitiko Europos dujų rinkoje.

Štai ir atsitiko sąlyginis kainų normalizavimas. Nors jos, suprantama, dar toli nuo normalių.

- Paskutiniu metu aptariama versija, jog pas Rusiją elementariai gali nebūti atliekamų dujų apimčių eksportui į Europą. Kažką tai galima prapumpuoti per „Šiaurinį srautą – 2“, jį paleidus. Bet tas „kažką“ nebūtinai atitiks europiečių lūkesčiams. Gal būt, mes kiek tai perdėtai vertiname „Šiaurinio srauto – 2“ reikšmę.

- Tai pagrista pastaba. Principe, viskas priklauso nuo to, koks mūsų požiūris į situaciją.

Pastaruoju metu, kai dujų kainos didėjo (liepos – rugpjūčio mėnesiais jos buvo kažkur tai apie 500 dolerių už tūkstantį kubinių metrų), „Gazpromas“ nedidino eksporto apimčių. Kainos priimtinos, kontraktai vykdomi, viskas tvarkoje.

Galima buvo spėti, jog tai koks tai bandymas paveikti Europą –įtikinti ją kuo sparčiau paleisti „Šiaurinį srautą – 2“.

Dar kartą pažymėsiu: „Gazpromui“ tai nenaudinga. Per daug aukštos kainos sukelia nereikalingą įtampą, veda link paklausos degradavimo, stimuliuoja alternatyvių energijos šaltinių paiešką ir t.t. Rusija kaltinama nepagristomis manipuliacijomis.

Bet ar pas „Gazpromą“ buvo galimybė padidinti eksportą į Europą? Keletas publikacijų autoritetinguose leidiniuose nurodė, jog tokios galimybės nebuvo. Naujojo šildymo sezono išvakarėse Rusijai reikėjo užpildyti nuosavas požemines dujų saugyklas.

Paprasčiausiai mes esame pripratę, jog pas „Gazpromą“ visada yra daug atliekamo kuro.

Be to, pastarieji metai „Gazpromui“ buvo sunkūs. 2020-ieji – tai iš viso atskira istorija, bet ir 2019 metais vidutinė Europos rinkos biržos dujų kaina sudarė tik 160 dolerių už tūkstantį kubinių metrų. Suprantama, esant tokioms sąlygoms kompanija priversta taupyti ir be reikalo ne investuoti.

Bet kokiu atveju, „Šiaurinio srauto – 2“ paleidimas – tai ne greita istorija. Turi būti atliktos tam tikros techninės procedūros, o jos reikalauja laiko (ne vieną ir ne dvi dienas).

Nors šiandieną galima tiekti Ukrainos maršrutu, bet tai nevyksta. Gal būt reikalas geografijoje. Suprantama, pas mus nėra viso vaizdo. Ukrainos „atšaka“ – tai viena istorija, šiaurinė „atšaka“ – kita.

Galimai, iš telkinių, kurie orientuoti į šiaurinį maršrutą, paprasčiau padidinti tiekimo apimtis. Bet tai jau spekuliavimas.

Neseniai Rusijos energetikos ministras Aleksandr Novak pareiškė, jog kai tik „Gazpromas“ užpildys savo požemines saugyklas, jis galės vėl pardavinėti dujas Europoje pagal sandorius (spot contract).

Pažiūrėsim.

- Pasitarimo su prezidentu metu tas pats Novak pasiūlė tiekti papildomas dujų apimtis prekybai Sankt-Peterburgo biržoje, o Putinas jo idėją palaikė. Mažai kas į tai atkreipė dėmesį. Kodėl būtent Sankt-Peterburgo birža?

- Labai teisingas klausimas. Iš tikrųjų, yra Sankt-Peterburgo birža, ir yra „Gazpromo“ elektroninės prekybos platforma (EPT), per kurią rusiškos dujos parduodamos užsienyje iš pristatymo taško. Tai beveik birža. Nors ten tik vienas pardavėjas – „Gazpromas“.

Sankt-Peterburgo tarptautinėje prekių-žaliavų biržoje dujos parduodamos vidaus rinkai. Apie ką buvo kalbama pasitarime pas Putiną, iki galo neaišku, nors čia detalės didelės reikšmės neturi.

Ir bendrai paėmus, geras dalykas turėti savo mazgą (habą) ir savo biržą. Europoje to siekia daugelis šalių. Tai kodėl gi Rusija ir „Gazpromas“ turi vystyti svetimas struktūras? Norite daugiau dujų – pirkite jas mūsų prekybos aikštelėse.

Užuomina buvo būtent tokia.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 4 — id: `scraped:rubaltic_lt:078f0ffc58047807`

**Title:** Kalbėsim tik su JAV: Rusija nutraukė santykius su NATO

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Rusija stabdo savo pastovaus atstovo prie NATO veiklą. Iš Maskvos pusės šis žingsnis reiškia šiuolaikinio diplomatinio korektiškumo atsisakymą. NATO nėra pilnavertė tarptautinė organizacija – tai tik instrumentas JAV rankose. Su amerikiečiais Rusija ir kalbės ir dėl NATO, ir dėl, tokių NATO narių, kaip Pabaltijo respublikos, dėl kurių Maskvos ir Šiaurės Atlanto aljanso dialogas anksčiau skaitėsi ypatingai vertingu.

Mėnesio pradžioje NATO sekretoriatas paskelbė apie aštuonių Rusijos diplomatų išsiuntimą iš savo buveinės ir dar dviejų vietų sumažinimą Rusijos diplomatinėje misijoje. Pažymėtina, jog šis sprendimas Rusijoje buvo beveik nepastebėtas. Diplomatų išsiuntimas jau tapo nusistovėjusia praktika, prie to visi priprato, šie išsiuntimai buvo be jokių padarinių, neskaitant atsakomojo diplomatų išsiuntimo kita šalimi.

Tuo įdomesnė šiurkšti ir akivaizdžiai neproporcionali Maskvos reakcija.

„Atsakydami į NATO veiksmus mes sustabdome savo pastovios atstovybės prie NATO veiklą, tame tarpe ir vyriausiojo karinio atstovo, tikriausiai, nuo lapkričio mėnesio 1 dienos arba, gal būt, tam prireiks dar keletą dienų“,- spalio mėnesio 18 dieną pareiškė Rusijos užsienio reikalų ministras Sergėj Lavrov.

Be karinės misijos, taip pat nutraukiama Rusijos informacinio biuro Monse (NATO buveinė Briuselio priemiestyje) veikla. Iš esmės Monse palieka visi oficialios Maskvos įgalioti atstovai. Sergėj Lavrov pabrėžė šią aplinkybę ypatingai, nurodydamas į tai, jog jei Šiaurės Atlando aljanso buveinės darbuotojams reikia skubiai susisiekti su Maskva, tai jie gali kreiptis į RF ambasadorių Belgijoje.

Paskutiniu metu šiuo klausimu Rusijos valdžia yra nuosekli. Prieš keletą mėnesių Maskva faktiškai atsisakė pripažinti Europos Parlamentą, uždraudusi šios, pavirtusios į gigantišką antirusišką plepalynę, organizacijos pirmininkui įvažiuoti į RF.

Sekantis logiškas žingsnis – atsisakymas pripažinti Europos Sąjungą ir sutikimas turėti reikalą tik su jos nariais – šalimis: Vokietija, Prancūzija, Lenkija ir kitomis. Juk pastarosios taip pat nepripažįsta EAzES ir pažymi, jog turės reikalą tik su Kazachstanu, Armėnija ir kitais jos nariais – šalimis.

Kas liečia NATO, tai čia Rusijos URM sprendimas ne toks jau ir šiurkštus, jei jį vertinti dinamikos požiūriu.

Po šaltojo karo postsovietinė Rusija sutiko vertinti NATO kaip derybų šalį ir tarptautinį partnerį, atidarydama savo diplomatinę misiją prie Aljanso buveinės. Ji įsijungė į NATO ir NATO partnerių-šalių Euroatlantinės partnerystės tarybą. „Partnerystė taikos labui“ programos rėmuose dalyvavo taikdarystės operacijose. Įkūrė tarybą „Rusija – NATO“, kurios pagrindinis pasiekimas (NATO, o ne Rusijai) tapo Aljanso tranzitinės bazės greta Uljanovsko organizavimas karinių pajėgų permetimui į Afganistaną.

Visas šis kursas stiprino organizacijos, sukurtos kaip šaltojo karo instrumentas, pozicijas ir legitimaciją, po šaltojo karo pabaigos tapo vienu iš pagrindinių JAV, pasiskelbusiu save šio karo laimėtoja, globalinio dominavimo instrumentų.

Kitos NATO gyvavimo esmės, kaip vasalų subūrimas prie Vašingtono po TSRS sugriuvimo, nebeliko. O kad blokinė disciplina būtų tvirta, vasalams reikalingas bendras visus apjungiantis priešas. Tokiu priešu Europos šalims – Aljanso nariams gali būti tik Rusija.

Prie to kuo toliau vystėsi NATO ir Rusijos santykiai, tuo priešiškesnis Rusijai darėsi NATO.

Nuo šios tendencijos supratimo prasidėjo atgalinis santykių procesas. Jos starto tašku galima vertinti Vladimiro Putino 2007 metų „Miuncheno kalbą“, kai Rusijos prezidentas pavadino nepagrista vienapolią pasaulio tvarką, vadovaujama JAV ir NATO, kaip vienu iš jos institutų.

Tolimesnių metų laikotarpiu buvo sustabdytos visos bendros programos, nutraukta tarybos „Rusija – NATO“ veikla ir baigtas politinis dialogas. Per septynerius metus Rusijos misija prie NATO sumažėjo nuo 70 iki 10 žmonių, prie to RF paskutinių trejų metų laikotarpiu neturėjo savo atstovybės Monse vadovo.

Dabar šioje daugiametėje santykių degradacijos istorijoje padėtas finalinis taškas. Maskva išsilaisvino nuo nereikalingo diplomatinio korektiškumo.

Tarp kitko, ir kalba, ir tai jai gerai gaunasi, ką parodė Putino ir Baideno derybos Ženevoje, o taip pat neseniai įvykęs JAV valstybės sekretoriaus pavaduotojos Viktorija Nuland vizitas į Maskvą.

Kas liečia tai, jog NATO sudėtyje randasi Lenkija ir Pabaltijo šalys, kurių militarizacija ant pat Rusijos sienos sukelia Maskvos susirūpinimą, tai dėl šių klausimų Rusija kalbėsis ne su NATO ir netgi ne su tomis pačiomis šalimis, o su Jungtinėmis Valstijomis.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 5 — id: `scraped:rubaltic_lt:8f8b6d0fa95383ed`

**Title:** Šaltis ne brolis: Lietuva ir Lenkija pereina ant medienos kuro iš Baltarusijos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Šiais metais Baltarusija ES šalims pardavė rekordinį medžio granulių partijų kiekį. Apie tai liudija Baltarusijos universalios prekių biržos (BUPB) duomenys. Kuro granulių, kurias pagamino „paskutinė Europos diktatūra“, pirkėjų sąraše Lenkijos ir Lietuvos kompanijos. Likimo ironija, būtent šios šalys lobijuoja naujų ekonominių sankcijų paketų Lukašenkos režimui įvedimą, kurios gali paliesti Baltarusijos medžio apdirbimo pramonę.

Rekordinis dujų pabrangimas verčia Europos vartotojus ieškoti alternatyvius energijos šaltinius. Tai iššaukė akmens anglies paklausą, nuo kurios ES stengėsi kuo greičiau atsakyti savo „žaliojo sandorio“ realizavimo rėmuose. Energetinės krizės naudos gavėjų tarpe taip pat atsidūrė biologinio kuro gamintojai.

Šiandienй ši šaka Baltarusijoje vystosi aktyviai – per praėjusius metus miško produkcijos eksportas jai davė 180 milijonų dolerių. Ir yra pagrindo manyti, jog medienos kuro eksportas augs.

Baltarusijos Valstybės kontrolės komiteto vadovo Leonido Anfimovo nuomone, vienas iš perspektyviausių šalies eksporto produktu yra medžio granulės.

Nenuostabu, jog eilinio šildymo sezono išvakarėse biologinio kuro gamintojai gavo galimybę maksimaliai padidinti savo pelną.

„Staigiai išaugęs pirkėjų iš Europos interesas baltarusiškoms medžio granulėms, visų pirma susijęs su šildymo sezono pradžia, o atsižvelgiant į rekordiškai aukštas gamtinių dujų kainas, žymiai padidėjo alternatyvių kuro rūšių paklausa. Dėl to viso per šių metų 9 mėnesius mes jau viršijome pardavimų eksportui rodiklį už 2020 metus“, - praneša BUPB.

Biržos atstovai atskirai paminėjo apie kažkokį „stambų Danijos holdingą, kuris specializuojasi biologinio kuro tiekime į Europos Sąjungą“. Danija – vienas iš žaliosios energetikos pasaulio lyderių, bendradarbiavimas su ja Baltarusijai leidžia tikėtis medžio granulių eksporto didėjimo.

Bet sudaryti sandorius su BUPB, kaip rodo praktika, siekia netgi Lietuvos ir Lenkijos kompanijos. Baltarusijos skiedros jas domina nuo seno.

„Tačiau jei dėl pastarųjų savaičių įvykių Baltarusijoje importas bus apribotas, Lietuvoje ir dalinai Latvijoje galimybės užsitikrinti reikiamą aukštesnės kokybės skiedrų kiekį biokurui išliks gan ribotos“, – pažymi Vaidotas Jonutis, tarptautinės biržos „Baltpool“ prekybos skyriaus vadovas.

Bet vėliau pats Minskas nusprendė miško medžiagą ir medžio apdirbimo produkciją apmokestinti išvežamaisiais muitais (atitinkamas įsakas paskelbtas Baltarusijos prezidento svetainėje).

„ Pas mus kiekvienais metais eksportuojamas pakankamai didelis skiedrų kiekis – milijonai kubų. Mes jau priartėjome prie sprendimo įvesti netgi skiedrų išvežimo, iš esmės, užtveriamuosius muitus“,- sakė Baltarusijos miško ūkio ministras Vitalijus Droža.

Akivaizdu, apribojus eksportą, „Batka“ pabandys išspręsti dvejus pagrindinius uždavinius – stimuliuoti biologinio kuro vartojimą pačioje Baltarusijoje ir padidinti medienos produkcijos eksportą su aukštesniu pridėtinės vertės mokesčiu.

Bet baltarusiškų skiedrų importuotojams nėra ko jaudintis. „Metų metais organizuojant eksportinius aukcionus biržoje jau susidarė pastovių šios produkcijos pirkėjų grupė. Daugiausiai tai kompanijos iš Latvijos, Lietuvos, Lenkijos ir Estijos. Mažėjant skiedrų eksportui, greičiausiai, būtent šios šalys taps pagrindine tėvyninių medžio granulių realizacijos rinka. Medienos produkcijos rinka yra labai dinamiška, ir, kaip taisyklė, greitai prisitaiko prie naujų sąlygų“, - praneša BUPB spaudos tarnyba.

Vitalijaus Droži žodžiais tariant, Baltarusijos miško ūkis jau gavo maksimalų pelną iš medienos kuro eksporto.

Apie kokias sumas kalbama, ministras nepatikslina. Ir teisingai daro. Informacijos apie komercinius sandorius pagarsinimas neduos naudos sandorių dalyviams.

Latvijoje jau buvo bandyta apriboti baltarusiškų skiedrų importą. Vietiniai miško pramoninkai asmeniškai skundėsi ministrui pirmininkui Krišjansui Karinšiui: esą, importinio kuro vartojimas prieštarauja pareikštiems „Apie energetiką“ tikslams.

„ Latvijos ekonomikai yra kenksmingas vietinių gamintojų neparėmimas. Ir toks stambiausias skiedrų pirkėjas, kaip AB „Rigas siltums“, kurio pusė akcijų priklauso valstybei, jokiu būdu neremia vietinių gamintojų! 2018 metų skiedrų tiekimo konkurse „Rigas siltums“ nugalėjo komersantas, kuris prekiauja tik baltarusiška žaliava“, - savo kreipimesi sako Latvijos ministras pirmininkas

Paminėtą kompaniją netgi kaltino radioaktyviomis skiedromis iš Mogiliovo ir Gomelio – tų rajonų, kurie nukentėjo nuo Černobylio AE avarijos. „Rigas siltums“ būk tai žinojo, jog šilumines energijos gaminimui vartoja užterštą kurą, ir tai darė dvejus metus. Kuo ne argumentas uždrausti skiedrų importą iš Baltarusijos, išvalant lauką alternatyviems tiekėjams.

Galų gale situaciją išsprendė: „Rigas siltums“ valdybos narys Raivis Elinš pareiškė, jog importuojami kroviniai bus tikrinami dozimetrais.

Paskutiniai BUPB duomenys nėra sensacingi. Kalbama apie paprastus komercinius sandorius, kurie nepažeidžia nei europietiškų sankcijų režimo, nei šalių - biologinio kuro importuotojų nacionalinių įstatymų. Tuo jie ir parodomieji: atskiruose sferose, kur politika ne viršauja virš ekonomikos, Baltarusija sėkmingai prekiauja su savo kaimynais.

Ir netgi didina eksporto apimtis.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 6 — id: `scraped:rubaltic_lt:1d7302715929d351`

**Title:** Lietuva pristabdo geležinkelio modernizaciją dėl sankcijų Baltarusijai

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvoje pristabdomas pagrindinės geležinkelio linijos šalies vakaruose ruožo rekonstravimo projektas, kainuojantis 56,5 milijono eurų. Apie tai pranešė „Lietuvos geležinkelių“ (LG) dukterinės įmonės LTG Infra spaudos tarnyba. Peržiūrėti savo planus Vilniui prisiėjo dėl sankcijų Baltarusijai, kurios artimiausiu metu gali išprovokuoti tranzito krizę Pabaltijo respublikoje. Esant tokiom sąlygom Lietuva yra priversta veikti taip pat, kaip ir kaimyninė Latvija – stabdyti anksčiau pradėtus investavimo projektus.

Šiandieną galima jau tvirtai pasakyti, jog JAV ir ES sankcijos Baltarusijai visgi suveikė. Bet ne prieš Baltarusiją, o prieš Lietuvą: LG sustabdė pagrindinės šalies geležinkelio linijos ruožo Plungė – Šateikiai modernizavimą.

Projektas buvo pradėtas 2019 metais, rangovų konkursą laimėjo kelių tiesimo ir tiltų statybos bendrovė „Kauno tiltai“. Gavę vyriausybės ir komisijos, tikrinančios strateginės kompanijos sandorius, leidimą, „Lietuvos geležinkeliai“ pasirašė su ja 56,5 milijono eurų vertės kontraktą.

Už šiuos pinigus „Kauno tiltai“ turėjo rekonstruoti 13,9 kilometro geležinkelio sankasos, nutiesti tokio pat ilgio naują kelią, atnaujinti tiltus ir pralaidas, rekonstruoti geležinkelio iešmus ir pervažas, modernizuoti pačias Plungės ir Šateikių geležinkelio stotis.

Visą tai atlikus, šiame ruože keleivinių traukinių leidžiamas greitis išaugtu nuo 120 iki 160 kilometrų per valandą, o krovininių – no 90 iki 120 kilometrų per valandą.

„Vienas svarbiausių šio projekto tikslų yra užtikrinti strateginio IXB koridoriaus, kuris jungia sostinę Vilnių su pagrindiniu Lietuvos krovinių ir logistikos centru Klaipėdos jūrų uostu, ruožo pralaidumą ir greičio didinimą“, – pranešime sakė „LTG Infra vadovas Karolis Sankovskis.

Štai ką pareiškia tas pats Sankovskis: „Geopolitinė situacija dėl Europos Sąjungos ir JAV taikomų sankcijų Baltarusijai verčia peržiūrėti kai kurių projektų investicinę grąžą“.

Iš pirmo žvilgsnio jo žodžiai gali pasirodyti keistais. Kol kas vienintelis tranzito krovinys iš Baltarusijos, kurio neteko Lietuva – tai naftos produktai. Viskas kas liko, eksportuojama per Klaipėdos uostą, o kai kurios krovinių apyvartos pozicijos netgi auga. Tai patvirtinama LG finansine ataskaita: per 2021 metų pirmuosius šešis mėnesius piniginės įplaukos sumažėjo tik 0,4 procento (nuo 206,1 iki 205,3 milijono eurų). LTG Cargo krovinių vežimas sumažėjo 1 procentu, LTG Infra pelnas – 2 procentais. Sumažėjimas nėra visiškai kritiškas, jei iš viso tai galima pavadinti sumažėjimu.

JAV finansų ministerija, kaip ir tokiais atvejais dera, išdavė generalinę sandorių, kurių dalyvis yra Baltarusijos gigantas (arba kompanija, kuriai priklauso ne mažiau 50 procentų akcijų), sustabdymo licenziją. Licenzijos galiojimo terminas baigiasi gruodžio mėnesį.

Lietuva galėtu ignoruoti šį dokumentą, kadangi Jungtinių Valstijų sankcijos liečia tik Amerikos fizinius ir juridinius asmenis. Bet, kad išvengti nesklandumų, Pabaltijo respublika nusprendė taip pat nutraukti kontraktą su „Belaruskalij“ . Lietuvos transporto ministras Marius Skuodis prognozuoja, jog gruodžio mėnesį iš viso bus nutrauktas visas baltarusių produkcijos eksporto tranzitas per Klaipėdos uostą.

Geležinkelininkai, suprantama, visą tai priėmė savo žinai. „Panašu, artėja momentas, kai tiekimas bus sustabdytas, o tai reiškia, jog mes prarasime apie 60 milijonų eurų metinių pajamų, o visa Lietuvos logistikos grandinėlė negaus daugiau nei 100 milijonų eurų pajamų“,- sakė LG generalinis direktorius Mantas Bartuška.

Valstybės subsidijas, reikalingas infrastruktūros palaikymui, jis įvertino 60 milijonų eurų. Jei „Lietuvos geležinkeliai“ negaus tų pinigų, jiems teks pakelti krovinių ir keleivių vežimo tarifus.

Antrasis variantas regisi yra realesnis.

Visų pirma, valstybės iždas neišlaikys nenumatytų 60 milijonų eurų dydžio išlaidų (LG poreikių patenkinimui teks arba sumažinti kitus biudžeto išlaidų straipsnius, arba skolintis).

Apie tai rugsėjo mėnesio pabaigoje pareiškė Lietuvos ekonomikos ir inovacijų ministrė Aušrinė Armonaitė: „Sakysiu tiesiai: negali būti ir kalbos apie jokias subsidijas. Mes suprantame, jog yra sunkumai, bet tikimės, jog jie laikini“.

Kitaip sakant, su neapgalvotos Lietuvos politikos padariniais prisieis tvarkytis patiems uostininkams ir geležinkelininkams. Jie žinojo su kuo susideda, kai vedė reikalus su „autokratine valstybe“. LG išgirdo Armonaitės žodžius. Kompanija nusprendė stabdyti geležinkelio ruožo Plungė – Šateikiai rekonstrukcijos investavimą, suprasdami, jog „skęstančiųjų gelbėjimas yra jų pačių reikalas“.

Kaimynai latviai patvirtins: anksčiau jie taip pat buvo pasirengę modernizuoti geležinkelį, o dabar jį parduoda aukcionuose.

Tarp kitko, Lietuvoje situacija vystosi pagal žinomą scenarijų. Praeitais metais Latvijos kompanija Latvijas dzelzceļš (LDz) nusprendė stabdyti geležinkelio elektrifikavimą. Šiam projektui jau buvo išskirta šimtai milijonų eurų iš ES susibūrimo fondo, bet išskyrė tada, kada LDz ruošėsi kasmet apdoroti 45-55 milijonus tonų krovinių. Netekus rusiško tranzito, tie planai tapo atvirai nerealūs, o elektrifikacijos projektas – beprasmiškas.

Skirtumas tarp Lietuvos ir Latvijos geležinkelininkų tik tame, jog pastarieji peržiūrėjo savo investicijų planus jau pačiame krizės įkarštyje. Iki to jie ignoravo rusiškų krovinių perorientavimo į Leningrado srities uostus grėsmę.

Ir teisingai daro! Naujų krovinių siuntėjų, kurie galėtų kompensuoti baltarusiško tranzito netekimą, LG vis vien nesuras. Vienintelis smūgio sušvelninimo būdas – sumažinti savo nuosavas išlaidas.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 7 — id: `scraped:rubaltic_lt:9d6cff2d812d0a8d`

**Title:** Antausis Lietuvai: JAV pradėjo atšaukti sankcijas Rusijai

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Rusijoje randasi oficiali Amerikos delegacija, vadovaujama JAV valstybės sekretoriaus pavaduotojos Viktorijos Nuland. Tam, kad amerikiečių vizitas į Maskvą įvyktų, Vašingtonas iš sankcijų sąrašo išbraukė dalį rusų. Tuo pačiu amerikiečiai nesąmoningai skėlė diplomatinį antausį savo patiems ištikimiausiems sąjungininkams Rytų Europoje, kurie jau aštuntus metus kartoja: jokio sankcijų Rusijai atšaukimo iki „išėjimo iš Donbaso“ ir „Krymo gražinimo“.

Apie tai, kad dėl derybų Maskvoje amerikiečiai sušvelnino sankcijų režimą, papasakojo Rusijos URM oficiali atstovė Marija Zacharova. Reikalas tame, kad Viktorijai Nuland norėjosi ne neutralioje teritorijoje, o būtent Maskvoje, pravesti derybas pačiais opiausiais Rusijos-Amerikos santykių klausimais, bet tai padaryti buvo neįmanoma, kadangi valstybės sekretoriaus pavaduotoja ir daugelis jos bendradarbių patys buvo Rusijos „juodajame sąraše“.

„Ji iš tikrųjų buvo sankcijų sąraše, o tai numato, jog žmogus negali kirsti sieną. Jie įtraukė Rusijos atstovus, tarptautininkus į savo sankcijų sąrašus. Todėl šiuo atveju klausimas buvo išspręstas remiantis pariteto pagrindu“, - apie Viktoriją Nuland pasakė Marija Zacharova.

Kitaip sakant, konfliktas buvo išspręstas remiantis mainų principu. Vašingtonas iš savo „stop-lapų“ išbraukė keletą Rusijos piliečių, kuriems buvo uždraustas įvažiavimas į JAV, Maskva iš savo „stop-lapų“ išbraukė tuos Amerikos delegacijos narius, kuriems buvo uždraustas įvažiavimas į Rusiją.

Rusijoje.

Ukrainoje, Lenkijoje arba Baltijos šalyse šis sprendimas turi būti įvertintas taip pat kaip ir Džozefo Baideno sutikimas dujotiekio „Šiaurinis srautas – 2“ statybai, Barako Obamos atsisakymas dislokuoti priešraketinės gynybos objektus greta Rusijos sienų ir kitos, ilgai besitęsiančios amerikiečių išdavysčių savo ištikimų JAV sąjungininkų Rytų Europoje chronologijos, istorijos.

Jokio sankcijų švelninimo iki tol, kol Kremlius „ne pakeis savo elgesio“ – ne „išeis iš Donbaso“ ir ne „gražins Krymo“ Šią dogmą kartojo septynerius metus, o dabar JAV atšaukia sankcijas, nors klastingas Kremlius iš niekur neišėjo, už nieką ne užmokėjo ir dėl nieko neatgailavo.

Prieš keletą metų „sanitarinio kordono“ šalys jau piktinosi Vokietijos elgesiu, kai į „Normandijos ketvertuko“ posėdį Berlyne buvo įleistas RF prezidento padėjėjas Vladislovas Surkovas, kuris buvo Europos Sąjungos „juodosiose sąrašuose“. Bet tada už principų atsisakymą Vokietiją buvo galima apskųsti „vyresniajam“, o ką daryti, kai sankcijų režimą pažeidžia pats „vyresnysis“?

Pastaraisiais mėnesiais visas Vašingtono dėmesys nukreiptas į Kiniją. Ruošiantis ryžtingoms grumtynėms už globalinio lyderio vardą su pagrindiniu konkurentu, JAV kuria naujas ir aktyvuoja senas karines-politines sąjungas Ramiojo vandenyno regione, nesigėdydama meta regioninius sąjungininkus ir išeina iš jais okupuotų šalių, ir vis mažiau dėmesio skiria Europai ir NATO.

Kam tokiame kontekste Baltiesiems rūmams reikalinga Rusija? Maksimaliai tam, kad išvengti pilnavertės karinės-politinės jos sąjungos su Kinija, kuri padarys Padangių šalį „neužmušama“ šalimi. Nerangi paskutiniųjų metų Vašingtono politika atvedė labai arti prie tokios sąjungos formavimo.

Minimaliai, Amerika turi būti garantuota, jog lemiamo susidūrimo su Pekinu momentu Maskva neatvers jai „antrąjį frontą“. Toje pačioje Europoje, pavyzdžiui.

Todėl su Rusija būtina suderinti „raudonas linijas“. Plūdurus, už kurių abi šalys įsipareigoja neužplaukti. Susitarti, kokiu būdu valdyti konfrontaciją.

Visų pirma, tai liečia Ukrainą, bet taip pat ir Baltarusiją, Nato „pafrontės valstybes“ palei sieną su Rusija ir jų forsuotą militarizavimą.

Ir Rusijai naudinga nesilaikyti politeso, o tik jį vaizduoti. Kadangi diplomatinis požiūris į Ukrainą, kaip į formaliai suvereninę ir nepriklausomą valstybę, susilpnins jos pozicijas derybose su amerikiečiais.

Todėl, pavyzdžiui, RF Saugumo tarybos pirmininko pavaduotojas Dmitrijus Medvedevas pasveikino Viktoriją Nuland straipsniu „Kodėl beprasmiški kontaktai su dabartine Ukrainos vadovybe“. Buvęs Rusijos prezidentas į šį klausimą atsako Leonido Gaidajaus komedijos personažo stiliuje: mes kalbėsimės su piemeniu, o ne su besmegeniais avinais!

Ir amerikiečiai sutinka tokiam pokalbiui. Jis jiems taip reikalingas, jog ir sankcijos, ir solidarumas, ir Ukraina, ir NATO sąjungininkai Baltijoje šonan.

Sankcijos, štai, jau aukojamos …

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 8 — id: `scraped:rubaltic_lt:14c7b2eaf2506433`

**Title:** Lietuva pralaimėjo „maisto prekių karą“ Rusijai

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Per aštuonerius 2021 metų mėnesius Latvija 48 procentais padidino agropramonės produkcijos užpirkimus Rusijoje. Apie tai liudija nauji „Agroeksport“ (RF Žemės ūkio ministerijos APK produkcijos federalinio eksporto plėtros centro) duomenys. Tokie, nedžiuginantys Pabaltijo, „maisto prekių karo“, kuris eina nuo 2014 metų, su Rusija, rezultatai. Rusija ne tik susidorojo su importuojamu APK prekių pakeitimu savos gamybos prekėmis, bet dar ir sugebėjo užkariauti naujas realizavimo rinkas nedraugiškose Europos Sąjungos šalyse. Latvijos ir Lietuvos žemės ūkis tuo pasigirti negali.

„Sausio – rugpjūčio mėnesiais Rusija eksportavo į Latviją 420 tūkstančių tonų kviečių (6 kartus daugiau nei 2020 metais) už 102 milijonus dolerių (7 kartus daugiau), kukurūzų – 107 tūkstančius tonų (4 kartus daugiau) už 24 milijonus dolerių (6 kartus daugiau)“, - praneša „Agroeksporto“ spaudos tarnyba.

Be to, Latvija tapo viena iš stambiausiu rusišku saulėgrąžų išspaudų pirkėja (317 tūkstančių tonų) ir runkelių išspaudų (195 tūkstančiai tonų). Lyginant su analogišku praeitų metų laikotarpiu, maisto prekių importą iš Rusijos ji padidino 48 procentais.

Šias skaičiais galima apibendrinti sankcijų karo, kurį Europa bendrai (ir Latvija konkrečiai) prieš 7 metus paskelbė Maskvai, rezultatą. Kaip atsakomąją priemonę Vladimiras Putinas įvedė atskiroms prekių grupėms iš ES šalių embargo maisto prekėms. Šis įsakas rimtai įtakojo Rusijos agrarinės pramonės vystymuisi.

Eilėje krypčių Rusija, paprasčiausiai, persiorientavo į alternatyvius tiekėjus. Pavyzdžiui, jūros produktus iš Norvegijos ir Islandijos, pakeitė analogiškos prekės iš Indijos ir Vietnamo.

„Dėl klimato sąlygų mes negalime pakeisti visus importuojamus vaisius ir daržoves“, - sakė agentūros Agro and Food Communications administruojantis partneris Ilja Berezniuk.

2018 metams ji pasiekė 99 procentus jai būtinos grūdų lygio gamybos, 93 procentus mėsos ir mėsos produktų, 95 procentus cukraus, 84 procentus pieno. APK eksporto pajamos taip žymiai išaugo. Teigiamai Rusijos gamintojus paveikė koronaviruso pandemija: krizės fone daugelis šalių didino maisto prekių užpirkimo apimtis, o Rusija operatyviai tenkino jų poreikius. Išaugo beveik visos tiekimo į užsienį pozicijos: grūdai, mėsa, cukrus, pienas ir t.t.

Pirmą kartą postsovietinėje Rusijos istorijoje Rusija tapo maisto prekių netto – eksportuotoju: eksportuodama ji uždirbo daugiau, nei išleido importui.

Suprato ne šiandieną ir ne vakar. Staigus rusiškos žemės ūkio produkcijos eksporto ūgtelėjimas į Pabaltijo respubliką buvo stebimas 2018 metais. Tada Latvija įsiveržė į pagrindinių neapkenčiamų „putiniškų“ grūdų importuotojų trejetuką. Priekyje buvo tik Egiptas ir Turkija.

Latvijos žemdirbiai, priešingai, dideliais pasiekimais pasigirti negali. Vakaruose jų produkcija neturi paklausos, o surasti pakaitalą Rusijos rinkai pasirodė problematišku. Putino embargo maisto prekėms Latvijai atsiliepė šimtais milijonų eurų nuostolių.

„Mes eksportuojame pieną į 20 naujų šalių, žuvies produktus – į dar didesnį kiekį. Jei pas mus būtų bankrotai, tai jūs apie tai išgirstumėte, Bet, tos apimtys, kurios buvo eksportuojamos į Rusiją, niekur neparduodamos. Nei Kiniją, nei Amerika tokių mūsų produktų apimčių neperka“. –prisipažino Latvijos žemės ūkio ministras Janis Duklavs.

Jo žodžius patvirtina žuvies konservų įmonės „Gamma-A“ valdybos pirmininkas Aivars Lejietis: dėl vartojimo ypatybių Latvijos konservų gamintojams Vakaruose nėra ko veikti.

Ši problema yra aktuali ir Lietuvai. Vietinių fermerių problemomis rūpinosi asmeniškai prezidentas Gitanas Nausėda, kuris reikalavo iš Europos Sąjungos dotacijų padidinimo Baltijos šalių žemės ūkio produkcijos gamintojams.

Lietuvos eksministras pirmininkas Algirdas Butkevičius savo šalį pavadino labiausiai nukentėjusią nuo Maskvos kontr sankcijų. Dėl „pasikeitusios geopolitinės situacijos“ ir rusiško embargo maisto prekėms, vyriausybei prisiėjo peržiūrėti savo ilgalaikius planus.

„Mūsų vyriausybė nepaiso priešiškų Rusijos veiksmų ir pataikauja jai, perka ne tik trąšas, bet ir grikius bei kviečius, nors yra galimybė šiuos grūdus įsivežti iš Ukrainos ar kitų šalių“, - piktinasi Tėvynės sąjungos – Lietuvos Krikščionių demokratų (TS-LKD) partijos pirmininkas Kazys Starkevičius.

Galimybė žinoma, yra. Kaip ir galimybė eksportuoti į Ukrainą suskystintas gamtines dujas per Lietuvą ir Lenkiją. Tada kodėl „Nezaležnaja“, kaip ir anksčiau, pasiima sau rusišką kurą iš tranzitinio vamzdžio, naudodama „virtualinio reverso“ schemas? Todėl, jog tai paprasčiau ir pigiau.

Pas jį – rekordiniai derliai ir patys naudingiausi pasiūlymai. Bendradarbiauti su juo naudingiau, negu su alternatyviais tiekėjais iš draugiškų šalių.

„Lašų duonos“ kompanijos direktorius Nerijus Aukštuolis pasakoja, jog dėl to bendradarbiavimo lietuviai netgi sugalvojo įmantrią schemą: „Jūs turbūt žinote, kad rinką Europa apsaugo, yra muitai dideli, kruopom – 129 eurai, žaliavai – 37 eurai tonai, bet rado apėjimą verslininkai ir jas padaro ukrainietiškas, žodžiu iš Rusijos per Ukrainą eina be jokių muitų“.

Ir kiek dar „šalis agresorius“ užvertinės Pabaltijį savo grūdais? Galima netgi kreiptis pas „specialistus“, kurie paliudys, jog rusiški maisto produktai – patys kenksmingiausi pasaulyje. Ypatingai, jei juos ruošti naudojant „smirdančias“ rusiškas dujas...

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 9 — id: `scraped:rubaltic_lt:743e1719f34e4429`

**Title:** Putinas nustatė savo taisykles Europos dujų rinkoje

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Maskva yra suinteresuota pasaulio energetikos rinkos stabilizavimu ir pasiruošusi paremti Europą, bet vadovausis savo interesais. Apie tai darbinio pasitarimo metu pareiškė Rusijos prezidentas Vladimiras Putinas. Iš jo pasisakymo paaiškėja, jog „Gazpromas“ nesiruošia didinti ukrainietiško maršruto apkrovą – papildomas dujų apimtis europiečiai galės gauti „Šiauriniu srautu – 2“. O ilgalaikėje perspektyvoje europiečiams  prisieis pagalvoti apie savo santykių su Rusijos monopolija peržiūrėjimą, jei jie nenori naujų energetinių krizių.

Putinas galėjo abstrahuotis nuo situacijos Europos dujų rinkoje, bet nusprendė paremti europiečius ir pasisakyti. Būtent taip reikia suprasti jo pasisakymą pasitarime dėl energetikos plėtros klausimų.

Aukštos dujų kainos jau gąsdina net ir Rusijos vadovybę.

Tai įvyko parėjusiais metais, pačiame koronaviruso pandemijos įkarštyje – tada energijos resursų paklausa dėl karantino apribojimų stipriai krito. Biržoje dujomis buvo prekiaujama pigiau, negu pagal ilgalaikes sutartis. Prisiminkime Aleksandro Lukašenkos pasipiktinimą: Pergalės metinių metu baltarusiai rusiškas dujas pirko po 127 dolerius už tūkstantį kubų, o vokiečiai po 70 dolerių. Europoje tada pagalvojo, jog jie nutvėrė Dievą už barzdos. Disbalansas tarp pasiūlymo ir paklausos pastarojo naudai rodėsi ilgalaikiu trendu.

Būtent to ilgus metus siekė Briuselis. Kaip pastebi energetikos ekspertas Igor Juškov, europiečiai pas save kūrė „vartotojų rinką“. Rinką, kurioje tarp savęs turi konkuruoti įvairūs energijos resursų tiekėjai – „Gazpromas“, suskystintų gamtinių dujų (SGD) biržų brokeriai, „žaliosios“ elektros energijos gamintojai ir t.t.

SGD teikėjai nukeliavo į Azijos-Ramiojo vandenyno (ARV) regioną ir Pietų Ameriką, kur jų produkcijos kainos dar didesnės. „Vėjo energetika“ „nusėdo“ dėl oro sąlygų. Dujų gavyba Europos šalyse vis mažėja.

Pridėkim dar keletą faktorių: pasaulio ekonomikos atsistatymas, ekstremaliai šalta 2020-2021 metų žiema ir anomaliai karšta vasara, kas pareikalavo didelių elektros energijos apimčių kondicionieriams...

Tačiau, pernelyg aukštos „žydrojo kuro“ kainos jam nereikalingos.

Visų pirma, jos skaudžiai atsiliepia pramonės įmonėms, kurioms rusiškoji monopolija tiekia kurą, Antrą, Europoje tai stimuliuoja tolimesnę alternatyvių energijos šaltinių paiešką. Dujos netenka konkurentiškos prekės statuso.

„Pirkti jas tokiomis kainomis jau nebeįdomu, tai atsiliepia, tame tarpe, ir mūsų prekei. (...) Mes susiduriame su paklausos degradacijos situacija: iš visur ateina informacija, jog Europoje užsidaro gamyklos, pavyzdžiui,  trąšų gamyba. Nuskurdo gamtinių dujų tiekėjai galutiniams vartotojams“, - tvirtina „Gazprom-Eksport“ kontraktų ir kainodaros struktūrizavimo valdybos viršininkas Sergėj Komlev.

Tokius pat argumentus pasitarime su Putinu pagarsino Rusijos energetikos ministras Aleksand Novak: „Žinoma, dabar uždirba tos kompanijos, kurios yra dujų tiekėjos, bet fundamentaliai daugelis gamybų esant tokiomis sąlygomis, ypatingai dujų-chemijos įmonės, gali užsidaryti, kas jau ir vyksta, tai mes matome toje pačioje Didžiojoje Britanijoje, Europos bei kituose šalyse. Prie tokių kainų vyksta intensyvesnis perėjimas į atstatomuosius energijos šaltinius, ir, žinoma, kyla noras investuoti į mažiau efektyvius gavybos projektus. Todėl, suprantam, reikia kuo greičiai stabilizuoti rinką“.

Deklaruodamas pasiryžimą pagelbėti europiečiams spendžiant dujų krizę, Putinas sako gryną tiesą. Todėl, jog schema „vartotojų nuostoliai = tiekėjų pajamos“ jau nebeveikia.  Neadekvačios energijos resursų kainos kenkia visiems rinkos dalyviams.

Bet yra ir kita medalio pusė: Putino žodžiais tariant, numušti dujų paklausos ažiotažą Rusija pasirengusi, bet „tik nedarant sau žalos“. Šiame kontekste RF prezidentas paminėjo apie vidinius šalies poreikius rudens – žiemos periodui.

Tikriausiai „Gazpromo“ aruoduose, paprasčiausiai, nėra atliekamų 20 – 30 milijardų kubinių metrų kuro, kurį jis yra pasirengęs operatyviai eksportuoti. Kuklesnes papildomas apimtis Europa gali gauti tuo atveju, jei pradės veikti „Šiaurinis srautas – 2“.

Į klausimą, kodėl Rusija ne apkrauna Ukrainos dujų transporto sistemos, Putinas atsakė gana išsamiai. Realiai tranzitas didėja: per šių metų devynis mėnesius „Gazpromas“ perpildė savo kontraktinius įsipareigojimus Ukrainai  daugiau kaip 8 procentais. Tolimesnį didėjimą Kremliuje skaito netikslingu.

„Iš tikrųjų būtu galima padidinti tiekimą per Ukrainos dujų transporto sistemą, tik „Gazpromui“ tai nuostolinga. Kaip aš jau pasakiau, naudodamas naujas vamzdynų sistemas „Gazpromas“ taupo maždaug 3 milijardus dolerių per metus, turiu omenyje, jog tai šiuolaikinė pumpavimo įranga, nauji vamzdžiai, galima padidinti slėgį, ko negalima padaryti Ukrainos dujų transporto sistemoje, kadangi ji dešimtmečiais nebuvo remontuojama, ir ten bet kuriuo momentu gali kažkas tai pratrūkti, atsitikti. Ir tada iš viso kils nepalankios pasekmės visiems: ir tranzito šaliai, ir vartotojams“, - pažymėjo Putinas.

Pati sertifikavimo procedūra pagelbės kainų stabilizavimui biržoje. Tarp kitko, kalbama tik apie „pirmąją pagalbą“ Europos energetikos rinkai. Tam, kad  apsisaugoti nuo panašių krizių pasikartojimo, ES turi peržiūrėti savo santykių pobūdį su „Gazpromu“ .

„Mes kalbėjomės dar su Europos komisijos buvusią sudėtimi, ir visa jos veikla buvo nukreipta link, taip vadinamų, ilgalaikių kontraktų sumažinimo, buvo nukreipta link perėjimo prie prekybos dujomis biržoje. Pasirodo, o dabar tai tapo akivaizdu, jog tokia politika yra klaidinga – klaidinga todėl, kadangi neatsižvelgia į dujų rinkos specifiką, apibrėžiamą dideliu skaičiumi nenusakomų faktorių“, -kalbėjo Putinas.

Vakarų žurnalistai, politikai ir energetikos ekspertai neskuba paneigti Rusijos  prezidento žodžius. Bet tikriausiai jo ir nepasiklausys.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 10 — id: `scraped:rubaltic_lt:8aec3145d8c6feee`

**Title:** Kova su „Kremliaus propaganda“ sužlugdyta: Lietuva pasiliko Rusijos informaciniame lauke

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Apie 30 procentų lietuvių informaciją apie pasaulį semiasi rusiškoje žiniasklaidoje. Pasaulio paveikslą jiems formuoja „agresyvus kaimynas“. Tokia sociologija – kurtinantis Lietuvos valdžios, kuri dešimtmečiais naikino iš nacionalinės žiniasklaidos visą tai kas rusiška, pastangų žlugimas. Rusijos televizijos kanalų atjungimas, kovos su „Kremliaus propaganda“ kampanijos, draudimai rusų žurnalistams atvykti į Lietuvą – viskas veltui.

„Beveik pusė (48,7 procento) respondentų per paskutinį prieš apklausą mėnesį žiūrėjo, skaitė ar klausėsi užsienio žiniasklaidos. Dažniausiai buvo vartojami Rusijos žiniasklaidos šaltiniai, kuriais naudojosi 29,4 procento apklaustųjų“, - pateikia socialinės apklausos rezultatus Lietuvos nacionalinis televizijos kanalas LRT. Lietuvos kultūros ministerijos užsakymu apklausą atliko Rinkos tyrimų centras.

Pusė Lietuvos piliečių informaciją apie pasaulį semiasi iš užsienio šaltinių – tai jau daug ką pasako apie tai, kas yra Lietuva ir kokia piliečių nuomonė apie ją. Tačiau, Lietuvos valdžiai ši situacija nebūtu tokia baisi, jei lietuviai pirmenybę suteiktų amerikiečių, britų, vokiečių arba netgi lenkų žiniasklaidai. Lietuvos žurnalistai vis vien kartoja kolegas iš vakarų ir savo darbe remiasi jų metodikomis, lygiuodamiesi į gimtos šalies valdžią, kuri visus pasaulio įvykius vertina pagal JAV Valstybės departamento instrukcijas.

Informacinis Rusijos buvimas Lietuvoje – senas Lietuvos valdžios „bzikas“. Ji nejuokauja, kai specialių tarnybų ataskaitose Rusijos žurnalistus skelbia grėsme nacionaliniam saugumui. Valdantiems paranojikams tai iš tikrųjų taip ir yra.

Su Rusijos televizijos kanalais ir Interneto svetainėmis Lietuvoje susiejama „penktos kolonos“ formavimo grėsmė: didelių nelojalių gyventojų grupių, kurios krizės momentu gali surengti „ukrainietišką scenarijų“: pradėti maištauti prieš Lietuvą, paskelbti sąlyginę „Vilniaus liaudies respubliką“ ir paraginti Putiną įvesti kariuomenę.

Savitaiga tokia stipri, jog iš baimės Vilniuje yra pasiruošę netgi įsileisti Lenkiją į buvusiai ginčytinas teritorijas ir leisti jai skleisti informaciją Lietuvos lenkams. Kad tik tuo neužsiimtų Rusija.

„Kaip parodė tyrimas, po buvusios vyriausybės sprendimo retransliuoti lenkų televizijos kanalus Lietuvos pietryčiuose, pusė gyventojų jų nežiūri, o kai kurie teikia pirmenybę Rusijos televizijai“, - pavasarį buvo rašoma to pačio LRT svetainėje. – […] – Paklausus, kodėl jie nežiūri lenkų televizijos laidų, 39 procentai pietryčių Lietuvos gyventojų atsakė, jog renkasi rusiškus kanalus, 30 procentų pareiškė, jog žiūri lietuviškos televizijos laidas“.

Tarp kitko, Lietuvos lenkai – tai tik 6 procentai Lietuvos gyventojų. Rusai Lietuvoje sudaro 5 procentus visų gyventojų. Paskutinė apklausa rodo, jog rusišką žiniasklaidą skaito ir žiūri beveik kas trečias respublikos gyventojas. Tai yra, „agresyvaus kaimyno“ Interneto svetainės ir televizijos kanalai yra populiarūs ne tik tarp tautinių mažumų, bet ir tarp titulinės tautos atstovų.

Rusijos televizijos kanalų atjungimas (kaip tik pastarosiomis dienomis VGTRK laimėjo teisme su Lietuvos radijo ir televizijos komisija dėl „RTR –Planneta“ Lietuvoje blokavimo), Rusijos žurnalistų deportavimas iš Lietuvos, neleistinų įvažiavimui, kurių skaičius siekia šimtus, „juodieji sąrašai“, slaptas draudimas korespondentų punktams Lietuvoje – niekas nepagelbėjo. Lietuviai vis vien masiškai teikia pirmenybę rusiškai, o ne lietuviškai žiniasklaidai.

Ką tokioje situacijoje darys kovotojai už Lietuvos informacinį saugumą? Jų veiksmų algoritmas jau seniai atidirbtas. „Kremliaus propagandos“ temos aktualizavimas Lietuvoje. Biudžeto eiliniam „kontrpropagandiniam“ projektui kaulijimas iš Vakarų. Pageidautina, televizijos kanalas trejomis kalbomis: lietuvių, lenkų ir rusų.

Ir dar, būtiniausi kvalifikacijos kėlimo kursai Lietuvos žurnalistams Anglijoje arba Amerikoje. Eilinio tiriamosios žurnalistikos, faktų tikrinimo, žiniasklaidos priemonių naudojimo raštingumo centro įkūrimas ar dar kas tai tokio, skambančio taip įspūdingai. Kitaip sakant, dar vieno NKO, kuri pasiskelbs tiesa paskutinėje instancijoje ir, Lietuvos vyriausybės bei Džordžo Soroso lėšomis, aiškins lietuviams iš kokių žiniasklaidos šaltinių galima semti informaciją, o iš kokių – fu!

Visų tų „kontrpropagandinių“ pastangų efektą galima numatyti iš anksto. Kadangi čia viskas dešimtmečiais taip pat sukasi ratu.

Nieko nepasikeis.

Todėl kad lietuviška žiniasklaida – tai ir yra pati tikriausia propaganda. Siauraprotiška, buka, nepaslanki, sovietų stiliaus valstybinė propaganda. Apie įvykius Lietuvoje ir pasaulyje lietuviškas oficiozas pasisako užkeikimais, tarptautinės žurnalistikos ir politinės analitikos juose nėra iš viso kaip reiškinio. Visą tai pakeičiama mantrų apie transatlantinį solidarumą ir „tikėjimu į Amerika prie bet kokio prezidento“ rinkiniu.

Kai pasaulyje vyksta tai, kas nepatogu lietuviškai valdžiai, pavyzdžiui, tikėjimo į JAV visagalingumą kompromitavimą (tai vyksta vis dažniau ir dažniau), Lietuvos žiniasklaida dažniausiai į tai visiškai nereaguoja. Todėl, jog negali suprasti, ką sakyti. Ji netgi naujienas apie Afganistano valdžios pakeitimą, arba apie tai, jog milijonai amerikiečių nepripažįsta legitimiais JAV prezidento rikimus publikuoja vėluodami visa diena.

O jau apie „aiškinamąją žurnalistiką“, kuri objektyviai ir argumentuotai pasakoja auditorijai apie vykstančių įvykių priežastis, iš vis nėra ką ir kalbėti.

Suprantama,esant tokiom sąlygom lietuviai kaip skaitė, žiūrėjo, klausėsi, taip ir skaitys, žiūrės ir klausysis rusiškąją žiniasklaidą.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 11 — id: `scraped:rubaltic_lt:6df3e18264abd307`

**Title:** Smūgis į nugarą: Lietuva nusprendė pasipelnyti Ukrainai netekus rusiškų dujų tranzito

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuva laukia žymaus rusiškų dujų tranzito per Ukraina sumažėjimo. Apie tai pareiškė Pabaltijo respublikos energetikos ministras Dainius Kreivys. Jo nuomone Kijevo problemos bus naudingos SGD terminalui Klaipėdoje, kuris „žydriuoju kuru“ aprūpins vartotojus užsienyje. Tai yra, Lietuva numato perimti „broliškos“ Ukrainos šalies-tranzitininko statusą. Tą patį gali pareikšti lenkai, kurie 2023 metais ruošiasi atsisakyti rusiškų dujų importo.

Apie Europos energetikos rinkos užkariavimo planus Dainius Kreivys papasakojo komentaruose Reuters agentūrai. Jis prognozuoja, jog antroje 2022 metų pusėje pradės veikti dujotiekis GIPL, jungiantis Pabaltijo dujų tinklus su Lenkija. Teoriškai juo galima perpumpuoti kurą, kurį Lietuva importuoja suskystintą.

Apie šiuos planus Vilnius pareiškia atvirai. GIPL turi pagelbėti Klaipėdos SGD terminalui surasti naujas realizavimo rinkas.

„Mes tapsime didelės integruotos centrinės Europos rinkos dalimi, dujų paklausa regione auga, ir tuo pačiu metu mes laukiame žymaus rusiškų dujų importo per Ukraina sumažėjimo“, - kalbėjo Lietuvos energetikos ministras.

Jo minčių eiga suprantama. Jei „Gazpromas“ sustabdys (arba nors kiek sumažins) tranzitą per Ukrainą, tai energetinė krizė Europoje pasieks katastrofos mastą.

Dujų kainos taps kosminėmis.

Dėl teisės naudotis jo paslaugomis konkuruos visi, pas ką yra fiziška galimybė importuoti dujas iš Lietuvos. Pavyzdžiui, slovakai – jie kaip tik baigia tiesti dujotiekį prie Lenkijos sienos.

Lenkijos ir Čekijos dujų transporto sistemos buvo sujungtos 2011 metais, be to, šis projektas tapo tiesioginiu Rusijos – Ukrainos tranzito krizės padariniu. „Lenkų – čekų dujotiekis yra vilties, jog dujų problemos jau niekada nepalies mūsų valstybių, ženklas. Galų gale ne taip stipriai, kaip prieš keletą metų“, - sakė tuometinis Lenkijos ministras pirmininkas Donaldas Tuskas iškilmingoje dujotiekio atidarymo ceremonijoje.

Bet pagrindinis Lietuvos tikslas – tai kontraktai su pačiais lenkais. Jie randasi arčiausiai, juos galima sugundyti galimybe išnaudoti Inčukalnio dujų saugyklą Latvijoje (stambiausia Pabaltijo teritorijoje). Kreivio žodžiais tariant, Vilnius numato suderinti su jais lengvatinius „žydrojo kuro“ tiekimo GIPL sistema tarifus.

„Pradėjus eksploatuoti dujotiekį, terminale ( Klaipėdoje - RuBaltic.Ru pastaba), visų tikriausiai nebeliks neišnaudotų pajėgumų“, - prognozuoja Lietuvos ministras.

Jie nori įsisavinti Pabaltijo energetinę rinką. Jų manymų, dujas iš Lenkijos turi importuoti Lietuvos vartotojai, o ne atvirkščiai.

Visus savo dujotiekius Varšuva lobijavo ir tiesė siekdama tapti dujų paskirstymo centru Europoje. Ji jau turi savą SGD terminalą. Tikėtinai, atsiras dar vienas. Baltic Pipe dujotiekis sujungs Lenkiją su telkiniais norvegų šelfe. Ir tai, tikriausiai, vienintelis vamzdis, kuriuo lenkai ruošiasi ne eksportuoti, o importuoti dujas.

Vis dar atviras naujojo kontrakto su „Gazpromu“ (senasis baigiasi 2022 m. gruodžio mėn. 31 d.) sudarymo klausimas.

Atskiro dėmesio vertas jo pasisakymas apie tai, jog Lietuva laukia „žymaus rusiškų dujų importo per Ukrainą sumažėjimo“. Iki 2024 metų „žymaus sumažėjimo“ nebus: „Gazpromas“ privalo eksportuoti per Ukrainą kontrakto numatytas dujų apimtis, remiantis principu „pumpuok arba mokėk“.

Beprasmiška pažeisti sutartį – tokiu atveju Kijevas inicijuos ir garantuotai laimės bylinėjimąsi Stokholmo arbitraže. 2018-2019 metais Rusija dėl to jau „apdegė“

Bet lieka neišspręsta, kokias tranzito apimtis išsaugos ukrainiečių dujų transportavimo sistema pasibaigus kontraktui su „Gazpromu“. Maskva daro viską kas įmanomą, kad užkrauti apylankos „srautus“. Su Vengrija jau sudarytas dujų tiekimo susitarimas per Serbiją ir Austriją. 2024 metais turi atsitikti tai, apie kalba Kreivys.

„Gazpromas“ jokiu būdu nesiruošia palikti Europos rinką, nors ir diversifikuoja eksportą.

Teoriškai Lietuva gali pasinaudoti didėle, Kijevo provokuojama, energetikos krize. Visiškas rusiškų dujų tranzito per Ukrainą sustabdymas 2024 metais taps sankcijų „Šiauriniam srautui - 2“ priežastimi.

Atsitiks tai, kas galėjo atsitikti 2020 metų pradžioje, jei „Gazpromas“ ir „Naftogazas“ ne būtų suderinę naujojo kontrakto sąlygas.

Ir dėl to nukentės ir Europa, ir Ukraina, ir Rusija.

Tarp kitko, visa tai ne daugiau, kaip nieko nereiškiančio kalbos. Jei atsitiks tranzito krizė, tai ji prasitęs ne ilgiau, kaip keletą dienų (ne ilgiau 2009 metų krizės). Derybų šalims vis vien teks rasti kompromisą. Užsitęsusio konflikto kaina jiems per daug aukšta.

Taip kad ir čia likimas nelemia Lietuvos SGD terminalui prašokti į „damą“.

Pačius „napoleoniškus“ Kreivio planus nėra lengva komentuoti be ironijos. Nors Ukrainai čia nėra nieko juokingo. Lietuva įnirtingai priešinosi „Šiaurinio srauto – 2“ tiesimui.

Tą patį gali pasakyti (ir , tikriausiai, pasakys!) lenkai, kurie iš viso ruošiasi atsisakyti bendradarbiauti su „Gazpromu“: jei Kijevo ir Maskvos nesutarimai sumažins „nešvarių“ rusiškų dujų tiekimą Europon, tai dar ir bus gerai. Draugystė lieka draugyste, o tabakėlis atskirai.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 12 — id: `scraped:rubaltic_lt:eddd5d7a02983d44`

**Title:** Kaliningradas ir Lenkija vietoj Lietuvos uždirbs tranzito dėka iš Kinijos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Kaliningrado srityje pradėjo veikti naujas terminalų – logistinis centras, kurio pagrindinė funkcija: kinų krovinių, gabenamų į Europa „Naujojo šilko kelio“ šiauriniu maršrutu perkrovimas. Prieš tai Kinija atidarė naują krovinių gabenimo maršrutą į Lenkija, o dar anksčiau pristabdė krovinių gabenimą Lietuvos geležinkeliu. Toliausiai į vakarus nutolęs Rusijos regionas ir lenkų Gdanskas dabar gaus tą, apie ką svajojo Lietuvą, ir ką pati iš savęs atėmė savo intrigantiškos politikos dėka: investicijas į bendradarbiavimo su KLR infrastruktūrą.

Naujas geležinkelio terminalas buvo pastatytas pačiame Kaliningrado srities centre – ties Černiachovsko miestu.

„Kaliningrado kryptis – viena iš perspektyviausių krovinių gabenimo krypčių. Tik per pastaruosius trejus metus konteinerių tranzito apimtis per Kaliningrado sritį padidėjo septynis kartus. Naujo terminalo sukūrimas suteikia papildomas šių gabenimų ir mūsų šalies tranzitinio potencialo didinimo galimybes“, - kalbėjo AB „Rusijos geležinkeliai „ generalinis direktorius Oleg Beloziorov terminalų – logistinio centro (TLC) atidarymo ceremonijoje.

„Naujajame komplekse realizuotas unikalus Kaliningrado transporto sistemos pranašumas: rusiško ir europietiško geležinkelio bėgių formato buvimas. Šioje aikštelėje kuriama infrastruktūra, kuri mums leidžia įsitaisyti į Naująjį šilko kelią, į naujus logistikos projektus“, - sakė Kaliningrado srities gubernatorius Anton Alichanov terminalo atidaryme.

TLC „Rytai – Vakarai“ randasi pusvalandį trunkančios kelionės iki Železnodorožnyj – Skandava sienos kirtimo punkto nuotolyje. Černiachovske konteineriai su kinų prekėmis bus perkraunami iš vagonų su rusišku plačiu tarpuvėžiu (1520 milimetrai) į vagonus su europietišku siauru tarpuvėžiu (1435 milimetrai) ir toliau vyks– į ES šalis.

Tarp kitko, ne tik viena Kaliningrado sritis galėjo būti tokiu logistiniu tiltu tarp Rytų ir Vakarų. Pabaltijo šalyse taip pat yra geležinkeliai su rusišku plačiu tarpuvėžiu („okupacijos paveldas“) ir yra atskiri nutiesti nukamuoto geležinkelio Rail Baltica ruožai su europietišku siauru tarpuvėžiu. Kinų konteinerius būtų galima laisvai perkrauti ir ten.

Būtent apie tai ir svajojo Lietuva, kuri daugelį metų reklamavo save kinams kaip Padangių šalies „vartais į Europos Sąjungos rinkas“. Klaipėdos uosto plėtra. Lietuvos geležinkelio modernizavimas KLR strateginių investicijų į geležinkelio infrastruktūrą sąskaita.

Dabar visi tie „norėjimai“ Lietuvai – priežastis atnaujinti daugiausiai pasaulyje vartojančios alkoholį šalies vardą.

„Parodomoji pyla“ Lietuvos veikėjams buvo surengta iš karto keliomis kryptimis, tame tarpe ir trokštamo tranzito sferoje. Rugpjūčio mėnesį geležinkelio kompanija China railway container transport corp. paskelbė, jog dėl nepalankios politinės situacijos, krovinių gabenimas iš Kinijos į Lietuvą yra pristabdomas.

Padangių šalis įveda sankcijas Lietuvai, tiesiai taip ir sakydama. Tai sankcijos. Už jūsų priešiškumą ir intrigiškumą.

Lietuvos vadovybė ir jos globėjai Vakaruose puolė įtikinėti, netekusius vilties gauti kinų pinigų, lietuvius, jog Pekinas, siekdami pakeisti Lietuvos geopolitinį išsirinkimą, išnaudoja ekonominę prievartą. Tuos prasimanymus netrukus paneigė pats Pekinas.

Lenkija – tokia pat nepalaužiamai proamerikietiška šalis, kaip ir Lietuva. Apie tai, ką palaikys Lenkija besiplečiančioje globalinėje kinų – amerikiečių konkurencijoje, neabejoja niekas. Nei Varšuvoje, nei, Vašingtone, nei Pekine. Ir visgi, Kinija plečią bendradarbiavimą su lenkais.

Kodėl? Tikėtina, todėl jog lenkų vadovybė laikosi kokių tai mažų mažiausių padorumo taisyklių, kurios, principe, leidžia šalims palaikyti santykius ir ne atšaukti ambasadorius iš sostinių. Nekuria rezoliucijų „apie uigūrų genocidą“ ir Europarlamentą neragina jas priimti. Ne skelbia karą kinų išmaniesiems telefonams. Neklykia ant visos Europos, jog ji pati doriausia Europos Sąjungoje, kadangi galvoja ne apie kinų pinigus, o apie vertybes, ir todėl apie Kiniją šneka viską, ką tik nori.

Paskutiniame punkte, tarp kitko, Lietuvos valdžia gudrauja. Vilniuje apie kinų pinigus galvoja ir dar kaip. Lietuvos valdžia kartas nuo karto primena, jog suinteresuota santykių su Kinija vystymuisi, kartoja savo mėgstama „politika - atskirai, ekonomika – atskirai“, ir tikisi gražinti į Lietuvą kinų ambasadorių

Kaip sakoma viltis miršta paskutinė. Gal būt, Lietuva dar pamatys kinų pinigus?

Tai va, nepamatys.

O Lietuvos politikai gali džiaugtis savo „vertybėmis“ .

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 13 — id: `scraped:rubaltic_lt:acfea53365885169`

**Title:** Europa pripažino energetinę priklausomybę nuo Rusijos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Europos žiniasklaida praneša apie Europos Sąjungos prašymą Rusijai padidinti akmens anglies tiekimą į Europą. Kūrenimas anglimi grubiai prieštarauja naujai „žaliajai“ ES ideologijai, bet šmėkšančios prieš juos energetinės krizės fone europiečiams ideologija neberūpi. Jie noriai pripažįsta Rusiją energetine supervalstybe ir prašo tiekti Europai kiek galima daugiau energijos, kas visiškai neseniai buvo vertinama kaip „energetinė priklausomybė“.

Bloomberg agentūros šaltiniai praneša, jog Briuselyje vyrauja beveik panika. Europos dujų saugyklos pustuštės, atsinaujinantieji energijos ištekliai – vėjo jėgainės, saulės energijos jėgainės, bangų energiją ir kiti „žaliosios energetikos“ stebuklai – nesugeba padengti energijos deficito, ir europiečiams vis ryškiau aiškėja šildymo sezono sužlugdymo perspektyva.

Esant tokiom sąlygom, priklausomybė nuo pigios energijos iš Rusijos tampa kritine ir prisieina imtis kraštutinių priemonių.

Šaltinių informacija labai panaši į tiesą. Anksčiau padidinti dujų tiekimą į Europą Rusijos ne prašė, o reikalavo ne tik patys europiečiai, bet ir Tarptautinė energetikos agentūra, o taip pat ir JAV valstybės departamentas. Kitaip sakant, visi tie, kurie buvusius prieš tai du dešimtmečius dirbtinai ribojo rusiškų dujų tiekimą į Europą. Dabar jie stengiasi įbrukti bendruomenei konspirologinę versiją, jog tai Rusija dirbtinai riboja tiekimą Europon ir dujų rinkoje sukuria deficitą, kad greičiau paleisti „Šiaurinio srauto-2“ dujotiekį.

Būnant prie šildymo sezono sužlugdymo ribos Europai nerūpi ideologija energetinėje politikoje. Ir kalbama ne tik apie rusofobiją.

Pavyzdžiui, Estijoje, vėl pradėjo eksploatuoti senas, skalūnais kūrenamas elektrines. Estijai toks sprendimas - „nusikaltimas“ iš karto dviems ideologiniams pagrindams. Ekologinė Europos Sąjungos politika, kuria Estija, kaip madinga ir progresyvi šiaurės Europos šalis, privalo sekti, o skalūnų energetika Estijai, tai „sovietų okupacijos“, „prakeikto paveldo“ doktrinos likutis.

Kadangi šaltis ne šildo – prisieina atmesti visus tuos kliedesius apie „okupaciją“.

Anglies užpirkimai Rusijoje, apie kuriuos europiečiai sužino ne iš oficialiųjų šaltinių bet per intarpus žiniasklaidoje – tai iš tos pačios serijos. Šildytis kūrenant anglį, lyg kažkoks tai Tadžikistanas, šiuolaikiniai, Gretos Tumberg isterijomis išauklėtai Europai – paprasčiausiai yra nepadoru. Ir ką daryti? Niekam nesinori šalti žiemą.

Tarp kitko, mažai kas atkreipė dėmesį, jog atominė energetika Europoje kažkaip tai nepastebimai buvo priskirta prie ekologiškos ir madingos. Statyti atomines elektrines dabar tapo prestižišku ir Briuselis to nesmerkia (suprantama, jei jas stato ne „Rosatomas“), todėl savo atomines programas parengė ta pati Estija ir Lenkija.

Lietuvos valdžia, su savo besitęsiančia kova su BelAE, tokiame kontekste išrodo labai kvailai, bet kas žino, ar nepasikeis Vilniaus požiūris į „Astravo monstrą“ po to, kai išseks dujų atsargos, o jų kaina pakils iki naujo istorinio maksimumo? Ta kaina jau aukštesnė 1100 eurų už tūkstantį kubinių metrų...

Bendrai paėmus, pamokytina stebėti, kaip, įtakojant pilnaverčiai apvalančiai krizei, energetinė Europos politika atsikrato visų tų sąnašų, politizuoto, ir atsiveria fundamentalūs dalykai.

Tradiciniai energijos šaltiniai patys patikimiausi ir neturintys pakaito. Atsinaujinantieji energijos šaltiniai, kokiais madingais ir ekologiškais jie bebūtu, negali būti pilnaverte tradicinės energetikos alternatyva. Klimato ir kitų kataklizmu sąlygomis visos tos brangiai kainuojančios saulės bei vėjo energijos jėgainės genda ir sukuria energetikos krizę, kaip tai metų pradžioje atsitiko Teksaso valstijoje, ir kas dabar gresia Europai.

Pats patikimiausias ir pigiausias dujų tiekimas – tai tiekimas dujotiekio vamzdynais iš Rusijos.

Tie, kurie pasirašė tokius kontraktus, dabar dujas gauna žymiai pigiau, negu tie, kurie pasitikėjo laisvu kainų susidarymu, kaip kainų sumažėjimo užtikrinimu. Pats ryškiausiais pavyzdys – Baltarusija, kuri moka 128 dolerius už tūkstantį kubinių metrų: 10 kartų mažiau negu ta kaina, kuria ES rinkoje dabar prekiaujama dujomis.

Visa ekvilibristika su energetinių alternatyvų tiesioginiam tiekimui iš Rusijos išradimais, kaip tai SGD terminalai, reversas ar skalūnų dujų paieška savo teritorijoje, tik pakelia energijos kainą.

Pagaliau, laikas įvertinti ir Rusijos vaidmenį europietiškoje energetikoje.

Stovint ant energetinės krizės slenksčio europiečiai yra priversti priimti šią, jiems karčią, tiesą.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 14 — id: `scraped:rubaltic_lt:97e37318a554c983`

**Title:** Rusija, gelbėk: Pabaltijyje baigiasi dujų atsargos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Inčukalnio požeminėje dujų saugykloje – stambiausioje Baltijos šalių teritorijoje – dujų atsargos gali baigtis pačiame šildymo sezono įkarštyje. Apie tai pareiškia dujų transporto sistemos AS Conexus Baltic Grid Latvijos operatoriaus atstovas. Jei žiema bus šalta, Pabaltijui tikriausiai prisieis ieškoti alternatyvinius energijos šaltinius, kartu su tuo, visi realūs variantai taip ar šiaip bus susiję su “agresyviu kaimynu” – Rusija.

Inčukalnio saugyklą galima pavadinti vienu iš Pabaltijo „energetinės nepriklausomybės“ simboliu. Suskilus TSRS, trečdalis jo akcijų atiteko „Gazpromui“, kuris negailėjo lėšų savo turto išlaikymui užsienyje. Praeitais metais, vykdant ES Trečiojo energetikos paketo reikalavimus, rusišką monopolistą visgi atstūmė nuo latviškos DTS.

„Gazpromo“ dalį išpirko kompanija Augstsprieguma tīkls. Ji taip pat įsigijo ir Uniper ir Itera Latvija akcijas, tuo pačiu pradėjo kontroliuoti Conexus Baltic Grid – nepriklausomą Latvijos dujų transporto sistemos operatorių.

Rusijos šalis nesiginčijo. Priešingai, ji pasinaudojo proga gauti gerus pinigus. Sandorio suma sudarė 77 milijonus dolerių - Uniper ir Itera Latvija savo akcijas pardavė pigiau.

„Tai žinios ne rinkai ir vartotojams, bet tai turi svarbią psichologinę reikšmę vyriausybei. Todėl, kad visi kaimynai, žinoma, užduoda klausimą: „Kas vyksta ten pas jus?“ Pas jus ten toks svarbus elementas, o dividendus nuo kompanijos gauna „Gazpromas““, - kalbėjo energetikos specialistas Juris Ozolinš

Dabar „Gazpromas“ nieko negauna ir nieko nededa į Inčukalnio dujų saugyklą. Bet kam nuo to palengvėjo?

„Žydrojo kuro“ atsargos Inčukalne gali baigtis sekančių metų sausyje. Pačiame šildymo sezono įkarštyje.

2018 metais Pabaltijys jau buvo susidūręs su analogiška problema. Bet tada problemos kilo ne dėl gamtinių dujų stygiaus, bet dėl nepakankamo slėgio saugykloje. Na, ir žiema Baltijos šalyse buvo pakankamai švelni.

„Dujų rinkos atvėrimas Latvijoje buvo orientuotas ne į tiekimo patikimumą, o į mistinę prielaidą, kad kris kainos. Tokia buvo politinė nuostata, kuriai buvo paaukotas dujų tiekimo patikimumas. Jei praėjusią žiemą žemesnė nei minus 20 laipsnių temperatūra būtų išsilaikiusi dvi tris dienas ilgiau, Latvijoje būtų prasidėjusi energetinė krizė“, – prisipažino „Latvijas gaze“ valdybos pirmininkas Aigars Kalvitis

Rinkos dalyviai griebėsi aktyviai imti dujas iš Inčukalnio saugyklos. Ypatingai dideli srautai, pavyzdžiui, tekėjo iš Latvijos į kaimyninę Lietuvą: 2,4 TWh tik per tris mėnesius. Tai istorinis rekordas.

2020-2021 metų šildymo sezoną Inčukalnio dujų saugykla baigė pakankamai nualinta. O po to kilo problemos, susijusios su jos užpildymu: SGD deficitas, kurių tiekėjai puolė į Aziją, „Gazpromo“ atsisakymas rezervuoti papildomus galingumus Ukrainos DTS, dėl stiprių karščių padidėjusi elektros energijos paklausa ir t.t

Vasaros pradžiai dujų kainos ne tik nenukrito, bet pradėjo kilti į viršų. Conexus Valdybos pirmininkas Uldis Bariss baimingai pažymėjo, jog šių metų energetikos rinka yra labai nestabili.

Nuo sausio iki birželio mėnesio į Latviją buvo perduota 0,6 TWh – 78 procentais mažiau negu prieš metus. Lietuvos Amber Grid generalinis direktorius Nemunas Biknius tam randa logišką paaiškinimą: „Šaltos žiemos Europoje ir kituose pasaulio regionuose ištuštino dujų saugyklas, kurias tiekėjai, nežiūrint į smarkų gamtinių dujų kainų padidėjimą fondų biržose, tikisi užpildyti sekančiam šildymo sezonui. Be to, dėl smarkaus išmetimų kvotų kainos padidėjimo, Europos pramonė siekia sudeginamą akmens anglį pakeisti dujomis, kurios išmeta mažesnį kiekį CO 2 . Dujų paklausa didėja taip pat ir dėl Azijos rinkų atsistatymo po pandemijos, todėl dujų tiekėjai taip pat dažniausiai savo krovinį nukreipia į Azijos vartotojų pusę“.

Todėl Inčukalnio dujų saugykla naują šildymo sezoną pasitiko būdama ne geriausioje savo formoje.

Kompanijos korporatyvinės strategijos skyriaus vadovo Janis Eisaks žodžiais tariant, dabar pildyti saugyklas dujomis nenaudinga – biržų brokeriai, naudodamiesi palankia kainų konjunktūra, stengiasi jas parduoti.

„Kiekviena perteklinė megavatvalandė, užpirkta prekiautojais ir saugoma Inčukalne potencialiai gresia €30 netekimu sekančių metų pavasarį. (...) Skaitykime, jog ši žiema bus panaši į praėjusią. Atsižvelgiant į aukštą kainų riziką, gali būti ir tokia situacija, kad iki sausio mėnesio Inčukalnis ištuštės“, - perspėja Eisaks

Pats paprasčiausias variantas – padidinti elektros energijos importą. Praeitą žiemą Latvija taip ir padarė: sausio mėnesį ji iš Rusijos importavo 473,4 GWh elektros energijos (tai 2,5 karto daugiau nei prieš mėnesį).

Tačiau laisvam srovės pertekėjimui BRELL elektros žiedu trukdo Lietuvos sisteminis operatorius Litgrid, kuris rugsėjo mėnesio 15 d. vienašališkai apribojo maksimalų elektros perdavimo linijų pralaidumą per Baltarusijos sieną. Tokiu būdu Vilnius ketina „boikotuoti“ Baltarusijos atominę elektrinę (BalAE)

Latvijoje Litgrid veiksmus pavadino techniškai nepagristais ir pažadėjo paduoti skundą Europos komisijai.

Latvių susirūpinimą suprasti galima: ant nosies sunkiausio šildymo sezono startas.

Todėl Lietuvos eilinis BalAE blokados „priepuolis“ atsitiko ne laiku. Galimai, po trejų – keturių mėnesių jai vėl prisieis kapituliuoti prieš baltarusišką „atominį monstrą“

O pavasarį viskas vėl prasidės iš pradžios.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 15 — id: `scraped:rubaltic_lt:66c7325cc286bac1`

**Title:** Lietuva užmiršta: dėl naujų sąjungininkų Azijoje JAV nusispjauna ant NATO

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Sudariusi karinį bloką AUKUS su Didžiąja Britanija ir Australija, JAV iškėlė į naują lygmenį QUAD karinį junginį su Indija, Japonija ir ta pačia Australija. Amerikiečių diplomatinio aktyvumo siekiai pagarsinami tiesiogiai – kova su Kinija. Tuo pat metu paaštrėjo karinė-politinė situacija taip vadinamoje Kosovo valstybėje, atsiradusioje po to, kai amerikiečiai ir jų NATO sąjungininkai Europoje bombomis atakavo Jugoslaviją. Tačiau, amerikiečiams dabar jau galutinai nusispjaut ir ant Kosovo, ir ant NATO, ir ant sąjungininkų Europoje.

Paaiškėjo, jog, rodos, jau seniai „demokratinės bendruomenės“ užgesintas konfliktas dėl buvusios Jugoslavijos teritorijų, iki šio su mumis. Serbija apkaltino Kosovo, kurią ji skaito savo teritorija, Kosovo serbų pogromais, kurie atmetė Prištinos ultimatumą pereiti ant Kosovo automobilinių numerių ir už tai neteko laisvo judėjimo teisės.

Šalies Prezidentas Aleksandr Vučič prigrasino Prištinai karo aviacijos panaudojimu, jei neįsimaišys Vakarai ir neprivers Kosovo baigti etninių serbų pogromus nacionaliniuose anklavuose.

„Septynias dienas Vakarai nekreipė dėmesio, bet dėmesį atkreipė, kai Serbija parodė, jog neleis pogromų. Jie galvojo, jog aš juokauju“, - nervingai pareiškė Vučič per nacionalinę televiziją.

Aleksandr Vučič, jo pačio žodžiais tariant, netgi skambino generaliniam NATO sekretoriui Jens Stoltenberg ir reikalavo nors kaip įvertinti situaciją. Aiškaus Jens Stoltenberg atsakymo jis neišgirdo, dėl ko buvo labai suglumintas.

Tik tada, kai Belgradas pradėjo koncentruoti karines pajėgas prie sienos su Kosovo ir prigrasino smogti į Prištiną iš oro, Šiaurės Atlanto aljansas atsigavo ir nukreipė NATO pajėgas link Kosovo ir Serbijos atribojimo linijos.

„KFOR [NATO kontingentas] įdėmiai stebi situacija Kosovo ir yra susikoncentravęs savo mandatą taikyti visų Kosovo gyvenančių bendruomenių saugios ir apgintos aplinkos bei judėjimo laisvės užtikrinimui“, - pareiškė Aljanso buveinėje Monse.

Klausiama, kodėl eskalacijos metu NATO savo tiesioginės atsakomybės zonoje tai keistai elgėsi? Kodėl Belgradas visą savaitę negalėjo susisiekti su jo sekretoriatu?

Būtent demonstratyviai. Amerikiečiai savo požiūrio neslepia, ir atvirkščiai, siunčia NATO sąjungininkams signalus, esą, iš tos pelkės išsikapstykite patys, kaip mokate.

JAV valstybės sekretoriaus padėjėjas Europai ir Eurazijai Gabrijiel Eskobar atsisakė dalyvauti Briuselyje derybose dėl buvusios Jugoslavijos, juose dalyvaujant Belgrado ir Prištinos atstovams. „Ne, ponas Eskobar derybose nedalyvaus. Šiame dialoge dalyvauja Kosovo, Serbija ir ES. Visi likusieji dialogą palaiko iš išorės“, - JAV atstovo nedalyvavimą darbo grupėje patvirtino ES atstovas spaudai išorės politikos ir saugumo klausimams Peter Stano.

Tik pagalvokite: dalyvauti beveik karinės krizės Europoje sureguliavime atsisakė ne JAV prezidentas, be valstybės sekretorius, ir netgi ne jo padėjėjas Europai ir Eurazijai, o to padėjėjo pavaduotojas.

Klausiama, kuomi dabar taip užsiėmusios Jungtinės Valstijos? Vidaus problemomis? Ne, palikęs Afganistaną Vašingtonas pradėjo aktyvią veiklą užsienio politikos sferoje. Tik to aktyvumo erdvė – kitame nuo Europos pasaulio gale.

Tomis dienomis Baltieji rūmai iškėlė į kokybiškai naują lygį Keturšalį saugumo dialogą, Indijos - Ramiojo vandenyno regiono specialistams žinomą kaip QUAD – JAV, Japonijos, Indijos ir Australijos karinę – politinę sąjungą. 2007 metais QUAD idėją pasiūlė Japoniją ir ją entuziastingai palaikė Indija, šios dvi šalys atvirai bijosi Kinijos, ir todėl jos seniai JAV lobijavo „azijietiško NATO“ idėją.

Vašingtonas malonėjo išgirsti azijietiškų sąjungininkų prašymą, bet kol ruseno viltis, jog Pekine pasikeis režimas, QUAD greičiau buvo „mieganti“ struktūra. Už tai po to, kai JAV suprato, jog Kinija sudaro pačią didžiausią grėsmę jos globaliniam dominavimui ir buvo pripažinta pagrindiniu Amerikos priešu, dėmesys prieš Kiniją nukreiptam aljansui su azijiečiais ir Australija pradėjo augti ne dienomis bet valandomis.

Viso to rezultatu tapo tai, jog JAV inicijavo pirmąjį valstybių vadovų lygio akivaizdinį QUAD susitikimą dalyvaujant Džozefui Baidenui. Pastarajam ši priemonė akivaizdžiai buvo įdomi, o ne atrodė kaip protokolinės prievolės atlikimas, kaip tai buvo NATO susitikime vasarą.

Baltieji rūmai skaito QUAD aktyvavimą svarbiu neseniai sudaryto AUKUS bloko – dar vienos, prieš Kiniją nukreiptos JAV, Didžiosios Britanijos ir Australijos sąjungos, papildymu.

Amerikiečiai, be didžių geopolitinių tikslų, dar ir „atspaudė“ iš prancūzų 66 milijardų dolerių vertės povandeninių laivų statybos Australijai kontraktą. Prancūzai ilgai ir nesėkmingai piktinosi, o nuskriausta ES pareiškė, jog pas Europą taip pat yra savi interesai ir galimybės Indo-Pacifikos regione, ir ji, gal būt, taip pat įeitu į AUKUS.

Tik amerikiečiai jos nepakvietė.

Vyksta strateginiai procesai, apie kuriuos žymus mokslininkai-tarptautininkai perspėjo dar tais laikais, kai gyvavo Sovietų Sąjunga, vyko šaltasis karas ir tarptautinis gyvenimas sukosi aplink Rytų Europos. Dabar visa Europa, o ne tik Rytų pereina į tarptautinės politikos, kurios centras persikelia į Pietvakarių Aziją, periferiją.

Ir tai labiausiai išryškėja tame, jog Europa pasiliko tolimoje amerikiečių dėmesio tarptautiniams reikalams periferijoje.

Nagi, paurgzkite ant jų už AUKUS. Šioje organizacijoje iš karto du NATO nariai: JAV ir Didžioji Britanija. Ir Didžioji Britanija Amerikai yra įdomi kaip AUKUS narys kovai su Kinija, o ne kaip NATO narys kovai su Rusija.

Dabar amerikietiškieji sąjungininkai NATO nariams „akis muilina“, juos „meta“ ir visokeriopais duoda suprasti, kad tie nelįstų prie jų ir ne maišytų jiems svarbesniuose reikaluose.

Tačiau „demokratijos eksportuotojai“ Pabaltijyje kažkodėl tai iki šiol tikisi, jog patronai už vandenyno užsiminės jų fobijomis ir įsivėlinės į konfliktus, kuriuos savo antirusiškais išsišokimais Pabaltijys sukelia postsovietinėje erdvėje.

Prablaivėjimas bus negailestingas.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 16 — id: `scraped:rubaltic_lt:c592fb5309e6723d`

**Title:** Pabaltijys pavertė pajuokos objektu pagrindinę „Europietiško pasirinkimo“ statybą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Geležinkelio Rail Baltica eksploatacijos pradžią vėl nukels – šį kartą iki 2030 metų. Paskelbęs apie tais administruojančios kompanijos Rail Baltica valdybos pirmininkas pažadėjo, jog jau tam terminui, 2030 metais Rail Baltica tikrai-tikrai pradės veikti. Kuo dar labiau pralinksimo tuos, kurie dešimtmečiais stebi Pabaltijo „amžiaus statybą“, kurios galo nesimato, o visa šio stambiausio Europos Sąjungos infrastruktūrinio projekto Pabaltijyje esmė tame, kad „pjaustyti“ ir, tiesiogine šio žodžio prasme, užkasti į žemę ES biudžeto pinigus.

«Iki šiol 2026 metai buvo mūsų pačių išsikeltas tikslas, kuris tvirtai, kaip akmuo, nebuvo apibrėžtas Europos lygmeniu. Deja, akivaizdu, jog šio grafiko laikytis neįmanoma. Viena vertus, jo neįmanoma įgyvendinti techniniu ir struktūriniu požiūriu, kita vertus, nėra padengtas visas projekto finansavimas“,- sakė Tynu Griunber, Rail Baltica Estonia valdybos pirmininkas.

Griunbergo žodžiai reiškia, jog geležinkelio Rail Baltica atidarymas vėl bus perkeltas. Šį kartą – 2030 metams. Ir jau 2030 metais paleis tiksliai, geležinė garantija! Jei prieš tai buvęs „trumpiausias terminas“ 2026 metai – Pabaltijui buvo „tvirtas kaip akmuo“, tai naujas bus atlietas iš bronzos.

Po to, suprantama, namo paršliaužia ant savo keturių, ir prasideda nepertraukiamo girtuokliavimo laikotarpis.

Tas pats ir su Rail Baltica. Geležinkelį iš Skandinavijos į Centrinę Europą per Pabaltyjį projektuoja ir stato jau ketvirtį amžiaus, o ekspluatacijos pradžios terminas nutolsta vis toliau, kažkur tai už horizonto. Ir kiekvieną kartą paaiškėja, jog stinga pinigų, kuriuos Europos Sąjunga skiria šiai statybai.

Štai ir dabar Rail Baltica valdybos pirmininkas aimanuoja, jog „nėra padengtas visas projekto finansavimas“. Nors dar tik metų pradžioje Lietuva, Latvija ir Estija prigrasino užblokuoti ES ekonomikos atstatymo fondą, jei Briuselis jiems neišskirs žadėtų pusantro milijardo eurų Rail Baltica statybai baigti.

Tada Briuselis kapituliavo, davė pinigų, bet praėjus keliems mėnesiams, pasirodė, jog jų vėl nebėra, ir statybos pabaiga vėl nukeliama į miglotą ateitį.

Bendra geležinkelio statybos kaina dešimtmečiais augo kas metai ir išaugo iki 7 milijardų dolerių (kurių, kaip dabar tapo aišku, taip pat maža) Per tą laiką ir už tokius pinigus jau buvo galima nutiesti TransSibiro magistralę, tačiau Rail Baltica vadybininkai bendruomenei vis pateikia „galutinius terminus“ ir prašo dar padidinti sąmatą.

Efektingame integraciniame darinyje tuos vadybininkus seniau jau būtų pasodinę, ir visos vyriausybės Lietuvoje, Latvijoje ir Estijoje būtų atsistatydinusios dėl kaltinimo korupcija įsisavinant ES fondus. Tačiau Briuselis apsimeta, jog nieko nemato, arba iš tikrųjų nieko nemato.

Suprantama, jog sunku nepamatyti, kaip šiaurės-vakarų periferijoje užkasė į žemę jau 7 milijardus ES pinigų, bet taip ir nepastatė tokį kelią, kurio statybai tie pinigai buvo duodami. Bet, tikėtina, kad Europos Sąjungai ant tiek nusispjauti į Pabaltijį, jog ji sąmoningai šeria vietinius vadovus, kad tik tie per daug nelįstų su prašymais ir reikštų savo lojalumą?

Jei taip, tai Estijai, Latvijai ir Lietuvai ši naujiena yra labai bloga.

„Sovietų okupantai“ jei tiesė Pabaltijui kelius, tai pabaltijiečiai tais keliais važinėjo, ir važinėja iki šiol. Europos Sąjungoje Pabaltijys tai pat gyvena svetima sąskaita, bet sovietų pinigai skirti keliams įsikūnijo į kelius, o europietiški pinigai skirti keliams įsikūnija į, turinčios prieigą prie vyriausybinės rangos, gigantiškos kamarilės elitinį vartojimą.

O tai reiškia, jog kai pas ES vėl pasibaigs pinigai, Pabaltijui nieko neliks. Nei elitinio vartojimo, nei kelių.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 17 — id: `scraped:rubaltic_lt:aefe568deab2c54a`

**Title:** Europa isterijoje: rusiškos dujos nueina į Kinija

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Europos Sąjungoje rengia slaptą „dujų karo“ su Rusija planą. Apie tai pranešė britaniškos Times apžvalgininkas Bruno Uoterfild. Jo žodžiais tariant, iniciatyvos autoriai siūlo sudaryti strategines „žydrojo kuro“ atsargas, idant apsaugoti Europą nuo tarptautinių energetikos rinkų svyravimų. Paradoksas tame, jog tokius strateginius rezervus Europa turėjo – rusiškų dujų vartotojai visada galėjo pasikliauti, kad papildomos apimtys bus tiekiamos. Dabar ne taip, „Gazpromas“ užpildo savo saugyklas ir didina teikimą į Kiniją vamzdynu „Sila Sibiri“. Rusiškų dujų Europai nelieka.

„Europos energetikos ministrai aptarė ambicingus strateginių dujų atsargų užpirkimo bendru bloku planus siekiant priešintis Rusijos pastangoms sumažinti tiekimą ir padidinti kainas, - rašo Bruno Uoterfild. – Dabartinis Europos Sąjungos posėdis turėjo būti pašvęstas klimato kaitai, bet buvo sudrumstas dujų stygiumi ir, dėl to kilusiais kainų šuoliais, kurie šią žiemą grasina energetine krize. Pagrindinis krizės faktorius yra gamtinių dujų apimčių eksporto iš Rusijos į Šiaurės Europą sumažėjimas po to, kai dėl ilgos praeitų metų žiemos buvo sumažinti saugyklų pajėgumai“.

Times apžvalgininkas arba nežino informacijos, arba tikslingai dezinformuoja savo skaitytojus.

Priešingai, „Gazpromas“ tiksliai vykdo savo kontraktinius įsipareigojimus ir didina eksporto apimtis.

Per šių metų aštuonis su puse mėnesio rusiška monopolija išsiuntė į tolimo užsienio šalis 138,6 milijardo kubinių metrų dujų – truputi mažiau, negu rekordiniais 2018 metais (141,3 milijardo kubinių metrų). Tiekimas į Turkija išaugo 157,7 procento, į Vokietija – 35,8 procento, į Rumuniją – 347,6 procento, į Bulgarija – 52,3 procento.

Tarp kitko, Europai vis vien nepakanka: dujų atsargos jų PDS randasi minimaliame lygyje per daugelį metų.

Tam, kad ištaisyti situaciją, Ispanija siūlo sudaryti „bendrą kuro katilą“ – įsigyti strategines dujų atsargas, kurios apsaugos Europą nuo nestabilumų pasauliniuose energetikos rinkose. Tada Rusija daugiau nebegalės imtis savo vakarų partnerių šantažo.

Rusiškų dujų vartotojai visada turėjo galimybę užsisakyti papildomas apimtis. Pats „Gazpromas“ reiškė savo pasirengimą tiekti europiečiams kurą virš savo kontraktiniuose įsipareigojimuose numatytų apimčių.

„Daugelį metų kompanija pabrėždavo, jog turima apsčiai gamybinių gavybos pajėgumų, kuriuos galima išnaudoti kaip Rusijos ir Europos Sąjungos dujinio bendradarbiavimo plėtros bonusus. Bet tie viršijantys pajėgumai susidarė prieš daugelį metų dėl perinvestavimo, kuris vyko pernelyg optimistinio būsimos paklausos vertinimo fone ir, laikui bėgant, palaipsniui, tikėtinai, jie buvo prarasti“,- spėlioja energetikos ekspertas iš Rusijos Aleksandr Sobko.

Uoterfild aprašyta „dujų karo“ su Rusija koncepcija pagrista nusenusiais stereotipais.

Kas pagelbėjo Europai susidoroti su be precedentiniais šių metų sausio-vasario šalčiais, kai jos požeminės saugyklos pasirodė pus tuščios? „Gazpromas“.

Kas turi kompensuoti dujų deficitą Europoje prieš naujo šildymo sezono pradžią? „Gazpromas“.

Bet reikalas ne tame, jog Rusijos monopolija dėl kokių tai priežasčių sulaiko eksportą.

„Gazpromo„ gamybinis aktyvumas yra susietas su jo produkcijos realizavimo Rusijoje ir užsienyje planiniais rodikliais. Kalbant paprastai, kompanija turi apskaičiuoti kiek dujų ji galės parduoti. Kokia prasmė siekti rekordinių dujų gavybos apimčių, jei nėra tų apimčių realizavimo rinkos?

Galima tik spėlioti, į kokias apimtis šiais metais orientavosi „Gazpromas“.

Bet vargu ar jis numatė, jog Europoje kils toks aštrus dujų deficitas.

Preliminariais duomenimis, per šių metų aštuonis su puse mėnesio kompanija padidino gavybą 17,8 procento (arba 53,9 milijardo kubinių metrų). Maždaug ant tiek, išreiškiant procentais, padidėjo eksportas į tolimo užsienio šalis (17,4 procento). Auga dujų tiekimas į Kiniją vamzdynu „Sila Sibiri“ – jis reguliariai viršija „Gazpromo“ paros kontraktinius įsipareigojimus.

Pagaliau, vartojimas taip pat auga ir Rusijos vidaus rinkoje. Daugelyje regionų šildymas buvo pradėtas savaitę anksčiau, negu praeitais metais. Rusijai pačiai reikia ruoštis žiemai, kuri pagal sinoptikų prognozes žada būti labai rūsti. „Gazpromas“ neslėpė, jog šiais metais numato tėvynines PDS užpildyti rekordinėmis kuro apimtimis.

„Gazpromo“ dėmesys nukreiptas į vidaus rinką, kartu su tuo jis siekia išvengti tiekimo destabilizavimo, nežiūrint į rekordinio pelno perspektyvą užsienyje. Pas „Gazpromą“   ne tiek daug papildomų laisvų pajėgumų, kad taip, staiga, padidinti gavybą“, - pažymėjo kompanijos Wood & Co. Analitikas Ildar Davletšin.

Tuo metu suerzinta Europa susigalvojo sąmokslo teoriją, remiantis kuria, Maskva išnaudoja energetinį šantažą dėl greito „Šiaurinio srauto – 2“ paleidimo. Žinoma, šis tvirtinimas turi savo logiką. Bet lieka atviras klausimas, kokias dujų apimtis Rusija pasiruošusi pasiūlyti savo vakarų partneriams.

Tai tiesioginis kovos už „energetinę nepriklausomybę“ rezultatas. Kovos, kurią ji aktyviai organizuoja paskutiniais 10-15 metų. ES forsavo atnaujinamų energijos šaltinių (AEŠ), kaip tradicinės generacijos alternatyvą, vystymą ir pasistatė SGD terminalus. Rezultate vėjo malūnai ir saulės baterijos neišlaikė stiprių šalčių, suskystintų gamtinių dujų tiekėjai pačiu atsakingiausiu momentu puolė į Azijos – Ramiojo vandenyno (ARV) regioną – ten, kur energetikos resursų kainos dar didesnės.

Juridinis karas su „Gazpromu“ vyksta nuo 2009 metais Trečiojo energetikos paketo implementavimo į europietiškus įstatymus. Apribojimo prieš rusišką kurą meno apogėjumi tapo atnaujintos ES dujų direktyvos priėmimas, kuri turi apriboti „Šiaurinio srauto – 2“ pralaidumą.

Palaikyti perteklines gavybos pajėgumus ne racionalu. Bet dabar kovotojai už „energetinę priklausomybę“ nuo Rusijos piktinasi, jog „Gazpromas“ ne didina savo dalį europietiškoje dujų rinkoje. Didina – blogai, ne didina – taip pat blogai.

Bejėgiškumo priepuolyje ES kuria fizinio dujų rezervo sudarymo planus. Šiam šildymo sezonui jie niekaip neįtakoja – kalbama apie strateginį sprendimą. Bus logišku klausimas: iš kokių šaltinių Europa ruošiasi užpildyti rezervines PDS? Ar tik neprisieis dėl to importuoti tas pačias rusiškas dujas?

Pačio paprasčiausio sprendimo Europa ar tai nemato, ar tai nenori matyti: paprasčiausiai nereikia politizuoti energetikos sferą, nekišti pagalius į pačio patikimiausio dujų tiekėjo ratus, neriboti jo konkurencinio pranašumo. Tai yra pats tas atvejis, kai nematomas rinkos ranka pati viską sureguliuos.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 18 — id: `scraped:rubaltic_lt:f15bc3dbf67cec88`

**Title:** Kovotojai su „sovietų okupacija“ Lietuvoje Vilnių palieka be oro uosto

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos susisiekimo ministerija nori nugriauti Vilniaus oro uostą, kadangi jis nuseno ir, iš viso, „sovietų okupacijos“ palikimas. Kalba apie „okupaciją“ reiškia, jog pas pačią Lietuvą pinigų naujam oro uostui nėra, ir ji tikisi jų gauti iš ES struktūrinių fondų postsocialistinėms Rytų Europos šalims. Ar gaus – tai dar didelis klausimas, turint omenyje įtampą ES su pinigais, solidarumu ir dėmesiu Rytų Europai. Gali atsitikti, kad Lietuvos vadovybė Vilnių paliks be oro uosto: seną nugriaus, o naujam nesuras pinigų.

„Man atrodo, atėjo laikas labai aiškiai pasakyti, kad sovietinis okupacinio laikotarpio pastatas neatitinka šiandienos modernios Lietuvos įvaizdžio ir tų funkcionalumų, kurie reikalingi šiuolaikiniam oro uostui. Šį pastatą turėtų pakeisti naujas, modernus oro uostas“, – pastarosiomis dienomis kalbėjo Lietuvos susiekimo ministras Marius Skuodis. Kalbama apie Vilniaus oro uostą, kurio pagrindinis pastatas buvo pastatytas 1954 metais ir yra stalininio ampyro paminklas. Antrasis oro uosto terminalas buvo statomas 1980-aisiais metais ir perduotas eksploatuoti jau po to, kai Lietuva išėjo iš TSRS sudėties. Trečiąjį Vilniaus oro uosto terminalą Lietuva gavo jau būdama ES sudėtyje.

Klausiama, dėl ko reikėjo prie įprasto infrastruktūrinio projekto prikabinti ideologiją, ir vietoje paprastų žodžių apie tai, jog senus oro uosto terminalus ir pakilimo-nutūpimo takus reikia keisti, užvirti košę apie „sovietų okupaciją“ ir Lietuvos įvaizdį? Dėl ko Marius Skuodis iš savęs daro pajuokos objektą?

Bet jei griauti Vilniaus oro uostą, kaip „okupacijos paveldą“, tai tada reikia griauti ir Lietuvos Seimo pastatą, ir Vyriausybės rūmus. Jie gi taip pat pastatyti „okupacijos“ laikais.

Ko dar ten?

Tai bus tiksli lietuviškos ideologijos seka. Ji gi smerkia Molotovo – Ribentropo paktą ir, po to sekusį, sienų pasikeitimą Rytų Europoje laiko jo tiesioginiu padariniu. O Vilniaus perdavimas į Lietuvos sudėtį – tai tiesioginė Raudonosios Armijos žygio į Lenkiją, Maskvos ir Kauno savitarpio pagalbos sutarties ir įvedimo į Lietuvą tarybinio karinio kontingento pasekmė.

Tai dėl ko Lietuvos susisiekimo ministerijos vadovas taip save gėdina? Paprasčiausiai, dėl kvailumo? Viskas žymiai gudriau. Lietuva nėra įpratusi infrastruktūrinius projektus realizuoti savo kaštais. Sovietų laikais kelius, stotis, oro uostus jai statė „okupantai“, o paskutiniuosius 16 metų stato Europos Sąjunga. Infrastruktūra, statyba – tai tos sferos, kurioms visų pirmą skiriamos struktūrinių ES fondų dotacijos.

Prie ko čia okupacija? Prie to, jog struktūriniai ES fondai (Susibūrimo fondas, regioninės plėtros fondas ir kiti) buvo kuriami buvusių socialistinių valstybių infrastruktūriniam atsilikimui įveikti ir jų jungimuisi su likusia Europa. Todėl, jei reikalingi pinigai, Briuselio valdininkams reikia aiškinti apie sunykusius „sovietų okupacijos periodo“ paminklus.

Kitas klausimas, ar Lietuva gaus iš ES fondų reikalingus pinigus? Paskutiniaisiais pusantrų metų Briuselyje visiškai viskas blogai ir su pinigais, ir su solidarumu, ir su dėmesiu į tai, kaip „Naujoji Europa“ įveikia socialistinio periodo pasekmes.

Bet ir anksčiau buvo ne ką geriau. Ignalinos AE Lietuva uždarė – naujai „demokratiniai“ AE pinigų jai Europa nedavė. Independence SGD terminalą Lietuva įsivežė savo sąskaita –finansuoti jo funkcionavimą Europa atsisakė.

Ir tuo stebėtis nereikės. Dabar gi valdžioje tie patys konservatoriai, kurių, prieš tai buvusi vyriausybė nukirsdino, auksinius kiaušinius dedančią vištą – Ignalinos AE. Žmonės, kurie sugeba iš pagrindinio elektros energijos eksportuotojo regione paversti Lietuvą pagrindiniu jos pirkėju, sugebės ir Lietuvos sostinę palikti be oro uosto. Nepasiekdami geresnio rezultato teisinasi tuo, jog už tai dabar su „okupacijos paveldu“ tiksliai viskas baigta.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 19 — id: `scraped:rubaltic_lt:44ee5f9049248bf9`

**Title:** Lietuva pati iš savęs atima naujausias Kinų technologijas

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos valstybės institucijoms verta atsisakyti naudotis kinų gamintojų Huawei ir Xiaomi išmaniaisiais įrenginiais. Apie tai pareiškė respublikos gynybos viceministras Margiris Abukevičius, remdamasis neseniai atliktais Nacionalinis kibernetinio saugumo centro (NKSC) tyrimų rezultatais. Draudimą naudotis kinų brendo produkcija tokiame ar šiokiame pavidale Lietuva bandys „pratempti“ ir per Europos Sąjungą.

„Buvo pasirinkti trys Kinijos gamintojai, kurie nuo praėjusių metų Lietuvos vartotojams siūlo įsigyti 5G mobiliuosius įrenginius ir kurie, tarptautinės bendruomenės buvo įvardinti, kaip keliantys tam tikras kibernetinio saugumo rizikas“, ,- sakė Margiris Abukevičius.

Kalbama apie Huawei, Xiaomi bei OnePlus. Suprantama, Lietuvos ekspertų tyrimu skaitmeninio saugumo sferoje objektu tapo išimtinai tik kinų įrenginiai. Turint noro, į „įtartinų“ gamintojų sąrašą NKSC galėtų įtraukti ir, pavyzdžiui, Apple. Neseniai pati kompanija paskelbė apie pažeidžiamumą, kuris leidžia kontroliuoti jos įrengimus, apeinant vartotojo veiksmus (ir telefonus, ir planšetes, ir kompiuterius su MacOs operacine sistema).

Tyrimu rezultatai buvo prognozuojami: NKSC išaiškino keturias „esmines kibernetinio saugumo rizikas“. Trys „rizikos“ – pas Xiaomi, viena – pas Huawei. Tik OnePlus produkcija, kuri nėra dominuojanti pasaulinėje išmaniųjų telefonų rinkoje, sėkmingai praėjo Lietuvos specialistų tikrinimą.

Pasirodo, Xiaomi Mi 10T 5G įrenginyje yra įdiegta techninė galimybė vykdyti į jį atsisiunčiamo turinio cenzūrą, kuri reaguoja į 449 raktažodžių sąrašą: Longing Taiwan Independence („Tegyvuoja Taivanio nepriklausomybė“), Voice of America („Amerikos balsas“), („Išlaisvinkite Tibetą“) ir kiti.

Nuostabus sutapimas: šį modulį Xiaomi įrenginyje aptiko, būtent tos šalies atstovai, kuri, palaikydamas Taivanį, sugadino santykius su Kinija. Kaip sakoma, kas ieško, tas visada suranda. Mūsų skaitytojai iš Lietuvos bei kitų ES šalių gali paimti savo Xiaomi išmaniuosius telefonus ir patikrinti NKSC išvadų patikimumą. Tada jie pamatys, jog kinų gamintojai jiems nedraudžia nei pritarti Taivanio nepriklausomybei, nei raginti išlaisvinti Tibetą.

Reikalas tame, kad cenzūros mechanizmai Europos Sąjungos teritorijoje, esą išjungti. Bet Xiaomi bet kuriuo momentu gali jį įjungti.

Tas pats išmaniojo telefono modelis NKSC ekspertams atskleidė dar vieną šiurpę paslaptį: kiekvieną kartą, pajungus įrenginį į Xiaomi Cloud debesiją, įrenginys slapta nuo naudotojo siunčia į Xiaomi serverius užšifruotas SMS žinutes. Lietuviai kol kas nesugebėjo jų iššifruoti (dar keletą mėnesių galima dirbti biudžeto pinigų sąskaita).

Trečioji rizika slepiasi Xiaomi – Mi Browser naršyklėje. Jos pagalba Mi 10T, jei tikėti Lietuvos specialistams, duomenys apie įrengimą yra perduodami į serverius Kinijoje.

„Mūsų vertinimu tai yra tikrai perteklinė informacija apie vartotojo veiksmus. Riziką kelia ir faktas, jog ši gausi statistinė informacija šifruotu kanalu siunčiama ir saugoma „Xiaomi“ serveriuose trečiose šalyse, kur negalioja Bendrasis duomenų apsaugos reglamentas“.

Būtent kokia informacija? Apie tai NKSC kažkodėl tai nutyli.

Visų pirmą Margiris Abukevičius kreipėsi į savo kolegas – valdininkus: „Mes identifikavome virš 200 valstybės institucijų, kurios yra tokius telefonus įsigijusios. Iš viso – virš 4,5 tūkst. telefonų, tai, mūsų manymu, didina rizikas ir šias problemas reikia spręsti. (...) Mūsų raginimas – jau dabar pagalvoti apie tai, kad nebepirkti naujų kinų gamintojų telefonų. Ir trumpiausiu metu jų atsisakyti“ Tolimesnis karo su išmaniaisiais telefonais vektorius taip pat nustatytas. Abukevičius išreiškė viltį, jog Seimas pritars įstatymo projektui, draudžiančiam valstybės institucijom pirkti kibernetiniam saugumui rizikingą įrangą.

Jie tai dar nežino, kad bet kuriuo momentu Xiaomi gali uždrausti jiems pritarti Taivanio nepriklausomybei.

Lieka tik spėlioti, kodėl gigantiškos kinų korporacijos – vienos iš vedančiųjų pasaulio išmaniųjų telefonų gamintojos paslaptis atskleidė mažos Pabaltijo valstybės Gynybos ministerijos pareigūnai. Kas tie genijai? Kodėl iki šiol jie neskaito paskaitas Pentagone?

Visiškam vaizdo papildymui visgi verta atsižvelgti į sensacingo NKSC tyrimo kontekstą. Lietuva aktyviai veikė prieš Huawei kompaniją, kaltindama ją nesankcionuotų informacijos apie naudotojus rinkimu. „Tėvynės Sąjungos – Lietuvos krikščionių demokratų“ (TS-LKD) partijos deputatai siūlė paruošti rekomendacijas „atsakingoms institucijoms“ dėl išimtinai ES ir NATO šalyse paruoštų technologinių ryšio produktų naudojimo.

Jei mes įstatymiškai neapribosime, mūsų pirkimų sistema veiks įprastu režimu – mes ieškosime pačio pigiausio tiekėjo. Tačiau realybė tokia, jog ne patys patikimiausi tiekėjai visada siūlo pigiausią ir prieinamą įrangą“, - sakė Lietuvos Gynybos ministras Arvydas Anušauskas. Jam vadovaujant veikia tas pats Nacionalinis kibernetinio saugumo centras, kuris pasaulyje pirmas aptiko Xiaomi produkcijos “nesaugumą”.

Pagaliau, visai neseniai, garsiai pasisakė Lietuvos Seimo Užsienio reikalų komiteto vadovas Žygimantas Pavilionis.

Šiuo remiasi visa, prieš Kiniją nukreipta, Lietuvos politika: ne tik „pridergti“ Pekinui, bet ir paskui save patraukti visą likusį vakarų bloką.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 20 — id: `scraped:rubaltic_lt:e26c8760d8de0478`

**Title:** Rekordinės dujų kainos veda link  komunalinių maištų Pabaltijyje

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Ateinanti šildymo sezono pradžia Pabaltijo šalims tampa vis grėsmingesnė. Latvijos ir Lietuvos vadovybė perspėja gyventojus apie neišvengiamą komunalinių tarifų didėjimą, kartu su tuo, kad atskirais atvejais jie padidės daugiau nei pusantro karto. Rekordinės dujų kainas Europoje papildomai stimuliuoja protestų nuotaikos Baltijos šalyse, o jau pradėti bandymai dėl susiklosčiusios situacijos apkaltinti Rusiją nepadeda: užsienio politika tik labiau piktina žmones.

Lietuvos Valstybinė energetikos reguliavimo taryba perspėjo lietuvius, jog naujame sezone šildymas brangsta 30 procentų.

Tai vidutiniškai visai Lietuvai. Atskiruose savivaldybėse dar blogiau. Sostinėje Vilniuje mokestis už šildymą padidės 60 procentų. Reguliavimo tarybos atstovas Matas Taparauskas tai paaiškina tuo, jog Vilniaus komunalinės tarnybos gamtinių dujų naudoja žymiai daugiau nei likusieji miestai.

Komunalinių tarifų didėjimas laukia ir kaimyninę Latviją. Rygoje mokestis už šildymą jau padidintas 27 procentais ir laukiamas sekantis padidinimas – 15 procentų.

„Rygoje artimiausiu metu padidės šiluminės energijos kainos, kadangi dramatiškas gamtinių dujų kainų didėjimas tęsiasi ir jos jau pakilo dešimt kartų, palyginus su praėjusių metų vasarą“, - sako Latvijos sostinės šilumos tiekimo tarnybos Rīgas siltums vadovas Normundas Talcis.

Analogiškai kalbama ir Lietuvoje .

Tokiu būdu, situacija darosi grėsminga.

„Dujų krizė įmanoma. Bet aš tikiuosi, Jog Europos komisija, kartu su (ES)

šalimis – nariais išspręs šį klausimą, ir pas mus nebus to, kas buvo daugiau kaip prieš 10 metų, kai Europoje buvo sutrikimai, o daugelyje šalių, netgi žiemos viduryje, nebuvo dujų“, - pareiškė Lietuvos energetikos ministras Dainius Kreivys.

Energetikos ministerijos vadovas, tradiciškai Pabaltijo veikėjams, visas problemos sprendimo viltis sieja su Europos Sąjunga ir taip pat tradiciškai įžiūri Rusijos intrigas bet kokių sunkumų užnugaryje. Kreivio nuomone, kainų didėjimą iššaukia dujų apimčių sumažėjimas Europoje, o sumažėjimą, savo ruožtu, iššaukia „ Rusijos bandymas kaip galima greičiau nutiesti antrąją dujų vamzdyno linija („Šiaurinis srautas – 2“) Baltijos jūros dugnu į Vokietiją“. Standartinis bandymas išnaudoti rusofobiją, kaip atsakomybės už problemą perkėlimo instrumentą, šiuo atveju rodosi jau visiškai absurdišku.

Todėl, kad dabartinės anomalijos ES dujų rinkoje priežastys yra akivaizdžios visiems, bet ne šizofrenikams iš Rytų Europos. Pasaulis išeina iš pandemijos, pasaulio ekonomika – iš 2020 metų krizės, griuvimo vyksta atsistatomasis augimas, o tam reikalinga energija. Pačias didžiausiais kainas už energiją siūlo Pietryčių Azija – pasaulio ekonomikos regionas-centras – atitinkamai, dujų tiekėjai visų pirmą savo žvilgsnius nukreipia į tą pusę.

Rinką Europa domina (ypač SGD, suskystintų gamtinių dujų rinką) pagal liekamąjį principą, kartu su tuo, jog Europos dujų saugyklos ištuštintos dėl anomaliai šaltos žiemos (šildymas) ir karštos vasaros (kondicionavimas). Dėl to Europoje dujų kaina ir viršija 800 dolerių už kubinį metrą.

Dėmesio, klausimas: būtent kas dešimtimis metų Europoje tuo užsiiminėjo? Kas Briuselyje rėmė Trečiąjį energetikos paketą? Kas agitavo ES sąjungininkus už amerikietiškas SGD, kurios dabar pasitraukė į Pietryčių Aziją? Kas iki šiol reikalauja atsisakyti „Šiaurinio srauto – 2“?

Lietuva ir Baltijos šalys.

Anksčiau joms rusiškų dujų Europoje buvo per daug, dabar gi - per maža. Ir gyventojai, kuriems dešimtmečiais buvo kalbama apie „energetinę nepriklausomybę“ nuo Rusijos, dabar klausosi kalbų, jog naujos šildymo kainos – dėl „Šiaurinio srauto – 2“ paleidimo.

Idant neleisti dujų krizės, reikia, tikriausiai, įvesti naujas sankcijas Rusijai ir sumažinti „Šiaurinio srauto – 2“ pralaidumą. Arba iš viso uždrausti tiekti dujas tokiu „Putino hibridinio ginklu“, kaip vamzdynai. Toks poveikis Rusijai tikrai užpildys Europos saugyklas ir numuš dujų kainas.

Jei rimtai, tai dabartinės rekordinės kainos smogia į ES energetinės politikos, kuri paskutiniaisiais 20 metų kuriama remiantis, nukreiptu prieš Rusiją, pagrindu, pamatus.

Tam pačiam Pabaltijui tokia situacija – papildomas stimulas žmonėms išeiti į gatvę, po to kai jie gaus naujas mokėjimo už šildymą sąskaitas.

Pabaltijyje protestai palaipsniui jau tampa kasdienybės dalimi. Vilniuje ir Rygoje kiekvieną mėnesį susirenka daugiatūkstantiniai Lietuvos ir Latvijos vadovybių priešininkų mitingai. Taip kad nepasitenkinimas tarifais papuola į maitinamą terpę.

Ir paaiškinti situaciją objektyviais faktoriais (o tuo labiau „Rusijos hibridiniu karu“) nebus galima.

Taip kad Pabaltijį laukia komunaliniai maištai.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```
