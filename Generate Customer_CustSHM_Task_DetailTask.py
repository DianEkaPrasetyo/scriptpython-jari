import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import os
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

fake = Faker('id_ID')
geolocator = Nominatim(user_agent="jari-data-generator")

# Path setup
output_dir = "D:/JARI/JARI/Output"
os.makedirs(output_dir, exist_ok=True)
csv_output_dir = "D:/JARI/JARI/Output CSV"
os.makedirs(csv_output_dir, exist_ok=True)

today = datetime.today()
assign_date = today.strftime("%Y-%m-%d")
valid_date = (today + timedelta(days=7)).strftime("%Y-%m-%d")

# Load headers from uploaded files to match structure
template_dir = "D:/JARI/JARI/Template/"
customer_headers = pd.read_excel(template_dir + "Import_MasterCustomer.xlsx", nrows=0).columns.tolist()
shm_headers = pd.read_excel(template_dir + "Import_MasterCustomer_shm.xlsx", nrows=0).columns.tolist()
task_headers = pd.read_excel(template_dir + "Import_MasterTask.xlsx", nrows=0).columns.tolist()
detail_task_headers = pd.read_excel(template_dir + "Import_MasterTask_DetailTask.xlsx", nrows=0).columns.tolist()                                                                                                                                                                                                                                       

# Helper functions
def generate_phone():
    return f"62{random.randint(81200000000, 81999999999)}"

def generate_cabang(address):
    address_lower = address.lower()
    if "kalimalang" in address_lower:
        return "KLM"
    elif "kebayoran" in address_lower:
        return "KBY"
    elif "kaliurang" in address_lower:
        return "KLR"
    return random.choice(["KLM", "KBY", "KLR"])

def generate_gender():
    return random.choice(["Pria", "Wanita"])

def generate_marital_status():
    return random.choice(["Single", "Menikah"])

def generate_custtype():
    return random.choice(["Individu", "PT"])

def random_date(start_year=2005, end_year=2024):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    return (start + timedelta(days=random.randint(0, (end - start).days))).strftime('%Y-%m-%d')

def get_lat_lon(address):
    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            return str(location.latitude), str(location.longitude)
    except GeocoderTimedOut:
        time.sleep(1)
        return get_lat_lon(address)
    return "", ""

def generate_latitude_jakarta():
    return round(random.uniform(-6.4, -6.1), 6)

def generate_longitude_jakarta():
    return round(random.uniform(106.7, 107.0), 6)

# Generate base contract/customer data
customers = []
shms = []
tasks = []
detail_tasks = []

