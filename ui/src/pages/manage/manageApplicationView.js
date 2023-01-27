import {useNavigate, useParams} from "react-router-dom";
import {useEffect, useState} from "react";
import {getUserData} from "../../utils/users";
import {useAuth0} from "@auth0/auth0-react";
import LoadingView from "../LoadingView";
import NavBar from "../../components/navBar";
import {Box, Button, Grommet, Text} from "grommet";
import {ApplicationView} from "../../components/applicationView";
import {apiDomain, getAxios} from "../../config/axios";
import css from "./style/manageApplicationView.module.css"

const changeApplicationStatus = async (isAccepted, userId, getAccessTokenSilently, setApplicationUpdateResponse) => {
    const token = await getAccessTokenSilently({
        audience: 'wichacks.io',
    });
    const config = {
        headers: { Authorization: `Bearer ${token}`}
    }
    const payload = {
        "userId": userId,
        "status": isAccepted ? "ACCEPTED" : "REJECTED"
    }
    getAxios().put(apiDomain() + `/user/application`, payload, config)
        .then(async (response) => {
            setApplicationUpdateResponse({error: false})
        }).catch(async () => {
            setApplicationUpdateResponse({error: true})
    })
    window.scrollTo(0, 0)
}


export function ManageApplicationView(){
    const {userId} = useParams();
    const [userResponse, setUserResponse] = useState();
    const [applicationUpdateResponse, setApplicationUpdateResponse] = useState();
    const {getAccessTokenSilently, logout} = useAuth0();

    useEffect( () => {
        getUserData(getAccessTokenSilently, setUserResponse, null)
    }, [])

    let navigate = useNavigate();
    if (!userResponse){
        return(<LoadingView />);
    }

    let updateDisplay = null
    if (applicationUpdateResponse?.error){
        updateDisplay = <div className={css.failure}>Application Status Update Failure</div>
    } else if (applicationUpdateResponse){
        updateDisplay = <div className={css.success}>Application Status Updated</div>
    }

    const navbarDisplay = <Grommet>
        <NavBar title="WiCHacks HackManager Admin Portal">
            <Button plain onClick={ () => navigate("/manage/applications") }>
                <Box background="white" round="15px" height="30px" pad="small" align="center" justify="center">
                    <Text weight="bold" color="#714ba0">Back</Text>
                </Box>
            </Button>
        </NavBar>
    </Grommet>


    if(userResponse?.error){
        return (
            <div>
                {navbarDisplay}
                <p>Retrieving Hacker Application Data Failure</p>
            </div>
        );
    } else {
        return (
            <div>
                {navbarDisplay}
                <div>
                    <div className={css.applicationUpdate}>
                        {updateDisplay && updateDisplay}
                    </div>
                    <div className={css.applicationUpdate}>
                        <h2>Hacker Application</h2>
                    </div>
                    <div className={css.statusWrapper}>
                        <p className={css.statusHeader}>Application Status</p>
                        <p className={css.statusValue}><b>Status: </b>{userResponse.data.status}</p>
                    </div>
                    <ApplicationView userData={userResponse.data} />
                    <div className={css.statusButtonWrapper}>
                        <button className={css.accept + ' ' + css.statusButton} onClick={() => changeApplicationStatus(true, userId, getAccessTokenSilently, setApplicationUpdateResponse)}>Accept</button>
                        <button className={css.deny + ' ' + css.statusButton} onClick={() => changeApplicationStatus(false, userId, getAccessTokenSilently, setApplicationUpdateResponse)}>Reject</button>
                    </div>
                </div>
            </div>
        );
    }
}