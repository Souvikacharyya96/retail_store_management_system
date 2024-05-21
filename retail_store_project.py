import mysql.connector
import random

# Connect to MySQL
conn_obj = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Souvik@1996",
    auth_plugin="mysql_native_password"
)
cur_obj = conn_obj.cursor()

# Create a new database
try:
    cur_obj.execute("CREATE DATABASE IF NOT EXISTS retail_database")
    conn_obj.commit()
except mysql.connector.Error as err:
    print(f"Error1: {err}")
    conn_obj.rollback()

# Use the created database
try:
    cur_obj.execute("USE retail_database")
except mysql.connector.Error as err:
    print(f"Error2: {err}")
    conn_obj.rollback()

# Create a users table
cur_obj.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id VARCHAR(50) PRIMARY KEY,
        full_name VARCHAR(50) NOT NULL,
        username VARCHAR(50) NOT NULL,
        password VARCHAR(50) NOT NULL,
        email_id VARCHAR(50) NOT NULL
    )
''')

# Create a table for PRODUCTS
try:
    cur_obj.execute(''' 
    CREATE TABLE IF NOT EXISTS product_category (
        product_id INT AUTO_INCREMENT PRIMARY KEY,
        product_category VARCHAR(50) NOT NULL,
        product_name VARCHAR(50) NOT NULL,
        buy_price DECIMAL(10, 2) NOT NULL,
        sale_price DECIMAL(10,2) NOT NULL,
        stock_quantity DECIMAL(10, 2) NOT NULL
        )
    ''')
    conn_obj.commit()
except mysql.connector.Error as err:
    print(f"Error: {err}")

# Create a table for CUSTOMERS
try:
    cur_obj.execute('''
   CREATE TABLE IF NOT EXISTS customers (
        customer_id VARCHAR(50) PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        phone VARCHAR(50) NOT NULL,
        address VARCHAR(50) NOT NULL,
        city VARCHAR(50) NOT NULL,
        state VARCHAR(50) NOT NULL,
        country VARCHAR(50) NOT NULL,
        pincode VARCHAR(50) NOT NULL
        )
    ''')
    conn_obj.commit()
except mysql.connector.Error as err:
    print(f"Error: {err}")

# Create a table for ORDERS
try:
    cur_obj.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INT AUTO_INCREMENT PRIMARY KEY,
        customer_id VARCHAR(50) NOT NULL,
        product_name VARCHAR(50) NOT NULL,
        quantity INT NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        order_date DATE
        )
    ''')
    conn_obj.commit()
except mysql.connector.Error as err:
    print(f"Error: {err}")

def generate_customer_id():
    return "".join(random.choices("S01", k=3))

def generate_user_id():
    return "".join(random.choices("0123", k=4))

