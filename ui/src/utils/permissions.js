import {apiDomain, getAxios} from "../config/axios";

export const checkUserPermissions = async (permission, type, getAccessTokenSilently, setHasPermissions) => {
    const token = await getAccessTokenSilently({
        audience: 'wichacks.io',
    });
    const config = {
        headers: { Authorization: `Bearer ${token}`}
    }
    const permissionUrl = apiDomain() + `/permission/` + permission + '/' + type
    getAxios().get(permissionUrl, config)
        .then(async () => {
            setHasPermissions(true)
        }).catch(async () => {
        setHasPermissions(false)
    })
}