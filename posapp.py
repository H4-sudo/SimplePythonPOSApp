import os

class Waiter:
    '''
    The Waiter class is used for the purpose of signing a user in based on their username and password,
    the username and password are read from an external file.
    '''
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Table:
    '''
    The Table class is used to pre-define the structure of how the tables will be presented throughout
    the program.
    '''
    def __init__(self, number, waiter=None):
        self.number = number
        self.waiter = waiter
        self.customers = 0
        self.orders = []
        self.bill = None
    
    def __str__(self):
        return f"Table {self.number}"

class Bill:
    '''
    The Bill class is used for creating the "Bill" for the waiter to give to the customer,
    it has a display_bill method and a save_bill method where the save_bill method saves the bill to
    a user defined file. The display_bill method is only visible to the waiter that is currently signed in.
    There is a calculate bill method as well, that calculates the total the customer owes.
    '''
    def __init__(self, table_number):
        self.table_number = table_number
        self.items = []

    def add_item(self, item, quantity):
        self.items.append((item, quantity))

    def display_bill(self):
        print("===================================")
        print(f"Bill for Table {self.table_number}\n")
        print("        Item         Quantity    Price")
        for item, quantity in self.items:
            print(f"        {item.name}    x    {quantity}           R{item.price}")
        print(f"Total: R{self.calculate_bill_total()}")
        print("===================================")

    def calculate_bill_total(self):
        total = 0
        for item, quantity in self.items:
            total += item.price * quantity
        return total

    def save_bill(self, filename):
        with open(filename, 'w') as file:
            file.write("==========================================\n")
            file.write(f"Bill for Table {str(self.table_number)}\n")
            file.write("\n        Item         Quantity    Price\n")
            for item, quantity in self.items:
                file.write(f"\n        {item.name}    x    {quantity}           R{item.price}\n")
            file.write("\nTotal: R" + str(self.calculate_bill_total()) + "\n")
            file.write("==========================================")
        print(f"Bill saved as: {filename}")

class Item:
    '''
    The Item class has the same functionality as that of the Waiter class. It reads the stock items
    from an external file, and implements it throughout the code.
    '''
    def __init__(self, name, price):
        self.name = name
        self.price = price

