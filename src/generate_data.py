import datetime
import random

import pandas as pd


def random_date(start, end):
    """
    Returns a random date between two datetime objects

    :param start: start datetime
    :param end: end datetime
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)


routes = [
    ("Sorriso", "Santos", 2150),
    ("Sinop", "Miritituba", 1050),
    ("Rondonópolis", "Paranaguá", 1600),
    ("Rio Verde", "Santos", 1200),
    ("Barreiras", "Salvador", 850),
    ("Primavera do Leste", "Santos", 1900),
    ("Lucas do Rio Verde", "Miritituba", 1100),
    ("Cascavel", "Paranaguá", 580),
]

vehicles = {
    "Rodotrem": {"capacity": 74},
    "Bitrem": {"capacity": 57},
    "Carreta LS": {"capacity": 32},
    "Vanderleia": {"capacity": 35},
    "Truck": {"capacity": 23},
}

price_per_km = 5.00
safra_begin = datetime.datetime(2025, 3, 1)
safra_end = datetime.datetime(2025, 5, 31)
negative_arrival = 0
negative_freight = 0
impossible_speed = 0
max_records = 5000

records = []
for i in range(max_records):
    route = random.choice(routes)
    vehicle_type = random.choice(list(vehicles.keys()))
    departure_date = random_date(safra_begin, safra_end)
    record = {
        "origin_city": route[0],
        "destination_city": route[1],
        "distance_km": route[2],
        "vehicle_plate": f"{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))}{random.randint(0, 9)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(0, 9)}{random.randint(0, 9)}",
        "vehicle_type": vehicle_type,
        "vehicle_capacity": vehicles[vehicle_type]["capacity"],
        "departure_date": departure_date,
        "arrival_date": departure_date
        + datetime.timedelta(hours=(route[2] / random.uniform(60, 80))),
        "freight_value": route[2] * price_per_km,
        "diesel_price": random.uniform(5.50, 6.90),
    }

    if random.random() < 0.05:
        event = random.randrange(0, 3)
        if event == 0:
            record["arrival_date"] = record[
                "departure_date"
            ] - datetime.timedelta(
                hours=(record["distance_km"] / random.uniform(60, 80))
            )
            negative_arrival = 1
        elif event == 1:
            record["freight_value"] *= -1
            negative_freight = 1
        else:
            record["arrival_date"] = record[
                "departure_date"
            ] + datetime.timedelta(hours=1)
            impossible_speed = 1

    records.append(record)

records[0]["arrival_date"] = records[0]["departure_date"] - datetime.timedelta(
    hours=5
)
records[1]["freight_value"] *= -1
records[2]["arrival_date"] = records[2]["departure_date"] + datetime.timedelta(
    hours=1
)

df = pd.DataFrame(records)
df.to_csv("data/raw/freight_data.csv", index=False)
