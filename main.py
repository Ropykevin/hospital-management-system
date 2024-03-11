from flask_login import LoginManager, login_user, logout_user, current_user
from flask import Flask, jsonify, request, render_template, redirect, session, flash
from dbs import Hospital, Specialty, Doctor, Patient, db, User
import sqlite3
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.secret_key = 'your_secret_key' 
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))



@app.route('/')
def landing():
    return render_template("index.html")

# Route to retrieve all hospitals


@app.route('/hospitals', methods=['GET'])
def get_hospitals():
    try:
        hospitals = Hospital.query.all()
        return render_template('hospitals.html', hospitals=hospitals)
    except Exception as e:
        print(f"Error fetching hospitals: {str(e)}")
        # Optionally, log the error message for further investigation
        # logger.error(f"Error fetching hospitals: {str(e)}")
        return render_template('error.html', error_message="Error fetching hospitals")

# Route to retrieve a specific hospital by ID


@app.route('/hospital/<int:hospital_id>', methods=['GET'])
def get_hospital(hospital_id):
    hospital = Hospital.query.get(hospital_id)
    if hospital:
        return render_template('hospital.html')
    else:
        flash('error Hospital not found')

# Route to create a new hospital


@app.route('/add_hospital', methods=['GET', 'POST'])
def add_hospital():
    if request.method == 'POST':
        # Handle form submission to add a new hospital
        name = request.form['name']
        location = request.form['location']
        contact_info = request.form['contact_info']
        # Create a new hospital object and add it to the database
        new_hospital = Hospital(
            name=name, location=location, contact_info=contact_info)
        db.session.add(new_hospital)
        db.session.commit()
        flash('Hospital added successfully', 'success')
        return redirect('/hospitals')
    return render_template('add_hospital.html')
# Route to update an existing hospital


@app.route('/update_hospital/<int:hospital_id>', methods=['GET', 'POST'])
def update_hospital(hospital_id):
    hospital = Hospital.query.get(hospital_id)
    if hospital:
        if request.method == 'POST':
            # Handle form submission to update the hospital
            hospital.name = request.form['name']
            hospital.location = request.form['location']
            hospital.contact_info = request.form['contact_info']
            db.session.commit()
            flash('Hospital updated successfully', 'success')
            return redirect(f'/hospital/{hospital_id}')
        return render_template('update_hospital.html', hospital=hospital)
    else:
        flash('Hospital not found', 'error')
        return redirect('/hospitals')


@app.route('/delete_hospital/<int:hospital_id>')
def delete_hospital(hospital_id):
    hospital = Hospital.query.get(hospital_id)
    if hospital:
        db.session.delete(hospital)
        db.session.commit()
        flash('Hospital deleted successfully', 'success')
    else:
        flash('Hospital not found', 'error')
    return redirect('/hospitals')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # handle request
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful, please login.', 'success')
        return redirect('/login')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Login successful.', 'success')
            return redirect('/dashboard')
        else:
            flash('Invalid email or password.', 'error')
            return redirect('/login')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


@app.route('/doctors')
def doctors():
    doctors = Doctor.query.all()  # Fetch all doctors from the database
    return render_template('doctors.html', doctors=doctors)


@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect('/login')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
