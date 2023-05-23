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

