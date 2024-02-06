from flask import Flask, flash, jsonify, render_template, request, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, auth, firestore, storage
import os
from flask import send_file
import pandas as pd
from io import BytesIO

app = Flask(__name__)
# secret_key = os.urandom(24)
app.secret_key = os.urandom(24)  # Change this to a strong secret key

# Initialize Firebase Admin SDK
cred = credentials.Certificate(
    'flaskfirebase-7f1ef-firebase-adminsdk-135v6-c10dcd1b4b.json')
firebase_admin.initialize_app(cred, {'storageBucket': 'flaskfirebase-7f1ef.appspot.com'})


db = firestore.client()
bucket = storage.bucket()



@app.route('/')
def index():
    # Retrieve data from Firestore's 'sample-data' collection
    users_ref = db.collection('States/MH/CT/PU/EVTS')
    users = users_ref.stream()

    user_data = [{'Event Name': user.to_dict()['Name'], 'Event Information': user.to_dict(
    )['Short Description'], 'Keywords': user.to_dict()['Keywords'], 'Image URL': user.to_dict()['Image'], 'Registration Link': user.to_dict()['Link']} for user in users]

    # Check if the user is logged in or not
    # Assuming you store the user's ID in the session
    is_logged_in = 'user_email' in session

    return render_template('index.html', users=user_data, is_logged_in=is_logged_in)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            # Query Firestore to find the user with the given email
            user_docs = db.collection('College').where('email', '==', email).limit(1).get()

            if len(user_docs) == 1:
                user_data = user_docs[0].to_dict()
                #print(f"User Data from Firestore: {user_data}")
                stored_password = user_data.get('password', '')
                #print(stored_password)

                # Check if the entered password matches the stored password
                if stored_password == password:
                    # Store the user's ID in the session to check if the user is logged in
                    session['user_email'] = user_data['email']
                    #print("Successful")

                    # Redirect back to the index page after successful login
                    return redirect(url_for('index'))
                else:
                    #print("Fail-1")
                    flash('Authentication error: Invalid email or password', 'danger')
            else:
                print("Fail-2")
                flash('Authentication error: User not found', 'danger')

        except Exception as e:
            flash(f'Error: {e}', 'danger')
            print(f'Error: {e}')

    return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        college_code = request.form['college_code']
        mobile_no = request.form['mobile_number']

        try:
            user = auth.create_user(
                email=email,
                password=password
            )
            db.collection('College').add({
                'email': email,
                'password': password,
                'college_code': college_code,
                'mobile number': mobile_no
            })

            # Add the user's ID to the session
            session['user_id'] = user.uid

            # Redirect back to the index page
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error: {e}', 'danger')

    return render_template('register.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        team_leader_name = request.form['team_leader_name']
        team_member1_name = request.form['team_member1_name']
        team_member2_name = request.form['team_member2_name']
        team_member3_name = request.form['team_member3_name']
        team_leader_email = request.form['team_leader_email']
        mobile_no = request.form['mobile_number']
        team_name = request.form['team_name']

        try:
            # Add team information to the database
            db.collection('Teams').add({
                'team_leader_name': team_leader_name,
                'team_member1_name': team_member1_name,
                'team_member2_name': team_member2_name,
                'team_member3_name': team_member3_name,
                'team_leader_email': team_leader_email,
                'mobile_number': mobile_no,
                'team_name': team_name
            })

            # Render a template with the success message
            return render_template('registration_success.html')
        except Exception as e:
            flash(f'Error: {e}', 'danger')

    return render_template('registration.html')

@app.route('/data_form', methods=['GET', 'POST'])
def data_form():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']

        # Create a new document in Firestore's 'users' collection
        db.collection('users').add({
            'name': name,
            'mobile': mobile
        })

        return 'Data submitted successfully!'

    return render_template('data_form.html')


@app.route('/data', methods=['GET'])
def display_data():
    # Retrieve data from Firestore's 'users' collection
    users_ref = db.collection('users')
    users = users_ref.stream()

    user_data = [{'name': user.to_dict()['name'], 'mobile': user.to_dict()[
        'mobile']} for user in users]

    return render_template('display_data.html', users=user_data)



@app.route('/add_event')
def add_event():
    return render_template('add_event.html')

@app.route('/submit_event', methods=['POST'])
def submit_event():
    event_name = request.form.get('event_name')
    event_info = request.form.get('event_info')
    venue = request.form.get('venue')
    date = request.form.get('date')
    time = request.form.get('time')
    keywords = request.form.get('keywords')
    organizer = request.form.get('organizer')
    registration_link = request.form.get('registration_link')
    image_link = request.form.get('image_link')

    # Process the form data as needed, e.g., save it to a database

    
    # Check if an image file is included in the form
    db.collection('new-data').add({
            'Event Name': event_name,
            'Event Information': event_info,
            'Venue': venue,
            'Date': date,
            'Time': time,
            'Keywords': keywords,
            'Organizer': organizer,
            'Registration Link': registration_link,
            'Image URL': image_link  # Save the image URL in Firestore
        })


    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    # Clear the user's session to log them out
    session.clear()
    return redirect(url_for('index'))


# Add a new route for the college dashboard
@app.route('/college_dashboard')
def college_dashboard():
    # Retrieve data from Firestore's 'new-data' collection
    events_ref = db.collection('sample-data')
    events = events_ref.stream()

    event_data = [{'Event Name': event.to_dict()['Event Name'],
                   'Event Information': event.to_dict()['Event Information'],
                   'Venue': event.to_dict()['Venue'],
                   'Date': event.to_dict()['Date'],
                   'Time': event.to_dict()['Time'],
                   'Keywords': event.to_dict()['Keywords'],
                   'Organizer': event.to_dict()['Organizer'],
                   'Registration Link': event.to_dict()['Registration Link']} for event in events]
    
    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(event_data)

    # Create an in-memory Excel file
    excel_file = BytesIO()
    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Events')

    excel_file.seek(0)

    # Check if the user wants to download the Excel file
    download = request.args.get('download')
    if download:
        return send_file(excel_file, as_attachment=True, download_name='events_data.xlsx')

    # Check if the user is logged in or not
    # Assuming you store the user's ID in the session
    is_logged_in = 'user_email' in session

    return render_template('dashboard.html', events=event_data, is_logged_in=is_logged_in)



if __name__ == '__main__':
    app.run(debug=True)
