import { StrictMode } from 'react';
import ReactDOM from 'react-dom/client';
import axios from 'axios';
import App from './App';
import * as serviceWorkerRegistration from './serviceWorkerRegistration';
import reportWebVitals from './reportWebVitals';
import getApiUrl from './utils/getApiUrl';

axios.defaults.baseURL = getApiUrl();

// Comment these lines to use real server even in development mode
// if (process.env.NODE_ENV === 'development') {
//   const worker = require('./mocks/browser').default;
//   worker.start()
// }

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);
root.render(
  <StrictMode>
    <App />
  </StrictMode>,
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://cra.link/PWA
serviceWorkerRegistration.register();

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
