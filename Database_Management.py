import mysql.connector
import streamlit as st
from streamlit_option_menu import option_menu

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="classicmodels"
)
mycursor=mydb.cursor()

def main():
    st.title("Database Management System")
    st.success("Connection Established")

    with st.sidebar:
        option = option_menu("Retrive System", ["Read","Create","Update","Delete","User Query"], 
            icons=['bi bi-book', 'bi bi-gear', "bi bi-pencil","bi bi-x", "bi bi-database-gear"], menu_icon="bi bi-coin", default_index=0)

    if option=="Read":
        st.subheader("Read Records")
        mycursor.execute("select * from customers")
        result = mycursor.fetchall()
        col_names = [i[0] for i in mycursor.description]
        st.table([col_names] + result)

    elif option=="Create":
        st.subheader("Create a Record")
        Customer_Number =st.text_input("Enter Customer Number")
        Customer_Name=st.text_input("Customer Name")
        contactLastName = st.text_input("Contact Last Name")
        contactFirstName = st.text_input("Contact First Name")
        phone = st.text_input("phone")
        addressline1 = st.text_input("Address Line 1")
        addressline2 = st.text_input("Address Line 2")
        city = st.text_input("City")
        state = st.text_input("State")
        postalcode = st.text_input("Postal Code")
        country = st.text_input("Country")
        salesRepEmployeeNumber = st.text_input("Sales Rep Employee Number")
        cred_limit = st.number_input("Credit Limit")
        
        if st.button("Create"):
            sql= "insert into customers(customerNumber, customerName, contactLastName, contactFirstName, phone, addressLine1, addessLine2, city, state, postalcode, country, salesRepEmployeeNumber, creditLimit) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %d)"
            val= (Customer_Number, Customer_Name, contactLastName, contactFirstName, phone, addressline1, addressline2, city, state, postalcode, country,salesRepEmployeeNumber, cred_limit)
            mycursor.execute(sql,val)
            mydb.commit()
            st.success("Record Created Successfully!!!")


    elif option=="Update":
        st.subheader("Update a Record")
        Customer_Number =st.text_input("Enter Customer Number")
        Customer_Name=st.text_input("Customer Name")
        contactLastName = st.text_input("Contact Last Name")
        contactFirstName = st.text_input("Contact First Name")
        phone = st.text_input("phone")
        addressline1 = st.text_input("Address Line 1")
        addressline2 = st.text_input("Address Line 2")
        city = st.text_input("City")
        state = st.text_input("State")
        postalcode = st.text_input("Postal Code")
        country = st.text_input("Country")
        salesRepEmployeeNumber = st.text_input("Sales Rep Employee Number")
        cred_limit = st.number_input("Credit Limit")

        if st.button("Update"):
            sql="update customers set customerNumber=%s customerName=%s contactLastName=%s contactFirstName=%s phone=%s addressLine1=%s addessLine2=%s city=%s state=%s postalcode=%s country=%s salesRepEmployeeNumber=%s creditLimit=%d"
            val= (Customer_Number, Customer_Name, contactLastName, contactFirstName, phone, addressline1, addressline2, city, state, postalcode, country,salesRepEmployeeNumber, cred_limit)
            mycursor.execute(sql,val)
            mydb.commit()
            st.success("Record Updated Successfully!!!")

    elif option=="Delete":
        st.subheader("Delete a Record")
        id=st.text_input("Enter Customer Number")
        if st.button("Delete"):
            sql="delete from customers where id = %s"
            val=(id,)
            mycursor.execute(sql,val)
            mydb.commit()
            st.success("Record Deleted Successfully!!!")

    elif option == "User Query":
        custom_query = st.text_input("Enter a SQL query:")
        if st.button("Execute Query"):
            mycursor.execute(custom_query)
            results = mycursor.fetchall()
            st.write("Query result:")

            if results:
                col_names = [i[0] for i in mycursor.description]
                st.table([col_names] + results)

if __name__ == "__main__":
    main()
