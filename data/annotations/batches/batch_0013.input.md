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

### Article 1 — id: `scraped:rubaltic_lt:013ff3b54d0bd69c`

**Title:** Įvykių prie Vilniaus televizijos bokšto tyrimas verčia abejoti Lietuvos valdžios legitimumu

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuva patenka į politinio nestabilumo zoną, kuri siejama ne tik su artėjančia valdžios kaita, bet ir su sausio 13-osios bylos nuosprendžio paskelbimu akivaizdžiai nekaltiems, tačiau kaltinamiems karo nusikaltimais ir nusikaltimais žmoniškumui Rusijos kariškiams. Susidūrimo 1991 metų sausio mėn. prie Vilniaus televizijos bokšto aplinkybių aptarimas iškelia viešumon vis daugiau parodymų, jog dėl žmonių žudynių kalti judėjimo už nepriklausomybę lyderiai, o tai verčia abejoti Lietuvos valdžios legitimumu.

Šiais metais Lietuva gana kukliai pažymėjo eilines tragiškų 1991 metų sausio 13-osios įvykių metines. Seimo spaudos tarnyba anonsavo ne savaitės priemonių programą, o tik dviejų dienų — sausio 12 ir 13-osios. Nebuvo mokslinės konferencijos, seminaro, kuriame būtų dalintasi kovine priešpastatymo „sovietinei agresijai“ patirtimi, estafetės, vaikų piešinių parodos. Apsiribota atmintinų laužų liepsnojimu, o kitą dieną — iškilmingu vėliavos iškėlimu Nepriklausomybės aikštėje. Jau tradiciškai Seimo salėje buvo įteiktos 2018 metų Laisvės premijos.

Laureatais tapo buvę taip vadinamieji lietuviškieji “partizanai“, šeštame praeito amžiaus dešimtmetyje teisti tarybų valdžios už banditizmą taikių Lietuvos gyventojų atžvilgiu. „Partizanai“ pokario metais sugebėjo barbariškais būdais — sušaudymais, pakariant, sudeginant, žudant kirviais ir pjūklais — sunaikinti daugiau kaip 25 tūkstančius taikių gyventojų, tame tarpe tūkstantį vaikų. Jie buvo nubausti už tai, jog tiesiog sutiko su tarybų valdžia: 90 proc. nukentėjusiųjų buvo lietuviai, kurie norėjo gyventi ir auginti vaikus, be kurių šiandien nebūtų Lietuvos.

Vytauto Landsbergio konservatoriai dar 2017 metais siūlė skirti Laisvės premiją antitarybinio pasipriešinimo Lietuvoje vadams su Jonu Žemaičiu priešakyje. Tačiau tada premija teisėtai už nuopelnus buvo skirta buvusiai tarybinei disidentei Nijolei Sadūnaitei.

Pagerbimas buvusių „miškinių“, kaip pokario metais buvo vadinami Lietuvos „partizanai“, o tiksliau — banditų („miško broliais“ jie buvo pakrikštyti jau pertvarkos laikais), Seimo salėje praėjo blankiai, be ypatingo patoso. Turbūt dėl laureatų kontingento. Bet ne tik.

Priemonių santūrumą galimai įtakojo laukimo atmosfera. 2019 metų gegužės mėn. Lietuvoje bus renkamas naujas prezidentas. Nors Dalia Grybauskaitė ir elgiasi kaip šeimininkė, tačiau supranta, kad ji šioje šventėje tik perpus viešnia.

Vasario 18 dieną Lietuva laukia nuosprendžio, kuris bus neakivaizdžiai paskelbtas 64 buvusiems tarybiniams piliečiams, kurie dalyvavo jėgos akcijoje atstatant TSRS ir Lietuvos TSR konstitucijų galiojimą Lietuvoje. 58 iš jų — Rusijos piliečiai.

Dviem RF piliečiams, Rusijos gvardijos atsargos pulkininkui Jurijui Meliui ir buvusiam tarybiniam pulkininkui Genadijui Ivanovui, nuosprendis bus paskelbtas akivaizdžiai. Ikiteisminį tyrimą baudžiamojoje byloje dėl 1991 metų sausio 13-osios įvykių Vilniaus apygardos teismas vedė dvejus metus ir devynis mėnesius.

Nepaisant to, jog Lietuvos teisėjai, kaip 2015 birželio mėn. savo Facebook taikliai pastebėjo teisėjas Audrius Cininas, „įstatymo įpareigoti veikti kartu su kaltintojais, gynėjams esant bejėgiais“, neverta manyti, jog Vilniaus apygardos teismo teisėjų kolegija sutiks su visais prokurorų pasiūlymais dėl bausmių kaltinamiesiems.

Kai kurie liudytojai ir kaltinamųjų sausio 13-osios byloje advokatai teisminių svarstymų metu pateikė nemažai įtikinamų faktų, kurie verčia suabejoti ne tik kai kurių kaltinamųjų kalte, bet ir Lietuvos generalinės prokuratūros 1991 metų sausio 13-osios įvykių versija.

Be to, Lietuvos politinis ir teisėtvarkos elitas patyrė tikrą šoką, kai 2018 metų liepos mėn. Rusijos tardymų komitetas pranešė, jog iškėlė baudžiamąją bylą Lietuvos Respublikos generalinės prokuratūros ir teismo darbuotojams pagal RF Baudžiamojo kodekso 299 straipsnio 2 dalį (baudžiamosios bylos iškėlimas akivaizdžiai nekaltam žmogui). Šis faktas privertė rimtai susimąstyti daugelį Lietuvos prokurorų ir teisėjų, tame tarpe ir teisminę kolegiją, kuri turi paskelbti nuosprendį sausio 13-osios byloje.

Populiarus Lietuvoje laikraštis „Respublika“, nemažai nuveikęs 1990–1991 metais Lietuvos nepriklausomybės atgavimo labui, 2018 metų vasario mėn. pasiūlė sukurti Tautos tribunolą, kurį sudarytų nepriklausomi autoritetingi asmenys. Jie, laikraščio raginimu, turėtų „įvertinti ir pranešti Lietuvai, kas konkrečiai ir kaip pakenkė ir tebekenkia mūsų valstybei“.

Prie šio raginimo buvo pridėtas sąrašas kai kurių aferų ir nusikaltimų, kuriuos įvykdė valdančiojo Lietuvos elito atstovai. Visa tai gali tapti rimtu papildymu tame Lietuvos pareigūnų baudžiamąjame persekiojime, kurį paskelbė Rusija.

O dar paminėsime, jog 2018 metų kovo mėn. Nepriklausomybės akto signatarai Audrius Butkevičius, Zigmas Vaišvila ir prie jų prisijungęs Bronius Genzelis, tai yra buvę Landsbergio šalininkai ir bendražygiai, LR generalinėje prokuratūroje įregistravo pareiškimą, reikalaujantį ištirti antivalstybinę ir teroristinę buvusio Lietuvos TSR Aukščiausiosios Tarybos — Atkuriamojo Seimo vadovo Vytauto Landsbergio veiklą tikslu išlaikyti arba susigrąžinti valdžią.

Savo pareiškime šie signatarai išdėstė nusikalstamos Landsbergio klano veiklos epizodus, išvardino liudininkus, kurie gali patvirtinti tuos epizodus, o taip pat išvardino pavardes 9 mirusių ar nužudytų Kauno savanorių, ypač aktyviai dalyvavusių 1993 metais Kaune riaušėse prieš Algirdo Brazausko išrinkimą Lietuvos prezidentu.

Lietuvos generalinė prokuratūra pristabdė šį signatarų pareiškimo tyrimą argumentuodama tuo, kad jame neva nėra faktų ir pateikta tik asmeninė nuomonė. Vilniaus apylinkės teismas palaikė prokurorų nuomonę. Dabar bylą nagrinės Vilniaus apygardos teismas.

Tačiau net ne juristui aišku, jog tokia byla vilkinama nepagrįstai.

Juk antivalstybinės ir teroristinės Landsbergio veiklos tyrimas palies ne tik jį, bet ir visą jo išpampusį klaną, kuris beveik 30 metų laiko Lietuvą savo dusinančiuose gniaužtuose.

2019 metų gegužės mėn. pasikeitus valdžiai daugeliui Lietuvos valdančiojo elito atstovų teks prisiminti, kas tai yra atsakomybė prieš įstatymą. Be to, reikia pripažinti, jog landsbergininkų valdantysis režimas sugebėjo savo viešpatavimo Lietuvoje metu sukurti tvorą įstatymų, kurie malšina bet kokį kitokios nuomonės respublikoje pasireiškimą.

Jį gali sukelti ne tik socialinis nepasitenkinimas, bet ir išaiškinimas šokiruojančių Landsbergio klano kruvinos 1991 metų sausio 13-osios tragedijos organizavimo smulkmenų.

Ir todėl klanas reguliariai išmeta sensacingus liudijimus, neva patvirtinančius tarybinių kariškių nusikaltimus 1991 metų sausio mėn. Tokia „sensacija“ tapo chirurgo Kęstučio Vitkaus apsireiškimas socialiniuose tinkluose ir jo interviu Lietuvos televizijai.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 2 — id: `scraped:rubaltic_lt:889e2b5a9d684ded`

**Title:** „Kremliaus agentai“ Simpsonai: kompleksai verčia Lietuvą kovoti su multikais

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvoje prisiminta iniciatyva uždrausti “Simpsonus” po to, kai vienoje iš multiplikacinio filmo serijų buvo pajuokauta, jog personažai nežino, kas tai yra Lietuva. Anekdotinė Lietuvos reakcija išduoda nepilnavertiškumo kompleksą. Pabaltijyje supranta, jog jie pasauliui neįdomūs: be kalbų apie “rusų grėsmę” globalinėje Pabaltijo šalių kultūrinėje erdvėje jie neturi ką pasakyti žmonijai.

30-ojo “Simpsonų” sezono 12-toje serijoje Liza apgaudinėja draugę, sakydama, kad jos tėvai apsigyveno kitoje šalyje. Ji bando sugalvoti šalį, kurioje jos draugai tikrai niekada nebuvo, ir įvardina Lietuvą.

“Mano tėvai išvyksta į Lietuvą. Jūs buvote Lietuvoje?” — klausia Liza draugės tėvo. Tas, nesupratęs, atsako: “Ne, tai buvo skaudanti vieta”.

Amerikiečių multiplikacinio serialo kūrėjai vargu ar norėjo paliesti švelnius Lietuvos “patriotų” jausmus, tačiau išėjo taip, jog dūrė jiems pirštu į akį.

Reaguota į pajuokavimą buvo anekdotiškai neadekvačiai.

Gruodžio mėn. Lietuvos radijo ir televizijos komisija nurodė “Simpsonus” vedančiai kompanijai AII Media Lithuania, kad multikas propaguoja alkoholizmą ir transliuojamas netinkamu laiku, kai jį gali pamatyti vaikai.

Iš pradžių buvo norima multiplikacinį serialą visai uždrausti, tačiau vėliau buvo leista jį transliuoti po dešimtos valandos vakaro. Tačiau dabar, kai paaiškėjo nelojalus “Simpsonų” požiūris į Lietuvos Respubliką, Lietuvoje iškilo klausimas: o gal be reikalo neuždraudėme?

“Simpsonų” epizodas verčia prisiminti Pabaltijo “kryžiaus žygį” prieš rusų multiplikacinį serialą “Maša ir Lokys”. Tai mėgstamas pabaltijiečių užsiėmimas — kovoti su multikais. Net britų Times praeitais metais pripažino Pabaltijo šioje srityje pirmavimą, paminėdama žymiausius kovos su nupieštų personažų “grėsme” specialistus Talino universiteto Komunikacijų instituto darbuotoją Priitą Chybimegi ir Lietuvos Seimo deputatą Lauryną Kaščiūną. Minėti “ekspertai” savo “moksliniuose darbuose” įrodinėjo, jog “Maša ir Lokys” — vaikų psichiką žeidžiantys Kremliaus propagandinės įtakos instrumentai, ir rusų multiplikacinį serialą būtina uždrausti.

Reakcijoje į “Simpsonus” ir “Mašą ir Lokį” yra daug bendro. Šios istorijos turi bendrą vardiklį: nepilnavertiškumo kompleksą.

Liguistas požiūris į “Mašą ir Lokį” — šio multiko populiarumo pasaulyje pasekmė. Kuo populiaresnis tampa multiplikacinis filmas, tuo aršiau pasireiškia Pabaltijo liguistumas.

“Maša ir Lokys” pagal peržiūrėjimų visumą laikomas populiariausiu pasaulyje serialu. Vienas iš multiplikacinio filmo leidimų pateko į Gineso rekordų Knygą kaip labiausiai žiūrimas. Rezultatu 3,4 milijardo peržiūrėjimų YouTube epizodas “Maša plius košė” patenka į penketuką labiausiai pasaulyje žiūrimų vaizdo įrašų.

Tai yra mes turime pasaulinio masto fenomeną. Ir kas labiausiai nepatinka Pabaltijui – tą fenomeną pagimdė rusų kultūra. Tai neteisinga, taip negali būti. Rusija — atsilikusi, degraduojanti šalis, kuri netrukus subyrės ir nugaiš patvoryje nuo degtinės, taip pasauliui teigė Rusiją tiriantys Pabaltijo “ekspertai”, o dabar rusų multiplikacinis filmas laimi konkurenciją su “Disnėjumi” dėl amerikiečių ir europiečių vaikų meilės.

Pabaltijo rusofobai neranda kuo atsakyti į “Mašą ir Lokį”, neskaitant pareiškimų, kad ši saldi porelė — Putino hibridinis ginklas. Priešpastatyti “Kremliaus agentams” Lokiui ir Mašai savą ginklą jie negali, todėl kad pasaulio žemėlapyje nėra masinės ir elitarinės Pabaltijo šalių kultūros.

Tuo jos principialiai skiriasi nuo kaimynų.

Rusija turi “Mašą ir Lokį” — labiausiai žiūrimą pasaulyje serialą, kurį mėgsta milijonai vaikų. Baltarusiai turi World of Tanks — vieną iš populiariausių pasaulyje kompiuterinių žaidimų. Lenkija turi pasaulyje žinomą kinomatografą. Lenkų filmas “Šaltasis karas” šiais metais gali sulaukti “Oskaro” už geriausią režisūrą ir geriausią operatoriaus darbą ir lygiomis kausis su Holivudo produkcija dėl amerikiečių kino akademijos premijos.

Kada jų filmus buvo siūloma apdovanoti “Oskaru”? O kada paskutinį kartą ką nors girdėjome apie Pabaltijo filmus ir serialus?

Pastarasis klausimas — neretorinis. Atsakymas į jį Pabaltijo “patriotams” ypatingai nemalonus. Tarybinais laikais latvių serialą “Ilgas kelias kopose” žiūrėjo visa Tarybų Sąjunga ir socialistinės stovyklos šalys.

Tarp kitko, “Ilgas kelias kopose” pasakojo apie “miško brolius” ir latvių deportaciją į Sibirą po Antrojo pasaulinio karo. Šiandieninis Pabaltijis taip pat norėtų papasakoti pasauliui apie deportacijas ir “miško brolius” ir savo istorija sudominti pasaulį. Tada amerikiečių vidutiniokas iš “Simpsonų” bent jau sužinotų, ką reiškia žodis “Lietuva”.

Tačiau to pasakyti jis negali. Rusija, Rumunija ir Lenkija sugebėjo sukurti savo originalų postsocialistinį kinomatografą, o Pabaltijo šalys — ne. Jos nepajėgia sukurti tokio savos kultūros produkto, kuriuo susidomėtų pasaulis.

Alek Bolduin, kurdamas Donaldo Trampo parodiją, susitinka su Lietuvos, Latvijos ir Estijos vadovais ir negali prisiminti, kas tie žmonės. Pajuokų multiplikaciniame filme apie Europos Sąjungos šalis ir jų ypatumus Estija visai neminima, o Lietuva su Latvija išsiskiria tuo, kad jos pastoviai gąsdinamos.

Vienintelė išimtis iš šios taisyklės — pseudodokumentinis Bi-bi-si filmas apie tai, kaip Trečiasis pasaulinis karas prasideda dėl “žaliųjų žmogeliukų” desanto Daugpilyje. Ten jau anglai nesupainiojo Lietuvos su Latvija, ištyrė Latgalijos specifiką, įvertino Latvijos rusų faktorių ir atkūrė pabaltijiečių kliedesius apie “neišvengiamą rusų agresiją”.

Šis atvejis daug ką paaiškina. Po jo tampa aišku, kodėl Pabaltijo šalys negali pateikti nė vieno rusų agresijos fakto, tačiau maniakaliai įkyriai pasakoja apie ją pasauliui.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 3 — id: `scraped:rubaltic_lt:c2358f404495b432`

**Title:** Grybauskaitė tampoma už virvučių: kas valdo Lietuvos prezidentę

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Pirmojo posttarybinės Lietuvos vadovo menas vadovauti šaliai pasinaudojant turima valstybės vadovą kompromituojančia medžiaga, pačiam liekant šešėlyje, pasiekė viršūnę Dalios Grybauskaitės prezidentavimo metu. Komunistinė Grybauskaitės praeitis, jos veikla VSK (КГБ) ir gyvenimas Leningrade konspiraciniame bute suteikia Landsbergiui, taip pat įmerkusiam uodegą į čekistų paslaptis, tiesiog beribes galimybes šantažuoti. RuBaltic.Ru tiria, kas iš tiesų pastaruoju dešimtmečiu valdė Lietuvą „raudonosios Dalios“ vardu.

Tebūnie Dalia Lietuvos dalia!

Šiuo metu Vytautas Landsbergis sėkmingai manipuliuoja Lietuvos prezidente Dalia Grybauskaite. Ši situacija — klasikinis ilgalaikės profesoriaus kadrų politikos pavyzdys. 2009 metų pavasarį prezidento rinkimų metu Landsbergis ir jo partija „Tėvynės sąjunga – Lietuvos krikščionys demokratai“ netikėtai, kaip visiems atrodė, palaikė ne šiaip sau Europos komisarę Dalią Grybauskaitę, bet buvusią Vilniaus aukštosios partinės mokyklos politekonomijos katedros docentę ir TSKP CK organizacinio partinio darbo skyriaus rezervistę.

Ši frazė akivaizdžiai sąlygojo užtikrintą Grybauskaitės pergalę kovoje dėl prezidento kėdės. Ji gavo 69,9 proc. respublikos rinkėjų balsų — geriausias visų posttarybinių laikų rinkimų Lietuvoje rezultatas.

Šiandien galima drąsiai teigti, jog aktyvios buvusios komjaunuolės ir komunistės Grybauskaitės palaikymą Landsbergio konservatorių elektorato jėgomis 2009 metų prezidento rinkimuose reikia vertinti sekančiais momentais.

Pažymėsime, jog antroji konservatorių Grybauskaitės palaikymo sąlyga buvo jos sutikimas reanimuoti baudžiamąją sausio 13-osios bylą. 2011 metų sausio mėn. ji turėjo būti nutraukta suėjus patraukimo baudžiamojon atsakomybėn terminui.

Juk Lietuvoje kasmet iškyla vis nauji landsbergininkų kaltės, kad prie televizijos bokšto buvo pralietas kraujas, įrodymai. Jie bijo atpildo už šį nusikaltimą, neišvengiamo po to, kai bus paviešinta visa kruvinojo sausio tiesa.

Grybauskaitės išrinkimas Lietuvos prezidente tapo paskutine Lasndsbergio galimybe padėti savo pseudoteisėtą tašką tragiškų 1991 metų sausio įvykių tyrime. Juk būtent jis ir jo aplinka organizavo tada kruvinąsias aukas.

Sausio 13-osios baudžiamosios bylos reanimavimas

Dalia Grybauskaitė, tapusi Lietuvos prezidente, nedelsdama ėmėsi vykdyti Landsbergio prašymus. Jau 2009 metų birželio 3 d. Lietuvos generaliniu prokuroru ji paskyrė Darių Valį. Iki tol jis vadovavo tolimo Akmenės rajono prokuratūrai. Tuo žingsniu Grybauskaitė suteikė vietinės reikšmės prokurorui Valiui neįtikėtiną paslaugą kopiant karjeros laiptais. Šis viską suprato ir besąlygiškai vykdė motinos–viršininkės nurodymus.

Po Valio atėjimo į Lietuvos Respublikos Generalinę prokuratūrą prasidėjo diskusijos dėl būtinybės suderinti Baudžiamąjį kodeksą su tarptautinės humanitarinės teisės normomis, visų pirma — karo nusikaltimų ir nusikaltimų prieš žmogiškumą atžvilgiu. 2009 metų rugpjūčio mėn. Valys sudarė darbinę prokurorų grupę, kuri ėmėsi ruošti Lietuvos Baudžiamojo kodekso pataisų projektą.

Pirmiausia tai lietė Baudžiamojo kodekso 100 straipsnį, nurodantį neleistiną su žmonėmis elgesį, uždraustą tarptautinės teisės.

2010 metų gruodžio mėn. Grybauskaitė, užbėgdama už akių sausio 13-osios bylos nutraukimui suėjus patraukimo baudžiamojon atsakomybėn terminui, spėjo pateikti Seimui atitinkamas Baudžiamojo kodekso pataisas. Tas pataisas Seimas patvirtino 2011 metų kovo 22 d. Lietuvos Respublikos įstatymu XI-1291. Jos leido įvykius prie televizijos bokšto kvalifikuoti kaip karo nusikaltimus ir nusikaltimus prieš žmogiškumą, neturinčius senaties termino.

O dar buvo priimtos pataisos, leidžiančios Lietuvos teismams teisti užsienio šalių piliečius be jų dalyvavimo baudžiamąjame procese. Lietuvos Seimas priėmė jas skubos tvarka (!), prezidentei Grybauskaitei reikalaujant.

2010 metų gruodžio 29 d. Lietuvos Generalinėje prokuratūroje buvo suburta nauja tardytojų grupė, kuri turėjo užsiimti 1991 metų sausio įvykiais. Buvo pranešta, kad grupę sudarė keturi esą aukščiausios kvalifikacijos prokurorai su didele darbo patirtimi. Tardytojų grupės vadovu buvo paskirtas prokuroras Simonas Slapšinskas, charakterizuojamas kaip aukštos kvalifikacijos specialistas.

Tačiau sausio 13-osios bylos medžiaga leidžia tvirtinti, jog gandai apie tardyno grupės prokurorų aukščiausią kvalifikaciją buvo ženkliai išpūsti. Tuo tikslu pakanka išanalizuoti abejotiną turinį Kaltinamojo akto, kuriame apstu nevykusių falsifikavimų, nesudūrimų galo su galu ir neįrodytų teiginių.

Remdamasis pataisomis, kurios pateko į Baudžiamąjį kodeksą Grybauskaitės pastangų dėka, Vilniaus apygardos teismas nuo 2016 metų sausio iki 2018 metų spalio tyrė bylą Nr. 09-2-031-99 arba 1991 metų sausio 13-osios bylą, kurioje kaltinimai pateikti 66 Rusijos, Baltarusijos ir Ukrainos piliečiams (du iš jų mirė).

Lietuvos politikai ir prokurorai įsitikinę, kad šių „nusikaltėlių“ nuteisimas leis padėti paskutinį tašką klausime, kas yra sausio tragedijos „kaltininkas“.

Bet tai ginčytinas tvirtinimas. Ir egzistuoja įsitikinimas, kad Rusija sugebės jį paneigti.

Nusikalstami Landsbergio prašymai

Pirmojo Grybauskaitės prezidentavimo metu ji ir Landsbergis nesistengė slėpti savo gana dažnų kontaktų. Buvę prezidentūros darbuotojai papasakojo žurnalistei Rūtai Janutienei, Lietuvoje triukšmą sukėlusios knygos (2013 m.) „Raudonoji Dalia“ autorei, jog Landsbergis dažnai atvykdavo pas Grybauskaitę į jos rezidenciją elitinėje Turniškių gyvenvietėje.

Taigi akivaizdus Lietuvos Respublikos Konstitucijos 84-jo straipsnio pažeidimas. Nėra abejonių, jog Landsbergis, duodamas Grybauskaitei kaip prezidentei pavedimus, vykdė sunkius valstybinius nusikaltimus. Tai daug svaresnis nusižengimas, negu tas, kuriuo buvo kaltinamas prezidentas Rolandas Paksas. Tačiau Landsbergis vis dar jaučiasi laimingas.

2014 metų gegužės mėn. Landsbergis vėl parėmė Grybauskaitę prezidento rinkimuose. Šį kartą pasiekti prezidento posto jai buvo sudėtingiau, nors jos oponentas Zigmantas Balčytis, Lietuvos socialdemokratų atstovas, ypatingo autoriteto rinkėjų tarpe nebuvo pelnęs. Ir vis dėlto rinkimai tada turėjo antrąjį ratą.

Antrąjame rate 2014 metų gegužės 25 d. Grybauskaitė nugalėjo, surinkdama 57,87 proc. atėjusių balsuoti rinkėjų balsų. O atėjo tik 47,3 proc. rinkėjų, tai yra nuo 2,56 tūkstančio 1,2 tūkstančio. Faktiškai už Grybauskaitę balsavo tik 27,37 proc. visų Lietuvoje užregistruotų rinkėjų. Tai labai kuklus rezultatas.

Savaime aišku, jog po 2014 metų gegužės rinkimų Grybauskaitė prezidento kėdėje jautėsi ne taip ryžtingai, kaip pirmosios kadencijos metu.

Landsbergio rusofobų klano palaikymo jai reikėjo labiau, nei bet kada.

Grybauskaitės valdymo metu Landsbergio klanas, pasinaudodamas momentu, galutinai primetė respublikai žalingus totalitarinės klano demokratijos principus, kuriais, manipuliuodama Seimu, vadovaujasi jo partija.

Situacija su Lietuvos prezidentais Algirdu Brazausku, Valdu Adamkum, Rolandu Paksu ir Dalia Grybauskaite liudija, jog politika užsiėmęs muzikologas tapo tikru politikos rykliu, sugebėjusiu visais parametrais aplenkti savo „mokytojus“.

Antrasis Grybauskaitės apsireiškimas

Šiuo metu Landsbergis ir jo konservatoriai susidūrė su rimta problema. 2019 metų gegužės mėn. išėjus Grybauskaitei iškyla realus „totalitarinės demokratijos“ griūties pavojus, tos „demokratijos“, kurią Landsbergio klanas sugebėjo primesti Lietuvai.

Buvę aktyvūs landsbergininkai Zigmas Vaišvila, Audrius Butkevičius ir Bronius Genzelis trokšta rimtai suvesti sąskaitas su muzikologu.

Išsigelbėjimą Landsbergis mato savo užkulisinio Lietuvos Respublikos valdymo tęsinyje. Šiuo tikslu Tėvynės sąjunga – Lietuvos krikščionys demokratai kandidate į Lietuvos prezidentus 2018 metais iškėlė šios frakcijos Seime deputatę Ingridą Šimonytę.

Tai antrasis Grybauskaitės apsireiškimas. Moteris 44 metų, netekėjusi, bevaikė, ekonomistė. Beveik vienas prie vieno Grybauskaitė. Ir ji, kaip ir dabartinė prezidentė, turi biografijoje šusnį tamsių dėmių. Tvirtinama, jog Šimonytė, 2019–2012 metais būdama Lietuvos finansų ministrė, dalyvavo ne vienoje prezidentės Grybauskaitės inicijuotoje aferoje.

