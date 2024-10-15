import os
import sqlite3
import streamlit as st
import pandas as pd

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

    # 创建订单详情表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_details (
        detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
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

# get_all_products 函数
def get_all_products():
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT product_id, name, description, price, category FROM products')
    data = cursor.fetchall()
    conn.close()

    # 创建一个带有列名的 DataFrame
    columns = ['商品ID', '商品名称', '商品描述', '价格', '分类']
    df = pd.DataFrame(data, columns=columns)
    return df

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
    cursor.execute('SELECT stock_id, product_id, quantity, location FROM stock')
    data = cursor.fetchall()
    conn.close()

    # 创建一个带有列名的 DataFrame
    columns = ['库存ID', '商品ID', '数量', '库存位置']
    df = pd.DataFrame(data, columns=columns)
    return df

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
    cursor.execute('SELECT order_id, order_type, order_date, customer_or_supplier_id, total_amount FROM orders')
    data = cursor.fetchall()
    conn.close()

    # 创建一个带有列名的 DataFrame
    columns = ['订单ID', '订单类型', '订单日期', '客户/供应商ID', '总金额']
    df = pd.DataFrame(data, columns=columns)
    return df

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
    cursor.execute('SELECT supplier_id, name, contact_name, phone_number, address FROM suppliers')
    data = cursor.fetchall()
    conn.close()

    # 创建一个带有列名的 DataFrame
    columns = ['供应商ID', '供应商名称', '联系人姓名', '联系电话', '地址']
    df = pd.DataFrame(data, columns=columns)
    return df

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
    cursor.execute('SELECT customer_id, name, phone_number, address FROM customers')
    data = cursor.fetchall()
    conn.close()

    # 创建一个带有列名的 DataFrame
    columns = ['客户ID', '客户名称', '联系电话', '地址']
    df = pd.DataFrame(data, columns=columns)
    return df

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

