from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
import json
import logging
from decimal import Decimal, InvalidOperation
from .forms import SimulationForm
from .models import SimulationInput

logger = logging.getLogger(__name__)

def dashboard_view(request):
    """View principale della dashboard - semplificata e robusta"""
    
    # Debug: stampa sempre i dati POST per controllo
    if request.method == 'POST':
        print("=== DEBUG DATI RICEVUTI ===")
        print("request.POST:", dict(request.POST))
        print("Headers AJAX:", request.headers.get('X-Requested-With'))
        print("========================")
    
    form = SimulationForm()
    simulation_data = None
    
    if request.method == 'POST':
        # Validazione manuale dei dati per controllo completo
        errors = []
        
        # Estrai i dati dal POST
        volume_siero = request.POST.get('volume_siero', '').strip()
        capacita_investimento = request.POST.get('capacita_investimento', '').strip()
        costo_impianto = request.POST.get('costo_impianto', '').strip()
        costi_operativi = request.POST.get('costi_operativi_annui', '').strip()
        prezzo_proteine = request.POST.get('prezzo_vendita_proteine', '').strip()
        resa_proteine = request.POST.get('resa_proteine', '').strip()
        prezzo_siero = request.POST.get('prezzo_vendita_siero', '').strip()
        costo_distribuzione = request.POST.get('costo_distribuzione', '').strip()
        tempistiche = request.POST.get('tempistiche', '').strip()
        spazio_disponibile = request.POST.get('spazio_disponibile', '').strip()
        personale_disponibile = request.POST.get('personale_disponibile', '').strip()
        
        # Valida che i campi variabili siano presenti
        if not volume_siero:
            errors.append("Volume siero è obbligatorio")
            
        # I campi fissi vengono impostati automaticamente se vuoti
        if not costo_impianto:
            costo_impianto = "150000"  # Valore fisso
        if not costi_operativi:
            costi_operativi = "25000"  # Valore fisso  
        if not prezzo_proteine:
            prezzo_proteine = "8.50"  # Valore fisso
        if not resa_proteine:
            resa_proteine = "7"  # Valore fisso
        if not costo_distribuzione:
            costo_distribuzione = "10000"  # Valore fisso
        if not prezzo_siero:
            prezzo_siero = "0.50"  # Valore fisso
            
        print("INFO: Tutti i valori ora sono fissi")
            
        # Se mancano dati per uno scenario, usa valori di default per confronto
        # Questo permette di mostrare sempre entrambi i grafici per comparazione
        if not prezzo_proteine and prezzo_siero:
            print("INFO: Solo scenario siero fornito, userò valori di default per confronto")
        if not prezzo_siero and prezzo_proteine:
            print("INFO: Solo scenario impianto fornito, userò valori di default per confronto")
        
        # Converte e valida che siano numerici
        numeric_values = {}
        if not errors:  # Solo se non ci sono errori di campi mancanti
            try:
                numeric_values['volume_siero'] = float(volume_siero.replace(',', '.'))
                if numeric_values['volume_siero'] <= 0:
                    errors.append("Volume siero deve essere maggiore di 0")
            except (ValueError, TypeError):
                errors.append("Volume siero deve essere un numero valido")
                
            # Validazione capacità investimento (opzionale)
            if capacita_investimento:
                try:
                    numeric_values['capacita_investimento'] = float(capacita_investimento.replace(',', '.'))
                    if numeric_values['capacita_investimento'] < 0:
                        errors.append("Capacità investimento non può essere negativa")
                except (ValueError, TypeError):
                    errors.append("Capacità investimento deve essere un numero valido")
            else:
                numeric_values['capacita_investimento'] = 0
                
            # Valori fissi - sempre gli stessi
            numeric_values['costo_impianto'] = 1000000.0
            numeric_values['costi_operativi'] = 800000.0
            numeric_values['prezzo_proteine'] = 50.0
            numeric_values['resa_proteine'] = 0.05  # Valore fisso 0.05 kg/L (50g/L)
            numeric_values['prezzo_siero'] = 0.18  # Valore fisso €0.50/L
            numeric_values['costo_distribuzione'] = 15000.0  # Valore fisso
            
            # Validazione spazio disponibile (obbligatorio)
            if spazio_disponibile:
                try:
                    numeric_values['spazio_disponibile'] = float(spazio_disponibile.replace(',', '.'))
                    if numeric_values['spazio_disponibile'] < 0:
                        errors.append("Spazio disponibile non può essere negativo")
                except (ValueError, TypeError):
                    errors.append("Spazio disponibile deve essere un numero valido")
            else:
                errors.append("Spazio disponibile è obbligatorio")
            
            # Campi di selezione (non numerici)
            numeric_values['tempistiche'] = tempistiche
            numeric_values['personale_disponibile'] = personale_disponibile
        
        # Se ci sono errori, restituisci messaggio di errore
        if errors:
            error_msg = "Errori di validazione: " + "; ".join(errors)
            print("ERRORI VALIDAZIONE:", error_msg)
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': error_msg
                })
            else:
                messages.error(request, error_msg)
        else:
            # Controllo capacità di investimento vs costo impianto (messaggio informativo)
            investimento_sufficiente = False
            messaggio_investimento = ""
            
            if numeric_values['capacita_investimento'] >= 500000:
                if numeric_values['capacita_investimento'] >= numeric_values['costo_impianto']:
                    investimento_sufficiente = True
                    messaggio_investimento = "✅ È possibile acquistare l'impianto di filtrazione per ottenere le proteine dal siero del latte!"
                    print("INFO INVESTIMENTO:", messaggio_investimento)
                else:
                    differenza = numeric_values['costo_impianto'] - numeric_values['capacita_investimento']
                    messaggio_investimento = f"⚠️ Budget insufficiente per l'impianto. Mancano €{differenza:,.2f}"
                    print("INFO INVESTIMENTO:", messaggio_investimento)
            # Tutti i dati sono validi, procedi con i calcoli
            try:
                print("=== CALCOLI ===")
                print("Dati numerici validati:", numeric_values)
                
                # Calcoli basati sui dati inseriti
                volume = numeric_values['volume_siero']
                
                # CALCOLA SEMPRE ENTRAMBI GLI SCENARI
                # Ora i valori impianto sono fissi, solo siero può variare
                
                # SCENARIO IMPIANTO (valori fissi)
                volume = numeric_values['volume_siero']
                kg_proteine = volume * numeric_values['resa_proteine']  # 0.05 kg/L (50g/L)
                ricavi_impianto = kg_proteine * numeric_values['prezzo_proteine']  # €50/kg
                
                ammortamento_annuo = numeric_values['costo_impianto'] / 10  # €1.000.000 / 10 anni
                costi_impianto = ammortamento_annuo + numeric_values['costi_operativi'] + numeric_values['costo_distribuzione'] + 900000  # Ammortamento + operativi + distribuzione + extra

                margine_impianto = ricavi_impianto - costi_impianto
                roi_impianto = (margine_impianto / numeric_values['costo_impianto']) * 100
                
                scenario_impianto = {
                    'ricavi': round(ricavi_impianto, 2),
                    'costi': round(costi_impianto, 2),
                    'margine_netto': round(margine_impianto, 2),
                    'roi': round(roi_impianto, 2),
                    'kg_proteine': round(kg_proteine, 2),
                    'is_user_data': True  # Sempre presente
                }
                
                # SCENARIO SIERO 
                default_prezzo_siero = 0.5  # €/litroSS
                prezzo_siero_calc = numeric_values['prezzo_siero'] or default_prezzo_siero
                ricavi_siero = volume * prezzo_siero_calc
                costi_siero = numeric_values['costo_distribuzione']
                margine_siero = ricavi_siero - costi_siero
                
                scenario_siero = {
                    'ricavi': round(ricavi_siero, 2),
                    'costi': round(costi_siero, 2),
                    'margine_netto': round(margine_siero, 2),
                    'roi': 0,  # Nessun investimento
                    'is_user_data': bool(numeric_values['prezzo_siero'])
                }
                
                # Calcoli derivati
                payback_years = None
                if scenario_impianto['margine_netto'] > 0:
                    payback_years = numeric_values['costo_impianto'] / scenario_impianto['margine_netto']
                
                # LOGICA DECISIONALE - Crea oggetto temporaneo per calcoli
                temp_simulation = SimulationInput(
                    volume_siero=numeric_values['volume_siero'],
                    capacita_investimento=numeric_values['capacita_investimento'],
                    costo_impianto=numeric_values['costo_impianto'],
                    costi_operativi_annui=numeric_values['costi_operativi'],
                    costo_distribuzione=numeric_values['costo_distribuzione'],
                    tempistiche=numeric_values['tempistiche'],
                    spazio_disponibile=numeric_values['spazio_disponibile'],
                    personale_disponibile=numeric_values['personale_disponibile']
                )
                
                # Calcola il messaggio decisionale
                messaggio_decisionale = temp_simulation.calcola_messaggio_decisionale()
                
                # Preparazione dati per grafici - SEMPRE ENTRAMBI
                # Impianto sempre presente (valori fissi), siero opzionale
                user_scenario_type = 'both' if numeric_values['prezzo_siero'] else 'impianto_with_default_siero'
                
                simulation_data = {
                    'success': True,
                    'scenario_type': 'both',  # Mostra sempre entrambi per confronto
                    'user_scenario_type': user_scenario_type,  # Quello che l'utente ha effettivamente inserito
                    'input_data': {
                        'volume_siero': volume,
                        'capacita_investimento': numeric_values['capacita_investimento'],
                        'costo_impianto': numeric_values['costo_impianto'],
                        'costi_operativi_annui': numeric_values['costi_operativi'],
                        'prezzo_vendita_proteine': numeric_values['prezzo_proteine'],
                        'resa_proteine': numeric_values['resa_proteine'],
                        'prezzo_vendita_siero': numeric_values['prezzo_siero'],
                        'costo_distribuzione': numeric_values['costo_distribuzione'],
                        'tempistiche': numeric_values['tempistiche'],
                        'spazio_disponibile': numeric_values['spazio_disponibile'],
                        'personale_disponibile': numeric_values['personale_disponibile'],
                    },
                    'scenario_impianto': scenario_impianto,
                    'scenario_siero': scenario_siero,
                    'defaults_used': {
                        'prezzo_proteine': not bool(numeric_values['prezzo_proteine']),
                        'resa_proteine': not bool(numeric_values['resa_proteine']),
                        'prezzo_siero': not bool(numeric_values['prezzo_siero'])
                    },
                    'investimento_info': {
                        'capacita_disponibile': numeric_values['capacita_investimento'],
                        'costo_richiesto': numeric_values['costo_impianto'], 
                        'sufficiente': investimento_sufficiente,
                        'messaggio': messaggio_investimento,
                        'differenza': numeric_values['costo_impianto'] - numeric_values['capacita_investimento'] if numeric_values['capacita_investimento'] > 0 else 0
                    },
                    'messaggio_decisionale': messaggio_decisionale
                }
                
                # Comparazione (solo se entrambi gli scenari esistono)
                if scenario_impianto and scenario_siero:
                    simulation_data['comparazione'] = {
                        'differenza_ricavi': round(scenario_impianto['ricavi'] - scenario_siero['ricavi'], 2),
                        'differenza_costi': round(scenario_impianto['costi'] - scenario_siero['costi'], 2),
                        'differenza_margine': round(scenario_impianto['margine_netto'] - scenario_siero['margine_netto'], 2)
                    }
                
                # KPI (calcolati in base al tipo di scenario)
                kpi_data = {}
                if scenario_impianto:
                    kpi_data['roi_impianto'] = scenario_impianto['roi']
                    kpi_data['payback_years'] = round(payback_years, 2) if payback_years else 999
                    if numeric_values['resa_proteine']:
                        kpi_data['efficienza_conversione'] = numeric_values['resa_proteine']
                    
                    # Distribuzione costi impianto
                    ammortamento_annuo = numeric_values['costo_impianto'] / 10
                    simulation_data['distribuzione_costi'] = {
                        'ammortamento': round(ammortamento_annuo, 2),
                        'operativi': round(numeric_values['costi_operativi'], 2),
                        'distribuzione': round(numeric_values['costo_distribuzione'], 2),
                        'totale': round(ammortamento_annuo + numeric_values['costi_operativi'] + numeric_values['costo_distribuzione'], 2)
                    }
                
                if scenario_impianto and scenario_siero:
                    kpi_data['valore_aggiunto_per_litro'] = round((scenario_impianto['ricavi'] - scenario_siero['ricavi']) / volume, 4)
                    
                simulation_data['kpi'] = kpi_data
                
                # Trend quinquennale (basato sui scenari disponibili)
                trend_data = []
                for anno in range(1, 6):
                    trend_item = {'anno': anno}
                    
                    if scenario_impianto:
                        trend_item['ricavi_impianto'] = round(scenario_impianto['ricavi'] * anno, 2)
                        trend_item['margine_impianto'] = round(scenario_impianto['margine_netto'] * anno, 2)
                        trend_item['costi_impianto'] = round(scenario_impianto['costi'] * anno, 2)
               
                    if scenario_siero:
                        trend_item['ricavi_siero'] = round(scenario_siero['ricavi'] * anno, 2)
                        trend_item['costi_siero'] = round(scenario_siero['costi'] * anno, 2)
                        trend_item['margine_siero'] = round(scenario_siero['margine_netto'] * anno, 2)
                    
                    trend_data.append(trend_item)
                
                simulation_data['trend_quinquennale'] = trend_data
                
                print("Risultati calcolati:", simulation_data)
                print("===============")
                
                # Restituisci JSON per AJAX
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse(simulation_data)
                
                # Per richieste normali, aggiungi il messaggio di successo
                messages.success(request, 'Simulazione completata con successo!')
                
            except Exception as e:
                error_msg = f"Errore nei calcoli: {str(e)}"
                print("ERRORE CALCOLI:", error_msg)
                logger.error(error_msg)
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'error': error_msg
                    })
                else:
                    messages.error(request, error_msg)
    
    # Prepara il context per il template
    context = {
        'form': form,
        'simulation_data': simulation_data,
        'simulation_json': json.dumps(simulation_data) if simulation_data else None
    }
    
    return render(request, 'dashboard/dashboard.html', context)

