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

### Article 1 — id: `scraped:rubaltic_lt:928fd9da9f46c6b5`

**Title:** Rusofobijos eurokomisarė: Grybauskaitei tikimasi sukurti naujas pareigas

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Europos komisijoje (EK) ES šalių atstovams dalinami portfeliai: Lietuvos prezidentas ir premjeras ta proga kalba, kaip svarbu „nugriebti“ solidų postą atsinaujinusios Europos sąjungos vadovybėje. Oficialus Vilnius net pateikė pasiūlymą įvesti naujas pareigas, užimti kurias turėtų lietuvis, ir buvusios prezidentės Dalios Grybauskaitės klapčiukai norėtų matyti jose „Raudonąją Dalią“.

„Lietuva sieks svarbaus portfelio tose sferose, kuriose ji sukaupė daugiausia įdirbio ir kompetencijos, — praneša Lietuvos ministrų kabineto spaudos tarnyba po vyriausybės vadovo Sauliaus Skvernelio susitikimo su eurokomisaru energetikos klausimais Marošu Šefčovičium. — Prioritetinės yra sferos, susietos su ekonominiu vystymusi ir energetika, o taip pat būtinas žingsnis į priekį saugant išorinę Europos sąjungos sieną“.

Apie kokį įdirbį ekonomikos sferoje eina kalba? Ko gali išmokyti Europą šalis, kuri tenkinasi Briuselio „sausu daviniu“ ir maldauja infrastruktūros projektams eurofondų finansavimo?

Neseniai atsirado dar vienas nuostabus „įdirbis“: statistinė agentūra Eurostat paskelbė Europos sąjungos šalių ekonominių rodiklių reitingą.

Ir esant tokiam fonui Skvernelis pretenduoja turėti atstovybę ekonominiame Europos komisijos bloke?

Lietuvos kompetencija energetikos sferoje — atskira kalba. Čia Pabaltijo respublika tikrai sukaupė unikalią patirtį. SGD terminalo Klaipėdoje nuomą, kurią pats premjeras pavadino „mokesčių mokėtojų našta“, galima drąsiai pavadinti amžiaus afera.

Ir „Europos sąjungos išorinių sienų apsaugos“ klausimu Skvernelis akivaizdžiai pasikarščiavo.

Vilnius gali pasigirti tik išlaidų gynybai didinimu ir garbinga dešimta vieta tarp pasaulio šalių, sparčiausiai didinančių karinį biudžetą. Tiesa, ant gynimosi nuo „rusų agresijos“ altoriaus teko padėti socialinę sferą. Vakarų Europa vargu ar norės pasekti šiuo pavyzdžiu.

Skvernelio pastangos „nugriebti“ naujoje Europos komisijos sudėtyje solidžias pareigas atrodo kvailai, tačiau dėsningai. Praeitoje ES vadovybėje Lietuvos vaidmuo buvo labiau nei kuklus. Net kaimynų fone.

Buvęs Latvijos premjeras Valdis Dombrovskis Junkerio komisijoje buvo užėmęs viceprezidento ir komisaro euro bei socialinio dialogo klausimais pareigas. Vienu iš šešių viceprezidentų taip pat tapo buvęs Estijos vyriausybės vadovas Andrus Ansip.

O lietuviui Vyteniui Andriukaičiui — tos šalies, kuri pretenduoja tapti regiono lydere, atstovui atiteko sveikatos apsaugos ir maisto saugumo sferos.

Žodis „saugumas“ Lietuvai ne šiaip sau garsas. Jau daugelį metų ji kovoja dėl „energetinio saugumo“ ir pasiruošusi atremti nematomo priešo ES rytiniame pasienyje puolimą. Net ekonomikoje pirmauja saugumo sumetimais — specialios tarnybos atkakliai kaunasi su Rusijos oligarchais ir jų įtakos agentais šalies viduje.

Po rinkimų į Europos parlamentą situacija iš esmės nepasikeitė. Buvusiai prezidentei Daliai Grybauskaitei neatiteko vadovaujančių pareigų, kurių ji akivaizdžiai troško. Į ES vadovybę išvis nepateko nė vieno Centrinės ir Rytų Europos politiko. Skvernelį tai nemaloniai nustebino.

Apie tai jis pasakė prabėgomis, kalbėdamas apie užsitęsusias kandidato į eurokomisarus paieškas: „Kuo ilgiau mes delsiam, tuo mažiau ant stalo liks tų portfelių, beje, tokių, kokių mes norėtume — įtakingų. Nes aš manau, jog Lietuva, kaip Centrinės ir Rytų Europos valstybė, nepakankamai atstovaujama po EK vadovybės formavimo sprendimų“.

Taigi sudėti ginklus išdidi Pabaltijo respublika neketina. Nenuskilo vadovaujančios pareigos, pretenduosime į įtakingus Europos komisijos postus.

Užimti jas turėtų tik Lietuvos atstovas. Kas sugalvojo, tam ir pirmenybė!

Deja, šis klausimas nesvarstomas. O parinkti Lietuvos atstovo EK kandidatūrą būtina nedelsiant. Priešingu atveju visi reikšmingiausi portfeliai bus išdalinti iki pakviečiant Vilnių dalyvauti derybose. Dėl to nerimauja ne tik Nausėda.

“Aš taip pat manau, jog mes vėluojame. Tačiau aš apie tai kalbėjau jau seniai, — pareiškė užsienio reikalų ministras Linas Linkevičius. Beje, neseniai Lietuvos URM vadovas pats troško gauti vieną iš 27 Europos komisijos portfelių. Ir tai suprantama: pasikeitus valdžiai, diplomatinė Linkevičiaus karjera — vieno iš artimiausių Grybauskaitės bendražygių — gali pradėti riedėti nuokalnėn.

Ką tokiu atveju Grybauskaitė būtų tempusi su savim į Briuselį? Tą, kuris daugelį metų paklusniai žvelgė į burną “valdovei”, ir net buvo kalbama, kad galėtų tapti prezidento pareigų perėmėju.

Tačiau “valdovė” pati atsidūrė prie suskilusios geldos. Dar daugiau: iš užtrukusių derybų sprendžiama, jog atstovauti Lietuvai Europos komisijoje petenduoja ne tik ji. Pasak Nausėdos, svarstomos trys kandidatūros.

Su Skverneliu jie riejasi seniai ir atvirai. Gal todėl vyriausybės vadovas ir prabilo apie “svarbų portfelį” Europos komisijoje. Kas iš Lietuvos atstovų gali pretenduoti į pareigas ekonominiame arba energetiniame bloke, jei ne buvusi prezidentė? Be to, ji sukaupė patirtį dirbdama biudžeto ir finansinio planavimo komisare.

Nausėdą tokia perspektyva nedžiugina, todėl jis mielu noru išlydėtų ją į Briuselį.

Klausimas tik tame, kas konkrečiai gali atitekti buvusiai prezidentei. Jau minėtame sveikatos apsaugos ir maisto saugumo komisaro poste Grybauskaitė gal ir atrodytų savo vietoje.

Pagyvenę žmonės dažnai lankosi poliklinikose, renka sveikatos receptus ir augina daržoves priesodybiniuose sklypuose.

Vargu ar Berlynas su Paryžium jai pasiūlys ką nors rimtesnio.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 2 — id: `scraped:rubaltic_lt:2bf1e39b2b099cbd`

**Title:** Lietuva pralaimėjo „Gazpromui“ ir negaus rusiškų pinigų

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Švedijos apeliacinis teismas galutinai atėmė iš Lietuvos viltį gauti rusiškas dujas žemomis kainomis. Nesuinteresuota pusė vėl pripažino „Gazpromo“ dujų kainą Lietuvai rinkos kaina, neaptiko monopolijos piktnaudžiavimo ir nepareikalavo išmokėti lietuviams kompensacijos. Vilniuje galutinai žlugo eilinė idėja uždirbti Rusijos sąskaita, demonstruojant save „nekalta Rusijos agresijos auka“.

Apeliacinis Švedijos apygardos Svea teismas galutinai atmetė Lietuvos prašymą peržiūrėti Stokholmo arbitražinio teismo 2016 m. birželio 22 dienos nutartį, kai pastarasis užėmė“Gazpromo“ pusę užsitęsiusiame Lietuvos ginče su Rusijos dujų monopolininku.

Ta diena tapo juoda Lietuvos energetikos politikai ir diplomatijai. Stokholmo arbitražas neįžvelgė monopolijos piktnaudžiavimo energetikos rinkoje, formuojant 2006–2015 metais Lietuvai dujų kainą.

Rusiškų dujų kaina buvo pripažinta rinkos ir teisinga. Lietuvos reikalavimas išmokėti jai 1,5 milijardo eurų „Gazpromo“ kompensaciją neva už permokėjimą buvo atmestas.

Lietuvos valdžios tada pareiškė, kad jos su tuo nesitaikys ir paduos apeliaciją. Ir štai — po trejų metų galutinė apeliacinio teismo nutartis: visos Lietuvos pusės pretenzijos atmestos, ankstesnė nutartis konflikto su Rusijos koncernu klausimu nebegalioja, ir Lietuva privalo ją pilnumoje įvykdyti.

„Tokiu būdu galutinai patvirtintos išvados Stokholmo arbitražo, kurios atmetė visus Lietuvos reikalavimus rusiškų dujų pirkimo sąlygų klausimu“, — apie švedų apeliacinio teismo nutartį teigia „Gazpromo“ spaudos tarnyba.

„Energetikos ministerija vertina teismo nutartį ir jo motyvus. Tik susipažinus su nutarties argumentacija ir jos motyvais bus galima spręsti, ar galimi tolimesni veiksmai ir būtent kokie“, — naujienas iš Švedijos komentuoja Lietuvos vyriausybė.

Vilnius atsisako ginčų su „Gazpromu“ baigtį vertinti kaip savo pralaimėjimą ir įkyriai tvirtina, jog pastarųjų metų Lietuvos energetinė politika — vien tik pasiekimai.

„Nepaisant aktyvaus „Gazpromo“ pasipriešinimo, Lietuvai pavyko liberalizuoti gamtinių dujų rinką ir užtikrinti palankesnes dujų tiekimo vartotojams sąlygas“, — pareiškė Energetikos ministerija, matomai turėdama omenyje plačiai nuskambėjusią 20 proc. nuolaidą dujoms Lietuvai, kurią „Gazpromas“ jai suteikė prieš penkerius metus ir kurią lietuviai sieja su suskystintų gamtinių dujų terminalo Klaipėdoje atsiradimu.

Penkeri metai nesuprantami, kuo jie čia dėti, jeigu nuolaidos dujoms atsirado gerokai prieš SGD terminalo Independence Klaipėdoje atsiradimą. Taip pat nesuprantama, apie kokias palankias dujų tiekimo vartotojams sąlygas eina kalba.

Lietuvos įmonės kovoja su SGD terminalu ir prašo valdžių atsisakyti būtinybės pirkti jo produkciją: suskystintos dujos per brangios, jos jas visas prives prie bankroto. Pačios valdžios dėl to nesiginčija, energetikos ministro ir vyriausybės vadovo lygyje vadindamos Independence „našta“ Lietuvos mokesčių mokėtojams.

Tad kame slypi rinkos liberalizavimo nauda ir kur palankios tiekimo sąlygos?

Tačiau po velnių tą propagandą. Dar daktaras Gebelsas sakė, kad kuo labiau melas nerealus, tuo didesnis noras atsiranda juo tikėti.

Galutinis Lietuvos pralaimėjimas teismuose su „Gazpromu“ — tai ne šiaip valstybinės propagandos pralaimėjimas. Žinoma, ir jis. Lietuviams tiek metų buvo kalama, kad jie yra Maskvos „melsvo vėzdo“ nekaltos aukos ir kad Lietuvos nepriklausomybė patiria energetinį šantažą, o Stokholmo arbitražas (o dabar ir arbitražinis teismas) daro išvadą, kad dujų kaina sąžininga ir niekas niekam neišsukinėja rankų.

Tačiau ne tas svarbiausia.

Priversti rusus mokėti ir atgailauti — Lietuvos užsienio politikos esmė rytų kaimyno atžvilgiu. Įprotis dešimtmečiais Tarybų Sąjungos laikais gauti iš Maskvos veltui pinigų taip įaugo į Lietuvos politikų kraują, kad jie visus 28 „antrosios nepriklausomybės metus“ daro viską, kad tik Kremlius vėl jiems mokėtų. Tik skirtumas tame, kad jiems nereikėtų imituoti „tautų draugystės“, kaip tais prakeiktais tarybiniais laikais, o būtų galima gauti iš Rusijos pinigų ir tuo pačiu metu ją atvirai nekęsti.

Ir todėl apskaičiavimas galutinės materialinių kompensacijų už „sovietinę okupaciją“ sumos tapo Lietuvoje nacionaline sporto šaka.Visokiausios komisijos ir ekspertų grupės ketvirtį amžiaus lenktyniavo tarpusavyje, spręsdamos, kiek reikėtų pareikalauti iš šalies — TSRS perėmėjos.

Skaičiai siekė 834 milijardus dolerių, tai yra tema buvo strateginė, ir ji susilaukė rimto dėmesio. Nusimatė, jog kompensaciją už „okupacijos nuostolius“ Rusija mokės be galo, o Lietuva už tuos pinigus sočiai gyvens iki pasaulio pabaigos.

Tada Lietuvos vadovybė surezgė kitokį planą. Paskelbė rusiškų dujų kainą dirbtinai padidintą ir poliškai motyvuotą. Ir nutarė įžūliai pareikalauti iš „Gazpromo“ sumažinti Lietuvai dujų kainą. O kai „Gazpromas“ atsisakys, jo poziciją pavadinti energetiniu šantažu, kerštu ir išvis Lietuvos „ekonomine okupacija“.

Pagrįsta kaina šiuo atveju oficialų Vilnių visiškai nedomina. Priešingai, Lietuva kovėsi dėl nepagrįstos, nerinkos rusiškų dujų kainos.

Tai yra vyko eilinės variacijos amžina tema „mokėti ir atgailauti“. Nenorite mokėti kompensacijos už „sovietinę okupaciją“? Mokėsite kompensaciją už per didelę dujų kainą. Gaila mums pinigų? Tieksite dujas mūsų kainomis.

Ir čia Lietuvos politikai vėl „tūpė į balą“. „Permokėjimo“ kompensacijos epopėja baigėsi taip pat, kaip ir kompensacijos už „okupaciją“. Neuždirbtų pinigų iš Rusijos jiems nematyt kaip velniui rojaus, o eilinis bandymas „išmušti“ pinigus baigėsi tuo, kad pinigus Rusijai mokės Lietuva.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 3 — id: `scraped:rubaltic_lt:2aaea3aa0e006987`

**Title:** Lietuva ir Lenkija reikalauja iš ES pinigų „energetinės nepriklausomybės“ nuo Rusijos reikmėms

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Kompanijos — Lietuvos ir Lenkijos elektros tiekimo linijų operatorės Litgrid ir PSE — prašo Europos Sąjungos skirti lėšų ETL sandūros potencialo per Baltijos jūrą tyrimui. Reikėtų dešimties milijonų eurų, kurie galėtų būti skirti, jei paraiškai pritars Programų inovacijų ir tinklų prie Europos komisijos vykdomoji įstaiga (EVĮ). Suma juokinga, tačiau pačios sandūros statyba pareikalaus iš Lietuvos ir Lenkijos šimtų milijonų dolerių. Neabejotinai ir šiuo atveju didesnę dalį lėšų jos tikisi išreikalauti iš Europos Sąjungos.

Pasak Litgrid vadovo Daivio Virbicko, birželio 11 dieną kompanija paprašė EVĮ paramos. Lietuvos dalis tiriant jūros sandūrą Harmony Link sudaro 8 milijonus eurų — pusę šios sumos Vilnius planuoja gauti iš Europos Sąjungos. Lenkija tikisi 6 milijonų.

Maždaug tuo pačiu metu „pamelžti“ EVĮ sumanė Lietuvos ir Latvijos dujų transportavimo sistemų operatoriai. Jie prašo pinigų bendro dujotiekio praplėtimui. Suma taip pat nedidelė — tik vos daugiau 7,5 milijonų eurų. Tačiau jūros sandūros atvejo pagrindinės išlaidos dar ateityje.

Visai neseniai Briuselyje Europos komisijos, Lenkijos ir Pabaltijo šalių vadovai patvirtino šio nepaprasto proceso kalendorinį grafiką. „Delain“ nesikeičia — 2025 metai.

Pirmame etape Lietuva, Latvija ir Estija turi atnaujinti ir sustiprinti savo vidaus tinklus. Po to planuojama padidinti veikiančios elektros sandūros LitPol Link galingumus, o paskui — įkurti dar vieną energetinį tiltą tarp Lenkijos ir Lietuvos.

Pats sprendimas dėl aukštų voltų nekintamos srovės kabelio paklojimo Baltijos jūroje buvo priimtas praeitų metų gruodžio mėnesyje. Sutartį pasirašė tie patys Litgrid ir PSE operatoriai, sutarę bendromis jėgomis ieškoti investorių. Projekto Harmony Link atžvilgiu šis klausimas galimai taps skausmingiausiu.

Surasti šias lėšas planuojama jau kitais metais.

