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

### Article 1 — id: `scraped:rubaltic_lt:a7ae6918fd9085f4`

**Title:** Grybauskaitė patvirtino gandus apie savo praeitį

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos prezidentė Dalia Grybauskaitė raštu atsisakė leisti publikuoti Rusijos archyvuose saugojamus jos personalius duomenis. Su tokiu prašymu į Grybauskaitę kreipėsi signataras Zigmas Vaišvila, daugelį metų kaltinantis prezidentę bendradarbiavimu su VSK ir reikalaujantis jos apkaltos. Atsisakydama publikuoti archyvų duomenis, kurie galėtų išsklaidyti tamsius gandus apie jos praeitį, Dalia Polikarpovna asmeniškai patvirtino, kad gandai turi pagrindo, o paviešinti archyvų dokumentai patvirtintų juos, o ne paneigtų.

Dalios Grybauskaitės biografija — tai griaučių virtinė archyvų spintose. Lietuvos prezidentės gyvenimas tarybiniais laikais — „tamsių dėmių“ rinkinys. „Tamsių dėmių“ tiesiogine prasme: žurnalistė Rūta Janutienė, ruošdama knygą „Raudonoji Dalia“, aptiko, kad iš Grybauskaitės asmens bylos išplėšti puslapiai nuo 6-ojo iki 17-ojo. Dalios Polikarpovnos santykiai su archyvų dokumentais labai sudėtingi ir supainioti. Archyvai galėtų pagaliau paaiškinti visus Lietuvos prezidentės biografijos ginčytinus momentus, nes tik ten galima gauti atsakymus į neeilinius Lietuvos konstitucinio teismo ir baudžiamosios įstatymų klausimus.

Kaip Grybauskaitė 1990 metais galėjo tapti TSKP Vilniaus mokyklos moksline sekretore, jeigu 1989 metais (jos žodžiais) pasitraukė iš Lietuvos Komunistų partijos (TSKP platformoje) ir įstojo į Brazausko vadovaujamą nepriklausomą Kompartiją? Kur jos ranka rašytas dokumentas, kad ji išstoja iš LKP (TSKP platformoje) ir įstoja į savarankišką LKP? Kuriais metais Grybauskaitė tikrai pasitraukė iš TSKP ir ar neatsitiko tai jau po 1991 metų sausio 13 d.? jei taip, ją būtina liustruoti ir taikyti baudžiamąjį persekiojimą.

Kaip 1991 metais Grybauskaitė, pasitraukusi iš aukštosios partinės mokyklos, galėjo patekti į JAV Džordžtauno universiteto stažuotes? Kas iš TSRS atstovų pasirašė siuntimą į tą stažuotę? Kodėl Lietuvos prezidentės tinklalapyje (skyrelis „Biografija“) siuntimo į JAV metai pakeisti iš 1991-ųjų į 1992-uosius?

Ir kas slypi už daugybės Grybauskaitės darbo VSK labui gandų, kuriuos savo memuaruose ir interviu patvirtina Dalią Polikarpovną 80-aisiais metais Vilniaus partinėje mokykloje pažinoję žmonės ? Jei šie gandai nemelagingi, tai vėlgi pagal Lietuvos įstatymus Grybauskaitei gręsia liustravimas ir baudžiamasis persekiojimas.

Archyvai galėtų atsakyti į šiuos klausimus, tačiau jie tyli.

Su prašymu leisti išslaptinti archyvus į ponią prezidentę kreipėsi Nepriklausomybės akto signataras Zigmas Vaišvila, daugelį metų studijuojantis Lietuvos valstybės vadovės „drumzliną“ praeitį. Anksčiau Vaišvila jau buvo inicijavęs Grybauskaitės apkaltą, aiškindamas, kad tokio žmogaus vadovavimas šaliai — moralinė gėda ir grėsmė Lietuvos saugumui.

„Viena — kada nuslepi biografiją, čia jau tiek to. Bet jei tu meluoji beveik visais klausimais, ko mes su tokiu vadovu pasieksime?“ — piktinosi Zigmas Vaišvila 2014 metais interviu RuBaltic.Ru. „Meluojama taip, kad kandidatės į prezidentus anketoje 2009 metais ji parašė nebuvusi Brazausko vadovaujamos ir nuo TSKP atsiskyrusios partijos narė, o šių metų anketoje parašė, jog buvo. Bet tai melas, ir tai rodo dokumentai, ir ji pati sau prieštarauja oficialiuose dviejuose dokumentuose. Dar gyvuoja daug Lietuvos Kompartijos narių, kurie organizavo šį atsiskyrimą ir kurie pasakė, kad tai melas,“ — tada sakė signataras.

Praeitais metais Vaišvila pasišovė ištirti Grybauskaitės dalyvavimą sudėtyje tarybinės diplomatinės delegacijos, apsilankiusios JAV 1991 metais. Ką šios delegacijos sudėtyje veikė būsimoji Lietuvos prezidentė, tuo metu oficialiai kuravusi Vilniaus partinės mokyklos mokslinę veiklą? Kas ją įtraukė į delegacijos sudėtį? Kokias pareigas ji ten ėjo?

„Aš buvau Lietuvos vicepremjeru 1991–1992 metais. Ir aš tiksliai žinau, kad Lietuva jos į Ameriką nesiuntė. Pirma, mes stokojome lėšų. Antra, Lietuvoje nebuvo JAV ambasados, galinčios išduoti jai vizą. Patekti į Ameriką ji galėjo tik su TSRS pagalba,“ — taip aiškina signataras savo suinteresuotumą šiuo Grybauskaitės biografijos epizodu.

Visus savo klausimus Zigmas Vaišvila oficialiai pateikė Rusijos užsienio reikalų ministerijai ir Rusijos ambasadai Lietuvoje. Rusijos ambasadorius Lietuvoje Aleksandr Udalcov atsiuntė signatarui oficialų atsakymą.

„Gerbiamas p. Vaišvila, su Jūsų 2015 m. kovo 23 d. kreipimaisi į RF užsienio reikalų ministeriją ir RD ambasadą Lietuvoje, prašant pateikti duomenis apie galimą ponios Dalios Grybauskaitės darbą TSRD ambasadoje JAV 1991 metais, įdėmiai susipažinta. Pagal 2006 m. liepos 27 d. 152 RF federalinio įstatymo „Dėl asmens duomenų“ 7 straipsnį operatoriai ir kiti prienantys prie personalių duomenų asmenys privalo neatskleisti tretiesiems asmenims ir neplatinti personalius duomenis be personalių duomenų subjekto sutikimo, jei Federalinis įstatymas nenumatytų kitaip... Tokiu būdu, ponios D.Grybauskaitės personalinius duomenis liečiančią informaciją gali pareikalauti tik pati ponia D.Grybauskaitė“.

Zigmas Vaišvila nepasimetė ir kreipėsi pas pačią D.Grybauskaitę prašydamas pasirašyti leidimą atskleisti jos asmeninę informaciją Rusijos archyvuose.

„Paaiškėjo, kad prezidentė į signataro laišką sausio 15 d. atsakė raštu ir informavo, kad tokį sutikimą kategoriškai atsisako duoti, — rašo Lietuvos portalas Ekspertai.ru . — Paprašius plačiau pakomentuoti atsisakymo priežastis, Prezidentūra paaiškino, kad jokių komentarų šiuo klausimu niekada nebus“.

Savo atsisakymu Dalia Grybauskaitė pasakė daug daugiau, negu ketino. Neigiamas rezultatas — taip pat rezultatas, neigiamas atsakymas — taip pat atsakymas. Jei ponia prezidentė būtų sutikusi paviešinti savo archyvinius duomenis, tai dar iki paviešinimo būtų pademonstravusi, kad ji stipri ir teisi, kad neturi ko slėpti ir kad jai nėra ko bijoti.

Tokiu būdu nenorinti paneigti gandų apie savo biografijos „tamsias dėmes“ „raudonoji Dalia“ plunksnos brūkštelėjimu įrodė, kad gandai skleidžia tiesą. Ir Lietuvos valstybinė propaganda susidūrė su rimta problema: kaip pateisinti prezidentės sprendimą.

Tikėtina, kad čia vėl išdygs „Rusijos specialiųjų tarnybų provokacijos“, kurios „pametės į archyvus savo klastotes“. Ir būtinai bus paminėti „rusų propaganda“ ir „hibridinis karas“.

Tačiau tai pernelyg primityvūs aiškinimai. O paneigti visus esą propagandinius gandus paprasta — parodykit dokumentus, kurie viską sudėliotų į savo vietas. „Galutinis popierėlis. Faktinis. Tikras. Šarvas!“ Tačiau Grybauskaitė ir pati to nedaro, ir kitiems neleidžia. Todėl Dalios Polikarpovnos praeitis ir dabartinė abejotina reputacija klostosi kaip sename tarybiniame anekdote. „Štirlicas ėjo koridoriumi ir negalėjo suprasti kreivų bendradarbių žvilgsnių. Štirlicas nežinojo, kad paskui jį driekėsi ilgas parašiuto šleifas“.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 2 — id: `scraped:rubaltic_lt:69f516c1dc6edaf6`

**Title:** Lietuvos žiniasklaida siūlo žudyti kitaminčius

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Vienoje didžiausių Lietuvos žiniasklaidos priemonių išspausdinta instrukcija apie „kolaborantų neutralizavimo“ Lietuvoje metodus. Šaulių sąjungos nariai siūlo susidorojimo su šalies „penktąja kolona“ metodus prasidėjus karo veiksmams: kitaminčius rekomenduojama gąsdinti, daužyti jų langus, deginti namus, naikinti turtą, persekioti artimuosius bei šeimos narius ir t.t. — galop, fiziškai sunaikinti. Atsižvelgiant į tai, kad šalies prezidentė Dalia Grybauskaitė kadaise pareiškė, kad Rusija Lietuvą užpuolė ir karas vyksta, tokia instrukcija reiškia, kad Lietuvos kitaminčiai jau dabar gali sulaukti iš vietinių „patriotų“ pusės represijų ir niokojimų.

„Ko gero, reiktų atskirti du esminius tikslus. Pirmas – kolaborantą įbauginti, priversti jį nevykdyti priešiškos veiklos. Antras – visiškai sunaikinti“, — pokalbio metu samprotauja Lietuvos šaulių sąjungos parengimo centro instruktorius dimisijos majoras Albertas Daugirdas ir snaiperis Šarūnas Jasiukevičius. Šį pokalbį paviešino antrasis pagal apimtis Lietuvos portalas 15min.lt.

Pagal instrukciją, pirmasis kovos su „penktąja kolona“ būdas — psichologinis spaudimas. „Paprasčiausiai įmesti laišką į pašto dėžutę. Adresuotą konkrečiam asmeniui su konkrečiais reikalavimais. Būtina nurodyti terminą iki kada turi nutraukti kenkėjišką veiklą. Parašyti, kokios sankcijos numatytos. Galima įspėti kelis kartus. Po pirmojo įspėjimo atlikti kokius nors veiksmus, kurie buvo išdėstyti pirmajame įspėjime“, — teigiama Lietuvos „patriotams“ skirtose rekomendacijose.

Jeigu laiškai su grąsinimais nepadėjo, būtina imtis pilnaverčių persekiojimų. O veiklą reikia plėsti: „Jei tai (grąsinantys laiškai — RuBaltic.Ru pastaba ) neefektyvu, tuomet galima imtis kitų veiksmų – padeginėjimo, langų daužymo, turto naikinimo“. Pasak Lietuvos šaulių sąjungos nuomonės, labai efektyvi priemonė — žeminantys užrašai. „Ant kolaboranto turto, automobilio, namo. Išjuokiantys, niekinantys užrašai. Dažniausiai tokius grasinimus bandoma nuslėpti, todėl pakartotinius geriau „įteikti“ viešai. Pavyzdžiui, kartu su plyta per darbovietės langą. Tuomet apie tai sužinos daugiau kolaboruojančių asmenų. Jie taip pat bus įbauginti. Be to, įvykdžius grasinimą, kitiems kolaborantams bus rimtas signalas“, — rekomenduoja Albertas Daugirdas ir Šarūnas Jasiukevičius.

„Kad ir kas sakytų, kad tai nemoralu, bet tai veiksminga“, — 15min.lt portale samprotauja Šaulių sąjungos aktyvistai. „Įbauginta žmona turės gerokai didesnį poveikį nei dešimt grasinamųjų laiškų. Paprastas pokalbis su žmona, paaiškinant, kad jei vyras nenutrauks veiklos, tuomet jūs ir jūsų vaikai nukentės. Galima raštelį įteikti vaikui, kad perduotų. Dažnai kolaborantai savo artimuosius stengiasi slėpti, kaip ir kovotojai. Labai efektyvu kolaborantui atsiųsti jo artimųjų nuotrauką. Geriau su kovotojais greta. Jam bus rimtas signalas, kad jo šeima nėra saugi. Galima gauti informaciją, kur išvežta šeima, ir ją surasti. Po pirmų mandagių perspėjimų, jei jis tokios kalbos nesupras, galima gerokai prikulti“, — sako Daugirdas ir Jasiukevičius.

Visa tai, jų manymu, — „lengvo moralinio poveikio formos“. Tokia lengva forma — ir fizinis „kolaboranto“ žmonos prievartavimas. „Kitas veiksmingas būdas yra viešoje vietoje pririšti prie gėdos stulpo su užrašu ant kaklo. Efektyviau nuogą. Arba nuogą išmesti iš automobilio viešoje vietoje. Irgi su užrašu po kaklu. Be abejo, reikia nepamiršti šių vaizdų nuotraukų išplatinti socialiniuose tinkluose. Ypač skausminga moraliai“.

15min.lt patalpinta instrukcija neva aprašo partizaninių veiksmų Lietuvos karinės okupacijos sąlygomis metodiką. Tačiau instrukcijos autoriai, vardindami „kolaborantų neutralizavimo“ priemones, nesuvokiamu būdu siūlo kovoti su pastaraisiais pasitelkiant valdžią (negi okupacinę?).

„Jei grasinimo veiksmai neduoda efekto, tuomet reikia pereiti prie griežtesnių argumentų – fizinių bausmių – laisvės atėmimo. Būtina parodyti, kad bus imtasi vis skaudesnių priemonių“, — tvirtina Šaulių sąjungos nariai, pabrėždami, kad prieš nelojalius gyventojus būtina inicijuoti „valymus, kratas ir areštus“. Tik kaip lietuviškieji „patriotai“ inicijuos kratas ir areštus: juk nusimato, kad jie bus ne kolaborantai, o kovotojai prieš kolaborantus?

Atsakymas akivaizdus.

Apeliavimas į karo laikmetį nieko neturi apgauti — per pastaruosius du su puse metų Lietuvos valdžia įtikino nemažą gyventojų dalį, kad jie jau gyvena karo stovio sąlygomis. Netrukus sukaks metai isteriškam Lietuvos prezidentės Dalios Grybauskaitės pareiškimui, kad Rusija Lietuvą jau užpuolė ir karas vyksta (!). Tokie pareiškimai Lietuvos vadovybei lojaliems ekspertams — tik garsi, vidaus vartotojui skirta politinė retorika. Tačiau tam „vidaus vartotojui“, nacional-konservatyviam lietuviškam elektoratui „raudonosios Dalios“ žodžiai — oficialus kursas ir veiklos vadovas.

O jei karas prieš Lietuvą jau vyksta, tai ir „vidaus priešai“, „okupantų pagalbininkai“ ir „penktoji kolona“ — ne propagandiniai šūkiai, o reali grėsmė.

Lietuvos šaulių sąjunga — ypatingas sukarintas Lietuvos karinių pajėgų dalinys, kurio paskirtis — formuoti gyventojų įgūdžius partizaninio karo sąlygomis. Formaliai — savanoriška visuomeninė organizacija, jungianti akylesnius ir besiruošiančius atremti karinę agresiją „patriotus“. Tačiau finansuoja šaulius valstybės biudžetas, ir todėl jie tampa gretavalstybine valdžią remiančia struktūra.

Tokia pat išvada peršasi ir apie „kolaborantų neutralizavimo“ pokalbį, patalpintą 15min.lt: viename pagrindinių Lietuvos žiniasklaidos portalų, remiančių valdžios pastangas, o formaliai esančių nepriklausomais. Kartu su Šaulių sąjunga skandalo centre atsidūrė ir 15min.lt: pastovus šio portalo autorius Dovydas Pancerovas su pasididžiavimu patvirtino daugybės gandų realybę, kad jis dirba Lietuvos spectarnybų labui.

Priminsime, kad Pancerovas išgarsėjo persekiodamas nepriklausomas žiniasklaidos priemones, kaltindamas jas „antivalstybine ir propagandine veikla“, puldamas Lietuvos mokslininkus už tai, kad jie vyksta į Rusijos mokslinius renginius (tai jis pateikė beveik kaip Tėvynės išdavystę), ragindamas atimti bėglio statutą iš opozicinio žurnalisto Anatolijaus Šarijaus ir išduoti jį kaip dovaną Ukrainos sąjungininkams. Dabar gi jis dar patvirtina, kad už jo veiklos 15min.lt stovi Valstybės saugumo departamentas.

ir tai vyksta ne Hitlerio Vokietijoje prieš „krištolo naktį“. Ir ne Sirijoje ar Irake, kuriuos kontroliuoja „Islamo valstybės“ (RF uždrausta teroristinė organizacija) banditai. Tai vyksta 2016 metais Europos šalyje. Taigi kol Lietuvoje nebus sukvailiota „krištolo nakties“ pavyzdžiu, visi perspėjimai dėl dabartinių visuomeninių-politinių santykių taip ir bus vadinami vien tik „rusiška propaganda“.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 3 — id: `scraped:rubaltic_lt:f1ef15fa399f59f6`

**Title:** Lietuvos energetinė strategija virto propaganda

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuva atsisakė pirkti JAV suskystintas gamtines dujas, nors praeitais metais politikai pastoviai tvirtino, kad Lietuva taps pirmuoji Europos šalis, įvežanti amerikiečių SGD. Lietuvos energetinė politika galutinai prasilenkė su realiu gyvenimu ir tapo propagandos įrankiu — visi Lietuvos energetiniai projektai vystosi pagal schemą: pirmiausia šalies lyderiai garsiai skelbia, kad jie eilinį kartą parodys Rusijai, kur „vėžiai žiemoja“, ir įgis „energetinę nepriklausomybę“, paskui šie pareiškimai susiduria su realybe ir „energetinės nepriklausomybės“ įgijimo projektai triukšmingai griūva.

Praeitų metų pradžioje Lietuva oficialiai pareiškė, kad bus viena iš pirmųjų JAV suskystintų dujų pirkėjų, kai amerikiečiai pradės jas eksportuoti į Europą. Lietuvos energetikos ministras Rokas Masiulis tai pareiškė Vašingtone susitikdamas su savo amerikiečių kolega Ernesto Mazisu.

„SGD eksporteriams mes siūlome dujas tiekti per Klaipėdos terminalą ne tik į Lietuvą, bet ir į Latviją, Estiją, o nuo 2019 metų — Lenkijos ir Ukrainos vartotojams“, — pareiškė Masiulis amerikiečiams, eilinį kartą energetinę temą susiedamas su geopolitinėmis ambicijomis: Lietuva siekia būti JAV ne atskira nedidelės valstybės rinka, o didelės regioninės rinkos dalimi — taip buvo pasakyta Energetikos ministerijos ataskaitoje.

Visus sekančius mėnesius Lietuvos vadovybė reiškė norus patekti istorijon kaip pirmoji Europos šalis, aprūpinsianti savo energetiką JAV skalūnų dujomis. Antai sausio 11 d. pasklido naujiena, kad pirmąją suskystintų gamtinių dujų partiją amerikiečiai pardavė iš eksporto terminalo Sabine Pass ir žingsniu priartėjo prie savo SGD pardavimo Europai ir, žinoma, Lietuvai.

Kaip matome, lietuviai amerikietiškos prekės ne tik atsisakė — dar ir įžeidė, pavadinę jų dujas nekokybiškomis. Netinka taip eilgtis su pagrindiniu strateginiu sąjungininku, užtikrinančių karinę Lietuvos saugumą ir leidžiančiu jos prezidentei bebaimiškai klykti apie „teroristinę valstybę“. Puikūs Vašingtono sąjungininkai: reikalauja, kad JAV didintų regione karinį dalyvavimą, o patys bodisi pirkti amerikietišką produkciją.

Po tokių išpuolių JAV elitas gali susimąstyti ir dar kartą perskaityti rezonansinį gruodžio straipsnį „Forbes“ apie tai, ar reikalingos JAV ir jų NATO sąjungininkams „neįgalios Pabaltijo tautos“.

Iš kitos pusės, galima suprasti ir Lietuvos vadovus: jie ištisus metus įtikinėjo elektoratą, kad per visą Atlantą iš Meksikos įlankos į Klaipėdą atvežamos dujos bus pigesnės, nei rusų bei suskystintos norvegų, kurios šiuo metu tiekiamos Lietuvos terminalui.

Bet kuriam mąstančiam žmogui buvo aišku, kad to negali būti. Tačiau Lietuvos politikai su džiaugsmo blizgesiu akyse vis tiek įtikinėjo, kad viskas taip ir bus. Todėl negali jie dabar sąžiningai pasakyti, kad suskystintų amerikiečių dujų nepirks todėl, kad pagaliau suvokė, kokia jų galima kaina.

Pagal tokią schemą vystosi visi Lietuvos energetiniai projektai: pirma pagarsinami politikų pareiškimai, kaip Lietuva parodys Rusijai, kur „vėžiai žiemoja“, ir įgis „energetinę nepriklausomybę“, o paskui rėksminga propaganda susiduria su rūsčia realybe ir tada eilinės „amžiaus statybos“ lieka tik popieriuje.

Taip nutiko ir su Visagino AE. Visi ekonomistai ir energetikai įtikinėjo Lietuvos vadovybę, kad dabartinėmis sąlygomis neįmanoma Lietuvoje pastatyti atominės elektrinės. Į tai ta vadovybė su fanatišku akių blizgesiu atsakydavo: mes ją pastatysime! Ir, žinoma, nepastatė.

Taip nutiko ir su skalūnų dujomis. Ištisus 2013 metus buvo triūbinama, kad Lietuva ne tik energetiškai nepriklausys nuo Rusijos, bet pati taps regionine energetine šalimi. Rezultatas: išaiškėjo, jog Lietuvos skalūnų ištekliai tokie maži, kad amerikiečių energetikai dingo iš šalies ir apie skalūnų dujų gavybą Lietuvoje kalbos baigėsi.

Praeitų metų kovo mėnesį energetikos ministras Rokas Masiulis pareiškė, kad derybos su „Gazpromu“ Lietuvai neitin svarbios — maža, tačiau išdidi respublika turi SGD terminalą, todėl dabar lai „Gazpromui“ rūpi rusiškų dujų tiekimo kontrakto pabaiga 2015 metų gruodžio mėn. O Lietuva su savo SGD terminalu gali visai tuo kontraktu nesirūpinti ir išvis atsisakyti rusiškų dujų. Praėjo keli mėnesiai. Ir tada Lietuvos premjeras Algirdas Butkevičius įpareigojo energetikos kompanijas pradėti su „Gazpromu“ naujas derybas.

Kai Klaipėdoje apsireiškė plaukiojantis SGD terminalas Independence, Lietuvos veikėjai išdidžiai pareiškė, kad nuosavo SGD terminalo projektas ypač naudingas Lietuvai ekonomine prasme, kad suskystintos norvegų dujos daug pigesnės rusiškų, o jų perteklių Lietuva perpardavinės Latvijai ir Estijai...

Praėjo keli mėnesiai. Oficialūs Lietuvos asmenys taip ir nepagarsino „labai pigių“ norvegų dujų kubinio metro kainos, Latvija su Estija pirkti „labai pigias“ dujas atsisakė todėl, kad jos labai brangios, o baigiantis metams Lietuvos vyriausybė nusižemindama kreipėsi į norvegus prašydama peržiūrėti kontraktą, nes pirkti dujas dabartiniais kiekiais ir dabartinėmis kainomis Lietuva nepajėgi.

Suskystintų dujų iš JAV pirkimo projektas vystėsi pagal tokį pat scenarijų. Pirma girdėjosi triukšmingi oficialūs pareiškimai, kad Lietuva pirmoji Europoje taps regionine lydere, kad amerikietiškomis dujomis aprūpins visus kaimynus... Vėliau propaganda vėl atsimušė į realybę, ir Lietuva grubiai atsisakė pirkti amerikiečių dujų.

Tokia Lietuvos energetinė politika būdinga visom šalim, kurių energetika atsidūrė ne ekonominėje, o politinėje plotmėje. Tokia, kaip Lietuvoje, absurdo energopolitika dabar būdinga Ukrainai, kuri vis ruošiasi statyti SGD terminalą Juodojoje jūroje, o kol kas atsisako pirkti rusiškas dujas (212 dolerių už 1000 m³), keisdamas jas į iš Europos sugrįžtančias, tik jau brangesnes. Svarbiausia, tos dujos, nors vis tiek rusiškos, patenka iš Europos, o už tokį „europietiško pasirinkimo“ džiaugsmą galima ir permokėti.

Anksčiau ar vėliau objektyvi ekonominė realybė viską sudėlios į savo vietas, ir kai kuriose šalyse egzistuojanti absurdo energetinė geopolitika užsidengs variniu dubeniu.

Žinoma, bus įdomu pažiūrėti, kaip tai įvyks Lietuvoje.

Tačiau Lietuvos valdžia tiek didžiavosi šiuo projektu ir namuose, ir užsienyje, kad atsisakyti jo nepajėgia — tai būtų baisus smūgis reputacijai. Bet ir naudotis šiuo projektu nepavyks ilgai — nuostolių suma pastoviai auga. Ir todėl tragikomedija dvelkianti istorija neišvengiamai ritasi prie atomazgos.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 4 — id: `scraped:rubaltic_lt:3a27c4a90eeaf48a`

**Title:** Pabaltijis išsikovojo karinio Rusijos priešo statusą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Rusijos prezidentas Vladimiras Putinas patvirtino RF nacionalinio saugumo strategiją. Naujoje Strategijos versijoje pagrindiniu potencialiu Rusijos priešu įvardinamas NATO, o pagrindine karinio saugumo grėsme — NATO karinės infrastruktūros priartėjimas prie Rusijos sienų. Siekiant pasipriešinti šiai grėsmei, Nacionalinio saugumo strategija numato prie Rusijos sienų su NATO išdėstyti aukštos technologijos daugiafunkcinius karinius kompleksus. Patvirtintas dokumentas juridiškai įtvirtina seną faktą: Pabaltijo militarizavimas, kurio aktyviai siekė vietiniai politikai, kilus kariniam konfliktui su NATO, paverčia šį regioną pirmojo Rusijos smūgio objektu.

2014–2015 m. NATO ir JAV karinis dalyvavimas Pabaltijo šalyse augo geometrine progresija. Dukart buvo padidinti Pabaltijo priešlėktuvinės gynybos pajėgumai — aeroparkas Šiauliuose papildytas 16 NATO raketiniais naikintuvais. Į Latviją iš JAV atgabenta 150 kovinės technikos vienetų, tame tarpe tankai „Abrams“ ir šarvuočiai „Bredli“. Visose Baltijos šalyse išdėstyti amerikiečių specialiosios paskirties daliniai, turėsiantys atlikti karinius ir prieškarinius veiksmus. Buvo skelbiami elektroninės žvalgybos sistemos išdėstymo netoli Rusijos sienos planai, atidaromi NATO „kibersaugumo“ centrai, kuriems buvo pavesta vesti informacinius karus rusakalbėje media erdvėje.

Panašiai skubos tvarka buvo vykdoma NATO karinio dalyvavimo plėtra Rytų Europos šalyse: Lenkijoje, Rumunijoje, Bulgarijoje ir t.t. Tačiau Rumunija arba Bulgarija neturi su Rusija bendros sienos, o štai Rusijos su Pabaltijo šalimis siena gana ilga. Todėl būtent Pabaltijo militarizavimas buvo Maskvoje įvertintas kaip pagrindinė praktinė karinės NATO infrastruktūros plėtros Rytų Europoje grėsmė.

Lietuvai, Latvijai ir Estijai tokia situacija reiškia, kad šioms šalims bus visiškai vis tiek, kaip užsibaigs Rusijos karas su „Vakarų demokratine bendrija“. Sakykime, jei Rusija šio karo metu bus pažeminta ir nugalėta, net „civilizuoto pasaulio“ jėgomis nušluota nuo žemės paviršiaus, — Pabaltijo politikai vis tiek nieko nepamatys, nes jų šalys bus pirmosios nušluotos nuo žemės paviršiaus.

Ši išvada priimtina bet kuriam protaujančiam žmogui — tam nebūtinas karinio analitiko ar eksperto mąstymas. Ir sveiku protu mąstantys žmonės visais skubos tvarka Pabaltijos militarizavimo metais nurodinėjo vietiniams vadovams, kad brukimas į regioną masinio naikinimo ginklų, jo pavertimas Rusijos ir Vakarų ginklavimosi epicentru ir konflikto tarp karinių-politinių blokų provokavimas ne tik negarantuoja Lietuvai, Latvijai ir Estijai saugumo, bet kenkia jam.

Garantuoti Pabaltijui saugumą gali tik visiškai priešinga politika: abipusis NATO Baltijos regiono ir Rusijos demilitarizavimas, Maskvos ir Vakarų šalių santykių įtampos mažinimas, Pabaltijo šalių pavertimas tarpininkėmis, kurios padėtų Maskvai ir Vakarų sąjungininkams integruotis Rusijai į tarptautinė Vakarų bendriją.

Tokia specializacija pasaulinėje praktikoje Kremlius Baltijos šalyse labai suinteresuotas, o tai šioms šalims taptų karinio saugumo garantija. Deja, pabaltijiečiai ėmė specializuotis pasaulio politikoje kaip smulkūs provokatoriai.

Pabaltijo diplomatija dės šiais metais visas pastangas stengdamasi įtikinti savo sąjungininkes NATO nutraukti 1997 metų Akto, draudžiančio išdėstyti pastovias NATO sausumos pajėgų bazes prie Rusijos sienų, galiojimą.

Paskutinio NATO samito Uelse metu Pabaltijo šalims nepavyko įtikinti savo europietiškų sąjungininkų, tad dabar jų viltys siejamos su NATO samitu Varšuvoje, kuris įvyks šių metų vasarą. Akivaizdu, kad, nerdamosi iš kailio, jos nori sunaikinti Europos saugumo architektūrą, nes beveik du dešimtmečius 1997 metų Aktas, kurį pasirašė Rusija ir NATO, garantavo Rytų Europos šalių saugumą. Dabar gi Pabaltijo šalys reikalauja, kad sąjungininkai demonstratyviai į jį spjautų ir jų teritorijose atsidurtų pastovios NATO bazės — ir tai nepaisant jokių su Rusija susitarimų.

Tokiu būdu jos provokuoja europietiško saugumo griūtį ir tiesioginį Rusijos konfliktą su NATO, nors priešpriešos arena tokiu atveju taptų Pabaltijo teritorija.

Paskutinę 2015 metų dieną Rusijos prezidentas Vladimiras Putinas patvirtino naują RF nacionalinio saugumo strategiją. Naujoje jo redakcijoje pagrindine grėsme Rusijos saugumui įvardinamas NATO: „NATO jėgos potencialo didinimas ir globalių paskirčių, kurios realizuojamos pažeidžiant tarptautinės teisės normas, jam suteikimas, bloko šalių karinių veiksmų aktyvinimas, tolimesnė jo plėtra ir karinės infrastruktūros prie Rusijos sienų artinimas kelia grėsmę nacionaliniam saugumui“.

Dokumente minimas ir Rytų Europos militarizavimas, kurį atlieka JAV: „Galimybė palaikyti globalinį ir regionalinį stabilumą sumenkinama išdėstant Europoje, Azijos-Ramiojo vandenyno regione ir Artimuosiuose Rytuose JAV priešraketinės gynybos komponentų, praktinio „globalinio smūgio“ koncepcijos realizavimo, strateginių nebranduolinių aukšto tikslumo, o taip pat kosmose ginklų išdėstymo sąlygomis“.

T.y. prie Lenkijos ir Pabaltijo šalių, kurias Rusija jau juridiškai pripažino pirmojo karinio smūgio objektais iškilus tiesioginiam konfliktui su NATO. Jos pačios, pasirinkusios savo diplomatijos kelyje provokacijų politiką, susikūrė tokią situaciją.

Pakanka prisiminti įvežimą į regioną ne gynybinės, o puolimui skirtos NATO ginkluotės („Abramsai“) — ir tai atsižvelgiant į įvykius Ukrainoje ir vertinant kaip būtinybę stiprinti savo saugumą. Arba NATO karinius mokymus Baltijoje, kai buvo iškelta užduotis okupuoti Kaliningrado sritį (tai taip pat liečia „gynybą nuo rusų agresijos“).

Įsidėmėtina, kad tokia provokacijų politika tęsiasi. Provokuoti konfliktą tarp Rusijos ir NATO — svarbiausias Pabaltijo diplomatijos uždavinys šiais metais. Ir baisu įsivaizduoti, kokią visagriaunančią pergalę patirs Lietuva, Latvija ir Estija, jei šis „svarbus“ uždavinys bus įgyvendintas.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 5 — id: `scraped:rubaltic_lt:0000a6beda4951f6`

**Title:** „Europą norima paversti Pabaltiju“

**Source:** rubaltic_lt (propaganda)

**Text:**

