from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from queries import NutritionRepository
import textwrap


def show_welcome():
    print("""
    ###################################
    # WELCOME TO NUTRITION CALCULATOR #
    ###################################
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

def print_results(results, portion):
    if not results:
        print("\nNo results found.")
        return
    
    print(f"\nSearch Results (per {portion}g):")
    
    # Formatowanie nagłówków
    print("{:<60} | {:<30} | {:>10} | {:<10}".format(
        "Food Name", "Nutrient", "Amount", "Unit"
    ))
    separator = "-" * 120
    print(separator)
    
    # Grupujemy wyniki po nazwie produktu
    grouped_results = {}
    for row in results:
        if row.food_name not in grouped_results:
            grouped_results[row.food_name] = {}
        
        # Grupujemy składniki odżywcze
        if row.nutrient_name not in grouped_results[row.food_name]:
            grouped_results[row.food_name][row.nutrient_name] = {
                'values': [],
                'unit': row.unit_name
            }
        
        # Dodajemy wartość po przeliczeniu na porcję
        adjusted_amount = row.amount * (portion / 100)
        grouped_results[row.food_name][row.nutrient_name]['values'].append(adjusted_amount)
    
    # Ustalamy kolejność składników
    nutrient_order = [
        "Energy",
        "Carbohydrate, by difference",
        "Protein",
        "Total lipid (fat)"
    ]
    
    # Iterujemy po grupach produktów
    for food_name, nutrients in grouped_results.items():
        # Dzielimy długą nazwę produktu na wielolinijkowy blok
        name_lines = textwrap.wrap(food_name, width=60)
        
        # Wyświetlamy pierwszą część nazwy produktu w pierwszym wierszu
        print("{:<60} | {:<30} | {:>10} | {:<10}".format(
            name_lines[0] if name_lines else "",
            "",
            "",
            ""
        ))
        
        # Wyświetlamy pozostałe części nazwy (jeśli istnieją)
        for line in name_lines[1:]:            print("{:<60} | {:<30} | {:>10} | {:<10}".format(
                line,
                "",
                "",
                ""
            ))
        
        print(separator)
        
        # Iterujemy po składnikach odżywczych w ustalonej kolejności
        for nutrient_name in nutrient_order:
            if nutrient_name in nutrients:
                nutrient_data = nutrients[nutrient_name]
                values = nutrient_data['values']
                unit = nutrient_data['unit']
                
                # Obliczamy średnią jeśli jest wiele wartości
                if len(values) > 1:
                    avg_amount = sum(values) / len(values)
                    display_amount = f"{avg_amount:.2f} (avg)"
                else:
                    display_amount = f"{values[0]:.2f}"
                
                # Wyświetlamy wiersz ze składnikiem
                print("{:<60} | {:<30} | {:>10} | {:<10}".format(
                    "",
                    nutrient_name,
                    display_amount,
                    unit
                ))
        
        # Dodajemy dodatkową linię separatora po wszystkich składnikach produktu
        print(separator)

def main_menu(repo): 
    while True:
        print("\nMain Menu:")
        print("1. Search by Category")
        print("2. Search by Food Type")
        print("3. Search all Categories and Food Types (Whole Database)")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            handle_category_search(repo) 
        elif choice == '2':
            handle_food_type_search(repo)  
        elif choice == '3':
            handle_whole_database_search(repo)
        elif choice == '4':
            print("\nThank you for using Nutrition Calculator!")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1-4.")

def handle_category_search(repo):  
    print("\n=== Category Search ===")
    portion = get_user_portion()
    
    # Pokazujemy dostępne kategorie
    show_all_categories(repo)
    
    try:
        category_id = int(input("\nEnter category ID: "))
        search_term = input("Enter search term: ").strip()
        
        # Używamy metody repozytorium
        results = repo.get_by_food_category(category_id, search_term)
        
        if not results:
            print("\nNo results found for your search criteria.")
            return
            
        print_results(results, portion)
            
    except ValueError:
        print("\nInvalid category ID. Please enter a numeric value.")

def show_all_categories(repo):
    categories = repo.get_available_categories()
    print("\nAvailable Food Categories:")
    print("{:<6} | {}".format("ID", "Category Name"))
    print("-"*6 + "|" + "-"*30)
    for cat in categories:
        print("{:<6} | {}".format(cat.id, cat.description))

def handle_food_type_search(repo):
    print("\n=== Food Type Search ===")
    portion = get_user_portion()
    
    food_types = repo.get_available_food_types()
    
    print("\nAvailable Food Types:")
    for idx, (_, type_name) in enumerate(food_types, 1):
        print(f"{idx}. {type_name}")
    
    try:
        type_choice = int(input("\nEnter food type number (1-2): "))
        if type_choice < 1 or type_choice > 2:
            raise ValueError
            
        search_term = input("Enter search term: ").strip()
        food_type = food_types[type_choice-1][0]
        
        # Używamy metod repozytorium
        if food_type == 'branded_food':
            results = repo.get_branded_foods(search_term)
        elif food_type == 'sr_legacy_food':
            results = repo.get_legacy_foods(search_term)
        
        if not results:
            print("\nNo results found for your search criteria.")
            return
            
        print_results(results, portion)
            
    except ValueError:
        print("\nInvalid input. Please enter a number between 1-2.")

def handle_whole_database_search(repo):
    print("\n=== Whole Database Search ===")
    portion = get_user_portion()
    search_term = input("Enter search term: ").strip()

    results = repo.get_whole_database(search_term)

    if not results:
        print("\nNo results found for your search criteria.")
        return
    
    print_results(results, portion)

def main():
    engine = create_engine("sqlite:///USDA-SQLite.sqlite")
    Session = sessionmaker(bind=engine)
    
    with Session() as session:
        try:
            repo = NutritionRepository(session)
            
            show_welcome()
            main_menu(repo)  
        finally:
            session.close()

if __name__ == "__main__":
    main()