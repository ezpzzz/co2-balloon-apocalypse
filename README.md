# ☠️ CO₂ Balloon Apocalypse Simulator

Interactive visualization of the environmental impact of carbonated drinks, comparing daily global soda CO₂ emissions with cars and flights.

## 🌐 Live Demo

**GitHub Pages**: https://ezpzzz.github.io/co2-balloon-apocalypse/

## 📊 What it shows

- **Daily CO₂ from global soda consumption**: ~3,125 tonnes/day
- **Balloon visualization**: If all that CO₂ formed a balloon, it would be 145m diameter (26.4 giraffes tall!)  
- **Environmental comparison**: How soda emissions compare to 10M Toyota Camrys and 6,000 Boeing 737 flights
- **Hypothetical impact**: If the balloon burst over Hollywood, estimated kill radius and casualties

## 🔬 Science & Sources

All assumptions are interactive and based on real data:

- **Global soda volume**: 23.47 L/capita/year × 8.1B people (Statista 2024)
- **CO₂ per liter**: 6g/L industry average (CySoda)  
- **Car emissions**: 198 g/km for Toyota Camrys (AHG Auto Service)
- **Flight emissions**: 11.37t CO₂ per Boeing 737 flight (CarbonIndependent.org)
- **Lethality scaling**: Based on Lake Nyos disaster (1.6M tonnes, 25km radius, 1,746 deaths)

## 🛠️ Technologies

- **Frontend**: Pure HTML/CSS/JavaScript with Plotly.js
- **Backend version**: Python/Dash (see `app.py`)
- **Deployment**: GitHub Pages

## 🚀 Running locally

### Static version (GitHub Pages)
```bash
# Just open index.html in your browser
open index.html
```

### Python/Dash version
```bash
python3 -m venv venv
source venv/bin/activate
pip install dash plotly numpy
python app.py
# Visit http://localhost:8050
```

## 📈 Features

- **Interactive sliders** for all parameters
- **Real-time calculations** and visualizations  
- **Responsive design** works on mobile/desktop
- **Scientific transparency** with inline citations
- **Modular code structure** for easy modification

## 🎯 Educational Purpose

This simulator helps visualize:
- Scale of global consumption impacts
- Relative emissions between different sources
- How small daily habits aggregate globally
- Environmental data in accessible, memorable formats

*Note: This is an educational tool. The "apocalypse" scenario is hypothetical and based on scientific scaling from historical events.*