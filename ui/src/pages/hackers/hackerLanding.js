import {useEffect, useState} from "react";
import {useAuth0} from "@auth0/auth0-react";
import {localAxios} from "../../config/axios";
import {useNavigate} from "react-router-dom";

const getUserData = async(getAccessTokenSilently, setUserResponse, setNewUser) => {
    const token = await getAccessTokenSilently({
        audience: 'wichacks.io',
    });
    const config = {
        headers: { Authorization: `Bearer ${token}`}
    }
    localAxios.get(`http://localhost:5001/user`, config)
        .then(async (response) => {
            if (response.status === 204){
                setNewUser(true)
                return
            }
            setUserResponse({data: await response.data, error: null})
        }).catch(async () => {
        setUserResponse({data: null, error: true})
    })
}

export default function UserHomepage() {
    const [userData, setUserData] = useState(null);
    const [newUser, setNewUser] = useState(false)
    const {getAccessTokenSilently} = useAuth0();

    useEffect(() => {
        getUserData(getAccessTokenSilently, setUserData, setNewUser)
    }, [])

    let navigate = useNavigate()
    if (newUser){
        navigate("/user/create")
    }
    const navigateToPage = (path) => {
        navigate(path)
    }

    if (userData?.error){
        return (
            <p>Error</p>
        );
    } else if (!userData?.data){
        return (
            <p>Loading....</p>
        );
    }

    let user = userData.data

    return (
        <div>
            <h1>Welcome {user.first_name} {user.last_name}!</h1>
            {user.application_id ? <p>*Insert Edit Application Button</p> : <p>*Insert Apply Button</p>}

            { user.status_id &&
                <h3>Application Status: user.data.status_id</h3>
            }
            <h3>*Insert some edit functionality here*</h3>
        </div>
    );
}