from database.database_connection import app, db
from services.dish_service import check_dish_availability, dev_log, check_customer_id, insert_dish, check_dish_removal



print(check_dish_availability(1))

dev_log('test')

print(check_customer_id(2))

print(insert_dish('a dish', 'yes', 40, 2))

print('dish removal: ' + str(check_dish_removal(1)))
