import React from 'react'
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler,
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler,
)

import { Line } from 'react-chartjs-2';
import { ThemeContext } from '@/context/ThemeProvider';
import {faker} from '@faker-js/faker'

const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
const fakeDataset = {
    labels:months,
    datasets:[
        {   
            data: months.map(() => faker.datatype.number({ min: 1000, max: 20000 })),
        },
    ],
};


const LineChart:React.FC<{
    width:string, height:string, isFakeData?:boolean
}> = ({width, height, isFakeData}) => {

    const {mode} = React.useContext(ThemeContext);


    const options = {
        plugins:{
            legend:{
                display:false
            },
        },
        elements:{
            line:{
                tension:.4,
                borderWidth:2,
                borderColor: `${mode === 'dark' ? 'rgba(255,255, 255, 1)' : 'rgba(0,0, 0, 1)' }`,
                fill:'start',
                backgroundColor:'transparent'
            },
            point:{
                radius:6,
                itRadius:1
            },
        },
        scales:{
            xAxis: {
                display: false,
            },
            yAxis: {
                display:false
            },
            x: {
                grid: {
                    // color: 'red'
                }
            }
        },
    };

    return (
        <Line 
            data={fakeDataset} 
            width={width} 
            height={height} 
            options={options} 
        />
    )
}

export default LineChart