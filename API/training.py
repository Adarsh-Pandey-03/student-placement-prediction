import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import numpy as np
df=pd.read_csv("placementdata.csv")

print("First Data:")
print(df.head())
print(f"Rows: {df.shape[0]} Column: {df.shape[1]}")
print("Statistics Of Data:")
print(df.describe())
print("Info About Data:")
print(df.info())

print("Total Null Values:")
print(df.isnull().sum())

# ====================================
# Encoding
# ====================================
le=LabelEncoder()
df["PlacementStatus"]=le.fit_transform(df["PlacementStatus"])

# =====================================
# Feature and target
# =====================================
features=[
   "CGPA",
   "Internships",
   "Projects",
   "Workshops",
   "AptitudeTestScore",
   "SoftSkillsRating",
   "SSC_Marks",
   "HSC_Marks"
   ]

X=df[features]
y=df["PlacementStatus"]

# =====================================
# Train-Test-Split
# =====================================

X_train, X_test, y_train, y_test=train_test_split(
   X,
   y,
   test_size=0.2,
   random_state=42,stratify=y
   )

# ============================================================
# Logistic Regression Pipeline Scaling + Logistic Regression
# =============================================================

logistic_model=Pipeline([
   ("scaler",StandardScaler()),
   ("model",LogisticRegression(max_iter=1000))
])

# ========================================================================
# MODEL 1: Logistic Regression
# ========================================================================

logistic_model.fit(X_train,y_train)
logistic_y_pred=logistic_model.predict(X_test)

print("\n==============================")
print("LOGISTIC REGRESSION")
print("==============================")

print("Accuracy:",accuracy_score(y_test,logistic_y_pred))

print("\nClassification Report:")
logistic_classi_report=classification_report(y_test,logistic_y_pred)
print(logistic_classi_report)

print("\nConfusion Matrix:")
logistic_conf_matrix=confusion_matrix(y_test,logistic_y_pred)
print(logistic_conf_matrix)

print("\nCross Validtion Accuracy:")
score=cross_val_score(
   logistic_model,
   X_train,
   y_train,
   cv=5,
   scoring="accuracy"
)
print(score.mean())

# =========================================================================
# MODEL 2: DECISION TREE
# =========================================================================

decision_tree_model=DecisionTreeClassifier(random_state=42,max_depth=5)
decision_tree_model.fit(X_train,y_train)
tree_y_pred=decision_tree_model.predict(X_test)

print("\n==============================")
print("DECISION TREE")
print("==============================")

print("Accuracy:",accuracy_score(y_test,tree_y_pred))

print("Classification Report:")
decision_classi_report=classification_report(y_test,tree_y_pred)
print(decision_classi_report)

print("Confusion Matrix:")
tree_conf_matrix=confusion_matrix(y_test,tree_y_pred)
print(tree_conf_matrix)

print("\nCross Validtion Accuracy:")
score=cross_val_score(
   decision_tree_model,
   X_train,
   y_train,
   cv=5,
   scoring="accuracy"
)
print(score.mean())


# ========================================================================
# MODEL 3:RANDOM FOREST
# ========================================================================

forest_model=RandomForestClassifier(n_estimators=100,random_state=42)

forest_model.fit(X_train,y_train)

forest_y_pred=forest_model.predict(X_test)

print("\n==================================")
print("RANDOM FOREST")
print("====================================")

print("Accuracy:",accuracy_score(y_test,forest_y_pred))

print("Classification Report")
forest_classi_report=classification_report(y_test,forest_y_pred)
print(forest_classi_report)

print("Confusion Matrix")
forest_conf_matrix=confusion_matrix(y_test,forest_y_pred)
print(forest_conf_matrix)

print("\nCross Validtion Accuracy:")
score=cross_val_score(
   forest_model,
   X_train,
   y_train,
   cv=5,
   scoring="accuracy"
)
print(score.mean())

# ==============================================
# Confusion Matrices
# ==============================================

fig,axes=plt.subplots(1,3,figsize=(12,5))

# Logistic Regression
# -----------------------------
sns.heatmap(
   logistic_conf_matrix,
   annot=True,
   fmt='d',
   cmap='Blues',
   xticklabels=["Not Placed","Placed"],
   yticklabels=["Not Placed","Placed"],
   ax=axes[0]
)
axes[0].set_title("Logistic Regression")
axes[0].set_xlabel("predicted")
axes[0].set_ylabel("actual")

# Decision Tree
# -----------------------------
sns.heatmap(
   tree_conf_matrix,
   annot=True,
   fmt="d",
   cmap="Blues",
   xticklabels=["Not placed","Placed"],
   yticklabels=["Not Placed","Placed"],
   ax=axes[1]
)
axes[1].set_title("Decision Tree")
axes[1].set_xlabel("predicted")
axes[1].set_ylabel("actual")

# Random Forest Tree
# -------------------------------
sns.heatmap(
   forest_conf_matrix,
   annot=True,
   fmt="d",
   cmap="Blues",
   xticklabels=["Not Placed","Placed"],
   yticklabels=["Not Placed","Placed"],
   ax=axes[2]
)
axes[2].set_title("Random forest Tree")
axes[2].set_xlabel("Predicion")
axes[2].set_ylabel("actual")

