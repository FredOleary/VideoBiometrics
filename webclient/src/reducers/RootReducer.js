import { UPDATE_DEVICE, UPDATE_HEARTRATE, UPDATE_SELECTED_DEVICE } from "../constants/actionTypes";

const initialState = {
    devices: [],
    chartData:{datasets: []},
    selectedDevice: {}
  };
  function rootReducer(state = initialState, action) {
    let newState;
    switch (action.type){
        case UPDATE_DEVICE:
            newState = {...state}
            newState.devices = action.devices;
            newState.selectedDevice ={};
            return newState;
        case UPDATE_HEARTRATE:
            newState = {...state}
            newState.chartData = action.chartData;
            return newState;
         case UPDATE_SELECTED_DEVICE:
            newState = {...state}
            newState.selectedDevice = action.selectedDevice;
          return newState;
       default:
            break;
    }
    return state;
  };
  export default rootReducer;