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

### Article 1 — id: `scraped:rubaltic_lt:718631741184c857`

**Title:** Italų politologas: „Mus šokiravo lietuvių įstatymai“

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Italijoje išleista žurnalistės Galinos Sapožnikovos knyga „Lietuviškas sąmokslas: kaip žudė TSRS“ . Apie tai, kaip knyga buvo sutikta Romoje, portalui RuBaltic.Ru papasakojo leidėjas ir politologas Sandro Teti.

– Pone Teti, kodėl išleisti knygą Jūs nutarėte Italijoje?

– Apie knygą man papasakojo senas draugas — žinomas publicistas, žurnalistas ir politikas, buvęs eurodeputatas Džuljeto Kjeza. Aš iškart susidomėjau, nes žinau, kad Pabaltijyje daugelį metų diskriminuojamos tautinės mažumos. Vėliau, kai sužinojau, kad kalba eina apie 1991 metų sausio 13-osios įvykius, apie naują požiūrį, neoficialią įvykių versiją, aš ir nutariau išleisti knygą. Ir ne todėl, kad visiškai arba dalinai pritariu jos turiniui, o norėdamas, kad italų skaitytojai sužinotų ir pirmą kartą susipažintų su šia versija. Beje, kiek žinau, alternatyvus požiūris į 1991 metų įvykius gali tapti Lietuvoje baudžiamojo persekiojimo priežastimi, nes pagal Lietuvos įstatymus negalima neigti oficialios valdžios versijos. Todėl tegul italų skaitytojai patys nusprendžia, kaip galvoti, tegul farmuoja savo nuomonę ir lietuvišką versiją lygina su ta, kurią pateikia Sapožnikova.

Knygoje labai daug įrodymų, faktų, virš 20 interviu su liudininkais. Aš manau, kad knyga skatina nuomonių pliuralizmą, ji bus labai naudinga.

Aš to nesuprantu. Juk Lietuva — Europos Sąjungos narė. Lietuviai turi gerbti nuomonių pliuralizmą ir židžio laisvę.

– Kaip suprantu, Lietuvos ambasadorius bandė kištis į tai, kas vyko parlamente? Ar kas nors panašaus buvo pastebėta anksčiau Italijos istorijoje? Kad užsienio politikas ar diplomatas taip pasielgtų?

– Taip, jis sėdo ir parašė spikeriui Pjetro Graso protesto notą, kurioje prašė atšaukti užplanuotą renginį. Žinoma, jo pastangos buvo bergždžios. Daugiau panašių atvejų aš nepamenu. Tai, mažiausiai, labai netinkamas žingsnis.

– Kaip manote, kas paskatino ambasadorių taip pasielgti?

– Manau, Lietuvos politikai bijo, kad Vakarų visuomenė sužinos naujas šalies istorijos detales. Kitos priežasties nematau.

– Kaip italų deputatai reagavo į pristatymą?

– Mes pristatėme knygą diskusijų, pristatymų ir konferencijų salėje. Žinoma, dalyvavo parlamentarai, atėjo labai daug žurnalistų. Buvo ir oponentų. Dalyvavo Italijos universiteto profesorius, kuris kritikavo autorės išvadas. Tačiau dauguma dalyvių palaikė knygą. Klausimai ir diskusijos truko keletą valandų, dėl triukšmingų diskusijų renginys užsitęsė.

Deputatai gana gerai reagavo ir demonstravo susidomėjimą. Ir domėjosi įvairių politinių požiūrių deputatai. Jie nebuvo susipažinę su aprašytomis istorijomis. Manau, jog artimiausiais mėnesiais ne tik politikai, bet ir eiliniai Italijos piliečiai bei žiniasklaida aktyviai svarstys Sapožnikovos iškeltus klausimus.

Tai sužinojusi auditorija patyrė šoką.

– Pati Galina Sapožnikova pasakojo mums, kad italus taip pat nustebino taip vadinamų „raudonųjų profesorių“ likimas — komunistų, kuriuos 90-aisiais, byrant TSRS, Lietuvoje nuteisė už veiklą...

– O tai praktiškai žodžio laisvės pažeidimas! Nesuprantu, kaip tai gali būti. Ir čia matome informacijos stoką ne tik Italijoje, bet ir visuose Vakaruose. Ir todėl visos šios krypties publikacijos yra sveikintinos.

Mes ketiname tęsti knygos pristatymą. Rugsėjo-spalio mėnesiais planuojame ją pristatyti Milano ir kituose Italijos miestuose. Pakartosiu savo, leidėjo, poziciją: svarbiausia — sudaryti italų visuomenei galimybę palyginti du skirtingus požiūrius. Iki šiol Italijoje egzistavo tik Lietuvos valdžios požiūris. Sapožnikovos knygos pasirodymas skatina informacinį pliuralizmą.

– Kaip italų žiniasklaida įvertino pristatymą?

– Žiniasklaida, mano manymu, reagavo gana vangiai, tačiau rudenį mes surinksime jau daugiau žurnalistų. Tikiuosi, jog pavyks pralaužti tą izoliaciją, į kurią pateko Lietuvoje opozicinės jėgos.

– Ar italų visuomenė turi supratimą apie bendrą situaciją Baltijos šalyse? Pavyzdžiui, apie Jūsų paminėtą situaciją su nepiliečiais.

– Deja, ne. Aš, kaip žmogus, kuris seka įvykius, vykstančius potarybinėje erdvėje, žinoma, žinau šią temą. Tačiau dauguma italų net neįtaria, kad Baltijos šalyse pažeidžiamos žmogaus teisės. Tikiuosi, jog minėta knyga padės žmonėms visa tai sužinoti.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 2 — id: `scraped:rubaltic_lt:e07ced4525c82322`

**Title:** „Nemanau, kad mano knyga bus laisvai pardavinėjama Pabaltijyje“

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Romoje praėjo žurnalistės ir „Komsomolskaja pravda“ apžvalgininkės Galinos Sapožnikovos knygos „Lietuviškas sąmokslas. Kaip žudė TSRS“ pristatymas. Apie knygos istoriją ir aprašomų įvykių aktualumą portalui RuBaltic.Ru papasakojo autorė.

–  Galina, kodėls Jūs ėmėtės šios knygos?

– Pirma, aš pati dalyvavau šiuose įvykiuose. 80-ųjų pabaigoje, kai byrėjo Tarybų Sąjunga, aš dirbau Estijoje „Komsomolskaja pravda“ korespondente. Žinoma, stebėjau procesą, vykusį sąjunginėse respiblikose. Tada tai buvo mano pirmoji žurnalistinė patirtis, aplinkiniai įvykiai atrodė visiškai nuoširdūs ir apie jokias politines technologijas mūsų neprityręs skaitytojas neturėjo supratimo. Vėliau situacija ėmė kartotis, mane pastoviai persekiojo dežaviu pojūtis — tai Gruzijoje, tai Ukrainoje, tai Kirgizijoje. Atsirado jausmas, kad visa tai aš jau mačiau — keitėsi tik dalyvių veidai, tautybė ir šalis. Tokiu būdu pamažu akys pradėjo žvelgti pro jas dengusią miglą.

Vienu savo profesinio gyvenimo metu aš rimtai užsiėmiau 1991 metų sausio tragiškų Vilniaus įvykių tyrimu. Pažiūrėjus išsamiau, aš staiga aptikau šioje byloje daug nesusiduriančių galų. Ir darydama tokią išvadą aš nebuvau vieniša. Lygiagrečiai savo tyrimu užsiiminėjo visuomenės veikėjas Algirdas Paleckis, kuris vėliau Lietuvoje buvo teisiamas už nepriklausomą požiūrį. Tuo metu jau buvo išleistos rašytojo ir politiko Vytauto Petkevičiaus ir buvusio Lietuvos KP CK sekretoriaus Juozo Kuolelio knygos. Galų gale išsiskalidė visos abejonės, ir aš supratau, kad mes buvome apgauti, —

Aš ieškojau atsakymo į klausimą „kas atsitiko?“, tačiau mano žurnalistiniame tyrime atsidūrė konkrečių žmonių likimai ir visiškai nei Rusijoje, nei Europoje nežinomi istorijos puslapiai. Būtent: išėjusi iš Tarybų Sąjungos sudėties Lietuva vogčiomis davė startą politinių represijų mechanizmui. Buvo medžiojami kitokią nuomonę turintys žmonės. Daugybė buvusių komunistų faktiškai buvo priversti tapti politiniais bėgliais. Dešimtys žmonių atsidūrė kalėjimuose išgalvotai apkaltinti. Visiškai tragiška istorija nutiko „raudoniesiems profesoriams“: senyvus komunistus, peržengusius 60 metų ribą, pasodino kalėjiman tik už tai, kad jie buvo komunistai! Davė 8, 10, 12 metų... Europa nutylėjo, lyg to nepastebėjusi. Papasakoti apie tai visuomenei laikiau savo pareiga.

Konkrečiai pradėti rašyti knygą mane paskatino dvi istorijos. Pirmoji nutiko 2014 metų gruodį, kai mano akyse Estijoje buvo areštuotas ir iš šalies deportuotas žymus italų žurnalistas Džuljeto Kjeza. Mes su juo seni pažįstami. Ir kada aš jį lydėjau į Maskvą, jis man Talino perone pasakė: „Galina, tu labai svarbių įvykių Pabaltijyje liudininkė. Ir, kaip žurnalistė, tiesiog privalai apie tai parašyti“. Tai tapo startu. O galutiniu „stebuklingu spyriu“, privertusiu sėsti prie rašomojo stalo, tapo manęs pačios deportavimas iš Lietuvos. Aš, gali būti, bučiau keletą metų besiruošusi rašyti, tačiau 2015 metų rugpjūčio 26 dieną raumeningi Lietuvos vyrukai pabandė sustabdyti mano veiklą, kai aš vykau imti interviu iš mokslo daktaro Juozo Kuolelio, praleidusio kalėjime už savo įsitikinimus 8 metus. Pusiaukelėje, tarp miškų ir laukų, mašiną pasivijo policija ir įteikė dokumentą, kad įvažiuoti į šalį man draudžiama penketą metų.

– Kodėl Jūs pavadinote savo darbą „Kaip žudė TSRS“? Net Rusijos istorijos vadovėliuose, iš kurių aš mokiausi, buvo sakoma, kad TSRS subyrėjo savarankiškai — dėl giluminių vidaus problemų ir prieštaravimų, dar ir ekonomikoje. Jūs priėjote kitokių išvadų?

– Nė viena „spalvota revoliucija“ neįmanoma klestinčioje šalyje, čia jūs teisus. Šios technologijos gyvybingos, kai yra uždedamos ant sudribusio kūno, — bet kūnas gyvas, nemiręs! Žinoma, Tarybų Sąjungoje tada egzistavo aibė problem. Tačiau vien tik sudribusio kūno, kaip 80-ųjų pabaigoje atrodė TSRS, buvo maža. Apie ekonominę sudedamąją dabar nekalbu — tai visiškai kita istorija. Apie tai, kaip Saudo Aravija įsivėlė į sandorį su JAV ir sugriovė naftos kainas, nemažai parašė kiti autoriai. Tuometinėje TSRS buvo stokojama neapykantos žmogui sudedamosios.

Todėl maždaug 1985–1986 metais prasidėjo visuotinas „smegenų transformavimas“ — informacinė kompanija diskredituojant valstybę, jėgos struktūras ir kariuomenę. Tai labai primena dabartinius reiškinius. Atkreipkite dėmesį į šių dienų liberalios žiniasklaidos leksiką — maždaug taip kalbėjo šalis. Buvo atlikta galinga savęs žeminimo ideologijos injekcija, privertusi mus patikėti, kad gyvename „kvailių šalyje“, kad blogesnės pabaisos, nei TSRS, žmonijos istorijoje dar neegzistavo...

Mes tai džiaugsmingai „prarijome“. Bet ir tai ne viskas. Reikėjo pasėti tarp žmonių neapykantą. Prasidėjo galingas žmonių tragedijų poetizavimas — aš visų pirma turiu omeny stalinines deportacijas. Ir truputėlis pipirų į viralą — kokios nors garsios laidotuvės. Tuo tikslu ir buvo surengta provokacija Vilniuje. Likti abejingu kai šimtatūkstantinė minia lydėjo 13 karstų, o šie buvo uždengti Lietuvos tautinėmis vėliavomis, nebuvo įmanoma...

Kai po daugelio metų mano rankose atsidūrė Džino Šarpo knyga apie 198 valdžios nuvertimo jėga būdus, viskas sutapo. Reikia aukos? Štai jums ir auka. Jei aukų nėra, būtina padėti joms atsirasti. Reikalingos gražios teatralizuotos laidotuvės? Štai, prašom, laidotuvės. Reikia kad žmonės vienas kitą nekęstų? Lengvai! Tik reikia ištraukti ir molekulėmis išmėtyti kokias nors praeities detales. Esant norui, naudojantis šia technologija, galima per keletą dienų priversti rusus, pavyzdžiui, prisiminti totorių-mongolų priespaudą ir paversti vargšus nekaltus mongolus pagrindiniais rusų tautos priešais...

– Kokių skaitytojų atsiliepimų Jūs laukiate, tame tarpe ir Lietuvoje, į kurią Jūsų neįleidžia? Kritikai kaltina Jus, kad po 25 metų Jūs tiesiog bandote pateisinti TSRS egzistavimą.

– Ką reiškia „pateisinti TSRS egzistavimą“? Ji puikiai egzistavo ir be manęs, ne aš ją pagimdžiau ir ne aš užmušiau. Aš tik duodu teisę pasisakyti žmonėms, kurių 25 metus niekas nenorėjo girdėti, ir sudaužau mitą, kad Lietuva vieningai, šimtu procentu žavėjosi vakarietiškomis vertybėmis. Taip nėra. Lietuvoje mūsų sąjungininkų buvo 50 proc., tame tarpe ir lietuvių. Aš noriu, kad lietuviai pažvelgtų į save iš šalies ir išsklaidytų tuos 25 pastaruosius metus juos gaubiančius dirbtinus debesis.

– Lietuvoje populiari nuomonė, kad „raudonieji profesoriai“ — Burokevičius, Jermalavičius, Kuolelis ir kiti — nenusipelnė tiek dėmesio. Jie laikomi provokatoriais, Lietuvos išdavikais, būrelių senukų, kurie įstrigo praeityje ir „pavėlavo su savo laiku“. Kaip Jūs tai vertinate?

– Tai aklų žmonių pozicija. Italų parlamente, beje, kuriame mano knyga buvo pristatyta birželio 1 dieną, būtent „raudonųjų profesorių persekiojimo istorija iššaukė didžiausią šoką. Tegul Lietuvos prokuratūra pirmiausia praves normalų tyrimą ir paaiškins kaip tragedijos vietoje atsirado 1898 metų pavyzdžio Mosino šautuvo šovinių gilzės — šių šovinių „Alfos“ grupuotė neturėjo savo ginkluotėje. Tegul paaiškins, kiek Medininkų byloje nesiduria galų, o paskui bandys mums pasakoti apie senukus, kurie „pavėlavo su savo laiku“.

O tie, kurie, priešingai, išdavė, dabar užima Lietuvos prezidento ir užsienio reikalų ministro postus.

– Ar tikitės, kad Jūsų knyga galų gale pateks ant Lietuvos, Estijos, kitų Vakarų šalių prekystalių?

– Žinoma! Nors ir abejoju. Mano ankstesnė knyga „Arnoldas Meris. Paskutinis estų didvyris“ ant Estijos prekystalių taip ir nepateko. Papasakosiu linksmą istoriją: aš padovanojau ją vienai estei — aprūpintai, šiuolaikiškai. Mane sukrėtė jos reakcija.

Kai šių dienų europietiškoje visuomenėje, tame tarpe ir Pabaltijyje, tokioje būklėje egzistuoja laisvė, aš visai nesitikiu, kad knyga bus laisvai pardavinėjama, — tai ne Maskva, kur ant knygų prekystalių galima rasti bet kurią alternatyvią nuomonę. Tačiau pažadu: aš sugebėsiu ją padaryti prieinama visuomenei. Galų gale patalpinsiu internete elektroniniame formate. Tai man daug svarbiau, nei honoraras.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 3 — id: `scraped:rubaltic_lt:ccd5e1deeef399a5`

**Title:** Lietuvos gyventojams norima neleisti gauti internetu nepriklausomos informacijos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos radijo ir televizijos valstybinė komisija siūlo blokuoti televizijos kanalus, „skleidžiančius internete propagandą“. Šią iniciatyvą jau palaikė kabelinės televizijos asociacija. Cenzūra Lietuvos interneto tinklo segmente gali oficialiai tapti valstybine Lietuvos Respublikos politika.

Lietuvos kabelinės televizijos asociacija (LKTA) išplatino pareiškimą : „Kabelinė televizija pasiruošusi boikotuoti propagandą internete platinančius kanalus“. Šiuo pareiškimu Lietuvos kabelininkai reiškia solidarumą su partijos ir vyriausybės iniciatyva įvesti interneto tinkle cenzūrą. Čia eina kalba apie blokavimą internete Lietuvoje uždraustų Rusijos televizijos kanalų.

Pastaraisiais trejais metais Lietuva ne kartą draudė transliuoti televizijos kanalus „RTR-Planeta“, „NTV-Mir“ ir 1-ąjį Baltijos kanalą. Tačiau teisingai laisvę suprantantys lietuviai visada rasdavo būdus kaip apeiti Lietuvos radijos ir televizijos komisijos draudimus ir vis tik naudotis „rusų propaganda“. Viena iš tokių galimybių buvo interneto televizija, kurios dalis ryšium su minėtos Komisijos veikla pastoviai auga ir šiuo metu siekia 20 proc. Lietuvos valdininkai šioje situacijoje įžvelgė betvarkę: kova su „rusų propaganda“ neefektyvi, vartotojai iš aukštos varpinės spjauna į jų draudimus! Ir biurokrato mąstymo logika neišvengiamai gimdo sprendimą — blokuoti Lietuvos interneto transliavimą tų kanalų, kuriuos uždraudė Lietuvos radijo ir televizijos komisija.

Būtent šią iniciatyvą palaikė Lietuvos kabelinės televizijos asociacija. Jos nariai pasiruošę blokuoti nelegaliai internete veikiančius kanalus: jie LKTA pareiškime pavadinti „informacijos diversantais“, keliančiais grėsmę Lietuvos saugumui.

Jau sugalvota ideologinė priedanga, pateisinanti cenzūros įvedimą internete bei neprisilaikymo savosios Konstitucijos ir eilės tarptautinių susitarimų (pvz., Europos žmogaus teisių konvencijos 10 str.), kuriuos pasirašė Lietuva. Ši priedanga nekinta jau daugelį metų — „Rusijos grėsmė“. Lietuviai gi — maži vaikučiai, juos nevalia prileisti prie „rusų propagandos“, nes kur tiesa, kur melas, vis tiek nesupras, galvoti savarankiškai, lyginti informaciją ir analizuoti faktus nesugebės ir gali prieiti „neteisingų“ išvadų. Todėl Lietuvai būtina įvesti cenzūrą, ją pavadinant kaip nors gražiau. Na kad ir Lietuvos Respublikos nacionalinio saugumo informacinėje erdvėje užtikrinimu. Kad niekam galvon netoptelėtų...

Vakarų sąjungininkų reakcija į „demokratinę cenzūrą“ bus akivaizdi — nutylėjimas. Ką tik JAV sausumos pajėgų Europoje vadas Ben Chodžes pareiškė, kad reikia aktyviau priešintis Rusijai media erdvėje. Ir Lietuvos valdantieji be abejonės pajėgs įvertinti amerikiečių generolo žodžius kaip Vašingtono palaiminimą apriboti Lietuvoje žodžio laisvę. Tačiau jei ir nebus palaiminimo (juk beveik per trejus informacinio karo metus JAV ir Europa nepasekė įkyriu Vilniaus pavyzdžiu ir neatjungė rusiškų kanalų), ką Vakaruose rimtai sudomins Lietuva? Jei ten kas nors ir sužinos apie Lietuvos valdžios išdykavimus, pasistengs nutylėti. Kaip ne kartą buvo.

„Raudonoji“ prezidentės Grybauskaitės praeitis, korupcijos skandalai vyriausybėje, Lietuvos valdžios kritika Vakaruose ir t.t. iki paskutiniųjų emigravimo iš Lietuvos skaičių gali būti vertinama kaip „rusų propaganda“, kuri kelia grėsmę nacionaliniam saugumui ir todėl turi būti uždrausta. O informacijos šaltinis gali ir nebūti rusiškas — jis gali būti ir vidinis, lietuviškas internete. Vėl gi, valdžia, esant norui, visada jį pavadins „prorusiška penktąja kolona“, „Putino agentais“ ir „Maskvos ranka“. Vadinasi, rusų propaganda; vadinasi, grėsmė nacionaliniam saugumui; vadinasi, blokavimas ir draudimas.

Tokios liūdnos perspektyvos laukia Lietuvos Respublikos gyventojų. Nori būti tikras Lietuvos patriotas — užmiršk įvairius informacijos šaltinius, alternatyvias nuomones, juolab, kad reikia vystyti kritišką mąstymą ir turėti ant pečių savo galvą. Klausyk kreipimosi į tautą Dalios Grybauskaitės ir vyk šalin „priešų balsus“. Tai ir bus tavo europietiškas pasirinkimas, žodžio laisvė ir demokratija.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 4 — id: `scraped:rubaltic_lt:db57e33734b49a1d`

**Title:** Energetinė nepriklausomybė lietuviškai. Vilnius grįžta prie Gazpromo

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuva nepasiruošusi mokėti realią kainą už atsisakymą rusiškų dujų SGD naudai. Perspektyvoje nauji ilgalaikiai kontraktai su Gazpromu. Išgarsinta „energetinė nepriklausomybė“ netapo tokia džiuginanti, kokią ją prieš porą metų piešė oficialus Vilnius.

Lietuva nušoko nuo Gazpromo adatos — džiaugėsi oficialus Vilnius, 2014 metų gruodį įvedęs rikiuotėn plaukiojantį SGD terminalą Klaipėdoje simboliniu Independence pavadinimu. Galėsime derėtis su Maskva, visiškai atsisakysime rusiškų dujų, „melsvu kuru“ aprūpinsime visą regioną — gąsdino Kremlių naujai įgyta „energetine nepriklausomybe“ Lietuvą valdantieji.

„Neseniai mūsų kolegos iš Lietuvos atėjo ir paklausė, ar galėtų sugrįžti prie ilgalaikių sutarčių. Mes, žinoma, pagalvosime, duosim atsakymą, tačiau galvoti reikėjo anksčiau, kai sakė, jog kontraktas nereikalingas“, — pasakė Gazpromo valdybos pirmininko pavaduotojas Aleksandras Medvedevas spaudos konferencijos metu.

Plaukiojantį Lietuvos „energetinės nepriklausomybės“ mitą galutinai sudaužė realybė. Demokratinės norvegų (katariečių, amerikiečių) dujos tapo per brangios. Kaimynams jos nereikalingos. O už Independence nuomą reikia mokėti. Beje, nemažai — 154 tūkstančius JAV dolerių už parą. O ir dirba terminalas beveik tuščiai. Naudojami tik 20 galingumo proc. — praėjusių metų pabaigoje pripažino Lietuvos energetikos ministras Rokas Masiulis.

Respublikos „melsvo kuro“ poreikis 2016 metais — 2 milijardai kubinių metrų. Visi stambieji importuotojai priversti pirkti per Klaipėdos SGD terminalą 1,35 milijardo kub. metrų norvegų Statoil dujų. Likusieji 0,7 milijardo perkami iš rusų vamzdynų pagal „take or pay“ principą. Tokiu būdu 4 milijardų kub. metrų tūrio Klaipėdos terminalas taip ir liks apkrautas ne daugiau ketvirtadalio. Gegužės mėnesį premjeras Algirdas Butkevičius, suprasdamas, kokiuose :energetiniuose spąstuose“ atsidūrė Lietuva, pranešė apie oficialaus Vilniaus ketinimus vėl pradėti derybas su norvegų kompanija Statoil dėl importuojamų SGD kainų sumažinimo. Anksčiau ši kompanija suteikė esmines nuolaidas, tačiau vyriausybė stengiasi dar nors kai ką išsiderėti.

Šių metų pradžioje po sudėtingų ir ilgų derybų Lietuvai pavyko išsiderėti atnaujintą kontraktą, pagal kurį SGD numatyta tiekti 30 proc. pigiau. Buvo pakeista kainodaros formulė: SGD kaina lietuviams sumažinta 15-20 proc. Tačiau, nuolaidžiaudamas, Statoil pareikalavo, kad Vilnius pratęstų 2014 metais pasirašytą penkerių metų sutartį su Lietuvos valstybine monopolija Litgas dar penkeriems metams — iki 2024-ųjų.

