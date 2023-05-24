import logging

from flask_restful import Resource
from flask import request
from flask_restful_swagger_2 import swagger
from flask_restful_swagger_2 import Schema

from utils.authentication import authenticate
from data.resume import uploadResume, checkIfUserHasResume
from data.users import getUserIdFromAuthID
from utils.swagger import USERS_TAG

logger = logging.getLogger("Application")


class ResumeModel(Schema):
    type = 'object'
    properties = {
        'resume': {
            'type': 'file'
        }
    }


class Resume(Resource):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'jpg', 'png'}

    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    PATH = '/user/resume'

    @swagger.doc({
        'summary': "resume upload",
        'tags': [USERS_TAG],
        'description': 'Verify recaptcha',
        'consumes': ['multipart/form-data'],
        'parameters': [
            {
                'name': 'resume',
                'description': 'token generated by the recaptcha for verification',
                'required': True,
                'in': 'body',
                'schema': ResumeModel
            }
        ],
        'responses': {
            '200': {
                'description': 'recaptcha verified'
            },
            '400': {
                'description': 'recaptcha verification failure'
            }
        }
    })
    def post(self):
        authenticationPayload = authenticate(request.headers)
        if authenticationPayload is None:
            return {"message": "Authorization Header Failure"}, 401
        auth0_id = authenticationPayload['sub']
        userID = getUserIdFromAuthID(auth0_id)
        if userID is None:
            logger.error("Could not get user ID from auth ID")
            return {"message": "User Error"}, 500

        # Have to verify filename exists, if filename is empty file upload didn't work
        if 'resume' not in request.files or request.files['resume'].filename == '':
            return {"message": "Request Does Not Have Resume"}, 400

        resume = request.files['resume']
        if not (resume and self.allowed_file(resume.filename)):
            # resume doesn't exist or has wrong extension
            return {"message": "Resume File Format Not Accepted"}, 400
        uploadSuccessful = uploadResume(userID, resume, request.mimetype)
        if uploadSuccessful:
            return {"message": "Resume upload successful"}, 200
        else:
            return {"message": "Resume upload failure"}, 500

    @swagger.doc({
        'summary': "check if user has uploaded resume",
        'tags': [USERS_TAG],
        'description': "endpoint to determine if the hacker has previously uploaded a resume",
        'responses': {
            '200': {
                'description': 'hacker has uploaded resume'
            },
            '400': {
                'description': 'hacker has not uploaded resume'
            }
        }
    })
    def get(self):
        authenticationPayload = authenticate(request.headers)
        if authenticationPayload is None:
            return {"message": "Authorization Header Failure"}, 401
        auth0_id = authenticationPayload['sub']
        userID = getUserIdFromAuthID(auth0_id)
        if userID is None:
            return {"message": "User Error"}, 500

        if checkIfUserHasResume(userID):
            return {"message": "User has a resume uploaded"}, 200
        return {"message": "User has no resume uploaded"}, 400
