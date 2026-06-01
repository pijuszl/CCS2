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

### Article 1 — id: `scraped:rubaltic_lt:272856d531fd85fc`

**Title:** Lietuva išsigando RuBaltic.Ru tarptautinio aktyvumo

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos Valstybės saugumo departamentas paskelbė kasmetinę respublikos nacionalinio saugumo grėsmių ataskaitą. Tradicinį išmislų paradą ir paranojos triumfą šį kartą papildo Rusijos pilietinės visuomenės aktyvumo baimė. Lietuvos valdžios išsigando RuBaltic.Ru akcijos ginant Jurijų Melį ir kitas „sausio 13-osios bylos“ politinių persekiojimų aukas. Vilniuj akivaizdžiai nepriprasta, kad žmogaus teisių pažeidimais ne Lietuva kaltina Rusiją, o Rusija Lietuvą, ir tuo užsiima ne valstybė, o žmonės.

„Kremliaus propagandos skleidimą lydėjo bauginimas, juo siekta paveikti bylos tyrėjus ir teisėjus. Rusijos valdžios atstovai nedviprasmiškai viešai teigė, kad Lietuvos teismo paskelbto nuosprendžio Sausio 13-osios byloje nepaliks be atsako. Lietuvoje vykstančius teisinius procesus buvo siekiama diskredituoti tarptautinės bendruomenės akyse. 2019 m. vasario 20 d. Briuselyje, Europos Parlamento pastate, organizuotame renginyje buvo pristatytas agresyvią Rusijos propagandą skleidžiančio informacinio-analitinio portalo rubaltic.ru tyrimas apie politines represijas Baltijos šalyse. Didžioji jo dali skirta Sausio 13-osios bylai. Dar vėliau Kremliaus agresyvią užsienio ir vidaus politiką palaikančios Rusijos nevyriausybinės organizacijos kreipėsi į ESBO ragindamos atkreipti dėmesį į Lietuvoje tariamai vykdomą politinį persekiojimą”, —teigiama 2019 metų Lietuvos Valstybės saugumo departamento nacionalinio saugumo grėsmių ataskaitoje.

Čia turima omeny pranešimą „Politinės represijos Pabaltijyje. Baudžiamoji justicija sergėjant Lietuvos, Latvijos ir Estijos politinius režimus“, kurį RuBaltic.Ru išties pristatė Europos parlamente, o dar ir ESBO. O dar JT, ką budrios Lietuvos specialiosios tarnybos, sprendžiant iš jų paskvilio, pražiopsojo.

Šiose tarptautinėse organizacijose oficialų Vilnių atstovaujantys asmenys dalyvavo RuBaltic.Ru pristatymuose ir net keletą kartų bandė mums prieštarauti. Visa tai atrodė, tiesą sakant, apgailėtinai.

Tai jie ten 30 metų lakštingalomis suokė apie „sovietinę okupaciją“, Molotovo–Rybentropo paktą ir Rusijos opoziciją. O kai tose tarptautinėse erdvėse Rusijos visuomenininkai ir žurnalistai ėmė kalbėti apie disidentų ir politinių kalinių Lietuvoje persekiojimą, jos atstovai patyrė šoką ir todėl elgėsi tiesiog kvailai.

Pavyzdžiui, Lietuvos atstovė Europos parlamente leptelėjo, jog kažkaip keista kalbėti apie kažkokius 2-3 kitaminčių Lietuvoje persekiojimus po kančių 130 tūkstančių lietuvių, kuriuos Stalinas ištrėmė į Sibirą. Tai yra, klykiant apie tai, kaip „Kremliaus propaganda šmeižia“ europietišką demokratinę respubliką, kitaminčių persekiojimas Lietuvoje lyg ir neneigiamas.

Dar toliau nukeliavo Lietuvos atstovė ESBO, ryžtingai pareiškusi, kad Rusijos nekomercinių organizacijų skleidžiamas melas — tiesa, ir Lietuvoje tikrai ribojama žodžio laisvė kai kuriomis istorinėmis temomis. Kam nepatinka jų teisių apribojimas, lai kreipiasi į teismą.

Taigi nenuostabu, jog Lietuvos oficialiems veikėjams nepasiruošus atremti smūgį ir nesugebant prieštarauti dėl pateiktų faktų, RuBaltic.Ru tarptautinį aktyvumą VSD pripažino grėsme nacionaliniam saugumui.

„Asmenys, prisilaikantys radikalių pažiūrų ir veikiantys Kremliaus interesais, organizavo Lietuvoje ir užsienyje šalies „politinių kalinių“ palaikymo akcijas. Peticijos, straipsniai, vaizdo įrašai, nukreipti prieš tariamą politinį persekiojimą, buvo aktyviai platinami internete, ypač populiariausiuose socialiniuose tinkluose“, — rašo VSD.

Taip Lietuvos specialiosios tarnybos savo paukščių kalba pasakoja apie RuBaltic.Ru Jurijaus Melio palaikymo akciją — palaikymo sunkiai sergančio Rusijos karininko, kurį Lietuvos valdžios nutarė paversti „kraštutiniu“ byloje dėl žmonių žūties prie Vilniaus televizijos bokšto ir skyrė 7 laisvės atėmimo metus pagal straipsnį „kariniai nusikaltimai ir nusikaltimai žmoniškumui“ už tai, kad Melis švietė tanko žibintais ir triskart iš patrankos šovė tuščiomis į orą.

Vaizdo kreipimaisi į Jurijų Melį, linkint jam sveikatos, sielos jėgų ir ištvermės, kai tarp autorių buvo Valstybės dūmos ir Europos parlamento deputatų bei eilinių kaliningradiečių — nė už ką persekiojamo karininko žemiečių, buvo įrašyti RuBaltic.Ru paraginus. Tai iš esmės buvo liaudies akcija, kurioje savo poziciją Lietuvos veiksmų atžvilgiu pademonstravo ne Rusijos URM, o vietos gyventojai.

Lietuvos valdžių užgaidas akivaizdžiai nekalto žmogaus atžvilgiu sutelkė tą Rusijos pilietinę visuomenę, prie kurios Vilnius priskyrė tuos „laisvės mylėtojus“, kuriuos tos pačios Lietuvos specialiosios tarnybos kartą pusmetyje suveža į Laisvos Rusijos forumą. To išdavoje pilietinė iniciatyva Lietuvos grėsmių sąraše atsidūrė greta Baltijos karinio jūrų laivyno karinio potencialo stiprinimo.

Ne veltui šioje VSD ataskaitoje atskiras skyrius skirtas Rusijos eksperimentui su nemokamomis elektroninėmis vizomis. Lietuviams, žinoma, kategoriškai nerekomenduojama lankytis Kaliningrado srityje ir kituose RF regionuose pagal supaprastintą vizų režimo programą. Ko čia abejoti — juk elektroninių vizų dėka lietuviai pamatys tikrąją Rusiją, o ne tą, kurią jiems sugalvojo valdžia.

Lietuvos valdančiajam režimui ta Rusija, kurią jis išsigalvojo ir kuria jis gąsdina visus Lietuvoje ir už jos ribų, būtų daug saugesnė ir naudingesnė, nei tikroji Rusija. Nuo viso pasaulio izoliuota, atsilikusi, purvina, gyvenanti svajonėmis apie agresijas ir aneksijas; tokia Rusija pateisintų režimo, sukurto ant rusofobijos pamatų, egzistavimą. Į tokią Rusiją pačios Lietuvos valdžios organizuotų demo-išvykas.

Grėsmių Lietuvos ir lietuvių saugumui dėl kaimynystės su Rusija nėra jokių. O štai Lietuvos valdžioms, pagal kurių interesus sukurptas VSD pranešimas, iškyla didžiulė rizika.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 2 — id: `scraped:rubaltic_lt:b8e34fcf0f7e4b8c`

**Title:** Molotovo-Ribentropo paktas ir Lietuvos „sovietų okupacija“ nesusisieja

**Source:** rubaltic_lt (propaganda)

**Text:**