Nepaisant kovingų „energetinės nepriklausomybės“ propaguotojų, Vilnius taip ir netapo pionieriumi perkant amerikiečių SGD. Lietuva pasiruošusi įsigyti SGD iškart, kai amerikiečių kompanijos pradės jas eksportuoti, — pasakojo Lietuvos energetikos ministras Rokas Masiulis susitikime su JAV energetikos ministru Ernestu Monizu vasario mėnesį metu. „SGD eksportuotojams mes galime pasiūlyti tiekti per Klaipėdos terminalą ne tik į Lietuvą, bet ir į Latviją bei Estiją, o nuo 2019 metų — Lenkijos ir Ukrainos vartotojams“, — taip Masiulus reklamavo regioninės rinkos ir Independence terminalo galimybes užjūrio kolegoms.

Tačiau perspektyvos pirkti iš lietuvių brangias SGD nenudžiugino kaimynų. 2015 metais estai nupirko iš Lietuvos apie trečdalį respublikai reikalingų dujų (metams reikia 0,6 milijardo kub. metrų). Daugiau neperka. Įmonė Eesti Gaas pasirašė trejų metų sutartį su Rusijos dujų gigantu. Kompanija atsisako viešinti tiekiamų dujų kiekį, tačiau patikino, jog kontraktas tenkina estų vartotojų poreikius.

Panašiai santykiai klostosi ir su Latvija. „Mūsų, latvių, dujų poreikius tenkina ilgalaikis kontraktas su Rusijos Gazpromu. Rinkai dėl dujų pertekliaus nereikalingi papildomi kiekiai“, — pasakojo Latvijas Gāze valdybos pirmininko pavaduotojas Mario Nullmejeris interviu leidiniui Natural Gas Europe.

Todėl, nepaisant pernykščių planų pirkti amerikiečių SGD, Lietuva buvo priversta atsisakyti šių sumanymų. Suskystintos dujos, kurias buvo planuojama vežti iš Meksikos įlankos per visą Atlanto vandenyną į Klaipėdą, „nuostabiu“ būdu tapo brangesnės nei vamzdynais tiekiamos rusiškos. Formali lietuvių atsisakymo priežastis — neatitinka kokybė. „Tos dujos neatitinka kokybės Lietuvoje reikalavimus. Ateityje, jei atitiks, svarstysime“, — pranešė „Lietuvos energijos“ vadovas Dalius Misiūnas, išdrįsęs įžeisti pagrindinius sąjungininkus, pavadinęs jų dujas nekokybiškomis.

O tuo metu Gazpromas ėmė skatinti Pabaltijo vartotojus ir per aukcionų sistemą dalinti papildomus dujų paketus. Kovo viduryje Rusijos dujų gigantas pravedė Baltijos šalims antrąjį aukcioną. Buvo realizuota 80 lotų bendru virš 420 milijonų kub. metrų kiekiu. Ir tuo metu Pabaltijo pirkėjai, kaip teigia Gazpromo valdybos pirmininko pavaduotojas Aleksandras Medvedevas , pareiškė norą grįžti prie ilgalaikių kontraktų. „Akivaizdu, jog pajuto skirtumą, kai rizikuojama ir kaina, ir kiekiu, o kada yra patikimas ilgalaikis kontraktas, kuris leidžia ilgalaikėje perspektyvoje planuoti savo veiklą“, — pasakojo top menedžeris. Štai ir Lietuva atsisakė mokėti už atsisakymą pirkti rusišką „žydrą kurą“ SGD naudai — patriukšmavo ir nusiramino.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 5 — id: `scraped:rubaltic_lt:f21b9c1408c8edec`

**Title:** „Kaip galėjome nežadėti?“ — 10 svarbiausių Pabaltijo suklydimų

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Nuo „dainuojančių revoliucijų“ iki šiol Pabaltijo politikai žada tautai aukso kalnus, tačiau žadėtų klestėjimo ir gerovės nesimato ir nesimatys — tai ekspertai ir blaiviai mąstantys Lietuvos, Latvijos ir Estijos piliečiai seniai suprato. RuBaltic.ru surinko 10 svarbiausių Pabaltijo politikų neįvykdytų pažadų — suklydimų, kurie tapo apgavystėmis ir gyventojų suklaidinimu.

Mes dyvensime kaip danai ir švedai!

Pertvarkos metu Sajūdžio ir Liaudies frontų lyderiai įtikinėjo Lietuvos, Latvijos ir Estijos gyventojus, kad jie gyvena skandinavų šalyse ir, ištrūkę iš TSRS gniaužtų bei “sovietinės okupacijos” pasekmių, pradės gyventi kaip danai, švedai ir suomiai — taps vienos turtingiausių, sočiausių ir geriausiai gyvenančių Europos tautų.

Realybė.Kuo labiau tolsta TSRS subyrėjimas, tuo labiau Pabaltijis atsilieka nuo Šiaurės Europos. „Okupacijos“ pasekmių, neleidžiančių per ketvirtį desovietizacijos politikos amžiaus, pasak vietinių nacionalistų, latviams ir lietuviams pasiekti švedų ir danų lygio, akivaizdu, atsiranda vis daugiau, nes praraja tarp Skandinavijos ir Pabaltijo ne mažėja, o didėja. Pagal ekonomikos lygį, demografijos augimą, socialinę apsaugą tarybinės Lietuva, Latvija ir Estija prie Skandinavijos buvo labiau priartėjusios, nei šiandien. Norvegija ir Švedija pagal BVP asmeniui užima pirmąsias vietas Europoje ir pirmauja ES pagal gimstamumo augimą. Latvija ir Lietuva pagal gyventojų gerovę užima ES paskutines vietas, o gyventojų skaičiaus mažėjimo klausimu pateko tarp pasaulio lyderių.

Pilietybę gaus visi!

Kovodami dėl išėjimo iš TSRS sudėties Pabaltijo separatistai žadėjo, kad atkūrus prieškarines respublikas pilietybę gaus visi pastoviai gyvenantys. „Latvijos LF pasisako už tai, kad pilietybė būtų suteikta visiems pastoviai Latvijoje gyvenantiems, kurie pareikš norą ją įgyti ir savo likimą skirti Latvijos valstybei“, — skelbė Latvijos liaudies fronto programa 1989 metų rudenį.

Realybė. Praktiškai iškart po išėjimo iš TSRS sudėties ir nepriklausomybės atkūrimo beveik visi rusakalbiai Latvijos ir Estijos gyventojai prarado pilietybę, o kartu ir savo fundamentalias politines ir socialines ekonomines teises. Vėliau Laudies frontų lyderiai ir valdžion įkopę Latvijos ir Estijos politikai sąžiningai prisipažino, kad sąmoningai melavo rusų tautybės gyventojams. „Argi galėjome nežadėti?“ — ši ekspremjero Einarso Repše frazė tapo Latvijoje priežodžiu.

Pabaltijis taps tiltu tarp Rusijos ir Vakarų!

Nuo pertvarkos laikų Pabaltijo politikai žadėjo Rusijai, pasauliui ir savo gyventojams, kad nepriklausomos Lietuva, Latvija ir Estija taps geopolitiniu „tiltu“ tarp Rusijos ir Vakarų, padės integruotis Rusijai į vakarietišką pasaulį, taps tarpininkėmis ir organizuos dialogą tarp Maskvos, JAV ir Europos Sąjungos.

Tikrovė. Paskelbusios „antrąją nepriklausomybę“  Baltijos šalys tapo smulkiomis provokatorėmis, ardančiomis Rusijos ir Vakarų dialogą ir atsakingomis už antirusišką Europoje isteriją. Nuo 1991 metų jų santykiai su Rusija apsiribojo reikalavimais „kompensacijos už okupaciją“, pretenzijomis dėl teritorijų, parama čečėnų kovotojams ir antirusiška veikla buvusiose tarybinėse respublikose. Vietoj geopolitinio „tilto“ Pabaltijis tapo buferine zona, varančia pleištą tarp Rusijos ir Europos ir besistengiančia įtakoti „Rytų partnerystės“ šalis.

Mes pastatysime naują, efektyvesnę ir ekologiškai saugią AE!

Ieškodami argumentų, pateisinančių vienintelės Pabaltijyje atominės elektrinės likvidavimą, Lietuvos dešinieji tvirtino, kad Ignalinos AE — „okupacijos palikimas“: ji sieja Lietuvą su Rusija, daro ją ekonomiškai priklausomą, be to, nesaugi ekologiškai. Todėl Ignalinos AE būtina uždaryti, o vietoj jos pastatyti naują — vakarietišką, šiuolaikišką, progresyvią ir ekologiškai saugią.

Tikrovė. Ignalinos AE likvidavo, Visagino AE... Na, žinote: „stato“, „artimiausiu metu užbaigs“.

Įvedus eurą kainos nepakils!

Prieš euro įvedimą savo laiku pasisakė dauguma Estijos, Latvijos ir Lietuvos gyventojų. Valdantieji šių šalių politikai daug kartų žadėjo elektoratui, kad, pakeitus nacionalinę valiutą bendra europietiška, kainos nepakils.

Tikrovė. Įvedis eurą, maisto produktų ir kitų būtiniausių prekių kainos Latvijoje pakilo 20 proc. Pagal DNB „Latvijos barometras“ apklausą, 2014 metų gegužę 87 Latvijos gyventojų proc. patvirtino, kad įvedus eurą kainos pakilo. Lietuvoje įvedus eurą gyventojai pradėjo masiškai važinėti prekių į Lenkiją, kurioje maisto produktai ir kitos prekės kainuoja pusantro-dukart pigiau nei Lietuvoje. Šį mėnesį kainų Lietuvoje augimas iššaukė protesto akcijas — stambiausių prekybos centrų boikotas, ką gyventojai pavadino „kalafijorų revoliucija“.

SGD terminalo produkcija bus pigesnė už rusų dujas!

Sugalvojusi Klaipėdos SGD terminalo epopėją Lietuvos valdžia įtikinėjo gyventojus, kad norvegų SGD bus pigesnis nei „Gazpromo“ produkcija. Buvo skelbiamos kainos — 200-300 dolerių už kubinį dujų metrą, lietuviams buvo žadama, kad, įvedus rikiuotėn terminalą, jiems nereikės taip daug mokėti už apšildymą — komunalinių paslaugų tarifai Lietuvoje mažės.

Tikrovė. Įvedusi rikiuotėn SGD terminalą Lietuvos vyriausybė užslaptino galutinę tiekiamos produkcijos kainą. Pagal energijos ekspertų paskaičiavimus, susumuojant transportavimo, redujofikavimo ir plaukiojančio terminalo Independence nuomos išlaidas, galutinė suskystintų gamtinių dujų kaina siekia 560-570 dolerių už kubinį metrą, o tai pusantro karto brangiau už vamzdžiais tiekiamas rusų dujas. Kaimyninės šalys atsisakė pirkti iš Lietuvos „pigesnes“ nei „Gazpromo“ norvegų dujas, Lietuvos valdžia privertė stambias įmones pirkti dujas iš terminalo, o komunaliniai tarifai Lietuvoje ėmė kilti.

Sankcijos nepakenks mūsų ekonomikai!

Baltijos šalys buvo aktyviausios ekonominių sankcijų prieš Rusiją įvedimo šalininkės. Atsakydami į klausimus dėl Pabaltijo ekenomikų priklausomybės nuo Rusijos vietiniai politikai įtikinėjo, kad ta priklausomybė — prasimanymas ir „rusų propaganda“, sankcijos tikrai neįtakos Lietuvos, Latvijos ir Estijos ekonomikų, o jei Rusija įves atsakomąsias — Pabaltijo gamintojai visada galės perorientuoti savo eksporto srautus naujų rinkų kryptimi.

Tikrovė. Bloomberg agentūra pripažino Lietuvą labiausiai nukentėjusia nuo sankcijų karo ES šalimi. Pasak Lietuvos statistikos departamento, eksportas į Rusiją praeitais metais sumažėjo 38%, tame tarpe 76% sumažėjo antžeminių transporto priemonių, 82% — elektros mašinų, įrangos ir jų dalių, 94% — pieno ir pieno produktų eksportas ir visiškai nutrūko mėsos ir mėsos produktų eksportas. Lietuva 2015 metais tapo lydere tarp 28 ES šalių pagal eksporto kritimo tempą. Tuo metu banko Nordea ekonomistai rašo, kad Lietuvos eksportas į ES šalis liko tame pačiame lygyje — t.y. neįvyko jokio perorientavimo į naujas rinkas. Panašios problemos drebina Latviją su Estija: Pabaltijo pienininkystė priartėjo prie žūties ribos, Ventspilio, Talino ir Rygos uostų prekių apyvarta katastrofiškai mažėja, o po europietiško embargo Rusija atskirai uždarė prekybą latvių ir estų šprotais.

Įstojus į NATO ir ES santykiai su Rusija pagerės!

Baltijos šalių įstojimo į NATO ir ES išvakarėse tarptautinei bendruomenei buvo žadėta, kad integracija į euroatlantines struktūras pavers Lietuvą, Latviją ir Estiją labiau konstruktyviomis ir racionaliomis tarptautinių santykių dalyvėmis. Narystė NATO garantuoja Pabaltijui saugumą, narystė ES skatins jų lyderius būti atsakingesniais pasisakymų metu, ir visa tai gerins santykius su Rusija.

Tikrovė. ES institutus Baltijos šalys panaudojo Europos skaldymui, Pabaltijo politikai pavertė juos antirusiškų provokacijų instrumentais. „Rytų partnerystę“ su ES suartėjimo su buvusiomis tarybinėmis respublikomis programa jie pavertė geopolitine „sanitarinio kordono“ nuo Rusijos statyba; Lietuva, vienintelė ES šalis, vetavo derybas dėl bevizio Rusijos ir ES režimo, o vėliau, pusmetį pirmininkaudama ES, propagavo agresyviai antirusišką „geopolitinį žaidimą“. Narystę NATO Pabaltijis panaudojo reikalavimams didinti savo šalyse užsienio karinį kontingentą, išdėstyti karinę NATO infrastruktūrą prie Rusijos sienų ir dėl to atsisakyti bazinių Rusijos ir NATO susitarimų. Išvada: įstojimas į ES ir NATO pritvirtino Pabaltijui pastovios įtampos tarptautiniuose santykiuose šaltinio statusą.

Mūsų prioritetas — socialiniai klausimai ir rūpestis eiliniais žmonėmis!

Nuo rinkimų iki rinkimų Pabaltijo politikai žada skirti prioritetinį dėmesį socialiniams klausimams: didinti sveikatos apsaugos finansavimą, pensijas ir socialines išmokas.

Tikrovė. Nė vienoje Pabaltijo respublikoje socialinė politika netapo valstybės prioritetu. Lietuvoje vyriausybei vadovaujantys socialdemokratai, atėję valdžion su socialinių pažadų paketu, užmiršę pažadus, prisijungė prie prezidentės Grybauskaitės ir konservatorių ieškant tamsiame kambaryje juodą katę — „rusų grėsmę“. Latviją praeitais metais sukrėtė visiškai neeilinis įvykis: buvusi Seimo vadovė ir valdančiosios partijos „Vienybė“ lyderė Solvita Aboltinia nušvilpė pensijų pakėlimo reikalavusių pensininkų demonstraciją.

Visi emigrantai sugrįš!

Baltijos šalys pirmauja pasaulyje pagal gyventojų emigraciją. Iš Latvijos ir Lietuvos per ketvirtį amžiaus išbėgo šimtai tūkstančių žmonių. Londonas dabar — septintas pagal lietuvių skaičių miestas pasaulyje; kas trisdešimtas lietuvis ir latvis gyvena Didžiojoje Britanijoje. Bandydamos pateisinti gyventojų išsilakstymą, kuris visiškai prieštarauja pasakoms apie progresyvių jaunų demokratijų „sėkmės istoriją“ prie Baltijos jūros, Pabaltijo valdžios juokingai aiškina, kad žmonės niekur neemigruoja, jie tik keliauja po Europą, nes ES — vieninga erdvė, tad vidinė migracija neturi jokios reikšmės, ir (svarbiausia!) visi emigrantai būtinai sugrįš.

Tikrovė. Septyniems Latvijos gyventojams, atsižymėjusiems Airijos migracijos tarnyboje, tenka tik vienas, atsižymėjęs Latvijos migracijos tarnyboje po sugrįžimo iš Airijos. Pabaltijo juodadarbių apklausosDidžiojoje Britanijoje ir Airijoje rodo, kad 60-80 emigrantų proc. neketina grįžti į Lietuvą, Latviją ir Estiją. Emigrantai išsiveža vaikus ir net tėvus, naujoje tėvynėje užmiršta gimtąją kalbą, o Pabaltijį su ten likusiais meluojančiais politikais prisimena lyg baisiuose sapnuose.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 6 — id: `scraped:rubaltic_lt:931c61bf7d330d30`

**Title:** Lietuvos kariuomenė žudo savo karius

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos premjeras Algirdas Butkevičius pareiškė, kad Lietuva iš autsaiderių pereina į NATO lyderių dešimtuką. Tuo pat metu iš Lietuvos kariuomenės viena po kitos ateina žinios apie masiškus apsinuodijimus su mirties atvejais, erkių įkandžiotus kareivius ir netinkamą Lietuvoje dislokuotų amerikiečių sąjungininkų elgesį. Lietuvos politikų svajonės apie galingą ir sugebančią „sulaikyti“ Rusiją kariuomenę susiduria su tikrove, kuri neturi nieko bendro su savų šauktinių gyvenimu ir sveikata.

2017 metais Lietuva padidins savo karinį biudžetą 150 milijonais eurų ir jis sudarys 725 milijonus eurų arba 1,77 BVP proc. Tai jau ne pirmas išlaidų gynybai didinimas: karinis Lietuvos biudžetas nuosekliai auga nuo užpraeitų metų taip, kad 2018 metais pasiektų 2 BVP proc. — kaip numatyta pagal NATO standartus.

Iki užpraeitų metų savo agresyve užsienio politika pasižyminti Lietuva karinėms reikmėms eikvojo mažiau nei visos kitos NATO šalys — 0,8 BVP proc. Peržiūrėti savo požiūrį į karines pajėgas Lietuvos politikus privertė krizė Ukrainoje, kurioje jie įžvelgė „Maskvos imperiškų ambicijų atgijimą“. O rezultatas — visuotinio šaukimo į lietuvišką kariuomenę atgaivinimas, amerikiečiams ir kitiems NATO sąjungininkams adresuoti reikalavimai siųsti kaip galima daugiau karių ir karinės technikos Lietuvos gynybai ir spartus Lietuvos karinio biudžeto augimas. 2015 metais išlaidos gynybai, lyginant su praėjusiais metais, išaugo trečdaliu, 2016 metais — 35 proc., 2017 metais išaugs dar 26 proc.

Siekiant tenkinti kariuomenės reikmes, visais įvardintais metais buvo apkarpomi kiti šalies biudžeto straipsniai, pirmiausia — gyvybiškai svarbios lietuviams socialinės išlaidos. Lietuvos prezidentė Dalia Grybauskaitė 2014 metų priešrinkiminės kampanijos metu žadėjo tautai pakelti minimalias pensijas iki 650 litų ir grąžinti išmokas ligos atveju. Pirmuoju po perrinkimo sprendimu Grybauskaitė pervedė žadėtas lėšas karinėms reikmėms.

Lietuvos valdžia ir save lietuviškaisiais patriotais vadinantys jos padlaižiai tokius isteblišmento veiksmus pateisina garsia Napoleono fraze: „Nenorintis maitinti savosios kariuomenės maitins svetimą“.

Metų pradžioje Lietuvoje kilo skandalas dėl skirtumo aprūpinant maisto produktais amerikiečių ir lietuvių kariškius. Lietuvos kariuomenėje tarnaujantis savanoris parašė savo tinklalapyje, jog valgiaraščiai amerikiečiams ir lietuviams skirtingi; lietuvius valgykloje sodina priešingame NATO kariškiams kampe, valgyti greta amerikiečių jiems neleidžia, o eilinio JAV kario mitybai Lietuvos krašto apsaugos ministerija parai skiria lėšų trečdaliu daugiau, nei saviškiams.

Krašto apsaugos ministerija šios informacijos nepaneigė. „Reikėjo daug aštrių prieskonių, bulkučių, picų, konservuotų vaisių, sausų pusryčių (kukurūzų dribsnių) ir t.t.; atvykusiems į Lietuvą NATO kariškiams sudarėme ir patvirtinome valgiaraštį atsižvelgdami į kultūros ir virtuvės skirtumus“, — situaciją paaiškino karinės žinybos atstovė Asta Galdikaitė.

T.y. Lietuvos valstybė tiesiogine prasme nenori maitinti savosios kariuomenės, o maitina svetimą. Tačiau problema daug platesnė: savuosius Tėviškės gynėjus Lietuvos valstybė maitina taip, kad geriau visai nemaitintų. Todėl kad nuo to maisto Lietuvos kareiviai patenka į infekcines ligonines ir miršta nuo apsinuodijimo.

Pastarosiomis dienomis keli Lietuvos kariškiai buvo atgabenti į Kauno infekcinę ligoninę. Vienas iš jų, 21 metų šauktinis M.Jurkus, mirė. Velionio tarnybos draugai tvirtina, kad mažiausiai pas šešis kariškius aptikti tokie pat simptomai, jie skundžiasi, jog kareivinės aprūpinamos blogu vandeniu, ir atsisako maitintis vietinėje valgykloje. „Mane stebina žodžiai Krašto apsaugos ministerijos atstovų, kad viskas tvarkoj. Nesinori antros mirties. Kaip supratau, šauktiniai nesisako sergą, nes už tai baudžiami, todėl vaizduoja didvyrius“, — sako vieno iš atgabentų į Kauno infekcinę ligoninę giminaitė.

Masiško apsinuodijimo Rukloje skandalu istorija apie Lietuvos kariuomenės tarnybos sąlygas nesibaigia. Metų pradžioje mokymuose netoli Pabradės buvę naujokai pasiuntė žiniasklaidai laišką, kuriame prašė pagalbos. „Pas mus labai šalta, neveikia krosnis, pamėlynavusios kojos, niekas nesiruošia sutvarkyti apšildymo. Mums šalta, mes drebame ir nežinome, ką daryti. Viršininkai į mūsų prašymus nekreipia dėmesio. Gelbėkite, nes tik jūs galite mums padėti“, — guodėsi šauktiniai. Prie laiško buvo pridėta neveikiančios krosnies nuotrauka. „Tai mūsų krosnis, visą naktį ji nesikūreno, nes neveikia. Mes ne kartą bandėme ją užkurti, tačiau nieko neišėjo. Ką jau kalbėti apie tai, kaip atrodo palapinės! Naktį iš ketvirtadienio į penktadienį mums teko miegoti esant 20 laipsnių šalčiui“.

Po mėnesio tame pačiame poligone prie Pabradės 40 šauktinių pasiskundė aštriais skrandžių skausmais ir prasta savijauta. Infekcijos priežastimi, panašu, tapo nekokybiška mityba. Praeitą mėnesį Lietuvos šauktinius užpuolė erkės, nes mokymų metu jie miegojo palapinėse be dugnų. „Aš žinau tą žmogų. Jei tiksliau, jį įkando 201 erkė. Aš pats tai mačiau. Dvi medicinos seselės traukė jas 40 minučių“, — papasakojo apie erkių užpultą savo tarnybos draugą vienas iš šauktinių. Krašto apsaugos ministerijoje buvo patvirtinta, kad naktimis šauktiniai miega palapinėse be dugnų. O tuo metu norėjęs tęsti tarnybą Lietuvos kariuomenės karys medicininės komisijos metu dėl gydytojų neapdairumo vos neliko aklas.

Ar ne per daug mažoje, 2,9 milijoninėje Lietuvoje įvyko tokių atsitikimų pastaraisiais mėnesiais? Kyla vis tas pats klausimas: kur nueina pastoviai didėjantis Lietuvos kariuomenės finansavimas, jei ji negali garantuoti savo kareiviams gyvybės ir sveikatos?

Picoms ir bulkutėms amerikiečiams?

Patys amerikiečiai, beje, patvirtina šią išvadą: Lietuvoje elgiasi taip, kaip ir turi elgtis okupacinės kariuomenės kontingentas užkariautoje valstybėje. Praeitą mėnesį amerikiečių kareiviai išniekino Lietuvos vėliavą: nuplėšė ją Kaune nuo prokuratūros pastato ( apie tai parašiusi „Kauno diena“ gėdingai nutylėjo, kaip buvo vėliava išniekinta).

Tačiau Lietuvos valdžia nesiruošia pripažinti, kad šalis yra okupuota. Ir informaciją apie vėliavos išniekinimą amerikiečių rankomis ji bandė užslaptinti, ir apie atkurtos šauktinių kariuomenės reformavimą kalba tik mažoro tonu. Premjeras Algirdas Butkevičius neseniai pareiškė, kad kasmetinis karinio biudžeto didinimas 150 milijonų eurų pavers Lietuvą viena iš NATO šalių lyderių. Kaip šie 150 milijonų gerina Lietuvos kariškių mitybą, Butkevičius nepatikslino.

