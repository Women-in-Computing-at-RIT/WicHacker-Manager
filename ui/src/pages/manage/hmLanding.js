import {apiDomain, getAxios} from "../../config/axios";
import {useEffect, useState} from "react";
import {useAuth0} from "@auth0/auth0-react";
import {useNavigate} from "react-router-dom";
import {Box, Button, Grommet, Text} from "grommet";
import {getUserData} from "../../utils/users";
import LoadingView from "../LoadingView";
import {StatisticsView} from "../../components/statistics";
import NavBar from "../../components/navBar";
import {AdminComponent} from "../../hocs/adminRoute";
import {STATISTICS, READ} from "../../utils/constants";

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
            <NavBar title="WiCHacks HackManager Admin Portal">
                <Button plain onClick={ () => logout({ returnTo: "https://apply.wichacks.io" }) }>
                    <Box background="white" round="15px" height="30px" pad="small" align="center" justify="center">
                        <Text weight="bold" color="#714ba0">Logout</Text>
                    </Box>
                </Button>
            </NavBar>
            <div>
                <h2>Hello {user.first_name} {user.last_name}</h2>
                <Button label="Manage Applications" onClick={() => {navigate("/manage/applications")}}/>

                <div>
                    <h4>Hacker Statistics</h4>
                    <AdminComponent permission={STATISTICS} type={READ} children={<StatisticsView />}/>
                </div>

            </div>
        </Grommet>
    );
}
