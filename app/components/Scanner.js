import React, { useState } from 'react';
import { ScrollView, Text, View, PermissionsAndroid,TextInput } from 'react-native';
import Slider from "react-native-sliders";
import WifiManager from 'react-native-wifi-reborn';
import { Button } from './Button';
import { styles } from './styles';

export const Scanner = () => {
  const [networks, setNetworks] = useState([]);
  const [scanning, setScanning] = useState(false);
  const [error, setError] = useState('');

  const [time, setTime] = useState({ start: new Date(), end: new Date() });

  const [NValue, setSliderValueN] = useState(3);
  const [AValue, setSliderValueA] = useState(-50);

  const rssiToDistance = rssi => {
    const A = -50; // Signal strength at 1 meter
    const N = 2; // Path exponent

    // rssi = -10 * N * log(D) + A
    // D = 10^((rssi - A) / (-10 * N))
    return Math.pow(10, (rssi - AValue) / (-10 * NValue));
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
        <Text style={{color: 'black', marginHorizontal:20}}>
           Value of N is : {NValue}
        </Text>
        <Slider
        //Slider that will hold the value of N
          style={{flex:1, marginHorizontal:20}}
          minimumValue={1}
          maximumValue={3}
          minimumTrackTintColor="#FFFFFF"
          maximumTrackTintColor="#000000"
          value={NValue}
          onValueChange={
            (NValue) => setSliderValueN(NValue)
          }
        />
        <Text style={{color: 'black', marginHorizontal:20}}>
           Value of A is : {AValue}
        </Text>
        <Slider
          //Slider that will hold the value of A
          style={{flex:1, marginHorizontal:20}}
          minimumValue={-100}
          maximumValue={0}
          minimumTrackTintColor="#FFFFFF"
          maximumTrackTintColor="#3333cc"
          value={AValue}
          onValueChange={
            (AValue) => setSliderValueA(AValue)
          }
        />

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
