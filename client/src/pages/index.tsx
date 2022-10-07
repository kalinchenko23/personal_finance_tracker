import * as React from 'react';
import axios from 'axios';

import Layout from '@/components/layout/Layout';
import ArrowLink from '@/components/links/ArrowLink';
import ButtonLink from '@/components/links/ButtonLink';
import UnstyledLink from '@/components/links/UnstyledLink';
import Accent from '@/components/Accent';
import Seo from '@/components/Seo';

import { ThemeContext } from '@/context/ThemeProvider';
import LineChart from '@/components/charts/LineChart';
import { VscAccount } from 'react-icons/vsc';
import { AiOutlineLineChart } from 'react-icons/ai';
import Image from 'next/image';
import plaidSvg from '../assets/plaid.png';
import PieChart from '@/components/charts/PieChart';
/**
 * SVGR Support
 * Caveat: No React Props Type.
 *
 * You can override the next-env if the type is important to you
 * @see https://stackoverflow.com/questions/68103844/how-to-override-next-js-svg-module-declaration
 */

import Chip from '@/components/Chip';
import clsx from 'clsx';
import Button from '@/components/buttons/Button';

// !STARTERCONF -> Select !STARTERCONF and CMD + SHIFT + F
// Before you begin editing, follow all comments with `STARTERCONF`,
// to customize the default configuration.

