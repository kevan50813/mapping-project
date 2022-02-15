import React, { useContext, useState } from 'react';
import { Text, View } from 'react-native';
import { Button } from './Button';
import { styles } from './styles';
import { APVisualisation } from './APVisualisation';
import { NetworkContext } from './NetworkProvider';
import { trilateration } from './Trilateration';

export const Localisation = () => {
  const [knownNetworks, setKnownNetworks] = useState([]);
  let usedNetworks = [];
  let predictedLocation = [];
  //let error = -1;

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

    startScan();
  };

  if (visibleNetworks.length > 0) {
    let data = trilateration(visibleNetworks, knownNetworks);

    console.log(data);

    predictedLocation = data.predictedLocation;
    usedNetworks = data.usedNetworks;
    //error = data.error;
  }

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
      <View style={styles.plotly}>
        <APVisualisation
          knownNetworks={knownNetworks}
          visibleNetworks={visibleNetworks}
          usedNetworks={usedNetworks}
          predictedLocation={predictedLocation}
          //error={error}
        />
      </View>
    </View>
  );
};
