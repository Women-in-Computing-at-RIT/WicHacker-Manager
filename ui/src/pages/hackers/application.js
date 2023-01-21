import {useNavigate} from "react-router-dom";
import {useEffect, useState} from "react";
import {apiDomain, localAxios} from "../../config/axios";
import {useAuth0} from "@auth0/auth0-react";
import css from "./style/form.module.css"
import ReCAPTCHA from "react-google-recaptcha";
import { Grommet, Box, Form, Heading, Button, Paragraph, FormField, TextInput, Text, Select, CheckBox, RadioButtonGroup, TextArea, DateInput } from 'grommet';
import { Close } from "grommet-icons";
import wichacksGrommetTheme from "../../wichacksGrommetTheme";

const createApplication = async(userJson, getAccessTokenSilently, setSubmissionError, navigateToPage) => {
    const token = await getAccessTokenSilently({
        audience: 'wichacks.io',
    });
    const config = {
        headers: { Authorization: `Bearer ${token}`}
    }
    console.log(userJson);
    localAxios.post(apiDomain + `/user/apply`, userJson, config)
        .then(async (response) => {
            navigateToPage("/user")
        }).catch(async (error) => {
        if (error?.response?.status === "400"){
            setSubmissionError({"error": true, "description": "Please make sure all fields are filled in and try again"});
        } else {
            setSubmissionError({"error": true, "description": "Server error"});
        }
        window.scrollTo(0, 0)
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

export default function HackerApplication() {
    let navigate = useNavigate()
    const [submissionError, setSubmissionError] = useState(null)
    const {getAccessTokenSilently} = useAuth0();

    const navigateToPage = (path) => {
        navigate(path)
    }

    useEffect(() => {
        redirectUsersIfApplied(getAccessTokenSilently, navigateToPage)
    }, [])

    const isSchoolOther = (schoolName) => {
        const selectOptionSchoolNames = {"RIT": true, "Waterloo": true, "SUNY Oswego": true, "Syracuse": true, "Cornell": true, "Ithaca": true}
        if (selectOptionSchoolNames.hasOwnProperty(schoolName)){
            // School in select list
            return false
        }
        return true
    }

    const isLevelOfStudyOther = (levelOfStudy) => {
        const selectOptionLevelOfStudy = {"High School": true, "First Year Undergraduate": true, "Second Year Undergraduate": true, "Third Year Undergraduate": true, "Fourth Year Undergraduate": true, "Fifth Year Undergraduate": true, "Graduate Studies": true}
        if (selectOptionLevelOfStudy.hasOwnProperty(levelOfStudy)){
            // level of study in select list
            return false
        }
        return true
    }

    const submitUserCreation = async(e) => {
        e.preventDefault()

        const affirmedAgreements = ritEventPolicies && mlhCodeOfConduct && mlhDataSharing && allInformationCorrect
        if (!affirmedAgreements){
            setSubmissionError({"error": true, "description": "Must agree to all policies and agreements"});
            window.scrollTo(0, 0)
            return
        }

        let userData = {
            "major": major,
            "levelOfStudy": levelOfStudy,
            "birthday": birthday,
            "shirtSize": shirtSize,
            "hasAttendedWiCHacks": (hasAttendedWiCHacks && hasAttendedWiCHacks === "true"),
            "hasAttendedHackathons": (hasAttendedHackathons && hasAttendedHackathons === "true"),
            "university": (university && !isSchoolOther(university)) ? university : otherUniversity,
            "gender": gender,
            "busRider": (eligibleForBusing && busRider === "true"),
            "busStop": busStop,
            "dietaryRestrictions": dietaryRestriction,
            "specialAccommodations": specialAccommodations,
            "affirmedAgreements": affirmedAgreements,
            "isVirtual": (isVirtual && isVirtual === "true")
        }
        await createApplication(userData, getAccessTokenSilently, setSubmissionError, navigateToPage)
    }

    const [major, setMajor] = useState();
    const [levelOfStudy, setLevelOfStudy] = useState();
    const [otherLevelOfStudy, setOtherLevelOfStudy] = useState();
    const [birthday, setBirthday] = useState();
    const [shirtSize, setShirtSize] = useState();
    const [hasAttendedWiCHacks, setAttendedWiCHacksInput] = useState();
    const [hasAttendedHackathons, setAttendedHackathonsInput] = useState();
    const [university, setUniversity] = useState();
    const [otherUniversity, setOtherUniversity] = useState();
    const [gender, setGender] = useState();
    const [busRider, setBusRider] = useState();
    const [busStop, setBusStop] = useState();
    const [hasDietaryRestriction, setHasDietaryRestriction] = useState();
    const [dietaryRestriction, setDietaryRestriction] = useState();
    const [hasSpecialAccommodations, setHasSpecialAccommodations] = useState();
    const [specialAccommodations, setSpecialAccommodations] = useState();
    const [ritEventPolicies, setRitEventPolicies] = useState();
    const [mlhCodeOfConduct, setMlhCodeOfConduct] = useState();
    const [mlhDataSharing, setMlhDataSharing] = useState();
    const [allInformationCorrect, setAllInformationCorrect] = useState();
    const [isVirtual, setIsVirtual] = useState();

    let eligibleForBusing = (university !== "RIT") && (isVirtual && isVirtual === "true")

    // form based on Registration Form Guideline https://docs.google.com/document/d/1FxLkwcFK-W513G10m53Jxulou0wpJNiXDZmEYvfpW8o/edit#
    return (
        <Grommet theme={wichacksGrommetTheme}>
            <Box pad="small">
                <Heading>WiCHacks Application</Heading>
                {submissionError?.error && /** Ruh roh scooby doo */
                    <Box background="#c94254" round="small" align="center" justify="between" pad="medium" margin={{ bottom: "medium" }} direction="row">
                        <Text><Text weight="bold">Error Submitting Application:</Text> {submissionError?.description}</Text>
                        <Button plain onClick={ () => { setSubmissionError({"error": false, "description": "" }) } }>
                            <Close size="medium" />
                        </Button>
                    </Box>
                }
                <Box>
                    <Form>
                        <Box>
                            <Heading level={2} margin="none">General Information</Heading>
                            <Paragraph fill>This section will gather information about you to help us keep in touch, determine elligibility, and plan for WiCHacks!</Paragraph>
                            <Box background="#714ba0" height="4px" round="2px" margin={{ bottom: "medium" }}/>
                            
                            <Box>
                                <Heading margin="none" level={4}>Gender</Heading>
                                <TextInput placeholder="How you identify" value={gender} onChange={ e => setGender(e.target.value) } />
                            </Box>
                            
                            <Box margin={{ vertical: "medium" }}>
                                <Heading margin="none" level={4}>Major(If Applicable)</Heading>
                                <TextInput placeholder="What you study" value={major} onChange={ e => setMajor(e.target.value) } />
                            </Box>

                            <Box>
                                <Heading level={4} margin="none">Current Level of Study</Heading>
                                <Select 
                                    placeholder="How Long You've Studied" 
                                    value={levelOfStudy}
                                    onChange={ e => setLevelOfStudy(e.target.value) } 
                                    options={["High School", "First Year Undergraduate", "Second Year Undergraduate", "Third Year Undergraduate", "Fourth Year Undergraduate", "Fifth Year Undergraduate", "Graduate Studies", "Other"]} 
                                />
                            </Box>

                            {levelOfStudy && isLevelOfStudyOther(levelOfStudy) &&
                                <FormField label={
                                    <Box>
                                        <Text>Other Level of study: </Text>
                                    </Box>
                                }>
                                    <TextInput value={otherLevelOfStudy} onChange={ e => setOtherLevelOfStudy(e.target.value) } />
                                </FormField>
                            }
                            
                            <Box margin={{ vertical: "medium" }}>
                                <Heading level={4} margin="none">Date of Birth</Heading>
                                <Text size="small" color="gray">Only those over the age of 18 can participate in this hackathon. Under 18? Reach out to us for
                                    information about ROCGirlHacks, WiC’s hackathon for minors!</Text>
                                    <DateInput
                                        defaultValue={(new Date()).toISOString()}
                                        format="yyyy-mm-dd"
                                        onChange={ (e) => setBirthday(e.target.value) }
                                    />
                            </Box>

                            <div className={css.selectDiv}>
                                School:
                                <select className={css.formSelect} value={university} onChange={e => setUniversity(e.target.value)}>
                                    <option value="none" selected disabled hidden>Select your School</option>
                                    <option value="RIT">Rochester Institute of Technology</option>
                                    <option value="Waterloo">University of Waterloo</option>
                                    <option value="SUNY Oswego">SUNY Oswego</option>
                                    <option value="Syracuse">Syracuse University</option>
                                    <option value="Cornell">Cornell</option>
                                    <option value="Ithaca">Ithaca</option>
                                    <option value="other">Other</option>
                                </select>
                            </div>

                            {university && isSchoolOther(university) && // Alex please fix me
                                <>
                                    <label>
                                        Please enter the name of your school:
                                        <input className={css.textInput} value={otherUniversity} onChange={e => setOtherUniversity(e.target.value)} type={"text"} />
                                    </label><br />
                                </>
                            }

                            <Box>
                                <Heading level={4} margin="none">Shirt Size</Heading>
                                <Select 
                                    placeholder="My shirt size is..." 
                                    value={shirtSize}
                                    onChange={ e => setShirtSize(e.target.value) }
                                    options={ [ "X-Small", "Small", "Medium", "Large", "X-Large", "XX-Large", "XXX-Large" ] }
                                />
                            </Box>

                            <Box margin={{ top: "medium" }}>
                                <Text margin={{ bottom: "small" }}>Have you participated in any hackathons before?</Text>
                                <RadioButtonGroup
                                    options={ ["Yes    ", "No    "] }
                                    name="wantBus"
                                    onChange={ (e) => { setAttendedHackathonsInput(e.target.value === "Yes    " ? "true" : "false" ) } }
                                />
                            </Box>

                            <Box margin={{ top: "medium" }}>
                                <Text margin={{ bottom: "small" }}>Have you participated in WiCHacks before?</Text>
                                <RadioButtonGroup
                                    options={ ["Yes   ", "No   "] }
                                    name="wantBus"
                                    onChange={ (e) => { setAttendedWiCHacksInput(e.target.value === "Yes   " ? "true" : "false" ) } }
                                />
                            </Box>
                        </Box>
                        {/** MARK: Section Two */}
                        <Box>
                            <Heading level={2} margin={{ bottom: "none", top: "medium" }}>Attendance and Travel</Heading>
                            <Paragraph fill>This section will gather information about how you'll be participating this weekend!</Paragraph>
                            <Box background="#714ba0" height="4px" round="2px" margin={{ bottom: "medium" }}/>

                            <Text margin={{ bottom: "small" }}>How will you be participating?</Text>
                            
                            <RadioButtonGroup 
                                options={ ["In-Person", "Online Only"] }
                                name="isVirtual"
                                onChange={ (e) => { setIsVirtual(e.target.value === "In-Person" ? "true" : "false" ) } }
                            />

                            {eligibleForBusing &&
                                <Box>
                                    <Box margin={{ top: "medium" }}>
                                        <Text margin={{ bottom: "small" }}>Would you like to travel to RIT via one of the buses?</Text>
                                        <RadioButtonGroup 
                                            options={ ["Yes  ", "No  "] }
                                            name="wantBus"
                                            onChange={ (e) => { setBusRider(e.target.value === "Yes  " ? "true" : "false" ) } }
                                        />
                                    </Box>
                                    {(busRider && busRider === "true") &&
                                        <Box margin={{ top: "medium" }}>
                                            <Text margin={{ bottom: "small" }}>At which stop would you like to board the bus?</Text>
                                            <Select 
                                                placeholder="I will board..." 
                                                value={busStop}
                                                onChange={ e => setBusStop(e.target.value) } 
                                                options={[ "University of Toronto", "University of Waterloo", "SUNY Buffalo", "Skidmore College", "RPI", "Siena College", "SUNY Albany", "Union College" ]} 
                                            />
                                        </Box>
                                    }
                                </Box>
                            }
                            <hr className={css.sectionBreak}/>
                        </Box>
                        {/** MARK: Section Three */}
                        <Box>
                            <Heading level={2} margin="none">Accommodations and Information</Heading>
                            <Paragraph fill>This section will gather information about how you'll be participating this weekend!</Paragraph>
                            <Box background="#714ba0" height="4px" round="2px" margin={{ bottom: "medium" }}/>

                            <Text margin={{ bottom: "small" }}>Do you have any dietary restrictions?</Text>
                            
                            <RadioButtonGroup 
                                options={ ["Yes", "No"] }
                                name="dietary"
                                onChange={ (e) => { setHasDietaryRestriction(e.target.value === "Yes" ? "true" : "false") } }
                            />

                            {(hasDietaryRestriction === "true") &&
                                <Box margin={{ top: "medium", bottom: "medium" }}>
                                    <Text>Please list your dietary restrictions below so we can ensure to have food available for you:</Text>
                                    <TextArea 
                                        placeholder="My dietary restrictions are..."
                                        value={dietaryRestriction}
                                        onChange={ (e) => { setDietaryRestriction(e.target.value) } }
                                    />
                                </Box>
                            }

                            <Text margin={{ top: "medium" }}>Will you require any special accommodations you feel may not be already planned?</Text>
                            <Text color="gray" size="small" margin={{ bottom: "small" }}>Please note, this includes a need for interpreting/captioning services. WiCHacks plans to provide these services during opening and closing ceremonies but needs to identify those requiring these services to RIT. Additionally, please report this request to RIT Department of Access Services.</Text>
                            
                            <RadioButtonGroup 
                                options={ ["Yes ", "No "] }
                                name="specialAccomodations"
                                onChange={ (f) => { setHasSpecialAccommodations(f.target.value === "Yes " ? "true" : "false") } }
                            />
                            
                            {(hasSpecialAccommodations === "true") &&
                                <Box margin={{ top: "medium", bottom: "medium" }}>
                                    <Text>Please elaborate below</Text>
                                    <TextArea 
                                        placeholder="My dietary restrictions are..."
                                        value={specialAccommodations}
                                        onChange={ (e) => { setSpecialAccommodations(e.target.value) } }
                                    />
                                </Box>
                            }
                        </Box>
                        <Box>
                            <Heading level={2} margin={{ top: "medium", bottom: "none" }}>Agreements</Heading>
                            <Paragraph fill>This section will gather information about how you'll be participating this weekend!</Paragraph>
                            <Box background="#714ba0" height="4px" round="2px" margin={{ bottom: "medium" }}/>
                            <Box gap="small">
                                <CheckBox label={ 
                                    <Text>I have read and agree to the <a href="https://www.rit.edu/academicaffairs/policiesmanual/c000" target="_blank" rel="noreferrer">RIT Code of Ethical Conduct and Compliance</a> </Text> 
                                } onChange={(e) => {
                                    if (e.target.type === 'checkbox') {
                                        setRitEventPolicies(true)
                                    } else {
                                        setRitEventPolicies(false)
                                    }
                                }}/>
                                <CheckBox label={ 
                                    <Text>I have read and agree to the <a href="https://static.mlh.io/mlh-code-of-conduct.pdf" target="_blank" rel="noreferrer">MLH Code of Conduct</a></Text> 
                                } onChange={(e) => {
                                    if (e.target.type === 'checkbox') {
                                        setMlhCodeOfConduct(true)
                                    } else {
                                        setMlhCodeOfConduct(false)
                                    }
                                }}/>
                                <CheckBox label={ 
                                    <Text>I authorize WiCHacks to share my application/registration information with Major League Hacking for event administration,
                                    ranking, and MLH administration in-line with the <a href="https://mlh.io/privacy" target="_blank" rel="noreferrer">MLH Privacy Policy</a>. I further agree to the
                                    terms of both the <a href="https://github.com/MLH/mlh-policies/blob/main/contest-terms.md" >MLH Contest Terms and Conditions</a> and the <a href="https://mlh.io/privacy" target="_blank" rel="noreferrer">MLH Privacy Policy</a>.</Text> 
                                } onChange={(e) => {
                                    if (e.target.type === 'checkbox') {
                                        setMlhDataSharing(true)
                                    } else {
                                        setMlhDataSharing(false)
                                    }
                                }}/>
                                <CheckBox label={ 
                                    <Text>By submitting my application to WiCHacks I confirm all provided information is accurate and I will inform the WiCHackshackathon organizers should any information change</Text> 
                                } onChange={(e) => {
                                    if (e.target.type === 'checkbox') {
                                        setAllInformationCorrect(true)
                                    } else {
                                        setAllInformationCorrect(false)
                                    }
                                }}/>
                            </Box>
                        </Box>
                        <Box className={css.applicationSubmitButton}>
                            <Button type="submit" onClick={submitUserCreation}>
                                <Box background="#714ba0" pad="medium" align="center" justify="center" style={{ borderRadius: "20px" }} width="medium">
                                    <Text weight="bold" size="large">Submit Application</Text>
                                </Box>
                            </Button>
                        </Box>
                    </Form>
                </Box>
            </Box>
        </Grommet>
    );
}