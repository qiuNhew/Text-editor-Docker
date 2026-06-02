from flask import Flask, request, jsonify
from flask_cors import CORS
from commaCount import comma_counting

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def comma_count():
    output = {
        "error": False,
        "string": "",
        "answer": 0,
        "details": {}
    }
    try:
        text = request.args.get('text', '')
        total_count = comma_counting(text)
        output["string"] = f"Contains {total_count} commas"
        output["answer"] = total_count
    except Exception as e:
        output["error"] = True
        output["string"] = f"Error processing request: {str(e)}"
    return jsonify(output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
