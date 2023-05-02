from flask import Flask, render_template, request

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
