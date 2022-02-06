import React, { Component } from 'react';
import {Button, StyleSheet, Text, View} from 'react-native';
import {PermissionsAndroid} from 'react-native';
import WifiManager from 'react-native-wifi-reborn';


class Localisation extends Component {

    state = {
        debugList: []
    };

    getPermission = async () => {

        const granted = await PermissionsAndroid.request(
            PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
            {
                title: 'title',
                message: 'message',
                buttonNegative: 'DENY',
                buttonPositive: 'ALLOW',
            }
        );

        console.log("granted:" + granted);

        if (granted === PermissionsAndroid.RESULTS.GRANTED) {
            // not cry
            console.log("access allowed");


            WifiManager.loadWifiList().then(

                list => {
                    this.setState({
                        debugList: list
                    })
                },
                () => {
                    console.log("list couldnt be loaded");
                }

            )



        } else {
            console.log("denied");
        }
    };

    renderRow(elem) {
        return (
            <View style={{ flex: 1, alignSelf: 'stretch', flexDirection: 'row' }}>
                <Text key={elem.BSSID}>{elem.SSID}</Text>
            </View>
        )
    }


    render () {

        const listAP = this.state.debugList.map(elem => {
            return (
                <Text style={{fontFamily: "monospace", fontSize: 9}} key={elem.BSSID}> {elem.SSID.padEnd(15, " ")} | {elem.BSSID} | {('' + elem.frequency).padEnd(5)} | {elem.level} | {elem.timestamp} </Text>
            )
        });


        return(

            <View
                style={{
                    flex: 1,
                    justifyContent: "center",
                }}>
                <Button title="Request Permissions" onPress={this.getPermission} />
                <Text style={{fontFamily: "monospace", fontSize: 9}} key="header"> {"SSID".padEnd(15, " ")} | {"BSSID/MAC".padEnd(17)} | Freq. | dBm | Timestamp</Text>
                {listAP}
            </View>
        );
    };
}

export default Localisation;

















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
