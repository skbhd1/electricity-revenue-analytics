# =============================================================================
# Bad Debt Risk Predictor — Machine Learning Pipeline
# Author  : Shaik Abdullah
# GitHub  : github.com/skbhd1/electricity-revenue-analytics
# Model   : Random Forest Classifier
# Dataset : 138,509 consumer billing records | 16 columns
# Tools   : Python, scikit-learn, pandas, NumPy, matplotlib, seaborn
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
import os

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (classification_report, confusion_matrix,
                             roc_auc_score, roc_curve, ConfusionMatrixDisplay)
from sklearn.preprocessing import LabelEncoder

warnings.filterwarnings("ignore")

# ── 0. CONFIG ─────────────────────────────────────────────────────────────────

INPUT_FILE  = "Project_Data_Set_-_27_03_2026.xlsx"
OUTPUT_DIR  = "ml_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

BRAND_BLUE  = "#1F3864"
BRAND_MID   = "#2E5090"
COLOR_RED   = "#E24B4A"
COLOR_GREEN = "#1D9E75"
COLOR_AMBER = "#EF9F27"

plt.rcParams.update({
    "font.family"       : "DejaVu Sans",
    "axes.spines.top"   : False,
    "axes.spines.right" : False,
    "axes.grid"         : True,
    "grid.alpha"        : 0.3,
    "grid.linestyle"    : "--",
})

# ── 1. LOAD DATA ──────────────────────────────────────────────────────────────

print("=" * 65)
print("  BAD DEBT RISK PREDICTOR — ML PIPELINE")
print("  Shaik Abdullah | github.com/skbhd1")
print("=" * 65)

print("\n[1/7] Loading dataset...")
df = pd.read_excel(INPUT_FILE)
print(f"      Loaded : {df.shape[0]:,} rows × {df.shape[1]} columns")

# ── 2. FEATURE ENGINEERING ────────────────────────────────────────────────────

print("\n[2/7] Engineering features...")

# Clean outliers — cap collection ratio
df['Collection_Ratio_Clean'] = df['Collection Ratio'].clip(0, 2)

# Leakage ratio
df['Leakage_Ratio'] = np.where(
    df['Total Billing'] > 0,
    (df['Total Billing'] - df['Total Receipting']) / df['Total Billing'],
    0
).clip(0, 1)

# High debt flag
df['High_Debt_Flag'] = (df['Total 90 Debt'] > df['Total 90 Debt'].quantile(0.75)).astype(int)

# Zero collection flag
df['Zero_Collection'] = (df['Collection Ratio'] == 0).astype(int)

# Log transforms for skewed columns
for col in ['Total Billing', 'Total Receipting', 'Total 90 Debt',
            'Property Value', 'Total Write Off']:
    df[f'Log_{col.replace(" ", "_")}'] = np.log1p(df[col].clip(0))

# Encode Account Category
le = LabelEncoder()
df['Category_Encoded'] = le.fit_transform(df['Account Category'])

print(f"      Features engineered : {df.shape[1] - 16} new columns added")

# ── 3. PREPARE MODEL INPUT ────────────────────────────────────────────────────

print("\n[3/7] Preparing model input...")

FEATURES = [
    'Account Category ID',
    'Property Value',
    'Property Size',
    'Total Billing',
    'Avg Billing',
    'Total Receipting',
    'Avg Receipting',
    'Total 90 Debt',
    'Total Write Off',
    'Debt Billing Ratio',
    'Total Elec Bill',
    'Has ID No',
    'Collection_Ratio_Clean',
    'Leakage_Ratio',
    'High_Debt_Flag',
    'Zero_Collection',
    'Log_Total_Billing',
    'Log_Total_Receipting',
    'Log_Total_90_Debt',
    'Log_Property_Value',
    'Log_Total_Write_Off',
    'Category_Encoded',
]

TARGET = 'Bad Debt'

X = df[FEATURES]
y = df[TARGET]

print(f"      Features used  : {len(FEATURES)}")
print(f"      Target classes : Bad Debt={y.sum():,} | Good={len(y)-y.sum():,}")
print(f"      Class balance  : {y.mean()*100:.1f}% bad debt rate")