Tuo pačiu metu prezidentė supirkinėjo valstybės obligacijas, tuo neteisėtai praturtėdama. Taip mano buvusi Europos parlamentarė Margarita Starkevičiūtė, priminusi, jog Europos Sąjungoje už tokius nusikaltimus baudžiama turto konfiskavimu.

Be to, Šimonytė aktyviai dalyvavo skandalingame vieno iš vedančiųjų bankų, Snoro, bankrote. To pasekoje 8 milijardų litų vertės banko aktyvai ir nuosavybė dingo be pėdsakų. Ir tvirtinama, jog dalis šio banko pajamų 2014 metais buvo panaudota Grybauskaitės rinkimų kampanijai.

Ta proga „Laisvas laikraštis“ 2018 metų spalio 16 d. išspausdino išsamų straipsnį „Naujas šviesus mafijos veidas“. Jame gana smulkiai aprašytos Šimonytės nuodėmės.

Ir, žinoma, verta atkreipti dėmesį į nuotrauką, kurioje konservatorių patriarchas Landsbergis laimina Šimonytę, pakilusią kovon už Lietuvos prezidentės postą. Toks keliaklupščiavimas — retas reiškinys net Lietuvoje. Jis liudija, jog Šimonytė savo nuolankumu leido suprasti, jog bet kurie Landsbergio prašymai jai taps įstatymais, kai ji užims Lietuvos prezidentės vietą.

Informacija Lietuvos rinkėjui

2016 metais Pietų Korėjos prezidentė Pak Kyn Che, gana energinga netekėjusi moteris, buvo nuteista 24 metus kalėti už tai, jog ją neteisėtai įtakojo artima draugė Čchve Sun Sil. Draugė kišosi į prezidentės politinių sprendimų priėmimo procesus, o taip pat reikalavo, kad stambios kompanijos pervestų dideles sumas jos kontroliuojamiems fondams.

Čchve Sun Sil pelnė trejus laisvės atėmimo metus, o prezidentė — 24. 2018 metų liepos mėnesį už kyšio paėmimą ir valstybės lėšų iššvaistymą Seulo teismas jai pridėjo dar aštuonerius metus.

Belieka tikėtis, kad Lietuvos Temidė kada nors paseks Pietų Korėjos pavyzdžiu.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 4 — id: `scraped:rubaltic_lt:957664fe44751eee`

**Title:** Kaip VSK agentas tapo Lietuvos „pilkuoju kardinolu“. Tikroji Landsbergio biografija

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Vytautas Landsbergis iki šių dienų lieka vienu iš įtakingiausių šiuolaikinės Lietuvos žmonių. Pagyvenusio Lietuvos valstybingumo patriarcho įtakingumą priimta aiškinti Landsbergio moraliniu autoritetu ir jo dalyvavimu kovojant už Lietuvos nepriklausomybę, tačiau tikrosios „tautos tėvo“ galingumo priežastys daug klaikesnės. Buvęs Sąjūdžio lyderis sukaupė medžiagą, kompromituojančią pirmojo Lietuvos ešelono politikus, ir gali juos visus šantažuoti. Didelę paspirtį kaupiant kompromatus kelių kartų Landsbergių klanas įgijo darbuodamasis TSRS specialiųjų tarnybų labui.

Kaip Landsbergis tapo Sąjūdžio lyderiu

Verta priminti, kaip apolitiškas, Lietuvoje visiškai nežinomas  muzikologas Vytautas Landsbergis 1988 metų biržely tapo Lietuvos judėjimo už pertvarką iniciatyvinės grupės nariu, o vėliau — lyderiu. Judėjimas buvo pavadintas Sąjūdžiu.

Abejonių nekeliantys šaltiniai byloja (straipsnio autorius buvo pakankamai informuotas žmogus, nes dirbo Lietuvos KP Vilniaus miesto Spalio rajono pirmuoju sekretoriumi, o šiame RK partinėje įskaitoje buvo Lietuvos TSR VSK komunistai — RuBaltic.Ru pastaba.), kad Landsbergis pateko į iniciatyvinę Sąjūdžio grupę tik reikalaujant VSK kuratoriui kaip „patikrintas tarybinis inteligentas“. Jis privalėjo informuoti Komitetą apie visus iniciatyvinės grupės kurso „nukrypimus“.

Po Sąjūdžio sukūrimo pirmuoju jo neformaliu lyderiu tapo rašytojas ir populiarus visuomenės politinis veikėjas Vytautas Petkevičius. Būtent jam vadovaujant judėjimas pasireiškė kaip nauja ir galinga respublikoje politinė jėga. Tačiau TSKP CK ir Lietuvos TSR VSK Sąjūdžio kuratoriams Petkevičius tapo neparankia figūra: Vytautas garsėjo kraštutinai nepriklausomu charakteriu.

Nedidelis nukrypimas. Kaip žinia, Sąjūdžio pavadinimas buvo uždraustas 1944 metais atkūrus Lietuvoje tarybų valdžią. Juk taip save vadino antitarybinis ir pronacistinis Lietuvos aktyvistų frontas (LAF), sukurtas Berlyne 1940 metų liepą.

Tačiau nereikia stebėtis. Viskas vyko pagal nurodymus pagrindinių Kremliaus pertvarkytojų: TSKP CK generalinio sekretoriaus Michailo Gorbačiovo ir TSKP CK sekretoriaus, Politinio biuro nario Aleksandro Jakovlevo.

Lietuvos KP CK biuras superslaptai rekomendavo...

1988 metų rugpjūty Aleksandras Jakovlevas pabuvojo Lietuvoje tikslu patikrinti, kaip klostosi reikalai organizuojant liaudies Judėjimą, kuris turėjo rimtai stumtelti politiniame lauke „partijos kunigaikštukus“. Taip 1988 metų liepą lankydamasis Lenkijoje Gorbačiovas pavadino TSKP sekretorius.

Jakovlevui nepatiko Lietuvos judėjimo lyderis Petkevičius, kuris turėjo savo nuomonę ir pokalbio su Jakovlevu metu išdrįso kritikuoti Kremliaus politiką Lietuvoje. To išdavoje 1988 metų rugsėjy Maskvoje buvo nutarta pakeisti Petkevičių neišvazdžia, amorfine Landsbergio asmenybe.

Kodėl marksistinės–lenininės estetikos dėstytojas Landsbergis buvo parinktas kaip Petkevičiaus pakaitalas?

Bet čia verta priminti, kad greta garsiai ir iškalbingai pasireiškiančio tribūno Petkevičiaus muzikologas Landsbergis atrodė nekaip, o 1988 metų biržely patyrė viešą konfūzą. Mitinge, skirtame Lietuvos delegatų palydoms į XIX Sąjunginę partinę konferenciją, Landsbergis bandė pasisakyti, tačiau dėl prastos dikcijos patyrė nesėkmę. Iš minios jam šaukė: „Išsitrauk šiaudus iš nosies!“

Turbūt būtent todėl 1988 metų rugsėjy Lietuvos KP CK biuro nariai superslapto posėdžio metu (be protokolo) sutiko su Lietuvos TSR VSK pirmininko Eduardo Eismunto pasiūlymu rekomenduoti profesorių muzikologą Sąjūdžio lyderiu.

Ypač Eismuntas akcentavo tai, kad Landsbergio šeima visada buvo tarybinėse pozicijose, o jo tėvas Vytautas Žemkalnis–Landsbergis suteikė tarybų valdžiai neįkainojamas paslaugas, dirbdamas НКВД, o vėliau КГБ agentu nuo 1927 metų.

LKP CK biuro nariai manė, kad, paskyrus Landsbergį, Sąjūdis taps paklusniu partinio elito ir VSK įrankiu.

Muzikologas buvo faktiškai Lietuvos vadovas

Pasinaudodamas tuo autoritetu, kurį Sąjūdis pelnė vadovaujant Petkevičiui, Landsbergis pradėjo diktuoti sąlygas Tarybų Lietuvos vadovybei. Algirdas Brazauskas 1988 metų spaly, palaikant Sąjūdžiui, tapęs pirmuoju LKP CK sekretoriumi, o vėliau, 1990 metų sausy, Lietuvos TSR Aukščiausiosios Tarybos Prezidiumo pirmininku, buvo priverstas skaitytis su Landsbergiu. Ir ne šiaip sau skaitytis, o pastoviai su juo susitikinėti.

Apie savo pastovius susitikimus su Landsbergiu Brazauskas papasakojo prisiminimų knygoje „Lietuviškos skyrybos“, kuri buvo išleista 1993 metais. Jis parašė, jog 1989 1990 metais slapta susitikinėjo su Landsbergiu Vingio parke ir aptarinėjo su juo veiksmus Lietuvos Komunistų partijos, kuri 1989 metų gruody pasitraukė iš TSKP.

Tikėtina, jog ir prezidentavimo metu (1993–1998 m.) Brazauskas buvo priverstas skaitytis su lietuviškojo Moriarti nuomone, nors tuomet buvę komunistai buvo skaudžiai nustūmę nuo Lietuvos politinės arenos Landsbergio klaną. Tačiau akivaizdžiai neryžtinga prezidento Brazausko politika, nepalietusi nė vieno Lietuvai pragaištingo sprendimo, priimto Landsbergio valdymo metu, liudija, kad pastarasis vis dar jį įtakojo.

Gana efektyviai „šešėlinio spaudimo“ taktika Landsbergis naudojosi prezidento Valdo Adamkaus, pakeitusio Brazauską, atžvilgiu.

Tai išaiškėjo 2011 metų rugpjūty. Tada spaudos konferencijoje, kuri buvo organizuota pristatant Adamkaus prisiminimų knygą „Paskutinė kadencija. Prezidento dienoraščiai“, buvęs prezidentas pranešė, kad, būdamas valdžioje, pastoviai buvo spaudžiamas „gana gerbiamų Lietuvoje asmenybių“.

Adamkus rašo, kad jie jam diktavo, kaip reikia elgtis ir ką į kokias pareigas skirti. Tokias instrukcijas jis gaudavo ne tik asmeniškai, bet ir faksu bei telefonu.

Be to, Adamkus sulaukė nedviprasmiškų užuominų, kad nepaklusnumo atveju jis bus politiškai sunaikintas. Tokį elgesį Adamkus pavadino šantažu.

Į klausimą, kodėl Adamkus nepaviešino šantažuotojų vardų, buvęs prezidentas davė nevisai suprantamą atsakymą. Adamkus pareiškė, jog tie žmonės, iš kurių jis gaudavo nurodymus, Lietuvoje beveik „dievinami“ ir iki šiol laikomi iškovotos nepriklausomybės simboliu. Todėl, Adamkaus manymu, jų vardų paskelbimas iš jo pusės taptų „nusikaltimu prieš šventą tikėjimą laisve ir demokratija“.

Tačiau situacija, kai Adamkų valdė jau minėtas klanas, buvo sąlygota štai kuo. Iki išrinkimo Lietuvos prezidentu jis pastoviai gyveno Čikagoje (JAV). Pagal Lietuvos Respublikos Konstitucijos 78 straipsnį jis negalėjo dalyvauti Lietuvos prezidento rinkimuose, nes kandidatas į prezidentus turėjo ne mažiau trejų pastarųjų metų pastoviai gyventi šalyje.

Ir nors Adamkaus varžovai pareiškė, jog Šiauliai —  ne jo namai, o tik ta vieta, kurioje jis „laiko savo šlepetes“, apygardos teismo nutarimas leido jam balotiruotis į Lietuvos prezidento vietą.

Linas Kuojelis, amerikiečių deleguotas Landsbergio patarėjas 1990–1991 metais, interviu „Respublikos“ laikraščiui  Lietuvos teismo nutarimo dėl Adamkaus gyvenamosios vietos klausimu pastebėjo: „Kiek suprantu, Lietuvos teismai linkę paneigti ne tik Lietuvos Konstituciją (Kuojelis talkino ruošiant Lietuvos Respublikos Konstituciją – Vl.Š.), bet ir Einšteino bei Njutono dėsnius. Vienas ir tas pats objektas tuo pačiu metu negalėjo būti dviejose vietose (JAV ir Lietuvoje).“

Būdamas šios melagingos nutarties, kuri leido Adamkui tapti prezidentu, organizatoriumi, Landsbergis gavo į rankas galingą manipuliavimo ja įrankį.

Verta pažymėti, jog Landsbergis jokių savo dalyvavimo aferoje su Adamkaus gyvenamaja  vieta dokumentinių pėdsakų nepaliko.

Tai natūralu, nes Lietuvos Respublikos 84 straipsnis kategoriškai draudžia įtakoti prezidentą priimant nutarimus. Tokie reikalavimai egzistuoja daugelyje pasaulio šalių. Ten prezidento įtakojimas bet kuria prasme laikomas sunkiu nusikaltimu.

Pakso peripetijos

Vienintelis Lietuvos prezidentas, kurio atžvilgiu Landsbergis neturėjo kompromato, buvo Rolandas Paksas. Žinomas Lietuvos lakūnas ir sklandytojas, 1980 metais tapęs aukščiausiojo pilotažo TSRS čempionu.

Pagal 2002 metų gruodžio — 2013 metų sausio prezidento rinkimų rezultatus Paksas buvo išrinktas prezidentu. Landsbergio klanui teko sutelkti daug pastangų, siekiant pašalinti Paksą, kuris buvo žinomas savo konstruktyvia pozicija Rusijos atžvilgiu.

Galų gale 2003 metų spaly Paksas buvo apkaltintas ryšiais su rusų verslininku Jurijum Borisovu, kuris esą rėmė priešrinkiminę politiko kampaniją už tai, kad jei šis bus išrinktas prezidentu, pelnys eilę sprendimų savo naudai. Visus kaltinimus savo adresu Paksas atmetė ir visa tai pavadino „sistemos kerštu už pastangas kovoti šioje šalyje su korupcija“.

Tačiau 2004 metų balandy Lietuvos Respublikos Konstitucinis teismas pripažino jį kaltu, ir tą patį mėnesį balsavimo Seime metu jam buvo pareikšta apkalta. Pravedus priešlaikinius prezidento rinkimus, valstybės vadovu vėl tapo Adamkus.

2009 metų biržely Paksas buvo išrinktas Europos parlamentaru, atstovaudamas Lietuvos centro dešiniųjų politinei partijai „Tvarka ir teisingumas“. Susidorojimas su Lietuvos publikos numylėtiniu lakūnu Rolandu Paksu eilinį kartą pademonstravo Landsbergio klano jėgą.

2018 metais JT Žmogaus teisių komitetas paskelbė „Baigiamasias pastabas Nr.CCPR/C/LTU/CO/4 dėl žmogaus teisių Lietuvoje“. Jose Komitetas išreiškė susirūpinimą tuo, jog Lietuva vilkina Konstatacijos vykdymą byloje „Paksas prieš Lietuvą“ dėl grąžinimo jam atgaline data nuo 2004 metų teisės būti prezidentu ir premjeru.

Ypatingą JT Komiteto susirūpinimą iššaukė Lietuvos Konstitucinio teismo 2016 metų nutarimas, kuriuo atsisakyta grąžinti Paksui aukščiau minėtas teises, remiantis savitu Lietuvos Respublikos Konstitucinio teismo traktavimu.

Toks požiūris, pažymėjo JT Žmogaus teisių komitetas, prieštarauja tarptautiniams Lietuvos įsipareigojimams. Tačiau tokia situacija dabartinėje Lietuvoje natūrali. Juk Konstitucinio teismo vadovu nuo 2014 metų dirba tūlas Dainius Žalimas — nuo 17 metų ištikimas Landsbergio tarnas, tiksliau — klapčiukas. Dėka muzikologo pastangų Žalimas tapo ne tik diplomuotu juristu, bet ir sėkmingai kilo karjeros laiptais.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 5 — id: `scraped:rubaltic_lt:7230d2279e73f4e1`

**Title:** „Paleckio byla–2“. Lietuviai verčiami tylėti apie įvykius prie Vilniaus televizijos bokšto

**Source:** rubaltic_lt (propaganda)

**Text:**

