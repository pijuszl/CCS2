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

### Article 1 — id: `scraped:rubaltic_lt:13273a99e993a929`

**Title:** Padnestrė ir Kaliningradas. Kijevas agituoja už „antruosius frontus“  kare su Rusija

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Kijevo režimas agituoja savo sąjungininkus atidaryti „antruosius frontus“ Rusijai visame jos sienos perimetre. Tarp labiausiai perspektyvių „skausmo taškų“ minimos Kurilų salos ir Kaliningrado sritis. Tikrovėje sąjungininkai pasirodė tuščiakalbiais: Rusijos specialioji operacija Ukrainoje atvedė juos į protą, todėl Kijevui, kuris aštuonerius metus siekė ir pagaliau pasiekė susidūrimą su Rusiją, jie siūlo kariauti su ja vieniems patiems.

Ukrainos nacionalinio saugumo ir gynybos tarybos sekretorius Aleksejus Danilovas pareiškė, kad prieš Rusiją būtina atidaryti „antruosius frontus“, „Jei prieš Rusiją bus atidaromi antrieji frontai, tai mums bus labai gera pagalba kovoje su okupantų užpuolimu“, - kalbėjo Danilovas, ir, kaip į perspektyvius Kremliaus „skausmo taškus“, nurodė Kurilų salas, Karabachą ir Kaliningrado sritį.

Jo pasisakymas rodo, kaip įtemptai Ukrainos valdžia stebi tarptautinį landšaftą, tikėdamasi stebuklo, kuris pakeis jos beviltišką situaciją. Panašiai taip pat 1945 metais Hitlerio vadavietėje buvo laukiama ar tai Ruzvelto mirties, ar tai antihitlerinės koalicijos sąjungininkų ginčų, ar dar ko tai, kas pagelbės užkirsti kelią katastrofai.

Tai įrodo Tbilisio ir Kišiniovo reakcija į Danilovo pasiūlymą. Ukrainos vadovybei būtų labai gerai „jei šiandieną ir Moldova ir Gruzija užsiimtų savo teritorijų gražinimu“, - sakė NSGT sekretorius.

„Raginimas Gruzijai pradėti naują karą su Rusija niekaip nėra siejamas su Gruzijos tautos interesais“, - atsakė Danilovui parlamento valdančios partijos „Gruzijos svajonė“ deputatas Michailas Sardžveladzė, pažymėdamas, kad siūlymai eiti ir iš Maskvos atkariauti „okupuotas teritorijas“ dabartiniu metu „neteisingi ir nepagristi“ .

Anksčiau Kijevas (teisingiau pasakius – Kijevo režimas, kuris geografiškai vargu ar randasi Kijeve) ne kartą yra pareiškęs, kad laukia Rusijos taikdarių smūgio Padnestrėje, ir siūlė sąjungininkei Moldovai paremti Ukrainą, pačiai smūgiuojant į Padnestrę. Oficialus Kišiniovas atsakydamas, kaip mantrą tvirtino, kad Moldova neutrali, savo neutraliteto nepažeis ir nekariaus.

Gaunasi tragiško farso situacija.

Kas išvertus reiškia: patys užšokote ant Rusijos – patys su ja ir kariaukite.

Iš nevilties Kijevo režimas kabinasi netgi už neoficialių pareiškimų, skelbdamas juos valstybės politiką. Tas pats Danilovas prisikabino prie lenkų dimisijos generolo Voldemaro Skšipčako pasisakymo, paskelbusio, kad nuo 1945 metų Kaliningrado sritis yra „rusų okupuota teritorija“.

„Lenkija, kol kas neoficialiame lygyje, jau pareiškė savo pretenzijas į Kaliningrado sritį. Tai mus tikslai paremtu“, - šį pasisakymą komentavo NSGT sekretorius, įvertinęs dimisijos generolo pasisakymą kaip oficialią Varšuvos poziciją.

Tarp kitko, su Lenkija ir Pabaltiju Zelenskio komanda turi visgi daugiau šansų dėl „antrojo fronto“, negu su Gruzija ir Moldova. Ukrainos tragedija NATO „Rytų sparno“ šalių neatvedė į protą, taip pat kaip ir ES „Rytų partnerystės“ programos „pirmūnų“. Lenkija ir Baltijos šalys, kaip ir anksčiau, stengiasi didinti įtampą ir fontanuoja antirusiškais pasiūlymais. Būtent dėl tos priežasties, kad jos – teisėtos Šiaurės Atlanto aljanso dalyvės, kurio pagrindinės šalys patvirtino, kad rusiškos agresijos atveju, jos kariaus už jas.

Be NATO.

Dėl to buvo užmirštos visos drąsios lenkų ir pabaltijiečių iniciatyvos. Ukrainos oro erdvės uždarymas, kovinių oro laivų tiekimas Ukrainai kariuomenei, NATO taikdarių kontingento įvedimas į Ukrainą – viskas „nuėjo užmarštin“.

Lenkija ir Lietuva taip pat bandė aktyvuotis dėl Kaliningrado srities. Prieš keletą savaičių lenkų vyriausybėje prasitarė, kad kartu su kolegomis iš Lietuvos apgalvojama Kaliningrado transporto blokada apeinant Europos sąjungos lygio reglamentus ir susitarimus.

Ši tema taip pat baigėsi niekuo. Panašu, kad Varšuvai ir Vilniui „atlėkė“ iš paminėtos Europos sąjungos. Briuselyje visgi dar iki galo neišprotėjo nuo visų tų susirūpinimų dėl Ukrainos likimo: ten supranta, Kaliningrado srities blokavimas Maskvai - casus belli. O kariauti su ja niekam nesinori.

Atitinkamai, visa Lenkijos ir Lietuvos parama Ukrainai nuo to „antrojo fronto“ bus tik tame, kad jie taps Kijevo įsteigto geopolitinių nevykėlių klubo nariais, kurie daugelį metų „kariavo“ su Rusija ir apsidergė, kai ta, pagaliau, į tą karą atvyko.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 2 — id: `scraped:rubaltic_lt:b8cca41b5439e724`

**Title:** Pabaltijys lobijuoja Rusijos jūrų blokadą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Baltijos šalys ketina uždrausti įplaukti į savo jūrų uostus rusų laivams ir ragina likusius Europos sąjungos narius pasekti jų pavyzdžiu. ES tradiciškai nėra pasirengusi paremti radikalias antirusiškas Rytų Europos iniciatyvas, todėl viskas juda link eilinio „persišovimo“ – simbolinio, žalingo patiems sau, Pabaltijo veiksmo. Gi, tos sankcijos nieko nepakeis, kadangi ir be to dauguma rusiškų kompanijų jau seniai atsisakė Lietuvos, Latvijos ir Estijos uostų.

Latvijos susisiekimo ministras Talis Linkaits žadėjo uždrausti įplaukti į jūrų uostus laivams su Rusijos vėliava.

„Mes vylėmės, kad bus bendras Europos sąjungos sprendimas. Mes matome, kad yra šalys kurios ryžtingai tam priešinasi, todėl akivaizdu, kad sprendimas bus regioninio pobūdžio“, - papildė Linkaits.

Pastaba yra principiška. Baltijos šalys lieka sau ištikimos. Jos visada pareiškia pačias radikaliausias antirusiškas iniciatyvas ir jas pateikia savo didiesiems, įtakingiems ir atsargiems „vyresniesiems draugams“ iš NATO ir Europos sąjungos kaip nekompromisingumo ir ryžtingumo pavyzdį, pirmosios prisiimdamos atitinkamų priemonių. Taip buvo nuo 2014 metų, su ginklų tiekimu Kijevui – taip ir dabar, su rusų laivų blokavimu.

Atitinkamų priemonių jau imamasi. Taip, nuo kovo pradžios laivams su Rusijos vėliava uždraudė įplaukti į Klaipėdos uostą. Atsižvelgdama į šį sprendimą, o taip pat ir į sankcijas Baltarusijai bei baltarusiškų krovinių netekimą, uosto vadovybė prognozuoja beveik dvigubą krovinių apyvartos sumažėjimą.

Savo ruožtu, Latvijoje Rygos uoste numatomas beveik dvigubas krovinių apyvartos sumažėjimas, o Ventspilio uoste – dvejais trečdaliais. Ir tai tada, kai pastaraisiais metais apyvarta nenumaldomai mažėjo. Esant tokiai padėčiai jūrų uostose, ne visai suprantama, kam Latvijai ir Lietuvai reikalingas geležinkelis, ir kokių lėšų dėka jos toliau galės gyvuoti.

Tačiau Pabaltijį, kaip galima nesunkiai suvokti, tai nesustabdys. Kuo didesnė auka, kuria jos aukojasi, tuo įtikimesniu atrodo jų principingumas ir ištikimybė „vertybių politikai“.

Dar 2016 metais RF vadovybė paskelbė Pabaltijo transportinių pajėgumų persiorientavimo kursą į tėvyninius, ir nuo to meto rusiškas tranzitas nenumaldomai kėlėsi iš Pabaltijo. Tuo ir paaiškinamas dramatiškas Pabaltijo uostų apyvartos kritimas pastaraisiais metais.

Šiandiena surištomis su Lietuvos, Latvijos ir Estijos uostais pasiliko tik mažas kiekis nedidelių kompanijų, kurios neatsiliepė į daugkartinius raginimus neturėti reikalų su beribiai nedraugiškomis Rusijai šalimis, tuo metu, kai egzistuoja tėvyninė alternatyva, ir savo tranzitą perkelti į tėvynę. Taip joms dabar ir reikia.

Bendrai paėmus, eiliniai Pabaltijo išpuoliai Rusijai – tai „niekas“. Jį jų netgi nepastebės. Eilinis Pabaltijo „šūvis sau į koją“ - Lietuvai, Latvijai ir Estijai standartinis simbolinis veiksmas, kuris yra gryna politinė, niekam neturinti jokios įtakos, demonstracija.

Ar tai reiškia, kad iš viso nereikia kreipti dėmesio į jų paiką aktyvumą? Ne, čia yra savo niuansas.

15 pastarųjų metų Pabaltijys panaudojamas labiausiai radikalių, antirusiškų sprendimų „įdirbimui“, kurie Vakaruose pradžioje vertinami kaip neįmanomi, bet po kelių metų ten tampa norma.

Dėl to verta dėmesio neseniai pasirodžiusi JAV atstovų prielaida apie visišką Rusijos prekybos blokadą, kuri tame tarpe pasireikš ir rusiškų laivų įplaukimo blokavimu į neutralius vandenis, draudimu jiems įplaukti į užsienio uostus ir jų užgrobimu tarptautiniuose jūrų keliuose.

Tai pats tas, kas kol kas Vakarams neįmanoma, bet Baltijos šalims jau tampa norma. Jei Rusija nesutramdys savo šiaurės – vakarų kaimynių, po kelerių metų (o gal būt ir anksčiau, kadangi dabar laikas bėga greičiau), tai taps standartu ir Vakarams.

Todėl Rusijai pats laikas pagaliau kaip reikiant atsakyti Pabaltijui į jo nedraugiškumą.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 3 — id: `scraped:rubaltic_lt:0772a9db115fc3f9`

**Title:** Mus nepriversti tylėti, kol mus skaito, Pabaltijyje užblokavo  RuBaltic.Ru

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Latvija oficialiai užblokavo RuBaltic.Ru analitikos portalą, pavadinus jį grėsme valstybės saugumui. Apsunkinta prieiga į svetainę Lietuvoje. Tai yra pripažinimas ir pasisekimas: beveik po 10 metų nesėkmingų bandymų paneigti tai ką rašo RuBaltic.Ru apie Pabaltijį, Baltijos šalių valdžia ėmėsi jį bukai „slopinti“. Bukumas tame, kad ši jų priemonė sužlugs, kaip ir visos buvusios prieš tai, kadangi prieš Pabaltijo režimus sukyla technologinis procesas.

Pavadinkime daiktus tikraisiais vardais: Internete neįmanoma kažką tai galutinai ir visam laikui uždrausti, jei žmonės nori skaityti bei žiūrėti tai ką siūlo autoriai, kurie jiems yra įdomūs, jie tai darys, ir jokia blokada jų nesustabdys. Nesustabdys netgi Latvijoje jau įvestos administracinės nuobaudos už tai kad žiūrima nepageidaujama žiniasklaida.

Įstatymu laikomasi kai yra gerbiama, juos išleidusi valstybė. O kaip gerbti šalį, kuri taip bijo nuo jos nepriklausančių žurnalistų, kad yra pasirengusi bausti tuos, kurie skaito jų publikacijas?

Prasidėjo nuo to, kad Lietuvos valstybinių aukštųjų mokyklų vadovybei buvo skambinama iš Prezidentūros ir reikalaujama uždrausti savo darbuotojams duoti interviu bei komentarus RuBaltic.Ru portalui. Po to mus paskelbė „Kremliaus minkštos jėgos instrumentu“, kurį sukūrė Rusijos specialiųjų tarnybų elitas kad diskredituoti Dalią Grybauskaitę. Per visą Lietuvą nuskambėjo raginimas: nieko neskaityti iš „Maskvos propagandos“ ir niekuo netikėti!

Po to šių eilučių autoriui buvo uždraustas įvažiavimas į Lietuvą su formuluote „asmuo keliantis grėsmę nacionaliniam saugumui“. Prisipažįstu, tai buvo velniškai malonu ir staigiai padidino mano savivertę. Pasirodė, kad Lietuvos valdžia mūsų portalą ne tik nagrinėja, bet dargi jo bijosi. Apie tai, kad ten mus skaito, man buvo žinoma: perduodavo, kaip mano straipsnius perpasakoja Klaipėdos mokyklose pertraukų metu.

Po to Latvijos saugumo policija savo metinėje ataskaitoje nurodė, kad RuBaltic.Ru pasirodymas tapo pačia reikšmingiausia grėsme informaciniam saugumui per ataskaitinį periodą. Kaip paaiškėjo, mūsų prisibijo ir Latvijoje.

Praėjo dar metai ir mano knygas apie Pabaltijį uždraudė pardavinėti Estijoje. Paskui Lietuvoje...Ko jie taip išsigando?

Pakankamai neįtikinamu rodosi mitas apie šalių, iš kurių pabėgo pusė darbingų gyventojų, kurios velkasi visų sėkmingumo Europos sąjungoje reitingų gale ir pakiša savo tuštėjančią teritoriją Rusijos raketų smūgiams, įveždamos į ją NATO puolamąją ginkluotę, „sėkmę“. Jis subyrėjo nuo pateikiamų bazinių faktų apie Pabaltijo respublikas, ir paneigti šiuos argumentus Lietuvoje, Latvijoje ir Estijoje niekas negalėjo, viskas kas jiems beliko – bandyti diskredituoti oponentą.

Todėl ant RuBaltic.Ru daugelį metų buvo pilamas didžiausias užsakytų „žurnalistinių tyrimų“, „faktų tikrinimo komisijų“ ataskaitų, „sensacingų demaskavimų“ , kurie vėliau buvo pateikiami Latvijos prezidentui, srautas, taip pat specialiųjų tarnybų ataskaitose bei valstybės televizijoje reguliariai buvo vertinamas kaip informacinė grėsmė.

Facebook Rytų Europos biurui buvo nurodyta apriboti portalo turinį socialiniame tinkle, o kai   RuBaltic.Ru pradėjo vystyti video formatą, analogiškos problemos prasidėjo ir su YouTube.

Tačiau norimo rezultato vis vien nebuvo pasiekta.

