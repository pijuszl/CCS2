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

### Article 1 — id: `scraped:rubaltic_lt:8866e56397190926`

**Title:** Lenkų klasikas smerkia Lietuvą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Žinomas lenkų režisierius Kšištofas Zanusi apsilankė Vilniuje ir paragino Lietuvą atgailauti už kolaboravimą su komunistiniu režimu. Tačiau Lietuvos politikai sugeba pareikalauti atgailos ir materialinių kompensacijų iš kitų, o patys atgailauti neketina, todėl kad jie buvo sudėtinė komunistinio režimo dalis. Sekretoriais ideologijos klausimais, partijos aktyvistais, partinių mokyklų dėstytojais, komjaunuoliais — iš esmės atgailauti šiems žmonėms reikštų liustruotis.

„Štai ko aš nematau čia, Lietuvoje: neatgailaujama dėl komunizmo, dėl bendradarbiavimo su režimu. Čekijoje, Lenkijoje tai jau buvo, šiek tiek Vengrijoje, — pareiškė Kšištofas Zanusi interviu Lietuvos portalui Delfi. — Yra tautos, kurios tai padarė, kurios nusikalto, bet atgailavo, o tai buvo teisėjai, prokurorai, profesoriai, rektoriai. Ir jie turėjo pasakyti: „Aš kaltas“.

Tokie Lietuvą smerkiantys lenkų kino klasiko žodžiai — nemaloni staigmena Daukanto aikštėje tupintiems informacinės politikos kuratoriams. Juk dabartinę Lietuvą pasmerkė ne „Kremliaus agentas“, o visiškas jos ideologinis sąjungininkas ir bendramintis. Duodamas interviu Lietuvos Delfi, Zanusi kalbėjo tai, ką norėjo girdėti šios šalies politikų ausys. Jis pasakė, kad Lietuva, Lenkija, Ukraina ir kitos šalys kartu patyrė „karinio komunizmo košmarą“, kad Rusija „ nuo išsivysčiusių šalių atsilieka 50 metų“, kad rusų inteligentija neturi tylėti — ji privalo kalbėti apie „kruviną“ Putino režimą.

Tačiau tuo ir nepatogūs principingi ir tvirtų įsitikinimų žmonės „fliugeriams“, kurie keičia savo įsitikinimus 180 laipsnių priklausomai nuo politinės konjunktūros. Pirmųjų principingumas visada griauna antrųjų planus, nes idėjinių žmonių atvirumas ir vienašališkumas neišvengiamai parodo „persivertėlių“ dviveidiškumą, dvigubus standartus ir veidmainystę.

Taip atsitiko ir šį kartą. Savo strėles Kšištofas Zanusi nukreipė Rusijos link, o pataikė į Lietuvą. Lenkų įžymybė lyg ir apie Rusiją kalba, kad ten neįmanoma gyventi, nes visuomenė dar neatgailavo. Tačiau tuo pačiu visa tai liečia ir Lietuvą.

O paprieštarauti patriarchui tiesiog neįmanoma. Nes kaip Kšištofas Zanusi įsivaizduoja atgailą dėl kolaboravimo su „okupantais“ lietuviškai? Kaip nuskambės Lietuvos politiko kančiose pagimdyta frazė „Aš kaltas“?

Pabandykime tai įsivaizduoti: ateina prezidentė Dalia Grybauskaitė prie Gedimino bokšto ir sako:

— Štai aš stoviu prieš jus, TSKP CK Vilniaus aukštosios partinės mokyklos mokslinė sekretorė. Disertaciją Maskvoje politinės ekonomijos tema apgynusi, „miško brolius“ „klasių priešais“ vadinusi, kovoje už Lietuvos nepriklausomybę nedalyvavusi, apie pasitraukimą iš Lietuvos Kompartijos TSKP platformoje melavusi, 1991 metų vasarą TSRS pasiuntinybėje Vašingtone dirbusi. Atleisk tu man, lietuvių tauta, aš kalta.

Po Ekscelencijos Dalios į baudžiamąją vietą pakyla „tautos tėvas“ Vytautas Landsbergis ir pareiškia: ir tėvelis mano buvo NKVD agentas, ir aš dirbau KGB labui, ir Sąjūdį kūrė KGB, ir jo lyderiu mane padarė KGB. Liustruokite mane, žmonės mielieji, aš kaltas.

Po Dėdulės į tribūną pakyla užsienio reikalų ministras Linas Linkevičius. Pradeda svaidytis įprastomis frazėmis, dėdamas lygybės ženklą tarp komunizmo ir nacizmo, sapaliodamas apie būtinybę atgailauti ir išmokėti Lietuvai materialinę kompensaciją už „okupaciją“, apie naujas sankcijas ir visišką Maskvos diplomatinį izoliavimą... o paskui staiga nutyla, kaip nekalta mergelė raudonuoja ir taip pat energingai ima skanduoti komjaunuoliškus šūkius. Ir visiems viskas aišku be jokių prisipažinimų: iš už solidaus europietiškos šalies ministro nugaros išlenda ausys LLKJS CK skyriaus vedėjo, kuris komjaunuoliško girtuokliavimo Maskvoje metu buvo siunčiamas degtinės į valiutinę parduotuvę.

Todėl Lietuvos valdžia gali kitus raginti atgailauti, bet tik ne save. Rusija — TSRS teisių perėmėja, lai ji ir atgailauja, o mus, kaip Cezario žmoną, nėra kuo kaltinti. Todėl atgailos dėl komunizmo temą Lietuva mato tik užsienio politikoje, bet jokiu būdu — ne vidaus.

Dėl visiško neatitikimo, kas deklaruojama ir kas buvo realiai, Lietuva ir kitos Pabaltijo šalys pastoviai patenka į nepatogią padėtį santykiuose su Centrinės ir Rytų Europos šalimis, kuriose tikrai vyko antikomunistinė kova. Pasiūlys Lietuva Europos parlamente komunizmo nusikaltimus smerkiančią rezoliuciją, taikydama Rusijai, o lenkų parlamentarai staiga prisimena pačios Lietuvos prezidentės komunistinę jaunystę.

Juk ir Kšištofas Zanusi, smerkdamas Lietuvą, pasisako kaip Vyšegrado grupės atstovas: kaip pavyzdį lietuviams pateikia Lenkiją, Čekiją, Vengriją. „Lenkijoje šis procesas seniai praėjo ir eina toliau, — sako lenkų klasikas apie kolaborantų, bendradarbiavusių su komunistais, atgailą. — Ir jis praėjo taip, kad mes jaučiame, jog buvo kaltė ir moralinė nuobauda. Juk kiek mūsų piliečių visame tame dalyvavo, svetimi tiek nebūtų padarę“.

Ar verta stebėtis, kad Lietuvoje nebuvo tos atgailos, kaip Lenkijoje. Lenkų „Solidarumas“ atsirado 1980 metais po antitarybinio darbininkų judėjimo su centru Gdanske dešimtmečio. Valdžion „Solidarumas“ atėjo dar po dešimties metų veiklos pogrindyje. Dviejų antitarybinio darbo dešimtmečių pakako, kad tuo metu, kai griuvo socialistinė sistema ir subyrėjo Varšuvos blokas, Lenkijoje susiformuotų pajėgus šaliai vadovauti kontrelitas. Ir šiandien „Solidarumo“ išeiviai sudaro lenkų politinę klasę.

O kuo Lietuva gali didžiuotis kovos su „tarybine okupacija“ laukuose? Negi Lietuvos kolūkius terorizavusiais banditais, kuriuos gaudė dabartinės Lietuvos prezidentės tėvelis, raudonasis „Birutės-4“ būrio partizanas ir specialaus NKVD padalinio Lietuvos TSR darbuotojas Polikarpas Grybauskas, ir kuriuos dabar ant pjedestalo kelia jo dukra, praėjusio politinio gyvenimo metu visiškai teisėtai vadinusi miško banditus „klasių priešais“?

O gal pertvarką remiančiu judėjimu, kurio sukūrimo idėja priklausė TSKP CK sekretoriui Aleksandrui Jakovlevui, sugalvojusiam suformuoti „socializmo vitrinoje“ — Pabaltijyje vietos inteligentijos susivienijimus Gorbačiovo reformoms remti? Beje, šios idėjos įgyvendinimu užsiiminėjo respublikiniai KGB padaliniai.

Todėl lietuviškasis desovietizavimas ir „prakeiktosios“ raudonosios praeities įveikimas praktiškai virsta tragifarsu su baudžiamuoju persekiojimu už „okupacijos“ neigimą, išėmimu iš vaikų prekių parduotuvių Raudonosios armijos kareivukų, draudimu raudonosios žvaigždės ir kampanijomis, smerkiančiomis „tarybinių“ dešrelių gamintojus.

Apie kokią tikrą atgailą lietuvių visuomenėje galima kalbėti, žinant koks yra valdžios moralinis vaizdas? Tikras ir rimtas liustravimas lietuvių atveju atrodytų lyg sename uzbekų anekdote.

Pareina uzbekas namo ir sako žmonai: „Oi, nelaimė, Zulfija, į partiją manęs nepriėmė. Paklausė, ar buvau Kur-baši gaujoje, atsakiau — buvau, štai ir nepriėmė“. Žmona nustebusi: „Negi negalėjai sumeluoti, pasakyti, kad nebuvai?“ Uzbekas: „Negalėjau sumeluoti, nes klausė pats Kur-baši“.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 2 — id: `scraped:rubaltic_lt:858701f7b24c4dbd`

**Title:** Lietuviai pradeda nusivilti savo šalimi

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Demokratijos veikla Lietuvoje nepatenkinti 59 proc. lietuvių. Šis rodiklis kasmet didėja, kasmet didėja ir emigracijos srautas. Lietuviai masiškai nusivilia savo valstybe ir šalyje susiformavusia „demokratija“, kuri nėra demokratija.

Sociologinės apklausos duomenimis, kurią ELTos užsakymu pravedė Baltijos tyrimai, 2015 metų liepos mėnesį demokratijos veikla Lietuvoje buvo nepatenkintas 51 proc. lietuvių.

Tų pačių Baltijos tyrimų duomenimis, 2016 metų rudenį demokratijos veikla savo šalyje buvo nepatenkinti 55 proc. Lietuvos piliečių.

Pagaliau, šių metų kovą pagal Baltijos tyrimų apklausą neigiamai Lietuvos demokratijos lygį vertino 59 proc. respondentų. Teigiamai demokratijos lygį vertina 34 proc. respondentų — tik kas trečias lietuvis.

Palyginkime Lietuvos sociologų statistiką su šalies emigracijos statistika. Pagal 2016 metų rezultatus, Lietuva mušė pasaulio depopuliacijos rekordus, kasmet prarasdama 1,5 proc. gyventojų. Lyginant su praeitais metais, emigracija iš Lietuvos padidėjo 6,5 proc. Na, o 2015 metais, lyginant su 2014-aisiais, emigracija buvo ūgtelėjusi 21,6 proc. Šių metų kovą iš Lietuvos emigravo 4607 žmonės, o tai 1129 žmonėmis daugiau, nei 2016 metų kovą.

Šie skaičiai — europietiškas rekordas. Statistikos departamento duomenimis, 2017 metų kovo 1 dieną Lietuvoje gyveno 2,849 milijono žmonių, o tai 39,2 tūkstančio mažiau nei prieš metus. Pagrindinė tokios depopuliacijos priežastis — gyventojų emigracija.

Šių metų „didžioji kelionė“ iš Lietuvos pagal savo apimtis sumušė visų praėjusių metų rekordus. 2017 metų sausio mėnesį buvo gauta 15 tūkstančių išvykimo iš Lietuvos deklaracijų, o tai triskart daugiau nei 2016 metų sausį — tada buvo paduotos 5082 deklaracijos. Ir štai po metų — jų jau 15388. Arba emigracijos srautas per metus tikrai triskart išaugo, arba tikrieji praėjusių metų gyventojų išvykimo skaičiai buvo ženkliai sumažinti, ir šiandien Lietuvoje gyvena ne daugiau kaip 2,5 milijono žmonių.

Emigracija iš Lietuvos — gyvybinga naujos kartos strategija. Pagrindinis emigrantas — jaunimas: 52 proc. praeitų metų pirmąjį pusmetį išvykusių — 18–35 metų žmonės. Šalį palieka aktyviausi, besistengiantys kopti karjeros laiptais. Lietuva praranda naujas kartas ir kvalifikuotus svarbiausių sferų specialistus.

Palyginkime dvi rodiklių grupes. Nepasitenkinimas Lietuvos demokratijos institutų veikla kasmet didėja, didėja ir emigracija. Ar nėra čia užčiuopiamas ryšys? Ar emigracija netapo to nepasitenkinimo pasekme?

Ar gali tai kelti nuostabą, atsižvelgiant į Lietuvos vyriausybių darbą? Pagal visas demokratines normas šalies vyriausybės keičiasi kas ketveri metai, tačiau jų veikla nekinta, ir joms būdingas neveiklumas pagrindiniais klausimais, aktyviai spręsti kuriuos buvo žadėta rinkėjams.

Antroji iš eilės koalicija Lietuvoje įšoka valdžion nuo socialinių pažadų tramplino. Buvusi socialdemokratų vyriausybė žadėjo vadovautis šalies viduje socialiai orientuota politika ir atsisakyti savo pirmtakų konservatorių geopolitinio „donkichotiškumo“, o užsienio politikoje siekti susitaikymo su kaimynais — Rusija, Lenkija, Baltatusija.

Nieko nepadaryta: vietoj socialinės politikos, kaip svarbiausio prioriteto, sulaukta „Rytų partnerystės“, ginklų tiekimo Ukrainai, raginimo visiškai diplomatiškai izoliuoti Maskvą, kovos su Baltarusijos atomine elektrine. Net su lenkais nesugebėjo susitaikyti.

Dabartinė „valstiečių“ ir socialdemokratų koalicija po vyriausybės praėjusių metų rudenį suformavimo svarbiausia Lietuvos problema įvardino demografiją ir vėl pažadėjo vykdyti socialiai atsakingą politiką tikslu „išsaugoti“ lietuvių tautą.

„Jeigu sėsdami į lėktuvą žmonės tikėtų, jog namuose rytoj bus geriau, jie persigalvotų skristi“, — pareiškė rinkimus laimėjusios Lietuvos valstiečių ir žaliųjų sąjungos lyderis Ramūnas Karbauskis konferencijos, skirtos naujos vyriausybės formavimui, metu. Kaip tada tvirtino naujos valdančiosios partijos vadovas, naujai suformuota vyriausybė girdi „demografinės bombos tiksėjimą“ ir pasirengusi kovoti dėl demografinės situacijos Lietuvoje gerinimo. Lietuvos demografijos gerinimui reikėjo terapijos komplekso. „Egzistuoja daug sisteminių klausimų: švietimas, sveikatos apsauga, ekonomikos vystymasis, regionų politika. Aš manau, svarbiausia — švietimas, jo kokybė, kad žmonės turėtų darbą Lietuvoje ir tas darbas būtų gerai apmokamas“, — sako LŽVS lyderis.

O kuo gi savo darbą pradėjo naujoji vyriausybė?

Kokia tai prasme valdančiosios partijos pirmininkas nesumelavo. Kalbėjo, jog pagrindine depopuliacijos mažinimo priemone jis mato švietimą; „žaliųjų“ vyriausybė ir pradėjo nuo depopuliacijos. O iš tikrųjų tai — pasityčiojimas.

Priešrinkiminės kampanijos metu Lietuvos valstiečių ir žaliųjų sąjunga siūlė įvesti valstybines subsidijas jaunų šeimų būstams. Ir kur jos? Lenkų konservatoriai 2015 metais taip pat žadėjo — ir netrukus, patekę valdžion, pasiūlė programą „Šeima+”. Tačiau visokio plauko Lietuvos partijos po pergalės rinkimuose visus pasiūlymus ir pažadus gyventojams pakeičia „rusų grėsme“. Priklausant nuo užsienio politikos konjunktūros prie šios pagrindinės grėsmės jos dar gali pripliusuoti „baltarusių grėsmę“ (kaip šiuo metu dėl atominės elektrinės) ir „lenkų grėsmę“ (kuri lietuviškiesiems nacionalistams rusens amžinai, kol Lietuvoje gyvena nenorintys tapti lietuviais lenkai).

Socialdemokratai 2012 metais atrodė alternatyva konservatoriams. „Valstiečiai“ 2016-aisiais reiškėsi kaip alternatyva socialdemokratams. Į Dalią Grybauskaitę 2009 metais žiūrėta kaip į alternatyvą politinei elitai. Tačiau po rinkimų Lietuvos visuomenė pamatė tą pačią politinę pelkę, o žodis „permainos“ buvo išskraidintas į šiukšlyną.

Ir todėl dauguma lietuvių nusivylė politinių institutų darbu. Net du trečdalius gyventojų netenkina tokia „demokratija“. Balsuok nebalsavęs — vis tiek išlįs dėdulės Landsbergio ausys.

Tame ir glūdi emigracijos iš Lietuvos esmė — emigracijos, kuri didėja didėjant gyventojų nusivylimui Lietuvos valstybe ir joje sukurta „demokratija“.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 3 — id: `scraped:rubaltic_lt:7d0b2188b6ff7f32`

**Title:** Lietuvos vadovybė „spaudžia ir apvaginėja darbščiąsias biteles“

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos ekonomistai, finansų ekspertai ir net Seimo nariai pagaliau pripažino: infliacija šalyje pasiekė apogėjų. Vis sunkiau lietuviams gyventi. Viskas brangsta, ir tai skatina juos masiškai emigruoti, o valdžia pagaliau susigriebė: kaip gerai buvo gyventa neįstojus į ES.

RuBaltic.Ru paruošė įvairiausių ekspertų svarbiausių pareiškimų ir prognozių apžvalgą. Kiekvienas iš jų atkreipė dėmesį į tam tikrus faktorius, kurie sukėlė katastrofišką Lietuvos Respublikos ekonomikos krizę.

Žmonės priversti išvykti

Vyresnioji banko DNB Lietuvos skyriaus analitikė Indrė Genytė, analizuodama einamąją Lietuvos situaciją, paminėjo daugybę valdžios klaidų, sukėlusių eilę problemų. Svarbiausia iš jų – nesugebėjimas paruošti ilgalaikę nacionalinės ekonomikos atgaivinimo strategiją.

„Politikams atrodo, jog geriausia priimti eilę nutarimų, kaip iš vienų atimti, o kitiems duoti, – nesvarbu, jog po ketverių metų (geriausiu arveju) juos pakeis tretieji. Bet visa tai primena prisidengimą figos lapu: gal ką nors ir pavyks paslėpti, bet praktiškos naudos mažai.

Jei tos motyvuotos darbščios bitelės, kurios nebijo veikti, kurti, siekti, mokytis, tobulėti, bus patenkintos ir niekuo neapribotos, jų pagamintu medumi galės mėgautis ir kiti socialiai pažeidžiami visuomenės segmentai.

Kainų augimas pasiekė apogėjų

Vyresnysis Danske Bank Baltijos šalyse ekonomistas Rokas Grajauskas savo ataskaitoje rašo, kad kainų augimas šalyje pasiekė aukščiausią tašką.

Jo žodžiais, situacija netrukus turėtų stabilizuotis. Kainos, žinoma, nesumažės, tačiau būtinai teks pakelti atlyginimus.

Šių metų kovą infliacija Lietuvoje sudarė 3,1 proc. Priežastis – naftos kainos, alkoholio ir tabako gaminių akcizų augimas. Tačiau artimiausiu metu infliacijos tempai turi sumažėti, o atlyginimai šalyje didės greičiau, nei kainos,- mano Rokas Grajauskas.

„Artimiausiais mėnesiais nebus reikšmingesnio naftos kainos padidėjimo, todėl kainos neturėtų augti ankstesniu greičiu. Visa tai metų pabaigoje sumažins infliaciją iki 2,5 proc. Danske Bank paskaičiavimais, vidutinė šių metų infliacija bus 2,8 proc., kitais metais sumažės iki 2,4 proc. Tačiau atlyginimai augs vėlgi ženkliai: šiais metais – 6,7, kitais – 7,1 proc., – teigiama ataskaitoje.

