from flask import abort, make_response


def valid_id(id):
    try:
        id = int(id)
    except ValueError as e:
        print(e)
        abort(400, 'Request must be a valid integer')
    return id


def valid_model(id, model):
    valid = model.query.get(id)
    if not valid:
        abort(make_response({"message": f" The id #{id} was not found"}, 404))
    return valid



def missing_fields(request_body, model):
    for field in model.required_fields:
        if field not in request_body:
            return {"details": f"Request body must include {field}."}
    return False

def check_request_body(request_body,model):
    for item in request_body:
        if item not in model.required_fields:    
            return {"details": f"{item} is not a valid field"}
    return False
        

