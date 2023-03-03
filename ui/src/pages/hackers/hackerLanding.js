import {useEffect, useState} from "react";
import {useAuth0} from "@auth0/auth0-react";
import {apiDomain, getAxios} from "../../config/axios";
import {useNavigate} from "react-router-dom";
import css from "./style/hackerLanding.module.css"
import LoadingView from "../LoadingView";
import { Grommet, Box, Heading, Text, Button, Paragraph, Form, FileInput } from 'grommet';
import NavBar from "../../components/navBar";
import { Help } from "grommet-icons";
import {getUserData} from "../../utils/users";
import {checkUserPermissions} from "../../utils/permissions";
import {CONSOLE, READ} from "../../utils/constants";

const uploadResume = async (e, getAccessTokenSilently, setResumeUpload) => {
    e.preventDefault()
    if (e.target.files?.length === 1){
        const file = e.target.files[0];

        if (file.size > 10000000){
            setResumeUpload({"status": false, "error": "File Too Large"})
        }

        const data = new FormData();
        data.append("resume", file)

        const token = await getAccessTokenSilently({
            audience: 'wichacks.io',
        });
        const config = {
            headers: { Authorization: `Bearer ${token}`}
        }
        getAxios().post(apiDomain() + `/user/resume`, data, config)
            .then(async (response) => {
                setResumeUpload({"status": true, "error": null})
            }).catch(async () => {
                setResumeUpload({"status": false, "error": "Resume Upload Failed"})
        })

    } else {
        //prompt that they need to upload a file
        setResumeUpload({"status": false, "error": "Please only upload one file"})
    }
}

const checkIfUserHasUploadedResume = async (getAccessTokenSilently, setHasUploadedResume, userData, newUser) => {
    if ((!userData?.data) || newUser){
        // don't check resume if we don't have user data or will get redirected
        return
    }
    const token = await getAccessTokenSilently({
        audience: 'wichacks.io',
    });
    const config = {
        headers: { Authorization: `Bearer ${token}`}
    }
    getAxios().get(apiDomain() + `/user/resume`, config)
        .then(async (response) => {
            setHasUploadedResume(true)
        }).catch(async () => {
            setHasUploadedResume(false)
    })
}

const checkCanUserViewManageButton = async (getAccessTokenSilently, setCanViewManageButton) => {
    await checkUserPermissions(CONSOLE, READ, getAccessTokenSilently, setCanViewManageButton);
}


