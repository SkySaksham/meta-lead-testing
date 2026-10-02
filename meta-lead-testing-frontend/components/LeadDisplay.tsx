import { View, Text } from 'react-native';
import { useStore } from '../store/store';

export default function LeadDisplay() {
  const leads = useStore((state) => state.leads);

  return (
    <View>
      {leads.length === 0 ? (
        <Text>No leads</Text>
      ) : (
        leads.map((lead, index) => (
          <View key={index}>
            <Text>{lead.name}</Text>
            <Text>{lead.phone}</Text>
            <Text>{lead.email}</Text>
          </View>
        ))
      )}
    </View>
  );
}