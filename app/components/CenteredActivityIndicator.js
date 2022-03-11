import React from 'react';
import { View, ActivityIndicator, Text } from 'react-native';
import { styles } from './styles';

export const CenteredActivityIndicator = ({ text }) => {
  return (
    <View style={styles.centerAbsolute}>
      <ActivityIndicator size="large" color="#4c94eb" />
      <Text style={styles.indicatorText}>{text}</Text>
    </View>
  );
};
