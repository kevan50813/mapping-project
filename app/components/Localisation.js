import React, { useState } from 'react';
import { ScrollView, Text, View, PermissionsAndroid } from 'react-native';
import { Button } from './Button';
import { styles } from './styles';
import { Scan } from './Scanner';

export const Localisation = () => {
  const [networks, setNetworks] = useState([]);
  const [scanning, setScanning] = useState(false);
  const [error, setError] = useState('');
  const [time, setTime] = useState({ start: new Date(), end: new Date() });
  let networkData = null;

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
    networkData = require('./Wifi_Nodes.json').features;
    for (let feat in networkData) {
      console.log(networkData[feat]);
    }
    //console.log(networkData);
  };

  return (
    <View style={styles.background}>
      <ScrollView contentInsetAdjustmentBehavior="automatic">
        <Button
          style={styles.button}
          title="Load JSON Data"
          onPress={loadData}
        />
        {networkData ? (
          <Button style={styles.button} title="Scan" onPress={startScan} />
        ) : null}
      </ScrollView>
    </View>
  );
};
