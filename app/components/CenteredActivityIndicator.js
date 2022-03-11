import React from 'react';
import { View, ActivityIndicator, Text } from 'react-native';
import { styles } from './styles';

export const CenteredActivityIndicator = ({ text }) => {
  return (
    <View style={styles.centerAbsolute}>
      <ActivityIndicator size="large" color={'#000'} />
      <Text style={styles.indicatorText}>{text}</Text>
    </View>
  );
};
