# Scenariusz 3: Kroniki Rubieży — Horda i Ekspedycje (v6.6 — 4P Co-op RPG/RTS)

**Plik scenariusza:** `Kroniki_Rubiezy_Horda_Coop.aoe2scenario`  
**Typ rozgrywki:** Obrona przed 14 falami Hordy + Tryb Endless + Zegar Fali + Sanktuarium Balansu + 4 Questy poboczne i niszczenie 6 Settlementów (Grades 1–3)  
**Horyzont czasowy partii:** 60–90 minut  
**Rozmiar mapy:** 200×200 (Olbrzymia)  

---

## 1. Warunki uruchomienia w lobby i konfiguracja graczy (P1–P8)

W menu gry wybierz: **Multiplayer -> Host Game -> Game Mode: Custom Scenario (Niestandardowy scenariusz) -> `Kroniki_Rubiezy_Horda_Coop`**.

### Przypisanie slotów, drużyn i cywilizacji

W scenariuszu numery slotów i przypisane kolory ściśle determinują pozycję bazy, sektor obrony oraz mechaniki triggerów. **Gracze P5–P8 są już fabrycznie ustawieni w pliku scenariusza jako Komputer (AI) z narzuconymi i zablokowanymi cywilizacjami (`lock_civ = True`)**:

