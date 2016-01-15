import os
import uuid
import cv2
import sys
from flask import Flask, request, redirect, url_for, send_from_directory, Response, jsonify
from werkzeug import secure_filename
import yaml
import shuffle_cv
import score

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/score')
def get_score():
    with open('current_score.yaml', 'r') as f:
	#return Response(f.read(), mimetype='application/json')
        score = yaml.load(f)
	return jsonify(**score)

#def find_pucks(imagePath):
#    cascPath = 'haarcascade_frontalface_default.xml'
#    
#    # Create the haar cascade
#    faceCascade = cv2.CascadeClassifier(cascPath)
#    
#    # Read the image
#    image = cv2.imread(imagePath)
#    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#    
#    # Detect faces in the image
#    faces = faceCascade.detectMultiScale(
#        gray,
#        scaleFactor=1.1,
#        minNeighbors=5,
#        minSize=(30, 30),
#        flags = cv2.CASCADE_SCALE_IMAGE
#    )
#    
#    print "Found {0} faces!".format(len(faces))
#    return faces

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = str(uuid.uuid4()) + secure_filename(file.filename)
            output_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(output_file)
            shuffle_cv.mask_for_blue(output_file)
            blue_pucks = shuffle_cv.find_pucks('static/img/blue.jpg')
            open('cheatsheet.yaml', 'r') as f:
              params = yaml.load(f)
            res = score.score(params['wall'], blue_pucks, [])
            with open('current_score.yaml', 'w') as f:
              f.write('red: 0\n')
              f.write('blue: %d\n'.format(res))
            return str(res)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/html/<path:path>')
def send_html(path):
    return send_from_directory('static/html', path)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)


