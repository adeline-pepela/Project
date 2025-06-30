from django.shortcuts import render
from django.conf import settings
import os
import pickle
import pandas as pd
import numpy as np
from .forms import ModelSelectionForm

def home(request):
    """View for the home page"""
    return render(request, 'model_selector/home.html')

def load_model(model_dir):
    """Load the selected model from the models directory"""
    model_path = os.path.join(settings.MODELS_DIR, model_dir, 'churn_model.pkl')
    
    # If the model file doesn't exist with the standard name, try to find any .pkl file
    if not os.path.exists(model_path):
        for file in os.listdir(os.path.join(settings.MODELS_DIR, model_dir)):
            if file.endswith('.pkl') and 'model' in file.lower():
                model_path = os.path.join(settings.MODELS_DIR, model_dir, file)
                break
    
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        return model
    except ModuleNotFoundError as e:
        # Handle missing module error
        return f"Error: Missing module - {str(e)}. Please install the required package."
    except Exception as e:
        return f"Error loading model: {str(e)}"

def index(request):
    """View for the prediction page"""
    prediction_result = None
    selected_model = None
    probability = None
    error_message = None
    
    if request.method == 'POST':
        form = ModelSelectionForm(request.POST)
        if form.is_valid():
            # Get the selected model
            selected_model = form.cleaned_data['model_choice']
            
            # Load the model
            model = load_model(selected_model)
            
            # Check if model loading returned an error message
            if isinstance(model, str) and model.startswith("Error"):
                error_message = model
            else:
                # Encode CustomerSegment as a numeric value
                customer_segment = form.cleaned_data['CustomerSegment']
                segment_value = 0
                if customer_segment == 'Medium Value':
                    segment_value = 1
                elif customer_segment == 'High Value':
                    segment_value = 2
                
                # Prepare input data for prediction using the exact feature names from the model
                input_data = {
                    'MonthlyCharges': form.cleaned_data['MonthlyCharges'],
                    'Average Monthly Spend': form.cleaned_data['avg_monthly_spend'],
                    'CustomerSegment': segment_value,
                    'Total Revenue': form.cleaned_data['total_revenue'],
                    'TotalCharges': form.cleaned_data['TotalCharges'],
                    'Total Refunds': form.cleaned_data['total_refunds'],
                    'Daily Mobile Usage (Minutes)': form.cleaned_data['daily_mobile_usage'],
                    'Total Extra Data Charges': form.cleaned_data['total_extra_data'],
                    'Total Long Distance Charges': form.cleaned_data['total_long_distance'],
                    'Daily Data Usage (MB)': form.cleaned_data['daily_data_usage'],
                }
                
                # Convert to DataFrame for prediction
                input_df = pd.DataFrame([input_data])
                
                # Make prediction
                try:
                    # Set predict_disable_shape_check for LightGBM models
                    if hasattr(model, 'predict') and 'lightgbm' in str(type(model)).lower():
                        prediction = model.predict(input_df, predict_disable_shape_check=True)[0]
                    else:
                        prediction = model.predict(input_df)[0]
                    
                    # Get probability if available
                    if hasattr(model, 'predict_proba'):
                        try:
                            if 'lightgbm' in str(type(model)).lower():
                                probability = model.predict_proba(input_df, predict_disable_shape_check=True)[0][1]
                            else:
                                probability = model.predict_proba(input_df)[0][1]
                        except:
                            probability = None
                    
                    prediction_result = "Churn" if prediction == 1 else "No Churn"
                except Exception as e:
                    error_message = f"Error making prediction: {str(e)}"
    else:
        form = ModelSelectionForm()
    
    return render(request, 'model_selector/index.html', {
        'form': form,
        'prediction_result': prediction_result,
        'selected_model': selected_model,
        'probability': probability,
        'error_message': error_message
    })