import React, { Component } from 'react';
import { connect } from "react-redux";
import DeviceEntry from './DeviceEntry';

const mapStateToProps = state => {
    return { devices: state.devices, selectedDevice: state.selectedDevice };
  };

class ConnectedDeviceDetails extends Component{
    render(){
        return (
            <div style = {{marginTop:"20px"}}>
                <DeviceEntry label="Device" value={this.getDeviceInfo("name")}/>
                <br/>
                <DeviceEntry label="ID" value={this.getDeviceInfo("id")}/>
                <DeviceEntry label="Description" value={this.getDeviceInfo("description")}/>
                
          </div>
        )
    }
    getDeviceInfo = (info)=>{
        if(this.props.selectedDevice.hasOwnProperty("entry") ){
            return this.props.selectedDevice.entry[info];
        }
        return null;
    }
};


const DeviceDetails = connect(
    mapStateToProps,
)(ConnectedDeviceDetails);
export default DeviceDetails