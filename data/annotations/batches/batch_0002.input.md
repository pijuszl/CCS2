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

### Article 1 — id: `scraped:rubaltic_lt:9734fe57e4501c50`

**Title:** Lietuviai sužlugdė pergalės dienos prieš „sovietų okupantus“ šventimą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos valstybė pradėjo baimintis susitikimų su savo tauta.  Po to, kai metinių susirėmimo prie Vilniaus televizijos bokšto proga mitinge buvo nušvilpti vyriausybės nariai, valdžia tikisi, kad minia tokiu pat būdu sužlugdys ir kitas Lietuvos valstybės šventes. Valdančiųjų konservatorių populiarumo griūtis, kuri iki šiol buvo išreiškiama sociologų paskaičiuotais paramos procentais, dabar išreikiama pačios pasigailėtiniausios naujojoje Lietuvos istorijoje vyriausybės viešąją gėda.

Kruvina  1991 metų sausio mėnesio 13 nakties provokacija prie Vilniaus televizijos bokšto Lietuvoje vadinama Laisvės gynėjų diena ir, tų, kurie tą provokaciją organizavo, yra minima kaip valstybės šventė.

Eilines sausio 13 metines Lietuvos valdžia nusprendė paminėti surengiant iškilmingą mitingą, ir Vilniaus centrinėje aikštėje surinko tūkstančius lietuvių. Tai, tarp kitko, dar vienas patvirtinimas, kad dabartinė Lietuvos vyriausybė –talentinga alternatyviai, kas jau seniai tapo aišku ir lietuviams, ir stebėtojams iš už Lietuvos ribų.

Nepriklausomybės aikšte, kurioje buvo numatyta priemonė, turėjo priminti organizatoriams apie vasaros neramumus, kai tūkstančiai nepatenkintųjų susirinko greta Seimo pastato, o paskui bandė blokuoti jame esančius valdančios konservatorių partijos deputatus. Per praėjusį pusmetį sociologai nefiksavo tautos meilės „landsbergistam“ didėjimo – tik tolimesnį jų populiarumo mažėjimą. Galimai, akcijos organizatoriai galvojo, kad sakralinė sausio 13 data suvienys valdžią su tauta?

Be reikalo.

Oficiali žiniasklaida delikačiai aprašė šį nepatogų įvykį: sausio 13 mitinge buvo girdimas ne vien tik pritarimas. Valdantieji politikai  paskelbė, kad į Lietuvos patriotų gretas įsismelkė keletas antivalstybinių provokatorių.

Tačiau skleisti melą visuotinio informacinio skaidrumo ir visuotinio prieinamumo prie informacijos epochoje beprasmiška. Įvykių vaizdo įrašą vienu mygtuko nuspaudimu gali pasižiūrėti kas tik nori: šiame vaizdo įraše aiškiai matosi, kad „gėda“ valdžios atstovams tribūnoje skanduoja visa daugiatūkstantinė minia ir jiems nešdintis reikalauja toli gražu ne keletas provokatorių.

Valdančių lageryje kilusią isteriką galima apibūdinti dvejomis citatomis.

„Įsijungiau transliaciją iš aikštės prie Seimo. Visi, kurie ten esate ne dėl sausio 13 aukų pagerbimo, o dėl protesto prieš valdžią – jūs esate penktoji Rusijos kolona, naudingi idiotai ir visuomenės vėžys“, - pareiškė Vilniaus mero patarėjas Karolis Žukauskas visiškai atitikdamas lietuviško juoko „Kremliaus ranka privarė man į kelnes“ esmę.

„Kokie čia žmonės, čia jedinstvo. Nereikia jų vadinti Lietuvos žmonėmis – fašistai, jedinstvo. Problema, žinoma. Pamišėlių pakankamai daug.Anais laikais jedinstvos mitingai būdavo atskirai ir, kai vieną kartą čia buvo prie Seimo du mitingai, aš išėjau ir prašiau žmonių, kad tik nesiartintų prie jų, tegul jie sau rėkia, ką nori, o mūsų gyvenimas eina savo keliu“, - atsigavo nuo šoko ir pradėjo kliedėti pagrindinis šventės herojus, nusenęs „tautos tėvas“ Vytautas Landsbergis. Būtent jis 1991 metais vadovavo judėjimui už Lietuvos nepriklausomybę ir ragino žmones savo kūnais apginti prieigas prie Vilniaus televizijos bokšto, dėl ko buvo užmušta 14 žmonių.

Pagrindinio kruvinos provokacijos prie televizijos bokšto organizatoriaus šokas suprantamas.

Anksčiau apie tai buvo galima kalbėti tik remiantis sausais sociologų duomenimis, pagal kuriuos valdančiųjų „landsbergistų“ („Tėvynės Sąjunga – Lietuvos krikščionys demokratai“) reitingai siekia vienaženklį skaitmenį, o URM vadovo Gabrieliaus Landsbergio, kurį jo senelis, „tautos tėvas“ svajoja pasodinti į prezidento kėdę, veiklą remia 3 % lietuvių. Dabar lietuviai pademonstravo savo tiesioginį požiūrį į Landsbergių šeimynėlę bei jų partiją.

Kad neleisti tam atsitikti, „šventos datos“ išvakarėse valdžia ėmėsi precedento nuturinčių saugumo priemonių, aikštėje priešais parlamentą tarp tribūnos ir minios išskyrė plačią tuščią „saugumo erdvę“. Niekas nepagelbėjo. Kaip tai buvo vasarą, su kumščiais savo „elito“ lietuviai nepuolė, bet balsu aiškiai davė suprasti, ką jie galvoja apie ją.

Po šios traumos jie jau nervuojasi, kad Kremliaus agentai jiems sužlugdys ir sekančią eilinę šventę: vasario 16 Lietuvos nepriklausomybės dieną ir kovo 11 nepriklausomybės atkūrimo dieną. Bet vienintelė priemonė išvengti susitikimo su „antivalstybiniais elementais“ – išvengti susitikimo su visais lietuviais.

Taip, kad daugiau jokių bendrų su lietuviais priemonių, švenčiant valstybės šventes! Lietuviai tegul švenčia patys sau, o valdžia – pati sau. Ji ir taip seniai jau gyvena dvejuose skirtinguose pasauliuose – tokia praktiką reikią sutvirtinti doktrina.

Be tautos Lietuvos „elitui“ gyventi bus lengva ir patogu.

Niekas neprimins teismo medicinos ekspertų parodymus apie tai, jog prie Vilniaus televizijos bokšto užmuštųjų kūnuose įstrigusios kulkos lėkė ne iš sovietų karių pusės, o nuo gretimų namų stogų. Niekas nepaklaus, kokiu būdu galėjo žūti televizijos bokšto gynėja nuo to, kad ją pervažiavo tankas, jei po jos mirties jos kūne nebuvo nei vieno sulaužyto kaulo? Niekas nepacituos  atvirus „Sajūdžio“ smogikų vadovo Audriaus Butkevičiaus pasisakymus, jog susirėmime su SSSR jis užtikrino Lietuvai moralinę pergalę, įsakęs pralieti kraują, kad vakarų žiniasklaidai pateikti šiurpų vaizdą.

Juolab, lietuvių nebuvimas žymiai palengvins Lietuvos vyriausybės gyvenimą. Galima „suturėti“ Rusiją, kovoti su Kinija ir savo kompanijomis, kurios perka kinų prekes, geležinkeliui drausti gabenti baltarusiškus krovinius ir palikti be darbo tūkstančius žmonių. Ir niekas nešūkaus mitinge, neįžeidinės ir nebadys akių užsienio reikalų ministrui ir pačio „tautos tėvo“ anūkui, kurį senelis parinko būti nauju prezidentu, tuo, kad jo veiklos pritarimo reitingas – 3%.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 2 — id: `scraped:rubaltic_lt:04750f6a37db2319`

**Title:** Lenkija parduos Pabaltijui „energetinės nepriklausomybės“ nuo Rusijos iliuziją

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lenkija ir Lietuva užbaigė regioninio dujotiekio GIPL statybą. Kaip ir daugelis energetikos projektų Rytų Europoje, dujotiekis pastatytas už Europos sąjungos pinigus, siekiant užtikrinti „energetinę nepriklausomybę nuo Rusijos“ ir ekonomikos požiūriu absoliučiai beprasmiškas. Šio projekto esmė tame, kad Pabaltijo politikai už savo daugiametes grumtynes su “Kremliaus dujų vėzdu“ mokės Lenkijai iš Lietuvos, Latvijos ir Estijos biudžetų, pirkdami visgi rusiškas dujas, bet tik dar brangiau.

Dujotiekio GIPL statyba oficialiai buvo grindžiama sekančiai: „ Šiuo metu Baltijos šalys nepakankamai diversifikuotos dujų tiekimo maršrutų atžvilgiu ir visiškai priklauso nuo vienintelio gamtinių dujų tiekėjo, o būtent nuo Rusijos. Sujungimas su ES dujų rinka gali žymiai padidinti dujų tiekimo saugumą šioms valstybėms- ES narėms“.

Apie dujotiekio ekonomiką, naudą, atsipirkimą, rentabilumą šiame pagrindime nieko nesakoma. Europos sąjunga skyrė lėšas griežtai politiniam Pabaltijo dujų transportavimo sistemos sujungimo projektui su Lenkija, o per Lenkija – su visa ES dujų transportavimo sistema.

Kokie variantai čia yra galimi? Pirmas ir pats paprasčiausiais – plačiai nuskambėjęs reversas. Lenkija pati vartoja Gazpromo produkciją –nauju dujotiekiu ją galės nukreipti ir į Pabaltijo šalis. Suprantama, su antkainiu už tranzitą ir politinę priedangą, kad, remiantis dokumentais, dujos nėra rusiškos, jos lenkiškos.

Kitas variantas – GIPL vamzdynu lenkiško SGD terminalo Svinoustėje produkciją tiekti į Pabaltijį. Taip ir buvo numatoma projektuojant šį, jungiantį Lietuvą su Lenkiją, dujotiekį.

Čia kyla iš karto du klausimai. Visų pirmą, tada kodėl Lietuva Klaipėdoje įrengė savo SGD terminalą Independence? Sekant Lietuvos politikų logika, tiekimas jau diversifikuotas ir “energetinė nepriklausomybė“ nuo Rusijos jau įgyta.

Tai antras klausimas. Baltijos jūros regione vartojamos suskystintos gamtinės dujos (SGD) daugiausiai yra rusiškos kilmės. Rinkoje jos pačios pigiausios ir jas lengviausia atgabenti.

Ta pati Lietuva, kuri Klaipėdoje iškilmingai atidarė savo SGD terminalą, praėjus vos keliems metams, gėdydamasi ir, pradžioje netgi slaptai, pradėjo užpirkinėti jo užpildymui rusiškas suskystintas dujas. Kadangi amerikietiško ir norvegų SGD projektas nėra pakeliamas, kartu su tuo, kad ir rusiškos SGD yra brangesnės už rusiškas vamzdyno dujas.

Lenkai, žinoma, gali iš „geros valios“ tiekti į Pabaltijį griežtai norvegiškas dujas, kurias Lenkija ketina gauti dujotiekiu Baltic Pipe. Bet! Visų pirma – tai ilgalaikė statyba, kuri iki šio laiko nebaigta. Antra, Norvegijos dujų telkiniai senka. Trečia, norvegų vamzdyno dujų kaina Lietuvai su likusiomis „Baltijos seserimis“ bus nepakeliama, kaip joms nėra pakeliama ir norvegų SGD kaina.

Taip, kad viskas eina link klasikinės situacijos.

Kiekvienu tokiu atveju yra tretysis džiaugiantysis, kuriam yra naudinga absurdiška Pabaltijo politikų rusofobija. Dujotiekio GIPL atveju tai - Lenkija. Būtent lenkai gaus Vilniuje, Rygoje ir Taline valdančių režimų rusofobijos dividendus, kurie energetinės krizės ir be galo aukštų komunalinių paslaugų tarifų sąlygomis iš biudžeto bus mokami už iliuziją, jog jie išgelbėjo Lietuvą, Latviją ir Estiją nuo Rusijos monopolijos energetikos srityje.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 3 — id: `scraped:rubaltic_lt:312a9a4480450130`

**Title:** Lietuvą laukia šimtų milijonų eurų dydžio bauda: Vilnius nutrauks kontraktą su „Belaruskalij“

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Susitarimas dėl baltarusiškų kalio trąšų tranzito geležinkeliu per Lietuvos teritoriją bus anuliuotas vasario mėnesio 1 dieną. Apie tai pareiškė Lietuvos transporto ministras Marius Skuodis. Valdininko žodžiais tariant, formaliu to pagrindu taps valstybinės komisijos, tikrinančios strategiškai svarbių įmonių sandorius, išvados. Bet panašus „alibi“ neišgelbės Lietuvą nuo teisminių ieškinių, nei nuo krovinių srauto perorientavimo į kaimyninių šalių uostus grėsmės.

Atėjusiose metuose Pabaltijo šalies grumtynės su „Belaruskalij“, regis, įgijo apkasų karo pobūdį. Ingridos Šimonytės ministrai atsikvėpė ir nusiramino: nei Skuodis, nei URM vadovas Gabrielius Landsbergis neatsistatydino.

Savo pareigų neteko tik „Lietuvos geležinkelio“ (LG) vadovas Mantas Bartuška. Dėl ko – neaišku, užtat dabar valdantieji konservatoriai galės užtikrintai „prastumti“ savo žmogų į kompanijos vadovo postą.

Dar viena istorijos su „Belaruskalij“ auka tapo, dabar jau buvęs, Seimo užsienio reikalų komisijos pirmininkas Žygimantas Pavilionis. „Savo postą palieku todėl, kad politika – darbas komandoje, ir kartais prisieina nusileisti vardan bendro tikslo. Ši politinė bendrija mane iškėlė, kaip politikas buvau jos remiamas ir paskirtas į šias pareigas. Būtu negarbinga nepaklusti jos sprendimui“, - sakė Pavilionis.

Bendrai paėmus, tai galima pavadinti atpildu už pernelyg didelį iškalbumą (patekęs nemalonėn deputatas išdrįso kritikuoti savo bendražygius vyriausybėje už tai, jog tie nesugebėjo įgyvendinti amerikiečių sankcijas „Belaruskaliui“) Nors Pavilionio atsistatydinimas ir taip buvo laukiamas – jam iš paskos seka ilgas skandalų šleifas. Tame trape ir tarptautinių.

Vadovaujantis Nacionalinio saugumui užtikrinti svarbių objektų apsaugos koordinavimo komisijos sprendimui, vyriausybės sprendimu sutartis bus laikoma negaliojančia, kaip neatitinkanti nacionalinio saugumo interesams nuo vasario 1 d.“, - sausio 12 pareiškė Lietuvos transporto ministras.

Kalbama apie sutartį, remiantis kuria, LG teikia „Belaruskaliui“ tranzito geležinkeliu paslaugas.

Kito sprendimo ir negalėjo būti – Lietuvos Ministrų kabinetas, paprasčiausiai ieškojo formalaus pagrindo baltarusiško tranzito sustabdymui (kaip paaiškėjo, JAV finansų ministerijos sankcijos „Belaruskaliui“ to nepagrindžia).

Jei tikėti Skuodžiu, nuo vasario 1 „diktatoriškų“ trąšu gabenimas per Pabaltijo respublikos teritorija bus sustabdytas, kadangi „tam jau nebebus teisinio pagrindo“.

„Tuo atveju, jei Lietuva pažeis tarptautines sutartis, mes išnaudosime visas teisinės apsaugos priemones ir paduosime ieškinius į teismus. Be to, mūsų manymu, į teismus kreipsis ir daugelis mūsų klientų – trąšų pirkėjų, kurie liks be prekių ir patirs žymią žalą dėl Lietuvos veiksmų. Dėl to jie bus priversti pirkti trąšas už aukštesnę kainą. Ieškinių kainos šioje byloje gali siekti milijardus eurų“, - perspėjo oficiali „Belarusijos kalio kompanijos“ („Belaruskalij“ treiderio) atstovė Irina Savčenko.

Lietuvos Seimo nacionalinio saugumo ir gynybos komiteto nieko vertos išvados vargu ar taps atsakovo pateisinimo pagrindu. Netgi premjerė Ingrida Šimonytė puikiai supranta savo pozicijos silpnumą, todėl jį atvirai kalbėjo apie tokių kontrakto nutraukimo būdų paiešką, kurių dėka galima būtų išvengti finansinės žalos valstybei. Bet, kaip matosi, paieška nebuvo sėkminga. Skuodis nieko nepasakė apie tai, kokiu būdu Lietuva atrems „Belaruskailij“ juristų atakas.

Bendrai sakant, Lietuvos Ministrų kabinetą galima pasveikinti eilinio „pasiekimo“ proga: jo politika valstybės biudžetui atsilieps kolosaliais nuostoliais.

Kartu su tuo Skuodis išvardijo apie dešimtį įmonių, kurios galės iš LG perimti baltarusišką tranzitą („realiausios galimybės pas dvejas“), Ar jos yra Lietuvos rezidentais, valdininkas nepatikslina. Greičiausiai kalbama apie kompanijas iš kitų šalių – ES narių – Latvijos, Lenkijos, Estijos. Anksčiau Landsbergis buvo išreiškęs savo susirūpinimą dėl to, jog Lukašenka tęs savo eksportą per kaimyninių šalių uostus. Tarp kitko, Estija jau padidino baltarusiškų naftos produktų, kurie išėjo iš Klaipėdos, tranzitą.

Šią problemą Vilnius bando spręsti ES lygyje. Atkreipkime dėmesį į Svetlanos Tichonouskos pranešimą Telegram kanale po jos susitikimo su Lietuvos prezidentu Gitanu Nausėda: „Tichonouskaja ir Nausėda susitarė tęsti koordinuotą režimo (Aleksandro Lukašenko - RuBaltic.Ru pastaba) spaudimo veiklą. Jie sutarė, jog svarbu užtverti sankcijų spragas ir rasti būdus sustabdyti sankcinių produktų tranzitą per Pabaltijo respublikas, Dabar ES rengia šeštąjį sankcijų paketą“.

