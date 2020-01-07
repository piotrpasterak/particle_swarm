from math import sin, cos, sqrt, atan2, radians
import json

# approximate radius of earth in km
R = 6373.0

def calculate_distance(latitude_source, longitude_source, latitude_destination, longitude_destination):
    source_radians_latitude = radians(latitude_source)
    source_radians_longitude = radians(longitude_source)

    destination_radians_latitude = radians(latitude_destination)
    destination_radians_longitude = radians(longitude_destination)

    dlon = destination_radians_longitude - source_radians_longitude
    dlat = destination_radians_latitude - source_radians_latitude

    a = sin(dlat / 2)**2 + cos(source_radians_latitude) * cos(destination_radians_latitude) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def sigmoid(x):
  return 1 / (1 + exp(-x))


with open('data/cites.json') as json_file:
    data = json.load(json_file)