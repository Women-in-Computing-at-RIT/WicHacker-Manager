import {Route, Outlet, useLocation, Navigate} from "react-router-dom";
import {useAuth0, withAuthenticationRequired} from "@auth0/auth0-react";

export const ProtectedComponenet = ({component, ...args}) => {
    const { loginWithRedirect } = useAuth0();
    const location = useLocation().pathname;
    console.log(location);
    const Comp = withAuthenticationRequired(component,{
        onRedirecting: () => <div>Loading...</div>,
        loginOptions: () => loginWithRedirect(),
        returnTo: useLocation.pathname
    });
    return <Comp {...args} />
}

