import React, { Component } from 'react';
import { ActivityIndicator, View, Text, TouchableOpacity, StyleSheet, Dimensions } from 'react-native';

const { width, height } = Dimensions.get('window');

export default class CustomActivityIndicator extends Component {

    constructor(props) {
        super(props);
        this.state = {
            show: this.props.show
        }
    }

    render() {
        return (
            <View style={styles.containerNew}>
                <ActivityIndicator
                    animating={this.state.show}
                    color="#37c100"
                    size="large" />
            </View>
        );

    }
}

const styles = StyleSheet.create({
    container: {
        position: 'absolute',
        height: 100,
        width: 100,
        padding: 20,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#F5FCFF88'
    }, containerNew: {
        position: 'absolute',
        left: 0,
        right: 0,
        top: 0,
        bottom: 0,
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: 'rgba(0,0,0,0.5)',
        zIndex:999
    }

})