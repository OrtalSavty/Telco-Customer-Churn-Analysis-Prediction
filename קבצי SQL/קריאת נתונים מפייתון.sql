/* הסבר כללי: 
בגלל שבפייתון חלק מהשדות (כמו Total_Charges) נקלטו כטקסט ולא כמספרים, 
אנחנו יוצרים View כדי לסדר את הנתונים, להמיר אותם לפורמט מספרי 
ולהפוך ערכים טקסטואליים (Yes/No) למספרים (1/0) לצורך חישובים עתידיים.
*/

-- בדיקה אם ה-View כבר קיים, אם כן - נמחוק אותו כדי ליצור מחדש
IF OBJECT_ID('v_clean_data', 'V') IS NOT NULL
    DROP VIEW v_clean_data;
GO

CREATE VIEW v_clean_data AS
-- שליפת העמודות הרלוונטיות מהטבלה הגולמית
SELECT 
    customerID, 
    MonthlyCharges, 
    tenure, 
    Contract, 
    InternetService, 

    -- המרת עמודת Churn מערך טקסטואלי לערך מספרי (1 ל-Yes, 0 אחרת)
    CASE 
        WHEN Churn = 'Yes' THEN 1
        ELSE 0
    END AS churn_label,

    -- המרת עמודת TotalCharges מפורמט טקסט לפורמט מספרי (Float)
    -- השימוש ב-TRY_CAST מונע שגיאות אם יש ערכים שלא ניתנים להמרה
    TRY_CAST(TotalCharges AS FLOAT) AS total_charges_clean 

FROM dbo.raw_data_staging;
GO