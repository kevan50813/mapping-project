import React, { createContext, useState } from 'react';
import { PermissionsAndroid } from 'react-native';
import WifiManager from 'react-native-wifi-reborn';

// OFFLINE FLAG
export const Offline = false;

export const NetworkType = {
  UNSCANNED: 1,
  SCANNED: 2,
  USED: 3,
};

export const NetworkContext = createContext({
  networks: [],
  startScan: async () => {},
  state: {
    scanning: false,
    error: '',
  },
  info: {
    start: 0,
    duration: 0,
  },
  params: {
    a: -50,
    n: 3,
    setA: () => {},
    setN: () => {},
  },
});

export const NetworkProvider = ({ children }) => {
  const [networks, setNetworks] = useState([]);
  const [scanning, setScanning] = useState(false);
  const [error, setError] = useState('');

  const [duration, setDuration] = useState(0);

  const startScan = async () => {
    // if offline, skip all the rest and just load from a file
    if (Offline) {
      // update this to the offline path you want
      const networkData = require('../components/offline_scans/test.json');
      setScanning(networkData.state.scanning);
      setNetworks(networkData.networks);
      setError(networkData.state.error);
      setDuration(networkData.info.duration);
    } else {
      console.log('Starting scan at', new Date());

      setScanning(true);
      setError('');

      const start = new Date().getTime();

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

          setDuration(new Date().getTime() - start);

          setNetworks(
            wifiNetworks
              .map(({ SSID, BSSID, level }) => ({
                SSID,
                BSSID,
                RSSI: level,
              }))
              // Highest to lowest
              .sort((n1, n2) => n2.RSSI - n1.RSSI),
          );
        } catch (e) {
          console.error(e);
          setError('Problem while scanning');
        }
      } else {
        setError('Permission denied');
      }

      setScanning(false);
    }
  };

  const networkValue = {
    networks,
    startScan,
    state: {
      scanning,
      error,
    },
    info: {
      duration,
    },
  };

  console.log(JSON.stringify(networkValue));

  return (
    <NetworkContext.Provider value={networkValue}>
      {children}
    </NetworkContext.Provider>
  );
};
