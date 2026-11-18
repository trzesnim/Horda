# Przewodnik Gracza — Kroniki Rubieży: Horda i Ekspedycje (v7.0.5)

Krótka ściągawka przed meczem dla naszej czwórki — najważniejsze zasady, podział ról na mapie, rekomendowana ścieżka wypraw oraz przegląd szlifów `v7.0.5` po analizie telemetrii z naszego pierwszego, 62-minutowego playtestu co-op (`2026-11-16`).

---

## TL;DR — Najważniejsze zasady w 30 sekund

- **Cel gry:** Broń **Cytadeli (Feitorii P2)** w sercu bazy `(54, 146)` (jej utrata = natychmiastowa porażka wszystkich). Wyjdź za mury, zniszcz **6 Twierdz Hordy (`G1–G3`)** (zostawiając najbliższy obóz `G1` na koniec!), a po `60s` na powrót armii zgładź **Wielkiego Chana Subotaia (4500 HP)** przed Bramą Centralną (po upadku 6. Twierdzy aura Imama wyłącza się, a gwardia `P8` traci połowę Furii Settlementów; dopóki w strefie bitwy `(15..140, 85..185)` żyją jego Żelazne Słonie, Chan regeneruje `+180 HP/3s`).
- **Ustawienia i Fale:** Gracze `P1–P4` (ludzie, P2 najlepiej Hiszpanie) vs `P5–P8` (AI **Extreme**). 14 fal od `8:30` do `92:00` (Fale 7–14 rozrzedzone co 6–8 min, potem Endless co 10 min od `102:00`) — zegar do kolejnej fali i poziom trudności są zawsze na górze **Objectives**, a skrót tych zasad (`TL;DR`) znajduje się na górze zakładki **Objectives** po kliknięciu ikony w górnym pasku gry oraz w **Hints**.
- **Role (`P1–P4`):**
  * **P1 (Niebieski):** Brama Centralna + Król w odizolowanym **Sanktuarium `(4, 138)`** na zachodniej krawędzi mapy (wejście na flagę zmienia trudność `-2..+2`, w tym skaluje wyłomy saperskie `F9`/`F12`).
  * **P2 (Czerwony):** Handel, obrona chłopów przed **Szakalami** + Król-Kwatermistrz w odizolowanej komnacie **`(4, 164)`** (od `10:00` co 4 min wejście Królem na Północną lub Południową Flagę daje rosnące wsparcie: `10–20m` Małe, `20–30m` Średnie, `30m+` Duże; o odnowieniu informuje **flara na `(4, 164)`, dźwięk i wyraźny komunikat na czacie**).
  * **P3 (Zielony):** Brama Północna (uwaga: w **`52:00`** alarm 2 minuty przed wycinką, w `53:30` drugi alarm 30s, a w **`54:00`** saperzy wyrąbią wyłom w północnym lesie!).
  * **P4 (Żółty):** Brama Wschodnia (w **`74:00`** alarm 2 minuty przed wycinką, w `75:30` drugi alarm 30s, a w **`76:00`** wyłom we wschodnim lesie — bez jednoczesnego rajdu handlowego, który przesunięto na F13 `84:00`!) + korytarz handlowy na południu.
- **Wyprawy (Settlementy, Questy i Map PoI):** Zburzenie każdego **Settlementu (`G1–G3`)** daje surowce i **na stałe wyłącza jego fale oraz jednostki specjalne** (wywołując jeden kontratak i *Furię*). **Questy (`Q1–Q4`)** dają potężne perki całej drużynie (`Q1`: mur i handel; `Q2`: rozbij 2 Baszty Bombardowe by zdjąć tarczę Uniwersytetu -> bonus strzelców/jazdy; `Q3`: stały dochód `+100F/+100W/+90G/+20S` co 1 min; `Q4`: przetrwaj 30s odwetu -> `+30%` HP/pancerz i Wielki Klasztor). Dodatkowo na mapie ukryto **3 punkty eksploracyjne (`PoI 1–3`)**.
- **3 złote zasady w walce:** (1) W pierwszej kolejności zabijaj **Arcymaga (Imama)** przed Bramą Centralną (daje kolumnie `P7` tarczę `+8/+8` pancerza i leczy wrogów w strefie `+25 HP/3s`!), (2) Chroń wieśniaków pod TC przed szybkimi **Szakalami** (`7` ataku!), (3) Nie buduj na polanach spawnu Hordy przed bramami (fala niszczy budynki w miejscu swojego pojawienia się).

