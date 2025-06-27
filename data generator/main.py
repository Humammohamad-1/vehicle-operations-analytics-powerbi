import pandas as pd
import numpy as np
import random
from faker import Faker
import os

# Setup
fake = Faker('nl_BE')  # Belgian locale
np.random.seed(42)
random.seed(42)

# Constants
NUM_VEHICLES = 200
NUM_SUPPLIERS = 20
NUM_SERVICE_VISITS = 1000

# Vehicle brand-model pairs
brands_models = [
    ("Toyota", "Corolla"), ("Toyota", "Yaris"), ("Toyota", "C-HR"),
    ("Ford", "Focus"), ("Ford", "Fiesta"), ("Ford", "Kuga"),
    ("Renault", "Clio"), ("Renault", "Captur"), ("Renault", "Megane"),
    ("BMW", "320i"), ("BMW", "X1"), ("BMW", "i3"),
    ("Peugeot", "208"), ("Peugeot", "3008"), ("Peugeot", "508"),
    ("Volkswagen", "Golf"), ("Volkswagen", "Passat"), ("Volkswagen", "Tiguan"),
    ("Hyundai", "Ioniq"), ("Hyundai", "Tucson"),
    ("Tesla", "Model 3"), ("Tesla", "Model Y")
]

fuel_types = ["Petrol", "Diesel", "Electric", "Hybrid"]

# Generate dim_vehicle
vehicle_records = []
for i in range(1, NUM_VEHICLES + 1):
    brand, model = random.choice(brands_models)
    fuel_type = random.choice(fuel_types)
    reg_date = fake.date_between(start_date="-5y", end_date="today")
    vehicle_records.append([i, brand, model, fuel_type, reg_date])

dim_vehicle = pd.DataFrame(vehicle_records, columns=[
    "vehicle_id", "brand", "model", "fuel_type", "registration_date"
])

# Generate dim_supplier with Belgian addresses
dim_supplier = pd.DataFrame({
    "supplier_id": range(1, NUM_SUPPLIERS + 1),
    "name": [fake.company() for _ in range(NUM_SUPPLIERS)],
    "region": [fake.city() for _ in range(NUM_SUPPLIERS)],
    "address": [fake.address().replace("\n", ", ") for _ in range(NUM_SUPPLIERS)],
    "rating": [random.randint(1, 5) for _ in range(NUM_SUPPLIERS)]
})

# Generate dim_service_type
service_categories = [("SMR", "Service, Maintenance, and Repairs"), ("Tyres", "Tire replacement or rotation")]
dim_service_type = pd.DataFrame({
    "service_type_id": [1, 2],
    "category": [cat[0] for cat in service_categories],
    "description": [cat[1] for cat in service_categories]
})

# Map category to ID
service_category_map = {"SMR": 1, "Tyres": 2}

# Generate fact_service_visits
fact_service_visits = []
for i in range(1, NUM_SERVICE_VISITS + 1):
    vehicle_id = random.randint(1, NUM_VEHICLES)
    supplier_id = random.randint(1, NUM_SUPPLIERS)
    category = random.choice(["SMR", "Tyres"])
    service_type_id = service_category_map[category]
    service_date = fake.date_between(start_date="-2y", end_date="today")
    labor_cost = round(random.uniform(50, 500), 2)
    parts_cost = round(random.uniform(20, 1000), 2)
    total_cost = round(labor_cost + parts_cost, 2)
    SLA_met = random.choices(["Yes", "No"], weights=[0.8, 0.2])[0]
    duration_days = random.randint(1, 10)

    fact_service_visits.append([
        i, vehicle_id, supplier_id, service_type_id, service_date,
        labor_cost, parts_cost, total_cost, SLA_met, duration_days
    ])

fact_service_visits = pd.DataFrame(fact_service_visits, columns=[
    "visit_id", "vehicle_id", "supplier_id", "service_type_id", "service_date",
    "labor_cost", "parts_cost", "total_cost", "SLA_met", "duration_days"
])

# ✅ Save to your PC
output_dir = r"C:\Users\Humam\Documents\VehicleOpsData"
os.makedirs(output_dir, exist_ok=True)

dim_vehicle.to_csv(os.path.join(output_dir, "dim_vehicle.csv"), index=False)
dim_supplier.to_csv(os.path.join(output_dir, "dim_supplier.csv"), index=False)
dim_service_type.to_csv(os.path.join(output_dir, "dim_service_type.csv"), index=False)
fact_service_visits.to_csv(os.path.join(output_dir, "fact_service_visits.csv"), index=False)

print(f"All files saved to: {output_dir}")
