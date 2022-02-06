import React, { Component } from 'react';
import {Button, StyleSheet, Text, View} from 'react-native';
import {PermissionsAndroid} from 'react-native';
import WifiManager from 'react-native-wifi-reborn';


class Localisation extends Component {

    /**
     * List of states used by this component
     *
     * @type {{networkList: Array}} - List of networks scanned
     */
    state = {
        networkList: []
    };

    /**
     * Converts RSSI to distance. This calculation is not bounded.
     * Please note parameters need substantial tuning for good results.
     *
     * @param {number} RSSI - Signal strength of input number
     * @returns {number} distance - Distance of AP derived from RSSI
     */
    static RSSItoDistance(RSSI) {

        // RSSI = -10 * n * log(d) + A
        let a = -50;    // signal strength at 1m
        let n = 2;      // path loss exponent

        return Math.pow(10, (RSSI - a) / (-10 * n));

    }

    /**
     * Performs scans for nearby networks using WifiManager, after checking
     * the application has permission to do so. If it does not, permission is
     * asked for and obtained inside this function.
     */
    doScan = async () => {

        // ask for permission
        const granted = await PermissionsAndroid.request(
            PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
            {
                title: 'title',     // TODO - update title
                message: 'message', // TODO - update message
                buttonNegative: 'DENY',
                buttonPositive: 'ALLOW',
            }
        );

        // only proceed if we have permission
        if (granted === PermissionsAndroid.RESULTS.GRANTED) {

            // reset list of detected networks
            this.setState({
                networkList: []
            });

            console.log("scan started");

            // TODO - rescan or load? overhead vs accurate data...
            WifiManager.reScanAndLoadWifiList().then(


                // if fulfilled, we have an array of WifiEntry objects
                list => {

                    console.log("scan ended");

                    // set distance from each AP - added onto the WifiEntry
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

                // TODO - handle errors in the scan
                () => {
                    console.log("scan failed");
                }
            )

        } else {

            // TODO - handle rejection :(
            console.log("denied permissions");
        }
    };


    /**
     * Render networks to screen - temporary for testing/demoing
     */
    render () {

        /**
         * Iterates through network list object, allowing each to be printed
         * via a react-native <Text/> entry
         *
         * @returns - Series of text entries, one for each network
         */
        const listAP = this.state.networkList.map(elem => {
            return (
                <Text style={{fontFamily: "monospace", fontSize: 9}} key={elem.BSSID}> {elem.SSID.padEnd(15, " ")} | {elem.BSSID} | {elem.level} | {('' + elem.distance.toPrecision(8)).padEnd(8)} | {elem.frequency} </Text>
            )
        });

        // parent display function
        return(

            <View
                style={{
                    flex: 1,
                    justifyContent: "center",
                }}>
                <Button title="Request Permissions" onPress={this.doScan} />
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
