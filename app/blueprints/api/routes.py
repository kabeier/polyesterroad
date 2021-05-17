from .import bp as api
from flask import  request,jsonify
from app.blueprints.shop.models import Item

@api.route('/item', methods=['POST'])
def make_item():
    data=request.json
    for item in data:
        newitem=Item()
        newitem.from_dict(item)
        newitem.save()
    return jsonify(data), 201
