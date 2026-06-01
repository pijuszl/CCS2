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

### Article 1 — id: `scraped:rubaltic_lt:bf0a602d08189476`

**Title:** Lietuvos verslas pasisako prieš antirusišką Vilniaus politiką

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Oficialaus Vilniaus kova su „rusų grėsme“ iškelia privačiom kompanijom nemažai problemų. Lietuvos geležinkelininkų operatorius LGC Cargo apskundė Europos komisijai Lietuvos transporto saugumo administracijos (LTSA), „Lietuvos geležinkelių“ ir respublikos Transporto ir komunikacijų ministerijos veiksmus. Valstybė atsisako derinti maršrutus, kuriais LGC Cargo galėtų gabenti krovinius iki sienos su Kaliningrado sritimi.

Neišsprendžiama problema tapo tranzito Lietuvos teritorija iki sienos su Rusijos Federacija klausimas. Tuo užsiiminėti leidžiama tik valstybiniam geležinkelininkų operatoriui — privatininkai „vejami“ „valstybės saugumo“ sumetimais.

Jei tikėti LGC Cargo vadovu Sergejumi Gračiovu, kompanija suinteresuota vien tik pervežimais Pabaltijo teritorija. Tačiau praeitais metais Lietuvos transporto saugumo adminintracija klausimą užaštrino: iš vežėjo pareikalavo dokumentacijos, patvirtinančios, kad jis neketina užsiimti tranzitu. Šis atsisakė, todėl ir buvo „pavytas“.

„Mums skirti galingumai — į niekur, mes negalime nei atvežti, nei išvežti krovinio, — pažymi kompanijos vadovas Sergejus Gračiovas. — Jeigu šiandien Latvijoje atsiras krovinys, kurį reikia pargabenti į Lietuvą, mes nepajėgsime to padaryti“.

Verta priminti, kad nors LGC Cargo ir yra Lietuvos kompanija, bet pagrindinis jos akcininkas — Latvijos Baltic Transit Service, neva turintis ryšį su „Rusijos geležinkeliais“. Žurnalistų sukurta grandinė labai ilga ir mįslinga: Baltic Transit Service akcininkė yra Rigas Tirdzniecibas osta, kurią netiesiogiai kontroliuoja buvusio premjero Andriso Škele ir buvusio transporto ministro Ainarso Šleserso šeimos. O joms priklauso (vėlgi netiesiogiai) akcijos grupės Latvijas Transporta Grupa, investavusios į bendrus su „Rusijos geležinkeliais“ projektus.

„Lietuvos ir Latvijos geležinkelių sistemoje vis dar daug skirtumų, — tvirtina kompanijos logistikos menedžeris Tomas Keršis. — Latvija prieš daugelį metų liberalizavo ir restrukturizavo savo geležinkelių rinką. Lietuva atsilieka“.

Pašalinti dirbtinus apribojimus kompanijų vadovai ketina su Europos komisijos pagalba. Ne taip seniai Lietuva, pažeidusi konkurencijos sąlygas, jau nukentėjo, kai išardė Mažeikių – Renge geležinkelio atkarpą. Latvijos uostai dėl to prarado klientus, o Europos komisija Vilniui skyrė 28 milijonų eurų baudą.

Praeitais metais pasipriešino trąšų gamyklos Achema vadovai, atsisakę pasirašyti suskystintų gamtinių dujų (SGD) kontraktą su terminalu Klaipėdoje.

Generalinio direktoriaus Ramūno Miliausko žodžiais, Achema priversta mokėti per metus 20 milijonų eurų mokestį terminalo Independence išlaikymui: „Tai didina gamyklos produkcijos savikainą ir tokiu būdu mažina jos konkurencingumą ne tik vidaus, bet ir pasaulio rinkoje. Mūsų atlyginimų fondas beveik lygus mokesčiams, kuriuos moka kompanija už SGD terminalą. Sumažinus šį mokestį, mes galėtume dalį sutaupytų lėšų skirti darbo užmokesčiui ir reikalingoms investicijoms“.

Vyriausybė vis dėlto pasiūlė sumažinti Achemos indėlį į SGD terminalo išlaikymą, užtat pareikalavo pasirašyti ilgalaikius jos produkcijos tiekimo kontraktus. Kompanijos vadovybė priėjo išvadą, jog tai tas pats velnias.

„Kaip ilgalaikiai įsipareigojimai nebuvo galimi iš ministerijos atstovų pusės, taip ilgalaikiai įsipareigojimai negalimi ir iš mūsų pusės, — pažymėjo Achemos grupės valdybos pirmininkė Lidija Lubienė. Mes visada už energetinę nepriklausomybę, tačiau naštą būtina paskirstyti protingai, neužkraunant ant vienos įmonės pečių“.

Kalba, pavyzdžiui, apie Kauno merą Visvaldą Matijošaitį. Jis dar ir pagrindinis Vičiūnų įmonių grupės, turinčios Kaliningrado srities Sovetsko mieste žuvies perdirbimo gamyklą, akcininkas. Valdančiosios Lietuvos valstiečių ir „žaliųjų“ sąjungos lyderį Ramūną Karbauskį politiniai oponentai taip pat kaltina turint RF aktyvus.

„Lietuvos valstiečių ir „žaliųjų“ sąjungos lyderis Ramūnas Karbauskis ir Kauno meras Visvaldas Matijošaitis turi nedelsiant atsisakyti savo verslo Rusijoje, — 2018 metais reikalavo parlamento Nacionalinio saugumo ir gynybos pirmininko pavaduotoja Rasa Juknevičienė. — Tai susikerta su politiko statusu ir analize, kurią tiesiogiai ir netiesiogiai pateikia Lietuvos žvalgyba“.

Tad kokį verslą turi Rusijoje Karbauskis? Jo bendražygis ir Lietuvos premjeras Saulius Skvernelis tvirtina, kad jokio: tai tik gandai. Karbauskiui priklausantis Agrokoncernas pirko trąšų iš kompanijos „Kuibyševazot“, kurios direktorių tarybos pirmininkas yra partijos „Vieningoji Rusija“ narys Viktoras Gerasimenka, tačiau „valstiečių“ lyderis tame nemato jokios problemos.

„Šiuo atveju mes turime nuspręsti, jog nieko neimportuosime iš Rusijos, — sako Karbauskis. — Kiek aš žinau, kiek teko girdėti, daugiausia prekių importuojama iš Rusijos. Jei mes nuspręsim, kad ką nors importuoti iš Rusijos nereikia, tada tokiam sprendimui pritars visos kompanijos“.

Tokiu atveju už kažką priekaištauti Karbauskiui beprasmiška. Tą Agrokoncernas akcentavo tada, kai jis buvo pakartotinai apkaltintas pirkęs trąšų per tarpininką Dubajuje.

„Mes norėtume sužinoti, ar turi teisę valstybės valdininkas pasirinktinai išskirti vieną komercinę įmonę iš kitų ir su savo įtarimais kreiptis į teisėsaugos organus, o taip pat viešai platinti šią informaciją“, — pareiškė kompanijos vadovas Edgaras Šakys.

Lietuvos ekonomika kenčia nuo antirusiškų sankcijų. Oficialiam Vilniui to maža: prisidengdama nacionalinio saugumo rūpesčiu ir kova dėl „energetinės nepriklausomybės“, valstybė spaudžia privačias kompanijas. Tačiau jei su bendaeuropietiškomis sankcijomis jos susitaikė, tai toleruoti vietinės valdžios išsišokimus jos neketina.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 2 — id: `scraped:rubaltic_lt:7f30cbd7cc6bcdf1`

**Title:** Tarybinis tankas ir lietuvių mitas: „nusikaltimus“ Vilniuje vykdė Jurijus Melis

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Vilniaus apygardos teismas paskelbė nuosprendė dėl susidūrimų prie Vilniaus televizijos bokšto 1991 metų sausio 13 dieną. Pagrindinis kaltinamasis ant teisiamųjų suolo — Rusijos kariuomenės atsargos pulkininkas Jurijus Melis. Jis nuteistas kalėti septynerius metus. Buvo tikėtasi verdikto sulaukti vasario 18 dieną, tačiau neva dėl teisėjų kolegijos nario „ligos“ lietuvių Temidė proceso pabaigą nukėlė. Analitinis portalas RuBaltic.Ru nutarė priminti skaitytojams ir skandalingo proceso dalyviams, kas ne taip „sausio 13-osios byloje“.

Apie 1991 metų sausio 13-osios Lietuvoje tragiškų įvykių istoriją nemažai parašyta. Prieš kruviną atomazgą prie Vilniaus televizijos bokšto, kurios nekantriai laukė Lietuvos politikos „patriarchas“ Vytautas Landsbergis, įsiplieskė konfliktas tarp sąjunginio centro ir nepriklausomybės atkūrimą paskelbusios Pabaltijo respublikos.

Tarybų Sąjungos prezidentas Michailas Gorbačiovas pasipiktino LTSR Aukščiausiosios Tarybos veiksmais ir pabandė spustelti Lietuvą ekonomine blokada. Po to, kai ji buvo atšaukta, vyko beviltiškos derybos ir tragiškas bandymas karinėmis pasjėgomis įvesti Vilniuje tvarką.

Tarybinio tanko įvaizdis liguistu Lietuvos požiūriu į sausio 13-osios įvykius tapo vienu iš pagrindinių. Daug tonų sveriančių tonų vikšrai traiškė vargšus praeivius — tokį įvaizdį jau kitą dieną po masiškų žudynių piešė žiniasklaida. Tiesa, tankų užvažiavimų kadrų keistu būdu neišliko (tik surežisuotos nuotraukos), o ant aukų kūnų vikšrai paliko tik įdrėskimus...

„Odos įdrėskimai pagal formas primena keturkampius“, — taip ir parašė akte teismo medicinos ekspertas apie Loretos Asanavičiūtės mirties priežastis. Ir tai po to, kai merginą neva pervažiavo 58 cm pločio tanko vikšras! Kokių tik stebuklų nebūna, kai nesvarbu kaip būtina apkaltinti “okupantus”.

Bet kokiu atveju Vilnius turi pretenzijų tarybiniams tankistams. Ir buvo galima tikėtis, jog 2014 metų kovą sulaikytas Jurijus Melis bus apkaltintas ne žudant taikius gyventojus, tai bent jau bandymu juos pervažiuoti.

O kas iš tikrųjų? “544 numerio Jurijaus Melio tankas, taikytojas D.Bolšakovas, mechanikas — vairuotojas S.Dragocenyj (jam baudžiamoji byla už nusikaltimus žmoniškumui ir karinius nusikaltimus neiškelta), sulaužė televizijos bokšto vakarų pusės teritorijoje esančią tvorą, pavojingai manevruodamas, įvažiavo į teritoriją, kur ne mažiau trijų kartų tuščiais iššovė į orą, paleido dūmų uždangą, karinės technikos šviesos prietaisais švietė į civilius žmones, užimamą objektą ir aplinkinius pastatus, tokiu būdu gąsdindamas ir terorizuodamas civilius žmones”.

Nieko neužmušė ir nesužalojo.

Būtų logiška visa tai išgirsti iš teisiamojo asmens advokatų arba iš jį teisinančių “Kremliaus propagandistų”, tačiau minėtą citatą mes aptinkame Vilniaus miesto apylinkės teismo nutartyje pripažinti Jurijų Melį įtariamuoju.

Na, žinoma, už sulaužytą tvorą iš tanko ekipažo vado tikrai galima pareikalauti kompensacijos. Ir už stiklus Vilniaus televizijos bokšto langų rėmuose, jeigu jie būtų išbyrėję nuo šūvių tuščiomis. Tačiau to turbūt neįvyko, nes apygardos teismas tikrai nebūtų praleidęs galimybės priminti apie siautėjimą garso bangų, kurias sukėlė “agresoriai”.

Už tris šūvius tuščiomis — kaltinimai nusikaltimais žmoniškumui ir reikalavimas įkalinti iki gyvos galvos. Tokią formulę išrado Lietuvos “teisėtvarka”. Tai jau, neabejotinai, naujas teisės mokslų žodis!

Lietuvos nepriklausomybės gynėjų manymu, Melio kaltę apsunkina dar viena aplinkybė — jis “puolė” ne kažkokią abstrakčią žmoniją, o suverenią šalį.

Generalinės prokuratūros pozicija tame, jog Lietuva 1991 metų sausyje jau buvo išstojusi iš TSRS. Taigi tarybiniai kariškiai bandė pažeisti jos teritorijos vientisumą, nuversti konstitucinę santvarką ir taip toliau. Ar galėjo Melis jausti, kad visa tai daro? Vargu. Kaip ir viso pasaulio bendrija.

Tad kokią konstitucinę santvarką bandė nuversti Jurijus Melis?

Net jeigu patikėti, jog Lietuva sausio 13 dieną jau buvo nepriklausoma, jos teritorijoje vis tiek galiojo Lietuvos TSR Baudžiamasis kodeksas — kito nebuvo. Pagal jį ir reikėtų teisti tragedijos kaltininkus, tačiau Jurijui Meliui buvo taikomas kodeksas, priimtas po minėtų įvykių praėjus daugeliui metų.

Ir čia teisiamąjį gina Europos žmogaus teisių ir pagrindinių laisvių gynimo 1950 metų lapkričio 4 dienos konvencijos 7 straipsnis. Jis skelbia, “kad niekas negali būti nuteistas už kokį nors atliktą ar neatliktą veiksmą, kuris tuo momentu, kai buvo atliktas, pagal nacionalinę arba tarptautinę teisę nebuvo laikomas baudžiamuoju nusikaltimu”.

Taip kad ir tarybinė įstatymų leidyba, ir tarptautinė teisė — Jurijaus Melio pusėje. Įstatymas atgaline data negalioja — elementari kiekvienam teisės fakulteto pirmojo kurso studentui žinoma aksioma. Tiktai Lietuvai ji kažkodėl neparašyta.

Tiesa, minėtame 7 straipsnyje yra svarbus papildymas: “Šis straipsnis netrukdo teisti ir bausti bet kokį asmenį už įvykdymą ar neįvykdymą kokio nors veiksmo, kuris jo atlikimo metu buvo baudžiamasis nusikaltimas pagal bendrus teisės principus, kuriuos pripažino civilizuotos šalys”.

Pati formuluotė (“bendri teisės principai, kuriuos pripažino civilizuotos šalys”) skamba labai nekonkrečiai. Tačiau mes jau išsiaiškinom, jog “civilizuotos šalys” 1991 metų sausyje nebuvo suabejojusios TSRS teritoriniu vientisumu. O jeigu pažvelgti į Melio kaltinimus be ideologinės potekstės, tai byla subliuška kaip tas kortų namelis.

Melį remia dar vienas tarptautinis dokumentas. Pažvelkime į 1998 metų liepos 17 dienos Tarptautinio baudžiamųjų bylų teismo Romos statuto 33 straipsnį. Jame išvardinti atvejai, kuriuose asmuo, nusikaltęs vykdydamas vadovybės įsakymą, atleidžiamas nuo atsakomybės:

a) tas asmuo juridiškai privalėjo įvykdyti šios vyriausybės arba viršininko įsakymus;

b) tas asmuo nežinojo, kad įsakymas neteisėtas;

c) įsakymas buvo akivaizdžiai neteisėtas.

“Atsižvelgiant į įvykio aplinkybes ir tas visiškai neaiškias politines sąlygas, niekaip negalima teigti apie kariškių suvokimą, jog gautas įsakymas buvo visiškai neteisėtas”, — konstatuoja Europos juridinės tarnybos Maskvoje juristas Andrejus Tokarevas.

Pastaba apie politinių sąlygų neaiškumą labai teisinga. “Visame pasaulyje tokiu atveju skelbiama amnestija, kaip skelbė Rusija po 1993 metų įvykių ir karo Čečėnijoje, kaip TSRS skelbė 1955 metais vokiečiams tarnavusiems kolaborantams, kaip po maidano buvo paskelbta Ukrainoje (tiesa, užsibaigė liustravimu), — rašo juristas Aleksejus Jelajevas. — Nereikia remti pilietinių karų, maža kas kuo buvo permainų metu”.

Lietuvos nacionalistai paprieštaraus — ne, ne maža! Jei tu “agresorius’, tai atsakyk pagal įstatymą. Arba ne pagal įstatymą, tačiau vis tiek atsakyk.

Jis buvo tardytojų kviečiamas, Landsbergis net piktinosi, kodėl ant teisiamųjų suolo nėra buvusio TSRS prezidento. Tačiau atsakymas visiems žinomas. Michailas Sergejevičius — visos “progresyvios žmonijos” numylėtinis. Argi galima jį teisti?

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 3 — id: `scraped:rubaltic_lt:95e211db8a0e169d`

**Title:** Lukašenkos dovana: Latvija pervilioja iš Lietuvos baltarusijos tranzitą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Klaipėdos uostas palaipsniui praranda baltarusių tranzitą. Apie tai pareiškė „Latvijos geležinkelių“ valdybos pirmininkas Edvin Berzinš. Jo žodžiais, krovinių siuntėjai vis dažniau renkasi Latvijos uostų paslaugas. Lietuva, Baltarusijos prezidento Aleksandro Lukašenkos perspėjimus dėl tranzito perorientavimo į Latviją nepalaikiusi rimtais, pralaimi uostų su Pabaltijo kaimyne kovą.

Baltarusijos krovinių tranzito per Latvijos uostus apimtys pernai ūgtelėjo 10 proc., — teigia Edvin Berzinš. Į jo pateiktus skaičius verta žvelgti atsargiai. „Latvijos geležinkelių“ viršininkas vis dėlto labai suinteresuotas pagražinti savo šalies uostų pasiekimus. Ar neįsivėlė į jo statistiką gudrus manipuliavimas?

Kad būtų aiškiau, būtina atkreipti dėmesį į kitus skaičius. Pirmiausia, Baltarusija 2018 metais padidino prekių eksportą 15,3 proc. ir ėmėsi rimtų žingsnių diversifikuojant realizavimo rinką. To išdavoje EAES šalių dalis bendrame baltarusių eksporto sraute krito nuo 46,7 iki 41,2 proc., o ES dalis pakilo nuo 26,8 iki 30,2 proc. Manoma, jog tai ir įtakojo baltarusių tranzito per Latviją padidėjimą.

O kuo dėta Lietuva? Klausimas tampa vis labiau aktualus, jei atsižvelgti į tai, jog Klaipėdos uosto krovinių apyvarta 2018 metais išaugo 7,3 proc.

Po Baltarusijos prezidento Aleksandro Lukašenkos žodžių, jog reikia „daugiau remtis Latvija“, to reikėjo laukti.

„Jei kalbėti apie tokius krovinius, kaip trąšos ir naftos produktai, tai mes negalime ignoruoti galimybių, jog bus priimti sprendimai ir duoti nurodymai įmonėms keisti pakrovimo ir eksporto uostus. To nevertėtų atmesti“, — taip Lukašenkos pareiškimą komentavo Klaipėdos konteinerių terminalo direktorius Vaidotas Šileika.

Kai buvo pareikalauta, kad Lietuvos transporto ir komunikacijų ministras Rokas Masiulis atsakytų, kodėl vyriausybė visiškai nereaguoja į Latvijos pastangas pervilioti iš Klaipėdos dalį baltarusių krovinių, jis ragino kolegas nesinervinti. Ko nervintis, jei Lietuva, žvelgiant iš logistikos pozicijų, siūlo geriausias sąlygas? Minskas, kaip žinia, iš dviejų ir daugiau komercinių pasiūlymų visada pasirenka naudingiausią, o ne politiškai tikslingą.

Visa tai vaizdžiai demonstruoja pavyzdys Rusijos uostų, kurie, RF prezidento paraginti, tuoj pat bandė persivilioti baltarusių tranzitą. 2017 metų rugpjūčio mėnesį Vladimiras Putinas tiesiogiai pareiškė, jog geriau būtų iš rusiškų žaliavų baltarusių gaminamus naftos produktus eksportuoti per Rusijos uostus. Pasakyta – padaryta: lapkrityje koncernas „Belneftechim“ pasirašė kontraktą dėl savo produkcijos perkrovimo per RF uostus.

Tačiau baltarusių naftos tranzito perorientavimo į Ust-Lugos uostą procesas užstrigo. Iki šios dienos pagrindinis baltarusių naftos tranzito srautas vis dar nukreiptas į Pabaltijo uostus.

Liepojos uostas nuo Klaipėdos visai netoli (tiesiai atstumas mažiau 100 kilometrų). Kompensuoti transporto praradimus baltarusių naftos produktų tranzito perorientavimo į Liepoją atveju galima susisiekimo geležinkeliu tarifų mažinimo sąskaita.

Ir į ką tada orientuosis Minskas: į Lietuvą, kuri visokeriopai bando stabdyti Baltarusijos atominės elektrinės (BalAE) statybą, ar į Latviją, kuri neprieštarauja šio projekto realizavimui?

Lietuvos valdžios neabejoja, jog latvių nuolaidumas — tai bandymas išsiderėti naujas baltarusių tranzito apimtis, kurias Lukašenka gali permesti iš Klaipėdos krypties.

Iš Latvijos jis laukia naudingų komercinių pasiūlymų, o ne palakymo tarptautinėje arenoje. Už palaikymą priklauso tik kukli dovana, apie kurią džiaugsmingai praneša „Latvijos geležinkelių“ valdybos pirmininkas.

Baltarusijos krovinių tranzito augimas 10 proc., kai jos eksportas per metus ūgtelėjo 15 proc., — lašas jūroje. Kiek dar „lašų“ sulauks Latvija? Viskas priklauso nuo to, kokias sąlygas ji pasiruošusi pasiūlyti.

Prie Leningrado srityje esančių uostų netrukus prisidės daugiaprofilinis giliavandenis uosto kompleksas Vyborgo rajone su krovinių apyvarta iki 70 milijonų tonų per metus. Vietos valdžia neslepia, kad jo pagrindinis tikslas – „sužlugdyti“ Pabaltijo uostus.

„Leningrado sričiai tai svarus projektas, naujas augimo taškas, kuris suteiks galimybes ne tik vystyti prie uosto esančias teritorijas, bet ir perorientuoti rusų eksporto krovinius iš Pabaltijo regiono užsienio uostų“, — pareiškė Leningrado srities gubernatorius Aleksandras Drozdenka.

Taip pat neverta ignoruoti baltarusių tranzito perorientavimo į Rusijos uostus galimybės. Čia pagrindinis klausimas geležinkelio tarifai, kuriuos „Rusijos geležinkeliai“ pastaraisiais metais baltarusių naftos reideriams mažino du kartus.

Kaip bebūtų, baltarusių tranzito diversifikavimai lieka grynai ekonominiu klausimu. Uostus krovinių perkrovimui Lukašenka renkasi remdamasis kruopščiais apskaičiavimais.

Lietuvos valdžioms tai naudinga, todėl jos ir pliauškia vis tą patį: Minskui nenaudinga atsisakyti Klaipėdos. Ir nereikia, teigia, painioti griekų su dora! BalAE — sau, tranzitas — sau.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 4 — id: `scraped:rubaltic_lt:09ebc1492d9a70b3`

**Title:** Grupės „Alfa“ vadas: prie Vilniaus televizijos bokšto išduoti buvome mes ir lietuviai

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Analitinis portalas RuBaltic.Ru pravedė Kaliningrade kovo 18 dieną viešuosius svarstymus dėl Jurijaus Melio, kuriam kurpiamas nuosprendis “sausio 13-osios byloje”, likimo. Svarstymų metu pasisakė Vilniaus televizijos bokšto šturmo 1991 metų sausio 13 dieną dalyvis, grupės “Alfa” vadas, TSRS VSK dimisijos pulkininkas Michailas Golovatovas. Interviu RuBaltic.Ru Golovatovas papasakojo, kas Vilniuje vyko sausio 13-osios naktį, kas į ką šaudė ir kas ką išdavė.

— Pone Golovatovai, ar Jūs niekada naktimis nesapnuojate 1991 metų sausio 13-osios įvykių?

— Esmė tame, kad jeigu prisiminti visas operacijas, kuriose aš dalyvavau savo gyvenime, tai sapnuoti turėčiau viską, ką mačiau ir kur buvau. Bet jei kalbėti apie Lietuvą, tai ji įsiminė todėl, kad tiek išdavysčių aš daugiau niekur nemačiau.

Ypač prisimenant išdavikišką šalies vadovybės poziciją.

— Jūs turite omeny Michailą Gorbačiovą?

— Ne tik Gorbačiovą. Aš pamenu, kaip sužinojau, kad vykstu į Lietuvą. Tai buvo šeštadienį, 1991 metų sausio 6 dieną. Kitą dieną aš traukiniu išvykau į Vilnių kartu su dar dviem darbuotojais. Atvykęs ten ir išklausęs Valdybos viršininko Maskvai instruktažą, išvykau ruošti visas priemones, kad po kelių dienų (ne vėliau 3–4) galėtų atvykti pagrindinė grupė.

Tačiau kai kam (galiu pasakyti, kam) reikėjo tempti laiką. Ir 11, ir 12 sausio nieko nevyko. Naktį iš 12 į 13 mes apsiribojome televizijos centro ir bokšto išlaisvinimu, kad nebūtų laidų, diskredituojančių TSRS. Prezidentinio valdymo įvedimo užduotys tuo metu jau “susigėrė smėlyje”.

— Kalbėdamas apie išdavystę, Jūs turite omenyje tą vadovybę Maskvoje, kuri neprisipažino įsakiusi įvesti į Vilnių kariuomenę ir užimti strateginius objektus?

— Sakykime, man aukščiausias vadovas buvo VSK pirmininkas, 7 Valdybos viršininkas generolas leitenantas (Jevgenijus) Rasščepovas, kuriems aš atsiskaitydavau Maskvoje. Ir, savaime, tas štabas, kuris buvo sukurtas Vilniuje ir Šiaurės miestelyje. Iš ten gaudavome informaciją apie mūsų pajėgų panaudojimą.

Svarbiausia, aš supratau, kad štabo priimami nutarimai buvo perduodami Maskvai. Ir aš jau pradėjau suvokti: tai, ką mes perduodavom Maskvai, po valandos kitos buvo žinoma Lietuvos Aukščiausioje Taryboje.

Ir niekas iki šiol nenori aiškintis, kad tada buvo paskelbta komendanto valanda. Kokiu būdu Lietuvos piliečiai, Vilniaus gyventojai galėjo atsidurti prie televizijos centro ir bokšto komendanto valandos, kuri galiojo nuo vidurnakčio iki 6 valandos ryto, metu?

Tą komendanto valandą paskelbė Vilniaus komendantas, Vilniaus divizijos vadas. Tačiau ten buvo organizuotas maisto produktų pristatymas, buvo atvežami žmonės, ir svarbiausia — jie jau buvo suskirstyti kovinėmis grupėmis su vadovais, jos sudarė televizijos bokšto skydą.

Jei prie televizijos bokšto buvo nuo 6 iki 8 tūkstančių žmonių, tai prie centro mažiau — nuo 3 iki 5 tūkstančių.Jie stovėjo glaustu žiedu, ir, norint įeiti, minią reikėjo perkirsti taip, kad nebūtų sukelta spūstis ir niekas netraumuotas.

Tankai pasitraukė, iš kiekvienos pusės privažiavo po dvi ŠPM (БМП) su ekipažais ir desantu. Desantas pabandė pramušti mums koridorių, tačiau to padaryti nepavyko. Tada mes apėjome bokštą ir patekome prie jo užnugario. Čia žmonių buvo mažiau, ir visas protestuojančiųjų dėmesys buvo nukreiptas į tą įėjimą, prie kurio dislokavosi ŠPM, o iki tol – tankai.

Tai suteikė mums galimybę, panaudojant šviesos garsines granatas, pramušti sau koridorių ir patekti į televizijos bokštą. Ten taip pat mums buvo pasipriešinta, panaudojant inertines, gaisrų gesinimui naudojamas dujas. Mes turėjome dujokaukes, jos mus išgelbėjo.

Mes turėjome išvesti iš rikiuotės retransliuotojus, kurie perdavinėjo laidas Pabaltijui. Jeigu juos sugadinti Vilniuje, laidų nebus nei Rygoje, nei Taline. Jų sutaisymui reikėtų iki trijų mėnesių.

Mes nuginklavome besipriešinusius grobikus, nes turėjome vedlius, kurie parodė, kur eiti ir kur yra skydinės (31 ir 32 aukštuose). Liftai neveikė. Buvo paskirti karininkai, kurie nedelsiant ten pateko ir neleido atjungti skydinių.

— Ar Jūs pats matėte tuos snaiperių šūvius nuo stogų, apie kuriuos kalba liudytojai?

— Aš ne tik juos mačiau. Tuo vadovaudamasis iškviečiau šarvuotą techniką, kad mes galėtume išeiti.

— Tai yra šaudoma buvo į jus, “Alfos” karius?

— Šaudoma buvo ir į aplink susibūrusią minią, ir į konvojaus kariuomenės karius, kurie taip pat stovėjo žiedu aplink televizijos bokštą, ir į desantininkus. Kariškiai slėpėsi už kovinės technikos. Tai yra buvo šaudoma ir į kovinę techniką. Atitinkamai, nuo šių šūvių pradėjo žūti žmonės. Savi šaudė į savus.

— Ir tai buvo dviguba išdavystė? Ta pusė taip pat išdavė tuos, kurie ją rėmė?

— Taip. Ir apie ketvirtą — pusę penkių ryto mes trimis ŠTR (БТР) išvykome į Šiaurės miestelį, palikę desantininkus ir konvojų saugoti televizijos bokštą ir centrą — du išlaisvintus objektus.

Aš turėjau apie 60 žmonių, juos teko suskirstyti į dvi grupes. Apie trečią valandą nakties gavome pranešimą: „vienas su minusu“. Taip buvo pranešta, kad žuvo Viktoras Šatskich.

Ir mes 40 minučių nepajėgėme jo išvežti į medicinos įstaigą; per tą laiką susirietė plaučiai. Jis mirė nuo kraujo išsiliejimo į plautį.

— Aš įdėmiai skaitau Lietuvos spaudą, jie iki šiol tvirtina, kad Šatskich pašovė saviškiai. Tai buvo „draugiška ugnis“. Taip jie išsireiškia.

— Draugiška ugnis, taip? Jeigu Šatskich ėjo priešpaskutinis, tai mes negalime sakyti, kad į jį šovė saviškis. Aš žinau, kas ėjo paskui jį. Kai Šatskich pasiekė antrą aukštą, jis kreipėsi į šį kariškį: „Mane kažkaip degina“. Tvirtinti, kad šis kariškis turėjo kovinį šovinį? Nesąmonė.

Kai kompensatorius užvyniotas, šaudant koviniais šoviniais, jis plyštų.

— Ir tai dar vienas lietuviško melo pavyzdys, kurio įkaitu tapo Jurijus Melis.

— Jurijus Melis triskart iššovė, kai patrankos vamzdis buvo pakeltas nuo žemės 75 laipsnių kampu.

Net tie decibelai, kuriuos sukėlė šaudymas tuščiomis, negalėjo pažeisti žmogaus klausos organų, nes viskas nuskriejo į viršų. Pastatuose, esančiuose arčiau 100 metrų, net stiklai neišlėkė.

— Visa tai piešia fantastiško melo vaizdą.

— Taip. Prisiminkime, kad net Landsbergis sakė, kad televizijos bokšto išlaisvinimo metu nei ant pastato sienų, nei jo viduje grupės kariškiai nepaliko jokių kulkų pėdsakų. Taip buvo konstatuota, kad šaudėme ne mes.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 5 — id: `scraped:rubaltic_lt:6de0a82172668aea`

**Title:** Grybauskaitė vs Skvernelis: įdomiausi žodinio apsišaudymo epizodai

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Kritikuodama premjerą Saulių Skvernelį, prezidentė Dalia Grybauskaitė nesivaržo išsireiškimuose. Jis „smūgius“ priima oriai, bet nepamiršta įžūliai atsakyti. Analitinis portalas RuBaltic.Ru siūlo skaitytojams prisiminti įdomesnius šio žodinio apsišaudymo epizodus.

Moterų diskriminavimas

Šių metų sausio mėnesį Dalia Grybauskaitė apgailestavo, kad moterims Lietuvoje neleidžiama aktyviai dalyvauti priimant politinius sprendimus. Tai, kaip žinia, pasaulinė tendencija: 2018 metais moterų skaičius vadovaujančiuose svarbiausių pasaulio kompanijų postuose sumažėjo 15 proc. Tačiau Grybauskaitė tikina, kad šiuo klausimu Lietuva atsilieka nuo kitų Europos Sąjungos šalių.

Į tai atkreipė dėmesį ir Grybauskaitės patarėjas Dovydas Špokauskas.

Ir tikrai, kai Skvernelis ministrų portfelius atėmė iš Jurgitos Petrauskienės ir Lianos Ruokytės–Jonson, vyriausybėje liko vieni vyrai. Grybauskaitė, kaip „kovotoja“ už moterų teises, tiesiog negalėjo su tuo susitaikyti.

Konstitucijos pažeidimas

Praeitais metais tarp Skvernelio ir Grybauskaitės įsiplieskė nedidelis karas dėl teisingumo ministro posto. Kandidatūrą teikia premjeras, o tvirtina prezidentė. Tačiau patvirtinti Skvernelio teiktą advokatą Giedrių Danielių Grybauskaitė atsisakė. Jos argumentai vyriausybės vadovo netenkino.

„Jeigu kas nors mano, kad diktatas arba Konstitucijos numatytų įgaliojimų viršijimas — normalus reiškinys, tai aš nelaikau, jog tai yra normalu“, — aiškią užuominą metė Skvernelis.

Kiek anksčiau Grybauskaitė pateikė premjerui tokias pat pretenzijas, kai šis atsisakė atleisti skandalingai pagarsėjusį žemės ūkio ministrą Bronių Markauską. Oponentai nekaltino jo nesąžiningu ūkininkavimu, kai tuo metu pagal įstatymą Markauskui visiškai buvo uždrausta užsiiminėti papildomais darbais. „Tuo pačiu ir premjerui tenka atsakomybė už galimą Konstitucijos pažeidimą“, — pasakė Grybauskaitė.

Argumentas taip pat silpnokas. Taip apsikeista vienodai nevykusiais smūgiais.

Žemas politinės kultūros lygis

Dar būdamas Lietuvos vidaus reikalų ministru Skvernelis įsivėlė į visiškai kvailą situaciją. O buvo taip: antrankiais sukaustytas pažeistos psichikos dvidešimt vienerių metų Lietuvos pilietis buvo vežamas į ligoninę. Kažkokiu būdu jam pavyko atimti iš policininko automatą ir pabėgti — jo ieškoti puolė visas miestas.

Viena iš tų, kurie negailėjo Skverneliui kritikos, buvo Grybauskaitė. Ją papiktino informacija, jog bėglio sulaikymo operacija vidaus reikalų ministras nesidomėjo. Jeigu tikėti Seimo pirmininkės Loretos Graužinienės žodžiais, jis tuo metu miegojo. Tačiau Skvernelio versija kita: pokalbis su Grybauskaite buvo „neadekvatus“, todėl jį teko nutraukti. Bet kokiu atveju, prezidentės nuomone, ministras pasielgė nevykusiai.

„Turiu apgailestaudama pastebėti, kad Skvernelis ne pirmą kartą demonstruoja žemą politinės kultūros lygį, bandydamas komentuoti arba nesuvokdamas savo atsakomybės lygio, — pažymėjo Grybauskaitė. — Vidaus reikalų ministras privalo laiku ir išsamiai informuoti apie įvykius visus šalies vadovus“.

Pavojingas populistas

Elektroninis Grybauskaitės ir korupcija įtariamo buvusio liberalų lyderio Eligijaus Masiulio susirašinėjimas — atskira tema. Jos paviešinimas stipriai pakenkė ponios Dalios reputacijai (elitas sušneko apie apkaltos galimybę).

Viename laiške Grybauskaitė užsiminė apie žmogų, kuris artimiausiu metu taps jos pagrindiniu politiniu oponentu.

Buvęs VRM vadovas tada pareiškė, jog atsakydamas nesiruošia kritikuoti prezidentės, nes jis kitaip supranta moralę ir etiką. Tačiau ir jis, kaip rodo praktika, žodžių kišenėje neieško.

Buldozeris prieš „nupieštą fasadą“

Eilinis žodinis Drybauskaitės ir Skvernelio apsišaudymas įsiplieskė ant mokytojų streiko bangos praeitų metų lapkričio-gruodžio mėnesiais. Šalies prezidentė negailėjo epitetų. Jos manymu, antrieji vyriausybės darbo metai buvo skirti „jėgos demonstravimui“, o valdančiosios partijos „arogantiškas visko žinojimas“ privedė prie chaoso daugelyje sferų. Ministrų kabinetą ji palygino su buldozeriu.

Skvernelis atsakė taip pat kandžiai: „ Mes matome nupieštą fasadą, o tikrą vaizdą, manau, daugelis politikų, kaip aš ir Butkevičius, galėtų nupiešti“. Be to, šį kartą premjeras vis dėlto „smogė“ Grybauskaitei, primindamas jos susirašinėjimą su Masiuliu.

