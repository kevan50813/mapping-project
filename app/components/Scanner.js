import React, { useState } from 'react';
import { ScrollView, Text, View } from 'react-native';
import { Slider } from '@miblanchard/react-native-slider';
import { Button } from './Button';
import { Scan } from './Scan';
import { styles } from './styles';

export const Scanner = () => {
  const [networks, setNetworks] = useState([]);

  const [scanning, setScanning] = useState(false);
  const [error, setError] = useState('');
  const [time, setTime] = useState({ start: new Date(), end: new Date() });

  const [nValue, setN] = useState(3);
  const [aValue, setA] = useState(-50);

  const rssiToDistance = rssi => {
    // rssi = -10 * N * log(D) + A
    // D = 10^((rssi - A) / (-10 * N))
    return Math.pow(10, (rssi - aValue) / (-10 * nValue));
  };

  const startScan = async () => {
    setScanning(true);

    let scan = new Scan();

    await scan.startScan();

    setNetworks(scan.getNetworks());
    setError(scan.getError());
    setTime(scan.getTime());
    setScanning(false);
  };

  return (
    <View style={styles.background}>
      <View style={styles.spacedBox}>
        <Text style={styles.small}>N = {nValue.toFixed(2)}</Text>
        <Slider
          minimumValue={1}
          maximumValue={3}
          value={nValue}
          onValueChange={v => setN(v[0])}
        />
        <Text style={styles.small}>A = {aValue.toFixed(2)}</Text>
        <Slider
          minimumValue={-100}
          maximumValue={0}
          value={aValue}
          onValueChange={v => setA(v[0])}
        />
      </View>
      <Button style={styles.button} title="Scan" onPress={startScan} />
      {scanning ? <Text style={styles.info}>Scanning...</Text> : null}
      {error ? <Text style={styles.error}>{error}</Text> : null}
      <Text style={styles.info}>
        Took {(time.end.getTime() - time.start.getTime()) / 1000}s
      </Text>

      <ScrollView>
        {networks.map(({ SSID, BSSID, level }) => (
          <View key={BSSID} style={styles.box}>
            <Text style={styles.big}>
              {SSID} ({BSSID})
            </Text>
            <Text style={styles.small}>
              {level}dBm = {rssiToDistance(level).toFixed(2)}m
            </Text>
          </View>
        ))}
      </ScrollView>
    </View>
  );
};