Apie tai, kad svetainė, nežiūrint į bet ką, įtakoja protams, sakė ir vietiniai kovotojai su „rusiška grėsme“, ir, dabar Rusijoje pripažinti nepageidaujamomis organizacijomis, amerikiečių ekspertų centrai, kurie specializuojasi kovoje su rusiška įtaka Rytų Europoje. Todėl viskas ėjo link paprasto ir buko, kaip laužtuvas, sprendimo: užblokuoti RuBaltic.Ru Baltijos šalyse.

Ar pagelbės šis draudimas? Nepagelbės. Dėl aukščiau išdėstytų priežasčių. Šiuolaikinės Interneto technologijos suteikia galimybę lankytis ir uždraustuose Interneto svetainėse. Uždrausta žiniasklaida vis vien gyvuos, kol yra kam ten dirbti ir yra tas, kas ją skaito.

Išgelbėti Pabaltijo režimus nuo galvos skausmo RuBaltic.Ru pavidale galime tik mes patys, jei nustosime rašyti, filmuoti, kalbėti ir publikuoti. O mes nenustosime.

O nutraukti šį gyvą ryšį tarp redakcijos ir žmonių negali joks administracinis draudimas.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 4 — id: `scraped:rubaltic_lt:8c410d32fec61aff`

**Title:** Ant jūros blokados slenksčio: JAV grasina panaudoti jėgą prieš Rusiją

**Source:** rubaltic_lt (propaganda)

**Text:**

