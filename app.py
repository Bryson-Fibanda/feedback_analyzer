from flask import Flask, render_template, request, jsonify, session, flash, redirect, url_for
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename

from config import Config
from utils.file_processor import process_uploaded_file, allowed_file
from utils.analysis import analyze_feedback, generate_response_suggestions


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/analyze', methods=['POST'])
    def analyze_feedback_route():
        try:
            if 'file' not in request.files:
                return jsonify({'error': 'No file uploaded'}), 400

            file = request.files['file']
            analysis_type = request.form.get('analysis_type', 'basic')

            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400

            if file and allowed_file(file.filename):
                # Generate unique session ID for this analysis
                session_id = str(uuid.uuid4())
                session['analysis_id'] = session_id

                # Process uploaded file
                reviews = process_uploaded_file(file)

                if not reviews:
                    return jsonify({'error': 'No valid reviews found in file'}), 400

                # Perform analysis (NO TEXTBLOB - using our custom analyzer)
                analysis_results = analyze_feedback(reviews, analysis_type)
                analysis_results['total_reviews'] = len(reviews)
                analysis_results['analysis_id'] = session_id
                analysis_results['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Store results in session for later access
                session['last_analysis'] = analysis_results

                return jsonify(analysis_results)

            return jsonify({'error': 'Invalid file type. Please upload CSV or TXT files.'}), 400

        except Exception as e:
            return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

    @app.route('/generate-responses', methods=['POST'])
    def generate_responses():
        try:
            data = request.get_json()
            negative_reviews = data.get('negative_reviews', [])

            if not negative_reviews:
                return jsonify({'error': 'No negative reviews provided'}), 400

            responses = generate_response_suggestions(negative_reviews)
            return jsonify({'suggested_responses': responses})

        except Exception as e:
            return jsonify({'error': f'Response generation failed: {str(e)}'}), 500

    @app.route('/results')
    def results():
        analysis_data = session.get('last_analysis', {})
        return render_template('results.html', analysis=analysis_data)

    @app.route('/pricing')
    def pricing():
        return render_template('pricing.html')

    return app


if __name__ == '__main__':
    app = create_app()
    print("🚀 Feedback Analyzer Started Successfully!")
    print("✅ No external dependencies needed - 100% self-contained")
    app.run(debug=True)