Kol kas lietuviai kupini optimizmo. Pirmajam Pabaltijo energijos sistemos sinchronizavimo su kontinentine Europa etapui Europos komisija metų pradžioje jau skyrė 323 milijonus eurų, o tai sudaro 75 proc. išlaidų. „Mes planuojame, jog ir antrojo bei trečiojo etapų finansavimo intensyvumas bus toks pat“, — sako Litgrid valdybos vadovas Rimvydas Štilinis.

Tačiau koks bus intensyvumas, sunku nuspėti. Europai šiandien kaip niekada aktuali tampa patarlė: „Ne apie taukuotą gyvenimą kalba — kad tik gyviems išlikti“. Apie tai byloja ne rusų propaganda, o duomenys pačios Europos komisijos, kuri svarstys Harmony Link statybos finansavimo klausimą.

Vasario mėnesį ji ženkliai sumažino didžiausių Europos ekonomikų augimo prognozes.

Taip, pavyzdžiui, Vokietijos BVP 2019 metais turi ūgtelti 1,1 proc. vietoj 1,8, kaip atrodė anksčiau. Italijoje viskas dar blogiau: 0,2 proc. vietoj 1,2.

Visumoje prognozė Europos zonoje krito nuo 1,9 proc. iki 1,3, ir tai galimai ne pats blogiausias scenarijus. „Rizika lieka rimta ir susiklostė ji pagrindinai dėl rimtų klaidų viso pasaulio ekonomikos politikoje“, — pažymi Europos komisija.

Dotacijos tai pačiai Lietuvai pagal ilgalaikio ES biudžeto projektą 2021–2027 metams turi sumažėti beveik ketvirtadaliu. Vilnius, žinoma, ketina ginčytis dėl šio sprendimo. Tačiau gali būti, jog smagratis pasisuks kiton pusėn ir ES dar stipriau suverš diržą ant Pabaltijo respublikos juosmens. Tada teks užmiršti dosnias infrastruktūrų ir energetinių projektų dotacijas. Harmony Link — vienas pirmųjų pretendentų.

Kodėl?

Tarp Lenkijos ir Lietuvos jau veikia LitPol Link elektros tiekimo sistema, kurios pralaidumo galimybes planuojama padidinti. Tai yra kalba ėjo apie vieną liniją ir vieną nekintamos srovės kabelį. Interviu analitiniam portalui RuBaltic.Ru Pasaulinės energetikos tarybos Lietuvos komiteto garbės narys Algirdas Stumbras perspėjo dėl tokios schemos pavojingumo: „Kas gali apdrausti sistemą nuo teroristų akto arba žaibo? Niekas. O siūloma eletros tiekimo tarp Lenkijos ir Lietuvos schema labai nepatikima“.

Atrodo, jog praeitų metų gruodžio mėnesį Litgrid ir PSE nutarė apsidrausti, paklodamos Baltijos jūroje dar vieną kabelį. Žvelgiant iš saugumo sumetimų, sprendimas atrodo visiškai logiškas. Nedirba Litpol Link — elektros energija paduodama per Harmony Link. Arba atvirkščiai. Su elektra menki juokai, visada reikia turėti patikimų rezervų.

Baltijos jūros dugnu jau įrengtas elektros energetinis ryšys Lietuvos su Švedija — sandūra NordBalt, kuri pastoviai genda. Dėl jos remonto Lietuvoje kyla elektros energijos kainos.

Kitas rimtas klausimas — o kam išvis reikalinga papildoma sandūra su Lenkija, jei lenkai tiekia Lietuvai mažus elektros energijos kiekius?

Čia vertėtų prisiminti Lietuvos kompanijos „Energijos tiekimas“ planus pradėti eksportuoti elektros energiją į Lenkiją. Tiesa, savas reikmes viršijančios savos gamybos elektros Pabaltijo respublika neturi — kalba eina apie schemą „pirk ir parduok“. Pavyzdžiui, pirk iš skandinavų ir perparduok lenkams. O per Lenkiją atsiveria išėjimas į plačią vokiečių rinką.

„Ekonominis tokių tiekimų tikslingumas visiems energijos tiekimo dalyviams neakivaizdus, tačiau matosi Pabaltijo šalių elitų suinteresuotumas susieti „Senąją Europą“ su Pabaltijo interesais ne tik stumiant prie Rusijos sienų NATO karinę infrastruktūrą, bet ir kuriant energijos tilto iš Skandinavijos į Centrinę Europą infrastruktūrą“, — pažymi ekonomikos mokslų daktaras Aleksejus Balašovas.

Teoriškai Lietuva tikrai galėtų uždarbiauti elektros energijos tranzitu.

RF jau pareiškė, jog sutinka tiekti energiją ir po to, kai Pabaltijis pasitrauks iš BRELL. Baltarusijos valdžios taip pat neatsisako eksportuoti elektros energijos, įvedus rikiuotėn BelAE. Tačiau ir Lenkija, ir Lietuva šių pasiūlymų kategoriškai kratosi.

SGD terminalas Klaipėdoje, pasak Lietuvos valdžių, išklibino „Gazpromo“ monopoliją ir privertė jį taikyti dujoms nuolaidas. Kodėl pasinaudoti tokiu triuku Lietuva nenori elektros energetikos sferoje? Argi reikia savo noru nustumti nuo savos rinkos tiekėjus, jeigu pasiūlų gausa įtakoja kainų mažėjimą?

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 4 — id: `scraped:rubaltic_lt:5a25f6829864d283`

**Title:** Dabar jau viešai skelbiama: Grybauskaitė „praskrido” virš visų ES pareigų

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Europos lyderiai aptarė ir suderino kandidatus į aukščiausius valdžios postus Europos Sąjungoje. Tarp jų nespėjamai neatsirado Lietuvos prezidentės Dalios Grybauskaitės vardo. Istorijos analų vertas Grybauskaitės „šuolis“ į Europos Sąjungos valdžios viršūnę nevirto tikrove: buvusios kolegos leido suprasti baigiančiai prezidentės pareigas Grybauskaitei, kad jos griežta antirusiška pozicija nedomina Europos.

Nauja Europos Komisijos – aukščiausiojo ES vykdomosios valdžios organo – pirmininke Europos Vadovų Taryba nusprendė paskirti Vokietijos gynybos ministrę Ursulą von der Leyen. Pačios Europos Vadovų Tarybos pirmininku taps Belgijos premjeras Charles Michelis. Europos Parlamento pirmininku tapo italų socialistas Davidas-Maria Sassoli.

Europos Centrinio Banko vadovo pareigos užims Tarptautinio valiutos fondo (TVF) vadovė, buvusi Prancūzijos ekonomikos ministrė Christine Lagarde. ES užsienio politika ir gynyba vadovaus Ispanijos užsienio reikalų ministras Josepas Borrellis. Europos Parlamento pirmininko pareigas buvo nuspręsta pavirsti rotacinėmis: pirmąją kadencijos pusę jas eis Europos liaudies partijos atstovas, o antrąją pusę – socialdemokratų atstovas.

Kandidatų skirimą į aukščiausias ES valdžios pareigas dar turi patvirtinti Europos Parlamentas, bet šita procedūra yra techninė. Pagrindinės ES šalys apsisprendė ir susitarė dėl kandidatų, o jų deputatai Europos Parlamente turi daugumą balsų.

Bet kokiu atveju apie labai ambicingos Baltijos valstybės ir jos tokios pat ambicingos prezidentės rezultatus galima kalbėti jau dabar.

Europos gigantai, įsitraukę į viliojančią Briuselio administracinio pyrago dalybą, net nepastebėjo, kad Europos Sąjungos skubiame valstybių vadovų susitikime dalyvavo ir Lietuvos prezidentė, kuri irgi norėjo gauti kokias nors aukštas pareigas.

Grybauskaitei teko su savo norais likti vienai, kol Vokietija ir Prancūzija dalino jėgas ir įtaką „Vieningoje Europoje“ artimiesiems 5 metams.

Tuo tarpu visa Lietuva pastaraisiais metais tikėjo, jog „mūsų Daliai“, kai pasibaigs prezidentės kadencija, lemta padaryti išskirtinę karjerą Europoje. Lietuvos politikai tikėjo, kas Jos Prakilnybė priklauso pačių įtakingiausių žmonių skaičiui Briuselyje, lygiai taip pat, kaip Nikolajaus Gogolio kūrinio veikėjai-biurokratai įtikino vienas kitą, kad Chlestakovas Peterburge – asmuo išskirtinis.

Jie ginčijosi tik dėl to, kuo taps Grybauskaitė, kai baigs eiti prezidentės pareigas – Europos Vadovų Tarybos arba Europos Komisijos pirmininke? Turint atmintyje konfūzą su Ukraina per „Rytų partnerystės“ viršūnių susitikimą Vilniuje, po kurio Grybauskaitės galimybės pirmininkauti Europos Komisijai išnyko, dauguma susitarė, kad ji vadovaus Europos Tarybai.

Niekas negalėjo patikėti tuo, kad po 2019 metų Baltijos „geležinė ledi“ Briuselyje liks niekuo. Nors, o ko stebėtis?

Tai buvo aiškiai suprantama visur, išskyrus Lietuvą, kurios politikai ir gyventojai buvo įsitikinę jog Briuselyje Grybauskaitė gaus pelnytas pareigas. Europos Sąjungos šaltiniai ne kartą sakė amerikiečių bei lenkų žiniasklaidai, kad Lietuvos lyderės šansai tapti ES lydere artėja į nulį, bet Lietuvos respublikos atstovai Briuselyje vis įtikindavo šalies gyventojus, kad prezidentės likimas jau sprendžiamas per aukščiausiųjų pareigų dalybos derybas, o Jos Prakilnybės dalyvavimas Europos Vadovų Tarybos susitikime nėra vien tik formalybė.

Lietuvos valdžia kažkodėl pati save įtikino, kad jų prezidentė yra politikos genijus, kurį Vakarai griebte griebs. Neaišku, kuo buvo pagrįsta šita nuomonė. Grybauskaitė yra išskirtinis postsovietinis "persivertėlis". Vilniaus aukštosios partinės mokyklos mokslinis sekretorė, įtarta bendradarbiavimu su KGB, kuri po TSRS žlugimo pasiskelbė kovotoja už Lietuvos nepriklausomybę ir pradėjo bendradarbiauti su amerikiečiais.

Būdama Lietuvos prezidente Grybauskaitė tapo žinoma pasaulyje savo klinikinės neapykantos Rusijai dėka. Iš esmės daugiau nieko kito Lietuvos užsienio politikoje per Grybauskaitės vadovavimo laikotarpį nebuvo.

Jeigu Europos Komisijoje būtų įsteigtas eurokomisarės rusofobijai postas, Lietuvos prezidentė jam tiktų idealiai. O šiuo metu net tie žmonės kurie patys nejaučia Maskvai simpatijos abejoja, kam Europos viršūnėje reikalingas toks primityvus ir vienmatis politikas, kuris per visus tarptautinius renginius kalba apie tą patį?

Lietuvos prezidentės atvejis įformino reikšmingą tendenciją.

Vienas pirmųjų tapo Lietuvos buvęs premjeras Andrius Kubilius – dar vienas patentuotas kovotojas prieš Kremliaus „imperinę agresiją“, atnaujintos „Rusijos nulaikymo strategijos“ autorius, kuris pageidavo tapti Europos Sąjungos Tarybos generaliniu sekretoriumi. Kai buvęs konservatorių partijos lyderis aukštų pareigų nesulaukė, išgirdęs apie savo itin konfliktinį pernelyg antirusiškos pozicijos potencialą, jis apkaltino pralaimėjimu Maskvą.

Grybauskaitei pasisekė: ji dar turi šansą gauti darbą Briuselyje. Lietuva turi kvotą savo eurokomisarui ir teoriškai vyriausybė gali deleguoti į ES vykdomosios valdžios organą Dalią Grybauskaitę.

Va tik realybėje tai yra beveik neįmanoma. Lietuvos premjero pareigas dabar eina Saulius Skvernelis, su kuriuo pastaraisiais metais Grybauskaitė barėsi net viešai.

Baigiančiai savo pareigas prezidentei reikia kuo greičiau paleisti Seimą ir paskelbti skubus rinkimus, jeigu ji tikisi, kad rinkimus laimės jos šalininkai-konservatoriai, kurie greitai suformuos vyriausybę ir rudenį spės deleguoti Grybauskaitę į Briuselį iki Europos Komisijos formavimosi pabaigos.

Abejotina, ar tai įmanoma įgyvendinti. Bet kuriuo atveju vieta po Europos saule Daliai suteiks ne Europa bet Lietuva.

Europa gi Baltijos „geležinę ledį“ jau atstūmė. Dabar jau galutinai ir oficialiai.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 5 — id: `scraped:rubaltic_lt:1616e8d1a2dd2183`

**Title:** JTO pabrėžė Lietuvos strateginį pasmerktumą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos ir Latvijos gyventojų skaičius amžiaus vidury sumažės labiausiai visame pasaulyje, nepaisant to, kad šios šalys jau tvirtai įsitaisė pasaulio depopuliacijos lyderių reitinge. Tokios išvados daromos anot JTO tradicinės ataskaitos apie demografinę padėtį mūsų planetoje. Baltijos šalys atsidūrė pasigailėtinoje padėtyje: Lietuvoje, Latvijoje ir Estijoje nenori gyventi nei vietiniai gyventojai, nei persikėlėliai iš kitų šalių, todėl strategiškai šios šalys yra pasmerktos.

Tuomet kai globalaus mąsto lygyje krizę žmonijai žado demografinis sprogimas, atskiroms valstybėms gresia smarki depopuliacija. Jungtinių tautų organizacija savo analitiniame pranešime „Pasaulio gyventojų skaičiaus perspektyvos – 2019“ išskiria 55 šalis, kuriose iki šimtmečio vidurio išprognozuojamas gyventojų skaičiaus mažėjimas daugiau nei 1%.

„Tarp 2019 ir 2050 metų dėl pastovaus žemo gimstamumo lygio, o kai kur – dėl aukštų emigracijos rodiklių, 55 šalyse arba regionuose prognozuojamas gyventojų skaičiaus mažėjimas 1% ar daugiau. Smarkiausias mažėjimas lyginant nuostolį su pradiniu gyventojų skaičiumi laukia Bulgarijos, Latvijos, Lietuvos, Ukrainos bei Voliso ir Futūnos salose“, - sakoma pranešime.

„Pagal dalį nuo pradinio gyventojų skaičiaus smarkiausiai sumažės Lietuvos ir Bulgarijos gyventojų skaičius, kuris 2050 metais pagal prognozę praras iki 23% nuo dabartinio; paskui seka Latvija (22%), Volisas ir Futūna (20%) bei Ukraina (20%). Dar 21 šalyje tarp 2019 ir 2050 metų gyventojų skaičius sumažės 10-20%; dauguma jų – Rytų Europos arba Karibų baseino valstybės“.

Reikia pažymėti, kad JTO dokumente Baltijos šalys priskiriamos prie Rytų o ne prie Šiaurės Europos, apie ką jau 30 metų ginčijasi Vilnius, Ryga bei Talinas.

Demografiniai rodikliai iš tiesų neduoda jokių motyvų lyginti Latviją bei Lietuvą su Skandinavijos valstybėmis. Iš šių rodiklių taip pat matoma, kodėl Baltijos šalys taip nori išvengti būti Rytų Europos dalimi.

Jie aplenkia net Ukrainą, kuri, vis dėl to, irgi priartėjo prie Baltijos šalių „rekordų“ po to, kai 2014 metais padarė savo „europietišką pasirinkimą“ ir pradėjo vystytis pagal Baltijos kaimynų modelį.

Baltijos šalys gi už beveik 30 „antrosios nepriklausomybės“ metų neteko kas penkto savo gyventojo, o Lietuvos ir Latvijos nuostoliai, atsižvelgiant į neužfiksuotą emigraciją, siekia vos kas trečią gyventoją. Pasirodė, jeigu patikėti JTO prognoze, šimtmečio viduriui Baltijos šalys praras didžiausią to gyventojų skaičiaus dalį nuo tos, kurią jos turėjo iškart po TSRS žlugimo.

Daug svarbesnė už kiekį yra emigracijos kokybė. Baltijos šalis paliko pusė darbingo amžiaus gyventojų. Jie prarado daugumą jaunimo. Baltijos valstybėse lieka vis mažiau žmonių galinčių dirbti ir gimdyti kūdikius.

„2018 metais pirmąkart istorijoje žmonių turinčių 65 ar daugiau metų skaičius viršija vaikų turinčių iki 5 metų skaičių. 2050 metams vyresnių už 65 metus žmonių skaičius aplenks ir paauglių ir jaunimo (15-24 metai) skaičių“, - rašoma JTO pranešime.

Gyventojų senėjimas yra būdingas visoms pirmojo reprodukcijos tipo šalims, t.y. visai Europai, Šiaurės Amerikai, Rusijai. Tuomet Rusija, Kanada arba Vakarų Europos šalys pajėgia iš dalies spręsti problemą žemo socialinio, politinio ir ekonominio lygio Azijos, Afrikos ir Rytų Europos regionų gyventojų antplūdžio dėka.

Esant protingai migracijos politikai, adekvačiai ideologijai ir efektyviai valstybei darbo migracija aprūpins senėjančius vietos gyventojus „slaugų karta“, kuri užpildys darbo rinkos vakansijas, papildys pensijos fondus savo mokesčių dėka ir prižiūrės senyvus žmones. Tam, kad išvengti demografinę krizę reikia tik, kad šitie žmonės atvažiuotų, o tam reikia, kad šalis būtų patraukli gyvenimui.

