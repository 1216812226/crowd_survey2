from flask import Flask, render_template, request, redirect, send_file
from datetime import datetime
import pandas as pd
from pathlib import Path

app = Flask(__name__)

EXCEL_FILE = "responses.xlsx"


def save_to_excel(data):
    new_row = pd.DataFrame([data])

    if Path(EXCEL_FILE).exists():
        df = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df, new_row], ignore_index=True)
    else:
        df = new_row

    df.to_excel(EXCEL_FILE, index=False)


@app.route('/', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':

        data = {
            'submit_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'age': request.form.get('age'),
            'gender': request.form.get('gender'),
            'Q1': request.form.get('Q1'),
            'Q2': ', '.join(request.form.getlist('Q2')),
            # 'Q2reason': request.form.get('Q2reason'),
            # 'Q3': ', '.join(request.form.getlist('Q3')),
            # 'Q3add': request.form.get('Q3add'),
            # 'Q4': ', '.join(request.form.getlist('Q4')),
            # 'Q4add': request.form.get('Q4add'),
            'Q3': ', '.join(request.form.getlist('Q3')),
            # 'Q3add': request.form.get('Q3add'),
            # 'Q6': request.form.get('Q6'),
            'Q4': ', '.join(request.form.getlist('Q4')),
            # 'Q4reason': request.form.get('Q4reason'),
            'Q5': request.form.get('Q5'),
            'Q5_reason': ', '.join(request.form.getlist('Q5_reason')),
            # 'Q9_rank_1': request.form.get('Q9_rank_1'),
            # 'Q9_rank_2': request.form.get('Q9_rank_2'),
            # 'Q9_rank_3': request.form.get('Q9_rank_3'),
            # 'Q9_rank_4': request.form.get('Q9_rank_4'),
            'Q6_add': request.form.get('Q6_add'),
            'Q7': request.form.get('Q7'),
            'Q8': request.form.get('Q8'),
            'Q9': ', '.join(request.form.getlist('Q9')),
            'Q9reason': request.form.get('Q9reason'),
            # 'Q13': request.form.get('Q13'),
            'Q10': request.form.get('Q10'),
            'Q10_image': request.form.get('Q10_image'),
            'Q10_reason': request.form.get('Q10_reason'),
            'Q11': request.form.get('Q11'),
            'Q12': request.form.get('Q12'),
            'Q12_image': request.form.get('Q12_image'),
            # 'Q12_reason': request.form.get('Q12_reason'),
            'Q13': request.form.get('Q13'),
            'Q14': request.form.get('Q14'),
            # 'Q14_reason': request.form.get('Q14_reason'),
            'Q15': request.form.get('Q15'),
            'Q16_reason': request.form.get('Q16_reason'),
        }

        save_to_excel(data)

        return redirect('/thankyou')

    return render_template('survey.html')


@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')


@app.route('/admin')
def admin():

    if not Path(EXCEL_FILE).exists():
        return "No responses yet."

    df = pd.read_excel(EXCEL_FILE)

    return df.to_html(index=False)


@app.route('/export/excel')
def export_excel():

    if not Path(EXCEL_FILE).exists():
        return "No data found."

    return send_file(
        EXCEL_FILE,
        as_attachment=True,
        download_name='responses.xlsx'
    )


if __name__ == '__main__':

    app.run(debug=True)

    # import os
    #
    # port = int(os.environ.get("PORT", 5000))
    #
    # app.run(
    #     host="0.0.0.0",
    #     port=port,
    #     debug=False
    # )