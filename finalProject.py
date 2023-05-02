from flask import Flask, render_template, request

app = Flask(__name__)

#Global Variables that define how many rows and columns there are
ROWS = 12
COLUMNS = 4

#Seat chart that uses the global variables
seat_chart = [[0 for col in range(COLUMNS)] for row in range(ROWS)]
#cost matrix 
cost_matrix = [[100, 75, 50, 100] for row in range(ROWS)]

#renders our index.html page
@app.route("/")
def index():
    return render_template("index.html")
#renders the admin_login page
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        #checks the admin username/password
        if username in admin_users and admin_users[username] == password:
            with open("reservations.txt", "r"):
                total_sales = calculate_sales()
                return render_template("admin_dashboard.html", reservations=reservations, total_sales=total_sales, ROWS=ROWS, COLUMNS=COLUMNS)
        #returns error if admin username/password are incorrect
        else:
            return render_template("admin_login.html", error=True)
    else:
        return render_template("admin_login.html", error=False)
    
    #renders the seat reservation page
@app.route('/reserve_seat', methods=['GET', 'POST'])
def reserve_seat():

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        row = int(request.form['row'])
        col = int(request.form['col'])
        #checks to see if the reservation was successful 
        if seat_chart[row][col] == 0:
            confirmation = reservation_confirmation(first_name)
            seat_chart[row][col] = 1
            save_reservation(first_name, row, col, confirmation)
            return render_template('reservation_success.html', first_name=first_name, last_name=last_name, row=row, col=col, confirmation=confirmation)
        #renders the reservation error page if the seat is already taken 
        else:
            return render_template('reservation_error.html')
    else:
        with open("reservations.txt", "r"):
                return render_template("reserve_seat.html", reservations=reservations, ROWS=ROWS, COLUMNS=COLUMNS)

app.run(debug=True)
