import React, { useState } from 'react';
import { Text, View } from 'react-native';
import { Button } from './Button';
import { styles } from './styles';
import { Scan } from './Scan';
import { APVisualisation } from './APVisualisation';

export const Localisation = () => {
  const [knownNetworks, setKnownNetworks] = useState([]);
  const [visibleNetworks, setVisibleNetworks] = useState([]);

  const execute = async () => {
    setKnownNetworks([]);
    setVisibleNetworks([]);

    await loadData();

    let scan = new Scan();
    await scan.startScan();
    setVisibleNetworks(scan.getNetworks());
  };

  const loadData = async () => {
    setKnownNetworks(
      require('./Wifi_Nodes.json').features.map(({ geometry, properties }) => ({
        coordinates: geometry.coordinates,
        name: properties.AP_Name,
        BSSID: properties.MacAddress,
      })),
    );
  };

  return (
    <View style={styles.background}>
      <View style={styles.background}>
        <Button
          style={styles.button}
          title="Execute Process"
          onPress={execute}
        />
        {knownNetworks.length > 0 ? (
          <Text style={styles.info}>Loaded network data from JSON.</Text>
        ) : null}
        {visibleNetworks.length > 0 ? (
          <Text style={styles.info}>Network scan successful.</Text>
        ) : null}
      </View>
      <View style={{ height: '70%' }}>
        <APVisualisation
          knownNetworks={knownNetworks}
          visibleNetworks={visibleNetworks}
        />
      </View>
    </View>
  );
};
