import sys
import os
from datetime import datetime
import random
import pandas as pd
import numpy as np

# Add backend to path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from database import db
from models.predictor import predictor
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_test_data():
    """Load test data from CSV"""
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'test.csv')
    df = pd.read_csv(data_path)
    return df

def seed_database(n_students=50):
    """
    Seed MongoDB with student data and predictions
    """
    print("=" * 50)
    print("🎓 ONTRACK - Database Seeding")
    print("=" * 50)
    
    # Check database connection
    if not db.check_connection():
        print("❌ Database not connected. Make sure MongoDB is running.")
        return False
    
    # Check if model is loaded
    if not predictor.is_loaded():
        print("❌ Model not loaded. Make sure model file exists.")
        return False
    
    # Load test data
    df = load_test_data()
    df = df.sample(min(n_students, len(df)))  # Random sample
    
    print(f"\n📊 Loading {len(df)} students from test data...")
    
    # Clear existing data (optional)
    response = input("\n⚠️  Do you want to clear existing student data? (y/n): ")
    if response.lower() == 'y':
        deleted = db.delete_all_students()
        print(f"🗑️  Cleared {deleted} existing records")
    
    # Process each student
    successful = 0
    failed = 0
    
    for idx, row in df.iterrows():
        try:
            # Prepare features
            features = {
                'gpa': float(row['gpa']),
                'attendance': float(row['attendance']),
                'assignments_submitted': float(row['assignments_submitted']),
                'extracurricular': int(row['extracurricular']),
                'age': int(row['age'])
            }
            
            # Get prediction
            prediction_result = predictor.predict(features)
            
            if prediction_result is None:
                failed += 1
                continue
            
            # Prepare student record
            student_record = {
                'student_id': row['student_id'] if 'student_id' in row else f'ONT{str(idx).zfill(5)}',
                'features': features,
                'prediction': {
                    'probability': prediction_result['dropout_probability'],
                    'risk_level': prediction_result['risk_level'],
                    'shap_values': prediction_result['shap_values'],
                    'timestamp': datetime.now()
                },
                'actual_dropout': 'Yes' if row['dropout'] == 1 else 'No',
                'timestamp': datetime.now()
            }
            
            # Insert into database
            db.insert_student(student_record)
            successful += 1
            
            # Print progress
            if (successful + failed) % 10 == 0:
                print(f"   Progress: {successful + failed}/{len(df)}")
                
        except Exception as e:
            logger.error(f"Failed to process student: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print("📊 Seeding Complete!")
    print("=" * 50)
    print(f"✅ Successfully added: {successful} students")
    print(f"❌ Failed: {failed} students")
    
    # Show distribution
    risk_dist = db.get_risk_distribution()
    print("\n📈 Risk Distribution:")
    for level, count in risk_dist.items():
        percentage = (count / successful) * 100 if successful > 0 else 0
        print(f"   - {level}: {count} ({percentage:.1f}%)")
    
    return True

def seed_with_custom_data():
    """Create and seed with custom balanced data"""
    print("\n🔄 Generating balanced synthetic data...")
    
    # Clear existing
    db.delete_all_students()
    
    # Generate 30 students for demo (balanced)
    risk_levels = ['Low', 'Medium', 'High']
    colors = {
        'Low': {'gpa': (3.2, 0.3), 'attendance': (90, 5), 'assignments': (90, 5)},
        'Medium': {'gpa': (2.5, 0.3), 'attendance': (75, 8), 'assignments': (70, 10)},
        'High': {'gpa': (1.8, 0.4), 'attendance': (55, 10), 'assignments': (50, 12)}
    }
    
    successful = 0
    
    for risk in risk_levels:
        for i in range(10):  # 10 per risk level
            params = colors[risk]
            
            # Generate features
            features = {
                'gpa': round(max(0, min(4, np.random.normal(*params['gpa']))), 2),
                'attendance': round(max(0, min(100, np.random.normal(*params['attendance']))), 1),
                'assignments_submitted': round(max(0, min(100, np.random.normal(*params['assignments']))), 1),
                'extracurricular': random.choice([0, 1]),
                'age': random.randint(18, 30)
            }
            
            # Get prediction
            prediction_result = predictor.predict(features)
            
            if prediction_result:
                student_record = {
                    'student_id': f'DEMO{str(successful).zfill(3)}',
                    'features': features,
                    'prediction': {
                        'probability': prediction_result['dropout_probability'],
                        'risk_level': prediction_result['risk_level'],
                        'shap_values': prediction_result['shap_values'],
                        'timestamp': datetime.now()
                    },
                    'actual_dropout': None,  # Unknown for demo
                    'timestamp': datetime.now()
                }
                
                db.insert_student(student_record)
                successful += 1
    
    print(f"\n✅ Added {successful} balanced demo students")
    return True

if __name__ == "__main__":
    print("🎓 ONTRACK - Database Seeding Utility")
    print("\nChoose an option:")
    print("1. Seed with test data (realistic)")
    print("2. Seed with balanced demo data (perfect for presentation)")
    print("3. Clear database only")
    
    choice = input("\nEnter choice (1/2/3): ")
    
    if choice == '1':
        n = input("Number of students to seed (default 50): ")
        n = int(n) if n.strip() else 50
        seed_database(n)
    elif choice == '2':
        seed_with_custom_data()
    elif choice == '3':
        confirm = input("⚠️  Delete ALL students? (yes/no): ")
        if confirm.lower() == 'yes':
            deleted = db.delete_all_students()
            print(f"🗑️  Deleted {deleted} students")
    else:
        print("❌ Invalid choice")