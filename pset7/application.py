from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from time import gmtime, strftime
import cs50

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():

    # get data from portfolio and users databases
    portfolio = db.execute("SELECT * FROM portfolio WHERE id = :id", id = session["user_id"])
    users = db.execute("SELECT * FROM users WHERE id = :id", id = session["user_id"])

    # declare variable for calculating sum of all stocks user has
    sum_stock_value = 0

    # iterate through user's portfolio
    for row in portfolio:
        symbol = row["Symbol"]
        shares = row["Shares"]
        stock = lookup(symbol)

        # update portfolio database with current prices and calculate cash balance
        db.execute("UPDATE portfolio SET Price = :price, TOTAL = :total WHERE Symbol = :symbol AND id = :id",
            price = stock["price"], total = round(stock["price"] * shares, 2), symbol = symbol, id = session["user_id"])

        # update sum
        sum_stock_value += stock["price"] * shares


    # display data for user
    return render_template("index.html", rows = portfolio, cash = users[0]["cash"], grand = round(users[0]["cash"] + sum_stock_value, 2), user = users[0]["username"])

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""

    users = db.execute("SELECT * FROM users WHERE id = :id", id = session["user_id"])

    if request.method == "POST":

        # get symbol and number of shares from user they want ot buy
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if symbol == "" or shares == "":
            return apology("must enter symbol and number of shares")

        stock = lookup(symbol)
        if not stock:
            return apology("invalid symbol")

        # get current amount of user's cash
        user_current_cash = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])

        # calculate difference
        diff_cash = user_current_cash[0]["cash"] - stock["price"] * int(shares)

        # if user can afford it, buy shares and update databases
        if not diff_cash < 0:

            # check if user already has stocks he wants to buy
            exists = db.execute("SELECT * FROM portfolio WHERE id = :id AND Symbol = :symbol", id = session["user_id"], symbol = stock["symbol"])

            # if so, just update portfolio
            if exists:

                current_shares = exists[0]["Shares"]
                current_TOTAL = exists[0]["TOTAL"]

                db.execute("UPDATE portfolio SET Shares = :shares, Price = :price, TOTAL = :total WHERE id = :id AND Symbol = :symbol",
                    shares = current_shares + shares, price = stock["price"], total = round(current_TOTAL + stock["price"] * shares, 2), id = session["user_id"], symbol = stock["symbol"])

            # else insert data
            else:
                db.execute("INSERT INTO portfolio (id, Symbol, Name, Shares, Price, TOTAL) VALUES(:id, :Symbol, :Name, :Shares, :Price, :TOTAL)",
                    id = session["user_id"], Symbol = stock["symbol"], Name = stock["name"], Shares = shares, Price = stock["price"], TOTAL = round(stock["price"] * int(shares), 2))

            # update user's cash
            db.execute("UPDATE users SET cash = :diff_cash WHERE id = :id", diff_cash = round(diff_cash, 2), id = session["user_id"])

            # insert transaction in history
            time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            db.execute("INSERT INTO history (id, Symbol, Shares, Price, Transacted) VALUES(:id, :Symbol, :Shares, :Price, :Transacted)",
                id = session["user_id"], Symbol = stock["symbol"], Shares = shares, Price = round(stock["price"], 2), Transacted = time)

            return redirect(url_for("index"))
        else:
            return apology("you can't afford it!")
    else:
        return render_template("buy.html", user = users[0]["username"])

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""

    users = db.execute("SELECT * FROM users WHERE id = :id", id = session["user_id"])

    # get data for user from history database
    transactions = db.execute("SELECT * FROM history WHERE id = :id", id = session["user_id"])

    # display user's transactions
    return render_template("history.html", rows = transactions, user = users[0]["username"])

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    users = db.execute("SELECT * FROM users WHERE id = :id", id = session["user_id"])

    if request.method == "POST":

        # get symbol from user
        symbol = request.form.get("symbol")

        # ensure user entered symbol
        if symbol == "":
            return apology("must enter symbol")

        # pass it to lookup function
        stock = lookup(symbol)

        # if symbol doesn't exist return apology
        if not stock:
            return apology("invalid symbol")
        else:
            # return results with quote_dislay template
            return render_template("quote_display.html", name = stock["name"], symbol = stock["symbol"], price = usd(stock["price"]), user = users[0]["username"])

    else:
        return render_template("quote.html", user = users[0]["username"])

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # ensure password was confirmed
        elif not request.form.get("confirm_password"):
            return apology("must confirm password")

        # check if passwords match
        elif request.form.get("password") != request.form.get("confirm_password"):
            return apology("passwords don't match")

        # encrypt password
        hash_pw = pwd_context.hash(request.form.get("password"))

        # insert username and password into users database
        insert = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
            username = request.form.get("username"), hash = hash_pw)

        # if username is taken, return apology
        if not insert:
            return apology("username already exists")
        else:
            rows = db.execute("SELECT * FROM users WHERE username = :username", username = request.form.get("username"))
            session["user_id"] = rows[0]["id"]
            return redirect(url_for("index"))

    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""

    users = db.execute("SELECT * FROM users WHERE id = :id", id = session["user_id"])

    if request.method == "POST":

        # get symbol and number of shares from user they want ot buy
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        if symbol == "" or shares == "":
            return apology("must enter symbol and number of shares")

        stock = lookup(symbol)
        if not stock:
            return apology("invalid symbol")

        # get current amount of user's cash
        user_current_cash = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])

        # get number of certain shares user owns
        user_current_shares = db.execute("SELECT Shares FROM portfolio WHERE id = :id AND Symbol = :symbol", id = session["user_id"], symbol = stock["symbol"])

        # calculate difference
        diff_shares = user_current_shares[0]["Shares"] - int(shares)

        # if user has more shares than he wants to sell, sell shares and update database
        if not diff_shares < 0:

            # calculate how much cash will user have after selling the shares
            diff_cash = user_current_cash[0]["cash"] + stock["price"] * int(shares)

            # update portfolio and users databases
            db.execute("UPDATE portfolio SET Shares = :diff_shares, TOTAL = :total WHERE id = :id AND Symbol = :symbol", diff_shares = diff_shares, total = stock["price"] * diff_shares, id = session["user_id"], symbol = stock["symbol"])
            db.execute("UPDATE users SET cash = :diff_cash WHERE id = :id", diff_cash = round(diff_cash, 2), id = session["user_id"])

            # delete if all shares are sold
            portfolio = db.execute("SELECT * FROM portfolio WHERE id = :id", id = session["user_id"])
            db.execute("DELETE FROM portfolio WHERE id = :id AND Shares = :shares", id = session["user_id"], shares = 0)

            # insert transaction into history database
            time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            db.execute("INSERT INTO history (id, Symbol, Shares, Price, Transacted) VALUES(:id, :Symbol, :Shares, :Price, :Transacted)",
                id = session["user_id"], Symbol = stock["symbol"], Shares = - int(shares), Price = round(stock["price"], 2), Transacted = time)

            return redirect(url_for("index"))
        else:
            return apology("you don't have enough shares!")
    else:
        return render_template("sell.html", user = users[0]["username"])

