from AP_processor import AP_Processor
from trilateration import trilaterate_triplet, visualise_trilateration

class Trilateration_Heuristics():

    @staticmethod
    def first_three(ap_dict):

        return dict(list(ap_dict.items())[:3])



class Localisation():

    def __init__(self):

        self.ap_processor = AP_Processor("Wifi_Nodes.json")

        # dict to store the APs we want to use - has distances within the dict
        self.ap_dict = {}

        # dict to store the reference nodes
        self.ap_reference = self.ap_processor.network_reference

        # dict to store the scanned nodes
        self.scanned_ap = {}


    # helper function to execute a network scan and process the returned data
    def execute_scan(self):
        self.ap_processor.run_process()
        self.ap_processor.process_network_data()

        self.scanned_ap = self.ap_processor.network_dict


    def load_offline_data(self, path):
        self.ap_processor.load_offline_data(path)

        self.scanned_ap = self.ap_processor.network_dict


    def compare_ap_data(self):

        # reset dict
        self.ap_dict = {}

        # for every scanned access point
        for key in self.scanned_ap:

            # we asserted earlier all keys are upper case

            # if its in the reference data for this floor, we can use it!
            if key in self.ap_reference:

                self.ap_dict[key] = {
                    "ap_name": self.ap_reference[key]["ap_name"],
                    "lon": self.ap_reference[key]["lon"],
                    "lat": self.ap_reference[key]["lat"],
                    "distance": self.scanned_ap[key]["distance"]
                }


    # large control function for trilaterion is general
    def perform_trilateration(self):

        if len(self.ap_dict) < 3:
            print("ERR: Not enough network data. Skipping...")
            return

        # choose which 3 aps to use
        tri = Trilateration_Heuristics()
        used_dict = tri.first_three(self.ap_dict)


        # visualise! temporary
        err = None
        pos = trilaterate_triplet(used_dict)
        print(pos)
        # err = approximate_error(ap_sample, pos)
        visualise_trilateration(self.ap_reference, self.ap_dict, used_dict, pos, err)



    # -----------------------------------------------------
    # GETTER/SETTER
    # -----------------------------------------------------

    # returns the AP reference dict
    def get_ap_reference(self):
        return self.ap_reference


    # returns the dict of currently scanned APs
    def get_scanned_ap(self):
        return self.scanned_ap

    # retuns the dict of "good" aps for use
    def get_ap_dict(self):
        return self.ap_dict



if __name__ == "__main__":

    OFFLINE = True
    OFFLINE_PATH = "readings/studyroom_r1.csv"

    local = Localisation()
    if not OFFLINE:
        local.execute_scan()
    else:
        local.load_offline_data(OFFLINE_PATH)
    local.compare_ap_data()

    local.perform_trilateration()


    #print(local.get_ap_reference())
    #print(local.get_scanned_ap())
    #print(local.get_ap_dict())