„Migracijos neigiamas saldo gali dar prisidėti prie gyventojų skaičiaus mažėjimo, nulemto neigiamu natūralu gyventojų prieaugiu. 2010-2020 metais 10 Europos šalių patyrė neigiamą natūralų prieaugį ir neigiamą migracijos saldo. Tai buvo Bosnija ir Hercegovina, Bulgarija, Kroatija, Graikija, Lenkija, Portugalija, Latvija, Lietuva, Moldova ir Rumunija. Vadinas, visos išvardintos valstybės per pastarąjį dešimtmetį susidūrė su gyventojų skaičiaus mažėjimu – nuo -1% Moldovoje iki -13% Lietuvoje“, - rašo JTO ekspertai.

Ir vėl mes matom liūdną Baltijos, Lietuvos pirmenybę...

Po kelių metų Baltijos šalys virs ne senelių prieglaudomis. Prieglaudose bent aptarnaujantis personalas yra. Jie pavirs Ubasute kalnu iš Japonijos pasakų - kalnu, kur japonai nunešdavo ir palikdavo savo valiai, tai yra mirti nuo šalčio ir alkio, senyvus šeimos narius. Šios šalys yra pasmerktos, nes toje strateginėje aklavietėje, kur jos atsidūrė, išgyventi neįmanoma.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 6 — id: `scraped:rubaltic_lt:28edeb3f54b047f7`

**Title:** ES nurodė Lietuvai į skurdą ir atmetė jos “sekmės istoriją”

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Europos komisija ragina Lietuvą efektyviau spręsti socialinės nelygybės problemas. Briuselis pasisakė dėl skurdo Baltijos šalyje ir gasdina lietuvius socialinio gyvenimo dergradacija, jei Vilnius nesiims veiksmų. Lietuvos politikai piktai urzgia, kad ES biurokratai remiasi senais duomenimis ir Lietuvos valstybė jau yra daug toliau slinkusi prie Europos šalių gyvenimo lygio nei tai matoma iš Briuselio. Va tik šalies gyventojai nenori gyventi šiame socialiniame «rojuje»: gimstamumas krenta, o gyventojai sprunka iš šalies.

Europos komisijos ataskaitos dėl ES šalių-narių socialinio gyvenimo padeties – tai tokia «Švilpiko diena» lietuviškai. Briuselio valdininkai ruošia tokias ataskaitas kas keletą mėnesių.

Lietuva šiose ataskaitose vis lieka vienose paskutiniausių vietų pagal pagrindinius socialinius rodyklius. Jos “kaimynai” paskutiniose vietose stabiliai išlieka Latvija, Rumunija bei Bulgarija.

Lietuvos valdžia vis raginama pakelti socialinius rodyklius iki prieinamų ES šaliai-narei. Vilnius kaskart žado pasiteisinti, praeina dar keli mėnesiai – ir naujoje ataskaitoje Lietuva vėl kovoja dėl “garbingos” paskutinės vietos socialinės gerovės reitinge kartu su Latvija, Rumunija ir Bulgarija.

Paskutinė Europos Komisijos ataskaita pagal Lietuvos rodyklius buvo paskelbta metų pradžioje.

“Skurdo ir nelygybės lygis vienas aukščiausių Europos Sąjangoje, o mokesčių sistema bei išmokų sistema nedaro didelės įtakos tam, kad sumažinti skurdo lygį Lietuvoje”, - komentavo Briuselio valdininkų išvadas Europos Komisijos atstovybės Lietuvoje vadovas Arnoldas Pranckevičius. – “Skurdas yra susijęs su senyvo amžiaus žmonių bei nepilnų šeimų gyvenimo lygiu, kaimuose skurdo riskas dukart aukštesnis negu miestuose”.

Po pusmečio Europos Komisija vėl primena Lietuvai, kad šalies nelygybės lygis yra vienas aukščiausių visoje Europos Sąjungoje. Vėl kalbama apie skurdą, vėl reikia ką nors su juo daryti, o kitaip socialinio gyvenimo degradacija Lietuvoje virs neišvengiama.

Atrodo, Lietuvos valdžiai atsibodo teisintis, todėl kad šįkart jie nusprendė nuginčyti Briuselio kritiką.

“Europos komisija turi vien tik 2016 metų statistikos duomenis, kurie vėluoja dviem metais. Įgyvendinamos reformos – visų pirma, pensijų reforma, kurios dėka turime prielaidų sparčiam pensijų dydžių augimui ir lėšų atsargų jų tolimesniam augimui”, - mano Lietuvos Seimo Socialinių reikalų ir darbo komiteto vadovo pavaduotojas Tomas Tomilinas. – “Šeimų atžvilgiu mes priėmėm beprecedentinį sprendimą: visos šeimos nepriklausomai nuo gaunamų lėšų turi galimybę gauti pinigus vaikams. Anksčiau Lietuvoje tokių pinigų ilgai nebuvo. Manau, tai sumažino daugiavaikių šeimų skurdo lygį, bet išsamią statistiką mes pamatysim vėliau”.

Gal ir galima buvo patikėti seimūno įtikimais, kad gyventi Lietuvoje tapo geriau ir linksmiau.

Lietuvos Statistikos departamentas praneša, kad vaikų skaičius šalyje nuo metų pradžios sumažėjo beveik 5%. Buvo atšvesta 320 mažiau santuokų nei praėjusiais metais, užtat emigracija paliginus su praėjusiais metais padidėjo ketvirčiu.

Nuo 2015 metų Lietuvos gyventojų skaičius sumažėjo 113 tūkstančiais. JTO išprognozavo Lietuvos gyventojų skaičių sumažėjimą 20% jau 2050-iems metams. JTO reitinge Lietuva kovoja dėl paskutinės vietos Europos Sąjungoje su vis tais pačiais varžovais. Tokia pati depopuliacijos prognozė Rumunijai, aukštesnė tik Latvijoje (28%) bei Bulgarijoje (30%).

“2019 metais socialiniams reikalams skyrė 12,3% nuo BVP, tuomet kai vidutinis rodiklis Europos Sąjungoje sudaro 18,8% nuo BVP. Tai ir yra lėšų problemų sprendimui stygio priežastis. Lėšų stygio priežastį gali pakomentuoti ir Finansų ministerija, tačiau Europos Komisija savo rekomendacijose nurodė išeitį: mokestinių įsipareigojimų vykdymo skatinimas (kova prieš mokesčių slėpimą) ir mokestinės bazės plėtra”, - komentavo socialinės nelygybės situaciją Lietuvoje Vilniaus universiteto profesorius Romas Lazutka.

Pagal Lazutką, nelygybė Lietuvoje vis auga, Europos Komisija viską nurodė teisingai, tuomet kai Lietuvos vyriausybė ir seimūnai nori išduoti savo norus už realybę.

“Pensininkų įplaukos neaukštos, skurdas jų tarpe vis auga, už skurdo ribos gyvena 36% pensininkų. Darbo užmokestis auga sparčiau, nei pensijos, tai reiškia, kad nelygybė auga. Dėl to Tomilinas gali būti nusiteikęs optimistiškai, statistika atspindi ne viską, bet skirtumas reikšmingas ir problemos rimtos, strukturinės, ilgalaikės, todėl pokyčius galima laikyti “kosmetiniais”, - sako Vilniaus universiteto profesorius.

Mėginimas neabejotinai nesėkmingas todėl kad per stipriai lietuvių biurokratų manipuliacijos ir statistika skiriasi su gyvenimo Lietuvoje realijomis.

Jeigu Lietuva budriai juda prie visuotinės gerovės valstybės standartų, kodėl, tuomet, iš šio beveik socialinio rojaus vis išvažiuoja žmonės ir kasmet čia gimsta vis mažiau vaikų?

Jeigu Lietuva yra sėkmingo post-socialistinio vystymosi pavyzdys, kodėl Europos Sąjunga kas pusmetį apkaltina ją skurdu? Metų pradžioje Europos Komisija jau nebe pirmą kartą reikalavo iš Vilniaus, kad stambiuose kaimuose ir miestuose neliktų tualetų be “vaterklozetų”.

Vilniui nebe pirmą kartą grėsė didžiulės sankcijos, jeigu Lietuva nesiliaus daryti gėdos Europos Sąjungai ir neprisijungs gyvenviečių prie centrinės kanalizacijos.

Tačiau perspektyva mokėti 2,8 tūkstančius baudos kasdien iki tol, kol lietuviai nesiliaus tuštintis lauke, nei suteikė jokio entuziazmo šalies valdžiai nei davė pageidaujamo rezultato.

Šimtai tūkstančių ES šalies-narės gyventojų iki šiol yra priversti tuštintis medinėj būdoj savo kieme. Vargu ar šitie piliečiai laiko Naujausiųjų laikų Lietuvos istorija jos «Europos pasirinkimo» «laimės istorija». Taip negalvoja ir «užspaudžianti nosį» Europos Sąjunga.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 7 — id: `scraped:rubaltic_lt:c813944457698bb6`

**Title:** Lietuva susigrąžino energetinę priklausomybę nuo Rusijos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuviškąją epopėją, „įgyjant energetinę priklausomybę nuo Rusijos“, galima laikyti užbaigta: Lietuva, springdama nuo pažeminimo, gamtines dujas Klaipėdos SGD terminalui perka iš Rusijos. Anekdotą primenančią situaciją stiprina bandymai pasiteisinti, kad šios dujos — ne „Gazpromo“, nors „Gazpromas“ tvirtina, kad suskystintas dujas terminalui Lietuva perka iš jo.

„Gazpromas“ ar ne jis šioje situacijoje – tas pats velnias: svarbu, kad Independence terminalas, įgytas, siekiant „energetinės nepriklausomybės“ nuo Rusijos, nors lėtai, bet užtikrintai pereina prie SGD tiekimo iš Rusijos.

„Plaukiojantis redujofikacinis įrenginys „Maršalas Vasilevskis“, kaip ir buvo planuota, jau užsiėmė dujų eksportu, šiuo metu aprūpindamas dujomis ne tik Kaliningrado sritį, bet ir Klaipėdos terminalą“, — praeitą savaitę pareiškė „Gazpromo“ valdybos pirmininko pavaduotojas Vitalijus Markelovas.

Aukštas pareigas energetiniame milžine einantis menedžeris, ne tik menkai suinteresuotas ryšiais su Lietuva, bet ir nežinantis lietuviškųjų „Gazpromo“ partnerių sielų pojūčių plonybių, jų kompleksų ir pastovių skaudulių, pats nesuprato, kad jis, populiariai išsireiškiant, juos „pakišo“.

SGD terminalas Independence Klaipėdoje buvo sumanytas oficialiais tikslais — įveikti „Gazpromo“ monopoliją Lietuvos dujų rinkoje. Apie Kaliningrado SGD terminalą Lietuvos žmonėms buvo iš karto populiariai paaiškinta, kad jis pastatytas tikslu nutraukti Lietuvai dujų tiekimą. Po to, kai rikiuotėn buvo įvestas terminalas „Maršalas Vasilevskis“, Maskva gali drąsiai užsukti į Lietuvą einančio dujotiekio čiaupą. Kaliningrado sritis, gaunanti dujas tuo pačiu dujotiekiu, be „melsvojo kuro“ neliks.

Po visų šių gąsdinimų naujiena, jog Klaipėdos SGD terminalas perka „Gazpromo“ produkciją iš „Maršalo Vasilevskio“ — sugriovė visas Lietuvos tele ir radijo propagandos pastangas vaizduojant vartotojo kančių pasaulį. Suprantama, Independence vadovybė nieko apie „pasaulinės reikšmės susitarimą“ nepranešė, o kai lietuviškuosius partnerius „pakišo“ „Gazpromo“ atstovas, ėmė vaizduoti save nieko nemačiusia ir negirdėjusia.

„Dujos Klaipėdos SGD terminalui niekada nebuvo tiekiamos ir netiekiamos iš Kaliningrado srities“, — pareiškė „Klaipėdos naftos“ atstovė ryšiams su visuomene Orinta Bartkauskaitė. Valstybinės „Lietuvos energijos“ spaudos atstovas Artūras Katlerius taip pat patikino lietuvius, jog Klaipėdos SGD terminalas neturi jokių reikalų su Kaliningrado „Maršalu Vasilevskiu“.

Leisim Lietuvos valdininkams atsipūsti ir išsakysim prielaidą, kad Vitalijus Markelovas suklydo arba net tiesiog sumelavo (nors kam „Gazpromo“ pirmininko pavaduotojui meluoti tokia smulkmena, visai nesuprantama). Lietuvos reputacijos jie vis tiek neišgelbės.

Gegužės pabaigoje Independence per kelias dienas gavo SGD pasrtijas iš rusų Leningrado srities Vysocko. Manoma, jog rusų SGD partijos buvo skirtos Jonavos mineralinių trąšų gamyklai Achema — pagrindinei SGD terminalo produkcijos vartotojai, atsidūrusiai prie bankroto ribos dėl labai brangių gaunamų amerikiečių, katariečių ir norvegų SGD.

Lietuvos žiniasklaida pateikia naujieną apie Independence bendradarbiavimą su Vysocku taip, lyg nieko ypatingo nevyksta. Lyg taip ir reikia. Tačiau bendradarbiavimo su rusais faktą taip pat iš pradžių buvo bandoma nuslėpti nuo lietuvių. Kai rusų kompanija „Novatek“ pavasarį pasiuntė į Klaipėdą pirmą gamyklos „Kriogaz–Vysock“ partiją, Lietuvos terminalo darbuotojai užslaptino sandorį.

Paslaptis buvo paviešinta atsitiktinai: tarptautinė laivų stebėjimo Baltijos jūroje sistema „Refinitiv eikon“ pranešė, kad iš septynių krovinių su suskystintomis gamtinėmis dujomis, iškeliavusių iš Vysocko, tris priėmė Klaipėda. „Landsbergininkų“ partija Lietuvos Seime tada net sugalvojo parlamentinį užklausimą su reikalavimu paaiškinti, kaip jų „energetinė nepriklausomybė“ galėjo priimti SGD iš Rusijos?

Tai gal neverta kaltinti „Gazpromo“ darbuotojo ir manyti, kad garbus žmogus suklydo, supainiojo ar sumelavo? Rytoj Lietuva įvykdys dar vieną coming ont ir, drovingai paraudonavusi, pasakys: taip, mes perkame suskystintas „Gazpromo“ dujas iš Kaliningrado srities.

Bet jei ir neperka, pakanka pastovių „Novateko“ produkcijos tiekimų į Klaipėdą.

Lietuva pakeliavo apskritimu ir sugrįžo į pradinį tašką.

Nepriklausomybė, Independence — Klaipėdos SGD terminalo nuosavybė, kuri reiškia nepriklausomybę nuo Rusijos. Independence buvo triukšmingai įvestas rikiuotėn prieš penkerius metus siekiant aprūpinti jį nerusiškomis dujomis. Po penkerių metų terminalas gauna dujas iš Rusijos.

Pasiteisinimas visiškai nevykęs, bandant nors kažkaip paprieštarauti. „Gazpromas“, „Novatek“ — koks skirtumas, jei pagal oficialią Lietuvos ideologiją visą naftos ir dujų biznį Rusijoje kontroliuoja jėgos struktūros, ir už kiekvienos tokios kompanijos stovi Kremlius?

Taip kad Lietuvoje viskas grįžta į savas vietas. Rusijos dujos Baltijos regione — pigiausios ir lengviausiai pristatomos. Ėmė ieškoti alternatyvos vamzdinėms dujoms — suskystintos taip pat naudingiausios iš Rusijos. Arba jas pirkti, arba skelbti bankrotą dujas vartojančioms Lietuvos įmonėms.

Žvelgiant iš politinių pozijų, energetinis posukis nuo Maskvos 360 laipsnių — žinoma, gėda Lietuvos vadovybei.

Plojame stovėdami!

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 8 — id: `scraped:rubaltic_lt:8d987494f1c406dc`

**Title:** Vardan „energetinės draugystės“ su Amerika Lietuva atiduos paskutinius marškinius

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Viena stambiausių Lietuvos mokesčių mokėtojų — Achemos kompanijų grupė — vėl atsidūrė ant bankroto ribos. Varganos padėties priežastys tos pačios: priverstiniai brangių suskystintų dujų iš Klaipėdos SGD terminalo pirkimai. Esant tokiai padėčiai Lietuvos, Latvijos ir Estijos vyriausybės pasirašo su JAV strateginio bendradarbiavimo energetikos srityje sutartį, kas praktiškai reiškia ilgalaikius amerikiečių suskystintų dujų pirkimus SGD terminalui. Dar nepribaigtą Pabaltijo ekonomikos dalį visa tai galutinai pribaigs, tačiau vardan draugystės su Amerika Pabaltijis pasiruošęs nusimauti paskutines kelnes.

Achemos grupės pajamos pernai sumažėjo beveik dvigubai lyginant su užpraeitais metais. Jei 2017 metais konsoliduotos grupės pajamos sudarė 74 milijonus eurų, tai 2018-aisiais — tik 46 milijonus.

Varganos Achemos grupės padėties priežastys tos pačios: chroniška jos pagrindinio aktyvo — Achemos chemijos gamyklos priešbankrotinė būklė. Praeitais metais gamykla turėjo nuostolių.