Be euro buvo geriau?

Visapusiškas brangimas ir kainų augimas papiktino net Lietuvos Seimo narius. Pavyzdžiui, opozicinės parlamentinės partijos „Tvarka ir teisingumas“ lyderį Remigijų Žemaitaitį papiktino nepateisinamai padidintos vaikiškų žaislų kainos.

Tautos išrinktasis patyrė šoką vienoje iš Vilniaus prekybos centro „Panorama“ žaislų parduotuvėje: įprastas pliušinis meškinas joje kainavo 269 eurus arba 928 litus.

Jo žodžiais, šiandien 269 eurai neatrodo labai gąsdinanti suma, tačiau, pavertus ją litais, tenka krūptelti. Anksčiau už minkštą žaisliuką niekas neprašė pakloti 1000 litų. Niekas nebūtų sutikęs pirkti už tokius pinigus, tačiau šiandien prekybininkai begėdiškai manipuliuoja skaičiais.

Faktiškai kaina litais susilygino su kaina eurais. Pasikeitė tik valiutos ženklas. Deputatas tai vadina pasityčiojimu iš Lietuvos piliečių, kurių atlyginimai, lyginant su kainomis, nepadidėjo.

Jo manymu, tai padės žmonėms suvokti, kiek iš jų nori „išplėšti“ nesąžiningi prekeiviai. „Pavyzdžiui, Vokietijoje kainos nacionaline valiuta, marke, buvo nurodomos net dešimtmečiui po euro įvedimo praėjus. Kodėl mes negalime panašiai pasielgti?“ – klausia Žemaitaitis.

Atsirūgo nusisukimas nuo Rusijos

Lietuvos pramonininkų konfederacijos viceprezidentas Arūnas Laurinaitis pareiškė, jog valstybė nepadeda saviems verslininkams įsitvirtinti užsienio rinkose. 2014 metais Lietuva prarado pagrindinę realizavimo rinką Rusijoje, o alternatyvos taip ir nesusirado.

Arūnas Laurinaitis apgailestavo, kad valstybė kliudo vystytis ekonominiams ryšiams su Rusija, Kazachstanu ir kitomis buvusiomis Tarybų Sąjungos respublikomis. Jis pritaria Lietuvos gamintojų siekiams įsitvirtinti Azijos ir Persų įlankos šalių rinkose, tačiau tvirtina, jog valstybė ir URM nenori padėti mūsų biznieriams. O atrasti naujas rinkas be diplomatiškos paramos faktiškai neįmanoma.

„Pagrindinė problema ne komercinėje veikloje, o šalies nežinojime ir nepatikimume arba valstybės ryšių su ja nebuvime. Be oficialių asmenų, pasiuntinių ir diplomatų vizitų komercinė veikla nesugebės įsitvirtinti naujose rinkose. Čia būtina priemonių visuma nuo diplomatijos pasiuntinių iki specialių atašė paskyrimų“, – sako jis.

Šiai dienai eksportas sudaro 87 proc. Lietuvos BVP ir yra varomoji visos ekonomikos jėga. Pastaraisiais metais Lietuvos eksporto apimtis sumažėjo 7,3 proc.

Oficialusis Vilnius ragina visiškai atsisakyti bendravimo su Rusija ir persiorientuoti į kitas rinkas. Tačiau ir per trejetą sankcijų metų Lietuva nesugebėjo kompensuoti to, ką prarado netekusi Rusijos rinkos. Nuo 2014 iki 2016 metų į iždą nepateko virš 2 milijardų eurų.

2016 metų rezultatas: bendra eksporto apimtis sudarė 22,5 milijardo eurų, importo – 25 milijardai. Tokiu būdu, šalyje vėl matome prekybos su užsieniu deficitą, kuris sudarė 2,5 milijardo eurų.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 4 — id: `scraped:rubaltic_lt:43378867bf5f0771`

**Title:** Lietuvos vadovybė nemato savo kaltės dėl vykstančios depopuliacijos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Neseniai paskelbta Eurostato prognozė, jog per keletą dešimtmečių faktiškai išnyks visi Lietuvos gyventojai, sukėlė sąmyšį šalies vadovybėje. Nepaisant to, jog pagrindine valstybės problema tapo masiška emigracija, valdžiai rūpi visiškai kitkas. Tarp prioritetų – „rusų grėsmė“ ir vidaus priešų paieška.

Pagal prognozę, 2080 metais Lietuvoje liks tik 1650 tūkst. gyventojų. Taigi 1,2 mln. Mažiau, nei jų yra dabar. Pesimistiškas scenarijus, kai demografijos plane Lietuvos išnykimas vyks greičiau nei kitų ES šalių, paremtas apskaičiavimais. Pagal prognozes, jau 2050 metais lietuvių liks tik 2 milijonai.

Atrodytų, toks liūdnas scenarijus neturėtų tapti naujiena Lietuvos visuomenei, tačiau tai, kas žinoma visiems, tiesiog sukrėtė premjerą Saulių Skvernelį ir prezidentę Dalią Grybauskaitę. Pastaroji nepriėmė smūgio ir pareiškė, kad dėl emigracijos ir kitų lietuvių nelaimių kalti visi, bet tik ne ji.

Svajojama apie diktatūrą?

Geležinė Pabaltijo ledi vienareikšmiškai davė suprasti, kad kalti vyriausybė, Seimas ir valstybiniai valdymai, nesugebantys pravesti greitų ir efektyvių reformų.

Dalia Grybauskaitė pasisakė ta prasme, kad ministrai ir deputatai nemoka dirbti ir priimti sprendimų, o ji, deja, neturi savo rankose tiek valdžios, kad suvaldytų situaciją ir išgelbėtų Tėvynę.

„Žmonės emigruoja dėl įvairių priežasčių: dėl gyvenimo lygio skirtumo, švietimo kokybės, biurokratijos, socialinės savijautos ir dar dėl daug ko. Kol mes nesiryžtame imtis veiksmingų reformų, žmonės ieškos geresnio gyvenimo kitose šalyse. Žadėti pokyčiai turi būti greiti ir efektyvūs. Jie reikalingi visiems – net ir tiems, kurie norėtų sugrįžti“, – taip Eurostato prognozę komentavo prezidentė.

Dalios Grybauskaitės pozicija, be abejonės, jai patogi: ji sugebėjo gudriai atsikratyti visų problemų ir negatyvių momentų, kaltę dėl visų bėdų suversdama kitiems. Tokį žaidimą ji žaidžia visos kadencijos metu. Kai tik šalyje pakyla visuomeninės įtampos laipsnis, prezidentė tampa nepatenkintos minios užtarėja ir pila kritiką vyriausybės bei Seimo adresu.

Kaip senos tarybinės sistemos užgrūdintas žmogus ir Kompartijos narė, Grybauskaitė bando pasakyti, kad, turėdama savo rankose daugiau valdžios, ji daug ką pakeistų gerąja linkme. Iš jos kalbų ir pareiškimų nesunku daryti išvadą: sielos gelmėse ji gyvena svajone, jog Lietuva taps prezidentine respublika su visais reikalingais atributais.

Premjeras maitina rytdiena

Premjeras Saulius Skvernelis, oponuodamas prezidentei, pareiškė, kad jo Ministrų kabinetas pradėjo dirbti ne taip seniai ir todėl negali tuoj pat išspręsti visų problemų. Jo žodžiais, greitu ir efektyviu sprendimu gali tapti tik draudimas išvykti iš Lietuvos.

„Įsivaizduokime, jog mes tikrai priėmėme įstatymą, draudžiantį išvykti iš Lietuvos,– tai turbūt ir būtų tas greitas sprendimas (apie kurį kalba prezidentė – RuBaltic.Ru pastaba). Tačiau jei mes norime kad žmonės neišvažiuotų,– o išvažiuoja jie todėl, kad savo šalyje jaučiasi nelaimingi, nes neturi galimybės socialiniame plane gyventi oriai,– mes tikrai nepriimsime neteisingų sprendimų. Žmonės nepamatys blogų vyriausybės veiksmų praėjus 100–150 mūsų darbo dienų“,– pasakė žurnalistams premjeras kovo 23 dieną.

O karalius – nuogas!

Tragedija tame, kad Lietuvos valdžiai, nepaisant skambių žodžių ir parodomojo susirūpinimo tokiomis problemomis, kaip emigracija, aukštas mirtingumas ir gyventojų nuskurdinimas, neitin rūpi šie klausimai.

Pastaroji tema tapo ypač aktuali pastarosiomis dienomis. Būtinybę stiprinti vidaus saugumą ir priešintis penktąjai kolonai, t.y. vidaus priešui, Grybauskaitė akcentavo naujo Valstybės saugumo departamento pastatų komplekso atidarymo ceremonijos metu.

Akivaizdu, jog Lietuvos Respublikos vadovei jau nusibodo kalbėti apie rusų grėsmę, todėl ji atkreipė dėmesį į vidaus problemas, tik, deja, vėl ne į tas.

„Valstybė saugi tik tol, kol valdžia tarnauja ne įvairioms įtakos grupėms, „rosatomams“ ar Kremliaus propagandistams, o žmonėms, kurie nori būti laisvi, nepriklausomi, kurių balsai girdimi valstybėje. Todėl žvalgybai turi rūpėti ne tik išorės priešo kėslai, bet ir pasipriešinimas vidaus grėsmėms“, – šį pranešimą pagarsino Lietuvos prezidentūra.

Kalbėdama apie įvairias „įtakos grupes“ ir „rosatomus“, prezidentė vienareikšmiškai priminė skandalą su buvusiu Seimo pirmininko pavaduotoju socialdemokratu Mindaugu Basčiu, kurį VSD apkaltino valstybinės paslapties atskleidimu ir pernelyg tampriais ryšiais su Rusijos atstovais.

Savo pareiškimu apie priešų paieškas ir pasipriešinimą vidaus grėsmei ji faktiškai paskatino VSD agentus organizuoti eilinę raganų medžioklę. Tai patvirtina ir jos netiesioginis priminimas apie Basčio „bylą“.

Blaivaus proto balsas

Šiandien tik nedaugelis Lietuvos politikų atvirai pareiškia, kad valstybė ritasi link katastrofos ir visiško išnykimo. Tarp jų – buvęs prezidentas, o dabar eurodeputatas Rolandas Paksas ir Lietuvos diplomatas, ES pasiuntinys Rusijoje konservatorius Vygaudas Ušackas.

„3,7 mln... 2,85 mln... 2,0 mln... 1,65 mln. Pasigėrėsime baisiu ir katastrofišku Lietuvos valstybės likimo peizažu, kuris užsibaigs 2080 metais. Ir tai ne niūrios prognozės ar mokslininkų apskaičiavimai laboratorijose. Tai oficiali katastrofa, kurią mes matėme ir matome kasdien dėl kvailumo žmonių, kurie atsakingi už strateginių sprendimų priėmimą mūsų valstybėje pastarojo šimtmečio Lietuvos egzistavimo eigoje.

Galų gale mes turime pripažinti, kad laipsniškas Lietuvos išnykimas yra didžiausia grėsmė jos nacionaliniam saugumui. Tačiau mes neišdrįstame to pripažinti. O laiko mes daugiau neturime, ir būtina priimti sprendimą“, – savo puslapyje Facebooke parašė Vygaudas Ušackas.

Panašiai pasisakė ir eksprezidentas Rolandas Paksas. Jo žodžiais, šiandien Lietuvoje vyksta kampanija pavadinimu „Skatink emigraciją“ – taip jis vertina Lietuvos valdžios veiksmus ir politiką pastaraisiais 20 nepriklausomybės metų.

„Emigracija Lietuvoje tapo įprastu, kasdieniu reiškiniu. Kasdien su tėviške atsisveikina dešimtys ir net šimtai darbingų žmonių. Atrodo, nieko nejaudina, kad lietuviai emigruoja {...} Mano įsitikinimu, tai vyksta dėl visiško piliečių nepasitikėjimo savo valstybe, o taip pat dėl baisios socialinės nelygybės ir dėl valdžios atitrūkimo nuo realybės“,– sako jis.

Tuo metu, kai pirmieji šalies asmenys pastoviai ragina ieškoti nesančių priešų, konfliktuoti su kaimynais, skirti šimtus milijonų eurų gynybai nuo Rusijos ir Baltarusijos, kurios, beje, niekada nereiškė Lietuvai jokių pretenzijų, tokių politikų, kaip Ušackas ir Paksas, žodžiai suteikia viltį, kad Lietuvoje dar ne viskas prarasta ir situacija gali pasikeisti.

P.S.

Baigdami pateikiame nemirtingą profesoriaus Filipo Preobraženskio monologą, kuris šiandien kaip niekada aktualus politiniam Lietuvos elitui.

„Kas ji, ta jūsų suirutė? Senė su kačerga? Ragana, kuri sudaužė visus stiklus, užgesino visas lempas? Jos gi išvis nėra. Ką jums sako šitas žodis? {...} Štai ką: jeigu aš vietoj operacijų kas vakarą pradėsiu savo bute choru dainuoti, būtinai sulauksiu suirutės. Jeigu aš, įėjęs į išvietę, pradėsiu, atsiprašau už išsireiškimą, šlapintis greta unitazo, o taip pat elgsis dar ir Zina bei Darja Petrovna, išvietėje prasidės suirutė. Išvada: suirutė ne klozetuose, o galvose. Vadinasi, kai šie baritonai klykia „mušk suirutę“, aš juokiuos. {...} Prisiekiu jums, man juokinga! Tai reiškia, kad kiekvienas iš jų turi pliekti sau per pakaušį! Ir štai, kai jis išvarys iš savęs visokias haliucinacijas ir užsiims tvartų iškopimu – tiesiogine savo veikla,– suirutė pati dings. Dviem dievam nevalia tarnauti! Neįmanoma vienu metu šluoti tramvajaus liniją ir rūpintis kažkokių ten užsienio driskių likimais ! Tai niekam, daktare, nepavyks padaryti, tuo labiau – žmonėms, kurie išvis savo išsivystyme nuo europiečių atsilikę 200 metų ir iki šiol vis dar neryžtingai užsisega savo nuosavas kelnes!“

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 5 — id: `scraped:rubaltic_lt:eb7cbbe3aec4e08c`

**Title:** Pabaltijo ekspertai prognozuoja Pabaltijo išmirimą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Pabaltijo šalys atsidūrė už išmirimo ribos. Jos tuštėja, tampa demografinėmis dykvietėmis su teritorija be gyventojų. Šių šalių išmirimo procesas jau tapo nesustabdomas. Apie tai kalba pačių Pabaltijo respublikų ekspertai, vargu ar dirbantys „rusų propagandos“ labui.

Dalis Lietuvos teritorijos vis labiau primena Sacharos dykumą, mano Lietuvos socialinių tyrimų centro vyresnysis mokslinis bendradarbis Vidmantas Daugirdas.

„Pagal gyventojų skaičiaus mažėjimo tempus mes pirmaujame ES ir esame vieni iš pirmųjų pasaulio lyderių. Priežastys, atrodo, aiškios: didžiulė emigracija, žemas gimstamumas, visuomenės senėjimas, — sako Daugirdas. — Mums žinomas terminas „demografinis sprogimas“, bet kaip pavadinti procesą, kai kasmet prarandame 2 proc. gyventojų?“

Tai, kas vyksta Lietuvoje, ekspertas vadina demografine depresija ir tvirtina, kad menkai apgyvendintų teritorijų išmirimas — nesustabdomas reiškinys. Tuo metu menkai apgyvendintos teritorijos Lietuvoje sudaro 45 proc. šalies ploto. Pasak Daugirdo, šalyje yra seniūnijų, kuriose per metus negimsta nė vieno vaiko, o miršta 3–4 proc. gyventojų.

„Manau, jog menkai apgyvendintos teritorijos demonstruoja tai, kas mūsų laukia. Atsiranda demografinės dykvietės. Po 15–20 metų visos kaimiškos teritorijos bus menkai apgyvendintos“, — teigia Lietuvos socialinių tyrimų centro darbuotojas.

Tuo metu ir miestuose mažėja gyventojų skaičius. Visi jie mažiau ar daugiau susiduria su šia problema. Klaipėdoje ši tendencija mažiau pastebima, Kaune — labiau, Vilniuje beveik nejaučiama, tačiau augimo nėra niekur. Miestai savo apimtimi mažėja. „Mes turime 22 savivaldybes, kurias galima pavadinti menkai apgyvendintomis, o 2011 metais tokių buvo septynios“, — teigia Vidmantas Daugirdas.

Eksperto išvada liūdna: „Emigracija pareikalavo didesnės dalies potencialiai reproduktyvių gyventojų, tad demografinė duobė pastoviai didės“.

Lietuvos centrinio banko pirmininko pavaduotojas Raimondas Kuodys neseniai pareiškė, kad jei demografinė situacija nesikeis, Letuvoje netrukus liks du su puse miesto, o paskui išnyks ir jie. Lietuvoje egzistuoja dvi ekonomikos — sostinės ir kita, mano ekonomistas. Vilniaus ekonomikos svoris, lyginant su visos šalies, artėja prie 50 proc. Atlyginimai Vilniuje trečdaliu didesni nei vidutiniškai Lietuvoje.

Vilniuje demografinė situacija sąlyginai normali, nes emigravusių į Vakarų Europą sostinės gyventojų skaičių dalinai kompensuoja persikėlę į ją regionų gyventojai. Tačiau Vilnius nėra visa Lietuva, kuri, Centrinio banko pirmininko pavaduotojo manymu, tampa didžiuliu pensionatu, kuriame gyvena „daug ekonomiškai neefektyvių žmonių — pensininkų ir pašalpų gavėjų“. „Jie neturi darbo ir jo neieško“, — sako Raimondas Kuodys.

Lietuvoje netrukus liks trys miestai: Vilnius, Kaunas ir dalinai Klaipėda.

Iš Lietuvos žemėlapio jau dingo šimtai vienkiemių ir kaimų, dabar iš jo išnyksta ir miestai. Miesto teises jau prarado Juodupė, Tiruliai ir Kulautuva, rytoj tokia grėsmė gali iškilti Marijampolei ir Panevėžiui, poryt — Šiauliams, o po to demografinė katastrofa pasieks ir Kauną su Klaipėda.

Apie katastrofišką savo šalies demografinę padėtį kalba ir Latvijos ekspertai. Latvijos universiteto profesorius Leon Taivans, pavyzdžiui, mano, kad latviai kaip etninis vienetas pasmerkti išmirimui. „Kad šis procesas jau vyksta, — akivaizdu, apie tai kalba demografai, ir man atrodo, kad pakeisti šios situacijos neįmanoma. Po 40 metų ši šalis, gali būti, dar bus vadinama Latvija, tačiau čia vyraus visiškai kitokia etninė situacija“, — sako Taivans.

Pagal latvių demografo Ilmar Mežs paskaičiavimus, 2050–2060 metais imigrantų skaičius Latvijoje taps lygus vietinių gyventojų skaičiui, o po to jį viršys. Tai įvyks, jei imigrantai įsikurs Latvijoje be jokio valstybinio skatinimo: etninė struktūra vis tiek keisis įprastu būdu. Latvija nebus latviška — visi latviai išmirs, o latvių kalba taps mirusia.

Savosios nacijos išnykimas gresia ir lietuviams. Viltys, jog lietuviai ir emigracijoje išliks lietuviais, — savęs apgaudinėjimas. Apie tai kalba vėlgi pačių lietuvių ekspertai.

„Kaip rodo tyrimai, trečioji emigrantų karta jau nemoka lietuvių kalbos. Nuo pusės milijono XIX amžiaus pabaigos — XX amžiaus pradžios neliko jokių Lietuvos emigrantų pėdsakų. Baigiantis Antrajam pasauliniam karui, 1944 metų vasarą ir rudenį, kartu su besitraukiančia vokiečių kariuomene į Vakarus išbėgo apie 60 tūkstančių lietuvių. Jie tada keletą metų gyveno Vakarų Europoje, o paskui visi išvyko į JAV, Kanadą, Australiją. O kas sugrįžo? Vienetai“, — teigia Vilniaus edukologijos universiteto dabuotojas Liudas Truska.

