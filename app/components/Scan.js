import { PermissionsAndroid } from 'react-native';
import WifiManager from 'react-native-wifi-reborn';

export const Network = {
  UNSCANNED: 1,
  SCANNED: 2,
  USED: 3,
};

export class Scan {
  constructor() {
    this.networks = [];
    this.error = '';
    this.timeStart = new Date();
    this.timeEnd = new Date();

    this.A = -50; // signal strength at 1 meter
    this.N = 2; // path exponent loss
  }

  rssiToDistance(rssi) {
    // rssi = -10 * N * log(D) + A
    // D = 10^((rssi - A) / (-10 * N))
    return Math.pow(10, (rssi - this.A) / (-10 * this.N));
  }

  getNetworks() {
    return this.networks;
  }

  getError() {
    return this.error;
  }

  getTime() {
    return { start: this.timeStart, end: this.timeEnd };
  }

  async startScan() {
    console.log('Starting scan at', new Date());

    this.networks = [];
    this.error = '';
    this.timeStart = new Date();
    this.timeEnd = new Date();

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

        this.timeEnd = new Date();

        this.networks = wifiNetworks
          .map(({ SSID, BSSID, level }) => ({
            SSID,
            BSSID,
            level,
            distance: this.rssiToDistance(level),
          }))
          // Highest to lowest
          .sort((n1, n2) => n2.level - n1.level);
      } catch (e) {
        console.error(e);
        this.error = 'Problem while scanning';
      }
    } else {
      this.error = 'Permission denied';
    }
  }
}
