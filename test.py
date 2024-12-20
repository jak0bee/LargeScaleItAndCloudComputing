from database.database_connection import app, db
from services.dish_service import check_dish_availability, dev_log, check_customer_id, insert_dish, check_dish_removal, check_price_total, get_latest_order, add_dish_to_order,get_all_dishes, order_dish

print('test')
dev_log('test')

print('check dish av')
print(check_dish_availability(1))

print('check customer')
print(check_customer_id(2))

print('insert dish')
print(insert_dish('a dish', 'yes', 40, 2))

print('dish removal: ' + str(check_dish_removal(1)))

print('get price total: ' + str(check_price_total(1)))

print('get latest order: ' + str(get_latest_order(1)))

print()
add_dish_to_order(1,1)

print(get_all_dishes)

with app.app_context():
    response, status_code = get_all_dishes()
    print("Response JSON:", response.get_json())  # Extract JSON
    print("Status Code:", status_code)  # Print status code
print("add dish")
print(insert_dish("Steak","Steak with fries and a side of fried onions",6870, 15.99))


data_dish_not_available = {'customer_id': '1', 'dish_id': '1'}
print('order dish')
print('order dish' + order_dish(data_dish_not_available))