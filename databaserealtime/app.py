from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase






config = {

  "apiKey": "AIzaSyCWteM0sMb5OE5KhY1w_LMaElO0nBQhW7c",

  "authDomain": "yazeedalyan00-d8676.firebaseapp.com",

  "projectId": "yazeedalyan00-d8676",

  "storageBucket": "yazeedalyan00-d8676.appspot.com",

  "messagingSenderId": "555134451022",

  "appId": "1:555134451022:web:f1b92fb8f7864b6fe3721f",

  "measurementId": "G-DGMFC4JCRZ",
  "databaseURL": "https://yazeedalyan00-d8676-default-rtdb.europe-west1.firebasedatabase.app/"

}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

user = {
    "email" : "email" , "full_name" : "full_name" , "username" : "username" , "password" : "password" , "bio" : "bio" 
}





app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
      
       try:
          login_session['user'] = auth.sign_in_with_email_and_password(email, password)
          db.child("users").child(login_session['user']['localid']).set(user)
          return redirect(url_for('add_tweet'))
       except:
           error = "Authentication failed"
           return render_template("signin.html")
    else :
           return render_template("signin.html")




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       full_name = request.form['full_name']
       username = request.form['username']
       bio = request.form['bio']

       try:
        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        return redirect(url_for('add_tweet'))

       except:
        error = "Authentication failed"
        return render_template("signup.html")
    else :
        return render_template("signup.html")




@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
       try:
        tweet = {"Title":request.form['Title'],"Text":request.form['Text'],"uid": login_session['user']['localId']}
        db.child("tweets").push(tweet)
        return redirect(url_for('all_tweet'))
       except:
         print("cant refresh")
   



    return render_template("add_tweet.html")

@app.route('/all_tweet', methods=['GET', 'POST'])
def all_tweet():
    tweets = db.child("tweets").get().val()
    return render_template("all-tweets.html", tweets = tweets)


  


if __name__ == '__main__':
    app.run(debug=True)