class POSApplication:
    '''
    The POSApplication class is used to define and initialise all the other classes. It also contains
    the "run" method to be able to use the Point-of-Sale application. It consists of 2 loading methods
    wherein it loads the waiters file, and the stock file to be made available to the program. It contains
    the display_main_menu method and the "login" method wherein the username and password are used to log the
    waiter in. The assign_table method assigns a table to the waiter that is logged in.
    '''
    def __init__(self):
        self.waiters = []
        self.tables = []
        self.sales = 0
        self.items = []
        self.available_tables = []

    def load_waiters(self, filename):
        ''' 
        # This function loads the "Login.txt" file to be used
        # by the application as the login for the waiters.
        '''
        with open(filename, 'r') as file:
            for line in file:
                username, password = line.strip().split(',')
                self.waiters.append(Waiter(username, password))

    def load_stock(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                item_name, price = line.strip().split(',')
                item = Item(item_name, float(price))
                self.items.append(item)

    def display_main_menu(self):
        print("\nMain Menu:")
        print("1. Assign Table")
        print("2. Change amount of customers")
        print("3. Add to Order")
        print("4. Prepare bill")
        print("5. Complete Sale")
        print("6. Cash up")
        print("0. Log Out\n")

    def login(self):
        print("User Login\n")
        username = input("Username: ")
        password = input("Password: ")
        for waiter in self.waiters:
            if waiter.username == username and waiter.password == password:
                return waiter
        return None

    def assign_table(self, waiter):
        if not self.available_tables:
            print("No tables available.")
            return
        for table_num in self.available_tables:
            print(f"{table_num}. Table {table_num}")
        table_number = int(input("Enter table number: "))
        if table_number not in self.available_tables:
            print("Invalid table number.")
            return

        for table in self.tables:
            if table.number == table_number:
                if table.waiter is not None:
                    print(f"Table {table_number} is already assigned to another waiter.")
                else:
                    table.waiter = waiter
                    print(f"Table {table.number} assigned to {waiter.username}")
                    self.available_tables.remove(table.number)
                    self.add_customers(table, waiter)
                break

    def add_customers(self, table, waiter):
        add_customer_choice = input("Would you like to add customers to the table?(Yes/No)\n")
        if add_customer_choice.lower() == 'yes' or add_customer_choice.lower() == 'y':
            self.show_assigned_tables(waiter)
            table_selection = input("Please select an available table: ")
            try:
                table_selection = int(table_selection)
                selected_table = self.get_table_by_num(table_selection)
                if selected_table:
                    customers = input("Enter the number of customers: ")
                    try:
                        customers = int(customers)
                        table.customers = customers
                    except TypeError:
                        print("Please input a number.")
                else:
                    print("Invalid table number.")
            except TypeError:
                print("Please input a number.")
        elif add_customer_choice.lower() == 'no' or add_customer_choice == 'n':
            self.display_main_menu()
        else:
            print("Invalid choice, please try again.")

    def change_customer_amount(self, waiter):
        assigned_tables = [table for table in self.tables if table.waiter == waiter]
        self.show_assigned_tables(waiter)
        table_number = int(input("Enter table number: "))
        for table in assigned_tables:
            if table.number == table_number:
                self.add_customers(table, waiter)
                break
        else:
            print("Invalid table number.")

    def add_to_order(self, waiter):
        assigned_tables = [table for table in self.tables if table.waiter == waiter]
        self.show_assigned_tables(waiter)
        table_number = int(input("Enter table number: "))
        for table in assigned_tables:
            
            if table.number == table_number:
                print("Available items:")
                for i, item in enumerate(self.items, start=1):
                    print(f"{i}. {item.name} - R{item.price}")

                item_index = int(input("Enter the item number: ")) - 1
                if item_index < 0 or item_index >= len(self.items):
                    print("Invalid item number.")
                    return

                item = self.items[item_index]

                quantity = int(input("Enter quantity: "))
                table.orders.append((item, quantity))
                print(f"{quantity} {item.name}(s) added to the order.")
                break
        else:
            print("Invalid table number.")


    def prepare_bill(self, waiter):
        assigned_tables = [table for table in self.tables if table.waiter == waiter]
        self.show_assigned_tables(waiter)
        table_number = int(input("Enter table number: "))
        for table in assigned_tables:
            if table.number == table_number:
                bill = Bill(table.number)
                bill.items = table.orders
                table.bill = bill
                bill.display_bill()
                break
        else:
            print("Invalid table number.")

    def complete_sale(self, waiter):
        assigned_tables = [table for table in self.tables if table.waiter == waiter]
        self.show_assigned_tables(waiter)
        table_number = input("Enter the table number: ")
        try:
            table_number = int(table_number)
            for table in assigned_tables:
                if table.number == table_number:
                    if table.bill is None:
                        print("Bill has not yet been prepared.")
                        return

                    self.sales += table.bill.calculate_bill_total()
                    self.clear_orders(table)
                    self.clear_waiter_assignment(table)
                    self.save_bill(table.bill)
                    print("Sale completed successfully.")
                    break
            else:
                print("Invalid table number.")
        except TypeError:
            print("Please input a valid number.")

    def cash_up(self):
        print("Total sales: R", self.sales)
        clear = input("Clear daily total? (Yes/No): ")
        if clear.lower() == "yes" or clear.lower() == 'y':
            self.sales = 0

    def clear_orders(self, table):
        table.orders = []

    def clear_waiter_assignment(self, table):
        table.waiter = None
        self.available_tables.append(table.number)

    def get_item(self, name):
        for item in self.items:
            if item.name == name:
                return item
        return None

    def save_bill(self, bill):
        filename = input("Enter file name to save the bill: ")
        bill.save_bill(filename)

    def run(self):
        ''' 
        # This method is used to make the Class run when called by
        # using {object}.run(), after assigning the {object} with
        # the POSApplication class.
        '''
        self.load_waiters("Login.txt")
        self.load_stock("Stock.txt")
        self.create_tables(6) # Creates the tables before a waiter logs in
        while True:
            print("Welcome to Highlands Café\n")
            print("1. Login\n2. Exit\n")

            use_pos = input("Please select an option: ")
            if use_pos == '1':
                login_success = False
                while not login_success:
                    current_waiter = self.login()
                    if current_waiter is not None:
                        login_success = True
                    else:
                        print("Invalid username or password. Please try again.")

                    while True:
                        self.display_main_menu()
                        choice = input("Enter your choice: ")
                        if choice == '1':
                            self.assign_table(current_waiter)
                        elif choice == '2':
                            self.change_customer_amount(current_waiter)
                        elif choice == '3':
                            self.add_to_order(current_waiter)
                        elif choice == '4':
                            self.prepare_bill(current_waiter)
                        elif choice == '5':
                            self.complete_sale(current_waiter)
                        elif choice == '6':
                            self.cash_up()
                        elif choice == '0':
                            print("Logged out.")
                            break
                        else:
                            print("Invalid choice. Please try again.")

                    restart = input("Do you want to log in with a different account? (Yes/No): ")
                    if restart.lower() == "yes":
                        continue
                    elif restart.lower() == 'no':
                        print("Goodbye!")
                        exit()

            elif use_pos == '2':
                print("Goodbye!")
                exit()

            else:
                print("Please enter a valid selection.")

    def create_tables(self, num_tables, waiter=None):
        '''
        This method is used for the creation of the available tables. You call the method to
        give the amount of tables that you would like to make available.
        '''
        self.tables = []
        self.available_tables = []
        for i in range(1, num_tables + 1):
            table = Table(i, waiter)
            self.tables.append(table)
            self.available_tables.append(i)
    
    def show_assigned_tables(self, waiter):
        '''
        This method is used to show the tables that are assigned to a specific waiter in the program.
        It prints out the table number that is assigned to the waiter if there is any.
        '''
        waiter_assigned_tables = [table for table in self.tables if table.waiter == waiter]
        if not waiter_assigned_tables:
            print("You are not assigned to any tables.")
        else:
            print("Assigned tables:")
            for table in waiter_assigned_tables:
                print(f"{table.number}. {table}")

    def get_table_by_num(self, table_number):
        for table in self.tables:
            if table.number == table_number:
                return table
        return None

# Usage of the POS Application
app = POSApplication()
app.run()

# Made by Henrico Swanepoel, ICAS:20231912