Taip ir gyvena Lietuva dviejuose matavimuose: Lietuvos politikų pareiškimuose ir tikrovėje. Pasak politikų, tai klestinti europietiška šalis su inovacijų ekonomia, lazeriais ir džiūgaujančiais gyventojais. O tikrovėje šimtai tūkstančių lietuvių bėga iš šio „rojaus“ į Angliją ir Airiją. Pasak Dalios Grybauskaitės ir jos daugelio antrintojų, „baisi ir kraujo trokštanti Rusija“ artimiausiu metu užpuls Lietuvą. Tikrovėje Lietuvos kariškiai rizikuoja numirti nuo savo kareivinių valgyklų maisto, o ne nuo rusiško agresoriaus kulkos. O tie, kurie išlaikys ir nenumirs, rizikuoja gyventi mokymų metu neapšildomose žiemą patalpose ir palapinėse be dugnų, kovodami ne su kruvina ir agresyve Rusija, o su erkėmis.

Ir todėl atsiradus realiam kariniam pavojui šaunioji Lietuvos kariuomenė ramia sąžine išsilakstys, nė karto neiššovusi. Kariauti, o tuo labiau mirti už tuos, kurie savo kariuomenę maitina atliekomis, o svetimą — bulkutėmis ir picomis, neis niekas ir niekada.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 7 — id: `scraped:rubaltic_lt:6c06bdd7cf306180`

**Title:** Ukraina ir Rusija nugalėjo politinėje „Eurovizijoje“

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Ukrainos dainininkė Džamala tapo estrados konkurso „Eurovizija-2016“ nugalėtoja. Jos daina „1944“ buvo skirta Krymo totorių deportacijai. Konkurso rezultatai atspindėjo ne muzikinius, o politinius vertinimus, šia prasme ir Rusija tapo „Eurovizijos“ nugalėtoja: milijonai žmonių tiesioginiame eteryje pamatė, kaip valstybinių kanalų — konkurso Europos šalims transliuotojų „profesionalūs žiuri“ dirbtinai menkino Rusijos rodiklius, o po to šių šalių gyventojai be jokios politikos atidavė savo balsus Rusijos atlikėjui.

„Eurovizijos“ taisyklės draudžia siųsti į konkursą politizuotas dainas, tačiau ‚Eurovizijos“ dalyviai reguliariai suranda būdus, kaip tas taisykles apeiti. Ta pati Ukraina 2005 metais pasiuntė į konkursą grupę „Gryndžoly“ su „oranžinės revoliucijos“ himnu — šukaliojimo dain „Mūsų iškart daug“. Tada jos atlikėjai pelnė tik 19-tą vietą.

Šiai metais Ukraina pasaldino muzikinį šou politiškai protingiau ir talentingiau. Krymo totorė Džamala pateikė europiečiams dramatišką baladę su rytietiškais motyvais, skirtą tragiškam savo tautos likimui. „Mano jaunystė nežydėjo ten, nes jūs pasiėmėte mano pasaulį“, — dainuoja Džamala apie stalines deportacijas, aistringai pabrėždama priedainyje angliškai ir Krymo totorių kalba: „Kur jūsų protas? Jūs manote esą dienai, tačiau visi miršta“.

Ukrainos konkursantės dainoje viskas tiko pergalei: ir žodžiai, ir vokalas, ir potekstė, ir kontekstas. Europietiška žiniasklaida ir prieš ir po konkurso ryžtingai rašė apie Džamalos dainos politinę potekstę ir politinį už Ukrainą balsavimo charakterį, viską vertindama iš esmės teigiamai.

Amerikiečių CNN pateikė medžiagą apie „Euroviziją“ pavadinimu „Nugalėjo antirusiška daina“, kurioje sulygino Džamalos pasirodymą su filmo „Šindlerio sąrašas“ garso taku. „32 metų džiazo dainininkė Džamala sako, kad jos daina „1944“ skirta ne tik Krymo tororių deportacijai Antrojo pasaulinio karo metu, bet ir pastarųjų dviejų metų įvykiams pusiasalyje“, — „Eurovizijos“ metu rašė britų Guardian straipsnyje „Tu klausai, Putinai?“. Guardian straipsnis tapo pranašišku: britų leidinys tiesiai pareiškė, kad „daugelis Centrinėje ir Rytų Europoje ketina balsuoti taktiškai, kad išvengtų rusų triumfo“ ir kad rusų favorito pergalę galima panaikinti politiniu balsavimu už „dainą, kuri dėl aneksijos rauda skausmo balsu“.

Taip ir atsitiko.

Pergalę Ukrainai tikrai atnešė politinis balsavimas: pagrindinį indėlį į šią pergalę įnešė balsai taip vadinamų „profesionalių žiuri“ — tiksliau, valstybinių televizijos kanalų — konkurso Europos šalių transliuotojų, dauguma kurių aukščiausius taškus skyrė Ukrainai ir nė vieno — Rusijai. Tai vis akivaizdžios antirusiškos užsienio politikos šalys: Lenkija, Lietuva, Estija, Švedija, Gruzija.

Pirma, rusų atstovui Sergejui Lazarevui pirmąją vietą skyrė balsavę žiūrovai. Eiliniai Europos televizijos žiūrovai balsavo už rusų atlikėją, kurio dainoje nebuvo jokios politikos.

Antra, milijonai žmonių turėjo galimybę pamatyti, kaip konkurso rezultatus iškraipo ir reikalinga linkme koreguoja idėjiškai pakaustyti valstybinių kanalų „profesionalūs žiuri“. Akivaizdu, jog besigiriantys skaidrumu ir demokratiškumu europietiški valdininkai realybėje prisilaiko blogiausių tarybinių partinių komitetų ir meno tarybų tradicijų. Tai buvo žinoma ir anksčiau, tačiau naujos rezultatų skelbimo taisyklės, pagal kurias žiuri ir žiūrovų balsavimo rezultatai buvo paviešinti atskirai, leido šį faktą įrodyti eksperimentaliai.

Keliant kai kuriose Europos šalyse „Rusijos stabdymo“ klausimą, negali būti vietos nei objektyvumui, nei demokratiškumui. Praeitais metais į  mini skandalą „Eurovizijoje“ įsivėlė Lietuva, kurios „profesionalus žiuri“ Rusijos dainininkei skyrė žemiausius įvertinimus — tokius, kad net atsižvelgiant į Lietuvos žiūrovų balsavimą Rusija gautų nulį taškų. Šiai metais lietuvių žiuri ne tik pakartojo šį išpuolį, bet ir pateikė visuomenei savo darbo technologiją: keturi iš penkių Lietuvos Respublikos nacionalinio žiuri narių patvirtino, kad skyrė Rusijos atstovui pačią paskutinę vietą.

Tačiau „Rusijos stabdytojus“ muzikiniame fronte, kaip ir prieš metus, pavedė eiliniai lietuviai. Nepaisydami jokios politikos, jie skyrė balsus ir Rusijai, ir Ukrainai, ir kitoms šalims, kurių atstovų dainos jiems patiko. Rezultatas: pagal Lietuvos žiūrovų balsų skaičių Sergej Lazarev pelnė trečiąją vietą.

Ši trečioji vieta — svarbiausias Rusijos politinės sėkmės „Eurovizijoje“ įrodymas.

Lietuva šiuo atveju — toli gražu ne pati ryškiausia iliustracija. Štai kokie matosi kontrastai „profesionalių žiuri“ ir eilinių atskirų Europos šalių žiūrovų balsavime (aukščiausias „Eurovizijos“ vertinimas — 12 taškų, antrasis — 10):

Vokietija: žiuri — 0 taškų, žiūrovai — 12.

Estija: žiuri — 0 taškų, žiūrovai — 12.

Vengrija: žiuri — 0 taškų, žiūrovai — 10.

Čekija: žiuri — 0 taškų, žiūrovai — 10.

Slovenija: žiuri — 0 taškų, žiūrovai — 10.

Serbija: žiuri — 1 taškas, žiūrovai — 12.

Ir tai po dvejų ryžtingo neapykantos eskalavimo metų: „Putino vatnikams“, „koloradams“, „rusų agresoriams“ ir „okupantams“. Ir kuo užsibaigė? Tuo, kad Ukrainos televizijos žiūrovai „Eurovizijoje“ skyrė Rusijai aukščiausią įvertinimą (beje, Rusijos žiūrovai skyrė Ukrainai antrąją vietą — 10 taškų). Ryškiausiai dvejų metų neapykantos propagandos ir dviejų tautų atitolinimo žlugimą pademonstravo Ukrainoje Gegužės 9-oji, kai dauguma ukrainiečių, nepaisydami oficialios propagandos, vis tiek šią šventę vadino Pergalės diena: žmonės stebėjo šventines televizijos programas ir dalyvavo miestuose „Nemirtingojo pulko“ eitynėse.

Tik kitais metais, kaip Ukrainai, jai nereikės mokėti už šią pergalę.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 8 — id: `scraped:rubaltic_lt:ac40f414d87ad6a3`

**Title:** Kaip Pabaltijis prarado rusų tranzitą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Pabaltijo respublikų tranzito sfera atsidūrė ant kolapso ribos. Mažėja krovinių pervežimai geležinkeliais, katastrofiškai krinta Pabaltijo uostų krovinių apyvarta. RuBaltic.ru nutarė priminti, kaip Lietuvos, Latvijos ir Estijos transporto logistinė sfera atsidūrė tokioje padėtyje — kaip ketvirtadalio amžiaus antirusiška politika pasitarnavo Pabaltijui prarandant rusų tranzitą .

Kaip kūrėsi Pabaltijo tranzito šaka

Lietuvos, Latvijos ir Estijos šiuolaikiškos būklės sektorius buvo sukurtas tarybiniu laikotarpiu. Jis buvo kuriamas kaip dalis vieningo TSRS liaudies ūkio komplekso ir siejo Pabaltijo respublikas su visa Sąjunga. Pokario metais atkuriant Lietuvos, Latvijos ir Estijos infrastruktūrą bei ekonomiką buvo restauruoti geležinkelio danga bei automobilių kelių tinklas. Pabaltijo keliai buvo laikomi geriausiais TSRS — tai nenuostabu, prisimenant, kad Lietuvos, Latvijos ir Estijos TSR 1970–80 metais pirmavo tarp tarybinių respublikų pagal investicijų į infrastruktūrą apimtį vienam gyventojui.

Sprendžiant šį uždavinį buvo kompleksiškai modernizuoti Pabaltijo uostai. Naujasis Talino jūrų uostas — rekonstruotas ir išplėstas Talino miesto uostas — TSRS byrėjimo metu buvo laikomas brangiausiu pokario Europos infrastruktūros projektu. Vykdant naftotiekio „Družba“ — vieno stambiausių energetikos infrastruktūros srityje TSRS projektų — statybą, šio naftotiekio atšakose buvo pastatytas Butingės naftos perpylimo terminalas Klaipėdoje ir naftos perpylimo uostas Ventspilyje — pastarajame buvo įvestas rikiuotėn vienas stambiausių šalyje terminalų trąšų bei chemijos pramonės produkcijos transportavimui. Buvo visapusiškai modernizuoti Klaipėdos ir Rygos uostai, dėl ko juose atsirado galimybė vykdyti praktiškai visų egzistuojančių krovinių rūšių transportavimą.

Apart puikių jūrų uostų ir geriausių TSRS geležinkelių bei automobilių kelių, kiekviena Pabaltijo respublika tarybiniais metais turėjo nuosavą prekybos laivyną. Lietuvos TSR turėjo didžiausią Europoje žvejybos laivyną. Skelbdama nepriklausomybę, Lietuva turėjo apie 500 laivų. Latvijoje 1947 metais sukurtas Respublikos prekybos laivynas „dainuojančią revoliuciją“ pasitiko apginkluotas pasaulinės klasės laivais — tankeriais, konteinerių vežėjais, refrižeratoriais.

Visa Pabaltijos prekybos laivynų istorija po 1991 metų pasireiškė užsitęsusiu tarybinio palikimo pridavimu į metalo laužą.

90–ieji metai: Pabaltijis — rusų tranzito monopolininkas

„Antrosios nepriklausomybės“ laikotarpiu tranzito reikšmė Pabaltijo ekonomikoms ženkliai padidėjo. Tai šių šalių ekonomikos struktūrų pasikeitimo rezultatas. 90–aisiais Latvija ir Estija (mažiau Lietuva, kurioje tada valdžioje buvo Algirdas Brazauskas) paskelbė šventąjį karą tarybiniams fabrikams ir gamykloms. Pastoviai uždarant, bankrutuojant ir priduodant į metalo laužą „okupacijos palikimą“, Pabaltijo ekonomikos gamybos dalis per keletą metų sumažėjo nuo 60 iki 20–25 proc. 1990-ųjų pradžioje kolapsą patyrė Pabaltijo žemės ūkis.

Staigus ekonomikos struktūros transformavimas iki 60–65 proc. padidino paslaugų apimtis, prie kurių ekonomikos mokslas priskiria ir tranzitą. Tačiau tranzitas potarybiniu laikotarpiu vaidino Pabaltijui nepalyginamą su bankų sfera arba turizmu vaidmenį.

Pavyzdžiui, rusų kroviniai ir vežami į Rusiją kroviniai įvairiais metais sudarė 75–90 proc. Latvijos geležinkelio krovinių pervežimo apimties.

Lyginant su stambia tarybine pramone, logistikos sfera 90-aisiai metais nekėlė Pabaltijo nacionalistams sąmoningo noro ją sunaikinti (nors naikinti prekybos laivyną puolė jau tada). Tranzito šakai leido egzistuoti, nors infrastruktūros palaikymui ir vystymuisi nevo skirta nė cento, — pakanka priminti, jog per 22 „antrosios nepriklausomybės“ metus Latvijoje buvo pastatytas tik vienas geležinkelio tiltas (o pastatytas dėka ES finansavimo).

Uostū monopolija leido šioms šalims be baimės eskaluoti maksimaliai priešišką Rusijos ir rusų atžvilgiu politiką: dalinti savo gyventojus į piliečius ir nepiliečius, remti čėčėnų kovotojus, reikalauti „kompensacijos už okupaciją“, reikšti teritorines pretenzijas. Taline, Rygoje ir Vilniuje suprato, kad Maskvai vis tiek nėra kur dingti: Pabaltijo tranzitas Rusijos Šiaurės Vakarams neturėjo alternatyvos, tad su Pabaltijo šalimis ji vis tiek turėjo tęsti bendradarbiavimą.

Esant tokiai Pabaltijo valdžių pozicijai, statyba Baltijoje Rusijos uostų tapo neišvengiamu ir vieninteliu tinkamu sprendimu.

2000-ieji metai: infrastruktūros atsiribojimas

Siūlymai kurti Šiaurės Vakaruose savą logistikos infrastruktūrą ir ja pakeisti pabaltijiškąją Rusijoje skambėjo visais 90-aisiais metais — jie vis labiau populiarėjo. Beje, 1997 metais būsimasis Rusijos prezidentas Vladimiras Putinas savo disertacijoje rašė apie prekybos uostų statybos tikslingumą Leningrado srityje.

Šis tikslingumas buvo ir ekonominis, ir politinis: baigiantis 90-iesiems, Rusijos ir Pabaltijo santykiai degradavo iki sankcijų taikymo. Latvija tapo pirmąja pasaulyje šalimi, prieš kurią Rusija įvedė ekonomines sankcijas: po to, kai 1998 metais Rygoje policija sumušė rusų pensininkų demonstraciją, Maskva nutraukė naftos tranzitą per Ventspilį ir uždraudė latviškų produktų importą. Tuo pat metu stambus rusų biznis savo iniciatyva paskelbė prieš Lietuvą neoficialias sankcijas: po to, kai valdantieji „landsbergininkai“ atsisakė parduoti „Lukoilui“ Mažeikių NPG, pasirinkdami korupcija dvokiantį sandorį su amerikiečiais, stambiausios Rusijos kompanijos nutraukė naftos į „Mažeikių naftą“ bei Butingės terminalą tiekimą.

Taip susiklosčius santykiams, priklausomybė nuo tranzitinių šalių Maskvoje buvo suvokta kaip grėsmė nacionaliniam saugumui.

Dujotiekį „Šiaurės srautas“, naftotiekių sistemą BVS-2 (Baltijos vamzdynų sistema) ir rusų prekybos uostus Leningrado srityje (Ust-Luga, Vyborgas, Primorskas) buvo pradėta statyti pagal šį kursą.

Rusijos alternatyvos Pabaltijo tranzitui atsiradimas iškart negatyviai įtakojo trijų šalių krovinių apyvartos sumažėjimą uostuose ir geležinkeliuose. Po skandalingo „Bronzinio kareivio“ perkėlimo „Rusijos geležinkeliai“ nutraukė naftos tiekimą į Estiją, rusų eksporteriai, vietoj Talino, nukreipė savo krovinius į kitus uostus, o „Estijos geležinkeliai“ dėl rekordinio krovinių apyvartos kritimo buvo priversti atleisti 8,5 proc. personalo. „Bronzinė naktis“, kaip pareiškė buvęs Estijos premjeras Tijt Viachi, šaliai kainavo 8 milijardus eurų, Estijos ekonomikos augimas sumažėjo dukart, o buvusio tranzito lygis pagal rodiklius krito negrįžtamai.

Mūsų laikai: tranzito šakos kolapsas

Savo laiške Federaliniam Susirinkimui 2015-ųjų metų pabaigoje Rusijos prezidentas paragino vystyti savuosius Baltijos uostus, patvirtinęs, jog Kremlius priėmė strateginį sprendimą atsisakyti Pabaltijo uostų ir galutinai užbaigti rusų tranzito perorientavimą į Rusijos Šiaurės Vakarų uostus.

Tais pačiais 2015-aisiais pilnu pajėgumu pradėjo dirbti nauji Leningrado srities uostai. To išdavoje rusų uostai praeitiasi metais užėmė lyderių pozicijas krovinių apyvartoje tarp rytinėje Baltijos jūros dalyje esančių uostų. Ust-Lugos uosto apyvarta praėjusiais metais ūgtelėjo 16 proc. ir 6 proc. š.m. pirmame ketvirtyje. Beje, šis spartus augimas vyko esant antirusiškoms sankcijos, rusų maisto produktų embargo ir rusų ekonomikos krizei.

Visų Pabaltijo uostų apyvarta praėjusiais metais sumažėjo 7 proc., o Talino uosto — 21. Pirmame 2016 metų ketvirtyje Talino uosto apyvarta krito 16 proc., Rygos — 14. Dar 2014 metų pabaigoje rusų „Transnafta“ pareiškė išeinanti iš Ventspilio ir nukreipianti savo naftos tranzitą link Primorsko ir Ust-Lugos. To išdavoje Ventspilio uosto apyvarta 2015 metais sumažėjo 14 proc., o š.m. pirmame ketvirtyje — 19.

Visose trijose Pabaltijo šalyse krinta pervežimai geležinkeliais. Praeitais metais Rusija nutraukė per Latviją anglies ir mineralinių trąšų tranzitą. Šiais metais „Estijos geležinkelių“ valdyba paskelbė esant katastrofai: traukinių iš Rusijos kiekis mažinamas perpus — nuo 12 iki 6 traukinių porų per dieną. Pasak Eesti Raudtee pirmininko, toks kritimas — ne riba: artimiausiais mėnesiais rusų krovinių tranzitas gali visai nutrūkti, ir geležinkelio laukia jei ne bankrotas, tai masiški atleidimai.

Tačiau situacijos tragiškumą matome dar aiškiau, prisiminę, jog 2006 metais Estijos geležinkeliais per dieną pravažiuodavo iš Rusijos 32 traukiniai. Nereikėjo niekinti kapų ir perkelti „Bronzinio kareivio“ — tuo atveju dalis šių traukinių dar būtų važiavę per Estiją. O esant dabartinei situacijai, Pabaltijo respublikos turi vieną išeitį: bėgius ir uostų kranus priduoti į tą patį metalo laužą, į kurį jie pridavė savo prekybos laivyną.

Tokia esmė minėtų strateginių sprendimų: jie realizuojami ilgai ir nepastebimai, tačiau, juos įgyvendinus, posūkis atgal praktiškai neįmanomas.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 9 — id: `scraped:rubaltic_lt:53a3deca83d6fbeb`

**Title:** „Kontaktus su Rusija reikia vystyti, o ne gąsdinti jais jais tautą“

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Neseniai Lietuvos Švietimo ir mokslo ministerija išleido knygą apie pastarųjų penkiolikos metų valstybinės premijos „Metų mokytojas“ laureatus. Tarp knygoje aprašytų pedagogų — ir vienas Klaipėdos rusų mokyklos mokytojas ekspertas Andrej Fomin, pelnęs šią premiją 2001 metais.

Mažai kas iš prisilietusių prie Lietuvos ir Pabaltijo Rusų pasaulio nėra girdėjęs apie Andrejų Fominą. Vieni prisimins jį kaip savo mylimą istorijos mokytoją, kitiems jis įsiminė kaip Lietuvos rusų tėvynainių koordinavimo tarybos pirmininkas ir kaip žmogus su aktyvia visuomenine pozicija, kai kam jis — knygų ir žurnalų straipsnių apie rusų istoriją autorius, o dar kai kas susipažins su juo pagal šį interviu, kuriame buvo aptartos ne tik Lietuvai, bet ir visoms Baltijos šalims aktualios aštrios problemos.

Susitikome su Andrejum Vadimovičium betarpiškai prie „staklių“ — mokykloje. Jis sėdėjo prie vadovėliais ir sąsiuviniais užversto stalo. Iš vienos krūvelės ištraukė Lietuvos švietimo ir mokslo ministerijos išleistą albumą, kurį aš iš anksto paprašiau atnešti. Puslapiuose mirgėjo pedagogų veidai, ir štai — pamačiau du Fominus. Vieną — prie darbo stalo, kitą — albume.

— Andrejau Vadimovičiau, o Jūs albume vienintelis mokytojas rusas iš rusų mokyklos?

— Atrodo, taip, tačiau norisi tikėti, kad jų bus daugiau. Džiaugiuos, kad ši premija paskatino valdžią atkreipti dėmesį ir į rusų mokyklas. O šioje knygoje aš stengiausi akcentuoti tą didžiulį darbą, kurį atlieka rusų mokyklos. Pati knyga glaustai pristato „Metų mokytojus“ ir jų patirtį. Knygos pristatymo metu švietimo ir mokslo ministrė teisingai pasakė — mes privalome tausoti ir propaguoti sukauptą pedagoginę patirtį. Čia ir pasakojama apie žmones, kurie mokyklose pasiekia svarių rezultatų. Juos būtina žinoti ir perimti vertingą patirtį. Daugelį jų žinau. Tai — rimti žmonės, tai darbštuoliai, kurie visada noriai dalinasi savo meistriškumu ir patirtimi.

— Konkursas vyksta 15 metų, o tarp laureatų Jūs vienintelis rusų mokyklos mokytojas. Ar jaučiate šališkumą?

— Manau, jog ryškaus šališkumo nėra, tačiau įžvelgiu aiškaus įvertinimo ir, gali būti, dėmesingumo rusų ir tautinių mažumų patirčiai stoką. Egzistuoja ir kitas aspektas. Mokytoją pastebi, kai jis pats ryškiai išsiskiria, kūribingai sukuria kažkokių idėjų, savitus metodus. Todėl, iš vienos pusės, Ministerija ir konkurso komisija galėtų atidžiau analizuoti Lietuvos rusų mokyklų darbo patirtį, iš kitos — ir mūsų mokytojai neturėtų bijoti rodyti savo patirties, savo švietėjiškos veiklos sistemos. Aš ir kolegoms visada sakau: nereikia slėptis, būtina aktyviai rodyti savo darbo pasiekimus. Juk mes turime puikių mokytojų, kieno patirtis vertinga ir įdomi.

— O gal tai ir yra bijojimas viešai parodyti save ir savo patirtį?

— Žinoma, jaučiasi baimė parodyti save gyvenant bei dirbant kitokių kultūros ir kalbos ir administracinių reikalavimų apsuptyje. Bet gi Lietuvos rusų mokykla visada garsėjo aukštu savo auklėtinių paruošimo lygiu. Ji turi savo tradicijas, savo piukius pedagogus. Todėl nėra ko kompleksuoti! Tačiau ir valstybė privalo deramai įvertinti rusų mokyklų darbą. Ir kuo dažniau būtų vertinami rusų mokyklų pedagogai, tuo geriau visuomenė suprastų, kad tautinių mažumų mokyklos nėra kažkokios antraeilės įstaigos — priešingai, tai sėkmingai ir efektyviai šalies labui dirbanti švietimo sistema.

Jaučiamas dar vienas svarbus momentas: politika pas mus pastaraisiais metais pakeičia švietėjiškos vaiklos metodiką. O tai nenormalu.

— O kokį įspūdį Jums padarė Valstybės saugumo departamento ataskaita, kurioje būtent taip vertinamos tautinių mažumų mokyklos?

— Gana keistas įspūdis. Lyg ataskaitą būtų parašę dvejetukininkai. Jokios gilios analizės, vien tik prielaidos ir propagandiniai štampai. Daugiapuslapiniame pranešime neskirta rimto dėmesio tikrosioms grėsmėms, tokioms, kaip terorizmas, Europą užtvindę abejotino charakterio migrantų srautai ir katastrofiškas Lietuvos gyventojų emigravimas... Užtat pastoviai eskaluojama prasimanyta Rusijos ir Baltarusijos grėsmė. Lyg nebūtų kitų problemų ir grėsmių. Visa tai liguisto mąstymo rezultatas. Nėra jokių faktų, vien tik dirbtinos prielaidos. Net tai, kad iš Kijevo į Lietuvą buvo atvežti pravoslavų pasišventėlių Šventieji palaikai įvertinta kaip Pravoslavų cerkvės grėsmė.

