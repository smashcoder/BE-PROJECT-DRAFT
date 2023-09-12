from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Path to your CSV file
csv_path = 'AcademicEvent.csv'

# Load CSV data using pandas
df = pd.read_csv(csv_path)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form.get('keyword', '').lower()
        matches = df[df['Keywords'].str.lower().str.contains(keyword)]
        if matches.empty:
            result_message = "No matching results found. Please recheck if any other characters are used in the search bar or if there are any extra spaces."
            return render_template('index.html', result_message=result_message)
        else:
            result_entries = matches.to_dict(orient='records')
            return render_template('index.html', result_entries=result_entries)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
