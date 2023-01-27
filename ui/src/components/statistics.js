import {useEffect, useState} from "react";
import {useAuth0} from "@auth0/auth0-react";
import {getUserData} from "../utils/users";
import {apiDomain, getAxios} from "../config/axios";
import LoadingView from "../pages/LoadingView";
import {WiCHacksTable} from "./table";

const getHackathonStatistics = async(getAccessTokenSilently, setStatistics) => {
    const token = await getAccessTokenSilently({
        audience: 'wichacks.io',
    });
    const config = {
        headers: { Authorization: `Bearer ${token}`}
    }
    getAxios().get(apiDomain() + `/statistics`, config)
        .then(async (response) => {
            setStatistics({data: await response.data, error: null})
        }).catch(async () => {
            setStatistics({data: null, error: true})
    })
}

const hackerCountColumns = [
    {
        displayName: 'Status',
        dataKey: 'value',
        dataScope: 'row'
    },
    {
        displayName: 'Count',
        dataKey: 'count',
    }
];

const schoolCountColumns = [
    {
        displayName: 'School',
        dataKey: 'value',
        dataScope: 'row'
    },
    {
        displayName: 'Count',
        dataKey: 'count',
    }
];

const translateCountJSONToList = (map) => {
    let list = []
    for (const [key, value] of Object.entries(map)) {
        list.push({"count": value, "value": key})
    }
    return list
}

export function StatisticsView(){
    const [statisticsResponse, setStatisticsResponse] = useState();
    const {getAccessTokenSilently, logout} = useAuth0();

    useEffect(() => {
        getHackathonStatistics(getAccessTokenSilently, setStatisticsResponse)
    }, [])

    if (!statisticsResponse){
        return (<LoadingView />);
    }
    if (statisticsResponse?.error){
        return (<p>Error Loading Statistics, please contact the website manager</p>);
    }

    const statistics = statisticsResponse.data;

    return (
        <div>
            <div>
                <WiCHacksTable title={"Application Status Counts"} data={translateCountJSONToList(statistics['applications'])} columns={hackerCountColumns}/>
            </div>
            <div>
                <WiCHacksTable title={"Hackers By School"} data={translateCountJSONToList(statistics['schools'])} columns={schoolCountColumns}/>
            </div>
            <div>
                <p>Number of Different Schools Accepted: {statistics['schoolCount']}</p>
            </div>
        </div>
    );

}