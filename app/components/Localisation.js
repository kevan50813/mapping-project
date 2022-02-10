import React, { useState } from 'react';
import { ScrollView, Text, View } from 'react-native';
import { Button } from './Button';
import { styles } from './styles';
import { Scan } from './Scanner';

export const Localisation = () => {
  const [networks, setNetworks] = useState([]);
  const [scanning, setScanning] = useState(false);
  const [error, setError] = useState('');
  const [time, setTime] = useState({ start: new Date(), end: new Date() });
  const [networkData, setNetworkData] = useState([]);

  const startScan = async () => {
    setScanning(true);

    let scan = new Scan();
    await scan.startScan();

    setNetworks(scan.getNetworks());
    setError(scan.getError());
    setTime(scan.getTime());
    setScanning(false);
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

  return (
    <View style={styles.background}>
      <ScrollView contentInsetAdjustmentBehavior="automatic">
        <Button
          style={styles.button}
          title="Load JSON Data"
          onPress={loadData}
        />
        {networkData !== null ? (
          <Text style={styles.info}>Loaded network data from JSON.</Text>
        ) : null}
        <Button style={styles.button} title="Scan" onPress={startScan} />
      </ScrollView>
    </View>
  );
};