```
„Šnipų sąmokslas“ Lietuvoje apauga naujomis smulkmenomis. Sąraše asmenų, kurie esą darbavosi Rusijos žvalgybai, atsirado naujos pavardės. Tačiau pagrindiniu bylos figūrantu lieka jaunas opozicijos politikas Algirdas Paleckis — vienas iš nedaugelio, drįstančių viešai abejoti oficialia Vilniaus pozicija 1991 metų sausio 13-osios įvykių atžvilgiu. Jau tapo aišku, jog jo areštas tiesiogiai siejasi su masiškų žudynių prie Vilniaus televizijos bokšto tyrimu.

Paleckis ir kompanija kaltinami tuo, jog rinko informaciją, kurią perdavinėjo Rusijos specialiosioms tarnyboms. Portalo lrytas.lt duomenimis, politiko veikla galėjo turėti ryšį su „galimu įkaitų užgrobimu“. Apie kokius įkaitus eina kalba?

Esmė tame, kad praeitais metais Rusijos tyrimų komitetas iškėlė baudžiamąją bylą atsakingiems Lietuvos Respublikos generalinės prokuratūros ir teismo darbuotojams. Jų veiksmuose įžvelgiami požymiai nusikaltimo, numatyto RF Baudžiamojo kodekso 299 sraipsniu: „Baudžiamosios bylos iškėlimas akivaizdžiai nekaltam“. Informaciją apie šiuos teisėjus ir prokurorus esą ir rinko Paleckio vadovaujamas „šnipų tinklas“.

Spaudoje jau pasirodė pranešimai apie tai, kad politikas kaltinamas informacijos rinkimu būtent apie sausio 13-osios įvykius. Viena iš pirmųjų apie tai prabilo Rusijos žurnalistė, knygos „Kas ką išdavė“ autorė Galina Sapožnikova: „Ką naujo Paleckis gali pranešti Maskvai apie sausio 13-osios bylą? Viskas jau seniai aprašyta mano knygoje: skaitykite į sveikatą“.

Paleckiui mestų kaltinimų esmė tapo aiški, kai verslininkas Pavlas Ževžikovas, pas kurį buvo atlikta krata, pareiškė, kad jis neturi „nei galimybių, nei noro“ talkinti nemalonėn patekusiam politikui, renkant Rusijos žvalgybai informaciją apie Lietuvos teisėsaugos organų atstovus, kurie tiria 1991 metų sausio 13-osios žudynes.

Įdomu tai, kad byloje atsiranda nauji vardai. Iš pradžių Paleckio ir Rusijos publicisto Valerijaus Ivanovo (kuriam, gali būti, buvo skiriamas ryšininko vaidmuo) kompanijon patekę Leonidas Minkevičius, Artūras Šidlauskas ir Vaidas Prunckus. Žiniasklaida spėliojo, ar pastarasis nėra buvusios Lietuvos premjerės Kazimiros Prunskienės sūnus. Paaiškėjo, jog šnipinėjimo tema jis buvo apklaustas, tačiau neareštuotas.

lrytas.lt portalas į numatomų Paleckio talkininkų sąrašą įtraukė Deimantą Bertauską — Vilniaus kompanijos Food Expert ir viešosios įstaigos XXI amžius direktorių. O dar į teisėsaugininkų akiratį pateko Socialistinio liaudies fronto pirmininko pavaduotojas Andrejus Gorbatenkovas. Tačiau visas „liaudies priešų“ sąrašas iki šiol nepaskelbtas: sulaikyti ir kiti asmenys, kurių vardai kažkodėl slepiami.

Apie tai, kodėl „šnipų tinklas“ buvo aptiktas būtent dabar, nebūtina dar kartą priminti. Ne už kalnų priešrinkiminė karštligė, ir premjeras Saulius Skvernelis, Valerijaus Ivanovo žodžiais, į prezidento rūmus įjoti nori baltu rusofobijos žirgu. O iki nuosprendžio paskelbimo sausio 13-osios byloje lieka mažiau mėnesio.

Šioje situacijoje konservatoriai taip pat suinteresuoti antirusiška isterija. Tragiški įvykiai prie Vilniaus televizijos bokšto — jų arkliukas.

Tokių žmonių skaičius kasmet auga: oficialiosios versijos „baltosios dėmės“ per daug krenta į akis.

Paleckis, kaip žinia, jau nukentėjo už „sovietinės agresijos“ neigimą. Už žodžius apie tai, jog „savi šaudė į savus“, jam teko sumokėti piniginę baudą. Tiesa, į teismą jis atsivedė 12 gynybos liudytojų, kurie po priesaikos pareiškė, jog į minią prie televizijos bokšto šaudė ne tarybiniai kariškiai. Dėl to lietuviškoji Temidė buvo patekusi į nepatogią padėtį.

Abejonę kelia „sovietinių okupantų“ nusikaltimai? Už tai ir anksčiau buvo galima pelnyti bausmę. Tačiau dabar jau vargu ar išsipirksi pinigine bauda — bet kuriuo momentu tave gali įrašyti į užsienio informatorių sąrašą, o tai jau rimtas straipsnis.

Ir tikrai verta prisiminti parodymus Boleslovo Biloto – vieno iš „Paleckio bylos“ liudytojų. Jau sausio 13-osios rytą Sąjūdžio štabe rašytojas Vytautas Petkevičius pasakė jam, jog „savi šaudė į savus“. „Aš sakau: tada bus tarptautinis skandalas! Sužinos Maskva, atsiųs komisiją ir kariuomenę, ir mes visi po poros dienų atsidursime Sibire! O jis sako: kas dabar šiame bardake ras galus? Viskas bus suversta rusams, tuo ir baigsis...”

Naujoji Paleckio byla — argi ne “gydytojų–nuodytojų”, kuriuos buvo nupirkusi amerikiečių žvalgyba, byla?

Ir tai vyksta dabartinėje Lietuvoje, kurioje demokratija esą nugalėjo galutinai ir negrįžtamai. Perfrazuosime žinomą citatą: Pabaltijis gali išbėgti iš “sovietizmo”, bet “sovietizmas” iš Pabaltijo — niekada.

Paskutinė informacija priverčia atkreipti dėmesį į dar vieną svarbų faktą: RF tyrimų komiteto veiksmai akivaizdžiai dirgina Lietuvos teisėsaugininkų nervus. Lietuvos užsienio reikalų ministras Linas Linkevičius jau perspėjo juos, kad nuo šiol į Rusiją ir jos “šalis–satelites” jiems vykti neverta. Beje, ar tai reiškia, kad kitose šalyse prokurorai ir teisėjai gali jaustis saugiai?

Buvę Lietuvos TSR partijos funkcionieriai Juozas Jermalavičius ir Mykolas Burokevičius taip pat galvojo, kad suvenerios Baltarusijos teritorijoje jie yra saugūs. Tačiau lietuviškosios specialiosios tarnybos sugebėjo išvogti juos ir atgabenti į tėvynę, kur abu buvo nuteisti kalėti už bandymą organizuoti “valstybinį perversmą” 1991 metų sausio įvykių metu.

Gal Jermalavičiaus ir Burokevičiaus šmėklos neduoda ramiai miegoti sausio 13-osios bylos dalyviams? Ar nebūkštauja jie, kad dabar juos pasieks kaulėta FST (ФСБ) ranka? Galų gale, viskas šiame pasaulyje apsisuka ratu.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 6 — id: `scraped:rubaltic_lt:2c2cd826e99c8bee`

**Title:** Lenkija ir Suomija atsisakys Lietuvos SGD terminalo paslaugų — Rusijos dujos pigesnės

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvoje skelbiama eilinė dviejų menkų suskystintų gamtinių dujų partijų iš Klaipėdos terminalo pardavimo Suomijai „sėkmės istorija“. Vilniaus planuose pardavinėti Independence produkciją ir Rytų Europai per Lenkiją, tačiau įgyvendinti šių planų nepavyks. Pirma, Lenkija ir Skandinavijos šalys turi savo SGD terminalus ir dujų transportavimo sistemas, antra — daug naudingiau pirkti rusiškas dujas, tad pati Lietuva praeitais metais trečdaliu sumažino SGD pirkimą ir padidino iš RF gaunamų vamzdinių dujų apimtį. Tokiomis sąlygomis „įbrukti“ Baltijos regiono kaimynams Independence produkciją galima tik svajonėse.

Lietuvos elektros energijos ir dujų tiekimo kompanija „Lietuvos energijos tiekimas“ pardavė suomių Gasum du mažos apimties SGD krovinius. Sensacijos — nė kvapo, tačiau Lietuvoje tvirtinama, jog „kipšas slypi smulkmenose“. O smulkmenos liudija, kad ne už kalnų didelė pergalė energetikos fronte.

LET generalinio direktoriaus Manto Mikalajūno žodžiais, svarbus pats faktas, kad jo firma pradėjo bendradarbiauti su nauju klientu — suomių dujų kompanija Gasum, ir lai nedidelės SGD perkrovimų per Klaipėdą apimtys nieko nejaudina. „Tai iki šiol labiausiai intensyvus laikotarpis prekybos SGD rinkoje Lietuvoje mažais kiekiais, — tvirtina Mantas Mikalajūnas. — Vien tik per tris savaites jūs keturis kartus perkrovėte SGD įvairiems klientams. Jeigu panašius tempus pavyks išlaikyti ir ateityje, — 2019 metai gali tapti rekordiniais perkraunant Lietuvoje mažų apimčių SGD.“

Pasiekti rekordo pradedant nuliu, kaip žinia, nesudėtinga. Bet kuris rezultatas gali tapti „rekordiniu“. „Lietuvos energijos tiekimo“ kompanijos veikla — būtent šis atvejis.

„Sudėtinga kalbėti apie perkrovimų didėjimą informacijos ir dviejų mažų partijų pagrindu,“ — pažymi Nacionalinės energetikos saugumo fondo direktoriaus pavaduotojas Aleksejus Grivač. Eksperto nuomone, SGD bunkeravimo poreikiai šiame regione augs, tačiau ir konkurencija smarkiai sugriežtės, ypač po to, kai Rusijoje bus įvestos rikiuotėn dvi vidutinio tonažo gamyklos (kompresorių stoties „Portovaja“ rajone ir Vysocke). Neužmirškime, kad nuosavus SGD terminalus nori turėti Suomija ir Estija.

„Suomiai neturi priimamojo SGD terminalo, ir jei Lietuva parduoda SGD suomių kompanijoms, tai nereiškia, kad jos pateks būtent į Suomiją, — pažymi Nacionalinio energetinio saugumo fondo vedantysis analitikas Igoris Juškovas. — Apie kažkokias stambias apimtis čia jokiu būdu negali būti kalbos.“

Europos SGD rinka, lyginant su Azija, tampa vis labiau konkurencinga. Nedidelio pelno sulaukia ir LET kompanija, tačiau nereikia manyti, kad ji nutvėrė Dievą už barzdos.

„Lietuva nėra stambus perkrovimo punktas, — atsako Igoris Juškovas. — Stambūs punktai — Olandija, prancūzų uostai ir Belgijos SGD terminalas Zeebriugge, kuris teikia perkrovimo paslaugas „Jamalui–SGD“. Viskas, ką mes matome Lietuvoje, — tai mažiausi pirkimai iš SGD terminalo ir Rusijos vamzdinių gamtinių dujų pirkimai. Ir daugybė visokiausių skambių pareiškimų. Realybėje Lietuva nėra joks SGD langas į Europą. Tai — muilo burbulas.“

Tačiau liūdnas „energetinės nepriklausomybės“ rezultatas, kurį aprašė Juškovas, netrukus keisis. Apie tai pareiškia SGD terminalo Klaipėdoje operatorius Klaipėdos Nafta. Kompanijos vadovo Mindaugo Jusio žodžiais, Independence importo apimtis daugiau kaip du kartus padidins po 2021 metų, kai bus įvesti rikiuotėn dujotiekiai į Lenkiją ir Suomiją.

„Mes matome tarptautinių prekybos namų suinteresuotumą naudotis šia infrastruktūra — terminalo ir tiesiamų dujotiekių, — siekiant įsitvirtinti Centrinės ir Rytų Europos dujų rinkose.“

Taigi sumanymas paprastas: po 2021 metų redujofikuotos SGD iš Klaipėdos keliaus dujotiekiais į Lenkiją ir Suomiją, o Lietuva taps dujų paskirstymo centru. Tai, žinoma, Mindaugo Jusiaus manymu. Realybėje jo sumanymas neišlaiko jokios kritikos.

Atvejis su Lenkija kvepia anekdotu. Pirma, lenkai turi savo SGD terminalą Svinousce. Antra, jie patys neatsisakytų tiekti lietuviams dujas statomu dujotiekiu.

Igoris Juškovas nesupranta, kokiu būdu tas dujotiekis padės Lietuvai tapti dujų paskirstymo centru. „Nevalia sakyti, kad tu gali tapti paskirstytoju tik todėl, kad per tave kažkas praeina, — tvirtina ekspertas. — Tame punkte pirmiausia kaupiamos dujos ir vyksta prekyba, o ne šiaip perkrovimas. Lietuvoje reikalingų dujų saugyklų nėra.“

Tikrieji punktai yra Nyderlanduose ir Didžiojoje Britanijoje. Prie jų gali prisijungti Vokietija — ji turi saugojimo galingumus, į juos patenka didelės dujų apimtys. Ten gali vystytis prekyba. Lietuva ir Lenkija, Juškovo nuomone, net labai norėdamos tokiais punktais negali tapti.

„Norint tapti punktu, be dujų importui ir paskirstymui skirtos infrastruktūros būtina turėti naudingas tiekėjų sąlygas, — priduria Aleksejus Grivač. — Kol SGD Rytų Europos rinkoje gerokai brangesnės už rusų vamzdines, lietuvių svajonės taip ir liks svajonėmis.“

Tas pats ir su statomu dujotiekiu Balticconnector, kuris sujungs Estiją su Suomija.

„Vargu ar per Balticconnector eis kažkokios stambios apimtys, — mano Igoris Juškovas. — Suomija kuria alternatyvius dujų tiekimo šaltinius. Čia ta pati istorija, kaip su Klaipėdos SGD terminalu — jūs jį turite, bet juo jūs nelabai naudojatės. Kaliningrado redujofikacijos terminalas tos pačios serijos: tai atsarginis variantas, tiekimas vykdomas vamzdžiais.

ES iš visų Europos šalių reikalauja turėti mažiausiai tris tiekimo šaltinius, o suomiai praktiškai visiškai priklauso nuo Rusijos. Dabar jie paklos vamzdį, nori įsigyti savą SGD terminalą — štai ir įvykdys ES reikalavimą.“

‚Jeigu SGD netaps pigesnėmis už vamzdines rusų, kas mažiau tikėtina, vamzdis bus tuščias“, — trumpai komentuoja situaciją Aleksejus Grivač.

Lietuvos valdžių „žaisliukas“ Klaipėdoje tampa nereikalingas joms pačioms. Ir negi jis bus reikalingas dar kam nors?

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 7 — id: `scraped:rubaltic_lt:b731c22f8d9b8086`

**Title:** Rusijos atsakas į „Sausio 13-osios bylos“ nuosprendį bus labai rimtas

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuva eilinį kartą mini tragiškų įvykių prie Vilniaus televizijos bokšto metines, o jau kitą mėnesį bus paskelbtas nuosprendis „Sausio 13-osios byloje“. Tikėtina, jog teisiamieji Jurijus Melis ir Genadijus Ivanovas bus pripažinti kaltais, tačiau tai nereiškia, kad tyrimas bus užbaigtas. Apie tai, kas yra masiškų žudynių naktį iš sausio 12 į 13-ąją kaltininkai ir kokios Rusijos reakcijos gali sulaukti Lietuva už nuosprendį Rusijos piliečiams dėl susidūrimo prie Vilniaus televizijos bokšto, analitiniam portalui RuBaltic.Ru papasakojo žinomas Rusijos istorikas, publicistas, filosofas, knygos „Lietuviškasis kalėjimas“ autorius Valerijus IVANOVAS.

— Pone Ivanovai, Jums sausio 13-oji — neabejotinai žinoma data. Kokiais jausmais Jūs sutikote 28-ąsias tragiškų įvykių prie Vilniaus televizijos bokšto metines?

— Pasitikau kaip istorikas ir filosofas, kuris žino, kad visi procesai vyksta pagal tam tikrus dėsningumus, turi savo pradžią ir pabaigą. Viskas šiame pasaulyje pavaldu tokiai tvarkai.

Aš jau suvokiau, jog būtent po 28 metų užsibaigė tam tikras ciklas: tragedija prie Vilniaus televizijos bokšto įvyko naktį iš šeštadienio į sekmadienį.

Aš galiu tai tvirtinti, nes ne tik dalyvavau tuose procesuose, bet ir dėmesingai juos analizavau (mano išsilavinimo tokiems tikslams pakanka). Būtinybės pagal Maskvos įsakymą įvesti kariuomenę nebuvo. Buvo galima viską išsiaiškinti taikiai ir ramiai, be kraujo praliejimo.

— Jūsų žodžiai susišaukia su „Sausio 13-osios byloje“ kaltinamo Jurijaus Melio žodžiais. Jo manymu, tarybine kariuomene Vilniuje buvo pasinaudota nusikalstamu būdu.

— Visiškai sutinku! Ir čia esmė ne tame, kaip pasielgė Vilniaus garnizono vadas Vladimiras Uschopčikas. Jis vykdė įsakymą — jis jį vykdė. Čia nebuvo jokios saviveiklos. Kariuomenė negali veikti savo nuožiūra, ji pavaldi vyriausiajam vadui. Be įsakymo niekas nebūtų dalinio išvedęs.

— Pažvelkime giliau. Egzistuoja versija, jog TSRS prezidentas Michailas Gorbačiovas buvo pasiruošęs ir net norėjo išleisti Pabaltijį...

— Būdamas judėjimo už šalies vienybės išsaugojimą lyderiu, aš 1989 metais susipažinau su dokumentu, iš kurio tapo aišku, apie ką Reikjavike kalbėjosi Gorbačiovas su JAV prezidentu Ronaldu Reiganu 1986 metų pabaigoje. Tai buvo uždaras privatus pokalbis.

Buvo aptariamos keturios temos: trečioji — Pabaltijo klausimas. Būtent tada Gorbačiovas davė sutikimą, kad Lietuva, Latvija ir Estija išstotų iš TSRS. Paskui viską tvarkė technika.

Kai kas priešinosi: „Kaip? Mes nesugebėsime!“ Jų niekas neklausė. Pirmyn su daina! Šį procesą skatino kai kurios Lietuvos TSR partinės ir jėgos struktūros. Tokia tiesa.

— Tai gal reikėtų pirmiausia teisti Gorbačiovą? Konservatorių lyderis Landsbergis neseniai pareiškė, kad Gorbačiovą reikia patraukti atsakomybėn „Sausio 13-osios byloje“ .

— Teisingai sako. Pradėti sausio 13-osios įvykių tyrimą reikėjo nuo Gorbačiovo, nes jis buvo pirmasis TSRS asmuo. Visi keliai veda link jo. Bandymai tvirtinti priešingybę — bandymai pateisinti Gorbačiovą.

Pats jis pasinaudojo strategija kito politikos veikėjo, kuris 1917 metais organizavo Kornilovo riaušių provokaciją. Vienas prie vieno! Tbilisio provokacija — iš tos pačios serijos. O viskas užsibaigė YPVK (ГКЧП) putču (taip pat Gorbačiovo avantiūra). Adekvatūs žmonės tai puikiai supranta.

— Ar galima teigti, kad įvykiai prie Vilniaus televizijos bokšto tapo YPVK repeticija?

— Žinoma. Tai senas provokacijos organizavimo būdas, jos fone vykdant tam tikrus politinius veiksmus. 1917 metais buvo uždavinys atiduoti valdžią Rusijoje bolševikams, ir Kerenskis su Trockiu to pasiekė. 1991 metais kažką panašaus padarė Gorbačiovas.

— Pagrindiniai sausio 13-osios mito sergėtojai yra „konservatoriai–landsbergininkai“. Jeigu iš jų rankų iškris šalies valdymo vadžios, ar atsiras galimybė peržiūrėti tų įvykių oficialią poziciją?

— Pirmiausia, kaip žinia, tai ne mitas. Sausio 13-oji — realybė. Aukos tikrai buvo. Sakralinės aukos, padėtos ant Lietuvos laisvės aukuro, kaip dabar priimta sakyti. Tai iš anksto suplanuota priemonė, žmonės nežinojo, kad jie buvo pasmerkti.

Žinoma, sausio 13-osios įvykių atminimas tapo vienu iš ideologinių ramsčių palaikant tuos žmones, kurie juose dalyvavo. Ir jie įsikibę laikosi to gelbėjimosi rato.

Iš kitos pusės, mitai mitais, o gyvenimas teka savo vaga. Kai iš Lietuvos išvažiavo daugiau kaip milijonas piliečių, kai trečdalis gyventojų atsidūrė už skurdo ribos, kai klesti nedarbas, mitai nepajėgūs pakeisti padėties.

Be to, kaupiasi debesys. 2020 metais baigiasi Europos Sąjungos subsidijos, kurios buvo skiriamos Lietuvai pereinamuoju laikotarpiu. Ateis skolų grąžinimo laikas. Europoje, kaip žinia, dabar netrūksta problemų — ten vyksta savi destrukcijos procesai.

Vyksta kova tarp norinčių normalizuoti santykius su Maskva ir įsikibusiais į senuosius mitus. Manau, jog turi laimėti realijos.

— „Realybė, duota mums pojūčiuose“, privers Lietuvos visuomenę peržiūrėti savo santykius su Rusija?

— Peržiūrėjimo procesas jau vyksta. Rolandas Paksas lankėsi Maskvoje ir buvo susitikęs su Putinu, o Paksas — buvęs Lietuvos prezidentas. Jis taip pat yra tam tikros Lietuvos visuomenės dalies lyderis. Tiesa, jis buvo svetimkūnis toje orbitoje, kurią rėmė Landsbergio žmonės, todėl ir buvo sparčiai pašalintas iš aukščiausio valstybės posto.

Ir čia nieko nepadarysi — „landsbergininkai“ dabar labai įtakingi. Tačiau ir jie negali įveikti realybės ir panaikinti gamtos dėsnių.

— Artinasi „Sausio 13-osios bylos“ nuosprendžio paskelbimas.

— Taip. Tai įvyks vasario 18 dieną. Aš stebiu šį veiksmą.

— Manote, tuo užsibaigs tyrimas?

— Nemanau. Tašką tyrime galima padėti tada, kai nustatomi visi faktai ir objektyviai įvertintas įvykis, tuo pagrindu priimamas nuosprendis. Apie šį procesą negaliu pasakyti nieko panašaus.

Paskelbus nuosprendį, viskas tik prasidės, o ne užsibaigs.

Todėl lauksime atsakomojo Rusijos žingsnio. Man atrodo, kad atsakas bus labai rimtas.

— Dokumentai, apie kuriuos Jūs kalbate, — tie 37 tyrimų tomai, kurie buvo perduoti Lietuvos generalinei prokuratūrai1991 metų rugsėjy? Manote, Rusijoje jie išliko?

— Taip, kiek žinau, išliko jų kopijos. Neverta Lietuvai galvoti, kad ji sugriebė Dievą už barzdos ir žino absoliučią tiesą.

— O tada ko laukia Rusija? Procesas išsitęsė daugeliui metų, teisiami RF piliečiai...

— Rusija laukia kada bus paskelbtas nuosprendis.

Suprantate, 1991 metų rugsėjo 26 dieną buvo pasirašyta sutartis tarp Vilniaus ir Maskvos dėl bendro sausio 13-osios įvykių tyrimo. Deja, Lietuvos Respublika atsisakė Rusijos tyrėjų paslaugų — ji tik paėmė dokumentus ir pradėjo juos savarankiškai interpretuoti. Todėl Lietuvos Femidė paskelbs savo nuosprendį, tačiau jį gali paskelbti ir kita šalis.

— Šiame kontekste verta priminti naujieną, jog Rusijos tyrimų komitetas iškėlė baudžiamąją bylą Lietuvos prokurorams ir teisėjams, tiriantiems „Sausio 13-osios bylą“.

— Matyti, tam yra kažkokios priežastys. Tyrimų komitetas neiškels baudžiamosios bylos tuščioje vietoje, taip kaip Lietuvos teisėsaugininkai man bandė „prikirpti“ šnipinėjimą Maskvos naudai. Absoliučiai išgalvotas kaltinimas tikslu neutralizuoti mane, nors aš nelendu į Lietuvos politiką.

— Kaip manote, ar Jūsų sulaikymas gali turėti ryšį su nuosprendžio paskelbimu „Sausio 13-osios byloje“?

— Žinoma, tai politinis žingsnis. Jokio nusikaltimo nebuvo ir nėra, aš niekada neužsiminėjau šnipinėjimu. Aš nevagiu svetimų paslapčių, aš užsiiminėju analitika.

Taip, mano sulaikymas turi ryšį ir su nuosprendžio „Sausio 13-osios byloje“ paskelbimu, ir su Lietuvos prezidento rinkimais gegužės mėnesį. Dalia Grybauskaitė išeina — į jos vietą taiko premjeras Saulius Skvernelis.

Bet aš nenoriu būti tuo baltuoju žirgu.

— Sausio 13 dieną Lietuvoje įteikiamos laisvės premijos „miško broliams“...

— Taip. Kaip tik dabar įteikia — aš stebiu transliaciją (interviu su Valerijum Ivanovu įrašėme sausio 13 dieną — RuBaltic.Ru pastaba). Aš nenoriu pasakyti, kad šie žmonės neturėjo teisės kovoti už savo idealus, tačiau aš žinau tų įvykių užkulisius.

Ant daugelio šių partizanų rankų kraujas tų dviejų šimtų tūkstančių žydų, kurie buvo nukankinti Lietuvoje. Jie žudė savo tautiečius lietuvius, kurie rėmė tarybų valdžią. Žudė ne tik vyrus, bet ir moteris, vaikus, senelius. Dabar jiems įteikiami apdovanojimai.

Как-то это все некрасиво. По жертвам трагедии 13 января мы скорбим, а по жертвам массовых убийств в военный и послевоенный период — нет.

Kaip visa tai negražu, aš nesu blogos nuomonės apie lietuvius. Mano velionė žmona, padovanojusi man kūdikį, buvo lietuvė. Tai protinga, racionali tauta. Aš gerai ją pažįstu ir gerbiu. Tiesiog kažkas ilgai vedžioja lietuvius už nosies.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 8 — id: `scraped:rubaltic_lt:596a37404f604e73`

**Title:** „Užmiršo Gorbačiovą“. Vytautas Landsbergis nori pasodinti buvusį TSRS prezidentą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Kaltinimus Gorbačiovo adresu Lietuvos politikos „patriarchas“ meta ne pirmą kartą. 2011 metais jis pergyveno, kad Vakaruose Gorbačiovas yra gerbiamas, nors pagarbos visiškai nenusipelnė. „Iki šiol pasaulyje daugelio smegenys neprasiskalavo, kai kas mano, jog kalėjimo reformatorius buvo išvaduotojas“, — tada pasakė Landsbergis.

Pirmojo posttarybinės Lietuvos vadovo pasipiktinimas suprantamas. Jis niekada nesusitaikys su tuo, jog pagrindiniu antitarybinės epopėjos didvyriu tapo ne jis — pagrindinis politikos veikėjas pirmosios respublikos, kuri paskelbė pasitraukimą iš Tarybų Sąjungos, — o Gorbačiovas. Tame ir esmė jo užuominos. Negarbinkit „kalėjimo prižiūrėtojo“ — garbinkit mane, vaduotoją!

Nekelia abejonių, jog senukas Landsbergis galutinai įsikalė sau į galvą, kad naujoji istorija ne iki galo įvertino jo asmenybės mastą. Pyktis ėmė skverbtis per visus plyšius.

Michailą Gorbačiovą galima tik užjausti. Negi ne jis pagimdė Pabaltijyje „liaudies frontus“, kuriais rėmėsi kovodamas su konservatyviais TSKP sluoksniais? Negi ne jam dėmesingai vadovaujant tvirtėjo lietuviškasis Sąjūdis, kurį visokeriopai rėmė „pertvarkos darbų vykdytojas“ Aleksandras Jakovlevas? Ar ne jis nesiėmė jokių priemonių, kai Pabaltijo separatistai atvirai rėkė, kad TSRS, panašiai kaip Kartageną, būtina sugriauti?

Ir štai jis, dėkingumas. Buvo reformatorius (tegul jau ne vaduotojas), o tapo nusikaltėliu.

Savo sąsają su sausio 13-ąja Gorbačiovas, kaip žinia, neigia. „Alfą“ į Lietuvą jis esą nesiuntęs. O kas siuntė? Pagal jo versiją, tie žmonės, kurie jau nesiskaitė su šalies prezidentu ir norėjo jį pakišti, sukruvinti, primesti jam faktą. „Aš nežinau, kas vykdytojai, tačiau akivaizdu, kad be Kriučkovo ir Jazovo nebuvo apsieita“, - nedviprasmiškai pateikia užuominą Gorbačiovas.

Tuometinio TSRS gynybos ministro, maršalo Jazovo nuomonė šiuo klausimu kitokia. „Tai žmogus kareiviško ir tarybinio raugo, todėl išduoti savo vyriausiąjį vadą jis negalėjo, — interviu analitiniam portalui RuBaltic.Ru pasakojo Rusijos žurnalistė, knygos „Kas ką išdavė“ autorė Galina Sapožnikova. — Tačiau iš jo reakcijos į mano klausimus buvo galima suprasti, kad pastatyti Lietuvą į vietą jam įsakė Gorbačiovas, ir buvo priimtas nutarimas įvesti Vilniuje ypatingą stovį.“

TSRS VSK 7-osios valdybos „A“ grupės vado pavaduotojas Michailas Golovatovas taip pat tvirtina, kad įsakymas buvo gautas iš Gorbačiovo: „Vadovauti mūsų būriui, pagal Politinio biuro arba vyriausiojo karinių pajėgų vado įsakymą, galėjo tik VSK vadovas.“

Apie Gorbačiovo sąsają su tragedija knygoje „Lietuviškasis labirintas“ smulkiai rašo Lietuvos komjaunimo ir tarybinis partijos veikėjas Vladislavas Švedas, kuris „Sausio 13-osios byloje“ yra kaltinamųjų sąraše. Perfrazuosime patį Gorbačiovą: visiškai akivaizdu, kad be jo šioje situacijoje „neapsieita“.

Tačiau nereikia viskuo kaltinti tik Gorbačiovą. Pagrindinių tragedijos prie Vilniaus televizijos bokšto kaltininkų vardai seniai žinomi.

Gorbačiovas suteikė jam unikalią galimybę paversti Lietuvą „tarybinės agresijos auka“. Visa kita tvarkė technika.

Mitas apie „tarybinę agresiją“ prie Vilniaus televizijos bokšto tapo vienu iš lietuviškąją nepriklausomybę remiančių bokštų. „Landsbergininkai“ tą bokštą kaip akies vyzdį saugoja jau 28 metus, užkišdami burnas visiems, kas išdrįsta suabejoti oficialia versija. Tačiau pačiam Landsbergiui to maža.

Jo nuomone, Lietuvos teisėsaugos organus „sukaustė kažkokios jėgos“. „Egzistuoja nusistatymas, o gal ir gniaužtai, apribojimai, kurių neįmanoma ištirti, - pranešė politikas pristatyme savo naujos knygos iškalbingu pavadinimu „Naujai atitirpę Sausio 13-osios pėdsakai ir mirtinai abejingas lietuviškas teisingumas“.

Tiksliau nepasakysi.

Žuvęs A.Kanapinskas ruošėsi mesti link tarybinių kariškių sprogmenų paketą, tačiau atsitiktinai susisprogdino. Argi jo įrašymas į „okupantų“ aukų sąrašą nėra nusistatymas?

Lietuvis Ignas Šimulionis buvo sušaudytas jau po mirties, jo kune buvo rastos septynios įvairaus kalibro kulkos. Kaltinti tuo specnazo ir TSRS karinių pajėgų karius – ar ne nusistatymas?

Medicinos ekspertų akte apie Loretos Asanavičiūtės mirtį pasakyta, kad tanko vikšras, kurio plotis 58 cm, paliko ant jos kūno „odos įdrėskimus, pagal formą panašius į keturkampius.“ Tuos, kurie rašė šį aktą, „nesukaustė kažkokios jėgos“?

O Lietuvos respublikinio teismo medicinos biuro viršininką A.Garmų? 1991 metų vasario 6 dieną jis pasirašė pažymą „Apie sausio aukų žūties priežastis“, kuria patvirtino, kad Romualdas Jankauskas – dar vienas žmogus, kurį esą pervažiavo tarybinis tankas, - iš tiesų jis žuvo autoavarijos metu.

Kai Galina Sapožnikova išsiuntė Garmui minėtos pažymos kopiją, šis atsakė: „Aš ją matau pirmą kartą, nepamenu, kad kažką panašaus būčiau pasirašęs. Prašau daugiau manęs netrukdyti.“ Įdomu, ar jį jokios jėgos nekaustė? Nebuvo jokių gniaužtų ir apribojimų?

Akivaizdu, jog visa tai Vytautą Landsbergį tenkina. Bet kad teisėsaugininkai Gorbačiovo neapklausė — netvarka.

Šaukimą atvykti į teismą buvęs tarybinis lyderis gavo, tačiau atvažiuoti į Lietuvą atsisakė. Dalyvauti lietuviško teismo spektaklyje jis kategoriškai atsisakė net kaip liudytojas, todėl Landsbergio pretenzijų esmė nevisai suprantama.

Knygoje „Aušros purpurinės“ buvęs Lietuvos premjero pavaduotojas Romualdas Ozolas rašo, kad Landsbergio cinizmas 1991 metais neturėjo ribų. Po 28 metų mažai kas pasikeitė.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 9 — id: `scraped:rubaltic_lt:a51f865374dc9319`

**Title:** Pabaltijo valdžios slepia NATO okupantų nusikaltimus

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Pabaltijyje dislokuoti Amerikos kareiviai nupl ėšė Lietuvos v ė liav ą nuo prokurat ū ros pastato Kaune . Tokia informacija ne pirm ą kart ą pasiekia ž iniasklaid ą, ta č iau Lietuvos vald ž ios , kaip visada , susilaiko nuo komentar ų. U ž Lietuvos valstybinio simbolio i š niekinim ą, kaip ir u ž kitus Pabaltijo š alyse į vykdytus nusikaltimus , NATO kari ū nai nebaud ž iami .

Kas įdėmiai seka Lietuvos naujienas, neabejotinai prisimins istoriją apie amerikiečius ir nuplėštą vėliavą. Tai įvyko dar 2016 metų balandžio mėnesį. Kai tapo žinoma, kad vandalizmo aktą įvykdė “draugai” iš JAV, Lietuvos valdžios nutarė užslaptinti informaciją.

Nei vietos policijos, nei bendroje respublikos VRM policijos departamento suvestinėje nepasirodė jokios informacijos. Vėliau paaiškėjo, jog veltui buvo bandyta nutylėti: informacija vis tiek pateko spaudon.

Apie nuplėštą Kaune vėliavą pranešė “Kauno diena”, tačiau smulkiau apie įvykį nepavyko sužinoti. Būtent kas nusprendė užslaptinti informaciją, nebuvo pranešta. Ar girti buvo amerikiečiai? Taip pat nežinoma, nors geriau būtų, kad išniekinimu jie būtų užsiėmę išgėrę. Jeigu iš JAV atvykę “pasaulio kariai” blaiviame stovyje niekina Lietuvos valstybinius simbolius, tai jos santykiai su sąjungininkais nekokie.

Neverta klausti, ar bandė Lietuvos teisėsaugininkai nubausti kaltuosius. Kaip visada tokiais atvejais, sprendimas vienintelis — tylėti.

Prisiminkime, už kokią veiką kaltu buvo pripažintas opozicijos politikas Algirdas Paleckis. Taigi už tai, kad savo “viešu įžeidžiančiu pareiškimu” palietė sausio 13-osios tragedijos aukų atminimą, nors apie žuvusius ir jų artimuosius Paleckis niekada nekalbėjo nepagarbiai. Už ką metus kalėjo istorikas Valerijus Ivanovas? Vėl už tai – už nepagarbą kovotojams už Lietuvos laisvę ir nepriklausomybę.

Suprask: abejoti oficialia tragedijos prie Vilniaus televizijos bokšto versija — įžeisti tautos atmintį, o jei išniekinamas valstybinis simbolis, nėra nieko žeidžiančio.

Tiesa, atsirado nemąstančių liudytojų, kurie po incidento kreipėsi į policiją. Tačiau teisėsaugininkai greičiausiai jiems paaiškins, kad valstybinio simbolio išniekinimas nėra žeidžianti veika.

Ir ko jaudintis? Visi gyvi ir sveiki.

Rygoje, pavyzdžiui, 2016 metais girti britų kariūnai sumušė Akselį Aizkalį, o kiti NATO “gynėjai” sudaužė taksi vairuotojo mašiną. 2015 metais amerikiečių kareivis sukėlė eismo įvykį, kurio metu nukentėjo penki žmonės, tame tarpe ir Latvijos autolenktynininkas Vasilijus Grezinas. Neatsilikti stengiasi ir čekai: Klaipėdos policininkams, siekiant sutramdyti įsisiautėjusius čekų kariškius, teko griebtis elektrošokerių.

Esant norui, visus incidentus galima pateisinti. Susipešė, pažeidė eismo taisykles – kam neatsitinka? Net gali būti, jog peštynėse dalyvavę NATO kariškiai visiškai nekalti – juos išprovokavo pabaltijiečiai. Tačiau kai kuriuos užsienio kariškių veiksmus, atsižvelgiant į transatlantinį solidarumą, paaiškinti sunku.

2014 metų vasarą Ventspilio meras Aivars Lembergs buvo priverstas skųstis NATO jūreivių elgesiu savo mieste NATO generaliniam sekretoriui Andersui Fog Rasmusenui. Pasak Lembergs, NATO kariškiai elgėsi kiauliškai, nepaisė įstatymų, viešai gėrė alkoholį, plėšė nuo klombų prostitutėms gėles ir gamtinius reikalus atliko viešose vietose.

2017 metų birželio 20 dienos naktį Lietuvos policijos patrulis Vilniaus centre pamatė neįprastą vaizdą: “broliškos” kariuomenės kariškis šlapinosi ant respublikos Vidaus reikalų ministerijos sienos. Ir visiškai nekreipė dėmesio į greta atsidūrusius teisėsaugininkus. Tačiau šį kartą ir santūriems lietuviams pritrūko kantrybės: su pažeidėju buvo pravestas pokalbis ir net išdrįsta jam skirti 15 eurų baudą.

Žinoma, šlapimas amerikiečių kariškiams nesilaiko ne tik Pabaltijo teritorijoje. Praeitų metų lapkrity tapo žinoma, kad jie “apšlapino Norvegiją” — atliko ne tik mažus, bet ir didesnius reikalus prie mokyklų, vaikų darželių ir sporto aikštelių ir darė tai taip aktyviai, jog dėmesį į situaciją atkreipė Norvegijos karinių pajėgų majorė Mariana Be, atsakinga už aplinkos apsaugą. Ji su liūdesiu pažymėjo, kad “norvegams tenka šalinti tai, ką palieka kareiviai”.

Piktinosi ir fermeriai, kurių sklypus subjauriojo NATO technika. Buvo pranešimų apie sulaužytas tvoras, pažeistas elektros energijos linijas, su šaknimis išrautus medžius. Beje, Trident Juncture mokymai Norvegijoje sukėlė daug nemalonių incidentų. Vietos gyventojai pateikė apie 450 skundų NATO kareivių ir karininkų adresu, o oficialiam NATO atstovui Eisten Kvarving teko atsiprašinėti.

Atkreipiame dėmesį, jog kalba eina apie Norvegiją — toli gražu ne paskutinę šalį Šiaurės aljanse. Jeigu ir ten neapsieinama be “ekscesų”, tai Pabaltijy užsienio kariškiai gali elgtis visiškai laisvai.

Praėjusių metų įvykiai visa tai dar kartą patvirtino.

Mažiau nei per dvi karinių mokymų Saber Strike Lietuvoje 2018 metais savaites įvyko trys avarijos, kuriose dalyvavo įvairių šalių NATO kariškiai. Rugpjūty kariškiai išprovokavo eismo įvykį, kuriame nukentėjo vyriškis ir penkiametis vaikas, o metų pabaigoje NATO sunkvežimis susidūrė su lengvąja mašina. Avarijos metu žuvo dvi merginos.

Dar vienas amerikiečių kariškis praėjusią vasarą susimušė Kaune su dviem Azerbaidžano piliečiais. Policijoje buvo pažymėta, kad visi muštynių dalyviai buvo neblaivūs, tačiau daugiausia alkoholio buvo rasta amerikiečio kraujyje...

Ypač nepasisekė tiems, kurie tupi mažuose provincijos miesteliuose — nuobodu ir tiek. Sunku sutikti su Pabaltijo politikais, kurie teigia, kad NATO kariškiai Lietuvoje, Latvijoje ir Estijoje jaučiasi kaip namuose.

Greičiau atvirkščiai — kaip svetimoje, jiems tolimoje teritorijoje. Be to, namuose už savo teisėtvarkos pažeidimus tenka atsakyti pagal įstatymus. O Lietuvoje, Latvijoje ir Estijoje galima naudotis visomis okupacinės kariuomenės privilegijomis.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 10 — id: `scraped:rubaltic_lt:7fa3ed3091e8dabe`

**Title:** Lietuvoje prieš paskelbiant nuosprendį tarybiniams kariškiams vyksta kitaminčių „apvalymas“

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvos policija sulaikė 71 metų Valerijų Ivanovą — Rusijos istoriką ir publicistą, jau praleidusį Lietuvos kalėjime keletą metų už tai, jog išsakė savą 1991 metų sausio 13-osios dienos įvykių versiją, kuri kertasi su oficialia. Kitą dieną tapo žinoma, jog areštuotas Algirdas Paleckis — buvęs Lietuvos socialistinio liaudies fronto lyderis, kuriam jau buvo iškelta baudžiamoji byla už tai, jog jis teigė, kad sausio 13-ąją į žmones prie Vilniaus televizijos bokšto šaudė Sąjūdžio separatistai. Prieš paskelbiant nuosprendį tarybiniams kariškiams „Sausio 13-osios byloje“ Lietuva pradeda seriją represijų tų disidentų atžvilgiu, kurie pasiruošę įvardinti tikruosius 1991 metų masiškų žudynių kaltininkus.

Gruodžio 18-osios vakare Rusijos pilietis Valerijus Ivanovas parašė tinklalapyje, kad į jo butą Vilniuje bandė įsibrauti nepažįstamieji. Po kelių valandų paaiškėjo, kad publicistas ir istorikas sulaikytas, jo bute pravesta krata.

Kitą dieną Lietuvos policija pranešė, kad pas Ivanovą rastas ginklas. Lietuvos policijos generalinis komisaras Linas Pernavas papasakojo, kad kratos metu pas publicistą rastas „šaunamasis ginklas“.

Byla, kuri rengiama 71 metų Lietuvos rusų literatų ir menininkų sąjungos pirmininkui ir buvusios lietuvių–rusų–lenkų visuomeninės organizacijos „Jedinstvo“ vadovui, labai primena Valerijaus Ivanovo latvių kolegos — portalo IMHO-club.lv vyriausiojo redaktoriaus Jurijaus Aleksejevo persekiojimą.

Jo atžvilgiu latvių policija nusprendė, kad sviestas košės negadina, ir „aptiko“ Aleksejevo bute šaudmenų sandėlį. Ir dabar kaltina latvių žurnalistą kuo tik sugeba: ir pasikėsinimu į konstitucinę santvarką, ir šnipinėjimu, ir neteisėtu ginklų laikymu, ir vaikiškos pornografijos platinimu.

Atrodo, jog lietuvių specialiosios tarnybos taip pat nutarė nekreipti dėmesio į savo kaltinimų teisingumą.

Tuo pačiu metu, kai kaltinimai buvo mesti Ivanovui, paaiškėjo, kad jau virš mėnesio kalėjime laikomas buvęs Socialistinio liaudies fronto lyderis Algirdas Paleckis. Jo areštas buvo nutylimas, ir tik po Valerijaus Ivanovo sulaikymo informacija apie tai buvo pametėta žiniasklaidai.

Generalinė prokuratūra ir Lietuvos saugumo departamentas vadina Paleckį su Ivanovu nariais nusikalstamos grupės, kuri šnipinėjo Rusijos naudai. Tarp dviejų baudžiamosios bylos figūrantų tikrai daug bendro.

Tuo pačiu metu, kai kaltinimai buvo mesti Ivanovui, paaiškėjo, kad jau virš mėnesio kalėjime laikomas buvęs Socialistinio liaudies fronto lyderis Algirdas Paleckis. Jo areštas buvo nutylimas, ir tik po Valerijaus Ivanovo sulaikymo informacija apie tai buvo pametėta žiniasklaidai.

Generalinė prokuratūra ir Lietuvos saugumo departamentas vadina Paleckį su Ivanovu nariais nusikalstamos grupės, kuri šnipinėjo Rusijos naudai. Tarp dviejų baudžiamosios bylos figūrantų tikrai daug bendro.

Algirdas Paleckis žinomas tuo, jog 2010 metais metė Lietuvos radijo stoties eteryje frazę: „Kaip dabar paaiškėjo, savi šaudė į savus“, tuo pabrėždamas, jog prie Vilniaus televizijos bokšto darbavosi Sąjūdžio snaiperiai.

Už šią frazę Paleckiui buvo iškelta baudžiamoji byla pagal ką tik įrašytą į Baudžiamąjį kodeksą straipsnį „Baudžiamųjų režimų nusikaltimų neigimas“. Politikui grėsė 5 metai kalėjimo, ir tik tarptautinis pasipiktinimas tuo, jog Lietuvoje susidorojama su disidentu, privertė apsiriboti bauda.

Antrasis kitamintis, Valerijus Ivanovas, nuo 1991 metų sausio 13 dienos įrodinėja, kad į žmones prie televizijos bokšto šaudė Landsbergio provokatoriai. Už tai jis kalėjo dukart.

Pirmą kartą Valerijus Ivanovas trejus metus sėdėjo kankinimo kameroje 2x0,78 metro už tai, kad pasisakė prieš Sąjūdį ir už Lietuvos narystę Tarybų Sąjungoje. Išleistas, jis parašė knygą „Lietuviškasis kalėjimas“.

Už šiuos žodžius Valerijus Ivanovas po to, kai buvo išleistas „Lietuviškasis kalėjimas“, Lietuvos kalėjime praleido dar metus kaip žmogus, „įžeidęs sausio 13-osios aukų atminimą“.

Ir štai dabar Lietuvos valdžios dar kartą prisiminė 71 metų publicistą.

Lietuvos valdžia ruošia pavyzdinį parodomąjį teismą, kaltinamaisiais kuriame bus ne tik konkretūs kariškiai Genadijus Ivanovas ir Jurijus Melis, bet ir visa tarybinė „nusikalstama santvarka“, už kurios piktadarybes atsakinga jos teisių perėmėja Rusijos Federacija.

Pirmiesiems respublikos asmenims „Sausio 13-osios bylos“ kaltinamojo nuosprendžio svarbą neįmanoma pervertinti. Nuo to, ar viskas praeis sklandžiai, priklausys prezidento rinkimų gegužės mėnesį rezultatai, o taip pat Dalios Grybauskaitės karjera Briuselyje, apie kurią ji svajoja pasibaigus Lietuvos prezidentės kadencijai.

Nuosprendis vasario 18 dieną turi būti paskelbtas be jokių abejonių. Vertinimai šalyje — vien tik teigiami. Tarptautinių Lietuvos partnerių vertinimai — tuo labiau.

Lietuvos jėgos struktūrų veikla užsipuolant disidentus nenuosekli ir nerimastinga. Jų aktyvumo ryšys su „Sausio 13-osios byla“ puikiai matomas, ir jų pametėtas į butą ginklas negali įrodyti, kad kitaminčiai persekiojami kitais sumetimais.

Tačiau Valstybės saugumo departamentas, prokuratūra ir politiniai jėgos struktūrų kuratoriai nesupranta, kad jų veikla turi atgalinį efektą. Juk bandymai prigąsdinti disidentus, jėga užčiaupti ir labiausiai prieštaraujančius iš jų pasodinti už grotų prieš nuosprendžio Genadijui Ivanovui ir Jurijui Meniui paskelbimą — savaime įrodo, kad tarybiniai kariškiai nekalti dėl masiškų žudynių prie Vilniaus televizijos bokšto.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 11 — id: `scraped:rubaltic_lt:1e21d2436ba76930`

**Title:** Paksas: Putinui patiko Lietuvos ir Kaliningrado demilitarizavimo idėja

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Neseniai 2003–2004 metų Lietuvos prezidentas, europarlamentaras Rolandas Paksas pabuvojo Maskvoje ir pabendravo su pirmaisiais Rusijos Federacijos asmenimis (tame tarpe ir su prezidentu Vladimiru Putinu). Tėvynėje oponentai piktai kritikavo politiką, o Europos Taryboje oficialusis Vilnius dar kartą buvo paragintas grąžinti Paksui teisę dalyvauti prezidento rinkimuose. Apie pokalbį su Rusijos valdžiomis, žmogaus teisių nepaisymą Lietuvoje ir artėjančius rinkimus į Europos parlamentą buvęs Lietuvos prezidentas papasakojo analitiniam portalui RuBaltic.Ru.

— Pone Paksai, norėtųsi pradėti nuo temos, apie kurią kalba visas pasaulis. Gruodžio 11-tąją tapo žinoma, kad Prancūzijos prezidentas Emanuelis Makronas įveda ypatingąją padėtį. Jūs dabar esate Strasbūre. Ką apie tai kalbama Europos parlamento plenarinėje sesijoje?

— Pokalbio turinys priklauso nuo to, kas konkrečiai pasisako. Kalbėjo ir komisijos pirmininkas, ir vadovaujančios šalies atstovas, ir parlamento frakcijų lyderiai. Man buvo pavesta pasisakyti mūsų frakcijos vardu („Tiesioginės demokratijos laisvoji Europa“ — RuBaltic.Ru past.).

Todėl aš ir patikslinu, kad viskas priklauso nuo to, kas kalba. Jei paminėti globalizmo pozicijų prisilaikančią valdančiųjų frakciją, kuriai Briuselis viršiausias, o nacionalinės valstybės ateityje turi išnykti, tai ji nemato jokios problemos. Jos atstovai teigia, jog viskas normalu: tiesiog yra laikinų problemų, kaip pas mus buvo sakoma tarybiniais laikais. Taip ir šiandien. Viskas tvarkoj, viskas normalu.

— Dar viena pastarųjų dienų naujiena: Europos taryba eilinį kartą priminė Lietuvai slaptąjį ČŽV kalėjimą. Ir raginama Lietuvą panaudoti „visas galimas priemones, siekiant kuo greičiau gauti JAV pareigūnų diplomatines garantijas, kad būtų nutraukta savavališka pareiškėjo išvada“. Tai yra Lietuvos valdžios turi reikalauti iš JAV kažkokių garantijų. Jums neatrodo, kad toks pasiūlymas yra keistas?

— Jei kalbėti iš esmės, tai Strasbūro teismo nutarimas, kurį Lietuva norėjo apskųsti (ir apskųsti kurį nepavyko), teigia, jog kalėjimas buvo, žmogus jame buvo, jam būtina išmokėti 130 tūkstančių eurų ir t.t. Ir tas sprendimas neapskundžiamas.

Visi šie žaidimai, kuriuos mes dabar stebime, — bandymas nepripažinti atsakomybės tų asmenų, kurie buvo priėmę sprendimą. Prie to einama.

Neseniai sukako 70 metų, kai buvo priimta Bendroji žmogaus teisių deklaracija. Šią datą paminėjo daugelis šalių. Taip pat ir Lietuva, tačiau niekas nepastebėjo, kad Lietuva jau aštuonerius metus nevykdo Strasbūro teismo nutarimo piliečio Rolando Pakso klausimu.

— Prie šios temos mes dar sugrįšime, užbaikime su CŽV kalėjimais. Kažkodėl visi kalba apie Lietuvos atsakomybę, tačiau niekas neužsimena apie JAV kaltę. Lyg jos išvis nebūtų.

— Suprantate, čia kaip pažiūrėti.

Tie JAV politikai arba valdininkai, kurie užsiiminėjo tokiais reikalais, tikrai prisilaikė savo šalies įstatymų ir Konstitucijos, pagal kuriuos Valstijose tokie reikalai neleistini. Jie turėjo informaciją, jog yra šalys, kurių politikai už kažkokius dividendus su malonumu padarys tai, kas jiems bus pasakyta. Ir JAV įstatymo lyg ir bus prisilaikyta, ir tikslo bus pasiekta.

— O ką tokioje situacijoje turi daryti Lietuva? Pripažinti savo kaltę? Ponia Grybauskaitė teigia, jog tai neigiamai paveiks šalies įvaizdį.

— Žinote, viename rusų seriale yra toks personažas — sargybinis Borodač (Aleksandras Borodač iš „Mūsų Raši“ — RuBaltic.Ru past.). Jis visada savo pasisakymus užbaigia žodžiais: „Suprasti ir atleisti“. Taip reikia pasielgti ir Lietuvoje.

Taip, buvo. Taip, kaltieji patraukti atsakomybėn. Taip, daugiau to nebus. Viskas! Kito kelio nėra. Reikia arba vykdyti pasirašytas deklaracijas, arba trauktis iš Europos tarybos ir Jungtinių Tautų.

— Neseniai Europos taryba paragino grąžinti Jums teisę dalyvauti prezidento rinkimuose. Ar turite vilčių, kad oficialusis Vilnius sureaguos?

— Žinote, anksčiau aš tikėjau, kad Europos tarybos arba JT sprendimai Lietuvos politikams taps kelrodžiu. Taip turi būti. Tačiau dabar aš tuo netikiu. Kol klausimas nebus iškeltas kategoriškai, nieko neišeis. Nieko!

Daug žmonių nori balsuoti už mano kandidatūrą. Apie tai sako bendravimo su jais patirtis. Jų pilietinės teisės taip pat pažeidžiamos, nes negali atiduoti balso tam, kurį laiko tinkamiausiu.

Manau, aštuoneri metai — pakankamas laikotarpis Strasbūro teismo sprendimo įvykdymui, O 2019 metų sausio 6 dieną sukaks lygiai aštuoneri metai, kai Didžioji Strasbūro teismo kolegija priėmė šį sprendimą.

Kol nebus pareiškimo, pripažįstančio Lietuvos rinkimus nedemokratiškais (ir neligitymiais), Lietuvos valdžios situacijos nepakeis.

— Vadinasi, žmogaus teisių problema aktuali ne tik Lietuvai, bet ir Europai.

— Sutinku, kol kas Europos taryba neperžengia tam tikro barjero. Lietuvos valdžios tuo naudojasi, todėl kad visiems nenaudinga leisti dalyvauti rinkimuose stipriam kandidatui. Štai tokia karuselė.

Jau aišku, kad Strasbūro teismo nutarimai kai kuriais klausimais „bedančiai“. Tie žaidimai tęsis tol, kol iš Lietuvos nebus atimta balso Europos taryboje ir JT teisė.

— Populiariausių kandidatų 2019 metų Lietuvos prezidento rinkimuose sąraše premjeras Saulius Skvernelis, buvusi finansų ministrė Ingrida Šimonytė, finansų analitikas Gitanas Nausėda. Ar turite vilčių, kad kas nors iš jų rimtai keis Lietuvos politiką? Ar kurį nors remsite?

— Nenorėčiau užsiiminėti kurio nors iš kandidatų parama (ypač dabar). Tačiau nenorėčiau matyti, kad tęsiama daugiametė Dalios Grybauskaitės politika. O iš trijų kandidatų, kuriuos paminėjote, du tikrai tęs dabartinį kursą.

— Vadinasi, reikia paremti trečią?

— Tur būt, taip.

— Jūsų apsilankymas Rusijoje sukėlė daug triukšmo. Kai kurie žurnalistai ir politikai apie jį pasisakė labai aštriai. Po to, kai Jūs susitikote su RF prezidentu Vladimiru Putinu, ar nejaučiate Lietuvoje spaudimo?

— Aš jau ne mažas vaikas, kad kreipčiau į tai dėmesį. Man gaila, kad šį žingsnį neteisingai suprato mane gerai žinantys žmonės. O kitkas mane mažai jaudina.

Aš džiaugiuos, kad man pavyko susitikti su tokiais aukšto rango rusų politikais, kaip prezidentas, Valstybės dūmos ir Federacijos tarybos pirmininkai. Taip reikia elgtis ne tik buvusiems valdžioje, bet ir šiandien joje esantiems. Susitikinėti patiems, o ne kritikuoti tuos, kurie susitinka.

Taip, reikia susitikinėti, reikia kalbėtis. Mano mėgiamas politikas Vinstonas Čerčilis dažnai kartodavo, kad geriau kalbėtis, negu kariauti.

Žodžiu, mane menkai domina oponentų kritika. Aš jaučiu, kad elgiuosi teisingai.

— Jūs vykote į RF, kad išgirstumėte rusų nuomonę apie incidentą Kerčės sąsiauryje. Po pokalbio su pirmaisiais valstybės asmenimis Jūs jau įsivaizduojate, kas ten iš tiesų nutiko?

— Manau, Jūs ne visai tiksliai suformulavote klausimą. Aš sakiau, kad, vykdamas, turėjau du tikslus. Pirmasis — parodyti Europos politikams, kad su Rusija reikia ir galima vesti dialogą, ieškoti išėjimo iš krizės kelių. O antrasis...

Suprantate, aš svajoju, kad Lietuva ir Kaliningradas pradėtų demilitarizavimą, kad politiniais ir diplomatiniais instrumentais šiame regione būtų pasiekta stabilumo, kad šiandien ateitų investicijos, technologiniai parkai ir t.t.

Tai mano svajonė, ir link jos aš žengiau pirmą žingsnį. Rusijos prezidentui idėja patiko.

Kas dėl Ukrainos — taip, aš tikrai klausiausi.

— Po Jūsų susitikimų su RF atstovais nuskambėjo pasiūlymas sukurti neformalią darbo grupę tarp Europos parlamento ir Valstybės dūmos. Rusijos šalis, manau, neprieš. O Europos parlamentas tam pasiruošęs?

— Aš antra diena Strasbūre, mano padėjėjai jau studijuoja šį klausimą. Pažiūrėsime, kaip reikalai klostosi Europos parlamente. Tada ir pažiūrėsime, kokius žingsnius galima žengti.

Manau, tai geras pasiūlymas. Kaip sakoma, darbinis. Ir nepriklausomai nuo valios politinių jėgų, kurios šiandien dominuoja parlamente, atsiras parlamentarų, kurie susidomės šia idėja. Čia juk protingi žmonės. Jie supranta, kad rinktis galima žmoną, o kaimyną pagal žemėlapį duoda Dievas. Su kaimynais reikia gyventi taikiai, santarvėje.

— Beje, jėgų išsidėstymas Europos parlamente taip pat gali pasikeisti — artėja rinkimai. Ar su optimizmu laukiate jų?

— Taip.

— Jūs kalbate apie dešiniąsiais partijas?

— Aš kalbu apie tas partijas, kurios mato Europą kaip lygių valstybių sąjungą, kurioje kiekvienas gali įtakoti sprendimų priėmimą. Jos gali būti dešiniosios, gali būti ir kairiosios.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 12 — id: `scraped:rubaltic_lt:fff3596580205bf8`

**Title:** Šuoliuojantis kainų augimas taps lietuviams naujametine dovana

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Pabaltijo respublikos ekonominės „sėkmės“ istorija priartėjo prie finišo. Lietuvos valdžios jau pateikė šalies gyventojams „naujametinę dovaną“, oficialiai pranešdamos apie nusimatantį elektros energijos ir dujų kainų augimą. O kaip kitaip reguliuoti vidinę rinką, kai paklusni priklausomybė nepalieka vietos ekonominiam tikslingumui?

Lietuvos energetinės rinkos dalyviai ir Valstybinė kainų ir energetikos kontrolės komisija pareiškė, jog elektros energijos ir dujų kainos gyventojams 2019 metais neišvengiamai augs. Prognozuojama, jog elektros energijos kaina padidės 15–18 proc.

Nesuteikia vilčių ir pareiškimai šia tema Lietuvos energetikos ministro Žygimanto Vaičiūno, pavadinusio situaciją energijos išteklių rinkoje „šokiruojančia“. Tačiau energetinės žinybos vadovas mano, kad verslas prie to jau priprato, nes visus metus, pirkdamas elektros energiją rinkoje, patiria nuostolius, o gyventojai dėl atidėliotino efekto neiškart pajus „naują realybę“.

Beje, čia su ministru sunku sutikti. Dujų ir elektros energijos kainų augimas verslui tiesiogiai įtakos gyventojų pragyvenimo lygį.

Maža to, jog lietuviai parduotuvėse susidurs su naujomis kainomis, — prie jų prisidės papildomos išlaidos mokant už elektros energiją. Todėl nereikia stebėtis, kai lietuviškieji vartotojai socialiniuose tinkluose, lygindami tų pačių prekių kainas, pavyzdžiui, su Norvegija, pasipiktinę konstatuoja dešimčių eurų skirtumą.

Visa tai ekonomiškai pagrįsta. Juk viena iš prekių ir paslaugų savikainos sudėtinių dalių yra elektros energija. Norvegija turi savus jos gamybos šaltinius. Dėka tolygiai visoje šalyje išdėstytų hidroišteklių, praktiškai visą šalies elektros energiją (81 milijardas kw/val per metus) pagamina hidroelektrinės.

Lietuvoje dėl praktiškai visiško savos energijos nebuvimo energijos balansas kuriamas importuojamų išteklių pagrindu. Taip buvo nevisada. 2004 metais įstodama į ES, šalis savo noru atsisakė savojo energetinio suvereniteto, įsipareigodama 2009 metais uždaryti galingiausią Pabaltijyje Ignalinos AE (eksploatavimo terminas — iki 2032 metų), kuri gamino 80 proc. respublikai reikalingos elektros energijos. Eksportui elektros energiją tiekusi šalis visiškai staiga ėmėsi ją importuoti.

Po visiško AE sustabdymo 2009 metais, ėmė sparčiai augti užsieninės valstybės skolos. Jeigu 2008 metų pabaigoje jos sudarė 4,7 milijardo eurų, tai, Finansų ministerijos valstybinio iždo departamento duomenimis, 2017 metų pabaigoje skolos ūgtelėjo iki 17 milijardų (41,5 proc. BVP).

Ir kontroliuoti ją kasmet vis sudėtingiau. Dar 2016 metais Lietuvos valstybės kontrolė pirmą kartą pateikė valstybės sektoriaus finansinio stabilumo prognozę su ilgalaikės perspektyvos analize. Išvada nedžiugino. Valstybės įsiskolinimų lygis pripažintas „nestabiliu“, o, be to, prognozuotas jo spartus augimas, pradedant 2024 metais, dėl išlaidų, susietų su gyventojų senėjimu, o taip pat su „sniego gniužulo“ efektu. Pagal finansinės žinybos prognozes, per šį dešimtmetį skolos išaugs 20 proc. BVP. Tokiu būdu, jos priartės prie Maastrichte kriterijų, pagal kuriuos valstybės, ES narės, skolų slenkstis neturi viršyti 60 proc. BVP.

Štai ir tenka Pabaltijo respublikai kasmet užsienio rinkoje skolintis milijardus eurų tikslu padengti einamasias skolas. Šios lėšos nepatenka į šalies ekonomiką, jos iškart skiriamos užsieninių skolų restruktūrizavimui.

O jeigu į skolų situaciją pažvelgti per numatomą nuo 2020 metų europietiškų dotacijų mažinimo prizmę, situacija atrodys visiškai niūriai.

Atrodytų, esant tokiai apgailėtinai finansų būklei, Lietuvos valdžios turėtų siekti maksimaliai efektyvaus energetinio balanso, ieškant ilgalaikių kontraktų, kurie leistų garantuoti prieinamas energijos išteklių kainas ir stabilų ekonomikos vystymąsi.

Lietuvos kurse „diversifikuojant“ energijos išteklių tiekimą, siekiant „nepriklausomybės nuo rytų kaimyno (Rusijos) politinių kainų diktato“, nesimato jokio ekonominio tikslingumo. Nuo tada, kai respublika pradėjo pirkti suskystintas amerikiečių dujas, ženkliai nukentėjo biudžetas, nes, lyginant su rusų vamzdžių analogu, valstybė permoka pusantro karto. Šiais metais, kaip ir 2017–aisiais, galutinė perkamų Amerikoje dujų kaina viršija 280 JAV dolerių už tūkstantį kūbų.

Ir paversti tą kainą viliotina neįmanoma dėl dujų rinkos ypatumų. Amerikiečių perdirbėjai patys perka dujas iš nepriklausomų gavėjų ir, panaudodami savo galingumus, suskystina jas, pagamina perdirbtą, iš esmės aukštos pridėtinės vertės produktą. Po to eksportuotojai, kurių vaidmenis atlieka neamerikiečių kompanijos, melsvą kurą pristato galutiniam užsakovui.

O „Gazpromas“, turintis savą žaliavos bazę, gamybos galingumus ir dujų transportavimo sistemą (RuBaltic.Ru pastaba), gali kainodaros klausime sau leisti lankstumą. Juk dujų savikaina Rusijoje šiandien viena iš mažiausių pasaulyje — 20 dolerių už tūkstantį kūbinių metrų. Jos eksporto kainos europietiškiems vartotojams šiemet kinta diapazone 180–190 JAV dolerių.

Žinoma, Lietuva gali pasirinkti dar vieną europietiškos rinkos dujų žaidėją (jo naudai) — norvegų kompaniją Statoil, tačiau ir ji nusileidžia rusų dujų gigantui. Pirmiausia pagal išteklius ir galingumus, įvesdama rikiuotėn visus savo galingumus.

Panaši situacija ir elektros energijos tiekimo sferoje. Respublika apribojo tiesioginį tiekimą iš Rusijos, daugiau elektros pirkdama iš Šiaurės Europos biržos Nord Pool.

Per pastaruosius aštonis šių metų mėnesius vidutinė biržos Nord Pood elektros kaina — 47 eurai už megavat — valandą, o tai trečdaliu viršija tą patį 2017 metų laikotarpį. Didmeninė elektros energijos kaina sudarė 3,4 cnt. už kw/val, o galutinis buities vartotojas už kw/val turėjo mokėti 11,3 cnt. Dėl kainų šiais metais biržoje augimo, 2019 metais neišvengiamai didės elektros kaina buities vartotojams. Ir tai jau patvirtino Lietuvos valdžios. Tad ar vertėjo atsisakyti tiesioginio elektros energijos tiekimo iš Rusijos?

Ką begalvotum, tačiau ekonominės situacijos Lietuvoje kitais metais pablogėjimą objektyviai iššaukė Lietuvos valdžios kursas energetikos sferoje. Papildomos biudžeto išlaidos dėl energijos išteklių vertės geopolitinės sudedamosios, valstybės skolų bei gynybos finansavimo augimas — visa tai pareikalaus iš Lietuvos valdžių paieškos papildomų finansinių šaltinių, o jais kitais metais gali tapti nauji mokesčiai, taikomi transportui ir nekilnojamam turtui.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 13 — id: `scraped:rubaltic_lt:1ea2bec8f0a51d58`

**Title:** Teisėsaugininkas: juvenalinė justicija — vaikų namų pasipelnijimo šaltinis

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lapkričio pabaigoje Lietuvos miestuose praėjo protesto akcijos, reikalaudamos pakeisti naują vaikų teisių gynimo įstatymą. Tėvai baiminasi, kad Lietuva nukopijuos blogiausią norvegų socialinės tarnybos Barnevarn patirtį – juk dabar, kad iš šeimos būtų paimtas vaikas, pakanka vieno anoniminio skambučio. Ar pavyks pasitelkiant mitingus padaryti pakeitimus juvenalinės justicijos įstatymų leidyboje, kaip kovoti su vaikų teisių gynimo Tarnybos veiksmais ir kodėl Lietuva pasirinko „antišeimyninę ideologiją“, analitiniam portalui RuBaltic.Ru papasakojo teisėsaugininkas, Socialistinio liaudies fronto pirmininkas Giedrius Grabauskas.

— Pone Grabauskai, kaip Jūs vertinate naują juvenalinių įstatymų leidybą?

— Aš ją vertinu neigiamai dėl dviejų priežasčių.

Pirma, ši įstatymų leidyba kišasi į vidinį šeimų gyvenimą. Mes smerkiame akivaizdų smurtą, tačiau egzistuoja vidinis šeimos gyvenimas. Tėvai auklėja vaikus kartais ir pakeldami balsą.

Pagal naujas pataisas, jei vaikų teisių gynimo Tarnybos darbuotojai sužinos iš gelbėtojų, kad vaikui nors kartą buvo suduota, jie pasiruošę kelti baudžiamąją bylą, o tėvą arba motiną įkalinti. Ir tokiu atveju iš šeimos reikia paimti ir perduoti vaikų namams visus vaikus. Patekęs į šiuos namus, vaikas nori sugrįžti į šeimą ir pabėga. Tokius vaikus paskui suranda, grąžina ir užrakina. O sąlygos ten panašios į kalėjimo.

Antra, čia įžvelgiamas vaikų namų ir vaikų priežiūros tarnybų suinteresuotumas, nes jie atrado „aukso kasyklą“. Esmė tame, jog prieš keletą metų kai kuriuose vaikų namuose buvo vaikų stygius, ir jiems buvo iškilusi uždarymo grėsmė. Vaikų teisių gynimo tarnybas, turinčias ryšių su vaikų namais, naujos pataisos nudžiugino. Dabar vaikų namai gauna daugiau vaikų, o tarnybos — didesnį finansavimą. Šis suinteresuotumas — korupcija, kurią remia kai kurie politikai. Šiais metais esant menkoms priežastims iš tėvų buvo paimta nemažai vaikų.

— Kas paskatino valdžias peržiūrėti juvenalinių įstatymų leidybą ir kodėl ginti vaiką turintis įstatymas pažeidžia tėvų teises?

— Prieš pusantrų metų Kauno rajone gyveno narkomanų šeima. Nuo narkotikų apsvaigę tėvai užmušė savo vaiką (2017 metų sausy Kėdainiuose motina ir patėvis mirtinai primušė ketverių metų berniuką: tragedija sukėlė visuomenės pasipiktinimą ir privertė valdžias peržiūrėti įstatymų leidybą. Pataisas taip ir pavadino: „Matuko reforma“ — RuBaltic.Ru pastaba).

Panašūs atvejai pasitaiko bet kurioje pasaulio šalyje. Tačiau politikai priėmė abejotinus įstatymus, pažeidžiančius daugelio šeimų teises. Tai kitas kraštutinumas. Ir atsiranda kreivų veidrodžių karalystė.

— Pokyčiai įstatymų leidyboje, skirti vaikų teisių gynimui, buvo priimti vasarą. Kodėl į gatves žmonės išėjo tik dabar?

— Pirmiausia, aptarimas vyko už uždarų durų, o pataisas priėmė vasarą. Vasarą žmonės išvyksta, mažiau žiūri televizorių ir klauso radijo. Birželis ir liepa — idealus laikas priimti nepopuliarius įstatymus.

Paskui žmonės pamatė, kas dedasi. Rugpjūty, rugsėjy ir spaly buvo daug atvejų, kai vaikai buvo paimami dėl menkniekių. Tarnybos naudojosi tuo, kad piliečiai nežino savo teisių. Pagal įstatymus žmonės turi teisę neatidaryti durų, jei jiems nepateiktas orderis.

Lapkričio viduryje į vieną kaimą atvyko policijos ir vaikų teisių gynimo Tarnybos darbuotojai. Apsilankė daugiavaikėje šeimoje. Šventės proga motina buvo truputį išgėrusi. Tarnautojai ėmė kabinėtis — ji esą girta. Situaciją išgelbėjo visuomenės veikėjas Nastas Jansaros, kuris atvyko ir fotografavo telefonu. Jis sugebėjo įmesti į Facebook tiesioginę transliaciją, kas numalšino policijos ir Tarnybos darbuotojų įniršį. Paskui parėjo visiškai blaivus vaikų tėvas, „svečiai“ surašė protokolą ir išsinešdino.

— Kyla klausimas dėl Tarnybos darbuotojų kompetencijos ir profesionalumo.

— O čia ir susiduria Tarnybos darbuotojų kompetencijos stoka ir įstatymų netobulumas. Tarnybon patenka labai skirtingi žmonės. Neseniai paaiškėjo, kad šioje organizacijoje visai neseniai dirbo Teodoras Ismailovas — keletą kartų teistas aferistas. Yra žinoma, jog jis žavisi neonacizmu, kartais vaikščioja su svastika ir ja puošia savo automobilį. Daugelyje atvejų, kai Tarnybos darbuotojai atvykdavo paimti vaikų, Ismailovas elgėsi grubiai, plėšė vaikus iš tėvų rankų.

— Kokie dar povandeniniai akmenys yra įstatyme?

— Pati vaikų paėmimo iš šeimos procedūra tapo greitesnė. Anksčiau egzistavo kai kokie saugikliai: tyrimą atlikdavo komisija, dirbo psichologai, taigi jautėsi, jog yra tvarka.

Dabar retorika pasikeitė. Tarnybos darbuotojai sako, kad jie turi veikti pagal greitojo reagavimo principą. Supainiotos kategorijos. Sunkiai suvokiamos tapo šių tarnybų funkcijos. Jos dabar budi ištisomis paromis. Joms pakėlė atlyginimus, garantuojamos geros premijos. Dabar dirbti tarnybose atsirado galimybė priimti nepatikimus žmones. Žodžiu, pasipelnyti galima biudžeto sąskaita, o biudžetas, kaip žinia, formuojamas iš gyventojų mokesčių.

— Triukšmą sukėlė įvykis Kaune, kai vaikai iš Eglės Kručinskienės buvo atimti jai išeinant iš parko. Vienas iš vaikštinėjusių pamatė, kaip motina pliaukštelėjo nepaklusniam vaikui, ir paskambino policijai. Ar daug lietuvių gali atsidurti Kručinskienės vietoje?

— Gali daugelis. Egzistuoja daug variantų. Dažnai šios Tarnybos darbuotojai ateina vakare, nors žmonės turi teisę neatidaryti jiems durų nepateikus orderio. Jei nori ateiti, lai skambina ir susitaria, kokiu laiku žmonėms patogu juos priimti.

Kručinskų vaikai buvo paimti tiesiog parke. Tokioje situacijoje gali atsidurti daug kas. Atsirado keistas liudytojas, sėdintis parke ant suolelio ir stebintis motiną su vaikais. Koks normalus 50 metų vyriškis tuo užsiims? Kručinskų advokatai bando patraukti vyriškį atsakomybėn, juk policijai jis pranešė, kad parke mušami vaikai, ko nebuvo. Mama pliaukštelėjo vaikui delnu per rūbelius, kai jis bandė bėgti nuo jos link judrios gatvės. Ekspertizė parodė, kad nebuvo rasta jokių sumušimo pėdsakų.

— Kaip Jūs manote, ar pavyks lietuviams protesto akcijomis pasiekti, kad įstatymų leidyba būtų pakeista?

— Ir taip, ir ne. Judėjimas turi tęsti savo politiką. Būtina pastoviai kreiptis į deputatus su peticijomis — pilietiškai spausti valdžią. Būtina kreiptis į tarptautines organizacijas.

— Europos juvenalinė įstatymų leidyba, ypač Skandinavijoje, dar griežtesnė. Ar Lietuvos valdžios ir toliau eis „antišeimyninės ideologijos“ įteisinimo keliu?

— Ir Seime, ir kituose valdžios organuose yra tokių griežtų įstatymų šalininkų. Jeigu visuomenė ir normalūs politikai nepajėgs susivienyti ir žengti bendrus žingsnius, gali būti, kad tokie įstatymai bus priimti. Skandinavijos šalyse jau veikia prieš šeimas nukreipti įstatymai.

Seimui pateiktas projektas įstatymo, kuris lei apriboti esamų pataisų galiojimą. Jį pateikė jaunas Valstiečių ir žaliųjų sąjungos seimūnas Mindaugas Puidokas. Tai dar ne įstatymas, tačiau jis lyg lakmuso popierėlis. Jeigu per mėnesį ar du jį pavyks prastumti ir priimti, tai bus ženklas, kad socialinių tarnybų prievartą jau įmanoma prislopinti.

Vaikai — nariai šeimos, kurioje yra sava tvarka. Valstybė turi įsikišti tada, kai nustatomas akivaizdus smurtas.

— Tarybų Sąjungos laikais, priešingai, egzistavo šeimų, motinystės ir vaikystės palaikymo politika. Ar efektyviai tada dirbo sistema?

— Tarybinė sistema, skirta šeimai ir jaunimo auklėjimui, buvo labai gera. Tada vaikai buvo paimami tik ypatingais atvejais. Darbas vyko ir mokykloje. Piktybiniai chuliganai po trijų perspėjimų buvo patalpinami internatuose. Lietuvoje toks internatas veikė Čiobiškėse. Perauklėti, jie buvo grąžinami į paprastas mokyklas.

Egzistavo daugiavaikių šeimų rėmimo sistema. 1980-aisiais daugiavaikėmis buvo laikomos šeimos, auginančios tris vaikus. Tarybinė sistema orientavosi į žmogiškumo principus. Mokyklose, vykdomuosiuose komitetuose dirbo komisijos. Vaikai su tėvais buvo kviečiami į mokyklą bet kurių klausimų aptarimui. Esant problemai, buvo suteikiama pagalba. Stengtasi apsieiti be griežtų represinių priemonių.

— Smurtas šeimose dažnai atsiranda dėl alkoholizmo, narkomanijos ar kitų visuomenės ligų. Kaip Lietuvoje reiškiasi šios bėdos?

— Alkoholizmas gana paplitęs. Po aštuntos valandos vakaro ir sekmadieniais alkoholis nepasrduodamas. Tokios priemonės atrodo juokingai, jos neduoda jokios naudos.

Tačiau alkoholizmas ne toks grėsmingas, kaip narkomanija. Rusijoje, Čekijoje ir kitose Europos šalyse šiai problemai spręsti skiriami valstybinio lygio projektai. Lietuvoje daug narkomanų landynių. Narkotikai pardavinėjami visur — klubuose, gatvėse, net greta mokyklų. Vyresnių klasių moksleiviai kaip taisyklė žino, kur galima įsigyti narkotikų.

Kova su narkomafija Lietuvoje labai žemo lygio. Čia taip pat yra rėmėjų. Per pastaruosius dešimt metų augo narkomanijos lygis. Narkotikai parduodami beveik legaliai, o kovojama kartais tik kosmetinėmis priemonėmis.

— Jūs sakėte, jog valdžios struktūrose yra rėmėjų. Ar įmanoma dekriminalizuoti lengvuosius narkotikus, kaip kai kuriose kitose ES šalyse?

— Taip, yra politikų, pasisakančių už šio reiškinio dekriminalizavimą. Jo šalininkai ne kartą organizavo atviras akcijas Vilniuje prie Seimo. Pradeda nuo mažiausio — siūlo legalizuoti 2–3 narkotinių medžiagų kategorijas. Suveikia „Overtono lango“ principas.

Kai kurie savo laiku iš Lietuvos išvykę žmonės dabar sugrįžta ir pasisako už legalizavimą. Aktyviai propaguojama, jog naudoti kai kuriuos narkotikus — normalu.

— Susumuokime rezultatus. Valstybė privalo ginti vaikus, tačiau kokiais metodais, Jūsų manymu, tai reikia daryti?

— Valstybė turi griežtai kištis ne tik tais atvejais, kai susiduriama su atviru smurtu šeimose. Tai šeimos, kuriose egzistuoja šeimyninis smurtas ir klesti narkomanija. Būtina skirti smurtą nuo auklėjimo, nes auklėjimas — vidinis šeimos reikalas.

Tai veda prie šeimų subyrėjimo. Ir tuo metu kai kurių vaikų namų vadovus naujoji sistema džiugina: įstaigos plečiasi, auga finansavimas.

Mindaugo Puidoko įstatymo projektas parodys, kaip viskas susiklostys — ar dar įmanoma sustabdyti destrukcinį procesą, ar juvenalinės justicijos grėsmė pakibo virš lietuvių šeimų. Daug kas priklauso nuo pačių piliečių vidinio situacijos suvokimo. Jie gali tiesiog neįsileisti į savo namus vakare socialinės tarnybos darbuotojų. Tačiau pavojus nedingsta. Savo požiūriu į juvenalinę justiciją Lietuva atsidūrė kryžkelėje.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 14 — id: `scraped:rubaltic_lt:8c0561cd33d67fc0`

**Title:** Lietuviai tarnauja Jos Didenybei. RuBaltic.Ru antirusiškos kampanijos Londone dalyvių dosje

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Informacinėje kampanijoje, kurią Didžioji Britanija galimai organizavo prieš RF prisidengdama projektu Integrity Initiative, galėjo dalyvauti įvairių Europos šalių atstovai. Jei tikėti paviešintais dokumentais, lietuvius kuratoriai apjungė viename „pabaltijietiškame klasteryje“. Apie šios grupės koordinatorių analitinis portalas RuBaltic.Ru papasakojo praeitoje medžiagoje . Kas dar, be kapitono Tomo Taugino, galėjo dalyvauti antirusiškoje Londono kampanijoje?

Pirmojo Strateginių komunikacijų departamento vadovo Sauliaus Guzevičiaus vardą mes jau minėjome praeitoje medžiagoje.

Kaip ir Tauginas, šis žmogus nėra viešas, tačiau kartą jis pasisakė Seime, o 2014 metų pavasarį išsakė eksperto nuomonę apie situaciją Ukrainoje.

Tiesa, naujos struktūros šefo išvados pasirodė, švelniai tariant, kitokiomis. Apie sėkmingas rusų kariuomenės transformacijas, jo manymu, buvo galima spręsti pagal įvykius Kryme, nes kampanija Čečėnijoje truko ne vienerius metus, Gruzijoje — keletą dienų, o Krymas buvo „okupuotas“ per kelias valandas.

Tur būt Guzevičiui niekas nepaaiškino, jog Kryme nevyko jokių karinių veiksmų...

Asta Skaisgirytė pastoviai žiniasklaidos minima kaip Lietuvos užsienio ministerijos politinis direktorius.

Kai Integtity Initative programa pradėjo veikti, Skaisgirytė užėmė Didžiojoje Britanijoje respublikos ambasadorės postą. Tiesa, būnant šiame poste, jai dažniau teko kovoti ne su „rusų imperializmu“, o su anglų ksenofobija.

Pavyzdžiui, 2013 metais leidinys The Independent išspausdino karikatūrą, kurioje pavaizduota pakuotė su sudėtais į ją nuogais žmonių kūnais. Užrašas teigė, kad ši „pakuotė — pigi darbo jėga“ iš Rytų Europos („du už trijų kainą“) ir kad „naudingas kiekvienas lietuvis“.

Išreikšti lietuvių tautos įsižeidimo kartėlį tada teko Aistei Skaisgirytei. Ji parašė laišką vyriausiajam redaktoriui, karikatūrą pavadino šlykščia, rasine ir ksenofobine.

Su fiziniais ksenofobijos pasireiškimais Skaisgirytė susidūrė po „Brexit“ balsavimo: liepos viduryje ponia ambasadorė pasakojo apie daugybę karalystėje gyvenančių lietuvių užpuolimo faktų, kurių priežastimi tapo nukentėjusiųjų tautybė.

Tačiau kaip ten bebūtų, pagrindine grėsme savo šaliai Skaisgirytė visada laikė Rusiją. Kai 2015 metais britų Leiboristų partijos vadovu tapo Džeremi Korbin — aktyvus NATO plėtros į Rytus kritikas, — Guardian išspausdino atvirą Lietuvos ambasadorės Londone jam laišką.

„Mes patys beldėmės į aljanso duris, reikalaudami, kad mus įsileistų, nes mes bijojome, kad vieną gražią dieną Rusija gali tapti tuo, kuo ji tapo šiandien: grėsme“, — pareiškė ji.

Į tą, kuris beldžiasi į duris reikalaudamas įsileisti, požiūris bus atitinkamas. Todėl, neabejotinai, nusiskundimą ksenofobija Asta Skaisgirytė galėjo pasilikti sau.

Diplomato karjera gali didžiuotis dar vienas „pabaltijietiško klasterio“ figūrantas Eitvydas Bajarūnas . Gerokai anksčiau prieš 2014 metus jis dirbo Lietuvos konsulu Sankt–Peterburge, po to — Lietuvos ambasadoriumi Švedijoje.

Dabar Lietuvos užsienio reikalų ministerijoje jis eina ambasadoriaus specialiems pavedimams pareigas. Bajarūnas atsakingas už tarptautinį pasipriešinimo išgarsintoms hibridinėms grėsmėms koordinavimą.

Nebūtina aiškinti, iš kurios šalies, Bajarūno manymu, sklinda šios grėsmės. O juk dirbdamas Peterburge jis garsėjo kaip nuostabiai taikingas diplomatas, siekiantis „bevizio režimo tarp Rusijos ir ES šalių, nes tarp mūsų seni turistiniai, šeimyniniai, humanitariniai ir darbiniai ryšiai“.

Dabar gi Bajarūnas jaučia „karo kvapą“ ir stengiasi, kad jį pajustų ir kiti.

Į sąrašą pateko ir buvusio Lietuvos ambasadoriaus Rusijoje Renato Norkaus vardas. Per 27 diplomatinės tarnybos metus jis spėjo padirbėti ir Lietuvos misijoje NATO, ir URM amerikiečių departamente, ir Lietuvos ambasadoje Vašingtone.

Naujas posūkis Norkaus karjeroje prasidėjo 2014 metais, kai jis buvo atšauktas iš ambasadoriaus Rusijoje pareigų. Pagal spaudos pranešimus, nuo tada jis ne kartą keitė darbovietę: vadovavo Lietuvos ambasadai Uzbekijoje, URM saugumo politikos skyriui, paskui tapo Lietuvos ambasadoriumi Didžiojoje Britanijoje.

Jokiais skandalingais rusofobo pasisakymais Norkus pastaraisiais metais nepasižymėjo. Diplomatas mano, jog „Rusija turi keisti savo elgesį ir retoriką“. Viskas padorumo rėmuose.

O štai Lietuvos Seimo Nacionalinio saugumo ir gynybos komiteto pirmininkas Vytautas Bakas (dar vienas sąrašo figūrantas) aktyviai kaunasi su „rusų agresija“. Ir suranda ją visiškai netikėtose vietose.

Pavyzdžiui, šį pavasarį „Kremliaus čiuptuvai“ jam pasivaideno Ignalinos AE. „Tragedija“ ne tame, kad aukštų technologijų kompleksus, neutralizuojant naudotą branduolinį kurą ir radioaktyvias atliekas, stato vokiečių Nukem Technologies, o tame, kad šios firmos akcijos priklauso rusų AB „Atomstrojeksport“.

Tad ar gali ramiai gyventi tai žinantis lietuviškasis patriotas? „Man sunku įsivaizduoti, kaip Nukem gali darbuotis Lietuvoje mūsų strateginiuose objektuose“, — pareiškė Bakas.

Neduoda parlamentarui ramybės ir statoma Baltarusijos AE, ji dirgina kito Lietuvos Seimo nario — Lauryno Kaščiūno — nervus. „Pabaltijiečių klasteryje“ jų vardai atsidūrė kaimynystėje.

Kaščiūnas pastoviai svaidosi rusofobiškais pareiškimais. Kai kurie iš jų prasilenkia ne tik su sveiku protu, bet ir su elementariu padorumu. Pavyzdžiui, šių metų kovą Lietuvos deputatas pasiūlė taikyti sankcijas Europos komisijai dėl jos pirmininko Žan Klod Junker „proputiniškos“ pozicijos.

Dar labiau „į lankas“ Kriščiūnas nukeliavo savo apmąstymuose apie užšifruotus politinius rusiškų multiplikacinių filmų tikslus. „Vienas ryškiausių pastarųjų metų fenomenas — visame pasaulyje populiarus animacinis serialas „Maša ir Lokys“, kuris stengiasi parodyti Lokį (suprask — Rusiją) geru, taikiu, saugojančiu mažą mergytę padaru“, — aiškino deputatas. Kaip rodo praktika, Didžiojoje Britanijoje atsirado žmonių, kurie šiuos paaiškinimus suprato kaip rimtus...

Kitas pagal sąrašą – tūlas „Dr. Povilas Malakauskas“. Tai tur būt tas pats Povilas Malakauskas , kuris yra vadovavęs Saugumo departamentui.

Jo atsistatydinimą žiniasklaida traktavo kaip dėl slaptojo CŽV kalėjimo Lietuvoje kilusio skandalo pasekmę. Tiesa, tai nutiko senokai, 2009 metais, t.y. gerokai prieš tai, kai buvo sukurtas projektas Integrity Initiative. Po to Malakauskas dirbo policijos generalinio komisaro patarėju, o dabar spauda jo beveik neprisimena. Sunku suprasti, kuo jis gali būti naudingas britams.

Kas toks Mantas Martišius , nesunku suvokti.Visai neseniai žmogus tokia pavarde tapo Lietuvos radijo ir televizijos valstybinės komisijos vadovu (faktiškai pagrindiniu šalies cenzoriumi).

Verta pripažinti, jog dėl Martišiaus rusofobijos niekada nekilo abejonių. Lietuvoje jis atlieka ne tik vieno iš pagrindinių kovotojų su propaganda, bet ir šalies rusakalbiams skleidžiančio neapykantą veikėjo vaidmenį. Filme „Karas 2020. Informacinė Rusijos agresija“ docentas Mantas Martišius perspėja tėvynainius, kad rusai gali būti pavojingi. Dabar jie lojalūs valstybei, o rytoj gali tapti „penktąja kolona“.

Mintys apie „rusų grėsmę“ privedė Martišių prie dar vienos „genialios“ išvados: nuo pražūtingos rusų propagandos įtakos lietuvius gali apginti... nemokėjimas rusų kalbos. Juk nesuprantantys rusų kalbos nepajėgs naudotis rusų žiniasklaidos informacija.

Linas Kojala 2016 metais tapo Rytų Europos tyrimų Lietuvos centro vadovu. Anksčiau jis dirbo šios įstaigos analitiku, o jos direktoriumi tapo po išėjusio iš šių pareigų mums jau pažįstamo Kaščiūno.

Beje, kaip ir jo buvusiam viršininkui, Kojalai didžiulį nerimą kelia filmas „Maša ir Lokys“. Ypač mergytės kepuraitės.

„Kai kuriuose epizoduose Maša dėvi kareivišką VRLK (NKVD) kepurę (kepurė priklauso Lokiui), o tai reiškia, jog serialas propagandinis, — įsitikinęs Kojala. — Matant tokią simboliką, stalininės represijos atrodo normaliomis, nekaltomis ir net priimtinomis mūsų laikais“.

Tačiau naujasis Centro vadovas žengė toliau savo pirmtako. Propagandą jis aptiko ir kitame animaciniame filme. „Kine geri vyrukai vaizduojami kaip tikrų rusų vertybių sergėtojai, ir tai tuo metu, kai Kijevo kunigaikštis pasireiškia kaip piktas menkysta“, — taip Kojala atsiliepia apie filmą „Trys galiūnai ir jūrų valdovas“.

Reikia nemažų pastangų, siekiant įžvelgti antiukrainietišką režisieriaus poziciją, tačiau lietuviškasis „kovotojas su propaganda“ savo tikslą sėkmingai pasiekė.

O štai tūlas Ainis Razma , atrodo, nepasižymėjo skandalingais pareiškimais. Jo vardas žiniasklaidoje šmėstelėjo 2014 metų vasarą. Tada Šaulių sąjungos narys Ainis Razma sakė, jog agresijos prieš Lietuvą atveju jo organizacija galėtų suformuoti savigynos būrius, perimant iš kariuomenės tam tikras funkcijas“. „Šauliai galėtų saugoti gyvenamuosius kvartalus, komunalinės reikšmės objektus, vaikų darželius, sandėlius ir t.t.“.

Beje, agresijos nebuvo sulaukta, todėl šauliai liko be darbo.

Dalis „pabaltijietiško klasterio“ figūrantų — nelietuviai, tašiau jie nėra svetimi Lietuvai. Kalbame apie tokius žmones, kaip Didžiosios Britanijos karo atašė Lietuvoje Džein Vit , Didžiosios Britanijos ambasadorius Lietuvoje Kler Lourens , Baltijos gynybos koledžo lektorius Džeims Rodžers . Andrejus Tiuška — tai, tur būt, Europos koledžo mokslinis bendradarbis (tik nesuprantama, kodėl jie atsidūrė „pabaltijiečių klasteryje“).

Viktorija Urbonavičiūtė atsidūrė sąrašo gale ir negali pasigirti, kad yra žinoma. Galime paminėti, kad moteris tokia pavarde dirbo Lietuvos ambasadoje Rusijoje (prieš keletą metų).

Tur būt apie šiuos žmones kalbama tuose dokumentuose, kuriuos paviešino chakeriai. O gal jie juos suklastojo?

Rusijos vyriausybei vertėtų iškelti šį klausimą britų kolegoms, nes daugelis ne tik „pabaltijietiško“, bet ir kitų klasterių figūrantų galėjo ne šiaip sau gauti pinigų už savo antirusiškus išpuolius — jie dar ir dirbo RF teritorijoje.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 15 — id: `scraped:rubaltic_lt:6151876b24b10b77`

**Title:** „Už pinigus maloniau nekęsti Rusijos“: lietuviškuosius rusofobus demaskavo chakeriai

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Europoje įsiplieskė skandalas dėl antirusiško sąmokslo. Anonymous chakeriai paviešino dokumentus, teigiančius, jog Londonas remia ir koordinuoja įvairių kontinento šalių rusofobus, tame tarpe iš Lietuvos. Prisidengdama projektu Integrity Initiative Didžiosios Britanijos vyriausybė galimai sukūrė didžiulę slaptą tarnybą, kurioje triūsia politinių, karinių, akademinių ir žurnalistų bendrijų atstovai. Jų tikslas — visam pasauliui pasakoti apie „rusų grėsmę“.

Chakeriai tvirtina, jog pagal minėtą projektą Didžioji Britanija ne kartą kišosi į nepriklausomų Europos šalių vidaus reikalus. Jų pateiktas ryškiausias pavyzdys — operacija „Monkloa“ Ispanijoje: Didžioji Britanija sumanė neleisti vidaus saugumo departamento direktoriumi skirti Pedro Banjosą. Ispanų klasteriui Integrity Initiative šios užduoties įgyvendinimui prireikė tik keturių valandų“.

Klasteriai, apie kuriuos eina kalba, — grupės žmonių, apjungtų tautybės principu. Paviešinti dokumentai liudija, jog britų agentūra veikia Vokietijoje, Prancūzijoje, Italijoje ir kitose šalyse. Tačiau mus labiausiai domina „pabaltijietiškas klasteris“, kuriame kruta ir Lietuvos atstovai. Negi kas galėjo pagalvoti, kad jų ten nebus?

Paslaptingas koordinatorius

„Pabaltijietiškame klasteryje“ aptinkame 16 pavardžių. Kadangi jokios papildomos informacijos, apart elektroninių adresų, sąrašuose nėra, identifikuoti kai kuriuos asmenis problematiška. Atviruose šaltiniuose informacijos apie juos nedaug.

Net Tomas Tauginas — žmogus, kuris laikomas „pabaltijietiško klasterio“ koordinatoriumi, — asmenybė visiškai neišryškinta.

Prieš dvejus metus Taugino pavardė skambėjo dviejuose vedančiuosiuose britų leidiniuose — The Times ir The Independent. Tuo metu „miglotame Albione“ jau buvo suformuota Jos Didenybės kariuomenės 77-oji brigada tikslu vesti informacinį karą ir kovoti prieš rusų propagandą.

Nuostabą žurnalistams sukėlė tai, jog šio nelengvo verslo plonybių britų kolegos mokėsi iš draugų pabaltijiečių. Į Jungtinę Karalystę atvyko specialaus Lietuvos kariuomenės dalinio atstovai, kurie pasakojo apie „Kremliaus informacinius karus“.

Atrodo, jog kartu su skyriaus vadovu Juriu Žgutsu jie smagiai „pasivažinėjo anglų ausimis“. Žgutsas, pavyzdžiui, skundėsi, kad jo šalis „perpildyta rusų kultūros“ ir jam kai kada atrodo, jog jis gyvena Rusijoje. Savo mintis papulkininkis pateikė kaip Maskvos agresyvius planus, kuriuose net tarybiniai paminklai — kovos elementas.

Neatsiliko ir jo pavaldinys. Pasak publikacijų spaudoje, Tomas Tauginas aiškino britų žurnalistams, kad Rusijos valdžios skirtingai dirba su įvairia auditorija. „Savo šalies gyventojams jos sako, kad NATO — stipri ir besiplečianti organizacija, ji su kiekviena diena vis labiau artėja prie Rusijos ir gali būti, jog vieną kartą užpuls“, — tai Taugino žodžiai The Independent.

O prieš vizitą į Didžiąją Britaniją Tauginas dalyvavo konferencijoje „ES tyrimų galimybių plėtra saugumo srityje dėka bendrų inovacijų, bendrų sukūrimų ir bendrų implementacijų“, kuri vyko Vilniaus Mykolo Riomerio universitete. Darbotvarkėje Tauginas minimas kaip strateginių komunikacijų skyriaus atstovas.

Beje, Tomo Taugino vardas aptinkamas kai kuriuose tyrimuose, kurie buvo atlikti bazuojantis minėtame universitete, o 2006 metais jis čia apgynė magistro vardą tema „Lietuva europietiškoje ir euroatlantinėje saugumo sistemoje: vystymasis, dabartis ir perspektyvos“ (marketingo ir administravimo poskyris).

Tauginas Mykolo Riomerio universitete laikomas ir veikalo „Automatizuota parinktų laisvos prieigos Internet išteklių turinio analizė kaip valstybinių nutarimų priėmimo instrumentas“.

Ši tema artima žmogaus, apie kurį kalbame, specializacijai. Surizikuosime išsakyti prielaidą, jog Tomas Tauginas iš universiteto ir Tomas Tauginas iš Strateginių komunikacijų departamento — tas pats žmogus. Tačiau mus labiau domina antroji institucija.

„Fotelių kariauna“

Kas gi tai yra – Lietuvos karo pajėgų Strateginių komunikacijų departamentas? Kažkas panašaus į specialią tarnybą. Atviruose informacijos šaltiniuose apie ją pasakyta labai mažai.

Pasidomėsime Lietuvos teisėsaugininko Giedriaus Grabausko nuomone.

Oficialiai publikuojami tik direktoriaus Jurio Žgutso (leitenanto-pulkininko) kontaktai.

Šis departamentas veikia nuo 2014 metų kovo–balandžio; būtent tada pasirodė pirmieji pranešimai apie veiklą šios struktūros, kuriai tuo metu vadovavo Saulius Guzevičius. Departamentas aktyviai propaguoja NATO bloką, jo darbuotojai rašo straipsnius, susitikinėja su moksleiviais ir įvairių organizacijų darbuotojais“.

Apie atskirų departamento atstovų veiklą galima spręsti iš jo uždavinių. Seržantas Tomas Čeponis, pavyzdžiui, nesivaržydamas pareiškia, kad jo komanda vykdo „monitoringą dezinformacijos“, didžioji dalis kurios primena tą propagandinę kampaniją, apie kurią buvo pranešę Ukrainos specialistai“.

Vieno iš jo „atradimų“ esmė tame, jog Rusija Pabaltijo regione siekia sukurti nedideles valstybes kaip Donecko ir Lugansko liaudies respublikos.

Paaiškėjo, jog V. Megre, V. Sinelnikovo, V. Serkino, S. Lazarevo ir kitų autorių knygos, kurias Lietuvos bibliotekoms norėjo padovanoti visuomenininkė Irina Judina, skleidžia „propagandą ir begėdišką melą“.

„Ir ką, kariškiai ėmėsi cenzūros? — stebėjosi Grabauskas. — Kas gi daro išvadas, kas tie paslaptingieji cenzoriai? Tai Lietuvos kariuomenės Strateginės komunikacijos departamentas ir jo atsakingi darbuotojai. Departamentas pasiuntė bibliotekoms laiškus su grąsinančiomis rekomendacijomis (pagal stilių — įsakymas), o kaip elgtis buvo nurodoma telefonu“.

Pasak Grabausko, skambino ir laiškus siuntinėjo vyresnioji departamento specialistė Auksė Ūsienė. Po metų ji dalyvavo persekiojant rašytoją Rūtą Vanagaitę, kuri išdrįso kritikuoti vieną iš „miško brolių“ lyderių Adolfą Ramanauską–Vanagą“.

„Visi žino, kad Rusija turi agentų ne tik tarp rusų, ji pastoviai ieško, kas galėtų kalbėti jos vardu, kas galėtų išvystyti griaunančią veiklą pasirinktoje valstybėje. Aš manau, jog čia kaip tik tas atvejis“, — pareiškė Ūsienė.

Ar tikėti chakeriais?

Pateiktų faktų visiškai pakanka, siekiant suformuoti įvaizdį departamento, kuriame dirba Tomas Tauginas, įtariamas esant „pabaltijiečių koordinatoriumi“. Geresnės bendradarbiavimo su britais Integrity Initiative rėmuose struktūros ir nesugalvosi.

Pats Tauginas po atmintinos išvykos į Britaniją užsiėmė aktyvia veikla. Pavyzdžiui, 2017 metų spalio mėnesį jis pasisakė Kijeve vykusiame forume „Ukrainos pulsas“, kur kartu su kitais garbingais svečiais aptarinėjo kibernetinio saugumo, propagandos ir melagingų naujienų problemas.

Po poros savaičių jis jau dalinosi žvalgybos paslaptimis atvirų šaltinių pagrindu (Open source intelligence, OSINT) konferencijoje Slovėnijoje. Šią vasarą Tauginas dalyvavo Venecijos klubo darbe (neformali žinomiausių ir labiausiai patyrusių specialistų grupė valstybinių Europos komunikacijų srityje), rudenį vyko į NATO strateginių komunikacijų konferenciją Romoje.

Kol kas sunku pasakyti.

Chakerių paviešintas medžiagas galima laikyti vertas vien tik apmąstymų. Kad jos originalios, abejoja net Rusijos politikai.

„Manau, jog labai svarbu ištirti įrodyminę bazę ir neskubėti su kaltinimais, nors ir norėtųsi juos pametėti“, — pareiškė Federacijos Tarybos Tarptautinių reikalų komiteto vadovas Konstantinas Kosačiovas.

Keli Anonymous sąrašų figūrantai jau paneigė savo dalyvavimą antirusiškame projekte. Analitinis portalas RuBaltic.Ru elektroniniu paštu paprašė Tomo Taugino komentarų, tačiau atsakymo kol kas nesulaukė.

Federaliniame tyrimų biure informacija nekomentuojama, britų URM sureagavo nelabai suprantamai: „Integrity Initiative yra programa, informacija apie kurią lengvai prieinama. Mes džiaugsimės, jei informacija apie šį projektą bus aukštesnio lygio“.

O štai kokį „aukšto rango URM valdininko“ atsakymą pateikia vyriausiasis „Echo Moskvy“ redaktorius Aleksejus Venediktovas: „Mes nekomentuojame pateiktų dokumentų statuso. Kas dėl Integrity Initiative, tai ji yra visiškai atvira programa. Mūsų finansavimas leidžia jai ir ateityje publikuoti svarbius darbus, siekiant demaskuoti dezinformaciją ir kitus neigiamus reiškinius. Mes džiaugiamės, kad šis projektas pasiekė viešumo aukštumas“.

Tokius atsirašinėjimus galima vertinti tik kaip sumišimą.

Ko džiaugiatės, ponai?

Kol kas šie klausimai pakibo ore.

Išsami „pabaltijiečių klasterio“ figūrantų analizė — sekančioje medžiagoje.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 16 — id: `scraped:rubaltic_lt:5bf71863a7356e1c`

**Title:** Paimti negalima palikti: kodėl Lietuvoje vaiko teisių gynimo reforma griauna šeimas

**Source:** rubaltic_lt (propaganda)

**Text:**

```
2017 metų vasary Lietuvos Seimas priėmė Civilinio kodekso straipsnių ir lydimųjų aktų, liečiančių vaiko teisių gynimą, pataisas. Dirbti šiuo klausimu buvo pradėta po tragedijos Kėdainiuose, kai praeitų metų sausy motina ir patėvis mirtinai primušė ketverių metukų vaiką. Pataisos taip ir pavadintos: „Matuko reforma“, pagerbiant vaiko, kurio mirtis privertė Lietuvos visuomenę atkreipti dėmesį į smurtą prieš vaikus šeimose, atminimą. Tačiau skubotai priimtas įstatymas slepia daugybę povandeninių akmenų, į kuriuos atsimušė daugelis šeimų.

