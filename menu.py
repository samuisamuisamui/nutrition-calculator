from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from queries import get_available_categories, get_by_food_category  # zaimportuj odpowiednie funkcje

def show_welcome():
    print("""
    ################################
    #  WELCOME TO NUTRITION CALCULATOR  #
    ################################
    """)

def main_menu(session):
    while True:
        print("\nMain Menu:")
        print("1. Search by Category")
        print("2. Search by Food Type")
        print("3. Calculator")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            handle_category_search(session)
        elif choice == '2':
            handle_food_type_search(session)
        elif choice == '4':
            print("\nThank you for using Nutrition Calculator!")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1-4.")

def handle_category_search(session):
    print("\n=== Category Search ===")
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
            
        print("\nSearch Results:")
        print("{:<50} | {:<20} | {:<10} | {}".format(
            "Food Name", "Nutrient", "Amount", "Unit"
        ))
        print("-"*100)
        
        for row in results:
            print("{:<50} | {:<20} | {:<10} | {}".format(
                row.food_name,
                row.nutrient_name,
                round(row.amount, 2),
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
    # Tutaj możesz dodać logikę dla wyszukiwania przez typ żywności
    print("\nThis feature is under construction. Please check back later!")

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