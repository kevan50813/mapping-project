import React, {useState} from 'react';
import QueryTest from './TestQueries/QueryTest'
import {
  ApolloClient,
  InMemoryCache,
  ApolloProvider,
} from "@apollo/client";

const client = new ApolloClient({
  uri: 'http://192.168.0.36:8888',
  cache: new InMemoryCache()
});

export default function App() {
  return (
    <ApolloProvider client={client}>
      <QueryTest />
    </ApolloProvider>
  )
}

// import {
//   // evyrhing from viro, genraly if soemthing is missing and its viro related add it here
//   ViroARScene,
//   ViroText,
//   ViroConstants,
//   ViroARSceneNavigator,
//   ViroBox,
// } from '@viro-community/react-viro';

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
