import json
import sys
import os

class AP_Parser():
    # declare the nodes array to store the node data
    ap_nodes = []

    data = []

    # Constructor
    def __init__(self, path):
        self.path = str(path)

        # parse the file
        self.parse_AP_nodes()
    
    def parse_AP_nodes(self):
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
        with open(self.path + "/Wifi_Nodes.json", "r") as file:
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
            self.data = {
                "ap_name": ap,
                "longitude": lon,
                "latitude" : lat

            }

            #create node with Json node data
            self.ap_nodes.append({
                    mac : self.data
                })
         #print nodes for testing   
        for node in self.ap_nodes:
            print(node, '\n')

#run parser for testing
if __name__ == '__main__':
    cwd = str(os.getcwd())
    foo = AP_Parser(cwd)
    AP_Parser.parse_AP_nodes(foo)