# 订单详情表
# 添加订单详情
def add_order_details(order_id, product_id, quantity, price):
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO orderdetails (order_id, product_id, quantity, price)
    VALUES (?, ?, ?, ?)
    ''', (order_id, product_id, quantity, price))
    conn.commit()
    conn.close()

# 获取所有订单详情
def get_all_order_details(order_id):
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orderdetails WHERE order_id=?', (order_id,))
    order_details = cursor.fetchall()
    conn.close()
    return order_details




# 第三部分 交互逻辑区
# Streamlit Interface
# 商品页面
def manage_products():
    st.title("商品管理")
    action = st.selectbox("选择操作", ["查看商品", "添加商品", "更新商品", "删除商品"])

    if action == "查看商品":
        products = get_all_products()
        st.table(products)  # 显示带有列名的商品表格
    elif action == "添加商品":
        name = st.text_input("商品名称")
        description = st.text_input("商品描述")
        price = st.number_input("价格")
        category = st.text_input("类别")
        if st.button("添加商品"):
            add_product(name, description, price, category)
            st.success(f"商品 '{name}' 添加成功。")
    elif action == "更新商品":
        product_id = st.number_input("商品 ID", min_value=1)
        name = st.text_input("商品名称")
        description = st.text_input("商品描述")
        price = st.number_input("价格")
        category = st.text_input("类别")
        if st.button("更新商品"):
            update_product(product_id, name, description, price, category)
            st.success(f"商品 ID {product_id} 更新成功。")
    elif action == "删除商品":
        product_id = st.number_input("商品 ID", min_value=1)
        if st.button("删除商品"):
            delete_product(product_id)
            st.success(f"商品 ID {product_id} 删除成功。")
 

# 库存页面
def manage_stock():
    st.title("库存管理")
    action = st.selectbox("选择操作", ["查看库存", "添加库存", "更新库存", "删除库存"])

    if action == "查看库存":
        stock = get_all_stock()
        st.table(stock)
    elif action == "添加库存":
        product_id = st.number_input("商品 ID", min_value=1)
        quantity = st.number_input("库存数量", min_value=1)
        location = st.text_input("库存位置")
        if st.button("添加库存"):
            add_stock(product_id, quantity, location)
            st.success(f"商品 ID {product_id} 的库存已成功添加。")
    elif action == "更新库存":
        stock_id = st.number_input("库存 ID", min_value=1)
        product_id = st.number_input("商品 ID", min_value=1)
        quantity = st.number_input("库存数量", min_value=1)
        location = st.text_input("库存位置")
        if st.button("更新库存"):
            update_stock(stock_id, product_id, quantity, location)
            st.success(f"库存 ID {stock_id} 已成功更新。")
    elif action == "删除库存":
        stock_id = st.number_input("库存 ID", min_value=1)
        if st.button("删除库存"):
            delete_stock(stock_id)
            st.success(f"库存 ID {stock_id} 已成功删除。")


# 订单管理页面
def manage_orders():
    st.title("订单管理")
    action = st.selectbox("选择操作", ["查看订单", "添加订单", "更新订单", "删除订单"])

    if action == "查看订单":
        orders = get_all_orders()
        st.table(orders)
    elif action == "添加订单":
        order_type = st.selectbox("订单类型", ["采购", "销售"])
        order_date = st.date_input("订单日期")
        customer_or_supplier_id = st.number_input("客户/供应商ID", min_value=1)
        total_amount = st.number_input("订单总金额", min_value=0.0)

        if st.button("添加订单"):
            # 首先添加订单
            order_id = add_order(order_type, str(order_date), customer_or_supplier_id, total_amount)
            st.success(f"订单添加成功，订单ID为: {order_id}")

            # 跳转到订单详情页面进行操作
            manage_order_details(order_id)
    elif action == "更新订单":
        order_id = st.number_input("订单ID", min_value=1)
        order_type = st.selectbox("订单类型", ["采购", "销售"])
        order_date = st.date_input("订单日期")
        customer_or_supplier_id = st.number_input("客户/供应商ID", min_value=1)
        total_amount = st.number_input("订单总金额", min_value=0.0)
        if st.button("更新订单"):
            update_order(order_id, order_type, str(order_date), customer_or_supplier_id, total_amount)
            st.success(f"订单 ID {order_id} 更新成功。")
    elif action == "删除订单":
        order_id = st.number_input("订单ID", min_value=1)
        if st.button("删除订单"):
            delete_order(order_id)
            st.success(f"订单 ID {order_id} 删除成功。")

### 2. 修改后的订单详情页面代码：
# 订单详情页面
def manage_order_details(order_id):
    st.subheader(f"订单详情 (订单ID: {order_id})")

    # 初始化商品列表，确保每次操作时不会重置
    if "product_list" not in st.session_state:
        st.session_state.product_list = []  # 初始为空商品列表

    # 显示当前的商品列表
    if st.session_state.product_list:
        st.write("当前商品列表:")
        for idx, product in enumerate(st.session_state.product_list):
            st.write(f"商品 {idx + 1}: 商品ID={product['product_id']}, 数量={product['quantity']}, 单价={product['price']}")

    # 商品输入表单
    st.write("添加商品:")
    product_id = st.number_input("商品ID", min_value=1, key="product_id_input")
    quantity = st.number_input("数量", min_value=1, key="quantity_input")
    price = st.number_input("单价", min_value=0.0, key="price_input")

    # 点击 "新增商品" 按钮后，商品被添加到列表中
    if st.button("新增商品"):
        new_product = {
            "product_id": product_id,
            "quantity": quantity,
            "price": price
        }
        st.session_state.product_list.append(new_product)  # 将商品添加到 session_state 列表中
        st.success(f"商品ID {product_id} 已添加到订单详情。")

    # 提交订单详情
    if st.button("提交订单详情"):
        if st.session_state.product_list:
            for product in st.session_state.product_list:
                add_order_details(order_id, product["product_id"], product["quantity"], product["price"])
            st.success(f"订单详情已成功添加到订单 ID {order_id}。")
            
            # 清空商品列表以便下次添加
            st.session_state.product_list = []
        else:
            st.error("请先添加至少一个商品再提交订单详情。")


# 供应商管理页面
def manage_suppliers():
    st.title("供应商管理")
    action = st.selectbox("选择操作", ["查看供应商", "添加供应商", "更新供应商", "删除供应商"])

    if action == "查看供应商":
        suppliers = get_all_suppliers()
        st.table(suppliers)
    elif action == "添加供应商":
        name = st.text_input("供应商名称")
        contact_name = st.text_input("联系人姓名")
        phone_number = st.text_input("联系电话")
        address = st.text_input("地址")
        if st.button("添加供应商"):
            add_supplier(name, contact_name, phone_number, address)
            st.success(f"供应商 '{name}' 添加成功。")
    elif action == "更新供应商":
        supplier_id = st.number_input("供应商 ID", min_value=1)
        name = st.text_input("供应商名称")
        contact_name = st.text_input("联系人姓名")
        phone_number = st.text_input("联系电话")
        address = st.text_input("地址")
        if st.button("更新供应商"):
            update_supplier(supplier_id, name, contact_name, phone_number, address)
            st.success(f"供应商 ID {supplier_id} 更新成功。")
    elif action == "删除供应商":
        supplier_id = st.number_input("供应商 ID", min_value=1)
        if st.button("删除供应商"):
            delete_supplier(supplier_id)
            st.success(f"供应商 ID {supplier_id} 删除成功。")


# 客户管理页面
def manage_customers():
    st.title("客户管理")
    action = st.selectbox("选择操作", ["查看客户", "添加客户", "更新客户", "删除客户"])

    if action == "查看客户":
        customers = get_all_customers()
        st.table(customers)
    elif action == "添加客户":
        name = st.text_input("客户名称")
        phone_number = st.text_input("联系电话")
        address = st.text_input("地址")
        if st.button("添加客户"):
            add_customer(name, phone_number, address)
            st.success(f"客户 '{name}' 添加成功。")
    elif action == "更新客户":
        customer_id = st.number_input("客户 ID", min_value=1)
        name = st.text_input("客户名称")
        phone_number = st.text_input("联系电话")
        address = st.text_input("地址")
        if st.button("更新客户"):
            update_customer(customer_id, name, phone_number, address)
            st.success(f"客户 ID {customer_id} 更新成功。")
    elif action == "删除客户":
        customer_id = st.number_input("客户 ID", min_value=1)
        if st.button("删除客户"):
            delete_customer(customer_id)
            st.success(f"客户 ID {customer_id} 删除成功。")


# 调用数据库初始化
initialize_database()

# 主页面
def main():
    st.sidebar.title("库存管理系统")  # 修改为中文标题
    menu = ["商品管理", "库存管理", "订单管理", "供应商管理", "客户管理"]  # 修改菜单为中文
    choice = st.sidebar.selectbox("选择功能", menu)  # 修改选择框提示为中文

    # 根据选择展示不同页面
    if choice == "商品管理":
        manage_products()
    elif choice == "库存管理":
        manage_stock()
    elif choice == "订单管理":
        manage_orders()
    elif choice == "供应商管理":
        manage_suppliers()
    elif choice == "客户管理":
        manage_customers()


if __name__ == "__main__":
    main()