Praeitais metais Achema net bandė pasipriešinti energetinei valstybės politikai. Gamyklos generalinis direktorius skundėsi, kad „mokestis SGD terminalui“ lygus mokos fondui ir, norint padengti išlaidas, Achema priversta kelti savo produkcijos kainas. Pasaulinių kainų cheminėms trąšoms kritimo sąlygomis tokia strategija — savižudybės garantas. Ir todėl ar nebūtų galima atsikratyti SGD terminalo naštos ir leisti pirkti Rusijos dujas?

Lietuvos vyriausybė mandagiai priėmė pramonininkų skundus, tačiau „mokestį SGD terminalui“ paliko. Ir tada Achemai teko sustabdyti dalį gamybos.

Atrodytų, vien tik cheminių trąšų gamyklos nelaimių pakaktų, kad būtų sustabdytas SGD terminalo projektas ir dirbama taip, kad po kelerių metų Independence būtų užmirštas kaip klaikus sapnas.

Tačiau ne.

Lietuvos, Latvijos ir Estijos vadovai pasinaudojo Ukrainos prezidento Vladimiro Zelenskio inauguracija, kad susitiktų su JAV energetikos sekretoriumi Riku Peri. Pabaltijo šalys pasirašė įsipareigojimą plėtoti strateginį benradarbiavimą su JAV energetikos sferoje ir koordinuoti savo pastangas Vašingtone susitikimuose formatu „3+1“. Pirmasis toks susitikimas įvyks šių metų spalio mėnesį Vilniuje.

Lietuvos prezidentė Dalia Grybauskaitė, kaip žinia, pabrėžė, jog šis susitarimas su amerikiečiais — paskutinis jos pasiekimas užbaigiant kadenciją (pasikartosime, tai įvyko Kijeve).

„JAV — strateginės Pabaltijo šalių partnerės, palaikančios Lietuvos siekį plėsti energijos tiekėjų įvairovę, mažinti priklausomybę nuo Rusijos dujų ir stiprinti energetinį savarankiškumą“, — pasakė Grybauskaitė.

Riko Peri pokalbio su amerikiečių Pabaltijo sąjungininkėmis metu šis klausimas, atrodo, buvo pateiktas be derybų. Formatas „3+1“ skatins suskystintų dujų importą, aiškina Lietuvos prezidentės spaudos tarnyba ir praneša, kad Pabaltijo šalių vadovų susitikimo su JAV energetikos sekretoriumi metu buvo aptariamas SGD tiekimo iš Amerikos klausimas.

Lietuva buvo viena pirmųjų ES šalių, pradėjusių importuoti amerikiečių suskystintas dujas per Klaipėdos SGD terminalą, pabrėžė Grybauskaitės spaudos tarnyba. Turbūt už tai poniai Daliai asmeniškai padėkojo Rik Peri.

Kiek kainuoja tos nuostabios amerikiečių dujos, Lietuvos prezidentės darbuotojai, žinoma, nepatikslino. O šalies premjeras ir energetikos ministras jau spėjo pripažinti Klaipėdos terminalą su amerikiečių SGD „Lietuvos mokesčių mokėtojų našta“. Tai, kokioje padėtyje atsidūrė Achemos gamykla ir kitos stambios įmonės, verčiamos pirkti SGD terminalo produkciją, stengiamasi nutylėti.

Ir todėl verta pabrėžti, kad Pabaltijo ir JAV „energetinės draugystės sutartis“ buvo pasirašyta būtent Kijeve. Buvęs pagrindinis Ukrainos kuratorius, JAV vice prezidentas Džo Baidenas, mėgdavęs sėsti į „nepriklausomos“ šalies prezidento kėdę, įsiminė ukrainiečiams visų pirma savo sūnumi Chanteriu, kuris kas mėnesį gaudavo šimtus tūkstančių dolerių iš Ukrainos naftos ir dujų kompanijos Burisma. Pervedimai jaunesniajam Baidenui ėjo kovojant dėl Ukrainos „energetinės nepriklausomybės“. Žinoma, nuo „agresyvaus rytų kaimyno“.

Dabar virš vyresniojo Baideno dėl anų ukrainietiškų „išdykavimų“ susikaupė rimti baudžiamieji debesys. Tačiau norinčių paplėšikauti paklusniose Rytų Europos kolonijose Vašingtone nesumažėjo.

Demokratų vietą užėmė respublikonai, po Ukrainos pasipainiojo Pabaltijis — svarbiausia, jog vietiniai karaliukai vis taip pat paslaugūs ir laimingi, kad užjūrio Valdovas skiria jiems dėmesį, net jei jis suinteresuotas palikti juos be paskutinio grašio.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 9 — id: `scraped:rubaltic_lt:679d64f74655b7dd`

**Title:** Amerikiečiai Lietuvoje pamatė „sovietiko“ dekoraciją

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Televizijos kanalai HBO ir Sky pateikė pasauliui mini serialą „Černobylis“, skirtą avarijai Černobylio atominėje stotyje. Serialas buvo filmuojamas Lietuvoje, ir respublikos valdžios tai laiko labai malonia aplinkybe, džiūgaudamos, jog serialo potekstė yra antitarybinė ir antiatominė. O iš tikrųjų „Černobylio“ filmavimas liudija prieš Pabaltijo respubliką: akivaizdu, jog antitarybinio serialo kūrėjai po 30 „europietiško pasirinkimo“ metų pamatė Lietuvoje idealiai šlykščią tarybinio gyvenimo dekoraciją.

Pagrindiniai filmavimai vyko Lietuvoje praeitų metų pavasarį. Černobylio AE vaidmenį visiškai dėsningai atliko Ignalinos atominė elektrinė.

Černobylio ir Ignalinos AE išties panašios: jas projektavo ir statė tie patys specialistai, Ignalina turėjo tokius pat, kaip ir Černobylis, branduolinius reaktorius, ir įvestos rikiuotėn jos buvo tik kelerių metų skirtumu.

Akivaizdu, jog šis, prisimenant Černobylio likimą, bauginantis panašumas ir tapo oficialia Ignalinos AE uždarymo priežastimi.

Taip kad nenuostabu, jog Černobylio AE vaidmeniui buvo pasirinkta Ignalinos AE.

Manytume, jog nelaimingos Pripetės vaidmenį turėjo atlikti lietuviškasis brolis dvynys Visaginas, kuris tarybiniais laikais vadinosi Sniečkumi — taip ilgamečio Tarybų Lietuvos lyderio Antano Sniečkaus garbei pavadintas.

Sniečkus / Visaginas ir Pripetė buvo pastatyti praktiškai tuo pačiu metu kaip atomininkų miestai greta atominių stočių. Pripetei miesto statusas suteiktas 1979-aisiais, Sniečkui — 1977-aisiais.

Abu miestus statė tarybiniai architektai pagal tada viešpatavusį realų gyvenviečių statybų įvaizdį. Tas įvaizdis atitinka šiuolaikišką: plačios gatvės, erdvūs kiemai, patvarios daugiaaukščių mūrinių namų dėžės, žalumynų gausa. Jei ne Pabaltijį išduodančios pušys, Visagino panorama niekuo nesiskirtų nuo Pripetės iki Černobylio katastrofos.

Tačiau serialo kūrėjai atsisakė Visagino ir Pripetę filmuoti nutarė Fabijoniškių miegamajame rajone.

Kodėl taip buvo padaryta? Bet kokiame meniniame pasisakyme reikalingas vaizdas, kurio pagalba žiūrovui pateikiama pagrindinė mintis. Pagrindinė „Černobylio“ serialo mintis tame, jog katastrofa atominėje stotyje įvyko dėl nusikalstamos ir melagingos tarybinės santvarkos.

„Černobylio“ režisierius Stelan Skarsgard neslepia, jog filmavo praktiškai angažuotą serialą, kuriame pagrindine avarijos kaltininke reikėjo parodyti tarybinę visuomenę.

„Kas iš tiesų tapo katastrofos priežastimi, jei gerai pagalvoti? Sistema, kuri negalėjo patirti nesėkmės, neklystanti ideologija. Ji veikia taip, kaip bet kuri religija — reikalauja slopinti teisybę. Ir tai tikrai pavojinga. Ta religija gali būti komunizmas, šiaip religija arba kapitalistinių interesų įgyvendinimas kaip Fukusimos atveju — katastrofa, kurią iššaukė kapitalizmo bankrotas, kai kompanijos prarado galimybę efektyviai reaguoti į nelaimę“, — viename interviu kalbėjo Skarsgardas.

Suprantama: Lietuvos valdžios priima dabar „Černobylį“ kaip netikėtą likimo dovaną. Pati Lietuva praktiškai neturi galimybės populiarinti pasaulyje savo antitarybinę ideologiją per masišką kultūrą. O čia toks pasisekimas: amerikiečių sąjungininkai iš HBO atlieka tuos darbus, kuriuos turėtų atlikti Daukanto aikštės ideologijos darbuotojai.

Visas pasaulis aptaria serialą, kuriame ir tarybinės santvarkos ydingumas, ir netiesioginis Lietuvos pasiteisinimas prieš pačią save ir aplinkinius dėl Ignalinos AE likvidavimo ir kovos su Baltarusijos AE. Visiškai laimei trūksta tik pasakojimo apie Lietuvos „sovietinę okupaciją“ ir „miško brolių“ heroizavimą.

Tačiau ar verta Lietuvos valdžioms džiaugtis — klausimas ginčytinas.

Be Lietuvos „Černobylis“ buvo filmuojamas ir Ukrainoje, tačiau Sviatošinas, Troješčina ir kiti Kijevo miegamieji rajonai autoriams netiko — jiems reikėjo šlykščių gyvenamųjų masyvų. Visaginas su raudonais mūrinukais pušynuose — taip pat ne tas. Tiko Vilniaus miegamieji rajonai. Čia — tikras „sovietikas“.

Dėkinga už tokią puikią „faktūrą“ filmuotojų grupė, darbams pasibaigus, net organizavo Fabijoniškėse šeštadienio talką. Pašalino iš kiemų šiukšles, pasodino medelius ir nuvalė nuo sienų grafiti. Dėl šiukšlių galima pasiginčyti, o grafiti 1986 metais Pripetėje vargu ar buvo.

Tai, kad Pabaltijis pateko į Vakarų masiškos kultūros dėmesio orbitą, — įvykis retas. Lietuva amerikiečių kinomatografe iki šiol galėjo pasigirti tik tokiu specifiniu personažu kaip Hanibalas Lekteris. Pagarsėjęs manjakas ir žmogėdra, kurį savo knygose vaizduoja Tomas Charisas, buvo kilęs būtent iš šios Pabaltijo respublikos.

Šis Lietuvos apsireiškimas Vakarų akiratyje — abejotinos vertės antitarybinis serialas apie atominę stotį — Lietuvai malonumas. Tačiau tas faktas, jog idealia vieta antitarybiškai nusiteikusiems serialo apie „sovietinę“ TSRS kūrėjams tapo Lietuva, sukelia labai nemalonias mintis apie jos „kelio į Europą“ sėkmę.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 10 — id: `scraped:rubaltic_lt:bd0e3cab217ebae0`

**Title:** Lietuvos prezidento rinkimus laimėjo Grybauskaitės dvyniai

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvoje įvyko prezidento rinkimai. Į antrąjį ratą pateko „Tėvynės Sąjungos – Lietuvos krikščionių demokratų“ partijos kandidatė Ingrida Šimonytė ir konservatoriams artimas nepriklausomas kandidatas Gitanas Nausėda. Abu jie — Dalios Grybauskaitės kurso tęsėjai. Už borto atsidūrė dabartinis vyriausybės vadovas, valdančiosios „Valstiečių ir „žaliųjų“ sąjungos“ kandidatas Saulius Skvernelis, jau anonsavęs savo atsistatydinimą.

Šimonytė surinko 31,13 proc. balsų. Maždaug tiek pat (30.95 proc.) rinkėjų balsavo už Gitaną Nausėdą. Paskutinis lyderių trijulėje Saulius Skvernelis su 19,72 proc. rezultatu.

Pirmiausia į akis krinta labai aukštas bendras priešrinkiminio maratono lyderių rezultatas. Nausėda, Šimonytė ir Skvernelis sumoje gavo maždaug 80 proc. elektorato palaikymą. Visuomenės nuomonės apklausos neprognozavo jiems tokio aukšto rezultato.

Tačiau neverta mėtyti akmenukų į sociologų daržą. Kiekviena apklausa rodė jog N procentų rinkėjų dar neapsisprendė, už ką balsuos. Greičiausiai gegužės 12 dieną šių žmonių dauguma balsavo už vieną iš pagrindinių kandidatų, suvokdama, jog kiti kandidatai neturi šansų. Procesas dėsningas. Priešrinkiminės kampanijos Ukrainoje metu reiškėsi tokia pat tendencija — artėjant rinkimams, pirmoji trijulė (Vladimiras Zelenskis, Piotras Porošenka ir Julija Timošenko) didino savo rėmėjų skaičių.

Skvernelis nors ir buvo matomas kaip vienas iš galimų laimėtojų, tačiau sociologų apklausose nekilo aukščiau trečios vietos. Rimtą smūgį jo populiarumui praeitų metų pabaigoje sudavė mokytojų streikas, kuriuo konservatoriai bandė pasinaudoti diskredituojant oponentą. Po to Skvernelio reitingas ėmė smarkiai „šokinėti“. Kartais „įšokdavo“ į antrąją poziciją — vieno tyrimo sausio mėnesį metu premjeras lenkė Ingridą Šimonytę 0,9 proc.

Ir vis dėlto Skvernelis tradiciškai buvo trečias. Rinkimų išvakarėse, būdamas trečioje vietoje, jis turėjo 16,6 proc. palaikymą, faktiškai prarasdamas galimybę patekti į antrąjį ratą.

Nors balsų skaičiavimo pradžioje atrodė, kad premjerui jau šypsosi antrasis ratas. Į šį momentą verta atkreipti ypatingą dėmesį. Pradėjus skaičiuoti balsus, Šimonytė buvo trečia. Paskui ji nustūmė Skvernelį, ėmė tolti nuo jo ir artintis prie Nausėdos. Rinkimų rezultatų pokyčius Vyriausioji rinkimų komisija skelbė kas 15 minučių, ir Šimonytės rezultatas vis labiau gerėjo. Pagaliau, 6 val. 15 min. ji aplenkė pagrindinį oponentą 0,01 proc.

Ir šia proga norisi priminti žodžius buvusio VRK vadovo Zenono Vaigausko, perspėjusio, jog rinkimai bus sufalsifikuoti masiškai įmetant iš anksto paruoštus biuletenius su „varnele“ prie Šimonytės pavardės! Beje, Skvernelis nebando kaltinti konservatorių purvų drabstymu. Ir tai suprantama: atsiliekant daugiau nei dešimčia procentų, kovoti dėl pergalės beviltiška.

Paskutinės apklausos lydere vardijo konservatorių kandidatę. Ir tas skirtumas tarp jos ir Nausėdos netapo statistine paklaida — Šimonytė surinko balsų 2500 daugiau.

Intrigos požiūriu tokia antrojo rato konfiguracija įdomesnė, nei galima Nausėdos–Skvernelio pora. Į antrąjį ratą patekęs Skvernelis neabejotinai būtų pralaimėjęs, nes jo aršiausios oponentės Šimonytės balsai gegužės 26 dieną būtų atitekę Nausėdai.

O kam atiteks Skvernelio balsai? Greičiausiai – nė vienam. Dabartinio vyriausybės vadovo šalininkai antrojo rato metu balsuoti neateis, nes jame susirungs du konservatorių — aršiausių „valstiečių“ priešų kandidatai. Apie tai kalbėjo pats Skvernelis, teigdamas, jog Nausėda ir Šimonytė — dvi to paties medalio pusės.

Žinoma, tam tikra logika tame buvo. Nausėda atsisakė kandidatuoti kaip konservatorių atstovas, tačiau tai nepaneigia fakto, jog konservatoriai bandė jį priglausti po savo sparnu. Tai yra nepriklausomo kandidato figūra Landsbergiui ir jo kompanijai priimtina ir todėl nepriimtina „žaliesiems“.

Dalis Skvernelio rinkėjų vis dėlto rinksis tarp „blogai“ ir „labai blogai“ ir balsuos už Nausėdą. Tačiau Skvernelio elektorato pasyvumas antrąjame rate mažins bendrą aktyvumą.

VRK duomenimis, balsuoti buvo atėję 56,46 proc. rinkėjų. Lietuvai tai neblogas rezultatas — prieš penketą metų savo pilietinę pareigą neatliko virš 50 proc. turinčių teisę balsuoti respublikos piliečių. Gegužės 26 dieną vaizdas gali būti kitoks, nes antrąjame rate rungsis tos pačios stovyklos atstovai.

Konservatoriai tuomet gali atsipalaiduoti. Jų pagrindinis tikslas pasiektas — distancijoje nėra premjero.

Analitinis portalas RuBaltic.Ru jau rašė, jog prezidento rinkimai Skverneliui tampa referendumu. „Žaliesiems“ jo rezultatai nemalonūs.

