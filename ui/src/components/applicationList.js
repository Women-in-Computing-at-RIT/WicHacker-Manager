import {apiDomain, getAxios} from "../config/axios";
import {useEffect, useState} from "react";
import {useAuth0} from "@auth0/auth0-react";
import {useNavigate} from "react-router-dom";
import LoadingView from "../pages/LoadingView";
import {WiCHacksTable} from "./table";
import {Button} from "grommet";

const getApplicantsFromApi = async(getAccessTokenSilently, setApplicationResponse) => {
    const token = await getAccessTokenSilently({
        audience: 'wichacks.io',
    });
    const config = {
        headers: { Authorization: `Bearer ${token}`}
    }
    getAxios().get(apiDomain() + `/users`, config)
        .then(async (response) => {
            setApplicationResponse({data: await response.data, error: null})
        }).catch((response, error) => {
            setApplicationResponse({data: null, error: error})
    })
}

export function ApplicationList(){
    const [applicationResponse, setApplicationResponse] = useState(null)
    const {getAccessTokenSilently} = useAuth0();
    let navigate = useNavigate();

    useEffect(() => {
        getApplicantsFromApi(getAccessTokenSilently, setApplicationResponse)
    }, [])

    if (!applicationResponse){
        return (<LoadingView />);
    } else if (applicationResponse?.error){
        return(<p>Error Loading Applications, please contact the website manager</p>);
    }

    const columns = [
        {
            displayName: "",
            dataKey: 'user_id',
            dataScope: 'row',
            format: user_id => <Button plain onClick={() => navigate("/manage/applications/" + user_id)}>View</Button>
        }
    ]

    const applications = applicationResponse.data;


    return(
        <div>
            <WiCHacksTable title={"Applications"} data={applications} columns={columns}/>
        </div>
    );
}