from flask import Flask, render_template, jsonify
import requests
import random
import time
import smtplib
import threading
from email.mime.text import MIMEText
import logging
from datetime import datetime
import json
import os

class MonitoringService:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_logging()
        self.load_config()
        self.service_status = {}
        self.performance_metrics = {}
        self.setup_routes()
        
        # Start monitoring thread
        self.monitoring_thread = threading.Thread(target=self.periodic_monitoring, daemon=True)
        self.monitoring_thread.start()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)

    def load_config(self):
        try:
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
            with open(config_path, 'r') as file:
                self.config = json.load(file)
        except Exception as e:
            self.logger.error(f"Error loading config: {str(e)}")
            self.config = {}

    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html',
                                service_status=self.service_status,
                                performance_metrics=self.performance_metrics)

        @self.app.route('/api/status')
        def get_status():
            return jsonify({
                'service_status': self.service_status,
                'performance_metrics': self.performance_metrics
            })

    def generate_test_text(self):
        # Generate random text with known characteristics for testing
        words = ['and', 'test', 'comma,', 'deed', 'vowel', 'python']
        return ' '.join(random.choices(words, k=10))

    def calculate_expected_results(self, text):
        return {
            'wordcount': len(text.split()),
            'charcount': len(text),
            'andcount': text.lower().count('and'),
            'commacount': text.count(','),
            'palindromecount': sum(1 for word in text.split() 
                                 if word.lower() == word.lower()[::-1]),
            'vowelcount': sum(1 for char in text.lower() 
                            if char in 'aeiou')
        }

    def test_service(self, service_name, url):
        test_text = self.generate_test_text()
        expected = self.calculate_expected_results(test_text)
        
        try:
            start_time = time.time()
            response = requests.get(f"{url}/?text={test_text}", timeout=5)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                actual_count = result.get('count', 0)
                is_accurate = abs(actual_count - expected[service_name]) <= 1
                
                return {
                    'status': 'up',
                    'accurate': is_accurate,
                    'response_time': response_time,
                    'last_checked': datetime.now().isoformat(),
                    'expected': expected[service_name],
                    'actual': actual_count
                }
            else:
                return {
                    'status': 'error',
                    'accurate': False,
                    'response_time': response_time,
                    'last_checked': datetime.now().isoformat(),
                    'error': f'HTTP {response.status_code}'
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'status': 'down',
                'accurate': False,
                'response_time': None,
                'last_checked': datetime.now().isoformat(),
                'error': str(e)
            }

    def send_alert_email(self, service_name, status):
        # Email settings are read from environment variables so no credentials
        # are stored in source. See editor-monitoring/README.md / .env.example.
        SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
        SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
        SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
        SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")
        RECIPIENT_EMAIL = os.environ.get("RECIPIENT_EMAIL", SENDER_EMAIL)

        if not (SENDER_EMAIL and SENDER_PASSWORD and RECIPIENT_EMAIL):
            self.logger.warning(
                "Email alert skipped: SENDER_EMAIL / SENDER_PASSWORD / "
                "RECIPIENT_EMAIL not configured in the environment."
            )
            return

        try:
            msg = MIMEText(
                f"Service {service_name} is {status['status']}.\n"
                f"Error: {status.get('error', 'N/A')}\n"
                f"Time: {status['last_checked']}"
            )
            msg['Subject'] = f"Alert: {service_name} service {status['status']}"
            msg['From'] = SENDER_EMAIL
            msg['To'] = RECIPIENT_EMAIL

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.send_message(msg)
                
            self.logger.info(f"Alert email sent for {service_name}")
        except Exception as e:
            self.logger.error(f"Failed to send alert email: {str(e)}")

    def periodic_monitoring(self):
        while True:
            for service_name, url in self.config.items():
                service_name = service_name.replace('URL', '').lower()
                status = self.test_service(service_name, url)
                
                # Store the results
                self.service_status[service_name] = status
                
                # Store performance metrics
                if status['response_time'] is not None:
                    if service_name not in self.performance_metrics:
                        self.performance_metrics[service_name] = []
                    self.performance_metrics[service_name].append({
                        'timestamp': status['last_checked'],
                        'response_time': status['response_time']
                    })
                    # Keep only last 100 measurements
                    self.performance_metrics[service_name] = \
                        self.performance_metrics[service_name][-100:]
                
                # Send alert if service is down or inaccurate
                if status['status'] != 'up' or not status['accurate']:
                    self.send_alert_email(service_name, status)
            
            # Wait for 5 minutes before next check
            time.sleep(60)

    def run(self, host='0.0.0.0', port=80, debug=False):
        self.app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    service = MonitoringService()
    service.run(debug=True)