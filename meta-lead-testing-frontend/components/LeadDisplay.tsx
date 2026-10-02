import { View, Text, StyleSheet } from 'react-native';
import { useStore } from '../store/store';

export default function LeadDisplay() {
  const leads = useStore((state) => state.leads);

  if (leads.length === 0) {
    return (
      <View style={styles.empty}>
        <Text style={styles.emptyText}>No leads</Text>
      </View>
    );
  }

  return (
    <View style={styles.table}>
      {/* Header */}
      <View style={[styles.row, styles.header]}>
        <Text style={[styles.cell, styles.headerText]}>Leadgen ID</Text>
        <Text style={[styles.cell, styles.headerText]}>Name</Text>
        <Text style={[styles.cell, styles.headerText]}>Phone</Text>
        <Text style={[styles.cell, styles.headerText]}>Email</Text>
      </View>

      {/* Rows */}
      {leads.map((lead, index) => (
        <View style={styles.row} key={index}>
          <Text style={styles.cell}>{lead.leadgen_id}</Text>
          <Text style={styles.cell}>{lead.name}</Text>
          <Text style={styles.cell}>{lead.phone}</Text>
          <Text style={styles.cell}>{lead.email}</Text>
        </View>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  table: {
    width: '95%',
    borderWidth: 1,
    borderRadius: 8,
    overflow: 'hidden',
  },

  row: {
    flexDirection: 'row',
    borderBottomWidth: 1,
    paddingVertical: 12,
  },

  header: {
    backgroundColor: '#eee',
  },

  cell: {
    flex: 1,
    paddingHorizontal: 8,
    fontSize: 14,
  },

  headerText: {
    fontWeight: 'bold',
  },

  empty: {
    padding: 20,
    alignItems: 'center',
  },

  emptyText: {
    fontSize: 16,
    color: '#777',
  },
});