Pataisos įsigaliojo nuo 2018 metų liepos 1 dienos. Pagal naujas taisykles Vaikų teisių gynimo tarnyba privalo nedelsiant patalpinti vaiką į saugią erdvę, jei įtariama, jog pažeidžiamos jo teisės. Per keletą mėnesių iš šeimų paimta pusantro tūkstančio vaikų. Dėl šių naujovių pastoviai iškyla skandalai, nes Vaiko teisų gynimo tarnybos darbuotojai kartais elgiasi nekorektiškai. Tėvams kyla klausimai — ar efektyvios šios priemonės, kokios kvalifikacijos vaiko teisių gynimo skyrių darbuotojai ir kaip apsaugoti savo šeimą nuo skubotai sukurtų organų įsikišimo. Analitinis portalas RuBaltic.Ru nutarė paanalizuoti pavyzdžius, kaip veikia naujos priemonės ir ko turi saugotis tėvai.

„Aš su viskuo sutinku, kad tik vaikai būtų ramioje aplinkoje“

Labiausiai nuskambėjo atvejis Kaune. Eglė Kručinskienė vaikščiojo parke su dviem vaikais: berniuku ir mergaite. Sūnelis ištrūko ir nubėgo. Eglė garsiai sušuko, norėdama jį sustabdyti, tačiau supratus, kad vaikas nepakluso, palikusi dukrą, pradėjo vytis.