---

## 1. Ustawienia Lobby (Obowiązkowe)

* **Tryb gry:** Niestandardowy scenariusz (`Custom Scenario`) -> **`Kroniki_Rubiezy_Horda_Coop`**.
* **Gracze 1–4 (Drużyna 1 — Sojusz):** Ludzie.
  * **Gracz 2 (Czerwony):** najlepiej wybrać **Hiszpanów** ze względu na drużynowy bonus **+25% złota z handlu** na długim szlaku przez całą szerokość mapy.
  * **Gracze 1, 3 i 4:** dowolne cywilizacje (np. mocni łucznicy/obrońcy dla Niebieskiego, szybka piechota/machiny dla Zielonego, mocna kawaleria lub kontry na słonie dla Żółtego).
* **Gracze 5–8 (Drużyna 2 — Horda):** Komputer (AI) — ich cywilizacje są automatycznie ustawione i zablokowane przez scenariusz.
  * **Poziom trudności AI w lobby obowiązkowo ustawcie na `Extreme` (Ekstremalny)** — dzięki temu jednostki wroga po wyjściu z lasu mądrze wybierają cele i nie zacinają się przed murami. Prawdziwą siłą i wielkością fal sterujemy sami w trakcie gry w Sanktuarium Balansu.
* **Pozostałe opcje:** Widoczność mapy: **Normalna**, Limit populacji: **200** (rośnie przez zadania nawet do 250), Zablokuj drużyny (`Lock Teams`): **Wyłączone**, Prędkość gry: **Normalna (zablokowana)**, Wszystkie technologie i Kody: **Wyłączone**.

---

## 2. Cel Gry i Zasady Przetrwania

* **Obrona Twierdzy Sojuszu:** Startujemy razem w południowo-zachodniej części mapy (z gotowymi domkami i wspólną wizją z Kartografii). Horda uderza w **14 głównych falach**: pierwsza fala przychodzi o **`8:30`**, druga o **`13:00`**, trzecia o **`18:00`**, Fale 4–6 co 5,5 minuty (`23:30`, `29:00`, `34:30`), natomiast od Fali 7 tempo zwalnia (co 6–8 minut: `40:30`, `47:00`, `54:00`, `61:00`, `68:30`, `76:00`, `84:00`) aż do finałowej 14. fali o **`92:00`** (od **`102:00`** włącza się Tryb Endless co `10` minut). Po `65:30` eskalacja czasowa Hordy całkowicie staje na limicie `+67 HP / +9 Ataku`.
* **Jak wygrać:** Nie wystarczy siedzieć za murami! Musimy wyjść w głąb mapy, zniszczyć wszystkie **6 Twierdz Hordy (Settlementów `G1–G3`)**, po czym dostajemy **60 sekund** na wycofanie armii i obstawienie wszystkich 3 bram (Centralnej `(104, 114)`, Północnej i Wschodniej), aby odeprzeć **Ostatni Szturm Wielkiego Chana Subotaia (4500 HP)** i zgładzić samego Chana.
* **Jak przegrywamy:** Jeśli wrogowie zburzą centralną **Cytadelę (Feitorię Gracza 2)** w sercu naszej bazy, cała drużyna natychmiast przegrywa.

---

## 3. Podział Ról dla 4 Graczy (Kto za co odpowiada)

* **Gracz 1 (Niebieski — Brama Centralna i Sanktuarium Balansu):**
  * Broni głównej **Bramy Centralnej** na wschodniej ścianie centrum bazy (pierwsze podjazdy ruszają tam już od `13:00`, a od `23:30` nadciągają ciężkie fale z Arcymagami i później Słoniami).
  * Posiada nieśmiertelnego Króla w szczelnie odizolowanym klifami i lasem **Sanktuarium Balansu** na zachodniej krawędzi mapy `(4, 138)` (komnata jest zawsze widoczna dla całej drużyny). Wejście Królem na **górną `(4, 135)`** lub **dolną flagę `(4, 141)`** pozwala w dowolnej chwili meczu zwiększyć (`+1`, `+2`) lub zmniejszyć (`-1`, `-2`) poziom trudności Hordy.

