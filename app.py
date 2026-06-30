from flask import *
import pymysql
import os
from flask_cors import CORS
# initialize the application
app = Flask(__name__)

CORS(app)

app.config['UPLOAD_FOLDER'] = 'static/images'

# Create the folder if it does not exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Create a reusable function for uploading images
def save_image(file):
    filename = file.filename
    photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(photo_path)
    return filename
 

# define the route/endpoint
@app.route("/api/signup" , methods=["POST"])

# define the function
def signup():
    # get user inputs from the form
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    phone = request.form["phone"]

    # connection to database
    connection = pymysql.connect(
    host=" mysql-mark234.alwaysdata.net",
    user="mark234",
    password="modcom2026",
    database="mark234_sokogarden"
    ) 

    # define the cursor
    cursor = connection.cursor()

    # define sql to users
    sql = "INSERT INTO users(username,password,email,phone) VALUES(%s,%s,%s,%s)"

    # define your data
    # NB: Coming from step 3
    data = (username,password,email,phone)

    # execute/run query
    cursor.execute(sql,data)

    # commit/save changes
    connection.commit()

    return jsonify({"message" : "User registered Successfully"})

# member signin/login
# define the route/endpoint
@app.route("/api/signin", methods=["POST"])

# define the function
def signin() :
    # get user inputs from the form
    email=request.form["email"]
    password=request.form["password"]
    
    # connection to database
    connection = pymysql.connect(
    host=" mysql-mark234.alwaysdata.net",
    user="mark234",
    password="modcom2026",
    database="mark234_sokogarden"
    ) 

    # define the cursor
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    # define sql to select users
    sql = "select * from users where email = %s and password = %s"

    # define your data
    # NB: Coming from step 3
    data = (email , password)

    # execute/run query
    cursor.execute(sql,data)

    # wrong email and password
    if cursor.rowcount == 0 :
        return jsonify({"message" : "Invalid email or password"})
    
    # correct email and password
    if cursor.rowcount == 1 :
        # fetch the user
        user = cursor.fetchone()
        return jsonify({"message" : "Login Successful" , "user" : user 
        })
    
    
# add products
# 1. define your route/endpoint
@app.route("/api/addproduct", methods=["POST"])

# 2. define the fuction
def addproduct():
    # 3. get user inputs from the form
    product_name = request.form["product_name"]
    product_description = request.form["product_description"]
    product_cost = request.form["product_cost"]
    product_category = request.form["product_category"]
    product_photo = request.files["product_photo"]

    filename = save_image(product_photo)

     # 4. connection to database
    connection = pymysql.connect(
    host=" mysql-mark234.alwaysdata.net",
    user="mark234",
    password="modcom2026",
    database="mark234_sokogarden"
    ) 

    # 5. define the cursor
    cursor = connection.cursor()

    # 6.define sql to products
    sql = "INSERT INTO product_details(product_name,product_description,product_cost,product_category,product_photo) VALUES(%s,%s,%s,%s,%s)"

    # 7. define your data
    # NB: Coming from step 3
    data = (product_name,product_description,product_cost,product_category,filename)

    # 8. execute/run query
    cursor.execute(sql,data)

    # 9. commit/save changes
    connection.commit()

    return jsonify({"message" : "Product added Successfully"})

# fetch products/get products
# 1.Define route/endpoint
@app.route("/api/getproducts" , methods=["GET"])

# 2. Define the function
def getproducts() :

    # 3. Connection to database
    connection = pymysql.connect(
    host=" mysql-mark234.alwaysdata.net",
    user="mark234",
    password="modcom2026",
    database="mark234_sokogarden"
    ) 

    # 4. Define the cursor
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    # 5. Define sql to fetch products
    sql = "select * from product_details"

    # 6. Execute/run query
    cursor.execute(sql)

    # 7. Fetch all products
    allproducts = cursor.fetchall()

    # 8. Return all products
    return jsonify(allproducts)

# MPESA INTEGRATION
    # Mpesa Payment Route 
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth

@app.route('/api/mpesa_payment', methods=['POST'])
def mpesa_payment():
        if request.method == 'POST':
            # Extract POST Values sent
            amount = request.form['amount']
            phone = request.form['phone']

            # Provide consumer_key and consumer_secret provided by safaricom
            consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
            consumer_secret = "amFbAoUByPV2rM5A"

            # Authenticate Yourself using above credentials to Safaricom Services, and Bearer Token this is used by safaricom for security identification purposes - Your are given Access
            api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
            # Provide your consumer_key and consumer_secret 
            response = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
            # Get response as Dictionary
            data = response.json()
            # Retrieve the Provide Token
            # Token allows you to proceed with the transaction
            access_token = "Bearer" + ' ' + data['access_token']

            #  GETTING THE PASSWORD
            timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')  # Current Time
            passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'  # Passkey(Safaricom Provided)
            business_short_code = "174379"  # Test Paybile (Safaricom Provided)
            # Combine above 3 Strings to get data variable
            data = business_short_code + passkey + timestamp
            # Encode to Base64
            encoded = base64.b64encode(data.encode())
            password = encoded.decode()

            # BODY OR PAYLOAD
            payload = {
                "BusinessShortCode": "174379",
                "Password":password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": "1",  # use 1 when testing
                "PartyA": phone,  # change to your number
                "PartyB": "174379",
                "PhoneNumber": phone,
                "CallBackURL": "https://coding.co.ke/api/confirm.php",
                "AccountReference": "SokoGarden Online",
                "TransactionDesc": "Payments for Products"
            }

            # POPULAING THE HTTP HEADER, PROVIDE THE TOKEN ISSUED EARLIER
            headers = {
                "Authorization": access_token,
                "Content-Type": "application/json"
            }

            # Specify STK Push  Trigger URL
            url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  
            # Create a POST Request to above url, providing headers, payload 
            # Below triggers an STK Push to the phone number indicated in the payload and the amount.
            response = requests.post(url, json=payload, headers=headers)
            print(response.text) # 
            # Give a Response
            return jsonify({"message": "An MPESA Prompt has been sent to Your Phone, Please Check & Complete Payment"})







    









    






    
    

    










































































































































































































# run the application
app.run(debug=True)
