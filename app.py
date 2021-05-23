from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from yahoo_fin.stock_info import get_data
import logging

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Fund(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    weightage = db.Column(db.Float)

@app.route("/")
def home():
    fund_list = Fund.query.all()
    return render_template("index.html", fund_list=fund_list)

@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name")
    weightage = request.form.get("weightage")
    new_fund = Fund(name=name, weightage=weightage)
    # after adding, we can add the top 10 holdings and their percentages for this fund
    db.session.add(new_fund)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/update/<int:fund_id>", methods=["POST"])
def update(fund_id):
    
    if request.form.get("update_name") == '':
        raise TypeError("Please give proper name")
    else:
        update_name = request.form.get("update_name")

    if request.form.get("update_weightage") == '':
        raise TypeError("Please give proper weightage")
    else:
        update_weightage = request.form.get("update_weightage")
    

    update_fund = Fund(id=fund_id, name=update_name, weightage=update_weightage)
    fund = Fund.query.filter_by(id=fund_id).first()
    db.session.delete(fund)
    db.session.add(update_fund)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:fund_id>")
def delete(fund_id):
    fund = Fund.query.filter_by(id=fund_id).first()
    db.session.delete(fund)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/refresh/", methods=["get"])
def refresh():
    fund_list = Fund.query.all()

    ticker_list = []
    for each in fund_list:
        ticker_list.append(each.name)

    historical_datas = {}
    for ticker in ticker_list:
        historical_datas[ticker] = get_data(ticker)

    print(historical_datas['XLF'])
    #use historical_data to do math

    #### use a ticker list then get data for the entire portfolio
    # amazon_weekly= get_data("xlf", start_date=request.form.get("start_date"), end_date=request.form.get("end_date"), index_as_date = True, interval="1wk")

    return redirect(url_for("home"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)




