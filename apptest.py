import os
import sqlite3
import streamlit as st

# 获取当前脚本所在目录，并将数据库文件路径设置为相对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'inventory_management.db')


# 第一部分初始化数据库和创建所有表格 Initialize SQLite database and create tables
def initialize_database():
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()

    # Create Products table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        category TEXT NOT NULL,
        image BLOB
    )
    ''')

    # Create Stock table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stock (
        stock_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        location TEXT NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
    ''')

    # Create Orders table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_type TEXT NOT NULL,  -- 'purchase' or 'sale'
        order_date TEXT NOT NULL,
        customer_or_supplier_id INTEGER NOT NULL,  -- ID of either customer or supplier
        total_amount REAL NOT NULL
    )
    ''')

    # Create Suppliers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS suppliers (
        supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact_name TEXT,
        phone_number TEXT,
        address TEXT
    )
    ''')

    # Create Customers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone_number TEXT,
        address TEXT
    )
    ''')

    conn.commit()
    conn.close()

# Call the function to initialize the database
initialize_database()

print("Database initialized successfully.")


# 第二部分 创建所有表格的增删改查功能
# 1.商品表
# Add a new product
def add_product(name, description, price, category, image=None):
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO products (name, description, price, category, image)
    VALUES (?, ?, ?, ?, ?)
    ''', (name, description, price, category, image))
    conn.commit()
    conn.close()
    print(f"Product '{name}' added successfully.")

# Get all products
def get_all_products():
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return products

# Update a product
def update_product(product_id, name, description, price, category, image=None):
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE products SET name=?, description=?, price=?, category=?, image=?
    WHERE product_id=?
    ''', (name, description, price, category, image, product_id))
    conn.commit()
    conn.close()
    print(f"Product ID {product_id} updated successfully.")

# Delete a product
def delete_product(product_id):
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE product_id=?', (product_id,))
    conn.commit()
    conn.close()
    print(f"Product ID {product_id} deleted successfully.")

# 2.库存表
# Add stock entry
def add_stock(product_id, quantity, location):
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO stock (product_id, quantity, location)
    VALUES (?, ?, ?)
    ''', (product_id, quantity, location))
    conn.commit()
    conn.close()
    print(f"Stock for Product ID {product_id} added successfully.")

# Get all stock entries
def get_all_stock():
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM stock')
    stock = cursor.fetchall()
    conn.close()
    return stock

# Update stock entry
def update_stock(stock_id, product_id, quantity, location):
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE stock SET product_id=?, quantity=?, location=?
    WHERE stock_id=?
    ''', (product_id, quantity, location, stock_id))
    conn.commit()
    conn.close()
    print(f"Stock ID {stock_id} updated successfully.")

# Delete stock entry
def delete_stock(stock_id):
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM stock WHERE stock_id=?', (stock_id,))
    conn.commit()
    conn.close()
    print(f"Stock ID {stock_id} deleted successfully.")

# 3.订单表
# Add an order
def add_order(order_type, order_date, customer_or_supplier_id, total_amount):
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO orders (order_type, order_date, customer_or_supplier_id, total_amount)
    VALUES (?, ?, ?, ?)
    ''', (order_type, order_date, customer_or_supplier_id, total_amount))
    conn.commit()
    conn.close()
    print(f"Order added successfully.")

# Get all orders
def get_all_orders():
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders')
    orders = cursor.fetchall()
    conn.close()
    return orders

# Update an order
def update_order(order_id, order_type, order_date, customer_or_supplier_id, total_amount):
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE orders SET order_type=?, order_date=?, customer_or_supplier_id=?, total_amount=?
    WHERE order_id=?
    ''', (order_type, order_date, customer_or_supplier_id, total_amount, order_id))
    conn.commit()
    conn.close()
    print(f"Order ID {order_id} updated successfully.")

# Delete an order
def delete_order(order_id):
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM orders WHERE order_id=?', (order_id,))
    conn.commit()
    conn.close()
    print(f"Order ID {order_id} deleted successfully.")

# 4.供应商表
# Add a supplier
def add_supplier(name, contact_name, phone_number, address):
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO suppliers (name, contact_name, phone_number, address)
    VALUES (?, ?, ?, ?)
    ''', (name, contact_name, phone_number, address))
    conn.commit()
    conn.close()
    print(f"Supplier '{name}' added successfully.")

