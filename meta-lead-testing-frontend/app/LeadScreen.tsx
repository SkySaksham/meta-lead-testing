import { useEffect } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { LeadWebSocket } from '../services/LeadWebSocket';
import LeadDisplay from '../components/LeadDisplay';

export default function LeadScreen() {
  useEffect(() => {
    console.log('LeadScreen opened');

    const socket = new LeadWebSocket();

    console.log('Creating WebSocket...');
    socket.connect();

    return () => {
      console.log('LeadScreen closed');
      socket.disconnect();
    };
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Leads</Text>

      <LeadDisplay />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },

  title: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 20,
  },
});