„Aš prieš tai maldavau jį sustoti, nebėgti toliau... vaikas nepakluso. Tada aš jį tris kartus pliaukštelėjau per užpakaliuką, kurį dengė kombinezonas, jis nieko nepajuto ir neketino paklusti, nenorėjo sugrįžti pas paliktą miške sesutę. Jis bandė bėgti toliau, tada aš jį keketą kartų pliaukštelėjau per ranką“, — papasakojo žurnalistams Eglė.

Į šiuos motinos veiksmus dėmesį atkreipė greta vaikštinėjusi šeima — ji ir iškvietė policiją. Eglei išeinant iš parko ji jau buvo laukiama. „Kvalifikuoti“ darbuotojai, kaip paliudijo įvykį matę žmonės, elgėsi grubiai ir labai išgąsdino mergaitę su berniuku. Vaikai iš tėvų buvo paimti. Pirmiausia jie buvo nuvežti į vaikų namus, paskui perduoti laikiniems globėjams, bet ne giminėms, o pašaliniams žmonėms.

Po to, kai žiniasklaida sukėlė triukšmą, einanti Kauno vaiko teisių gynimo tarnybos vadovės pareigas Daiva Porutienė pareiškė spaudai, jog arešto metu Eglė buvo girta. Ši informacija buvo melaginga: ir teisėsaugos organai, ir medicininė ekspertizė patvirtino, kad motina buvo blaivi. Ponia Porutienė buvo nuimta nuo pareigų, tačiau iš tarnybos neatleista.

