import {useEffect, useState} from "react";
import {useAuth0} from "@auth0/auth0-react";
import {apiDomain, getAxios} from "../../config/axios";
import {useNavigate} from "react-router-dom";
import css from "./style/hackerLanding.module.css"

const getUserData = async(getAccessTokenSilently, setUserResponse, setNewUser) => {
    const token = await getAccessTokenSilently({
        audience: 'wichacks.io',
    });
    const config = {
        headers: { Authorization: `Bearer ${token}`}
    }
    getAxios().get(apiDomain + `/user`, config)
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
        getAxios.post(apiDomain + `/user/resume`, data, config)
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
    getAxios().get(apiDomain + `/user/resume`, config)
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
            <p>Loading....</p>
        );
    }

    let user = userData.data

    return (
        <div>
            <h1>Welcome {user.first_name} {user.last_name}!</h1>
            <button onClick={() => logout({ returnTo: "https://wichacks.io"})}>
                Logout
            </button>

            {user.application_id && <p><button onClick={() => navigate("/user/application")}>View Application</button></p>}

            { user.status &&
                <h3>Application Status: {user.status}</h3>
            }

            <div>
                {hasUploadedResume ? <h3>Overwrite Existing Resume</h3> : <h2>Resume Upload</h2>}
                <div>
                    {resumeUpload?.status && <p>Resume Upload Success</p>}
                    {resumeUpload?.error && <p>{resumeUpload.error}</p>}
                </div>
                <form>
                    <input className={css.resumeInput} type="file" onChange={(e) => uploadResume(e, getAccessTokenSilently, setResumeUpload)}/>
                </form>
            </div>
        </div>
    );
}