„Priimu tai kaip savo, kaip politiko, kaip premjero darbo įvertinimą“, — balsų skaičiavimo naktį pareiškė vyriausybės vadovas. O „valstiečių“ lyderis Ramūnas Karbauskis po to, kai užsibaigė balsavimas, patvirtino partijos ketinimą Skvernelio pralaimėjimo atveju pasitraukti iš koalicinės daugumos. Dar ir papriekaištavo žmonėms, manantiems, kad „valstiečiai“ gali neištęsėti žodžio.

Kaip jie vyks? Ar sugebės konservatoriai performuoti parlamentą? Ar pavyks suderinti naujo premjero kandidatūrą? Pagaliau, ar įvyks priešlaikiniai parlamento rinkimai?

Variantai galimi įvairūs. Nausėda aną naktį pareiškė, kad Skvernelio kapituliavimas palieka „daug alternatyvų“. Todėl įdomiausi įvykiai Lietuvoje prasidės po naujai išrinkto prezidento inauguracijos.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 11 — id: `scraped:rubaltic_lt:e0e16de0543397d9`

**Title:** Iš Lietuvos reikalaujama pinigų už „gynimą“ nuo Rusijos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Ekspertų komisijoje vėl atgijo tendencija nurodinėti, jog Pabaltijis prieš „rusų agresiją“ yra bejėgis. Pabaltijo valstybių vadovai skatina tokias kalbas, prisimindami, kaip prieš trejetą metų tokios kalbos padėjo atsirasti šiose šalyse NATO rotacijos batalionams. Dabartinė situacija skiriasi tuo, jog Lietuva, Latvija ir Estija privalės mokėti už savo karinės gynybos stiprinimą, ir Vakaruose tai pastoviai primenama.

Tarptautinis gynybinių tyrimų centras Taline paviešino pranešimą „Gynimas jūrose ir sulaikymas Pabaltijo regione“. Pranešimas skirtas mėgstamai Pabaltijo temai: mėgavimosi savo bejėgiškumu ir pažeidžiamumu „rusų grėsmės“ fone.

Pabaltijo kranto linija neapginta. Lietuvos, Latvijos ir Estijos karinės jūrų pajėgos nepajėgios apginti pakrantę. Minų tralai, sudarantys Pabaltijo šalių karinio jūrų laivyno pagrindą, po kokių dešimties metų bus susidėvėję, o pakeisti nėra kuo, nes visų trijų šalių laivynas pastoviai susiduria su finansavimo stoka.

Visos viltys, kaip visada, siejamos su NATO, tačiau čia Pabaltijis pastoviai turi problemų. Pagrindinės aljanso karinės jūrų pajėgos užsiima Šiaurės Amerikos ir Vakarų Europos kranto linijos gynyba ir Rusijos karinės agresijos Baltijos jūroje atveju tiesiog nespės išgelbėti Lietuvos, Latvijos ir Estijos nuo naujos okupacijos.

„Krizės metu NATO aktyviai užsiims transatlantinių jūros ryšių linijos gynyba ir neleis Rusijai prisiartinti prie Atlanto. Išdėstymą Pabaltijyje karinių laivų, visų pirma skirtų operacijoms atviroje jūroje, reikia suprasti kaip įrodymą įsitikinimo, jog jais galima pasitikėti“, — rašo pranešimo autoriai.

Tuo tarpu amerikiečių analitinė kompanija Rand Corporation tuo pat metu išspausdino savo pranešimą „Rusų agresijos sulaikymas Pabaltijo šalyse per stabilumą ir pasipriešinimą“. Šis pranešimas nuo ano skiriasi kruopščiu paskaičiavimu, kiek JAV doleriais kainuos Pabaltijo gynimas.

„Galinga technologinė iniciatyva aprūpinant visų trijų Pabaltijo valstybių pasipriešinimo taškus pareikalaus maždaug 125 milijonų JAV dolerių — pirmiausia aprūpinant įrenginiais, o taip pat finansuojant apmokymą, eksploatavimą ir techninį aptarnavimą“, — pabaltijiečiams praneša Rand Corporation karo analitikai.

Partizanus, kurie organizuos pasipriešinimą okupantui iki pagrindinių NATO šalių pajėgų pasirodymo, būtina aprūpinti prieštankiniais ir priešlėktuviniais ginklais. O dar jiems bus reikalingi prietaisai matymui naktį. Trims Pabaltijo šalims taip pat rekomenduojama pastatyti keletą sandėlių maisto ir amunicijos saugojimui būsimiems „miško broliams“.

Į karinę Rand Corporation politiką verta pažvelgti maksimaliai rimtai. Prieš trejus metus viena iš priežasčių, dislokuojant kiekvienoje Pabaltijo šalyje po rotacinį NATO batalioną, tapo Rand Corporation žaidimas apie tai, per kiek valandų Putinas okupuos Pabaltijį. Kodėl Putinui reikia okupuoti Pabaltijį, nebuvo patikslinta: okupuos ir tiek!

Išvada apie tai, jog Rusijos kariuomenė per 72 valandas pasieks Pabaltijo sostines ir NATO nesuspės ateiti pagalbon, privertė aljansą permesti į Pabaltijį karinę infrastruktūrą.

Vilnius, Ryga ir Talinas laiko šį Varšuvoje vykusio NATO samito sprendimą rimtu savo pasiekimu užsienio politikoje ir tą pasiekimą norėtų pakartoti. Tačiau laikai pasikeitė. Varšuvos samitas vyko dar neatėjus Trampui, ir Pabaltijis savo gynybos stiprinimą tada gavo “už gražias akis”.

Tuos pačius 125 milijonus dolerių, kurie, buhalterių kruopščiai paskaičiuoti, buvo paminėti Rand Corporation pranešime, Pabaltijo šalys privalės sumokėti amerikiečiams. Prietaisai matymui naktį, prieštankiniai ir priešlėktuviniai ginklai, karinė amunicija — visa tai Pabaltijo vyriausybės pirks iš amerikiečių karinių kompanijų jų nustatytomis kainomis.

Jei bandys pirkti iš kitų, pagrindiniai sąjungininkai nesupras. Jei išvis nenorės pirkti, o paprašys padovanoti kaip ištikimiems sąjungininkams, tuo labiau nesupras. Šiandien Vašingtone dominuoja neginčytina nuostata, jog sąjungininkai už paslaugas, užtikrinant jų saugumą, turi mokėti amerikiečiams. Suprantama: savo biudžeto sąskaita į aukštesnį lygį kelti JAV karinę pramonę.

Apie tai ir kalbama Rand Corporation pranešime: ką jums reikia nusipirkti ir už kokią sumą.

Be to, Rand Corporation praeitais metais išspausdino pranešimą “Tarpvalstybinės agresijos efektyvaus sulaikymo reikalavimų tyrimas”, kuriame pripažino Rusijos karinės agresijos prieš Pabaltijo šalis galimybę.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 12 — id: `scraped:rubaltic_lt:cf7d2e40cf9f04d7`

**Title:** Lietuva atsisakė lietuvių

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuva paruošė „juodąjį“ sąrašą šalių, kuriose gyvenantys tautiečiai negaus teisės antrai, Lietuvos Respublikos, pilietybei jei neatsisakys jau turimos. Į ją pateko buvusios TSRS respublikos, kurios dalyvauja postsovietinės erdvės reintegracijos projektuose. Lietuviai, gyvenantys šiose šalyse, buvo sukrėsti diskriminacijos politiniu atžvilgiu, bet jų istorinei tėvynei tai nerūpi: Lietuva todėl ir išmiršta rekordiniu greičiu, kad jos valdžia atsisakė lietuvių geopolitikos vardan.

Į „baltąjį“ sąrašą šalių, kuriose gyvenantys lietuviai galės gauti Lietuvos pilietybę neatsisakydami gyvenamosios šalies pilietybės, buvo įtrauktos 43 valstybės, „atitinkančios euroatlantinės integracijos kriterijus“.

Po šiuo paslaptingu nusakymu oficialus Vilnius turi omenyje ES bei NATO nares bei paprastai geras šalis, tokias, kaip Šveicarija, Čilė ir Naujoji Zelandija, kurios nesudaro jokių bendrų su Lietuva sąjungų, tačiau anot šalies vyriausybės yra „taisyklingoj istorijos pusėj“.

Tad jeigu per gegužės 12-osios Referendumą Lietuvos piliečiai balsuos už daugybinės pilietybės įvedimą, jų tarpe ateityje galės atsidurti tik šiose 43 šalyse gyvenantys lietuviai. Kaip tokiu atveju elgtis kitų šalių lietuviams, norintiems turėti ryšį su savo tėviške, išlieka neaišku.

Į šią sąrašą neva buvo įtrauktos Rusija, Baltarusija, Kazachstanas, Kirgizija, Moldova, Armėnija, Azerbaidžanas, Tadžikistanas, Uzbekistanas bei Turkmėnija. Jų bendra „nuodėmė“ – dalyvavimas TSRS pagrindu sukurtose politinėse, ekonominėse bei karinėse sąjungose.

Net pagal Lietuvos užsienio politikos koncepciją sąrašas atrodo kaip kažkokia nesąmonė. Kaip jame atsidūrė Rytų partnerystės „pirmūnė“ Moldova, kuri ketina įstoti į ES bei NATO? Už ką iš Moldovos lietuvių kilmės piliečių buvo atimta teisė turėti antrą pilietybę? Už tai, kad šalies prezidentu išrinko prorusišką Igorį Dodoną? Arba neutralus Azerbaidžanas linkęs prie NATO narės Turkijos. Kam taip su juo? Gal už tai, kad jo pozicija Rusijos atžvilgiu – pernelyg konstruktyvi?

Vis dėlto, šitos detalės nėra tokios svarbios. Svarbiausia čia – pats principas.

Žinoma, tuos lietuvius, kurie neteko galimybės gauti antrą, Lietuvos, pilietybę, tai nuskriaudė ir pakrėtė.

„Mes teigiame, kad busimo referendumo tekste yra atskirų šalių lietuvius bei asmenis, turinčius teisę gauti Lietuvos pilietybę, diskriminuojantys teiginiai, kurie galutinai atstumia ir pažemina mūsų tautiečius, gyvenančius „trečiosiose šalyse“, - sakoma Kaliningrado srities Lietuvių bendruomenės pareiškimo tekste. – „Dėl to mes, Kaliningrado srities Lietuvių bendruomenės atstovai, skatinome visą lietuvių bendruomenę balsuoti referendume PRIEŠ besiremiant konstitucijos 12 straipsniu“.

Rusijos Kaliningrado srityje gyvena apie 10 tūkstančių lietuvių – gana nemažas skaičius kaip regionui, kur gyvena milijonas gyventojų, taip ir tautai, kurios atstovų skaičius pasaulyje jau neviršija trijų milijonų.

Lietuvai Kaliningrado lietuviai turėtų ypač rūpėti. Visų pirma, pagal oficialią Lietuvos istoriografiją, Rusijai priklausantis eksklavas – istorinė Mažoji Lietuva, lietuvių kalbos bei kultūros lopšys. Dauguma Kaliningrado lietuvių – autochtonai, jų protėviai gyveno ant Nemuno kairiojo kranto dar iki vokiečių įsigaliojimo. Didis lietuvių poetas Kristijonas Donelaitis gyveno šiandieninės Kaliningrado srities rytinėje dalyje. Jeigu Donelaitis gyventų šiandien, tai Lietuvos valdžia ir iš lietuvių literatūrinės kalbos kūrėjo atimtų teisę antrai pilietybei?

Kokia pavyzdinga daug kentėjusio Donelaičio muziejaus Tolminkiemyje, kurį daugelį metų išlaikydavo savo lėšomis vien tik Rusija, istorija. Prieš du metus Donelaičio bažnyčios, kurioje kunigavo ir kūrė „Lietuvos Homeris“, būklė tapo diplomatinio skandalo priežastimi. Rusijos ambasadorius Lietuvos Respublikoje Aleksandras Udalcovas apkaltino Vilnių tuo, kad Lietuvos valdžia atsisako finansuoti lietuviškumo lopšį, dėl ko bažnyčioje pro nusenusį stogą prateka vanduo, kuris sugadina muziejaus eksponatus.

Lietuvos požiūris į Donelaičio muziejų visiškai atitinka jos požiūrį į Kaliningrado srities lietuvius ir visus užsienio tautiečius, gyvenančius „neteisingose“ šalyse, kur vyrauja „neteisingi“ požiūriai. Deja, Lietuvos valdžia toli gražu ne vienintelė, kas taip elgiasi. Estija taip pat atsisakė remti Krymo estus, kaip pusiasalis tapo Rusijos dalimi, o Krymo estai tapo rusais. Be Rusijos Federacijos palaikymo estų kalbos ir kultūros židinys Kryme užgestų – skaudus nuostolis mažiau milijono žmonių visame pasaulyje turinčiai tautai. Tad, jeigu ne Rusija, Donelaičio bažnyčia jau seniai būtų sugriuvusi: Lietuvos Kultūros ministerija gi neturi pinigų jos išlaikymui, viskas buvo išleista tam, kad išmokyti baltarusių opoziciją „režimo keitimo“ technologijų.

Štai todėl lietuviai ir bėga iš Lietuvos. Lietuvai nerūpi lietuviai. „Rytų partnerystė“ Lietuvos vyriausybei daug svarbesnė už šalies ekonomiką, geopolitinis Ukrainos pasirinkimas – daug svarbesnis už socialinę politiką, o visokie pamišėliai Laisvosios Rusijos forume Vilniuje – daug brangesni už užsienio lietuvius.

Lietuvai nereikalingi lietuviai dėl to, kad jie atsisako sieti savo gyvenimą su šalimi. Kam tokiu atveju prireikė Referendumo dėl daugybinės pilietybės?

Deja, iš tikrųjų, šitie emigrantai jau nebelaikomi Lietuvos piliečiais. Jie atsisakė Lietuvos. Todėl kad Lietuva atsisakė jų.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 13 — id: `scraped:rubaltic_lt:227c8aed94b7c88d`

**Title:** Nafta Baltijos jūroje tapo konflikto tarp Lietuvos ir Latvijos priežastimi

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuva ir Latvija — vienintelės šalys — Europos Sąjungos narės, iki šiol neturinčios aiškiai užfiksuotos tarpusavio jūros sienos. Praėjus dviems dešimtmečiams po sudarymo sutarties dėl pasiskirstymo jūros teritorija, „Pabaltijo sesės“ taip ir nesugebėjo išspręsti teritorinių vandenų ir žemės gelmių klausimo. Pagrindinė nesutarimų priežastis — potencialūs naftos telkiniai Baltijos jūroje.

Klausimas dėl jūros sienos tarp Lietuvos ir Latvijos iškilo iškart po Tarybų Sąjungos subyrėjimo. 1993 metais Latvija paskelbė ketinimus pradėti naftos gavybos žvalgybą Baltijos jūros šelfe. Nenorėdama likti nuošalyje, Lietuva pateikė savo pretenzijas šiame angliavandeniais turtingame ruože.

1995 metų gegužės mėnesį Latvija pateikė pasiūlymą nustatyti sieną pagal „vidutinę liniją“. Tačiau Lietuvos vyriausybė jį atmetė, nes tokiu būdu padalinus jūrų teritoriją, nustatytas naftos telkinys priklausytų Latvijai. Iš savo pusės Vilnius pasiūlė jūros sieną nustatyti tiesia linija nuo sausumos dviejų valstybių sienos iki sąlyčio su Švedijos ekonomine zona.

Ryga tebegynė savo teisę valdyti naftos telkinį Baltijos jūroje. 1995 metų pabaigoje latvių vyriausybė pasirašė sutartį su tarptautiniu konsorciumu Amoco Opab dėl naftos telkinio žvalgybos ir gavybos. Aptikus gavybai tinkamą naftos telkinį, Latvijai, pagal sutartį, turėjo atitekti 10 proc. išgautos naftos. Sutarties vykdymo sąlyga tapo teritorinio ginčo su Lietuva sprendimas. Tačiau per sutartyje numatytą laikotarpį Pabaltijo šalys taip ir nesugebėjo susitarti dėl jūros sienos.

Naujos sienos variantas pagal dokumentą panašus į tą, kurį anksčiau rėmė Lietuva — tiesi linija nuo Pabaltijo šalių sienos iki sąlyčio taško su švedų ekonomine zona. Susitarimas taip pat reglamentuoja žvalgybą ir gamtinių resursų gavybą teritoriniuose vandenyse.

Tuo atveju, jei naudingų iškasenų klodai slypi abipus jūros sienos, jie gali būti dalinai arba pilnai panaudoti tame tarpe tik vienos pusės, jeigu ši, savo ruožtu, suderina visas žvalgybos ir resursų gavybos sąlygas su antrąja valstybe. Taip pat įsigaliojęs susitarimas įpareigoja šalis pradėti derybas dėl jūros dugno ir jo gelmių sutarties sąlygų.

Tai ir tapo kliuviniu siekiant priimti galutinį dokumentą.

Kaip ir buvo galima tikėtis, po trijų mėnesių Lietuvos Seimas ratifikavo susitarimą. Pasirašyta sutartis Vilniui buvo naudinga — naujoji siena praplėtė Lietuvos vandenis maždaug dešimčia tūkstančių kilometrų.

Savo ruožtu, Latvija iki šiol neratifikavo sutarties, nes nuosekliai pasisako už pirmoje eilėje pasirašymą dokumento dėl ekonominio bendradarbiavimo kontinentiniame šelfe, ir tik po to neva gali būti aiškiai nustatyta tarp šalių jūrų siena.

