import React, { useState } from 'react';
import { ScrollView, Text, View, PermissionsAndroid } from 'react-native';
import WifiManager from 'react-native-wifi-reborn';
import { Button } from './Button';
import { styles } from './styles';

export const Scanner = () => {
  const [networks, setNetworks] = useState([]);
  const [scanning, setScanning] = useState(false);
  const [error, setError] = useState('');

  const [time, setTime] = useState({ start: new Date(), end: new Date() });

  const rssiToDistance = rssi => {
    const A = -50; // Signal strength at 1 meter
    const N = 2; // Path exponent

    // rssi = -10 * N * log(D) + A
    // D = 10^((rssi - A) / (-10 * N))
    return Math.pow(10, (rssi - A) / (-10 * N));
  };

  const startScan = async () => {
    console.log('Starting scan at', new Date());
    setTime({ start: new Date(), end: new Date() });
    setScanning(true);
    setError('');

    const granted = await PermissionsAndroid.request(
      PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
      {
        title: 'Location permission is required for WiFi connections',
        message:
          'This app needs location permission as this is required to scan for wifi networks.',
        buttonNegative: 'DENY',
        buttonPositive: 'ALLOW',
      },
    );

    if (granted === PermissionsAndroid.RESULTS.GRANTED) {
      try {
        const wifiNetworks = await WifiManager.reScanAndLoadWifiList();
        console.log('Scan complete!');
        setTime(s => ({ ...s, end: new Date() }));

        const list = wifiNetworks
          .map(({ SSID, BSSID, level }) => ({
            SSID,
            BSSID,
            level,
          }))
          // Highest to lowest
          .sort((n1, n2) => n2.level - n1.level);

        setNetworks(list);
      } catch (e) {
        console.error(e);
        setNetworks([
          { SSID: 'Problem while scanning', BSSID: 'n/a', level: 0 },
        ]);
      }
    } else {
      setNetworks([{ SSID: 'Permission denied', BSSID: 'n/a', level: 0 }]);
    }

    setScanning(false);
  };

  return (
    <View style={styles.background}>
      <ScrollView contentInsetAdjustmentBehavior="automatic">
        <Button style={styles.button} title="Scan" onPress={startScan} />
        {scanning ? <Text style={styles.info}>Scanning...</Text> : null}
        {error ? <Text style={styles.error}>{error}</Text> : null}
        <Text style={styles.info}>
          Took {(time.end.getTime() - time.start.getTime()) / 1000}s
        </Text>
        {networks.map(({ SSID, BSSID, level }) => (
          <View key={BSSID} style={styles.box}>
            <Text style={styles.big}>
              {SSID} ({BSSID})
            </Text>
            <Text style={styles.small}>
              {level} = {rssiToDistance(level).toFixed(2)}m
            </Text>
          </View>
        ))}
      </ScrollView>
    </View>
  );
};
