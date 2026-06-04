
import pandas as pd
import sqlalchemy
import urllib

# יצירת נתיב לקובץ CSV
file_path = "Customer_Data.csv"

# קריאה של הקובץ
# טיפוס טבלה dataFrame
df = pd.read_csv(file_path)

# בדיקה של כמה שורות וכמה עמודות יש בקוצץ והאם הוא קריא
# 7043 שורות,  21 עמודות
print ("Data shape:", df.shape)

# תצודה של 5 השורות הראשונות
print(df.head())

# משתנים
# שם השרת
server = r'.\SQLEXPRESS'
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


# פונקציה זו היא חברת ההובלות והמתורגמנית שלנו, היא מעבירה את הנתונים ל-SQL
# פונקציה זו חוסכת לנו קליטת נתונים ידנית של ה-7043 שורות שיש בדאטה בייס
# המשתנים שהכנסנו לתוכה:
# את השם שאני רוצה שיקראו לטבלה ב-SQL,
# דרך איזה צינור להעביר את המידע (שזה המשתנה enging שיצרתי קודם),
# מה לעשות את קיימת טבלה כזו (למחוק אוותה),
# איך לשמור את מספור העמודות (נהפוך את המספרי העמודות לערך בוליאני
df.to_sql('raw_data_staging', engine, if_exists='replace', index=False)