| Slot / Kolor | Typ gracza | Rola w scenariuszu i sektor obrony | Drużyna | Przypisana / Rekomendowana cywilizacja |
| :--- | :--- | :--- | :--- | :--- |
| **1 (Niebieski)** | **Człowiek** | **Mistrz Balansu i Obrońca Bramy Centralnej:** Kontroluje nieśmiertelnego Inżyniera Balansu (Króla na `6, 150`), broni podejścia pod Bramę Centralną `(104, 114)` przed atakiem Magów P7 i Tytanów P8; odpowiada za stałą wizję celów (stałe Revealers). Startuje z **2 domkami**. | **Drużyna 1** | **Bizancjum** (tanie kontry i wytrzymałe budynki pod napór w centrum), **Brytowie** (daleki zasięg łuków na Magów i Snajperów), **Teutoni**, **Czesi** |
| **2 (Czerwony)** | **Człowiek** | **Cytadela Sojuszu i Koordynator Handlu:** Chroni centralną Cytadelę Sojuszu (Feitoria na `54, 146` z +3000 HP — jej upadek to natychmiastowa porażka!). Startuje z **6 domkami** (+20 pop room kompensujące Feitorię od 0:00) oraz `+20` Bonus Pop Cap w 0:01. Zarządza Placem Targowym `(3..23, 177..198)` oraz sojuszniczym Marketem po Q1 `(195, 194)`. | **Drużyna 1** | **Hiszpanie** (**Kluczowy wybór!** Bonus drużynowy **+25% złota z handlu** na 190-kratkowym szlaku), **Portugalczycy**, **Frankowie**, **Burgundczycy** |
| **3 (Zielony)** | **Człowiek** | **Strażnik Przełęczy Północnej:** Broni Bramy Północnej `(48, 100)` przed szturmami Berserkerów P5 i Snajperów P6; zabezpiecza wyłom saperski w północnym lesie w Fali 9 (51:00); ma najbliżej do Q2 (Klif Artylerii). Startuje z **2 domkami**. | **Drużyna 1** | **Celtowie** (szybka piechota i machiny do kontrowania snajperów), **Goci** (masowa produkcja piechoty), **Polacy**, **Rzymianie** |
| **4 (Żółty)** | **Człowiek** | **Obrońca Skrzydła Wschodniego i Szlaku Handlowego:** Broni Bramy Wschodniej `(104, 162)` i Bramy Handlowej `(104, 193)`; odpiera natarcia ze Wschodu (G1/G3), chroni szlak handlowy przed rajdami od 45:00 oraz wschodni wyłom w lesie w Fali 12 (67:30); ma najbliżej do Q1. Startuje z **2 domkami**. | **Drużyna 1** | **Litwini** (Leitis przebijający pancerz Słoni-Tanków P8!), **Hindustańczycy** (wielbłądy na kawalerię i słonie), **Węgrzy**, **Saraceni** |
| **5 (Turkusowy)** | **Komputer (AI — narzucony w scenariuszu)** | **Awangarda Hordy (Szturmowcy, Berserkerzy i Saperzy):** Kontroluje Obozy G1 Północny `(76, 72)` i Wschodni `(132, 152)` oraz Q1 Karawanseraj `(154, 190)`. Wysyła Berserkerów, Huskarlów, Petardy, Płonące Wielbłądy, Tarany i Halabardników. | **Drużyna 2** | **Wikingowie (Vikings)** *(Zablokowana w scenariuszu — `lock_civ = True`)* |
| **6 (Fioletowy)** | **Komputer (AI — narzucony w scenariuszu)** | **Korpus Oblężniczy (Snajperzy Imperialni i Artyleria):** Kontroluje Obóz G2 Akademia Snajperów `(68, 34)` oraz Q2 Klif Artylerii `(28, 32)`. Wysyła Snajperów Imperialnych (zasięg 19), Moździerze Oblężnicze (zasięg 21, nie niszczące drzew) oraz Onagery wyrębujące lasy. | **Drużyna 2** | **Turcy (Turks)** *(Zablokowana w scenariuszu — `lock_civ = True`)* |
| **7 (Szary)** | **Komputer (AI — narzucony w scenariuszu)** | **Zakon Magów i Zagon Dywersyjny (Wsparcie i Eco-Raids):** Kontroluje Obóz G2 Klasztor Magów `(148, 72)` oraz Q4 Krwawy Ołtarz `(105, 20)`. Spawnuje Arcymaga Tarczy (Imam dający globalnie +30/+30 pancerza i lokalne leczenie) oraz Szakale Eco-Raiders polujące na wieśniaków pod TC. | **Drużyna 2** | **Saraceni (Saracens)** *(Zablokowana w scenariuszu — `lock_civ = True`)* |
| **8 (Pomarańczowy)**| **Komputer (AI — narzucony w scenariuszu)** | **Żelazny Legion i Cytadele Tytanów (Boss i Najcięższy Pancerz):** Kontroluje Cytadelę Północną `(142, 24)`, Cytadelę Wschodnią `(176, 56)` oraz Q3 Skarbiec Krasnoludów `(142, 118)` (Krepost). Wysyła Taran-Żółwie / Żelazne Słonie (1450 HP, niewrażliwe na mnichów dzięki Faith), Paladynów i rajdy na szlak handlowy od 45:00. | **Drużyna 2** | **Persowie (Persians)** *(Zablokowana w scenariuszu — `lock_civ = True`)* |

### Wymagane parametry pokoju (Lobby Settings)