Tame, ką reikia daryti siekiant sustabdyti demografinį procesą, tarp Pabaltijo ekspertų prieštaravimų nesimato. Vykdyti aktyvią socialinę politiką, investuoti į gyventojų socialinę apsaugą, padėti vaikus gimdančioms jaunoms šeimoms, finansiškai remti ir skatinti daugiavaikes šeimas, kurti savo šalyje gerai apmokamas darbo vietas, kad žmonėms nereikėtų iš jos išvykti.

„Pagrindinis Latvijos demografijos priešas — tai, tikriausiai, Finansų ministerija. Ji blokuoja bet kokius gerinimus demografinės politikos srityje“, — sako Ilmar Mežs iš Latvijos.

Apie tai, kad vyriausybei nusispjaut link bedarbių, kalba Lietuvos centrinio banko pirmininko pavaduotojas. „Valstybė jiems nepadeda, jų pašalpos juokingos, ir po kiek laiko nutraukiamas jų mokėjimas. Šie žmonės neturi pasirinkimo, jie priversti emigruoti arba ieškoti darbo kuriame nors gyvybingame sektoriuje, pavyzdžiui Vilniuje, ir tai jau mažesnė bėda. Deja, didesnė dalis mūsų jaunimo ir vidutinio amžiaus žmonių ieško laimės Vakaruose, nes savo šalyje nesimato jokios pragmatinės politikos, kuri skatintų kokybišką užimtumą“.

Raimondas Kuodys kaip antisocialinės Lietuvos politikos pavyzdį pateikia Andriaus Kubiliaus konservatorių vyriausybės veiksmus — jos darbo metu iš šalies emigravo rekordinis gyventojų skaičius. Konservatoriai krizės metu bandė ieškoti užsienyje investorių, o saviems bedarbiams pagalbos nesuteikė.

„Prie nevykusių veiksmų kovojant su ekonomine krize, su emigracijos banga, kurią pagimdė krizė, galima priskirti karštus debatus su Andriumi Kubiliumi, kuris vietoj paramos krizės metu darbą praradusiems žmonėms ėmė remti tuos, kurie turėjo darbą, kad jis taptų dar geresnis“, — mano ekonomistas.

Po Andriaus Kubiliaus Lietuvoje ir Valdžio Dombrovskio Latvijoje laikų Pabaltijyje niekas nepasikeitė. Jau antroji Lietuvos vyriausybė ateina valdžion žadėdama socialinių reformų, tačiau perėjimo prie socialinio modelio Lietuvoje taip ir nesimato. Latvijos vyriausybė tebeuždarinėja ligonines, mokyklas ir aukštojo mokslo įstaigas, maitina gyventojus pažadais imtis „nepopuliarių sprendimų“ socialinės politikos srityje ir didina mokesčius.

Pabaltijo valdantieji žudo savo šalis. Apie tai kalba jų gyventojai, bėgliai-emigrantai iš šių šalių, jų ekspertai. Depopuliacija ir nesugebėjimas sukurti realios socialinės politikos — tai tikroji ir didžiausia grėsmė Pabaltijo išlikimui.

Tačiau Pabaltijo „elitas“ pripažįsta tik vieną „grėsmę“ — rusų. Kovodamas su šia liguistoje vaizduotėje gimusia grėsme, jis žudo savo šalis ir tautas. Faktiškai jau nužudė.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 6 — id: `scraped:rubaltic_lt:04f91356c3a6fe86`

**Title:** Per pusantro savo darbo mėnesio Lietuvos Seimo deputatai išeikvojo per 0,5 milijono eurų

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Naujai išrinktieji Lietuvos parlamento deputatai ėjo į rinkimus su šūkiu „Korupcijai — ne !“ Visi žadėjo užtikrinti maksimalų savo veiklos skaidrumą ir nešvaistyti mokesčių mokėtojų pinigų, tačiau nieko panašaus neįvyko. Vos per pusantro mėnesio tautos išrinktieji sugebėjo išleisti per 0,5 milijono eurų. Tai liudija Seimo kanceliarijos duomenys, su kuriais susipažino RuBaltic. Ru.

Kiekvieną mėnesį deputatams skiriama po 793,3 euro taip vadinamoms kanceliarinėms išlaidoms. Naujieji deputatai pradėjo eiti šias pareigas nuo praeitų metų lapkričio vidurio, vadinasi, iki Naujųjų jie turėjo teisę išleisti po 1217,85 euro. Pabrėžtina, jog dauguma deputatų šias lėšas išeikvojo iki paskutinės kapeikos.

Tautos pinigų eikvotojai

Nepaisant to, jog  žiniasklaida neakcentavo šios temos, o valdžia stengėsi nuslėpti didžiules Lietuvos mastu sumas, informacija prasiskverbė viešumon ir tapo prieinama visuomenei. Lietuvos laikraštis „Respublika“ paviešino ypač pasižymėjusių parlamentarų pavardes — tų, kurie „varė“ jiems skirtas sumas iki nulio. Tarp jų:

Kęstutis Bacvinka, Juozas Baublys, Geda Burokienė, Justas Džiugelis, Dainius Gaižauskas, Jonas Jarutis, Laurynas Kasčiūnas, Greta Kildišienė, Gintautas Kindurys, Jonas Liesys, Bronius Markauskas, Laimutė Matkevičienė, Kęstutis Mažeika, Česlav Olševskij, Aušra Papirtienė, Žygimantas Pavilionis, Kęstutis Pukas, Juozas Rimkus, Viktoras Rinkevičius, Gintarė Skaistė, Kęstutis Smirnovas, Lauras Stacevičius, Levutė Staniuvienė, Dovilė Šakalienė, Audrys Šimas, Tomas Tomilynas, Stasys Tumėnas, Gintaras Vaičekauskas, Petras Valiūnas, Jonas Varkalis, Antanas Vinkus.

Išvardintieji parlamentarai išleido visą kiekvienam skirtą sumą: 1217,85 euro. Kaip jie sugebėjo taip kruopščiai „nuvaryti“ iki nulio ją visą ir neapvalią — atskirų svarstymų tema.

Pabrėžtina, jog čia paminėtos pavardės tik tų išrinktųjų, kurie „varė“ tą sumą iki paskutinės kapeikos, tačiau yra ir tokių, kurie taip pat kruopščiai išlaidavo, tačiau dar neišmoko pasiekti nulio: antai Monika Navickienė grąžino šalies biudžetui 4 centus, o Bronislovas Matelis – net 33 centus. Yra ir tokių, kurie dosniai grąžino biudžetui daugiau kaip 1 eurą . Tarp dosniųjų Edmundas Pupinis (1,01 euro), Zenonas Streikus (1,18 euro), Aurimas Gaidžiūnas (1,25 euro), o Algimantas Kirkutis sutaupė valstybei net 1,33 euro.

Iškeliauja milijonai

Vos per pusantro mėnesio naujai išrinktieji deputatai sugebėjo išleisti 568221,07 euro, taigi per 0,5 milijono eurų. Deja, šiandien neįmanoma nustatyti, kiek lėšų išeikvojo perrinktieji deputatai, nes jų išlaidos skaičiuojamos pagal kitokias schemas. Tos lėšos, kurios buvo išeikvotos nuo lapkričio vidurio iki Naujųjų metų, pateko į išeikvotų per 2016 metų paskutinį ketvirtį sumą. Beje, tarp Seimo senbuvių taip pat nemažai įgudusių išeikvoti pinigus iki paskutinio cento.

Remiantis Seimo kanceliarijos darbuotojų turimais duomenimis, galima suprasti, kodėl daugumos tautos išrinktųjų visiškai nejaudina dideli mokesčiai, riebios sąskaitos už šildymą ir pastoviai augančios kainos. Kai kurie nesivaržydami pateikė čėkius, bylojančius, jog pinigai buvo eikvojami įvairių sąskaitų bei komunalinių patarnavimų apmokėjimui.

Šventieji

Tačiau Seime galima aptikti ir stebinančių išimčių: yra ir tokių deputatų, kurie beveik neprisilietė prie šių pinigų. O štai buvusi finansų ministrė konservatorė Ingrida Šimonytė, užsienio reikalų ministrasLinas Linkevičius ir konservatorių vadas Gabrielius Landsbergis nepaėmė nė cento.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 7 — id: `scraped:rubaltic_lt:329794ff5ad01e29`

**Title:** Trampas neketina finansuoti Pabaltijo

**Source:** rubaltic_lt (propaganda)

**Text:**

```
JAV administracija pareiškė, jog ženkliai mažina Valstybės departamento ir tarptautinio vystymosi agentūros USAID biudžetą. Labiausiai bus sumažintas kitų valstybių rėmimo finansavimas. Prezidentas Donaldas Trampas vykdo savo priešrinkiminius pažadus ir nusikrato balasto. JAV biudžeto pinigai bus eikvojami pačių amerikiečių reikmėms, o Pabaltijui ir kitiems parazitams, prisisiurbusiems prie Valstybės departamento kišenės, Vašingtonas parodė špygą taukuotą.

“Viskas gana paprasta: kuo mažiau pinigų išmetama užsieniui, tuo jų daugiau lieka čia,“ — taip pakomentavo paskutinę sensacingą naujieną Baltųjų rūmų biudžeto valdybo direktorius Mis Malvani.

O naujiena tokia: JAV administracija ketina ženkliai sumažinti užsienio politikos finansavimą.

Smarkiai sumažintas bus ir USAID (Jungtinių Valstijų tarptautinio vystymosi agentūra) biudžetas.

Obamos prezidentavimo metu šios žinybos metinis biudžetas sudarė 1 VBP procento. USAID ir įvairių JAV Valstybės departamento viešosios diplomatijos programų finansavimui buvo skiriama per metus 50 milijardų dolerių. O dar per kitas Vašingtono žinybos begaliniams Amerikos sąjungininkams, satelitams ir šeimininkų lėkščių laižytojams visame pasaulyje kasmet nubyrėdavo 36 milijardai dolerių.

Tokiu būdu atsirasdavo kažkokie neribojami, astronomiški skaičiai. Tokių pinigų sočiai užtektų siekiant išgelbėti nuo bankroto Detroitą ir rekonstruoti „surūdijusią juostą“. Vietoj to Amerikos pinigai plaukė visokiems parazitams, organizavusiems prašmatnius Power Point pristatymus su pasakomis apie „demokratijos pastūmėjimą“ ir „transatlantinį solidarumą“.

Keisti tokią padėtį prieš rinkimus žadėjo Donaldas Trampas. Amerikiečių pinigai turi likti Amerikoje, „America First“ — „Amerika pirmiausia“. Globalus dominavimas per brangus JAV piliečiams: jis suvalgo amerikiečių mokesčių mokėtojų pajamas ir kareivių gyvybes. Būtina nutraukti finansavimą Amerikos parazitų — „demokratijos eksportuotojų“ ir išvesti iš jų teritorijų amerikiečių karines bazes. Lai patys kuria savas demokratijas, jei jos jiems reikalingos, ir lai patys save gina, o Amerikai būtina užsiimti savo siena, o ne svetimomis.

Suprantama, kodėl ištisos gaujos amerikietiškų programų dalyvių ir amerikietiško finansavimo siurbėlių, kurias diplomatiškai bei kaustytu kareivio batu rėmė Dėdė Semas, JAV prezidento rinkimuose meldė Hilari Klinton pergalės, o respublikonų kandidatą nesivaržydami dergė. Juk Trampas nedviprasmiškai pareiškė atimsiąs iš jų davinį. Ir blogiausia, jog savo pažadus jis vykdo.

Pirmiausia šis kirvis USAID ir visokeriopų „demokratijos kryžiuočių biudžetui smogs amerikiečių užsienio politikos agentams buvusiose tarybinėse respublikose, kur jų priviso ypač daug, nes šiose vietose driekiasi „naujojo šaltojo karo“ linija ir priešakinės „Rusijos sulaikymo“ ruožas.

Kaip neatsargiai prisipažino buvusi JAV valstybės sekretoriaus padėjėja Europos ir Euroazijos reikalams Viktorija Nuland, vien tik Ukrainos „demokratijos ir pilietinės visuomenės vystymuisi“ Amerika paaukojo 5 milijardus dolerių. O kokie didžiuliai pinigai iš amerikiečių biudžeto buvo tiesiogiai skirti Michailui Saakašviliui, siekiant paversti Gruziją amerikietiško pasirinkimo vitrina!

Pinigai skiriami iki šiol: praeitų metų pabaigoje USAID padidino finansinę paramą Gruzijai ir skyrė gruzinų vyriausybei 22,5 milijono dolerių „demokratiškai kontrolei ir balansui bei atsiskaitomam valdymui“. Nors Michailas Saakašvilis pačių gruzinų paieškomas tarptautiniu mastu, paskutinį kartą jis buvo pastebėtas Trampo inauguracijos metu, kai eksprezidentas visokeriopai stengėsi demonstruoti, kad Respublikonų partijos kandidato pergalė rinkimuose — ir jo politinis atgimimas, o draugas Donaldas — artimiausias bičiulis.

Panašioje situacijoje, kaip buvęs Gruzijos prezidentas ir Odesos srities gubernatorius, atsidūrė ir dabartiniai Pabaltijo lyderiai. Jiems belieka nekviestiems skristi į Vašingtoną, užsikarti ant Baltųjų rūmų tvoros ir mojuoti rankomis, tikintis kad amerikičių lyderis juos pastebės. Nes, nors net patarėjai Trampo prezidentavimo metu ir rodė jam žemėlapyje Lietuvą, Latvija ir Estiją, šis taip ir neįsiminė tų Amerikai nereikalingų provincijų šiame regione ir niekam nepaskambino.

Ir tas amerikietiškas Pabaltijo politikų, kaip ir visų kitų, finansavimas priėjo liepto galo. O finansavimas buvo svarus, prisiminkime bent jau Valstybės departamento ir USAID pastangas. Mažai rasime Pabaltijyje politinių veikėjų, kurie nebūtų dalyvavę įvairiuose jaunų lyderių kursuose, stažuotėse, kvalifikacijos kėlimuose.

Visi jie praėjo šiais keliais: skraidė už vandenyno ir keliavo po Ameriką šios šalies mokesčių mokėtojų lėšomis — mokėsi tenykščio gyvenimo meno. Dalia Grybauskaitė — Fulbraito stipendijos gavėja ir Džordžtauno universiteto absolventė. Ne, savosiose kišenėse jie neieškojo pinigėlio mokslams JAV ir naudingų pažinčių užmezgimui su amerikiečių elito atstovais.

Tačiau visi tie kursai ir stažuotės perspektyviems Rytų Europos nacionaliniams kadrams — JAV kišeninės išlaidos, taigi menkniekis, prisiminus, jog Vašingtonas pats užsiminėjo partine statyba, „bruko“ jam tinkamus kandidatus į prezidentų kėdes, kūrė ir finansavo masines informacijos priemones.

Lietuvos konservatoriai sukūrė partiją („Tėvynės Sąjunga — Lietuvos krikščionys demokratai“), kuri visiškai kopijuoja JAV Respublikonų partiją. Latvijos „Vienybės“ partija buvo suramstyta iš kelių nacional-liberalių projektų, tiesiogiai vadovaujant amerikiečių ambasadai. Ruškesni šios partijos atstovai savo karjeros laiptais kilo dėka bendradarbiavimo su amerikiečiais. Pavyzdžiui, eurodeputatas ir buvęs Latvijos gynybos bei užsienio reikalų ministras Artis Pabriks ne vienerius metus „valgė“ Soroso latvių fondo (visuomeninis politinis centras Providus, atvirumo bendruomenė Delna) pinigus.

Ir taip jau sutapo, kad visi tie dolerių „valgytojai“: Pabriks, Rinkevič, Grybauskaitė ir kiti — garsiausiai Pabaltijyje klykia apie „rusų grėsmę“ ir „atslenkančią rusų agresiją“. Tačiau dabar sočiai maitintiems amerikiečių tarnams ateina juodos dienos. Už vandenyno sėdintis Trampas parodė jiems špygą taukuotą ir atsisakė apmokėti vasalų paslaugas.

Dabartinis Vašingtono lėšas švaistančių organizacijų biudžetų apkarpymas — pirmoji kregždė amerikiečių klientūros tragiškuose pokyčiuose. Paskutiniaisiais Obamos prezidentavimo metais amerikiečių karinių pajėgų Europoje biudžetas buvo padidintas keturis kartus, iki 3,4 milijonų eurų, — Trampas jau pasakė, jog tai pernelyg daug: JAV kariškių buvimą Europoje ir jų finansavimą būtina mažinti. Amerikos įnašas į NATO neturi sudaryti 80 proc. jo biudžeto — tai išvis pasenusi organizacija, šaltojo karo reliktas.

Jeigu europietiškiems sąjungininkams reikia NATO, lai patys jį finansuoja ir patys gina, — kodėl Amerika turi išlaikyti rotacijos batalionus Pabaltijyje, priešraketinės gynybos sistemą, kurią įkurdinti regione nori Dalia Grybauskaitė? NATO kibersaugumo centra Taline? NATO strateginių komunikacijų centrą Rygoje? Eiliniams amerikiečiams ir Talinas, ir Ryga — greičiausiai kurių nors valstijų miestai.

Ir svarbiausia: naujoji JAV administracija nesuinteresuota „Rusijos sulaikymu“. Koncepcija pasikeitė. Pagrindinė JAV konkurentė — Kinija, o ne Rusija, o su Putinu Trampas norėtų susidraugauti.

Todėl „sanitarinės užkardos“ paslaugos nereikalingos — didmeninė rusofobijos ranga nenusimato.

Pinigų jums daugiau neturime. Tačiau jūs tame savo Pabaltijyje laikykitės!

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 8 — id: `scraped:rubaltic_lt:2d40fc2d020f183c`

**Title:** Lietuva peržengė depopuliacijos nesugrįžimo ribą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuva tebepraranda savo piliečius. Kas valandą 4 –5 žmonės atsisveikina su savo pabaltijietiška tėvyne ir išvyksta į Vakarų Europą. Iš žemėlapio išnyksta ištisi geografijos objektai, dingsta gyvenvietės. Jei tokia griaunanti tendencija tęsis, Lietuvoje liks 2,5 miesto, perspėja respublikos Centrinio banko pirmininko pavaduotojas Raimundas Kuodis. Bet galų gale ir jie išsivaikščios.

Lietuva peržengė nesugrįžimo ribą, skelbia pavojų respublikos Centrinio banko pirmininko pavaduotojas Raimundas Kuodis, ir šalyje beliks 2,5 miesto. Diskusijos „Socialinė Europa — nauji iššūkiai― parlamente metu Kuodis dar kartą diagnozavo daugelio ekonomikų, tame tarpe ir pabaltijietiškų, chronines ligas, — didžiulę regionų vystymosi disproporciją, kuri iššaukia emigraciją.

Lietuvoje, ekonomisto manymu, egzistuoja dvi ekonomikos: sostinės ir kita. Lyginamasis Vilniaus ekonomikos svoris šalies atžvilgiu artėja prie 50 proc., o atlyginimai sostinėje trečdaliu didesni, nei respublikos regionuose.

„Tai (Vilnius — RuBaltic.Ru pastaba) išties atskira ekonomika. Kodėl čia santykinai viskas gerai? Todėl, jog čia neblogas demografinis ciklas, ir jis labai svarbus. Politikai tai ignoruoja ir savo samprotavimuose apie emigraciją, ir kalbėdami apie Darbo kodeksą. Paklausos klausimas, kuris itin svarbus besivystančiam bizniui, ignoruojamas, — kalba Raimundas Kuodis.

Ekonomistas bando įkalti į Seimo narių galvas elementarią tiesą: paklausos šaltinis, kuris reikalingas ekonomikos augimui, —  mokesčius mokantys piliečiai. Sostinėje jų dar yra. Pastaruosius penkerius metus Vilniaus gyventojų skaičius praktiškai nekito. Vietoj išdūmusių į Vakarų Europos šalis vilniečių sostinėje įsikūrė bėgliai iš regionų. Miestas laikosi.

Bet yra ir kita Lietuva — regionų Lietuva. „Ten kitoks ciklas: žmonės išvyksta dėl vidaus ir išorinės emigracijos. Jie persikelia. Išvyksta paklausa. Krentant paklausai, mažėja darbo našumas, o tai neleidžia didinti atlyginimų, auga išlaidos, skirtos prekėms ir paslaugoms, — pažymi Kuodis. Didžioji Lietuvos dalis, Centrinio banko pirmininko pavaduotojo manymu, tampa didžiuliu pensionu, kuriame „daug ekonomiškai neefektyvių žmonių — pensininkų arba žmonių, kurių pragyvenimo šaltinis — pašalpos. „Jie neturi darbo, bet jo ir neieško, — teigia ekonomistas.

Pagal prognozes, gerame cikle gali likti Vilnius, Kaunas ir dalinai Klaipėda, kiti regionai sunyks, beviltiškai konstatuoja Kuodis. Situacija išties negrįžtama, atgręžti demografinį procesą per trumpą laiką neįmanoma, — prieina išvados Centrinio banko pirmininko pavaduotojas.

Biznio terpės gerinimas, užsienio investicijos, eurofondų eikvojimo efektyvumo augimas ir kitos protingos kvailystės, apie kurias taip mėgsta postringauti vietiniai valdininkėliai, nepajėgios ištaisyti susiklosčiusios situacijos. Pabaltijis baigia nugyventi savo amžių, tampa pensionu, rytų europietiškais senelių namais.

Lietuva, Eurostato duomenimis, muša gyventojų skaičiaus mažėjimo tarp Europos šalių antirekordus. Kas valandą 4–5 lietuviai atsisveikina su savo tėvyne, kas dieną emigruoja apie 100 žmonių, per metus — 35 tūkstančiai. Tas pats Eurostatas prognozuoja: per artimiausius 40 metų Lietuvos gyventojų skaičius sumažės 38 proc. 2020–2030 metais pensininkais taps gausiausia respublikos gyventojų karta, o į darbo rinką ateis žemiausio gimstamumo karta.

Lietuviai galutinai atsisakė Lietuvos. „Jaunimas mokosi visame pasaulyje! Tai kam reikalinga ta Lietuva? Kad išlaikytų parlamento deputatus, kurie priverčia žmones emigruoti? Yra apie ką pamąstyti. Aš šimtu procentų pritariu emigracijai, — rašo jaunas, sėkmingai besidarbuojantis Lietuvos dizaineris Juozas Statkevičius, — 25 metai laisvės, o pokyčių jokių! Viskas tik blogyn! Vien tik pažadai ir tušti, nieko nereiškiantys žodžiai! Blogai! Aš vėl ketinu iš čia bėgti! Iš šalies, kur nacionalinis patiekalas — kitas lietuvis! Geriau mylėti Lietuvą iš toli, iš tos šalies, kurioje galima uždirbti, kurioje šilta ir kurioje iš motinos pensininkės niekas neatims pinigų. Trūksta žodžių. Reikia veikti — ruošti lagaminą, nes čia nieko nebus! Ir jums patariu! Bėgam iš čia! Nes ateis laikas, neišleis! Bėgam!

„Metas išdumti, — kreipiasi į lietuvius jų kūrybinė inteligentija. Bereikalingos pastangos. Lietuviai aktyviai „dumia ― be jokių raginimų, kaip kas išmano . Vieni keliasi iš provincijos į Vilnių, kiti iš šio europietiško pakraščio skuodžia į Vakarų Europą. Svarbiausia: „branduolys„ pasiglemžia ― periferiją.

Įveikti šią griaunančią emigracijos tendenciją vis dar nepavyksta. Pabaltijo respublikos ateitis — ta pati tamsa tunelio gale.

Lietuva taps dykviečių ir pelkių regionu. Kurį laiką šioje teritorijoje be žmonių dar šiek tiek krutės 2,5 miesto — Vilnius, Kaunas, pusė Klaipėdos. Dar sėdės ir kivirčysis deputatai, dar šmirinės juos aptarnaujantis personalas. Tačiau ateis laikas, kai ir jie išdums.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 9 — id: `scraped:rubaltic_lt:9d40b0e6c17e7e75`

**Title:** NATO kareiviams Pabaltijyje leidžiama elgtis kaip okupacijos zonoje

**Source:** rubaltic_lt (propaganda)

**Text:**

```
NATO kariškiai Pabaltijyje sukėlė naują incidentą. Sekmadienio naktį penki svetimšaliai kareiviai sukėlė muštynes su Klaipėdos jaunimu. Tai ne pirmos NATO kariškių sukeltos riaušės, ateityje tokių incidentų bus daugiau: pavasarį Pabaltijo šalyse pradės įsikurti daugianacionaliniai NATO batalionai. Nujausdamos, jog konfliktų su vietiniais gyventojais nepavyks išvengti, Pabaltijo valdžios visokeriopai gina svetimšalius kariškius. Jiems negali būti taikomi vietinių BK straipsniai, na, o tie piliečiai, kurie išdrįs susiginčyti su NATO kariūnais, neabejotinai bus paskelbti Kremliaus šnipais ir provokatoriais.

