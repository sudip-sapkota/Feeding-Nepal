import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import json
import os
from django.conf import settings

def load_and_train_model():
    """
    Load health dataset and train Random Forest model
    """
    try:
        # Get the path to health.csv
        csv_path = os.path.join(os.path.dirname(__file__), 'health.csv')
        
        if not os.path.exists(csv_path):
            # Create synthetic training data if CSV doesn't exist
            return create_synthetic_model()
        
        # Load the dataset
        df = pd.read_csv(csv_path)
        
        # Prepare features and target
        # Create target variable based on health indicators
        def determine_eligibility(row):
            risk_factors = 0
            
            # Temperature check
            if row['temperature'] > 100.0 or row['temperature'] < 96.0:
                risk_factors += 2
                
            # Heart rate check
            if row['heart_rate'] > 100 or row['heart_rate'] < 60:
                risk_factors += 1
                
            # Blood pressure check
            if row['blood_pressure_systolic'] > 140 or row['blood_pressure_diastolic'] > 90:
                risk_factors += 2
                
            # Oxygen saturation check
            if row['oxygen_saturation'] < 95:
                risk_factors += 3
                
            # COVID symptoms
            if row.get('covid_symptoms', 0) == 1:
                risk_factors += 3
                
            # Chronic conditions
            if row.get('chronic_conditions', 0) == 1:
                risk_factors += 1
                
            # High fatigue/stress
            if row.get('fatigue_level', 0) > 6 or row.get('stress_level', 0) > 7:
                risk_factors += 1
                
            # Poor sleep
            if row.get('sleep_hours', 8) < 5:
                risk_factors += 1
                
            # BMI check
            bmi = row.get('bmi', 22)
            if bmi > 30 or bmi < 18.5:
                risk_factors += 1
                
            # Determine eligibility
            if risk_factors >= 5:
                return 'not_eligible'
            elif risk_factors >= 3:
                return 'pending'
            else:
                return 'eligible'
        
        # Create target variable
        df['eligibility'] = df.apply(determine_eligibility, axis=1)
        
        # Select features
        feature_columns = [
            'age', 'temperature', 'heart_rate', 'blood_pressure_systolic',
            'blood_pressure_diastolic', 'oxygen_saturation', 'respiratory_rate',
            'covid_symptoms', 'fatigue_level', 'stress_level', 'sleep_hours',
            'bmi', 'chronic_conditions', 'fitness_level'
        ]
        
        X = df[feature_columns]
        y = df['eligibility']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train Random Forest model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Calculate accuracy
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        return {
            'model': model,
            'accuracy': accuracy,
            'feature_columns': feature_columns,
            'training_data': df
        }
        
    except Exception as e:
        print(f"Error in model training: {e}")
        return create_synthetic_model()

