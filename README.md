# NutriCalc - nutrition-calculator

## Założenia projektu:

Aplikacja będzie miała za zadanie przeliczenie wartości odżywczych w wybranej przez użytkownika żywności (podstawowe - węglowodany, białka, tłuszcze, skład ilościowy wody), (inne - np. witaminy, minerały - opcjonalnie), (kcal) - wyniki będą opracowane na podstawie dostępnych baz/bazy danych powiązanych z żywnością (baza danych USDA). W przypadku nie odnalezienia podanego typu żywności program nie będzie wyświetlał wyników.

Program będzie przeliczał wartości odżywcze przypadające na wybraną (ustaloną) ilość, np. 100 g.



Projekt będzie oparty na wykorzystaniu terminala (bez GUI).

### Propozycje zmian/rozszerzenia projektu:

- wprowadzenie GUI 
- możliwość korzystania z baz danych online
- korzystanie z innej bazy danych (zawierających polską żywność/produkty)

- możliwość wyliczenia wartości odżywczych na podstawie dania (nie pojedynczego produktu)

## Funkcjonalności

- wyświetlanie podstawowych wyników wyszukiwań dla wybranej żywności ✅
- wyświetlanie podstawowych składników odżywczych dla wybranej żywności (węglowodany, białka, tłuszcze, wartość odżywcza w kcal) ✅

- wyświetlanie wyników dla wybranej przez użytkownika wartości (w g) (domyślnie jest to 100 g) ✅

## Technologie

- SQLite + SQLAlchemy (lokalna baza danych)

### Link do wykorzystywanej bazy danych:

```
https://github.com/MenuLogistics/USDASQLite
```

### Uproszczony schemat wykorzystywanej bazy danych:
```mermaid
erDiagram
    FOOD {
        Integer fdc_id PK
        String data_type
        String description
        String food_category_id FK
    }
    
    FOOD_CATEGORY {
        Integer id PK
        String code
        String description
    }
    
    FOOD_ATTRIBUTE {
        Integer id PK
        Integer fdc_id FK
        String seq_num
        Integer food_attribute_type_id FK
        String name
        String value
    }
    
    FOOD_ATTRIBUTE_TYPE {
        Integer id PK
        String name
        String description
    }
    
    BRANDED_FOOD {
        Integer fdc_id PK,FK
        String brand_owner
        String gtin_upc
        String ingredients
        Float serving_size
        String serving_size_unit
        String household_serving_fulltext
        String branded_food_category
        String data_source
        String modified_date
        String available_date
        String market_country
        String discontinued_date
    }
    
    SAMPLE_FOOD {
        Integer fdc_id PK,FK
    }
    
    SR_LEGACY_FOOD {
        Integer fdc_id PK,FK
        Integer ndb_number
    }
    
    NUTRIENT {
        Integer id PK
        String name
        String unit_name
        String nutrient_nbr
        Float rank
    }
    
    FOOD_NUTRIENT {
        Integer id PK
        Integer fdc_id FK
        Integer nutrient_id FK
        Float amount
    }
    
    FOOD_PORTION {
        Integer id PK
        Integer fdc_id FK
        String seq_num
        Float amount
        Integer measure_unit_id FK
        String portion_description
        String modifier
        Float gram_weight
        Integer data_points
        String footnote
        String min_year_acquired
    }
    
    MEASURE_UNIT {
        Integer id PK
        String name
    }
    
    WWEIA_FOOD_CATEGORY {
        Integer wweia_food_category_code PK
        String wweia_food_category_description
    }

    FOOD ||--o{ FOOD_ATTRIBUTE : attributes
    FOOD ||--o{ FOOD_PORTION : portions
    FOOD ||--o{ FOOD_NUTRIENT : nutrients
    FOOD ||--|| BRANDED_FOOD : branded_food
    FOOD ||--|| SAMPLE_FOOD : sample_food
    FOOD ||--|| SR_LEGACY_FOOD : sr_legacy_foods
    FOOD }o--|| FOOD_CATEGORY : category
    FOOD_ATTRIBUTE }o--|| FOOD_ATTRIBUTE_TYPE : attribute_type
    FOOD_PORTION }o--|| MEASURE_UNIT : measure_unit
    FOOD_NUTRIENT }o--|| NUTRIENT : nutrient
```