Tai padaryti nesunku – gana uždrausti baltarusiškos kilmės trąšų gabenimą per šalių – ES narių uostus (analogiškas draudimas naftos produktams jau veikia). Tada Lietuva gaus garantijas, kad kaimynai negauna pelno jos nuostolių sąskaita.

„Atkreipiu dėmesį, kad JAV dažnu atveju, ypač priimant naujausius sankcijų paketus Europoje, atliepdavo juos praktiškai identiškais paketais Amerikoje. Šiuo atveju turime ryškų išsiskyrimą dėl to, kad Europa yra įvedusi sankcijas tam tikriems trąšų produktams, kurie negali atvykti į ES, o JAV – visam juridiniam asmeniui“, - skundėsi Landsbergis, siūlydamas sinchronizuoti amerikiečių ir europiečių apribojimus Baltarusijos atžvilgiu. Šiame pasisakyme taip pat girdisi užtušuotas raginimas blokuoti „Belaruskalij“ tranzitą visos Europos sąjungos lygyje.

LG ir „Belaruskalij“ susitarimo galiojimas baigiasi 2023 metais. Lietuva galėtų ramiai sulaukti to momento (o geležinkeliui ir Klaipėdos uostui atsirastu laiko, kad pasiruošti neišvengiamam baltarusiško tranzito netekimui). Bet Lietuvos konservatoriai lengvų kelių neieško. Iš visų variantų pasirenka patį idiotiškiausią ir labiausiai apsunkinantį gyventojus variantą.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 4 — id: `scraped:rubaltic_lt:dd747d81f2f1d8ee`

**Title:** Šildymas kreditu: Lietuva lenda į skolas, kad išgyventi žiemą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
„Vilniaus šilumos tinklai“ (VŠT) gaus eilinį 20 milijonų eurų sumos dydžio kreditą. Tokiu būdu kompanijos įsiskolinimo SEB bankui prievolės kirs bauginančią 100 milijonų eurų ribą. Bet ir šių pinigų VŠT nepakaks, kad išgyventi šildymo sezoną: gretutinai vedamos derybos dėl „alternatyvių finansavimo modelių gilėjančios krizės fone“. Skolai apmokėti sotinės šilumos energijos tiekėjas visus metus „melš“ vartotojus arba kreipsis pagalbos į valstybės biudžetą.

Siekiant „amortizuoti“ energijos kainų augimą, parėjusių metų lapkrityje Lietuvos valdžia ėmėsi neatidėliotinų priemonių. Palaimintus rinkos mechanizmus pakeitė „sovietinis“ valstybinis reguliavimas, Seimas revizavo iš karto penkis įstatymus.

Viena iš pataisų numatoma, kad dabar šilumos gamintojai žymią gamtinių dujų dalį gali įsigyti tiesiogiai pas tiekėjus – iki to, ne mažiau 50 % metų poreikio „žydrojo kuro“ jie privalėjo pirkti biržoje. Pusei metų atidėtas nepriklausomo elektros energijos tiekėjo pasirinkimas pusei milijono Lietuvos vartotojų. Šios ir kitos priemonės turi užkirsti kelią nekontroliuojamam tarifų už komunalines paslaugas augimui.

Viso to rezultate, valstybei kontroliuojant, padidėjo tarifai, bet nuo to lietuviams netapo lengviau. 15 tūkstančių neturtingų sostinės gyventojų, gavę sąskaitas už šildymą, kreipėsi kompensacijų. „Ir pagalbos prašytojų gretos padidėjo, ir piniginės išmokos 20 % didesnės nei praėjusiais metais“, - pažymi Vilniaus vicemeras Valdas Benkunskas.

Šalies naujienų portalas „Delfi“ pateikia sekančius duomenis: Justiniškių gyventojai už 50 m 2 ploto būsto apšildymą ir karštą vandenį buvo pateikta 189 eurų sąskaita. 66 kvadratų būsto viename iš Vilniaus rajonų apšildymas apsieis 170 eurų.

„Žymiai pabrango dujos, kas tapo išlaidų padidėjimo priežastimi. Jei paimti seną 50 kv.m. ploto būstą, tai praėjusį sezoną gyventojai mokėjo 40 eurų, o dabar 123 eurus. Priežastis – dujų pabrangimas 7 kartus, plius gruodyje buvo 3,5 laipsnio šalčiau, negu užpraeitais metais“, - aiškina AB „Vilniaus šilumos tinklai“ klientų aptarnavimo skyriaus atstovas Laurynas Jakubauskas. Sausyje ir vasaryje dujų kainos nemažės, o oro temperatūra žada nukristi keliais laipsniais. Todėl Vilniaus gyventojams verta būti pasiruošusiems dar didesnėms išlaidoms.

Vyriausybė šia problemą siūlo spręsti dvejais būdais. Neturtingiems, kaip tai buvo paminėta, numatytos kompensacijos iš valstybės biudžeto. Socialinės apsaugos ministerija tikina, jog pinigų pakaks (ten numatė būsimą „prašytojų“ skaičiaus didėjimą). Likę gali susitarti su kompanija – šilumos energijos tiekėju dėl skolos išmokėjimo atidėjimo.

Kažkam toks variantas gali pasirodyti patraukliu. Įprast, žmogus kas mėnesį gauną fiksuotą atlyginimą už darbą arba pensiją, bet žiemą už komunalines paslaugas prisieina mokėti žymiai daugiau negu vasarą. Kodėl gi šį mokestį nepaskirstyti tolygiai? Skamba logiškai, tačiau VŠT klientams verta paieškoti atsakymą į tokį klastingą klausimą: kokia situacija susidarys pasibaigus žiemai?

Jau visiems aišku, jog pavasarį gamtinių dujų kainos negrius. Šildymo sezoną Europa baigs su rekordiškai mažomis atsargomis požeminėse saugyklose – iš karto bus pradėta rengtis sekančiai žiemai. “Šiaurinio srauto-2“ paleidimo vilkinimas garantuotai laikys aukštas „žydrojo kuro“ kainas.

Situacija blogėja dar ir tuo, jog „Vilniaus šilumos tinklai“ atsidūrė labai sunkioje finansinėje padėtyje.

Prieš keletą dienų jie susitarė su SEB banku dėl eilinio 20 milijonų eurų sumos dydžio kredito. Kompanijoje aiškina, jog nepakanka apyvartinių lėšų: dujų kainų tarifų pokytis galutinius vartotojus pasiekia tik po dvejų mėnesių, o už žaliavą reikia mokėti iš karto. Atsiranda finansinė skylė, kurią VŠT bando užlopyti pačiu paprasčiausiu būdu – kreditais.

Sostinės energijos tiekėjas ir anksčiau buvo kreipęsis į bankus dėl pagalbos. Lapkrityje jau pasiskolino 50 milijonų eurų. Kartu su tuo, rugsėjo 30 dienai ilgalaikiai ir trumpalaikiai VŠT įsipareigojimai SEB bankui sudarė 45,4 milijono eurų.

„2021 m. gruodžio mėn. 21 d. dujų kaina pasiekė 140 eurų už MW/h ir buvo 824% aukštesnė už Valstybinės energetikos reguliavimo tarybos nustatytą (17 eurų už MW/h). Būtinų apyvartinių lėšų užtikrinimui VŠT susitarė su SEB banku dėl 20 milijonų eurų kredito. Tų lėšų turi pakakti darniai kompanijos veiklai sausyje, bet tuo pačiu metu ieškoma galimybių gauti paramos instrumentų ir užsitikrinti alternatyviais finansavimo modeliais gilėjančios krizės fone“, - pažymi „Vilniaus šilumos tinklų“ finansų direktorė Ras Gudė.

Tikriausiai, jau po mėnesio kompanijai teks vėl ieškoti „finansinio“ maitinimo šaltinį. Bet pagrindinis klausimas tame, kokiu būdu ji apmokės susidariusią skolą. Negalima atmesti, jog pavasarį VŠT pareikš maždaug taip: „Šildymo sąskaitos pasirodė nepagristai žemos, nemokėtojų skaičius staigiai padidėjo. Mums nepakaks pinigų, kad atsiskaityti su banku“.

Kokia išeitis iš šios situacijos?

Valstybė parems – neskelbti gi sostinės šilumos tiekėjo bankrotu! Kaip bebūtu, bet kokie bandymai sutaupyti šildymo sezono metu galų gale pasireikš papildomomis išlaidomis. Ir dar su palūkanomis.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 5 — id: `scraped:rubaltic_lt:bc993f08d1903ea5`

**Title:** Mes kovojame su Kinija, kad išgelbėti Ukrainą: Lietuvos valdžia puolė į marazmą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos išprovokuotas konfliktas su Kinija, padeda apginti Ukrainą nuo „rusiškos agresijos“. Tokia nuomonę išreiškė Europos parlamento narys, Pabaltijo respublikos ekspremjeras ir vienas iš valdančios Tėvynės sąjungos – Lietuvos krikščionių demokratų (TS-LKD) partijos „garbės veteranų“ Andrius Kubilius. Jo žodžiais tariant, karas Ukrainoje bus lydymas Kinijos bandymu užgrobti Taivaną, ir „jei demokratijos pralaimės viename susidūrime, jos, greičiausiai, pralaimės ir kitame“.

Sausio 10 Lietuvos nacionalinė radijo ir televizijos kompanija (LRT) paviešino išplėstą Andriaus Kubiliaus straipsnį, kuriame jis „duoda velnių“ Lietuvos užsienio politikos kritikams.

Buvusi premjerą piktina kalbos apie tai, kad „berniukai iš URM“, esą, elgėsi neatsakingai, kai erzino kinų drakoną.

„Kita vertus, pats laikas yra sistemiškiau susidėlioti racionalius argumentus, kodėl Kinijos reakcija į Lietuvos veiksmus yra klaidinga ir kodėl Lietuvos veiksmai yra racionalūs bei toliaregiški, rašo Kubilius. - Nenoriu plėtotis į ilgus apibendrinimus apie „vertybinės politikos“ ilgalaikę pragmatinę naudą. Šio teksto tikslas – argumentuotomis tezėmis paneigti ir atsakyti į šioje „Kinijos diskusijoje“ pradedančius vyrauti trafaretinius argumentus, o taip pat sudėlioti keletą ilgalaikių akcentų, kurie vis ryškiau matosi bent jau Europos Parlamente“.

Pavyzdžiui, pirmasis “trafaretinis argumentas” jo sąraše skamba taip: “Esame maži ir nieko negalime. Mus Kinija užsmaugs!“

Kokiu būdu autorius paneigia šį argumentą?

„Ir pagaliau pats argumentas, kad „esame maži, o Kinija didelė“ neatlaiko elementarios istorinės Kovo 11–osios logikos (tą 1990 metų dieną buvo paskelbta Lietuvos nepriklausomybė – RuBaltic.RU pastaba). Ir tada buvo tokių, kurie skelbė, kad esame maži, o Sovietų Sąjunga yra didelė. Lygiai taip pat buvo daug visiškos ekonominės katastrofos pranašysčių. Ir ką? Jeigu tada būtume pasidavę tokioms apokaliptinėms pranašystėms, tai ir Nepriklausomybės nebūtume išdrįsę atkurti”, - pareiškia Kubilius.

Ta faktą, kad praėjus vieneriems metams nuo aprašomų įvykių, nepriklausomybes įgijo visos, be išimties, SSSR respublikos, buvęs Lietuvos premjeras kažkodėl tai ignoruoja.

Kubiliaus argumentavime yra vienas ypatingai įdomus momentas. Stengdamasis pateisinti Lietuvos užsienio politiką, jis daro įtartiną išvadą: konfrontacija su Kinija pagelbės apginti Ukrainą nuo „rusiškos agresijos“.

„Nėra sunku prognozuoti, kad esminių susidūrimų bus keletas: vienas iš jų vyks netoli mūsų – dėl Ukrainos, o kitas šiek tiek toliau – dėl Taivano. Silpstantis autoritarinis Kremlius iki paskutiniųjų trukdys Ukrainai tapti sėkminga valstybe; stiprėjanti Kinija savo globalią galią visų pirma projektuos į Taivaną. Šie susidūrimai lems arba demokratinę, arba autoritarinę globalią lyderystę. Demokratijoms pralaimėjus viename susidūrime, jos, greičiausiai, pralaimėtų ir kitame“.

Toliau skaitytojas gali savarankiškai išvystyti Andriaus Kubiliaus mintį

Demokratijos tęsia savo atsitraukimą ir „susitraukimą“. Rytų Europoje triumfuoja prokremlinės jėgos, pasaulio žemėlapyje atsiranda nauja Sovietų Sąjunga. Lietuva praranda patį brangiausią, ką ji turi – nepriklausomybę. Baisus scenarijus, kuriam užkirsti kelią visomis išgalėmis stengiasi „landsbergistai“ O juos už tai dar ir kritikuoja!

Kubiliaus tekstas akivaizdžiai demonstruoja kokie iš tikrųjų yra Lietuvoje valdantys konservatoriai. Jie ne paprasti fanatikai.

Jiems nevalia galvoti apie nacionalinius interesus, todėl, jog nuo jų priklauso pasaulio likimas...

Tegul taip: Lietuva kovoja už tolimą demokratinę šalį, kuriai gresia „kinų agresija“. Pati ši mintis nėra nauja, vakarų ekspertai jau seniai mano, jog KLR Taivano atžvilgiu gali pasinaudoti „Krymo scenarijumi“.

Bet kokiu būdu Lietuva stengiasi neleisti tokiam scenarijui vystytis?

Jei laikytis Kubiliaus logikos, Taivano likimas jau nulemtas – už jį amerikiečiai ir jų sąjungininkai kariauti nesiruošia. Klausimas tame, ar Kinija yra pasiryžusi panaudoti karinę jėgą saloje. Štai čia Lietuva kaip tik ir atlieka provokatoriaus vaidmenį.

Bendrai tariant, sudaryti elementarias priežasties – pasekmių grandines Andrius Kubilius iki savo karjeros saulėlydžio taip ir neišmoko. Už tai jam būdingas kitas „privalumas“: jis yra beribiai atsidavęs savo partijai. Kai „landsbergistų“ kvailystės tampa visiems akivaizdžios, senukas Kubilius vis vien jas teisina.

Čia ir yra būtent toks atvejis.

Pergalės atveju sekančiuose parlamento rinkimuose, opozicija žada normalizuoti santykius su Pekinu. Netgi Lietuvos prezidentas Gitanas Nausėda metų pradžioje atkreipė konservatorių dėmesį į jų nekompetentingumą: „Aš manyčiau, kad ne Taivaniečių atstovybės atidarymas buvo klaida, o pavadinimas, kuris nebuvo derintas su manimi. (...) Pagrindinė kibirkštis buvo labiau dėl pavadinimo, todėl šiuo metu mes turime kovoti su pasekmėmis“. Ar verta stebėtis, jog Kubilius rašo straipsnį gindamas „racionalią bei toliaregę“ Lietuvos užsienio politiką? Kartu su tuo pateikia argumentus, kurie anksčiau nebuvo naudojami.

Ir tik tuo atveju, jei protingų argumentų pas jį jau nebeliko.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 6 — id: `scraped:rubaltic_lt:d046b5d453fccaee`

**Title:** Derybas su Rusija amerikiečiai pradėjo iniciatyvomis dėl Pabaltijo pašalinimo iš NATO

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Derybų su Rusija dėl strateginio stabilumo ir NATO buvimo Rytų Europoje pradžioje stambiose amerikiečių žiniasklaidos leidiniuose daugėja publikacijų apie tai, jog, esant tam tikrom sąlygom, galima būtu „atiduoti“ Putinui Ukrainą ir netgi Pabaltijo šalis. Vašingtonas siunčia Kremliui viešus signalus, jog, leistinos derėjimesi su Maskva ribos yra daug platesnės nei oficialiai pripažįstamos, ir atsakydamos į tam tikrus Rusijos žingsnius, JAV pasirengusios atsisakyti savo satelitų.

„Ukraina, Gruzija (Sakartvelas) bei kitos buvusiuos sovietiškos respublikos – nuostabios, didingos, suverenios šalys. Kaip mes jas nebegerbtume, bet mokslinės, pramoninės ar ekonominės galios požiūriu jos nėra pagrindinės strateginės pasaulio zonos. Tai ne tos vietos, į kurias karo atveju mes turime būti pasiruošę kovai ir mirčiai pasiusti amerikiečių karines pajėgas. Mums reikia surasti įvairius Ukrainos, Gruzijos (Sakartvelo) bei kitų neutralių Rytų Europos šalių gynybos būdus, numatančius kokį tai ilgalaikį neutraliteto arba neprisijungimo variantą“, - praeitų metų pabaigoje buvo rašoma prestižiniame amerikietiškame leidinyje USA Today.

Todėl jog „koks tai ilgalaikio neutraliteto arba neprisijungimo variantas„ – tai yra tai, ko siekia Kremlius, Rusijos vadovybė niekada nebuvo pareiškusi amerikiečiams, jog Ukraina – neatskiriama Rusijos dalis, ir ji turi būti RF sudėtyje, arba, mažiausiai, tapti Kolektyvinio saugumo sutarties organizacijos (KSSO) nariu.

Rusijos reikalavimas – Ukrainos karinis neutralumas. Neutralios juostos tarp NATO ir Rusijos išsaugojimas. Amerikiečiu kariuomenė neturi būti dislokuota greta Belgorodo, kuris nuo Maskvos randasi keleto valandų trukmės kelionės atstumu. Štai ir viskas.

Spėliojimai apie „imperines ambicijas“, apie tai jog Putinas „atgaivina SSSR“, reikalingi tik tam, kad užplepėti klausimo esmę. Priešingu atveju prisieis pripažinti, jog Maskvos reikalavimai yra pagristi.

