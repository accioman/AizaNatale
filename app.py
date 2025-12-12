import numpy as np
import plotly.graph_objects as go
import streamlit as st

# ================== CONFIGURAZIONE ==================
st.set_page_config(page_title="Buon Natale, amore", page_icon="🎄", layout="centered")

# ================== TESTI PERSONALIZZABILI ==================
# QUI PUOI CAMBIARE IL TITOLO
TITOLO = "🎄 Buon Natale, amore mio! 🎁"
# QUI PUOI CAMBIARE IL SOTTOTITOLO
SOTTOTITOLO = "Una piccola scena 3D per ricordarti quanto ti voglio bene."
# MODIFICA QUI IL TESTO DEL TUO MESSAGGIO DI NATALE
MESSAGGIO = (
    "Che questa notte di Natale sia luminosa come le nostre speranze, "
    "dolce come i tuoi abbracci e calda come i nostri sogni insieme. "
    "Ti amo con tutto il cuore."
)

# ================== FUNZIONI DI SUPPORTO ==================
def crea_cono(z_offset: float, altezza: float, r_base: float, colore: str):
    """Crea una superficie conica per una "gonna" dell'albero."""
    theta = np.linspace(0, 2 * np.pi, 50)
    r = np.linspace(0, r_base, 20)
    T, R = np.meshgrid(theta, r)
    X = R * np.cos(T)
    Y = R * np.sin(T)
    Z = z_offset + altezza * (1 - R / r_base)
    surface = go.Surface(
        x=X,
        y=Y,
        z=Z,
        colorscale=[[0, colore], [1, colore]],
        showscale=False,
        opacity=0.98,
        lighting=dict(ambient=0.4, diffuse=0.7, specular=0.6, roughness=0.35),
        lightposition=dict(x=2000, y=1000, z=3000),
    )
    return surface

def crea_cilindro(z_offset: float, altezza: float, r: float, colore: str):
    """Crea un cilindro per il tronco."""
    theta = np.linspace(0, 2 * np.pi, 40)
    z = np.linspace(z_offset, z_offset + altezza, 2)
    T, Z = np.meshgrid(theta, z)
    X = r * np.cos(T)
    Y = r * np.sin(T)
    return go.Surface(
        x=X,
        y=Y,
        z=Z,
        colorscale=[[0, colore], [1, colore]],
        showscale=False,
        lighting=dict(ambient=0.3, diffuse=0.5, specular=0.4, roughness=0.6),
        lightposition=dict(x=1000, y=500, z=1000),
    )

def crea_sfera(centro, raggio, colore):
    """Crea una piccola sfera decorativa (es. puntale)."""
    u = np.linspace(0, 2 * np.pi, 20)
    v = np.linspace(0, np.pi, 20)
    x = centro[0] + raggio * np.outer(np.cos(u), np.sin(v))
    y = centro[1] + raggio * np.outer(np.sin(u), np.sin(v))
    z = centro[2] + raggio * np.outer(np.ones_like(u), np.cos(v))
    return go.Surface(
        x=x,
        y=y,
        z=z,
        colorscale=[[0, colore], [1, colore]],
        showscale=False,
        opacity=0.96,
        lighting=dict(ambient=0.5, diffuse=0.5, specular=0.8, roughness=0.3),
    )

def crea_base(raggio: float, colore: str, spessore: float = 0.02):
    """Crea un disco piatto che funge da pavimento/neve."""
    theta = np.linspace(0, 2 * np.pi, 60)
    r = np.linspace(0, raggio, 30)
    T, R = np.meshgrid(theta, r)
    X = R * np.cos(T)
    Y = R * np.sin(T)
    Z = np.full_like(X, -spessore)
    return go.Surface(
        x=X,
        y=Y,
        z=Z,
        colorscale=[[0, colore], [1, colore]],
        showscale=False,
        opacity=0.92,
        lighting=dict(ambient=0.8, diffuse=0.2, specular=0.05, roughness=0.9),
    )

def crea_regalo(centro, dimensione, colore_base, colore_top):
    """Crea un pacco regalo come piccolo cubo Mesh3d."""
    cx, cy, cz = centro
    d = dimensione / 2
    # Vertici del cubo
    vertices = np.array(
        [
            [cx - d, cy - d, cz - d],
            [cx - d, cy + d, cz - d],
            [cx + d, cy + d, cz - d],
            [cx + d, cy - d, cz - d],
            [cx - d, cy - d, cz + d],
            [cx - d, cy + d, cz + d],
            [cx + d, cy + d, cz + d],
            [cx + d, cy - d, cz + d],
        ]
    )
    # Facce del cubo
    i, j, k = (
        [0, 0, 0, 1, 1, 2, 4, 4, 5, 5, 6, 6],
        [1, 2, 3, 2, 5, 3, 5, 6, 6, 7, 7, 4],
        [2, 3, 1, 5, 2, 6, 6, 7, 7, 6, 4, 5],
    )
    return go.Mesh3d(
        x=vertices[:, 0],
        y=vertices[:, 1],
        z=vertices[:, 2],
        i=i,
        j=j,
        k=k,
        flatshading=True,
        color=colore_base,
        opacity=0.95,
        hoverinfo="skip",
        showscale=False,
        lighting=dict(ambient=0.6, diffuse=0.5, specular=0.3, roughness=0.4),
        lightposition=dict(x=800, y=1000, z=1200),
        facecolor=[
            colore_base,
            colore_base,
            colore_base,
            colore_base,
            colore_top,
            colore_top,
            colore_top,
            colore_base,
            colore_base,
            colore_base,
            colore_top,
            colore_top,
        ],
    )

