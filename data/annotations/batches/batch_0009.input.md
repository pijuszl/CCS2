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

### Article 1 — id: `scraped:rubaltic_lt:16d1ed95199d6cd2`

**Title:** Putinas atėmė iš Lietuvos paskutinę viltį „sovietų okupacijos“ kompensacijai

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Rusijos prezidento Vladimiro Putino straipsnis apie Antrąjį pasaulinį karą tuoj pat sukėlė labai negatyvią reakciją Baltijos šalyse. Baltijos šalių pasipiktinimas yra suprantamas, jo priežastys akivaizdžios: Putinas visiškai atsisakė nuolaidžiauti Antrojo pasaulinio karo klausimais, ir be to besąlygiškai atmetė Baltijos šalių „sovietų okupacijos“ doktriną. Lietuva, Latvija ir Estija gali galutinai palikti savo viltis gauti piniginę kompensaciją už 50 metų trukusią buvimą TSRS sudėtyje.

„1939 metų rudenį, spręsdama savo karines, strategines bei gynybines užduotis, Tarybų Sąjunga pradėjo Latvijos, Lietuvos ir Estijos inkorporacijos procesą. Jų įstojimas į TSRS buvo realizuotas pagal sutartį, esant gyventojų teisėtai išrinktos valdžios pritarimui. Tai atitiko to laiko tarptautines ir valstybines teisės normas. Beje, Lietuvai 1939 metų spalio mėnesį buvo grąžintas Vilniaus miestas su apskritimi, kurie anksčiau sudarė Lenkijos dalį. Baltijos respublikos TSRS sudėtyje išsaugojo savo valdžios organus, kalbą, turėjo atstovybę aukščiausiosiose tarybų valstybinėse struktūrose“, - rašo Vladimiras Putinas straipsnyje prestižiniam amerikiečių žurnalui apie tarptautinius santykius The National Interest.

Baltijos šalių reakcija į šiuos žodžius buvo nuspėjama.

„Šitie pasisakymai – melagingi nuo pat pradžios iki galo, ir aš juos pasmerkiu“ – pakomentavo Putino žodžius Estijos užsienio reikalų ministras Urmas Reinsalu ir paragino surengti Rusijai kaip Tarybų Sąjungos įpėdinei antrą Niurnbergo tribunolą, kad tarptautinė bendruomenė įvertintų „nusikaltimams žmoniškumui, padarytiems palaikiusio antihumanišką komunistinę TSRS ideologiją režimo metu“.

„Rusijos valdžia vis dar nepajėgia objektyviai įvertinti tarybų režimo atsakingumą už Antrojo Pasaulinio karą sukėlimą ir daugelį nusikaltimų prieš Europos, Rusijos ir jos kaimyninių šalių tautas“, - praneša Latvijos URM.

Oficialioj Rygoj mano, jog Baltijos šalys „buvo neteisėtai okupuotos ir aneksuotos grasinimų ir karinių okupacijų dėka“, o TSRS „pažeidė savo įsipareigojimus pagal tarptautines sutartis ir įvykdė agresijos aktą“. „Baltijos šalių iliuzinė autonomija tarybų okupacijos metu buvo tik priedanga tarybų režimo nusikalstamai politikai, kuri buvo nulemta Tarybų valstybės vadovybės ir Komunistinės partijos Maskvoje“, - teigia Latvijos URM.

Iki savaitės pabaigos tik Lietuvos URM niekaip neatsakė į Rusijos prezidento straipsnį. Matyt, lietuvių diplomatai labai neatsakingai dirba ir iki šiol nesugebėjo rasti tinkamų žodžių tam, kad atsakyti į pasipiktinimą keliančią tiesą dėl Vilniaus prijungimo prie Lietuvos aplinkybių po Lietuvos diktatoriaus Smetonos susitarimo su sovietų diktatoriumi Stalinu.

Pasipiktinimą sukelia dvi akivaizdžios priežastys.

Visų pirma, Putinas pažeidė Baltijos šalių monopoliją savo istorijos išdėstymui tarptautinei bendruomenei. Baltijos šalių „sovietų okupacijos“ mitologija vakaruose laimėjo todėl, kad niekas nesiūlė alternatyvos. Lietuva, Latvija ir Estija mažai kam žinomos, įdomios ir tikrai nedaugelis žmonių Šiaurės Amerikoje ir Vakarų Europoje rimtai nagrinės jų istoriją. Todėl viešoji nuomonė Vakaruose išmoko „sovietų okupacijos“ mantrą atmintinai ir net negalvojo, kad tai nėra aksioma ir egzistuoja kitokios nuomonės šiuo klausimu.

Šiuo atžvilgiu Putino straipsnis tikrai pavojingas.

Vladimiras Putinas pastaruoju metu virto tarptautinės informacinės erdvės žvaigžde, ir jo žodžius ir pasisakymus godžiai klausia ir tie, kurie laiko Rusijos prezidentą tikru velniu, ir tie, kurie mano, kad jis yra išdidus valstybinis veikėjas. Putino straipsnis National Interest žurnalui jau sukėlė diskusiją tarp anglakalbių žurnalo skaitytojų. Taip pat ir apie Baltijos šalių praeitį.

O Baltijos šalys bijo lyg ugnies bet kurių savo praeities bei šiuolaikinės situacijos aptarimų.

Vladimiras Putinas kreipiasi į vakarų šalių auditoriją, bet visiškai neturi omeny tikslo ieškoti susitarimo su vakarų valstybių lyderiais istorijos klausimais. Jis tiesiog išdėsto Rusijos nuomonę pagal Antrąjį pasaulinį karą.

Tarybų Sąjunga iki paskutiniausio mėgindavo sustabdyti karą ir sukurti antihitlerinę koaliciją. Deja Europos didžiosios valstybės vietoj koalicijos prieš siaubingą nacių režimą suteikė pirmenybę sutaikymo su Hitleriu politikai, besitikėdamos nukreipti jo agresiją į rytus ir sukurstyti prieš TSRS. Šios politikos pasekme tapo Miuncheno susitarimas su Čekoslovakijos padalijimu ir daugybė nepuolimo sutarčių, sudarytų su Trečiuoju Reichu bei pasirašytų dar prieš Molotovo-Ribentropo paktą.

Trečiojo Reicho ir jo sąjungininkų sutriuškinimas buvo ne vien tik įprasta vieno geopolitinio bloko pergalė prieš kitą, bet pergalė prieš fašistinės ideologijos absoliutų pyktį.

Istorijos perrašinėjimo pastangos yra sudarytos 1945 metais pasaulio tvarkos suirimas. Tarybų Sąjunga buvo viena iš to pasaulio tvarkos architektų, todėl istorijos falsifikacija įgyvendinama tam, kad susilpninti o geriau net pašalinti TSRS įpėdinę – Rusiją – iš tarptautinių santykių. Žmoniškai tai, kas dabar yra atliekama su istorine atmintimi – niekšiškumas, ir Maskva šito niekšiškumo nepamirš ir neatleis.

„Mes apginam tikrą, neišlygintą ir nesulakuotą tiesą apie karą“, - rašo Putinas. Jo straipsnis – to patvirtinimas. Joje nėra jokių diplomatinių ekivokų, jokių „gerbiame kitas nuomones“, jokių „viskas buvo ne taip vienprasmiška“ ir siūlymų rasti kompromisą.

Rusijos prezidentas nedviprasmiškai leido suprasti, kad jokio politinio derėjimosi su jo valstybe Antrojo pasaulinio karo istorinės tiesos klausimais negali būti.

Taip pat negali būti jokio derėjimosi dėl Baltijos šalių „sovietų okupacijos“ bei piniginių kompensacijų Lietuvai, Latvijai ir Estijai pripažinimo ar atmetimo.

Putinas viešai paskelbė tai ne vien tik Baltijos valstybėms, bet visam pasauliui.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 2 — id: `scraped:rubaltic_lt:dbdcf26db92b5e28`

**Title:** Lietuva triukšmauja Briuselyje: reikalaujame ES dotacijų pratęsimo

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos prezidentas Gitanas Nausėda pareiškė, kad naujoji Europos Sąjungos 7 metų finansinė programa „turėtų būti labiau ambicinga“, o susibūrimo politikos išmokos – žymiai didesnėmis. Jo kalboje aiškiai skamba susierzinimo natos. Baltijos šalies valdžia jau ne ragina, bet reikalauja neatimti iš jų prieigos prie bendrų europietiškų lėšų. Matyt, Briuselis privalo vadovautis įžymiu Antuano de Sent Egziuperi posakiu: „Tampi amžinai atsakingas už tą ką prisijaukinai“. Arba prisipratinai duodant ėsti.

Gitanas Nausėda per vaizdo konferenciją laikė derybas su Europos Komisijos vicepirmininku Valdžiu Dombrovskiu, kuris atsako už finansinio stabilumo ir socialinio dialogo klausimus. Lietuvos lyderio oficiali svetainė skelbia , kad derybų šalys aptarė eilę ekonominio pobūdžio klausimų.

Reikėtų manyti, kad Nausėda sieja didžiules viltis su latviu Dombrovskiu – pačiu „sunkiasvoriu“ pagal reikšmę Baltijos regiono atstovu dabartinėje ES vadovybėje. Ar ne jam taikoma ypatingas vaidmuo pinigų Lietuvai, Latvijai ir Estijai kaulyjime?

Beje, EK vicepirmininkas gali tikėtis sėkmės. Gal tada europietiško finansavimo Baltijos šalims apribojimas nebus toks radikalus, kaip tai buvo manoma iš pradžių. Dombrovskiui tai leistų sustiprinti savo politinę įtaką tėvynėje.

Koronaviruso epidemijos ekonominių pasekmių nugalėjimui Baltijos šalies prezidentas inicijuoja apmokestinamų pajamų didį, laikiną pajamų mokesčio fizinių asmenų algoms įprasto tarifo laikiną sumažinimą nuo 20% iki 15% (nuo dalies iki trijų vidutinių algų), mažai pajamų gaunančių šeimų pašalpų programą ir vienkartines išmokas vaikams. Analogišką paramos paketą, kaip pabrėžia Nausėda, neseniai priėmė Vokietija.

Ką gi, galima tik pagirti Lietuvos lyderį už norą aprūpinti savo tautiečius vokiškais socialiniais standartais.

Kur rasti pinigų tam, kad „sulopyti“ skyles biudžete, kurios būtinai atsiras po Nausėdos antikrizinio paketo implementacijos? Yra tik viena išeitis – „užsienis mums padės“.

„Prezidentas pabrėžė, kad Lietuvos pozicija dėl ES biudžeto didžio išlieka tokia, kaip buvo – šios beprecedentiškos situacijos priešaky ilgalaikė finansinė programa privalo būti daug ambicingesnė, būtina siekti žymesnio finansavimo susibūrimo politikos realizacijai ir visuotinio tiesioginių išmokų fermeriams išlyginimo“, – skelbiama prezidento administracijos pranešime.

Susibūrimo politika buvo sugalvota kaip „Senosios Europos“ geros valios gestas, kuriuo buvo nuspręsta „patempti“ savo rytų kaimynus. Jokių įsipareigojimų stabiliai išlaikyti aukšto lygio finansines sroves neprisiėmė, atvirkščiai iš pat pradžių buvo numatyta, kad per tam tikrą laiką Baltijos šalys išmoks uždirbti pinigus savarankiškai ir nestokos dotacijų. Todėl Europos Sąjungos logika yra griežta.

Fermerių paminėjimas nusipelno atskiro aptarimo. Nausėda reguliariai kelia šią temą: žemės ūkio išmokos Lietuvoje žymiai žemesnės, nei Vakarų ir Pietų Europos šalyse. Valdančiąją koaliciją sudarančios partijos „Lietuvos lenkų rinkimų akcija – Krikščioniškų šeimų sąjunga“ lyderis Valdemaras Tomaševskis irgi pritaria, kad disproporciją reikia pašalinti kuo galima greičiau.

„Aš dirbau 10 metų Žemės ūkio reikalų komisijoje ir ne kartą įtraukdavau pataisas, kad priemokos fermeriams būtų išlygintos. Bent kad nebūtų tokio skirtumo, nes dabar skirtumas yra labai didelis. Taigi čia yra kaip tik mano ir mūsų grupės, dirbusios Europos Parlamente, pasiūlymas. Dabar esame nepatenkinti šia politika dėl žymių disproporcijų: Graikijoje gauna virš 500 eurų, mes dabar gauname 170 eurų, bet buvo 130 eurų. Pakėlėm dydį šių raginimų dėka“, - taip Tomaševskis komentavo nesenus Nausėdos pareiškimus.

Papildomi 40 eurų – gana kuklus kovos už Lietuvos ūkininkų teises rezultatas. Bet tikėtis daugiau nėra prasmės, ypač postkoronaviruso sąlygomis.

Patys Lietuvos politikai ne kartą pabrėždavo, kad dėl nesąžiningo finansinių srovių paskirstymo jų žemės ūkio produkcijos gamintojai neatlaiko konkurencijos. Pasirodo, Europos Sąjungos lyderiai, būdami sveiko proto, privalo nei iš šio, nei iš to pakirsti Graikijos, Prancūzijos, Olandijos fermerių pozicijas? Tuo labiau, kad dabar yra sunki finansinė krizė.

Pokalbyje su Dombrovskiu Lietuvos prezidentas taip pat paminėjo, kad jo šalis „laukia iš ES, kad pastaroji atliktų savo įsipareigojimus dėl būtino finansavimo Ignalinos AE darbo stabdymui ir Kaliningrado srities tranzito schemos realizacijai“. Matyt, ne viskas yra taip lengva, jei tenka priminti.

Dėl Ignalinos AE problemų anksčiau jau buvo minima. Tas pats Nausėda ES biudžeto 2021-2027 metams Suomijos projekto aptarymo metu pareiškė, kad atominės elektrinės uždarymo darbų biudžetą reikia padidinti. Anksčiau tokį pat teiginį skelbė Lietuvos ambasadorė Europos Sąjungoje Jovita Neliupšienė: Suomijos pasiūlymus reikia koreguoti, nes kitaip IAE likvidavimo darbai „buksuos“.

Pastaroji savo eile pritarė tam, kad finansuoti atominio giganto likvidavimą. Bet dotacijų vis tiek neužtenka. Beje, 2056 metais Lietuvai teks pradėti ilgalaikių branduolinių atliekų saugyklos statybą, kuri kainuos 2,5 milijardų dolerių. Europietiško finansavimo Lietuvos vyriausybėje gauti nesitiki: Energetikos ministerija siūlo savo jėgomis taupyti pinigų specialiame rezerviniame fonde, į kurį būtų skiriami 25% dividendų gaunamų iš valstybinių įmonių.

O ką gi Europos Sąjunga? Jinai, kaip pasirodė, „užspaudžia“ pinigus net esamoms išlaidoms Ignalinos AE likviduoti. Su naujo Europos biudžeto priėmimu Lietuva turėtų dar labiau gailėtis dėl savo atominės energetikos likvidavimo.

Kol Lukašenka siūlo Vengrijai pasidalinti šiuolaikiškiausia patirtimi šioje sferoje, Nausėda stovi su ištiesta ranka prieš „Briuselio obkomą“. Taip „europietiška svajonė“ Lietuvai virto nacionaliniu pažeminimu.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 3 — id: `scraped:rubaltic_lt:44fed5026812f680`

**Title:** Lietuvos prezidentą paverčia „atpirkimo ožiu“ už pralošimą kovoje su Astravo AE

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Vilniaus pralošimo kovoje su Baltarusijos Astravo AE pagrindinis kaltininkas – Baltijos šalies prezidentas Gitanas Nausėda. Tokį pareiškimą padarė žinomas diplomatas, „Sąjūdžio“ aktyvistas bei Lietuvos nepriklausomybės atkūrimo akto signataras Albinas Januška. Anot jo, valstybės vadovas pritarė „branduolinio monstro“ paleidimui ir taip užtraukė gėdą visai savo šaliai. Akivaizdu, kad Januška toli gražu ne vienintelis asmuo, kas kaltins Nausėdą kapituliacija. Vis dėlto Lietuvos prezidentas pats nulėmė savo ateitį, kai prisijungė prie jau praloštos kovos su Astravo AE.

