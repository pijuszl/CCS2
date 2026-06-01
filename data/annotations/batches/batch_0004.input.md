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

### Article 1 — id: `scraped:rubaltic_lt:aafde4e5ebd6340b`

**Title:** Rusai sovietmečio Pabaltijyje: dar vienas įrodymas, jog „okupacijos“ nebuvo

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Situacija su rusakalbiais gyventojais trejose Pabaltijo respublikose skiriasi iš esmės. Jei Latvijoje rusakalbiai sudaro daugiau nei trečdalį gyventojų, tai Lietuvoje rusų mažiau nei 5 procentai. Tokia padėtis – sovietmečio paveldas, kai respublikų vadovybės – etniniai lietuviai, latviai ir estai – pačios sprendė, ar atsivežti migrantų iš kitų SSSR respublikų ir, jei taip, tai kokiam darbui ir kiek. „Rusų klausimas“ Pabaltijyje –tai dar vienas įrodymas, jog „sovietų okupacija“ Lietuvoje, Latvijoje ir Estijoje – grynas prasimanymas.

Lietuvoje etninių rusų procentas visada buvo palyginant nedidelis. Rusijos imperijos Vakarų krašto gubernijose rusų skaičius, kaip 1897 m., taip ir 1914 metais, nesiekė 6 procentų. Visiškai nežymią gyventojų dalį rusai sudarė ir tarpukario Lietuvoje. Taip, 1923 metais respublikoje gyveno 2,4% ar 2,5% rusų.

Vienintele vidurinio lavinimo įstaiga rusų kalba buvo Dėstytojų bendrovės Kauno rusų gimnazija, už mokslą kurioje reikėjo mokėti. Netgi pradinių mokyklų skaičius laikui bėgant mažėjo.

Pribloškiantis kontrastas: 1929 metais Lietuvoje buvo penkiolika pradinių rusų mokyklų, o jau 1936 metais, nacionalistinės Antano Smetonos diktatūros laikais, jų skaičius staigiai sumažėjo iki trijų. Antroje 1930 metų pusėje rusų vaikų, lankiusių mokyklą, skaičius nukrito žemiau 6 procentų.

Toliau įvyko Lietuvos sovietizavimas. Pasibaigus Didžiajam Tėvynės karui dalį atvykusiųjų rusų sudarė karininkai ir jų šeimos – žmonos, vaikai, susenę tėvai, o taip pat atsiųsti atstatyti, karo metu sugriautą Lietuvos pramonę, kvalifikuoti inžinierinių – techninių specialybių kadrai.

Tokia situacija buvo iki pat Stalino mirties.

Vieninteliu veržliai rusifikuojamu miestu sovietmečio Lietuvoje tapo Klaipėda, kur buvo įrengta galinga laivybos bazė. Ten intensyviai kūrėsi uosto infrastruktūra.

Greitu laiku Klaipėda tapo svarbiausiu SSSR prekybos uostu Baltijos jūroje. Pagrindinę uosto kompleksų aptarnavimo specialistų masę sudarė rusai (rusakalbiai).

Ir, žinoma, į Lietuvą vyko aukštos kvalifikacijos migrantai iš kitų SSSR respublikų realizuoti struktūrinių energetikos amžiaus projektus – pavyzdžiui, AE statybą Ignalinoje. Taip pat dalis darbininkų atvyko į Vilniaus, Kauno, bei kitų stambių Lietuvos miestų šiuolaikinių miegamųjų rajonų statybas.

Įdomūs 1989 metų duomenys. Rusai sudarė tik 9,4 % Lietuvos SSR gyventojų. Iš jų apie 38 % mokėjo lietuvių kalbą.

Palyginkim su padėtimi Latvijoje. 1989 metais Latvijoje rusai sudarė 34% visų gyventojų, iš jų latvių kalbą mokėjo daugiau nei 22 %.

Latvijos partinis elitas siekė didelę sunkaus, turinčio industrinę reikšmę, techniškai nedėkingo darbo apimtį perkelti ant, mažiau reiklių ir geriau intelektualiai paruoštų, darbo migrantų pečių, o tuo tarpu Lietuvos partinis elitas, kontaktuodamas su Maskva tokiu slidžiu klausimu, kaip nacionalinis, akcentavo į „lietuviško etniškumo“ išsaugojimą.

Atitinkamai, ten kur Latvijoje dirbo rusai, Lietuvoje dalį fizinių ir inžinierinių darbų atliko etniniai lietuviai.

Išimtis galima suskaičiuoti vienos rankos pirštais. Pati pagrindinė – tai jau paminėta Ignalinos AE statyba. Čia jau lietuviai, kad ir kaip norėdami, patys nesusitvarkytu.

Planingo rusų išstūmimo iš Lietuvos etninės kultūros ir sociologinio gyvenimo strategija davė savo vaisius. Taip, 1989 metais rusų dalis Vilniaus gyventojų tarpe sudarė 20 %, o šiuo momentu Lietuvos sostinėje gyvena vos daugiau nei 10 % rusų.

O 2020 metais rusų skaičius respublikoje sumažėjo iki 4,5%. Šiuo metu rusiškos etninės bendruomenės Lietuvoje skaičiaus kritimas tapo katastrofišku.

Tai leidžia prieiti išvados, jog šliaužiančios asimiliacijos ir latentinių apartheido formų taktika, naudojama Lietuvoje. sukėlė labiau negatyvias pasekmes, negu išskirtinai agresyvi ir tiesmuka segregacinė Latvijos politika.

Tarp kitko, ir oficialios Latvijos lingvocido politika prisidėjo prie etninės transformacijos. Taip, 1989 metais latviai, kurie pripažino rusų kalbą gimtąją, sudarė 42 % gyventojų, o 2011 metais 37,2 % gyventojų rusų kalbą pripažino bendravimo namuose (šeimos vidaus) kalba.

Tuo pačiu metu, remiantis 2021 metų tyrimais, bendras rusų kilmės gyventojų skaičius Latvijoje jau sudarė 24,5%.

Tokiam mažėjimui įtakojančių faktorių pakanka – natūralios priežastys, masinė migracija į ekonomiškai sėkmingesnes šalis, dalies etninių rusų marginalizavimas, sukeltas radikaliomis Latvijos valdžios reformomis kalbos ir ugdymo srityse.

Verta dėmesio situacija Estijoje. Jei 1897 metais rusų skaičius Estliandijos gubernijoje (neskaitant Jurvevo / Tartu) sudarė tik 3,3 %, tai 1930 m. – jau 8,2, kas buvo susieta su teritorinių pokyčių faktoriumi. Prie Estijos respublikos buvo prijungta nuo amžių rusiškos žemės Pečiorai, Izborskas, dešinioji Narvos pakrantė, Estiška Ingermanlandija.

Sovietmečio laikais Estijos SSR, bendrai paėmus, migracijos srautų atžvilgiu laikėsi lojalios politikos. Rusai, baltarusiai, ukrainiečiai bei kitų SSSR tautų atstovai atvykdavo į Estiją ir įsidarbindavo stambiuose pramonės įmonėse, specializuotose aukštojo mokslo įstaigose, mokslinio – tyrimo centruose, medicinos įstaigose.

1989 m. rusų skaičius sudarė vos daugiau 30% Estijos gyventojų. O visą trylikos metų nepriklausomybės laikotarpį, jų kiekis svyruoja nuo 24 iki 25%. Jų nežymus padidėjimas susijęs su atskirais aukštais ekonominiais rodikliais, kurie išskiria Estiją Latvijos ir Lietuvos fone.

Palanki socialinė-ekonominė atmosfera Estijos pasienio su Latvija rajonuose, o taip pat ir stambiuose miestuose – Tartu bei Taline – prisideda prie nedidelio kiekio migrantų atvykimo iš kitų Pabaltijo respublikų. Tarp ES bendros administracinės erdvės rėmuose persikėlėlių pastebima ir nedidelė dalis rusų (rusakalbių).

Tačiau tai nedaro principingos įtakos.

Papildoma įtampa buvo išprovokuota 2007 metais, kai Estijos valdžia demontavo paminklą tarybiniams kariams išvaduotojams – Bronzinį karį.

Svarbu paminėti ir kitą. Paskutiniais metais Estijoje vyrauja rusiškos bendruomenės atstovų marginalizavimo darbo rinkoje strategija.

Kartu su tuo, Estijos rusų pasiryžimas išvykti į sėmingesnes ES šalis, yra žymiai mažesnio lygio nei toks pats rusų kilmės Latvijos gyventojų pasiryžimas.

Atsižvelgiant į tokią socialinę etninę politiką, galima pasakyti, jog Estijos visuomenė greitu laiku bus standartizuota – neprestižinės ir žemos kvalifikacijos profesijos bus paliktos rusų kilmės gyventojams, o prestižinės ir aukštos kvalifikacijos profesijos atiteks etniniams estams.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 2 — id: `scraped:rubaltic_lt:acbba1693a1e5ab2`

**Title:** Lietuva išprašė iš JAV pinigų kovai su Kinija

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Vilnius pasirašė tiesioginių paskolų 600 milijonams dolerių susitarimą su JAV Eksporto – Importo banku (Ex-Im Bank). Apie tai pranešė Lietuvos užsienio reikalų ministerijos spaudos tarnyba. Pabaltijo respublikos URM vadovas Gabrielius Landsbergis šį sandorį pateikia kaip didelę pasipriešinimo Kinijai pergalę. Noras amerikiečiai, teikdami paramą Lietuvai priešintis KLR „prekybinei agresijai“, faktiškai remia patys save.

Oficialus vizitas į Vašingtoną Gabrieliui Landsbergiui įvyko pačiu tinkamiausiu metu. Lapkričio pradžioje sociologai paviešino apklausos rezultatus, kurie rodo, jog Lietuvos užsienio reikalų ministras – vienas iš pačių nepopuliariausių savos šalies politikų. Jį negatyviai vertina 57,2% apklaustųjų.

Blogesni reikalai tik pas ekonomikos ir inovacijų ministrę Aušrinę Armonaitę. Ji, tarp kitko, nepretenduoja į naujojo „tautos tėvo“ ir būsimo prezidento vaidmenį.

Nieko nėra nuostabaus tame, jog kelionę į JAV Landsbergis bandė paversti savęs liaupsinimo akcija.

Netgi Landsbergio priėmimo laikas, jei juo tikėti, buvo parinktas specialiai. „Simboliška, kad Valstybės sekretorius (JAV Antoni Blinken - RuBaltic.Ru pastaba) mus priėmė Tarptautinę demokratijos dieną ir kad susitikimo metu buvo paskelbta apie Baltarusijos reikalų skyriaus įkūrimą JAV ambasadoje Vilniuje, kuriame bus sutelktos JAV pastangos siekti demokratinių pokyčių Baltarusijoje. Tai irgi ženklas, kad Lietuvos indėlis, kovojant už vertybėmis grįstą valstybių bendradarbiavimą, Vašingtone yra vertinamas“, – sakė ministras G. Landsbergis.

Su Blinkenu jis aptarė pačius „aktualiausius“ klausimus: regioninio saugumo stiprinimą, amerikiečių karinių pajėgų buvimą Lietuvoje, bendro atsako „hibridinėms grėsmėms“ parengimas. Nebuvo apsieita ir be kaltinimų Rusijai, kuri, esą, stiprina įtampą pasienyje su Ukraina.

Atsakydamas į tai, Pekinas pažemino diplomatinių santykių su Vilniumi lygį. Dabar Lietuvos verslas skaičiuoja potencialius nuostolius, kylančius dėl prekybinių-ekonominių santykių su Padangių šalimi nutraukimo. Todėl nenuostabu, jog iš Jungtinių Valstijų Landsbergis atvežė, jo nuomone, naudingą susitarimą su Ex-Im Bank.

Lietuvos šalies pareiškimai byloja, jog iš JAV Eksporto-Importo banko ji gavo 600 milijonų dolerių sumos tiesioginių paskolų garantiją, Šiais pinigais galės pasinaudoti abiejų šalių kompanijos, kurios yra orientuotos į JAV ir Lietuvos prekybinių – ekonominių ryšių stiprinimą.

Kitaip sakant, kalbama tik apie lengvatinį kreditavimą.

Pati technologija nėra nauja. JAV Eksporto – Importo bankas buvo įkuriamas specialiai tam, kad stimuliuoti Amerikos eksportą į konkrečias šalis. Panašios įstaigos egzistuoja ne tik Amerikoje.

„Plečiame ekonominius ryšius su strateginiais partneriais ir ieškome įvairių naujų alternatyvų Lietuvos verslui, patiriančiam prieš Lietuvą nukreiptą ne rinkos ekonomikos šalių ekonominį spaudimą.“, − kontekste su Ex-Im Bank sakė G. Landsbergis.

Aišku, jog ne rinkos ekonomikos šalimis jis supranta Kiniją ir Baltarusiją (šiandieną, būtent su jomis yra susijusios pačios didžiausios lietuviško verslo rizikos). Nesamprotausime, kaip tai teisinga. Landsbergis gali visada prisidengti tų pačių JAV ir Europos parlamento pozicija, kurie atsisako pripažinti KLR ekonomiką rinkos ekonomika.

Iškrentančias importo iš Kinijos apimtis dalinai pakeis amerikietiškos prekės, o Lietuvos kompanijos, kurios eksportuoja savo produkciją į Kiniją, persiorientuos į Jungtinių Valstijų rinką. Tame juos parems Ex-Im Bank paskolos.

Aišku, Kinijos nėra pagrindinių Pabaltijo respublikos užsienio ekonominio bendradarbiavimo partnerių sąraše. Praeitais metais jo prekių apyvarta sudarė apie 1,5 milijono dolerių, iš kurių tik 300 milijonai dolerių atiteko lietuviškam eksportui.

Tačiau, dar prieš keletą metų oficialus Vilnius ragino verslininkus aktyviai vystyti prekybą su Kinija.

Pavyzdžiui, prekiaujanti mediena Medvita Kinijos liaudies respublikoje realizuoja 99 % savo produkcijos.

„Kinų partneriai naudojasi bet kokia proga idant nutraukti santykius“, - pažymi Lietuvos grūdų perdirbėjų ir prekybininkų asociacijos prezidentas Karolis Šimas

Bet ar efektyvus bus šis instrumentas? Ex-Im Bank gali tik teikti lietuviams paskolas, Bet tai nėra neatlyginama parama – pinigus vis vien prisieis gražinti. Ir niekas negarantuoja Kinų „prekybinės agresijos“ aukoms, jog jų prekės turės paklausą Jungtinėse Valstijose.

Taip pat lieka klausimas, kokiu būdu bus skirstoma bendra paskolų apimtis tarp lietuviškų ir amerikietiškų kompanijų. Tikriausiai, Ex-Im Bank pirmenybę teiks pastarosioms.

„Remdamas“ Lietuvos kovą su Kinija, jis visų pirmą, remia savo tėvyninį verslą.

Lietuvos jūrų krovos kompanijų asociacijos prezidentas Vaidotas Šileika prognozuoja, jog šalies tranzito verslui tai bus stiprus smūgis: „Konteinerių perkrova Klaipėdos uoste sumažės maždaug 30 – 50 % ir dėl to kentės ne tik uosto kompanijos, bet ir visa logistikos grandinė – kompanijos rinksis Lenkijos ir Latvijos uostus, dėl ko kils pervežimų kainos ir brangs prekės“.

Landsbergis ir toliau tvirtina, jog „kinų grėsmės“ akivaizdoje Lietuvą visokeriopai remia JAV.

Na o iš tikrųjų, visa ši parama atsiriboja Valstybės departamento pareiškimais ir Ex-Im Bank paskolų lėšomis. Kuriomis pasinaudos patys amerikiečiai.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 3 — id: `scraped:rubaltic_lt:0557b8440c14f758`

**Title:** Pabaltijys netenka pagrindinio sąjungininko kovoje už tai, kad Rusija pripažintų „sovietų okupaciją“

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Galimas bendrijos „Memorialas“ likvidavimas Rusijoje (Rusijoje pripažinta užsienio agentu - RuBaltic.Ru pastaba) Pabaltijo šalyse sukelia nuoširdų pasipiktinimą. „Memorialas“ užsiiminėjo tuo pačiu, kuo ir Pabaltijys po TSRS subyrėjimo: juodino sovietišką periodą. Stiprėjant šiai organizacijai Lietuvoje, Latvijoje ir Estijoje vylėsi, jog kada nors Rusija pripažins „sovietų okupaciją“ ir sutiks išmokėti pabaltijiečiams materialinę kompensaciją. Memorialo“ marginalizavimas ir, tuo labiau, jo panaikinimas nepalieka Pabaltijui jokių šansų, jog „puiki ateities Rusija“ užmokės ir atgailaus.

„Tai yra įspūdingą darbą Rusijos atminties politikoje, stalinizmo, apskritai, komunizmo nusikaltimų išaiškinime padariusi organizacija. Jos įdirbis yra milžiniškas. Archyvai, kurie yra patiems rusams labai svarbūs, yra didžiuliai“, – komentavo teismo procesą dėl „Memorialo“ likvidavimo Lietuvos gynybos ministras Arvydas Anušauskas. Kad Rusijos auditorija išgirstų Lietuvos balsą, Anušauskas nepraleido progos „įkąsti“ Rusijai. „Tokios organizacijos naikinimas rodo, kad Rusija jau stovi tame kelyje, kuriame buvo Stalinas. Ir ne kitaip“, - sakė aukštas pareigas užimantis „landsbergistas“.

Arvydas Anušauskas – ne pirmas, ir, tikėtina, ne paskutinis žmogus Pabaltijyje, kuris palaiko „Memorialą“.

