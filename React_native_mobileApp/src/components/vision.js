import React, { Component } from 'react';
import { Text, View,StyleSheet ,Image,TouchableOpacity,ScrollView,KeyboardAvoidingView ,SafeAreaView,Platform,ActivityIndicator} from 'react-native';
import {launchCamera, launchImageLibrary} from 'react-native-image-picker';
import DefaultImage from '../../assets/placeholder.jpg';
import CustomActivityIndicator from '../utils/CustomActivityIndicator';
const DEFAULT_IMAGE = Image.resolveAssetSource(DefaultImage).uri;
class Vision extends Component {

    constructor(props) {
        super(props);
        this.state = {
          fileUri:DEFAULT_IMAGE,
          myComment:"",
          animating: false,
          img:'',
          fileName:"",
        };
      }
      //require('../../assets/placeholder.jpg')
      selectPicture = async() => {
        let options = {
          title: 'Select Image',
          includeBase64: true,
          quality: 0.5,
          storageOptions: {
            skipBackup: true,
            path: 'images',
          },
        };
        await launchImageLibrary(options, response => {
          console.log('Response = ', response);
          if (response.didCancel) {
            console.log('User cancelled image picker');
          } else {
            console.log('response', JSON.stringify(response));
            console.log(response.assets[0].fileName)
          
            this.setState({
              fileUri: response.assets[0].uri,
              img: response.assets[0].base64,
              fileName: response.assets[0].fileName,
            });
           
          }
        });
    
        this.setState({
          animating: true,
        })
    
    
        console.log('User cancelled image picker');
        console.log( 'image------------'+this.state.img);
       await fetch('http://ec2-13-126-63-255.ap-south-1.compute.amazonaws.com/API/upload-vision', {
                             method: 'POST',
                             headers: {
                               Accept: 'application/json',
                               'Content-Type': 'application/json',
                             },
                             body: JSON.stringify({
                               
                               fileName: this.state.fileName,
                               photo: this.state.img,
                              
                             }),
                           })
                      .then((response) => response.json())
                      .then((responseJson) => {
    
                      if(responseJson.status===200)
                      {
                       console.log('User cancelled image picker-------');
                       this.setState({
                         myComment: responseJson.text,
                       })
                       this.setState({
                         animating: false,
                       })
                       
                        }
                        else
                        {
                             data1=""
                             this.setState({
                               animating: false,
                             })
                        }
    
                      })
                      .catch((error) =>{
                       console.log(error);
                       this.setState({
                         animating: false,
                       })
                      })
    
    
    
      }
      takePicture= async() =>{
        let options = {
          title: 'Select Image',
          includeBase64: true,
          quality: 0.5,
          storageOptions: {
            skipBackup: true,
            path: 'images',
          },
        };
        await  launchCamera(options, response => {
          console.log('Response = ', response);
          if (response.didCancel) {
            console.log('User cancelled image picker');
          } else {
            console.log('response', JSON.stringify(response));
            
            console.log(response.assets[0].fileName)
          
            this.setState({
              fileUri: response.assets[0].uri,
              img: response.assets[0].base64,
              fileName: response.assets[0].fileName,
            });
          }
        });
        this.setState({
          animating: true,
        })
    
    
        console.log('User cancelled image picker');
        console.log( 'image------------'+this.state.img);
       await fetch('http://ec2-13-126-63-255.ap-south-1.compute.amazonaws.com//API/upload-vision', {
                             method: 'POST',
                             headers: {
                               Accept: 'application/json',
                               'Content-Type': 'application/json',
                             },
                             body: JSON.stringify({
                               
                               fileName: this.state.fileName,
                               photo: this.state.img,
                              
                             }),
                           })
                      .then((response) => response.json())
                      .then((responseJson) => {
    
                      if(responseJson.status===200)
                      {
                       console.log('User cancelled image picker-------');
                       this.setState({
                         myComment: responseJson.text,
                       })
                       this.setState({
                         animating: false,
                       })
                       
                        }
                        else
                        {
                             data1=""
                             this.setState({
                               animating: false,
                             })
                        }
    
                      })
                      .catch((error) =>{
                       console.log(error);
                       this.setState({
                         animating: false,
                       })
                      })
    
    
    
    
    
      }
    
     
    
    
    
        render() {
    
            return (
              <KeyboardAvoidingView  behavior={Platform.Os == "ios" ? "padding" : "height"}   keyboardVerticalOffset={100}>
              <SafeAreaView style={{padding: 10,paddingTop:10,height:'100%', backgroundColor: '#add8e6',}}>
       
                <ScrollView style={{flex: 1}}  contentInsetAdjustmentBehavior="automatic" keyboardShouldPersistTaps="handled" >
                <Image source={{uri: this.state.fileUri}} style={{margin: 10,borderRadius : 7,width: '95%',height: 250,resizeMode: 'stretch'}}/>
           
    
           <View style={{flex: 1,flexDirection: 'row',justifyContent: 'center',}}>
                 <TouchableOpacity onPress={this.selectPicture}  style={[styles.buttonContainer, styles.uploadButton]}>
                   <Text style={styles.buttonText}>Gallery</Text>
    
                 </TouchableOpacity>
                  <TouchableOpacity onPress={this.takePicture}  style={[styles.buttonContainer, styles.uploadButton]} >
                         <Text style={styles.buttonText}>Camera</Text>
                         </TouchableOpacity>
      </View>
      <Text style={styles.titleText}>Output of Google Vision OCR :-</Text>  
            <Text style={styles.boxText}>{this.state.myComment}</Text> 
    
            
            </ScrollView>
            {this.state.animating && <View style={styles.fullScreen}>
              {this.state.animating && <CustomActivityIndicator />}
            </View>}
            </SafeAreaView>
    
    
    
               </KeyboardAvoidingView>
        
    
            );
        }
    }
    
    const styles = StyleSheet.create({
        container: {
          flex: 1,
          backgroundColor: 'blue',
          alignItems: 'center',
          justifyContent: 'center',
        },
        buttonContainer: {
            height:45,
            flexDirection: 'row',
            justifyContent: 'center',
            alignItems: 'center',
            marginBottom:20,
            width:100,
            borderRadius:10,
          },
          uploadButton: {
            backgroundColor: "#3699d4",
           marginLeft: 10,
           color:"white",
          },
          buttonText:{
            color:"white"
            },
            textInputStyle: {  
              borderColor: '#9a73ef',  
              borderWidth: 1,  
              height: 100,  
              margin: 20,  
              padding: 10,  
            }, 
            fullScreen: {
              position: 'absolute',
              left: 0,
              right: 0,
              top: 0,
              bottom: 0,
          },
          titleText: {
            fontSize: 20,
            fontWeight: "bold",
            color: '#191970'
          },
          boxText: {
            fontSize: 20,
            fontWeight: "bold",
            color: '#696969'
          }
      });
export default Vision;