import axios from 'axios'

export const localAxios = axios.create(
    {
        proxy: {
            protocol: 'https',
            host: 'api.wichacks.io',
            port: 433
        }
    }
)

export const apiDomain = "https://api.wichacks.io"