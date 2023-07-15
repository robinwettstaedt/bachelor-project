from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Connection strings for the two databases
app.config['SQLALCHEMY_BINDS'] = {
    'eplf_db': 'postgresql://postgres:postgres@192.168.0.23:5432/db',
    'zd_db': 'postgresql://postgres:postgres@192.168.0.24:5432/db'
}

db = SQLAlchemy(app)

class EplfPayments(db.Model):
    __bind_key__ = 'eplf_db'
    __tablename__ = 'Payments' # name of your table
    id = db.Column(db.Integer, primary_key=True)

class EplfLog(db.Model):
    __bind_key__ = 'eplf_db'
    __tablename__ = 'Log' # name of your table
    id = db.Column(db.Integer, primary_key=True)

class ZdPayments(db.Model):
    __bind_key__ = 'zd_db'
    __tablename__ = 'Payments' # name of your table
    id = db.Column(db.Integer, primary_key=True)

class ZdLog(db.Model):
    __bind_key__ = 'zd_db'
    __tablename__ = 'Log' # name of your table
    id = db.Column(db.Integer, primary_key=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/eplf_payments')
def get_eplf_payments():
    payments = EplfPayments.query.all()
    return jsonify([payment.id for payment in payments])

@app.route('/api/eplf_logs')
def get_eplf_logs():
    logs = EplfLog.query.all()
    return jsonify([log.id for log in logs])

@app.route('/api/zd_payments')
def get_zd_payments():
    payments = ZdPayments.query.all()
    return jsonify([payment.id for payment in payments])

@app.route('/api/zd_logs')
def get_zd_logs():
    logs = ZdLog.query.all()
    return jsonify([log.id for log in logs])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
