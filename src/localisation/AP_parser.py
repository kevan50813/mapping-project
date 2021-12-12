import json
import sys
import os

class AP_Parser():
    # declare the nodes array to store the node data
    ap_nodes = []

    # Constructor
    def __init__(self, path):
        self.path = str(path)

        # parse the file
        self.parse_AP_nodes()
    
    def parse_AP_nodes(self):
        """
            Node data structure

            ap_node = {
                "ap": "",
                "mac": "",
                "coordinates": ()
            }
        """

        #Read Wifi_Nodes.json
        with open(self.path + "/Wifi_Nodes.json", "r") as file:
            json_ways = json.loads(file.read())

        #for every access point
        for feature in json_ways["features"]:

            #store the info that is in the Json
            coord = feature["geometry"]["coordinates"]
            mac = feature["properties"]["MacAddress"]
            ap = feature["properties"]["AP_Name"]

            #create node with Json node data
            self.ap_nodes.append({
                    "ap": ap,
                    "mac": mac,
                    "coordinates": coord
                })
         #print nodes for testing   
        print(self.ap_nodes)

#run parser for testing
if __name__ == '__main__':
    cwd = str(os.getcwd())
    foo = AP_Parser(cwd)
    AP_Parser.parse_AP_nodes(foo)