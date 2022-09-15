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
    Filler
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
)

import { Line } from 'react-chartjs-2';
import { ThemeContext } from '@/context/ThemeProvider';


const LineChart = () => {
    const {mode} = React.useContext(ThemeContext)
    const data = {
        labels:['Jan', 'Feb', 'March', 'April', 'May', 'June','July', 'August', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets:[
            {
                data: [  8400, 8100, 11700, 9400, 10500, 13200, 10300, 16000, 13500, 12600, 17300 ]
            },
        ],
    };
    
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
                radius:0,
                itRadius:0
            },
        },
        scales:{
            xAxis: {
                display: false,
            },
            yAxis: {
                display:false
            },
        },
    }
    return (
        <Line data={data} width={'100%'} height={'30%'} options={options} />
    )
}

export default LineChart