import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import ErrorBoundry from "./components/errorBoundry";
import {BrowserRouter} from "react-router-dom";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
      <ErrorBoundry>
          <BrowserRouter>
              <App />
          </BrowserRouter>
      </ErrorBoundry>
);
