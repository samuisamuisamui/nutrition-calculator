from sqlalchemy import create_engine, literal_column, case
from sqlalchemy.orm import sessionmaker
from models import Food, Nutrient, FoodNutrient, FoodCategory

localDbName = "USDA-SQLite.sqlite"
dbURL = f"sqlite:///{localDbName}"
engine = create_engine(dbURL)

Session = sessionmaker(bind=engine)
session = Session()

def get_nutrient_data():
    query = (
        session.query(
            Food.description.label("food_name"),
            Nutrient.name.label("nutrient_name"),
            FoodNutrient.amount,
            Nutrient.unit_name,
            literal_column("'per 100g'").label("portion_size")
        )
        .join(FoodNutrient, Food.fdc_id == FoodNutrient.fdc_id)
        .join(Nutrient, FoodNutrient.nutrient_id == Nutrient.id)
        .join(FoodCategory, Food.food_category_id == FoodCategory.id)
        .filter(
            Food.data_type == 'sr_legacy_food',
            Food.description.ilike('%Apple%'),
            Nutrient.id.in_([1008, 1003, 1004, 1005, 1051, 1162])
        )
        .order_by(
            Food.description,
            case(
                
                    (Nutrient.id == 1008, 1),
                    (Nutrient.id == 1005, 2),
                    (Nutrient.id == 1003, 3),
                    (Nutrient.id == 1004, 4),
                    (Nutrient.id == 1051, 5),
                    (Nutrient.id == 1162, 6),
                    else_=None
                )
        )
    )
    
    return query.all()

if __name__ == "__main__":
    results = get_nutrient_data()
    for row in results:
        print(f"{row.food_name} | {row.nutrient_name}: {row.amount}{row.unit_name}")