```
JAV leidžia galimu paskelbti totalinį prekybos embargo Rusijai, kas numato visišką jūros kelių užtvėrimą ir laivų užgrobimą. Panašūs grasinimai – nevilties gestas, kadangi jie reiškia masinį badą pasaulyje ir Trečiojo Pasaulinio karo pradžios priežastį. Tačiau amerikiečiams nieko kito nebelieka, kaip maksimaliai didinti spaudimą: nuo „pragariškų sankcijų“ Rusija nepalūžo, ir JAV belieka pasirinkti – arba atsisakyti nuo Ukrainos, arba jėgos panaudojimu pakeisti ekonominį Maskvos spaudimą.

Jungtinės Amerikos Valstijos rengia eilines sankcijas Rusijai. JAV finansų ministro pavaduotojas Uoli Adaijemo interviu CNBC televizijos kanalui pareiškė, kad amerikiečiai „vis dar svarsto visišką prekybos embargo ir RF prieigos prie tarptautinių vandens kelių blokavimą“.

Iš visų amerikiečių pareiškimų apie galimas naujas sankcijas, būtent tas sukėlė patį didžiausią tarptautinį atgarsį. Suprantama kodėl. Visos kitos iniciatyvos – tai ankstesnės linijos tęsinys, bandymai sugniuždyti Rusiją taikant ekonominį spaudimą. Jie jau nebeįdomūs, todėl, „linija“ neveikia.

Paskutinėmis savaitėmis Rusiją padengusi „devintoji sankcijų banga“  jos nepalaužė. Rusijos ekonomija ir toliau gyvuoja, milijonai rusų, patyrę šoką, netekus „Makdonaldo“ su „Koka-Kola“, neišėjo į gatves nuversti Putiną, ir, svarbiausiai, specialioji karinė operacija Ukrainoje buvo tęsiama.

Dabar galima diskutuoti dėl draudimo įvežti iš Rusijos nikelį ir uraną arba naftą ir dujas, bet jokio šių priemonių efektyvumo jau niekas negarantuoja. Aštuonerius metus Rusija buvo bauginama atjungimu nuo bankinės SWIFT sistemos. Vasario mėnesį stambiausius bankus atjungė nuo SWIFT sistemos – ir kas? Ir nieko. Valstybei tai nieko nepasikeitė, jos veikloje iš viso nepastebima pakitimų. Dabar taip pat baugina uždrausti energijos nešėjų tiekimą... ir patys mato, kad Rusijos požiūris į tokius grasinimus yra flegmatiškas ir tai jos visiškai nebaugina.

Tokiu būdu nauji ekonominiai apribojimai gali būti įvedami tik tam, kad nubausti Rusiją ir rusus už nepaklusnumą. Atkeršyti, padaryti jiems kiek galima skaudžiau. Tai emocijos. Svarbiausiame sankcijos neveikia. Jie negali priversti Putiną „pakeisti savo elgesį“. Karinė specialioji operacija tęsiama.

Finansų ministro informacijos apie galimą jūros kelių Rusijai užtvėrimą įmetimas, šia prasme yra riba. Kaip Jungtinės Valstijos gali blokuoti Rusijos prekybinių laivų logistiką? Tik jėga. Užgrobiant abordažu laivus ir konfiskuojant prekes. Naujaisiais laikais toks reiškinys buvo vadinamas kaperių arba korsarų praktika, tiesiai pasakius -  įteisintas piratavimas.

Amerikiečiams panašūs veiksmai bus lošimas peržengiant bet kokias leistinas ribas.

Rusija – stambiausias pasaulyje kviečių tiekėjas. Kartu Ukraina ji duoda trečdalį pasaulinio eksporto. Sėja Ukrainoje sužlugdyta, daugelis logistikos grandinių, per kurias buvo tiekiami rusiški grūdai, sugriauta, dėl ko Afrikos kontinentas jau atsidūrė ant bado slenksčio, o Europoje jau prasideda problemos su maistu.

Dėl amerikiečių embargo ši situacija taps negrįžtama.

Visiškai aišku, kokiu būdu Rusija reaguos į bandymus užgrobti jos prekybinius laivus. Ji juos gins, dideles eksporto siuntos bus gabenamos su karo laivyno laivų konvojaus palyda.

Taip, žingsnis po žingsnio, prieis iki tiesioginio ginkluoto Rusijos ir JAV susidūrimo.

Amerikiečiai tai supranta ir todėl bijo imtis karinių sprendimų Ukrainoje. Tačiau jie supranta, kad šiame lošime labai daug pastatyta. Jei laimės Rusija, JAV visos planetos akivaizdoje taip „apsidergs“, kad tai užtemdys netgi jų buvusį gėdingą bėgimą iš Afganistano.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 5 — id: `scraped:rubaltic_lt:0d24c3b4bfe98f5b`

**Title:** NATO šalys ieško būdų blokuoti Kaliningrado sritį

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Lenkijos vyriausybė pareiškė, kad ieško „būdų ir progų“ tam, kad, apeinant Europos reglamentus, blokuoti Rusijos prekybinį susisiekimą su Europos sąjunga. Anksčiau buvo minima, kad ši veikla vyksta glaudžiai ją koordinuojant su Lietuvos vyriausybe, dėl ko pagrindiniu smūgio objektu tampa Kaliningrado sritis, kuri randasi užspausta tarp Lietuvos ir Lenkijos. NATO šalys jau surengė šio, toliausiai į vakarus nutolusio Rusijos regiono oro blokadą, dabar kalbama apie prekinę blokadą. O rytoj Lietuva gali iškelti klausimą dėl sausumos koridoriaus į Kaliningradą uždarymo.

Paskutiniu metu pabėgėliai iš Ukrainos blokuoja vilkikus su rusiškais ir baltarusiškais numeriais prie Baltarusijos – Lenkijos sienos. Dėl šių „aktyvistų“ vilkikų kamštis yra nusitęsęs keletą kilometrų.

Eiliniu reiškiniu tapo vilkikų eilė ir prie Baltarusijos - Lietuvos sienos.

Lenkijos ir Lietuvos valdžia yra patenkintos susidariusia situacija, bet vis vien šio rezultato joms atrodo nepakankama.

Apie tai neseniai pareiškė oficiali Varšuva. „Premjeras Mateušas Moraveckij ne kartą ragino tai padaryti. Bet dėl to, kad ES lygyje nėra vieningos nuomonės, mes ieškome įstatymuose kitus būdus bei progas šios veiklos apribojimui“, - pasakė Lenkijos vyriausybės atstovas spaudai Piotr Miuker apie planus uždrausti Rusijos ir Baltarusijos vilkikams įvažiuoti į Europos sąjungą.

Anksčiau buvo paskelbta, kad logistikos ryšių nutraukimo „būdų ir progų“ su Rusija ir Baltarusija paieška užsiima ir Lietuva, kartu su tuo Vilnius ir Varšuva derina vienas su kita savo veiklą.

Iš visos Sąjunginės valstybės teritorijos būtent toliausiai į vakarus nutolęs Rusijos regionas yra labiausiai pažeidžiamas ir, būtent jis taps pagrindiniu smūgio objektu.

NATO šalys de-fakto jau atvėrė Kaliningrado srities izoliavimo nuo Rusijos kelią, kai uždarė oro erdvę RF civiliam oro laivynui. Laimei, čia to beveik nepajuto, kadangi yra tiesioginis išėjimas į Baltijos jūrą, ir Rusijos oro laivai gali skristi į Kaliningradą ir iš Kaliningrado aplenkiant Baltijos šalis.

Tačiau Kaliningrado srities kaimynėms to negana, ir jos, nesislėpdamos, aptaria antrąjį etapą – prekybos-transporto blokadą.

Pirmomis dienomis po Rusijos specialios operacijos Ukrainoje pradžios Lietuvos premjerė Ingrida Šimonytė pareiškė, kad Vilnius negali sustabdyti tranzitą į Kaliningrado sritį per savo teritoriją, kadangi tai yra Europos sąjungos lygis, ir laisvas rusų keleivių judėjimas į Kaliningradą – ta sąlyga, su kuria Lietuva buvo priimta į Europos sąjungą

„Kaliningrado tranzitas yra Europos Sąjungos teisės sudėtinė dalis. Tai yra specialus ES susitarimas su Rusijos Federacija. Tikrai norėčiau, kad mes į tokius dalykus nelįstume, nes čia nėra Lietuvos sprendimas. Mes galime uždaryti Lietuvos oro erdvę, bet sprendimas dėl Kaliningrado tranzito yra jau ES sprendimas“,- tada sakė Šimonytė. Kartu su tuo dėl krovininio automobilių transporto Lenkijos ir Lietuvos valdžia, kaip jos pačios prisipažista, “ieško būdų ir progų” kaip neleisti vilkikus iš Rusijos ir Baltarusijos į Europos sąjungą ir atvirkščiai. Šiuo atveju veikia tas pats principas kaip ir su Kaliningrado tranzitu. Vilkikų pravažiavimas yra kontroliuojamas ES įstatymais ir jį reguliuoti remiantis nacionaline teise, Lenkija ir Lietuva įstodamos į Europos sąjungą atsisakė. Tačiau jos vis vien ieško būdų, kad remiantis jų pačių įstatymais būtų nutraukti pervežimai.

Truktelėti šį Rusijos spaudimo svertą – Lietuvos politikų svajonė nuo pat persitvarkymo laikų. Dar Sąjūdžio vadai laikė galimu prispausti Gorbačiovą sprendžiant Lietuvos nepriklausomybės klausimą, užblokavus geležinkelį į RTFSR Kaliningrado sritį. Ir po „nepriklausomybės atstatymo“, metas nuo meto pasirodydavo oficialių Lietuvos asmenų pareiškimai, kad Vilnius gali uždrausti tranzitą į Kaliningrado sritį.

Gali, bet to nedarys. Nors gali.

Suprantant Lietuvos politinės klasės neadekvatiškumą ir nuoširdžią neapykantą Rusijai, netgi nuostabu, kad jie iki šiol neiššovė iš šio, scenoje kabančio šautuvo. Reikalas tame, kad vyresnieji draugai iš NATO ir ES įsako savo lietuviškiems pavaldiniams sumažinti savo uolumą, atsimenant, kad tiesiogine Antrojo Pasaulinio karo priežastimi tapo tos pačios teritorijos, kurioje dabar randasi Kaliningrado sritis, teritorinis izoliavimas ir jos transporto blokada.

Na, bet nieko. Artimiausiu metu Rusija jiems tai išaiškins. Ukrainos pavyzdžiu ji įrodė, kad tokius daiktus moka aiškinti suprantamai.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 6 — id: `scraped:rubaltic_lt:5b45cd7870346e21`

**Title:** Sankcijomis į smilkinį: „ekonominis karas“ su Rusija užmušė tranzitą Lietuvoje

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Pabaltijo verslininkai apie Lietuvos, Latvijos ir Estijos tranzito ūkio šakos padėtį samprotauja apokaliptiniais posakiais. Krovinių apyvartos rodikliai, kurie daugelį metų krito, dabar pradėjo staigiai pikiruoti. Tranzitas – tai ta Pabaltijo ekonomikos ūkio šaka, kuri negali egzistuoti be Rusijos: jei pastarajai Vakaruose paskelbtas „totalinis ekonominis karas“, tai reiškia, kad Pabaltijyje užmuštas tranzitas.

„Dabar mes kiekvieną dieną netgi perkeliame eilinį valdybos posėdį, kad būtų apie ką kalbėti. Šiandieną bet kokios kalkuliacijos yra beprasmiškos! Nagrinėjame patį sunkiausią variantą: imame „visas tranzitas lygus nuliui“ ir tuo remiamės“, - sako Latvijos logistikos asociacijos valdybos pirmininkas Normund Kruminš.

Šiandieną būdingu yra posakis „tranzitas lygus nuliui“.

„Dabar atslenkanti grėsmė pervežimams, tai katastrofa“, - pasisako, pavyzdžiui, Latvijas Auto asociacijos valdybos narys Aleksandras Čerkasovas. Tą patį gali pasakyti kitų Pabaltijo transporto ūkio šakų atstovai.

Artimiausiais mėnesiais jūrų uostuose laukiamas rekordinis krovinių srauto kritimas. Taip, ekonomistai prognozuoja Latvijos Rygos uosto krovinių apyvartos griūtį beveik trečdaliu. Lietuvos Klaipėdos uoste prognozuojamas dvigubas prekių apyvartos kritimas ir ten jau prasidėjo masiškas personalo atleidimas iš darbo.

Staigiai pablogėjo ir krovinių oro transporto padėtis. Rygos oro uostas neteko daugumos tranzitinių krovinių, kurie buvo tiekiami iš Kinijos.

Ir visais, be išimties, atvejais logistinės katastrofos priežastis viena: sankcijos Rusijai.

Tranzito kroviniai iš Kinijos buvo vežami į Rygos oro uostą tolimesniam jų gabenimui į Rusiją. Per Rygą prekes vežė kompanijos-operatoriai, kuriems dabar taikomos sankcijos.

Tolimų reisų vairuotojai vilkikais negali laisvai vežti krovinius dėl ES ir konkrečiai Pabaltijo šalių taikomų apribojimų Rusijos piliečių vizoms. „Dabar Europos sąjunga paskelbė sankcijas, bet jos nelietė darbo vizų. O Latvija, viena iš nedaugelio šalių, kuri uždraudė ir jas. Tai yra, jei pas mūsų vairuotoją baigiasi vizos galiojimo terminas, mes turime jį atleisti iš darbo“, - sako Latvijas Auto asociacijos atstovas.

Pagaliau, su Pabaltijo uostais ir geležinkeliais viskas galutinai aišku. Užsienio kompanijos nutraukia tiekimą į Rusiją, kuris buvo vykdomas per Pabaltijo uostus. Vakarų vyriausybės viena paskui kitą skelbia sankcijas Rusijos firmoms, kurių produkcijos dalis iki šiol buvo eksportuojama per Pabaltijį.

Pagrindinis Estijos, Latvijos ir Lietuvos geležinkelių užsienio partneris – „Rusijos geležinkeliai“, o jam paskelbtos sankcijos. Su „Rusijos geležinkeliais“ negalima turėti jokių reikalų, jų vagonais nevalia naudotis. Kaip viso to padarinys – Pabaltijo geležinkeliai beveik negali užsiimti krovinių gabenimu.

Ir tuo netenka stebėtis, gi, Prancūzijos ekonomikos ministro žodžiais tariant, Rusijai paskelbtas „totalinis finansinis karas“. Šis karas pasireiškia visų Vakarų ekonominių ryšių nutraukimu su Rusija. O tranzitas – tai ir yra būtent ryšiai. Natūralioje, prekinėje išraiškoje.

Pabaltijyje tranzitas – tai prekių srautas iš rytų ir į rytus. Visi tuos šnekalus apie tai, kad kažkas tai gabens per jos teritoriją dideles prekių apimtis iš Suomijos į Lenkiją, jau seniai paneigė pats gyvenimas. Ši ūkio šaka Pabaltijyje nenumaldomai degradavo dėl nepertraukiamo Baltijos šalių santykių blogėjimo su savo rytų kaimynėmis – Rusija ir Baltarusija.

To „“pragariškų sankcijų“ politikos rikošeto, ne tai, kad jo niekas nepastebi – niekas jo neskaito tokiu žymiu ryškiniu, bet į kurį verta atkreipti dėmesį.

Pabaltijo politikai sako tiesiai: taip, gyventi taps blogiau, mes sutinkame su ekonominiais praradimais. Bet dėl „Rusijos sutūrėjimo“ dėl tų praradimų mes nesustosime ir netgi padarysime juos didesniais. Štai, Lietuva uždraudė Rusijos laivams įplaukti į, ir be to vargstantį be baltarusiškų krovinių, Klaipėdos uostą.

Iki šiol Pabaltijys savo kova su Rusija ir sankcijų politikos inicijavimu jos atžvilgiu šaudė sau į koją. Šiandieną jis muša mirtinai ir šauna sau į smilkinį.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 7 — id: `scraped:rubaltic_lt:b79b0940263f15c5`

**Title:** Lietuva plakasi rusofobijos konvulsijose dėl Rusijos specialios operacijos Ukrainoje

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Rygai, Vilniui ir Talinui prisieis atsakyti už jų sukeltą „antirusišką psichozę“. Apie tai pareiškė oficiali RF URM atstovė Marija Zacharova. Jos žodžiais tariant, Lietuvos sostinėje faktiškai jau prasidėjo Rusijos ambasados apgula, o vienas iš diplomatų buvo užpultas ir jo atžvilgiu buvo panaudota fizinė jėga. Toli gražu tai vienintelis pavyzdys to, kaip Pabaltijys šėlsta dėl įvykių Ukrainoje.

Šnipomanija – vienas iš ryškių antirusiškos psichozės pasireiškimų Latvijoje. Per paskutines keletą dienų čia nepagavo nei vieno FST informatoriaus, bet tai tik laiko klausimas.

„Nereikia nemanyti, kad Rusijos specialios tarnybos čia neturi savo agentų. Turi. Ir dėl to reikia būti labai atsargiais. Galvoti ką mes vienas kitam sakome. Taip, kalbėti vienas su kitu reikia, bet reikia ir galvoti, būtent ką mes sakome, kadangi jie bus pasirengę provokuoti. Kaip sakoma, įvaryti į kampą, jie gali padaryti tai, apie ką mes ir nesapnavome. Būtent tai ir reikia suprasti. Jei mes ir nesapnavome, kad Europoje yra galimas karas, tai mes manome, kad negali būti provokacijų. Gali būti“,- kalbėjo buvęs Latvijos prezidentas Valdis Zatlers.

Ką gi, jei latviams „netgi nesisapnavo“ galimi Rusijos specialiųjų tarnybų veiksmai, tai gal geriau iš viso nekalbėti. Užsinorėjai nueiti į parduotuvę apsipirkti – niekam apie tai nesakyk! Ne duok Dieve, FST agentas tuo metu įsiskverbs į tavo tuščią butą ir ant sienos nubraižys prakeiktąją raidę Z.

Valstybės policija, kartu su Nacionaline elektroninės žiniasklaidos (NEPLP) Taryba parengė Įstatymo apie apsaugotas paslaugas pataisą. Kai ji bus priimta, nelegalių sistemų panaudojimas nekomerciniais tikslais siekiant gauti audio-vaizdo paslaugas bus baudžiamas perspėjimu arba 700 eurų dydžio bauda.

„Ateityje uždraustų Latvijos teritorijoje televizijos kanalų žiūrėjimas bus labai brangus. Įstatymo dvasia prevenciška. Pradžioje bus perspėjama ir aiškinamas pažeidimas, duodant laiko jam pašalinti. Mums reikia apsaugoti mūsų žiniasklaidos erdvę“, - paaiškina Seimo deputatas, parlamento Žmogaus teisių ir visuomenės reikalų komisijos pirmininkas Artūrs Kaiminš.

Daug dirba ir Vilniaus meras Remigijus Šimašius. Jo iniciatyva bus pakeistas sostinės gatvės, kurioje randasi RF ambasados pastatas, pavadinimas. „Rusijos ambasada, pasikeiskite vizitines korteles: Ukrainos didvyrių, 2. Kiekvieno Rusijos ambasados darbuotojo vizitinė kortelė nuo šiol turės pagerbti Ukrainos didvyrius. O kiekvienas, rašantis laišką ambasadai, turės pagalvoti ir apie Rusijos agresijos aukas, ir Ukrainos didvyrius. (...) Įtariu, kad Lietuvos paštas nebūtinai pristatys laiškus, jei adresas bus nurodytas neteisingai. Vienintelis adresas Ukrainos didvyrių gatvėje bus Rusijos ambasados“, – teigė R. Šimašius.

Taip vienbalsiai nutarė sostinės Domės valdančios koalicijos partijos. Beliko tik palaukti, kada gi atsibus estai.

Dar vieną labai svarbų sprendimą priėmė Valstybinė lietuvių kalbos komisija. Prieš keletą dienų buvo įteisintas antras oficialus Ukrainos sostinės pavadinimas – Kyjivas („Кыйив“). Dabar jis bus galima naudoti kartu su tradiciniu Kijevas („Киев“). “Mes norime parodyti dar kartą Lietuvos paramą Ukrainai, įteisinti šį kalbos faktą, kuris yra subrendęs“, - pareiškia Valstybinė lietuvių kalbos komisija. Su tokia parama Ukrainos Ginkluotų pajėgų kariai tai jau tiksliai neprapuls! Sklinda kalbos, kad mūšius Kijevo srities Buši ir Irpėnia rajonuos jie pradėjo iš karto, kai tik išgirdo naujienas iš Lietuvos...

Rusijos krepšinio klubo „Parma“ gynėjas Adas Juškevičius ir vyriausiojo trenerio padėjėjas Gintaras Kadžiulis paliko komandą. Jei tikėti Sport24 portalu, tai padaryti lietuvius privertė oficialūs jų šalies atstovai, grasindami anuliuoti pasus. Pasipiktinimą keliantis įvykis, bet kam tai įdomu?

Ši šalis išdrįso ne balsuoti už JTO rezoliuciją, kuria pasmerkiama Rusijos karinė operacija Ukrainoje. Atsakydamas į tai Vilnius nepasidalino su ja ankščiau jai pažadėta vakcina Pfizer.

Jau kiek kartų Pasaulio sveikatos organizacija ir kitos „kontoros“ ragino žmones atmesti savo politinius kompleksus, kai kalbama apie kovą su koronaviruso pandemija? Kiek kupinų patoso kalbų buvo pasakytą apie būtinumą dalintis vakcinos pertekliumi su tais, kam ji reikalinga? Lietuvos valdžiai į visą tai nusispjauti - jų dirbtinis humanizmas kapituliuoja prieš neapykantą Putinui.

„Tai užims kurį tai laiką, kadangi mes tik ką užsakėme didelę siuntą. Mes jau pradėjome nuiminėti vandenį nuo lentynų, Artimiausiu metu šios prekės, jūs jau nebesurasite mūsų parduotuvėse, Suprantama, ir naujų užsakymų nebus daroma“, - praneša prekybos tinklo Selver atstovas Rivo Veski.

Pasirodo, „Boržomi“ gamybą kontroliuoja rusiška kompanija „Alfa-Group“, kuriai būk tai taikomos vakarų sankcijos. Čia pagrindinis žodis „būk tai“. Į Europos sąjungos „juoduosius sąrašus“ iš tikrųjų įtrauktas „Alfa-bankas“ ir „Alfa-Group“ bendraturčiai Michail Fridman ir Piotr Aven. Tai yra, jokių teisinių pagrindų atsisakyti užpirkti mineralinį vandenį „Boržomi“ pas estų kompanijas nėra (bent jau dabartiniu metu). Bet jie vis viena tai daro. Įdomu bus pasižiūrėti kaip į tai reaguos Gruzija, kuri tikrai tokio „smūgio iš pasalos“ nesitikėjo.

Torto papuošalas – visiškai nesenas Ukrainos Generalinės prokurorės Irinos Venediktovos pareiškimas, „Dvejos šalys jau pradėjo savo šalių baudžiamąją teiseną dėl Rusijos invazijos į mūsų valstybę. Lietuvos Generalinė prokuratūra pradėjo ikiteisminį agresijos, neteisėto, tarptautine teise uždrausto elgesio su žmonėmis ir uždraustų Rusijos karinių atakų Ukrainoje tyrimą. Lenkijos Generalinė prokuratūra tiria bylą dėl grobikiško karo pradėjimo ir jo vedimo“, - sakė Venediktova.

Bet su tokiais dalykai geriau nejuokauti. Kaip rodo tos pačios Ukrainos pavyzdys, jei ilgą laiką kviesti Rusijos gynybos ministrą, jis galų gale ateina.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 8 — id: `scraped:rubaltic_lt:d8a2955ea7c964ea`

**Title:** Vienpoliarinio pasaulio krachas: Rusija gavo tarptautinę paramą Ukrainos klausimu

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Tarptautinis specialios operacijos Ukrainoje pasmerkimas gavosi visiškai ne visuotinas, kaip to tikėjosi kovotojai už diplomatinį Rusijos izoliavimą. Maskvą vieningai smerkia tik vakarų bloko dalyviai. Dauguma ne vakarų šalių nieko nesako, o eilė stambių valstybių išreiškia savo paramą Rusijai ir atsisako prisijungti prie sankcijų. Tai Pax Ameticana – vienpoliarinio pasaulio, paremto globaliniu JAV dominavimu, krachas.

Apžvelkime pagrindinius pasaulio regionus ir pažiūrėkime, kaip ten reagavo į įvykius tolimoje Rytų Europoje.

Šiaurės Amerika. Čia viskas aišku. JAV – vienareikšmis Rusijos pasmerkimas ir sankcijos. Kanada – netgi dar stipresnis pasmerkimas ir daug skubesnės bei ryžtingesnės sankcijos negu JAV.

Šalis – kontinentas Australija. Taip pat viskas aišku. Kaip ir su Naująją Zelandija viskas aišku: vienareikšmis Putino pasmerkimas.

Lotynų Amerika. Čia jau viskas daug įdomiau.

„Ukrainos prezidentu išrinko komiką. Tauta patikėjo humoristui savo likimą“, - pasakė Brazilijos prezidentas Žajir Bolsonaru, prasidėjus Rusijos specialiai operacijai, ir pridūrė, kad „jokių sankcijų ir Putino pasmerkimo nėra“ ir šiame konflikte Brazilija renkasi neutralumo statusą.

Atsižvelgiant į atstumą nuo Brazilijos iki karo veiksmų teatro, pasisakymas apie Brazilijos neutralumą skamba kiek keistokai. Tikriausiai, omenyje turimas ne Rusijos – Ukrainos, o Rusijos – Amerikos konfliktas? Salvadoro prezidentas apie tai pasakė tiesiogiai, „JAV greitu laiku pasibaigs“,- parašė apie įvykius Naijib Bukele.

Vienareikšmiai Rusijos veiksmus pasmerkė Čilė, Kolumbija, Gvatemala, Kosta-Rika ir Urugvajus. Vienareikšmiai Rusiją parėmė Kuba, Nikaragva ir Venesuela.

Persikelsime į rytų pusrutulį. Islamo pasaulyje kol kas vienareikšmiai Rusiją pasmerkė tik Libanas, sauditai, Kuveitas ir Nepalas. Nusišalinimo nuo situacijos geografija: visa likusi Šiaurės Afrika, Irakas, Pakistanas. Rusiją ir Putiną remia Iranas ir Jemenas. Labai prieštaringai elgiasi Turkija, šalis – NATO narys!

Indija – šalis, kuri skaitoma stambiausiu JAV sąjungininku už taip vadinamo vakarų bloko ribų – nuo įvykiu vertinimo Ukrainoje susilaiko.

Įdomiausiai – Azijos – Ramiojo vandenyno regionas, kuris XXI amžiuje tampa centriniu planetos regionu. Šiame regione vienareikšmiai prieš Rusija pasisakė Japonija ir Singapūras, tarp kitko, Japonijos – šalies, kurioje dislokuotos amerikiečių karinės bazės – pasisakymas nėra toks jau griežtas ir ryžtingas, kokio galima buvo tikėtis.

„Mano požiūriu, situacijoje su Ukraina Rusija, visų pirma, imasi būtinų veiksmų nukreiptų į savo pačios valstybės suvereniteto išsaugojimą ir sustiprinimą. Antra, Rusija kaip didžioji valstybė užtikrina pasaulio jėgų pusiausvyrą, kuri leidžia palaikyti taiką visame pasaulyje, - pareiškė oficialus Mjanmo vadovybės atstovas generolas Zo Min Tun.

Mjanme manoma, kad Rusijos specialioji operacija Ukrainoje bus pirmas žingsnis, nukreiptas į tai, kad „su šaknimis sunaikinti šiuolaikinį kolonializmą ir pasaulinio žandaro viešpatavimo politiką“.

Tai labai paplitęs Rusijos rėmimo motyvas.

Prie istorinio revanšizmo verta prijungti atvirą Serbijos piktdžiugiškumą, dėl kurio netgi europietiška vienybė jau neatrodo absoliučia. Dar gi: dabar rusai su amerikiečių marijonietėmis Ukrainoje daro tą patį, ką 1999 metais NATO darė su serbais!

Visas šias dienas sklinda atkaklios kalbos, kad JAV šantažuoja Kiniją Taivano pripažinimu, jei dėl Ukrainos Pekinas nepareikš savo principinę antirusišką poziciją. Jei tai taip, jokio rezultato nesimato.

Oficialūs Kinijos atstovai mano pagristu Rusijos susirūpinimą savo saugumu iš vakarų šalies, o tikra grėsme planetai vadina Jungtines Amerikos Valstijas.

Ir koks rezultatas? Iš 193 šalių, turinčių tarptautinį pražinimą – JTO narių, Rusijos veiksmus pasmerkė kažkur tai apie 60. Tai yra mažuma. Pagrinde tai JAV sąjungininkai NATO nariai ir šalys ne NATO narės.

Dar kartą: jų mažuma.

Tai vadinasi vienpoliarinio pasaulio krachas: Jungtinių Valstijų, pagal kurios dūdelę šokdinama visa žmonija, globalinio dominavimo jau nebeliko.

Šis faktas jau tapo pasaulinės istorijos dalimi.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 9 — id: `scraped:rubaltic_lt:c789f7e216e11e81`

**Title:** Po Ukrainos bus Pabaltijys Lietuva žengė pirmąjį žingsnį link Kaliningrado blokados

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Pažvelkime tiesai į akis: Ukraina reikalas nesibaigs, bet tik prasidės. Baltijos šalys, kurių „gynybai“ į Pabaltijį jau daugelį metų įveža puolamąją (!) ginkluotę, ir NATO kontingentas, kurį, karinio Maskvos spaudimo prasme nuspręsta daug kartų padidinti, niekuo nesiskiria nuo Ukrainos. Koks skirtumas, kur bus dislokuotos raketos su branduoliniais užtaisais: greta Charkovo ar greta Talino? Pabaltijį sparčiai gena Ukrainos keliu, ir jo ateitis – sakralinės aukos dalia, kuri bus paaukota dėl amerikietiško globalinio dominavimo ir Rusijos sunaikinimo.

Nuo kurio tai laiko aš ne laisvas menininkas, o vadovas, kuris yra atsakingas už normalų dešimčių žmonių gyvenimą. Daugelis iš jų gyvena už Rusijos ribų, kai kurie – Donbase, beveik fronto linijoje. Iš pradžių nepasirūpinęs apie tai, kad artimiausiam metui paremti savo bendradarbius, aš nejaučiau nei teisės, nei noro pasisakyti apie vykstančius įvykius. Dabar galiu įvykdyti šią savanorišką pareigą.

Visą savo sąmoningą gyvenimą aš laikausi vienos labai paprastos taisyklės: bet kokioje situacijoje reikia būti su savo šalimi. Jei tu prieš savo šalį, nelauk, kad ji tave gins, nesitikėk jos pagalbos, neimk iš jos pinigų ir, galų gale, nedirbk jos labui. Daugelis mūsų sąjungininkų iš naujų darinių palei RF vakarų sieną taip ir daro.

Visgi, kas nori gyventi Rusijoje, greta Rusijos, ir iš viso gyventi, turi suprasti vieną paprastą dalyką.

Rusija kariauja ne su Ukraina, o su Jungtinėmis Valstijomis ir jos tarnais. Ukraina – teritorija. Lygiai prieš aštuonerius metus Maidane ją išlošė vakarai ir visą laiką po to jos teritorijoje rengė slaptas, skirtas Rusijos užpuolimui, NATO bazes. Dar 10 metų „derybų Normandijos formate“ ir tas užpuolimas taptų realybe.

Šiandiena tarptautinė konjunktūra visais galimais aspektais – nuo energijos šaltinių atsistatančiajai po pandemijos pasaulio ekonomikai iki JAV vidaus politines situacijos - palanki tam, kad Rusija sustabdytų tą procesą Visi tie, kurie to nepastebi – arba kvailiai, arba priešai. Nei su tais, nei su kitais nėra prasmės kalbėti.

Todėl sekantis Rusijos ir JAV derybų dėl strateginio saugumo raundas – tai derybos dėl NATO Pabaltijyje. Jei šios derybos bus tokios pat kaip ir buvusios, tada Pabaltijo šalis laukia Ukrainos likimas. Ir yra didelė tikimybė, kad taip ir atsitiks.

Jungtinėms Valstijoms paaukoti šias šalis taip pat naudinga, kaip joms dabar naudinga, kad Rusija ilgam įklimptų Ukrainos laukuose. Kad būtų pralieta kuo daugiau kraujo. Tame tarpe ir ukrainietiško.

Šiuo atžvilgiu ypatingai svarbi Kaliningrado sritis. Ji yra pats pažeidžiamiausias Rusijos saugumo sistemos elementas, ir jau prasidėjo šio Achilo kulno spaudimas. Kas mėnesį didės bendro masto blokados tikimybė.

Viltį duoda tai, kad Rusijos valdžia visus tuos metus puikiai suprato, kas randasi Lenkijos ir Lietuvos valdžioje, ir kas jiems įsakinėja. Ne be reikalo visą tą laiką Kaliningrado srityje buvo statomos elektrinės, investuojama į žemės ūkį, buvo įvežti „Iskanderai“ ir SGD terminalas.

Strateginė regiono autonomija ir saugumas ant tiek užtikrintas, kad tai leidžia galvoti apie žmonių gyvenimo lygio išsaugojimą, o ne apie jų apsaugojimą nuo bado bei bombardavimo. Kaliningradiečiai neturi mokėti daugiau už aviacijos maršruto į Rusiją pailgėjimą. Jų skrydžių bilietų kainą turi subsidijuoti valstybė ir ta kaina turi būti žemesnė už geležinkelio bilieto kainą. Šiuo klausimu užsiiminėsiu aš, kaip Kaliningrado srities Visuomenės rūmų narys.

Skaitytojams iš Pabaltijo pasakysiu vieną.

Sakyti jums apie tai neleidžiama - RuBaltic.Ru portalas, pavyzdžiui, paskutinėmis dienomis yra nepertraukiamai atakuojamas DDoS, o Facebook jau daugelį metų mus be pertraukos „dergia“.

Jei jūs visgi galėsite perskaityti šį tekstą, pagalvokite apie tai ką aš sakau. Galvojančio atsakingo žmogaus pasirinkimas dabar – bėgti iš Pabaltijo arba kovoti už tai, kad jis nebūtu įmesta į „Rusijos sutūrėjimo“ pakurą. Bet tik neremti vietinių valdančiųjų marijoniečių mekenimo apie tai, kad reikia daugiau NATO, jokių derybų su Rusija ir Amerika už jus kariaus

P.S. Rusijos operacijos Ukrainoje pradžios dieną pakartotinai buvo pradėtas demonstruoti Francis Ford Coppola filmas „Krikštatėvis“. Po dabartinės jo peržiūros didžiajame ekrane, aš supratau, kad visą šį laiką man nebuvo suprantama vieno iš geriausių istorijoje filmų esmė. Todėl nesupratau jo devizo „valdžia negali būti duota, ji gali būti paimta“. Jis atrodė per daug pretenzinis, beprasmiškas ir tuščias tų filmo citatų fone, kurios tapo priežodžiais visomis pasaulio kalbomis. Vykstančių įvykių fone man tapo suprantamas šis devizas. „Krikštatėvis“ – tai kino juosta apie tai, kad norint atremti daug stipresnio priešo smūgį, kuris siekia nužudyti tavo artimuosius, tenka imtis nekonvencinių, radikalių, nepaprastų priemonių. Ir taip pasiekiamos valdžia ir pergalė.

Šiandieną Rusiją įtraukė situacijon, kai reikia imtis nekonvencinių, radikalių, nepaprastų priemonių. Kitaip, kelių metų perspektyvoje ją sunaikins. Todėl Rusiją iš kenčiančios šalies tampa šalimi nugalėtoja, kuri pati sunaikins visus tuos, kurie ruošėsi ją sunaikinti.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 10 — id: `scraped:rubaltic_lt:d0d06c3f8c9f4c6e`

**Title:** „Who is mister Putin“: Vakarai patys sau išrinko Rusijos prezidentą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Kas toks misteris Putinas? Šis klausimas pirmą kartą buvo užduotas 2000 metų sausio mėnesį Davoso forume. Vadovaujamos Anatolijaus Čiubaiso Rusijos delegacijos nariai sutriko, salėje pasigirdo kikenimas. Niekas nežinojo, „who is mister Putin“? Atsakymo prisiėjo laukti ilgiau nei du dešimtmečius, Visą tą laiką Rusijos prezidentas stovėjo kryžkelėje, akivaizdžiai norėdamas žengti vienu keliu, o ji atkakliai stūmė į kitą kelią.

Rusijos karinės operacijos Ukrainoje pradžia iškelia aštrų, nemalonų, dalinai netgi baisų klausimą, kuri negalima neskaityti kardinaliu: nejaugi mes suklydome? „Mes“ reikia skaityti visu tuos, kurie paskutinius keletą metų iki valios prisijuokė iš Rusiškos invazijos grėsmės. Tuos, kurie neigė pačią RF ir Ukrainos karinių pajėgų konflikto tikimybę.

Ir ne tik neigė! Mes gi pateikėme begalę „gelžbetoninių“ argumentų, kad tokio scenarijaus galimybė lygi nuliui. Nejaugi teisūs tapome ne mes, o jie, kurie iki užkimimo šaukė apie imperines Putino ambicijas bei jo siekį išspręsti Ukrainos klausimą jėgos pagalba. Nejaugi Ukrainos karinės pajėgos panaudojo išgarsėjusius „Dževelinus“ ir „Stingerius“, kurie, mūsų požiūriu, turėjo dulkėti kažkur tai sandėliuose toli nuo Donbaso? Nejaugi britaniškas laikraštukas The Sun nemelavo savo skaitytojams, pasakodamas apie neišvengiamą invaziją? Apsiriko tik keliomis dienomis...

Mūsų realybė žūsta nuo rusiškų sparnuotų raketų smūgių, mūsų argumentus slopina šturmuojančios aviacijos ūžesys Kijevo padangėje. Pasimetę mes bandome „suvirškinti“ naujienas, kurios neatitinka mūsų pasaulio įvaizdžio.

Pageidaujamą mes skaitėme tikrove? Galų gale galiu pasakyti apie save: aš ieškojau galimus Ukrainos krizės sprendimo variantus išimtinai diplomatijos plotmėje. Kiti variantai atrodėsi nerealiais. O Putinas atrodė politiku, kuris iki savo valdymo pabaigos stengsis nedaryti per daug staigių judesių. Sukalbamas, nuolaidus Putinas – europietiško tipo prezidentas.

Ne atsitiktinai, neseniai, savo kreipimesi į Rusijos gyventojus (kuris, žinoma, buvo adresuojamas kaimyninės šalies tautai) Putinas prisiminė savo 2000 metų pokalbį su Bilu Klintonu. Tada Rusijos įstojimo į NATO perspektyva rodėsi ne tokia jau fantastiška.

Savo pirmąją prezidento kadenciją Kremliaus šeimininkas pradėjo laikydamasis politiko, kuris yra nusiteikęs sąjunginiams santykiams su Vakarais, pozicijos. „Nulinių“ metų pradžios Putinas vienas iš pirmųjų sureagavo į rugsėjo 11 d. tragediją, pareikšdamas pasirengimą paremti JAV kovos su pasauliniu terorizmu pastangas. „Nulinių“ metų pavyzdžio Putinas buvo populiarus Vakaruose, palaikė gerus santykius su didžia Europos lyderių dalimi, ir nerodė „revanšistinių“ užmojų. Jis nulenkė galvą prieš Katynės tragedijos aukas, vienareikšmiai vertino Stalino epochos nusikaltimus.

Vakarų partnerių požiūriu jo problemos esmė buvo viename: jie nenorėjo būti nugalėtos šalies, su kuria galima elgtis gyvuliškai, lyderiu.

Pašaipos baigėsi seniai. Bet kokiu atveju, 2014 metais, kai Kremliaus šeimininką paskelbė beveik priešu visam „civilizuotam“ pasauliui. Tame ir reikalas, kad „beveik“. Turėdamas visas galimybes nušalinti jam nepageidaujamą (kartu su tuo absoliučiai neteisėtą) Kijevo režimą, Putinas to nepadarė. Maskvai tarpininkaujant buvo sudaryti, pradžioje pirmieji, po to antrieji Minsko susitarimai, kurie leido Ukrainoje atstatyti politinių jėgų pusiausvyrą, suteikiant atskiriems Donecko ir Luhansko liaudies respublikų rajonams ypatingą statusą. Bendrai paėmus, buvo kalbama apie taikų šalies sugrįžimą į „iki maidaninį“ stovį.

Ilgus aštuonerius metus Vakarai nebuvo vieningi vertindami Rusijos prezidentą. Nebuvo jokio pagrindo prikabinti jam „naujojo Hitlerio“ etiketę. Koks čia Hitleris, kuris yra tolerantiškai nusiteikęs greta jo pašonėje esančios atvirai priešiškos valstybės atžvilgiu? Pas kokį Hitlerį netgi artimiausias sąjungininkas (šiuo atveju Baltarusija) laikosi daugiavektorinio kurso ir leidžia sau tai, ko niekada sau neleis amerikiečių pakalikai Rytų Europoje? Kur jūs matėte Hitlerį, kuris nuolankiai vykdo Stokholmo arbitražo sprendimus ir niekada nepažeidžia savo dujų tiekimo Europai įsipareigojimų? Kodėl per visą laiką „rusiškų žemių vienytojas“ prie Rusijos prijungė tik mažytį pusiasalį?

Kažkas tai trukdė prikabinti gėdingą etiketę Kremliaus šeimininkui. Bet Vakarai planingai siekė savo, įvarydami Rusiją į „imperijos“ stovį. Šiame reikale Ukrainai buvo skirtas ypatingas vaidmuo.

Dabar galima ir atsikvėpti. Buvusio Putino, nesuprantamo ir nevienareikšmio, daugiau neegzistuoją. Į pasaulį atėjo Rusijos prezidentas, kurio taip ilgai laukė JAV ir Europa.

„Putinas bus pasmerktas pasaulio ir istorijos akyse. Jis niekada negalės nuplauti nuo savo rankų Ukrainos kraują, ir nors Didžioji Britanija ir mūsų sąjungininkai iki pat galo taikė visas diplomatijos galimybes, aš darau išvada, kad Putinas visada buvo pasiryžęs užpulti savo kaimynę, nepriklausomai nuo to, ką mes darėme. Dabar mes jį matome tokį, koks jis yra – krauju susitepusį agresorių, tikinčiu imperiškais užkariavimais“, - džiūgauja Didžiosios Britanijos premjeras Boris Džonsonas.

Neturiu jokio noro prieštarauti ir kometuoti šį pasisakymą.

Iš dviejų Putinų jūs sąmoningai išsirinkote tą, kurio norėjote. Jūsų reikalas....

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 11 — id: `scraped:rubaltic_lt:711dceaf00f4b016`

**Title:** Persilaužimas ekonominiame kare: Sankcijos Rusijai nustojo veikti

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Rublio kursas ir stambiausių Rusijos kompanijų akcijos staigiai paaugo, JAV ir Europos sąjungai įvedus naujas sankcijas Rusijai. Sankcijos už tai, kad Maskva pripažino Donecko ir Luhansko liaudies respublikų nepriklausomybę yra pernelyg švelnios, ir patys europiečiai bei amerikiečiai pripažįsta, kad griežtesnių sankcijų Rusijai jie jau nebegali įvesti, kadangi tokios sankcijos skausmingai atsilieps patiems Vakarams.

Bendras JAV prezidento paskelbtų ir Europos komisijos parengtų sankcijų sąrašas yra sekantis:

1. Sankcijos keliems rusiškiems bankams ;

2. Sankcijos Rusijos valstybiniam įsiskolinimui: operacijų su Rusijos vertybiniais popieriais uždraudimas ;

3. Dujotiekio „Šiaurinis srautas-2“ sertifikavimo sustabdymas »;

4. Sankcijos Rusų valdininkams ir deputatams, parėmusiems Donbaso respublikų nepriklausomybę: draudimas įvažiuoti ir jų aktyvų užsienyje blokavimas.

Per kelias valandas po Džozefo Baideno Vašingtone ir Žozepo Borrelio Briuselyje pasisakymų dolerio ir euro kursai rublio atžvilgiu krito, atitinkamai 1,2% ir 1,24%. “Gazpromo” akcijos, po to, kai jo projektui „Šiaurinis srautas-2“ „buvo padaryta pauzė”, išaugo 4,2%.

Tokios rinkos reakcijos į sankcijas dar nebuvo. Ir ne tik rinkos. Rusijos visuomenė į naujas sankcijas reagavo... juoku. Juoko pagrindu tapo Europos diplomatijos vadovas Žozepas Barrelis, kuris parašė, kad rusų „oliharkams“ daugiau neteks apsipirkti Milane, nebus vakarėlių San-Trope ir deimantų Antverpene. Galima tik įsivaizduoti, kokį įspūdį rusiškai auditorijai sukėlė tokia „baisi“ bausmė: Rusijos deputatai (tik pagalvokite!) nebegalės daugiau pirkti deimantus Antverpene!

Ir pačiam didžiausiam linksmumui betrūko tik to, kad Žozepas Borrelis pašalintų savo paskyrą apie deimantus. Būtent taip jis ir padarė.

Jei kalbėti rimtai, oficialūs asmenys Europoje ir JAV dabar įtikinės visus, kad Rusijai įvestos „švelnios“ sankcijos – tai tik pirmasis paketas, o tikrosios „pragariškos sankcijos“ dar bus.

„Rusijos vyriausybė metai iš metų pertvarkinėjo biudžetą ir finansus, kad šalies ekonomika galėtų pasipriešinti būsimoms sankcijoms. Vyriausybės pastangos buvo remiamos aukštomis naftos ir dujų rinkos kainomis. Dabar Rusijos išorės skola yra palyginimai nedidelė, ir ji yra mažiau priklausoma nuo kreditorių, nuo užsienio organizacijų, negu tai buvo 2014 metais. Ir, kas ypatingai svarbu, šalies valiutinį rezervą sudaro 631 milijardas dolerių. O tai – ketvirtas pagal dydį valiutinis rezervas pasaulyje“, - apie naujas sankcijas rašo New York Times.

Vienintelėmis jautriomis sankcijomis, kurios gali rimtai pakirsti ekonominę putiniškos Rusijos bazę – tai draudimas tiekti rusišką naftą ir dujas. Tačiau New York Times ekspertai vieningi savo išvadose: vakarų politikai to niekada nepadarys. Kadangi tokios sankcijos iš tikrųjų skausmingai atsilieps ir Vakarams.

New York Times ekspertų išvadas gyvenimas jau patvirtino. Po sprendimo sustabdyti „Šiaurinio srauto – 2“ sertifikavimą, dujų kainos Europoje šoko aukštyn.

Tokiame pat lygyje naujų Vakarų sankcijų bumerango efektas yra aktualus ir kitoms „pragariškoms sankcijoms“, kuriomis paskutiniais metais grasinama Rusijai. Atjungimas nuo pervedimų tinklo SWIFT, transporto blokada, technologinės kooperacijos grandinių nutraukimas – tai visos sankcijos, kurioms, visų pirma, Rusija jau daugelį metų ruošėsi, antra, tai sankcijos, kurios kirs ir tuos, kurie jas įveda.

Todėl situacija, kai iš vakarų valdininkų įvedamų sankcijų juokiamasi, o, paskelbus naują sankcijų pakėtą, rublis auga, tai ne sistemos sutrikimas. Ekonominėje kovoje pasiektas persilaužimas, ir panašios situacijos bus atkuriamos.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 12 — id: `scraped:rubaltic_lt:fe08d29b69c96a9f`

**Title:** Ukrainą paversime Afganistanu: Lietuva siunta dėl Putino sprendimo apie Donbasą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Naujiena, kad RF prezidentas Vladimiras Putinas pripažino Donecko ir Luhansko liaudies respublikų nepriklausomybę, Pabaltijyje sukėlė sąmyšį.

Lietuvos Latvijos ir Estijos atstovai reikalauja Europos sąjungos įvesti pačias griežčiausias sankcijas Rusijai ir net gi grasina jai karu. Toliau visų, veikiausiai, nužengė Lietuvos Seimo nacionalinio saugumo ir gynybos komiteto pirmininkas Laurynas Kasčiūnas: jis gailisi, kad ES it NATO per praėjusius aštuonerius metus nepavertė Ukrainos antruoju Afganistanu.

„Rusijos Federacijos prezidento sprendimas pripažinti Ukrainos nekontroliuojamas Luhansko ir Donecko teritorijas tęsia, dar 2014 metais prasidėjusią, Ukrainos suvereniteto ir teritorijos vientisumo ataką, numatant neteisėtą sienų perbraižymą Europoje. Šiurkščiai pažeisdama tarptautinę teisę, prisidengdama sufabrikuota priežastimi ir platindama melagingą informaciją, Rusija siekia išprovokuoti Ukrainos politinės vadovybės ir užsienio politikos kurso pakeitimą per prievartą“. – sakoma pareiškime, kurį pasirašė Latvijos prezidentas Egils Levits, Seimo pirmininkė Inara Murniecė, premjeras Krišjans Karinš ir užsienio reikalų ministras Edgar Rinkėvič.

Protesto notą jie paruošė iš anksto (tikriausiai, dar kai posėdžiavo RF Saugumo komitetas, kai paaiškėjo, kad Putinas yra nusiteikęs pripažinti DLR ir LLR).

Kaimynai nutarė neatsilikti. Istorinę Putino kalbą Lietuvos užsienio reikalų ministras Gabrielius Landsbergis komentavo sekančiai: „Rusija turi būti pripažinta tokia, kokia ji yra: valstybė už tarptautinių taisyklių ir civilizuotų normų ribų. Toks eskalacinis elgesys turėtų sulaukti sankcijų“.

Estijos URM vadovas priduria, kad DLR ir LLR pripažinimas yra „aiškiu Minsko susitarimų pažeidimu ir iškvies vienašališką susitarimų nutraukimą“.

Į iš Pabaltijo girdimų šabloniškų pareiškimų srautą papuldavo ir kai kurie konkretūs pasiūlymai. Taip, pavyzdžiui buvusi Estijos ambasadorė Rusijoje Marina Kaljurand ragino atjungti Rusiją nuo SWIFT ir galutinai sustabdyti „Šiaurinį srautą – 2“. Taip, tai bus smūgis ir ES ir Estijai. Bet, galų gale, būtina užtikrinti Europos sąjungos energetinę nepriklausomybę nuo Rusijos“, - mano Kaljurand.

Paskutiniųjų įvykių kontekste tezė apie ES „energetinės nepriklausomybės“ įsigijimą blokuojant „Šiaurinį srautą – 2“, skamba kaip iš konteksto išplėšta frazė.

Estijos prezidentas Alar Karis taip remia Ukrainą, kad ją aplankė sekančią dieną po to kai Putinas pripažino Donbaso respublikas. „Kremliaus sprendimas pripažinti Ukrainos rytuose esančius separatistų regionus kaip atskiras valstybes, dar labiau pagilina dabartinę saugumo krizę Europoje ir aiškiai rodo, kad Maskva atsisakė diplomatijos ir pasirinko agresiją, mes turime skubiai ir vienbalsiai įvesti naujas ir efektyvias sankcijas Rusijai“.

Vėl gi, čia svarbu kontekstas. Prieš septynerius metus buvo pasirašyti, taip vadinami antrieji Minsko susitarimai, kurių vykdymą metai iš metų sabotavo Ukraina, ir to visiškai neslėpė. O kalbama apie pagrindinį taikos ir saugumo užtikrinimo Rytų Europoje dokumentą. Per septynerius metus nei vienas Europos lyderis nepriekaištavo Ukrainai už tai, kad ji provokuoja krizės gilėjimą.

Tik dabar atsipeikėjo.

Reikėtų prisiminti paskutinį „Normandijos ketverto“ susitikimą Paryžiuje, kai Rusija siūlė atitraukti pajėgas išilgai visos atsiribojimo linijos Donbase. Tai buvo vienintelis efektyvus būdas nutraukti kraujo praliejimą ir nors ir dalinai išspręsti problemas. Bet ir čia Kijevas atsisakė Maskvos pasiūlymo. Tuometinis Ukrainos vidaus reikalų ministras Arsenas Avakovas pasakė tiesiai, kad jo šaliai tai yra visiškai nenaudinga.

Atskiri Pabaltijo politikai netgi neslepia, kad jie taip pat veikė šia kryptimi. Kol Lietuvos prezidentas tvirtina apie Rusijos padarytus tarptautinės teisės pažeidimus, Lietuvos Seimo nacionalinio saugumo ir gynybos komiteto pirmininkas Laurynas Kasčiūnas priekaištauja kolektyviniams vakarams: „Nenorėjo priimti Kijevą į Šiaurės Atlanto bloką – gerai, nepriimkite. Be prisotinti šiuolaikine priešraketine, prieštankine ginkluote, priešlėktuvinės gynybos priemonėmis ir karo laivais tiesiog privalote.(...) Mes galėjome Ukraina paversti antruoju Afganistanu. Ukrainiečiai galėjo Rusijai tapti tokiais pat modžahedais, kokiais jie buvo SSSR armijai“.

Kokiu būdu į šią koncepciją įsiterpia Minsko susitarimai? Niekaip. Kasčiūnas netgi neprisimena, kad Kijevas turėjo konkrečius taikos įtvirtinimo Donbase įsipareigojimus. Pasirodo, kad vietoje konflikto sureguliavimo, Ukrainos teritorijoje reikėjo sukurti didelį nestabilumo židinį, į kurį įklimps Rusija.

„Mūsų atsakymas turi būti toks: „Brangus mūsų drauge, mes esame taikus aljansas, bet mes esame pasirengę eiti į kovą už mūsų laisves. Mes jūsų nebijome. Jei jūs norite karo, jūs jį gausite“,- kalba Latvijos gynybos ministras Artis Pabriks. Anksčiau jis pats neigė latviško karinio kontingento pasiuntimo į Ukrainą galimybę. Tikriausiai, už „jų laisves“ turi kovoti išskirtinai tie žmonės, kuriuos ponas Kasčiūnas mato kaip naujus modžahedus.

O Pabaltijo elitui situacija vystosi kaip niekada gerai.

Donbaso respublikų pripažinimas Rusijoje – tai Lietuvos, Latvijos ir Estijos valdžių politikos apogėjus. Tiesiog dabar auga jų pagrindinės eksporto prekės – rusofobijos kaina.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 13 — id: `scraped:rubaltic_lt:f13804975de4cc0f`

**Title:** Baisus Lietuvos sapnas išsipildė: Rusijos karinės pajėgos pasiliks Baltarusijoje

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Rusijos karinės pajėgos pasiliks Baltarusijos teritorijoje, Rusijos – Baltarusijos karinės pratybos „Sąjunginis ryžtas – 2022“ bus tęsiamos. Šią informaciją patvirtino Baltarusijos Respublikos Generalinis štabas, kuris tokį sprendimą paaiškina įtempta geopolitine situacija regione. Lenkijos ir Pabaltijo šalių įprotis bet kokioje situacijoje remti Rusijos ir Vakarų santykių paaštrėjimą, padarė taip, kad jų ilgametis košmaras tapo realybe: Rusijos tankai po pratybų Baltarusijos teritorijoje pasiliks NATO rytų pasienyje.

„Augant kariniam aktyvumui greta Sąjunginės valstybės išorės sienų ir paaštrėjus situacijai Donbase: Baltarusijos Respublikos ir Rusijos Federacijos prezidentai nusprendė pratęsti Sąjunginės valstybės reagavimo pajėgų parengties patikrinimą.“, - vasario 21 d. ryte pranešė Baltarusijos Respublikos Generalinio štabo viršininkas, generolas – majoras Viktoras Gulėvičius.

„Pajėgos ir priemonės, kurios buvo dislokuotos Rytų Europos regione, tame tarpe greta Baltarusijos Respublikos valstybės sienos, yra vienas iš faktorių, kurie įtakoja tolimesnei situacijos raidai“, - kalba Gulėvičius. – „Baltarusijos Respublika turi teisę reikalauti atitraukti nuo Baltarusijos Respublikos ir Sąjunginės valstybės sienos JAV karinių pajėgų bei atskirų šalių – NATO narių sudarytas grupuotes, ir užtikrinti karinių pajėgų išvedimo verifikaciją“.

Pažymėtina, kad kalbama išskirtinai apie Baltarusijos užsienio ir gynybos politiką. No pat pradžių ir iki šios dienos.

Minskas buvo karinių pratybų „Sąjunginis ryžtas – 2022“ ir Rusijos karinių pajėgų įvedimo į Baltarusijos teritoriją iniciatoriumi. Dabar gi Minskas skelbia, kad manevrai bus tęsiami ir Rusijos pajėgus liks Baltarusijos teritorijoje. Ir vėl gi, Minskas sukelia karinių – politinių blokų susidūrimo grėsmę, kaip tokio sprendimo pagrindą: galutine prieškarinės situacijos Rytų Europoje priežastimi vadina NATO plėtrą į rytus.

Maskva šią situaciją iš viso nekomentuoja. Tikriausiai, kad neapkaltintu „Baltarusijos „okupavimu“.

„Baltarusija leidžia Rusijai panaudoti savo teritoriją kariniams veiksmams, tiksliai taip pat mes turime kalbėti apie sankcijas Baltarusiškam režimui“, - sakė Lietuvos užsienio reikalų ministras Gabrielius Landsbergis.

Tarp kitko, apie „Rusijos okupavimą Baltarusiją“ Landsbergis taip pat pasakė. Vienas kita neigiantys pasisakymai, bet kurgi profesionaliems Pabaltijo rusofobams be „okupavimo“. „Esame priversti pripažinti, kad tai, ką mes matome, - tai labai lėtas Baltarusijos teritorijos ir valstybės okupavimas“, - pasakė Lietuvos URM vadovas.

Tarp kitko nurodytos šalys savo baisų sapną pačios pavertė realybe. Nuo įstojimo į NATO laikų visa jų tarptautinė politika buvo nukreipta į Rusijos ir Vakarų santykių paaštrinimą.

Šios šalys savo „nepalenkiama pozicija“ padarė beveik neįmanomu sureguliuoti tuos fundamentalius prieštaravimus, kurie Rytų Europoje susikaupė tarp Rusijos ir Vakarų, diplomatijos ir derybų būdu. Jie tapo Vakarų tradicijos sureguliuoti klausimus su Maskva diplomatijos ir derybų būdu griovimo instrumentu.

Tokio požiūrio rezultatu tapo NATO plėtra į Rytus ir amerikietiškų tankų atsiradimas greta Sankt-Peterburgo ir Kaliningrado.

Tokiu būdu, ir pas juos neapibrėžtą laiko tarpą rusiški tankai stovės greta Vilniaus.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 14 — id: `scraped:rubaltic_lt:306154e7190ba783`

**Title:** Putinas nesustos: Vakarai išrinko Pabaltijį nauja „Rusijos agresijos“ auka

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Pabaltijys gali tapti nauju RF prezidento Vladimiro Putino taikiniu, jei Vakarai neužkirs kelią „rusiškai invazijai“ į Ukrainą. Apie tai pareiškė Didžiosios Britanijos URM vadovė Liz Trass. Anksčiau analogišką prognozę pagarsino savo skandalais žinomas bulvarinis leidinys The Sun, o JAV išreiškia savo pasirengimą prikgrūsti Pabaltijį letalia ginkluote. Vakarų politikų ir žurnalistų pareiškimų dėka Pabaltijys virsta nauju „karštu tašku“ Europos žemėlapyje.

Pavojinga situacija Donbase ir bendrų Rusijos ir Baltarusijos karinių pratybų tęsinys aidu atsiliepia Lietuvoje, Latvijoje ir Estijoje, kurios rytiniame NATO sparne pačios sau priskiria priešakinio forposto vaidmenį.

„Atsakant į Ukrainos okupavimą, stiprinti Pabaltijį“, - tokią nesudėtingą formulę pagarsino JAV prezidentas Džozefas Baidenas. Įvairiuose interpretacijose ją pakartojo  ir kiti vakarų politikai. Kadangi „rusiškos invazijos“ grėsmė nemažėja, Pabaltijiečiai užduoda logišką klausimą: kada gi pradės juos „stiprinti“?

Apie tai Lietuvos, Latvijos ir Estijos prezidentai pasidomėjo pas JAV viceprezidentę Kamalą Harris, kuri su jais diskutavo Miuncheno saugumo konferencijos pakraščiuose.

„Buvo pasakyta, kad šiuo metu kaip tik svarstomas klausimas dėl Baltijos šalių sustiprinimo, kadangi tos grėsmės, kurios yra dabar, jos reikalauja atsako tiek NATO formatu, tiek mūsų sąjungininkų, pirmiausia JAV. Manau, kad jie dabar yra procese ir netrukus turėtų būti tam tikri sprendimai“, – pasakė Lietuvos lyderis Gitanas Nausėda.

Nieko konkretaus apie Baltijos šalių karinio potencialo sustiprinimą žurnalistai iš jo neišgirdo (išskyrus tezę apie tai, kad esant būtinybei, amerikiečiai yra pasirengę į Rytų Europą atsiųsti papildomą karinį kontingentą). Pentagono vadovas daugiau kalbėjo apie Ukrainą. Kartu su tuo įsigudrino susipainioti savo pasisakymuose.

Ostino žodžiais tariant, Rusijos kariuomenė „šiuo metu randasi pasirengimo smūgiuoti Ukrainai pozicijose“. Po to tas pats Ostinas sako, kad „Kremliaus pajėgos vis arčiau sėlina link Ukrainos sienų“. Tai jos jau randasi pozicijoje, ar dar ne? Jei ne, tai kame jų tokio nevikrumo priežastys? Pirmieji pranešimai apie rusišką „blickrigą“ pasirodė dar prieš trejus mėnesiui.

Bet kokiu atveju, Ostinas užtikrino Jungtinių Valstijų paramą Pabaltijui.

Vilniui tai pasirodė mažai. „Mes turime rimtai pažvelgti ne į suturėjimą, o į gynybą. Mes turime būti pasirengę ginti Baltijos šalis ir Lenkiją“, - kalbėjo Lietuvos URM vadovas Gabrielius Landsbergis bendros spaudos konferencijos su LLoid Ostinu metu.

Dar konkrečiau pasisakė Pabaltijo valstybės premjerė Ingrida Šimonytė: „[Jungtinių Valstijų ] gynybos ministrui aš išreiškiau Lietuvos pasirengimą priimti daugiau JAV kariškių, jei bus toks administracijos sprendimas“. Užuomina aiški: Baltijos šalys jau dabar pageidauja, kad regione pastoviai būtų dislokuoti amerikiečiai. Kitu atveju atsitiks bėda.

Įtampą didina ir gynybos žinybų vadovybė. Lietuvos ministras Arvydas Anušauskas ragina skirti papildomus resursus kariuomenės modernizavimui ir perginklavimui, jo kolega iš Latvijos Artis Pabriks kalba apie pirmųjų preventyvinių sankcijų įvedimą Rusijai. Estijos gynybos ministras Kalle Laanetas prašo amerikiečių atsiusti į jo šalį naikintuvų.

Ypatingai pasižymėjo Britų bulvarinis laikraštis The Sun (tas pats, kuris vasario 16 paskelbė „Rusijos invazijos“ į Ukrainą data). Pagal jo versiją, po sėkmingo vienos postsovietinės respublikos užgrobimo Putinas gali ant tiek išdrąsėti, kad pasigodės  Lietuva, Latvija ir Estija. Invazija bus vykdoma „Hitlerio stiliumi“. „Tai kaip Hitleris: duosite pirštą, jis atkąs ir ranką“ –laikraštėlyje The Sun komentuoja buvęs NATO atstovas Maskvoje Harry Tabaks.

Praėjus kelioms dienoms po šios publikacijos, apie „rusiškos invazijos“ grėsmę Pabaltijyje prakalbo Didžiosios Britanijos URM vadovė Liz Trass: „Baltijos šalys pavojuje... Vakarų Balkanai taip pat. Putinas viešai buvo pareiškęs, kad nori sukurti didžiąją Rusiją, kad jis nori grįžti prie situacijos, kuri buvo anksčiau, kai Rusija kontroliavo didžiules Rytų Europos teritorijas. Todėl yra taip svarbu, kad mes ir mūsų sąjungininkai pasipriešintų Putinui“.

Rusijos užsienio reikalų ministerijoje šį pareiškimą padarė pajuokos objektu. Trass būgštavimus taip pat išsklaidė Suomijos prezidentas Sauli Nijiniste: situaciją Baltijos jūros regione jis apibūdino kaip „pakankamai taikią“. Lietuvos, Latvijos ir Estijos atstovai šios medžiagos rengimo momentu tyli.

Galimai, atsiras ir nauji žvalgybos duomenys apie Putino planus „užtvirtinti  sėkmę“ po sėkmingos karinės operacijos Ukrainoje. Ypatingas vaidmuo šiuose „planuose“ bus skirtas Lietuvai.

Visų pirma, esą, per jos teritoriją Rusijai prisieis pramušti sausumos koridorių į Kaliningrado sritį. Antrą, už nutrauktą „Belaruskalij“ krovinių tranzitą lietuviams atkeršyti panorės Baltarusijos prezidentas Aleksandras Lukašenka.

Dar ir Kinija.

Kinija taip pat turi savo priekaištų Lietuvai, dėl kurių ėmėsi neoficialių prekybos sankcijų. Bet jei Putinas panorės rakėtomis „kirsti“ į Pabaltijo respublikas, tai Pekine už tai bus padėkos aplodismentais...

Maždaug tokios koncepcijos gali laikytis Lietuvos valdantys konservatoriai-„landsbergistai“. Gražiai skamba: iškarto trys „grėsmės“ (rusiška, baltarusiška ir kinų) susilieja į vieną ir pakimba virš Vilniaus. Panaši retorika Gabrieliui Landsbergiui atvers vakarų lyderių kabinetų duris. Dar atsitiks taip, kad Baidenas pakvies jį į Baltuosius rūmas  pilnavertėms deryboms. Pačios Lietuvos viduje „rusiška agresija“ atitrauks visuomenės dėmesį nuo socialinio-ekonominio pobūdžio problemų.

Ukrainos Aukščiausiosios Rados frakcijos „Tautos tarnas“ vadovas Dovydas Arachamija paskaičiavo, kad kiekvieną mėnesį jo šaliai isterija apie „rusišką invaziją“ apsieina 2-3 milijardus dolerių. Kapitalo bėgimas, investicinio klimato blogėjimas, tėvyninių kompanijų akcijų kritimas, nacionalinės valiutos devalvavimas – visą tai vyksta šalyje, kuri gyvena laukdama karo.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 15 — id: `scraped:rubaltic_lt:075570f51c3b881e`

**Title:** Prie sprogimo ribos: Lietuvos gyventojai remia masinius protestus

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Nepriklausomybės diena Lietuvoje buvo atšvęsta esant panašiom į kovinę padėtį sąlygom. Lietuvos žiniasklaida šventinius renginius komentavo su tokia nuotaika, lyg tai baimindamasi   jų peraugimo į revoliuciją. Ir tai nestebina: praėjusiuose masiniuose renginiuose minia nušvilpė vyriausybės narius, apie savo paramą protesto akcijoms prisipažįsta 40 % lietuvių.

„Tiesiogiai arba užuominomis, provokacijoms, ypač socialiniuose tinkluose, ragina prokremliškai nusiteikę veikėjai, su COVID pandemija susijusių sąmokslo teorijų platintojai,  visuomenės nuotaikų  radikalizavimu bei  padėties valstybėje destabilizavimu suinteresuoti asmenys“, - Nepriklausomybės švenčių išvakarėse perspėjo Lietuvos saugumo departamentas.

Specialioji tarnyba perspėjo Lietuvos vadovybę ir visuomenę, kad šventiniais vasario 16 renginiais gali bandyti pasinaudoti „neįtakingos, bet agresyviai nusiteikusios grupės, kurstančios neramumus visuomenėje“. Susijusios, suprantama, su Kremliumi. Ir dar su Lukašenka.

Susidaro įspūdis, kas apie „Kremliaus ranką“ Lietuvos saugumiečiai kalba jau grynai automatiškai. Arba pasakojimas apie intrigas iš užsienio jau tapo Kanono, kurį negalima ignoruoti dalimi. Kitu atveju juos pačius priskirs prie Kremliaus agentų.

Remiantis kompanijos Vilmorus sociologinės apklausos rezultatais, nuo praeitų metų vasaros protesto akcijas Lietuvoje daugiau ar mažiau rėmė apie 40% gyventojų. Protesto akcijas vienareikšmei smerkė 20% lietuvių, maždaug tiek pat negalėjo apsispręsti, 17% visiškai rėmė protestų aktyvumą, 22% - greičiau rėmė.

Tokia sociologija atžagaria ranka tvoja Lietuvos valdžios „advokatams“, kurie, jau greitai sukaks metai, kaip įrodinėja, kad išeinantys dalyvauti masinėse akcijose ir viešosiose renginiuose nušvilpiantys ministrus, žmonės – tai vienetiniai marginalai, kuriuos į Vilnių suveža Kremliaus agentai.

Ekspertai jiems kala į galvą: jei nepripažinti, kad Lietuvoje protesto nuotaikos yra masinio pobūdžio ir nebaigti smerkti juos kaip „Kremliaus ranka“ bei „penktąją kolona“, socialinio sprogimo grėsmė šalyje tik didės.

„Žmonės negyvena vakuume, jie bendrauja su aplinkiniais. Jei mes matome, kad yra socialinės grupės, kur remiančiųjų procentas aukštesnis negu neremiančiųjų, jie bendrauja viena su kita, mato tuos, kurie remia. Ir mato kontrastus visuomenės erdvėje, kurie byloja apie kitką. Įsivaizduokite, kaip jie turi jaustis. Jei jie savo akimis mato, kad aplinkui visi nepatenkinti, remia protestus. O viešumoje viską pateikia kitaip. Tada auga pyktis, didėja mobilumas“,- aiškina Vilniaus universiteto profesorė Ainė Armonaitė.

Po to, kai sausio 13 mitinge minia nušvilpė Lietuvos ministrus, valdančios konservatorių partijos politikai pradėjo baimintis naujų viešų pažeminimų daugiatūkstantiniuose susirinkimuose. Todėl Lietuvos žiniasklaida transliavo vasario 16 renginius su tokia nuotaika, lyg tai buvo kalbama ne apie Nepriklausomybės dienos šventimą, o apie „rusų rengimąsi invazijai į Ukrainą“. VSD informacija apie Nepriklausomybės dienos šventėje laukiamas „prokremliškų jėgų“ provokacijas tokiame kontekste pradedama vertinti kaip preventyvi reakcija į eilinę viešą konfūziją.

Ar verta stebėtis tokia konfūzija ir sociologijoje, remiantis kuria, iki 40% Lietuvos piliečių remia masinius protestus, kai valdančios partijos ir šalies vyriausybės paramos reitingas randasi 10% rajone? Nenuostabu, kad vasario 16 iškilmėse Vilniaus centre „tautos tėvas“ – pirmasis postsovietinės Lietuvos vadovas ir konservatorių partijos dvasinis įkvėpėjas Vytautas Landsbergis ir vėl buvo nušvilptas.

Visi laukė tautos reakcijos pagrindinio „landsbergisto“ atžvilgiu– ir tauta neapvylė.

Tuo įdomesnė Lietuvos politikų aistra abejoti kitų legitimumu. Prieš keletą savaičių Lietuvos atstovai ETPA, pavyzdžiui, bandė paskelbti nelegitimiu Vladimirą Putiną.

Psichologijos požiūriu čia viskas logiška. Nuosavi kompleksai veržiasi išorėn arba, kaip sako liaudis, kas kam skauda, tas apie tą ir kalba. Apie visuomenės dorovę visų daugiausiai pergyvena seksualiniai iškrypėliai, o kitų legitimumą neigia politikai, kuriuos rinkėjai jau štai pakabins ant šakių.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 16 — id: `scraped:rubaltic_lt:f8b523a9a19a8212`

**Title:** Latvija ribojasi su Ukraina: Vakarai nugrimzdo į geografinį kretinizmą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Fenomenali įtampos eskalacija aplink Ukrainą yra lydima fenomenaliu vakarų politikų, ekspertų ir žurnalistų kvailystės srautu. Kraštutine šios kvailystės apraiška yra geografinė kvailystė. Europoje ir JAV demonstruojamas geografijos nežinojimas mokykliniame lygyje, bet kartu su tuo pareiškiama apie visą žinančią savo žvalgybą regione, kuri praneša apie „ruošiamą Rusijos invaziją“. RuBaltic.Ru analitikos portalas surinko pačius ryškiausius geografijos „pažinimo“ paskutiniaisiais mėnesiais „perlus“.

Smolenskas- siena su Ukraina

Geografinė kvailystė iš pat pradžios tapo vakarų isterijos pagrindu apie „Rusijos invaziją“ į Ukrainą. Nuo praeitų metų rudens amerikiečių žiniasklaida pradėjo publikuoti savo šaltinių tvirtinimus apie tai, kad Putinas ruošia Ukrainos užpuolimą, kadangi rusų pajėgų smūgiuojanti grupuotė sukoncentruota palei Smolenską – prie Rusijos – Ukrainos sienos.

Ne pats trumpiausiai kelias žaibiškam užpuolimui, akimirksniu kirtus sieną.

Charkovas tai Rusija

Sausyje amerikiečių televizijos kanalas CNN parengė eilinį šabloninį siužetą apie „Rusijos invaziją“ į Ukrainą, kur Charkovo miestą pripažino Rusijos dalimi.

Šiame amerikiečių pasityčiojime iš geografijos jaučiasi gilus istorinis paveldimumas. Didžiosios Britanijos premjeras Deividas Lloidas Džordžas Pilietinio karo metais buvo įsitikinęs, kad Charkovas – tai rusų baltagvardiečių generolas.

Karalius Georgas Penktasis apdovanojo „generolą Charkovą“ britų Michailo ir Georgijaus ordinu, ir britų misija Denikino štabe ilgą laiką bandė surasti naujai iškeptą Jo Didenybės riterį, kad jam pranešti apie didžią monarcho malonę.

1927 metais apie tą, jau tapusį patarle, anglų nemokšiškumą, rašė didysis rusų rašytojas Vladimiras Nabokovas.

Rostovas ir Voronežas – tai ne Rusija

Šlovingas britų geografinės kvailystės tradicijas mūsų dienomis pratęsė Didžiosios Britanijos užsienio reikalų ministrė Elizabet Trass. Diskusijos, kuri vyko Maskvoje, metu Trass apkaltino Rusiją, kad ši rengiasi pulti Ukrainą tuo pagrindu, jog Rusijos karinių pajėgų manevrai vyksta greta Ukrainos sienų. Rusijos diplomatai pažymėjo, kad Rusija turi visišką suvereninę teisę organizuoti karinių pajėgų manevrus savo teritorijoje ir kolegai uždavė retorinį klausimą, ar ji pripažįsta RF suverenitetą Rostovo ir Voronežo srityse.

Grįžus iš Maskvos Elizabet Trass teko pergyventi savo tėvynainių pajuokų bangą. Britai kalbėjo, kad Foreing Offise vadovė padarė gėdą visai šaliai ir patarinėjo jai sėdėti namuose – esą, su tokiais smegenimis nauja „geležinė ledi“ iš jos vis vien nesigaus.

Britų URM buvo priverstas pasiaiškinti, kad ponia ministrė galvojo, jog kalbama apie Ukrainos Rostovo ir Voronežo sritis. Tai dar labiau palinksmino publiką. Labiausia išprusę Oksfordo absolventai šiuo atveju citavo Nabokovą.

Latvijos – Ukrainos siena

Geografiniu kretinizmu Rytų Europos atžvilgiu sirguliuoja ne tik amerikiečiai už vandenyno, bei kitame Europos gale esantys anglai. Pačioje Rytų Europoje savo regiono geografiją taip pat yra blogai žinoma.

Tikriausiai, SSSR mokyklinis geografijos kursas Latvijos SSR buvo skaitomas „okupaciniu“ dalyku, o paaugę LETA autoriai bei redaktoriai jį pravaikštinėjo. O jauni autoriai bei redaktoriai po „nepriklausomybės atstatymo“ „pasirinko Europą“ ir mokykloje mokėsi tik tų šalių geografijos, kurios randasi į vakarus nuo Latvijos ir yra NATO ir Europos sąjungos narės.

Bet kokiu atveju, jiems nėra žinoma, kad į Latviją iš Ukrainos reikia „braukti“ apie tūkstantį kilometrų per visą Baltarusiją ir Lietuvą, o Latvijos – Ukrainos siena iš viso neegzistuoja.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 17 — id: `scraped:rubaltic_lt:6ae30019a1247d7e`

**Title:** Nemačiau, bet smerkiu: Lietuva atsisakė stebėti karinius manevrus Baltarusijoje

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Baltarusija savo teritorijoje neorganizuoja „kokios tai žymios karinės veiklos“, apie kurią iš anksto reikia painformuoti ir aptarti su vakarų partneriais. Apie tai Minsko atstovai pareiškė ESBO pasėdyje, sušauktame Pabaltijo respublikų iniciatyva. Lietuvos ir Latvijos susirūpinimas atrodo ypatingai komišku, kadangi jos atsisakė stebėti baigiamąją Rusijos Baltarusijos karinių manevrų „Sąjunginis ryžtas-2022“ baigiamąją fazę. Tai dar karta pabrėžia, kad Pabaltijį patys manevrai nedomina – joms tiesiog reikia sukelti kuo daugiau triukšmo.

Nuo vasario 10 iki 20, Baltarusija kartu su Rusija praveda bendrus karinius manevrus „Sąjunginis ryžtas-2022“. Žinoma, kalbama apie ryžtą „užpulti“ Ukrainą, iš visų pusių ją apsupti, suimti į žnyples ir taip toliau.

Nenuostabu, kad į „įtartiną“ „paskutinės diktatūros Europoje“ karinį aktyvumą atkreipė dėmesį Lietuva, Latvija bei Estija. Jų iniciatyva įvyko ESBO pasėdis, kuriame dalyvavo oficialūs Minsko atstovai. Pabaltijys preliminariai buvo painformuotas apie manevrus, bet informacija liko nepatenkintas.

„Atsakant į Baltijos šalių paklausimą, vasario 11 buvo gautas atsakymas iš Baltarusijos, kuriame nebuvo pateikta užklausiama informacija apie karinius manevrus „Sąjunginis ryžtas-2022“, todėl Latvija, Lietuva ir Estija prašo susitikimo su Baltarusija ESBO formate, kuri įvyks 48 valandų laikotarpyje, siekiant pakartotinai pateikti informacijos užklausimą(...) Baltarusija pateikė informaciją apie tai, kad manevrų apimtis neviršija 13 000 kariškių, kas atitinką informacijos pateikimo pagal Vienos dokumentą ribą, bet visiems prieinama informacija, o taip pat ir informacija, kurią turi Latvijos gynybos ministerija, aiškiai nurodo, kad, užimtų manevruose baltarusių ir rusų kariškių bei karinės technikos kiekis, žymiai viršija šią ribą“,- sakoma Latvijos gynybos ministerijos Interneto svetainėje.

Ir netgi kokia tai „visiems prieinama informacija“ nurodo į tikrąjį manevrų „Sąjunginis ryžtas-2022“ mastą. Tada, kodėl Vilniui, Rygai ir Talinui prireikė reikalauti atsakymo iš Lukašenkos? Jie ir taip viską žino...

Be to, į Latvijos gynybos ministerijos pranešimą įsibrovė siaubinga klaida! Baltijos šalys nebegali gauti atsakymo iš Baltarusijos, kadangi šios šalies „teisėtai išrinkta prezidentė“ Svetkana Tichonouskaja sėdi Lietuvoje ir visiškai nieko nežino apie manevrus „Sąjunginis ryžtas-2022“.

Buvo gautos jo atstovų atsakymas. Ir jo atstovai tiesioginių diskusijų metu pakartotinai išaiškino savo poziciją Pabaltijo kolegoms.

Minskas turėjo visišką moralinę teisę akcentuoti dėmesį šiam klausimui: kodėl sankcijos visada įvedamos prieš Lukašenkos režimą, kurį vakaruose jokiu būdu negalima tapatinti su šalimi, o diskutuoti be jokių išlygų kviečia Baltarusiją? Tiksliai taip pat „atsakovas“ galėjo ignoruoti užklausimą.

Bet Baltarusijos diplomatai priėmė Pabaltijo kvietimą ir pažymėtinai mandagiai atsakė į jos pretenzijas. Vieši informacijos šaltiniai leidžia išskirti pagrindinius oficialaus Minsko argumentus: Baltarusijoje „nevyksta kokia tai žymi karinė veikla, apie kurią reikia painformuoti iš anksto“; Baltarusija ėmėsi savanoriškų veiksmų nukreiptų manevrų skaidrumui padidinti; Baltarusija pati susirūpinusi savo vakarų kaimynų kariniu aktyvumu.

„Mums susidarė įspūdis, kad nepriklausomai nuo mūsų atsakymo esmės, mūsų partneriai jau yra nulėmę savo sekantį žingsnį. Apie tai liudija jų žaibiška vieša reakcija į mūsų atsakymą. Ar gi tai tikra diplomatija, kai apie mūsų partnerių reakciją mums tampa žinoma iš žiniasklaidos, kuri cituoja mūsų pačių atsakymus? Ar gi tai gelbsti mūsų sąžiningam dialogui? Mes labai abejojame, kad tai yra taip“.

Be to, atsargoje pas baltarusių delegaciją lieka dar vienas „koziris“.

„Mes esame gavę kvietimą stebėti baigiamąją manevrų fazę. (...) Mes puikiai suprantame, kad dažniausiai tai būna parodomasis šou. Visiškam skaidrumui reikalinga smulki informacija apie dalyvių skaičių, jų sudėtį, techniką“, - pasakė Lietuvos gynybos ministras Arvydas Anušauskas.

Vėliau paaiškėjo, kad panašų kvietimą gavo Latvija. Jei Pabaltijiečiai daugiau visų pergyvena dėl karinių manevrų Baltarusijoje, tai jiems niekas netrukdo stebėti savo pergyvenimų objektą. Tegul tai būna parodomasis šou (stebėjimo programą parengia priimančioji šalis). Bet tokiu atveju Vilnius ir Ryga galės pareikšti, kad jie nepatenkinti pamatytų, kadangi Baltarusija nuo jų nuslėpė realų manevrų mastą.

„Stebėti manevrus buvo pakvieti Lietuvos ir Latvijos atstovai, o taip pat karo atašė, akredituoti prie Baltarusijos gynybos ministerijos. Atsakymo įkvietimą, kuris buvo išsiųstas kaip geros valios gestas, mes negavome“, - kalbėjo pastovus Baltarusijos atstovas prie ESBO Andrėjus Dapkiūnas.

„Ne skaičiau, bet smerkiu“ – tokia frazė, būk tai, buvo pasakyta 1958 metais SSSR Rašytojų sąjungos valdybos posėdyje svarstant Boriso Pasternako bylą. Panašiu principu šiandieną vadovaujasi Pabaltijo politikai – patys labiausiai atsidavę „sovietiškų“ tradicijų pasuolėtajai.

Stebėti Rusijos – Baltarusijos manevrus jie nenori. Bet pasirengę juo pasmerkti.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 18 — id: `scraped:rubaltic_lt:4317e64fdf094a46`

**Title:** Iš Lietuvos pabėgs: Rusija pasiekė NATO kariškių išvijimo iš Ukrainos

**Source:** rubaltic_lt (propaganda)

**Text:**

```
JAV ir Didžioji Britanija iš Ukrainos teritorijos evakavo savo karinius instruktorius. Tai stambi Rusijos pergalė, kadangi aktualiausia grėsme jos nacionaliniam saugumui iš Ukrainos pusės buvo tai, kad NATO karinė infrastruktūra Ukrainoje plečiasi ir jai nebūnant Šiaurės Atlanto aljanso nare. Dabar NATO kariškiai paprasčiausiai bėga iš Ukrainos, šiais savo veiksmais įrodydami, kad už Rytų Europą jie su Rusija nekariaus.

