from database.database_connection import app, db
from services.dish_service import check_dish_availability, dev_log, check_customer_id, insert_dish, check_dish_removal, check_price_total, get_latest_order, add_dish_to_order



print(check_dish_availability(1))

dev_log('test')

print(check_customer_id(2))

print(insert_dish('a dish', 'yes', 40, 2))

print('dish removal: ' + str(check_dish_removal(1)))

print('get price total: ' + str(check_price_total(1)))

print('get latest order: ' + str(get_latest_order(1)))

add_dish_to_order(1,1)