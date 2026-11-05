import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
#an e-commerce product catalogue database
data={
    'product_id': [101, 102, 103, 104, 105],
    'product_name': ['TV', 'Mobile', 'Earphones', 'Shirt', 'Jeans'],
    'category': ['Electronics', 'Electronics', 'Accessories', 'Clothing', 'Clothing'],
    'price': [80.00, 45.0, 120.0, 35.0, np.nan],
    'stock_count': [15, 3, 8, 50, 100]
}


#Creating a dataframe

df=pd.DataFrame(data)
print('Original Product Catalogue:')
print(df)

if not os.path.exists("users.csv"):
    pd.DataFrame(
        columns=["username", "password"]
    ).to_csv("users.csv", index=False)

if not os.path.exists("cart_history.csv"):
    history=pd.DataFrame(columns=["username", "product_id", "product_name", "category", "price", "quantity", "subtotal"])
    history.to_csv("cart_history.csv", index=False)

#Registering the user
def register():
    username=input("Enter your username: ")
    password=input("Enter your password: ")

    users=pd.read_csv('users.csv')
    if username in users["username"].values:
        print("Username already exists!")
    else:
        new_user=pd.DataFrame({
            "username": [username],
            "password": [password]
        })

        users=pd.concat([users, new_user], ignore_index=True)
        users.to_csv("users.csv", index=False)
        print("Registration Successful")

#Login
def login():
    username=input("Enter username: ")
    password=input("Enter password: ")

    users=pd.read_csv("users.csv")

    result = users[
        (users["username"] == username) &
        (users["password"] == password)
    ]
    if result.empty:
        print("Invalid Username or Password")
        return None
    print("Login Successful")
    return username

#Catalogue
def catalogue():
    print("Hello user, here is your catalogue:")
    print(df[['product_name', 'price']])

#Search
def search_product(product_id):
    print("Is this what you are looking for?")
    result=df[df['product_id'] == product_id]

    if result.empty:
        print('Product not found')
    else:
        print(result)

#Cart
def cart(product_ids, quantities):
    print("Loading cart.....")
    cart=df[df['product_id'].isin(product_ids)].copy()
    cart["quantity"]=quantities
    return cart
#Cart History
def save_cart_history(username, cart_data):
    history=pd.read_csv("cart_history.csv")
    cart_data=cart_data.copy()
    cart_data["username"]=username
    cart_data["subtotal"]=(cart_data["price"]*cart_data["quantity"])
    history=pd.concat([
        history,
        cart_data[[
            "username",
            "product_id",
            "product_name",
            "category",
            "price",
            "quantity",
            "subtotal"
        ]]
    ], ignore_index=True)
    history.to_csv("cart_history.csv", index=False)
    print("Cart Created")
#Shipping
def shipping_service(subtotal):
    if subtotal > 300:
        shipping = np.random.randint(0,100)
    else:
        shipping = 0

    return shipping

def analyse_history():
    history=pd.read_csv("cart_history.csv")
    sns.histplot(data=history,x='price', bins=10,kde=True)
    plt.title("Distribution of product prices")
    plt.xlabel("price")
    plt.ylabel("Frequency")
    plt.show()

def main():
    print("1. Register")
    print("2. Login")
    choice=int(input("Please enter your selection"))
    if choice == 1:
        if not register():
            return
        username=login()
        if username is None:
            return
    elif choice == 2:
        username=login()
        if username is None:
            return
    else:
        print("Invalid choice")
        return
    print("Welcome", username)
    catalogue()
    id=int(input("Please enter the product id you are looking for"))
    search_product(id)
    product_ids=[]
    quantities=[]
    while True:
        prod = int(input("Enter product ID to cart"))
        quant=int(input("Enter quantity"))
        product_ids.append(prod)
        quantities.append(quant)
        choice = input("Do you want to add another product? (Yes/No)")
        if choice.lower() != "yes":
            break

    cart_data=cart(product_ids, quantities)
    if not cart_data.empty:
        save_cart_history(username, cart_data)
        print(cart_data)
        cart_data["subtotal"]=cart_data["price"]*cart_data["quantity"]
        subtotal=cart_data["subtotal"].sum()
        shipping_price=shipping_service(subtotal)
        print("Subtotal", subtotal)
        print("Shipping price", shipping_price)
        print("Your final amount: ", subtotal+shipping_price)
        vis=input("Do you want to visualize the graph? (Yes/No)")
        if vis.lower() == "yes":
            analyse_history()
        else:
            return None
    else:
        print("Empty")

        

if __name__=="__main__":
    main()