„Gitanas Nausėda pamiršo apie valstybės nacionalinius interesus tuo metu, kai kreipėsi į Europos Tarybos vadovą Šarlį Mišelį su reikalavimu būtinai atlikti streso testus Astravo atominėje elektrinėje iki jos paleidimo. Šitoks reikalavimas buvo paskelbtas kaip pritarimo jėgainės darbo pradžiai sąlyga. Bet ponas Nausėda nereikalavo atsisakyti Astravo AE pagamintos elektros pirkimų! Valstybės pirminis nacionalinis interesas buvo pamirštas, jo pačio pareigos buvo užmirštos“, - pasipiktina Januška savo Facebook paskyroje.

Epizodas, apie kurį pasakoja politikas, įvyko gegužės 18 dieną. Telefono pokalbyje su Šarliu Mišeliu Lietuvos prezidentas tikrai pareikalavo „įtraukti visus ES institucijas“, kad priversti Baltarusiją atitikti branduolinio saugumo reikalavimus.

Pirmąjį bloką numatyta paleisti birželio 18 dieną.

Pasak Januškos, šita diena taps „Lukašenkos interesų triumfu, bei Lietuvos gėdingu pralošimu“.

„Jeigu Lietuvos politikai, kurie bent kiek yra susirūpinę šalies saugumu ir jos užsienio politikos interesais, nepasisakys prieš tai“, - prideda susierzinęs diplomatas.

Tarkim, pasisakys, ir kas bus toliau? Lietuvos „pasisakymai“, kurie labiau primena cirko pasirodymus, besitęsia jau kelis metus iš eilės. „Koncertas“ nesiliovė net valdžios keitimo laikotarpiu: kol Dalia Grybauskaitė ėmėsi savo paskutinių puolimų prieš Astravo AE, visi pagrindiniai kandidatai prezidento pareigoms žadėdavo tęsti jos beprasmiškas pastangas.

Šiuo klausimu Nausėda parodė pavyzdingą padorumą. Pasakė – padarė. Niekas negali apkaltinti jį tuo, kad jis pamiršo baltarusių „atominį monstrą“. Atvirkščiai stebina Lietuvos prezidento karingumas, kuris priešrinkiminės kampanijos metu pasirodė pačiu blaiviai žiūrinčiu ir pragmatišku pretendentu eiti aukščiausias pareigas valstybės tarnyboje.

Bet branduolinio pavojaus įtikinimai Vilniaus sąjungininkams įtakos nedaro. Europos Sąjunga to pavojaus išvis nemato, pasitikėdama TATENA padarytomis išvadomis, kurios liudija Astravo AE aukščiausią saugumo lygį. Nepavyko net užtikrinti sau besąlygišką kaimynų palaikymą. Latvijos ir Estijos pozicija pagal elektros pirkimus iš Baltarusijos kol kas išlieka neaiški.

Bet Albinas Januška aiškiai išpunta problemą, kai kaltina viskuo Nausėdą. Pastarojo sąžinė gali būti rami. Dalios Grybauskiatės antros kadencijos pabaigai kovos už Astravo AE baigtis jau buvo nulemta. Nedaug laiko prieš Nausėdos pergalę per rinkimus pirmajame bloke buvo pradėti priešpaleidiminiai derinimo darbai.

Galų gale, Nausėdai būtų verta atkreipti dėmesį į ministro-pirmininko Sauliaus Skvernelio „chuliganišką planą“, paskelbtą nedaug laiko prieš prezidento rinkimus. Tai buvo nerangi pastanga rasti kompromisinį sprendimą pagal Astravo AE – aiškus ženklas tam, kad su Grybauskaitės stiliaus boikotu atėjo laikas atsisveikinti.

Jeigu lyginti tuos įvykius su karo veiksmais, tai lietuvių frontas, kovojantis prieš Astravo AE, laiku, kai vadovavimas buvo perduotas Gitanui Nausėdai, buvo toje pačioje padėtyje, kaip ir feldmaršalo Fridricho Pauliaus vadovaujama 6-oji armija po Stalingradu: priešintis dar galima, tačiau tikėtis sėkmės – nebe.

Ir čia galima Januškai pritarti: būtino streso testų atlikimo reikalavimas suveda galutinę ribą po Vilniaus pastangomis sustabdyti Astravo AE. Tolimesnės pastangos bus nukreiptos į tai, kad neleisti arba, blogiausiu atveju, maksimaliai apsunkinti baltarusių energijos gabenimus į Nord Pool biržą.

Bet tuo atveju, jei streso testai, kurių reikalauja Nausėda, bus atlikti ir įrodys jėgainės saugumą, kam Lietuvai tęsti jos boikotavimą? Tai atrodys visiškai kvailai. Tokiu būdu, Baltijos valstybės lyderio reikalavimai atveria kelią kaip Astravo AE paleidimui, taip ir jos gaminsimos produkcijos eksportui vakarų šalių kryptimi.

Jausdamas neišvengiamą pasipiktinimo bangą, Nausėda vis tiek mėgina atsikratyti atsakomybės už pralošimą: „ Tokių iliuzijų, kad AE bus pastatyta kitoje vietoje arba išvis bus sulyginta su žeme, tikriausiai, mes sau leisti negalime. Reikėjo tai daryti prieš 11-12 metų; deja, mes nepadarėme nieko“.

Todėl ir Januška pats savęs visai logiškai klausia: „Kas atsitiko su prezidentu Nausėda, kuris staiga persigalvojo (stabdyti Astravo AE statybą – RuBaltic.Ru pastaba)?“

Galėjo ne persigalvoti, o iš pradžios rinktis konstruktyvios pozicijos. Jėgainės boikotavimu turėjo užsiėminėti jo pirmtakai – mums telieka bendradarbiauti su Minsku tam, kad patvirtinti jos saugumą. Toks Nausėdos pareiškimas sukeltų kritikos škvalą, bet išvadovautų jo iš būtinybės atsakyti už svetimas klaidas.

Januška tikriausiai nėra vienintelis žmogus, kuris tars, kad sėkmė buvo įmanoma. Jeigu tik prezidentas paskutine akimirka nepasitrauktų iš „taisyklingo“ kelio...

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 4 — id: `scraped:rubaltic_lt:8a0eaf6c37903963`

**Title:** Lietuva pasitaiko: nutraukti ryšius su Rusija mums yra svarbiau už mūsų ekonomiką

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos Respublikos užsienio reikalų ministras Linas Linkevičius pripažino, kad šalies energetinė politika glaudžiai susieta su geopolitika, o ne su žemomis kainomis energijos nešėjams. Oficialus Vilnius ragina išstoti iš BRELL (Baltarusija – Rusija – Estija – Latvija – Lietuva) energetinio žiedo, kovoja su Astravo AE statyba ir tempia Klaipėdos SGD terminalo naštą ne todėl, kad tai yra ekonomiškai naudinga lietuviams, bet todėl, kad tai yra pabėgimo nuo Rusijos į Vakarus kelio dalis. Lietuvos ekonomikai tikėtis gauti pigią energiją iš Lietuvos energetikos projektų neverta – aiškiai leidžia suprasti Linas Linkevičius.

„Mes kažkada anksčiau diskutavome apie pigesnę dešrą, apie tai, kiek ji kainuoja iš tikrųjų, tai šita situacija – kažkas panašaus. Čia iš tikrųjų procesas daug stambesnis: jeigu pageidaujame desinchronizuoti savo energetikos tinklus su Rytais ir sinchronizuoti juos su Vakarų Europa, numatome pasiekti šito tikslo iki 2025 metų ir suprantame, kaip sunku tai padaryti, tai iš esmės tai yra geopolitinės pastangos, o ne vien tik pigi elektra“, - pareiškė Lietuvos URM vadovas.

Šiais žodžiais Linkevičius pakomentavo Lietuvos nesėkmingas pastangas pasirašyti tarpvyriausybinį susitarimą su kitomis Baltijos valstybėmis dėl elektros energijos prekybos su Baltarusija, kuris apdraustų Lietuvą nuo patekimo į jos teritoriją Astravo AE pagamintos elektros.

Anot oficialaus Vilniaus, Latvija ir Estija privalo kartu su Lietuva boikotuoti Baltarusijos branduolinę programą, kas taps Lietuvos užsienio politikos didžiule pergale.

Deja, Latvija nieko boikotuoti nenori ir sako, kad Astravo AE elektros energija bus naudinga jos ekonomikai.

Baltijos šalių susitarimas atsisakyti pirkti Astravo AE gaminsimos elektros yra „keblus balansavimas tarp geopolitikos ir kainų“, o nuomonė, kad atominės elektrinės istorijos laimėtoju taps tas, kas gaus pigiausią elektrą, klaidinga. „Todėl ir verta numatyti, kad kažkas turi įvykti kažko kito dėka“, - sako Linas Linkevičius. Šiuo atveju – „europietiškas pasirinkimas“ protingų kainų elektrai dėka.

Prie dvejų Baltijos energetikos siužetų – išstojimo iš BRELL žiedo ir Astravo AE – lietuvių ministras pridedą trečią: Klaipėdos SGD-terminalą Independence. Tai, anot jo, tos pačios rūšies siužetas. Prieš kelis metus Lietuva, kaip ir dabartinė Latvija, rinkosi tarp žemų kainų dujoms ir dujų tiekimų diversifikacija, ir pastarosios opcijos pasirinkimas tapo „geopolitiniu lūžiu“.

Šis apreiškimas skamba kaip tikras „coming out“.

Visiems sekantiems nuostabus SGD-terminalo nuotykius tai buvo aišku ir anksčiau. Suskystintos dujos kainavo daugiau už rusiškas. Lietuvos ministras-pirmininkas vadindavo SGD-terminalą „našta Lietuvos mokesčių mokėtojams“. Daug kalbų sukėlusią nuolaidą iš Gazpromo Lietuva gavo daug seniau už atgabenimo į Klaipėdą SGD-terminalo Independence, ir visi, kas išmanė aritmetiką, gūžtelėjo pečiais, kai valstybės valdžia pasakodavo, jog energijos nešėjų diversifikacija leido Lietuvai sumažinti kainą rusiškoms dujoms.

Vis dėl to Vilnius atkakliai kartodavo, kad SGD-terminalas įrengtas ekonominiais tikslais ir yra naudingas verslo projektas. O dabar URM vadovas sako: mes rinkomės tarp menkaverčių tikslų ir Rusijos monopolijos energijos tiekimui ir pasiekėme „geopolitinio lūžio“. Na bent už tai ačiū. Geriau jau vėliau pasakyti vartotojams tiesą, nei niekados tai nepadaryti.

Piniginis pelnas visais atvejais apsiriboja tuo, kad būtų įmanoma gauti projektui pinigų iš Europos Sąjungos ir paskirstyti juos tarp artimų valdininkams įmonių. Šiam merkantilizmo kupinam interesui tariamasi dėl finansavimo su Briuseliu, kur Baltijos šalių valdininkai seka Europos Komisijai pasakas apie galutinį ‚sovietų okupacijos“ paveldo nugalėjimą.

Vidinėj auditorijai tokio argumentavimo neužtenka. Ideologijai pavaldus nacionalistų elektorato „branduolys“ dar pritars, bet gyventojų dauguma pasipiktins: kodėl antirusiškos politikos vardan esame priversti daugiau už elektrą ir dujas? Todėl rinkėjams valdžia mėgino sugalvoti ekonominius argumentus. O taip pat ekologinius, kaip Ignalinos AE uždarymo atveju, kurią Lietuvoje pastatė ir teikė aptarnavimo paslaugas „Rosatomas“, ir Astravo AE atveju, kurią stato ir irgi prižiūrės „Rosatomas“.

Ar Europos Sąjunga dabartinėje padėtyje yra pasiryžusi teikti pinigus šiam Baltijos didžiajam tikslui – abejingas klausimas. Ar eiliniai lietuviai krizės sąlygomis yra pasiryžę mokėti triskart daugiau už komunalines paslaugas galutinio ir nepakeičiamo atskyrimo nuo Rusijos vardan – klausimas dar labiau abejingas.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 5 — id: `scraped:rubaltic_lt:82520828a8421ea6`

**Title:** Lietuva apmoka JAV paramą karinėmis ir gynybos išlaidomis

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos Krašto apsaugos ministerija praneša, kad respublika neatsisakys planuotų karinių ir gynybos išlaidų, kurių numatytas dydis sudaro 2% nuo BVP. Koronavirusas ir jo sukelta krizė neprivertė Lietuvą imtis gynybos biudžeto mažinimo. 2% nuo BVP normatyvas tapo Lietuvai sakraliniu skaičiumi, kuris užtikrina Baltijos šaliai JAV palankumą. Tam, kad gauti Baltųjų rūmų paramą po karinės technikos įsigijimo valstybės valdžia yra pasiruošusi taupyti iš paramos nukentėjusiems nuo pandemijos.

„Nepaisant COVID-19, konvencinė grėsmė neišnyko. Kariniai mokymai – mūsų parengimo ir nulaikymo elementas, todėl privalome kuo greičiau grįžti prie jų įprastos tvarkos. Tam, kad užtikrinti paruoštumą privalome ir toliau išlaikyti finansavimo lygį ne žemesnį nei 2% nuo BVP“, - pareiškė Lietuvos Krašto apsaugos ministras Raimundas Karoblis per šalių – NATO narių gynybos įstaigų vadovų videokonferenciją.

„Konvencinė grėsmė“, kurią mini Lietuvos Krašto apsaugos ministerijos vadovas, yra, žinoma, Rusijos agresijos pavojus. Konvencine ji yra vadinama ta prasme, kad yra pažįstama, visiems aiški ir seniai tapusi lietuvių gyvenimo rutina.

Tiesa, Rusijos agresijos nebuvo, nėra ir nenumatoma, kaip ir neaptinkama jokių jos parengimo požymių. Deja, valdžia daugelį metų nepavargsta įtikinanti lietuvius, kad įsiveržimas tuoj prasidės ir nauja okupacija užpuls Lietuvą.

Kol kas Lietuvą užpuolė visiškai kitoks įsiveržimas. Nekonvencinis pavojus, kuriam šalyje niekas nebuvo pasirengęs. Ir, tarp kitko, koronaviruso sukelta nepaprastoji padėtis perkėlė dvejų ar daugiau procentų nuo BVP gynybai į visiškai kitą plokštumą

Lietuvos Respublikai iš tikrųjų teko mobilizuotis, lietuviška kariuomenė susidūrė su netikėtu tikslu: apginti lietuvius nuo naujo, nematomo priešo, kaip vadindavo koronavirusą COVID-19 kai kurie Europos lyderiai.

Tame pačiame ministro Karoblio pasirodyme visai nepaminėta mobiliųjų ligoninių statyba kariškiais, humanitarinių krovinių perkėlimas armijos jėgomis, gyventojų biologinės apsaugos įtvirtinimas.

Toks Krašto apsaugos ministerijos resursų pritaikymas būtų politiškai naudingas bei „žmoniškas“.

„Koronakrizės“ metu, kai Lietuvos gyventojai patyrė ne fantomą, bet realų pavojų, šis skaičius galėjo tik išaugti. Bet ta pati krizė leisdavo politinei vadovybei įrodyti lietuviams, kad išlaidos gynybai – tai tikrai apie jų saugumą. Kad investicijos karinei infrastruktūrai, pavyzdžiui, leis Lietuvai susidoroti su koronavuriso antrąja banga, nesustabdant ekonomikos karantino laikotarpiui.

Vietoj šito Lietuvos valdžia siekia pandemijos intensyviausiu laikotarpiu organizuoti NATO mokymus savo teritorijoje ir platinti karinės technikos parką. Krašto apsaugos ministras dėkoja sąjungininkus už NATO oro policijos misiją Baltijos šalyse ir už internacionalų batalioną Rukloje, kuris tęsia savo treniruotes nepaisant koronavirusą. Pabrėšim, kad neteikdamas jokios pagalbos kovoje su virusu.

Ir tegul kovo mėnesį dėl pandemijos Lietuva apribojo išlaidas gynybai iki 1,7% nuo BVP, dabar šalis sugrįš prie normatyvinių dvejų procentų ir net pati baisiausia ekonominė krizė netrukdys Vilniui tai padaryti.