Kitas reikalas, kad vien tik Ukraina kalba apie RF vakarinių sienų strateginį saugumą nesibaigia. Pabaltijo šalys jau NATO sudėtyje, Aljanso kontingentai ten jau dislokuoti, ir metai iš metų kuriama infrastruktūra, kuri pačiu trumpiausiu laiku leidžia gerokai padidinti NATO pajėgas Lietuvoje, Latvijoje ir Estijoje.

Amerikiečių raketos palei Taliną Rusijai bus ne kiek geresnės už amerikiečių raketas palei Charkovą. Nuo Estijos sienos iki Sankt-Peterburgo galima nusigauti per tris valandas, ir NATO kariškiai jau daugelį metų organizuoja demonstratyviai - parodomuosius paradus Narvoje.

„ [NATO ir Rusijos susitarimo] Nuostatose numatyta garantija, kad ..... JAV ir NATO balistinės rakėtos nebus dislokuotos Rytų Europoje. Rusijos siūlomo susitarimo dėl saugumo nuostatoje sakoma, jei JAV įsipareigos neleisti tolimesnės NATO plėtros į rytus ir atsisakys įtraukti į NATO buvusio SSSR valstybes, ką galima interpretuoti kaip Estijos, Latvijos ir Lietuvos išbraukimą [iš NATO]”, - pirmąją naujųjų metų dieną rėžė prestižinis, skirtas nušviesti tarptautiniams santykiams amerikiečių žurnalas The National Interest.

Praėjus kelioms dienoms, tas pats The National Interest rašo: “Pabaltijo respublikų prijungimas [prie NATO] 2004 metais buvo pats pavojingiausias žingsnis šiame procese. Kaip ir sekantis mažų Balkanų šalių prijungimas prie NATO atvejis, trejos Baltijos šalys maža ką gali pasiūlyti karinio potencialo atžvilgiu. 6 700 Estijos kariškių, 5 500 Latvijos kariškių ir netgi 20 500 Lietuvos kariškių reikš visiškai nedaug, jei prasidės NATO ir Rusijos karas“.

Šio tvirtinimo autorius – amerikietiškų tyrimų tarptautinių santykių srityje klasikas, buvęs JAV Kongreso narys ir pačio artimiausio valdančiam isteblišmentui Katono Instituto vyresnysis mokslinis bendradarbis Tedas Karpenteris.

Numanoma išvada: išvykime Pabaltijį iš NATO ir atiduokime jį Rusijai. Atsikratykime to galvos skausmo.

Paminėtam Pabaltijui belieka tik guostis tuo, jog ši nuomonė, kaip ir kitos šiame straipsnyje minimos nuomonės – privatus požiūris, o ne oficiali Baltųjų Rūmų ir Valstybės departamento nuomonė. Tačiau tikrovė kur kas sudėtingesnė.

Įžymioji pirmoji JAV Konstitucijos pataisa kiekvienam amerikiečiui garantuojanti žodžio laisvę – gana sąlyginis dalykas. Šiuolaikinėje Amerikoje negalima sakyti ir rašyti viską, ką tik nori. Už nepriimtinus žodžius tavęs nepasodins ir neišsius – tave, kaip dabar ten sakoma, „išjungs“.

Dabar JAV visos nuomonės pasidalino į leistinas ir neleistinas. Jei gerbiami Forbes, National Interest ir USA Today autoriai, Brukingso ir Katono Institutų darbuotojai, pavyzdžiui tvirtintu, kad visi žmonės gimsta arba vyriškos lyties, arba moteriškos lyties, o visi transgenderiai – iškrypėliai, su jais nutrauktu darbo sutartį, baigtu spausdinti jų straipsnius, neduotu grantų, nekviestu į mokslo konferencijas ir neįtrauktu į darbo grupes.

Tačiau, siekiant išvengti konflikto su Rusija, siūlymas išvyti Pabaltijį iš NATO nėra nepriimtinas pasisakymas, ir tie žmonės, kurie taip kalba, lieka gerbiamais ekspertais, kuries gerai priimami JAV politiką formuojančiuose sluoksniuose.

Sisteminių ekspertų pagalba Vašingtonas siunčia Maskvai viešą signalą: derybų Ženevoje dėl strateginio stabilumo ir abipusių saugumo garantijų galimybių erdvė mums daug platesnė, negu ta, apie kurią mes oficialiai pareiškiame.

Kas tai per sąlygos? Tikėtina, kažkas tai susiję su Kinija – pagrindiniu strateginiu Amerikos konkurentu. Pavyzdžiui, Rusijos atsisakymas karinės-techninės kooperacijos su Padangių šalimi – galų gale, branduolinio ir post branduolinio (hipergarso ginklo) srityje

Šio straipsnio kontekste amerikiečių sąlygos Putinui – tai nesvarbiausia. Svarbu kita.

Ir sąjungininkams regione reikia gyventi su tokiu pagrindinio gynėjo ir globėjo požiūriu. Tegul pasiguodžia tuo, jog, galimai, neilgai liko gyventi.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 7 — id: `scraped:rubaltic_lt:70e7a1afbbdc324c`

**Title:** Kazachstanas – mūsų: Rusija užėmė svarbiausią strateginę aukštumą kovoje su JAV

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Metų pradžios įvykiai Kazachstane daugelį kartu sustiprina Rusiją šioje, jai svarbiausioje šalyje. Maskva tampa ne tik Kazachstano vadovybės valdžios išsaugojimo  garantu, bet ir pačio Kazachstano, kaip vieningos valstybės išsaugojimo garantu.  Chaosas Kazachstane ir Kazachstano subyrėjimas Rusijai būtų tapęs geopolitine katastrofa, bet vietoj to, įvykęs vakarietiškos grupuotės sugniuždymas ir KSSO pajėgų įvedimas į šalį, formuoja Maskvai svarbiausią strateginę poziciją derybose su Jungtinėmis Valstijomis dėl NATO buvimo Rytų Europoje.

Kas Rusijai yra Kazachstanas? Tai pati svarbiausia jos kaimynė iš buvusių sovietinių respublikų nacionalinio saugumo užtikrinimo požiūriu. Strateginio Rusijos saugumo požiūriu Kazachstano reikšmė dargi didesnė nei Baltarusijos, kadangi jos, Rusijos, gyvavimo interesai susiję būtent su šia šalimi.

Gana tik vieno pavyzdžio. Kazachstanas – tai beveik pusė pasaulyje iškasamo urano. Rusijos atominės elektrinės naudoja Kazachstano žaliavą. Destabilizacija ir, dar daugiau, Kazachstano subyrėjimas nutraukia urano tiekimą – su visomis, iš to sekančiomis pasekmėmis Rusijos energetikai, ekonomikai ir ekologijai.

Tarptautinei politikai įvykių Almaty ir (dar kol kas) Nur Sultane esmė gana paprasta. Kazachstane sugriuvo politinis režimas, kuris laikėsi daugiavektorinės užsienio politikos.

Pakanka pažvelgti į stambiausių Kazachstano naftos gavybos kompanijų nuosavybės struktūrą: kontroliniai akcijų paketai priklauso Chevron, Exxon Mobile ir kitoms Didžiosios Britanijos bei JAV naftininkų kompanijoms.

Blogėjant Rusijos ir Vakarų santykiams, auganti britų ir amerikiečių įtaka Kazachstano Respublikoje darėsi vis grėsmingesnė jo šiaurės kaimynei. Ši grėsmė buvo netgi didesnė, negu galimi „vakarų partnerių“ veiksmai iš Ukrainos teritorijos, nors ir nebuvo kalbama apie Kazachstano perėjimą į amerikiečių protektoratą pagal ukrainietišką pavyzdį: kazachų vadovybė rėmėsi užsienio politikos neutralumu ir  sumaniai laviravo tarp Rusijos, Vakarų ir Kinijos.

Reikalas ne protektorate.

Vakarų buvimo respublikoje mastai – pakanka prisiminti apie 16 tūkstančių amerikietiškų nevyriausybinių organizacijų –Vašingtonui ir Londonui darė tokią galimybę įmanoma.

Galima tik įsivaizduoti Maskvos galvos skausmą.  Geležinkelio iš europinės Rusijos dalies į Sibirą išsaugojimas, Baikanuro kosmodromo likimas, Kazachstano rusų gyventojų  saugumas, pabėgėliai, urano tiekimas – po viso to Rusijai būtu ne iki ultimatumų dėl raštiškų garantijų neplėsti NATO į rytus.

Rusijoje daugelis įsitikinę, jog 2022 metų pirmųjų dienų įvykiai Kazachstano miestuose ir buvo bandymas sukelti tokį galvos skausmą Maskvai rusų – amerikiečių derybų dėl branduolinio ginklo ir Ukrainos išvakarėse. Tikėtina. Atsižvelgdamas į įvykių raidą, autorius linksta link minties, jog Rusijos valdžiai buvo žinoma apie ruošiamus įvykius ir ji, aplenkdama juos, suveikė, iš anksto suderinusi visus veiksmus su Kazachstano prezidentu Kasymu-Žomartu Tokajevu.

Tarp kitko, tai antraeilė.

Neutralus, daugiavektorinis Kazachstanas daugiau nėra įmanomas.

Visų pirma todėl, jog be Rusijos, valdžią savo rankose prezidentui Tokajevui neišlaikyti. Metų pradžios krizė pademonstravo klanų kovos respublikoje įkarštį ir tos kovos įtaką pajėgų pareigūnų lojalumui. Be Rusijos pajėgų paramos Tokajavą labai greitai  sunaikins vidaus priešai.

Antra, Rusija Kazachstane tapo įstatymo ir tvarkos užstatu didžiųjų miestų gyventojams (visų pirma – rusakalbiams, bet ne tik jiems), kurie savo kailiu patyrė puslaukinių, nuskurdusių aulų, kur didelę įtaką turi islamo radikalai – pagrindinis pogromų ir plėšimų socialinis variklis, agresiją.

Respublikos valdžia legitimi todėl, jog ji paprašė Rusijos pagalbos, kuri tik ir gali išsaugoti kazachstaniečius nuo gatvių gaujų, marodierių, etninių valymų ir radikalaus islamo plėtros, galinčios sukelti teroro sprogimą.

Kinija nuo tokios veiklos visada pasišalina, savo buvimą apriboja ekonomine veikla. Vakarams Kazachstano panirimas į chaosą kovos su Rusija ir ta pačia Kinija kontekste yra naudingas. Kazachstano pajėgų pareigūnai pademonstravo savo nepatikimumą ir demoralizavimą.

Kas lieka? Tik Rusija.

Tokiu būdu, situacija, taip vadinamoje postsovietinėje erdvėje principingai keičiasi. Šios erdvės antroji, pagal dydį ir svarbą, šalis papuolą į strateginę priklausomybę nuo Maskvos, kuri dabar nustato tolimesnį Kazachstano, kaip stabilios ir vieningos šalies, gyvavimą.

Šveicarijoje kaip tik prasideda Rusijos ir JAV atstovų derybos dėl strateginio stabilumo (branduolinio ginklo) ir raštiškų garantijų neplėsti NATO buvimą Rusijos pasienyje. Dar prieš savaitę JAV turėjo galimybę pradėti derybas esant tokiom sąlygom, jog pas rusus „svyla“ greta pietinės sienos. Dabar gi, amerikiečiams prisieis ginti užgrobtas pozicijas Rusijos vakariniame pasienyje esant sąlygoms, kai Rusija užsitikrino strateginį saugumą pietuose.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 8 — id: `scraped:rubaltic_lt:e8da16f540340f18`

**Title:** Okupantų dovana: kodėl Lietuva gėdijasi švęsti tikrąją „Nepriklausomybės“ dieną

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Metų laike Lietuvoje švenčiamos trys „Nepriklausomybės dienos“: Lietuvos valstybės diena (liepos 6 d.), Lietuvos valstybės atkūrimo diena (vasario 16 d.) Lietuvos valstybės nepriklausomybės atkūrimo diena (kovo 11 d.). Bet kartu su tuo, tikroji Nepriklausomybės diena – 1917 m. gruodžio mėnesio 24 d., kai iš tikrųjų buvo paskelbta Lietuvos valstybė, Lietuvoje ši diena nešvenčiama ir netgi nutylima apie jos egzistavimą. Dėl labai paprastos priežasties, tėvai – įkūrėjai Lietuvą paskelbė, leidus vokiečių okupaciniai valdžiai ir prisiekę okupantams „amžinais Lietuvos valstybės su Vokietija sąjunginiais ryšiais“.

Vienu iš trejus dešimtmečius įdiegiamų į masinę sąmonę postulatų buvo „pas lietuvius SS nebuvo“. Normaliam žmogui iš šalies tai visada reiškė ne daugiau kaip „gavę vokiečių sankciją latviai žudė savo žydus, apsirengę štai tokia uniforma, o lietuviai – kitokia“. Na, žinoma, patys lietuviai bandė ir bando tam suteikti gilesnę esmę: esą, tada mes nesiklausėm vokiečių, ir mechaniškai nevykdėme jų įsakymų, kadangi mes laisva tauta.

Bet faktai lieka faktais 1943 metais vokiečiams iš tikrųjų nepavyko suformuoti lietuvišką SS legioną, ir autorių, kaip istoriką, visada domino klausimas: kodėl?

Kyla maždaug toks atsakymas: lietuviai psichologiškai yra mažiau priklausomi nuo vokiečių nei latviai ir estai, kurie šimtmečiais buvo vokiečiams pavaldžios tautos. Mintis diskutuotina, bet turinti teisę egzistuoti.

Kai kalbama apie Pabaltijo šalių atsiskyrimo nuo Rusijos paskelbimą po 1917 metų revoliucijos, oficialūs Lietuvos , Latvijos ir Estijos propagandistai įprastai droviai praleidžia šią labai svarbią klausimo pusę: tų paskelbimų legitimumą. O jis, atleiskite, yra nulinis.

Visai trejais atvejais politinius sprendimus dėl, pagal dydį įspūdingų teritorijų likimo priiminėjo niekuo neįgaliota, savavališkai susirinkusi liaudies dainų mėgėjų ir folkloro rinkėjų „pagrindinės“ tautybės, nors šiose teritorijose gyveno ir kitos tautos, grupė. Lietuvišku atveju, netgi čia – įžymios.

Kalbant kita (teisine) kalba, grupė Rusijos pavaldinių, pasinaudojusi karo bei jų gyvenamos vietos okupavimo užsienio kariuomene aplinkybėmis, okupacinės valdžios iniciatyva bei jos interesais įsteigė valdžios „organą“, kuris veikė okupantų nustatytose rėmuose.

Bendrai, jei estų ir latvių „tautinės tarybos“ 1917 metais, paprasčiausiai, buvo savavališkomis, niekuo neišrinktų asmenų sueigomis, tai lietuviškame atvejyje viskas buvo kur kas liūdniau.

Likimo ironija tame, jog pareikalauti atsakymo iš lietuviškų kvislingų, paprasčiausiai nėra kam: per tuos beveik 23 metus, kuriais Lietuvoje tęsėsi vokiečių okupacinės administracijos sukurta „politinė tradicija“, reali Rusija buvo „perkrauta“ naujovėmis ir kurį tai laiką neskaitė save istorinės Rusijos teisių perėmėja.

Bet štai lietuviškos kilmės vokiečių liokajų veiksmams tai jokio legitimumo neprideda, kadangi legitimumas atgaline data nekyla.

Suprantama, jog jokio legitimumo nebuvo ir 1917 m. gruodžio mėn. 24 d. Tarybos sprendime dėl Lietuvos nepriklausomybės atstatymo ir „amžinų Lietuvos valstybės su Vokietija sąjunginių ryšių“.

Tai yra, iš Berlyno, niekada neįžvelgusio jo pačio sukurtame Lietuvos „valstybingume“ jokios esmės, neskaitant vištų, žąsų bei paršiukų mobilizacijos kariaujančio Antrojo reicho poreikiams, šūktelėjo savo įsidūkusiom marionetėm, ir jos momentaliai „pasuko atgal“.

Bet faktas lieka faktu: jokių kitų įgaliojimų, neskaitant tų apie kuriuos buvo painformuota okupacinė vokiečių valdžia, nei Taryba, nei iš jos 1918 m. liepos mėn. 11 d. save transformavusi „Lietuvos Valstybės Taryba“ niekada neturėjo, visų jos veiksmų bei sprendimų, įskaitant paskelbtas dvejas „nepriklausomybes“ (su toliau sekančiu antros atšaukimu ir sugrįžimu į pirmąją), dviejų „laikinų konstitucijų“ „priėmimą“ ir Steigiamojo Seimo sušaukimą 1920 metais, legitimumas yra lygus nuliui.

Žinoma, jei jūs nepastebite Vokietijos vadovybės „teisės“ Rusijos Kauno ir Vilniaus gubernijų teritorijose, kokiomis jos juridiškai buvo 1917 metų rugpjūtyje – gruodyje, suteikti kažkam tai kokius tai įgaliojimus.

Bet kuris objektyvus stebėtojas, neskaitant to, jog šis vaidelis nėra labai gražus, pastebės dar kai ką: aukščiau aprašytos „politinės tradicijos“ likvidavimas 1940 metų birželyje buvo kur kas legitimesnis – bet kokiu atveju, per rinkimus. Žinoma, visa tai buvo paremta Kremliaus politine valia, bet formali politika visgi buvo išlaikyta.

Kas liečia tikrąsias „nepriklausomybės“ metines, tai jas Lietuvoje, žinoma, niekada nešvęs – atšvęs netikrąją, vasario 16. Tačiau istorija – tai kaip buvo, o ne tai kaip norėjosi kad būtų. Kaip tai bebūtu nemalonu kol kas dar valdantiems Lietuvą „landsbergistams“.

