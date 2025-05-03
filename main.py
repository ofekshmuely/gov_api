

from fastapi import FastAPI
import pandas as pd

app = FastAPI()

# טוען את הדאטה
df = pd.read_csv('https://drive.google.com/uc?export=download&id=1WvpiI7gvQmV7F3JxEhWD2YtXEFMPrOFP')
df.columns = df.columns.str.strip()  # מנקה רווחים בעמודות

@app.get("/")
def get_all_data(limit: int = 200):
    if limit > len(df):
        limit = len(df)
    return df.head(limit).to_dict(orient='records')


@app.get("/sum-vat")
def sum_vat():
    total_vat = df['VAT'].sum()
    return {"sum_VAT": total_vat}

@app.get("/filter-country")
def filter_country(country: str):
    filtered = df[df['Origin_Country_IL'].str.strip() == country.strip()]
    return filtered.to_dict(orient='records')

@app.get("/filter-customshouse")
def filter_customshouse(customs_house: str):
    filtered = df[df['CustomsHouse'].str.strip() == customs_house.strip()]
    return filtered.to_dict(orient='records')

@app.get("/summary-by-customshouse")
def summary_by_customshouse():
    summary = df.groupby('CustomsHouse')['Quantity'].sum().to_dict()
    return summary

@app.get("/summary-by-country")
def summary_by_country():
    summary = df.groupby('Origin_Country_IL')['Quantity'].sum().to_dict()
    return summary

@app.get("/total-taxes")
def total_taxes():
    total_general_tax = df['GeneralCustomsTax'].sum()
    total_purchase_tax = df['PurchaseTax'].sum()
    total_vat = df['VAT'].sum()
    return {
        "total_GeneralCustomsTax": total_general_tax,
        "total_PurchaseTax": total_purchase_tax,
        "total_VAT": total_vat
    }


# מספר רשומו של מדינה -> http://127.0.0.1:8000/count-country?country=סין
@app.get("/count-country")
def count_country(country: str):
    filtered = df[df['Origin_Country_IL'].str.strip() == country.strip()]
    count = len(filtered)
    return {"country": country, "count": count}



@app.get("/sum-ton")
def sum_ton():
    filtered = df[df['Quantity_MeasurementUnitName'].str.strip().str.lower() == 'kilogram'].copy()
    filtered['Quantity'] = pd.to_numeric(filtered['Quantity'], errors='coerce')
    total_kg = filtered['Quantity'].sum()
    total_ton = total_kg / 1000
    rounded_ton = round(total_ton, 0)  
    return rounded_ton


#סכום כללי של  המע"מ
@app.get("/sum-vat")
def sum_vat():
    df['VAT'] = pd.to_numeric(df['VAT'], errors='coerce')  # ממיר למספרים בבטחה
    total_vat = df['VAT'].sum()
    total_vat = round(total_vat, 2)  # עיגול לשתי ספרות אחרי הנקודה
    return total_vat


# ערך הסחורות בעסקה - NISCurrencyAmount
@app.get("/sum-nis")
def sum_nis():
    total_nis = df['NISCurrencyAmount'].sum()
    return {"NISCurrencyAmount": total_nis}

