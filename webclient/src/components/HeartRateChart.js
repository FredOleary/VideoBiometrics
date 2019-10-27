import React, { Component } from 'react';
import {Chart, Line} from 'react-chartjs-2';
import { connect } from "react-redux";


const mapStateToProps = state => {
    return { chartData: state.chartData, selectedDevice: state.selectedDevice, devices: state.devices };
  };

const getIndex = (chart,tooltipItem) =>{
   
    return tooltipItem.index
}
let chartComponent = null;


  class ConnectedHeartRateChart extends Component {
    componentDidMount() {
        chartComponent = this;
    }
    render() {
        return (<div className = "chart">
                <Line
                    data={this.getChartData()}
                    options={{
                        tooltips: {
                            callbacks: {
                                label: tooltipItem => {return "Index-" + chartComponent.getIndex(tooltipItem)}
                                // label: tooltipItem => {this.getIndex.bind(this)}
                                // label: function(tooltipItem) {
                                //     return "Index-" + getIndex(HeartRateChart, tooltipItem);
                                // }
                            }
                        },
                        maintainAspectRatio: true,
                        scales: {
                            yAxes: [{
                                id:'A',
                                position:'left',
                                scaleLabel:{
                                    display:true,
                                    labelString:"Beats Per Minute",
                                    fontColor: "blue"
                                },
                                ticks: {
                                    beginAtZero:false,
                                    min: 40,
									max: 140,
									stepSize: 10,
                                }
                             },{
                                id:'B',
                                position:'right',
                                scaleLabel:{
                                    display:true,
                                    labelString:"Frame rate/FFT Confidence",
                                    fontColor: "red"
                                },
                               ticks: {
                                    beginAtZero:true,
									max: 100,
									stepSize: 10,
                                }
                            }],
                            xAxes: [{
                                ticks: {
                                    autoSkip: true,
                                    autoSkipPadding: 30
                                }
                            }]

                        },
                        title: {
                            display: true,
                            text: 'Heart Rate (BPM)',
                            position:"bottom"
                        }

                    }}
                />
            </div>
        );
    }
    getChartData = () =>{
        console.log("Get Chart Data")
        return this.props.chartData;
    }
    getIndex = tooltipItem =>{
        if( this.props.chartData.source && this.props.chartData.source.length > 0 ){
            let value = tooltipItem.value
            let deviceId = this.props.chartData.source[tooltipItem.index].DeviceId;
            for (let index = 0; index < this.props.devices.length; index++) { 
                if( this.props.devices[index].entry.id == deviceId){
                    let source = this.props.devices[index] .label;
                    return "Value: " +  value + ", Source: " + source;
                }
            }
        }
        return "Value: " +  tooltipItem.value;
    }
}
const HeartRateChart = connect(
    mapStateToProps,
)(ConnectedHeartRateChart);

export default HeartRateChart;
