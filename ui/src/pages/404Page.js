import { Grommet, Box, Text, Button } from "grommet";
import { Twitter, Facebook, Instagram } from "grommet-icons";

export default function PageNotFound() {
    return (
        <Grommet>
            <Box background="#714ba0" flex="grow" pad="medium" height="100vh">
                <Text color="white" weight="bold" size="140pt">:(</Text>
                <Box>
                    <Text margin={{ vertical: "large" }} size="large" weight="bold">We ran into a problem, and we didn't know where to send you. Now you need to choose.</Text>
                    <Text>You can't search online for the solution, but you can click a link below!</Text>
                    <Button plain href="/user" margin={{ vertical: "medium" }}>
                        <Box background="white" style={{ borderRadius: "20px"}} pad="medium" width="medium" align="center" justify="center">
                            <Text weight="bold" color="#714ba0" size="large">Apply to WiCHacks</Text>
                        </Box>
                    </Button>

                    <Button plain href="https://wichacks.io">
                        <Box background="white" style={{ borderRadius: "20px"}} pad="medium" width="medium" align="center" justify="center">
                            <Text weight="bold" color="#714ba0" size="large">Learn About WiCHacks</Text>
                        </Box>
                    </Button>

                    <Box direction="row" align="center" justify="center" width="medium" margin={{ top: "medium" }}>
                        <Button plain href="https://twitter.com/wichacks?lang=en">
                            <Twitter />
                        </Button>
                        <Button plain href="https://www.instagram.com/wichacks/" margin={{horizontal: "medium"}}>
                            <Instagram />
                        </Button>
                        <Button plain href="https://www.facebook.com/wic.hacks.rit/">
                            <Facebook />
                        </Button>
                    </Box>
                </Box>
            </Box>
        </Grommet>
    );
}