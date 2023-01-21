import React, { Component } from 'react';
import { Grommet, Box, Text, Button } from "grommet";

/** Documentation because I'm a little lazy: any children will replace the view on the right of this bar, otherwise will display a countdown to WiCHacks */
class NavBar extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <Grommet>
                <Box background="#714ba0" pad="medium" direction="row" align="center" justify="between">
                    <Text weight="bold">{this.props.title}</Text>
                    <Box>
                        {this.props.children ? this.props.children :
                            <></> // add countdown to wichacks
                        }
                    </Box>
                </Box>
            </Grommet>
        );
    }
}
export default NavBar;