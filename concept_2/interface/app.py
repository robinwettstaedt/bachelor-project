from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, create_engine

app = Flask(__name__)

# Create SQLAlchemy engines
engine_eplf = create_engine('postgresql://postgres:postgres@192.168.0.23:5432/db')
engine_zd = create_engine('postgresql://postgres:postgres@192.168.0.24:5432/db')

@app.route('/')
def home():
    try:
        with engine_eplf.connect() as connection:
            result_eplf = connection.execute(text("SELECT COUNT(*) FROM Payments"))
            eplf_payment_data = result_eplf.fetchone()[0]

        with engine_zd.connect() as connection:
            result_zd = connection.execute(text("SELECT COUNT(*) FROM Payments"))
            zd_payment_data = result_zd.fetchone()[0]

        with engine_eplf.connect() as connection:
            result_eplf = connection.execute(text("SELECT COUNT(*) FROM Log"))
            eplf_log_data = result_eplf.fetchone()[0]

        with engine_zd.connect() as connection:
            result_zd = connection.execute(text("SELECT COUNT(*) FROM Log"))
            zd_log_data = result_zd.fetchone()[0]

        return render_template('index.html', eplf_payment_data=eplf_payment_data, zd_payment_data=zd_payment_data, eplf_log_data=eplf_log_data, zd_log_data=zd_log_data)
    except Exception as e:
        return str(e)

@app.route('/update_data')
def update_data():
    try:
        with engine_eplf.connect() as connection:
            result_eplf = connection.execute(text("SELECT COUNT(*) FROM Payments"))
            eplf_payment_data = result_eplf.fetchone()[0]

        with engine_zd.connect() as connection:
            result_zd = connection.execute(text("SELECT COUNT(*) FROM Payments"))
            zd_payment_data = result_zd.fetchone()[0]

        with engine_eplf.connect() as connection:
            result_eplf = connection.execute(text("SELECT COUNT(*) FROM Log"))
            eplf_log_data = result_eplf.fetchone()[0]

        with engine_zd.connect() as connection:
            result_zd = connection.execute(text("SELECT COUNT(*) FROM Log"))
            zd_log_data = result_zd.fetchone()[0]

        return jsonify({
            'eplf_payment_data': eplf_payment_data,
            'zd_payment_data': zd_payment_data,
            'eplf_log_data': eplf_log_data,
            'zd_log_data': zd_log_data
        })
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