Vaikai pas globėjus gyveno virš mėnesio. Tuo metu atliktas tyrimas parodė, kad Kručinskų šeima darni, sutuoktiniai kartu gyvena 20 metų, iki šio atvejo jų atžvilgiu nebuvo jokių skundų, jų nėra policijos įskaitoje.

Keista, kad iš karto nebuvo priimtas toks sprendimas, juk akivaizdu, kad ir kalbos nebuvo apie tai, jog esą iškilo grėsmė vaikų sveikatai ir gyvybei. Gintaro atžvilgiu jokių skundų nebuvo, o smurto namie faktas nepasitvirtino.

„Aš su viskuo sutinku, kad tik vaikai būtų ramioje aplinkoje“, — komisijos nutarimą komentavo Eglė.

Kodėl su Egle buvo pasielgta taip griežtai ir kaip dirba įstatymas?

Naują įstatymą juvenalinės justicijos srityje ir Vaikų teisių gynimo tarnybos veiklos reformą galima laikyti reakcija į atvejį, kai nuo motinos ir sugyventinio sumušimų mirė ketverių metukų Matukas. Jau praėjus po šios tragedijos mėnesiui Seimas skubos tvarka priėmė Civilinio kodekso ir vaiko teisių lydimųjų aktų pataisas, o 2018 metų rugsėjy — naują vaiko teisių gynimo pagrindų įstatymo redakciją.

Reformą reikėjo pravesti seniai, tačiau politikai laukė „atvejo“. Pagal statistiką, nepriklausomos Lietuvos metais dėl tėvų arba globėjų kaltės žuvo 500 vaikų. Dar pridėsim paauglių savižudybių 2017 metais skaičių. Higienos duomenimis, tada nusižudė 25 paaugliai nuo 16 iki 19 metų.

Naujas įstatymas centralizavo sistemą: visi regioniniai vaiko teisių gynimo skyriai tapo pavaldūs valstybinei Vaiko teisių gynimo ir įvaikinimo sistemai ir turi dirbti pagal vieningus standartus. Šią tarnybą savo ruožtu kontroliuoja Socialinės apsaugos ir darbo ministerija.

Kiekviename teritoriniame skyriuje (o jų Lietuvoje 12) darbuojasi psichologai, vaiko teisių gynimo ir darbo su žmonėmis, kuriems nustatyta priklausomybė, specialistai. Šie skyriai dirba režime 24/7. Gavus pareiškimus apie galimus pažeidimus, į įvykio vietas išvyksta mobilios grupės.

Ir jau po to sprendžiama, ar gali vaikas sugrįžti į šeimą. Tuo atveju, kai vaiko sveikatai ir gyvybei nėra grėsmės, tačiau šeimoje iškilo kokie nors sunkumai, reikiamą šeimai pagalbą turi suteikti savivaldybė.

Lietuviškas atnaujintas įstatymas rankos mostu įvedė bet kokio smurto vaiko atžvilgiu draudimą, tame tarpe fizinę nuobaudą ir psichologinį spaudimą, netinkamą vaiko priežiūrą. Dabar vaikus iki šešerių metų galima palikti tik vyresnių, nei keturiolika metų, asmenų priežiūroje.

Siekiant užtikrinti kvalifikuotą pagalbą vaikams ir šeimoms, buvo padidinti reikalavimai Vaiko teisių gynimo tarnybos darbuotojams, jiems būtinas atitinkamas išsilavinimas, o kuratoriumi grupės, dirbančios su atitinkama šeima, gali būti paskirtas asmuo tik turintis universitetinį išsilavinimą ir ne mažesnę nei vienerių metų darbo su vaikais ir šeimomis patirtį.

Nejaugi Kručinskų vaikų sveikatai ir gyvybei buvo iškilusi grėsmė, kad buvo nutarta paimti juos iš šeimos?

Iš pirmo žvilgsnio ta sistema, kurią pasiūlė įstatymų rengėjai, atrodo solidžiai ir įtikinamai. Tai kodėl lietuvišką Tarnybą pradėta lyginti su blogiausiais darbo pavyzdžiais norvegų Barnevernet, kuri pasižymėjo griežta vaiko teisių priežiūros kontrole? Problema tame, jog net Norvegijoje pastoviai iškyla skandalai dėl Tarnybos korumpavimo, darbuotojų įpareigojimų viršijimo paimant iš šeimų vaikus, o taip pat nutarimų argumentacijos stokos.

Interneto erdvėje taip pat galima rasti istorijas, kai vaikai buvo paimami įtariant tėvus girtuoliavimu. Situacija dažniausiai atrodo taip. Šeima vyksta namo iš pobūvio gimtadienio proga, žinoma, tėvai nėra visiškai blaivūs. Pro šalį važiuoja policijos patrulių mašina, ir akylūs tvarkos sergėtojai, sustoję, reikalauja dokumentų ir „papūsti į vamzdelį“. Ką gi, tėvas girtas — apie 1,5 promilės, o mamos, po vyno taurės, girtumas — 0,2. Policininkai iškviečia mobilią grupę, ir ši paima vaiką arba vaikus.

Atsižvelgiant į tai, kokią vietą užima Lietuva pagal alkoholio suvartojimą vienam asmeniui, rizikos zonoje atsiduria labai daug šeimų. Bet ir pliaukštelėjimas per užpakaliuką iki šiol lieka veiksmingu.

Smurtas vaiko atžvilgiu — be abejonės, blogai. Tačiau tai nėra pagrindas paimti iš tėvų vaiką ir laikyti jį „kamaroje“, neišsiaiškinus visų aplinkybių.

Įstatyme pasakyta, kad nedelsiant paimti vaikus iš šeimos būtina, jeigu atvejui suteiktas antras pavojingumo lygis, tai yra egzistuoja pavojus vaiko sveikatai arba gyvybei. Ką gi baisaus įvykdė parke Eglė Kručinskienė, kad Tarnyba buvo priversta paimti jos vaikus? Esmė tame, kad įstatyme yra toks prierašas: vaiką galima paimti, kai vietoje neįmanoma tinkamai įvertinti situacijos ir vienareikšmiai suteikti jai kokį nors pavojingumo lygį.

Išvada: pateiktuose atvejuose specialistai pervertino pavojų. Ir todėl nukentėjo vaikai. Ar šiuose atvejuose buvo apgintos jų teisės?

Kokias dar įstatymo „skyles“ pavyko aptikti?

Dar vienas skubotumo rezultatas, kuris atsirado ruošiant įstatymą, — melagingi pranešimai apie problemas šeimose. Pagal statistiką, nuo liepos 1 dienos gauta 6 tūkstančiai pareiškimų, 60 proc. kurių nepasitvirtino koks nors pavojus vaikui.

Šeimos psichologės Rūtos Kišlytės nuomone, Lietuva šiandien nepasiruošusi įgyvendinti naujo įstatymo numatytų priemonių. Jos manymu, įstatymas liečia daug kol kas Lietuvoje neišspręstų problemų.

„Kai įstatymas dar tik buvo ruošiamas ir buvo reformuota sistema, atrodė, kad teoriškai viskas daroma teisingai, buvo sudarinėjamas paslaugų, reikalingų vaikui ir šeimai, sąrašas. Tačiau teko suvokti, kad mes nieko nežinome apie vaiką ir šeimą.

Vardan tiesos verta pasakyti, kad popieriuje valstybės teikiamos paslaugos egzistuoja, ir jų sąrašas įspūdingas. Šeimai gali būti suteikta galimybė nemokamai lankyti pozityvius tėvystės ir šeimos įpročių vystymosi kursus. Jos gali sulaukti psichologinės pagalbos, mediacijos ir vaikų priežiūros paslaugų ir net transferio. Iš biudžeto kompleksinei pagalbai šeimoms nuo 2016 iki 2020 metų skirta 21,16 milijono eurų. Tačiau praktiškai šis projektas realizuojamas prastai, ypač mažuose miesteliuose ir ištuštėjusiuose Lietuvos rajonuose, kur ne apie „mediacijos paslaugas“, o kaip išlaikyti šeimą galvojama.

Ir baigiant

Ir vėl susiduriame su situacija, kai valdžios, priimdamos įstatymus, kovoja su pasekmėmis, nors būtina elgtis taip, kad nepasikartotų Matuko tragedijos. Paimti iš šeimų tūkstantį vaikų ir tuo išgelbėti vieną gyvybę, žinoma, taip pat išeitis, bet kokia kaina? Ar ne geriau būtų sukurti veiklią sistemą, užsiimančią smurto prieš vaikus prevencija? Nustatytais atvejais suteikti šeimoms kompleksinę pagalbą: psichologinę, socialinę, teisinę. Ir vaikas, ir tėvai turi pasitikėti Tarnyba, o ne bijoti, jog kažkieno neteisingai pateiktas vaizdas sugriaus šeimą.

Ta reforma, kurią įgyvendino Lietuvos valdžia, labiau primena norą užsidirbti politinius taškus prieš rinkimus. Politikai pademonstavo rinkėjams, kaip greitai jie reaguoja į rezonansinius atsitikimus ir garsius skandalus. Beskubėdami deputatai priėmė įstatymo redakciją, kurioje nupiešė laimingą ateitį. Tačiau kokiais metodais siekiama to tikslo?

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 17 — id: `scraped:rubaltic_lt:bf2954775730f375`

**Title:** Lietuvos mokyklose uždraustas kenksmingas maistas. Kur dabar maitinami vaikai ir kas dėl to džiūgauja?

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvoje nuo rugsėjo 1 dienos įvesti nauji reikalavimai mokyklų, vaikų darželių, vaikų stovyklų ir socialinės paramos įstaigų valgykloms. Sveikatos apsaugos ministerija paskelbė karą angliavandeniams, maisto papildams ir kenksmingoms kalorijoms. Kaip tvirtina valdininkai, naujovės buvo ruošiamos išimtinai tikslu pagerinti bendrą lietuvių tautos sveikatą. Analitinis portalas RuBaltic.Ru nutarė išsiaiškinti, kam atiteks naujų patiekalų grietinėlė.

VISKAS PRASIDĖJO NUO DAINŲ

Nekeliantis apetito maistas mokyklos ar ligoninės valgykloje — liūdna Lietuvos realybė. Seniai žinoma, kad valgykla — ne restoranas, todėl pavalgydins ten pigiai, tačiau nenudžiugins nei estetika, nei patiekalų skonio kokybėmis. Lietuvos ekspertai ir žurnalistai teigia, kad toks požiūris į maistą – tarybinis palikimas. Jų nuomone, būtent tarybiniais laikais skaičiuotina tik kalorijos, riebalai ir baltymai, nekreipiant dėmesio į maisto naudingumo komponentus ir išvaizdą.

Beveik trisdešimt metų gyventa Lietuvoje su šia „sovietine atgyvena“, niekas nieko nedarė gerinant mokyklų valgyklų patiekalus. Pirmą kartą apie maitinimo organizavimo trūkumus bendro lavinimo įstaigose rimtai prabilta moksleivių Dainų šventės 2016 ir 2017 metais metu. Esmė tame, kad festivalio dalyviai ėmė viešinti nuotraukas maisto, kurį gaudavo maitinimo punktuose, socialiniuose tinkluose.

Pietų išvaizda ir kokybė negalėjo nesukelti pasipiktinimo. Konkursantai skundėsi, kad maisto mažai, jis neskanus, dažnai atšalęs. Pasitaikė ir vaikų apsinuodijimo atvejų (ne masiškų). Rimtų pažeidimų ruošiant ir laikant maistą Lietuvos Respublikos Valstybinė maisto tarnyba ir Veterinarija nenustatė.