* **Gracz 2 (Czerwony — Cytadela, Handel i Kwatermistrz Twierdzy):**
  * Startuje w bezpiecznym sercu bazy obok **Cytadeli (Feitorii)**, ze zwiększonym na starcie limitem populacji (`220`) i sześcioma gotowymi domkami.
  * Odpowiada za gospodarkę, handel wozami (Plac Targowy jest w lewym dolnym rogu mapy) oraz za mobilne odwody w głębi bazy — szczególnie przeciwko wrogim **Szakalom**, które omijają walkę na bramach i wpadają prosto między naszych chłopów pod Town Center!
  * Obsługuje szczelnie odizolowany **Posterunek Kwatermistrza Twierdzy** (`4, 164` na zachodniej krawędzi mapy — odblokowywany o **`10:00`** po Fali 1). Wchodząc **wyłącznie swoim Królem** na jedną z dwóch flag, może raz na **4 minuty** wezwać wsparcie rosnące wraz z czasem meczu (po każdym odnowieniu na `(4, 164)` pojawia się **flara, sygnał dźwiękowy dla P2 i komunikat `[KWATERMISTRZ P2 - GOTOWY!]`**, żeby nie tracić cykli w ferworze walki):
    * **Poziom 1 (`10:00–20:00` — Mały Bonus):** Flaga Północna `(4, 161)` daje **`4x Konkwistador + 1x Mangonel`** wokół `(54, 149)`; Flaga Południowa `(4, 167)` daje **`+125 Żywności/Drewna i +100 Złota`** każdemu graczowi *(bez naprawy murów)*.
    * **Poziom 2 (`20:00–30:00` — Średni Bonus):** Flaga Północna `(4, 161)` daje **`4x Konkwistador + 2x Kolubryna`**; Flaga Południowa `(4, 167)` daje **`+200 Żywności/Drewna/Złota`** każdemu graczowi oraz naprawia Twierdzę i Mur `Q1` o **`+250 HP`**.
    * **Poziom 3 (`od 30:00+` — Duży Bonus):** Flaga Północna `(4, 161)` daje **`6x Elitarny Konkwistador + 2x Kolubryna + 2x Taran Oblężniczy`**; Flaga Południowa `(4, 167)` daje **`+300 Żywności/Drewna/Złota`** każdemu graczowi oraz naprawia Twierdzę i Mur `Q1` o **`+500 HP`**.

* **Gracz 3 (Zielony — Brama Północna i Klif Artylerii):**
  * Broni **Bramy Północnej** (pierwsze uderzenie już o **`8:30`**!). Uwaga: w **`52:00`** pojawia się **wczesny alarm saperski na 2 minuty przed wycinką** (drugi alarm 30s przed w `53:30`), a w **`54:00`** wrodzy saperzy wyrąbią dodatkowy wyłom w północnym lesie na prawo od bramy.
  * Ma najbliżej do pierwszego obozu wroga (**`G1 Północ`**) oraz zadania **`Q2 (Klif Artylerii)`** w północno-zachodnim narożniku mapy.

* **Gracz 4 (Żółty — Brama Wschodnia i Szlak Handlowy):**
  * Broni **Bramy Wschodniej** (pierwszy atak już o **`8:30`**) oraz południowej **Bramy Handlowej**. Uwaga: od **47. minuty** wybrane fale (F8 `47:00`, F10 `61:00`, F13 `84:00`, F14 `92:00` i Endless) wysyłają dodatkowy atak od południa wprost na Szlak Handlowy, w **`74:00`** przychodzi **alarm saperski 2 minuty przed wycinką** (drugi alarm 30s przed w `75:30`), a w **`76:00`** saperzy wycinają przejście we wschodnim lesie (oddzielnie od 3. rajdu handlowego przeniesionego na `84:00`)!
  * Ma najbliżej do zadania **`Q1 (Karawanseraj)`**, którego zburzenie buduje długi Kamienny Mur Handlowy z 6 basztami i otwiera bezpieczny szlak dla wozów handlowych przez całą mapę.

