import {useNavigate, useSearchParams} from "react-router-dom";
import {useEffect, useState} from "react";
import {apiDomain, getAxios} from "../../config/axios";
import {useAuth0} from "@auth0/auth0-react";
import LoadingView from "../LoadingView";

export const sendSaveDiscordId = async(getAccessTokenSilently, discordCode, discordSalt, setIntegrationResponse) => {
    const token = await getAccessTokenSilently({
        audience: 'wichacks.io',
    });
    const config = {
        headers: { Authorization: `Bearer ${token}`},
        params: { code: discordCode, state: discordSalt}
    }
    getAxios().post(apiDomain() + `/discord`, {}, config)
        .then(async (response) => {
            setIntegrationResponse(true)
        }).catch(async () => {
            setIntegrationResponse(false)
    })
}

export function DiscordCallback() {
    let navigate = useNavigate()
    const [integrationResponse, setIntegrationResponse] = useState(null)
    const [searchParams, setSearchParams] = useSearchParams();
    const {getAccessTokenSilently} = useAuth0();

    useEffect(() => {
        sendSaveDiscordId(getAccessTokenSilently, searchParams.get('code'), searchParams.get('state'), setIntegrationResponse)
    }, [])

    if (typeof integrationResponse === 'boolean'){
        if (integrationResponse){
            navigate("/user");
        } else {
            navigate("/error");
        }
    }

    return (
        <LoadingView />
    );
}