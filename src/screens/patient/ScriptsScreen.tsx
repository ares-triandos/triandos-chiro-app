import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  ActivityIndicator,
  Linking,
} from 'react-native';
import auth from '@react-native-firebase/auth';
import firestore from '@react-native-firebase/firestore';

const ScriptsScreen = () => {
  const [scripts, setScripts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchScripts();
  }, []);

  const fetchScripts = async () => {
    try {
      const user = auth().currentUser;
      if (!user) return;

      const snapshot = await firestore()
        .collection('patients')
        .doc(user.uid)
        .collection('scripts')
        .orderBy('createdAt', 'desc')
        .get();

      setScripts(snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() })));
    } catch (error) {
      console.error('Error fetching scripts:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleViewScript = (url: string) => {
    Linking.openURL(url);
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#0F7EA8" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.headerSection}>
        <Text style={styles.sectionTitle}>Your Scripts</Text>
        <Text style={styles.subtitle}>Treatment recommendations and exercises</Text>
      </View>

      <FlatList
        data={scripts}
        keyExtractor={item => item.id}
        renderItem={({ item }) => (
          <View style={styles.scriptCard}>
            <View style={styles.scriptInfo}>
              <Text style={styles.scriptTitle}>{item.title}</Text>
              <Text style={styles.scriptDate}>
                {new Date(item.createdAt?.toDate?.() || new Date()).toLocaleDateString()}
              </Text>
              {item.description && (
                <Text style={styles.scriptDescription}>{item.description}</Text>
              )}
            </View>
            <TouchableOpacity
              style={styles.viewButton}
              onPress={() => handleViewScript(item.url)}>
              <Text style={styles.viewButtonText}>View</Text>
            </TouchableOpacity>
          </View>
        )}
        ListEmptyComponent={
          <View style={styles.emptyState}>
            <Text style={styles.emptyText}>No scripts yet</Text>
            <Text style={styles.emptySubtext}>
              Check back after your appointment
            </Text>
          </View>
        }
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f9f9f9',
    paddingTop: 10,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  headerSection: {
    paddingHorizontal: 16,
    paddingVertical: 16,
    backgroundColor: '#fff',
  },
  sectionTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 14,
    color: '#666',
  },
  scriptCard: {
    backgroundColor: '#fff',
    marginHorizontal: 16,
    marginVertical: 8,
    padding: 16,
    borderRadius: 8,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  scriptInfo: {
    flex: 1,
  },
  scriptTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 4,
  },
  scriptDate: {
    fontSize: 12,
    color: '#999',
  },
  scriptDescription: {
    fontSize: 13,
    color: '#666',
    marginTop: 8,
    fontStyle: 'italic',
  },
  viewButton: {
    paddingVertical: 8,
    paddingHorizontal: 16,
    backgroundColor: '#0F7EA8',
    borderRadius: 6,
  },
  viewButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  emptyState: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 60,
  },
  emptyText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
  },
  emptySubtext: {
    fontSize: 14,
    color: '#999',
  },
});

export default ScriptsScreen;