```
2015 metais krito naftos kainos, stiprėjo Eurozonos krizė, kelią skynėsi ambiciniai JAV prekybiniai projektai. Portalas RuBaltic.Ru aiškinosi su ekonomistu Michailu CHAZINU, ko 2016 metais galima tikėtis ekonomikos srityje.

– Michailai Leonidovičiau, ką galėtumėte pasakyti apie naftos kainas 2016 metais?

– Šiuo klausimu domisi milijardai žmonių pasaulyje, tik atsakymo niekas nežino. Jei vadovautis fundamentaliomis tendencijomis, naftos kaina turėtų pakilti iki 60 dolerių už barelį. Tačiau tiksliai pasakyti neįmanoma, nes tai priklauso nuo daugybės veiksnių.

– Nuo kokių dėsningumų visų pirma priklausys kainų svyravimai?

– Dėsningumai įvairiausi: ilgalaikiai ir trumpalaikiai, egzistuoja ir neekonominiai veiksniai — karų Artimiausiuose Rytuose mastai ir dolerio zonos irimo problema. Įvairiuose regionuose vyksta lokalizavimas, egzistuoja savi gavybos šaltiniai, taigi vidutinė naftos kaina gali nepasikeisti, nors įvairiuose regionuose ji gali būti labai skirtinga. Gali vaidmenį suvaidinti ir tai, kad pigios naftos kiekiai mažėja, o brangios — didėja. Dar egzistuoja politinis veiksnys — Europos Sąjungai draudžiama pirkti pigią naftą. Ir taip toliau. Situacija sunkiai prognozuojama.

– FRT pakėlė bazinį procentinį atlygį. Ekspertai, tarp kurių RF Taupomojo banko vadovas Germanas Grefas, teigia, kad FRT politika, priešingai, sutvirtins dolerį ir sumažins naftos kainas. Ar jūs pritariate tokiems vertinimams?

– Kas dėl amerikiečių veiksmų, tai FRT galimybės keliant atlygį ribotos, todėl manyti, kad jos įtakos naftos kainą, tiesiog nerimta.

– FRT pakėlė atlygį pirmąkart per devynerius metus. Kodėl tai įvyko?

– Išties amerikiečiai tai padarė, nes įvėlė klaidą. Jie sukėlė gyventojams jausmą, kad prasidėjus ekoniminiam augimui būtina kelti atlygį. Tačiau šis ryšys nėra būtinas, be to, ekonominis JAV augimas neprasidėjo. Kalbėti apie tai garsiai nevalia. Štai todėl JAV ir turėjo pakelti atlygį, nes priešingu atveju tai būtų buvę įvertinta, kad nėra jokio ekonominio augimo. Tada būtų prasidėjusios vartotojiško pasikliavimo, vėliau — paklausos problemos. Tokiu būdu akivaizdu: didžiules skolas susikaupę amerikiečiai negali ženkliai pakelti atlygio. Visa kita — bankai. Įtakoti naftos kainų jie negali.

– Amerikiečiai atsisako 40 metų trukusio naftos eksporto embargo. Ar tai įtakos naftos rinkos plėtrą, pigios naftos kiekio ūgtelėjimą?

– Tai gali pakeisti tik regioninį balansą. Padidinę eksportą, JAV turės padidinti ir importą. Globalia prasme naftos balanso tai nepakeis.

– O kaip kis dolerio kursas? Jūs paminėjote dolerio zonos problemas.

– Pažvelkite: neseniai JAV principingai pažeidė žaidimo taisykles, kurios galiojo 70 metų. Pirmoji taisyklė — jos leido Tarptautiniams valiutos fondui (TVF) suteikti skolininkui kreditą. Antra — jie pakėlė bankroto reitingą. Čia turime omeny Ukrainą. Akivaizdu, kad tokie veiksmai galimi tik tais atvejais, kai visi suvokia, jog nusistovėjusiai sistemai jau nėra ateities.

– Reikia suprasti, kad dėl Ukrainos įra Bretono–Vudo modelis?

– Dabar net nesvarbu, dėl ko. Precedento arba nėra, arba jis kuriamas.

– Ir dėl to ženkliai pasikeis TVF praktika?

– Pasikartosiu: TVF jau radikaliai pasiketiė, leidęs suteikti kreditą nemokiai šaliai. Sakyčiau, tai pasaulinio finansinio modelio katastrofa. Bretono–Vudo sistemos vadovai supranta, kad jis negyvybingas.

– Jei tas modelis diskredituotas, ar yra žaidėjų, ketinančių jį pakeisti arba reformuoti?

– Egzistuoja intelektuali struktūra — Atnaujintas Bretono–Vudo komitetas. Prieš keletą mėnesių jis išleido storą knygą, kurioje daugybė ekspertų svarstė, ar galima pakeisti situaciją. Galiu teigti, kad optimizmas nejaučiamas. Pagal pačius optimistiškiausius pareiškimus, gali būti, kad dar pavyks išsaugoti senąją sistemą. Tačiau žmonės supranta, kad esminiai pakeitimai ne už kalnų. Kartais jie tai stengiasi nuslėpti, ir juos galima suprasti — kai visą gyvenimą užsiiminėjai viena viekla, sunku pripažinti, kad ta veikla rieda pabaigon. Tuo labiau, kad naujovės neišvangiamos. Tačiau dabartiniai vadovai visiškai neįsivaizduoja, koks turėtų būti globalus ekonominis modelis.

– Dėl to nukentės tik atskiri regionai, ar ir JAV?

– JAV susilauks rimtų pasekmių, nes pasaulio finansų sistemą jos kontroliuoja per dolerį. Tačiau neaišku, kas joms bus blogiau — bandyti išlaikyti dabartinę padėtį ir tam naudoti visus išteklius, ar jos atsisakyti. Tai spręsti jie turi patys.

– Daug kalbų girdisi apie JAV Ramiojo vandenyno partnerystę. Pačioje šalyje šia tema vyksta karštos diskusijos. Kaip tai atsilieps regionui?

– Šis projektas kartu su Transatlantinės partnerystės projektu, pirmiausia, turi nutraukti tą bambagyslę, kuri jungia JAV su Kinija. Antra, amerikiečiai stengiasi apsieiti minimalia krizės apimtimi. Greičiausiai Transatlantinė partnerystė netaps tokia, kokios jie siekia. Ramiojo vandenyno partnerystė be Atlanto praranda prasmę. Ar pavyks ją realizuoti? Čia galimybių daugiau, tačiau vis tiek yra rimtų problemų.

– Kokias problemas Jūs matote?

– Pagrindinė problema — reikia siekti, kad JAV būtų tiekiama nekontroliuojama Kinijos pigi produkcija. Įkurti Pietryčių Azijoje galingus ir Kinijos nekontroliuojamus gamybinius pajėgumus gana sudėtinga. Tai greitai padaryti tikrai neįmanoma.

– Europoje pastoviai protestuojama dėl Transatlantinės prekybinės investicinės partnerystės. Ar šie protestai turi pagrindo?

– Dėl Europos viskas aišku. Europa taps Pabaltiju. Šio projekto Europos Sąjungai esmė — JAV su Vakarų Europa pasielgs taip, kaip Vakarų Europa pasielgė su Pabaltiju ir Moldova — visiškai likvidavo savą gamybą. Mechanizmai visiškai tie patys. Kreditai gamybai nebus skiriami. Europietiška produkcija neturės paklausos. Bus tikslingai palaikomas amerikietiškas eksportas. Dėl visiško tarifų panaikinimo Europoje, kurioje mokesčiai didesni, gamybos savikaina taip pat bus didesnė nei JAV.

– Jei bus taip blogai, kodėl europietiški lyderiai palaiko šį projektą?

– Jie politiškai priklausomi Vašingtonui. Jei kas nors bando prieštarauti, kaip Didžiosios Britanijos premjeras, žiniasklaida tuoj pat paskelbia, kad jis narkomanas, užsiiminėja netradiciniu seksu ir t.t.

– Ir vis dėlto: kodėl Europos šalių politikai griauna savą ekonomiką? O reputacija, reitingai?

– Graikijos krizė apnuogino ir užaštrino daugelį Europos Sąjungos problemų. Pažvelgus iš ekonominių pozicijų, kaip ši Sąjunga išsilaikė praėjusiais metais?

– Ekonomiškai Europos Sąjungos projektas visiškai žlugo. Europos Sąjunga galėjo egzistuoti tik stabilaus ekonominio augimo sąlygomis. Ekonominis augimas užsibaigė ir tapo akivaizdu, kad tolimesnis Europos Sąjungos egzistavimas neįmanomas. Vokietijos ir „trejetuko“ bandymai išgelbėti Graikiją lokaliai buvo sėkmingi. Sistemiškai jie situaciją tik pablogino.

– Į visą tai atsižvelgiant, kokia, Jūsų manymu, Europos Sąjungos ateitis?

– Priklausys nuo aplinkybių. Variantų daug: nuo esminio Europos Sąjungos sumažėjimo iki pagrindinių Vakarų Europos šalių iki visiško subyrėjimo.Europos Sąjungos projektas baigiasi, nes jis buvo sukurtas remiantis nesibaigiančio augimo logika. Nusimatė perteklinio produkto perskirstymo mechanizmai. O jeigu jūsų produktas ne perteklinis, o nepakankamas, byra visa sistema.

– Nuo 2000-jų metų pradžios, kai buvo įvedamas euras, euroskeptikai prognozavo Europos Sąjungos griūtį. Tačiau kol kas tai nenusimato.

– Tačiau turime ir atskirų ekonominio augimo pavyzdžių. Auga Lenkijos ekonomika, gerai laikosi Skandinavija.

– Lenkija ir Skandinavija — ne pavyzdys. Mažos šalys savo drausmės dėka gali demonstruoti augimą bendrojo nuosmukio sąlygomis. Pagrindinės šalys — Didžioji Britanija, Prancūzija, Vokietija, Italija. Ten nuosmukis. Žinoma, Vokietija ir Prancūzija stengiasi demonstruoti augimą, tačiau bet kuris raštingas ekonomistas nurodys klastotę. Nuosmukis tęsiasi ir stiprėja.

– Tokiu būdu šių šalių vadovybė apgaudinėja visuomenę? O gal tai objektyvūs apsirikimai?

– Kaip Jūs tai įsivaizduojate? Politikai pasakys: atleiskite, mes tiek metų jums melavome, iš tikrųjų pas mus ekonominis nuosmukis? Ne, jie ir toliau meluos. Tokia bendra situacija. Tai standartas. Nepatinka žodis „melas“, sakysime „optimistiškai pagražina“.

– Kinija taip pat pirmąkart per daugelį metų patyrė augimo nuopuolį. Kame sunkumai?

– Kame Kinijos ekonomikos esmė, įtariu, nežino net dauguma kinų, o gal ir niekas nežino. Bet Kinijos problema — antroji JAV problemų pusė. Ekonomiškai tai abi vienos monetos pusės, jos kris vienu metu. Čia matome vartojimo kiekių pelno augimui neatitikimą. Ir JAV, ir Kinijoje žmonės išleidžia ženkliai daugiau, nei realiai uždirba. Kinijoje tai įtakoje išoriniai pardavimai — jie gauna papildomą pelną, o JAV skatinami kreditų poreikiai.

– Čia ir pasireiškia Euroazijos ekonominė sąjunga. Ar gali ši Sąjunga įtakoti regiono ekonomiką?

– Ar šiuo metu egzistuoja valiutų diversifikavimas, siekiant likviduoti dolerio monopoliją?

– Teoriškai investicinio resurso nebuvimą galima kompensuoti perėjimu prie regioninių valiutų. Sakysime, reikia performuoti Europos Sąjungą, išmetant iš jos nereikalingas šalis: Pabaltijo ir Rytų Europos — palikti Vakarų Europą 1991 metų formate. Šiuo atveju euro dėka situaciją būtų galima pakreipti teigiama kryptimi, bet tai būtų labai sudėtinga reforma, nes norint ją įgyvendinti reikįtų keisti politinius elitus. Jeigu tokiose stambiose šalyse, kaip Didžioji Britanija, Prancūzija ir Vokietija, valdžion ateis tokie veikėjai kaip Marin Le Pen (prancūzų „Nacionalinio fronto“ lyderė), įgyvendinti tokius scenarijus bus realu. Valdant dabartiniam elitui nieko, išskyrus ekonominių nuosmukį ir laipsnišką Vakarų Europos pavertimą islamo regionu, mes nepamatysim.

– Apžvelgiant 2015 metus, kokie įvykiai, Jūsų nuomone, yra svarbiausi? Ir į ką reikia atkreipti dėmesį 2016-aisiais?

– Daug įvykių lydėjo praeitus metus. Reikšmingiausius minėjome — tai esminiai TVF Bretono-Vudo taisyklių pakeitimai, kai buvo leista kreditus skirti skolininkei Ukrainai, ir FRT atlygio pakėlimas. O trečias momentas, iš pirmo žvilgsnio, privatus: rugpjūčio mėnesį pirmąkart istorijoje siekiant užkirsti kelią biržės Niujorke griūčiai, rankiniu būdu buvo sustabdytos derytuvės, teigiant, jog sustreikavo kompiuteriai. Tai taip pat būdinga pasaulio ekonomikos būklei. Ir todėl patariu sekti Baltic Dry Index, įvykius Artimuosiuose Rytuose ir iš vis stebėti biržę, todėl kad bet kada galima sulaukti jos griūties.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 6 — id: `scraped:rubaltic_lt:75846a880e828a11`

**Title:** Amerikiečiai susimąstė dėl Pabaltijo šalių pašalinimo iš NATO

**Source:** rubaltic_lt (propaganda)

**Text:**

```
„ Forbes“ žurnalo puslapiuose viešai pripažinta, jog Pabaltijo šalių buvimas NATO yra beprasmis. Dėl šių šalių narystės NATO jau nukentėjo JAV saugumas: dėl jų veiklos NATO iškilo branduolinio karo su Rusija grėsmė, ir tai tuo metu, kai JAV šios šalys visiškai nereikalingos. Ką tokie pareiškimai reiškia Pabaltijo elitui? Tai priminimas, kad amerikietiškiems šeimininkams Lietuva, Latvija ir Estija — avarinis balastas, kurį JAV, esant reikalui, lengvai išmes už borto.

Viename ypač žinomame ir įtakingame amerikiečių finansų-ekonominiame žurnale „Forbes“ mėnesio pradžioje buvo išspausdintas „programinis“ analitinis straipsnis „Dėl ko Amerika įeina į NATO?“ , kuriame svarstoma, ar reikalingas Šiaurės Atlanto Aljansas, kuris ne tik negarantuoja JAV saugumo, bet kelia tam saugumui grėsmę.

Pagrindinė straipsnio mintis — įtraukiant į Aljansą naujus narius — neretai silpnas, netinkamas ir nepajėgias savigynai šalis, — NATO verčia amerikiečius glausti po savo sparneliu šiuos naujus apgailėtinus sąjungininkus. Tai Vašingtonui sukelia galvos skausmą, nes verčia jį veltis į visokius regioninius konfliktus dėl šalių, kurios neprideda JAV saugumo. Taigi šios šalys Amerikai visiškai nereikalingos.

NATO plėtra jau seniai tapo savitiksliu — praktikoje ji amerikiečiams yra beprasmė, kertasi su nacionaliniais JAV interesais, o perspektyvoje ir Pentagonui, ir Valstybės departamentui kelia problemas. „Įtraukti Juodkalniją — tai įgyti dar vieną Facebook beprasmį draugą“, — taip pradeda straipsnį etatinis „Forbes“ darbuotojas Dag Bendou.

„Prezidentai ir įstatymų kūrėjai tebesuteikia garantijas už amerikiečių pinigų ir gyvybių įkaitą kitoms šalims, ir tai daroma net ir tada (Juodkalnijos atvejis), kai jos visiškai nereikšmingos JAV saugumui“, — rašo „Forbes“. Dalykiškas leidinys negailestingai kritikuoja NATO gretų papildymo politiką, šaiposi iš „plėtros dėl plėtros“ principo, dėl kurio JAV privalo, pavyzdžiui, vykdyti sąjunginius įsipareigojimus su Turkija — JAV „drauge-prieše“, kurią valdo islamistas Erdoganas, aršiai kritikuojantis „pūvančius Vakarus“ ir „amerikietišką imperializmą“, tačiau skuodžiantis pas NATO sąjungininkus po paties išprovokuoto konflikto su Rusija.

„Plėtra Pabaltijo valstybių sąskaita yra didžiulė klaida, nes NATO narėmis tapo neįgalios tautos, ginti kurias nesuinteresuota likusi Europa, šalys, neturinčios Amerikai jokios geopolitinės reikšmės, tačiau įveltos į aštrią polemiką su Rusija, — rašo amerikiečių leidinys. — Jei atsitiks kas nors blogo, Briuselyje prieglobsčio ieškantys europietiški „sąjungininkai“ Ameriką palaikys tik minimaliai, ir ji ginčytinus klausimus, labiau rūpinčius branduolinį ginklą turinčiai Rusijai, turės spręsti su ja“.

Svarbu tai, kad „Forbes“ visiškai nepaminėjo „imperiškų ambicijų“ arba „agresyvios kaimynystės“ — Rusijos ir Pabaltijo konfliktas objektyviai egzistuoja, tačiau jo priežastimi nurodoma „aštri polemika“ tarp Maskvos ir Pabaltijo šalių. Kas šia polemika užsiima — klausimas retorinis, nes būtina pabrėžti, kad 2013 metais priimtoje Rusijos Federacijos užsienio politikos Koncepcijos nė žodžiu neužsimenama apie Pabaltijo šalių egzistavimą, juridiškai patvirtinta Maskvos diplomatijos politika Lietuvos, Latvijos ir Estijos atžvilgiu yra šios trijulės ignoravimas. Paniekinantis tylėjimas — tai universalus oficialus Rusijos atsakas į raginimus ją tarptautiniu mastu izoliuoti, lyginant su Trečiuoju reichu ir skleidžiant moterišką isteriją apie „teroristinę valstybę“. Tik po kelių mėnesių, be jokio įžvelgiamo ryšio su šiais viešaisiais išpuoliais, staiga buvo uždrausti latvių šprotai, embargas palietė pieno produktus, o Rusijos tranzitas buvo nukreipiamas iš Pabaltijo į Rusijos uostus.

O būtent to Pabaltijo sąjungininkai iš JAV ir reikalauja: nepraeina savaitės, o Vilniuje vėl išspjaunamas eilinis raginimas didinti regione JAV pajėgas. Pačios Pabaltijo šalys už save neatsako: jos mažos, tad už jų agresyvius plepalus turi atsakyti sąjungininkai. Ir iš vis sąjungininkai privalo didinti regione NATO pajėgas, išdėstyti šiose šalyse karines bazes, tokiais veiksmais konfliktuodami su Rusija.

Toks elgesys, tarp kitko, prieštarauja anglo-saksų ir amerikiečių kultūros pagrindams, kuriuos nuo mažens moko gyvenime pasikliauti tik savimi, ir gali sukelti tik pasibjaurėjimą. Toks pasibjaurėjimas įskaitomas „Forbes“ publikacijoje tarp eilučių, iš to pasibjaurėjimo išplaukia klausimas: ar reikalingi JAV ir sąjungininkams šios „neįgalios tautos“? „Galų gale, po Antrojo pasaulinio karo pabaigos praėjo 70 metų. Europos Sąjungos VBP ir gyventojų skaičius ženkliai didesni nei JAV ir Rusijos. Ar ne metas turtingiems Vašingtono draugams patiems apsiginti?“ — irzliai rašo amerikiečių žurnalas, pabrėždamas, kad dėl savo kinkas drebinančių sąjungininkų Baltieji rūmai „rizikuoja savo piliečių gyvybėmis, ir tai todėl, kad Europa nenori turėti pakankamą kiekį uniformuotų vyrų ir moterų“.

„Forbes“ straipsnis — ne šiaip sau straipsnis, todėl kad „Forbes“ ne šiaip sau biznio žurnalas. Tai vienas iš Wall street ruporų, tai pirmosios pasaulio ekonomikos „sienlaikraštis“, kurio balsu kalba JAV dalykinis ir politinis elitas. „Forbes“ pasakoja savo ne kiekiu, o kokybe brangiai auditorijai apie „gamybos pirmūnus“ (pačių pasaulio turtingiausių reitingas) ir apie superkorporacijos, kuri vadinasi JAV, darbo problemas.

Publikacija apie vargingus, nereikalingus ir JAV saugumui grėsmę keliančius sąjungininkus negalėjo žurnale atsirasti šiaip sau. Amerikiečių elitas suvokė situaciją su „neįgaliomis tautomis“ kaip problemą ir priėjo išvados, kad Lietuva, Latvija ir Estija nėra JAV jokia vertybė ir, esant reikalui, Vašingtonas Pabaltijį išduos.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 7 — id: `scraped:rubaltic_lt:560d0febbe7539f3`

**Title:** „Energetinę nepriklausomybę“ Lietuva bruka visai Europai

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos prezidentė Dalia Grybauskaitė dujotiekio „Šiaurės srautas – 2“ projektą pavadino grėsme energetiniam Europos saugumui, nes jis pratęsia ES šalių priklausomybę nuo Rusijos dujų. Tuo pat metu Lietuva inicijavo derybas su Statoil kompanija dėl Klaipėdos SGD terminalui tiekiamų dujų kiekio sumažinimo — norvegiškos dujos Lietuvai per brangios, be to, dabartinius kiekius nėra kur dėti. Būtent tokį energetinės „sėkmės“ modelį Lietuva dabar nori įpiršti visai Europai: atsisakyti pigių Rusijos dujų ir pirkti triskart brangesnes amerikiečių SGD.

Oficiali Lietuvos valdžia taip ir nepaviešino vieno kubinio metro norvegiškų dujų iš SGD terminalo kainos. Egzistuoja daugybė neoficialių skaičiavimų, pasikaptę kuriuose žingeidūs piliečiai nustato tikrą kainą: prie norvegų kompanijos Statoil tarptautinėje rinkoje esančios dujų vertės prideda dujų transportavimo iki Lietuvos bei redujofikavimo kainas bei mokestį už SGD terminalo nuomą... skaičiavimai rodo, kad galutinė „energiškai nepriklauso,ų dujų“ vertė svyruoja nuo 560 iki 570 dolerių už kubinį metrą. O tai 200 dolerių daugiau, nei dabar kainuoja Rusijos dujos, ir 120 dolerių viršija buvusią „Gazpromo“ kainą, dėl kurios buvo triukšmauta su SGD terminalu.

Oficialūs asmenys šių skaičiavimų nekomentuoja, 560-570 dolerių kainos nepatvirtina, bet ir savosios neįvardina. Pasak jų, reikėtų tikėti, kad norvegiškos dujos ne pigios, o labai pigios. Tokios pigios, kad šildymo išlaidos Vilniuje šį mėnesį ūgtelėjo iki 26%, o Klaipėdoje per pastaruosius tris mėnesius — 36%: komunalines tarnybas prievartos būdu verčia pirkti SGD terminalo dujas.

Spalio mėnesį „Vilniaus energija“ pirko iš terminalo 87,3% reikalingų dujų. Lapkričio mėnesį bus įsigyta apie 90%, gruodį — 67%. Tendencija akivaizdi: kuo daugiau tiekėjas perka SGD terminal dujų, tuo daugiau sostinės gyventojai moka už šilumą. „Kaina kis priklausomai nuo dujų kiekio terminale — tai labiausiai įtakoja tarifus. Kas mėnesį mes turime pirkti iš terminalo skirtingą dujų kiekį. Todėl šildymo kaina Vilniuje gruodžio ir sausio mėnesiais bus didesnė, o vasario mėnesį vėl sumažės“, — šią išvadą patvirtina „Vilniaus energijos“ prezidentas Linas Samuolis.

Tačiau vis tiek norvagiškos dujos labai pigios. Jos tokios pigios, kad Lietuvai trūksta pinigų joms pirkti. Šių metų liepos mėnesį Lietuvos premjeras Algirdas Butkevičius pareiškė, kad SGD terminalą valdanti kompanija „Klaipėdos nafta“ privalo mėnesio eigoje rasti šio objekto išlaikymo išlaidų sumažinimo variantus. Vėliau paaiškėjo, jog vienintelė išeitis, mažinant šias išlaidas, — keisti kontraktą su Statoil. Arba mažinti kubinio metro kainą, arba — tiekiamos produkcijos kiekį.

Pasirašydama kontraktą Lietuva įsipareigojo penkerius metus pirkti iš norvegų 540 milijonų kubinių metrų dujų. Pradėjus vykdyti kontraktą paaiškėjo, kad tokio dujų kiekio Lietuvai nereikia — Lietuvos ekonomika ir gyventojų skaičius tirpsta kaip pavasarį sniegas, energetinių galingumų poreikis mažėja, todėl kitais metais norvegiškų dujų perteklius Lietuvoje sudarys 280 milijonų kubinių metrų. Iš pradžių Lietuvos vadovybė planavo SGD terminalo perteklines dujas parduoti kaimynams, tačiau tokias „pigias“ dujas nepanoro pirkti nei Latvija, nei Estija. Štai ir tenka Lietuvai triskart brangiau pirkti dujas, kurias paskui nėra kur dėti. Na, tiesiog nors pasprink tomis suskystintomis dujomis!

Po to, kai Lietuva pasirašė su „Gazpromu“ naują, jai naudingą kontraktą, Statoil atstovai pareiškė, kad nesiruošia nieko keisti 2014 m. vasario mėn. pasirašytame kontrakte: lietuviai gaus dujas tomis kainomis ir tais kiekiais, kuriuos patvirtino savo parašais. Šioje situacijoje norvegai nenori suprasti Lietuvą valdančių vargšelių, nesugebančių suskaičiuoti, kiek jiems reikia dujų ir kokia jų kaina galėtų sudominti kaimynus. Tačiau padiskutuoti apie galimą kontrakto pakeitimą sutiko. Pirmieji derybų rezultatai gali būti paviešinti metų pabaigoje.

