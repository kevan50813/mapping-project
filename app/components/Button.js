import React from 'react';
import { Text, Pressable } from 'react-native';
import { styles } from './styles';

export const Button = ({ title, onPress }) => (
  <Pressable style={styles.button} onPress={onPress}>
    <Text style={styles.buttonText}>{title}</Text>
  </Pressable>
);
