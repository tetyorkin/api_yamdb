from rest_framework.exceptions import APIException 

class UniqueReviewException(APIException):
    status_code = 400
    default_detail = 'Unable to duplicate review.'
    default_code = 'Unable_to_duplicate_review'