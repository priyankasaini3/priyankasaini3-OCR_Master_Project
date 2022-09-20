import * as React from 'react';
import { Text, View } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Icon from 'react-native-vector-icons/Ionicons';
import Tesseract from './src/components/tesseract'
import Aws from './src/components/aws'
import Vision from './src/components/vision'

const Tab = createBottomTabNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator  screenOptions={({ route }) => ({
          tabBarActiveTintColor: 'tomato',
          tabBarInactiveTintColor: '#87cefa',
        })}>
        <Tab.Screen name="Tesseract" component={Tesseract} options={{
      tabBarLabel: 'Tesseract',
      tabBarIcon:({color})=>(  
        <Icon name="cube-sharp" color={color} size={25}/>  
    )  ,
    tabBarOptions: { activeTintColor:'tomato',inactiveTintColor:'#87cefa' }
    }} />
        <Tab.Screen name="Google Vision" component={Vision}  options={{
      tabBarLabel: 'Google Vision',
      tabBarIcon:({color})=>(  
        <Icon name="logo-google" color={color} size={25}/>  
    )  ,
    tabBarOptions: { activeTintColor:'tomato',inactiveTintColor:'#87cefa' }
    }}/>
        <Tab.Screen name="AWS" component={Aws} options={{
      tabBarLabel: 'AWS',
      tabBarIcon:({color})=>(  
        <Icon name="cloud-circle-outline" color={color} size={25}/>  
    )  ,
    tabBarOptions: { activeTintColor:'tomato',inactiveTintColor:'#87cefa' }
    }}/>
      </Tab.Navigator>
    </NavigationContainer>
  );
}