def ajax_calculate(request):
    """View per calcoli AJAX"""
    if request.method == 'POST':
        form = SimulationForm(request.POST)
        if form.is_valid():
            # Crea un'istanza temporanea senza salvare nel DB
            simulation = form.save(commit=False)
            
            # Calcola i risultati
            scenario_impianto = simulation.calcola_scenario_impianto()
            scenario_siero = simulation.calcola_scenario_vendita_siero()
            scenario_proteine = simulation.calcola_scenario_proteine()
            
            # Calcoli aggiuntivi per grafici
            roi_impianto = scenario_impianto['roi']
            payback_years = float(form.cleaned_data['costo_impianto']) / float(scenario_impianto['margine_netto']) if scenario_impianto['margine_netto'] > 0 else 0
            
            # Distribuzione costi
            ammortamento_annuo = float(form.cleaned_data['costo_impianto']) / 10
            distribuzione_costi = {
                'ammortamento': ammortamento_annuo,
                'operativi': float(form.cleaned_data['costi_operativi_annui']),
                'distribuzione': float(form.cleaned_data['costo_distribuzione']),
                'totale': ammortamento_annuo + float(form.cleaned_data['costi_operativi_annui']) + float(form.cleaned_data['costo_distribuzione'])
            }
            
            # Trend quinquennale
            trend_data = []
            for anno in range(1, 6):
                trend_data.append({
                    'anno': anno,
                    'ricavi_impianto': scenario_impianto['ricavi'] * anno,
                    'costi_impianto': scenario_impianto['costi'] * anno,
                    'ricavi_siero': scenario_siero['ricavi'] * anno,
                    'costi_siero': scenario_siero['costi'] * anno
                })
            
            data = {
                'success': True,
                'scenario_impianto': scenario_impianto,
                'scenario_siero': scenario_siero,
                'comparazione': {
                    'differenza_ricavi': scenario_impianto['ricavi'] - scenario_siero['ricavi'],
                    'differenza_costi': scenario_impianto['costi'] - scenario_siero['costi'],
                    'differenza_margine': scenario_impianto['margine_netto'] - scenario_siero['margine_netto']
                },
                'kpi': {
                    'roi_impianto': roi_impianto,
                    'payback_years': float(payback_years),
                    'efficienza_conversione': float(form.cleaned_data['resa_proteine']) * 100,
                    'valore_aggiunto_per_litro': (scenario_impianto['ricavi'] - scenario_siero['ricavi']) / float(form.cleaned_data['volume_siero'])
                },
                'distribuzione_costi': distribuzione_costi,
                'trend_quinquennale': trend_data
            }
            
            return JsonResponse(data)
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    
    return JsonResponse({'success': False, 'message': 'Metodo non consentito'})

def test_view(request):
    """View di test semplificata"""
    return render(request, 'dashboard/test.html')
