import pandas as pd
import boto3
import cv2 as cv
from botocore.exceptions import ClientError

def get_text(img):
        access_key_id = ""
        secret_access_key = ""
        client = boto3.client('rekognition', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key,region_name="ap-south-1")
        filename=img
        img='/home/ubuntu/flaskapp/static/'+filename
        photo1 = cv.imread(img)
        imgHeight, imgWidth, channels = photo1.shape

        with open(img, 'rb') as source_image:
            source_bytes = source_image.read()

        response = client.detect_text(
            Image={
                'Bytes': source_bytes
            })

        res_response=""

        for i in range(len(response['TextDetections'])):
            if 'ParentId' not in response['TextDetections'][i].keys():

                res_response=res_response+" "+response['TextDetections'][i]['DetectedText']
                dimensions = response['TextDetections'][i]['Geometry']['BoundingBox']
                boxWidth = dimensions['Width']
                boxHeight = dimensions['Height']
                boxLeft = dimensions['Left']
                boxTop = dimensions['Top']
                # Plotting points of rectangle
                start_point = (int(boxLeft * imgWidth), int(boxTop * imgHeight))
                end_point = (int((boxLeft + boxWidth) * imgWidth), int((boxTop + boxHeight) * imgHeight))
                # Drawing Bounding Box on the coordinates
                thickness = 2
                color = (36, 255, 12)
                photo1 = cv.rectangle(photo1, start_point, end_point, color, thickness)
                cv.imwrite("/home/ubuntu/flaskapp/static/result_"+filename,photo1)
                # cv2.imshow('Target Image', photo1)
                # cv2.waitKey(0)
        print(res_response)
        statement="success"
        return response, filename, res_response,statement