Taigi Lietuvos „energetinės nepriklausomybės“ epizodo baigties dar nesimato. Gal ji dar tik prasideda. Dabar ir nuo Norvegijos...

Ir štai Lietuvos prezidentė Dalia Grybauskaitė eilinį kartą kreipėsi į visą Europą, ketindama „apsaugoti“ ją nuo dujotiekio „Šiaurės srautas – 2“ statybos. Pasak Grybauskaitės, Nord Stream – 2 pažeidžia pagrindinius ES energetinės politikos principus, didina Europos šalių priklausomybę nuo Rusijos dujų ir gali nutraukti dujų transportavimą per Ukrainą. „Tai kelia grėsmę energetiniams saugumui ne tik Ukrainos, net ir visos Europos“, — prieina besąlygiškos išvados Dalia Polikarpovna.

Ir nieko šiuo atveju neturi suklaidinti kreipimasis į Ukrainą. Kova prieš alternatyvius Rusijos energetinių resursų tiekimo į Europą maršrutus ir išsaugojimą ukrainietiškos monopolijos Rusijos dujų tranzitui neturi ryšio su pačios Ukrainos rėmimu. Per penkiolika pastarųjų metų Ukraina pastoviai įrodinėjo nesanti patikima tranzito šalis. Ukrainos elitas vogė dujas iš tranzitinio vamzdžio, ką diplomatai vadino „nesankcionuotu paėmimu“, provokavo „dujų karus“, sugalvodavo vieną po kitos korupcinę dujų tranzito schemą, kraudamiesi sau turtus.

Pastarieji dveji metai šia prasme nieko nepakeitė: „europietiška“ Ukrainos valdžia tęsia dujines machinacijas ir provokuoja Europai naują energetinę krizę. Ir tai tuo metu, kai lyg ir bandžiusi tapti nepriklausoma valstybe Ukraina tapo visiška JAV satelitė. JAV vice prezidentas Baidenas, šiomis dienomis apsilankęs Ukrainoje, galėjo pareikalauti iš šios šalies vadovų, kad jie nekeltų Europos šalims grėsmės likti žiemą be dujų. Tačiau Baidenas, bent jau viešai, to nepadarė.

Ir visi tie, kas dabar Europos Sąjungoje kovoja su „Šiaurės srauto – 2“ projektu ir siekia, kad Ukrainos tranzitinė monopolija išliktų, nutyli, kad Ukraina yra visiškai nepatikima tranzitinė šalis, kad ji kasmet vogė Europai priklausančias dujas, kad tranzito sistema Ukrainoje taip ir nebuvo modernizuota ir atsidūrė avarinėje padėtyje, kad, visa tai susumuojant, alternatyvūs energetinių resursų tiekimo maršrutai vienodai svarbūs ir Rusijai, ir Europai.

Būtent todėl tos šalys, kurios sudaro amerikietiškos įtakos grupę, aktyviausiai kaunasi dėl Rusijos-Europos vieningos energetinės erdvės panaikinimo, visose ES šalyse terminalų statybos, priešinantis naujų Rusijos dujotiekių statybai. Jos ne dėl savęs iš kailio neriasi — jos dirba šeimininko naudai. Lietuva kur tik gali klykia apie savo terminalą kaip apie itin svarbų pasiekimą, kitais metais ji pirmoji ES pradės pirkti suskystintas amerikietiškas dujas, o Dalia Grybauskaitė „Šiaurės srautą – 2“ vadina „grėsme Europos energetiniam saugumui“. Tokiu būdu akivaizdu, kad Lietuvos prezidentė pataikūniškai siūlo visiems ES kolegoms lipti ant lietuviškų grėblių: atsisakyti pigių Rusijos dujų, pirkti brangias suskystintas ir meluoti sau ir aplinkiniams, kad tai visiems naudinga.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 8 — id: `scraped:rubaltic_lt:3d0ef38b8e6f2020`

**Title:** Putino kreipimasis: Rusija galutinai atsisakys Pabaltijo uostų

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Skelbdamas kreipimąsi Federaliniam Susirinkimui, Rusijos prezidentas Putinas paragino vystyti Baltijoje Rusijos uostus. Putino kreipimasis į Baltijos regioną reiškia, kad Kremliuje priimtas politinis sprendimas galutinai atsisakyti Pabaltijo jūrų uostų ir užbaigti Rusijos tranzito perorientavimą į Rusijos šiaurės vakarų uostus. Šis sprendimas jau nebus atšauktas: nei sankcijų panaikinimas, nei Lietuvos, Latvijos ir Estijos antirusiškos retorikos švelninimas šiuo klausimu nieko nepakeis.

„Mes tęsime transporto infrastruktūros modernizavimą, vystysime galingus logistikos centrus — Azovo-Juodosios jūros ir Murmansko transporto mazgus, šiuolaikiškus Baltijos ir Tolimųjų Rytų uostus,“ — pareiškė Rusijos prezidentas savo kreipimasi į Federalinį Susirinkimą.

Tokiu būdu V.Putinas aiškiai nubrėžė šalies transporto-logistikos vystymosi prioritetus, atsisakydamas paslaugų tranzitinių šalių — Ukrainos uostų Juodojoje jūroje, Baltijoje — Lietuvos, Latvijos ir Estijos.

Dėka tokios oficialiai paskelbtos valstybinės politikos išloš Novorosijskas, Tamanė ir kiti Juodosios jūros uostai; Vyborgas, Ust-Luga, Primorskas ir kiti Rusijos uostai Baltijoje. Pagrindiniai pralošę uostai: Odesa, Iljičevskas ir kiti Ukrainos uostai; Klaipėda, Ryga, Ventspilis, Talinas — t.y. jūrų prekybos uostai Lietuvoje, Latvijoje bei Estijoje.

Senų modernizavimas ir naujų jūrų krovininių uostų statyba Baltijoje tapo Rusijos valstybine politika nuo šio šimtmečio pradžios. Po nepriklausomybės atkūrimo, nepaisant ypatingai įtemptų santykių tarp Rusijos ir Pabaltijo šalių, visą dešimtmetį tvyrojo viltis, kad Lietuva, Latvija ir Estija nustos kvailioti, išsigydys nuo rusofobijos kaip augimo ligos, visiems gyventojams suteiks vienodas teises, o įstojusios į NATO ir ES nustos bijoti Rusijos ir įgis saugumo jausmą, — taigi taps adekvačios tarptautinių santykių dalyvės, nelauktai neiškrečiančios Rusijai kokios nors smulkmeniškos šunybės.

Tačiau visi šie lūkesčiai neišsipildė. Įstojusios į NATO, šios šalys ėmė raginti savo sąjungininkes peržiūrėti senas su Rusija sutartis, atsisakyti Maskvai duotų garantijų ir didinti Baltijos regione NATO pajėgas. Lietuvos prezidentė D.Grybauskaitė net pametėjo iniciatyvą panaudoti prieš Rusiją 5-tą NATO įstatų straipsnį. Pabaltijo šalių narystė ES paskatino Lietuvą, Latviją ir Estiją panaudoti Europos tribūną antirusiškiems pasisakymams, kišant pagalius į Rusijos/ES dialogo ratus: tai vetuoja bevizio režimo derybas, tai bando uždrausti „Šiaurės srautą“, „Pietų srautą“ ir kitus Rusijos-Europos energetinius projektus.

Dėl to ir Ukrainą bei Lenkiją lenkiantys dujotiekiai, o taip pat statyba naujų ir modernizavimas senų Rusijos prekybos uostų Baltijoje. Ir jeigu realizuojant bendrus su ES šalimis energetinius projektus „sanitarinės užkardos“ šalys dar galėjo pakenkti Eurokomisijos lygmenyje, tai dėl Ust-Lugos prekybos uosto statybos Pabaltijo šalims teko užsičiaupti. Taigi dabar prekių apyvarta rytinėje Baltijos pakrantėje sparčiausiai auga Rusijos uostuose Suomijos įlankoje — tai pasėkmė tikslingos valstybinės politikos perorientuojant tranzitą ir išvystant savą logistinę infrastruktūrą.

Šiais metais paskelbta apie uosto Ust-Lugoje statybos pabaigą. Praeitais metais prekių apyvarta Ust-Lugoje siekė 75,6 milijono tonų — didžiausias rodiklis Baltijos regione. Tačiau statant uostą buvo pareikšta, kad per metus bus perkraunama iki 170-180 mln. tonų. Iš kur ateityje atsiras trūkstantys 100 milijonų? Atsakymas akivaizdus: atsižvelgiant į valstybinę savosios logistinės šakos vystymąsi ir įveikiant priklausomybę nuo tranzitą vykdančių šalių — peradresuojant transporto srautus iš Pabaltijo į Leningrado sritį.

Šią Rusijos valstybinę politiką Baltijos šalys jau pajuto. Prekių apyvarta arčiausiai Sankt-Peterburgo ir Leningrado srities uostų esančio Talino uosto per šių metų 9 mėnesius sumažėjo 21%. Prekių apyvarta Ventspilio uoste per šių metų pirmąjį pusmetį sumažėjo beveik 15%. Tuomet, statant naują naftos užpylimo terminalą Leningrado srities Primorso uoste, buvo tiesiogiai nurodoma, kad šis terminalas atsiras kaip alternatyva Ventspiliui.

Naftotiekis, Mažeikių naftos perdirbimo gamykla ir Ventspilio bei Klaipėdos naftos užpylimo terminalai buvo statomi Latvijos ir Lietuvos TSR kaip bendros infrastruktūros dalis transportuojant į Europą tarybinę naftą.

Taigi Kremlius savo politika faktiškai atlieka Pabaltijo politikų darbą — išlaisvina juos nuo „materialių okupacijos pasekmių“. Jeigu Lietuvos, Latvijos ir Estijos jūrų uostai ir geležinkeliai būtų nacionalinė nuosavybė ir bendras palikimas, būtų galima kalbėti apie priešišką Pabaltijui Rusijos politiką ir skaičiuoti nuostolius, kuriuos patirs Pabaltijo šalys dėl Rusijos tranzito „nacionalizavimo“. Pavyzdžiui, Latvijos tranzitas siekia 12-13% BVP, o 80% tranzito tenka Rytų kroviniams. Šią vasarą Latvijos susisiekimo ministerija paskaičiavo, kad, prarasdamas Rusijos tranzitą, šios šalies biudžetas neteks 1,6 milijardo eurų.

Tačiau tokie skaičiavimai būtų įdomūs tuo atveju, jei tranzitas Pabaltijo vyriausybėms turėtų politinės vertės. Praktikoje jis — ir „okupacijos palikimas“, ir grėsmė saugumui. Dabar gi Rusijos krovinių srautą aptarnaujantys uostai ir geležinkeliai gimdo tose šalyse „penktą ekonominę koloną“ — nemažas grupes žmonių, kurie kritiškai suinteresuoti turėti gerus savo šalių su Rusija santykius. Pragmatiškus, konstruktyvius, abiem pusėm naudingus.

Pastarųjų metų tendencija: valdžios atstovai, suinteresuoti tranzito vystymusi, ar tai geležinkelis (iki šių metų vasaros „Latvijos geležinkelio“ valdybos pirmininkas Ugis Magonis), ar tai jūrų uostas (iki šiol Talino meras Edgar Savisaar), tapo baudžiamojo persekiojimo objektais. Esant tokioms sąlygoms Rusijos vadovybė negalėjo priimti kito sprendimo — tik visiškai atsisakyti tranzito per Pabaltijo šalis.

Pabaltijo tranzitas nereikalingas nei Rusijai, nei Pabaltijo vadovybėms. Rusija finansų atžvilgiu išloš daug daugiau, jeigu savo prekes eksportuos per savo uostus. Kokiu pagrindu Rusijos vadovybė galėtų leisti savo transporto darbuotojams padėti uždirbti Lietuvai, Latvijai, Estijai? Tik vieninteliu: jeigu Rusija galėtų palaikyti kaimyniškus santykius su draugiškomis šalimis. Bet ko Pabaltijo šalyse niekada per pastaruosius dvidešimt penkerius metus nebuvo, tai kaimyniškų santykių su Rusija ir su jai draugiškomis šalimis.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 9 — id: `scraped:rubaltic_lt:12e25b6206c1d384`

**Title:** Pabaltijis moko protauti Ukrainą, kuri paskelbė karą komunizmui

**Source:** rubaltic_lt (propaganda)

**Text:**

```
„ Bolševizmo šmėkla“ neleidžia naujai Ukrainos valdžiai užsiimti šalies vystymusi. Oficialus Kijevas, apsiginklavęs Pabaltijo vystymosi modeliu, reikalauja dekomunizavimo proceso tąsos. Pagrindine naujos Ukrainos valdžios mokytoja kovoje su tarybine praeitimi greičiausiai taps Lietuva, atsisakiusi dalyvauti antiteroristinėje koalicijoje, bet vėl pradėjusi kovą antikomunistiniame fronte.

Ukrainos prezidentas Piotr Porošenką pareikalavo visiško ir besąlygiško Ukrainos dekomunizavimo ir tęsti VSK archyvų paviešinimą. Tai valstybės vadovas pareiškė minint bado aukas Tautiniame muziejuje „Bado aukų Ukrainoje atminties memorialas“. Komunistų partijos vaidmuo šalies istorijoje „baisus ir nusikalstamas,“ pabrėžė prezidentas.

Dar pavasarį Ukrainos parlamentas priėmė dekomunizavimo įstatymų paketą. Dokumentai draudė tarybinės simbolikos naudojimą, smerkė komunistinį režimą, o USA karius vadino kovotojais už nepriklausomybę. Buvo nutarta išslapstinti VSK archyvus.

Lapkričio mėnesį Ukrainoje prasidėjo naujas kryžiaus žygis kovoje su tarybine praeitimi. Aukščiausioji Rada įgavo teisę savarankiškai keisti miestų ir gatvių pavadinimus. Parlamentas „žingsnis po žingsnio naikins totalitarinę praeitį. Lai niekas negalvoja, kad sugebės sustabdyti Ukrainos dekomunizavimo procesą“, — tokį eilinio etapo kovos su komunizmo šmėkla anonsą pateikė Aukščiausiosios Rados pirmininko pavaduotojas Andrej Parubij.

Kariaudama su tarybiniu palikimu naujoji demokratinė Ukrainos elita ėmė žengti „Pabaltijo mokytojų“ keliu.

Pabaltijo respublikos, sugebėjusios sukurti legendą apie sėkmingą tarybinės praeities transformavimą, tapo Ukrainai savotiškomis „demokratijos mokytojomis“. Penktadienį Latvijos sostinę paliko gausi Ukrainos valdininkų delegacija, kuri iš vietinių politikos funkcionierių perėmė „valdymo bei ekonominio vystymosi reformomų vykdymo“ patirtį. Latvijos deputatai ir vyriausybės nariai vien tik 2015 metais Kijeve lankėsi daugiau kaip dešimt kartų — jie skaitė „paskaitas“ ir mokė „kolegas“ „efektyviai diegti demokratinius pertvarkymus“.

Kadaise Talino, Vilniaus ir Rygos politikai, galėję pasiekti VSK archymus, visokeriopais būdais bandė naikinti savo ir gauti konkurentus kompromituojančias bylas. Kas nespėjo pasidarbuoti prie savų bylų, pelnė profesijos ir pareigų draudimą. Valdžios ešelonų valymas nedavė reikiamo rezultato ir Ukrainoje. „Per tuos dvejus metus iš liustravimo išėjo šnipštas. Regionalai, tame tarpe nekenčiami, vėl įlindo į parlamentą, į vietines tarybas, į merų pareigas ir t.t.“, — pareiškė greta frakcijų besistumdantis deputatas Andrej Iljenka. Tačiau nepaisant pirmojo etapo nesėkmių, „demokratična vlada“ nutarė tęsti savo žygį „Pabaltijo keliu“.

Iki šiol Aukščiausioje Radoje nesibaigia svarstymai dėl įstatymo „Apie Ukrainos pilietybę“ pakeitimo. Birželyje Radikaliosios partijos lyderis Oleg Liaško užregistravo įstatymo projektą, pagal kurį pilietybė būtų atimama iš visų „rusiško pasaulio“ šalininkų. Anksčiau Ukrainos pilietybės atėmimo įstatymą, kuris turėjo būti taikomas Donbaso gyventojams, ruošė buvęs bataliono vadas, o šiuo metu — Aukščiausiosios Rados deputatas Semion Semenčenka, o žinomas politologas Jurij Romanenka atvirai ragino kopijuoti Pabaltijo masinio pilietybės nesuteikimo institutą „vatnikų elektorato problemos sprendimui“ Ukrainoje.

Liaudies deputatai aktyviai siūlė ir kitus galimus įstatymo variantus, kurie keltų rimtus keblumus gaunant ukrainietišką pasą. Parlamentara ne kartą reiškė norą tikrinti pretendentų gauti Ukrainos pilietybę lojalumą valdžiai ir politines pažiūras.

Tačiau pats Ukrainos valdžios noras atimti pilietybę dėl „neteisingų“ politinių pažiūrų kartoja Pabaltijo šalių kelią 90-ųjų metų pradžioje, kai Latvijos ir Estijos gyventojai buvo suskirstyti į pilnateisius ir nepilnateisius, piliečius ir nepiliečius.

Vertėtų prisiminti ir iškart po maidano pergalės panaikintą įstatymą „Dėl valstybinės kalbos politikos“. Ukrainoje, nepaisant tautinio mišrumo, buvo atgaivintas 10 Konstitucijos straipsnis dėl vienos valstybinės kalbos, kopijuojantis politinę Pabaltijo praktiką.

Galima tikėtis, kad ir tolimesnis dekomunizavimo procesas taps toks pat absurdiškas ir sudarkytas, kokį sukūrė Latvija, Estija ir Lietuva. Atsižvelgiant į tai, kad tarp Pabaltijo sesučių Ukrainos pertvarkymais aktyviausiai užsiiminėja būtent Lietuvos politikai (Abromavičius, Kubilius, Audickas, Udrėnas, Šemeta ir t.t.), kova su „komunizmo šmėkla“ Ukrainoje, greičiausiai, tęsis pagal lietuvišką pavyzdį.

Kovodamas su tarybine praeitimi oficialusis Vilnius nuo tradicinio paminklų vertimo nuėjo iki susirėmimo su žaislais — raudonamiečių figūrėlėmis, ant kurių buvo įžvelgti tarybinės simbolikos elementai. „Komunizmo šmėkla“ išgąsdino ne tik valdžią: nemažai eilinių lietuvių taip pat panoro tapti antikomunistinio revanšo dalyviais. Taip, pavyzdžiui, patyrę patriotiškai nusiteikusių visuomenės atstovų spaudimą populiarių „Tarybinių“ dešrelių gamintojai buvo priversti pakeisti savo produkcijos pavadinimą: „dekomunizuotas“ dešreles jie suskubo perkrikštyti.

Ateityje Ukrainos dekomunuzacijos, greičiausiai, laukia tas pats farsas, kuris vyko Pabaltijo respublikose. Tačiau, galbūt, kai susirėmimas su tarybine praeitimi virs kova su žaisliukais-kareivėliais ir dešrelėmis, Ukrainos visuomenė paaiškins savo politikams, kad „Pabaltijo kelias“ link Europos nėra pats tinkamiausias.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 10 — id: `scraped:rubaltic_lt:c1510b4e05522074`

**Title:** Šalys mirtininkės — Pabaltijo šalys ir Ukraina — atiduoda save „Islamo valstybės“ (IV) žiniai

**Source:** rubaltic_lt (propaganda)

**Text:**

```
„ Islamo valstybė“ (Rusijoje uždrausta teroristinė organizacija) paskelbė sąrašą 60 šalių, kurioms skelbia karą. Į tą sąrašą tarp kitų pateko ir Lenkija, Ukraina, Moldavija, Lietuva ir Estija. Ir tai tuo metu, kai Pabaltijo šalys paskelbė demaršą, oficialiai atsisakydamos prisijungti prie tos antiteroristinės koalicijos, į kurią įeina Rusija.Neseniai buvo paviešinta, kad Ukraina pardavinėjo „Islamo valstybei“ ginklus. Pabaltijo šalys ir Ukraina elgiasi lyg šalys šachidės: besistengdamos pakenkti Rusijai, jos veikia labui tų banditų, kurie mielu noru perpjautų joms gerkles.