Tai ir yra Pabaltijo respublikų intereso, kuris nėra įdomus pačiai Rusija, paaiškinimas. Pabaltijui tapo norma atidžiai sekti Rusijos vidaus politiką ir įsikišti į Rusijos vidaus reikalus. Bet čia pats Lietuvos gynybos ministras komentuoja rusišką siužetą, kuriuo rusai beveik nesidomi.

Kodėl? Todėl, jog „Memorialas“ – tai normalus Baltijos šalių sąjungininkas Rusijoje. Organizacija buvo įsteigta lygiai taip pat, kaip ir Lietuvos „Sąjūdis“: „paremti persitvarkymą“, kovoti su konservatyviais jo priešininkais, ir ne be KGB dalyvavimo.

Šiuo atveju buvo numanoma kova istorinės politikos priemonėmis: sovietų represijų hiperbolizavimas ir TSRS istorijos juodinimas, visą tai turėjo įrodyti, jog persitvarkymas yra būtinas.

Maždaug tuo pačiu ir tuo pat metu užsiiminėjo „Tautos frontai“ Pabaltijyje.

Deklaruojamas „Memorialo“ tikslas – pasakoti apie politinių represijų aukas, kad jos niekada nepasikartotu – suprantama, yra kilnus. Visai kitą – priemonės, kurios, esą, pateisina šį tikslą.

Niekas neneigia, jog 1937 metais TSRS buvo masinės represijos. Bet persitvarkymo metu prireikė išgalvoti skaičių – 15-20 milijonų sušaudytų bei siaubingu melu aptemdyti keleto šimtų tūkstančių nuo „didelio teroro“ realiai žuvusių atmintį. Kam to prireikė? Tam, jog skaičius 15-20 milijonų „skamba“, daro reikalingą psichologinį poveikį ir tarnauja ryškiu tvirtinimo, jog TSRS buvo „Blogio imperija“, įrodymu.

Tą patį principą „tiesa nieko nereiškia“ savo istorijos politikoje naudoja Pabaltijo šalys. Niekas neneigia 1940 metų stalininių deportacijų iš Lietuvos, Latvijos ir Estijos. Bet šios deportacijos Pabaltijyje skelbiamos sovietišku genocidu, „mūsų Holokaustu“. Priverstinis didelių gyventojų grupių perkėlimas į naują gyvenamąją vietą lyginamas su jų fiziniu išnaikinimu.

Kartu su tuo, informacija apie savo „didvyrių“ dalyvavimą realiame Holokauste yra neigiama ir visokeriopai slepiama.

Ne veltui už rusišką nevyriausybinę organizaciją užsistojo Lietuvos gyventojų genocido ir rezistencijos tyrimo centras (LGGRTC) – tokia pati siaubo apie sovietmetį išgalvojimo tarnyba, tik ne rusiška, o lietuviška, ir ne marginalinė, o maksimaliai artima valdžiai.

„Memorialo“ surinktas neįkainuojamas istorinis archyvas, jo parama sovietų periodo tyrimui buvo ir lieka labai svarbiu ne tik Lietuvai, bet ir daugumai, patyrusių sovietų okupaciją, valstybių, todėl „Memorialo“ veiklos nutraukimas, šios organizacijos sunaikinimas tapo ne tik Rusijos ir jos piliečių, bet ir visos tarptautinės bendrijos didele netektimi“,- sakoma LGGRTC direktoriaus kreipimesi.

Pasakyta gana atvirai.

Ir ne todėl, kad „neįkainuojamame“ „Memorialo“ archyve yra istoriniai šaltiniai, įrodantys sovietų Pabaltijo okupaciją. Visų pirmą, „Memorialas“ – jis kaip Pabaltijo politikai: ne apie istorinius šaltinius, o apie publicistinę demagogiją. Antra, jei tokie šaltiniai ir būtų buvę, užsienio agentas ir jo rėmėjai jau ne kartą juos būtų iš tų archyvų paėmę ir perdavę Pabaltijui.

Reikalas tame, jog kaip Pabaltijo istorijos falsifikavimo fabrikų paskirtis ugdyti vietiniuose tituliniuose gyventojuose aukos kompleksą, taip ir „Memorialo“ paskirtis po 1991 metų Rusijos piliečiuose ugdyti kaltės kompleksą. Mūsų šalis – grynas blogis, mes – kolonizatoriai, mes – okupantai, mes turime kolektyviai atgailauti už mūsų aukas.

Bet nesusiklostė. Ir nesusiklostys. Rusai atsisako mokėti ir atgailauti. Ir joks „Memorialas“, nesvarbu, ar jis veiks, ar neveiks, šios situacijos nepakeis.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 4 — id: `scraped:rubaltic_lt:5a072fc8273cf650`

**Title:** Santykiuose su Lukašenka Vokietija „pamiršo“ Lietuvą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
„Jei kalbama apie kokius tai susitarimus, kurie turi būti privalomi Lenkijai ir Lenkijos valdžiai, arba apie tokius, kuriuos lenkų valdžia turi kokiu tai būdu vykdyti, tai bus susitarimai, kuriuos sudarėme išimtinai mes, tose formatuose, kuriuose mes tiesiogiai dalyvaujame, kuriuose Lenkija atstovauja atitinkame lygyje“, - komentavo Lenkijos prezidentas Andrzei Duda Angelos Merkel derybas su Aleksandru Lukašenka dėl migracijos krizės sureguliavimo prie Baltarusijos – Lenkijos sienos.

Lenkijos lyderio pasisakyme jaučiamas gana rimtas susierzinimas.

Ir dar daugiau žeminančio, Vokietija dėl situacijos prie Lenkijos sienos derasi netgi ne su Putinu, o su Lukašenka. Tarp kitko, iš pradžių Angela Merkel dėl krizės sureguliavimo ketino susitarti būtent su Putinu. Tai, tarp kitko, dar ta situacija: vokiečiai sutaria su rusais dėl Lenkijos sienos...

Tačiau Rusijos lyderis išgelbėjo lenkus nuo skausmingų istorinių analogijų, nurodydamas  Merkel į tai, jog, jei probleminė situacija susiklostė  prie baltarusių – lenkų sienos, tai ir ją spręsti reikia kontaktuojant su Baltarusijos ir Lenkijos vadovybe. Rusija čia išvis ne prie ko.

Su Lenkijos vadovybe Vokietija ir taip pastoviai kontaktuoja. Bet jei bandyti kontaktuoti su oficialiu Minsku, tai būtu gražu ir politiškai korektiška organizuoti ne dialogą, o mažiausiai, trialogą – dalyvaujant Lenkijai. Dar geriau polilogą, kur dalyvauja Lenkija, Lietuva ir Latvija,  tai yra visos Europos Sąjungos šalys - sąjungininkės, kurias palietė migracinė krizė.

Reikalas ne tame, jog, kol kas dar frau kanclerę, nedomina Rytų Europos šalių – ES ir NATO narių mintys ir jausmai. Kaip tik atvirkščiai, Angela Merkel – nusistačiusi priešingai amerikietiškam stiliui nusispjaut į sąjungininkus. Merkel stilius – švelninti aštrius prieštaravimus ir visomis išgalėmis išsaugoti taiką „europietiškoje šeimoje“.

Tačiau, atvejyje su Lenkija ir Pabaltiju likti ištikimu savo stiliui dažnai nebūna galimybės. Jeigu, pavyzdžiui, dabar Merkel nuspręstu laikytis politinių taisyklių, kas iš to gautųsi? Pradžioje Lenkija ir Lietuva atsisakytu kalbėti su Lukašenka, po to „nulietu“ žiniasklaidai informaciją, jog Merkel pageidauja susiskambinti su „paskutiniuoju Europos diktatoriumi“ ir organizuotu skandalą, o galų gale prisijungtu prie pokalbio su Lukašenka su sąlyga, jog jame dar dalyvaus Latuško ir Tichanouskaja.

Esant kitokiai situacijai Berlynas išklausytų savo rytinius sąjungininkus, bet stovint ant karinio konflikto slenksčio prie pat NATO ir KSSO sienos „mamytei“ Merkel nėra kada vargintis su jais.

Taip visada buvo santykiuose su Rusija, ir Rytų Europoje jau susitaikė su tuo, jog lyderiai – JAV, Vokietija ir Prancūzija su Putinu bendrauja apeidami juos, sąjungininkų neklausia: ką jie galvoja dėl dialogo su Kremliumi. Tačiau pokalbis dar ir su Lukašenka apeinant NATO narius iš Rytų Europos – tai jau ypatingas pažeminimas.

Baltarusijos Respubliką kaimynai iš vakarų pusės laiko jiems Dievo duotu misionierinės veiklos lauku. Lenkija ir Lietuva (mažiau – Latvija) dešimtmečiais

baltarusiams ugdė „naująją elitą“, tai yra palaikė baltarusišką opoziciją, formavo Baltarusijos visuomeninę nuomonę, ten ruošė „demokratines revoliucijas“. Jie įprato save vadinti Europoje vyriausiaisiais dėl Baltarusijos, ir susitaikyti su tuo, jog lenkus ir pabaltijiečius su jų ambicijomis nukelia į šoną dėl derybų su Lukašenka, jiems beveik neįmanoma.

Merkel su Lenkijos prezidentu nesiaiškino. Baigiantis politiniai karjerai galima sau leisti parodyti sąjungininkams visą tai, ką tu apie juos galvoji.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 5 — id: `scraped:rubaltic_lt:e31bd027c4b65556`

**Title:** Lietuva surengė mirtinai sergančio režisieriaus pjudymą už „sovietų okupacijos“ neigimą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Nereikia smerkti žmogų už tai, jog, iš pradžių jis tvirtino vieną, o paskui rašo kitą. Rimas Tuminas – Lietuvos pilietis, ir tuo viskas pasakyta. Tai Rusijoje jis galėtu laisvo pokalbio metu pasakyti viską, ką galvoja. Būtu pasakęs Vladimirui Pozneriui, jog Lietuvoje buvo sovietų okupacija – nieko už tai Rusijoje jam nebūtu. Dargi taptų „senosios gvardijos“ – liberalinės inteligencijos, kuri kiekvieną pirmadienio naktį žiūri programą „Pozner“, stabu.

Bet tai, gi, „demokratinė“ Lietuva. Savo „pasiaiškinimą“ jai Tuminas, pagal visus požymius derino su advokatu, kad nepapulti už grotų už „okupacijos“ neigimą.

LRT kanalas - lietuviškas Pirmojo kanalo analogas – paskelbė, jog bandė susiskambinti su Rimu Tuminu, bet šis nepakėlė ragelio, kadangi serga vėžiu, jis hospitalizuotas ir ruošiamas operuoti. Tačiau Lietuvos valstybiniai televizijai netgi mirtina liga – nesudaro pagrindo nesikalbinti prie žmogaus, kai kalbama apie pasikėsinimą į oficialiąją ideologiją.

„R. Tuminas savo pasisakymais ne kartą kėlė audras Lietuvoje. 2015-aisiais su J. Vachtangovo teatro spektakliu „Nusišypsok mums, Viešpatie“ viešėdamas Niujorke pateisino kietą Vladimiro Putino ranką, sakydamas, kad griežtas valdymas Rusijoje tiesiog būtinas“, - rašoma LTR Interneto svetainėje.

Tikriausiai bus ir administracinės šio „nagrinėjimo partijos komitete“ pasekmės. Lietuvos kultūros ministerijoje manoma jog „Kremliaus agento“ pasiaiškinimų nepakanka, kad jam palikti Vilniaus Mažąjį dramos teatrą, kuriam jis taip pat ir vadovauja.

„Pirmiausia norėtųsi gerb. R. Tumino nuomonės apie tai, kokias pasekmes sukėlė jo interviu ir kokių pasekmių ateityje jis gali turėti Mažajam teatrui. Lauktume jo komentaro Lietuvos žmonėms, šalies žiniasklaidai“, – sako Lietuvos kultūros ministras Simonas Kairys.

Tai yra, be įtikinančio atgailos akto, saviplakos, ir pačio savęs apmėtymo akmenimis, režisieriui iš Rusijos į Lietuvą gėriau negrįžti. Susitikimas su istorine tėvyne įžymiam lietuviai gali tapti baisesniu ne vėžinis navikas.

Apie ką sako ši makabrinė istorija?

Ar galima Rusijoje įsivaizduoti, jog Pirmasis kanalas skambina į ligoninę mirtinai sergančiam vėžiu kultūros veikėjui, reikalaudamas pasiteisinimo už Putino kritiką? Jei taip atsitiktų, skandalas būtu tęsiamas kelėtą mėnesių.

Dėl Tumino kazuso Lietuvoje, geriausiu atveju, stengiasi nutylėti. Blogiausiu – prisijungia prie kolektyvinio pjudymo ir pradeda moralinį režisieriaus naikinimą.

Taip, kad Lietuvos dydis, jos ES ir NATO narystė, neturi nieko apgaudinėti dėl „demokratijos“, kuri ten viešpatauja. Sovietmečiu buvo priimta sakyti, jog ne tą šalį pavadino Gondurasu. Mūsų laikais ne tą šalį vadina Mordoromu.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 6 — id: `scraped:rubaltic_lt:97100b3d27c767b1`

**Title:** Vokietija sugriaus Pabaltijo planus dėl ES „energetinės nepriklausomybės“ nuo Rusijos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Federalinė Vokietijos tinklų agentūra neterminuotam laikui pristabdė „Šiaurinio srauto – 2“ sertifikavimą. Ši naujiena Europos biržose sukėlė veržlų kainų augimą. Nord Stream 2 AG spaudos tarnyba nekomentuoja vokiečių reguliatoriaus sprendimo, bet „Gazpromui“ nieko baisaus neatsitiko. Greičiau atvirkščiai: kalbama apie naujos kompanijos registravimą, kuri atitiks nepriklausomo „Šiaurinio srauto – 2“ operatoriaus kriterijams. Jos pagalba dujotiekį galima iškelti už ES Trečiojo energetikos paketo ribų, kurį savo metu lobijavo Lenkija ir Baltijos šalys, idant išstumti Rusiją iš Europos dujų rinkos.

„Šiaurinio srauto – 2“ sertifikavimas parsidėjo daugiau nei prieš dvejus mėnesius. Nei Federalinė VFR tinklų agentūra, nei ekonomikos ir energetikos ministerija niekada neprognozavo šio proceso pabaigos termino, kuris atliekamas prieš pradedant fizinį tiekimą iš trečiųjų šalių bet kuriuo magistraliniu dujotiekiu.

Bet Bundestago ekonomikos ir energetikos komiteto vadovas Klaus Ernst neseniai sakė, jog, vargu, kad šias metais pradės veikti „Šiaurinis srautas – 2“. Jo žodžiais tariant, Nord Stream 2 AG (projekto kompanijos-operatoriaus) paraiškos nagrinėjimą reguliatorius gali uždelsti iki sausio pradžios, o po patikrinimą pradės Europos komisija. Ji gali atidėti dujotiekio paleidimą dar keturiems mėnesiams.

Tą patį nurodė ir agentūra Bloomberg: sprendimą dėl Nord Stream 2 AG sertifikavimo Federalinės tinklų agentūros atstovai turi priimti iki sausio 8 dienos, po to Europos komisija patikrins ar projektas atitinka europietiškų įstatymų reikalavimams. Tam jai duodamas dvejų mėnesių terminas, bet, atskirais atvejais, procedūrą galima pratęsti. Tokiu būdu nustatyta galutinė „Šiaurinio srauto – 2“ paleidimo data - 2022 metų gegužės mėnesio 8 diena.

Rinka iš karto sureagavo į Federalinės VFR tinklų agentūros sprendimą: TTF biržoje fjučersų kaina pirmą kartą po spalio 20 viršijo 1100 dolerių už tūkstantį kubų. Panašu, kad Treiderius nenuramina pareiškimai apie tai, jog politika čia nieko dėta.

Iš pirmo žvilgsnio gali pasirodyti, jog, iš tikrųjų, vokiečiai, naudodamiesi formaliomis dingstimis, sudaro dirbtines kliūtis „Šiauriniam srautui – 2“.

Kodėl gi, nespėlioti, jog vokiečių reguliatorius yra naudojamas kaip svertas, skirtas Maskvos spaudimo?

Žibalo į ugnį, pavyzdžiui, papila Aukščiausios Ukrainos Rados partijos „Opozicinė platforma – Už gyvenimą“ (OPUG) deputatas Vadimas Rabinovičius. „Čia yra „Šiaurinio srauto“, kurį reikia sustabdyti, klausimas. Tam, kad jį sustabdyti, dabar vystoma istorija su migrantais, vystoma karo istorija (Rusijos ir Ukrainos – RuBaltic.Ru pastaba). Jau šiandieną Jungtinės Valstijos pareiškė, jog reikia įvesti sankcijas, kad sustabdyti „Šiaurinį srautą-2“. Todėl, jog jiems reikalinga energetinių resursų tiekimo čionai monopolija“, - tvirtina Rabinovičius.

Truputi kitaip į šią situaciją žvelgia partijos „Alternatyva Vokietijai“ (AV) partijos atstovas Albertas Brainingeris. Jis mano, jog formaliai nepriklausomas reguliatorius, paprasčiausiai, nori sulaukti naujos valdančios koalicijos suformavimo.

„Viskas ne taip paprasta, sunku pasakyti, koks komponentas vyrauja – politika ar vokiška biurokratija, - samprotauja Brainingeris. – Tikriausiai, reguliatorius surado sertifikavimo atsisakymo pretekstą. Koalicija kol kas nesuformuota, ir reguliatorius, nori išlošti laiko, kol šis klausimas nebus sureguliuotas... Suprantama, politiniai komponentai yra, šis projektas buvo politizuotas nuo pat pradžios“.

