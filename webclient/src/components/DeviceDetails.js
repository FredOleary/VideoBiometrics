import React, { Component } from 'react';
import { connect } from "react-redux";
import DeviceEntry from './DeviceEntry';

const mapStateToProps = state => {
    return { devices: state.devices, selectedDevice: state.selectedDevice, chartData: state.chartData };
  };

class ConnectedDeviceDetails extends Component{
    render(){
        return (
            <div style = {{marginTop:"20px"}}>
                <DeviceEntry label="Device" value={this.getDeviceInfo("name")}/>
                <br/>
                <DeviceEntry label="ID" value={this.getDeviceInfo("id")}/>
                <DeviceEntry label="Description" value={this.getDeviceInfo("description")}/>
                <DeviceEntry label="Error" value={this.getErrorInfo("description")}/>
                
          </div>
        )
    }
    getDeviceInfo = (info)=>{
        if(this.props.selectedDevice.hasOwnProperty("entry") ){
            return this.props.selectedDevice.entry[info];
        }
        return null;
    }
    getErrorInfo = () =>{
        if( this.props.chartData.datasets.length > 0 ){
            console.log("foo")
        }
        return "N/A"
    }
};


const DeviceDetails = connect(
    mapStateToProps,
)(ConnectedDeviceDetails);
export default DeviceDetails