import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import ErrorBoundry from "./components/errorBoundry";
import {BrowserRouter} from "react-router-dom";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
      <ErrorBoundry>
          <BrowserRouter>
              <App />
          </BrowserRouter>
      </ErrorBoundry>
  </React.StrictMode>
);
