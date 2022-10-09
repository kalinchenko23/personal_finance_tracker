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
);

// import { Chart } from 'react-chartjs-2';
import { Line } from 'react-chartjs-2';
import { ThemeContext } from '@/context/ThemeProvider';
import {faker} from '@faker-js/faker'
import type { ChartData, ChartArea, ScriptableContext } from 'chart.js';

const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
const colors = [
    'red',
    'orange',
    'yellow',
    'lime',
    'green',
    'teal',
    'blue',
    'purple',
];

// export const data = {
//     months,
//     datasets: [
//       {
//         label: 'Dataset 1',
//         data: months.map(() => faker.datatype.number({ min: 1000, max: 20000 })),
//       },
//       {
//         label: 'Dataset 2',
//         data: months.map(() => faker.datatype.number({ min: 1000, max: 20000 })),
//       },
//     ],
//   };


const data = () => {
    return {
      labels: months,
      datasets: [{
        // label: "First dataset",
        data: months.map(() => faker.datatype.number({ min: 1000, max: 20000 })),
        fill: "start",
        backgroundColor: ({chart:{ctx}}: ScriptableContext<"line">) => {
          const gradient = ctx.createLinearGradient(0, 0, 0, 200);
          gradient.addColorStop(0, "#fde047");
          gradient.addColorStop(1, "#f97316");
          return gradient;
        },
        borderColor: "transparent"
      }]
    };
};



const LineChart:React.FC<{
    width:string, height:string, isFakeData?:boolean
}> = ({width, height, isFakeData}) => {

    const {mode} = React.useContext(ThemeContext);

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins:{
            legend:{
                display:false
            },
        },
        elements:{
            line:{
                tension:.4,
                borderWidth:7,
                borderColor: `${'rgba(250,0,0, 0)'}`,
                fill:'start',
                backgroundColor:'transparent'
            },
            point:{
                radius:0,
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
                    color: 'transparent'
                }
            }
        },
    };

    return (
        <Line 
            data={data()} 
            width={width} 
            height={height} 
            options={options} 
        />
    )
};

export default LineChart;