# הצגת הנתונים בצורה גרפית
from itertools import groupby

import pandas as pd
import sqlalchemy
import urllib
import matplotlib.pyplot as plt

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

# כמה לקוחות עזבו וכמה נשארו
# פונקציה קיימת בפנדס שעושה את ספירת הערכים
# נבקש ממנה לקרוא את הערכים מהדאטה שלנו מהעמודה שנקראת 'churn_label'
counts = df['churn_label'].value_counts()

# ציור של נתונים אלו בגרף
# סוג סרטוט: עוגה
# תציד את האחוז של כל פרוסה כמספר עשרוני עם מספר 1 אחרי הנקודה
# כותרות לגרף
counts.plot(kind='pie', autopct='%1.1f%%', labels=['Stayed', 'Left'])
# הגדרת כורתרת ראשית לתרשים
plt.title('Churn Label Distribution')
#הגדרה של כותרת ציר Y כ-ריקה
plt.ylabel("")
# הצגת התנתונים
plt.show()



# דף חדש שבוא אין ציור של הגרף הקודם
plt.figure()
# גרף היסטוגרמה
# בודק את העמודה של עזיבה
# רמת שקיפות הגרפים כדי שנראה אותם כשהם אחד על השני
# כותרת \ תווית מה כל צבע אומר
# צבע הגרף

# גרף 1
# בודק אם שווה ל-0 כלומר לא עזב
# הולך לאלא שלא עזבו ובודק בעמודה של התשלומים מה ההחזר תשלומים שלהם
plt.hist(df[df['churn_label'] ==0]['MonthlyCharges'], alpha=0.5, label='Stayed', bins=30, color='green')
# גרף 2
plt.hist(df[df['churn_label'] ==1]['MonthlyCharges'], alpha=0.5, label='Left', bins=30, color='red')

# הוספת כותרת ראשית
plt.title('Monthly Charges Distribution by Churn')
# הוספת כותרת לציר X
plt.xlabel('Monthly Charges ($)')
# הוספת כותרת לציר Y
plt.ylabel('Number of Customers')
# תוספת מקרא מי אדום ומי ירוק
plt.legend()

# הצגת הגרף
plt.show()

# דף חדש שבוא אין ציור של הגרפים הקודמים
plt.figure()

# גרף 4
# האם אנשים בלי התחייבות עוזבים יותר
# האם לקוחות חדשים נמצאים בסיכון יותר גבוהה

contract_churn = df.groupby('Contract')['churn_label'].mean()
contract_churn.plot (kind = 'bar' )
plt.title('Contract Churn Distribution')

# כותרת ציר X
plt.xlabel('contract type')
# כותרת ציר Y
plt.ylabel('Number of Customers')

# תסדרי מספיק רווח לפי הכותרות שלא יחתכו
plt.tight_layout()
# הצגת הגרף
plt.show()

# דף חדש שבוא אין ציור של הגרפים הקודמים
plt.figure()
# גרף 5
# היסטוגרמה שמראה וותק לעומת עזיבה

plt.hist(df[df['churn_label'] == 1]['tenure'], bins=30, color='orange', edgecolor='black')

#הוספת כותרת ראשית
plt.title('Tenure of Customers Who Left')
#  כותרת לציר X
plt.xlabel('Tenure (Months)')
#  כותרת לציר Y
plt.ylabel('Number of Customers Left')
# הצגת מקרא
plt.tight_layout()

# הצגת הגרף
plt.show()