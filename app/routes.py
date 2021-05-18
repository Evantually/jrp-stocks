from app import app, db
from app.models import Company, Trade, MarketOrder
from app.forms import AddCompanyForm, AddTradeForm, AddMarketOrderForm, MarketOrderFillForm
from datetime import datetime
from flask import render_template, url_for, flash, redirect, jsonify

@app.route('/')
def index():
    companies=Company.query.all()
    return render_template('index.html', companies=companies)

@app.route('/trade_history')
def trade_history():
    trades = Trade.query.all()
    return render_template('trades.html', name='All Trading History', trades=trades)

@app.route('/stock/trade_history/<ticker>')
def stock_history(ticker):
    company = Company.query.filter_by(ticker=ticker).first()
    trades = Trade.query.filter_by(company=company.id).all()
    return render_template('trades.html',name=f'{company.name} Trading History', trades=trades)

@app.route('/market_orders')
def market_orders():
    market_orders = MarketOrder.query.all()
    return render_template('market_orders.html',name='Market Orders', market_orders=market_orders)

@app.route('/order_confirmation/<shares>/<company>')
def order_confirmation(shares, company):
    return render_template('confirmation.html', shares=shares, company=company)

@app.route('/market_orders/<order_id>', methods=['GET', 'POST'])
def market_order(order_id):
    market_order = MarketOrder.query.filter_by(id=order_id).first()
    form = MarketOrderFillForm()
    form.shares.data = market_order.shares
    if market_order.shares > 0:
        order_type = 'buy'
    else:
        order_type = 'sell'
    if form.validate_on_submit():
        market_order.shares -= form.shares.data
        if market_order.shares == 0:
            db.session.delete(market_order)
        elif (order_type=='buy' and (market_order.shares < 0)) or (order_type=='sell' and (market_order.shares > 0)):
            flash('More shares are attempting to be exchanged than exist in this order.')
            return redirect(url_for('market_order', order_id=order_id))
        db.session.commit()
        return redirect(url_for('order_confirmation', shares=form.shares.data))
    return render_template('')

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

@app.route('/add_market_order', methods=['GET', 'POST'])
def add_market_order():
    form = AddMarketOrderForm()
    if form.validate_on_submit():
        company = Company.query.filter_by(name=str(form.company.data)).first()
        market_order = MarketOrder(shares=form.shares.data, company=company.id)
        db.session.add(market_order)
        db.session.commit()
        flash('Trade has been added.')
        return redirect(url_for('index'))
    return render_template('add_company.html', form=form)

@app.route('/add_trade', methods=['GET', 'POST'])
def add_trade():
    form = AddTradeForm()
    if form.validate_on_submit():
        company = Company.query.filter_by(name=str(form.company.data)).first()
        company.market_cap = form.share_price.data*company.shares_outstanding
        company.equity += (form.share_price.data - company.ipo_price) * form.shares.data
        company.price_earnings = company.market_cap / company.equity
        trade = Trade(shares=form.shares.data, company=company.id)
        db.session.add(trade)
        db.session.commit()
        flash('Trade has been added.')
        return redirect(url_for('index'))
    return render_template('add_company.html', form=form)