import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(page_title="Newton avec Frottements", layout="centered")
st.title("🪂 Impact des Frottements sur la Trajectoire")
st.write("Cette simulation compare le modèle idéal (sans frottement) au modèle réel avec frottement de l'air.")

# Barre latérale pour les paramètres
st.sidebar.header("Conditions Initiales")
v0 = st.sidebar.slider("Vitesse initiale v0 (m/s) :", 5.0, 40.0, 20.0, 0.5)
alpha = st.sidebar.slider("Angle de tir α (degrés) :", 0, 90, 45, 1)

st.sidebar.header("Paramètre de l'air")
f = st.sidebar.slider("Coefficient de frottement fluide (f) :", 0.0, 0.5, 0.1, 0.01)

# Paramètres physiques fixes
g = 9.81
m = 1.0  # Masse normalisée pour simplifier
alpha_rad = np.radians(alpha)

# Résolution numérique temporelle (car l'équation avec frottement n'est plus une parabole simple)
dt = 0.01
t = np.arange(0, 10, dt)

# --- 1. CAS SANS FROTTEMENT (Idéal) ---
x_ideal = v0 * np.cos(alpha_rad) * t
y_ideal = -0.5 * g * t**2 + v0 * np.sin(alpha_rad) * t
# On ne garde que les points au-dessus du sol
ideal_mask = y_ideal >= 0
x_ideal = x_ideal[ideal_mask]
y_ideal = y_ideal[ideal_mask]

# --- 2. CAS AVEC FROTTEMENT (Modèle fluide : F = -f*v) ---
x_frot = [0.0]
y_frot = [0.0]
vx = v0 * np.cos(alpha_rad)
vy = v0 * np.sin(alpha_rad)

x_actuel = 0.0
y_actuel = 0.0

for _ in t:
    # Calcul des accélérations (2ème loi de Newton : a = g - (f/m)*v)
    ax = -(f / m) * vx
    ay = -g - (f / m) * vy
    
    # Mise à jour des vitesses (Méthode d'Euler)
    vx += ax * dt
    vy += ay * dt
    
    # Mise à jour des positions
    x_actuel += vx * dt
    y_actuel += vy * dt
    
    if y_actuel < 0: # Arrêt si le projectile touche le sol
        break
        
    x_frot.append(x_actuel)
    y_frot.append(y_actuel)

# --- TRACÉ DU GRAPHIQUE ---
fig, ax = plt.subplots(figsize=(10, 5))

# Courbe théorique idéale
ax.plot(x_ideal, y_ideal, color='#3182ce', linewidth=2, linestyle='--', label="Modèle idéal (Sans frottement)")
# Courbe avec frottements
ax.plot(x_frot, y_frot, color='#e53e3e', linewidth=2.5, label=f"Modèle réel (Avec frottement f={f})")

# Habillage
ax.set_title("Comparaison des trajectoires avec et sans frottement de l'air", fontsize=11, fontweight='bold')
ax.set_xlabel("Distance horizontale x (m)", fontsize=10)
ax.set_ylabel("Altitude y (m)", fontsize=10)
ax.grid(True, linestyle=':', alpha=0.6)
ax.set_xlim(0, max(x_ideal[-1], 5.0) * 1.05)
ax.set_ylim(0, max(max(y_ideal), 5.0) * 1.1)
ax.legend()

st.pyplot(fig)

# Bilan pédagogique dynamique
st.subheader("💡 Observations pour les élèves :")
portee_perdue = ((x_ideal[-1] - x_frot[-1]) / x_ideal[-1]) * 100 if x_ideal[-1] > 0 else 0
st.write(f"• **Portée idéale :** {x_ideal[-1]:.1f} m | **Portée réelle :** {x_frot[-1]:.1f} m")
if f > 0:
    st.warning(f"⚠️ À cause des frottements de l'air, le projectile perd **{portee_perdue:.0f}%** de sa portée maximale !")
    st.info("📉 **Asymétrie :** Remarquez que la phase de descente est plus raide (la courbe s'écrase) que la phase de montée. La trajectoire n'est plus une parabole symétrique.")