Bet kokiu atveju Brainigeris taip pat linkęs vykstančiame įžiūrėti politinius motyvus.

Vokiškas reguliatorius paaiškina, jog užtrūkimas yra susijęs su projekto organizacinės struktūros performinimu. Nord Stream 2 AG reikia įsteigti atskirą dukterinę įmonę valdančią vokišką „Šiaurinio srauto-2“ atkarpą. Kodėl? Reikalas tame, jog „Gazpromas“ per savo dukrą siekia gauti nepriklausomo dujotiekio operatoriaus statusą ir apeiti ES Trečiojo energetikos paketo normas, kurios dirbtinai apriboja vamzdžio pralaidumą.

Tai ir yra pagrindinė „Šiaurinio srauto-2“ sertifikavimo intriga: ar leis Vokietija išnaudoti visą jo galingumą?

Tikriausiai, nagrinėjant dokumentus, reguliatorius priėjo prie išvados, jog Nord Stream 2 AG neatitinka nepriklausomo operatoriaus kriterijų. Bet jei vokiškai vamzdžio atkarpai įsteigti atskirą kompaniją (ir kartu su tuo atsižvelgti į vokiečių valdininkų rekomendacijas), tai problema bus išspręsta. Tai ne kliudo paleisti „Šiaurinį srautą-2“.

Būtent taip tai vertina Kremliuje. Rusijos prezidento atstovas spaudai Dmitrijus Peskovas pareiškė, jog nelaiko vokiečių reguliatoriaus sprendimą politizuotu: „Šiuo atveju tikrai yra tam tikri protokolai, europietiškų įstatymų normos tokiam atvejui. Ir kompanija operatorius yra pasiruošusi įvykdyti visus, galiojančių įstatymų reikalavimus, kad kuo greičiau paleisti, šį, kiekvienam svarbų projektą“.

Bet dar labiau parodomoji, tai Kijevo reakcija. Kol „visažinė“ žiniasklaida šėrė savo auditoriją eiliniu feiku apie Rusijos“ pralaimėjimą“, „Naftogazo“ vadovas Jurij Vitrenko ragino savo tėvynainius prieš laiką šampano negerti.

„Iš gerų naujienų - „Šiaurinio srauto-2“ sertifikavimas pristabdytas. Bet viskas ne taip jau vienareikšmis. Gazpromas imasi juridinių triukų. Vokiečių reguliatoriui Gazpromas pareiškė apie savo ketinimą Vokietijoje įkurti dukterinę kompaniją, kuri bus lyg tai nepriklausomas „Šiaurinio srauto-2“ vamzdyno operatorius, bet tik tos atkarpos, kuris randasi Vokietijos teritorijoje. Tai pasišaipymas iš europietiškų taisyklių. Tai visiškai neatitinka europietiškiems dujotiekių sertifikavimo įstatymų reikalavimų“, - rašė Vitrenko, ir iš karto paragino JAV įvesti sankcijas naujam (dar neįkurtam!) vokiškos „Šiaurinio srauto-2“ atkarpos operatoriui.

Būtu verta „Naftogazo“ vadovui pateikti vieną principingai svarbų patikslinimą: „Gazpromas“ ne pats nusprendė įkurti „dukrą“, kuri valdys vokiškąją vamzdžio atkarpą. Iš pradžių jam tai rekomendavo Federalinė VFR tinklų agentūra.

Lieka atviru klausimas, ar sugebės „Šiaurinis srautas-2“ apeiti ES Trečiojo paketo normas. Bet Nord Stream 2 AG sertifikavimo pristabdymas „Gazpromui“ yra greičiau gera naujiena.

Juk dabar Rusijos monopoliją nejaudina projekto paleidimo terminai. Svarbiausiai – panaikinti „Šiaurinio srauto-2“ apkrovos apribojimus ir, tuo pačiu, sudaryti tranzito per Rytų Europą „“nunulinimo“ prielaidas.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 7 — id: `scraped:rubaltic_lt:0b36fc000092450e`

**Title:** Požiūris į derybas su Lukašenka suskaldė Lietuvą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Naujiena apie Vokietijos kanclerės Angelos Merkel skambutį Baltarusijos prezidentui Lietuvoje sukėlė tikrą politinę audrą. Valdančios konservatorių partijos atstovai demaskuoja Merkel, jog ši nukrypo nuo „tikrosios Vokietijos pozicijos“, o Lietuvos Prezidentūra pripažįsta, jog norint išspręsti migrantų problemą, dialogas su Lukašenka yra būtinas. Požiūris į Baltarusijos prezidentą faktiškai suskaldė politinę Lietuvos vadovybę.

Vokietijos ir Baltarusijos lyderių pokalbį telefonu galima pavadinti jei ne istoriniu, tai, bent, gana žymėtinu įvykiu. Nuo „paskutinio Europos diktatoriaus“ perrinkimo jie nė karto nebendravo. Praėjusių metų rugpjūtyje Merkel skambino Lukašenkai – pastarasis nepakėlė ragelio. Tarp kitko, tada Baltarusijos prezidentas pagal visus formalius požymius dar buvo legitimus (Europoje laikoma, jog jo įgaliojimų terminas oficialiai baigėsi rudenį).

Po to, Merkel ir Lukašenka sklandžiai pasikeitė vaidmenimis. VFR kanclerė nenorėjo bendrauti su „nelegitiminiu“ valdytoju, o Baltarusijos lyderis davė suprasti, jog jis nieko prieš konstruktyvių santykių atnaujinimą su šalimis – ES narėmis.

„Valstybės vadovas pateikė bendrą pasiūlymą kaip išspręsti situaciją. Šalys susitarė, jog kol kas neviešins konkrečių detalių. Angela Merkel paprašė pauzę atitinkamam klausimui aptarti su Europos Sąjungos nariais. Po to turi būti dar vienas šalių lyderių pokalbis telefonu“, - praneša Sputnik Belarus, remdamasis Lukašenkos žodžiais.

Pats prezidentas priduria, jog „pirmasis klausimas“ (kuris buvo aptariamas pokalbio metu) –pabėgėliai, ekspansija prie valstybės sienos. Mūsų nuomonės sutapo, jog ekspansija niekam nėra reikalinga – nei Europos Sąjungai, nei Baltarusijai“.

Tokiu būdu, Lukašenkos ir Merkel bendravimas bus tęsiamas. Dar daugiau, jų pokalbio telefonu dalyku tapo konkretus pasiūlymai, kuriuos l.e.p. VFR kanclerė ruošiasi paviešinti kitiems šalių – ES narių lyderiams. Pagal faktą ji pripažino Lukašenkos, kaip žmogaus su kuriuo galima kontaktuoti ir susitarti, statusą.

Jie tai numatė visiškai kitą migracijos krizės „išeitį“: stiprinti sankcinį Baltarusijos spaudimą, statyti tvoras, siekti aviacijos reisų, kuriais naudojasi migrantai, atšaukimo. Bet jokiu būdu nesiderėti su „teroristais“!

Lukašenka gi, to ir laukia.

„Manęs turbūt nestebina, kad Vokietijos kanclerei rūpi situacija prie rytinės Europos Sąjungos sienos. Juo labiau, kad didžioji dalis žmonių, kurie ten yra susikaupę arba tų žmonių, kurie atvyksta į Minską, ketindami nelegaliai kirsti Europos Sąjungos sieną, net neslepia, kad jų galutinis tikslas yra Vokietija, todėl susirūpinimas situacija yra labai suprantamas ir aiškus“, – teigė Lietuvos premjerė ministrė Ingrida Šimonytė stengdamasi išvengti Merkel ir Lukašenkos pokalbio telefonu įvertinimo.

Į klausimą, ar galima kalbėti apie Baltarusijos prezidento legitimaciją, ji nieko neatsakė, tik pridūrė, jog „ nenuostabu, kad šis pokalbis Baltarusijos valdžios propagandistų buvo tiems tikslams ir panaudotas“. Tai yra, Merkel visgi palaikė „priešą“. Dar griežčiau pasisakė Pabaltijo Respublikos Seimo deputatas, parlamento užsienio reikalų komisijos pirmininkas Žygimantas Pavilionis.

„Dar penktadienį kartu su dabartiniu kandidatu į CDU (Krikščionių demokratų sąjungos - RuBaltic.Ru pastaba) lyderiu Norbertu Roettgenu pasirašėme pareiškimą, kur aiškiai įvardijome, kad A. Lukašenka yra nusikaltėlis, kad jis turi būti teisiamas. (…)“.„Dabar renkami įrodymai, siuvami prie bylos ir bus įvardyti kaltieji. Čia yra oficiali Vokietijos pozicija. Labai tikiuosi, kad ji tokia ir liks“, – pareiškė Pavilionis.

Pagaliau, visus taškus ant i sudėjo Lietuvos užsienio reikalų ministras Gabrielius Landsbergis: bendrauti su Lukašenka negalima, kitu atveju jis pajus Vakarų pripažinimą. Lygtai to pripažinimo nebuvimas ji kaip tai kausto...

Tačiau, ne visi oficialaus Vilniaus atstovai neigiamai įvertino Merkel ir Lukašenkos pokalbį telefonu.

„Taip, sankcijos reikalingos, mūsų nuomone, už tuos nusikaltimus žmonėms ir iš viso žmoniškumui. Tačiau, ar tai padeda išspręsti situaciją – ne, tai nepadeda išspręsti situaciją, iki šio laiko nepadėjo išspręsti situaciją, todėl mes turime imtis kitų priemonių, kurios yra mūsų arsenale (...) Bendravimas yra viena iš tokių priemonių, todėl mes ją (Merkel - RuBaltic.Ru pastaba) visiškai nesmerkiame – atvirkščiai, mes matome, jog per Vokietijos ir Prancūzijos lyderius mes galime nusiusti signalą tiems autoritariniams lyderiams, su kuriais mes nebendraujame“, - sako Nausėdos patarėja Asta Skaisgirytė .

Kiek vėliau ir pats Lietuvos prezidentas patvirtino, jog su diktatoriais galima ir reikia bendrauti: „Aš manau, jog yra galimybės išspręsti krizę, kreipiantis į poną Lukašenką, kaip tai tik ką padarė Angela Merkel. Mums reikia pasikalbėti su kažkuo, kas yra atsakingas už tai, kas dedasi prie sienos“.

Žurnalistams reikėjo paklausti Nausėdą: o ar galima su Lukašenka sudaryti kokius tai susitarimus? Sakysim, pasirašyti naują susitarimą apie readmisiją ir atnaujinti bendradarbiavimą per sieną, kuris šias metais buvo nutrauktas. Atrodo, būtent apie tokį variantą Lukašenka pasiūlė Merkel pamastyti.

Viena šalis palaiko susitarimus su Lukašenka, o kita bus kategoriškai prieš. Elektoratiniu atžvilgiu, be abejonių, išloš prezidentas. Lietuvos gyventojai puikiai supranta, jog kaimyninės šalies „demokratizavimas“ (netgi, jei tai gerovės labui) yra atidedamas neterminuotam laikui.

Lukašenka niekur neišeina. Su tuo reikia kaip tai gyventi, o ne neigti objektyvią tikrovę.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 8 — id: `scraped:rubaltic_lt:b9448079fa8c4ecb`

**Title:** Lietuva peržengė visas ribas: pats laikas įvesti sankcijas už rusofobiją

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Rusijos ambasada Lietuvoje pavadino gėda nuosprendį visuomeniniam veikėjui iš Klaipėdos Aleksejui Greičiui, kuris gavo keturis metus kalėjimo, kaltinant šnipinėjimu už tai, jog prižiūrėjo tarybinių karių  kapus ir teikė pagalbą organizuojant „Nemirtingą pulką“ Klaipėdoje. „Greičiaus byla“ netikėtai sukėlė rezonansą Rusijoje, kurios informacinė erdvė paprastai yra abejinga tam, kas vyksta Pabaltijyje. Greičiaus kaltinamo absurdiškumas peržengia visas ribas, o nuosprendis paremtas isteriška neapykanta Rusijai – esant tokiems santykiams Maskvai tik belieka  priimti tokius santykius ir oficialiai pripažinti Lietuvą Rusijai nedraugiška šalimi.

„Gėdingu laikome Lietuvos valdžios veiksmus, skyrus ketverių metų laisvės atėmimo bausmę A. Greičiui, jaunimo asociacijos „Juvenis“ atstovui, akcijos „Nemirtingas pulkas“ organizatoriui Klaipėdoje“, – rašoma paskelbtame Rusijos ambasados Lietuvoje pranešime. - „Naujas Vilniaus politinių represijų prieš savo piliečius etapas nusipelno dėmesio ir atitinkamos atitinkamų tarptautinių organizacijų reakcijos“.

Priminsime, jog tik prieš keletą dienų iki to Rusijos ambasadorius Lietuvoje Aleksejus Isakovas pasisakė apie Maskvos suinteresuotumą gerais santykiais su Vilniumi. Praėjus mažiau nei dviem savaitėm Rusijos atstovų retorika – „gėda“ ir  politinės represijos„.

Temą galima laikyti užbaigta.

Nuosprendis Aleksėjui Greičiui tai visiškai patvirtina. Šios bylos rezonansas peržengė Lietuvos ribas: dėl Greičio šių eilučių autoriui skambino ne tik Rusijos žiniasklaidos atstovai, bet ir trečiųjų šalių žurnalistai, nors, tuo kas vyksta Pabaltijyje, įprastai, niekas nesidomi.

Atvejis su Greičiu tapo išskirtiniu. Nuo nuosprendžio Rusijos karininkui Jurijui Meniui, gavusiam 7 metus kalėjimo (dabar jau 10) pagal straipsnį „karo nusikaltimai ir nusikaltimui žmoniškumui“ už tai,  jog 1991 metų sausio mėnesio 13 naktį tanko žibintais švietė į minią greta Vilniaus televizijos bokšto, laikų Lietuvos kreivasauga neskelbė absurdiškesnių verdiktų.

„Greičiaus byla“ kažkuo tai dar absurdiškesnė nei „Menio byla“. Lietuvos valdžia ne tik vėl pasodino į kalėjimą neabejotinai žinoma nekaltą žmogų, bet dar ir netiesiogiai patvirtino, jog jis yra nekaltas.

Nagrinėjant šios bylos detales belieka tik stebėtis.

Kaltinamo šalis tvirtina sekantį. Rusijos FST Pasienio tarnybos Kaliningrade pareigūnas užverbavo Baltijos jaunimo asociacijos „Juvenis“ direktorių, žinomo Lietuvos rašytojo sūnų Aleksėjų Greičių, kad pastarasis rūpintųsi paminklais tarybiniams kariams Klaipėdos krašte, prižiūrėtu raudonarmiečių kapus ir gegužės 9 d. Klaipėdoje organizuotu „Nemirtingą pulką“. To siekdamas, FST pareigūnas siuntė Greičiui pinigus, o visuomenininkas, atsakydamas kuratoriui siuntė sutvarkytų kapelių, nušienautų vejų ir publikuojamos spaudoje medžiagos apie „Nemirtingą pulką“ fotografijas.

Būtent paminklų ir kapelių fotografijas Lietuvos Temidė pavadino duomenų perdavimu užsienio žvalgybai. Ir Lietuvos teismas patvirtino: bendradarbiavimas su užsienio žvalgyba, netgi jei jis nėra susijęs su valstybės paslapties atskleidimu, vis viena – šnipinėjimas.

Jokia „Kremliaus propaganda“ nesugebės labiau sugriauti Lietuvos, kaip teisinės valstybės įvaizdį, kaip ši baudžiamoji byla. Tokio koncentruoto kliedesio nebuvo netgi „Jurijaus Mielio“ byloje.

Visų pirma, karių kapų priežiūra ir „Nemirtingo pulko“ organizavimu visame pasaulyje užsiima Rusijos diplomatinės atstovybės užsienyje. Tai ypatingai aktualu tokiose šalyse, kaip Lietuva, kur memorialinė veikla – viena iš nedaugelio, kuria gali užsiimti Rusijos diplomatai, būdami izoliuoti buvimo šalyje. FST įsiterpti į šią, susijusią su paminklų priežiūra konsulatų bei ambasadų veiklą, paprasčiausiai yra kvaila.

Antra, pats Lietuvos teismas pažymėjo, jog Greičiaus veikla ne buvo slaptos informacijos rinkimu, valstybės paslapties atskleidimu, šnipinėjimu. Bet nuteisia už šnipinėjimą...

Trečia, rimtose šalyse, tokiais kaltinimais, kaip “šnipinėjimas“ ir „valstybės išdavimas“ be reikalo nesišvaistoma. Tai sunkūs nusikaltimai, už kuriuos, jei jie yra įrodyti, pavyzdžiui, JAV galima kalėti iki gyvos galvos.

Kaip čia neprisiminti kitą „valstybės priešą“ – Algirdą Paleckį, kurį Lietuvos teisėsaugininkai taip pat apkaltino valstybės išdavimu (už tai, jog šis rašė knygą) ir paleido stebėjimui su elektronine apyranke taip, jog dabar Paleckis netgi išstoja mitinguose.

Ketvirta, visuomenininkas iš Klaipėdos iš viso negalėjo perduoti duomenis užsienio žvalgybai, kadangi FST – ne žvalgyba. Rusijoje yra atskira organizacija, užsiimanti žvalgybinę veikla – IŽT, išorinės žvalgybos tarnyba. Bet Lietuva įrodinėja, jog žvalgybine veikla užsiiminėjo būtent FST, bet ne kaip tokia, o Pasienio tarnyba, kuri yra Federalinės saugumo tarnybos sudėtyje.

