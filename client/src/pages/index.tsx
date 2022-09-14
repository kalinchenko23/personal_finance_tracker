import * as React from 'react';


import Layout from '@/components/layout/Layout';
import ArrowLink from '@/components/links/ArrowLink';
import ButtonLink from '@/components/links/ButtonLink';
import UnstyledLink from '@/components/links/UnstyledLink';
import Accent from '@/components/Accent';
import Seo from '@/components/Seo';
import Image from "next/image"

import { ThemeContext } from '@/context/ThemeProvider';
import LineChart from '@/components/charts/LineChart';
import CapitalOne from '@/assets/CO.png'
/**
 * SVGR Support
 * Caveat: No React Props Type.
 *
 * You can override the next-env if the type is important to you
 * @see https://stackoverflow.com/questions/68103844/how-to-override-next-js-svg-module-declaration
 */

import Chip from '@/components/Chip';
import clsx from 'clsx';

// !STARTERCONF -> Select !STARTERCONF and CMD + SHIFT + F
// Before you begin editing, follow all comments with `STARTERCONF`,
// to customize the default configuration.

const chipsList = ['banks', 'transactions', 'expenses', 'loans', 'charts', 'insights']
const bakns = ['Bank of America', 'Chase', 'Capital One']

const ChartUp:React.FC<{
  mode?:'light'|'dark'
}>= ({mode}) => {

  return  <svg width={450} height={200} className='stroke-primary-600'>
    <path
      strokeWidth={1.5}
      fill="none"
      strokeLinecap="round"
      strokeLinejoin="round"
      d="m0 200 3.75-7.608 3.75 3.164 3.75 3.974 3.75-9.669 3.75.014 3.75-6.438 3.75 14.915L30 181.275l3.75 14.284 3.75-1.372 3.75-2.764L45 183.38l3.75.33 3.75.782 3.75 8.7 3.75 5.69 3.75-13.668 3.75 11.725 3.75.634L75 198.77l3.75-.794 3.75.562 3.75-13.137L90 163.8l3.75 9.09 3.75-.908 3.75-12.825 3.75 4.961 3.75 3.554 3.75 12.496 3.75 16.5 3.75-2.095 3.75-6.204 3.75-22.43 3.75 13.26 3.75-32.288 3.75-2.522 3.75-12.33 3.75 2.761 3.75 4.795 3.75 6.664 3.75 14.869 3.75-21.775 3.75-16.981 3.75.287 3.75 10.723 3.75 24.765 3.75 3.597 3.75 19.46 3.75 9.966 3.75 3.879 3.75 1.782 3.75-5.529 3.75-8.785 3.75-18.651 3.75 6.973 3.75-4.708 3.75-16.304 3.75-.693 3.75 2.954 3.75-6.289 3.75 7.105 3.75-23.823 3.75-3.236 3.75-7.188 3.75-17.5 3.75-21.261 3.75-9.947 3.75 12.91 3.75 2.155 3.75.815 3.75 23.683 3.75 3.996 3.75-10.802 3.75.525L285 90.473l3.75 18.917 3.75 18.934 3.75 10.904 3.75-9.438 3.75-9.301 3.75-28.702 3.75-20.749 3.75 5.646 3.75 7.437 3.75-7.868 3.75-10.358 3.75 8.528 3.75-19.682 3.75-4.658 3.75 20.31 3.75-7.769 3.75 11.643 3.75 18.846 3.75-.314 3.75-5.016 3.75 28.808 3.75-1.539 3.75-12.7 3.75 9.952 3.75-15.221 3.75-14.979 3.75 11.605 3.75-5.024 3.75 3.44 3.75 2 3.75-6.371 3.75 7.275 3.75 4.519 3.75-27 3.75-20.236 3.75-4.31 3.75-10.553 3.75-8.205 3.75-15.99L435 21.86l3.75 7.177 3.75-4.046 3.75-6.478L450 0"
    />
  </svg>


  return <svg width={250} height={250}className='stroke-primary-600'>
    <path
      strokeWidth={2}
      fill="none"
      strokeLinecap="round"
      strokeLinejoin="round"
      d="m0 200 2.083-.101 2.084-1.162 2.083-18.784 2.083-5.535 2.084-3.093 2.083 6.907 2.083-2.19 2.084-2.117 2.083-1.174 2.083-4.375 2.084-4.677L25 139.035l2.083-3.214 2.084.266 2.083 22.342 2.083 17.336 2.084-14.697 2.083-4.19 2.083-2.886 2.084 25.238 2.083-.089 2.083 13.284 2.084 3.772L50 179.652l2.083 6.039 2.084-3.026 2.083-6.428 2.083 5.892 2.084-2.651 2.083 5.442 2.083 9.676 2.084-9.104 2.083-1.825 2.083-17.191 2.084-13.77L75 122.551l2.083 12.135 2.084-9.34 2.083 15.09 2.083-17.05 2.084-.168 2.083 26.228 2.083-.468 2.084.374 2.083 6.87 2.083 5.935 2.084-3.532L100 143.333l2.083-6.094 2.084 4.748 2.083 7.578 2.083-16.945 2.084-2.838 2.083-16.856 2.083-13.191 2.084-8.498 2.083 23.587 2.083-16.856 2.084-16.255L125 70.96l2.083 10.704 2.084-2.193 2.083 17.226 2.083 1.788 2.084 3.116L137.5 70.16l2.083-7.688 2.084 2.318 2.083-1.209 2.083-2.38 2.084 4.61L150 67.694l2.083 7.861 2.084 16.635 2.083-6.23 2.083-4.79 2.084 14.4 2.083-21.836 2.083-10.283 2.084-14.638 2.083-4.744 2.083-12.42 2.084-.955L175 25.739l2.083-6.185 2.084 31.472 2.083 24.098 2.083 10.118 2.084-1.806 2.083-8.25 2.083 8.104 2.084-4.827 2.083-12.022 2.083 7.28 2.084 13.582L200 64.466l2.083 17.555 2.084-15.005 2.083 9.318 2.083-1.568 2.084-27.344L212.5 69.15l2.083-11.922 2.084-9.558 2.083 3.375 2.083-.679 2.084 7.2L225 39.507l2.083-11.204 2.084-3.67 2.083.431 2.083 4.32 2.084 10.125 2.083 1.904 2.083-17.853 2.084-7.098 2.083 21.432 2.083-17.172 2.084-12.058L250 0"
    />
  </svg>
};