Minsko susitarimų, kuriuos jau aštunti metai vakarų sąjungininkai negali priversti Ukrainą įvykdyti, 10 punktas nurodo „ Iš Ukrainos teritorijos išvesti visas užsienio karines formuotes, karinę įrangą ir samdytus kovotojus, stebint ESBO. Nuginkluoti visas neteisėtas grupuotes”.

Po septynerių metų „marlezono baleto Normandijos formate“ Minsko susitarimai šioje dalyje pradėjo vykdytis savaime.

Pentagono vadas Lloid Ostinas, pažymėtina, po pokalbio su kolega iš Rusijos Sergejumi Šoigu, įsakė išvesti amerikiečių kariškius iš Ukrainos. „Ministras Ostinas davė potvarkį laikinai perdislokuoti 160 Floridos Nacionalinės gvardijos kariškių, kurie nuo lapkričio pabaigos buvo dislokuoti Ukrainoje“, - sakoma Pentagono pranešime.

Dar anksčiau, ir taip pat po pokalbio su Sergejumi Šoigu, Didžiosios Britanijos gynybos ministro pavaduotojas Džeimsas Hippi paskelbė apie maždaug šimto britų karinių instruktorių evakavimą iš Ukrainos. Tai dar labiau parodomasis žingsnis negu, analogiškas JAV sprendimas. Būtent, po „Breksito“ bandanti save įtvirtinti pasaulio arenoje, Didžioji Britanija pastaraisiais metais yra pagrindinis NATO antirusiškumo sužadintojas.

