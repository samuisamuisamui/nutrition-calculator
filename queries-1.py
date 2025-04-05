from sqlalchemy import case, literal_column
from sqlalchemy.orm import session
from models import Food, Nutrient, FoodNutrient, FoodCategory, BrandedFood, Sr_legacy_food

# Wspólne parametry
COMMON_NUTRIENT_IDS = [1008, 1003, 1004, 1005, 1051, 1162]
NUTRIENT_ORDER = case(
    [
        (Nutrient.id == 1008, 1),  # Energia
        (Nutrient.id == 1005, 2),  # Węglowodany
        (Nutrient.id == 1003, 3),  # Białko
        (Nutrient.id == 1004, 4),  # Tłuszcz
        (Nutrient.id == 1051, 5),  # Wapń
        (Nutrient.id == 1162, 6),  # Sód
    ],
    else_=None
)

def base_query():
    return session.query(
        Food.description.label("food_name"),
        Nutrient.name.label("nutrient_name"),
        FoodNutrient.amount,
        Nutrient.unit_name,
        literal_column("'per 100g'").label("portion_size")
    ).join(FoodNutrient, Food.fdc_id == FoodNutrient.fdc_id
    ).join(Nutrient, FoodNutrient.nutrient_id == Nutrient.id)

# Wyświetlenie dostępnych kategorii + id

# Przeszukanie całej bazy:

def get_all(search_term: str):
    return (base_query()
            .join(Food)
            .filter(Food.description.ilike(f"%{search_term}%"),
                    Nutrient.id.in_(COMMON_NUTRIENT_IDS))
            .order_by(Food.description, NUTRIENT_ORDER)
            .all()
    )
# Przeszukanie wybranej kategorii jedzenia 

def get_food_category(category_id: int):
    return (base_query()
        .join(Food.category)
        .filter(Food.food_category_id == category_id,
                Nutrient.id.in_(COMMON_NUTRIENT_IDS))
        .order_by(Food.description, NUTRIENT_ORDER)
        .all()
    )

# Wyszukiwanie na podstawie wybranej kategorii jedzenia:

def get_by_food_category(category_id: int, search_term: str):
    return (base_query()
        .join(Food.category)
        .filter(
            Food.food_category_id == category_id,
            Food.description.ilike(f"%{search_term}%"),
            Nutrient.id.in_(COMMON_NUTRIENT_IDS))
        .order_by(Food.description, NUTRIENT_ORDER)
        .all()
    )

# Wyszukiwania na podstawie typów żywności (branded, legacy..):

def get_branded_foods(search_term: str):
    return (base_query()
        .join(Food.branded_food)
        .filter(
            Food.data_type == 'branded_food',
            Food.description.ilike(f"%{search_term}%",
            Nutrient.id.in_(COMMON_NUTRIENT_IDS))
        )
        .order_by(Food.description, NUTRIENT_ORDER)
        .all()
    )

def get_legacy_foods(search_term: str):
    return (base_query()
        .join(Food.sr_legacy_foods)
        .filter(
            Food.data_type == 'sr_legacy_food',
            Food.description.ilike(f"%{search_term}%",
            Nutrient.id.in_(COMMON_NUTRIENT_IDS))
        )
        .order_by(Food.description, NUTRIENT_ORDER)
        .all()
    )

# Wyszukiwania na podstawie kategorii i typów żywności: