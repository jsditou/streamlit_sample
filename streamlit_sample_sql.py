import streamlit as st
import sqlite3

# データベースの接続とテーブルの作成


def init_db():
    conn = sqlite3.connect('employee.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            department TEXT
        )
    ''')
    conn.commit()
    conn.close()

# データベースに社員情報を登録する関数


def add_employee(name, age, department):
    conn = sqlite3.connect('employee.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO employees (name, age, department) VALUES (?, ?, ?)
    ''', (name, age, department))
    conn.commit()
    conn.close()

# 全社員情報を取得する関数


def get_all_employees():
    conn = sqlite3.connect('employee.db')
    c = conn.cursor()
    c.execute('SELECT * FROM employees')
    employees = c.fetchall()
    conn.close()
    return employees

# 特定の社員情報を取得する関数


def get_employee(employee_id):
    conn = sqlite3.connect('employee.db')
    c = conn.cursor()
    c.execute('SELECT * FROM employees WHERE id = ?', (employee_id,))
    employee = c.fetchone()
    conn.close()
    return employee

# 社員情報を更新する関数


def update_employee(employee_id, name, age, department):
    conn = sqlite3.connect('employee.db')
    c = conn.cursor()
    c.execute('''
        UPDATE employees
        SET name = ?, age = ?, department = ?
        WHERE id = ?
    ''', (name, age, department, employee_id))
    conn.commit()
    conn.close()

# 社員情報を削除する関数


def delete_employee(employee_id):
    conn = sqlite3.connect('employee.db')
    c = conn.cursor()
    c.execute('''
        DELETE FROM employees
        WHERE id = ?
    ''', (employee_id,))
    conn.commit()
    conn.close()

# Streamlitアプリケーション


def main():
    st.title("社員情報管理システム")

    # データベースの初期化
    init_db()

    menu = ["登録", "一覧表示", "更新", "削除"]
    choice = st.radio("メニュー", menu)

    if choice == "登録":
        st.subheader("社員情報の登録")
        name = st.text_input("名前")
        age = st.number_input("年齢", min_value=18, max_value=100, step=1)
        department = st.text_input("部署")
        if st.button("登録"):
            if name and department:
                add_employee(name, age, department)
                st.success("社員情報を登録しました！")
            else:
                st.error("すべてのフィールドを入力してください。")

    elif choice == "一覧表示":
        st.subheader("社員情報の一覧")
        employees = get_all_employees()
        for employee in employees:
            st.write(
                f"ID: {employee[0]}, 名前: {employee[1]}, 年齢: {employee[2]}, 部署: {employee[3]}")

    elif choice == "更新":
        st.subheader("社員情報の更新")
        employee_id = st.number_input("更新する社員のID", min_value=1, step=1)
        employee = get_employee(employee_id)
        if employee:
            name = st.text_input("名前", value=employee[1])
            age = st.number_input("年齢", min_value=18,
                                  max_value=100, step=1, value=employee[2])
            department = st.text_input("部署", value=employee[3])
            if st.button("更新"):
                update_employee(employee_id, name, age, department)
                st.success("社員情報を更新しました！")
        else:
            st.error("指定されたIDの社員が存在しません。")

    elif choice == "削除":
        st.subheader("社員情報の削除")
        employee_id = st.number_input("削除する社員のID", min_value=1, step=1)
        if st.button("削除"):
            delete_employee(employee_id)
            st.success("社員情報を削除しました！")


if __name__ == "__main__":
    main()