O svarbiausia — tokių ataskaitų ir pranešimų autoriai tarp išgalvotų problemų nemato tikrų grėsmių nacionaliniam saugumui. Pagrindinė grėsmė — vidinė: masiškas Lietuvos gyventojų emigravimas.

— Ar skiriasi valstybės požiūris į mokyklas su dėstymu valstybine kalba nuo tautinių mažumų mokyklų?

— Nustebinsiu jus: tautinių mažumų mokyklos finansuojamos geriau, nei lietuviškos. Ir tai todėl, jog daugiau lėšų skiriama sustiprintam valstybinės — lietuvių kalbos dėstymui. Tačiau, jei kalbėti atvirai, pastaruoju metu visuomenėje samoningai formuojamas negatyvus požiūris į visa, kas rusiška, tame tarpe į rusų mokyklas, rusų mokytojus, visuomenines organizacijas, dirbtinai eskaluojama įtampa, dažnai — išgalvotai argumentuojant. Vidutinis miesčionis, deja, tai priima kaip neginčijamą tiesą, pradeda kreivai žiūrėti į mųsš reikalavimus išsaugoti mokymą gimtąja kalba, į mūsų mokyklų pedagogines tradicijas. Ir, žinoma, atsidūrę tokioje situacijoje pedagogai jaučiasi nejaukiai. Tačiau aš, pats daugelį metų dirbantis švietimo sistemoje ir rusų mokykloje, užsiimdamas sąžininga pedagogine veikla, privalau pareikšti, kad visa tai — išgalvota nesamonė! Nekelia grėsmės nei mūsų mokiniai, nei mokytojai, nei mūsų tradicijos bei mentalitetas, nei kultūriniai kontaktai, kuriuos mes vystome su Rusija ir jos regionais. Ir tuos kultūrinius kontaktus reikia skatinti bei vystyti, o ne gąsdinti jais tautą.

— Tai gal mokytojų baimė pasireikšti, pastangos „nepastebimai gyventi“ — būtent ir yra tos dirbtinos atmosferos šalyje pasekmė?

— Neabejoju, tokia atmosfera įtakoja nuotaikas. Nemalonu gyventi, kai į tave žiūrima įtartinai. Tačiau norisi tikėti, kad ši reakcija į dabartinę politinę konjunktūrą laikui bėgant ištirps, ir viskas sugrįš į normalias vėžes. Tik va kada?

— Ir kada tai gali įvykti?

— O čia jau klausimas ir Lietuvos politikams, ir lietuvių tautai. Aš bendrauju su daugeliu lietuvių — išsilavinusiais ir kultūringais žmonėmis, kurie blaiviai vertina tai, kas vyksta, gailėsi dėl visuomenei peršamos isterijos. Juk ne iškart atsirado šiandieninis antirusiškas posūkis, kuris būdingas Pabaltijo bei Europos Sąjungos ir NATO šalims narėms. Dar prieš keletą metų tarp Rusijos ir Lietuvos egzistavo visiškai normalūs santykiai.

Beje, net kai kurie Lietuvos ir kitų šalių politikai jau atvirai apie tai kalba. Tačiau jaučiasi inercija — prieš keletą metų suveikė postūmis — ir kol kas valdžios dreifuoja primestu kursu. Žinoma, nemaža tų, kuriems naudinga išsaugoti aukštos isterijos gaidą. Ir tai — pagrindinė dabartinio kurso priežastis.

— Ar galima teigti, kad antirusiškas postūmis Lietuvoje labiau jaučiamas, nei kitose Pabaltijo šalyse?

— Abejoju. Aš stebiu įvykius Latvijoje ir Estijoje, ten taip pat būna savų pakilimų ir kritimų, šių procesų aktyvėjimo ir aprimimų, tačiau manau, jog kursas maždaug vienodas. Toną savo  tautinių mažumų, visų pirma rusų, atžvilgiu kartais užduoda Lietuva, Latvija arba Estija. Susidaro įspūdis, kad šių šalių valdžios išbando įvairias tautinių mažumų „integravimo“ metodikas. Čia nesimato konkretaus nuoseklumo. Pavyzdžiui, kurį laiką egzistavo Tautinių mažumų prie Lietuvos Respublikos Vyriausybės departamentas, tačiau vėliau, esą dėl ekonominės krizės ir lėšų taupymo, jis buvo likviduotas. Šiuo metu panašus departamentas vėl atkurtas. Kur logika? Juk viskas paprasčiau: jeigu tautinės mažumos demokratinėje visuomenėje turi lygias su dauguma teises, tai būtina jas gerbti ir jų prisilaikyti, veikiant pagal „Tautinių mažumų teisių rėminę konvenciją“, numatančią plačias galimybes naudotis gimtąja kalba, mokymo gimtąja kalba sistemos sukūrimą, vardų ir pavardžių gimtąja kalba rašymą pagal šios kalbos normas ir tradicijas. Ir taip toliau.

Tai yra: tik reikia prisilaikyti ratifikuotų tarptautinių sutarčių, o ne kurti naujų struktūrų, neišgalvoti dirbtinų piliečių lojalumo kėlimo būdų, negąsdinti jų išgalvotomis grėsmėmis. Ir tada įsivyraus savitarpio supratimas ir visuomeninė santarvė.

— Kokie Rusų pasaulio išsaugojimo Lietuvoje keliai?

— Pirma, mokymo gimtąja kalba ir mūsų tautinių auklėjimo tradicijų išsaugojimas, nes rusų mokykla — vienintelis masiškas ir veiklus rusų bendruomenės Lietuvoje tęstinumo šaltinis. Antra, mūsų istorinės atminties išsaugojimas. Trečia, palankių sąlygų rusų kultūros vystymuisi išsaugojimas. Ketvirta, kontaktų su mūsų istorine tėvyne išsaugojimas. Ne apribojimas ir siaurinimas jų, o priešingai — pilnaverčio kultūrinio bendradarbiavimo sukūrimas. Ir tik tada Rusų pasaulis sugebės išlikti. Tačiau svarbu suvokti: ar nori šalies valdžia, kad jis išliktų? Ar tai atitinka jos interesus ir tikslus? Juk dabar, beje, pačią Rusų pasaulio sąvoką kai kurie politikai naudoja gąsdinimo tikslais.

— Mūsų su Jumis praeitame interviu Jūs sakėte, kad vidutinis rusų mokyklų mokytojų amžius — apie ir virš 50 metų. Laikas eina, amžius didėja. Kas ateityje dirbs rusų mokyklose?

— Žinoma, didelių ir džiugių perspektyvų šiuo atveju nesimato. Viena aštriausių, pagrindinių problemų —pedagoginių kadrų stoka. Padėtis tokia, kad vidutinis rusų mokyklų mokytojų amžius artėja prie pensijinio. Tačiau pedagogai tautinių mažumų mokykloms Lietuvoje neruošiami. Tad situacija dramatinė, netrukus galinti tapti tragiška. Praeis nedaug laiko, ir rusų pedagogų kadrų neliks. Kas tada bus? Juos pakeis mokytojai lietuviai? Arba, kas daug realiau, neliks rusų mokyklų, jos taps lietuviškomis?

Štai apie tai ir reikia galvoti. Čia kaip tik slypi rimta grėsmė nacionaliniam saugumui. Tačiau valdžia jos nemato arba nenori matyti.

— Kaip žinia, jaunimas veržiasi ten, kur uždirbs dešimteriopai daugiau, negu tėvynėje. Ar yra ryšys tarp emigracijos ir rusų mokyklų nykimo?

— Iš Lietuvos išvyksta daug jaunų žmonių, dėl to trečdaliu sumažėjo gyventojų skaičius. Emigracija įtakoja bendrą mokinių mokyklose skaičių. Tačiau tiesioginio ryšio tarp jaunimo iš Lietuvos emigravimo ir rusų mokyklų uždarymo nematau. Čia pagrindinį vaidmenį atlieka politika mokymo ir švietimo srityje ir visuomenėje sukurtas psichologinis klimatas. Mokinių rusų mokyklose skaičius mažėja ne tiek dėl emigravimo, kiek dėl bendrų psichologinių nuostatų.

Kai kurių mokinių tėvai galvoja: kadangi rusų kalba Lietuvos valstybėje neatlieka jokio vaidmens, o priešingai, gerbūvis ateityje priklauso nuo lietuvių kalbos žinojimo, lai geriau jie mokysis lietuvių mokykloje. Ir nemažą dalį mokinių kontingento lietuvių mokyklose sudaro išeiviai iš rusų šeimų. Suveikia miesčioniškasis požiūris. Ir aš, žinoma, išreikščiau priekaištą tokiems tėvams, galvojantiems kad jiems rūpi vaiko gerbūvis. Iš tiesų jie atima iš vaiko ryšį su šaknimis, su turtinga rusų kultūra, siaurina turiningą vidinę kultūrinę asmens būklę. Tačiau žvelgiant iš miesčionio varpinės — nėra ko skaityti Dostojevskį, svarbiausia, kad ant stalo būtų šaltiena, o piniginėje — banko kortelė su neliesa sąskaita.

— Praeitais metais buvo užbaigta struktūrinė mokyklų reforma. Ką Jūs galite pasakyti apie jos rezultatus?

— Struktūrinė mokyklų pertvarka, prieš kurią mes pradėjome pasisakyti dar prieš 10 metų, buvo pavadinta labai skambiai — „Švietimo įstaigų tinklo optimizavimas“. Beje, valdžia optimizavo ne tik švietimo sistemą, bet visą Lietuvą, taip optimizavo, kad šalis prarado vos ne milijoną su ja atsisveikinusių piliečių. Dėl ko vykdomas šis optimizavimas? Suprasčiau, jei būtų ženkliai ūgtelėjęs gyventojų pragyvenimo lygis, jų socialinis saugumas ir aprūpinimas... Tačiau realybėje to nėra. Tada vardan ko? Taigi rusų mokyklų optimizavimas iš pat pradžių pakvipo naikinimu. Mes iškart sakėme, kad tai struktūrinė lietuvių mokyklų pertvarka: vidurinės mokyklos teisėtai tampa gimnazijomis ir progimnazijomis, ir tai nepavojinga, nes jų daug. Tačiau rusų mokykloms, kurių ne tiek daug, pakvipo nykimo drama. Išsaugoti pilnavertį 12-metį išsilavinimą suteikiančią vidurinę mokyklą — optimali tautinių mažumų mokyklų išeitis. Bet mes nebuvome išgirsti.

Reformos smagratis malė mokyklas. Dėl šio optimizavimo buvo prarasta nemažai mokyklų. Pirmiausia — Klaipėdoje, vėliau — Vilniuje. Blogiausia, kad optimizavimui buvo sukurta gražbylavimo ir neįgyvendinamų pažadų priedanga. Kur išsilaisvinusios lėšos? Kur gerėjanti švietimo aplinka? Nauja technika? Šiuolaikiškos mokymo priemonės? Kodėl Lietuvoje streikuoja mokytojai, streikuoja, pabrėžiu, ne tik dėl sugrąžinimo krizės metu apkarpytų atlyginimų, bet svarbiausia — dėl savo auklėtinių mokymo aplinkos pagerinimo? Tad dėl ko vykdoma ši reforma? Sutaupyti pingų, kurie vėliau bus panaudoti visai kitais tikslais?

— Ar Jus tenkina minėto mokytojų streiko rezultatai?

— Aš negaliu pasakyti, kad tenkina, netenkina ir kitų mokytojų. Tačiau pedagogai vis dėlto sugebėjo parodyti vyriausybei, kad būtina spręsti mokyklų problemas, įsiklausyti į mokytojų nuomones. Tame ir glūdi moralinė šio streiko esmė. Vyriausybė vis dėlto pamatė, kad kažką reikia daryti: ne žodžiais, o praktiškai.

Beje, ir streiko metu išlindo „asilo ausys“: savuosius pedagogus, kurie, nesulaukę valdžios pažadų vykdymo, buvo priversti streikuoti, premjeras gėdino, kad jie veikia pagal Maskvos nurodymus. Tai dar kartą patvirtino, kad valdžia nesugeba spręsti savo liaudies problemų, o, dumdama akis, ieško išorinio priešo.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 10 — id: `scraped:rubaltic_lt:8b77fa6bcf55a3af`

**Title:** Pabaltijis praranda rusų tranzitą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Po Latvijos Estija pripažino savo logistinės srities krizę, atsiradusią praradus rusų tranzitą. Estijos atstovai baiminasi, kad tranzito rodikliai gali kristi iki nulio, o susiklosčiusią situaciją aiškina naftos kainų mažėjimu ir rusų ekonomikos krize. Tačiau rimčiau įsigilinus į Pabaltijo tranzito problemas, matosi, jog jas neįtakojo nei ekonomika, nei antirusiškos sankcijos, nei Rusijos politika jo respublikų atžvilgiu. Tranzito problemos neišvengiamai atsirado dėl Lietuvos, Latvijos ir Estijos antirusiškos politikos: pati Istorija įvedė sankcijas prieš Pabaltijį, kurio šalys pasirinko sau geopolitines „Rusijos stabdymo“ funkcijas.

Estijos geležinkelių valdybos pirmininkas Suleva Loo apgailestavo, jog kritiškai sumažėjo Rusijos tranzitas geležinkeliais. Rusija pareiškė norą sumažinti krovinių geležinkeliu pervežimą Estijos kryptimi du kartus — nuo 12 iki 6 traukinių porų per dieną. „Traukinių porų skaičius sumažintas perpus. Priežastys ekonominės: atpigo nafta. Rusija mažiau gamina mazuto, ir jo realizavimui rado geresnes galimybes savo uostuose. Štai taip viskas paprasta“, — situaciją komentuoja Suleva Loo, pareiškęs, kad jei krizinė situacija nebus sureguliuota, teks atleisti iš darbo dalį krovinių pervežėjų.

„Mes tęsiame su Rusija dialogą, nes norime suvokti, ko galime sulaukti. Griūti viskas gali iki nulio, nors visiškai blogai nebus, nes trąšų pervežime konkurentų nedaug“, — mano Suleva Loo. Norėdama nuo galutinės katastrofos išgelbėti savo tranzito darbuotojus, estų delegacija artimiausiu metu išskrenda derybų į Maskvą.

Deja, tai daroma vėluojant dešimtmečiu. Skristi derybų reikėjo praėjusį dešimtmetį, o 2015–2016 metais Estija ir kitos Pabaltijos šalys sulaukė ilgalaikio ir išsamaus atsako į savo dar prieš ketvirtį amžiaus pasirinktos ir nekintančios tarptautinėje arenoje politikos.

Eesti Raudtee valdybos direktorius ženkliai sumenkina situaciją, teigdamas, kad tranzito problemos slypi naftos kainų mažėjime. Ne mažutė esmė. Rusijos tranzitas estų geležinkeliais mažėja mažiausiai 10 pastarųjų metų. Tas mažėjimas matėsi kai naftos barelio kaina siekė 140 dolerių, iki visokių sankcijų ir net iki 2008 metų krizės. 2006 metais iš Rusijos estų geležinkeliais pravažiuodavo per parą 32 traukiniai. Jei 2015 metais krovinių srautas sumažėjo iki 12 traukinių porų, vadinasi, krizė prasidėjo ne pirmaisiais 2016 metų mėnesiais. Akivaizdu, jog iki 2016 metų reiškėsi vangi chroniška krizė, o Rusijos krovinių Estijos keliais pervežimams kritus nuo 12 iki 6 traukinių per dieną prasidėjo griūtis.

Ir tuo metu Rusijos jūrų uostų, pastatytų kaip alternatyva pabaltijiečiams, apkrovimas visus šiuos metus augo nepaisant jokių krizių. Ust-Lugos uosto krovinių apyvarta 2015 metais išaugo 16 proc. Pirmaisiais 2016 metų mėnesiais — 6 proc. Palyginimui, Talino uosto payvarta 2015 metais krito 21, o pirmame 2016 metų ketvirtyje — 16 proc. Rygos uosto krovinių apyvarta pirmaisiais 2016 metų mėnesiais sumažėjo 14 proc. Visų kartu Pabaltijo jūros uostų apyvarta praėjusiais metais krito 7 proc. Beveik visi šie kroviniai vežami į arba iš Eurazijos ekonominės sąjungos teritorijos. O vien tik Ust-Lugoje, pasikartosime, krovinių apyvarta praėjusiais metais ūgtelėjo 16 proc. Tai, sakote, Rusijoje krizė?

Tai, kas vyksta, ne krizė, o, priešingai, rutiniškas, dėsningas reiškinys.

Šias pasekmes visu rimtumu pajuto latvių ir estų tranzitas, o taip pat visų trijų Pabaltijo šalių maisto produktų sektorius. Labiausiai nuo Rusijos kontrsankcijų tarp ES šalių nukentėjo Lietuva: jos Statistikos departamento duomenimis, lietuviškasis eksportas į Rusiją 2015 metais sumažėjo 38 proc. Baltarusijos dėka Lietuvos tranzitas iki šiol dar nepatyrė tokių pasekmių prarandant ryšius su Rytais, kaip Latvijos ir Estijos. Tačiau Lietuvos valdžia stengiasi, kad patirtų. Krizė Rusijoje reiškia krizę Baltarusijoje, o krizė Baltarusijoje reiškia smūgį Lietuvos tranzitui. Oficialus Vilnius nuosekliai siekia, kad Europos parlamentas pratęstų sankcijas prieš Rusiją, bet ir siekia blokuoti Ostroveco AE statybą.

Tokia kenkėjiška savo kaimyno ir svarbaus ekonominio partnerio ekonomikos atžvilgiu politika po kelerių metų neišvengiamai duos rezultatą: Klaipėdos uostas ir Lietuvos geležinkeliai atsidurs tokioje pat padėtyje kaip Talino uostas ir Eesti Raudtee.

Tranzito ir kitų su Rusija susietų Pabaltijo ekonomikų krizė — objektyvus reiškinys, atsiradęs dėl antirusiškos Lietuvos, Latvijos ir Estijos politikos.

O kokio kitokio rezultato galėjo sulaukti Rusijos-Pabaltijo santykiai, jei po 1991 metų šios šalys norėjo kontaktuoti su Rusija tik reikalaudamos 750-834 milijardų dolerių už „sovietinę okupaciją“, sugalvojo nepiliečių institutą, ėmėsi persekioti rusų kalbą, remti čečėnų kovotojus. Tik laiko, egzistuojant tokiai politikai, reikalavo strateginis Rusijos sprendimas atsisakyti Pabaltijo uostų ir geležinkelių tranzito paslaugų ir statyti prie jūros savą logistinį sektorių.

Jei Rusija Pabaltijyje turėtų sąjungininkes arba bent neutralias šalis, alternatyva būtų. O jei šiame regione atvirai reiškiasi nesimaskuojantys priešai, tai ir pasirinkimo nėra, ir prarasti nėra ko.

Ar verta dabar Estijos valdžiai stebėtis, kad Rusijos krovinių srautas per dešimt metų sumažėjo nuo 32 traukinių iki 6 ir gali pasiekti nulį? Pakanka prisiminti tai, kas vyko nuo 2006 iki 2016 metų, ir bus aiškus šios dinamikos dėsningumas. Vandalizmo aktas perkeliant „Bronzinį karį“, bandymas kišti pagalius į „Šiaurės srauto“ Baltijos jūroje statybos ratus, rusų ir Rusijos visokiais būdais demonizavimas — nuo prezidento Ilveso kalbų iki kapo (nacių stovyklų prižiūrėtojų) metraščių. Ir po to jie tvirtins, jog Talino uosto ir Estijos geležinkelių krizė atsirado dėl to, kad Rusija ėmė mažiau pardavinėti mazuto?!

Ar verta Lietuvos valdžiai piktintis, kai jai sakoma, kad lietuviškieji mėsos ir pieno produktai daugiau niekada nepateks į Rusijos rinką? Pakanka prisiminti, kad Lietuva vienintelė iš 28 ES šalių vetavo derybas dėl bevizio režimo tarp Rusijos ir Europos Sąjungos šalių; kad Lietuvos prezidentė Dalia Grybauskaitė siūlė sukviesti NATO Tarybą ir apsvarstyti klausimą dėl Įstatų 5 straipsnio taikymo — siekiant bendromis jėgomis sustabdyti „Rusijos agresiją“. Pakanka prisiminti Lietuvos prezidentės išgalvotą „teroristinę valstybę“ ir tada taps aiškios su Rusija susietų Lietuvos ekonomikos sričių krizės priežastys.

Daugelis Pabaltijo verslininkų ir valdininkų ne vienerius metus tikėjo, kad politika — sau, o jų, kaip partnerių, ryšiai su Rusija — sau. Kad Pabaltijo politikų retorika — „baltasis triukšmavimas“, kuris nieko neįtakoja: kol Briuselio ir Vašingtono politikai kalba apie „atgimstančią kruviną Rusijos imperiją“, mes visada sugebėsime Maskvoje susitarti su reikalingais žmonėmis ir, kaip anksčiau, vešime savo geležinkeliais ir perkrausime uostuose rusų naftą, anglis ir skaldą.

Šie žmonės nepajėgė ar nenorėjo suprasti net to, kad politikų retorika — toli gražu ne „baltasis triukšmavimas“, o tai, kad Pabaltijo sostinių antirusiška politika neapsiribojo vien tik retorika.

Šie veiksmai — ne retorika ir ne „baltasis triukšmavimas“. Tai ne žodžiai, o būtent veiksmai. Reali, praktinė politika, kurios pagrindas — kraštutinis priešiškumo Rusijai lygis. Todėl neturi stebinti adekvatus atsakas.

Rusai lėtai kinko, bet greitai važiuoja. Visais 90-aisiais Rusijos Federacija lūkuriavo: negi Lietuva, Latvija ir Estija nepersirgs antirusiškos isterijos liga? Užaugs, nustos kvailioti. Vėliau, 2000-aisiais, buvo nutarta statyti prie Baltijos savo uostus ir į juos nukreipti tranzitą. Statybos užtruko daugiau nei 10 metų. Tačiau dabar procesas taip įsibėgėjo, kad jau neįmanoma sustabdyti. Krizė, sankcijos ir naftos kainos niekuo dėti — Rusija daugiau nenori turėti jokių reikalų su Pabaltiju, juolab, ji dabar nėra priklausoma nei nuo Pabaltijo tranzito, nei nuo žemės ūkio produktų importo.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 11 — id: `scraped:rubaltic_lt:f3bb9bbf1c9cd9aa`

**Title:** Lietuvos valdžia pripažino, jog visuomenė atsidūrė pastovaus streso būsenoje

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos premjeras Algirdas Butkevičius pareiškė, kad šalyje įsivyravo nesveikas psichologinis klimatas ir žmonės pastoviai jaučia baimę. Butkevičiaus manymu, baimės atmosferą sukūrė opozicijoje esantys konservatoriai, „pamiršdamas“ paminėti prezidentės Dalios Grybauskaitės ir savosios vyriausybės vaidmenį paverčiant Lietuvos Respubliką „palata Nr. 6“.

Praeitą savaitę Lietuvos politikai ne pirmą kartą varinėjo „žalius žmogeliukus“.Seimo Nacionalinio saugumo ir gynybos komiteto vadovas Artūras Paulauskas pareiškė, kad Lietuvoje mokymų metu galėjo nusileisti rusų desantininkai. Remdamasis neseniai paskelbta Valstybės saugumo departamento kasmetine ataskaita, kurioje buvo tvirtinama, kad „jaučiama, jog Rusijos specialiosios paskirties kariniai daliniai taikos metu prasisverbia į užsienio valstybes“, Paulauskas išsakė prielaidą, kad „žalieji žmogeliukai“ galėjo nusileisti Juodkrantėje: „Turbūt vyko kažkokie mokymai, ir jie nusileido“.

Paistalai apie Pabaltijo politikų matytus rusų desantus, tankus ir povandeninius laivus tampa šio regiono gyvenimo norma. Neseniai Lietuvos kaimynė Latvija „matė“ prie savo krantų rusų povandeninį laivą. 2014 metų rudenį visi profesionalūs Pabaltijo rusofobai draugiškai patikėjo, jog Švedijos teritoriniuose vandenyse nuskendo rusų povandeninis atominis laivas ir laukė Baltijos jūroje dar vieno Černobylio. Ir ar galima pamiršti benefisą buvusio Lietuvos kriminalinės policijos vadovo Algirdo Matonio, kuris automobilio vairavimą, turėdamas kraujyje 1,71 promilės, aiškino tuo, jog gėrė miške su agentu naminį vyną ir pastarasis pranešė jam apie artimiausią vidurnaktį ruošiamą „žalių žmogeliukų“ įsiveržimą į Lietuvą!