---

## 4. Wyprawy poza Mury: 6 Settlementów, 4 Questy i 3 Punkty Eksploracyjne

Wszystkie 6 Twierdz Hordy i 4 Questy mają nad sobą stałe odsłonięcie pod Mgłą Wojny — w każdej chwili możecie na nie kliknąć, żeby sprawdzić opis i nagrody.

### 6 Twierdz Hordy (Settlementów `G1–G3`)
Zniszczenie głównego budynku obozu daje każdemu graczowi duży zastrzyk Żywności i Złota oraz **na stałe wyłącza jego fale i przypisane do niego jednostki specjalne**:
1. **`G1 Północny`** *(+700 Żywności / +700 Złota)* — wyłącza **Berserkerów i Petardy**.
2. **`G1 Wschodni`** *(+700 Żywności / +700 Złota)* — wyłącza **Huskarlów i Płonące Wielbłądy**.
3. **`G2 Akademia`** *(+1000 Żywności / +1000 Złota)* — wyłącza **Snajperów, Moździerze Oblężnicze oraz wycinanie lasów przez saperów**.
4. **`G2 Klasztor`** *(+1000 Żywności / +1000 Złota)* — wyłącza **Arcymagów z globalną tarczą oraz rajdy Szakali**.
5. **`G3 Cytadela Północna`** *(+1500 Żywności / +1500 Złota)* — wyłącza **Żelazne Słonie** atakujące od północy/centrum.
6. **`G3 Cytadela Wschodnia`** *(+1500 Żywności / +1500 Złota)* — wyłącza **Żelazne Słonie** na wschodzie oraz **ataki na Szlak Handlowy**.

*Uwaga:* Zburzenie każdego obozu wywołuje natychmiastowy kontratak z pobliskiego kierunku oraz lekko wzmacnia pozostałe siły Hordy (*Furia Hordy*).

### Rekomendowana kolejność celów wypraw (Wskazówka taktyczna)
1. **`Q1 Karawanseraj`** *(ok. `20–30 min`)* — buduje Mur Handlowy, daje **`+20%` szybkości pracy chłopów**, **`+30` populacji** i otwiera złoty handel przez całą mapę.
2. **`Q3 Skarbiec`** — zapewnia całej drużynie stały pasywny dochód **`+310` surowców/min na gracza** (`+100F, +100W, +90G, +20S` co minutę) i `+20` populacji.
3. **`G2 Akademia Inżynierów` oraz `G2 Klasztor Mrocznych Magów`** — **zburzenie `G2 Akademia` przed `54:00` całkowicie zapobiega obu Wyłomom Saperskim w lesie i wyłącza Moździerze!**, a zniszczenie `G2 Klasztor` wyłącza Imamów i Szakale.
4. **Najbliższy obóz `G1 Północ` lub `G1 Wschód` zostawcie na sam koniec** — dzięki temu po zburzeniu 6. obozu cała armia ma bardzo blisko pod Bramę Centralną na finałową walkę z Wielkim Chanem Subotaiem!

