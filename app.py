from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from yahoo_fin.stock_info import get_data

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

@app.route("/refresh/?start_date=<string:start_date>&end_date=<string:end_date>", methods=["POST"])
def refresh():
    for all in Fund.query.all():
        print(all)
    # amazon_weekly= get_data("xlf", start_date=request.form.get("start_date"), end_date=request.form.get("end_date"), index_as_date = True, interval="1wk")
    # ticker_list = ["SPY", "IUSV", "XLR"]
    # historical_datas = {}
    # for ticker in ticker_list:
    #     historical_datas[ticker] = get_data(ticker)

    #### use a ticker list then get data for the entire portfolio

    # refresh based on the start and end date, using this df to come up with a total returns value or chart first
    # amazon_weekly= get_data("xlf", start_date=start_date, end_date=end_date, index_as_date = True, interval="1wk")
    # print(amazon_weekly)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)