Donaldas Trumpas taip atkakliai reikalauja iš NATO sąjungininkų atidėti karinėms išlaidoms ne mažiau už 2% nuo BVP, kad aprūpinti amerikiečių karinę pramonę užsakymais. Prieš porą metų europiečiai kukliai pamėgino prieštarauti ir pareiškė: karinį biudžetą padidinsime, bet užsakymais aprūpinsime savo karinės pramonės kompleksą, nes karinė pramonė Europoje išvystyta ir Prancūzijoje, ir Švedijoje, ir daug kur kitur. Iš Vašingtono akimirksniu atskrido grėsmingas šūksnis: Dar paišdykaukit! Mes jums pusę amžiaus nemokamai teikėme karinę apsaugą nuo Sovietų. Nenorite grąžinti 800 milijardų dolerių skolą – pirkite amerikiečių karinės pramonės produkciją.

Savaime aišku, kad šitokia politika skirta visų pirma Vokietijai, Prancūzijai ir kitoms didelėms ir turtingoms Europos šalims. Iš tokių valstybių kaip Lietuva amerikiečių karinei pramonei pasipelnyti beveik neįmanoma, nes jos neturi lėšų apmokėti naujausius šarvuotųjų transporterių bei naikintuvų modelius.

Tačiau tokios šalys atlieka savo vaidmenį. Joms lemta savo pavyzdžiu sugėdinti didžiulius europietiškus sąjungininkus su išties gera perkamąja galia.

Pastaruoju metu Lietuvos įsigytos karinės išdėvos – morališkai pasenę sraigtasparniai UH-60 Black Hawk, Pentagono pripažinti eksploatacijai nebetinkamais šarvuočiai JLTV (Joint Light Tactical Vehicle), vidutinio nuotolio priešlėktuvinės gynybos sistemos NASAMS su seniau naudotomis raketomis – nepajėgs atsispirti karinei agresijai. Rusijos invazijos atveju visi šitie gremėzdai suirs ne dėl Rusijos artilerijos ugnies, bet vien dėl to, kad pamėgins šauti pati.

Vis dėl to Lietuva užsispyrusiai perka šitą surūdijusį laužą ir be to įbrenda į skolas, kad pirkti dar daugiau ir pasiekti 2% nuo BVP karinių išlaidų žymę. Lietuvos prezidentas Gitanas Nausėda žado NATO generaliniam sekretoriui padidinti karini biudžetą iki 2,5% nuo BVP.

Kad pelnyti savo šeimininko iš už okeano pritarimą, Lietuvos valdžia yra pasiryžusi atsisakyti bet kurių išlaidų savo gyventojų reikmėms.

Ir net pačiais lietuviais.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 6 — id: `scraped:rubaltic_lt:e8cc1943762de3d7`

**Title:** Lietuva prarado adekvatumą kovoje su Baltarusijos AE

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos prezidentas Gitanas Nausėda pareikalavo iš Europos Komisijos pirmininko asmeniškai jungtis į kovą už Baltarusijos AE saugumo užtikrinimą. Šitas pareiškimas – dar vienas iš eilės liudijimų, kad BelAE paleidimo išvakarėse Vilnius praranda savo adekvatumą. Elgesys pasiekė net isterijos priepuolių, kai Briuseliui pareiškiama, kad atsakomybę už nesaugią atominę elektrinę priklauso visai Europos Sąjungai.

„ Tokių iliuzijų, kad AE bus pastatyta kitoje vietoje arba išvis bus sulyginta su žeme, tikriausiai, mes sau leisti negalime. Reikėjo tai daryti prieš 11-12 metų; deja, mes nepadarėme nieko“, - pareiškė Lietuvos prezidentas, kalbėdamas apie Baltarusijos atominę elektrinę.

Nepajėgimo paveikti atominės elektrinės statybos projektą Gardino srities Astravo rajone Baltarusijoje pripažinimas jokiu būdu nereiškia, kad Lietuvos vyriausybė atsisakė savo „didžiosios kovos“. Gitano Nausėdos pozicija yra ta, kad Lietuva privalo reikalauti iš Baltarusijos atitikti Europos Sąjungos atominės energetikos saugumo reikalavimus.

Būtent to Lietuva iš Europos Sąjungos ir stengiasi gauti.

Naujienos apie tai, kad į Astravo atominę elektrinę buvo atgabentas branduolinis kuras sukėlė oficialaus Vilniaus karštligiškos veiklos bangą.

Per pastarąsias savaites Lietuva pareikalavo iš Europos Sąjungos skirti sankcijas „Rosatomui“ (atominę elektrinę stato Rusijos kompanija). Kreipėsi su dar vienu skundu dėl „neleistinos situacijos“ į Tarptautinę atominės energijos agentūrą (TATENA). Nusprendė įtikinti visus savo vakarų sąjungininkus skirti sankcijas visiems rangovams. O dar skundėsi dėl Astravo atominės elektrinės

Jungtinėms Valstijoms (jau nebe pirmą kartą) ir kažkodėl Armėnijai, gavo iš oficialaus Kijevo draudimą baltarusiškos elektros energijos importui į Ukrainą ir išsiuntė į Minską eilinę protesto notą.

Darydama išvadas iš savo prastos veiklos, lietuviška diplomatija skelbia, kad Briuselis ir kaimyninės šalys išgirdo jos poziciją dėl Astravo AE. Kur jau neišgirstų! Kai Vilnius taip “riekia”! Kitas dalykas, kad šio riekimo rezultatas neakivaizdus.

Latvija ir Estija kol kas taip ir nepasisakė už visuotinį Baltarusijos gaminamos elektros energijos draudimą Baltijos šalių energetikos rinkoje. Europos Komisija iš vis „žaidžia“ Minsko pusėje, įtikindama Lietuvą, kad viskas yra gerai.

„Baltarusija įsipareigojo tęsti bendradarbiavimą su ES branduolinės saugos reguliavimo institucija (ENSREG)“, - atsakė Europos Sąjungos komisarai dėl energetikos ir kaimynystės politikos klausimų į Lietuvos Respublikos energetikos ministerijos skundą. Jie įtikina Vilnių, kad Baltarusija atominės elektrinės eksploatavimo pradžios išvakarėse laikosi visų branduolinio saugumo reikalavimų.

„Pasitikėjimas branduoline energija ir TATENA kaip organizacija esamuoju laiku visiškai priklauso nuo TATENA veiksmų ir atitinkamo atsakymo į nepakenčiamą situaciją Baltarusijoje“, - tokius žodžius prideda Lietuvos Energetikos ministras Žigimantas Vaičiūnas prie skundo dėl baltarusių atominės programos į Tarptautinę atominės energijos agentūrą.

Kitais žodžiais TATENA reputacija tiesiogiai priklauso nuo to, ar organizacija imsis veiksmų prieš Baltarusiją ir „Rosatomą“ ar ne. Jei nesiims, Lietuva ją taip išbars, kad “tateniečiai“ ilgai prisimins.

„Mes vis pabrėžiame, kad Baltarusijos atominės elektrinės projekto neatitikimas visiems branduolinio saugumo reikalavimams priskirs atsakomybę ne vien tik Baltarusijai, bet ir Europos Sąjungoms institucijoms, dalyvaujančioms šiame procese“, - taip jau minėtas Žygimantas Vaičiūnas komentuoja eurokomisarų griežtą atsakymą.

Visi jau suprato, kad Lietuvos manymu Astravo atominė elektrinė Baltarusijoje negali atitikti branduolinio saugumo reikalavimus „a priori“. Nejaugi Lietuva įrengs „kryžiaus žygį“ į Briuselį, kai atominė elektrinė pagaliau bus paleista?

Tokio lygio pareiškimai, kuriuose savo nacionalinio saugumo suirimu kaltinami ne vien tik Rusija ir Baltarusija, bet ir ištisa Europos Sąjunga – neabejotinas ženklas, kad kovodama su Astravo AE Lietuvos vyriausybė prarado paskutinius adekvatumo likučius. Jo ir anksčiau buvo nedaug, bet dėl to, kad daugelį metų trukusios pastangos sustabdyti atominės elektrinės statybą nedavė rezultatų, oficialus Vilnius, artėjant lemiamai valandai, yra pasiruošęs pasiduoti kolektyviniam pamišimui.

Kokiomis racionalinėmis mintimis nesivadovautų Lietuvos valdžia, nuspręsdama iki galo kovoti prieš atominę elektrinę kaimyninėje šalyje (o jie, neabejotinai, jomis vadovavosi), iracionalumas jų veiksmuose jai seniai užtemdė racionalumą. Kalba emocijos, o ne interesai ir juo labiau ne vertybės.

Lietuva kovoje su šituo projektu tai išpūtė „statymus“, kad būsimas pralošimas, kurį konstatuoja atominės elektrinės veiklos pradžia, sukels grupinį priepuolį respublikos vadovybėje. Vilnius tokioje būklėje bus pasiryžęs viskam.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 7 — id: `scraped:rubaltic_lt:b2dfc26c15f6d792`

**Title:** Vokiečių feldmaršalas apsidengė dėmėmis, o prancūzų generolas šokių metu nukrito: kaip buvo pasirašytas Vokietijos kapituliacijos Aktas

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Iš maršalo Georgijaus Žukovo prisiminimų:

„Vokiečiams buvo pasiūlyta atsisėsti už atskiro stalo, kuris buvo specialiai jiems skirtas ir pastatys netoli įėjimo.

Atsistojęs, aš pasakiau: „Siūlau vokiečių delegacijai prieiti čia, prie stalo. Čia jus pasirašysite besąlygiškos Vokietijos kapituliacijos Aktą“.

Keitelis greitai atsikėlė, pažiūrėjęs į mus priešiškai, o paskui nenėrė akis ir, lietai paėmęs nuo staliuko maršalo lazdą, netvirtais žingsniais pajudėjo link mūsų stalo. Jo monoklis krito ir pakabo ant užraiščio. Veidas apsidengė raudonomis dėmėmis... Grąžinęs monoklį į vietą, Keitelis atsisėdo ant kėdės pakraštį ir šiek tiek drebančia ranka pasirašė penkis Akto egzempliorius. Tuoj pat juos pasirašė ir Stumpffas su von Friedeburgu.

Po Akto pasirašymo Keitelis atsikėlė nuo stalo, užsimovė dešinę pirštinę ir iš naujo pamėgino padaryti įspūdį kariška laikysena, bet tai jam nepavyko, ir jis tyliai žengė prie savo stalo.

Iš Nikolajaus Antipenko, 1-ojo Baltarusijos fronto užnugario vadovo, parengusio šventinę vakarienę Vokietijos kapituliacijos Akto pasirašymo minėjimui, prisiminimų:

„Pasak fronto vadovybės nurodymus, vakarienę turėjo būti sudaryta iš tarybų nacionalinių patiekalų. Vadovaujantis šitais nurodymais, vyriausiasis virėjas V. Pavlovas pasiūlė rusų kopūstienę, ukrainiečių kalakutą, Uralo pyragą, gruzinų šašlyką, skirtingus žuvies patiekalus ir pan.

Žinoma, mums buvo nelengva viskuo tuo aprūpinti vakarienę. Bet juk ir įvykis neįprastas: pergale pasibaigė keturių metų kova ir šia proga ir susirinko šalių-nugalėtojų atstovai.

Mes stengėmės gerai priimti svečius, ir, kaip aš dabar įžiūriu, puota išėjo puiki. Tiesą sakant, neapsiėjo be nenumatytų sunkumų. Pietūs buvo paruoštas gegužės 8 dienos 15 valandai, bet tuo metu Akto pasirašymo ceremonija net neprasidėjo: dar tesėsi derybos tarp Maskvos, Vašingtono ir Londono dėl pasirašymo procedūros.

Tik vielai naktį atėjo ilgai laukta akimirka. Kapituliacija buvo paskelbta 1945 metų gegužės 9 dieną apie 0 val.45 min. Maskvos laiku. Antrą valandą nakties visi ceremonijos dalyviai buvo pakviesti vakarienei.

Puotą trumpu tostu Pergalei, tarybų kariuomenei, sąjunginių valstybių kariuomenėms ir visų dalyvaujančių puotoje sveikatai pradėjo maršalas Žukovas. Paskui savo tostus paskelbė kiti šio vėlyvo pietaus dalyviai. Jis pasibaigė dainomis ir, žinoma, narsu rusišku šokiu. Šoko maršalas Žukovas.

Išsiskyrėm mes tą akimirką kaip tikri kovos draugai. Ir atrodė, jog ta draugystė sutvirtinta kovos su neapkenčiamu priešu krauju, truks amžinai ir niekas nesutrikdys gerų santykių tarp rusų, anglų, amerikiečių, prancūzų. Deja...“.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 8 — id: `scraped:rubaltic_lt:5b46fb66b65ee4bb`

**Title:** JAV priverčia Lietuvą užpirkti amerikietiškus testus koronavirusui

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Oficialus Rusijos Federacijos Užsienio Reikalų ministerijos atstovas Marija Zacharova paskelbė, kad JAV valdžia priverčia Lietuvą užpirkti amerikiečių gaminamus koronaviruso testus bei individualios apsaugos priemones. Anksčiau Lietuvos vadovybė iš tikrųjų pasirašė stambią sutartį su Thermo Fisher Scientific Baltics – JAV kompanijos vietiniu padaliniu. Lietuvos valdžia galėtų pavadinti tai vaizdingu euroatlantinės vienybės atveju bei dviejų sąjunginių valstybių efektingu bendradarbiavimu, bet nei Lietuvos URM, nei JAV valstybės departamentas, nei patys Thermo Fisher Scientific Inc. Zacharovos pareiškimą kažkodėl nekomentuoja. Nejaugi yra, ką slėpti?

„Oficialiems JAV asmenims ne gėda daryti spaudimą savo europiečių partneriams, kai kalbama apie amerikiečių kompanijų komercinius interesus, nesvarbu kas tai – prekyba energijos nešėjais, technologijomis, ginklavimusi ar vaistiniais preparatais. Dabar tokio politinio spaudimo taikiniu tapo ir Lietuva; tikslas – paskatinti Vilnių užsipirkti koronaviruso testų ir apsaugos priemonių iš JAV gamintojo, Thermo Fisher Scientific korporacijos, ir viskas tai – nepaisant to, kad paminėta kompanija jau anksčiau šiais metais neatliko savo įsipareigojimų pagal kitą sutartį su Lietuva“, - teigė Rusijos URM oficialus atstovas.

Thermo Fisher Scientific – visame pasaulyje žinomas mokslinės ir medicininės technikos gamintojas. Į Lietuvos rinką kompaniją įžengė 2010 metais, kai įsigijo 100% akcijų jau seniau veikusios čia transnacionalinės korporacijos Fermentas International.

Nuo tų laikų Baltijos šalies valdžia lepina kompaniją visais įmanomais būdais. Į kompanijos laboratorijos atidarymą 2015 metais asmeniškai atvyko pati Dalia Grybauskaitė. Ir žavėsi tuo, kad „lietuvių mokslininkų kuriami produktai atveria naujas galimybes kovojant su pražūtingomis lygomis visame pasaulyje“.

Nenuostabu, kad Thermo Fisher Scientific kartu su kitomis panašios specializacijos kompanijomis atsidūrė kovos su koronavirusu priešakyje.

Pavyzdžiui, praėjusį mėnesį paaiškėjo, kad Thermo Fisher Scientific Inc. perka už 11,5 milijardų dolerių olandų kompaniją Qiagen, kuri gamina medicininius testus (taip pat ir koronavirusui). Nuo metų pradžios šitas sandoris tapo stambiausiu „prarijimu“ medicinos srityje.

Qiagen – vienas pasaulio lyderių molekulinės diagnostikos srityje. Besinaudojant savo duomenimis, kompanija pagamino greituosius testus koronavirusui ir pradėjo juos tiekti Kinijai vasario pabaigoje. Jau po kelių dienų amerikiečiai nusprendė kompaniją „pričiupti“, o paskui buvo paskelbta, kad Qiagen gavo iš JAV Sveikatos apsaugos ir socialinių tarnybų ministerijos Biomedicinos pažangiųjų tyrimų ir plėtros tarnyba (BARDA) skyrė beveik 600 tūkstančius dolerių savo testų rinkinio QIAstat-Dx gamybos paspartinimui.