Tai yra, pasienietis užverbavo Aleksėjų Greičį ir gaudavo iš jo „žvalgybos duomenis“ atrestauruotų tarybinių paminklų fotografijų pavidalu. Laikantis tokios logikos, dešimtys tūkstančių lietuvių, kurie iki pandemijos lankėsi Kaliningrado srityje – užverbuoti šnipai. Gi, visi jie, be jokių išimčių, perdavinėjo FST Pasienio tarnybai informaciją savo pasų duomenų pavidalu.

Patiems Lietuvos piliečiams duodama suprasti, jog Lietuvoje simpatijos Rusijai – tai kriminalinis nusikaltimas. Aleksėjaus Greičio „valstybės išdavimas“ yra tame, kuomi daugelį metų užsiiminėjo visuomeninis veikėjas. Prižiūrėjo tarybinių karių kapus, gynė karo paminklus, rėmė „Nemirtingo pulko“ organizavimą.

Tuo pačiu Baltijos jaunimo asociacijos „Juvenus“ vadovas išdavė Lietuvą, kurį jau daugelį metų švarina biografijas ir heroizuoja nacių kolaboracionistus – Holokausto organizatorius.

Tarp kitko, Holokausto metais Aleksėjau Greičiaus senelis ir senelė  gelbėjo Lietuvos žydus, už ką Izraelis jiems suteikė Pasaulio tautų teisuolių vardus. Visuomenininko tėvas – rašytojas Rimantas Greičius gimė Sibiro tremtyje, bet užaugo dideliu TSRS patriotu. Tai taip pat yra ta priežastis dėl kurios reikia nekęsti tokių žmonių sūnaus ir anūko.

Kas liečia gerus Lietuvos ir Rusijos kaimyninius santykius, tai Greičiaus kazusas šią temą turi užverti visiems, kurie dėl to dar buvo apimti iliuzijų.

Su visomis sankcijomis ir visu kitu, kas priklauso nedraugiškoms šalims už iškeltą į oficialios ideologijos rangą rusofobijos statusą.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 9 — id: `scraped:rubaltic_lt:ea1e9ab50b4cb2b7`

**Title:** Lietuva išsikovojo „energetinę nepriklausomybę“ nuo Rusijos: dujos nueis į Kiniją

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Dujotiekio „Sojuz Vostok“ iš Rusijos į Kiniją statyba bus pradėta 2024 metais. Apie tai praneša „Moncame“ informacijos agentūra, pasiremdama Mongolijos vicepremjeru Sainbujangijn Amarsaichan. Artimiausiu metu turi būti baigtas projekto techninis – ekonominis pagrindimas (TEP). Po to „Gazpromo“ laukia derybos su Kinija dėl garantuotų eksporto apimčių ir tranzito sutarties su Mongolija pasirašymas. Procesas žada būti ilgas ir nepaprastas, bet rezultate Rusija gauna antrąją dujotiekio „Sila Sibiri“ giją, kurios dėka Europos dujų rinka VšAB „Gazpromui“ tampa mažareikšme ir periferine.

Pirmasis magistralinis dujotiekis, kuriuo Kinija gauna „žydrąjį kurą“ iš Rusijos pradėjo veikti visiškai neseniai – 2019 metų gruodyje. Po kelių mėnesių prasidėjo koronaviruso pandemija, dėl karantininių apribojimų pasaulinėje angliavandenių rinkoje buvo stebimas rimtas paklausos ir pasiūlymo disbalansas. Buvo atvejų, kai „Gazpromui“ tekdavo realizuoti savo produkciją žemesne už savikainą kaina (tuo momentu apie pelną iš viso nebuvo kalbama).

Kaip ir buvo laukiama, RF vadovybė tapo „ekspertų“, kurie juokiesi iš jos „neapgalvotos“ energetinės politikos, griežtos kritikos objektu. Nutiesė „Sila Sibiri“, o ji, esą, pasirodė „bejėgė“ ir „beprasmiška“.

Artėjant 2021 metams kalbos apie tai nurimo.

Kinijoje siaučia ne mažesnė nei Europoje energetikos krizė. Šaliai katastrofiškai stinga iškasamo kuro, anglies paros gavyba pasiekė rekordinius rodiklius, dujų tiekimas „Sila Sibiri” gija spalio mėnesio pabaigoje viršijo Rusijos monopolisto kontraktinius įsipareigojimus daugiau nei 19 procentų.

Palyginimui: liepos mėnesį Turkmėnistanas pardavė Padangių šaliai dujas po 238 dolerius, Kazachstanas – 195 dolerius, Uzbekistanas – 193 dolerius.

Nenuostabu, jog šiame fone Mongolijos vicepremjeras Sainbujangijn Amarsaichan pareiškia apie dujotiekio „Sojuz Voistok“ perspektyvas.

Jo žodžiai tariant, iki metų galo turi būti paruoštas projekto techninis – ekonominis pagrindimas. Po to Rusijos ir Mongolijos vyriausybės sudarys tarifų reguliavimo susitarimą ir pradės parengiamuosius darbus.

Šio projekto darbai buvo pradėti dar 2019 metų pabaigoje, kai Ulan-Batoras ir „Gazpromas“ pasirašė savitarpio pagalbos memorandumą. Po to Mongolija įregistravo specialios paskirties kompaniją „Dujotiekis Sojuz Vostok“ ir įkūrė bendrą su Rusija darbo grupę. Jos darbo vaisiumi turi tapti konkretus naujo vamzdžio statybos projektas.

„Eksportinis dujotiekio „Sila Sibiri – 2“ galingumas gali viršyti daugiau nei 1,3 karto dujotiekio „Sila Sibiri“ galingumą. Tai sudarys galimybę tiekti dujas iš Vakarų Sibiro eksportui didesnėmis apimtimis ne tik vakarų, bet ir rytų kryptimi“,- praneša VšAB „Gazprom“ informacijos valdyba.

Idėja sukurti papildomą dujų transportavimo infrastruktūrą, skirtą eksportui į Kiniją kompanijoje gimė dar iki „Sila Sibiri“ eksploatavimo pradžios.

RuBaltic.Ru analitinis portalas dar 2018 metais rašė, jog Rusija ne atmeta magistralių „Sila Sibiri – 2“ („Altai“) ir „Sila Sibiri – 3“ statybos. Užduotį – maksimum pagarsino „Gazpromo“ vadovas Aleksejus Milleris: eksporto apimtis į Kiniją padidinti iki 110 milijardo kubinių metrų dujų per metus.

Jei viskas eis kaip numatyta, pirmoji „Sila Sibiri“ gija 2024 metais pasieks projektinį galingumą (38 milijardai kubų). Tada prasidės naujo vamzdyno statyba, kuris Mongolijai sudarys galimybę tapti ne tik rusiškų dujų tranzito šalimi, bet imti jas savo poreikiams, dėl ko sumažės šalies priklausomybė nuo anglies.

Šiame kelyje Rusiją laukia nemaža kliūčių. Jai dar teks išspręsti pagrindinį uždavinį – tiesiogiai su Pekinu sudaryti ilgalaikį dujų tiekimo kontraktą.

„Sila Sibiri-2“ statyba neprasidės iki tol, kol „Gazpromas negaus tvirtų savo kinų partnerių garantijų. Ir Mongolija gaus tvirtas garantijas tik tada, kai Rusija susitars su KLR.

Šios derybos nežada būti paprastomis, kadangi Padangių šalis nesiekia staigaus energijos resursų importo apimčių augimo. Žymias dujų apimtis į išgauna savarankiškai. Be to, kinai, kaip ir europiečiai, siekia angliavandeninio neutralumo. Paprasčiausiai jų planai ne taip išreklamuoti, kaip plačiai nuskambėjęs ES „žaliasis“ sandoris.

„Kinijoje vyksta globalinis ekonomikos persitvarkymas pagal be angliavandeninius parametrus. Apie tai kalba ir rodo ir „sovietų/rusų propaganda“, ir tarptautiniuose forumuose pats Pekinas tai ambicingai pareiškia. Tai dar ta paslaptis“, - rašė Rusijos URM sekretorius spaudai Marija Zacharova.

Šalies vadovybei tikriausiai gana bus išminties tai suprasti ir prieiti prie išvados, jog angliavandenių epocha artimiausiais 10-15 metų nepasibaigs. Antrosios „Sila Sibiri“ gijos atsipirkimui bus pakankamai laiko.

Tarp kitko, atviru lieka klausimas, ar pavyks Rusijai pritraukti kinų kapitalą finansuoti naujo vamzdžio statybą. Tuo suinteresuotas „Gazpromas“, o Pekino pozicija kol kas nėra aiški. Bet tai tik vienas iš techninių momentų, kuriuos, turint noro, galima išspręsti. Svarbiausiai – politinė Rusijos ir Kinijos vadovybių valia.

Būtent jos sudarė maksimaliai nekomfortines „Gazpromo“ veiklai vakarų kryptimi sąlygas: palaikė Trečiojo energetikos paketo normas, sabotavo „Šiaurinio srauto – 2“ statybą, inicijavo begalinius nagrinėjimus Stokholmo arbitraže ir pan.

Prisidengdami kova už „energetinę nepriklausomybę“ nuo RF, vikrūs europiečiai pas save kūrė „vartotojų rinką“. Jie tikėjosi, jog „Gazpromui“ prisieis dėl jų konkuruoti su suskystintų gamtinių dujų tiekėjais ir „žaliosios“ energijos gamintojais.

Todėl, kad nuo Europos jis priklauso ne mažiau, kaip Europa nuo jo.

Rusiškų dujų tiekimo į Kiniją padidinimas ne būtinai turi tapti tiekimo į ES šalis sumažinimo padariniu. Idealiu atveju „Gazpromas“ gali padidinti bendras eksporto apimtis naujų telkinių įsisavinimo sąskaita.

„Šiaurinis srautas – 2“ Europai taps paskutiniu rusišku eksporto dujotiekiu. Nauji jai daugiau nereikalingi.

Na o „Gazpromui“ jie tuo labiau nereikalingi. Jis atsiveria Kinijai.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 10 — id: `scraped:rubaltic_lt:10be3a722ca1403f`

**Title:** Taivanas kursto Lietuvą nutraukti diplomatinius santykius su Kinija

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Taivano prezidentė Cai Inven numato aplankyti „drąsiąją Lietuvą“ pasibaigus koronaviruso pandemijai. Apie tai, remdamasi valstybės vadovo pasisakymu, praneša Kinijos Respublikos, kurią KLR skaito savo provincija, Valstybinis radijas. Tokiu būdu, Taivano lyderės dėka Vilnius pateko į gana keblią padėtį: jei šis vizitas įvyks, Pekinas spręs klausimą dėl diplomatinių santykių nutraukimo su Lietuva. Priešingu atveju, niekas nemaišys Cai Inven dažnai svečiuotis Europos Sąjungoje.

Kaip žinoma, šiandieną Taivanas tapo dviejų politinių jėgų – konservacingo Gomindano, kuris linkęs integruotis su Kinija, ir, Pekinui nedraugiškos Demokratinės progreso partijos kovos lauku. Cai Inven atstovauja pastarajai.

Praeitais metais perrinkta į prezidentės postą, ji pareiškė: „Mums nepriimtinas principas „viena šalis – dvi sistemos“, kurį mums perša žemyninės Kinijos vadovybė, siekdama pažeminti Taivano statusą ir pakirsti status - quo Taivano sąsiauryje. Mes tvirtai laikomės šios pozicijos“.

Taivano diplomatine pergale galima skaityti naujieną apie greitą jo atstovybės atidarymą Vilniuje (kartu su tuo, pavadinime bus panaudotas būtent žodis „Taivanas“, o ne „Teibei“, kaip tai yra priimta tarptautinėje praktikoje).

Pabaltijo respublika taip įkvėpė ponią Inven, jog ji panorėjo pati asmeniškai išreikšti padėką savo naujiems draugams.

„Prezidentė Cai Iven sako, jog pasibaigus pandemijai nori aplankyti Lietuvą, kadangi tai drąsi šalis. Apie tai pasakė antradienį, transliuojant tinklalaidę. Ji pasakė, jog toks vizitas gali įvykti, jei tai netrukdys pandemija bei bus palankios diplomatinės sąlygos“ – lapkričio mėnesio 9 d. pranešė Taivano valstybinis radijas.

Ar Cai Inven gavo preliminarų Lietuvos valdžios sutikimą tokios kelionės organizavimui? Apie tai istorija nutyli.

Iš vienos pusės, Pabaltijo respublika įsitvirtino pačios antikinietiškiausios ir pačios protaivanietiškos šalies kontinente statuse. Valdantieji konservatoriai, kartu su prezidentu Nausėda kuria būtent tokį jos įvaizdį. Bet jei jų galvose yra bent vienas vingis, jie turi suprasti kokios bus pirmojo oficialaus Cai Inven vizito į ES pasekmės.

Už ketinimą atidaryti Taivano biurą Lietuva jau neteko kinų ambasadoriaus, nors panašūs biurai jau seniai veikia daugelyje vakarų šalių. Šiame kontekste reikia pripažinti, jog Vilnius nepadarė nieko principingai naujo.

Cai Inven pakvietimas – tai visiškai kitas reikalas.

Ir tai logiška, kadangi su visomis išlygomis Europos Sąjunga visgi pripažįsta Kinijos teritorinį vientisumą. Amerika, tarp kitko, taip pat. Jungtinėse Valstijose ponia Inven buvo, bet ne su oficialiu vizitu, o pravažiuojant, pakelyje iš Paragvajaus ir Belizo - tai vienos iš nedaugelio šalių, su kuriomis Taivanas palaiko diplomatinius santykius.

Be to, amerikiečiai – tai ypatingas atvejis. Dėl JAV geopolitinės ir ekonominės galios, joms leidžiama daryti daug ką iš to, kas yra draudžiama likusiems. Ilgame „likusiųjų“ sąraše randasi ir Baltijos šalys.

Tik įsivaizduokime, į Lietuvą (būtent „nepriklausomo“ Taivano lyderio statuse) tikslingai atvyksta Cai Inven. Čia ji priimama aukščiausiame lygyje – negi galima kitaip? Ji susitinka su pagrindiniais vyriausybiniais valdininkais. Galima tikėti, netgi su šalies prezidentu Gitanu Nausėda.

Privalo gi, valstybės vadovas savo pavyzdžiu parodyti, kaip reikia paremti mylintį laisvę Taivaną, apie kurį tiek daug kalba Lietuvos valdžia!

Tarp kitko, šiuo instrumentų kinai jau naudojosi. Štai, 2007 metų naujiena: „šeštadienį KLR ambasadorius Sent Liusijoje Gu Hyamin šios Karibų valstybės vyriausybei perdavė kategoriška protestą dėl sprendimo užmegzti „diplomatinius santykius“ su Taivanu. KLR vyriausybės vardu Gu Hyamin painformavo apie sprendimą sustabdyti šalių diplomatinius santykius bei nutraukti visų abipusių tarpvalstybinių susitarimų vykdymą“.

Sent Liusija – mažytė salų valstybėlė, kurio gyvena 200 tūkstančių gyventojų. Lyginant su ja, Lietuva rodosi politiniu „sunkiasvoriu“. Bet būtent dėl to jai ir gali „atskristi“ iš Padangių šalies. Į patį Pabaltijį kinams nusispjaut nuo aukšto Taišano kalno. Jiems svarbu tai, jog Taivano lyderė, galimai, bus priimama Europos Sąjungos teritorijoje.

Kinija gali tai „praryti“, ir po kurio laiko pasirodys, jog Cai Inven keliauja po visą Europą: štai, ją priima Prancūzijos prezidentas, o rytoj ji svečiuojasi pas Vokietijos kanclerį (pasakoja apie nenumaldomą Taivano siekį nepriklausomybės). O kodėl gi ne? Kas kliudo likusioms ES šalims pasekti Lietuvos pavyzdžiu, jei vienintelė Kinijos reakcija dėl Inven kelionės į Europą – tai protesto notos?

Lietuva jau pakankamai padarė diplomatinių santykiu su KLR nutraukimo labui.

Pirmasis Caj Inven vizitas į Europą taptų žymia užsienio politikos pergale ir papildomu nepriklausomybės siekimo argumentu. Galimai, ji, siekdama savo interesų, sąmoningai išnaudoja Lietuvą.

Taivanas Inven kelionę pateiks kaip „dovaną“ drąsiai Pabaltijo respublikai. Bet iš tikrųjų ši „dovana“ reikalinga pačiam Taivanui, o Lietuvai ji nežada nieko gero.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 11 — id: `scraped:rubaltic_lt:f6d654b8bfd573bf`

**Title:** Prekių blokada: Kinija išmokys Rusiją griežtai reaguoti į Lietuvos priešiškumą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvoje išsigando likti be kinų prekių dėl politinio konflikto su Pekinu. Lietuvos verslininkai perspėja, jog daugelio importo iš Kinijos pozicijų nėra kuo pakeisti, ir šalyje atsiras rimtas prekių deficitas, jei Padangių šalis blokuos prekybą su Lietuvą. Dėl pagrindinio Lietuvos užsienio ekonomikos partnerio – Rusijos – iki šiol nebuvo baiminamasi, jog vieną kartą Maskva, atsakydama Vilniaus priešišką politiką, blokuos importą Lietuvai. Tai netiesiogiai patvirtina, jog Rusija Vilniaus atžvilgiu elgęsi pernelyg švelniai.

O pastarajai tokia perspektyva – tiesioginė grėsmė nacionaliniam saugumui. Kadangi pakeisti eilę pagrindinių importo pozicijų iš Kinijos (visų pirma – technologijose) nėra kuo.

Tuo tarpu, konfliktas jau gylėja. Praeitą savaitę Lietuvos prezidentas Gitanas Nausėda gavo aukščiausiojo palaiminimą tęsti prieš Kiniją nukreiptą politiką asmeniškai nuo Jungtinių Amerikos Valstijų prezidento.

