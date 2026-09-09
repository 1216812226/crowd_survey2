from flask import Flask, render_template, request, redirect, send_file
from datetime import datetime
import pandas as pd
import os
import psycopg2
from io import BytesIO

app = Flask(__name__)


# =========================================================
# PostgreSQL database connection
# =========================================================

def get_db_connection():
    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL is not set.")

    return psycopg2.connect(database_url)


# =========================================================
# Create database table
# =========================================================

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id SERIAL PRIMARY KEY,
            submit_time TEXT,
            age TEXT,
            gender TEXT,
            Q1 TEXT,
            Q2 TEXT,
            Q3 TEXT,
            Q4 TEXT,
            Q5 TEXT,
            Q5_reason TEXT,
            Q6_add TEXT,
            Q7 TEXT,
            Q7_reason TEXT,
            Q10 TEXT,
            Q10_image TEXT,
            Q11 TEXT,
            Q12 TEXT,
            Q12_image TEXT,
            Q13 TEXT,
            Q14 TEXT,
            Q15 TEXT,
            Q16_reason TEXT
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


# =========================================================
# Save survey response to PostgreSQL
# =========================================================

def save_to_database(data):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO responses (
            submit_time,
            age,
            gender,
            Q1,
            Q2,
            Q3,
            Q4,
            Q5,
            Q5_reason,
            Q6_add,
            Q7,
            Q7_reason,
            Q10,
            Q10_image,
            Q11,
            Q12,
            Q12_image,
            Q13,
            Q14,
            Q15,
            Q16_reason
        )
        VALUES (
            %(submit_time)s,
            %(age)s,
            %(gender)s,
            %(Q1)s,
            %(Q2)s,
            %(Q3)s,
            %(Q4)s,
            %(Q5)s,
            %(Q5_reason)s,
            %(Q6_add)s,
            %(Q7)s,
            %(Q7_reason)s,
            %(Q10)s,
            %(Q10_image)s,
            %(Q11)s,
            %(Q12)s,
            %(Q12_image)s,
            %(Q13)s,
            %(Q14)s,
            %(Q15)s,
            %(Q16_reason)s
        )
    """, data)

    conn.commit()

    cur.close()
    conn.close()


# =========================================================
# Survey
# =========================================================

@app.route('/', methods=['GET', 'POST'])
def survey():

    if request.method == 'POST':

        data = {
            'submit_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'age': request.form.get('age'),
            'gender': request.form.get('gender'),
            'Q1': request.form.get('Q1'),
            'Q2': request.form.get('Q2'),
            'Q3': request.form.get('Q3'),
            'Q4': request.form.get('Q4'),
            'Q5': request.form.get('Q5'),
            'Q5_reason': ', '.join(request.form.getlist('Q5_reason')),
            'Q6_add': request.form.get('Q6_add'),
            'Q7': request.form.get('Q7'),
            'Q7_reason': request.form.get('Q7_reason'),
            'Q10': request.form.get('Q10'),
            'Q10_image': request.form.get('Q10_image'),
            'Q11': request.form.get('Q11'),
            'Q12': request.form.get('Q12'),
            'Q12_image': request.form.get('Q12_image'),
            'Q13': request.form.get('Q13'),
            'Q14': request.form.get('Q14'),
            'Q15': request.form.get('Q15'),
            'Q16_reason': request.form.get('Q16_reason'),
        }

        save_to_database(data)

        return redirect('/thankyou')

    return render_template('survey.html')


# =========================================================
# Thank you page
# =========================================================

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')


# =========================================================
# Admin page
# =========================================================

@app.route('/admin')
def admin():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM responses ORDER BY id DESC", conn)
    conn.close()

    if df.empty:
        return "No responses yet."

    return df.to_html(index=False, classes="table table-striped", border=1)


# =========================================================
# Export Excel
# =========================================================

@app.route('/export/excel')
def export_excel():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM responses ORDER BY id", conn)
    conn.close()

    if df.empty:
        return "No data found."

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Responses')

    output.seek(0)
    return send_file(
        output,
        as_attachment=True,
        download_name='responses.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


# =========================================================
# Initialize database
# =========================================================

try:
    init_db()
except Exception as e:
    print("Database initialization failed:")
    print(e)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