```
: Lietuvos prezidentas Gitanas Nausėda savo neseniai padarytame pareiškime dėl Rusijos pastangų perrašyti Antrojo Pasaulinio karo istoriją priminė apie 1989 metų 2-ojo TSRS Liaudies deputatų suvažiavimo nutarymą, kuriame Molotovo-Ribentropo paktas buvo pasmerktas. Tuo tarpu šitas nutarymas buvo priimtas politiniais tikslais ir prieštaravo ir istorijos faktams, ir pagrindinėms istorijos mokslo taisyklėms. Būtent Lietuva Sovietų Sąjungos ir Vokietijos „įtakos sferų“ sutartyse minima ne Molotovo-Ribentropo pakte, bet visai kituose dokumentuose, tad 1939 metų rugpjūčio 29 dienos nepuolimo sutartis jokiu būdu nelėmė Baltijos „sovietų okupaciją“.

2-ojo TSRS Liaudies deputatų suvažiavimo nutarymas dėl Molotovo-Ribentropo pakto vertas atskiro vertinimo, nes iki šiol yra naudojamas Rusijos priešų spekuliacijoms. Žinoma, kad pakto teisės ir istorijos atžvilgiu abejotinas vertinimas Baltijos Tarybų Socialistinių Respublikų buvo laikomas pseudoteisiniu pagrindu išstoti iš TSRS.

Nuostabiausia yra tai, kad lietuvių separatistai, 26 metus manipuliuodami paktu kaip pagrindiniu TSRS įrankiu Lietuvos įtraukimui į Sovietų Sąjungą, taip ir nesuvokė pakto esmę. Rusijoje to irgi nepastebėjo.

Esmingiausias reikalas yra tame, kad Lietuva buvo įtraukta į TSRS įtakos sferą pagal slaptą papildomą Sovietų Sąjungos ir Vokietijos sutarties protokolą, pasirašytą 1939 metų rugsėjo 28 dieną, o ne 1939 metų rugpjūčio 23 dieną.

Lietuvos Generalinės prokuratūros tardymo grupės paruoštame ir teismui pateiktame kaltinamajame akte jau buvo frazė: „...Lietuvos kaip nepriklausomos valstybės lemtis buvo nuspręsta sutartyse tarp TSRS ir Vokietijos, pasirašytose 1939 metų rugpjūčio 23 ir rugsėjo 28 dienomis ir vadinamose Molotovo-Ribentropo paktu...“.

Tuo tarpu viešai žinoma, kad Molotovo-Ribentropo paktu vadinama tiktai nepuolimo sutartis pasirašyta tarp TSRS ir Vokietijos 1939 metų rugpjūčio 23 dieną, bei slaptas tos sutarties protokolas.

Tai tvirtina ir tas faktas, kad 2-asis TSRS Liaudies deputatų suvažiavimas, kuriame dalyvavo ir Lietuvos TSR liaudies deputatai, 1989 metų gruodžio 24 dieną paskelbė konkrečiai 1939 metų rugpjūčio 23 dieną pasirašytos vokiečių ir sovietų nepuolimo sutarties ir jos slapto protokolo politinį ir teisinį įvertinimą.

Po beveik tris dešimtmečius po Suvažiavimo lietuvių politikai su siaubu suprato, kad ir valstybė, ir Europa mini datą, kuri neturi nieko bendro su Lietuvos įtraukimu į TSRS įtakos sferą.

Pripažinti savo klaidą jie nenorėjo, tad sugalvojo „raguotą“ kiškį, pavadinę abidvi vokiečių ir sovietų sutartis Molotovo-Ribentropo paktu.

Toks Rusijos priešų vartotojiškas požiūris į svarbiausią dokumentą nulemtas tuo, kad šalies oficialūs istorikai skiria nepakankamai dėmesio manipuliacijoms su istoriniais šaltiniais.

Toks 2-ojo TSRS Liaudies deputatų suvažiavimo pakto įvertinimo nuostolingumas buvo nulemtas tuo, kad deputatų komisija paruošusi nutarimo projektą, atsižvelgdavo į „per se“ principą.

Pasak šį principą pakto pasirašymo sprendimas buvo nagrinėjamas neatsižvelgiant nei į prieš tai buvę, nei į galimus sekančius įvykius Antrojo Pasaulinio karo išvakarėse. Tai buvo visiškai antiistorinis požiūris, kuris iki šiol negavo atitinkamo įvertinimo.

Taip pat svarbu paminėti, kad TSRS liaudies deputatų grupei, ruošusiai suvažiavimo nutarimo projektą, vadovavo TSKP Centro Komiteto sekretorius Aleksandras Jakovlevas, vėliau pripažinęs, kad jau tuomet jis buvo aršusis antikomunistas.

Jo patys aktyviausi padėjėjai buvo Baltijos respublikų deputatai, kurie sudarė beveik pusę grupės narių.

Jie atgabeno į Maskvą pakto slapto protokolo kopijas (amerikiečių suteiktas), kuriomis manipuliavo lyg sukčiautojai.

Iš tikrųjų Baltijos respublikų deputatai siekė vienintelio tikslo. Jiems reikėjo diskredituoti 1939 metų sovietų ir vokiečių sutartį ir išgauti sutarties pasmerkimą suvažiavimu. Tai suteikė Baltijos respublikoms teisę nuginčyti jų įtraukimo į TSRS teisėtumą.

Iš esmės, per suvažiavimą buvo įvykdyta teisės ir istorijos sąvokų didelio mąsto politinė manipuliacija. Galiausiai, 2-asis TSRS Liaudies deputatų suvažiavimas savo nutarimu pasmerkė 1939 metų rugpjūčio 23 dienos sutartį tarp TSRS ir Vokietijos bei jos slaptą protokolą ir pripažino ją „ negaliojančia nuo jos pasirašymo datos “.

Tuo tarpu nekyla abejonių, kad Molotovo-Ribentropo paktas liovėsi galiojęs, kai Vokietija 1941 metų birželio 22 dieną pradėjo karinius veiksmus prieš TSRS.

Europos pokario pasaulio tvarka buvo įgyvendinama jau besiremiant Jaltos ir Potsdamo sutartimis. Vienintelis 1939 metų rugpjūčio 23 dienos sovietų ir vokiečių pakto likęs reliktas – Vilniaus ir Vilniaus srities priskirimas Lietuvos Respublikai. Bet apie tai nei 2-ojo suvažiavimo metu, nei vėliau niekas neužsiminė.

Viena iš buvusio Lietuvos prezidento Valdo Adamkaus atsisakymo vykti į Maskvą Pergalės 60-mečio minėjimui priežasčių buvo „nepriimtini“ Ribentropo-Molotovo pakto įvertinimai, o taip pat mėginimai „persvarstyti TSRS Liaudies deputatų suvažiavimo nutarimą“, kurie suskambėjo tuometinio Rusijos Federacijos prezidento Vladimiro Putino interviu per Slovakijos radiją 2005 metų vasario 22 dieną.

Iš esmės šiame interviu Putinas tiktai pakartojo Vinstono Čerčilio duotą Ribentropo-Molotovo pakto įvertinimą: „Stalinas buvo priverstas pasirašyti sutartį su Vokietiją po nesėkmingų pastangų rasti šalininkų prieš Hitlerį Vakaruose“.

Tai papiktino buvusį nacių kolaboracionistą Adamkų, kuris, matyt, net nežinojo, jog lygiai taip pat paktą įvertino Čerčilis dar 1948 metais.

Savo požiūrį į paktą daug tiksliau ir detaliau Putinas aprašė straipsnyje „Istorijos puslapiai – motyvas tarpusavio pretenzijoms arba pagrindas susitaikinimui ir partnerystei?“. Straipsnis buvo išspausdintas lenkų laikraštyje Gazeta Wyborcza 2009 metų rugpjūčio 31 dieną, Putino vizito į Gdanską išvakarėse.

Straipsnyje Putinas pažymėjo, kad „šiandien mums siūloma be svarstymų pripažinti, kad vienintele Antrojo Pasaulinio karo pradžios priežastis yra 1939 metų rugpjūčio 23 dienos TSRS ir Vokietijos nepuolimo paktas. Deja šio požiūrio šalininkai neatkreipia dėmesio į paprasčiausius klausimus – argi po Versalio taikos sutarties, kuria pasibaigė Pirmasis pasaulinis karas, neliko „uždelsto veikimo bombų“? Jų pagrindinė – ne vien tik pralaimėjimo skelbimas, bet Vokietijos pažeminimas. Argi valstybinių sienų ribos Europoje nebuvo irstamos daug anksčiau nei 1939 metų rugsėjo 1 dieną?

Ir nebuvo Austrijos anšliuso, nebuvo išdraskytos Čekoslovakijos, kai ne vien Vokietija, bet ir Vengrija, ir Lenkija iš esmės dalyvavo Europos perdalijime? Miuncheno suokalbio dieną Lenkija pareiškė ultimatumą Čekoslovakijai, o lenkų kariuomenė kartu su vokiečių armija įžengė į Tešino ir Frištado sritis.

Ar galima užmerkti akis į vakarų demokratijų užkulisines pastangas atsikratyti Hitlerio ir nukreipti jo agresiją „Rytams“?“

Dėl pakto slaptumo ir amoralumo

2-ojo TSRS Liaudies deputatų suvažiavimo nutarymo teiginys, jog slaptas protokolas pridėtas prie 1939 metų rugpjūčio 23 dienos TSRS ir Vokietijos nepuolimo sutarties pagal sudarymo būdą ir turinį pažeidė tarptautinę teisę, yra ne vien tik politizuotas bet ir visiškai nekompetentingas.

Panašūs paktai ir sutartys, turintys papildomus konfidencialus, slaptus (pavadinimas esmės nekeičia) protokolus, kurių turinys nebuvo viešai skelbiamas, su Vokietija tarpukario metais sudarė Anglija, Prancūzija, Lenkija, Estija, Lietuva, Italija ir Japonija.

Molotovo-Ribentropo paktui 80 metų. Bet Europa irgi sudarydavo sąjungas su Hitleriu, apie tai, tačiau, nekalbama.

Slapti sutarimai iki šiol išlieka vakarų diplomatijos metodika. 1960-ųjų metų pradžioje JAV ir Japonija, kuri paskelbė esanti nebranduolinė šalis, sudarė slaptą paktą, pagal kurį Japonijoje gali būti saugomi amerikiečių branduoliniai ginklai. Šita sutartis leidžia amerikiečių karo laivams ir lėktuvams, gabenantiems branduolinius ginklus, rastis Japonijoje ir bet kuriuo metu sukelti pavojų visam pasauliui.

Ypač svarbu pasisakyti dėl taip vadinamo pakto amoralumo. Šitas momentas yra akcentuojamas lietuvių ir kai kurių rusų politikų ir istorikų. Šiuolaikinių pozicijų atžvilgiu samprotavimai šia tema yra klaidingi.

Beje, mes ir šiandien vargu ar atspėsim, kas iš šiuolaikinių „garbingų“ politikų bus pavadintas nusikaltėliu. Kandidatų šiam titului nemažai.

O kalbant apie įtakos sferas, galima pabrėžti, kad šiandien JAV, besinaudojant pasaulio galingiausios valstybės statusu, jau atvirai deklaruoja savo teisę dalinti pasaulį į savo įtakos sferas, įtraukiant į jas ir valstybes, turinčias bendras sienas su Rusija. Tai nekelia vakarų bendruomenės pasmerkimo. Įdomu, kaip ta pati bendruomenė reaguotų jei Rusija paskelbtų savo gyvybinio intereso sfera Kanadą, Meksiką bei Panamą, tai yra. artimiausius JAV kaimynus?

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 3 — id: `scraped:rubaltic_lt:c01c64624cc21472`

**Title:** Putino ataka „istoriniame fronte“ nugąsdino Lietuvą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos prezidentas Gitanas Nausėda pareiškė, kad Rusija pastaruoju metu visomis išgalėmis stengiasi perrašyti istoriją. Taip griežtai Lietuvos lyderis reagavo į paskutinį Putino pareiškimą, kad Antrąjį pasaulinį karą išprovokavo ne Molotovo–Rybentropo paktas, o Europos šalių nuolaidžiavimas Hitleriui. Manoma, jog šios Pabaltijo respublikos valdančiuosius sluoksnius nugąsdino Rusijos prezidento kontrpuolimas „informaciniame fronte“: tokiai šaliai, kaip Lietuva, sukurtai visiškai sufalsifikavus istorinius faktus, nepriimtina mintis, kad gali būti peržiūrėti jos fundamentalūs mitai.

„Pastaruoju metu Rusija visomis išgalėmis stengiasi perrašyti istoriją. Vienas iš tokių pavyzdžių — Molotovo–Rybentropo pakto slaptųjų protokolų įtakos Europos istorijai liguistas neigimas, — savo Facebook puslapyje parašė Lietuvos prezidentas Gitanas Nausėda. — Šie slapti nacistinės Vokietijos ir komunistinės Tarybų Sąjungos susitarimai nulėmė vėlesnę Pabaltijo šalių okupaciją.“

Visa tai parašyti Lietuvos prezidentą paskatino fenomenalus Rusijos prezidento aktyvumas „istoriniame fronte“. Tradiciškai kasmet vykstančios spaudos konferencijos metu Putinas papasakojo, jog daug metų studijavo istorinius šaltinius ir dabar rašo straipsnį apie tai, kaip Europos šalių lyderiai Antrojo pasaulinio karo išvakarėse bendravo su Hitleriu ir stengėsi jo apetitą nukreipti link Tarybų Sąjungos. Būtent ši išprotėjusio fiurerio kurstymo, nuolaidžiavimo ir agresijos prieš Rusiją provokavimo politika ir tapo pagrindiniu Antrojo pasaulinio karo detonatoriumi. O plačiai nuskambėjęs Molotovo–Rybentropo paktas ir praėjus 80 metų sukelia „europoietiškų partnerių“ įniršio priepuolius, jaučiant, jog tarybinė diplomatija juos įveikė patį paskutinį momentą.

Jau kitą dieną po spaudos konferencijos Rusijos lyderis palietė kovos su istorijos falsifikavimu temą NVS samito metu. Buvusių tarybinių respublikų vadovams, susirinkusiems aptarti ekonomikos klausimų, išsamus pasisakymas apie tai, kaip buvo įtvirtinamos Hitlerio pozicijos, tapo perkūnija iš giedro dangaus.

Putinas davė suprasti, jog Rusijai dabar svarbiausia — istorinė politika. Ne nafta, ne dujos, ne prekių apyvarta, ne „integracijos stiprinimas“, o Didžiosios Pergalės Didžiajame Tėvynės kare gynimas. Kremliaus vykdomas skirstymas į savuosius ir svetimus vykdomas būtent šiuo principu: į tuos, kurie kartu su Rusija pasiryžę ginti šį atminimą, ir tuos, kurie užima kitą poziciją arba prisilaiko neutraliteto.

„Istorinis Rusijos prezidento kontrpuolimas“ akivaizdžiai nugąsdino šalis, pripratusias galvoti, jog tik joms svarbiausia — istorinė politika, o Maskva taip ir siūlys joms pragmatinius santykius vietoj pokalbio apie vertybes. Įprastos schemos griūtis buvo sutikta kaip grėsmė.

Gitanas Nausėda pasirinko, jo manymu, tinkamą datą: lygiai prieš 30 metų TSRS Aukščiausioji Taryba pripažino Tarybų Sąjungos–Vokietijos nepuolimo sutarties egzistavimą ir paskelbė negaliojančiais slaptuosius Molotovo–Rybentropo pakto protokolus. Lietuvos prezidentas tuo bando kažką įrodyti, pats nesuprasdamas, ką.

Rusija ir po 30 metų neneigia, jog egzistuoja Tarybų Sąjungos–Vokietijos nepuolimo sutartis, ir nelaiko jos pasirašymą pasididžiavimo pagrindu. Esmė kitur: Maskva daug metų stengėsi suformuoti antihitlerinę koaliciją, tačiau Vakarų šalys viena po kitos siekė suokalbio su naciais ir pasirašinėjo su Trečiuoju reichu nepuolimo sutartis, tikėdamosios jo apetitą nukreipti link Tarybų Sąjungos.

Protokolo nuotraukose Hitleriui džiaugsmingai šypsosi Didžiosios Britanijos premjeras Čemberlenas ir prancūzijos premjeras Deladje, Bulgarijos caras Borisas ir Lenkijos maršalas Pilsudskis. Tik nėra Stalino su Hitleriu nuotraukos, nes TSRS iki paskutiniųjų iki Antrojo pasaulinio karo pradžios vadino nacių režimą visišku blogiu, o pastarasis deklaravo rusų valstybės sunaikinimą, prie ko jis buvo aktyviai stumiamas. Stalinas turėjo pasirinkimą: pasmerkti savo šalį šiam sunaikinimui arba sudaryti taktinį sandorį su blogiu, kurį jau buvo sudarę visi „apsišvietusieji europiečiai.“

Taip kad antitarybinė Antrojo pasaulinio karo mitodologija subliūkšta net be kažkokių ten archyvinių atradimų. O Rusija tuos duomenis atranda ir pristato. Lietuvos vadovybė neranda kaip paprieštarauti, ir tada milijoninį kartą pakartoja: Trečiojo reicho ir Tarybų Sąjungos atsakomybė vienoda, nacizmas lygus komunizmui, Molotovo–Rybentropo paktas nulėmė Pabaltijo šalių okupaciją.

Tačiau šiandieninis lietuviškasis Vilnius nepasakys, kad diktatorius Antanas Smetona sudarė sandorį su Stalinu ir dalyvavo „ketvirtame Lenkijos padalinime“, atsakydamas į Raudonosios armijos kontingento Lietuvoje dislokavimą. Šiandien Lietuva vaizduoja nekaltą prievartavimo auką, nors į Antrąjį pasaulinį karą įžengė kaip viena iš geopolitinių grobuonių ir pasireiškė šio karo metu žydų genocide „žygdarbiais“ kolaborantų, kurie paskui lakstė nuo VRLK (НКВД) po miškus ir, prisidengdami kova už nepriklausomą Lietuvą, terorizavo žemiečius lietuvius.

Po karo Lietuva sparčiai statė komunizmą ir pagal TSKP narių skaičių šimtui tūkstančių gyventojų tapo pirmaujančia tarp tarybinių respublikų. Vėliau respublikos VSK (КГБ) Maskvos nurodymu sukūrė Lietuvoje pirmąjį TSRS nacionalinį judėjimą persitvarkymui remti su savo agentu — Dėdule Landsbergiu priešakyje. Kai Tarybų Sąjunga pradėjo siūbuoti, šis judėjimas ėmė reikštis kaip kovojantis už nepriklausomą Lietuvą ir, siekdamas pagreitinti atsiskyrimą nuo TSRS, prie Vilniaus televizijos bokšto organizavo kruviną provokaciją.

Tokia tikroji Lietuvos XX amžiaus istorija.

Suprantama, kodėl dabar Lietuvos viršūnėlės sunerimo dėl Putino siekio kautis vardan istorinės tiesos. Rusijos prezidentas — ne bejėgis Lietuvos disidentas Algirdas Paleckis. Putinui nepavyks pritaikyti Baudžiamojo kodekso „okupacijos neigimo“ straipsnio. Jo nepagąsdinsi Vilniaus apygardos teismu ir į Kybartų kalėjimą neįkiši.

Ir todėl Lietuvos valdžioms belieka atitrūkti nuo pastangų, siekiant išteisinti Holokausto organizatorius, ir verkšlenti, jog ne jos, o Putinas perrašinėja istoriją.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 4 — id: `scraped:rubaltic_lt:0acc266737de7510`

**Title:** Lietuvos prezidentas „sudegino visus tiltus“, kurie galėjo padėti normalizuoti santykius su Rusija

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos prezidentas Gitanas Nausėda tebedidina rusofobijos laipsnį. Praėjusiame NATO samite paskelbęs, jog Rusija — „grėsmė pasaulinei tvarkai“, Pabaltijo respublikos lyderis priminė Europos Sąjungai, jog būtina pratęsti sankcijas, pagyrė Zelenskį, kad nenuolaidžiavo Putinui derybų Paryžiuje metu, o konferencijoje užsienio politikos klausimais išdrožė kažką panašaus į Čerčilio „Fultono kalbą“. Atrodo, jog metų pabaigoje Nausėda tikslingai „degina tiltus“ , nepalikdamas jokių šansų Lietuvos — Rusijos santykių normalizavimui.

Nausėda priėmė Zelenskį Vilniuje lapkričio 27 dieną ir patarė jam „jokiu būdu nenuolaidžiauti Rusijai“. Kažkokias papildomas instrukcijas jam pateikė privataus pokalbio metu. Po „Normandijos ketvertuko“ susitikimo paaiškėjo, kokias.

„Ukrainos pusė, kaip jai patarė Gitanas Nausėda, sutarė iki Kalėdų apsikeisti belaisviais ir nutraukti ugnį, — pranešė Lietuvos prezidento patarėja Asta Skaisgirytė. — Tačiau Paryžiuje nepavyko susitarti dėl Rusijos kariuomenės dalinių išvedimo iš Donbaso ir jo perdavimo visiškai Kijevo kontrolei. Tikėkimės, kad sprendimas atsiras kitų etapų metu“.

Pareiškimo tonas primena Dalios Grybauskaitės toną. Buvusi Pabaltijo respublikos prezidentė ne šiaip rėmė Ukrainą, bet matė joje šalį, kuriai labai reikalinga vyresnių draugų globa. Ir tai suprantama. Su „Rusijos agresija“ Lietuva susidūrė dar prieš Tarybų Sąjungos subyrėjimą. Kas, jei ne ji, geriausiai supranta šios temos svarbą?

Ir visiškai taip pat jis pervertina savo vaidmenį užsienio politikoje: esą būtent taip, kaip jis patarė, elgėsi Ukrainos pusė derybų Paryžiuje metu.

Tačiau dar labiau stebina tas faktas, jog pokalbio su Zelenskiu metu Nausėda palietė skaudžius derybų klausimus, susietus su apsikeitimu belaisviais ir ugnies nutraukimu. Ir tai galima įvertinti kaip diplomatinį įžūlumą. Kodėl gi buvęs Lietuvos finansininkas ėmė įsivaizduoti, jog puikiai susigaudo taikos pasiekimo Donbase klausimuose? Ar gali svaidytis patarimais, kaip elgtis derybose su Putinu, žmogus, nė karto nesusitikęs su Rusijos prezidentu? Ir, tikriausiai, nesusitiks…

Iš pradžių jis užsiminė, jog dar iki vietinių rinkimų atskiruose Donecko ir Lugansko sričių rajonuose tikslinga sugrąžinti Ukrainai sienos kontrolę, o vėliau, susitikęs su Europos Sąjungos šalių ambasadoriais, pareiškė, jog antirusiškos sankcijos „turi galioti kol nebus įgyvendinti visi Minsko sutarties punktai“.

Už liežuvio Lietuvos lyderio niekas netimptelėjo: visi, vadinasi, visi. 9-ame „Minsko–2“ punkte teigiama, kad Ukraina pradeda kontroliuoti Donbase valstybinę sieną nuo kitos dienos po vietinių rinkimų. Vadinasi, jį taip pat būtina vykdyti. Tačiau Zelenskis priešinasi. Ir peršasi klausimas: jeigu sankcijos siejamos su Minsko nutarimų vykdymu, tai kam jas reikėtų taikyti? Ar ne tai pusei, kuri atsisako juos vykdyti?

Tai anksčiau Rusija buvo bloga, nes nenorėjo vykdyti „Minsko“. Dabar ji bloga todėl, kad nenori peržiūrėti „neteisingų“ sutarčių.

Nenorint patekti į nepatogią padėtį, Lietuvos prezidentui vertėtų pasitikslinti, kad įgyvendinti turi būti visi Minsko sutarties punktai, išskyrus 9-tą — jį būtina perrašyti. O gal ne tik jį. O kodėl neparuošti teksto visiškai naujos sutarties, kurią Maskva esą privalo vykdyti?

Gali keistai atrodyti, kad Putino ir Zelenskio „dvikovoje“ nugalėtoju Nausėda paskelbė pastarąjį. Tačiau taip atrodo tik iš pirmo žvilgsnio. Jei gerai pagalvoti, Lietuvos prezidentas mato esmę. Svarbiausias ketvertuko susitikimo rezultatas — karo tęsinys. Todėl nugalėjo tas, kuriam nereikia taikos.

Neatsitiktinai Ukrainos vidaus reikalų ministras Arsenas Avakovas prasitarė, jog būtent Zelenskis su kompanija atsisakė atitraukti karinius dalinius nuo visos susidūrimo Donbase linijos — esą, jiems dabar tai nenaudinga.

Pabaltijo politikai baiminasi Kijevo ir Maskvos santykių normalizavimo. Dabar jau aišku, jog normalizavimas atidedamas iki geresnių laikų.

„Mes neturime apgaudinėti savęs paviršutiniškomis kalbomis apie mūsų didžiąją kaimynę. Deja, aš girdžiu daug tokių kalbų.Vakarų pasaulis turi vieną kartą padaryti išvadas iš atvejų su Gruzija ir Ukraina. Rusija pastaruoju metu net ėmėsi neigti Pabaltijo šalių aneksijos ir okupacijos 1940 metais. Visi ankstesnieji bandymai pažvelgti Rusijos vadovybei į akis ir užsiiminėti savęs apgaudinėjimu nedavė norimo rezultato“, — pareiškė Nausėda konferencijoje Lietuvos užsienio politikos klausimais.

Pergalės prieš „agresorę“ receptas paprastas: didinti išlaidas gynybai, neįteisinti Rusijos „neteisėtų veiksmų“, reikalauti iš jos atsakomybės visuose įmanomuose formatuose. Tačiau Lietuvos prezidentas pamiršo vieną labai svarbią detalę: būtina nuleisti naują „geležinę uždangą“.

Santykiai tarp Rusijos ir Lietuvos vargu ar šiltesni, nei kadaise tarp Tarybų Sąjungos ir Vakarų Europos. Tačiau kitoje Europoje girdisi daug „paviršutiniškų pokalbių apie mūsų didžiąją kaimynę“. Situaciją tenka taisyti.

Zelenskis, žinoma, nelaikė galvoje Nausėdos patarimų, vesdamas derybas su RF prezidentu. Dar mažiau jo patarimai reikalingi prancūzams ir vokiečiams.

Kremliuje po išsišokimo pagal geriausias Dalios Grybauskaitės tradicijas net nepagalvos apie galimybę derybų su naujuoju Lietuvos prezidentu. Nors visai neseniai tokia galimybė egzistavo.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 5 — id: `scraped:rubaltic_lt:661561de216b4bb4`

**Title:** Lietuva pardavė savo „energetinę nepriklausomybę“ lenkams

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lenkijos valstybinė įmonė PGNiG nuo šiol naudosis skirstomąja SGD stotimi Klaipėdoje. Varšuva ne vien tik gaus kontrolę virš dujų saugyklas pajūryje, bet ir galimybę spręsti, kas pripildys tas saugyklas dujomis. Šitą smulkų komercinį kontraktą galima nagrinėti kaip lenkų pretendavimo į Baltijos regiono dujų Habo vaidmenį ir Lietuvos ketinimo parduoti savo „energetinę nepriklausomybę“ pagrįstą rezultatą.

Prieš du metus Klaipėdoje, 7 kilometrų nuo SGD-terminalo Independence atstume, buvo įkurta smulkaus tonažo dujų skirstymo stotis, kurią sudaro 5 rezervuarai. Iš čia SGD yra pildomos į autocisternas ir toliau teikiamos galutiniam vartotojui, o taip pat vartojamos laivų, naudojančių suskystintas gamtines dujas, bunkeriavimui.

Pagal Klaipėdos Naftos vadybos sumanymą, stotis turi būti naudinga tiems vartotojams, kas neturi prieigos prie magistralinių dujotiekių.

Nuo 2014 metų jie nesėkmingai stengiasi pasiekti iš Norvegų išsinuomoto SGD-terminalo apsimokėjimo (apie pelną iš vis net nekalbama). Kai paaiškėjo, kad terminalas Independence nepateisina su juo sietų vilčių, Klaipėdos Naftoj buvo nuspręsta paeksperimentuoti su SGD tiekimais be sudujinimo. Tokia skystas dujas galima naudoti kaip kurą automobiliams, jūros bei upių laivams, elektros gaminimui atskiruose regionuose.

Penkios saugyklos, kurių bendra talpa – 5 tūkstančiai kubiniai metrai SGD, buvo pastatytos vokiečių kompanijos PPS Pipeline Systems ir jos čekiško partnerio Chart Ferox. Stoties paleidimas buvo priderintas trečioms SGD-terminalo atvykimo į Klaipėdą metinėms, o patį renginį pristatė kaip dar vieną „sėkminga“ Lietuvos energetikos projektą.

Klaipėdos Naftos eksvadovas Mindaugas Jusius pasakodavo apie bendradarbiavimo su tarptautiniu plastiko gamintoju Indorama ir logistikos kompanija Girteka perspektyvas. Pasak jį, kai kurios vietinės įmonės net svarstė nuosavos SGD saugyklos statybos netoli stoties galimybę. Nuo čia pat galima teikti kurą elektros gaminimui šiaurės Lietuvos miestuose.

Apskritai kalbant, žodžiuose viskas buvo nuostabu.

„Pasiekę susitarimo, galime nukreipti dėmesį į infrastruktūros operatoriaus veiklą, užtikrinti stabilų pelną ir padengti kapitalo ir operacines išlaidas. Tuo tarpu strateginis partneris atsakys už SGD pardavimus bei rinkos plėtrą“, - pasakė įmonėje.

„Strateginiu partneriu“ galų gale tapo PGNiG – konkurse dalyvavo penkios įmonės, bet palankiausias sąlygas pasiūlė lenkai. Šiuo sandėriu labai patenkinti liko ir Lietuvos energetikos ministras, ir Klaipėdos Naftos generalinis direktorius. Vilnius aukštai įvertino lenkų patirtį ir kompetencijas suskystintų gamtinių dujų prekyboje. Tikriausiai, Lietuva tikisi, kad naftos ir dujų gigantas iš kaimyninės šalies sugebės sutvarkyti dujų pardavimo stoties darbą Klaipėdoje.

Stoties rentabilumą Mindaugas Jusius ligino su vis augančiu poreikiu naudoti SGD kaip transporto kurą.

„Pasak mūsų verslo planą, stotis turi tapti pelninga 2020 metais. Iki to laiko mes matom nuoseklų veiklos augimą, o patį sparčiausią jos paslaugų reikmės augimą mes matom tarp 2020 ir 2025 metų“, - objekto paleidimo metu teigė buvęs Klaipėdos Naftos vadovas.

Laimė jau visai arti – vos-vos ateis tie lemtingi 2020 metai. Bet vietoj to, kad savarankiškai pasipelnyti iš projekto, įsivyrauti smulkaus tonažo SGD rinkoje ir statyti papildomus rezervuarus, lietuviškas operatorius kreipiasi pagalbos į pažengę lenkus.

Arba su pelnu irgi nesiseka? Mažai Baltijos respublikai PGNiG – įmonė, kuri valdo milijardus dolerių – tikrai atrodo kaip koks naftos ir dujų milžinas. Suskystintų gamtinių dujų rinkoje lenkai turi daugiau ryšių ir daugiau galimybių. Todėl Lietuvoje ir tikisi, kas Varšuvos atstovai sugebės panaudoti dujų skirstymo stotį maksimalaus pelno gavimui.

Lenkija savo ruožtu sudominta tuo, kad išmėginti laimę Baltijos šalių smulkaus tonažo SGD rinkoje. Pastaraisiais metais šita rinka tikrai vystasi rekordiniais greičiais (visų pirma pigaus ir ekologiško dujų variklių kuro augančio vartojimo dėka). PGNiG vadovas Piotras Vozniakas tiesiogiai sieja stoties nuomą su įmonės įsigaliojimu Centrinėje ir Rytų Europoje.

Lietuva sugebėjo išsivaduoti iš „sovietų okupacijos“ ir „Gazpromo monopolijos“, bet padaryti sekantį logišką žingsnį – tapti savarankišku rinkos dalyviu – nepajėgė. Arba nepanorėjo. Galų gale visada daug lengviau „gulti su kuo nors į lovą“. Energetikos srityje idealu „senjoru“ Lietuvai gali tapti Lenkija, paklusni tam pačiam „Vašingtono obkomui“

Kol kas sutarimas tarp PGNiG ir Klaipėdos Naftos atrodo kaip smulkus komercinis sandoris. Bet Vozniako pozicija liudija apie tai, kad Varšuvos apetitai gali ir neapsiriboti tik viena skirstymo stotimi.

„Tiekimų saugumo atžvilgiu labai svarbu, kad PGNiG savarankiškai nustatytų, kas atliks tiekimus į skirstymo stotį Lietuvoje“, - teigė kompanijos vadovas.

Viskas atrodytų logiškai: lenkai gauna pilną kontrolę virš išsinuomotą infrastruktūrą. Išlieka vienintelis klausimas – kaip įgyvendinama PGNiG teisė SGD tiekėjo pasirinkimui. Dujos į saugyklą tikriausiai bus pristatomos nedideliais tanklaiviais iš to paties terminalo Klaipėdos uoste.

Ir jeigu jie pradės, tai kas gi galiausiai liks nuo Lietuvos „energetinės nepriklausomybės“?

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 6 — id: `scraped:rubaltic_lt:0491ce21f7e9ece8`

**Title:** Dauguma lietuvių – prieš konfrontaciją su Rusija

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Absoliuti lietuvių dauguma mano, kad valstybės politika Rusijos atžvilgiu yra pernelyg drastiška, ir pasisako prieš išlaidų karinėms reikmėms augimo. Lietuvos valdžia net pradėjo viešą ginčą su savo žmonėmis: prezidentas Gitanas Nausėda priekaištavo lietuviams dėl politinio nesąmoningumo kylančio iš nenoro gaišti pinigų armijai. Pirmą kartą valdžios konfrontacinės politikos Rusijos atžvilgiu nepopuliarumas tapo toks akivaizdus Lietuvoje.

Lietuvoje beveik iš eilės buvo paskelbti sociologinių tyrimų sensacingi rezultatai. Pirmas – kompanijos „Vilmorus“ visuomenės nuomonės apklausa – parodė, kad daugiau nei pusė lietuvių prieštarauja tolimesniam karinio biudžeto augimui.

Šiems metams Lietuva pagaliau pasiekė NATO ir JAV prezidento Donaldo Trumpo normatyvuose reikalaujamo 2% nuo šalies BVP didžio karinio biudžeto. Deja Lietuvos valdžiai ir to neužtenka: dabar jie su iškėlė uždavinį padidinti išlaidas gynybai iki 2,5% nuo šalies BVP.

Tolimesniam karinių išlaidų augimui nepritaria ir greičiau nepritaria 55% šalies gyventojų. Dėl militarizacijos tęsimo maždaug įsitikinę yra 30% respondentų, o 14,5% susilaikė nuo atsakymo.

Oficialios politikos nesutapimas su gyventojų nuomone taip smarkiai rėžia akį, kad net prezidentas nusprendė “sugėdinti” lietuvius dėl jų politinio nesąmoningumo.

“Aš sieksiu to, kad mes suprastumėme vieną paprastą dalyką – jeigu norime sutaupyti, gailėdami pinigų saugumui, tokiu atveju pensijas mes, žinoma, galime gauti ir iš kitos šalies. Lietuvoje valdžia didina išlaidas gynybai viešai besiskelbdama, kad tai daroma “Rusijos agresijos atrėmimui”, - teigė Lietuvos prezidentas Gitanas Nausėda per pasirodymą, kas yra svarbu, Pabradės poligone netoli Baltarusijos valstybinės sienos, kur jis atvažiavo įsigyti amerikietiškų tankų.

Besąlygišku prioritetu šalies gyventojai laiko socialinių reikalų srities problemų sprendimą. Nieko keisto. Šalis, kuri pirmauja pasaulyje pagal alkoholizmo lygį ir Europoje – pagal savižudybių skaičių, taip pat “lyderiauja” skurdo, nužudymų, gyventojų mirtingumo, emigracijos reitinguose. Aišku, kad su tuo reikia ką nors daryti.

Valdžia, atrodo, prieš tai neprieštarauja. Tas pats Nausėda su pasipiktinimu sako, kaip jam gėda už tas socialines garantijas, kurias užtikrina Lietuvos valstybė savo gyventojams. Už skurdo lygį Lietuvoje, už pasigailėtinas pensijas.

Bet kaip gi taip – pasipiktina gyventojai. Valdžia ką tik įsigijo iš JAV 200 šarvuotų visureigių už 150 milijonų dolerių. “Abrams” tankus į šalį atgabeno, karinius biudžetus kasmet didina. Tankams pinigai yra, šarvuočiams ir karinėms pajėgoms – irgi yra, o pensininkams – nėra?

Vietoj atsakymo gyventojai išgirsta valdžios pamokslavimą su sakramentiniu posakiu – “tiems, kas nenori išlaikyti savo armijos, teks išlaikyti svetimą”. Norite, kad pensijas jums mokėtų rusų okupantai? Juk nepamirškite, kad turime smurtaujantį kaimyną, kuris greit mus užpuls.

Po daugelio metų nesiliaujančios valstybinės isterijos, vadinamos “rusai puola”, absoliuti lietuvių dauguma laiko antirusišką politiką netinkamu.

Lietuvos vyriausybė paskelbė apklausos, kuo didžiuojasi lietuviai, rezultatus. Taigi tik 11% gyventojų didžiuojasi nepalenkiamai negatyvia Lietuvos pozicija santykiuose su Rusija. Pernelyg drastiška šią poziciją laiko 53% lietuvių.

Tai yra, daugiau nei pusės gyventojų neįkvepia tai, kuo sužavėjo oficialią propagandą buvusi Lietuvos prezidentė Dalia Grybauskaitė – antirusiškas lojimas, pavadintas politine drąsa, ir griežta pozicija. Rusija per visus šiuos metus taip ir nepuolė, neokupavo Lietuvos ir neparodė nei mažesnio ketinimo tai daryti. Kam ir toliau pirkti iš amerikiečių šarvuotus visureigius, darant dar labiau žalos pensijoms ir vienišoms motinoms skirtoms pašalpoms, niekas ryžtingai nebesupranta.

Valstybinės apklausos rezultatuose daugelis įdomų rodyklių. Pavyzdžiui, net 70% lietuvių laiko savo šalį korumpuota, o net 52% mano, kad Lietuva yra mažiau sėkminga šalis, nei regiono kaimynai. Tuo pačiu laiku tik ketvirtadalis apklausos dalyvių didžiuojasi respublikos orientacija į JAV ir tik 26% žavisi Lietuvos vaidmenimis NATO ir Europos Sąjungoje. Nes tas vaidmuo – riekiančio apie “Rusijos grėsmę” dykumoj.

Konflikto epicentre – šalies prezidentas Gitanas Nausėda, kuris pavasarį triumfavo per rinkimus, nes žadėjo laikytis teigiamų pokyčių politikos. Įskaitant tokį ekstremalų šiuolaikinės Lietuvos aplinkybėmis pokytį kaip politinio dialogo su Rusija atkūrimą.

Deja vietoj naujos politikos Lietuva iš įpročio seka Dalios Grybauskaitės ir jos rėmusių “landsbergiečių” pramintu taku. O ateities pokyčių simbolis Nausėda po rinkimų pasisako prieš derybas su Maskva ir pasmerkia savo rinkėjus už pasiryžimą paaukoti išlaidas karinei technikai tam, kad padidinti pensijas ir pagerinti socialines garantijas.

Vis dėlto, akivaizdus dabartinės politikos nepopuliarumas visai nepriverčia valdžios jos atsisakyti. Valdžia laikosi savo linijos tam, kad nepaisant gyventojų nepasitenkinimo ir toliau pirkti tankus iš JAV ir skanduoti antirusiškus lozungus.

Jeigu tokia yra demokratija tai tik kažkokia labai savotiška lietuviška jos versija. Tai yra Rusijos ir Vakarų pasienyje esančios šalies-limitrofo demokratija, kurioje joks piliečių valios pareiškimas negali būti vertinamas labiau nei paskirta šaliai istorinė “Rusijos agresijos atlaikymo” misija.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 7 — id: `scraped:rubaltic_lt:0e3453e5b235a167`

**Title:** SGD-terminalas Lietuvoje toks “sėkmingas”, kad klientai priversti kreiptis į teismą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Pagrindinis Klaipėdos SGD-terminalo produkcijos pirkėjas, lietuviškas koncernas „Achemos grupė“ kreipėsi į Europos Sąjungos Teisingumo Teismą dėl to, kad Lietuva priverčia koncerną įsigyti dujas iš SGD-terminalo. Achema ir kiti plūduriuojančio terminalo Idependence priversti klientai jau nebe pirmus metus maištauja prieš vyriausybę, dėl ko pastaroji virsta pajuokos objektu, nes daugelį metų įtikindavo Europą, jog SGD-terminalas tapo labai pelninga verslo idėja. Labiausiai iš tos verslo idėjos pasipelnė tikrovėje Rusija.

Stambiausia Rytų Europos trąšų gamykla Achema jau antrus metus atstovauja lietuviškų gamintojų kovai prieš jiems primesto gamtinių dujų tiekėjo – SGD-terminalo Klaipėdoje. Achema – stambiausias Idependence produkcijos vartotojas ir tuo pačiu metu labiausiai nukentėjęs.

Prieš pusantrų metų Achema pradėjo maištą prieš “energetinės nepriklausomybės” ir teigė tiesiai: SGD-terminalas neapsimoka, o patį koncerną išvis į pragaištį įstumia. Lietuvos valdininkai tuomet dar važinėdavo po tarptautinius simpoziumus ir pasakodavo visiems, kas sutikdavo klausyti, kokią “laimės istoriją” teko patirti Lietuvai po “energetinės nepriklausomybės” nuo Rusijos atgavimo SGD-terminalo paleidimo dėka.

Kai problema pasireiškė visame savo rimtume, Lietuvos valdžia buvo priversta pakeisti savo retoriką dėl SGD-terminalo. Ministras-pirmininkas Saulius Skvernelis pervardino buvusią “sėkmės istoriją” į “Lietuvos mokesčių mokėtojų naštą”, su kuria reikia ką nors daryti.

Paprasčiausiu ir aiškiausiu sprendimu buvo leisti smunkantiems verslininkams atsisakyti SGD-terminalo dujų ir pirkti vietoj suskystintų įprastas dujotiekio dujas iš Rusijos. Bet valdžia tokiam žingsniui pasiryžusi nebuvo, nes jeigu terminalas netektų savo produkcijos priverstų pirkėjų, tai būtų Idependence garantuotas bankrutavimas. Savo ruožtu tai būtų visuotinis Lietuvos energetikos politikos susikirtimas ir padarytų šaliai daug gėdos viso pasaulio akyse.

Buvo pasiūlytas kompromisas. Achema pasirašys ilgalaikę sutartį suskystintų dujų tiekimams iš Independence už ką įmonei bus sumažinta SPG-terminalo išlaikymo rinkliava. Jonavos gamykla dar labiau pasipiktino ir pareiškė, jog į vergovę savo valia neeis.

Pavasarį Achema apskundė ES teisingumo teisme SGD-terminalo išlaikymo tvarką. Įmonės atstovai pavadino primestą būtinumą apmokėti jo išlaikymą rinkos dalyvių diskriminacija. Rugsėjį Europos teismas skundą atmetė, teigdamas, kad Lietuvos valstybė turėjo teisę nustatinėti verslo vedimo taisykles energiją gaminančioms įmonėms. Deja Achema nenurimo ir dabar ruošiasi apeliacijai. Nauja byla bus pateikta į Briuselį jau šią savaitę.

Šioje Lietuvos verslo ir vyriausybės užsitęsusioje rungtinėje yra kai kas nematomas trečias. Tai – Rusija, dėl kurios visa kova ir prasidėjo. Pati Rusija tam nieko kaip nedarė taip ir nedaro. Bet visi konfliktai ir skandalai dėl SGD-terminalo vienaip ar kitaip yra nuvedami prie rusiškų dujų pirkimų klausimo.

Dėl šio sprendimo Lietuvos valdžia vėl ir vėl patenka į apgailėtinai juokingas situacijas kartu su savo “energetine nepriklausomybe”. Atgabeno SGD-terminalą į Klaipėdą – neatsirado pirkėjų suskystintoms dujoms. Privertė savo pramonę naudotis produkcija iš Independence – pramoninkai kreipėsi į ES teismą. Paskelbė savo energetinę politiką kaip pavyzdį visai Europai – ir patys pripažino SGD-terminalą “našta mokesčių mokėtojams”.

Visai ypatinga istorija – rusiškų SGD tiekimai į Klaipėdos plūduriuojantį terminalą kaip priverstinis kompromisas su pramoninkais, kuris leidžia jiems išsigelbėti nuo bankrutavimo. Rusiškų suskystintų dujų pirkimus, skirtus Independence, iš pradžių buvo bandoma nuslėpti, o dabar bandoma uždrausti tam, kad nedaryti Lietuvai dar didesnės gėdos.

Bet be pigų rusiškos kilmės SGD Achema ir kiti terminalo Independence klientai tikrai nepragyvens. Patirtimi jau pagrįsta, kad pirkti norvegiškas, amerikietiškas ir kitas “demokratines” dujas lietuviškos įmonės sau leisti negali.

Visų pirma, Rusija kaip teikė taip ir teikia į Lietuvą įprastas dujas naudojant Gazpromo dujotiekį. Antra, nuo šių metų pavasario Rusija teikia ir “Novatoko” suskystintas dujas iš Leningrado srities. Beje, nuo smulkių tiekimų jau prieina prie stambaus tonažo gabenimų. Trečia, be finansinio pelno Rusija turi teigiamą politinį efektą tarptautinėje arenoje, kuris parodo visą antirusiškos politikos neįžvalgumą ir kvailumą.

Nesvarbu, kuo prasitęs komedija su Independence, Maskvai tai bus linksma ir pelninga.

Jos pelnas toks akivaizdus, kad Lietuvos patriotams nebelieka nieko kito, kaip pareikšti, kad idėją atgabenti SGD-terminalą į Klaipėdą jiems primetė pats Vladimiras Putinas.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 8 — id: `scraped:rubaltic_lt:b283a85a4cfc08c2`

**Title:** Lietuva praranda tranzitą: transporto kompanijos bėga iš šalies.

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Dešimtys transporto kompanijų pasitraukė iš Lietuvos, užsiregistruodamos kitose Europos Sąjungos šalyse. Tranzito šakos atstovai pervežėjų išbėgimą aiškina tuo, jog valstybė verčia didinti atlyginimus tolimųjų reisų vairuotojams, ir tai tuo metu, kai Lietuvos logistikos verslas laikosi labai sunkiai ir transportininkų darbo sąlygos daug blogesnės nei pas kaimynus. Susiklosčiusi situacija vadinama grėsme nacionaliniam saugumui: be darbo gali likti dešimtys tūkstančių žmonių, o Lietuva praras tranzito šaką.

Praeitą mėnesį Lietuvos vyriausybė priėmė nutarimą pakelti sunkiasvorių mašinų vairuotojų atlyginimus. Šiandien jų atlyginimų koeficientas sudaro 1,3 minimalaus Lietuvoje atlyginimo. Nutarta jį padidinti iki 1,65 minimalaus atlyginimo.

Geri valdininkų norai pagerinti sunkiasvorių mašinų vairuotojų gyvenimą įsikūnijo žinomoje formulėje: „norėjo geriau — išėjo kaip visada“.

Skubiai Lietuvos parlamente organizuotuose klausymuose transportininkai paaiškino: prieš mus alternatyva — arba perkelti verslą į kitas Europos Sąjungos šalis, arba bankrutuoti.

„Mums tai bus skausmingas sprendimas. Mūsų kompanijoje dirba apie 1000 žmonių, o tai labai daug, mes juk žinom, jog pelnas sudarė 2 milijonus. Šios išlaidos „suvalgys“ mūsų pelną“, — sako tarptautinio transporto ir logistikos aljanso direktorius Hegelmann Transporte Tomas Jurgelevičius. „Kai tokias sumas padaugini, verta susimąstyti, ar verta turėti Lietuvoje transporto verslą ir plėstis“, — pareiškė biznierius Lietuvos politikams.

Kai buvo išaiškintos krizės priežastys, sužinota, jog koeficientų didinimas — tai ne priežastis, o paskutinis lašas.

Todėl naudingiau perkelti verslą į kitas šalis, nei pas save vystyti transporto sektorių. Logistines firmas žlugdantys vairuotojų atlyginimų koeficientai lengvai stumtelėjo verslą numatyta kryptimi. Kitose šalyse nėra jokių koeficientų, tačiau vairuotojų atlyginimai didesni, o verslas geriau organizuotas.

„Pagal išlaidas — Lenkija optimalus variantas, pats įkūrimas, licenzijos, ten tam skirtos išlaidos mažesnės. Kompaniją įkūrus, ji iš pat pradžių turėjo šansą gauti finansavimą. Čia ir mobilumo paketas. Lenkija savo teritorija geografiškai sėkmingesnė: jei atsižvelgti į reikalavimą sugrįžti, lyginant su Lietuva, bus mažiau „tuščių“ kilometrų. O kas dėl pinigų komandiruotėms, jiems nenustatytas koeficientas. Be to, Lenkijos draudimo rinkoje egzistuoja gera konkurencija“, — Lietuvos Seime pareiškė transporto kompanijos Savesta Consulting atstovas Ignas Volbikas, patvirtinęs, jog vien tik jie perkėlė į Lenkiją 60 savo įmonių.

Tai, kas vyksta, vadinama grėsme Lietuvos nacionaliniam saugumui. Nacionalinėje ekonomikoje viskas siejasi tampriai, o krizė vienoje šakoje neišvengiamai palies ir kitas. Prieš vienuolika metų visa Lietuvos ekonomika patyrė didžiulę recesiją dėl krizės viename sektoriuje — bankų, kai ipotekos kredito rinkoje trūko pūslė.

Dabar situacija panaši: „Domino efekto“ rizika akivaizdi ir ne ekonomistams, ir tuo metu niekas nežino mastų, kurie įtrauks į bankrotą vienas ir privers emigruoti kitas transporto įmones.

Įdomi šiame kontekste frazė „grėsmė nacionaliniam saugumui“. Šiaip Lietuvoje ji pasitelkiama, kai kalbama apie Kremliaus „rankas, kojas ir kitas kūno dalis“. Grėsmė Lietuvos nacionaliniam saugumui dainininkas Grigorijus Lepsas ir aktorius Michailas Porečenkovas, internet saito šefas Maratas Kasemas ir tie lietuviai, kurie Maskvos teatruose dirba meno vadovais.

Lietuvos URM ir Saugumo departamento lūpose šis išsireiškimas virto populiariu štampu dykinėjančioms namų šeimininkėms, pensininkams ir miestų bepročiams, kuriems maloniai dirgina nervus kalbos apie „rusų grėsmę“. Su realia saugumo politika ši šypseną sukelianti politika, liečianti estrados žvaigždes, kurios savo dainomis „klibina pamatus“, o taip pat „grėsmių“ vaidmenyje Mašą ir Lokį, neturi nieko bendro.

Taip atsitiko praeitą mėnesį su automobilių padangų gaisru Alytuje, kuris, pasak vidaus reikalų ministrės, buvo užgesintas, tačiau dar visą savaitę nuodijo Alytaus rajoną nuodingomis išmetomis. Taip dedasi dabar, priverstinai didinant sunkiasvorių mašinų vairuotojų atlyginimus.

Iš esmės sureguliuoti dabartinę krizės situaciją nėra labai sudėtinga. Atlyginimo koeficientas dar nepadidintas ir jį lengva nedidinti.

Patys transportininkai atkakliai pabrėžia: atlyginimų koeficiento didinimas — tai griūvančių stūmimas. Ir be jo Lietuvos tranzito sferoje buvo nemažai vargo. Jeigu viešieji mokesčiai, paslaugos, draudimai Lietuvoje būtų buvę kaip Lenkijoje, verslas nebūtų persikėlęs į šią šalį ir vairuotojų atlyginimai nebūtų buvę mažesni ir be jokių koeficientų.

Tačiau sukurti verslui naudingas sąlygas Lietuvos valdžioms — uždavinys ne jų gabumams. Visa, ką jie sugeba, — užblokuoti Rusijos deputatams ETPS tualeto kabinas ir paskelbti grėsme nacionaliniam saugumui eilinį „Žvaigždžių fabriko“ nugalėtoją.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 9 — id: `scraped:rubaltic_lt:2c39b7e989812a6e`

**Title:** Lietuvos prezidentas susiriejo su Suomija dėl gerų santykių su Rusija

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos prezidento Gitano Nausėdos apsilankymas Helsinkyje pasižymėjo viešu ginču su Suomijos prezidentu Sauli Niinisto (Sauliu Nyniste) dėl Rusijos. Niinisto žodžius, kad vis daugiau Europos Sąjungos šalių grįžta prie dialogo su Rusija, Nausėda suprato kaip išpuolį prieš Lietuvą ir kartu ragino Suomiją kovoti prieš Baltrusijos Astravo AE. Lietuvos pastangos įtraukti Suomiją į savo Rytų Europos rusofobų klubą atvirai kalbant yra juokingos, nes dialogas su Maskva užtikrina Skandinavijos šaliai neprilygstamai aukštą vietą tarptautiniuose reikaluose. Be viso to, „Rosatom“ stato Suomijai atominę elektrinę, kuri bus tokia pat kaip ir Baltarusijos AE.

Bendroje su Lietuvos prezidentu spaudos konferencijoje Sauli Niinisto (Saulis Nynistė) pasisakė už dialogą su bendru Rytų kaimynu, pabrėžęs tai, kad Suomija niekada to dialogo nenutraukdavo ir sėkmingai jį tęsia.

„Tai nereiškia, kad tu pritari Kremliui, bet jis (dialogas su Kremliumi) naudingas tam, kad suprasti, apie ką jie galvoja“, - Niinisto patikslino Suomijos poziciją kontaktų su Maskva atžvilgiu ir su pasididžiavimu pabrėžė, kad tokia pozicija dabar periminėjama visoje Europoje.

„Čia aš matau progresą: vis daugiau ir daugiau Europos Sąjungos šalių pradeda dialogą su Rusija“, - pažymėjo Suomijos prezidentas.

Gitano Nausėdos reakcija buvo netikėta.

„Aš visada esu dialogo šalininkas, bet mes taip pat privalome turėti principų bei vertybių“, - pasakė Nausėda, pasak kurio vakarų šalys turi ne tęsti dialogą su Putinu, bet stiprinti spaudimą tam, kad priversti jį atsisakyti agresijos prieš Rusijos kaimynus.

„Jeigu šitas elgesys pasikeis į gerąją pusę, mes busime pirmi tarp tų, kas pritars tokiems Rusijos pokyčiams“, - našlaujančios karalienės tonu teigė Lietuvos prezidentas.

Žinoma, stebėti šitą situaciją – juokinga. Prezidentūroje Daukanto aikštėje, matyt, tikrai tiki tuo, kad bendravimas su Vilniumi bus aukščiausiu „atlyginimu“, apie kurį Kremlius tik svajoja. Sėdi Putinas sau savo „Gorki-9“ rezidencijoje ir svajoja apie tai, kada jam paskambins Gitanas Nausėda. Dažniau jis galvoja tik apie tai, kas gi toks yra tas Nausėda...

Nausėda pasiūlė įtraukti į darbą Suomijos specialistus, kad užtikrinti Astravo AE saugumą. „Mano idėja slypi tame, kad pritaikyti Suomijos patirtį šioje sferoje, nes šita šalis turi daugybę ekspertų, kurie galėtų padėti Baltarusijai pastatyti atominę elektrinę, atitinkančią visus būtinus kokybės standartus. Tai būtų pats optimalus variantas visiems“, - pasakė Lietuvos prezidentas.

Juokas tame, kad šie ekspertai ir taip greičiausiai dirbs Astravo AE, nes Baltarusijos atominė energetika yra kuriama tų pačių žmonių, kurie jau sukūrė ir plečia Suomijos branduolinės energetikos sritį.

Suomijos vakaruose „Rosatom“ stato „Hanhikivi-1“ AE, ir šios atominės elektrinės projektas sutampa su Astravo AE projektu. Be to, Suomijoje jau daugiau nei 40 metų veikia „Loviisa“ AE, kurią pastatė dar Tarybų metų branduolinės energetikos inžinieriai ir už kurios saugų darbą atsako „Rosatom“ ekspertai.

Beje, kalbant apie kitas Lietuvos pridarytas nesąmones, Suomijos „Loviisa“ AE – yra tokio pat tipo atominė elektrinė, kaip ir Ignalinos AE Lietuvoje. Jos buvo pastatytos tų pačių žmonių ir beveik vienodu laiku.

Lietuva savo atominę elektrinę uždarė, nes 1) ją tai padaryti privertė Europos Sąjunga; 2) ekologinio saugumo vardan; 3) „energetinės nepriklausomybės“ nuo Rusijos vardan. Suomija savo AE išsaugojo, suremontavo ir pratęsė energoblokų eksploatacijos ribas, nes 1) tapo ES narė kaip turtinga šalis-donorė, o ne išlaikytinė, ir primesti jai sąlygų niekas nedrįso; 2) padarė visus reikalingus tikrinimus ir dėl AE saugumo neabejojo; 3) neturi antirusiškų neurozų.

Galų gale Suomija išsaugojo ir net padidino savo eksporto galimybes kaip vienas pagrindinių elektros energijos pardavėjų Baltijos regione, kol Lietuva virto iš elektros pardavėjo į elektros pirkėją ir dabar kovoja su Astravo AE visų pirma dėl Lietuvos politikų, supratusių savo kvailumą, kompleksų.

Tas nemalonus savo menkumo pojūtis, kai prieš akis – sėkmės istorija, greičiausiai ir nulėmė Lietuvos prezidento kelionės į Suomiją nuotaiką.

Suomija palaikydavo ir plėsdavo ekonominius ryšius su Rusija, kai Lietuva tuos ryšius panaikino. Dviejų atominių elektrinių istorijų lyginimas – chrestomatinis, deja ne vienintelis pavyzdys.

Suomija išsaugojo savo neutralitetą net Karibų krizės laikais, o Lietuva, pirmai galimybei pasitaikius, įšoko į NATO ir dabar iš visų jėgų tempia prie Rusijos ir Baltarusijos ribų amerikiečių tankus. Suomija visais laikais buvo „tiltu“ tarp Rytų ir Vakarų, o Lietuva mato save tik kaip „buferinė zona“ ir talpina visas savo užsienio politikos kuklias jėgas tam, kad paversti postsovietines šalis į „sanitarinę apsaugos zoną“ nuo Rusijos.

Ką, galų gale, turime?

Šita šalis užima neproporcingai svarbią palyginus su jos kukliu potencialu vietą tarptautiniuose reikaluose. Suomija turi nepriklausomą poziciją tarptautinėje arenoje, ja žavisi JAV prezidentas Donaldas Trumpas, kai renkasi Suomiją kaip vietą deryboms su Vladimiru Putinu.

Lietuva yra pavyzdingas Rytų Europos „užkaboris“.

Lietuvos prezidentą Vašingtone priima kartu su Latvijos ir Estijos lyderiais, painioja šalis su Balkanais, o Donaldas Trumpas pasakoja prezidentams apie „labai kvailus žmones“, kuri nenori turėti gerų santykių su Rusija.

Gana skriaudus tačiau teisingas apibrėžimas. Kas gali nuvažiuoti į Helsinkį agituoti Suomiją atsisakyti dialogo su Rusija ir visos jos dabartinės padėties tam, kad įstoti į Rytų Europos rusofobų klubą? Ir kas tam pritars ir nuspręs būti ne turtingu ir sveiku, bet vargšu ir ligoniu?

Tik „labai kvaili žmonės“.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 10 — id: `scraped:rubaltic_lt:c1c092dfee47af70`

**Title:** Londonas ir Paryžius privertė TSRS pasirašyti sutartį su Hitleriu: nauji archyvų duomenys

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Sukako 80 metų, kai buvo pasirašyta Tarybų Sąjungos ir Vokietijos nepuolimo sutartis, kuri labiau žinoma kaip Molotovo–Rybentropo paktas. Vakarų istoriografijoje teigiama, jog šis įvykis tapo kruviniausio žmonijos istorijoje konflikto „gaiduku“. Tačiau archyvų duomenys, pateikti internetо projekte „1939 metai. Nuo „sutaikinimo“ prie karo“, liudija kitką. Apie tai, kodėl Tarybų Sąjunga buvo priversta suartėti su Hitleriu, analitiniam portalui RuBaltic.Ru papasakojo Rusijos valstybinio karinio archyvo (RVKA) direktorius Vladimiras Tarasovas.

— Pone Tarasovai, parodoje matome šimtus dokumentų, tačiau RVKA ir kitų įstaigų fonduose jų, žinoma, daug daugiau. Ar galėtumėt paaiškinti, kokiu principu buvo atrenkami dokumentai ekspozicijai?

— Pradėkime tuo, jog šis 1939 metų projektas yra tęsinys kito projekto, skirto Miuncheno suokalbio 80-mečiui. Virtualiai parodai buvo atrinkta beveik dukart daugiau dokumentų nei realiai.

Mes paėmėme laikotarpį nuo 1939 metų kovo 15 dienos iki rugsėjo 23 dienos. Miuncheno suokalbio projektas kaip tik užsibaigė kovą, tai yra kalba ėjo apie jo chronologinį tęsinį. O rugsėjy Lenkija nustojo egzistavusi kaip nepriklausoma valstybė.

Visa, kas svarbiausia ir vertinga pagal šį laikotarpį ir ką pavyko surasti (mūsų archyve ir kitose organizacijose), mes atrinkome parodai. Net iš politinio Vokietijos URM archyvo pavyko gauti trūkstamų dokumentų. Tame tarpe JAV prezidento Ruzvelto telegramą Hitleriui.

Nepateko dokumentai, kurie jei ir nedubliuoja parodoje eksponuojamų, tai ir neturi šiame fone nieko svarbaus.

— Kitam mano klausimui Jūs užbėgote už akių: norėjau Jūsų paprašyti išskirti porą projekto „perliukų“ — įdomiausius dokumentus, kurie, galimai, viešinami pirmąkart. Kokius dar galite prisiminti? Ir kuo įdomi minėta Ruzvelto telegrama?

— Kaip žinia, Ruzveltas iš esmės pritarė Miuncheno susitarimams ir palaimino Didžiosios Britanijos ir Prancūzijos politiką susitaikant su Vokietija. Telegramoje Hitleriui jis bandė atkalbėti jį nuo grobikiškų planų, ragino visus klausimus apsvarstyti tarptautinėje konferencijoje, o taip pat išvardino 31 Europos ir Azijos šalį, kurių atžvilgiu Trečiasis reichas neturėjo imtis jokių agresyvių veiksmų.

Pirmiausia jis liepė savo diplomatams išsiaiškinti, ar Ruzvelto išvardintos šalys įpareigojo JAV kalbėti jų vardu. Paaiškėjo, jog į jį niekas nesikreipė.

Tada pasisakymo Reichstage metu Hitleris nutraukė karinę jūrų sutartį su Didžiąja Britanija ir aštriai pasisakė prieš lenkus. Jo kalba pranašavo tolimesnius Vokietijos agresyvius veiksmus.

Tai labai vertingi šaltiniai, kurie leidžia geriau suvokti, kas tuo metu dėjosi Europos kontinente. Pavyzdžiui, didelio dėmesio vertas 1939 metų kovo 23 dienos specialusis Žvalgybos valdybos pranešimas apie karinius Vokietijos pasiruošimus. Jame konkrečiai pasakyta, kokiu būdu Berlynas stiprino savo kariuomenę.

Mane labai sudomino žemėlapis-plakatas apie Vokietijos teritorijos plėtrą 1938–1948 metais. Jį naciai atvirai platino Prahoje ir Prikarpatės Rusijoje.

Ten aiškiai, terminais nurodyta, kaip bus plečiama Vokietijos teritorija. Ir Hitleris prisilaikė šio plano.

— Rusijos ambasada Kanadoje paviešino savo portale Prancūzijos karinio atašė Maskvoje 1939 metų liepos 13 dienos raštelio kopiją . Į tai atsakydamas vienas naudotojas parašė: „Tai vienas iš daugelio rusų manipuliavimų. Tiesa tame, kad sąjunga su nacių Vokietija buvo dalimi tarybinės Rusijos dienotvarkės“. Ar įmanoma pagal dokumentus nustatyti, būtent kada „sąjunga su Vokietija“ tapo „TSRS dienotvarkės dalimi“? Ir ar išvis pridera kalbėti apie sąjungą?

— Visų 1939 metų eigoje aktyvios derybos vyko įvairiausiomis linijomis.

Šie pasiūlymai, švelniai tariant, buvo paversti plepalais, nes jokių sutarčių su TSRS Europoje niekas neketino pasirašyti.

Be to, Maskva ne kartą siūlė ne kažką abstraktaus — ji norėjo sukurti visavertę sąjungą siekiant užkirsti kelią agresyviems Vokietijos kėslams. Visa tai buvo atmesta.

Tik įsitikinus, jog susitarti su britais ir prancūzais nepavyks, Tarybų Sąjunga persiorientavo į Vokietiją.

Jei mes nebūtume pasirašę sutarties su Vokietija, sieną būtume turėję 30 kilometrų nuo Minsko.

Iki 1939 metų liepos pabaigos Tarybų Sąjunga nesiėmė jokių rimtų žingsnių siekiant priimti Berlyno pasiūlymus, kurie buvo pateikiami ir anksčiau. Vokietija juk suprato, jog tuo metu kariauti dviem frontais (prieš Prancūziją ir Didžiąją Britaniją vakaruose ir prieš Lenkiją su TSRS rytuose) reiškė iš anksto suvokti pralaimėjimą.

Hitleriui buvo svarbu, kad jam užpuolus Lenkiją Tarybų Sąjunga laikytųsi neutraliteto. Todėl jis buvo pasiruošęs nuolaidžiauti, kas galų gale ir įvyko.

Tačiau pasikartosiu: visa tai galėjo įvykti tik po nesėkmingų derybų su Londonu ir Paryžiumi. Tik tada Tarybų Sąjunga atsiliepė į Berlyno iniciatyvas.

Galų gale tikslas buvo pasiektas: karo pradžią nustūmėme. Tai yra galima tvirtinti, jog sutarties pasirašymas buvo naudingas ir Tarybų Sąjungai, ir Vokietijai.

— Ir vis dėlto kodėl žlugo tarybų–britų–prancūzų derybos? Todėl kad Londonas ir Paryžius iš pat pradžių neketino kalbėtis su Maskva? Ar sprendžiamąjį vaidmenį atliko kategoriškas lenkų atsisakymas bendradarbiauti su „raudonaisiais“?

— Manau, teisingi abu tvirtinimai.

Derybų tarp TSRS, Didžiosios Britanijos ir Prancūzijos metu vyravo nepasitikėjimas, tai jautėsi ir net nebuvo slepiama. Yra žinomas britų premjero Čemberleno pasisakymas: „Aš greičiau atsistatydinsiu, nei kalbėsiuos su Tarybų Sąjunga“. Ir susirašinėdamas su seserimi jis atmetė bet kokią susitarimo su Maskva galimybę. Prancūzijos politika buvo kaip Didžiosios Britanijos.

Šiose šalyse buvo žmonių, kurie mąstė racionaliai ir suprato, jog tik bendri su TSRS veiksmai padės pasiekti kokių nors teigiamų poslinkių santykiuose su vokiečiais. Tačiau elito politika buvo kitokia. Iš Tarybų Sąjungos buvo reikalaujama vienpusių įsipareigojimų, o taip elgtis ji, žinoma, negalėjo.

Visa tai ir trikdė tarybų–britų–prancūzų derybas. Tai yra iš Tarybų Sąjungos reikalavo pakilti prieš Trečiąjį reichą, į ką Maskva atsiliepdavo logišku klausimu: „Kaip mes galime tai padaryti, neturėdami su Vokietija sienos?“

Reikėjo praeiti Lenkijos teritoriją. Varšuva to nenorėjo girdėti. Pagrindinio rusofobo vaidmenį, manau, tuo metu atliko Lenkijos užsienio reikalų ministras Juzefas Bekas.

Ir šiaip esą su vokiečiais galima kalbėtis. O Tarybų Sąjunga — barbarai, su kuriais neįmanomi jokie susitarimai.

— Aš suprantu, kad Londonas ir Paryžius ir nesistengė jų kitaip nuteikti?

— Bandė. Įvairaus aktyvumo derybos dėl bendrų veiksmų vyko nuo 1939 metų pavasario. Britai ir prancūzai iki paskutiniųjų stengėsi įtikinti lenkus.

Tik rugpjūčio 25 dieną, po Tarybų Sąjungos–Vokietijos pasirašyto nepuolimo pakto, pavyko išgauti iš Lenkijos gana miglotą formuluotę, jog esant tam tikroms galimybėms ir sąlygoms būtų galima apsvarstyti klausimą dėl bendrų veiksmų su TSRS. Tačiau traukinys jau buvo išvykęs. Veiksmų logika nukrypo pagal kitą scenarijų.

— Į Hitlerio „sutaikinimo“ problemą dabartiniai istorikai žiūri įvairiai. Kai kurie mano, jog Versalio taikos garantai tiesiog suklydo — pasirinko neteisingą elgesio liniją, „pražiopsojo“ monstro atsiradimą. Rusijos ekspertų tarpe vis dažniau girdisi tezė apie tai, jog Vakarai tikslingai vedė Hitlerį prie TSRS sienų. Kurią versiją iš šių patvirtina archyvų duomenys?

— Archyvai patvirtina, jog vakarų šalys išties bandė nukreipti Hitlerio agresiją į rytus. Tai patvirtina Raudonosios armijos žvalgybos duomenys, agentūros informacija, įvairių diplomatų pokalbių įrašai. Beje, mūsų vakarietiški partneriai viso to ir nesistengė nuslėpti.

Žinoma, jie suklydo vertindami Hitlerio galimybes.

Istorija vaizdžiai parodė, ką gali sukelti tokia politika.

— Nusistovėjo nuomonė, jog Molotovo–Rybentropo paktas tapo triuškinančiu europietiškos (visų pirma britų) diplomatijos pralaimėjimu. Britai nesitikėjo, kad Maskva ir Berlynas gali pasirašyti nepuolimo sutartį?

— Sutinku. Britų ir prancūzų diplomatija patyrė smūgį. Ir Londonas išties netikėjo, kad Berlynas gali susitarti su Maskva. Nors Vakaruose buvo aukšto rango žmonių, kurie įžvelgė galimybę tarybų–vokiečių susitarimo, prie kurio prives Prancūzijos ir Didžiosios Britanijos politika. Pavyzdžiui, Prancūzijos karinis atašė Maskvoje Opost Palas.

Tai buvo savo nacionalinių interesų gynimas, ką vėliau pripažino daugelis vakarų politikų. Winstonas Čerčilis rašė, jog Stalino vietoje jis būtų pasielgęs taip pat.

Įdomiai į tarybų–vokiečių sutarties pasirašymą reagavo įvairios šalys.

Paryžiuje buvome priversti imtis papildomų priemonių apsaugant mūsų ambasadą. O Japoniją sukrėtė politinė krizė. Japonai, kūrę planus TSRS teritorijų atžvilgiu, įvertino tarybų–vokiečių sutartį kaip smūgį į nugarą. Tai įtakojo ir tolimesnę Tokijo politiką.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 11 — id: `scraped:rubaltic_lt:b2714a0e5c94825c`

**Title:** 100 Nausėdos dienų: kuo naujas Lietuvos prezidentas skiriasi nuo Grybauskaitės

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Sukako 100 dienų kaip Lietuvos prezidentas Gitanas Nausėda eina valstybės vadovo pareigas. Apie padarytus darbus ir planus ateičiai jis nusprendė atsiskaityti spaudos konferencijoje, bet jokių svarbų pareiškimų joje neskambėjo. Pagal keletą esminių klausimų dėl vidaus bei užsienio reikalų politiką Nausėda tęsia prieš jį buvusio prezidento kryptį. Nors yra ir keletas skirtumų.

Analitinis portalas RuBaltic.Ru išaiškino, kuo naujas Lietuvos lyderis yra panašus į Dalią Grybauskaitę ir kuo skiriasi nuo jos.

Kuo panašus?

1. Euroatlantiniai siekimai

Gitanui Nausėdai, kaip ir Grybauskaitei, Vašingtonas bei Briuselis besilieka pagrindiniais užsienio politikos „švyturiais“. Atsisakymo nuo euroatlantinės krypties jis, matyt, net mintyse nelaiko. Ir priešrinkiminės kampanijos metu prezidentas ne kartą deklaravo ketinimą stiprinti strateginę partnerystę su Jungtinėmis Valstijomis.

Jokių siurprizų čia nėra ir būti negali. Geriausiu atveju iš Nausėdos galima buvo tikėtis tik „pakelti balsą“ kalbant su Briuseliu – panašiai, kaip tai daro kaimyninė Lenkija. Bet lenkiško pūtimosi Lietuvos lyderiui kol kas neužtenka. Su amerikiečiais jis tuo labiau kalba įprastu Baltijos šalių politikams „pataikūno“ tonu.

2. Kolaboracionistų šalininkas

Pirmas šimtas Nausėdos dienų įsiminė garsias skandalais dėl istorinės atminties klausimų. Pagal Vilniaus mero Remigijaus Šimašiaus iniciatyvą sostinėje buvo demontuota memorialinė lenta skirta nacių bendrininkui Jonui Noreikai, kas sukėlė nacionalistų pasipiktinimą.

Nausėda suprato, kad negalės ignoruoti šio konflikto, todėl skyrė sau arbitro vaidmenį ir paragino „įvesti moratoriumą istorinės atminties trynimui“. Tai yra iš esmės nacių bendrininkų asmenybių kulto nuvainikavimo stabdymas.

3. Valstybės saugos galimybių problemos

Lietuvos karinis saugumas jaudina Nausėdą ne mažiau už jo pirmtako. Panašiai kaip Grybauskaitė jis ruošiasi ir toliau didinti respublikos karinį biudžetą, kuris jau viršija 2% nuo šalies BVP.

Naują prezidentą, lygiai taip pat kaip ir ankstesnį, gąsdina aukšta rusų kariuomenės koncentracija Karaliaučiaus srityje.

Idėja nėra nauja: Grybauskaitė irgi vadino priešlėktuvinę gynybą vienu saugos pagrindinių prioritetų.

Pagaliau, Nausėda irgi nori pasiekti pastovaus amerikiečių karinio buvimo savo valstybėje. Lyg nauju būdu atlikta sena daina.

4. Energetinis saugumas

Energetikos sfera kažkodėl tai nelabai domi Gitano Nausėdos, jis niekaip nekomentuoja situacijos su SGD-terminalu Klaipėdoje, kurio išlaikymas skaudžiai smogia po Lietuvos biudžetą.

Jis griežtai kritikuoja dujotiekio „Nord stream – 2“ statybą, nenori įsigyti elektros energijos iš Baltarusijos Astravo AE ir tikisi kuo greičiau pasprukti iš „okupacinio“ BRELL (Baltarusija – Rusija – Estija – Letvija – Lietuva) žiedo.

5. Nenorėjimas bendrauti su Putinu

Skirtingai nuo savo rinkimų oponentės Ingridos Šimonytės Nauseda laikė galimomis derybas su Rusijos prezidentu Vladimiru Putinu. Tačiau šiandien apie tokio susitikimo organizavimą nebeužsiminima.

„Kol kas Ukrainoje tokia situacija, kol mes matom įtampos eskalaciją visame regione, nematau jokio pagrindo ištarti įprastų diplomatiškų, malonų žodelių, o visų pirma neturiu tokios moralinės teisės“, - teigė Nausėda.

Apie priežastis reikėtų kalbėti atskirai, bet faktas išlieka: naujas Lietuvos lyderis, lygiai taip pat kaip Grybauskaitė, nenori siekti ryšių su RF vyriausybe.

Kuo skiriasi?

1. Diplomatiškumas

Dar būdamas kandidatu prezidento pareigoms, Gitanas Nausėda laikėsi santūraus, mandagaus, diplomatiško politiko įvaizdžio, kuris geriau patylės, kai negali pasakyti nieko gero.

Iš vienos pusės Lietuvos prezidentas neleidžia sau įžeisti savo oponentų, kaip tai darė Grybauskaitė. Iš kitos jis įžvalgiai nedaro jokių griežtų pareiškimų Rusijos valdžios pusėn. To dėka aukščiausios valdžios lygio dialogo galimybė vis išlieka.

2. Santykių su Lenkija įtempimo sumažinimas

Per savo pirmą užsienio kelionę Nausėda, kaip ir žadėjo, nuvažiavo į Lenkiją. Beje, padarė tai vos po 4 dienas po inauguracijos. Juo labiau, Varšuvoje Lietuvos prezidentas kukliai mėgino pateisinti Lenkijos Konstitucinio teismo reformą, kurią žiauriai kritikuoja ES.

„Prieš tai, kaip smerkti, mums reikėtų gerai susipažinti su situacija, ir aš manau, kad Lenkijos sprendimas buvo nulemtas noru kovoti su korupcija, su nomenklatūros pasireiškimais teismų sistemoje“, - pasakė Nausėda.

Dalios Grybauskaitės kadencijos pradžioje Lenkijos ir Lietuvos santykiai žymiai ir akivaizdžiai pablogėjo. Bet Nausėdos, kuris daug tikisi iš regioninio bendradarbiavimo, tai aiškiai netenkina.

3. Baltarusijos „prijaukinimas“

Savo kadencijos pirmais metais Dalia Grybauskaitė mėgino būti Baltarusijos „advokatu“ vakaruose. Deja, nieko gero iš šio sumanymo neišėjo: Nausėdos kadencijos pradžiai Minsko ir Vilniaus santykiai pasidarė maksimaliai įtempti. Naujas Lietuvos lyderis ketina tai ištaisyti.

Astravo atominės elektrinės (AE) atžvilgiu kompromisų, greičiausia, būti negali. Nausėda visiškai remia konservatorių „kryžiaus karą“ prieš baltarusišką „atominį monstrą“. Ir net prisideda prie jo. „Įstatymą dėl Astravo AE elektros pirkimų [ir įleidimo] draudimo būtina patvirtinti konkrečių priemonių efektingu planu. Jo sudarymu dabar užsiima mano patarėjai ir vyriausybė“, - pareiškė Nausėda.

Spaudos konferencijos metu Lietuvos prezidentas pakartojo dvi esmines tezes. Visų pirma, kad Vilnius privalo „neslėpti galvos smėlyje, apsimetinėdamas juk kaimyno nėra“. Antra, būtų neteisinga galvoti, kad „jokio Baltarusijos suvereniteto neegzistuoja iš vis“.

Grybauskaitė gi vadovavosi visai kitais supratimais.

4. Geri santykiai su „agrarais“

Lietuvoje vyraujančią valstiečių ir žaliųjų sąjungą (LVŽS) rinkimuose atstovavo savo kandidatas – ministras-pirmininkas Saulius Skvernelis, kol Nausėda „agrarijų“ buvo laikomas Tėvynės sąjungos - Lietuvos krikščionių demokratų (TS-LKD) atstovu. Skvernelis net grasino savo atsistatydinimu, jeigu jis praloštų kam nors iš „konservatorių kandidatų“.

Galų gale prezidentas ir ministras-pirmininkas neblogai susitarė. Seimas veikia įprastu režimu – pertvarkyti valdančią daugumą niekas nemėgina. Vyriausybėje atsirado vos trys nauji ministrai. Užsienio politikos atžvilgiu (pavyzdžiui, Lenkijos ir Baltarusijos kryptimis) Skvernelis remia Nausėdos iniciatyvas.

O Skvernelio sunki liga galėjo būti puiku pretekstu tam, kad atleisti jį nuo pareigų. Grybauskaitė, kuri negalėjo pakęsti Lietuvos vyriausybės pirmininko, greičiausia taip ir pabandytų padaryti.

5. Akcentas į ekonomiką

Savo pagrindiniu tikslu buvęs finansininkas Nausėda deklaruoja „visuotinės gerovės valstybės“ sukūrimą. Kaip tai bus įgyvendinama kol kas neaišku, bet Lietuvos prezidentas nusprendė asmeniškai vadovauti ekonominiams pertvarkymams šalyje.

Pasiūlymai, kuriuos pagal Nausėdos iniciatyvą nagrinėja Seimas ir vyriausybė, susieti su mokesčių sistemos reformavimu, pensijų didinimu, kova su korupcija ir t.t.

Dalia vien tik kritikavo visų Lietuvos vyriausybių, kurios dirbo jos kadencijų metu, darbą, bet socialinei ir ekonominei padėčiai šalyje tai turėjo mažai įtakos.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 12 — id: `scraped:rubaltic_lt:6b8a0ed151461c8c`

**Title:** Lietuva nori pirkti SGD iš JAV, tačiau perka iš Rusijos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos valdžia žadėjo JAV energetikos sekretoriui Rikui Periui pereit nuo vienkartinių amerikiečių SGD pirkimų prie pastovių. Tačiau kol kas Lietuva perėjo tik prie pastovių SGD tiekimų iš Rusijos. SGD terminalas Klaipėdoje draskomas tarp politinės būtinybės pirkti suskystintas dujas iš JAV ir ekonominio būtinumo, kuris priverčia jas įsigyti Rusijoje.

Vilnius sutinka aukšto posto svečio. Į Transatlantinio energetinio bendradarbiavimo konferenciją atvyko “pats” JAV energetikos sekretorius Rikas Peris. Su “obkomo” komandiruotuoju asmeniu mielai bendravo visa aukščiausioji Lietuvos valdžia.

Šalies prezidentas Gitanas Nausėda pabrėžė, kad energetika privalo būti transatlantinio bendradarbiavimo prioritetu. “Europa ir JAV yra daug stipresnės, saugesnės ir sėkmingesnės, kai veikia kartu”, - pabrėžė Nausėda ir tradiciškai “spyrė” rusų ir vokiečių dujotiekį «Nord Stream – 2».

Lietuvos ministras-pirmininkas Saulius Skvernelis žadėjo iš už vandenyno atvykusiam svečiui pereiti nuo vienkartinių mažų amerikietiškų SGD partijų prie pilnaverčių reguliarių tiekimų. JAV SGD eksporto platinimas Baltijos regione paspartins konkurenciją bei suteiks naudos Lietuvos kaimynams mano Skvernelis, protingai nutylėjęs, kad kaimynai jau atsisakė pirkti amerikiečių SGD iš lietuvių SGD-terminalo.

Ideologinį šių pareiškimų foną užtikrina Lietuvos URM vadovas Linas Linkevičius. “Mums tiksliai yra žinoma laisvės kaina, bet mes žinom ir energetinio saugumo kainą. Dar visai neseniai mus kvietė energetine sala blogąja šio žodžio prasme, nes mes buvom visiškai izoliuoti ir priklausėm nuo vieno tiekėjo”, - pasakė Linkevičius ir su niekaip neišnaikinamu komsomolo karščiavimu pridėjo: “Jus mums reikalingi Europoje, reikalingos jūsų skalūnų dujos Europoje. Mes galim naudoti mūsų vartus Klaipėdoje tolimesniam skalūnų dujų transportavimui į Europą”.

Pirmus rusiškų SGD tiekimų į Lietuvą atvejus valstybinės įmonės mėgino nuslėpti. Kai išlaikyti paslaptį nepavyko, jos pradėjo teisintis: maža kur SGD-terminalas Independence perka dujas? Kataras, Norvegija, JAV – viena maža Leningrado srities kilmės SGD partija šiuo atveju nereikšminga.

Deja, atsitiko taip, kad SGD pirkimai iš JAV virto vienkartinėmis akcijomis vardan politikų išpūstų pareiškimų apie transatlantinę energetinę draugystę.

Tanklaiviai su suskystintomis dujomis iš Floridos atkeliavo į Klaipėdą 2017 metų rudenį skambant propagandos trimitui. Ir jau tuomet skambėjo visi tie žodžiai apie Klaipėdos istorinę energetikos tilto tarp Amerikos ir Europos vaidmenį, pirmo Europoje amerikiečių dujų gavėjo vaidmenį ir t.t. Tiktai sudujintas amerikiečių SGD iš Klaipėdos terminalo pirkti niekas nenorėjo, tad šia tema savaime nutilo.

Be visokių politikų ir be visokios retorikos. Vadinti tai pavieniais atvejais nepavyks, nes rusiškų SGD partijos atvyksta reguliariai. Pavadinti jas mini-partijomis, nereikšmingomis viso tiekimo srauto maste, irgi negalima: praėjusį mėnesį Lietuva įsigijo pirmą didelio tonažo rusų kilmės SGD partiją.

Bet ir apsimetinėt, jog nieko tokio ypatingo Klaipėdos SGD terminale nevyksta, nebepavyksta, nes profesionalūs kovotojai prieš Rusiją nustojo net prisimesti. Lietuvos konservatoriai teisingai nurodė vyriausybei, kad Lietuva nupirko SGD-terminalą iš Norvegijos tam, kad turėti alternatyvą rusiškoms dujoms. O galų gale kas? Šis terminalas galutinai pritaikytas rusiškoms SGD?!

Atkreipiant dėmesį į šiuos keblus politinius niuansus JAV administracijos energetikos sekretoriaus vizitas į Vilnių įgyja naują reikšmę.

Už SGD-terminalo statybą Baltijoje agitavo NATO Energetinio saugumo kompetencijos centras Lietuvoje, pavaldus amerikiečiams. Amerikiečiai skatino ir gyrė lietuvius už SGD-terminalo iniciatyvą, galvodami, kad “energetinės nepriklausomybės” projektas atitiks strateginius JAV tikslus Europoje.

Šių tikslų esmė – išstumti Rusiją iš Europos gamtinių dujų rinkos ir užimti jos vietą. Tam ir reikalingi SGD-terminalai vietoj dujotiekių ir suskystintos dujos vietoj įprastų.

Kokie gi “signalai” atkeliauja dabar iš Lietuvos? Keletą kartų savo propagandos tikslais lietuviai nupirko amerikiečių SGD, o tuo pačiu metu slaptai perėjo į rusiškas SGD. Vargu ar tai ir yra taisyklingas energetinės politikos pavyzdys visai Europai?

Kad ir kaip ten būtų, po Riko Perio apsilankymo Lietuvos energetikos ministras iškart pareiškė, kad Lietuva yra pasiruošusi deryboms dėl SGD teikimų iš JAV didinimo.

Tuo pačiu metu Žygimantas Vaičiūnas droviai tarė, kad amerikiečių SGD kaina privalo būti konkurentiška. “Mūsų tikslas nėra pirkti dujas bet kokia kaina, turi būti suteikta konkurentiška rinkoje kaina. Galbūt mes aptarsime, kas kliudo, ir ką dar reikės padaryti tam, kad paskatinti JAV SGD srautus kaip į Europą, taip ir į Baltijos šalis”, - diplomatiškai užsiminė Energetikos ministerijos vadovas dėl to, kad amerikietiškos dujos brangokos, o “mums gal nuolaidelę”...

Nepriklausoma šalis niekada tokioje situacijoje neatsidurtų. Bet nepainiokit nepriklausomos šalies ir Lietuvos. Pastaroji gali ilgai bėdoti dėl pinigų stygiaus, bet galų gale darys taip, kaip “ponas liepė”. Įsigijote sau SGD-terminalą tam, kad pakeisti rusiškas dujas Europoje amerikietiškomis? Valgykit dabar amerikiečių SGD ir nedejuokit.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 13 — id: `scraped:rubaltic_lt:f958a817ca61c032`

**Title:** Hitleris pats nieko nežudė: kaltė už Holokaustą suversta Lietuvai

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Vokiečių leidinys Deutche Welle paskelbė, kad Europos sostinių išvadavimo nuo nacizmo 75 metų proga paleistas Maskvoje fejerverkas yra Molotovo-Ribbentropo pakto jubiliejaus minimas. Šis teiginys puikiai atitinka Europos Parlamento paskelbtą skandalingą rezoliuciją, pagal kurią nepuolimo sutartis pasirašyta tarp TSRS ir Vokietijos yra Antrojo pasaulinio karo priežastis. Balsavimas Europos Parlamente atrodo lyg Rytų Europos Antrojo pasaulinio karo mito pergalė, tačiau daugiau kitų šiame istorijos perrašinėjime laimi Vokietija, o Baltijos šalims bus suversta kaltė, kurią jos norėjo primesti kitiems.

“Antrasis Pasaulinis karas, pats pražūtingas per visą Europos istoriją, yra liūdnai pagarsėjusios Nepuolimo sutarties tarp nacių Vokietijos ir TSRS, taip pat žinomos kaip Molotovo-Ribbentropo paktas, ir jos slaptų protokolų tiesioginė pasėkmė. Pagal sutartį ir jos protokolus du totalitariniai režimai, ketinantys užkariauti pasaulį, dalino Europą į dvį įtakos zonas”, - tai yra pati “skambi” rezoliucijos dėl europiečių atminties svarbumo Europos ateičiai dalis. Rugsėjo 19 dieną rezoliuciją parėmė dauguma Europos Parlamento deputatų.

Šiuolaikiniame media sraute naujienos “gyvena” 3 dienas, bet ši rezoliucija yra aptarinėjama jau savaitę. Joje gausu nemalonų pasažų – ko vertas vien tik Raudonosios Armijos paminklų Europoje smerkimas!

Rytų Europos istorijos politika, pasirodo, yra labai naudinga jų Vakarų Europos bičiuliams.

Visai neatsiktinai kaip tik vokiečių organizacijos per dešimtmečius finansavo Baltijos šalių istorijos perrašinėjimo darbą. Konrado Adenauerio fondo ir panašių organizacijų lėšomis buvo be galo rengiamos konferencijos ir leidžiamos brošiūros apie Molotovo-Ribbentropo paktą, apie komunizmo identiškumą nacizmui ir pan.

Šis istorinės atminties performatavimo procesas buvo rengiamas subtiliai, atidžiai ir beveik nepastebimai. Vokiečių kancleriai Gegužės 9 dienomis lankydavosi Raudonojoje aikštėje ir dėkojo sovietų kariuomenei, kad išlaisvino juos nuo Hitlerio, o Baltijos šalyse šiuomet vasaros mokyklos vokiečių lėšomis buvo skelbiama, kad nacius pakeitė sovietų okupantai.

Vokietijos istorinė politika yra labai apgalvota ir sumani. Jos tikslas atitinka šalies ilgalaikius interesus: išvaduoti Vokietiją nuo kaltės ir atsikratyti visuotinės atsakomybės už Antrojo pasaulinio karo sukėlimą.

Lenkija ir Baltijos šalys šioje politikoje atlieka “naudingų durnų” vaidmenis, kurie savo rankomis traukia iš ugnies kaštonus vokiečiams. Jie galvoja, kad istorinė politika padeda kovoti prieš Rusiją ir padeda sutvirtinti jų pozicijas tarptautinėje arenoje.

Iš tikrųjų jie patys sau kasa duobę.

Kur vyko pačios masinės ir žiaurios žydų žudynės? Nacių okupuotose Rytų Europos teritorijose. Kas vyko genocidą? Vokiečiai? Kodėl gi tokiu atveju vokiečių okupuotoje Danijoje 90% žydų buvo išgelbėti, o okupuotoje Lietuvoje 90% žydų – nužudyti? Gal todėl, kad Danijos karalius viešai lankėsi sinagogoje, kol šiuolaikinės Lietuvos “herojai” apiplėšinėdavo ir žudydavo žydus?

Galima prisiminti ir tuos įvykius, kai genocidas buvo vykdomas vien tik vietos gyventojų pastangomis, tai yra visiškai be Reicho dalyvavimo. Kauno žudynės Lietuvoje ir Lvovo žudynės Ukrainoje įvyko dar prieš tai, kaip į Kauną ir Lvovą įžengė vokiečiai. Raudonoji armija iš šių miestų jau pasitraukė, naciai dar neatvyko, o šiame laiko tarpe ukrainiečiai ir lietuviai nužudė tūkstančius žydų.

Visame istorijos perrašinėjimo komplekse yra tik vienas punktas, kurio “vyresni bičiuliai” neatleidžia ir pagal kurį nesudaro jokių kompromisų su Rytų Europos šalimis. Tai – mėginimai paneigti vietos gyventojų dalyvavimą Holokauste.

Šiuo klausimu jau susimovė Lenkija, kuri Vakarų buvo priversta panaikinti baudžiamąją atsakomybę už kaltinimą lenkus už nacių nusikaltimus. Susimovė ir Lietuva, kai joje buvo nuspręsta persekioti disidentus už teigimus, kad žydus Lietuvoje žudė patys lietuviai.

Ir kai eilinį kartą tos šalys vėl sukliegs “Mes nekaltos aukos ir reikalaujame kompensacijos už okupaciją”, jau ne Rusija bet Vakarų Europa joms atsakys: “O kas žydus žudė? Jus ir žudėt. O ką Hitleris? Juk Hitleris niekam galvų nepramušė Kauno malkinėj?

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 14 — id: `scraped:rubaltic_lt:e10574e7ca232f65`

**Title:** Lietuviai priversti mokėti už Rusijos ir JAV SGD verslą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuva pirmą kartą užpirko suskystintų gamtinių dujų didelio tonažo partiją iš "Jamal SGD" gamyklos. Rusijos dujų pirkimas Klaipėdos SGD terminalui iš vienkartinių akcijų virsta pastoviu procesu. Lietuvos SGD-terminalas, valstybės vyriausybės įrengtas atsižvelgiant į JAV interesus, dabar veikia Rusijos gėriui. JAV ir Rusijos verslą apmokėti tenka įprastiems Lietuvos gyventojams, kurių interesai iš pat pradžios šalies politikus nedomino.

Po kelių bandomųjų smulkių rusiškų SGD partijų pirkimo niekas nebeapsimetinėja. Lietuva nebebando padaryti įspūdį jog bendradarbiavimas su Rusijos energijos gamintojais – tik vienkartinės akcijos, už kurių nesislepia jokia strategija, ir kad rusiškų SGD pirkimai yra niekai paliginus su stambiomis dujų partijomis atgabentomis iš Kataro bei Norvegijos.

Dabar su rusiškų SGD tiekimais viskas yra rimta, tad nei vienas Lietuvos valdininkas nepasakys, kad tai “nieko nereiškia”. Klaipėdos pasiekė pirma gamtinių dujų didelio tonažo partija iš "Jamal SGD" gamyklos.

Rusiškų dujų pirkėjas – mineralinių trąšų gamykla Achema, o pagal kitus duomenis – net valstybinė energijos tiekimo kompanija Ignitis (anksčiau “Lietuvos energijos tiekimas”).

Pagrindinė šios istorijos detalė – stambią rusiškų dujų partiją Lietuva nupirko ne tiesiai iš “Jamal SGD”, o iš tarpininko – prancūzų įmonės Total. SGD iš Jamalo Nencų autonominės apygardos iš pradžių buvo atgabentos į Prancūzijos Atlanto pakrantę, kur buvo perkeltos į prancūzų dujų tankerį, o pastaruoju atgabentos jau į Lietuvą.

Kam buvo tai padaryta? Tam, kad Lietuvos vyriausybė galėtų pasiteisinti prieš rinkėjus ir save, jog pagal dokumentus gautos dujos neva esančios ne rusiškos. O kitaip gaunama, kad SGD terminalas Klaipėdoje, sukurtas kaip alternatyva Rusijos dujoms, rusiškos dujoms ir buvo galų gale pritaikytas.

Tam, kad išvengti tokios nemalonios situacijos, Lietuvos politikai nepasigailėjo pinigų tarpininkui ir prailgintai logistikai, kuri irgi turėjo įtakos dujų galutinei kainai. Ir šita detalė iš tikrųjų yra reikšminga.

Visų pirma iš Lietuvos SGD terminalo pasipelnė Jungtinės Amerikos Valstijos. JAV nerūpėjo nei Lietuvos “energetinė nepriklausomybė”, nei šalies “atkakli” kova prieš neapkenčiamo Gazpromo monopoliją. Amerikiečiams, tiesą pasakius, Lietuva visiškai nerūpėjo.

JAV reikėjo pertvarkyti Europos dujų rinką taip, kad joje vietoj ilgalaikių vamzdinių dujų tiekimo kontraktų įsivyrautų vienkartiniai atskirų SGD partijų tiekimo kontraktai. Tam laikui už Atlanto vandenyno jau įvyko skalūnų revoliucija, bet įrengti dujų tiekimo vamzdį iš JAV į Europą vandenyno dugnu buvo nerealu. Tam, kad užtikrinti rinką savo eksportui, amerikiečiai tikėjosi pakeisti “žaidimo taisykles”, kad visiškai nugalėti Rusiją rungtinėje už dujų tiekimus Europai.

Šiuo tikslu Vašingtonas visas paklusnias JAV Europos valstybes pradėjo įkalbinėti statyti SGD terminalus. Vilniuje, tam, kad kuo greičiau primesti šitą idėją ir kitoms Europos valstybėms, 2012 metais buvo įrengtas NATO Energetinio saugumo kompetencijos centras.

Lietuvos Respublikos, kuri visada pasižymi ryžtumu įrodyti savo ištikimybę amerikiečiams, ilgai įkalbinėti neteko. Tuometinė valstybės vadovė Dalia Grybauskaitė, nepaisant visų klausimų ir abejonių dėl to, kiek kainuos lietuviams nuosavas sudujinimo įrenginys bei kokia bus tokiu atveju dujų kaina, liepė išsinuomoti Norvegijoje SGD terminalą Independence ir iškilniai pristatė jį Klaipėdoje.

Iš amerikiečių Lietuva už tokį neabejotiną ištikimybės įrodymą gavo nuoširdų “ačiū” ir nei cento finansinės paramos. Su Independence išlaikymu, kuris atnešė tik nuostolių, teko susidoroti patiems.

Bet jei anksčiau Lietuvos valdžia save ramindavo tuo, kad šalis turi alternatyvą Rusijos dujoms ir ji įrodė savo energetinę nepriklausomybę Putinui, šiuomet viskas galutinai susipainiojo.

Vašingtonui pavyko pakeisti žaidimo taisykles ir pridėti prie ilgalaikių vamzdinių dujų tiekimo kontraktų ir vienkartinius SGD tiekimus. Bet Rusijai pasisekė iš karto prisitaikyti prie naujų sąlygų ir jau šiandien aplenkti JAV pagal SGD eksportą.

Rusijos energijos gamintojai pastatė suskystinimo ir sudujinimo gamyklų, pristatė rinkoje savo palankias sąlygas, ir kaip tik reikalinga Rusijos SGD priėmimui infrastruktūra Europoje jau buvo paruošta.

Juokingiausia yra tai, kad šita infrastuktūra buvo kuriama “prieš Rusiją”. Dabar gi europietiškuose SGD-terminaluose viename po kito talpinamos rusiškos dujos. Jų skaičiuje ir lietuviškas terminalas Independence – energetinis projektas su pačia antirusiška ideologija tarp visų SGD terminalų.

Deja, pačiai Lietuvai jokio pelno iš jos vyriausybės kvailų energetinių išsišokimų nėra. Rusiškos vamzdinės dujos bet kuriuo atveju kainuoja mažiau nei SGD, o pirkti rusiškas SGD tenka tik todėl, kad bet kurios kitos – dar brangesnės.

Iš Lietuvos “energetinės nepriklausomybės” pasipelnė Norvegija, kuri išnuomojo valstybei sudujinimo įrenginį Independence; JAV, kurios neišleido nei cento, bet įgyvendino savo interesus Europoje; Rusija, kuri gavo infrastruktūrą savo SGD eksportui ir kuriai irgi nereikėjo išleisti lėšų tokios infrastruktūros statybai.

Net Prancūzija, kuri, atrodo, yra nieko dėta, pasipelnė iš Lietuvos kompleksų ir psichikos traumų, kai gavo mokestį už tarpininkavimą, kad rusiškos dujos bent anot dokumentų atrodytų nerusiškomis.

Taigi, laimėjo visi...

Išskyrus lietuvius, kurie jau penkis metus yra priversti tempti “energetinės nepriklausomybės” naštą ir apmokėti iš savo mokesčių svetimą pelną.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 15 — id: `scraped:rubaltic_lt:8cb5ceb332cc5422`

**Title:** Lietuvos propaganda ir Chodorkovskis parodė Rusijos didybę

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Oficialioji Lietuvos propaganda vykdė užsakymą diskredituoti Rusijos atstovybę Lietuvoje. Rusijos diplomatų juodinimu buvo užsiėmę Lietuvos valdžioms artimi buvusio oligarcho Michailo Chodorkovskio bendrininkai. Jų bendras produktas primena juokingą nesąmonę: tarp tradicinių Lietuvai šnipų šmėklų ir paranojos šmirinėja faktai, kurie jokiu būdu nediskredituoja Rusijos atstovybės — jie rodo Rusijos didybę.

„Prisidengdami diplomatine tarnyba, Rusijos atstovybėse darbuojasi Užsienio žvalgybos tarnybos (UŽT — politinė žvalgyba), Federalinės saugumo tarnybos (FST) tarnautojai, o taip pat oficialūs karinių atašė aparatų šnipai, kaip taisyklė baigę Antrąjį Rusijos gynybos ministerijos Agentūrinės operatyvinės žvalgybos fakultetą (žvalgų žargonu — „Konservatoriją“), — taip prasideda „tyrimas“, kurį pagal Lietuvos valstybinės televizijos ir radijo kompanijos (LRT) užsakymą atliko Michailo Chodorkovskio centras „Dosje“.

Kokiu tikslu LRT reikia visa tai įrodinėti, matosi jau teksto „įžangoje“. Lietuvos valdžios turi kažkaip motyvuoti eilinį „raganų medžioklės“ sezoną, kurio auka šį kartą tapo Seimo deputatė Irina Rozova. Todėl kad istorijoje su Rozova Lietuvos politikai pasireiškė visiškai beviltiškais paranojikais.

Viena iš „Rusų aljanso“ vadovių kaltinama, jog yra Tarptautinės pravoslavų asamblėjos sudėtyje ir bendrauja su Rusijos atstovybės diplomatais. Abiem temom peršasi sakramentinis klausimas: ir ką?

Tarptautinėje pravoslavų asamblėjoje galima sutikti dviejų dešimčių šalių parlamentarus, Lietuva viena iš tų šalių — šio formato steigėjų, ir 2003 metais asamblėja posėdžiavo Vilniuje. O kas dėl susitikimų su Rusijos atstovybės diplomatais, tai tam jie ir yra diplomatai, kad bendrautų su piliečiais tos šalies, kurioje darbuojasi, ir tuo vystytų tarpvalstybinius santykius.

Taip kad Rozovos kaltinimas valstybės išdavyste atrodo kaip drebėjimas prieš šnipų šmėklas ir sezoninis paranojos paaštrėjimas. Ypač Lietuvos valdžią įsiutino, kad Rusijos ambasadorius Lietuvoje Aleksandras Udalcovas tiesiog pirštu bakstelėjo, pavadindamas Rozovą „politinio persekiojimo auka“.

Vykdyti šį užsakymą kartu su Rusijos opozicija LRT ėmėsi energingai. Kas gi išaiškėjo „tyrimo“ metu?

Aleksandras Udalcovas — anūkas revoliucionieriaus Ivano Udalcovo, kurio vardu pavadinta viena Maskvos gatvė. Stalino laikais buvęs pogrindininkas Udalcovas dirbo Maskvos valstybinio universiteto rektorium, tapo vienu iš MVTSI (Maskvos valstybinis tarptautinių santykių institutas) įkūrėjų ir pirmuoju jo vadovu. Rusijos ambasadoriaus Lietuvoje sūnėnas Sergejus Udalcovas — kairysis radikalas ekstremistas, keletą metų sėdėjęs pagal „Bolotnoje“ bylą.

Dauguma Udalcovo darbuotojų taip pat baigė MVTSI (tiesiog keista, kad būsimieji diplomatai pasirinko būtent šią aukštąją mokyklą). Pirmasis atstovybės sekretorius — žinomo mokslininko sūnus ir anūkas Raudonosios armijos generolo, Didžiojo Tėvynės karo metais TSRS gynybos ministerijos Generalio štabo viršininko pavaduotojo. Antrojo sekretoriaus tėvas dirbo „Gazprome“, vieno atašė brolis prokuroras, o patarėjo tėvas tarnauja Rusijos atstovybėje Berlyne.

Kaip Rusijos diplomatų giminystės ryšių išvardinimas įrodo, kad atstovybės tikslas — užverbuoti kuo daugiau Lietuvos piliečių? Kad ir visi atstovybės darbuotojai būtų Štirlico proanūkai, kuo gali motyvuoti Irinos Rozovos kaltintojai?

„Dosje“ centro ir LRT „tyrimai“ labiausiai primena klasikinį anekdotą apie erotomaną, kuris visur mato lytinį organą. „Daktare, ir iš kur pas jus tokie paveikslėliai?“

Taip ir čia stengiamasi visur matyti ryšį su Rusijos žvalgyba. Juk apie MVTSI sakoma, jog ten knibžda visokiausios specialiosios tarnybos, o Rusijos ambasadoje darbuojasi vien tik šio instituto diplomais apginkluoti žmonės. Ir ką? Visose atstovybėse darbuojasi diplomatinę priedangą turintys žvalgai, o Rusijos atstovybė Lietuvoje tokia pat, kaip visos kitos. Ir ką?

Vieno Aleksandro Udalcovo darbuotojo automobilis įregistruotas name, esančiame gatvėje... kieno gi? Teisingai, Ivano Udalcovo. Šio namo butai esą buvo išdalinti Užsienio žvalgybos tarnybos darbuotojams, todėl jis esą vadinamas „šnipų namu“. Jeigu Rusijos atstovybės darbuotojas priregistruotas „šnipų name“, tai jau akivaizdus įrodymas, jog jis pats šnipas. O jeigu „šnipų namas“ Maskvoje stovi Udalcovo gatvėje, tai Rusijos ambasadorius Lietuvoje taip pat šnipas.

Ir todėl su užduotimi įrodyti, jog kiekvienas lietuvis, sutikęs bendrauti su Rusijos diplomatais, yra nusikaltęs valstybei, taigi tėvynės išdavikas, visiškai nesusidorota.

Vienoje iš mažiausiai įtakingų Europos šalių Lietuvoje Rusijos atstovybėje dirba iškilių valstybės veikėjų, kariškių, mokslininkų palikuonys. Įžvelgti šiame kartų tęsiamume „blatą“, apie kurį įkyriai kalba Chodorkovskio centras, gali tik žmogus, nežinantis, kokie diplomatų atlyginimai, nekalbant apie tai, kokie jie „laimingi“, dirbdami tokioje palaimingoje šalyje kaip Lietuva.

Ir vis dėlto jie dirba, dirba sėkmingai, jei jau pagrindinis Lietuvos žiniasklaidos ruporas de-fakto ir de-jure ant greitųjų iškepa apie juos užsakymo blyną. Dirgina nervus. Erzina.

Gal ir tuo, jog pati Lietuva savo bandymą tapti galinga šalimi sužlugdė dar XVI amžiuje.

Ir ką dabar Vilnius gali priešpastatyti Rusijos diplomatijos mokyklai ir valstybingumo tradicijai? Keletą dvigubų agentų kartų — profesionalių Landsbergių išdavikų?

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 16 — id: `scraped:rubaltic_lt:061f4c7defdbc081`

**Title:** Lietuvos propaganda vėl įvarė save į kampą: kažkas ne taip DELFI tekstuose apie Rusiją

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos DELFI nutarė duoti atkirtį mūsų portalui, nutvėrusiam juos meluojant apie Kaliningradą. Ir tada didžiausias Lietuvos internet-portalas vėl tūpė balon, įveldamas daug faktinių klaidų. Beje, skleisti neapykantą ir meluoti apie viską, kas liečia Rusiją, jau tapo būtinu elementu Lietuvos „nepriklausomos“ žurnalistikos darbe.

Pasakojimas giliai žvelgiančio lietuvio Chuberto, kurio estetinius jausmus papiktino išvyka į Kaliningrado sritį, iššaukė galingą rezonansą ir Lietuvoje, ir Kaliningrade. Rezonansas tik negatyvus — ir ten, ir čia.

Pakanka paskaityti komentarus rašiniui apie Lietuvos pilietį, kuris po apsilankymo Kaliningrade nutarė daugiau niekada ten nevažiuoti, kad suprastumėt ką galvoja brangūs skaitytojai apie portalą DELFI. Įdomu tai, kad komentarų skaičius pastarosiomis dienomis tai didėjo, tai mažėjo; akivaizdu, „brangioji redakcija“ šalino „dėkingų“ skaitytojų atsiliepimus apie save.

Ignoruoti kritikos srautą DELFI redakcija nepajėgė, o atsakinėti į kritiką šis garbus portalas gali vieninteliu būdu: skelbti kritikuojančius „Kremliaus propagandistais“. Taip atsitiko ir šį kartą.

Redakcija skubotai iškepė tekstą „DELFI provokacija Rusijoje išprovokavo isteriją“, kurio liūto dalis skirta analitiniam portalui RuBaltic.Ru, apkaltinusiam Lietuvos valdžiai paklusnų internet-portalą neapykantos ir melo skleidimu apie Kaliningradą.

Aukštyn kojom apversta viskas: juridiniai RuBaltic.Ru ryšiai, jo auditorijos kiekis ir struktūra. Neanalizuosime faktų ir nesiimsime DELFI redaktorių darbo. Visa informacija apie portalą lengvai prieinama: tik būtina mokėti naudotis internetu.

Pakanka pasakyti, jog „liūdnai pagarsėjęs“ šių eilučių autorius jokiu būdu nėra įkūrėjas RuBaltic.Ru „propagandinių naujienų kalvės“, o pusės metų mūsų portalo auditoriją sudaro ne 350 tūkstančių, o 3,2 milijono skaitytojų.

Ir čia jaučiasi kažkokia patologija. Lietuvos leidinys bando parodyti dantis straipsniui, kuris nutvėrė jį meluojant, ir vėl pateikti suklastotą informaciją.

Į tai dėmesys buvo atkreiptas visų pirma Kaliningrado srityje. Gal irnevertėtų kreipti dėmesio į paistalus apie nuostabius lietuvio nuotykius Kaliningrade ir mafijų tinklus miesto viešbučiuose, apie gyventojų rūbus „lyg iš sovietinio turgaus“, apie „visišką bardaką“ keliuose. Visa tai galima vertinti kaip asmeninius pasakotojo įspūdžius, kurie neįrodomi ir nepaneigiami. Chubertas — menininkas, jis taip matė.

Psichologijoje egzistuoja mitomanijos ir patologinio melo sąvokos. Tai kada žmogus meluoja nesustodamas, nes negali nemeluoti. Jam nėra reikalo meluoti, jam nesėkminga meluoti, jo melas akivaizdus, klastotė tuoj pat atskleidžiama ir atstumia nuo jo žmones. Ir net pats patologinis melagis tai supranta. Tačiau jis vis tiek tebemeluoja, nes nepajėgia savęs kontroliuoti.

Mitomanija — sunkus psichinis susirgimas, kurį iššaukia, kaip taisyklė, menkas savęs įvertinimas, nepilnavertiškumo kompleksas. Žmogus liguistai varžosi tokio savęs, bijo aplinkinių patyčių, bando nuslėpti kamuojančią apie save tiesą ir todėl pradeda meluoti, kad jis buvo pilietinio karo Amazonėje didvyris arba pakerėjo tūkstančio moterų širdis.

Paimkime Delfi. „Rusija aneksavo Krymą. Rusija dislokavo kariuomenę. Rusija pasmerkė, Rusija parėmė, pasodino, pareiškė, paneigė. Kiekvieną dieną atsiranda šimtai ir net tūkstančiai naujienų apie tai, ką vėl padarė Rusija. Dažniausiai tai nelabai geros naujienos — apie politinius teisminius procesus, santykius su Ukraina arba, geriausiu atveju, kovinių delfinų mobilizavimas pasienio tarnybon“, — teigiama viename reportaže apie Rusiją.

Pirmasis šio ciklo straipsnis pavadintas savotiškai: „Ten, kur Rusija. Kelio pradžia ir baimės kvapas“.Užbaigiamas šis straipsnis sakramentiniu klausimu: „Po dviejų savaičių, keliaudamas atgal, kai priartėjau prie rusų muitinės, vėl klausiau savęs, ko gi aš bijau?“

Ir iš tiesų, ko gi bijo šis lietuvaitis, jeigu masiškas lietuvių antplūdis į Kaliningrado sritį iššaukia tokias liguistas fantazijas, kaip pasakojimas apie nuostabius lietuvio Chuberto nuotykius Kaliningrade, iš kurių šaiposi patys lietuviai?

Kuo paaiškinti, jog Lietuvos didžiausio ir skaitomiausio internet-portalo žurnalistai nepajėgia Google žemėlapiuose sužinoti, kiek Kaliningrade prekybos centrų, ir paskui skelbia akivaizdžią nesąmonę? Nebent tuo, jog normalūs žurnalistai iš šios šalies išvyko į Airiją rūšiuoti dėžučių, o liko tik kreivarankiai kopijuotojai, kuriuos Lietuvos prezidentas apdovanoja ne už profesionalizmą, o už „teisingą“ požiūrį į Rusiją.

Lietuvos žurnalistikos degradavimas — vienas iš Lietuvos humanitarinės sferos degradavimo pasireiškimų. Jeigu šalies vadovybės myluojamas vedantysis internet-portalas nemato nieko tokio, jog prasta žmonių apranga siejama su jų tautybe, tai jau dugnas.

Beje, lietuviškosios DELFI panašiuose dugnuose atsiduria dažnai.

„Mane stebina DELFI, vieno iš stambiausių lietuvos naujienų portalo, lygis. Norėtųsi palinkėti jo kolektyvui daugiau savigarbos kaip profesionaliems žurnalistams, o svarbiausia — gerbti savo skaitytojus“, — ryšium su tuo pareiškė RuBaltic.Ru Rusijos ambasadorius Lietuvoje Aleksandras Udalcovas.

Mes neketiname pamėgdžioti Lietuvos DELFI — neraginsim jų neskaityti. Skaitykite ką tik norite, brangūs mūsų kaimynai lietuviai, ir lankykitės Kaliningrado srityje, į kurią dabar galima važiuoti nemokamai, apiforminus elektroninę vizą.

Patys viską pamatysite ir patys padarysite išvadas apie savo politikus ir jų ruporus, kurie neleidžia, draudžia ir meluoja, siekiant sulaikyti jus savame ribotame ir baimingame pasaulėlyje.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 17 — id: `scraped:rubaltic_lt:3edd1e4029ceb065`

**Title:** Šeši „landsbergininkų“ pralaimėjimai, dėl kurių Landsbergis kraustosi iš proto

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Pastaruoju metu Lietuvos politikos „patriarchą“ akivaizdžiai kamuoja psichinė negalia. „Tautos tėvas“ prognozuoja, jog po to, kai rikiuotėn bus įvesta Baltarusijos AE, jo šalį lauks „branduolinė mirtis“, kaltina Gorbačiovą nuslėpus slaptuosius Molotovo – Rybentropo pakto protokolus ir koneveikia AMAZON dėl kūjo ir pjautuvo ant futbolininkų marškinėlių. Dėdulę galima suprasti: pastaruoju metu jam ir jo partijai nesiseka. Analitinis portalas RuBaltic.Ru nustatė 6 Lietuvos konservatorių pralaimėjimus, dėl kurių Landsbergiui „važiuoja stogas“.

1. Naujo prezidento atžarumas

Akivaizdu, jog „Tėvynės sąjunga – Lietuvos krikščionys demokratai“ iki šiol neatsipeikėjo po preėzidento rinkimų. Antrame rate rinkėjai „pavijo“ jų kandidatę Ingridą Šimonytę, kurią jie matė Dalios Grybauskaitės paveldėtoja.

Rinkimus laimėjęs Gitanas Nausėda neabejotinai suvokė, ką reiškia balsavimo rezultatai.

Pavyzdžiui, naujasis prezidentas vykdo ikirinkiminius pažadus ir nekoneveikia savo rytų kaimynės, ką darė Dalia Grybauskaitė (esą, ne viską daro ideologiniame fronte). Pirmasis jo vizitas — į Lenkiją, su kurios vadovais iš pat pradžių nesusiklostė Grybauskaitės — ištikimos Landsbergio bendražygės — santykiai. Nuostabu: Nausėda neblogai sutaria su valdžioje esančiais „valstiečiais“.

Prieš prezidento rinkimus premjeras ir „valstiečių“ kandidatas Saulius Skvernelis skelbėsi pralaimėjimo atveju pasitrauksiąs iš pareigų. Po rinkimų persigalvojo. Nausėdai pritarus, vyriausybės vadovas liko pareigose, toliau darbuojasi beveik visi ministrai.

Politinės kryptys Lietuvoje nesikeičia, Nausėda nerodo noro jas peržiūrėti. Tačiau konservatoriams jis taip ir lieka ne pačiu patogiausiu prezidentu.

2. Kapituliuota Baltarusijos elektrinei

Atrodytų, apie Baltarusijos AE Lietuvoje pasakyta viskas ir net daugiau. Tačiau šiuo metu Landsbergis vis dėlto įkopė į aukščiausią savo skurdaus protavimo viršūnę — apkaltino Rusiją paskelbus Europai „branduolinį karą“.

„Tai jėgos demonstravimo politika, ne sutarčių ar derybų — tai diktato politika, nes jie galvoja, jog labai galingi. Taip, jie turi galią — tai bomba Ostrovece. Bomba, pakibusi virš rytinės ES dalies, pirmiausia — virš Lietuvos“, — pareiškė Lietuvos konservatorių lyderis.

Kas tai, jei ne nevilties šauksmas?

Vilniaus kovos su Baltarusijos AE rezultatai liūdni: elektrinę baigiama statyti, o vartus į Europą jai atvers latviai.

Po skandalingos naujienos, jog Ryga perkelia prekybą elektros energija su trečiomis šalimis prie sienos su Rusija, Latvijos premjeras Krišjanis Karinš suskubo ieškoti pasiteisinimų — esą, žiniasklaida neteisingai intepretavo vyriausybės nutarimą, nes nebuvo kalbos apie Baltarusijos AE produkcijos pirkimą. Kiek vėliau jis patikino Skvernelį, jog „sprendimo pirkti Ostroveco elektrinės energiją Latvijos vyriausybė nepriėmė“.

Tačiau Latvijos valdžiai nebūtina priimti nutarimą pirkti Baltarusijos elektros energiją.

Apie tai susitikęs su kolegomis iš Lietuvos užsiminė pats Karinš, pasakydamas, jog elektros energijos rinka — atvira. Aiškintis, kur atsirado kiekvienas kilovatas, niekas neketina.

Lietuvos vadovai tebevaizduoja save galingais.

Ir vertėtų pagalvoti apie taikos sutartį bent kiek palankiomis sąlygomis (jei tokiu atveju dar galima kalbėti apie palankumą).

3. Nacių talkininkų kulto demaskavimas

Žlugus TSRS, „landsbergininkai“ iš peties padirbėjo suteikdami „miško broliams“ tautos didvyrių vardus ir neginčijamus moralės autoritetus.

Tokie atsirado ir konservatorių „užnugaryje“ — sostinės miesto taryboje. Vietos valdžios nutarimu Vilniuje pervardinta Lietuvos aktyvistų fronto įkūrėjo Kazio Škirpos alėja. Kiek vėliau miesto mero Remigijaus Šimašiaus nurodymu buvo demontuota paminklinė lenta kitam „didvyriui“ — Jonui Noreikai — generolui Vėtrai.

Ir savo poziciją miesto vadovas kietai argumentavo Lietuvos prezidentui. Šimašiaus nuomone, Noreikos kova su „sovietiniais okupantais“ pelnė pagarbos, tačiau Lietuvos sukilėlių lyderis „elgėsi ir kitaip, ko negalima pateisinti“.

Noreika — galimai šlykščiausias lietuviško didvyriško epo personažas, „išprausti“ kurį neįmanoma jokiomis priemonėmis. Praeitais metais nuo jo nusisuko respublikos užsienio reikalų ministras Linas Linkevičius.

Deja, tada toliau kalbų reikalai nepajudėjo. Smagračiai ėmė suktis tik dabar, o tai — nekoks ženklas Dėdulei.

4. Nauja senoji vyriausybė

Kaip jau buvo pasakyta, naujasis prezidentas tuoj pat surado bendrą kalbą su vadovaujančia „agrarijų“ partija. Ir todėl vykdomoji valdžia patyrė tik neesminius pokyčius: savo postus prarado trys ministrai, o paskui Seimas savo pasitikėjimą vyriausybe patvirtino balsavimu.

Konservatorių nuomone, Seimas privalėjo balsuoti vyriausybės programos klausimu — ankstesnioji buvo patvirtinta 2016 metais, ir nuo tada Skvernelio kabinete pasikeitė daugiau kaip pusė ministrų.

„Landsbergininkai“ tikėjosi, kad Skvernelio pralaimėjimas prezidento rinkimuose smogs „valstiečių“ pozicijoms parlamente ir vyriausybėje. Kol kas valdančioji partija laikosi.

5. Smūgis Grybauskaitei

Tarp pretendentų į aukščiausius ES postus nesimatė buvusios prezidentės Dalios Grybauskaitės. Po to ji galėjo tikėtis kokios nors kuklios eurokomisarės pareigų, tačiau prieš tai jai reikėjo užsitikrinti paramą pačioje Lietuvoje.

Kaip paaiškėjo, ir šiame etape ponia Dalia susidūrė su problemomis. Kandidatų iškėlimas respublikoje užsitęsė, nes tapti eurokomisarais pageidavo keli žmonės.

Lietuvos kandidatu tapo ekonomikos ir inovacijų ministras Virginijus Sinkevičius.

„Tautinės atrankos“ metu konservatoriai atvirai rėmė Grybauskaitę. Gabrielius Landsbergis net siuntė laišką Skverneliui, kuriame argumentavo, kodėl Vilniui Europos parlamente turi atstovauti „labiausiai patyręs asmuo, puikiai žinantis vidaus ir užsienio ES politiką, aukštos tarptautinės reputacijos“.

Po kitos kandidatūros patvirtinimo konservatoriai įjungė atbulinę pavarą. Partijos frakcijos vadovo pavaduotojas Jurgis Razma pareiškė, jos partijoje nebuvo vienybės, kai kas pasisakė prieš Sinkevičiaus kandidatūrą, o kai kas parėmė. Žinoma, tokios kalbos vargšų naudai.

Daug metų Grybauskaitė gynė Tėvynės sąjungos – Lietuvos krikščionių demokratų partijos interesus. Kokius jausmus patyrė Landsbergis, kai jo statytinė tapo nepageidaujama ne tik Europos sąjungoje, bet ir Lietuvoje, nesunku suvokti.

6. „Sovietinė“ simbolika

Vyšnia ant torto — eilinis simbolikos apsireiškimas ant marškinėlių, kuriais prekiauja AMAZON. Šia proga Lietuvos politikos „patriarchas“ asmeniškai kreipėsi į kompanijos įkūrėją Džefą Bezosą: „Jūsų kūrinys AMAZON kai kurias prekes platina su TSRS komunistinės tironijos ir genocido nusikaltimų su hitlerininkais dalyve simbolika. Konkrečiai — „pjautuvas ir kūjis“ pavaizduoti ant sofų pagalvėlių ir vaikų marškinėlių“.

Lietuva, kaip žinia, seniai kaunasi prieš „komunistinės tironijos simboliką“. Ir kaunasi ne beviltiškai: analitinis portalas RuBaltic.Ru jau rašė, jog pasipiktinusių pabaltijiečių spaudžiami tinklai Walmart ir kompanija Adidas nustojo pardavinėję atitinkamas prekes.

Suvokdamas savo amželį, Dėdulė Landsbergis tikriausiai jau mąsto, kokį pasaulį jis paveldės palikuonims. O to optimizmo mažoka: pasaulis visiškai nesuvokia, jog „sovietinė“ simbolika kelia pavojų. O ten, ką gali žinoti, ir Tarybų Sąjunga atsikurs...

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 18 — id: `scraped:rubaltic_lt:1d54d73284819da5`

**Title:** Lietuvos „miško brolių“ gynėjai demaskavo „žydų–Kremliaus“ sąmokslą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Po to, kai Vilniuje buvo uždaryta sinagoga, vietos nacionalistai apkaltino Lietuvos žydų bendruomenės (LŽB) pirmininkę Fainą Kuklianski dirbant Kremliaus labui. Nacių nusikaltėlių gynimo mitinge buvo iškelti plakatai su užrašais „Lietuvos žydų bendruomenė — Kremliaus filialas?“ ir „Putinas myli Kuklianski“. Dar daugiau — Rusijos pėdsaką antisemitinio skandalo metu aptiko konservatorių lyderis Vytautas Landsbergis. Ir tai nenuostabu: esant norui, Lietuvoje galima surasti ištisą „žydų–Kremliaus sąmokslą“ su šaknimis istorijoje.

LŽB nutarimas po nacionalistų grasinimų uždaryti savo būstinę ir sostinės sinagogą nevienareikšmiai buvo sutiktas ir tarp lietuvių, ir tarp pačių žydų. Penki Bendruomenės regioninių skyrių pirmininkai sukritikavo poziciją Kuklianski, kuri „nekorektiškai pasisakė, tokiu būdu galimai nuteikdama prieš Lietuvos žydus kitą Lietuvos visuomenės dalį“.

Ar tikrai LŽB susipriešinta sinagogos uždarymo klausimu, ar Kuklianski oponentai tiesiog pasinaudojo šia istorija, kad galėtų paleisti į ją strėles? Belieka tik spėlioti.

Bet kokiu atveju Bendruomenės vadovybė akivaizdžiai tikėjosi sulaukti Lietuvos valdžios reakcijos. Valdžios sureagavo, tik nevienodai.

Prezidentas Gitanas Nausėda nepasakė nieko konkretaus — apsiribojo miglotais raginimais nesipykti ir nesuteikti „galimybės džiūgauti Lietuvos priešams, kokie jie bebūtų — vidaus ar išorės“.

Vilniaus meras Remigijus Šimašius patikino, kad žydai gali jaustis ramiai. Tokia pat pozicija ir premjero Sauliaus Skvernelio, kuris, beje, paragino teisėsaugininkus sudėlioti visus i taškus.

„Premjeras ragina teisėsaugos organus nedelsiant imtis priemonių, užkirsti kelią visokiems tarpnacionalinių kivirčų elementams ir, esant būtinybei, panaudoti kitas įstatymo numatytas priemones“, — teigiama vyriausybės pranešime.

Pačiais griežčiausiais komentarais, kaip ir buvo tikėtasi, pasižymėjo Lietuvos politikos „patriarchas“ Vytautas Landsbergis. Akivaizdu, jog būtent konservatorių partiją Kuklianski apkaltino nuolaidžiavimu antisemitinei propagandai ir garbinimu karo nusikaltėlių, dalyvavusių žydų naikinime.

„Dabar turi nuskambėti visame pasaulyje, kad žydai Lietuvoje taip baisiai persekiojami, jog jie net uždarė sinagogą. Aišku, kam tai gali būti naudinga: Kremliui geresnės dovanos nereikia“, — kandžiai pasišaipė politikas.

Žinoma, „dovaną“ Kremliui Kuklianski pateikė esą ne specialiai, o dėl savo kvailumo. Na, ir pati Bendruomenė, jei tikėti Landsbergiu, šioje istorijoje niekuo dėta. „Nemanau, kad tai Bendruomenė, aš matau vieno žmogaus aklumą. Kaip Šimašius nesuprato, ką daro, dabar turbūt Kuklianski nesupranta“.

Išpuolis miesto mero atžvilgiu pateisinamas, tačiau nelogiškas. Šimašius akivaizdžiai nepanašus į žmogų, kuris nesupranta, ką daro. Priešingai, jis jau paaiškino prezidentui, kodėl nuėmė lentą Jonui Noreikai, ir pareiškė, jog ruošiasi pateikti peržiūrėjimo Vilniuje įamžinimo politikos planą.

Nacionalistai, įsitikinę, jog pasitelkus rusofobiją galima apginti net aršiausius niekšus, Šimašiaus nepalaiko. Savo nepasitenkinimą jie nutarė pareikšti mitinge rugpjūčio 7 dieną, kurio metu Vilniaus meras taip pat pateko į „Kremliui naudingų idiotų“ sąrašą.

Galų gale, kas bando „perrašyti istoriją pagrindu kaltinimų, sukurptų okupacinės sovietų valdžios represinėmis struktūromis?“ Tai Lietuvos užsienio reikalų viceministro Albino Zananavičiaus formuluotė — taip jis aiškino Rusijos ambasadoriui Aleksandrui Udalcovui, kad neverta juodinti „miško brolių“ vado Adolfo Ramanausko–Vanago „gero vardo“.

Bet dabar išaiškėjo, jog ant „sufabrikuotų kaltinimų“ užkibo net Vilniaus meras. Apie Fainą Kuklianski ir kalbos nėra — žydas tradiciškai užima griežtą ir bekompromisinę poziciją visų dabartinės Lietuvos „didvyrių“ atžvilgiu. Todėl tame mitinge, kuriame buvo ginami Noreika ir Škirpa, LŽB pirmininkei taip pat kliuvo.

O svarbiausia „miško brolių“ gynėjai pasakyti užmiršo: kaip reikia reaguoti į tai, kad Lietuvoje Kremlius įgijo žydų „filialą“. Iš kitos pusės, tai sakyti nebūtina. Sprendžiant iš to, jog LŽB pastoviai gauna grąsinančius laiškus, anoniminiai kovotojai už „istorinį teisingumą“ jau pradeda veikti. Ir kuo ryžtingiau Vilniaus valdžios kovos su nacių talkininkų atminimo įamžinimu, tuo labiau sius jų pasekėjai.

„Jis turėjo galvoti, kas iš to gali išeiti“, — taip Landsbergis atsiliepė apie Šimašiaus veiklą. Pareiškimas nors ir ciniškas, bet turintis prasmės. Taip, konservatorių propagandos pripumpuoti nacionalistai, pasiryžę ginti „istorinę Lietuvos atmintį“, suveikė kaip saugiklis.

Skandalas dėl Vilniaus sinagogos uždarymo — tik aisbergo viršūnė. Kuo ne „Kremliaus talkininkas“, pavyzdžiui, Amerikos žydas Grantas Gočinas, kuris, nepavykus sustabdyti Noreikos garbinimo, pareiškė, jog „kiekvienas padorus lietuvis“ turi išvykti iš Lietuvos?

„Aš visiškai pritariu tiems žingsniams, kurių neseniai ėmėsi Lietuvos žydų bendruomenės pirmininkė Faina Kuklianski, laikinai uždarant Vilniaus sinagogą ir visuomeninės organizacijos būstinę dėl daugybės vietos nacionalistų grąsinimų, — RuBaltic.Ru komentare pažymėjo žinomas nacių medžiotojas Simono Vizentalio Centro Jeruzalės skyriaus vadovas Efraimas Zurofas. — Tai atsargos priemonė, kuri, tikimės, privers vyriausybę imtis reikiamų priemonių užtikrinant Lietuvos žydų ir jų institutų saugumą ir gerovę“. Gal ir Simono Vizentalio Centrą dabar metas pavadinti „Kremliaus filialu?“

„Deja, daug istorikų tą mitą palaiko: žydai neva pasirinko Staliną kad išsigelbėtų nuo Hitlerio“, — konstatuoja Vilniaus istorikas Ilja Lempertas.

Besitęsianti isterika dėl Jono Noreikos lentelės nuėmimo, Škirpos alėjos pervadinimo ir Vilniaus sinagogos uždarymo tyliai stumteli nacionalistus link minties, jog žydai ir rusai „Lietuvos fronte“ veikia kartu. Jie patys to dar nežino, tačiau Lietuvai tai tipiška istorija: Rusija, atrodo, iki šiol nesuvokė, kad nori okupuoti Pabaltijį...

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 19 — id: `scraped:rubaltic_lt:310774409f1492b7`

**Title:** Elektroninių vizų efektas: atvira Rusija nugąsdino Lietuvos rusofobus

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Veikiant elektroninių vizų režimui, per mėnesį Kaliningrado srityje apsilankė dešimt tūkstančių užsieniečių. Eksperimento su elektroninėmis vizomis sėkmė viršijo tai, ko buvo tikėtasi, ir ši aplinkybė nedžiugina kaimyninės Lietuvos, iš kurios į Kaliningrado sritį keliauja daugiausia svečių. Masiškas Lietuvos gyventojų apsilankymas šioje srityje kelia baimę jos vadovams: žmonės turi galimybę pamatyti tikrąją Rusiją, o ne tą, kurią jiems sugalvojo valdžioje sėdintys rusofobai.

Baigiantis pirmam supaprastinto vizų režimo mėnesiui dėl noro apsilankyti Kaliningrado srityje buvo pateikta dvidešimt tūkstančių paraiškų elektroninėms vizoms ir dešimt tūkstančių 33 šalių piliečių jau aplankė Kaliningrado sritį su šiomis vizomis. Didžiausias srautas — iš Lietuvos, Latvijos, Lenkijos ir Vokietijos.

Tačiau absoliuti elektroninių vizų čempionė nuo pat pradžių buvo ir tebelieka Lietuva.

Kaliningrade nebuvo tikėtasi tokio galingo efekto. Nereikėjo skirti laiko ypatingai informacijos kampanijai, kad kaimyninės šalies gyventojai imtų plūsti į šią Rusijos sritį. Lengvųjų automobilių eilės prie Lietuvos–Rusijos sienos nusidriekia keletą kilometrų, stovėti jose tenka ne vieną valandą.

Dėmesį į tokią situaciją pirmiausia atkreipė Lietuvos žiniasklaida, veidmainiškai užjaučianti ir tyliai džiūgaudama, teigdama su kokiais sunkumais tenka susidurti tėvynainiams, įstrigusiems kelyje į Kaliningradą. Jos pasisakymų moralė paprasta: nėra ko ten važiuoti.

Tačiau vien tik kritikos kančioms pasienyje nepakanka.

Pastaruoju metu iš savo spaudos ir televizijos kanalų lietuviai galėjo sužinoti, kad rasti Kaliningrade viešbutį ir jame apsigyventi nelengva, o gal ir visiškai neįmanoma, kad Kaliningrado sritis per dešimtmečius nepasikeitė, kad ten viskas pasenę, tai griūvantis „sovietmečio“ palikimas, ir kad po keturių laukimo eilėje valandų rusų pasieniečiai gali jų neįsileisti.

Taigi vėl pasireiškia Lietuvą užvaldžiusi paranoja. Esą Kaliningrado srityje apstu specialių tarnybų, bet kuris pakeleivis visuomeniniame transporte gali būti įpareigotas jus verbuoti, o pagal telefono numerį prisijungus prie WiFi, jūsų duomenys taps žinomi Federalinei saugumo tarnybai.

Taigi reakcija klinikinė. Ir tai tuo metu, kai Kaliningrado sritis Lietuvos istoriografijoje — Mažoji Lietuva, lietuvių kultūros lopšys. Čia gyveno Kristijonas Donelaitis — didysis poetas, lietuvių literatūrinės kalbos pradininkas. Kenigsberge (dabar Kaliningradas), o pagal lietuvių tradicijas Karaliaučiuje, buvo išspausdinta pirmoji lietuviška knyga.

Lietuvos valdžios turėtų išreikšti pasitenkinimą, kad jos piliečiai lanko šią žemę. Tačiau vietoj to Seimo deputatai gąsdina rinkėjus, jog „priešo teritorijoje“ jie visi bus užverbuoti.

Būtina pabrėžti, jog dauguma lietuvių į Kaliningradą vyksta ne nusilenkti Donelaičio atminimui, o išgerti–užkąsti, pailsėti prie jūros, o svarbiausia — šauniai apsipirkti, nes kainos čia parduotuvėse ženkliai mažesnės negu Lietuvoje. Anksčiau lietuviai tuo tikslu važinėjo į Lenkiją, kur kainos taip pat žemesnės, negu Lietuvoje.

Vilniuje šia proga taip pat buvo piktintasi, bet vis dėlto ne tiek. Dėl Kaliningrado — nirštama. Labai jau netikėta visa tai lietuvių ideologijai.

O taip pagal visus „visiškai teisingus“ įsivaizdavimus neturi būti. Tie nelaimingieji kaliningradiečiai turi veržtis į šią „geležinės uždangos“ pusę — į „klestinčią Europą“. Lietuva gi yra Europos sąjungos sudėtyje, koks gali būti lietuviams Kaliningradas? Jiems atviras Paryžius, tačiau jie į jį nesiveržia.

Rusijos regionas jame apsilankiusiam lietuviui grįžus į savą visuomenę atrodo vis labiau patrauklus, o rusofobija sergančiai valdančiai klasei to visiškai nereikia. Kaip dabar Dėdulė Landsbergis pasakos, kad Rusija „visa š–e“, o Vilniaus meras pavadins ją „Mordoru“, jeigu tūkstančiai lietuvių renkasi kelionei „Mordorą“ ir mato realią Rusiją, o ne nusišnekančio „tautos tėvo“ fantazijų vaisių?

Panašiai Pabaltijis pernai reagavo ir į Pasaulio futbolo čempionatą. Atsisakyti čempionato organizavimo Rusijoje garsiau nei Pabaltijo šalys reikalavo nebent Ukraina. Milijonai pasaulio sirgalių pamatė tikrąją, o ne rusofobų sugalvotą Rusiją, ir visą mėnesį informacijų laukas skendo nuostabose, kokia tai nuostabi, šiuolaikiška, atvira ir nuoširdi šalis.

Pabaltijo „Rusijos ekspertams“, aiškinantiems pasaulio visuomenei, koki ši, raketomis apsijuosusi, šalis yra agresyvi, tada beliko griežti dantimis ir užsičiaupti, laukiant, kada užsibaigs ta pragariška kančia.

Tačiau situacija su elektroninėmis vizomis į Rusiją „ekspertams“ dar blogesnė. Supaprastintas vizų režimas veiks ne mėnesį, o pastoviai, ir iš tų šalių, kurioms jis taikomas, piliečių labiausiai jis lies lietuvius.

Aiškinimai, jog klastingas Putinas specialiai lietuviams sukūrė Kaliningrado srityje „Potiomkino kaimą“, o visa kita Rusija tokia, kokią ją piešia „tautos tėvas“ Landsbergis, nepadės. Nuo 2021 metų elektroninės vizos galios visoje Rusijoje. O tai reiškia, jog 2018 metų futbolo čempionato efektas taps pastovus.

Ir žmonės naudojasi šia galimybe ir nustoja tikėti Pabaltijo „svieto lygintojams“, kurie nori juos apsaugoti nuo Putino įtakos. Karas su „blogio imperija“ užbaigtas, ir visi išsiskirsto patenkinti. Ir lietuviai taip pat.

Nelaimingi tik keli šimtai „protingiausių“, kurie pavertė savo neapykantą Rusijai pašaukimu ir profesija.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 20 — id: `scraped:rubaltic_lt:22cf0c9f7f822f90`

**Title:** Giliavandenio uosto projektas Klaipėdoje liks be pinigų

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvoje įsiplieskė diskusija išorinio giliavandenio uosto Klaipėdoje statybos klausimu. Pagrindinė problema: tokiom statybom šalis neturi pinigų. Aktualia tema pasisakė net Lietuvos prezidentas Gitanas Nausėda, skeptiškai pažvelgęs į idėją pasitelkti kinų investuotojus. Ne iki galo aišku, kodėl iškeliamas šis klausimas. Kinija netrokšta investuoti lėšų į Pabaltijo šalių infrastruktūrinius projektus, ir Lietuva tampa pajuokos objektu, pergyvendama dėl jai nesiūlomų investicijų.

Apie būtinybę sukurti Klaipėdai išorinį giliavandenį uostą Lietuvoje prabilta prieš dešimt metų. Vyrtiausybė nedvejodama įtraukė šią idėją į sąrašą dešimties svarbiausių projektų, kurių realizavimui būtina pritraukti privatų kapitalą. Atrodo, jau tada oficialusis Vilnius nelabai tikėjosi ką nors „išpešti“ iš eurofondų, o po aferos su SGD terminalu šis klausimas išvis nustojo egzistuoti dienotvarkėje.

Briuselis davė suprasti, jog SGD terminalą Independence ES biudžetas gali paremti tik tuo atveju, jei jis taps regioniniu. Tačiau kaimynai nepasinaudojo Lietuvos terminalo paslaugomis. „Ernergetinės nepriklausomybės“ našta buvo užkrauta ant Lietuvos mokesčių mokėtojų pečių.

Išlaidų šalyje ir be to pakanka — tai streikuojantys mokytojai reikalauja didinti atlyginimus, tai žvejams uždraudžiama gaudyti menkes Baltijos jūroje, tai suremontuoti keliai „staiga“ atsiduria nepatenkinamoje būklėje. Ir tokiame fone dar reikia karines išlaidas didinti!

O kalba eina apie rimtas sumas. Praėjusiais metais sąmata Klaipėdos giliavandenio uosto statybai buvo ne kartą skaičiuojama. Galutiniai skaičiai, ką bedarytum, pasakiški.

Pavyzdžiui, kompanija Smart Continent LT įvertino du projekto variantus: uostas Butingėje kainuotų 1,163 milijardo eurų, o Melnragėje — 619 milijonų.

Šiandien žiniasklaida kalba apie 800 milijonų. Šaliai, kurios BVP pagal praeitus metus sudarė vos daugiau 45 milijardų, suma labai rimta.

Viliamasi, jog situaciją išgelbės privatūs investoriai. Tokie, kurie pinigų neskaičiuoja (taupus kapitalistas į abejotinus lietuvių sumanymus neinvestuos).

Iš pirmo žvilgsnio, gal ir „nuskils“. Pekinas intensyviai investuoja į projektus, kurie siejami su „Naujo Šilko kelio“ iš Azijos į Europą statyba. Ypatingą dėmesį kinai skiria uostams. Klaipėda taip pat atkreipė jų dėmesį.

Pramoninė korporacija China Merchants (CMG) planavo čia įsteigti savo atstovybę, įsigyti nuosavą terminalą ir dalyvauti minėto uosto statyboje. Klaipėdos uostas su kinų investoriais pasirašė net keturis memorandumus, sukuriant transporto logistinį „Šilko kelio“ centrą, ir sutartį dėl strateginės partnerystės projekto rėmuose.

Beje, netrukus paaiškėjo, jog šiuose dokumentuose nėra jokių konkrečių įsipareigojimų. Kinų siekiai taip ir liko siekiais — žadėtų investicijų Klaipėda iki šiol laukia. O gal jau nelaukia?

Sprendžiant iš Valstybinio saugumo departamento (VSD) ir Lietuvos karinės žvalgybos vasario ataskaitos, „raudonasis drakonas“ jau kvėpuoja į nugarą „rusų lokiui“. Kinija esą meta į Pabaltijį vis daugiau savo agentų ir stengiasi pasiekti slaptą informaciją. Kur gi daugiau NATO ir ES gali laikyti savo svarbiausias paslaptis, jei ne Dievo užmirštoje Europos periferijos teritorijoje?

Net vienas iš pagrindinių kooperacijos su Kinija vystymosi iniciatorių — premjeras Saulius Skvernelis buvo priverstas atsikvošėti. „Kol kas nėra rimtų bandymų realiai (iš kinų pusės) investuoti. O jei jie bus, mes tikrai juos įvertinsim labai atsakingai, ir aš nemanau, jog mes galėtumėm pasielgti taip, kad į strateginius ir svarbius nacionaliniam saugumui šalies objektus ateitų investorius, dėl kurio patikimumo gali kilti abejonių“, — pareiškė vyriausybės vadovas.

Skandalo su Huawei metu Lietuva taip pat pasižymėjo. Konservatorių deputatų grupė išsakė Seime reikalavimą apsaugoti Lietuvą nuo kinų kompanijos produkcijos. O juk Kinijos atstovai buvo perspėję europiečius: nedrįskite spausti Huawei, nes sulauksite nemalonumų.

Dar prisiminkime Pabaltijo konfrontaciją su Rusija — pagrindine Kinijos partnere „Naujo Šilko kelio“ projekto rėmuose, o taip pat daugiametę Lietuvos valdančiųjų draugystę su Dalaj — lama.

Kažkada Dalia Grybauskaitė net neatsargiai ryžosi jį priimti prezidentūroje.

Atrodytų, Lietuva padarė viską, kad „Naujas Šilko kelias“ praeitų pro ją. Tačiau respublikos valdžios tebesvarsto investijas, kurias joms niekas nesiūlo.

Pasak Gitano Nausėdos, išorės uostas Klaipėdoje neturi patikimų investorių, kurie atitiktų „visiems nacionalinio saugumo kriterijams“. „Jeigu tai kinų investicijos, jos siejasi su kitais klausimais, kurie šiandien labai svarbūs visai Europai, tai nacionalinio saugumo aspektas“, — tvirtina Lietuvos prezidentas.

Įdomu, apie kokias kinų investicijas eina kalba? O gal korporacija China Merchants Group savo Pabaltijo draugams pagaliau „atplukdė“ 800 milijonus eurų? O gal atsirado kitos kompanijos, įžvelgusios Klaipėdos uosto infrastruktūros plėtros perspektyvas? Vertėtų tai pagarsinti. Ir pradėti investoriaus patikimumo patikrinimo procedūrą, apie kurią kalbėjo Saulius Skvernelis.

Tačiau tame ir esmė, kad nieko naujo Nausėda negali pasakyti. Iš China Merchants Group Lietuvoje beliko vien tik beviltiški memorandumai. Kinai juos jau pamiršo, o Lietuvos valdžios vis dar mąsto, ar atverti neegzistuojantiems investoriams Klaipėdos uosto vartus?

O Nausėdos susirūpinimas „nacionaliniu saugumu“ sukelia graudulį.

Lietuva mielu noru atsilygintų Pekinui lojalumu tarptautinėje arenoje. Nors jis to nereikalauja: labiausiai „prokiniška“ Rytų Europos šalis Vengrija nebuvo pastebėta ginant Kinijos interesus. Čia viskas paprasta: Vengrijoje Kinija turi ekonominių interesų, o Pabaltijyje — ne.

Susitaikyti su tuo nelengva. Ir todėl bandoma dalinti nenudėto drakono kailį.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```