„Tai jūsų nelabųjų koalicija. Su Iranu, Turkija bei Rusija, kurios jungiasi kovai prieš tiesą“, — kalbama vaizdajuostėje, kurią neseniai sukūrė „Islamo valstybės“ smogikai, išvardinę 60 šalių, esą prisijungusių prie Vakarų antiteroristinės koalicijos ir todėl tapusių mirtinais IV priešais. Šių šalių karius „pasieks karo liepsna ir sudegins mirties kalnuose“, — žada „Islamo valstybės“ smogikai.

Beje, šis įrašas buvo skubiai pašalintas iš Youtube bei kitų pagrindinių video šaltinių, tačiau vis tiek spėjo plačiai pasklisti po mediapasaulį. Tarp kitų, į sąrašą šalių, kurioms buvo paskelbtas „šventas džichadas“, pateko Lenkija, Ukraina, Suomija, Estija ir Lietuva.

„Mes turime suprasti, ką kiekvienam iš mūsų reiškia Rusijos agresija lyg tai ir tolimoje Sirijoje ir kiek šie visiškai neatsakingi žingsniai priartino mus prie trečiojo pasaulinio karo“, — pareiškė Ukrainos prezidentas P.Porošenką iškart po Rusijos karinės operacijos pradžios prieš IV. „Kviečiu visus, turinčius informacijos apie Rusijos piliečius, dalyvaujančius nepaskelbtame kare prieš Sirijos piliečius, pateikti ją tinklalapyje „Taikdarys“, kuriame bus sukurtas atskiras skyrelis „Putino nusikaltimai Sirijoje ir Artimuosiuose Rytuose“, — tada pasiūlė Ukrainos VR ministro padėjėjas ir Rados deputatas A.Geraščenka, pasiūlęs perduoti islamistams Rusijos kariškių duomenis, kad šie „paskui galėtų juos surasti ir atkeršyti pagal Šariato reikalavimus“.

Ir štai praeitą savaitę — skandalas dėl Ukrainos prekybos su „Islamo valstybe“ ginklais. Associated Press agentūra pranešė, kad lapkričio 19 d. Kuveite buvo sulaikytas Libano pilietis Usama Muchamedas Chaijatas, kuris buvo atsakingas už IV teroristų ginkluotę. Chaijatas prisipažino dalyvavęs sandėriuose ir ginklų priėmime iš Ukrainos pardavėjų. Jis pateikė schemą, pagal kurią šaudmenys keliavo pas Sirijos smogikus. „Usama Muchamedas Chaijatas prisipažino vykdęs sandėrius perkant Ukrainoje ginklus ir persiunčiant juos į Siriją per Turkijos teritoriją“, — teigiama Associated Press pranešime, remiantis Kuveito VRM pareiškimu.

Būtent Ukrainoje buvo perkami kiniški pernešamieji zenitiniai raketų kompleksai FN-6, skirti kariniams lėktuvams ir sraigtasparniams numušti. Ir kodėl „Islamo valstybės“ smogikams prireikė PZRK? Atsakymas akivaizdus: kad numuštų antiteroristinės koalicijos, bombarduojančios IV pozicijas, lėktuvus. Negi Ukrainos veikėjai nesuprato, kokiais tikslais visa tai parduodama smogikų pirkėjams? Suprato, tikėdamiesi, kad IV pradės numušinėti būtent Rusijos lėktuvus.

Be plačios antiteroristinės koalicijos, kurią dabar formuoja JAV ir pagrindinės Europos Sąjungos šalys, Rusija ir Iranas, Sirijos krizėje veikia dar ir slapta teroristinė koalicija, tiesiogiai ar netiesiogiai palaikanti IV. Teikdama teroristams PZRK ir garsėdama savo oficialių asmenų pareiškimais Ukraina įrodė, kad ji yra teroristinės koalicijos dalyvė ir kelia pavojų visam pasauliui — juk ukrainietiški pernešamieji zenitiniai raketų kompleksai gali numušti ne tik Rusijos, bet ir, pavyzdžiui, amerikiečių naikintuvus.

Akivaizdu, kad slaptosios teroristinės koalicijos dalyvė yra Turkija, formuojanti terorizmo ekonomiką, perkanti iš IV naftą, teikianti smogikams humanitarinę pagalbą, gydanti juos savo pasienio karo ligoninėse. Numušdama Rusijos bombonešį Turkija galutinai įrodė esanti antiteroristinėje koalicijoje dviguba agentė.

Pagrindinė strateginė priežastis, dėl ko Turkija numušė Su-24, — noras pakenkti Rusijai, Iranui ir Vakarams solidarizuotis kovoje su „Islamo valstybe“, o Turkija – NATO narė, todėl turi teisę reikalauti, kad, iškilus konfliktui su Rusija, sąjungininkai ją apgintų. Ir nenuostabu, kad bjaurią provokaciją įvykdę turkai nuskuodė paramos pas NATO, lyg tai Rusija būtų numušusi turkų lėktuvą, o ne Turkija Rusijos. Turkijai labai reikia, kad Turkijos-Rusijos konfliktas taptų naujos Rusijos ir Vakarų priešpriešos pradžia.

O to reikia ne tik Turkijai. NATO sudėtyje yra visa grupė šalių, kurios siekia provokuoti konfliktus tarp Rusijos ir Vakarų. Į šią grupę įeina ir Pabaltijo šalys, pareiškusios atsisakančios dalyvauti kartu su Rusija bet kurioje antiteroristinėje koalicijoje. Tą pačią savaitę Latvijos užsienio reikalų ministras Edgar Rinkevič pareiškė, kad jo šalis solidarizuojasi su Turkija, o NATO šalys privalo ją paremti. Na, o numušti Rusijos lėktuvą turkai esą turėjo pagrindo.

Tos šalys, kurios tiesiogiai ar netiesiogiai palaiko ekstremistus, siekiančius neleisti susivienyti kovojančioms prieš juos jėgoms, — tampa mirtininkėmis, šachidėmis, norinčiomis susprogdinti Rusija ir pasiruošusiomis pačioms žūti. Jos parduoda „Islamo valstybei“ ginklus, demonstratyviai atsisako dalyvauti antiteroristinėje koalicijoje ir tokiu būdu faktiškai pasaulyje tampa sąjungininkėmis tų žmonių, kurie atvirai skelbia jas galabiusią. O gal jos mano, kad IV už jų diplomatines paslaugas pasigailės ir nepasiųs savo galvažudžių žudyti Vilniaus arba Talino gyventojų? Veltui: religinis ekstremizmas visada veikia principu „žudykite visus, Viešpats atpažins savus“. Islamo fanatikai gali visai nežinoti, kur yra ta ar kita Lietuva ir kuo ji skiriasi nuo Latvijos. Vis tiek jie visi jiems vienodi: tai visai kito tikėjimo žmonės, kurių paslaugomis galima pasinaudoti, o paskui kaip šunis išnaikinti.

Todėl šiandien Pabaltijo šalys ir prie jų prisijungusi Ukraina bet kuria proga bet kurioje tarptautinėje situacijoje stengamos kenkti Rusijai elgiasi kvailiau, nei bet kada anksčiau. Taikindamos IV, jos jau ne šiaip sau, kaip sako rusai, „senelės piktumui ausis nušalsiu“. Čia jau — „senelės piktumui galvą į sieną persiskelsiu“.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 11 — id: `scraped:rubaltic_lt:02763cb2561432a9`

**Title:** Nusimato Lenkijos ir Lietuvos santykių atšalimas

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Po spalio Seimo rinkimų Lenkijoje prisiekė nauja šalies vyriausybė. Lietuvos premjeras Algirdas Butkevičiusšia proga pareiškė, jog tikisi „draugiško ir intensyvaus dialogo“ su nauja Lenkijos vadovybe, kuri yra „artima Lietuvos draugė ir strateginė partnerė“. Pastarieji žodžiai perdėti: paskutiniaisiais metais Lietuvos-Lenkijos santykiai buvo ne draugiški, o priešingai — konfrontaciniai. Ir atėjusi valdžion Varšuvoje „Teisės ir teisingumo“ vyriausybė šią situaciją tik paaštrins.

Lenkija ir Lietuva turi bendrą istoriją, bendrą sieną, bendrus infrastruktūros vystymosi projektus, vienodus užsienio politikos planus ir uždavinius. Taigi atrodytų, abi šalys turi būti strateginėmis sąjungininkėmis. Tačiau, nors Lietuvos premjeras Algirdas Butkevičius teigia, kad taip ir yra, tai galima pavadinti tik svajonėmis.

Strateginė Lenkijos ir Lietuvos partnerystė taip ir nesusiklostė, o kartais santykiuose reiškėsi atvira konfrontacija, kuri beveik visada lietė pažeistas Lietuvos lenkų teises. Ryškiausiai taipasireiškė 2010–2012 metais, kai tarpvalstybiniai Lenkijos-Lietuvos santykiai buvo įvardinami blogiausiais tarp dviejų NATO ir ES šalių. Tuomet neapykanta pasiekė tokio lygio, jog Vilniuje nežinomieji išniekino maršalo Pilsudskio kapą.

Dvišalių santykių pagerėjimo buvo tikimasi 2012 metais, kai Lietuvoje konservatorius valdžioje pakeitė socialdemokratai. „Lietuvybė“: lenkiškų mokyklų likvidavimas, mokymosi jose valstybine kalba organizavimas, lenkiškų vardų ir pavardžių rašyba pagal lietuviškas taisykles, dvikalbių lentelių lenkų kompaktinio gyvenimo vietose nuėmimas — visa tai toleravo Tėvynės sąjungos — Lietuvos krikščionių demokratai.

Socialdemokratai žadėjo peržiūrėti tautinių mažumų įstatymą, neliesti mokymosi nevalstybine kalba, į valdančiąją koaliciją įtraukė Lietuvos lenkų rinkiminę akciją, o jos atstovą paskyrė į strategiškai svarbias pareigas — energetikos ministru. Sąjunga su Lenkija (bent jau susitaikymą) prieš pastaruosius rinkimus į Seimą žadėjo socialdemokratai.

Lietuvos prezidentės Dalios Grybauskaitės pastangomis, kuri po to, kai konservatoriai prarado vyriausybę, ėmė plaukti jų farvateriu, dingo numatytas tautinių mažumų klausimų įstatymuose liberalizavimas, atsinaujino baudos už dvikalbystę, o naujojoje švietimo reformoje nusimato tolimesnis dėstymo nevalstybinėmis kalbomis mažinimas.

Esant tokiai padėčiai nėra ir kalbos apie Lenkijos-Lietuvos strateginį bendradarbiavimą, nors, atrodytų, tam yra galimybių. Tačiau naujasis Lenkijos prezidentas Andžej Duda, savo inauguracijos kalboje iškėlęs Tarpjūrio koncepciją, faktiškai atgaivinančią Jogailaičių idėją, savo pirmuoju vizitu pasirinko ne jogailaičių gimtinę Lietuvą, o tolimą Lenkijai Estiją. Aišku kodėl: sutampant užsienio politikos kryptims, lankantis Lietuvoje neišvengiamai būtų paliesti Lietuvos lenkų padėties klausimai, o tai neabejotinai paaštrintų senstelėjusį konfliktą.

Panašios problemos santykiose su Vilniumi iškils ir naujai lenkų vyriausybei, kuri, kaip ir prezidentas, atstovauja konservatoriškai „Teisės ir teisingumo“ partijai.

Panašios problemos Lenkijai iškyla ir santykiuose su Ukraina: strateginė abiejų šalių sąjunga prieš Rusiją joms pageidautina, tačiau pagalius į ratus kiša istoritnė oficialaus Kijevo politika, didvyriais vaizduojanti Banderos gaujas, išžudžiusias dešimtis tūkstančių Volynės ir Galičinos lenkų.

Beje, Ukraina — svarbiausia šalis antirusiškos „sanitarinės užkardos“ formavime: dėl to naujoji Lenkijos vyriausybė gali atsisakyti savo patriotiškų principų, nusileisdama Kijevui. Na, o Lietuva Rytų Europoje jokio strateginio vaidmens nevaidina, apie jos misijos paskirtį tik svavoja „landsbergistai“. Ir todėl santykiuose su Vilniumi lenkų elitas gali demonstruoti rinkėjams prinsipingumą ir nekurti strateginės sąjungos tol, kol bus pažeidžiamos Lietuvos lenkų teisės.

Tačiau akivaizdus klausimas: o ar nori strateginės sąjungos su Varšuva Vilnius? Ne paslaptis, jog nežiūrint į seniai susiklosčiusias teigiamas aplinkybes ji neatsirado tik dėl Lietuvos vadovybės kaltės. Norint Lietuvai suartėti su Lenkija nebūtinai reikėjo suteikti visas teises Vilniaus krašto lenkams — būtų pakakę neaštrinti Lietuvos lenkų padėties. Elementariai — neuždaryti lenkiškų mokyklų, nepanaikinti Tautinių mažumų įstatymo ir supaprastintos lietuvių kalbos egzaminų nelietuvių šeimų vaikams laikymo tvarkos, neliesti dvikalbių lentelių ir nebausti tų savivaldybių vadovų, kurie nepanoro jų nuimti.

Tačiau Lietuvos konservatoriška vadovybė ir prezidentė Grybauskaitė pastoviai aštrino Lietuvos lenkų temą.

Kam jiems to reikėjo, turint palaikymą lietuviškojo elektorato, vis prisimenančio lenkiško socialinio dominavimo laikus? Atsakant verta priminti, kad dabartinę Lietuvą ekonomiškai išlaiko du fenomenai: rekordinė depopuliacija, dėl kurios gyventojams reikia skirti vis mažiau išlaidų, ir Briuselio dotacijos, sudarančios 20% Lietuvos BVP. Tačiau Eurokomisijos valdininkai neskirs eurofondus Lietuvos prašymu šiaip sau: jie už tai nori sulaukti Vilniaus atpildo.

Briuselis, Grybauskaitei padedant, vykdo Lenkijos pristabdymo politiką. Tokią, kokią Lenkija norėtų vykdyti santykiuose su Rusija. Rytų Europai Lenkija per didelė, per daug kylanti, savarankiška, įžūli. Reikalauja iš Briuselio biurokratijos teisių ir ypatingo požiūrio, demonstruoja regioninio lyderio ambicijas, nesistegdama vaidinti, jog tai daro ES labui.

„Teisės ir teisingumo“ atėjimas valdžion šią lenkų valdžios ypatybę tik sustiprins: ir prezidentas Andžej Duda, ir premjeras Beata Šidlo, ir URM vadovas Vitoldas Vaščikovskis, ir už jų nugarų stovintis Jaroslavas Kačinskis ne kartą sakė, kad santykiuose su Eurokomisija Varšuva turi elgtis ryžtingiau ir radikaliau. Jeigu „Teisės ir teisingumo“ veikėjai konfrontuos su Briuseliu, o tai jau matėme jiems esant valdžioje 2005–2007 metais, tai strateginė Lenkijos-Lietuvos sąjunga dar labiau atitols: Grybauskaitės ir kitų Lietuvos politikų provokatoriški talentai, ardantys tarptautinius santykius, tokiomis sąlygomis bus kaip niekada reikalingi.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 12 — id: `scraped:rubaltic_lt:68d1416c5b3d0f90`

**Title:** Lietuvos energetinės nepriklausomybės mitas — ant subliuškimo ribos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Oficialaus Vilniaus planai tapti Pabaltijo regione „benzino kolonėlės karaliumi“ bliūška: Lietuvos Seimas svarsto galimybę sumažinti norvegų dujų importą Klaipėdos terminalui. Ne už kalnų eilinės derybos su „Gazpromu“ dėl „nedemokratinių“ dujų pirkimo iš Rusijos. Lietuvos energetinės nepriklausomybės mitas artėja prie subliuškimo ribos.

Šiuo metu Seimas svarsto, kiek suskystintų gamtinių dujų (SGD) pirkti iš Norvegijos. Svarstoma galimybė inicijuoti derybas su Statoilo koncernu, kad būtų sumažinta SGD tiekimo apimtis. Dėl būtinybės pasukti šiuo keliu pirmadienį susitikimo Ekonomikos komitete metu susitarė Litgas, Klaipėdos nafta, Kainų komisijos bei Energetikos ministerijos atstovai.

Pasirodo, dujų poreikis Lietuvoje sparčiai krinta, o jų perteklius nereikalingas nei vietos rinkai, nei kaimyninėms Pabaltijo respublikoms. Pagal agentūros Reuters pranešimą, šiais metais liks neparduota maždaug 200 mln iš Norvegijoje užsakytų 540 mln kubinių metrų dujų. Kitais metais dujų perteklius gali siekti 240 mln.

2014 metais Lietuvoje pradėjo veikti SGD terminalas simboliniu pavadinimu Independence („Nepriklausomybė“ — RuBaltic.Ru past.). Lietuvos ir Europos politikai pavadino šį įvykį itin svarbiu kuriant ES energetinę rinką ir monopolijos pabaigos pradžia to „Gazpromo“, kuris ne taip seniai vienintelis tiekė dujas respublikos rinkai. Buvo tikėtasi, kad 145 mln eurų kainavęs terminalas padovanos Lietuvai realią energetinę nepriklausomybę ir visiškai išstums iš vidaus rinkos „nedemokratines“ Rusijos dujas.

Oficialusis Vilnius susikūrė mitą, jog lietuviškasis energetinės nepriklausomybės kelias toks šaunus, kad šalies vadovybė pradėjo dalintis savo pasiekimais kovoje su „totalitariniais“ dujų tiekėjais. „Lietuva pasirengusi pasidalinti patirtimi kuriant LNG-terminalus (SGD terminalus — RuBaltic.Ru past.) ir atsikratant priklausomybės Rusijai“, — parašė Ukrainos prezidentas Piotr Porošenko savo puslapyje Twitter po susitikimo Kijeve su lietuviškaja „geležine ledi“ Dalia Grybauskaite.

Tačiau SGD kaina (ypač žiemos sezono metu), dešimties metų terminalo Independence laivo-saugyklos nuoma ir išlaidos Klaipėdos terminalo infrastruktūros statybai padarė „nepriklausomas“ suskystintas dujas žymiai brangesnes už „Gazpromo“.

Taip, norvegų dujų kaina sudaro 328,9-365,5 dolerių už tūkstantį kubinių metrų, suskystinimo ir išskystinimo procedūros — 60 dolerių; kitos SGD terminalo išlaidos — dar 145 doleriai. Taigi visa SGD kaina sudaro 534-571 dolerių už tūkstantį kubinių metrų, tuo metu kai „Gazpromo“ dujos kainuoja 370 dolerių. Logiška, kad Lietuvai tiek brangių SGD nereikia, o jei naudoti tik jas, šildymo kainos kils iki debesų, o pramonės likučiai taps visiškai nerentabilūs.

