import axios from 'axios'

const tenantName = ""
const region = ""
const basepath = `https://${tenantName}.${region}.auth0.com`
const token = ""
const config = {
    headers: { Authorization: `Bearer ${token}`}
}

export const REQUEST_ERROR = Error("Request Error");

/*
Eventually want to make this more secure
 */

export function getUser(userId){
    const url = `${basepath}/api/v2/users/${userId}`
    return axios.get(url, config).catch(function (error){
        console.log("Request Error: ", error)
        return REQUEST_ERROR;
    })
}