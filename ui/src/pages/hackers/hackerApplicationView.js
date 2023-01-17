import {useEffect, useState} from "react";
import {useAuth0} from "@auth0/auth0-react";
import {apiDomain, getAxios} from "../../config/axios";
import {useNavigate} from "react-router-dom";
import {ApplicationView} from "../../components/applicationView";

const getUserData = async(getAccessTokenSilently, setUserResponse, navigateTo) => {
    const token = await getAccessTokenSilently({
        audience: 'wichacks.io',
    });
    const config = {
        headers: { Authorization: `Bearer ${token}`}
    }
    getAxios().get(apiDomain + `/user`, config)
        .then(async (response) => {
            if (response.status === 204){
                navigateTo("/user/apply")
            }
            setUserResponse({data: await response.data, error: null})
        }).catch(async () => {
        setUserResponse({data: null, error: true})
    })
}

export default function HackerApplicationView(){
    const [userData, setUserData] = useState(null);
    const {getAccessTokenSilently} = useAuth0();

    let navigate = useNavigate()

    useEffect(() => {
        getUserData(getAccessTokenSilently, setUserData, navigate)
    }, [])

    return(
        <>
            {userData ? <ApplicationView userData={userData.data}/> : <p>Loading...</p>}
            <button onClick={() => {navigate("/user")}}>Back</button>
        </>
    )
}
