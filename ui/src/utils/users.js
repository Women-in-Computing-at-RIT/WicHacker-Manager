import {apiDomain, getAxios} from "../config/axios";

export const getUserData = async(getAccessTokenSilently, setUserResponse, setNewUser) => {
    const token = await getAccessTokenSilently({
        audience: 'wichacks.io',
    });
    const config = {
        headers: { Authorization: `Bearer ${token}`}
    }
    getAxios().get(apiDomain() + `/user`, config)
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