export default function HomePage() {
  const { mode } = React.useContext(ThemeContext);
  const textColor = mode === 'dark' ? 'text-gray-300' : 'text-gray-800';
  const cardStyle =
    mode === 'dark'
      ? 'border-solid border border-primary-500 shadow-primary-500/40'
      : 'bg-white border-solid border border-gary-50';

  const [card, setCard] = React.useState<string>('Banks');

  return (
    <Layout>
      <Seo templateTitle='Home' />

      <main className={clsx('flex h-full w-full flex-col', textColor)}>
        <div
          className={clsx(
            'flex w-full flex-col items-center',
            'sm:flex-row',
            'p-4'
          )}
        >
          <section
            className={clsx(
              'h-full w-full ',
              'my-2 flex flex-col-reverse items-center',
              'md:items-start md:justify-center'
            )}
          >
            <div className={clsx()}>
              <h1
                className={clsx(
                  'text-4xl font-extrabold tracking-tight',
                  'sm:text-5xl md:text-3xl  xl:text-6xl'
                )}
              >
                Take{' '}
                <UnstyledLink href='#'>
                  <Accent>control</Accent>
                </UnstyledLink>{' '}
              </h1>
              <h1
                className={clsx(
                  'text-4xl font-extrabold tracking-tight',
                  'sm:text-5xl md:text-3xl  xl:text-6xl'
                )}
              >
                over your money
              </h1>
              <div className='my-5 h-[1px] w-full bg-gray-500' />
              <p className='mt-4 text-2xl'>
                <Accent> PersonalFinance </Accent> will help you organize your
                bank data
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
            className={clsx(
              'h-full w-full',
              'my-2 flex flex-col-reverse items-center',
              'sm:h-full sm:w-3/4 sm:flex-col '
            )}
          >
            <div
              className={clsx(
                'w-full  rounded-2xl p-4 shadow-2xl',
                'sm:h-4/5 sm:w-fit md:p-5',
                cardStyle
              )}
            >
              <div className='mb-2 flex flex-wrap'>
                {chipsList.map((el) => {
                  return (
                    <button onClick={() => setCard(el)}>
                      <Chip className='text-xl' key={el} text={el} />
                    </button>
                  );
                })}
              </div>

              <div className='my-2 h-[1px] w-full bg-gray-500' />
              <div className='min-h-80 h-full w-full'>
                {card === 'Banks' && <BanksCard />}
                {card === 'Expenses' && <ExpensesCard />}
              </div>
            </div>
          </section>
        </div>

        <section
          className={clsx(
            `bg-[url('../assets/blurry-gradient-haikei.svg')]`,
            `h-full w-screen text-gray-800`
          )}
        >
          <div className='flex h-full  w-full flex-col items-center p-8'>
            <h1 className=' my-8 text-4xl font-extrabold tracking-tight md:text-6xl'>
              Financial tools for your {'  '}
              <span
                className={clsx(
                  ['text-white'],
                  'text-4xl font-extrabold  tracking-tight md:text-6xl'
                )}
              >
                Goals
              </span>
            </h1>
            <div className='flex items-center'>
              <h2 className='mb-14 font-extrabold tracking-tight'>
                We visualize data provided by Plaid API
              </h2>
            </div>
          </div>
        </section>

        <section className=' h-screen w-screen text-gray-800'>
          <div className='mt-10 flex w-full justify-center'>
            <div
              className={clsx(
                'h-[10rem] w-[25rem]',
                'mx-2 py-3 px-2',
                'flex  flex-col items-center',
                'justify-center rounded-3xl bg-white shadow-xl'
              )}
            >
              <Image src={plaidSvg} width={'90%'} height={'90%'} className='' />
              <h3> Set up your Plaid Account </h3>
            </div>
            <div
              className={clsx(
                'h-[10rem] w-[25rem]',
                'mx-2 py-3 px-2',
                'flex  flex-col items-center',
                'justify-center rounded-3xl bg-white shadow-xl'
              )}
            >
              <VscAccount className='mb-2 text-5xl' />
              <h3> Sign Up </h3>
              <Accent className='text-3xl'> Personal Finance</Accent>
            </div>
            <div
              className={clsx(
                'h-[10rem] w-[25rem]',
                'mx-2 py-3 px-2',
                'flex  flex-col items-center',
                'justify-center rounded-3xl bg-white shadow-xl'
              )}
            >
              <AiOutlineLineChart className='mb-2 text-5xl' />
              <h3>Analyze your cash flow</h3>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}

const chipsList = ['Banks', 'Transactions', 'Income', 'Expenses', 'Credits'];

const BanksCard: React.FC = () => {
  return (
    <div className='mb-4 '>
      <h4 className='mx-1 font-mono text-xl font-semibold'>Banks:</h4>
      <div className='mb-4 flex'>
        {banks.map((b) => (
          <Chip key={b} text={b} />
        ))}
      </div>

      <div
        className={clsx(
          'mb-4 h-1/5 w-full',
          'flex items-center justify-center',
          'relative overflow-hidden'
        )}
      >
        {/* add chart randomizer */}
        <LineChart width={'100%'} height={'35%'} />
      </div>
    </div>
  );
};
const banks = ['Bank of America', 'Chase', 'Capital One'];

const ExpensesCard: React.FC = () => {
  return (
    <>
      <div
        className={clsx(
          'mb-4 h-1/5 w-full',
          'flex items-center justify-center',
          'relative overflow-hidden'
        )}
      >
        <div className='h-3/5 w-3/5'>
          <div className=' h-full rounded-xl border border-gray-400/40 p-3'>
            <h1 className='font-italic'> Dec 2022</h1>
            <div className='my-1 h-[1px] w-full bg-gray-400/40' />
            <h4 className='font-normal'>Monthly expenses</h4>
            <h4>
              cutted by <Accent className='font-mono'>12%</Accent>
            </h4>
            <div className='my-1 h-[1px] w-full bg-gray-400/40' />

            <h4 className='font-normal'>Biggest expense in</h4>
            <h4>
              <Accent className='font-mono'>Travel</Accent>
            </h4>

            <h4 className='font-normal'>Most often spendings</h4>
            <div className='flex justify-around'>
              <h4>
                <Accent>Shopping</Accent>
              </h4>
              <h4>
                <Accent red>Groceries</Accent>
              </h4>
              <h4>
                <Accent green>Gas</Accent>
              </h4>
            </div>
          </div>
        </div>
        <div className=' h-full w-3/5'>
          <PieChart radius={'100%'} />
        </div>
      </div>
    </>
  );
};
