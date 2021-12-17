import json
import sys
import os

PRINT_REPR = False

class AP_Parser():

    # Constructor
    def __init__(self, path):
        self.path = str(path)

        # declare the nodes dict to store the node data
        self.ap_nodes = {}


    def __repr__(self):

        out = "MAC,ap_name,lon,lat\n"
        for key, value in self.ap_nodes.items():
            out += f"{key},{value['ap_name']},{value['lon']},{value['lat']}\n"

        return out


    def get_ap_nodes(self):
        return self.ap_nodes

    
    def parse_ap_nodes(self):
        """
            Node data structure

            data = {
                "ap_name": "",
                "longitude": "",
                "latitude": ""
            }

            ap_nodes = {
                macaddress : data,
            }
            
        """

        #Read Wifi_Nodes.json
        with open(self.path, "r") as file:
            json_ways = json.loads(file.read())

        #for every access point
        for feature in json_ways["features"]:

            #store the info that is in the Json
            coord = feature["geometry"]["coordinates"]
            mac = feature["properties"]["MacAddress"]
            ap = feature["properties"]["AP_Name"]
            lon = coord[0]
            lat = coord[1]

            # create a temporary data dictionary to store the information
            data = {
                "ap_name": ap,
                "lon": lon,
                "lat" : lat

            }

            #create node with Json node data
            self.ap_nodes[mac] = data

#run parser for testing
if __name__ == '__main__':
    parser = AP_Parser("Wifi_Nodes.json")
    parser.parse_ap_nodes()

    print(repr(parser))