* **Tryb gry (Game Mode):** **Niestandardowy scenariusz (Custom Scenario)** -> plik `Kroniki_Rubiezy_Horda_Coop`.
* **Poziom trudności AI w lobby (AI Difficulty):** **Ekstremalny (Extreme)** — **KRYTYCZNE!** AI w Age of Empires II na niższych poziomach trudności zachowuje się nieporadnie taktycznie. Ustawienie **Extreme** gwarantuje, że jednostki Hordy po otrzymaniu rozkazów ze skryptów sprawnie wybierają cele, nie blokują się i nie robią głupot podczas szturmu. Natomiast wielkością fal i statystykami Hordy steruje niezależnie **Sanktuarium Balansu na żywo w trakcie gry** (`6, 150`).
* **Widoczność mapy (Map Visibility):** **Normalna (Normal)** — Mgła Wojny jest aktywna. Nad środkiem każdego budynku Questu i Settlementu wisi stały odsłaniacz punktowy (`Map Revealer`, `LOS = 4`), dzięki czemu kluczowe cele strategiczne są stale widoczne i klikalne pod Mgłą Wojny, a pozostała część rubieży wymaga aktywnego zwiadu.
* **Limit populacji (Population Limit):** **200** — scenariusz dynamicznie zwiększa limity: Gracz 2 otrzymuje na start 6 domków (kompensacja 20 popu zajmowanego przez Feitorię w 0:00) oraz w 0:01 `+20` Bonus Pop Cap, zburzenie Q1 (Karawanseraj) daje stałe `+30` popu (limit 230), a zburzenie Q3 (Skarbiec Krasnoludów) daje kolejne `+20` popu (limit 250 dla całej drużyny!).
* **Zasoby i Wiek startowy (Starting Resources & Age):** **Domyślne / Standardowe (zdefiniowane w scenariuszu)** — gracze ludzcy P1–P4 startują z 500F, 600W, 400G, 300S, 6 chłopami, skautem oraz wybudowanymi domkami (~5 kratek na północ od krawędzi TC: 2 domki dla P1/P3/P4 i 6 domków dla P2). Graczom AI (P5–P8) scenariusz zeruje zasoby w 0:00 i automatycznie bada kolejne ery i technologie kowalskie w triggerach.
* **Zablokuj drużyny (Lock Teams):** **Wyłączone (Unchecked)** — krytyczne, aby trigger inicjalizujący (`01_Init_Diplomacy_And_Cartography`) mógł poprawnie skonfigurować i utrzymać sojusze P1–P4 oraz wrogość wobec P5–P8.
* **Prędkość gry (Game Speed):** **Normalna (1.7x)** (lub preferowana przez drużynę).
* **Zablokuj prędkość gry (Lock Speed):** **Włączone (Checked)** — zapobiega przypadkowej zmianie tempa w trakcie partii wieloosobowej.
* **Wszystkie technologie (All Techs):** **Wyłączone (Unchecked)** — unikalne drzewka technologiczne cywilizacji mają kluczowe znaczenie.
* **Dozwolone kody (Allow Cheats):** **Wyłączone (Unchecked)**.
* **Wskazówka strategiczna dotycząca cywilizacji:** Jeśli Gracz 2 (lub dowolny inny gracz) wybierze **Hiszpanów**, ich bonus drużynowy (**+25% złota z handlu**) w połączeniu ze 190-kratkowym szlakiem handlowym i Placem Targowym w lewym dolnym rogu generuje ogromne zasoby złota, niezbędne do utrzymania imperialnych armii w late-game.

---

## 2. Sanktuarium Balansu — Zmiana trudności na żywo w trakcie meczu `(6, 150)`

W zachodnim lesie Twierdzy `(6, 150)` znajduje się odizolowana skalnymi klifami komnata (poza szlakiem handlowym), w której stoi nieśmiertelny **Inżynier Balansu (Król Gracza 1)**:

* **Ruch Królem w GÓRĘ `(6, 146)` (Pochodnie Północne):** Zwiększa poziom trudności o **+1 stopień**.
* **Ruch Królem w DÓŁ `(6, 154)` (Pochodnie Południowe):** Zmniejsza poziom trudności o **-1 stopień**.
* **Automatyczny powrót, dynamiczny panel Objectives i logowanie:** Po wejściu na flagę Król jest natychmiast zatrzymywany rozkazem `stop_object` i teleportowany na środek komnaty `(6, 150)`. Aktualny poziom trudności wyświetla się na żywo w nagłówku panelu Celów (`order = 109`), a na czacie pojawia się wpis `[LOG BALANSU]`.
* **Brak blokad czasowych:** Zmiana poziomu trudności jest dostępna w każdym momencie gry (brak sztucznych timerów blokujących). Odwrócony porządek topologiczny triggerów w silniku AoE2 zabezpiecza przed wielokrotnym przeskokiem poziomu w jednym ticku. Wszystkie warianty fal, rajdy Szakali oraz szturmy na szlak handlowy są w 100% skalowane do wybranego poziomu trudności.
* **Gwarancja obecności jednostek specjalnych (`mandatory_min_one`):** Kluczowe jednostki oblężnicze i specjalne (Żelazne Słonie, Arcymagowie, Moździerze, Snajperzy, Berserkerzy, Kamikaze, Tarany) mają w rejestrze flagę `mandatory_min_one = True` — na poziomach `-1` i `-2` nigdy nie są redukowane poniżej `1` sztuki w grupie (redukcja liczebności odbywa się kosztem zwykłych jednostek w tej samej grupie; jeśli grupa składa się wyłącznie z pojedynczej jednostki obowiązkowej, zachowuje ona `1` szt.).
* **5 poziomów trudności (z odwracalnymi liczbami całkowitymi delty HP, bez kumulacyjnego dryfu):**
  * **Poziom `-2` (Bardzo Łatwy):** **-40% liczebności kolejnych fal** oraz **-30% HP** wroga (dwukrotność delty 15%).
  * **Poziom `-1` (Łatwy):** **-20% liczebności kolejnych fal** oraz **-15% HP** wroga (pojedyncza delta 15%).
  * **Poziom `0` (Domyślny):** **100% bazowej liczebności fal** i bazowe statystyki.
  * **Poziom `+1` (Trudny):** **+25% liczebności kolejnych fal** oraz **+15 HP i +2 Ataku** wroga.
  * **Poziom `+2` (Ekstremalny):** **+50% liczebności kolejnych fal** oraz **+30 HP i +4 Ataku** wroga.

---

## 3. Opis rozgrywki i układ Twierdzy Sojuszu

Wszyscy 4 gracze startują na równych warunkach (500 żywności, 600 drewna, 400 złota, 300 kamienia, 6 wieśniaków, 1 skaut oraz wybudowane domki na północ od TC) wewnątrz Twierdzy Sojuszu w południowo-zachodniej części mapy:

* **Domki startowe (~5 kafelków od północnej krawędzi TC):** Gracze P1, P3 i P4 rozpoczynają grę z **2 wybudowanymi domkami** (po północnej stronie TC, z dala od skupisk zasobów), dzięki czemu nikt nie jest „housed” w pierwszych sekundach gry. Gracz P2 rozpoczyna z **6 domkami**, które w 0:00 kompensują 20 populacji zajmowane przez pre-postawioną Feitorię.
* **Zegar Fali (Odliczanie w panelu Objectives):** Na samej górze panelu Celów (`order = 110`) wyświetla się na żywo licznik **`Zegar Fali: Fala X/14 za MM:SS`**, aktualizowany bezpiecznie co 30 sekund (zbudowany na statycznych banerach UI bez użycia podatnego na crashe silnika efektu `display_timer`). Dodatkowo na 1 minutę przed każdą falą (oraz 30 sekund przed Falą 1) pojawia się żółte ostrzeżenie na czacie.
* **Plac Handlowy Graczy w lewym rogu mapy `(3..23, 177..198)`:** W lewym dolnym narożniku bazy znajduje się duży, czysty plac o wymiarach 22×22 kratek — idealne miejsce na wybudowanie Targowisk wszystkich 4 graczy.
* **10-kratkowy korytarz handlowy na całej długości mapy (`y = 189..199`):** Od lewego rogu (`x = 2`) aż do prawego rogu mapy (`x = 199`) ciągnie się 10-kratkowy pas wolny od drzew i skał z brukowanym traktem na `y = 194`.
* **Wspólna wizja i stały podgląd celów (`LOS = 4`):** Wszyscy gracze mają od startu zbadaną **Kartografię**. Nad środkiem każdego budynku Questu i Settlementu wisi stały odsłaniacz (`4` kratki), dzięki czemu w każdej chwili można kliknąć na budynek zadania i sprawdzić jego opis pod Mgłą Wojny.
* **Cytadela Sojuszu (Feitoria Gracza 2):** W centrum Twierdzy `(54, 146)` stoi wzmocniona **Feitoria należąca do Gracza 2** (+3000 HP oraz +20 limitu populacji dla Gracza 2). Jej utrata oznacza porażkę drużyny.
* **Trzy przełęcze bojowe + Brama Handlowa:** Brama Północna `(48, 100)`, Centralna `(104, 114)`, Wschodnia `(104, 162)` oraz Południowa Brama Handlowa `(104, 193)` są zamknięte pełną **Wzmocnioną Palisadą (+400 HP)** z **Bramą Palisadową** i **2 Wieżami Strażniczymi**.
* **Działanie Mnichów:** Mnisi graczy (`P1–P4`) działają normalnie (leczą i konwertują zwykłe jednostki wroga). Mnisi komputerowi (`P5–P8`) mają zablokowaną konwersję, natomiast Arcymagowie (`P7`) leczą pobliskie jednostki Hordy obszarowo (+15 HP co 3s).

