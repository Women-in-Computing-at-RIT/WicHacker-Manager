import axios from 'axios'

export const localAxios = axios.create(
    {
        proxy: {
            protocol: 'http',
            host: 'localhost',
            port: 3000
        }
    }
)
const prodAxios = axios.create()

export const localApiDomain = "http://localhost:5002"
export const prodApiDomain = "http://localhost:5002"

export const apiDomain = () => {
    return prodApiDomain
}

export const getAxios = () => {
    return prodAxios
}