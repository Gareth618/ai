# Team
Dima Elisabeta, Florea Bogdan, Jinga Andreea, Oleniuc Iulian, Tomescu Mihai

# Contributions
- AI Agent and NN: Dima Elisabeta, Oleniuc Iulian
- Environment: Jinga Andreea, Tomescu Mihai
- Training: Florea Bogdan
- Testing: everybody
 
# Video presentation
https://www.youtube.com/playlist?list=PLqtRfUCC8StaPgSLI6wnQX4bzQ5Qsi_VD

# Statistics
Number of steps needed to reach the target vs. shortest path improvement over time
![steps](https://user-images.githubusercontent.com/76652381/214874904-0c2cf7cc-7b13-492f-9339-8cb8380319e2.png)

Reward convergence over time and slight decrease on the long run while using one neural network
![rewards](https://user-images.githubusercontent.com/76652381/214875318-c9e592ad-6cac-43da-9643-01d6296f9ae8.png)


# Description
- avem o imagine single-channel, mai precis o matrice $n \times n$ cu valori întregi între $0$ și $9$, unde valoarea $9$ apare exact o singură dată și reprezintă targetul nostru
- imaginile naturale nu conțin pixeli distribuiți random, ci în general aceștia formează diverși gradienți, de exemplu în paper avem gradienți liniari și circulari
- agentul trebuie să exploreze imaginea formând un path care merge cât de cât pe drumul indus de gradient și care la final atinge targetul
- la pasul curent, agentul poate vedea doar pe o anumită rază, stabilită de noi

# Tasks
- environment
  - generare de imagini random
  - generare de imagini cu gradienți circulari
  - afișare (de exemplu cu `pyplot`) a imaginii cu traseul ales (valorile între $0$ și $10$ trebuie mapate la culori reale, probabil alb-negru, unde $10$ reprezintă valoare pixelilor din afara matricei)
- agent
  - funcție care efectuează pasul curent cu $\epsilon$-greedy
  - funcție care face experience replay
- learning
  - execuția episoadelor
  - afișare de statistici
  - euristici de genul _hai să băgăm 3 frame-uri într-1 state_
- neural network
  - structura cu convoluții și chestii