# Get all suppliers
def get_all_suppliers():
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM suppliers')
    suppliers = cursor.fetchall()
    conn.close()
    return suppliers

# Update a supplier
def update_supplier(supplier_id, name, contact_name, phone_number, address):
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE suppliers SET name=?, contact_name=?, phone_number=?, address=?
    WHERE supplier_id=?
    ''', (name, contact_name, phone_number, address, supplier_id))
    conn.commit()
    conn.close()
    print(f"Supplier ID {supplier_id} updated successfully.")

# Delete a supplier
def delete_supplier(supplier_id):
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM suppliers WHERE supplier_id=?', (supplier_id,))
    conn.commit()
    conn.close()
    print(f"Supplier ID {supplier_id} deleted successfully.")

# 5.客户表
# Add a customer
def add_customer(name, phone_number, address):
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO customers (name, phone_number, address)
    VALUES (?, ?, ?)
    ''', (name, phone_number, address))
    conn.commit()
    conn.close()
    print(f"Customer '{name}' added successfully.")

# Get all customers
def get_all_customers():
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customers')
    customers = cursor.fetchall()
    conn.close()
    return customers

# Update a customer
def update_customer(customer_id, name, phone_number, address):
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE customers SET name=?, phone_number=?, address=?
    WHERE customer_id=?
    ''', (name, phone_number, address, customer_id))
    conn.commit()
    conn.close()
    print(f"Customer ID {customer_id} updated successfully.")

# Delete a customer
def delete_customer(customer_id):
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM customers WHERE customer_id=?', (customer_id,))
    conn.commit()
    conn.close()
    print(f"Customer ID {customer_id} deleted successfully.")

# 第三部分 交互逻辑区
# Streamlit Interface
# 商品页面
def manage_products():
    st.title("Product Management")
    action = st.selectbox("Choose an action", ["View Products", "Add Product", "Update Product", "Delete Product"])

    if action == "View Products":
        products = get_all_products()
        st.table(products)
    elif action == "Add Product":
        name = st.text_input("Name")
        description = st.text_input("Description")
        price = st.number_input("Price")
        category = st.text_input("Category")
        if st.button("Add Product"):
            add_product(name, description, price, category)
            st.success(f"Product '{name}' added successfully.")
    elif action == "Update Product":
        product_id = st.number_input("Product ID", min_value=1)
        name = st.text_input("Name")
        description = st.text_input("Description")
        price = st.number_input("Price")
        category = st.text_input("Category")
        if st.button("Update Product"):
            update_product(product_id, name, description, price, category)
            st.success(f"Product ID {product_id} updated successfully.")
    elif action == "Delete Product":
        product_id = st.number_input("Product ID", min_value=1)
        if st.button("Delete Product"):
            delete_product(product_id)
            st.success(f"Product ID {product_id} deleted successfully.")

# 库存页面
def manage_stock():
    st.title("Stock Management")
    action = st.selectbox("Choose an action", ["View Stock", "Add Stock", "Update Stock", "Delete Stock"])

    if action == "View Stock":
        stock = get_all_stock()
        st.table(stock)
    elif action == "Add Stock":
        product_id = st.number_input("Product ID", min_value=1)
        quantity = st.number_input("Quantity", min_value=1)
        location = st.text_input("Location")
        if st.button("Add Stock"):
            add_stock(product_id, quantity, location)
            st.success(f"Stock for Product ID {product_id} added successfully.")
    elif action == "Update Stock":
        stock_id = st.number_input("Stock ID", min_value=1)
        product_id = st.number_input("Product ID", min_value=1)
        quantity = st.number_input("Quantity", min_value=1)
        location = st.text_input("Location")
        if st.button("Update Stock"):
            update_stock(stock_id, product_id, quantity, location)
            st.success(f"Stock ID {stock_id} updated successfully.")
    elif action == "Delete Stock":
        stock_id = st.number_input("Stock ID", min_value=1)
        if st.button("Delete Stock"):
            delete_stock(stock_id)
            st.success(f"Stock ID {stock_id} deleted successfully.")

# 订单页面
def manage_orders():
    st.title("Order Management")
    action = st.selectbox("Choose an action", ["View Orders", "Add Order", "Update Order", "Delete Order"])

    if action == "View Orders":
        orders = get_all_orders()
        st.table(orders)
    elif action == "Add Order":
        order_type = st.selectbox("Order Type", ["purchase", "sale"])
        order_date = st.date_input("Order Date")
        customer_or_supplier_id = st.number_input("Customer/Supplier ID", min_value=1)
        total_amount = st.number_input("Total Amount", min_value=0.0)
        if st.button("Add Order"):
            add_order(order_type, str(order_date), customer_or_supplier_id, total_amount)
            st.success(f"Order added successfully.")
    elif action == "Update Order":
        order_id = st.number_input("Order ID", min_value=1)
        order_type = st.selectbox("Order Type", ["purchase", "sale"])
        order_date = st.date_input("Order Date")
        customer_or_supplier_id = st.number_input("Customer/Supplier ID", min_value=1)
        total_amount = st.number_input("Total Amount", min_value=0.0)
        if st.button("Update Order"):
            update_order(order_id, order_type, str(order_date), customer_or_supplier_id, total_amount)
            st.success(f"Order ID {order_id} updated successfully.")
    elif action == "Delete Order":
        order_id = st.number_input("Order ID", min_value=1)
        if st.button("Delete Order"):
            delete_order(order_id)
            st.success(f"Order ID {order_id} deleted successfully.")

# 供应商页面
def manage_suppliers():
    st.title("Supplier Management")
    action = st.selectbox("Choose an action", ["View Suppliers", "Add Supplier", "Update Supplier", "Delete Supplier"])

    if action == "View Suppliers":
        suppliers = get_all_suppliers()
        st.table(suppliers)
    elif action == "Add Supplier":
        name = st.text_input("Supplier Name")
        contact_name = st.text_input("Contact Name")
        phone_number = st.text_input("Phone Number")
        address = st.text_input("Address")
        if st.button("Add Supplier"):
            add_supplier(name, contact_name, phone_number, address)
            st.success(f"Supplier '{name}' added successfully.")
    elif action == "Update Supplier":
        supplier_id = st.number_input("Supplier ID", min_value=1)
        name = st.text_input("Supplier Name")
        contact_name = st.text_input("Contact Name")
        phone_number = st.text_input("Phone Number")
        address = st.text_input("Address")
        if st.button("Update Supplier"):
            update_supplier(supplier_id, name, contact_name, phone_number, address)
            st.success(f"Supplier ID {supplier_id} updated successfully.")
    elif action == "Delete Supplier":
        supplier_id = st.number_input("Supplier ID", min_value=1)
        if st.button("Delete Supplier"):
            delete_supplier(supplier_id)
            st.success(f"Supplier ID {supplier_id} deleted successfully.")

# 客户页面
def manage_customers():
    st.title("Customer Management")
    action = st.selectbox("Choose an action", ["View Customers", "Add Customer", "Update Customer", "Delete Customer"])

    if action == "View Customers":
        customers = get_all_customers()
        st.table(customers)
    elif action == "Add Customer":
        name = st.text_input("Customer Name")
        phone_number = st.text_input("Phone Number")
        address = st.text_input("Address")
        if st.button("Add Customer"):
            add_customer(name, phone_number, address)
            st.success(f"Customer '{name}' added successfully.")
    elif action == "Update Customer":
        customer_id = st.number_input("Customer ID", min_value=1)
        name = st.text_input("Customer Name")
        phone_number = st.text_input("Phone Number")
        address = st.text_input("Address")
        if st.button("Update Customer"):
            update_customer(customer_id, name, phone_number, address)
            st.success(f"Customer ID {customer_id} updated successfully.")
    elif action == "Delete Customer":
        customer_id = st.number_input("Customer ID", min_value=1)
        if st.button("Delete Customer"):
            delete_customer(customer_id)
            st.success(f"Customer ID {customer_id} deleted successfully.")

# 调用数据库初始化
initialize_database()

# 主页面
def main():
    st.sidebar.title("Inventory Management System")
    menu = ["Products", "Stock", "Orders", "Suppliers", "Customers"]
    choice = st.sidebar.selectbox("Select Section", menu)

    # 根据选择展示不同页面
    if choice == "Products":
        manage_products()
    elif choice == "Stock":
        manage_stock()
    elif choice == "Orders":
        manage_orders()
    elif choice == "Suppliers":
        manage_suppliers()
    elif choice == "Customers":
        manage_customers()


if __name__ == "__main__":
    main()