Oficialus Vašingtonas skelbia šitą akciją kaip dalį globalių pastangų kovoje su koronavirusu.

Tačiau, Thermo Fisher Scientific ir be olandų partnerių turi pakankamai kompetencijų koronaviruso testų gaminimo srityje. Didžiules viltis su bendradarbiavimu su korporacija sieja asmeniškai Trumpas, kurio administracija paruošė ištisą partnerystės planą su JAV komercinėmis laboratorijomis. Ir taip atsitiko, kad Thermo Fisher Scientific turi savo laboratoriją Lietuvoje. Tokiu atveju kodėl vietinė valdžia turėtų kreiptis į ką nors kitą?

Kovo 20 dieną tarp Baltijos šalies ir amerikiečių korporacijos pasirašytos testų tiekimo sutarties piniginė suma sudaro beveik 2 milijonus eurų.

„Testų poreikis Jungtinėse Valstijose – 10 milijonų per dieną. Kol kas niekas nepajėgia tai padaryti, bet mes bendradarbiaujame su visu pasauliu, ir Lietuva užima itin aukštą pagal prioritetą padėtį tų šalių, kurioms Thermo Fisher Scientific tieks testus, sąraše“, - teigia korporacijos lietuviško padalinio vadovas Algimantas Markauskas. Tai yra, patiems amerikiečiams neužtenka, o jie dalinasi su savo ištikimais sąjungininkais Rytų Europoje. Argi ne euroatlantinės vienybės pavyzdys?

Pačios Thermo Fisher Scientific Baltics vieklą galima pavadinti žymiu JAV ir Lietuvos kooperacijos pavyzdžiu. Kompanija kontroliuojama amerikiečių, bet ji teikia darbo vietas vietos gyventojams. Pačioje Baltijos šalyje gamins dalį komponentų koronaviruso testams. Thermo Fisher Scientific padalinio buvimas Lietuvoje turi užtikrinti tai, kad problemų nustatant mirtiną lygą čia neištiks – ačiū Amerikai!

Taip galima būtų bent pateikti šią istoriją. Bet vyriausybė nusprendė neafišuoti kooperacijos su Thermo Fisher Scientific fakto.

Rusijos URM oficialaus atstovo pasirodymas spaudai buvo ketvirtadienį, balandžio 9 dieną. Šio straipsnio paruošimo dienai praėjo daigiau už tris poras. Bet iš JAV valstybinio departamento nėra jokios reakcijos ir jokių komentarų. Tyli ir Thermo Fisher Scientific vadovybė, nors jai pirma verta būtų paneigti Zacharovos žodžius. Apkaltinimai nesąžininga konkurencija – skaudus smūgis bet kurios kompanijos reputacijai.

Bet pats nuostabiausias yra tas faktas, kad tyli oficialus Vilnius. Kažkodėl nesuveikė sąlyginis refleksas – neigti visas „klastotes“ dėl situacijos Baltijos šalyse, kurias skleidžia Kremlius. Čia pats Dievas liepė ne vien tik paneigti Zacharovos žodžius, bet ir viešai sugėdinti ją. Kaip tik galima buvo apkaltinti dorus amerikiečius, kurie padeda savo sąjungininkams!

Spėliojimą, kad Lietuvos Užsienio reikalų ministerija neatkreipė dėmesio į Rusijos URM pareiškimą, galima paneigti iš karto. Tokius dalykus Linkevičius ir jo kompanija stebi prioriteto tvarka. Ypač dabar, kai jie teigia, kad Kremlius ėmėsi įnirtingų informacinės kovos veiksmų prieš Europos Sąjungos ir NATO.

Žinoma, kad amerikiečių korporacijos filialas buvo ne vieninteliu pretendentu reagentų gamybai. Sveikatos apsaugos ministras Aurelijus Veryga pranešė apie derybas su įvairiomis kompanijomis.

Kodėl galų gale pasirinkimo buvo verta Thermo Fisher Scientific? Nejaugi pasiūlė pačias palankias sąlygas?

Panašu, kad šitą ir daugelį kitų klausimų Lietuva nusprendė palikti be atsakymo.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 9 — id: `scraped:rubaltic_lt:7121912b731010b7`

**Title:** Trys scenarijai: ką ketino Gorbačiovas padaryti su Lietuva, kai yrėsi Tarybų Sąjunga?

**Source:** rubaltic_lt (propaganda)

**Text:**

```
1990 metais tarp Michailo Gorbačiovo ir Baltijos respublikų vadovų vyko derybos dėl Lietuvos, Latvijos bei Estijos išstojimo iš Tarybų Sąjungos. Prieš derybų pradžią Ministrų Tarybos, Valstybinio plano komiteto, Valstybinio materialinio techninio tiekimo komiteto bei Valstybinio statistikos komiteto darbuotojai paruošė TSRS prezidentui ataskaitas apie Baltijos respublikų ekonominę padėtį. Pateikiame jūsų dėmesiui šiuos unikalus dokumentus.

I variantas

Lietuvos dalyvavimas TSRS sąjunginėje rinkoje.

Pagrindu skelbiama susiklosčiusi 1990-1991 metų tvarka perėjimo prie rinkos ekonomikos sąlygomis.

Prieš visuotinį perėjimą prie didmeninės prekybos Valstybinio plano ir Valstybinio materialinio techninio tiekimo komitetai pagal bendrą tvarką, nustatytą liaudies ūkiui, skiria Respublikų Ministrų Taryboms centralizuotai skirstamų išteklių limitus be apribojimų pagal šakas ir sritis.

Atsižvelgiant į tai, TSRS ir Lietuvos santykiai plečiami sekančiu būdu:

1. Lietuvoje esančių įmonių ir organizacijų materialinio ir techninio aprūpinimo pagrindinė forma – tiesioginiai neriboti užsakymai, įforminti horizontalių ūkinių ryšių tarp gamintojo ir vartotojo tiekimo sutartimis (kaip variantas – per tarpininkavimo organizacijas).

Informacinė pastaba. Tokiomis sąlygomis TSRS organizuojami ryšiai pagal 8 tūkstančius gamybinės ir techninės paskirties produkcijos rūšis, kurie 1990 metais sudarė apie 40%, o 1991 metais – apie 60% bendros produkcijos kainos.

II variantas

Lietuvos išstojimas iš TSRS pereinamuoju laikotarpiu kelių metų bėgyje.

Už pagrindą priimami principai, nustatyti Pagrindinėmis liaudies ūkio stabilizacijos ir perėjimo prie rinkos ekonomikos kryptimis bei TSRS įstatymu „Dėl įmonių TSRS“, pagal kuriuos įmonės parengia savo gamybos ir kapitalinės statybos materialinį bei techninį aprūpinimą įsigyjant išteklius prekių ir paslaugų rinkoje.

Kelių metų bėgyje Lietuvoje, kaip ir visoje Sąjungoje apskritai, realizuojama nuosavybės denacionalizavimo ir privatizacijos programa, o įmonėms, organizacijoms ir piliečiams taikoma ūkinės veiklos ir verslininkystės tiesioginė laisvė, pagal kurią visi gamybos ir aprūpinimo klausimai jų sprendžiami savarankiškai.

Atitinkamai, pereinamojo laikotarpio kelių metų bėgyje:

1. Tiesioginiai neriboti užsakymai, įforminti horizontalių ūkinių ryšių tarp gamintojo ir vartotojo tiekimo sutartimis tampa pagrindinė aprūpinimo forma. Pradedant nuo 1992 metų visos TSRS ir Lietuvos įmonės ir organizacijos (išskyrus esančių Sąjungos jurisdikcijoje gynybinių ir kuro ir energijos gaminančių įmonių apribotą sąrašą) pagal visą gamybinės ir techninės paskirties produkcijos nomenklatūrą organizuoja materialinį bei techninį aprūpinimą bet jokio TSRS ir Lietuvos valstybinių organų dalyvavimo.

III variantas

Lietuvos išstojimas iš TSRS be jokio pereinamojo laikotarpio.

Vadovaujamasi TSRS ir užsienio šalių ekonominių ryšių susiklostę principai, organizacija ir praktika.

Atitinkamai, ekonominiai santykiai tarp TSRS ir Lietuvos įforminamos ilgalaikiais (kas 5 metams) Sutarymais dėl prekių apyvartos ir apmokėjimų tarp TSRS ir Lietuvos bei kasmetiniais Protokolais dėl prekių apyvartos ir apmokėjimų tarp TSRS Ministrų Tarybos ir Lietuvos Ministrų Tarybos.

Į Sutarymą dėl prekių apyvartos ir apmokėjimų tarp TSRS ir Lietuvos bus įtraukti keturi prekių sąrašai:

1 – tarybinio eksporto,

2 – lietuviško eksporto,

3 – tarpusavyje susijusių tarybinių ir lietuviškų prekių tiekimai,

4 – prekių, kurių tiekimai atliekami pagal tiesiogines sutartis tarp įmonių ir atsižvelgiant į tam tikras licencijavimo taisykles.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 10 — id: `scraped:rubaltic_lt:d94fc6665ce5d85b`

**Title:** “Koronakrizė“ irsta Baltijos šalių infrastruktūrą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Dėl koronaviruso pandemijos Lietuvoje laikinai sustabdyti Ignalinos atominės elektrinės uždarymo darbai. Reguliariai iš darbo atleidžiami Latvijos nacionalinė oro linijų bendrovė airBaltic. Baltijos šalių geležinkeliai ir jūros uostai dar prieš krizę pranešdavo apie rekordinius nuostolius. Baltijos šalių transporto bei energetikos infrastruktūroms, kurios dar prieš koronavirusą buvo kritinėje padėtyje, COVID-19 pandemija gręsią visuotiniu sugniužimu.

Nuo balandžio 6 dienos Ignalinos atominė elektrinė buvo perkelta į „tausojantį“ režimą: artimiausiomis dvejomis savaitėmis bus atliekama įmanomai mažiausia darbų apimtis. Tai nulėmė sunki epidemiologinė padėtis Baltijos šalyje. Publikacijos parengimo metu laboratoriniai patvirtintų koronaviruso atvejų skaičius Lietuvoje peržengė 800. Skaičius, žinoma, ne itin didelis, bet šaliai, kurios gyventojų skaičius vos seka 3 milijonus, ir jo užtenka tam, kad pradėti nerimauti.

Ignalinos vadovybė atsidūrė prie būtinybės maksimaliai sumažinti darbuotojų kontaktų skaičių. Kai kas iš jų pervestas į darbą nuotoliniu būdu, apie tūkstantį žmonių bus prastovoje (darbo užmokestį jiems buvo pažadėta išsaugoti). Atominės elektrinės pavedimas į karantiną – visai sveika priemonė, nes po energoblokų uždarymo jokios naudos šaliai jėgainė neduoda.

Deja, tai nereiškia, kad „koronakrizė“ aplenks Ignalinos jegainę. Praeitų metų rugsėjį Lietuvoje pradėta statyti radioaktyviųjų atliekų saugykla, prieš kelias dienas buvo paskelbtas tenderis dviejų gelžbetoninių modulių statybai. Apytikslė objekto kaina – 73,1 milijonų eurų. Didžiąją šių lėšų dalį pristatys eurofondai. Ir viskas būtų gerai, bet kalbama vos apie žemo radioaktyvumo lygio atliekas. Ką daryti su likusiomis – lieka neaišku.

Sauliaus Skvernelio vadovaujama vyriausybė praeitais metais pasisakė už iniciatyvą pradėti rinkti lėšas ilgaamžių atliekų saugyklos statybai, kuri pagal planą prasidės vos 2056 metais. Galvoti apie tai verta jau šiandien, nes statybos kaina – 2,5 milijardų eurų.

Dokumente, kurį parengė Lietuvos Respublikos Energetikos Ministerija, siūloma kaupti lėšas rezerviniame fonde – kasmet perkelti ten maždaug 25% nuo visų įplaukusių į valstybės biudžetą valstybinių įstaigų dividendų.

„Lietuva atsakingai žiūri į ilgaamžių radioaktyviųjų atliekų saugojimą, - pabrėžė energetikos ministras Žygimantas Vaičiūnas. – Kad užtikrinti strategiškai svarbų ir ilgalaikį pastovų finansavimą, mes privalome jau dabar numatyti lėšų kaupimo šaltinius tam, kad nereikėtų vartoti pinigų iš valstybinio biudžeto, o visi darbai ateityje turi būti atliekami laiku ir kokybiškai“.

Iš pradžių buvo numatyta, kad pagrindiniu visų Ignalinos jėgainės likvidavimo išlaidų finansavimo šaltiniu bus Europos Sąjunga. Iki šiol taip ir buvo, nors skiriamų lėšų žiauriai neužtenka.

„Šitų pinigų užtenka tik būtiniausioms operacijoms, kad objekte nekiltų negatyvių technogeninių pokyčių, kad galima būtų užkonservuoti jėgainę daugmaž stabilioje būsenoje ir perkelti Ignalinos AE likvidavimo klausimą naujai nepriklausomos Lietuvos mokesčių mokėtojų kartai“, - teigia energetikos sferos ekspertas Aleksejus Anpilogovas.

Po „koronakrizės“, kuri, pagal įvairių ekspertų įvertinimus, bus daug siaubingesnė, nei 2008-2009 metų finansinis „sudrebėjimas“, Ignalina tikrausiai taps Lietuvai dar sunkesniu „branduoliniu lagaminu be rankenos“. Tiesiog pasireikš tai ne iš karto, kaip ir Baltijos šalių uostų artveju.

Rygos laisvojo uosto atstovai, pavyzdžiui, skelbia, jog nepaprastosios padeties režimas Latvijoje neturi žymios įtakos sostinės jūros uostui. Daryti išvadas apie tai galima bus tik po oficialių krovinių apyvartos apimčių duomenų publikacijos, bet jei net dabar uostas veikia įprastu režimu, koronaviruso pasekmes jie ištirs dar ilgai. Kol kas neaišku kokių krovinių perkrovimas nukentės.

„Latvijas dzelzceļš“ sustabdo geležinkelių elektrifikaciją, gaujomis atleidžia iš darbo savo darbuotojus ir prašo iš valstybės 40 milijonų eurų dotacijų. „Įplaukos taip sumenkėjo, kad jos net nedengia išlaidų, kurios sumažintos iki pačio minimumo“, - su kartėliu skelbia LDz.

Tokioje pat prastoje padėtyje atsidūrė ir Latvijos nacionalinė oro linijų bendrovė airBaltic. Kovo 24 dieną valstybės Ministrų kabinetas palaikė 150 milijonų eurų investavimą į bendrovės pagrindinį kapitalą.

Visuotiniame nuotolinio darbo režime vairuotojai lieka be darbo, o kompanijos neturi finansinių rezervų krizės įveikimui.

Epidemija pridarė bėdos – net po jos pabaigos vargu ar Baltijos šalys sugebės atstatyti buvusias prekių eksporto apimtis.

„Pagalvokite, kiek laiko reikės tam, kad atsirastų naujos rinkos. Ir tai yra tragedija, nes ryšiai suardyti. Mes prarandam eksporto šalis, pavyzdžiui Vokietiją, Italiją. Kam parduosim mūsų produkciją? Gal, Rusija nupirks, tačiau visi ryšiai su ja irgi suardyti. Toks yra politinis sprendimas“, - apgailestauja buvęs Lietuvos prekybos ministras Albertas Sinevičius, kuris priligina šalies padėtį su 1990 metų blokadą.

Koronavirusas lygtinai padalino visas pasaulio šalis į dvi grupes: vienos sukaupė finansines atsargas, kitos – ne.

Pastarųjų dienų naujienos dėl Baltijos transporto ir energetikos infrastruktūros būklę labai gerai tai parodo.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 11 — id: `scraped:rubaltic_lt:1ca3aecde400d565`

**Title:** Vietoj paramos Lietuvai reagentų stokai nugalėti JAV išveža iš Europos koronaviruso testus

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Klaipėdos miesto meras Vytautas Grubliauskas pranešė, kad miesto mobilus koronaviruso patikros punktas uždarytas dėl reagentų stokos. Patikros sutrikimai tuo metu, kai Lietuvoje 129 patvirtinti koronaviruso atvejai yra akivaizdus nacionalinio saugumo pavojus. Vilniui šiuo atveju reikėtų gauti palaikymą iš sąjungininkų, deja išėjo visai ne taip. Epidemijos įkarščio metu amerikiečiai gabena iš Italijos 500 tūkstančius sudedamųjų dalių skirtų COVID-19 diagnostikos sistemoms.

Iš pradžių Jungtinių Valstijų ir farmacijos kompanijos Copan Diagnostics Inc. sandorį nebuvo ketinama skelbti viešai. Patys save išdavė amerikiečiai, kurie savo Instagram paskyroje pasidalino nuotrauka, padaryta karinio transporto lėktuvo Boeing C-17 Globemaster III pilnutėliame salone.

Socialiniuose tinkluose pradėjo plisti gandai, jog kovo 17 dieną amerikiečiai apsilankė Italijos šiaurėje ir išvežė iš ten privačios laboratorijos Copan Diagnostics Inc. – virusinių ligų nustatymo testų gamintojų – produkciją. Komplektai tepinėlio SARS-CoV-2 – naujo koronaviruso štamo – nustatymui gaminami būtent čia.

Atrodytų, tai galėjo būti klastotė. Bet Italijos gamintojo ir Pentagono atstovai tylėjo, o gandai iš socialinių tinklų nukeliavo į žiniasklaidą bei ekspertų sritį. Žurnalistai neslėpė savo pasipiktinimo.

„Visas pasaulis teigia, jog tai yra karas. Ir pirmąkart istorijoje – visų karas prieš visus. Čia nėra nei sąjungų, nei sąjungininkų, kiekvienas rūpinasi tik savimi. Kovoje prieš koronavirusą pagrindinis ginklas – tamponai, kaukės, respiratoriai, testai. Amerikiečiai, nusipirkę pus milijoną testų tepinėliams, pervežė šiuos trofėjus į Memfį ir švenčia savo pergalę“.

Kas leido testo sistemų pardavimą Jungtinėms Valstijoms? Kiek pinigų amerikiečiai pasiūlė už prekes? Kas pasipelnė iš tiekimų? Atsakymų šitiems klausimams nėra iki šiol. Bet kai kas paaiškėjo, kai su oficialiu pareiškimu pasirodė JAV karinių oro pajėgų brigados generolas Polas Frydrichsas.

Visų pirma, jis patvirtino pasklidusių gandų tikrumą: „Koronaviruso testai susideda iš keleto dalių. Pirma – tamponai skirti biologinės medžiagos paėmimui iš paciento. Antra – skistis, kurioje tamponai talpinami. Tai mes ir atvežėm iš Italijos“.

Antra, pasak Frydrichso, kalbama apie paprastą sandėrį, neva JAV ir patys gamina tokius tamponus, bet nusprendė apsipirkti Europoje, kad „patenktinti globalią paklausą“.

Kitas JAV karinių oro pajėgų vadas generolas Davidas Goldfeinas pridėjo, kad bendradarbiavimas su Italijos įmonėmis prasitęs – artimiausiomis dienomis planuojami nauji sandėriai. Besilieka tik spėlioti, kokios prekės nuplauks už okeano šitą kartą. Ar yra garantijų, kad amerikiečiai vadovaudamiesi asmeniniu Trumpo įsakymu neišpirks Italijos rinkoje visus medikamentus ir įrangą. kurių taip trūksta europiečiams?

Baltųjų Rūmų šeimininkui tai – ne kliūtis. Ypač atsižvelgiant į paskutinių dienų įvykius, kai vyriausybė prarado kontrolę virš padėtį dėl koronaviruso. Pagal užsikrėtusių skaičių šalis užėmė trečiąją vietą pasaulyje.

Copan Diagnostics Inc. ragina nedidinti įtempimą. Kompanija taip pat liovėsi tylėdama ir paaiškino, kad nesiverčia diagnostinių medžiagų gamyba. Jos specializacija – komplektai skirti koronavuriso analizei, tai yra tamponai.

«Stokos nėra. Kaip ir draudimo prekiauti su užsieniu. Įmonė jau kelius dešimtmečius eksportavo į JAV savo produkciją, bet dėl koronaviruso mes patyrėme problemų su logistika. Todėl amerikiečiai surengė skubų tamponų nugabenimą transporto lėktuvu“, - paaiškino įmonės generalinė direktorė Stefanija Triva. Ir prigrėsė teismu kai kuriems leidiniams už nepatikrintos informacijos platinimą.

Vis dėlto, kaltė už gandų skleidimą iš dalies priklauso pačiai kompanijai. Naivu buvo galvoti, kad JAV karinio transporto lėktuvo patraukymas sandėrio įgyvendinimui gali likti nepastebėtas. Kodėl visuomenė nebuvo informuota iš anksto?

Beje, Copan Diagnostics vadovybė ir Pentagonas išlaikė ilgą pauzę prieš tai, kaip paskelbti savo įvykių versiją.

Arba Boeing C-17 Globemaster III lėktuvas, kuris grįžo iš Italijos, gabeno ne vien tik konteinerius su tamponais?

Vyriausybė šitą situaciją taip ir nekomentavo. Tai yra savaime aišku: kritikuoti amerikiečius visai nesinori, o teisinti juos – tuo labiau. Komentarai šiuo atveju, daugiausia, nereikalingi.

Vietoj to, „dėdė Semas“ prekiauja su italais, lyg nieko neatsitiko. Nieko asmeniško, tik verslas.

Besilieka vos vienas svarbus klausimas: ar nekenkia šita komercija Europos interesams, kai jos šalys atsidūrė kovos su koronavirusu priešakyje?

Jau minėta Lietuva, kuri praeitą savaitę susidūrė su reagentų deficitu, dėl ko aptiko koronaviruso testavimų sutrikimų. Galėtų pasakyti amerikiečiams, kad šalia verslo dar egzistuoja sąjungininkų santykiai, ir šiuo atveju pirkti iš Europos jai būtiniausias prekes, pasiūlydami geriausią kainą – amoralu.

Bet nepasakys. Tyliai praris.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 12 — id: `scraped:rubaltic_lt:0471274d541eecee`

**Title:** Kalniškio mūšis: stambiausios „miško brolių“ kautynės su tarybų kariuomene

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Iš 1-ojo Pabaltijo fronto NKVD kariuomenės 220-ojo Kutuzovo ordino pasienio pulko operatyvinių karo veiksmų, skirtų gaujos Lietuvos TSR Alytaus apskrityje likvidavimui, aprašymo.

1945 m. gegužės 14 d. iš Simno rajono NKVD skyriaus viršininko gauti duomenys apie tai, kad Seminiškių miško rajone, 37 km į vakarus nuo Alytaus, 8 km į pietvakarius nuo Simno, slepiasi „miško brolių“ gauja, ginkluota rankiniais ir sunkiaisiais kulkosvaidžiais, automatais ir šautuvais. Ši gauja paskutinių 10 dienų laikotarpyje smulkiomis grupėmis iš 10-15 žmonių išeidavo iš miško ir užsiiminėdavo vietinių gyventojų plėšimu ir atskirų gyventojų išsivedimu į mišką...

Gegužės 16 dieną, vykdomas miško išnaršymą, 1-asis batalionas 2 kilometrų aukštyje į pietų rytus nuo Krasnianų, aptiko nenustatyto žmonių skaičiaus gaują, kuri, pastebėjusi mūsų karius ir pajutusi, kad yra blokuota, užėmė visapusiškas gynybines pozicijas aukštumoj ir pradėjo šaudyti iš rankinių ir sunkiųjų kulkosvaidžių, automatų ir šautuvų į artėjančius dalinius.

19 valandai, suspausdami apsupimo žiedą, sovietų daliniai susitelkė prie aukštumos.

Matydamas, kad dėl tokio priešo pasipriešinimo atakuojantys daliniai turės didelių nuostolių, įsakė: trims sunkiesiems kulkosvaidžiams, įsikūrusiems iš aukštumos skirtingų pusių, nuslopinti priešo pagrindinius šaudymo priemones - rankinius ir sunkiuosius kulkosvaidžius, kurie ypatingai trukdo prastūmimui, šaudymu „išvalyti“ medžių viršūnes, ant kurių sėdi „gegutės“.

Ir kai valandą užtrukusio šaudymo parengimo dėka priešo ugnies pasipriešinimas žymiai susilpnėjo, nusprendžiau: 9-osios sargybos jėgomis atakuoti priešą. Rytų, vakarų ir šiaurės aukštumos pusėse išsiskaldę į smulkias šturmo grupes po 12-15 žmonių tam, kad išvengti nereikalingų nuostolių, 9-oji sargybas pradėjo prastūmimą į aukštumą. Pietų šlaitas liko „atviras“ tam atvejui, jeigu gauja, neatlaikiusi atakos, puls pietiniu šlaitu, kurio papėdėje jau buvo sutelktos mūsų dalinių pagrindinės pajėgos.

Kadangi „miško broliai“ sumažino savo aktyvumą ir turėjo nuostolių dėl valandą trukusio mūsų dalinių artilerinio antpuolio, jie nebegalėjo atkakliai priešintis šturmo grupėms kai pastarosios pradėjo prastūmimą į aukštumą.

Kovos veiksmų rezultatai. Gaujos nuostoliai: likviduotas, sužeistas ir užgrobtas – 71 banditas.

Mūsų nuostoliai: nužudyti 4 raudonarmiečiai, sužeisti 7 raudonarmiečiai.

220-ojo pasienio pulko vadas majoras Jacenko.

P.S. Apie 20 „miško brolių“ sugebėjo prasilaužti per kovos rikiuotę ir pasislėpti artimiausiose Žuvinto pelkėse. Jų tarpe – vienas pačių įžymiausių „miško brolių“ vadų Jonas Neifalta slapyvardžiu Lakūnas. Neifaltos žmona žuvo su kulkosvaidžiu rankose.

„Miško brolių“ operacijų prieš sovietų kariuomenės metodai turėjo rimtą trūkumą. Jiems sekėsi netikėti „žaibiški“ užpuolimai, bet įnirtingame mūšyje jie buvo daug silpnesni už sovietų karius. Kalniškio mūšis puikiai vaizduoja, kas vyko, kai tokios grupės buvo priverstos kovoti sovietų sąlygomis.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 13 — id: `scraped:rubaltic_lt:6f884db13227dd12`

**Title:** Į Tarybų Lietuvą investavo 3-5 kartus daugiau, nei į kitus regionus: slaptų informacinių raštų, pateiktų Gorbačiovui 1990 metais, duomenys

**Source:** rubaltic_lt (propaganda)

**Text:**

```
1990 metais tarp Michailo Gorbačiovo ir Baltijos respublikų vadovų vyko derybos dėl Lietuvos, Latvijos bei Estijos išstojimo iš Tarybų Sąjungos. Prieš derybų pradžią Ministrų Tarybos, Valstybinio plano komiteto, Valstybinis materialinio techninio tiekimo komiteto bei Valstybinio statistikos komiteto darbuotojai paruošė TSRS prezidentui ataskaitas apie Baltijos respublikų ekonominę padėtį. Pateikiame jūsų dėmesiui šiuos unikalus dokumentus.

