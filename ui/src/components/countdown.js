import React, { Component } from 'react';
import { Grommet, Box, Text, Button, Clock } from "grommet";
import Countdown from 'react-countdown';

/** Documentation because I'm a little lazy: any children will replace the view on the right of this bar, otherwise will display a countdown to WiCHacks */
class WHCountdown extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        const renderer = ({ })
        return (
            <Grommet>
                <Box background="#714ba0" direction="row" align="center" gap="small">
                    <Countdown date={ new Date("March 2, 2024 12:00:00") }/>
                    <Text>Until WiCHacks</Text>
                </Box>
            </Grommet>
        );
    }
}
export default WHCountdown;