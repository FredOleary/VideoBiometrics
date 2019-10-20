import React, { Component } from 'react';
import Select from 'react-select';
import {devicesActions} from '../actions/devicesAction';
import { connect } from "react-redux";
import {bindActionCreators} from "redux";

const breadLogo = require('.././images/heart2.png');


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

const toolbarButton = {
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
    select = {value:null};
    componentDidMount() {
        console.log("ConnectedToolbar-componentDidMount");
        this.selectedItem = null;
        this.select = {value:null};
        this.props.devicesActions.fetchDevices();
        // setInterval( this.onAutoUpdate.bind(this), 10000);
     }
    render(){
        return (
            <div style = {toolbar} id = "tbar" >
                <div style ={deviceSelector}>
                    <Select value={this.select.value} options={this.getDeviceAndVideo()} onChange={this.onSelectChange.bind(this)} />
                </div>
                <div style={toolbarButton}>
                    <button disabled ={this.isSelectedEmpty()} onClick={this.onRefresh.bind(this)} style ={{height:30, fontSize:'16px'}}>Refresh</button>
                </div>
                <div style={toolbarButton}>
                    <button disabled ={this.isSelectedEmpty()} onClick={this.onDelete.bind(this)} style ={{height:30, fontSize:'16px'}}>Delete...</button>
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
        this.select.value = selectedItem;
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

    onDelete(){
        this.props.devicesActions.deleteDevice( this.props.selectedDevice.value);
        this.selectedItem = null;
        this.select.value = null;
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