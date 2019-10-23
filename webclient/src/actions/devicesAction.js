import { UPDATE_DEVICE, UPDATE_HEARTRATE, UPDATE_SELECTED_DEVICE } from "../constants/actionTypes";
import { axiosService } from '../services/axiosService';
import { all } from "q";

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
                let result = {createdAt:[], sumFFTs:[], greenFFT:[], groundTruth:[], fps:[],FFTConfidence:[] }
				if(response.status === 200){
                    result.createdAt = response.data.map( entry =>{
                        return (new Date(entry.createdAt)).toLocaleString();
                    });
                    // result.sumFFTs = response.data.map( entry => {return entry.sumFFTs});
                    // result.correlatedFFTs = response.data.map( entry => {return entry.correlatedFFTs});
                    // result.correlatedPkPk = response.data.map( entry => {return entry.correlatedPkPk});
                    // result.verticalPkPk = response.data.map( entry => {return entry.verticalPkPk});
                    // result.verticalFFT = response.data.map( entry => {return entry.verticalFFT});
                    result.greenPkPk = response.data.map( entry => {return entry.greenPkPk});
                    result.greenFFT = response.data.map( entry => {return entry.greenFFT});
                    result.groundTruth = response.data.map( entry => {return entry.groundTruth});
                    result.fps = response.data.map( entry => {return entry.fps});
                    result.FFTConfidence = response.data.map( entry => {return entry.FFTConfidence});
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
        datasets: []
    };
    if( heartRate.length == 0 ){
        return chartData;
    }
    if( heartRate.createdAt.length > 0 ){
        chartData.labels = heartRate.createdAt; 
        let greenFFT = {};
        greenFFT.data = heartRate.greenFFT;
        greenFFT.backgroundColor='rgb(0, 80, 0)';
        greenFFT.fill=false;
		greenFFT.pointRadius=0;
        greenFFT.borderColor='rgb(0, 80, 0)';
        greenFFT.label = "Green FFT";
        greenFFT.lineTension = 0;
        greenFFT.yAxisID = 'A';
        chartData.datasets.push( greenFFT);

        let greenPkPk = {};
        greenPkPk.data = heartRate.greenPkPk;
        greenPkPk.backgroundColor='rgb(80, 255, 80)';
        greenPkPk.fill=false;
		greenPkPk.pointRadius=0;
        greenPkPk.borderColor='rgb(80, 255, 80)';
        greenPkPk.label = "Green Pk-Pk";
        greenPkPk.lineTension = 0;
        greenPkPk.yAxisID = 'A';
        chartData.datasets.push( greenPkPk);

        let groundTruth = {};
        groundTruth.data = heartRate.groundTruth;
        groundTruth.backgroundColor='rgb(220, 200, 00)';
        groundTruth.fill=false;
		groundTruth.pointRadius=0;
        groundTruth.borderColor='rgb(220, 200, 00)';
        groundTruth.label = "HR - Ground Truth";
        groundTruth.lineTension = 0;
        groundTruth.yAxisID = 'A';
        chartData.datasets.push( groundTruth);
       
        let fps = {};
        fps.data = heartRate.fps;
        fps.backgroundColor='rgb(255, 0, 0)';
        fps.fill=false;
		fps.pointRadius=0;
        fps.borderColor='rgb(255, 0, 0)';
        fps.label = "Frames per second (fps)";
        fps.lineTension = 0;
        fps.yAxisID = 'B';
        chartData.datasets.push( fps);

        let FFTConfidence = {};
        FFTConfidence.data = heartRate.FFTConfidence;
        FFTConfidence.backgroundColor='rgb(53, 53, 183)';
        FFTConfidence.fill=false;
		FFTConfidence.pointRadius=0;
        FFTConfidence.borderColor='rgb(53, 53, 183)';
        FFTConfidence.label = "FFT Confidence (%)";
        FFTConfidence.lineTension = 0;
        FFTConfidence.yAxisID = 'B';
        chartData.datasets.push( FFTConfidence);

        // let correlatedFFTs = {};
        // correlatedFFTs.data = heartRate.correlatedFFTs;
        // correlatedFFTs.backgroundColor='rgb(80, 80, 250)';
        // correlatedFFTs.fill=false;
		// correlatedFFTs.pointRadius=0;
        // correlatedFFTs.borderColor='rgb(80, 80, 250)';
        // correlatedFFTs.label = "Correlated FFTs";
        // correlatedFFTs.lineTension = 0;
        // correlatedFFTs.yAxisID = 'A';
        // chartData.datasets.push( correlatedFFTs);

        // let correlatedPkPk = {};
        // correlatedPkPk.data = heartRate.correlatedPkPk;
        // correlatedPkPk.backgroundColor='rgb(53, 183, 91)';
        // correlatedPkPk.fill=false;
		// correlatedPkPk.pointRadius=0;
        // correlatedPkPk.borderColor='rgb(53, 183, 91)';
        // correlatedPkPk.label = "Correlated Pk-Pk";
        // correlatedPkPk.lineTension = 0;
        // correlatedPkPk.yAxisID = 'A';
        // chartData.datasets.push( correlatedPkPk);

        // let verticalFFT = {};
        // verticalFFT.data = heartRate.verticalFFT;
        // verticalFFT.backgroundColor='rgb(250, 80, 80)';
        // verticalFFT.fill=false;
		// verticalFFT.pointRadius=0;
        // verticalFFT.borderColor='rgb(250, 80, 80)';
        // verticalFFT.label = "Vertical FFT";
        // verticalFFT.lineTension = 0;
        // verticalFFT.yAxisID = 'A';
        // chartData.datasets.push( verticalFFT);


        // let verticalPkPk = {};
        // verticalPkPk.data = heartRate.verticalPkPk;
        // verticalPkPk.backgroundColor='rgb(200, 200, 91)';
        // verticalPkPk.fill=false;
		// verticalPkPk.pointRadius=0;
        // verticalPkPk.borderColor='rgb(200, 200, 91)';
        // verticalPkPk.label = "Vertical Pk-Pk";
        // verticalPkPk.lineTension = 0;
        // verticalPkPk.yAxisID = 'A';
        // chartData.datasets.push( verticalPkPk);


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