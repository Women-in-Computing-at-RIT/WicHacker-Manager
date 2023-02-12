import {useEffect, useState} from "react";
import {useAuth0} from "@auth0/auth0-react";
import {useNavigate} from "react-router-dom";
import {getUserData} from "../../utils/users";
import LoadingView from "../LoadingView";
import {Box, Button, Grommet, Text} from "grommet";
import NavBar from "../../components/navBar";
import css from "./style/manageLanding.module.css";
import {AdminComponent} from "../../hocs/adminRoute";
import {READ, STATISTICS} from "../../utils/constants";
import {StatisticsView} from "../../components/statistics";
import {AccommodationsView} from "../../components/accomodations";


export default function ManageAccommodations() {
    let navigate = useNavigate()

    return (
        <Grommet>
            <NavBar title="WiCHacks HackManager Accommodation View">
                <Button plain onClick={ () => navigate("/manage") }>
                    <Box background="white" round="15px" height="30px" pad="small" align="center" justify="center">
                        <Text weight="bold" color="#714ba0">Manage Home</Text>
                    </Box>
                </Button>
            </NavBar>
            <div>
                <h3>Hacker Accommodations</h3>
                <div>
                    <AdminComponent permission={STATISTICS} type={READ} children={<AccommodationsView />}/>
                </div>

            </div>
        </Grommet>
    );
}
