import {Route, Outlet, useLocation, Navigate} from "react-router-dom";
import {useAuth0, withAuthenticationRequired} from "@auth0/auth0-react";
import LoadingView from "../pages/LoadingView";

export const ProtectedComponent = ({component, ...args}) => {
    const { loginWithRedirect } = useAuth0();
    const location = useLocation().pathname;
    const Comp = withAuthenticationRequired(component,{
        onRedirecting: () => <LoadingView />,
        loginOptions: () => loginWithRedirect(),
        returnTo: useLocation.pathname
    });
    return <Comp {...args} />
}

