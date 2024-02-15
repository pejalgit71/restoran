import streamlit as st
st.set_page_config(layout="wide")

import pandas as pd
from datetime import datetime
import warnings
import os, fnmatch
from PIL import Image
import glob
cwd = os.getcwd() 
st.write("Current working directory:", cwd) 

# file = []
# file = fnmatch.filter(os.listdir(cwd+"/pages/images"), '*.png')
# st.write(file)
# # images = glob.glob("/Users/xstream/pages/images/")
# totalimage = len(file)
# index= st.number_input('Index', min_value=0)

# if st.button('Next'):
#     index+=1
#     st.write(index)
    
# if st.button('Prev'):
#     if index > 0:
#         index = index -1
#         st.write(index)
        
# image = Image.open(cwd+"/pages/images/"+file[index])
# st.write(cwd+"/pages/images/"+file[index])
# st.image(image, use_column_width=True)


warnings.filterwarnings("ignore")


# st.set_page_config(
# #     page_title="Menu Restoran Xstream",
# #     page_icon="🧊",
#     layout="wide",
# #     initial_sidebar_state="expanded",
#     )
# Function to calculate total order
    
def calculate_total_order(order_list, menu_df):
    total = 0
    item_totals = []
    for item, quantity in order_list.items():
        price = menu_df.loc[menu_df['Item'] == item, 'Price'].values[0]
        item_total = price * quantity
        total += item_total
        item_totals.append((item, item_total))
    return total, item_totals

# Function to save order to CSV
def save_to_csv(order_list, total, item_totals):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # order_df = pd.DataFrame(list(order_list.items()), columns=['Item', 'Quantity'])
    # order_df['Total'] = order_df['Item'].apply(lambda x: menu_df.loc[menu_df['Item'] == x, 'Price'].values[0])
    # order_df.to_csv(f'order_{timestamp}.csv', index=False)

    # item_totals_df = pd.DataFrame(item_totals, columns=['Item', 'Item Total'])
    dfmerge = pd.DataFrame
    dftotal,dfitem = report_sales(order_list, total_order, item_totals)
    dfmerge = dfmerge.merge(dfitem, dftotal)
    dfmerge.to_csv(f'sales_report_{timestamp}.csv', index=False)
    filename = "item_totals_"+timestamp+".csv"
    return filename
    
def report_sales(order_list, total, item_totals):
    order_df = pd.DataFrame(list(order_list.items()), columns=['Item', 'Quantity'])
    order_df['Price'] = order_df['Item'].apply(lambda x: menu_df.loc[menu_df['Item'] == x, 'Price'].values[0])
    item_totals_df = pd.DataFrame(item_totals, columns=['Item', 'Item Total'])
    return item_totals_df, order_df
    
# Load menu data from CSV
st.sidebar.title("Restoran Meracau")

menu_df = pd.read_csv("menu.csv")
menu_df = menu_df.reset_index(drop=True)
menu_df.index = menu_df.index+1
TableNo=0

formside = st.sidebar.form("side_form")
choose = formside.radio("pilih menu",["Order","Chef", "Admin"], index=None)
formside.form_submit_button("Submit")

