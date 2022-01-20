import React, {useState} from 'react';
import {Button, StyleSheet} from 'react-native';
import {
  ViroARScene,
  ViroText,
  ViroConstants,
  ViroARSceneNavigator,
  ViroBox
} from '@viro-community/react-viro';



// all AR related stuff from vriomidea timeplate -- creates a baisc hellowlrd applation

const InitialScene=()=>{
  //equivlent of a view in a 2d scene
  return(
   <ViroARScene>
      <ViroText
      text={"Hello World"}
      position={[-2,-5,-1]}
      style={{fontSize:50,fontFamily:'Arial',color:'blue'}}
      />
          <ViroBox
          height={2} // for creating a 3D cube
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