---

## 4. Harmonogram fal, eskalacja czasowa i taktyki specjalne

* **Harmonogram fal głównych (Fale 1–14):**
  * **Fala 1 (8:30):** Szturm Feudalny **bez taranów i bez jednostek specjalnych**.
  * **Fala 2 (13:00):** Szturm Feudalny **z pierwszym Taranem i Mangonelem oraz zwiadem na Bramę Centralną, bez jednostek specjalnych**.
  * **Fala 3 (18:00) i kolejne fale (4–14) co 5,5 minuty (330 sekund):** Stopniowy napływ elity i klas specjalnych (w Fali 3 na Bramę Centralną uderzają już Rycerze i Taran z obozu `G2_Mages`, a w Fali 4 dołącza pierwszy Arcymag Tarczy).
  * **Fala 14 (78:30):** Finałowy szturm kampanii z udziałem wszystkich aktywnych obozów, uzbrajający bramki Trybu Endless (`03_Endless_Gate_*`).
  * **Tryb Endless (od 84:00):** Cykliczne uderzenia co 330s generowane indywidualnie przez ocalałe Settlementy na bieżącym poziomie trudności (w tym dwuflankowe rajdy Szakali z Bramy Północnej i Wschodniej prosto w strefy ekonomiczne P3 i P4).
* **Trzystopniowa eskalacja czasowa (natychmiastowy 1. tick w minucie progowej i powtórzenie co 5 min):**
  * **20:00 (Bieg 1):** Pierwsza mobilizacja Hordy: **+5 HP i +1 Ataku** co 5 min.
  * **45:00 (Bieg 2):** Furia Late-Game: dodatkowo **+9 HP i +1 Ataku** co 5 min (łącznie **+14 HP i +2 Ataku** co 5 min).
  * **55:00 (Bieg 3):** Eskalacja Endgame: dodatkowo **+6 HP i +1 Ataku** co 5 min (łącznie **+20 HP i +3 Ataku** co 5 min).
* **Taktyki specjalne Hordy po 45. minucie:**
  * **Co druga fala od 45:00 (Fale 8, 10, 12, 14 i Endless) — Atak na Trade Line (zależny od `G3_East`):** Wydzielony korpus z Taranami Oblężniczymi, Paladynami i Konnymi Łucznikami spawnuje się na `(162, 180)` i uderza z rozkazem `attack_move` na `(96, 194)` (w lewo w stronę Bramy Handlowej `(104, 193)`, atakując mur Q1 lub korytarz handlowy i bazę graczy).
  * **Wyrąb lasu przez Saperów Oblężniczych (zależny od `G2_Snipers`, zapowiedziany alarmem i flarą na 15s przed falą):**
    * **Fala 9 (51:00):** Wrogie Onagery wycinają korytarz `6×11` kratek w **Północnym Lesie `(75, 95 .. 80, 105)`**, którym wchodzą Snajperzy Imperialni i Kusznicy P6.
    * **Fala 12 (67:30):** Wrogie Onagery wycinają korytarz `11×6` kratek we **Wschodnim Lesie `(99, 137 .. 109, 142)`**, którym wchodzą Snajperzy Imperialni i Kusznicy P6.