if (choose == "Order"):
    st.title("Restaurant Menu Display and Order System")
    st.image("menu_food.png")
    col1, col2, col3= st.columns(3)
    # Display menu
    col1.subheader("Menu")
    col2.subheader("Place Your Order")
    col3.subheader("Table No Information")

    TableNo = col2.number_input(f"Table No", min_value=1, max_value=9 )
    menu_df['Quantity'] = menu_df.apply(lambda x: col2.number_input(f"Quantity of {x['Item']}", min_value=0, max_value=10, key=x['Item']), axis=1)
    menu_display_df = menu_df.drop(columns=['Quantity'])  # Exclude the Quantity column from display
    menu_display_df = menu_display_df.rename(columns={'Price': 'Price (RM)'})
    col1.write(menu_display_df[["Item","Price (RM)"]])
    # col1.write(menu_df[["Item","Quantity"]])
    # Order section

    # Create order dictionary
    order_list = {}
    for index, row in menu_df.iterrows():
        quantity = row['Quantity']
        if quantity > 0:
            order_list[row['Item']] = quantity

    # Calculate total order and item totals
    total_order, item_totals = calculate_total_order(order_list, menu_df)

    # Display item totals
    # col1.subheader("Item-wise Totals")
    # for item, item_total in item_totals:
    #     col1.write(f"{item}: RM{item_total:.2f}")

    # Display grand total
    # col1.subheader("Grand Total")
    # col1.write(f"Total Order Amount: RM{total_order:.2f}")

    # Save to CSV button
   
    with st.expander("Reports"):
        # Total Sales Report
        dfmerge = pd.DataFrame
        col1.subheader("Total Order")
        col1.write("This section will display the total sales report.")
        dftotal,dfitem = report_sales(order_list, total_order, item_totals)
        dfmerge = dfmerge.merge(dfitem, dftotal)
        dfmerge.index = dfmerge.index+1
        col1.write(dfmerge)
        col1.write(f"Total Order Amount: RM{total_order:.2f}")

        
        # st.write(dfitem)
    if col1.button("Save/Submit Order"):
        timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
        dfmerge = pd.DataFrame
        dftotal,dfitem = report_sales(order_list, total_order, item_totals)
        dfmerge = dfmerge.merge(dfitem, dftotal)
        dfmerge.to_csv(f'sales_order_{TableNo}_{timestamp}.csv', index=False)
        st.success("Order saved and submit successfully!")

    #Display Current Order
    cwd = os.getcwd()
    print (cwd)
    file = []
    file = fnmatch.filter(os.listdir(cwd), 'sales_chef*.csv')
    for order in file:
        tableno = order[11]
        orderdf = pd.read_csv(order)
        orderdf = orderdf.reset_index(drop=True)
        orderdf.index = orderdf.index+1
        col3.subheader(":green[Meja No "+tableno+", order sedang dihantar]")
        col3.write(orderdf[["Item", "Quantity","Item Total"]])
    # video_file = open('https://youtu.be/Wh66ThpxvI4?si=_2OuZ_t5UBuT3CIC', 'rb')
    # video_bytes = video_file.read()
    col3.video('https://youtu.be/Wh66ThpxvI4?si=_2OuZ_t5UBuT3CIC')
    
elif (choose == "Admin"):
    st.title("Admin Page")
    file = []
    file = fnmatch.filter(os.listdir(cwd), 'sales_chef*.csv')
    for order in file:
        tableno = order[11]
        orderdf = pd.read_csv(order)
        orderdf = orderdf.reset_index(drop=True)
        orderdf.index = orderdf.index+1
        orderdf["Rating"]= 5
        st.data_editor(
            orderdf[["Item", "Quantity", "Price", "Item Total", "Rating"]], column_config={
                "Rating": st.column_config.NumberColumn(
                    "Your rating",
                    help="Rating Star (1-5)?",
                    min_value=1,
                    max_value=5,step=1,
                    format="%d ⭐",
                ),
            },disabled=["Item", "Quantity", "Price", "Item Total"], hide_index=True)
        
        st.write(f"Chef Dah Siap untuk meja :{tableno}")
        if st.button('Klik Sini Kalau Dah Hantar ke Meja '+tableno):
            timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
            orderdf.to_csv('sales_report_'+tableno+'_'+timestamp+'.csv')
            os.rename(order,"served"+order)
            st.success("Order dah hantar ke pelanggan!")
    
elif (choose == "Chef"):
    st.title("Chef Page")
    cwd = os.getcwd()
    print (cwd)
    file = []
    file = fnmatch.filter(os.listdir(cwd), 'sales_order*.csv')
    ordersum =len(file)
    for order in file:
        tableno = order[12]
        orderdf = pd.read_csv(order)
        orderdf["Done"] = False
        orderdf["TableNo"]= tableno
        st.data_editor(
            orderdf,disabled=["Item", "Quantity", "Price", "Item Total"], hide_index=True)
        
        if st.button('Confirm Siap Table '+tableno):
            orderdf["Done"] = True
            orderdf.to_csv('sales_chef_'+tableno+'.csv')
            os.rename(order,"chefdone"+order)
            st.success("Order Chef Save and submit successfully!")
        
    # st.write(file[0])
    
# Add a new column for quantity input
# menu_df['Quantity'] = menu_df.apply(lambda x: st.number_input(f"Quantity of {x['Item']}", min_value=0, max_value=10, key=x['Item']), axis=1)

# Streamlit app
# def main():
    

# if __name__ == '__main__':
    # main()
