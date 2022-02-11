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
        SSID: properties.AP_Name,
        BSSID: properties.MacAddress,
      })),
    );
  };

  // only fire when networkData/networkScanned update
  useEffect(() => {
    if (networkData.length > 0 && networkScanned.length > 0) {

        console.log(networkData.map(element => element.BSSID).sort());
        console.log(networkScanned.map(element => element.BSSID).sort());

        // hash using the BSSID. allows O(1) direct access via the key
        let scannedDict = Object.assign({}, ...networkScanned.map((networkScanned) => ({[networkScanned.BSSID]: networkScanned.distance})));

        for (let index = 0; index < networkData.length; index++) {
            let key = networkData[index].BSSID;
            console.log(key);
            if (key in scannedDict) {
                console.log("woo");
                networkData[index].distance = networkScanned.distance;
            } else {
               networkData[index].distance = -1;
            }
        }

        console.log(networkData);

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