„Aš ne kartą sakiau, kad mūsų terminalas buvo politinis projektas, stengėmės jį pastatyti kaip galima greičiau, viską padarėme paskubom, gavosi labai brangiai“, — prieš metus „Žinių radijui“ sakė Pramonininkų konfederacijos direktoriaus pavaduotojas Vidmantas Jankauskas. Jo SGD terminalo, kaip politinio projekto, vertinimas atitinka tikrovės, nes tokiam menkam, kaip Lietuva, vartotojui suskystintos dujos negalėjo būti pigesnės, nei tiekiamos vamzdžiu. Siekdamas nors kiek kompensuoti politinės „energetinės nepriklausomybės“ praradimus, oficialusis Vilnius tikėjosi perparduoti dujų perteklių kaimyninei Latvijai. Tačiau kai klausimas paliečia piniginę, pabaltijo vienybė ima irti. Štai ir šį kartą oficialioji Ryga išdavė lietuvišką SGD terminalą, likdama ištikima rusų dujų monopolininkui. „Latvijos dujų poreikius visiškai tenkina ilgalaikis kontraktas su „Gazpromu“, — pranešė Latvijas Gaze kompanijos valdybos narys Mario Nullmeyer.

Latvijai tiekiamos rusiškos dujos 8-12 % pigesnės, nei Klaipėdos terminalui tiekiamos Statoilo, ir tai neįskaitant transportavimo išlaidų.

Štai ir estai, kuriuos Vilnius laikė potencialiais pirkėjais ir kurie, būdami solidarūs, net įsigijo bandomąjį kiekį suskystintų dujų, ketina statyti savo SGD terminalą, o tai galutinai palaidos Klaipėdos terminalo, kaip regioninio, ambicijas.

Kas dėl Lietuvos vyriausybės pastangų kuriant „energetinę nepriklausomybę“ ir garbinant SGD terminalą, tai jos primena postringavimą apie peles, kurios „verkia, badosi, tačiau tebegraužia kaktusą“. Dabar gi, supratęs, kad suskystintos „demokratinės“ dujos išdidžiai respublikai per daug tuština kišenę, oficialusis Vilnius vėl veda derybas su rusų dujų monopolininku dėl naujų pirkimų. Ir tuo pačiu metu lietuviškasis elitas aktyviai ieško būdų kaip sumažinti importą norvegų dujų, kurios turėjo dovanoti respublikai „energetinę laimę“.

Tokiu būdu, Klaipėdos SGD terminalas tapo brangiu ir nereikalingu žaisliuku, už kurį Lietuvos mokesčių mokėtojai dar ilgai turės tuštinti savo kišenes.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 13 — id: `scraped:rubaltic_lt:53052f4d7c3653dc`

**Title:** Jei Lietuva atsisakys rusiškų dujų...

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Likus mėnesiui iki kontrakto su „Gazpromu“ galiojimo pabaigos Lietuvos viršūnėlės giriasi visiškai atsisakysiančios rusiškų dujų. Energetikos ministras Rokas Masiulis teigia, kad dabar šalis turi nuosavą SGD terminalą, o vyriausybė vietoj rusiškų dujų renkasi amerikietiškas. Ir tuo metu nutylima, kad Klaipėdos SGD terminalas tenkina tik trečdalį Lietuvos energetinių poreikių. Neinformuojama, kiek kainuos suskystintos užjūrio dujos lyginant su rusiškomis. Tokiu būdu bus įdomu stebėti, kaip gyvuos Lietuva, jei jos vadovybė didingu mostu visiškai atsisakys rusiškų dujų.

„Jeigu „Gazpromas“ pasiūlys gerą kainą, atnaujinsim susitarimą, jei ne, naudosim suskystintas gamtines dujas“, — taip komentavo derybas su rusų tiekėju energetikos ministras Rokas Masiulis. Kitą mėnesį baigiasi sutarties us „Gazpromu“ terminas, pagal kurią rusiškos dujos Lietuvai buvo tiekiamos po 370 dolerių už tūkstantį kūbinių metrų. Tokiu būdu, jei Lietuvos derybininkus nauja kaina netenkins, ji lengvai pereis prie SGD.

Atsižvelgiant į tai, kad Lietuvos Respublika nėra „Gazpromui“ stambi ir svarbi vartotoja, vargu ar tokie grūmojimai nors kiek nugąsdino rusų koncerno darbuotojus. Tačiau Lietuvos vadovybė gyvena savame pačios sukurtame ypatingame pasaulėlyje, kuriame jei „Gazpromas“ sumažina Lietuvai dujų kainą, tai neabejotinai todėl, jog išsigando SGD terminalo atidarymo.

Tai ne blefas, tai nuoširdus įsitikinimas.

Pasak ne tik logikos, bet ir fizikos dėsniams prieštaraujančio Lietuvos dešiniųjų argumentavimo, rusiškų dujų kainų sumažinimas — konkurencijos Lietuvos energetikos rinkoje atsiradimas, nors sumažinimas įvyko prieš pusę metų iki to atsiradimo. Kaip konkurencija su SGD terminalu privertė 20 % sumažinti Lietuvai dujų kainą, jei tas terminalas 2014 metų gegužę neegzistavo — klausimas Lietuvos dešiniesiems.

Kitas klausimas: kodėl „Gazpromas“ mažino dujų kainą, jei rinkos konkurencijos sąlygomis jų kaina ir taip buvo mažesnė, nei suskystintų gamtinių dujų? Senoji kaina buvo 450 dolerių už tūkstantį kūbų, ir „Gazpromas“ turi pakankamai ekspertų ir analitinių struktūrų, kad paskaičiuotų, kiek Europos energetikos rinkoje kainuoja suskystintos gamtinės dujos ir kiek savo kišenę turės patuštinti Lietuva įskaitant transportavimą, infrastruktūros išlaikymą ir kitas išlaidas. Pasirodo, virš 450 dolerių — tai kodėl „Gazpromas“ turėjo išsigąsti ir sumažinti kainą?

Trečias klausimas: jei kainas Lietuvos dujų rinkoje po SGD terminalo atidarymo nustato rinkos konkurencija, tai kodėl Lietuvos valstybė perka ne pigesnes, o brangesnes dujas? Tai kertasi su rinkos kainodaros pagrindais ir blaiviu mąstymu.

Tačiau Lietuvos vyriausybė ne šiaip sau renkasi SGD, bet prievarta verčia įmones būtent jas pirkti (o kur tada rinkos konkurencija?). O energetikos ministras Rokas Masiulis teigia, jog Lietuvos prioritetas — atsisakius rusiškų, pirkti amerikietiškas dujas: „Mes norėtume, kad mūsų sistemoje daugiau būtų dujų ne iš Rusijos, JAV dujos atitinka mūsų dujų formulę, pagal sudėtį jos panašios į rusiškas“.

Tačiau Lietuvos valdžia vis tiek pasiryžusi aprūpinti šalį amerikietiškomis dujomis ir mano, kad ne ji, o „Gazpromas“ turi bijoti šio „genialaus“ sumanymo ir išlaikyti žemą savosios produkcijos kainą, siekiant nepralaimėti rinkos konkurencijos. Kokia tokiu atveju turi būti rusiškų dujų kaina, kad nupigtų dujų kelionė iš Šiaurės Amerikos, baisu įsivaizduoti.

Padėtis Lietuvos piliečiams tampa dar baisesnė, suvokiant šalies energetikos ministro žodžių prasmę: „Jei „Gazpromas“ pasiūlys gerą kainą, atnaujinsim susitarimą, jei ne — naudosim suskystintas gamtines dujas“. Kontraktas su „Gazpromu“ nustoja galiojęs kitą mėnesį. Jei Lietuvos derybininkams nepatiks siūloma kaina ir jie įvykdys žadėtus grąsinimus, demonstratyviai atsisakydami rusiškų dujų, Lietuva nepasinaudos SGD — ji tiesiog liks be dujų. Todėl kad norvegų kompanija Statoil — vienintelis šiuo metu SGD tiekėjas Lietuvai — įsipareigojo kasmet tiekti 540 mln. kūbų dujų, o tai pasirašant sudarė 18-20 % Lietuvos energetinio poreikio.

Tiesa, po to dėl šalies ekonominio vystymosi sulėtėjimo ir nesibaigiančio gyventojų emigravimo poreikiai sumažėjo, tačiau ir dabar SGD terminalas padengia tik trečdalį Lietuvos dujų poreikio.

Žinoma, laivo Independence dėka šios krizės bus galima išvengti — į Klaipėdą bus atvežtos naujos suskystintos dujos. Tačiau tam reikės laiko. Ir galima suvokti, kiek ši produkcija kainuos: pirkti papildomą SGD kiekį teks skubotai, o pagal vis tos pačios rinkos konkurencijos dėsnius kuo didesnis poreikis, tuo aukštesnė kaina. Todėl bet kokiu atveju kaina bus aukštesnė už „Gazpromo“.

Visi šie argumentai akivaizdūs. Tačiau problema glūdi tame, jog akivaizdūs jie pašaliniams blaiviam stebėtojui, bet ne Lietuvos politinei klasei, kuri gyvena savame ypatingame energetiniame pasaulyje. Tame pasaulyje gyvenantis Lietuvos Seimo narys teigia, kad Klaipėdos SGD terminalą turi išlaikyti ir... „Gazpromas“, kurio konkurentu ir buvo sumąnytas tas terminalas. Ir jei rusiškų dujų kaina Lietuvos netenkins, tai jos delegacija gali jų atsisakyti. Ir kadangi rusiškos dujos per brangios, reikia džiaugtis amerikietiškomis, vežti kurias iš Amerikos, žinoma, daug pigiau nei pasiimti iš rusiško vamzdžio.

Seniai žinoma: geriausias minčių realybei atitinkamumo patikrinimas — susidūrimas su realybe. Todėl jei oficialūs Lietuvos asmenys tiki tuo, ką kalba, — lai taip ir daro. Lai atsisako rusiškų dujų — dėl įdomumo: o kas gi toliau? O kas toliau — tikrai įdomu. Tačiau nereikia savo paistalais gąsdinti „Gazpromo“ — tai taip par juokinga ir neefektyvu, kaip derybų metų žadėti užbaigti jas savižudybe.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 14 — id: `scraped:rubaltic_lt:e196222108f64bcc`

**Title:** Lietuva – Lenkija: dvišalių santykių pamokos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Įspūdinga J. Kačinskio vadovaujamų Lenkijos konservatorių pergalė parlamento rinkimuose susilaukė rimto Lietuvos politikų ir politologų atgarsio. Prezidentė D. Grybauskaitė išreiškė viltį, jog bus tęsiamas konstruktyvus bendradarbiavimas energetikos ir saugumo srityse. Tačiau valstybės vadovė nepanoro liesti galimo įtampos tarp Vilniaus ir Varšūvos ūgtelėjimo tautinių mažumų klausimo. Beje, užsienio reikalų ministras L. Linkevičius pareiškė, jog Lenkijos tautinių mažumų politikų keliamos problemos „neturi sukelti įtampos santykiuose su būsima Lenkijos vyriausybe ir stabdyti bendradarbiavimą saugumo ir energetikos srityse“.

Kodėl santūriai reaguojama į parlamento rinkimų Lenkijoje rezultatus?

Pasak Kauno Vytauto Didžiojo universiteto profesoriaus Š. Leikio, Vilniui bus sudėtinga bendrauti su partijos „Tvarka ir teisingumas“ konservatoriais — šiuo metu šiai partijai atstovauja ne tie politikai, kuriems prieš dešimt metų rūpėjo geri santykiai su Lietuva. Politologo nuomone, valdžion atėjusiai naujai politikų kartai visų pirma rūpi „savos valstybės ir savų interesų gynyba“. Todėl tikėtina, jog nauja valdžia aktyviai rems užsienyje, tame tarpe ir Lietuvoje, gyvenančius lenkus, kurie „piktinasi įvairiais klausimais ir kreipiasi su prašymais“.

Galima drąsiai teigti, kad naujoji lenkų valdžia visų pirma pasistengs spręsti kompleksą dvišalių santykių senstelėjusių problemų, kurias daug pažadų žarsčiusi Lietuvos valdžia taip ir nerealizavo. Pagrindine tema taps lenkų mažumų interesų ignoravimas (originalus oficialiuose dokumentuose lenkiškų pavardžių rašymas, lenkų asimiliavimo politika mažinant mokomųjų dalykų dėstymą gimtąja kalba ir t.t.). Varšuva ne tik aktyvins dialogą šia tema — ji pasinaudos Europarlamento tribūna, siekdama įpareigoti Vilnių vykdyti europietiškas rekomendacijas ginant tautinių mažumų teises.

Jeigu 2014 metais D. Grybauskaitė Europarlamento sesijoje galėjo teigti, jog tautinės mažumos nėra diskriminuojamos, ir viešai aiškintis santykius su lenkų europarlamentarais, tai nuo šiol visa tai taps problematiška. Beje, jau tada Lietuvos prezidentės žodžius lenkai paneigė remdamiesi europietiškų organizacijų išvadomis. Antai organizacija „Freedom House“ (2013 m.) pareiškė, kad etninių mažumų diskriminavimas Lietuvoje tapo problema, ypač pabrėždama, kad šių mažumų mokiniai verčiami laikyti egzaminus kartu su lietuvių vaikais pagal vieningą lietuvišką standartą. Teisėsaugos organizacija „Amnesty International“ savo ataskaitose nuolat nurodo, jog Lietuva iki šiol neratifikavo Žmogaus teisių ir fundamentalių laisvių gynimo konvencijos, kuri draudžia visas diskriminavimo formas, Protokolo Nr.12. Europos Tarybos ministrų komiteto rezoliucija dėl Rėminės tautinių mažumų gynimo konvencijos vykdymo iki šiol nesulaukė Lietuvos valdžios dėmesio. Joje, beje, nurodoma, jog Lietuvoje nėra aiškaus teisinio tautinių mažumų gynimo reguliavimo, apstu kliūčių skiriant tautinių mažumų mokykloms valstybinių lėšų, menkai finansuojama ir nesulaukia pakankamo dėmesio kultūros sritis, kai kurie Lietuvos teismų sprendimai prieštarauja Rėminei konvencijai.

Lenkija daugelį metų siekia per saviškius — Lietuvos lenkų rinkiminę akciją (Lietuvoje gyvena 200 tūkst. lenkų — 6,5% šalies gyventojų) — Lietuvos valdžios įsipareigojimo priimti įstatymą dėl originalaus lenkiškų vardų rašymo vykdymo. Vilnius šia tema naudojasi derantis priklausomai nuo konkrečios užsienio politikos ir ekonominės konjunktūros. Antai eilines kalbas dėl šio įstatymo priėmimo inicijavo socialdemokratų lyderis ministras pirmininkas A. Butkevičius šių metų gegužės mėnesį. Tuo metu Lietuvos valdžios geranoriškumas atsirado prisibijant, kad Lenkija gali panaudoti spaudimą atidedant Europos Sąjungos finansavimą strategiškai svarbios Lietuvai dujų tarp dviejų šalių sandūros, kuri padės galutinai integruotis į vieningą Europos dujų rinką (iki 2020 m.). Kai Europos komisija patvirtino reikalingus projekto finansavimo parametrus, savaime išnyko klausimas dėl svarstymo Seime Įstatymo projekto, kuris eilinį kartą buvo pasmerktas apdorojimui. O kas dėl premjero A. Butkevičiaus pažadų kolegai D. Tuskai (2014 m. balandis), kad Įstatymas bus priimtas per keletą mėnesių, tai jie buvo sėkmingai pamiršti.

Varšuva nuo 2014 m. ėmė siųsti signalus Vilniui, jog daugiau nenori tenkintis tuščiais pažadais. Oficialaus vizito Vilniuje 2014 m. metu lenkų parlamento vicespikeris C. Grabarčikas pareiškė, kad įstatymo dėl tautinių mažumų nebuvimas pažeidžia lenkų diasporos teises, o taip pat iškėlė teisminio persekiojimo klausimą dėl gatvių pavadinimų dvikalbių iškabų kompaktinio lenkų mažumos gyvenimo vietovėse.

Atsakydama į besitęsiantį ignoravimą, Lenkija atitolo nuo Lietuvos politikos regionalaus saugumo srityje, savo prioritetu pasirinkdama „savus interesus, o ne Ukrainos likimą“. Tokiu būdu Lietuvos diplomatija patyrė netikėtą smūgį — ta diplomatija, kuri visose tarptautinėse aikštelėse triūbino (norėdama sumenkinti Minsko sutarimus Ukrainos karinio konflikto sureguliavime), jog „Rusijos agresija Ukrainoje — grėsmė visai Europos Sąjungai“. Kitas konkretus Varšuvos žingsnis — prezidento veto dėl etninių ir tautinių mažumų regioninės kalbos įstatymo (lietuvių — 6 tūkstančiai arba 0,02% Lenkijos gyventojų).

Susiformuoti pragmatiškam Varšuvos žvilgsniui padėjo ir skandalingas Mažeikių Naftos perdirbimo gamyklos įsigijimas — galutinė kaina dukart viršijo konkurentinius pasiūlymus, o tai 2,4 milijardo JAV dolerių. Maža to, Lenkija sulaukį žaliavos tiekimo dujotiekiu „Družba“ sustabdymo, o dar Lietuvos geležinkeliai (valstybės kontrolė) atsisakė pateikti anksčiau suderintą pagal pirkimo sąlygas lengvatinį geležinkelio tarifą krovinių pervežimui. Lenkijos bandymas persiorientuoti į pigesnę logistiką per Ventspilio, Rygos ir Liepojos uostus buvo sutiktas blokada. Geležinkeliečiai, suvaidinę neatidėliotiną remontą, išardė 19 kilometrų kelio Mažeikiai – Rengė (Latvija), o tai 80 kilometrų prailgino kelią iki Ventspilio, tuo panaikindami latviško tranzito naudą. Lietuva eilinį kartą aukščiausiame lygyje pažadėjo Lenkijai išspręsti šią logistinę problemą, tačiau nuo 2010 metų reikalai taip ir nepajudėjo iš vietos.

Iš naujosios lenkų valdžios Lietuvai nėra ko tikėtis. D. Grybauskaitės, atsakingos už šalies užsienio politiką, nenoras antrosios kadencijos metu normalizuoti santykius su Lenkija galutinai suardė partnerių pasitikėjimą. Deja, abipusiai santykiai gali pasiekti naują lygį, ir tada susikaupęs konfliktinis potencialas pasireikš visa savo galia.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 15 — id: `scraped:rubaltic_lt:3e3eb7cf6aae829d`

**Title:** Už „energetinę nepriklausomybę“ privers mokėti eilinius lietuvius

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvoje svarstomos SGD terminalo Įstatymo pataisos, pagal kurias terminalo išlaikymo išlaidas turės padengti visi dujų vartotojai ir gyventojai. Energetikos ministerija grąsina, jog jei galutiniai vartotojai nefinansuos terminalo išlaikymo, tai vien tik Vilniuje šildymo tarifai ūgtels 20%. Tokiu šalies vadovybės kovos už „energetinę nepriklausomybę“ rezultatu turi „pasidžiaugti“ eiliniai piliečiai.

Lietuvos vadovų energetinė politika visada dvelkė nesamone – ir kai jie uždarė Ignalinos AES, ir kai bandė statyti Visagino AES, ir kai ieškojo Lietuvoje skalūnų dujų, ir kai svajojo visą šalį apšildyti biokuru.

Ne išimtis šiuose „Lietuvos energetinės nepriklausomybės“ klystkeliuose ir SGD terminalo epizodas.

SGD terminalo statyba Klaipėdoje buvo sumanyta tikslu atsikratyti „Gazpromo“ monopolijos, kurią Lietuvos vyriausybė sukūrė pati, uždarydama Ignalinos AES. Tikėtasi, jog alternatyvaus tiekėjo atsiradimas sumažins galutinę vidutinę dujų kūbinio metro kainą Lietuvai.

