from flask import *

# initialize the application
app = Flask (__name__)

# Define route/endpoint
@app.route("/api/home")

# Define function
def home():
    return jsonify ({"message" : "Welcome home"})

@app.route("/api/services")
def services() :
    return jsonify({"message":"Welcome to services"})

@app.route("/api/about")
def about() :
    return jsonify({"message":"welcome to about"})

@app.route("/api/contact")
def contact() :
    return jsonify({"message":"Contact us for more information"})

@app.route("/api/products")
def products() :
    return jsonify({"message":"Products available"})

@app.route("/api/students")
def students() :
    return jsonify({"message" :"List of students"})

@app.route("/api/courses")
def courses() :
    return jsonify({"message":"Courses offered"})

@app.route("/api/teachers")
def teachers() :
    return jsonify({"message":"List of teachers"})

@app.route("/api/news")
def news() :
    return jsonify({"message":"Latest news updates"})

@app.route("/api/gallery")
def gallery() :
    return jsonify({"message":"Gallery images"})

@app.route("/api/faq")
def faq() :
    return jsonify({"message":"Frequently asked questions"})

@app.route("/api/profile")
def profile() :
    return jsonify({"message":"Student profile information"})

@app.route("/api/events")
def events():
    return jsonify({"message":"Upcoming events"})

@app.route("/api/library")
def library():
    return jsonify({"message":"Library resources available"})


@app.route("/api/add" , methods=["POST"])
def addition():
    if request.method=="POST":         
        number1=request.form["number1"]
        number2=request.form["number2"]

        sum=int(number1) + int(number2)
        return jsonify({"The answer is":sum})
    

    
@app.route("/api/diff" , methods=["POST"])
def difference():
    if request.method=="POST":
        number1=request.form["number1"]
        number2=request.form["number2"]


        difference=int(number1) - int(number2)
        return jsonify({"The difference is" : difference})
    

@app.route("/api/multi" , methods=["POST"])
def multiplication():
    if request.method=="POST":
        number1=request.form ["number1"]
        number2=request.form["number2"]

        multiplication=int(number1) * int(number2)
        return jsonify({"Answer" : multiplication})
    
@app.route("/api/div" , methods=["POST"])
def division():
    if request.method=="POST":
        number1=request.form["number1"]
        number2=request.form["number2"]   

        division=int(number1) / int(number2)
        
        return jsonify({"Answer" : division})
      










# run the application 
app.run(debug=True)