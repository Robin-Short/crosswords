# Crossword Generator

Lo scopo di questo lavoro è di generare delle parole crociate a partire da uno _scheletro_ (una matrice con alcune celle 
nere e le altre bianche) e da un _dizionario_ (con le parole come chiavi e le definizioni come definizioni).

## Approcci
### Competitive
Ispirati da algoritmi genetici e competitivi, l'idea è quella di modificare una configurazione localmente in un ciclo 
infinito sperando di giungere a convergenza. La competitività deriva dalla scelta di adoperare due agenti **H** e **V** 
che si occupano rispettivamente delle modifiche delle parole **orizzontali** e **verticali**. In questo approccio va
decisa, ad ogni iterazione, il **turno** e la **mossa**: facciamo questo secondo un'euristica.
Questo è quello che abbiamo provato a fare in `generator1.py`.
Ad ore i risultati non sono soddisfacenti.

### Brute Force
Detto `N` il numero di celle bianche e `A` il numero di lettere dell'alfabeto (tipicamente 26), la taglia dello spazio 
da esplorare è di `A^N`, e quindi inaccessibile.

L'unica speranza è quella di fare un buon _pruning_ unito ad un _ordine di esplorazione_ euristicamente sensato.

Abbiamo deciso di inserire ad ogni chiamata ricorsiva delle parole appartenenti al dizionario, restringendo così 
notevolmente lo spazio esplorabile. Detti `NH` ed `NV` il numero di mosse rispettivamente orizzontali e verticali che vanno 
fatte per riempire uno scheletro, una configurazione è determinata da `NH + NV` scelte successive, esplorando quindi uno
spazio di dimensione `D^(NH + NV)`. Tipicamente `N` è quadratico in `(NH + NV)`.

Questo è quello che abbiamo provato a fare in `generator2.py`.

### Randomic
Anche qui si vuole esplorare lo spazio delle configurazioni ma lo si vuole fare probabilisticamente. Usando le stesse 
euristiche dell'approccio **_brute force_** vogliamo esplorare tale spazio seguendo una distribuzione di probabilità 
verosimilmente concentrate sulle soluzioni.

Questo è quello che abbiamo provato a fare in `generator3.py` (TO DO).
