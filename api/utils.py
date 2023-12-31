from rest_framework.views import exception_handler
from datetime import datetime
import ast
import re

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        error_types = list(response.data.keys())  # Create a copy of the keys
        errors = []
        for key in error_types:
            error_title = ""
            print("Respone data: ", response.data[key])
            if type(response.data[key]) != list:
                error_title = response.data[key].title()
            else:
                if type(response.data[key][0]) == dict and response.data[key][0].get('message'):
                    error_title = response.data[key][0].get('message').title()
                else:
                    error_title = response.data[key][0].title()
            
            if '[' in error_title:
                error_description = ast.literal_eval(error_title)
                errors.append({key: ' '.join([e for e in error_description])})
            else:
                errors.append({key: error_title})
            
            del response.data[key]
        
        response.data['errors'] = errors
        response.data['success'] = False
        response.data['time'] = datetime.now()

    return response


def in_restricted_paths(restricted_paths, path):
    for restricted_path in restricted_paths:
        if re.search(restricted_path, path, re.IGNORECASE):
            return True
    return False