Informacinis raštas dėl klausimų, kurie gali kilti per artėjančias derybas su Lietuvos TSR.

1945 metais Lietuvos pramonės bendroji produkcija sudarė 40% nuo ikikarinių apimčių. Smarkiai sukentėjo žemės ūkio sritis. Palyginus su ikikariniais metais galvijų skaičius sumažėjo 53,6%, kiaulių – 63,9%, avių – 45,7%, pasėlių plotai – 20%, o derlingumas – 22%.

Nuostolis, padarytas respublikos ekonomikai nacių Vokietija, pasiekė 17 milijardų rublių (pagal 1941 metų kainų lygį), tarp kurių nuostolis valstybinėms pramonės įmonėms sudarė 4,8 milijardų rublių, kooperatyvinėms, profsąjungų, religinėms ir kitoms visuomeninėms organizacijoms – 0,9 milijardų rublių, o Lietuvos TSR piliečiams – 11,3 milijardų rublių.

Greitai energotraukiniai pradėjo veikti Akmenėje, Klaipėdoje ir kituose miestuose. Tam, kad atkurti liaudies ūkį iš Rusijos TFSR atvykdavo ešelonai su metalo pjovimo staklėmis, garo katilais, vidaus degimo varikliais, lokomotyvais, elektrine įranga, automobiliais, juodaisiais ir spalvotaisiais metalais...

Broliškų tarybinių respublikų paramos dėka sugriautos pramonės atkūrimui užteko mažiau už penkis metus. TSRS vyriausybė skyrė Lietuvai 200 milijonų rublių dotaciją. 1948 metais buvo pasiektas ikikarinis pramonės lygis.

Per 1945-1950 metus buvo pastatyta virš dviejų šimtų stambių pramonės įmonių. Metalo staklių gamyklos „Žalgiris“ bei elektrotechnikos gamyklos ELFA statyboje dalyvavo įmonės iš daugiau nei 40 kitų tarybų respublikų miestų. Įranga Kauno gamyklai „Pergalė“ buvo teikiama iš Rusijos TFSR, Ukrainos bei Baltarusijos TSR 50 miestų. Kauno hidroelektrinės statyboje dalyvavo beveik visos broliškos respublikos, Lietuvos Lenino valstybinės rajoninės elektrinės Elektrėnuose dalyvavo 200 sąjunginių įmonių, o įrangą Kėdainių chemijos kombinatui teikė daugiau už tris šimtus šalies įmonių.

Pavyzdžiui, per devintą penkmetį (1971-1975 metai) respublikai buvo suteikti gamybinės paskirties kapitaliniai įdėjimai, kurių dydis, jei perskaičiuot žemės ūkio naudmenų vienam hektarui, buvo 3,8 kartų didesnis nei TSRS vidurkis ir triskart didesnis, nei Rusijos TFSR. Atitinkamai per dešimtą penkmetį skirtumas sudarė 3,4 ir 2,6 kartų; per vienuoliktą – 3,2 ir 2,5 kartų; 1986-1989 metais – 3,4 ir 2,5 kartų. Tai nulėmė tą, kad 1 ha dirvos kapitalo ir darbo santykis šiandieninėje Lietuvos TSR 2,6 kartų didesnis, nei bendras šalies rodiklis, ir 2,8 kartų didesnis nei Rusijos TFSR.

Už valstybės lėšas respublikoje buvo įgyvendinti stambi žemės melioracijos, kaimo socialinės plėtros, kelių statybos darbai. 1970-iems metams respublikos 36% žemės ūkio naudmenų buvo numelioruoti, o dabar šitas rodiklis pasiekė 70% (kadangi bendras TSRS rodiklis sudarė atitinkamai 3% ir 7%). Tai nulėmė puikias galimybes tam, kad išvežti žemės ūkio produkciją už respublikos ribų.

Daugelis respublikos kolūkių ir tarybinių ūkių gaudavo materialinių bei techninių išteklių dotacinėmis kainomis. Lietuva dirvos 1 ha gaudavo 3-5 kartus didesnes dotacijas, nei kiti TSRS regionai, nes materialinių ir techninių išteklių tiekimai čionai buvo žymiai stambesni. Tai leido gerokai padidinti žemės ūkio našumą.

Nurodyto periodo kapitalinių įdėjimų lyginamasis svoris pagal pramonės įmones ir organizacijas sudaro 45%, pagal pramoninės paskirties objektus – 52%. Iš viso nuo 1940 iki 1989 metų Lietuvos TSR teritorijoje įvykdytų valstybinių kapitalinių įdėjimų didis sudaro 38,7 milijardų rublių, iš kurių 28 milijardai rublių išleisti pramoninės paskirties objektams. Jeigu laikytis 1986-1986 metų pramonės įmonių ir sąjunginio pavaldumo įmonių kapitalinių įdėjimų lyginamojo svorio, tai už 1940-1989 metus kapitalinių įdėjimų apimtis pagal šią įmonių grupę sudarys 17,5 milijardų rublių, iš jų – 14,6 milijardų rublių skirti pramoninės paskirties objektams.

