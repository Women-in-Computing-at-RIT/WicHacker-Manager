import {apiDomain, getAxios} from "../../config/axios";
import {useEffect, useState} from "react";
import {useAuth0} from "@auth0/auth0-react";
import {useNavigate} from "react-router-dom";
import {Box, Button, Grommet, Text} from "grommet";
import NavBar from "../../components/navBar";
import css from "./style/manageEmails.module.css"
import buttonCss from "./style/manageLanding.module.css"

const sendPresetEmail = async(getAccessTokenSilently, setEmailResponse, presetName) => {
    const token = await getAccessTokenSilently({
        audience: 'wichacks.io',
    });
    const config = {
        headers: { Authorization: `Bearer ${token}`}
    }
    getAxios().post(apiDomain() + `/email/preset/` + presetName, {}, config)
        .then(async (response) => {
            setEmailResponse({status: true})
        }).catch(async () => {
            setEmailResponse({status: false})
    })
}

const sendCustomEmail = async(getAccessTokenSilently, setEmailResponse, content, subject, statusFilters) => {
    const token = await getAccessTokenSilently({
        audience: 'wichacks.io',
    });
    const config = {
        headers: { Authorization: `Bearer ${token}`}
    }
    let statusFilterList = []
    for (const [status, shouldSend] of Object.entries(statusFilters)) {
        if (shouldSend){
            statusFilterList.push(status)
        }
    }

    const payload = {
        "body": content,
        "subjectLine": subject,
        "recipientStatusFilter": statusFilterList
    }
    getAxios().post(apiDomain() + `/email`, payload, config)
        .then(async (response) => {
            setEmailResponse({status: true})
        }).catch(async () => {
            setEmailResponse({status: false})
        })
}

export default function ManageEmails() {
    let [emailResponse, setEmailResponse] = useState();
    let [content, setContent] = useState();
    let [subjectLine, setSubjectLine] = useState();

    // Note: You can refactor these to be a single state object but be careful, there's plenty of pitfalls with that
    // approach that could hinder readability and future updates for those who aren't super familiar with intricacies of
    // React and state
    let [sendApplied, setSendApplied] = useState();
    let [sendRejected, setSendRejected] = useState();
    let [sendAccepted, setSendAccepted] = useState();
    let [sendConfirmed, setSendConfirmed] = useState();

    const {getAccessTokenSilently, logout} = useAuth0();
    let navigate = useNavigate()

    return (
        <Grommet>
            <NavBar title="WiCHacks HackManager Admin Portal">
                <Button plain onClick={ () => navigate("/manage") }>
                    <Box background="white" round="15px" height="30px" pad="small" align="center" justify="center">
                        <Text weight="bold" color="#714ba0">Back</Text>
                    </Box>
                </Button>
            </NavBar>

            <div>
                <h2>Send Preset Emails</h2>
                <div className={buttonCss.buttonWrapper}>
                    <button className={buttonCss.manageButton} onClick={() => {sendPresetEmail(getAccessTokenSilently, setEmailResponse, "requestConfirmation")}}>Request Confirmations</button>
                </div>
            </div>
            <div>
                <h2>Send Custom Emails</h2>
                <div className={css.sendEmailForm}>
                    <label>
                        Subject Line:
                        <input className={css.textInput} value={subjectLine} onChange={e => setSubjectLine(e.target.value)} type="text" />
                    </label><br />
                    <label className={css.paragraphLabel}>
                        Email Body with in-line styling:<br />
                        <textarea className={css.largeTextInput} value={content} onChange={e => setContent(e.target.value)} rows={50} />
                    </label><br />
                    <div className={css.selectRecipients}>
                        <p className={css.selectHeading}>Select Recipients</p>
                        <label className={css.checkboxLabel}>
                            Applied
                            <input className={css.checkbox} type="checkbox" onChange={(e) => {setSendApplied(e.target.checked)}}
                            />
                        </label><br />
                        <label className={css.checkboxLabel}>
                            Accepted
                            <input className={css.checkbox} type="checkbox" onChange={(e) => {setSendAccepted(e.target.checked)}}
                            />
                        </label><br />
                        <label className={css.checkboxLabel}>
                            Rejected
                            <input className={css.checkbox} type="checkbox" onChange={(e) => {setSendRejected(e.target.checked)}}
                            />
                        </label><br />
                        <label className={css.checkboxLabel}>
                            Confirmed
                            <input className={css.checkbox} type="checkbox" onChange={(e) => {setSendConfirmed(e.target.checked)}}
                            />
                        </label><br />
                    </div>
                    <button className={css.sendCustomEmailButton} onClick={() => {sendCustomEmail(getAccessTokenSilently, setEmailResponse, content, subjectLine, {"APPLIED": sendApplied,"REJECTED": sendRejected,"ACCEPTED": sendAccepted, "CONFIRMED": sendConfirmed})}}>Send</button>
                </div>
            </div>

        </Grommet>
    );
}
