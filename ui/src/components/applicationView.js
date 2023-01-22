import { Grommet, Box, Button, Text, Heading } from "grommet";
import NavBar from "./navBar";
import { UNSAFE_DataRouterStateContext, useNavigate } from "react-router-dom";

export function ApplicationView({userData}) {
    let navigate = useNavigate();
    console.log(userData)
    return(
        <Grommet>
            <Box>
                <NavBar title="WiCHacks Hacker Application">
                    <Button plain onClick={ () => navigate("/user") }>
                        <Box background="white" round="15px" height="30px" pad="small" align="center" justify="center">
                            <Text weight="bold" color="#714ba0">Home</Text>
                        </Box>
                    </Button>
                </NavBar>
                <Box pad="medium">
                    <Box background="#ded492" pad="small" round="small">
                        <Text>Below you can see your application. To change or edit any information, please email <a href="mailto:wichacks@rit.edu" target="_blank" rel="noreferrer">wichacks@rit.edu</a> and an organizer will help you.</Text>
                    </Box>
                    <Heading level={2}>User Information</Heading>
                    <Box gap="small">
                        <Text><Text weight="bold">Name:</Text> {userData.first_name} {userData.last_name}</Text>
                        <Text><Text weight="bold">Gender:</Text> {userData.gender}</Text>
                        <Text><Text weight="bold">Email:</Text> {userData.email}</Text>
                        <Text><Text weight="bold">Phone Number:</Text> {userData.phone_number}</Text>
                        <Text><Text weight="bold">Birthday:</Text> {userData.birthday}</Text>
                    </Box>

                    <Heading level={2}>Application Information</Heading>
                    <Box gap="small">
                        <Text><Text weight="bold">Major:</Text> {userData.major}</Text>
                        <Text><Text weight="bold">Level of Study:</Text> {userData.level_of_study}</Text>
                        <Text><Text weight="bold">University:</Text> {userData.university}</Text>
                        <Text><Text weight="bold">Shirt Size:</Text> {userData.shirt_size}</Text>
                        <Text><Text weight="bold">Attended Hackathons Before:</Text> {userData.has_attended_hackathons === 1 ? "Yes" : "No" }</Text>
                        <Text><Text weight="bold">Attended WiCHacks Before:</Text> {userData.has_attended_wichacks === 1 ? "Yes" : "No" }</Text>
                        <Text><Text weight="bold">Attendance Modality:</Text> {userData.is_virtual ? "Online" : "In-Person" }</Text>
                        <Text><Text weight="bold">Dietary Restrictions:</Text> {userData.dietary_restrictions ?? "None" }</Text>
                        <Text><Text weight="bold">Special Accommodations:</Text> {userData.special_accommodations ?? "None"}</Text>
                    </Box>

                    <Heading level={2}>Travel Information</Heading>
                    <Box gap="small">
                        <Text><Text weight="bold">Requested a Bus:</Text> {userData.bus_rider === 1 ? "Yes" : "No" }</Text>
                    </Box>
                    {userData.busRider == 1 && <Box>
                        
                    </Box>}
                </Box>
            </Box>
        </Grommet>
    //       <div className={css.dataPointWrapper}>
    //           <p className={css.dataLabel}>Attending Online Only</p>
    //           <p className={css.data}>{userData.is_virtual ? "Yes" : "No"}</p>
    //       </div>
    //       <div className={css.dataPointWrapper}>
    //           <p className={css.dataLabel}>Dietary Restrictions</p>
    //           <p className={css.data}>{userData.dietary_restrictions ? userData.dietary_restrictions : "None"}</p>
    //       </div>
    //       <div className={css.dataPointWrapper}>
    //           <p className={css.dataLabel}>Dietary Restrictions</p>
    //           <p className={css.data}>{userData.special_accommodations ? userData.special_accommodations : "None"}</p>
    //       </div>
    //   </div>
    );
}