Likus pusmečiui iki plaukiojančiojo terminalo Independence įvedimo ekploatacijon, „Gazprom“ 20% sumažino Lietuvai dujų kainą, ir tai Lietuvos valdžia tuoj pat pavadino pasiekimu: suprask, rusiškas monopolininkas pabūgo būsimosios konkurencijos, štai ir puolė mažinti kainą.

Deja, po to, kai Klaipėdoje buvo pradėta eksploatuoti terminalą, paaiškėjo, kad norvegų suskystintos dujos brangesnės už buvusias ir esamas rusiškas dujas iš vamzdžio.

O dar kai kurios valstybinės ir municipalinės Lietuvos įmonės priverstos iš SGD terminalo pirkti dujų 60% ir daugiau. Antai sostinės vartotojams šilumą tiekiančią „Vilniaus energiją“ valdžia privertė pirkti iš terminalo 65% jai reikalingų dujų — todėl sumažėjusios kainos už šildymą vėl ėmė kilti.

Taigi kame slypi Lietuvos energetinis politinis laimėjimas, jei vietoj atpigusių rusiškų dujų įmonės verčiamos pirkti brangias norvegiškas?

O toliau — dar gražiau.

Energetikos ministerija paruošė SGD terminalo Įstatymo pataisas, pagal kurias terminalo išlaikymo išlaidas privalės padengti visi vartotojai. Energetikos ministras Rokas Masiulis tvirtina, jog Įstatymo pataisos reikalingos siekiant permesti išlaidų padengimą ant platesnio rato vartotojų pečių ir susieti jas su konkretaus vartotojo pajėgumu: kuo vartotojas pajėgesnis, tuo daugiau jis turi mokėti.

Tikiu būdu, jei kišenes terminalo išlaikymui ims tuštinti visi piliečiai, Vilniaus gyventojai už dujas mokės 4% mažiau. O jei terminalą išlaikys siauresnis vartotojų ratas, pagrindinis finansinis krūvis teks šilumos tiekėjams, kurie šildymo kainas Vilniuje turės padidinti net 20%.

Suprask, bet kokiu atveju piliečiai turės mokėti daugiau: arba už „energetinę nepriklausomybę“, arba už šildymą. Tačiau primokėti už „energetinę nepriklausomybę“ reikęs mažiau, nei už šildymą — taip eilinius piliečius džiugina valdininkai, norėdami įtikinti lengvatikius, kad išlaikyti brangiai kainuojantį nerentabilų SGD terminalą tiesiog privalu.

Visaliaudinis Klaipėdos terminalo finansavimas gal ir turėtų prasmę, jeigu pats terminalas turėtų ekonominę prasmę. Tačiau tokia prasmė neegzistuoja. Kad būtų padengtos visos terminalo išlaikymo išlaidos, jo metinė apyvarta turi būti 10 kartų didesnė už tą energijos kiekį, kuris reikalingas Lietuvai. Tačiau tokios apyvartos Klaipėdos terminalas nepasieks niekada: tiek energijos nesuvartos nei Lietuva, nei jos kaimynai.

SGD terminalas Lietuvos valdžiai — lagaminas be rankenos. Sunku jį nešti, bet ir išmesti nevalia. Ne vienerius metus buvo kalbama apie šį terminalą, triukšmingai praeitą rudenį įvedant jį rikiuotėn, pasigiriant sąjungininkams Vakaruose, nudžiuginant savuosius „runkelius“ — įvykis pateiktas kaip didis Lietuvos vadovybės laimėjimas.

Ir argi dabar galima pripažinti, kad terminalas nuostolingas? Jokiu būdu! Išeitis — užkrauti jo išlaikymą ant gyventojų pečių. Ir tai valdžia padarys jai būdingu būdu: aiškinant, kad ji visada tarnauja tautai. O jei ta tauta neparems „energetinės nepriklausomybės“, jai, nieko nesuprantančiai, teks mokėti už šilumą 20% daugiau.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 16 — id: `scraped:rubaltic_lt:b1e31de9d72f9f08`

**Title:** „Jei žmonės bėga plauti grindis už 800 eurų, tai daug ką sako apie jų gimtąjį kraštą“

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Krizė iškėlė klausimą visų griežtumu — arba į Europą, arba į Rusiją, bet tikrai nelikti Lietuvoje. 2008 metais su tokia dilema susidūrė daugelis Pabaltijo gyventojų. Mūsų šiandienos herojaus istorijoje buvo pasirinkta Rusija.

Viktor, 31 metai, inžinierius. Pasidavęs visuotinei emigrancijos jaunimo madai 2008 metais, iškeitė jaukią Šiaulių buitį į gintarinius Kaliningrado saulėlydžius.

2007 metais aš dirbau didžiausioje Šiaulių projektavimo organizacijoje. Mūsų kolektyve buvo moteris, kurios brolis gyveno Amerikoje ir užsiimdavo automobilių pervežimais. Būtent iš jo aš išgirdau, kad JAV bręsta krizė. Pagalvojau, kad greitai parkeliaus ir pas mus. Lietuvoje staigiai krito nekilnojamojo turto kainos, žmonės pradėjo prarasti darbą, statybos praktiškai sustojo. Gyvenimas ženkliai blogėjo. Aš supratau, kad mūsų statybų sferoje bręsta labai rimta krizė. Tada ir susimąsčiau apie emigraciją iš Lietuvos.

Išvykti iš Lietuvos staiga tapo madinga. Daugelis vis dėl to planavo sugrįžti. Tarp kitko, staigus būsto kainos kritimas buvo išprovokuotas ir emigracijos. Būstas Lietuvoje tapo nebereikalingas. Visi išvažiuodavo ir išvažiuodavo, ir kolkas niekas negrįžo.

Iš mano draugų ir pažįstamų Lietuvą paliko apie 60-70 %. Kai kurie išvyko iš Šiaulių į didesnius miestus — į Vilnių ir Kauną. Bet daugiausia, be abejo, išvyko į kitas Europos šalis. Man taip pat kilo noras kur nors išvažiuoti. Apie Rusiją tada nemąsčiau: žinojau, kad ten viskas bus daug sudėtingiau dėl dokumentų. Jokiu būdu nepasinaudočiau gyventojų persikėlimo programa – tai labai sudėtinga biurokratijos atžvilgiu.

Nagrinėjau visokiausius variantus, bet persikėliau vis tiek į Rusiją: aš sutikau merginą iš Kaliningrado, kuri tapo mano žmona. Man persikelti į Kaliningradą buvo daug paprasčiau, negu mums abiems į kažkokią kitą Europos šalį. Pirmiausia, man Rusijoje buvo paprasčiau surasti darbą, negu jai Europoje. Antra, sunkumų su jos dokumentais ES būtų daugiau, nei su mano Rusijoje. Galiausiai Rusijoje buvo mažiau biurokratinių vilkinimų, buvo paprasčiau surasti gerai apmokamą darbą. Todėl pasirinkau Rusiją ir gyvenu ten iki šiol, nors su žmona seniai išsiskyrėm.

Kai aš persikrausčiau į Kaliningradą, jokio kultūrinio šoko nepatyriau. Mūsų jaunimo kultūros labai panašios. Tiesiog lietuviai labiau agresyvi tauta, o čia man visi ramesni.

Kaliningrade nustebino didelis skaičius benamių gyvūnų gatvėse. Tokia problema buvo Lietuvoje 90-ais metais, bet ją išsprendė. Manau, kad tai stebina visus europiečius, kurie atvyksta į Kaliningrado sritį. O šiaip — tos pačios „chruščiovkės“, tie patys benamiai, viskas tas pats.

Kiek gyvenu Kaliningrade, nei karto man nekilo noras grįžti į Lietuvą. Ir aš manau, jis kils nedaugeliui išvykusių. Aš nežinau, kas turėtų įvykti Lietuvoje, kad žmonės pradėtų ten grįžti. Nes Lietuva ekonomiškai nestabili šalis. Daug nestabilesnė už Rusiją. Rusijoje nors ir šokinėja valiūta, infliacija ir taip toliau, bet vis tiek čia stabiliau. O Lietuvoje šiandien labai paprasta prarasti darbą. Darbdaviai kelia reikalavimus, kadangi darbo rinkoje daug bedarbių. Dėl to auga konkurencija. O Kaliningrade yra daug galimybių užsidirbti pinigų.

Daug mano draugų išvažiavo į Angliją, Airiją, Norvegiją. Kartais aš su gailesčių galvoju, kad neišvažiavau ten, kaip jie. Bet tai tik pamąstymai, o ne pavydas. Aišku, jų algos daug didesnės ir jie turi daugiau tam tikrų galimybių, tačiau yra vienas „bet“. Visi jie vis tiek jaučiasi svetimi šiose šalyse. Ir į juos žiūrima kaip į antrarūšius žmones, nepaisant to, kad visi jie europiečiai. Ir daugiausia jie, Lietuvos emigrantai, dirba tose pačiose pareigose, kaip ir atvykėliai iš trečių šalių.

O Kaliningrade aš jaučiuosi savas. Nė karto nesu susidūręs su tokiai reiškiniais, kaip „tu, lietuvi, eik iš čia“. Čia nėra jokių engimų. Manau, Rusija iš vis labai tolerantiška kitų tautų atžvilgiu šalis, ypač palyginus su ES šalimis. Tai mano asmeninė nuomonė.

Ar sudėtinga Kaliningrade būti emigrantu? Nė kiek. Na, pasitaiko vietinių juokelių dėl politinės padėties Lietuvoje. O šiaip, jokio ypatingo požiūrio į save aš nejaučiu.

Saviidentivikacija? Aš jaučiuosi rusas, taip. Mano mintys rusų kalba, skaitau aš rusiškai.

Aš nedalyvauju aktyviam pilietiškam Lietuvos gyvenime, neinu į rinkimus — nors aš ir Lietuvos pilietis, tačiau ten negyvenu ir neketinu grįžti. Nežinau, kokia ateitis laukia Lietuvos. Manau, kad žmonės ir toliau emigruos. Šalyje apsigyvens pabėgėliai. Žinoma, juokauju. Bet kiekviename juoke yra dalis tiesos. Aš manau, kad žmonės bėga ne iš gero gyvenimo. Jei žmonės bėga plauti grindis už 800 eurų svetimoje šalyje, tai daug ką pasako apie jų gimtąją šalį. Lietuva nebloga šalis, ten gyvena geri žmonės. Tačiau aš visiškai nesigailiu, kad išvažiavau iš Lietuvos, ir net neturiu pažymėti, ko man čia trūksta.

Iš visų mano draugų iš Šiaulių į Lietuvą grįžo tik vienas. Vienas! Be to, jis grįžo tik dėl to, kad krosnis, kurias jis statė Anglijoje, jis pradėjo tiekti Lietuvon. Kitų žmonių tarp mano pažįstamų, kurie norėtų ir galėtų grįžti į Lietuvą, aš nežinau.

Nenoriu važiuoti į Rusijos didmiesčius. Ten gražu, bet labai dideli atstumai, ir viskas išnyksta. O Kaliningradas — gera vieta gyventi, viskas kompaktiška, šalia, dar kolkas nedideli kamščiai.

Išvykti į Europą? Taip, kartais kyla tokių minčių. Pirmiausia dėl rubliaus padėties ir žemos mano darbo kainos. Dėl šito kyla minčių persikelti į Europą. Bet dar pakenčiamai.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 17 — id: `scraped:rubaltic_lt:ad4f254d42e67412`

**Title:** Kaip kūrėsi ukrainizmas: idėjinės šaknys

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Ukrainietiškas nacionalizmas — tai giliai archajiškas, svetimas progresui ir bendražmogiškai kultūrai reiškinys, kurio vienintelis tikslas — suskaldyti vieningą tautą, dirbtinai sukuriant iš etnografinių pietų Rusijos ypatumų atskirą — ukrainietišką — tautą. Apie tai kalbėjo patys ukrainizmo tėvai-steigėjai privačiuose laiškuose ir net atviroje spaudoje. Ukrainietiško nacionalinio-politinio judėjimo patriarchai genialiai išpranašavo šiandieną: viskas, kas antrojoje XIX amžiaus pusėje – XX amžiaus pradžioje buvo aptariama marginalinėje inteligentų-ukrainofilų aplinkoje, dabar vyksta Ukrainoje visos tautos mastu.

„Mes barbarai; mūsų svajos ir siekiai tikrovėje yra menki (niekingi) ... prieš tai mes sunaikinome lenkų kultūrą, dabar pasiryžę sunaikinti rusų, o jei pasisektų, tai sunaikintumėm ir bendražmogiškąją kultūrą“, — rašo garsus Ukrainos rašytojas, etnografas ir filologas P.Kuliš savo laiške Galicijos ukrainofilui L.Barvickui. „Mes“ — tai ukrainofilai, ukrainietiško nacionalinio judėjimo veikėjai. Panteleimon Kuliš buvo vienas aktyviausių ukrainofilų: jis sukųrė ukrainietišką abėcėlę – „kulišovką“. Kartu su Tarasu Ševčenka, Nikolajumi Kostomarovu ir Michailu Gruševskiu jį galima pavadinti vienu iš Ukrainos tėvų-steigėjų. Ukrainos kaip atskiros valstybės, sukurtos ypatingos tautos.

Ukrainofilų judėjime Kuliš galiausiai tapo svetimu tarp savų. Nuo „kulišovkos“ sudarytojo, nuo kurios prasidėjo rašytinė ukrainietiška kalba, nusisuko beveik visi jo bendraminčiai: tai atsitiko po to, kai rašytojas ir mokslininkas parašė trijų tomų „Rusijos susijungimo istoriją“.

Apie archajišką, barbarišką ukrainizmo esmę pareiškė vienas pagrindinių ukrainietiško nacionalinio judėjimo ideologų! Ir ne jis vienas: daugelis ukrainietiško judėjimo dalyvių, priklausančių XIX amžiaus nacionalinei inteligentijai, parodo suvokimą, kad jų veiklos esmė — tai išskyrimas iš Mažosios Rusijos vietinių etnografinių ypatumų naujos kultūros, kuri būtų nukreipta prieš visą bendražmogiškąją kultūrą ir svarbiausia prieš rusų kultūrą.

„Besisukant bendrarusiškų protinių ir politinių interesų aplinkoje, gyvenant rusų literatūros, kurioje be galo daug bendrarusiško ir bendražmogiško turinio temų, turtu, Mažosios Rusijos inteligentija, kaip vaizdžiai išsireiškė profesorius-ukrainofilas, priversta taip sakant nusilenkti, kad įeiti į žemą provincinės ukrainietiškos literatūros priemenę“, — rašo Rusijos mokslininkas ir publicistas Sergej Ščiogolev knygoje „Šiuolaikinis ukrainizmas“ (1914 metai). Ne pas priešininkus, bet pas šalininkus „mazepos“ ideologijos Ščiogolev randa teigimus, kad iš milijonų tamsių nemokšiškų pietų Rusijos valstiečių naują tautą bando sukurti nuo gyvenimo atitolusių humanitarų saujelė — nacional-romantikų: „Žurnalas „Ukr. Chata“ prieš tris metus atviravo, kad ukrainietiška tauta susideda iš 30 milijonų vergų (sic) ir Don Kichotų saujelės“.

Šiuolaikinėje Ukrainoje nepopuliaru kalbėti apie ukrainiečius-valdovus ir Rusijos bendravaldovus: pradedant broliais Razumovskiais ir baigiant Chruščiovu bei Brežnevu. Kaip galėjo ukrainiečiai valdyti metropoliją, jei Ukraina, anot dabartinės ideologijos, visada buvo kolonija, o dabar kovoja su kaimyno „imperiškomis ambicijomis“? Analogiškas klausimas ir dėl literatūros: visas ukrainizmas remiasi Taraso Ševčenkos kultu, kuris rašė eiles gimtaja kalba, tuo metu kai tokie vardai kaip Gogol, Korolenka ir ypač Bulgakov, kuris šaipėsi iš ukrainietiško judėjimo gyvenime ir knygose, visiškai užmiršti. Užmiršti fizikai, inžinieriai-konstruktoriai, kosmonautai, kurie dirbo Ukrainoje tarybiniais laikais: juk jie stūmė žmoniją į priekį bendro su rusais tarybinio projekto rėmuose. Užtat Viačeslav Černovol ir Leonid Kravčuk, kurie žmonijai nepadarė nieko, bet vadovavo judėjimui už Ukrainos išstojimą iš TSRS — dabar tai moraliniai kamertonai, ukrainietiškos tautos sąžinė.

Prieš šimtą metų, kai formavosi ukrainizmas, tai buvo taip pat aišku ir taip pat suglumindavo gebančius mąstyti bendralaikius, kaip ir dabar. „Rusų kultūros kūrime Kijevo Rusė dalyvavo ne mažiau už šiauriečius“, sakė 1913 metais Maksim Gorkij, nustebintas ukrainietiško separatistinio judėjimo, kurio dalyviai atsisako patys savęs.

Vėl gi, ši archaizacija ir degradavimas buvo išpranašautas dar prieš šimtą metų. „Savo vidiniu turiniu ukrainietiškas judėjimas visai ne progresyvus; jis tik opozicinis valstybiniai Rusijos vienybei ir priešiškas rusų kultūrai, o todėl neišvengiamas Ukrainos likimas — pastovi opozicija Rusijos vyriausybei, kol egzistuoja Rusija kaip vieningas vienetas, — rašo Sergej Ščiogolev. — Ukrainofilų tvarkymasis užlaikytų Pietų Rusijos kultūrinį ekonominį vystymąsi dešimtmečiams ir pietvakarių kraštui būtų daug kartų blogesnis už polonizaciją“.

Būtent tai ir vyksta dabar šiuolaikinės Ukrainos ekonomikoje.

Lai vietoj viso to bus vienkiemis. Su molio trobele, saulėgrąžomis, svogūnais, kiaulėmis bei vištomis. Su Taraso Ševčenkos portretu rankšluostyje ir geltona-žydra vėliava ant stogo.

Būtų ne taip baisu, jei ši archaizacija liestų tik ekonomiką ir socialinę infrastruktūrą. Iš ties baugina tai, kad nauja barbarybė liečia santykius tarp žmonių. O juk vėl gi iš šimto metų senumo ukrainietiškos publicistikos galima buvo suprasti, kad taip ir bus. „Jei pas mus kalbama apie Ukrainą, mes privalome naudoti vieną žodį — neapykanta jos priešams. Ukrainos atgimimas — neapykantos savo žmonai „moskovkai“, savo vaikams kacapams, savo tėvui ir motinai kacapams sinonimas. Mylėti Ukrainą — reiškia paaukoti savo kacapišką giminę“, — rašė žurnalas „Ukrajinskaja chata“ 1913 metais. Būtent tai dabar ir vyksta: kiek buvo pasakojimų apie tai, kaip Kijevo sūnus atsisakė Donecko motinos, kadangi ji buvo „vatnikė“, palaikiusi „separus“?

„Skaitant ukrainietišką spaudą, matosi, kad ukrainietiškos partijos šalininkai laiko neapykantą visam „rusiškam“ nuvalkiota, vaikščiojančia morale“, — rašė Sergej Ščiogolev 1914 metais. Belieka pridurti: skaitant dabartinę ukrainietišką spaudą, galima pamatyti tą patį. Neapykanta degina žmones Odesoje, neapykanta verčia kariauti Donbase, neapykanta — tai tas kuras, kurio varomas veikia ukrainietiškas nacionalizmas.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 18 — id: `scraped:rubaltic_lt:db5e03558f13e700`

**Title:** Kaip kūrėsi ukrainizmas?

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Ukrainietiškas nacionalizmas gimė ne Maidane ir net ne Ukrainos sukilėlių armijoje. Šio reiškinio ištakos – XIX amžiaus ukrainietiškame nacionaliniame judėjime, kuriam lemiantį palaikymą skyrė Austrijos imperija, pavertusi jai priklausančią Galičiną „ukrainietišku Pjemontu“. Išorinis ukrainietiško judėjimo palaikymas buvo reikalingas Rusijai susilpninti dirbtino pietinių Rusijos gubernijų gyventojų išskyrimo iš rusų tautos ir naujos, rusams priešiškos etninės grupės sukūrimo – ukrainiečių – būdu. Todėl ukrainietiškas nacionalizmas buvo palaikomas Vakaruose prieš šimtą metų, todėl palaikomas ir dabar.

