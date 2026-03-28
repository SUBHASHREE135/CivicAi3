from flask import Flask, render_template, request, redirect
from collections import Counter
import json
import os

app = Flask(__name__)

complaints = []

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Form Page
@app.route('/form')
def form():
    return render_template('form.html')

# Submit
@app.route('/submit', methods=['POST'])
def submit():

    problem = request.form['problem']
    description = request.form['description']
    location = request.form['location']

    image = request.files.get('image')
    filename = ""

    if image and image.filename != "":
        filename = image.filename
        image.save(os.path.join('static', filename))

    complaints.append({
        'problem': problem,
        'description': description,
        'location': location,
        'image': filename
    })

    return redirect('/dashboard?success=1')

# Dashboard
@app.route('/dashboard')
def dashboard():
    problem_types = [c['problem'] for c in complaints]
    counts = Counter(problem_types)

    weights = {
        'Road': 3,
        'Water': 2,
        'Garbage': 1
    }

    scores = {p: counts[p] * weights[p] for p in counts}

    counts_json = json.dumps({
        "Road": counts.get("Road", 0),
        "Water": counts.get("Water", 0),
        "Garbage": counts.get("Garbage", 0)
    })

    return render_template(
        'dashboard.html',
        complaints=complaints,
        scores=scores,
        counts_json=counts_json
    )

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Render assigns the PORT
    app.run(host="0.0.0.0", port=port)
    