Didina savo karinį buvimą Lenkijoje, Pabaltijyje ir Rumunijoje, rengia karines provokacijas prie Krymo krantų, ten pat stumia ir ukrainietiškus sąjungininkus.

Tai yra, pasielgė taip, kaip panašiose situacijose visada elgiasi pigūs provokatoriai. Populiariai kalbant „nutekėjo“.

Suprantama, NATO specų bėgimas iš Nezaležnos teritorijos yra lydimas daugiažodžiais patikinimais, kad evakavimas yra laikinas, ir pagrindiniai sąjungininkai vis vien niekada neatsisakys savo principų. Tai yra duris į NATO Ukrainai neužvers, ir jokių jos neįstojimo į Aljansą garantijų Putinui neduos.

Tačiau reikalingų sau tarpinių rezultatų Rusija jau pasiekė.

Aktualiausia grėsmė Rusijai buvo būtent tame. Paslaptingas NATO karinių bazių dislokavimas Ukrainoje buvo Polišinelio paslaptimi: Rusijos žiniasklaida dar spalio mėnesį publikavo tyrimą apie tai, kiek NATO bazių randasi Nezaležnoj ir kur jos slepiamos. Tai yra, plačiai nuskambėjusios amerikietiškos raketos greta Charkovo nebuvo perspektyvine grėsme – ten jos galėjo tuo pat atsirasti.

