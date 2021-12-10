import matplotlib.pyplot as plt
import math


def trilaterate_triplet(ap_dict, distance_dict):
    """ Given 3 access point locations and distances, calculates and outputs the expected user position

    :param ap_dict: Dict of 3 access points' locations, in the form { MAC: [xpos1, ypos1], ... }
    :param distance_dict: Dict of 3 access points' distances, in the form { MAC: distance1, ... }

    :return location: Array of the predicted user position
    """

    # cast to array for easy access, keys do not matter here
    ap_triplet = list(ap_dict.values())
    distance_triplet = list(distance_dict.values())

    # extract values for clarity
    p1 = ap_triplet[0]
    p2 = ap_triplet[1]
    p3 = ap_triplet[2]

    r1 = distance_triplet[0]
    r2 = distance_triplet[1]
    r3 = distance_triplet[2]

    # -2*x1 + 2*x2
    a = -2*p1[0] + 2*p2[0]

    # -2*y1 + 2*y2
    b = -2*p1[1] + 2*p2[1]

    # r1^2 - r2^2 - x1^2 + x2^2 - y1^2 + y2^2
    c = r1**2 - r2**2 - p1[0]**2 + p2[0]**2 - p1[1]**2 + p2[1]**2

    # -2*x2 + 2*x3
    d = -2*p2[0] + 2*p3[0]

    # -2*y2 + 2*y3
    e = -2*p2[1] + 2*p3[1]

    # r2^2 - r3^2 - x2^2 + x3^2 - y2^2 + y3^2
    f = r2**2 - r3**2 - p2[0]**2 + p3[0]**2 - p2[1]**2 + p3[1]**2

    # return predicted user location
    return [(c*e - f*b)/(e*a - b*d), (c*d - a*f)/(b*d - a*e)]


def dist(p1, p2):
    """ Calculates distance between 2 points, each of the form [x, y]

    :param p1: point 1
    :param p2: point 2
    :return distance: the distance between the two points, as a float
    """

    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def approximate_error(ap_dict, distance_dict, location):
    """ Given the triplets and predicted location, approximate the crossover area of all 3 circles.
    This is then the error area - this can then be turned into a circle to give an easily measurable error metric

    :param ap_dict: Access point location triplet
    :param distance_dict: Access point distance triplet
    :param location: Predicted location of the user
    :return error: the radius of the approximated 'region of error'. -1 if circles do not overlap
    """

    # cast to array for easy access, keys do not matter here
    ap_triplet = list(ap_dict.values())
    distance_triplet = list(distance_dict.values())

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

    t1 = triangle_points[0]
    t2 = triangle_points[1]
    t3 = triangle_points[2]

    area = abs(0.5 * ((t2[0] - t1[0]) * (t3[1] - t1[1]) - ((t3[0] - t1[0]) * (t2[1] - t1[1]))))

    return math.sqrt(area / math.pi)


def visualise_trilateration(ap_triplet, distance_triplet, location, error):
    """ Given 3 access point locations and distances, and the position of the user, visualises them using pyplot
    Note that the keys for the ap_triplet and distance_triplet dictionaries must be identical

    :param ap_triplet: 3-length dictionary of access points' locations, in the form { MAC: [xpos, ypos], ... }
    :param distance_triplet: 3-length dictionary of access points' distances, in the form { MAC: distance, ... }
    :param location: Array containing the predicted location of the user, in the form [xpos, ypos]
    :param error: The radius of the circle of expected error
    """

    plt.axis('square')

    # setup axis to generic values
    fig, ax = plt.subplots()
    ax.set_xlim((0, 50))
    ax.set_ylim((0, 50))

    # iterate over both dictionaries in tandem
    for ap_key, distance_key in zip(ap_triplet, distance_triplet):

        # ensure keys are consistent across each triplet
        if ap_key != distance_key:
            print("ERR: Key mismatch in trilateration visualisation")
            return

        # create a circle from the data given
        ap_coord = ap_triplet[ap_key]
        distance = distance_triplet[distance_key]
        circle = plt.Circle((ap_coord[0], ap_coord[1]), distance, fill=False)

        # plot center of circle, and add it to the plot
        ax.plot(ap_coord[0], ap_coord[1], 'o')
        ax.annotate(ap_key, (ap_coord[0], ap_coord[1]), textcoords="offset points", xytext=(0, 10), ha="center")
        ax.add_patch(circle)

    # plot the user location
    ax.plot(location[0], location[1], 'x')

    if error > 0:
        error_circle = plt.Circle((location[0], location[1]), error, fill=False, color="red")
        ax.add_patch(error_circle)

    plt.show()

    print_representation(ap_triplet, distance_triplet, location, error)


def print_representation(ap_triplet, distance_triplet, location, error):
    """ Repr dump for attributes of trilateration ran

    :param ap_triplet
    :param distance_triplet
    :param location
    :param error
    """

    print("ACCESS POINT TRIPLET")

    # iterate over both dictionaries in tandem
    for ap_key, distance_key in zip(ap_triplet, distance_triplet):

        # ensure keys are consistent across each triplet
        if ap_key != distance_key:
            print("ERR: Key mismatch in trilateration representation")
            return

        print(f"{ap_key}: pos <{ap_triplet[ap_key][0]}, "
              f"{ap_triplet[ap_key][1]}>, dist {distance_triplet[distance_key]}")

    print(f"\nPREDICTED LOCATION: <{location[0]}, {location[1]}>")
    print(f"EXPECTED ERROR RADIUS: {error}")


if __name__ == "__main__":

    # sample data for quick dirty test
    ap_sample = {
        "REF_1": [25, 10],
        "REF_2": [40, 40],
        "REF_3": [10, 40]
    }

    distance_sample = {
        "REF_1": 25,
        "REF_2": 25,
        "REF_3": 25
    }

    pos = trilaterate_triplet(ap_sample, distance_sample)
    err = approximate_error(ap_sample, distance_sample, pos)
    visualise_trilateration(ap_sample, distance_sample, pos, err)
