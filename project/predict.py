
# Mathematics score prediction function
def predict_math_score(student_data):
    # Loading models and preprocessing tools
    import joblib
    import pandas as pd
    import numpy as np
    model = joblib.load('best_math_score_model.pkl')
    
    # === Preprocessing input data (completely consistent with the training step)===
    # 1. Define feature names and feature types (same as when training)
    numerical_features = [
        'Medu', 'Fedu', 'traveltime', 'studytime', 'failures', 
        'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 
        'health', 'absences'
    ]
    
    categorical_features = [
        'school', 'sex', 'address', 'famsize', 'Pstatus', 
        'Mjob', 'Fjob', 'reason', 'guardian', 'schoolsup',
        'famsup', 'paid', 'activities', 'nursery', 'higher',
        'internet', 'romantic'
    ]
    
    # 2. Convert input to DataFrame(Use the characteristic order during training)
    all_features = numerical_features + categorical_features
    input_df = pd.DataFrame([student_data], columns=all_features)
    
    # 3.Loading pre-trained OneHotEncoder(Save during training)
    encoder = joblib.load('onehot_encoder.pkl')  # Make sure this file exists
    
    # 4. Unique coding classification characteristics
    encoded_categorical = encoder.transform(input_df[categorical_features])
    encoded_categorical_df = pd.DataFrame(
        encoded_categorical,
        columns=encoder.get_feature_names_out(categorical_features)
    )
    
    # 5. Combining numerical features and encoded classification features
    processed_data = pd.concat(
        [input_df[numerical_features], encoded_categorical_df], 
        axis=1
    )
    
    # === Combining numerical features and encoded classification features ===
    prediction = model.predict(processed_data)[0]
    
    # === Risk classification and recommendations ===
    prediction_rounded = round(prediction, 1)
    if prediction >= 12:
        risk_level = "low risk"
        action = "No intervention required"
    elif prediction >= 10:
        risk_level = "Medium risk"
        action = "Pay attention to learning situation"
    else:
        risk_level = "High risk"
        action = "Arrange tutoring now"
    
    return ("Predicted results": prediction_rounded,"Risk level": risk_level,"Suggested actions": action)

# Sample 
# Characteristic order£º['Medu','Fedu','traveltime',...£¨Numerical features£©, 'school','sex',...£¨Classification characteristics£©]
# student_sample = [4, 4, 1, 2, 0, 4, 3, 4, 1, 1, 5, 0, 'GP', 'F', 'U', 'GT3', 'T', 'services', 'other', 'home', 'mother', 'yes', 'yes', 'yes', 'yes', 'yes', 'no', 'yes', 'yes']
# print(predict_math_score(student_sample))