Ir ji, istorija turi pasikartojimo savybę.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 9 — id: `scraped:rubaltic_lt:bc1389a6b61b6ea9`

**Title:** Istorikas: Lietuva neturi nei vieno, esą, Raudonosios Armijos surengto lietuvių „genocido“ fakto

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos istorinė politika remiasi istorinių mitų fabrikavimu, kuriuos vėliau Vilnius bando panaudoti politiniais tikslais. Daugumoje atvejų tie mitai nukreipti prieš Rusiją. Tam ryškus pavyzdys – tvirtinimas, jog Raudonoji Armija Didžiojo Tėvynės karo metu Rytų Prūsijoje užsiiminėjo vietinių lietuvių „genocidu“. Kaip pasipriešinti istoriniam oficialaus Vilniaus melui RuBaltic.Ru analitikos portalui papasakojo Kaliningrado istorikas, I. Kanto Baltijos federalinio universiteto Geopolitinių ir regioninių tyrimų instituto Istorinės atminties tyrimų centro jaunesnysis mokslinis bendradarbis Albert ADYLOV.

- ponas Adylov, pagrindinis mitas apie „Mažąją Lietuvą“, kurį bando prastumti Vilnius, tai mitas apie tai, jog lietuvninkų, prūsiškų lietuvių iš Rytų Prūsijos išnykimas yra 1944 metų Raudonosios Armijos surengto „genocido“ Gulbinės-Goldapo operacijos, tai yra sovietų kariuomenės įžengimo į Rytų Prūsiją metu rezultatas. Tai oficiali Lietuvos pozicija. Kaip Jūs galite tai apibūdinti?

- Oficialiąją Lietuvos poziciją negalima skaityti kaip atitinkančią istorinę tiesą. Oficialioji Lietuvos pozicija – tai ir tai, jog pas ją buvo didysis Lietuvos revoliucionierius Kostas Kalinauskas, nors šis žmogus niekada savo gyvenime neturėjo tokios pavardės ir visiškai nemokėjo lietuvių kalbos.

Ir be jo yra daug, taip vadinamų lietuviškų istorinių veikėjų, paprasčiausiai paimtų pas kaimynes tautas, sulietuvinant jų vardus ir pavardes.

Iš tikrųjų, taip, lietuvių tautybės gyventojai Rytų Prūsijoje išnyko, bet kartu su likusiais vokiečių tautybės gyventojais, kurie buvo perkelti po to, kai Karaliaučius (Kaliningradas) ir Memelis (Klaipėda) buvo prijungti prie SSSR

Nors, lyg tai Memelio krašte, dabartiniame Klaipėdoje krašte, kažkas tai pasiliko. Tiesiog žmonių vienetai, kurie vėliau kokiu tau būdu prie sovietų valdžios legalizavosi.

- Pas mus, Kaliningrado srityje pasiliko vokiečių vienetai.

- Taip, jokio genocido, jokio teritorijos valymo čia nebuvo. Paprasčiausiai gyventojai išėjo įsakius jų viršininkams, taip sakant partiniams, valstybiniams.

Niekas nesugeba dokumentaliai įrodyti, jog Rytų Prūsijoje kažką tai naikino už tai jog jie lietuviai.

- Bet visgi, kiekvieną spalio 16 d. Lietuvoje minima kaip Raudonosios Armijos organizuoto Mažosios Lietuvos gyventojų genocido diena. Dėl to yra Seimo nutarimas, kuriuo 1944 metų įvykiai paskelbti Rytų Prūsijos lietuvių kilmės gyventojų genocidu.

- Tai, kad paskutiniaisiais 30 metų Pabaltijyje gana plačiai traktuojama genocido sąvoka, yra visiems žinoma. Kaip žinoma, ten genocidu vadinamos ir stalininės deportacijos, nors jos nieko bendro su genocidu neturėjo, be abejonės, ir, dažniausiai, tai buvo daroma tos pačios tautybės asmenimis savo gentainių atžvilgiu. Todėl aš nemanau, jog tai reikia rimtai nagrinėti.

- O jei Lietuva pabandys aktualizuoti šią temą ir eiliniam Goldapo -Gumbinės operacijos jubiliejui Suvienytų Tautų organizacijos lygyje pareikalaus išmokėti kompensaciją už Prūsijos lietuvių genocidą?

- Generalinėje asamblėjoje galima kalbėti apie bet ką, pareikšti bet kokius pareiškimus, bet reikalas tame, jog kai visą tai reikia praktiškai realizuoti, yra STO Saugumo Taryba, pastovūs jos nariai. Vienų iš pastoviųjų narių yra Rusijos Federacija ir, suprantama, jog tokia rezoliucija bus blokuota, ir jokių padarinių, neskaitant informacinio triukšmo, ji nesukels.

Tiesa sakant, mano klausimai ir liečia informacinį triukšmą. Jei bus sukeltas toks informacinis triukšmas, tai ar pas mus, Kaliningrade, yra mokslinė bazė, kurios pagalba visą tai galimą paneigti?

Manau, jog tam tikra „tuštuma“ tame yra. Ilgą laiką šie klausimai nebuvo keliami, aptariami, nagrinėjami. Manau, jog tai ne pačių mokslininkų kaltė, o valstybės, kuri nepateikė socialinio užklausimo. Jei toks socialinė užklausimas bus, tai, tikriausiai bus tyrimai, bus publikuojami darbai.

Todėl čia visgi nereikia vežimą statyti priekyje arklio.

- Greičiau galima pasakyti, jog faktūros, patvirtinančios, pavyzdžiui, Lietuvių tautybės gyventojų genocidą 1944 metais, neegzistuoja.

Todėl, jog Seimo deklaracijos lygyje – tai viena, o tai patvirtinti kokiais tai dokumentais, vargus ar kas sugebės. Kol kas, kiek man žinoma, nieko nesigavo.

- Jūsų požiūrių, kokiu būdu Rusija turi veikti, idant paneigti ginčą dėl Kaliningrado srities priklausymo RF teisėtumo?

Mano nuomone, pagrindine profilaktikos priemone galėtu būti darbas su istorine atmintimi. Pas mus galėtų daug giliau tyrinėti Kaliningrado regiono istoriją ir jo ryšį su Rusija.

Čia mes ne tuščiažodžiaujame, kadangi aš pats tuo senai užsiimu ir, kaip man rodosi, gana sėkmingai. I. Kanto BFU realizuoju projektą „Rusų kario keliai“, kuris kaip tik yra į tai nukreiptas.

Kokio tai karo metu per šią gyvenvietę žygiavo rusų kariai, kovėsi, buvo sustoję poilsiui. Šiuolaikinių patalpintų Internete šaltinių apimties dėka, konkrečiai, apie Pirmąjį pasaulinį karą, ir pagrinde apie Didįjį Tėvynės karą – tai gana lengva surasti. Apdovanojimo lapai, įsakymai, ataskaitos apie kovos veiksmus.

Mūsų projektas buvo pradėtos nuo tada, kai, niekam nežinomojoje Bagrationovsko rajono gyvenvietėje, kurią sudaro 10 sodybų, mes aptikome tris rusų karo istorijos epizodus; 1807 metų, 1914 metų ir 1945 metų. Ir ten išstatėme stendą. O dabar, tam tikra prasme, ši vieta jau tapo traukos tašku.

Pati pirmoji apsaugos nuo istorijos falsifikacijos priemonė turi tapti aiškinimai žmonėms mokyklos lygyje, bibliotekų lygyje, jog ši tema mums nėra svetima.

Žinoma, turi būti aiškinama idėja ir apie Mažąją Lietuvą, kuri, bendrai pasakius, yra iš piršto laužta. Jos propagandistai, sakysim taip, ne labai dori, jei galima taip pasakyti, istorikai (nors iš tikrųjų ne istorikai, o publicistai-propagandistai) nekreipia dėmesio į vieną faktą. Taip vadinami prūsų lietuviai – tai atvykėliai, kurie Prūsijoje pasirodė XIV amžiaus pabaigoje dėka įvairių lengvatų, kurias Teutonų ordinas suteikdavo atvykėliams, siekiant kolonizuoti teritoriją. Tai yra, faktiškai jie čia atsirado jau po vokiečių.

- Tai yra, kažkada čia gyvenę prūsai ir lietuviai – tai dvi skirtingos tautos?

- Taip, bet tai, deja, mažai kas žino ir supranta. Ir visgi, kuriems tai įdomu, tai suvokia taip, jog, štai, va, baltai – jie ir yra baltai. Tai kažkas bendra, kadangi jų vardai ir pavardės baigiasi „s“. Bet tai maždaug tas pats, kaip ir pareikšti, jog Varšuva priklauso čekams arba Praha priklauso lenkams, kadangi tie ir kiti – slavai. Ne, žinoma, slavai, bet visgi tai skirtingos tautos. Tas pats ir su prūsais bei lietuviais.

Neabejotinai, bendrai, lietuviams, lietuvių diasporai visame pasaulyje, Kaliningrado sritis labai reikšminga ta prasme, jog tai yra jos kultūros lopšys. Tokios įžymybės kaip, Martynas Mažvydas, Kristijonas Donelaitis – jie dirbo būtent čia. Bet jie dirbo turėdami tam prūsų valdžios leidimą ir tiesioginį jos nurodymą. Karaliaučiaus universiteto Lietuviška seminarija egzistavo ne dėl abstraktaus mokslo vystymo, ir ne dėl abstrakčios kultūros plėtros. Ši seminarija ruošė liuteronų klebonus kaip valstybės valdininkus, kurie, paprasčiausiai, turėjo skleisti tikybą gyventojų mažumai jai suprantama kalba. Tam, kad vėl gi, skleisti valdžiai reikalingą ideologiją, Štai pagrinde ir viskas.

Tai rusiška kultūros įstaiga, kuri saugo lietuviškos literatūrinės kalbos kūrėjo atmintį. Čia vėl galima pašnekėti apie pasaulinę rusišką atjautą, va, štai kokie mes. Tai, suprantama, neturi būti tapti kokiu tai varžymu: štai, mes ten jiems viską sugriausim arba sunaikinsim.

Nors, galima, jog nugriaunant sovietų generolo Ivano Černiachovskio paminklą Lenkijos Penenžno mieste, buvo girdėti balsai, - aš pats esu šios idėjos šalininkas, sakysim taip, maža to, aš pats ją ir iškėliau, - apmainyti Šopeno paminklą Kaliningrade į Černiachovskio paminklą. Ši idėja, sakyčiau taip, paremta nebuvo.

Ir Frederikas Šopenas, visgi, - didysis pasaulinio masto kompozitorius. Didysis lenkų kilmės prancūzų kompozitorius, jeigu jau išsiaiškinti. Bet tai ne ta priežastis, kad nusileisti iki tų žmonių, kurie ten griauna paminklus, lygio.

Todėl tai, jog Donelaičio muziejus mūsų yra remiamas – yra teisinga. Tai turi tapti priekaištu Lietuvos šaliai, kuri, kaip žinoma, visus paskutiniuosius 30 nepriklausomybės metų bando užgniaužti rusišką švietimą, rusišką kultūrą Lietuvoje.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 10 — id: `scraped:rubaltic_lt:0af94f1f6500893b`

**Title:** Sutriuškinta visuose frontuose: Lietuvos užsienio politikos krachas

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Valdančioji Lietuvos partija 2021 metus baigė turėdama gėdingai žemus reitingus: tik per metus jos šalininkų gretos praretėjo beveik dvejus su pusę karto (nuo 24,86% iki 11,5%). Konservatorių lyderis Lietuvos užsienio reikalų ministras Gabrielius Landsbergis pačių populiariausių šalies politikų sąraše užima „garbingą“ antrąją vietą iš galo. Socialinių apklausų rezultatai tiksliai korailiuojasi su „landsbergistų“ užsienio politikos „pasiekimais“, Jie pademonstravo savo bejėgiškumą kovoje su Baltarusijos atomine elektrine (BelAE), jų dėka pavojingoje padėtyje atsidūrė Klaipėdos uostas, ant Lietuvos verslo jie užtraukė galingos Kinijos pyktį.

Astravo „atominio monstro“ problemą Ingridos Šimonytės ministrų kabinetas paveldėjo iš Lietuvos Valstiečių sąjungos ir „žaliųjų“ (LVSŽ). Nors ir patys konservatoriai, būdami opozicijoje, aktyviai rėmė BelAE boikotą, balsavo už taip vadinamą anti Astravo įstatymą, reikalavo jo praktiško taikymo ir t.t.

Kai paaiškėjo, jog Lietuva negali atsitverti nuo baltarusiškos elektros, Landsbergis ir kompanija apkaltino Sauliaus Skvernelio vyriausybę nekompetentingumu. Ypatingai buvo išskirtas energetikos ministras Žygimantas Vaičiūnas. Būtent jis parengė kompromisinio susitarimo su Latvija ir Estija prekybos su trečiosiomis šalimis projektą.

Atsakydami konservatoriai pradėjo spiegti vos ne apie valstybės išdavimą ir kapituliaciją Lukašenkai. Pareikalavo atstatydinti Vaičiūną.

Tarp kitko, šis klausimas buvo išspręstas 2020 metų parlamento rinkimų rezultate. Laimėjo konservatoriai, kurie „sukalė“ valdančiąją koaliciją su Liberalų sąjūdžiu ir Laisvės partija . Naująja premjere tapo Šimonytė, o energetikos ministru – Dainius Kreivys. Pastarasis iš karto pripažino, jog anti Astravo įstatymas nėra vykdomas, baltarusiška elektra ir toliau patenka į Lietuvą.

Visų pirma, fizinis elektros energijos srautas iš Baltarusijos nesustabdytas. Kad tuo įsitikinti, gana užeiti į Lietuvos elektros tinklų sisteminio operatoriaus Litgrid svetainę. Čia, realaus laiko režimu atnaujinami duomenys apie perdavimo tarp Baltarusijos ir Lietuvos galias. Pavyzdžiui, ruošiant šią medžiagą (gruodžio 27 17:00) jos sudarė daugiau nei 560 MW.

Antrą, sudarytį susitarimą dėl trišalės prekybos elektra metodikos Kreivys nesugebėjo. Latvija ir Estija, kaip ir anksčiau, nepriima Lietuvos pasiūlymų. Rugsėjyje Litgrid apribojo tarpvalstybinės elektros perdavimo linijų Baltarusijos pasienyje maksimalų elektros energijos perdavimo pralaidumą, ir Kreivys paskubėjo paskelbti save nugalėtoju kovoje su BelAE.

„Šiai dienai elektra iš Astravo jau nepatenka į Lietuvą, (...) Dabar tai aš galiu garantuoti 110 procentų. Tam elektros perdavimo linijų pralaidumas yra reguliuojamos taip, kad ji (BelAE produkcija - RuBaltic.Ru pastaba) nepatektų“,- kalbėjo Lietuvos energetikos ministras.

Dabar jau laikas jo oponentams kelti triukšmą. Tinklo operatorius ne „nunulino“, o tik sumažino perdavimo galią pasienyje su Baltarusija. Tai kodėl gi Kreivys yra įsitikinęs, jog „elektra iš Astravo jau nepatenka į Lietuvą“? Tam nėra jokių techninių kliūčių.

Skandalas su „Belaruskalij“ tapo dar vienu vyriausybės nekompetentingumo požymiu. Rugpjūtyje Lietuvos transporto ir komunikacijų ministras Marius Skuodis kažkodėl tai nusprendė, jog jo šalis turi laikytis JAV sankcijų ir blokuoti baltarusiškų trąšų tranzitą. Kai tranzitas nesustojo, Skuodis ir URM vadovas Landsbergis puolė į isteriją. Netgi buvo pasirengę atsistatydinti, bet Šimonytė nepanoro atleisti tokius „vertingus“ specialistus.

Faktiškai JAV sankcijos Lietuvai nėra privalomos, apie ką ji ir buvo painformuota oficialiu raštu. Landsbergis ir kompanija, paprasčiausiai, nori išvyti „Belaruskalij“ iš Klaipėdos uosto. 2022 metai tai beveik garantuotai atsitiks. Dėl to Lietuvos ekonomika, remiantis respublikos jūros krovos kompanijų asociacijos prezidento Vaidoto Šileikos vertinimu, neteks maždaug 300 milijonų eurų per metus.

„Lietuvai pažeidus tarptautines sutartis, mes išnaudosime visas teisinės apsaugos priemones ir su ieškiniais kreipsimės į teismus. Be to, manome, kad į teismus kreipsis ir dauguma mūsų klientų, trąšų pirkėjų, kurie dėl Lietuvos veiksmų liks be prekių ir patirs didelę žalą. Dėl to jie gali būti priversti pirkti trąšas gerokai didesnėmis kainomis. Ieškinių sumos šiuo atveju gali siekti milijardus eurų“, - grasino oficiali „Baltarusijos kalio kompanijos“ (BKK) atstovė Irina Savčenko savo interviu LRT radijui.

Oficialus Vilnius, regis, turėtų atsakyti tipo „Mums nusispjaut į jūsų ieškinius“. Bet ir Skuodis, ir Landsbergis, ir Šimonytė tyli. Jie puikiai supranta, jog Lietuva negalės išvengti kompensacijų už kontrakto pažeidimą, kadangi jokių teisinių pagrindų „skirtis“ su „Belaruskalij“ nėra.

Už šią valdžios avantiūra anksčiau ar vėliau teks atsiskaityti valstybės biudžeto bei paprastų mokesčių mokėtojų sąskaita.

Landsbergio liudytojų sektos adeptai neigs jog tai katastrofa. Bet faktas lieka faktu: Pabaltijo respublikos valdžia nesitikėjo ir neapskaičiavo potencialios žalos dėl neoficialių Pekino sankcijų. Ji buvo tvirtai įsitikinusi, jog Padangių šalis negali pakenkti Lietuvai, kadangi ji nėra svarbi prekybos partnerė.

Ir tik metų gale Lietuvos verslo atstovai įsisąmonino visą katastrofos mastą. Žodis „katastrofą“ šia labiau nei tinkamas.

