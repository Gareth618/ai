# recapitulare

- avem o imagine single-channel, mai precis o matrice $n \times n$ cu valori întregi între $0$ și $9$, unde valoarea $9$ apare exact o singură dată și reprezintă targetul nostru
- imaginile naturale nu conțin pixeli distribuiți random, ci în general aceștia formează diverși gradienți, de exemplu în paper avem gradienți liniari și circulari
- agentul trebuie să exploreze imaginea formând un path care merge cât de cât pe drumul indus de gradient și care la final atinge targetul
- la pasul curent, agentul poate vedea doar pe o anumită rază, stabilită de noi

# task-uri

- environment
  - generare de imagini random
  - generare de imagini cu gradienți circulari
  - afișare (de exemplu cu `pyplot`) a imaginii cu traseul ales (valorile între $0$ și $9$ trebuie mapate la culori reale, probabil alb-negru)
- agent
  - funcție care efectuează pasul curent cu $\epsilon$-greedy
  - funcție care face experience replay
- learning
  - execuția episoadelor
  - afișare de statistici
  - euristici de genul _hai să băgăm 3 frame-uri într-1 state_
- neural network
  - structura cu convoluții și chestii

# dileme

- trebuie să alegem niște dimensiuni (sau una singură) standard pentru imagini, că de mărimea imaginii depinde structura rețelei neuronale
- trebuie să vedem cum asignăm reward-uri fiecărui state, că scorul pentru drumul final se calculează ușor, dar pentru un singur pas cum facem??
  - ok, deocamdată am ales reward $1$ pentru orice pas și scorul final calculat ca în paper pentru pasul final, care ne duce la target
  - putem diminua rewardul $1$ pentru celulele pe care deja le-am vizitat
