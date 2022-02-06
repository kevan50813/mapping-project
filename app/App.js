import React, { Component } from 'react';
import {Button, StyleSheet, Text, View} from 'react-native';
import {PermissionsAndroid} from 'react-native';
import WifiManager from 'react-native-wifi-reborn';


class Localisation extends Component {

    state = {
        networkList: []
    };

    static RSSItoDistance(RSSI) {

        /* Converts RSSI to distance. This calculation is not bounded.
        Please note parameters need substantial tuning for good results.

            :param rssi: the RSSI of the given access point
            :return: the predicted distance to the access point
        */

        // RSSI = -10 * n * log(d) + A
        let a = -50;    // signal strength at 1m
        let n = 2;      // path loss exponent

        return Math.pow(10, (RSSI - a) / (-10 * n));

    }

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

        if (granted === PermissionsAndroid.RESULTS.GRANTED) {

            // reset list of detected networks
            this.setState({
                networkList: []
            });

            console.log("scan started");

            // TODO - rescan or load? overhead vs accurate data...
            WifiManager.reScanAndLoadWifiList().then(

                list => {

                    console.log("scan ended");

                    // set distance from each AP
                    for (let i = 0; i < list.length; i++)
                        list[i].distance = Localisation.RSSItoDistance(list[i].level);

                    // save list to state
                    this.setState({

                        // sorts list based on ascending distance
                        // needs a custom compare function as this is an array of objects
                        networkList: list.sort((a, b) =>
                            (a.distance > b.distance) ? 1 : ((b.distance > a.distance) ? -1 : 0)
                        )
                    });
                },

                () => {
                    console.log("scan failed");
                }
            )

        } else {
            console.log("denied permissions");
        }
    };


    render () {

        const listAP = this.state.networkList.map(elem => {
            return (
                <Text style={{fontFamily: "monospace", fontSize: 9}} key={elem.BSSID}> {elem.SSID.padEnd(15, " ")} | {elem.BSSID} | {elem.level} | {('' + elem.distance.toPrecision(8)).padEnd(8)} | {elem.frequency} </Text>
            )
        });

        return(

            <View
                style={{
                    flex: 1,
                    justifyContent: "center",
                }}>
                <Button title="Request Permissions" onPress={this.getPermission} />
                <Text style={{fontFamily: "monospace", fontSize: 9}} key="header"> {"SSID".padEnd(15, " ")} | {"BSSID/MAC".padEnd(17)} | dBm | Distance | Frequency</Text>
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
