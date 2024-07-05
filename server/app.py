from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from models import db, Plant  

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json_encoder = None

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/plants')
def get_plants():
    plants = [plant.to_dict() for plant in Plant.query.all()]
    return jsonify(plants)


@app.route('/plants', methods=['POST'])
def create_plant():
    data = request.get_json()
    new_plant = Plant(name=data['name'],image=data['image'],price=data['price'],is_in_stock=data.get('is_in_stock', True))
    db.session.add(new_plant)
    db.session.commit()
    return jsonify(new_plant.to_dict())

@app.route('/plants/<int:id>')
def plant(id):
    plant = Plant.query.get(id)
    if not plant:
        return jsonify({'error': 'Plant not found'})
    else:
        return jsonify(plant.to_dict())
        
@app.route('/plants/<int:id>', methods=['PATCH'])
def patch_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        return jsonify({'error': 'Plant not found'})
    
    data = request.get_json()
    for key, value in data.items():
        setattr(plant, key, value)
    db.session.commit()
    return jsonify(plant.to_dict()), 200


@app.route('/plants/<int:id>', methods=['DELETE'])
def delete_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        return jsonify({'error': 'Plant not found'})
    db.session.delete(plant)
    db.session.commit()
    return ''


if __name__ == '__main__':
    app.run(port=5555, debug=True)
