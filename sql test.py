import sqlite3

db = sqlite3.connect('db.sqlite3')
cursor = db.cursor()
cursor.execute("UPDATE main_product SET stock = 51 WHERE main_product.id = 1 ")
db.commit()
db.close()



'''db = sqlite3.connect('db.sqlite3')
update_sql = "UPDATE main_product SET stock = 51 WHERE main_product.id = 1 "
update_cursor = db.cursor()
update_cursor.execute(update_sql)
update_cursor.close()
db.close()'''


db = sqlite3.connect('db.sqlite3')
cursor = db.cursor()
cursor.execute("SELECT product_id, quantity FROM main_orderitem WHERE order_id='106'")


for product_id, quanity in cursor:
    product_id = product_id
    print('prodID:', product_id)
    print('prodQ:', quanity)
    print('-----')


db = sqlite3.connect('db.sqlite3')
cursor = db.cursor()
cursor.execute("SELECT stock FROM main_product WHERE id= 12 ")


for stock in cursor:
    print('prod STOCK:', stock)

    print('-----')



#cursor.execute("SELECT stock FROM main_product WHERE product_id= 1", (ordernumber,))
cursor.execute("SELECT stock FROM main_product WHERE id= ?", (1, 10))
for stock in cursor:
    print('stock:', stock)




#newPrice = '$19.99'
#book_id = 4
#cursor.execute('''UPDATE books SET price = ? WHERE id = ?''', (newPrice, book_id))