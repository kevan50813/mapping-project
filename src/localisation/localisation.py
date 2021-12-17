import subprocess as sp
import math

from AP_parser import AP_Parser

OFFLINE = True
OFFLINE_PATH = "readings/studyroom_r1.csv"
AP_DATA_PATH = "Wifi_Nodes.json"
PRINT_REPR = False

class Localisation:

    def __init__(self):

        # dict will store networks in the following dict format:
        # { MAC_ADDRESS: {quality: <>, RSSI: <>, distance: <>, SSID: <>) }
        # Quality is not required - a value of -1 means quality was not obtained
        # SSID is also not required, but kept for reference
        self.network_dict = {}

        # list of networks in the building from AP_parser.py
        parser = AP_Parser(AP_DATA_PATH)
        parser.parse_ap_nodes()
        self.network_reference = parser.get_ap_nodes()

        # stores raw output from process pipe
        self.process_output = ""

    def __repr__(self):
        """ Representation of the dict stored in this class
        :return out: string representation of the network dictionary
        """

        out = "MAC,Quality,RSSI,Distance,SSID\n"
        for key, value in self.network_dict.items():
            out += f"{key},{value['quality']},{value['RSSI']},{value['distance']},{value['SSID']}\n"

        return out

    @staticmethod
    def quality_to_rssi(quality):
        """ Converts quality to RSSI, using the formula RSSI = (quality / 2) - 100
        This is bounded to be within the range -50 ... -100

        :param quality: quality of the signal
        :return: the equivalent RSSI value
        """
        if quality <= 0:
            return -100
        elif quality >= 100:
            return -50
        else:
            return (quality / 2) - 100

    @staticmethod
    def rssi_to_distance(rssi):
        """ Converts RSSI to distance. This calculation is not bounded.
        Please note parameters need substantial tuning for good results.

        :param rssi: the RSSI of the given access point
        :return: the predicted distance to the access point
        """

        # RSSI = -10 * n * log(d) + A
        a = -50  # signal strength at 1m
        n = 2   # path loss exponent
        return math.pow(10, (rssi - a) / (-10 * n))

    def run_process(self):
        """ Runs pipeline process to get all access points nearby.
        This is the equivalent of running "iwlist scan" on a linux machine.

        The output of this function is raw data saved into process_output
        """

        # create the process to scan for networks - LINUX BASED IMPLEMENTATION
        # TODO - how do we make this process more universal?
        proc = sp.Popen(["iwlist", "scan"], stdout=sp.PIPE, universal_newlines=True)

        # communicate output from the process
        self.process_output, error = proc.communicate()

    def process_network_data(self):
        """ Processes the raw data getting frm the network scan into meaningful information

        The output of this function is population of the dict of networks in range
        """

        data = self.process_output.split("\n")

        # set a default key. if ERR is added to the dict, we know parsing hasn't worked correctly
        cur_key = "ERR"

        # .. and a default SSID
        cur_ssid = "ERR"

        for line in data:
            line = line.strip()

            # will give the key for this dict entry - MAC address
            if "Cell " in line:
                cur_key = line.split(": ")[1]

            # store ssid for adding to the dict later
            elif "SSID" in line:
                cur_ssid = line.split(':"')[1][:-1]

            # from this, we can discern RSSI and distance
            elif "Quality" in line:

                try:

                    # this might throw an IndexError - ignore if so
                    quality = float(line.split("=")[1].split("/")[0])

                    # convert to rssi and distance
                    rssi = self.quality_to_rssi(quality)
                    distance = self.rssi_to_distance(rssi)

                    # add the dict to the network dictionary
                    network_data = {
                        "quality": quality,
                        "RSSI": rssi,
                        "distance": distance,
                        "SSID": cur_ssid
                    }

                    self.network_dict[cur_key] = network_data

                except IndexError:

                    # TODO - do we throw an error here? should we handle this?
                    pass

        self.network_dict = dict(sorted(self.network_dict.items(), key=lambda item: item[1][2]))


    def load_offline_data(self, path):
        """ Loads network data from .csv file for offline testing

        :param path: path to the file to read from
        Populates internal dict network_dict, does not return anything
        """

        # get all data from csv file
        with open(path, 'r') as f:
            data = f.readlines()

        # skip the top line, as its the CSV header and not actual data
        for line in data[1:]:
            line = line.strip()

            # line is in form MAC,Quality,RSSI,Distance,SSID
            parts = line.split(",")
            self.network_dict[parts[0]] = {
                "quality": parts[1],
                "RSSI": parts[2],
                "distance": parts[3],
                "SSID": parts[4]
            }


if __name__ == "__main__":

    local_test = Localisation()

    if OFFLINE:
        local_test.load_offline_data(OFFLINE_PATH)
    else:
        local_test.run_process()
        local_test.process_network_data()

    print(repr(local_test))

    '''
    with open("studyroom_r3.csv", 'w') as f:
        f.write(repr(local_test))
    '''
