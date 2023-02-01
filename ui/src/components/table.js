import React from 'react'
import {
    Grommet,
    Table, TableBody, TableCell, TableHeader, TableRow,
    Text,
} from 'grommet';

// examples below
// code based on Grommet component example
export const WiCHacksTable = ({title, data, columns}) => (
    <Grommet>
        <Table caption={title}>
            <TableHeader>
                <TableRow>
                    {columns.map(c => (
                        <TableCell key={c.displayName} scope='col' border='bottom' >
                            <Text>{c.displayName}</Text>
                        </TableCell>
                    ))}
                </TableRow>
            </TableHeader>
            <TableBody>
                {data.map(dataItem => (
                    <TableRow key={dataItem.id}>
                        {columns.map(c => (
                            <TableCell key={c.displayName + c.dataKey} scope={c.dataScope}>
                                <Text>
                                    {c.format ? c.format(dataItem) : dataItem[c.dataKey]}
                                </Text>
                            </TableCell>
                        ))}
                    </TableRow>
                ))}
            </TableBody>
        </Table>
    </Grommet>
);


// ============== EXAMPLES ==================

const data_example = [
    {
        id: 1, name: 'Eric', email: 'eric@local', amount: 3775,
    },
    {
        id: 2, name: 'Chris', email: 'chris@local', amount: 5825,
    },
    {
        id: 3, name: 'Alan', email: 'alan@local', amount: 4300,
    },
];

// functional formatter example
const amountFormatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
});

const column_example = [
    {
        displayName: 'Name',
        dataKey: 'name',
        dataScope: 'row',
        format: datum => <strong>{datum.name}</strong>,
    },
    {
        displayName: 'Email',
        dataKey: 'email',
    },
    {
        displayName: 'Amount',
        dataKey: 'amount',
        format: datum => amountFormatter.format(datum.amount / 100),
    },
];