Tačiau spaudoje periodiškai buvo išsakoma tėvų ir vaikų nuomonė ir ėmė atsirasti anoniminiai laiškai pačių maistą gaminančių ir maitinimą organizuojančių kompanijų darbuotojų, teigiantys, jog valgis vaikams ruošiamas antisanitarijos sąlygomis, pažeidžiant maisto šaldymo ir laikymo technologijas.

NEJAUNI FUD–BLOGERIAI

Pasipiktinimo banga palaipsniui perėjo į interneto akciją, kuri pasiekė ir ligoninių pacientus.

2016 metais tinklalapyje Facebook žmonės pradėjo talpinti „ligoninių“ pietų nuotraukas. Viena iš labiausiai aptariamų tapo nuotrauka mamos dvimetės mergytės, kuriai Alytaus S.Kudirkos ligoninėje pusryčiams atnešė košelę su daktariška dešra.

Piliečių diskusijos internete ir žiniasklaidoje supykdė Sveikatos apsaugos ministerijos maitinimo ir fizinio aktyvumo skyriaus viršininką Almantą Kranauską. Jo manymu, lietuviai moka per mažai mokesčių, todėl ligoninės negali skirti daugiau lėšų pacientų mitybai. Žodžiu, ligoninė — ne kurortas, todėl nėra ko stebėtis, gavus virtos dešros. Verta pažymėti, kad 2018 metais mėnesinis privalomasis medicininis draudimas sudarė 36 eurus.

O reaguoti į piliečių pasipiktinimus vis dėlto teko. Sveikatinimo įstaigose buvo pravesti patikrinimai, o pagal jų rezultatus pateiktos rekomendacijos. Tačiau pozicija iš esmės nepasikeitė; maistas ligoninėse turi būti paprastas ir naudingas; nesvarbu, kokia yra pateikiamo maisto skonio kokybė.

Paskui buvo nutarta „įvesti tvarką“ mokyklose ir vaikų darželiuose. Sveikatos apsaugos ministerijai jautriai vadovaujant, buvo ruošiami nauji maitinimo standartai, apribojant cukraus ir druskos naudojimą ir uždraudžiant kai kuriuos produktus. Valdininkai pareikalavo, ruošiant patiekalus švietimo ir sveikatinimo įstaigoms, naudoti tik aukštos kokybės produktus, rekomendavo kaip komponentus plačiau naudoti daržoves ir vaisius.

Tiesa, mokyklų ir ligoninių finansavimas nepasikeitė. Tačiau, kaip RuBaltic.Ru papasakojo mokiniai, patiekalų kainos mokyklų valgyklose ūgtelėjo, o skonio kokybė, priešingai, krito.

IŠ PIRMŲJŲ LŪPŲ

Evelina, J.Kraševskio gimnazijos 10 klasės mokinė.

„Valgiaraštis mokyklos valgykloje mažai pasikeitė, o porcijos ženkliai sumažėjo ir dar pabrango. Kas anksčiau kainavo 1,70 euro, dabar kainuoja 2 eurus. Kas dėl skonio, maistas pablogėjo. Dabar valgykloje nėra Kijevo kotletų, o karbonatas ruošiamas be džiūvėsių. Iš esmės valgis tapo neskoningas, ir mokykloje valgančių mokinių skaičius sumažėjo. O atsinešti į mokyklą savo valgį nerekomenduojama. Kaip suprantu, tokios naujienos mokytojų nedžiugina, nes jiems tai dar viena problema — kai kuriose mokyklose mokytojai verčiami tikrinti mokinių portfelius, aiškinantis, ar jie neatsinešė ko nors draudžiamo. Pas mus kol kas taip nedaroma“.

Liza, „Žaros“ gimnazijos 8 klasės mokinė.

„Valgykloje viskas tapo neskanu. Neskoningas valgis, jame beveik nėra druskos. O dar ir kainos aukštos, pats pigiausias antrasis patiekalas kainuoja 1,50 euro — tai grietinėje troškinta vištiena, o, pavyzdžiui, žuvis kainuoja 2,20 euro, ir visa tai be sriubos, arbatos arba vandens. Ypač sunku mūsų berniukams, jie juk pastoviai nori valgyti, o dabar mokykloje jiems beveik nėra skanaus valgio“.

Egzistuoja nuomonė, jog vaikams nepatinka teisingai maitintis mokykloje, nes namuose jie maitinami neteisingai (suprask „skaniai“). Dietologai įsitikinę, kad tėvai leidžia vaikams valgyti čipsus, miltų gaminius, saldumynus, todėl, atėję į mokyklą, jie nenori beskonės košės ir garų kotletų.

Pateiksime Vilniaus moksleivių tėvų asociacijos narių komentarus tinklalapyje.

— Na ką aš galiu pasakyti, mūsų dietų išminčiai, tautą Seime atstovaujantys, mano, kad maitinti vaikus reikia būtent taip. Turbūt jiems atrodo, kad paskui vaikai neturės svorio ir persivalgymo problemų. Gaila, jie pamiršo paklausti tikrų dietologų ir vaikiško maisto specialistų dėl cukraus, druskos ir gyvulinių reikalų draudimo vaikams. O dar dėl neriebaus pienelio, žalių daržovių ir pribrendusių grūdų "naudos" vaikiškiems skrandžiams.

— o ministerijoje sėdi vis tokios grakščios ponios, lai jos pradės nuo savęs, o mes jau kaip nors nuspręsim, kuo maitinti mūsų vaikus - mes nekvailesni!

KAM ATITEKS GRIETINĖLĖ

Be viso kito, kyla klausimas: kam naudingas naujas valgyklų valgiaraštis? Ar tik tautos gerovė rūpėjo novatoriams, ar už naujovių slypi dar kažin kas? Ir čia yra keletas figūrantų, ties kuriais apsistosime išsamiau.

Raminta Bogušienė — maisto technologė ir maitinimo specialistė, narė komisijos, ruošiančios naujus valgiaraščius ir rekomendacijas valgykloms. Ponia Bogušienė, talkinant rėmėjams kompanijos Pontem, kuri teikia visuomeninio maitinimo paslaugas, išleido knygą „Palankių sveikatai technologinių kortelių ir valgiaraščių rinkinys“.

„Knyga atitinka Sveikatos apsaugos ministerijos reikalavimus ir vaikų mitybos organizavimą“, — taip reklamavo „kūrinį apie neskanų ir sveiką maistą“ vice ministrė Aušra Bilotienė.

Raminta Bogušienė, be kita ko, yra kompanijos „Sveikatai palankus“ direktorė ir steigėja. Savo įmonės tinklalapyje, afišuodama knygą, ji parašė: „Šis leidinys gali padėti bendrojo lavinimo įstaigoms pereiti prie naujų, sveikatai palankių ir atitinkančių naujas vaikų mitybos taisykles valgiaraščių...“

Tokiu būdu, mokyklos buvo suklaidintos ir priėmė Bogušienės knygą kaip privalomą priemonę. Pagal kai kuriuos vertinimus, apie 300 švietimo įstaigų įsigijo šią kulinarijos vertybę už ... 100 eurų. Ir tai tuo metu, kai Pontem apmokėjo knygos spausdinimą ir išleidimą, neišperkant autorinių teisių.

Dar daugiau, paaiškėjo, kad knygos viršelyje neturėjo būti Sveikatos apsaugos ministerijos emblemos, tai, autorės žodžiais, nemaloni klaida, ir ji nežino, kaip tai galėjo atsitikti.

Tačiau knyga — tai tik pirmoji grandis: toliau seka mokyklų, vaikų darželių ir ligoninių maitinimo organizatoriai. Šiandien Lietuvoje egzistuoja kelios stambios firmos, kurias galima pavadinti šios srities monopolininkėmis.

Žinoma, valstybėje egzistuoja švietimo ir sveikatinimo įstaigos su savomis valgyklomis. Verta pažymėti, kad kai kurių mokyklų virtuvėms reikia kapitalinio remonto, apie ką liudija specialių komisijų ataskaitos. Kaip taisyklė, nei mokyklos, nei valstybė neturi lėšų šių virtuvių remontui.

Patogiau ir pigiau bus pirkti pietus iš stambių firmų, kurios pagal savo gamybos apimtis pasiruošusios aprūpinti mokyklas ir vaikų darželius pigesniu maistu.

O KAS TOS FIRMOS?

Visuomeninių pirkimų tarnybos duomenimis, nuo 2013 iki 2015 metų 56 proc. konkursų visuomeninių pirkimų maisto produktų ir visuomeninio maitinimo paslaugų sferoje laimėjo ir stambiausius kontraktus pasirašė tik trys firmos: Pontem, Kretingos maistas (po kaltinimų sukčiavimu ir turto pasisavinimu, organizuojant 2014–2016 metais mitybą mokyklose ir ligoninėse, pervardintas į Bruneros — RuBaltic.Ru past.), Sanitex. 44 proc. likusių pirkimų tenka 252 kitoms firmoms. Be to, Kretingos maistas 2015 metais, leidus Konkurencijos tarnybai, nupirko Sanitex.

Nuo 2015 metų situacija šioje rinkoje praktiškai nepasikeitė. Pontem ir Bruneros sistemingai atsiduria skandalų centre: dempinguoja, pažeidžia kontraktų sąlygas. Bijoti rinkoje joms nėra ko, nes užimtos pozicijos nepalieka konkurentams jokių šansų.

Kenčia ir mažasis verslas: tie, kurie galėtų pirkti produkciją vietoje iš fermerių ir dirbti su viena arba keliomis periferijos mokyklomis, neatsilaiko prieš monopolininkus.

Maitinimo reforma mokyklose ir vaikų darželiuose vargu ar duos apčiuopiamų teigiamų rezultatų visuomeninio maitinimo organizavime. Beje, valstybėje, kurioje praktiškai pribaigtas mažasis verslas ir klęsti tokie gigantai, kaip Maxima, Rimi, Lesto, nėra nieko naujo.

— Mes lankome darželį. Nuo trečiadienio vaikui skauda skrandį. Anksčiau problemų nebuvo. Dabar lakstome pas gydytojus. Poliklinikoje aš supratau, kad vaikai labai skundžiasi naujuoju valgiaraščiu. Net mūsų gydytoja pirmiausia paklausė: "Ar jūs darželyje perėjote prie naujos mitybos?"

— ir iškart nukreipė pas gastroenterologą.

— štai tau ir sveikatingumas... Įdomu, ką pasakys specialistas, su jais, atrodo, nesitarta ....

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 18 — id: `scraped:rubaltic_lt:7500343cfe26d56c`

**Title:** Jums spręsti — ar pradėsite naują priešpriešos su Rusija etapą“ — atviras kreipimasis į Lietuvos teisėjus (2 dalis)

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvoje startuoja, pagal viską, paskutinis „Sausio 13-osios bylos“ teisminio proceso etapas, kuris respublikoje vadinamas „Niurnbergu Rusijai“. Lietuvos politinis elitas neslepia, jog pagrindinis šio proceso tikslas — ne nustatyti teisybę, o mesti prieš Rusiją išpuolį, ir kaltinami teismo salėje bus ne tiek sausio 13-osios įvykių dalyviai, kiek Rusija kaip šalis, nelojali vakarietiškoms „vertybėms“. Prieš paskutinį šio užsitęsusio proceso etapą į Lietuvos teisėjus atvirai kreipėsi Vladislavas Švedas : Lietuvoje vienas iš „teisiamųjų“, o iš tiesų — neišdavęs savo įsitikinimų buvęs Lietuvos Kompartijos CK antrasis sekretorius (nuo 1990 metų), dramatinių įvykių 1991 metų sausy Vilniuje liudininkas ir dabartinės Lietuvos Respublikos tyrinėtojas. Analitinis portalas RuBaltic.Ru pateikia antrąją šio kreipimosi dalį.

Rusija taip pat gali pateikti Lietuvai sąskaitą dėl 1944 metais žuvusių 160 tūkstančių tarybinių karių, vadavusių jos teritoriją iš nacių okupacijos. Pagaliau, Rusija turi teisę pareikalauti iš Lietuvos atlyginti išlaidas sąjunginio biudžeto, kuris tarybiniais laikais visada buvo pagrindinai formuojamas Rusijos sąskaita — visa tai 1944–1991 metais buvo investuota į Lietuvos industrializaciją ir socialinę sferą. RF ekonominio vystymosi ministerija tvirtina, jog ši suma sudaro 72 milijardus dolerių. Tačiau jeigu perskaičiuoti pagal dabartinį aukso kursą, tai gausime apie trilijoną dolerių (RF ekonominio vystymosi ministerijos pažyma šia proga buvo išspausdinta 2010 02 18 laikraštyje „Sovetskaja Rosija“).

Pagal buvusio TSRS Ministrų Tarybos pirmininko Nikolajaus Ryžkovo informaciją, vien tik 1988 m. į Lietuvą buvo įvežta 16,7 mln tonų akmens anglies, virš 13 mln tonų naftos, perpumpuota 4,9 milijardų kūbinių metrų dujų. Be to, respublika gavo 780 tūkst. tonų valcuoto metalo, 824 tūkst. tonų padarinės medienos, 496 tūkst. tonų mineralinių trąšų, 2,7 milijono tonų maistinių grūdų. Ir toks tiekimas praktiškai egzistavo Lietuvai visais tarybų valdžios metais.

Norint vaizdžiai suprasti, kaip Lietuva buvo finansuojama tarybiniu laikotarpiu, priminsiu, kaip buvo statomas Vilniaus televizijos bokštas. 1970 metų pradžioje TSRS Ministrų Taryba davė sutikimą statyti šalyje tris bokštus. Vieną buvo numatyta statyti Lietuvos TSR sostinėje Vilniuje, kitą Taline, trečią Sverdlovske — viename iš galingiausių TSRS industrijos centrų.

1974 m. buvo pakloti betoniniai Vilniaus televizijos bokšto pamatai. Projektavo jį Valstybinis sąjunginis TSRS ryšių ministerijos projektavimo institutas. Statė betoninę bokšto dalį pagal tuo metu unikalią monolitinę betoninę technologiją statybos montažo trestas „Specželezobetonstroj“ (Maskva).

Finansavo statybas, kaip buvo pasakyta aukščiau, sąjunginis biudžetas. 1981 m. sausy televizijos bokštas buvo įvestas eksploatacijon. Šiek tiek anksčiau, 1980 m. liepą, pradėjo veikti tokio pat tipo Talino televizijos bokštas. Jį buvo pradėta statyti vėliau, negu Vilniaus, tačiau darbus pagreitinti teko dėl 1980 m. XXII Olimpinių Maskvos žaidynių burlaivių regatos Taline. Šio bokšto statybą taip pat finansavo sąjunginis biudžetas.

Sverdlovske (dabar Jekaterinburgas — RuBaltic.Ru past.) televizijos bokšto, tokio pat, kaip Vilniuje, statyba buvo pradėta tik 1983 m. Jam nepakako biudžetinių lėšų ir specializuotų galingumų. Minėtas trestas „Specželezobetonstroj“ iki tol buvo užimtas darbais Vilniuje ir Taline. 1990 m. lėšos, skirtos Sverdlovsko televizijos bokšto statybai, užsibaigė, ir jis prastovėjo neužbaigtas iki 2018 m. kovo, kai buvo nugriautas sprogdinant.

Užbaigiant galimų Rusijos atsakomųjų pretenzijų Lietuvai temą, būtina pasisakyti apie tai, jog Rusija, atsakydama į pripažinimą, kad rusai nusikalto prieš žmogiškumą ir įvykdė karo nusikaltimus, pareikalaus iš Lietuvos valdžių atsakymo, kodėl Lietuvoje nė vienas karo nusikaltėlis, įvykdęs nusikaltimus Lietuvos teritorijoje 1941–1942 ir 1944–1953 metais, nepatrauktas baudžiamojon atsakomybėn. Net daugiau: dauguma jų įvardinti didvyriais.

Tarybų Lietuvoje lietuvių dalyvavimas 1941 metais masinėse žydų žudynėse buvo nutylimas. Pamenu, kaip 1957 metais Utenoje pirmą kartą buvo minimas 4 tūkstančių žydų sušaudymas Rešės miške. Į gedulingą mitingą buvo pakviesti visų Utenos mokyklų pionieriai. Rusų mokyklai atstovavau aš. Mitinge kalbėjęs vykdomojo komiteto pirmininkas sakė, kad dėl žydų žudynių kalti vokiškieji fašistai. Ši versija tada buvo visuotinai priimtina.

Būtent jie šaudė žydus Rešės miške. Vyresni kaimynų vaikinai, pamenantys nacių okupaciją, pasakojo, kaip nacionalistai kolonomis varė žydus sušaudymui tame miške. Net parodė namus, kuriuose anksčiau gyveno „žydšaudžiai“. Vardino tuos, kurie aktyviausiai dalyvavo apiplėšiant žudomus žydus ir dėka prisiplėšto jų turto pasistatė arba išpuoselėjo savo namus.

Šia tema 2016 m. išleista lietuvių rašytojos Rūtos Vanagaitės knyga „Mūsiškiai“ pašiaušė Lietuvos visuomenę, nors ji buvo parašyta remiantis dokumentine medžiaga. Prieš porą metų iki šios knygos pasirodymo Vanagaitė kartu su Jeruzalės Simono Vizentalio centro vadovu, užsiimančiu nacių karo nusikaltėlių paieškomis, pavažinėjo po Lietuvą, apklausdama Holokausto liudytojus.

Panaudodama surinktą medžiagą, Vanagaitė parašė aukščiau minėtą knygą. Tačiau vėliau, pasinaudodama Lietuvos TSR VRLK (NKVD) archyvų duomenimis, bendradarbiavimu su tarybiniais organais apkaltino paskutinį „miško brolių“ vadą Adolfą Ramanauską Vanagą. Jis dabartinėje Lietuvoje paskelbtas didvyriu, ir po mirties jam suteiktas brigados generolo laipsnis. Visa tai sukėlė naują skandalą ir rašytojos persekiojimą. Tada Vanagaitei teko laikinai išvykti iš Lietuvos. Visos jos parašytos knygos, net grynai moteriška tema, nekalbant apie „Mūsiškius“, buvo išimtos, jas net buvo norėta utilizuoti.

Tuo tarpu ne paslaptis, jog 1944 m. tarp norinčiųjų kovoti prieš „sovietinius okupantus“ daugiausia buvo tų žmonių, kurie susitepė ne tarnavimu naciams, o masišku tarybinio ir partinio aktyvo bei žydų žudymu. Šiems „žydšaudžiams“ nebuvo kelio nei į Vakarus, nei pas amerikiečius, jiems nebuvo pakeliui ir su tarybų valdžia. Todėl jie bendradarbiavo su naciais, praėjo apmokymus buvusiose Abvero mokyklose, kurias 1944 metais kuravo SD (Sicherheidiensts — SS saugumo tarnyba), ir buvo parašiutais išmesti į Tarybų Lietuvos teritoriją.

Kai kuriais duomenimis, trečdalis taip vadinamųjų „partizanų“ vadų dalyvavo žudant žydus („Litovskij kurjer, 2010 12 02, „Kita vidurnakčio pusė“). Jau 1944 m. rugpjūty Lietuvoje buvo parašiutais išmesti 25 nacių paruošti agentai. Jie turėjo sukurti partizanų būrių tinklą.

Apie šių grupių sudėtį byloja toks pavyzdys. 1944 m. lapkričio 18 d. Panevėžio apskrityje nusileido 12 parašiutininkų diversantų grupė, vadovaujama Antano Šilo. Kaip VRLK pasakojo areštuotas šios grupės narys Antanas Birbilas, ji buvo suformuota iš LAF (Lietuvos aktyvistų frontas — Berlyne 1940 m. sukurta pronacistinė organizacija) narių, daugiausia iš buvusių policininkų, nacių talkininkų ir vokiečių kariuomenės karininkų“.

Lietuvos valstiečiui tuo metu buvo ypač sunku išgyventi. Dienomis ateidavo tarybiniai liaudies gynėjai (ginkluoti savanoriai, talkinę Lietuvos TSR VSM), o naktį — „miško broliai“. Ir vieni, ir kiti norėjo valgyti.

Net tokiame mieste, kaip Utena, kur stovėjo tarybinis karinis dalinys, „miškiniai“ neretai ateidavo „į svečius“ pas kai kuriuos gyventojus. Kai kas juos pasitikdavo automato serija, o neturintiems automato tekdavo „svečiams“ atidaryti duris. Ir tų, kurie „priimdavo“, laukė arba „miškinių“ kulkos, arba kelionė į Sibirą. Pasitaikydavo ir viena, ir kita.

1944–1956 metais nuo taip vadinamų lietuviškųjų „partizanų“ rankų Lietuvoje žuvo 25108 žmonės, 2965 buvo sužeisti. Tarp nužudytų 993 vaikai iki 10 ir 52 — iki 2 metų. 118 vaikų buvo sužeista (TSKP CK „Izvestija“ Nr. 10, 1990 m., pusl. 139).

Pacituosiu Boriso Bergo straipsnį „Kita vidurnakčio pusė“ , kuris buvo išspausdintas laikraštyje „Litovskij kurjer“ (2010 12 02). „Žmonės, kurie šiandien daromi nacionalinio pasipriešinimo tarybiniam okupaciniam režimui didvyriais, apdovanojami valstybiniais apdovanojimais ir pelno įvairius garbinimus, iš tiesų buvo toli gražu ne Dievo avinėliai. Vargu ar jie pateko į rojų, nes paliko pokario Lietuvoje labai daug nekaltai nužudytų sielų...“

Sugrįžkime prie jau minėto Adolfo Ramanausko. Lietuvoje tvirtinama, kad jo dalyvavimas žydų žudyme neįrodytas. Tačiau buvęs žydų geto kalinys, vėliau tarybinis partizanas Josifas Melamedas po karo sutelkė grupę patyrusių tyrinėtojų specialistų. Vokietijos, Rusijos, Lenkijos ir Izraelio archyvuose jie surado duomenų, kad Ramanauskas dalyvavo nacistams žudant taikius gyventojus.

Melamedas tvirtina, jog jie surado įrodymų, kad Ramanauskas po hitlerininkų įsiveržimo į Lietuvą kartu su grupe savo bendrininkų padėjo naciams šaudyti tarybinius karius. Remiantis Melamedo grupės 1999 metų medžiaga, Izraelio „Žydų, išeivių iš Lietuvos asociacija“ pasiuntė LR generaliniam prokurorui sąrašą kelių tūkstančių lietuvių, reikalaudami ištirti jų nusikaltimus, nes jie bendradarbiavo su naciais ir dalyvavo žydų žudynėse.

Kaip atsakymas 2009 metais pasigirdo grupės Lietuvos Seimo narių raginimas pravesti ikiteisminį tyrimą, bet ne nacių kolaborantų, o Izraelio „Žydų asociacijos...“ ir jos pirmininko, buvusio tarybinio partizano J.Melamedo, „apšmeižusio“ „antitarybinio pasipriešinimo dalyvius“ , atžvilgiu.

Didelis skandalas įsiplieskė Lietuvoje demaskuojant Joną Noreiką, buvusį Lietuvos kariuomenės kapitoną. 1945 metų gruody jis nutarė apjungti Lietuvos „partizanus“. Noreika ir grupė jo bendraminčių sukūrė Vilniuje taip vadinamą Laikiną Lietuvos pilietinę vyriausybę ir Aukščiausiąją Lietuvos ginkluotų pajėgų vadovybę. Vyriausiuoju šių pajėgų vadu Noreika paskelbė save. Dėl to, kad atrodytų solidžiau, jis sugalvojo sau pseudonimą „generolas Vėtra“ . Tačiau kapitonas ir jo bendražygiai Lietuvoje buvo menkai žinomi. O dar jie į visokius postus patys skyrė save. Jų galimybės apjungti Lietuvoje antitarybinį pasipriešinimą buvo minimalios.

Pasireikšti „partizanų“ lyderio vaidmenyje, kaip ir daugeliui jo pirmtakų, Noreikai nepavyko. Jau 1946 metų kovą jis buvo areštuotas ir po metų sušaudytas. Ir vis dėlto dabartinėje Lietuvoje jis gerbiamas kaip vienas iš „partizaninio pasipriešinimo“ lyderių.

Ypač pikantiškai J.Noreikos demaskavimas atrodo todėl, kad tuo užsiėmė jo anūkė Silvija Foti. Remdamasi savo motinos surinkta medžiaga — tai trys tūkstančiai VSK stenogramų puslapių, 77 laiškai senelei, pasaka, kurią Noreika sukūrė Silvijos mamai kalėdamas Študhofo koncentracijos stovykloje, šeimos laiškai apie jo vaikystę bei šimtai laikraščių ir žurnalų straipsnių, — Silvija paruošė knygą „Tiesos ieškant“ . Joje ji daro išvadą, kad jos senelis dalyvavo Holokauste. Silvija patyrė šoką, tačiau Lietuvoje jos išvados buvo priimtos gana santūriai. Juk ji amerikietė, todėl persona neliečiama. Tačiau mitas apie nacių kolaborantus kaip kovotojus už Lietuvos laisvę ir nepriklausomybę stipriai sušlubavo.

Žinoma, įdomu, kaip Lietuvoje buvo pasielgta su nacių karo nusikaltėliais, kurie buvo perduoti į jos teisėsaugos rankas. Štai ką šia proga pasakė aukščiau paminėtas Efraimas Zurofas: „Lietuva, Latvija ir Estija — vienintelės pasaulio šalys, kuriose ant teisiamųjų suolo nebuvo pasodintas nė vienas taikių gyventojų masinių žudynių dalyvis. Teisminiai tyrimai virto akių dūmimais. Teisiamieji net nepasirodė teismuose. Svarbų teisminį procesą valstybės gynėjai pavertė juokais“ .

Įsitikinęs, kad jei šia problema užsiims Rusija, Lietuvai nepavyks išsigelbėti bendrais žodžiais. Atsakyti teks iš esmės. Juk apstu dokumentinių įrodymų, jog Lietuvos „didvyrių, kovojusių už nepriklausomybę“, kurių rankos iki alkūnių suteptos nekaltų aukų krauju, yra daug. Kai kuriuos įrodymus aš priminsiu: „Lietuvos tragedija: 1941–1944 metai. Archyvinių dokumentų apie Lietuvos kolaborantų nusikaltimus Antrojo pasaulinio karo metais rinkinys“ (M., leidykla „Europa“, 2006). A.Diukovas: „Holokausto išvakarėse. Lietuvos aktyvistų frontas ir tarybinės represijos Lietuvoje, 1940–1941 m.“, Holokaustas Lietuvoje: žydų pogromai Vilijampolėje ir masinės žudynės VII forte ; Ž.Butkus: „Kruvinoji Lietuva. Nacionalistinis teroras ir jo priežastys“.

Straipsnio pradžią galima perskaityti čia .

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 19 — id: `scraped:rubaltic_lt:42d01529d2225ea6`

