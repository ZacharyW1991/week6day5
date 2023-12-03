from . import api
from app import db
from app.models import Address
from flask import request
from .auth import basic_auth, token_auth



@api.route('/addresses', methods=['GET'])
def get_addresses():
    addresses=db.session.execute(db.select(Address)).scalars().all()
    return [address.to_dict() for address in addresses]

@api.route('/addresses/<id>', methods=['GET'])
def get_address(id):
    address=db.session.get(Address, id)
    if not address:
        return {'error': f"Address with and I.D. or {id} does not exist"}, 400
    return address.to_dict()

@api.route('/addresses', methods=['POST'])
def create_address():
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    data=request.json
    required_fields=['first_name', 'last_name', 'phone', 'address']
    missing_fields=[]
    for field in required_fields:
        if field not in data:    
            missing_fields.append(field)
    if missing_fields:
        return {'error': 'Your content-type must be application/json'}, 400
    first_name=data.get('first_name')
    last_name=data.get('last_name')
    phone=data.get('phone')
    address=data.get('address')
    new_address=Address(first_name=first_name, last_name=last_name, phone=phone, address=address)
    db.session.add(new_address)
    db.session.commit()
    return new_address.to_dict(), 201  