---

## 5. Bestiariusz Hordy — 6 wyspecjalizowanych klas jednostek (z Poświatą Bohatera)

| Jednostka specjalna (Od której minuty) | Rola i specjalizacja | Sposób pokonania / Kontra |
| :--- | :--- | :--- |
| **1. Taran-Żółw / Żelazny Słoń** *(od 34:30 — Słoń Bojowy P8)* | **Tank i Niszczyciel Budynków:** **1450 HP** (z korektą -20 HP po Bloodlines), prędkość **`0.72`**, **+10/+12 pancerza**, **odporny na konwersję**. Ma **+220 obrażeń przeciwko budynkom i murom**, ale zadaje **zawsze tylko 3 obrażenia jednostkom** (pełna odporność na buffy ataku z Kuźni, eskalacji i trudności)! | W walce z armią jest niegroźny — zignorujcie go, wybijcie resztę fali, a potem otoczcie Halabardnikami (+60 bonus dmg) zanim dojdzie do zamków. |
| **2. Szakale Dywersyjne** *(od 18:00 — Huzarzy P7)* | **Eco-Raiders:** Prędkość **`1.62`**, **+6 pancerza na strzały**, **zawsze tylko 2 ataku** (skalują wyłącznie HP). Wjeżdżają z rozkazem `MOVE` przez Bramę Północną lub Wschodnią prosto pod TC atakować chłopów (są wykluczone z globalnego `attack_move` na bramach bocznych)! | Schowajcie chłopów do TC i cofnijcie kilku rycerzy/pikinierów. |
| **3. Arcymag Tarczy** *(od 23:30 — Imam P7)* | **Globalny Support Hordy:** Gdy stoi w strefie `36×36` (promień 18 kratek wokół `110, 114`) przed Bramą Centralną `(104, 114)`, daje **GLOBALNIE +30/+30 Pancerza wszystkim armiom Hordy (P5–P8 na całej mapie)** oraz **LOKALNIE leczy (+15 HP/3s)** jednostki Hordy w tej strefie `36×36`! | Ma złotą poświatę, flarę co 8s, **240 HP**, **3/4 pancerza** i **regenerację 5 HP/s**. Automat dwustanowy: zabicie Imama przed bramą natychmiast zdejmuje tarczę z całej Hordy. |
| **4. Moździerz Oblężniczy** *(od 29:00 — Onager P6)* | **Artyleria Dalekosiężna:** **350 HP**, prędkość **`0.58`**, **21 zasięgu**, **+75 ataku**, promień wybuchu **2,6 kratki**. Pociski mają **`Blast Attack Level = 2`** (nie ścinają drzew wokół bram). | **Martwa strefa 6 kratek (`Minimum Range = 6`)** oraz strzał raz na **10 s**. Bezbronny w zwarciu. |
| **5. Snajperzy Imperialni** *(od 18:00 — Janczarzy P6)* | **Egzekutor pojedynczych celów:** **90 HP**, **19 zasięgu**, **+85 ataku** (~107 dmg w jeden cel). | Strzelają co **6,5 s** — zasypcie ich grupą tanich jednostek lub dojedźcie kawalerią. |
| **6. Berserkerzy i Kamikaze** *(od 18:00 — P5)* | **Szturmowcy i Saperzy:** Szybcy (`1.40–1.50`), wysoki atak wręcz / wybuch obszarowy `2,4`. | **0 pancerza przeciw strzałom** — wycinajcie ich łucznikami i kusznikami zanim dobiegną. |

---

## 6. Cztery Questy poboczne (Q1–Q4) i Adaptacja Hordy