**Title:** „Jums spręsti, ar pradedate naują priešpriešos su Rusiją etapą“, — atviras laiškas Lietuvos teisėjams (1 dalis)

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lietuvoje galimai startuoja paskutinis etapas teisminio proceso, kuris čia vadinamas „Sausio 13-osios byla“, arba jei dar atviriau — „Niurnbergu Rusijai“. Lietuvos politinis elitas neslepia, kad pagrindinis šio proceso tikslas — ne nustatyti teisingumą, o tęsti išpuolį prieš Rusiją, ir kaltinamaisiais teismo salėje bus ne tiek Sausio 13-osios įvykių dalyviai, kaip Rusija — šalis, nelojali vakarietiškoms „vertybėms“. Prieš paskutinį šio užsitęsusio proceso etapą į Lietuvos teisėjus atvirai kreipėsi Vladislav Šved; Lietuvoje vienas iš „teisiamųjų“, o iš tiesų — neišdavęs savo įsitikinimų buvęs antrasis Lietuvos Kompartijos CK sekretorius (nuo 1990 m.), mačiusysis dramatiškus 1991 m. sausio įvykius Vilniuje ir šiuolaikinės Lietuvos Respublikos tyrinėtojas. Analitinis portalas RuBaltic.Ru skelbia pirmąją šio kreipimosi dalį.

Gerbiamieji ponai teisėjai! Jūs nagrinėjate Lietuvai ir Rusijai svarbią baudžiamąją bylą Nr. 09-2-031-99, turinčią tarptautinę reikšmę. Lietuvos žiniasklaida šią bylą vardina „Sausio 13-osios byla“, o baudžiamąjį procesą pagal šią vylą įvardina kaip „Niurnbergą-2“.

Praėjus 72 metams Jums bandoma primesti teisėjų vaidmenį naujo „Niurnbergo“ tribunolo, kuris turi pripažinti kaltais buvusį TSRS gynybos ministrą, TSRS Maršalą Dmitrijų Jazovą, buvusį TSRS Vidaus reikalų ministerijos Vidaus kariuomenės valdybos viršininką Pabaltijo Šiaurės Vakaruose Vasilijų Saviną, buvusį legendinio TSRS VSK grupės „A“ vadą Michailą Golovatovą, kuris visada tvirtai gynė tarybinių piliečių ramybę, buvusį 107-osios motorizuotos šaulių divizijos vadą Vladimirą Uschopčiką, buvusį TSRS Oro desantinės kariuomenės 76-osios divizijos vado pavaduotoją Vasilijų Kustrjo, o su jais 57 buvusius tarybinius karininkus, vykdžiusius Lietuvoje įsakymą TSRS prezidento ir Vyriausiojo kariuomenės vado Michailo Gorbačiovo, kurio, beje, tarp kaltinamųjų nėra.

Dar kartą noriu pabrėžti, kad kaltinamasis baudžiamosios Sausio 13-osios bylos nusprendis iš esmės įtakos Rusijos–Lietuvos santykius. Kaip žinia, Lietuvos ir Rusijos istorija glaudžiausiu būdu susieta aštuonių šimtmečių eigoje. Ir nevalia pamiršti, jog būtent Rusija 1991 metais suvaidino pagrindinį vaidmenį atkuriant Lietuvos nepriklausomybę.

1991 metų sausį RTFSR Aukščiausios Tarybos pirmininko Boriso Jelcino pareiškimas sustabdė prezidentinio valdimo įvedimo Lietuvoje procesą. 1991 m. rugsėjo mėnesį RTFSR prezidento B. Jelcino pozicija TSRS Valstybės taryboje suteikė Lietuvai galimybę išstoti iš TSRS sudėties su visomis tarybiniais metais susigrąžintomis teritorijomis, sudarančiomis 30 proc. dabartinės Lietuvos teritorijos, ir visu pramoniniu ir ekonominiu potencialu, sukurtu gaunant sąjunginio biudžeto finansavimą.

O dar priminsiu, jog 1991 m. rugpjūčio pabaigoje RTFSR prezidentas B. Jelcinas pasirašė Įsaką dėl Lietuvos, Latvijos, Estijos nepriklausomybės pripažinimo . Štai ką apie tai anuometinės Rusijos užsienio reikalų ministro pirmasis pavaduotojas Fiodoras Šelovas-Kovedejavas papasakojo žurnalui „Ruskaja žizn“ (2009 m. sausis). „Aukščiausioje RTFSR Taryboje štai jau pusė metų paruošti dvišalių sutarčių su Pabaltijo respublikomis projektai su sąlygomis ir dėl rusų gyventojų statuso, ir dėl rusų kalbos. Viskas buvo aprobuota atitinkamuose Pabaltijo parlamentų komitetuose. Už savo nepriklausomybę jie buvo pasiruošę sumokėti. Buvo pasiruošę bet kokia kaina pirkti iš Maskvos nepriklausomybę. O Rusija jas pripažino prezidento įsakais išvis be sąlygų. Štai kaip pasireiškė plati rusiška Boriso Nikolajevičiaus natūra“.

Nėra abejonių, kad nuosprendžiai Sausio 13-osios byloje gali atversti naują tolimesnio Rusijos–Lietuvos santykių puslapį arba paaštrinti konfrontaciją tarp dviejų valstybių. Jie juk palies ne tik atskirus Rusijos piliečius, bet ir Rusija, kaip TSRS teisių perėmėją, kurią dabartinės Lietuvos valdžios bando įvardinti kaip nacistinės Vokietijos antrininkę.

Žodžiu, gerbiamieji ponai teisėjai, jums spręsti: arba kaltinamaisiais nuosprendžiais Rusijos piliečiams pradedatenaują ir žiaurų priešpriešos tarp Lietuvos ir Rusijos etapą, arba sąžiningai įvertinate falsifikuotą baudžiamosios Sausio 13-osios bylos medžiagą. Faktiškai prieš jus nelengvas pasirinkimas: arba jūs stojate tiesos pusėn, arba lauksite, kol atsiskleis didžiuliai falsifikavimai, kuriuose šiandien skandinama Sausio 13-osios byla. Tuo, kad jie bus atskleisti, aš neabejoju. Smulkiau apie šiuos falsifikavimus aš papasakosiu vėliau.

Šiandien baudžiamojo proceso situacija vienareikšmiai krypsta link kaltinamųjų nuosprendžių. Tai patvirtino baigiamosios kaltinamosios kalbos Lietuvos prokurorų Gintauto Paškevičiaus ir Daivos Skorupskaitės-Lisauskienės, atstovaujančių baudžiamąjame Sausio 13-osios bylos procese valstybinį kaltinimą. Jie savo kalbose vėl pylė ant jūsų galvų šusnį abejotinių faktų ir įrodymų, daugumą iš kurių iš tiesų yra juridiniai išmislai (paprasčiau, feikai).

Būdama įsitikinusi pagrįstumu savo kaltinimų, kurie išdėstyti Kaltinamąjame akte, arba vykdydama viršininkų nurodymus, D. Skorupskaitė-Lisauskienė savo kaltinamojoje kalboje pasiūlė Vilniaus apygardos teismui nuteisti kalėti iki gyvos galvos D. Jazovą, M. Golovatovą, V. Uschopčiką, V. Kustrjo, N. Demidovą ir V. Saviną. V. Švedą, kaip karinės operacijos Vilniuje kurstytoją, pasiūlyta pasodinti už grotų 20 metų.

Nubausti 16 metų laisvės atėmimų siūloma likusius tarybinius kariškius, apkaltintus įvykdžius karo nusikaltimus ir nusikaltimus prieš žmogiškumą. Tokia bausmė visiškai neatitinka tarybinių kariškių veiksmus 1991 m. sausį. Bet tegul visa tai bus Lietuvos prokurorų sąžinės reikalas.

Kaltinamųjų nuosprendžių paskelbimas duos pradžią rimtos įtampos Rusijos–Lietuvos santykiuose. Pagrindinės problemos Lietuvai iškils tada, kai ji pabandys realizuoti Sausio 13-osios bylai skirtus nuosprendžius. RF Konstitucija neleis išduoti Rusijos piliečius, siekiant juos įkalinti Lietuvos kalėjimuose. Neabejoju — į Lietuvos pasiūlymą įkalinti nuteistuosius Rusijos piliečius Rusijos kalėjimuose bus atsakyta neigiamai.

Lietuvos bandymai, sprendžiant šį klausimą, pasitelkti pagalbon Europos Sąjungą ir JAV nepadės, tik paaštrins situaciją. Rusija mobilizuos savo mokslinį teisinį ir ekspertinį potencialą, o tai padės surasti Kaltinamąjame akte ir baudžiamosios Sausio 13-osios bylos medžiagose daugybę sufalsifikuotų kaltinamųjų epizodų ir liudytojų parodymų, o tai leis kvalifikuoti Sausio 13-osios bylą kaip didelio masto pseudoteisinį falsifikavimą.

Lietuvos bandymai išreikalauti iš Rusijos 11 mln JAV dolerių kompensacijos sausio aukoms taip pat užsibaigs nesėkme. Ši, savo ruožtu, primins savo pretenzijas. Ir tuo pačiu pabrėžiu, jog Rusija nuo 1990 m. kovo siekė ir siekia gerų santykių su Lietuva. Pasikartosiu, jog tik dėl TSRS Valstybės Tarybos pozicijos 1991 m. rugsėjį Lietuva pasitraukė iš TSRS su visais teritoriniais ir materialiais tarybinio laikotarpio įsigijimais. Ir Rusija niekada, sudarydama sutartis su Lietuva, nekėlė klausimo dėl jų sugrąžinimo ar kompensacijos.

Kaip žinia, Lietuvos teisės turėti savo sudėtyje 1939-1945 m. su TSRS pagalba prijungtas teritorijas gan abejotinos. Priminsiu, jog 2003 m. birželio 9 d. RF prezidentas V. Putinas patvirtino įstatymą dėl Rusijos Federacijos ir Lietuvos Respublikos sienų ratifikavimo, tuo pripažindamas esamas Lietuvos sienas. 2003 m. rugpjūčio 12 d. Lietuvos žiniasklaida su pasitenkinimu pažymėjo, kad sutartis dėl sienos su RF įsigaliojo. Tačiau ginčytinų teritorijų problema, jei Lietuva be pagrindo kels Rusijai nepriimtinas pretenzijas, be abejonės atsiras. Tad trumpai apie tai.

Ne paslaptis, jog neegzistuoja teisinių pagrindų, patvirtinančių Klaipėdos ir jos krašto buvimą Lietuvos sudėtyje. Šias teritorijas TSRS perdavė Potsdamo konferencijos metu (1945 m. liepą-rugpjūtį) visiems laikams kaip kompensaciją už nuostolius, kuriuos patyrė TSRS iš nacistinės Vokietijos pusės. O dar verta priminti, kad Klaipėda ir Klaipėdos krašto teritorija aštuonis šimtmečius buvo vokiečių Prūsijos sudėtyje ir vadinosi Memellandu. Kaip žinia, apie šios teritorijos atgavimą Vokietijoje svajoja „Išvarytųjų sąjunga“.

Verta priminti, jog 1939 m. kovo mėn. Lietuva, atsakydama į Vokietijos ultimatumą, sutiko besąlygiškai grąžinti jai Klaipėdos kraštą. Yra žinoma, kad tada Vokietijos užsienio reikalų ministras Jochimas Rybentropas griežtai pareiškė Lietuvos užsienio ministrui Juozui Urbšiui, jog Lietuvai atsisakius tai padaryti, į ją bus įvesti Vermachto daliniai, o Lietuvos sostinė Kaunas — „sulyginta su žeme“. Ir tuo metu Lietuvai buvo įžeidžiančiai patarta: „Siekdami išvengti tuščiai praleisto laiko, pasiųskite specialiu lėktuvu į Berlyną įgaliotuosius asmenis, kad pasirašytų perdavimo Vokietijai Memelio rajoną dokumentą“. Nelaukdamas oficialaus Lietuvos atsakymo į ultimatumą, Hitleris išvyko į Klaipėdą-Memelį vokiečių karinio laivyno flagmanu „Doičland“.

1939 m.kovo 22 d. J. Urbšys ir J. Rybentropas pasirašė sutartį-paktą, kurios 1-ame straipsnyje buvo konstatuota, kad „Klaipėdos kraštas, kuris pagal Versalio sutartį buvo atplėštas nuo Vokietijos, vėl prijungiamas prie vokiečių Reicho“. 1939 m. balandžio 1 d. prezidentas A. Smetona ratifikavo šią sutartį. Ir todėl, kad dabartinė Lietuvos Respublika skelbiasi esanti 1938 m. smetoniškos respublikos tęsėja, Urbšio-Rybentropo paktą galima laikyti galiojančiu su visomis išplaukiančiomis pasekmėmis .

Neatsitiktinai žinomas Lietuvos istorikas Liudas Truska 2011 m. kovo 7 d. interviu informaciniam portalui Delfi.lt pareiškė: „Kaip žinoti, o gal visa tai vėl atsinaujins, ir Vilnius, ir Klaipėda taps ginčų klausimu? Mes 100 procentų negalime pasakyti, kad ankstesnės teritorinės problemos ateityje nepasikartos“. Išmintingi žodžiai, tačiau Lietuvos politikai jų nenori girdėti.

Verta priminti ir taip vadinamo Suvalkų iškyšulio teritoriją. Jame Vilkaviškio, dalinai Marijampolės, Seinų ir Alytaus apskritys, kurių plotas 8,2 tūkst. kv. km. Šią pietvakarių Lietuvos teritoriją 1939 m. rugsėjį po Lenkijos sutriuškinimo Vokietija norėjo pasilikti sau, prisijungdama ją prie taip vadinamo Suvalkų trikampio. Prisijungdama Suvalkų iškyšulio teritoriją prie šio trikampio, ji būtų gavusi platų karinį placdarmą būsimąjame kare su TSRS.

2018 m. birželio 22 d. RF Gynybos ministerijos paviešintas pradinio „Barbaroso plano“ etapo trofėjinis žemėlapis vaizdžiai patvirtina Vermachto jėgų koncentraciją Suvalkų trikampyje 1941 m. birželio mėn.

Tarybinė vadovybė įvertino Suvalkų iškyšulį kaip turintį Vokietijai strateginę reikšmę būsimąjame kare su TSRS. Todėl, pasirašydama 1939 m. rugsėjo 23 d. TSRS-Vokietijos sutartį, pagal kurią Lietuva pateko į TSRS įtakos sferą, šalies Liaudies komisarų tarybos pirmininkas Viačeslavas Molotovas pareikalavo, kad iškyšulys liktų Lietuvoje, nors TSRS turėjo visišką teisę paimti jį savo kontrolėn . Šis kilnus žingsnis kainavo TSRS, pagal 1941 m. sausio 10 d. Sutartį su Vokietija, 7,5 mln auksinių dolerių. Šiandien ši sumą sudaro apie ketvertį milijardo JAV dolerių. O susitarimo dėl šios teritorijos pirkimo niekas nepanaikino.

Rusija ir Baltarusija kol kas nekelia klausimo, kad Lietuva prarado teisę disponuoti Baltarusijos TSR šiaurės vakarų teritorija, kurią sudaro 6,6 tūkst. kv. km. Ši teritorija buvo perduota Lietuvos TSR jai įstojant į TSRS 1940 m. rugpjūčio mėn. Savo teisę disponuoti šiomis teritorijomis Lietuva prarado 1990 m. kovo 11 d. todėl, kad 1940 m. rugpjūčio 3 d. Įstatymą „Dėl Lietuvos Tarybų Socialistinės Respublikos priėmimo į Tarybų Socialistinių Respublikų Sąjungą“ pripažino negaliojančiu .

Kaip žinia, 1990 m. kovo 29 d. Baltarusijos TSR Aukščiausiosios Tarybos Prezidiumas pasiuntė Lietuvos Aukščiausiajai Tarybai oficialų Pareiškimą, kuriuo priminė, kad Baltarusijos teritorijų buvimo Lietuvos TSR sudėtyje pagrindas — TSRS Aukščiausiosios Tarybos Įstatymas „Dėl Lietuvos Tarybų Socialistinės Respublikos priėmimo į Tarybų Socialistinių Respublikų Sąjungą“.

Šiame pareiškime buvo pažymėta, jog dėl to, kad Lietuvos Respublikoje aukščiau paminėtas įstatymas paskelbtas negaliojančiu, iškyla klausimas dėl Baltarusijos rajonų buvimo Lietuvos sudėtyje pagrįstumo . Situacija Lietuvos naudai išgelbėjo TSRS prezidentas Gorbačiovas, pasiekęs, kad Baltarusija atsisakytų šių pretenzijų, nes tai esą trukdė deryboms tarp Maskvos ir Vilniaus. Ir vis dėlto, visiškai aišku, jog dabartinė Lietuva, nepripažinusi TSRS Įstatymo dėl Lietuvos TSR įstojimo į TSRS sudėtį, prarado teisę disponuoti baltarusių teritorijomis. Baltarusijos TSR Aukščiausiosios Tarybos Prezidiumo Pareiškimas buvo išspausdintas 1990 m. balandžio 1 d. laikraštyje „Zvezda“.

Atskirai pasakysiu apie Vilno ir Vilno krašto teritoriją, kuri buvo perduota Lietuvos Respublikai 1939 m. spalio 10 d. pagal TSRS-Lietuvos sutartį. Yra žinoma, kad dabartinės Lietuvos valdžios 1939 m. rugpjūčio 23 d. nepuolimo sutartį tarp TSRS ir Vokietijos (taip vadinamą Molotovo-Rybentropo paktą) laiko nusikalstamu. Tačiau būtent TSRS-Vokietijos 1939 08 23 sutartis tapo teisiniu pagrindu pasirašant 1939 10 10 TSRS-Lietuvos sutartį dėl perdavimo Lietuvai Vilniaus ir Vilniaus krašto.

Neigdama 1939 08 23 TSRS-Vokietijos sutartį , Lietuva neišvengiamai neigia 1939 10 10 TSRS-Lietuvos sutartį ir tuo pačiu atkuria status quo, t.y. pripažindama Vilnių ir Vilniaus kraštą priklausiančius Lenkijai . Juk nepaneigiamas faktas — Vilnius ir Vilniaus kraštas Lietuvos Respublikos sudėtyje yra TSRS-Vokietijos sutarties, vadinamos „Molotovo-Rybentropo paktu“ išdava ir paskutinis reliktas.

Bus daugiau ...

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 20 — id: `scraped:rubaltic_lt:520a97553f8668c8`

**Title:** Lietuva prisimena Holokausko aukas heroizuodama karo nusikaltėlius

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Vokiškieji okupantai 1943 metų rugsėjo 23 dieną pradėjo likviduoti Vilniuje žydų getą. Vėliau Lietuvos Seimas patvirtins šią datą kaip oficialią žydų genocido aukų atminimo Dieną. Tradiciškai rugsėjo 23 dieną Pabaltijo respublikoje organizuojama gana daug teminių renginių. Lietuva stengiasi parodyti, kad mini Holokausto tragedijos aukas ir pergyvena skausmą, tuo pačiu metu heroizuodama kolaborantus, kuriuos istorikai įvardina žydų žudikais.

Prieš nacistų talkininkų atminimo įamžinimą nenuilstamai kovoja JAV pilietis, lietuvių kilmės žydas Grantas Gočinas, apie kurį jau rašė analitinis portalas RuBaltic.Ru. Lietuvos gyventojų genocido ir rezistencijos tyrimų centre buvo išsakyta užuomina, kad daug puslapių užimantis užklausimas, adresuotas šios organizacijos vadovei Teresei Birutei Barauskaitei, gali būti traktuojamas kaip turintis respublikos Konstitucijos ir Baudžiamojo kodekso pažeidimų požymius.

Dar vieną kreipimąsi Gočinas pasiuntė Lietuvos prokuratūrai, kaltindamas Barauskaitę nusikalstamu Holokausto neigimu. O strėlės skrajoja aplink žinomo „miško brolių“ vado Jono Noreikos figūrą. Pasak Gočino, nuo 2015 iki 2018 metų Centro direktorė aktyviai neigė nusikalstamą nacių talkininko veiklą. Kaip ryškų šios politikos pavyzdį kreipimosi autorius pateikia istoriko Alfredo Rukšėno 26 puslapių straipsnį, išspausdintą Centro leidžiamame žurnale. Jame Noreika vaizduojamas kaip „žydų gynėjas, kuris nieko nežinojo ir neturėjo polinkių genocidui“.

Apie tai, kaip „ekonominį genocidą“ vykdė Noreika, neseniai pasauliui paaiškino jo anūkė Silvija Foti: „Netrukus po sukilimo mano senelis pervežė savo šeimą į „staiga išsilaisvinusį“ namą miesto centre ir gyveno jame iki persikėlimo į Šiaulius, kur tapo apskrities pirmininku“. Kaip išsiaiškino Foti, tai buvo tipiškas scenarijus. Žydai „dingdavo“, namai išsilaisvindavo, juos užimdavo lietuviai.

Silvijos Foti sensacinis prisipažinimas — dar vienas kozyris rankovėje Granto Gošino, kuris tvirtai pasiryžęs pasiekti teisingumo. Prokuratūrai adresuotą laišką jis užbaigia šiais žodžiais: „Centro direktorės ir istorikų veiksmai atitinka Holokausto neigimo apibrėžimą, kuris vykdomas Lietuvos Respublikos vardu platinant propagandą valstybės lėšomis. Remiantis tuo, kas išdėstyta aukščiau, mes prašome pradėti ikiteisminį tyrimą Teresės Birutės Barauskaitės atžvilgiu dėl nusikaltimo, numatyto Baudžiamojo kodekso 170 (2) straipsniu“.

Rugpjūčio 24 d. Gočinas patalpino savo saite atsakymą. Susipažinęs su pateikta medžiaga, jis priėjo išvados, kad „vienašališki istoriniai apibendrinimai galimai neatitinka tikrovės, o Centro istorikų pozicijos ne visada sutampa su pareiškėjo pozicija „kai kuriomis aplinkybėmis“. Žodžiu, užsiimti tyrimu prokuratūra atsisakė.

Tačiau Grantas Gočinas neketina pasiduoti. Jis ir ateityje drums Lietuvos institutų ramybę ir gins savo poziciją teisme. Rugsėjo 12 d. jam buvo pranešta, kad Lietuvos vyriausybė, siekdama apginti savo interesus, nusisamdė žinomą advokatę Liudviką Meškauskaitę. Gočinas pabrėžia, jog Lietuva pasiruošusi mokėti pinigus už nacių nusikaltėlio „gero vardo“ gynimą.

O atskiras Gočino kreipimasis skirtas savo tėvynainiams: „Lietuva tvirtina esanti žydų draugė, norinti su jais susitaikymo. Ji ieško pas žydus investicijų [ir galimybės] vystyti turizmą, naudodama pinigus žydų žudikų reputacijos gynimui. Štai kaip dirba jūsų turistinių pinigų pelnas“.

Rugpjūty, prieš genocido aukų atminimo Dieną, tinklalapyje atsirado dar vienas įdomus dokumentas: tyrimas pavadinimu „Holokausto supainiojimo Baltijos judėjimas“. Manau, nebūtina aiškinti, kuo pasipiktinęs jo autorius profesorius Dovidas Kacas.

Štai vienas iš jo pastebėjimų: Genocido aukų muziejuje Vilniuje iki 2011 metų nebuvo žodžio „Holokaustas“. „Kitaip sakant, tas genocidas, kuris realiai vyko Lietuvoje, nebuvo pastebėtas, ir tai tuo metu, kai esą serija baisių nusikaltimų, kurie vis tiek po savęs paliko sėkmingai besivystančią šalį su augančiu gyventojų skaičiumi, pasiruošusią po TSRS griūties kuo greičiau įstoti į ES ir NATO, čia buvo pripažinti „genocidu“.

Apie tai, kaip Lietuvoje supainiojama Holokausto istorija, šiomis dienomis papasakojo teisių gynėjas Grantas Gočinas. Rugsėjo 10 d. jis su draugais, Lietuvos rusų sąjungos ir Socialistinio liaudies fronto atstovais, pabuvojo Merkinės miestelyje. Jo apylinkėse prieš 77 metus vokiškieji okupantai su vietos kolaborantais nužudė 854 žydus. Tačiau, pasirodo, genocido aukų vietą miestelyje sunku surasti — daug sunkiau, nei jų žudikų atminimo įamžinimo vietą.

„Aplankę muziejų, mes ėmėme ieškoti Holokausto aukų laidojimo vietos. Noriu pabrėžti, kad ieškojome ilgai, — rašo Grabauskas, —panašiai kaip šių metų rugpjūty ieškojome sunaikinto Vašukėnų kaimo. Vietą sunku rasti, nes per mažai rodyklių, ir net tada, kai lyg jau ėjome reikiama kryptimi, ir tai ne iškart radome. Nesimato aiškių takų, viskas užžėlę“.

Merkinės apylinkėse pabuvojo ir Klaipėdos deputatas Viačeslavas Titovas, išdrįsęs suabejoti, ar verta kabinti memorialinę lentą dar vienam Lietuvos „kovotojui už laisvę“ — „miško brolių“ vadui Adolfui Ramanauskui Vanagui.

Dabartinės Lietuvos didvyrių panteone Ramanauskas — viena išskirtinių, jei ne svarbiausia figūra. Į partizaninės veiklos viršūnes jis iškilo po karo, todėl „Vanago“ šalininkai tvirtina, kad su naciais jis nebendradarbiavo. Tačiau kai kurie tyrinėtojai mini jo dalyvavimą susidorojant su taikiais gyventojais, tame tarpe ir žudant Merkinėje žydus.

Titovo bylą miesto meras Vytautas Grubliauskas pavadino „ilgu, sudėtingu, tačiau svarbiu procesu“. Visiems „neįtinkantiems“ tai bus pamoka, kaip bus pasielgta su tais, kuriems nepriimtina oficiali Lietuvos istorijos traktuotė.

Nemaloniu siurprizu Lietuvos „patriotams“ tapo respublikoje gyvenančių žydų pozicija. Rugpjūty Lietuvos žydų bendrija (LŽB) paviešino atvirą laišką, kuriame išreiškė susirūpinimą, kad „vis dar visuomenėje kyla diskusija dėl Jono Noreikos (generolo Vėtros) atminimo įamžinimo. LŽB atkreipė dėmesį, kad reikėtų nuimti memorialinę Jono Noreikos lentelę nuo Vrublevskių bibliotekos pastato. Beje, žydų bendruomenė paragino valdžias tai padaryti kaip tik iki rugsėjo 23 dienos.

Nuostabu: net amerikiečių spauda neseniai susidomėjo Jono Noreikos figūra. Straipsnį pirmame puslapyje jam skyrė The New York Times. Analitinis portalas RuBaltic.Ru kruopščiai išnagrinėjo publikaciją, kurios autorius daro vienareikšmę išvadą: Jonas Noreika pasirinko neteisingą kelią. Ar tai ne užuomina, kad lietuviškiesiems draugams verta peržiūrėti savo požiūrį į „generolą Vėtrą“?

Ir vis dėlto šią problemą Lietuvoje stengiamasi tolerantiškai ignoruoti. Tikėtina, jog žydų genocido aukų atminimo Dieną memorialinė lenta Jonui Noreikai – žmogui, kurį baisiais nusikaltimais kaltina net jo anūkė – tebepuikuosis ant Vrublevskių bibliotekos pastato. O norintiems suabejoti jam panašių personažų „didvyriškumu“ valdžios visada pasiruošusios viešai išvanoti kailį. Žydų bendruomenės susirūpinimas tebelieka be dėmesio.

Tai kokią atmintiną datą Lietuva mini rugsėjo 23 dieną?..

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```
