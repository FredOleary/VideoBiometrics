import React, { Component } from 'react';
import {Chart, Line} from 'react-chartjs-2';
import { connect } from "react-redux";


const mapStateToProps = state => {
    return { chartData: state.chartData, selectedDevice: state.selectedDevice };
  };

const getIndex = (chart,tooltipItem) =>{
   
    return tooltipItem.index
}


  class ConnectedHeartRateChart extends Component {

    render() {
        return (<div className = "chart">
                <Line
                    data={this.getChartData()}
                    options={{
                        tooltips: {
                            callbacks: {
                                label: function(tooltipItem) {
                                    return "Index-" + getIndex(HeartRateChart, tooltipItem);
                                }
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
        console.log(this.props.chartData)
        return tooltipItem.index
    }
}
const HeartRateChart = connect(
    mapStateToProps,
)(ConnectedHeartRateChart);

export default HeartRateChart;
