import {useNavigate} from "react-router-dom";
import {Grommet, Button, Box, Heading, Paragraph } from "grommet";

export default function WiCHacksLanding() {
    let navigate = useNavigate()

    const onClickNavigate = (path) => {
        navigate(path)
    }

    return (
        <Grommet>
            <Box direction="column" justify="center" align="center">
                <Heading color="#714ba0">WiCHacks</Heading>
                <Heading level={2}>March 4th - 5th</Heading>
                <Heading level={3}>Registrations Are Open!</Heading>
                <Paragraph>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum</Paragraph>
                <Box direction="row">
                    <Button label="Hackers" onClick={() => {onClickNavigate("/user")}} />
                    <Button label="Admins" onClick={() => {onClickNavigate("/manage")}} />
                </Box>
            </Box>
        </Grommet>
    );
}