for i in range(200):
    accno = f"CTR{random.randint(100000000, 999999999)}"
    custno = f"ID{random.randint(1000000000, 9999999999)}"
    address = fake.address().replace("\n", " ").replace("\r", " ")
    cabang = generate_cabang(address)
    gender = generate_gender()
    marital = generate_marital_status()
    custtype = generate_custtype()
    birthdate = random_date(1975, 2000)
    due_date = random_date(2024, 2025)
    sertifikat_no = f"SRTF{100000 + i}"
    due_date_obj = datetime.strptime(random_date(2024, 2025), "%Y-%m-%d")
    dpd = (due_date_obj - today).days
    due_date = due_date_obj.strftime('%Y-%m-%d')   

    # Customer
    customer_row = {
        'accno': accno,
        'accountname': fake.name_male() if gender == "Pria" else fake.name_female(),
        'custno': custno,
        'custtype': custtype,
        'cabang': cabang,
        'zipcode': '',
        'gender': gender,
        'maritalstatus': marital,
        'birthdate': birthdate,
        'birthplace': fake.city(),
        'custaddress': address,
        'custemail': 'dian@jari.co.id',
        'custphoneno': generate_phone(),
        'mobileno': generate_phone(),
        'mobileno2': generate_phone(),
        'negativestatus': random.choice(['Ya', 'Tidak']),
        'negativedesc': '' if random.random() > 0.2 else fake.sentence(),
        'relativename': fake.name(),
        'relativetype': random.choice(['Kakak', 'Adik', 'Orangtua', 'Saudara']),
        'relativeaddress': fake.address().replace("\n", " ").replace("\r", " "),
        'relativephone': generate_phone(),
        'spousename': fake.name(),
        'spousebirthdate': random_date(1970, 2000),
        'spousebirthplace': fake.city(),
        'spouseaddress': fake.address().replace("\n", " ").replace("\r", " "),
        'spousemobileno': generate_phone(),
        'spouseoffice': fake.company(),
        'spouseofficephone': generate_phone(),
        'spousejobname': fake.job(),
        'companyname': fake.company(),
        'companybusiness': fake.bs(),
        'companyaddress': fake.address().replace("\n", " ").replace("\r", " "),
        'companyphone': generate_phone(),
        'companyfax': generate_phone(),
        'jobname': fake.job(),
        'latitude': round(random.uniform(-6.4, -6.1), 6),
        'longitude': round(random.uniform(106.7, 107.0), 6)
    }
    customers.append(customer_row)

    # SHM
    shm_row = {
        "accno": accno,
        "lokasiagunan" : fake.city(),
        "jenisagunan" : random.choice(['Gedung Kantor', 'Ruko', 'Rumah']),
        "luastanah": random.randint(300, 500),
        "luasbangunan": random.randint(50, 300),
        "jeniskepimilikan" : 'Pribadi',
        "nosertifikat": accno,
        "alamatlokasiagunan": address,
        "nilaipasar": random.randint(100000000,9000000000),
        "nilaihakanggunan": random.randint(100000000,9000000000),
        
    }
    shms.append(shm_row)

    # Task
    task_row = {
         "taskcode": accno,
        "collectorcode" : 'dian',
        "accno": accno,
        "tasktype" : 'COLL',
        "assigndate": assign_date,
        "validdate": valid_date,
        "validuntil": valid_date,  # Tambahan
        "installment" : random.randint(100000000,9000000000),
        "collectfee" : '0',
        "tenor" :  random.randint(12,400),
        "ospokok" :  random.randint(100000000,9000000000),  # Ganti dari Ospokok → ospokok
    }
    tasks.append(task_row)

    # Detail Task
    detail_task_row = {
        "taskcode": accno,
        "assigndate": assign_date,
        "duedate": due_date,
        "period": random.randint(1, 400),
        "dpd": dpd,
        "angstung": random.randint(100000000,800000000),
        "denda": random.randint(100000000,800000000),
    }
    detail_tasks.append(detail_task_row)

# Convert to DataFrames and reorder columns to match templates
df_customer = pd.DataFrame(customers)[customer_headers]
df_shm = pd.DataFrame(shms)[shm_headers]
df_task = pd.DataFrame(tasks)[task_headers]
df_detail_task = pd.DataFrame(detail_tasks)[detail_task_headers]
def clean_text(text):
    return str(text).replace("\n", " ").replace("\r", " ")

# Save to Excel
df_customer.to_excel(f"{output_dir}/Import_Customer.xlsx", index=False)
df_shm.to_excel(f"{output_dir}/Import_Customer_SHM.xlsx", index=False)
df_task.to_excel(f"{output_dir}/Import_Task.xlsx", index=False)
df_detail_task.to_excel(f"{output_dir}/Import_Detail_Task.xlsx", index=False)

# Save to Csv
df_customer.to_csv(f"{csv_output_dir}/Import_Customer.csv", index=False, sep=';', header=False)
df_shm.to_csv(f"{csv_output_dir}/Import_Customer_SHM.csv", index=False, sep=';', header=False)
df_task.to_csv(f"{csv_output_dir}/Import_Task.csv", index=False, sep=';', header=False)
df_detail_task.to_csv(f"{csv_output_dir}/Import_Detail_Task.csv", index=False, sep=';', header=False)

template_path = "D:/JARI/JARI/Output/Import_Customer.xlsx"  # sesuaikan dengan file output yang kamu simpan

if not os.path.exists(template_path):
    raise FileNotFoundError(f"File tidak ditemukan: {template_path}")
customer_headers = pd.read_excel(template_path, nrows=0).columns.tolist()

print(set(shm_headers) - set(shms[0].keys()))  # untuk lihat kolom yang hilang
print(set(shms[0].keys()) - set(shm_headers))  # untuk lihat kolom yang kelebihan
"Data berhasil dibuat dan disimpan."

