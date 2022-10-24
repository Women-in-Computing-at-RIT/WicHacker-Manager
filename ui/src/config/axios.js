import axios from 'axios'

export const localAxios = axios.create(
    {
        proxy: {
            protocol: 'http',
            host: 'api',
            port: 8080
        }
    }
)