import pickle
import os
import sys

def inspect_model(model_dir):
    model_path = os.path.join('..', 'models', model_dir, 'churn_model.pkl')
    
    if not os.path.exists(model_path):
        for file in os.listdir(os.path.join('..', 'models', model_dir)):
            if file.endswith('.pkl') and 'model' in file.lower():
                model_path = os.path.join('..', 'models', model_dir, file)
                break
    
    print(f"Loading model from: {model_path}")
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    print(f"Model type: {type(model)}")
    
    # Try different ways to get feature names
    if hasattr(model, 'feature_names_'):
        print(f"Feature names from feature_names_: {model.feature_names_}")
    elif hasattr(model, 'feature_names_in_'):
        print(f"Feature names from feature_names_in_: {model.feature_names_in_}")
    else:
        print("No feature_names_ or feature_names_in_ attribute found")
    
    # For ensemble models, check the first estimator
    if hasattr(model, 'estimators_') and len(model.estimators_) > 0:
        print("\nChecking first estimator in ensemble:")
        estimator = model.estimators_[0]
        if hasattr(estimator, 'feature_names_in_'):
            print(f"Feature names from first estimator: {estimator.feature_names_in_}")
    
    # For pipeline models
    if hasattr(model, 'steps'):
        print("\nThis is a Pipeline model with steps:")
        for name, step in model.steps:
            print(f"- {name}: {type(step)}")
        
        # Check the final estimator
        final_step = model.steps[-1][1]
        if hasattr(final_step, 'feature_names_in_'):
            print(f"Feature names from final estimator: {final_step.feature_names_in_}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        model_dir = sys.argv[1]
        inspect_model(model_dir)
    else:
        print("Please provide a model directory name")
