import pandas as pd
import numpy as np
from datetime import datetime
import random
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_synthetic_data(n_students=1000):
    """
    Generate synthetic student data for ONTRACK with realistic correlations
    """
    
    # Generate base features
    data = {
        'student_id': [f'ONT{str(i).zfill(5)}' for i in range(1, n_students + 1)],
        'age': np.random.randint(18, 35, n_students),
        'extracurricular': np.random.choice([0, 1], n_students, p=[0.4, 0.6]),  # 60% involved
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Generate correlated features
    gpa = []
    attendance = []
    assignments = []
    dropout = []
    
    for i in range(n_students):
        # Base probabilities depend on age and extracurricular
        base_success_prob = 0.7
        
        if df.loc[i, 'extracurricular'] == 1:
            base_success_prob += 0.1  # Extracurricular helps
            
        if df.loc[i, 'age'] > 25:
            base_success_prob -= 0.05  # Older students might have more responsibilities
        
        # Generate GPA (0-4 scale)
        if random.random() < base_success_prob:
            # Good student
            gpa_val = round(np.random.normal(3.2, 0.5), 2)
            attendance_val = round(np.random.normal(85, 10), 1)
            assignments_val = round(np.random.normal(85, 10), 1)
            dropout_val = 0
        else:
            # At-risk student
            gpa_val = round(np.random.normal(2.1, 0.6), 2)
            attendance_val = round(np.random.normal(60, 15), 1)
            assignments_val = round(np.random.normal(55, 15), 1)
            dropout_val = 1
        
        # Clip values to realistic ranges
        gpa.append(max(0, min(4, gpa_val)))
        attendance.append(max(0, min(100, attendance_val)))
        assignments.append(max(0, min(100, assignments_val)))
        dropout.append(dropout_val)
    
    df['gpa'] = gpa
    df['attendance'] = attendance
    df['assignments_submitted'] = assignments
    df['dropout'] = dropout
    
    # Add some noise to make it realistic
    noise_idx = np.random.choice(n_students, size=int(n_students*0.05), replace=False)
    df.loc[noise_idx, 'dropout'] = 1 - df.loc[noise_idx, 'dropout']  # Flip some labels
    
    return df

def split_and_save_data(df, data_dir='../data'):
    """
    Split data into train/test and save to CSV
    """
    # Create data directory if it doesn't exist
    os.makedirs(data_dir, exist_ok=True)
    
    # Shuffle the data
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Split 80-20
    split_idx = int(0.8 * len(df))
    train_df = df[:split_idx]
    test_df = df[split_idx:]
    
    # Save to CSV
    train_path = os.path.join(data_dir, 'train.csv')
    test_path = os.path.join(data_dir, 'test.csv')
    
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    
    print("=" * 50)
    print("🎓 ONTRACK - Data Generation Complete")
    print("=" * 50)
    print(f"✅ Generated {len(df)} students:")
    print(f"   - Train: {len(train_df)} students")
    print(f"   - Test: {len(test_df)} students")
    print(f"   - Dropout rate: {df['dropout'].mean():.1%}")
    print(f"   - Average GPA: {df['gpa'].mean():.2f}")
    print(f"   - Average Attendance: {df['attendance'].mean():.1f}%")
    
    # Show correlation with dropout
    print("\n📊 Feature correlation with dropout:")
    for col in ['gpa', 'attendance', 'assignments_submitted', 'age', 'extracurricular']:
        corr = df[col].corr(df['dropout'])
        print(f"   - {col}: {corr:.3f}")
    
    print(f"\n💾 Files saved:")
    print(f"   - {train_path}")
    print(f"   - {test_path}")
    print("=" * 50)
    
    return train_df, test_df

if __name__ == "__main__":
    print("🎓 ONTRACK - Generating synthetic student data...")
    
    # Generate data
    df = generate_synthetic_data(1000)
    
    # Save to CSV
    train_df, test_df = split_and_save_data(df)