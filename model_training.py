# אימון המודל

import pandas as pd
import sqlalchemy
import urllib
# חלןקת הנתונים לקבוצת אימון וקבוצת מבחן
from sklearn.model_selection import train_test_split

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

# הגדרה של שלושת הפיצרים שבהם נשתמש
features = ['MonthlyCharges','tenure','total_charges_clean']
X = df[features]
Y = df['churn_label']

# הדפסת גודל  X
print("X shape:", X.shape)
# הדפסת גודל  Y
print("y shape:", Y.shape)

# חיתוך הנתונים
# נשמור למבחן 20%
# 42 - מבטיח שהערבוב יהיה זהה בכל פעם
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
# הדפסה כדי לבדוק את חלוקת הנתונים
print (X_train.shape)
print(X_test.shape)