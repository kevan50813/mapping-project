import React, { useContext, useState, useEffect } from 'react';
import { ScrollView, Text, View } from 'react-native';
import { Slider } from '@miblanchard/react-native-slider';
import { Button } from './Button';
import { styles } from './styles';
import { NetworkContext } from './NetworkProvider';
import { Dirs, FileSystem } from 'react-native-file-access';
import Toast from 'react-native-simple-toast';

export const Scanner = () => {
  const { networks, startScan, state, info } = useContext(NetworkContext);
  const [networksToSave, setNetworksToSave] = useState(null);

  let [a, setA] = useState(-50);
  let [n, setN] = useState(3);

  const rssiToDistance = rssi => Math.pow(10, (rssi - a) / (-10 * n));

  useEffect(() => {
    // ignore the first push applied when the screen loads. kind of a hack, but
    if (networksToSave) {
      networksToSave.push(networks);
    } else {
      setNetworksToSave([]);
    }

    // shouldnt do this. but priority right now is just getting data
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [networks]);

  const saveNetworks = async () => {
    //  TODO - write to file

    const fileName = 'SCAN_' + Date.now() + '.json';
    const path = Dirs.DocumentDir + '/' + fileName;

    await FileSystem.writeFile(path, JSON.stringify(networksToSave), 'utf8');
    if (!FileSystem.exists(path)) {
      console.log('File I/O error. Saved networks not discarded.');
      return;
    }
    await FileSystem.cpExternal(path, fileName, 'downloads');

    console.log('Saved to ' + path);
    Toast.show('Successfully saved scan data to file.', Toast.SHORT);
    setNetworksToSave([]);
  };

  return (
    <View style={styles.background}>
      <View style={styles.spacedBox}>
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
      </View>
      <Button style={styles.button} title="Scan" onPress={startScan} />
      <Button
        style={styles.button}
        title={
          'Save ' + (networksToSave ? networksToSave.length : 0) + ' Scan(s)'
        }
        onPress={saveNetworks}
      />
      {state.scanning ? <Text style={styles.info}>Scanning...</Text> : null}
      {state.error ? <Text style={styles.error}>{state.error}</Text> : null}
      <Text style={styles.info}>Took {info.duration / 1000}s</Text>

      <ScrollView>
        {networks.map(({ SSID, BSSID, RSSI }) => (
          <View key={BSSID} style={styles.box}>
            <Text style={styles.big}>
              {SSID} ({BSSID})
            </Text>
            <Text style={styles.small}>
              {RSSI}dBm = {rssiToDistance(RSSI)}m
            </Text>
          </View>
        ))}
      </ScrollView>
    </View>
  );
};