Šaltinis: Tarybų ekspertų informacinis raštas paruoštas M. Gorbačiovo deryboms su Lietuvos TSR vyriausybe, kuri paskelbė išstosianti iš TSRS, nuo 1990.08.09.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 14 — id: `scraped:rubaltic_lt:2a18040d61996a8e`

**Title:** TSRS išgelbėjo žmoniją: Molotovo-Ribentropo paktas nulėmė Hitlerio sumušimą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lenkijos užsienio reikalų ministras Jacekas Čaputovičius pripažino Tarybų Sąjungos pagrindinį vaidmenį Nacistinės Vokietijos nugalėjime. Tuo pačiu metu Čaputovičius eilinį kartą apkaltino Maskvą Molotovo-Ribentropo pakto pasirašymu. Tuo tarpu Tarybų Sąjungos ir Trečiojo Reicho nepuolimo sutartis tapo lemtingu Hitlerio armijos sumušimo faktoriumi. Be šios situacinės sutarties TSRS būtų sparčiai sunaikinta, kas nulemtų nacių įsivyravimą pasaulyje. Sovietų Sąjunga išgelbėjo žmoniją, ir Molotovo-Ribentropo pakto lemiamą įtaka pripažino patys nacių bonzai Niurnbergo tribunole.

1939 metų rugpjūtį Stalinas paskutinį kartą mėgino sukurti iš Prancūzijos, Didžiosios Britanijos bei TSRS antihitlerinę karinę sąjungą. Bet dėl Paryžiaus ir Londono nekonstruktyvių pažiūrų ir Lenkijos tiesioginio pasipriešinimo ir ši pastanga nebuvo sėkminga. Sovietų Sąjungai tebeliko paskutiniausia – sutikti pasirašyti sutartį su Vokietija, gauti iš to didžiausią pelną ir nudelsti karo pradžią. Bet jis vis tiek buvo neišvengiamas.

Po laimėjimų Austrijoje ir Čekoslovakijoje Hitleris tapo panašus į bėgiką, pasiruošusį startui. Pasaulio pagrobimą jis pradėrtų bet kuriuo atveju, apie ką visiškai aiškiai parašyta knygoje Mein kampf. Tarybų Sąjungos vadovybė tolimesnį situacijos vystymąsi numatė absoliučiai aiškiai.

Bet kiekis nelemia kokybės.

Reikėtų turėti omeny, kad 1939 metų rugpjūčio mėnesį Tarybų Sąjunga Chalchyno upės baseine buvo įtrauktą į sudėtingą ginkluotą konfliktą su Japonija, Vokietijos sąjungininku. Bendras TSRS ir japonų kariuomenės, dalyvavusios karo veiksmuose Chalchyno baseine, skaičius sudarė 130 tūkstančių žmonių. Karo veiksmuose dalyvavo apie 700 tankų, virš tūkstančio pabūklų ir minosvaidžių, daugiau nei 1200 lėktuvų.

Žinoma, kad 1939 metų rugpjūtį Vokietija energingai dalyvavo derybose dėl nepuolimo sutarties (Pakto) sudarymo ne vien tik su TSRS, bet ir su Didžiąja Britanija. Vokietijai buvo reikalingas laikas tam, kad pasiruošti karo veiksmams. Taip pat reikėjo užliūliuoti būsimų priešų budrumą.

Turėkite omeny, kad Didžiosios Britanijos užsienio reikalų ministras lordas Halifaksas 1938 metų rugsėjį teigė: „...Vokietija ir Didžioji Britanija yra Europos taikos du šulai ir pagrindinės antikomunistinės atramos, todėl būtina taikos būdu nugalėti mūsų dabartinius sunkumus... Galbūt, galia rasti sprendimą, prieinamą visoms šalims išskyrus Rusiją“.

Žinoma, kad įžymiojo „Kembridžo penketuko“ nariai, dirbęs britų Užsienio reikalų ministerijoje Donaldas Maklinas, ir jo kolega Gajus Berdžesas, buvęs tuo pačiu metu ir anglų žvalgybos darbuotoju, 1939 metais pranešė Maskvai, kad Londono pagrindinė politika tėra tame, kad „bendradarbiauti su Nacistine Vokietija prieš TSRS“ .

Neatsitiktinai anglai pakto su Vokietija pasirašymo klausymais veikė daug energingiau, nei TSRS. 1939 metų liepą britų ministro-pirmininko patarėjas Vilsonas parengė anglų-vokiečių bendradarbiavimo programą, žinomą kaip „Vilsono planas“. Rugpjūčio vidury Ribentropas gavo eilinį šio plano variantą. Anot jo, buvo numatytas 25 metų „gynybinės sąjungos“ sudarymas tarp Didžiosios Britanijos ir Vokietijos, palaipsniui vykstantis kolonijų grąžinimas Vokietijai, „įtakos sferų atribojimas, įskaitant Vokietijos ypatingų interesų pripažinimą“, ir t.t.

Pakto su TSRS sudarymas tapo didžiausiu Hitlerio suklydimu, nulėmusiu Trečiojo Reicho suirimą. Germanas Geringas Niurnbergo proceso metu pastoviai minėdavo šią fiurerio pražūtingą klaidą.

Taip Molotovo-Ribentropo paktas leido žmonijai pakeisti savo ateitį.

1939 metų rugpjūtį tarybinė vyriausybė atsidūrė prieš nelengvą pasirinkimą: arba pasirašyti sutartį su Nacistine Vokietija, arba artimiausioje ateityje kovoti dviem frontais. Tokiu atveju pradėti karą tektų po Minsku ir po Leningradu.

Galiausiai, Vermachtas pradėtų TSRS puolimą būdamas vos tik 32 kilometrų atstume nuo Minsko. Taip pat būtina pažymėti, kad Tarybų Sąjungos vadovybei Hitlerio planai po Lenkijos užgrobimo okupuoti Baltijos šalis nebuvo paslaptimi, juo labiau ten vyravo draugiški Vokietijai profašistiniai režimai.

Toliau milijoninė Hitlerio „Šiaurės“ armijų grupė pasuktų link Maskvos. Tokiu atveju vargu ar Sibiro divizijos sugebėtų sustabdyti vokiečių antpuolį į TSRS sostinę 1941 metų gruodžio mėnesį. O toliau prie karo prisidėtų Japonija, ir, galbūt, pasaulio istoriją šiandien rašytų Trečiojo Reicho istorikai.

Ribentropo-Molotovo paktas tapo rimtu šių sutarimų pažeidimu. Vokietija, būdama Japonijos sąjungininkė, „padarė pastarajai didžiulę kiaulystę“.

Japonų savimonei tai buvo itin skaudus smūgis. Neatsitiktinai 1941 metų birželio 26 dieną Japonijos Ginkluotųjų pajėgų Generalinio štabo viršininko pavaduotojas Osamu Cukada teigė: „Net jei Vokietija laikys situaciją išskirtinai palankia, <...> mes neišžygiuosim“.

Priešingu atveju Antrojo pasaulinio karo pabaiga galėjo tapti visiškai kita. Tai, kad naciai galėjo užgrobti Maskvą ir tuo beveik nuniokoti TSRS, nėra vienintelė problema. Situacija rytuose būtų nekiek ne lengvesnė. Ten japonų karinis pranašumas buvo visuotinis. Aviacijoje pranašumas buvo trijų kartų, toks pat – ir karinėse jūros pajėgose.

TSRS išgelbėjo pasaulį

TSRS įveikimo atveju Hitleris gautų gamtos ir žmonių išteklių kartu su milžiniškos Tarybų Šalies teritorija. Jokia jėga nekliudytų jam įgyvendinti jo plano vyrauti visame pasaulyje. Nekelia abejonių, kad Anglija pasiduotų fiurerio malonei. Jungtinės Valstijos tradiciškai nuspręstų perlaukti už okeano, kol vokiečių mokslininkai ir inžinieriai nepasibaigtų naujų ginklų – atominės bombos, tarpkontinentinės balistinės raketos, reaktyvios aviacijos ir pan.- kūrimą. O toliau karinė situacija vystytųsi nacių naudai.

Tiesą sakant, tai nebuvo pilnavertiški branduoliniai sprogimai, bet jie rimtai stūmė į priekį nacių branduolinę programą. Neatsitiktinai 1945 metų sausį Vokietijos Ginkluotės ir karinės pramonės reichsministras Albertas Špėras pareiškė: „Mums reikia išsilaikyti dar vienus metus, ir tada mes laimėsim karą. Egzistuoja degtukų dėžutės didžio sprogmuo, kurios kiekio užteks ištiso Niujorko sunaikinimui“.

Gavusi TSRS išteklių, Vokietija sukurtų naują ginklą žymiai greičiau. Galų gale žmonija būtų pasmerkta ilgaamžiai nacių vergovei. Tai, kad Hitleris mokė siekti savo tikslų, liudija jo 1933-1939 metų veiklos rezultatai.

Neatsitiktinai 1945 metų vasarį JAV valstybės sekretorius Edvardas Stettinius per Jaltos konferenciją pareiškė, kad „Amerikos žmonėms reikia atminti, kad jie buvo arti pražūties 1942 metais. Jeigu Sovietų Sąjunga neišsilaikytų ant savo fronto, vokiečiai turėtų galimybę užgrobti Didžiąją Britaniją. Jie okupuotų Afriką ir galėtų įsivyrauti Lotynų Amerikoje. Tokia grėsmė buvo nuolatos prezidento Ruzvelto rūpestis“.

JAV armijos štabo viršininkas, būsimas JAV valstybės sekretorius ir ekonominės paramos Europai plano autorius Džordžas Maršalas savo pranešime „Dėl pergalingo karo Europoje ir Ramiajame vandenyne“, kurį jis pristatė 1945 metų gruodį JAV vyriausybei, pripažino: „Mes iki šiol neįsisąmoninom, ant kokio plono plaukelio kybojo JTO likimas 1942 metais! Kaip arti Vokietija ir Japonija buvo pasaulinio įsivyravimo! Ir mes privalome pripažinti, kad amerikietiška pozicija tais laikais nedaro mums garbės“.

Tai, pasakysim tiesiai, menka kaina, turinti omeny, kad nugalėjimo atveju, kaip pabrėžė Hitleris 1939 metų spalio 17 dieną, naciai ketino „išvalyti“ Europos teritoriją nuo „žydų, lenkų ir likusių sąvalkų“ .

Šiandien keletas politikų ir istorikų mėgina iš visų jėgų įrodyti prieškario tarybinės vadovybės sumanymų ir politikos nusikalstamumą. Daugiausiai, tai yra žmonės, kuriems lemtis neleido pajusti sunkią valdžios bei galinčių pakeisti istorijos eigą šalyje ir pasaulyje sprendimų atsakomybės naštą. Kiekvienas jų serga futbolo sirgaliaus sindromu, kurio pagrindinis simptomas – „manyti save strategu, stebėdamas mūšį iš šalies“.

Pagrindinį prieškario TSRS politikos įvertinimą suteikė šiuolaikinis pasaulis, kuriame šiandien egzistuoja žmonija.

Visi likusieji turėtų neprieštaraujamai laikytis jų įsakymų ir, kaip tikėjosi nacių ideologai, gerbti Hitlerio išvaizdos stabus, įkurtus nacių ideologiją, neva išgelbėjusią pasaulį nuo komunistinio totalitarizmo ir pražūties, šlovinančiose šventyklose.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 15 — id: `scraped:rubaltic_lt:6f01521945b4fbdd`

**Title:** Lietuvos norai lieka be Europos Sąjungos paramos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Baltijos šalys susidūrė su sisteminiu savo iniciatyvų ignoravimu Europos Sąjungoje. Visi Baltijos valstybių pasiūlymai pradedant ES plėtra ir Ukrainos parama ir užbaigiant nuosavų infrastuktūros projektų vystymusi prieštarauja naujam europietiškam kursui link jėgų ir lėšų ekonomijos. Baltijos šalys atkakliai sugalvoja, kam išleisti svetimus pinigus, o Europos Sąjunga valdančios valstybės-donorės lygiai taip pat atkakliai leidžia suprasti, kad jos savo pinigus švaistyti nesirengia.

Neseniai Lietuva išreiškė pritarimą tolimesnei Europos Sąjungos plėtrai ir paragino priimti į „Europos šeimą“ Albaniją ir Makedoniją.

„Mes turime atsižvelgti į kandidatų lūkesčius ir atliktus darbus. Abi šalys parodo, kad yra ES ištikimi partneriai, nuosekliai derina savo politiką su ES bendra užsienio politika bei bloko saugumo politika, o Albanija dar nuo 2009 metų priklauso NATO“, - teigė Lietuvos Respublikos užsienio reikalų ministras Linas Linkevičius ir išreiškė viltį, kad kovo mėnesį Briuselyje priims sprendimą pradėti derybas dėl Albanijos ir Šiaurės Makedonijos įstojimo į Europos Sąjungą.

Europos Sąjunga praranda 75 milijardus eurų dėl Didžiosios Britanijos išstojimo, bet Baltijos politikų tai nekiek nesutrinka. Jie lyg nieko nebūtų atsitikę siūlo išsaugoti ir plėtoti savo šalių dotavimą, o dar priimti į ES visai nepadoriai skurdžias Albaniją ir Makedoniją, kad Europos Sąjungos regionų vystymosi išlyginimo politika būtų pritaikyta ir joms.

Duok „Naujajai Europai“ laisvę, ji ir Ukrainą su Moldaviją tuoj pat priims į ES, kad rumunų ar latvių skurdas „Europos šeimoje“ atrodytų nedidelis palyginus su ukrainiečių ar moldavų. Kur rasti pinigų jų integracijai – klausimas ne Rytų Europai. Jinai tų pinigų vis vien neturi.

Sugalvoti, kam išleisti svetimus pinigus – lengva ir malonu. Bet čia finansiniai optimistai iš Europos periferijos anksčiau ar vėliau susiduria su nauja rūsčia realybe.

Praeitais metais Albanijos ir Makedonijos klausimu prieš tolimesnės ES plėtros pasisakė Danija, Prancūzija ir Olandija: šalys-donorės, kurios pagrįstai įtarusios, kad joms tą plėtrą ir teks apmokėti.

Emanuelis Makronas tada visiškai atvirai paaiškino savo prieštaravimus prieš ES plėtrą į Vakarų Balkanus: „Kaip aš paaiškinsiu savo piliečiams, kad antros šalies, iš kurios gauname labiausiai politinio prieglobsčio prašymų, atstovai, yra žmonės atvykstantys iš Albanijos?“

Su Ukraina situacija atrodo visai negražiai. Visi Lietuvos projektai dėl Europos bendros finansinės paramos šaliai virto niekais. Tarkim, „Maršalo planas Ukrainai“, pagal kurį buvo siūloma susidėjus skirti Kijevui 50 milijardų eurų europietiškų reformų įgyvendinimui. Vakarų „vyresni bičiuliai“ net neatkreipė dėmesio nepaisant įkyrų eks-ministro-pirmininko Andriaus Kubiliaus pastangų.

Pačiai Ukrainai kaskart, kai šalis demonstruoja savo eurooptimizmą, leidžia suprasti, kad klausimas dėl Kijevo integracijos į ES nesvarstomas. Ir niekada nebuvo, lygiai taip pat kaip ir kitų postsovietinių respublikų, ES „Rytų partnerystės“ programos narių, atžvilgiu.

Lietuva, Latvija ir Estija viena po kitos rašo kolektyvinius laiškus Briuseliui, prašydamos atkreipti dėmesį į geležinkelio Rail Baltica sunkią padėtį. Pastarosios paleidimas į eksploataciją ir taip atidedamas jau kelius metus iš eilės, o be greitosios „piniginės“ pagalbos projektas iš vis gali būti uždarytas. Kad nepridaryt sau gėdos, „amžiaus statybai“ reikia skirti papildomą Europos finansavimą.

Bet Europos Sąjunga veikia atvirkščiai ir dar ketina sumažinti jau paskirtą Rail Baltica projektui biudžetą.

Panašios situacijos beveik su visais stambiais infrastruktūros projektais kuriems iki šiol buvo skiriamos ES lėšos. Baltijos šalių išstojimas iš BRELL (Baltarusija – Rusija – Estija – Latvija – Lietuva) energetinio žiedo dabar abejotinas dėl ES struktūrinių fondų mažinimo. Lietuvos SGD terminalui, iš pradžių planuotam kaip priemonė ES fondų pinigams išsiurbti, nebuvo skirta nei vieno eurocento iš Briuselio.

