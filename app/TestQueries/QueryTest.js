import React from 'react';
import {
  Text,
  StyleSheet,
  SafeAreaView,
  FlatList,
  TextInput,
  TouchableOpacity,
} from 'react-native';
import { useQuery, gql } from '@apollo/client';

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
    padding: 15,
    marginVertical: 5,
    marginHorizontal: '10%',
  },
  text: {
    fontSize: 20,
    color: '#ddd',
  },
});

const POLYGONS = gql`
  query polygons($search: String!) {
    search_polygons(graph: "test_bragg", search: $search) {
      id
      tags
    }
  }
`;

const Item = ({ text, onPress, backgroundColor }) => (
  <TouchableOpacity onPress={onPress} style={[styles.item, backgroundColor]}>
    <Text style={styles.text}>{text}</Text>
  </TouchableOpacity>
);

function Polygons(search) {
  const { loading, error, data } = useQuery(POLYGONS, {
    variables: { search },
  });
  if (loading) {
    return ['Loading...'];
  }
  if (error) {
    console.log(error);
    return ['Error'];
  }

  return data.search_polygons;
}

export default function QueryTest() {
  const [searchText, onSearchTextChange] = React.useState('');
  const [selectedId, setSelectedId] = React.useState();
  const data = Polygons(searchText);

  function renderItem(obj_data) {
    if (typeof obj_data.item === 'string') {
      return (
        <Item
          text={obj_data.item}
          onPress={() => {}}
          backgroundColor={'#777'}
        />
      );
    }

    const backgroundColor = obj_data.id === selectedId ? '#555' : '#777';
    const object = obj_data.item;
    const text = `${object.tags['room-name']} - ${object.tags['room-no']}`;
    return (
      <Item
        text={text}
        onPress={() => setSelectedId(obj_data.id)}
        backgroundColor={{ backgroundColor }}
      />
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <TextInput
        style={styles.input}
        onChangeText={onSearchTextChange}
        value={searchText}
        placeholder="Search for a room"
      />
      <FlatList data={data} renderItem={renderItem} />
    </SafeAreaView>
  );
}
