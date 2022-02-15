import React, { useContext, useEffect, useState } from 'react';
import { Text, View } from 'react-native';
import { Button } from './Button';
import { styles } from './styles';
import { APVisualisation } from './APVisualisation';
import { NetworkContext } from './NetworkProvider';
import { Trilateration } from './Trilateration';

export const Localisation = () => {
  const [knownNetworks, setKnownNetworks] = useState([]);
  const [usedNetworks, setUsedNetworks] = useState([]);
  const [predictedLocation, setPredictedLocation] = useState([]);
  const {
    networks: visibleNetworks,
    state: { scanning },
    startScan,
  } = useContext(NetworkContext);

  const loadKnownNetworks = async () => {
    return require('./Wifi_Nodes.json').features.map(
      ({ geometry, properties }) => ({
        coordinates: geometry.coordinates,
        name: properties.AP_Name,
        BSSID: properties.MacAddress,
      }),
    );
  };

  const scan = async () => {
    const data = await loadKnownNetworks();
    setKnownNetworks(data);

    await startScan();
  };

  // only fire when visibleNetworks updates
  useEffect(() => {
    let tri = new Trilateration(visibleNetworks, knownNetworks);
    tri.startTrilateration();

    setUsedNetworks(tri.getUsedNetworks());
    setPredictedLocation(tri.getPredictedLocation());
  }, [visibleNetworks]);

  return (
    <View style={styles.background}>
      <View style={styles.background}>
        <Button style={styles.button} title="Scan Networks" onPress={scan} />
        {knownNetworks.length > 0 ? (
          <Text style={styles.info}>Loaded network data from JSON.</Text>
        ) : null}
        {visibleNetworks.length > 0 ? (
          <Text style={styles.info}>Network scan successful.</Text>
        ) : null}
        {scanning ? <Text style={styles.info}>Scanning...</Text> : null}
      </View>
      <View style={{ height: '70%' }}>
        <APVisualisation
          knownNetworks={knownNetworks}
          visibleNetworks={visibleNetworks}
          usedNetworks={usedNetworks}
          predictedLocation={predictedLocation}
        />
      </View>
    </View>
  );
};
