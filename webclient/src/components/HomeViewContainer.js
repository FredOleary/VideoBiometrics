import React from 'react';
import Toolbar from './Toolbar';
import HeartRateChart from './HeartRateChart';
import DeviceDetails from './DeviceDetails';

export const HomeViewContainer = ({ component: Component, ...rest }) => (
	<div className="HomeView">
        <div className="HomeViewToolbar">
            <Toolbar/>
        </div>
        <div className="HomeViewContent">
            <div className="HomeViewDeviceDetails">
                <DeviceDetails/>
            </div>
            <div className="HomeViewChart">
                <HeartRateChart/>
            </div>
         </div>
    </div>
);

