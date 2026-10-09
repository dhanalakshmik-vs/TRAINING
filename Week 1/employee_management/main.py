from employee_functions import (
        add_employee, show_employee, 
        update_employee, delete_employee, 
        search_employee, 
        filter_employee, 
        export_json, 
        export_csv
    )

def main():

    print("Employee Management")
    while True:

        print("\n1. Add an Employee\n2. View all employee\n3. Update an Employee\n4. Delete an Employee\n5. Search an Employee\n6. Filter an Employee\n7. Export JSON\n8. Export CSV\n9. Exit")

        while True:
            try:
                choice = int(input("Enter the choice: "))

                if choice >= 1 and choice <= 9:
                    break

                print("Please enter a number between 1 and 9.")

            except ValueError:
                print("Please enter a valid number.")

        if choice == 1:
            add_employee()
    
        elif choice == 2:
            show_employee()

        elif choice == 3:
            update_employee()

        elif choice == 4:
            delete_employee()

        elif choice == 5:
            search_employee()

        elif choice == 6:
            filter_employee()

        elif choice == 7:
            export_json()

        elif choice == 8:
            export_csv()

        elif choice==9:
            print("Thank you")
            exit()


if __name__ == "__main__":
    main()
