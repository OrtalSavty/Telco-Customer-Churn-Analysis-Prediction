# הצגת הנתונים בצורה גרפית
import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plt
import seaborn as sns

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

#קריאה של הנתונים המתוקנים מה-SQL
# קריאה של הנתונים מ-v_clean_data שזה הטבלה הוירטואלית שיצרנו עם הנתונים המסודרים
df = pd.read_sql ("SELECT * FROM v_clean_data" ,engine)

# בדיקה שעבר וקרא את כל הדאטה מה-SQL
# מדפיס את ה-3 שורות הראשונות של הטבלה
# לא נדפיס את הכל כדי לא להציף את המחשב
print(df.head(3))

# --------------גרף 1 --------------
# kind - סוג גרף במקרה זה גרף עוגה
# חישוב האחוזים של כל פרוסה וכתיבה שלהם  בתוך העוגה - autopct
# labels - השמות של כל פרוסת עוגה

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

# --------------גרף 2 --------------
# דף חדש שבוא אין ציור של הגרף הקודם
plt.figure()
# גרף היסטוגרמה משתי גרפים
# alpha - שקיפות הגרף
# label - מקרא
# bins - מגדיל את מספר העמודות בגרף

# היסטוגרמה 1
# בודק אם שווה ל-0 כלומר לא עזב
# ואז הולך לאלא שלא עזבו ובודק בעמודה של התשלומים מה ההחזר תשלומים שלהם
plt.hist(df[df['churn_label'] ==0]['MonthlyCharges'], alpha=0.5, label='Stayed', bins=30, color='green')

# היסטוגרמה 2
# בודק אם שווה ל-0 כלומר לא עזב
# ואז הולך לאלא שלא עזבו ובודק בעמודה של התשלומים מה ההחזר תשלומים שלהם
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

# --------------גרף 3 --------------
# דף חדש שבוא אין ציור של הגרפים הקודמים
plt.figure()

# האם אנשים בלי התחייבות עוזבים יותר
# האם לקוחות חדשים נמצאים בסיכון יותר גבוהה
# kind - סוג הגרף במקרה זה גרף עמודות
# figsize - גודל התמונה (רוחב, גובה)

# חישוב אחוז נטישה
contract_churn = df.groupby('Contract')['churn_label'].mean() * 100
# הגת הנתונים
contract_churn.plot(kind='bar', color='skyblue', figsize=(8,5))

# כותרת ראשית לגרף
plt.title('Contract Churn Distribution')
# כותרת ציר X
plt.xlabel('contract type')
# כותרת ציר Y
plt.ylabel('Percent of Customers')
#  רווח לפי הכותרות שלא יחתכו
plt.tight_layout()
# הצגת הגרף
plt.show()


# --------------גרף 4 --------------
# דף חדש שבוא אין ציור של הגרפים הקודמים
plt.figure()
# edgecolor - צבע מסגרת של הגרף

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


# --------------גרף 5 --------------
# דף חדש שבוא אין ציור של הגרפים הקודמים
plt.figure(figsize=(10, 5))

# גרך הערכת צפיפות חלקה - מראה איפה מרוכזים רוב הלקוחות
# figsize - קובע את גודל הדף שאנחנו פותחים לתמונה (רוחב, גובה)
# hue - במקום הר אחד תצייר שתי הרים של אלו שעזבו ושל אלו שנשארו
# fill - צובע את השטח מתחת לקו
# common_norm - נירמול של כל קבוצה בנפרד (התעלמות מזה שיש קצת עוזבים לעומת נשארים כדי שנוכל להראות זאת בצורה יפה ונוחה בגרף)
# palette - קביעת צבע לכל גרף

# KDE יוצר גרף התפלגות כמו הרים לפי קבוצות
# ציר ה-X ייצג את וותק הלקוחות
sns.kdeplot(data=df, x='tenure', hue='churn_label', fill=True, common_norm=False, palette=['green', 'red'])

#  כותרת  ראשית לגרף
plt.title('Customer Tenure Distribution by Churn')
#  כותרת לציר X
plt.xlabel('Tenure (Months)')
#  כותרת לציר Y
plt.ylabel('Density')
# מקרא
plt.legend(["Stayed", "Left"])
#  הצגת הגרף
plt.show()



# --------------גרף 7 --------------

# פתיחת דף חדש לגרףוקביעת גודל הגרף
plt.figure(figsize=(10, 6))
# יצירת גרף עמודות. ציר X הוא סוג האינטרנט, ציר Y הוא אחוז הנטישה
ax = sns.barplot(x='InternetService', y='churn_label', data=df, errorbar=None, color='steelblue')
# כותרת ראשית
plt.title('Percentage of Churn by Internet Service Type')
# כותרת ציר Y
plt.ylabel('Churn Rate (%)')
# כותרת ציר X, הובפנו רווח הין הגרף לכותרת
plt.xlabel('Internet Service', labelpad=15)
#  הוספת האחוזים מעל כל עמודה
# לוקחים את הערך של כל עמודה, כופלים ב-100, ומוסיפים סימן של אחוז
labels = [f'{val*100:.1f}%' for val in ax.containers[0].datavalues]
ax.bar_label(ax.containers[0], labels=labels, padding=3)
# הוספת קווי רשת אופקיים
plt.grid(axis='y', linestyle='--', alpha=0.7)
# הצגת הגרף
plt.show()



