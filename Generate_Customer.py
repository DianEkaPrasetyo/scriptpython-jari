import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta  # ✅ ini saja, jangan pakai "import datetime"

fake = Faker('id_ID')  # Locale Indonesia

# Helper functions
def generate_phone():
    return f"62{random.randint(81200000000, 81999999999)}"

def generate_cabang(address):
    if "kalimalang" in address.lower():
        return "KLM"
    elif "kebayoran" in address.lower():
        return "KBY"
    elif "kaliurang" in address.lower():
        return "KLR"
    return random.choice(["KLM", "KBY", "KLR"])

def generate_gender():
    return random.choice(["Pria", "Wanita"])

def generate_marital_status():
    return random.choice(["Single", "Menikah"])

def generate_custtype():
    return random.choice(["Individu", "PT"])

def random_date(start_year=1970, end_year=2000):
    start_date = datetime.strptime(f"{start_year}-01-01", "%Y-%m-%d")
    end_date = datetime.strptime(f"{end_year}-12-31", "%Y-%m-%d")
    random_days = random.randint(0, (end_date - start_date).days)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

# Generate 200 rows of data
data = []
for i in range(200):
    address = fake.address()
    cabang = generate_cabang(address)
    gender = generate_gender()
    marital = generate_marital_status()
    custtype = generate_custtype()
    accno = f"CTR{random.randint(100000000, 999999999)}"
    custno = f"ID{random.randint(1000000000, 9999999999)}"
    birthdate = random_date(1975, 2000)
    spouse_birthdate = random_date(1970, 1995)

    row = {
        'accno': accno,
        'accountname': fake.name_male() if gender == "Pria" else fake.name_female(),
        'custno': custno,
        'custtype': custtype,
        'cabang': cabang,
        'zipcode': fake.postcode(),
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
        'relativeaddress': fake.address(),
        'relativephone': generate_phone(),
        'spousename': fake.name(),
        'spousebirthdate': spouse_birthdate,
        'spousebirthplace': fake.city(),
        'spouseaddress': fake.address(),
        'spousemobileno': generate_phone(),
        'spouseoffice': fake.company(),
        'spouseofficephone': generate_phone(),
        'spousejobname': fake.job(),
        'companyname': fake.company(),
        'companybusiness': fake.bs(),
        'companyaddress': fake.address(),
        'companyphone': generate_phone(),
        'companyfax': generate_phone(),
        'jobname': fake.job(),
        'latitude': str(fake.latitude()),
        'longitude': str(fake.longitude())
    }

    data.append(row)

# Save to Excel
df = pd.DataFrame(data)
df.to_excel("sample_customer_200.xlsx", index=False)
print("✅ Data berhasil dibuat: sample_customer_200.xlsx")
