from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for

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
    db.session.add(new_fund)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/update/<int:fund_id>", methods=["POST"])
def update(fund_id):
    update_name = request.form.get("update_name")
    update_weightage = request.form.get("update_weightage")
    update_fund = Fund(name=update_name, weightage=update_weightage)
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

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)