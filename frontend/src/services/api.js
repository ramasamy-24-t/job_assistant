import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:5000/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add a request interceptor to add the JWT token to requests
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Add response interceptor to handle token expiry (basic 401 handling)
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Clear local storage and force re-login if token is totally invalid
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            // A full app might want to redirect to login using window.location.href='/login'
        }
        return Promise.reject(error);
    }
);

export default api;
