from flask import Blueprint, request
from flask.json import jsonify
from src.db import db1
from bson import ObjectId
from flask_jwt_extended import  get_jwt_identity, jwt_required
from flasgger import swag_from
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED


templateRoutes = Blueprint("templateRoutes", __name__, url_prefix="/template")

@templateRoutes.route('/', methods=['POST'])
@jwt_required()
@swag_from('./docs/template/createTemplate.yaml')
def create_template():
    current_user = get_jwt_identity()

    template_name = request.json["template_name"]
    subject = request.json["subject"]
    body = request.json["body"]
   
    res = db1.insert_one({"template_name":template_name,"subject":subject,"body":body, "creator": current_user})
    return jsonify({
    'message': "Template created",
    

    }), HTTP_201_CREATED


@templateRoutes.route('/', methods=['GET'])
@jwt_required()
@swag_from('./docs/template/getAllTemplate.yaml')
def get_templates():
    current_user = get_jwt_identity()
    
    if request.method == "GET":
        templates =[]
        for i in db1.find():
            if i["creator"] == current_user:
                templates.append({"_ID":str(ObjectId(i["_id"])),"template_name":i["template_name"],"subject":i["subject"],"body":i["body"]})
        return jsonify(templates), HTTP_200_OK
   


@templateRoutes.route('/<id>',methods=["PUT"])
@jwt_required()
@swag_from('./docs/template/updateTemplate.yaml')
def update_template(id):
    current_user = get_jwt_identity()
   
    template = db1.find_one({"_id":ObjectId(id)})
    print(template["subject"])
    if not template:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND

    if template["creator"] == current_user:

        db1.update_one({"_id":ObjectId(id)},{"$set":{
            "template_name":request.json["template_name"],
            "subject":request.json["subject"],
            "body":request.json["body"]
        }})
        return jsonify({"message":"updated!"}), HTTP_200_OK
    return jsonify({'message': 'No access!'}), HTTP_401_UNAUTHORIZED



@templateRoutes.route('/<id>',methods=["DELETE"])
@jwt_required()
@swag_from('./docs/template/deleteTemplate.yaml')
def delete_template(id):
    current_user = get_jwt_identity()

    template = db1.find_one({"_id":ObjectId(id)})
    if not template:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND
    
    if template["creator"] == current_user:
    
        db1.delete_one({"_id":ObjectId(id)})
        return jsonify({"message":"deleted!"}), HTTP_200_OK
    return jsonify({'message': 'No access!'}), HTTP_401_UNAUTHORIZED

    
   


@templateRoutes.route('/<id>',methods=["GET"])
@jwt_required()
@swag_from('./docs/template/getTemplate.yaml')
def get_template(id):
    current_user = get_jwt_identity()
    
    template = db1.find_one({"_id":ObjectId(id)})

    if not template:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND
    
    if template["creator"] == current_user:
        return jsonify({
                            'message': 'Success',
                            'template': {
                                "_ID":str(ObjectId(template["_id"])),
                                "template_name":template["template_name"],
                                "subject":template["subject"],
                                "body":template["body"]
                            }

                        }), HTTP_200_OK
    return jsonify({'message': 'No access!'}), HTTP_401_UNAUTHORIZED
  
