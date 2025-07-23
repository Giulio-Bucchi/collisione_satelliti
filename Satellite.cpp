#include <iostream>
#include <cmath>
#include <fstream>

// Costanti fisiche
const double G = 6.67430e-11;                                      // Costante gravitazionale (m³/kg·s²)
const double M_TERRA = 5.972e24;                                   // Massa della Terra (kg)
const double R_TERRA = 6371.0;                                     // Raggio della Terra (km)


struct Satellite {

    double x,y,z;                                                   // posizione iniziali in km
    double vx, vy, vz;                                              // velocità iniziali in km/s

   
    
    // Aggiorna posizione e velocità considerando la gravità
    void aggiornare_posizione(double dt) {
        // Distanza dal centro della Terra
        double r = std::sqrt(x*x + y*y + z*z);
        
        // Conversione in metri per i calcoli gravitazionali
        double r_m = r * 1000.0;
        
        // Accelerazione gravitazionale (in m/s²)
        double g_mag = G * M_TERRA / (r_m * r_m);
        
        // Componenti dell'accelerazione (direzione verso il centro)
        double ax = -g_mag * (x / r) / 1000.0; 
        double ay = -g_mag * (y / r) / 1000.0;
        double az = -g_mag * (z / r) / 1000.0;
        
        // Aggiorna velocità
        vx += ax * dt;
        vy += ay * dt;
        vz += az * dt;
        
        // Aggiorna posizione
        x += vx * dt;
        y += vy * dt;
        z += vz * dt;
    }
};


void visualizza_posizione( const Satellite & sat, double t){

    std::cout<<"tempo : " << t << " s -> Posizione : " << sat.x << " , "<< sat.y <<" , "<< sat.z << " km\n ";
}

double calcola_distanza(const Satellite& a, const Satellite& b) {
    return std::sqrt(
        std::pow(b.x - a.x, 2) +
        std::pow(b.y - a.y, 2) +
        std::pow(b.z - a.z, 2)
    );
}

// Calcola la velocità orbitale per un'orbita circolare
double velocita_orbitale(double altitudine_km) {
    double r_m = (R_TERRA + altitudine_km) * 1000.0;
    return std::sqrt(G * M_TERRA / r_m) / 1000.0; 
}

int main() {

    //double angolo = M_PI/6;

    double altitudine = 629.0;                                     // Stessa altitudine per entrambi
    double v_orb = velocita_orbitale(altitudine);

    /*. 
            
            Collisione frontale :
            Satellite sat1 = {7000, 0, 0, 0, v_orb, 0};           // orbita standard
            Satellite sat2 = {7000, 100, 0, 0, -v_orb * 0.98, 0}; // orbita opposta, leggermente più lenta

            Collisione per raggiungimento : 
            Satellite sat1 = {7000, 0, 0, 0, v_orb, 0};           // orbita standard
            Satellite sat2 = {6950, 0, 0, 0, v_orb * 1.05, 0};    // stessa orbita ma più veloce

            Collisione per intercettazione : 
            Satellite sat1 = {7000, 0, 0, 0, v_orb, 0};           // orbita equatoriale
            Satellite sat2 = {7000, 50, 0, 0, v_orb * 0.95, 0.1}; // orbita inclinata più lenta

            Avvicinamento ma non collisione : 
            Satellite sat1 = {7000, 0, 0, 0, v_orb, 0};     
            Satellite sat2 = {6900, 500, 0, 0.5, v_orb * 1.02, 0};  
    */

    Satellite sat1 = {7000, 0, 0, 0, v_orb, 0};                 // orbita equatoriale
    Satellite sat2 = {6900, 500, 0, 0.5, v_orb * 1.02, 0};      // orbita inclinata 
    
    double dt = 20.0;                                           // passo temporale in secondi
    double T = 7200.0;                                          // 2 ore di simulazione
    
    double distanza_minima = 1e9;
    double distanza_soglia = 1.0;                               // 1 km per collisione
    
    std::ofstream file("dati_satelliti.csv");
    file << "tempo,x1,y1,z1,x2,y2,z2,distanza\n";
    
    bool collisione_rilevata = false;
    
    std::cout << "=== SIMULAZIONE COLLISIONE SEMPLICE ===" << std::endl;
    std::cout << "Satellite 1: posizione (7000, 0, 0), velocità (0, 5, 0) km/s" << std::endl;
    std::cout << "Satellite 2: posizione (7000, 50, 0), velocità (0, -5, 0) km/s" << std::endl;
    std::cout << "Collisione prevista in circa 5 secondi!" << std::endl << std::endl;
    
    
    for (double t = 0; t <= T; t += dt) {
        double distanza = calcola_distanza(sat1, sat2);
        
        // Stampa ogni secondo per vedere l'avvicinamento
        std::cout << "t=" << t << "s: Sat1(" << sat1.x << "," << sat1.y << ") "
                  << "Sat2(" << sat2.x << "," << sat2.y << ") "
                  << "Distanza=" << distanza << " km" << std::endl;
        
        if (distanza < distanza_minima) {
            distanza_minima = distanza;
        }
        
        if (distanza < distanza_soglia && !collisione_rilevata) {
            std::cout << "\n. COLLISIONE RILEVATA! " << std::endl;
            std::cout << "Tempo: " << t << " secondi" << std::endl;
            std::cout << "Distanza finale: " << distanza << " km" << std::endl;
            collisione_rilevata = true;
        }
        
        // Salva tutti i dati per l'animazione
        file << t << ","
             << sat1.x << "," << sat1.y << "," << sat1.z << ","
             << sat2.x << "," << sat2.y << "," << sat2.z << ","
             << distanza << "\n";
        
        sat1.aggiornare_posizione(dt);
        sat2.aggiornare_posizione(dt);
    }
    
    file.close();
    
    std::cout << "Distanza minima raggiunta: " << distanza_minima << " km\n";
    std::cout << "Simulazione completata. Dati salvati in dati_satelliti.csv\n";
    
    return 0;
}