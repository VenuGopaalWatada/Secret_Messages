from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SECRET_KEY'] = 'Bobby@0559'

login_manager = LoginManager()
login_manager.init_app(app)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    username = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)

db.init_app(app)

with app.app_context():
    db.create_all()
    
@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)

@app.route('/', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    try:
        if request.method == "POST":
            user = Users.query.filter_by(email=request.form.get("email")).first()
            if user.password == request.form.get("password"):
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash("Incorrect Password. Please try again.")
                return render_template('wrongpass.html')
    except AttributeError:
        flash("Incorrect Email ID. Please try again.")
        return render_template('wrongpass.html')
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        user = Users(username=request.form.get("username"),
                     email=request.form.get("email"),
                     password=request.form.get("password"))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    username = current_user.username
    return render_template('home.html', username = username)

@app.route('/encrypt')
@login_required
def encrypt():
    return render_template('encrypt.html')

@app.route('/encrypted', methods=['POST'])
@login_required
def encrypted():
    message = request.form.get("enc-mes")
    error = "Error messgage"
    try:
        small_alphabet='sairecvnugopljdhytwbmfkqxz' # Small Letters String.
        CAPITAL_ALPHABET='SIRBOYCHNAUJGMDLWTEKXFZPVQ' # Capital Letters String.
        numbers='3725481096' # Numbers String.
        special_character=''' !@#$%^&*()`~-_=+[]\{}|;:'",./<>?''' # Special Characters String.
        new_message='' # Creating an empty string to assign the encrypted message to this.
        key=1 # Key Value is 1.
        for character in message: # For loop to encrypt every character in the message.
            if character in small_alphabet: # If character is a small letter.
                position=small_alphabet.find(character) # Assigning the position of the character in the small letter string to variable-position.
                new_position=(position+key)%26 # Assigning the value of encrypted letter to a variable-new_position.
                new_character=small_alphabet[new_position] # Assigning the encrypted letter to new_character variable.
                new_message=new_message+new_character # Assigning the encrypted character to the encrypted string.
                key=key+1 # Incrementing Key Value for the next iteration.
            elif character in CAPITAL_ALPHABET: # If character is a capital letter.
                position=CAPITAL_ALPHABET.find(character) # Assigning the position of character in the capital letter string to variable-position.
                new_position=(position+key)%26 # Assigning the value of the encrypted letter to variable-new_position.
                new_character=CAPITAL_ALPHABET[new_position] # Assigning the encrypted letter to new_character variable.
                new_message=new_message+new_character # Assigning the encrypted character to the encrypted string.
                key=key+1 # Incrementing Key Value for the next iteration.
            elif character in numbers: # If character is a number.
                position=numbers.find(character) # Assigning the position of the character in the numbers string to variable-position.
                new_position=(position+key)%10 # Assigning the value of the encrypted number to variable-new_position.
                new_character=numbers[new_position] # Assigning the encrypted letter to new_character variable.
                new_message=new_message+new_character # Assigning the encrypted character to the encrypted string.
                key=key+1 # Incrementing Key Value for the next iteration.
            elif character in special_character: # If character is a special character.
                position=special_character.find(character) # Assigning the position of character in the special characters string to variable-position.
                new_position=(position+key)%33 # Assigning the value of the encrypted letter to variable-new_position.
                new_character=special_character[new_position] # Assigning the encrypted letter to new_character variable.
                new_message=new_message+new_character # Assigning the encrypted character to the encrypted string.
                key=key+1 # Incrementing Key Value for the next iteration.
            else: # If character is an unidentified character.
                new_message=new_message+character # No encryption of unidentified characters and assigning the character to encrypted string.
        return render_template('encrypted.html', msg = new_message)
    except IOError:
        return render_template('encrypted.html', msg = error)

@app.route('/decrypt')
@login_required
def decrypt():
    return render_template('decrypt.html')

@app.route('/decrypted', methods=['POST'])
@login_required
def decrypted():
    message = request.form.get("dec-mes")
    error = "Error messgage"
    try:
        small_alphabet='sairecvnugopljdhytwbmfkqxz' # Small Letters String.
        CAPITAL_ALPHABET='SIRBOYCHNAUJGMDLWTEKXFZPVQ' # Capital Letters String.
        numbers='3725481096' # Numbers String.
        special_character=''' !@#$%^&*()`~-_=+[]\{}|;:'",./<>?''' # Special Characters String.
        new_message='' # Creating an empty string to assign the decrypted message to this.
        key=1 # Key Value is 1.
        for character in message: # For loop to decrypt every character in the message.
            if character in small_alphabet: # If character is a small letter.
                position=small_alphabet.find(character) # Assigning the position of the character in the small letter string to variable-position.
                new_position=(position-key)%26 # Assigning the value of decrypted letter to a variable-new_position.
                new_character=small_alphabet[new_position] # Assigning the decrypted letter to new_character variable.
                new_message=new_message+new_character # Assigning the decrypted character to the decrypted string.
                key=key+1 # Incrementing Key Value for the next iteration.
            elif character in CAPITAL_ALPHABET: # If character is a capital letter.
                position=CAPITAL_ALPHABET.find(character) # Assigning the position of character in the capital letter string to variable-position.
                new_position=(position-key)%26 # Assigning the value of the decrypted letter to variable-new_position.
                new_character=CAPITAL_ALPHABET[new_position] # Assigning the decrypted letter to new_character variable.
                new_message=new_message+new_character # Assigning the decrypted character to the decrypted string.
                key=key+1 # Incrementing Key Value for the next iteration.
            elif character in numbers: # If character is a number.
                position=numbers.find(character) # Assigning the position of the character in the numbers string to variable-position.
                new_position=(position-key)%10 # Assigning the value of the decrypted number to variable-new_position.
                new_character=numbers[new_position] # Assigning the decrypted letter to new_character variable.
                new_message=new_message+new_character # Assigning the decrypted character to the decrypted string.
                key=key+1 # Incrementing Key Value for the next iteration.
            elif character in special_character: # If character is a special character.
                position=special_character.find(character) # Assigning the position of character in the special characters string to variable-position.
                new_position=(position-key)%33 # Assigning the value of the decrypted letter to variable-new_position.
                new_character=special_character[new_position] # Assigning the decrypted letter to new_character variable.
                new_message=new_message+new_character # Assigning the decrypted character to the decrypted string.
                key=key+1 # Incrementing Key Value for the next iteration.
            else: # If character is an unidentified character.
                new_message=new_message+character # No decryption of unidentified characters and assigning the character to decrypted string.
            print(new_message) # Displaying the decrypted message.
        return render_template('decrypted.html', msg = new_message)
    except IOError:
        return render_template('decrypted.html', msg = error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)