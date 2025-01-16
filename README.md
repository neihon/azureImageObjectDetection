Object detection and URL-based image analysis using the Microsoft Azure AI/Computer Vision API. The list of objects (and certainty of guess) are returned.

// You have to have an active microsoft Azure subscription in order to test the script. 
// The image has to be passed as a URL.

test api validity: curl -X POST -H "Ocp-Apim-Subscription-Key: YOUR_API_KEY" -H "Content-Type: application/json" -d '{"url": "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png"}' "https://computervisionprojectneihon.cognitiveservices.azure.com/vision/v3.2/analyze?visualFeatures=Objects,Description"


analyse image: curl -X POST -H "Content-Type: application/json" -d '{"url": "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png"}' http://127.0.0.1:5000/process-img

