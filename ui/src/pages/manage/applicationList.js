import {useEffect, useState} from "react";
import {useAuth0} from "@auth0/auth0-react";
import {localAxios} from "../../config/axios";

const getApplicantsFromApi = async(getAccessTokenSilently, setApplications) => {
    const token = await getAccessTokenSilently({
        audience: 'wichacks.io',
    });
    const config = {
        headers: { Authorization: `Bearer ${token}`}
    }
    localAxios.get(`http://localhost:5001/users`, config)
        .then(async (response) => {
            setApplications({data: await response.data, error: null})
        }).catch((response, error) => {
        setApplications({data: null, error: error})
    })
}

export default function ApplicationList(){
    const [applications, setApplications] = useState(null)
    const {user, getAccessTokenSilently} = useAuth0();

    useEffect(() => {
        getApplicantsFromApi(getAccessTokenSilently, setApplications)
    }, [])

    let display;
    if (applications?.error){
        // error response from API
        display = <p>Error from API</p>
    } else if (applications?.data){
        display = <div><pre>{JSON.stringify(applications.data, null, 2)}</pre></div>
    } else {
        display = <p>Loading....</p>
    }

    return (
        <div>
            <h1>Applications</h1>
            {display}
        </div>
    );
}