import pandas as pd
import sqlalchemy
import urllib

# 1. הגדרת פרטי החיבור
server = 'localhost'  # <-- כאן תדביקי את שם השרת שהעתקת מ-SSMS
database = 'ChurnDB'
driver = 'ODBC Driver 17 for SQL Server' # בדרך כלל זה הדרייבר המותקן. אם לא עובד, נסה 'SQL Server'

# 2. יצירת מחרוזת החיבור (Connection String)
# אנחנו משתמשים ב-Trusted_Connection=yes כדי להתחבר עם המשתמש של הווינדוס (בלי סיסמה)
connection_string = f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

# 3. יצירת המנוע של SQLAlchemy
params = urllib.parse.quote_plus(connection_string)
engine = sqlalchemy.create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# 4. בדיקה שזה עובד
try:
    with engine.connect() as conn:
        print("✅ ההתחברות ל-SQL Server הצליחה!")
except Exception as e:
    print("❌ שגיאה בהתחברות:", e)
