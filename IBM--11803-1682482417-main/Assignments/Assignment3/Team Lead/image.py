from flask import *
import os
import ibm_boto3
from ibm_botocore.client import Config,ClientError

app=Flask(__name__)

@app.route('/')
def home():
    return render_template("homepage.html")

@app.route('/result')
def result():
    return render_template("output.html")

@app.route('/result1',methods=['POST','GET'])
def result1():
    if request.method == 'POST':
        f=request.files['image']
        basepath=os.path.dirname(__file__)
        #print(basepath)
        filepath=os.path.join(basepath,'uploads',f.filename)
        #print(filepath)
        f.save(filepath)
        
        COS_ENDPOINT = "https://s3.us-south.cloud-object-storage.appdomain.cloud"
        COS_API_KEY_ID = "uJFMT2wXD1jGQ5yhYZX-Ss__CI3yqYAxpgscL9lMJtCo"
        COS_INSTANCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/ae59ecb09e744614b12361ffc50fe6f0:96275ded-aeac-4088-a7b3-a460e9cd5517::"
        cos = ibm_boto3.client('s3',ibm_api_key_id=COS_API_KEY_ID,ibm_service_instance_id=COS_INSTANCE_CRN,config=Config(signature_version="oauth"),endpoint_url=COS_ENDPOINT)
        cos.upload_file(Filename=filepath,Bucket='jprabhu',Key='images.jpg')
        return "Image uploaded successfully"
    else:
          return "not uploaded"
    #return "Image uploaded successfully"
    #return filepath

if __name__=="__main__":
    app.run(debug=True,port=5000,host='0.0.0.0')
    

