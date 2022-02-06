import React from 'react';
import {
  Text,
  StyleSheet,
  View,
  SafeAreaView,
  FlatList,
  TextInput,
} from 'react-native';
import {useQuery, gql} from '@apollo/client';

var styles = StyleSheet.create({
  input: {
    backgroundColor: '#777',
    padding: 20,
    marginVertical: 8,
    marginHorizontal: 16,
  },
  container: {
    backgroundColor: '#333',
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

const POLYGONS = gql`
  query polygons ($search: String!) {
    search_polygons (graph: "test_bragg", search: $search) {
      id
      tags
    }
  }
`;

const Item = ({text}) => (
  <View style={styles.item}>
    <Text style={styles.text}>{text}</Text>
  </View>
);

function Polygons(search) {
  const {loading, error, data} = useQuery(POLYGONS, {variables: {search}});
  if (loading) {
    return <Text styles={styles.text}>Loading...</Text>;
  }
  if (error) {
    console.log(error)
    return <Text styles={styles.text}>Error!</Text>;
  }

  return data.polygons;
}

export default function QueryTest() {
  const [text, onChangeText] = React.useState();
  const data = Polygons(text);

  function renderItem(item) {
    const object = item.item;
    const text = `${object.id}: ${object.tags['room-name']} - ${object.tags['room-no']}`;
    return <Item text={text} />;
  }

  return (
    <SafeAreaView style={styles.container}>
      <TextInput
        style={styles.input}
        onChangeText={onChangeText}
        value={text}
        placeholder='Search for a room'
      />
      <FlatList
        data={data}
        renderItem={renderItem}
        keyExtractor={item => item.id}
      />
    </SafeAreaView>
  );
}
