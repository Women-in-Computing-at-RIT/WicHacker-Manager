import {useEffect, useState} from "react";
import {useAuth0} from "@auth0/auth0-react";
import {localAxios} from "../../config/axios";
import {useNavigate} from "react-router-dom";
import {Grommet} from "grommet";

const getUserData = async(getAccessTokenSilently, setUserResponse, setNewUser) => {
    const token = await getAccessTokenSilently({
        audience: 'wichacks.io',
    });
    const config = {
        headers: { Authorization: `Bearer ${token}`}
    }
    localAxios.get(`http://localhost:5002/user`, config)
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
    console.log("happenings beginning")
    if (e.target.files?.length === 1){
        const file = e.target.files[0];
        const data = new FormData();
        data.append("resume", file)
        console.log("happenings")

        const token = await getAccessTokenSilently({
            audience: 'wichacks.io',
        });
        const config = {
            headers: { Authorization: `Bearer ${token}`}
        }
        localAxios.post(`http://localhost:5002/user/resume`, data, config)
            .then(async (response) => {
                setResumeUpload({"status": true, "error": null})
            }).catch(async () => {
            setResumeUpload({"status": false, "error": true})
        })

    } else {
        //prompt that they need to upload a file
        setResumeUpload({"status": false, "error": 0})
    }
}

export default function UserHomepage() {
    const [userData, setUserData] = useState(null);
    const [newUser, setNewUser] = useState(false);
    const [resumeUpload, setResumeUpload] = useState(null);
    const {getAccessTokenSilently} = useAuth0();

    useEffect(() => {
        getUserData(getAccessTokenSilently, setUserData, setNewUser)
    }, [])

    let navigate = useNavigate()
    if (newUser){
        navigate("/user/create");
    }

    if (userData?.error){
        return (
            <p>Error</p>
        );
    } else if (!userData?.data){
        return (
            <p>Loading....</p>
        );
    }

    let user = userData.data

    return (
        <div>
            <h1>Welcome {user.first_name} {user.last_name}!</h1>
            {user.application_id ? <p>*Insert Edit Application Button</p> : <p>*Insert Apply Button</p>}

            { user.status_id &&
                <h3>Application Status: user.data.status_id</h3>
            }
            <h3>*Insert some edit functionality here*</h3>

            <h2>Resume Upload</h2>
            <div className={"Resume-Upload-Textbox"}>
                {resumeUpload && <p className={"Success"}>Resume Upload Success</p>}
                {resumeUpload?.error === 0 && <p className={"Failure"}>Resume Upload Failure</p>}
            </div>
            <form>
                <input type="file" onChange={(e) => uploadResume(e, getAccessTokenSilently, setResumeUpload)}/>
            </form>
        </div>
    );
}