Europos Sąjungos karinio mobilumo programos, pagal kurią buvo numatyta transporto infrastruktūros plėtra sparčiam kariuomenės perkėlimui prie ES išorės sienų, biudžetas vos už kelis kartus buvo sumažintas nuo 6,5 milijardų eurų iki... nulio. Programos galutiniais naudos gavėjais ir kartu jos pagrindiniais lobistais buvo Lietuva, Latvija ir Estija.

Bet realybėje paaiškėjo, kad net tokiam „šventam tikslui“ kaip Baltijos gynyba nuo Putino tapusi žiauriai šykšti Europos Sąjunga pinigų duoti nepageidauja. Pasirodė, gobšumas taip užvaldė Vakarų Europos ES donorėmis, kad jeigu Putinas iš tikrųjų nuspręs užgrobti Estiją, Latviją ir Lietuvą, jos tik pasidžiaugs. Juk tai dar didesnė ekonomija...

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 16 — id: `scraped:rubaltic_lt:abf9f1b03b7e20c3`

**Title:** Trumpas atėmė skirtus Lietuvos gynybai pinigus sienos su Meksika statybai

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Vašingtonas ketina žymiai sumažinti išlaidas skirtas Europos atgrasymo iniciatyvos (European Deterrence Initiative — EDI) finansavimui. Iniciatyva buvo paleista po Krymo prijungimo prie Rusijos ir už 5 metus „išsipūtė“ iki rekordinių 6,5 milijardų dolerių. Dabar JAV prezidentas Donaldas Trumpas nutraukia šias machinacijas: dalis lėšų skirtų Rusijos „nulaikymui“ NATO rytų ribose Trumpas perskirs savo mylimos sienos su Meksika statybai.

Plačiai žinoma, kad amerikiečių lyderis skeptiškai vertina daugumą savo pirmtako, Barako Obamos, projektų. Bet EDI iniciatyva yra išimtis: po praėjusių JAV prezidento rinkimų jos fondas teauga. Būtent Trumpas 2017 metais pasiūlė viršplaninį asignavimo didinimą Europos apsaugai nuo „Rusijos agresijos“.

Šitą idėja skeptiškai priėmė net kai kurie jo vienpartiečiai, nes suteikti papildomas finansines privilegijas kariškiams galima tik sumažinus kitas biudžeto išlaidas. Užtat džiaugėsi NATO generalinis sekretorius Jensas Stoltenbergas, kuris rėmėsi Trumpo finansiniu planu argumentuodamas JAV prezidento ištikimybę euroatlantinėms vertybėms.

Bet 2019 metais šita schema liovėsi veikti. Po rekordinių 6,5 milijardų dolerių EDI biudžetą sumažino iki 5,9 milijardų. Nauja Pentagono užklausa nebedžiugina ir JAV karinio buvimo didinimo šalininkų Europoje.

Apie prioritetų pasikeitimą Trumpo komandoje paaiškėjo praėjusį rudenį. Baltųjų rūmų „šeimininkas“ pageidavo iškratyti pinigų iš EDI fondo tam, kad ištesėti savo priešrinkiminį pažadą ir rasti lėšų JAV ir Meksikos valstybinės sienos modernizacijai – Trumpo sienos statybai.

Dėl šio projekto 2018 metų pabaigoje tarp prezidento ir Kongreso kilo karas, JAV vyriausybė buvo priversta laikinai sustabdyti savo darbą. Nuo tų laikų Trumpas pradėjo ieškoti alternatyvų skandalingo pastato finansavimui.

„Kadangi Baltieji rūmai yra pasiruošę prašyti mažiau pinigų sienai artėjančioje oficialioje biudžeto užklausoje Kongresui, administracija, panašu, vis labiau pasikliauna Pentagono lėšomis savo tikslo – papildomų barjerų valstybės sienoje statybai – įgyvendinimui, – praneša CNN. – Trumpo administracija teigė, kad jai nereikia Kongreso pritarimo tam, kad perskirti karines lėšas „Trumpo sienai“.

Praėjusių metų rugsėjį Pentagonas paskelbė „Trumpo sienos“ statybos „dėka“ finansavimo neteksiančių projektų sąrašą .

Tai daug mažiau, nei reikalinga Trumpui, todėl „sulys“ ne vien tik Europos atgrasymo iniciatyva, bet ir visos kitos išlaidos taip vadinamoms užsienio nepaprastosioms operacijoms. Omeny turima amerikiečių sąjungininkų parama Afganistane, Irake, Sirijoje ir kitose valstybėse.

Atsižvelgiant į istorinės reikšmės JAV ir talibų taikos sutarties pasirašymą ši kryptis atrodo logiškai. Jeigu nekils netikėtų situacijų, per 14 mėnesių Afganistane nebeliks nei vieno amerikiečių kariškio.

Analitinis portalas RuBaltic.Ru jau rašė , kad rinkimų išvakarėse Trumpas suinteresuotas ilgiausio JAV istorijoje karo užbaigimu. Ir čia dėlionės fragmentai sutampa idealiai, nes pasitraukimas iš Artimųjų Rytų ir sienos statyba pasienyje su Meksika – esminiai Trumpo priešrinkiminės kampanijos pažadai. Telieka visai nedaug laiko tam, kad juos įvykdyt.

Tuo tarpu reikalai su „Trumpo siena“ nesikloja. Pagal paskutiniausius pranešimus statybos darbai užbaigti tik 131 mylių ruože. Tai reiškia, kad užbaigti projektą Trumpui vis tiek teks po rinkimų (žinoma, tuo atveju, jei jis išlaikys prezidento pareigas). Dabar jis tegali parodyti tautiečiams, kad Kongreso pasipriešinimas nekliuvo jam išspręsti finansavimo problemą.

Iš viso iš užsienio programų „Trumpo sienos“ statybai atims beveik pusę reikalingos sumos (1,8 milijardų dolerių).

Bet yra ir kita medalio pusė. Trumpas, kaip yra plačiai žinoma, nuosekliai kritikuoja Europą už nepageidavimą didinti išlaidas savo gynybai. Nedaugelis ES valstybių pasak Vašingtono reikalavimą padidino savo karinį biudžetą iki 2% nuo šalies BVP. Tai yra suprantama: Pentagono bendrų išlaidų didinimas ir amerikietiškos Rusijos „atlaikymo“ programos „išpūtimas“ jų neskatina.

Dabar situacija turėtų pasikeisti. Pasak JAV gynybos sekretorių Marką Esperį Vašingtonas tikrai duoda ženklą savo europiečių sąjungininkams.

Įsidėmėtina tai, kad Trumpo impičmento istorija iš dalies yra susieta su EDI. Per šitą fondą yra teikiama karinė parama Ukrainai, ir anais metais JAV prezidentas šitą paramą nusprendė apriboti. Tuo būdu, pasak demokratus, jis šantažavo Kijevą.

Trumpas turėjo tam net du paaiškinimus: iš pradžių buvo kalbama apie šių lėšų taikymo racionalumą, paskui Baltųjų rūmų šeimininkas prasitarė, kad norėtų įteikti Ukrainos paramos naštą Europai.

Bet kuriuo atveju, po grandiozinio skandalo 250 milijonų skirtų Ukrainai naujo Pentagono biudžeto projekte niekas „nelietė“. Už Ukrainą atkentės ES šalys. Bet kas tiksliai?

Atsakymą randame jau paminėtame sąraše, į kurį įtraukti projektai, kurių įgyvendinimą Pentagonas nusprendė atidėti tam, kad finansuoti sienos su Meksika statybą. Tarp Europos šalių pagal šių projektų skaičių pirmauja Vokietija, nors pagal EDI prie „ilgalaikius“ buvo priskirtas vos vienas sandėliavimo patalpos statybos projektas Ramštaino oro bazėje. Tarp Vidurio ir Rytų Europos šalių „kliuvo“ Vengrijai, Rumunijai, Slovakijai, Estijai bei Lenkijai.

Žinoma, kalbama apie labai kuklias sumas. Pentagonas atėmė iš visų po truputį. Pamažu iš viso pasaulio – Trumpui užteks jo sienai pastatyt. Bet pats lėšų perskirstymo faktas vargu ar džiugina Rytų Europos JAV globotinius. Septynerius metus jie atlaiko nesiliaunančią „Rusijos agresiją“. Ir staiga paaiškėja, kad Putino Baltuosiuose rūmuose bijo mažiau nei kažkokių meksikietiškų nelegalų.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 17 — id: `scraped:rubaltic_lt:5138d07b114923f7`

**Title:** „Numetė“ savo čekistus kaip „amerikiečių desantą“: kaip sovietų specialiosios tarnybos likvidavo vieną iš „miško brolių“ vadų Juozą Lukšą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
NKVD vilkšunis, „miško brolių“ sovietų siaubas Nachmanas Dušanskis, kuris pokario metu dirbo MGB Kauno poskyryje, kovojančiame su banditizmu, paliko prisiminimus apie tai, kaip buvo likviduotas vienas iš Lietuvos antisovietinio pasipriešinimo vadų – Juozas Lukša:

Pirmąkart Lukša atkreipė į save NKVD tarnybų dėmesį iškart po Lietuvos išvadavimo nuo nacių. Jis dalyvavo Lietuvos studentų susitikime su atvykusiu iš Maskvos rašytoju ir pagrindiniu Stalino laikų publicistu Ilja Erenburgu ir perdavė svečiui iš salės raštelį, kuriame buvo sakoma: „Stalinas ir Hitleris – Lietuvos okupantai“. O kažkas iš susitikimo dalyvių iškart atpažino Lukšą kaip vieną iš tų studentų, kurie 1941 metų birželį peiliais pražudydavo ir laužais negyvai užplakdavo Kauno žydus per „Lietūkio“ garažo žudynes.

Tą dieną Lukšą nespėjo suimti, jis paspruko į mišką pas „miško brolius“ ir partizanavo iki 1947 metų, o paskui kartu su Krikščiūno gauja, kurioje buvo apie 5-7 žmonių, bandė su kova prasiveržti per Lenkijos sieną į vakarus. Per šitą epizodą juos beveik visus likvidavo, bet Lukša staiga pasirodė gyvas jau Stokholme, o iš ten persikėlė į Ameriką, kur metus mokėsi žvalgybos mokykloje, spėjo vesti ir parašyti savo pirmą prisiminimų knygą.

1949 metų rudenį, anglų žvalgybai dalyvaujant, jis buvo nusiųstas į Lietuva pro Londoną. Tai buvo pats „Šaltojo karo“ įkarštis, ir mūsų buvę sąjungininkai dirbo prieš TSRS kartu. Mes iš anksto žinojome, kad Lukša turi greit pasireikšti mūsų kraštuose, gavome iš Maskvos perspėjimą apie tai. JAV ambasados pareigūnas, aišku, kad žvalgytojas dirbęs kaip diplomatas, padėjo į slaptavietę konteinerį skirtą jo agentui. Konteineris buvo laikinai atsargiai išimtas, o jame buvę dokumentai – sufotografuoti. Tarp dokumentų buvo rastas laiškas lietuvių kalba, kurį persiuntė mums. Pagal rašyseną nustatėme, kad tai yra Lukšos laiškas, kuriame jis savo draugei Reginai Budreikaitei parašė: „Greit pasimatysime“.

Pats Lukša su savo parašiutininkų grupe nusileido sėkmingai, bet po jų buvo numesta Širvio vadovaujama diversantų grupė, kuri buvo vietinio MGB rajono skyriaus sulaikyta iškart po nusileidimo: du diversantai buvo sulaikyti gyvi, i vienas buvo nužudytas susišaudymo metu.

Mes iškart surinkom savo diversinę netikrą „Širvio grupę“, kurią numetėme į mišką ryšininko gyvenamame rajone. Mūsų agentai apsimetinėdami „desantu iš JAV“ susisiekė su ryšininku ir pasakė, jog atvežė Lukšai naujų instrukcijų ir panašiai. Lukša nusprendė patikrinti „naujokus“ ir liepė Moščinskiui užduoti Širviui klausimą: „Koks buvo šuns su trejomis kojomis, kuri gyveno tame pačiame name, kaip ir mus, vardas?“. Bet Širvys mums viską papasakojo, mes žinojome daugelį smulkmenų, net šuns vardą, tad mūsų atsakymas buvo teisingas.

Lukša sutiko atvykti į susitikimą su „Širvio būriu“ ir „Kauno pogrindžio atstovais“, kuris buvo paskirtas Garliavoje, 12 kilometrų atstume nuo Kauno. Nuo susitikimo su mūsų agentu-vedliu vietos iki Garliavos reikėjo naktį nukeliauti pėsčiomis 30 kilometrų pro mišką, o toks kelias galėko užtrūkti ne vieną naktį.

Lukšos suėmimo operaciją įdėmiai sekė iš Maskvos su savo spec.grupe atvykęs MGB ministro pavaduotojas generolas Eugenijus Pitovranovas. Įsakymas buvo griežtas: „Suimti gyvą bet kokia kaina!”, nes paskui ketino pateikti Lukšą į JTO kaip anglų bei amerikiečių specialiųjų tarnybų žvalgybinės ir diversinės veiklos prieš TSRS įrodymą. Vedlį, agentą slapyvardžiu „Jonukas“, prieš pat operaciją Pitovranovas instruktavo pats asmeniškai. Jis žadėjo agentui, kad tuo atveju, jei jis nuves Lukšą gyvą iki tos vietos, kur pasislėpus pasaloje laukia suėmimo grupė, gaus Tarybų Sąjungos Didvyrio garbės vardą, įsakymas tam jau paruoštas.

Paskui buvo Lukšos gaujos likusių dalyvių sulaikymas.

Pradėjome nagrinėti, kiek žmonių kraujo praliejo kiekvienas iš jų. Tardymo metu klausiu vieną suimtą į nelaisvę Lukšos gaujos banditą: „Anksčiau jus šovėt milicininkus, komunistus, raudonarmiečius, naikintojų batalionų savanorius, bet savus, įprastus lietuvius, kam šovėt? Eigulį kam nužudei? Jis gi su mumis nebendradarbiavo...“. O „sukilėlis“ atsakė: „Šitas eigulys karo metu 10 žydų išgelbėjo, už tai ir buvo nubaustas“. Patikrinome ir sužinojome, kad tikrai šitas eigulys pas save slėpė nuo nacių 10 pabėgėlių, pasprukusių iš Kauno geto, tarp jų – pogrindininką Mišą Musulasą, kuris tai patvirtino...

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 18 — id: `scraped:rubaltic_lt:b6b8720ab20c3538`

**Title:** „Daugelį žmonių užkasinėjo gyvus, po ko žemė judėjo po kelias valandas...“: nacizmas Lietuvoje

**Source:** rubaltic_lt (propaganda)

**Text:**

