from flask import render_template, request, redirect, flash, url_for, session
from flask_app import app
from flask_app.models.item import Item

@app.route('/dashboard')
def view_storefront():
    items = Item.get_all()  # Fetch all items from the database
    return render_template('dashboard.html', items=items)

@app.route('/new_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'price': request.form['price'],
            'stock': request.form['stock'],
            'description': request.form['description'],
            'user_id': session['user_id']
        }
        result = Item.save(data)  # Save new item
        if result:
            return redirect(url_for('view_storefront'))
        else:
            flash("Item could not be saved to the database.", 'danger')
            return redirect('/new_item')
    return render_template('add_item.html')  # Render the form to add a new item

@app.route('/items/<int:item_id>')
def view_item(item_id):
    item = Item.get_by_id(item_id)  # Fetch the specific item by ID
    if item:
        return render_template('view_items.html', item=item)
    else:
        flash("Item not found.", 'danger')
        return redirect(url_for('view_storefront'))

@app.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
def edit_item(item_id):
    item = Item.get_by_id(item_id)
    if not item:
        flash("Item not found.", 'danger')
        return redirect(url_for('view_storefront'))

    if request.method == 'POST':
        data = {
            'id': item_id,
            'name': request.form['name'],
            'price': request.form['price'],
            'stock': request.form['stock'],
            'description': request.form['description'],
            'user_id': session['user_id']
        }

        success = Item.update(data)  # Update the item
        if success is not False:
            flash('Item updated successfully!', 'success')
            return redirect(url_for('view_storefront'))
        else:
            flash('Error updating item', 'danger')
            return redirect(url_for('edit_item', item_id=item_id))
    
    return render_template('edit_item.html', item=item)

@app.route('/item/<int:item_id>/delete', methods=['POST'])
def delete_item(item_id):
    Item.delete(item_id)  # Delete the item
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('view_storefront'))
