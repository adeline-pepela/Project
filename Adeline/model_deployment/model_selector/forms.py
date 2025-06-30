from django import forms
import os
from django.conf import settings

def get_available_models():
    """Get available model directories as choices for the form"""
    model_dirs = []
    for model_dir in os.listdir(settings.MODELS_DIR):
        if os.path.isdir(os.path.join(settings.MODELS_DIR, model_dir)):
            model_dirs.append((model_dir, model_dir.replace('_', ' ').title()))
    return model_dirs

class ModelSelectionForm(forms.Form):
    model_choice = forms.ChoiceField(
        choices=get_available_models,
        label="Select Model",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Features matching the trained model's expected input - exact names from model inspection
    MonthlyCharges = forms.FloatField(
        label="Monthly Charges",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=65.0
    )
    
    CustomerSegment = forms.ChoiceField(
        choices=[
            ('High Value', 'High Value'),
            ('Medium Value', 'Medium Value'),
            ('Low Value', 'Low Value')
        ],
        label="Customer Segment",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    TotalCharges = forms.FloatField(
        label="Total Charges",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=1560.0
    )
    
    # Additional features with exact names from model inspection
    avg_monthly_spend = forms.FloatField(
        label="Average Monthly Spend",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=70.0
    )
    
    total_revenue = forms.FloatField(
        label="Total Revenue",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=1800.0
    )
    
    total_refunds = forms.FloatField(
        label="Total Refunds",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=0.0
    )
    
    daily_mobile_usage = forms.FloatField(
        label="Daily Mobile Usage (Minutes)",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=45.0
    )
    
    total_extra_data = forms.FloatField(
        label="Total Extra Data Charges",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=10.0
    )
    
    total_long_distance = forms.FloatField(
        label="Total Long Distance Charges",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=15.0
    )
    
    daily_data_usage = forms.FloatField(
        label="Daily Data Usage (MB)",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=500.0
    )