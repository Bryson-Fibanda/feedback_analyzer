import csv
import io
from flask import current_app


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def process_uploaded_file(file):
    """Process uploaded CSV or TXT file and extract reviews"""
    reviews = []

    if file.filename.endswith('.csv'):
        # Read CSV file
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.reader(stream)

        for row in csv_reader:
            if row:  # Skip empty rows
                review_text = row[0] if len(row) > 0 else ''
                if len(review_text.strip()) >= current_app.config['MIN_REVIEW_LENGTH']:
                    reviews.append(review_text.strip())

    elif file.filename.endswith('.txt'):
        # Read TXT file
        content = file.stream.read().decode("UTF-8")
        lines = content.split('\n')

        for line in lines:
            line = line.strip()
            if line and len(line) >= current_app.config['MIN_REVIEW_LENGTH']:
                reviews.append(line)

    return reviews