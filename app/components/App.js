/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 * @flow strict-local
 */

import React, { createContext, useMemo, useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { ApolloClient, InMemoryCache, ApolloProvider } from '@apollo/client';
import { StatusBar, View } from 'react-native';

import { Scanner } from './Scanner';
import { RoomSearch } from './RoomSearch';
import { Localisation } from './Localisation';
import { styles } from './styles';
import { Button } from './Button';

export const IPContext = createContext({ ip: '', setIP: () => {} });

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
  </View>
);

const App = () => {
  const Stack = createStackNavigator();

  const [ip, setIP] = useState('192.168.0.1');
  const value = useMemo(
    () => ({
      ip,
      setIP,
    }),
    [ip],
  );

  const client = new ApolloClient({
    cache: new InMemoryCache(),
    uri: `http://${ip}`,
  });

  return (
    <IPContext.Provider value={value}>
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
          </Stack.Navigator>
        </NavigationContainer>
      </ApolloProvider>
    </IPContext.Provider>
  );
};

export default App;
