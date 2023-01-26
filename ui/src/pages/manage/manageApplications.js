import {Box, Button, Grommet, Text} from "grommet";
import NavBar from "../../components/navBar";
import {useNavigate} from "react-router-dom";
import {ApplicationList} from "../../components/applicationList";

export default function ManageApplications(){
    let navigate = useNavigate();

    return (
        <div>
            <Grommet>
                <NavBar title="Hacker Applications">
                    <Button plain onClick={ () => navigate("/manage") }>
                        <Box background="white" round="15px" height="30px" pad="small" align="center" justify="center">
                            <Text weight="bold" color="#714ba0">Manage Home</Text>
                        </Box>
                    </Button>
                </NavBar>
            </Grommet>

            <div>
                <ApplicationList />
            </div>
        </div>
    );
}