# ── 4. TRAIN / TEST SPLIT ─────────────────────────────────────────────────────

print("\n[4/7] Splitting data and training model...")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"      Training set : {len(X_train):,} records")
print(f"      Test set     : {len(X_test):,} records")

# ── 5. TRAIN RANDOM FOREST ────────────────────────────────────────────────────

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    min_samples_split=20,
    min_samples_leaf=10,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)
print("      Model trained successfully ✓")

# Predictions
y_pred       = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Scores
accuracy  = (y_pred == y_test).mean() * 100
roc_auc   = roc_auc_score(y_test, y_pred_proba) * 100
cv_scores = cross_val_score(model, X, y, cv=5, scoring='roc_auc', n_jobs=-1)

print(f"\n  {'METRIC':<35} {'VALUE':>10}")
print(f"  {'-'*45}")
print(f"  {'Model Accuracy':<35} {accuracy:>9.1f}%")
print(f"  {'ROC-AUC Score':<35} {roc_auc:>9.1f}%")
print(f"  {'Cross-Validation AUC (5-fold)':<35} {cv_scores.mean()*100:>9.1f}%")
print(f"  {'CV Std Dev':<35} {cv_scores.std()*100:>9.2f}%")

print("\n  Classification Report:")
print(classification_report(y_test, y_pred,
      target_names=['Good Standing', 'Bad Debt']))

# ── 6. VISUALISATIONS ─────────────────────────────────────────────────────────

print("\n[5/7] Generating charts...")

# ── Chart 1: Feature Importance ──
feature_importance = pd.DataFrame({
    'Feature' : FEATURES,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=True).tail(12)

fig, ax = plt.subplots(figsize=(10, 6))
colors = [COLOR_RED if v > 0.1 else COLOR_AMBER if v > 0.05 else BRAND_MID
          for v in feature_importance['Importance']]
bars = ax.barh(feature_importance['Feature'], feature_importance['Importance'],
               color=colors, height=0.6, zorder=2)
for bar, val in zip(bars, feature_importance['Importance']):
    ax.text(val + 0.002, bar.get_y() + bar.get_height()/2,
            f"{val*100:.1f}%", va='center', fontsize=9)
ax.set_xlabel("Feature Importance Score", fontsize=10)
ax.set_title("Top 12 Features — Bad Debt Risk Predictor",
             fontsize=13, fontweight='bold', color=BRAND_BLUE)
plt.tight_layout()
out1 = os.path.join(OUTPUT_DIR, "01_feature_importance.png")
plt.savefig(out1, dpi=150, bbox_inches='tight')
plt.close()
print(f"      Saved: {out1}")

# ── Chart 2: ROC Curve ──
fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(fpr, tpr, color=BRAND_MID, linewidth=2,
        label=f'Random Forest (AUC = {roc_auc:.1f}%)')
ax.plot([0, 1], [0, 1], color=COLOR_RED, linestyle='--',
        linewidth=1, label='Random baseline (50%)')
ax.fill_between(fpr, tpr, alpha=0.1, color=BRAND_MID)
ax.set_xlabel("False Positive Rate", fontsize=11)
ax.set_ylabel("True Positive Rate", fontsize=11)
ax.set_title("ROC Curve — Bad Debt Risk Model",
             fontsize=13, fontweight='bold', color=BRAND_BLUE)
ax.legend(fontsize=10)
plt.tight_layout()
out2 = os.path.join(OUTPUT_DIR, "02_roc_curve.png")
plt.savefig(out2, dpi=150, bbox_inches='tight')
plt.close()
print(f"      Saved: {out2}")

# ── Chart 3: Confusion Matrix ──
fig, ax = plt.subplots(figsize=(7, 5))
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                               display_labels=['Good Standing', 'Bad Debt'])
disp.plot(ax=ax, colorbar=False, cmap='Blues')
ax.set_title("Confusion Matrix — Predictions vs Reality",
             fontsize=13, fontweight='bold', color=BRAND_BLUE)
