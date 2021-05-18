from app import app, db
from app.models import Company, Trade
from app.forms import AddCompanyForm, AddTradeForm
from datetime import datetime
from flask import render_template, url_for, flash, redirect, jsonify

@app.route('/')
def index():
    companies=Company.query.all()
    return render_template('index.html', companies=companies)

@app.route('/trade_history')
def trade_history():
    trades = Trade.query.all()
    return render_template('trades.html', trades=trades)

@app.route('/stock/trade_history/<ticker>')
def stock_history(ticker):
    company = Company.query.filter_by(ticker=ticker).first()
    trades = Trade.query.filter_by(company=company.id).all()
    return render_template('trades.html', trades=trades)

@app.route('/add_company', methods=['GET', 'POST'])
def add_company():
    form = AddCompanyForm()
    if form.validate_on_submit():
        company = Company(name=form.name.data)
        db.session.add(company)
        db.session.commit()
        flash('Company has been added.')
        return redirect(url_for('index'))
    return render_template('add_company.html', form=form)

@app.route('/add_trade', methods=['GET', 'POST'])
def add_trade():
    form = AddTradeForm()
    if form.validate_on_submit():
        company = Company.query.filter_by(name=str(form.company.data)).first()
        trade = Trade(shares=form.shares.data, company=company.id)
        db.session.add(trade)
        db.session.commit()
        flash('Trade has been added.')
        return redirect(url_for('index'))
    return render_template('add_company.html', form=form)