Todėl nuo rudens Maskva pradėjo primygtinai reikalauti iš Džozefo Baideno administracijos strateginio saugumo Europoje garantijų. Ir Baltieji rūmai, atsižvelgdami į Rusijos karinės sąjungos su Kiniją grėsmę, sėdo už derybų dėl saugumo garantijų stalo.

Iki šio politinio derėjimosi pabaigos dar gana toli – ne faktas, kad jis pasibaigs kokiais tai strateginiais susitarimais iki 2024 metų, kai ir Rusijoje ir JAV vyks prezidento rinkimai.

Baltieji rūmai anonsavo Rusijos invaziją trečiadienį, vasario 16 d. – ir čia pat patvirtino, kad per išeigines, vasario 12-13 d. amerikiečių kariniai instruktoriai iš Ukrainos bus išvežti. JAV piliečiai Rusijos ir Ukrainos kare jokių būdu nedalyvaus, kadangi Jungtinėms Valstijoms Ukraina reikalinga tik Rusijos „suturėjimui“. Ukrainos su Rusija karas idealiai užtikrina tokį „suturėjimą“, o pati Ukraina JAV nereikalinga.

Bet ši taisyklė liečia ne vien tik Ukrainą. Kam, pavyzdžiui, Jungtinėms Valstijoms Pabaltijys kaip ne Rusijos spaudimui? Pačios Lietuva, Latvija ir Estija niekam nereikalingos.

