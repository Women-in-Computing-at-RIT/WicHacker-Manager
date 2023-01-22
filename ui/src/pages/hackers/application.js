import {useNavigate} from "react-router-dom";
import {useEffect, useState} from "react";
import {apiDomain, localAxios} from "../../config/axios";
import {useAuth0} from "@auth0/auth0-react";
import css from "./style/form.module.css"
import { Grommet, Box, Form, Heading, Button, Paragraph, FormField, TextInput, Text, Select, CheckBox, RadioButtonGroup, TextArea, DateInput, Image } from 'grommet';
import { Close } from "grommet-icons";
import wichacksGrommetTheme from "../../wichacksGrommetTheme";
import Autocomplete from "../../components/autocompleteTextbox";
import { NumberInput } from 'grommet-controls';
import { Alert } from 'grommet-icons';
import {mlhSchoolList} from "../../data/mlh";
import NavBar from "../../components/navBar";

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
        return levelOfStudy === "Other";
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
            "age": age,
            "shirtSize": shirtSize,
            "hasAttendedWiCHacks": (hasAttendedWiCHacks && hasAttendedWiCHacks === "true"),
            "hasAttendedHackathons": (hasAttendedHackathons && hasAttendedHackathons === "true"),
            "university": university,
            "gender": gender,
            "busRider": (eligibleForBusing && busRider === "true"),
            "busStop": busStop,
            "dietaryRestrictions": dietaryRestriction,
            "specialAccommodations": specialAccommodations,
            "affirmedAgreements": affirmedAgreements,
            "mlhEmailsAllowed": mlhEmails,
            "isVirtual": (isVirtual && isVirtual === "true")
        }
        await createApplication(userData, getAccessTokenSilently, setSubmissionError, navigateToPage)
    }

    const [major, setMajor] = useState();
    const [levelOfStudy, setLevelOfStudy] = useState();
    const [otherLevelOfStudy, setOtherLevelOfStudy] = useState();
    const [age, setAge] = useState();
    const [shirtSize, setShirtSize] = useState();
    const [hasAttendedWiCHacks, setAttendedWiCHacksInput] = useState();
    const [hasAttendedHackathons, setAttendedHackathonsInput] = useState();
    const [university, setUniversity] = useState();
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
    const [mlhEmails, setMLHEmails] = useState();
    const [allInformationCorrect, setAllInformationCorrect] = useState();
    const [isVirtual, setIsVirtual] = useState();

    const [mlhSchoolSuggestions, setMLHSchoolSugggestions] = useState();

    const matchesSchoolFilter = (e) => {
        const re = new RegExp('.*' + university + '.*', 'i')
        return re.test(e);
    };

    const updateUniversity = (e) => {
        setUniversity(e.target.value);
        setMLHSchoolSugggestions(mlhSchoolList.filter( (sugg) => { return matchesSchoolFilter(sugg) } ))
    }

    let eligibleForBusing = (university !== "Rochester Institute of Technology (RIT)") && (isVirtual && isVirtual === "true")

    // form based on Registration Form Guideline https://docs.google.com/document/d/1FxLkwcFK-W513G10m53Jxulou0wpJNiXDZmEYvfpW8o/edit#
    return (
        <Grommet theme={wichacksGrommetTheme}>
            <NavBar title="WiCHacks" />
            <Box pad="small">
                <Heading>WiCHacks Application</Heading>
                <Box background="#ded492" round="small" align="center" justify="between" pad="medium" margin={{ bottom: "medium" }} direction="row">
                    <Text>We're excited you want to apply to attend WiCHacks 2023! This form will collect information about you, and how you'd like to attend. If you have any questions or concerns about this form, please email <a href="mailto:wichacks@rit.edu" target="_blank" rel="noreferrer">wichacks@rit.edu</a> and our team will work with you.</Text>
                </Box>
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
                                <Text size="small" color="gray">Due to the proven systematic oppression of people identifying as gender minority in computing fields, WICHacks is a gender-minority only hackathon. Gender minority is being defined as cisgendered women, nonbinary individuals, transgender people, and all other people who have been systematically oppressed on the basis of gender identity. As such, we are collecting information about how you identify to determine your eligibility to participate. Others, including cisgender men, will be denied participation for this event</Text>
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
                                    options={["Less than Secondary / High School", "Secondary / High School", "Undergraduate University (2 year - community college or similar)", "Undergraduate University (3+ year)", "Graduate University (Masters, Professional, Doctoral, etc)", "Code School / Bootcamp", "Other Vocational / Trade Program or Apprenticeship", "Other", "I'm not currently a student", "Prefer not to answer"]} 
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
                                <Heading level={4} margin="none">Age</Heading>
                                <Text size="small" color="gray">Only those over the age of 18 can participate in this hackathon. Under 18? Reach out to us for information about ROCGirlHacks, WiC’s hackathon for minors!</Text>
                                <NumberInput 
                                    onChange={setAge}
                                    placeholder="I am... "
                                />
                            </Box>

                            <Box>
                                <Heading level={4} margin="none">School or University Name</Heading>
                                <TextInput
                                    placeholder="University..."
                                    onChange={updateUniversity}
                                    value={university}
                                    onSuggestionSelect={(e) => { setUniversity(e.suggestion); }}
                                    suggestions={mlhSchoolSuggestions}
                                />
                            </Box>

                            <Box>
                                <Heading level={4} margin={{ top: "medium", bottom: "none" }}>Shirt Size</Heading>
                                <Select 
                                    placeholder="My shirt size is..." 
                                    value={shirtSize}
                                    onChange={ e => setShirtSize(e.target.value) }
                                    options={ [ "X-Small", "Small", "Medium", "Large", "X-Large", "XX-Large", "XXX-Large" ] }
                                />
                            </Box>

                            <Box margin={{ top: "medium" }}>
                                <Heading level={4} margin={{ bottom: "none", top: "none" }}>Have you participated in any hackathons before?</Heading>
                                <Text size="small" color="gray" margin={{ bottom: "small" }}>This will not affect your elligibility for WiCHacks</Text>
                                <RadioButtonGroup
                                    options={ ["Yes    ", "No    "] }
                                    name="wantBus"
                                    onChange={ (e) => { setAttendedHackathonsInput(e.target.value === "Yes    " ? "true" : "false" ) } }
                                />
                            </Box>

                            <Box margin={{ top: "medium" }}>
                                <Heading level={4} margin={{ bottom: "none", top: "none" }}>Have you participated in WiCHacks before?</Heading>
                                <Text size="small" color="gray" margin={{ bottom: "small" }}>This will not affect your elligibility for WiCHacks</Text>
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
                            <Box background="#714ba0" height="4px" round="2px"/>

                            <Heading level={4} margin={{ top: "medium", bottom: "small" }}>How will you be participating?</Heading>
                            <Text>This year, WiCHacks is inviting all individuals to participate in person at RIT, or online through our Discord platform. If in-person, you can take one of the provided buses or your own transportation to RIT. Parking will be provided.</Text>
                            <RadioButtonGroup
                                options={ ["In-Person", "Online Only"] }
                                name="isVirtual"
                                onChange={ (e) => { setIsVirtual(e.target.value === "In-Person" ? "true" : "false" ) } }
                                margin={{ bottom: "medium", top: "small" }}
                            />

                            {eligibleForBusing &&
                                <Box pad="small" background="#ded492" round="small">
                                    <Box> {/** Information on bussing */}
                                        <Heading level={3} margin={{ vertical: "small" }}>WiCHacks has buses this year!</Heading>
                                        <Text>To help more of our participants enjoy WiCHacks in person this year, we'll be sending out two buses to provide you transportation to and from the event. Buses will pick up participants early Saturday 3/4/23 morning, and return you to your respective stops Sunday 3/5/23 evening. One bus will be traveling from Toronto, and the other from Albany area.</Text>
                                        <Text weight="bold">See Image Below For Bus Route Information</Text>
                                        <Box pad="small" background="#fff" border={{ color: "#000", size: "medium" }} round="small">
                                            <Image
                                                round="small"
                                                src="/REPLACEME_busroutes.jpg"
                                            />
                                        </Box>
                                        <Box direction="row" background="#c94254" round="small" align="center" margin={{ vertical: "small" }} pad="small" gap="small">
                                            <Alert />
                                            <Text weight="bold">Please note, filling out the below does not guarantee you a spot on buses. WiCHacks organizers will reach out with more information.</Text>
                                        </Box>
                                    </Box>
                                    <Box>
                                        <Heading level={4} margin={{ top: "none", bottom: "small" }}>Would you like to travel to RIT via one of the buses?</Heading>
                                        <RadioButtonGroup 
                                            options={ ["Yes  ", "No  "] }
                                            name="wantBus"
                                            onChange={ (e) => { setBusRider(e.target.value === "Yes  " ? "true" : "false" ) } }
                                        />
                                    </Box>
                                    {(busRider && busRider === "true") &&
                                        <Box margin={{ top: "medium" }}>
                                            <Heading level={4} margin={{ bottom: "small", top: "none" }}>At which stop would you like to board the bus?</Heading>
                                            <Select 
                                                placeholder="I will board..." 
                                                value={busStop}
                                                onChange={ e => setBusStop(e.target.value) } 
                                                options={[ "University of Toronto", "University of Waterloo", "SUNY Buffalo", "Skidmore College", "Rensselaer Polytechnic Institute", "Siena College", "SUNY Albany", "Union College" ]} 
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
                            <Paragraph fill>This section helps us figure out how to best ensure you have a great weekend!</Paragraph>
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
                            <Paragraph fill>We have to make sure everyone at WiCHacks is safe and has a good time! Take a moment to read the agreements below</Paragraph>
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
                                    <Text>[OPTIONAL] I authorize MLH to send me an email where I can further opt into the MLH Hacker, Events, or Organizer Newsletters and other communications from MLH.</Text> 
                                } onChange={(e) => {
                                    if (e.target.type === 'checkbox') {
                                        setMLHEmails(true)
                                    } else {
                                        setMLHEmails(false)
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
                        <Box margin={{ vertical: "medium" }}>
                            <Button type="submit" onClick={submitUserCreation}>
                                <Box background="#714ba0" pad="medium" align="center" justify="center" style={{ borderRadius: "20px" }} width="medium">
                                    <Text weight="bold" size="large">Submit Application</Text>
                                </Box>
                            </Button>
                        </Box>
                        <Box color="gray" align="center" gap="small" direction="row">
                            <Alert size="medium" />
                            <Text size="small">Submitting your application does not guarantee participation. You will receive emails with more information within 3-5 business days</Text>
                        </Box>
                    </Form>
                </Box>
            </Box>
        </Grommet>
    );
}