```
3-iojo Baltarusijos fronto Kontržvalgybos SMERŠ valdybos generolo leitenanto ZELENINO specialus pranešimas dėl nacionalistinės organizacijos „Šaulys“ veiklos.

Visiškai slaptai, 1944 metų rugsėjo 3 dieną.

Pagal 3-iojo Baltarusijos fronto Kontržvalgybos SMERŠ valdybos turimus duomenis tarp visų Lietuvos TSR egzistuojančių ir mūsų atskleistų nacionalistinių organizacijų okupacijos laikotarpiu labiausiai savo veikla pasižymėjo organizacija „Šaulys“.

Nustatyta, kad labiausiai savo veikla organizacija „Šaulys“ pasižymėjo Lietuvos TSR nacių okupacijos laikotarpiu.

11-osios gvardijos armijos SMERŠ skyriaus sulaikytas „šaulietis“ PAVLAITIS Germanas tardymo metu parodė:

„1941 metų rugpjūtį pagal vokiečių vadovybės įsakymą Marijampolės apskrities policija surengė masines apskrityje gyvenančių žydų gaudynes. Visa policija, įskaitant mane, buvo išsiųsta į gyvenvietes, iš kur mes išveždavome sulaikytas žydų šeimas kartu su kūdikiais, sodindavome į vežimus ir su ginkluota palyda atgabendavome į Marijampolės miestą.

Už tris operacijos dienas mūsų pastangomis buvo suvaryti apie 7700 žydų – moterų, senių, vyrų ir visų amžių vaikų.

Trečią dieną, Šventojo karaliaus Liudviko minėjimo dieną, visi jie, apie 7700 žmonių, buvo policijos sušaudyti. Aš, kaip ir visi kiti, dalyvavau pasmerktų žūti sergėjime ir sušaudyme...“.

Pasakodamas apie Marijampolės apskrities žydų žudynių aplinkybes, 1944 metų rugpjūčio 12 dieną Pavlaitis parodė:

„Prieš sušaudymą visi pasmerkti žūti buvo užrakinti arklidėse.

... Po kalinių kratos iš jų skaičiaus išrinko fiziškai stiprus vyrus, kurie buvo priversti kasti duobes. Iš viso buvo iškastos 8 duobės, iš jų dvi – 150 metrų ilgio, 5 metrų gylio ir 4 metrų pločio, o likusios 6 duobės – 100 metrų ilgio, 4 metrų pločio bei 5 metrų gylio.

Kai visi žydai buvo priversti nusirengti ir liko tik su apatiniais, prasidėjo sušaudymas.

Pirmiausia sušaudė vyrus, atvesdami juos po 100-200 žmonių grupes.

Kai visi vyrai buvo sušaudyti, tokia pat tvarka pradėjo moterų ir visų amžių vaikų šaudymą.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 19 — id: `scraped:rubaltic_lt:b62dba57d9cdd88b`

**Title:** Lietuvių chunveibinai persekioja rusų kalbos mokytoją už meilę Rusijai

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvoje prasidėjo nauja kitamanių persekiojimo kampanija. Persekiojimo auka tapo Klaipėdos rusų gimnazijos rusų kalbos mokytoja, kuri išdrįso palankiai atsiliepti apie Sovietų Sąjungą, Rusiją ir Putiną. Mokiniai įrašė dėstytojos žodžius ir pateikė garso įrašą “kur reikia”. Naujai atsiradusių lietuvių “kultūros revoliucijos” chunveibinų* poelgis nusipelnė Klaipėdos miesto valdžios ir stambiausios Lietuvos žiniasklaidos aukščiausiojo pritarimo.

“Tu teisingai pažymėjai, aš – už Rusiją. Ir kai man sako, vienaip ar kitaip, kad ten nėra išsilavinusių žmonių, kad ten neaišku, kas vyksta, man darosi juokinga”, - sako garso įraše Klaipėdos Vidūno gimnazijos rusų kalbos mokytoja Galina Liachova.

Šitie žodžiai yra ginčo apie Rusiją, Lietuvą ir TSRS su mokiniais pabaiga.

Liachina, pavyzdžiui, išdrįso palyginti šiuolaikinę Lietuvą su sovietų laikų respublika ir teigė, jog okupacijos laikais buvo daug geriau.

“Jus dar nematėte tų gamyklų, kurias panaikino. Kiek darbo vietų jose buvo! Kokios mokyklos buvo kaimuose, aš gi jums pasakojau. Kaip puikiai buvo aprūpinami kabinetai. Veikė ir felčerio punktai, ir poliklinikos, viskas. Ką padarė? Ką pastatė?” – klausia mokytoja ir dar drįsta peikti Lietuvos laimėjimus Europos Sąjungos sudėtyje.

«Puiku, skaičiuojame jau ketvirtą jūsų nepriklausomybės dešimtmetį. O jeigu nebūtų ES, ar išgyventumėte? Gana, nieko nebesakysiu. Jūsų tėvams buvo suteikti butai. Ar jie mokėjo už juos ar ne? Atsakykit! O mane erzina, kai sako: “Jie patys užsidirbo”», - pasipiktina Liachova, kalbėdama apie tai, kad tarybų Lietuvoje butus dalino nemokamai, o dabar už butą reikia atiduot apie 50-60 tūkstančių eurų.

Nauja atsakinga karta nusprendė, kad nesvarstyti tokius pareiškimus neleistina it pateikė pokalbio garso įrašą “kur dera”. “Iš kur dera” įrašą perdavė lietuvių žurnalistams.

Galinos Liachovos vardą niekina stambiausia Lietuvos žiniasklaida, o pasisakyti apie jos politinius požiūrius laikė būtina net pats Klaipėdos meras. Vytautas Grubliauskas pavadino Liachovos žodžius “gėdingais” ir padėkojo politiškai išprususiems moksleiviams, kurie “pasirodė gerokai sąmoningesni, pilietiškesni ir patriotiškesni, nei juos „mokanti“ pedagogė”.

Klaipėdos Vidūno gimnazijos, kur dėsto pedagogas, direktoriuis žado padaryti išvadas, galbūt net orgišvadas, po skandalo išnagrinėjimo.

“Mes su ja aptarėm šitą situaciją, iš kur atsirado tokios temos. Aptariama tema buvo Rusija, vaikai turėjo klausimų, savo nuomonę, mokytoja aiškino savo ir, matyt, peržengė leistiną ribą. Mūsų visai nedžiugina tokia situacija, bet mes ją išspręsim, įvertinsim, išnagrinėsim ir pasistengsime padaryti viską, kad vaikai viską suprastų teisingai”, - pakomentavo situaciją Arvydas Girdziauskas.

Miesto valdžia daro gana skaidrias užuominas į kito vietinio “kitamanio nusikaltėlio” – buvusio Klaipėdos miesto savivaldybės tarybos deputato Viačeslavo Titovo – likimą.

Titovas drįso suabejoti nacionalistinio pogrindžio kovūnų – “miško brolių” – “heroizmu” ir nepripažino savo “mirtinos nuodemės”. Už tai iš jo, nepaisant rinkimų rezultatų, dukart atėmė Klaipėdos miesto savivaldybės tarybos deputato mandatą.

“Nepaisant dėstytojos amžiaus, jos kvalifikacijos, patirties ir kitų aplinkybių, reikia aiškiai atsakyti į visus klausimus. Galvojau, kad žmonės pasimokė iš buvusio miesto savivaldybės tarybos nario istorijos, o pasirodė, kad ne”, - Klaipėdos meras Vytautas Grubliauskas faktiškai prigrėsė Galinai Liachovai atleidimu.

Turint reikalų su panašiomis naujienomis iš Lietuvos svarbiausia – apsiprasti, kad tai ne prisigalvota nesąmonė ir ne antiutopija. Tai vyksta realiame gyvenime. Specialiosios tarnybos įsiveržia į mokyklas dėl vaikų kelionių į vasaros stovyklas Rusijoje. “Tautos tėvas” siūlo rašytojai pasikarti miške už jos parašytą knygą apie lietuvių dalyvavimą Holokauste. Žinomas disidentas teisiamas po kaltinimo neva mėginęs pavogti teisėjus ir prokurorus ir tuo pačiu metu įrengti klausymosi aparatūrą valstybės prezidento kabinete.

O XXI amžiuje Europos Sąjungos šalyje Pavliko Morozovo “žygdarbis” vėl tampa sektinu pavyzdžiu jaunimui.

“ES Šiaurės Korejos” pelnytą titulą Lietuva, panašiai, jau peržengė ir dabar siekia Kambodžos diktatoriaus Pol Poto ir Kinijos lyderio Mao Dzedungo valdžios laikų laimėjimus. Artimiausia istorinė analogija su tuo, kas įvyko Klaipėdoje – chunveibinų, moksleivių, kurie padėjo Mao Dzedungui įgyvendinti “kultūros revoliuciją”, judėjimas.

Pirmomis ir pagrindinėmis moksleivių “tvarkos teroro” aukomis buvo, savaime aišku, dėstytojai

“Mūsų mokykloje aš mačiau vos tik vieną mušimą. Filosofijos mokytoja gana niekinamai žiūrėjo į tuos moksleivius, kam blogai sekėsi jos dėstamas dalykas. Tie mokiniai pajuto neapykantą jai ir apkaltino ją “suirimu”. Berniukai įvedė ją į kabinetą ir ėmėsi “revoliucingų priemonių”, - toks buvo mušimų eufemizmas. Man taip pat paaiškino, kad privalau dalyvauti bausmėje tam, kad įveikti savo silpnumą ir “pasimokyti iš revoliucijos”. Kai mušimas prasidėjo, aš pasislėpiau mažame kambaryje susitelkusių moksleivių galinėje eilėje. Kambario centre vienas po kito mokiniai mušė mano rėkiančią iš skausmo mokytoją. Jos šukuosena nuslinko į šoną, ji rėkė, maldavo, kad jie sustotų”, - tipiškas atsakingo kinų jaunimo kovos už ideologijos tyrumą aprašymas.

Bet kas žino, ir dalykai nenueis per toli, kai moksleivių niekšiškumą taip uoliai ragina šalies valdžia.

*Chunveibinai – 1960 metų Kinijos kultūros revoliucijos laikotarpio moksleivių bei studentų būriai, kurie naikino seną kultūros ir mokslo elitą, paminklus, istorinį paveldą ir t.t.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 20 — id: `scraped:rubaltic_lt:186e7ac26f63dcb1`

**Title:** „Baltijos tigru“ save vaizdavusią Lietuvą, kovojančią dėl Europos sąjungos dotacijų, laukia skurdas

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuva nenustoja kovojusi, kad tebeliktų eurofondų dotacijos. Respublikos prezidento patarėjo Simono Krepštos žodžiais, Vilnius nesusitaikė su Europos sąjungos 2021–2027 metų biudžeto projektu, o užsienio reikalų ministras Linas Linkevičius dokumento sudarytojams papriekaištavo nesąžiningumu. Tuo metu valdininkai sutartinai prabilo, kad už stiprios ekonomikos fasado slypi rimtos problemos. Kaip gi atsitiko, kad, svarstant daugiametę Europos sąjungos perspektyvą, „sėkmės“ Lietuva staiga tapo akiplėšiška elgeta?

Ginčai dėl septynerių metų Europos sąjungos biudžeto ciklo vis labiau kaista. Pirmasis Europos lyderių derybų raundas, vykęs praeitų metų spaly, rezultatų nedavė. Gruodžio samite istorija pasikartojo. Ir vargu, ar visi i taškai bus sudėlioti numatyto Europos sąjungos šalių vadovų susitikimo metu.

Neseniai Portugalijos Beža mieste įvyko „nuskriaustųjų suvažiavimas“: 15 valstybių grupė priėmė bendrą nutarimą sabotuoti tokio biudžeto projekto tvirtinimą. „Nė viena valstybė narė neturi nukentėti dėl smarkiai ir neproporcionaliai mažinamo Europos fondo solidarumo lėšų paskirstymo“, — sakoma bendrame pareiškime pagal susitikimo rezultatus.

Laikraštis Financial Times, aprašydamas priemonę, išskiria protesto akcijos iniciatores — Lenkiją su Vengrija. Šios šalys gali labiausiai nukentėti nuo atsisakymo tos politikos, kuri nukreipta „senosios“ ir „naujosios“ Europos šalių pragyvenimo lygio išlyginimui. Būtent jos laikomos pagrindinėmis ES riaušių organizatorėmis. Tad ar nepabandys Briuselis, siekdamas sutramdyti lenkus su vengrais, panaudoti finansinį „rimbą“?

Tiksliau, prieš projektus. Pirmiausia Vilnius sukritikavo Europos komisijos pasiūlymus, paskui visiškai sudirbo suomių variantą, kuris lietuviams buvo dar labiau nenaudingas. „Pagal komisijos pasiūlymą, mes būtumėm gavę 24 proc. mažiau sandūros politikos lėšų, kas mums nepriimtina, o pagal suomių pasiūlytą kompromisą sumažinimas būtų padidėjęs iki minus 27 proc. O tas dar labiau nepriimtina“, — prieš gruodžio ES samitą verkšleno Lietuvos finansų ministerijos atstovas Darius Trakelis.

Akivaizdu, jog per du mėnesius niekas nepasikeitė. Lietuvos valdžios nenori girdėti nieko — tvirtina, jog dabartinis biudžeto variantas nevykęs. Jo patvirtinimas Lietuvai apsieitų 270 mln. eurų per metus (maždaug tiek Pabaltijo respublika praras lyginant su praėjusia setynerių metų ES finansine parama).

Tai daug ar mažai? Kad situacija būtų aiškesnė, priminsime žinomą faktą: Klaipėdoje stovinčio terminalo Independence pastatymas kainavo 300 milijonų dolerių.

Nenuostabu, kad Vilniuje jaučiamas pasimetimas. Nors su pačiu dotacijų mažinimu valdžios susitaikė. „Visi žinojo, kad mažinimas bus“, — su lūdesiu pripažįsta finansų vice ministrė Miglė Tuskienė. Žinojo, bet nesitikėjo tokio žiauraus rezultato.

Pagrindinė įvykio priežastis gerai matoma — iš ES traukiasi Didžioji Britanija, pasiimdama iš bendro katilo milijardinius įnašus. Be jos prancūzų–vokiečių branduoliui bus daug sudėtingiau šelpti Rytų Europos išlaikytinius. Tuskienė išskiria ir kitas priežastis: „Mes kalbame apie naujus prioritetus — gynybą, saugumą, globalų atšilimą. Viską bandoma įsprausti į ankstesnį biudžetą“.

Kyla klausimas: kuo gi nepatinka Lietuva? Pagrindine savo išorine grėsme Europos sąjunga tebemato RF. Tam, kad atremtų „rusų agresiją“, apie kurią pastoviai paisto Lietuvos valdžios, jai būtina daugiau lėšų skirti gynybai ir saugumui.

Dar vieną lėšų, skiriamų Lietuvos „šelpimui“, mažinimo priežastį atskleidžia prezidento patarėjas Simonas Krėpšta. Pabaltijo respublika ... per daug sėkminga.

„Lietuva pastaraisiais 7 metais pademonstravo ženklų BVP augimą vienam gyventojui. Tai vienas iš kriterijų, kodėl mažinamos jai skiriamos lėšos“, — tvirtina Krėpšta.

Atrodytų, pats laikas apsidžiaugti ir šelpimo mažinimo faktą įvardinti kaip svarbiausią Lietuvos demokratijos pergalę.

„Negalima apsistoti ties vienu rodikliu, tarp mūsų regionų didelis skirtumas, sumažėjo gyventojų skaičius, didelis pajamų skirtumas“, — taip Krėpšta aprašo Lietuvos poziciją derybose su ES. Jo žodžiais, Vilniaus regione BVP vienam gyventojui siekia 112 proc. bendro europietiško lygio, o likusioje šalies dalyje — tik 85 proc. Šio skirtumo mažinimui gyvybiškai būtinas eurofondų finansavimas.

Su šia pozicija sutinka ir užsienio reikalų ministras Linkevičius. Lietuva ir jos broliai neva „baudžiami už sėkmingai pravestas struktūrines reformas ir pasiektą progresą, o biudžeto projektui, nors jis sudarytas atsižvelgiant į rimtus iššūkius, vis dėlto „trūksta sąžiningumo“.

Jei reformos įgyvendintos ir pasiekta sėkmės, pats metas mažinti dotacijas (kalba eina būtent apie mažinimą — Lietuva, kaip ir anksčiau, gaus didžiules sumas iš europietiško „bendrabučio“). Jei ne, tada Pabaltijo respubliką tuo labiau verta vyti nuo „lovio“. Nes beviltiška ją maitinti pinigais.

Neseniai apie Lietuvos klaidas, įveltas po Tarybų Sąjungos subyrėjimo, prabilo pats prezidentas Nausėda. Pasirodo, per daug stipri „nematoma rinkos ranka“ neatnešė šaliai laimės: ekonomika daugelį metų vystėsi „pagal Laukinių Vakarų principus ir jų sąlygomis“, judėjimą link europietiško BVP vidurkio rodiklio vienam gyventojui tebelydi smarki socialinė ir turtinė atskirtis. Tą patį Nausėda kalbės derybose dėl ES biudžeto.

Iš vienos pusės, ji ir toliau bando vaizduoti stiprų sėkmės „Baltijos tigrą“. Iš kitos — įrodinėja, kad be Europos pašalpų lietuviams bus gana striuka. Dėl pinigų tenka būti „truputį nėščia“.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```
