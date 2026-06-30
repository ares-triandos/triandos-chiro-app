import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  Alert,
  ActivityIndicator,
} from 'react-native';
import auth from '@react-native-firebase/auth';
import firestore from '@react-native-firebase/firestore';
import { Calendar } from 'react-native-calendars';
import { format } from 'date-fns';

const AppointmentsScreen = () => {
  const [appointments, setAppointments] = useState([]);
  const [selectedDate, setSelectedDate] = useState('');
  const [loading, setLoading] = useState(true);
  const [showBooking, setShowBooking] = useState(false);

  useEffect(() => {
    fetchAppointments();
  }, []);

  const fetchAppointments = async () => {
    try {
      const user = auth().currentUser;
      if (!user) return;

      const snapshot = await firestore()
        .collection('patients')
        .doc(user.uid)
        .collection('appointments')
        .orderBy('dateTime', 'asc')
        .get();

      setAppointments(snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() })));
    } catch (error) {
      console.error('Error fetching appointments:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleBookAppointment = async () => {
    if (!selectedDate) {
      Alert.alert('Error', 'Please select a date');
      return;
    }

    try {
      const user = auth().currentUser;
      if (!user) return;

      await firestore()
        .collection('patients')
        .doc(user.uid)
        .collection('appointments')
        .add({
          dateTime: selectedDate,
          status: 'scheduled',
          notes: '',
          createdAt: firestore.FieldValue.serverTimestamp(),
        });

      Alert.alert('Success', 'Appointment booked!');
      setSelectedDate('');
      setShowBooking(false);
      fetchAppointments();
    } catch (error: any) {
      Alert.alert('Error', error.message);
    }
  };

  const handleCancelAppointment = async (appointmentId: string) => {
    try {
      const user = auth().currentUser;
      if (!user) return;

      await firestore()
        .collection('patients')
        .doc(user.uid)
        .collection('appointments')
        .doc(appointmentId)
        .delete();

      Alert.alert('Success', 'Appointment cancelled');
      fetchAppointments();
    } catch (error: any) {
      Alert.alert('Error', error.message);
    }
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
      {!showBooking ? (
        <>
          <View style={styles.headerSection}>
            <Text style={styles.sectionTitle}>Your Appointments</Text>
            <TouchableOpacity
              style={styles.bookButton}
              onPress={() => setShowBooking(true)}>
              <Text style={styles.bookButtonText}>+ Book Appointment</Text>
            </TouchableOpacity>
          </View>

          <FlatList
            data={appointments}
            keyExtractor={item => item.id}
            renderItem={({ item }) => (
              <View style={styles.appointmentCard}>
                <View style={styles.appointmentInfo}>
                  <Text style={styles.appointmentDate}>{item.dateTime}</Text>
                  <Text style={styles.appointmentStatus}>{item.status}</Text>
                </View>
                <TouchableOpacity
                  style={styles.cancelButton}
                  onPress={() =>
                    Alert.alert(
                      'Cancel Appointment?',
                      'Are you sure?',
                      [
                        { text: 'No', onPress: () => {} },
                        {
                          text: 'Yes',
                          onPress: () =>
                            handleCancelAppointment(item.id),
                        },
                      ]
                    )
                  }>
                  <Text style={styles.cancelButtonText}>Cancel</Text>
                </TouchableOpacity>
              </View>
            )}
            ListEmptyComponent={
              <View style={styles.emptyState}>
                <Text style={styles.emptyText}>No appointments yet</Text>
                <Text style={styles.emptySubtext}>
                  Book one to get started
                </Text>
              </View>
            }
          />
        </>
      ) : (
        <View style={styles.bookingContainer}>
          <TouchableOpacity
            style={styles.backButton}
            onPress={() => setShowBooking(false)}>
            <Text style={styles.backButtonText}>← Back</Text>
          </TouchableOpacity>

          <Text style={styles.sectionTitle}>Select a Date</Text>
          <Calendar
            onDayPress={day => setSelectedDate(day.dateString)}
            markedDates={{
              [selectedDate]: {
                selected: true,
                selectedColor: '#0F7EA8',
              },
            }}
          />

          <TouchableOpacity
            style={styles.confirmButton}
            onPress={handleBookAppointment}>
            <Text style={styles.confirmButtonText}>Book This Date</Text>
          </TouchableOpacity>
        </View>
      )}
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
    marginBottom: 12,
  },
  bookButton: {
    backgroundColor: '#0F7EA8',
    paddingVertical: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  bookButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  appointmentCard: {
    backgroundColor: '#fff',
    marginHorizontal: 16,
    marginVertical: 8,
    padding: 16,
    borderRadius: 8,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  appointmentInfo: {
    flex: 1,
  },
  appointmentDate: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  appointmentStatus: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
  cancelButton: {
    paddingVertical: 8,
    paddingHorizontal: 12,
    backgroundColor: '#f5f5f5',
    borderRadius: 6,
  },
  cancelButtonText: {
    color: '#d32f2f',
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
  bookingContainer: {
    flex: 1,
    paddingHorizontal: 16,
    paddingVertical: 16,
    backgroundColor: '#fff',
  },
  backButton: {
    paddingVertical: 8,
    marginBottom: 16,
  },
  backButtonText: {
    color: '#0F7EA8',
    fontSize: 16,
    fontWeight: '600',
  },
  confirmButton: {
    backgroundColor: '#0F7EA8',
    paddingVertical: 14,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 20,
  },
  confirmButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});

export default AppointmentsScreen;
