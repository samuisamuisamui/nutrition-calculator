from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

base = declarative_base()

class Food(base):
    __tablename__ = 'food'
    fdc_id = Column(Integer, primary_key=True)
    data_type = Column(String, nullable=False)
    description = Column(String, nullable=False)
    food_category_id = Column(String, ForeignKey('food_category.id'), nullable=False)

    category = relationship("FoodCategory", back_populates="foods")
    attributes = relationship("FoodAttribute", back_populates="food")
    portions = relationship("FoodPortion", back_populates="food")
    branded_food = relationship("BrandedFood", back_populates="food", uselist=False)
    sample_food = relationship("SampleFood", back_populates="food", uselist=False)
    sr_legacy_foods = relationship("Sr_legacy_food", back_populates="food")
    nutrients = relationship("FoodNutrient", back_populates="food")

    def __str__(self):
        return f"{self.fdc_id}"

class FoodAttribute(base):
    __tablename__ = 'food_attribute'
    id = Column(Integer, primary_key=True)
    fdc_id = Column(Integer, ForeignKey('food.fdc_id'))
    seq_num = Column(String)
    food_attribute_type_id = Column(Integer, ForeignKey('food_attribute_type.id'))
    name = Column(String)
    value = Column(String)

    food = relationship("Food", back_populates="attributes")
    attribute_type = relationship("FoodAttributeType", back_populates="attributes")

class FoodAttributeType(base):
    __tablename__ = 'food_attribute_type'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    attributes = relationship("FoodAttribute", back_populates="attribute_type")

class FoodCategory(base):
    __tablename__ = 'food_category'
    id = Column(Integer, primary_key=True)
    code = Column(String)
    description = Column(String)

    foods = relationship("Food", back_populates="category")

class WWEIAFoodCategory(base):
    __tablename__ = 'wweia_food_category'
    wweia_food_category_code = Column(Integer, primary_key=True)
    wweia_food_category_description = Column(String)
    
class BrandedFood(base):
    __tablename__ = 'branded_food'
    fdc_id = Column(Integer, ForeignKey('food.fdc_id'), primary_key=True)
    brand_owner = Column(String)
    gtin_upc = Column(String)
    ingredients = Column(String)
    serving_size = Column(Float)
    serving_size_unit = Column(String)
    household_serving_fulltext = Column(String)
    branded_food_category = Column(String)
    data_source = Column(String)
    modified_date = Column(String)
    available_date = Column(String)
    market_country = Column(String)
    discontinued_date = Column(String)

    food = relationship("Food", back_populates="branded_food")


class SampleFood(base):
    __tablename__ = 'sample_food'
    fdc_id = Column(Integer, ForeignKey('food.fdc_id'), primary_key=True)

    food = relationship("Food", back_populates="sample_food")

class Sr_legacy_food(base):
    __tablename__ = 'sr_legacy_food'
    fdc_id = Column(Integer, ForeignKey('food.fdc_id'), primary_key=True)
    ndb_number = Column(Integer)

    food = relationship("Food", back_populates="sr_legacy_foods")
    
class Nutrient(base):
    __tablename__ = 'nutrient'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    unit_name = Column(String)
    nutrient_nbr = Column(String)
    rank = Column(Float)

    food_nutrients = relationship("FoodNutrient", back_populates="nutrient")
    
class FoodNutrient(base):
    __tablename__ = 'food_nutrient'
    id = Column(Integer, primary_key=True)
    fdc_id = Column(Integer, ForeignKey('food.fdc_id'))
    nutrient_id = Column(Integer, ForeignKey('nutrient.id'))
    amount = Column(Float)
    
    food = relationship("Food", back_populates="nutrients")
    nutrient = relationship("Nutrient", back_populates="food_nutrients")

class FoodPortion(base):
    __tablename__ = 'food_portion'
    id = Column(Integer, primary_key=True)
    fdc_id = Column(Integer, ForeignKey('food.fdc_id'))
    seq_num = Column(String)
    amount = Column(Float)
    measure_unit_id = Column(Integer, ForeignKey('measure_unit.id'))
    portion_description = Column(String)
    modifier = Column(String)
    gram_weight = Column(Float)
    data_points = Column(Integer)
    footnote = Column(String)
    min_year_acquired = Column(String)

    food = relationship("Food", back_populates="portions")
    measure_unit = relationship("MeasureUnit", back_populates="portions")

class MeasureUnit(base):
    __tablename__ = 'measure_unit'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    portions = relationship("FoodPortion", back_populates="measure_unit")