Tačiau skaudžiausia tada buvo smogta ne Grybauskaitei, o jos draugams iš Tėvynės Sąjungos — Lietuvos krikščionių demokratų partijos.

Daugiau žalos, negu naudos

Neseniai vizito į Izraelį metu Skvernelis vėl tūpė į balą. Jeigu iki šiol Lietuvos politikai tradiciškai lankė Palestinos autonomiją, tai dabartinis premjeras to nepadarė demonstratyviai. „Tai pažeidžia įprastą ES praktiką, tai pažeidžia tarptautinę teisę ir siunčia palestiniečiams labai blogą signalą“, — situaciją komentavo Palestinos užsienio reikalų ministras Amal Džadu.

Ir Grybauskaitė nutarė šliūkštelti į ugnį žibalo, pareikšdama, kad Skvernelio vizitas „davė daugiau žalos, negu naudos“.

Priešrinkiminis skandinimas

Pristatydamas savo rinkimų štabą ir rinkimų programą, Skvernelis kelis kartus kritikavo prezidentės politiką. Pavyzdžiui, apgailestavo, kad ji jam trukdė priimti socialiai orientuotą biudžetą ir, gali būti, vėl bandė pažeisti Konstituciją. „Aš niekada nesusitaikysiu su biudžetu, kuris galimai bus antikonstitucinis, kuris užprogramuotai menkins socialinę piliečių gerovę — mažins pensijas, atlyginimus ar svarbias socialines išmokas“.

Tačiau skaudžiausias Skvernelio pasisakymo smūgis — priminimas, jog Lietuvos prezidentė negali pasiekti dvišalio bendradarbiavimo su JAV formato.

Pasaulinio masto gėda

Įžeista Grybauskaitė suskubo atsakyti. Neseniai Skvernelio paskelbtame „plane-chuligane“ Baltarusijos AE atžvilgiu ji aptiko ... Konstitucijos pažeidimą. „Konstitucija numato, kad sprendimus priima tik prezidentas, užsienio politika vykdoma kartu su vyriausybe. Taip kad, kadangi ši tema nebuvo derinama, o tai strateginis užsienio politikos tikslas, manau, susidūrėme su antikonstituciniu veiksmu“.

Dar griežčiau Grybauskaitė pasisakė po to, kai Skvernelis atmetė draugystę su latviais.

Skvernelis atsakydamas kol kas tik teisinasi. Šią žodinės kovos dalį jis akivaizdžiai pralaimėjo.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 6 — id: `scraped:rubaltic_lt:caf19802961c0edb`

**Title:** Priešais Lietuvos konsulatą Kaliningrade priimtas Melį palaikančios rezoliucijos projektas

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Kaliningrade viešųjų svarstymų, palaikant Lietuvoje areštuotą Jurijų Melį, metu jų dalyviai pareikalavo iš Pabaltijo respublikos panaikinti Rusijos kariškio kaltinimus ir nutraukti kitų 1991 metų sausio 13-osios bylos figūrantų persekiojimą. Galutinis dokumentas bus išsiųstas Rusijos URM, Valstybės Dūmai, Europos sąjungos vadovybei ir tarptautinėms organizacijoms.

Viešųjų svarstymų, kuriuos organizavo Baltijos I.Kanto federalinis universitetas ir portalas RuBaltic.Ru, metu, palaikant Jurijų Melį, universiteto pastate priešais Lietuvos konsulatą Kaliningrade, buvo pateikti 1991 metų sausio 13-osios bylos dėl susidūrimų prie Vilniaus televizijos bokšto faktai ir ekspertų išvados. Valdžios organų ir vietos savivaldybės, akademinės bendrijos ir verslininkų sluoksnių atstovai, juristai, visuomeniniai aktyvistai, studentai ir kursantai dalyvavo paruošiant galutinį rezoliucijos projektą.

Svarstymų metu priimtas rezoliucijos projektas bus išsiųstas Rusijos URM, Valstybės Dūmai, vadovaujantiems Europos sąjungos ir tarptautinių organizacijų JT, OBSE, PASE organams.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 7 — id: `scraped:rubaltic_lt:f831d4901343abef`

**Title:** Kreivas Europos teisingumas: kovą su „miško broliais“ EŽTT pavadino genocidu

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Europos žmogaus teisių teismas (EŽTT) užėmė poziciją Lietuvos, kuri sulygino tarybų valdžios kovą su „miško broliais“ su genocidu. Apie tai sakoma nutartyje, paskelbtoje organizacijos portale. Susipažinus su nutartimi neišvengiamai kyla klausimas: kodėl sprendžiant panašią bylą 2015 metais teismas priėmė visiškai priešingą nutarimą?

Penkiais balsais prieš du EŽTT atmetė skundą buvusio VSK (КГБ) darbuotojo Stanislovo Drelingo, kuris Lietuvoje buvo pripažintas genocido kaltininku dėl dalyvavimo sulaikant lietuvių partizanų vadą Adolfą Ramanauską–Vanagą ir jo žmoną.

Stanislovas Drelingas dalyvavo slaptoje operacijoje sulaikant Ramanauską ir jo žmoną Birutę Mažeikaitę. Abiejų likimai susiklostė nepavydėtinai: Vanagas buvo nubaustas mirties bausme, o Mažeikaitė aštuonerius metus praleido lageriuose. Už tai 2014 metais Drelingas buvo apkaltintas genocidu.

Kai Kauno apygardos teismas pripažino jį kaltu, o Aukščiausiasis teismas skyrė bausmę, nuteistojo advokatai bandė apskųsti šį nutarimą EŽTT.

Vienas iš Drelingo gynybos argumentų — Lietuvos teismas pažeidė Europos žmogaus teisių konvencijos 7 straipsnį. Jis teigia, jog negalima skirti bausmės „už įvykdymą kokios nors veikos arba už neveiklumą, kuris jo įvykdymo metu pagal nacionalinę arba tarptautinę teisę nebuvo traktuojamas kaip nusikaltimas“.

Beje, teismas nusprendė, jog „miško brolių“ sulaikymo metu nuteistasis turėjo rimtai susimąstyti apie savo veiksmus.

„Pareiškėjas 1950 metais turėjo žinoti, kad jis gali būti apkaltintas genocidu, ir jo pasmerkimą buvo galima numatyti. Todėl jokių Konvencijos pažeidimų nebuvo“, — sakoma dokumente.

Lai bus taip, tačiau gynyba atsargoje turėjo rimtesnį argumentą: ne taip seniai Vilnius jau pralaimėjo panašią bylą.

Tada spauda rašė, jog EŽTT sudavė Lietuvos istorinei politikai triuškinantį smūgį. Dabar skaitome visiškai priešingus pavadinimus: Strasbūras pripažino lietuvių tautos genocidą. Kodėl dviejuose analoginiuose atvejuose teismas priima visiškai skirtingus nutarimus?

Kipšas, kaip žinia, slypi smulkmenose. Šiuo atveju pagrindinė smulkmena — tikslus „genocido“ termino apibrėžimas.

JT Konvencijoje, kalbant apie kelio genocido nusikaltimui užkirtimą ir bausmę už jį, šis žodis aiškinamas kaip „veiksmas, siekiant visiškai arba dalinai sunaikinti kokią nors nacionalinę, etninę, rasinę arba religinę grupę“. Lietuvos valdžios 1998 metais prie išvardintų grupių pridėjo dar dvi — socialinę ir politinę.

Bėgant laikui, ši norma, prieštaraujanti įstatymų leidybai ir Baudžiamajam kodeksui, buvo pašalinta, tačiau Vasiliausko byloje Lietuva dar bandė žaisti apibrėžimais, įvardindama partizanus „politine grupe“.

Tame ir buvo pagrindinė klaida.

Beje, tuo bandė vadovautis ir Drelingo gynyba. Remdamiesi Vasiliausko atveju, advokatai tvirtino, jog partizaninis judėjimas — politinės grupės veikla. Ir todėl kovą su „miško broliais“ negalima traktuoti kaip genocidą.

Tačiau Lietuvos atstovai šį kartą vadovavosi Strasbūro rekomendacijomis: norint išsaugoti Drelingui skirtą nuosprendį, paprasčiausiai reikia įtikinti teismą , kad „Lietuvos partizanai atstovavo lietuvių tautai“.

Ir su šia užduotimi atsakovas susidorijo. Jei tikėti EŽTT nuosprendžiu, respublikos Aukščiausiasis teismas sureguliavo tuos vidinius teisinius nesutapimus, dėl kurių Vasiliausko byla tapo paini. Aukščiausiasis teismas išaiškino, kodėl tarybų valdžiai pasipriešinę partizanai gali būti įvardinti „svarbia tautos sudėtine dalimi“.

Būtent kaip Lietuva įrodinėjo Strasbūrui savo „miško brolių svarbą“? Šį momentą istorija nutyli. Teismo nutartyje deklaruojama, kad partizanai tikrai „suvaidino svarbų vaidmenį gindami nacionalinę tapatybę, kultūrą ir lietuvių tautos nacionalinę savimonę“. Be to, Vilnius remiasi 2014 metų Konstitucinio teismo nutartimi, kurioje užfiksuota partizaninio judėjimo svarba lietuvių tautai. Vadinasi, Vasiliausko atveju tas „kozyris“ nebuvo panaudotas.

Išvada: Lietuvos Temidės atstovai tiesiog „sušukavo“ savo kaltinimus genocidu, paprakaitavo ieškodami kelių, atvedančių juos prie tarptautinių normų reikalavimų. O EŽTT dabar priblokštas: argi galima nepripažinti genocidu Vanago persekiojimo, jei jis buvo toks šaunus tautos atstovas?