Lietuvos vadovybė vis tai pat nusiteikusi išsitarnauti amerikiečių akyse. Ne veltui viršūnių susitikime dėl klimato Glazgo Nausėda išnaudojo jam suteiktų keletą minučių  pokalbiui su Džo Baidenu  ne Rusijos, bet Kinijos aptarimui. Supranta, kas šiuo metu visų pirma domina dievybę iš už vandenyno.

Aukščiausiojo indulgencija tęsti kovą su KLR Vilnius iš karto buvo panaudota tam, kad į tą kovą įjungti kitas Pabaltijo šalis. Trečiadienį Nausėda bendravo su Baidenu, o penktadienį Lietuvos URM jau paragino Latviją ir Estiją suformuoti bendrą santykių su Kiniją strategiją.

Vargu ar Rygą ir Taliną įkvėps panašia idėja, kadangi prieš Kiniją nukreiptos politikos kaina Lietuvai auga su kiekvienu antikiniškos politikos žingsniu.

Ir Lietuvos politikai, būdami paikais ir neadekvačiais, supranta grėsmių mastą ir todėl gerai matosi jų baimė žengiant antikinišku kursu. Prezidentas Gitanas Nausėda paragino Pekiną Vilniaus sprendimus dėl santykių su Taivanu plėtros vertinti „ne taip jau jautriai“, o Lietuvos URM išreiškia nedrąsią mintį, jog KLR ambasadorius vis tik sugrįš į Lietuvą.

Kinija Lietuvos politikus gąsdina ne tuo, jog ji didelė ir galinga, o tuo, jog ji tokia didelė ir galinga, priešiškus Lietuvos veiksmus nevertina atlaidžiai. Lietuvos politikai, dešimtmečiais lodami Rusijos adresu, jau įprato būtent prie tokio vertinimo. Dramblys ignoruoja šunelį.

Kas ten ta Lietuva? Daugiausiai, iš to ką ji gali sugebėti su savo rusofobija – tai iš bejėgiškumo bei pykčio daužydama į sieną prasiskelti sau kaktą. Tai, kad Vilniuje tegul loja ir toliau. Įprotis nekreipti dėmesio į tą lojimą Rusijoje jau taip įsišaknijo, jog ten jau jo iš tikrųjų nebegirdi.

Kinija į nedraugišką elgesį reaguoja principingai kitaip. Pekine manoma, jog kiekvienas veiksmas turi iššaukti atoveiksmį. Todėl atsakas antikiniškom Europarlamento  Lietuvos  deputatų rezoliucijoms, pareiškimams apie „uigūrų genocidą“ ir Taivano atstovybės atidarymui Vilniuje – kinų ambasadoriaus atšaukimas, kinų investicijų Lietuvoje stabdymas, o dabar dar ir prekių blokados perspektyva.

Dabartinį baiminimąsi, jog Pekinas paprasčiausiai gali palikti Lietuvą be kinų importo, tai pat netiesiogiai patvirtina Maskvos politikos švelnumas. Todėl jog Rusija – pagrindinis Lietuvos užsienio ekonomikos partneris, tačiau iki šiol nebuvo kalbų apie tai, jog vieną kartą Maskva, atsakydama į peržengianti bet kokias ribas priešiškumą, paprasčiausiai, nutrauks prekybinį-ekonominį bendradarbiavimą,

Daugiausiai buvo baiminimąsi dėl elektros energijos tiekimo, bet rusiškas importas į Lietuvą – tai, toli gražu, ne tik dujos ir elektros energija. Rusija tiekia Lietuvai naftos chemijos produkciją, maisto produktus, medieną, transporto priemones, mechaninę įrangą.

Vilniuje išsigando netekti kinų importo už  1,2 milijardo eurų, o Lietuvos ir Rusijos užsienio prekybos apyvarta sudaro 9 milijardus eurų. Rusija – tai ketvirtadalis Lietuvos užsienio prekybos, tuo pačiu metu kai Rusijos užsienio ekonomikos ryšių struktūroje Lietuvos Respublikos dalis – 0,4 procento.

Tai yra, Rusija nėra priklausoma nuo Lietuvos, ir niekas nemaišo Maskvai elgtis „kinietiškai“.

Vieninteliu, kas anksčiau sulaikydavo Maskvą nuo tokio scenarijaus, buvo Kaliningrado sritis, bet čia kaip tik Lietuva, savo neadekvačia ir antirusiška politika padarė viską kas nuo jos priklauso, kad ši kliūtis būtų panaikinta.  Kad rusiškas eksklavas taptų nepriklausomu nuo išprotėjusios Rusijos kaimynės, Rusija ilgą laiką kūrė strateginę Kaliningrado srities autonomiją ir pasiekė, jog dabartiniu metu ji yra visais atžvilgiais apsaugota nuo Lietuvos.

Autonominis energijos tiekimas, maisto saugumas, susisiekimas oru ir jūra per neutralius Baltijos jūros vandenis su pagrindine šalies teritoriją –neliko nei vienos sferos, kur Lietuva galėtu ne tik sugadinti toliausiai į vakarus nutolusiam Rusijos regionui gyvenimą, bet ir sudaryti kritinę grėsmę jo gyvavimui.

Akivaizdžiu pavyzdžiu, kokia gali būti nauja Rusijos politika, šiandiena yra Kinija.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 12 — id: `scraped:rubaltic_lt:a7438a904ed29d04`

**Title:** Lietuvoje pradėjo kalbėti apie prezidento apkaltą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos prezidentas Gitanas Nausėda tapo pagrindiniu valdančiųjų konservatorių bei jų sąjungininkų  kritikos objektu. Ministrė pirmininkė Ingrida Šimonytė atvirai jį kaltina vakcinacijos sabotažu, euro deputatas Andrius Kubilius pareiškia, jog valstybės vadovo reitingai tampa „grėsme nacionaliniam saugumui“, o buvęs Seimo pirmininkas Arūnas Valinskas iš viso kalba apie „prezidentūros paksėjimą“. Tai užuomina į tau, jog Nausėda gali laukti „prorusiško  prezidento“ Rolando Pakso likimas, kuriam 2004 metais buvo pareikšta apkalta.

RuBaltic.Ru analitikos portalas jau rašė, jog Lietuvos parlamento tarptautinių reikalų komisijos pirmininkas Žygimantas Pavilionis nori apskųsti prezidentą Valstybės saugumo departamentui (VSD). Dėl absoliučiai išgalvotos ir visiškai nereikšmingos priežasties: esą, Nausėda pažeidė įstatymą, iš anksto pagarsindamas respublikos ambasadoriaus Europos Sąjungoje kandidatūrą.

Jau tada mes spėjome, jog reali šio „užvažiavimo“ priežastis slepiasi neseniai atliktos socialinės apklausos rezultatuose, remiantis kuriais, prezidentas lieka pačiu populiariausiu Lietuvos politiku, o vyriausybės narių reitingai, atvirkščiai, nenumaldomai krenta.

Kaip išaiškėjo, konservatoriai iš tikrųjų susipažino su šiuo tyrimu.  Ir tai jiems sukėlė didelį nerimą. Štai ką paskutiniu metu pareiškė „Tėvynės Sąjungos – Lietuvos Krikščionių Demokratų“ (TS-LKD) partijos „veteranas“, buvęs ministras pirmininkas Andrius Kubilius: „Prezidento reitingai (jų smukimas) tampa grėsme šalies nacionaliniam saugumui. Gal reikia arba jų nebematuoti, arba nebeskelbti, bent jau kol pandemija nebus įveikta“.

Apie kokį smukimą kalbama? Kubilius remiasi kažkokia tai apklausa, kur „Nausėdą aplenkė Vilija Blinkevičiūtė“.

Tokiu būdu jis, būk tai, stengiasi užsitikrinti „antivakserių“ simpatijas.

„Taivane būtų keliamas klausimas apie pastangas sąmoningai kenkti Vyriausybės kovai su pandemija. Su Mario Draghi (Italijos premjeras-ministras - RuBaltic.Ru) pastaba Gitano Nausėdos nėra net kaip lyginti. Ir viskas tik todėl, kad paskutinėse apklausose Vilija Blinkevičiūtė aplenkė G. Nausėdą? Tik dėl to tokia panika ir noras susigrąžinti antivakserių balsus?“ – klausimą kėlė A. Kubilius. Jis, žinoma, gudrauja: jei ir buvo kokia tai apklausa, remiantis kuria parlamento spikeris Blinkevičiūtė aplenkia Nausėdą (nors mums apie tokią apklausą mes nieko negirdėjome), tai paskutiniai duomenys liudija atvirkščiai.

Taip pat griežtai pasisako ir premjerė ministrė Ingrida Šimonytė. Spalio pabaigoje Nausėda jai priekaištavo dėl „dirbtinai sulėtėjusių vakcinacijos tempų“.

„Mes praktiškai pražiopsojome, pramiegojome pirmą vasaros pusę, kai, nežinau dėl kokių sumetimų, buvo dirbtinai sulėtinti skiepijimosi tempai. Galbūt dėl to, kad nebūtų pasiektas prezidento tikslas 70 proc. iki liepos vidurio. O po to, kai jau buvo pamatyta, kad susikaupė didelės vakcinos atsargos ir kad gali būti kritika iš visuomenės pusės, tada buvo verčiamasi per galvą“, – sakė prezidentas.

Savo ruožtu Šimonytė nusprendė replikuoti mokamų COVID-19 testų vetavimą:

„Atrodo, kad prezidentūra nusprendė sąmoningai stabdyti skiepijimo progresą tam, kad nebūtų pasiektas ambicingas prezidento tikslas, tikriausia toks gali būti mano komentaras“.

Dar vienas įdomus faktas: Lietuvos premjerė ministrė pareiškė, jog jie su Nausėda nesusitinka ir nieko neaptarinėja. Tikriausiai tai jų asmeninio varžymosi už teisę atstovauti šalį tarptautinėje arenoje atbalsiai.

Neseniai tokius pat kaltinimus pagarsino buvęs šalies parlamento pirmininkas Arūnas Valinskas. Jis ne TS-LKD narys, bet jo Tautos prisikėlimo partija sudarė koaliciją su konservatoriais, o jis pats vadovavo Seimui tuo metu, kai jau minėtas Kubilius užėmė ministro-pirmininko pareigas.

Ne per seniausiai interviu Valinskas tiesiog „sudraskė“ Nausėdą dėl jo neatitikimo užimamoms pareigoms. Pavyzdžiui, štai taip jis komentavo prezidento patarėjo pasisakymą dėl to jog žmonės nėra kalti už tai, kad jie nepaskiepyti: „Tai čia aiškiai rodoma pirštu į ministrą Arūną Dulkį, premjerę Ingridą Šimonytę, kad jie yra kalti. Šioje vietoje man atrodo, kad yra peržengtos visos politinės elgsenos ir pagarbos vienos institucijos kitai ribos. Galiu pasakyti tik tiek, kad prezidentas kaip buvo savo laiku banko tarnautojėlis, taip ir liko. Tik anksčiau skaičiuodavo pinigus, o dabar – savo reitingo taškus“. Valinsko pasisakyme taip sunku nepastebėti užuominos.

O štai, tikriausiai, pats garsiausias buvusio Lietuvos Seimo pirmininko pareiškimas: „Vyksta Prezidentūros paksėjimo procesas. Ir tai yra akivaizdu. Žmonės tiesiog sukąs dantis ir tiesiog pralauks tuos trejus metus. Dvejus pralaukė, pralauks ir trejus. Ir šioje situacijoje mano žodžiai buvo pragaištingai pranašingi – tokioje situacijoje geriau jokio prezidento nei toks“.

Kas per „paksėjimas“? Akivaizdu, tai autorinis pono Valinsko neologizmas.

Sunku sugalvoti gėdingesnį valstybės vadovo kaltinimą. Be to nesuprantama, ar ne peraugs šie kaltinimai į grasinimus. Jei Nausėda virsta „naujuoju Paksu“, tai ar ne reikia jo sustabdyti?

Kol kas nėra ko rimtai kalbėti apie veikiančio Lietuvos prezidento apkaltos perspektyvą. Iš kitos pusės, jo ir valdančios partijos santykiai tampa vis labiau įtempti, o Lietuva stovi ant rimtų išbandymų slenksčio.

Kol kas galima pasakyti tik vieną: Nausėdos reitingai tikrai užgauna  konservatorius. To jie ir patys neslepia.

Kaip nekeista, bet ir TS-LKD papuolė į tuos pačius žabangus kaip ir Lietuvos Valstiečių ir žaliųjų Sąjunga (LVŽS). Ši partija po 2016 metų parlamento rinkimų  tapo koalicijos „branduoliu“, o vėliau prarado savo reitingus ir perdavė savo lyderystę konservatoriams, o prieš tai buvusiose prezidento rinkimuose jos kandidatas – tuometinis ministras-pirmininkas Saulius Skvernelis – nesugebėjo netgi praeiti į antrąjį rinkimų turą.

Ir prezidento Nausėdos priešininkai su tuo nieko negali padaryti.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 13 — id: `scraped:rubaltic_lt:e90442f650d24361`

**Title:** Rupūžė puolė gyvatę: valdančioji Lietuvos partija grasina nuteisti prezidentą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos prezidentą Gitaną Nausėdą gali apskųsti Valstybės saugumo departamentui (VSD) dėl „farso“ su respublikos ambasadoriaus paskyrimo prie Europos Sąjungos. Tai pareiškė Seimo deputatas Žygimantas Pavilionis. Pažymėtina, jog keletą dienų prieš tai sociologija paskelbė Nausėdą pačiu populiariausiu Lietuvos politiku, o jo tikimiausias konkurentas sekančiuose prezidento rinkimuose – konservatorių lyderis ir užsienio reikalų ministras Gabrielius Landsbergis – tapo vienu iš reitingo autsaiderių.

Žygimanto Pavilionio nepasitenkinimo priežastimi tapo, būk tai, naujojo Lietuvos ambasadoriaus prie ES patvirtinimo procedūros pažeidimai. Deputatas remiasi diplomatinės tarnybos įstatymo nuorodomis: „Iš anksto kandidatūrą apsvarsčius Seimo Užsienio reikalų komitete, Lietuvos Respublikos diplomatinį atstovą užsienio valstybėje, tai užsienio valstybei sutikus jį priimti, Vyriausybės teikimu skiria Respublikos Prezidentas dekretu, kurį taip pat pasirašo ministras pirmininkas“.

Pavilionio nuomone, atvejyje su Raimundu Karoblis, kurį Nausėda ruošiasi siųsti į Briuselį, viskas buvo padaryta atvirkščiai: pradžioje prezidentas demonstratyviai išsirinko šią kandidatūrą, o po to pasiūlė „pradėti būtinas paskyrimo procedūras“.

„Jeigu, kaip per savo patarėjus nurodo Prezidentas, bus pradėtos jau viešai įvardyto R.Karoblio skyrimo ambasadoriumi ES reikalingos procedūros, aš, kaip Seimo Užsienio reikalų komiteto pirmininkas, neturėsiu kito pasirinkimo, kaip kreiptis į VSD pradėti tyrimą dėl tarnybinės paslapties paviešinimo pažeidimo. Todėl aš labai tikiuosi, jog ateityje visi ambasadorių skyrimo procedūros dalyviai laikysis diplomatinio įstatymo nuostatų, ir aukščiausiųjų diplomatinių atstovų skyrimas ne bus viešas. (...) Aš taip pat siūlau, kad viešai skiriami ambasadoriai nedalyvautų tame viešai politizuotame aukščiausiųjų diplomatinių atstovų skyrimo farse, kuris yra atliekamas pažeidžiant įstatymą“,- pareiškė Pavilionis.

Jis ir anksčiau neslėpė savo skepticizmo Nausėdos atžvilgiu, bet grasinimas nuteisti veikiantį valstybės vadovą – tai jau per daug akiplėšiškas žingsnis. Atskiras Seimo deputatas vargu ar sugebėtu prisiimti sau tokią atsakomybę, negavęs partijos vadovybės pritarimo.

Prezidento ir „landsbergistų“, kurie laimėjo praėjusių metų rinkimus į parlamentą, konflikto jau niekas nenori slėpti (nebent gali būti slepiami tos konfrontacijos mastai). Bet kokius konservatorių išpuolius Nausėdos adresu galima vertinti, kaip bandymą pakelti lošimui pastatytą sumą. Bet Pavilionio panikavimas visgi atrodo nelogišku, netgi absurdišku.

Gal būt, konservatoriai, paprasčiausiai, nori „prastumti“ į ambasadoriaus prie ES pareigas savo žmogų? Anaiptol.

Visų pirma, tai ne toks jau ir svarbus paskyrimas, kad dėl jo provokuoti politinę krizę. Antra, alternatyvių kandidatų niekas nesiūlo.

Trečia, Raimundo Karoblio figūra visiškai priimtina TS-LKD. Taip, jis dirbo prieš tai buvusioje Sauliaus Skvernelio vyriausybėje (užėmė Gynybos ministro postą), bet tada buvę opozicijoje konservatoriai jį gerbė.

Kai 2019 metais Seime buvo svarstomas naujas koalicinis susitarimas, Gabrielius Landsbergis įtarė, jog „visas tas stumdymasis alkūnėmis pasibaigs tikrai gerai dirbančių ministrų pakeitimu“. Bijau, jog Roką Masiulį arba Raimundą Karoblį pakeis, ir bus pasakyta, jog tai nauja kokybiška vyriausybė, nors iš tikrųjų tai du ministrai, kurie gali netikti Ramūnui Karbauskui arba valdančiai daugumai“, - spėjo Landsbergis.Tuometinis gynybos ministras netgi nesiteisino: esą, jis nėra tokia svarbi figūra, kad dėl jo „reformuoti“ koaliciją...

