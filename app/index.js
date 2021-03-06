/**
 * @format
 */

import 'react-native-gesture-handler';
import { AppRegistry } from 'react-native';
import App from './components/App';
import { name as appName } from './app.json';

import { LogBox } from 'react-native';

LogBox.ignoreLogs([
  "[react-native-gesture-handler] Seems like you're using an old API with gesture components, check out new Gestures system!",
  'componentWillMount has been renamed, and is not recommended for use.',
  'Require cycle',
]);

AppRegistry.registerComponent(appName, () => App);