Teritorinių vandenų dalybų klausimą pastoviai aptaria tarpvyriausybinė darbo grupė, tačiau iki šiol į priekį nežengta nė vieno žingsnio. Vienas iš variantų, kurį siūlo Ryga, — sutartį dėl ekonominio bendradarbiavimo šelfe ir jūros sienos ratifikuoti vienu paketu.

Naftos telkinių Baltijos jūroje priklausomybė yra pagrindinis, tačiau ne vienintelis prieštaravimas Lietuvos–Latvijos santykiuose jūros sienos nustatymo klausimu. Kitas sutarties ratifikavimo kliuvinys — žvejybinių zonų paskirstymo problema, tačiau po to, kai šalys įstojo į Europos Sąjungą ir buvo priimta kvotų sistema, nesutarimai šiuo klausimu nusikėlė į antrą planą.

Šiandien jūros sienos Susitarimo klausimas įvarytas į aklavietę.

Šalys lieka savo pozicijose ir neketina nusileisti viena kitai. Sutartį ratifikavusi Lietuva tvirtina, jog padarė viską, siekiant sureguliuoti ginčą, ir laukia iš Latvijos atsakomojo žingsnio, o tuo metu Ryga kategoriškai prieštarauja.

Kol jūros siena neužfiksuota, nė viena naftos kompanija nenorės šiame regione pradėti pilnavertės angliavandenių žvalgybos arba gavybos. Taip pasireiškia išgarsinta „pabaltijietiška vienybė“.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 14 — id: `scraped:rubaltic_lt:13125bc748c8f3ad`

**Title:** Lietuva moka už saugumo iliuziją

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Baltijos šalių militarizacija tęsiasi. Auga išlaidos valstybės apsaugai, o kariniai mokymai tampa vis intensyvesni, atnaujinama karinė infrastruktūra. Visa tai kartu su naryste NATO, kaip mano Estijos, Latvijos ir Lietuvos valdžios, užtikrina apsaugą nuo „Rusijos agresijos“. Deja, už saugumo iliuziją tenka mokėti realus pinigus. Bet ar militarizmas neužves Baltijos šalių į aklavietę ir socialine ir ekonomine prasme?

Priekiniame fronte

Taip ir neišnykę už pastaruosius trejus dešimtmečius po „antrosios nepriklausomybės“ iškovojimo praeities fantomai vis neduoda ramybės Baltijos šalių valdžioms. Estija, Latvija ir Lietuva, matančios tikrą grėsmę iš savo Rytų kaimyno, aktyviai plečia šią temą ir net grindžia ja savo identiškumą. Kreipiamasi ne vien tik į pasakojimus apie rusų kariuomenės potencialią invaziją, bet ir į spėliojimus apie kitokias galimas agresijos formas, įskaitant kiberatakas, kišimąsi į rinkimų sistemos organus ir masinę dezinformaciją.

Anot jų, Baltijos šalių demokratijų išsaugojimas priklauso nuo tarptautinių sąjungų ir susitarimų, kurie gali turėti įtakos Maskvai. O narystė Šiaurės Atlanto Sutarties Organizacijoje reikalauja sparčios militarizacijos bei išlaidų ginklavimuisi augimo tam, kad būti visiškai pasiruošę „Rusijos atlaikymui“ NATO priekiniame fronte.

Estija, Latvija ir Lietuva seka 2014 metų NATO viršūnių Velso susitikimo sprendimus, jų skirti apsaugai biudžetai vis auga, nors jau 2018 metais pasiekė NATO numatyto tikslo – skirti apsaugai 2% nuo šalies BVP. Beje, dar 2017 metais Latvijos gynybos ministras Raimonds Bergmanis teigė , kad „2% nuo šalies BVP numatyti gynybai sekančių metų biudžete – nėra ir neturėtų būti aukščiausia riba tuo atveju, kai mes norim vystytis ir eiti koja į koją su šiuolaikinėmis technologijomis ir žiniomis“.

Galios iliuzija

Žiūrint iš vienos pusės, tokia politika duoda savo vaisių. Baltijos šalys faktiškai tapo placdarmu, kuro NATO gali demonstruoti savo karinę galią visai arti Rusijos valstybinės sienos. Tad 2019 metais Estijoje, Latvijoje ir Lietuvoje vyks įvairaus mąsto bei skirtingų trukmės ir formos NATO mokymai, į kuriuos tarp kitko įtraukta kiberapsauga bei karinių oro pajėgų mokymai.

Šalys stiprina savo karinę infrastruktūrą, gerina apsaugos planavimą vieningo vadovavimo kūrimo dėka, o šių šalių oro erdvių apsaugą užtikrina Šiaurės Atlanto Sutarties Organizacijos šalys pagal NATO oro policijos misiją Baltijos šalyse.

Žiūrint iš kitos pusės, neverta užmiršti apie Baltijos šalių biudžetų absoliučius dydžius. „2% nuo šalies BVP“ rodiklis atrodo itin įspūdingai, bet žiūrint iš arčiau pasirodo, kad iš tikrųjų tai yra labai kuklus skaičius. Pavyzdžiui, 2018 metais Lietuvoje išlaidos apsaugai sudarė apie 1071 milijoną eurų, Latvijoje – 711 milijonų eurų, o Estijoje – 627 milijonus eurų. Tokios išlaidos nors ir sudaro aptarinėtus 2%, bet neprilygsta tu pačių metų išlaidoms gynybai Prancūzijoje (34,2 milijardai eurų) arba kaimyninėje Lenkijoje (10 milijardų eurų).

Finansavimo ribotumas sukelia kitą problemą.

Dažnai tokie užpirkimai tampa ne itin sėkmingomis investicijomis į gynybą, sukelia skandalų, kai kariškiai yra kaltinami korupcija ir nusenusių pirkinių žemu efektyvumu.

Ryškus pavyzdys - Latvijos karinių pajėgų pėstininkų brigados mechanizacijos bandymas, kai naudoti britų „šarvuočiai“ kainavo Baltijos šalies iždui brangiai, nors buvo nusenę. Arba atvejis, kai Lietuva įsigijo Vokietijoje dar Vietnamo karo laikų amerikiečių gamintus „šarvuočius“ M577, kurių eksploatavimas Bundesvere buvo nutrauktas.

Nagrinėjant Baltijos šalių karinių pajėgų būklę jų atsparumo „Rusijos grėsmei“ atžvilgiu, kyla itin nelinksmų išvadų.

Šiandien Baltijos šalims tenka mokėti NATO už savo saugumą ir būti Šiaurės Atlanto Sutarties Organizacijos poligonu tam, kad apsiginti nuo praeities fantomų.

Ginklai vietoj sviesto

Kol kas itin reikšminga Šiaurės Atlanto Sutarties Organizacijai tema išlieka 2% nuo BVP skyrimas apsaugai. Bet dar 2018 metais JAV prezidentas Donaldas Trumpas pasiūlė šią skaičių padvigubinti. Trumpo pareiškimas buvo ne formalus reikalavimas, o, greičiau, pasiūlymas didinti išlaidas apsaugai. Bet Baltijos šalys šitą pasiūlymą palaikė. 2018 metų lapkričio 24 dieną per šių šalių apsaugos institucijų vadovų susitikimą buvo patvirtintas ketinimas didinti gynybos biudžetus, kad jie viršytų 2% nuo šalių BVP.

Deja, nors kariškiai ir politikai labai nori didinti gynybos biudžetą, jie neišvengiamai patiria sunkumų su jo pertvarkymu.

Bet Baltijos šalių valdžios elitų šiandieninė pozicija teigia, kad išlaidos gynybai ir socialiniams poreikiams tampa lygiareikšmės. Kaip pareiškė Lietuvos prezidentė Dalia Grybauskaitė, „... jis [gynybos biudžetas] negali būti priešpriešinamas kitiems valstybėms poreikiams. O tos partijos, kurios mėgina priešpriešinti gynybą socialiniams poreikiams, elgiasi negražiai ir neatsakingai“.

Ką gi, gal žmonės, suvokiantys gynybos biudžeto didinimo būtinybę, elgiasi teisingai ir yra realistai. Bet ar bus įmanoma Baltijos šalims išspręsti piliečių nepasitikėjimo valdžia ir nusivylimo viešojo sektoriaus paslaugomis problemų bei emigracijos ir demografijos klausimų ginklų pirkimo ir poligonų plėtros dėka?

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 15 — id: `scraped:rubaltic_lt:e9167af56cca6250`

**Title:** Ukraina ir Lietuva pralaimėjo karą dėl komunizmo ir Stalino demonizavimo

**Source:** rubaltic_lt (propaganda)

**Text:**

