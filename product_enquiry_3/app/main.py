from flask import Flask, request, render_template, jsonify
import logging
from log import setup_logging

app = Flask(__name__)

# Setup logging
setup_logging()

# List to store form submissions
submissions = []

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        product = request.form.get('product')
        message = request.form.get('message')

        # Store the submission in the list
        submission = {'name': name, 'email': email, 'product': product, 'message': message}
        submissions.append(submission)

        # Log the submission
        logging.info(f'Form submitted: {submission}')

        return render_template('submit.html', name=name, email=email, product=product, message=message)
    except Exception as e:
        logging.error(f'Error processing form: {e}')
        return 'There was an error processing your form submission.', 500

@app.route('/submissions', methods=['GET'])
def get_submissions():
    return jsonify(submissions)

@app.route('/api/submit', methods=['POST'])
def api_submit():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        product = data.get('product')
        message = data.get('message')

        # Store the submission in the list
        submission = {'name': name, 'email': email, 'product': product, 'message': message}
        submissions.append(submission)

        # Log the submission
        logging.info(f'Form submitted via API: {submission}')

        return jsonify({'message': 'Form submitted successfully'}), 200
    except Exception as e:
        logging.error(f'Error processing API submission: {e}')
        return jsonify({'error': 'There was an error processing your submission'}), 500

if __name__ == '__main__':
    app.run(debug=True)