def genera_palline(num_palline: int, rng: np.random.Generator):
    """Genera posizioni e colori per le palline sulle diverse "gonne"."""
    colori = ["crimson", "gold", "royalblue", "darkorange", "mediumseagreen"]
    z = rng.uniform(0.6, 2.1, num_palline)
    angoli = rng.uniform(0, 2 * np.pi, num_palline)
    r = np.maximum(0.2, 1.2 - z * 0.4)
    x = r * np.cos(angoli)
    y = r * np.sin(angoli)
    colori_scelti = rng.choice(colori, size=num_palline)
    return x, y, z, colori_scelti


def genera_luci(num_luci: int, rng: np.random.Generator):
    """Genera piccole lucine scintillanti sull'albero."""
    z = rng.uniform(0.5, 2.0, num_luci)
    angoli = rng.uniform(0, 2 * np.pi, num_luci)
    r = np.maximum(0.15, 1.0 - z * 0.35)
    x = r * np.cos(angoli)
    y = r * np.sin(angoli)
    return x, y, z


# ================== INTERFACCIA UTENTE ==================
st.title(TITOLO)
st.write(SOTTOTITOLO)

nome = st.text_input("Scrivi il nome della persona a cui vuoi fare gli auguri", "Amore")
st.markdown(f"### 💌 Per {nome}")
st.write(MESSAGGIO)

st.markdown("---")
st.subheader("Scena 3D di Natale")

num_palline = st.slider("Numero di palline colorate", min_value=20, max_value=140, value=70, step=5)
palline_size = st.slider("Dimensione media delle palline", min_value=4, max_value=14, value=8, step=1)
scala_altezza = st.slider("Altezza dell'albero", min_value=0.8, max_value=1.5, value=1.05, step=0.05)

# ================== SCENA 3D (ALBERO, REGALI, ECC.) ==================
fig = go.Figure()

# RNG con variazione per slider così ogni combinazione genera un layout leggermente diverso
rng_seed = 42 + num_palline + int(scala_altezza * 100)
rng = np.random.default_rng(rng_seed)

# Base innevata
fig.add_trace(crea_base(raggio=2.2, colore="snow"))

# Tronco
fig.add_trace(crea_cilindro(z_offset=-0.05, altezza=0.35, r=0.12, colore="saddlebrown"))

# Gonne dell'albero con gradienti di verde
livelli = [
    dict(z=0.25, h=1.0 * scala_altezza, r=1.2, color="#0b6623"),
    dict(z=0.55, h=0.8 * scala_altezza, r=0.95, color="#127b34"),
    dict(z=0.9, h=0.6 * scala_altezza, r=0.75, color="#1a9344"),
    dict(z=1.2, h=0.45 * scala_altezza, r=0.55, color="#25ad56"),
]
for livello in livelli:
    fig.add_trace(crea_cono(livello["z"], livello["h"], livello["r"], livello["color"]))

# Puntale/stellina con piccola sfera brillante
puntale_z = livelli[-1]["z"] + livelli[-1]["h"] + 0.12
fig.add_trace(crea_sfera((0, 0, puntale_z), raggio=0.06, colore="gold"))
fig.add_trace(
    go.Scatter3d(
        x=[0],
        y=[0],
        z=[puntale_z + 0.12],
        mode="markers",
        # Il simbolo "star" non è supportato in Scatter3d; usiamo un marker semplice e luminoso
        marker=dict(size=14, color="gold"),
        hoverinfo="skip",
    )
)

# Palline di Natale
x_p, y_p, z_p, colori_p = genera_palline(num_palline, rng)
fig.add_trace(
    go.Scatter3d(
        x=x_p,
        y=y_p,
        z=z_p * scala_altezza,
        mode="markers",
        marker=dict(
            size=rng.normal(loc=palline_size, scale=1.5, size=num_palline).clip(3, 16),
            color=colori_p,
            opacity=0.96,
            line=dict(width=0.6, color="rgba(255,255,255,0.6)"),
        ),
        hoverinfo="skip",
    )
)

# Lucine
x_l, y_l, z_l = genera_luci(num_luci=max(30, num_palline // 2), rng=rng)
fig.add_trace(
    go.Scatter3d(
        x=x_l,
        y=y_l,
        z=z_l * scala_altezza,
        mode="markers",
        marker=dict(size=3, color="lightgoldenrodyellow", opacity=0.9),
        hoverinfo="skip",
    )
)

# Pacchi regalo ai piedi dell'albero
posizioni_regali = [(-0.7, -0.4), (0.9, 0.3), (-0.4, 0.9), (0.6, -0.8)]
colori_regali = [
    ("indianred", "mistyrose"),
    ("royalblue", "skyblue"),
    ("seagreen", "honeydew"),
    ("darkviolet", "plum"),
]
for (xg, yg), (c_base, c_top) in zip(posizioni_regali, colori_regali):
    fig.add_trace(
        crea_regalo(
            centro=(xg, yg, 0.05),
            dimensione=rng.uniform(0.18, 0.26),
            colore_base=c_base,
            colore_top=c_top,
        )
    )

# Impostazioni scena
fig.update_layout(
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        aspectmode="manual",
        aspectratio=dict(x=1.2, y=1.2, z=1.8),
        camera=dict(eye=dict(x=1.4, y=1.4, z=1.45), projection=dict(type="perspective")),
        dragmode="orbit",
        bgcolor="rgba(0,0,0,0)",
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    uirevision="mobile-touch",
    hovermode=False,
)

plotly_config = {
    "displayModeBar": False,
    "responsive": True,
    "scrollZoom": True,  # pinza per zoomare su mobile
}

st.plotly_chart(fig, use_container_width=True, config=plotly_config)

# ================== FOOTER ==================
# Cambia il nome qui per personalizzare la firma
st.caption("Creata con ❤️ da [Il tuo nome]")