def add_product(product_category, product_name, buy_price, sale_price, stock_quantity):
    try:
        cur_obj.execute("INSERT INTO product_category (product_category, product_name, buy_price, sale_price, stock_quantity) VALUES (%s, %s, %s, %s, %s)", (product_category, product_name, buy_price, sale_price, stock_quantity))
        conn_obj.commit()
        product_id = cur_obj.lastrowid
        print("\nProduct added successfully.")
        print(f"PRODUCT ID : {product_id}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def customer_details(customer_id, name, phone, address, city, state, country, pincode):
    try:
        customer_id = generate_customer_id()
        cur_obj.execute("INSERT INTO customers (customer_id, name, phone, address, city, state, country, pincode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (customer_id, name, phone, address, city, state, country, pincode))
        conn_obj.commit()
        print("CUSTOMER DETAILS ADDED SUCCESSFULLY")
        print(f"CUSTOMER ID: {customer_id}")
        return customer_id
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def search_product_price(product_name):
    try:
        cur_obj.execute(
            "SELECT sale_price, stock_quantity FROM product_category WHERE product_name = %s",
            (product_name,))
        result = cur_obj.fetchall()

        if result:
            price_per_product = result[0][0]
            print("\nPRICE:", result[0][0])
            print("STOCK AVAILABLE:", result[0][1])
            return price_per_product
        else:
            print("Product not found")
            return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")

def place_order(customer_id, product_name, quantity, price, order_date):
    try:
        cur_obj.execute("SELECT stock_quantity FROM product_category WHERE product_name = %s", (product_name,))
        stock_quantity = cur_obj.fetchone()[0]
        if stock_quantity >= quantity:
            cur_obj.execute("UPDATE product_category SET stock_quantity = stock_quantity - %s WHERE product_name = %s", (quantity, product_name))

            cur_obj.execute(
                "INSERT INTO orders (customer_id, product_name, quantity, price, order_date) VALUES (%s, %s, %s, %s, %s)",
                (customer_id, product_name, quantity, price, order_date))
            conn_obj.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

def view_orders(customer_id, order_id):
    cur_obj.execute("SELECT * FROM orders WHERE customer_id = %s AND order_id = %s", (customer_id, order_id,))
    result = cur_obj.fetchall()

    if result:
        print("DATE:", result[0][5])
        print("PRODUCT NAME:", result[0][2])
        print("QUANTITY:", result[0][3])
        print("PRICE:", result[0][4])
        print("ORDER DATE:", result[0][5])

# Function to register a new user
def register_user(user_id, full_name, username, password, email_id):
    try:
        cur_obj.execute("INSERT INTO users (user_id, full_name, username, password, email_id) VALUES (%s, %s, %s, %s, %s)", (user_id, full_name, username, password, email_id))
        conn_obj.commit()
        print("USER REGISTERED SUCCESSFULY.")
        # Retrieve the user_id of the newly inserted user
        cur_obj.execute("SELECT user_id FROM users WHERE username = %s", (username,))
        result = cur_obj.fetchone()

        if result:
            user_id = result[0]
            print(f"YOUR REGISTERED USER ID: SUVO{user_id}")
        else:
            print("USER ID NOT AVAILABLE")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn_obj.rollback()

# Function to authenticate an existing user
# Giving options to upload user's details
def existing_user(username, password):
    cur_obj.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cur_obj.fetchall()
    if user:
        print("\nLOGIN SUCCESSFUL.")
        # Main Menu
        print("\nARE YOU A BUYER OR SELLER?")
        print("1. SELLER")
        print("2. BUYER")

        option = input("ENTER YOUR CHOICE: ")

        if option == "1":
            while True:
                product_category = input("ENTER YOUR PRODUCT CATEGORY: ")
                product_name = input("ENTER PRODUCT NAME: ")
                buy_price = float(input("ENTER PRODUCT BUY PRICE: "))
                sale_price = float(input("ENTER PRODUCT SALE PRICE: "))
                stock_quantity = float(input("ENTER PRODUCT STOCK QUANTITY: "))
                add_product(product_category, product_name, buy_price, sale_price, stock_quantity)
                print("If you want to add more product write 'Yes'. Else you can write 'No'.")
                user_input = input("Add product Yes/No?: ")
                if user_input == "Yes":
                    continue
                elif user_input == "No":
                    break
        elif option == "2":
            while True:
                print("\nWELCOME TO THE SUVO RETAIL STORE MANAGEMENT SYSTEM".center(50))
                print("\n1. NEW USER")
                print("2. SEARCH PRODUCT")
                print("3. ADD TO CART")
                print("4. EXIT")

                option = input("\nCHOOSE YOUR OPTION IN (1/2/3): ")

                if option == "1":
                    customer_id = generate_customer_id()
                    name = input("Enter customer name: ")
                    try:
                        cur_obj.execute("SELECT * FROM customers WHERE name = %s", (name,))
                        result = cur_obj.fetchall()

                        if result:
                            print("This name is used before. So, you can't used it again.")
                            break
                        else:
                            print(" ")

                    except mysql.connector.Error as err:
                        print(f"Error: {err}")
                        conn_obj.rollback()

                    phone = input("Enter customer phone: ")
                    try:
                        cur_obj.execute("SELECT * FROM customers WHERE phone = %s", (phone,))
                        result = cur_obj.fetchall()

                        if result:
                            print("This Phone No. is used before. So, you can't used it again.")
                            break
                        else:
                            print(" ")

                    except mysql.connector.Error as err:
                        print(f"Error: {err}")
                        conn_obj.rollback()

                    address = input("Enter customer address: ")
                    city = input("Enter customer city: ")
                    state = input("Enter customer state: ")
                    country = input("Enter customer country: ")
                    pincode = input("Enter customer pincode: ")
                    customer_details(customer_id, name, phone, address, city, state, country, pincode)
                elif option == "2":
                    while True:
                        print("\nSEE PRODUCT AVAILABILITY HERE")
                        product_name = input("\nENTER PRODUCT NAME: ")
                        price_per_product = search_product_price(product_name)
                        if price_per_product is not None:
                            quantity = int(input("QUANTITY: "))
                            total_cost = price_per_product * quantity
                            print(f"TOTAL COST TO BUY THE PRODUCT: {total_cost}")
                        else:
                            print("Product not found")
                        print("\nIf you want to add more product write 'Yes'. Else you can write 'No'.")
                        user_input = input("\nAdd product Yes/No?: ")
                        if user_input == "Yes":
                            continue
                        elif user_input == "No":
                            break
                elif option == "3":
                    while True:
                        print("\n1. PLACE ORDER")
                        print("2. VIEW ORDERS")
                        print("3. EXIT")

                        option = input("\nENTER YOUR CHOICE: ")

                        if option == "1":
                            customer_id = input("ENTER YOUR CUSTOMER ID: ")
                            try:
                                cur_obj.execute("SELECT * FROM customers WHERE customer_id = %s",
                                                (customer_id,))
                                result = cur_obj.fetchall()

                                if result:
                                    print(" ")
                                else:
                                    print("This customer id is not found.")
                                    break

                            except mysql.connector.Error as err:
                                print(f"Error: {err}")
                                conn_obj.rollback()

                            product_name = input("ENTER PRODUCT NAME: ")
                            try:
                                cur_obj.execute("SELECT * FROM product_category WHERE product_name = %s",
                                                (product_name,))
                                result = cur_obj.fetchall()

                                if result:
                                    print(" ")
                                else:
                                    print("This product is not available.")
                                    break

                            except mysql.connector.Error as err:
                                print(f"Error: {err}")
                                conn_obj.rollback()

                            quantity = int(input("QUANTITY: "))
                            price_per_product = search_product_price(product_name)
                            if price_per_product is not None:
                                total_cost = price_per_product * quantity
                                print(f"TOTAL COST TO BUY THE PRODUCT: {total_cost}")
                            else:
                                print("Product not found")
                            price = float(input("\nPLEASE PAY TOTAL PRICE TO COMPLETE YOUR ORDER: "))
                            if price == total_cost:
                                print("\nOrder placed successfuly.")
                            else:
                                print("Order not placed successfuly.")
                            order_date = date.today()
                            place_order(customer_id, product_name, quantity, price, order_date)
                            try:
                                cur_obj.execute("SELECT * FROM orders WHERE customer_id = %s", (customer_id,))
                                result = cur_obj.fetchall()
                                if result:
                                    print("Order Id:", result[0][0])
                                else:
                                    print(" ")
                            except mysql.connector.Error as err:
                                print(f"Error: {err}")
                                conn_obj.rollback()
                        elif option == "2":
                            customer_id = input("ENTER YOUR CUSTOMER ID: ")
                            try:
                                cur_obj.execute("SELECT * FROM orders WHERE customer_id = %s",
                                                (customer_id,))
                                result = cur_obj.fetchall()

                                if result:
                                    print(" ")
                                else:
                                    print("This customer id is not found.")
                                    break

                            except mysql.connector.Error as err:
                                print(f"Error: {err}")
                                conn_obj.rollback()

                            order_id = int(input("ENTER YOUR ORDER ID: "))
                            try:
                                cur_obj.execute("SELECT * FROM orders WHERE order_id = %s",
                                                (order_id,))
                                result = cur_obj.fetchall()

                                if result:
                                    print(" ")
                                else:
                                    print("This order id is not found.")
                                    break

                            except mysql.connector.Error as err:
                                print(f"Error: {err}")
                                conn_obj.rollback()
                            view_orders(customer_id, order_id)
                        elif option == "3":
                            print("EXISTING PAGE. GOOD BYE!")
                            break
                elif option == "4":
                    print("EXISTING PAGE. GOOD BYE!")
                    break
                else:
                    print("INVALID OPTION")
        return True
    else:
        print("LOGIN FAILED. INVALID USER NAME OR PASSWORD.")
        return False

def genaration_pin():
    return "".join(random.choices("0123", k=4))

def forgot_password(username, password):
    try:
        cur_obj.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur_obj.fetchall()
        if user:
            # Update Password
            cur_obj.execute(f"UPDATE users SET password = %s WHERE username = %s", (password, username,))
            print("\nNEW PASSWORD UPDATE SUCCESSFULY")
            print(f"YOUR NEW PASSWORD: {password}")
            conn_obj.commit()
        else:
            print("ENTERED WRONG USERNAME")
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()

# LOGIN Menu
while True:
    print("HELLO, USER".center(50))
    print("WELCOME TO THE SUVO RETAIL STORE MANAGEMENT SYSTEM".center(50))
    print("\nPLEASE CONFIRM: \nARE YOU A NEW USER OR AN EXISTING USER?")
    print("\nCHOOSE THE RIGHT OPTION BETWEEN 1 & 2:")
    print("1. REGISTER A NEW USER")
    print("2. LOGIN")
    print("3. FORGET PASSWORD")
    print("4. LOGOUT")

    action = input("\nPLEASE SELECT THE OPTION: ")

    if action == "1":
        def validate_input(full_name, username, password, email_id):
            if not (full_name.isupper() == True):
                print("FULL NAME IS IN WRONG FORMAT, PLEASE CHECK")
                return False
            if not (username.find("@") != -1 and username.istitle() and len(username) < 17):
                print("USERNAME IS WRONG, PLEASE CHECK")
                return False
            elif not(len(password) <= 8 and password.istitle()):
                print("PASSWORD IS WRONG, PLEASE CHECK")
                return False
            elif not (email_id.find("@") != -1 and email_id.endswith(".com")):
                print("EMAIL ID IS WRONG, PLEASE CHECK")
                return False
            return True

        user_id = generate_user_id()
        full_name = input("\nENTER YOUR FULL NAME(IN CAPITAL LETTERS): ")
        username = input("\nENTER USER NAME(FORMAT: Limit - 15 Characters(Alphabet, Special Character only '@', Numbers are allowed), EX- 'Souvik@1996'): ")
        try:
            cur_obj.execute("SELECT * FROM users WHERE username = %s", (username,))
            result = cur_obj.fetchall()

            if result:
                print("THIS USERNAME IS USED BEFORE")
                break
            else:
                print(" ")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            conn_obj.rollback()
        password = input("\nENTER NEW PASSWORD(FORMAT: Limit - 8 Characters(Only Alphabet & Numbers), EX- 'Suvo1996'): ")
        try:
            cur_obj.execute("SELECT * FROM users WHERE password = %s", (password,))
            result = cur_obj.fetchall()

            if result:
                print("THIS PASSWORD IS USED BEFORE")
                break
            else:
                print(" ")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            conn_obj.rollback()
        email_id = input("\nENTER YOUR EMAIL ID: ")

        if validate_input(full_name, username, password, email_id):
            # Check for duplicate username and password in the database
            try:
                cur_obj.execute("SELECT username, password FROM users WHERE full_name = %s OR username = %s OR password = %s OR email_id = %s",(full_name, username, password, email_id))
                result7 = cur_obj.fetchall()

                if result7:
                    print("THIS USER NAME OR PASSWORD CANNOT BE UPLOADED (USED)")
                else:
                    print("USERNAME & PASSWORD IS ACCEPTED")
                    print(f"\nYOUR REGISTERED USER NAME: {username} AND PASSWORD: {password}")
                    register_user(user_id, full_name, username, password, email_id)

            except mysql.connector.Error as err:
                print(f"Error: {err}")
                conn_obj.rollback()
        else:
            print("PLEASE CHECK USER NAME OR PASSWORD")
        pass
    elif action == "2":
        attempt = 3
        while attempt > 0:
            username = input(
                "\nENTER EXISTING USERNAME(FORMAT: Limit - 16 Characters(Alphabet, Special Character only '@', Numbers are allowed), EX- 'Souvik@1996'): ")
            password = input(
                "\nENTER EXISTING PASSWORD(FORMAT: Limit - 8 Characters(Only Alphabet & Numbers), EX- 'Suvo1996'): ")

            if existing_user(username, password):
                break

            attempt -= 1
            print(f'YOU HAVE {attempt} ATTEMPTS REMAINING.')
        pass
    elif action == "3":
        pin = genaration_pin()
        print(f"OTP: {pin}")
        otp = input("\nENTER OTP TO RESET PASSWORD: ")
        if otp == pin:
            username = input("\nENTER YOUR USERNAME: ")
            password = input("ENTER YOUR NEW PASSWORD(FORMAT: Limit - 8 Characters(Only Alphabet & Numbers): ")
            try:
                cur_obj.execute("SELECT * FROM users WHERE password = %s", (password,))
                result = cur_obj.fetchall()
                if result:
                    print("THIS PASSWORD IS USED BEFORE")
                    break
                else:
                    print(" ")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                conn_obj.rollback()
            if len(password) <= 8:
                print(" ")
            else:
                print("NOT OK")
                break
            forgot_password(username, password)
        else:
            print("YOU HAVE ENTERED WRONG OTP")
        pass
    elif action == "4":
        print("LOGGED OUT")
        break
    else:
        print("INVALID OPTION.")

# Close the cursor and connection
conn_obj.close()
