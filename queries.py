from sqlalchemy import case
from sqlalchemy.orm import Session
from models import Food, Nutrient, FoodNutrient, FoodCategory

class NutritionRepository:
    def __init__(self, session: Session):
        self.session = session

        self.COMMON_NUTRIENT_IDS = [1008, 1003, 1004, 1005]
        self.NUTRIENT_ORDER = case(
            (Nutrient.id == 1008, 1),  # Energia
            (Nutrient.id == 1005, 2),  # Węglowodany
            (Nutrient.id == 1003, 3),  # Białko
            (Nutrient.id == 1004, 4),  # Tłuszcz
            else_=None
        )

    def _base_query(self):
        """Wewnętrzna metoda do budowania bazowego zapytania"""
        return self.session.query(
            Food.description.label("food_name"),
            Nutrient.name.label("nutrient_name"),
            FoodNutrient.amount,
            Nutrient.unit_name
        ).join(FoodNutrient, Food.fdc_id == FoodNutrient.fdc_id
        ).join(Nutrient, FoodNutrient.nutrient_id == Nutrient.id)
    
    def get_available_categories(self):
        """Pobiera dostępne kategorie żywności"""
        return self.session.query(
            FoodCategory.id,
            FoodCategory.description
        ).order_by(FoodCategory.id).all()
    
    def get_available_food_types(self):
        """Zwraca dostępne typy żywności"""
        return [
            ('branded_food', 'Branded Food (Produkty Markowe)'),
            ('sr_legacy_food', 'Legacy Food (Podstawowe produkty)')
        ]
    
    def get_whole_database(self, search_term: str):
        """Przeszukuje całą bazę danych"""
        return (self._base_query()
            .filter(
                Food.description.ilike(f"%{search_term}%"),
                Nutrient.id.in_(self.COMMON_NUTRIENT_IDS)
            )
            .order_by(Food.description, self.NUTRIENT_ORDER)
            .all()
        )
    
    def get_by_food_category(self, category_id: int, search_term: str):
        """Wyszukiwanie w określonej kategorii"""
        return (self._base_query()
            .join(Food.category)
            .filter(
                Food.food_category_id == category_id,
                Food.description.ilike(f"%{search_term}%"),
                Nutrient.id.in_(self.COMMON_NUTRIENT_IDS))
            .order_by(Food.description, self.NUTRIENT_ORDER)
            .all()
        )
    
    def get_branded_foods(self, search_term: str):
        """Wyszukiwanie produktów markowych"""
        search_any = f"%{search_term}%"
        return (self._base_query()
            .join(Food.branded_food)
            .filter(
                Food.data_type == 'branded_food',
                Food.description.ilike(search_any), 
                Nutrient.id.in_(self.COMMON_NUTRIENT_IDS)
            )
            .order_by(Food.description, self.NUTRIENT_ORDER)
            .all()
        )
    
    def get_legacy_foods(self, search_term: str):
        """Wyszukaj podstawowe produkty (legacy)"""
        return (self._base_query()
            .join(Food.sr_legacy_foods)  
            .filter(
                Food.data_type == 'sr_legacy_food',
                Food.description.ilike(f"%{search_term}%"),
                Nutrient.id.in_(self.COMMON_NUTRIENT_IDS)
            )
            .order_by(Food.description, self.NUTRIENT_ORDER)
            .all()
        )