Poilsio dienos Klaipėdoje nebuvo ramios. Girti NATO kariškiai susimušė su vietiniais gyventojais ir policijos darbuotojais. Sekmadienio naktį penki NATO kariai prie miesto naktinio klubo susikivirčijo su vietiniu jaunimu. Mušeikos atsisakė paklusti į įvykio vietą atskubėjusiems teisėtvarkos darbuotojams. Siekiant nuraminti agresyvius kariškius, atvykę policininkai buvo priversti panaudoti elektros šokerius.

Amerikiečių kariškiai pasižymėjo siautėdami Druskininkų akvaparke, Lietuvos valstybinės vėliavos išniekinimu, kurią nuplėšė Kaune nuo prokuratūros pastato, muštynėmis.

Panašiai sąjungininkai „tarnavo“ ir kaimyninėse respublikose. 2014 metais Latvijos Ventspilio meras Aivars Lembergs pareiškė, kad užsienio šalių kariškiai „elgiasi lyg okupantai, nepripažįstantys Latvijos suvereniteto ir įstatymų“. „Prisilakę, jie (NATO jūreiviai — RuBaltic.Ru pastaba) šlapinosi viešose vietose ir ant vitrinų, vėmė, viešai gėrė stipriuosius gėrimus, kas neleistina. Jie draskė nuo klombų gėles ir dovanojo jas prostitutėms,“ — piktinosi Ventspilio šeimininkas, žadėdamas skųsti karių elgesį tuometiniam NATO generaliniam sekretoriui Andersui Fogui Rasmusenui.

Ypatingo rezonanso susilaukė praeitų metų lapkričio įvykis Latvijoje. Tada NATO kariškiai sukėlė muštynes Rygos McDonald‘s. Du girti Didžiosios Britanijos gvardijos grenadierių pulko kareiviai išprovokavo konfliktą su juridinės firmos 23 metų darbuotoju. Lyg ir kasdienis reiškinys, tačiau paviešinti jį nepatingėjo The Telegraph.

Pavasarį, kaip buvo nutarta 2016 metų liepą Varšuvoje vykusio NATO samito metu, Pabaltijo šalyse pradės įsikurti daugianacionaliniai NATO batalionai — jie turės apsaugoti šias respublikas nuo „rusų agresijos“ užsienio šalių kariškių skaičius ženkliai ūgtels, padažnės ir jų sukeltų incidentų. Nujausdami, jog svečių „šeimininkavimo“ nebus išvengta, Pabaltijo funkcionieriai ėmė ruošti informacinį foną, kad, eilinio kariškių šėliojimo atveju, visą kaltę būtų galima suversti Kremliui.

Estijos informacijos departamento vadovas Mikas Maranas suskubo įtarti Rusiją, jog ji specialiai provokuoja NATO kariškių muštynes vietiniuose baruose jų diskreditavimo tikslais, o taip pat bando panaudoti taip vadinamus medaus spąstus — vietines moteris, kurios turi sužavėti ir užverbuoti užsienio šalių kariškius.

„Sklinda kalbos, kad vietinių gyventojų nedžiugina šie kareiviai. O ten bus 800 jaunų britų karių. Jie iš savo bazių važinės į miestus. Akivaizdu, lankysis aludėse. Mes negalime užkirsti kelio kai kurioms peštynėms, kurias gali inicijuoti priešingoji komanda, kaip mes visa tai vadiname Estijoje,“ — Miraną cituoja britų dienraštis The Times. Jokių argumentų šiuo klausimu valdininkas, kaip žinia, nepateikia.

Patogus požiūris — iš anksto sukurti kaltumo prezumpciją visiems įveltiems į incidentus su užsienio kariūnais. Jei tave įžeidė arba sumušė girtas NATO karys — vadinasi, tu esi rusų šnipas ir provokatorius. Jei iš moters nekantrūs sąjungininkai reikalauja artumo — ta moterėlė neabejotinai yra „Kremliaus Mata Chari“.

Pabaltijo šalys pripažino ypatingą JAV kariškių statusą. Nuo šiol priimanti šalis įsipareigoja sukurti jiems rojaus sąlygas su daugybe lengvatų: mokesčių režimą be PVM, be pardavimo ir akcizų mokesčių, o taip pat specialias parduotuves, kuriose prekės bus realizuojamos naudingomis kainomis. Be to, JAV kariams bus taikomis dalinis imunitetas Pabaltijo respublikų baudžiamojo persekiojimo atveju.

Įkurdindamas savo karius svetimoje teritorijoje, Vašingtonas reikalauja, kad priimanti šalis „perleistų“ jam teisę bausti už nusižengimus ir nusikaltimus. Tik Generalinei prokuratūrai pareikalavus pabaltijiečiams bus suteikta galimybė savarankiškai smerkti paišdykavusius užsieniečius.

Ir lai ta amerikiečių Femidė, kuriai nebūdingas humaniškumas ir kuri visada griežta, savų nusikaltusių kariškių atžvilgiu rūpestingai baltu raiščiu užsidengia savo bešališkas akis. Priminsime, jog praeitų metų pavasarį JAV jūrų pėstininkas Okinavoje buvo pripažintas kaltu dėl vietinės moters išprievartavimo. Amerikiečių tribunolas skyrė jam piniginę baudą ir tik 2,5 metų pataisos darbų. Japonų spaudos duomenimis, 1972–2014 metais amerikiečių kariškiai ir Okinavos bazes aptarnaujantis personalas įvykdė 5862 nusikaltimus, tame tarpe 737 sunkius: nužudymus, išprievartavimus, apiplėšimus, padegimus. Nuobaudos už šiuos nusikaltimus atskirais atvejais buvo nuostabiai švelnios.

Ženkliai šiais metais padidėsiantis jų skaičius neišvengiamai sukels naujus konfliktus su vietiniais gyventojais. Apmaudu, jog ir buvusių ir būsimų konfliktų atžvilgiu Pabaltijo valdžios aklai gina užsienio šalių kariškių pozicijas.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 10 — id: `scraped:rubaltic_lt:b58e2dbaea512efa`

**Title:** Lietuviai atsisako Lietuvos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
2017-ieji metai dar tik prasidėjo, o Lietuva jau muša europietiškos emigracijos rekordus, jos pačios pasiektus praeitais metais. Lietuviai iš savo šalies skuodžia vis sparčiau: beveik visi Lietuvos moksleiviai, tapę pilnamečiais, ketina bėgti iš gimtosios šalies, Lietuvos kultūros veikėjai ragina gyventojus emigruoti, o „nepriklausomybės dienos“ — valstybinės šventės ir oficialios poilsio dienos  tampa Lietuvos gyventojams proga išvykti į kaimynines šalis. Didysis lietuvių tautos Išėjimas vis labiau primena keleivių bėgimą iš skęstančio laivo.

„Nesunku pastebėti, jog maistą mes perkame Lenkijoje, dirbame Norvegijoje, Anglijoje. Poilsiaujame Ispanijoje, Turkijoje. Jaunimas mokosi visame pasaulyje! Tai kam reikalinga ta Lietuva? Kad išlaikyti parlamento deputatus, priverčiančius žmones emigruoti? Čia jau tema apmąstymams. Aš visu šimtu procentu už emigraciją, — parašė savo tinklalapyje dizaineris Juozas Statkevičius, — jau dvidešimt penkeri metai, kai mes laisvi, o pokyčių jokių. Viskas blogyn. Tik pažadai ir nieko nereiškiantis tuščiažodžiavimas! Blogai! Aš vėl ruošiuosi iš čia bėgti! Iš šalies, kurioje nacionalinis patiekalas — kitas lietuvis! Geriau mylėti Lietuvą iš toli, iš tos šalies, kurioje galima uždirbti, kur šilta ir kur iš motinos-pensininkės niekas neatims pinigų (ir vietoj 50 atimtų sugrąžins 14). Trūksta žodžių, ką gi, reikia veikti — ruošti lagaminą, čia nieko nebus! Ir jums patariu! Bėkim iš čia! Nes ateis laikas, kai neišleis! Bėgam!“

Šis madingo dizainerio raginimas bėgti sukėlė Lietuvos informacinėje erdvėje tikrą žemės drebėjimą. Juozo Statkevičiaus sielos šauksmą imta cituoti, jis pateko į tinklalapius, tapo intensyviai svarstomas Lietuvos Respublikos žiniasklaidos. Ir, žinoma, susilaukė „kontrpropagandinio atkirčio“. Negi išgirdę tokį lietuviškosios dabarties šmeižtą galėjo nutylėti partijai ir vyriausybei ištikimi Lietuvos kultūros veikėjai?

„Brangūs šios žvaigždės liga susirgusios šiukšlės gerbėjai, išvykite iš čia visi kaip galima greičiau ir netrukdykite mums ramiai įvesti tvarką savo kieme. Nes kuo mažiau Lietuvoje bus tokių utėlėtų nepilnapročių, kaip dauguma tų, kurie žavisi šios menkystos kūryba, tuo geresnis bus gyvenimas mūsų šalyje,“ — taip sureagavo į meno pasaulio kolegos pareiškimą lietuvių režisierius ir scenaristas Jonas Banys.

Įpykusio patrioto atkirtis Lietuvos šmeižikui — giesmė, skaityti kurią — vien tik malonumas. Režisierius Banys nebando paneigti nusikaltėlio-dizainerio žodžių ir įrodinėti, kad Lietuvoje ne viskas taip jau blogai. Jo argumentai paprasti, gal net primityvūs. Tokią Lietuvą esą sukūrė patys lietuviai. O jei tas gaminys nepatinka — čiuožkit iš čia, ir bėra ko valdžios koneveikti, jei jūs patys esate šios gėdos kaltininkai.

„Ne valdžia, o patys Lietuvos gyventojai 27 metus apvaginėjo valstybę, o dabar piktinasi, kad ji nėra tokia gera, kaip ta, kurią sukūrė kitur gyvenantys žmonės... Jei visus tuos 27 metus būtumėte mokesčius mokėję taip sąžiningai, kaip estai, mūsų šalis būtų buvusi dukart turtingesnė. Dukart. Dukart būtų didesnės pajamos, pensijos, mokytojų ir gydytojų atlyginimai, infrastruktūros investicijos. Viską ištąsė, suvalgė ir dar prišiko ant stalo. Nepergyvenkite: mes, čia liekantys, visa tai iškuopsime. O jūs čiuožkit iš čia ir niekada negrįžkite,“ — išvykstantiems iš Lietuvos palinkėjo tautiškai mąstantis kultūros veikėjas.

Lietuva kasmet praranda 1,5 proc. savo gyventojų. Kiekvieną valandą iš šios šalies išvyksta 4–5 žmonės, kasdien — 100 žmonių, kasmet — 35 tūkstančiai. Lietuvos statistikos departamento duomenimis, 2017 metų sausio 1 d. šalyje gyveno 2,849 mln žmonių, o tai 39,2 tūkst. mažiau negu pernai. Du trečdalius prarasto skaičiaus sudaro emigrantai.

Tokia buvo situacija pagal 2016 metų rezultatus. Tačiau naujieji metai atnešė ir naujus rekordus. 2017 metų sausio mėnesį paduota 15 tūkstančių išvykimo iš Lietuvos deklaracijų. Tai tris (tris!) kartus daugiau, nei pernai: 2016 metų sausio mėnesį paduotos 5082 deklaracijos, šių metų sausį — 15388. Arba emigracija per metus išties ūgtelėjo tris kartus, arba anksčiau realūs emigracijos skaičiai buvo smarkiai sumažinti.

Departamento duomenimis, daugiau nei pusė emigrantų — 52 proc. išvykusių iš Lietuvos per pirmąjį 2016 metų pusmetį — 18–35 metų jaunimas. Šiuos duomenis patvirtina ir sociologai.

„Nustatytas gąsdinantis skaičius: 90,4 proc. 15–19 metų amžiaus respondentų pareiškė, kad atsiradus palankioms sąlygoms jie iš Lietuvos išvyks,“ — teigia Sociologijos centro ‚Baltijos Tyrimai“ direktorius Gintaras Chomentauskas. Sociologo manymu, Lietuva sparčiai praranda savo ateitį: Lietuvos Respublika jau nėra ta šalis, kurioje gyvenant galima tikėtis geresnės ateities.

Nepasitikėjimas savo šalimi pasireiškia ne tik iš jos emigruojant. Jis pasireiškia ir smulkmenose: eilinių lietuvių „kasdienybės struktūrose“, kai jie savo buitiniu elgesiu, to nesuvokdami, trenkia savo valstybei skambų antausį.

Praėjusiais metais Lietuvos konservatoriai jau piktinosi elgesiu savosios tautos, kuri pagrindines tautines šventes — Valstybės atkūrimo ir Valstybės nepriklausomybės atkūrimo dienas — masiškai panaudoja išvykoms į Lenkiją dešrų pirkti. Tačiau eiliniai lietuviai į politikų pasipiktinimą atsako savo pasipiktinimu. „Gatvėje šalę pirkėjai negailėjo piktų žodžių Lietuvos valdžios adresu. Buvo siūloma nufotografuoti lietuvius, nešančius produktus iš lenkų bazių, ir pasiųsti nuotraukas prezidentei Daliai Grybauskaitei. Turi juk ji žinoti, kaip žmonės švenčia Vasario 16-ąją,“ — pasakojo lietuviškojo Delfi reporteris apie tai, kaip eilinę Nepriklausomybės dieną „šventė“ lietuviai eilėse lenkų Suvalkuose.

Tačiau šiais metais lietuviškojo valstybingumo architektai susilaukė iš tautiečių dar didesnio pažeminimo: savo šventąsias valstybines šventes lietuviai panaudojo išvykoms į Baltarusiją. Būtent Vasario 16-ąją didžiausias tautiečių skaičius vienai dienai vyko apsipirkti „paskutinio Europos diktatoriaus“ batu prispaustoje šalyje. Ir būtent tą dieną Dėdulę Landsbergis, apsireiškęs pamėgtame Pasirašinėtojų rūmų balkone ir sveikindamas lietuvių tautą su 99-osiomis valstybės atkūrimo metinėmis, mokė „atsilikusius homo sovietikus“ baltarusius kaip reikia gyventi. Kažkokią nesuvokiamą tragikomediją kūrė „Patriarchas“...

Iš atskirų gabalėlių galima sudėlioti sukrečiantį vaizdą. Pasauliniu mastu rekordinė emigracija, 90 proc. lietuvių vaikų, besiruošiančių atsisveikinti su Lietuva, tų vaikų tėvai, kuriems svarbiausia valstybinė šventė, o tiksliau — nedarbo diena, reikalinga išvykai pas kaimynus pigiau apsipirkti.

Lietuva neturi ateities, nes Lietuva praranda lietuvius. Vis mažiau lietuvių nori gyventi Lietuvoje, o jos jaunimas nenori tokio likimo. Todėl Lietuvos ateitis — dykvietės ir pelkės, greta kurių šmirinės tik valdininkai, deputatai ir juos aptarnaujantis personalas. Nesimatys tokiose dykvietėse jokio gyvybės ženklo — tik retsykiais pasigirs liūdnas, širdį draskantis kauksmas. „Kas per garsai iš pelkių sklinda, Berimorai?“ — „Tai Dalia Grybauskaitė perspėja NATO sąjungininkus apie „rusų grėsmę“ Lietuvai“.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 11 — id: `scraped:rubaltic_lt:1a420055eafe376f`

**Title:** Lietuvos politikai lenktyniauja rusofobijos varžybose

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Vilniaus meras Remigijus Šimašius mano, kad Rusija — tai žudinės kitų šalių teritorijose ir prievarta šeimoje. Rusofobijos priepuolį Šimašius patyrė išgirdęs pirmosios Lietuvos Seimo pirmininko pavaduotojos Rimos Baškienės pasisakymą, jog iš Rusijos yra ko pasimokyti.

„Mes manome, kad Rusija — blogis. Nieko panašaus. Ten daug yra gero, yra ko pasimokyti,“ — pareiškė Lietuvos Seimo pirmininko pavaduotoja Rima Baškienė, atstovaujanti Lietuvos valstiečių ir „žaliųjų“ sąjungai.

Šie žodžiai lietė švietimo sritį, kurią, įstamdavių valdžios įpareigota, kuruoja Baškienė. Ji rekomendavo pasidomėti rusų patirtimi ir pareiškė, jog „dvasingumas — švietimo reformų pagrindas“.

Sureaguota buvo žaibiškai. Lietuvos žiniasklaida vieningai įjungė pavojaus signalą ir ėmėsi pranešinėti, jog valdančiosios partijos lyderiai leidžia sau svaidytis prorusiškomis frazėmis ir „keliaklupsčiauja prieš prezidentą Putiną“.

Ir Lietuvos politikai neilgai tylėjo. „Landsbergininkai“ iškart įžvelgė, jog Lietuvos vyriausybėje darbuojasi „penktoji kolona“, o Rimos Baškienės žodžiuose — ryšį su, jų nuomone, nepakankama Lietuvos užsienio ministerijos veikla remiant Ukrainos sąjungininkus paskutiniųjų mūšių Donbase metu.

Lietuvos užsienio reikalų ministras Linas linkevičius nors ir pasakė, kad pagrindinė konflikto kaltininkė yra Rusija, tačiau paragino susirėmusias šalis nutraukti ugnį prie Avdejevkos. „Tarptautinė visuomenė skiria Ukrainai dėmesio vis mažiau, todėl mes dėsime dar daugiau pastangų,“ — pareiškė Linkevičius Ukrainos ambasadoriui Lietuvoje, apgailestaudamas, jog situacija primena 2014-uosius metus.

Tokia Lietuvos URM reakcija papiktino konservatorius. „Rusija — agresijos ir konflikto pradininkė“, ir viskas?! O kur Putino palyginimas su Hitleriu, kur žodžiai apie „blogio imperiją“, kur raginimas „numesti ant Maskvos neutroninę bombą“?

Ir štai „landsbergininkai“ už viso šio jau mato gauruotą „Maskvos ranką“ ir baisią išdavystę. „Kas tai: blaidžiojimas neapgalvotao pasielgus, URM bandymas keisti Lietuvos užsienio politikos kryptį ar nuoseklus naujosios žaliai raudonos koalicijos poelgis? — piktinasi buvęs Lietuvos URM vadovas, konservatorių atstovas Seime Audronius Ažubalis, kolegų ir Linkevičiaus raginimu nutraukti abi puses ugnį. — Juk tuo pačiu metu Seimo pirmininko pavaduotoja Rima Baškienė pareiškė, jog mes darome iš Rusijos monstrą, nors iš tikrųjų ten yra daug ko puikaus, ko mums vertėtų pasimokyti“.

Toliausiai šį kartą rusofobiškai spjauti sugebėjo Liberalų sąjūdžio lyderis, Vilniaus meras Remigijus Šimašius, neabejotinai patyręs priepuolį. „Valstiečių lyderiai pareiškia: „Rusijoje yra daug gero“. Tačiau man atrodo, kad Rusija turi tik vieną gerą dalyką — žmones, kuriems nepatinka, kas dedasi jų šalyje,“ — parašė Šimašius savo Facebook puslapyje.

„Visais laikais Rusijos gyventojai gelbėjosi nuo savo carų ir rasdavo prieglobstį Lietuvoje arba kitose Europos šalyse,“ — teigia Lietuvos liberalų lyderis. Jo nuomone, Rusijoje gerai ten, kur nėra žmonių. „Aš ten buvojau, daug kur pavaikščiojau. Lankiausi už Uralo, Kamčatkoje ir Altajuje. Gražu ten, kur nėra žmonių,“ — pareiškė Šimašius, primesdamas Lietuvos „žaliesiems“, kad jiems, reikia manyti, patinka „dvasingas požiūris į žudynes kitų šalių teritorijose ir prievartą šeimoje“.

Nes Rusija jam — žudynės kitose šalyse ir prievarta šeimoje. Nieko gero toje Rusijoje nėra — tik žmonės, kuriems Rusija nepatinka. Gerai Rusijoje tik ten, kur nėra žmonių. O dar geriau — numesti ant Rusijos neutroninę bombą, kad gražios vietos už Uralo, Kamčatkoje, Altajuje išliktų, o rusų ten nebūtų.

Atkreiptinas dėmesys į tai, jog šį rusofobijos priepuolį rimtas ir neeilinis politikas patyrė išgirdęs nedrąsų kito politiko bandymą pakeisti savo tautiečių požiūrį į Rusiją, kitu — santūresniu ir apgalvotu. Nieko baisaus nebuvo pasakyta — tik kad nereikia daryti iš Rusijos monstro, nes ten ne vien blogis, yra ko ir pasimokyti. O reakcija į šiuos žodžius — elito ir žiniasklaidos smerkiančių pamokymų uraganas, kaltinimai, sąmokslų teorijos ir įžeidinėjimai.

Tikrasis Lietuvos patriotas turi gyventi prisilaikydamas priesaikos Dėdulės Landsbergio, kuris praėjusį rudenį atsakingai pareiškė, kad Rusija — ji „visa š...e“. Tik šios intelektualo nuostatos prisilaikant reikia kalbėti apie Rusiją, o ne plepėti, kad ten ne viskas bloga ir net verta šio to pasimokyti. Ne, viskas blogai, viskas! Ten prievarta šeimoje, žudynės, ir žmonės, gelbėdamiesi, iš ten bėga. Viena, kas ten gali būti gero, — Rusijos nemėgstantys žmonės. Mes juos visus sukviesim į Vilnių, į Laisvosios Rusijos forumą, o kas dėl kitų žmonių — geriausia, kad jų Rusijoje išvis nebūtų. Tai pilka, nieko apie gėrį nesuvokianti masė, be kurios ir Altajus su Kamčatka būtų daug gražesni.

Rusofobija Lietuvai — būtinas politinis poreikis. Ir neabejotinai — liga. Tai Lietuvos elito liga, kuria politiškai verta sirgti. Todėl Landsbergis, Ažubalis arba Šimašius nesigydo. O kai liga negydoma, ji progresuoja.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 12 — id: `scraped:rubaltic_lt:daeb6219ab735e4c`

**Title:** Grybauskaitė tiki, kad Trampas paskambins

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos prezidentė Dalia Grybauskaitė paragino Europos Sąjungos kolegas atkreipti rimtesnį dėmesį į JAV prezidento Donaldo Trampo siunčiamus signalus. Nepaisant visiško naujojo JAV lyderio abejingumo Rytų Europos, tame tarpe ir Lietuvos, atžvilgiu, ponia Dalia nepraranda vilties, kad Donaldas persigalvos ir sugrįš pas pačius ištikimiausius sąjungininkus.

Pirmomis dienomis savo sensacingos pergalės prezidento rinkimuose Donaldas Trampas pasikalbėjo telefonu su Turkijos, Pietų Korėjos, Izraelio, Egipto, Japonijos, Australijos, Airijos ir Indijos lyderiais. Po to Trampas paskambino daugiausia problemų JAV užsienio ir vidaus politikai keliančių šalių lyderiams: Meksikos, Rusijos, Kinijos. Su Rusijos prezidentu Vladimiru Putinu naujasis JAV prezidentas pasikalbėjo du kartus ir jau anonsavo susitikimą su juo Islandijos Reikjavike.

Nuo pirmųjų išrinkimo į aukščiausias pareigas dienų Trampas ėmė demonstruoti nepagarbą Senajam Pasauliui. Iki pat inauguracijos naujasis JAV prezidentas demonstratyviai atsisakė bendrauti telefonu su Vokietijos kanclere Angela Merkel (kuri kritikavo Trampą rinkiminės kampanijos metu) ir Prancūzijos prezidentu Fransua Olandu, pareiškusiu, jog žiūrint į Trampą jam norisi vemti, ir tinklalapyje bendravusiu su britų užsienio reikalų ministru Borisu Džonsonu, pavadinusiu Trampą bepročiu.

Tiesa, pirmąja užsienio valstybės lydere, kurią, tapęs Baltųjų rūmų šeimininku, priėmė Trampas, tapo Didžiosios Britanijos premjerė Tereza Mej. Tačiau ir šis susitikimas europiečiams atrodė abejotinas: Donaldas Trampas pritarė britų sprendimui trauktis iš Europos Sąjungos ir pažadėjo, jog amerikietiškieji sąjungininkai rems Londoną einant šiuo ilgu ir duobėtu keliu. Taigi JAV nepademonstravo, jog laikysis savo, kaip sąjungininkės, įsipareigojimų NATO atžvilgiu, tačiau tapo akivaizdu, jog anglosaksai formuoja vieningą poziciją atžvilgiu kontinentinės Europos, kuri nepatenkinta Trampo iškilimu valdžion ir ketina nubausti Didžiąją Britaniją už Brexit (kad daugiau niekas iš europiečių nesugalvotų pasekti jos pavyzdžiu).

Ta situacija, kuri klostosi viduje Vakarų pasaulio, Rytų Europos šalims, pasirinkusioms JAV sateličių dalią, ir liūdna, ir dramatiška.

Palyginimui: su Lenkijos prezidentu JAV prezidentas šiek tiek pabendravo – užtikrino A. Dūdą, jog Lenkija tebelieka JAV sąjungininke. O štai Ukrainos prezidentą taip nudžiugino Trampo skambutis, jog jis net pamiršo mandagumo taisykles, nes tas skambutis jam reiškė, jog „ponas paskyrė mane mylimiausia žmona“.

„Aš – vienas iš pirmųjų pasaulio lyderių, kuriam Trampas paskambino iškart po rinkimų... Mūsų pokalbis – daug ką žadantis… Mes susitarėme, kada aš vyksiu į Vašingtoną, apie ką ir kaip kalbėsimės,” – pareiškė laime švytintis Porošenka ir pridūrė, kad jau jaučia pasitenkinimą būsimuoju susitikimu su Trampu. Ukrainiečiai į savo „garanto“ džiūgavimą atsakė anekdotu. Trampas skambina Kijevui:

–       Chelou, Petro, kaip laikaisi?

–       Donaldai, šiandien Ukrainoje šventė!

–       Na, na? Kokia?

–       Kristaus krikštynos!

–       Ou, nou, nou, tai jau per daug, tai tik inauguracija.

Bet kaip ten bebūtų, – Trampas Kijevui paskambino. O Vilniui – ne. Ir Rygai – ne. Ir Talinui nepaskambino. Liūdna? Labai! Juk tai patys ištikimiausi JAV sąjungininkai tarp NATO šalių: jie su JAV ir Afganistane, ir Irake, ir Libija bombarduoti, ir Kadafį žudyti, ir Rusiją sankcijomis klupdyti, ir atplėšti nuo tos Rusijos Gruziją, Ukrainą ir Vakarų Europą. Geriausius savo metus JAV interesams paaukojo.

O jis neskambina.

Ypač skaudu turėtų būti Lietuvos prezidentei Daliai Grybauskaitei. Kaip didvyriškai ponia Dalia atleido Trampui jo išdavystę transatlantinio solidarumo atžvilgiu ir nepuolė isterijon, kai Donaldas gyrė Putiną bei vadino NATO pasenusia organizacija, o jos narius, JAV sąjungininkus, – nesugebančiais patiems apsiginti. Ji viską pasiruošusi iškentėti, kad tik pavyktų išgelbėti „šeimą“.

O štai kiti JAV sąjungininkai prezidento rinkimų kampanijos metu nesugebėjo protauti moteriškos išminties lygyje. Matydami Trampą televizoriaus ekrane jie norėjo išsivemti, mėtė jo adresu bjauriausius žiodžius. Ne tokia Grybauskaitė. Ji, net išgirdusi Trampo abejones, ar verta Amerikai gelbėti Pabaltijo šalis rusų agresijos atveju, švelniai šypsodamasi atsakė, kad Lietuva mylės Ameriką nepaisant, kas bus jos prezidentas.

Ir po sensacingos Trampo pergalės rinkimuose ponia Dalia viena iš pirmųjų prisiekė ištikimybe naujam Baltųjų rūmų šeimininkui. „Mums JAV – visada buvo demokratijos, taikos ir laisvės vėliava. Manau, ne tik mums – visam pasauliui. Be tokios vilties pasaulis prarastų stimulą vystytis, saugumą, laisvės ir nepriklausomybės viltį, – visa tai pasauliui nešė JAV. Kaip aš pasakiau po rinkimų, mums nesvarbu, kokia bus JAV administracija, mums svarbu, kad mes pasitikime Amerika ir jos gyventojais,” – pareiškė Grybauskaitė CNN praėjusių metų lapkričio mėnesį. O ištikimas „Raudonosios Dalios“ ginklanešys, Lietuvos užsienio reikalų ministras Linas Linkevičius pakuždėjo šeimininkei, jog, kritikuodamas NATO ir tuos JAV sąjungininkus, kurie nevykdo savo įsipareigojimų, Trampas šiek tiek teisus.

Į tokį naujos administracijos palaikymą turėtų būti atsakyta maloniai. Bet Trampas Grybauskaitei nepaskambino. Ir vis dar neskambina. Galėtų paskambinti ir pasakyti, kad be reikalo „Raudonoji Dalia“ iš kailio neriasi, nes jam jos paslaugos nereikalingos. „Tu paskambink vakare su gera gera žinia, Tu paskambink vakare ir nudžiuginki mane. Tu paskambink vakare su gera gera žinia, Kad galų galų gale, tu vėl myli tik mane.”

Naujasis amerikiečių prezidentas nori kalbėti su Putinu tiesiogiai, ir jam neįdomios Lietuvos paslaugos palaikant Barako Obamos pastangas boikotuoti Europoje Rusiją ir izoliuoti Maskvos diplomatiją. Trampas ateityje nemato Europos Sąjungos, remia Brexit ir savo dangoraižyje priima Marin Le Pen. Tai matydami, europiečiai vadina Trampą viena iš grėsmių Europos Sąjungos egzistavimui – kartu su Rusija, Kinija ir islamo teroristais. Ir kylančiose šioje šeimoje peštynėse niekam nerūpi vieniša ir jau senstelėjusi moteris, svajojusi, JAV protekcijos paremta, rasti sau prieglobstį Europos komisijos pirmininko kėdėje.

Akivaizdu, kad Leningrado A. Ždanovo valstybinio universiteto ir TSKP CK Visuomeninių mokslų akademijos absolventė neblogai įvaldė politinių triukų strategiją.

Lietuvos prezidentė vis dar tikisi sutaikyti Donaldą Trampą su Europos Sąjungos lyderiais. Europos šalių vadovai turi išmokti skaityti tai, ką rašo naujasis JAV prezidentas Donaldas Trampas Twitter‘yje, ir teisingai reaguoti, pareiškė Grybauskaitė ES samito metu Maltoje. Ji pabrėžė, kad europietiški lyderiai privalo išmokti kritiškai, o ne pažodžiui vertinti Trampo pareiškimus, įsiklausyti į jo siunčiamus signalus.

„Be abejonės, tokia diplomatija – greitesnė ir autentiškesnė. Ir su tokiais iššūkiais mums teks dirbti,“ – pareiškia ponia Dalia apie Trampo manierą nesivaržant išsakyti savo nuomonę apie NATO ir Europos Sąjungą, kviesdama kolegas neskubėti svaidytis žodžiais ir neatsakyti į kritiką kritika, o įsiklausyti į Trampo žodžius ir ieškoti juose ypatingos prasmės.

Ką ir kalbėti – toks ambicingas tikslas galėjo gimti būtent Vilniaus aukštosios partinės mokyklos mokslinės sekretorės galvoje. Tačiau norint, kad šis tikslas virstų realybe, turi susibėgti mažiausiai trys sąlygos.

Pirma, naujasis JAV prezidentas turi atsisakyti sumanymo statyti sieną tarp JAV ir Meksikos, prekybinio karo su Kinija ir draudimo įvykti į šalį islamo migrantams, savo aukščiausiąjį dėmesį nukreipiant į Europą.

Antra, jis privalo pakeisti savo požiūrį į Europos Sąjungą, neremti Brexit ir nesišiaušti prieš kontinentinius euroskeptikus.

Šiandien nei viena iš šių sąlygų nėra gyvybinga. Daliai Grybauskaitei belieka tik tikėtis, kad JAV prezidentas pastebės, jog Europa turi ir Rytus, Lietuvą ir, žinoma, ją. Ir kad paskambins. Tikėti taip, kaip gali tikėti tik mylinti ir be galo atsidavusi savo Vieninteliam Moteris: „Kai aš nustosiu Trampo laukti, ateis jis, būtinai ateis...“

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 13 — id: `scraped:rubaltic_lt:3f65d7c644eabae5`

**Title:** Pabaltijui reikia suklusti: JAV prezidentas vykdo savo priešrinkiminius pažadus

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Prezidentas Trampas pradėjo vykdyti priešrinkiminius pažadus. Pasitraukimas iš Ramiojo vandenyno partnerystės, siena pasienyje su Meksika, antimigrantiški įsakai — per dvi savaites naujasis Baltųjų rūmų šeimininkas parodė, kad laikosi žodžio. Trampo ryžtingumas įrodo: kitoje Atlanto pusėje esantiems politiniams lyderiams, kurie tikėjosi demokratų pergalės, neverta laukti džiugių naujienų iš Vašingtono.

Naujai išrinkto JAV prezidento Donaldo Trampo kritikai neveltui nerimavo. Savo priešrinkiminius pažadus nekenčiamas milijardierius pradėjo vykdyti jau inauguracijos dieną. Iškart po iškilmingos ceremonijos Trampas pasirašė pirmuosius dokumentus, tarp kurių įsakas profilinėms žinyboms mažinti ekonominį apkrovimą toms kompanijoms, kurios priverstos padengti darbuotojų draudimo išlaidas pagal liūdnai išgarsėjusią reformą Obamacare, o taip pat proklamacija naujos šventės — Patriotiškumo nacionalinė diena.

Savo tiesioginiais sprendimais, kuriems nereikalingas Kongreso pritarimas, naujasis prezidentas ėmė įrodinėti amerikiečiams, kad netuščiažodžiauja, kad laikosi žodžio. Jau įrodė. Dabar prasideda tikrasis sudėtingas ir lankstus darbas — pradėti įgyvendinti iniciatyvas, kurios lauks rimto pasipriešinimo, o taip pat tas, kurias reikia „pertempti“ per parlamento palatas. Kalbėti apie Kongreso lojalumą Trampui kol kas per anksti, tačiau tas faktas, kad daugumą vietų abiejose palatose užima naujojo prezidento  bendrapartiečiai, negali nesukelti vilčių Baltųjų rūmų vadovybei.

TTP — tai preferencinė prekybos sutartis tarp 12 Azijos-Ramiojo vandenyno regiono šalių, kuri mažina tarifines kliūtis. Visa tai didina prekybinį deficitą ir mažina vietos gamybą, tačiau išlošia transnacionalinės korporacijos. Priešrinkiminės kampanijos metu JAV reindustrializaciją skelbęs Trampas aktyviai kritikavo sutartį, remdamas amerikiečių darbininkų interesus ir pareikšdamas, kad gamyklos turi sugrįžti į tėvynę. Kongresas taip ir nesuspėjo ratifikuoti TTP, ir todėl naujai išrinktam prezidentui neprireikė buvusios administracijos įsakų panaikinimo teisės.

„Valstybė be sienų — ne valstybė. Nuo šios dienos Jungtinės Amerikos Valstijos susigrąžina sienų kontrolę, susigrąžina sau savo sienas,“ — taip komentavo iniciatyvą nekenčiamas milijardierius.

