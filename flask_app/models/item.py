from flask import flash
from flask_app.config.mysqlconnection import MySQLConnection

class Item:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.price = data['price']
        self.in_stock = data['in_stock']
        self.description = data['description']

    @classmethod
    def get_all(cls):
        # GET ALL
        query = "SELECT * FROM items;"
        results = MySQLConnection('storefront').query_db(query)
        items = []
        for row in results:
            items.append(cls(row))
        return items

    @classmethod
    def get_by_id(cls, item_id):
        # GET BY ID
        query = "SELECT * FROM items WHERE id = %(id)s;"
        data = {'id': item_id}
        result = MySQLConnection('storefront').query_db(query, data)
        if result:
            return cls(result[0])
        return None

    @staticmethod
    def save(data):
        # SAVE
        if Item.validate_item(data):
            query = """
            INSERT INTO items (name, price, stock, description, category)
            VALUES (%(name)s, %(price)s, %(stock)s, %(description)s, %(category)s);
            """
            mysql = MySQLConnection('storefront')
            item_id = mysql.query_db(query, data)
            if item_id:
                flash('Item added successfully!', 'success')
                return item_id
            else:
                flash('Failed to add item. Please try again.', 'danger')
                return None
        else:
            flash('Invalid data. Please check your inputs.', 'danger')
            return None
                # Validation flash msgs

    @classmethod
    def update(cls, data):
        # EDIT/UPDATE
        if not cls.validate_item(data):
            return False
        query = """
        UPDATE items
        SET name=%(name)s, price=%(price)s, in_stock=%(in_stock)s, description=%(description)s, category=%(category)s
        WHERE id = %(id)s;
        """
        MySQLConnection('storefront').query_db(query, data)
        return True

    @classmethod
    def delete(cls, item_id):
        # DELETE
        query = "DELETE FROM items WHERE id = %(id)s;"
        data = {'id': item_id}
        MySQLConnection('storefront').query_db(query, data)

    # Validation
    @staticmethod
    def validate_item(data):
        is_valid = True

        if not data.get('name') or len(data['name']) < 2:
            flash("Item name must be at least 2 characters long.", 'danger')
            is_valid = False

        if not data.get('price') or float(data['price']) <= 0:
            flash("Price must be greater than 0.", 'danger')
            is_valid = False

        if not data.get('in_stock') or int(data['in_stock']) < 0:
            flash("In-stock quantity cannot be negative.", 'danger')
            is_valid = False

        if not data.get('description') or len(data['description']) < 10 or len(data['description']) > 200:
            flash("Description must be between 10 and 200 characters.", 'danger')
            is_valid = False

        return is_valid
