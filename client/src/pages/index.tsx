import * as React from 'react';


import Layout from '@/components/layout/Layout';
import ArrowLink from '@/components/links/ArrowLink';
import ButtonLink from '@/components/links/ButtonLink';
import UnstyledLink from '@/components/links/UnstyledLink';
import Accent from '@/components/Accent';
import Seo from '@/components/Seo';

import { ThemeContext } from '@/context/ThemeProvider';

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
const bakns = ['Bank of America', 'Chase', 'Capital One', 'JPMorgan']

const ChartUp:React.FC<{
  mode?:'light'|'dark'
}>= ({mode}) => {
  // const svgColor = mode === 'dark' ? 'stroke-gray-300' : 'stroke-gray-900';
  return (
    <svg width={900} height={400} className={'stroke-primary-600 '}>
      <path
        // stroke="#000000"
        strokeWidth={3.5}
        fill="none"
        strokeLinecap="round"
        strokeLinejoin="round"
        d="m0 400 7.5-17.55 7.5-55.26 7.5-23.194 7.5 9.663 7.5 17.664 7.5-.813 7.5 7.364 7.5 3.151 7.5-15.11L75 304.7l7.5-63.575 7.5-3.318 7.5-2.658 7.5-15.088 7.5-25.952 7.5 39.553 7.5 1.406 7.5-25.116 7.5-14.324 7.5 13.658 7.5 13.508 7.5 36.355 7.5 28.291 7.5-30.07 7.5 5.302 7.5 5.002 7.5 5.406 7.5-5.847 7.5 2.437 7.5 47.642 7.5.552 7.5 20.191 7.5 38.876 7.5-11.345 7.5-40.508 7.5 25.01 7.5-9.31 7.5-17.621 7.5 37.834 7.5-46.46 7.5-8.115 7.5-1.741 7.5-22.328 7.5 8.185 7.5 33.263 7.5.889 7.5 13.38 7.5 3.497 7.5 24.955 7.5-8.528 7.5-10.297 7.5 13.046 7.5 19.849 7.5 13.786 7.5-17.853 7.5-11.323 7.5-1.765 7.5-48.16 7.5 15.619 7.5-11.572 7.5 3.145 7.5-15.846 7.5-17.447 7.5 6.209 7.5-16.289 7.5-7.017 7.5-10.32 7.5-23.128 7.5-39.595 7.5 13.487 7.5-9.33 7.5 9.091 7.5-16.65 7.5 3.866 7.5-14.146 7.5-20.446 7.5-22.522 7.5 5.886 7.5-10.191 7.5 2.145 7.5 21.565 7.5 12.526 7.5-19.205 7.5 13.2 7.5-35.033 7.5-1.018 7.5-20.595 7.5.325 7.5-41.952 7.5-41.361 7.5 13.677L690 79.45l7.5 69.133 7.5 1.506 7.5-38.596 7.5-17.642 7.5-.644 7.5-6.577 7.5-21.332 7.5-9.469 7.5-6.068 7.5-2.109 7.5-2.028 7.5 6.805 7.5 25.212 7.5-25.638 7.5 16.552L810 51.91l7.5-31.98 7.5-3.234L832.5 0l7.5 1.739 7.5 7.388 7.5 29.71 7.5 25.228 7.5 3.99 7.5 1.708 7.5-18.517 7.5 9.177 7.5 9.093"
      />
    </svg>
  )
};

export default function HomePage() {
  const { mode } = React.useContext(ThemeContext);
  const textColor = mode === 'dark' ? 'text-gray-300' : 'text-gray-900';


  return (
    <Layout>
      <Seo templateTitle='Home' />
      
      <main className={clsx('w-full h-full flex flex-col sm:flex-row', textColor)}>
        <section className='h-3/5 sm:w-2/4 sm:h-[80vh] p-6 flex justify-center items-center'>
          <div className='lg:pl-16'>
            <h1 className='text-3xl font-extrabold tracking-tight  sm:text-5xl xl:text-6xl'>
              Take {' '}
              <UnstyledLink href='#'>
              <Accent>control</Accent>
              </UnstyledLink>{' '}
              over your money.
            </h1>
            <p className='mt-4 text-xl text-gray-600'>
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
        <section className='h-full sm:w-2/4 sm:h-[80vh] p-6 '>
          <h4>Banks:</h4>
          <div className='flex'>
            {bakns.map(b=><span className='font-semibold mx-1'>{b}</span>)}
          </div>
          
          <h4>Total balance:</h4>
          <span className='font-semibold mx-1'>$17 300</span>
          <div className='overflow-hidden'>
            
            {/* add chart randomizer */}
            <ChartUp/>
          </div>
          <div className='flex flex-wrap'>
            {chipsList.map(el=> <Chip text={el}/>)}
          </div>

        </section>
      </main>

    </Layout>
  );
}