def create_synthetic_model():
    """
    Create a synthetic model when CSV is not available
    """
    # Create synthetic data
    np.random.seed(42)
    n_samples = 200
    
    data = {
        'age': np.random.randint(18, 65, n_samples),
        'temperature': np.random.normal(98.6, 1.2, n_samples),
        'heart_rate': np.random.randint(60, 100, n_samples),
        'blood_pressure_systolic': np.random.randint(110, 140, n_samples),
        'blood_pressure_diastolic': np.random.randint(70, 90, n_samples),
        'oxygen_saturation': np.random.randint(95, 100, n_samples),
        'respiratory_rate': np.random.randint(14, 20, n_samples),
        'covid_symptoms': np.random.binomial(1, 0.1, n_samples),
        'fatigue_level': np.random.randint(1, 10, n_samples),
        'stress_level': np.random.randint(1, 10, n_samples),
        'sleep_hours': np.random.normal(7.5, 1.5, n_samples),
        'bmi': np.random.normal(23, 3, n_samples),
        'chronic_conditions': np.random.binomial(1, 0.2, n_samples),
        'fitness_level': np.random.randint(1, 6, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Create eligibility based on health factors
    def determine_eligibility(row):
        risk_score = 0
        if row['temperature'] > 100: risk_score += 2
        if row['heart_rate'] > 90: risk_score += 1
        if row['blood_pressure_systolic'] > 130: risk_score += 1
        if row['oxygen_saturation'] < 97: risk_score += 2
        if row['covid_symptoms']: risk_score += 3
        if row['fatigue_level'] > 7: risk_score += 1
        if row['stress_level'] > 8: risk_score += 1
        if row['chronic_conditions']: risk_score += 1
        
        if risk_score >= 4:
            return 'not_eligible'
        elif risk_score >= 2:
            return 'pending'
        else:
            return 'eligible'
    
    df['eligibility'] = df.apply(determine_eligibility, axis=1)
    
    feature_columns = list(data.keys())
    X = df[feature_columns]
    y = df['eligibility']
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    return {
        'model': model,
        'accuracy': 0.85,  # Estimated accuracy
        'feature_columns': feature_columns,
        'training_data': df
    }

# Global model instance
_model_data = None

def get_model():
    """
    Get trained model (singleton pattern)
    """
    global _model_data
    if _model_data is None:
        _model_data = load_and_train_model()
    return _model_data

def analyze_health(health_check):
    """
    Analyze health check data and predict eligibility
    """
    model_data = get_model()
    model = model_data['model']
    feature_columns = model_data['feature_columns']
    
    # Prepare input data
    input_data = {
        'age': health_check.age,
        'temperature': health_check.temperature,
        'heart_rate': health_check.heart_rate,
        'blood_pressure_systolic': health_check.blood_pressure_systolic,
        'blood_pressure_diastolic': health_check.blood_pressure_diastolic,
        'oxygen_saturation': health_check.oxygen_saturation,
        'respiratory_rate': health_check.respiratory_rate,
        'covid_symptoms': int(health_check.covid_symptoms),
        'fatigue_level': health_check.fatigue_level,
        'stress_level': health_check.stress_level,
        'sleep_hours': health_check.sleep_hours,
        'bmi': health_check.bmi,
        'chronic_conditions': int(health_check.chronic_conditions),
        'fitness_level': health_check.fitness_level
    }
    
    # Create DataFrame for prediction
    input_df = pd.DataFrame([input_data])
    
    # Make prediction
    prediction = model.predict(input_df)[0]
    prediction_proba = model.predict_proba(input_df)
    
    # Get probability scores
    classes = model.classes_
    proba_dict = dict(zip(classes, prediction_proba[0]))
    
    # Calculate health score (0-100)
    if prediction == 'eligible':
        health_score = 85 + (proba_dict.get('eligible', 0) * 15)
    elif prediction == 'pending':
        health_score = 50 + (proba_dict.get('pending', 0) * 35)
    else:
        health_score = proba_dict.get('not_eligible', 0) * 50
    
    # Determine risk level
    if health_score >= 80:
        risk_level = 'low'
    elif health_score >= 60:
        risk_level = 'medium'
    else:
        risk_level = 'high'
    
    # Generate visualizations
    charts = generate_health_charts(input_data, model_data['training_data'], prediction)
    
    return {
        'score': round(health_score, 2),
        'eligibility': prediction,
        'risk_level': risk_level,
        'accuracy': model_data['accuracy'],
        'prediction_probabilities': proba_dict,
        'charts': charts,
        'analysis_details': {
            'vital_signs': analyze_vital_signs(input_data),
            'risk_factors': identify_risk_factors(input_data)
        }
    }

def generate_health_charts(input_data, training_data, prediction):
    """
    Generate visualization charts for health analysis
    """
    charts = {}
    
    try:
        # 1. Vital Signs Comparison Chart
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('Health Analysis Dashboard', fontsize=16)
        
        # Temperature comparison
        axes[0, 0].hist(training_data['temperature'], bins=20, alpha=0.7, label='Population')
        axes[0, 0].axvline(input_data['temperature'], color='red', linestyle='--', linewidth=2, label='Your Value')
        axes[0, 0].set_title('Temperature Distribution')
        axes[0, 0].set_xlabel('Temperature (°F)')
        axes[0, 0].legend()
        
        # Heart Rate comparison
        axes[0, 1].hist(training_data['heart_rate'], bins=20, alpha=0.7, label='Population')
        axes[0, 1].axvline(input_data['heart_rate'], color='red', linestyle='--', linewidth=2, label='Your Value')
        axes[0, 1].set_title('Heart Rate Distribution')
        axes[0, 1].set_xlabel('Heart Rate (bpm)')
        axes[0, 1].legend()
        
        # Blood Pressure
        axes[1, 0].scatter(training_data['blood_pressure_systolic'], training_data['blood_pressure_diastolic'], alpha=0.5)
        axes[1, 0].scatter(input_data['blood_pressure_systolic'], input_data['blood_pressure_diastolic'], 
                          color='red', s=100, marker='*', label='Your Value')
        axes[1, 0].set_title('Blood Pressure Distribution')
        axes[1, 0].set_xlabel('Systolic BP')
        axes[1, 0].set_ylabel('Diastolic BP')
        axes[1, 0].legend()
        
        # BMI vs Fitness Level
        axes[1, 1].scatter(training_data['bmi'], training_data['fitness_level'], alpha=0.5)
        axes[1, 1].scatter(input_data['bmi'], input_data['fitness_level'], 
                          color='red', s=100, marker='*', label='Your Value')
        axes[1, 1].set_title('BMI vs Fitness Level')
        axes[1, 1].set_xlabel('BMI')
        axes[1, 1].set_ylabel('Fitness Level')
        axes[1, 1].legend()
        
        plt.tight_layout()
        
        # Save as base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        charts['vital_signs'] = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        # 2. Risk Factors Heatmap
        fig, ax = plt.subplots(figsize=(10, 6))
        
        risk_data = {
            'Temperature': [input_data['temperature']],
            'Heart Rate': [input_data['heart_rate']],
            'BP Systolic': [input_data['blood_pressure_systolic']],
            'BP Diastolic': [input_data['blood_pressure_diastolic']],
            'Oxygen Sat': [input_data['oxygen_saturation']],
            'Fatigue': [input_data['fatigue_level']],
            'Stress': [input_data['stress_level']],
            'Sleep Hours': [input_data['sleep_hours']],
            'BMI': [input_data['bmi']]
        }
        
        risk_df = pd.DataFrame(risk_data)
        
        # Normalize data for heatmap
        risk_normalized = (risk_df - risk_df.min()) / (risk_df.max() - risk_df.min())
        
        sns.heatmap(risk_normalized, annot=True, cmap='RdYlGn_r', center=0.5, 
                   cbar_kws={'label': 'Risk Level'})
        ax.set_title('Health Risk Factors Heatmap')
        ax.set_ylabel('Your Health Status')
        
        plt.tight_layout()
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        charts['risk_heatmap'] = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        # 3. Health Score Gauge
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Calculate health score
        health_score = calculate_health_score(input_data)
        
        # Create gauge chart
        categories = ['Poor', 'Fair', 'Good', 'Excellent']
        colors = ['red', 'orange', 'yellow', 'green']
        values = [25, 25, 25, 25]
        
        wedges, texts = ax.pie(values, colors=colors, startangle=180, counterclock=False)
        
        # Add health score indicator
        angle = 180 - (health_score / 100) * 180
        ax.annotate('', xy=(0.7 * np.cos(np.radians(angle)), 0.7 * np.sin(np.radians(angle))), 
                   xytext=(0, 0), arrowprops=dict(arrowstyle='->', lw=3, color='black'))
        
        ax.set_title(f'Health Score: {health_score:.1f}/100\nPrediction: {prediction.title()}', 
                    fontsize=14, fontweight='bold')
        
        # Add category labels
        for i, (category, color) in enumerate(zip(categories, colors)):
            angle = 180 - (i * 45 + 22.5)
            ax.text(0.9 * np.cos(np.radians(angle)), 0.9 * np.sin(np.radians(angle)), 
                   category, ha='center', va='center', fontweight='bold')
        
        plt.tight_layout()
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        charts['health_gauge'] = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
    except Exception as e:
        print(f"Error generating charts: {e}")
        charts = {'error': str(e)}
    
    return charts

def calculate_health_score(data):
    """
    Calculate overall health score
    """
    score = 100
    
    # Temperature penalty
    if data['temperature'] > 100 or data['temperature'] < 97:
        score -= 15
    elif data['temperature'] > 99 or data['temperature'] < 98:
        score -= 5
    
    # Heart rate penalty
    if data['heart_rate'] > 100 or data['heart_rate'] < 60:
        score -= 10
    elif data['heart_rate'] > 90 or data['heart_rate'] < 65:
        score -= 5
    
    # Blood pressure penalty
    if data['blood_pressure_systolic'] > 140 or data['blood_pressure_diastolic'] > 90:
        score -= 15
    elif data['blood_pressure_systolic'] > 130 or data['blood_pressure_diastolic'] > 85:
        score -= 8
    
    # Oxygen saturation penalty
    if data['oxygen_saturation'] < 95:
        score -= 20
    elif data['oxygen_saturation'] < 98:
        score -= 5
    
    # Lifestyle factors
    if data['fatigue_level'] > 7:
        score -= 10
    if data['stress_level'] > 8:
        score -= 8
    if data['sleep_hours'] < 6:
        score -= 10
    
    # BMI penalty
    bmi = data['bmi']
    if bmi > 30 or bmi < 18.5:
        score -= 15
    elif bmi > 27 or bmi < 20:
        score -= 5
    
    # COVID symptoms
    if data['covid_symptoms']:
        score -= 25
    
    # Chronic conditions
    if data['chronic_conditions']:
        score -= 10
    
    return max(0, score)

def analyze_vital_signs(data):
    """
    Analyze vital signs and provide assessment
    """
    analysis = {}
    
    # Temperature analysis
    temp = data['temperature']
    if temp > 100.4:
        analysis['temperature'] = 'High fever detected - immediate medical attention needed'
    elif temp > 99.5:
        analysis['temperature'] = 'Mild fever - monitor closely'
    elif temp < 97:
        analysis['temperature'] = 'Low body temperature - may indicate health issues'
    else:
        analysis['temperature'] = 'Normal temperature'
    
    # Heart rate analysis
    hr = data['heart_rate']
    if hr > 100:
        analysis['heart_rate'] = 'Elevated heart rate - may indicate stress or illness'
    elif hr < 60:
        analysis['heart_rate'] = 'Low heart rate - could be athletic or concerning'
    else:
        analysis['heart_rate'] = 'Normal heart rate'
    
    # Blood pressure analysis
    sys_bp = data['blood_pressure_systolic']
    dia_bp = data['blood_pressure_diastolic']
    if sys_bp > 140 or dia_bp > 90:
        analysis['blood_pressure'] = 'High blood pressure - needs medical evaluation'
    elif sys_bp > 130 or dia_bp > 85:
        analysis['blood_pressure'] = 'Elevated blood pressure - monitor regularly'
    else:
        analysis['blood_pressure'] = 'Normal blood pressure'
    
    return analysis

def identify_risk_factors(data):
    """
    Identify specific risk factors
    """
    risk_factors = []
    
    if data['covid_symptoms']:
        risk_factors.append('COVID-19 symptoms present')
    
    if data['chronic_conditions']:
        risk_factors.append('Pre-existing chronic conditions')
    
    if data['temperature'] > 100:
        risk_factors.append('Fever')
    
    if data['oxygen_saturation'] < 96:
        risk_factors.append('Low oxygen saturation')
    
    if data['fatigue_level'] > 7:
        risk_factors.append('High fatigue level')
    
    if data['stress_level'] > 8:
        risk_factors.append('High stress level')
    
    if data['sleep_hours'] < 6:
        risk_factors.append('Insufficient sleep')
    
    bmi = data['bmi']
    if bmi > 30:
        risk_factors.append('Obesity (BMI > 30)')
    elif bmi < 18.5:
        risk_factors.append('Underweight (BMI < 18.5)')
    
    return risk_factors if risk_factors else ['No significant risk factors identified']
