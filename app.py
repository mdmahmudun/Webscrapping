import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Function to get data from the website
def get_data(dept):
    webpage = requests.get(f"https://www.{dept}.ruet.ac.bd/teacher_list").text
    soup = BeautifulSoup(webpage, 'lxml')
    teachers = soup.find_all('tr')[1:]
    
    name_en = []
    designation = []
    phone_no = []
    email = []
    for i in teachers:
        name = i.find_all('td')[1].text.strip()
        desig = i.find_all('td')[3].text.strip()
        phone = i.find_all('td')[6].text.strip()
        em = i.find_all('td')[5].text.strip()
        name_en.append(name)
        designation.append(desig)
        phone_no.append(phone)
        email.append(em)
    data = pd.DataFrame({'Name': name_en,
                         'Designation': designation,
                         'Phone': phone_no,
                         'Email': email}) 
    return data

# Function to filter data based on selected designations
def filter_data(data, selected_designations):
    if 'All' in selected_designations:
        return data  
    else:
        filter_condition = data['Designation'].isin(selected_designations)
        return data[filter_condition].reset_index(drop=True)

# Streamlit app
def main():
    st.title("RUET Teacher's Information")

    # Department selection
    depts = ['EEE', 'CSE', 'ETE', 'ECE', 'CE', 'URP', 'ARCH', 'BECM', 'ME', 'IPE', 'GCE', 'MTE', 'MSE', 'CFPE', 'CHEM', 'MATH', 'PHY', 'HUM']
    dept = st.sidebar.selectbox('Select Department', depts).lower()

    if dept:
        data = get_data(dept)

        st.sidebar.write('### Select Designations')
        options = ['Professor', 'Associate Professor', 'Assistant Professor', 'Lecturer']
        selected_designations = [option for option in options if st.sidebar.checkbox(option)]

    if st.sidebar.button('Submit'):
        final_data = filter_data(data, selected_designations)

        st.write(final_data.style.set_properties(**{'max-width': '1000px'}))

if __name__ == '__main__':
    main()
