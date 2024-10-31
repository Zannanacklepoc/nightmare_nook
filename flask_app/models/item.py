from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash

class Item:
    db = "storefront"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.price = data['price']
        self.stock = data['stock']
        self.description = data['description']
        self.user_id = data['user_id']

    @staticmethod
    def save(data):
        query = """
        INSERT INTO items (name, price, stock, description, user_id)
        VALUES (%(name)s, %(price)s, %(stock)s, %(description)s, %(user_id)s);
        """
        item_id = MySQLConnection(Item.db).query_db(query, data)
        print("Item ID created:", item_id)  # Debug: Confirm item is created
        if item_id:
            flash('Item added successfully!', 'success')
            return item_id
        else:
            flash('Failed to add item. Please try again.', 'danger')
            return None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM items;"
        results = MySQLConnection(cls.db).query_db(query)
        items = [cls(row) for row in results]
        return items

    @classmethod
    def get_by_id(cls, item_id):
        query = "SELECT * FROM items WHERE id = %(id)s;"
        data = {'id': item_id}
        result = MySQLConnection(cls.db).query_db(query, data)
        return cls(result[0]) if result else None
    
    
    @classmethod
    def update(cls, data):
        query = """
        UPDATE items
        SET name=%(name)s, price=%(price)s, stock=%(stock)s, description=%(description)s, user_id=%(user_id)s
        WHERE id = %(id)s;
        """
        print("Executing Update Query:", query, "with Data:", data)
        result = MySQLConnection(cls.db).query_db(query, data)
        print("Update Execution Result:", result)  # This should log whether it returns anything or not
        return result




    @classmethod
    def delete(cls, item_id):
        query = "DELETE FROM items WHERE id = %(id)s;"
        data = {'id': item_id}
        return MySQLConnection(cls.db).query_db(query, data)

    @staticmethod
    def validate_item(data):
        is_valid = True

        if not data.get('name') or len(data['name']) < 2:
            flash("Item name must be at least 2 characters long.", 'danger')
            is_valid = False

        if not data.get('price') or float(data['price']) <= 0:
            flash("Price must be greater than 0.", 'danger')
            is_valid = False

        if not data.get('stock') or int(data['stock']) < 0:
            flash("In-stock quantity cannot be negative.", 'danger')
            is_valid = False

        if not data.get('description') or len(data['description']) < 10 or len(data['description']) > 200:
            flash("Description must be between 10 and 200 characters.", 'danger')
            is_valid = False

        return is_valid