plt.tight_layout()
out3 = os.path.join(OUTPUT_DIR, "03_confusion_matrix.png")
plt.savefig(out3, dpi=150, bbox_inches='tight')
plt.close()
print(f"      Saved: {out3}")

# ── Chart 4: Risk Score Distribution ──
df_full_proba = model.predict_proba(X)[:, 1]
df['Risk_Score'] = df_full_proba
df['Risk_Score_Pct'] = (df['Risk_Score'] * 100).round(1)

fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(df[df['Bad Debt']==0]['Risk_Score_Pct'], bins=50,
        alpha=0.7, color=COLOR_GREEN, label='Good Standing', zorder=2)
ax.hist(df[df['Bad Debt']==1]['Risk_Score_Pct'], bins=50,
        alpha=0.7, color=COLOR_RED, label='Bad Debt', zorder=2)
ax.axvline(x=50, color=BRAND_BLUE, linestyle='--',
           linewidth=1.5, label='Decision threshold (50%)')
ax.set_xlabel("Predicted Risk Score (%)", fontsize=11)
ax.set_ylabel("Number of Accounts", fontsize=11)
ax.set_title("Risk Score Distribution — Good vs Bad Debt Accounts",
             fontsize=13, fontweight='bold', color=BRAND_BLUE)
ax.legend(fontsize=10)
plt.tight_layout()
out4 = os.path.join(OUTPUT_DIR, "04_risk_score_distribution.png")
plt.savefig(out4, dpi=150, bbox_inches='tight')
plt.close()
print(f"      Saved: {out4}")

# ── Chart 5: Average Risk Score by Category ──
cat_risk = df.groupby('Account Category')['Risk_Score_Pct'].mean().sort_values(ascending=True)
fig, ax = plt.subplots(figsize=(10, 5))
bar_colors = [COLOR_RED if v > 60 else COLOR_AMBER if v > 45 else COLOR_GREEN
              for v in cat_risk]
bars = ax.barh(cat_risk.index, cat_risk.values, color=bar_colors, height=0.6, zorder=2)
ax.axvline(x=50, color=BRAND_BLUE, linestyle='--', linewidth=1.2,
           label='50% risk threshold')
for bar, val in zip(bars, cat_risk.values):
    ax.text(val + 0.3, bar.get_y() + bar.get_height()/2,
            f"{val:.1f}%", va='center', fontsize=9)
ax.set_xlabel("Average Predicted Risk Score (%)", fontsize=10)
ax.set_title("Average Bad Debt Risk Score by Account Category",
             fontsize=13, fontweight='bold', color=BRAND_BLUE)
ax.legend(fontsize=9)
plt.tight_layout()
out5 = os.path.join(OUTPUT_DIR, "05_risk_by_category.png")
plt.savefig(out5, dpi=150, bbox_inches='tight')
plt.close()
print(f"      Saved: {out5}")

# ── 7. EXPORT PREDICTION REPORT ───────────────────────────────────────────────

print("\n[6/7] Exporting prediction report...")

# Add risk labels
df['Risk_Label'] = pd.cut(
    df['Risk_Score_Pct'],
    bins=[0, 30, 50, 70, 100],
    labels=['Low Risk', 'Medium Risk', 'High Risk', 'Critical Risk']
)

# Top feature names (human readable)
feature_labels = {
    'Log_Total_90_Debt'    : '90-Day Debt Amount',
    'Collection_Ratio_Clean': 'Collection Ratio',
    'Leakage_Ratio'        : 'Revenue Leakage Ratio',
    'Log_Total_Billing'    : 'Total Billing Amount',
    'Zero_Collection'      : 'Zero Collection Flag',
    'High_Debt_Flag'       : 'High Debt Flag',
    'Has ID No'            : 'Has ID Number',
    'Log_Property_Value'   : 'Property Value',
    'Log_Total_Receipting' : 'Total Receipting',
    'Category_Encoded'     : 'Account Category',
}

# Export columns
export_cols = [
    'Account Category', 'Acc Cat Abbr',
    'Total Billing', 'Total Receipting',
    'Total 90 Debt', 'Collection Ratio',
    'Has ID No', 'Bad Debt',
    'Risk_Score_Pct', 'Risk_Label'
]

