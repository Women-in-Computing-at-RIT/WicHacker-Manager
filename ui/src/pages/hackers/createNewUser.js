import {useNavigate} from "react-router-dom";
import {useEffect, useState} from "react";
import {apiDomain, localAxios} from "../../config/axios";
import {useAuth0} from "@auth0/auth0-react";
import css from "./style/form.module.css"
import ReCAPTCHA from "react-google-recaptcha";


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

function useTextInput() {
    const [value, setValue] = useState("");
    const input = <input className={css.textInput} value={value} onChange={e => setValue(e.target.value)} type="text" />;
    return [value, input];
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

const redirectUsersIfApplied = async(getAccessTokenSilently, navigate) => {
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
            }
        }).catch(async () => {

    })
}

export function NewUserForm({applicationRedirectRequired}) {
    let navigate = useNavigate()
    const [submissionError, setSubmissionError] = useState(null)
    const {getAccessTokenSilently} = useAuth0();

    useEffect(() => {
        redirectUsersIfApplied(getAccessTokenSilently, navigateToPage)
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

    const [firstName, firstNameInput] = useTextInput();
    const [lastName, lastNameInput] = useTextInput();
    const [email, emailInput] = useTextInput();
    const [phoneNumber, phoneNumberInput] = useTextInput();

    const [recaptchaStatus, setRecaptchaStatus] = useState();
    // this is not a private key, do not place private keys anywhere within this react app
    const RECAPTCHA_KEY = "6Le2GdkjAAAAAJ8xF_aJBjjHUAksuHIqGb-HKHkR"


    return (
        <div>
            <h2 className={css.pageTitle}>Hacker Profile Creation</h2>
            {submissionError &&
                <div>
                    <h2>
                        Error Creating User Account
                    </h2>
                </div>
            }
            <div>
                <form className={css.applicationForm}>
                    <div className={css.hackerProfileFormFields}>
                        <label>
                            First Name: <br />
                            {firstNameInput}
                        </label><br />
                        <label>
                            Last Name: <br />
                            {lastNameInput}
                        </label><br />
                        <label>
                            Email: <br />
                            {emailInput}
                        </label><br />
                        <label>
                            Phone Number: <br />
                            {phoneNumberInput}
                        </label><br />
                        <div>
                            <ReCAPTCHA sitekey={RECAPTCHA_KEY}
                                       onChange={checkRecaptcha}
                                       render="explicit"
                                       size="normal"
                            />
                        </div>
                        <input className={css.submitButton} type="submit" onClick={submitUserCreation} value={(applicationRedirectRequired ? "continue" : "submit")}/>
                    </div>
                </form>
            </div>
        </div>
    );
}