Ir todėl Paulausko samprotavimuose apie, gali būti, rusų desanto nusileidimus Juodkrantėje nesimato nieko nuostabaus. Stebina tik pasakoriaus partiškumas — juk Artūras Paulauskas Seime atstovauja Darbo partijai. Paranoja ir sekimo manija tarp Lietuvos elito per dvejus su puse metų taip išsišakojo, kad šiais kolektyviniais nukrypimais užsikrėtė ir tradiciškai prorusiškos politinės jėgos.

„Lietuvoje įsivyravo nesveikas psichologinis klimatas, žmonės gyvena baimės būsenoje, — mano Lietuvos Respublikos premjeras, socialdemokratų lyderis Algirdas Butkevičius. — Šis Lietuvos susiformavęs politinis psichologinis klimatas ir toliau formuojamas baimės pagrindu, jį būtina sustabdyti, su tuo reikia kovoti, daugiausia instrumentų tam turi politikai, parlamentinę kontrolę vykdantys deputatai“.

Lietuvos premjero filipika buvo adresuota Parlamento opozicijai, pirmiausia — konservatorių partijai, „Tėvynės Sąjungai – Lietuvos krikščionims demokratams“. Be to, „landsbergininkams“ nuo Butkevičiaus kliuvo ne už visuomenės gąsdinimą „neišvengiama rusų agresija“, o už korupcijos skandalų Lietuvos vyriausybėje eskalavimą pastaraisiais mėnesiais.

Tačiau vargu ar pavyks ką nors įtikinti, kad visuotinos baimės ir panikos atmosfera atsirado visuomenėje dėl smulkaus žulikavimo Žemės ūkio ir Aplinkos ministerijose. Tai įvyko šalies prezidentės pareiškimų, kad Rusija Lietuvą jau užpuolė ir karas vyksta, visuotinės karo prievolės atnaujinimo, brošiūrų apie partizaninio karo metodus Rusijos agresijos atveju išsiuntinėjimo ir karinių kontingentų į Lietuvą atkaklių kvietimų fone!

O pirmiausia, kaip žinia, — šalies vadovė Dalia Grybauskaitė, pasižymėjusi pastaraisiais metais lygindama Putiną su Hitleriu, sankcionavusi Lietuvoje prorusiškosios penktosios kolonos paiešką ir bandžiusi inicijuoti 5-ojo NATO Įstatų straipsnio Rusijai dėl kolektyvinio atkirčio agresoriui taikymą. Kai tavo šalies prezidentas de-fakto dėl konflikto Ukrainoje siūlo pradėti Trečiąjį pasaulinį karą, nenoromis tapsi isteriku.

Tačiau ištikimais Grybauskaitės pasisakymų antrininkais apie „teroristinę valstybę“ ir „hibridinį karą“ prieš Lietuvą, kuris „jau vyksta“, buvo ne tik ponios prezidentės veiklą kontroliuojantys konservatoriai, bet ir anksčiau įvardinti jų politiniai antagonistai socialdemokratai. Ko vertas vien tik Lietuvos užsienio reikalų ministras Linas Linkevičius, už nuoseklų prezidentės užsienio politikos linijos palaikymą pelnęs „imperatorės pažo“ pravardę.

Pagaliau, ir socialdemokratų lyderis, Lietuvos premjeras Algirdas Butkevičius, šiuo metu pradėjęs kalbėti apie nesveiką šalies visuomenėje psichologinį klimatą, atrodo, apsinuodijo šiuo klimantu. Vasario mėnesį jis teigė, kad neterminuotas Lietuvos mokytojų streikas — Rusijos specialiųjų tarnybų išmislas. Būtent taip jis ir pasakė: „Streikuojantiems diriguoja suinteresuotos destabilizuoti Lietuvos situaciją rankos iš Rusijos“.

Po vedančiųjų socialdemokratų ir „darbiečių“ — Lietuvos politinių jėgų, tradiciškai priešinusių „landsbergininkų“ paranojiškai ir šizofreniškai rusofobijai, pareiškimų apie „Maskvos ranką“ Lietuvos mokytojų gretose ir apie „žalius žmogeliukus“ šalies pajūryje tenka pripažinti, kad liguista psichologinė atmosfera Lietuvos Respublikoje įsivyravo ilgam. Jei ne visiems laikams.

Lietuvos politikai prieš rinkimus gali pripažinti tokios atmosferos egzistavimą ir kalbėti apie kovos su ją būtinybę, tačiau patys jie seniai pažeisti šios ligos metastazėmis. Atrodo, jie jau nesugeba patys išsigydyti ir Lietuvos išgydyti.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 12 — id: `scraped:rubaltic_lt:b149a3a794e6b4e3`

**Title:** Vakarai pripažino Lietuvos ekonominius praradimus

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuva tarp ES šalių labiausiai nukentėjo nuo Rusijos kontrsankcijų — rašo viena stambiausių pasaulyje informacinių agentūrų Bloomberg. Bloomberg pabrėžia situacijos paradoksalumą: labiausiai nuo sankcijų karo nukentėjo šalis, aktyviausiaitarp ES šalių reikalavusi sankcijų prieš Rusiją, — ir prieina išvados, kad kelio lietuviškoms prekėms į Rusijos rinką daugiau nebus. Lietuvos užsienio politika tapo vidinės katastrofos priežastimi: radikalus Lietuvos valdžios antirusiškas kursas užsibaigė nacionalinių gamintojų bankrotu.

„Per 17 mėnesių sankcijų ir metus recesijos Rusija prarado pagrindinės lietuviškojo eksporto šalies statusą. Šį mėnesį paviešinti duomenys teigia, kad Rusijos draudimas importuoti iš ES maisto produktus ir jos ekonominis nuosmukis pagaliau pribaigė dviejų šalių prekybinius santykius, — taip apie Lietuvos-Rusijos santykius rašo informacinė agentūra Bloomberg. — Ši vienintelė tarp 28 ES narių Pabaltijo šalis, labai priklausiusi nuo Rusijos, nepaisant šaltų politinių santykių, dabar ieško rinkos kitoje vietoje“.

Pasak Lietuvos Statistikos departamento, kurio duomenimis remiasi Bloomberg, Lietuvos eksportas į Rusiją 2015 metais sumažėjo 38 proc. Maisto ir žemės ūkio lietuviškos kilmės produktų eksportas — 54,5 proc. Praktiškai nutrūko lietuviškų pieno produktų eksportas į Rusiją — jis sumažėjo Lietuvos žemdirbiams katastrofišku procentu — 94. Lietuviškos kilmės mėsa ir mėsos produktai į Rusiją visiškai neekspotuojami.

Be to, ženkliai sumažėjo eksportas į Rusiją ir tų lietuviškų prekių, kurioms nebuvo taikytos kontrsankcijos. 82 proc. sumažėjo eksportas elektrinių mašinų, įrenginių ir jų dalių, 76 % — antžeminių transporto priemonių.

Ir tuo metu nepavyko įgyti žadėtų naujų rinkų: pagal bendrojo eksporto sumažėjimo tempus Lietuva tarp 28 ES šalių pirmauja.

„Tuo metu, kai kaimyninės Lenkija ir Latvija užsiėmė skylių užkamšymu, o prezidentė Dalia Grybauskaitė lieka nuosekliausia ES sankcijų šalininke (tai privertė Rusiją įvesti maisto produktų embargą), Lietuvos įmonės bus psiruošusios atkurti savo ryšius su Rytais, kai nuslūgs įtampa ir pagerės ekonominės sąlygos“, — samprotauja Bloomberg, kurio analitikai daro išvadą, kad silpnam lietuviškam eksportui Rusija pagal daugelio prekių pozicijas lieka alternatyvos neturinčia realizavimo rinka: tik Rytuose galima prekiauti vietiniais brendais, žinomais ten nuo tarybinių laikų ir nežinomais Vakaruose.

Tuo metu tarptautinė informacinė agentūra abejoja, ar po to, kai bus panaikintos sankcijos ir kontrsankcijos, galės sugrįžti į Rusijos rinką lietuviška produkcija. „Gruzija, 2008 metais pralaimėjusi penkių dienų karą prieš Rusiją, diversifikavo savo užsienio prekybą, tačiau politinių santykių atšilimas negrąžino Rusijos dominavimą importuojant gruzinų vyną ir mineralinį vandenį, — rašo Bloomberg ir daro išvadą: — Lietuvos eksporteriai akylai stebės, kaip Rusija stengiasi įveikti recesiją, o ES peržiūri sankcijas, įvestas ryšium su įvykiais Ukrainoje“.

Tokiu būdu Lietuvos užsienio politika ir šalies eksporterių–mokesčių mokėtojų interesai siejasi atvirkščiai proporcingai. Visos jų viltys — kad ES panaikintų sankcijas prieš Rusiją, o ši — prieš ES šalis. Visos jų viltys — kad žlugtų užsienio politika prezidentės Dalios Grybauskaitės ir URM vadovo Lino Linkevičiaus, kurie siekia, kad Briuselis pratęstų sankcijas iki begalybės. O jeigu Lietuvos politinę vadovybę lydės sėkmė ir sankcijų karas bus pratęstas, žlugs visos lietuviškų prekių gamintojų viltys.

O dar Bloomberg nutyli, kad be Rusijos dialogo su ES dar egzistuojajos santykiai su atskiromis ES šalimis, kurios pastaraisiais krizės metais skyrėsi didžiuliais kontrastais. Pirmiausia — sankcijų klausimu.

Nė viena ES šalis nesiekė sankcijų prieš Rusiją taip aktyviai, kaip Lietuva, nė viena Europos Sąjungos šalis per dvejus pastaruosius metus nepateikė tiek antirusiškų iniciatyvų ir nė vienos šalies politinė vadovybė nesimėtė Rusijos atžvilgiu tokia įžūlia retorika, kaip Lietuvos prezidentė ir URM vadovas.

Apolitinius lietuviškų sūrių ir varškės gamintojus galima pasigailėti, tačiau to neleidžia padaryti vienas atšakus faktas: būtent Lietuvos pienininkystė iki pastarųjų metų atkakliai rėmė aršiausius Europoje rusofobus — „Tėvynės Sąjunga — Lietuvos krikščionis demokratus“. Eiliniai rusų vartotojai, pirkę parduotuvėse varškės sūrelius iš Rokiškio ir sūrį „Svaja“, rėmė veiklą juos nekenčiančių žmonių, įvairiais metais raginusių izoliuoti Rusiją, neišduoti rusams Šengeno vizų, blokuoti Kaliningrado sritį, Briuselyje ir strasbūre priimti čečėnų kovotojus.

Jei Lietuva užsienio politikai paaukojo savo ekonomiką, tai Rusija gali sėkmingai suderinti užsienio politikos kursą su ekonominiu vystymusi remdama savo gamintoją (o ateityje ir palankiausius Maskvai ES šalių gamintojus) ir nefinansuodama Lietuvos konservatorių. Palikti be rusiškų pinigų ponus Landsbergį, Ažubalį, Kubilių, Juknevičienę, o taip pat tyliai landsbergininkų kuruojamą Grybauskaitę — ar tai neatitinka Rusijos nacionalinius interesus?

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 13 — id: `scraped:rubaltic_lt:80e059b7542bc34c`

**Title:** Rusija atsakys į NATO karinių pajėgų Pabaltijyje didinimą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
RF gynybos ministras Sergejus Šoigu pareiškė, kad Rusija priversta reaguoti į NATO karinių pajėgų prie savo sienų didinimą. Rusijos šiaurės vakarų militarizavimas — simetrinis atsakas į Lietuvos, Latvijos ir Estijos NATO militarizavimą: reaguojant į NATO karinės technikos didinimą, į regioną įvežama Rusijos karinė technika, o atsakant į planus išdėstyti Pabaltijyje septynias NATO brigadas, prie vakarų sienos formuojamos naujos Rusijos divizijos. Pats Baltijos regionas ir jo gyventojai tampa ginklavimosi lenktyniavimo įkaitais: abipusis militarizavimas neleidžia Pabaltijui vystytis, o bet kokia provokacija arba karinė klaida gali tapti jo nušlovimo nuo žemės paviršiaus priežastimi.

„NATO ir toliau didina savo potencialą Europoje, tame tarpe prie pat Rusijos sienų. Be abejonės, tokia situacija negali nekelti mums nerimo. Mes priversti į tai reaguoti“, — pareiškė Rusijos gynybos ministras Šoigu.

Reakcijos į NATO karinės infrastruktūros priartėjimą prie Rusijos sienų rezultatu Šoigu pavadino permetimą į Vakarų karinę apygardą virš 1100 vienetų naujos ir modernizuotos karinės technikos, tame tarpe lėktuvų, sraigtasparnių, tankų, šarvuotų transporterių, ryšių ir valdymo priemonių.

Tai ne pirmas šiais metais viešas pareiškimas apie papildomą Rusijos šiaurės vakarų sienos stiprinimą. Sausio mėn. RF gynybos ministerijos vadovas pareiškė, kad 2016 m. prie Rusijos vakarų sienos bus suformuotos trys naujos divizijos. Dvi iš jų — prie Baltijos jūros krantų. Taip pat Gynybos ministerija planuoja 2016 metais sutvarkyti jų pastovaus dislokavimo vietas — užbaigti statybą poligonų ir ginkluotės bei šaudmenų sandėliavimo arsenalų. Anksčiau Kaliningrado srityje buvo išdėstyta priešlėktuvinės gynybos sistema , nutarta į Rusijos anklavą permesti raketų kompleksus „Iskander“, galinčius naikinti taikinius 280–500 kilometrų atstumu.

Į Pabaltijį per pastaruosius dvejus metus buvo permesta 150 tankų „Abrams“, 16 raketų naikintuvų ir karinis specialiosios paskirties amerikiečių dalinys. Dar didesni NATO generolų planai 2016 metams. Vasario NATO Tarybos posėdyje buvo nutarta kokybiškai sustiprinti NATO rytų flangą Lenkijoje ir Pabaltijy. Pagal naują planą į Rytų Europos šalis buvo nukreipti JAV, Didžiosios Britanijos ir Vokietijos kariškiai. Naujiems NATO daliniams planuojama perduoti raketas „žemė-oras“, smogiamuosius lėktuvus ir sraigtasparnius. Pačioms „naujosios Europos“ šalims ir to mažai: jos siekia išdėstymo pas save septynių NATO brigadų — ir ne rotacijos pagrindu, o pastoviai, dėl ko NATO sąjungininkai turėtų nutraukti su Rusija tarptautinius santykius.

Metų pradžioje Pentagonas pareiškė, jog amerikiečių pajėgų Europoje finansavimas bus padidintas keturis kartus. JAV karinės išlaidos „senajame pasaulyje“ sieks 3,4 milijardo dolerių — šių lėšų liūto dalis bus skirta Rytų Europos militarizavimui. 2015 m. pabaigoje JAV Europoje sausumos dalinių vyriausiasis vadas patvirtino įrengimą 2016 metais Pabaltijyje sunkiosios karinės technikos sandėlių. Didžioji Britanija pareiškė, kad nukreips į Baltijos jūrą penkis savo karinius laivus pagal karinio NATO dalyvavimo Rytų Europoje strategiją.

Tokiu būdu abi šalys viena su kita juridiškai sutvirtina tikėtino priešo statusą. Atnaujintoje JAV Karinėje strategijoje pagrindiniu amerikiečių karinių pajėgų Europos vadovybės uždaviniu įvardintas pasipriešinimas Rusijai. Naujoje Rusijos Nacionalinio saugumo strategijoje pagrindiniu potencialiu priešu įvardinamas NATO, o svarbiausia karine grėsme — NATO karinės infrastruktūros išdėstymas prie Rusijos sienų.

Be to, abi šalys įtaria, kad kita gali panaudoti branduolinį ginklą. Vyriausiasis EUCOM vadas Filipas Bridlavas svarstymo JAV Kongrese metu dalinosi įtarimais, kad kaliningradietiški „Iskanderai“ gali turėti branduolines galvutes. Tačiau ir NATO lėktuvai Šiauliuose gali būti panaudoti kaip amerikiečių taktinio branduolinio ginklo nešėjai.

Kol Pabaltijos šalys neklykė, reikalaudamos, kad NATO užtikrintų jų saugumą, Rusija į jas nekreipė dėmesio. Dabar gi, kai į jas permetami tankai su bombonešiais ir planuojama steigti NATO bazes, jos tampa Rusijos taikiniu. Karas su Vakarais prasidėtų šūviais į šį regioną, nes JAV sąjungininkai paverčia jį poligonu galimam Rusijos puolimui. Jeigu juos tikrai domintų tik Pabaltijo sąjungininkų saugumas, kaip bandoma įtikinti publiką, jie negabentų į Pabaltijį puolamąją ginkluotę. Tačiau jie gabena būtent puolamąją, o tai reiškia, kad Pabaltijo sąjungininkų saugumas juos mažiausiai domina.

Galimai nedaugelis Pabaltijo politikų, dar sugebančių mąstyti ne tik apie būsimą karjerą Briuselyje ir Vašingtone, bet ir savo šalių bei tautiečių likimą, mano, kad abipusis Rusijos ir NATO pristabdymas Lietuvai, Latvijai ir Estijai garantuoja saugumą geriau, nei perėjimas nuo ginklavimosi prie derybų tikslu abiem šalim demilitarizuotis. Esą kaina karinio susidūrimo su branduolinėmis galvutėmis Šiauliuose vienoje pusėje ir Kaliningrado branduolinėmis galvutėmis kitoje būtų tokia didelė, kad nė viena iš jų į tokį susidūrimą nesivels.

Toks situacijos matymas klaidingas. Pirma, jei susidūrimo neįvyks, militarizavimas Pabaltijos ateitį vis tiek galutinai palaidos. Kokios gali būti užsienio investicijos, infrastruktūrų projektai, pasienio ryšiai ir įprasti žmogiškieji kontaktai regione, kuriame gausu susidūrimui besiruošiančių armijų žvalgybininkų ir kontržvalgybininkų, ginkluotės sandėlių,o, gal būt, ir branduolinių ginklų? Tokiame regione galima tarnauti arba iš jo bėgti.

Antra, proporcingai karinio susidūrimo kainai išauga klaidos bei atsitiktinumo kaina ir, galų gale, provokacijos. Regionas paverčiamas parako statine. Mesi degtuką, ir ji sprogs. O kvailysčių arba provokacijų variantus galima be galo vardinti. NATO naikintuvai lydėjo Rusijos gynybos ministro Sergejaus Šoigu lėktuvą, skrendantį į Kaliningrado sritį — ar tai ne provokacija? Ir ar ne provokacija Bi-Bi-Si „dokumentinis“ filmas, kuriame Daugpilio rusai organizuoja maištą, dėl to Rusija įsiveržia į Latviją ir pradeda Trečią pasaulinį karą? O rusų atominis povandeninis laivas, kuris esą nuskendo prie Švedijos krantų ir kurį 2014 metų rudenį ieškojo visas Pabaltijo regionas, kol nepaaiškėjo, kad jokio povandeninio laivo nebuvo — tai, turbūt, vietinių rusofobų ir šizofrenikų haliucinacijos? O ką galima pasakyti apie buvusį Lietuvos kriminalinės policijos viršininką, kuris prieš dvejus metus nusigėrė iki žemės graibymo ir nulėkė pranešti viršininkams apie Rusijos į Lietuvą įsiveržimą artimiausią vidurnaktį?

Trečia, abiejų šalių karinio susidūrimo kaina nebus vienoda.

O kas pasakė Pabaltijo politikams, kad siekiantys savų interesų ir visiško šeimininkavimo Europoje amerikiečiai niekada neišprovokuos Rusijos ir NATO Pabaltijyje susidūrimo? Ponai Ilvesai, Rinkevičius, Grybauskaitė ir kiti išties nutarė, kad užjūrio šeimininkus tikrai domina jie patys ir jų saugumas?

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 14 — id: `scraped:rubaltic_lt:635178f32763f2d9`

**Title:** Europos Sąjunga aštriai kritikuoja Lietuvą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuva nedemonstruoja jokio progreso, lieka viena iš skurdžiausių ir socialiai nesėkmingų Europos sąjungos šalių, ir jai skubiai reikia reformų. Būtent apie tokį Europos komisijos požiūrį į savo šalį pareiškė prezidentė Dalia Grybauskaitė, dalyvaudama Europos sąjungos Tarybos posėdyje. Paviešindama tikrąjį Europos sąjungos požiūrį į Lietuvą, Grybauskaitė taikėsi į socialdemokratų vyriausybę, o pataikė į save ir į Lietuvą: ponia prezidentė asmeniškai pripažino, kad Briuselyje nėra jokių iliuzijų dėl Lietuvos „sėkmės istorijos“, o užsienio politikos ir kovos su „rusų grėsme“ prioritetas tapo valdžios spjūviu į eilinius lietuvius ir socialiniu ekonominiu šalies degradavimu.

Vasario pabaigoje Europos komisija paviešino Lietuvos ekonominių iššūkių analizę ir rekomendacijas jos valdžioms socialinėje ekonominėje srityje. Tokius analitinius dokumentus Europos sąjungos vykdomasis organas publikuoja kiekvienai iš 28 ES šalių kasmet.

Europos komisijos kritika Lietuvos atžvilgiu ir pasiūlymai daugelį metų nekinta. ES vadovybė kaltina Lietuvos valdžią tuo, kad šalis pagal europietiškus standartus vis dar lieka labai varginga, kad joje aukštas nedarbo lygis, o ši problema sprendžiama darbingų gyventojų sąskaita, o dar tuo, kad socialiai pažeidžiamos grupės (pensininkai, šeimos us vienu iš tėvų) nėra apsaugotos nuo materialinio susvetimėjimo grėsmės.

Kasmet reikalaujama, kad oficialusis Vilnius reorganizuotų darbo rinką, pensijų ir mokesčių sistemą. Priešingu atveju Lietuva niekada neištrūks iš uždaro „kylančių mokesčių, migracijos augimo ir atlyginimų stagnacijos“ rato.

Paskutiniame analitiniame Europos komisijos dokumente ekspertai įžvelgia augantį Briuselio funkcionierių susierzinimą, kad Lietuvoje ignoruojami visi jų nurodymai dėl žemo Europos sąjungos šaliai pragyvenimo lygio ir pasiūlymai dėl reformų socialinėje ekonominėje srityje. „Tai liudija, jog Lietuva nevykdo Europos komisijos rekomendacijų: darbo grupės pasiūlymai pasidengė stalčiuje dulkėmis, o priėmimas socialinio modelio, kuris numato pensijų, darbo rinkos ir valstybinių finansų reformą, stabdomas“, — taip dabartinės Briuselio vadovybės pasiūlymus Lietuvos vadovynei komentuoja banko Nordea Baltijos šalių tyrimo padalinio vadovas Žigimantas Mauricas.

Praeitą savaitę vyko Europos sąjungos Tarybos posėdis, skirtas šios sąjungos ekonominiam vystymuisi. Buvo aptarta, kaip kiekviena ES šalis vykdo Europos komisijos rekomendacijas ir ko pasiekė praėjusiais metais socialinėje ekonominėje srityje. Apibendrindama Europos Tarybos posėdžio rezultatus, valstybės vadovė pareiškė: Europos sąjungos vadovybė (Europos komisija, 28 šalių vadovai – ES Tarybos nariai) daug metų nepatenkinta Lietuva.

„Toks Komisijos vertinimas sako, jog Lietuva per praėjusius metus praktiškai nepasiekė jokio progreso. Pastabos dėl reformų neefektyvumo arba jų nevykdymo kartojasi kasmet. Tai labai aštrus raginimas pasitempti“, — teigia Dalia Grybauskaitė.

Paviešindama tikrąjį europiečių požiūrį į Lietuvą, Grybauskaitė, atrodo, galvojo, kad suduos smūgį tik socialdemokratų vyriausybei. Per septynerius savo prezidentavimo metus ji akivaizdžiai priprato prie pareigų pasiskirstymo: ji Lietuvoje atsakinga už teigiamus reiškinius, o vyriausybės — už neigiamus. Jeigu lietuvis prarado darbo vietą, badauja jo šeima, o visas pajamas suvalgo komunaliniai mokesčiai, vadinasi, ekonomika ir socialinė sritis nepriklauso ponios prezidentės kompetencijai: lai apskundžia vyriausybę, o ji pati niekuo dėta. Todėl pasakodama, kaip Briuselyje pykstama dėl Lietuvos socialinės ekonominės situacijos, Grybauskaitė jautėsi visiškai saugiai.

Veltui.

Vadovaujančiuose ir nukreipiančiuose užsienio centruose — Briuselyje ir Vašingtone — nematomi politiniai atspalviai ir pustoniai. Jiems egzistuoja Lietuva ir jos politinė klasė, kuri atsakinga už šiandieninę šalies padėtį.

Tame tarpe ir prezidentę Dalią Grybauskaitę, kuri, žinoma, visiškai atsakinga už eilinių lietuvių gyvenimą. Valstybės vadovė gali įtakoti vyriausybę ruošiant biudžeto projektą, ir parlamentą, priimant biudžetą. Ji gali išdėstyti prioritetus ir teikti visuomenei bei politikams vieną ir kitą Lietuvos vystymosi modelį.

