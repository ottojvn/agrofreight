import hashlib

import pandas as pd
from db_connect import get_engine

engine = get_engine()

df = pd.read_csv("data/raw/freight_data.csv")
df = df.drop(columns=["vehicle_type", "vehicle_capacity"])
df = df.drop_duplicates()
df["vehicle_plate"] = df["vehicle_plate"].apply(
    lambda x: hashlib.sha256(x.encode()).hexdigest()
)
df["arrival_date"] = pd.to_datetime(df["arrival_date"])
df["departure_date"] = pd.to_datetime(df["departure_date"])
df = df.rename(
    columns={
        "origin_city": "Origin",
        "destination_city": "Destination",
        "distance_km": "DistanceKM",
        "vehicle_plate": "PlateNumber",
        "freight_value": "FreightValue",
        "diesel_price": "DieselPrice",
        "weight_ton": "WeightTon",
    }
)


with engine.connect() as conn:
    df_db_route = pd.read_sql(
        "SELECT RouteID, Origin, Destination, DistanceKM FROM Dim_Route", conn
    )
    df_db_vehicle = pd.read_sql("SELECT VehicleID, PlateNumber FROM Dim_Vehicle", conn)
    df_db_date = pd.read_sql("SELECT DateID, RecordDate FROM Dim_Date", conn)
    df_db_facts = pd.read_sql(
        "SELECT \
    DepartureDateID, \
    ArrivalDateID, \
    RouteID, \
    VehicleID, \
    FreightValue, \
    DieselPrice, \
    WeightTon \
    FROM Fact_Freight",
        conn,
    )
df_db_date["RecordDate"] = pd.to_datetime(df_db_date["RecordDate"])
df_db_facts = df_db_facts.astype(
    {
        "DepartureDateID": int,
        "ArrivalDateID": int,
        "RouteID": int,
        "VehicleID": int,
        "FreightValue": float,
        "DieselPrice": float,
        "WeightTon": float,
    }
)

df = df.merge(df_db_route, on=["Origin", "Destination", "DistanceKM"], how="inner")
df = df.drop(columns=["Origin", "Destination"])

df = df.merge(df_db_vehicle, on=["PlateNumber"], how="inner")
df = df.drop(columns=["PlateNumber"])

df["normalized_departure_date"] = df["departure_date"].dt.normalize()
df = df.merge(
    df_db_date, left_on="normalized_departure_date", right_on="RecordDate", how="inner"
)
df = df.drop(columns=["RecordDate", "normalized_departure_date"])
df = df.rename(columns={"DateID": "DepartureDateID"})

df["normalized_arrival_date"] = df["arrival_date"].dt.normalize()
df = df.merge(
    df_db_date, left_on="normalized_arrival_date", right_on="RecordDate", how="inner"
)
df = df.drop(columns=["RecordDate", "normalized_arrival_date"])
df = df.rename(columns={"DateID": "ArrivalDateID"})

df = df[
    df["RouteID"].notnull()
    & df["VehicleID"].notnull()
    & df["DepartureDateID"].notnull()
    & df["ArrivalDateID"].notnull()
]

df = df.merge(df_db_facts, on=df_db_facts.columns.tolist(), how="left", indicator=True)
df = df[df["_merge"] == "left_only"]
df = df.drop(columns=["_merge"])

df["time_delta"] = df["arrival_date"] - df["departure_date"]
df["time_delta"] = df["time_delta"] / pd.Timedelta(hours=1)
df = df.drop(columns=["departure_date", "arrival_date"])

mask_speed = (df["DistanceKM"] / df["time_delta"]) >= 100
df = df.drop(columns=["DistanceKM"])
mask_speed = mask_speed.drop(columns=["DistanceKM"])

mask_time = df["time_delta"] <= 0
df = df.drop(columns=["time_delta"])
mask_time = mask_time.drop(columns=["time_delta"])
mask_speed = mask_speed.drop(columns=["time_delta"])

mask_freight_value = df["FreightValue"] <= 0
mask_diesel_price = df["DieselPrice"] <= 0

df["ErrorMessage"] = None
df.loc[mask_speed, "ErrorMessage"] = "Violação Física: Velocidade >= 100km/h"
df.loc[mask_time, "ErrorMessage"] = (
    "Violação Temporal: Data de Chegada <= Data de Saída"
)
df.loc[mask_freight_value, "ErrorMessage"] = "Violação Financeira: Preço do Frete <= 0"
df.loc[mask_diesel_price, "ErrorMessage"] = "Violação Financeira: Preço do Diesel <= 0"

df_errors = pd.DataFrame(columns=["RawData", "ErrorMessage"])
df_errors["ErrorMessage"] = df["ErrorMessage"][df["ErrorMessage"].notna()].copy()
df_errors["RawData"] = (
    df[df["ErrorMessage"].notna()]
    .drop(columns="ErrorMessage")
    .apply(func=lambda row: row.to_json(), axis=1)
)

df = df[df["ErrorMessage"].isna()]
df = df.drop(columns=["ErrorMessage"])

with engine.begin() as conn:
    df.to_sql("Fact_Freight", conn, if_exists="append", index=False)
    df_errors.to_sql("Log_Errors", conn, if_exists="append", index=False)

print("--- Relatório de Carga ---")
print(f"Total de fatos no banco: {len(df_db_facts)}")
print(f"Fatos carregadas: {len(df)}")
print(f"Errors carregadas: {len(df_errors)}")
