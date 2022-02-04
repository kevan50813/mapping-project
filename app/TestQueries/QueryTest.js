import React from 'react';
import {Text, StyleSheet, View} from 'react-native';
import {
  useQuery,
  gql
} from "@apollo/client";

var styles = StyleSheet.create({
  TextStyle: {
    fontSize: 15,
    color: '#fff',
    marginBottom: 0,
  },
});

const EXCHANGE_RATES = gql`
  query Nodes {
    polygons (graph: "test_bragg") {
      id
      tags
    }
  }
`;


function Polygons() {
  const { loading, error, data } = useQuery(EXCHANGE_RATES);
  if (loading) {
    console.log("Loading")
    return <Text styles={styles.TextStyle}>Loading...</Text>;
  }

  if (error) {
    console.log(error);
    return <Text styles={styles.TextStyle}>Error</Text>;
  };

  return data.polygons.map(({id, tags}) => (
      <View key={id}>
        <Text style={styles.TextStyle} key={id}>
          {id}: {tags.indoor}, {tags['room-name']} - {tags['room-no']}
        </Text>
      </View>
  ));
}

export default function QueryTest() {
  return (
    <Polygons />
  );
};