Każdy ukończony Quest powoduje spektakularne zawalenie się pobocznych wież i budynków obozu (`kill_object` w promieniu `±14`), zapewnia potężne, stałe wzmocnienie dla wszystkich 4 graczy, ale wywołuje również **Adaptację Hordy** (niewielki wzrost HP i ataku wrogich jednostek w rejestrze):

1. **`Q1 - Karawanseraj (Mur Handlowy, +30 Pop, +20% Eko)` `(154, 190)`:**
   * Po zburzeniu usuwa wrogie wieże strażnicze P5, stawia **Kamienny Mur Obronny na `y = 186` z dwoma 2-kratkowymi otworami wypadowymi (`x = 122..123` oraz `x = 170..171`) osłoniętymi Basztami `KEEP` na `y = 184`** oraz **pojedyncze sojusznicze Targowisko w prawym rogu mapy `(195, 194)`**.
   * W połączeniu z Waszym placem na Targowiska w lewym rogu bazy `(3..23, 177..198)` daje to maksymalny szlak handlowy przez całą szerokość mapy (190 kratek!).
   * Daje **+30 Limit Populacji na stałe** (`230 pop`), **+20% szybszą pracę Wieśniaków**, **+25% szybsze Wozy Handlowe**, 4 darmowe Wozy i +500 Złota dla każdego gracza.
   * *Adaptacja Hordy:* **+8 HP i +1 Ataku**.
2. **`Q2 - Klif Artylerii (+2 Zasiegu, +4 Ataku, Szybkosc)` `(28, 32)`:**
   * Darmowa Balistyka, Chemia, Inżynierowie Oblężniczy i Thumb Ring.
   * **+2 Zasięgu i +4 Ataku** dla wszystkich strzelców graczy (w tym jednostek unikalnych i regionalnych: `Longbowman`, `Chu Ko Nu`, `Mangudai`, `War Wagon`, `Plumed Archer`, `Conquistador`, `Genoese Crossbowman`, `Camel Archer`, `Rattan Archer`, `Kipchak`, `Composite Bowman`, `Imperial Skirmisher`, `Elephant Archer`, `Genitour`, `Slinger`, `Janissary`, `Arambai`, `Chakram Thrower`, `Ratha`).
   * **+12% prędkości i +4 Ataku** dla całej kawalerii graczy (w tym `Savar`, `War Elephant`, `Shrivamsha Rider`, `Camel Scout`, `Ratha`, `Elite Steppe Lancer`, `Heavy/Imperial Camel Rider`, `Battle Elephant` oraz jednostek unikalnych: `Cataphract`, `Leitis`, `Boyar`, `Tarkan`, `Magyar Huszar`, `Konnik`, `Keshik`, `Coustillier`, `Monaspa`, `Centurion`, `Winged Hussar`) oraz **+12% prędkości** dla konnych jednostek dystansowych (`Cavalry Archer`, `Mangudai`, `Camel Archer`, `Kipchak`, `Conquistador`, `War Wagon`, `Elephant Archer`, `Genitour`, `Arambai`, `Ratha`).
   * *Adaptacja Hordy:* **+8 HP i +1 Ataku**.
3. **`Q3 - Skarbiec Krasnoludów (+20 Pop i Duzy Staly Dochod)` `(142, 118)`:**
   * **+20 Limit Populacji na stałe** (`250 pop`) oraz jednorazowo +600 Złota i +300 Kamienia dla każdego gracza.
   * Stały dochód surowcowy co minutę **dla każdego z 4 graczy (`P1–P4`)**: **+250 Żywności, +250 Drewna, +200 Złota i +40 Kamienia co 60s**.
   * *Adaptacja Hordy:* **+10 HP i +1 Ataku**.
