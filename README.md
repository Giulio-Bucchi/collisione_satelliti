# Simulatore di Collisione Satelliti  🛰️

https://github.com/user-attachments/assets/8a9848fe-eced-49ac-b3b9-1931cfb7a5eb

## Descrizione del Progetto

Questo progetto simula il movimento di due satelliti in orbita terrestre e visualizza la loro traiettoria, prevedendo potenziali collisioni. Il simulatore è composto da:

Un programma C++ che calcola le orbite e le posizioni relative dei satelliti
Uno script Python che visualizza l'animazione 3D delle traiettorie

## Funzionalità Principali

Simulazione fisica accurata del moto orbitale
Rilevamento automatico di collisioni e avvicinamenti pericolosi
Visualizzazione 3D interattiva delle traiettorie
Indicatori visivi per diversi livelli di pericolo
Registrazione della distanza minima tra i satelliti

## Requisiti di Sistema

Compilatore C++ (g++ o equivalente)
Python 3.x
Librerie Python richieste:
```bash
  pip install pandas matplotlib numpy
```
## Clonare il repository:
```bash
git clone https://github.com/tuoutente/simulatore-collisioni-satelliti.git
cd simulatore-collisioni-satelliti
```

Compilare il programma C++:
```bash
g++ Satellite.cpp -o Satellite_sim
```
Eseguire il simulatore C++ per generare i dati:
```bash
./satellite_simulator
```
Generare l'animazione con Python:
```bash
python Grafico.py
```
Configurazione della Simulazione

È possibile modificare i parametri iniziali dei satelliti nel file Satellite.cpp:

```bash
// Esempi di configurazioni preimpostate:
// Collisione frontale:
Satellite sat1 = {7000, 0, 0, 0, v_orb, 0};
Satellite sat2 = {7000, 100, 0, 0, -v_orb * 0.98, 0};

// Collisione per raggiungimento:
Satellite sat1 = {7000, 0, 0, 0, v_orb, 0};
Satellite sat2 = {6950, 0, 0, 0, v_orb * 1.05, 0};

// Avvicinamento senza collisione:
Satellite sat1 = {7000, 0, 0, 0, v_orb, 0};
Satellite sat2 = {6900, 500, 0, 0.5, v_orb * 1.02, 0};
```


# Il programma genera:

Un file CSV (dati_satelliti.csv) con le traiettorie dei satelliti
Un'animazione GIF (orbita_collisione.gif) della simulazione
Personalizzazione.
Nello script Python Grafico.py è possibile modificare:

Soglie di allarme per collisione
Aspetto grafico dell'animazione
Durata e velocità dell'animazione

```bash
# Soglie di allarme (in km)
if dist_km < 2000.0:  # Modifica questo valore
    # ... codice di avviso ...

# Aspetto grafico
ax.plot(x1, y1, z1, 'b--', alpha=0.4)  # Colore/trasparenza orbite

# Durata animazione
ani = FuncAnimation(fig, update, frames=len(x1), interval=20)  # Modifica interval

```