Dar vienas parodomasis faktas: 2020 metų kovo mėnesį Landsbergis siūlė atstatydinti Sveikatos apsaugos ministrą Aurelijų Verygą, ir į jo pareigas paskirti Karoblį. Tada tai, tikriausiai, buvo pareigos Nr. 1 – šalyje prasidėjo koronaviruso epidemija.

Pagaliau, tas pats Landsbergis, sveikino Nausėdos žodžius apie tai, jog jis pasiruošęs patvirtinti Karoblio kandidatūrą (anksčiau prezidentas abejojo dėl tokio pasirinkimo teisingumo). „Nežiūrint į tai, jog tokių klausimų suderinimo ne per žiniasklaidą praktika yra įprasta, aš buvau maloniai nustebintas, kad prezidentas persigalvojo, ir aš tuo džiaugiuosi“, - kalbėjo Lietuvos užsienio reikalų ministras.

Tik praėjus kelioms dienoms jo partijos bendražygiai pradėjo skambinti visais varpais ir prigrasino apskųsti Nausėdą!

Šioje situacijoje prezidentą galima suprasti: jis žinojo, jog Karoblio paskyrimas faktiškai jau suderintas. Buvusio gynybos ministro kandidatūrą nagrinėjo dar šių metų pradžioje, ir, būtent Nausėda buvo prieš. Karobliui ir URM eks-vadovui Linui Linkevičiui jis siūlė „atvėsti“ prieš užimant naujus atsakingus postus

Prezidento veiksmai, mažų mažiausiai yra logiški. O kokia logika vadovaujasi Pavilionis, kai tiesiog lygioje vietoje „kabinasi“ prie Nausėdos? Per daug menka priežastis skelbti valstybės vadovo apkaltą. Smūgiuoti į jo reitingą – taip pat. Lietuvos rinkėjai iš Pavilionio pretenzijų paprasčiausiai pasijuoks.

Bendrai, mes nespėliosime iš kavos tirščių. Viso paveikslo mes nematome.

Vilmorus socialinės apklausos rezultatai rodo, jog Nausėda pasilieka pačiu populiariausiu Lietuvos politiku – teigiamai jį vertina 52,8 procento respondentų. O Landsbergis šiame reitinge atsidūrė antroje vietoje iš galo. Blogiau lietuviai vertina tik ekonomikos ir inovacijų ministrę Aušrinę Armonaitę.

RuBaltic.Ru analitikos portalas jau rašė, jog yra didelė tikimybė, kad sekančiuose prezidento rinkimuose, būtent Landsbergis bus TS-LKD kandidatu.

Tikriausiai dėl to Landsbergis netapo Seimo pirmininku arba ministru pirmininku. Pirmosios pareigos per daug rutiningos ir nepastebimos, antrosios – per daug pavojingos (vyriausybės vadovas tradiciškai yra asmeniškai atsakingas už socialinę – politinę padėtį šalyje).

Už tai Lietuvos URM vadovo poste galima per daug nesistengti, nei už nieką neatsakyti ir visada būti dėmesio centre. Idealus naujo „tautos tėvo“ „populiarizavimo“ variantas.

Bet praktikoje ši idėja neveikia.

Pas ją 46,9 procento negatyvių įvertinimų, pas Landsbergį – 57,2 procentai. Pastarajam antrame rinkimų ture su veikiančiu prezidentu nieko nešviečia, neskaitant gėdingo (netgi žeminančio) pralaimėjimo.

TS-LDK – sektantiško tipo partija. Ją sudaro nedidelis atsidavusių fanatikų branduolys (10-15 procentų). To pakanka tam, kad visada papulti į parlamentą ir periodiškai į valdžią. Nors Lietuvos gyventojų dauguma niekada nebalsuos už konservatorius.

Patys „landsbergistai“ tai tikriausiai supranta, bet nieko negali padaryti.

Jų padėtyje galima tik „užpuolinėti“ prezidentą, dėl prigalvotų dingsčių skųstis prezidentu ir tuo pačiu demonstruoti savo bejėgiškumą.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 14 — id: `scraped:rubaltic_lt:9740d0f4abcaa83c`

**Title:** Lietuva apvils Europą: Vilniuje apgalvojamas Taivanio pripažinimas

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Jungtinės Valstijos yra pasiruošusios suteikti Lietuvai visokeriopą paramą jos diplomatiniame pasipriešinime Kinijai. Apie tai, po neformalaus susitikimo Glazgo su Baidenu, pareiškė Pabaltijo respublikos prezidentas Gitanas Nausėda. Gavęs savo globėjų iš už vandenyno komandą „fas“, Vilnius, tikriausiai, tęs agresyvią, nukreiptą prieš Kinija, politiką ir stengsis į ją įtraukti likusią Europą. Yra tikimybė, jog Lietuva taps pirmąją ES šalimi, kuri pripažins Taivano nepriklausomybę.

Klimato pokyčiams skirtos JTO konferencijos Glazgo (COP26) metu Gitanui Nausėdai nusišypsojo laimė neformaliai pabendrauti su Baltųjų Rūmų šeimininku. Pilnavertėmis derybomis tai sunku pavadinti – pas Lietuvos lyderį nebuvo laiko aptarti su Baidenu visas jį, jaudinančias temas. Jis pasirinko pačią aktualiausią: Kinija.

„Tikrai mums šiandien yra reikalinga ir moralinė, ir kitokia parama iš mūsų bendraminčių, - kalbėjo G. Nausėda - tai Amerikos prezidentas patvirtino, kad jis seka šią temą ir Jungtinių Amerikos Valstijų pasirengimas padėti mums visais būdais yra garantuotas“.

Kokią paramą, neskaitant moralinės, Vašingtonas pasiruošęs teikti Lietuvai? Apie tai nutylima. Bet čia svarbi pati nuoroda.

Ji pati vykdo veiksmus, kurie nepatinka Kinijai, ir pati patraukia prie to vakarų sąjungininkų dėmesį.

Atkreipsime dėmesį į dar viena Nausėdos pareiškimą: „Lietuva nesiekia provokuoti konflikto lygioje vietoje. Lietuvos tikslas yra iš esmės įgyvendinti suverenios valstybės užsienio politiką, užmegzti kultūrinius, ekonominius santykius su tais regionais ir valstybėmis, su kuriomis mes norime tai daryti, ir šie veiksmai, niekaip nekvestionuoja vienos Kinijos politikos, kurią mes deklaravome prieš 30 metų, kurios mes laikomės ir šiandien“.

Iš visų nepripažintu valstybių Vilniaus dėmesį kažkodėl pritraukia būtent Kinijos Respublika.

Taibėjaus atstovybės, faktiškai atliekančios ambasadų funkcijas, Europoje yra plačiai paplitusios. Viena iš tokių įstaigų veikia Varšuvoje.

Dar 1990 metais Latvija bandė užmegzti ryšius su Taivanu. „Tai latviams baigėsi blogai, Taivanas atsisakė, o latviai kreipėsi į Kinija“, - prisimena Kinijos žinovas, RMA Tolimųjų Rytų Instituto direktoriaus pavaduotojas Andrėj Ostrovskij.

Lietuvos politikams tik šiais metais „prireikė“ atidaryti Kinijos Respublikos atstovybę. Anksčiau jie paskelbė karą KLR pagamintiems išmaniesiems telefonams, seime aptarinėjo „uigūrų genocido“ problemą, išėjo iš projekto „17+1“ (ir paragino likusias Europos šalis padaryti tą patį).

Taivano atstovybės atidarymas - viena, iš ilgos Lietuvos antikinietiškos politikos grandinės, grandžių.

Jis puikiai mato, amerikietiškos užsienio politikos prioritetus. Strateginiu varžovu Baidenui, kaip ir jo pirmtakams, lieka KLR – galingiausia pasaulio ekonomika, kuri parodė savo pranašumą koronaviruso pandemijos metu. Iš jos (o ne iš Rusijos!) sklinda pagrindinė grėsmė Jungtinių Valstijų hegemonijai.

Tikriausiai, todėl pasipriešinime su Rusija Baltųjų Rūmų šeimininkas padarė pauzę, o “Šiaurinio srauto - 2“ klausimu nusileido Maskvai ir Berlynui.

Ar verta brangų Badeno laiką skirti pasakojimams apie „rusišką agresiją“? Arba geriau akcentuoti jo dėmesį į tai, jog Lietuva įsijungė į pasipriešinimą Kinijai?

Nausėda tvirtina, jog, kaip ir anksčiau, jo šalis yra „vienos Kinijos“ šalininkė. Bet pasiremiant bet kokia patogia dingstimi šią poziciją galima peržiūrėti.

Šiame kontekste verta atkreipti dėmesį į Seimo deputato Lietuvos parlamentines grupės santykiams su Taivanu pirmininko Mato Maldeikio pasisakymą. Savo misiją jis mato tame, jog Lietuvos – Taivano santykius padarytu „pasisekimo istorija“. „Geriau turėti reikalą su aukšto išsimokslinimo, išvystytų technologijų demokratine šalimi su 23 milijonais gyventojų, negu su autoritariniu režimu, kuris gali imtis atsakomųjų priemonių, jei jūs žengsite žingsnį, su kuriuo jie nesutinka“, - tvirtina Maldeikis.

Tai yra, jo pasaulio įvaizdyje Taivanas ir Kinija yra antipodai. Nėra „vieningos Kinijos“ – yra „demokratinė šalis“ ir „autoritarinis režimas“, kuriuos Lietuvos politikas aiškiai atskiria. Bet to, Taivaną jis vadina būtent šalimi, o ne regionu ar sala.

Esą, būtent tame ir yra Pabaltijo respublikos „drąsos ir principingumo“ priežastis. Jos pačios patirtis rodo, kaip lengva netekti savo suvereniteto, turint reikalą su „autoritariniu režimu“.

Panašūs palyginimai verčia abejoti, jog „vieningos Kinijos„ principas Vilniui yra tarptautinių santykių aksioma. Juk, būtent Lietuva, prie 30 metų pirmoji pareiškė, jog išeina iš TSRS sudėties. Jei jos konfrontacija su KLR iš tikrųjų yra „vertybių politikos“ pasireiškimas, tai kas jai kliudo griežtai palaikyti Taivano nepriklausomybę?

Kinijos žinovas Nikolaj Vavilov mano, jog JAV nurodžius, Lietuva iš tikrųjų gali žengti tokį žingsnį. Papildomu stimulu jai gali tapti korupciją sudarančioji dalis.

„Žinomi atvejai, kai Taivano atstovai įkalbinėjo nedideles Afrikos ir Lotynų Amerikos šalis, kurios neturi absoliučiai jokių santykiu su Kinija, užmėgsti ryšius su Taivanu, idant padidinti jo autoritetą. O [tų šalių] vyriausybės buvo be galo korumpuotos, ir tuose mažuose Afrikos šalyse režimai buvo labai nestabilūs ir, kaip taisyklė, buvo kalbama apie korupciją aukščiausioje vadovybėje. Tai yra, šiuo atveju, akivaizdu, jog tokia Taivano taktika galėjo paliesti ir Lietuvą. Šiame Vašingtono ir Taivano interesai galėjo sutapti“, - tvirtino Vavilov.

Toks sprendimas kardinaliai pakeis visą Kinijos – Europos santykių kontekstą. Už tai užmokėti prisieis ne tik ir ne tiek Lietuvai, kiek vedančioms ES šalims. Be to kaina bus labai aukšta.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 15 — id: `scraped:rubaltic_lt:cb4ee734ed20f5af`

**Title:** Principo reikalas: Rusija turi atsisakyti turėti reikalų su Lietuva

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Rusijos ambasadorius Vilniuje atsakė į Lietuvos prezidento pareiškimą apie suinteresuotumą turėti gerus santykius su Rusija, pasakydamas, jog Rusija visada yra apsiruošusi geriems kaimyniniams santykiams su Lietuva. Problema tame, jog prezidentas Gitanas Nausėda pareiškė pasirengimą geriems santykiams su kokia tai alternatyvia, kita Rusija, o ta Rusija, kuri yra, jo netenkina. Gera priežastis susimastyti, ar dabartinė Lietuvą tenkina Rusija, kad palaikyti su ja gerus kaimyninius santykius?

„Rusijos – Lietuvos santykiai, deja, kaip jau ne karta mes pabrėžėme, randasi pačiame žemiausiame visos naujausios jų gyvavimo istorijos taške“, - interviu Lietuvos žiniasklaidai pareiškė Rusijos ambasadorius Vilniuje Aleksėj Isakov.

Be to, kas liečia Rusijos, tai „mes esame pasiruošę tikriems geriems kaimyniniams santykiams, pagristiems abipuse pagarba, atsižvelgiant į abiejų šalių interesus, laikantis nesikišimo į vidaus reikalus principo“, - sakė ambasadorius.

Šį pasisakymą galima skaityti replika dėl Lietuvos prezidento Gitano Nausėdos pareiškimo apie gerų santykių su Rusiją viltį.

Galiojanti sutartis apie Rusijos ir Lietuvos tarptautinių santykių pagrindus, kuri suteikia viltį geriems santykiams, buvo pasirašyta 1991 metų liepos mėnesio 29 dieną. Viltis siejama ne tik su pačia sutartimi, bet ir su pasirašymo data, kada “Rusijos ir Lietuvos tautos kartu kovojo už laisvę“.

„Tai buvo laikotarpis, kai lietuviai Vilniuje, o rusai – Maskvoje drąsiai stojo prieš tankus, jausdami nuoširdžią vieni kitų paramą. Kartu mes buvome stipresni“, – sakė Gitanas Nausėda.

Tai yra, įsigilinus, nieko sensacingo Lietuvos prezidentas nepasakė.

Kokia tai buvo Rusija? Rusija, kuri prakeikė savo sovietinę praeitį, įskaitant ir Pergalę Didžiajame Tėvynės kare, suskilo į dalis, palikusi 25 milijonus rusų buvusiose nacionaliniuose pakraščiuose, priėjo prie masinio bado slenksčio, savanoriškai atidavė visus savo nacionalinius interesus ir prileido NATO prie pat savo valstybės sienos. O dar pradėjo melstis JAV kaip Dievui, gyventi nuo vieno TVF kredito iki kito, ir tapo pavaldi „Harvardo berniukų“ nurodymams.

Prisiminimai apie tą Rusiją absoliučiai daugumai rusų sukelia siaubo ir kankinančios gėdos mišinio jausmą, todėl Lietuvos vadovybės viltims apie kitą Rusija nelemta išsipildyti. Tai nereiškia, jog Rusija niekada nepasikeis. Savo tūkstantmetine istorija Rusija įrodė sugebėjimą fantastinėm metamorfozėm. Tai reiškia, jog tikimybė, kad Rusija bus kuriama 1991 metų pavyzdžiu, artėja prie nulio.

Kokia tai Lietuva? Tai Lietuva, kurioje Rusijos pilietis Jurij Mel nuteistas 10 metų kalėti pagal straipsnį „karo nusikaltimai ir nusikaltimai žmoniškumui“ už tai, kad 1991 metų sausio mėnesio 13 dienos naktį švietė tanko žibintais ir, iš nukreiptos į orą patrankos, iššovė tuščiu šoviniu, Lietuva, kurioje visuomeninius veikėjus, kurie pasisako už gerus kaimyninius santykius su Rusija, automatiškai kaltina valstybės išdavimu.

Įsigalėjus persitvarkymui, Sovietų disidentai išeidavo į gatves kovoti už demokratinę Lietuvos ateitį. Šiuolaikinėje Lietuvoje atsirado savi disidentai, kurie už atsisakymą nuo valstybinės ideologijos yra persekiojami sovietų metodais.

Lietuvos valdžia išima iš spaustuvių ir draudžia platinti knygas, areštuoja jų leidėjus ir pjudo jų autorius. Už nesutikimą su oficialiu istorijos klausimų traktavimu galioja baudžiamasis straipsnis, pagal kurį galima keleriems metams sėsti į kalėjimą. Kai pradedi nagrinėtis, išaiškėja, jog toks griežtumas reikalingas tam, kad nuo istorinių faktų ir teismo medicinos ekspertizių išvadų apginti savo melą apie tai, jog Didžiojo Tėvynės karo metu Rytų Prūsijoje raudonarmiečiai užsiiminėjo Lietuvos gyventojų genocidu, o Vilniaus televizijos bokšto gynėjus 1991 metų sausio mėnesio 13 dieną sušaudė sovietų specnazas.

Kas liečia Rusijos – Lietuvos santykius, tai kokiais tie santykiai buvo, kai jie buvo? Kokią dvišalių santykių dienotvarkę siūlė Vilnius? Atgailauti už „sovietinę okupaciją“ ir išmokėti Lietuvai 830 milijardų dolerių materialinę kompensaciją.

Gal būt ir geriau, jog su Lietuva dabar Rusija jokių politinių santykių nepalaiko?

Su puikia ateities Lietuva, kurioje žmonių nesodina už tai, jog jie gina istorinę tiesą ir rašo knygas apie sausio 13? Kurioje kalėjimuose už nieką nekalinami sunkiai sergantys rusai.

Rusijos patvarumo atsargos didesnės nei Lietuvos. Ji greičiau sulauks naujos, geresnės Lietuvos, ir dargi gali pagelbėti bjauraus ančiuko pavirtimo gulbe procesui.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 16 — id: `scraped:rubaltic_lt:f7ed30cd1db2b8e6`

