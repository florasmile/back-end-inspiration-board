from flask import abort, make_response
from ..db import db

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response = {"message": f"{cls.__name__} {model_id} is invalid"}
        abort(make_response(response, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        response = {"message": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))

    return model


def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
        
    except KeyError as e:
        response = {"message": f"Missed required field: {str(e)}"}
        abort(make_response(response, 400))
    except ValueError as e:
        response = {"message": str(e)}
        abort(make_response(response, 400))
    
    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201
