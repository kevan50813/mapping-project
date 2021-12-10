import matplotlib.pyplot as plt


def trilaterate_triplet(ap_triplet, distance_triplet):
    """ Given 3 access point locations and distances, calculates and outputs the expected user position

        :param ap_triplet: 2D array of 3 access points' locations, in the form [ [xpos1, ypos1], ... ]
        :param distance_triplet: Array of 3 access points' distances, in the form [ distance1, ... ]

        :return location: Array of the predicted user position
    """

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


def visualise_trilateration(ap_triplet, distance_triplet, location):
    """ Given 3 access point locations and distances, and the position of the user, visualises them using pyplot
        Note that the keys for the ap_triplet and distance_triplet dictionaries must be identical

        :param ap_triplet: 3-length dictionary of access points' locations, in the form { MAC: [xpos, ypos], ... }
        :param distance_triplet: 3-length dictionary of access points' distances, in the form { MAC: distance, ... }
        :param location: Array containing the predicted location of the user, in the form [xpos, ypos]
    """

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
        ax.add_patch(circle)

    # plot the user location
    ax.plot(location[0], location[1], 'x')

    plt.show()


if __name__ == "__main__":

    # sample data for quick dirty test
    ap_sample = {
        "REF_1": [25, 10],
        "REF_2": [40, 40],
        "REF_3": [10, 40]
    }

    distance_sample = {
        "REF_1": 20,
        "REF_2": 20,
        "REF_3": 30
    }

    # cast dicts to array for trilateration function
    location = trilaterate_triplet(list(ap_sample.values()), list(distance_sample.values()))
    visualise_trilateration(ap_sample, distance_sample, location)
