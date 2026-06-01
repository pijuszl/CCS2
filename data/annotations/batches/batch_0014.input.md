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

### Article 1 — id: `scraped:rubaltic_lt:c506a210d1d7a0d5`

**Title:** Pragyvenimo pabrangimas ir gyventojų skurdas: kur atvedė Lietuvą finansinio suvereniteto atsisakymas

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuva — rinkos ekonomikos šalis, kurios aukštą statusą šiomis dienomis patvirtino narystė Ekonominio bendradarbiavimo ir vystymosi organizacijoje, pasiruošusi panaudoti nerinkos mechanizmus kovoje su infliacija. Praėjus trejiems metams po euro įvedimo šioje Pabaltijo respublikoje atsitiko tai, ką, perspėdami, prognozavo daugelis ekonomistų — kainos išaugo visuose ekonomikos sektoriuose.

Einamosios socialinės ir ekonominės situacijos Lietuvoje startu tapo 2015 metai, kai šalis įsivedė eurą. Ir padaryta tai buvo nesant plačios visuomenės paramos, juk lietuviams jau buvo žinomos neigiamos perėjimo prie europietiškos valiutos Latvijoje ir Estijoje pasekmės.

Pasak latvių leidinio Nra.1v, maisto produktų kainos Latvijoje (ji įsivedė eurą 2014 metų sausio 1d.) mažiau nei po pusmečio po euro įvedimo pašoko 20 proc. Savo ruožtu, SEB darbo su privačiais asmenimis skyriaus vadovas Trijn Mesimas pažymėjo, kad Estijoje po euro įvedimo kainos ūgtelėjo labiau nei Latvijoje.

Tuo metu paviešintas Eurobarometr tyrimas parodė: daugiau nei pusė Lietuvos gyventojų buvo įsitikinę, jog nacionalinės valiutos atsisakymas neigiamai paveiks pragyvenimo lygį. Galų gale, greta Lenkija, kuri sėkmingai vystosi ekonomiškai, išlaikydama savo finansinį suverenitetą. Ir šiaip valstybės — ES narės — nelabai skuba į eurozoną: iš 28 šalių tik 18 įsivedė eurą.

Ir išėjo taip, ko baiminosi Lietuvos Respublikos gyventojai. Kainų augimas matosi visose ekonomikos sferose. Profsąjungų „Solidarumas“ duomenimis, daugelio prekių kainos Lietuvoje jau pasiekė vidutines ES ir net viršijo vidutines ES rūbų, avalynės, buitinės technikos kainas 15 proc., o tuo metu vidutinis uždarbis Lietuvoje siekia tik 45 proc. Europos Sąjungos vidutinio uždarbio.

Tai patvirtina ir Lietuvos rinkos tyrimų, kuriuos atliko Teisės ministerija ir Valstybinė vartotojų teisių gynimo tarnyba, rezultatai: „daugelio prekių kainos respublikoje aukštesnės lyginant su kitomis Europos Sąjungos šalimis, pavyzdžiui, rūbai Lietuvoje brangesni 15 proc.“.

Savo ruožtu Šilumos tiekimo asociacija įspėjo, jog artimiausiu metu neišvengiamai 10 proc. kils šildymo kainos — jas įtakos biokuro sąnaudos (2015 metais biokuro dalis energijos gamyboje šilumos tiekimo sektoriuje sudarė 61 proc.).

Šiandien pagrindinius iššūkius šalies ekonomikai meta infliacija. Pavyzdžiui, SEB banko prezidento patarėjas, ekonomistas Gitanas Nausėda infliacijoe įžvelgia pagrindinę grėsmę valstybės stabilumui, matydamas tiesioginį šios problemos ryšį su didėjančiu žmonių, atsidūrusių už skurdo ribos, skaičiumi. Norint išspręsti šią problemą, jo manymu, reikia didinti BVP dalią, kuri turi būti perskirstoma per biudžetą socialinės politikos finansavimui, visų pirma remiant konkrečius menkai aprūpintus žmones. Viena iš tokių priemonių, jo manymu, yra pensijų indeksavimas atsižvelgiant į einamąjį infliacijos lygį. Iš esmės susidaro vaizdas, jog šiandien valdžios nežino, kaip kovoti su Lietuvos įstojimo į eurozoną pasekmėmis. Ir mato jos vien tik nerinkos priemones. Lietuvos valstiečių ir žaliųjų sąjungos lyderis Ramūnas Karbauskis „Žinių radijo“ eteryje pažadėjo susidoroti su kainų augimu, respublikos parduotuvėse apribojant prekybos centrų darbą poilsio dienomis. „Jei turėtume mechanizmus, kuriuos galėtumėm taikyti reguliuojant maisto produktų kainas, mes tikrai tai padarytumėm, bet ten šiek tiek kitaip: maisto produktų kainos taip nereguliuojamos, mes tuoj pat sulauktumėm Europos Sąjungos sankcijų“, — pareiškė „valstiečių“ lyderis.

O tuomet socialdemokratai, kurie 2015 metais buvo Lietuvoje valdžioje, euro įvedimo metais jau bandė pasinaudoti kainų reguliavimo mechanizmais pienininkystės šakoje. Tada iš vėžių išmušė Rusijos kontrsankcijos. Maisto embargas privertė Lietuvos parlamentą priimti naujas pienininkystės rinkos reguliavimo taisykles, kurios paliko supirkėjus be pieno žaliavos, o perdirbėjai prarado galimybę greitai keisti kainas. Jiems buvo uždrausta supirkimo kainas mažinti rečiau nei kartą per 30 dienų, o taip pat pareikalauta prieš 30 dienų perspėti ūkininkus apie pasikeitimus kontrakte arba apie jo nutraukimą. Ir tuo metu buvo įvesti pirkimų apimčių pakeitimų apribojimai (ne daugiau kaip 10 proc. kontraktuose numatytų apimčių). Žemės ūkio ir maisto produktų rinkos reguliavimo agentūra buvo įpareigota papildomai kontroliuoti kainas iki kiekvienos sutarties ekspertizės, jei pieno žaliavos kaina buvo pakeista daugiau nei 3 proc. mažėjimo pusėn.

Tai prieštarauja principams Ekonominio bendradarbiavimo ir vystymosi organizacijos, kurios įstatai teigia: EBVO yra tarptautinė išsivysčiusių šalių ekonominė organizacija, pripažįstanti atstovaujančios demokratijos ir laisvos rinkos ekonomikos principus.

Narystei EBVO prieštarauja ir naujausia statistika, pagal kurią kiekvienas penktas šalies gyventojas yra atsidūręs už skurdo ribos, o vidutinės metinės infliacijos rodiklis — didžiausias eurozonoje.

Beje, Lietuvos statistikos departamento duomenimis, 2017 metais apie 650 tūkstančių žmonių buvo pripažinti labiausiai socialiai pažeidžiami, o tai beveik ketvirtadalis šalies gyventojų. Savo ruožtu Eurostat pranešė, kad metinė infliacija 2018 metų biržely Lietuvoje siekė 2,6 proc., o tai pusantro karto viršija vidutinį ES rodiklį — 1,7 proc. Tokiais tempais eidama, šalis gali užbaigti metus kainoms ūgtelėjus 4 proc. (2017 metais — 3,7 proc.). Verta priminti, kad pagal Maastrichto kriterijus, įtvirtintus Europos Sąjungos sutartyje, šalies infliacijos dydis neturi viršyti 1,5 proc. trijų valstybių — ES narių, — pasiekusių geriausių rezultatų kainų stabilumo sferoje, vidutinio lygio. Pavyzdžiui, pagal 2017 metų rezultatus, žemiausi rodikliai buvo užfiksuoti Kipre (0,5 proc.), Airijoje (0,4 proc.) ir Portugalijoje (0,3 proc.), o tai duoda vidutiniškai pasvertą rodiklį — 0,4 proc.

Kaip socialinio ekonominio degradavimo fone paaiškinti Lietuvos Respublikos piliečiams, kad euras yra jų gerovės pamatas, neaišku. Ir čia jau nedirbs įkyrėję vietinio elito argumentai apie „apsuptą tvirtovę“ ir „priešpastatymą rusų grėsmei“, konsoliduojant elektoratą prieš 2019 metų prezidento rinkimus. Einamoji ekonomikos padėtis — tai dėsningas rezultatas dviejų kadencijų šalies prezidentės Dalios Grybauskaitės politikos, kurią aktyviai rėmė konservatoriai ir prisitaikėliai socialdemokratai.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 2 — id: `scraped:rubaltic_lt:172744957fd0cafb`

**Title:** Lietuva iki 2024 metų ruošiasi įveikti „rusų vamzdį“. RuBaltic.Ru apskaičiavo pergalės kainą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos valstybinė ekonominės infrastruktūros vystymosi komisija rugpjūčio 20 d. priėmė sprendimą nupirkti redujofikavimo laivą Independence, kuris nuo 2014 metų puošia Klaipėdos uosto prieplauką. O teisę jį nusipirkti Lietuva įgis tik 2024 metais, kai užsibaigs dešimties metų nuomos sutartis, pasirašyta su norvegų kompanija Hoeg LNG. Šalies premjeras Saulius Skvernelis pakomentavo šį sprendimą atitinkamos retorikos porcija, kuri turi pademonstruoti jo reikšmę — maksimaliai sumažinti energetinę priklausomybę, gyventojų išlaidas gamtinėms dujoms ir t.t.

Už šių žodžių, kurie turi nuraminti Lietuvos rinkėją, slypi rūsti realybė. Prisiminkime samatas dviejų projektų: SGD tiekimo ir redujofikacinių terminalų statybų — Lietuvos Independence ir lenkų terminalo Svinousce. Jie ir geografiškai artimi, nes abu funkcionuoja prie Baltijos jūros.

Independence metinės nuomos kaina sudaro 60 milijonų eurų, per 10 metų Lietuvos biudžetas praras 600 milijonų eurų, o dar reikia pridėti 60 milijonų eurų išlaidas dujotiekio Klaipėda–Kuršėnai statybai. Uosto prieplaukos sutvarkymas (laivą redujofikatorių SGD priėmimo metu neturi supti audros, priimtos dujos turi būti perduodamos į krantą ten viską paruošus, o tam reikalingos kompresorinės stotys) kainavo dar 200 milijonų eurų.

Lenkijos išlaidos, skirtos Svinousce, oficialiai nebuvo skelbtos, tačiau ekspertai teigia, jog tai maždaug 1,1–1,2 milijardo dolerių. Šių dviejų projektų samatos faktiškai panašios, tačiau Lenkija iš pat pradžių statė antžeminį terminalą kaip valstybės nuosavybę.

Svinousce projektas ekonomiškai labiau pasiteisinantis. Latvija ir po 10 metų bus redujofikacinio terminalo savininkė, o Lietuva, jeigu sukrapštys pinigų, šią teisę įgaus 2024 metais arba išplaukiančiam iš uosto Independence pamojuos skarele.

Suma, kurią teks pakloti perkant Independence, — komercinė paslaptis, tačiau Lietuvos žiniasklaida prognozuoja, jog tai bus 120–160 milijonų eurų. Palyginti yra su kuo. Pavyzdžiui, pastaraisiais metais visi dujas transportuojančių naujų laivų užsakymai keliauja į Pietų Korėją — tos šalies laivų statytojai lenkia savo konkurentus kainomis ir kokybe. Vidutinė naujo laivo kaina – apie 190 milijonų dolerių, tačiau tai šiaip plaukiojančios „kriogeninės SGD saugyklos“, jose nėra aparatūros redujofikavimui, nėra kompresorių, perpumpuojančių dujas į kranto infrastruktūrą.

Kiek gali kainuoti šie papildomi įrenginiai, galima suprasti vėlgi neatsisveikinus su Baltija — Kaliningrado srityje rusų „Gazpromas“ realizuoja redujofikavimo terminalo projektą būtent specializuoto laivo variantu.

Beje, nugalėtojais tapo tie patys pietų korėjiečiai, bet čia jau nieko napadarysi — rinka yra rinka. Rusija ne viena tokia, šiuo metu visos besivaržančios kompanijos, užsiimančios SGD, laksto pas Korėjos laivų statytojus.

Taigi, pradedant nuo nulio, pagal individualų projektą redujofikavimo laivas „Gazpromui“ kainuos 560 milijonų dolerių. Mažiausiai du kartus mažiau, negu išleido savo projektui Lietuva, o rezultatas — jos nuosavybe taps prieš 15 metų pastatytas laivas.

Susikivirčijusi su kaimynais — Latvija ir Estija, Lietuva iš paskutiniųjų jėgų, alindama biudžetą, priversdama vos ne bankrutuoti stambiausią respublikoje dujų vartotoją Achemą, — tempia ir tempia ne pagal savo jėgas naštą simboliniu pavadinimu Independence. Vietoj realaus energetinio saugumo lietuviai gavo pastoviai augančias elektros kainas, kurios priklauso nuo AE Švedijoje, HE Latvijoje ir jūrų kabelio darbingumo.

Net 2024 metais išperkamas Independence neduos momentalaus pelno. Lietuvai dar teks susirasti personalą, sugebantį užtikrinti redufikavimo įrenginių funkcionavimą. Beje, Lietuvos vadovybė turi teisę priimti bet kokius sprendimus, o diktuoti sąlygas gali tik šalies rinkėjas.

Unison su premjero komentaru byra ir Energetikos ministerijos komentarai. „Labai svarbu, kad būtų išlaikomas monopolisto spaudimas kainomis, nes jei mes atsisakysime terminalo ir jis nuplauks, kainos gali ūgtelti ir 20 proc.“ Ir tai taip pat bandymas užbėgti už akių rinkėjo reakcijai, bet, kaip ir premjero žodžiai, šis tekstas neturi jokio pagrindo. Dėl ko „Gazpromas“ kels kainas, kodėl būtent 20 proc., o ne, sakykim, 24 ar 16? Tai tur būt pirmas skaičius, kuris toptelėjo į galvą energetikos ministrui.

Ir vis dėlto naujame Lietuvos vyriausybės sprendime galima įžvelgti užuominą, jog politikai bando apčiuopti kaip pakeisti projektą, kad atsirastų nors menkiausia išeikvotų pinigų sugrįžimo į šalies biudžetą viltis. Gali būti, kad šį kartą Lietuvos politikai įsiklausė į savo pietinių kaimynų patarimus — tai galima išgirsti šiame Lietuvos energetikos ministro Žygimanto Vaičiūno komentare: „Lietuva išsaugos išėjimą į tarpautines SGD rinkas ir vienu kartu gaus didžiulį lankstumą ir galimybes ateityje greitai reaguoti į rinkos situacijos pokyčius“.

Pirmą kartą Lietuvos valdininko komentare nėra žodžių apie tai, kad Independence galima ir reikia panaudoti tik siekiant tiekti dujas Lietuvos vartotojams, pirmą kartą kalbama tik apie tarptautines SGD rinkas. Tai geras signalas — negalima atmesti, jog Lietuvos vadovai nutarė prisiminti, kad ekonomikos klausimus jie gali spręsti pragmatiškai, o ne vadovaujantis politinėmis ir ideologinėmis nuostatomis.

Tačiau siekiant „iššifruoti“ užuominą, slypinčią Vaičiūno žodžiuose, reikia tam skirti laiko, kad nors šiek tiek suvokti, kas tai yra tarptautinės SGD rinkos, kokie ten viešpatauja papročiai, kokios nustatytos žaidimo taisyklės. Ne, tuo tikslu nereikės gilintis į biržų reikalus, kylančius ir smunkančius trendus — tai šia tema galvosūkius sprendžiančių profesionalų užsiėmimas. Pakaks išsiaiškinti, kodėl Vaičiūnas naudojasi daugiskaita. Pažvelkite įdėmiai — jis kalba apie kelias, o ne apie vieną tarptautinę rinką.

Įvairiuose planetos regionuose jų kaina nustatoma pagal skirtingas taisykles, įvairūs SGD gamintojai skirtingai jas parduoda — kontraktai, kuriuos siūlo klientams norvegų Statoil, visiškai ne tokie, kaip Oatargas kontraktai, o SGD, pagamintos JAV teritorijoje, parduodamos išvis pagal „trečiąsias“ taisykles. Gamtinės dujos — labai neįprasta prekė, ir tuo įdomiau bus Lietuvos valdžioms susipažinti su jų tarptautinėmis rinkomis.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 3 — id: `scraped:rubaltic_lt:cf1c7fb5892d0f81`

**Title:** Lietuvoje kerštas žydams, „miško brolių“ aukų palikuoniams

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Šiauliuose išniekintos žydų kapinės. Žydų organizacijų aktyvistai įtaria, jog tai vandalizmo aktas — kerštas Lietuvos žydų bendrijai už kovą prieš heroizavimą kolaboranto Jono Noreikos, kuris kaip tik Šiaulių apylinkėse vykdė masiškas žydų žudynes. Amerikos žydui Grantui Gorinui, daugelį metų pasisakančiam prieš Noreiką ir kitus „miško brolius“, Lietuvoje buvo pagrasinta baudžiamosios bylos iškėlimu. Lietuvos vadovybė peržengia visas „raudonas linijas“ ir provokuoja tarptautinį skandalą, kuris gali sukelti konfliktą tarp Vilniaus ir Izraelio su JAV.

„Litvakų (Lietuvos žydų) bendruomenei, pažyminčiai, kaip ir „Sąjūdis“ (įkūrimo), savo atkūrimo 30-metį, o taip pat Vilniaus geto likvidavimo 75-metį, kelia nerimą vis dar nesibaigiančios visuomenėje diskusijos dėl Jono Noreikos („generolo Vėtros“) atminimo įamžinimo. Tie duomenys, kuriais mes disponuojame, liudija, kad Jonas Noreika tiesiogiai ir netiesiogiai dalyvavo įgyvendinant Lietuvoje Cholokausto politiką“, — sakoma atvirame žydų bendruomenės laiške.

Žydų bendruomenė pateikia dokumentalius įrodymus, kad kolaborantas Noreika tiesiogiai dalyvavo žydų genocide, pareiškia, jog Lietuvos kultūros valdininkai gina ir teisina „miško brolius“, ir reikalauja nuimti atmintiną lentą „generolui Vėtrai“ nuo Lietuvos mokslų akademijos bibliotekos iki rugsėjo 23-iosios — Lietuvos žydų genocido aukų atminimo dienos.

„Mes manome, jog Lietuvos visuomenė, mininti valstybingumo šimtmetį, pakankamai subrendusi, todėl pajėgi įvertinti istorinius faktus, o valstybė — prisiimti atsakomybę už viešai demonstruotą nepagarbą istoriniam teisingumui“, — sako Lietuvos žydai, reikalaujantys, kad valdžios pripažintų tą faktą, jog Lietuvos nacionalistai dalinai atsakingi už žydų genocidą Lietuvos teritorijoje.

Vykdant žemės darbus ir klojant vamzdžius, buvo išrausti žydų kapai ir žmonių palaikai išmesti ant paviršiaus. Kapinės — kultūros paveldo objektas, ten jokie vamzdžiai negali būti klojami — žemės darbai tokioje teritorijoje draudžiami. Todėl tame, kas atsitiko Šiauliuose, Lietuvos žydai įžvelgia ne nesusipratimą, o sąmoningą vandalizmo aktą.

„Tie kaulai gali būti mano giminių. Nepagarba... Tai panašu į smūgį širdin peiliu, kaip kažin kas gali taip smarkiai nekęsti? Kaip žmonės gali būti tokie beširdžiai? Tose krūvose gali būti mano šeima“, — taip kapinių Šiauliuose išniekinimą įvertino Lietuvos žydų palikuonis, JAV pilietis Grantas Gočinas.

Lietuvos valdžių santykiai su Gočinu ypatingi. Kalifornijos gyventojas daug metų demaskuoja Hitlerio talkininkus Pabaltijyje ir kritikuoje Lietuvos, Latvijos bei Estijos istorinę politiką.

