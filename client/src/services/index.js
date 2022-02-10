import axios from 'axios';
import { BASE_URL } from '../globals';

const Client = axios.create({
  baseURL: BASE_URL
});

const auth_token = localStorage.getItem('auth_token');

Client.defaults.headers.common['Authorization'] = auth_token
  ? 'Token ' + auth_token
  : '';

export default Client;
