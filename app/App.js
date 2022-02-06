/**
 * @format
 * @flow strict-local
 */

import * as React from 'react';
import { View, StyleSheet, SafeAreaView, Button } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { ApolloClient, InMemoryCache, ApolloProvider } from '@apollo/client';
import QueryTest from './TestQueries/QueryTest';

const Stack = createStackNavigator();
const client = new ApolloClient({
  uri: 'http://192.168.0.36:80',
  cache: new InMemoryCache(),
});

function Query({ navigation }) {
  return (
    <>
      <Button
        title="HomeScreen"
        onPress={() => navigation.navigate('HomeScreen')}
      />
      <ApolloProvider client={client}>
        <QueryTest />
      </ApolloProvider>
    </>
  );
}

function HomeScreen({ navigation }) {
  return (
    <SafeAreaView style={styles.container}>
      <View>
        <Button
          title="Query Test"
          onPress={() => navigation.navigate('Query')}
        />
      </View>
    </SafeAreaView>
  );
}

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen name="HomeScreen" component={HomeScreen} />
        <Stack.Screen name="Query" component={Query} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    marginHorizontal: 16,
  },
  title: {
    textAlign: 'center',
    marginVertical: 8,
  },
  fixToText: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  separator: {
    marginVertical: 8,
    borderBottomColor: '#737373',
    borderBottomWidth: StyleSheet.hairlineWidth,
  },
});

export default App;
