import {useEffect, useState} from "react";
import {useAuth0} from "@auth0/auth0-react";
import {apiDomain, localAxios} from "../../config/axios";
import {useNavigate} from "react-router-dom";
import css from "./style/hackerLanding.module.css"
import LoadingView from "../LoadingView";
import { Grommet, Box, Heading, Text, Button, Paragraph } from 'grommet';
import NavBar from "../../components/navBar";
import { Help } from "grommet-icons";

const getUserData = async(getAccessTokenSilently, setUserResponse, setNewUser) => {
    const token = await getAccessTokenSilently({
        audience: 'wichacks.io',
    });
    const config = {
        headers: { Authorization: `Bearer ${token}`}
    }
    localAxios.get(apiDomain + `/user`, config)
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
        localAxios.post(apiDomain + `/user/resume`, data, config)
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

const checkIfUserHasUploadedResume = async (getAccessTokenSilently, setHasUploadedResume) => {
    const token = await getAccessTokenSilently({
        audience: 'wichacks.io',
    });
    const config = {
        headers: { Authorization: `Bearer ${token}`}
    }
    localAxios.get(apiDomain + `/user/resume`, config)
        .then(async (response) => {
            setHasUploadedResume(true)
        }).catch(async () => {
            setHasUploadedResume(false)
    })
}


export default function UserHomepage() {
    const [userData, setUserData] = useState(null);
    const [newUser, setNewUser] = useState(false);
    const [resumeUpload, setResumeUpload] = useState(null);
    const {getAccessTokenSilently, logout} = useAuth0();
    const [hasUploadedResume, setHasUploadedResume] = useState();

    useEffect(() => {
        getUserData(getAccessTokenSilently, setUserData, setNewUser)
    }, [])

    // On initial render and when resume upload is attempted, reload if user has already uploaded resume
    useEffect(() => {
        checkIfUserHasUploadedResume(getAccessTokenSilently, setHasUploadedResume)
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
    console.log(user);

    let displayStatus = "You haven't applied yet";
    if (user.status == "APPLIED") {
        displayStatus = "Your Application Has Been Received 👍"
    } // Switch out the different statuses we have once has been implemented

    return (
        <Grommet>
            <Box>
                <NavBar title="WiCHacks User Home">
                    <Button plain onClick={ () => logout({ returnTo: "/" }) }>
                        <Box background="white" round="15px" height="30px" pad="small" align="center" justify="center">
                            <Text weight="bold" color="#714ba0">Logout</Text>
                        </Box>
                    </Button>
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



                            { hasUploadedResume ?
                                <div className={css.resumeUploadPadding}>
                                    <Box>
                                        <Text>Resume Uploaded <br />Overwrite existing resume</Text>
                                    </Box>
                                </div>
                                 :
                                <div className={css.resumeUploadPadding}>
                                    <Box>
                                        <Text>Plz upload your resume, we will get you a job /s</Text>
                                    </Box>
                                </div>
                            }

                            <Box>
                                {resumeUpload?.status && 
                                    <Box background="green">
                                        <Text>Resume Upload Success</Text>
                                    </Box>
                                }

                                {resumeUpload?.error && 
                                    <Box background="red">
                                        <Text>Resume Upload Error: {resumeUpload.error}</Text>
                                    </Box>
                                }
                            </Box>
                            <form>
                                <input className={css.resumeInput} type="file" onChange={(e) => uploadResume(e, getAccessTokenSilently, setResumeUpload)}/>
                            </form>
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