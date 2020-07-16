from flask import Flask, request
import boto3

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <form method="POST" enctype=multipart/form-data action="upload">
    <input type="file" name="myFile">
    <input type="submit">
    </form>
    '''

@app.route('/upload', methods=['POST'])
def upload():
    s3 = boto3.resource('s3')
    s3.Bucket('regform2020').put_object(Key='salar.png', Body=request.files['myFile'])

if __name__=='__main__':
    app.run(debug=True)