Jei tikėti Lietuvos pramonininkų konfederacijos vadovu Vidmantu Janulevičiumi, 2022 metais jos šalis dėl Kinijos sankcijų gali netekti 3-5 milijardus eurų. Kodėl tie daug?

Dabartiniu metu sunku rasti stambią transnacionalinę kompaniją, kuri iš Kinijos nieko neimportuoja arba ten nesiunčia gatavą produkciją. Todėl Padangių šaliai nėra būtina būti stambiu Lietuvos prekybos partneriu, kad skaudžiai smogti jos ekonomikai.

Ar galėjo Lietuvos ekspertai apie tai pagalvoti iš anksto? Aišku, galėjo. Tik jų niekas apie tai neprašė. Vyriausybė, su Vytauto Landsbergio ryžtingumu, kuris 1991 metų sausyje vedė žmones prie Vilniaus televizijos bokšto pastato, paprasčiausiai, įkišo galvą į kilpą.

Įdomiausia, jog iki konservatorių atėjimo į valdžią Vilniaus ir Pekino santykius buvo galima pavadinti lygiais. Tegul ir ne draugiškais.

Valstybės saugumo departamento ataskaitose jau figūravo „kinų grėsmė“, prezidentas Nausėda demonstratyviai atsisakinėjo investicijų iš KLR (kurios, tarp kitko, ir nebuvo siūlomos).

RuBaltic.Ru analitikos portalas jau buvo rašęs, jog Lietuvos užsienio reikalų ministro postas – tai tramplinas, nuo kurio Gabrielius Landsbergis turi „įšokti“ į valstybės vadovo kėdę. Bet per kelius mėnesius anūkėlis sugebėjo netekti, ir be to neaiškius pergalės kovoje už prezidento kėdę, šansus. Absoliuti lietuvių dauguma jo darbo rezultatus vertina negatyviai.

Tik pačiam Dievui žinoma, kaip dar po metų giliai kris personalinis jaunesniojo Landsbergio reitingas.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 11 — id: `scraped:rubaltic_lt:68d60518f5b3d3a7`

**Title:** Europa ragina Lietuvą kapituliuoti prieš Kinija

**Source:** rubaltic_lt (propaganda)

**Text:**

