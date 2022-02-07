//import React, {useState} from 'react';
//import {Button, StyleSheet} from 'react-native';
/*import { // evyrhing from viro, genraly if soemthing is missing and its viro related add it here
  ViroARScene,
  ViroText,
  ViroConstants,
  ViroARSceneNavigator,
  ViroBox
} from '@viro-community/react-viro';*/
/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 * @flow strict-local
 */

 import * as React from 'react';
 import { View, Text, StyleSheet, SafeAreaView, Button, Separator } from 'react-native';
 import { NavigationContainer } from '@react-navigation/native';
 import { createStackNavigator } from '@react-navigation/stack';
 import { HomeScreen } from './screens/HomeScreen.js';
 import { MapScreen } from './screens/MapScreen.js';
 import { ServerScreen } from './screens/ServerScreen.js';
 import { LocalizationScreen } from './screens/LocalizationScreen.js';
 
 const Stack = createStackNavigator();
 
 //creates a stack navigotro that is used to switch netwen pages, each page is stored in the screens foulder and returns the page as requetsed
 function App() {
   return (
     <NavigationContainer>
       <Stack.Navigator initialRouteName="Home">
         <Stack.Screen name="Home" component={HomeScreen} />
         <Stack.Screen name="Localization" component={LocalizationScreen} />
         <Stack.Screen name="Mapping" component={MapScreen} />
         <Stack.Screen name="Server" component={ServerScreen} />
       </Stack.Navigator>
     </NavigationContainer>
   );
 }
 
 export default App;
 

 /*
 const Separator = () => (
   <View style={styles.separator} />
 );
 
 const App = () => (
   <SafeAreaView style={styles.container}>
     <View>
       <Button
         title="localization"
         onPress={() => Alert.alert('Simple Button pressed')}
       />
     </View>
     <Separator />
     <View>
       <Button
         title="mapping"
         onPress={() => Alert.alert('Simple Button pressed')}
       />
     </View>
     <Separator />
     <View>
       <Button
         title="server"
         onPress={() => Alert.alert('Simple Button pressed')}
       />
     </View>
   </SafeAreaView>
 );
 
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
 
 export default App;*/
/* COMMETED OUT UNTIL WE NEED AR STUFF
// all AR related stuff from vriomidea timeplate
const InitialScene=()=>{
  //equivlent of a view in a 2d scene
  return(
    // anything that is required to be in 3D soace gose in the <ViroARScene> tag
   <ViroARScene>
      <ViroText // exsmaple of text
      text={"Hello World"}
      position={[-2,-5,-1]}
      style={{fontSize:50,fontFamily:'Arial',color:'blue'}}
      />
          <ViroBox
          height={2} // for creating a 3D cube that is 2 x 2 x 2 
          length={2}
          width={2}
          position={[0,0,0]}
        />
     </ViroARScene>
  );
};

export default () => {
    return(
      //used for rendering all AR things
      <ViroARSceneNavigator
        initialScene={{
          scene:InitialScene
        }}
        styles={{flex:1}}
      />
    );
};

//creats a style sheet that is used for styling the text etc...
var styles = StyleSheet.create({
  f1: {flex: 1},
  helloWorldTextStyle: {
    fontFamily: 'Arial',
    fontSize: 30,
    color: '#ffffff',
    textAlignVertical: 'center',
    textAlign: 'center',
  },
});
*/