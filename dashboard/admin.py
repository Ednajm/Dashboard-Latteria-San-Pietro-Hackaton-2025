from django.contrib import admin
from .models import SimulationInput

@admin.register(SimulationInput)
class SimulationInputAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'volume_siero', 
        'capacita_investimento',
        'costo_impianto', 
        'prezzo_vendita_proteine', 
        'resa_proteine',
        'created_at'
    ]
    list_filter = ['created_at']
    search_fields = ['id']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Parametri Principali', {
            'fields': ('volume_siero', 'capacita_investimento', 'costo_impianto', 'costi_operativi_annui')
        }),
        ('Prezzi e Resa', {
            'fields': ('prezzo_vendita_proteine', 'resa_proteine', 'prezzo_vendita_siero')
        }),
        ('Informazioni', {
            'fields': ('created_at',)
        }),
    )