@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    """Make a deposit."""

    users = db.execute("SELECT * FROM users WHERE id = :id", id = session["user_id"])

    if request.method == "POST":

        cc_num = request.form.get("cc_num")
        amount = request.form.get("amount")
        if cc_num == "" or amount == "":
            return apology("must enter credit card number and amount")

        # check if credit card is valid
        sum1 = 0
        sum2 = 0
        i = int(cc_num)
        j = int(cc_num) // 10

        # implement Luhn algorothm
        while i > 0:
            sum1 += i % 10
            i //= 100

        while j > 0:
            if j % 10 * 2 < 9:
                sum2 += j % 10 * 2
            else:
                sum2 += (j % 10 * 2) // 10 + (j % 10 * 2) % 10
            j //= 100

        if (sum1 + sum2) % 10 == 0:
            if (int(cc_num) // 10000000000000 == 34 or int(cc_num) // 10000000000000 == 37) or (int(cc_num) // 100000000000000 > 50 and int(cc_num) // 100000000000000 < 56) or (int(cc_num) // 1000000000000 == 4 or int(cc_num) // 1000000000000000 == 4):

                user_current_cash = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])
                db.execute("UPDATE users SET cash = :amount WHERE id = :id", amount = user_current_cash[0]["cash"] + float(amount), id = session["user_id"])

                return redirect(url_for("index"))
        else:
                return apology("invalid credit card number")
    else:
        return render_template("deposit.html", user = users[0]["username"])