```
J.Stalinui pritarimo lygis Rusijos visuomenėje pasiekė naują rekordą: jo nuopelnus šaliai teigiamai vertina 70 proc. respondentų. Žavesį, pagarbą ir simpatijas Stalinui pareiškė daugiau kaip pusė Rusijos gyventojų (51 proc.). Šie duomenys aktyviai aptarinėjami ne tik Rusijoje, bet ir užsienyje. Ir tik Pabaltijis, kuris laikė savo pareiga „palaidoti“ komunizmą visoje posttarybinėje erdvėje, kolkas visiškai tyli.

Apklausos, liečiančios požiūrį į Staliną, visada buvo palaiminga visokių manipuliavimų dirva. Jų rezultatai labai priklauso nuo to, kaip suformuluoti klausimai ir kuriuose istorijos puslapiuose sociologai akcentuoja lyderio vaidmenį. Didžiąjame Tėvynės kare Rusijos gyventojai kaip taisyklė vertina teigiamai. Tačiau požiūris tampa nuosaikesnis, kai kalbama apie 1937–1938 metų terorą, TSRS tautų deportacijas ir t.t.

Neseniai pravesta Levados centro apklausa sugriovė pastarąją tendenciją. 46 proc. respondentų mano, jog kažkokia prasme tos žmonių aukos, kurias tarybinė liaudis prarado prie Stalino, buvo pateisinamos. Tų, kurie kategoriškai atsisako jas pateisinti, vienu procentu mažiau.

Ukrainos užsienio reikalų ministras Pavlas Klimkinas niršta iš pykčio. Klausimą apie žmonių aukų pateisinimą jis pavadino „žmogėdrų testu“, o viso tyrimo rezultatus charakterizavo taip: „Kremliaus režimas dar kartą įrodė, kad meistriškai įvaldė klastingiausius masiškos sąmonės manipuliavimo metodus ir šiuo metu didesnę rusų visuomenės dalį laiko zombių būklėje“.

Aktoriaus oponentai taip pat kalba apie pasakišką manipuliavimo technologijomis efektyvumą, nors tikrąsias jo triumfo priežastis sunku nepastebėti. Ta pati istorija su Stalinu: patyrusio ūkininko, „stiprios rankos“, socialinio teisingumo paklausa.

Pagrindinė Klimkino išvada skamba taip: „Visuomenės pavertimas zombi ir humanizmo neigimas tampa reiškiniais pavojingais, galinčiais režimo įsakymu diegti didelį blogį“. Tai yra su „neteisingais“ rusais reikia kažką daryti. Pasmaugti „komunistinę bjaurybę“ vos jai užgimus, kol šalis galutinai nenusirito į totalitarizmą.

Pabaltijietiški Klimkino draugai, atsakydami į jo postulatus, gali tik liūdnai nusišypsoti.

Rusijoje — taip pat. Surizikuosime konkretizuoti: pirmiausia Rusijoje! Juk būtent ji tapo Tarybų Sąjungos teisių perėmėja.

Šios kovos dalimi tapo reikalavimai atlyginti Pabaltijo respublikoms už „sovietinės okupacijos“ metais patirtus nuostolius. Ekspertai ir žurnalistai dažnai kalba apie finansinę klausimo pusę, tačiau pamiršta, kad Lietuvai, Latvijai ir Estijai reikia paties Maskvos atgailavimo fakto dėl savo totalitarinės praeities. Lietuvos genocido ir rezistencijos tyrimų centro direktorė ir taip vadinamos „komisijos sovietinės okupacijos nuostolių atlyginimo klausimu“ vadovė Teresė Birutė Barauskaitė nedviprasmiškai pareiškė, jog moralinė kompensacija jos šaliai daug svarbesnė, negu materialinė.

„Niekas nekaltina dabartinių Rusijos gyventojų, rusų tautos, — komentuoja Barauskaitė. — Tai buvo žiaurus totalitarinis režimas ir komunistinė ideologija, kuri atnešė daug kančių ir Rusijos gyventojams, visos TSRS tautos nuo to nukentėjo“.

Taigi atgailaukite patys sau! Pasmerkite komunizmo baisumus, prie gėdos stulpo prikalkite Staliną.

Kodėl rusai nereaguoja į patarimus?

Tarybų Sąjungos tautos jos atsisakė savo noru. Ir visai taip pat geranoriškai jos gali pakeisti požiūrį į ją.

Žinoma, profesionaliems Pabaltijo šalių antitarybininkams visa tai neduoda ramybės. Jie norėtų matyti komunizmą fiziškai nugalėtą ir sutryptą. Neatsitiktinai Lietuvos valdžios taip jaudulingai žvelgia į „sovietinės agresijos“ 1991 metų sausio 13-osios mitą. Tai buvo jų mažytė pergalinga kova. Tik tas „karas“ tų pačių metų gruodžio mėnesį kažkaip neteisingai užsibaigė. Nei tankų Maskvos gatvėse, nei Kremliaus griuvėsių, nei sutryptų tarybinių vėliavų...

O dabar aiškėja, kad muštas priešas gyvas.

Ne, tegul ten sau murdosi Rusija! Svarbiausia — Europa turėjo suprasti, kad komunizmas ir nacizmas — broliai dvyniai. Pabaltijo šalys ir jai stengėsi “įpūsti” proto.

Gana keistai jos bandė atkreipti dėmesį į šią temą įstojimo į ES išvakarėse. Lietuvos, Latvijos ir Estijos atstovai paruošė bendrą pareiškimą, smerkiantį komunizmą, ir neslėpė, jog ketina “išspausti” šią tematiką Europos lygyje. Rezultatas nepakilo aukščiau nulio.

Po poros metų “naujokai” nevykusiai pabandė uždrausti Europos Sąjungoje komunistinę simboliką priimant įstatymą apie rasizmą ir ksenofobiją. Jiems pritarė čekai, vengrai, slovakai. Tačiau tuoj pat susilaukė antausio: Europos komisija atmetė šį pasiūlymą, o komisaras teisėsaugos klausimais Franko Fratini tiesiai pareiškė, kad “nutarimas visoje Europoje uždrausti šiuos simbolius bus kvailas ir sunkiai paaiškinamas”.

Pirmasis apie tai prakalbo Estijos justicijos ministras Urmas Reinsaly: “Mes privalome įvertinti komunizmo režimo nusikaltimus tarptautiniame lygyje ir kartu juos pasmerkti. Komunistinio režimo nusikaltimai šiandien viršija kompetenciją bet kurio tarptautinio teismo”.

Su šia idėja estų ministras nubėgo pas Lietuvos ir Latvijos kolegas. Tačiau toliau kalbų reikalai nejuda. Net ant antirusiškos isterijos bangos užšokusi “Senoji Europa” neturi noro dalyvauti tokiose avantiūrose. Belieka vienintelis variantas — sukurti trijų improvizuotą tribunolą.

Kaip žinia, reikalavimai kompensacijų už “sovietinę okupaciją” taip pat nesulaukė paramos tarptautinėse organizacijose, nors tas pats Reinsalu kartu su latvių justicijos ministru Dzintarsu Rasnačsu ketino šį klausimą spręsti JT lygyje.

Pabaltijis gali pasigirti nebent neseniai pateiktu Europos Parlamentui rezoliucijos projektu, kuris ragina Rusiją”pasmerkti komunizmą ir sovietinį režimą”. Balsų dauguma jis buvo priimtas. Tačiau EP daug ką priima. Jis ir “Šiaurės srautą–2” ragino sustabdyti.

O pagal faktą niekur be atskirų rytų europietiškų “demokratijų” komunistų partijos neuždraustos, juolab — komunistinė simbolika. Eiliniams europiečiams Tarybų Sąjungos demonizavimas nesuprantamas ir neįdomus, o Rusijoje didėja pritarimo lygis istoriniam veikėjui, kuris pavertė TSRS galinga šalimi.

Tai tokie jie, liūdni Pabaltijo kovos su tarybinės praeities šmėkla rezultatai.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 16 — id: `scraped:rubaltic_lt:eef25e6d74912a67`

**Title:** Linksmas snukių daužymas: kaip NATO kariškiai „gina“ Lietuvą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Pabaltijo šalių, Lenkijos ir Ukrainos valdžios pavydėtinai atkakliai kviečia į savo teritoriją NATO kontingentus tikslu ginti nuo „rusų grėsmės“. Rytų kariškiai niekaip nesusiruošia pulti, užtat kariai-gynėjai pastoviai tampa susidūrimų su vietos gyventojais dalyviais, o kartais ir kriminalinių suvestinių figūrantais.

Tokių atvejų apstu, yra ir visiškai „šviežutėlių“. Antai balandžio 14 dieną Povidz miesto lenkai apkūlė NATO kariškius už tai, kad amerikiečių konvojus posūkyje rėžėsi į vietinio gyventojo tvorą. O jau kitą dieną Vilniuje, įtariant apiplėšimu, buvo sulaikytas norvegų kariškis. Įtariamasis kartu su keturiais bendrais užpuolė Vilniaus gyventoją, atėmė iš jo du telefonus ir pinigus. Analitinis portalas RuBaltic.Ru nutarė atkurti nusikalstamą kroniką įvykių, kurių dalyviais tapo atvykę Pabaltijį ginti NATO kareiviai.

Natininkų godos Klaipėdoje

Visai neseniai, 2019 metų balandžio 6 dieną, į Klaipėdos ligoninę buvo atvežtas latvių kariškis su galvos trauma. Pasak nukentėjusiojo, jį po vidurnakčio kruizinių laivų terminale sumušė nepažįstami asmenys.

Nuostabu, bet tos pačios dienos rytą Klaipėdoje nukentėjo dar vienas NATO kariškis iš Latvijos. Nusikaltėliai užpuolė jūrų pajėgų kariškį, pagrobė jo mobilųjį telefoną, pinigus ir dokumentus.

Latvijos policija mums nė motais

2018 metų balandžio 24 dieną Rygoje vėl pasižymėjo britų kariškiai. Po to, kai jie girti sukėlė riaušias, į konflikto vietą atvyko vietos policija. Tačiau NATO kareiviams į latvių teisėsaugininkus nusispjaut. Todėl prasidėjo muštynės. Siekiant sutramdyti suįžūlėjusius britus, kurie buvo atvykę „ginti“ Latvijos nuo „agresoriaus“, teisėsaugininkų pajėgos buvo priverstos panaudoti pipirines dujas.

Padeda tik elektrošokeriai

2017 metų vasario 19-osios naktį Klaipėdos teisėsaugos organų darbuotojai atvyko į vietinį klubą Portas tikslu apraminti siautėjusius NATO kareivius iš Čekijos.

Kariškiai atvyko į Lietuvą tik sausio viduryje, tačiau to pakako, kad čia pasijustų tikrais šeimininkais. Todėl nenuostabu, kad jie tiesiog atsisakė paklusti policijos reikalavimams ir nutarė pasipriešinti. Siekiant įvesti tvarką, teisėsaugininkai čekus ramino elektrošokeriais.

Nelįsk į svetimą daržą

2017 metų gegužės 25 dieną penkiasdešimt šešerių metų estų kaimo Ochepalu gyventojas netikėtai aptiko savo darže NATO kareivius, atvykusius į Pabaltijį dalyvauti manevruose Kevadtorm („Pavasario štormas“). Kad atsikratytų nekviestais svečiais, žemės sklypo savininkas buvo priverstas griebtis ginklo. Suįžūlėjusių natininkų laimei, šūvį žmogus paleido į orą. Tačiau ir to pakako, kad nekviesti „keliauninkai“ tuoj pat paliktų svetimą daržą.

Naktį girtam nedera vaikščioti

2017 metų birželio 3-iosios naktį buvo sudrumsta ramybė Jonavos miesto gyventojų: keturi girti Vokietijos kariškiai sukėlė masiškas muštynes. Šį kartą vokiškieji svečiai patyrė nesėkmę — NATO bataljono kariai neblogai gavo į kailį.

Mes privalome už kažką mokėti?

2017 metų liepos 1 dieną du girti NATO kareiviai iš Nyderlandų susiginčijo su Vilniaus restorano darbuotoju dėl sąskaitos apmokėjimo. Lietuvis, pateikęs sąskaitą, nepajėgė pasipriešinti ir buvo sumuštas; dėl galvos traumos jam teko kreiptis medikų pagalbos. Konflikto metu greta buvo dar du Nyderlandų kariškiai, tačiau jie piršto nepajudino, kad girti bičiuliai būtų sutramdyti.

Tu mane gerbi?

2016 metų gegužės mėnesį Rukloje, netoli Kauno, susipešė išgėręs lietuvis ir trys čia dislokuoto garnizono vokiečių kariškiai. Šie taip pat buvo gerokai įkaušę.

Mušk saviškius, kad svetimi bijotų

2017 metų spalio mėnesį vėl buvo susimušta Ruklos bare. Šį kartą susimušė du vokiečių kariškiai — po to, kai smagiai nusigėrė. Vienas iš „kovotojų“ pateko ligoninėn.

Čia vertėtų priminti, kad siunčiant iš Vokietijos į Pabaltijį kariškius jiems buvo įsakyta elgtis santūriai, ypač išeinant į miestą, kad nepakenktų NATO ir Vokietijos kariuomenės reputacijai.

Kariniams mokymams tinka ir taksi

2016 metų birželio mėnesį du NATO kareiviai iš Jungtinės Karalystės, atvykę į Latviją dalyvauti kariniuose mokymuose Saber Strike, nutarė išbandyti savo narsą ir drąsą atsitiktinai sutiktame taksi. Kai vienas kariškis ėmė ant automobilio stogo šokti, kitas dėl kompanijos taip pat bandė užsikabarnoti. Kaip jūs jau supratote, abu „didvyriai“ buvo gerokai įkaušę.

Latviai muša britus, o kaltas Kremlius?

2016 metų pabaigoje Rygoje nežinomi asmenys užpuolė britų karius. Šį veiksmą nufilmavo atvykusi į įvykio vietą grupė.

Didžiosios Britanijos karinė tarnyba paaiškino įvykį iš Rytų pusės vykdomu hibridiniu karu — Rusija suinteresuota parodyti Pabaltijyje tarnaujančius NATO karius chuliganais ir teisėtvarkos pažeidėjais.

Problemos dėl sąskaitos už važiavimą

2014 metų balandžio 25 dieną keturi amerikiečių natininkai, šauniai pailsėję Senojoje Rygoje, nutarė sugrįžti į savo būstinę. Jau prie viešbučio įvyko konfliktas su taksi vairuotoju. Jam pagalbon atskubėjo verslo kolegos. Kilo muštynės, kurių metu vienam JAV kariškiui buvo apdaužytas veidas.

Nevykęs dalyvavimas diskotekoje

Taip pat 2014 metų balandžio mėnesį NATO kareivis iš Nyderlandų, atvykęs dalyvauti tarptautinėje išminavimo operacijoje Open Spirit–2014 Ventspilyje, nutarė atsipalaiduoti šokių aikštelėje. Užsibaigė jam tai gana liūdnai, nes lankytojai nepanoro jo čia matyti. Jūrininkas buvo atgabentas į ligoninę be sąmonės su sunkia galvos trauma, veido kaulų lūžiais ir smegenų pabrinkimu. Medikų pagalbos, nors ir menkesnės, prireikė dar keliems jūrininkams, ignoravusiems rekomendacijas nelankyti latvių naktinių klubų.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 17 — id: `scraped:rubaltic_lt:df817d103cf38d01`

**Title:** Apsėsta pavyduliavimo, Lietuva nenori dalintis Estija su Putinu

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos Respublikos užsienio reikalų ministras Linas Linkevičius pasmerkė Estijos prezidentės Kersti Kaljulaid susitikimą su Rusijos prezidentu Vladimiru Putinu Maskvoje. Anot Lietuvos URM Kaljulaid elgesys ardo Baltijos šalių vieningumą, o Estijos lyderė privalėjo suderinti veiksmus su Lietuvos ir Latvijos kolegomis prieš vykstant į Rusiją. Už oficialaus Vilniaus pozicijos slypi banalus moteriškas pavydas Estijos prezidentei, kuri lygiomis teisėmis bendrauja su Putinu, kol kai kurie Lietuvos valdžios atstovai tokią galimybę yra visiškai praradę.

„Paprastai kai koordinuojame ir vieningiau veikiame, visada tai yra efektyviau, nes visada išlieka bandymai mus skaldyti ir visą laiką tikrinti Europos šalių ar Baltijos šalių vienybę“, - teigė Lietuvos užsienio reikalų ministras Linas Linkevičius, kalbėdamas apie Baltijos šalių, kurios įprastai tarpusavyje derina bendravimą su Maskva, užsienio politiką.

Estijos prezidentė to nepadarė, kuo labai įžeidė Lietuvos ministrą.

Kas „blogiausia“, Kaljulaid neinformavo Vilnių apie savo susitikimą Kremliuje net po to, kai jis įvyko. Lietuvos ministras išreiškė viltį, kad Estijos prezidentė anksčiau ar vėliau vis gi pasidalins informacija apie susitikimą su Putinu ir paprašė jos ateityje būti atsargesnei bendravime su Rusijos lyderiu, derinti visus kontaktus su Rusija su kitomis Baltijos šalimis ir neardyti Baltijos šalių vieningumo.

Linkevičiaus pareiškimai tokie, kad „bet pasakyk kam nors, nepatikės“. Vienos šalies užsienio reikalų ministras kritikuoja kitos šalies prezidentą, dėl to, kad pastarasis nepraneša jam apie savo derybas su trečiosios šalies prezidentu. Iškart po lankymosi pas Putiną Kersti Kaljulaid turėjo keliauti į Vilnių pas Linkevičių atsiskaityti. Net į JAV ambasadą užsukti nereikėjo – Linkevičius paskui pats užeitų.

Tiems, kurie nėra susipažindinę su išskirtine lietuvių „diplomatijos“ mokykla, sunku patikėti, kad tokie priekaištai iš Vilniaus pusės – rūsti tikrovė, o ne absurdo teatras.

Estijos įžeistas Lietuvos užsienio reikalų ministras prieš kelis metus palygino Putiną su Hitleriu ir ragino visuotinę Rusijos diplomatinę izoliaciją. Dalia Grybauskaitė seniau vadindavo Rusiją „teroristine valstybe“ ir viešai spėliojo apie šalies prezidento psichines traumas, kai savo interviu vokiečių žurnalui pavadino Putiną „paranojiku“.

Po tokių pareiškimų šitie veikėjai neturi net menkiausios galimybės tiesioginiam dialogui su Maskva. Dar po „teroristinės valstybės“ Dalia Grybauskaitei buvo leista suprasti, kad Rusijai nei ji, nei jos atstovai daugiau nebeegzistuoja.

Estijos patirtis parodo, kad Lietuvos ir Rusijos santykiai nėra visiems laikams pasmerkti. Abstraktus Lietuvos prezidentas galės susitikti su Rusijos prezidentu. Bet Lietuvos prezidentė Dalia Grybauskaitė galimybę su juo bendrauti visiškai prarado.

Lygiai taip pat abstraktus Lietuvos užsienio reikalų ministras gali vesti derybas su kolegomis iš Rusijos. Tačiau konkrečiai su Linu Linkevičiumi Maskvoje net nekalbės.

Įamžinimo anekdotuose verta Lietuvos užsienio reikalų ministro reakcija dėl Estijos prezidento vizito pas Putiną – banalus pavydas. Negana to, šitas pavydas – ne jo paties išgyvenamas jausmas: „siauruose ratuose“ ponas Linkevičius yra vadinamas „Jos Prakilnybės pažu“, nes visi jo pasisakymai transliuoja valstybės vadovės požiūrius.

Taigi, šitas pavydas – tiktai Dalios Grybauskaitės moteriškas pavydas. Ne jai, „geležiniai Baltijos ledi“, leistina lygiateisiškai vykdyti dvipuses derybas su Vladimiru Putinu Kremliaus rūmų Jekaterinos salėje. Jai nebelemta nieko svarbesnio už Baltijos šalių vadovų bendrų susitikimų su JAV prezidentu, Europos Komisijos pirmininku ir Vokietijos federaliniu kancleriu.

Įskriausto „pažo“ Linkevičiaus pareiškime galima įžiūrėti net „konstruktyvų pasiūlymą“: tegul mes Baltijos šalių vienybės ir saugumo vardan ir su Putinu susitiksime kartu? Bet nei jis, nei jo „matrona“ to nesulauks: į Kremlių Grybauskaitė su Linkevičiumi net su turistų grupe nepateks.

Kersti Kaljulaid ne kartą pasižymėjo antirusiškais pareiškimais, bet kritikuodama Rusijos veiksmus niekada neperžengdavo “raudonosios linijos” ir nevartodavo neapykantos kalbos. Mandagus elgesys ir nulėmė tai, kad Kremliuje Kaljulaid buvo priimta su tokia pagarba, kokios neteikia Baltijos sąjungininkams Vašingtonas. Priimta kaip garbinamas oponentas. Oponentas, bet garbinamas.

Estijos prezidentės komunikacijos taktika tapo sėkminga.

Toks įvaizdis sparčiai suteikia reikšmingumo Estijos prezidentei Vakarų šalių akyse. O kokios yra, lyginant su Kaljulaid, profesionalų rusofobų, kuriems priklauso ir Grybauskaitė, reputacijos? Visai neseniai artimas Grybauskaitės požiūriams į Rusiją buvęs Lietuvos ministras pirmininkas Andrius Kubilius pralošė Europos Tarybos generalinio sekretoriaus rinkimus. Ir nulėmė tai priežastis, kad išskyrus kovą su Kremliumi šis veikėjas niekuo daugiau nepasižymi. O tarptautiniai biurokratijai toks “galvos skausmas” visiškai nereikalingas.

Tad ir Dalios Grybauskaitės bei jo “pažo” jokia išskirtinė sėkmė tarptautinėje politikoje ateityje nelaukia. Jie pastatė viską ant kortos, galvodami, kad Rusijos ir Vakarų santykių krizė ir Maskvos tarptautinė izoliacija truks amžinai, o jų aistringos ir pilnos neapykantos Kremliui kalbos visada bus reikalingos.

Pastatė ir pralošė. Tegul dabar liūdi vienatvėje savo numylėtame rusofobijos apkase ir nepavydi tiems, kas pasielgė daug protingiau

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 18 — id: `scraped:rubaltic_lt:ec88b5e634b1d0a9`

**Title:** Lietuva slaptai perka iš Rusijos SGD terminalui reikalingas dujas

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuva slaptai perka iš Rusijos savo SGD terminalui suskystintas gamtines dujas. Tokia sensacinga išvada peršasi pasitelkiant laivų Baltijos jūroje stebėjimo sistemas. Lietuvos valdžios nieko nesakė gyventojams apie suskystintų dujų pirkimą iš Rusijos, ir tai nenuostabu, nes Lietuvos SGD terminalas paskelbtas „energetinės nepriklausomybės“ diegimo projektu.

Rusijos kompanija „Novatek“ metų pradžioje įvedė rikiuotėn suskystintų gamtinių dujų gamybos gamyklą „Kriogaz–Vysock“. Nuo šio mėnesio gamykla pradeda savo produkcijos eksportą. Pagrindiniai vartotojai — Baltijos jūros regiono valstybės.

„Refinitiv Eikon“ duomenimis, „Novatek“ nuo kovo 31 d. iki balandžio 16 d.išsiuntė iš Vysocko uosto septynis krovinius bendro 67800 kūbinių metrų užšaldytų dujų tūrio. Tris krovinius gavo Klaipėdos uostas, po vieną iš suomių uostų Tachkoluoto (Pori) ir Tornio, o likę du iškeliavo į Visbi ir Ninašamn Švedijoje“, — rašo Reuters.

Ir štai čia — būgnų garsai!

Lietuvos valdžios ir Klaipėdos terminalo Independence menedžeriai neprasitarė visuomenei pasirašę kontraktą su „Novatekom“ dėl suskystintų dujų tiekimo SGD terminalui iš Leningrado srities.

Iš ekoniminės pusės tame nėra nieko nuostabaus. Analitinis portalas RuBaltic.Ru dar praeitų metų rudenį prognozavo, jog taip atsitiks, kai JAV, nepaisydamos savo ryžto pašalinti Rusiją iš Europos dujų rinkos, pirko rusų suskystintas dujas šalančio Bostono apšildymui. O kodėl nepirkti, jeigu rusų SGD pigesnės nei savos, amerikietiškos?

„Tų pačių amerikiečių veikla pačioje Amerikoje rodo Europos šalims efektyvaus sprendimo pavyzdį. Išlaidos SGD terminalų sukūrimui gali pasiteisinti, jeigu vietoj amerikiečių produkcijos jie bus „maitinami“ Rusijos suskystintomis gamtinėmis dujomis“, — tada rašė RuBaltic.Ru.

Kaip sakoma, nepraėjo nė metų...

Suprantamas žmogaus, nežinančio savo šalies užmačių, susidomėjimas: kodėl Klaipėdos terminalo vadovams reikia kaip partizanams tylėti, slėpti nuo tautos pelningą sutartį? Užtat žinantys iškart supras, kame reikalas. Ekonominis Lietuvos pasiekimas, žvelgiant iš politinių aukštumų, nusikalstamas.

Tokio „nusikaltimo“ išties geriau neskelbti. Iš gėdos sudegsi. Alternatyva vamzdinėms dujoms iš Rusijos tapo suskystintos dujos ... iš Rusijos. Kova su rusų energetine monopolija baigiasi tuo, jog SGD terminalas perka rusų suskystintas dujas.

„Klaipėdos naftos“ veiksmų logiką galima suprasti.

Kataro, amerikiečių ir norvegų dujos, kurias įvairiais metais pirko Independence, brangesnės nei rusų. Kaimynai SGD terminalo produkcijos neperka, savas stambus verslas nepatenkintas būtinybe bendradarbiauti su Independence, trys ketvirtadaliai terminalo galingumų nenaudojami, išmokos norvegams už laivo nuomą neišsiperka, premjeras ir energetikos ministras atviraudami plaukiojantį terminalą vadina „Lietuvos mokesčių mokėtojų našta“.

Į SGD rinką atėjimas Rusijos kompanijų — reali galimybė išvengti žeminančios Lietuvos SGD terminalo bankroto procedūros. Trys suskystintų dujų kroviniai, atkeliavę į Klaipėdą iš Leningrado srities, tik pirmosios kregždutės. Rusijos SGD tiekimo Baltijos jūros regionui apimtys kasmet didės.

Suskystintas gamtines dujas Pabaltijo regione jau gamina „Gazpromui“ priklausančios mini-gamyklos „Kriogaz“ Pskove ir Kingisepe — jų galingumai atitinkamai 23 tūkstančiai ir 10 tūkstančių tonų per metus. Šiuo metu „Kriogaz“ stato SGD gamybos gamyklas Petrozavodske (100 tūkstančių tonų) ir Kaliningrade (150 tūkstančių tonų). Jau eksploatuojamas Vysocke 660 tūkstančių tonų galingumo „Kriogaz“.

SGD kompanija „Gorskaja“ stato Sankt-Peterburge 1,2 milijono tonų galingumo per metus suskystintų gamtinių dujų gamyklą. Praeitais metais „Gazpromas“ pasirašė rėminę sutartį su olandų Royal Dutch Shele dėl techninio „Pabaltijo SGD“ projekto paruošimo Ust-Lugos uostui 10 milijonų tonų suskystintų gamtinių dujų per metus galingumu.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 19 — id: `scraped:rubaltic_lt:16b7ef74a9f0af86`

**Title:** Neramumai dėl Brexit’o kartu su Didžiąja Britanija sukrėtė ir Lietuvą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Skubame ES viršūnių susitikime buvo nuspręsta atidėti Brexitą. Jungtinės Karalystės ministrė pirmininkė Theresa May turės dar kelis mėnesius tam, kad rasti išeitį iš beviltiškos padėties, deja niekas nesupranta, ką jinai ketina daryti. Artimiausiu laiku Didžiąją Britaniją vėl sudrebins Brexitas, tačiau situacijos neaiškumas privertė susinervinti ir Lietuvą.

Juokavę apie tai, kad Jungtinės Karalystės išstojimu iš ES galima mėgautis amžinai, buvo gerokai tiesūs. “Brexitas” pavirto tragikomedija, kuri vienus žiūrovus nuvargina, o kitus – linksmina. Bet šio veiksmo dalyvius juokas tikrai neima.

Balandžio pradžioje Britanijai ir Europai grėsė “kietosios skyrybos”, kurių stengiasi išvengti abi pusės. Sprendimas dėl išstojimo atidėjimo tarsi savaime piršosi.

Stebint iš šalies viskas atrodė padoriai: Theresa May pasiūlė “atstumti” Brexit’o realizacijos terminą, o Europos Vadovų Tarybos Pirmininkas Donaldas Tuskas balandžio 10 dieną surinko skubų susitikimą.

Jungtinės Karalystės ministrė pirmininkė tikisi įveikti tikslą greičiau. Prieš balsavimą May teigė jog nėra pasiruošusi tam, kad išstojimas būtų atidėtas vėliau už birželio 30 dieną. Bet Tuskas, kuris viską laiką stebėjo jos nesėkmingas pastangas, užsiminė, kad ES pasiruošusi dar kartą peržiūrėti Jungtinės Karalystės išstojimo terminus. Ir šis scenarijus yra itin tikėtinas.

Ką suteiks Theresai May išstojimo atidėjimas pusmečiui? Pats Tuskas pasiūlė savo “draugams iš Britanijos” tris variantus: ratifikuoti galutinę „skyrybų sutartį“, peržiūrėti Brexit’o strategiją arba iš vis atšaukti pranešimą dėl išstojimo iš ES. Neaišku, ką jis turi omenyje kalbėdamas apie strategijos peržiūrėjimą.

Iš esmės Jungtinės Karalystės ministrė pirmininkė prarado galimybę manevruoti ir siekti kompromisų: Briuselis atsisako keisti patvirtinto susitarimo sąlygas.

Jau triskart May bandė “prastumti” sutarimą naujom sąlygom per parlamentą, bet veltui. Ir, galbūt, jai tai nepavyks nei iki birželio 30-os, nei iki spalio 31-os. Po pusmečio Londonas gali atsidurti tokioje pačioje padėtyje kaip ir dabar.

Brexito atidėjimas – neabejotinas įrodymas, kad Didžioji Britanija atsidūrė aklavietėje ir nežino kaip tai išspręsti. Sprendimo variantai gali būti skirtingi. Ar galima garantuoti tai, kad May nepavyks pasiekti susitarimo su Briuselio sąlygų peržiūrėjimo? Iš kitos pusės, ar potencialūs pasidavimai padės priversti parlamentą pakeisti savo nuomonę?

Tarptautinio humanitarinių ir politinių tyrimų instituto ekspertas Vladimiras Bruteris siūlo labai neįprastą scenarijų: Brexitas bus atidedamas iki sekančių Jungtinės Karalystės parlamento rinkimų. Tikėtina, kad valdžią pasieks leiboristai, kurie iš vis atsisakys Brexito. Galų gale, negalima atmesti ir “kietojo Brexito” galimybę.

Neaiškumo jausmas vargina Europą. Ankščiau Briuselis duodavo suprasti, kad yra pasiruošęs suteikti Theresai May išstojimo atidėjimą tuo atveju, jeigu jinai turės aiškų susitarimo ratifikacijos planą. Apie tai ES šalių užsienio reikalų ministrai kalbėjo vos prieš dieną iki susitikimo. Galutinai Brexitas buvo atidėtas, bet May iki šiol neturi jokio plano. Savaime peršasi klausimas: kaip teks veikti ES institucijoms sąlygomis, kai Didžioji Britanija vis negali apsispręsti?

Didžiajai Britanijai teks dalyvauti rinkimuose jei šalis neratifikuos išstojimo iš ES susitarimą iki gegužės 22 dienos – šita sąlyga nurodyta priimtame sprendime dėl termino atidėjimo. Tuo atveju, jeigu Jungtinėje Karalystėje rinkimų nebus, iš Londono bus reikalaujama įvykdyti Brexitą iki gegužės 31 dienos, o ne iki spalio 31 dienos.

Nors May ir neatmeta galimybės “prastumti” naują susitarimą iki gegužės 22 dienos, tačiau šansų tai padaryti ji turi nedaug. Ministrei pirmininkei vėl bus trukdoma, nes ES rinkimai Jungtinėje Karalystėje yra stiprus smūgis Brexitui, kuris sutvirtins kovojančių už pakartotiną balsavimą pozicijas. Dar vienas visai ne tuščias klausimas: koks bus išsirinktų per rinkimus Britanijos deputatų statutas, kai (arba tuo atveju, jeigu) šalis išstos iš Europos Sąjungos?

Europos parlamento rinkimai yra vien tik ledkalnio viršūnė.

Nėrimo priežastis akivaizdi: tuo metu, kai lietuvių skaičius Baltijos šalyje vis mažėja, Jungtinėje Karalystėje jų – šimtai tūkstančių. Kaip tik su šitais žmonėmis yra susieti Lietuvos valdžios nėrimai.

Po Brexito vyriausybė ketina sugriežtinti migracijos įstatymus ir atimti lengvatas iš ES šalių darbo migrantų. Kalbama apie dosnias socialines pašalpas, kurios ir patraukė Baltijos šalies gyventojus.

Pasikeitusi situacija Didžiosios Britanijos lietuvius privers priimti vieną iš dviejų sprendimų: likti migrantais, turinčiais žymiai mažiau teisių už vietos gyventojus, arba pakeisti Lietuvos pasą į Didžiosios Britanijos (t.y. atsisakyti Lietuvos pilietybės Didžiosios Britanijos pilietybės naudai). Akivaizdu, kad pastarasis sprendimas daugumai bus labiau pageidautinas.

Tam, kad to išvengti, Lietuvos Seimas priėmė sprendimą paruošti referendumą dėl dvigubos pilietybės instituto plėtros. Šis referendumas bus laikomas kartu su šalies prezidento rinkimais.

Lietuvos valdžia iš visų jėgų remia šitą sprendimą, tačiau ar jis vertas tokių aukų? Gal Londonas pakeis savo požiūrį į darbo migrantus?

Galų gale Brexitas iš vis gali neįvykti. Bet mes sužinosime apie tai ne anksčiau kaip po pusmečio, o balsuoti teks jau kitą mėnesį...

Nemažai klausimų kyla ir dėl žmonių, kurie nuspręs išsaugoti Lietuvos pilietybę, likimo. Kaip Londonas elgsis su jais? Susitikimų su kolegomis iš Didžiosios Britanijos metu Lietuvos atstovai ne kartą kėlė šitą temą ir darė užuominas, kad tikisi sulaukti palankumo iš Jungtinės Karalystės.

Įstatymus dėl Lietuvos paruošimo Brexitui Seimui pristatė Lietuvos Respublikos Užsienio reikalų ministras Linas Linkevičius. Dalis jų parlamentarai patvirtino dar balandžio 10 dieną. URM iniciatyva siekia tai, kad net “kietojo Brexito” atveju Didžiosios Britanijos piliečiams būtų suteiktos kuo palankesnės sąlygos. Britų Lietuvoje gyvena nedaug – apie 400 žmonių, bet, susirūpinęs dėl jų likimo, Seimas jau ruošia skirtus jiems įstatymus.

Dar vienas svarbus klausimas – naujo ES biudžeto 2021-2028 metams sudarymas.

Jeigu Brexitas užsitęs (o viskas taip ir ketina būti), Londonas bus priverstas prisidėti

prie bendros “taupyklės“. Lietuvai tai duoda viltį išsaugoti bet dalį dotacijų iš Europos Sąjungos fondų.

Pareikštas dotacijų apribojimas susietas su tuo, kad iš „Europos tautų šeimos“ pasitraukia vienas jos pagrindinių „donorų“. Arba jau nebepasitraukia?

Pagaliau, Brexito tema svarbi Lietuvai politiniu atžvilgiu. Anot britų leidinio Daily Mail, Theresa May laiko Baltijos šalis bei Lenkiją instrumentais, kurių dėka gali paveikti nepalenkiamą Briuselio poziciją. Be to, Londoną remia ir JAV prezidentas Donaldas Trumpas, kuris po Brexito atidėjimo iškritikavo Briuselį už nereikalingą nepalenkiamumą.

Jeigu europiečių bei anglosaksų konfrontacija suaštrės, Baltijos šalys atsidurs tarp dviejų ugnių.

Lietuva laiko nepriklausomybę svarbiausia tautos ir valstybės vertybe. Bet griežta realybė griauna lietuviškas „oro pilis“. Tarptautinė konjunktūra priverčia Lietuvą rengti referendumus, keisti nacionalinę įstatymų sistemą bei manevruoti tarp skirtingų politinių jėgų centrų.

Britanijos išstojimo iš Europos Sąjungos istorija tai puikiai parodo.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 20 — id: `scraped:rubaltic_lt:2d69df01679ddf2f`

**Title:** Lietuvos URM ir ambasada Rusijoje išniekino Vilnių

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Neregėtas korupcijos skandalas, įsiliepsnojęs dėl Lietuvos Respublikos ambasados Rusijoje, smarkiai pakenkė tarptautiniam Lietuvos imidžui, be to, tą smūgį padvigubino Baltijos šalies Užsienio reikalų ministerija. Lietuvos diplomatai yra įtarti kyšių ėmimu. Maža to, Lietuvos diplomatinė tarnyba mėgino nukreipti dėmesį nuo šio įvykio, pakišdama nuolatinę “Rusijos agresijos” temą ir nežinia kam prikalbėjo nesąmonių dėl Maskvoje esančio ambasadoriaus pareiškimo dėl Sausio 13-osios bylos nuteistų sovietų kareivių. Situacija virto baisiausia gėda.

Balandžio 7 dieną Lietuvos Respublikos specialiųjų tyrimų tarnyba sulaikė Prekybos, pramonės ir amatų rūmų asociacijos vadovą Rimantą Šidlauską, kuris 2002-2008 metais ėjo Lietuvos ambasadoriaus Rusijos Federacijoje pareigas.

Šidlauskas kaltinamas kyšio prievartavimu iš Rinato Nasirovo, „Novyj promyšlenyj bank“ banko, iš kurio praeitais metais buvo atimta licencija, bendrasavininko.

Savo žodį Šidlauskas, pasirodė, išlaikė, nes kartu su Lietuvos diplomatijos tarnybos veteranu specialiųjų tyrimų tarnyba sulaikė Lietuvoje ir Nasirovą.

Korupcijos skandalo epicentre atsidūrė Lietuvos respublikos ambasada Maskvoje, ryšiai kurioje leido Prekybos, pramonės ir amatų rūmų vadovui užtikrinti Šengeno vizą neteisėtais veiksmais įtartam verslininkui, kuriuo jau seniai domisi Rusijos teisėsauga.

Lietuvos respublikos ambasadorius Rusijoje Remigijus Motuzas paskubėjo pranešti, kad nežino nieko apie vykdomą tyrimą o konsulato darbuotojams, kurie sprendžia vizų klausimus, daryti įtakos neįmanoma. Tačiau Lietuvos specialiosios tarnybos nusprendė kitaip.

Prokuratūra pranešė, kad ambasadoriui buvo suteiktas specialiojo liudytojo statusas. Toks statusas parodo, kad žmogus yra baudžiamosios bylos figūrantas, tačiau nėra tiek įrodymų, kad jų pakaktų pareikšti įtarimus dėl neteisėtų veiksmų.

Po atšaukimo iš Maskvos Remigijus Motuzas kelias dienas nebuvo pasiekiamas, o paskui pareiškė, kad atsistatydinti nesiruošia. „Atsistatydinimas būtų, kad aš pripažįstu, jog mes atlikome neteisėtą veiksmą. Aš esu tvirtai įsitikinęs, kad jokių įtarimų nėra ir jokių neteisėtų veiksmų nėra“, - pasakė Lietuvos Respublikos ambasados vadovas.

Šis skandalas dėl buvusių ir esamų diplomatinės tarnybos darbuotojų verslumo pasirodė labai žymus. Smūgį tarptautiniam Lietuvos imidžui teko pripažinti net šalies prezidentei. Grybauskaitė pasakė, kad Lietuvos diplomatas apklaustas kaip baudžiamosios bylos dėl kyšio vizos išdavimo metu liudytojas „meta šešėlį į diplomatinę tarnybą“.

Deja, Lietuvos Užsienio reikalų ministerijai tos gėdos neužteko, todėl jie nusprendė dar prisidaryti sau bėdų.

Jokio kito geresnio pasiteisinimo už pamiltą „Rusijos agresiją“ Užsienio reikalų ministerijoje sugalvoti nesugebėjo ir susiejo ambasadoriaus atšaukimą iš Maskvos su 1991 metų sausio 13-osios įvykių prie Vilniaus televizijos bokšto bylos nuosprendžiu.

„Ambasadorius atšaukiamas konsultacijoms dėl pažeidžiamumo, kuriuos lemia grasinimai, kurių sulaukė ambasada, ambasados darbuotojai ir ambasadorius po Sausio 13-osios bylos nuosprendžio“, - pranešė Lietuvos užsienio reikalų ministro Lino Linkevičiaus atstovė spaudai Rasa Jakilaitienė.

Jakilaitienė pranešė tai balandžio 11 dieną. Bet vos už vieną porą Motuzas pareiškė, kad atsisakyti savo pareigų nesiruošia. Reiškia, ambasadorius nori grįžti į Maskvą. Kaip gi tai įmanoma? Jam gi ten gresia didžiulis pavojus. Jis gi gauna grasinimų. Jis gi jau gali nebegrįžti iš Rusijos gyvas. Jis gi Rusijoje bus užmuštas ir išdarinėtas už tai, kad Lietuvoje 7 metams kalėjime buvo nuteistas pulkininkas Jurijus Melis...

Pono Linkevičiaus darbuotojai tiek metų atkakliai sudaro nepageidaujamų valdžiai rašytojų, mokslininkų, žurnalistų, dainininkų ir aktorių „juoduosius“ sąrašus, kurių vienintelis „nusikaltimas“ – Rusijos politikos rėmimas ir (o, Viešpatie!) Lietuvos politikos kritika.

Tuo pačiu metu už kyšį jie įleidžia į Europos Sąjungą nusikaltėlį.

Pagauti, šie žmonės vėl puola kaltinti „Rusijos agresiją“ ir kvailai tvirtina, jog ambasadorių iš Maskvos atšaukė dėl Jurijaus Melio. Jų žodžius tuo pačiu metu neigia Lietuvos prokuratūra, kuri teigia, kad ambasadorius buvo atšauktas apklausai dėl kyšio. Kitą dieną savo URM kolegų žodžius neigia jau pats ambasadorius.

Vargu ar lietuvių diplomatai kada nors supras, kodėl jie atsidūrė tokioje nemalonioje situacijoje. Jie taip daro savo darbą, o kitaip – nemoka.

Bet kokioje sau nemalonioje situacijoje – juo labiau minėkite „Rusijos grėsmę“.

Tad ir turim, kad „tai ne aš apsišūdinau, tai Putinas pridėjo man į kelnes“.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```
