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

### Article 1 — id: `scraped:rubaltic_lt:39e84a756d6c4769`

**Title:** Lukašenka pavirto kovos už valdžią Lietuvoje instrumentu

**Source:** rubaltic_lt (propaganda)

**Text:**

```
JAV finansų ministerijos Užsienio aktyvų kontrolės valdyba pranešė, jog „Lietuvos geležinkeliai“ (LG) neprivalo stabdyti baltarusiškų trąšų tranzitą vykdant amerikiečių sankcijas. Bet kompanija vis vien ketina nutraukti santykius su „Belaruskalij“. Pabaltijo respubliką nedomina, ar tai yra efektyvus kovos su „paskutiniu Europos diktatoriumi“ instrumentas. Lietuvos valdančioji partija, prisidengdama Lukašenkos „baidykle“, sprendžia savo vidaus politikos problemas.

Kaip žinoma, LG generalinis direktorius Mantas Bartuška jau teiravosi pas JAV finansų ministerijos atstovus, ar reikia jo kompanijai nutraukti kontraktus su „Belaruskalij“. „Pokalbio metu mus patikino ir paaiškino, jog dabartinėje sankcijų apimtyje, jei amerikiečių subjektai nedalyvauja tiekimo grandyje, tai sankcijos neveikia“, kalbėjo Bartuška.

Dabar jo žodžiai patvirtinti dokumentaliai.

Apie tai gruodžio mėnesio 20 d. pranešė geležinkelio kompanijos atstovas Mantas Dubauskas.

Dar prieš kelias savaites Lietuvos valdančios partijos atstovai kartu su premjerė Ingrida Šimonytę galėjo „vaidinti“ silpnapročius:, esą, mums nežinoma kaip veikia JAV sankcijos, klausimas reikalauja papildomo nagrinėjimo. Dabar situacija paaiškėjo.

Lieka tik išsiaiškinti, su kuo susijęs maniakinis konservatorių troškimas pjauti šaką, ant kurios sėdi Lietuva.

Viena iš priežasčių paviršiuje: Pabaltijo respublika banaliai nori įsiteikti amerikiečiams. Blogas tas „palaižūnas“, kuris nesolidarus su „šeimininku“.

Bet tai tik viena medalio pusė.

Vieną iš tarpinių uždavinių „landsbergistai“ jau išsprendė: artimiausiu metu Mantas Bartuška paliks savo aukštą postą. Taip nusprendė LG valdybą, išnagrinėjusi Lietuvos susisiekimo ministro Mariaus Skuodžio kreipimąsi. Būtent jis nuspėjo, jog po skandalo su „Belaruskalij“ Bartuška bus priverstas atsistatydinti.

Konkrečiai, ką pažeidė Lietuvos geležinkelio vadovas? Nieko. Jį atleisti galima nebent pagal formuluotę „už pavyzdingą įstatymų laikymąsi“ . Bartuška veikė sutinkamai su savo kontrakto prievolėmis bei JAV finansų ministerijos rekomendacijomis, kurių jis pats apdariai ir užklausė.

Skuodis pirmasis nuspėjo, jog gruodžio 8 baltarusiškų trąšu tranzitas per Lietuvą bus sustabdytas. Kai tai neįvyko, jis sukėlė skandalą ir pareiškė jog pasirengęs atsistatydinti, bet Ingrida Šimonytė jo neatleido.

Toks pat likimas ruošimas ir Klaipėdos uosto vadovui Algiu Latakui (jis dar priešinasi). Kodėl? Todėl, jog abu valdininkai buvo paskirti į pareigas dar prie buvusios valdžios.

Bartuška pradėjo vadovauti LG 2016 m. gruodyje, iš karto to po triuškinančios Lietuvos Valstiečių ir „žaliųjų“ Sąjungos (LVŽS) pergalės parlamento rinkimuose. Latakas pradėjo vadovauti uostui užpraeitą vasarą.

Nei vienas iš jų, tikriausiai, nėra Landsbergistų klano lobistas. Nei tą, nei kitą negalima paprastai atleisti. Reikalingas skambus skandalas.

Artimiausiu metu dvejomis ypatingai svarbiomis valstybės kompanijomis – Klaipėdos uosto direkcija ir Lietuvos geležinkeliu gali pradėti vadovauti artimi valdžios partijai žmonės.

Apie tai RuBaltic.Ru analitikos portalas rašė dar prieš metus: „Gabrielius Landsbergis, kuris savo laiku įžvelgė baltarusiškų investicijų į Klaipėdos uostą „grėsmę“, dabar vadovauja URM ir pretenduoja į Lietuvos politikos naujojo lyderio vaidmenį. Nenuostabu, kodėl konservatorių vyriausybė demonstratyviai pradėjo galvoti apie sankcijas „Belaruskalij“? Jiems tai gali būti „nepatikimo“ investoriaus išvijimo iš Klaipėdos uosto instrumentu. Negalima atmesti, jog Vilnius iš tikrųjų vers „Belaruskalij“ parduoti savo biriųjų krovinių terminalo akcijas“.

Kalbama apie Biriųjų krovinių terminalą, kurio 30% akcijų priklauso baltarusiškai kompanijai. Savo laiku LRT kanalas išaiškino, jog LVŽS rinkiminę kompaniją rėmė žmonės, susiję su šia kompanija, o „Belaruskalij“ generalinis direktorius Ivan Golovat atvirai simpatizavo Lietuvos „valstiečių“ lyderiui Ramūnui Karbauskiui.

Tai, kad „landsbergistams“ baltarusiško tranzito sustabdymas – ne tik principo reikalas, bet ir būdas, kaip susilpninti „vidinius“ konkurentus.

Pats tas Karbauskis neišsigando pasmerkti isteriją dėl „Bekaruskalij“.

„Dėl vaikų darželio lygio užsienio politikos Kinijos ir Baltarusijos atžvilgiu Lietuva neteks šimtus milijonų eurų, tuo metu, kai Latvija, Estija bei kitos šalys juos lengvai paims, todėl jog tai, ką konservatoriai Lietuvoje pateikia kaip „tabu“, kituose ES šalyse neveikia. Kodėl dabar reikia valstybės ekonomiką įvaryti krizėn, padaryti mūsų valstybę ir verslą nekonkurencingais, atėmus iš jo visas galimybes būti regiono lyderiu?“, - stebisi Karbauskis.

Kaip rodo sociologinė apklausos, sankcijų karo su Lukašenka priešininkai Lietuvoje, visiškai ne marginalai: vyriausybės veiklai Baltarusijos kryptimi nepritaria 37% respondentų. Laikui bėgant jų gali padaugėti.

Tai gana solidi elektoratinė „šėrykla“. Ypatingai Lietuvos valstiečių ir žaliųjų sąjungai, kuriai dabartinis metas ne geriausi laikai.

Šiandieną „valstiečiai“ stovi kryžkelėje: arba jie susiras naują amplua, arba paliks aukščiausią Lietuvos politikos ešeloną. Kaip tik, paprastos liaudies, kuri kenčia dėl beprotiškos konservatorių politikos, gynėjo vaidmuo neužimtas.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 2 — id: `scraped:rubaltic_lt:0e3a1a7f6b5e46ea`

**Title:** Lietuva susigriebė:  Latvija ir Estija pasiima Baltarusišką tranzitą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
„Beraruskalij“ trąšų tranzitas, kurio ketina atsisakyti Lietuva, gali būti vykdomas per Latvijos uostus. Apie tai pareiškė Lietuvos URM vadovas Gabrielius Landsbergis. Negalima atmesti , jog dalį baltarusiškų kalio trąšų imsis vežti Estija, kuri jau pasiėmė baltarusiškų naftos produktų tranzitą. Jokių juridinių kliūčių tam nėra – ES ir JAV sankcijų režimas leidžia Pabaltijo respublikoms bendradarbiauti su „Belaruskalij“.

Sprendžiant iš lietuviškos šalies pareiškimų, aiškėja, jog ji rimtai ketina sustabdyti baltarusiškų krovinių tranzitą. Ingridos Šimonytės  ir Seimo valdančios koalicijos arsenale yra keletas variantų.

RuBaltic.Ru analitikos portalas jau aprašė viena iš jų: Lietuva gali organizuoti finansinę „Belaruskalij“ blokadą (tokią pat kaip ir sanatorijai „Belarus“ Druskininkuose). Jei nei vienas bankas neaptarnaus „uždraustų“ krovinių perkrovos Klaipėdos uoste, tranzitas sustos.

Atitinkamas dokumentas Seime jau užregistruotas.

Galų gale, „Lietuvos geležinkelis“ (LG) paprasčiausiai, nepaaiškinant priežasčių, gali nutraukti kontraktus su „Belaruskalij“. Bet šiuo atveju jam garantuoti daugiamilijoniniai teismo ieškiniai.

Bendrai paėmus, Pabaltijo respublikos vadovybei reikia spręsti nepaprastą uždavinį: stabdyti baltarusišką tranzitą ir neleisti nacionalinio geležinkelio operatoriui  bankrutuoti.

Laikraštis Eesti Paevaleht pranešė, jog Estija didina baltarusiškos produkcijos tranzitą: „Remiantis statistikos departamento duomenimis, spalyje buvo viršytos rekordinės, importuojamų ir Baltarusijos, prekių, kurios pagrinde per Estija gabenamos tranzitu, apimtys. Per šių metų pirmuosius 10 mėnesių iš Baltarusijos į Estiją buvo įvežta prekių už pusę milijardo eurų. Pagrinde, tai sunkieji naftos produktai, tokie, kaip mazutas, kuris sudaro 4/5 importo“.

Jei estų politikai pamėgdžiotų lietuvius, jie sukeltų grandiozinį skandalą: ministrai atsistatydintų, nacionalinės geležinkelio kompanijos vadovą padarytų atpirkimo ožiu, o parlamente pasiūlytų įsteigti „pasipiktinimą keliančio“ baltarusiško tranzito fakto tyrimo komisiją.

Ir nieko tokio neatsitiko.

Sektorinės Europos sąjungos sankcijos numato baltarusiškos kilmės naftos produktų transportavimo draudimą.

Kodėl tranzito apimtys siekia rekordus? Tikriausiai, todėl, jog galiojančiais estų-baltarusių kontraktais tai yra numatoma.

Tuo tarpu, Latvijos krovinių vežėjai jau sulaukia užklausų dėl „Belaruskalij“ produkcijos tranzito organizavimo galimybės. Mažiausiai viena kompanija tai oficialiai patvirtino.

„Manau, jie (baltarusiai – RuBaltic.Ru pastaba) bando visus variantus, kurie galimi, įskaitant ir Latviją. (...) Mes kalbėjome apie geležinkelio technologijas, apie kokioje padėtyje randasi Latvijos geležinkelio infrastruktūra. Aš nekalbu apie sankcijas, teisinius niuansus, aš kalbu tik apie technologijas ir techninius dalykus – mes konsultavomės su „Belarusklaij“, taip - pareiškė privačios latvių geležinkelio kompanijos Baltijas Expresis valdybos pirmininkas Maris Bremzė.

Jo žodžiais tariant, iš tikrųjų yra grėsmė, jog baltarusiškų trąšų tranzitas bus perkeltas į Latviją, kadangi „privalomo sankcijų režimo nėra“. „Tai, ne nuo vyriausybės (Latvijos -  RuBaltic.Ru pastaba) priklausantys sprendimai. Vyriausybė nusiteikusi labai geranoriškai ir linkusi bendradarbiauti su mumis... Bet yra privačios kompanijos, kurios, matydamos jog nėra jokių teisinių pasekmių, gali tiesiogiai imtis ir  veikti taip, kaip joms rodosi“, - tvirtina Landsbergis.

„Jei Latvijoje nebus priimtas įstatymas dėl baltarusiškų krovinių tranzito, o Latvija nesiruošia tokio įstatymo priimti, jie gali ramiai pasiimti krovinį ir vežti, kaip tai jie jau labai sėkmingai darė iki 2012-13 metų“, - papildo Lietuvos geležinkelio kompanijų asociacijos vadovas Tomas Keršis.

Europietiškos sankcijos neliečia baltarusiškų trąšų tranzito sferą, o JAV sankcijos nėra eksteritorinio pobūdžio (jos liečia tik amerikietiškus fizinius ir juridinius asmenis). Tai faktas, kurį pripažįstąs pats Landsbergis.

Baltarusiško tranzito atsisakymas –  grynas Lietuvos politikų kaprizas.

Buvęs Lietuvos premjeras ir buvęs susisiekimo ministerijos vadovas Algirdas Butkevičius įsitikinęs, jog tai atsitiks. „Tai aš pastebėjau būdamas premjeru ir transporto ministru: prie stalo sėdėjome kartu, vedėme bendrus pasitarimus, o po to kiekviena šalis bandė pritraukti papildomus krovinius iš trečiųjų šalių. (...) Ši konkurencija visada buvo: viešai buvo kalbama vieną, o daroma visai kitą. Jei nėra raštiško susitarimo dėl to jog mes veiksime principingai ir nevežime tam tikrų krovinių, tai tikėtis, jog bus laikomasi žodinių susitarimų nėra ko – to niekada nebuvo“, - aiškino Butkevičius.

Istorija kartojasi: kažkada Lietuva jau priėmė, taip vadinamą, anti-Astravos įstatymą, kuris draudžia elektros energijos importą iš Baltarusijos. O Latvija ir Estija jokių sankcijų BelAE neįvedė. Dar daugiau, latviai netgi perkėlė prekybos elektra su trečiomis šalimis tašką ant savo nacionalinės sienos (anksčiau visos operacijos buvo vykdomos per Lietuvą).

Butkevičiaus žodžius neverta priimti kaip gryną tiesą: ne faktas, jog Lukašenkai bus atverti latvių uostų vartai. Galų gale, Europos sąjunga gali kopijuoti amerikietiškas sankcijas ir uždrausti baltarusiškų trąšų tranzitą per savo teritoriją.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 3 — id: `scraped:rubaltic_lt:401b4dd45e62fb5f`

**Title:** „Pabaltijo seserys“ kovodamos su baltarusiškai kroviniais, rungiasi dėl ištikimybės JAV

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Baltarusijos krovinių tranzitas per Pabaltijo uostus virsta karšta bulvę, kurią Pabaltijo uostai metinėja vienas kitam į rankas tikėdamasi kuo greičiau ja nusikratyti. Ekonominė logika, remiantis kuria, Latvijai, Lietuvai ir Estijai baltarusiškas tranzitas yra naudingas, atmetama kaip gėdinga. Laimi politinė logika, remiantis kuria, daryti pinigus su šalimi, kuriai JAV įveda sankcijas – parodyti savo politinį nelojalumą siuzerenui. „Pabaltijo seserys“ pradeda rungtyniauti, kuri iš jų daugiau atsidavusi Amerikai.

Lietuvoje istorija dėl tęsiamo, nepaisant įsigaliojusių JAV sankcijų, „Belaruskalij“ produkcijos tranzito, pavirto pigia politine muilo opera.

Lietuvos transporto ir užsienio reiklų ministrai, liaudiškai sakant, supsichavo ir padavė pareiškimus apie atsistatydinimą, Esą, tokia gėda.

Ir jie laiku nesugebėjo nieko su tuo padaryti.

Lietuvos premjerė Ingrida Šimonytė įsakymo atleisti nepasirašė ir liepė ministrams grįžti į darbą. Pasiaukojančiu triūsu išpirkti savo kaltę Jungtinėms Valstijoms.

Šį sprendimą pasmerkė Lietuvos prezidentas Gitanas Nausėda. Jo nuomone, ministrai suveikė neatsakingai ir turi būti atleisti, kadangi savo apsileidimu jie diskreditavo vertybiškai orientuotą Lietuvos užsienio politiką.

Visiems akivaizdu, jog išsivysčiusi absurdiška melodrama – tai veikiančiojo valstybės vadovo ir konservatorių vyriausybės, kuri nori „nustumti“ Gitaną Nausėdą ir jo kėdėn pasodinti URM vadovą Gabrielių Landsbergį, kova.

Kitaip sakant, kas sėkmingiau suveiks prieš Lietuvos interesus.

Kuo gi prezidentas Nausėda pričiupo „landsbergistus“? Tuo, jog jie, tokie principingi, tokie pro amerikietiškai nusiteikę, su tokiu ryžtingumu niokojantys Lietuvos ekonomiką dėl „vertybių politikos“, nesugebėjo sinchronizuoti Lietuvos užsienio politikos su JAV politika. Amerikiečių sankcijos „Belaruskaliui“ jau veikia, o „Belaruskalij“ tranzitas per Lietuvą pratęstas 2022 metams – koks siaubas!

Kartu su tuo visiems farso dalyviams šimtą kartų buvo kartojama, jog JAV sankcijos liečia tik amerikiečių kompanijas, ir Lietuva neprivalo, remdamasi amerikiečių sankcijomis, įvesti sankcijas „Belaruskaliui“. Tai kartojo, tame tarpe, patys amerikiečiai – JAV finansų ministerija. Bet ar gali Lietuva nepasinaudoti galimybe išreikšti transatlantinį solidarumą ir išsitarnauti siuzerenui?

Nors pats siuzerenas to ir neprašo.

Paradoksali situacija.

O taip pat ir trečiam pagal dydį šalies miestui – Klaipėdai, kurios gyvavimas priklauso nuo uosto veiklos.

Ekonominė logika visiškai pralaimi politinei. Tas, kuris kovoje už valdžia remsis nacionaliniais interesais ir nauda Lietuvai, pralaimi iš karto ir visam laikui.

Ši taisyklė tinka ne vien tik Lietuvai.

Estijos statistikos departamento duomenimis, šiais metais Estijos ir Baltarusijos prekių apyvarta pasiekė rekordinį lygį: įvežamo į respubliką baltarusiško mazuto ir tepalų sąskaita Baltarusija pateko į šalių dešimtuką su didžiausia importo į Estiją apyvarta. Estijos uostų ir geležinkelio pelnas baltarusiškų naftos produktų dėka sudarė pusė milijardo eurų.

Estijos žiniasklaida į šiuos palankius duomenis reagavo tokio tipo antraštėmis „Estija remia kraugerišką Lukašenkos režimą“. Šalies vyriausybė priversta teisintis, jog Europos sąjungos sankcijų Estija nepažeidžia.

„Prekių judėjimą kontroliuoja Latvijos muitinė ir Estijos mokesčių-muitinės departamentas, o prekių vežėjai patikrino prekių atitinkamumą sankcijuojamų prekių sąrašui ir pažeidimų nebuvo rasta“, - sakė Estijos URM sekretorė spaudai Kristina Ots – dabartiniu metu užsienio reikalų ministerijoje nėra pagrindo manyti, jog Estijos valstybės įmonė ar kompetentingos įstaigos pažeidė nustatytas sankcijas. Jei apribojimai bus patikslinti arba pakeisti, jų taikymas, suprantama, bus peržiūrėtas“.

Pas Estijos valdančiąją koaliciją nėra tokių galingų konkurentų kovoje už valdžią, kaip Lietuvoje, todėl ten galvoja, jog gali reikšti tokius pareiškimus ir leisti truputi uždirbti Estijos tranzito šakai, kuri ilgą laiką buvo nuostolinga. Bet be vidaus politikos konkurencijos dar egzistuoja ir išorinė.

Šiame pavyzdyje Vilnius save pozicionuos vertybių politikos moraliniu kriterijumi, o Estiją – silpna grandimi europietiško ir transatlantinio solidarumo grandinėje, kuri daro pinigus su „paskutiniuoju Europos diktatoriumi“.

Ir pastarajai tai bus pačios liūdniausios pasekmės. Juk „Pabaltijo seserys“ vieningos tik kovoje su Rusija, o taip jos pastoviai konkuruoja viena su kita dėl europietiškų ir amerikietiškų investicijų.

Kurioje iš trejų Pabaltijo šalių bus regioninis SGD terminalas, kurios šalies sostinėje bus geležinkelio Rail Baltica buveinė (ir kur, atitinkamai, eis pinigai iš ES fondų), kur bus įkurdintas amerikiečių karinis kontingentas? Visa tai yra aštrių intrigų ir žūtbūtinės užkulisinės Lietuvos, Latvijos ir Estijos kovos dalykai.

Latvijoje, kuri anksčiau pasižymėjo savo pragmatišku požiūriu į Minską, iki tos paprastos minties, panašu jau prisigalvojo. „Mano nuomone, latviškoji užsienio politika labai aiški. Kol mūsų valstybėje į valdžia neateis kitos politinės jėgos, mums labai aišku, kas yra mūsų bendradarbiavimo draugai ir partneriai“, - kalbėjo susisiekimo ministras Talis Linkaits apie tai, jog baltarusiškų ir rusiškų krovinių tranzitas Latvijai jau ne ekonominis, bet politinis klausimas.

Kas liečia Rusiją, tai Maskvoje jau labai seniai suprato tą logiką, kuria gyvena „Pabaltijo partneriai“, todėl dar prieš dvidešimt metų pradėjo naujų Baltijos jūros uostų kroviniams statybą, o paskutiniaisiais 5 metais aktyviai perveda į juos tranzitą.

Ir perorientuoti į Rusiją visa baltarusišką tranzitą, nepasitikint ontologiniu Estijos priešiškumu Minskui.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 4 — id: `scraped:rubaltic_lt:da46ff59dd4f5dc3`

**Title:** Bėk, Lietuva, bėk: Rusija slenka link sąjungos su Kinija prieš NATO Pabaltijyje

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Politinė Rusijos ir Kinijos sąjunga pasiekia kokybiškai naują lygį. Kremliuje pareiškė, jog KLR Pirmininkas Si Czinpinas parėmė Rusijos prezidento Vladimiro Putino iniciatyvą dėl raštiškų Vakarų garantijų neplėsti NATO karines pajėgas greta RF sienų. Pekinas įsitraukia į geopolitinę kovą Rytų Europoje, palaikydamas Maskvą, ir žengia rimtą žingsnį, nukreiptą į savo užsienio politikos Rytų Europoje sinchronizavimą su Rusija. Pro amerikietiškai nusiteikusiems limitrofams prie Rusijos sienų šis rusų-kinų tandemas nežada nieko gero.

„Kadangi Pirmininkas specialiai pareiškė, jog jis remia Rusijos reikalavimą garantijų, tai, žinoma, jis apie tai gerai painformuotas ir supranta svarbiausią: susirūpinimą, kurį jaučia Rusija prie savo vakarinių sienų“, - sakė Rusijos prezidento padėjėjas užsienio reikalams apie Vladimiro Putino ir Si Czinpino video pokalbio turinį.

Tai, ką sako Kremliaus atstovas, sensacija pasaulio ir Europos politikoje.

Ne tik parėmė, bet ir sutiko su tuo, jog Rusijos šalis pagarsins jo, draugo Si poziciją: jis remia šį, dabartiniu metu „nugalėtojams šaltajame kare“ faktiškai neįmanomą Putino reikalavimą Vakarams.

„Šalys sutarė kontaktuoti šiuo klausimu. Ir mes informuosime kinų kolegas apie tai, kaip vystysis kontaktai ir derybos šiuo klausimu su amerikietiškais ir NATO partneriais“, - sakė Jurijus Ušakovas apie Putino ir KLR Pirmininko susitarimus.

Šis pareiškimas ne mažiaus svarbus kaip ir prieš tai buvęs.

Kartu su tuo atsižvelgdama į Rusijos interesus bei susiejant kinų interesus su rusų interesais.

Ar didelė tikimybė, jog rusų-kinų tandemas regione susiformuos iš tikrųjų? Taip, tam yra visos prielaidos.

Visų pirmą, šiandieną Rusijos-Kinijos santykiai yra kaip niekada aukštame lygyje, Vladimiras Putinas juos charakterizavo Si Czinpinui „tikras dvidešimt pirmojo amžiaus tarpvalstybinio bendradarbiavimo pavyzdys“.

Antra, bendras Maskvos ir Pekino priešas – Vašingtonas, kuris jų abiejų atžvilgiu vartoja „sulaikymo“ taktiką, Rusijos ir Kinijos perimetru regzdamas nestabilumo lanką iš joms priešiškai nusiteikusių pro amerikietiškų režimų.

Trečia, Rusija ir Kinija idealiai papildo viena kitą. Kinijos ekonominė galia stiprina Rusiją, o karinė Rusijos galia stiprina Kiniją.

Ketvirtą. Maskvai tapo pozityviu kinų atėjimas į RF artimojo užsienio regionus. Toks sudėtingas ir probleminis regionas, kaip Centrinė Azija, Rusijos saugumui gresia kur kas mažiau, negu Rytų Europa, kadangi ten daug daugiau Kinijos, daug mažiaus Amerikos ir beveik nėra Europos.

Penktą, jau keletą metų Kinija aktyviai juda į Rytų Europą ir susiduria su tokiomis pačiomis problemomis, kaip ir Maskva. Pavyzdžiui, jos kelyje papuolė tokia maža ir labai pikta šalis, kaip Lietuva, kuri, dėl to, kad atkreipti į save JAV dėmesį, surengė parodomąjį Pekino aplojimą. Tai yra, Kinijos atžvilgiu užsiėmė tuo pačiu, kuo ankstesniais metais ir užsiiminėjo Rusijos atžvilgiu.

Kinija į lietuvišką nedraugiškumą sureagavo nepalyginamai griežčiau nei Rusija. Tam jog sutramdyti Vilnių, ji per pusę metų padarė daugiau nei Rusija per 30 metų. Faktiškas diplomatinių santykių su Lietuva nutraukimas ir sisteminis lietuviškos produkcijos eksporto į Kiniją ir Kinijos produkcijos importo į Lietuvą trikdymas. Grasinimai užsienio kompanijoms neleisti jų Kinijos rinką, jei jos turės reikalų su Lietuva.

Šiandieną tik Kaliningrado faktorius neleidžia Rusijai reaguoti į Lietuvos priešiškumą griežtais kinų metodais. Tačiau Lietuva daro viską kas galimą, kad šis faktorius būtų įveiktas, savo rusofobija stimuliuodama Maskvą investuoti į strateginę Kaliningrado srities autonomiją.

Kai tik šis procesas pasieks savo finalinę stadiją, ir Kaliningrado sritis taps visiškai nepažeidžiama tokio nenormalaus kaimyno, kaip Lietuvos Respublika, pastarajai bus nelengva.

Ir tada Lietuvos politikams nebeliks laiko skųstis Vašingtonui. Geriau iš karto pulti į Vilniaus oro uostą ir skristi iš Lietuvos kur akys mato.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 5 — id: `scraped:rubaltic_lt:ec2b123c27ad6a5a`

**Title:** Be elektros energijos iš Rusijos Pabaltijyje sustoja gamyba

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Stambi celiuliozės gamykla Estonian Cell Kundos mieste visiškai nutraukė gamybą. Kompanijos vadovybės žodžiais, jos produkcija eksporto rinkose tampa nekonkurencinga dėl nepakeliamai aukštų elektros energijos kainų. Tokiu būdu, Estijoje atsirado pirmas pramonės objektas, kuris neišlaikė energetinės krizės išbandymų. Už tai daugeliu yra atsakinga Lietuva, kuri neleidžia kitoms Baltijos šalims didinti elektros energijos tiekimą iš Rusijos.

Pabaltijo respublikos atsidūrė pagrindinių energetinės krizės, kuri siaučia Europoje, aukų rate. RuBaltic.Ru analitikos portalas jau rašė, jog nuo Naujųjų metų dujų kaina Estijos namų ūkiui sudarys 1,27 euro už kubinį metrą – tai beveik du kartus daugiau, nei dabar.

Elektros energijos rinkoje situacija ne ką geresnė. Lapkričio pabaigoje tarifas estų vartotojams Nord Pool biržoje šoktelėjo iki 421 euro už megavatvalandę, o gruodžio 7 ryte pasiekė beprotišką 1000 eurų ribą.

Tokia pati bėda apėmė Suomiją, kuri kaltina Lietuvą, Latviją ir Estiją energetikos rinkos iškreipimu. „Baltijos šalys akivaizdžiai nebenori importuoti elektros energiją iš Rusijos, ir jų elektrinėse buvo sutrikimai, todėl elektros energija eksportuojama iš Suomijos į Pabaltijį ir regione nusistato rekordinės kainos“, kalbėjo Suomijos elektros tinklų kompanijos-operatoriaus Fingrid direktorius Jukka Ruusunen.

Estų garbei, jie savo klaidą pripažino ir netgi bandė ją ištaisyti.

„Dabar mes galime patvirtinti, jog vakar iš tikrųjų turėjome kontaktus [dėl elektros energijos importo iš RF ir Baltarusijos padidinimo] su mūsų, visų pirmą, Lietuvos, kolegomis, ir tie kontaktai, neabejotinai, artimiausių dienų laikotarpyje bus pakankamai intensyviai tęsiami“, - kalbėjo Elering atstovas Ain Kester.

Jo žodžiais tariant, anksčiau Latvija ir Estija parėmė Lietuvą, sumažindami elektros energijos importą iš Rusijos.

Iš Maskvos atsakė jog yra pasiruošę pagelbėti Pabaltijui. „Rusijos šalis lieka atvira dialogui dėl elektros energijos tiekimo į Baltijos šalis padidinimo. Esančiomis schemų - režimų sąlygomis, atsižvelgiant į fizinį skersmenų pralaidumą, galimas iki 1 gigavatvalandės tiekimas iš Rusijos teritorijos į Baltijos šalis. Rusiškos elektros tiekimas gali būti pradėtas nedelsiant ir maksimaliai galima apimtimi. Be to, siekiant Baltijos šalių įstatymų laikymosi, rusiška šalis išreiškia savo pasirengimą patvirtinti visais būtinais teisiniais būdais išimtinai rusišką tiekiamos elektros energijos kilmę“, - pareiškė l.e.p. „Inter RAO“ trading bloko vadovė Aleksandra Panina.

Pasiruošimas patvirtinti rusišką elektros energijos kilmę – tai reveransas Lietuvai, kuri stengiasi atitverti save ir visą likusią Europą nuo „nesaugios“ BelAE produkcijos. Niekas negali priversti Rusiją dirbti pagal šią sistemą, bet ji sutiko pati. Reikia daugiau elektros energijos? Imkite! Reikalingi kilmės sertifikatai? Mes padarysime!

Estijos ekonomikos ir komunikacijų ministerijos vicekancleris energetikos klausimams Timo Tatar pareiškė, jog Pabaltijui nereikia tikėtis elektros energijos importo iš Rusijos apimčių didėjimo: „Šiuo klausimu nėra rimto persilaužimo. Lietuva analizuoja, ką galima padaryti. Ši problema greitai nesisprendžia“

Nesisprendžia dėl paprastos priežasties, jog viena iš „Pabaltijo seserų“ nenori nieko spręsti. Konkretūs susitarimai, jei tikėti Tataru, geriausiu atveju, pasirodys sekančių metų pradžioje.

Tarp kitko, energetikos krizės padariniai Estijoje jaučiami jau dabar.

„Pavyzdžiui, galima pasiūlyti išdėstymą keliais terminais, sąskaitas išdėstyti ilgesniems periodams, kadangi vasarą sąskaitos mažesnės. Nedaryti staigių judesių, dėl kurių žmonės papuls į sudėtingas situacijas“, - siūlė Kallas.

Bet problemos dėl rekordiškai aukštų elektros energijos kainų kilo ne tik namų ūkiams. Gruodžio 8 sustojo stambi celiuliozės gamykla Estonian Cell Kunda mieste – viena iš progresyviausių ir energijos imliausių Estijos įmonių. Tik lapkrityje kompanijos išlaidos energijos resursams išaugo maždaug 1,5 milijonais eurų, per paskutiniuosius keletą mėnesių apskaičiuotas biudžetas viršytas 5 milijonais.

„Mes neturime galimybių vietinį žaliavos ir resursų kainų padidinimą perdėti vartotojams iš įvairių kontinentų. Todėl mes ieškome sprendimų, kaip susidoroti su ta (norisi tikėti, laikina) krize.(...) Prašome surasti reikalingą šių išlaidų padengimą kvotų (CO2 išmetimo) pardavimo pajamų sąskaita, idant neperdėti krūvį ant kitų vartotojų. Prašome taikyti atitinkamas ES instrukcijoms priemones, kurių taikymas yra išskirtinai svarbus kovoje su energetine krize“,- sakoma Estonian Cell rašte, kuris išsiųstas Estijos premjerui.

Celiuliozės gamyklos problemas dalinai galima nurašyti nepalankių aplinkybių sąskaita. Galu gale tai ne vienintelė įmonė, kuri nukentėjo nuo nepakeliamai aukštų elektros energijos kainų (Europos azotinių trąšų gamintojai pradėjo stabdyti gamybą dar rugsėjo mėnesį).

Iš karto, tik paleidus gamybą, vykdomasis Estonian Cell direktorius Margus Kochava suabejojo projekto atsiperkamumu, kadangi išlaidos pasirodė daug didesnės nei tai buvo numatyta biznio plane. „Mes supratome taip, jog sutartyje užfiksuota kaina įskaito visus išlaidų komponentus, bet vėliaus paaiškėjo, jos joje neįskaičiuotas elektros energijos perdavimo apmokėjimas“, - sakė Kochava.

Kompanijos vadovybei elektra tapo galvos skausmu. Dėl per daug didelių gamybinių išlaidų Estonian Cell kasmet ėjo “į minusą”. Dveji iš jos pirminių investorių – Europos rekonstrukcijos ir plėtros bankas (ERPB) ir Larvik Cell iš projekto pasitraukė, jų akcijas supirko Heinzel Group.

„Pačioje pradžioje mūsų investoriams buvo duoti trys pažadai. Visų pirma, jog Estijoje yra žymūs miško resursai, ir tai iš tikrųjų taip. Antra, Estijoje yra konkurencinga ir kvalifikuota darbo jėga, ji taip pat yra. Trečias pažadas, jog Estijoje konkurencinga elektros energijos kaina, neišpildytas“, - konstatavo Estonian Cell valdybos narys ir finansų direktorius Sijri Lache.

Kiek vėliau kompanija nusprendė pastatyti naują celiuliozės kombinatą. Bet ne Estijoje. „Gamyklą buvo galima pastatyti ir Kundos mieste, greta jau turimos įmonės, tačiau, buvo nuspręsta investuoti Austrijoje, nežiūrint į tai, jog darbo jėga ten yra žymiai brangesnė“, - kalbėjo Lache. – Taip buvo nuspręsta dėl kaitaliojančiosios Estijos ekonominės politikos ir aukštų energetinių išlaidų“.

Estonian Cell pavyzdys akivaizdžiai demonstruoja, jog energetinė krizė Pabaltijyje tik apnuogino tas problemas, kurios egzistavo ir anksčiau.

Nauji pramonės objektai šioje teritorijoje nuo pat savo starto pereina į išgyvenimo režimą. Ir griūna pirmieji, kai tik sugriežtėja sąlygos.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 6 — id: `scraped:rubaltic_lt:5e4c0a077e3d7fd5`

**Title:** Rekordinės dujų kainos provokuoja ekonominę krizę Pabaltijyje

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvoje, Latvijoje ir Estijoje šildymo kainos pasiekė rekordines aukštumas. Mokėti už komunalines paslaugas namų ūkiai negali. Dėl to, jog apmokėti šildymą Pabaltijo gyventojai pasiruošę viskuo naudotis taupiai. Toks elgesys gresia Pabaltijo šalių ekonomikos vartojimo modelio griuvumu ir naujos ekonominės krizės atsiradimu.

Vilniaus gyventojams šildymo kaina pakilo du kartus. Dviejų kambarių buto Lietuvos sostinėje gyventojai, pavyzdžiui, lapkričio mėnesį už šildymą turės užmokėti 84 eurus. Tai 214 % daugiau nei prieš metus.

Kituose Pabaltijo respublikose situacija taip pat kritiška. Latvijoje su siaubu laukia gruodžio mėnesio mokėjimų.

Namų ūkiai, kurie sunaudoja nuo 250 iki 500 kubinių metrų dujų, už dujas mokės apie vieną eurą už kubinį metrą. Namų ūkiams, kurie sunaudoja daugiau nei 500 kubų, kaina pakils iki 0,80 euro už kubinį metrą – praktiškai dvigubai.

Estijoje dabar privatiems vartotojams dujos kainuoja 0,66 euro už kubą, o nuo Naujų metų kainuos 1,27 euro už kubinį metrą. Ir vėl, beveik dvigubas didėjimas.

Palyginimui ir supratimui: Maskvoje vienas kubinis metras dujų, perskaičiavus į bendrąją Europos valiutą, kainuoja 0,08 euro.

RuBaltic.Ru analitikos portalas jau rašė, jog rekordinės dujų kainos Pabaltijyje iššaukia komunalinius maištus.

Priežastinis-pasekminis ryšis čia labai paprastas. Lietuviai, latviai ir estai jau įjungia griežtos ekonomijos režimą, idant išlaikyti nepakeliamą komunalinių mokesčių naštą. Remiantis socialine apklausa, 40% Lietuvos gyventojų, 57% Latvijos gyventojų ir 65% Estijos gyventojų tam, kad apmokėti komunalines paslaugas, yra pasiruošę sumažinti visas likusiai savo išlaidas. Po Naujųjų metų, kai tarifai šoktels dar aukščiau, padidės ir ekonomijos šalininkų išlaidos.

Kaip tai atsilieps ekonomikai? Tiesiogiai. Pastovietiško Pabaltijo ekonomika pagristas paslaugų sritimi. Paslaugos sudaro daugiau nei pusę Lietuvos, Latvijos ir Estijos BVP.

Tokio ekonomikos modelio funkcionavimas pagristas vidaus vartojimu. Gyventojų vartojimas – tai kuras, kuriuo veikia ekonomika. Pabaltijyje jo aktyvumas stimuliuojamas įvairiais būdais, įskaitant ir ne rinkos būdus: Europos Sąjungos dotacijos, darbo migrantų uždarbių pervedimai pasilikusioms gimtinėje šeimoms.

Po to jau nebebus svarbu, dėl ko Pabaltijyje kilo masiniai protestai: dėl kosminių dujų ir šilumos tarifų ar dėl ekonominės krizės, kilusios dėl situacijos komunalinių paslaugų rinkoje. Bet kokiu atveju priežastis viena – strategiškai klaidinga Pabaltijo vadovybių energetinė politika, kurios jos pusantro dešimtmečio ne tik laikėsi savo šalyse, bet ir bruko visai Europos Sąjungai.

„Priminsiu, jog kol pirmenybė buvo teikiama atominei ir dujiniai generacijai, panašių krizių nebuvo. Joms nebuvo iš kur imtis. Papildysiu, jog Rusijoje dabar tokių problemų, paprasčiausiai, ačiū Dievui, neįmanoma netgi įsivaizduoti. Ilgalaikis požiūris į kuro energetikos kompleksą mums leidžia užtikrinti gyventojams ir įmonėms pačio žemiausio lygio kainas Europoje. Vidutinė elektros energijos kaina Rusijoje, perskaičiavus eurais, sudaro apie 20 už MW/h. Lietuvoje – 256 eurai, Vokietijoje ir Prancūzijoje – 300 eurų, Didžiojoje Britanijoje – 320“,- rudenį tokią politiką apibudino Rusijos prezidentas Vladimiras Putinas.

Pabaltijyje atominę energetika likvidavo, dujų energetikoje daugelį metų buvo griaunamos bet kokios konstruktyvinio bendradarbiavimo su Rusija galimybės, ir normaliems santykiams su „Gazpromu“ pirmenybę teikė kvailiems ir beveik užmirštiems SGD terminalams.

Vietoje stabilių bei patikimų pigios energijos šaltinių Pabaltijo politikai pirmenybę teikė rinkoje pačioms brangiausioms ir kartu su tuo krizės metu t nenaudingoms technologijoms, kaip tai biokuras ir „žalioji energija“, o iš BRELL (Baltarusija-Rusija-Estija-Latvija-Lietuva) energetikos žiedo, kuris dabar gelbėja Pabaltijį, nežiūrint į visus protingus samprotavimus, nori išeiti.

Ši energetinė krizė yra pagimdyta tomis dogmomis, kurias Pabaltijo politikai metai iš metų gynė energetikos srityje. Krizinė situacija rinkoje pademonstravo, jog dogmos nėra adekvačios realybei. Ir dabar ateina laikas už tai atsakyti.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 7 — id: `scraped:rubaltic_lt:f1c8bb01e3e5150b`

**Title:** Kinija pasuko Lietuvos ekonominio smaugimo kryptimi

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Priešiška Kinijos atžvilgiu Lietuvos politika sukelia vis daugiau problemų lietuviškam verslui. Kaip ir pas Lietuvos eksportuotojus, problemos atsirado ir pas Lietuvos importuotojus: verslininkai skundžiasi, jog negali gauti Kinijoje užsakytų prekių. Lietuvos politikai skundžiasi, jog Pekinas grasina neleisti į kinų rinką bet kokias užsienio kompanijas, kurios bendradarbiaus su Lietuva. Akivaizdu, kad KLR rimtai ėmėsi Vilniaus ir priešiškiems Lietuvos veiksmams atsako savo demonstratyviais veiksmais, kurių esmė – ekonomiškai sunaikinti šunelį, kuris išdrįso amsėti ant Padangių šalies.

„Dirbančios logistikos sferoje Lietuvos kompanijos, kurios visada vežė krovinius per Klaipėdą, mane nustebino – prieš dvejas savaites atsiuntė pasiūlymą vežti per Rygos uostą. Aš dabar supratau, kodėl. Mes tik šiandien rytą sužinojome, jog kiti jau seniai taip planuoja. Aš baiminuosi kamšaties Rygoje, neaišku, kas bus, jei visa Lietuva važiuos per Rygą“, - kalba Lietuvos verslininkas, kuri 20 metų vežą kinų prekes į Lietuvą.

Rygos uosto pasirinkimas yra susijęs su tuo, jog vežėjai bijo nurodyti prekių paskirties šalį Lietuvą: kinų muitinė, pastebėjusi, jog KLR produkcija skiriama Lietuvai, nieko neaiškindami sulaiko krovinį ant sienos.

„Reikia pradėti kalbėtis dėl pavasario sezono, vakar kaip tik apmokėjome depozitą – 10 tūkst. dolerių už vieną konteinerį. Kitą planavome vėliau apmokėti. Bet sulaukėme žinios: „Po patikrinimo su logistikos kompanija apie prekių siuntimą mes negalime pabaigti muitinės deklaracijos. Negalime prekių išsiųsti į Lietuvą dabar, informuosime, kai situacija pagerės“, - skundžiasi verslininkas. Prieš porą savaičių Lietuvos kompanijos susidūrė su daug rimtesne problema. Lietuva staiga prapuolė iš kinų muitinio apiforminimo sistemos. Tokia šalis buvo – ir daugiau jos nebėra. Atitinkamai, kaip galima vežti į Kinijos liaudies respubliką produkciją, kuri pagaminta neegzistuojančioje šalyje.

Tada problema išsisprendė per keletą dienų. Lietuva grižo į KLR muitinės registrą taip pat netikėtai, kaip ir buvo prapuolusi. Kodėl prapuolė, kodėl, kodėl sugražino – dėl to kinai nieko nepaaiškino. Jų muitinis registras – jų reikalas. Kaip ištrynė, taip ir įrašė. Kaip įrašė, taip ir vėl ištrins.

Tarp kitko, niekas neklausė, kodėl Lietuvos verslininkams prasidėjo problemos su kinų muitine. Visiems ir taip aišku.

Lietuvos verslą kankina pastovios problemos su Kinija nuo to meto, kai galutinai buvo suformuotas priešiškas KLR Vilniaus kursas.

Dar vasarą Lietuvos gamintojai pradėjo skųstis, jog bendradarbiavimas su kinų partneriais tampa vis sudėtingesnis. Kinai nepasirašo kontraktų su lietuviais, nenori pirkti jų produkcijos. Jie supranta, jog turi reikalų su nedraugiškos KLR valstybės piliečiais, o Kinijoje tai nėra sveikintina.

Lietuvos ištrynimą iš KLR muitinio apiforminimo sistemos galima skaityti kaip „paskutinįjį kinų perspėjimą“ Vilniui. Peržiūrėkite savo politiką mūsų šalies atžvilgiu, kitaip sekantį kartą Lietuva į Kinijos liaudies respublikos muitinės registrą jau nebebus sugražinta.

Skaidrią kinų užuominą Vilniuje ignoravo. Po sugražinimo į KLR muitinės sistemą Lietuva paskelbė apie diplomatinį Olimpiados Pekinę boikotą.

Ir štai jau Lietuvos politikai skundžiasi jog Pekinas grasina neleisti į kinų rinką bet kokias užsienio kompanijas, kurios bendradarbiaus su Lietuva.

„ [Kinija] siunčia transnacionalinėm kompanijom pranešimus apie tai, jog jeigu jos naudos komplektuojančias dalis ir medžiagas iš Lietuvos, tai daugiau negalės parduoti prekių kinų rinkoje“, - sakė užsienio reikalų viceministras Mantas Adomėnas. Ar gali Pekinas iš tikrųjų užkirsti kelią į pačią didžiausią pasaulyje rinką kompanijoms, kurios bendradarbiauja su Lietuva. investuoja į Lietuvą? Atsakant į tai reikia suprasti, jog Kinija jau ir taip žengė daug toliau, negu iš jos buvo laukiama, ir pas ją yra priežasčių nesustoti.

Vilnius pasiekė tai, jog Lietuvos – Kinijos santykiai tampa įdėmaus tarptautinio dėmesio objektu. Jų vystymąsi seka Amerikoje, Europoje, Rusijoje, Azijoje ir taip toliau iki pat Australijos ir Okeanijos. Šiame konflikte, bendrai pasakius, visiems nusispjauti į Lietuvą, kuri pati nieko nereiškia, o dar ir elgiasi standartiškai. Visus domina Kinija, kuri dabartiniu metu aktyviai ateina į pasaulį, ir kurią visi stebi, kaip ji elgsis.

Dispozicija tokia. Yra mažas, bet piktingas rytų europietiškas šunelis, kuris per 30 metų politikoje specializavosi nebaudžiamai aploti kitus, idant atkreipti vakarų sąjungininkų-globėjų dėmesį į save ir gauti jų paramą. Atvejyje su Kinija Lietuvos valdžia jau neslepia, jog amsėti ant jos su Taivano palaikymu ir „uigūrų genocidu“ pradėjo dėl to, kad gražinti Lietuvai JAV dėmesį.

Ir yra šalis, turinti naujojo globalinio lyderio potencialą, iš kurios laukiama, kokias tarptautinės politikos taisykles pasiūlys ta šalis.

J ei konfliktą su Lietuva dabar seka visas pasaulis, tai Pekinas suinteresuotas pademonstruoti visiems, jog nenubaudžiamai amsėti ant Padangių šalies niekam nėra leista, ir kiekvienas, kuris savo politikoje pasirinks priešiškumą Kinijai – dėl to stipriai pasigailės.

Todėl lietuvius muš. Atsargiai bet stipriai. „Kaip aš suprantu, Lietuvą nusprendė paversti į pavyzdinę bokso kriaušę, kaip šalį, kurios negaila ir su kuria galima ramiai nutraukti bet kokius santykius“, - rašo rusų Kinijos žinovas, Aukštosios ekonomikos mokyklos Kompleksinių europietiškų ir tarptautinių tyrimo centro direktorius (KETTC) Vasilij Kašin.

Taip kad dabar Vilniui pačios radikaliausios prognozės nebus neįmanomos. Lietuvos pavertimas tarptautiniams investoriams tabu zona, lietuviškos produkcijos paklausos tarptautinėje rinkoje degradavimas, Lietuvos verslininkų pavertimas nepageidaujamais partneriais užsienio ekonominėje veikloje.

Pas Kiniją pakanka resursų ir pasaulinės įtakos, idant užsmaugti Lietuvą ekonomiškai, ir tam ji yra pakankamai stimuliuotą.

Vilniuje netgi dabar iki galo nesupranta ant ko jie užšoko, kai iš įpročio pabandė truputi paloti.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 8 — id: `scraped:rubaltic_lt:f611adbc3846f91f`

**Title:** Rusofobai iš Lenkijos ir Lietuvos agituoja Kazachstaną  „pjauti rusus“

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Kolektyvinio saugumo sutarties organizacijos (KSSO) taikdarių pajėgų įvedimą į Kazachstaną lydi masinė informacinė kompanija, kurios tikslas – išprovokuoti kazachus su ginklu pasipriešinti „rusų okupantams“. Šioje srityje aktyviausiai veikia lenkų Telegram – kanalas NEXTA Live, bet ne tik jis vienas. Provokatorių pastangas remia ir ukrainiečių nacionalistai, ir rusų „liberalai“ – nuolatiniai Laisvos Rusijos forumo Lietuvoje dalyviai.

2020 metais Telegram–kanalas NEXTA Live koordinavo masinį pasipriešinimą Baltarusijos prezidentui Aleksandrui Lukašenkai.   Baltarusijoje revoliucija neįvyko, tačiau įtakojimo infrastruktūra išliko: iki šio laiko prie NEXTA Live yra prisijungę daugiau nei 800 tūkstančių žmonių. Nesišvaistyti gi gėriu!

Kanalo administratoriai pareiškė, jog neleis „ramiai miegoti nei vienam postsovietinės erdvės diktatoriui“, ir pradėjo štampuoti naujienas apie įvykius Kazachstane.

Žmones, kurie išplėšė Nacionalinio saugumo komiteto (NSK) ginklų sandėlius Kazachstane, NEXTA vadina protestuojančiais. Ir dargi leidžia sau sarkastiškai pastebėti: „Vakar protestuojantys iš pajėgų struktūrų pasiėmė techniką ir ginklus. Įdomu, ar ginklų sandėliuose iš viso kas tai liks iki kol atvyks KSSO pajėgos?“

Teisėsaugos pareigūno žiauraus sumušimo kadrus NEXTA palydi pagiežingais komentarais: „Pasirodo nauji kadrai, kurie demonstruoja liaudies meilę Nazarbajevo pajėgų pareigūnams“.

Cituojame kai kuriuos punktus:

„1. Grupuokitės greta žmonių, kurie turi kovinę patirtį. Tarnaujantys pagal kontraktą kareiviai, kariavę Afganistane, taikdariai – nesvarbu. Tai žmonės, kurie dalyvavo koviniuose veiksmuose ir yra atitinkamai pasiruošti, jie sugebės vadovauti jūsų kovos su grobikais veiksmams. Grupėje turi būti maždaug 10-20 žmonių.

2. Veikite laikydamiesi taisyklės „įkask ir bėk“ – jei priešas yra pranašesnis už jus, pasistenkite padaryti jam kuo daugiau žalos ir pasitraukti su minimalia žala sau.

(…)

7. Maksimaliai apsiginkluokite. Jei jūs nemokate šaudyti, gaminkite kokteilius ir meskite juos pro langus ir iš karto palikite poziciją“.

Kokiu būdu jūs patarsite į tai reaguoti eiliniams kazachui, kuris išėjo į mitingą protestuodamas prieš staigų suskystintų dujų pabrangimą? Pasirodo, jam būtina dalyvauti koviniuose veiksmuose, mėtyti granatas, nuvarinėti policijos automobilius...

Kiek vėliau NEXTA nurodo kazacham naują „priešą“: Rusų kareiviai išskrido į Kazachstaną. Jei jie galvoja, jog ten juos sutiks su tuščiomis rankomis, tai jie labai klysta. Kazachai svetinga tauta, vietos stepėje užteks visiems“.

Ar galima panašų pareiškimą vertinti kaip raginimą užmušinėti rusų karius? Suprantama, taip.

Dar viena ryški provokacija – taip vadinamo „Kazachstano išlaisvinimo fronto“ įkūrimas. Interneto tinkle jau keletą dienų aptariamas vaizdo įrašas, kur ginkluoti žmonės kviečia kazachus atremti, atstovaujamus KSSO pajėgomis, „okupantus“. (dabartiniu metu vaizdo įrašas pašalintas iš Youtube už bendrijos taisyklių pažeidimą).

„Kareiviai ir karininkai, šiandieną Kazachstano nepriklausomybė priklauso nuo jūsų. Prezidentas Tokajevas jau pažeidė konstituciją, sutrypė visas laisves, ruošia mūsų šalies suverenitetą atiduoti į Maskvos rankas, kaip tai daro Lukašenka su Baltarusija ir bandė padaryti Janukovičius su Ukraina. Tik nuo jūsų patriotinio sąmoningumo priklauso mūsų valstybės gyvavimas. Pereikite į revoliucinių jėgų pusę! Kartu mes nuversime režimą, įgyvendinsime teisingumą ir ryžtingai pasipriešinsime okupantams. Mes esame apsiginklavę ir pasirengę ištrenkti KSSO pajėgas iš mūsų šalies“, - kalba persirengėlis kovotojas su Rusija.

Leidinio „Strana“ informacijos šaltinių duomenimis, vaizdo įrašą paruošė Ukrainos nacionalistai iš Dmitrij Korčinskij aplinkos – skandalingai žinomo Maidano „kurstytojo“ ir karo Donbase dalyvio (RF Tyrimo komitetas įkaltina jį parama čečėnų separatistams 1994 – 1995 m.). Įdomu, jog pirmasis vaizdo įrašą paviešino Yuotube-kanalas HotNews, prie kurio prisijungę vos daugiau nei vienas šimtas žmonių. Anksčiau jis viešino provokacinius vaizdo įrašus Armėnijos-Azerbaidžano konflikto tema.

Šių eilučių autorius puikiai žino, jog būtent tokios rusų šnektos ypatybės yra būdingos Rytų Ukrainos gyventojams – Charkovo, Odesos, Dnepropetrovsko ir taip toliau.

Tarp kitko, provokuoti ginkluotą konfliktą Kazachstano teritorijoje ėmėsi ne tik Telegram-kanalai bei anoniminiai ukrainiečių nacionalistai. Visiškai atvirai tai daro kai kurie Rusijos liberalios inteligentijos atstovai.

Pavyzdžiui, štai kaip tai aiškina istorikas-opozicionierius Andrėjus Zubovas: „Kai Tokajevas suprato, jog visi jėgos struktūrų pareigūnai arba pasislėpė arba išstojo prieš jį, jis, Putino džiaugsmui, atsisakęs savo gudrių ketinimų tapti naujuoju Li Kuan Ju, kreipėsi į Kremlių. Ir Kremlius, savo bėdai, atsakė į šį reveransą pasiusdamas kariuomenę. Dabar į kazachus šaudys rusai. Ir tai sukels visų pasipiktinimą – ir išsilavinusių vakariečių, ir kultūringų kazachų patriotų, ir pačių tamsiausių islamo fundamentalistų“.

http://www.facebook.com/andrei.b.zubov/posts/3189763857975610

Ir dėl ko rusams šaudyti į kazachus? Šios medžiagos rengimo momentu jau buvo aišku, Kazachstano teisėsaugininkai savo šalyje savarankiškai užbaigs, nukreiptą prieš terorizmą operaciją. Tačiau ne tokios pabaigos tikėjosi Rusijos kovotojai „už demokratiją“.

„Aš esu gimęs Kazachstane ir galiu pasakyti: ne maišykite kazachus su baltarusiais“ – kaip reikalo žinovas, rašo buvęs RF vicepremjeras, dabar, kaip ir Zubovas, nuolatinis Laisvos Rusijos forumo Lietuvoje dalyvis Alfredas Kochas. – Tai visiškai kita tauta su kitais papročiais bei kitu mentalitetu. Prieš automato žiotis jie nesudės rankų plaštakų širdele ir nedovanos gėlių musorams. Ir jau tikrai, priekyje savęs negins bobų. Pasižiūrėkite kroniką iš Kazachstano: ten protestuojančių kolonose beveik nėra moterų. Tie žmonės eina ne į demonstraciją, o į karą“.

Visas „džentelmeniškas rinkinys“: policijos pareigūnus jis vadina „musorais“, moteris – „bobomis“, o baltarusius tautų hierarchijoje stato žemiau kazachų.

Visus demonstrantus Kochas priskyrė prie žmonių, kurie eina į karą. Kas tai, jei ne raginimas imtis prievartos?

Absoliučiai nepatenkintų Kazachstano gyventojų daugumai pakako proto nesuklausyti tokių raginimų.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 9 — id: `scraped:rubaltic_lt:955ac971f6bef2f4`

**Title:** Dar viena šunybė Kinijai: Lietuva prisijungia prie Olimpiados Pekine boikoto

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuva parėmė žiemos Olimpiados Pekine diplomatinį boikotą, kurį organizavo Jungtinės Valstijos. Aplankyti Kiniją atsisakė Pabaltijo respublikos prezidentas Gitanas Nausėda, užsienio reikalų ministras Gabrielius Landsbergis, švietimo, mokslo ir sporto ministrė Jurgita Šiugždinienė. Bet tai nereiškia, jog Olimpinių žaidynių atidarymo ceremonijoje nebus nei vieno politiko iš Lietuvos – opozicijoje esantys socialdemokratai gali laisvai patys nuvykti į Pekiną.

Gruodžio mėnesio 9 d. duomenimis Olimpinėms žaidynėms Pekine diplomatinį boikotą jau paskelbė keletas valstybių. Viso proceso avangarde Jungtinės Valstijos: Baltieji Rūmai nesiruošia siusti į Kiniją oficialią delegaciją ir žada savo sportininkus remti nuotoliniu būdu. Amerikiečius palaikė Australija, Naujoji Zelandija, Kanada ir Didžioji Britanija.

Likę Vašingtono sąjungininkai arba vis dar galvoja arba jau atsimojo nuo boikoto. Prancūzijos liaudies švietimo ministras Žan Mišel Blanker pareiškė, jog jo šalis Pekine bus atstovaujama ir sportiniame ir diplomatiniame lygyje. Remiantis televizijos kanalo RaiNews24, analogiškai suveiks Roma (Italijos Nacionalinio olimpinio komiteto prezidentas Džovani Malago anksčiau buvo nusistatęs prieš Olimpinių žaidynių boikotą). Vokiečiai ir japonai kol kas susilaiko nuo komentarų.

Apie ateinančių Olimpinių žaidynių boikotą čia buvo galvojama dar praeitą mėnesį.

„Mes kreipėmės į prezidentą, vyriausybę ir į visus Lietuvos politikus su kvietimu boikotuoti Olimpines žaidynes Kinijoje, nedalyvauti jos atidarymo ir uždarymo ceremonijoje, nesiųsti ten oficialias valstybinės delegacijas“.,- sakoma keleto Lietuvos Seimo valdančiosios koalicijos deputatų paruoštoje peticijoje.

Dar daugiau, kvietė sportininkus „pademonstruoti pilietinę poziciją, nedalyvauti varžybose ten, kur juos bando paversti autoritarinio režimo surežisuoto spektaklio marionetėmis“.

Atsakydamas į tai Lietuvos užsienio reikalų ministras Gabrielius Landsbergis pasakė, jog pasikonsultuos su kolegomis iš JAV ir Europos Sąjungos, ar tikslinga vykti į Olimpines žaidynes. „Tiesą sakant, aš nematau diplomatų ir oficialių asmenų eilės, kad vykti... Aš nemanau, jog Pekinas taip pat nori mus priimti“. – sakė Landsbergis.

Asmeniškai pats Si Dzinpinas organizuoja pasitarimus šia tema...

Galu gale paskelbti boikotą žaidynėms Kinijoje Lietuva nesugebėjo. Valdančiųjų konservatorių iniciatyvos neparėmė Respublikos Nacionalinis olimpinis komitetas. „Sportininko karjera neilga, Olimpinės žaidynės – pačios svarbiausios rungtynės jo gyvenime, kurioms ruošiamasi ne vienerius ir ne ketverius metus, o daug ilgiau. Todėl mes nemanome, jog būtu teisinga prašyti sportininkų atsisakyti šios galimybės dėl politinių priežasčių“. – sakoma komiteto pranešime.

Po to švietimo, mokslo ir sporto ministrė Jurgita Šiugždienė patvirtino, jog Lietuvos sportininkai, kurie išsikovojo teisę atstovauti šalį Olimpinėse žaidynėse, būtinai vyks į Kiniją. Bet politikai pasiliks namie.

Pati Šiugždienė apsilankyti sporto šventėje neketina, su ja sutinka Landsbergis ir Lietuvos prezidentas Gitanas Nausėda. Čia jokių valstybės vadovo ir vyriausybės prieštaravimų nėra.

Tai, tarp kitko, nereiškia, jog Pekine Lietuvą niekas neatstovaus politiniame lygyje. Valdančiųjų konservatorių opozicijos gretose randasi socialdemokratai, kurie demonstratyviai gailisi dėl sugadintų santykių su Kinija. Apie tai jie asmeniškai pasakė KLR reikalų patikėtiniui Lietuvoje Ciui Baichua.

„Olimpinės žaidynės – tai viso pasaulio ir viso olimpinio judėjimo įvykis, todėl iš sportininkų, kurie daugelį metų ruošėsi olimpiniams startams, negalima atiimti galimybės jame dalyvauti, galimybės kuri atsiranda tik vieną kartą jų sportinės karjeros metu“, -pasakė buvęs Pabaltijo respublikos premjeras Algirdas Butkevičius.

Kodėl gi Lietuvos socialdemokratams neatvykti į Olimpinių žaidynių atidarymo ceremoniją. Tam prisieis turėti išlaidų (valstybės biudžetas, suprantama, tokią kelionę neapmokės). Bet valdančioji partija gaus skausmingą antausį.

Jaunesniajam Landsbergiui – liks tik guosti save tuo, jog jo audringa, nukreipta prieš Kinija, politika neliko nepastebėta užsienyje. Leidinys Politico Lietuvos užsienio reikalų ministrą įtraukė pačių įtakingiausių žmonių Europoje sąrašą (kartu su Europos komisijos vadove Ursula fon der Lyayen, Prancūzijos prezidentu Emanueliu Makronu ir kitais).

„Lietuvos užsienio reikalų ministras savo Baltijos respubliką nukreipė į susivaidijimo su Pekinu kursą ir ne demonstruoja jokių sulėtėjimo požymių. Iš karto, tik pradėjęs eiti pareigas, 2020 metų gruodyje, jis paskelbė, jog Lietuva nedalyvaus taip vadinamoje diplomatijos platformoje „17+1“, kurią Kinija išnaudoja bendradarbiavimui su Centrinės ir Rytų Europos šalimis. Netrukus Lietuva supykdė Pekiną, leisdama Taivanui atidaryti savo atstovybę Vilniuje“, -rašo Politico.

Olimpinių žaidynių Pekine boikoto istorija akivaizdžiai rodo, kuo Baltarusija skiriasi nuo Pabaltijo. Šiais metais iš „paskutinio Europos diktatoriaus“ buvo atimta teisė organizuoti pasaulio čempionato ledo rutulio mačus ir turnyrą atidavė Latvijai. Ko ne priežastis boikotuoti? Bet Baltarusijos ledo rutulininkai visgi nuvyko į varžybas.

„Mes ne kartą kalbėjome, jog išsiaiškinti kas stipresnis esame linkę sporto aikštelėse“, - pasakė Baltarusijos Respublikos Ledo rutulio federacija.

Turnyro įkarštyje Rygos meras miesto centre demonstratyviai nuplėšė BR vėliavą ir pakeitė ją baltu-raudonu-baltu audeklu. Po to pradėjo plėstis gandai, jog Baltarusijos ledo rutulininkai protestuodami pirma laiko paliks čempionatą. Bet jie ramiai tęsė savo dalyvavimą varžybose.

Baisu pagalvoti kokia isterija sukeltu Lietuva, jei ji atsidurtu tokioje situacijoje...

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 10 — id: `scraped:rubaltic_lt:0d18e89685e83eab`

**Title:** Lietuvos vyriausybė griūna dėl skandalo su „Belaruskalij“

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos užsienio reikalų ministras Gabrielius Landsbergis pareiškė jog yra pasiruošęs atsistatydinti, jei valstybinei geležinkelio kompanijai iš tikrųjų iš anksto buvo apmokėta už baltarusių trąšų tranzitą po gruodžio 8 dienos. Savanoriškai palikti savo pareigas taip pat ruošiasi ir susisiekimo ministras Marius Skuodis. Abu politikai mano, jog Lietuva apsigėdijo prieš visą pasaulį, kadangi nesugebėjo įgyvendinti amerikiečių sankcijų.

Gruodžio 8 oficialiai baigėsi JAV finansų ministerijos išduotos savo kompanijoms generalinės licenzijos užbaigti sandorius su „Belaruskalij“ terminas. Lietuvos susisiekimo Ministras Marius Skuodis prognozavo, jog tą dieną jo šalis neteks baltarusiškų trąšų tranzito šalies statuso. Bet vagonai su „diktatorišku“ kaliu ir toliau važiuoja į Klaipėdos uostą. Gruodžio mėnesį „Lietuvos geležinkeliai“ (LG) turi pervežti apie vieną milijoną tonų tokio krovinio –už tai Baltarusija apmokėjo iš anksto.

„Tuo atveju, jei sutartis bus nutraukta, kita šalis gali pareikalauti kompensuoti patirtus nuostolius“, - sakė LG direktorius komunikacijoms Mantas Dubauskas

Tuo pat metu Mantas Bartuška Lietuvos Seime išstojo prieš koalicinės Liberalų partijos deputatus. Tikslios nuostolių dėl kontrakto su „Belariuskalij“ nutraukimo sumos jis nepasakė (tai komercinė paslaptis), bet davė suprasti, jog kalbama apie šimtus milijonų dolerių.

Galima neabejoti, jog teismai su „Belaruskalij“ bus pralošti. Bartuška eilinį kartą atvėrė Polišinelio paslaptį: Lietuva neturi jokio pagrindo sustabdyti baltarusiškų trąšų tranzitą. JAV sankcijos – ne argumentas, kadangi jos liečia tik fizinius ir juridinius amerikiečių asmenis.

„Mums reikalingas teisinis valstybės institucijų sprendimas, kad mes galėtume sustabdyti sutartį su „Belaruskaliu“, Šis klausimas valstybės rankose“,- sakė Bartuška. Bet Marius Skuodis valstybės vardu perkelia iniciatyvą geležinkeliečiams: „Ministras negali įpareigoti „Lietuvos geležinkelių“ padaryti vieną žingsnį – nutraukti sutartį. Galiu pasakyti, bet valdyba geležinkelių už sprendimų pasekmes, finansines pasekmes, galimą žalą, ieškinius – ji prisiima atsakomybę praktiškai asmeniniu turtu“.

Kol valdininkai aiškinosi ką daryti su baltarusiškais kroviniais, Lietuvos užsienio reikalų ministras pribloškė visuomenę savo pareiškimu apie galimą atsistatydinimą. Priežastis – tas pats avansinis „Belaruskalij“ mokėjimas.

„Šiandieną aš pasakiau premjeriai, iš tikrųjų vakar vakare, jog aš esu pasiruošęs atsistatydinti, ir laukiu premjerės sprendimo (...) Aš suprantu kokią žala padaryta Lietuvos reputacijai“, - krimtosi Landsbergis. Jo isteriką palaikė Skuodis. Tiesa, avansiniuose mokėjimuose jis ieško ne Lietuvos gėdos tarptautinėje arenoje požymių, o korupciją.

„Aš nenorėčiau komentuoti konkrečių detalių, iki galo man net nėra žinomi visi niuansai, tik patvirtinu faktą, bet taip, pervedimai nebuvo tipiški ir visiškai kitokie, nei tie, kurie ėjo visą sutarties laiką. Kitaip sakant, čia buvo avansuojama toli į priekį“, - kalbėjo Skuodis.

Jo galvoseną suprasti nesunku: „Belaruskalij“ specialiai padidino išankstinio mokėjimo sumą, kad po gruodžio 8 LG negalėtų sustabdyti tranzitą. Tikėtina, jog šis sandoris taps specialios vyriausybinės komisijos patikrinimo objektu, o Bartuškai gali iškelti baudžiamąją bylą.

Bet kokiu atveju Skuodis taip pat pasiruošęs palikti Transporto ministerijos vadovo postą. „Ryte aš informavau premjerę, jog esu pasiruošęs prisiimti atsakomybę, paprasčiausiai nepasisekė įgyvendinti sankcijas“; - kalbėjo ministras.

Gerai pagalvokite: Pabaltijo respublikos ministrų kabineto narys sako, jog jam nepasisekė „įgyvendinti“ JAV sankcijas, kurios jo šalies jokių būdu neliečia! Dėl to jis nori atsistatydinti.

Ir Bartuška, ir Skuodis, ir Landsbergis pripažįsta, joj Lietuvos kompanijos neturi vadovautis Jungtinių Valstijų finansų ministerijos nurodymais. Patys amerikiečiai išaiškino generaliniam LG direktoriui, jog užsienio subjektai ir po gruodžio 8 ramiai gali bendradarbiauti su krovinių siuntėjais iš Baltarusijos.

Tai kodėl lapkričio mėnesį Bartuška negalėjo pritarti avansiniam mokėjimui iš „Belaruskalij“? Galėjo, tam turėjo pilną teisę. Netgi Skuodis to neneigia: „Tai faktas, jog įmonė turi veikti laikydamasi teisės aktų, ir kol kas pas mane nėra kokių tai faktų, kuriais remiantis aš galėčiau pasakyti, jog įmonė pažeidė teisės aktus ar panašiai“.

Bendrai paėmus, niekas nieko nepažeidė. Nebuvo jokio kriminalo. „Lietuvos geležinkeliai“ gabena baltarusiškus krovinius remiantis savo kontraktiniais įsipareigojimais, nacionaliniais įstatymais ir JAV finansų ministerijos rekomendacijomis.

Baisu pasakyti – ji nebuvo solidari su amerikiečiais! Ir visiškai nusispjauti, kad patys amerikiečiai to net neprašė...

Savanoriškas atsistatydinimas, kaip taisyklė, visada rodosi gražiai. Tam ryškus pavyzdys – buvęs Austrijos kancleris Sebastjan Kurt, kuris atsistatydino, atliekamo jo atžvilgiu tyrimo fone. Kažkada vidaus reikalų ministro postą savo noru paliko Saulis Skvernelis. Tai jam padėjo išsaugoti savo reputaciją ir po keleto metų tapti vyriausybės vadovu.

Bet Landsbergis ir Skuodis atsidūrė kitoje padėtyje.

Likę pasuks pirštu prie smilkinio.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 11 — id: `scraped:rubaltic_lt:77716522794f7499`

**Title:** „Mes su Amerika“:  Lietuvos valdžia reikalauja, kad verslas uždarytų baltarusišką tranzitą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Generalinė licenziją, kurią JAV finansų ministerija išdavė savo kompanijoms, idant jos užbaigtų sandorius su „Belaruskalij“, baigiasi gruodžio mėnesio 8 d. Iki šiol neaišku, ar Lietuva vykdys šias sankcijas. Pabaltijo respublikos užsienio reikalų ministras Gabrielius Landsbergis patvirtino, jog Vašingtonas nereikalauja užsienio subjektų nutraukti baltarusiškų trąšų tranzito kontraktus. Bet valdantys konservatoriai vis vien reikalauja tai padaryti, solidarumo su JAV vardan .

Gruodžio mėnesio 8 d. išvakarėse Lietuvos top – valdininkai pasisakė dėl amerikiečių sankcijų „Belaruskaliui“ ir jų taikymo Pabaltijo teritorijoje galimybių.

Pavyzdžiui, susisiekimo ministras Marius Skuodis pažymėjo, jog „dėl JAV sankcijų daug diskutuojama“. Maždaug ta patį pasakė ir vyriausybės vadovė Ingrida Šimonytė.

Į savo išplėstus samprotavimus ji įsigudrino įterpti feiką, į kurį mažai kas atkreipė dėmesį. „JAV sankcijos turi šiokių tokių specifikų, kadangi, skirtingai nuo Europos Sąjungos sankcijų, tų, kurios yra mums įprastos, dėl kurių būna susitariama ES institucijose, yra sankcionuojama įmonė, o ne produktas, ir yra šiokių tokių teisinių niuansų, kuriuos reikia pirmiausia iki galo išsiaiškinti“, – teigė I. Šimonytė.

Tarp kitko, ne visą įmonės produkciją, o tik atskiras jos rūšis (konkrečiai, kalį, kurio sudėtyje naudingos medžiagos yra mažiau 40% ir daugiau 62%). Europos Sąjungos 2021m. birželio mėnesio 24 d. vyriausybiniame biuletenyje galima rasti visą trąšų sąrašą, kurias šalims – bendrijos narėms draudžiama importuoti. Žodis „Belaruskalij“ šiame dokumente nė karto nėra minimas.

O štai JAV sankcijos, atvirkščiai, įvestos konkrečiai „Belaruskaliui“. Iki 2021 m. gruodžio mėnesio 8 d. amerikiečių asmenims duotas laikas užbaigti sandorius su šia įmone.

Europietiškos sankcijos – produktui, amerikiečių sankcijos – kompanijai. O pas Šimonytę kažkodėl tai viskas atvirkščiai.

Su tokiais valstybės pareigūnais - „profesionalais“ Lietuva neprapuls...

Dar vienas „minties gigantas“ – Lietuvos užsienio reikalų ministras Gabrielius Landsbergis – parvirtino, jog „tiesioginės juridinės pareigos įgyvendinti Amerikos sankcijas nekyla“. RuBaltic.Ru analitikos portalas apie tai rašė iš karto po to, kai pradėjo sklisti gandai, jog artimiausiu metu „Belaruskalij“ paliks Klaipėdos uostą.

Situacija galutinai paaiškėjo,kai „Lietuvos geležinkelio“ (LG) generalinis direktorius Mantas Bartuška gavo JAV finansų ministerijos paaiškinimą: „Pokalbio metu mus patikino ir paaiškino, jog esančių sankcijų apimtyje, jei amerikietiški subjektai nedalyvauja tiekimo grandyse, tai sankcijos neveikia“.

Išvertus iš diplomatų kalbos tai reiškia, jog „Belaruskaliui“ ruošią sanatorijos „Belarusj“ Druskininkuose likimą, kuriai anksčiau Europos Sąjunga paskelbė sankcijas. Formalią finansinę šios įstaigos blokadą organizavo švedų Swedbank. Realiais iniciatoriais buvo šalies vadovybė.

O kaip kitaip paaiškinti tą faktą, jog analogiškai baltarusiškai sanatorijai Latvijoje jokių sankcijų nebuvo?

„Mes gi, kreipėmės ir į kitus bankus, domėjomės galimybe juose atidaryti sąskaitas. Tai SEB Bankas, Medicinos Bankas ir kiti. Jie visi atsisakė, nurodydami, jog dėl mūsų situacijos reikia gauti atitinkamų Lietuvos Respublikos valdžios struktūrų išaiškinimus. Situacija neaiški“, - kalbėjo sanatorijos „Belarusj“ vyr. gydytojas Ilja Epifanovas.

Ant jo užpjudys tikrinančias institucijas, organizuos problemas dėl patalpų nuomos, atims svarbius klientus. Ir tada bankas tikriausiai panorės „savanoriškai“ vykdyti amerikietiškas sankcijas.

Nesvarbu apie kokį banką kalbama – norvegų, švedų ar vokiečių. Jo skyrius vis vien veikia Lietuvoje, ir valstybė lengvai gali jį užgniaužti.

„Kiekvienas tiekimo grandinėje dalyvaujantis juridinis subjektas turi apsispręsti, ar jis sudarinės sandorius, ar ne. Iš esmės sankcijų įgyvendinimas priklauso nuo paties subjekto sprendimo“, – sako Landsbergis. Ir Lietuvoje valdantys konservatoriai, žinoma, pagelbės priimti “teisingą” sprendimą. Tai liečia ne tik bankus – dar yra valstybės geležinkelis ir Klaipėdos uostas. Su visais logistinės grandinės, kuria vyksta baltarusiškų trąšų tranzitas, dalyviais URM tikriausiai pakalbės ir viską paaiškins.

„ Stambiausios JAV sankcijos įvedimo nusikalstamam Lukašenkos režimui išvakarėse Seimo užsienio reikalų komiteto nariai balsų dauguma vienareikšmiai pareiškė: mes su Amerika. Mes turime nedelsiant sustabdyti trąšų tranzitą vardan solidarumo su JAV, kuri gina mūsų ir mūsų kaimynų, ir baltarusių laisvę“, - sakė Lietuvos parlamento užsienio reikalų komiteto pirmininkas Žygimantas Pavilionis.

Anekdotiška situacija. Pradžioje Lietuvos susisiekimo ministras paskelbė, jog gruodžio mėnesį baltarusiškų trąšų tranzitas bus sustabdytas. Vėliau paaiškėja, jog nėra jokio teisinio pagrindo tranzito sustabdymui.

Duok Dieve, Amerika išgirs ir atsakys keliais švelniais žodžiais. Paslaugaus pakaliko nereikia nieko prašyti – jis ir pats žino, ko laukia ponas.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 12 — id: `scraped:rubaltic_lt:fa5aa55b3381ee89`

**Title:** Putinas išlošė: Lietuvos mokesčių mokėtojų pinigai buvo išleisti veltui

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos sostinėje įvyko eilinis Laisvos Rusijos forumas, į kurį tradiciškai suvažiuoja nesitaikstantys kovotojai su „Putino režimu“. Šiais metais išskirtiniu šio forumo bruožu tapo „totalinio beviltiškumo“ atmosfera: vietoj to, kad pasakoti apie „puikią ateities Rusiją“, išstojantys kalbėjo apie „diktatūros“ pasiekimus ir siuntė prakeikimus beprincipiams vakarų pasaulio lyderiams. RuBaltic.Ru analitikos portalas surinko pačius ryškiausius Laisvos Rusijos forumo dalyvių pasisakymus.

1. „Putinas gaus tai, apie ką seniai svajoja“

Žinomas politologas, televizijos kanalo „Doždj“ („Lietus“) (Rusijoje pripažintas užsienio agentu) vedantysis Konstantinas Eggertas savo pasisakyme atkreipė dėmesį į „hibridinę ataką“, kurią Maskva ir Minskas, esą, organizavo prieš kolektyvinius Vakarus. Jo nuomone, šį įvykį reikia tinkamai įvertinti. Putinas „zonduoja“ ne tik Europos Sąjungą, bet ir NATO.

„Jis (Šiaurės Atlanto aljansas - RuBaltic.Ru pastaba), žinoma, nesugrius bet atsižvelgiant į tai jog JAV persiorientavo į Kiniją, kokią saugumo koncepcija priims europietiški NATO sąjungininkai, čia neesu įsitikinęs ir neesu optimistiškai nusiteikęs. Čia gali būti patys įvairiausi įvykių variantai, įskaitant ir tai, apie ką ilgą laiką svajojo ir svajoja Putinas – tai, ką dalis politologų vadina „Jalta-2“ – įtakos sferų padalijimą“, - sakė Konstantinas Eggertas.

Galima tik pavydėti žmogui, kuris informuotas apie slaptas Kremliaus šeimininko svajones.

Ar ne laikas Eggertui ir kompanijai pagalvoti apie Laisvosios Kinijos forumą?

2. „Ukraina remia Lukašenkos režimą“

Antri metai iš eilės Laisvos Rusijos forume, kaip nekeista, didelis dėmesys skiriamas Baltarusijai. Bet vilčių, jog artimiausiu metu bus neverstas „paskutinis Europos diktatorius“ šiandien nebeliko. Interneto svetainės „Chartija’97“ vyriausioji redaktorė Natalja Radina savo pasisakymą paskyrė tam, kad išreikšti savo nepasitenkinimą Kijevo politika.

„Apie Ukrainą norisi pažymėti, aš jau neberandu žodžių, kaip galima paaiškinti tai, jog demokratinė Ukraina išlaiko diktatorių Lukašenką. Ir tai tada, kai jis jau paskelbė, jog de-fakto ir de-jure Krymas priklauso Rusijai, ir pasakė, jog Rusijos karo su Ukraina atveju, jis rems Rusiją. Ir vėl jokios griežtos reakcijos iš Ukrainos URM pusės mes neišgirdome. Kaip ir anksčiau, prakeiktas neapsibrėžtumas. Ir kartu su tuo Ukraina šiandieną perka didelį kiekį baltarusiškų naftos produktų, trąšų ir elektros energijos. Pagamintos toje pačioje atominėje elektrinėje, kuri jei susprogs, tai Vilniaus nebeliks. Man regis, šį klausimą reikia kelti griežtai, todėl, jei Ukraina nori būti demokratinę šalimi, tai visgi ji turi laikytis tam tikrų principų“, - pasipiktino Radina.

Ta pati Lietuva didina BelAE, su kuria žadėjo kovoti, produkcijos importą. Bet jai jokių pretenzijų Radina nepareiškia – bijo, jog ją deportuos tiesiog iš tribūnos?

3. „Ekonominio kolapso Rusijoje neįvyko“ ir Kremlius buvo teisus“

Ekonomistas, sociologas ir politinis veikėjas Vladislovas Inozemcevas – vienas iš pastovių Laisvosios Rusijos forumo pranešėjų. Žmogus, kuris gerai žino, ką reikia sakyti panašiame sambūryje.

„Metų pradžioje mes labai tikėjomės, jog ekonominė krizė, jei ne kolapsas, sukels rimtus trikdžius Rusijos vadovybei ir sudarys rimtas problemas Putinui ir jo komandai. Po dviejų metų prasidėjo pandemija, galima sakyti, jog mūsų prognozės neišsipildė. Rusijoje ekonominio kolapso neįvyko, atvirkščiai, šiandien Rusijoje ekonominė situacija gana stabili. Rusijoje buvo padaryta taip, jog ekonomika nesustojo, ir žymi gyventuoju dalis nepatyrė jokių sukrėtimų. Rimto lokauto neatsitiko, ir tai patvirtina paskutinių mėnesių eiga“, - pažymi Inozemcevas.

Po to ekspertas pabarė Europą už skubotą siekį įgyvendinti „žaliąjį perėjimą“. Dėl ko ji išprovokavo globalinę energetinę krizę, kurios dėka „Gazpromas“ gaus rekordinį pelną.

Ir iš viso, Inozemcevo žodžiais tariant, 2021 metais Rusijos papildomas pajamas sudarys maždaug 7 trilijonai rublių, Su tokia finansinę „pagalve“ artimiausiu metu šalies valdžia gali nė dėl ko nesijaudinti.

„Mes pastoviai kartojome, jog Rusija – pasaulio ekonomikos parazitas, kuris save aprūpina naftos ir dujų sąskaitą... Ar tai iš tikrųjų taip? Ir kodėl rimtai krentant eksporto pajamoms, vidaus paklausa išlieka?“, - klausia Inozemcevas.

Į „nusiminusių“ ekspertų ratą galima įtraukti ir Džordžo Vašingtono Universiteto Europos, Rusijos ir Eurazijos tyrimų instituto (IERES) mokslinę bendradarbę Mariją Sniegovają. Ji apgailestauja, jog vakarų bendrija nekonsoliduoja prieš išorės grėsmes. Amerikietiškiems demokratams „trampistai“ yra didesnis blogis nei pats Putinas.

„Aš dabar nematau JAV galimybės gražinti sau globalinio lyderio vaidmenį, ir čia tenka konstatuoti, jog Kremlius su savo pastoviu multipolinio pasaulio akcentavimu pasirodė teisus. Iš tikrųjų mes stebime šio multipolinio pasaulio atsiradimą, kur demokratijos silpnėja, o autokratijos bando pasinaudoti tuo momentu“, - reziumavo Sniegovaja.

4. „Baideno ir Putinu susitikimas – tai gėda!“

Forumo pakraščiuose tikrai isteriškai pasielgė vienas iš jo organizatorių Gari Kasparovas. Jo kritikos objektu tapo ne Rusijos prezidentas, o Jungtinės Valstijos kurios veda “bestuburią” užsienio politiką.

“Putinas ir toliau demonstruoja savo sugebėjimą kontroliuoti Vakarų pasaulį. Po visiškai gėdingo Baideno susitikimo su Putinu mus visus apėmė eilinio nebaudžiamumo jausmas“, - piktinasi Kasparovas.

Obama bandė draugauti su Kremliaus šeimininku, su Trampu „viskas aišku“, bet ir Baidenas nedemonstruoja pasiruošimo gražinti Amerikai globalinio lyderio vaidmenį.

„ Tie Rusijos olicharkai, kurie iš Ženevos stebėjo kas dedasi, galvoja: „Ko mums baimintis? Na, priims eilinį sankcijų paketą, Putinas mus vis vien apgins“. Putiną jie vertina kaip jų kapitalų neliečiamumo garantą“, - kalbėjo Kasparovas.

Likimo ironija, Laisvos Rusijos forumas vyko antrojo Putino ir Baideno derybų raundo išvakarėse. Šiam įvykiui Kasparovas tiksliai jokių vilčių nesitikėjo, jo „eilinio nebaudžiamumo jausmas“ dabar tik sustiprės.

5. „Liberalai, jūs pralošėte!“

Tikriausiai, pačią išsamiausią ir turiningiausią kalbą pasakė žurnalistas Arkadijus Babčenko. Savo liberaliniams draugams jis patarė pripažinti tą faktą, jog jie pralošė.

„Dabar Rusijoje nėra revoliucinės situacijos absoliučiai, visiškai. Jos iš viso nėra. Jei dabar kas ir kviečia išeiti į gatvę, tai arba provokatorius, arba žmogus, kuris nieko nesupranta. Jau vėlu, diktatūra įsitvirtino.

Dabar rusiškai opozicijai aš galiu pasakytu tik vieną: mano bičiuliai, jūs pralošėte, susitaikykite su tuo, ir atsižvelgdami į tai, ruoškite tolimesnes savo strategijas“, - pasakė Babčenko.

Tiems kurie ketina sėdėti sudėję rankas, žurnalistas patarė remti Ukrainos kariuomenę – pervesti jai pinigus naujoms kuprinėms, termovizoriams, taikikliams snaiperiams ir taip toliau įsigyti.

Jei visi Laisvos Rusijos forumo dalyviai susimes nors po 100 dolerių, tai Putino Rusijai bus galas. Bet tai dar netiksliai.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 13 — id: `scraped:rubaltic_lt:b7367d10de30ecd5`

**Title:** Kinija skaldo Lietuvos vadovybę

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Konfrontacijos su Kinija nepopuliarumas Lietuvos bendruomenėje Lietuvos – Kinijos santykius daro politinės vidaus kovos Vilniuje faktoriumi. Lietuviškoji opozicija susitinka su KLR atstovais ir apgailauja dėl santykių degradavimo. Pekinas, kuriam svarbu demonstratyviai nubausti Lietuvos vadovybę už anti kinietišką politiką, gali paspartinti vyriausybės pasikeitimą Vilniuje, perduodant kozirius valdančiųjų konservatorių priešininkams.

Prieš keletą dienų konservatorių atstovas sąžiningai prisipažino, dėl ko jiems prireikė „kryžiaus žygio“ prieš Kiniją avantiūros, remiant uigūrus, taivaniečius ir Dalai-lamą.

„Norint iš tikrųjų turėti JAV dėmesį, mūsų santykių su Taivanu stiprinimas yra vienas iš labai protingos politikos instrumentų. Mums Taivanas ir taip rūpi, bet kartu jis duoda ir didžiulį rezultatą“, - sakė buvęs premjeras ir Europarlamento deputatas Andrius Kubilius.

Tai yra visą tai, apie ką RuBaltic.Ru analitikos portalas rašė paskutiniaisiais keletą mėnesių, dabar „landsbergistai“ patvirtina tiesiogiai.

Tradicinis Lietuvos pasiūlymas tarptautinėje politikos rinkoje – Europos santykių su Rusija griovimas – užsakovui jau taip, kaip anksčiau, nebereikalingas. Todėl buvo sugalvota alternatyvi paslauga - Europos santykių su Kinija griovimas.

Užsakovas, kaip tai galima spręsti iš JAV valstybės sekretoriaus Antoni Blinkino bei kitų oficialių asmenų iš Vašingtono pareiškimų, tai palankiai įvertino.

Kartu su tuo Andriaus Kubiliaus paaiškinimuose jaučiasi bandymas pasiteisinti.

Remiantis Norstat LT lapkričio mėnesio apklausa, 41% lietuvių pasisakė prieš dabartinį santykių su Kinija ir Taivanu kursą. Šį kursą palaikė 34% apklaustųjų, o 26% dar neapsisprendė.

Apklausa buvo atlikta iki sensacingo Pekino sprendimo pašalinti Lietuvą iš kinų muitinio apiforminimo sistemos. Po to neapsisprendusiųjų skaičius staigiai sumažėjo, pertekėdamas į nusiteikusiųjų prieš Lietuvos URM politiką skaičių. Kadangi tapo aišku ko viliamasi šiame anti kinietiškame žaidime.

Vienu kartu iš Lietuvos verslininkų atimti prieigą prie pačios didžiausios pasaulio rinkos – tai jau ne juokai. O kas atsakingas tiems verslininkams? Tikriausiai, tas, kas prisigalvojo surengti šią diplomatinę avantiūrą, idant gražinti sau, už vandenyno esančios dievybės, palankumą.

Lietuvos vidaus politikoje kinų faktorius jau gyvuoja. Užsienio politikos nepopuliarumas ir miglota nuojauta, jog su Kinija Lietuva susilauks stambių nemalonumų, skatina Lietuvos opozicija veikti naudojant kontrastą.

Praeitą savaitę Lietuvos socialdemokratai susitiko su KLR laikinuoju reikalų patikėtiniu Lietuvoje Čiu Baichua ir patikino jį, jog apgailestauja dėl sugadintų Lietuvos Respublikos ir Padangių šalies santykių. Valdančios partijos iniciatyvą opozicija vertina kaip išprotėjimą, kuris panaikino rūpestingai dešimtmečiais kuriama Lietuvos – Kinijos dialogą.

„Olimpinės žaidynės – tai viso pasaulio ir viso olimpinio judėjimo įvykis, todėl iš sportininkų, kurie daugelį metų ruošėsi olimpiniams startams, negali būti atimta galimybė juose dalyvauti, kuri atsirado tik kartą per visą jų sportinę karjerą“, - komentavo, pavyzdžiui, konservatorių idėją boikotuoti Olimpiadą Pekine buvęs Lietuvos premjeras Algirdas Butkevičius.

Akivaizdu, jog Lietuvos opozicionierių, kai jie pareiškia tokius pareiškimus,   tikslinė auditorija ne Kinija, o jų Lietuvos rinkėjai. Tačiau kinų diplomatas, kuris visą turi įvertinti, visgi nusprendė pritarti ir susitikti su žmonėmis, kurie jokiu būdu nenustato užsienio politikos kursą. Tuo pačiu KLR atstovas pabrėžė Lietuvos opozicijos pareiškimo svarbą.

Kinijos naudai suveikia valdančios partijos nepopuliarumas, daugelio lietuvių nenoras turėti nuostolių dėl intrigantinės politikos, o taip pat besiplečiantis Lietuvos valdžios skilimas. Prezidento Gitano Nausėdos ir „landsbergistų“ vyriausybės konflikto jau niekas neslepia, ir apie jo priežastį Lietuvoje pasisakoma atvirai: konservatorių noras „nuimti“ valstybės vadovą, kad sekančiu šalies prezidentu padaryti užsienio reikalų ministrą Gabrielių Landsbergį.

Esant tokioms aplinkybėms Pekinui atsiranda daug galimybių teikti pagalbą Lietuvos valdžios pasikeitimui. Tikėtinai, priešlaikiniam.

Kartu su tuo kinams nusispjauti, kas valdys Lietuvoje. Jiems svarbu kita. Jei jau Vilniuje nusprendė pasirodyti Europai „principiškų“ santykių su Kinija pavyzdžiu, tai Pekinas Lietuvos pavyzdžiu parodys visai Europai, kaip galima ir kaip nevalia elgtis su Padangių šalimi.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 14 — id: `scraped:rubaltic_lt:9c6a673a0e4e256b`

**Title:** Kinija „panaikino“ Lietuvą: jūsų prekės mūsų rinkoje daugiau neegzistuoja

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Kinija blokavo prekių importą iš Lietuvos: KLR muitinės sistemoje tokia šalis daugiau nebeegzistuoja. Informaciją apie tai patvirtino Lietuvos URM ir vietinė pramoninkų konfederacija. Oficialus Vilnius Pekino veiksmus apibūdino „beprecedenčiais“ ir kreipėsi į Europos komisiją pagalbos. Tokiu būdu Lietuva patvirtina, jog ji, amerikiečių džiaugsmui, sąmoningai bando sukivirčyti KLR ir Europos sąjungą.

Prieš keletą dienų lietuviškas leidinys „15 minučių“ pranešė, jog į jų redakciją kreipėsi koks tai nepatenkintas, į Kiniją eksportuojantis medieną, verslininkas. Neseniai jis išsiuntė stambią savo prekės siuntą į Kiniją, bet nesugebėjo jos išmuitinti.

„Klientas pasiima per banką dokumentus ir, konteineriams esant netoli uosto, kreipiasi į Kinijos muitinę, susimoka muito mokestį ir prašo išmuitinti prekes. Lygiai tokia pat sistema veikia ir ES. Klientas vakar nusinešė dokumentus į Kinijos muitinę ir jam pasakė, kad Lietuvos, kaip importuotojos, nėra. Ji yra ištrinta“, – aiškino verslininkas anonimas. Tokia situacija susidarė Šanchajaus uoste.Bet lietuviai patikrino ne tik Šanchajaus uostus, bet ir kituose uostuose – analogiška situacija. Informaciją patvirtino Lietuvos pramoninkų konfederacijos pirmininkas Vidmantas Januliavičius: „Lietuva išbraukta iš muitinės sistemų, tokios šalies Kinijos muitinės sistemoje, panašu, kad nėra. Tai sukelia papildomų problemų eksportuotojams, nes negali išsiųsti, kiek likę tų krovinių“. „Kad muitinė bando blokuoti prekes iš Lietuvos, yra logiška ir tam nebūtina Kinijos vyriausybės oficialių nurodymų, kad stabdytų importą iš Lietuvos – tai gali būti vidiniai nurodymai, kurie nėra oficialūs. O atsisakyti importuoti prekes iš Lietuvos gali būti daug priežasčių nurodoma – formalių ir neformalių, o mes nesunkiai galime atspėti, kodėl tai vyksta. Kad gali būti sąmoningas blokavimas, visai tikėtina “, – teigė Lietuvos-Kinijos prekybos asociacijos generalinis direktorius Rokas Radvilavičius. Nesunku atspėti, dėl kokios priežasties Kinija blokavo prekybą su Lietuva.

Į šį pavyzdį verta atkreipti dėmesį ir kitoms šalims, kurias Lietuva taip pat erzina.

Ką daro Kinija kai jos atžvilgiu kai kas pasielgia nedraugiškai? Visų pirma, ji veikia greitai ir ryžtingai. Antra, niekas Kinijoje nepareiškia garsių pareiškimų, nerengia jokiu sankcinių paketų ir neaiškina, kokiu būdu tos sankcijos veiks.

Lietuvius taip pat nepainformavo, jog jų prekes daugiau nebegalima eksportuoti į Kiniją.

Ką daryti su konteineriais, kurie jau atgabenti arba tik gabenami į Šanchajaus uostą? Retorinis klausimas. „Indėnų“ (t.y. krovinio siuntėjų) problemos kinų „šerifą“ nedomima.

Panašiai normalus žmogus reaguoja į uodą, kuris jį gelią. Uodui beprasmiška aiškinti ar kelti kokius tai reikalavimus. Paprasčiau priploti, ir viskas.

„Mes atsakomųjų sankcijų įvesti negalime, nes neturime galimybės iš muitinės sistemos išbraukti vienos ar kitos Kinijos įmonės. Muitines sistemas reguliuoja EK. Todėl manome, kad dėl to turėtų įsitraukti institucijos ir atstovauti Lietuvai“, – pažymi respublikos užsienio reikalų ministras Gabrielius Landsbergis. Bet kam iš viso reikalingos atsakomosios sankcijos? Patys Lietuvos politikai tikina, jog Kinija negali padaryti kokią tai jaučiamą žalą Lietuvos ekonomikai: tik 1,1% bendros Pabaltijo respublikos eksporto apimties krenta KLR daliai (maždaug 300 milijonų eurų į metus).

Be to, dabar Lietuvos verslas gali tikėtis prekybinių-ekonominių santykių vystymosi su Taivanu.

„Jau geriau palaikyti santykius su išsilavinusia technologiškai išsivysčiusia demokratine šalimi, kurioje gyvena 23 milijonai žmonių, negu su autoritariniu režimu, kuri gali imtis atsakomųjų priemonių, jei jūs padarysite kažką tai tokio su kuo jie nesutinka“, - kalbėjo Lietuvos parlamento grupės santykiams su Taivanu pirmininkas Matas Maldeikis.

Pagaliau, neseniai Landsbergis iš JAV Eksporto-importo banko gavo tiesioginių paskolų 600 milijonams dolerių garantijas. Šių lėšų gali tikėtis ir amerikietiškas verslas, jei jis numato plėsti savo produkcijos realizacijos rinkas Pabaltijo respublikoje.

Tas pats liečia ir lietuvius, kurie pageidauja eksportuoti į JAV. Landsbergis iš anksto išprašė savotišką kompensaciją už sugadintus santykius su Kinija.

Vilnius galėjo pareikšti, jog jis pasiruošęs KLR sankcijoms ir nemano reikalingu aptarti atsakomas priemones. Bet vietoj to ministras kreipiasi pagalbos į Europos Komisiją. Kodėl? RuBaltic.Ru analitikos portalas jau ne kartą atsakė į šį klausimą: nusistatymas prieš Pekiną Landsbergiui ir kompanijai yra daugiau instrumentas, o ne tikslas.

Kai kurie Lietuvos politikai to ir neslepia. Štai, pavyzdžiui, visiškai nesenas buvusio Lietuvos premjero ir veikiančio Europarlamentaro Andriaus Kubiliaus prisipažinimas: „Norint iš tikrųjų turėti JAV dėmesį, mūsų santykių su Taivanu stiprinimas yra vienas iš labai protingos politikos instrumentų. Mums Taivanas ir taip rūpi, bet kartu jis duoda ir didžiulį rezultatą“.

„Didžiulio rezultato“ bus dar daugiau, jei Europos Sąjunga parems Pabaltijo respubliką kilus Kinijos „prekybinei agresijai“.

Bet dėl to reikia labai pasistengti.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 15 — id: `scraped:rubaltic_lt:edf53b2680ee84fb`

**Title:** Putinas iškėlė ultimatumą Vakarams: NATO palieka Pabaltijį ir Ukrainą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Vakarų ir Rusijos „nervų karas“ dėl Ukrainos pasiekė savo apogėjų: RF URM vadovas Sergėjus Lavrovas perspėjo, jog į Europą grįžta „košmariškas karinės konfrontacijos scenarijus“. Kartu su tuo Rusijos prezidentas Vladimiras Putinas paaiškino, kokiu būdu Europa gali išvengti „košmariško scenarijaus“. Tam reikalingos juridiškai įpareigojančios NATO atsisakymo nuo tolimesnės plėtros į rytus garantijos. Šis Maskvos reikalavimas apglėbia ne tik tai, jog prie Aljanso ne būtu prijungiamos naujos šalys – Rusijos kaimynės, bet ir atsisakymą dislokuoti naujas ginkluotes greta Rusijos sienų šalyse, kurios jau yra NATO: Estijoje, Latvijoje, Lietuvoje.

„Tie, kurie, kaip mokinukai išmokę pamoką, kartoja Bukarešto tezes ir tvirtina, jog klausime dėl NATO plėtros trečiosios šalys neturi teisės išreikšti savo poziciją – žmonės, kurie „žaidžia su ugnimi“. Aš esu įsitikinęs, jog jie to negali nesuprasti. Noriu, kad visiems būtų labai aišku: mūsų kaimynių-šalių pavertimas į priešinimosi Rusijai placdarmą, NATO pajėgų dislokavimas tiesiogiai greta mūsų saugumui strategiškai svarbių rajonų kategoriškai nepriimtina“, - pabrėžė Sergėjus Lavrovas   ESBO šalių užsienio reikalų ministrų tarybos posėdyje.

Rusijos ministro pasisakymo kontekstas buvo apie Ukrainą bei kitas Rusijai kaimynines šalis, kurias vakarų „vanagai“ stengiasi įgrūsti NATO.

Tačiau Rusijos kaimynių pavertimas į priešinimosi Rusijai placdarmą – tai ne tik apie Gruziją ir Ukrainą.

Tai yra, NATO atsisakymas plėstis toliau į rytus Rusijoje suprantamas plačia esme: ne tik Ukrainos, Suomijos, Gruzijos neįstojimas į Aljansą, bet ir Baltijos regiono NATO narių – šalių militarizavimo nutraukimas.

Dar konkrečiau apie tai, koks Maskvos požiūris į pačio stambiausio konflikto su Vakarų šalimis sureguliavimą, pasisakė Rusijos prezidentas Vladimiras Putinas. „Dialoge su Jungtinėmis Valstijomis ir jų sąjungininkais mes sieksime suformuluoti konkrečius susitarimus, eliminuojančius bet kokią tolimesnę NATO plėtrą į rytus ir, mums sukeliančių grėsmę, ginkluočių sistemų dislokavimą tiesiogiai greta Rusijos teritorijos sienų. Siūlome šiuo klausimu pradėti konkrečias derybas“, - sakė Putinas užsienio valstybių ambasadorių skiriamųjų raštų priėmimo ceremonijoje.

Rusijos lyderis konkretizavo savo mintį: kalbama apie tai, jog reikalingos „būtent teisinės, juridinės garantijos, kadangi vakarų kolegos neišpildė savo pačių atitinkamų žodinių įsipareigojimų“, kai paleidžiant Varšuvos sutarties bloką ir susijungiant Vokietijai Gorbačiovui buvo pažadėta, jog NATO nebus plečiamas į rytus.

Tokiu būdu, Rusijos sąlygos: raštiškos garantijos, jog Ukraina bei kitos, su Rusija ribojančiosios šalys, nebus priimamos į NATO, o tuose, kurios jau priimtos, bus nutrauktas ginkluotės eskalavimas.

Būtent dėl šio principo kas kartą buvo atsisakoma išklausyti Rusijos argumentų, bei atsižvelgti į jos interesus. Pagal Vakarų logiką Rusija gali turėti tik vieną interesą: tapti „laisvojo pasaulio“, į kurį ji įstos turėdama pralaimėjusio ir kapituliavusio statusą, dalimi.

O dėl to rusai, kaip Bulgakovo Šarikovas, turi „tylėti ir klausyti, tylėti ir klausyti ką jums sako“.

Pradžioje rusai tylėjo ir klausėsi, vėliau klausėsi, bet pradėjo atsakinėti, paskui ir klausyti baigė, kai įsitikino, jog jų nebeklauso. Šiuo atžvilgiu praeinantys metai buvo galutiniai, kai Maskva pareiškė, jog nesiruošia klausytis JAV ir ES pamokymų apie demokratiją bei žmogaus teises iki to meto, kol jie patys neišmoks jas gerbti.

Šiuo atžvilgiu būdinga tapo reakcija į praeitų metų įvykius Baltarusijoje, kai Europos lyderiai dėl situacijos sureguliavimo vienas paskui kitą pradėjo skambinti į Kremlių – Putinui. Tokio elgesio motyvą vėliau paaiškino Prancūzijos prezidentas: mes nenorime, kad Baltarusijoje pasikartotu tas pats, kas atsitiko Ukrainoje.

Priminsime, jog Ukrainoje, prieš septynerius metus iki įvykių Baltarusijoje, Europa demonstratyviai atsisakė atsižvelgti į Rusijos interesus. O taip pat ir į prorusiškos Ukrainos dalies interesus. Ir taip baigėsi katastrofa.

Dabar Maskva kovoje už rūpinimąsi Rusijos interesais siekia naujo lygio.

Jei Putinas nusprendė paviešinti tokias sąlygas – tai yra tikras kardinalaus nusilpimo požymis. Tačiau, iki to, kad jis sutiks įvykdyti šias sąlygas arba bent jas aptarti, dar gana toli. Sutikti – tai pripažinti, jog „pergalės šaltajame kare“ periodas baigtas. Tai dar blogiau nei pripažinti pasaulio , kuriame visa valdžia sukoncentruota vienose rankose, pabaigą.

Rusijai duoti raštišką pasižadėjimą, juridiškai apriboti savo visko leistinumą Rytų Europoje – tai padaryti nei JAV nei jos sąjungininkai nesugebės. Jiems tai, paprasčiausiai, neįmanoma.

Ir kol tai nėra įmanoma, pasilieka karinės konfrontacijos „košmariškas scenarijus“.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 16 — id: `scraped:rubaltic_lt:8af0648a4383c7c2`

**Title:** Lietuvos valdžia referendumuose įžiūrėjo „dovaną Kremliui“

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Iniciatyvos dėl parašų, skirtų referendumui paskelbti, kartelės skaičiaus sumažinimo rėmimas Lietuvos prezidento Prezidentūroje yra naudingas Kremliui. Apie tai pareiškė valdančios konservatorių partijos Seimo deputatas Mindaugas Lingė. Anksčiau Respublikos užsienio reikalų ministras Gabrielius Landsbergis kritikavo prezidentą Gitaną Nausėdą už pasiūlymą dažniau skelbti referendumus. Situacija atrodo paradoksiškai: kovotojams už demokratiją Baltarusijoje, Rusijoje bei kituose pasaulio šalyse savo namuose tiesioginė demokratija nėra priimtina.

Dirvą eiliniam Lietuvos valdančiosios partijos ir prezidento Nausėdos Prezidentūros konfliktui parengė Konstitucinis teismas, kai praeitų metų liepos mėnesį „užbrokavo“ referendumo įstatymą. Šio dokumento priešininkai sugebėjo įrodyti, jog buvo pažeista jo priėmimo procedūra. Tokiu būdu, prieš penkis mėnesius senas įstatymas neteko savo galios, o naujas iki šiol nepriimtas.

Opozicija pasipiktinusi: kodėl lietuviai liko be savo konstitucinės teisės inicijuoti referendumus?

Teisingumo ministrė Evelina Dobrovolska kaltina buvusią vyriausybę: esą, ji ne atliko jokio “namų darbo“. Vasarą naujojo įstatymo apie referendumą projektas Seime buvo išnagrinėtas per pirmąjį skaitymą, rugsėjo mėnesį jį rengėsi nagrinėti pakartotinai.

Dobrovolska tikėjosi, jog jau rudens sesijos pradžiai šį klausimą parlamentas išspręs. Bet dėl nežinomų priežasčių, per tą laiką nieko padaryti nepavyko: Seimo teisės klausimų komisijos pirmininkas Stasys Šedbaras mano, jog antrajam skaitymui įstatymo projektas bus parengtas tik sekančių metų kovo mėnesį.

„Šiuo metu renkami parašai dėl Referendumo iniciatyvos kartelės sumažinimo iki 100 000 piliečių parašų, kuri šių metų birželio mėnesio 29 dieną yra įregistruota VRK (Vyriausioji rinkiminė komisija – RuBaltic.Ru pastaba). Remiantis galiojančios Lietuvos respublikos Konstitucijos 9 ir 147 straipsniais, būtina surinkti 300 000 parašų“,- pranešama organizacijos Interneto svetainėje.

Kampanija įgijo bendranacionalinį mastą, ją remia žinomi politikai bei ekspertai. Naujų referendumo paskelbimo taisyklių lobistams jau paskirtas laikas televizijos eteryje savo pozicijos paaiškinimui.

Iš pradžių VRK atsisakė išduoti jiems parašų rinkimo lapus, nurodydami į tai, jog senas įstatymas apie referendumą jau negalioja, bet teismo sprendimu buvo priversta tai padaryti. Tarp kitko, ši tema nėra laužta iš piršto.

Todėl ne nuostabu, jog Lietuvos žurnalistai paprašė apie tai pasisakyti Jūratę Šovienę – Lietuvos prezidento Gitano Nausėdos patarėją. Paklausus, ar turi būti supaprastinta referendumo sušaukimo procedūra, ji atsakė sekančiai: “Matyt, turėtų. Būtų suteiktos didesnės galimybės pasisakyti tautai, piliečiams dėl tam tikrų svarbių valstybei klausimų sprendimų, būtų geresnės galimybės“.

Į šį nekaltą epizodą pasipiktinančiai atsiliepė „Tėvynės sąjunga – Lietuvos krikščionys demokratai“ (TS-LKD) partijos Seimo deputato Mindaugas Lingė.

Prie ko čia Rusija? Pas Lietuvos konservatorius ji visada „prie ko“ Lingės nuomone, Rusija galės „prastumti“ kokias tai „atsitiktines iniciatyvas“ visuotiniam balsavimui Lietuvoje.

„Viena didžiausia Kremliaus pergalių – sužlugdyta Visagino atominės elektrinės statyba prieš rinkimus pasinaudojus ir įsūdžius referendumą. Rezultatas – Astrave (Baltarusijos atominė elektrinė – RuBaltic.Ru pastaba). Tai tik vienas pavyzdys, kai demokratinis instrumentas panaudotas antivalstybiniams tikslams“, - rašo Lingė. Kalbama apie 2012 metų įvykius, kai Lietuvos konservatorių oponentai iš tikrųjų paskelbė referendumą dėl naujos atominės elektrinės statybos. Iš atvykusių 52,6%, beveik 65% Pabaltijo respublikos piliečių balsavo „prieš“. Tikriausiai, „Kremliaus pasisekimas“ yra tame, kad Baltarusijos AE pašalino savo potencialų konkurentą Lietuvoje. Tiesa, Lingė užmiršo eilę smulkmenų.

Tarp kitko, konservatoriams čia viskas yra tipiška. Kiekvieną kartą, kai jų vyriausybė „prisidaro“, jie seka nuostabias pasakėles, jog jų kelnaites ištepliojo „Kremliaus ranka“.

Lingės pasisakymą feisbuke komentavo dar viena žymi politikė – Europos parlamento „landsbergistų“ deputatė Rasa Juknevičienė. „Och tu! Tai sena Kremliaus svajonė! Argi niekas nepapasakojo prezidentui apie latvių patirtį, kai Kremlius organizavo referendumą dėl antrosios valstybinės kalbos? Ir tai padaryti jis sugebėjo todėl, jog buvo labai supaprastinta referendumų sušaukimo procedūra“, - pareiškė Juknevičienė.

Netgi nesikabinsim prie tvirtinimo, jog 2012 metais referendumą dėl kalbos Latvijoje, esą, sušaukė Rusija. Tegul tai komentuoja psichiatrai. Bet apie kokią „labai supaprastintą procedūrą“ kalba ponia Juknevičienė?

Kampanijos iniciatoriai Latvijos VRK pateikė 187378 tūkstančius parašų, kas sudaro 12,14% bendrojo rinkėjų skaičiaus. Minimali kartelė – 10%. Tai visiškai atitinka rėminėms referendumų sušaukimo Europos šalyse sąlygoms. Tarp kitko, šiuo metu Lietuvoje oficialiai gyvena 2,7 milijono žmonių. 300 tūkstančių parašų referendumo sušaukimui – tai žymiai daugiau nei 10% pilnamečių respublikos piliečių.

Ir kodėl Lietuvą turi gąsdinti latviška patirtis? Prieš rusų kalbos valstybinį statusą balsavo beveik 75 % referendumo dalyvių. Tai tapo dovana vietiniams nacionalistams: jie gali nutraukti bet kokias kalbas apie dvikalbybės įtvirtinimą Latvijoje įstatymu, nurodydami į piliečių pareikštą valią.

Pavyzdžiai čia pat: beveik prieš keletą dienų buvo paviešinti socialinės apklausos rezultatai, kurie rodo, jog sąlyginė lietuvių dauguma nepritaria konfrontacijai su Kinija (šiandiena tai vienas iš pagrindinių „landsbergistų“ užsienio politikos elementų).

Netgi nepagalvojus, galima surasti eilę klausimų, į kuriuos Lietuvos tautos ir, dabartiniu metu valdančiosios partijos, atsakymui bus skirtingi. Apie tai, tarp kitko, atvirai pareiškė Gitanas Nausėda: šalies valdžia nepageidauja, jog esminiai valstybės gyvenimo klausimai būtų visuotiniai aptariami. „Dar nesubrendome kaip demokratinė valstybė, jeigu politikai žvelgia į piliečius kaip į statistinius vienetus, kurių balsas reikalingas kartą per kelerius metus rinkimuose. Nuo kada pradėjome bijoti mūsų žmonių?“ – klausė valstybės vadovas.

Veikianti ministrė pirmininkė Ingrida Šimonytė vos tik praėjus keturiems mėnesiams po naujojo Ministrų kabineto patvirtinimo, visiems nepatenkintiems patarė laukti naujų parlamento rinkimų. Tikriausiai, tada konservatoriai pereis į opozicijon, o po keturių metų vėl atsidurs valdžioje, dirbs laikydamiesi principo: „Ką noriu, ta ir darau“.

Į šią sistemą referendumai neįsirašo. Štai koks paradoksas. Pagrindiniai kovotojai už demokratiją „nuo Baltarusijos iki Taivano“, kaip jie patys pasako, savo pačių šalyje nepalaiko pagrindinio tiesioginės demokratijos instrumento panaudojimą.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 17 — id: `scraped:rubaltic_lt:1f7812e1bfa23f22`

**Title:** Lietuviai smerkia Lietuvos užsienio politiką

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos politikai Baltarusijos atžvilgiu pritaria 49% ir nepritaria 37% Pabaltijo respublikos gyventojų. Tokiu būdu, Lietuvos bendruomenės nuomonė dėl Baltarusiją yra skilusi. Dar būdingesnė nuomonė dėl Kinijos. Nedraugiškai Lietuvos politikai KLR atžvilgiu nepritaria dauguma lietuvių.

Rinkos tyrimo kompanija Norstat LT Lietuvoje organizavo bendruomenės nuomonės apklausą. Respondentams buvo pasiūlyta įvertinti pačius aktualiausius šalies užsienio politikos klausimus – santykius s Baltarusija ir Kinija.

Valdantiems konservatoriams rezultatas ne tapo triumfu.

„ Apklausos rezultatai rodo, jog Lietuvos politikai Baltarusijos atžvilgiu pritaria 49% šalies gyventojų ir nepritaria 37%. Dar 15% apklaustųjų pareiškė, jog jie neturi nuomonės dėl šių klausimų“, - sakoma atskaitoje.

Sunku ginčytis su ekspertais, kurie, komentuodami šią informaciją, kalba apie žymų bendruomenės pritarimą Lietuvos veiksmams Baltarusijos atžvilgiu. Beveik pusė apklaustųjų – tai tikrai daug. Kur kas daugiau, negu partinis valdančiosios partijos reitingas.

„Baltarusijos atžvilgiu vedama politika apglėbia ne tik dabartinę valdžią, bet ir prieš tai buvusią valdžią. Sugriežtinta Baltarusijos atžvilgiu pozicija, Lukašenkos, prezidento rinkimų rezultatų nepripažinimas ir klausimai dėl sankcijų prasidėjo dar tada, kai valdžioje buvo Sauliaus Skvernelio vadovaujama vyriausybė ir tęsiasi prie konservatorių vyriausybės“, - pažymi politologas Mažvydas Jastremskis.

Lieka atviru klausimas, kuo motyvuoja 37% nesutinkančiųjų. Patikslinantys klausimai pagelbėtų jų suskirstymui į keletą grupių. Galimai, kai kas atvirai simpatizuoja „paskutiniam Europos diktatoriui“ ir jo sukurtą valstybės valdymo sistemą vertina kaip efektyvią, kiti juo nepasitiki, bet mano neteisingu kištis į kitos valstybės reikalus.

O, gal būt, kai kurie baiminasi, jog Baltarusijos atsakas gali smogti į jų pačių gerovę. Ypatingai tai liečia tuos, kurie dirba uostuose, geležinkelyje, prekybos sferoje.

Tyrimo detalės rodo, jog respondentų atsakymai tikrai priklauso nuo jų socialinio statuso. Tarp žmonių su aukštuoju išsilavinimu Lietuvos politiką Baltarusijos atžvilgiu remia 60% apklaustųjų, o tarp apklaustųjų su viduriniu išsilavinimu – tik 35%. Paramos lygis tarp aukšto ir vidutinio lygio vadovų - 61%, tarp paprastų darbininkų - 35%, tarp bedarbių - 33%.

Norstat LT apklausoje taip pat nekonkretizuojama, būtent ką reiškia formuluotė „Lietuvos politika Baltarusijos atžvilgiu“. Paskutiniu metu ši politika tapo labai daugiapusiška.

Daugelis apklausos dalyvių, pavyzdžiui, gali remti priemones, nukreiptas į atkirtį Lukašenkos „migracijos agresijai“, bet kartus su tuo pasisakyti prieš naujas ekonomines sankcija. Kai kas pasisako už sankcijų politikos sugriežtinimą, bet nemano, jog reikia remti ir teikti finansinę paramą bukagalviai baltarusiškai opozicijai, atstovaujamai Svetlanos Tichonouskojos biuru.

Praėjusių metų rugpjūčio – rugsėjo mėnesiais panašios apklausos rezultatai būtu principingai kitokie. Tada absoliuti lietuvių dauguma tikrų tikriausiai remtu pastangas, nukreiptas į valdžios pakeitimą kaimyninėje šalyje. Bet dabar netgi patys „kietakakčiausieji“ demokratai supranta, jog Lukašenka pasilieka ir su tuo kaip tai reikia susitaikyti.

Jei kalbėti apie santykius su Kiniją, tai čia Lietuvos valdžia nėra remiama netgi sąlygine piliečių dauguma. „Visiškai kita situacija su Lietuvos politikos požiūriu į santykius su Kinija ir Taivanu. Šiuo klausimu tik 34% apklaustųjų parėmė dabartinę Lietuvos poziciją, 41% jos nepalaikė, ir dar 26% neturėjo jokios nuomonės“, - pasakyta ataskaitoje.

Daugiau nei ketvirtis neapsisprendusiųjų – tikslus, Lietuvoje paprasčiausiai ne aktualizuotos temos rodiklis. Baltarusija su savo „hibridiniais migrantais“ randasi šalia, po šonu, o Kinija – kažkur tai toli. Be to, kaip tiksliai pastebi Mažvydas Jastremskis, šiame klausime nėra buvusios vyriausybės pozicijos tęstinumo dabartine vyriausybe.

Tik prieš metus, konservatoriams atėjus į valdžią, Kinija tapo svarbiu Lietuvos užsienio politikos faktoriumi. Buvęs ministras pirmininkas Saulis Skvernelis nebuvo nusiteikęs griežtam nusistatymui Kinijos atžvilgiu. Todėl akivaizdu, jog šiame klausime respondentų nuomonė daugumoje priklauso nuo to, kuriai partijai jie teikia pirmenybę.

Tie 34%, kurie remia kovą su „kinų grėsme“ savo daugumoje yra valdančių – konservatorių, liberalų ir Laisvės partijų rinkėjai. Likę, arba išviso „ne temoje“, arba užduoda logišką klausimą: kodėl būtent Lietuva tapo pati antikiniškiausia Europos šalimi? Kodėl tik ji atsidūrė ant diplomatinių santykių nutraukimo su Kiniją slenksčio?

Daugelis respondentų iš tikrųjų mano, jog jų šalis turi laikytis įžūlios užsienio politikos ir ginti demokratiją nuo Baltarusijos iki Taivano. Bet yra ir kiti – tie, kurie pasaulį mato ne juodai – baltą. Jie skiria ir kitas spalvas.

Ir tokius žmones Lietuvoje anaiptol negalima vadinti marginalais.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 18 — id: `scraped:rubaltic_lt:9030e18b518f71ea`

**Title:** Lietuva padovanos rusų uostams kinų tranzitą į Pabaltijį

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Taivane apsilankė Pabaltijo šalių parlamentarų grupė. „Baltijos seserų“ atstovai jau pasiūlė pritarti Lietuvos iniciatyvai ir atidaryti Taivano diplomatines atstovybe Latvijoje ir Estijoje, nežiūrint į tai, kaip tai įvertins oficiali Kiniją. Lietuvai tokia „Baltijos vienybė“ bus užsienio politikos pergalė, bet dar daugiau išloš Rusija: Vilniaus pastangų dėka kinų tranzitas paliks visą Pabaltijį ir pereis i rusų uostus.

Estija turi judėti link oficialaus Taivano pripažinimo – Taibėjuje pareiškė Estijos parlamento deputatas Rijgikogu Matis Milling. Tautos išrinktasis atstovas mano, jog šis procesas turi vykti palaipsniui, žingsnis po žingsnio. Pirmąją būtinąją Taivano pripažinimo sąlyga politikas įvardino oficialios alternatyvinės Kinijos respublikai atstovybės atidarymą Taline.

Akivaizdu, kokia šalis šiuo atveju bus pavyzdžiu Estijai. Šių metų rugpjūtyje Lietuva atidarė oficialią Taivano atstovybę Vilniuje, kuo išprovokavo faktišką diplomatinių santykių su Pekinu nutraukimą. Po to KLR ambasadorius buvo atšauktas iš Lietuvos; Pekinas neketina užgniaužti skandalą ir gražinti ambasadorių į Vilnių.

Pastarieji jau žengia tuo keliu.Tai įrodo pats tas Pabaltijo parlamentarų vizitas į Taivaną. Reikia pripažinti: tai Lietuvos užsienio politikos pasiekimas, kuri svajoja savo konfrontacinę santykių linija su Kinija primesti visai Europai. Pirmas ir pats logiškiausias šios linijos etapas – suagituoti į kovą su „komunistine diktatūra“ dvejas savo „Baltijos seseris“.

Paminėtas deputatas Rijgikogu Matis Milling išreiškė viltį, jog Estijos bendradarbiavimas su Taivaniu ne taps konflikto su Kinija priežastimi, kaip tai atsitiko su Lietuva.

Nepagrista viltis.

„Ilgalaikis stabilus ir veiksmingas bendradarbiavimas yra įmanomas būtent todėl, kad mūsų visuomenės remiasi tais pačiais demokratijos, žmogaus teisių ir teisinės valstybės principais“, – pabrėžė susitikime Taibėjuje Lietuvos delegacijos vadovas Matas Maldeikis. Į ką Taivano prezidentė atsakė visiems Pabaltijo atstovams, kad jų šalis jungia bendra „išsilaisvinimo iš autoritarinio valdymo ir kovos už laisvę“ patirtis. Tai yra, projektui jau rengiamas ideologinis pamatas. Pas mus – demokratija, pas juos – diktatūra. Pas mus – laisvas pasaulis, pas juos – totalitarinis režimas. Mes kovojome už laisvę, jie – genetiniai vergai.

Toks metodas Baltijos šalių santykių su Rusija griovimo istorijoje suveikė patikimai. Bet kokia ekonominė prasmė, nauda nacionaliniams interesams, 30 metų eigoje spaudžiama politinių dogmų, triuškinančiai pralošinėjo. Tuo labiau jie pralošia ir atvejyje su Kinija, su kuria nėra tokių gilių ekonominių ryšių, kokie po SSSR sugriuvimo buvo su Rusija.

Ir jau nebebus.

Tarp kitko, apie Rusiją. Istorijoje apie nukreiptą prieš Kinija politiką, Lietuva tokia pat suinteresuota šalis, kaip ir Jungtinės Valstijos. Jos nauda dėl Vilniaus veiksmų daugiau yra vietinio pobūdžio, negu amerikiečiams. Bet be jokių abejonių ji yra.

Bet jau Vilniuje tikrai pasistengs, kad taip būtu. Vien tik Taivano diplomatinėmis atstovybėmis Rygoje ir Taline Latvija su Estija neatsikratys, Bus ir „uigūrų genocido“ pasmerkimas, ir Dalai Lamos priėmimas, ir „kinų grėsmė“ specialiųjų tarnybų ataskaitose. Pastaroji, tarp kitko, jau yra.

Kas žengė link nuožulnios plokštumos, tas ja ir rieda.

Nesunku atspėti, kokiu būdu KLR atreaguos į Baltijos šalių nedraugiškumą. Lietuvos patirtis parodė, jog Pekinas laikosi tvirto principo: šalys kurios veda nukreiptą prieš Kiniją politiką turi netekti kinų pinigų ir galimybės uždirbti Padangių šalies sąskaita.

Todėl, jei anksčiau vyravo hipotetinė galimybė, jog kinų partneriai paprašys „Rusijos geležinkelius“ praleisti jų krovinius į Pabaltijo uostus, tai esant šiuolaikinėms tendencijoms, tie kroviniai garantuotai judės į Ust-Lugą, Vysocką, Primorską.

Dėl to siūloma Lietuvos URM rusofobus apdovanoti Rusijos Draugystės ordinu. Tiesa, jie nesupras už ką toks apdovanojimas, ir pamanys, jog tai provokacija. Tačiau protingi žmonės iš širdies pasijuoks.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 19 — id: `scraped:rubaltic_lt:624573047021f07f`

**Title:** «Kovotojas su blogio imperija»:  paprasti lietuviai apmoka dėdulės Landsbergio piarą Vakaruose

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Dokumentinis filmas „Misteris Landsbergis. Sunaikinti blogio imperiją“, skirtas buvusiam Lietuvos Seimo pirmininkui, gavo pagrindinį IDFA 2021 kino festivalio Amsterdame prizą. Verta dėmesio tai, jog šis projektas buvo finansuojamas Valstybinio Lietuvos kino centro. “Tautos tėvo“ šlovinimui režisierius Sergėj Loznica iš Pabaltijo respublikos gavo 184 tūkstančius eurų, ir , iš visko sprendžiant, neblogai susitvarkė su savo užduotim.

„Šį projektą aš pradėjau nuo paprasto klausimo: „Kodėl anksčiau Lietuvoje niekas jo (Vytauto Landsbergio - RuBaltic.Ru pastaba) nefilmavo.“ Jis toks žymus žmogus, žymus pasakorius“,-sako Sergėjus Loznica.

Tai yra, režisierius pripažįsta, jog jo autorinis sumanymas pagrįstas feiku.

Pavyzdžiui, „tautos tėvo“ žmona Gražina Ručytė-Landsbergienė kartu su režisiere Agne Marcinkevičiūte sukūrė trilogiją „Vytautas Landsbergis: mintys ir kūryba“. Bet to jai pasirodė maža, ir ji paruošė dar vieną filmų seriją „Lūžis prie Baltijos“ (pasakojimo centre - vis tas pats pagrindinis herojus).

„Į klausimą, ką ji gali pasakyti žmonėms, kurie mano, jog Lietuvos nepriklausomybė labai stipriai siejama su Landsbergio vardu, moteris atsakė, jog nesikoncentruoja tik į savo vyrą, bet niekas negali neigti Landsbergio vaidmens atgimimo procese“,- 2013 metai rašė Lietuvos naujienų portalas „Delfi“.

2003 metais Landsbergio sūnus sukūrė juostą su iškalbingu pavadinimu „Visa tiesa apie mano tėvą“, Rusijos režisierius Aleksandras Sokūrovas buvusį Seimo pirmininką padarė savo filmo „Paprastoji elegija“ herojumi.

Tai ne visas sąrašas, bet to pakanka, kad suprasti: dokumentinių filmų apie Landsbergį apstu. Ar galėjo apie tai nežinoti S. Loznica?

Surizikuosime paspėlioti, jog jo naujas dokumentinis projektas tapo šalto passkaičiavimo rezultatu. Visų pirma, tema be abejonių, labai palanki. Nepažymėti nei vienu prizu juostą apie „blogio imperijos“ žlugimą – tai tas pats, kas ir nepriklupti ant vieno kelio prieš juodaodį.

Ir čia Loznica neapsiriko! 2021 metais Lietuvos kino centras išskyrė 1,8 milijono eurų meninių, animacinių bei dokumentinių filmų gamybai. Maždaug 10 procentų šios sumos (184 tūkstančiai eurų) gavo Ukrainos režisieriaus kūrinys.

Šiuolaikinio kinematografo mastais, pinigai ne kokie. Na bet ir Loznica – ne Stivenas Spilbergas, kuris filmuoja eilinį „oskarinį“ blokbasterį. Remiantis filmo „Misteri Landsbergis“ aprašymu paaiškėja, jog jo turinį sudaro kino kronikos iš archyvų ir pokalbių su pagrindinių herojumi įrašas. Nei tas, ne kita didelių išlaidų nereikalauja.

O Klaipėdos miesto municipalinės tarybos narė Nina Puteikienė ne pabijojo parašyti savo Facebook paskyroje: „Tokių sumų užtektu mažiausiai dvejiems filmams: ir apie Ozolą, ir apie Landsbergį. Demokratinės valstybės ne bando kurti asmens kultą, jos supranta, jog istorija – ne vieno žmogaus rankų ir minčių darbas“.

Tarp kitko, pas Lietuvos kino centrą buvo dar viena motyvacija. Finansinės pagalbos į juos kreipėsi ne paprastas režisierius iš užsienio. Sergėjus Loznica – baltarusių kilmės ukrainietis. Kaip sakoma, du viename...

Lietuviškos šalies lūkesčius Landsbergio šlovintojas tikriausiai pateisino. Jau gana to, jog jo kino juostos chronometražą sudaro, nei daugiau, nei mažiau, 246 minutės. Apie juostos menines savybes mes, suprantama, negalime spręsti (viešai ji dar nebuvo demonstruojama), bet keturias valandas klausyti susenusio politiko pasakėles - tai gana abejotinas malonumas netgi „Tėvynės Sąjungos – Lietuvos krikščionių demokratų“ rikėjams.

„Sudėtinga atgaivinti istoriją. Dar sudėtingiau paversti ją jaudinančia, aktualia ir praturtinančia, padaryti taip, jog būk tai mes pergyvename visą tai, kas vyko. Visuose meistriškumo lygiuose laimėjęs filmas žymi didelį pasiekimą ir visapusiškai išnagrinėja, kokį vaidmenį vienas žmogus, viena tauta ir viena istorinė akimirka gali suvaidinti vis dar vykstančioje pasaulinėje kovoje už laisvę ir nepriklausomybę“, – argumentavo IDFA 2021 žiuri nariai „Misterio Landsbergio“ pergalę.

Gaunasi tokia istorinė „matrioška“: vienas žmogus suvaidino atitinkamą vaidmenį „vienos tautos“ istorijoje, o tauta suvaidino atitinkamą vaidmenį „pasaulinėje kovoje už laisvę ir nepriklausomybę“.

„Šią istoriją apie okupacijos pabaigą galima vertinti ir kaip apysaką apie dviejų asmenybių – Landsbergio ir Gorbačiovo buvimą opozicijoje. Sergėjaus Loznicos pašnekovas iki šiol vertina paskutinį SSSR prezidentą kaip savo oponentą ir su malonumu prisimena visus ėjimus šachmatų partijoje su Gorbačiovu, kurią jis laimėjo“, - rašo „Radijo Svoboda“ (Rusijoje pripažinta užsienio agentu – RuBaltic.Ru pastaba).

Akivaizdu, jog per visą filmą ši mintis driekiasi raudona gija: puikus Landsbergis aplošė pirmąjį ir paskutinį SSSR prezidentą, Štai ką sako pats Loznica apie „lietuviškos demokratijos patriarchą: „Aš seniai žavėjausi Vytautu Landsbergiu, dar tada, kai jis 1989 metais išdrįso prabilti apie Molotovo – Ribentropo paktą, lydymas salėje sėdinčių leliojimo. Tai buvo labai tikslus ėjimas. Po to aš stengiausi spaudoje ieškoti jo tekstus, jie labai dažnai sutapdavo su mano mintimis apie tai, kas vyksta, kadangi jis sako tiesą, negudrauja, pasako labai iškalbingai ir tiksliai“.

Palyginimui – to pačio Loznicos žodžiai: „Filmui Rusijos televizijos archyve mes paprašėme Liaudies deputatų suvažiavimo medžiagą. Aš buvau nustebintas, kaip kitaip tada aš vertinau Gorbačiovo figūrą. Iš viso, kaip žmonės galėjo klausyti tai, ką jis sakė? Stebina, kokios bereikšmės ir nesurištos buvo jo kalbos“.

Tai yra, netgi oratorinio meno lygyje dieviškasis Landsbergis buvo pranašesnis už savo oponentą. Ir tai tik vienas iš daugelio jo privalumų.

Lyginant su juo Marvel visatos herojai – apgailėtini diletantai!

Bet Lietuvos gyventojams visą tai jau seniai žinoma.

Kiek turi dar užmokėti mokesčių mokėtojai už tai, kad jų „patriarcho“ „didybė“ visam pasauliui taptų akivaizdi?

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 20 — id: `scraped:rubaltic_lt:52c0ac1cfe0de8d3`

**Title:** Aistros dėl „Belaruskalij“:   sankcijos Baltarusijai skaldo Lietuvą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
„Belaruskalij“ partneriai Pabaltijyje gali nepergyventi, jog juos paveiks amerikiečių sankcijos. Apie tai pranešė „Lietuvos geležinkelių generalinis direktorius Mantas Bartuška, nurodydamas į JAV iždo departamento Užsienio aktyvų kontrolės biurą (OFAC). OFAC pareigūnų paaiškinimai jam reiškia, jog Klaipėdos uostas neprivalo atsisakyti baltarusiškų trąšu tranzito. Paprasčiausiai, Lietuvos valdžia ieško formalių pretekstų verslo, kuris neatitinka jų „vertybių politikai“, sunaikinimui.

Gruodžio 8 dieną baigiasi sandorių užbaigimo su „Belaruskalij“ terminas, kurį Jungtinės Valstijos nustatė saviems kompanionams. Čia pagrindinis žodis –„saviems“. Kai Lietuvos susiekimo ministras Marius Skuodis pirmą kartą pareiškė apie tai, jog baltarusių trąšos palieka Klaipėdos uostą, analitikos portalas RuBaltic.Ru ne atsitiktinai atkreipė dėmesį į tai kad JAV sankcijos liečia išimtinai amerikietiškus asmenis (U.S. persons).

Prie ko čia Lietuva? Belaukiant „iks valandos“ dabar ir pats Skuodis patvirtina, jog ne viskas yra vienareikšmiška: „Europinės sankcijos kaip ir aiškios, dėl JAV sankcijų vyksta daug diskusijų. Be to, per vieną dieną gali daug kas pasikeisti, JAV ir ES gali imtis naujų sankcijų, jeigu mūsų kaimynystėje niekas nesikeis. (...) Sankcijos nėra įvestos dėl sankcijų, režimui tereikia pakeisti savo elgesį ir tranzitas, kuris vyko, tarp mūsų šalių ir apskritai galės toliau tęstis“.

Taip kalbėjo Skuodis 2021 metų lapkričio mėnesį. O štai ką jis sakė rugpjūtyje: „Bankai nepriims atsiskaitymų už suteiktas paslaugas. Įmonės, jeigu yra sankcionuotas subjektas, atsisako su juo turėti bet kokių verslo santykių vengdami rizikos ir galiu tvirtai teigti, kad nuo gruodžio, kai sankcijos įsigalios, trąšos per Lietuvą nustos judėti“.

Kas atsitiko? Kodėl prieš trejus mėnesius baltarusiško tranzito klausimas rodėsi jau išspręstas, o dabar jau viskas ne taip jau vienareikšmiška? Reikalas tame, jog „Lietuvos  geležinkelių“ generalinis direktorius Mantas Bartuška kreipėsi paaiškinimų į amerikietiškąją „specialiąją sankcijų tarnybą“  - į JAV iždo departamento Užsienio aktyvų kontrolės biurą (OFAC).

„Pokalbio metu gavome patikinimus ir paaiškinome, kad dabartinėje apimtyje, jei grandinėje nėra JAV subjektų, sankcijos netaikomos“,- sakė Bartuška.

Juolab, spalio mėnesio pradžioje pats Bartuška lankėsi Jungtinėse Valstijose ir konsultavosi pas amerikiečius dėl sankcijų „Belaruskalij“. Informacijos agentūra BNS tvirtina, jog tai buvo pagrindinis jo kelionės tikslas.

Bendrai, kai amerikiečiai nori išplatinti savo sankcijas užsienio kompanijoms, tai jie daro atvirai. Tam yra „Šiaurinio srauto-2“ precedentas.

2019 metų pabaigoje JAV jam įvedė sankcijas. Šveicarų kompanija Allseas, kuri tiesė dujotiekį, sustabdė darbus, paprašė JAV Finansų ministerijos paaiškinimų ir tik po to galutinai paliko projektą.

Bet su Lietuva viskas paprasčiau.

Bet kokia kompanija gali pasekti LG generalinio direktoriaus pavyzdžiu  ir išsiaiškinti, ar ji gali bendradarbiauti su baltarusiškų krovinių siuntėjais. Šia nėra ko spėlioti. Jei pačios JAV neigia eksteritorinį sankcijų „Belaruskalij“ pobūdį, tai kodėl jas turi vykdyti Lietuva?

Naivu manyti, jog bankai, siekdami išsaugoti savo reputaciją, atsisakys priiminėti mokėjimus už baltarusiškų trąšų perkrovą Klaipėdos uoste (apie tai rašo BNS, remdamasi kažkokiu tai ekspertu).

Arčiau visų prie to buvo Norvegų Yara, bet netgi ir ji toliau sėkmingai perka trąšas pas „paskutinį Europos diktatorių“. Apie kokią žalą reputacijai galima kalbėti, jei nei lietuviški, nei amerikietiški, nei europietiški įstatymai nedraudžia bankams lydėti baltarusiško kalio tranzitą?

Bazinė Skuodžio „prognozė“, jog Batką visgi išvarys iš Klaipėdos, faktiškai yra spekuliacinio pobūdžio.

Pageidaujamą ministras pateikia kaip tikrovę.

Valdantiesiems konservatoriams tai principo reikalas, o potencialų negatyvinį efektą šalies ekonomikai jie skaito nežymiu.

Surizikuosim nuspėti, jog tiesiog už keleto dienų Lietuvoje prasidės kova (galimai, ilgai trunkanti) dėl „Belaruskalij“ produkcijos. Ir geležinkelis, ir Klaipėdos uostas, su šiuo verslu afeliuoti vietinės valdžios atstovai turi priešintis nemotyvuotam tranzito atsisakymui.

Pirmu smuiku čia gros Birių krovinių terminalas, kuris tiesiogiai užsiima baltarusiškų trąšų perkrova. Kitoje barikados pusėje – Ministrų kabinetas ir Seimo koalicija su jų „vertybių politika“.

Ypatingai įdomu bus stebėti ką darys Lietuvos prezidentas Gitanas Nausėda. Prieš keletą mėnesių jis viešai paskelbė, jog abejoja galimų tranzitinių sankcijų „Baltaruskalij“ efektyvumu, kurios bus naudingos rusiškiems Baltijos uostams.

Ar surizikuos jis tai pasakyti dabar? Vargu.

Tikimiausiai, Nausėda kovoje nedalyvaus.

Kam prezidentui tokia „laimė“? Jam jau laikas pagalvoti apie perrinkimą antrajai kadencijai.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```
