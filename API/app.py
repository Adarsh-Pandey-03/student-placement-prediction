from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import io
from fastapi.responses import StreamingResponse
import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
# API
# ====================
app=FastAPI()

# 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and features
# =================================

decision_tree=joblib.load("decision_tree_model.pkl")
random_forest = joblib.load("random_forest_model.pkl")
logistic_regression = joblib.load("logistic_regression_model.pkl")


feature=joblib.load("features.pkl")
model_analysis=joblib.load("model_analysis.pkl")
model_evaluation=joblib.load("model_evaluation.pkl")

# Input Schema
# ===============================

class validate(BaseModel):
    CGPA: float=Field(gt=0,lt=10,description="Enter total CGPA ")
    Internships: int=Field(gt=0,description="Enter your total internships ")
    Projects: int=Field(gt=0,description="Enter your total Projects ")
    Workshops: float=Field(gt=0,description="Enter total Workshops ")
    AptitudeTestScore: float=Field(gt=0,lt=100,description="Enter your AptitudeTestScore ")
    SoftSkillsRating: float=Field(gt=0,lt=4,description="Enter total SoftSkillsRating")
    SSC_Marks: float=Field(gt=0,lt=100,description="Enter your SSC_Marks ")
    HSC_Marks: float=Field(gt=0,lt=100,description="Enter your HSC_Marks ")

# Home URL
# =========================

@app.get("/")
def home():
    return{
        "message":"welcome to placement prediction",
        "prediction":"for prediction go to /predict",
        "features":list(feature)
    }

# Prediction URL
# =========================

@app.post("/predict")
def predict(data:validate):
    try:
        input_data=pd.DataFrame([{
                "CGPA":data.CGPA,
                "Internships":data.Internships,
                "Projects":data.Projects,
                "Workshops":data.Workshops,
                "AptitudeTestScore":data.AptitudeTestScore,
                "SoftSkillsRating":data.SoftSkillsRating,
                "SSC_Marks":data.SSC_Marks,
                "HSC_Marks":data.HSC_Marks
            }])
        
        # 1. Decision Tree Prediction
        # --------------------------------

        dt_prediction = decision_tree.predict(input_data)[0]
        dt_probability = decision_tree.predict_proba(input_data)[0][1]

        # 2. Random Forest Prediction
        # --------------------------------

        rf_prediction = random_forest.predict(input_data)[0]
        rf_probability = random_forest.predict_proba(input_data)[0][1]

        # 3. Logistic Regression Prediction
        # ------------------------------------

        lr_prediction = logistic_regression.predict(input_data)[0]
        lr_probability = logistic_regression.predict_proba(input_data)[0][1]


        # Helper function to format results
        # ----------------------------------------

        def get_prediction(prediction, probability):
            if prediction == 0:
                label = "Likely to be NOT PLACE"
            else:
              label = "Likely to be PLACE"

            return {
                "Prediction": label,
                "Probability": f"{probability * 100:.02f}%"
            }

        # Return all three model results
        # ----------------------------------
        
        dt_result= get_prediction(dt_prediction, dt_probability)
        rf_result= get_prediction(rf_prediction, rf_probability)
        lr_result= get_prediction(lr_prediction, lr_probability)

        return {
          "DecisionTreePrediction": dt_result["Prediction"],
          "DecisionTreeProbability": dt_result["Probability"],

         "RandomForestPrediction": rf_result["Prediction"],
         "RandomForestProbability": rf_result["Probability"],

         "LogisticRegressionPrediction": lr_result["Prediction"],
         "LogisticRegressionProbability": lr_result["Probability"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"something's wrong {e}"
        )
        
# confusion matrix
# -----------------------------------
@app.get("/image")
def send_matrices(model:str="Random Forest"):
    
    confusion_matrices = model_analysis["confusion_matrices"]
    class_names = model_analysis["class_names"]

    if model not in confusion_matrices:
        raise HTTPException(
        status_code=400,
        detail="Invalid model name"
                )
        
    cm = confusion_matrices[model]
    fig, ax = plt.subplots(figsize=(7, 5))
    
    sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=class_names,
            yticklabels=class_names,
            ax=ax
        )

    ax.set_title(f"{model} - Confusion Matrix")
    ax.set_xlabel("Predicted Label")
    ax.set_ylabel("Actual Label")
                
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
                
    return StreamingResponse(buf, media_type="image/png")

# feature importance
# --------------------------------
@app.get("/image2")
def send_importance(model:str="Random Forest"):
    feature_importance=model_analysis["feature_importance"]
    class_names=model_analysis["class_names"]

    if model not in feature_importance:
        raise HTTPException(
            status_code=400,
            detail="Invalid model name"
        )
    FI=feature_importance[model]

    FI["Importance"] = pd.to_numeric(
    FI["Importance"], errors="coerce"
    )
    FI = FI.dropna(subset=["Importance"])
    FI = FI.sort_values(by="Importance", ascending=True)
    fig, ax= plt.subplots(figsize=(7,5))

    sns.barplot(
        data=FI,
        x="Importance",
        y="Feature",
        color="steelblue",
        ax=ax
)
    ax.set_title(f"{model} - Feature importance")
    ax.set_xlabel("Importance")
    ax.set_ylabel("Feature")

    buf=io.BytesIO()
    fig.savefig(buf, format="png",bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)

    return StreamingResponse(buf , media_type="image/png")

@app.get("/evaluation")
def evaluation_data():
    logistic_model_eval=model_evaluation["logistic_regression"]
    decision_model_eval=model_evaluation["decision_tree"]
    forest_model_eval=model_evaluation["random_forest"]
    class_names=model_evaluation["class_names"]

    def get_evaluation(accuracy,precision,recall,f1):
        return{
            
                "accuracy":accuracy,
                "precision":precision,
                "recall":recall,
                "f1":f1
        }
    
    logistic_eval=get_evaluation(
                       logistic_model_eval["accuracy"],
                       logistic_model_eval["precision"],
                       logistic_model_eval["recall"],
                       logistic_model_eval["f1"]
                       )
    decision_eval=get_evaluation(
                   decision_model_eval["accuracy"],
                   decision_model_eval["precision"],
                   decision_model_eval["recall"],
                   decision_model_eval["f1"]
                   )
    forest_eval=get_evaluation(
                       forest_model_eval["accuracy"],
                       forest_model_eval["precision"],
                       forest_model_eval["recall"],
                       forest_model_eval["f1"]
                       )
    return {

        "Logistic Regression":logistic_eval,
        "Decision Tree":decision_eval,
        "Random Forest":forest_eval
    }