### 4 Questy Poboczne (`Q1–Q4`)
Każdy ukończony Quest daje stałe, potężne wzmocnienie całej drużynie (i lekko wzmacnia Hordę):
* **`Q1` Karawanseraj (południowy wschód):** Stawia długi Kamienny Mur Handlowy z 6 basztami i bramami wypadowymi oraz sojusznicze Targowisko w prawym dolnym rogu mapy. Daje **`+30` limitu populacji**, **+20% szybszą pracę wieśniaków**, +25% szybsze wozy handlowe, 4 darmowe wozy i +500 Złota dla każdego.
* **`Q2` Klif Artylerii (północny zachód — dwuetapowy):** Po obudzeniu garnizonu `Q2` włącza się tarcza regenerująca Uniwersytet (`+400 HP` co 2s), którą utrzymują **2 wysunięte Baszty Bombardowe** — zniszczcie je w pierwszej kolejności, a potem sam Uniwersytet. Nagroda: darmowa Balistyka, Chemia, Inżynierowie Oblężniczy i Thumb Ring, **`+2` zasięgu i `+4` ataku** dla wszystkich strzelców, **`+12%` prędkości i `+4` ataku** dla kawalerii, **`+12%` prędkości** dla konnych strzelców, **`2 Kolubryny`** dla Zielonego (`(27, 36)` i `(29, 36)`) oraz podgląd na obóz `G2 Akademia`.
* **`Q3` Skarbiec (wschód):** Daje **`+20` limitu populacji**, jednorazowo +600 Złota / +300 Kamienia oraz **stały dochód co minutę dla każdego gracza**: **`+100 Żywności, +100 Drewna, +90 Złota i +20 Kamienia`**.
* **`Q4` Krwawy Ołtarz (daleka północ — dwuetapowy):** Po zburzeniu Klasztoru wroga zabudowa obozu zapada się, w ruinach pojawia się Relikt, a z południa rusza odsiecz Zakonu (m.in. Elitarni Jeźdźcy Stepowi, Mamelucy i Wielbłądy) — trzeba **przetrwać 30 sekund Krwawego Odwetu**. Nagroda: **`+30% HP` i `+2/+2` pancerza** dla całej piechoty, jazdy i strzelców, **`+40%` szybsza produkcja wojska**, osłabienie wrogich Arcymagów do 120 HP oraz budowa **Wielkiego Klasztoru z `2` Mnichami** dla Niebieskiego na wyznaczonym placu `(58, 152)` (oznaczonym dwiema pochodniami — nie budujcie tam własnych budynków!).

### Warto zwiedzać mapę zwiadowcą!
Poza głównymi obozami na rubieżach ukryte są także trzy punkty eksploracyjne: **Opuszczony Obóz Inżynierów `(30, 76)`** przed północno-zachodnim lasem (odblokowywany w `10:00`), **Zaginiona Karawana `(124, 178)`** na wschodzie oraz **Kamień Wędrowca i Zwiadowcy `(50, 90)`** na północ od bazy (`2x Lekka Kawaleria`, `+150 Kamienia/+150 Złota` dla każdego oraz odsłonięcie brodu rzecznego `(122, 62)`). Pierwszy gracz, który wyśle tam zwiadowcę lub oddział, zgarnia bonus dla całej drużyny.

---

## 5. Groźni Przeciwnicy (Na kogo uważać w tłumie)

* **Arcymag Tarczy (Imam przed Bramą Centralną):** Najwyższy priorytet pod Bramą Centralną! Dopóki żyje w strefie przed Bramą Centralną (pokazuje go flara na mapie), nakłada na **swoją kolumnę `P7`** tarczę **`+8/+8` pancerza** (nie wzmacnia już pozostałych bram!) i mocno leczy wrogów wokół siebie (**`+25 HP / 3s`**). Zabijcie go jako pierwszego!
* **Szakale Dywersanci:** Bardzo szybka lekka jazda, która ignoruje walkę na murach i pędzi prosto pod nasze Town Center zabijać wieśniaków. Mają wysoki pancerz na strzały i zadają teraz **7 obrażeń** — chowajcie chłopów do TC i wybijajcie ich rycerzami lub pikinierami.
* **Moździerze Oblężnicze i Snajperzy:** Dalekosiężna artyleria typu *Glass Cannon* — Moździerze mają teraz tylko **70 HP** (bez skalowania HP!), pancerz **`0/3`**, zasięg **21**, martwą strefę 6 kratek w zwarciu, nie niszczą lasów przy bramach, a ich pociski lecą znacznie wolniej (**`3.2`**), więc można z nich unikać i łatwo dobić je kawalerią lub łucznikami! Snajperzy (zasięg **19**) wciąż biją mocno w pojedynczy cel.
* **Żelazne Słonie (1450 HP):** Olbrzymie żywe tarany o wysokim pancerzu i pełnej odporności na mnichów. Walcząc z żołnierzami zadają tylko po **3 obrażenia**, ale szybko niszczą mury i zamki (**`+140` obrażeń przeciw budynkom**) — najlepiej wybić najpierw ich eskortę, a potem otoczyć słonie halabardnikami.

