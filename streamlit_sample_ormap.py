import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLAlchemyの設定
Base = declarative_base()


class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    department = Column(String)


# データベースの初期化
engine = create_engine('sqlite:///employee.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Streamlitアプリケーション


def main():
    st.title("社員情報管理システム")

    menu = ["登録", "一覧表示", "更新", "削除"]
    choice = st.radio("メニュー", menu)

    if choice == "登録":
        st.subheader("社員情報の登録")
        name = st.text_input("名前")
        age = st.number_input("年齢", min_value=18, max_value=100, step=1)
        department = st.text_input("部署")
        if st.button("登録"):
            if name and department:
                new_employee = Employee(
                    name=name, age=age, department=department)
                session.add(new_employee)
                session.commit()
                st.success("社員情報を登録しました！")
            else:
                st.error("すべてのフィールドを入力してください。")

    elif choice == "一覧表示":
        st.subheader("社員情報の一覧")
        employees = session.query(Employee).all()
        for employee in employees:
            st.write(
                f"ID: {employee.id}, 名前: {employee.name}, 年齢: {employee.age}, 部署: {employee.department}")

    elif choice == "更新":
        st.subheader("社員情報の更新")
        employee_id = st.number_input("更新する社員のID", min_value=1, step=1)
        employee = session.query(Employee).filter(
            Employee.id == employee_id).first()
        if employee:
            name = st.text_input("名前", value=employee.name)
            age = st.number_input("年齢", min_value=18,
                                  max_value=100, step=1, value=employee.age)
            department = st.text_input("部署", value=employee.department)
            if st.button("更新"):
                employee.name = name
                employee.age = age
                employee.department = department
                session.commit()
                st.success("社員情報を更新しました！")
        else:
            st.error("指定されたIDの社員が存在しません。")

    elif choice == "削除":
        st.subheader("社員情報の削除")
        employee_id = st.number_input("削除する社員のID", min_value=1, step=1)
        if st.button("削除"):
            employee = session.query(Employee).filter(
                Employee.id == employee_id).first()
            if employee:
                session.delete(employee)
                session.commit()
                st.success("社員情報を削除しました！")
            else:
                st.error("指定されたIDの社員が存在しません。")


if __name__ == "__main__":
    main()
