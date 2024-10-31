from flask import render_template, request, redirect, session, url_for, flash
from flask_app import app
from flask_app.models.item import Item
from flask_app.models.user import User

# READ ALL
@app.route('/')
def view_storefront():
    items = Item.get_all()
    return render_template('dashboard.html', items=items)

# CREATE
@app.route('/new_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        try:
            data = {
                'name': request.form['Name'],
                'price': request.form['Price'],
                'in_stock': request.form['Stock'],
                'description': request.form['Description']
            }

            # Attempt to save the item to the database
            result = Item.save(data)

            # Check if the result indicates a successful insertion
            if result:
                flash('Item added successfully!', 'success')
                return redirect(url_for('view_inventory'))  # Redirect to inventory view
            else:
                flash('Error adding item', 'danger')

        except KeyError as e:
            flash(f'Missing field: {str(e)}', 'danger')
            return redirect('/dashboard')  # Redirect back to the form if there's an error
    return render_template('dashboard.html')

# READ ONE
@app.route('/items/<int:item_id>')
def view_item(item_id):
    item = Item.get_by_id(item_id)
    return render_template('view_items.html', item=item)

# EDIT
@app.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
def edit_item(item_id):
    item = Item.get_by_id(item_id)
    if request.method == 'POST':
        data = {
            'id': item_id,
            'name': request.form['name'],
            'price': request.form['price'],
            'in_stock': request.form['in_stock'],
            'description': request.form['description']
        }
        success = Item.update(data)
        if success:
            flash('Item updated successfully!', 'success')
            return redirect(url_for('view_inventory'))
        else:
            flash('Error updating item', 'danger')
    return render_template('edit_item.html', item=item)

# DELETE
@app.route('/item/<int:item_id>/delete', methods=['POST'])
def delete_item(item_id):
    Item.delete(item_id)
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('view_inventory'))