---

## 6. Co zmieniło się po naszym pełnym 62-minutowym playteście co-op (`v7.0.3 -> v7.0.4`)?

1. **Więcej oddechu w late-game (rozrzedzenie Fal 7–14 i Endless co 10 min):** Od Fali 7 (`40:30`) do Fali 14 (`92:00`) fale są rozrzedzone z `5,5` do `6–8` minut, a Tryb Endless rusza o `102:00` co `10` minut (`600s`), dzięki czemu po odparciu szturmu mamy wreszcie czas wyjść z kontratakiem na obozy wroga i Questy.
2. **Brak OOS w `40:00` oraz twardy sufit eskalacji w `65:30`:** Przesunięto fazowo pętlę bram (`17s`) i Biegów Eskalacji (`+17s`), naprawiono nakładanie się trzech pętli eskalacji i dodano twardy wyłącznik w `65:30` (maks. **`+67 HP, +9 Ataku`**).
3. **2 minuty na reakcję przed wyłomami saperskimi:** Saperzy w Fali 9 (`54:00`) i Fali 12 (`76:00`) dają wczesny alarm z flarą już **2 minuty przed wycinką** (`52:00` i `74:00`), a przypomnienie na `30s` przed.
4. **Lokalny Imam i Moździerze *Glass Cannon*:** Aura pancerza Imama (`+8/+8`) działa już tylko na jego kolumnę `P7` pod Bramą Centralną (z mocniejszym leczeniem `+25 HP/3s` w tej strefie), a Moździerze mają **70 HP**, pancerz **`0/3`** i spowolnione pociski (`3.2`).
5. **Sprawdzone fundamenty z `v7.0.1–v7.0.3`:** Płynnie działające Sanktuarium Balansu `(4, 138)` i Kwatermistrz P2 `(4, 164)` (od `10:00` co 4 min z awansem `10–20m`, `20–30m`, `30m+`), Zegar Fali i `TL;DR` w zakładce **Objectives**, `PoI 1–3`, dwuetapowe `Q2/Q4` i 3-bramowy finał z Wielkim Chanem Subotaiem (`4500 HP`).

---

## 7. Finalne szlify przed rewanżem (`v7.0.4 -> v7.0.5 / Etap R16`)

1. **Wyraźne powiadomienia Kwatermistrza P2 (`240s`):** po każdym odnowieniu flag w komnacie `(4, 164)` na mapie pojawia się **flara**, Gracz 2 słyszy **dźwięk**, a na czacie wyświetla się wyróżniony komunikat `[KWATERMISTRZ P2 - GOTOWY!]`.
2. **Skalowanie Wyłomów Saperskich (`F9` i `F12`):** liczba jednostek w wyłomach w Fali 9 i Fali 12 skaluje się w 100% poziomem trudności Sanktuarium (`-2..+2`).
3. **Równomierniejsze tempo na Wschodzie (3. Rajd Handlowy w F13):** 3. uderzenie na Szlak Handlowy (`39` jedn.) zostało przeniesione z Fali 12 (`76:00`) do **Fali 13 (`84:00`)**, aby nie nakładało się na Wschodni Wyłom Saperski w F12.
4. **Arytmetyczne rozdzielenie wszystkich timerów (`02e`, `01d–01f`, `04c`/`04e`):** pętla bram `02e` startuje po `11 s` (`11 + 17k` s), badania AI przesunięto o `+23 s` (`8:53`, `18:23`, `34:53`), a przełączniki Biegów Eskalacji `04c`/`04e` na `35:18` (`2118 s`) i `55:18` (`3318 s`) — zero kolizji klatek.
5. **Czystszy finał z Wielkim Chanem (`07a` / `07b`):** w momencie zburzenia 6. Twierdzy wyłącza się aura Imama (ze zdjęciem aktywnej tarczy `+8/+8` z `P7`), morale Hordy słabnie (`P8` traci połowę Furii Settlementów: `-42 HP, -4 Ataku`), a strefa wykrywania Żelaznych Słoni leczących Chana obejmuje szerszy obszar `(15..140, 85..185)`.