export default function HomePage() {
  const { mode } = React.useContext(ThemeContext);
  const textColor = mode === 'dark' ? 'text-gray-300' : 'text-gray-900';




  return (
    <Layout>
      <Seo templateTitle='Home' />
      
      <main className={clsx('w-full h-full flex flex-col', textColor)}>

        <div className={clsx('w-screen h-[75vh] flex flex-col sm:flex-row px-4')} >
          <section className='h-3/5 sm:w-2/4 sm:h-[80vh] flex justify-center items-center p-4'>
            <div className='lg:pl-16'>
              <h1 className='text-3xl font-extrabold tracking-tight  sm:text-5xl xl:text-6xl'>
                Take {' '}
                <UnstyledLink href='#'>
                <Accent>control</Accent>
                </UnstyledLink>{' '}
                over your money.
              </h1>
              <p className='mt-4 text-2xl'>
                <Accent>PersonalFinance</Accent> will help you organize your bank data.
              </p>
              <div className='mt-6'>
                <ArrowLink
                  as={ButtonLink}
                  variant='light'
                  className='inline-flex items-center'
                  href='#'
                >
                  How it works
                </ArrowLink>
              </div>
            </div>
          </section>
          
          <section 
            className='sm:w-3/4 sm:h-full p-6'
          >
            <div
              className='sm:w-full sm:h-4/5s p-6 
              border-solid border rounded-2xl border-primary-500
              shadow-2xl shadow-primary-500/40'
            >
              <h4>Banks:</h4>
              
              <div className='flex'>
                {bakns.map((b)=><Chip key={b} text={b}/>)}
              </div>
              
              <h4>Total balance:</h4>
              <span className='font-semibold font-mono text-2xl mx-1'>$17 300</span>
              <div className='overflow-hidden mb-2' >
                {/* add chart randomizer */}
                <LineChart/>
              </div>
              <div className='flex flex-wrap'>
                {chipsList.map(el=> <Chip key={el} text={el}/>)}
              </div>
            </div>
          </section>


        </div>


        <section className="bg-[url('../assets/blurry-gradient-haikei.svg')] w-screen h-screen">
          

        </section>
      </main>
    </Layout>
  );
}
