import React, { useState, useEffect } from 'react';
import { ScrollView, Text, View } from 'react-native';
import { Button } from './Button';
import { styles } from './styles';
import { Scan } from './Scanner';

export const Localisation = () => {
  const [networkScanned, setNetworkScanned] = useState([]);
  const [networkData, setNetworkData] = useState([]);
  const [networkWithDist, setNetworkWithDist] = useState([]);

  const execute = async () => {
    let scan = new Scan();
    await scan.startScan();
    setNetworkScanned(scan.getNetworks());

    await loadData();

    // any further execution now is in useEffect when both arrays have been populated
  };

  const loadData = async () => {
    setNetworkData(
      require('./Wifi_Nodes.json').features.map(({ geometry, properties }) => ({
        coordinates: geometry.coordinates,
        name: properties.AP_Name,
        BSSID: properties.MacAddress,
      })),
    );
  };

  // only fire when networkData/networkScanned update
  useEffect(() => {
    if (networkData.length > 0 && networkScanned.length > 0) {

        // for every network
        for (let index = 0; index < networkData.length; index++) {

            let key = networkData[index].BSSID;

            // pre set some new data we want to record
            networkData[index].distance = -1;
            networkData[index].type = "unscanned";
            networkData[index].SSID = "n/a";

            // inefficient to nest array for loops, but necessary as partial keys being used
            // i'd like to use a dict as faster, but the key would be an issue...
            for (let scan = 0; scan < networkScanned.length; scan++) {

                // check for partial key - i.e. skim off very last digit
                if (networkScanned[scan]["BSSID"].includes(key.slice(0, -1))) {

                    networkData[index].distance = networkScanned[scan].distance;
                    networkData[index].SSID = networkScanned[scan].SSID;
                    networkData[index].type = "scanned";
                }
            }
        }

        setNetworkWithDist(networkData);
    }
  }, [networkData, networkScanned]);

  return (
    <View style={styles.background}>
      <ScrollView contentInsetAdjustmentBehavior="automatic">
        <Button
          style={styles.button}
          title="Execute Process"
          onPress={execute}
        />
        {networkData.length > 0 ? (
          <Text style={styles.info}>Loaded network data from JSON.</Text>
        ) : null}
        {networkScanned.length > 0 ? (
          <Text style={styles.info}>Network scan successful.</Text>
        ) : null}
      </ScrollView>
    </View>
  );
};
