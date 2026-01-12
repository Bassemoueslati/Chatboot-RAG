import pandas as pd
import os

def load_datasets():
    datasets = {}
    files = [
        'dataset/diet_recommendations_dataset.csv',
        'dataset/gym_members_exercise_tracking_synthetic_data.csv',
        'dataset/megaGymDataset.csv',
        'dataset/Nutrition__Physical_Activity__and_Obesity.csv'
    ]
    for file in files:
        if os.path.exists(file):
            datasets[file] = pd.read_csv(file)
            print(f"Loaded {file} with shape {datasets[file].shape}")
        else:
            print(f"File {file} not found")
    return datasets

def preprocess_diet_data(df):
    documents = []
    for _, row in df.iterrows():
        text = f"Patient ID {row['Patient_ID']}: Age {row['Age']}, Gender {row['Gender']}, Weight {row['Weight_kg']}kg, Height {row['Height_cm']}cm, BMI {row['BMI']}, Disease {row['Disease_Type']}, Severity {row['Severity']}, Physical Activity {row['Physical_Activity_Level']}, Daily Calories {row['Daily_Caloric_Intake']}, Cholesterol {row['Cholesterol_mg/dL']}, Blood Pressure {row['Blood_Pressure_mmHg']}, Glucose {row['Glucose_mg/dL']}, Restrictions {row['Dietary_Restrictions']}, Allergies {row['Allergies']}, Preferred Cuisine {row['Preferred_Cuisine']}, Weekly Exercise Hours {row['Weekly_Exercise_Hours']}, Adherence {row['Adherence_to_Diet_Plan']}%, Imbalance Score {row['Dietary_Nutrient_Imbalance_Score']}. Recommended Diet: {row['Diet_Recommendation']}."
        documents.append(text)
    return documents

def preprocess_gym_data(df):
    documents = []
    for _, row in df.iterrows():
        text = f"Gym Member: Age {row['Age']}, Gender {row['Gender']}, Weight {row['Weight (kg)']}kg, Height {row['Height (m)']}m, Max BPM {row['Max_BPM']}, Avg BPM {row['Avg_BPM']}, Resting BPM {row['Resting_BPM']}, Session Duration {row['Session_Duration (hours)']} hours, Calories Burned {row['Calories_Burned']}, Workout Type {row['Workout_Type']}, Fat Percentage {row['Fat_Percentage']}%, Water Intake {row['Water_Intake (liters)']}L, Workout Frequency {row['Workout_Frequency (days/week)']} days/week, Experience Level {row['Experience_Level']}, BMI {row['BMI']}."
        documents.append(text)
    return documents

def preprocess_mega_gym_data(df):
    documents = []
    for _, row in df.iterrows():
        text = f"Exercise: {row['Title']}. Description: {row['Desc']}. Type: {row['Type']}, Body Part: {row['BodyPart']}, Equipment: {row['Equipment']}, Level: {row['Level']}, Rating: {row['Rating']}, Rating Desc: {row['RatingDesc']}."
        documents.append(text)
    return documents

def preprocess_nutrition_data(df):
    documents = []
    # Sample a subset to avoid too many documents
    df_sample = df.sample(n=min(1000, len(df)), random_state=42)
    for _, row in df.iterrows():
        text = f"Year {row['YearStart']}-{row['YearEnd']}, Location {row['LocationDesc']}, Class {row['Class']}, Topic {row['Topic']}, Question: {row['Question']}. Data Value: {row['Data_Value']} {row['Data_Value_Unit']}, Type: {row['Data_Value_Type']}. Sample Size: {row['Sample_Size']}, Age: {row['Age(years)']}, Education: {row['Education']}, Gender: {row['Gender']}, Income: {row['Income']}, Race: {row['Race/Ethnicity']}."
        documents.append(text)
    return documents

def main():
    datasets = load_datasets()
    all_documents = []
    if 'diet_recommendations_dataset.csv' in datasets:
        all_documents.extend(preprocess_diet_data(datasets['diet_recommendations_dataset.csv']))
    if 'gym_members_exercise_tracking_synthetic_data.csv' in datasets:
        all_documents.extend(preprocess_gym_data(datasets['gym_members_exercise_tracking_synthetic_data.csv']))
    if 'megaGymDataset.csv' in datasets:
        all_documents.extend(preprocess_mega_gym_data(datasets['megaGymDataset.csv']))
    if 'Nutrition__Physical_Activity__and_Obesity.csv' in datasets:
        all_documents.extend(preprocess_nutrition_data(datasets['Nutrition__Physical_Activity__and_Obesity.csv']))
    print(f"Total documents: {len(all_documents)}")
    return all_documents

if __name__ == "__main__":
    documents = main()
    # Save documents for later use
    with open('data_processing/documents.txt', 'w', encoding='utf-8') as f:
        for doc in documents:
            f.write(doc + '\n')