Trampas pažadėjo sienos statybos darbų finansavimą „pakabinti“ ant pačių meksikiečių ir pasiryžęs to siekti. O ta siena oi netrumpa: net 3,2 tūkstančio kilometrų. Naujoji amerikiečių administracija jau pradėjo išsukinėti rankas prezidentui Enrike Penja Njeto: Baltųjų rūmų spaudos sekretorius Šon Spaiser pareiškė, kad už sieną kaimynai galės atsiskaityti 20 proc. mokesčiu Meksikos importui.

Ir visa tai — per dvi savaites. Naujai išrinktas prezidentas „smogia iš peties“, nedelsdamas savo priešrinkiminius pažadus paversdamas politiniais sprendimais. Ir jis savo daug kam netikėtas, nusišnekėjimu ir populistinėmis pagyromis  oponentų pavadintas idėjas paverčia realybe. Pasirodo, Trampas — reiškinys rimtas; kurie bijojo jo prezidentavimo, dreba neveltui.

Tarp tų šalių, kurios, stebėdamos šaunią naujo amerikiečių lyderio darbą, nepajėgia atsikratyti meilės Obamai jausmo, — ištikimiausios JAV sąjungininkės Rytų Europoje Pabaltijo šalys.

Ir nors Pabaltijo sostinės nuo Vašingtono skiria 7 tūkstančiai kilometrų, politine prasme jos daug artimesnės. Būtent Pabaltijo šalys vaidino Europos Sąjungoje JAV „Trojos arklį“, gindamos amerikiečių interesus. Būtent jų pastangas „sulaikyti Rusiją“ ir viltis stiprinti NATO pozicijas Europoje rėmė Obamos administracija. Tačiau situacija keičiasi.

Šiaurės Atlanto aljansas — pasenusi organizacija, kuri neatitinka saugumo idėjoms ir kurią būtina reformuoti, ne kartą sakė Donaldas Trampas. „Rusų grėsmė“, jo nuomone, ne daugiau kaip akių dūmimas ir ji jau išbraukta iš JAV „gynybinių prioritetų“. Nelaikykite rimtais Trampo žodžius apie NATO, naiviai ramino Pabaltijo šalis Obamos viceprezidentas Džo Baidenas praeitų metų rugpjūčio mėnesį. Bet, pasirodė, naujasis Baltųjų rūmų šeimininkas visai nejuokavo.

Didesnė dalis karinės technikos ir kontingento, kurių permetimas į Rytų Europos ir Pabaltijo šalis prasidėjo sausio pradžioje, bus sugrąžinta į savo bazes po manevrų, įsitikinęs JAV Tarptautinių santykių tarybos narys Arijel Koen. „Manevrai užsibaigs, planai bus įgyvendinti, ir tada beveik visi tankai su kareiviais sugrįš į tas bazes, iš kurių buvo pasiųsti,“ — mano politologas.

Šiandien Maskva ir Vašingtonas planuoja pradėti spręsti tas problemas, kuriose galima aptikti bendrus pagrindus, sakė Konuej.

Tokiu būdu, sparčiai ir be prievartos, strategijos Pabaltijo vadovybių, viską dariusių siekiant įtikti prezidento Obamos administracijai, byra lyg kortų namelis.

Jų elgesys užsienio politikoje, be abejonės, bus koreguojamas: politikai ir persiaus, ir persirengs, ir pasistengs kuo rimčiau atsikratyti vakarykščių avantiūrų purvo — laiko tėkmė privers. Tačiau ir diplomatinis svoris šalių, nesugebančių pozityviai paveikti situaciją, kris iki minimumo.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 14 — id: `scraped:rubaltic_lt:b1bc258a5d8041f1`

**Title:** Vakarų analitikai Pabaltijį vertina kaip išlaikytinį

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Naujausieji vakarietiški tyrimai įrodo, jog egzistuoja fundamentali Pabaltijo ekonomikų priklausomybė nuo Europos Sąjungos dotacijų. Lietuva, Latvija ir Estija įstojo į ES išlaikytinių teisėmis ir gyvuoja joje dėka turtingų šalių donorų malonės. Tačiau po „breksito“ ir kontinentinėje Europoje nusimatančių naujųjų dešiniųjų pergalių užsibaigs pabaltijiečių parazitavimas „senųjų europiečių“ sąskaita.

Stambiausias prancūzų laikraštis Le Figaro po to, kai visą Europą sukrėtė referendumas dėl Didžiosios Britanijos išstojimo iš Europos Sąjungos, pravedė savąjį tyrimą apie tai, kas ką ES maitina ir kokiais kiekiais. Tyrimo metodas buvo gana paprastas: kiek pinigų ES šalys narės perveda Briuseliui mokesčių pavidalu ir kiek pinigų jos gauna dotacijų forma.

Tyrimų rezultatai nebuvo netikėti.

Dešimt šalių donorių, atiduodančių ES biudžetui daugiau, nei gauna, yra šios (įnašų mažėjimo tvarka): Vokietija, Prancūzija, Didžioji Britanija, Nyderlandai, Italija, Švedija, Belgija, Austrija, Danija, Suomija. Besąlygiškai šioje eilėje pirmauja pagrindinis europietiškos integracijos „lokomotyvas“ — Vokietija: kasmet Berlynas į ES biudžetą įneša beveik 26 milijardus eurų, o eurofondų gauna 10 milijardų. T.y. FVR atiduoda Briuseliui 15,5 milijardo eurų daugiau, negu pasiima.

Antroje donorų sąraše yra Prancūzija: Paryžius kasmet perveda į ES 7,7 milijardo eurų daugiau, negu pasiima. Trečioje vietoje dar neseniai buvo Londonas, pervesdavęs Briuseliui 5,5 milijardo eurų daugiau, negu pasiimdavo. Po „breksito“ trečioje vietoje atsidurs Nyderlandai: Olandija, kuri pagal plotą 1,5 karto mažesnė už Latviją su Lietuva, „Vieningos Europos“ projektui atiduoda 11,3 milijardo eurų — 5 milijardas daugiau, negu pasiima.

Nors, gali būti, ir neatsidurs: pavasarį Nyderlanduose įvyksiančiuose parlamento rinkimuose gali laimėti ir vienos partijos vyriausybę suformuoti Gerto Vilderso Laisvės partija, žadanti olandams šalies išstojimą iš ES. Ir Paryžius gali iškristi iš Rytų Europos rėmėjų sąrašo, jeigu prezidento rinkimus pavasarį laimės Marin Le Pen, kurios šalininkai nenori matyti Prancūzijos Europos Sąjungoje. Didžioji Britanija iš Europos Sąjungos jau traukiasi...

Absoliuti eurofondų gavimo europietiška lyderė — Lenkija. Varšuva Europos Sąjungoje pelnytai išsikovojo teisę vadintis šalimi, geriausiai sugebančia išpešti iš Briuselio pinigų ir juos įsisavinti. 2014 metais lenkai gavo iš ES biudžeto 17,2 milijardo eurų — beveik du kartus daugiau, nei Vokietija, kuri pagal gyventojų skaičių Lenkiją viršija du kartus. Ir tuo metu Varšuva pervedė į ES biudžetą 3,5 milijardo eurų — penkis kartus mažiau, nei Berlynas. Tokiu būdu lenkai gavo iš Briuselio 13,7 milijardo eurų daugiau, negu įnešė mokesčių.

Vilniui, Rygai ir Talinui, žinoma, dar nepavyko pasiekto lenkiško apsukrumo lygio, įsisavinant eurofondus. Bet ir tos iš ES biudžeto gaunamos dotacijos, kurias gauna Pabaltijo respublikos, atlieka ypatingą vaidmenį. Estija perveda į ES biudžetą 178 mln. eurų, o pasiima 652 milijonus. Tris kartus daugiau! Latvija atiduoda 320 mln. eurų, o gauna 1,1 milijardo. Beveik keturis kartus daugiau! Na, o rekordus tarp Pabaltijo šalių muša Lietuva: atiduodama 244 mln., ji pasiima net 1,8 milijardo. Skirtumas — daugiau kaip septyni kartai!

Dar ryškiau Pabaltijo ekonomikų priklausomybė nuo materialinės Europos Sąjungos pagalbos matosi į Lietuvos, Latvijos ir Estijos ekonomiką pažvelgus per procentinio santykio prizmę. Tokie tyrimai taip pat atliekami.

Pastovų ES fondų eikvojimo Centrinėje ir Rytų Europoje monitoringą atlieka tarptautinė kompanija KPMG — viena iš keturių stambiausių pasaulio auditorių agentūrų. Paskutinis KPMG analitinis pranešimas serijos „ES fondai Centrinėje ir Rytų Europoje“ rėmuose buvo išleistas praeitais metais.

KPMG audito duomenimis, eurofondai sudaro 15 proc. „Naujosios Europos“ šalių BVP. Europietiškų dotacijų „suvalgymo“ rekordininkė — Vengrija: Briuselio lėšos formuoja beveik 23 proc. vengrų BVP. Po Budapešto pagrindinių išlaikytinių sąraše aptiksime Pabaltijo šalis.

Įdomu tai, jog eurofondų dalis Lenkijos ekonomikoje procentine išraiška mažiau įspūdinga, negu Briuselio piniginės injekcijos į lenkų ekonomiką absoliučiais skaičiais. ES struktūrinių fondų dotacijos sudaro 15,7 proc. lenkų BVP. Pagal šį rodiklį Lenkiją tarp 11 Centrinės ir Rytų Europos šalių matome šeštoje vietoje. Lenkija — didelė ir erdvi rinka, pajėgi išsilaikyti sisteminės krizės metu ir adaptuotis praradus ateityje Briuselio finansinę paramą.

Lietuva, Latvija, Estija — Europos Sąjungos šalys išlaikytinės. Potarybiniu laikotarpiu šių šalių lyderiai sugriovė savąsias ekonomikas, nuskurdino savuosius gyventojus; to išdavoje jos tapo išlaikytinėmis Vakarų Europos, kuri šelpia šias šalis savo įnašais į europietišką biudžetą ir priima iš jų bėgančius bedarbius.

Pabaltijo elitas net ta jam dykai atitekusia europietiška pagalba nesugebėjo pasinaudoti taip, kaip lenkai. Lenkija, pasinaudojusi eurofondais, per dešimt metų dukart prailgino savo automagistrales, kuriomis dabar vykdomas autotranzitas iš Vokietijos. O pats stambiausias Pabaltijo infrastruktūros projektas, kurį numatoma įgyvendinti europietiško sofinansavimo pagalba, — geležinkelis Rail Baltica, „kelias į niekur“, kuriame niekada nebus tiek krovinių ir keleivių, kad jis visiškai apsipirktų.

Kokioms reikmėms Lietuva paskutinį kartą paprašė europietiško finansavimo? Tvoros nuo „rusų grėsmės“ prie sienos su Kaliningrado sritimi statybai? Deja, deja — Briuselis parodė „špygą“. Ech, kokį pelną būtų gavusi, taukuose pasivartaliojusi, šių pinigų sulaukusi Lietuva! Kas yra tvora? Tai labai naudingas verslo infrastruktūrinis projektas: pasakiškai pelningas, greit atsiperkantis, su perspektyva plėstis ir eksportuoti produkciją. Tai ne kažkokios ten jūsų atominės elektrinės.

Todėl Didžioji Britanija palieka Europos Sąjungą, tuo pačiu keliu jau pavasarį gali pasukti Prancūzija ir Olandija. O jei nepasuks, vis tiek bus priverstos gelbėti europietišką integraciją, įsiklausydamos į visuomenės nuomonę, kuri vienareikšmė: pakaks kišti Briuseliui milijardus eurų, atgal sulaukiant daug kartų mažiau. Kodėl kažkokia ten Lituanie turi siurbti prancūzų mokesčio mokėtojo lėšas? Ir ar tie mokėtojai žino, kas tai yra Lituanie, kur ji tupi ir kuo skiriasi nuo Lettonie? Lituanie ir Lettonie — tai dvi skirtingos šalys ar viena, kurios pavadinimas skirtingai tariamas? Ir, svarbiausia, kodėl ta Lettonie/Lituanie įsisiurbė į mūsų kūną kaip erkė? Lai ji savu maistu minta.

Ir dar bus mažinama, nes visuomenės nuomonės nepaisymas yra ES subyrėjimo rizika, o po subyrėjimo visos kalbos apie paramą Pabaltijui prarastų prasmę. Todėl Lietuvai, Latvijai ir Estijai palaipsniui bus mažinama europietiška ekonominio invalidumo pašalpa.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 15 — id: `scraped:rubaltic_lt:e252165e996d5558`

**Title:** „Rusų grėsmei“ Lietuvos valdžia smogs tvora

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos valdžia pasienyje su Rusija ketina pastatyti tvorą, kuri turės apsaugoti Lietuvą nuo „agresyvaus kaimyno“. Kaliningrado vadovybė pasiūlė lietuviams pirkti statyboms vietinių plytų. Tokios statybos kaimynų sąskaita Rusijai naudingos, nes jos garantuos, jog ateityje į Kaliningradą nepateks pabėgėliai, kuriuos Vilniui pirš Eurokomisija; Lietuvai tokios tvoros nuo Rusijos statybos — eilinis eurofondų ir savojo biudžeto iššvaistymas, kuriuo užsiims politikai prisidengdami „rusų grėsme“.

Lietuva ne pirmoji su Rusija besiribuojanti šalis, nutarusi tvora gelbėtis nuo „agresyvaus rytų kaimyno“. Stebina, jog oficialus Vilnius su šia idėja kažkaip keistai suvėlavo. Antirusiška Lietuvos valdžios retorika Pabaltijyje brandžiausia, rusofobija (pagal vietos terminologiją — kremliafobija) tapo oficialiąja ideologija ir užsienio politikos pagrindu, o štai statyti tvorą buvo sumanyta jau po Latvijos ir Estijos.

Estijos valdžia dar užpraeitų metų rugpjūtį nutarė atsiriboti nuo Rusijos spygliuotos vielos tvora, kurios ilgis 108 kilometrai, aukštis — 2,5 metro. Užbaigti statybas planuojama iki Estijos Respublikos šimtmečio 2018 metais — tokią „dovaną“ mylimoji vyriausybė įteiks estams jubiliejaus proga. Tvora (ją estų valdžia pakiliai vadina „aukštos technologijos siena“) iš valstybės biudžeto išsunks 70 milijonų eurų.

Praėjus dviem mėnesiams, estų pavyzdžiu pasekė latviai. 2015 metų spalio mėnesį Latvijos vidaus reikalų ministras Richardas Kozlovskis paviešino vyriausybės planus atsiriboti nuo Rusijos siena, kurios ilgis — 90 kilometrų, aukštis — 2,7 metro be virš sienos spygliuotų vielų eilių. Statybos turėtų paimti iš biudžeto 17 milijonų eurų.

Ukrainos premjeras Arsenijus Jaceniukas 2014 metais anonsavo projektą „Siena“ — „Europietiško pylimo“ statybos visos sienos su Rusija perimetru. Tas „pylimas“ esą turės apginti ne tik Ukrainą, bet ir visą „civilizuotą pasaulį“ nuo naujojo laukinio knibždyno. Aukščiausioji Rada šio projekto įgyvendinimui išskyrė 600 milijonų grivnų (15,6 mln. dolerių), o bendroji projekto vertė — 4 milijardai grivnų.

Už išskirtus pinigus Jaceniukas išrausė pasienyje griovius ir 72 kilometrų ruože įrengė žemus, žmogaus ūgio lygio metalinius grotus. Dabar šis „Europietiškas pylimas“ primena retą stačiatvorę, kokią galima pamatyti ukrainiečių kaimuose — su ant kuolų užmautomis molinėmis puodynėmis, avinų galvomis ir džiovinamais baltiniais.

Na, o už tuos perimetru išrikiuotus pasienio stulpus Jaceniuko vyriausybė sumokėjo (už kiekvieną) po 10 tūkstančių grivnų, kai didžiausia kiekvieno kaina — 800 grivnų. Ir todėl šiuo metu „Sienos“ projektą tiria Ukrainos antikorupcinis biuras. O Lietuvos politikai, pastoviai klykdami apie „rusų grėsmę“, „agresyvų kaimyną“ ir „žaliuosius žmogeliukus“, ilgai kraipė ūsą link ukrainiečių ir Pabaltijo kaimynų ir tik dabar susiprotėjo užsiimti „strateginėmis“ statybomis.

Kovos su „imperine agresija“ ideologija Lietuvoje pajėgi pateisinti bet kurią biudžetinę paraišką, todėl tvoros statybų iniciatoriai (ir būsimieji pasipelnytojai) lenktyniauja gražbyliaudami. „Tvora — signalas, kad kaimyninę valstybę vertiname kaip agresorių,“ — pareiškė Lietuvos vidaus reikalų ministras Eimutis Misiūnas.išgirdęs tokią skambiai paviešintą magišką formulę bet koks Lietuvos Seime įsikūręs atskalūnas, atsisakęs aukoti „šventam reikalui“ ir dosniai finansuoti kovą su „agresyviu kaimynu“, bus apšauktas penktąja kolona ir „Maskvos ranka“ bei įvardintas Putino agentu.

O statybos prie sienos su Rusija bus pradėtos jau šį pavasarį ir užbaigtos metų pabaigoje. Tvora iškils nuo Vištyčio iki Nemuno — tai 135 kilometrai. Pirmąjam statybų etapui išskirta 3,6 milijono eurų, ir tai ne tik iš lietuviškojo, bet ir iš Briuselio biudžeto — iš ES viešojo saugumo fondo.

Pasak Lietuvos valdžios atstovų, tvora pasienyje pirmiausia apgins lietuvius nuo nelegalių migrantų ir kontrabandininkų, bet ir rusų tankus Vilnius neužmiršta. „Tokia tvora nesulaikys tankų ir kitos karinės technikos, bet ji parodys, kad mes, tikėdamiesi geresnių santykių su Rusija, situaciją vertiname realiai. Mes darome viską, siekdami sumažinti rusų grėsmes,“ — pareiškė Lietuvos Seimo Nacionalinio saugumo ir gynybos komiteto atstovė Rasa Juknevičienė, pabrėždama, kad tvora turi simbolinę reikšmę ir turi padėti Lietuvai tęsti nesibaigiančią kovą su „rusų grėsme“.

„Vėliavą jiems į rankas, — pareiškė Alichanovas. — […] Prie pat sienos su Lietuva veikia puiki mūsų plytinė. Jei kolegos norės, mes galime jiems tiekti plytas tos sienos statybai“.

Išties, negi Rusija protestuos prieš tokios tvoros statybas? Jeigu lietuviškieji kolegos nori savo lėšomis įtvirtinti valstybinę sieną su Rusija, — vėliavą jiems į rankas. Ateityje ši tvora labai bus reikalinga Kaliningrado sričiai. Atsiras garantija, kad į Kaliningradą iš Lietuvos neprasibraus pabėgėliai, kuriuos, aštrėjant krizei Šiaurės Afrikoje ir Artimuosiuose Rytuose, vis didėjančiais kiekiais pirš Vilniui Europos komisija.

Taip kad lai stato. Rusijai ta tvora naudinga. Jeigu Lietuvos valdžios atstovai nori realizuoti Rusijai naudingą projektą ir tuo pačiu nugvelbti nors dar šiek tiek biudžetinių pinigų, tai jau Lietuvos, o ne Kaliningrado ir ne Maskvos, mokesčių mokėtojų problemos.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 16 — id: `scraped:rubaltic_lt:9cfc47597bf18abe`

**Title:** Pabaltijis pripažino ypatingą amerikiečių kariškių statusą savo teritorijoje

**Source:** rubaltic_lt (propaganda)

**Text:**

