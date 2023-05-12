from flask import Flask, render_template, request

app = Flask(__name__)

#Global Variables that define how many rows and columns there are
ROWS = 12
COLUMNS = 4

#Seat chart that uses the global variables
seat_chart = [[0 for col in range(COLUMNS)] for row in range(ROWS)]
#cost matrix 
cost_matrix = [[100, 75, 50, 100] for row in range(ROWS)]
#create an empty reservations dictionary
reservations = {}
#open and read from reservations.txt
with open("reservations.txt", "r") as f:
    for line in f:
        data = line.strip().split(", ")
        if len(data) >= 4:
            reservations[(int(data[1]), int(data[2]))] = {"name": data[0], "ticket_number": data[3]}
        else:
            print(f"Error: Invalid line in reservations file: {line}")
admin_users = {}
#open and read from passcodes.txt
with open("passcodes.txt", "r") as f:
    for line in f:
        data = line.strip().split(", ")
        admin_users[data[0]] = data[1]

#writes into reservations.txt once the user reserves a seat
def save_reservation(first_name, row, col, confirmation):
    with open("reservations.txt", "a") as f:
        f.write(f"{first_name}, {row}, {col}, {confirmation}\n")
        reservations[(row, col)] = {"name": first_name, "ticket_number": confirmation}

#generates the confimation number that is written into reservations.txt
def reservation_confirmation(first_name):
    name = first_name
    class_code = "INFOTC4320"
    confirmation = ""
    for i in range(len(name)):
        confirmation += name[i] + class_code[i]
    confirmation += class_code[len(name):]
    
    return confirmation

#reads from reservations.txt and calculates the total sales based on the cost_matrix
def calculate_sales():
    sales = 0
    with open("reservations.txt", "r") as f:
        for line in f:
            data = line.strip().split(", ")
            if len(data) >= 4:
                row = int(data[1])
                col = int(data[2])
                if (row, col) in reservations:
                    seat_cost = cost_matrix[row][col]
                    sales += seat_cost
            else:
                print(f"Error: Invalid line in reservations file: {line}")
    return sales

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
