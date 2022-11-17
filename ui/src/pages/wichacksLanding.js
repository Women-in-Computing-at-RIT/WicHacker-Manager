import {useNavigate} from "react-router-dom";
import {Grommet, Button} from "grommet";

export default function WiCHacksLanding() {
    let navigate = useNavigate()

    const onClickNavigate = (path) => {
        navigate(path)
    }

    return (
        <Grommet>
            <div>
                <h1>WiCHacks</h1>

                <Button label="Hackers" onClick={() => {onClickNavigate("/user")}}/>
                <Button label="Admins" onClick={() => {onClickNavigate("/manage")}}/>
            </div>
        </Grommet>
    );
}
