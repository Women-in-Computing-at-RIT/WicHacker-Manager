import logo from './logo.svg';
import {Auth0Provider} from "@auth0/auth0-react"
import {useNavigate} from "react-router-dom";

import './App.css';
import AppRoutes from "./components/routes";

function App() {
  const navigate = useNavigate();

  const onRedirectCallback = (appState) => {
      console.log("On Rediret callback appstate: ", appState)
      // Use router history to replace url
      navigate(appState.returnTo || window.location.origin, {replace: true})
  };

  return (
      <Auth0Provider
        domain="wichacks.us.auth0.com"
        clientId="oTpWdnroYxfqQrprklhfXTGxIK5Vn8Df"
        redirectUri={`${window.location.origin}/auth`}
        onRedirectCallback={onRedirectCallback}
      >
        <AppRoutes />
      </Auth0Provider>
  )
}

export default App;
