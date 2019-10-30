import { UPDATE_DEVICE, UPDATE_HEARTRATE, UPDATE_SELECTED_DEVICE } from "../constants/actionTypes";
import {CHART_HR_TRUTH_LABEL, CHART_COLOR_FFT_LABEL, CHART_CONFIDENCE_LABEL, 
    CHART_COLOR_PK_PK_LABEL, CHART_FPS_LABEL, FFT_ERROR_LABEL, PKPK_ERROR_LABEL} from "../constants/chartTypes";

import { axiosService } from '../services/axiosService';

const COLUMN_PK_PK = 'colorPkPk';
const COLUMN_FFT = 'colorFFT';

const arrAvg = arr => arr.reduce((a,b) => a + b, 0) / arr.length

function updateDevices(devices) {
    return { type: UPDATE_DEVICE, devices: devices }
};

function updateSelectedDevice(selectedDevice) {
    return { type: UPDATE_SELECTED_DEVICE, selectedDevice: selectedDevice }
};

function updateHeartRate(heartRate) {
    let chartData = createChartData( heartRate);
    return { type: UPDATE_HEARTRATE, chartData }
};

function fetchDevices() {
	return dispatch => {
		axiosService('/devices')
			.then(response => {
				if(response.status === 200){
                    let devices = response.data.map( entry =>{
                        let label = entry.name + " - " + entry.video ;
                        return ({entry:entry, value:entry.id, label:label});
                    });
                    let allDevices = {label:"All heart rate data", value:-1, entry:null, entry:{name:"All", id:-1, description:"All Heart rate data"}}
                    devices.unshift(allDevices)
					dispatch(updateDevices(devices));
				}else{
					dispatch(updateDevices([]));

				}
			})
			.catch( error =>{
				// This means the service isn't running.
				dispatch(updateDevices([]))
			});
	};
}

function fetchHeartRateForDevice( deviceId) {
    let params = {deviceId:deviceId};
	return dispatch => {
		axiosService.get('/heartrate', {params})
			.then(response => {
                let result = {source:null, createdAt:[], colorPkPk:[], colorFFT:[], groundTruth:[], fps:[],
                    FFTConfidence:[], PkPkError:[], FFTError:[], PkPkErrorAverage:0, FFTErrorAverage:0 }
				if(response.status === 200){
                    result.source = response.data
                    result.createdAt = response.data.map( entry =>{
                        return (new Date(entry.createdAt)).toLocaleString();
                    });
                     // result.verticalFFT = response.data.map( entry => {return entry.verticalFFT});
                    result.colorPkPk = response.data.map( entry => {return entry[COLUMN_PK_PK]});
                    result.colorFFT = response.data.map( entry => {return entry[COLUMN_FFT]});
                    result.groundTruth = response.data.map( entry => {return entry.groundTruth});
                    result.fps = response.data.map( entry => {return entry.fps});
                    result.FFTConfidence = response.data.map( entry => {return entry.FFTConfidence});
                    result.PkPkError =  response.data.map( (entry,index) => {
                        if(entry.groundTruth != null ){
                            let PkPkError =  Math.abs( entry[COLUMN_PK_PK] - entry.groundTruth)/ entry.groundTruth * 100
                            return Math.floor(PkPkError * 100) / 100;
                        }else{
                            return null;
                        }
                    });
                    result.PkPkErrorAverage = arrAvg(result.PkPkError);
                    
                    result.FFTError =  response.data.map( (entry,index) => {
                        if(entry.groundTruth != null ){
                            let FFTError =  Math.abs( entry[COLUMN_FFT] - entry.groundTruth)/ entry.groundTruth * 100
                            return Math.floor(FFTError * 100) / 100;
                        }else{
                            return null;
                        }
                    });
                    result.FFTErrorAverage = arrAvg(result.FFTError);
					dispatch(updateHeartRate(result));
				}else{
					dispatch(updateHeartRate([]));

				}
			})
			.catch( error =>{
				// This means the service isn't running.
				dispatch(updateHeartRate([]))
			});
	};
}

