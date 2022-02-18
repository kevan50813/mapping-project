/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 * @flow strict-local
 */

import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { ApolloClient, InMemoryCache, ApolloProvider } from '@apollo/client';
import { StatusBar, View } from 'react-native';

import { Scanner } from './Scanner';
import { RoomSearch } from './RoomSearch';
import { Localisation } from './Localisation';
import { Floorplan } from './Floorplan';
import { styles } from './styles';
import { Button } from './Button';
import { NetworkProvider } from './NetworkProvider';

// Replace with local IP for development
export const server = 'mappingapp.azurewebsites.net';

const Home = ({ navigation }) => (
  <View style={styles.background}>
    <Button
      title="Network Scanner"
      onPress={() => navigation.navigate('Scanner')}
    />
    <Button
      title="Search Rooms"
      onPress={() => navigation.navigate('RoomSearch')}
    />
    <Button
      title="Perform Localisation"
      onPress={() => navigation.navigate('Localisation')}
    />
    <Button title="Map" onPress={() => navigation.navigate('Floorplan')} />
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
            <Stack.Screen name="RoomSearch" component={RoomSearch} />
            <Stack.Screen name="Scanner" component={Scanner} />
            <Stack.Screen name="Localisation" component={Localisation} />
            <Stack.Screen name="Floorplan" component={Floorplan} />
          </Stack.Navigator>
        </NavigationContainer>
      </ApolloProvider>
    </NetworkProvider>
  );
};

export default App;
