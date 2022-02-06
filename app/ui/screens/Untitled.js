import React from 'react';
import { StyleSheet, View, Text } from 'react-native';

function Untitled(props) {
  return (
    <View style={styles.container}>
      <View style={styles.rect}>
        <Text style={styles.mapping}>mapping</Text>
      </View>
      <View style={styles.rect1}>
        <Text style={styles.loalcazation}>loalcazation</Text>
      </View>
      <View style={styles.rect2}>
        <Text style={styles.severQuerys}>sever querys</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  rect: {
    width: 266,
    height: 117,
    backgroundColor: '#E6E6E6',
    marginTop: 73,
    alignSelf: 'center',
  },
  mapping: {
    fontFamily: 'roboto-regular',
    color: '#121212',
    height: 40,
    width: 109,
    marginTop: 33,
    marginLeft: 73,
  },
  rect1: {
    width: 266,
    height: 117,
    backgroundColor: '#E6E6E6',
    marginTop: 93,
    alignSelf: 'center',
  },
  loalcazation: {
    fontFamily: 'roboto-regular',
    color: '#121212',
    height: 73,
    width: 126,
    marginTop: 38,
    marginLeft: 104,
  },
  rect2: {
    width: 266,
    height: 117,
    backgroundColor: '#E6E6E6',
    marginTop: 121,
    marginLeft: 47,
  },
  severQuerys: {
    fontFamily: 'roboto-regular',
    color: '#121212',
    height: 59,
    width: 115,
    marginTop: 24,
    marginLeft: 67,
  },
});

export default Untitled;