4. **`Q4 - Krwawy Ołtarz (+30% HP Armii i +40% Produkcji)` `(105, 20)`:**
   * **+30% Max HP i +2/+2 Pancerza** dla całej piechoty, jazdy i strzelców graczy (w tym `Militia`, `Legionary`, `Serjeant`, `Flemish Militia`, linia `Eagle Warrior` oraz wszystkie jednostki unikalne piechoty, jazdy i strzelców, takie jak `Teutonic Knight`, `Huskarl`, `Woad Raider`, `Obuch`, `Ghulam`, `Samurai`, `Berserk`, `Jaguar Warrior`, `Kamayuk`, `Condottiero`).
   * **+40% szybsza produkcja wojska** we wszystkich budynkach militarnych (Koszary, Stajnie, Strzelnice, Zamki, Warsztaty Oblężnicze, `Krepost` oraz `Donjon`).
   * Obniżenie Max HP wrogich Arcymagów do **120 HP**.
   * *Adaptacja Hordy:* **+10 HP i +1 Ataku**.

---

## 7. Sześć Settlementów Hordy i Gradacja Furii (Stopnie 1–3)

Zburzenie każdego Settlementu powoduje natychmiastowe zawalenie się pobocznych zamków, wież i budynków koszarowych obozu (`kill_object` w promieniu `±14`), trwale wycofuje jego oddziały z kolejnych fal 1–14 oraz z Trybu Endless, deaktywuje jego garnizony i smycze terytorialne, nagradza drużynę surowcami oraz wywołuje natychmiastowy kontratak (z bramy odpowiadającej kierunkowi obozu: Północnej, Centralnej lub Wschodniej) i wzmocnienie pozostałych obozów zależne od stopnia obozu (**Grade 1–3**):

* **Grade 1 (Obozy zewnętrzne — nagroda `+700 Żywności i +700 Złota`, Furia `+5 HP i +0 Ataku`):**
  * **`G1 - Północny` `(76, 72)`:** usuwa Berserkerów i Petardy. Kontratak (Brama Północna): `8x Cavalier + 10x Pikeman`. Furia: **+5 HP i +0 Ataku** (tylko wzrost HP, bez wzrostu ataku!) dla pozostałych wrogów.
  * **`G1 - Wschodni` `(132, 152)`:** usuwa Huskarlów i Płonące Wielbłądy. Kontratak (Brama Wschodnia): `8x Cavalier + 10x Pikeman`. Furia: **+5 HP i +0 Ataku**.
* **Grade 2 (Obozy wyspecjalizowane — nagroda `+1000 Żywności i +1000 Złota`, Furia `+10 HP i +1 Ataku`):**
  * **`G2 - Akademia Snajperów` `(68, 34)`:** usuwa Snajperów, Moździerze Oblężnicze oraz wyłomy Saperów w Fali 9, 12 i Endless. Kontratak (Brama Północna): `10x Cavalier + 12x Halberdier`. Furia: **+10 HP i +1 Ataku**.
  * **`G2 - Klasztor Magów` `(148, 72)`:** usuwa Arcymagów i Szakale. Kontratak (Brama Centralna): `10x Cavalier + 12x Halberdier`. Furia: **+10 HP i +1 Ataku**.
* **Grade 3 (Główne Cytadele Hordy — nagroda `+1500 Żywności i +1500 Złota`, Furia `+15 HP i +2 Ataku`):**
  * **`G3 - Cytadela Północna` `(142, 24)`:** usuwa Taran-Żółwie / Żelazne Słonie z natarcia północnego. Kontratak (Brama Centralna): **`1x Żelazny Słoń + 12x Paladin + 14x Halberdier`**. Furia: **+15 HP i +2 Ataku**.
  * **`G3 - Cytadela Wschodnia` `(176, 56)`:** usuwa Taran-Żółwie / Żelazne Słonie z natarcia wschodniego oraz rajdy na Szlak Handlowy w Falach 8, 10, 12, 14 i Endless. Kontratak (Brama Wschodnia): **`1x Żelazny Słoń + 12x Paladin + 14x Halberdier`**. Furia: **+15 HP i +2 Ataku**.

**Warunek Zwycięstwa:** Zniszczenie wszystkich 6 Settlementów kończy scenariusz natychmiastowym zwycięstwem graczy!