Tuo Grybauskaitė pastaraisiais metais ir užsiiminėjo, bet ką ji teikė? Kokį vystymosi modelį siūlė Lietuvai? Nejaugi tai buvo socialinis modelis? Visiškai ne. Socialinio vystymosi modelio dabar iš Lietuvos vadovybės reikalauja Europos sąjunga, o Grybauskaitė pateikė šaliai egzistavimą apsuptoje tvirtovėje, atsiribojusioje nuo kaimynų apkasais ir gyvenančioje laukiant rusų agresijos.

Dalia Grybauskaitė siekė visuotinės karinės tarnybos sugrąžinimo ir specialiųjų tarnybų finansavimo didinimo. Siekė karinių išlaidų didinimo iki 2 proc. Lietuvos VBP. Tačiau ji niekada nesiekė mokesčių mažinimo, nesiūlė priemonių nacionalinio gamintojo palaikymui, nereikalavo, kad valstybė vykdytų savo socialinius įsipareigojimus, didintų socialines išmokas, keltų pragyvenimo lygį.

Ekonomika ir socialinė sfera pradėdavo dominti Lietuvos politikus prieš keletą mėnesių iki rinkimų ir užsibaigdavo po jų. Tas pastebėjimas liečia visas politinės klasės frakcijas, tame tarpe ir vyriausybę sudariusius kairiuosius. Eidami valdžion socialdemokratai 2012 metais žadėjo likviduoti potarybinėje erdvėje lietuviškąjį mesionizmą, o visus geopolitiniame donkichotiškame kelyje sutaupytus energiją, pinigus ir laiką eikvoti socialiai orientuotai politikai. Po rinkimų paaiškėjo, kad elektoratą apgavo: buvo suabejota, ar tikrai Lietuvos piliečius vargina socialinės problemos, nes politikus viliojo Vilniaus samitas, „Rytų partnerystė“, sankcijos, Ukraina.

Išdavystė rinkėjų atžvilgiu — dbūdingas Lietuvos politikams bruožas. Ne tik socialdemokratų — būtent visų. Dalia Grybauskaitė 2015 metų prezidento rinkimų metu žadėjo didinti minimalią pensiją iki 650 litų ir grąžinti išmokas ligos atveju. Po rinkimų prezidentė suskubo nukreipti žadėtas lėšas kariuomenės perginklavimui. Be jokios abejonės — „rusų grėsmė“ — dalykas šventas, bet kodėl reikėjo meluoti pensininkams?

Tą ideologiją, kurios pagrindu kūrėsi Europos sąjunga, galima apibūdinti dviem žodžiais: taika Europoje. Siekiant amžinos taikos kontinente, kurį sukrėtė du pasauliniai karai, buvo sukurti ES institutai tikslu užkirsti kelią konfliktams, bendromis jėgomis sureguliuoti ginčytinus klausimus. Lietuvos Respublika pasinaudojo europietiškais institutais, programomis ir mechanizmais (pirmininkavimas ES Taryboje, „Rytų partnerystės“ programa) siekdama priešingo — provokacijų, sukurstant ir gilinant Europoje konfliktus.

Šiuolaikiška ir paprasta europietiška idėja — kiekvieno europiečio gerbūvis ir gerovė. O apie Lietuvą Europos komisija ir ES šalių vadovai sako, kad jos vadovybei nusispjaut į mokesčius, pensijas, pragyvenimo lygį ir darbo vietas. Vietoj gerbūvio ir gerovės Lietuvos vadovybei rūpi kaip paremti Rusijos opoziciją, teikti ginklus Ukrainai, pratęsti sankcijas ir kurti Rytų Europoje NATO bazes.

Ar ne todėl lietuviškieji geopolitikos žaidėjai tarptautinėje plotmėje elgiasi priešingai nei karaliai Midasai: kai prie ko nors prisiliečia, visa tai paverčia ne auksu, o visai kita substancija. Lietuva aktyviausiai Europoje parėmė Gruziją, kai Saakašvilis pasodino kas dešimtą, o jo draugeliai šalyje išdarinėjo ką tik norėjo. Lietuva aktyviausiai pasaulyje remia Ukrainą, kurios vadovybę Europos sąjunga, kaip ir Lietuvos, kritikuoja už visuotinę korupciją, reformas svajonėse ir gyventojų skurdą.

Su kuo susidraugausi, to ir būsi pamokytas. Ar galima stebėtis, kad visų potarybinėje erdvėje susidėjusių su Lietuva svajonės apie europietišką egzistavimą žlugo kaip ir pačioje Lietuvoje? Tai pagal pasaulinius rekordus nykstanti šalis, iš kurios bėga šimtmečius gyvenusi tauta... Ko gali kitus išmokyti tokios šalies vadovybė? Tik to, kaip nevalia elgtis su savo tauta.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 15 — id: `scraped:rubaltic_lt:15b7a5fec34e5506`

**Title:** Lietuva vs. Astravo AES: baltarusių žvilgsnis

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Jau keletą mėnesių Lietuvoje nerimsta gana emocionalus Baltarusijos AES Astrave statybos aptarimas. Šių diskusijų paaštrėjimą galima paaiškinti priešrinkimine kova dėl rinkėjų simpatijų. Dalis Lietuvos elito stengiasi pasireikšti kaip tikri patriotai, ginantys energetinį ir ekologinį šalies saugumą.

Šią retoriką būtų galima vertinti būtent kaip dalį politinio susigrūmimo ir nesureikšminti ją, nes tarpvalstybiniuose baltarusių-lietuvių santykiuose dažniausiai jaučiamas nuosaikus ir pragmatinis požiūris. Bet ne šiuo atveju. Lietuva prezidentės Dalios Grybauskaitės lūpomis pagarsino savo pretenzijas statomos stoties saugumo klausimu ir reikalavimus siekiant užkirsti kelią baltarusių elektros energijos eksportui į Lietuvą ir per ją Europos lygyje.

Baltarusijos energetikos ministras Michailas Michadiukas savo interviu „Lietuvos rytui“ išsamiai atsakė į panašias pretenzijas. Jo atsakymuose aiškiai matosi šios pozicijos:

Lietuvos pretenzijos saugumo klausimu neturi rimto, dokumentais paremto pagrindo, o Baltarusija šį klausimą sprendžia ypač kruopščiai.

Astravo AES statoma visų pirma siekiant patenkinti savus Baltarusijos poreikius taupant elektros energiją ir angliavandenilius, o eksportas nesvarstomas kaip jos statybos prioritetas.

Baltarusija vykdo visus savo įsipareigojimus Espo Konvencijos rėmuose, ir jos aiškinimai tenkina Konvencijos įgyvendinimo Komiteto vadovybę.

Tai reiškia, kad visi pagrindiniai klausimai, liečiantys Baltarusijos AES tarptautiniame kontekste, pagrindiniam tarptautiniam organui, kuris jais užsiiminėja, nekelia rimto nerimo.

Papildomai verta pasakyti apie elektros energijos eksporto problemą. Du statomi blokai tikrai tenkins vidinius Baltarusijos poreikius, ypač ryšium su Kinijos-Baltarusijos industrinio parko „Didysis akmuo“ statyba ir gamybinių pajėgumų įsisavinimu. Iki 2020 metų, kai turi būti įvestas rikiuotėn antrasis Astravo AES blokas, būtent šis parkas padidins kiekinius energijos vartojimo šalyje rodiklius. Ir tik trečiasis bei ketvirtasis blokai, kurių dar nėra net planuose, tarnaus eksportui.

Pirma, tai esminis tranzito ūgtelėjimas per Klaipėdos uostą: ten jau atėjo baltarusių ir kinų investoriai norėdami didinti tranzito, tame tarpe ir parko produkcijos, pajėgumus. Beje, Klaipėdos uosto ir jo galimybių plėtra pareikalaus papildomos energijos. Antra, ir parko statyba, ir jo gyventojų skaičiaus, o taip pat Minsko, padidėjimas neišvengiamai iškels klausimą dėl susisiekimo transportu per Lietuvą pagreitinimo ir intensyvinimo. Tai reiškia, kad papildomos energijos gali prireikti elektrifikuojant geležinkelio ruožą nuo Vilniaus iki Klaipėdos, o tai — kokybinis Lietuvos transporto infrastruktūros pagerėjimas ir nupiginimas.

Lietuviškieji kolegos tai tikriausiai supranta, tačiau turbūt tikisi, kad gaminti savą elektros energiją pavyks pagal Visagino AES projektą. Problema tame, kad šis projektas hipotetinis, nėra jo finansavimo, o jo gavimo galimybės labai miglotos. Na, o pirmąjį AES Astrave bloką planuojama įvesti rikiuotėn 2018 metais.

Tačiau kai kurie Lietuvos politikai pareiškia gana radikalias idėjas. Pavyzdžiui, Konservatorių partijos lyderis europarlamentaras Gabrielius Landsbergis pareiškė, kad „mes galime sustabdyti šio projekto finansavimą, ir aš manau, kad mes privalome sau kelti šį uždavinį“. Iš baltarusių pozicijų tai atrodo kaip noras įsikišti į kaimyninės šalies vidaus reikalus. Ir jei po šių pareiškimų seks konkretūs veiksmai, juos Baltarusijos vadovybė vienareikšmiškai vertins kaip nekaimyniškus ir nedraugiškus. Faktiškai, gali iškilti grėsmė visam praėjusiais metais pozityviai sustiprėjusiam Baltarusijos-Lietuvos santykių kontekstui.

Nesunku įsivaizduoti tokio lietuvių elgesio pasekmes.

Tikėtina, jog ir Kinija peržiūrės savo projektus su Klaipėdos uostu, nes kinams jis bus įdomus tik ryšium su „Didžiuoju akmeniu“. Juolab, Latvija jau pareiškė apie prisijungimo prie tranzitinio srauto, organizuoto aplink kinų-baltarusių parką, galimybes ir turi vilčių sulaukti kinų investicijų.

Galimi neapgalvoti Lietuvos veiksmai taip pat įtakos neišvengiamą Minsko ir Maskvos aktyvesnį bendradarbiavimą, tame tarpe ir karinėje-techninėje srityje. Baltarusija kol kas ne ypatingai reaguoja į Vilniaus mobilizacinį aktyvumą, nors įdėmiai stebi jį, tačiau veikia asimetriškai, nesiveldama į savo ginkluotės ir sąjungininkų kariuomenės didinimą. Tačiau situacija gali keistis, ir tada visai kitaip nuskambės klausimas apie rusų aviacijos bazę Baltarusijoje, tiekimą iš Rusijos kitos šiuolaikiškos ginkluotės. Ir neduok Dieve, kad vietoj taikaus atomo Baltarusijoje atsirastų atomas karinis.

Galimas Baltarusijos-Lietuvos smarkus santykių paaštrėjimas gali tapti draugiškų pasienio zonos ekonominių, humanitarinių, kultūrinių kontaktų praradimu ir „naujo šalto karo“ tarp mūsų šalių atsiradimu. Vargu ar tuo suinteresuota Lietuva, ypač jei tokia psichologinė įtampa paskatins aktyviausios gyventojų dalies emigraciją iš Lietuvos į ramesnes Vakarų Europos šalis.

Kai kurie Lietuvos politikai tai supranta. Socialdemokratas Gediminas Kirkilas mano, kad „mes tikrai tokiais žingsniais nesustabdysime šios elektrinės statybos... Egzistuoja ne tik Astravas, bet ir santykiai su Baltarusija, tranzitas per Lietuvą, Klaipėdos uostą“, o partijos „Tvarka ir teisingumas“ frakcijos vadovas Petras Gražulis teigia, kad grąsinimais Astravo elektrinės adresu Lietuva pavers Baltarusiją „savo prieše, o ne sąjungininke“, ir „tai atneš mūsų valstybei nuostolių“.

Šios nuomonės — proto balsas. Lietuvai Baltarusijos AES statyba ir įvedimas rikiuotėn gali duoti ne papildomų problemų, o pelno: pigią elektros energiją, tranzitinio krovinių srauto padidėjimą, transporto infrastruktūros modernizavimą, papildomą baltarusių turistų srautą. Baltarusija, atrodo, pasirengusi tam pritarti ir nežaisti santykių paaštrėjimu. Ir čia kaip niekada reikalingi supratingumas ir išmintingumas Lietuvos politikų, kurie supranta, kad geri santykiai tarp kaimynų, turinčių bendras istorines šaknis, gali būti sugriauti neapgalvotais, skubotais žodžiais ir veiksmais, kuriuos vėliau bus labai sunku atstatyti.

RuBaltic.Ru informacija :

Aleksej Dzermant — baltarusių politologas, filosofas, visuomeninio-politinio projekto „Citadelė“ (Baltarusijos Respublika) koordinatorius.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 16 — id: `scraped:rubaltic_lt:09dd7bcd8341d836`

**Title:** JAV generolas grąsina Rusijai karu Pabaltijyje

**Source:** rubaltic_lt (propaganda)

**Text:**