Šiandieną Pabaltijys Rusijos ir Vakarų santykiuose – tai tas pats, kaip ir Ukraina. Karinis placdarmas, NATO infrastruktūros plėtra, ir teritorija, kuri be sąryšio su Rusija, nereikalinga nei Europai, nei JAV.

Atitinkamai, ir Maskvos metodai turi būti tokie patys, kaip ir Ukrainoje, jei ten jie pademonstravo savo efektyvumą.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 19 — id: `scraped:rubaltic_lt:18563fe3e6b87c37`

**Title:** Ukraina pripažino: gandai apie „Rusijos invaziją“ – speciali JAV operaciją

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Jungtinės Amerikos Valstijos praveda vieną iš didžiausio istorijoje masto specialią informacinę operaciją prieš RF, ir ukrainiečiai turi tai suprasti, kai girdi apie „neišvengiamą Rusijos invaziją“. Apie tai pareiškė oficialus Kijevo atstovas NATO parlamento asamblėjoje Jegoras Černevas. Jo žodžiais tariant, vienas iš amerikiečių uždavinių – mobilizuoti NATO šalis ir suvienyti Aljansą prieš bendrą priešą. Tas faktas, kad Ukrainą tiesiogiai panaudojama kaip instrumentas, Černevą netrikdo. Savo tėvynainius jis kviečia pakentėti vardan solidarumo su Amerika.

Naujienų škvalas „apie Rusijos invaziją“, kurią Vakarai paskyrė ar tai vasario 15-ją, ar tai vasario 16 dieną, privertė Ukrainos prezidentą Vladimirą Zelenskį susinervinti. Nepatenkinta veido mina jis pareiškė, kad Ukrainos informacinė erdvė yra persotinta naujienomis apie agresyvius Maskvos ketinimus.

