# אימון המודל
import numpy as np
import pandas as pd
import sqlalchemy

# לגרפים
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc


# יבוא של פונקציית טהירות, מטריצת בלבול
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, recall_score
# יבוא של פונקציית נרמול
from sklearn.preprocessing import minmax_scale
# חלןקת הנתונים לקבוצת אימון וקבוצת מבחן, עירבוב הנתונים
from sklearn.model_selection import train_test_split

# יבוא של מודל רגרסיה לוגיסטית
from sklearn.linear_model import LogisticRegression
# יבוא של מודל יער אקראי
from sklearn.ensemble import RandomForestClassifier

# משתנים
# שם השרת
server = 'localhost'
# שם הדאטה בייס
database = 'ChurnDB'
# שם הדרייבר
driver = 'ODBC+Driver+17+for+SQL+Server'
# כל הפרטים מחוברים יחד כדי להיכנס לתוך הפונקציה הבאה
# בגלל שניכנס לתוך connection_url במקום רווחים כתבתי + כדי שהקובץ ידע לקרוא אותו
connection_url = f"mssql+pyodbc://{server}/{database}?driver={driver}&trusted_connection=yes"
# שלב החיבור
# פונקציה זו היא הצינור
# הפונקציה מתרגמת את פרטי החיבור (שרת, דרייבר וכו') לאובייקט שמנהל את התקשורת מול ה-SQL, כך שלא צריך לפתוח חיבור ידנית בכל פעם ששולחים פקודה
engine = sqlalchemy.create_engine(connection_url)
#קריאה של הנתונים המתוקנים מה-SQL
# קריאה של הנתונים מ-v_clean_data שזה הטבלה הוירטואלית שיצרנו עם הנתונים המסודרים
df = pd.read_sql ("SELECT * FROM v_clean_data" ,engine)
# בדיקה שעבר וקרא את כל הדאטה מה-SQL
# מדפיס את ה-5 שורות הראשונות של הטבלה
# לא נדפיס את הכל כדי לא להציף את המחשב
print(df.head())

# הגדרה של העמודות שנרצה כפיצארים
# לקחנו את: חיוב חודשי, קביעות, סך הוצאות נקי
features = ['MonthlyCharges', 'tenure', 'total_charges_clean', 'Contract', 'InternetService', ]

# קודם כל שולפים את הטבלה עם הפיצ'רים הרלוונטיים
X_temp = df[features]
# עכשיו הופכים את הטקסט למספרים ושומרים לתוך X
X = pd.get_dummies(X_temp, columns=['Contract', 'InternetService', ], drop_first=True)
# הגדרה של מה יהיה פיצ'ר המטרה שלנו
Y = df['churn_label']

# נרמול הנתונים
x_norm = minmax_scale(X)

# הדפסת גודל  X
print("X shape:", X.shape)
# הדפסת גודל  Y
print("y shape:", Y.shape)

# חיתוך הנתונים
# נשמור למבחן 20%
# 42 - מבטיח שהערבוב יהיה זהה בכל פעם
X_train, X_test, Y_train, Y_test = train_test_split(x_norm, Y, test_size=0.2, random_state=42, stratify=Y)

# הדפסה כדי לבדוק את חלוקת הנתונים
print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)

# ------------ אימון מודל רגרסיה לוגיסטית ------------
# קריאה לבנאי של המודל
logistic_model = LogisticRegression(class_weight='balanced')
# אימוד המודל על הנתונים
logistic_model.fit(X_train, Y_train)
# חיזוי בעזרת המודל
y_predict_logistic_model = logistic_model.predict(X_test)

# הדפסות
# הדפסת שורה ריקה
print()
# הדפסת כותרת
print ("----------Logistic Regression Results---------- \n")
# מדד טהירות המודל
accuracy_score_logistic_model = accuracy_score(Y_test, y_predict_logistic_model)
# עיגול לשתי ספרות אחרי הנקודה
print ("Accuracy Score:",round (accuracy_score_logistic_model,3),"\n")
# מטריצת בלבול
print("Confusion Matrix: \n", confusion_matrix(Y_test, y_predict_logistic_model), "\n")
# דוח מסודר שמציג את כל המדדים
print("Classification Report: \n", classification_report(Y_test, y_predict_logistic_model))
# הדפסת recall score
print ("Recall Score:", recall_score(Y_test, y_predict_logistic_model))


# ------------ בדיקת חשיבות הפיצ'רים (המשקולות של המודל רגרסיה לוגיסטית) ------------

# יצירת טבלה המכילה את שם הפיצ'ר והמשקל שהמודל נתן לו
feature_importance_logistic_model = pd.DataFrame({
    #  שמות הפיצארים שורות
    'Feature': X.columns,
    # המשקל של כל הפיצארים עמודה
    'Weight': logistic_model.coef_[0]
})

# הוספת עמודה של ערך מוחלט כדי שנוכל למיין מהפיצ'ר הכי משפיע להכי פחות
feature_importance_logistic_model['Absolute_Weight'] = feature_importance_logistic_model['Weight'].abs()
# ממין לפי הפיצר שהכי משפיע על המודל
feature_importance_logistic_model = feature_importance_logistic_model.sort_values(by='Absolute_Weight', ascending=False)

# הדפסת הטבלה המסודרת
print("\n---------- Feature Importance (Weights) ----------\n")
print(feature_importance_logistic_model[['Feature', 'Weight']],"\n")

# הסיכוי שבה המודל סיווג כל דגימה
p = logistic_model.predict_proba(X_train)


