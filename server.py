from flask import Flask, request, jsonify
import numpy as np
import cv2
from processes import recognize
# Initialize the Flask application
app = Flask(__name__)
# route http posts to this method
@app.route('/api/test', methods=['POST'])
def test():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    print ('server print: ', img.shape)
    name = recognize(img)
    return jsonify({'name':name})
# start flask app
server_ip = '0.0.0.0'
app.run(host=server_ip, port=8080, debug=True)