from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

COUNTRIES = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
]

CURRENCIES = ["USD", "EUR", "INR", "GBP", "JPY"]
RISK_AREAS = [
    "Advisory services", "Support Teams", "Operation teams", "Trading Desk - Equity", "Derivatives", "Fixed Income", "Client reporting teams", "Vendor", "Third Party"
]
EVENT_TYPES = ["Loss Event", "Near miss"]
IMPACT_RATINGS = ["Financial Impact", "Reputational Impact"]
RISK_RESPONSES = ["Accept", "Mitigate", "Transfer", "Avoid", "Not yet determined"]
ROOT_CAUSES = ["People", "Process", "Systems", "External Events", "Other", "NA"]

CSV_FILE = 'submissions.csv'

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        data = request.form.to_dict()
        # Ensure only the expected fields are included and in the right order
        expected_fields = [
            'entered_by', 'email', 'event_start_date', 'event_end_date', 'reported_date',
            'reported_by', 'originating_department', 'sub_department', 'event_description_details',
            'risk_area', 'event_type', 'country_of_occurrence', 'financial_impact', 'currency',
            'impact_rating', 'taxonomy', 'risk_response', 'root_cause_category', 'file'
        ]
        file = request.files.get('file')
        filename = ''
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data['file'] = filename
        # Fill missing keys with empty string to avoid KeyError
        for key in expected_fields:
            if key not in data:
                data[key] = ''
        # Save to CSV
        save_to_csv({k: data[k] for k in expected_fields})
        flash('Form submitted successfully!', 'success')
        return redirect(url_for('form'))
    return render_template('form.html', countries=COUNTRIES, currencies=CURRENCIES, risk_areas=RISK_AREAS, event_types=EVENT_TYPES, impact_ratings=IMPACT_RATINGS, risk_responses=RISK_RESPONSES, root_causes=ROOT_CAUSES)

def save_to_csv(data):
    fieldnames = [
        'entered_by', 'email', 'event_start_date', 'event_end_date', 'reported_date',
        'reported_by', 'originating_department', 'sub_department', 'event_description_details',
        'risk_area', 'event_type', 'country_of_occurrence', 'financial_impact', 'currency',
        'impact_rating', 'taxonomy', 'risk_response', 'root_cause_category', 'file'
    ]
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)


if __name__ == '__main__':
    app.run(debug=True)
