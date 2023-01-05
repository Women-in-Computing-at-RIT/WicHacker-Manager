import {useNavigate} from "react-router-dom";
import {Grommet, Button} from "grommet";
import {useState} from "react";
import {localAxios} from "../../config/axios";
import {useAuth0} from "@auth0/auth0-react";
import css from "./style/form.module.css"


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
    localAxios.post(`http://localhost:5002/user`, userJson, config)
        .then(async (response) => {
            if (!applicationRedirectRequired){
                navigateToPage("/user")
            }
            navigateToPage("/user/apply")
        }).catch(async () => {
            setSubmissionError(true)
    })
}

export function NewUserForm({applicationRedirectRequired}) {
    let navigate = useNavigate()
    const [submissionError, setSubmissionError] = useState(null)
    const {getAccessTokenSilently} = useAuth0();

    const navigateToPage = (path) => {
        navigate(path)
    }

    const submitUserCreation = async(e) => {
        e.preventDefault()
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
                <form>
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
                        <input className={css.submitButton} type="submit" onClick={submitUserCreation}/>
                    </div>
                </form>
            </div>
        </div>
    );
}