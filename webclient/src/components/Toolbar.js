import React, { Component } from 'react';
import Select from 'react-select';
import {devicesActions} from '../actions/devicesAction';
import { connect } from "react-redux";
import {bindActionCreators} from "redux";

const breadLogo = require('.././images/heart2.png');


// const options = [
//     { value:1, label:'one'}, 
 //    { value:2, label:'two'},
 //    { value:3, label:'three'}
 //  ];
// const defaultOption = options[1];

const toolbar = {
    backgroundColor: 'rgb(200,200,200)' ,
    display:'flex'
};

const deviceSelector = {
    width:500,
    backgroundColor: 'rgb(200,200,200)',
    marginLeft:'30px',
    marginTop:'auto',
    marginBottom:'auto',
    textAlign:'left'
};

const refreshButton = {
    backgroundColor: 'rgb(200,200,200)',
    marginLeft:'30px',
    marginTop:'auto',
    marginBottom:'auto',
    textAlign:'center'
};

const logo = {
    width:50,
    backgroundColor: 'rgb(200,200,200)',
    marginLeft: 'auto',
    marginRight: '30px'
};
const imageStyle ={
    maxWidth:'100%',
    maxHeight:'100%'
}
const duration ={
    marginLeft:'30px',
    marginTop:'auto',
    marginBottom:'auto',
 //   textAlign:'center'

}
const mapStateToProps = state => {
    return { devices: state.devices, selectedDevice: state.selectedDevice, chartData: state.chartData };
  };
function mapDispatchToProps(dispatch) {
    return {
        devicesActions: bindActionCreators(devicesActions, dispatch)
    };
}
  
class ConnectedToolbar extends Component{
    componentDidMount() {
        console.log("ConnectedToolbar-componentDidMount");
        this.selectedItem = null;
        this.props.devicesActions.fetchDevices();
        // setInterval( this.onAutoUpdate.bind(this), 10000);
     }
    render(){
        return (
            <div style = {toolbar} >
                <div style ={deviceSelector}>
                    <Select options={this.getDeviceAndVideo()} onChange={this.onSelectChange.bind(this)} />
                </div>
                <div style={refreshButton}>
                    <button disabled ={this.isSelectedEmpty()} onClick={this.onRefresh.bind(this)} style ={{height:30, fontSize:'16px'}}>Refresh</button>
                </div>
                <div style = {logo}>
                    <img style={imageStyle} src={breadLogo} alt="Bread icon" />
                </div>
            </div>
        )
    }
    getDeviceAndVideo(){
        return this.props.devices;
    }
    onSelectChange( selectedItem ){
        this.selectedItem = selectedItem;
        if( selectedItem){
            this.props.devicesActions.updateSelectedDevice(selectedItem);
            this.props.devicesActions.fetchHeartRateForDevice( selectedItem.value);
        }
    }
    isSelectedEmpty(){
        return JSON.stringify(this.props.selectedDevice) === JSON.stringify({});
    }
 
    onRefresh(){
        this.props.devicesActions.fetchHeartRateForDevice( this.props.selectedDevice.value);
     }
    onAutoUpdate(){
        if( this.selectedItem ){
            let batchEndTime = new Date( this.selectedItem.endDate);
            let nowDate = new Date();
            if( batchEndTime > nowDate){
                console.log("refreshing");      
                this.props.batchesActions.fetchHeartRateForDevice( this.props.selectedBatch.value);                        
            }else{
                console.log("batch has ended");               
            }
        }
      }
}
const Toolbar = connect(
    mapStateToProps,
    mapDispatchToProps
)(ConnectedToolbar);
export default Toolbar