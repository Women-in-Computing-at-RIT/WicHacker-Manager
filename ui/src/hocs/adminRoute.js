import {useAuth0} from "@auth0/auth0-react";
import LoadingView from "../pages/LoadingView";
import {apiDomain, getAxios} from "../config/axios";
import {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import {checkUserPermissions} from "../utils/permissions";

// Dev Note: Must be wrapped in a protected route so that user is logged in
// Security Note: We show a 404 page for all pages that a user does not have access to
export const AdminRoute = ({permission, type, children}) => {
    const [hasPermissions, setHasPermissions] = useState();
    const {getAccessTokenSilently} = useAuth0();
    const navigate = useNavigate();

    useEffect(() => {
        checkUserPermissions(permission, type, getAccessTokenSilently, setHasPermissions)
    }, [])

    if (hasPermissions){
        return (<div>{children}</div>);
    }
    if (typeof hasPermissions === 'boolean' && !hasPermissions){
        navigate("/notFound")
    }

    return(
      <LoadingView />
    );
}

// Component that requires permissions, only used on manager side so we can be more verbose in error responses
export const AdminComponent = ({permission, type, children}) => {
    const [hasPermissions, setHasPermissions] = useState();
    const {getAccessTokenSilently} = useAuth0();

    useEffect(() => {
        checkUserPermissions(permission, type, getAccessTokenSilently, setHasPermissions)
    }, [])

    if (hasPermissions){
        return (<div>{children}</div>);
    }
    if (typeof hasPermissions === 'boolean' && !hasPermissions){
        return (<p>Permissions Denied, Please Contact WiCHacks website manager for more details</p>);
    }

    return(
        <LoadingView />
    );
}