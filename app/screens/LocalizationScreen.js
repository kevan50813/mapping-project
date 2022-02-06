import * as React from 'react';
import { View, Text, StyleSheet, SafeAreaView, Button, Separator } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

export function LocalizationScreen({ navigation }) {
    return (
     <SafeAreaView style={styles.container}>
     <View>
       <Button
         title="Home"
         onPress={() => navigation.navigate('Home')}
       />
     </View>
     <View>
       <Button
         title="Mapping"
         onPress={() => navigation.navigate('Mapping')}
       />
     </View>
     <View>
       <Button
         title="Server"
         onPress={() => navigation.navigate('Server')}
       />
     </View>
   </SafeAreaView>
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