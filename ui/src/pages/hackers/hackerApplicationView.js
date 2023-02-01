import {useEffect, useState} from "react";
import {useAuth0} from "@auth0/auth0-react";
import {apiDomain, getAxios} from "../../config/axios";
import {useNavigate} from "react-router-dom";
import LoadingView from "../LoadingView";
import { ApplicationView } from "../../components/applicationView";
import {Box, Button, Grommet, Text} from "grommet";
import NavBar from "../../components/navBar";
import {LinkPrevious} from "grommet-icons";

const getUserData = async(getAccessTokenSilently, setUserResponse, navigateTo) => {
    const token = await getAccessTokenSilently({
        audience: 'wichacks.io',
    });
    const config = {
        headers: { Authorization: `Bearer ${token}`}
    }
    getAxios().get(apiDomain() + `/user`, config)
        .then(async (response) => {
            if (response.status === 204){
                navigateTo("/user/apply")
            }
            setUserResponse({data: await response.data, error: null})
        }).catch(async () => {
            navigateTo("/user")
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

    if (!userData){
        return (<LoadingView />);
    }

    return(
        <Grommet>
            <div>
                <NavBar title="WiCHacks Hacker Application">
                    <Button plain onClick={ () => navigate("/user") }>
                        <Box background="white" round="15px" height="30px" pad="small" align="center" justify="center">
                            <Text weight="bold" color="#714ba0">Back</Text>
                        </Box>
                    </Button>
                </NavBar>
            </div>
            <Box pad="medium" align="start">
                <Button plain onClick={ () => navigate("/user") }>
                    <Box gap="small" pad="small" direction="row" align="center" justify="center">
                        <LinkPrevious color="#714ba0" />
                        <Text weight="bold" color="#714ba0">Back to user home</Text>
                    </Box>
                </Button>
                <Box background="#ded492" pad="small" round="small">
                    <Text>Below you can see your application. To change or edit any information, please email <a href="mailto:wichacks@rit.edu" target="_blank" rel="noreferrer">wichacks@rit.edu</a> and an organizer will help you.</Text>
                </Box>
            </Box>
            <ApplicationView userData={userData.data} />
        </Grommet>
    )
}
