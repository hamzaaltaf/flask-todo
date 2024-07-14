price = 99
discount = 0
quantity = int(input("Enter the number of packages you have purchased? "))
if quantity < 1:
    print("Sorry!")
total_price = quantity * price
if quantity > 9 and quantity < 20:
    discount = 0.10 * total_price
    total_price = total_price - discount
elif quantity > 19 and quantity < 50:
    discount = 0.20 * total_price
    total_price = total_price - discount
elif quantity > 49 and quantity < 99:
    discount = 0.30 * total_price
    total_price = total_price - discount
print("Your discount is: ", discount)
print("Total amount of purchase after discount is: ", total_price)