import {useNavigate} from "react-router-dom";
import {Grommet, Button, Box, Heading, Paragraph, Image, Text } from "grommet";
import { Home } from "grommet-icons";
import NavBar from "../components/navBar";

export default function WiCHacksLanding() {
    let navigate = useNavigate()
    return (
        <Grommet>
            <NavBar title="WiCHacks" />
            <Box direction="column" justify="center" align="center" flex="grow">
                <Box pad={{left: "large", right: "large"}}>
                    <Image src="/wichackslogo.svg" a11yTitle="WiCHacks Logo, beneath is RIT Women in Computing written out" style={{ maxWidth: "100%", maxHeight: "100%" }} />
                </Box>
                <Heading responsive margin="none" level={2}>March 4th - 5th, 2023</Heading>
                <Heading fill responsive margin="small" textAlign="center" level={3}>MAGIC Spell Studios at RIT, or digitally from anywhere in the world</Heading>
                <Paragraph fill responsive margin={{ left: "large", right: "large", top: "small"}} textAlign="center">💜 WiCHacks is coming up soon! Our annual hackathon will be happening this March, and registration is open now! You can participate in-person at RIT, or online from anywhere in the world. Click below to get started! 💜</Paragraph>
                <Box direction="column">
                    <Button onClick={() => {navigate("/user")}}>
                        <Box background="#714ba0" pad="medium" align="center" justify="center" style={{ borderRadius: "20px" }}>
                            <Text weight="bold" size="large">Apply Now!</Text>
                        </Box>
                    </Button>

                    <Button plain onClick={() => {navigate("/user")}}>
                        <Box pad="small">
                            <Text style={{ textDecoration: "underline" }}>Already Applied? Check Your Application</Text>
                        </Box>
                    </Button>
                </Box>

                <Button plain href="https://wichacks.io">
                    <Box direction="row" align="center" justify="center" background="#f0e1f4" pad="small" style={{ borderRadius: "20px" }}>
                        <Home color="#4e1560" />
                        <Text margin={{ left: "small" }} color="#4e1560" style={{ textDecoration: "underline" }} >Learn about WiCHacks</Text>
                    </Box>
                </Button>
            </Box>
        </Grommet>
    );
}
