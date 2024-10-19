from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
from scipy.interpolate import griddata
import numpy as np

app = Flask(__name__)
app.secret_key = 'secretkey123'  # Secret key for session management (important for flashes)

# Load CSV data
df1 = pd.read_csv('data/freeness_data_consistency.csv')
df2 = pd.read_csv('data/freeness_data_temperature.csv')

# Extract freeness, consistency, and correction data from CSV
points1 = df1[['Freeness', 'Consistency']].values
values1 = df1['Correction'].values

# Extract freeness, temperature, and correction data from CSV
points2 = df2[['Freeness', 'Temperature']].values
values2 = df2['Correction'].values

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate_freeness():
    try:
        # Get input from form
        freeness_input = request.form['freeness']
        consistency_input = request.form['consistency']
        temperature_input = request.form['temperature']

        # Validasi input
        if not freeness_input or not consistency_input or not temperature_input:
            flash('All fields are required.', 'error')
            return redirect(url_for('index'))
        
        freeness_input = float(freeness_input)
        consistency_input = float(consistency_input)
        temperature_input = float(temperature_input)

        # Interpolasi menggunakan data dari CSV
        interpolated_value1 = griddata(points1, values1, [(freeness_input, consistency_input)], method='linear')
        interpolated_value2 = griddata(points2, values2, [(freeness_input, temperature_input)], method='linear')

        koreksi1 = interpolated_value1[0] if interpolated_value1 is not None and interpolated_value1.size > 0 else 0
        koreksi2 = interpolated_value2[0] if interpolated_value2 is not None and interpolated_value2.size > 0 else 0

        # Hitung freeness total
        freeness_total = freeness_input + koreksi1 + koreksi2

        # Redirect ke halaman hasil
        return render_template('result.html',
                               freeness_input=freeness_input,
                               consistency_input=consistency_input,
                               temperature_input=temperature_input,
                               correction_consistency=koreksi1,
                               correction_temperature=koreksi2,
                               freeness_total=freeness_total)

    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80, debug=True)
