# import sqlite3
# import os
#
#
# def create_company_database(db_path):
#     # 创建存放数据库的目录（如果不存在）
#     db_dir = os.path.dirname(db_path)
#     if not os.path.exists(db_dir):
#         os.makedirs(db_dir)
#
#     # 连接数据库
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
#
#     try:
#         # 1. 创建部门表（基础表）
#         cursor.execute('''
#         CREATE TABLE IF NOT EXISTS departments (
#             dept_id INTEGER PRIMARY KEY AUTOINCREMENT,
#             dept_name TEXT NOT NULL UNIQUE,
#             location TEXT,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         )
#         ''')
#
#         # 2. 创建员工表（关联部门表）
#         cursor.execute('''
#         CREATE TABLE IF NOT EXISTS employees (
#             emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
#             emp_name TEXT NOT NULL,
#             position TEXT,
#             dept_id INTEGER,
#             hire_date DATE,
#             salary REAL,
#             FOREIGN KEY (dept_id) REFERENCES departments(dept_id) ON DELETE SET NULL
#         )
#         ''')
#
#         # 3. 创建客户表
#         cursor.execute('''
#         CREATE TABLE IF NOT EXISTS customers (
#             cust_id INTEGER PRIMARY KEY AUTOINCREMENT,
#             cust_name TEXT NOT NULL,
#             contact_person TEXT,
#             phone TEXT,
#             address TEXT,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         )
#         ''')
#
#         # 4. 创建订单表（关联员工表和客户表） # 4. 创建订单表（关联员工表和客户表）
#         cursor.execute('''
#         CREATE TABLE IF NOT EXISTS orders (
#             order_id INTEGER PRIMARY KEY AUTOINCREMENT,
#             order_date DATE NOT NULL,
#             cust_id INTEGER NOT NULL,
#             emp_id INTEGER,
#             total_amount REAL,
#             status TEXT DEFAULT 'pending',
#             FOREIGN KEY (cust_id) REFERENCES customers(cust_id) ON DELETE CASCADE,
#             FOREIGN KEY (emp_id) REFERENCES employees(emp_id) ON DELETE SET NULL
#         )
#         ''')
#
#         # 插入示例数据
#         # 插入部门数据
#         cursor.execute('''
#         INSERT OR IGNORE INTO departments (dept_name, location) VALUES
#         ('销售部', '北京'),
#         ('技术部', '上海'),
#         ('财务部', '广州')
#         ''')
#
#         # 插入员工数据
#         cursor.execute('''
#         INSERT OR IGNORE INTO employees (emp_name, position, dept_id, hire_date, salary) VALUES
#         ('赖斯', '销售经理', 1, '2020-01-15', 8000),
#         ('黑糖', '程序员', 2, '2021-03-20', 7500),
#         ('嘟嘟', '会计', 3, '2019-07-05', 6800)
#         ''')
#
#         # 插入客户数据
#         cursor.execute('''
#         INSERT OR IGNORE INTO customers (cust_name, contact_person, phone, address) VALUES
#         ('ABC公司', '赵六', '13800138000', '北京市朝阳区'),
#         ('XYZ企业', '钱七', '13900139000', '上海市浦东新区')
#         ''')
#
#         # 插入订单数据
#         cursor.execute('''
#         INSERT OR IGNORE INTO orders (order_date, cust_id, emp_id, total_amount, status) VALUES
#         ('2023-09-01', 1, 1, 25000.00, 'completed'),
#         ('2023-09-10', 2, 1, 15000.00, 'pending')
#         ''')
#
#         # 提交事务
#         conn.commit()
#         print(f"数据库创建成功，保存路径：{db_path}")
#
#     except sqlite3.Error as e:
#         print(f"数据库操作错误：{e}")
#         conn.rollback()
#     finally:
#         # 关闭连接
#         conn.close()
#
#
# if __name__ == "__main__":
#     db_file_path = r'./sqlite_set/company.db'
#     create_company_database(db_file_path)

import sqlite3
import os
from datetime import datetime


