import React from 'react';
import {Text, StyleSheet, View, SafeAreaView, FlatList} from 'react-native';
import {useQuery, gql} from '@apollo/client';

var styles = StyleSheet.create({
  container: {
    backgroundColor: '#333',
    marginHorizontal: 20,
    flexGrow: 1,
  }, 
  item: {
    backgroundColor: '#555',
    padding: 20,
    marginVertical: 8,
    marginHorizontal: 16,
  },
  text: {
    fontSize: 20,
    color: '#ddd',
  },
});

const NODES = gql`
  query Nodes {
    polygons(graph: "test_bragg") {
      id
      tags
    }
  }
`;

const Item = ({ text }) => (
  <View style={styles.item}>
    <Text style={styles.text}>{text}</Text>
  </View>
);

function Polygons() {
  const {loading, error, data} = useQuery(NODES);
  if (loading) return <Text styles={styles.text}>Loading...</Text>;
  if (error) return <Text styles={styles.text}>Error!</Text>;

  return data.polygons;
}

export default function QueryTest() {
  const data = Polygons();

  function renderItem(item) {
    const object = item.item;
    const text = `${object.id}: ${object.tags['room-name']} - ${object.tags['room-no']}`;
    return <Item text={text} />;
  }

  return (
    <SafeAreaView style={styles.container}> 
      <FlatList 
        data={data} 
        renderItem={renderItem}
        keyExtractor={item => item.id}
      />
    </SafeAreaView>
  );
}