**Title:** Lietuva priėjo prie transporto krizės ribos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
„Latvijos geležinkeliai“ paskelbė apie eilinį masinį personalo sumažinimą. Rimtos problemos išryškėjo taip pat ir pas Lietuvos geležinkelininkus. Kartu su šiais procesais „Baltijos seserys“ gali likti be keleivių pervežimo autotransportu: Lietuvoje ir Latvijoje stinga autobusų vairuotojų, o tie, kurie yra, grasina pradėti streikuoti. Pabaltijui gresia kompleksinė transporto krizė.

„Latvijos geležinkeliai“ painformavo valstybinę užimtumo tarnybą apie savo planus iki metų pabaigos atleisti iš darbo 864 žmones. Tai jau trečias stambus personalo mažinimas paskutiniu metu.

Rugpjūčio mėnesį „Latvijos geležinkelis“ atleido apie 700 darbuotojų, o metų pradžioje pagarsino planą apie kas šešto darbuotojo – pusantro tūkstančio žmonių atleidimo iš darbo. Per paskutiniuosius trejus metus „Latvijos geležinkeliai“ personalas sumažėjo beveik trečdaliu: nuo dešimties tūkstančių iki septynių tūkstančių darbuotojų.

Ta pačia kryptimi situacija vystosi ir kaimyninėje Lietuvoje, kuri metų pradžioje jau neteko baltarusiško naftos tranzito, o metų pabaigoje, kaip laukiama, neteks ir baltarusiško kalio tranzito. Kroviniai iš Baltarusijos sudaro apie trečdalį „Lietuvos geležinkelių“ krovinių srauto – jų netekimas jai užtikrina tokius pačius procesus, kurie jau keletą metų aukštu tempu vyksta Latvijoje.

Tiesą sakant, šie procesai Lietuvoje prasidėjo jau seniai. Sustoja infrastruktūros atnaujinimas ir jos plėtra, Pavyzdžiui, neribotam laikui sustabdyti statybos darbai geležinkelio ruože Plungė - Šateikiai, kurių biudžetas siekia 56,5 milijono eurų.

Masinis darbuotojų atleidimas „Lietuvos geležinkeliuose“ – laiko klausimas. Lygiai taip pat kaip ir inventoriaus, bėgių, pabėgių bei vagonų pardavimas, sekant kaimynų latvių pavyzdžiu.

Kritinė situacija krovinių vežimų sferoje Lietuvai – jau, praktiškai, norma. Nacionalinė vežėjų automobiliais asociacija „Linava“ reguliariai pareiškia, jog rinkoje susidarė tolimų reisų vairuotojų deficitas, jog transporto firmos iš Lietuvos keliasi į Lenkiją bei kitas ES šalis, kuriuose iš karto keliais parametrais verslui vystytis yra lengviau.

Nuo praėjusio mėnesio nerimą keliantys signalai pasirodė ir Lietuvos keleivių vežimo automobiliais sferoje.

Priežastimi vadina nepatenkinamas darbuotojų darbo sąlygas dėl to pačio vairuotojų deficito. Sotinės savivaldybei stinga apie 200 vairuotojų.

„Vairuotojai priversti dirbti šešias dienas į savaitę, jie pavargę, pikti. Arba mes paskelbsime streiką, arba pati kompanija nebedirbs dėl darbuotojų trūkumo“, - aiškina Vilniaus viešojo transporto darbuotojų profsąjungos pirmininkas Algirdas Markevičius.

Analogiška padėtis ir Latvijoje. Stinga vairuotojų, kadangi vairuotojai nebenori vakcinuotis (jiems tai yra privaloma) nuo koronaviruso infekcijos, išeina iš darbo ir vyksta dirbti į Vakarų Europą. Dėl ko kyla grėsmė daugeliui autobusų maršrutų Latvijoje.

Kartu gali kilti ir geležinkelio pervežimų, ir pervežimų automobiliais: krovinių ir keleivių krizė. Pabaltijo jūrų uostai jau ilgą laiką randasi gilioje krizėje. Iki paskutinio laiko išsiskyrė tik lietuviška Klaipėda, bet tas laikas jau baigiasi. Dėl pandemijos, reguliariai uždaromų sienų bei visokiausių visokių kontaktų apribojimų, vežimų orlaiviais sferoje taip pat klostosi nepaprasta situacija.

Tam, kad įsivaizduoti, kaip praktikoje atrodys visiška transporto krizė, galima pažvelgti į Didžiosios Britanijos patirtį. Jungtinėje karalystėje šį rudenį ištuštėjo maisto produktų parduotuvių lentynos ir susidarė kilometrinės eilės prie prekybos centrų, kadangi nebuvo kam išvežioti maisto produktus. Karalystėje trūksta 100 tūkstančių vairuotojų.

Britų krizė buvo iššaukta sisteminėmis priežastimis. Tolimų reisų vairuotojais Britanijoje paskutiniais 15 metų dirbo taip vadinami „anglų tadžikai“. Gasterbaiteriai (atvykėliai iš kitų šalių) iš Rytų Europos: lenkai, bulgarai, tie patys atvykėliai iš Pabaltijo. Po „breksito“ ir pandemijos jie pradėjo masiškai grįžti į tėvynę, o vietiniams anglams arba škotams vairuotojo darbas – visiškai nerespektabilus ir mažai apmokamas darbas.

Visų pirma, tai santykiu sugriovimas su kaimynais – Rusija ir Baltarusijos respublika, kurios buvo pagrindiniais, o kai kuriuose sektoriuose – vieninteliais didelės logistikos infrastruktūros: jūrų uostų ir geležinkelių klientais.

Tai ir nepatenkinamos sąlygos verslui Pabaltijyje ir, bendrai paėmus, gyvenimo sąlygos Pabaltijyje, dėl ko iš Baltijos šalių emigruoja ir atskiri vairuotojai ir vežėjų organizacijos.

Šie gi metai Pabaltijyje – krizių metai. Sanitarinė – epidemiologinė, migracinė, energetikos... Dabar, štai, laukiama transporto krizė. Ir vėl reikės išgalvoti, kodėl dėl jos kalta Rusija.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 17 — id: `scraped:rubaltic_lt:e73c4b04110a02e6`

**Title:** Solidarumą su Ukraina Lietuva iškeitė į elektros energiją iš Rusijos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuva, Latvija ir Estija žymiai padidino elektros energijos importą iš Rusijos. Apie tai liudija 2021 metų pirmųjų devynių mėnesių kompanijos „Inter-RAO“ gamybinės veiklos rezultatai. Tuo pačiu metu RF atsisakė tiekti elektros energiją Ukrainai, kurios pastarajai nepakanka šildymo sezonui. Artimiausiu metu Pabaltijui gali būti iškeltas nemalonus klausimas: kaip galima didinti „Inter-RAO“ produkcijos importą, tuo metu, kai ši kompanija naudojama Ukrainos „smaugimui“?

Baltijos šalys tradiciškai yra vieni iš pagrindinių kompanijos „Inter-RAO“ eksporto rinkų. Sausio-rugsėjo mėnesiais pas Rusijos monopolistą jos užpirko 3,675 milijardo kWh elektros energijos, tai yra pusantro karto daugiau negu per praėjusių metų analogišką periodą.

Tam, kad korektiškai įvertinti situaciją, verta atsižvelgti į tai, jog pirmoji pandemijos banga iššaukė sunkiausią energetikos krizę: dėl karantininių apribojimų elektros energijos tiekimo iš RF paklausa stipriai „nusėdo“. Tai atsiliepė „Rosneft“, „Gazprom“: „Inter RAO“ bei kitų tėvyninių energetikos kompanijų gamybinėje veikloje. Galima teikti, jog dabar jos, paprasčiausiai, atsilygina praeitų metų eksporto nuostolius.

Nežiūrint į tai, rusiškos elektros energijos tiekimo į užsienį didėjimas vis vien yra įspūdingas.

Palyginimui: per 2019 metų pirmuosius devynis mėnesius užsienyje „Inter RAO“ realizavo 13,785 milijardo kWh elektros energijos, per tą patį 2018 metų laikotarpį – 11,936 milijardo kWh.

Šiuos rezultatus negalima paremti išskirtinai tik pasaulio ekonomikos atsistatymo tendencija.

Kalbant apie eksporto į Suomiją ir Baltijos šalis dinamiką, „Inter RAO“ išskiria du faktorius: klimatą („elektros vartojimo didėjimas 2021 metais, esant šaltesnei žiemai ir pavasariui, o taip pat karštai vasarai, taip pat ir žemam vandeningumui bei mažėjant HES gamybos apimtims „) ir kainas („elektros energijos bei anglies dvideginio (CO 2 ) išmetimo kvotų šiluminei generacijai Europoje kainų didėjimas“).

Naujiena apie tai iššaukė nervingą Aukščiausios Rados deputato iš „Opozicinė platformos – Už gyvenimą“ (OPUŽ) partijos Vadimo Rabinovičiaus reakciją

„Pirmoji sudarė sutartį penkerių metų sutartį su „Gazpromu“ iš karto po to, kai Ukraina jai padovanojo 1 milijoną kubų dujų, o antroji nupirko elektros energiją pas Rusiją, nors iki to ragino pačią Ukrainą to nedaryti“,- parašė Rabinovičius savo Facebook puslapyje.

Šiame trumpame „supratimo sraute“ yra kai kurie netikslumai. Visų pirmą, visgi keista kaltinti Lietuvą, jog ji „nupirko“ rusišką elektros energiją. Kalbama ne apie kokį tai vienkartinį sandorį – Pabaltijo respublika metai iš metų importuoja „Inter RAO“ produkciją. Antra, Lietuva ragino Ukrainą blokuoti elektros tiekimą iš Baltarusijos, o ne iš Rusijos.

Iš kitos pusės, Vadimo Rabinovičiaus pretenzijos gali tapti „pranašiškomis“.

Kol Baltijos šalys aktyviai perka energijos resursus pas „šalį-agresorių“, Ukraina stovi ant energetinės blokados slenksčio.

Visai neseniai tapo žinoma, jog Rusija nutraukė A markės anglies (antracitas) ir П (pasninkinis) markės anglies eksportą į Ukrainą. Nurodytos anglies markės naudojamos šiluminėse elektrininėse. „Priimtas sprendimas yra susijęs su didėjančia energetinių anglies markių paklausa. Rudens-žiemos periodu ypatingą dėmesį reikia skirti savų poreikių šalies viduje patenkinimui“, - pažymėjo RF Minekonomrazvityje.

Dūmos energetikos komiteto pirmininko pavaduotojas Igoris Ananskich tai aiškina kitaip. Jo žodžiais tariant, čia jokios politikos nėra – paprasčiausiai, Kijevas nepasirašė kontraktų su Rusijos anglių kompanijomis. „Kodėl Rusija kažkam tai turi duoti anglį be sutarties? Jei būtu sutartis, tai būtu ir tiekimas. Nėra sutarties – nėra tiekimo“, - susumavo Ananskich.

Rusišką energetinę anglį į Ukrainą importavo DTEK (Lugansko ŠE, Kirovorogo ŠE), „Donbasenergo“ (Slaviansko ŠE) ir „Technova“ (Darnicko ŠE, Sumų ŠE, Černigovo ŠE) kompanijos. Nejaugi žiemos išvakarėse jos „užmiršo“ užkontraktuoti jiems reikalingas kuro apimtis? Ar dėl kokių tai priežasčių derybos buvo nutrauktos?

Suprantama, Kijevas Maskvos veiksmuose įžiūri „energetinės agresijos“ požymius. Aukščiausios Rados energetikos komiteto pirmininkas Andrėjus Gerus sako, jog Rusija panašiai elgėsi 2014 metais – aktyvių kovinių veiksmų Donbase metu. Ir tai, tikriausiai, yra tas retas atvejis, kai Zelenskio komanda blaiviai vertina situaciją.

Turkiškų kovinių nepilotuojamų dronų „Bairaktara“ panaudojimas, LLR atstovo (kuris, tarp kitko, yra RF pilietis) sulaikymas pilkoje zonoje, Staromarjevka gyvenvietės užgrobimas...

„Tai Rusijos reakcija į paaštrėjimą Donbase“, - tvirtina Energetinės strategijos fondo pirmininkas Marunič, kuris nėra linkęs politizuoti energetikos klausimus.

Maždaug trečdalis, sudeginamos Ukrainos ŠE anglies, vežamas iš Rusijos. Pakeisti šias apimtis elementariai nėra kuo – visame pasaulyje stebimas iškasamo kuro deficitas. Esant norui, kūrenamas anglimi ŠE galima pervesti į kūrenamas dujomis, tačiau jų atsargos Ukrainoje ribotos.

Dar visai neseniai „liaudies tarnai“ manė, jog pas juos yra „stebuklinga lazdelė“ – galimybė atnaujinti rusiškos ir baltarusiškos elektros energijos tiekimą. Rodėsi, jog link to viskas ir ėjo. Embargo importui iš „nedraugiškų“ šalių baigėsi lapkričio mėnesio 1 dieną – Ukraina jo nepratęsė. Bet vėliau paaiškėjo, jog nei Rusijoje, nei Baltarusijoje nebuvo organizuoti elektros energijos tiekimo ukrainietiškom kompanijom aukcionai.

Kol kas neaišku, ar tai yra pilnavertės energetinės blokados pradžia. Panašios priemonės pasisekimas pagrinde priklausys nuo Baltarusijos pozicijos, kuri gali ne tik atnaujinti elektros tiekimą į Ukrainą, bet ir imtis rusiškos akmens anglies reeksporto. Ji turi patyrimą.

Tikėtina, jog to, kas vyksta, tiesa yra kažkur tai per vidurį. Rusija jau nebegali ignoruoti Zelenskio įžūlumo bei jo beribio leistinumo sau. Iš kitos pusės, atsisakymą eksportuoti į Ukrainą anglį ir elektrą galimą pagristi grynai rinkos santykiais.

Energetikos resursų paklausa pasaulyje žymiai viršija pasiūlymą, importuotojai yra priversti tarp savęs konkuruoti. RuBaltic.Ru analitikos portalas jau pasakojo apie tai, kaip rusiška akmens anglis nueina į Kiniją. Su elektra – ta pati istorija.

Kinai prašo „Inter RAO“ lapkričio ir gruodžio mėnesiais dvigubai padidinti elektros energijos tiekimą. Akivaizdu, jog kompanija jau ir taip dirba ant savo eksportinių galimybių ribos.

Artimiausiu metu išaiškės, ar Rusija yra pasiruošusi „nuraminti“ Zelenskį energetinių svertų pagalba. Ir tada Rabinovičiaus pareiškimas, kuris šiandiena kvepia trolingu, gali įgyti visiškai konkrečią reikšmę.

Kaip galima didinti elektros užpirkimą pas „Inter RAO“, kai ši kompanija naudojama Ukrainos „smaugimui“?

Vargu, ar Pabaltijys panorės atsakyti į šį klausimą.

Savi marškiniai arčiau kūno.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 18 — id: `scraped:rubaltic_lt:77e496c88a4a5c24`

**Title:** „Gražinti“ Kaliningradą: Lietuva kėsinasi į Rusijos teritorijos vientisumą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
JAV nesiliauja publikacijų srautas apie būtiną prevencinį smūgį Kaliningrado sričiai, kilus kariniam NATO konfliktui su Rusija. Auditorijai kalama mintis, jog Kaliningradas kelia grėsmę Europai. Geriausias šios grėsmės neutralizavimo variantas – iškelti Kaliningrado sritį iš Rusijos sudėties. Ir čia arenoje pasirodo Lietuva, kur, palaikant tom pačiom JAV, dešimtmečiais kuriama ir skleidžiama argumentų sistema, remiantis kuria Kaliningrado sritis – tai Mažoji Lietuva, kuri pagal teisybę turi priklausyti lietuviams.

„ Įtampos periodais NATO šalių vyriausybės gali lengvai sustabdyti krovininius automobilius, traukinius ir orlaivius aprūpinančius Kaliningradą. Naujos Estijos raketos, dislokuotos viename iš svarbiausių jūros sąsiaurių Europoje, gali pagelbėti produktų, kuro ir paramos srauto iš žemyninės Rusijos dalies į Kaliningrado sritį sustabdymui“, - šį mėnesį rašė žurnalas Forbes apie Kaliningrado srities maisto produktų blokadą, kaip Rusijos „nenuskandinamo lėktuvnešio“ Baltijos jūroje   sutriuškinimo priemonę.

Už vandenyno tokios publikacijos – įprastas dalykas.

Dar daugiau, neapykanta rusiškam eksklavui skleidžiama iš pat viršaus. JAV prezidento patarėjas nacionalinio saugumo klausimais Kaliningradą pavadino „durklu Europos širdyje“ Vyriausiais JAV karinių pajėgų Europoje vadas į jį nurodė kaip į pirmojo karinio smūgio objektą

Kokiu būdu išvaduoti Europą nuo „durklo“ jos širdyje? Visų pirma, žinoma, sutriuškinti Baltijos Karinio laivyno pajėgas Kaliningrade. Antra, okupavus regioną, peržiūrėti jo teisinį statusą ir pašalinti iš Rusijos sudėties.

Rusijoje pripažinta nepageidaujama organizacija Džeimstauno fondas – CŽV įkurta organizuoti darbą su sovietų pabėgėliais – prieš dvejus metus siūlė „po pergalės“ Kaliningrado sritį atiduoti Lenkijai. Atsidėkojant už tai, jog pastaroji sutriuškins RF karines pajėgas regione.

Ši sistema remiama sekančiomis tezėmis:

1. Šiuolaikiniame stovyje Kaliningrado sritis kelia grėsmę Europai ir turi būti demilitarizuota;

