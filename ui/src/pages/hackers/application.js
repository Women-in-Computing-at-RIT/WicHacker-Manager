import {useNavigate} from "react-router-dom";
import {Grommet} from "grommet";
import {useState} from "react";
import {localAxios} from "../../config/axios";
import {useAuth0} from "@auth0/auth0-react";

function useInput({ type /*...*/ }) {
    const [value, setValue] = useState("");
    const input = <input value={value} onChange={e => setValue(e.target.value)} type={type} />
    return [value, input];
}

const createApplication = async(userJson, getAccessTokenSilently, setSubmissionError, navigateToPage) => {
    const token = await getAccessTokenSilently({
        audience: 'wichacks.io',
    });
    const config = {
        headers: { Authorization: `Bearer ${token}`}
    }
    localAxios.post(`http://localhost:5001/user`, userJson, config)
        .then(async (response) => {
            navigateToPage("/user")
        }).catch(async () => {
        setSubmissionError(true)
    })
}

export default function HackerApplication() {
    let navigate = useNavigate()
    const [submissionError, setSubmissionError] = useState(null)
    const {getAccessTokenSilently} = useAuth0();

    const navigateToPage = (path) => {
        navigate(path)
    }

    const submitUserCreation = async(e) => {
        e.preventDefault()
        let userData = {
            "major": major,
            "year": year,
            "birthday": birthday,
            "resume": resume,
            "shirtSize": shirtSize,
            "hasAttendedWiCHacks": hasAttendedWiCHacks,
            "university": university
        }
        await createApplication(userData, getAccessTokenSilently, setSubmissionError, navigateToPage)
    }

    const [major, majorInput] = useInput({ type: "text" });
    const [year, yearInput] = useInput({ type: "text" });
    const [birthday, birthdayInput] = useInput({ type: "text" });
    const [resume, resumeInput] = useInput({ type: "text" });
    const [shirtSize, setShirtSize] = useState();
    const [hasAttendedWiCHacks, hasAttendedWiCHacksInput] = useInput({ type: "text" });
    const [university, universityInput] = useInput({ type: "text" });


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
                        Major:
                        {majorInput}
                    </label><br />
                    <label>
                        Year:
                        {yearInput}
                    </label><br />
                    <label>
                        Birthday:
                        {birthdayInput}
                    </label><br />
                    <label>
                        Resume Upload:
                        {resumeInput}
                    </label><br />
                    <label>
                        Shirt Size:
                        <select value={shirtSize} onChange={e => setShirtSize(e.target.value)}>
                            <option value="one">one</option>
                            <option value="two">two</option>
                            <option value="three">three</option>
                        </select>
                    </label><br />
                    <label>
                        Have you attended WiCHacks:
                        {hasAttendedWiCHacksInput}
                    </label><br />
                    <label>
                        University:
                        {universityInput}
                    </label><br />
                    <input type="submit" onClick={submitUserCreation}/>
                </form>
            </div>
        </Grommet>
    );
}