export default function UserHomepage() {
    const [userData, setUserData] = useState(null);
    const [newUser, setNewUser] = useState(false);
    const [resumeUpload, setResumeUpload] = useState(null);
    const {getAccessTokenSilently, logout} = useAuth0();
    const [hasUploadedResume, setHasUploadedResume] = useState();

    // Very Important Note: These variables are DOM modifyable so shouldn't be considered final truths
    // If someone wants to modify the DOM to get access to this button then all the power to them, there's
    // permissions attached to the route the button goes to so even if a user can see the button they still can't get
    // to admin protected routes without permissions
    const [canViewManageButton, setCanViewManageButton] = useState();

    // @TODO: set programmatic/dynamic way to set this so we can open up confirmations at a specified time closer to event
    const acceptingConfirmations = true;

    // @TODO: set programmatic/dynamic way to set that discord is open
    const discordReadyForConnections = true;

    useEffect(() => {
        getUserData(getAccessTokenSilently, setUserData, setNewUser)
    }, [])

    useEffect(() => {
        //once user is loaded, check permissions for manage button rendering
        checkCanUserViewManageButton(getAccessTokenSilently, setCanViewManageButton)
    }, [userData])

    // On initial render and when resume upload is attempted, reload if user has already uploaded resume
    useEffect(() => {
        checkIfUserHasUploadedResume(getAccessTokenSilently, setHasUploadedResume, userData, newUser)
    }, [resumeUpload, userData])

    let navigate = useNavigate()
    if (newUser){
        navigate("/user/create");
    }

    if (userData?.error){
        navigate("/notFound")
    } else if (!userData?.data){
        return (
            <LoadingView />
        );
    }

    let user = userData.data

    let displayStatus = "You haven't applied yet";
    if (user?.status === "APPLIED") {
        displayStatus = "Your Application Has Been Received 👍"
    } else if (user?.status === "ACCEPTED"){
        displayStatus = "Congratulations!! Your Application Has Been Accepted"
    } else if (user?.status === "REJECTED"){
        displayStatus = "We are sorry to say that your application has been rejected"
    } else if (user?.status === "CONFIRMED"){
        displayStatus = "Thank you for confirming, we'll see you at WiCHacks!"
    }
    // Switch out the different statuses we have once has been implemented

    return (
        <Grommet>
            <Box>
                <NavBar title="WiCHacks User Home">
                    <div className={css.navbarButtonWrapper}>
                        {canViewManageButton && <Button plain onClick={ () => navigate("/manage") }>
                            <Box background="white" round="15px" height="30px" pad="small" align="center" justify="center">
                                <Text weight="bold" color="#714ba0">Manage</Text>
                            </Box>
                        </Button>}
                        <div className={css.navbarButton}><p></p></div> {/* REMOVE AT SOME POINT, THIS IS BECAUSE THE CONDITIONAL RENDER MESSES WITH THE CSS STYLING FOR SOME REASON*/}
                        <Button plain className={css.navbarButton} onClick={ () => logout({ returnTo: "https://apply.wichacks.io" }) }>
                            <Box background="white" round="15px" height="30px" pad="small" align="center" justify="center">
                                <Text weight="bold" color="#714ba0">Logout</Text>
                            </Box>
                        </Button>
                    </div>
                </NavBar>
                <Box margin="small"> { /* Page content */}
                    <Heading>Welcome { user.first_name }!</Heading>
                    { user.application_id ?
                        <Box> {/** ALREADY APPLIED */ }
                            <Text size="large" margin={{ bottom: "medium" }}><Text weight="bold" size="large">Application Status:</Text> {displayStatus}</Text>
                            { user.status === "APPLIED" && <Box margin={{ bottom: "medium" }} direction="row" gap="small" color="gray">
                                <Help />
                                <Text>Your application will be reviewed by WiCHacks organizers and you will receive an email when a decision is made</Text>    
                            </Box>}

                            <Button plain onClick={ () => navigate("/user/application") }>
                                <Box background="#714ba0" pad="medium" align="center" justify="center" style={{ borderRadius: "20px" }} width="medium">
                                    <Text weight="bold" size="large">View Your Application</Text>
                                </Box>
                            </Button>

                            <Heading level={3} margin={{ bottom: "none" }}>Get Ready For WiCHacks</Heading>
                            {(acceptingConfirmations && user?.status === "ACCEPTED") &&
                                <Button plain onClick={ () => navigate("/user/confirm") }>
                                    <Box background="#714ba0" pad="medium" align="center" justify="center" style={{ borderRadius: "20px" }} width="medium">
                                        <Text weight="bold" size="medium">RSVP/Confirm Attendance</Text>
                                    </Box>
                                </Button>
                            }
                            {(discordReadyForConnections && (user?.status === "ACCEPTED" || user?.status === "CONFIRMED")) &&
                            <Button plain href={apiDomain()+"/discord?id=" + user?.user_id}>
                                <Box background="#714ba0" pad="medium" align="center" justify="center" style={{ borderRadius: "20px" }} width="medium">
                                    <Text weight="bold" size="medium">Connect to Discord</Text>
                                </Box>
                            </Button>
                            }


                            <Heading level={4} margin={{ bottom: "none" }}>Share your resume</Heading>
                            <Text>Please upload your resume, we will share your resume with qualifying sponsors for job opportunities! Lots of hackers connect with companies in unique ways during hackathons, and it can be a great way to show potential employers your skills.</Text>
                            { hasUploadedResume ?
                                <div className={css.resumeUploadPadding}>
                                    <Box>
                                        <Text weight="bold">You already have a resume uploaded. You may overwrite it with a new one below</Text>
                                    </Box>
                                </div>
                                 :
                                <Box margin={{ vertical: "small" }}>
                                    <Text weight="bold">You haven't uploaded a resume yet</Text>
                                </Box>
                            }

                            <Box>
                                {resumeUpload?.status && 
                                    <Box background="#a5dea4" pad="small" round="small" margin={{ vertical: "small" }}>
                                        <Text>Resume Upload Success</Text>
                                    </Box>
                                }

                                {resumeUpload?.error && 
                                    <Box background="#c94254" pad="small" round="small" margin={{ vertical: "small" }}>
                                        <Text>Resume Upload Error: {resumeUpload.error}</Text>
                                    </Box>
                                }
                            </Box>
                            <Form>
                                <Text size="small" color='gray'>Accepted file types: .txt, .pdf, .doc, .docx, .jpg, .png</Text>
                                <FileInput
                                    maxSize={10000000}
                                    multiple={false}
                                    onChange={(e) => {
                                        const fileList = e.target.files;
                                        if (fileList.length > 0) {
                                            uploadResume(e, getAccessTokenSilently, setResumeUpload)
                                        } else {
                                            setResumeUpload({ "status": false, "error": "Failed to select files"})
                                        }
                                    }} 
                                />
                            </Form>
                        </Box> :
                        <Box background="#00000010" round="medium" pad="medium"> { /** NEEDS TO APPLY */ }
                            <Heading level={3} margin="none">You Haven't Applied Yet! 😞</Heading>
                            <Paragraph fill>WiCHacks is still accepting applications! Apply now, it's super easy!</Paragraph>
                            <Button onClick={() => {navigate("/user/apply")}}>
                                <Box background="#714ba0" pad="medium" align="center" justify="center" style={{ borderRadius: "20px" }} width="medium">
                                    <Text weight="bold" size="large">Apply Now!</Text>
                                </Box>
                            </Button>
                        </Box>
                    }
                    
                </Box>
            </Box>
        </Grommet>
    );
}
