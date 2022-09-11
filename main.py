from collections import namedtuple

from flask import Flask
from flask_restx import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

Beacon = namedtuple('Beacon', 'beacon_name charge_level department_id location_id mac_address')

beacons = [
    Beacon('IL00000001', 100, 1, 2, 'aa:bb:cc:dd:ee:f1'),
    Beacon('IL00000002', 100, 1, 3, 'aa:bb:cc:dd:ee:f2'),
]
parser = reqparse.RequestParser


@api.route('/api/v1/beacon/')
class BeaconList(Resource):
    def get(self):
        return beacons

    def post(self, beacon_id):
        beacons[beacon_id] = parser.parse_args()
        return beacons

        beacons.append(Beacon())


@api.route('/api/v1/beacon/<string:mac_addr>')
class BeaconDetail(Resource):
    def get(self, mac_addr):
        result = list(filter(lambda x: x.mac_address == mac_addr, beacons))
        if result:
            return result[0]._asdict(), 200
        else:
            return None, 404

    def delete(self, mac_addr):
        result = list(filter(lambda x: x.mac_address == mac_addr, beacons))
        if result:
            beacons.remove(result[0])
            return 200
        else:
            return 404

    def put(self, mac_addr, beacon_id=None):
        result = list(filter(lambda x: x.mac_address == mac_addr, beacons))
        if result:
            beacons[beacon_id] = parser.parse_args()

            beacons.append("Beacon: ")
            return 200
        else:
            return 404


if __name__ == '__main__':
    app.run(debug=True, port=5002)
