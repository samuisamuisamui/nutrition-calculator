from queries import get_nutrient_data
from queries_1 import get_branded_foods #get_foods_by_type
from models import FoodDatatype
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

if __name__ == "__main__":
    localDbName = "USDA-SQLite.sqlite"
    dbURL = f"sqlite:///{localDbName}"
    engine = create_engine(dbURL)

    Session = sessionmaker(bind=engine)
    session = Session()

    results = get_branded_foods(session, search_term="Honey")

    # results = get_nutrient_data()
    for row in results:
        print(f"{row.food_name} | {row.nutrient_name}: {row.amount}{row.unit_name}")
