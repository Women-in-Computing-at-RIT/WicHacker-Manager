import logging

from flask_restful import Resource
from flask import request
from utils.authentication import authenticate
from data.resume import uploadResume
from data.users import getUserIdFromAuthID

logger = logging.getLogger("Application")


class Resume(Resource):

    ALLOWED_EXTENSIONS = {'txt', 'pdf', '.doc', '.docx'}

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    PATH = '/user/resume'

    def post(self):
        authenticationPayload = authenticate(request.headers)
        if authenticationPayload is None:
            return {"message": "Authorization Header Failure"}, 401
        auth0_id = authenticationPayload['sub']
        userID = getUserIdFromAuthID(auth0_id)
        if userID is None:
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

