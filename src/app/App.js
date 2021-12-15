import React from 'react';
import { Text, View } from 'react-native';
import ArCoreReactNativeViewManager from "ar-core-react-native"; //AR stuff

import { UIManager, findNodeHandle} from 'react-native';
import ArCoreReactNativeViewManager from "ar-core-react-native";


// code snippit form https://www.npmjs.com/package/ar-core-react-native/v/1.2.4
<ArCoreReactNativeViewManager ref="arCoreView" />
// on action button or any
// you send 2 parameter
// name_object - type:string : name object in 3D view.
// path_file - type:string : path file to glb in device.
function addObject(){
    UIManager.dispatchViewManagerCommand(
        findNodeHandle(this.refs.arCoreView),
        "CMD_RUN_SET_OBJECT",
        [name_object, path_file]);
}

// on action delete
function deleteObjectSeleted(){
  UIManager.dispatchViewManagerCommand(
      findNodeHandle(this.refs.arCoreView),
      "CMD_RUN_DELETE_OBJECT",
      []);
}

const HelloWorldApp = () => {
  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center"
      }}>
      <Text>Hello, world!</Text>
    </View>
  )
}
export default HelloWorldApp;