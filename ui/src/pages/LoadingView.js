import { Grommet, Box, Spinner } from "grommet";

export default function LoadingView() {
    return (
        <Grommet>
            <Box background="#714ba0" flex="grow" pad="medium" height="100vh" align="center" justify="center">
                <Spinner message="Loading..." size="xlarge" color="white" />
            </Box>
        </Grommet>
    );
}