2. Kaliningrado demilitarizacija Rusijos sudėtyje nėra įmanoma, iki to, kol ši netaps demokratine europietiška šalimi. Jei artimiausioje ateityje tokia Rusijos transformacija nėra įmanoma, tai Kaliningrado sritį reikia iš jos atimti;

3. Rusijos teisė į Kaliningrado sritį nėra šventa. Potsdamo konferencijos sprendimu Karaliaučius buvo perduotas Sovietų Sąjungai penkiasdešimčiai metų: šis terminas seniai baigėsi, ir dar 1995 metais Kaliningradą reikėjo gražinti Europai;

4. Iš visų Europos šalių Lietuva turi daugiausiai teisių į Kaliningrado sritį. Ši žemė – istorinė Mažoji Lietuva. Daugelį amžių lietuviai buvo pagrindiniais srities rytinių rajonų gyventojais, ten suformavo savo nacionalinę kultūrą, o autochtoninių lietuvių gyventojų išnykimas tapo sovietų genocido rezultatu

Jei jūs manote, jog panašūs įsitikinimai – išprotėjusių marginalų kliedesys, jūs klystate. Tai oficiali arba pusiau oficiali, bet, vis tik, valstybės lygyje patyliukais skleidžiama politika.

Iš viso to, kas aukščiau cituota, tik apie „perdavimą penkiasdešimčiai metų“ Vilnius kuklinasi pareikšti oficialiai – jau pernelyg lengvai melą paneigia tie, kurie moka naudotis Internetu ir moka bet kokią kalbą iš tų, kuriomis buvo surašyti ir pasirašyti baigiamieji Potsdamo konferencijos dokumentai.

Ir tą melą Lietuvoje kartoja ne nežinomi šizofrenikai, bet isteblišmento žmonės. Per pastaruosius metus pasisakymais apie „aneksuotą Kaliningradą“ pasižymėjo Seimo deputatai, eurodeputatai, valdžiai lojalūs politologai ir pats „tautos tėvas“ Vytautas Landsbergis – šešėlinis šiuolaikinės Lietuvos valdovas.

Kas liečia likusio - tai oficiali Vilniaus pozicija.

„1944 metų spalyje pagrindinėje Mažosios Lietuvos dalyje prasidėjo gyventojų genocidas – daugiau nei 300 tūkstančių gyventojų buvo nužudyta, 100 tūkstančių deportuota“, - apie Raudonosios Armijos Goldapo-Gumbinės operaciją rašo oficialus Lietuvos „istorijos falsifikavimo fabrikas“ –Lietuvos gyventojų genocido ir rezistencijos tyrimo centras. Respublikos parlamentas dar 2006 metais priėmė nutarimą pripažinti „1944 – 1948 metais Mažojoje Lietuvoje prasidėjo gyventojų genocidas, kurio metu buvo nužudyta 320 tūkstančių gyventojų, jų tarpe daugiau nei 130 tūkstančių lietuviškos kilmės ir kad šis kraupus įvykis vis dar nėra pripažintas tarptautiniu mastu”.

Kuo grindžiamas tvirtinimas, jog raudonarmiečiai Rytų Prūsijoje nekariavo su nacistais, o užsiiminėjo taikių lietuvių genocidu? Niekuo. Iš kur paimti „genocido metu „išpjautųjų“ skaičiai. Iš „lubų“

Iš viso to, apie ką garsiai ir patyliukais kalba Lietuvos valdžia, tiesa yra tik tai, jog Mažoji Lietuva egzistavo. Kaliningrado sritis – iš tikrųjų lietuviškos kultūros lopšinė, jos teritorijoje kūrėsi literatūrinė lietuvių kalba ir buvo atspausdinta pirmoji lietuviška knyga. Kaliningrado srityje ir po šią dieną gyvena lietuviai ir lietuviškos kultūros paveldas pačiuose Rusijos vakaruose yra rūpestingai saugomas.

Tik Lietuvos politikams tai nerūpi. Juos ir „Didžioji Lietuva“ nelabai domina. Bet kokiu atveju, mažiau nei „Rytų partnerystės“ vystymo programa, „Baltarusijos demokratizacija“ ir „Rusijos sulaikymas“ Ukrainoje. Kitu atveju Lietuva neemigruotu, nenusigertu ir neišmirtu istoriškai rekordiniais tempais.

Kas liečia „Mažąją Lietuvą“, tai tas, pusiau pamirštas praeities įvaizdis, Lietuvos valdžiai yra reikalingas kaip politinis konstruktas, kad pateisinti teritorines pretenzijas į Kaliningrado sritį. Kam Lietuvos valdžiai reikalinga Kaliningrado sritis, jei jiems ir pati Lietuva nebėra reikalinga?

Todėl trečiojo asmens po prezidento ir valstybės sekretoriaus JAV užsienio politikos hierarchijoje pasisakymai apie „durklą Europos širdyje“, straipsniai amerikietiškose žurnaluose apie Kaliningrado srities maisto produktų blokadą ir slapta Lietuvos diplomatijos atstovų veikla regione skleidžiant „Mažosios Lietuvos“, kuri turi priklausyti Lietuvai, doktriną, tai – vienos grandinės grandys.

Tikrasis kaliningradietiškos istorijos dalyvis ne Lietuva. Ji tik vykdytoja, nors ir sąmoninga bei aktyvi.

Lietuvos aktyvumas Kaliningrado atžvilgiu – tai tik mažytė, už vandenyno ruošiamų rusiško eksklavo atžvilgiu, priemonių komplekso dalelė.

RuBaltic.Ru analitikos portalas parengė pranešimą šia tema Rusija neturi apsimesti, jog ji nieko nemato.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 19 — id: `scraped:rubaltic_lt:461c97c80d7b9d7c`

**Title:** Lietuva „užvažiavo“ ant Ukrainos dėl priekaišto jog perka baltarusišką elektrą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Ukrainos liaudies deputato Andrėjaus Geruso pareiškimas apie tai, jog Lietuva importuoja baltarusišką elektrą, neatitinka tikrovės. Taip įvertino Zelenskio bendražygio žodžius Pabaltijo respublikos Energetikos ministerija. Kitaip sakant, šalies valdžia vis dar nenori pripažinti, jog ji perka baltarusišką elektrą. Nors apie tai akivaizdžiai liudija, mažiausiai, dviejų pačios Pabaltijo valstybės žinybų duomenys – Statistikos departamento ir elektros tinklų operatoriaus Litgrid.

Andrėjaus Geruso pastebėjimai apie Lietuvos elektros sistemos funkcionavimą sukėlė daug triukšmo žiniasklaidoje (prezidento Zelenskio bendražygis pareiškė, jog Pabaltijo respublika didina elektros energijos importą iš Baltarusijos, nors savo užsienio partnerius ragina to nedaryti). Bet mažai kas pastebėjo, jog Vilnius šį išpuolį nepaliko be atsako.

Lenkų televizijos kanalas „Belsat“ paprašė Lietuvos energetikos ministeriją pakomentuoti šią situaciją. Pakomentavo.

„Lietuva nepirko ir neperka elektros energija pas baltarusius,- užtikrino žinybos atstovai. – Baltarusijos AE kelia grėsmę visam regionui; būtent todėl Lietuva ėmėsi visų būtinų priemonių kad laikytis „anti Astravo“ įstatymo nuostatų. Dėl to komercinis importas iš ten baigtas, o techninis srautas apribotas. Pasirodžiusi informacija nėra pagrista: ji neatspindi tikrovės“.

Kiekvienas sakinys vertas to, kad ji plačiai pakomentuoti. „Lietuva nepirko ir neperka elektros energija pas baltarusius“, - tai tiesa. Formaliai Pabaltijo respublika elektros energiją pas baltarusius neperka, kadangi prekiaujama Latvijos biržoje. Ši BelAE produkcija „nuasmeninama“ (tiksliai taip pat, kaip „nuasmeninamos“ rusiškos dujos, kurias Ukraina, skaitydama „europietiškomis“ užperka per tarpines firmas).

Per šių metų aštuonis mėnesius Pabaltijo respublika už baltarusišką elektros energija sumokėjo 133 milijonus eurų (daug daugiau nei per visus praėjusius metus). Ir tai ne „Kremliaus propagandistų“ spėliojimai – tai oficialūs Lietuvos Statistikos departamento duomenys. Jo vadovybė netgi nebando nuslėpti tą faktą, jog BelAE blokada žlugo.

Andrėjus Gerus savo ruožtu nurodo į kitą šaltinį – Lietuvos elektros sistemų operatoriaus Litgrid Interneto svetainę. Joje bet kuris norintis realaus laiko režime gali sekti, kaip keičiasi elektros energijos pertekėjimų tarp Lietuvos ir Baltarusijos galingumas.

Tikriausiai, sisteminiam operatoriui niekas nepaaiškino, jog šalis jau, būk tai, neperka elektrą pas Lukašenką.

Važiuojam toliau „Lietuva ėmėsi visų būtinų priemonių kad laikytis „anti Astravo“ įstatymo nuostatų“. Sunku ginčyti! Lietuva pilnai galėjo imtis „visų būtinų priemonių“.

Bet ar tai reiškia, jog taip vadinamas anti Astravo įstatymas, kuris draudžia elektros energijos importą iš Baltarusijos, dabar yra vykdomas? Ne.

Tiesa, neperseniausiai jis atsikaitė apie didelę „pergalę“ prieš BelAE: „Šiai dienai elektra iš Astravo daugiau nepatenka į Lietuvą. Šiandieną tai aš galiu garantuoti 110 procentų“. Lieka tik spėlioti, kur ponas Kreivys išmoko nustatyti elektronų kilmę. Pagal skonį ar apčiuopiant?

Tegul jis papasakoja, kuomi BelAE produkcija skiriasi nuo elektros, pagamintos bet kurioje kitoje elektrinėje.

„ Po viso to komercinis importas iš ten (iš Baltarusijos - RuBaltic.Ru pastaba) baigtas, o techninis apribotas”, - tęsia Lietuvos Energetikos ministerija. Su komerciniu importu viskas aišku: Dabar baltarusišką elektrą Lietuva perka ne tiesiogiai, o per Latviją.

Ši sistema buvo paruošta dar buvusio energetikos ministro Žygimanto Vaičiūno laikais, kuris pasiūlė atskirti komercinį ir fizinį srautus.

Apie techninio elektros energijos srauto iš Baltarusijos į Lietuvą apribojimą analitikos portalas RuBaltic.Ru jau rašė rugsėjo mėnesio 15 dieną. Litgrid vienašališkai nustatė ribinę elektros perdavimo linijų galią prie respublikos rytų sienos – 400 MW. Bet jau spalio mėnesį Lietuva pradėjo bedieviškai viršyti savo pačios limitus. Ir sustoti, kaip matosi, neketina.

Tuo įsitikinti visiškai nesunku – reikia tik pažvelgti į paminėtą Litgrid Interneto svetainę, kokia galia tiesiogiai dabar veikia elektros perdavimo linijos prie sienos su Baltarusija.

Tai yra, Litgrit pradžioje apriboja Lietuvos-Baltarusijos junginio galią, paskui atsiskaito, jog tų apribojimų nesilaikoma. O Energetikos ministerija vis vien pareiškia, jog „techninis srautas apribotas“.

Jei „batka„ Machno būtų bandęs įdiegti anarchizmo principus į energetiką, pas jį gautųsi kažkas tai panašaus.

Savo komentarą Energetikos ministerija baigia sakydama apie tai, jog Geruso informacija „nėra pagrista“ ir „neatspindi tikrovės“. Galima buvo pasakyti paprasčiau – informacija melaginga. Bet reikalas tame, jog Gerusas nieko neišgalvojo ir nepagarsino jokių insaidų.

Ne kaltins, gi, Energetikos ministerija melo platinimu Lietuvos elektros tinklų operatorių! Ji gali tik pabarti Andrėjų Gerusą už tai, kad pastarasis nesupranta skirtumo tarp elektros energijos pirkimo pas Baltarusiją ir elektros energijos pirkimo iš Baltarusijos.

Bet klausimai atkris savaime, jei Kreivio globotiniai patikslins: jie gyvena savo ypatingoje realybėje. Ten Lietuva jau seniai „nunulino“ elektros perdavimo linijas prie sienos su Baltarusija, o Lukašenka, tarptautinės bendruomenės spaudžiamas, ruošiasi uždaryti „nesaugią“ BelAE.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 20 — id: `scraped:rubaltic_lt:63d518ea9704228d`

**Title:** Rusija – tai Kinija: NATO ir Pabaltijys bando gražinti JAV dėmesį

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Sąjungininkai Europoje deda visas pastangas JAV dėmesio gražinimui, kurios vis mažiau dėmesio skiria Senajam pasauliui ir „Rusijos sulaikymui“ ir vis daugiau dėmesio skiria kovai su Kinija. Užtikrinti patrono iš už Atlanto dėmesį sau, toks uždavinys vienija Pabaltijo šalis ir Šiaurės Atlanto aljanso sekretoriatą. Kovoje už šeimininko palankumą jie prisikalbėjo iki to, kad pradėjo tvirtinti, jog Kinija ir Rusija – tai vienas ir tas pats, ir jų „sulaikymą“ negalima atskirti.

„JAV turi fokusuoti savo sutelktą strateginį dėmesį ne tik į vieną Ramiojo vandenyno tašką, bet ir Europos rytuose“,- sako Lietuvos užsienio reikalų ministro pavaduotojas Mantas Adomėnas.

„Aš labai viliuosi, jog dabartinė JAV administracija ir Europos Sąjungos šalys neužmirš iššūkių, kuriuos sukuria Rusija“,- jį kartoja Latvijos URM vadovas Edgars Rinkėvičs.

„Su JAV mes bendradarbiaujame visuose sferose ir aiškiname jiems, kokią mes matome situaciją su mūsų regiono saugumu ir mūsų regiono problemas... Mums taip pat svarbu, kad JAV tęsia savo buvimą ir domisi įvykių Europoje vystymusi“,- kalba Estijos užsienio reikalų ministrė Ieva-Marija Lijimets.

Kyla klausimas, kas čia per kauksmas pelkėse? Ritualinė kolektyvinė rauda? Pabaltijo choras?

Apie tai jie choru maldauja žurnalo Newsweek puslapiuose. Jaučiasi tradicijos atnaujinimas: vakarų lyderiai pabaltijiečius priima viena krūva – amerikiečių žiniasklaida ima pas juos interviu taip pat viena krūva. Numanoma, jog jokio skirtumo tarp Lietuvos, Latvijos ir Estijos nebėra. Jų atstovai sako lygiai vieną ir tą patį. Jie nebegali viens kitam prieštarauti: tik papildyti ir pritarinėti.

Bet reikalas netgi ne tame. „Tų, kuriuos liovėsi mylėti, pastangose visada yra kažkas tai juokingo“, - savo laiku rašė Oskar Wilde.

„Vertimas iš fantominės kalbos į žmonių kalbą reiškia sekantį. Daugelį metų sąžiningai atidirbant amerikietiškas direktyvas nukreiptas į rusafobiją ir prieštaraujant savo interesams, visiškai nutraukus santykius su Rusija, šie politiniai režimai labai baiminasi, jog nesugebės įsikibti į, paliekančio savo ankstesnės geopolitinės įtakos ribas, amerikietiško orlaivio sparną“, - komentavo Vilniaus, Rygos ir Talino atstovų choro koncertą žurnalo Newsweek puslapiuose oficiali Rusijos UER atstovė Marija Zacharova.

Tačiau Pabaltijo respublikoms dabar visiškai nejuokinga. Ir ne tik joms. Visi, kas yra priklausomi nuo siuzereno už vandenyno, jaučia grėsmę dėl to, jog beveik visas jo kilnybės interesas persikėlė į Ramiojo ir Indijos vandenynų regionus, o Europa ir NATO daugiau nereikalingi.

Bandoma nuostabiausiais būdais pakartotinai suinteresuoti savimi ir įrodyti Amerikai savo reikšmę.

„Visa ta idėja dėl tiek daug skirtumų tarp Kinijos, Rusijos, Azijos-Ramiojo vandenyno regiono arba Europos [neteisinga] – tai viena didelė saugumo aplinka, ir į tai mes turime pažvelgti kartu“, - interviu Financial Times sakė Stoltenberg

Stoltenberg įsitikinęs: sąjungininkai neturi vertinti Kinijos „grėsmę“ atskirai nuo Rusijos „grėsmės“. Ir, dėl Kinijos, apie pastarąją jokių būdu negalima pamiršti.

Atsisakymas nuo Rusijos „sulaikymo“ sukels Rytų Europos šalių, kurios vertina Kremlių kaip egzistencinę grėsmę, protestus, o NATO – kaip vienintelio savo saugumo garanto – Amerikos skaitytojams įrodinėja generalinis NATO sekretorius.

Doktrina „mes sakome „Kinija“, numanome – „Rusija“; sakome „Rusija“, numanome „Kinija“, neabejotinai nauja ir originali. Tik šansai, jog amerikiečiai ja susidomės, beveik nepastebimi.

Vašingtono veiksmai Europoje ir Eurazijoje dabar yra pašvęsti tam, kad neleisti nesusidaryti dviejų jo pagrindinių priešininkų karinei-politinei sąjungai. Dėl to ir Baideno susitikimas su Putinu, ir Viktorijos Nuland vizitas į Maskvą, ir pirmasis sankcijų nuėmimas, ir beveik demonstratyvus Ukrainos ignoravimas.

Taip, kad kreatyvi Generalinio NATO sekretoriaus idėja – tai, kaip sakoma „Dievui į langą“. Teks jiems su Pabaltiju ir toliau kreatyvinti – o tai dar globėjas iš už Atlanto galutinai užmirš, jog yra tokia Europa, o Europoje JAV turi sąjungininkų, kuriuos jos turi palaikyti.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```