const createChartData = heartRate => {

	console.log("createChartData");
	let chartData = {
        x_axis:[],
        datasets: [],
        source:null,
        FFTErrorAverage: heartRate.FFTErrorAverage,
        PkPkErrorAverage: heartRate.PkPkErrorAverage
    };
    if( heartRate.length == 0 ){
        return chartData;
    }
    if( heartRate.createdAt.length > 0 ){
        chartData.source = heartRate.source;
        chartData.labels = heartRate.createdAt; 
        let colorFFT = {};
        colorFFT.data = heartRate.colorFFT;
        colorFFT.backgroundColor='rgb(0, 80, 0)';
        colorFFT.fill=false;
		colorFFT.pointRadius=0;
        colorFFT.borderColor='rgb(0, 80, 0)';
        colorFFT.label = CHART_COLOR_FFT_LABEL;
        colorFFT.lineTension = 0;
        colorFFT.yAxisID = 'A';
        chartData.datasets.push( colorFFT);

        let colorPkPk = {};
        colorPkPk.data = heartRate.colorPkPk;
        colorPkPk.backgroundColor='rgb(80, 255, 80)';
        colorPkPk.fill=false;
		colorPkPk.pointRadius=0;
        colorPkPk.borderColor='rgb(80, 255, 80)';
        colorPkPk.label = CHART_COLOR_PK_PK_LABEL;
        colorPkPk.lineTension = 0;
        colorPkPk.yAxisID = 'A';
        chartData.datasets.push( colorPkPk);

        let groundTruth = {};
        groundTruth.data = heartRate.groundTruth;
        groundTruth.backgroundColor='rgb(220, 200, 00)';
        groundTruth.fill=false;
		groundTruth.pointRadius=0;
        groundTruth.borderColor='rgb(220, 200, 00)';
        groundTruth.label = CHART_HR_TRUTH_LABEL;
        groundTruth.lineTension = 0;
        groundTruth.yAxisID = 'A';
        chartData.datasets.push( groundTruth);
       
        let fps = {};
        fps.data = heartRate.fps;
        fps.backgroundColor='rgb(255, 0, 0)';
        fps.fill=false;
		fps.pointRadius=0;
        fps.borderColor='rgb(255, 0, 0)';
        fps.label = CHART_FPS_LABEL;
        fps.lineTension = 0;
        fps.yAxisID = 'B';
        chartData.datasets.push( fps);

        let FFTConfidence = {};
        FFTConfidence.data = heartRate.FFTConfidence;
        FFTConfidence.backgroundColor='rgb(53, 53, 183)';
        FFTConfidence.fill=false;
		FFTConfidence.pointRadius=0;
        FFTConfidence.borderColor='rgb(53, 53, 183)';
        FFTConfidence.label = CHART_CONFIDENCE_LABEL;
        FFTConfidence.lineTension = 0;
        FFTConfidence.yAxisID = 'B';
        chartData.datasets.push( FFTConfidence);

        if(heartRate.FFTErrorAverage){
            let FFTError = {};
            FFTError.data = heartRate.FFTError;
            FFTError.backgroundColor='rgb(150,150,150)';
            FFTError.fill=false;
            FFTError.pointRadius=0;
            FFTError.borderColor='rgb(150,150,150)';
            FFTError.label = FFT_ERROR_LABEL;
            FFTError.lineTension = 0;
            FFTError.yAxisID = 'B';
            chartData.datasets.push( FFTError);
        }

        if(heartRate.PkPkErrorAverage){
            let PKPKError = {};
            PKPKError.data = heartRate.PkPkError;
            PKPKError.backgroundColor='rgb(200,200,200)';
            PKPKError.fill=false;
            PKPKError.pointRadius=0;
            PKPKError.borderColor='rgb(200,200,200)';
            PKPKError.label = PKPK_ERROR_LABEL;
            PKPKError.lineTension = 0;
            PKPKError.yAxisID = 'B';
            chartData.datasets.push( PKPKError);
        }

    }

	return chartData;
};

function deleteDevice( deviceId) {
    let params = {deviceId:deviceId};
	return dispatch => {
		axiosService.delete('/devices', {params})
			.then(response => {
                axiosService('/devices')
                .then(response => {
                    if(response.status === 200){
                        let devices = response.data.map( entry =>{
                            let label = entry.name + " - " + entry.video ;
                            return ({entry:entry, value:entry.id, label:label});
                        });
                        dispatch(updateDevices(devices));
                        dispatch(updateHeartRate([]));
                    }else{
                        dispatch(updateDevices([]));
    
                    }
                })
                .catch( error =>{
                    // This means the service isn't running.
                    dispatch(updateDevices([]))
                });
    
			})
			.catch( error =>{
				fetchDevices()
			});
    };
};

export const devicesActions = {
    updateDevices: updateDevices,
    fetchDevices: fetchDevices,
    fetchHeartRateForDevice: fetchHeartRateForDevice,
    updateSelectedDevice: updateSelectedDevice,
    deleteDevice:deleteDevice
}