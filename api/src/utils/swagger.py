from enum import Enum
from flask_restful_swagger_2 import Schema

# Tags
USERS_TAG = "users"
EMAILS_TAG = "emails"
PERMISSIONS_TAG = "permissions"
DISCORD_TAG = "discord"
STATISTICS_TAG = "statistics"
APPLICATIONS_TAG = "applications"


# Response Models (request models built off reqparse)
class UserResponseModel(Schema):
    type = 'object'
    properties = {
        'user_id': {
            'type': 'integer'
        }
    }

class UserModel(Schema):
    type = 'object'
    properties = {
        'user_id': {
            'type': 'integer'
        },
        "first_name": {
            "type": "string"
        },
        "last_name": {
            "type": "string"
        },
        "email": {
            "type": "string"
        },
        "phone_number": {
            "type": "string"
        },
        "address_id": {
            "type": "integer"
        },
        "address1": {
            "type": "string"
        },
        "address2": {
            "type": "string"
        },
        "city": {
            "type": "string"
        },
        "subdivision": {
            "type": "string"
        },
        "country": {
            "type": "string"
        },
        "application_id": {
            "type": "integer"
        },
        "major": {
            "type": "string"
        },
        "level_of_study": {
            "type": "string"
        },
        "age": {
            "type": "integer"
        },
        "shirt_size": {
            "type": "string"
        },
        "has_attended_wichacks": {
            "type": "integer"
        },
        "has_attended_hackathons": {
            "type": "integer"
        },
        "is_virtual": {
            "type": "integer"
        },
        "sponsor_id": {
            "type": "integer"
        },
        "company_name": {
            "type": "string"
        },
        "university": {
            "type": "string"
        },
        "status": {
            "type": "string"
        },
        "bus_rider": {
            "type": "integer"
        },
        "bus_stop": {
            "type": "string"
        },
        "dietary_restrictions": {
            "type": "string"
        },
        "special_accommodations": {
            "type": "string"
        },
        "affirmed_agreements": {
            "type": "integer"
        },
        "gender": {
            "type": "string"
        },
        "allowMlhEmails": {
            "type": "integer"
        }
    }
