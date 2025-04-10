from datetime import datetime, timedelta

def random_date(start_year=1975, end_year=2000):
    start_date = datetime.strptime(f"{start_year}-01-01", "%Y-%m-%d")
    end_date = datetime.strptime(f"{end_year}-12-31", "%Y-%m-%d")
    random_days = 100
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

print(random_date())
