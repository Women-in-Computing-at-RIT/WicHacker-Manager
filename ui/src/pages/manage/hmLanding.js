import {apiDomain, getAxios} from "../../config/axios";
import {useEffect, useState} from "react";
import {useAuth0} from "@auth0/auth0-react";
import {useNavigate} from "react-router-dom";
import {Button, Grommet} from "grommet";

const callApi = async(getAccessTokenSilently, setUserResponse, userId) => {
    const token = await getAccessTokenSilently({
        audience: 'wichacks.io',
    });
    const config = {
        headers: { Authorization: `Bearer ${token}`}
    }
    getAxios().get(apiDomain + `/userTest/${userId}`, config)
        .then(async (response) => {
            setUserResponse({data: await response.data, error: null})
        }).catch((response, error) => {
            setUserResponse({data: null, error: error})
        })
}

export default function HackathonManagerLandingPage() {
    const [userResponse, setUserResponse] = useState(null);
    const {user, getAccessTokenSilently} = useAuth0();

    useEffect(() => {
        callApi(getAccessTokenSilently, setUserResponse, user.sub)
    }, [])

    let navigate = useNavigate()
    const onClickNavigate = (path) => {
        navigate(path)
    }

    let display;
    if (userResponse?.error){
        display = <p>Error</p>
    } else if (userResponse?.data){
        display=<div><pre>{JSON.stringify(userResponse.data, null, 2)}</pre></div>
    } else {
        display = <p>Loading....</p>
    }

    return (
        <Grommet>
            <div>
                <h1>WiCHacks HM Landing</h1>
                <h3>Hello {user.name}</h3>
                {display}
                <Button label="Applications" onClick={() => {onClickNavigate("/manage/applications")}}/>
            </div>
        </Grommet>
    );
}
