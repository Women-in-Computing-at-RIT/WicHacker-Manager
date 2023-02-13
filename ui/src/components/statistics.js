import {useEffect, useState} from "react";
import {useAuth0} from "@auth0/auth0-react";
import {getUserData} from "../utils/users";
import {apiDomain, getAxios} from "../config/axios";
import LoadingView from "../pages/LoadingView";
import {WiCHacksTable} from "./table";
import css from "./style/statistics.module.css"
import { Box, Heading, Text } from "grommet";
import {useNavigate} from "react-router-dom";

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
    },
    {
        displayName: 'Count',
        dataKey: 'count',
    }
];

const shirtCountColumns = [
    {
        displayName: 'Size',
        dataKey: 'value',
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
        dataScope: 'row' // exception not rule to avoid formatting
    },
    {
        displayName: 'Count',
        dataKey: 'count',
    }
];

const busStopCountColumns = [
    {
        displayName: 'Bus Stop',
        dataKey: 'value',
        dataScope: 'row'
    },
    {
        displayName: 'Count',
        dataKey: 'count',
    }
];

const isVirtualCountColumns = [
    {
        displayName: 'Hacker Attendance',
        dataKey: 'value',
        dataScope: 'row',
        format: userData => userData["value"] === "1" ? "Virtual" : "In Person",
    },
    {
        displayName: 'Count',
        dataKey: 'count',
    }
];

const translateCountJSONToList = (map) => {
    if(!map){
        return []
    }
    let list = []
    for (const [key, value] of Object.entries(map)) {
        list.push({"count": value, "value": key})
    }
    return list
}

export function StatisticsView(){
    const [statisticsResponse, setStatisticsResponse] = useState();
    const {getAccessTokenSilently} = useAuth0();

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
            <div className={css.statisticsTable}>
                <WiCHacksTable title={"Application Statuses"} data={translateCountJSONToList(statistics['applications'])} columns={hackerCountColumns}/>
            </div>
            <div className={css.statisticsTable}>
                <WiCHacksTable title={"Shirt Size Counts"} data={translateCountJSONToList(statistics['shirts'])} columns={shirtCountColumns}/>
            </div>
            <div className={css.statisticsTable}>
                <WiCHacksTable title={"Hackers By School"} data={translateCountJSONToList(statistics['schools'])} columns={schoolCountColumns}/>
            </div>
            <div className={css.statisticsTable}>
                <p>Number of Different Schools Accepted: {statistics['schoolCount']}</p>
            </div>
            <div className={css.statisticsTable}>
                <WiCHacksTable title={"Bussing"} data={translateCountJSONToList(statistics['busStops'])} columns={busStopCountColumns}/>
            </div>
            <div className={css.statisticsTable}>
                <WiCHacksTable title={"Attendance"} data={translateCountJSONToList(statistics['isVirtual'])} columns={isVirtualCountColumns} />
            </div>
        </div>
    );
}