Čia vėl galima prisiminti „genocido“ apibrėžimą` kaip visišką nacionalinės grupės arba jos dalies sunaikinimą. Taigi peršasi išvada, kad Lietuvoje komunistai „naikino“ dalį tautos – žudė jos „brangiausius“ atstovus.

Bet kuo tokiu atveju užsiiminėjo pats Adolfas Ramanauskas–Vanagas? Argi ne savo tautos žudymu? „Aiškėja, jog tarp aukų daugiausia buvo būtent taikių gyventojų, neginkluotų ir neturinčių ryšių su Raudonaja Armija arba su valstybės saugumo organais“, — apie jo „žygdarbius“ pasakojo fondo „Istorinė atmintis“ tyrimų programų vadovas Vladimiras Simindėjus.

EŽTT tokių klausimų nekels ir jais neužsiminės. Teismui svarbus tik formalus bylos aspektas: kad nebūtų prieštaravimų tarp Lietuvos ir tarptautinės įstatymų leidybos.

„Faktų ir teisės normų aprašymas teisingas, o juridiniai teiginiai ir išvados, mano manymu, kreivi“, — taip nutartį charakterizavo Europos parlamento frakcijos „Žalieji/ Laisvas europietiškas aljansas“ patarėjas juridiniais klausimais Aleksėjus Dimitrovas.

Tačiau įdomiausia tai, jog EŽTT praneša, jog atnaujins vidinį Vasiliausko bylos Lietuvoje tyrimą. Žinoma, atsižvelgiant į Strasbūro rekomendacijas. Nepavyko nuteisti už politinės grupės genocidą — nuteis už lietuvių tautos genocidą.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 8 — id: `scraped:rubaltic_lt:f63d5192dd32a27c`

**Title:** 5 knygos, kurios neleistų Grybauskaitei ramiai miegoti naktį

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Po Tarybų Sąjungos suirimo „demokratinėje“ Lietuvoje egzistuoja keletas tabuotų temų. „Miško brolių“ nusikaltimai, masiškas lietuvių dalyvavimas žydų žudynėse, šiuometinių šalies lyderių kooperavimas su KGB, o taip pat Sausio 13-osios įvykiai prie Vilniaus televizijos bokšto – monografijos, neigiančios oficialias tokių temų versijas, yra persekiojamos Lietuvos valdžios su Šventosios inkvizicijos uolumu. Analitinis portalas RuBaltic.Ru primena 5 knygas, kurių neskaitys prieš miegą Dalia Grybauskaitė.

1. „Mūsiškiai“ (Rūta Vanagaitė)

Knyga „Mūsiškiai“ rašytojos tėvynėje pasirodė 2016 metais – Lietuvos nacistinės okupacijos 75 metų minimo proga. Šios okupacijos pasekmė – visuotinis vietinės žydų bendruomenės naikinimas (virš 90% jos narių). Kaip tik šitam neturinčiam senaties termino nusikaltimui prieš žmoniją yra skirtas Vanagaitės kūrinys.

Pirmoje knygos dalyje aprašomi 1941-1944 metų nusikaltimai prieš žydus, kuriuose aktyviai dalyvavo ir vietiniai okupuotų teritorijų gyventojai. Autorius taip pasakoja apie šituos įvykius: „Iš pradžių buvo planuota išvaryti žydus, o paskui pamažu juos išvarė giliai po žemę“.

Antroji dalis yra bendros Rūtos Vanagaitės ir Efraimo Zuroffo, Simono Vizantelio centro skyriaus Jeruzalėje vadovo, kelionės po žydų žudynių vietas apybraiža.

Reakcija Lietuvoje

Dalis lietuvių griežtai pasmerkė rašytoją už nemalonią tiesą. Kiti, atvirkščiai, parėmė jos norą išnagrinėti tikrą istoriją be „retušavimo“.

Situacija pasikeitė 2017 metais, kai Vanagaitė, kreipdamasi į parlamentarų komisiją, apkaltino „miško brolį“ Adolfą Ramanauską-Vanagą bendradarbiavimu su tarybiniais saugumo organais.

Kritiškai pasisakė ir valdančiojo elito atstovai. Vytautas Landsbergis nedviprasmiškai pasiūlė Vanagaitei nueit „į mišką, kur drebulės, pasimelsti ir nusiteisti“.

Agresijos taikiniu tapo ir rašytojos knygos.

Iškart po skandalo įsiliepsnojimo leidykla „Alma littera“ staiga nutraukė bendradarbiavimą su Vanagaite ir liovėsi parduoti visas jos knygas, nurodžiusi, kad neva rašytojos vieši pasisakymai pažemino Lietuvos istorinę atmintį.

Šie veiksmai privertė Rūtą Vanagaitę palikti Lietuvą ir emigruoti.

2. „Žali“ (Marius Ivaškevičius)

Itin skausmingą Lietuvos nacionalistams temą apie tikrąsias „miško brolių“ bylas nagrinėja Mariaus Ivaškevičiaus romanas „Žali“, išleistas 2002 metais. Knygoje aprašomi pokario, 1950 metų rugpjūčio mėnesio, įvykiai.

Pikantiškumo visam kūriniui suteikia faktas, kad jame kritikuojamas partizaninio judėjimo vadas Jonas Žemaitis. Jo autoritetas šiuolaikinėje Lietuvoje toks žymus, kad šalies Seimas pripažino Joną Žemaitį faktišku valstybės prezidentu nuo 1949-ųjų metų vasario 16 dienos iki pat jo mirties – 1954-ųjų metų lapkričio 26 dieną.

Reakcija Lietuvoje

Šita knyga irgi suskaldė šalį į dvi kariaujančias puses. Savo pasibjaurėjimą knyga, kaip atsitiks vėliau ir su Rūtos Vanagaitės kūriniu, pareiškė pagrindinis Lietuvos „nacionalinio orumo“ gynėjas Vytautas Landsbergis.

Kaip visuomet, jis pažymėjo, kad būtent Rusijos valdžiai naudingas šitos knygos pasirodymas. Pačią knygą jis pavadino „pseudofaktine provokacija“.

Skundą parėmė 32 žmonės, jų tarpe – skirtingų nevyriausybinių organizacijų atstovai. Jie prašė inicijuoti ikiteisminį tyrimą prieš rašytoją ir kartu pareikalavo atšaukti Ivaškevičiui skirtą Lietuvos nacionalinę kultūros ir meno premiją.

Vilniaus apygardos prokuratūra savo atsakyme į aktyvistų skundą teigė, kad Ivaškevičiaus knygoje nėra nieko, kas „galėtų pažeisti žmonių sveikatą, moralę, privatumą ar Lietuvos konstitucinę tvarką“. „Patriotus“ toks atsakymas, žinoma, nepatenkino.

3. „Raudonoji Dalia“ (Rūta Janutienė)

2012 metais žurnalistė Rūta Janutienė paruošė tiriamosios žurnalistikos laidą „Paskutinė instancija“, kurioje tikėjosi papasakoti apie komunistinę Lietuvos prezidentės praeitį.

Janutienė planavo papasakoti, kad net po Lietuvos nepriklausomybės atkūrimo 1990 metų kovo mėnesį Dalia Grybauskaitė tęsė darbą Vilniaus Aukštojoje partinėje mokykloje. Taip pat iš Janutienės laidos lietuviai būtų sužinoję daug naujo apie prezidentės bendradarbiavimą su KGB.

Laida turėjo pasirodyti 2012 metų lapkričio 22 dieną per privatų kanalą TV3.

Bet Rūta nenuleido rankų ir parašė knygą „Raudonoji Dalia“, kurioje surinko dokumentus, atskleidžiančius Lietuvos prezidentės biografijos detales, o taip pat žmonių, pažinančių Grybauskaitę ar nagrinėjusių jos biografiją, pasakojimus.

Dirbdama archyve savo žurnalistiniam tyrimui Janutienė pastebėjo, kad keli prezidentės asmeninės bylos puslapių buvo išimti iš jos. Matyt, kai kas nenori, kad „raudonosios Dalios“ praeitis būtų atskleista.

Reakcija Lietuvoje

Ažiotažas aplink „Raudonąją Dalią“ kilo, kai Europos Parlamento deputatai rado savo darbo pašto dežutėse išverstos į anglų kalbą knygos egzempliorius. Tyrimo metu paaiškėjo, kad popierinio leidinio platintoju buvo Euroskeptikų frakcijos darbuotojas iš Maltos Kevinas Ellul Bonici, kuris po kompromato platinimo buvo atleistas iš pareigų.

Gabrielius Landsbergis (Vytauto Landsbergio anūkas), Lietuvos konservatorių, įeinančių į Grybauskaitės aljansą, lyderis, pažymėjo, kad knyga pasirodė iškart po Lietuvos prezidentės griežtų pasisakymų prieš Rusiją. Jaunasis Landsbergis pavadino Janutienės knygos platinimo veiksmus „dar vienu informaciniu smūgiu prieš Lietuvą“.

4. „Kas ką išdavė“ (Galina Sapožnikova)

Knyga „Kas ką išdavė“ buvo parašyta 2016 metais laikraščio „Komsomolskaja pravda“ žurnalistės Galinos Sapožnikovos. Kūrinyje pasakojama apie tai, kaip Lietuva pirma iš Tarybų Sąjungos respublikų tapo „spalvotų revoliucijų“ manipuliatyvių technologijų aprobavimo aikšte.

Autorė aprašo įvykius, grindžianti savo požiūrį skirtingais pokalbiais su liudytojais ir tų įvykių dalyviais.

Galų gale Sapožnikova neigia įsivyravusią nuomonę, kad masinis judėjimas Lietuvoje už nepriklausomybę nuo TSRS buvo žmonių valios deklaracija.

Reakcija Lietuvoje

Knyga buvo išversta į anglų kalbą su viršeliu „Lietuviškas sąmokslas. Kaip žlugo Sovietų Sąjunga“.

Taip nutiko Romoje, kai Lietuvos Respublikos ambasadorius nukreipė į italų parlamentą reikalavimą dėl renginio uždraudimo. Panaši situacija susiklostė ir prezentacijos Milane metu: knygyno, kuriame vyko Sapožnikovos knygos prezentacija, vadovas gavo laišką iš Lietuvos ambasadoriaus su reikalavimu uždrausti renginį.

Laimei Italijoje tokios pastangos apriboti žodžio laisvę nebuvo sėkmingos.

Deja, tokie apribojimai Lietuvos skaitytojams gauti prieigą prie informacijos tik paskatino susidomėjimą Sapožnikovos darbu kitose šalyse. Pavyzdžiui, viena JAV leidykla, sužinojusi apie knygos persekiojimą Baltijos šalyje, atspausdino knygos tiražą savo lėšomis.

5. „Durnių laivas“ (Vytautas Petkevičius)

Knygą 2004 metais parašė miręs 2008 metais Vytautas Petkevičius. Savo kūrinyje Petkevičius išsamiai pasakoja, kaip kartu su patriotiniu antisovietiniu sukilimu Lietuvoje buvo sunaikintas nusistovėjęs gyvenimo būdas, o ant jo griuvėsių iškilo spekuliuojantys tautos laisve politikai.

Reakcija Lietuvoje

Lietuvos Aukščiausiojo Teismo sprendimu knyga buvo uždrausta respublikoje dėl to, kad joje Petkevičius neva apšmeižė Vytauto Landsbergio-Žemkalnio, jau minėto šiame straipsnyje

tautinio atgimimo lyderio tėvo, vardą. Petkevičius jį pavadino „Hitlerio draugu“. Tokio pareiškimo pagrindu buvo tai, kad Landsbergis-Žemkalnis buvo Nacių okupuotos Lietuvos laikinosios vyriausybės Komunalinio ūkio ministru.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 9 — id: `scraped:rubaltic_lt:d94bdf1515cfd4e2`

**Title:** „Chuliganiškas planas“. Lietuva nori permesti Baltarusijai SGD terminalo naštą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos premjeras Saulius Skvernelis paskelbė jau anksčiau anonsuotą „chuliganišką“ planą Baltarusijos AE atžvilgiu. Skvernelis pasiūlė statomai Baltarusijos elektrinei naudoti ne atominę energiją, o dujas, kurias jai tieks Lietuva. Lietuvos premjeras labai tiksliai charakterizavo savo planą: tai iniciatyva smulkaus chuligano, kuris nutarė: „SGD terminalo naštą“ reikia permesti nuo Lietuvos mokesčių mokėtojų ant baltarusių pečių, pasiūlant kaimynams dengti Lietuvos „energetinės nepriklausomybės“ nuostolius — už tai Lietuva atsilygins, užbaigdama su Minsku diplomatinį karą.

„Mes pasiūlytumėm Baltarusijai priimti strateginį sprendimą vystyti savarankišką ir diversifikacinį energetinį ūkį. Mes taip pat matome perspektyvas srityje atsinaujinančios energetikos, dėl kurios šalis neskęsta šimtus metų besitęsiančiuose projektuose. Žinoma, tai jau Baltarusijos teisė: rinktis — vystyti vienašalią priklausomybę nuo vienos šalies energetinės politikos pagrindų ar įgyvendinti strateginius pokyčius energetikos sferoje. Tokiu keliu eina Lietuva, kuri galėtų būti ir geru pavyzdžiu, ir naudinga Baltarusijos partnere“, — pareiškė Lietuvos premjeras Saulius Skvernelis.

Tai ir yra tas „chuliganiškas“ Baltarusijos AE siūlomas planas, kuriuo praeitą savaitę buvo suintriguota visa Lietuva. Tada Lietuvos premjeras pažadėjo pasiūlyti baltarusiams sprendimą — drąsų, tačiau kompromisinį, kuris garantuoja Lietuvos interesų paisymą ir leis baltarusiams neatsisakyti Ostroveco AE projekto.

Šie pažadai labai sunervino Lietuvos prezidentę Dalią Grybauskaitę ir URM vadovą Liną Linkevičių. Grybauskaitė pareiškė, jog negali būti tokio kompromiso, kuris leistų statyti atominę elektrinę prie Lietuvos sienų. Linkevičius pareiškė nieko nežinantis apie „chuliganišką“ Skvernelio planą ir kad Vilnius tebepasisako prieš Baltarusijos AE.

Pagaliau vyriausybės vadovas sugebėjo visus ne tik suintriguoti, bet ir nustebinti.

Čia turime priminti, kad į politiką Saulius Skvernelis atėjo po tarnybos policijoje, ir ši jo praeitis neišvengiamai įtakoja jo veiklą. Buvęs kelių policijos viršininkas ir sulaikytųjų eskortų komandos komisaras iš buvusių darboviečių perėmė savo pavaldinių — įvairių lygių nenaudėlių — metodus.

Lietuvos vyriausybės vadovas siūlo, išsireiškiant jam suprantama kalba, „spjauti į durnelio indėlį“. Baltarusijos AE statyboms 10 milijardų dolerių kreditą skyrė „Rosatomas“. Didžioji šių lėšų dalis jau investuota į elektrinės energetinę infrastruktūrą.

Pagrindinės skolos dalies grąžinimas prasidės po to, kai eksploatuoti bus pradėti du „Rosatomo“ atominiai reaktoriai ir Baltarusijos AE pradės gaminti energiją.

„Chuliganiškas planas“ — gana sąžininga šio projekto charakteristika. Tai natūralus tarptautinis nemokšiškumas.

Iškart jaučiasi Lietuvos premjero iniciatyvos antirusiškas dvelksmas, tačiau Skvernelis siekia ne tik visiems laikams supjudyti Maskvą su Minsku, bet ir „apdumti akis“ baltarusiams.

„Pasinaudodama Klaipėdos jūrų uoste esančio ir veikiančio suskystintų gamtinių dujų terminalo bei Lietuvos su Lenkija dujų sandūros galimybėmis, Baltarusija turės alternatyvią galimybę gauti dujų žaliavą“, — teigia Lietuvos premjeras.

Kad Independence Klaipėdoje mokesčių mokėtojams tapo našta, prieš porą metų pripažino pats Lietuvos vyriausybės vadovas. Plaukiojantis SGD terminalas nuostolingas. Naudojama mažiau ketvirtadalio jo galingumų, sunku rasti lėšų Independence laivo norvegų savininkui mokėti nuomą, kaimynai SGD terminalo produkcijos kratosi — jie perka pigiasnes rusiškas dujas, regioninio Pabaltijo projekto statuso Independence negavo, todėl negaus ir Europos Sąjungos finansavimo. Kur nepažvelgtum — visur nesėkmės.

Tada Saulius Skvernelis pažadėjo mokesčių mokėtojams pagalvoti, kaip atsikratyti šios naštos. Ir štai, atrodo, sugalvojo. Jei Latvija su Estija pirkti Lietuvos terminalo dujas atsisako, jas pirks Baltarusija, o Lietuva atsilygins atkurtais su ja gerais santykiais.

Gal kaip kompensaciją už tai, jog su vienu iš kaimynų tenka turėti gerus santykius, Lietuvos premjeras tikisi gerai uždirbti, tiekdamas Baltarusijai dujas? Minskui Lietuva tieks brangią Independence produkciją — suskystintas norvegų, katariečių ir amerikiečių dujas, o pati pirks pigias rusų vamzdines dujas. Neatsitiktinai „Gazpromo“ parduodamų Lietuvai dujų kiekiai pastoviai auga.

Nauda triguba. Pirma, Lietuva suranda klientą savo niekam nereikalingam terminalui. Antra, uždirba „velniškus pinigus“ iš rusiškų ir savo redujofikuotos energijos produkto vertės skirtumo. Trečia, supjudina Maskvą su Minsku ir stumteli Baltarusiją Vakarų link.

Tačiau išradingu ir gudriu „chuliganišką planą“ gali pavadinti tik nieko energetikoje nenusimanantis žmogus. Net paviršutiniškai įsigilinus į šios idėjos esmę gerai matosi jos kūrėjo įžūlumas ir kvailumas.

Pakeisti atominę elektrinę dujine galima tik visiškai nušlavus jau sukurtą atominės infrastruktūrą ir tuščioje vietoje pastačius dujinę. Likus keliems mėnesiams iki Baltarusijos AE eksploatavimo pradžios, teikti tokį pasiūlymą juokinga.

„Lietuva čia greičiausiai nori pasireikšti garsiais politiniais pareiškimais, puikiai suprasdama, kad esant betonuotai aikštelei, kai jau statomas reaktorius, niekas šio projekto neužšaldys“, — Lietuvos premjero iniciatyvą RuBaltic.Ru komentavo Nacionalinio energetinio saugumo fondo direktorius Konstantinas Simonovas.

Klausimas: kodėl Saulius Skvernelis paskelbė tokį pasiūlymą, jeigu jis akivaizdžiai kvailas ir priverčia iš jo juoktis? Peršasi gana nekorektiškas atsakymas: koks žmogus, toks ir pasiūlymas.

Jeigu įžvelgti hipotezę, kad Lietuvos vyriausybės vadovas daug ko pasimokė iš tų pašlemėkų, kuriuos savo policiškoje jaunystėje lydėjo į „cypę“, jo „chuliganiškas planas“ tampa suprantamas.

Tik kine ir literatūroje smulkūs žulikai patrauklūs, pasižymi intelektu ir liežuvingumu, kaip Ostapas Benderis. O gyvenime jų daugumos fantazija apsiriboja vienu sakiniu: „Dėde, pirk plytą“.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 10 — id: `scraped:rubaltic_lt:71089e0be824aed9`

**Title:** Pralošė visos partijos: municipalinių rinkimų rezultatai Lietuvoje

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvoje užsibaigė municipaliniai rinkimai, kuriuose prieš prezidentinę kampaniją „prasimankštino“ pagrindiniai politiniai žaidėjai. Po preliminaraus balsų skaičiavimo paaiškėįo, kad pralaimėjusiomis praktiškai galima laikyti visas Lietuvos partijas. Balsuodami pagal kandidatų sąrašus, rinkėjai pirmenybę suteikė visuomeniniams komitetams, tuo išreikšdami nepasitikėjimą partine sistema.

Preliminariai suskaičiavus balsus paaiškėjo, kad už visuomeninių komitetų sąrašus balsavo 26,75 proc. bendro rinkėjų skaičiaus. Palyginimui: paskutiniųjų municipalinių rinkimų metu komitetai buvo surinkę 2,5 karto balsų mažiau — vos per 10 proc. Tokia teigiama dinamika negali pasigirti nė viena politinė jėga.

Konservatoriai, „Tėvynės Sąjunga – Lietuvos krikščionys demokratai“ (TS–LKD), ūgtelėjo ststistinės paklaidos lygmenyje (16,02 prieš 15 proc. 2015 m.). Valdančioji Lietuvos valstiečių ir „žaliųjų“ sąjunga (LVŽS) ūgtekėjo trimis balsų procentais (11,15 proc. prieš 7 proc.). Jos koalicijos sąjungininkai socialdemokratai — priešingai: nuo 20 proc. krito iki 16 proc.

Galimai dalis Lietuvos socialdemokratų partijos elektorato po jos skilimo pasirinko perspektyvesnius „valstiečius“, neskaičiuojant tų 1,67 proc. rinkėjų, atidavusių balsus atskilusiai nuo jos Lietuvos socialdemokratų darbo partijai.

Rezultatai kitų politinių jėgų, kurios 2015 metais neketino skęsti, taip pat ženkliai pablogėjo.

Ir tai visiškai nenuostabu. Iš savo politinių viršūnių LLS krito beveik iškart po 2015 metų rinkimų. Partijos pirmininkas Eligijus Masiulis tapo vienu iš pagrindinių figūrantų MG Baltic byloje. Garsus korupcijos skandalas tapo liberalams nokdaunu, ir jau po mėnesio jų reitingas sumažėjo 9 proc. 2016 metų parlamento rinkimuose jie ėjo jau be Masiulio, užėmė ketvirtą vietą ir gavo 14 mandatų. Lietuvos liberalų sąjūdžio vadai visa tai palaikė sėkme, o Vilniaus meras Remigijus Šimašius net neatsargiai mestelėjo TS–LK adresu: „Jeigu iš šalies pažvelgti į „Tėvynės Sąjungą“, tai konservatoriai vietoj aktyvesnio konsolidavimo balsų, kurių jie galėjo sulaukti iš konservatyvesnių gyventojų, nutarė konkuruoti su Liberalų sąjūdžiu dėl liberaliai mąstančių žmonių“.

Ką gi, „landsbergininkai“ sparčiai išgydė liberalų lygybės sindromą. Prasidėjus išoriniam spaudimui, partijoje įsiplieskė vidiniai kivirčai, o praeitų municipalinių rinkimų triumfatoriai — jau minėtas Šimašius ir Klaipėdos meras Vytautas Grubliauskas — pasitraukė iš jos gretų.

Gabrieliaus Landsbergio lūpomis konservatoriai 2017 metais paskelbė liberalams „mirties nuosprendį“: „Deja, tenka pripažinti, kad tai, greičiausia, Liberalų sąjūdžio galas“.

Praėję rinkimai parodė, kad šis tvirtinimas buvo teisingas. Dabar liberalų laukia perspektyva rinkimų metu nepatekti į Seimą.

Atrodytų, jaunesniųjų sąjungininkų kritimu konservatoriai turėtų būti patenkinti, juk TS–LKD ir LLS, kaip tiksliai pastebėjo Šimašius, žaidžia tame pačiame elektorato lauke. Kuo labiau krinta liberalai, tuo aukščiau kyla konservatoriai. To buvo tikėtasi.

Alternatyvių politinių jėgų šalininkais netapo ir kitomis politinėmis jėgomis nusivylę rinkėjai. Darbo partija praeituose rinkimuose surinko apie 9 proc. balsų — šiandien krito iki 5,1 proc. Apie 3 proc. prarado Lietuvos lenkų rinkimų akcija, tiek pat — Tvarkos ir teisingumo partija.

Tačiau šių balsų negavo nei konservatoriai, nei „žalieji“. Jie atnešė sėkmę visuomeniniams rinkimų komitetams, išvengusiems partinių spalvų.

Rinkimų išvakarėse Gabrielius Landsbergis paviešino savo prognozes municipaliniuose rinkimuose: konservatoriai turi aplenkti 2015 metais pirmąją vietą užėmusius socialdemokratus. Uždavinys maksimum — užimti pirmąją vietą pagal mandatų skaičių. Sprendžiant pagal preliminarius rezultatus, TS–LKD užsibrėžto tikslo pasiekė.

Ši tendencija akivaizdžiai buvo matoma jau praeitų rinkimų rezultatuose. Jau tada nepriklausomi kandidatai tapo merais nemažų miestų, nustumdami savo partinius oponentus. Šiaulių vadovu, pavyzdžiui, tapo save iškėlęs Artūras Visockas, nepartiniai Rytis Mykolas Račkauskas ir Vytautas Grigaravičius rinkėjų pasitikėjimą pelnė Panevėžyje ir Alytuje.

Liberalų sąjūdis buvo iškilęs todėl, jog visuomenė pavargo nuo konservatorių ir socialdemokratų politikos. Tačiau LLS rinkėjai gana greitai nusileido iš padangių, nes suprato, kad jų numylėtiniai taip pat nuodėmingi. Šiandien ketvirtadalis Lietuvos rinkėjų jau nemąsto kandidatų partinio identiškumo kategorijomis. Ir tai rimtas iššūkis sisteminėms partinėms jėgoms. Pirmiausia — TS–LKD.

Iš vienos pusės, konservatoriai rodo stabilius rezultatus ir prie bet kurios konjunktūros gali pasikliauti savo rinkėju ( ko negalima pasakyti, pavyzdžiui, apie liberalus, kurie po pirmo rimto skandalo tuoj pat išbarstė elektoratą).

Iš kitos pusės, išseko TS–LKD rezervai keliant savo reitingą oponentų diskreditavimo sąskaita.

Nei konservatoriams, nei „valstiečiams“, kurie kaunasi dėl šalies prezidento posto, visa tai nežada nieko gero.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 11 — id: `scraped:rubaltic_lt:2e8c9b32e910c2aa`

**Title:** Europos parlamentaras: elitų suokalbis verčia Europos Sąjungą nutylėti represijas Pabaltijyje

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Europos parlamente vasario 20 dieną vyko viešas svarstymas tema „Politiniai persekiojimai Pabaltijo šalyse“. Renginio eigoje buvo pristatytas analitinis RuBaltic.Ru pranešimas „Politinės represijos ir politiniai Pabaltijo kaliniai“. Apie tai, ar europiečiai pasiruošę pripažinti politinių kalinių Pabaltijyje egzistavimą, kodėl persekiojimai Lietuvoje, Latvijoje ir Estijoje politiniais motyvais ir nacionaliniu pagrindu nesulaukia Europos Sąjungoje vieningo pasmerkimo ir kaip Pabaltijo vyriausybių atstovai reaguoja į kritiką savo adresu, RuBaltic.Ru papasakojo viešųjų svarstymų organizatorius, partijos „Latvijos rusų sąjunga“ bendravaldis pirmininkas, Europos parlamento deputatas Miroslavas Mitrofanovas.

— Pone Mitrofanovai, kai Jūs skelbėte Europos parlamente praėjusį renginį, ar tame parlamente pastebėjote nuostabą, kad Pabaltijo šalyse, sprendžiant iš svarstymų pavadinimo, vykdomos politinės represijos?

— Pastebėjau tam tikrą įtampą ir nepasitikėjimą, ir reikėjo visa tai įveikti. Bet mes jau turime patirties. Europietiškas rusų forumas, kuris praėjo praeitų metų pabaigoje, buvo sutiktas panašiomis emocijomis ir bandymais jį sutrikdyti.

Jie mums netrukdė, tačiau jautėme, jog esame aktyviai stebimi; iki paskutiniųjų stengėmės paslaptyje išlaikyti pavardes pakviestų žmonių, kad valdžios neturėtų galimybių sulaikyti juos, neįsileisti į svarstymus.

— Tai yra jie galėjo sutrukdyti pravesti renginį, jei apie jį būtų žinota iš anksto?

— Jie būtų galėję tiesiog neįsileisti žmonių, ir mes būtume pralaimėję. Viena, asmeninis bendravimas, o visai kas kita — televizijos tiltai ir t.t. Visa tai pagal mūsų jėgas, tačiau daug svarbiau — asmeninis dalyvavimas.

— O kai Jūs kvietėte kolegas iš Vakarų Europos dalyvauti svarstymuose, kaip jie reagavo į patį pavadinimą „Politinės represijos Pabaltijo šalyse“? Vėlgi, Vakaruose dažnai manoma, kad Pabaltijo šalyse negali būti politinių represijų, nes jos vykdo visas rekomendacijas demokratijos ir žmogaus teisių srityse ir yra pavyzdys net rytų kaimynams.

— Europos parlamente apie 750 deputatų, aš žinau, jog kiekvienas savaip žiūri į politines represijas. Yra dešiniųjų konservatyvių partijų žmonių, kurie net nekrūpteli, išgirdę žodį „represijos“, sako: „Juk turi būti tvarka“, tačiau tokių mažuma. Visas politinis spektras — nuo konservatorių iki komunistų — nepamiršta liūdnos praeito šimtmečio patirties, tai yra europietiškos istorijos, kai buvo ir diktatūra, ir represijos, ir laisvės apribojimai. Visa tai buvo sunkiai įveikiama, ir viskas iki šiol sunkiai juda į priekį, todėl į tai jie žvelgia su drebuliu.

Neseniai buvo skaitomas pranešimas, smerkiantis radikalizmą ir prievartą; absoliuti dauguma ES deputatų jį palaikė.

Kitas klausimas — elito sąmokslo egzistavimas: kai reikia reaguoti kokiais nors realiais žingsniais, jie prisimena, kas kam kiek skolingas. Ir, kaip nebūtų keista, atrodo, jog stipriausia šalis — Vokietija, ir kaip ji pasakys, taip ir bus. Tai toli gražu ne taip.

Dauguma nacionalinių valstybių mažesnės, nei didelių šalių regionai. Galima prisiminti Maltą (300 tūkstančių gyventojų) ir Estiją (vos daugiau milijono). Tačiau ir Lietuva su Latvija — pagal dydį ir ekonomikos lygį faktiškai keli Vokietijos miestai. Tačiau norint, kad ES būtų priimti ekonominiai sprendimai, didžiulė Vokietija turi užsitikrinti šių mikroskopinių, tačiau strategiškai svarbių valstybių valdančiųjų partijų paramą.

Todėl labai paprasta, pavyzdžiui, taikyti sankcijas Rusijai, tačiau paskui sudėtinga jas panaikinti. Arba lengva kalbėtis su eiliniais deputatais apie politinių persekiojimų faktus, apie teisingumą, apie žmogaus teisių bei tarptautinių normų kai kuriose ES šalyse pažeidimus.

Tai yra keičiamės: jūs remiate mūsų ekonominius sprendimus, o mes nekalbame apie jūsų teisėsaugos nesėkmes ir griaučius spintoje.

— Tai yra jie žino, tačiau nekalba apie tai, kokioje būklėje Pabaltijyje yra žmogaus teisės? Ar jie tiesiog nežino apie tokių problemų egzistavimą?

— Sprendžiant iš to, kad pernai jie palaikė kovos su radikalizmu ir prievarta rezoliuciją, jie viską žino. Kovo 16 dieną buvo pasmerkta Latvija už Latvių SS legiono maršą. Taigi matome, jog palaikė visos frakcijos, kitas dalykas — ne visos balsavo. Tačiau visumoje parlamento narių dauguma latvius smerkė.

Beje, ši rezoliucija — konkretaus žmogaus pozicija, tačiau kai reikalai krypsta link kolektyvinio intereso, jie stumia savo pozicijas į šalį.

Ką gali reikšti žmogaus teisės, jei pirmoje vietoje milijardinės investicijos?

— Šiandien mes su Jumis girdėjome oficialią Pabaltijo šalių poziciją, tame tarpe Lietuvos. Ji įdomi tuo, jog Vilniaus atstovė nesugebėjo paprieštarauti nė vienu punktu kaltinimų, kuriuos Lietuvos adresu išsakiau aš ir mano kolega Giedrius Grabauskas. Jos argumentai — ekonominiai Lietuvos pasiekimai, aukšti šalies reitingai tarptautinėse organizacijose ir sunkūs „sovietinės okupacijos“ dešimtmečiai. Jie visada taip pasisako“.

— Esmė tame, jog ten nėra normalios konkurencijos: matote, tarptautiniame lygyje Vilnius retai susiduria su opozicijos nuomone.

Tačiau, kaip Jūs teisingai pastebėjote, dabartinės problemos su žmogaus teisėmis siejamos labai silpnai. Ten nėra naujų argumentų, neturima kuo atsikirsti. Iki šiol nėra įrodymų, jog ištisus metus kalinamas žmogus buvo sulaikytas už šnipinėjimą Rusijos naudai. Kaip galėjo Algirdas Paleckis užsiiminėti šnipinėjimu, jei jis neturi nieko bendro su valstybės sistema?

Visi šie nesiduriantys galai gerai matomi, tačiau lietuviai kol kas neturi į juos atsakymų. Tačiau jeigu mes reikalausime juos dažnai pasisakyti šiomis temomis, jie mokysis išsisukinėti.

— Šalies viduje jie atrado labai paprastą būdą išvengti nuomonių konkurencijos: jie draudžia užsieniečiams įvažiuoti, blokuoja užsienio TV kanalus, žlugdo viešąsias priemones.

— Išties aš nepamenu pastaraisiais metais Lietuvos valdžių atstovų susitikimų su opozicija, kuriuose būtų aptariamos istorinės ir teisėtvarkos temos.

— Ar kas nors Europos parlamente, išskyrus Lietuvos deputatus, žino apie sausio 13-osios bylą ir Jurijui Meliui mestus kaltinimus?

— Manau, žino lenkų ir latvių deputatai. Tai yra tiesioginiai kaimynai.

— Tačiau vėlgi tyli politiniais sumetimais?

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 12 — id: `scraped:rubaltic_lt:06038b49017d4b7b`

**Title:** RuBaltic.Ru Jurijaus Melio problemą iškėlė Europos parlamente

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Vasario 20 d. Europos parlamente įvyko vieši politinių persekiojimų Pabaltijo šalyse klausimo svarstymai. Renginyje dalyvavo Latvijos ir Estijos eurodeputatai, o taip pat realios politinių persekiojimų Pabaltijo respublikose aukos.

Jis priminė, kad pagal Lietuvos versiją dėl 14 žmonų žūties 1991 metų sausio 13 dieną prie Vilniaus televizijos bokšto kalti tarybiniai kariškiai. Pagrindinis teisiamas kaltinamasis — Rusijos kariuomenės atsargos pulkininkas Jurijus Melis, kuris 1991 metais vadovavo tankų būriui ir prie Vilniaus televizijos bokšto tris kartus šovė tuščiais iš tanko. Lietuvos prokuratūra kaltina Melį karo nusikaltimais žmoniškumui ir reikalauja jam 16 metų kalėjimo.

„Jurijaus Melio byla — politinio persekiojimo pavyzdys. Lietuvos valstybė neneigia, kad nuo Melio veiksmų nenukentėjo nė vienas žmogus, tačiau už žmonių žūtį taiko jam kolektyvinę atsakomybę“, — nurodė RuBaltic.Ru apžvalgininkas.

Svarstymo metu Nosovičius pateikė pranešimą „Politinės represijos ir politiniai Pabaltijo kaliniai. Baudžiamoji justicija politinių Lietuvos, Latvijos ir Estijos režimų sargyboje“. Su visu pranešimo tekstu galima susipažinti čia:

RuBaltic.Ru pranešimas / Politinės represijos ir politiniai Pabaltijo kaliniai / rusų kalba

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 13 — id: `scraped:rubaltic_lt:204a8cee8448f364`

**Title:** Neviens neņems vērā Baltijas intereses strīdā iestigušajā Eiropas Savienībā

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Eiropas Savienību plosa iekšējās pretrunas. Francija tirgojas ar Vāciju par „Ziemeļu straumi 2“, Itālija atbalsta „dzelteno vestu“ kustību Francijā, bet Lielbritānija kašķējas ar visu „vienoto Eiropu“ par savu izstāšanos no ES. Par to, vai sašķēlies Eiropas Savienības romāņu-vācu „kodols“, pie kā novedīs Brexit, vai reāls ir ES sabrukuma risks un kas notiks ar Baltijas perifēriju krīzes plosītajā ES, analītiskajam portālam RuBaltic.Ru pastāstīja Politisko un ekonomisko pētījumu centra (Maskava) vadītājs Vasilijs KOLTAŠOVS.

Par Itālijas soļiem pret ES

— Par apvienoto Eiropu iespējams runāt, kamēr Vācija kontrolē procesus ES, bet briti bezpalīdzīgi vāļājas ceļos Angelas Merkeles priekšā un baidās pat iepīkstēties, ka viņi varētu sagraut ES. Taču Vācija šo Eiropu vada ar stingru roku.

Itālijai klāsies ļoti smagi, ja Merkele sadusmosies. Kad viņa sadusmojās 2015.gadā , uz ceļiem tika nospiesti grieķi.

Notikumi attīstās vienveidīgi: izskan draudi organizēt finansiālo izolāciju, to, ka jūs neapmeklēs neviens tūrists, neviena jūsu prece netiks pārdota Eiropā... Pēc tam visi atkal ir paklausīgi.

Tāpēc Itālijas lēmums atbalstīt “dzeltenās vestes” drīzāk liecina par cīņu resursu pārdales ietvaros Eiropas Savienībā. Tās sabrukums diezin vai ir iespējams.

Par ES vienotības perspektīvām

— ES sabrukums bija iespējams 2017.gadā, kad notika Francijas prezidenta vēlēšanas.

Taču briti deva priekšroku pārrunām ar ES birokrātiem un Merkeli. Rezultātā viņi saņēma noteikumus, kas viņiem šķiet neapmierinoši. Par to Terēza Meja saskārusies ar smagu kritiku.

Francijā uzvaru izcīnīja Emanuels Makrons, kam Merkele dāvājusi vairākus “reveransus”. Vācijas kanclere sniedza Makronam iespēju justies kā augsta līmeņa politiķim, kādu Fransuā Olands savas prezidentūras gados nekad nav sasniedzis.

Rezultātā franči primitīvi seko Vācijas fārvaterā. Grieķijas finanšu ministrs Jans Varufaks situāciju komentēja īsi: franči atkārto, ko teikuši vācieši.

Tātad ES sabrukums Rietumos ir maz iedomājams. Lielā mērā viss ir atkarīgs no sistēmas, no vācu tūristu plūsmas. Taču Austrumos draudi ir nopietni, jo tā ir nežēlīgi ekspluatētā perifērija (piemēram, Ukraina) un daļējā perifērija (piemēram, Polija).

Kādam atliek tikai “sašūpot” situāciju, un šajā virzienā to spēj paveikt tikai Krievija.

Lai saglabātu sistēmu, Eiropas Savienība ir spiesta turpināt virzību uz austrumiem: piedalīties pārrunās ar Aleksandru Lukašenko, lai arī Baltkrievija nokļūtu ES ietekmes zonā; noturēt Ukrainu, kontrolēt tajā notiekošos procesus un atbalstīt Krievijai naidīgi noskaņotus spēkus.

Balkāni ir vēl viena “pulvera muca” Eiropas Savienībā, jo Balkānu valstu ekonomika ir sagrauta, to nācijas ir pazemotas. Arī grieķi.

No šejienes var sākties ES sabrukums, jo Ungārija būs tur, kur būs Balkāni, savukārt tur, kur būs Ungārija, būs arī Slovākija.

Domstarpības “vienotajā Eiropā”

— Pretrunas liecina, ka ES dalībvalstīm dāvātās priekšrocības nav pietiekamas ekonomikas un uzņēmējdarbības attīstībai tādās valstīs kā Itālija, Spānija un Francija. Beneficiāru loks pēdējos gados sašaurinās. Tomēr arī tagadējie beneficiāri pagaidām spēj kontrolēt pakļautās valstis un bloķēt iespējamo dumpošanos.

Eiropas vienotās armijas izveides plāni

— Eiropas vienotās armijas izveides plāns bija vien reklāmas pasākums. Labi, pieļausim, ka ES tiks apvienots zināms skaits armijas vienību. Kas no tā mainīsies? Cilvēki runā dažādās valodās, viņiem ir dažādu valstu pilsonība, izstrādātas atšķirīgas militārās nostādnes. Jā, var parādīties eirokrātijai pakļautas papildu militārās vienības.

Tāpēc patlaban šis jautājums nešķiet nopietns. Makrons to vienkārši izmantoja, lai uzsvērtu Francijas lomu Eiropā.

Tas bija viņa galvenais PR uzdevums, turklāt netika veikts par spīti Vācijai. Piemēram, jautājumā par “Ziemeļu straumi 2” Francija nostājās Vācijas pusē, tāpēc gāzesvada būvdarbi turpināsies.

Par Brexit ietekmi ES perifērijas valstīs

— Valstis perifērijā saņems mazākas naudas summas, daļa iedzīvotāju atgriezīsies no Lielbritānijas, kur devušies peļņā, tomēr liela daļa paliks Eiropā. Dažs labs pārvāksies uz Īriju, citi – uz kontinentu, jo viņi nebrauks uz mājām, lai dzīvotu nabadzībā.

Eiropas Savienība turpinās izsūknēt resursus no perifērijas, dumpji kļūs vēl pirmatnīgāki nekā “dzelteno vestu” akcijas Francijā.

Bet tagad iedomājieties, kas notiks austrumos, kur nav vērienīgu arodbiedrību, nav pat politisko organizāciju ar sociālo pieredzi, kādu guvuši franči. Iespējami dumpji, var nodegt policijas iecirkņi, taču ES tos apspiedīs.

Tad būs vienots tirgus, vienoti noteikumi, vienota muita, un nekādas segregācijas vai vietējās ražošanas iznīcināšanas.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 14 — id: `scraped:rubaltic_lt:d708bab703ce8fb4`

**Title:** Jurijaus Melio gatvė: naujas Lietuvos konsulato adresas taps kampanijos prieš Lietuvą pradžia

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Iniciatyva pavadinti gatvę, kurioje Kaliningrade darbuojasi Lietuvos generalinis konsulatas, Jurijaus Melio vardu nuskambėjo diskusijų klubo RuBaltic.Ru posėdžio metu ir susilaukė rezonanso regiono informacinėje erdvėje. Kaliningrado politikai ir visuomenės veikėjai palaiko idėją Proletarų gatvę pavadinti Jurijaus Melio vardu, tačiau pabrėžia, jog Lietuvos konsulato adreso pakeitimas turi tapti pirmąja ir kol kas švelnia priemone, perspėjančia Lietuvos valstybę, jei ji paskelbs kaltinamąjį nuosprendį akivaizdžiai nekaltam Rusijos piliečiui.

Iniciatyvą Proletarų gatvę pavadinti Jurijaus Melio vardu pateikė Kaliningrado srities dūmos deputatas, Kaliningrado jūrų prekybos uosto direktorių tarybos pirmininkas Andrejus Kolesnikas.

„Būtina Proletarų gatvę, kurioje name 133 darbuojasi Lietuvos konsulatas, pavadinti Jurijaus Melio vardu. Tegul jie ten pasimuisto, — pareiškė Kolesnikas diskusijų klubo RuBaltic.Ru posėdžio metu, kuriame buvo aptariamas Lietuvos politinio kalinio likimas. — Lai pagyvens Jurijaus Melio gatvėje. Tai reikalinga, kad žmonės neužmirštų, ką padarė, ir kiekvieną kartą, ateidami į darbą, suprastų, kad mes neužmiršime tų niekšiškų poelgių.“

Kolesniko pasiūlymas sukėlė Kaliningrade ažiotažą: jį citavo stambiausios regiono žiniasklaidos priemonės. Iniciatyvą su savo išlygomis ir pasiūlymais palaikė vietos politikai ir visuomenininkai.

„Žinoma, pritariu. Kodėl gi, pagaliau, ne? Mes turime priminti mūsų lietuviškųjų brolių — kaimynų valdžioms, kad jos negerai elgiasi. Lai tas jiems kasdien primins jų niekšybę. Todėl kad ta Lietuvoje siaučianti savivalė ir Jurijui Meliui gresiantis susidorojimas neturi likti be atsako“, — RuBaltic.Ru pareiškė Kaliningrado dūmos deputatas, srities regioninio LDAALR (ДОСААФ — Laisvanoriška draugija armijai, aviacijai ir laivynui remti) skyriaus pirmininkas Olegas Urbaniukas.

„Aš manau, jog kiekvienas turi atsakyti už savo veiksmus. Jeigu tų tolimų Vilniuje įvykių metu buvo nužudyti žmonės, tai atsakyti turi tas žmogus, kuris tiesiogiai juos nužudė arba įsakė nužudyti. Tačiau jokiu būdu ne tas žmogus, kuris sėdėjo savo tanke ir nieko nenužudė bei nesuluošino.Jei netgi įsivaizduoti, kad Melis pažeidė Lietuvos (tuo metu tarybinį) įstatymą, tai jis jau su kaupu sumokėjo beveik penkerių metų kalinimu Lietuvos kalėjime, ir tokia visas ribas viršijanti nuoskauda, kaip žinia, kelia pasipiktinimą“, — RuBaltic.Ru portalui baudžiamąjį Jurijaus Melio persekiojimą komentavo Kaliningrado srities žmogaus teisių įgaliotinis Vladimiras Nikitinas.

Jurijaus Melio bylos aplinkybės išties kelia pasipiktinimą.

Pirma, Rusijos kariuomenės atsargos pulkininkas už 1991 metų įvykius teisiamas pagal 2000 metų Lietuvos Baudžiamąjį kodeksą ir jo pataisas, priimtas 2010 metais specialiai dėl „Sausio 13-osios bylos“.

Antra, Melis, kurio Lietuvos prokuratūra lyg ir nekaltina ką nors nužudžius arba sužeidus, tampa atsakingu už 14 žmonių žūtį todėl, kad jis buvo vienu iš šimtų tarybinių kariškių, pasiųstų užimti strateginius Vilniaus objektus. Kolektyvinės atsakomybės principas šiuo atveju — viduramžių absurdas.

Trečia, kaltinimo neadekvatumas. Rusijos pilietis teisiamas pagal straipsnį „kariniai nusikaltimai ir nusikaltimai žmoniškumui“ ir reikalauja 16 metų kalėjimo už tai, kad 1991 metų sausio 13-osios naktį jis iš tanko triskart šovė tuščiomis ir švietė žibintais.

Ką jau kalbėti apie tokias praeities „smulkmenas“, kad Jurijus Melis kalinamas beveik 5 metus, tuo metu kai pagal Lietuvos ir Europos Sąjungos normas žmogus be nuosprendžio negali būti kalinamas virš 3 metų? Ką jau kalbėti apie moralinę klausimo pusę, kai vietoj teismo Gorbačiovui, įsakiusiam įvesti į Vilnių kariuomenės dalinius, „karaštutiniu“ daromas sunkiai sergantis atsargos karininkas, vykęs Lietuvon vaistų nuo diabeto?

„Aš palaikau pervardinimą gatvės, kurioje darbuojasi Lietuvos konsulatas, į Jurijaus Melio gatvę kaip vieną iš spaudimo Lietuvai elementų, — RuBaltic.Ru pareiškė visuomeninės organizacijos „Blaivios kartos“ prezidentas Valerijus Nesterovas. — Būtina visomis priemonėmis siekti Melio išlaisvinimo. Aš palaikau visas priemones, kurios buvo siūlomos jūsų diskusijų klubo posėdžio metu: neišduoti Lietuvos piliečiams vizų, įvesti embargą visoms lietuviškoms prekėms, nieko nepirkti iš Lietuvos ir nieko jai neparduoti. Viską darykime, kad tik ištrauktumėme Jurijų Melį. Mes turime už tai kovoti, nes jis ten bus numarintas.“

2017 metais Rusijos tyrimų komitetas iškėlė baudžiamąją bylą 26 Lietuvos teisėjams ir prokurorams, kurie atsakingi už Jurijaus Melio persekiojimą. Jie kaltinami pagal straipsnį „baudžiamosios bylos iškėlimas akivaizdžiai nekaltam asmeniui“.

Tai būsimų Maskvos veiksmų pradžia. Šiuo metu aptariamas klausimas dėl Lietuvos prokurorų paieškos tarptautiniu mastu, baudžiamosios 1991 metų sausio 13-osios įvykių Vilniuje bylos iškėlimas Rusijoje, baudžiamosios bylos iškėlimas Dėdulei Landsbergiui ir jo bendrams.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 15 — id: `scraped:rubaltic_lt:16f381c1c1294607`

**Title:** Žlugo Lietuvos energetikos politika: SGD terminalas ir naftos perkrovimas pergyvena didelį nuosmukį

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Šie metai Lietuvai prasidėjo didžiuliu rodiklių transporto ir energetikos sferoje nuosmukiu. Valstybinė kompanija Klaipėdos Nafta raportuoja, jog suskystintų gamtinių dujų terminalo Klaipėdoje pelnas sumažėjo 16 proc. Lietuvos energetikos politika žlugo vienu metu keliomis kryptimis: iškart pasireiškė daugiametės kovos dėl „energetinės nepriklausomybės“ pasekmės.

Klaipėdos Naftos spaudos tarnyba praneša, kad kompanijos pelnas pakraunant naftos produktus Klaipėdos uosto Butingės terminale ir Subačio kuro bazėje pirmąjį šių metų mėnesį sumažėjo 26 proc. Tokį sumažėjimą galima drąsiai pavadinti griūtimi.

Sausio mėnesį Klaipėdos Nafta pakrovė 626 tūkstančius tonų naftos produktų, o tai 19 proc. mažiau, nei praeitų metų sausio mėnesį, kai buvo pakrauta 776 tūkstančiai tonų naftos produktų. Rodiklių mažėjimo priežastimi laikomas tiekimo apimčių iš Mažeikių naftos perdirbimo įmonės (Orlen Lietuva) ir naftos tranzito sumažėjimas.

Pirmasis skambutis Lietuvai nuskambėjo dar praeitų metų vasarą, kai bendrų gyvybiškai sėkmingų Klaipėdos uosto krovinių apyvartos rodiklių fone nemaloniu disonansu nuskambėjo naujiena, jog per pusmetį naftos produktų perkrovimo apimtys sumažėjo 2,7 proc.

Tuo metu Minskas jau buvo sutaręs su Maskva dėl milijono tonų baltarusių naftos tranzito nukreipimo iš Pabaltijo į Rusijos uostus. Baltarusijos URM vadovas apsilankė Rygoje, kad aptartų baltarusių eksportuotojų bendradarbiavimą su Latvijos uostais, o Baltarusijos ambasadorius Lietuvoje užsiminė, kad baltarusių įmonės pastoviai sulaukia

įdomių Rusijos uostų pasiūlymų. Galėtų Lietuvos valdžios suprasti tas užuominas, tačiau nuo begalinės kovos su „rusų grėsme“ atbuko jų smegenys.

Sekantį kartą jau ne skambutis, o perkūno trenksmas Klaipėdoje pasigirdo rugsėjo mėnesį, kai Baltarusijos prezidentas Aleksandras Lukašenka tiesiai pareiškė, kad jei Lietuvai nereikia gerų kaimyninių santykių su Minsku, baltarusiai bendradarbiaus su Latvija.

„Jūs suprantate, mes neprieiname prie jūros, ir jeigu Lietuva nelabai nori su mumis bendradarbiauti, kalbėkimės su Latvija“, — pasakė Lukašenka naujam baltarusių ambasadoriui Rygoje ir pavedė jam paversti Latviją jūrų uostu baltarusių eksportui.

Galbūt, Lietuvos valdžioms dar nebuvo vėlu apsigalvoti ir nutraukti savo beprasmę kovą su Baltarusijos AE, kovą, kuri niekaip negalėjo užblokuoti atominės elektrinės statybos, užtat galėjo rikošetu paliesti Lietuvos ekonomiką.

Jos nė valandėlei nesustabdė šios kovos, todėl nereikšmingą pernykštį naftos tranzito sumažėjimą pakeitė esminė šiuometinė griūtis.

Beje, blogos Klaipėdos Naftos naujienos tuo nesibaigia. Ši valstybinė kompanija yra dar ir Klaipėdos SGD terminalo savininkė. Pastarasis taip pat kelia problemų.

Praeitais metais Lietuvos valdžios džiūgavo, jog išpirks Independence iš norvegų kompanijos, tuo lyg atsakydamos į visus priekaištus, jog SGD terminalas brangus ir neefektyvus. Logika paprasta: jei perkam, vadinasi, jis efektyvus ir nebrangus. Negi mes pirktumėm nenaudingą ir nesėkmingą projektą?

Nepaprieštarausi.

Klaipėdos Nafta dievagojasi, prieš susirėmimą meta kovinį gorilos patino šauksmą ir pareiškia, jog pasiruošusi tapti stambiausia Europos SGD rinkoje operatore; o tuo metu jos pajamos šių metų sausio mėnesį krito 21 proc.

Kompanijos menedžeriai išdidžiai pareiškia, jog ateityje lietuviškąja infrastruktūra naudosis stambiausios vakarų kompanijos, kurios į SGD rinką ateis Centrinės ir Rytų Europos regione. Tačiau kol kas Independence paslaugų atsisakė net Latvija su Estija, kurioms pagrindinai terminalas ir buvo statomas. Lietuvos SGD terminalas taip ir nesulaukė regioninio statuso; kaimynai jo produkcijos neperka, todėl Europos Sąjunga Klaipėdos geldos išlaikymui lėšų neskiria.

Norvegų plaukiančiojo laivo išpirkimas pateikiamas kaip “enrgetinės nepriklausomybės“ sėkmės liudijimas, ir tuoj pat skamba visiškai prieštaraujantis pagal prasmę argumentas šio pirkimo naudai: taip Lietuva galės sumažinti išlaidas jo išlaikymui.

Beje, 6 milijonais per metus mažiau mokės pagrindinė Independence produkcijos šalyje vartotoja — kompanija Achema, kuriai „energetinė nepriklausomybė“ tapo tokiu „naudingu“ projektu, kad jos vadovybė praeitais metais kategoriškai atsisakė pasirašyti ilgalaikį suskystintų gamtinių dujų iš Klaipėdos tiekimo kontraktą.

Achema su liūdesiu pareiškė, jog SGD terminalo muitas kels bankroto grėsmę. Į tai vyriausybėje buvo paprieštarauta, jog alternatyvus „Gazpromui“ energijos šaltinis labai naudingas — muša dujų kainas. Ir bendrai, kaip išsireiškė energetikos ministras, atsakydamas laimingiems terminalo produkcijos vartotojams, „mes negalime imti ir permesti terminalo naštą nuo vienų vartotojų pečių ant kitų“.

Taip kad net Lietuvos valdžių pareiškimuose sėkmingos, ekonomiškai naudingos energetikos srityje politikos vaizdai nesudaro vientiso, viduje nekeliančio prieštaravimų pavidalo.

Du iš trijų jos pastarųjų metų simbolių: Klaipėdos SGD terminalas ir kova prieš energiją iš Baltarusijos AE tapo priežastimi vieno iš pagrindinių Lietuvos mokesčių mokėtojų — valstybinės Klaipėdos Naftos rodiklių mažėjimo.

Trečias simbolis — pasitraukimas iš energijos žiedo BRELL (Baltarusija, Rusija, Estija, Lietuva, Latvija) — paskutinį kartą save priminė tuo, jog atsijungimo nuo BRELL bandymas buvo perkeltas iš šių metų vasaros nenumatytam laikui. Elektros kabelis Nord Balt eilinį kartą išėjo iš rikiuotės, o už naujo elektros kabelio paklojimą lietuviai sumokės elektros energijos tarifų augimu.

Jei visa tai vadinasi „energetinės politikos sėkme“, tai ji kažkokia ypatinga, lietuviška sėkmė. Panašios „sėkmės“ visame likusiame pasaulyje vadinamos griūtimis.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 16 — id: `scraped:rubaltic_lt:ed93e06a723d2bf3`

**Title:** Optimizmas pasibaigė, neprasidėjus: Pabaltijį vėl palieka žmonės

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos ir Latvijos statistikos žinybos ir demografai vėl kalba apie Pabaltijo tautų išmirimą. Mirtingumas auga, gimstamumas krenta, lietuviai ir latviai išsilaksto po užsienius ir neketina sugrįžti į tėvynę. Kalbos apie demografinės situacijos gerėjimą Pabaltijo šalyse pasireiškė kaip priešlaikinės: Pabaltijo politikai apie tai kalbėjo pernai, nenorėdami sudrumsti Lietuvos, Latvijos ir Estijos šimtmečių švenčių — šių valstybių vis dar atsisako etniniai gyventojai.

Lietuvos statistikos departamentas praneša, jog respublikos gyventojų skaičius pernai sumažėjo 14,5 tūkstančio žmonių. Per pirmąjį šių metų mėnesį gyventojų skaičius sumažėjo 2 tūkstančiais žmonių. Šiandien Lietuvoje oficialiai gyvena 2,7 milijono žmonių — beveik milijonu mažiau, nei 1991 metais gyveno Lietuvos TSR.

Faktiškai šis skaičius dar mažesnis, nes neįskaito tų emigrantų, kurie išvyksta į Vakarų Europą nedeklaruodami savo išvykimo. Manoma, jog šiuo metu vargu ar Lietuvoje yra 2,5 milijono gyventojų, be to, jų skaičius pastoviai mažėja.

O iš tiesų Lietuvos gyventojų skaičius mažėja daug sparčiau, negu skelbia oficialios įstaigos. Statistikos departamento apskaičiavimai pastoviai optimistiški, ir sunku suprasti, kodėl tvirtinama, jog išvykę svetur uždarbiauti sugrįš.

O tuo tarpu pernai iš Lietuvos išvyko 32 tūkstančiai gyventojų. Tai mažiau, nei ankstesniais metais, tačiau mažai šaliai ir toks skaičius grėsmingas.

Lietuviai blaškosi Didžiojoje Britanijoje, Vokietijoje, Norvegijoje, Airijoje. Apie jų požiūrį į tą tėvynę, su kuria atsisveikino, byloja tai, jog britų imigrantai pasiryžę atsisakyti Lietuvos pilietybės ir po Brexit priimti britų. Siekdamos užkirsti kelią tokiam nemaloniam, reputaciją žeidžiančiam smūgiui, Lietuvos Respublikos valdžios nori įteisinti dvigubą pilietybę.

“Aš galiu palyginti mūsų gyvenimo lygį su mūsų artimųjų Lietuvoje gyvenimo lygiu: jiems tenka dirbti keliose vietose, kad šiek tiek uždirbtų. Kai mes atvykstam į Lietuvą ir matom kainas, patiriam šoką. Anglijoje gal ir brangu, gyvenimas nelengvas, tačiau tu dirbi, ir tavo darbas vertinamas. Dirbi ir uždirbi”, — Lietuvos žiniasklaidai pasakoja Gintarė, atsisakiusi Lietuvos pilietybės dėl gyvenimo Didžiojoje Britanijoje. “Išties mes jau daug metų galvojome apie pilietybės pakeitimą. Apie 10 metų. Mes neplanavome sugrįžti į Lietuvą”, — aiškina Gintarė.

Pagal Lietuvos URM informaciją, tokių žmonių, kaip Gintarė, pernai buvo 155.

Panašus požiūris į gimtąjį kraštą ir kaimyninėje Latvijoje. Sociologų duomenimis, kas trečias jaunas latvis šalyje”sėdi ant lagaminų”, pasiruošęs išvykti iš Latvijos artimiausiu metu. Esant dabartiniams jaunimo emigracijos tempams, amžiaus viduryje 60 proc. šalies gyventojų bus per 65 metus.

Iš Latvijos dažniausiai išvyksta jauni vyrai. Užsienyje latviai dažniau, nei tėvynėje, sukuria šeimas, pagimdo vaikus. Emigruoja labiau išsilavinę žmonės, Latvijoje lieka mažiau išprusę. Užsienyje aukštos kvalifikacijos latvių specialistai dirba tose šakose, kuriose Latvijoje kritiškai trūksta specialistų. Inžinieriai, gydytojai.

Ir taip pat, kaip lietuviai, išvykę latviai neskuba sugrįžti į tėvynę. Pagal latvių apklausą šimte pasaulio šalių, tvirtai pasiryžę sugrįžti į Latviją 16 proc. išvykusių. Dar 40 proc. sugrįš, jei situacija šalyje pagerės, likusi dauguma išvis nenusiteikusi grįžti.

Tačiau depopuliaciją Pabaltijo šalyse sukelia ne tik emigracija.

Gimstamumas Lietuvoje lyginant su praeitais metais krito 9,6 proc. Mirtingumas išaugo 2,5 proc. Susituokiama rečiau negu išsiskiriama.

Tokie pat liūdni skaičiai ir Latvijoje, kurios šimtmetis buvo pažymėtas gimstamumo antirekordu. Centrinė statistikos valdyba pareiškia, jog nuo praeitų metų sausio iki lapkričio šalyje gimė 17800 vaikų. Tai 7,5 proc. mažiau nei 2017 metais. O gruodyje buvo pasiekta absoliutaus mėnesio gimstamumo antirekordo visos stebėjimų istorijos metu — 1292 kūdikiai.

Gimstamumas Latvijoje krenta keletą metų iš eilės, mirtingumas ženkliai jį viršija. Tokiu būdu Latvija patenka į dešimtuką pasaulio šalių, kuriose sparčiausiai mažėja gyventojų skaičius.

“Šia tema egzistuoja geras anglų išsireiškimas Wishful thinking — tai yra kai mes galvojame taip, kaip norisi galvoti, kai norus įsivaizduojame išsipildžiusius, — pareiškimus apie Latvijos migracijos balanso pagerėjimą komentuoja Latvijos universiteto profesorius, demografas Michail Chazan. — Nepaisant to, jog ekonominė situacija gerėja, atsiranda vis daugiau galimybių įsidarbinti gerai apmokamame darbe kai kuriose šakose, o vidutinis darbo užmokestis pasiekė psichologinį 1000 erurų barjerą, Latvija dar negali laukti migracijos stebūklo. Nemanau, kad iš didelio minuso mes staiga iššoksime į nulį. Juk dauguma faktorių, skatinančių žmones išvykti, niekur nedingo.”

Demografinės situacijos Pabaltijyje gerėjimo iliuzija atsirado tik dėl to, jog į jį uždarbiauti be vizų atvyko ukrainiečiai. Pasirodžius jų srautui, atrodė, jog mažesniais tempais ėmė mažėti gyventojų skaičius ir ne toks dramatiškai didesnis išvykstančių iš Lietuvos ir Latvijos, nei atvykstančių, gyventojų skaičius.

Pabaltijo politikai žinojo, kad tai iliuzija, žinojo, dėl ko ji atsirado, tačiau savo valstybių šimtmečio proga sąmoningai klaidino žmones ir tvirtino, jog viskas pasikeis.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 17 — id: `scraped:rubaltic_lt:bdd3e695bc144ba7`

**Title:** 8 Pabaltijo koviniai būdai: kaip Pabaltijo šalys ruošiasi karui su Rusija

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Karo su Rusija atveju Estijos vyriausybė ruošiasi konfiskuoti savo piliečių automobilius. Estijos gynybos resursų departamentas jau sudarė sąrašą maždaug 2700 transporto priemonių, kurių savininkai privalo perduoti juos valstybei, jeigu respublikoje bus paskelbta ypatingoji padėtis. Kaip apsaugos Estiją nuo „rusų įsiveržimo“ piliečių transportas, galima tik spėlioti, tačiau panašios iniciatyvos Pabaltijyje pasireiškia reguliariai. Analitinis portalas RuBaltic.Ru surinko 8 atkirčio rusų agresijai receptus, sugalvotus Pabaltijo respublikose karo su Rusija atveju.

1. Apsirūpinti kariais

2015 metais Latvijos vidaus reikalų ministerija parašė gyventojams rekomendacijų projektą karo pradžios atveju. Latviai raginami pasitraukti iš pavojingų vietų su iš anksto surinktu krepšiu, kuriame turi būti reikalingiausi daiktai, tame tarpe kirviai.

O kad agresoriai būtų greičiau nugalėti, respublikos piliečiai turi būti budrūs ir pranešinėti teisėsaugininkams apie įtartinus asmenis, kurie kuo nors skiriasi nuo vietos gyventojų. Arba apie tuos, kurie šalį pasiekė desantu oru arbas jūra.

Tinklalapyje buvo juokaujama, kad karo atveju latviams siūloma pasiimti kirvius ir keliauti prie kranto linijos: gal statyti plaustų ir „dingti iš šalies“, gal taip atbaidyti priešą. Kas gi surizikuos pulti Latviją iš jūros, jeigu juos pasitiks kirviais apsiginklavusi kariuomenė?

2. Viliamasi Dievu

Lietuvos krašto apsaugos ministerija karo pradžios su Rusija atveju viliasi, jog padės Aukščiausiasis. Tiksliau, jo tarnai: paruošta įstatymo pataisa dėl karo prievolės siūlo visuotinos mobilizacijos metu imti kariuomenėn dvasininkus.

Lietuvos vyskupų konferencija šias pataisas palaikė.

3. Išplėsti partizaninį judėjimą

Dėl galimos „rusų agresijos“ Lietuvoje pilnu tempu vyksta partizanų ruošimas. Apie tai skaitytojams papasakojo The Time žurnalistas Tom Parfit, kuris, Šaulių sąjungos pakviestas, stebėjo, kaip apmokomi jos šauliai savanoriai. Suprasdami, jog Lietuvos kariuomenė prieš Rusijos karo mašiną neatsilaikys, šauliai ketina pasinaudoti „miško brolių“ patirtimi — mušti maskolius lengvai apginkluotų mobilių nereguliariosios kariuomenės dalinių jėgomis.

Šaulių štabe žurnalistui papasakojo, jog po 2014 metų įvykių organizacijos narių skaičius ženkliai ūgtelėjo. Tame tarpe pasipildo ir jaunasis sparnas. Žodžiu, karo pradžios atveju pakilti su ginklu rankose bus pasiruošę ir senas, ir mažas.

„Mes kalbame apie tai, kad šauliai ir savanoriai sugebės savomis priemonėmis prisijungti prie mūsų valstybės gynybos, o būtent — įsigyti pusiau automatinį ginklą, — iniciatyvą komentavo Sąjungos narys Robertas Juodka. — Tokiu būdu mes didiname sulaikymo potencialą, nes galimas priešas nežinos tikslaus skaičiaus piliečių, kurie turi ginklą ir sugebės pasipriešinti. Tuo padidėja ir mūsų valstybės gynybos potencialas“.

4. Išmokyti kariauti vaikus

Kariniam patriotiniam augančiosios kartos auklėjimui Pabaltijyje skiriamas didelis dėmesys: vaikai nuo vaikystės turi žinoti, kas jų priešas ir kaip jam pasipriešinti. Lietuvoje šiuo klausimu užsiiminėja jau minėta Šaulių sąjunga, Latvijoje — šauktiniai „Zemessardze“, Estijoje — Gynybos sąjunga „Kaitselijt“.

„Tarp paramilitarinių būrių — baikeriai, buvę kareiviai, medžiotojai ir gyvulininkystės darbuotojai, — įspūdžiais to, ką matė Pabaltijyje, žurnale The Atlantic dalinosi Siddehartcha Machanta. — Kiekviena grupė turi savo dalinį, kuris moko jaunus vyrus ir moteris karo taktikos ir patriotiškumo, kai kuriems savanoriams tik 12 metų. Šios grupės teigia, kad jų nedomina politika. Jos siekia apginti savo sienas ir apmokyti rytdienos karius, kad pasiruoštų pasitikti tai, ką jiems paruošė Putinas“.

Ką gi, kaip rodo RF uždraustos Islamo valstybės patirtis, vykdydami kai kurias kovines užduotis ir nesukeliantys įtarimų vaikai gali būti naudingesni nei suaugę kariai. Tad kodėl ir juos nepanaudoti tautos gelbėjimo „dieviškajam“ reikalui?

5. Slėptis mobiliose slėptuvėse

Estijoje sugalvojo gana nepaprastą išsisaugojimo nuo bombardavimo būdą: slėptis transportuojamuose požemio bunkeriuose, kuriuos prieš keletą metų nutarė gaminti Terramil firma.

Slėptuvę, kuri kainuoja maždaug 20 tūkstančių dolerių, galima pastatyti tik per 90 minučių ir paslėpti joje 12 žmonių. Atrodytų, labai praktiška, tačiau ypatingos paklausos Terramit bunkeriai nesusilaukė. Yra žinoma, jog Estijoje firmos įkūrėjas Krist Kirs vedė derybas su kitų šalių potencialiais piekėjais.

6. Įpareigoti piliečius priešintis agresijai

Praėjusių metų pradžioje Latvijoje buvo paruoštos pataisos įstatymų, įpareigojančių visus šalies piliečius priešintis agresoriui kovinių veiksmų pradžios atveju ir remti reguliarią kariuomenę.

Kad tai nepasikartotų, būtina keisti įstatymus.

„Todėl dabar, jeigu staiga atsitiks kažkas absoliučiai nerealaus ir mes prarasime vyriausiąją vadovybę, kareiviai ir jų tiesioginiai vadai neprivalės laukti kokių nors įsakymų, kad pradėtų kovą už suverenumo išsaugojimą“, — tvirtina Kalninš. Jo manymu, yra dar vienas svarbus įstatymo pataisų aspektas: jos pavers karių veiksmus kovojant su agresija visiškai teisėtais, ir nė viename tarptautiniame teisme žmogų esą negalės teisti už jo nepaklusnumo akcijas.

Tačiau ne visi Latvijoje pritaria Kalninš entuziazmui. „Kol kas pataisos, kurias nacionalinės gynybos įstatymui pateikė Gynybos ministerija, man atrodo lyg tai būtų komanda mobilizuoti reikiamu momentu patrankų mėsą, kad savimi apgintų valstybę, o valdžia tuo metu turėtų galimybę susikrauti į lagaminus mantą ir pasislėpti saugesnėse vietose“, — pažymėjo publicistas Viktoras Avotinš.

7. Pasitelkti pagalbon emigrantus

Iš visko sprendžiant, Latvija karo atveju pasikvies pagalbon didžiulį būrį savo emigrantų, kurie įsikūrė Vakarų Europoje. Kitose šalyse gyvenantys rezervistai šiandien gauna kvietimus atvykti į karo stovyklos vietą ir dalyvauti mokymuose. Tiesa, atitrūkti nuo darbo (kad ir laikinai) sutinka toli gražu ne visi. Gal karo pradžios atveju jų prioritetai pasikeis?

8. Mobilizuoti rusų rezervistus

Estijoje būtų galima pasiųsti į frontą rusakalbius rezervistus — net tuos, kurie nemoka estų kalbos. Įsakinėti jiems planuojama anglų kalba. Kaip sklandžiai bus koordinuojami karo veiksmai, nesunku nujausti.

Neveltui Estijos Konservatyviosios liaudies partijos pirmininkas Mart Chelme perspėjo tėvynainius, kad apie 5000 gerai paruoštų ir apmokytų „jaunų rusų žmonių“ jo šalyje neva pasiruošę kautis prieš valstybę. Ir po to juos mesti mūšin rytų fronte?

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 18 — id: `scraped:rubaltic_lt:6bd04e1f974357b3`

**Title:** Kovokite už mus: Didžioji Britanija pateikia teises Lenkijai ir Pabaltijui

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Didžiosios Britanijos premjerė Tereza Mej nori pareikalauti iš Lenkijos ir Pabaltijo šalių, kad jos įtikintų Europos Sąjungą būtinybe minkštinti Brexit. Iš britų premjerės pusės tai daugiau nei nevilties mostas. Londonas primena savo šimtametę geopolitinę Rytų Europos globą ir iš šefuojamo regiono vyriausybių reikalauja atsakomosios paslaugos: būti Europos Sąjungoje britų agentais.

Britų leidinys Daily Mail praneša, kad valstybės vadovė Tereza Mej ketina kreiptis į Pabaltijo šalis su prašymu įtikinti kitas ES šalis, kad jos atsisakytų remti Airiją jos derybose dėl Didžiosios Britanijos pasitraukimo iš Europos Sąjungos sąlygų.

Pagal Daily Mail informaciją, Tereza Mej tikisi prikalbinti Pabaltijo šalis (prie kurių laikraštis priskiria ir Lenkiją) užstoti Britaniją ir skatinti Briuselį atnaujinti derybas dėl Brexit sąlygų.

Įdomus ponios premjerės argumentavimas: kodėl visoje „Vieningoje Europoje“ pagalbos ji nori prašyti Lenkijos ir Pabaltijo?

Londonas jau konsultuojasi su Prancūzija ir Vokietija naujų derybų galimybių dėl Brexit sąlygų klausimu. Paryžius ir Berlynas niekaip nenusileidžia — susitarimas svarbiau nei pinigai, taip kad vykdykite esantį susitarimą. Briuselio pozicija tokia pat bekompromisinė: Europos komisijos vadovas Žan-Klod-Junker į visus Terezos Mej naujų derybų prašymus atsakė, jog susitarimas dėl Didžiosios Britanijos pasitraukimo iš ES pasirašytas ir peržiūrimas nebus.

Britų vyriausybė pasimetusi. Jos Didenybės parlamentas iškart prabalsavo už tai, kad iš Europos Sąjungos nebūtų pasitraukta be derybų, ir už tai, kad nesitraukti iš Europos Sąjungos pagal pasirašytą susitarimą. Jis taip pat uždraudė perkelti Brexit datą iš kovo 29 dienos, kurią numatytas Didžiosios Britanijos pasitraukimas iš ES.

Terezos Mej padėtis šioje situacijoje nepavydėtina. Kur nepažvelgtum, visur ne taip. Brexit gali „nukirsti“ Jungtinės Karalystės politinės sistemos ir ekonomikos „srieges: šiuo metu anglai, panikuodami, laukia Šiaurės Airijos separatizmo bangos ir ruošiasi evakuoti karalienę.

Pagalbos kreipimasis į Lenkiją ir Pabaltijį dėl to gali pasirodyti kaip kritiškos nervų įtampos pasiekusios moters nevilties mostą. Bet taip atrodo tik iš pirmo žvilgsnio. Terezos Mej ketinimai objektyviai išplaukia iš visos Britanijos imperijos sąveikos su Rytų Europos šalių patirtimi.

Šiandieninis Rytų Europos amerikiečių protektoratas perėmė tarpukario britų protektoratą. Tarpukario Lenkija — Antroji Tautų Respublika (ATR) — orientavosi į europietišką politiką ir, pirmiausia, į Britanijos, priimdama ją kaip pagrindinę sąjungininę kaip prieš Vokietiją, taip ir prieš TSRS.

Šiuo metu valdančiosios partijos „Teisė ir teisingumas“ užsienio politikos koncepcija šia prasme skyriasi perimamumu su Pilsudskio epocha: ji taip pat numatė Lenkijos ir Didžiosios Britanijos sąjungą, siekiant kartu priešintis Vokietijos Europos Sąjungoje dominavimui. Visuotinas britų pageidavimas pasitraukti iš ES, žinoma, tapo Varšuvai labai nemaloniu netikėtumu.

Iš Pabaltijo šalių, pasaulio politiniame žemėlapyje atsiradusių pagal Pirmojo pasaulinio karo rezultatus, pirmiausia būtent Londonas sukūrė „sanitarinį kordoną“, užkertantį bolševizmo patekimo į Europą kelią. Naujai sukurtos Lietuva, Latvija ir Estija turėjo atkirsti Rusiją nuo Europos, tapti pastoviu smulkiu kliuviniu Rusijos su Vokietija bendradarbiavime ir neleisti joms kartu įveikti liūdnas karo pasekmes.

Čia taip pat matosi perimamumas šia diena.

Ji palaikė visas pabaltijiečių kalbas apie „rusų grėsmę“, pasiuntė į Pabaltijį savo kariuomenę, pirmoji rėmė visas antirusiškas Lietuvos, Latvijos ir Estijos iniciatyvas: sankcijas, Trečiąjį energijos paketą ir t.t.

Britų įtaka Pabaltijo respublikų vidaus politikai savo mastais nusileidžia tik amerikiečių. Paskutinieji pavyzdžiai: britų žvalgybos ir gynybos fondas ištyrė Pabaltijo rusų nuotaikas, ir Didžiosios Britanijos ambasada Taline pakvietė estų valdininkus susipažinti su tyrimų rezultatais ir išklausyti britų patarėjų rekomendacijų.

Kur dar galima įsivaizduoti tokią situaciją: užsienio žvalgyba atvirai renka informaciją apie tautinių mažumų nuotaikas, o ambasadorius iškviečia tarnautojus valstybės, į kurią jis nukreiptas, pas save „ant kilimo“? Britų–pabaltijiečių santykiuose štai dar kas pasitaikė: 2004 metais Jos Didenybės pilietis Janis Kažocinš tapo latvių kontržvalgybos vadu, jam suteikiant teisę disponuoti Latvijos valstybės paslaptimis, neatsisakant britų paso.

Tokie paradoksai tarptautiniuose santykiuose paaiškinami kaip sena britų tradicija įtakoti pabaltijiečių reikalus, taip ir įtaka Pabaltijui JAV, kurioms debesuotasis Albionas ne tik pagrindinis sąjungininkas Europoje, bet ir protėvių tėvynė.

Tačiau Brexit verčia britus susimąstyti dėl naujų žaidimo taisyklių.

Terezos Mej raginimas, adresuotas Pabaltijo sąjungininkams, paremti Britaniją Europos Sąjungoje ir pasisakyti už naujas derybas dėl Brexit sąlygų turi tapti pirmuoju žingsniu link šios strategijos.

Britų valdžios, spaudos pranešimais, jaudinasi, kad jų argumentas, „ginant nuo rusų agresijos“, bus suprastas kaip grasinimas išvesti iš Pabaltijo Jungtinės Karalystės kariuomenę ir atiduoti lietuvius, latvius ir estus Putino sudraskymui. Tačiau bijoti jiems reikia kitko.

Didžiosios Britanijos, kuri trenkė durimis ir pasitraukė iš ES, interesų rėmimas kelia pavojų pabaltijiečių politikams, tikintiems gauti Europos komisijoje aukštų postų. Kaip ir santykiuose su Jungtinėmis Amerikos Valstijomis, Vilniui, Rygai ir Talinui iškils dvigubo lojalumo problema.

Vargu ar šis klausimas bus išspręstas Londono naudai.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 19 — id: `scraped:rubaltic_lt:3b90866d7f6f04f9`

**Title:** Per merginą pervažiavo tankas — lūžių nenustatyta: melas apie 1991 metų sausio 13-osios įvykius Lietuvoje

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvių chirurgas Kęstutis Vitkus sausio 11 dieną davė interviu kažkokiai Evelinai Ustinavičiūtei. O sausio 12 dieną jis apsireiškė Lietuvos TV ekranuose fone prie Seimo pastato liepsnojančių laužų ir papasakojo, kaip 1991 metų sausio 13-osios naktį sandėliavo žuvusių prie Vilniaus televizijos bokšto lavonus ligoninėje po laiptais, o paskui nukentėjusiems siuvo rankas ir kojas. Vitkaus pasakojimas — parodymai kaltinimo, kuris turi patvirtinti tarybinių kariškių kaltę sausio 13-osios naktį žudant žmones. Tačiau chirurgo liudijimai — melas nuo pradžios iki galo (tęsinys. Pradžia čia ).

Taigi paanalizuosime Vitkaus prisiminimus. Jis papasakojo apie Kęstutį Briedelį, kuris neva patyrė daug sužalojimų nuo tanko patrankos tuščio šūvio.

„Jis nukentėjo nuo pirmųjų tankų patrankų šūvių. Visas apdegęs, veidas smarkiai pajuodavęs paraku, lyg keptuvė išpaišytas, plaučiai atmušti, nepajėgia kvėpuoti, trachėjoje vamzdelis, atitrūkusi tinklainė — nieko nemato, visiška kontūzija, visur kraujas. Suprantu, kad man nėra kas veikti...”

Iš šių žodžių reikia suprasti, jog chirurgas Vitkus priėjo išvados, kad Briedelio laukia neišvengiama mirtis, ir paliko jį be pagalbos. Tačiau žinoma, jog jis liko gyvas!

Oficialiais duomenimis, kuriuos Lietuvos prokurorai 1991 metais pranešė tarybiniams kolegoms, sausio 13-osios naktį 48 žmonės buvo sužeisti šaunamasiais ginklais, 550 pareiškė patyrę akustines traumas nuo tankų patrankų tuščių šūvių.

Tanko patrankos tuščias šūvis sukelia 140 decibelų garsą. Ausų membrana plyšta tik tankų patrankoms šaudant koviniais užtaisais, kurių sukeliamas garsas — apie 210 decibelų. Nuo tokio šūvio tikrai gali plyšti ausų membrana, jei žmogus stovi greta tanko. Tačiau tokių šūvių prie televizijos bokšto ir Lietuvos radijo ir televizijos (LRT) pastato nebuvo.

Medicina dar neturi prietaiso, kuriuo būtų galima nustatyti žmogaus apkurtimo laipsnį. Čia svarbiausia faktas, kaip žmogus girdi arba negirdi.

Užtat 550 1991 metų mitingo prie televizijos bokšto dalyvių pareiškė Lietuvos gydytojams, kad jie pradėjo blogai girdėti. O 2012 metais tokių apkurtusių žmonių skaičius jau siekė tūkstantį.

Kaltinamajame akte pranešama: „A“ grupės kariškiai, prie LRT radijo pastato panaudoję šviesos garsinius sprogstamuosius užtaisus, Briedelį smarkiai suluošino: plėštinės žaizdos ir veido, odos, krūtinės, pilvo ir gaktos, klubų ir blauzdų, rankų plaštakų sumušimai su veido odos impregnavimu suodžiais (paraku) ir galvos plaukų nudegimais...“

Tai yra Vitkus net nepatikslino, nuo ko Briedelis patyrė tiek traumų. Puikus chirurgas!

Yra žinoma, jog „Alfos“ kariai buvo apginkluoti šviesos garsinėmis granatomis. Bet jos buvo gaminamos ne tikslu mechaniškai skeveldromis nukauti priešą, o jį neutralizuoti padarant akustinį (garsinį) ir šviesos poveikį, dėl ko žmogus patiria šoką.

Toks užtaisas akivaizdžiai sprogo greta Briedelio, dėl ko jis patyrė daugybę traumų. Yra žinoma, jog LRT radijo pastato prieangyje savadarbis sprogstamasis užtaisas sprogo po Alvydo Kanapinsko striuke. Ir sprogo jis tarp striukės ir megztinio. Tai buvo gerai matoma nuotraukoje, kai Kanapinskas lavoninėje buvo nurengiamas. Kanapinsko striukės skivytai buvo nukreipti į viršų, o megztinio gabalai įsprausti į žaizdą krūtinėje.

Tas nuotraukas tardytojas R.Judickas rodė draugovininkui Aleksandrui Bobyliovui, apkaltintam Kanapinsko nužudymu. Kai šis argumentuotai paaiškino Judickui, kad nuotraukos patvirtina jo nekaltumą, jos tuoj pat dingo iš Bobyliovo ir kitų įtariamųjų baudžiamųjų bylų medžiagų.

Tokio savadarbio sprogstamojo užtaiso aukomis prie keturių aukštų LRT radijo pastato tapo ne tik Briedelis ir Kanapinskas, bet ir kapitonas desantininkas Jevgenijus Gavrilovas. Pastarasis, sprogus savadarbiam užtaisui, vos neprarado kojos.

Yra žinoma, jog du tokius užtaisus lietuviškieji kariūnai susprogdino televizijos bokšte. Keli tokie nesprogę užtaisai ten buvo aptikti. Tai akivaizdus liudijimas, jog sausio įvykių išvakarėse kariūnai gamino savadarbius užtaisus.

Loreta Asanavičiūtė

Paskui Vitkus prisiminė Loretą Asanavačiūtę, kuri į „Raudonojo kryžiaus“ ligoninę buvo atvežta viena iš pirmųjų:

„Paliečiau kojas — oda apdegusi, ant jų tanko vikšrų pėdsakai. Tada paliečiau dubens dalį, o ten lyg kruopų maišas — ją visiškai sutraiškė vikšras. Ji dar kalbėjo, pasakė adresą. Sušnabždėjo: „Ar aš gyvensiu?“ Aš supratau, kad jos pilvas sutraiškytas ir kad jos niekas neišgelbės. Klaikus organizmo šokas, vidinis kraujavimas. Kuo daugiau įpilti skysčio, kraujo pakaitalo, tuo labiau kris spaudimas, ji uždus ir numirs. Loreta numirė.“

Karo lauko chirurgas Vitkus pareiškė, jog Asanavičiūtės kojos buvo apdegusios ir ant jų matėsi tanko vikšrų pėdsakai. O štai ant Loretos klubo sąnarių, per kuriuos neva pervažiavo 58 cm pločio tanko vikšras, to vikšro pėdsakų Vitkus nepastebėjo. Tačiau, palietęs dalį dubens, jis suprato, jog ta dalis —lyg kruopų maišas.

Prieš savo interviu Vitkui vertėjo pažiūrėti Broniaus Talačkos vaizdo filmą, kuriame Asanavičiūtę matome „Raudonojo kryžiaus“ ligoninės priimamajame, kai jos kūnas nuo palatos lovos buvo perkeliamas ant vežimėlio, kuriuo turėjo būti nugabentas į lavoninę. Loretos kūnas anatomiškai buvo visiškai sveikas, be jokių tanko vikšrų pėdsakų.

Ant merginos klubų tik matėsi kruvini plėštiniai įdrėskimai — žaizdos nuo galų trūkusios vielinės tvoros, prie kurios ją buvo prispaudusi šarvuota mašina.

Galimai neatstatomą kraujo kiekį Asanavičiūtė prarado ne tik dėl vidinio kraujavimo, bet ir kraujuojančių žaizdų. Kyla įtarimas, kad ji turėjo būtinai mirti kaip užvažiavusio tanko auka.

Prieš išvažiuojant nuo televizijos bokšto Greitosios pagalbos mašinai nežinomas vyriškis priėjo prie joje gulėjusios Loretos ir jai suleido neva širdį stiprinančių vaistų. Šio fakto prokurorai netyrė. Medikų žodžiais, Asanavičiūtei galimai buvo suleistas antiaguliantas, neleidžiantis krešėti kraujui, kas galėjo paskatinti kraujavimą ir mirtį.

Asanavičiūtės ligos istorijoje nebuvo nurodyti lūžiai dubens, klubų ar kitų kaulų. Lūžių nebuvimas neužfiksuotas ir chirurginės operacijos metu.

Štai ištrauka iš šios operacijos aprašymo: „Buvo prapjauta Asanavičiūtės L. pilvo sritis. Dubenyje ir kairėje strėnų pusėje aptiktos hematomos. Perrištos dvi klubų arterijos, išorėn išvestas gofruotas vamzdelis. Gilios plėštinės žaizdos tarpvietėje su vietomis apnuogintu kaulu užtampuotos. Operacija tęsėsi iki 4 val. 20 min.“ (b.b. Nr. 10-09-057-96, b.t. 3, b.l. 154 – 172).

Pasirodo, jokių „kruopų“ kaulų vietoje, operuojant Asanavičiūtę, nebuvo aptikta.

Titas Masiulis

Duodamas interviu Vitkus prisiminė, jog po Loretos buvo atvežtas Tito Masiulio lavonas. Praeitame straipsnyje buvo aprašyta nuotrauka, kurioje Masiulis ir Viktoras Šatskich guli ligoninėje ant grindų.

Tačiau Vitkaus interviu nėra pastraipos apie Masiulio sužeidimus. Turbūt todėl, kad jis buvo nužudytas dviem taikliais šūviais. Šaudė į Masiulį du žudikai, stovėję kairėje ir dešinėje. Viena kulka smigo iš priekio į krūtinės ląstą, į širdies sritį, kita — į nugarą, taip pat į širdies sritį.

Judėjimo „Vienybė“ lyderis Valerijus Ivanovas mano, jog vietoj Masiulio nužudytas turėjo būti jis. Ši versija atrodo įtikinama, nes Masiulis buvo gana panašus į Ivanovą ir patamsėse prie televizijos bokšto juos buvo galima lengvai supainioti.

Socialistinis judėjimas „Vienybė“, apjungęs Lietuvoje rusus, lenkus ir lietuvius, landsbergininkams buvo tapęs kaulu gerklėje. Neveltui visus Lietuvos Komunistų partijos/TSKP veikėjus Landsbergis savo knygose vadina „jedinstvenikais“.

Prisiuvo koją

Savo interviu Vitkus baigė pasakojimu apie fantastiškas operacijas, kurias jis neva atliko sausio 13-osios naktį.

Mūsų herojus prisiminė, jog po to, kai nukentėjusieji buvo šiek tiek surūšiuoti, jis nuėjo į operacinę.

„Operuoti reikėjo nedelsiant. Nukentėjusieji buvo kontūzyti, su peršautomis blauzdomis, pėdomis, rankomis, kūno audiniai buvo išplėšti tomis kulkomis su perstumtais centrais <...>. Teko operuoti moterį, kurios koja buvo visiškai sutrupinta ir kabojo tik ant sausgyslių. Ištraukiau tokį blauzdikaulį iš kitos jos kojos blauzdos, persodinau į sutrupintos kojos blauzdą. Paleidau kraujotaką, ir paskui ta moteris vėl vaikščiojo savo kojomis. Akivaizdu, jog tokia rekonstravimo operacija buvo atlikta ne tik tą naktį, bet ir vėliau“.

Šio rašinio autorius neturi medicininio išsilavinimo, tačiau puikiai supranta: atgaminti ant sausgyslių kabančią koją dabartinė chirurgija dar nepajėgi. O 1991 metais tuo labiau negalėjo to padaryti.

Papasakoti apie tokią fantastišką operaciją Vitkaus paprašė Lietuvos generalinės prokuratūros falsifikatoriai, juk sausio 13-osios byloje figūruoja panašūs Loretos Tručiliauskaitės parodymai. Neva sausio naktį ant jos kojos užvažiavo tankas, pastovėjo, apsisuko ir nuvažiavo.

Tačiau 1997 metais į teismo posėdį minėto Ivanovo byloje Tručiliauskaitė atėjo net be lazdelės. Tada Ivanovas pateikė jai atitinkamus klausimus, po kurių dama pravirko ir apleido posėdžių salę. Šį Tručiliauskaitės fantastišką atėjimą savo kojomis į teismą ir bandė paaiškinti chirurgas Vitkus.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 20 — id: `scraped:rubaltic_lt:41edc21a65f1f667`

**Title:** Melagis baltu chalatu: Lietuvos chirurgas televizijos eteryje melavo apie sausio 13-osios įvykius

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos chirurgas Kęstutis Vitkus sausio 11 dieną davė interviu kažkokiai Evelinai Ustinavičiūtei. O sausio 12 dieną jis apsireiškė Lietuvos TV ekranuose fone laužų, kurie liepsnojo greta Seimo pastato, ir pasakojo, kaip 1991 metų sausio 13-osios naktį krovė žuvusių prie Vilniaus televizijos bokšto lavonus ligoninėje po laiptais, o paskui siuvo nukentėjusiems rankas ir kojas. Vitkaus pasakojimas — kaltinimo parodymas, kuris turi patvirtinti tarybinių kariškių kaltę žudant žmones sausio 13-osios naktį. Tačiau šie chirurgo parodymai — melas nuo pradžios iki pabaigos.

Interviu Vitkaus, žmogaus, mačiusio „sovietinį žvėriškumą”, turėjo padėti tašką „bjauriems išsigalvojimams”, falsifikuojant sausio aukų žūties priežastis. Juk gydytojas–chirurgas savo akimis matė rezultatus „nusikaltimo žmoniškumui”, kuriuos įvykdė tarybiniai kariškiai. Tačiau jo prisiminimus verta įdėmiai išanalizuoti.

Siekdami įvertinti jo parodymų teisingumą, pasinaudosime:

a) 15 žuvusių nuotraukomis, kurios buvo padarytos 1991 metų sausio 13-ąją lavoninėje, esančioje Polocko 6;

b) Valerijaus Ivanovo pateiktu 2-ojo Vilniaus apeliacinio teismo teisėjui Ričardui Piličiauskui prašymu Nr.2 su analize dokumentų, patvirtinančių nukentėjusių ir sausio 13-ąją žuvusių pristatymo į Vilniaus ligonines ir lavoninę aplinkybes;

c) 1991 metų vasario 6 dienos pažyma Nr.29 iš baudžiamosios bylos Nr. 10-09-057-96 (8 tomas, 126- 130 psl.) apie sausio aukų žūties priežastis, kurią pasirašė Lietuvos teismo medicinos ekspertizės biuro viršininkas Antanas Garmus;

d) kaltinamuoju baudžiamosios bylos Nr. 09-2-031-99 arba sausio 13-osios bylos aktu.

Kad pasisakymai būtų solidesni, Vitkus pareiškė studijavęs karo lauko chirurgiją Vilniaus universitete ir kaip medikas buvo pasiruošęs dirbti karo sąlygomis. Į „Raudonojo kryžiaus” ligoninę jis su tėvu, taip pat mediku, atvyko savarankiškai po to, kai sausio 13-osios naktį išgirdo tankų patrankų šaudymą tuščiais šoviniais.

„Raudonojo kryžiaus” ligoninė — Vilniaus centre. Iki jos nuo Lietuvos radijo ir televizijos (LRT) pastato ir televizijos bokšto buvo arčiausia. Suprantama, ten ir buvo nukreiptas pagrindinis nukentėjusių prie šių objektų srautas.

Viktoro Šatskich žaizda

Vitkus praneša, kad vienas iš pirmųjų į ligoninę buvo atvežtas „omonininkas”, „Alfos” puolėjas (leitenantas V.Šatskich — RuBaltic.Ru past.). O paskui chirurgas pradeda fantazuoti. Ir ne todėl, kad specialiosios „A”VSK grupės karininką supainiojo su Ypatingos paskirties milicijos padalinio darbuotoju.

O todėl, jog tvirtino, kad Šatskich “buvo nušautas šūviu į nugarą. Nugaroje matėsi nedidelė skylutė, o priekyje — didelė kiaurymė nuo išlėkusios kulkos. Supratau, kad šauta buvo kulka su perslinktu centru — jos skrieja dideliu greičiu ir pažeidžia daug organų. Į jį šovė savi, kolegos... Aš dar spėjau nufotografuoti tas žaizdas. Supratau privaląs išsaugoti įkalčius, įrodančius, jog omonininką nužudė savi. Tėvas organizavo slaptą kūno išvežimą į Polocko gatvę, kur buvo ekspertizės biuras, siekiant atlikti pomirtinį skrodimą” .

Tiksliai žinoma, kad jokios didelės kiaurymės nuo išlėkusios kulkos Šatskich krūtinėje nebuvo. 5,45 mm kulka,pramušusi jo nugarą iš apačios į viršų 45 laipsnių kampu, atsimušė į krūtinkaulį ir liko leitenanto kūne. Šatskich mirė nuo plataus vidinio kraujo išsiliejimo, nes minia prie LRT pastato neleido laiku privažiuoti greitosios pagalbos mašinai.

Šatskich buvo paskutinis grandinėje “Alfos” karių, kurie veržėsi į devynaukštį LRT pastatą. Jį sužeidė lietuviškieji kovotojai, kai jis įšoko į šio pastato prieangį. Vėliau šiame prieangyje buvo aptikta daug kulkų išdaužų. Yra žinoma, jog “Alfos” kariai 1991 metų sausio 13-ąją koviniais šoviniais nesinaudojo.

1991 metų sausio 16 dieną 97-ąjame Lietuvos Aukščiausiosios Tarybos posėdyje Vytautas Landsbergis, remdamasis Lietuvos generaliniu prokuroru Artūru Paulausku, skersai išilgai šliaužiojusiu televizijos bokšte, buvo priverstas pripažinti, jog “Alfa” televizijos bokšte nesinaudojo šaunamaisiais ginklais. Tai nepaneigiamas faktas.

Priminsime užmaršuoliui chirurgui, jog “Raudonojo kryžiaus” ligoninėje gulėjusių ant grindų nušautų Viktoro Šatskich ir Tito Masiulio nuotrauka, kurią padarė informacinės agentūros ELTA foto korespondentas A.Gulevičius, buvo patalpinta Lietuvos laikraščiuose. Parašas po ja skelbė: “Titas Masiulis atliko Tėvynei didelę pareigą, o kokios priežastys atvedė į Lietuvą VSK leitenantą V.Šatskich?” Ta pati nuotrauka išspausdinta žurnalisto Edmundo Ganusausko knygos “Gyvoji barikada”, kuri buvo išleista Vilniuje 1992 metais, 107-me puslapyje.

Nuotraukoje gerai matosi apnuoginta ir siauru tvarsčiu perrišta Šatskich krūtinė. O oficialioje vyriausiojo Lietuvos medicinos eksperto Antano Garmaus pažymoje Nr.26, kuri apibendrina sausio aukų teismo medicinos ekspertų aktus, parašytus 1991 metų sausio mėn., pranešama, kad Šatskich “akla kulka peršauta krūtinės ląsta<...> įeinamoji anga nugaroje”.

Štai jums ir didžiulė žaizda krūtinėje!

Tačiau vien tik melo apie Šatskich žaizdą Vitkui nepakako.

Lavonai po laiptais

Vitkus prisimena: “Greitosios pagalbos mašinos važiavo ir važiavo... O mes su R.Vaičiūnu paskirstėme, kur nešti žmones. Uždarę vieną laiptinę, po laiptais krovėme lavonus. Vėliau juos išnešėme į kiemą, į garažą. Reikėjo išlaisvinti vietą gyviesiems...”

Pasak kaltinamojo sausio 13-osios bylos akto, mirtinomis šaunamojo ginklo aukomis sausio 13-osios naktį tapo 8 žmonės. Tai Vytautas Vaitkus, Ignas Šimulionis, Vidas Maciulevičius, Virginijus Druskis, Darius Gerbutavičius, Rimantas Juknevičius, Apolinaras Juozas Povilaitis, Titas Masiulis.

Be to, sprogus savadarbiui sprogstamajam užtaisui, prie LRT pastato žuvo Alvydas Kanapinskas.

Dešimtoji šaunamojo ginklo auka, Vytautas Koncevičius, mirė ligoninėje apie sausio 18 dieną. Tame pačiame akte pranešama, jog dėl mirtino tarybinių tankų užvažiavimo žuvo trys žmonės: Petras Kavolinskas, Loreta Asanavičiūtė ir Rolandas Jankauskas.

Kaip žinia, Asanavičiūtė mirė “Raudonojo kryžiaus” ligoninėje po operacijos apie 7 val. ryto sausio 13-osios. Tokiu būdu kartu su Šatskich sausio 13-osios naktį buvo 12 lavonų.

Valerijus Ivanovas, buvęs socialistinio judėjimo “Vienybė” lyderis, dirbdamas su dokumentais, kai jam buvo iškeltos baudžiamosios bylos, nustatė: į lavoninę Polocko gatvėje nuo 4-30 iki 5-00 buvo atvežti Kanapinsko, Vaitkaus, Povilaičio, Kavoliuko, o dar gali būti – Gerbutavičiaus ir 60-mečio Makulkos, mirusio nuo infarkto, o vėliau stebuklingu būdu tapusio 30-mečiu Matulka, lavonai.

Abejonių kelia sekantis Vitkaus tvirtinimas. Jis prisimena, jog rytą į “Raudonojo kryžiaus” ligoninę atėjo “Alfos” kariai ieškoti savo žuvusio draugo. Tačiau žinoma, jog rytą visi lavonai buvo pervežti iš ligoninės į lavoninę. Šatskich lavonas tuo metu buvo slapta pervežtas į Santariškių ligoninę, kur buvo neteisėtai laikomas. O Vitkus pareiškia, jog “Alfos” kariai sausio 13-osios rytą draugo ieškojo tarp po laiptais gulėjusių lavonų?!

Amfitaminas “Alfos” kariams

Vitkus taip pat pareiškė, kad į ligoninę atėję “Alfos” kariškiai atrodė prislėgti. Jis neabejodamas nustatė jiems diagnozę: “Vakar šiems kariams buvo duotas amfitaminas, todėl šiandien, nustojus jam veikti, jie atrodė kaip zombi. Jie beprasmiškai žiūrėjo į lavonus ir tylėjo”.

Vitkui ne chirurgu būti, o rašyti klaikių epizodų scenarijus amerikiečių režisieriui Alfredui Chičkokui.

Jo tvirtinimai, jog “Alfos” kariai naudojo amfitaminą, — šlykštus melas. Esmė tame, kad tokio stimuliatoriaus, kaip amfitaminas, naudojimas “A” grupės darbuotojams buvo neleistinas.

***

Straipsnio autorių Vladislavą Švedą pusantrus metus (1990–1991) “dengė” įvairūs “Alfos” karininkai.

“Per tą laikotarpį aš ju jais pabuvojau daugelyje situacijų. Jie dengė mane trijų sudėtingų pasikėsinimų metu, o du kartus užkirto jiems kelią. Nepastebėjau, kad kas nors iš jų būtų turėjęs keistų polinkių. Galima tik pavydėti Jų santūrumui ir šaltakraujiškumui paslaptingiausių situacijų metu. Degtinės jie taip gėrė labai saikingai, neprarasdami kovinių savybių” , — pasakojo jis.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```
