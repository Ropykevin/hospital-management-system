from flask_login import LoginManager, login_user, logout_user, current_user
from flask import Flask, jsonify, request, render_template, redirect, session, flash
from dbmodel import Hospital, Specialty, Doctor, Patient, db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Kevin254!@localhost/brian'
app.secret_key = 'your_secret_key'  # Add a secret key for session management
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def landing():
    return render_template("index.html")

# Route to retrieve all hospitals


@app.route('/hospitals', methods=['GET'])
def get_hospitals():
    hospitals = Hospital.query.all()
    return render_template('hospitals.html',hospitals=hospitals)
# Route to retrieve a specific hospital by ID


@app.route('/hospital/<int:hospital_id>', methods=['GET'])
def get_hospital(hospital_id):
    hospital = Hospital.query.get(hospital_id)
    if hospital:
        return render_template('hospital.html')
    else:
        flash('error Hospital not found')

# Route to create a new hospital


@app.route('/hospital', methods=['POST'])
def create_hospital():
    data = request.json
    hospital = Hospital(**data)
    db.session.add(hospital)
    db.session.commit()
    flash('Hospital created successfully', 'success')
    return redirect('/hospitals')

# Route to update an existing hospital


@app.route('/hospital/<int:hospital_id>', methods=['PUT'])
def update_hospital(hospital_id):
    hospital = Hospital.query.get(hospital_id)
    if hospital:
        data = request.json
        for key, value in data.items():
            setattr(hospital, key, value)
        db.session.commit()
        flash('Hospital updated successfully', 'success')
        return redirect('/hospital/{hospital_id}')
    else:
        return jsonify({'error': 'Hospital not found'}), 404

# Route to delete a hospital


@app.route('/hospital/<int:hospital_id>', methods=['DELETE'])
def delete_hospital(hospital_id):
    hospital = Hospital.query.get(hospital_id)
    if hospital:
        db.session.delete(hospital)
        db.session.commit()
        flash('Hospital deleted successfully', 'success')
        return redirect('/hospitals')
    else:
        return jsonify({'error': 'Hospital not found'}), 404


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