```
JAV kareiviams bus užtikrintos ypatingos Lietuvoje, Latvijoje ir Estijoje buvimo sąlygos. Tos naujovės — mokesčių lengvatos, žemos kainos, baudžiamojo persekiojimo imunitetas ir potencialūs konfliktai su vietos gyventojais.

Pabaltijo šalys sutarė su JAV dėl amerikiečių kariuomenės buvimo savo teritorijoje sąlygų. Atitinkamus susitarimus pasirašė Lietuva ir Estija. Taline parašus po dokumentais suraitė gynybos ministras Margus Cachkna ir JAV ambasadorius Džeims Melvil, o Vilniuje — Raimundas Karoblis ir ambasadorius En Chol. Anksčiau, sausio 12 dieną, tokį susitarimą pasirašė Latvijos gynybos ministras Raimond Bergmanis ir amerikiečių ambasadorius Nensi Petit.

Vietos žiniasklaida yra tos nuomonės, kad derybos su amerikiečiais vyko skubotai, nes tai padaryti reikėjo iki Donaldo Trampo inauguracijos sausio 20 d. Iki šiol amerikiečių kariškių kuopos lankė Lietuvą, Latviją ir Estiją tikslu dalyvauti mokymuose ir trumpalaikiuose manevruose. Pasirašyti susitarimai faktiškai suteikia kariškiams galimybę būti trijose respublikose pastoviai. O to ir siekė vietos valdžios. „Esu įsitikinęs, kad JAV pajėgų buvimas yra vienas iš svarbiausių veiksnių, leidžiančių Lietuvos gyventojams jaustis šiandieninėje situacijoje saugiai, — pasakė krašto apsaugos ministras Karoblis, — ir aš tikiuosi, kad pastovus buvimas išliks“. Amerikiečių sutikimui ruošiamasi pilnu tempu.

Ypatingas režimas

Tipiniai susitarimai dėl paj4g7 statuso (Status of Forces Agreements, SOFA) ir jų papildymai — neatskiriama stabilaus amerikiečių kariuomenės bazavimosi užsienyje dalis. Pentagonas sudarė virš 100 sutarčių, kurios reguliuoja jų kariškių santykius su tomis šalimis, kuriose jie bazuojasi. Iš esmės šalys sąjungininkės laiko SOFA prestižiniu įvykiu. Tai reiškia, kad Baltieji rūmai rimtai užsiėmė jų gynyba. Ir todėl, jei susitarimams bus įžiebta žalia šviesa, jie gali artimiausiu metu priartinti Lietuvą, Latviją ir Estiją prie artimiausių amerikiečių sąjungininkių — Japonijos, Pietų Korėjos ir Vokietijos.

Pabaltijo šalys įsipareigojasudaryti kariškiams pasakiškas sąlygas su daugybe lengvatų. Tarp jų — lengvatinis mokesčių režimas be PVM ir pardavimo be akcizų mokesčių, jų paslaugoms bus specialios parduotuvės su prekėmis palankiomis kainomis. Atskirai nurodoma, kad priimanti šalis nesiekia „papildomo pelno“ užsienietiško kontingento sąskaita. Amerikiečių atsakas į dosnų priėmimą — kariškiai įsipareigoja prisilaikyti Pabaltijo šalių įstatymų ir nekelti riaušių.

Svečių elgesys dažnai susilaukia nemalonių atsiliepimų. Netapo išimtimi ir praeiti metai: amerikiečiai Druskininkuose niokojo akvaparką, Kaune nuo prokuratūros pastato nuplėšė valstybinę vėliavą ir išniekino ją; Vokietijos tarnautojai Ruklos bazėje sumušė kolegą lietuvį; britai Rygos „Makdonaldse“ užpuolė latvį ir sulaužė jam nosį; japonų jūreiviai siautėjo Klaipėdoje ir kabinėjosi prie gyventojų. Kaip taisyklė, tokį elgesį demonstravo girti svečiai. Iššaukiantį kariškių elgesį ir chuliganiškumą Ventspilio meras Aivars Lembergs 2014 metais pavadino okupantų elgesiu. Su panašiais įvykiais pastoviai susiduria ir kitos šalys — pavyzdžiui, 2016 metų gegužės mėnesį italų Vičencėje dėl masiškų muštynių naktiniame klube buvo sulaikyta 13 elitinės 173-iosios JAV desantininkų brigados kariškių.

Imuniteto rizikos

Todėl aktualus tampa klausimas dėl baudžiamosios ir drausminės užsieniečių atsakomybės. Jei amerikiečių kareivis svetur prišiukšlino, kas turi tvarka užsiimti? Ir čia susiduriama su griežta Valstybės departamento pozicija: atsakomybė JAV piliečiams gali būti taikytina tik pagal jų jurisdikciją. „Dvigubos jurisdikcijos“ atveju amerikiečiai reikalauja, kad priimanti šalis perleistų jiems savo teisė bausti už prasižengimus ir nusikaltimus.

Tokie mechanizmai seniai veikia šalyse, kuriose dislokuotos amerikiečių bazės. Panašų požiūrį JAV taiko Pabaltijo šalims. Kaip buvo tikėtasi, amerikiečių kariškiams bus suteiktas dalinis imunitetas nuo persekiojimo. Dalinis todėl, jos Pabaltijo respublikos pasilieka sau teisę „perimti“ jurisdikciją pagal Generalinės prokuratūros užklausimą. Tik ne visos susitarimų detalės gali būti paviešintos. Antai Latvija susitarimo tekstą užslaptino iki patvirtinimo Seime. Tik bendrais bruožais žinoma, kad Ryga gali pareikalauti teisės savarankiškai bausti amerikiečius už sunkius ir labai sunkius nusikaltimus arba incidentus su aukomis.

Būtent amerikiečių kariškių imunitetas pastoviai iššaukia trintį tarp kariškių, vietinės valdžios ir gyventojų. Kategoriškas Irako vyriausybės atsisakymas suteikti amerikiečiams imunitetą neleido sudaryti sutartį dėl kariuomenės statuso, o tai paskatino Baraką Obamą 2011 metais pradėti kariuomenės išvedimą iš šalies. Su rimtomis problemomis susiduria amerikiečiai japonų saloje Okinava, kurioje dislokuoti keli kariniai objektai. Japonų spaudos duomenimis, 1972-2014 metais amerikiečių kariškiai ir civilinis bazių personalas įvykdė 5862 nusikaltimus, tame tarpe 737 sunkius: nužudymai, prievartavimai, apiplėšimai, padegimai. Praeitą pavasarį JAV jūrų pėstininkas buvo pripažintas kaltu išprievartavęs viešbutyje vietinę moterį. JAV tribunolas nuteisė jį 2,5 metų pataisų darbų ir įpareigojo sumokėti aukai 21,7 tūkstančio dolerių; dar 2,8 tūkstančio dolerių kompensaciją sumokėjo Pentagonas.

Vasarą kitas bazės tarnautojas buvo sulaikytas dėl dvidešimtmetės merginos išprievartavimo ir nužudymo, o girta kariškė išprovokavo kelių įvykį, dėl kurio nukentėjo du vietiniai gyventojai. Dėl šių įvykių prie amerikiečių bazės protestavo 60 tūkstančių žmonių. Kalbėdamas mitinge Okinavos gubernatorius Takesi Onaga paprašė vyriausybės iškelti už salos ribų amerikiečių bazę. Jis griežtai pasisakė prieš naujų amerikiečių karinių objektų statybą, todėl japonų vyriausybei teko paduoti gubernatorių į teismą.

Kokį svetingumą nerodytų užsienio kariškiams Pabaltijo šalių valdžios, ilgalaikis svetimų karinių kontingentų, nors ir sąjunginių, dislokavimas yra dalykas rizikingas, galimai sukeliantis kriminogenines situacijas. Jeigu jau eilinius mokymus lydėjo nepageidautini incidentai, tai ir aukštesnio statuso dalinių konfliktai su vietiniais gyventojais bus neišvengiami. Taigi užsikrovusioms ant savo pečių „Rusijos sulaikymo“ misiją Pabaltijo šalių valdžioms teks skaitytis ir su šia rizika.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 17 — id: `scraped:rubaltic_lt:899eb534f91225d8`

**Title:** Naujametinės pagirios baigėsi Lietuvoje paranojos paaštrėjimu

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Praėjusius metus Lietuva užbaigė kovodama su oženų kranu, o naujuosius pradeda kova prieš stambiausio šalyje duomenų centro statybą, įtardama, kas jis gali turėti ryšių su Rusijos šnipinėjimo centru. Tuo tarpu lietuviškieji konservatoriai tikina, kad Kremliaus pastangomis 2019 metais Lietuvos prezidentu taps prorusiškas žmogus. Taigi šnipinėjimo baubas ir paranojos liga Lietuvos politikus tebepersekioja — šiais metais šių pacientų būklė dar labiau kelia nerimą.

Šnipinėjimo baimė, akcentuojant kibersaugumą, tapo savotiška vakarietiška 2016–2017 metų sezono mada. Šią madą sukūrė JAV Demokratų partija, paskutines dienas Baltuosiuose rūmuose praleidžiantis Barakas Obama ir specialiosios amerikiečių tarnybos.

Šios tarnybos pagaliau paskelbė ilgai lauktą pranešimą apie rusų hakerius, kuriame pateikė „nepaneigiamus“ Rusijos įsikišimo į amerikiečių rinkimus įrodymus. Svarbiausi „įrodymai“ — televizijos kanalo Russia Today žinios ir penkerių metų senumo įrašai šios telekompanijos direktoriaus tinklalapyje.

Nenuostabu, kad tokiais įrodymais paremtas pranešimas iššaukė juoko bangą ne tik pačioje Amerikoje, bet ir už jos ribų. Tačiau tas juokas netrukdo išeinančiai amerikiečių valdžiai ryžtingai kartoti apie rusų hakerių įsikišimą į prezidento rinkimus, įvedinėti prieš Rusiją naujas sankcijas, išvaryti prieš Naujuosius metus rusų diplomatus ir abejoti, ar teisėtai prezidentu išrinktas Donaldas Trampas.

Amerika — įstatymdavė visam transatlantiniam pasauliui; nenuostabu, jog kibersaugumo isterija kaipmat pasiekė Senąjį pasaulį. Prancūzijos valdžia jau pareiškė, kad rusų hakeriai gali įsikišti į pavasarį vyksiančius jų prezidento rinkimus ir pasodinti į Prancūzijos vadovo kėdę Kremliaus žmogų. Bet ar gali antirusiškoje isterijoje nedalyvauti Lietuva? Lietuvos valdantiesiems šnipinėjimo baubas, paranoja ir „Maskvos rankos“ paieškos — normali būklė, o jei dabar tai tampa iš Vašingtono sklindančia mada, brautis į garsiausiai klykiančių gretas — garbės reikalas.

Lietuvos saugumo departamentas įspėjo šalies valdžią, kad tuo atveju, jei šis duomenų perdavimo centras bus sujungtas optoplaušais su Kaliningrado sritimi, jis gali būti pajungtas ir prie Rusijos FST radijo elektroninės žvalgybos. „VSD manymu, Arcus Novus duomenų centro vystomas projektas AmberCore dėl ryšių su Rusijos Federaline Saugumo Tarnyba (FST) kelia grėsmę Lietuvos nacionaliniam saugumui,“ — teigia Valstybės saugumo departamento direktorius Darius Jauniškis.

Arcus Novus ir jos „dukrelės“, kompanijos AmberCore DC, ryšių su rusų žvalgyba egzistavimą Lietuvos spectarnybos ne įtaria, o pateikia kaip įrodytą faktą. Įrodymai — CŽV pranešimo lygyje apie „rusų hakerių įsikišimą į JAV prezidento rinkimus“. 51 proc. akcijų Arcus Novus, ketinusios netoli Vilniaus statyti stambiausią Lietuvoje duomenų centrą, priklauso Danijoje registruotai kompanijai Satgate Holding, o 49 proc. — Kaliningrado srityje registruotam Valerijui Avetisjancui. Tinklalapio Linkedin duomenimis, Avetisjancas yra ir vienas iš Satgate Holding partnerių ir steigėjų, steigėjas ir direktoriaus pavaduotojas Kaliningrado srityje įregistruotos kompanijos STG, anksčiau jis dirbo kompanijose „Gazinvest grup“ ir „Gazprom komplektacija“.

Pagal VSD logiką, jei žmogus yra Rusijos pilietis (ypač, jei jis gyvena Kaliningrado srityje), jokių papildomų įrodymų dėl jo ryšių su FST ir nereikia. Jei lenda į Lietuvą su dvigalvio erelio pasu, vadinasi, jis FST agentas. Ir jokių kalbų! Kas dar iš Rusijos sugalvos brautis į Lietuvą? Ir išvis jie ten visi agentai!

Lietuvos vyriausybę tenkina tokie argumentai — statybos stambiausio šalyje duomenų centro netoli Vilniaus buvo sustabdytos. Taip Lietuva pradėjo 2017-uosius. Pradėjo taip, kaip užbaigė 2016-uosius.

Praeitų metų pabaigoje Lietuvoje siaučiančios šnipinėjimo baimės ir paranojos auka tapo „Lietuvos geležinkeliai“, kurie nepademonstravo reikiamo budrumo, dėl ko smūgį patyrė Lietuvos Respublikos nacionalinis saugumas: iš Rusijos gamintojų nupirko lokomotyvus ir (dėmesio!) oženų kraną. Šis kranas buvo sumontuotas Lazdijų rajone Šeštokų geležinkelio stotyje, o visi darbai, jį montuojant, pagal „Lietuvos geležinkelių“ ir Kaliningrado firmos „Baltkran“ kontraktą, buvo vykdomi karinės technikos ir amunicijos, ruošiantis NATO mokymams, pakrovimo-iškrovimo metu.

Iš to fakto, kad oženų krane buvo įrengtos vaizdo kameros ir kompiuteriai, o dar kad AB „Baltkran“ bazuojasi Kaliningrado srityje, o jos prezidentas — Draugystės ordinu apdovanotas Kaliningrado garbės pilietis, lietuviškieji kovotojai prieš „Maskvos ranką“ padarė „neginčitiną“ išvadą: oženų kraną į Lietuvą atsiuntė rusų specialiosios tarnybos su atsakinga užduotimi — stebėti Lietuvos kariškius.

Taigi dėlionė susideda. „Lietuvos geležinkeliai“ perka iš Rusijos lokomotyvus, oženų kranas filmuoja NATO karinės technikos pakrovimo-iškrovimo darbus, rusų verslininkas ketina statyti netoli Vilniaus stambiausią Lietuvoje duomenų centrą, iš kurio optoplaušo kabeliu galima pasiekti Kaliningrado sritį...

Konservatorių partijos atstovė Seime Rasa Juknevičienė įsitikinusi: 2019 metais rusai pasodins į Lietuvos prezidento kėdę savą statytinį! Tuo statytiniu, Juknevičienės manymu, taps 2016 metais parlamento rinkimus laimėjusios Lietuvos valstiečių ir „žaliųjų“ sąjungos lyderis Ramūnas Karbauskis.

Atkakli „landsbergininkė“ prisimena 2012 metų referendumą Visagimo AE klausimu, kurį, pasirodo, „laimėjo Putino žmonės“, o taip pat tie visur besisukinėjantieji rusų hakeriai, padarę Donaldą Trampą JAV prezidentu. Vargšė mažytė Lietuvėlė liūdi: Amerikai savą prezidentą Putinas jau pametėjo, pavasarį pasitreniruos Prancūzijoje, o paskui ir Lietuvai eilė ateis.

Tokios „juknevičienės“ ir iki jų lygio degradavę „klintonai“ ir „obamos“ patys nesupranta, jog savo elgesiu giria ir pila vandenį ant rusų pasipūtimo malūno. Idėjinis Juknevičienės vadas Dėdulė Landsbergis dar praeitą rudenį visus įtikinėjo, kad Rusija dabar „visa š...de“, iš kurio nepajėgia išsikabaruoti, nes rusams daugiau nieko nebelieka, kaip ten tupėti ir džiaugtis, kad Krymas — mūsų.

O dar Rusija turi oženų kranus su superšiuolaikiškais kompiuteriais ir vaizdo kameromis. O dar rusų rankose geriausi pasaulyje duomenų perdavimo centrai, kurių pagalba galima organizuoti kiberkarus ir į bet kurios pasaulio šalies prezidento kėdę pasodinti savą žmogų. Ir stato Rusija netoli Vilniaus stambiausią Lietuvoje duomenų centrą. Ir nori iš jo į Kaliningrado sritį nutiesti optopluoštų kabelį, kad ten esantis rusų šnipinėjimo centras pasodintų 2019 metais Vilniuje į prezidento kėdę savą žmogų.

Ir tai tvirtina ne kažkokios ten Russia Today, RuBaltic.Ru ir visa kita „rusų propaganda“. Tvirtina Barakas Obama, Hilari Klinton, CŽV, VSD, senatorius Makeinas ir, žinoma, Rasa Juknevičienė bei kiti patentuoti rusofobai, kuriems Rusiją — „pasiutusi benzino kolonėlė“, kuri „visa š...de“ ir kurios adresu jie nė karto gyvenime nieko gero nepasakė.

Argi galima jais netikėti?

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 18 — id: `scraped:rubaltic_lt:3f7b0e375207994c`

**Title:** Nepaisant draudimų, rusiškas televizorius užkariauja Pabaltijį

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Pabaltijo šalyse tęsiasi rusų žiniasklaidos diskriminavimas. Kanalam apribojamas transliavimas, jie kaltinami „Kremliaus propaganda“. Toliau — daugiau: ši kova jau persimeta į Europos parlamentą. Briuselis priima įmantraus pavadinimo rezoliuciją „Strateginės ES komunikacijos kaip atkirtis trečiųjų dalyvių propagandai“, kuri priešpastatoma Kremliaus informacinei politikai. Viso to nepaisant, Pabaltijyje auga Rusijos požiūrio poreikis, auga ir jos televizijos kanalų reitingai. Skirtingai nei politikai, eiliniai gyventojai suinteresuoti, kad būtų išsaugota žodžio laisvė.

Pabaltijo „kontrpropaganda“ rimtai buksuoja. Latviška auditorija vis dažniau žiūri rusiškus televizijos kanalus — dar birželio mėnesį skundėsi MTG TV Latvija mediakompanijos vadovė Baiba Zuzena. Rusakalbių auditorijoje kita tendencija: rusai visada mažai žiūrėjo latviškus kanalus, o kuo toliau, tuo dar mažiau juos žiūri, — pranešė Zuzena.

Latvijos gyventojai ėmė aktyviai žiūrėti rusų televiziją prasidėjus 2008 metų ekonominei krizei, ir tai ryšium su tuo, jog vietiniai kanalai prarado reklaminę rinką. „Iki krizės rusiška televizija Latvijoje užėmė apie 24 proc. laiko, o 2015 metais — jau apie 50 proc.“, — tokią statistiką pateikė Latvijos televizijos valdybos pirmininkas Ivars Belte. „Rusiškus kanalus žiūri trečdalis Latvijos gyventojų ir tik 40 proc. jų — rusakalbiai, visi kiti — etniniai latviai,“ — pasakojo Belte. Tendencija nesikeičia.

„Visa tai tęsėsi rugpjūčio ir rugsėjo mėnesiais. Mes privalome imtis priemonių. LTV1 (visuomeninis televizijos kanalas — RuBaltic.Ru pastaba) ir TV3 (vienas iš populiariausių Latvijos komercinių televizijos kanalų — RuBaltic.Ru pastaba) bando keisti situaciją, tačiau rusiškų kanalų reitingai tebeauga,“ — pranešė Lidaka.

2014 metų pabaigoje „Putino televizoriaus“ auditorija buvo ištirta Lietuvoje. Pasak kompanijos Vilmorus, rusiškus televizijos kanalus bent kartą per dieną žiūri 13 proc. lietuvių ir 61 proc. kitų tautybių piliečių. Rusijos „propaganda“ neigiamai įtakoja respublikos lenkų jaunimą, nerimauja Vilniuje. Socialinės apklausos parodė, kad etninių lenkų jaunimas su savo pagyvenusiais tėvais pastoviai žiūri rusiškus TV ir skaito rusų spaudą.

Pabaltijietiškos demokratijos bandė demokratiškiausiai kovoti su „priešų televizoriumi“ — draudimo būdu. Apribojo „RTR Planetos“ ir „NTV Mir“ kanalų transliavimo laiką. Pirmasis Baltijos kanalas ne kartą sulaukė baudų už nepageidaujamų rusiškų laidų retransliavimą. Talkinant lenkų draugams, pabaltijiečių kova su rusiškais kanalais pasiekė europietišką lygį. Lapkričio 23 d. Europos parlamentas priima rezoliuciją, kurios autorė eurodeputatė Ana Fotyga, dėl atkirčio Europos Sąjungai priešiškai išorės propagandai — pagal informacijos pavojingumą rezoliucija sulygina Rusiją su „Islamo valstybe“.

Virš 70 proc. europarlamentarų, kurie pritarė antirusiškai rezoliucijai, — Lenkijos, Lietuvos, Estijos, Kroatijos ir Slovėnijos deputatai. Tiesa, šį kartą dalyvauti kvailokoje kovoje su „Kremliaus propaganda“ atsisakė kai kurios tautiškai orientuotos Pabaltijo politinės jėgos.

Pavyzdžiui, koalicinės latvių partijos „Žaliųjų ir valstiečių sąjunga“ atstovė Iveta Grigule balsavo prieš. „Tik tada, kai Europos parlamentas taps pakankamai drąsus ir sugebės pažvelgti į akis realybei, kai nustos įvairiais klausimais įvairių šalių atžvilgiu naudoti dvigubus standartus, kai atsiras JAV „gerus darbus“ ir didžiųjų Europos Sąjungos valstybių „žygdarbius“ skelbianti deklaracija, kai pagaliau Europos parlamentas palaikys draudimą ES užsiiminėti ginklų prekyba, tame tarpe su į konfliktus įveltomis trečiosiomis šalimis, tada aš balsuosiu už tokią deklaraciją,“ — savo sprendimą aiškino politikė.

Nepaklusniai eurodeputatei jau pagrąsinta sankcijomis. :Ji peržengė visas ribas, kurias tik galėjo peržengti,“ — pranešė premjeras ir „Žaliųjų ir valstiečių sąjungos“ narys Maris Kučinskis, pridūręs, jog vadovybės lygyje gali būti palaikytas sprendimas pašalinti ją iš partijos. Už kitokį mąstymą latvių „žalieji“ radikaliai baudžia, nes prisilaikyti valdžios nubrėžtos generalinės linijos būtina. Latviška žiniasklaida šias valdžios nuostatas priima paklusniai.

Latvijos užsienio politikos instituto ir Gynybos ministerijos paskutinio tyrimo autoriai nurodo, jog latviškos propagandos priemonės vienbalsiai palaiko taip vadinamas Latvijos valstybės ginamąsias naujienas. Nacionalinė žiniasklaida pakeitė savo funkcijas: ne informuoti, ne šviesti, bet „neginčytinai“ saugoti valdžios poziciją. Kas tai, jei ne ypač sukaustyta propaganda, visiškai atsisakant objektyvumo? Ir tada nėra ko stebėtis, kad alternatyvus Rusijos požiūris sulaukia vis didėjančios paklausos.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 19 — id: `scraped:rubaltic_lt:2fafa62bffce5c6e`

**Title:** Naujoji Lietuvos valdžia pripažino demografiją pagrindine problema

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos valstiečių ir žaliųjų sąjungos lyderis Ramūnas Karbauskis pripažino demografinės krizės šalyje egzistavimą. Šios Sąjungos suformuota nauja vyriausybė žada išspręsti demografijos problemas. Tačiau rimtas darbas sprendžiant demografijos ir kitas socialines problemas prieštarauja politiniam kursui prezidentės Grybauskaitės ir už jos pečių stovinčių „landsbergininkų“, kuriems eilinių lietuvių problemos visada buvo antraeilės lyginant su jų geopolitiniais tikslais.

Pirmąjį šių metų pusmetį iš Lietuvos išvyko 6,5 proc. gyventojų daugiau, nei tuo pačiu laikotarpiu pernai. Lietuva, kaip ir Estija, Latvija, Slovakija, — vienintelės „Naujosios Europos“ šalys, iš kurių emigrantų srautas ne mažėja, o didėja. Lietuvoje jis auga sparčiausiai.

Kiekvieną valandą su Lietuva atsisveikina 4-5 žmonės, kasdien — 100 žmonių, per metus — 35 tūkstančiai. Kasmet šalis praranda 1,5 proc. gyventojų — Eurostatas prognozuoja, kad artimiausiais dešimtmečiais Lietuva praras 38 proc. gyventojų. Per pastaruosius 25 metus Lietuvos Respublika jau prarado daugiau kaip ketvirtadalį gyventojų: tokiu būdu, per 50-60 potarybinių metų ji jų praras du trečdalius.

Bet svarbios ne tik kiekybinės, bet ir kokybinės lietuviškosios emigracijos charakteristikos. Iš šalies masiškai bėga jaunimas, išvyksta vidutinio amžiaus darbingi žmonės — Lietuva virsta savo amžių baigiančių pensininkų namais. Tačiau demografinė situacija tokia, kad jų senatvė nebus tyli ir rami.

Gimstamumo mažėjimas ir rekordinė emigracija kritiškai didina Lietuvos visuomenėje dalį pagyvenusių žmonių, kuriems netrukus nebus iš ko mokėti pensijų, nes iš šalies išvyksta mokesčius mokantys darbingi gyventojai, o naujos kartos nesimato.

Be to, masiškai emigruoja atstovai tų profesijų, kurios gyvybingai svarbios palaikant socialinę infrastruktūrą. Tame tarpe gydytojai. Todėl Lietuvos demografinė krizė neišvengiamai iššauks socialinę krizę.

Daugelį metų ignoravę šią aštrią problemą, ją pagaliau pradeda pripažinti valdantieji politikai.

„Jei stovėdami prie lėktuvo žmonės tikėtų, kad rytoj bus geriau, jie persigalvotų ir neskristų“, — pasakė Karbauskis konferencijoje, skirtoje vyriausybės formavimui. Tačiau Lietuvos žemdirbių lyderis neturi vieningo recepto, kaip išvesti šalį iš to kelio, kuris veda link demografinės katastrofos. Pagerinti demografinę situaciją galima tik visumoj gerinant situaciją Lietuvoje. Kad žmonės nenorėtų išvažiuoti, jie turi tikėti Lietuvos ateitimi.

„Yra daug sisteminių klausimų: švietimas, sveikatos apsauga, ekonomikos vystymasis, regionų politika. Aš manau, svarbiausia — švietimas, jo kokybė, kad žmonės turėtų gerai apmokamą darbą Lietuvoje“, — teigia Ramūnas Karbauskis. Beje, priešrinkiminės kampanijos metu Lietuvos valstiečių ir žaliųjų sąjunga siūlė įvesti valstybines subsidijas jaunoms šeimoms būstams įsigyti.

T.y. norint išgydyti apleistą demografinę ligą (jei dar įmanoma ją išgydyti) reikalinga kompleksinė terapija.

Tačiau naujoji vyriausybė, savo prioritetu skelbdama socialinių problemų sprendimą, susidurs su tomis kliūtimis, kurių neįveikė buvusioji. Ta kliūtis — prezidentė Dalia Grybauskaitė ir už jos nugaros stovintys „landsbergininkai“.

Lietuvos dešiniesiems nerūpi liaudies išsaugojimas. Jiems išvis mažai rūpi Lietuva. Lietuva jiems — teritorinė platforma, ant kurios stovint galima užsiiminėti įvairiais geopolitiniais sumanymais. Pirmyn stumti ES „Rytų partnerystę“, potarybinėje erdvėje „eksportuoti“ demokratiją, steigti slaptuosius CŽV kalėjimus, dėl Lietuvos lenkų pyktis su Lenkija, su Baltarusija — dėl atominės elektrinės, o su Rusija — dėl ko tik pasaulyje įmanoma.

Lietuviai Grybauskaitei, Landsbergiui, Ažubaliui, Kubiliui ir į juos panašiems — medžiaga prakuroms.

Galbūt todėl, nepaisant gana stabilios ekonominės ir politinės situacijos, lietuviai taip sparčiai neria iš Lietuvos. Kokiai tautai patiks, kad sava valstybė ja visiškai nesirūpina — spjaudama į savo tautą, ji išradinėja naujas sankcijas prieš Rusiją, tiekia ginklus Ukrainai, remia Baltarusijos opoziciją.

Siekdama nors pabandyti šiek tiek ištaisyti demografinę situaciją ir sustabdyti gyventojų evakuaciją iš šalies, ši vyriausybė turėtų sugriauti susiklosčiusią politinę situaciją, pasisukti į lietuvius su jų opiomis problemomis veidu ir baigti tarptautinėje arenoje mojuoti kardu.

Bet tai padaryti nebus lengva: Dalia Grybauskaitė tebelieka Lietuvos prezidente, dėdulė Landsbergis — jos ypač artimu neoficialiu patarėju, ir visas tas Daukanto aikštėje dūzgiantis širšynas taip lengvai savo pozicijų neužleis. Norėdama realiai įveikti Lietuvos demografinę katastrofą, „žemdirbių“ vyriausybė turės pademonstruoti politinę valią ir tvirtumą, atsisakant to kurso, į kurį prezidentaudama abiem rankom įsikibusi laikėsi Grybauskaitė.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 20 — id: `scraped:rubaltic_lt:67d7e5120ec3e028`

**Title:** Europa daugiau nemaitins Pabaltijo

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Europos Sąjunga nuo sekančių metų ketvirtadaliu mažina Rytų Europos šalių palaikymo programų finansavimą. Po to, kai septyneriems metams bus priimtas ES biudžetas, nuo 2020 metų galimai bus nutrauktas „Naujosios Europos“ šalių finansavimas iš struktūrinių ES fondų. Europa daugiau nenori maitinti Pabaltijo ir kitų rytų europietiškų parazitų: Lietuva, Latvija ir Estija turės mokytis pačios užsidirbti pinigų.

Kochezijos politika — finansinis Centrinės ir Rytų Europos šalių palaikymas turtingomis Vakarų ir Šiaurės Europos šalimis. Jos tikslas — sulyginti senųjų, klestinčių Europos Sąjungos narių ir 2004 ir 2007 metais įstojusių į ES šalių pragyvenimo lygį ir ekonominį išsivystymą. Turtingos šalys — Vokietija, Prancūzija, Nyderlandai arba Švedija įneša į bendrą ES biudžetą mokestį, kuris ir suformuoja struktūrinius ES fondus, skirtus tokių vargingų ES šalių, kaip Rumunija, Vengrija arba Lietuva, ekonomikos ir socialinės sferos vystymosi finansavimui.

Takoskyra tarp ES šalių griežtai skiria tuos, kurie ES biudžetui atiduoda daugiau, negu paima, ir tuos, kurie daugiau paima, negu atiduoda. Prie pirmosios — šalių donorų grupės — priskiriamos ES sukūrusios, o taip pat Vakarų, Šiaurės ir Pietų Europos šalys, prisijungusios prie Europos ekonominės sąjungos 1970–1990 metais. Pavyzdžiui, Vokietija bendram europietiškam biudžetui atiduoda 11,9 milijardo eurų daugiau, nei paima. Prancūzija — 8,2 milijardo, Italija — 5 milijardais eurų, Nyderlandai — 2,3 milijardo, Švedija — 1,9 milijardo eurų daugiau, nei paima.

Dauguma dotuojamų šalių — buvusios socialistinės šalys, įstojusios į ES po 2004 metų: Lenkija, Bulgarija, Rumunija, Kroatija, Vengrija, Estija, Latvija, Lietuva ir kt. Siekiant įveikti jų socialinį ekonominį atsilikimą ir pasiekti pirmosios grupės šalių lygį, ir buvo sukurta kochezijos politika, pagal kurią šios šalys ir pradėjo kasmet gauti milijardines finansines injekcijas.

Rytų europietiškus išlaikytinius Briuselis finansavo pagrindinai iš trijų eurofondų: Europietiško regioninio vystymosi fondo, Europietiško socialinio ir Kochezijos fondo. Be šių pagrindinių, Briuselo biurokratija sukūrė daug dar šakinių eurofondų: Žemės ūkio vystymosi europietišką, Jūrų verslo ir žuvininkystės europietišką fondą ir kt.

Eurofondų lėšos pagrindinai buvo skiriamos infrastruktūros vystymuisi: buvo tikėtasi, kad ES struktūrinių fondų dotacijos sudarys Centrinės ir Rytų Europos šalių savarankiško ekonominio vystymosi pagrindą ir tos šalys po kelių dešimtmečių sugrąžins šiuos pinigus Briuseliui su kaupu. Tačiau praktikoje visa tai pasisuko daug liūdnesniu kampu.

Europietiška integracija ne tik nesukūrė Centrinei ir Rytų Europai savarankiško ekonominio išsivystymo pagrindo, priešingai — ji sunaikino tą pagrindą, suardė naujų ES narių nacionalines ekonomikas, atėmė iš jų savarankiškumo likučius ir pasodino ant eurofondų dotacijų „adatos“.

Pasak amerikiečių auditorių kompanijos KPMG „ES fondai Centrinėje ir Rytų Europoje“, pagal buvusio ES septynerių metų biudžeto rezultatus „Naujoji Europa“ yra depresinis Europos Sąjungos dotacinis regionas: 18 proc. šio regiono šalių bendro BVP sudaro ES struktūrinių fondų dotacijos.

Labiausiai priklausomos nuo eurofondų yra Pabaltijo šalys: Briuselio dotacijų injekcijos Lietuvos, Latvijos ir Estijos BVP viršija 20 proc.

„Pasakysime atvirai: praktiškai visa Latvijos statybų šaka laikosi dėka eurofondų užsakymų. Visi stambūs infrastruktūros objektai statomi europietiškais pinigais: ryškiausias pavyzdys — Rail Baltica. Visumoj europietiško finansavimo dėka latvių ekonomikoje sukuriama dešimtis tūkstančių darbo vietų, o kai kuriais paskaičiavimais — virš šimto tūkstančių. Todėl visiškai ne paslaptis, kad latvių ekonomika nėra savarankiška, ir dabartinis ekonominis stabilumas plius nedidelis augimas pagrindinai palaikom dėka pastovių europietiškų lėšų injekcijų, — rašo latvių ekonomistas Dmitrijus Smirnovas, prognozuojantis Latvijai ekonominę katastrofą, kurią, šalių donorų atsisakymo kochezijos politikos atveju, galima palyginti su 2008 metų krize. — Po eurofondų likvidavimo latvių ekonomika sumažės 15-20 proc. su iš to išplaukiančiomis pasekmėmis: nedarbo augimu ir pragyvenimo lygio sumažėjimu. Taip kad mes galime sulaukti naujų 2008 metų net bankams nebankrutavus.“ Tokios pesimistinės prognozės turi rimtą pagrindą. Pabaltijui ne šiaip gresia eurofondų atėmimas — jis jau prasidėjo.

Šis nutarimas buvo priimtas prisilaikant septynmetės finansinės perspektyvos, vienas iš kurios prioritetų yra kochezijos politika. Tačiau jau dabar ši politika koreguojama. Ir ką bekalbėti apie naują septynmetį ES biudžetą, kuris bus priimtas 2020 metais — tada turtingosios ES šalys gali visai atsisakyti remti skurstančias, o struktūrinius fondus — likviduoti. Taigi Europos Sąjungoje prie to ir einama.

Pirma, iš Europos Sąjungos traukiasi Didžioji Britanija: antroji stambiausia ES donorė, bendram europietiškam biudžetui skirdavusi jo 15 proc. Londonas jau atsisakė pervesti pinigus į Europietišką regioninio vystymosi fondą, o nuo pavasario nustos finansuoti kitus europietiškus fondus, ir po to, kai bus užbaigta su Brexit, bendrasis europietiškas biudžetas sumažės šeštadaliu.

Antra, šalis donores piktina Rytų Europa, užsisėdusi ant Vokietijos, Prancūzijos, Suomijos ir kitų šalių mokesčių mokėtojų sprando ir neužsidirbanti pati. Ir Brexit‘as tapo britų visuomenės reakcija į Rytų Europą: milijonai gyventojų balsavo už išstojimą iš Europos Sąjungos, todėl kad nenori daugiau matyti neišsenkančio lenkų ir pabaltijiečių juodadarbių srauto savo gatvėse.

Tokios pat nuotaikos stiprėja ir kitose Vakarų Europos šalyse. Visuotnas euroskepticizmo augimas provokuoja klausimą: kodėl savo kišenės sąskaita mes privalome kelti visokiems pabaltijietiškiems parazitams jų pragyvenimo lygį? Net jei pavyks išvengti euroskeptikų atėjimo į valdžią, „Senosios Europos“ elitui teks gelbėti Europietišką projektą pagal visuomenės reikalavimą. Tame tarpe — atsisakyti Rytų Europos dotavimo. Trečia, Pabaltijis Europos Sąjungoje daugiau negali tikėtis, kad JAV jį gins ir globos. Amerikos prezidento rinkimuose nugalėjo visiškas euroskeptikų bendramintis Donaldas Trampas. Jo užsienio politikos programoje — „nusimesti balasto“, t.y. nustoti maitinti, globoti ir remti begalę sąjungininkų parazitų. Amerikietiškam realizmui ir izoliacionizmui, kuriuos propaguoja Trampas, Rytų Europa su Pabaltiju — ne prioritetas, ir nėra ko gaišti laiko ginant juos Briuselyje, Paryžiuje ar Berlyne.

Ketvirta, kochezijos politikos fiasko — akivaizdus faktas. Galima užsiiminėti Pabaltijo ir Skandinavijos socialinio ekonominio vystymosi rodyklių palyginimu, o galima pasivažinėti Latvijos ir Lietuvos keliais ir savo akimis įvertinti jų išsivystymo lygio „sulyginimo“ su Vakarų ir Šiaurės Europa rezultatą. Prasti keliai, fabrikų ir gamyklų griuvėsiai, uždarytos atominės elektrinės, išmirę vienkiemiai, ištuštėję miestai ir begalinės emigrantų eilės Vilniaus ir Rygos oro uostuose. Ir į visą šią „sėkmės istoriją“ kasmet buvo pumpuojami Europos mokesčių mokėtojų pinigai?

Tokią nesveiką situaciją bet kokiu atveju reikėtų taisyti, tačiau visų europietiškų lyderių dabar pripažįstama Europos Sąjungos sisteminė krizė to reikalauja nedelsiant. 2004 metais atsiradusių išlaikytinių atsikratymas — praktiškai neišvengiamas scenarijus ES ekonominių ir socialinių problemų augimo sąlygomis. Lai savo gyvenimui užsidirba patys, jei nenori būti visiškai išvaryti iš Europos Sąjungos.

Ir jokie to pačio Pabaltijo skundai, dejavimai ir šukavimai apie „europietišką solidarumą“, „okupacijos pasekmes“ arba „agresyvią kaimynystę“ niekam Vakaruose nebus įdomūs. Pabaltijo politikams visada bus panosėn pakišamas pavyzdys šiaurės kaimynės Suomijos, kuri taip pat turi sienas su Rusija ir kuriai ši kaimynystė padėjo tapti viena iš turtingiausių ir socialiai sėkmingiausių pasaulio šalių ir ES donore, kuri į ES biudžetą įnešamomis lėšomis maitina ir tą patį Pabaltijį.

Jeigu Lietuva, Latvija ir Estija per ketvirtį amžiaus nesugebėjo padaryti taip, kaip Suomija, — tai jų, o ne Skandinavijos ir ne Vakarų Europos problemos. Jei šios šalys sunaikino normalius santykius su Rusija, kuri dabar atsisako jų tranzito paslaugų, perorientuoja savo krovinių srautą į Pabaltijo uostus ir atsisako matyti savo rinkoje pabaltijietiškus produktus — tai taip pat jų problemos.

Pabaltijo šalys paskelbė save „tikromis europietėmis“, ir jų įstojimas į Europos Sąjungą — „sugrįžimas namo“. Na ir lai maitina jas Europos Sąjunga.

Na, o jeigu europietiški giminaičiai maitinti šių šalių daugiau nenori, o „europietiškuose namuose“ į jas žiūrima ne kaip į lygiaverčius „europietiškos šeimos“ narius, o kaip į namų kenkėjus ir norima jų atsikratyti... ką gi, laipsniškas užgesimas Pabaltijo, iš kurio kito dešimtmečio metu išvyks mokesčius mokantys darbingi gyventojai, o Briuselis užblokuos eurofondų „dirbtinį kvėpavimą“, taps pamokančiu pavyzdžiu kitoms šalims, kas nutinka, kai visą savo vystymo modelį pradedi grįsti neapykanta kaimynui.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```
