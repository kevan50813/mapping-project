import matplotlib.pyplot as plt
from pygeodesy.sphericalNvector import LatLon, trilaterate
from pygeodesy.errors import IntersectionError


def trilaterate_triplet(ap_dict):
    """ Given 3 access point locations and distances, calculates and outputs the expected user position

    :param ap_dict: Dict of 3 access points' locations and distances from current location

    :return location: Array of the predicted user position
    """

    pos = []
    dist = []
    

    for key in ap_dict:

        location = ap_dict[key]
        pos.append(LatLon(location["latitude"], location["longitude"]))

        dist.append(ap_dict[key]["distance"])

    try:
        pos = trilaterate(pos[0], dist[0], pos[1], dist[1], pos[2], dist[2])
        return pos

    except IntersectionError:
        print("ERR: Supplied points do not intersect")
        # non-intersection
        return -1

    except (TypeError, ValueError):
        # error with values
        # TODO - handle this in a different way
        return -1

'''

TODO - needs updating for use with LatLon and the like
maybe pygeodesy has a better way to do this?

def approximate_error(ap_dict, ap_dict, location):
    """ Given the triplets and predicted location, approximate the crossover area of all 3 circles.
    This is then the error area - this can then be turned into a circle to give an easily measurable error metric

    :param ap_dict: Access point location + distance triplet
    :param location: Predicted location of the user
    :return error: the radius of the approximated 'region of error'. -1 if circles do not overlap
    """

    # cast to array for easy access, keys do not matter here
    ap_triplet = list(ap_dict.values())

    # the 3 points that make up the triangle bounding the intersection between the 3 circles
    triangle_points = []

    for index in range(3):

        r1 = distance_triplet[index]
        r2 = distance_triplet[(index + 1) % 3]

        p1 = ap_triplet[index]
        p2 = ap_triplet[(index + 1) % 3]

        d = dist(p1, p2)

        # if the circles are not overlapping, or one circle is fully contained in the other
        # we cant use this result, so discard
        if d > r1 + r2 or d == 0 or d < abs(r1 - r2):
            return -1

        # uses triangle calculations to get intersection points

        # a = r1^2 - r2^2 + d^2 / 2d
        a = (r1**2 - r2**2 + d**2) / (2 * d)

        # h = sqrt(r1^2 - a^2)
        h = math.sqrt(r1**2 - a**2)

        # the center of the intersection of the 2 circles
        mid_point = [p1[0] + (a * (p2[0] - p1[0])) / d,
                     p1[1] + (a * (p2[1] - p1[1])) / d]

        # in the extremely unlikely case that the 2 circles intersect at exactly one point
        if d == r1 + r2:
            triangle_points.append(mid_point)
            continue

        # finally, we can work on the intersections
        int1 = [mid_point[0] + (h * (p2[1] - p1[1]) / d),
                mid_point[1] - (h * (p2[0] - p1[0]) / d)]
        int2 = [mid_point[0] - (h * (p2[1] - p1[1]) / d),
                mid_point[1] + (h * (p2[0] - p1[0]) / d)]

        # finally, add the closest point to the target location to the triangle of points
        if dist(int1, location) < dist(int2, location):
            triangle_points.append(int1)
        else:
            triangle_points.append(int2)

    t1 = triangle_points[0]     # intersection of circle 1 and 2
    t2 = triangle_points[1]     # intersection of circle 2 and 3
    t3 = triangle_points[2]     # intersection of circle 3 and 1

    # get area of the triangle formed by the 3 points
    area = abs(0.5 * ((t2[0] - t1[0]) * (t3[1] - t1[1]) - ((t3[0] - t1[0]) * (t2[1] - t1[1]))))
    #print(f"Triangle area: {area}")

    # now take pairs of the points that make the triangle
    for index in range(3):

        # if we take the arc of the first 2 points, this will be an arc on circle 2
        # as they are intersections of 1+2 and 2+3
        p1 = triangle_points[index]
        p2 = triangle_points[(index + 1) % 3]
        chord = dist(p1, p2)
        r = distance_triplet[(index + 1) % 3]

        #print(f"r: {r}, p1: {p1}, p2: {p2}, dist: {dist(p1, p2)}")

        angle = math.acos(((2 * r**2) - chord**2) / (2 * r**2))

        #print(f"angle: {angle}, area: {r**2 * math.asin(chord / (2 * r)) - (chord / 4) * math.sqrt(4 * r**2 - chord**2)}")

        # add area of segment onto total area
        area += r**2 * math.asin(chord / (2 * r)) - (chord / 4) * math.sqrt(4 * r**2 - chord**2)

    return math.sqrt(area / math.pi)

'''
def visualise_trilateration(ap_dict, location, error):
    """ Given 3 access point locations and distances, and the position of the user, visualises them using pyplot
    Note that the keys for the ap_triplet and distance_triplet dictionaries must be identical

    X is longitude, Y is latitude

    :param ap_dict: 3-length dictionary of access points' locations and distances
    :param location: LatLon of the user's predicted position
    :param error: The radius of the circle of expected error
    """

    plt.axis('square')

    img = plt.imread("Map1.jpeg")
    fig, ax = plt.subplots()
    x = range(300)
    ax.imshow(img)
    ax.imshow(img, extent=[0,400,0,300])
    ax.plot(x,x, '--', linewidth=5, color='firebrick')

    # setup axis to generic values
    fig, ax = plt.subplots()
    fig.tight_layout()

    # keep track of maximum and minimum lon and lat found, for drawing
    max_lat = -999
    max_lon = -999
    min_lat = 999
    min_lon = 999

    # iterate over both dictionaries in tandem
    for key in ap_dict:

        max_lat = max(max_lat, ap_dict[key]["latitude"])
        max_lon = max(max_lon, ap_dict[key]["longitude"])
        min_lat = min(min_lat, ap_dict[key]["latitude"])
        min_lon = min(min_lon, ap_dict[key]["longitude"])

        # create a circle from the data given
        # TODO - convert distance into somethign meaningful. right now plot is in lat/lon, making dist useless
        circle = plt.Circle((ap_dict[key]["longitude"], ap_dict[key]["latitude"]), ap_dict[key]["distance"], fill=False)

        # plot center of circle, and add it to the plot
        ax.plot(ap_dict[key]["longitude"], ap_dict[key]["latitude"], 'o')
        ax.annotate(key, (ap_dict[key]["longitude"], ap_dict[key]["latitude"]),
            textcoords="offset points", xytext=(0, 10), ha="center")
        ax.add_patch(circle)

    # padding for around the APs, so they are not on the edge of the graph
    x_padding = (max_lon - min_lon) * 0.2
    y_padding = (max_lat - min_lat) * 0.2

    ax.set_xlim((min_lon - x_padding, max_lon + x_padding))
    ax.set_ylim((min_lat - y_padding, max_lat + y_padding))

    # plot the user location, if valid
    if type(location) is LatLon:
        ax.plot(location.lon, location.lat, 'x')


    # TODO - wait for new error calculation before plotting
    if error is not None and error > 0:
        error_circle = plt.Circle((location[0], location[1]), error, fill=False, color="red")
        ax.add_patch(error_circle)


    plt.show()


