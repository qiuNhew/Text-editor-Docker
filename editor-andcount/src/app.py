from flask import Flask, request, jsonify
from flask_cors import CORS
from andCount import count_and_occurrences

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def get_and_count():
    output = {
        "error": False,
        "message": "",
        "total_ands": 0,
    }
    
    try:
        text = request.args.get('text')
        
        # Validate input
        if text is None:
            raise ValueError("No text parameter provided")
        
        # Ensure text is a string
        if not isinstance(text, str):
            raise TypeError("Text must be a string")
        
        # Count 'and' occurrences
        and_count = count_and_occurrences(text)
        
        # Create output message
        output["message"] = f"The text contains {and_count} 'and's"
        output["total_ands"] = and_count
    
    except ValueError as ve:
        output["error"] = True
        output["message"] = f"Input Error: {str(ve)}"
    except TypeError as te:
        output["error"] = True
        output["message"] = f"Type Error: {str(te)}"
    except Exception as error:
        output["error"] = True
        output["message"] = f"Unexpected Error: {str(error)}"
    
    return jsonify(output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)