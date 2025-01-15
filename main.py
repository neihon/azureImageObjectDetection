from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify
import requests

load_dotenv()
apiKey = os.getenv("COMPUTER_VISION_API_KEY")
userRegion = os.getenv("API_REGION")
endpoint = os.getenv("COMPUTER_VISION_ENDPOINT")

app = Flask(__name__)

def parseUrl(data):
    if not data or "url" not in data:
        return None, "Invalid Request!", 400
    
    imgUrl = data["url"]
    if not imgUrl.lower().endswith((".jpeg", ".jpg", ".png")):
        return None, "Invalid Image Format!", 400
    
    return imgUrl, None, 200

def processImgData(imgUrl):
    headers = {
        'Ocp-Apim-Subscription-Key': apiKey,
        'Content-Type': 'application/json'
    }

    params = {
        'visualFeatures': 'Objects,Description'
    }
    
    body = {
        "url": imgUrl
    }

    try:
        response = requests.post(
            endpoint,
            headers=headers,
            params=params,
            json=body, 
            timeout= 30
        )
        
        response.raise_for_status()
        resReturn = response.json()
    
        detectedObj = resReturn.get("objects", [])
        descriptionObj = resReturn.get("description", {}).get("captions", [])
        
        return {
            'objects': detectedObj,
            'description': descriptionObj
        }, None
        
    except requests.exceptions.RequestException as e:
        return None, f"Error calling the Computer Vision API: {str(e)}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

@app.route('/process-img', methods=['POST'])
def processUrl():
    try:
        data = request.get_json()
        
        imgUrl, error_message, status_code = parseUrl(data)
        if error_message:
            return jsonify({"error": error_message}), status_code
        
        result, error_message = processImgData(imgUrl)
        if error_message:
            return jsonify({"error": error_message}), 500

        return jsonify({
            "url": imgUrl,
            "objects": result["objects"],
            "description": result["description"]
        }), 200

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)