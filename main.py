from utils import *
from classes import *


# Integrating load operations to initialize the system with data from JSON files at startup



def start_system():
    while True:
        print("\nWelcome to the Library Management System!")
        print("Main Menu:")
        print("1. Book Operations")
        print("2. User Operations")
        print("3. Author Operations")
        print("4. Genre Operations")
        print("5. Quit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            handle_book_operations()
        elif choice == '2':
            handle_user_operations()
        elif choice == '3':
            handle_author_operations()
        elif choice == '4':
            handle_genre_operations()
        elif choice == '5':
            print("Thank you for using the Library Management System.")
            break
        else:
            print("Invalid choice. Please try again.")

        if input("Return to Main Menu? (yes/no): ").lower() != 'yes':
            print("Exiting system...")
            break

def run_startup_tests():
    print("Running startup tests...")
    test_database_connection()
    test_initial_data_fetch()
    test_operational_readiness()
    print("All startup tests passed successfully.")

def main():
    try:
        # run_startup_tests()  # Ensuring all systems are go before starting
        start_system()
    except Exception as e:
        print(f"An error occurred during system startup: {e}")
    finally:
        print("System shutdown.")

if __name__ == "__main__":
    main()



