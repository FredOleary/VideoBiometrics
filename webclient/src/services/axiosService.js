import axios from 'axios';
import { proxy as baseURL } from '../../package.json';

const axiosOptions = {
	baseURL: process.env.NODE_ENV === 'production' ? '/' : baseURL
};

export const axiosService = axios.create(axiosOptions);

/*
 * This handles the response from the server before passing it to the next
 * `then`.
 * On a successful response, it does nothing
 *
 * In case of error, if the server responds with a status of 401, it means both the
 * token and the refresh token have expired, so we make another call to the
 * server for a new set of token and refreshToken. We then  save those to the
 * localStorage and reset the default headers of our instance and the original
 * request and finally, we re-send the original request. No interruption.
 *
 */
// axiosService.interceptors.response.use(response => response, function (error) {

// 	const originalRequest = error.config;

// 	if (error.response.status === 401 && !originalRequest._retry) {

// 		originalRequest._retry = true;

// 		const refreshToken = localStorage.getItem('refreshToken');

// 		return axiosService.post('/untapped/login/refresh', { refreshToken })
// 			.then(({data}) => {
// 				localStorage.setItem('token', data.token);
// 				localStorage.setItem('refreshToken', data.refreshToken);

// 				axiosService.defaults.headers.common['Authorization'] = 'Bearer ' + data.token;
// 				originalRequest.headers['Authorization'] = 'Bearer ' + data.token;

// 				return axiosService(originalRequest);
// 		});
// 	}

// 	return Promise.reject(error);
// });


// An interceptor for all requests to automatically add the latest saved token
// to the headers
axiosService.interceptors.request.use(config => {
	const token = localStorage.getItem('token');

	config.headers.common['Authorization'] = `Bearer ${token}`;

	return config;
}, err => Promise.reject(err));


// Our custom middleware to always update our axios headers with the latest
// token
// This saves us from including the token on every request.
// A middleware is a bridge between the action creator and the reducer
export const axiosMiddleware = ({ dispatch, getState }) => next => action => {
	if (action.type === 'RECEIVE_LOGIN') {
		axiosService.defaults.headers.common['Authorization'] = `Bearer ${action.data.token}`;
	}

	return next(action);
}
