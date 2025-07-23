import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Carica i dati dal file CSV
data = pd.read_csv('/Users/giulio_bucchi/Desktop/c++/Collisione/dati_satelliti.csv')
x1, y1, z1 = data['x1'], data['y1'], data['z1']
x2, y2, z2 = data['x2'], data['y2'], data['z2']
distanza = data['distanza']

# Imposta la figura e l'asse 3D
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Traccia le orbite complete (trasparente)
ax.plot(x1, y1, z1, 'b--', alpha=0.4, linewidth=1, label="Orbita Satellite 1")
ax.plot(x2, y2, z2, 'r--', alpha=0.4, linewidth=1, label="Orbita Satellite 2")

# Inizializza i punti per i satelliti e le loro traiettorie
sat1_point, = ax.plot([], [], [], 'bo', markersize=8, label="Satellite 1")
sat2_point, = ax.plot([], [], [], 'ro', markersize=8, label="Satellite 2")
traj1, = ax.plot([], [], [], 'b-', alpha=0.7, linewidth=2)
traj2, = ax.plot([], [], [], 'r-', alpha=0.7, linewidth=2)

# Punto di collisione (se presente)
distanza_min_idx = np.argmin(distanza)
if distanza.iloc[distanza_min_idx] < 5:  # se c'è una collisione entro 5 km
    ax.plot([x1.iloc[distanza_min_idx]], [y1.iloc[distanza_min_idx]], [z1.iloc[distanza_min_idx]], 
            'y*', markersize=15, label="Punto di avvicinamento massimo")

# Configurazione assi
ax.set_xlabel('X [km]')
ax.set_ylabel('Y [km]')
ax.set_zlabel('Z [km]')
ax.set_title('Simulazione Collisione Satelliti in Orbita Terrestre')
ax.legend()

# Imposta limiti degli assi per una vista equilibrata
max_range = max(np.max(np.abs(x1)), np.max(np.abs(y1)), np.max(np.abs(z1)),
                np.max(np.abs(x2)), np.max(np.abs(y2)), np.max(np.abs(z2)))
ax.set_xlim([-max_range, max_range])
ax.set_ylim([-max_range, max_range])
ax.set_zlim([-max_range, max_range])

# Testo per mostrare informazioni dinamiche ( si trova in alto a sinistra)
info_text = ax.text2D(0.02, 0.98, "", transform=ax.transAxes, fontsize=10, 
                      verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# Testo per messaggio di collisione (grande e centrale)
collision_text = ax.text2D(0.5, 0.5, "", transform=ax.transAxes, fontsize=14, fontweight='bold',
                          horizontalalignment='center', verticalalignment='center',
                          bbox=dict(boxstyle='round', facecolor='red', alpha=0.9),
                          color='white')

# Inizializzazione
def init():
    sat1_point.set_data([], [])
    sat1_point.set_3d_properties([])
    sat2_point.set_data([], [])
    sat2_point.set_3d_properties([])
    traj1.set_data([], [])
    traj1.set_3d_properties([])
    traj2.set_data([], [])
    traj2.set_3d_properties([])
    info_text.set_text("")
    collision_text.set_text("")
    return sat1_point, sat2_point, traj1, traj2, info_text, collision_text

# Aggiorna ogni frame
def update(frame):
    if frame >= len(x1):
        frame = len(x1) - 1
    
    # Satellite 1
    sat1_point.set_data([x1.iloc[frame]], [y1.iloc[frame]])
    sat1_point.set_3d_properties([z1.iloc[frame]])
    
    # Satellite 2
    sat2_point.set_data([x2.iloc[frame]], [y2.iloc[frame]])
    sat2_point.set_3d_properties([z2.iloc[frame]])
    
    # Traiettorie (mostra ultimi 20 punti per effetto scia)
    start_idx = max(0, frame - 20)
    traj1.set_data(x1.iloc[start_idx:frame+1], y1.iloc[start_idx:frame+1])
    traj1.set_3d_properties(z1.iloc[start_idx:frame+1])
    traj2.set_data(x2.iloc[start_idx:frame+1], y2.iloc[start_idx:frame+1])
    traj2.set_3d_properties(z2.iloc[start_idx:frame+1])
    
    # Informazioni dinamiche
    tempo_ore = data['tempo'].iloc[frame] / 3600
    dist_km = distanza.iloc[frame]
    altitudine1 = np.sqrt(x1.iloc[frame]**2 + y1.iloc[frame]**2 + z1.iloc[frame]**2) - 6371
    altitudine2 = np.sqrt(x2.iloc[frame]**2 + y2.iloc[frame]**2 + z2.iloc[frame]**2) - 6371
    
    info_text.set_text(f'Tempo: {tempo_ore:.2f} ore\n'
                      f'Distanza: {dist_km:.2f} km\n'
                      f'Alt. Sat1: {altitudine1:.0f} km\n'
                      f'Alt. Sat2: {altitudine2:.0f} km')
    
    #MESSAGGIO DI COLLISIONE 
    if dist_km < 2000.0:  # Soglia semplice e alta
        if dist_km < 500.0:
            collision_text.set_text(" COLLISIONE! ")
            collision_text.set_bbox(dict(boxstyle='round,pad=1', facecolor='red', alpha=0.9))
            collision_text.set_color('white')
            
            sat1_point.set_color('yellow')
            sat2_point.set_color('yellow')
            
            sat1_point.set_markersize(12)
            sat2_point.set_markersize(12)
            
        elif dist_km < 800.0:
            collision_text.set_text(" PERICOLO! ")
            collision_text.set_bbox(dict(boxstyle='round,pad=0.8', facecolor='orange', alpha=0.8))
            collision_text.set_color('black')
            
            sat1_point.set_color('orange')
            sat2_point.set_color('orange')
            
        else:
            collision_text.set_text(" ATTENZIONE ")
            collision_text.set_bbox(dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))
            collision_text.set_color('black')
            
            sat1_point.set_color('darkorange')
            sat2_point.set_color('darkorange')
    else:
        collision_text.set_text("")
        collision_text.set_bbox(dict(boxstyle='round', facecolor='none', alpha=0))
        # Ripristina colori normali
        sat1_point.set_color('blue')
        sat2_point.set_color('red')
        sat1_point.set_markersize(8)
        sat2_point.set_markersize(8)
        
    return sat1_point, sat2_point, traj1, traj2, info_text, collision_text

# Crea animazione - IMPORTANTE: usa blit=False per i grafici 3D
ani = FuncAnimation(
    fig, update, frames=len(x1),
    init_func=init, blit=False, interval=20, repeat=True
)

plt.tight_layout()
plt.show()

# Salva animazione come GIF
print("Salvando animazione...")
ani.save("orbita_collisione.gif", writer='pillow', fps=20)