Ypatingą vietą jo veikloje užima kova priš tai, jog „generolas Vėtra“ paverčiamas Lietuvos nacionaliniu didvyriu.

Tiesioginiu falsifikacijos organizatoriumi Gošinas įvardina Lietuvos genocido ir rezistencijos tyrimų centrą, vadovaujamą Teresės Birutės Barauskaitės. Be to, iš esmės nusikalstamą Centro veiklą heroizuojant Cholokausto organizatorių, toleruoja Saugumo departamentas ir asmeniškai Lietuvos prezidentė Dalia Grybauskaitė.

Grantas Gočinas pasiuntė Birutės Barauskaitės vadovaujamai įstaigai užklausimą apie Lietuvos valstybės požiūrį į Jono Noreikos veiklą. Prie užklausimo — 69 puslapiai dokumentų, įrodančių „miško brolių“ nusikaltimus. Tarp jų — raštiški Noreikos anūkės, lietuvių bendruomenės Čikagoje amerikiečių žurnalistės Silvijos Foti parodymai; ji dabar rašo knygą apie savo senelį. Be to, Amerikos žydas pateikė skundą Birutės Barauskaitės adresu, kaltindamas ją tuo, kad jos vadovaujama kontora sąmoningai neigia Cholokaustą.

„Jeigu aš, demaskuodamas genocidą vykdžiusį monstrą, įvykdžiau nusikaltimą, lai man bus iki mano gyvenimo pabaigos pasididžiavimo ženklas. Lai tai bus mano gyvenimiško palikimo dalis. Jei Lietuva genocido monstro demaskavimą laiko nusikaltimu, lai jai taps papildoma gėda visiems laikams“, — taip komentavo Lietuvos valdininko grasinimus Grantas Gočinas.

Kitaminčių, išdrįsusių sklaidyti „didvyriškų miško brolių“ mitą, gąsdinimo vaizdą puikiai papildo besitęsiantis persekiojimas dviejų kitų „eretikų“: Klaipėdos savivaldybės deputato Viačeslavo Titovo ir rašytojos Rūtos Vanagaitės. Šie asmenys išdrįso pakelti balsą prieš kitą „miško brolį“ — Adolfą Ramanauską–Vanagą.

Panevėžio dramos teatras (jame visą savo kūrybinį gyvenimą praleido didysis Donatas Banionis) paskelbė, jog pagal Rūtos Vanagaitės knygą „Mūsiškiai“ pastatys spektaklį. Knyga, priminsim, skirta masiškam lietuvių dalyvavimui Cholokauste.

Atsakant į tai pasireiškė visuomeninis judėjimas „AntiTitovas“. Atstovaujanti jam kažkokia Antonina L. Iš Butingės paskelbė, jog ruošiama akcija prieš teatrą, nutarusį inscenizuoti „Rusijos propagandistės Vanagaitės“ knygą.

Pavadinti Rūtą Vanagaitę „Rusijos propagandiste“ — tai, žinoma, aukščiausias visuomenės aktyvistų neadekvatumo ir marginalumo rodiklis. Tačiau lietuviškiesiems disidentams tokie neadekvatai ir marginalai gali tapti pavojingesni nei administracinis presingas. Jie gali sumanyti padegti Panevėžio dramos teatrą spektaklio pagal Vanagaitės knygą premjeros dieną.

Mesti Amerikos piliečiui, kovojančiam už tiesos apie Cholokaustą išsaugojimą, užuominas apie baudžiamąjį persekiojimą — įrodymas, jog už mitą apie „miško brolius“ Lietuvos valdžia pasiruošusi kautis iki paskutiniųjų. Tu gali būti JAV pilietis, net Donaldas Trampas, o į mūsų istorinę politiką nedrįsk brautis! Joks Grantas Gočinas, Jefraimas Zurofas, Džaredas Kušneras arba Binjaminas Netanjachu nepajėgs suabejoti šviesiu mūsų didvyrių įvaizdžiu.

2012 metais Lietuvos Respublikos valdžios galėjo sau leisti su karinėmis apeigomis garbingai perlaidoti „Lietuvos aktyvistų fronto“ lyderį ir Laikinosios Lietuvos vyriausybės premjerą, numodama ranka į protestus Izraelio, pasipiktinusio žydų pogromo Kaune organizatoriaus heroizavimu. Barako Obamos administracijai ne itin rūpėjo Izraelis ir žydai, todėl Vilnius ir galėjo į juos numoti ranka.

Šiandien toks Lietuvos valdžių fokusas nepraeis. Donaldas Trampas — Barako Obamos antipodas visais klausimais, tame tarpe ir remiant Izraelį. Žydų įtaka Baltiesiems rūmams šiandien didžiulė, Cholokausto atminimo gynimas — neliečiama Vašingtono užsienio politikos vertybė, o Izraelis — pagrindinis Amerikos sąjungininkas, užtikrinant kurio saugumą Trampas deda tokias pastangas, apie kurias Lietuva negali net svajoti.

Taip kad sumokės Lietuva už Antrojo pasaulinio karo istorijos perrašinėjimą ne tik Lietuvos–Rusijos (tai galima tik sveikinti) ir Lietuvos–Izraelio (su tuo galima susitaikyti), bet ir Lietuvos–Amerikos konfliktu.

Ir štai šio konflikto Lietuvos valdžia, ketvirtį amžiaus žvelgianti į Vašingtoną iš apačios į viršų pozoje „ko pageidaujate?“, tikrai neištvers.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 4 — id: `scraped:rubaltic_lt:029a7363da242cd0`

**Title:** Juos būtų nužudę tikraisiais Lietuvos didvyriais tapę „miško broliai“

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Oriolo srityje paminėtas Raudonosios Armijos 16-osios Lietuviškosios divizijos karių atminimas. Oficialūs Lietuvos Respublikos atstovai atmintinėje ceremonijoje nedalyvavo: pačioje Lietuvoje tuo metu buvo kaunamasi prieš didvyriško „miško brolio“ įvaizdžio desakralizavimą. Taikius gyventojus žudę banditai Lietuvos valdžioms svarbesni nei antihitlerinės koalicijos kovotojai, kurie 1944 metais išvadavo Lietuvą nuo nacių. Ir tai ne vienkartinis atvejis: RuBaltic.Ru prisiminė tikruosius didvyrius, kuriuos Lietuvos vadovai stengiasi nepastebėti ir kuriuos „miško broliai“ būtų nužudę kaip klasės priešus.

Raudonarmiečiai

Antrojo pasaulinio karo metu antihitlerinės koalicijos pusėje kovojo keli tūkstančiai lietuvių. 1941 metų gruodžio mėnesį iš lietuvių kareivių ir karininkų buvo suformuota 16-oji šaulių Lietuviškoji divizija — vėliau ji buvo apdovanota Raudonosios vėliavos ordinu ir pelnė garbingą Klaipėdos vardą. 1943 metų pradžioje diviziją sudarė dešimt tūkstančių žmonių, absoliuti dauguma buvo lietuviai. Įsakymai ir komandos iš pradžių buvo skelbiami lietuviškai.

Dvylika Lietuviškosios divizijos kareivių ir karininkų pelnė Tarybų Sąjungos Didvyrio vardą. Tarp jų — pirmasis lietuvis, pelnęs šį vardą, leitenantas Vaclovas Bernotėnas (vėliau nusipelnęs Lietuvos TSR kultūros ir švietimo veikėjas), žydų kilmės lietuvis majoras Volfas Vilenskis, Lietuvos lenkas vyresnysis seržantas Boleslovas Gegžnas, memuarų apie karą autorius jefreitorius Grigorijus Užpolis, vienas kovos metu sunaikinęs dvidešimt priešo kariškių jefreitorius Kalmanas Šuras, gyvybės kaina vokiečių tankų puolimo metu apgynęs perkėlą jaunesnysis seržantas Stasys Šeinauskas ir kiti didvyriai.

Raudonieji partizanai

Didžiausio antifašistinio pasipriešinimo metu okupuotoje Lietuvos teritorijoje veikė 67 tarybinių partizanų būriai ir grupės.

Raudonieji partizanai užsiiminėjo žvalgyba, organizuodavo diversijas, užpuldinėjo ginkluotus priešo dalinius. Jie padėjo Raudonąjai Armijai vaduoti Lietuvą — vienuolika Lietuvos partizanų būrių, susijungusių į Vilniaus ir Trakų grupes, dalyvavo vaduojant Vilnių.

Tarybinius valstybinius apdovanojimus pelnė 1800 partizanų ir pogrindininkų, veikusių Lietuvos teritorijoje. Septyniems Lietuvos partizanams suteiktas Tarybų Sąjungos Didvyrio vardas. Visi jie buvo lietuviai.

Beje, ši dukra linkusi neprisiminti tėvo ir jo kovų draugų, nes užsiėmė heroizavimu tų, prieš kuriuos rizikuodamas gyvybe kovėsi Polikarpas Grybauskas.

Trečiafrontininkai

„Trečias frontas“ — tai literatūrinis rašytojų, poetų ir publicistų susivienijimas, Antano Smetonos diktatūros metais leidęs tokio pavadinimo žurnalą. Šio „fronto“ nariais buvo Lietuvos rašytojai ir poetai Antanas Venclova, Petras Cvirka ir Salomėja Nėris.

Pavyzdžiui, poetė Salomėja Nėris trečiojo dešimtmečio metais buvo Paryžiuje Kominterno ir Lietuvos su Lenkija Komunistų partijų ryšininkė, o Kauno universitete vadovavo pogrindinei komjaunimo organizacijai.

Nėries mokinys ir literatūrinis perėmėjas Eduardas Mieželaitis nuo 15 metų buvo pogrindinės komjaunimo organizacijos narys: mokydamasis Vilniaus universiteto teisės fakultete, dirbo vyriausiuoju lietuviškosios „Komjaunimo tiesos“ redaktorium. „Lietuviškąjį Če Gevarą“ ir „lietuviškąjį Garsija Lorką“ — 27 metų poetą Vytautą Montvilą Smetona įkišo į katorgą už polinkį komunizmui, o pirmosiomis Lietuvos nacių okupacijos dienomis jis, 38 metų, buvo sušaudytas už antifašistinius eilėraščius.

Steponas Darius

Lietuvos ir Amerikos karo lakūnas, sportininkas, Olimpinių žaidynių dalyvis. Būdamas vaikas pateko į JAV, vėliau kaip JAV kariuomenės savanoris dalyvavo Pirmajame pasauliniame kare. Po karo grįžo į Lietuvą, dalyvavo kovose už Lietuvos Respublikos nepriklausomybę.

Lakūnų žygdarbis pavertė juos didvyriais ne tik Lietuvos, bet ir už jos ribų. Eilėraštį apie Dariaus ir Girėno žūtį parašė į Prancūziją emigravęs didysis rusų poetas Konstantinas Balmontas.

Tarybų Sąjungoje Lietuvos kino studijoje 1983 metais buvo sukurtas filmas apie Lituanicos skrydį — „Skrydis per Atlantą“.

Lietuvos krepšininkai

Po Antrojo pasaulinio karo atrodė, kad dar neseniai Lietuvoje klestėjęs nacionalinis sportas mirė — žymūs Lietuvos krepšininkai bėgo nuo karo už vandenyno. Tačiau jau 1944 metais buvo sukurtas legendinis krepšinio klubas „Žalgiris“, kuris penkis kartus tapo TSRS čempionu. O 1947 metais suformuotoje pirmoje TSRS krepšinio rinktinėje žaidė keturi lietuviai. Tais pačiais metais rinktinė pirmą kartą tapo eurokrepšinio nugalėtoja ir nuo to laiko reguliariai laimėdavo pasaulio bei Europos čempionatuose ir Olimpinėse žaidynėse.

Žvelgiant iš šių dienų Lietuvos ideologijos pozicijų, čia slypi sudėtingas moralės klausimas: ar buvo tikrais lietuviais ir Lietuvos patriotais įžymūs krepšininkai Modestas Paulauskas ir Arvydas Sabonis, jeigu jie žaidė „okupantų“ rinktinės sudėtyje, stovėjo po „okupantų“ vėliava ir po pergalės giedojo „okupantų“ himną?

Beje, ši ideologija tokia sąlygina ir supuvusi, kad Lietuvoje panašius klausimus stengiamasi nutylėti.

Todėl apie pasaulio, Europos ir Olimpinių žaidynių čempioną, TSRS rinktinės dalyvį Arvydą Sabonį „tautos tėvo“ sūnus Landsbergis jaunesnysis nieko nepaisydamas sukūrė filmą „Sabas“.

O štai kino režisieriaus Landsbergio senelį ir tėtušį, prezidentę Dalią Grybauskaitę ir jos tėvą — raudonąjį partizaną, o taip pat visus Lietuvos tarybinių laikų krepšininkus „miško broliai“ būtų sušaudę kaip kolaborantus, kurie išdavė lietuvių tautą ir bendradarbiavo su „okupaciniu režimu“.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 5 — id: `scraped:rubaltic_lt:ef73f9979a489722`

**Title:** Lietuvos valdžios užmiršo, kas yra demokratija

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Neteisminis politinės partijos „Lietuvos rusų sąjunga“ Klaipėdos skyriaus pirmininko, vietos savivaldybės tarybos nario Viačeslavo Titovo persekiojimas akivaizdžiai demonstruoja, jog Lietuvos valdžios atvirai ignoruoja demokratinius institutus ir procedūras. Tas, kuris suabejojo valstybės ideologija ir politika, vietinius nacistų talkininkus paverčiant tautos didvyriais, turi būti sunaikintas be tyrimo ir teismo.

Ko galima tikėtis iš valstybės, kurią ES pastoviai kritikuoja už žmogaus teisių pažeidimą, žiniasklaidos ir politinių oponentų persekiojimą? Tik tolimesnių kovų su kitaminčiais griežtinimo, ypač jei jie ne šiaip sau paviešina alternatyvią nuomonę, bet dar ir paremia ją plačia įrodymų baze. Išsisaugojimo instinktas ir istorinės atsakomybės baimė verčia Lietuvos valdžias imtis kraštutinių priemonių, užmirštant demokratines procedūras.

Ryškus pavyzdys — Lietuvos premjero Sauliaus Skvernelio pareiškimas. Duodamas interviu „Žinių radijo“ stočiai, jis pasakė, jog deputatas Titovas, kuris „melagingai apkaltino partizanų lyderį Adolfą Ramanauską-Vanagą nekaltų civilių žmonių žudymu“, nusipelnė apkaltos. Tokiu būdu, antrasis valstybės asmuo, nepaisydamas pagrindinio teisminio principo — nekaltumo prezumpcijos, grubiai pažeidė universalų valdžių pasiskirstymo principą.

Skverneliui, buvusiam kelių policijos inspektoriui, kuris šiandien reiškia savo prezidentines ambicijas artėjančių 2019 metais rinkimų proga, prieš skelbiant tokius viešuosius pareiškimus vertėtų prisiminti, jog pagal tarptautinę praktiką valstybės valdžios turi turėti vieną nuo kitos nepriklausančias šakas: įstatymdavystės, vykdomąją ir teisminę.

Norint juridiškai pasitobulinti, premjerui reikėtų susipažinti su istorine JAV patirtimi — ten valdžių pasiskirstymo principas palaipsniui buvo įvestas į 1797 metų JAV Konstituciją. Tada Amerikos tėvai kūrėjai sukūrė ištisą „sulaikymų ir atsvarų sistemą“, kurios rėmuose teisminė valdžia sugebėjo tapti tokia, kokia yra šiandien, — nepriklausoma.

Kokiu pagrindu Skvernelis daro išvadą, jog Titovas kaltas, kai išvadą po visapusiško ir objektyvaus pateiktų įrodymų tyrimo turi padaryti teismas? Šiuo atveju akivaizdžiai matomas visiškas premjero juridinis neraštingumas arba absoliutus įsitikinimas, jog teisminė sistema, kuri sergėja valstybės interesus ir neleis įsiplieksti jokiems precedentams, neklysta.

Klaipėdos deputato teisminis procesas atsidurs dėmesio centre ne tik Lietuvos susiskaldžiusios visuomenės, bet ir tarptautinės dėmesio centre. Akivaizdu, jog Titovo byla atsirado dėl atkaklaus Lietuvos valdžių ignoravimo visuomenėje egzistuojančios gilios prarajos tarp tų, kuriems nepriimtina valstybės ideologija heroizuojant nacių kolaborantus, ir tų, kurie pateisina savo tautiečius, ideologiniais sumetimais žudžiusius taikius lietuvius.

Savo ruožtu tarptautinės struktūros, besispecializuojančios Cholokaustu ir hitleriniu koloboravimu, taip pat įdėmiai stebės šio tyrimo eigą. Tokių pasauliniu mastu pripažintų organizacijų, kaip „Jad va-Šem“ ir Simono Vizentalio Centras, ekspertų parodymai teisme suteiktų šiam procesui didesnį svorį ir pasitikėjimą.

Su žmonėmis buvo aiškinamasi vengiant viešumo, kaip, pavyzdžiui, su vienu iš Vilniaus merijos vadovų Dariumi Udriu, patalpinusiu Facebooke „nepatogią“ informaciją. Valdininkas po Ramanausko-Vanago pavaldinių nuotrauka paliko socialiniame tinkle komentarą apie tai, jog jie ragino susidoroti su Lietuvos kolūkių pirmininkais ir tarybų valdžios atstovais.

„Pagal kokius kriterijus kokūkių kūrimą sulygino su nusikaltimu prieš žmoniškumą, už kurį etinės normos leidžia grąsinti mirtimi? Nejaugi todėl, kad tikslas pateisina priemones? Žudyti arba grąsinti mirtimi kolūkių kūrėjams — tai moralus poelgis? Pagal kokias etines normas?“ — klausė Udrys.

Valdininkas, žinoma, jokių atsakymų nesulaukė. Jį konservatoriai apkaltino „žeminant kovotojus už Lietuvos laisvę ir platinant tendencingas Lietuvos valstybingumo reikšmės interpretacijas savo pasisakymuose viešosiose erdvėse“. Pasekmės: atleistas iš valstybinės tarnybos pagal straipsnį „neatitikimas einamosioms pareigoms“.

Todėl šiandien Lietuvoje atsirado realus šansas iškelti šią problemą viešam aptarimui dalyvaujant tarptautinei visuomenei. Net jei vietiniai teismai, nieko nepaisydami ir pataikaudami politinei konjunktūrai, priims sprendimus, jie tuo pačiu atvers kelią į Europos žmogaus teisių teismą. Ir tada Lietuva susidurs su rimta rizika.

O kol kas Lietuvoje pats deputatas patiria didžiulį spaudimą. Valstybės kontroliuojama žiniasklaida veda prieš jį pastovią informacinę kampaniją. O struktūros savo ruožtu naudoja akivaizdaus gąsdinimo ir šantažo taktiką — krata namuose, darbovietėje ir mašinoje, namų orgtechnikos, elektroninių našiklių ir t.t. paėmimas. Titovą stengiamasi psichologiškai palaužti ir priversti atsisakyti savo teisminių planų.

Tai klasikinės policinės valstybės veiklos pavyzdys. O juk po neseniai įvykusio politiko užpuolimo, siekiant išvengti rimtesnių provokacijų, jam reikėtų skirti apsaugą.

Lietuvos valdžios savo veiksmais tik dar labiau kursto neapykantą ir ksenofobiją, demonstruoja akivaizdų demokratinių institutų nepaisymą, ką jau patyrė žinoma Lietuvos rašytoja Rūta Vanagaitė, besispecializuojanti Cholokaustu ir vietinių nacių talkininkų kolaboravimu. Ji taip pat buvo atsidūrusi prokuratūros taikinyje dėl Ramanausko-Vanago apšmeižimo. Pagaliau po griežtos tarptautinės reakcijos Lietuvos teisėtvarkos organai atsisakė kelti baudžiamąją bylą, „nesant nusikaltimo požymių“.

