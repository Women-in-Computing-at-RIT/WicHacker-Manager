import {Auth0Provider} from "@auth0/auth0-react"
import {useNavigate} from "react-router-dom";

import './App.css';
import AppRoutes from "./components/routes";

function App() {
  const navigate = useNavigate();

  const onRedirectCallback = (appState) => {
      // Use router history to replace url
      navigate(appState.returnTo || window.location.origin, {replace: true})
  };

  return (
      <Auth0Provider
        domain="dev-5fez71a01xmz0e34.us.auth0.com"
        clientId="cxaFtmQ0ZZ8agA8nelHbdAaAecgTO8iH"
        redirectUri={`${window.location.origin}/auth`}
        audience='wichacks.io'
        onRedirectCallback={onRedirectCallback}
      >
        <AppRoutes />
      </Auth0Provider>
  )
}

export default App;
