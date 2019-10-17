import React, { Component } from 'react';
import {Chart, Line} from 'react-chartjs-2';
import { connect } from "react-redux";


const mapStateToProps = state => {
    return { chartData: state.chartData, selectedDevice: state.selectedDevice };
  };



  class ConnectedHeartRateChart extends Component {

    render() {
        return (<div className = "chart">
                <Line
                    data={this.getChartData()}
                    options={{
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
                                    beginAtZero:true,
									max: 200,
									stepSize: 20,
                                }
                             },{
                                id:'B',
                                position:'right',
                                scaleLabel:{
                                    display:true,
                                    labelString:"Frame rate",
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
}
const HeartRateChart = connect(
    mapStateToProps,
)(ConnectedHeartRateChart);

export default HeartRateChart;
