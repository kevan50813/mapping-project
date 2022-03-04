import React, { useContext, useState } from 'react';
import { Text, View } from 'react-native';
import { Button } from './Button';
import { styles } from './styles';
import { APVisualisation } from './APVisualisation';
import { NetworkContext } from './NetworkProvider';
import { trilateration } from './Trilateration';
import {Slider} from "@miblanchard/react-native-slider";

export const Localisation = () => {
  const [knownNetworks, setKnownNetworks] = useState([]);
  let usedNetworks = [];
  let predictedLocation = {};

  let [a, setA] = useState(-50);
  let [n, setN] = useState(3);

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
    let data = trilateration(visibleNetworks, knownNetworks, a, n);

    predictedLocation = data.predictedLocation;
    usedNetworks = data.usedNetworks;
  }

  return (
    <View style={styles.background}>
      <View style={styles.background}>
        <Text style={styles.small}>N = {n.toFixed(2)}</Text>
        <Slider
            minimumValue={1}
            maximumValue={3}
            value={n}
            onValueChange={v => setN(v[0])}
        />
        <Text style={styles.small}>A = {a.toFixed(2)}</Text>
        <Slider
            minimumValue={-100}
            maximumValue={0}
            value={a}
            onValueChange={v => setA(v[0])}
        />
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
        />
      </View>
    </View>
  );
};