Viačeslavui Titovui taip pat teks susidurti su šiomis represijų girnomis, bet kas žino, gal, skirtingai nuo Rūtos Vanagaitės, savo teisminiu procesu jam pavyks atkreipti tikrų demokratinių šalių dėmesį į temą, kurią pastaraisiais dešimtmečiais Lietuvoje pastoviai buvo draudžiama liesti. Ir visiškai suprantama, kodėl.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 6 — id: `scraped:rubaltic_lt:356db172c1dc85bb`

**Title:** Adolfas Ramanauskas — „vanagas“ ar „maitvanagis“? RuBaltic.Ru istorinis neraštingumo likvidavimas

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Vieno iš pokario antitarybinio pasipriešinimo Lietuvoje lyderių Adolfo Ramanausko įvaizdis gali pasirodyti kaip patrauklus: išeivis iš socialinių apačių, pedagogas, talentingas organizatorius... Tačiau jau ne pirmą kartą Vanagas kaltinamas karo nusikaltimais. Naują skandalą išprovokavo Klaipėdos deputatas Viačeslavas Titovas, pasiryžęs įrodyti, kad Ramanauskas nevertas tautos didvyrio vardo. Kas iš tiesų buvo „miško brolių“ vadovas, kodėl jo kultas suklestėjo dabartinėje Lietuvoje ir kokiuose šaltiniuose galima atrasti tiesą apie jo veiklą? Į šiuos ir kitus klausimus rubrikos „Istorinis neraštingumo likvidavimas“ rėmuose atsako fondo „Istorinė atmintis“ tyrimų programų vadovas Vladimiras Simindėjus.

— Pone Simindėjau, 2018-ieji metai Lietuvoje paskelbti „miško brolio“ Adolfo Ramanausko metais, o visai neseniai dėl jo įsiplieskė eilinis didelis skandalas. Nejaugi tai tokia ryški asmenybė?

— Aš nesidomėjau atskirai Ramanausko biografija, tačiau, kiek galiu spręsti, jo sureikšminimas smarkiai išpūstas. Jo karjera, jeigu galima taip išsireikšti, klostėsi jau pokario metais. Būdamas Lietuvos karinių nacionalistinių formuočių dalyviu, jis palaipsniui užėmė jose gana reikšmingas pozicijas ir „miško“ epopėjos pabaigoje tapo vienu iš šio judėjimo vadovų. Tiesa, tuo metu minėtasis judėjimas gan liūdnai atrodė: dalyvių moraliniu stoviu ir jų koviniu pajėgumu.

Tačiau jis pasižymėjo valingais bruožais, agitatoriaus gabumais. Jis iki paskutiniųjų bandė organizuoti „brolius“ ir iš esmės buvo pasirinkto kovos kelio fanatikas. Ramanauskas iki paskutiniųjų nedegradavo, kuo ir skyrėsi nuo vidutinio statistinio „nacionalinio partizano“.

Mes turime atkreipti dėmesį į keletą svarbių momentų. Pirma, dabartinėje Lietuvoje Ramanauskas paverčiamas kulto figūra, tačiau tai daroma gana grubiai. Pavyzdžiui, atgaline data jam suteikiamas brigados generolo laipsnis. Tačiau egzistuoja tarptautinė pomirtinio apdovanojimo ir tam tikrų vardų suteikimo praktika.

O šio žmogaus kultas kuriamas perkeliant jo mitologines savybes į dabartinę lietuviškąją realybę: esą jis kaunasi kartu su visais. Tai ne nekalti dalykai, nes mes matome, su kokiu įsiutimu Ramanausko kulto agentai jį gina nuo tų, kurie abejoja, ar verta ir teisinga įamžinti jo atminimą — atminimą žmogaus, kurio karinės formuotės dalyvavo žudant daugybę lietuvių, priėmusių tarybų valdžią.

Egzistuoja gana didelė nacionalistinio teroro aukų bazė, šiuo klausimu užsiiminėjo tame tarpe ir fondas „Istorinė atmintis“. Lyginant šiuos duomenis su Ramanausko–Vanago formuočių aktyvumo rajonais Pietų Lietuvoje galima aptikti gana liūdną ir dokumentuose atspindėtą įvykių vaizdą: sužinoti, kas žuvo nuo „miško brolių“ kulkų, kur tai vyko.

Daug įdomių dalykų šia prasme yra kasdienėse tam tikrų tarybinių organų suvestinėse, kurios dalinai paviešintos. Jos yra ir Rusijos, ir Lietuvos archyvuose.

Ryšium su tuo bandymai įžūliai persekioti Klaipėdos deputatą, kuris atvirai pasisakė prieš Ramanausko heroizavimą, ir įvairių lietuvių visuomenės sluoksnių reakcija į šią situaciją vaizdžiai charakterizuoja jos politinę ir psichologinę būseną.

Kurstant pseudokarines aistras, esą Lietuva ne šiandien — rytoj vėl kariaus, ir labiausiai psichiškai „judrūs“ veikėjai tobulina savo įgūdžius, išvykdami į Ukrainą pašaudyti. Žinoma, duok jiems laisvę ir ypač nebaudžiamumo iliuziją — ir gali atsitikti tai, kas 1941 metais atsitiko su bejėgiais žydais. Tik dabar aukomis taps ne žydai, o žmonės, kurie dabartinėje Lietuvoje demonizuojami. Žinoma, kalba eina apie rusus.

— Viačeslavo Titovo situacijoje iš esmės viskas paremta šaltiniais. Titovas sako, kad yra konkretūs dokumentai, įrodantys Ramanausko kaltę, tame tarpe ir tarybinio teismo nuosprendis. O jo oponentai tvirtina, kad tuo negalima tikėti, VSK (KGB) tiesiog apšmeižė šlovingus kovotojus už Lietuvos nepriklausomybę.

— Čia reikia atskirti išties tikinčius viskuo „šventai lietuvišku“ nuo tų, kurie pajėgūs racionaliai mąstyti. Paliekant pastaruosius diskusijos rėmuose, nevalia užmiršti, kad yra labai rimtų darbų ir ta tyrimų tema, kaip reikia priimti ir kritikuoti tarybinius šaltinius.Tai ištisa kryptis istorijos moksle — darbas su šaltiniais. Pasinaudojant patikrintais mokslo metodais, galima išsamiai ištirti tarybinius (ir kitus) dokumentus, sulyginti juos ir bandyti priartėti prie tiesos. Čia paprasčiausiai reikalinga mokslinė sąžinė ir noras tuo užsiimti.

Pirma, aš jau minėjau kasdienes pažymas — ten nėra jokio pagrindo įžvelgti falsifikacijas prieš patį Ramanauską, tai paprasti eiliniai dokumentai. Antra, reikalinga trofėjinių medžiagų analizė. Archyvuose tikriausiai yra ne tik nelaisvėn paimtų smogikų parodymų, bet ir kartu su jais paimtų dokumentų, propagandinių lapelių ir t.t. Visa tai būtina tirti nešališkai.

Todėl su tais, kurie pajėgūs racionaliai mąstyti, dialogas galimas — žinoma, jeigu jie nepatiria galingo politinio spaudimo. O Lietuvoje, kaip matome, taip ir vyksta. Tiems istorikams, kuriems kelia abejones vienos ar kitos politinės ir istorinės dogmos, stengiamasi primesti visokių nemalonumų. Pavyzdžiui, jų neįsileidžia į Lietuvą, jei tai užsienio istorikai.

Deputatą Titovą gali ne tik miltais apipilti, bet ir sumušti, sukelti automobilio avariją, atimti mandatą (Lietuvos prokuratūra jau ieško tam pagrindo). Mes matome, kaip toli pažengė situacija šalyje.

— Bandykime šaltinių klausime daryti išvadas: jeigu atsispirti nuo šaltinių tyrimo klausimo ir kritiškai pažvelgti į tarybinius dokumentus, mes vis dėlto prieiname išvados, kad Ramanauskas, švelniai tariant, visiškai ne nenuodėmingas?

— Pasikartosiu, dokumentai, apie kuriuos eina kalba (tos pačios kasdienės chronikos), visiškai nenukreipti prieš Ramanauską. Dar ne faktas, kad tarybų valdžios struktūros žinojo jo vaidmenį vienoje ar kitoje akcijoje. Tačiau jau atgaline data, atsižvelgiant į lietuviškas publikacijas ir Ramanausko paliktus memuarus, galima kai ką palyginti. Ir tada išryškėja vaizdas, nepanašus į tą, kuris kuriamas dabartinėje Lietuvoje.

Dar vienas momentas: Lietuvos istoriniai tyrimai gana kukliai pateikia vokiečių okupacijos laikotarpį. Nurodoma, kad Ramanauskas mokytojavo. Ar iš tikrųjų taip buvo? Ką jis veikė trumpo Tarybų Lietuvos 1940–1941 m. laikotarpio metu? Čia taip pat iškyla įvairių klausimų. Žinoma, ramesnėmis sąlygomis istorikams būtų įdomu aiškintis.

— Titovas kaip tik ir pažymėjo, jog nori pradėti diskusiją. Ir jis greičiausiai teisus: tokia diskusija reikalinga. Juk ir Jūs patvirtinote, kad apie Ramanauską žinoma toli gražu ne viskas. Ar pavyks Titovui sudominti šia tema ekspertų bendriją? O gal jį parems Rusijos istorikai?

— Ramanauskas dabartinėje Lietuvoje išaukštinamas, ši figūra tapo vos ne pagrindinė. Tačiau tas laikotarpis, kai Lietuvos gyventojai buvo labiausiai terorizuojami, vis dėlto siejamas su tais metais, kai Ramanauskas dar nebuvo laikomas „miško brolių“ vadu. Tai ankstesni metai.

Kažkokia prasme einamieji Rusijos istorikų tyrimai gali paliesti šią temą. Tyrimai tęsiasi, ruošiamos įdomios publikacijos, tačiau ne visos palies Ramanauską arba tas teritorijas, kuriose jis veikė. Tai nėra pagrindinė tema. Ten yra ir ryškesnių personažų, kurie laukia savo tyrinėtojo.

— Gal būtent todėl ir tapo Ramanausko figūra pagrindine?

— Ji išpūsta!

— Ar ne todėl išpūsta, kad Ramanauskas — palyginant „saugus“ variantas? Ne toks baisus nusikaltėlis, kaip, pavyzdžiui, Jonas Noreika?

— Taip, ne toks baisus. Prasidėjus karui jis buvo gana jaunas. Tačiau mes turime suprasti, kad visų įvykių Lietuvoje baisumai ir žiaurumai palietė ir taikius gyventojus. Aukomis tapo ir realiai rėmę tarybų valdžią šimtai žmonių, ir prie jų priskaičiuoti. Tai visiškai ne vienkartiniai atvejai, ir dabartinėje Lietuvoje jie iki šiol dar deramai neįvertinti.

Net bandymai parabilti apie neginčijamai bjaurius žydų žudynių Lietuvoje dalyvius — ir tie susilaukia audringų emocijų.

Ne, tokiomis sąlygomis rami diskusija neįmanoma.

— Kur dar Viačeslavas Titovas gali paieškoti Ramanausko kaltės įrodymų? Juk jis rimtai pasišovė apginti savo tiesą.

— Aš atskirai neužsiiminėjau šia tema, bet, pakartosiu, metodas palyginimo rajonų Ramanausko aktyvumo su nacionalistinio teroro bazės duomenimis gali pasitarnauti teigiamai. Dabar reikia kruopščiai išanalizuoti areštuotų jo pavaldinių parodymus (žinoma, tai ir teisminiai dokumentai), kurie net ir kritiškai į juos pažvelgus gali duoti naudingos faktinės medžiagos. Manau, kad yra medžiagų, atsiradusių ir netarybinėje sferoje, tačiau tuo laikotarpiu — po 1944 metų — jos buvo gana objektyvios. Tikėtina, kad dalis informacijos pasiekė ir Vakarus.

Aš vis dėlto daugiau Latvija užsiiminėjau, ir štai ten yra visiškai unikalios istorijos: pavyzdžiui, amerikiečių pinigais buvo numatyta „gelbėti“ žydus, o iš tikrųjų gelbėjami buvo nacių kolaborantai, įsivėlę į žydų žudynes. Todėl būtina išsiaiškinti, ar kas nors prasiskverbė į Vakarus. Galimai tai kažkokie nevieši popieriai su Lietuvos visuomenės reakcija į taip vadinamų nacionalinių partizanų veiksmus. Tur būt ir ČŽV buvo kažkokia refleksija, bandymas išsiaiškinti, kodėl šis judėjimas vis dėlto pradėjo nykti. Negi vien tik tarybinės represinės priemonės tai skatino?

— Ar galima sakyti, kad šiandieniniai šamaniški šokiai aplin Ramanauską ir kitus abejotinus personažus — pasekmės to, kad tarybinių istorikų tyrimai neskyrė jiems reikiamo dėmesio?

— Tarybinių istorikų tyrimuose ši tema egzistuoja, tačiau jos išsami analizė buvo vertinama kaip elementas, galintis sutrukdyti lietuvių visuomenės nuraminimą. Esant kategoriškiems vertinimams, kuriuos tarybiniai istorikai skyrė „miško broliams“, išsamių jų nusikaltimų tyrimų, pasitelkiant viešuosius instrumentus, nesimatė.

Tur būt, žvelgiant iš politinės taktikos pozicijų, tai buvo pateisinama, tačiau mes praradome daug laiko, negavome labai daug parodymų. Tai liūdna ir ženkliai apsunkina darbą rekonstruojant dabartinius veiksmus.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 7 — id: `scraped:rubaltic_lt:2be3e05c77c2cc32`

**Title:** „Mes ginsimės!“ Deputatas Titovas įrodys, kad Ramanauskas–Vanagas buvo nusikaltėlis

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Partijos „Lietuvos rusų sąjunga“narys, Klaipėdos miesto tarybos deputatas Viačeslavas Titovas pasiryžęs įrodyti, kad nesulaužė priesaikos, kai klausė, ar verta įamžinti nacių talkininko Adolfo Ramanausko–Vanago atminimą. Apie tai RuBaltic.Ru papasakojo jo padėjėja Ela Andrejeva.

Anksčiau Klaipėdos miesto taryboje buvo sudaryta komisija, kuri ištirs Titovo pareiškimą, liečiantį Ramanauską–Vanagą. Klaipėdoje liepos 26 dieną lygiagrečiai vyko du mitingai — remiantys Titovą ir prieš jį. Akcijos metu deputatą miltais apipylė jo kolega taryboje Audrius Vaišvila.

Jos žodžiais, mitinge prieš Titovą jis buvo varomas į Rusiją. „Titovo gentis 300 metų gyvena Lietuvoje. Viačeslavas gimė Klaipėdoje. Jis turi tris šaunius mažamečius vaikus. Tai Lietuvos pilečiai, Lietuvos vaikai. Jie dirbs vardan Lietuvos gerovės, o jį šiuo metu kažkodėl bandoma išvyti į Rusiją. Jie turi būti mums dėkingi, kad mes, rusai, dar palaikome Lietuvą. Jie gi savo vaikus siunčia į užsienį“, — pažymėjo deputato padėjėja.

Ji pridūrė, kad toks elgesys netinkamas demokratinėje europietiškoje valstybėje. Andrejevos žodžiais, posėdžio išvakarėse vietinis televizijos kanalas ragino visus ateiti į piketą prieš Titovą, o apie jo palaikymo akciją nė žodžiu nebuvo užsiminta. „Tai provokacija, tai tarpnacionalinės nesantaikos kurstymas“, — pareiškė Andrejeva.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 8 — id: `scraped:rubaltic_lt:290914826f300933`

**Title:** „Jam pavaldžios gaujos nužudė 8 tūkstančius žmonių“: Adolfas Ramanauskas

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Baudžiamoji byla №63c, 1957 m.

Slaptai

NUTARTIS

Lietuvos Tarybų Socialistinės respublikos vardu 1957m. rugsėjo 24–25d.

Teisminė Lietuvos TSR Aukščiausiojo teismo Baudžiamųjų bylų kolegija uždarame teismo posėdyje išnagrinėjo baudžiamąją bylą

RAMANAUSKO Adolfo, Liudviko, gim. 1918 metais Nov-Bretain mieste, JAV.

Teismas, apklausęs teisiamąjį RAMANAUSKĄ ir liudytojus, išnagrinėjęs išankstinio ir teisminio tyrimo medžiagas,

NUSTATĖ:

Teisiamasis RAMANAUSKAS 1941 metais, kai prasidėjo Didysis Tėvynės karas ir Lietuvos teritoriją okupavo vokiečiai, dvi savaites vadovavo karinei „sargybai“ Druskininkuose.

1945 m. balandžio 28 d. RAMANAUSKAS įstojo į ginkluotą nacionalistų gaują, kuri vedė ginkluotą kovą prieš tarybų valdžią. Iš pradžių vadovavo banditų būriui, vėliau — kuopai, „Merkio“ ir „Dainavos“ rinktinėms, banditų apygardai Pietų Lietuvoje ir nuo 1949 m. rudens — taip vadinamoms „karinėms pajėgoms“.

Būdamas ginkluotoje nacionalistinėje gaujoje teisiamasis RAMANAUSKAS įvykdė eilę sunkių nusikaltimų.

1945 m. vasarą RAMANAUSKO vadovaujama gaujos dalyvių grupė viename kaime išvaikė valstiečių susirinkimą, išvedė ir sušaudė apylinkės pirmininką (pavardė nenustatyta). Ten pat RAMANAUSKAS pasakė valstiečiams antitarybinę kalbą.

1945 m. rudenį RAMANAUSKAS kartu su kitais gaujos dalyviais suruošė pasalas Sabartonių miške, kur sulaikė pravažiuojantį Merkinės kooperatyvo pirmininką Nikolskį, kurį pats tardė, o paskui kiti gaujos dalyviai jį nužudė [...]

Teisiamasis RAMANAUSKAS turėjo Vanago pravardę.

1947 m. vasarą RAMANAUSKAS su kitais gaujos nariais Šilo miške sulaikė nežinomą vyriškį ir įtardami, kad jis turi ryšių su saugumo organais, sušaudė.

1948 m. RAMANAUSKUI pavaldžios gaujos užpuolė Merkinės miestelį. Į valsčiaus vykdomojo komiteto patalpas, kuriose buvo įsikūrusi rinkiminė apylinkė, įmetė dvi granatas ir sužeidė keturis piliečius, tame tarpe vieną Lietuvos TSR ministrą.

1948m. balandžio 18 d. jaunimo vakaro metu buvo susprogdintas klubas — žuvo ir buvo sužeisti 47 žmonės [...]

RAMANAUSKO kaltė, vykdant minėtus nusikaltimus, įrodyta asmeniškais prisipažinimais, liudytojų parodymais, „prisiminimais“, kuriuos parašė pats RAMANAUSKAS, ir prie bylos prijungtais archyvų duomenimis.

Kadangi išdavė Tėvynę, įstojo į pogrindinę ginkluotą gaują. Duodavo nurodymus gaujų dalyviams atlikti teroristinius aktus, dalyvavo priimant mirties nuosprendžius, vykdant diversijų aktus, ir ragino tai daryti kitus, vedė antitarybinę propagandą, gyveno suklastojęs dokumentus.

Teismas, nustatydamas bausmę, laiko, jog byloje nėra lengvinančių aplinkybių.

Remiantis aukščiau išdėstytais faktais ir BK 319-320 str., Teismo kolegija

NUSPRENDĖ

Adolfą RAMANAUSKĄ, Liudviko pripažinti kaltu ir pagal str. 58-G „a“ skirti mirties bausmę sušaudant.

Šaltinis: Lietuvos TSR Aukščiausiojo teismo Baudžiamųjų bylų Kolegijos 1957 m. rugsėjo 24–25 d. nutartis, skirta Adolfui Ramanauskui–Vanagui.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 9 — id: `scraped:rubaltic_lt:d8562cc61aebfeff`

**Title:** „Prieinu prie pirmininko, o jis be ausų — nupjovė“ — specialiosios paskirties tarybinis dalinys prieš „miško brolius“

