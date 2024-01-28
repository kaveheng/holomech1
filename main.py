from flask import Flask, request, jsonify
from indeterminatebeam import Beam, Support, PointLoadV, DistributedLoadV

app = Flask(__name__)

# Initialize an empty beam object
beam = None

@app.route('/setup_beam', methods=['POST'])
def setup_beam():
    global beam
    data = request.get_json()
    length = data['length']
    E = data['E']
    I = data['I']

    # Create the beam instance
    beam = Beam(length, E, I)

    # Add supports
    for support in data['supports']:
        beam.add_supports(Support(support['coord'], tuple(support['fixed'])))

    # Add loads
    for load in data['loads']:
        if load['type'] == 'point':
            beam.add_loads(PointLoadV(load['magnitude'], load['location']))
        elif load['type'] == 'distributed':
            beam.add_loads(DistributedLoadV(load['magnitude'], tuple(load['range'])))

    # Perform analysis
    beam.analyse()

    return jsonify({'message': 'Beam setup and analysis successful'})

@app.route('/get_shear_force', methods=['POST'])
def get_shear_force():
    data = request.get_json()
    x_positions = data['x_positions']
    shear_forces = [beam.get_shear_force(x) for x in x_positions]

    return jsonify({'shear_forces': shear_forces})

@app.route('/get_bending_moment', methods=['POST'])
def get_bending_moment():
    data = request.get_json()
    x_positions = data['x_positions']
    bending_moments = [beam.get_bending_moment(x) for x in x_positions]

    return jsonify({'bending_moments': bending_moments})

#if __name__ == '__main__':
    #app.run(debug=True)
