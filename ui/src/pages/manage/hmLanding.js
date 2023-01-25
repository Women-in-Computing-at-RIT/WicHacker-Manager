import {apiDomain, getAxios} from "../../config/axios";
import {useEffect, useState} from "react";
import {useAuth0} from "@auth0/auth0-react";
import {useNavigate} from "react-router-dom";
import {Button, Grommet} from "grommet";
import {getUserData} from "../../utils/users";
import LoadingView from "../LoadingView";

const callApi = async(getAccessTokenSilently, setUserResponse, userId) => {
    const token = await getAccessTokenSilently({
        audience: 'wichacks.io',
    });
    const config = {
        headers: { Authorization: `Bearer ${token}`}
    }
    getAxios().get(apiDomain() + `/userTest/${userId}`, config)
        .then(async (response) => {
            setUserResponse({data: await response.data, error: null})
        }).catch((response, error) => {
            setUserResponse({data: null, error: error})
        })
}

export default function HackathonManagerLandingPage() {
    const [userData, setUserData] = useState(null);
    const {getAccessTokenSilently, logout} = useAuth0();
    let navigate = useNavigate()

    useEffect(() => {
        getUserData(getAccessTokenSilently, setUserData, null)
    }, [])

    if (userData?.error){
        navigate("/notFound")
    } else if (!userData?.data){
        return (
            <LoadingView />
        );
    }

    let user = userData.data

    return (
        <Grommet>
            <div>
                <h1>WiCHacks HM Landing</h1>
                <h3>Hello {user.first_name} {user.last_name}</h3>
                <p>Admin Console for WiCHacks</p>
                <Button label="Manage Applications" onClick={() => {navigate("/manage/applications")}}/>

            </div>
        </Grommet>
    );
}
