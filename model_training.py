# אימון המודל
import numpy as np
import pandas as pd
import sqlalchemy
import urllib
import matplotlib.pyplot as plt
from nltk import accuracy
from sklearn.metrics import accuracy_score, confusion_matrix

# יבוא של פונקציית טהירות, מטריצת בלבול
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
# יבוא של פונקציית נרמול
from sklearn.preprocessing import minmax_scale
# חלןקת הנתונים לקבוצת אימון וקבוצת מבחן, עירבוב הנתונים
from sklearn.model_selection import train_test_split

# יבוא של מודל רגרסיה לוגיסטית
from sklearn.linear_model import LogisticRegression


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

# בגדרה של העמודות שנרצה כפיצאים
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

# אימון מודל
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
accuracy_score = accuracy_score(Y_test, y_predict_logistic_model)
# עיגול לשתי ספרות אחרי הנקודה
print ("Accuracy Score:",round (accuracy_score,3),"\n")
# מטריצת בלבול
print("Confusion Matrix: \n", confusion_matrix(Y_test, y_predict_logistic_model), "\n")
# דוח מסודר שמציג את כל המדדים
print("Classification Report: \n", classification_report(Y_test, y_predict_logistic_model))



# בדיקת חשיבות הפיצ'רים (המשקולות של המודל)

# יצירת טבלה המכילה את שם הפיצ'ר והמשקל שהמודל נתן לו
feature_importance = pd.DataFrame({
    #  שמות הפיצארים שורות
    'Feature': X.columns,
    # המשקל של כל הפיצארים עמודה
    'Weight': logistic_model.coef_[0]
})

# הוספת עמודה של ערך מוחלט כדי שנוכל למיין מהפיצ'ר הכי משפיע להכי פחות
feature_importance['Absolute_Weight'] = feature_importance['Weight'].abs()
# ממין לפי הפיצר שהכי משפיע על המודל
feature_importance = feature_importance.sort_values(by='Absolute_Weight', ascending=False)

# הדפסת הטבלה המסודרת
print("\n---------- Feature Importance (Weights) ----------\n")
print(feature_importance[['Feature', 'Weight']],"\n")

# הסיכוי שבה המודל סיווג כל דגימה
p = logistic_model.predict_proba(X_train)


