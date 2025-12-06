import hashlib

import pandas as pd
from db_connect import get_engine

engine = get_engine()

df = pd.read_csv("data/raw/freight_data.csv")
df_route = df[["origin_city", "destination_city", "distance_km"]]
df_route = df_route.rename(
    columns={
        "origin_city": "Origin",
        "destination_city": "Destination",
        "distance_km": "DistanceKM",
    }
)
df_route = df_route.drop_duplicates()

df_vehicle = df[["vehicle_plate", "vehicle_type", "vehicle_capacity"]]
df_vehicle = df_vehicle.rename(
    columns={
        "vehicle_plate": "PlateNumber",
        "vehicle_type": "VehicleType",
        "vehicle_capacity": "Capacity",
    }
)
df_vehicle = df_vehicle.drop_duplicates()
df_vehicle["PlateNumber"] = df_vehicle["PlateNumber"].apply(
    lambda x: hashlib.sha256(x.encode()).hexdigest()
)

date_range = pd.date_range(start="2025-01-01", end="2025-12-31", freq="D")
df_date = pd.DataFrame(
    {
        "RecordDate": date_range,
        "Month": date_range.month,
        "Year": date_range.year,
    }
)
df_date["IsHarvestSeason"] = df_date["Month"].isin([3, 4, 5]).astype(int)

with engine.connect() as conn:
    df_db_route = pd.read_sql(
        "SELECT Origin, Destination, DistanceKM FROM Dim_Route", conn
    )
    df_db_vehicle = pd.read_sql("SELECT PlateNumber FROM Dim_Vehicle", conn)
    df_db_date = pd.read_sql("SELECT RecordDate FROM Dim_Date", conn)
df_db_date["RecordDate"] = pd.to_datetime(df_db_date["RecordDate"]).dt.normalize()

qtd_rotas = len(df_db_route)
qtd_veiculos = len(df_db_vehicle)
qtd_datas = len(df_db_date)

df_route_delta = df_route.merge(
    df_db_route,
    on=["Origin", "Destination", "DistanceKM"],
    how="left",
    indicator=True,
)
df_route_delta = df_route_delta[df_route_delta["_merge"] == "left_only"].drop(
    columns=["_merge"]
)

df_vehicle_delta = df_vehicle.merge(
    df_db_vehicle,
    on="PlateNumber",
    how="left",
    indicator=True,
)
df_vehicle_delta = df_vehicle_delta[df_vehicle_delta["_merge"] == "left_only"].drop(
    columns=["_merge"]
)

df_date_delta = df_date.merge(
    df_db_date,
    on="RecordDate",
    how="left",
    indicator=True,
)
df_date_delta = df_date_delta[df_date_delta["_merge"] == "left_only"].drop(
    columns=["_merge"]
)

with engine.begin() as conn:
    df_vehicle_delta.to_sql("Dim_Vehicle", conn, if_exists="append", index=False)
    df_route_delta.to_sql("Dim_Route", conn, if_exists="append", index=False)
    df_date_delta.to_sql("Dim_Date", conn, if_exists="append", index=False)

print("--- Relatório de Carga ---")
print(f"Total de rotas no banco: {qtd_rotas}")
print(f"Total de veículos no banco: {qtd_veiculos}")
print(f"Total de datas no banco: {qtd_datas}")
print(f"Rotas carregadas: {len(df_route_delta)}")
print(f"Veículos carregados: {len(df_vehicle_delta)}")
print(f"Datas carregados: {len(df_date_delta)}")
