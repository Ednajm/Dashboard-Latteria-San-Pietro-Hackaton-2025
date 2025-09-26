from django.db import models
from decimal import Decimal

class SimulationInput(models.Model):
    """Modello per memorizzare i parametri di input della simulazione"""
    volume_siero = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Volume di siero in litri"
    )
    capacita_investimento = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        help_text="Capacità di investimento in euro (opzionale)"
    )
    costo_impianto = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        help_text="Costo dell'impianto in euro"
    )
    costi_operativi_annui = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        help_text="Costi operativi annui in euro"
    )
    prezzo_vendita_proteine = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        help_text="Prezzo di vendita proteine in €/kg"
    )
    resa_proteine = models.DecimalField(
        max_digits=6, 
        decimal_places=4, 
        help_text="Resa in kg di proteine per litro di siero"
    )
    prezzo_vendita_siero = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        default=0.50,
        help_text="Prezzo di vendita del siero in €/litro"
    )
    
    # Campo per i costi di distribuzione
    costo_distribuzione = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=10000,
        help_text="Costo di distribuzione in euro"
    )
    
    # Opzioni per le tempistiche
    TEMPISTICHE_CHOICES = [
        ('', 'Seleziona tempistiche'),
        ('breve', 'Breve (< 6 mesi)'),
        ('media', 'Media (6-12 mesi)'),
        ('lunga', 'Lunga (> 12 mesi)'),
    ]
    
    tempistiche = models.CharField(
        max_length=10,
        choices=TEMPISTICHE_CHOICES,
        blank=True,
        null=True,
        help_text="Tempistiche di implementazione"
    )
    
    # Campo per spazio disponibile (in metri quadri)
    spazio_disponibile = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        help_text="Spazio disponibile in metri quadri"
    )
    
    # Opzioni per personale
    PERSONALE_CHOICES = [
        ('', 'Seleziona disponibilità personale'),
        ('Si', 'Sì'),
        ('No', 'No'),
    ]
    
    personale_disponibile = models.CharField(
        max_length=3,
        choices=PERSONALE_CHOICES,
        blank=True,
        null=True,
        help_text="Personale disponibile per gestire l'impianto"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Input Simulazione"
        verbose_name_plural = "Input Simulazioni"
        
    def __str__(self):
        return f"Simulazione {self.id} - {self.volume_siero}L siero"
    
    def calcola_scenario_impianto(self):
        """Calcola i risultati per lo scenario acquisto impianto"""
        kg_proteine = self.volume_siero * self.resa_proteine
        ricavi_proteine = kg_proteine * self.prezzo_vendita_proteine
        
        # Assumiamo ammortamento su 10 anni per semplicità
        ammortamento_annuo = self.costo_impianto / 10
        costi_totali = ammortamento_annuo + self.costi_operativi_annui
        
        margine_netto = ricavi_proteine - costi_totali
        roi = (margine_netto / self.costo_impianto) * 100 if self.costo_impianto > 0 else 0
        
        return {
            'ricavi': float(ricavi_proteine),
            'costi': float(costi_totali),
            'margine_netto': float(margine_netto),
            'roi': float(roi),
            'kg_proteine': float(kg_proteine)
        }
    
    def calcola_scenario_vendita_siero(self):
        """Calcola i risultati per lo scenario vendita siero"""
        ricavi_siero = self.volume_siero * self.prezzo_vendita_siero
        
        # Costi minimi per la vendita del siero (trasporto, gestione, ecc.)
        costi_vendita = ricavi_siero * Decimal('0.10')  # 10% dei ricavi
        
        margine_netto = ricavi_siero - costi_vendita
        
        return {
            'ricavi': float(ricavi_siero),
            'costi': float(costi_vendita),
            'margine_netto': float(margine_netto),
            'roi': 0  # Nessun investimento iniziale
        }
    
    def calcola_messaggio_decisionale(self):
        """Calcola il messaggio decisionale basato sui parametri di input"""
        # Calcola il budget rimanente
        budget_rimanente = (self.capacita_investimento - 
                          self.costo_impianto - 
                          self.costi_operativi_annui - 
                          self.costo_distribuzione)
        
        tempistiche_value = self.tempistiche or ''
        spazio_value = float(self.spazio_disponibile or 0)
        personale_value = self.personale_disponibile or ''
        
        # Logica decisionale
        if (budget_rimanente >= 500000 and 
            tempistiche_value != 'breve' and 
            spazio_value >= 50 and 
            personale_value == 'Si'):
            messaggio = "È possibile acquistare l'impianto per ricavare le proteine dal siero del latte"
            tipo_messaggio = "success"
            
        elif (budget_rimanente >= 500000 and 
              tempistiche_value != 'breve' and 
              spazio_value >= 50 and 
              personale_value == 'No'):
            messaggio = "È possibile acquistare l'impianto per ricavare le proteine dal siero del latte, tuttavia, è necessario assumere del personale per gestire l'impianto"
            tipo_messaggio = "warning"
            
        elif (budget_rimanente >= 500000 and 
              tempistiche_value != 'breve' and 
              spazio_value <= 50 and 
              personale_value == 'Si'):
            messaggio = "È possibile acquistare l'impianto per ricavare le proteine dal siero del latte, tuttavia, è necessario acquistare nuovi spazi per installare l'impianto"
            tipo_messaggio = "warning"
            
        elif (budget_rimanente >= 500000 and 
              tempistiche_value != 'breve' and 
              spazio_value <= 50 and 
              personale_value == 'No'):
            messaggio = "È possibile acquistare l'impianto per ricavare le proteine dal siero del latte, tuttavia, è necessario assumere del personale per gestire l'impianto e acquistare nuovi spazi per la sua installazione"
            tipo_messaggio = "warning"
            
        else:
            messaggio = "È consigliabile vendere direttamente il siero del latte a chi è dotato dell'impianto"
            tipo_messaggio = "info"
        
        return {
            'messaggio': messaggio,
            'tipo_messaggio': tipo_messaggio,
            'budget_rimanente': float(budget_rimanente),
            'dettagli': {
                'budget_rimanente': float(budget_rimanente),
                'tempistiche': tempistiche_value,
                'spazio': float(spazio_value),
                'personale': personale_value
            }
        }