```
2021 metų pabaigą Lietuvai sudrumstė naujiena, jog atsakomosios Europos Sąjungos kontrpriemonės Kinijai, geriausiu atveju gali pasireikšti po pusės metų. Taip prognozuoja eurokomisaras aplinkos ir vandenynų klausimams Virginijus Sinkevičius. Kartu su tuo niekas negarantuoja Lietuvai, jog ES iš viso vykdys anti kinietiškas sankcijas – pagrindinės bendrijos šalys nedega noru gadinti santykius su Padangių šalimi.

Pajutusi KLR ekonominį spaudimą, Lietuva, visų pirma, paprašė Briuselį užsistoti. Jau ne kartą Pabaltijo respublikos užsienio reikalų ministras Gabrielius Landsbergis ragino parodyti europietišką solidarumą. Būtent jis oficialiai kreipėsi pagalbos pas ES diplomatijos vadovą Žozepą Borelį ir Europos komisijos vadovo pavaduotoja Valdį Dobrovskį.

„Prašau jūsų Lietuvos vardu įsitraukti į diskusijas su Kinijos valdžios institucijoms, siekiant išspręsti esamą situaciją. Būsiu dėkingas už jūsų nuolatinę paramą užtikrinant, kad tarptautinė prekyba būtų vykdoma pagal visame pasaulyje pripažįstamas prekybos taisykles ir gerą praktiką, o muitinės bei kitos procedūros nebūtų naudojamos kaip politinio spaudimo prieš ES valstybę narę priemonė,“ – sakoma Landsbergio kreipimesi . Dėl pačio to rašto Lietuvos konservatorių lyderis pateko į gana kvailą padėtį.

Kalbama apie prekybos panaudojimą kaip konkrečios šalies (Baltarusijos) politinio spaudimo instrumentą. Gaunasi, jog su valstybėmis – ES narėmis taip elgtis nevalia, o su visomis likusiomis – galima?

Tarp kitko, į Landsbergio raginimą pagalbos iš Briuselio kol kas atsakymo nebuvo. Jungtinė Europa kol kas pareiškia tik „gilų susirūpinimą“.

Tikriausiai, vienintelį konkretų pareiškimą šia tema pareiškė Lietuvos atstovas Eurokomisijoje Virginijus Sinkevičius. Jo žodžiais tariant, ES iš viso negali diskutuoti su Pekinu dėl ekonominio Lietuvos spaudimo, kadangi nėra diskusijos dalyko.

Visi lietuviškų prekių importo arba kinų produkcijos eksporto į Lietuvą apribojimai viešai neveikia. Gal būt, tame ir buvo kinų minties esmė.

Įsivaizduokime, jog sąlyginis Žozefas Borelis atvyksta į Padangių šalį ir reikalauja atšaukti sankcijas šaliai – Europos sąjungos nariui. O kinai nustebę klausia: „Kokias sankcijas? Kur Jūs jas matėte? Jokių oficialių pareiškimų nėra, o jei nėra, tai ir nieko nėra“. Kokiu būdu įrodyti, jog kinų kompanijos gavo nurodymą visus savo partnerius iš Lietuvos nukreipti tiesiogiai į Taivaną?

„Šiuo metu diskusijų dalyko nėra. Daugelis spaudimo priemonių randasi po stalu, o ne ant stalo. Jas sunku fiksuoti ir tvirtinti, jog tame dalyvauja valstybė“,-aiškino Sinkevičius.

Spėkime, Europos sąjunga visgi užfiksuos ekonominio Lietuvos spaudimo faktus ir įrodys, jog tai Kinijos komunistų partijos rankų darbas. O toliau? Toliau prasidės biurokratinė painiava dėl kontrpriemonių taikymo.

Pradžioje reikia pareikšti pasiūlymus dėl kontr sankcijų, toliau išnagrinėti visokiose žinybose, vėliau pateikti ES Tarybos balsavimui. Ir sankcijos bus patvirtintos tik tuo atveju, jei jas palaikys delegatai, kurie atstovauja ne mažiau 65% Europos sąjungos gyventojų. Tai yra tokie nykštukai, kaip Lietuva, Latvija ir Estija ten nelabai ir vertinami...

„Aš manau, kad tai užtruks kurį laiką, bent pusmetį, kalbant apie tarpinstitucinį susitarimą dėl šios priemonės, taip pat daug priklausys nuo Prancūzijos pirmininkavimo, kada ji apsiims šį failą svarstyti“, – sakė V. Sinkevičius. Dabartiniais matavimais pusmetis – tai pakankamai ilgas laikotarpis.

Šiame kontekste verta atkreipti dėmesį į dar vieną įdomų pareiškimą, nuskambėjusi iš Lietuvos premjerės Ingridos Šimonytės lūpų: „Lietuva – nepriklausoma valstybės, niekas negali jai įsiūlyti užsienio politiką, netgi Europos sąjunga“.

Žinoma, tai yra melas. Europos sąjunga gali įsiūlyti užsienio politiką ir sėkmingai ją įsiūlo. Patys tie sankcijų mechanizmai, kurie vartojami trečiųjų šalių politiniam spaudimui, randasi išimtinai ES kompetencijoje. Jei sankcijos priimtos, bendrijos šalys – narės privalo jas vykdyti.

Bet kodėl Šimonytė iš viso mini Europos sąjungą? Kas čia per keistas priekaištas? Tik iš pirmo žvilgsnio jis rodosi keistu.

Pavyzdžiui, pakeisti Taivano biuro pavadinimą į Taibei biurą. Tai elementarus ir akivaizdus žingsnis.

O ten , duok Dieve, ir Kinija atsakys kokiu tai atsakomuoju gestu, Įtampa po truputį pradės žemėti.

Ar ne todėl Sinkevičius aiškiai davė suprasti, jog Briuselio užtarimo jo šaliai laukti neverta? Patys pažadinote drakoną – patys jį ir nuraminkite.

Bet Lietuva neketina nusileisti Kinijai. „Tvirtakakčiai“ konservatoriai trauktis nemoka, netgi tada kai jie įsisąmonina savo pirminės strategijos krachą.

Be to konfliktas su Kiniją duoda Lietuvai tam tikrą „naudą“. Prie tokios išvados priėjo buvęs Lietuvos premjeras Andrius Kubilius.

Dabar kiekvienas Lietuvos verslininkas, kuris neteko kinų realizavimo rinkos, gali ateiti prie KLR ambasados ir šūktelti: „Va jums! Mūsų Landsbergis skraido į Ameriką“.

Dėl to, suprantama, verta ir diržus užveržti.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 12 — id: `scraped:rubaltic_lt:1e9657d9ab056b43`

**Title:** Kinija pribaigs tranzitą per Lietuvą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos kompanijos bando apeiti neoficialius Kinijos apribojimus prekyboje, siųsdamos savo produkciją eksportui per kaimyninių šalių uostus. Apie tai pareiškė Jūros krovos kompanijų asociacijos prezidentas ir Klaipėdos konteinerių terminalo vadovas Vaidotas Šileika. Regis, Kinija nusprendė atskirai smūgiuoti tranzitui per Lietuvą. Šios priemonės nebus mirtinos, bet už tai sustiprins baltarusiškų trąšų išėjimo iš Klaipėdos efektą.

2021 metus Lietuva baigia prekybos karo su Kinija būsenoje. Kol kas rimtų netekimų nėra, bet ir nepastebima priežasčių vietinio verslo optimizmui.

„Pagrinde, visa produkcija stovi. Lietuvos eksportas į Kiniją sustojo“,- konstatuoja Lietuvos pramoninkų konfederacijos prezidentas Vidmantas Janulevičius. Jo žodžiais tariant, prasiskverbti į Kinijos rinką pasiseka tik nedideliam kiekiui technologinių kompanijų.

Lietuvos sugražinimas į kinų muitinės sistemą, iš kurios ji buvo išbraukta vos kelėtai dienų, įtakos situacijai nepadarė. Dabar Padangių šalies tiekėjai iš Pabaltijo respublikos gali pildyti deklaracijas, bet problemos kyla jas patvirtinant.

Jie, pavyzdžiui, atsisako nuo „nepageidaujamų“ alaus rūšių. „Nepriima tuose parduotuvėse, kuriuose anksčiau buvo priimama, sako: „Ne, daugiau jo nebus, jis lietuviškas“. Distributoriams, kurie tiekia į prekybos tinklus, pasako „lietuviškų prekių nebus, vežkit į Taivaną (...) Nė vienas iš didžiųjų Lietuvos gamintojų, ten nepatenka“, – aiškino Lietuvos aludarių gildijos prezidentas Saulis Galadauskas Žinoma, respublikos valdžia galėjo to tikėtis. Ir netgi perspėjo iš anksto, jog „indėnų problemos šerifą nejaudina“: lietuviškų prekių tiekimo į Kiniją apribojimo makroekonominis efektas bus mizerinis.

Kalbama apie 300 milijonų dolerių per metus. Tegul tie, kas nukentėjo, ieško naujas realizavimo rinkas. Negi be reikalo Lietuvos užsienio reikalų ministras Gabrielius Landsbergis derėjosi dėl paskolų garantijų su JAV Eksporto – importo banku?

RuBaltic.Ru analitikos portalas jau buvo rašęs, jog Pekinas nusprendė bausti Vilnių amerikietiškai. Iš vienos pusės, jis kliudo pramoninių prekių, kurios vartojamos Lietuvos gamyklose, eksportui. Iš kitos pusės, Kinija trikdo produkcijos, kurios sudėtyje yra kokie tai, pagaminti Lietuvoje, komponentai importą.

Bet tuo siurprizai nesibaigė. Dar prieš kelėtą mėnesių Lietuva tikėjosi „prisisiurbti“ prie naujojo prekybos ir logistikos centro (PLC) Kaliningrado srityje, kuris orientuotas į kinų prekių perkrovą. „Didelė dalis kinų srauto ir taip per Lietuvą tranzitu vyksta į Kaliningradą. Kadangi srautai iš Azijos didėja, natūraliai atsiveria papildomos galimybės mums, kadangi mes esame šio kelio dalimi“,- sakė „Lietuvos geležinkelio“ komunikacijų direktorius Mantas Dubauskas.

Dabar Jūros krovos kompanijų asociacijos prezidentas ir Klaipėdos konteinerių terminalo vadovas Vaidotas Šileika sako, jog šiems planams galima pastatyti kryžių.

Tai, tarp kitko, nesiūlo nieko gero ir Kaliningradui.

Pagaliau, dar viena Lietuvos ir Kinijos prekybos karo auka gali tapti Klaipėdos uostas. Šileika tvirtina, jog vietiniai gamintojai pradeda keltis į kaimyninių – Latvijos ir Lenkijos valstybių uostus.

Šiaurinėje Lietuvoje laikoma normalia praktika naudotis Rygos uosto paslaugomis. Bet paskutiniu metu Latvijos sostinė pritraukia vis daugiau krovinių, kurie anksčiau buvo gabenami per Klaipėda. Naudodami šį maršrutą Lietuvos eksportuotojai mėgina apeiti neformalias Kinijos sankcijas.

„Taip pat atsiranda požymių, jog krovinių importuotojai taip pat mėgina ieškoti alternatyvius uostus, - dalinasi savo pastebėjimais Šileika. – Importui iš Kinijos į Lietuvą jie nurodo Latvijos Rygą, kaip paskutinį iškrovimo uostą“.

Kadangi Kinija neafišuoja savo, su sankcijomis Lietuvai susijusios veiklos, viso vaizdo kol kas mes nestebime.

Tiems laimingiesiems, kurių dar neišvijo iš Kinijos rinkos, siūloma savo produkciją eksportuoti per Lenkiją ir Latviją. Su importu – tas pats. Tiekimas dalinai užblokuotas, o tai, ką dar galima gauti, prašoma pasiimti Rygoje.

Automatiškai Lietuvai gresia dar viena, neakivaizdi, bet gana reali grėsmė. Vietiniai politikai kažkodėl tai galvoja, jog į prekybą su Kinija orientuotos kompanijos neturi kitos išeities, išskyrus naujų realizavimo rinkų paiešką. Nors alternatyva visgi yra. Kai kurios firmos gali, paprasčiausiai, perkelti savo verslą į kaimynines šalis. Šileika nemano, jog tai nėra galima.

Galima neabejoti, jog naujaisiais metais tai atsitiks (Ingridos Šimonytės vyriausybei jau nebėra kur trauktis). Pačios skyrybos su „Belaruskaliu“ Lietuvai kainuos šimtus milijonų eurų per metus, jau nekalbant apie kompensacijas, kurių reikalaus Minskas už nepagristą kontrakto nutraukimą.

Pagal Šileikos paskaičiavimus, dėl konflikto su Kinija ir Baltarusija Klaipėdos uostas gali netekti iki 40% krovinių apyvartos. Kartu su tuo 26% krovinių tenka „diktatoriškoms“ trąšoms. Dar 4% - kitos baltarusiškos prekės. Vadinasi, likusius 10% Šileika nurašo kaip nuostolius, susijusius su Kinijos ekonominiu spaudimu.

Dėl skandalo su „Belaruskalij“ tranzito sritis tampa skausminga Lietuvos vieta. Kinija padarys taip, kad būtų dar skaudžiau.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 13 — id: `scraped:rubaltic_lt:96cba0a770302f16`

**Title:** Keturios 2021 metų išvados Rusijos kaimynams

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Praeinantys metai tapo etapiniais ribojančiom su Rusija valstybėm. Jie parodė, jog vakarų sąjungininkai nėra patikimi, Kinija sugeba griežtai ginti savo interesus tarptautinėje arenoje, o priklausomybė nuo Rusijos, praėjus 30 metų po SSSR subyrėjimo, ne tik išlieka, bet dar ir stiprėja. RuBaltic.Ru analitikos portalas suformavo  keturias pagrindines politinių 2021 metų išvadas Rusijos kaimynams.

Rusija nustato savas elgesio normas postsovietinėje erdvėje.

2021 metais įvyko Rusijos ir Vakarų geopolitinių santykių dėl Ukrainos  persilaužimas.

Pavasarį, kai Kijeve prasidėjo kalbos apie galimą Donbaso puolimą ir buvo pradėtas karinių pajėgų telkimas link ribojimo linijos, Rusija priartino savo pajėgas arčiau potencialaus karo veiksmų rajono ir dislokavo jas palei Rusijos – Ukrainos sienos perimetrą. Kremliaus atstovai viešai pareiškė, jog jei Kijevas atidengs ugnį, tai bus Ukrainos, kaip valstybės, galo pradžia.

Po keleto savaičių isterijos Ukrainoje ir Vakaruose, politinė ir karinė Ukrainos vadovybė atsisakė savo žodžių ir paskelbė, jog pas ją netgi mintyse nebuvo jokių kitų Donbaso reintegracijos scenarijų, išskyrus taikius.

Metų gale karinų scenarijų Donbase galutinai palaidojo JAV prezidentas Džozefas Baidenas, kuris po pokalbio su Vladimiru Putinu pasakė tiesiai: Rusijos karo su Ukraina atveju, JAV nekariaus su RF Ukrainos pusėje. Kitaip sakant, jei Kijevas užpuls Donecką, Putinui niekas netrukdys okupuoti Ukrainą.

Tai persilaužimas.

Ir amerikiečiai buvo priversti sutikti su šiomis normomis.

JAV, kaip globalinė supervalstybė, fatališkai „apsidergė“.

Paskutiniais metais besitęsiantis JAV silpnėjimas 2021 metais pasiekė kokybiškai naują lygį.

Metai prasidėjo tokia neapsakoma amerikietiškosios demokratijos gėda, kaip Kapitolijaus užgrobimas ultra dešiniaisiais, pralaimėjusio rinkimus prezidento Donaldo Trampo šalininkais. Naujas JAV prezidentas, iškaršęs Džo Baidenas, kurį Baltųjų rūmų administracija ištisus metus slėpė nuo visuomenės, sąjungininkų vilčių dėl Amerikos atgimimo, nepateisino.

Prie Baideno buvo tęsiamas Trampo kursas, nukreiptas į amerikiečių pasitraukimą iš išorinio pasaulio, į kovos su Kinija koncentravimą ir  į Amerikos pasitraukimą iš periferinių pasaulinės politikos regionų, vienu iš kurių galutinai tapo Europa.

Kadrai su amerikiečių diplomatais, išskrendančiais nuo ambasados stogo, ir paliktais amerikiečių sąjungininkais, kurie bando kabintis už orlaivių šasi, liko istorijoje kaip fejerinio Amerikos žlugimo simbolis. Amerikietiški statytiniai postsovietinė erdvėje, kad ir nenorėdami, turi susimastyti: ar neateis jų eilė bėgti į oro uostus ir kabintis už amerikietiškų bombonešių šasi?

Kinija pasirodė daug griežtesnė nei Rusija.

JAV nusilpimas praėjusiais metaus buvo lydimas Kinijos, kaip naujojo pretendento į globalinį lyderį, sustiprėjimu. Padangių šalis aktyviai žengia į pasaulinę areną, ir visas pasaulis atidžiai stebi, kaip ji elgiasi ir kokias elgesio taisykles siūlo.

Buvusiom sovietų respublikom, kurios įprato santykiuose su stipriais reikalauti  ir vaizduoti save kaip auką, idant gauti išorės pagalbą, šio stebėjimo rezultatai nėra džiuginantys.

Lietuvos viršūnė, siekdama JAV dėmesio ir norėdama užsitarnauti jos pritarimo, nesprendė surengti Kinijai tokią pat informacinį – ideologinį karą, kokį ji daugelį metų prieš tai praktikavo santykiuose su Rusija. Lietuvos politikai Europos parlamente prastūmė rezoliuciją apie kinų kompartijos pravedama „uigūrų genocidą“, Vilniuje atidarė oficialią Taivano atstovybę.

Lietuva išėjo iš bendradarbiavimo su Pekinu formato „17+1“, ragindama tą patį padaryti ir kitas Europos sąjungos šalis; Lietuvos vadovai paragino įtraukti „Kinijos sulaikymą“ į atnaujintą NATO strategiją.

Lietuvos isteblišmentui patirtis diktavo, jog už atvirą nedraugiškumą jiems nieko nebus. Rusija už tokį Lietuvos nedraugiškumą jos atžvilgiu apsiribojo politinio dialogo su Vilniumi nutraukimu.

Pekinas atšaukė savo ambasadorių iš Vilniaus ir atsisakė tęsti anksčiau pradėtą aptarimą dėl investicijų. Kinų verslininkai pradėjo nutraukinėti kontraktus su partneriais iš Lietuvos, Lietuvos verslininkams prasidėjo sisteminės problemos su lietuviškos produkcijos eksportu į Kiniją bei kinų prekių išvežimu į Lietuvą. Pekinas netgi tarptautinėms kompanijoms prigrasino uždaryti savo rinką, jei jos bendradarbiaus su Lietuva.

Rusiškas lokys tokios kinų drakono reakcijos fone tampa geru pliušiniu lokiuku. Ne tik Lietuvai, bet ir kitiems Rusijos kaimynams, kurie beveik nebaudžiamai praktikuoja rusofobiją, situacija tampa pavojinga.

Ir tada Gruzijai, Ukrainai, pabaltijiečiams bei kitiems limitrofams rusų-kinų tandemas gali sukelti daug rūpesčių...

SSSR subyrėjimo 30-čio metais buvusios sovietų respublikos pademonstravo kritinę priklausomybę nuo Maskvos, kuri, nežiūrint į bet kokias geopolitines katastrofas, išlieka iki šio laiko.

Bet ši kritinė priklausomybė ir dabar liečia kaip ir šalis -  Rusijos sąjungininkes (Armėniją, Tadžikistaną, Baltarusiją), taip ir šalis, kurios bando įsitvirtinti pasaulyje neapykantos Kremliui sąskaitą (Ukraina, Moldova).

Baltarusijoje prezidentas Aleksandras Lukašenka, stiprėjančio Vakarų spaudimo sąlygomis, valdžią savo rankose išlaiko sąjungos su Maskva sąskaita. Pas vakarų lyderius jau susiformavo įprotis svarbiausiais klausimais, susijusiais su Minsku, iš karto skambinti į Kremlių – Vladimirui Putinui.

Įdomi situacija susiklostė Moldovoje, kur šias metais atėjusi į valdžią provakarietiška komanda priversta vystyti santykius su Rusija – kito kelio pas ją nėra. Nepaisant visų deklaracijų apie Moldovos „europietišką kelią“, respublikoje  tikrąjį susidomėjimą sukelia ne prezidentės Majos Sandu susitikimai su vakarų lyderiais, bet susitikimai su Rusijos prezidento administracijos vadovo pavaduotoju Dmitijumi Kozaku bei derybos dėl rusų dujų kainos Moldovai. Kadangi tik tai yra iš tikrųjų reikšminga.

Ir Ukraina, ir Pabaltijo šalys 2021 – 2022 metų šildymo sezone gelbstisi rusiškų energetikos resursu dėka. Visos energetinės alternatyvos joms tapo chimeromis.

Ir energetika – tai tik vienas pavyzdys. Saugumas Centrinėje Azijoje pasikeitus valdžiai Afganistane, konfliktai tarp Užkaukazės respublikų, migracijos krizė baltarusių – lietuvių ir baltarusių – lenkų sienų: bet kuriame postsovietinės erdvės regione Rusija pasilieka pagrindiniu veikėju

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 14 — id: `scraped:rubaltic_lt:904aea21d6d49419`

**Title:** Paskaičiavo-apsiašarojo: Lietuva neteks milijardų dėl konflikto su Kinija ir Lukašenka

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos ekonomikos nuostoliai dėl Kinijos sankcijų 2022 metais gali siekti 5 milijardus eurų. Apie tai pareiškė Lietuvos pramoninkų konfederacijos vadovas Vidmantas Janulevičius. Dar vienu smūgiu Pabaltijo šaliai taps baltarusių trąšų perkrovos atsisakymas: Lietuvos jūrų krovos kompanijų asociacijos prezidentas Vaidotas Šileika prognozuoja, jog krovinių apyvarta Klaipėdos uoste gali sumažėti 30-40%. Tai Lietuvai padarys papildomus nuostolius, kurių dydis sieks šimtus milijonų eurų.

Lietuvoje niekas nebando paskaičiuoti konkrečią nuostolių sumą, kuriuos patirs šalis dėl nepaskelbto prekybos karo su Kinija. Prieš keletą dienų respublikos ekonomikos ir inovacijų ministrė Aušrinė Armonaitė pareiškė, jog šiuo klausimu niekas neužsiima.

„Tai tikriausiai dar nelabai kaip padaryti. Yra pasirodžiusios informacijos dėl investuotojų nerimo, bet nė vienas investuotojas nėra išėjęs (iš Lietuvos) ir artimiausių tokių realių planų nėra. Yra tik išreikštas susirūpinimas, atvirkščiai, kietiems metams pasirašinėjam didelės apimties sutartis su naujais investuotojais. Tokių bent 30 turime“, – teigė Armonaitė. Lietuvos verslo atstovai nėra nusiteikę taip optimistiškai.

Pradžioje Ingridos Šimonytės vyriausybė tikino, jog nėra jokių priežasčių nerimauti, gi KLR nėra svarbi Lietuvos prekybos partnerė.

„Ką mes galime įvertinti šiandien, tai yra mūsų tiesioginis eksportas, kuris į Kiniją sudaro vos 1 proc. viso Lietuvos eksporto ir tokiu atveju poveikis nebūtų ženklus“, – sakė finansų ministrė G. Skaistė. Vienas eksporto procentas – tai prekės už 300 milijonų eurų per metus. Suma viso Lietuvos ūkio komplekso masteliu lyg ir nedidelė. Ir kas pasakė, jog Pabaltijo respublika neteks tų pinigų? Netekę kinų rinkos, eksportuotojai ieškos naujų partnerių. Juos paremti privalo Taivanas ir Amerika. Užsienio reikalų ministras Gabrielius Landsbergis kaip tik susitarė su JAV Eksporto – importo banku (Ex-Im Bank) dėl tiesioginių 600 milijonų dolerių dydžio paskolų. Rodos, jog galima ir toliau nervinti kinų drakoną, nesibijant pasekmių.

„Kinija turi teisę bet kuriai kompanijai uždrausti pardavinėti į Lietuvą produkciją, kurioje naudojami kinų komponentai ar technologijos, o užsienio kompanijoms taip pat gali būti draudžiama pardavinėti kinų produktus, kurių sudėtyje yra žaliava ar komponentai iš Lietuvos“, - rašo laikraštis Global Times – Kinijos komunistų partijos (KKP) ruporas.

Tuo metu Reuters praneša, jog Padangių šalis reikalauja vokiečių koncerną Continental ne naudoti Lietuvoje pagamintų komponentų. Su analogiškomis problemomis susiduria ir kitos įmonės.

Jų logika yra paprasta ir aiški: galima netekti vieno filialo, kurio vertė 70-80 milijonų eurų, bet galima netekti ir kinų rinkos. Tada korporacijos nuostoliai bus skaičiuojami milijardais.

Kartu su tuo Kinija stengiasi padaryti taip, jog jos detalės nepatektų į Lietuvos gamyklas.

Praeitais metais Lietuva iš Kinijos importavo prekių už 1,2 milijardo eurų. Du trečdaliai iš jų – tai gamybinės paskirties produktai, įgyjami tolimesniam perdirbimui ar panaudojimui ūkinėje veikloje.

„Tikriausiai, mes kalbame apie 700 – 800 milijonus eurų, ir ši suma būtent tokia, tos prekės pavirsta į tris – penkis milijardus eurų per metus, kadangi surenkamas koks tai galinis produktas. Šią sumą bus galima skaityti kaip metų apyvartos sumažėjimą. (...) Visos įmonės, kur yra problemos su apmokėtų prekių išvežimu iš Kinijos, susijusios su pramone. Su žaliava, komponentais, įranga, kurie skiriami gamybinių pajėgumų plėtrai. Todėl, akivaizdu, jog tikslas – pramonė, kuri sukuria pridėtinę vertę. Visos kitos buitinės paskirties prekės juda nesustodamos“,- tvirtina Lietuvos verslininkų konfederacijos vadovas Vidmantas Janulevičius.

Dabar aišku, ką turėjo omenyje Kinijos užsienio reikalų ministerijos oficialus atstovas Čžao Liczian, kai grasino išsiųsti Lietuvą „į istorijos šiukšliadėžę“

Dar vienu Lietuvos ekonomikos išbandymu taps baltarusiškų trąšų tranzito netekimas. Lietuvos jūrų krovos kompanijų asociacijos prezidento Vaidoto Šileikos žodžiais tariant, 2022 metais Klaipėdos uosto krovinių apyvarta gali sumažėti 30-40%.

„Tokios sankcijos Lietuvos ekonomikai gali sukelti rimtas ir ilgalaikes pasekmes. Dabar apie 30% visų krovinių Klaipėdoje – baltarusių kroviniai, trąšos sudaro 26% visų uosto krovinių. Tai Lietuvos ekonomikai sudarys 300 milijonų eurų per metus nuostolių“, - tvirtina Šileika.

Likusius 200 milijonus eurų sudarys „Lietuvos geležinkelio“ (LG) bei visų kitų gretutinių verslo sričių, kurias „maitina“ tranzitas, nuostoliai. Kartu su tuo, vargu ar gausis kompensuoti šiuos nuostuolius. Visų pirma, pati Baltarusija blokuos prekių iš trečiųjų šalių (pavyzdžiui, iš Vidurio Azijos) tranzitą į Klaipėdą. Yra alternatyviniai maršrutai per Ukrainą bei Lenkiją, bet krovinių siuntėjams jie nėra patrauklūs. Antra, potencialius Klaipėdos uosto klientus baidys Lietuvos ir Kinijos konfrontacija.

„Uosto kompanijos daro viską kas įmanoma, kad padengti nuostolius, surasti naujų klientų, bet, atsižvelgiant į dabartinę geopolitinę situaciją, tai padaryti nėra paprasta. Kiek man žinoma, egzistuoja tam tikri tranzito per Baltarusiją apribojimai, kadangi geležinkelininkų planai ar krovinių pervežimo iš kitų šalių maršrutai nėra patvirtinti“, - skundžiasi Šileika.

Baltarusiško tranzito atsisakymui nėra jokių formalių pagrindų – JAV sankcijos liečia tik amerikietiškus asmenis.

Lietuvos santykiai su Kinija dar neseniai buvo tokie patys, kaip ir kitų Pabaltijo respublikų.

Tokių „pasiekimų“ dar nebuvo pasiekusi nei viena Lietuvos vyriausybė.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 15 — id: `scraped:rubaltic_lt:5acb7fe4d437e8f9`

**Title:** Europa pripažista: Rusija griežtai atkeršijo už sankcijas

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Europos Sąjunga kreipėsi į Pasaulio prekybos organizaciją (PPO) reikalaudama išieškoti iš Rusijos beveik 300 milijardų eurų už importo pakeitimo politiką. Tuo pačiu, ne „Kremliaus propaganda“, o patys europiečiai patvirtino: Rusijos atsakas į sankcijas sudavė kolosalų smūgį ES ekonomikai. Tarp kitko, kai „sankcijų karas“ tik prasidėjo, rusiškas maisto produktų embargo sukėlė pašaipų bangą: esą Rusija – tai „ekonominis nykštukas“, ir jokio kontrpriemonės neduos deramo atsako Vakarų sankcijoms. Praėjus 7 metams tie patys žmonės jau panikuoja, jog Rusijos virtimas agrarine supervalstybe tarptautiniuose reikaluose duoda Putinui naują spaudimo svertą.

„2019 metais rusiškų valstybės įmonių paskelbtų konkursinių pasiūlymų vertė sudarė 23,5 trilijono  rublių arba maždaug 290 milijardų eurų, kas ekvivalentu maždaug 20% Rusijos BNP“, -  sakoma oficialiame Europos Sąjungos skunde dėl Rusijos Pasaulio prekybos organizacijai.

Skundo esmė yra tame, jog Europos įmonėms neleidžiama dalyvauti Rusijos valstybės viešuosiuose pirkimuose.

Kontrsankcijų ir importo pakeitimo politikos rėmuose jos neįleidžiamos į Rusijos rinkas, ir visos rangos atiduodamos tėvyniniams tekėjams, kas prieštarauja PPO prekybos laisvės normoms.

Pas žydus toks elgesys apibudinimas žodžiu „chucpa“: ypatingas ciniškas ir niekšiškas poelgis kartus su tuo įžūliai pasitikint savimi ir demonstruojant absoliutų savo teisėtumą. Tai maždaug tas pats, kaip nužudyti savo tėvus ir po to šaukti, jog tave persekioja valdžia, kadangi tu - našlaitis.

Europos komisijos kreipimasis į PPO – tipiška „chucpa“. Septynerius metus europiečiai įvedinėjo ekonomines sankcijas Rusijai ir ignoravo Maskvos skundus, jog jų sankcijos neteisėtos, kadangi pažeidžia PPO taisykles... O dabar patys bėga skųstis į PPO, jog atsakomosios RF sankcijos skaudžiai atsiliepia Europos Sąjungos kompanijoms.

Tai yra vertingas pripažinimas, kadangi prieš tai buvusiais metais buvo skaitoma, jog apie negatyvų atsakomųjų sankcijų poveikį Europos Sąjungos ekonomikai gali kalbėti tik „Kremliaus propaganda“. Esą, Rusija – tai „ekonominis nykštukas“. Ji gali savo oponentus gąsdinti branduolinėmis raketomis, į jų rinkimus ir referendumus  siųsti „rusų hakerius“, bet tai elgetų bei vargšų šalis, ekonomikoje nesugebanti atsakyti smūgiu į Vakarų smūgį. Todėl maisto produktų iš ES embargo  - tai plačiai nuskambėjęs rusiškas „o atsakydami mes bombarduosime Voronežą“.

Dabar Europos Sąjunga – pati „Kremliaus propaganda“. Briuselio valdininkas patys skundžiasi PPO: Rusijos veiksmai, išstumiant europiečius iš tėvyninės rinkos, ES ekonomikai padarė 290 milijardų eurų dydžio žalą. Tie valdininkai – Kremliaus agentai? Ar tai Putinas vertė juos kartoti tai, ką sako „Kremliaus propaganda“: sankcijų karas bumerangu muša tuos, kurie jį pradėjo?

Ir kas yra pažymėtina, baiminasi tie patys žmonės, kurie 2014 metais ruošėsi draskyti į skutus Rusijos ekonomiką ir tuo privertė Maskvą užsiimti maisto saugumo problema. Rezultatas: paskutiniais dvejais metais Vakarų žiniasklaida reguliariai publikuoja, jog „kviečių eksportą Rusija gali paversti spaudimo įrankiu šalims, kur, dėl klimato kaitos kilęs maisto produktų stygius, joms neleis pasirinkti“.

Vakarams netikėti chamono bei parmezano uždraudimo Rusijoje padariniai – tai tik vienas pavyzdys to, kokias nemalonias pasekmes pageidaujantiems „nubausti Putiną už jo elgesį“ sukėlė „sankcijų karas“. Tai seka iš to pačio skundo PPO dėl Maskvos.

Rusija atsisako pirkti vakaruose (kur, minutėlę, ji oficialiai yra paskelbta strateginiu priešu) transporto priemones, įrangą, medicinos prietaisus ir tekstilės gaminius – skundžiasi Europos komisija. Ką tai reiškia? Tai, jog visą tai Rusija gamina pati.

O pasipiktinimas jos „skaitmenine ekonomika“ išverčiamas sekančiai: kokia prasmė bauginti Rusiją SWIFT atjungimu, jei dabar ji turi savo mokėjimų kortelę „Mir“ ir Rusijos Banko finansinių pranešimu perdavimo sistema (FPPS) – visiškas SWIFT analogas? Neteksime Rusijos rinkos ir šioje sferoje, turėsime tiesioginių nuostolių, o Kremlius vis vien nepakeis savo politikos.

Politiniai uždaviniai neišspręsti, ir, kartu su tuo, patirtos neatlyginamos finansinės išlaidos.

Tik prie ko čia Rusija? Visiškai ne Rusija 2014 metais tikino europietiškus sąjungininkus jos atžvilgiu organizuoti sankcijų politiką.

Bet kokiu atveju, Briuselio biurokratai suras metodus Lietuvai ir Latvijai. O gauti kompensacijas už importo pakeitimą iš Rusijos pas Europos Sąjungą tikimybė tokia pati, kaip ir pas Pabaltijį – „už sovietinę okupaciją“.

Tai yra siekianti nulį.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 16 — id: `scraped:rubaltic_lt:aa637ef391778b35`

**Title:** Krymo susijungimo su Rusija technologiją išrado Lietuva siekdama užgroti Klaipėdą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Paskutiniaisiais kelėtą mėnesių Kaliningrado srityje aktyviai aptariama Lietuvos ginčijama tema dėl „gintaro krašto“ priklausymo Rusijai teisėtumo ir „Mažosios Lietuvos“ doktrinos prastūmimo. Regiono žiniasklaidoje buvo publikuojama, ir Kaliningrado srities Visuomenės rūmuose vyko vieši šios temos aptarimai. Ar tai tiesa, jog Lietuva Kaliningrado srityje paslapčia platina separatistines nuotaikas, kam skiriama „Mažosios Lietuvos“ mitologija, ir kaip Lietuva kovoje už susijungimą su „Mažąją Lietuva“ išrado „mandagių žmonių“ technologiją, apie visą tai RuBaltic.Ru analitikos portalui papasakojo Kaliningrado istorikas, I. Kanto Baltijos federalinio universiteto Geopolitinių ir regioninių tyrimų instituto Istorinės atminties tyrimų centro jaunesnysis mokslinis bendradarbis Albert ADYLOV.

- Iš vietinių gyventojų – ne. Bet tai, jog iš užsienio, iš Lietuvos toks požiūris buvo platinamas ir platinamas dabar, nėra jokia paslaptimi. Faktiškai dėl to ir įsteigta Mažosios Lietuvos reikalų taryba.

Vietinės lietuviškos organizacijos Kaliningrado srityje tiesiogiai apie tai nieko nekalbėjo, suprantama, todėl kad tai iššauktų aštrią reakciją.

Konkrečiai, dar iki Sovietų Sąjungos subyrėjimo, aš asmeniškai atsimenu, 1990 metais paprastuose miesto spaudos kioskuose, kaip prekė, kurią kaip kokius tai ženkliukus, žinote, atveža ir parduoda, pardavinėjo geografinius žemėlapius su Rytų Prūsijos miestų herbais. Bet visi pavadinimai, visa toponimika buvo lietuvių kalba, įskaitant ir tą Rytų Prūsijos dalį, kuri dabar priklauso Lenkijai, kuri tikrai iš viso niekada niekaip nebuvo susijusi su šia toponimika.

Tai buvo 1990 metais, tai aš atsimenu puikiai. Pas mane kažkada toks žemėlapis buvo, bet aš jo neišsaugojau, eilinio persikėlimo metu šis raritetas pražuvo. Bet manau, jog pas kažką jie yra, kadangi čia jie buvo parduodami dideliais tiražais.

Atmintinas atvejis buvo Nesterove, Lietuvos pasienyje, 2010 metais, kai panašaus turinio brošiūros buvo rastos mokykloje, mokyklos bibliotekoje. Visa tai buvo pateikiama kaip nekalta kultūrinė veikla.

Problema buvo tame, jog išskyrus tikslinę auditoriją, to niekas negalėjo perskaityti. Atitinkamai, niekas negalėjo suprasti, kas ten parašyta. Kai šis atvejis tapo žinomu, tų brošiūrų kaina buvo direktoriaus pareigos, ir su tuo pakankamai greitai išsiaiškino.

- Lietuvių kalba, taip, literatūra, kuri buvo platinama tarp vietinių lietuvių.

- Mano nuomone, lietuvių kalba, čia, neskaitant lietuvių, daugiau niekas neskaito, vadinasi, taip. Sudėtingumas tame, jog, skirtingai nuo lenkų kalbos, kadangi lietuvių kalba – ne slavų, tokiame apytikriame supratimo lygyje nesuveiks, čia visgi reikia kalbą mokėti.

- Gali būti dvejos šio proceso medalio puses. Iš vienos pusės, tikriausiai, tai paprasčiausias šios idėjos entuziastų, žmonių kurie tuo užsidegę, užsiėmimas. Gal būt, tai jie daro be jokio tikslo ir pasisekimo vilties.

O jei atplėšimo scenarijus realus, tai, atitinkamai, kyla klausimas „O kas bus toliau?“ Suprantama, jog vokiškas variantas išbrauktas, kadangi jis automatiškai sujauks visą likusį Rytų Europos žemėlapį. Gi, ne tik Maskva 1945 metais prisijungė Vokietijos teritorijas? Tai padarė Lenkija Čekija, ir, bendrai pasakius, ta pati Lietuva Lietuvos TSR formate. Iškils pagristi klausimai. O štai, idėja paskirti kokį tai šios teritorijos kuratorių iš artimiausių kaimynų, Lietuvos ar Lenkijos, gali kai ką sudominti.

Kartu su tuo, ir vėl, kai kalba, jog to negali būti, niekas nekeis teritorijos etninę struktūrą... kiek mes atsimename, prieš 30 metų viskas buvo va taip, o dabar viskas pasikeitė. Pavyzdžiui, buvusios Jugoslavijos teritorijoje. Ir kituose teritorijose.

Todėl realiai visko gali būti, absoliučiai visko.

Konkrečiai, vietiniame kaliningradietiškame Facebook segmente paskutiniu metu labai aktyvus toks veikėjas Kęstutis Čeponis, kuris labai atvirai, rusų kalba Kaliningrado srities rusakalbių bendrijose pareiškia, jog tai lietuviška teritorija, ir, galų gale, mes jus visus iš jos išvarysim. Ir įdomu tai, jog kaip pavyzdį jis pateikia Kosovo. Kadangi albanai – yra šios teritorijos autochtonai, kurie ten gyveno iki slavų, ir tai, kas dabar ten įvyko, serbų etninių valymų organizatorių požiūriu, tik istorinės teisybės atstatymas. Tai tikslūs šio žmogaus žodžiai.

Iš kitos pusės, Čeponis, žinoma, demonstruoja kokį tai savo personos nerimtumą, kadangi ten jis smulkiai pasakoja apie savo dalyvavimą kokiose tai sovietmečio periodo pogrindinėse organizacijose. Pati ši idėja kai ką gali ir suinteresuoti, ir iš tikrųjų ne tokia jau ji nereali.

Tame tarpe ir „Mažosios Lietuvos“ scenarijus.

Kitas momentas, kaip į tai pažiūrės čia gyvenantys lietuviai. Tai gana taikūs žmonės, bendrai paėmus, lojalūs Rusijai, lojalūs iš pat pradžių nuo to momento, kai jie atvyko čionai atstatyti iš griuvėsių Kaliningrado sritį. Bet visai kitas klausimas, kur juos ves vadai, lyderiai, jai kas atsitiks.

Šiuolaikinis lietuviškų gyventojų srityje procento lygis (12 tūkstančių žmonių) nėra toks, jog apie jį iš vis kalbėti, kaip apie kokį tai reikšmingą faktorių. Bet, ir vėl, bet kokių tai geopolitinių pokyčių atveju viskas yra galima.

- Sakykim taip, šiuo atžvilgiu ja bando remtis, nors, kartoju, didelė dauguma Kaliningrado lietuvių visiškai lojalūs Rusijai žmonės. Tai, suprantama, kaip aš tai jaučiu: tie su kuriais aš susitikinėjau, bendravau.

Kitas reikalas, jog iš ten su jais dirbama naudojant tokius klastingus momentus, kaip kalba, kultūra.

Tai yra, prisidengiant tuo, kad žmonės neužmirštų savo kalbą, kultūrą, įkala, tame tarpe, ir štai šias brošiūrėles, kuriuose detaliai aiškinama, jog iš tikrųjų jie yra vieninteliai autochtoniniai gyventojai; vieninteliai, kurie čia turi teises.

O visi likę, tai taip, atvyko kokiam tai laikui.

Kokio pobūdžio aktualizavimas? Informacinio?

Tikriausiai tai bus. Bet tai bus koks tai vidaus politikos įvykis, kuris jokių padarinių Kaliningrado sričiai nesukels.

Tuo labiau, aš netgi pagalvočiau apie tai, jog Klaipėdos sukilimo, taip vadinamo, šimtmetis – tai labai įdomi dingstis mums pamastyti apie savo istoriją. Todėl, jog, susiejant su Krymu, mus bando prispausti „mandagiais žmonėmis“.

Tai ne paprastai tas pats, šia technologiją išrado lietuviai.

Pakankamai gerai aprašyta, kokiu būdu lietuviai skverbėsi į Memelį prisidengdami turistais ar kokiais tai komersantai, o „D“ dieną jie legalizavosi. Tik su vienu dideliu skirtumu: lietuvių procentas Klaipėdos krašte buvo ne toks didelis, kaip rusų procentas Kryme, Kelis kartus mažesnis.

Faktiškai, pagrinde buvo remiamasi tais lietuviškais „mandagiais žmonėmis“. Kodėl? Todėl, jog tuo momentu šioje teritorijoje Vokietijos valstybė fiziškai nevykdė jurisdikcijos. Jurisdikciją vykdė prancūzų okupacinė valdžia, kuri buvo patenkinta tuo kas įvyko, ir netgi neatkreipė dėmesio į tai, jog lietuviai nužudė viena prancūzų karį, kuris žuvo atsitiktinai ir dėl to prancūzai jokių pretenzijų nepateikė.

Kas ir buvo padaryta. Mano nuomone, šis pavyzdys – labai geras rodiklis to, jog kai mums bando durti į akis, tegul pažvelgia į save ir supranta, jog viskas kas nauja – tai gerai užmiršta seną.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 17 — id: `scraped:rubaltic_lt:5f34f62a08fb7f6b`

**Title:** Vilnius prisižaidė: baimindamiesi Kinijos, investoriai uždarys gamyklas Lietuvoje

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Nukreipta prieš Kiniją politika kiekvieną dieną Lietuvai pateikia naujus nemalonius siurprizus. Vokietijos verslininkai perspėjo, jog gali uždaryti savo įmones Lietuvoje ir išeiti iš šalies dėl blogėjančių Lietuvos ir Kinijos santykių. Galima neabejoti, jog tarp Vilniaus ir Pekino verslas pasirinks KLR. Kinija demonstruoja nepalaužiamą tvirtumą baudžiant Vilnių už priešiškumą, ir investoriai nerizikuos ryšiais su pagrindine ekonomine planetos supervalstybe dėl, vertos pasigailėjimo, Lietuvos.

„Vilniaus politikai gali manyti, jog Kinijos ir Lietuvos prekyba yra tokia menka, jog jie gali neprotingai pasinaudoti „Taivano korta“, tam, kad įsiteikti Vašingtonui, tikėdamiesi už tai būti paplotiems per pečius. Niekada nereikia neįvertinti Kinijos ryžto ginti savo nacionalinius interesus. Kai liečiami tokie pagrindiniai klausimai, kaip „Taivano“, ten nėra vietos manevrui. Vilniaus politikai apie tai, vienokiu ar kitokiu būdu, būtinai sužinos“, - rašo Kinijos Komunistų partijos leidinys – laikraštis Global Times.

„Lietuvos veiksmai tiesiogiai pažeidžia „vienos Kinijos“ principą ir rimtai palaužia nacionalinius Kinijos interesus, kas, savo ruožtu, be abejonės, labai rimtai atsilieps lietuviškom prekėm Kinijos rinkoje“, - žada leidinys.

Įrodymai, jog kinai neduodą tuščių pažadų, pasirodo non stop režimu. Tik prieš savaitę Lietuvos URM skundėsi, jog Kinija grasina neleisti į savo vidaus rinką tarptautines kompanijas, kurios tęsia bendradarbiavimą su Lietuva.

Vokietijos – Baltijos šalių prekybos rūmai nusiuntė Lietuvos URM ir ekonomikos ministerijai raštus, perspėjančius apie galimą savo gamyklų Lietuvoje uždarymą ir gamybos pervedimą į kitas šalis. Priežastis? Pekino ir Vilniaus ekonominių santykių pablogėjimas (skaityk: kinų sankcijos Lietuvai) kelią didelį užsienio verslo susirūpinimą.

Vokiški pinigai, kaip ir bet kokie pinigai, mėgsta tylą. Lietuvos užsienio politika apie bet ką, tik ne apie tylą. Todėl europietiški investoriai įtaigiai aiškina: jei Vilniaus ir Pekino ekonominiai santykiai nebus atstatyti (tai yra, jei Kinija ne atšauks savo sankcijas Lietuvai), tai verslo partneriai iš Vokietijos atsisakys turėti reikalų su Lietuvos Respublika.

Lietuvišku lazerio klasteriu vietiniai „patriotai“, kaip tai nebūtu kvaila, labai didžiavosi, kažkaip tai nepastebėdami, jog šiame klasteryje sukasi pinigai iš užsienio, o produkcija tiekiama į „autoritarinę Kiniją“, kovą su kuria tarptautinėje arenoje „branduolinis“ konservatorių partijos elektoratas aktyviai remia. Greitu laiku šis paradoksas liks praeityje. Didžiuotis lazerių gamyba su nepatikimais partneriais iš užsienio neteks, kadangi lazerių gamybos Lietuvoje nebus.

Lygiai taip pat, kaip ir kitų gamybų, kurioms komplektuojamos dalys importuojamos iš Kinijos, o produkcija tiekiama į KLR.

RuBaltic.Ru analitikos portalas anksčiau prognozavo, jog grėsmingi kinų pažadai apie Lietuvos ekonominės blokados organizavimą taps veiksmais, ir Vilniuje artimiausiu metu kils problemos su užsienio investoriais. Prognozė išsipildė vos praėjus kelioms dienoms.

Pabandysime numatyti dar vieną prognozę.

Lietuvos URM vadovas Gabrielius Landsbergis dėl ateinančių iš „kinų fronto“ neramių naujienų iš naujo pilnu pajėgumu įjungė diplomatinę sireną ir pradėjo čirkšti apie solidarumą, europietiškas vertybes ir apie tai, jog europiečiams reikia „vieningu frontu“ atremti ekonominį KLR spaudimą...

Tik verslui tas čirškėjimas apie solidarumą ir vertybes – tuščias garsas. Valdininkai iš Europos komisijos dar išreikš savo gilų susirūpinimą ir pareikš Lietuvai savo garsųjį solidarumą. Jiems pagal pareigas priklauso pasisakyti nieko nereiškiančiomis budinčiomis frazėmis.

Jam situacija nėra aptariama. Iš vienos pusės, yra Kinija – pati didžiausia pasaulyje rinka, pasireiškianti žymiu savo ekonominiu buvimu visose planetos kampeliuose. Iš kitos pusės – Lietuva, kuri pasaulio ekonomikos mastu – iš vis niekas. Visiškas nulis.

Kurią, iš tų dvejų paaukos tarptautinė kompanija, jei ji bus priversta rinktis? Retorinis klausimas.

O be investorių iš užsienio Lietuvai liks tik europietiškų dotacijų parama bei vidiniai rezervai, kurių, mirštančioje su 2,8 milijonais gyventojų šalyje, be gamtinių resursų ir su išprotėjusia vadovybę, nėra.

Ir jau niekada nebebus.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 18 — id: `scraped:rubaltic_lt:95b3356c93058fb9`

**Title:** „Rusijos sulaikymo“ bumerangas: Europa atsidūrė ant energetinės katastrofos slenksčio

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Dujų kainos Europoje pasiekė absoliutų istorinį maksimumą – 2 tūkstančiai dolerių už tūkstantį kubinių metrų. Europiečiai neįgali pirkti kurą už tokią kainą, o ir dujų tiekimas į kontinentą nutraukiamas. Europos sąjunga tenkinasi savo energetinės politikos vaisias: ilgalaikių kontraktų su „Gazpromu“ atsisakymu, ne paremtos rinkos santykiais energetikos vystymu ir protingų rinkos projektų, dalyvaujant RF, blokavimu. Visa ši veikla buvo įkvėpta „Rusijos sulaikymo“ idėja ir atsiliepė energetikos rinkos degradavimu, dėl ko šią žiemą europiečiams gresia masinis išmirimas sušalus savo butuose.

Savaitės pradžioje buvo pristabdytas dujų tiekimas “Jamal-Europa” dujotiekiu. „Gazprom“ nutraukė dujų tiekimą per „Jamal-Europa“ dujotiekį į Vokietiją, kadangi ten nėra paklausos šioms dujoms. Priežastis?

Pagrindinė ES ekonomika tiesiog neturi tiek pinigų, kad mokėti po 2 tūkstančius dolerių už tūkstantį kubinių metrų – būtent už tokią kainą Europos biržose gruodžio 21 dieną buvo pardavinėjamos dujos.

„Kada visi kalba ir vakarų žiniasklaida rašo apie šitą situaciją, kažkodėl tai pamirštama, jog kitame vamzdžio gale yra vartotojas, ir jis nustato, kiek dujų reikia praleisti vamzdžiu. Jei jis pirks daugiau, bus pumpuojama daugiau. O visi situaciją pateikia tokiu būdu, būk tai „Gazprom“ yra toks klastingas, kad ima ir nepumpuoja. Jis pumpuos, kada iš jo pirks“, – taip „RuBaltic.Ru“ portalui situaciją energetikos rinkoje pakomentavo Nacionalinio energetinio saugumo fondo vedantysis analitikas Igoris Juškovas.

Mikroekonomikoje susiklosčiusi situacija vadinama paklausos degradacija. Prekė neperkama, nes už ją neįmanoma susimokėti. Anomališkai aukšta kaina yra lygiai taip pat bloga kaip pardavėjui, taip ir pirkėjui. Ir tuo pačiu metu situacija rinkoje yra tokia, kad šitos kainos numušti nesigauna.

“RuBaltic.Ru” analitikos portalas daug kartų rašė apie šį rudenį kilusios anomalijos priežastis, kurios rezultate dujų kainos muša visus istorinius rekordus. Šalta 2021 metų žiema, ištuštinusi dujų saugyklas, atsistatantis pasaulinės ekonomikos augimas po praėjusių metų „covid krizės". Tačiau visa tai yra situaciniai veiksniai. Be jų yra dar ir sisteminių priežasčių, dėl kurių būtent Europa tapo pasaulinės energetinės krizės epicentru.

Visų pirma, Europa dabar neturėtų tokių problemų, jei jos šalys nebūtų atsisakiusios ilgalaikių sutarčių su „Gazprom“ sudarymo praktikos už fiksuotą kainą, nepriklausančią ir nekintančią nuo rinkos svyravimų. Tačiau profesionalūs kovotojai su Rusiją ilgą laiką ir nuosekliai torpedavo šią praktiką, įrodinėdami, kad „Gazprom“ kainos yra per daug aukštos ir neteisingos. Jas galima ir reikia sumažinti perkant dujas biržoje, kur rusiška produkcija konkuruos su daugeliu kitų pasiūlymų.

Ir štai dabar “kovotojai” gavo klasikinį „už ką kovojo, ant to ir užsirovė“.

Antra, Rusijos buvimui energetinėje rinkoje alternatyvos buvo ne rinkos pobūdžio ir todėl naikino rinką.

Jei konkrečiai kalbėti apie dujų rinką, tai ryškiausias pavyzdys – suskystintos dujos, kurių kaina visada buvo didesnė už „Gazprom“ kainą ir kurias vartotojus privertė pirkti dėl politinių priežasčių – vardan „energetinės nepriklausomybės“ nuo Rusijos.

Donaldas Trampas išsukinėjo rankas vokiečiams, siekdamas priversti Vokietiją, sumokėti už SGD tanklaivius, kompensuojant dešimtmečius besitęsenčią nemokamą JAV karinę apsaugą . Lietuvos vyriausybė išsukinėjo rankas Lietuvos pramonininkams, kad tie pirktų iš „Independence“ SGD terminalo Klaipėdoje amerikietiškas suskystintas dujas, vietoj pigių „Gazprom“ vamzdynų dujų.

Trečia, netgi dabar, artėjančios katastrofos fone, europiečiai nesugeba atsisakyti energetikos panaudojimo kovoje su Rusija. Naujoji Vokietijos vyriausybė pareiškia, kad dujotiekis „Nord Stream 2“ buvo geopolitinė klaida ir jo paleidimą reikia atidėti iki pavasario, iki vasaros. Vokietijos ministrai mano, kad tokiais savo pareiškimais jie gąsdina Putiną, pareiškia jam ultimatumus, šantažuoja, neleidžia jam „užpulti Ukrainos“. Tiesą sakant, tuo jie smogia pačiai Vokietijai, neleisdami nors kiek pasiūlą priartinti prie paklausos ir suformuoti adekvačią dujų kainą.

Vėlgi, tokia politika tęsiasi jau daugelį metų. Visiems energetiniams projektams, kuriuose dalyvauja Rusija, kaišiojo pagalius į ratus,  tokiu būdu apribodami pasiūlą energijos rinkoje.

Jie neleido statyti pirmojo „Nord Stream“, „Turkish Stream“, nutraukė „South Stream 2“, o dabar spekuliuoja „Nord Stream 2“. Liaudyje toks elgesys vadinamas „pats sau akis išsilupsiu, kad uošvienės žentas būtų kreivas“.

Dujų Europos saugyklose lieka iki sausio, o jeigu ateis šalčiai, tai jos baigsis dar anksčiau. Netgi Vokietija negali sau leisti pirkti dujų dabartinėmis kainomis.

Europos sąjungos šalyse gamyba stoja, o perspektyva būstus šildyti savadarbėmis buržuikomis europietiškiems biurgeriams tampa vis labiau realesnė.

„Rusijos sulaikymo „ bumerangas grįžta tiems, kurie jį paleido.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 19 — id: `scraped:rubaltic_lt:9dc48739b0ae0aaf`

**Title:** Europa juokiasi iš mūsų: verslas pasmerkė Lietuvos užsienio politiką

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Europos Sąjungos institucijų kuluaruose juokauja, jog Lietuvą yra pavojinga šalimi investicijoms. Apie tai „Žinių radijui“ sakė Vilniaus pramonės ir verslo asociacijos (VPVA) prezidentas Sigitas Besagirskas. Pasak jo, vieši protokoliniai Briuselio biurokratų pasisakymai skiriasi nuo to, ką jie kalba neformalių pokalbių metu. Viešai europiečiai remia Lietuvą, bet kuluaruose juokauja dėl jos neįžvalgios politikos.

Sigitas Besagirskas – ilgametis Lietuvos pramoninkų konfederacijos funkcionierius, buvęs šios organizacijos ekonomikos ir finansų departamento direktorius. Jo komentarai dėl aktualių įvykių šalyje ir už jos ribų niekada nebuvo politiškai korektiškais.

Pavyzdžiui, tolimais 2009 metais Besagirskas šešėlinę ekonomiką pavadino gerove Lietuvai: „Šešėlinė ekonomika daugiau gelbsti Lietuvai, nei jai kenkia,(...) Būtu kur kas daugiau problemų, jei lietuviai būtu sąmoningi ir mokėtų visus mokesčius“.

Jau po to, kai Ukrainoje pasikeitė valdžia, Besagirskas pasisakė: „Jei Lietuvos politikai neužsiiminės savireklama dėl sankcijų, priskirdami jas prie savo pasiekimų, o rodys jas kaip bendrą ES kūrinį, gal būt tada Lietuvai ir neteks nuo Rusijos“.

Žinoma, politikai jo nepaklausė – viso to gale Baltijos šalys tapo sankcijų karo su Rusija aukomis.

„Jau Briuselyje apie tai kalba, koridoriuose juokauja, kad Lietuva yra padidintos politinės rizikos šalis (...) Yra politinis tekstas, kurį būtina sakyti ir yra realus gyvenimas, kuris šiek tiek skiriasi nuo to politinio teksto“, – teigia S. Besagirskas. Iš kur jis tai žino? Vilniaus pramonės ir verslo asociacijos prezidentas tvirtina, jog jis pats asmeniškai girdėjo tokias maištingas kalbas: „Praėjusią savaitę buvau Briuselyje. Kalbėjausi su įvairių institucijų žmonėmis, ganėtinai specifiniais klausimais, bet ne vienas pajuokavo, kad Lietuva yra padidintos politinės rizikos šalis. Sakau, kodėl jūsų vadai, Europos Komisijos vadovai taip nešneka. Sako: šneka, tik prie kavos puodelio, o ne iš tribūnos“. Iš to, ką sakė Sigitas Besagirskas, galima prieiti prie dvejų išvadų.

Antra, netgi pirmieji Europos komisijos asmenys apie šią situaciją kalba visiškai ne taip kaip nustatyta.

Sąlyginis britų žurnalistas Edavard Lukas, Europos politikos analizės centro (CEPA) pirmasis viceprezidentas spaudoje gali visokeriopai girti įžūlią Lietuvos užsienio politiką. Ir netgi priskirti jai mitinius jos nusistatymo prieš Kiniją pasiekimus.

„Dabar Lietuva gali laisviau kvėpuoti. Jos ryžtingi ir išradingi veiksmai sukėlė didelį tarptautinį susidomėjimą, ypatingai Vašingtone. Tais laikais, kai egzistuoja rimtos problemos su Rusija ir Baltarusija, visa tai duos savo dividendus. Kitos šalys, kurios kreipiasi į Ameriką pagalbos, turi iš to pasimokyti“, - rašo Lukas.

Europos diplomatijos vadovas Žozef Borel gali ryžtingai smerkti Kinijos prekybinę agresiją prieš Lietuvą, o po to, nusirišęs kaklaraištį, stebėtis: ir iš viso, kodėl Pabaltijo „blusa“ puolė kinų „drakoną“?

Ko jai iš vis reikia?

Kas gi panorės investuoti į šalį, kuri tarptautinėje arenoje elgiasi kraštutiniai agresyviai ir neprognozuojamai?

„Supranta, kad Lietuva jau per daug rizikuoja ir šiandien atsiranda politinė rizika investuoti į Lietuvą, nes neaišku, koks bus kitas žingsnis. Lietuva dabar su kinais, baltarusiais susipyko, o kas bus kiti? Lenkija, gal Vokietija?", – samprotauja Vilniaus pramonės ir verslo asociacijos prezidentas. Dalinai, jis, aišku, perdeda. Tokių konfliktų kaip su Kinija ir Baltarusija, pas Lietuvą su Europos Sąjungos narėmis-šalimis negali būti.

Iš kitos pusės, Vilniaus ir Varšuvos santykiai toli gražu ne idealūs (pačiame žemiausiame taške jie buvo Dalios Grybauskaitės prezidentavimo metu). Kaimynus – latvius Lietuva kaltina tuo, jog jie ne nori paremti Baltarusijos atominės elektrinės boikotą.

RuBaltic.Ru analitikos portalas jau buvo rašęs apie latvių uostų galimybę perimti baltarusiškų trąšų tranzitą, kuris, akivaizdu, greitu laiku paliks Klaipėdą. Scenarijus nėra pats realiausiais, bet nėra jokių garantijų, jog Lietuva tam nemaišys. Ginčas dėl baltarusiško tranzito gresia kardinaliai keisti visą Pabaltijo „seserų“ santykių kontekstą. Tada kokioje padėtyje atsidurs latvių verslininkai, kurie taip neatsargiai investavo į Lietuvą?

Galų gale, šiandieną daugelis europietiškų kompanijų bendradarbiauja su Kinija: arba eksportuoją ten produkciją, arba ją iš ten importuoja. Po nesenų įvykiu, vargu, ar kas iš jų panorės pradėti savo verslą Lietuvoje ir papulti į atidų Pekino akiratį.

Jos valdžia specialiai kelia triukšmą (tikėdamasi, jog jis bus girdimas ir anoje Atlanto vandenyno pusėje).

Galima netgi sutikti su Edvardu Lukas: Pabaltijo respublikos veiksmai sukėlė tam tikrą tarptautinį rezonansą.

Tarptautinės reitingo agentūros kaip ir anksčiau gali girti jos „patrauklų“ verslui klimatą, bet konkretūs investoriai šimtą kartų pagalvos, ar verta į ją investuoti nors vieną centą.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 20 — id: `scraped:rubaltic_lt:a42ce44b426d0670`

**Title:** Kovos laukas – Pabaltijys: JAV ir Rusija slenka link naujos Karibų krizės

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Rusijos pasiūlymai JAV dėl strateginio stabilumo Europoje sąlygų formavimo sukėlė nuspėjamą Ukrainos, Lenkijos ir Pabaltijo šalių pasipiktinimą. Vietinių JAV agentų žūtbūtinis pasipriešinimas bandymams sureguliuoti geopolitinį konfliktą Rytų Europoje dar daugiau apsunkina Maskvai ir Vašingtonui surasti kokius tai sisteminius, nukreiptus į deeskalaciją, susitarimus. Tokiu atveju, vienintelė alternatyva Rusijos ir JAV deryboms – nauja Karibų krizė, kuriai, esant dabartinėm sąlygom, pati tikėtiniausia aikštelė – Pabaltijo šalys.

„Mes sutarėme, jog negalime leisti Rusijai braižyti naujas „raudonas linijas“. Europą negalima dalinti į saugumo sferas, negalima drausti šalims rinktis savo saugumo orientaciją“, - komentavo Lietuvos gynybos ministras Arvydas Anušauskas Rusijos pasiūlymus dėl raštiškų juridiškai įpareigojančių NATO sustabdyti plėtrą į rytus garantijų savo susitikime su kolega iš Vokietijos Kristina Lambrecht.

Lietuvos ministro nuomone NATO plėtros politika – tai klausimas, kuris nėra diskutuotinas su Rusija. Jei dėl NATO karinio buvimo Europoje bus derimasi su Maskva, tai sukels Šiaurės Atlanto aljanso skilimą viduje.

Šių Lietuvos gynybos ministro adresatas ne Kristina Lambrecht ir ne Maskva. Adresatas randasi Vašingtone.

Ir nereikia abejoti, jog Lenkija, Pabaltijo šalys ir kompanija tai padarys. Nereikia pervertinti jų priklausomumo nuo JAV laipsnį. Rytų Europos limitrofai vertingais amerikiečiams gali būti tik kaip rusofobai, todėl absoliutų savo antirusišką tvirtumą jie yra pasiruošę demonstruoti netgi priekaištaujant patiems amerikiečiams. Kai 2009 metais JAV atšaukė priešraketinės gynybos sistemų dislokavimą Lenkijoje, Lietuvos prezidentė Dalia Grybauskaitė netgi boikotavo kviestinę vakarienę su Baraku Obama.

Jei dabar Amerikos prezidentu būtu Donaldas Trampas, jis dėl šių, pačių pasigailėtiniausių Amerikos sąjungininkų užuominų sukeltų skandalą ir į visą tai nusispjautų. NATO narių – šalių, priklausančių nuo JAV karinės pagalbos, jausmus Trampas niekada negerbė.

Su Džozefu Baidenu sudėtingiau. Jo komanda bando parodyti Trampo sugadintų santykių su sąjungininkais iš NATO atstatymą, kaip vieną iš Baideno administracijos pasiekimų. Jo užsienio politikos pasiekimų ne daug, todėl, kas yra, tuo ir džiaugiamės.

Taip, kad grasinimai sukelti skandalą ir vieningu frontu stoti prieš „sąmokslą su Putinu“ Baltiesiems Rūmams yra reikšmingi. Ypatingai, jei tai vyks prieš rinkimus.

Be to, iš Vašingtono pusės iki šiol nebuvo pagarsintas vienareikšmis pareiškimas apie tai, jog Rusijos pasiūlymus dėl NATO buvimo Europoje parametrų patvirtinti raštiškai nėra įmanoma, neįtikinama ir ne aptartina. Tai yra, Baltuosiuose rūmuose pasirengę pokalbiui šia tema su Kremliumi. Kitas reikalas, jog surasti kokį tai kompromisinį šios temos sprendimą Vašingtonui su Maskva bus nelengva, o esant sąlygoms, kai jų derybas lydi Rytų Europos „išdavystės liudytojų„ choras, beveik neįmanoma.

Šis choras jau dabar įjungė visas savo balsų galimybes. Apie tai, jog neįmanoma priimti „europietiškam saugumui katastrofiškus“ reikalavimus, jau paskelbė Estija, Latvija, Lenkija, Lietuva, Ukraina. Kuo didesnis progresas bus pasiektas Rusijos ir JAV derybose, tuo garsiau skambės šis suvestinis ansamblis.

Atinkamai, deeskalacijos derybų keliu viltys tampa vis labiau iliuzinėmis. O kokia alternatyva? Susikaupusį prieštaravimų kamuolį galima iš išnarplioti tik dvejais būdais: derybos arba didelio masto karinė krizė.

Čia netgi yra daugiau tikimybės, jog Pabaltijo šalys taps karinio-politinio susirėmimo aikštele, negu Ukraina. Po video pokalbio su Rusijos prezidentu Vladimiru Putinu, Džozefas Baidenas Amerikos pozicijas derybose nurodė sekančiai: karo atveju, JAV už Ukraina su Rusija nekariaus, kadangi Ukraina ne NATO narė. Visai kitas reikalas – šalys kurios jau yra aljanse. Šiuos savo sąjungininkus, karo atveju amerikiečiai, žinoma, parems.

Ir patvirtino ketinimą nusiųsti papildomas karines pajėgas į NATO „rytinį flangą“.

Tačiau, Rusijai jokios principinės reikšmės neturi, būtent kur bus dislokuotos amerikiečių smogiamosios grupuotės: greta Charkovo ar Talino. Tai variantai iš serijos „abu blogesni“.

Ar tai Pabaltijys, ar tai Ukraina – visa tai ribojasi su centrinėmis Rusijos sritimis. Ar iš čia, ar iš ten, raketų atskridimo laikas iki Maskvos ir Sankt-Peterburgo – keletas minučių.

Bet kokiu atveju liečiami gyvybiški Rusijos interesai ir iškyla jos saugumo klausimas. Todėl Maskvos pozicija derybose apie Pabaltijį bus ne mažiau griežtesnė nei derybose apie Ukrainą.

Ir kuo šis susidūrimas besibaigs, pagrindiniais pralaimėjusiais liks pačios Pabaltijo šalys.

Jei nauja Karibų krizė baigsis nauju fundamentaliu susitarimu apie abipusį sulaikymą ir atsižvelgimą į vienas kito interesus, tai Lietuva, Latvija ir Estija taps šių susitarimų objektais, kurių nuomonės po sukrėtimo, atsidūrus prie didelio karo ribos, daugiau niekas ir neklausys.

Na, o jei karo riba bus peržengta, tai iš Pabaltijo šalių, paprasčiausiai, nieko nebeliks.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```
