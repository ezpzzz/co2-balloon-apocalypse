"""
CO₂ Balloon Apocalypse Simulator – v2 · August 2025
Author: ChatGPT (OpenAI o3)

How to run:
    $ python app.py
"""

import math
from textwrap import dedent

import dash
from dash import dcc, html, Output, Input
import plotly.graph_objects as go
import numpy as np

# --------------------------------------------------------------------------------------
# 1. SCIENCE LAYER ----------------------------------------------------------------------
# --------------------------------------------------------------------------------------

WORLD_POP = 8.1e9                     # people
GIRAFFE_HT = 5.5                      # m
LA_DENSITY = 6000                     # people / km² (Hollywood / DTLA core)

def soda_emissions(litres_per_capita_yr: float, g_co2_per_l: float) -> dict:
    """Return daily mass (t) and gas‑volume (m³) of CO₂ from global soda consumption."""
    daily_litres = (WORLD_POP * litres_per_capita_yr) / 365
    daily_g = daily_litres * g_co2_per_l
    daily_t = daily_g / 1e6
    moles = daily_g / 44
    volume_m3 = moles * 0.0224        # STP molar volume
    return {"t": daily_t, "m3": volume_m3}

def car_emissions(n_cars: int, miles_per_day: float, g_co2_mile: float) -> float:
    """Tonnes CO₂ per day for a fleet of identical cars."""
    return n_cars * miles_per_day * g_co2_mile / 1e6

def flight_emissions(n_flights: int, t_co2_per_flight: float) -> float:
    """Tonnes CO₂ per day for scheduled flights."""
    return n_flights * t_co2_per_flight

def sphere_diameter(volume_m3: float) -> float:
    """Return diameter (m) of a sphere containing the given volume."""
    r = (3 * volume_m3 / (4 * math.pi)) ** (1/3)
    return 2 * r

def lethal_radius(daily_t: float, nyos_mass_t=1.6e6, nyos_radius_km=25) -> float:
    """Nyos cube‑root scaling for kill radius from CO₂ ground‑hugging plume."""
    return nyos_radius_km * (daily_t / nyos_mass_t) ** (1/3)

def victim_estimate(kill_r_km: float, density=LA_DENSITY, lethality=0.35) -> int:
    area = math.pi * kill_r_km**2      # km²
    return int(area * density * lethality)

# --------------------------------------------------------------------------------------
# 2. DASH LAYER -------------------------------------------------------------------------
# --------------------------------------------------------------------------------------

app = dash.Dash(__name__, title="CO₂ Balloon Apocalypse Simulator v2")

def header(title):
    return html.H3(title, style={"marginTop": "1.2em", "marginBottom": "0.4em"})

app.layout = html.Div(
    style={"maxWidth": "900px", "margin": "auto", "fontFamily": "sans-serif"},
    children=[

    html.H1("☠️ CO₂ Balloon Apocalypse Simulator", style={"textAlign": "center"}),

    # ---------- CONTROLS ----------
    header("Editable assumptions"),
    html.Div([
        html.Label("Soda volume per capita (L/year)"),
        dcc.Slider(id="lpc", min=5, max=50, step=0.1, value=23.47,
                   tooltip={"placement": "bottom"}),

        html.Label("CO₂ dissolved per litre of soda (g/L)"),
        dcc.Slider(id="gpl", min=2, max=10, step=0.1, value=6),

        html.Label("Toyota Camrys (fleet size)"),
        dcc.Slider(id="cars", min=1e6, max=20e6, step=1e6, value=10e6,
                   marks={i*1e6:f"{i} M" for i in range(1,21)}),

        html.Label("Miles driven per Camry per day"),
        dcc.Slider(id="miles", min=5, max=100, step=1, value=30),

        html.Label("Boeing 737 flights per day"),
        dcc.Slider(id="flights", min=1000, max=10000, step=100, value=6000),
    ], style={"columnCount": 2, "gap": "20px"}),

    # ---------- LIVE METRICS ----------
    header("Daily snapshot"),
    html.Div(id="metrics", style={"fontSize": "18px", "lineHeight": "1.8em"}),

    # ---------- GRAPHS ----------
    html.Div([
        dcc.Graph(id="bar"),
        dcc.Graph(id="polar")
    ]),

    html.Footer(dedent("""
        Sources: Statista (per‑capita soda volume) · CySoda (CO₂ per can) · Toyota Environmental Metrics
        (tailpipe g/km) · CarbonIndependent.org (B737 fuel burn). All figures can be overridden above.
        """), style={"fontSize": "12px", "marginTop": "2em"})
])

# ---------- CALLBACK ----------
@app.callback(
    [Output("metrics", "children"),
     Output("bar", "figure"),
     Output("polar", "figure")],
    [Input("lpc", "value"),
     Input("gpl", "value"),
     Input("cars", "value"),
     Input("miles", "value"),
     Input("flights", "value")]
)
def update(lpc, gpl, cars, miles, flights):

    soda = soda_emissions(lpc, gpl)
    car_t = car_emissions(cars, miles, 318)           # 318 g/mi from 198 g/km
    flight_t = flight_emissions(flights, 11.37)

    dia = sphere_diameter(soda["m3"])
    giraffes = dia / GIRAFFE_HT
    kill_r = lethal_radius(soda["t"])
    deaths = victim_estimate(kill_r)

    # ------- METRIC TEXT -------
    block = html.Div([
        html.P(f"🌍 Daily soda CO₂: **{soda['t']:.0f} t** → {soda['m3']:.0f} m³"),
        html.P(f"🎈 Balloon diameter: **{dia:,.0f} m**  ({giraffes:.1f} giraffes)"),
        html.P(f"💀 If burst over Hollywood: kill radius **{kill_r:.1f} km**, "
               f"≈ {deaths:,} potential deaths"),
    ])

    # ------- BAR CHART -------
    bar = go.Figure(go.Bar(
        x=["Soda", "10 M Camrys", "6 000 B737s"],
        y=[soda["t"], car_t, flight_t],
        text=[f"{soda['t']:.0f} t", f"{car_t:,.0f} t", f"{flight_t:,.0f} t"],
        textposition="outside"
    )).update_layout(
        yaxis_title="Tonnes CO₂ per day",
        title="Daily CO₂ Emissions Comparison",
        uniformtext_minsize=8, uniformtext_mode='show'
    )

    # ------- POLAR / KILL ZONE -------
    polar = go.Figure(go.Scatterpolar(
        r=[0, kill_r],
        theta=[0, 0],
        mode="lines",
        fill="toself",
        name="Lethal CO₂ Zone",
        line=dict(width=2)
    )).update_layout(
        polar=dict(radialaxis=dict(range=[0, kill_r+1], visible=True)),
        showlegend=False,
        title="Projected ground‑level kill radius (center = Hollywood Blvd)"
    )

    return block, bar, polar

# --------------------------------------------------------------------------------------
# 3. MAIN -------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=False)