**Source:** rubaltic_lt (propaganda)

**Text:**

```
TSRS VSK (КГБ) dimisijos pulkininkas P.I. Činčenka:

„Mūsų ypatingosios Dzeržinskio divizijos 9-asis Raudonosios vėliavos ordino specialiosios paskirties pulkas 1946 metų vasario pabaigoje buvo skubiai oru permestas į Lietuvą — Šiaulius ir Vilnių. Prie mūsų pulko buvo pritvirtintas specialiosios paskirties būrys, visiškai įvaldęs diversijų ir žvalgybos operacijų meną.

Kartą iš kaimiškos apylinkės gavome informaciją, kad į vienkiemį atėjo gauja „miško brolių“, kuri tyčiojasi iš gyventojų. Mano būrys per keletą minučių sulipo į mašiną, ir po valandos mes jau buvome vietoje. Įeinam į apylinkės tarybos pastatą, o pirmininkas sėdi kampe suspaudęs delnais galvą ir vaitoja. O jo žmona rauda garsiau sirenos. Aš gi dar nepasiekus vienkiemio palikau laukymėse specialiosios paskirties pasalą. Snaiperiai įsikūrė medžiuose.

Tuos, kurie norėjo link miško prasiveržti, pasiekė snaiperiai, o ypač įžūlius ir užsispyrusius nukirto kulkosvaidininkai. Nelaisvėn to miško karo metu mes beveik neėmėm. Nebent ypatingų skyrių arba operatyviniai darbuotojai prašė savo reikmėms, tada mano kariai ėjo į mišką „liežuvio“.

Visus neatpažintus lavonus vežėme į Šiaulius prie bažnyčios, o ten jau artimieji juos atpažindavo ir pasiimdavo.“

Šaltinis: V.V.Malevanyj. Tarybiniai specialiosios paskirties daliniai Afganistane. — M.: Kučkovo laukas, 2009 — 380 pusl.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 10 — id: `scraped:rubaltic_lt:71db4ad561992ef7`

**Title:** „Atrodo, baigiasi Lietuvos demokratija“: už „miško brolių“ kritiką Lietuvoje persekiojamas deputatas

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos generalinė prokuratūra pradėjo eilinį tyrimą dėl kritinių pastabų „miško brolio“ Adolfo Ramanausko–Vanago atžvilgiu. Šį kartą Lietuvos valdžių smūgio susilaukė partijos „Lietuvos rusų sąjunga“ Klaipėdos skyriaus pirmininkas, miesto tarybos narys Viačeslavas TITOVAS.

— Pone Titovai, pasakykite, kodėl Jūsų pareiškimu susidomėjo Lietuvos prokuratūra?

— Viskas prasidėjo man ruošiantis Klaipėdos miesto savivaldybės Ekonomikos ir finansų komiteto posėdžiui.

Į darbotvarkę buvo įtrauktas mero pasiūlymas, siekiant įamžinti A.Ramanausko–Vanago atminimą, ant pedagoginio instituto sienos pakabinti lentą, nes iki 1938 metų jis mokėsi Klaipėdoje.

Iki tol aš nesidomėjau Vanagu, tačiau šiuo atveju panorau įsigilinti į temą. Aš ieškojau informacijos apie jį ir viename iš forumų aptikau oficialų dokumentą — Lietuvos TSR Aukščiausiosios Tarybos nutarimą.

Finansų komiteto posėdžio metu aš paklausiau: „Jūs manote, kad Klaipėdoje reikia įamžinti vardą žmogaus, susieto su aštuonių tūkstančių taikių gyventojų, tame tarpe ir vaikų, žūtimi?“ Man buvo atsakyta, jog tokia informacija nediskutuojama. Aš pateikiau dokumentą*, kuriame radau tokią informaciją. Priimti jį buvo atsisakyta.

— Kada buvo paskelbta apie tyrimo pradžią dėl Jūsų pasisakymo?

— Po pasisakymo „Klaipėdos“ laikraštyje lietuvių kalba. Facebook aš taip pat įmečiau pareiškimą, kad žmonės žinotų. Ir kilo skandalas, įsiplieskė karšti ginčai. Yra Vanago šalininkų, yra priešininkų. Man net skambino vienas anų laikų nusikaltimų liudininkas. Tuomet jis buvo mažas, visa šeima buvo išžudyta, berniukas augo vaikų namuose.

Mano klausimas daug kam nepatiktų. Nepatiko ir merui, kad aš nepatogius klausimus pateikiu. Po to vietoj diskusijų sekė kreipimasis į prokuratūrą. Vietoj diskusijos, remiantis faktais, jie nutarė eiti kiti keliu. Prokuratūra pradėjo ikiteisminį tyrimą elgesio žmogaus, kuris, būdamas miesto tarybos deputatu, užduoda klausimus. Taigi atrodo, kad demokratija pas mus baigiasi.

— Į prokuratūrą kreipėsi Jūsų kolegos?

— Atvirai sakant, nežinau, kas taip pasielgė. Apie šį faktą rytą sužinojau iš žurnalistų. Meras inicijavo mano mandato panaikinimą, numatoma rinkti parašus ir kreiptis į teismą su ieškiniu dėl priesaikos pažeidimo.

— Klaipėdos miesto meras pasakė, kad Jūs savo pareiškimu galimai pažeidėte miesto tarybos nario priesaiką. Ką jis turėjo omeny? Kuris priesaikos punktas galėjo būti pažeistas?

— Aš tik vykdžiau savo, deputato, pareigas, pateikiau klausimus. Jie gi tvirtina, kad tokiu būdu aš pažeidžiau priesaiką. Esą aš apkaltinau Vanagą nužudžius aštuonis tūkstančius žmonių.

Bet aš nesakiau, kad jis pats tai padarė, jis vadovavo anoje teritorijoje veikusioms grupuotėms. Jeigu žmogus tiesiogiai arba ne jame kaltas, aš manau, kad Klaipėdoje neturi būti vietos jo atminimo įamžinimui. Mūsų vaikai turi augti žinodami kitokius didvyrius.

— Kaip Jūs vertinate ikiteisminių tyrimų perspektyvas?

— Teismas gali nepripažinti tų dokumentų, kuriuos aš turiu, nes jie buvo priimti tarybų valdžios metais.

— Jūs manote, kad teismas gali priimti Jums nepalankų sprendimą?

— Nežinau, kuo tai baigsis. Jeigu ką nors ištemps viešumon, tai bus politinis užsakymas. Tada teisėsaugos ir teismų veiksmais aš galutinai nusivilsiu.

— 2017 metų lapkrity Lietuvos Seimas paskelbė 2018-uosius metus „miško brolio“ Ramanausko-Vanago metais. Maždaug tuo metu buvo koneveikiama Rūta Vanagaitė, taip pat dėl pareiškimų apie Vanagą. Vanagas kuo tai svarbus Lietuvai? Kodėl jam skiriama tiek daug dėmesio?

— Kaip supratau, tai kovos su tarybų valdžia simbolis. Jį pavertė simboliu. Kai kurie veikėjai tvirtina, kad jis kovėsi su Tarybų Sąjunga. Tačiau yra dokumentai, patvirtinantys jo nusikaltimus. Galimai buvo nutarta, jog visa tai nesvarbu ir neturi jokios reikšmės. Bet gi yra Lietuvos teismo nuosprendis, tačiau su juo Vanagą palaikantys asmenys nenori susipažinti.

— Kaip Jūs vertintumėte gyventojų, deputatų ir valdininkų požiūrį į Vanagą? Ar čia tikra meilė ir pagarba, ar kažkokia valstybės primesta mada?

— Galimai vyko kampanija, parodanti koks Vanagas šventas, geras žmogus. Yra žinoma, kad jo biografijoje buvo ir šviesių momentų, už ką žmonės jį gali gerbti. Bet mano rankose konkretus faktas — teismo nuosprendis, kuriame pasakyta, kad jis susietas su žmonių žudynėmis. Ir todėl aš nelaikau jo šventuoju.

— Kaip Klaipėdos gyventojai reaguoja į Jūsų persekiojimą dėl Vanago?

— Šiuo metu mane daug kas palaiko ir remia, mano veiksmams pritaria. Man sunku pasakyti, kiek aš turiu šalininkų. Triukšmą sukėlė politikai, valdininkai, formuojantys visuomenės nuomonę.

Be to, po metų pas mus vyks savivaldos rinkimai. Meras, tur būt, nori, kad ūgteltų jo reitingas, tad ir rodo, kad kaunasi su Titovu.

— Ar, Jūsų manymu, meras tikrai yra Vanago šalininkas, ar šią temą panaudoja politiniais tikslais?

— Pagal viską, aršus šalininkas. Nes jis inicijavo tą įamžinimą. Tai jo sprendimas.

— Kaip Jūs manote, kokiu tikslu Jūs persekiojamas, kodėl vyksta „miško brolių“ palaikymo kampanijos?

— Valstybingumas sukurtas neigiant visa tai, kas buvo tarybinio ir rusiško. Juk turi būti istoriniai didvyriai. Tokie didvyriai surandami, sukuriami mitai. Istorija visada perrašinėjama pagal valdžios poreikius. Tačiau yra daug padorių žmonių, kurių atminimą būtų galima įamžinti. Tačiau valdžia pasirinko gana keistą kelią.

— Ar, Jūsų manymu, sėkminga tokia pilitika?

— Tai kelias į niekur. Savo tautos krauju parašyta istorija nedaro valstybingumą tvirtesniu. Jeigu mes norime gyventi normalioje ir klestinčioje valstybėje, kuri rūpinsis kiekvienu savo gyventoju, privalome diskutuoti, pasinaudodami faktais. Bet nevalia naudotis buldozeriu, nušluojančiu visas diskusijas, kritiką ir pan.

— Ar Lietuvos gyventojai tiki savo vyriausybės politika?

— Vieni tiki, kiti — ne. Vieni netiki, bet tyli, nes bijo to buldozerio. Jau yra nukentėjusių. Todėl visi tyli.

* Lietuvos TSR Aukščiausiojo teismo Baudžiamųjų bylų Teisminės kolegijos 1957 m. rugsėjo 24–26d. nutartis Adolfo Ramanausko–Vanago atžvilgiu (versijos lietuvių ir rusų kalbomis).

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 11 — id: `scraped:rubaltic_lt:6fb82020c939acd6`

**Title:** Lietuvos energetinės nepriklausomybės kainas nustato politikai, o moka gyventojai

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvoje birželio pabaigoje elektros energijos kainos per keletą dienų išaugo 13 proc. ir viršijo 50 eurų už megavatvalandę. Toks svarus šuolis negali nesukelti nuostabos. Tačiau norint suprasti, kas dedasi Lietuvos respublikoje su elektros energijos kainomis, reikia pasitelkti atmintį, logiką ir susigaudymą statistikoje. Taigi pabandykime kartu pavaikščioti pagal šią paprastą grandinėlę.

„Vėjo jėgainių gamybos apimtys sumažėjo beveik perpus“. Perskaitykite šią frazę keletą kartų — gal ir suprasite, apie ką eina kalba. Kur, kokioje vietoje pastatytos šios paslaptingos elektrinės? Jeigu gamyba sumažėjo vos ne 50 proc., tai kodėl kainos pakilo tik 13 proc.? Kai visiškai nebuvo vėjo, ir ką bendro su visu tuo turi Lietuva? Vadinasi, priežastis ne tame.

2009-aisiais buvo galutinai sustabdyti abu Ignalinos AE reaktoriai — taip nutarė Lietuvos vyriausybė. Nuo to momento Lietuva tapo elektros energijos stokojančia valstybe, priklausomybė nuo elektros energijos importo padėjo kryžių ant šalies energetinio saugumo.

O jeigu kalbėti apie savos elektros energijos gamybą, tai būtina pažymėti visiškai paprastą faktą: sutikdama uždaryti Ignalinos AE, Lietuva pasmerkė save visiškai energetinei priklausomybei ne nuo Rusijos, o konkrečiai nuo vienos kompanijos, kuri vadinama „Gazpromu“. Jeigu atmesti Kauno HE su jos 100 megavatų, tai visos kitos Lietuvos elektrinės gyvuoja dėka gamtinių dujų.

Bet ne Rusija ir ne „Gazpromas“ primetė Lietuvai priklausomybę, viskas įvyko visiškai atvirkščiai, tai tūlas „Lietuvos vyriausiasis energetikas“, nedrąsiai įžengęs į „Gazpromo“ prezidento kabinetą, pralemeno: „Valdykite mus, nes žemė mūsų nors ir nedidelė, joje labai daug betvarkės“. Aleksejus Mileris neprieštaravo — ir ne daugiau.

Ar buvo informacija, kad „Gazpromas“ ženkliai sumažino Lietuvai tiekiamų dujų apimtis? Į šalį jos patenka iš Inčukalnsko požeminės dujų saugyklos Latvijoje per magistralinį dujotiekį Minskas–Vilnius. Ne, nieko panašaus nebuvo ir negalėjo būti, juk dėka dar vieno dujotiekio Minskas–Vilnius–Kaunas melsvą kurą gauna Kaliningradas ir Kaliningrado sritis. „Gazpromas“, be jokių priežasčių pažeidžiantis sutartimis numatytus santykius su Lietuva ir ketinantis Kaliningrado sritį palikti be dujų — tai net juokinga. Vadinasi, elektros energijos kainų šuolio priežastys ne tame.

Nuo to momento, kai Lietuva Klaipėdos uoste pastatė laivą Independence, respublika pradėjo naudoti suskystintas gamtines dujas (SGD) iš Norvegijos ir net iš Jungtinių Amerikos Valstijų. Ar buvo pasirodžiusi informacija, kad staiga dingo SGD? Ne, tokios nebuvo, t.y. ir čia beprasmiška ieškoti elektros energijos kainų šuolio priežasties.

Tokiu būdu — problema ne hipotetiniame gamybos apimčių kritime Lietuvos teritorijoje. Tenka aiškintis, kas gi iš išorinių tiekėjų sumažino tiekimo apimtis.

Lietuvos elektros tinklai sujungti su Latvija, Lenkija, Baltarusija ir Rusija, o povandeniniu kabeliu — su Švedija. Elektros energijos iš Lenkijos į Lietuvą tiekimas pagal 2017 metų statistiką sudarė tik 5 proc. sunaudotų apimčių — nėra prasmės apie tai kalbėti.

Su Baltarusija Lietuva pasistengė nutraukti visus pirkimus, realiai nuversdama stulpus ir nuimdama laidus — taip pat nėra prasmės šios situacijos analizuoti.

Elektros gamyba Latvijoje — tai Dauguvos elektrinių virtinė, biržely nuleisti vandenys, susikaupę pavasario polydžio metu. Ką sako statistika? Elektros energijos tiekimas iš Latvijos birželio mėnesį lyginant su geguže sumažėjo 79 proc. Štai kur šuo pakastas — prieš gamtos dėsnius jokie vyriausybių nutarimai ir balsavimai parlamentuose bejėgiai.

Pagal 2017 metų statistiką — 31 bendro importo apimties proc. O kas Rusijoje? O Rusijoje Smolensko AE vyksta planinis perspėjamasis energijos blokų remontas. Planinis tikrąja šio žodžio prasme, be jokių ypatingų atsitikimų ir staigmenų.

Bet Lietuva perka elektros energiją biržoje. Ir europietiškos taisyklės nenumato ilgalaikių kontraktų, o Lietuva, kaip žinia, nori prisilaikyti visų ES taisyklių. Todėl susitarti su Rusija kad ir žiemą — negalėjo ir nenorėjo.

Rusija ir jos „Rosatomas“ planingai sumažino generacijos apimtis profilaktinės reaktorių apžiūros metu. Vieninga energetinė sistema Sisteminio operatoriaus vaidmenyje visa tai iš anksto numatė, ir todėl Rusija savo problemas išsprendė, o Lietuvai nepasisekė.

Antras pagal apimtis elektros energijos Lietuvai tiekėjas — Švedija. Pagal 2017 metų rezultatus — 27 proc. Kodėl nepadėjo? Švedijos elektros energijos generacijos struktūra neužslaptinta, viską galima rasti žinynuose: 40 proc. — atominės elektrinės, 40 proc. — hidroelektrinės, visa kita — įvairūs atkuriamieji energijos šaltiniai.

Apie hidroelektrines nėra ko kalbėti — jau viskas pasakyta, samprotaujant apie Latviją. O atominės? Taip, čia rusų kalba nieko nerasime, pašykštėjo mums tokių smulkmenų žiniasklaida. Tačiau Švedijos atominės elektrinės niekada nebuvo užslaptintos, problema — viską perskaityti švedų kalba. Tekstas ten, tiesa, visiškai techninis, tačiau smulkmenos mus ne ypatingai domina — planiniai perspėjamieji remontai biržely vyko ir dviejose stambiausiose Švedijos AE — vienu metu Ringhals ir Forsmark. O, kaip jau buvo pasakyta, pirkti elektros energiją Lietuva gali tik biržoje, galimybės pasirašyti ilgalaikius kontraktus nenumatytos.

Kaip klostosi reikalai vėjo jėgainėse — visiškai nesvarbu, jų gaminamos elektros energijos kiekiai Lietuvoje siekia vos kelis procentus. Kokios išvados?

Jeigu Lietuva pasiryžusi vykdyti visus Europos Sąjungos nurodymus ir savo noru atsisako bendradarbiavimo energetinio žiedo rėmuose, už tokį malonumą moka jos gyventojai. „Nieko naujo po mėnuliu“, kaip pasakė vienas senovės išminčius: nepriklausomybė nuo sveiko proto — brangus malonumas. Belieka pasveikinti Lietuvą su šia nepriklausomybe ir pakartoti, kad šį kelią ji pasirinko be jokios prievartos.

Rezultatas: Lietuvos gyventojai ir verslininkai savo kišenėmis apmoka respublikos vadovybės politiką. Tuo, kas pasakyta, nepiktdžiugaujame.

Lietuva turi teisę disponuoti savo nepriklausomybe taip, kaip jos manymu reikia. Brangu — tačiau be Baltarusijos. Brangu — tačiau pagal ES taisykles, nepasinaudojant energetinio žiedo galimybėmis. Ir visai gali būti, kad lietuviams tai patinka.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 12 — id: `scraped:rubaltic_lt:3c85776d2a1ed4db`

**Title:** Lietuvoje greta laidojami nacių talkininkai ir prezidentai

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Paminėdama valstybingumo šimtmetį, Lietuva galutinai įteisins „miško brolius“ kaip naujus „kovos už laisvę“ simbolius. Šio proceso, užėmusio kelis dešimtmečius, kulminacija turi tapti Adolfo Ramanausko–Vanago palaikų perlaidojimas su karinėmis pagerbimo ceremonijomis. Likimo ironija: „miško brolių“ vadas, susikruvinęs rankas ne tik Antrojo pasaulinio karo metais žudant Lietuvos žydus, bet ir po karo taikius gyventojus, amžiną poilsį atras greta pirmojo dabartinės Lietuvos prezidento Algirdo Braz Paminėdama valstybingumo šimtmetį, Lietuva galutinai įteisins „miško brolius“ kaip naujus „kovos už laisvę“ simbolius. Šio proceso, užėmusio kelis dešimtmečius, kulminacija turi tapti Adolfo Ramanausko–Vanago palaikų perlaidojimas su karinėmis pagerbimo ceremonijomis. Likimo ironija: „miško brolių“ vadas, susikruvinęs rankas ne tik Antrojo pasaulinio karo metais žudant Lietuvos žydus, bet ir po karo taikius gyventojus, amžiną poilsį atras greta pirmojo dabartinės Lietuvos prezidento Algirdo Brazausko, viešai atsiprašiusio už Holokaustą ir žadėjusio nubausti jame dalyvavusius lietuvius.

Tikslu organizuoti iškilmingą nacių talkininko palaikų perlaidojimą, Lietuvoje sudaryta valstybinė komisija, o 2018-ieji paskelbti Adolfo Ramanausko–Vanago metais (jis gimė 1918 m.). Atsižvelgiant į tai, jog šiais metais minimas Lietuvos valstybingumo šimtmetis, ši priemonė, vietos valdžių sumanymu, turi tapti dukart simboline. Juk kalba esą eina apie politikos veikėją, kovojusį prieš „sovietinę okupaciją“ ir paklojusį dabartinės nepriklausomos valstybės pamatus.

Tuo, jog Lietuvos valdžios sugebės išaukštinti dar vieną nacių nusikaltėlį, netenka abejoti. Tame prezidentė Dalia Grybauskaitė sukaupė didelę patirtį. Būtent jos pastangomis 2012m. su karinėmis pagerbimo ceremonijomis buvo perlaidoti Juozo Ambrazevičiaus palaikai — vadovo taip vadinamosios Lietuvos laikinosios vyriausybės, kurią 1941 m. buvo sudarę tautos „partizanai“. Tas atvejis iššaukė tarptautinių žydų organizacijų protestą, o taip pat ir platų visuomenės rezonansą pačioje Lietuvoje, nes Ambrazevičius ne tik talkino naciams, bet ir tiesiogiai dalyvavo Lietuvos žydų genocide, kas patvirtinta dokumentaliai.

Beje, žudyti žydus „Lietuvos aktyvistų frontas“ pradėjo pirmosiomis karo dienomis. Jau 1941 m. birželio 27 d. Lietuvos laikinosios vyriausybės posėdžio protokole užfiksuotas komunalinio ūkio ministro Vytauto Landsbergio–Žemkalnio (Vytauto Landsbergio tėvo) pranešimas apie ypatingai žiaurius pasityčiojimus iš žydų Kaune. O birželio pabaigoje Ambrazevičiaus vadovaujama Lietuvos vyriausybė nutarė įkurti Kaune specialią koncentracijos stovyklą žydams. Iki mūsų dienų išliko Ambrazevičiaus pasirašytas posėdžio protokolas:

„Ministrų kabinetas nutarė: ... pritarti žydų koncentracijos stovyklos įkūrimui ir tai atlikti įpareigoti poną Švipą, komunalinio ūkio vice ministrą, kontaktuojant su pulkininku Bobeliu“.

Vieta koncentracijos stovyklai Kauno VII forto teritorijoje buvo parinkta ne atsitiktinai, nes ten ir anksčiau buvo masiškai žudomi žmonės. Esmė tame, jog po to, kai pasitraukė Raudonoji armija, miestą formaliai kontroliavo „Lietuvos aktyvistų frontas“, pradėjęs terorą prieš savo piliečius ir žydus.

Menkiausiai įtarus gyventojus bendradarbiavus su tarybų valdžia, jie buvo nedelsiant sušaudomi. Žudynės tapo tokiomis masiškomis, kad vokiečiai net buvo priversti uždrausti šaudyti žmones be jų leidimo.

Ši koncentracijos stovykla tapo pirmuoju „mirties konvejeriu“ nacių okupuotoje Tarybų Sąjungos teritorijoje. Iki 1941m. rugpjūčio pradžios VII forte buvo sušaudyta apie 5 tūkstančiai žmonių — dauguma žydai.

Šiandien VII forto teritorija privatizuota ir naudojama pasilinksminimo renginių organizavimui.

Pirmuosius susidorojimų su žydais rezultatus vokiečiai susumavo Saugumo policijos ir Saugumo tarnybos 1941m. liepos 11d. pranešime: „Po to, kai Raudonoji armija pasitraukė iš Kauno, miesto gyventojai stichiniu protrūkiu nužudė apie 2500 žydų. Kitą didelį žydų skaičių sušaudė pagalbinės tarnybos policija (partizanai)... Kaune dabar viso pribaigta 7800 žydų, dalinai pogromų metu, dalinai juos sušaudė lietuviškosios komandos“.

Jau 1941m. spalio 31d. brigadenfiureris Valteris Štalekeris konstatavo: „Bendras Lietuvoje likviduotū žydų skaičius sudaro 71105 žmones“.

2000 metų rugsėjy Seimo pirmininko Vytauto Landsbergio iniciatyva parlamentas vos nepriėmė įstatymo, pripažįstančio Laikinąją Ambrazevičiaus vyriausybę teisėta Lietuvos vyriausybe, tačiau buvo atšauktas visuomenei užprotestavus.

Lietuvos valdžių nutarimas karo nusikaltėlį paversti eiliniu nacionaliniu didvyriu įsiterpia į daugiametės valstybinės politikos vėžes kuriant nacionalistinę ideologiją, kurios pagrindą sudaro „miško brolių“ „išvadavimo“ karas. Šioje Pabaltijo respublikoje jie po mirties pagerbiami aukščiausiais valstybės apdovanojimais, atidengiami paminklai ir memorialinės lentos, jų vardais pavadinami parkai ir gatvės. Žydų bendruomenės ir progresyvios visuomenės pasipiktinimas, kaip žinia, ignoruojamas nurašant „rusų propagandai“.

Lietuvoje pastaraisiais dešimtmečiais buvo atliktas didžiulis darbas, siekiant išaukštinti nacių talkininką Ramanauską–Vanagą, įvykdžiusį senaties termino neturinčius karo nusikaltimus. 1999 metais Izraelis perdavė Lietuvai sąrašą žydų žudikų, kuriame yra ir pavardė šio būsimo lietuvių „nacionalinio didvyrio“ — „žiauraus ir vieno iš pagrindinių masiškų žydų žudynių Druskininkuose, Merkinėje, Butrimonyse, Jiezne ir kituose miestuose dalyvių“.

Dėl to Lietuvos valstybė bandė ne tik kelti baudžiamąsias bylas sudarytojams šio sąrašo, kuris, beje, iki šiol nepaviešinamas (jame virš 3 tūkstančių pavardžių), bet ir nuteisti savo veteranus, prisidėjusius prie „partizano“ sulaikymo ir žūties. Pavyzdžiui, Lietuvos žydų Izraelio asociacijos vadovui, buvusiam Kauno geto  kaliniui Josifui Melamedui ir jo kolegai, vienam iš memorialo Jad va–Šem steigėjų, Tarptautinės komisijos, tiriančios okupacinių režimų Lietuvoje nusikaltimus, nariui Ichakui Aradui net buvo iškeltos baudžiamosios bylos, kurios užsibaigė sensacingu tarptautiniu skandalu.

Pačioje Lietuvoje naujų didvyrių kėlimo ant pjedestalų priešais buvo paskelbti savi veteranai. Antai 2011 metų biržely Kauno apygardos teismas byloje „Dėl Lietuvos partizanų genocido“ buvusiam saugumo karininkui Vytautui Vasiliauskui skyrė ketverius laisvės atėmimo metus.

2015 metais Kauno apygardos teismas 84 metų tarybinio saugumo veteranui Stanislovui Drelingui skyrė penkerius laisvės atėmimo metus „už genocidą Lietuvos partizanų, kovojusių prieš tarybų valdžią“. Jis buvo kaltinamas dalyvavęs 1956 metais „pasipriešinimo“ organizatoriaus Ramanausko–Vanago sulaikymu. Ir nors teisiamasis neigė dalyvavęs šioje operacijoje, teisminė sistema nusprendė, kad jis dalyvavo „tuose veiksmuose, kurie padėjo kitiems sovietinės okupacinės valdžios atstovams“.

O Europos žmogaus teisių teismas sukritikavo Lietuvos teisminės sistemos bandymą išplėsti teisminę praktiką, įtraukiant į genocido sampratą „fizinis naikinimas dalies lietuvių gyventojų, priklausančių atskirai politinei grupei, o būtent Lietuvos partizanams“. 2015 metų spalio mėn. Europos teismas paskelbė nutartį pagal buvusio TSRS saugumo karininko Vytauto Vasiliausko ieškinį, kad „ieškovas buvo nepagrįstai nuteistas Lietuvoje kaltinant jį genocidu“.

Valstybinė Lietuvos politika siekiant išaukštinti lietuviškuosius nacių talkininkus, iš kurių nė vienas taip ir nebuvo teisiamas, ne tik grubiai pažeidža Jungtinių tautų rezoliuciją (2014m. gruodžio 18d. 69/160) „Dėl kovos prieš nacizmo heroizavimą“, bet ir sudaro sąlygas plėstis antisemitizmui, rasizmui, rasinei diskriminacijai, ksenofobijai ir nepakantumui.

Deja,  naujų tautos „didvyrių“ atsiradimas reikalauja naujų teisminių procesų tų Lietuvos partizanų atžvilgiu, daugiausia žydų tautybės, kurie kovėsi su naciais ir jų vietiniais talkininkais. Ir todėl Izraelio reakcija bus dar griežtesnė. Galų gale Lietuva rizikuoja patekti tarptautinėn izoliacijon, kaip tai neseniai atsitiko Lenkijai dėl jos istorinio antisemistinio revizionizmo politikos.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 13 — id: `scraped:rubaltic_lt:835818973d956514`

**Title:** Valdžių politika sustabdė Lietuvos projektą „Misija Sibiras“

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Rusija sustabdė vizų išdavimą lietuviškojo memorialinio projekto „Misija Sibiras“ dalyviams. Į šią naujieną dėl suprantamų priežasčių labai liguistai reagavo Lietuvos visuomenė. Tačiau kaltinti tuo, kas įvyko, Lietuvos gyventojai gali tik savo politinę vadovybę, kuri, paskelbusi „karą paminklams“ ir kliudydama prižiūrėti tarybinių karių kapus, privertė Rusiją imtis atsakomųjų priemonių. Būtent tokiu elgesiu Vilnius iškėlė grėsmę vienam iš vertingiausių Lietuvos ir Rusijos humanitarinių projektų.

„Misija Sibiras“ — retas Lietuvos–Rusijos santykiuose išties sėkmingai įgyvendintas projektas. Istorinės politikos sferoje tai bene vienintelis toks sėkmingas projektas. „Misija Sibiras“ — įrodymas, jog skausmingais ir kraujuojančiais bendros istorijos ir istorinės atminties klausimais tarp Lietuvos ir Rusijos galimi supratimas ir bendradarbiavimas.

Sakykime, buvo galimi.

Lietuvių, kurie tapo stalininių deportacijų aukomis, kapaviečių priežiūros projektą 2000 metais pasiūlė Lietuvos jaunimo organizacijos. Jį entuziastingai parėmė Lietuvos užsienio reikalų ministerija, kuri susitarė su rusų kolegomis dėl kasmetinių Lietuvos jaunimo išvykų į palaidojimo vietas Sibire.

Šių dienų Lietuvos URM laiminti tokį projektą, kaip „Misija Sibiras“, nepajėgi.

Pirma, kas Smolensko aikštėje leis Vilniaus atstovams peržengti slenkstį po to, ką dabartinis užsienio reikalų ministras Linas Linkevičius prišnekėjo (ir tebešneka) Rusijos adresu?

Antra, Maskvoje ilgainiui priprato prie to, jog Lietuvos istorinės politikos esmė — save matyti nekalta auka, kuriai visi aplinkiniai skolingi, tokioje būsenoje tūpti Rusijai ant sprando, priverčiant ją mokėti kompensacijas ir atgailauti.

Po visų Seimo komisijų, skaičiavusių, kiek šimtų milijardų čekį reikėtų išrašyti dėl „kompensacijos už okupaciją“, vargu, ar kas Maskvoje patikės, kad iš už Lietuvos URM iniciatyvos organizuoti Lietuvių ekspediciją kapaviečių tvarkymui nekyšo merkantilinio politinio apskaičiavimo ausys.

Trečia, abejotina, jog dabartiniai URM ir prezidentūros šeimininkai pritartų idėjai siųsti į Rusiją jaunus lietuvius. Juk jie ten atsidurs „rusų propagandos“ įtakoje! Namo sugrįš jau būdami Sibiro „minkštųjų jėgų“ paruoštais tikraisiais „Kremliaus agentais“.

Nepaisant tragiškų priežasčių, dėl kurių Lietuvos savanoriai kasmet vyko į Sibirą, lietuviškasis projektas buvo teigiamai vertinamas ir Lietuvoje, ir Rusijoje.

„Ši misija teigiama įvairiomis prasmėmis. Važiuoja ir suranda senas lietuvių kapines, sutvarko jas, vienija įvairių tautų atminimą. Kaip pasakoja patys šių ekspedicijų dalyviai, Rusijos žmonės stebisi, kad tuo pačiu tvarkomos ir pravoslavų kapinės. Gerbia atminimą visų, neskirstydami tautybės ir tikėjimo principu, — tai labai svarbu. Ekspedicijos dalyviai pažymi, jog vietinė valdžia šią veiklą vertina itin teigiamai. Tokiu būdu naujoji karta stato tiltus, ji remiasi nors ir skausminga praeitimi, tačiau šiandien tai atrodo naujoviškai, pozityviai, dvelkia susitaikymu, — prieš keletą metų sakė tuometinis Lietuvos užsienio reikalų ministro pavaduotojas Evaldas Ignatavičius. — Nesijaučia jokio priešiškumo. Jaunimas susiduria su gyva istorija, atranda naujus jos puslapius. Rusų tauta nemažiau nukentėjo nuo represijų — to neužmirštant, reikia daryti išvadas. Ir, žinoma, rūpintis paveldu, istorija, mūsų bendra praeitimi. Išvykų dalyviai tai ir daro“.

Taip kad „Misija Sibiras“ tikrai buvo retas sėkmės atvejis Lietuvos–Rusijos santykiuose. Šio projekto įtakoje vyko derybos dėl Rusijos–Lietuvos tarpvyriausybinio susitarimo tvakant kariškių ir civilių karo bei represijų aukų palaidojimo vietas. Tačiau vėliau lietuviai užšaldė visas derybas pagal šį dokumentą.

Lietuvos valdžios atkakliai priešinasi raudonarmiečių kapų priežiūros ir fašizmo nugalėtojų atminimo įamžinimo klausimais.

Kultūros paveldo departamentas įpareigojo Lietuvos karo istorijos asociaciją pašalinti antkapius, esančius Antakalnio kapinėse ant Rusijos imperatoriškosios kariuomenės kareivių, o taip pat ant Raudonosios armijos karių, žuvusių vaduojant Lietuvą iš nacizmo 1944 metais, kapų.

Palangoje siūloma atkasti raudonarmiečių kapus ir perkelti jų palaikus iš miesto centro į pakraštį.

Nemunėlio mieste prie paminklo tarybiniams kariams buvo pritvirtinta „paaiškinanti lentelė“ apie „sovietinę okupaciją“ ir „stalininį genocidą“. Taip padaryti siūloma visoje Lietuvoje.

Šiaulių valdžios planuoja de-fakto likviduoti paminklą tarybiniams kariams, pakeičiant jį gulinčia horizontalia plokštimi. Klaipėdoje ne kartą buvo išniekintas memorialas miesto vaduotojams.

Lietuvos Seimo nariai ruošia įstatymo projektą „Dėl komunizmo ir kitų totalitarinių režimų propagandos draudimo viešose vietose“, kurio aukomis gali tapti tarybiniai paminklai. Lietuvos saugumo departamentas paskutinėje kasmetinėje ataskaitoje pareiškė, kad karinių kapaviečių priežiūra ir memorialų restauravimas — „Lietuvos įtraukimas į Rusijos geopolitinę erdvę“. Suprask: tas lietuvis, kuris prižiūri nežinomo raudonarmiečio kapą greta savo artimųjų kapų, — Kremliui parsidavęs valstybės išdavikas.

O dar oficialusis Vilnius neleidžia Rusijai rūpintis kapinėmis. Pagal naujas taisykles bet kuris kultūros paveldo objekto (o tie objektai yra ir tarybiniai paminklai) finansavimas užsienio lėšomis galimas tik per objekto valdytojus – savivaldybes. Tačiau RF įstatymai draudžia perdavinėti Rusijos biudžetines lėšas kitoms valstybėms ir jų savivaldos organams. Tokiu būdu Rusija praranda galimybę vykdyti memorialų restauravimo darbus.

Rusijos atstovai daug mėnesių aiškino Lietuvos valdžioms, kad tokia politika verčia pasinaudoti vienintele išeitimi — imtis atsakomųjų priemonių ir užšaldyti projektą „Misija Sibiras“. Šios numodavo ranka.

Ir štai rezultatas.

Tokiu būdu ypač svarbios lietuvių tautai akcijos ateitis pakibo ant plauko. Ir kaltinti tuo Lietuvos piliečiai gali tik savo valdovus, kuriems neapykanta Rusijai svarbiau istorinės atminties išsaugojimo, protėvių kapų priežiūros, kartų ryšių ir naujų lietuvių kartų patriotinio auklėjimo.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 14 — id: `scraped:rubaltic_lt:bba6e5d3209b9f77`

**Title:** O dar aš pasakysiu: Grybauskaitė prisakė ruoštis Rusijos įsiveržimui

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos prezidentė Dalia Grybauskaitė pareiškė interviu vokiečių žurnalui Spiegel, kad reikia ruoštis Rusijos įsiveržimui į Lietuvą. Metams likus iki valstybės vadovės kadencijos pabaigos Grybauskaitės žodžius galima suprasti kaip politinį priesaką: ponia Dalia prisakė ateinančioms lietuvių kartoms ir tarptautiniams Lietuvos partneriams savo, kaip prezidentės, pagrindinį credo — niekada nepamiršti „rusų grėsmės“.

„Pavojus (Rusijos įsiveržimo į Lietuvą — RuBaltic.Ru past.) didelis, jei mes pastoviai nesirūpinsim savo gynimosi galimybėmis. Jei mes parodysim, kad galime ir norime gintis, tada mus niekas nepuls. Mes turime būti pasiruošę — mentaliai, politiškai, technologiškai, siela ir širdimi. Rusijos kariuomenė prie Pabaltijo šalių ir Lenkijos sienų savo sudėtimi dešimt kartų skaitlingesnė už NATO kariuomenę. Bet esmė ne tik skaitlingume. Svarbu pareiga ir noras gintis. Jeigu mūsų tauta ir partneriai bus tam pasiruošę, tokiu atveju nebus priežasčių mus okupuoti“, — kalba Dalia Grybauskaitė interviu Spiegel.

Publikacijos labiausiai įtakinguose ir daugiatiražiniuose Vakarų leidiniuose (o toks, be abejonės, yra vokiečių Spiegel) — neeilinis įvykis Pabaltijo šalių lyderiams. Todėl jie ypač atsakingai žiūri, ką reikia akcentuoti, būtent ką ir kokiais išsireiškimais pateikti vakarų sąjungininkams.

Grybauskaitės atveju tai, jog kalba eina apie interviu, nieko nekeičia. Lietuvos prezidentė, bendraudama su žiniasklaida, įrodė, kad tikrų, „gyvų“ interviu ji niekada neduoda. Jei žurnalistas nori su ja pabendrauti, ponia Dalia nuo jo pabėga. Jeigu vedantysis užduoda iš anksto nesuderintą klausimą, ji skandalingai išeina iš studijos.

Todėl galima neabejoti: vokiečių žurnalo klausimų poniai prezidentei sąrašas buvo iš anksto peržiūrėtas ir Daukanto aikštėje patvirtintas. O gal ten ir buvo sukurtas. Įtraukiant tą apie Rusijos įsiveržimo į Lietuvą pavojų.

Ir, žinoma, tai bus pateikta prezidentei būdingoje jausmingoje manieroje. „Mes turime būti siela ir širdimi pasiruošę Rusijos įsiveržimui...“ Ir taip šioje ponioje pasireiškia jos „raudonoji“ praeitis.

„ — Komjaunuoli! Atremti rusų agresiją būk pasiryžęs!

— Visada pasiryžęs!“

Žinoma, šaunu, kad ypatingas viltis ginant tėvynę Grybauskaitė sieja su Lietuvos jaunimu. „Jaunoji karta pasiryžusi ginti tėvynę“, — sako ji.

Iš kur pas ponią prezidentę atsirado tokia informacija? Lietuva pastaraisiais keliais metais tapo absoliučia Europos čempione pagal emigruojančių gyventojų skaičių, o juk 52 proc. išvykstančiųjų sudaro būtent jaunimas. Devyni iš dešimties vyresniųjų klasių moksleivių pareiškia, kad nori išvažiuoti iš Lietuvos. Keistas sutapimas — nauja emigracijos iš Lietuvos banga pakilo 2015 metais, kai buvo atnaujintas karinis šaukimas. Ar ne nuo karinės tarnybos bėga jauni lietuviai į Angliją ir Airiją?

Tačiau poniai prezidentei šie faktai, kaip žinia, nerūpi — ji ryžtingai pareiškia, kad jaunoji lietuvių karta pasiruošusi ginti tėvynę.

Pagrindinis bet kokio mito kūrimo priešas — faktai ir logika; Pabaltijyje įpratę jų atsikratyti emocionaliai ir sofistiškai.

Puiki Grybauskaitės patoso iliustracija: „Mes padarėme didžiulę klaidą, taip pasielgę 1940 metais (atsisakę ginti Lietuvos — RuBaltic.Ru past.), kai Raudonoji armija įžengė į Lietuvą ir ją okupavo. Tai baigėsi genocidu. Mes tada praradome beveik 15 proc. gyventojų, dauguma šių žmonių buvo deportuoti į sovietinius lagerius.“ Dešimtmečiais Pabaltijo politikai savo kalbose tarptautinėse erdvėse įrodė: požiūrių neadekvatumas ir isterija balse — geriausias ginklas prieš nepatogius klausimus, liečiančius tarptautinius ir teisinius okupacijos ir genocido apibrėžimus.

Lietuvos prezidentė sako, kad Rusijos kariuomenė prie Pabaltijo sienų dešimt kartų skaitlingesnė uš NATO. „Prie Pabaltijo sienų“ turbūt reiškia Rusijos Federacijos Vakarų karinę apygardą, kuri savo teritorija artima Europos Sąjungai. Tokiu būdu ir Maskvoje galėtų paskaičiuoti visus karinius dalinius visose ES šalyse ir pasakyti, kad prie Kaliningrado srities sienų sutelkta didžiulė kariuomenė Rusijos puolimui.

Kremliui taip reikalinga šalis su sugriauta ekonomika ir rekordiniais tempais išsilakstančiais gyventojais, kad okupuotų ją, rizikuodama sukelti karą su baranduoliniu NATO? Maskva skęsta svajonėse, kad daugelis Lietuvos rusofobų – Grybauskaitės rinkėjai ir „landsbergininkai“ — taptų Rusijos piliečiais? Pirmaujantys alkoholizmo ir savižudybių rodikliai tampa RF itin pageidaujamu ir skaniu kąsneliu?

Lietuvos prezidentė neturi atsakymų į šiuos klausimus. Ji ir neleis niekam tokius klausimus jai užduoti.

Didžiosios prancūzų revoliucijos vadai vadino nacionalizmą pilietine religija.

Ji užburia parapijiečius šventų žolelių kvapais, apsvaigina savo paistalais, ir tie parapijiečiai, Jos Didenybės apkvailinti, patiria patriotiškas haliucinacijas.

Savų vadovų nustekenta mirštanti Lietuva jiems pradeda rodytis prisikėlusia iš nebūties Didžiąja Lietuvos kunigaikštyste, valdančia didžiulius plotus nuo suomių uolų iki Juodosios jūros. Klestinčiu „Baltijos tigru“, į kurio „ekonominį stebuklą“ lygiuojasi Vakarų šalys.

Ir neokupuoja tik todėl, kad žino: visa Lietuva visiškai pasiruošusi kautis. Duokite pretekstą — ir jau rytoj galingi Lietuvos kariūnai bus Maskvoje. Virš Raudonosios aikštės suplėvesuos Vytis, Kremliaus komendantu už didžiulius nuopelnus bus paskirtas „dėdulė“ Landsbergis, o vietas okupuotos teritorijos pilietinėje administracijoje užims Laisvosios Rusijos forumo dalyviai.

Dalios Grybauskaitės priesakas ateinantiems Lietuvos prezidentams — neleisti išsisklaidyti šiems svaigalams. Neleisti lietuviams prasiblaivyti, ir toliau juos maitinant patriotiškomis haliucinacijomis.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 15 — id: `scraped:rubaltic_lt:895aa1da2d5fc711`

**Title:** Dėl depopuliacijos Pabaltijyje didės mokesčiai

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Tuomet, kai Pabaltijo šalyse mažėja gyventojų skaičius ir jie sensta, vienintelė išeitis siekiant turėti tinkamus pensijinius fondus, — didinti mokesčius. Tokias išvadas jau padarė Pabaltijo ekonomistai ir tarptautiniai analitikai, ir dabar jų prognozės pradeda pildytis: prisidengdami mokesčių reformos būtinybe politikai siūlo didinti tiesioginę ir šalutinę mokesčių rinkliavą.

Lietuvos vyriausybė pristatė Seimui mokesčių sistemos reformos projektą. Jį paskelbęs premjeras Saulius Skvernelis pradėjo tuo, jog Lietuvoje per dideli atlyginimų mokesčiai, tačiau per maži būstų apmokestinimai. Todėl būtina mažinti mokesčius dirbantiems ir didinti nekilnojamojo turto mokesčius.

Be nekilnojamojo turto mokesčių didinimo vyriausybė siūlo didinti akcizus. Planuojama didinti akcizus tabako gaminiams (sigaroms, sigaretėms, sigariloms) ir įvesti akcizinę rinkliavą elektroninėms sigaretėms, kurių sudėtyje yra nikotino.

Be to, bus peržiūrėti fizinių asmenų pajamų mokesčiai.

Eurokomisijos Lietuvoje vadovas Arnoldas Pranckevičius, atsakydamas į premjero pasisakymą, teigė, jog Lietuva surenka per mažai mokesčių, liečiančių aplinką ir nekilnojamąjį turtą. Šis „trūkumas“ Lietuvos vyriausybės darbe suteikia galimybę išplėsti mokesčių sistemos bazę.

O dar Lietuva, pasak Eurokomisijos atstovo, galėtų padidinti pridėtinę vertę, nes skirtumas tarp surenkamų PVM ir galimų PVM mokesčių — vienas iš didžiausių Europoje.

Iš to „reformos“ aptarimo Seime galima suprasti, kodėl mokesčių didinimas būtinas ir neišvengiamas. Lietuvos politikai aptaria mokesčių sistemą kartu su pensijine. Dėl emigracijos ir gyventojų senėjimo mažėja atlyginimų fondas, o tada ir pensijinis fondas, juk pensijos formuojasi iš ekonomiškai aktyvių gyventojų atlyginimų mokesčių.

Lietuvos ekonomiškai aktyvūs gyventojai daugiausiai pluša Anglijoje ir Airijoje — dėl to galų gale ir atsiranda pensijinio fondo deficitas. Lietuvos valdžios seniai pripažino šios problemos egzistavimą. 2016 metais Lietuvos Respublikos Socialinės apsaugos ir darbo ministerija paskelbė, jog, atsižvelgiant į Lietuvos demografines prognozes, artimiausiais 1,5–2 dešimtmečiais nuo 2020 metų lietuviškosios pensijos greičiausiai sudarys ne daugiau 24 procentų vidutinio šalyje uždarbio. O besitęsiant gyventojų skaičiaus mažėjimui pensijų dydis, lyginant su vidutiniu uždarbiu, dar labiau mažės.

Ši problema būdinga ne tik Lietuvai, bet ir visoms Pabaltijo šalims, nes demografiniai procesai jose vyksta vienodi. Pasak demografų prognozių, 2040 metais nedarbingų pasenusių gyventojų dalis sudarys: Estijoje — 40, Latvijoje — 43, Lietuvoje — 42 proc.

Pabaltijo respublikos taps senelių prieglaudomis, kurios nepajėgs tokiame pavidale egzistuoti: jų ekonomika neatlaikys tokios socialinės apkrovos, kaip pensijų išmokėjimas sąlygomis, kai vienam pensininkui tenka vienas dirbantysis.

Prieš du metus informacijos agentūra LETA, britų tyrimų kompanija Oxford Research ir latvių kompanija Firmas.lv paskelbė bendrus Latvijos mokesčių sistemos tyrimų rezultatus. Jų pagrindinė išvada: dėl kritiško gyventojų skaičiaus mažėjimo mokesčiai Latvijoje pastoviai didės.

Žvelgiant į šalies demografinę situaciją, darosi aišku, kodėl mokesčių didinimas neišvengiamas. Gyventojų, tai yra dabartinių ir būsimųjų mokesčių mokėtojų, skaičius tebemažėja. Tačiau siekiant palaikyti šalį su jos infrastruktūra, keliais, mokyklomis, ligoninėmis ir t.t. neturi mažėti proporcionaliai gyventojų skaičius, jis turi didėti, nes būtina kompensuoti infliaciją ir tenkinti augantį poreikį kokybinėms valstybės paslaugoms, — rašo Oxford Research analitikai.

Ir gyvenimas jau patvirtino britų analitikų prognozes. Lietuvos premjero Skvernelio paskelbtos struktūrinės reformos — mokesčių didinimas, siekiant užlopyti pensijinio aprūpinimo finansines skyles.

O siekdama pasaldinti savo piliečiams tabletę, pajamų mokesčio didinimą mažiausiai 6 proc., akcizų didinimą ir nekilnojamojo turto apmokestinimą vyriausybė vadina progresyviomis priemonėmis, kurios pavers Lietuvos ekonomiką labiau konkurencinga, pagerins Lietuvos ekonominį įvaizdį pasaulyje ir leis kiekvienam lietuviui uždirbti keliom dešimtim eurų daugiau, nei jis uždirba dabar.

Keliais žodžiais tariant, tai dar viena pabaltijietiška „sėkmės istorija“.

Tokios pat „sėkmės istorijos“, kai siekiant padengti pensijinį deficitą bus didinami mokesčiai, neišvengiamai laukia ir Latvijos su Estija.

Ir vienkartiniu mokesčių didinimu ši problema išspręsta nebus.

Ši priklausomybė veikia ir atgaline kryptimi: kuo labiau didės mokesčiai, tuo mažiau Pabaltijyje liks darbingų gyventojų. Todėl kad gyventojai nesikreips į būrėją, jie nepakeliamą mokesčių naštą nusimes emigravę iš tos šalies, kurioje pusė gyventojų taps socialiniais išlaikytiniais.

Ištrūkti iš to užburto rato įmanoma tik sustabdžius katastrofišką pabaltijiečių depopuliaciją. O sustabdyti ją gali pavykti tik užkirtus kelią emigracijai.

Bet ar pajėgi Pabaltijo politinė klasė pripažinti, kad „Baltijos kelias“ tapo aklaviete ir atvedė jų šalis prie sisteminės krizės ir visiško išnykimo grėsmės? Retorinis klausimas. Nepajėgi.

Pabaltijo politikai lengviau panaikins senatvės pensijų institutą, nei pripažins, kad jų šalys nėra sėkmingo vystymosi pavyzdys. Ir tai ne perdėjimas. Lietuvos Socialinės apsdaugos ir darbo ministras Linas Kukuraitis jau pareiškė, kad vienu iš pensijų gavimo šaltinių gali būti privatūs pensijiniai fondai, kuriuose žmonės turėtų kaupti senatvei savarankiškai. „Mūsų gyventojai turi pakankamai lėšų, kad jų dalį atidėtų ateičiai“, — lietuvių finansinėmis galimybėmis tiki Kukuraitis.

Kitas žingsnis šiuo keliu — palikti privačius pensijinius fondus kaip vienintelį pensijinio aprūpinimo šaltinį. Tegul žmonės taupo ir patys išmoka sau pensijas, o valstybė jiems nieko neskolinga.

Šiai „pensijinei reformai“ (kaip visada, labai progresyviai ir paverčiančiai ekonomiką labiau konkurencinga) reikia tik pritaikyti tinkamą ideologinę bazę.

Pavyzdžiui, pasakyti, kad pensijos iš valstybės biudžeto yra „sovietinė atgyvena“ ir „okupacijos palikimas“ — tai, ką šiuolaikinės, europietiškos ir progresyvios Pabaltijo šalys privalo įveikti.

Taip bus sulaukta dar vienos „sėkmės istorijos“.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 16 — id: `scraped:rubaltic_lt:8006df1f836df1d4`

**Title:** Dalia Grybauskaitė sukritikavo savo prezidentavimą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos prezidentė Dalia Grybauskaitė paskutinį kartą, būdama šiose pareigose, perskaitė Seimui kasmetinį pranešimą. Dešimtaisiais prezidentavimo metais Grybauskaitė atrado „neregėtą Lietuvą“, iš kurios bėga žmonės, nes joje viešpatauja godumas, gobšumas ir korupcija. Tokį „atradimą“ būtų galima skelbti pradedant dirbti šiose pareigose, nes baigiantis antrajai prezidentavimo kadencijai atsakyti už apgailėtiną situaciją Lietuvoje privalo tik valstybės vadovas. Taip kad Jos Didenybė atsisveikinimo pranešime sukritikavo savo valdymo rezultatus.

„Iš vienos pusės, mes matome įspūdingą Laisvės kūrinį, kurio progresas stebina pasaulį, kuriuo ir mes didžiuojamės, kuris mažiau nei per tris dešimtmečius pavertė Lietuvą savarankiška valstybe. Iš kitos pusės, iš politinių užkulisių į valstybės pamatus skverbiasi godumo ir nepasitikėjimo kirminas, verčiantis žmones svetur ieškoti teisingumo ir geresnio gyvenimo“, — papasakojo Dalia Grybauskaitė Seimo nariams apie prieštaringus jausmus, aplankančius ją mąstant apie Lietuvą.

Dešimtaisiais savo prezidentavimo metais Grybauskaitė atrado „neregėtą Lietuvą“. Tai Lietuva, kurioje „viską aptemdo ir kėsinasi į valstybę bei demokratiją ciniškas apskaičiavimas. Kur apstu godžių, klastingų, demoralizuotų glemžikų, nematančių valstybės. Kur suprantama tik šantažo, melo ir grasinimų kalba, o įtakojimas ir poveikis — einamiausia prekė“, — pasakė valstybės vadovė, kuriai pavaldūs teisėsaugos organai ir kuri devynerius metus turėjo savo rankose valdžią, galėjusią keisti Lietuvą teigiama linkme.

„Neregėtą Lietuvą“ Jos Didenybė atrado, žinoma, todėl, kad viešumon iškilo korupcijos skandalas, liečiantis koncerną MG Baltic. Ir kaip visada ponia prezidentė kalba taip, lyg ji su tais skandalais neturėtų nieko bendro, kas, švelniai tariant, netiesa. Paskutinieji skandalai kaip tik parodė, jog ponia Dalia — aktyvi žaidėja tų politinių užkulisių, kurių ji kratosi ir kuriuos kritikuoja.

Triukšmingiausias skandalas, susietas su MG Baltic, — asmeninis prezidentės Grybauskaitės susirašinėjimas su buvusiu Liberalų sąjūdžio lyderiu Eligijum Masiuliu, kuris kaltinamas gavęs iš MG Baltic kyšį.

Sprendžiant iš to susirašinėjimo, Masiulis buvo koncerno ir valstybės vadovės tarpininkas. Per jį Grybauskaitė kontaktavo su MG Baltic, reikalavo „nutildyti“ koncernui priklausančio televizijos kanalo žurnalistą ir, atsakant į palaikymą, suteikti jai kitus malonumus. Taip kad apie Lietuvą graužančią korupciją prezidentė kalba žinodama reikalo esmę.

Dabartinis Dalios Grybauskaitės pranešimas — įspūdingas paminklas jos epochai Lietuvos istorijoje, o taip pat pačiai valstybės vadovei.

Todėl aš galiu kritikuoti visus, o mane kritikuoti negali niekas. Lietuvos politiką visiškai persmelkė korupcija, tačiau aš, esanti tos politikos epicentre, nekalta ir švarutėlė kaip gėlytė. Lietuvos piliečiai nusivilia savo valstybe ir išvažiuoja, tačiau aš, valstybės vadovė, kuo dėta?

„Atsiranda vis daugiau politinės valios fundamentaliais nacionalinio saugumo klausimais. Priekines valstybės gynimo linijas papildo žurnalistų tyrimai, vidiniai judėjimai jau atsiranda mokyklose, ligoninėse, socialiniuose tinkluose“, — sako Grybauskaitė apie tai, kaip pilietinė visuomenė kyla ginti valstybės nuo korupcijos ir prekiavimo įtaka.

Tačiau kaip šios nuostabios Lietuvai tendencijos šviesoje atrodo pati Dalia Grybauskaitė? Jos Didenybė kontroliuoja Saugumo departamentą, prokuratūrą, teismus, kasmet slelbia karą valdžios oligarchams, o lietuviai baigiantis jos prezidentavimui priversti galvoti kaip mokyklų, ligoninių ir socialinių tinklų lygyje kovoti su korupcija.

Lietuvos politikai prieš netolimą ponios Dalios išėjimą iš Daukanto aikštės tapo drąsesni ir pripažino akivaizdų faktą: ta Lietuva, kurią sukūrė Grybauskaitė, negeriausia pasaulyje vieta.

Europarlamento deputatas Valentinas Mazuronis pareiškė, kad ponia prezidentė nepasakė Seimui svarbiausio dalyko: Lietuvoje viešpatauja baimės ir persekiojimo atmosfera, o teisėsaugos organai ir specialiosios tarnybos pasitelkiamos užkulisio žaidimams. Toks kasdieninis gyvenimas tos Lietuvos valstybės, kurią sukūrė ir kuriai devynerius metus vadovauja Lietuvos Respublikos prezidentė Dalia Grybauskaitė“, — sako Mazuronis.

„Svarbiausios Lietuvos problemos pranešime iškeltos aiškiai — tai didžiulė priešprieša ir šalies viduje, ir užsienio politikoje. Būtent tai aš laikau didžiausiu pavojumi mūsų valstybei: Lietuvoje su verslu susipriešino dirbantys gyventojai, išvykę — su likusiais, pacientai — su gydytojais, mokytojai — su mokiniais, miestas — su kaimu, gerovė — su saugumu“, — taip Grybauskaitės pasisakymą komentavo buvęs Lietuvos užsienio reikalų ministras ir Europos Sąjungos ambasadorius Rusijoje Vygaudas Ušackas.

Jis nepraleido progos mesti akmenuko į dar dirbančios valstybės vadovės daržą: „Siekiant įveikti priešpriešą, reikia pasitelkti valią ir tikėjimą, reikia vadovų, kurie vienytų, o ne skaldytų, kurie būtų teisingi visiems ir galėtų su visais kalbėtis. Ir pačioje šalyje, ir užsienio politikoje“.

Šios frazės potekstę supranta bet kuris Lietuvos pilietis: visi žino, kas šalyje mėto nesantaikos intrigų ir rietenų sėklas ir užsienio politikoje pykstasi su kaimynais.

Prie Grybauskaitės gyventojų skaičius sumažėjo lyg po maro — istorijoje tai svarbiausias jos prezidentavimo rezultatas. Toks rezultatas ir lydės prezidentę istorijoje.

Maro Dalia — tinkamiausias titulas valdovei, prie kurios iš šalies išbėgo šimtai tūkstančių gyventojų. Tai svarbiausia, ir tai istorijon įrašys „Grybauskaitės epocha“.

Istorija — teisinga ponia: ji ne tik viską pavadins savo vardais, bet ir įvardins atsakingus už tai, kas nutiko Lietuvai.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 17 — id: `scraped:rubaltic_lt:c7f447c24f4bda7a`

**Title:** ČŽV kalėjimas atėmė iš Lietuvos teisę kalbėti apie žmogaus teises

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Europos žmogaus teisių teismas pripažino, kad Lietuvoje veikė slaptas ČŽV kalėjimas, ir įpareigojo Lietuvos Respubliką išmokėti kompensaciją Palestinos piliečiui, kuris buvo neteisėtai kalinamas ir kankinamas netoli Vilniaus. Ši teismo nutartis deda riebų kryžių ant Lietuvos valdžių ambicijų būti europietiškų vertybių propaguotojais potarybinėje erdvėje: kiekvieną kartą, kai Lietuvos emisarai pradės mokyti „atsilikusius“ rytų kaimynus demokratijos ir žmogaus teisių, jiems bus galima priminti, kad jų šalyje, XXI amžiuje, valdžioms žinant, žmonės buvo kankinami slaptame kalėjime.

„Teismas priėjo išvados, kad Lietuvoje nuo 2005 metų vasaros iki 2006 metų kovo veikė slaptas ČŽV kalėjimas, kad jame buvo kalinamas ponas Zain al-Abidin Mochamed Chusain, o vietos valdžios žinojo, kad ČŽV elgiasi su juo taip, kaip uždrausta konvencijos“, – sakoma Europos žmogaus teisių teismo nuosprendyje, paskelbtame tiriant ČŽV slaptų kalėjimų Europoje bylą.

Teismas įpareigojo Lietuvą išmokėti Palestinos piliečiui Zain al-Abidin Mochamedui Chusainui (labiau žinomam kaip Abu Zubaida) 130 tūkstančių eurų kompensaciją už tai, jog, žinant Lietuvos valdžioms, jis buvo kankinamas slaptame kalėjime.

Teismas paskelbė, kad Lietuvos Respublika pažeidė Europos žmogaus teisių konvenciją, kuri draudžia kankinimus ir neteisėtą įkalinimą, garantuoja nekaltumo prezumpciją ir veiksnę teisinę gynybą.

O dar Europos žmogaus teisių teismas pažymi, kad Lietuva ne tik suteikė JAV teritoriją neteisėtam kalėjimui, bet ir pro pirštus žiūrėjo į tai, kaip amerikiečiai jame užsiiminėja kankinimais.

Oficialus Vilnius tyliai pripažįsta kaltinamąjį nuosprendį savo adresu. Lietuvos prezidentė Dalia Grybauskaitė pavadino Teismo nuosprendį nepalankiu Lietuvai, tačiau pažadėjo jį įvykdyti. Situacijos pikantiškumas slypi tame, jog Lietuvos valdžios visus tyrimų apie slaptus kalėjimus metus atsisakinėjo bendrauti su tyrėjais.

Istorija, kurios eilinis etapas užsibaigė Strasbūre gegužės 31d., tęsiasi pusantro dešimtmečio – nuo 2004 metų, kai į vakarų spaudą pradėjo prasiskverbti informacija apie slaptų ČŽV kalėjimų egzistavimą sąjunginėse JAV šalyse. Tame tarpe labiausiai proamerikietiškose Rytų Europos šalyse – Rumunijoje, Lenkijoje, Lietuvoje.

2009 metais amerikiečių televizijos kanalas ABC News papasakojo apie ČŽV kalėjimo veiklą Lietuvoje.

Lietuvos prezidentas Valdas Adamkus kategoriškai atmetė kaltinimus, pareikšdamas, kad jokių ČŽV kalėjimų Lietuvos teritorijoje nebuvo. Kalėjimo egzistavimą Adamkus neigia iki šiol, ir tai nenuostabu: tokios paskirties įstaiga Lietuvoje galėjo atsirasti tik sutikus tuometiniam šalies vadovui, todėl buvęs prezidentas tiesiogiai atsakingas už šį nusikalstamą veiksmą.

Dabartinė prezidentė Dalia Grybauskaitė 2005 – 2006 metais dirbo Briuselyje eurokomisare ir su įsteigimu prie Vilniaus ČŽV kalėjimo neturi nieko bendro. Todėl prezidento rinkimuose 2009 metais Grybauskaitė dosniai svaidėsi pažadais ištirti šią skandalingą istoriją ir nubausti kaltuosius.

Tačiau tapusi prezidente ji pradėjo „sukti uodegą“, nes kaltieji – dešinysis konservatoriškas Lietuvos elitas, su kuriuo ponią Dalią sieja glaudūs ryšiai, o taip pat JAV atstovai Lietuvoje, prieš kuriuos prezidentė ir žodžio nedrįsta ištarti. Todėl Grybauskaitė ir „suko uodegą“, ir daugelį metų įtikinėjo negalinti tiksliai pasakyti, ar buvo Lietuvoje ČŽV kalėjimas.

O tuo tarpu įrodymų gausėjo. 2011 metais portalas Wikileaks paviešino diplomatinį susirašinėjimą, kuriame JAV valstybinių struktūrų darbuotojai aptarinėjo ČŽV kalėjimo Lietuvoje veiklą.

2015 metais Amerikos Kongresas atnaujino slaptųjų kalėjimų užsienyje programų parlamentinį tyrimą, ir jame nuskambėjo žodis „Lietuva“.

2016 metais į Europos žmogaus teisių teismą kreipėsi Palestinos pilietis Abu Zubaida, kurį JAV valdžios kaltino 2001 metų rugsėjo 11d. teraktų paruošimu. Zubaida pareiškė, jog 2006 metais jis buvo pervestas į slaptą ČŽV kalėjimą Lietuvoje, kuriame buvo kankinamas, siekiant išgauti norimus parodymus.

Ir štai nuosprendis. ČŽV kalėjimas buvo ir Lietuva kalta pagal visus kaltinimo punktus. Ji pažeidė fundamentalias žmogaus teises, leisdama neteisėtai paversti žmogų belaisviu ir jį kankinti, vėliau bandant nuslėpti šį faktą.

Daug metų Lietuvos politikai, žinoma, visų pirma dešinieji, artimi buvusiam prezidentui Adamkui, leidusiam įsteigti ČŽV kalėjimą, neįsivaizdavo savęs be šios misionierių veiklos. Jų pamokslai apie žmogaus teises skambėjo Minske, Tbilisyje, Kišiniove ir Kijeve.

Oficialusis Vilnius ragino įvesti sankcijas prieš Baltarusiją, „paskutiniąją diktatūrą Europoje“ už tai, jog ši esą pažeidžia žmogaus teises. Lietuvos URM visose tarptautinėse erdvėse siekė visiškos Rusijos diplomatinės izoliacijos — „atstumtosios šalies“, kuri „eina prieš bendražmogiškasias vertybes“.

Lietuvos valdžios pro pirštus žiūrėjo, kai Gruzijoje, valdant jų numylėtajam Saakašviliui, buvo pasodintas kas dešimtas šalies gyventojas, tačiau atidarė Vilniuje Baltarusijos žmogaus teisių namus, kurie pagrindinai siekia neleisti pasodinti kalėjiman baltarusių radikalius nacionalistus,dalyvavusius gatvių riaušėse ir valstybinių pastatų Minske užgrobime.

Jie pritarė visiems Kijevo režimo nusikaltimams prieš Ukrainos liaudį ir tarptautinę humanitarinę teisę bei žmogiškumą, užtat užtvindė Vilnių Rusijos „teisėsaugininkais“, laisvosios Rusijos forumuose aptariančiais Putino „kruvinojo režimo“ žmogaus teisių pažeidimus ir sprendžiančiais į kiek dalių vardan laisvės ir demokratijos reikėtų suskaldyti Rusiją.

Ir dabar šį faktą patvirtino Europos žmogaus teisių teismas, pripažinęs Lietuvą kalta pažeidžiant tas žmogaus teises. Tas Teismo sprendimas toli gražu ne pirmas, tačiau svariausias įrodymas, kad metas padėti riebų tašką Lietuvai vaidinant mesiją.

Ir jei ateityje kuris nors oficialus ar neoficialus Lietuvos Respublikos atstovas bandys išsižioti ir ką nors leptelti apie kovą buvusiose tarybinėse respublikose už laisvę ir prisilaikymą žmogaus teisių, jam iškart teks priminti apie slaptą ČŽV kalėjimą prie Vilniaus ir pasakyti: tau metas stipriai prikąsti liežuvį.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 18 — id: `scraped:rubaltic_lt:c3445898240f6a24`

**Title:** Dalia Grybauskaitė — „sovietinė“ vadovė blogiausia šio žodžio prasme

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Slaptas Dalios Grybauskaitės susirašinėjimas, kuriuo ji bando savo naudai įtakoti parlamento darbą ir reikalauja „užčiaupti“ neįtikusį žurnalistą, pagimdė buvusių ponios prezidentės bendražygių atviravimų srautą apie „Pabaltijo geležinės ledės“ valdymo stilių. Grybauskaitė kaltinama autoritarizmu ir intrigantiškumu. Lietuvos prezidentė pastoviai demonstruoja blogiausius išeivės iš vėliausios tarybinės nomenklatūros bruožus: grubumą, neprincipingumą, piktnaudžiavimą tarnybine padėtimi, pataikavimą santykiuose su viršininkais ir įžūlumą pavaldinių atžvilgiu.

Lietuvą jau ne vieną savaitę drebina skandalas dėl slapto prezidentės Dalios Grybauskaitės susirašinėjimo su buvusiu Lietuvos liberalų sąjūdžio lyderiu Eligiju Masiuliu, kuriam iškelta baudžiamoji byla dėl kyšio paėmimo, paviešinimo.

Iš susirašinėjimo matosi, kad Grybauskaitė per Masiulį daug bendravo su koncernu MG Baltic — generaliniu Lietuvos liberalų rėmėju. Gavimu iš MG Baltic didžiulio kyšio Masiulis kaip tik ir kaltinamas. Kai 2016 metais ties Liberalų sąjūdžiu įsiplieskė skandalas, Lietuvos prezidentė garsiausiai reikalavo pribaigti politinę korupciją ir atriboti šalies valdžią nuo oligarchų įtakos.

Viename laiške Grybauskaitė pranešė liberalų lyderiui, kad Seime ketinama sudaryti komisiją, kuri „tirtų teisėsaugos organų spaudimą“, patikslino, jog „pagal formuluotę“ tai nukreipta prieš ją, ir prašė draugiškos frakcijos užkirsti tam kelią.

Kitame laiške ponia Dalia reikalavo „užčiaupti“ MG Baltic televizijos žurnalistą Tomą Dapkų, kuris kritikavo prezidentės kandidatą į Lietuvos generalinio prokuroro postą.

Grybauskaitė stengiasi išsikabarnoti iš ją palietusio skandalo jai įprastu būdu. Išsisukinėja, sako, kad jos laiškai ne taip suprasti, kad ji visom keturiom už žodžio laisvę, su MG Baltic kontaktavo tikslu apsaugoti juos nuo įsivėlimo į politiką ir korupciją, o tai, kas vyksta dabar, — oligarchų sąmokslas prieš prezidentę už tai, jog ji tik viena su jais kovoja.

Tačiau sausai atsikelti iš balos Grybauskaitei nepavyksta: jos pasiteisinimai skęsta vis naujų kaltinimų srautuose.

Tas pats Tomas Dapkus, kurį, susirašinėdama su Masiuliu, prezidentė vadino „skaliku“ ir reikalavo jį „patvarkyti“, paaštrino skandalą tuo, kaip Grybauskaitė į teisėjų ir prokurorų vietas sodina savus žmones, per juos kontroliuoja teismo struktūras ir pjudo neparankią spaudą.

„Kaip liudija buvęs „Lietuvos žinių“ redaktorius, kai aš ten dirbau, jau po kelių mano kritinių straipsnių VSD adresu vadovui biznio grupės, kuriai priklauso laikraštis, paskambino iš Prezidento rūmų ir liepė mane atleisti. Ne išimti straipsnius, ne sustabdyti mane, o atleisti. Prezidento rūmuose dabar pažanga! Po to, kai koncerno prezidentas perdavė reikalavimą redaktoriui, o šis atsisakė tai padaryti, atleisti iš darbo buvome abu“, — rašo Dapkus atvirame laiške Facebook, atsakydamas į atsitiktinai paviešintą VSD pažymą, kurioje žurnalistas vadinamas šantažuotoju, už kurio stovi MG Baltic.

Tuo tarpu buvę VSD vadovai pripažįsta: „atsitiktinis“ pažymos apie Dapkų paviešinimas Grybauskaitės skandalo įkarštyje su jos reikalavimu „sutramdyti“ žurnalistą negali būti sutapimai.

O dar buvęs VSD direktorius Gediminas Grina pastebi, jog istorijoje su MG Baltic Valstybės saugumo departamentas akivaizdžiai viršijo savo įgaliojimus, vykdydamas policijos funkcijas. O kas stovi už VSD? Valstybės vadovė.

Grybauskaitė kėlė balsą prieš kolegas, bėrė įžeidimus, skleidė šmeižikiškus gandus. Lietuviams ši informacija nenaujiena. Visa tai apie prezidentę buvo žinoma anksčiau.

Pakanka prisiminti buvusio premjero Algirdo Butkevičiaus nusiskundimus, jog Grybauskaitė pasakoja pletkus apie korumpuotą jo vyriausybę tiems Vakarų lyderiams, kurie netrukus turi susitikti su Butkevičium.

Arba pasakojimus buvusio Lietuvos prezidento patarėjo Lino Balsio apie tai, kaip Grybauskaitė malšina kritiką savo adresu Lietuvos žiniasklaidoje, tiesiogiai grąsindama jos savininkams.

Arba nuostabią frazę: „... manęs nedomina, ką galvoja ekonomikos ministrė, mane domina, kaip ji vykdo mano nurodymus“.

Arba ceremoniją, kai Rusijos pasiuntinys Aleksandras Udalcovas įteikė jai įgaliojamąjį raštą, o ponia Dalia jį pasitiko žodžiais: „Jūs dar nepaspringote lietuvišku pienu? Aš Jūsų klausiu!“

Taip kad nauji atviravimai tik priminė seną nelabai patrauklių „Pabaltijo geležinės ledės“ asmeninių savybių temą ir savotiškus jos vadovavimo metodus.

Grybauskaitė — partinės nomenklatūros TSRS griūties metu išsigimimo produktas. Joje įsikūnijo tipiniai partinio aparato darbuotojo bruožai sąstingio ir pertvarkos metu. Įstatymų nepaisymas ir piktnaudžiavimas tarnybiniais įgaliojimais kaip „pono teisės“ neatskiriamumas. Autoritarinis santykių stilius su pavaldiniais ir kitais nuo jos priklausančiais žmonėmis. Grubumas. Įžūlumas. Nesiskaitymas su kitokia nuomone. Paniekinantys kreivi žvilgsniai. Pokalbiai pakeltu tonu. Pataikavimas santykiuose su viršininkais: pakanka prisiminti, kokiu įsimylėjusiu žvilgsniu Grybauskaitė lydėjo kiekvieną JAV prezidento Trampo judesį, kai šis tiesiai į akis ją įžeidinėjo, sakydamas, jog „tik visiškai buki žmonės nenori turėti gerų santykių su Rusija“.

Nepriklausomos spaudos bijojimas, veiklos skaidrumas, laisvas bendravimas su žurnalistais. Tuo Jos Didenybė ypač pagarsėjo. Lietuvoje iš televizijos ir spaudos buvo šalinami tyrimai apie tarnybinę ponios prezidentės praeitį, po to Grybauskaitė skandalingai paliko latvių televizijos studiją, kai vedantysis bandė užduoti iš anksto nepatvirtintus klausimus, paskui bėgo nuo rusų filmavimo grupės, kai ši prašė jos komentaro.

„Sovietinę“ Grybauskaitės esmę išduoda viskas: nuo bendravimo su aplinkiniais manieros iki veido išraiškos ir šukuosenos. Jai labiau tinka ne Europos Sąjungos ir NATO vėliavos, o karelų beržo tribūna, ant kurios — grafinas su vandeniu, o už nugaros — raudona vėliava su Iljičiaus biustu.

Tokiose dekoracijose prezidentė ir turi reikštis, o ne klaidinti aplinkinius. Nes Lietuvoje viešpatauja įsisenėjęs karikatūrinis „vatnikas“ ir vadovauja ponia Dalia Lietuvai sovietiniais metodais.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 19 — id: `scraped:rubaltic_lt:6c199c7db9c08201`

**Title:** Lietuvių blogeris: represijos tapo įprastu siautėjančių Lietuvos valdžių ginklu

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Prieš 25 metus, 1993 metų gegužės 14 dieną, Lietuva tapo Europos Tarybos nare. Tai organizacija, kurios tikslas — ginti žmogaus teises ir palaikyti demokratiją. Tačiau po ketvirčio amžiaus Lietuvos Respublika vis labiau primena Šiaurės Korėją. Valdantieji sluoksniai tiesiogine prasme užsiėmė medžiokle žurnalistų, visuomenės veikėjų ir politikų, kurie pasisako prieš valdžias, nurodydami jų akivaizdžius trūkumus, nusikaltimus ir nesėkmes. Taip, pavyzdžiui, už postą Facebook šalyje, kuri yra Europos Tarybos narė, galima dvejiems metams atsidurti kalėjime. Lietuvos įstojimo į šią organizaciją metinių proga analitinis portalas RuBaltic.Ru pasikalbėjo su lietuvių blogeriu Simonu Zagurskiu apie tai, kaip respublikoje laikomasi žmogaus teisių, ypač — žodžio laisvės.

— Pone Zagurski, žiniasklaida pranešė, kad į Lietuvą iš Didžiosios Britanijos Jūs atvykote 2018 metų balandžio mėnesį, buvote septyniom dienom sulaikytas ir dabar negalite išvykti dėl Jums iškeltų baudžiamųjų bylų. Ar Jūs galėtumėte patvirtinti arba paneigti šią informaciją?

— Viskas taip. Iki atvykimo į Lietuvą aš septyniolika metų gyvenau Didžiojoje Britanijoje, kur manęs nepasiekė Lietuvos specialiosios tarnybos. Šių metų sausy Lietuvoje man buvo iškelta baudžiamoji byla, o specialiosios tarnybos gavo leidimą mane areštuoti. Aš to nežinojau, kai skridau į Lietuvą. Aš ketinau praleisti Lietuvoje ne daugiau penkių dienų, bet įstrigau ilgam.

Lietuvos teisėsaugos darbuotojai žinojo, kad baigiasi mano paso galiojimo terminas ir kad aš atvyksiu į Lietuvą jo pakeisti. Aš atskridau, mane areštavo ir įkišo į kalėjimą. O dar iš manęs paėmė dokumentus, kompiuterį, mobilų telefoną ir t.t. Po septynių dienų mane išleido, tačiau neturėdamas dokumentų negaliu išvykti iš šalies.

Dar daugiau — Lietuvoje pasijutau lyg būčiau užsienietis. Be paso mano teisės ženkliai apribotos: kai tenka kreiptis į ligoninę ar oficialiai išsinuomoti būstą, susiduriu su rimtomis problemomis.

— Ar galėtumėte smulkiau papasakoti kaip atsidūrėte tokioje situacijoje?

— Prieš pusantrų metų savo puslapyje Facebook patalpinau postą apie snaiperių dalyvavimą Vilniuje 1991 metų sausio įvykiuose. Tie snaiperiai — lietuviai, kurie kariavo Afganistane. Aš parašiau, kad įvykius Vilniuje organizavo firmos Edelman amerikiečių konsultantai ryšių su visuomene klausimais.

Snaiperiams buvo pažadėta sumokėti po tūkstantį dolerių už nakties darbą. O sumokėjo po du šimtus dolerių. Tie lietuviai, kurie vienaip ir kitaip buvo į tuos įvykius įvelti, sakė, kad kai kurie šauliai nusižudė dėl spaudimo (manoma, jog iš susirėmimų oraganizatorių pusės).

Naktį į 1991-ųjų sausio 13-ąją snaiperiai šaudė nuo pastatų stogų. Aš nežinau, kiek jų ten buvo. Šauliams nebuvo liepta nukauti būtent ką nors, jie turėjo šaudyti į minią. Prieš snaiperius stovėjo Tarybų Sąjungos kariškiai. Ir susirėmimas buvo organizuotas taip, kad užsienio žiniasklaida, o konkrečiai BBC ir CNN, nufilmuotų, kaip tarybiniai tankai esą traiško protestuojančius lietuvius. Taigi tos nakties įvykiai Vilniuje buvo surežisuoti ir žiniasklaidos parodyti pasauliui.

Savo puslapyje Facebook aš parašiau, kad įvykiai Vilniuje buvo apmokėti, o Lietuvos judėjimas „Sąjūdis“ — tai VSK (KGB) projektas.O taip pat kad Lietuvos komunistai po to, kai subyrėjo Tarybų Sąjunga, o JAV pasiūlė jiems pinigų, užėmė amerikiečių pusę.

Dar aš rašiau, kad galimai tarp JAV ir Rusijos egzistavo susitarimas, pagal kurį Pabaltijis turėjo atitekti JAV, Rusijos įtakos zonoje paliekant Artimuosius Rytus. Visa tai buvo suplanuota prieš 25–30 metų.

Žinoma, aš pažymėjau, kad tai tik versija, kad taip galėjo būti.

Mano originalus postas buvo pašalintas iš Facebook. Tačiau grupė chakerių „Jorkširio elfai“, kurią kontroliuoja Lietuvos konservatoriai, sukūrė „feiko“ profilį su mano asmens duomenimis, ten patalpino „feiko“ straipsnį ir pranešė apie jį policijai.

— Kuo Jūs kaltinamas? Kodėl Jūs tapote reikalingas Lietuvos specialiosioms tarnyboms?

— Lietuvos specialiosios tarnybos nori pasinaudoti mano byla parodant užsienyje gyvenantiems lietuviams, kas gali nutikti, jei bus pabandyta parašyti tai, kas prieštarauja oficialiai Lietuvos propagandai.

Šiandien apie milijonas lietuvių gyvena JAV, apie 300 tūkstančių — Didžiojoje Britanijoje, 200 tūkstančių — Norvegijoje ir Švedijoje, 50 tūkstančių — Airijoje.

Šiuo metu Lietuvoje įsiplieskė eilinis skandalas dalyvaujant šalies prezidentei [Daliai Grybauskaitei], kuri įsakė Lietuvos specialiosioms tarnyboms sekti žurnalistus. Manau, jog mano bylos eigą taip pat kontroliuoja Lietuvos prezidentės administracija ir Saugumo departamento vadovybė. Tačiau aš tik patalpinau informacijos nutekėjimą ir parašiau, jog beveik neabejoju informacijos teisingumu.

— Kaip suformuluotas kaltinimas?

— Aš kaltinamas tuo, kad tyčiojuosi iš 1991 metų sausio įvykių Vilniuje Esą nervinu tada nukentėjusius žmones. Tačiau juridiškai susidūrimų sausyje byla vis dar neužbaigta. Paprasčiausiai Lietuvos konservatoriai, kurie suinteresuoti plėsti šalyje rusofobiją, vyriausybės lygyje priėmė nutarimą, kad galvoti ir rašyti apie tuos įvykius neteisėta.

Aš tik paaiškinau įvykių versiją. Už tai mane pavadino „Kremliaus agentu“ ir gali dvejiems metams įkišti į kalėjimą. Visą tą laiką aš negalėsiu ištrūkti iš Lietuvos, o visi mano giminės gyvena Didžiojoje Britanijoje.

— Anglų ar lietuvių kalba Jūs rašėte savo postus?

— Lietuvių. Dar vienas momentas, jis svarbiausias: tai, kas publikuojama Facebook, yra JAV jurisdikcijoje ir vertinama pagal jų įstatymus. Kitaip sakant, Jus negali teisti už Amerikos ribų. Tačiau Lietuvoje tai vyksta.

— Pastaruoju metu Lietuvoje padažnėjo atvejų, kai žmonės areštuojami arba persekiojami politiniais motyvais. Jūsų manymu, ar šie atvejai kažkuo panašūs? Kas daugiausia nukenčia nuo tų persekiojimų?

— Net valdančiosios partijos lyderis buvo apkaltintas ryšiais su Rusija.

Egzistuoja slaptas sąrašas, kuriame — dviejų, o gal trijų tūkstančių lietuvių, gyvenančių JAV, pavardės. Jei jie atvyks į Lietuvą, gali būti areštuoti, kaip ir aš. Šiandien šalyje asmens duomenys menkai saugojami. „Jorkširio elfai“ turi ryšius su bankais, registracijų biurais ir kitomis įstaigomis. Šie ryšiai padeda chakeriams gauti informaciją apie biznį, nekilnojamą turtą ir t.t.

Oficiali spauda tai nutylėjo. Ir tai nenuostabu, nes Lietuvos prezidentė kontroliuoja spaudą, teismus, prokuratūrą ir kariškius. Dauguma lietuvių norėtų normalių santykių su Rusija, Baltarusija ir lietuviais, kurie gyvena Anglijoje ir JAV.

— Lietuvoje persekiojami politikai, žurnalistai, visuomenės veikėjai. Ar tai tos pačios grandinės grandys?

— Būtina suprasti, kad Lietuvą šiandien valdo mafijos grupė. Tai nedidelė grupė Lietuvos konservatorių partijos žmonių, kuriuos palaiko apie 12 procentų gyventojų ir kuri kontroliuoja žiniasklaidą, kariškius, teismus, policiją ir kitas jėgos struktūras. Visi šie žmonės — buvę VSK (KGB) agentai ir šnipai. Jeigu jūsų pozicija kertasi su šios mafijos pozicija, jūs automatiškai tampate „Kremliaus agentas“.

Neabejoju, Rusija lengvai galėtų pateikti šios grupuotės narius kompromituojančią medžiagą. Suprasdami grėsmę, visus kaltinimus savo adresu konservatoriai vadina „feikais“. Tačiau su šia įtakos grupe siejasi labai keisti dalykai.

Prieš dvejus metus Lietuvos karinės išlaidos sudarė 0,7 šalies BVP proc. Šiandien — jau 2 proc. Artimiausioje ateityje jos, atrodo, padidės iki 2,5 proc., nes baiminamasi „rusų agresijos“.

O tuo metu Amerika ir Vokietija parduoda Lietuvai pasenusią ginkluotę, o ši ją perduoda Ukrainai. Lietuva padeda Ukrainai kariauti Donbase, faktiškai tapo jos kariuomenės rėmėja. Lietuvos kalėjimai tuo metu baisiame stovyje, atlyginimai ir pensijos labai menki. Tačiau jei tu apie tai parašysi, lengvai atsidursi tardytojų kabinetuose, o gal ir kalėjime.

Prieš keletą dienų buvau tardomas pagal vieną iš bylų. Žurnalistas — VSK agentas tarybiniais metais lydėjo Kauno Žalgirio krepšininkų komandą ir dirbo kaip šnipas. Visi apie tai žinojo. Tačiau dabar šis žmogus žiauriai proamerikietiškas. Jis kalba, jog nieko nežino, nekenčia Rusijos ir panašiai. Aš patalpinau informaciją ir buvau iškviestas į teismą kad prisipažinčiau, jog šis žurnalistas nebuvo VSK agentas.

Netrukus Lietuva sulauks dar vieno skandalo. Į ją įvelta šalies prezidentė. 2,4 tūkstančių lietuviškų pasų buvo parduota Pietų Afrikos žydams, kurie niekada nebuvojo Lietuvoje ir nemoka lietuvių kalbos. Esą už tai Lietuva sulauks Izraelio paramos.

— Kokiu tikslu tuo užsiiminėja konservatorių partija?

— Juos remia tam tikri JAV sluoksniai, Lietuvos konservatoriai veikia pagal tų grupių interesus. Pėdsakai greičiausiai veda prie Chilari Klinton būstinės. Aš manau, jog konservatorius kontroliuoja Klinton asmenys. O Trampo Lietuvos konservatoriai nekenčia.

Šios grupės misija — užsiimti antirusiška, antibaltarusiška ir antilenkiška politika. Jie norėtų Lietuvoje sukurti režimą, panašų į buvusį Albanijoje prieš trisdešimt metų, ir kontroliuoti dirbančią Lietuvos vyriausybę.

Straipsniai, pagal kuriuos mane areštavo, kaip tik apie tai kalba. Konservatorius remia didelis biznis. Dirbančią vyriausybę palaiko visuomenė, tačiau ji pastoviai patiria spaudimą ir neįtakoja daugelio šalies gyvenimo sferų — pagrindinai dėl korupcijos.

Juokingiausia, kad Vakarų verslininkai norėtų gerų Lietuvos ir Rusijos santykių. Pavyzdžiui, dėl rusų embargo lietuvių eksportas ženkliai sumažėjo, nors Lietuvai būtų naudinga bendradarbiauti su Rusija.

Ta pati istorija su SGD terminalu. Lietuva nuomoja laivą ir perka Amerikoje dujas, kurios išgaunamos Bachreine arbo Saudo Arabijoje. Rusija galėtų parduoti Lietuvai dujas daug pigiau. Tačiau dėl politinių motyvų lietuviai permoka du ar net tris kartus daugiau.

Konservatoriai tvirtina, kad Lietuva turi remti Ukrainą ir užsiiminėti antirusiška propaganda. Ir tuo metu tūkstančiai Ukrainos vairuotojų ir statybininkų dirba Lietuvoje. Visi šie žmonės kalba, kaip žinia, ne lietuviškai, o rusiškai. Ir tai tiesiog juokinga.

Į Lietuvą atvažiuoja žmonės iš taikių Ukrainos regionų ir susiduria su valstybine pagalbos „nukentėjusiems kare“ programa. Šioms reikmėms Briuselis skiria pinigus. Tuo metu Lietuvos politikai atidaro ofšorus, per kuriuos pagalba „nukentėjusiems“ ukrainiečiams plaukia į reikalingas kišenes.

— Ar pasikeis Lietuvoje situacija po prezidento rinkimų?

— Ne. Valdančioji Lietuvos grupuotė — mafija. Ji nepaiso įstatymų, o jos tikslas — visiškai kontroliuoti Lietuvą. O pati šalis jiems nėra labai svarbi.

Ką nors pakeisti gali tik tie lietuviai, kurie gyvena užsienyje. Jie publikuoja informacijas apie korupciją ir nori sustabdyti rusofobiją, kad būtų atkurti santykiai su Rusija, Baltarusija ir kitais Lietuvos kaimynais. Deja, alternatyvi lietuviška žiniasklaida šiomis sąlygomis galima tik užsienyje, kur jos pasiekti negali Lietuvos specialiosios tarnybos.

Pavyzdžiui, mano publikacijos kokia tai prasme įtakoja Lietuvos politiką. Kai aš parašiau apie korupcijos skandalą: Lietuvos valdininkai vogė ES pinigus, — daugelis pareigūnų turėjo atsisveikinti su šiltomis vietelėmis, o kai kuriems išvis buvo uždrausta dirbti valstybinėse struktūrose.

— 1993 metų gegužės 14 dieną Lietuva tapo Europos Tarybos nare — organizacijos, kurios tikslas ginti žmogaus teises, remti demokratiją ir t.t. Jūsų nuomone, ar dabartinė Lietuva prisilaiko Europos Tarybos bazinių principų ir idėjų?

— Žinoma, ne. Dabartinė Lietuva neprisilaiko jokių normų ir taisyklių.

Lietuvoje egzistuoja režimas, primenantis stalininį. Šalis išmoka didžiules kompensacijas ir baudas šio režimo aukoms, kai Strasbūro teismas priima nutartis ne valstybės naudai. Lietuva atiduoda mokesčių mokėtojų pinigus.

— Ar tai reiškia, kad Vakarų šalys nenori matyti žmogaus teisių pažeidimų Pabaltijyje, nes nenori prarasti tų pranašumų, kuriuos gauna respublikose? Kodėl nesimato oficialios Vakarų pozicijos?

— Pirma, todėl, kad nuslepiami pažeidimų faktai. Paprasčiausiai žmonės sėdi kalėjimuose, o kartais sistema visiškai jų atsikrato. Retkarčiais žurnalistai užmušami arba dingsta be pėdsako.

Dažniausiai žmonės atsiduria pas tardytojus ir sumoka didžiules, nepakeliamas baudas. Po to jiems siūloma atgailauti. Jeigu sutinka, jie paliekami ramybėje.

— Jūsų manymu, ar artimiausioje ateityje gali pasikeisti situacija?

— Tokia galimybė egzistuoja. Reikėtų, kad vyriausybė kontroliuotų prokuratūrą, kariškius ir teisėjus. Tačiau vargu ar jai tai pavyks.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 20 — id: `scraped:rubaltic_lt:f08fba2de5553d7a`

**Title:** Pabaltijis Europos Sąjungoje. Nedžiuginantys rezultatai

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Prieš 14 metų, 2004 metų gegužės 1d., Lietuva, Latvija ir Estija įstojo į Europos Sąjungą. Europietiška integracija Pabaltijo šalių vadovybėms matėsi kaip istorinio vystymosi viršūnė ir atsidūrimas Dievo karalystėje, kurioje Lietuvos, Latvijos ir Estijos laukė vien tik gerovė ir suklestėjimas. Realybėje viskas susiklostė kitaip: būdamas ES sudėtyje Pabaltijis tapo degraduojančia Europos periferija su mirštančia ekonomika ir išsilakstančiais gyventojais.

1.      Gyventojai

Prognozės, jog narystė ES paskatins darbingų gyventojų emigraciją iš Lietuvos, Latvijos ir Estijos į Vakarų Europą, ne tik pasitvirtino, bet ir tapo per daug „optimistinės“.

Po įstojimo į Europos Sąjungą ir gavimo teisės laisvai keliauti Europa Pabaltijo šalis paliko kas penktas gyventojas. Krizės metu su Lietuva per keletą metų atsisveikino virš 150 tūkstančių žmonių, su Latvija — virš 100 tūkstančių. Tačiau ir po dalinio ekonomikos lygio pakilimo po krizės emigracija tebetęsiasi — Lietuvos gyventojų skaičius per metus sumažėjo 1,5, Latvijos — 1 proc.

Estų kalbą šiandien vartoja mažiau nei milijonas žmonių. Latvijoje gyvena vos virš milijono latvių. Jauni lietuviai, latviai ir estai masiškai atsisveikina su savo šalimis, užsienyje sukuria šeimas, atsisako sugrįžti į Pabaltijį, o jų palikuonys jau nemoka protėvių kalbos ir nesijaučia baltų tautų dalimi.

2.      Ekonomika

Europietiška integracija sunaikino atskiras Lietuvos, Latvijos ir Estijos nacionalinių ekonomikų šakas, o patirtus nuostolius Pabaltijo šalims Briuselis nekompensavo.

Europos Sąjunga privertė Lietuvą uždaryti stambiausią statybų metu pasaulyje Ignalinos AE.

Latvija, Briuseliui spaudžiant, buvo priversta atsisakyti cukraus gamybos ir uždaryti visus cukraus fabrikus.

Dėl europietiškų kvotų žvejybai ir žvejybinės pramonės apimčių apribojimų Baltijos jūroje teko pasmerkti Pabaltijo šalių žvejybinį laivyną supjaustymui metalo laužui.

Viso to išdavoje dėl narystės ES Pabaltijo šalys beveik prarado savo ekonomiką. Pabaltijo šalys Europos Sąjungoje nėra ekonomiškai savarankiškos ir gyvuoja dėka ES fondų, suteikiančių „dirbtinį kvėpavimą“.

3.      Europos fondai

Atsilygindama už gamybos apimčių mažinimą ir realios ekonomikos sunaikinimą Europos Sąjunga nukreipė į Pabaltijį struktūrinių ES fondų dotacijų srautą. Dotacijos turėjo „išlyginti“ Pabaltijo ekonomikas ir pakelti Lietuvą, Latviją bei Estiją iki vidutinio Europos Sąjungos ekonominio išsivystymo lygio.

Šiandien Europos fondai duoda Pabaltijo šalims 3 procentus BVP augimo – be dotacijų Lietuvos, Latvijos ir Estijos ekonomikos neišsilaikytų. ES struktūrinių fondų dėka dar kruta Pabaltijo žemės ūkis ir statybos sektorius – po to, kai Briuselio pinigų srautas išseks, šių šakų laukia krizė, kuri persimes į visą Pabaltijo šalių ekonomiką.

Pabaltijis jau dabar susiduria sdu finansavimo sutrikimais. Europos komisija atsisako prisidėti prie Klaipėdos SGD terminalo finansavimo, neskyrė lėšų Estijos SGD terminalui ir Visagino AE.

Tačiau po kelerių metų Europos Sąjungos išlyginimo politika gali visiškai išsekti arba pasikeisti ne Pabaltijo naudai. Financial, pavyzdžiui, praneša, jog reformavus finansinės paramos skyrimo sistemą europietiški pinigai iš Rytų Europos bus nukreipti į Graikiją, Italiją ir Ispaniją.

4.      Demokratija ir žmogaus teisė

Kai Lietuva, Latvija ir Estija stojo į Europos Sąjungą, optimistai tikėjosi, jog europietiška integracija pagerins nekokią situaciją, kuri susiklostė šių šalių demokratijoje ir žmogaus teisėse.

Pesimistai atsiliepė skeptiškai: jei Europa pasiruošusi priimti į savo gretas šalis su gėdingu nepiliečių institutu, tai į demokratijos ir žmogaus teisių Pabaltijyje problemas ten nekreipiama jokio dėmesio.

Teisūs buvo pastarieji.

Pabaltijis dabar turi savus politinius kalinius. Kitaip mąstantys ten tampa „sąžinės kaliniais“. Specialiosios tarnybos vardina „liaudies priešus“. Už „tik teisingos“ istorinių įvykių versijos neigimą galima penkeriems metams sėsti į kalėjimą.

Neparankūs žurnalistai ir visuomenininkai sodinami. Neparankūs televizijos kanalai atjungiami. Rusų kalba, kuria kalba trečdalis Latvijos ir ketvirtadalis Estijos gyventojų, neturi jokio oficialaus statuso.

Ir visa ši „demokratija“ gyvuoja po Europos Sąjungos vėliava.

5.      Pragyvenimo lygis

Lietuvoje, Latvijoje ir Estijoje buvo tikimasi, kad po įstojimo į Europos Sąjungą jos pagaliau pradės gyventi kaip Švedija, Danija ir Suomija. Kad pagal pragyvenimo lygį jos pasivys „Senąją Europą“.

Po 14 gyvenimo Europos Sąjungoje metų pagrindinių socialinės gerovės rodiklių skirtumas tarp Pabaltijo ir Skandinavijos su Vakarų Europos šalimis dar labiau paaštrėjo.

Pabaltijo šalys pagal išlaidas gyventojų socialinei apsaugai — Europos Sąjungos antilyderės. Latvijos išlaidos socialinei apsaugai sudaro 14,5 proc. BVP — paskutinė vieta Europos Sąjungoje. Panašiai atrodo ir Lietuva (14,7 proc.) su Estija (15,1 proc.) — priešpaskutinės vietos. Palyginimui, prancūzai socialinei apsaugai skiria 34 proc. BVP, o Danija — jo trečdalį.

Tokiu būdu Pabaltijo šalys praktiškai atsiduria tarp ES šalių visų socialinės gerovės reitingų gale. Jos paskutinėse vietose pagal išlaidas sveikatos apsaugai, socialinei infrastruktūrai, investicijas, socialinių programų finansavimą.

Tačiau Lietuva, Latvija ir Estija pirmauja kituose europietiškuose reitinguose. Juose gyventojų, atsidūrusių už skurdo ribos ir tų, kuriems gresia materialinė ir socialinė atskirtis, skaičius. Pabaltijo šalys pirmauja pagal žudynių ir savižudybių skaičių, alkoholio vartojimo apimtis. Tai liūdnas pirmavimas, tai akivaizdus jų narystės ES rezultatas.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```