```
JAV karinių pajėgų Europoje vadas Filipas Bridlavas pareiškė, jog JAV pasirengusi kovoti ir nugalėti Rusiją Europoje. Kalbėdamas JAV Kongrese, Bridlavas atkreipė dėmesį į Rusijos Kaliningrado sritį — pirmojo NATO smūgio objektą kilus karui. Tkiu būdu, amerikiečių generolas patvirtino, kad hipotetinis NATO ir Rusijos karinis susidūrimas prasidės nuo Pabaltijo, ir jeigu pirmojo NATO karinio smūgio ibjektu taps Kaliningrado sritis, tai pirmojo Rusijos karinio smūgio objektu taps Lietuva, Latvija ir Estija.

„Rusija nutarė būti priešu ir tampa ilgalaike grėsme JAV ir jų sąjungininkų bei partnerių Europoje egzistavimui“, — pareiškė vyriausiasis EUCOM (karinių JAV pajėgų Europos kontingento) vadas Filipas Bridlanas, pasisakydamas vasario 26 d. JAV Atstovų palatos Karinių pajėgų komitete. „Rusija stengiasi plėsti besąlygišką įtaką kaimyninėms šalims, siekdama sukurti buferinę zoną, — pareiškė generolas. — Rusija plečia savo įtaką dar toliau, stengdamasi įsitvirtinti pasaulinėje arenoje lyderės vaidmenyje“.

Praktinį savo pasisakymo tikslą Bridlavas atskleidė kariškai tiesmukiškai: JAV karinių pajėgų Europoje vadovybė motyvuoja keturis kartus didinamą kitų metų savo biudžetą. EUCOM, siekdama užtikrinti Europos saugumą, numato didinti amerikiečių kontingento Europoje finansavimą nuo 718 milijonų iki 4,3 milijardo dolerių. Reikalaudamas šių lėšų, Bridlavas ne kartą nurodė savo pranešime, kad daugelio NATO šalių biudžetai „chroniškai nesulaukia tinkamo finansavimo“ ir „išgyvena deficitą“.

„Mūsų biudžetinė paraiška atspindi tvirtą solidarumą su mūsų sąjungininkų ir partnerių saugumo interesais ir mūsų pasirengimą ginti jų tėvynę“, — paaiškino Filipas Bridlavas savo žinybos finansinius apetitus, o po to perėjo prie konkrečių reikalų. „Rusija ir Asado režimas sąmoningai naudoja migraciją iš Sirijos kaip ginklą bandant įveikti europietiškas struktūras ir sulaužyti Europos ryžtą“, — teigia amerikiečių generolas, kurio manymu Rusija Sirijoje užsiiminėja tik Asado ir jo sąjungininkų palaikymu ir beveik nieko nedaro kovojant su IGILu (Rusijoje uždrausta teroristinė organizacija).

Tokie vyriausiojo EUCOM vado logikos faktai priešia priešiškos Europai Rusijos veiklos vaizdą. Rusija remia Asadą, Rusija savo tikslais naudoja didžiulį pabėgėlių srautą Europoje, o dar rusų povandeniniai laivai plaukioja, lėktuvai skraido ir pasieniečiai išilgai sienos vaikščioja, todėl „siekiant pasipriešinti Rusijai, europietiška vadovybė kartu su sąjungininkais ir partneriais organizuoja sulaikymo priemones ir ruošiasi, esant būtinybei, kovoti ir nugalėti“.

Amerikiečių generolo rytų europietiška retorika — apgavystė, kurios prireikė siekiant išreikalauti iš politikų naujų karinių išlaidų. JAV ne Pabaltijis, kuris drebina kinkas prieš Rusiją.

Pirma, JAV gali rintai, kaip stiprieji su stipriaisiais, tartis su Maskva, kaip parodė paliaubos Sirijoje.

Norėdami sukelti su Rusija karinę konfrontaciją, sąjungininkai turi sugebėti prasibrauti pro Kaliningradą, — sako Bridlavas. Kaliningrado sritis karinės konfrontacijos su Rusija atveju taps NATO pajėgoms pirmuoju tikslu todėl, kad ten sukoncentruota daugybė ginkluotės sistemų, galinčių iš sausumos, jūros ir oro dideliuose atstumuose naikinti taikinius.

Tarp Lenkijos ir Lietuvos esanti Rusijos sritis tapo „tvirtove“, pro kurią teks brautis Aljanso pajėgoms. „Mes turime būti įsitikinę, kad sugebėsime ją palaužti“, — pasakė generolas Bridlavas Atstovų palatai apie Kaliningradą, aiškindamas EUCOM planą stiprinti savo rytinį flangą, įkuriant Pabaltijo šalyse pastovias NATO bazes.

Jeigu Kaliningrado sritis įvardinama pirmojo smūgio objektu, akivaizdu, kad atsakomojo Rusijos smūgio objektu taps Lietuva, Latvija ir Estija. Pirmiausia, todėl, kad tik šios NATO šalys turi sieną su Rusiją, antra, todėl, kad jos priklauso tam pačiam regionui, kaip ir Kaliningradas, trečia, todėl, kad būtent Kaliningradu, „tvirtove, kurią būtina įveikti“, amerikiečių generolas aiškina būtinybę didinti NATO pajėgas Pabaltijo šalyse.

Jeigu kalbama apie pastovių NATO bazių išdėstymą Lietuvoje, Latvijoje ir Estijoje bei karinių pajėgų šiose šalyse didinimą ir tuoj pat pabrėžiama būtinybė pulti Kaliningradą, tai subliūška visa Pabaltijo mitologija apie militarizavimą siekiant „apsiginti nuo agresyvaus rytų kaimyno“. Pabaltijį numatoma panaudoti kaip puolimo placdarmą, o tai neišvengiamai paverčia jo šalis Rusijos taikiniu.

JAV politikai ir kariškiai tai supranta, tačiau jie nepergyvena dėl Pabaltijo likimo, prisidengdami veidmainiškais žodžiais apie šių sąjungininkų gynybą. Lietuva, Latvija ir Estija nėra JAV valstijos (nors jų lyderiai to neatsisakytų), šių šalių gyventojai — ne JAV piliečiai. Galima neabejoti nuoširdumu amerikiečių generolo, sakančio, jog JAV pasiruošę kautis su Rusija Europoje. Savo žemėse amerikiečiai paskutinį kartą rimtai kariavo prieš pusantro amžiaus — 1861–1865 metais pilietinio karo metu. Nuo tada jie protingai vengia karų savo teritorijoje, ieškodami naudos karuose kitose šalyse ir kituose kontinentuose.

Visai kita — pačių Pabaltijo šalių vadovai. Kodėl jie nebijo konfrontacijos tarp Rusijos ir NATO ir ginkluočių didinimo savame regione? Jie turėtų suprasti, kad realaus susidūrimo atveju jų šalys bus sunaikintos pirmiausia. Tačiau jie arba to nesupranta, arba vaizduoja nesuprantą. Priešingai, jie reikalauja, kad NATO karinis dalyvavimas Pabaltijyje būtų ženkliai padidintas, kad grėsminga Aljanso grupuotė dislokuotųsi regione pastoviai ir turėtų teisę be NATO Tarybos 5 straipsnio implementacijos nutarimo duoti atkirtį rusų agresijai.

Už visa tai Lietuva, Latvija ir Estija birželio mėnesį kausis NATO samite Varšuvoje.

Kuo gi paaiškinti tokią savižudybe kvepiančią poziciją? Ar tik paranojiška baime, kai dingsta blaivus mąstymas ir tada Pabaltijo politikams vaidenasi, kad antirusišku placdarmu tapusios jų šalys netaps rusų taikiniu, o, priešingai, garantuos karinį nuo Rusijos saugumą? Ne. Čia pagrindinė esmė slypi konjuntūroje.

Amerikiečių karinis monstras, prisidengdamas pabaltijiečių istorija, siekia gauti iš JAV biudžeto keletą milijardų dolerių. Šių pinigų liūto dalis turėtų būti skirta Lietuvos, Latvijos ir Estijos militarizavimui.

Žinoma, į rankas šiuos milijardus gaus amerikiečių kariškiai. Tačiau Pabaltijo šalių vadovybės kunigaikščiai tikisi, kad ir jiems šiek tiek nubyrės.

Šis žaidimas neatsakingas todėl, kad smūgio objektu daro visų pirma eilinius Lietuvos, Latvijos ir Estijos gyventojus. Tačiau šių šalių vadovams nusispjauti į gyventojus: ar galima apie juos galvoti, kai atsiveria svaiginančios perspektyvos sulaukti kariniams tiklsams skirtų milijardų dolerių ir lieka galimybė isterišku riksmu priminti Vakarams apie savo egzistavimą!

Džiaugsmingai šokinėjantys kunigaikštukai negalvoja apie tai, kad jei jų pastangomis iš tiesų Pabaltijyje kas nors prasidės, sunaikinti bus ne tik eiliniai gyventojai. Vargu ar jie patys suspės nunešti kudašių iki artimiausio aerouosto.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 17 — id: `scraped:rubaltic_lt:87d626cfa2b177d3`

**Title:** Lietuva sieks amžinų sankcijų prieš Rusiją

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos vyriausybė pasirengusi reikalauti sankcijų prieš Rusiją pratęsimo tol, kol Maskva negrąžins Ukrainai „atimto“ Krymo. Amžini apribojimai Maskvos atžvilgiu tampa oficialaus Vilniaus antirusiškos politikos evoliucijos naujomis gairėmis.

„Mes niekada nepripažinsime prieš dvejus metus prasidėjusios neteisėtos Krymo okupacijos ir aneksijos. Sieksime, kad Rusijos Federacijai taikomos ES ir tarptautinės sankcijos dėl pusiasalio užėmimo tęstųsi tol, kol Rusija nepasitrauks iš neteisėtai užgrobtos teritorijos“, — sakoma Lietuvos URM pareiškime, paskelbtame, kaip teigiama pačios užsienio politikos įstaigos, „Krymo okupacijos antrųjų metinių proga“. Tokiu būdu, oficialaus Vilniaus antirusiškoje politikoje išryškėja naujos gairės: Lietuvos vairininkai nedviprasmiškai pasisakė už amžinas sankcijas prieš savo rytų kaimyną.

Lietuva ne vakar ėmė vaidinti Rusijos sutramdymo operatoriaus vaidmenį ir reikalauja Kremliaus atžvilgiu „bizūno politikos“. Priminsime, jog 2008 metais oficialusis Vilnius vetavo Maskvos ir Briuselio derybas dėl bevizio režimo tarp Rusijos ir Europos Sąjungos šalių.

Vilnius vienpusiškai ėmė uždarinėti europietiškas duris atskiriems Rusijos piliečiams. Lietuvos funkcionieriams pavyko uždrausti įvažiuoti į visas Šengeno zonos šalis Rusijos politologui Sergejui Michejevui – kaimyninių santykių tarp Briuselio ir Maskvos sureguliavimo šalininkui. Oficialaus Vilniaus diplomatijos vanagai aktyviai rėmė tų Rusijos piliečių „juodųjų sąrašų“ sudarymą ir papildymą, kurių atžvilgiu Briuselis turi taikyti individualius apribojimus.

Rytų kaimynas Lietuvos politikų smegeninėse pamažu virto ne tik nepriklausomos Pabaltijo respublikos, bet ir visos Europos visų nelaimių priežastimi. Žlugus „Rytų partnerystės“ programai, kurią Lietuva ir kai kurie jos europietiški bendraminčiai nuosekliai piešė antirusiškomis spalvomis, oficialaus Vilniaus politikai tuoj pat apkaltino Rusiją. Be abejonės, tik vienintelė Maskva kalta dėl Ukrainos tragedijos. „Besiplečianti Kijeve betvarkė atitinka Kremliaus nuostatoms: sukomprometuoti, suskaldyti ir atplėšti Ukrainą nuo Europos Sąjungos, galutinai įtraukiant ją į Rusijos įtakos lauką“, — teigiama Seimo opozicijos lyderio Andriaus Kubiliaus ir Audroniaus Ažubalio 2013 metų gruodžio 11 d. pareiškime — gerokai prieš karštai užsipliekiant Euromaidano įvykiams. Tuo pat metu (lapkričio-gruodžio mėn.) prezidentė Dalia Grybauskaitė „pašildė“ situaciją Kijeve, ragindama Euromaidano dalyvius „veikti aktyviau“.

Įsibėgėjus krizei Ukrainoje, oficialusis Vilnius plečia savo, kaip operatoriaus, vaidmenį tramdant Rusiją. Lietuva tampa antirusiškų sankcijų varomaja jėga. Būtent jauniausiojo Landsbergio pranešimas tampa Europos parlamento rezoliucijos pagrindu, kuri neleidžia „atkurti normalius santykius besitęsiant dabartinei Kremliaus politikai“. „Rusija prarado pasitikėjimą ir daugiau negali būti Europos Sąjungos partnere“, — skelbiama dokumente .

Lietuvos pirmininkavimas Europos Sąjungos Taryboje ir tuo metu vykęs „Rytų partnerystės“ samitas, kuriuo ir prasidėjo Ukrainoje karinė-politinė katastrofa, tapo Lietuvos vanagų pasididžiavimo objektu. „Lietuva taip didžiuojasi savo pirmininkavimu ES Taryboje, kad su malonumu sutiktų antrą kartą iš eilės pirmininkauti. Tarp savęs mes mėgstame juokauti, kad, jei ne Lietuva, Chorvatija nebūtų liepos 1 d. tapusi 27-ąja ES nare, Ukrainoje nebūtų prasidėjusi antroji oranžinė revoliucija ir jokios kitos šalies ministras nebūtų išdrįsęs uždrausti visoje ES mėtines cigaretes, ką padarė Lietuvos sveikatos apsaugos ministras Vytenis Andriukaitis“, — ciniškai pareiškė Seimo pirmininko pavaduotojas, Europos reikalų komiteto vadovas Gediminas Kirkilas ES valstybių Lietuvoje ambasadoriams iškilmingų pietų lietuviškojo pirmininkavimo pabaigos proga.

Toks Kirkilo „pajuokavimas“, beje, nuostabiai atskleidžia Lietuvos diplomatijos provincialumą, kuriai karinė-politinė Ukrainos katastrofa su daugiatūkstantinėmis aukomis tolygi mėtinėms cigaretėms. Štai ir su Krymu, gąsdindama Rusiją amžinomis sankcijomis, oficialusis Vilnius elgiasi kaip su bulvių maišu. Lietuvos vairininkams, neįpratusiems skaitytis su „laukinėmis slavų tautomis“, nė motais: pusiasalis — ne beasmenis daiktas, kurį galima pirmyn atgal stumdyti. Krymas — 2 mln. gyventojų, kurie 2014 metų referendumo metu vienareikšmiškai pareiškė: „norime būtu su Rusija“, ir negali būti jokios kalbos apie „sugrįžimą“ į Ukrainą.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 18 — id: `scraped:rubaltic_lt:f74c81281bbe5757`

**Title:** 7 dalykai, kurie labiausiai erzina Pabaltijo politikus

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Politika — tvirtų nervų užsiėmimas. Valstybių vairininkai pastoviai susiduria su nemaloniais ir erzinančiais dalykais. RuBaltic.Ru portalas paruošė sąrašą 7 svarbiausių dalykų, kurie sugeba neapsakomai suerzinti bet kurį nacionališkai mąstantį Pabaltijo politiką. Tai, neabejotinai, pagrindiniai bet kurio lygio Pabaltijo vadovo priešai, o todėl kova su jais šiose šalyse vyksta pastoviai.

„Geografija — tai likimas“, — mokė amžininkus Napoleonas Bonapartas. Latvijos, Lietuvos ir Estijos „geografinį likimą“ Pabaltijo politikai mato kaip žiaurų ir nepavydėtiną. Vidutinis pajūrio klimatas, neužterštas oras, pušynai — atrodytų, viskas puiku, tačiau visus šiuos gamtos malonumus temdo didysis rytų kaimynas. Būtent baimė prieš Rusiją, kuri, oficialių Pabaltijo sostinių asmenų nuomone, miega ir sapnuoja, kaip užkariauti šias laisvas tautas, formuoja vidaus ir užsienio politiką. Nerimstančios kaimynystės kompleksas padeda išsilaikyti valdžioje vanagaujantiems antirusiškiesiems funkcionieriams, žadantiems rinkėjams ginti nuo rytų agresijos gimtąsias žemes. „Nepavydėtinas“ geografinis likimas“ verčia Pabaltijo politikus verstis kūliais: Pabaltijo vanagų pareiškimai sukuria fantasmagorinius sūkurius, ir tada mesijinės Kremliaus sulaikymo idėjos pavirsta isterija ir prašymais, kad gynybos tikslais NATO atsiųstų papildomą kontingentą .

Su kaimynais — ypač didžiausiais — reikia draugauti. „Tačiau ne, mes geriau remsime savąsias ekonomiką žudančias antirusiškas sankcijas ir spjausime rytų pasienio kryptimi eiliniu konfrontaciniu pareiškimu, bet su „barbarais“ nedraugausime“.

Nepriklausomybės aušroje nematomos rinkos jėga ir Čikagos neoliberalios mokyklos priesaku patikėję laukinio entuziazmo apimti nauji Pabaltijo elitai puolė naikinti visą tarybinės planinės sistemos paveldą. Buvo nutraukti prekybiniai ryšiai su rytų kaimynais: Rusija, Ukraina, Baltarusija. Prarasta Pabaltijo prekių rinka. Šoko terapijos pasekoje ženkliai sumažėjo ir teberieda išnykimo kryptimi žemės ūkio ir pramonės sektoriai.

Griauti — ne statyti . Deramo ekonominio vystymosi kelio nauji elitai nepasiūlė. Europos Sąjunga, kurios galia aklai tikėjo Pabaltijo vadai, taip pat neatvėrė rojaus sodo vartų. Priešingai, Briuselio direktyvos ir kvotos tebesmaugė pramonę ir žemės ūkį, paversdamos buvusias išvystytos pramonės šalis Latviją, Lietuvą ir Estiją „paslaugų ekonomikomis“. Pagal atlyginimų ir gyventojų gyvenimo kokybę Pabaltijis atsidūrė Europos šalių autsaiderių sąraše, pirmaudamos tik pagal respublikose žodžio laisvės pasireiškimus rodiklius .

Ach, kaip saldžiai miegotų Pabaltijo politikai, jei išvis neegzistuotų ekonomikos, o visos reikalingos gerybės į Latviją, Lietuvą ir Estiją neišdžiūstančiais upeliais tekėtų iš Briuselio. Deja, gyvenama nepasiturinčiai protaujant nepriklausoma galva...

„Okupacijos pasekmės“ — taip Pabaltijo politikai vadina kai kuriuos tėvynainius ir mokesčių mokėtojus. Rusai oficialiems Talino ir Rygos funkcionieriams iki šiol primena kaulą gerklėje. „ Pilietybę atėmėm , apribojome teises, o jie vis nerimsta: kažkokią kultūrą nori išsaugoti, o dar ir vaikus mokyklose gimtąja kalba mokyti“, — guodžiasi tautiškai mąstantys Pabaltijo sostinių politikai. Ir nusispjaut, kad rusų kultūra — vienintelė pirmaeilė senoji Europos kultūra, kuri buvo atvira ir „kvietė“ šios teritorijos senbuvius (tuo skyrėsi nuo uždarosios vokiečių), o „tautų draugystė“ — neatsiejama valstybinio vystymosi sąlyga. Eilinė latvių vyriausybė vėl pradeda savo darbą po kovos su rusakalbiško švietimo likučiais vėliava. Nes į valstybių kūrimo projektą negali patekti „okupantai“ ir jų kalba.

Ar dėl to Pabaltijo šalių judėjimai už nepriklausomybę — Latvijos ir Estijos liaudies frontai ir Lietuvos „Sąjūdis“ — savo tikslais kėlė „viešumą“ ir kovą su tarybine cenzūra, kad po ketvirčio amžiaus galutinai palaidotų mažiausius savo respublikose žodžio laisvės pasireiškimus? Tačiau tai atsitiko... Tautiškai mąstantys politikai išvystė kovą su kitaminčiais visuose informacijos frontuose. Rusakalbė spauda skelbiama „Maskvos ranka“, dėl tų komentarų, kurie tinklalapiuose kertasi su Pabaltijo šalių generaline linija, keliamos baudžiamosios bylos, o „priešiškas“ teleprogramas retransliuojantys kanalai baudžiami didžiulėmis baudomis ir licenzijų pristabdymu.

Štai ir dabar į Latvijoje atsidariusią rusų „Sputniko“ tarnybos versiją skrieja kovotojų prieš žodžio laisvę strėlės. „Latvijos valdžia privalo surasti svertus, neleidžiančius atidaryti šalyje propagandines žiniasklaidos priemones“, — pareiškė eurodeputatas Robertas Zilė. Taigi „tiesos monopolijos“ statyba Pabaltijyje tęsiasi.

„Jeigu faktai prieštarauja mūsų teorijai, blogiau patiems faktams“, — šia formule vadovaujasi naujos Pabaltijo istorinės politikos kuratoriai. O norint kad nereikalingi faktai nepasirodytų, galima, grąsinant kalėjimu, uždrausti abejoti „okupacijos doktrina“, reikšti alternatyvius įvykių Vilniuje sausio 13-ąją vertinimus.

Bet ir nepatogius istorinius įvykius visada galima perrašyti. Sukurti komplimentais tryškiantį miuziklą apie nacių nusikaltėlį šaunų lakūną Herbertą Cukursą arba parašyti knygą apie mirties stovyklą darbo stovyklą — savotišką Salaspilso „vokiečių sanatoriją“.

Tarybinis (pasak šį žodį nekenčiančių — sovietinis) palikimas — štai kas iš tiesų erzina oficialias Pabaltijo sostines. Gatvių pervardinimas, paminklų ir bareljefų griovimas nenuramino latvių, lietuvių ir estų demokratų sielų. Kovos kirvis pakibo virš senų, esą totalitarinių kinofilmų ( „Septyniolika pavasario akimirkų“ ), o apogejaus pasiekė užsipuolus dešreles ir virtą dešrą nusikalstamu „Tarybinės“ pavadinimu.

Tačiau net po „dešreliškos liustracijos“ Pabaltijo elitas nepajėgia ramiai miegoti. Prakeikta „komunizmo šmėkla“ tebegyvena Pabaltijo šalių „naujosios“ nomenklatūros širdyse.

90-ųjų pradžioje išeiviai iš TSKP ir komjaunimo Pabaltijo šalių politinėje elitoje sudarė: Lietuvoje 28, Estijoje 73 ir Latvijoje 75 procentus. Pabaltijo „raudonoji gvardija“ iki šiol iš savo rankų neišleido vairo. Ryškus pavyzdys — Leningrado valstybinio A. Ždanovo universiteto ir Visuomeninių mokslų akademijos prie TSKP CK absolventė, mokslinė Vilniaus partinės mokyklos sekretorė Dalia Grybauskaitė .

Šių dienų kovingam antikomunizmui ir totalitarinių mundurų pakeitimui demokratiniais europietiškais švarkais, žinoma, būdingas terapeutinis charakteris, tačiau visa tai neišgydys ligos: labiausiai Pabaltijo elitą slegia jo paties tarybinė praeitis.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 19 — id: `scraped:rubaltic_lt:2ed7ef80067947f4`

**Title:** Prezidentas Adamkus slepia savo dalyvavimą Holokauste?

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Buvęs Lietuvos prezidentas Valdas Adamkus galimai dalyvavo Holokauste Lietuvoje. Iš oficialios biografijos tokie „nepatogūs“ epizodai ištrinti, visai neseniai panašiai buvo nuslėpta dabartinės Lietuvos prezidentės Dalios Grybauskaitės „raudonoji praeitis“.

Buvusi mažametė Minsko geto kalinė Cvija Kacnelson apkaltino buvusį Lietuvos prezidentą Valdą Adamkų antisemitizmu. Perskaičiusi Adamkaus memuarus, Kacnelson nustebo, kodėl kaunietis savo prisiminimuose neskyrė dėmesio tragiškiems šio miesto žydų likimams. Dar labiau ją nustebino, kad 1944 metų rudenį būsimasis prezidentas tarnavo liūdnai pagarsėjusio majoro Antano Impulevičiaus pavedimų vykdytoju. Impulevičius išgarsėjo organizuodamas susidorojimus su Lietuvos ir Baltarusijos žydais, o į Holokausto istoriją pateko pravarde „Minsko mėsininkas“. Impulevičiaus ir jo bendrų talentus masiškai naikinant žydus aukštai vertino vokiečių vadovybė. Lietuviai su tokiu noru it profesionalumu žudė, kad vokiečiai specialiai vežė jiems aukas iš kitų okupuotų teritorijų.

Rūta Vanagaitė, knygos „Mūsiškiai“ apie Holokaustą Lietuvoje autorė:

„ 5000 Austrijos, Čekijos žydų nužudyta lietuvių IX forte. Čia juos vežė skiepytis – žydai ėjo į duobes atraitomomis rankovėmis laukdami skiepo. Lietuviai taip gerai dirbo, kad Antano Impulevičiaus batalioną išvežė į Baltarusiją – ten nužudė 15 tūkst. žydų. Vokiečiai buvo nepaprastai patenkinti “ .

„Adamkus negalėjo nežinoti tiesos apie Impulevičių, apie žydų žudynes Lietuvoje ir konkrečiai Kaune. Jaunuolis negalėjo nežinoti bendro vaizdo, jis žinojo ir apie atvykstančius į Kauno stotį mirties ešelonus, todėl kad buvo aukšto geležinkeliečių pareigūno giminaitis“, — pasipiktino Kacnelson. Adamkaus tėvas Ignas Adamkevičius iš tiesų karo metais vadovavo Kauno geležinkelio stoties policijai. Adamkus memuaruose rašo, kad galėjo pasirinkti bet kurią tarnybos vietą, bet nukeliavo į Impulevičiaus batalioną, tačiau apie jo nusikaltimus neužsimena, — pažymi portalas BaltNews.lt.

Adamkus stengiasi neskelbti savo buvimo Impulevičiaus dalinyje. Įvairios oficialios biografijos skelbia, kad jis su šeima 1944 metų vasarą bėgo iš Lietuvos į Vokietiją, bijodamas tarybinės kariuomenės ir pakartotinos okupacijos. Tuo ir baigiasi šio politiko „karinis laikotarpis“.

Lietuvos žiniasklaida nemėgsta kapstytis šio savo lyderio kovinės šlovės plonybėse. Aprašomų įvykių metu Valdas Adamkus buvo 17-metis gimnazistas savanoris (gimė 1926 metais Voldemaro Adamkevičiaus vardu). Jis buvo žinomas kaip idėjinis Lietuvos nepriklausomybės šalininkas ir antitarybinio pogrindžio aktyvistas, su bendraklasiais talkino spausdinant propagandinius laikraščius ir lapelius, tame tarpe „Laisvą kovotoją“ — pagrindinį Kovos už Lietuvos laisvę sąjungos žinyną. Sąjunga buvo įkurta 1940 metais kovai su tarybų valdžia. Atėjus vokiečiams ji rėmė juos ir didžiavosi, kad daug lietuvių įstojo į Vermachto gretas.

Atviras 1942 m. liepos 7 d. Kovos už Lietuvos laisvę sąjungos laiškas pilietinės administracijos vokiečių komisarams (pagal Petro Stankerio knygą „Lietuvos policijos batalionai. 1941–1945 m.“):

„...A.Hitleris pareiškė, kad Vokietijai Rytuose padeda beveik visos Europos tautos. Tarp jų jis paminėjo lietuvius, estus, ukrainiečius ir totorius. Mes manome, kad mūsų savanoriai Rytuose turi apie 8000–10000 durtuvų... Lietuvių tauta santykiu savo gyventojų skaičiumi davė karių daug daugiau, negu visos išvardintos tautos“.

Pasak Adamkaus, po to, kai artėjant Raudonąjai armijai išbėgo šeima, jis sugrįžo į tėvynę ir įstojo į Tėvynės apsaugos rinktinę (TAR). Šis dalinys dar žinomas kaip Tėvynės gynimo legionas, Tėvynės gynimo kariuomenė (TGK), Žemaitijos draugovė, vokiečių suvestinėse — Žemaitijos šucmanšaftas arba Kovinė Mederio grupė (Kampfgruppe Mäder).

Ši organizacija susikūrė 1944 metų liepos 29 d. Keli Lietuvos karininkai susirinko Telšių apylinkėse tikslu aptarti, stoti į Vermachtą ir tiesiogiai kovoti su Tarybomis ar tapti savarankišku koviniu vienetu ir vystyti partizaninę veiklą. Nedidele balsų persvara pasirinko antrąjį variantą. Draugovę sudarė kelių sutriuškintų ir paleistų Lietuvos kolaborantų grupuočių likučiai, kurie buvo praskiesti idėjiniu jaunimu.

Istorikas Petras Stankeras, „Lietuvos policijos batalionai. 1941–1945 m.“:

„Ją sudarė pagrindinai iš Aukštaitijos atsitraukę Lietuvos policijos bendradarbiai, kariškiai ir karingai nusiteikęs jaunimas. TGK kariai dėvėjo Vermachto uniformą (vokiečiai neprieštaravo, kad ant kairiosios rankovės būtų prisiūta tautinių spalvų juostelė, o kariniai sunkvežimiai turėtų „Gedimino stulpų“ emblemą), apginkluoti buvo prancūzų ir tarybiniais ginklais. Idėjinis TGK įkūrėjas buvo kunigas, psichologijos daktaras, Zarasų burgomistras Jonas Steponavičius. Jis tikėjosi, kad vokiečių fizikai sukurs slaptą atominį ginklą ir sustabdys Raudonosios armijos puolimą“.

Be buvusių Lietuvos teritorinio apsaugos korpuso (Lietuvos vietinė rinktinė, Schutzkorps Litauen) policininkų į draugovę įsiliejo Vermachto pionierių bataliono ir aviacijos apsaugos dalinių lietuviai. Kunigo pagalba draugovininkai užmezgė kontaktą su Šiaulių gynybai vadovavusiu vokiečių pulkininku Helmutu Mederiu (Hellmuth Mäder) ir paprašė materialios pagalbos. Mederis davė (pagal kitą versiją pardavė) lietuviams ginklų ir uniformų ir tapo rinktinės kuratoriumi.

Valdas Adamkus, Lietuvos prezidentas 1998–2003 ir 2004–2009 m., memuarai „Likimo vardas — Lietuva. Apie laiką, įvykius, žmones“:

„Atvykau į štabą, prisistačiau. Adamkevičiaus pavardė buvo gerai žinoma kariškiams, nes mano dėdė buvo Lietuvos kariuomenės divizijos generolas, vadovavo Kauno karinei apygardai, man ji Sedoje atvėrė visas duris“.

Karininkai draugovininkai norėjo, kad jiems vadovautų Adamkaus dėdė — Edvardas Adamkevičius , dimisijos divizijos generolas, tarnavęs dar caro kariuomenėje. Štabas pasiuntė sūnėną prikalbinti dėdę, bet jam tai nepasisekė.

Tada vadovauti draugovei ėmėsi kapitonas Izidorius Jatulis. Antrajam pulkui, kuriame tarnavo Adamkus, vadovavo papulkininkas Mečys Kareiva, po jo — papilkininkas Matas Naujokas. Draugovės štabo archyvas karo metu išliko ir buvo išvežtas į užsienį. Lietuvos kariuomenės amerikiečių istorikas Henri L. Gaidys atkūrė draugovės vadovavimo struktūrą ir tai, kad „Minsko mėsininkas“ Impulevičius vadovavo 2-ojo pulko 1-ajam batalionui. Impulevičiaus pareigas Tėvynės gynimo kariuomenėje patvirtino istorikas Andrejus Stoliarovas savo darbe, kurį išleido Kauno Vytauto Didžiojo universitetas ir kuris buvo skirtas Lietuvos policijos batalionams.

Mederis svajojo, kad suvienyta Lietuvos draugovė laikui bėgant taps divizija, tačiau ji išsilaikė tik keletą mėnesių, kol Raudonoji armija ją galutinai nesutriuškino ties Telšiais ir Seda 1944 metų spalio mėn.

Istorikas Sergejus Čujevas, „Prakeiktieji kareiviai. Išdavikai III reicho pusėje“:

„Armijos“ likučiams, kuriuos sudarė apie 1000 žmonių, pavyko pasitraukti su vokiečiais į Rytų Prusiją, kur ji buvo performuota į aštuonių kuopų lietuvišką pionierių batalioną. Batalionas statė Baltijos pakrantėje įtvirtinimus, o vėliau pateko į Kuršo katilą. Ši aplinkybė sudarė sąlygas daugeliui karių nerti į Lietuvos miškus ir tapti partizaninio karo tarybiniame užnugaryje rezervu“.

Valdas Adamkus, Lietuvos prezidentas 1998–2003 ir 2004–2009 m., memuarai „Likimo vardas — Lietuva. Apie laiką, įvykius, žmones“:

„...ties Mažeikiais prasidėjo sutelktinis tarybinės armijos puolimas. Viską aplink šluodami, į miestelį įsiveržė rusų tankai. Mes neturėjome ginklų, mes negalėjome pasipriešinti, tačiau į mus buvo atidengta beprotiška ugnis, privertusi gelbėtis bėgant atviru lauku, kurį akėjo sviediniai ir kulkos... Kyburiuodami ant bėgančios vokiečių armijos karinių sunkvežimių bortų, mes judėjome Baltijos jūros kryptimi. Kretingos geležinkelio stotyje dar stovėjo ant platformų sunkūs tankai, kuriuos vokiečiai tikėjosi išvežti iš uždaromo apsupimo žiedo. Nutaikęs momentą, kai sargybiniai atsuko į mane nugaras, aš užšokau ant vienos platformos ir palindau po tanku“.

Taip Adamkui prasidėjo „nepalankios aplinkybės“.

Į Ameriką iškeliavo ir Impulevičius. Jis apsigyveno Filadelfijoje, kur ir numirė 1970 metais. Tarybinis teismas už akių nuteisė jį mirties bausme, tačiau amerikiečių valdžia atsisakė jo išduoti.

Tarnybos su savo liūdnai pagarsėjusiu bendražygiu smulkmenas Adamkus linkęs nutylėti. Mes kreipėmės į signatarą Zigmą Vaišvilą, pagarsėjusį pirmojo Lietuvos politikų ešelono tamsių biografijų vietų tyrimais.

Zigmas Vaišvila, politikas, verslininkas, Lietuvos nepriklausomybės atkurimo akto signataras:

„Miglotos vietos mūsų lyderių istorijose — neretenybė. Nieko nuostabaus, kad visi mūsų prezidentai, išskyrus Brazauską, turi „baltų dėmių“. Daug ko apie jų gyvenimą nežinome, ypač tai liečia žmones, atvykusius iš toli, iš Europos arba Amerikos. Daugelis bando retušuoti savo biografijų tarybinius laikotarpius, bet ne tik — kai kurie nutyli karjerą 90-ųjų pradžioje ir kuo jie užsiiminėjo karo metu. Kas dėl Adamkaus, ilgą laiką gyvenusio užsienyje, čia dar mažiau aiškumo“.

Pats Adamkus visada didžiavosi kovine praeitimi. Prezidentinio maratono 1997 metais metu, būdamas istorinėje tėvynėje mažai žinomas, jis apsilankė Sedoje tikslu susitikti su vietiniais gyventojais. „Kas tave pasiuntė? — pasidomėjo vietinis gyventojas. — JAV vyriausybė ar tu pats atvažiavai?“ Būsimasis prezidentas susierzinęs parodė pirštu bulvienojaus kryptimi, kur 1944 metais krito jo draugai, ir eilinį kartą ėmė pasakoti susirinkusiems, kaip kovėsi su tarybiniais tankais už Lietuvos laisvę.

Vėliau, 2012 metų nepriklausomybės dieną, jis vėl dalinosi prisiminimais apie jaunimo ryžtą eiti mūšin.

Valdas Adamkus, Lietuvos prezidentas 1998–2003 ir 2004–2009 m. :

„Vienas ryškus epizodas, demonstruojantis jaunatvišką maksimalizmą ir idealizmą, [...] nutiko Sedoje ir Barstyčiuose... Karo metu, kai tarybinė armija artinosi prie Lietuvos, Sedoje buvo formuojami savigynos ir lietuviškieji žemaičių būriai. Patriotiškumas ir idealizmas tryško sąlygomis, kai nebuvo logikos, kai jaunimas būrėsi Sedoje tuščiomis rankomis. Jauni žmonės troško ginti tėvynę, nors neturėjo ginklų. Pamenu, buvo vokiški pistoletai ir jiems netinkamos prancūziškos kulkos. Dabar visa tai bandoma apversti, pasakyti, kad mes tarnavome vokiečių kariuomenei. Aš savo kailiu patyriau mūšius ties Seda, juose krito apie šimtas nuostabių lietuvių. Likimas leido man išlikti ir iškeliauti į Vakarus“.

Beje, Lietuvoje yra abejojančių, jog būsimasis prezidentas dalyvavo koviniuose veiksmuose. Pagal leidinio „XXI Amžius“ duomenis, jaunasis Adamkus buvo nukreiptas į bataliono štabą vertėju.

Stanislovas Abromavičius, poetas ir rašytojas :

„Mūsų būsimajam prezidentui tada buvo tik 17 metų. Tvirtinama, jis net nebuvo apginkluotas ir, matyt, ten pateko atsitiktinai“.

Žurnalistas ir publicistas Česlovas Iškauskas teigia , kad, nepaisant gandų, „kovų už nepriklausomybę“ didvyriams galėjo būti 17–18 metų, ir pateikia veterano, „Kovos dvasia“ memuarų autoriaus Vlado Kazlausko pavyzdį.

Apie tai, kokie buvo lietuviškų kolaborantų būriai, mums papasakojo istorijos mokslų daktaras, RMA Sankt-Peterburgo istorijos instituto vedantysis mokslinis bendradarbis Borisas Kovaliovas :

— Kuo įsiminė lietuviškieji daliniai, veikę kartu su Vermachtu?

— Lietuvių būriai pagrindinai atliko baudžiamąsias funkcijas, kovojo su partizanais, kaimuose atiminėjo maisto produktus. Juos prisimenama blogu žodžiu. Aš rašiau knygą apie ispanų „Melsvą diviziją“. Vietiniai gyventojai pasakojo, kad jie buvo vagys ir čigonai — taip jie vadino ispanų savanorius — vietoj jų atėjo žudikai ir sadistai. Nesuvokiamas žiaurumas buvo būdingas Lietuvos ir Latvijos daliniams.

— Kieno iniciatyva buvo formuojami lietuviškieji būriai?

— 1941 metais labiausiai pasireiškė „apačių iniciatyva“. Noras parodyti save vokiečių ir naujos valdžios sąjungininkais.

Būriai savo turiniu galėjo būti savanoriški, tačiau karinių formuočių sudarymas vyko griežtai vokiečiams kontroliuojant. Nepasakyčiau, kad vokiečiai juos naudojo sunkiausiuose fronto ruožuose. Lietuvius naudojo „šlykščiausiuose“ ruožuose. Kartais vokiečiams reikėjo pasireikšti santykiuose su vietiniais gyventojais „gerų tyrėjų“ vaidmenyje, siekiant į juos geresnio, nei į sąjungininkus, požiūrio. 1944 metais hitlerininkai buvo pasiruošę be išimčių rinkti visus norinčius kautis vienose su jais gretose. Esmė tame, kad nacių Vokietija tuomet jau pradėjo prarasti savo pagrindines sąjungininkes — Italiją, Suomiją, Rumuniją. Vokietija buvo pasiruošusi jungtis su bet kuo, bet ką žadėti, kad tik būtų sutelkti sąjungininkų būriai.

— Kalbama, Žemaitijos draugovė buvo labai prastai aprūpinta, stokojo ginklų, šaudmenų...

— Taip, lietuviškieji būriai turėjo tenkintis likučiais. Geriausiais ginklais ir rūbais buvo aprūpinami vokiečių kareiviai. Reichas daugiausia rėmė žodžiais.

O ar buvo Reichas suinteresuotas teikti jiems paramą? Būtina suprasti, kad ir Lietuvos kareivių kokybė nevisada buvo aukšta kaip Vermachto.

— Buvęs prezidentas Valdas Adamkus prisimena, kad įstoti į draugovę jį paskatino patriotiški idealai ir noras kovoti už Lietuvos laisvę. Ar galėjo jis ir kiti jauni lietuviai nežinoti, kad jie faktiškai kaunasi vienose gretose su Impulevičiumi ir kitais nacių nusikaltėliais?

— Tai sudėtinga. Net daugelis vokiečių generolų tardymo metu įrodinėjo nieko nežinoję apie koncentracijos stovyklas ir SS veiklą. Manau, tai nerimti argumentai. Lietuva — šalis nedidelė. Kur dingo tūkstančiai kaimynų žydų, žinojo visi. Kas dėl patriotiškų jausmų, taip — nacių propaganda daug ko žadėjo. Tačiau ji žadėjo rusams viena, baltarusiams — antra, ukrainiečiams — trečia, lietuviams — ketvirta. Dažnai tai buvo nesuderinami dalykai. 1944 metais nacių propaganda veikė principu „kad tik išlikti“. Jeigu žmogus teigia, jog po to, kas Lietuvoje jau įvyko karo metais, ir jau realiai galima buvo suvokti nacių okupacinio režimo esmę, jis 1944 metais įstojo į būrį ne prievarta ir ne dėl mirties grėsmės tėvams, o patriotiškų jausmų vedinas, man gaila tokio jauno žmogaus.

Viso Lietuvoje žuvo apie 200 tūkstančių žydų, t.y. virš 90% prieškarinio žydų skaičiaus. Pagal Žydų universiteto Jeruzalėje istoriko ir buvusio Kauno geto kalinio Dovos Levino , Holokauste dalyvavo 10–20 tūkstančių lietuvių, žudžiusių žydus daugiau kaip 200 salies vietose. Tačiau masinių žydų žudynių lietuvių rankomis tema nutylima valdžios ir visuomenės. 1990-ųjų metų pradžioje prasidėjo pirmieji lietuviškųjų pagalbininkų naciams procesai. Amerikiečiai atėmė pilietybę buvusiam leitenantui Jonui Stelmokui, kai atsirado jo tarnybos 3-iame pagalbiniame policijos batalione įrodymų. Policininkas paskelbė, kad dokumentus suklastojo VSK, o specialusis prokuroras, kuriam buvo pavesta ištirti karo meto nusikaltimus, Vidmantas Vaicekauskas 1992 metais pasakė, kad skaičius lietuvių, padėjusių naciams žudyti žydus, labai išpūstas ir nesiekia tūkstančių.

Efraimas Zurofas, Jeruzalės Simono Vizentalio centro vadovas, žinomas „nacių medžiotojas“:

„Niekada nepamiršiu susitikimo su Lietuvos valstybės vadovu Vytautu Landsbergiu, kuris įvyko 90-ųjų metų pradžioje. Atsakydamas į mano siūlymą ištirti Holokaustą, jis parodė man knygą apie masiškus lietuvių trėmimus į Sibirą ir pasakė: „Štai mūsų Holokaustas“.

Istorinės Holokausto atminties klausimu Adamkaus administracija vykdė prieštaringus veiksmus. Pirmasis lietuvių kaltę pripažino ir Izraelio atsiprašė prezidentas Brazauskas. Adamkus tai pratęsė. Jis ne kartą smerkė ir patį Holokaustą Lietuvoje, ir lietuvių dalyvavimą masiškose žydų žudynėse. Jis pastoviai dalyvavo atmintinose ceremonijose, viešai lenkė galvą prie memorialo Paneriuose — apie 70 tūkstančių žydų žūties vietoje.

2000 metais Seimas nutarė oficialiai paskelbti birželio 23 dieną atmintina 1941 metų antitarybinio sukilimo diena. Tada kartu su tarybinės kariuomenės atsitraukimu Laikinoji Lietuvos vyriausybė paskelbė atkurianti respubliką. Ta diena laikoma ir Holokausto Lietuvoje pradžia, kai vietiniai gyventojai, valdžiai padedant, nelaukdami, kada vokiečiai užims Kauną, puolė areštuoti ir žudyti žydų. Daugelis pradėjo nuo kaimynų. Todėl parlamento nutarimą Adamkus pavadino gėda ir atsisakė pasirašyti įstatymą. Seimui teko paklusti. Pripažino Adamkus savo tautos nuodėmes ir prieš lenkus. 2004 metais jam tarpininkaujant įvyko simbolinis Lietuvos partizanų susitaikymas su Krajovos armijos kariais (lietuviškieji kovotojai už nepriklausomybę trukdė išlaisvinti Vilnių).

Adamkaus laikais buvo bandyta išaukštinti Laikinosios vyriausybės vadovą Juozą Ambrazevičių. Tais pačiais 2000 metais, Landsbergiui pasiūlius, Seimas ruošėsi pripažinti antisemitinį Ambrazevičiaus kabinetą (egzistavo nuo 1941 m. birželio 23 iki rugpjūčio 5 d.), įtraukiant jo lyderį į teisėtų Lietuvos vadovų panteoną. Ambrazevičius aktyviai bendradarbiavo su naciais, išleido „Žydų statutą“. Pagal hitlerininkų Niurnbergo įstatymus paruoštas dokumentas skelbė Lietuvos žydus antrarūšiais piliečiais. Jiems buvo draudžiama net dviračius turėti. Šios vyriausybės Komunalinio ūkio ministras buvo Landsbergio tėvas Vytautas Landsbergi-Žemkalnis (jo sūnus Gabrielius buvo Adamkaus bendraklasis, spausdino su juo laikraščius ir, kaip praneša Iškauskas, atvedė jį į mūšio vietą ties Seda). Žurnalistei Rūtai Janutienei pavyko rasti dokumentus, pagal kuriuos Landsbergis-Žemkalnis prieš karą studijavo architektūrą kartu su nacių ideologu Alfredu Rozenbergu. Ministerija savo ruožtu talkino vokiečiams įrengiant Kauno getą. Visuomenei reikalaujant skandalingas įstatymas buvo atšauktas. Tačiau 2009 metų birželio mėnesį (likus mėnesiui iki prezidento kadencijos pabaigos) Adamkus po mirties apdovanojo Ambrazevičių (jį iškilmingai perlaidojo jau Grybauskaitei prezidentaujant) Vyčio kryžiaus ordino Didžiuoju kryžiumi.

Genocido ir rezistencijos (pasipriešinimo) tyrimo centras kovotojais už laisvę pripažino Antaną Baltušį-Žveją, Vincą Kaulinį-Miškinį ir Juozą Krikštaponį. 2002 metais Adamkus visiems jiems po mirties suteikė garbės pulkininmo vardus.

Visi trys žudė žydus , ką kartojo žydų organizacijos ir teisėsaugininkai. Tik praėjus dešimčiai metų po įsako pasirašymo Genocido centras pripažino, kad buvusio prezidento Smetonos sūnėnas „karo didvyris“ karininkas Krikštaponis 1941 metų vasarą įstojo į 2-ąjį Impulevičiaus policijos batalioną ir tapo vienu iš vadų.

Slucko apygardos gebitskomisaras Heinrichas Karlas skundėsi savo šefui, Minsko generaliniam komisarui, lietuvių sadizmu.

„Mūsų istorikai vis dėlto aptiko nepaneigiamai liūdijančius dokumentus, patvirtinančius jo dalyvavimą Baltarusijoje kartu su A.Impulevičiaus batalionu tose egzekucijose, nes jis buvo 2-osios kuopos vadas“, — pranešė Genocido tyrimo centro direktorė Birutė Burauskaitė. Apie Baltušį-Žveją Centras nieko blogo neaptiko — jis „tik“ saugojo Maidaneko koncentracijos stovyklą. Vadinasi, jo pareiga buvo šaudyti į potencialius bėglius iš mirties fabriko. Pasak enciklopedijos „Jad va-Šem“, Maidaneke žuvo 360 tūkstančių žmonių.

Birutė Burauskaitė, Lietuvos gyventojų Genocido ir rezistencijos tyrimo centro generalinė direktorė:

„Vienintelis jam inkriminuojamas kaltinimas — jo būrys saugojo maidaneko koncentracijos stovyklą. Tai buvo išorinė sargyba“.

Pasiekus abu tikslus, tyrimai buvo nutraukti, o Adamkaus antrojo prezidentavimo metu pagreitį įgavo „dviejų lygiagrečių Holokaustų teorija“, kurios tikslas — nuslėpti tikruosius Lietuvos piliečių nusikaltimų mastus.

Istorikas Icchakas Aradas, buvęs Katastrofų ir Didvyriškumo muziejaus „Jad va-Šem“ (1972–1993 m.) direktorius, „Holokaustas Lietuvoje ir jo nuslėpimas. Pagal Lietuvos šaltinius“:

„Siekiant iškraipyti ir nutylėti lietuvių dalyvavimo masinėse žydų žudynėse faktus, imta perrašinėti istoriją. Išgalvojo žydų ir lietuvių Holokausto istorijas, kurias lietuviai pavadino atitinkamai ruduoju ir raudonuoju Holokaustais. Pagal šią teoriją, „rudojo Holokausto“ aukos buvo žydai, o dėl to kalti vokiečiai ir keli šimtai lietuvių; „raudonojo Holokausto“ aukos buvo lietuviai, o kalti žydai-bolševikai“.

Lietuvių dalyvavimas Holokauste tema labai skausminga, todėl liesti ją bijoma ir po 70 metų.

Rūta Vanagaitė, knygos „Mūsiškiai“ apie Holokaustą Lietuvoje autorė:

„Iki tokio laipsnio bijoma, kad susiduriu su absoliučia panika – nuo aukščiausių valdžios institucijų iki žmogaus kaime. Per pusmetį sutikau tik keletą žmonių, kurie nebijojo. Net su istorikais parke ant suolelio tekdavo susitikti... Kai kurių istorikų negaliu cituoti – jie nenori, vienas jų pasakė nuo šiol nebeskaitysiantis paskaitų šia tema – pavojinga…Tai balta dėmė mūsų istoriografijoje. Kodėl netirta? Yra tik keli istorikai, kurie tuo užsiima – man sakė, penki žmonės turėtų dirbti penkerius metus, kad ištirtų, kiek lietuvių dalyvavo Holokauste. N ė ra penki ų ž moni ų ir penkeri ų met ų”.

Panaši problema ir dėl Holokausto dalyvių vardų paviešinimo. Genocido tyrimo centras 2012 metais perdavė vyriausybei 2055 Hitlerio talkininkų vardus. Valdžia nei išspausdino sąrašo, nei tyrimą pradėjo. Centras šiemet nutarė pagarsinti 1000 talkininkų vardų, įtraukiant juos į naują knygą, tačiau po dviejų dienų pareiškė, jog geriau pirma persiųs sąrašą į prokuratūrą, nes klausimas per daug jautrus.

Istorikas Aleksandras Diukovas, fondo „Istorinė atmintis“ direktorius:

„Kalbėdami apie Holokaustą, Lietuvos tyrėjai baiminasi konfrontacijos su ta visuomene, kurioje gyvena. Holokaustas Lietuvoje niekada nebus ištirtas, o priežastis labai paprasta: nusikalto tada tie, kurie dabartinėje Lietuvoje paskelbti tautos didvyriais“.

Taigi nesunku suprasti, kodėl mažai kas išdrįsta „kasinėti“ ir pergyventi dėl valdžiai ir šalies visuomenei nepatogaus istorijos momento. Apie tai, ką matė, nutyli ir pirmieji valstybės asmenys, ir eiliniai kaimo žmonės. Kolaboravimas ir bendradarbiavimas su vokiškaisiais okupantais dėl laisvės ir nepriklausomybės iliuzijos žengė koja kojon su masišku antisemitizmu, kurį pakeitė masiškas tylėjimas.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 20 — id: `scraped:rubaltic_lt:704edd9f927dd3c6`

**Title:** Kinas ir Lietuviai: kuo Štirlicas neįtiko Lietuvai?

**Source:** rubaltic_lt (propaganda)

**Text:**

```
„Europietiško pasirinkimo“ neofitų bandymas pademonstruoti savo atotrūkį nuo tarybinės praeities ir neapsakomą meilę vakarietiškam pasauliui baigiasi konfūzu. „Tikrųjų europiečių“ snobizmas akivaizdžiai demonstruoja savo nuosmukį, nemokšiškumą ir kultūros stoką, o neapykanta Rusijai, rusams ir tarybiniam laikotarpiui tampa savų kompleksų demonstravimu.

