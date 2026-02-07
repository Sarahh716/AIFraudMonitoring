import pandas as pd
import random

try:
    from geopy.distance import geodesic
except ImportError:
    geodesic = None

# Internal Coordinates Database
LOC_COORDS = {
    "London": (51.5074, -0.1278), "New York": (40.7128, -74.0060),
    "Dubai": (25.2048, 55.2708), "Tokyo": (35.6762, 139.6503),
    "Singapore": (1.3521, 103.8198), "Sydney": (-33.8688, 151.2093)
}

def process_upload(uploaded_file):
    """Processes XLSX files for transaction data."""
    if not uploaded_file.name.lower().endswith(('.xlsx', '.xls')):
        return None
    
    try:
        df = pd.read_excel(uploaded_file)
        # Standardize Columns
        df.columns = [c.strip().capitalize() for c in df.columns]
        if 'Merchant' not in df.columns: df['Merchant'] = "Unknown"
        if 'Location' not in df.columns: df['Location'] = "Unknown"
        if 'Amount' not in df.columns: df['Amount'] = 0.0
        return df
    except Exception:
        return None

def apply_ai_scoring(df, flagged_merchants, office_loc, km_threshold):
    if df is None: return None
    
    office_pt = LOC_COORDS.get(office_loc, (51.5, -0.1))

    def calc_geo_risk(loc):
        if km_threshold == 0 or geodesic is None or loc == "Unknown": return 10
        target_pt = LOC_COORDS.get(loc, (random.uniform(-90,90), random.uniform(-180,180)))
        dist = geodesic(office_pt, target_pt).km
        return 95 if dist > km_threshold else 15

    df['Merchant_Risk'] = df['Merchant'].apply(lambda m: 95 if m in flagged_merchants else 10)
    df['Geo_Risk'] = df['Location'].apply(calc_geo_risk)
    df['Velocity_Risk'] = [random.randint(5, 95) for _ in range(len(df))]
    
    df['Risk_Score'] = ((df['Merchant_Risk'] + df['Geo_Risk'] + df['Velocity_Risk']) / 3).round(1)
    df['Flagged'] = df['Risk_Score'].apply(
        lambda x: "🚨 CRITICAL" if x > 75 else ("⚠️ WARNING" if x > 45 else "✅ CLEAN")
    )
    if 'Transaction_id' not in df.columns:
        df['Transaction_id'] = [f"TXN-{random.randint(1000, 9999)}" for _ in range(len(df))]
    return df

def analyze_single_json(json_data, flagged_merchants, office_loc, km_threshold):
    df_single = pd.DataFrame([json_data])
    processed = apply_ai_scoring(df_single, flagged_merchants, office_loc, km_threshold)
    return processed.iloc[0].to_dict()