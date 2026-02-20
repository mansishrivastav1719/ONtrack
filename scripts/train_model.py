import pandas as pd
import numpy as np
import xgboost as xgb
import joblib
import os
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Set random seed
np.random.seed(42)

def load_data(data_dir='../data'):
    """
    Load training and testing data
    """
    train_path = os.path.join(data_dir, 'train.csv')
    test_path = os.path.join(data_dir, 'test.csv')
    
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    
    print(f"📊 Loaded {len(train_df)} training samples and {len(test_df)} test samples")
    
    return train_df, test_df

def prepare_features(df):
    """
    Separate features and target
    """
    feature_cols = ['gpa', 'attendance', 'assignments_submitted', 'extracurricular', 'age']
    X = df[feature_cols]
    y = df['dropout']
    
    return X, y

def train_xgboost_model(X_train, y_train, X_val=None, y_val=None):
    """
    Train XGBoost model with hyperparameters
    """
    print("\n🚀 Training XGBoost model...")
    
    # Define model with optimal hyperparameters for hackathon
    model = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric='logloss',
        use_label_encoder=False,
        early_stopping_rounds=20  # Move this HERE, inside the model initialization
    )
    
    # Train model
    if X_val is not None and y_val is not None:
        model.fit(
            X_train, y_train,
            eval_set=[(X_val, y_val)],
            verbose=False
        )
        print(f"✅ Best iteration: {model.best_iteration if hasattr(model, 'best_iteration') else 'N/A'}")
    else:
        # Simple training
        model.fit(X_train, y_train)
    
    return model

def evaluate_model(model, X_test, y_test):
    """
    Evaluate model performance
    """
    print("\n📈 Evaluating model performance...")
    
    # Make predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    
    print("=" * 50)
    print("🎓 ONTRACK - Model Performance")
    print("=" * 50)
    print(f"✅ Accuracy:  {accuracy:.3f}")
    print(f"✅ Precision: {precision:.3f}")
    print(f"✅ Recall:    {recall:.3f}")
    print(f"✅ F1-Score:  {f1:.3f}")
    print(f"✅ ROC-AUC:   {roc_auc:.3f}")
    print("=" * 50)
    
    # Feature importance
    feature_names = ['GPA', 'Attendance', 'Assignments', 'Extracurricular', 'Age']
    importance = model.feature_importances_
    
    print("\n📊 Feature Importance:")
    for name, imp in sorted(zip(feature_names, importance), key=lambda x: x[1], reverse=True):
        print(f"   - {name}: {imp:.3f}")
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print("\n📊 Confusion Matrix:")
    print(f"   TN: {cm[0,0]:3d}  FP: {cm[0,1]:3d}")
    print(f"   FN: {cm[1,0]:3d}  TP: {cm[1,1]:3d}")
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'roc_auc': roc_auc,
        'feature_importance': dict(zip(feature_names, importance))
    }

def plot_confusion_matrix(model, X_test, y_test, save_path='../docs/confusion_matrix.png'):
    """
    Plot and save confusion matrix
    """
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Stayed', 'Dropped Out'],
                yticklabels=['Stayed', 'Dropped Out'])
    plt.title('ONTRACK - Confusion Matrix')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    
    # Save plot
    os.makedirs('../docs', exist_ok=True)
    plt.savefig(save_path, dpi=100, bbox_inches='tight')
    plt.close()
    print(f"\n💾 Confusion matrix saved to {save_path}")

def plot_feature_importance(model, save_path='../docs/feature_importance.png'):
    """
    Plot and save feature importance
    """
    feature_names = ['GPA', 'Attendance', 'Assignments', 'Extracurricular', 'Age']
    importance = model.feature_importances_
    
    # Sort by importance
    indices = np.argsort(importance)[::-1]
    
    plt.figure(figsize=(10, 6))
    plt.title('ONTRACK - Feature Importance')
    plt.bar(range(len(importance)), importance[indices], color='skyblue')
    plt.xticks(range(len(importance)), [feature_names[i] for i in indices], rotation=45)
    plt.xlabel('Features')
    plt.ylabel('Importance Score')
    plt.tight_layout()
    
    # Save plot
    os.makedirs('../docs', exist_ok=True)
    plt.savefig(save_path, dpi=100, bbox_inches='tight')
    plt.close()
    print(f"💾 Feature importance plot saved to {save_path}")

def save_model(model, model_dir='../model'):
    """
    Save trained model to file
    """
    # Create model directory if it doesn't exist
    os.makedirs(model_dir, exist_ok=True)
    
    # Save model
    model_path = os.path.join(model_dir, 'xgboost_model.pkl')
    joblib.dump(model, model_path)
    print(f"\n💾 Model saved to {model_path}")
    
    # Also save feature names for reference
    feature_names_path = os.path.join(model_dir, 'feature_names.txt')
    with open(feature_names_path, 'w') as f:
        f.write('\n'.join(['gpa', 'attendance', 'assignments_submitted', 'extracurricular', 'age']))
    print(f"💾 Feature names saved to {feature_names_path}")
    
    return model_path

def cross_validate_model(X, y):
    """
    Perform cross-validation
    """
    print("\n🔄 Performing 5-fold cross-validation...")
    
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        random_state=42,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    
    scores = cross_val_score(model, X, y, cv=5, scoring='roc_auc')
    
    print(f"✅ Cross-validation ROC-AUC scores: {scores}")
    print(f"✅ Mean ROC-AUC: {scores.mean():.3f} (+/- {scores.std() * 2:.3f})")
    
    return scores

if __name__ == "__main__":
    print("=" * 50)
    print("🎓 ONTRACK - Model Training Pipeline")
    print("=" * 50)
    
    # Load data
    train_df, test_df = load_data()
    
    # Prepare features
    X_train, y_train = prepare_features(train_df)
    X_test, y_test = prepare_features(test_df)
    
    print(f"\n📊 Training set: {X_train.shape}")
    print(f"📊 Test set: {X_test.shape}")
    print(f"📊 Dropout rate in training: {y_train.mean():.1%}")
    
    # Split training data for validation
    X_train_sub, X_val, y_train_sub, y_val = train_test_split(
        X_train, y_train, test_size=0.2, random_state=42, stratify=y_train
    )
    
    # Train model
    model = train_xgboost_model(X_train_sub, y_train_sub, X_val, y_val)
    
    # Evaluate
    metrics = evaluate_model(model, X_test, y_test)
    
    # Cross-validation
    cross_validate_model(X_train, y_train)
    
    # Save visualizations
    plot_confusion_matrix(model, X_test, y_test)
    plot_feature_importance(model)
    
    # Save model
    model_path = save_model(model)
    
    print("\n" + "=" * 50)
    print("✨ ONTRACK - Training Complete!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Start your backend: cd ../backend && python app.py")
    print("2. Test the API at http://localhost:8000/docs")
    print("3. Seed database with students: python seed_db.py")
    print("=" * 50)