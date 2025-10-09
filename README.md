# Dashboard Latteria San Pietro - Simulatore Mini-Impianto Siero → Proteine

![Django](https://img.shields.io/badge/Django-5.2.6-green.svg)
![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple.svg)

## 📋 Descrizione del Progetto

Il **Dashboard Latteria San Pietro** è un'applicazione web sviluppata in Django per l'**Hackaton 2025** che simula e analizza la fattibilità economica di un mini-impianto per l'estrazione di proteine dal siero del latte.

### 🎯 Obiettivo

L'applicazione aiuta le latterie a prendere decisioni informate su due scenari principali:
1. **Acquisto di un impianto** per trasformare il siero in proteine di alta qualità
2. **Vendita diretta del siero** a terzi che dispongono già dell'impianto

### ✨ Funzionalità Principali

- **Simulazione economica** con calcolo di ROI, margini netti e ricavi
- **Analisi comparativa** tra scenario impianto e vendita siero
- **Sistema decisionale intelligente** basato su budget, spazio, personale e tempistiche
- **Interfaccia user-friendly** con dashboard interattiva e grafici dinamici
- **Calcoli automatici** con parametri predefiniti del settore lattiero-caseario

## 🏗️ Architettura del Sistema

### Modello Dati Principale

Il sistema si basa sul modello `SimulationInput` che gestisce:

```python
- volume_siero: Volume di siero disponibile (litri)
- capacita_investimento: Budget disponibile (€)
- costo_impianto: Costo fisso dell'impianto (€1.000.000)
- costi_operativi_annui: Costi annuali di gestione (€800.000)
- prezzo_vendita_proteine: Prezzo di vendita proteine (€50/kg)
- resa_proteine: Resa in kg proteine per litro siero (0.05 kg/L)
- prezzo_vendita_siero: Prezzo vendita siero diretto (€0.18/L)
- tempistiche: Tempi di implementazione (breve/media/lunga)
- spazio_disponibile: Metri quadri disponibili
- personale_disponibile: Disponibilità personale qualificato
```

### 📊 Algoritmi di Calcolo

#### Scenario Impianto:
```
kg_proteine = volume_siero × resa_proteine
ricavi_proteine = kg_proteine × prezzo_vendita_proteine
ammortamento_annuo = costo_impianto ÷ 10 anni
costi_totali = ammortamento_annuo + costi_operativi_annui
margine_netto = ricavi_proteine - costi_totali
ROI = (margine_netto ÷ costo_impianto) × 100
```

#### Scenario Vendita Siero:
```
ricavi_siero = volume_siero × prezzo_vendita_siero
costi_vendita = ricavi_siero × 0.10 (10% per gestione/trasporto)
margine_netto = ricavi_siero - costi_vendita
```

### 🧠 Logica Decisionale

Il sistema fornisce raccomandazioni basate su:

- **Budget rimanente** ≥ €500.000
- **Tempistiche** ≠ breve termine
- **Spazio disponibile** ≥ 50 m²
- **Personale qualificato** disponibile

## 🚀 Installazione e Setup

### Prerequisiti

- Python 3.8+
- pip (package manager Python)
- virtualenv (consigliato)

### Installazione

1. **Clona il repository:**
```bash
git clone https://github.com/Ednajm/Dashboard-Latteria-San-Pietro-Hackaton-2025.git
cd Dashboard-Latteria-San-Pietro-Hackaton-2025
```

2. **Crea un ambiente virtuale:**
```bash
python -m venv venv
source venv/bin/activate  # Su Linux/Mac
# oppure
venv\Scripts\activate     # Su Windows
```

3. **Installa le dipendenze:**
```bash
pip install django==5.2.6
```

4. **Configura il database:**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Crea un superuser (opzionale):**
```bash
python manage.py createsuperuser
```

6. **Avvia il server di sviluppo:**
```bash
python manage.py runserver
```

7. **Accedi all'applicazione:**
   - Apri il browser e vai su: `http://127.0.0.1:8000`

## 💻 Utilizzo dell'Applicazione

### 1. Input dei Parametri

Nella dashboard principale, inserisci:

- **Volume di siero disponibile** (in litri)
- **Capacità di investimento** (budget disponibile in €)
- **Tempistiche di implementazione** (breve/media/lunga)
- **Spazio disponibile** (metri quadri)
- **Disponibilità personale** qualificato

### 2. Analisi dei Risultati

L'applicazione genera automaticamente:

- **Confronto economico** tra i due scenari
- **Grafici interattivi** per visualizzare ricavi, costi e margini
- **Raccomandazione finale** basata sui parametri inseriti
- **Dettagli finanziari** completi per ogni scenario

### 3. Interpretazione delle Raccomandazioni

- 🟢 **Verde**: Consigliato acquisto impianto
- 🟡 **Giallo**: Acquisto possibile con limitazioni da risolvere
- 🔵 **Blu**: Consigliata vendita diretta del siero

## 🧪 Testing

### Esecuzione Test

```bash
# Test degli scenari predefiniti
python test_scenarios.py

# Test unitari Django
python manage.py test
```

### Scenari di Test Disponibili

Il file `test_scenarios.py` include tre scenari di test:

1. **Solo Scenario Impianto**: Calcolo con vendita proteine
2. **Solo Scenario Siero**: Calcolo con vendita siero diretta
3. **Scenario Combinato**: Analisi comparativa completa

## 📁 Struttura del Progetto

```
Dashboard-Latteria-San-Pietro-Hackaton-2025/
├── manage.py                 # Script principale Django
├── db.sqlite3               # Database SQLite
├── test_scenarios.py        # Script di test scenari
├── README.md               # Documentazione del progetto
├── dashboard/              # App principale
│   ├── models.py          # Modelli dati e logica business
│   ├── views.py           # Controller e logica applicazione
│   ├── forms.py           # Form per input utente
│   ├── urls.py            # URL routing
│   ├── admin.py           # Interfaccia amministrativa
│   ├── templates/         # Template HTML
│   │   └── dashboard/
│   │       ├── dashboard.html
│   │       └── test.html
│   └── migrations/        # Migrazioni database
├── siero_simulator/       # Configurazione progetto Django
│   ├── settings.py        # Configurazioni
│   ├── urls.py           # URL principali
│   └── wsgi.py           # WSGI configuration
└── static/               # File statici (CSS, JS, immagini)
    └── css/
        └── dashboard.css
```

## 🛠️ Tecnologie Utilizzate

- **Backend**: Django 5.2.6 (Python)
- **Frontend**: Bootstrap 5.3.0, HTML5, CSS3, JavaScript
- **Database**: SQLite3
- **Grafici**: Chart.js
- **Icone**: Font Awesome 6.4.0

## 📊 Parametri Economici del Settore

### Valori Predefiniti (basati su analisi di mercato):

- **Costo impianto mini-produzione**: €1.000.000
- **Costi operativi annui**: €800.000
- **Prezzo proteine WPC80**: €50/kg
- **Resa estrazione proteine**: 50g/litro siero
- **Prezzo siero di mercato**: €0.18/litro
- **Ammortamento impianto**: 10 anni
- **Costi distribuzione**: €15.000

## 👥 Contributi

Questo progetto è stato sviluppato per l'Hackaton 2025 della Latteria San Pietro.

### Team di Sviluppo
- Sviluppo backend e logica business
- Design interfaccia utente
- Analisi parametri economici del settore

## 📞 Supporto

Per domande, bug report o suggerimenti:

1. Apri una **Issue** su GitHub
2. Contatta il team di sviluppo
3. Consulta la documentazione in `/docs` (se disponibile)

## 📝 Licenza

Questo progetto è sviluppato per scopi educativi e di ricerca nell'ambito dell'Hackaton 2025.

---

**Sviluppato con ❤️ per l'innovazione nel settore lattiero-caseario**
