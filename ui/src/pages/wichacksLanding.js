import { useNavigate } from "react-router-dom";
import { Grommet, Button, Box, Header, Text, Heading, Paragraph } from "grommet";

export default function WiCHacksLanding() {
    let navigate = useNavigate()

    const onClickNavigate = (path) => {
        navigate(path)
    }

    return (
        <Grommet>
            <Header background="purple" pad="small">
                <Text color="white" weight="bold">WiCHacks Application Manager</Text>
                <Button color="white" label="Manage Application" plain/>
            </Header>
            <Box direction="row">
                <Box width="50%" pad="large" align="start">
                    <Heading>WiCHacks 2023</Heading>
                    <Heading level={3} margin="none">March 4-5, 2023</Heading>
                    <Paragraph>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</Paragraph>
                    <Text>Read More on <Button plain color="purple" weight="bold" href="https://wichacks.io">our website</Button></Text>
                </Box>
                <Box width="50%" align="center" justify="center">
                    <Button onClick={() => {onClickNavigate("/user")}} margin="medium">
                        <Box background="purple" pad="small" width="medium" align="center" round="small">
                            <Text color="white" weight="bold">Hackers</Text>
                        </Box>
                    </Button>
                    <Button plain onClick={() => {onClickNavigate("/manage")}}>
                        <Text color="purple">Are You An Organizer? Manage Applications</Text>
                    </Button>
                </Box>
            </Box> {/* Main Section End */}
        </Grommet>
    );
}
