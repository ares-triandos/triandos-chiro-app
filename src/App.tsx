import React, { useEffect, useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { ActivityIndicator, View } from 'react-native';
import auth from '@react-native-firebase/auth';
import firestore from '@react-native-firebase/firestore';

// Screens
import LoginScreen from './screens/auth/LoginScreen';
import SignupScreen from './screens/auth/SignupScreen';
import AppointmentsScreen from './screens/patient/AppointmentsScreen';
import ScriptsScreen from './screens/patient/ScriptsScreen';
import SettingsScreen from './screens/patient/SettingsScreen';

// Navigation setup
const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

const AuthStack = () => (
  <Stack.Navigator
    screenOptions={{
      headerShown: false,
      animationEnabled: true,
    }}>
    <Stack.Screen name="Login" component={LoginScreen} />
    <Stack.Screen name="Signup" component={SignupScreen} />
  </Stack.Navigator>
);

const PatientTabs = () => (
  <Tab.Navigator
    screenOptions={{
      tabBarActiveTintColor: '#0F7EA8',
      tabBarInactiveTintColor: '#999',
      headerShown: true,
    }}>
    <Tab.Screen
      name="Appointments"
      component={AppointmentsScreen}
      options={{
        tabBarLabel: 'Book',
      }}
    />
    <Tab.Screen
      name="Scripts"
      component={ScriptsScreen}
      options={{
        tabBarLabel: 'Scripts',
      }}
    />
    <Tab.Screen
      name="Settings"
      component={SettingsScreen}
      options={{
        tabBarLabel: 'Settings',
      }}
    />
  </Tab.Navigator>
);

const App = () => {
  const [initializing, setInitializing] = useState(true);
  const [user, setUser] = useState(null);

  useEffect(() => {
    const subscriber = auth().onAuthStateChanged(user => {
      setUser(user);
      setInitializing(false);
    });

    return subscriber;
  }, []);

  if (initializing)
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <ActivityIndicator size="large" color="#0F7EA8" />
      </View>
    );

  return (
    <NavigationContainer>
      {user ? <PatientTabs /> : <AuthStack />}
    </NavigationContainer>
  );
};

export default App;
