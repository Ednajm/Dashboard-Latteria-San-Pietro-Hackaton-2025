from django import forms
from .models import SimulationInput

class SimulationForm(forms.ModelForm):
    # Override dei campi per renderli opzionali
    capacita_investimento = forms.DecimalField(
        max_digits=12, 
        decimal_places=2,
        required=False,  # Opzionale
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'es. 200000',
            'min': '0',
            'step': '0.01'
        })
    )
    
    # Campi con valori fissi
    costo_impianto = forms.DecimalField(
        max_digits=12, 
        decimal_places=2,
        initial=1000000,  # Valore fisso
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'value': '1000000',
            'readonly': True,
            'style': 'background-color: #f8f9fa;'
        })
    )
    
    costi_operativi_annui = forms.DecimalField(
        max_digits=12, 
        decimal_places=2,
        initial=800000,  # Valore fisso
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'value': '800000',
            'readonly': True,
            'style': 'background-color: #f8f9fa;'
        })
    )
    
    prezzo_vendita_proteine = forms.DecimalField(
        max_digits=8, 
        decimal_places=2,
        initial=50.0,  # Valore fisso
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'value': '50',
            'readonly': True,
            'style': 'background-color: #f8f9fa;'
        })
    )
    
    resa_proteine = forms.DecimalField(
        max_digits=6, 
        decimal_places=4,
        required=False,
        initial=0.05,  # Valore fisso 0.05 kg/L (50g/L)
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'value': '0.05',
            'readonly': True,
            'style': 'background-color: #f8f9fa;'
        })
    )
    
    prezzo_vendita_siero = forms.DecimalField(
        max_digits=6, 
        decimal_places=2,
        initial=0.18,  # Valore fisso
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'value': '0.18',
            'readonly': True,
            'style': 'background-color: #f8f9fa;'
        })
    )
    
    costo_distribuzione = forms.DecimalField(
        max_digits=12, 
        decimal_places=2,
        initial=15000,  # Valore fisso
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'value': '15000',
            'readonly': True,
            'style': 'background-color: #f8f9fa;'
        })
    )
    
    class Meta:
        model = SimulationInput
        fields = [
            'volume_siero', 
            'capacita_investimento',
            'costo_impianto', 
            'costi_operativi_annui', 
            'prezzo_vendita_proteine', 
            'resa_proteine',
            'prezzo_vendita_siero',
            'costo_distribuzione',
            'tempistiche',
            'spazio_disponibile',
            'personale_disponibile'
        ]
        
        widgets = {
            'volume_siero': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'es. 10000',
                'min': '0',
                'step': '0.01'
            }),
            'prezzo_vendita_proteine': forms.NumberInput(attrs={
                'class': 'form-control',
                'value': '50',
                'readonly': 'readonly',
                'disabled': 'disabled',
                'style': 'background-color: #f8f9fa; cursor: not-allowed;'
            }),
            'resa_proteine': forms.NumberInput(attrs={
                'class': 'form-control',
                'value': '0.05',
                'readonly': 'readonly',
                'disabled': 'disabled',
                'style': 'background-color: #f8f9fa; cursor: not-allowed;'
            }),
            'costo_impianto': forms.NumberInput(attrs={
                'class': 'form-control',
                'value': '1000000',
                'readonly': 'readonly',
                'disabled': 'disabled',
                'style': 'background-color: #f8f9fa; cursor: not-allowed;'
            }),
            'costi_operativi_annui': forms.NumberInput(attrs={
                'class': 'form-control',
                'value': '800000',
                'readonly': 'readonly',
                'disabled': 'disabled',
                'style': 'background-color: #f8f9fa; cursor: not-allowed;'
            }),
            'prezzo_vendita_siero': forms.NumberInput(attrs={
                'class': 'form-control',
                'value': '0.18',
                'readonly': 'readonly',
                'disabled': 'disabled',
                'style': 'background-color: #f8f9fa; cursor: not-allowed;'
            }),

            'tempistiche': forms.Select(attrs={
                'class': 'form-select'
            }),
            'spazio_disponibile': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'es. 100',
                'min': '0',
                'step': '0.01'
            }),
            'personale_disponibile': forms.Select(attrs={
                'class': 'form-select'
            })
        }
        
        labels = {
            'volume_siero': 'Volume Siero (litri)',
            'capacita_investimento': 'Capacità di investimento (€)',
            'costo_impianto': 'Costo Impianto (€) - FISSO: €1.000.000',
            'costi_operativi_annui': 'Costi Operativi Annui (€) - FISSO: €800.000',
            'prezzo_vendita_proteine': 'Prezzo Vendita Proteine - FISSO',
            'resa_proteine': 'Resa Proteine - FISSO',
            'prezzo_vendita_siero': 'Prezzo Vendita Siero - FISSO',
            'costo_distribuzione': 'Costo Distribuzione (€) - FISSO: €15.000',
            'tempistiche': 'Tempistiche di Implementazione',
            'spazio_disponibile': 'Spazio Disponibile (m²)',
            'personale_disponibile': 'Personale Disponibile per Gestire l\'Impianto'
        }
    
    def clean(self):
        """Validazione personalizzata per scenari alternativi"""
        cleaned_data = super().clean()
        
        prezzo_proteine = cleaned_data.get('prezzo_vendita_proteine')
        resa_proteine = cleaned_data.get('resa_proteine')
        prezzo_siero = cleaned_data.get('prezzo_vendita_siero')
        
        # Almeno uno scenario deve essere compilato
        if not prezzo_proteine and not prezzo_siero:
            raise forms.ValidationError(
                "Devi compilare almeno uno scenario: "
                "inserisci il prezzo delle proteine O il prezzo del siero."
            )
        
        # Se inserisci prezzo proteine, devi inserire anche la resa
        if prezzo_proteine and not resa_proteine:
            raise forms.ValidationError(
                "Se inserisci il prezzo delle proteine, "
                "devi anche inserire la resa proteine."
            )
        
        return cleaned_data
    
    def save(self, commit=True):
        """Override del save per gestire campi opzionali"""
        instance = super().save(commit=False)
        
        # Imposta valori di default per campi mancanti
        if not instance.prezzo_vendita_proteine:
            instance.prezzo_vendita_proteine = 0
        if not instance.resa_proteine:
            instance.resa_proteine = 0
        if not instance.prezzo_vendita_siero:
            instance.prezzo_vendita_siero = 0 
        if commit:
            instance.save()
        return instance