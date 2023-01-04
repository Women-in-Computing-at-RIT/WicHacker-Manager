import {useNavigate} from "react-router-dom";
import {Grommet, Button} from "grommet";
import {useState} from "react";
import {localAxios} from "../../config/axios";
import {useAuth0} from "@auth0/auth0-react";


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

function useInput({ type /*...*/ }) {
    const [value, setValue] = useState("");
    const input = <input value={value} onChange={e => setValue(e.target.value)} type={type} />;
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
            "lastName": lastName
        }
        await createUser(userData, getAccessTokenSilently, setSubmissionError, navigateToPage, applicationRedirectRequired)
    }

    const [firstName, firstNameInput] = useInput({ type: "text" });
    const [lastName, lastNameInput] = useInput({ type: "text" });



    return (
        <Grommet>
            {submissionError &&
                <div>
                    <h2>
                        Error Creating User Account
                    </h2>
                </div>
            }
            <div>
                <form>
                    <label>
                        First Name:
                        {firstNameInput}
                    </label><br />
                    <label>
                        Last Name:
                        {lastNameInput}
                    </label><br />
                    <input type="submit" onClick={submitUserCreation}/>
                </form>
            </div>
        </Grommet>
    );
}