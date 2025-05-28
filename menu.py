from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from queries import get_available_categories, get_by_food_category, get_available_food_types, get_branded_foods, get_legacy_foods, get_sample_foods


def show_welcome():
    print("""
    ################################
    #  WELCOME TO NUTRITION CALCULATOR  #
    ################################
    """)

def get_user_portion() -> float:
    while True:
        try:
            portion = float(input("Enter portion size in grams (default 100g): ") or 100)
            if portion <= 0:
                raise ValueError
            return portion
        except ValueError:
            print("Invalid input. Please enter a positive number.")

def main_menu(session):
    while True:
        print("\nMain Menu:")
        print("1. Search by Category")
        print("2. Search by Food Type")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            handle_category_search(session)
        elif choice == '2':
            handle_food_type_search(session)
        elif choice == '3':
            print("\nThank you for using Nutrition Calculator!")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1-4.")

def handle_category_search(session):
    print("\n=== Category Search ===")
    portion = get_user_portion()
    categories = get_available_categories(session)
    
    # Pokazujemy najpierw dostępne kategorie
    show_all_categories(session)
    
    try:
        category_id = int(input("\nEnter category ID: "))
        search_term = input("Enter search term: ").strip()
        
        results = get_by_food_category(session, category_id, search_term)
        
        if not results:
            print("\nNo results found for your search criteria.")
            return
            
        print(f"\nSearch Results (per {portion}g):")
        print("{:<50} | {:<20} | {:<10} | {}".format(
            "Food Name", "Nutrient", "Amount", "Unit"
        ))
        print("-"*100)
        
        for row in results:
            adjusted_amount = row.amount * (portion / 100)
            print("{:<50} | {:<20} | {:<10} | {}".format(
                row.food_name,
                row.nutrient_name,
                round(adjusted_amount, 2),
                row.unit_name
            ))
            
    except ValueError:
        print("\nInvalid category ID. Please enter a numeric value.")

def show_all_categories(session):
    categories = get_available_categories(session)
    print("\nAvailable Food Categories:")
    print("{:<6} | {}".format("ID", "Category Name"))
    print("-"*6 + "|" + "-"*30)
    for cat in categories:
        print("{:<6} | {}".format(cat.id, cat.description))

def handle_food_type_search(session):
    print("\n=== Food Type Search ===")
    portion = get_user_portion()
    food_types = get_available_food_types()
    
    print("\nAvailable Food Types:")
    for idx, (_, type_name) in enumerate(food_types, 1):
        print(f"{idx}. {type_name}")
    
    try:
        type_choice = int(input("\nEnter food type number (1-3): "))
        if type_choice < 1 or type_choice > 3:
            raise ValueError
            
        search_term = input("Enter search term: ").strip()
        food_type = food_types[type_choice-1][0]
        
        if food_type == 'branded_food':
            results = get_branded_foods(session, search_term)
        elif food_type == 'sr_legacy_food':
            results = get_legacy_foods(session, search_term)
        elif food_type == 'sample_food':
            results = get_sample_foods(session, search_term)
        
        if not results:
            print("\nNo results found for your search criteria.")
            return
            
        print(f"\nSearch Results (per {portion}g):")
        print("{:<50} | {:<20} | {:<10} | {}".format(
            "Food Name", "Nutrient", "Amount", "Unit"
        ))
        print("-"*100)
        
        for row in results:
            adjusted_amount = row.amount * (portion / 100)
            print("{:<50} | {:<20} | {:<10} | {}".format(
                row.food_name,
                row.nutrient_name,
                round(adjusted_amount, 2),
                row.unit_name
            ))
            
    except ValueError:
        print("\nInvalid input. Please enter a number between 1-3.")

def main():
    engine = create_engine("sqlite:///USDA-SQLite.sqlite")
    Session = sessionmaker(bind=engine)
    
    with Session() as session:
        try:
            show_welcome()
            main_menu(session)
        finally:
            session.close()

if __name__ == "__main__":
    main()