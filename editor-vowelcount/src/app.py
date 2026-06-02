from flask import Flask, request, jsonify
from flask_cors import CORS
from vowelCount import count_vowels

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def vowel_count():
    output = {
        "error": False,
        "string": "",
        "answer": 0,
        "details": {}
    }
    
    try:
        # Get text parameter, default to empty string if not provided
        text = request.args.get('text', '')
        
        # Validate input type
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        
        # Count vowels
        total_count, vowel_details = count_vowels(text)
        
        # Prepare output
        output["string"] = f"Contains {total_count} vowels"
        output["answer"] = total_count
        output["details"] = vowel_details
    
    except TypeError as te:
        output["error"] = True
        output["string"] = f"Type Error: {str(te)}"
    except Exception as e:
        output["error"] = True
        output["string"] = f"Unexpected Error: {str(e)}"
    
    return jsonify(output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)