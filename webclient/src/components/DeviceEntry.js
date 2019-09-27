import React, { Component } from 'react';

const deviceDiv = {
    marginLeft: '10px' ,
    marginRight:'10px',
    color:"white"
};

class DeviceEntry extends Component{
    render(){
        return (
            <div>
                <div style={deviceDiv}>
                    <span style={{float:"left"}}>{this.props.label}</span><span style={{float:"right"}}>{this.props.value}</span>
                </div>
                <br/>
           </div>
        )
    }
 
};


export default DeviceEntry