Stambiausias Lietuvos žiniasklaidos portalas Delfi.lt patalpino tarybinio teleserialo „Septyniolika pavasario akimirkų“ recenziją . Deja, sunku suvokti, kodėl šiam Lietuvos valdžios ruporui prireikė grįžti prie tarybinio kino klasikos. Pastaruoju metu nesimatė jokių informacinių priežasčių, kurios būtų paskatinusios prisiminti šį žymų Tatjanos Lioznovos telefilmą. Gal svarbiausiai Delfi.lt portalo skaitytojai taip įgriso jai adresuoti anekdotai apie Štirlicą, kad Daukanto aikštėje buvo paruoštas užsakymas duoti „Lietuvos šmeižikams“ atitinkamą atkirtį?

Kaip ten bebūtų, Andriaus Užkalnio straipsnyje nėra meninės kritikos — jis perpildytas srautu įžeidimų, kurie adresuoti ne tik „Septyniolikai pavasario akimirkų“, bet ir tarybiniam kinematografui bei visam tarybiniam laikotarpiui.

„Iš ekrano tiesiog lipa netikusi, medinė sovietinė kino vaidyba: aktoriai įpratę vaidinti teatre, ir filmavimo aikštelėje atrodo kaip scenoje, tarp dekoracijų. Gausu ilgų mąslių žiūrėjimų į niekur, daugiareikšmių pauzių, neva skvarbių žvilgsnių, reiškiančių, kad veikėjui galvoje sukasi šimtas labai svarbių minčių“ — rašo lietuviškasis „kino kritikas“.

Tačiau tame, kad šis filmas tapo kulto objektu, nėra nieko nuostabaus: kokie žmonės, toks ir jų kultas, o tarybiniai žmonės buvo nepaslankūs ir buki. „Filmą žiūrint šiandien, stebina lėti planai ir nežmoniškai vangūs režisieriaus sprendimai, regis, skirti tikrai negreito proto žiūrovui (tokiam jie ir buvo skirti – filmą žiūrėjo šalyje, kurioje dešimt metų buvo normalus didelio pastato statybos laikas ir kur žmonėms nepabosdavo žiūrėti į augančią žolę arba džiūvančius dažus)“, — rašo žmogus iš šalies, kurioje masiška gyvenamųjų namų statyba prasidėjo kaip tik tarybiniais laikais.

„Nepaslankaus proto žmonės“ vietoj vienkiemių su patogumais už namo statė šiuolaikiškus miestų rajonus, kuriuose iki šiol gyvena dauguma lietuvių. „Nepaslankaus proto žmonės“ užasfaltavo Lietuvoje kelius, pratiesė dujas ir elektrą į kiekvieną namą. Jie statė mokyklas, ligonines, vaikų darželius ir kultūros namus, aprūpindami socialine infrastruktūra daugelį būsimų Lietuvos gyventojų kartų.

Jei jau atsisakai laikyti save šių žmonių darbų tęsėju, tai bent pademonstruok elementarų padorumą ir padėkok jiems. Tai kad ne: visi jie buvo buki ir filmus žiūrėjo bukus, tačiau serialas apie Štirlicą nebuvo bukiausias, todėl ir įsiminė; jis „ buvo trimis galvomis aukščiau už šlamštą šalies ekranuose“.

„Ko vertas sovietinis kinas, lengva suprasti iš paprasto fakto, kad Sovietų Sąjungoje net indų filmai buvo populiaresni už vietinę produkciją. Indų filmai, kaip žinia, yra visi nufilmuoti pagal vieną kvailą pasakos scenarijų (princesė įsimyli sodininką), su tais pačiais aktoriais ir su tuo pačiu garso takeliu, ir idealiai tinka tiems žiūrovams, kurių intelekto koeficientas yra vienaženklis ir kurie, jei gyventų vazonuose, turėtų būti laistomi drungnu vandeniu, — iš savo intelektualių aukštumų spjaudo panieką recenzijos autorius. — „Legendiniu filmu“ tais laikais tapdavo daugmaž raštingai susukta juosta, pacukrinta seilėtais sentimentais ir lėkštoka, bet įtikinama meilės istorija šalyje, turėjusioje daugiausiai pasaulyje nelaimingų, išsiskyrusių moterų, kurioms beliko svajonės apie laimę ir šeimyninį švelnumą“.

Štai kaip! Kliuvo ir tarybiniams filmams, ir vargšėms išsiskyrusioms moterims, ir net indų kinui (jam už ką?). Ir visa tai — nuo stambiausio Lietuvos portalo, šalies, nuosavą kinematografą kuri turėjo tik būdama TSRS sudėtyje ir kuris dingo kartu su ja. Skirtingai negu nedėkingi palikonys, didysis Lietuvos aktorius Donatas Banionis, palyginimui, žinojo, kad pagrindinį vaidmenį Tarkovskio filme „Soliaris“ jis gavo dėka tarybinio kinematografo, ir tas vaidmuo davė jam viso pasaulio pripažinimą.

„Šiandien tai („Septyniolika pavasario akimirkų“ — RuBaltic.ru past.) atrodo naiviai ir vaikiškai, ypač palyginti su tų pačių laikų Holivudo kino produkcija, kuri atrodo maždaug penkiasdešimčia metų priekyje (visų laikų geriausias filmas, „Krikštatėvis“, pasirodė metais anksčiau, 1972-aisiais)“, — rašo Andrius Užkalnis.

Taigi autorius įsitikinęs, jog menas — ta žmogaus veiklos sritis, kurioje egzistuoja inovacinis vystymasis ir judėjimas pirmyn. Jei taip, tada ir televizorių gamyba yra tas pats, kas tapyba. Leonardas da Vinčis lyginant su impresionistais — akmens amžius, tačiau ir impresionistai jau moraliai ir technologiškai paseno ir neatlaiko rimtos konkurencijos su „Juoduoju keturkampiu“.

O ką, tokiu atveju, A.Užkalnis laiko kinematografo judėjimo pirmyn kriterijais? Pagal kokius kriterijus jis daro išvadą, kad Holivudo produkcija mažiausiai 50 metų aplenkė tarybinį kiną? Atsižvelgiant į daugybę nusiskundimų, kad „Septyniolikos pavasario akimirkų“ siužetas vystosi lėtai ir prislopintai, kino vystymosi kriterijus yra greitis. Kuo greičiau juda filmas, kuo daugiau jame specialių efektų, muštynių, scenų lovose — ir dar kad būtų galima, alų geriant, pažvengti, — tuo kokybiškesnis ir šiuolaikiškesnis jis kaip meno kurinys.

Vadovaujantis šiais kriterijais į istorijos šiukšlyną turi būti išmesti, kaip beviltiškai pasenę, ne tik „Septyniolika pavasario akimirkų“, bet Ingmaro Bergmano, Mikelandželo Antonioni, Stenli Kubriko ir t.t. filmai. Šie kinematografo šedevrai, pasirodo, per daug nuobodūs, ir mėgsta juos ne aukštos kultūros žmonės, o „nepaslankaus proto“.

Tai galima pasakyti ir apie „visų laikų geriausią filmą „Krikštatėvis“, kuris, beje, dešimtmečiais pirmauja tarp tų, apie kuriuos žmonės dažniausiai meluoja, kad juos žiūrėjo. Įdomu, ar matė „Krikštatėvį“ A.Užkalnis, jei jis jį priešpastato lėtoms, prislopintoms, nepaslankioms „Septyniolikoms akimirkoms“? Juk Frensiso Fordo Kopolos filmo ritmas panašus į Tatjanos Lioznovos.

Į Lietuvos „kino kritiko“ kūrybą būtų galima nusispjaut ir užmiršt. Kaip ir į dviejų išprotėjusių šaulių, pasakojusių , kaip naikinti Lietuvoje „penktąją koloną“. Negi Lietuva stokoja išprotėjusių ir idiotų?! Tačiau problema slypi ne juose.

„Vienalytė homoerotinė kompanija, kurioje veikėjas metų metais beviltiškai bando nusiprausti, įtikinamai parodo jo visišką nesugebėjimą turėti gilius ir ilgalaikius heteroseksualius santykius. Paprasčiau sakant, moteris Ženiai — didelio pavojaus šaltinis. Tačiau motina reikalauja vestuvių, pritarė kandidatūrai, viską paruošė šventiniam suėjimui, — dar viena lietuviško Delfi recenzija tarybinei kino klasikai, šį kartą „Likimo ironijai“. — ...Štai čia itin rusiškas tipas: mamytės sūnelis“.

Panašūs straipsniai Lietuvos žiniasklaidos priemonėse pasirodo pastoviai, kaip nauja naujametinė tradicija. « Likimo ironija - Naujuosius vėl sutiksime su ja? », — dar vieno Delfi.lt straipsnio pavadinimas. « Kodėl Rusija vis labiau myli Lietuvą? », — pavadinimas trejų metų senumo straipsnio, kurio autorius Dovydas Pancerovas pastoviai reiškiasi stambiausiame šalies laikraštyje „Lietuvos rytas“ ir antrame pagal populiarumą tinklalapyje 15min.lt, kuriame jis ragino saugotis rusų matrioškų, nevykti Rusijon į konferencijas ir būti atsargiems su išeiviais iš Rusijos. Dabar Pancerovas prisipažino daugelį metų esąs Lietuvos valstybės saugumo departamento agentas, t.y. pats patvirtino, kad visą šią neapykantą seniai kursto Lietuvos valdžia.

Snobų bandymai priešpastatyti save, „tikruosius europiečius“, „nepraustai Rusijai“ jiems atsigręžia dvasine katastrofa. Klykdami apie „europietišką pasirinkimą“ jie atsiduria fraką ant nuogo kūno vilkinčio valkatos vaidmenyje. Jie, to nesuvokdami, demonstruoja savo provincialumą ir neraštingumą, tuo įrodydami, kad, atsisakę ryšių su tarybine kultūra nė kiek nepriartėjo prie europietiškos.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```
