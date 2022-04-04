/**
 * @format
 * @flow strict-local
 */

import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { ApolloClient, InMemoryCache, ApolloProvider } from '@apollo/client';
import { StatusBar, View } from 'react-native';
import RNReactLogging from 'react-native-file-log';

import { Scanner } from './Scanner';
import { Localisation } from './Localisation';
import { LoadFloorplan } from './LoadFloorplan';
import { styles } from './styles';
import { Button } from './Button';
import { NetworkProvider } from './NetworkProvider';

RNReactLogging.setTag('MAPAPP');
RNReactLogging.setFileLogEnabled(true);
RNReactLogging.setConsoleLogEnabled(true);
RNReactLogging.printLog('=== NEW LOG ===');

// Replace with local IP for development
export const server = 'mappingapp.azurewebsites.net';

const Home = ({ navigation }) => (
  <View style={styles.background}>
    <Button
      title="Network Scanner"
      onPress={() => navigation.navigate('Scanner')}
    />
    <Button
      title="Perform Localisation"
      onPress={() => navigation.navigate('Localisation')}
    />
    <Button
      title="Floorplan"
      onPress={() => navigation.navigate('Floorplan')}
    />
  </View>
);

const App = () => {
  const Stack = createStackNavigator();

  const client = new ApolloClient({
    cache: new InMemoryCache(),
    uri: `http://${server}`,
  });

  return (
    <NetworkProvider>
      <ApolloProvider client={client}>
        <NavigationContainer>
          <StatusBar
            barStyle={'dark-content'}
            backgroundColor={'#ffffff00'}
            translucent={true}
          />
          <Stack.Navigator initialRouteName="Home">
            <Stack.Screen name="Home" component={Home} />
            <Stack.Screen name="Scanner" component={Scanner} />
            <Stack.Screen name="Localisation" component={Localisation} />
            <Stack.Screen name="Floorplan" component={LoadFloorplan} />
          </Stack.Navigator>
        </NavigationContainer>
      </ApolloProvider>
    </NetworkProvider>
  );
};

export default App;
