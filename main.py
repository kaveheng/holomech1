from flask import Flask, request, jsonify
from indeterminatebeam import Beam, Support, PointLoadV, DistributedLoadV

app = Flask(__name__)

# Global variable to store the beam instance
beam_instance = None

@app.route('/setup_beam', methods=['POST'])
def setup_beam():
    global beam_instance
    data = request.get_json()

    # Extract beam properties and loads from the request
    length = data['length']
    E = data['E']
    I = data['I']
    supports = data['supports']
    loads = data['loads']

    # Initialize the beam
    beam_instance = Beam(length, E, I)

    # Add supports
    for support in supports:
        beam_instance.add_support(Support(coord=support['coord'], fixed=support['fixed']))

    # Add loads
    for load in loads:
        if load['type'] == 'point':
            beam_instance.add_load(PointLoadV(load['magnitude'], load['location']))
        elif load['type'] == 'distributed':
            beam_instance.add_load(DistributedLoadV(load['magnitude'], load['range']))

    return jsonify({'message': 'Beam setup successful'})

@app.route('/get_shear_force', methods=['POST'])
def get_shear_force():
    data = request.get_json()
    x_positions = data['x_positions']
    shear_forces = [beam_instance.get_shear_force(x) for x in x_positions]

    return jsonify({'shear_forces': shear_forces})

@app.route('/get_bending_moment', methods=['POST'])
def get_bending_moment():
    data = request.get_json()
    x_positions = data['x_positions']
    bending_moments = [beam_instance.get_bending_moment(x) for x in x_positions]

    return jsonify({'bending_moments': bending_moments})

#if __name__ == '__main__':
    #app.run(debug=True)
