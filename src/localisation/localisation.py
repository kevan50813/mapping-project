import subprocess as sp
import math


class Localisation:

    def __init__(self):

        # dict will store networks in the follow format:
        # { MAC_ADDRESS: (Quality, RSSI, Distance, SSID) }
        # Quality is not required - a value of -1 means quality was not obtained
        # SSID is also not required, but kept for reference
        self.network_dict = {}

        # stores raw output from process pipe
        self.process_output = ""

    def __repr__(self):
        """ Representation of the dict stored in this class
        :return: out: string representation of the network dictionary
        """

        out = "      MAC      | Quality | RSSI |   Distance   | SSID\n"
        for key, value in self.network_dict.items():
            out += f"{key}, {value[0]}, {value[1]}, {value[2]}, {value[3]}\n"

        return out

    @staticmethod
    def quality_to_rssi(quality):
        """ Converts quality to RSSI, using the formula RSSI = (quality / 2) - 100
            This is bounded to be within the range -50 ... -100

            :param quality: quality of the signal
            :return the equivalent RSSI value
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
        n = 2.7  # path loss exponent
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

            # store ssid for adding to the tuple later
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

                    # add the tuple to the network dictionary
                    network_tuple = (quality, rssi, distance, cur_ssid)
                    self.network_dict[cur_key] = network_tuple

                except IndexError:

                    # TODO - do we throw an error here? should we handle this?
                    pass


if __name__ == "__main__":

    local_test = Localisation()
    local_test.run_process()
    local_test.process_network_data()

    print(repr(local_test))