def print_representation(ap_dict, location, error):
    """ Repr dump for attributes of trilateration ran

    :param ap_dict
    :param location
    :param error
    """

    print("ACCESS POINT TRIPLET")

    # iterate over both dictionaries in tandem
    for ap_key in ap_dict:

        print(f"{ap_key}: LAT/LON <{ap_dict[ap_key]['longitude']}/"
              f"{ap_dict[ap_key]['latitude']}>, dist {ap_dict[ap_key]['distance']}")

    if type(location) is LatLon:
        print(f"\nPREDICTED LAT/LON: {location.lat}/{location.lon}")
    elif type(location) is int:
        print(f"\nPREDICTED LOCATION: {location}")
    
    if error is not None:
        print(f"EXPECTED ERROR AREA: {error**2 * math.pi}")
        print(f"EXPECTED ERROR RADIUS: {error}")


if __name__ == "__main__":

    # sample data for quick dirty test
    ap_sample = {
        "REF_1": {"ap_name": "ref1", "longitude": -1, "latitude": 1, "distance": 31 },
        "REF_2": {"ap_name": "ref2", "longitude": -1.0001, "latitude": 1, "distance": 30 },
        "REF_3": {"ap_name": "ref3", "longitude": -1, "latitude": 1.0001, "distance": 30 }
    }

    err = None
    pos = trilaterate_triplet(ap_sample)
    #err = approximate_error(ap_sample, pos)
    visualise_trilateration(ap_sample, pos, err)
    print_representation(ap_sample, pos, err)
