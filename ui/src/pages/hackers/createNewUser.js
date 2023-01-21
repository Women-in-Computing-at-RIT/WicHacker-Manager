import {useNavigate} from "react-router-dom";
import {useEffect, useState} from "react";
import {apiDomain, localAxios} from "../../config/axios";
import {useAuth0} from "@auth0/auth0-react";
import css from "./style/form.module.css"
import ReCAPTCHA from "react-google-recaptcha";
import { Grommet, Box, Heading, Text, TextInput, Form, Button } from 'grommet';
import wichacksGrommetTheme from "../../wichacksGrommetTheme";
import NavBar from "../../components/navBar";
import { Close } from "grommet-icons";

export function NewHackerForm(){
    return(
        <NewUserForm applicationRedirectRequired={true}/>
    )
}

export function NewAdminForm(){
    return(
        <NewUserForm applicationRedirectRequired={false}/>
    )
}

const createUser = async(userJson, getAccessTokenSilently, setSubmissionError, navigateToPage, applicationRedirectRequired) => {
    const token = await getAccessTokenSilently({
        audience: 'wichacks.io',
    });
    const config = {
        headers: { Authorization: `Bearer ${token}`}
    }
    localAxios.post(apiDomain + `/user`, userJson, config)
        .then(async (response) => {
            if (!applicationRedirectRequired){
                navigateToPage("/user")
            }
            navigateToPage("/user/apply")
        }).catch(async () => {
            setSubmissionError(true)
    })
}

const redirectUsersIfUserExists = async(getAccessTokenSilently, navigate) => {
    const token = await getAccessTokenSilently({
        audience: 'wichacks.io',
    });
    const config = {
        headers: { Authorization: `Bearer ${token}`}
    }
    localAxios.get(apiDomain + `/user`, config)
        .then(async (response) => {
            if (response.status === 204){
                return
            }
            const userData = (await response.data);
            if (userData?.status){
                navigate("/user")
            } else {
                navigate("/user/apply")
            }
        }).catch(async () => {

    })
}

export function NewUserForm({applicationRedirectRequired}) {
    let navigate = useNavigate()
    const [submissionError, setSubmissionError] = useState(null)
    const {getAccessTokenSilently} = useAuth0();

    useEffect(() => {
        redirectUsersIfUserExists(getAccessTokenSilently, navigateToPage)
    }, [])

    const navigateToPage = (path) => {
        navigate(path)
    }

    const checkRecaptcha = async(value) => {
        const requestData = {"captchaToken": value}
        localAxios.post(apiDomain + '/recaptcha', requestData)
            .then(async (response) => {
                setRecaptchaStatus(true)
            }).catch(async () => {
            setRecaptchaStatus(false)
        })
    }

    const submitUserCreation = async(e) => {
        e.preventDefault()

        // check recaptcha
        if (!recaptchaStatus){
            setSubmissionError(true);
            return
        }

        // clear out the recaptcha for every submission
        setRecaptchaStatus(false)

        let userData = {
            "firstName": firstName,
            "lastName": lastName,
            "email": email,
            "phoneNumber": phoneNumber
        }
        await createUser(userData, getAccessTokenSilently, setSubmissionError, navigateToPage, applicationRedirectRequired)
    }

    const [firstName, setFirstName] = useState();
    const [lastName, setLastName] = useState();
    const [email, setEmail] = useState();
    const [phoneNumber, setPhoneNumber] = useState();

    const [recaptchaStatus, setRecaptchaStatus] = useState();
    // this is not a private key, do not place private keys anywhere within this react app
    const RECAPTCHA_KEY = "6Le2GdkjAAAAAJ8xF_aJBjjHUAksuHIqGb-HKHkR"


    return (
        <Grommet theme={wichacksGrommetTheme}>
            <NavBar title="WiCHacks" />
            <Box margin="small">
                <Heading>Create a WiCHacks User</Heading>
                <Text>This is just some basic information so that we can keep in touch with you! Next you'll be able to apply for WiCHacks and check your application status.</Text>
                <Box background="#714ba0" height="4px" round="2px" margin={{ bottom: "medium", top: "medium" }}/>
                {submissionError &&
                    <Box background="#c94254" round="small" align="center" justify="between" pad="medium" margin={{ bottom: "medium" }} direction="row">
                        <Text><Text weight="bold">Error Submitting Application:</Text> Make sure to fill out all fields and verify with the reCaptcha</Text>
                        <Button plain onClick={ () => { setSubmissionError(false) } }>
                            <Close size="medium" />
                        </Button>
                    </Box>
                }
                <Box>
                    <Form>
                        <Box gap="medium">
                            <Box>
                                <Heading margin="none" level={4}>Preferred First Name</Heading>
                                <Text size="small" color="gray">What you'd like to be called</Text>
                                <TextInput
                                    placeholder="ex. Name"
                                    // value={firstName}
                                    onChange={ (e) => { setFirstName(e.target.value) } }
                                />
                            </Box>

                            <Box>
                                <Heading margin="none" level={4}>Last Name</Heading>
                                <TextInput
                                    placeholder="ex. LastName"
                                    // value={lastName}
                                    onChange={ (e) => { setLastName(e.target.value) } }
                                />
                            </Box>

                            <Box>
                                <Heading margin="none" level={4}>Email</Heading>
                                <TextInput
                                    placeholder="ex. myname@mymail.com"
                                    // value={email}
                                    onChange={ (e) => { setEmail(e.target.value) } }
                                />
                            </Box>

                            <Box>
                                <Heading margin="none" level={4}>Phone Number</Heading>
                                <TextInput
                                    placeholder="ex. 207-555-5500"
                                    // value={phoneNumber}
                                    onChange={ (e) => { setPhoneNumber(e.target.value) } }
                                />
                            </Box>

                            <Box>
                                <ReCAPTCHA sitekey={RECAPTCHA_KEY}
                                        onChange={checkRecaptcha}
                                        render="explicit"
                                        size="normal"
                                />
                            </Box>

                            <Button type="submit" onClick={submitUserCreation}>
                                <Box background="#714ba0" pad="medium" align="center" justify="center" style={{ borderRadius: "20px" }} width="medium">
                                    <Text weight="bold" size="large">{( applicationRedirectRequired ? "Continue" : "Submit")}</Text>
                                </Box>
                            </Button>
                        </Box>
                    </Form>
                </Box>
            </Box>
        </Grommet>
    );
}