plt.tight_layout()
plt.show()

# ===================================================================
# Feature Importance
# ===================================================================

# ============================================
# 1. Decision Tree Feature Importance
# # ==========================================

decision_feature_importance=pd.DataFrame({
   "Feature":features,
   "Importance":decision_tree_model.feature_importances_
})
decision_feature_importance=decision_feature_importance.sort_values(
   by="Importance",
   ascending=False,
)
print("\n===========================================")
print("Decision Tree Feature Importance")
print("=============================================")
print(decision_feature_importance)

# =============================================
# 2. Random Forest Freature Importance
# =============================================
forest_feature_importance=pd.DataFrame({
   "Feature":features,
   "Importance":forest_model.feature_importances_
})
forest_feature_importance=forest_feature_importance.sort_values(
   by="Importance",
   ascending=False
)
print("\n===========================================")
print("Random Forest Feature Importance")
print("=============================================")

print(forest_feature_importance)

# =============================================
# 3. Logistic Regression Freature Importance
# =============================================

# getting logistic regression model from the pipeline
# --------------------------------------------------------
lr = logistic_model.named_steps['model']

# Create feature importance DataFrame
# ------------------------------------------
logistic_feature_importance = pd.DataFrame({
    'Feature': X_train.columns,
    'Coefficient': lr.coef_[0],
    'Importance': np.abs(lr.coef_[0])
})

# Sort by importance
# -------------------------------------
logistic_feature_importance = logistic_feature_importance.sort_values(
    by='Importance',
    ascending=False
)
print("\n===========================================")
print("Random Forest Feature Importance")
print("=============================================")

print(logistic_feature_importance)

# =============================================
# Feature Importance Graph Representaion
# =============================================

fig,axes=plt.subplots(1,3,figsize=(12,6))

# 1. Decision Tree
# -------------------------
sns.barplot(
   data=decision_feature_importance,
   x="Importance",
   y="Feature",
   color="steelblue",
   ax=axes[0]
)
axes[0].set_title("Decision Tree Feature Importance")
axes[0].set_xlabel("Importance")
axes[0].set_ylabel("Feature")

# 2. Random Forest
# --------------------------
sns.barplot(
   data=forest_feature_importance,
   x="Importance",
   y="Feature",
   color="steelblue",
   ax=axes[1]
)
axes[1].set_title("Random Forest Feature Importance")
axes[1].set_xlabel("Importance")
axes[1].set_ylabel("Feature")


# 3. Logistic Regression
# -------------------------------
sns.barplot(
   data=logistic_feature_importance,
   x="Importance",
   y="Feature",
   color="steelblue",
   ax=axes[2]
)
axes[2].set_title("Logistic Regression Feature Importance")
axes[2].set_xlabel("Importance")
axes[2].set_ylabel("Feature")

plt.tight_layout()
plt.show()


# =========================================
# SAVE EXISTING ANALUSIS RESULTS
# =========================================

model_analysis = {
    "confusion_matrices": {
        "Logistic Regression": logistic_conf_matrix,
        "Decision Tree": tree_conf_matrix,
        "Random Forest": forest_conf_matrix
    },
    "feature_importance": {
        "Logistic Regression": logistic_feature_importance,
        "Decision Tree": decision_feature_importance,
        "Random Forest": forest_feature_importance
    },
    "class_names": list(le.classes_)
}

# =========================================
# SAVE EXISTING EVALUATOIN RESULTS
# =========================================

model_evaluation={
   "logistic_regression": {
      "accuracy": accuracy_score(y_test,logistic_y_pred),
      "precision": precision_score(y_test,logistic_y_pred),
      "recall": recall_score(y_test,logistic_y_pred),
      "f1": f1_score(y_test,logistic_y_pred)
   },
   "decision_tree": {
      "accuracy": accuracy_score(y_test,tree_y_pred),
      "precision": precision_score(y_test,tree_y_pred),
      "recall": recall_score(y_test,tree_y_pred),
      "f1": f1_score(y_test,tree_y_pred)
   },
   "random_forest":{
      "accuracy":accuracy_score(y_test,forest_y_pred),
      "precision":precision_score(y_test,forest_y_pred),
      "recall":recall_score(y_test,forest_y_pred),
      "f1":f1_score(y_test,forest_y_pred)

   },
   "class_names":list(le.classes_)
}




# ===================================================
# SAVING MODELS AND THEIR EVALUTIONS
# ===================================================

with open("model_evaluation.pkl","wb") as f:
   pickle.dump(model_evaluation,f)


with open("model_analysis.pkl", "wb") as f:
    pickle.dump(model_analysis, f)

with open("logistic_regression_model.pkl","wb") as f:
   pickle.dump(logistic_model,f)

with open("decision_tree_model.pkl","wb") as f:
   pickle.dump(decision_tree_model,f)

with open("random_forest_model.pkl","wb") as f:
   pickle.dump(forest_model,f)