def create_enterprise_database(db_path):
    # 确保目录存在
    db_dir = os.path.dirname(db_path)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    # 连接数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # 启用外键约束
    cursor.execute("PRAGMA foreign_keys = ON")

    try:
        # 1. 基础配置表 - 公司信息
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS company_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            registration_code TEXT UNIQUE NOT NULL,
            address TEXT,
            contact_phone TEXT,
            business_scope TEXT,
            established_date DATE,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # 2. 部门表（扩展管理层级）
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            dept_id INTEGER PRIMARY KEY AUTOINCREMENT,
            dept_name TEXT NOT NULL,
            parent_dept_id INTEGER,
            manager_id INTEGER,
            location TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parent_dept_id) REFERENCES departments(dept_id) ON DELETE SET NULL,
            UNIQUE(dept_name, parent_dept_id)
        )
        ''')

        # 3. 角色与权限表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            role_id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT NOT NULL UNIQUE,
            permissions TEXT,  -- 存储权限标识，用逗号分隔
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # 4. 员工表（增强个人信息与权限关联）
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_no TEXT NOT NULL UNIQUE,  -- 员工编号
            emp_name TEXT NOT NULL,
            gender TEXT CHECK(gender IN ('男', '女', '其他')),
            birth_date DATE,
            position TEXT,
            dept_id INTEGER,
            role_id INTEGER,
            hire_date DATE NOT NULL,
            termination_date DATE,
            salary REAL NOT NULL,
            bank_account TEXT,
            id_card TEXT UNIQUE,
            phone TEXT,
            email TEXT UNIQUE,
            status TEXT CHECK(status IN ('在职', '离职', '休假')) DEFAULT '在职',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (dept_id) REFERENCES departments(dept_id) ON DELETE SET NULL,
            FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE SET NULL
        )
        ''')

        # 5. 客户表（细化分类与等级）
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            cust_id INTEGER PRIMARY KEY AUTOINCREMENT,
            cust_no TEXT NOT NULL UNIQUE,  -- 客户编号
            cust_name TEXT NOT NULL,
            cust_type TEXT CHECK(cust_type IN ('个人', '企业')),
            cust_level TEXT CHECK(cust_level IN ('VIP', '普通', '潜在')),
            contact_person TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            tax_id TEXT UNIQUE,
            payment_terms TEXT,  -- 付款条件
            credit_limit REAL,  -- 信用额度
            sales_id INTEGER,  -- 专属销售
            created_by INTEGER,  -- 创建人
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sales_id) REFERENCES employees(emp_id) ON DELETE SET NULL,
            FOREIGN KEY (created_by) REFERENCES employees(emp_id) ON DELETE SET NULL
        )
        ''')

        # 6. 供应商表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            supp_id INTEGER PRIMARY KEY AUTOINCREMENT,
            supp_no TEXT NOT NULL UNIQUE,  -- 供应商编号
            supp_name TEXT NOT NULL,
            contact_person TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            tax_id TEXT UNIQUE,
            bank_info TEXT,
            qualification TEXT,  -- 资质状态
            rating REAL,  -- 评级
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES employees(emp_id) ON DELETE SET NULL
        )
        ''')

        # 7. 产品表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            prod_id INTEGER PRIMARY KEY AUTOINCREMENT,
            prod_no TEXT NOT NULL UNIQUE,  -- 产品编号
            prod_name TEXT NOT NULL,
            category TEXT,
            specification TEXT,  -- 规格
            unit TEXT,  -- 单位
            purchase_price REAL,  -- 采购价
            selling_price REAL,  -- 售价
            tax_rate REAL,  -- 税率
            min_stock INTEGER,  -- 最低库存
            status TEXT CHECK(status IN ('在售', '下架', '停产')) DEFAULT '在售',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # 8. 库存表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            inv_id INTEGER PRIMARY KEY AUTOINCREMENT,
            prod_id INTEGER NOT NULL,
            warehouse TEXT,  -- 仓库位置
            quantity INTEGER NOT NULL DEFAULT 0,
            last_check_date DATE,  -- 最后盘点日期
            FOREIGN KEY (prod_id) REFERENCES products(prod_id) ON DELETE CASCADE,
            UNIQUE(prod_id, warehouse)
        )
        ''')

        # 9. 订单表（增强订单明细关联）
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_no TEXT NOT NULL UNIQUE,  -- 订单编号
            order_date DATE NOT NULL,
            cust_id INTEGER NOT NULL,
            emp_id INTEGER,  -- 经手人
            total_amount REAL NOT NULL,
            tax_amount REAL,
            discount REAL DEFAULT 0,
            payment_status TEXT CHECK(payment_status IN ('未付', '部分', '已付')),
            delivery_status TEXT CHECK(delivery_status IN ('未发', '部分', '已发')),
            remarks TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cust_id) REFERENCES customers(cust_id) ON DELETE CASCADE,
            FOREIGN KEY (emp_id) REFERENCES employees(emp_id) ON DELETE SET NULL
        )
        ''')

        # 10. 订单明细表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            prod_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total_price REAL NOT NULL,
            delivery_quantity INTEGER DEFAULT 0,
            FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
            FOREIGN KEY (prod_id) REFERENCES products(prod_id) ON DELETE CASCADE,
            UNIQUE(order_id, prod_id)
        )
        ''')

        # 11. 采购表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchases (
            purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
            purchase_no TEXT NOT NULL UNIQUE,  -- 采购编号
            purchase_date DATE NOT NULL,
            supp_id INTEGER NOT NULL,
            emp_id INTEGER,  -- 采购人
            total_amount REAL NOT NULL,
            status TEXT CHECK(status IN ('草稿', '已确认', '已收货', '已付款', '取消')),
            remarks TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (supp_id) REFERENCES suppliers(supp_id) ON DELETE CASCADE,
            FOREIGN KEY (emp_id) REFERENCES employees(emp_id) ON DELETE SET NULL
        )
        ''')

        # 插入基础数据
        # 公司信息
        cursor.execute('''
        INSERT OR IGNORE INTO company_info (company_name, registration_code, address, contact_phone, established_date)
        VALUES ('示例科技有限公司', '91110101XXXXXXXXXX', '北京市海淀区XX路XX号', '010-12345678', '2010-05-18')
        ''')

        # 角色数据
        cursor.execute('''
        INSERT OR IGNORE INTO roles (role_name, permissions, description) VALUES
        ('管理员', 'all', '系统全部权限'),
        ('销售', 'customer,order,report_sales', '客户管理、订单管理、销售报表'),
        ('采购', 'supplier,purchase,inventory', '供应商、采购、库存管理')
        ''')

        # 部门数据（含层级关系）
        cursor.execute('''
        INSERT OR IGNORE INTO departments (dept_name, parent_dept_id, location) VALUES
        ('总经办', NULL, '北京总部'),
        ('销售部', 1, '北京总部'),
        ('采购部', 1, '北京总部'),
        ('技术部', 1, '上海分部')
        ''')

        # 提交事务
        conn.commit()
        print(f"企业级数据库创建成功，保存路径：{db_path}")

    except sqlite3.Error as e:
        print(f"数据库操作错误：{e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    db_file_path = r'./sqlite_set/enterprise.db'
    create_enterprise_database(db_file_path)