# ------------ אימון מודל יער אקראי ------------
# קריאה לבנאי של המודל
rf_model = RandomForestClassifier(class_weight='balanced')
# אימוד המודל על הנתונים
rf_model.fit(X_train, Y_train)
# חיזוי בעזרת המודל
y_predict_rf_model = rf_model.predict(X_test)

# הדפסות
# הדפסת שורה ריקה
print()
# הדפסת כותרת
print ("---------- Random Forest Results---------- \n")
# מדד טהירות המודל
accuracy_score_rf_model = accuracy_score(Y_test, y_predict_rf_model)
# עיגול לשתי ספרות אחרי הנקודה
print ("Accuracy Score:",round (accuracy_score_rf_model,3),"\n")
# מטריצת בלבול
print("Confusion Matrix: \n", confusion_matrix(Y_test, y_predict_rf_model), "\n")
# דוח מסודר שמציג את כל המדדים
print("Classification Report: \n", classification_report(Y_test, y_predict_rf_model))
# הדפסת recall score
print ("Recall Score:", recall_score(Y_test, y_predict_rf_model))


# ------------ בדיקת חשיבות הפיצ'רים (המשקולות של המודל יער אקראי ) ------------

# יצירת טבלה המכילה את שם הפיצ'ר והמשקל שהמודל נתן לו
feature_importance_rf_model = pd.DataFrame({
    #  שמות הפיצארים שורות
    'Feature': X.columns,
    # המשקל של כל הפיצארים עמודה
    'Weight': rf_model.feature_importances_
})

# הוספת עמודה של ערך מוחלט כדי שנוכל למיין מהפיצ'ר הכי משפיע להכי פחות
feature_importance_rf_model['Absolute_Weight'] = feature_importance_rf_model['Weight'].abs()
# ממין לפי הפיצר שהכי משפיע על המודל
feature_importance_rf_model = feature_importance_rf_model.sort_values(by='Absolute_Weight', ascending=False)

# הדפסת הטבלה המסודרת
print("\n---------- Feature Importance (Weights) ----------\n")
print(feature_importance_rf_model[['Feature', 'Weight']],"\n")

# הסיכוי שבה המודל סיווג כל דגימה
p = rf_model.predict_proba(X_train)


# --------------גרף 1 --------------
# עושה דף חדש לגרף וקובע גודל
plt.figure(figsize=(10, 6))

# שימוש בנתונים מהטבלה של משקל כל פיצאר
sns.barplot(x='Weight', y='Feature', data=feature_importance_logistic_model, hue='Feature', palette='viridis', legend=False)
# כותרת ראשית
plt.title('Logistic Regression - Feature Importance')
# כותרת ציר X
plt.xlabel('Weight (Impact on Churn)')
# כותרת ציר Y
plt.ylabel('Feature')

# הוספת קו אנכי על ה-0 כדי להראות מה משפיע לחיוב ומה לשלילה
plt.axvline(x=0, color='black', linestyle='--')
plt.tight_layout()
# הצגת הגרף
plt.show()


# --------------גרף 2 --------------
# עושה דף חדש לגרף וקובע גודל
plt.figure(figsize=(10, 6))

# שימוש בנתונים מהטבלה של משקל כל פיצאר
sns.barplot(x='Weight', y='Feature', data=feature_importance_rf_model, hue='Feature', palette='viridis', legend=False)
# כותרת ראשית
plt.title('Random Forest - Feature Importance')
# כותרת ציר X
plt.xlabel('Weight (Impact on Churn)')
# כותרת ציר Y
plt.ylabel('Feature')

plt.tight_layout()
# הצגת הגרף
plt.show()

# --------------גרף 3 --------------
# גרף עקומה
# TPR -  אומר שהמודל זיהה נכון לקוח שעזב
# FPR -  אזעקת שווא המודל חשב שהלקוח עוזב ובפועל הוא לא עצב

# פונקיות
# predict_proba - (מחזיר 2 עמודות) מחזיר את ההסיתברות שהלקוח יעזוב ואת ההיסתברות שישאר לפי הפיצרים של המבחן
# אנחנו משתמשים רק בעמודה של העוזבים (ך נראה את הסיכויים לנטישה של כל לקוח בקבוצת המבחן) - [:, 1]

# חישוב הסיכויים  לכל מודל
# מודל רגרסיה לוגיטית
fpr_log, tpr_log, _ = roc_curve(Y_test, logistic_model.predict_proba(X_test)[:, 1])
# מודל יער רנדומאלי
fpr_rf, tpr_rf, _ = roc_curve(Y_test, rf_model.predict_proba(X_test)[:, 1])

# חישוב השטח שמתחת לעקומה
# הציון  של המודל
# כמה זיהה וכמה עשה אזעקת שווא
roc_auc_log = auc(fpr_log, tpr_log)
roc_auc_rf = auc(fpr_rf, tpr_rf)

# עושה דף חדש לגרף וקובע גודל
plt.figure(figsize=(8, 6))

# ציור העקומות
plt.plot(fpr_log, tpr_log, color='blue', label=f'Logistic Regression (AUC = {roc_auc_log:.2f})')
plt.plot(fpr_rf, tpr_rf, color='green', label=f'Random Forest (AUC = {roc_auc_rf:.2f})')

# קו אקראי (מודל שמנחש 50-50)
plt.plot([0, 1], [0, 1], color='red', linestyle='--')

# כותרת ראשית
plt.title('ROC Curve - Model Comparison')
# כותרת ציר X
plt.xlabel('False Positive Rate')
# כותרת ציר Y
plt.ylabel('True Positive Rate')
# מקרא
plt.legend(loc='lower right')
# הצגת הגרף
plt.show()