# Top 5000 highest risk
top_risk = df.sort_values('Risk_Score_Pct', ascending=False).head(5000)

# Summary by category
cat_summary = df.groupby('Account Category').agg(
    Total_Accounts     = ('Bad Debt', 'count'),
    Avg_Risk_Score     = ('Risk_Score_Pct', 'mean'),
    Critical_Risk_Count= ('Risk_Label', lambda x: (x == 'Critical Risk').sum()),
    High_Risk_Count    = ('Risk_Label', lambda x: (x == 'High Risk').sum()),
    Actual_Bad_Debt    = ('Bad Debt', 'sum'),
    Predicted_Bad_Debt = ('Risk_Score_Pct', lambda x: (x >= 50).sum()),
).round(2).reset_index()

# Model performance summary
model_summary = pd.DataFrame({
    'Metric': ['Model Type', 'Total Records', 'Training Records',
               'Test Records', 'Model Accuracy', 'ROC-AUC Score',
               'Cross-Validation AUC', 'Features Used',
               'Bad Debt Predicted (>50% risk)', 'Critical Risk Accounts (>70%)'],
    'Value': ['Random Forest Classifier', f'{len(df):,}',
              f'{len(X_train):,}', f'{len(X_test):,}',
              f'{accuracy:.1f}%', f'{roc_auc:.1f}%',
              f'{cv_scores.mean()*100:.1f}%', str(len(FEATURES)),
              f'{(df["Risk_Score_Pct"] >= 50).sum():,}',
              f'{(df["Risk_Score_Pct"] >= 70).sum():,}']
})

# Feature importance table
fi_table = pd.DataFrame({
    'Feature': [feature_labels.get(f, f) for f in FEATURES],
    'Raw_Name': FEATURES,
    'Importance_%': (model.feature_importances_ * 100).round(2)
}).sort_values('Importance_%', ascending=False)

excel_path = os.path.join(OUTPUT_DIR, "Bad_Debt_Risk_Prediction_Report.xlsx")
with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    model_summary.to_excel(writer, sheet_name='Model Performance', index=False)
    cat_summary.to_excel(writer, sheet_name='Risk by Category', index=False)
    top_risk[export_cols].to_excel(writer, sheet_name='Top 5000 High Risk', index=False)
    fi_table.to_excel(writer, sheet_name='Feature Importance', index=False)
    df[export_cols].to_excel(writer, sheet_name='All Accounts with Score', index=False)

print(f"      Excel report saved: {excel_path}")

# ── 8. FINAL SUMMARY ──────────────────────────────────────────────────────────

top_features = fi_table.head(3)

print("\n[7/7] Key Results\n")
print("  ┌──────────────────────────────────────────────────────────┐")
print(f"  │  Model accuracy          : {accuracy:.1f}%                      │")
print(f"  │  ROC-AUC score           : {roc_auc:.1f}%                      │")
print(f"  │  Cross-validation AUC    : {cv_scores.mean()*100:.1f}%                      │")
print(f"  │  Accounts scored         : {len(df):,}               │")
print(f"  │  Predicted bad debt (>50%): {(df['Risk_Score_Pct']>=50).sum():,}               │")
print(f"  │  Critical risk (>70%)    : {(df['Risk_Score_Pct']>=70).sum():,}                │")
print(f"  │  Top predictor           : {top_features.iloc[0]['Feature']:<26}   │")
print(f"  │  2nd predictor           : {top_features.iloc[1]['Feature']:<26}   │")
print(f"  │  3rd predictor           : {top_features.iloc[2]['Feature']:<26}   │")
print("  └──────────────────────────────────────────────────────────┘")

print(f"\n  All outputs saved to: ./{OUTPUT_DIR}/")
print("\n  Files generated:")
for f in sorted(os.listdir(OUTPUT_DIR)):
    size = os.path.getsize(os.path.join(OUTPUT_DIR, f))
    print(f"    ✓ {f:<50} ({size/1024:.0f} KB)")

print("\n" + "=" * 65)
print("  ML Pipeline complete.")
print("=" * 65)
