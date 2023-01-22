// Thank you to EasyWebsify from Medium for the autocomplete component
import React, { useState } from "react";
import { Box, List, Text, TextInput } from 'grommet';
import css from "./style/autocompleteTextbox.module.css"


const Autocomplete = ({suggestions, value, setValue}) => {
    const [active, setActive] = useState(0);
    const [filtered, setFiltered] = useState([]);
    const [isShow, setIsShow] = useState(false);


    const onChange = e => {
        const re = new RegExp('.*' + e.currentTarget.value + '.*', 'i')
        setValue(e.currentTarget.value)
        setActive(0);
        const newFilteredSuggestions = suggestions.filter(
            suggestion => re.test(suggestion)
        );
        setFiltered(newFilteredSuggestions);
        setIsShow(true);

    };
    const onClick = e => {
        setActive(0);
        setFiltered([]);
        setIsShow(false);
        setValue(e.currentTarget.innerText)
    };
    const onKeyDown = e => {
        if (e.keyCode === 13) { // enter key
            setActive(0);
            setIsShow(false);
            setValue(filtered[active])
        }
        else if (e.keyCode === 38) { // up arrow
            return (active === 0) ? null : setActive(active - 1);
        }
        else if (e.keyCode === 40) { // down arrow
            return (active - 1 === filtered.length) ? null : setActive(active + 1);
        }
    };
    const renderAutocomplete = () => {
        if (isShow && value) {
            if (filtered.length) {
                return (
                    <List
                        data={filtered.map((suggestion, index) => {
                            return suggestion;
                        })}
                    />
                        // {filtered.map((suggestion, index) => {
                        //     let className;
                        //     if (index === active) {
                        //         className = "active";
                        //     }
                        //     return (
                        //         <li className={className} key={suggestion} onClick={onClick}>
                        //             {suggestion}
                        //         </li>
                        //     );
                        // })}
                );
            }
        }
        return <></>;
    }
    return (
        <Box>
            <TextInput 
                onChange={onChange}
                onKeyDown={onKeyDown}
                value={value}
            />
            {renderAutocomplete()}
        </Box>
    );
}
export default Autocomplete;