„Aš nesakau, kad mes sutinkame ar nesutinkame su kokia tai informaciją apie būsimą įvykį, kuris neįvyko. Mes analizuojame įvairią informaciją. Ir aš negaliu pasakyti, kad mūsų ukrainietiška žvalgyba veikia blogiau vakarietiškos“, - taip Zelenskis atsakė į klausimą, ar jis pasirengęs paneigti vakarų žurnalistų ir politikų vertinimus.

Bendrai paėmus, Ze-komanda atsidūrė tarp kūjo ir priekalo. Stiprinti paniką jie nepageidauja, atvirai prieštarauti kuratoriams iš už vandenyno jie negali. Tenka mėmėti kažką tai nesuprantamą.

Bet, kaip sakoma „k iekviena šeima turi savo juodąją avelę“.

Tai Aukščiausios Rados partijos „Slugi naroda“ deputatas, Ukrainos gynėjų teisių ir laisvių užtikrinimo konsultacinės tarybos vadovo pavaduotojas, o taip pat Ukrainos delegacijos NATO parlamentinėje asamblėjoje vadovas Jegoras Černevas.

Tai, kas parašė savo „facebook“, panašu į užkietėjusią „Kremliaus propagandą“, Černevo žodžiais tariant, JAV veda prieš Rusiją „ vieną iš didžiausio istorijoje masto informacinę specialiąją operaciją“ kurios uždaviniai „gerai matosi“:

„1. NATO šalių mobilizavimas ir Aljanso bei Vakarų bendros vienybės atstatymas.

2. RF demonizavimas pasaulyje ir pastovaus toksiško jos įvaizdžio kūrimas.

3. Didžiausios žalos RF ekonomikai padarymas nekariaujant.

4. Antikarinių nuotaikų sužadinimas pačioje Rusijoje.

5. Rusų karinio elito demoralizavimas viešai demaskuojant jų slaptą medžiagą.

„Šios operacijos tikslas taip pat aiškus – galutinai išstumti Putiną iš Europos ir padarytį neįmanomu sukurti vieningą Eurazijos erdvę nuo „Vladivostoko iki Lisabonos“ ir projektą „Viena juosta – vienas kelias“, kur Rusijai skiriamas pagrindinis vaidmuo, o Ukraina būtų jos vasalu. Dėl to JAV nori priversti Putiną baigti hibridinių karų žaidimus ir pasirinkti galutinai: arba ryžtis į plataus masto invaziją, arba galutinai atsitraukti ir užsidaryti savo šalies viduje“.

Bet Kijevui nėra ko bijoti! Černevo nuomone, Vakarai „sparčiai palaidos RF ekonomiką“, Putino režimas grius, o ukrainiečiai „ilgus dešimtmečius galės ramiai gyventi ir taikiai vystytis“. Tai yra, karas su Rusija – tai dargi yra gėris.

Įsivaizduokite sau 1939 metų Lenkiją, kuri džiaugiasi (!) Antrojo pasaulinio karo pradžia. Rodos, absurdas, bet Ukrainoje maždaug taip ir vyksta...

JAV uždavinių sąraše, kurį sudarė Černevas, daug kas atrodo iščiulptu iš piršto. Ypatingai paskutinis punktas: kokią „slaptą medžiagą“ apie Rusijos invaziją paviešino už vandenyno paskutiniu metu?

Taip, pavyzdžiui, seniokas Mett Li surengė JAV Valstybės departamento spikerio Nedo Praiso parodomąją pylą.

Ned Prais: „ Rusijos specialiosios tarnybos planuoja Rusijos teritorijos užpuolimo Ukrainos kariškiais inscenizacijos vaizdo įrašą“.

Mett Li: „Ar jus turite kokius tai įrodymus?“

Prais: „Jei jūs abejojate JAV vyriausybės, Britanijos vyriausybės bei kitų vyriausybių duomenų patikimumu ir norite pasiguosti ta informaciją, kurią platina rusai, tada pirmyn, mes nekliudome“.

Li: „Pasiguosti?! Aš neklausiu kokią informaciją platina rusų vyriausybė. Ką tai iš viso reiškia? Aš pakankamai ilgai esu profesijoje ir gerai atsimenu pareiškimus apie masinio naikinimo ginklą Irake, ir užtikrinimus kad Kabulas negrius. Aš daug ką atsimenu. Kur ta išslaptinta informacija, neskaitant to, kad jūs čionai ateinate ir kalbate?“

Prais: „Man tenka gailėtis, kad jums nepatinka turinys. Gaila, kad jūs abejojate ta informacija, kuri yra pas amerikiečių vyriausybę...“

O kur dabar Rusijoje kyla antikarinės nuotaikos? Kur vyksta tūkstantiniai mitingai su plakatais „Šalin rankas nuo Ukrainos“?

Bet su jo sąrašo pirmuoju punktu sunku nesutikti: „NATO šalių mobilizavimas ir Aljanso vienybės atstatymas“. Čia Ukraina panaudojama kaip pėstininkas, kurį negaila paaukoti, dėl „sunkiasvorės“ figūros pozicijos pagerinimo ant šachmatų lentos.

Kartu su tuo, pats Jegoras Černevas tai ir pripažįsta. Jis taip ir rašo: Ukraina patirs esminius ekonominius praradimus dėl investicijų išėjimo ir panikiškų nuotaikų. Teks pakentėti. Kaip gi čia nepakentėti, jei užstatyti anglosaksų interesai?

„ – Bet gi jūs negalite pajudėti!

– Nesvarbu, ponia Miulerova, į karą aš vyksiu vežimėlyje. (...) Aš esu visiškai tinkamas patrankų mėsai, bet štai tik kojos... Bet kai reikalai su Austrija netikę, kiekvienas luošys turi būti savo poste“.

Apie tai Jaroslavas Hašekas rašė su humoru. Ar galėjo jis pagalvoti, kad XXI amžiuje ištisa europietiška šalis taps šauniuoju kareiviu Šveiku?

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```

### Article 20 — id: `scraped:rubaltic_lt:d93cff88b122d122`

**Title:** Lietuvos ambasadoriui Maskvoje tiesiai buvo pasakyta tiesa apie Rusijos piliečio persekiojimą

**Source:** rubaltic_lt (propaganda)

**Text:**

```
Vasario 3 d. Lietuvos ambasadorius Rusijoje Eitvydas Bajariūnas susitiko su Rusijos Federacijos Visuomenės Rūmų (VR) atstovais. Pažymėtina, kad susitikimo organizavimo iniciatyva priklausė pačiam diplomatui. Rusijos šaliai tai buvo siurprizu. Apie tai, kodėl dialogo pradžią su Bajariūnu galima pavadinti įvykiu, pažymėtu ženklu “plius” ir kad šiame dialoge buvo kalbama apie Rusijos karinių pajėgų pensininko Jurijaus Melio persekiojimą Lietuvoje, RuBaltic.Ru analitikos portalui papasakojo Rusijos Visuomenės Rūmų atstovas Michailas Aničkinas.

- Ponas Aničkinai, RF Visuomenės Rūmų Interneto svetainėje gana smulkiai aprašytas susitikimas su Lietuvos Respublikos nepaprastuoju ir įgaliotoju ambasadoriumi RF Eitvydu Bajariūnu. Susidaro įspūdis, kad jame vyravo maloni armosfera: buvo aptariami klausimai dėl kurių Maskva ir Vilnius gali efektyviai saveikauti, organizuoti bendradarbiavimą. Ponas Bajariūnas netgi pažymėjo, kad daugelis lietuvių “gyvena Rusijoje ir jaukiai jaučiasi”. Bet vėliau Jūs pažeidėte idiliją, paliesdami ruso Jurijaus Melio baudžiamojo persekiojimo temą. Ar aš teisingau suprantu įvykių eigą?

- Pradėkime nuo to, kad susitikti pasiūlė pats Lietuvos ambasadorius, tai buvojo iniciatyva. Tiesiai pasakius, neįprasta iniciatyva. Jums gi žinoma kas vyksta tarptautinėje arenoje. Ir staiga Lietuvos ambasadorius išreiškia pageidavimą apsilankyti RF Visuomenės Rūmuose, susipažinti su mūsų civilinių institucijų veikla. Manau, kad iš jo šalies tai buvo svarbus ir neordinarus žingsnis.

Bendrai, Eitvydas Bajariūnas apibūdinamas kaip gana tvirtas mūsų šalies atžvilgiu politikas. Be to jis turi didelė praktinę patirtį, anksčiau buvo konsulu Sank-Peterburge.

Bajariūną domino kokiu būdu pas mus susidėstę civilinės visuomenės ir valdžios santykiai. Jo požiūriu tai gana įdomi tema, kurią jis nagrinėja, kad ką tai, galimai, taikyti Lietuvoje.

Rūmų sekretorė Lidija Michejeva į susitikimą pakvietė Tautinių ir tarpreliginių santykių derinimo komisijos pirmininką Vladimirą Zoriną, Demografijos, šeimos apsaugos, vaikų ir tradicinių šeimos vertybių komisijos pirmininką Sergejų Rybalčenko.

Aš taip pat buvau pakviestas, kadangi Visuomenės Rūmai nuosekliai bando ginti mūsų piliečius nuo neteisingo teismo Vilniuje. Saugumo ir sąveikos komisijoje prie Visuomenės stebėsenos komisijos buvo įsteigta ir funkcionuoja darbo grupė, kuri užsiima šiuo klausimu. Mes turime paruošę rimtas programas, nukreiptas ginti mūsų tėvynainių teises.

Rybalčenko palietė migracijos temą. Aš taip pat pasakiau keletą pastabų, pavyzdžiui, priminiau apie Europos Sąjungos kvotas, remiantis kuriomis Pabaltijys privalės priimti migrantus, kurių kiekis sudaro 10% savų gyventojų. Kyla logiškas klausimas: kokia kalba po 30 metų bus kalbama Lietuvoje, Latvijoje ir Estijoje?

Buvo laiko atsiduoti nostalgijai. Aš prisiminiau, kad jaunystėje buvau „Žalgirio“ krepšinio klubą iš Kauno sirgaliumi, prisiminiau klubo žaidėjų pavardes. O toliau prisiėjo akcentuoti dėmesį į mums skausmingus klausimus. Aš kalbu ne tik apie 1991 m. sausio 13 d. bylą.

Ambasadorius buvo painformuotas, kad RF Visuomenės rūmai šiuo metu rengia kreipimąsi Lietuvos prezidento vardu dėl Jurijaus Melio išlaisvinimo. Ponas Bajariūnas pareiškė, kad yra pasiruošęs jį perduoti tiesiogiai savo šalies vadovui.

- Kaip jis iš viso reagavo? Ar nebandė įrodyti, kad tai yra Lietuvos vidaus reikalas, į kurį Rusija neturi įsimaišyti?

- Bajariūnas mano pasisakymą įvertino su supratimu. Dar kartą pažymėsiu, kad visa priemonė buvo labai konstruktyvi. Lietuvos ambasadorius sudarė taktiško ir protingo žmogaus įspūdį. Jis įdėmiai klausėsi, bandė sušvelninti aštrius kampus.

Pavyzdžiui, Bajariūnas pažymėjo, kad Lietuvoje įstatymas draudžia nacizmo heroizavimą, mokyklose ir vaikų darželiuose nedraudžiamas dėstymas rusų kalba. Vyko ramus pasikeitimas nuomonėmis. Pati susitikimo atmosfera buvo labai geranoriška.

- Nejaugi Lietuvos ambasadorius nieko nesakė apie „rusišką invaziją“ į Ukrainą arba apie Rusijos - Baltarusijos karinių pajėgų manevrus, kurie, būk tai, sudaro grėsmę Lietuvai?

- Ne. Ukrainos jis išviso nelietė – ją gana kvalifikuotai apėjo. Be to Bajariūnas pasiskundė, kad Rusija ne labai atidžiai prižiūri kai kuriuos savo kapus Lietuvos teritorijoje.

Jei Vilnius neturi nieko prieš, tai mūsų specialistai tuo užsiims.

Iš viso, susitikimas buvo organizuotas labai operatyviai. Pradžioje mes net nesupratome, staiga dėl ko Lietuvos ambasadorius vyksta į Visuomenės rūmus? Bet prasidėjus dialogui viskas tapo aišku. Prieš save mes pamatėme žmogų, kuris yra nusiteikęs konstruktyviniam bendradarbiavimui.

- O ar kiti ambasadoriai lankosi RF Visuomenės Rūmuose?

- Paskutinį kartą buvo Etiopijos atstovas. Mes stebėjome rinkimus šioje šalyje, todėl ambasadorius paprašė susitikimo, norėjo sužinoti mūsų nuomonę apie pamatytą. Bet Lietuva... Tai ypatingas atvejis. Ponas Bajariūnas vertas pagarbos.

- Logiška manyti, kad jo vizitas į VR buvo suderintas su šalies prezidentu arba URM vadovu.

- Taip, aš nemanau kad ambasadorius galėjo žengti šia linkme be Lietuvos prezidento sutikimo. Ten tikriausiai viskas suderinta. Kovo mėnesį pas mus, į VR atvyksta Lietuvos visuomenininkai. Tai opozicinių pažiūrų žmonės, artimi Algirdui Paleckiui. Anksčiau jie pabuvojo Baltarusijoje, dabar panoro apsilankyti Rusijoje.

Gal būt, būtent tai ir paskatino Lietuvos ambasadorių, sakykime, suveikti anksčiau?

Bet kokiu atveju gavosi netikėtas ir neordinarinis įvykis, pažymėtas ženklu “plius”

- Grįžkime prie Jurijaus Melio. Ar aš teisingai suprantu, kad VR įkurta kokia tai darbo grupė dėl jo baudžiamosios bylos.

- Jei būti tiksliu, tai situacijos monitoringo ir medžiagos, susijusios su 1991 metų sausio mėnesio 13d. įvykiais Vilniuje, analizės darbo grupė. Ji intensyviai dirbo, svarstė, surinko labai daug dokumentų.

Mes tiesiai pareiškėme, kad Jurijus Melis nuteistas neteisingai.

- Pasakykime, kad tai labai nemalonus ir nepatogus įvykis dviejų šalių santykių vystymuisi. Bet mes neturime apie jį nutylėti. Sausio 13 d. bylos figurantus teisė už karinius nusikaltimus ir nusikaltimus prieš žmoniškumą. Tai rimtas iššūkis mūsų valstybei.

Žinoma, reikalinga labai aktyvi mūsų valstybės organų poziciją, kurios mes nestebime. O vėliau viskas užsimirš. Jau auga antra žmonių karta, kuri nelabai supranta, kas vyko 1991 metais. Kaip jiems suprasti?

Atsiliepia tinkamos žiniasklaidos ir valstybės propagandos nebuvimas (gera šio žodžio prasme). Aš manau, kad Jurijaus Melio bylą ir kitus nuteistuosius už 1991 m. sausio mėn. 13 d. Vilniuje įvykius jokiu būdu negalima palikti savieigai.

Informacija

Citavimo sąlygos

Cituodami medžiagas būtinai nurodykite aktyvią mūsų portalo hipernuorodą. Hipernuoroda turi būti matoma, aktyvi, neuždaryta paieškų sistemomis nuo indeksavimo. Autoriai atsako už spausdinamose medžiagose pateiktų faktų teisingumą. Redakcijos nuomonė gali nesutapti su autoriaus nuomone. Už reklaminių publikacijų turinį atsako reklamos kūrėjas.
```
