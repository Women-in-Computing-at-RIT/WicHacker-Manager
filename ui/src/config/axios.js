import axios from 'axios'

export const localAxios = axios.create(
    {
        proxy: {
            protocol: 'http',
            host: 'localhost',
            port: 5001
        }
    }
)

export const apiDomain = "http://localhost:5002"