„Rašytojas Dmitro Doncov savo kalboje Lvovo studentų suvažiavime šių metų birželio mėnesį, ragindamas Ukrainos studentus palaikyti politinį separatizmą Ukrainoje, išreiškia karštą palinkėjimą, kad „didinguose Lenkijos ir pasaulio reikšmės judėjimuose Lenkijos ir Ukrainos vėliavos būtų kartu“, - 1914 metais rašė Kijeve rusų mokslininkas Sergej Ščiogolev. – Išleistoje šį pavasarį brošiūroje p. Doncov įrodo, kad augančiajai Mažosios Rusijos inteligentijos kartai (Rusijoje) labiau prireiktų Mickevičiaus kūriniai, negu, pavyzdžiui, Puškino „Poltava“ ar „Rusijos šmeižikams“.

1926 metais Dmitrij Doncov išleis pagrindinę savo gyvenimo knygą – „Nacionalizmas“, kurioje bus aprašyti visi esminiai ukrainietiško integralinio nacionalizmo pagrindai, paprasčiau kalbant – ukrainietiško nacizmo.

„Pavergėjais“ vadinami išskirtinai „moskaliai“, kurių imperija yra Auksinės Ordos įpėdinė, o patys jie yra mongolo totorių ir finougrų mišinys, kuriuose neliko nei lašo rytų slavų. Tuo pačiu ukrainiečiai – tai tikrų tikriausi grynakraujai slavai, o riba tarp civilizuotos Europos ir Azijos stepių praeina kaip tik per Ukrainos rytinę sieną.

Doncovo knyga tapo ideologiniu ukrainietiškų nacionalistų judėjimo pagrindu. Pats Doncov buvo etatinis UNO – Ukrainietiškų nacionalistų organizacijos, kuriai vadovavo Jevgenij Konovalcev, Andrej Melnyk ir Stepan Bandera, ideologas. Antrojo pasaulinio karo metais UNO pagrindu buvo įkurta USA, kuri kovoje už ukrainietišką nacionalinę valstybę pasižymėjo bendradarbiavimu su Hitlerio kariuomene, rusų, žydų bei lenkų sunaikinimu. Šiandien USA smogikus Ukrainos valdžia gerbia kaip didvyrius, o rasistinės Doncovo idėjos apie „grynakraujus ukrainiečius“ ir „finų-mongolų kacapus“ atranda platų gerbėjų ratą Ukrainos visuomenėje.

Tai įrodo šiandien pamiršto mokslininko Sergejaus Ščiogolevo knygos. Neetatinis ypatingų reikalų Kijevo gubernatoriaus valdininkas Ščiogolev tyrė „ukrainietišką klausimą“, kuris XX amžiaus pradžios Rusijos imperijoje reiškė separatistines tendencijas Mažosios Rusijos gubernijose. Šiai problemai skirtos dvi Ščiogolevo knygos: „Ukrainietiškas judėjimas kaip šiuolaikinis Mažosios Rusijos separatizmo etapas“ (1912 metų) ir „Šiuolaikinis ukrainizmas, jo kilmė, augimas ir uždaviniai“. Šiose knygose Ščiogolev remiasi pirmiausiai Austrijos šaltiniais, prie kurių jis kaip cenzorius turėjo prieigą. Šie šaltiniai įrodo, kad taip vadinamo ukrainietiško judėjimo atsiradimas susijęs su Austro-Vengrijos baime dėl prorusiškų nuotaikų Lvovo srityje. Iš to kilo idėjos, kad ukrainiečiai – ypatinga tauta, neturinti nieko bendro su rusais, piršimas, kuris buvo vykdomas Austro-Vengrijai atitekusiose Kijevo Rusios žemėse.

„Austrijos vyriausybė tikisi dirbtino ukrainietiško judėjimo sukilimo Galicijoje būdu iššaukti pietinėje Rusijoje nacionalinį ukrainietišką separatizmą ir reikalui esant sukelti ten net revoliucinius sunkumus“, - cituoja Sergej Ščiogolev telegramą iš Vienos Lvovo uniatų mitropolitui Andrejui Šeptickiui.

„Puikioji Viena“ finansiškai ir administratyviai skatino veiklą tokių ukrainietiško nacionalinio judėjimo aktyvistų, kaip Dmitrij Doncov, kad didžiojo karo išvakarėse suskaldyti rusų tautą į dvi dalis. Austrijos valdžia buvo taktinis sąjungininkas ukrainietiškos nacionalinės inteligentijos, kuri tikėjosi trimis etapais pasiekti autonomijos nuo Sankt-Peterburgo: iš pradžių kultūrinės pietinės Rusijos gubernijų autonomijos, kuriose buvo planuojama suteikti naujai dirbtinai kalbai, sukurtai iš vietinių dialektų, oficialų statusą; vėliau – ekonominės autonomijos su teise pasilikti mokesčius savo vietovėse; pagaliau, politinės autonomijos nuo Rusijos imperijos. Tai buvo vyresniosios ukrainofilų kartos doktrina, tarp kurių poetas Taras Ševčenka, istorikas Nikolaj Kostomarov, etnografas Panteleimon Kuliš (Kirilo-Mefodijaus brolija). Jaunesnioji karta, kuriai priklauso Ščiogolevo bendralaikiai Michail Gruševskij, Dmitrij Doncov ir Jevgenij Konovalec, pareikalaus jau nepriklausomos ukrainietiškos valstybės sukūrimo. Ukraina – aukščiau už viską!

Tuo pačiu dar „Šiuolaikiniame ukrainizme“ (1914 m.) įrodyta, kad ukrainietiškas separatistinis judėjimas Rusijoje yra marginalinis, dar daugiau – kvailas. Autorius pateikia pavyzdžius: folkloro šventėje Charkove ukrainietiško judėjimo aktyvistai raštuotais marškiniais nemokėjo suformuluoti savo minčių ukrainiečių kalba ir kalbėjo rusiškai. Viensėdininkai Poltavo srityje nesuprato „tautos dvasios žadintojų“, kurie kreipėsi į juos „gimtaja kalba“, ir klausė, kokia kalba jie kalbėjo.

Tai pabrėžia ne tik Sergej Ščiogolev, bei ir šiuolaikiniai vakarų autoriai. „Jei po Vienos Kongreso Rusijos imperija gautų Rytų Galiciją ar net okupuotų ją 1878 metais Balkanų krizės metu, ukrainietiškas žaidimas būtų baigtas ne tik Galicijoje, bet ir visoje Ukrainoje virš Dnepro“, - rašo ukrainiečių kilmės Amerikos istorikas John-Paul Himka.

Šiame išorinio centro ukrainietiškame nacionalizme suinteresotume – pati ryškiausia analogija su šiandiena. Juk šiandieninis ukrainietiškas nacionalizmas taip pat apgailėtinas ir kvailas: Dnepropetrovsko išeiviai Aukščiausioje Radoje, kurie nesugeba išdėstyti savo minčių ukrainiečių kalba, todėl kalba rusiškai; civiliai aktyvistai raštuotais marškiniais, kurie bėga į Rusiją bei Baltarusiją nuo šaukimo į karo laukus. Bet nepaisant viso to, idėjiniai Doncovo, Banderos ir Šuchevičiaus įpėdiniai jau pusantrų metų sunkiai, bet išsilaiko valdžioje. Nes jų ideologija išskirtinai priešiška Rusijai, todėl ji vėl įdomi vakarų išoriniams žaidėjams. Šimtas metų praėjo – niekas nepasikeitė.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 19 — id: `scraped:rubaltic_lt:c4ea35b170453da3`

**Title:** Lenkai ir AES: ko Lietuva galėtų pasimokyti iš Baltarusijos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Baltarusijos vakaruose tęsiama Ostrovecko AES statyba, kurios pagalba Baltarusija taps branduoline valstybe. Bet neskaitant šios užduoties Ostrovecko AES išsprendžia dar vieną: įdarbinimas atominėje stotyje arba jos infrastruktūros aptarnavimas leis galutinai integruoti gyvenančius AES statybos rajone baltarusiškus lenkus, visiems laikams pavertus juos Baltarusijos patriotais. Šioje istorijoje pasireiškia labai ryškus kontrastas tarp Minsko ir Vilniaus: Lietuva savo branduolinės valstybės statusą sunaikino, uždarius savo atominę stotį ir nepastačius naujos, o Lietuvos lenkus "integruoja" sunaikindama lenkiškas mokyklas, uždrausdama lenkišką toponimiką ir spręsdama teismuose teisingą lenkiškų vardų rašybą.

Buvusios Žeč Pospolitos teritorijos, kurios sudarė tarpukario Lenkiją, bet kurias ji prarado po Antrojo pasaulinio karo, lenkų kalba vadinasi rytų Kresai. Į rytų Kresus įėjo Galičina ir Volynė Ukrainos vakaruose, Vakarų Baltarusija ir Vilniaus kraštas (Lietuva). Ir jei Volynėje bei Galičinoje beveik visus lenkus sunaikino Banderos tarnai, Baltarusijoje ir Lietuvoje iki šiol kompaktiškai gyvena lenkų bendrijos.

Anot paskutinio surašymo Baltarusijoje lenkais save įvardino 3 gyventojų procentai. Dauguma Kresų gyventojų gyvena Gardino srityje Baltarusijos ir Lenkijos pasienyje, kur lenkai sudaro beveik ketvirtį gyventojų. Baltarusiškų lenkų skaičius pokario metais nuolat mažėjo: jie asimiliavo ir persikraustė gyventi į didmiesčius.

Skandalai, susiję su baltarusiškais lenkais, ne vieną dešimtmetį buvo pagrindinis Minsko ir Varšuvos santykių žymeklis. Lenkija kaltino Baltarusiją tautinės mažumos diskriminacija, lenkų visuomeninių bei kultūrinių organizacijų persekiojimu. Atsakydamas į tai, Baltarusijos prezidentas Aleksandr Lukašenka demonstratyviai pradėdavo savo priešrinkimines keliones nuo Gardino srities, kur susitikdavo su lenkų tautybės rinkėjais.

Tačiau Minske negalėjo neigti didžiosios lenkų bendrijos dalies nelojalumą Baltarusijos valstybei, nors ir aiškino šį nelojalumą išskirtinai Varšuvos specialiųjų tarnybų griaunamaja veikla, kurios formuodavo lenkų bendrijoje priešvalstybines nuotaikas, o taip pat Baltarusijoje transliuojamos lenkų žiniasklaidos (kad ir telekanalas „Belsat“).

Tuo įdomiau, kokiais būdais kresus, greičiausiai, pavyks paversti Baltarusijos patriotais.

Be abejo, atominė stotis Baltarusijoje statoma ne vietinių lenkų vardan. Baltarusija nusprendė tapti branduoline valstybe, ir ji jau arti branduolinio statuso gavimo. Tačiau be pagrindinio tikslo yra ir šalutinis (bet taip pat ilgalaikis ir strateginis) – pasiekti baltarusiškų lenkų lojalumo. Nykios vakarų Baltarusijos provincijos gyventojai turės galimybę aptarnauti supermodernios valstybinės įmonės darbą – tai nepalyginamos, negu buvo šiame regione iki šiol, algos ir visiškai kitas socialinis statusas. Pats regionas atominės stoties statybos dėka jau padarė savo vystymosi šuolį.

AES ir lenkai – tai dvi temos, kurios taip pat aktualios ir Lietuvai. Ir čia lyginant Lietuvos ir Baltarusijos patirtį pasireiškia veidrodžio principas: dvi šalys sprendžia vienodus, strategiškai svarbius klausimus visiškai priešingu būdu.

Todėl ir kyla klausimas, kas iš šių dviejų "apsišvietusi Europa" o kas "atsilikęs sovokas"? Iki šiol dešimtmečiais lietuviai manė, kad tikri europiečiai – jie, o baltarusiai – tikrų tikriausi sovokai. Bet šiandien kokią sferą bepaimtumėm – lyginant šias dvi šalis šis įsitikinimas kelia abejonių. Sankcijų prispausta "atsilikusi" Baltarusija jau tiekia Vakarų Europai savo pramoninę produkciją . Europos Sąjungos ir NATO narė "progresyvi" Lietuva tiekia ten gastarbaiterius – juodadarbius. Lietuva prarado savo branduolinę energetiką, Baltarusija ją sukūrė. Lietuvoje tautinių mažumų integracijai nesumąstė nieko protingesnio už represijas, Baltarusijoje nacionalinė politika organiškai įtraukta į kompleksinę šalies vystymo programą, ir visuomenės integracijos labui veikia didelių infrastruktūrinių projektų realizavimas. Ir kas tada tikroji Europa?

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 20 — id: `scraped:rubaltic_lt:6ca5dae5f82be806`

**Title:** Lietuvių netenkina jų "demokratija"

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Absoliuti Lietuvos gyventojų dauguma nepatenkinta Lietuvos demokratijos veikimu. Tai nenuostabu: sunku būti patenkintam tuo, ko nėra. Atstovaujančios demokratijos esmė tame, kad politikai išreiškia juos išrinkusių piliečių interesus. Lietuvoje gi politinė klasė ir tauta gyvena skirtinguose pasauliuose, ir vietoj to, kad atstovauti savo rinkėjų interesams, Lietuvos politikai jiems tik kenkia.

Paskutinių parlamento rinkimų metu juose laimėję social-demokratai žadėjo elektoratui pirmiausia vykdyti socialiai orientuotą politiką. O taip pat neužsiimti beprotiškais geopolitiniais oponentų konservatorių prožektais, o susitaikyti su kaimynais, „perkrovus“ santykius su Rusija, Lenkija ir Baltarusija. O taip pat atsisakyti Visagino AES statybos.

Iš visų pažadų pavyko įgyvendinti tik paskutinį, ir tai ne todėl, kad social-demokratai pasistengė, o todėl, kad nebuvo nei pinigų, nei sponsorių AES statybai. O šiaip social-demokratai buvo pasiruošę atsisakyti rinkėjams duotų pažadų: sakė, kad referendumas dėl AES buvo tik patariamojo pobūdžio, kad galutinai dar sprendimas nepriimtas.

Kituose klausimuose elektoratą iš tikrųjų „apgavo ir metė“. Social-demokratų užsienio politikoje neatsirado nieko, kas skirtųsi nuo konservatorių bruožų. Lietuvos lenkų teisės pastoviai pažeidžiamos ir dėl to santykiai su Varšuva lieka stabiliai blogi. Su Baltarusija politinio dialogo nebuvo ir nėra. Santykiai su Rusija iš vis atrodo kaip tikras chtoniškas siaubas.

Kalbant apie vidaus politiką, tai social-demokratams esant valdžioje Lietuva netapo socialiai orientuota valstybe.

Pažiūrėkime į kitą valdžios centrą Lietuvoje – prezidentą. Praeitų prezidento rinkimų metu Dalia Grybauskaitė žadėjo elektoratui padidinti minimalią pensiją iki 650 litų ir grąžinti ligos pašalpos išmokas. Po netriumfalinio, bet vis gi perrinkimo – prezidentė Grybauskaitė savo pirmuoju sprendimu nurodė pažadėtus socialinėms išmokoms skirtus pinigus išleisti karinio biudžeto didinimui. Kriminaline terminologija toks politinis metodas vadinasi „metimas“.

Ką jau bekalbėti apie kandidatės į Lietuvos prezidentus Dalios Grybauskaitės pažadus 2009 metais. Tada neseniai buvusi ES komisarė finansams ir biudžetui žadėjo per trumpiausią laiką įveikti ekonominę krizę, ypatingą dėmesį skirti nepasiturintiems gyventojų sluoksniams, užsienio politikoje vadovautis išskirtinai tautos interesais, santykius su kaimynais, tame tarpe ir Rusija, konstruoti pragmatiniu pagrindu. Realybėje visais prezidentavimo metais Grybauskaitei nerūpi nei ekonomika, nei nepasiturintys gyventojų sluoksniai, nei pragmatiniai santykiai su kaimynais. Ją domina šalių vadovų susitikimas Vilniuje, „Rytų partnerystė“, „teroristinė valstybė“, ginklų tiekimas – Ukrainai, „demokratijos eksportas“ – Gruzijai, Moldavijai ir Baltarusijai. Bet kas, kad ir kelionė į Kroatiją kovai su Rusijos energetiką Adriatikoje, bet tik ne tai, kuo Grybauskaitė žadėjo užsiimti rinkimų metu.

Paprasto lietuvio interesas – gyventi mažoje švarioje europietiškoje šalyje, kuri su niekuo nesibara, tiekia kaimynams savo produkciją ir iš uždirbtų pinigų gerai ir oriai gyvena. Grubiai sakant, jis suinteresuotas, kad Lietuvos vežėjai nestovėtų paromis pasienyje ir lietuviška varškė bei grietinė laiku patekdavo į kaimyninių valstybių hipermarketus. Kad veiktų lengvatiniai prekybos režimai, valstybės eksportuotojų paramos programa, investicijų pritraukimo programa. Galiausiai – kad Lietuvoje būtų darbas ir nereikėtų iš čia išvažiuoti.

Lietuvos politinės klasės interesas – jausti save Jagelonių bei Lietuvos Didžiosios Kunigaikštystės palikuoniais. „Sulaikyti Rusiją“ Europos Sąjungoje ir potarybinėje erdvėje. Būti ištikimiausiais JAV sąjungininkais: „kuo daugiau Europoje bus Amerikos, tuo mažiau Europoje bus Rusijos“. Skleisti „Rytų partnerystės“ šalyse demokratijos bei europietiškų vertybių, kurių jie patys nesilaiko, šviesą. Tuo pačiu gyventi iš Briuselio dotacijų ir išradinėti naujus projektus, kurių pagrindu būtų galima paprašyti ES fondų papildomo finansavimo.

Kaip rodo sociologinė apklausa, kurią atliko ELTA užsakymu Baltijos tyrimų kompanija, šių metų liepos mėnesį 51 procentas lietuvių nebuvo patenkinti demokratijos veikimu Lietuvoje. Pastaraisiais metais šis skaičius svyravo tai į vieną, tai į kitą pusę, bet ženkliai nepasikeitė: absoliuti lietuvių dauguma chroniškai nepatenkinta demokratija savo šalyje. Iš tikrųjų, kaip galima būti patenkintiems tuo, ko nėra?

Lietuvos respublika – pirmoji šalis Europoje, pasinaudojusi impičmentu, nes buvo išrinktas „neteisingas“ prezidentas. Kai reikėjo išrinkti „teisingą“ prezidentą, atsitiko labai blogai kvepiantis 2004 metų įvykis: iš pradžių balsų skaičiavimo metu rinkimuose laimėdavo „neteisingas“ kandidatas, o po to „sutriko“ elektroninio balsavimo sistema, ir po kompiuterių perkrovimo paaiškėjo, kad rinkimus laimėjo „teisingas“. Pasitikėjimo politiniais institutais reitingai tarp Lietuvos gyventojų lieka kritiškai žemi. Kalbant apie politiką, savo valdančiąją klasę šie gyventojai vadina vagių įstatyme susirinkimu. Valdančioji klasė atsilygina gyventojams tuo pačiu – siaurame elito rate tautą vadina burokais: raudonais iš išorės, „galvijais“ ir „sovokais“, kurie sielos gylumoje nesuvokia europietiško pasirinkimo ir demokratijos malonumų ir teigia, kad tarybiniais laikais jie gyveno geriau. Kas nors pastebi tokiuose „aukštuose“ santykiuose demokratiją?

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```
