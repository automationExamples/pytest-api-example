import uuid
from flask import Flask, request
from flask_restx import Api, Resource, fields, Namespace

app = Flask(__name__)
api = Api(app, version='1.0', title='Petstore API',
          description='A simple Petstore API')

# Enums
PET_STATUS = ['available', 'sold', 'pending']
PET_TYPE = ['cat', 'dog', 'fish']

# Models
pet_model = api.model('Pet', {
    'id': fields.Integer(description='The pet ID'),
    'name': fields.String(required=True, description='The pet name'),
    'type': fields.String(required=True, description='The pet type', enum=PET_TYPE),
    'status': fields.String(description='The pet status', enum=PET_STATUS)
})

order_model = api.model('Order', {
    'id': fields.String(readonly=True, description='The order ID'),
    'pet_id': fields.Integer(required=True, description='The ID of the pet')
})

order_update_model = api.model('OrderUpdate', {
    'status': fields.String(description='The pet status', enum=PET_STATUS)
})

# Namespaces
pet_ns = Namespace('pets', description='Pets operations')
store_ns = Namespace('store', description='Store operations')

api.add_namespace(pet_ns)
api.add_namespace(store_ns)

# In-memory data storage
pets = [
    {
        'id': 0, 'name': 'snowball', 'type': 'cat', 'status': 'available'
    },
    {
        'id': 1, 'name': 'ranger', 'type': 'dog', 'status': 'pending'
    },
    {
        'id': 2, 'name': 'flippy', 'type': 'fish', 'status': 'available'
    }
]

orders = {
'1': {
        'pet_id': 1, 'name': 'snowball', 'type': 'cat', 'status': 'available'
    }
}


'''
Pet Namespace
'''
# Get a list of all pets


@pet_ns.route('/')
class PetList(Resource):
    @pet_ns.doc('list_pets')
    @pet_ns.marshal_list_with(pet_model)
    def get(self):
        """List all pets"""
        return pets

    @pet_ns.doc('create_pet')
    @pet_ns.expect(pet_model)
    @pet_ns.response(409, 'Pet already exists')
    @pet_ns.marshal_with(pet_model, code=201)
    def post(self):
        """Create a new pet"""
        pet = api.payload
        for i in pets:
            if i['id'] == pet['id']:
                api.abort(409, f"Pet with ID {pet['id']} already exists")
        pets.append(pet)
        return pet, 201

@pet_ns.route('/<int:pet_id>')
@pet_ns.response(404, 'Pet not found')
@pet_ns.param('pet_id', 'The pet identifier')
class Pet(Resource):
    @pet_ns.doc('get_pet')
    @pet_ns.marshal_with(pet_model)
    def get(self, pet_id):
        """Fetch a pet by id"""
        pet = next((pet for pet in pets if pet['id'] == pet_id), None)
        if pet is not None:
            return pet
        api.abort(404, f"Pet with ID {pet_id} not found")

@pet_ns.route('/findByStatus')
@pet_ns.param('status', 'The status of the pets to find')
class PetFindByStatus(Resource):
    @pet_ns.doc('find_pets_by_status')
    @pet_ns.marshal_list_with(pet_model)
    def get(self):
        """Find pets by status"""
        status = request.args.get('status')
        if status not in PET_STATUS:
            api.abort(400, 'Invalid pet status {status}')
        if status:
            filtered_pets = [pet for pet in pets if pet['status'] == status]
            return filtered_pets
        
# Store Namespace
@store_ns.route('/order')
class OrderResource(Resource):
    @store_ns.doc('place_order')
    @store_ns.expect(order_model)
    @store_ns.marshal_with(order_model, code=201)
    def post(self):
        """Place a new order"""
        order_data = api.payload
        pet_id = order_data.get('pet_id')
        pet = next((pet for pet in pets if pet['id'] == pet_id), None)

        if pet is None:
            api.abort(404, f"No pet found with ID {pet_id}")
        
        if pet['status'] != 'available':
            api.abort(400, f"Pet with ID {pet_id} is not available for order")

        # Update pet status to pending
        pet['status'] = 'pending'

        # Create and store the order
        order_id = str(uuid.uuid4())
        order_data['id'] = order_id
        orders[order_id] = order_data
        return order_data, 201

@store_ns.route('/order/<string:order_id>')
@store_ns.response(404, 'Order not found')
@store_ns.response(400, 'Invalid status')
@store_ns.param('order_id', 'The order identifier')
class OrderUpdateResource(Resource):
    @store_ns.doc('update_order')
    @store_ns.expect(order_update_model)
    def patch(self, order_id):
        
        """Update an existing order"""
        if order_id not in orders:
            api.abort(404, "Order not found")

        update_data = request.json
        order = orders[order_id]
        print('orderx ',order)
        pet_id = order['pet_id']

        

        pet = next((pet for pet in pets if pet['id'] == pet_id), None)

        print("petxx :" , pet)

        if pet is None:
            api.abort(404, f"No pet found with ID {pet_id}")

        # Update the order status
        order['status'] = update_data['status']

        # Update the pet's status based on the order's new status
        if update_data['status'] == 'pending':
            pet['status'] = 'pending'
        elif update_data['status'] == 'sold':
            pet['status'] = 'sold'
        else:
            api.abort(400, f"Invalid status '{update_data['status']}'. Valid statuses are {', '.join(PET_STATUS)}")


        return {"message": "Order and pet status updated successfully"}

if __name__ == '__main__':
    app.run(debug=True)
