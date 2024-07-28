from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = '0311d15c2e79e038e94f0c5f0af549d9b0929c5bfb4212f22d9efa9eabc69f6b'  # Change this to a real secret key

# Database configuration
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'truck_management'
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('You need to be logged in to access this page.', 'error')
            return redirect(url_for('signin'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html')






@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        
        conn = get_db_connection()
        if not conn:
            flash('Database connection failed', 'error')
            return redirect(url_for('signup'))
        
        cursor = conn.cursor()
        
        # Check if the username already exists
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        
        if user:
            flash('Username already exists. Please sign in.', 'error')
            cursor.close()
            conn.close()
            return redirect(url_for('signin'))
        
        # Insert new user
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        try:
            cursor.execute('INSERT INTO users (username, password, role) VALUES (%s, %s, %s)',
                           (username, hashed_password, role))
            conn.commit()
            flash('Signup successful. Please sign in.', 'success')
        except Error as err:
            print(f"Error: {err}")
            flash('Failed to create account', 'error')
        finally:
            cursor.close()
            conn.close()
        
        return redirect(url_for('signin'))
    
    return render_template('signup.html')








@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        if not conn:
            flash('Database connection failed', 'error')
            return redirect(url_for('signin'))
        
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user and check_password_hash(user[2], password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials', 'error')
            return redirect(url_for('signin'))
    
    return render_template('signin.html')






@app.route('/dispatch_plans', methods=['GET', 'POST'])
@login_required
def dispatch_plans():
    conn = get_db_connection()
    if not conn:
        flash('Database connection failed', 'error')
        return redirect(url_for('dispatch_plans'))
    
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        data = request.json
        print(data)  # Debugging: Print the received data

        # Check if all fields are present
        required_fields = ['source', 'source_id', 'destination', 'destination_id', 'product_code', 
                            'product_description', 'priority', 'qty_case', 'weight_tons', 'truck_type_required']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            flash(f'Missing fields: {", ".join(missing_fields)}', 'error')
            return jsonify({'error': 'Missing fields'}), 400

        try:
            cursor.execute("""
                INSERT INTO dispatch_plans 
                (source, source_id, destination, destination_id, product_code, product_description, priority, qty_case, weight_tons, truck_type_required) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (data['source'], data['source_id'], data['destination'], data['destination_id'], data['product_code'], 
                  data['product_description'], data['priority'], data['qty_case'], data['weight_tons'], data['truck_type_required']))
            conn.commit()
            flash('Dispatch plan created successfully', 'success')
            return jsonify({'message': 'Dispatch plan created successfully'}), 201
        except Exception as e:
            print(f"Error: {e}")
            flash('Failed to create dispatch plan', 'error')
            return jsonify({'error': 'Failed to create dispatch plan'}), 500
        finally:
            cursor.close()
            conn.close()
    
    cursor.execute("SELECT * FROM dispatch_plans")
    dispatch_plans = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('dispatch_plans.html', dispatch_plans=dispatch_plans)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_dispatch_plan(id):
    conn = get_db_connection()
    if not conn:
        flash('Database connection failed', 'error')
        return redirect(url_for('dispatch_plans'))
    
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        data = request.form
        try:
            cursor.execute("""
                UPDATE dispatch_plans 
                SET source = %s, source_id = %s, destination = %s, destination_id = %s, product_code = %s, 
                    product_description = %s, priority = %s, qty_case = %s, weight_tons = %s, truck_type_required = %s 
                WHERE id = %s
            """, (data['source'], data['source_id'], data['destination'], data['destination_id'], data['product_code'], 
                  data['product_description'], data['priority'], data['qty_case'], data['weight_tons'], data['truck_type_required'], id))
            conn.commit()
            flash('Dispatch plan updated successfully', 'success')
        except Error as err:
            print(f"Error: {err}")
            flash('Failed to update dispatch plan', 'error')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('dispatch_plans'))
    
    cursor.execute("SELECT * FROM dispatch_plans WHERE id = %s", (id,))
    plan = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not plan:
        flash('Dispatch plan not found', 'error')
        return redirect(url_for('dispatch_plans'))
    
    return render_template('update.html', plan=plan)

@app.route('/dispatch_plans/<int:id>', methods=['DELETE'])
@login_required
def delete_dispatch_plan(id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM dispatch_plans WHERE id = %s", (id,))
        conn.commit()
        return jsonify({'message': 'Dispatch plan deleted successfully'}), 200
    except Error as err:
        print(f"Error: {err}")
        return jsonify({'error': 'Failed to delete dispatch plan'}), 500
    finally:
        cursor.close()
        conn.close()







@app.route('/invoices', methods=['GET', 'POST'])
@login_required
def invoices():
    conn = get_db_connection()
    if not conn:
        flash('Database connection failed', 'error')
        return redirect(url_for('home'))
    
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        data = request.json
        print(data)  # Debugging: Print the received data

        # Check if all fields are present
        required_fields = ['invoice_number', 'dispatch_plan_id', 'amount']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            flash(f'Missing fields: {", ".join(missing_fields)}', 'error')
            return jsonify({'error': 'Missing fields'}), 400

        try:
            cursor.execute("""
                INSERT INTO invoices 
                (invoice_number, dispatch_plan_id, amount) 
                VALUES (%s, %s, %s)
            """, (data['invoice_number'], data['dispatch_plan_id'], data['amount']))
            conn.commit()
            flash('Invoice created successfully', 'success')
            return jsonify({'message': 'Invoice created successfully'}), 201
        except Exception as e:
            print(f"Error: {e}")
            flash('Failed to create invoice', 'error')
            return jsonify({'error': 'Failed to create invoice'}), 500
        finally:
            cursor.close()
            conn.close()
    
    cursor.execute("SELECT * FROM invoices")
    invoices = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('invoices.html', invoices=invoices)

@app.route('/update_invoice/<int:id>', methods=['GET', 'POST'])
@login_required
def update_invoice(id):
    conn = get_db_connection()
    if not conn:
        flash('Database connection failed', 'error')
        return redirect(url_for('invoices'))
    
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        data = request.json
        try:
            cursor.execute("""
                UPDATE invoices 
                SET invoice_number = %s, dispatch_plan_id = %s, amount = %s
                WHERE id = %s
            """, (data['invoice_number'], data['dispatch_plan_id'], data['amount'], id))
            conn.commit()
            flash('Invoice updated successfully', 'success')
            return jsonify({'message': 'Invoice updated successfully'}), 200
        except Exception as e:
            print(f"Error: {e}")
            flash('Failed to update invoice', 'error')
            return jsonify({'error': 'Failed to update invoice'}), 500
        finally:
            cursor.close()
            conn.close()

    cursor.execute("SELECT * FROM invoices WHERE id = %s", (id,))
    invoice = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template('invoice_update.html', invoice=invoice)


@app.route('/delete_invoice/<int:id>', methods=['DELETE'])
@login_required
def delete_invoice(id):
    conn = get_db_connection()
    if not conn:
        flash('Database connection failed', 'error')
        return redirect(url_for('invoices'))
    
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM invoices WHERE id = %s", (id,))
        conn.commit()
        flash('Invoice deleted successfully', 'success')
        return jsonify({'message': 'Invoice deleted successfully'}), 200
    except Exception as e:
        print(f"Error: {e}")
        flash('Failed to delete invoice', 'error')
        return jsonify({'error': 'Failed to delete invoice'}), 500
    finally:
        cursor.close()
        conn.close()








@app.route('/truck_details', methods=['GET', 'POST'])
def truck_details():
    conn = get_db_connection()
    if not conn:
        flash('Database connection failed', 'error')
        return redirect(url_for('home'))
    
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        new_truck = {
            'truck_number': request.form['truck_number'],
            'truck_type': request.form['truck_type'],
            'truck_company': request.form['truck_company'],
            'length': request.form['length'],
            'width': request.form['width'],
            'height': request.form['height'],
            'conditions': request.form['conditions'],
            'dispatch_plan_id': request.form['dispatch_plan_id'],
            'driver_name': request.form['driver_name'],
            'driver_license': request.form['driver_license']
        }
        try:
            cursor.execute("""
                INSERT INTO truck_details 
                (truck_number, truck_type, truck_company, length, width, height, conditions, dispatch_plan_id, driver_name, driver_license) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (new_truck['truck_number'], new_truck['truck_type'], new_truck['truck_company'], new_truck['length'],
                  new_truck['width'], new_truck['height'], new_truck['conditions'], new_truck['dispatch_plan_id'],
                  new_truck['driver_name'], new_truck['driver_license']))
            conn.commit()
            flash('Truck added successfully', 'success')
        except Exception as err:
            print(f"Error: {err}")
            flash('Failed to add truck', 'error')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('truck_details'))
    
    cursor.execute("SELECT * FROM truck_details")
    trucks = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('truck_details.html', trucks=trucks)

@app.route('/update_truck/<int:truck_id>', methods=['GET', 'POST'])
def update_truck(truck_id):
    conn = get_db_connection()
    if not conn:
        flash('Database connection failed', 'error')
        return redirect(url_for('truck_details'))

    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM truck_details WHERE id = %s", (truck_id,))
    truck = cursor.fetchone()
    
    if request.method == 'POST':
        updated_truck = {
            'truck_number': request.form['truck_number'],
            'truck_type': request.form['truck_type'],
            'truck_company': request.form['truck_company'],
            'length': request.form['length'],
            'width': request.form['width'],
            'height': request.form['height'],
            'conditions': request.form['conditions'],
            'dispatch_plan_id': request.form['dispatch_plan_id'],
            'driver_name': request.form['driver_name'],
            'driver_license': request.form['driver_license']
        }
        try:
            cursor.execute("""
                UPDATE truck_details 
                SET truck_number = %s, truck_type = %s, truck_company = %s, length = %s, width = %s, height = %s, conditions = %s, 
                    dispatch_plan_id = %s, driver_name = %s, driver_license = %s 
                WHERE id = %s
            """, (updated_truck['truck_number'], updated_truck['truck_type'], updated_truck['truck_company'], 
                  updated_truck['length'], updated_truck['width'], updated_truck['height'], updated_truck['conditions'], 
                  updated_truck['dispatch_plan_id'], updated_truck['driver_name'], updated_truck['driver_license'], truck_id))
            conn.commit()
            flash('Truck updated successfully', 'success')
        except Exception as err:
            print(f"Error: {err}")
            flash('Failed to update truck', 'error')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('truck_details'))
    
    cursor.close()
    conn.close()

    if not truck:
        flash('Truck not found', 'error')
        return redirect(url_for('truck_details'))
    
    return render_template('truck_update.html', truck=truck)

@app.route('/delete_truck/<int:truck_id>', methods=['DELETE'])
def delete_truck(truck_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM truck_details WHERE id = %s", (truck_id,))
        conn.commit()
        return jsonify({'message': 'Truck deleted successfully'}), 200
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({'error': 'Failed to delete truck'}), 500
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)
