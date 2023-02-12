import {useEffect, useState} from "react";
import {useAuth0} from "@auth0/auth0-react";
import {apiDomain, getAxios} from "../config/axios";
import LoadingView from "../pages/LoadingView";
import {WiCHacksTable} from "./table";
import css from "./style/statistics.module.css"


const getAccommodationData = async(getAccessTokenSilently, setAccommodations) => {
    const token = await getAccessTokenSilently({
        audience: 'wichacks.io',
    });
    const config = {
        headers: { Authorization: `Bearer ${token}`}
    }
    getAxios().get(apiDomain() + `/accommodations`, config)
        .then(async (response) => {
            setAccommodations({data: await response.data, error: null})
        }).catch(async () => {
            setAccommodations({data: null, error: true})
    })
}

const hackerAccomodationsColumns = [
    {
        displayName: 'Dietary Restrictions',
        dataKey: 'dietaryRestrictions',
    },
    {
        displayName: 'Special Accommodations',
        dataKey: 'specialAccommodations',
    },
    {
        displayName: 'Email',
        dataKey: 'email',
    },
    {
        displayName: 'First Name',
        dataKey: 'firstName',
    },
    {
        displayName: 'Last Name',
        dataKey: 'lastName',
    }
];

export function AccommodationsView(){
    const [accommodationsResponse, setAccommodationsResponse] = useState();
    const {getAccessTokenSilently} = useAuth0();

    useEffect(() => {
        getAccommodationData(getAccessTokenSilently, setAccommodationsResponse)
    }, [])

    if (!accommodationsResponse){
        return (<LoadingView />);
    }
    if (accommodationsResponse?.error){
        return (<p>Error Loading Statistics, please contact the website manager</p>);
    }

    const accommodations = accommodationsResponse.data;

    return (
        <div>
            <div className={css.statisticsTable}>
                <WiCHacksTable title={"Accommodations"} data={accommodations} columns={hackerAccomodationsColumns}/>
            </div>
        </div>
    );
}