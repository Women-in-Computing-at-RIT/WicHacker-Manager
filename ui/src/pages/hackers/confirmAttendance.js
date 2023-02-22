import {useNavigate} from "react-router-dom";
import {useEffect, useState} from "react";
import {apiDomain, getAxios} from "../../config/axios";
import {useAuth0} from "@auth0/auth0-react";
import LoadingView from "../LoadingView";

export const sendConfirmUser = async(getAccessTokenSilently, setConfirmationResponse) => {
    const token = await getAccessTokenSilently({
        audience: 'wichacks.io',
    });
    const config = {
        headers: { Authorization: `Bearer ${token}`}
    }
    getAxios().post(apiDomain() + `/user/application/confirm`, {}, config)
        .then(async (response) => {
            setConfirmationResponse(true)
        }).catch(async () => {
            setConfirmationResponse(false)
    })
}

export function ConfirmUser() {
    let navigate = useNavigate()
    const [confirmationResponse, setConfirmationResponse] = useState(null)
    const {getAccessTokenSilently} = useAuth0();

    useEffect(() => {
        sendConfirmUser(getAccessTokenSilently, setConfirmationResponse)
    }, [])

    if (typeof confirmationResponse === 'boolean'){
        if (confirmationResponse){
            navigate("/user");
        } else {
            navigate("/error");
        }
    }

    return (
        <LoadingView />
    );
}