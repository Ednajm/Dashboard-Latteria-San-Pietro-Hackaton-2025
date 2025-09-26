#!/usr/bin/env python3

# Test script per testare i nuovi scenari condizionali

# Test 1: Solo scenario impianto
data_impianto = {
    'volume_siero': 10000,
    'costo_impianto': 150000,
    'costi_operativi_annui': 25000,
    'prezzo_vendita_proteine': 8.5,
    'resa_proteine': 0.0065,
    'prezzo_vendita_siero': None
}

# Test 2: Solo scenario siero  
data_siero = {
    'volume_siero': 10000,
    'costo_impianto': 150000,
    'costi_operativi_annui': 25000,
    'prezzo_vendita_proteine': None,
    'resa_proteine': None,
    'prezzo_vendita_siero': 0.5
}

# Test 3: Entrambi gli scenari
data_entrambi = {
    'volume_siero': 10000,
    'costo_impianto': 150000,
    'costi_operativi_annui': 25000,
    'prezzo_vendita_proteine': 8.5,
    'resa_proteine': 0.0065,
    'prezzo_vendita_siero': 0.5
}

def test_scenario(data, name):
    print(f"\n=== TEST {name} ===")
    print("Input:", data)
    
    volume = data['volume_siero']
    
    # Scenario Impianto (solo se ha prezzo proteine e resa)
    scenario_impianto = None
    if data['prezzo_vendita_proteine'] and data['resa_proteine']:
        resa_pct = data['resa_proteine'] / 100 if data['resa_proteine'] > 1 else data['resa_proteine']
        kg_proteine = volume * resa_pct
        ricavi_impianto = kg_proteine * data['prezzo_vendita_proteine']
        
        ammortamento_annuo = data['costo_impianto'] / 10
        costi_impianto = ammortamento_annuo + data['costi_operativi_annui']
        
        margine_impianto = ricavi_impianto - costi_impianto
        roi_impianto = (margine_impianto / data['costo_impianto']) * 100
        
        scenario_impianto = {
            'ricavi': round(ricavi_impianto, 2),
            'costi': round(costi_impianto, 2),
            'margine_netto': round(margine_impianto, 2),
            'roi': round(roi_impianto, 2),
            'kg_proteine': round(kg_proteine, 2)
        }
        print("Scenario impianto:", scenario_impianto)
    
    # Scenario Siero (solo se ha prezzo siero)
    scenario_siero = None
    if data['prezzo_vendita_siero']:
        ricavi_siero = volume * data['prezzo_vendita_siero']
        costi_siero = 0
        margine_siero = ricavi_siero - costi_siero
        
        scenario_siero = {
            'ricavi': round(ricavi_siero, 2),
            'costi': round(costi_siero, 2),
            'margine_netto': round(margine_siero, 2),
            'roi': 0
        }
        print("Scenario siero:", scenario_siero)
    
    print("Scenario type:", 'both' if (scenario_impianto and scenario_siero) else 'impianto' if scenario_impianto else 'siero')

if __name__ == "__main__":
    test_scenario(data_impianto, "SOLO IMPIANTO")
    test_scenario(data_siero, "SOLO SIERO") 
    test_scenario(data_entrambi, "ENTRAMBI")