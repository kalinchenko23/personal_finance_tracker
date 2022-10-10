import * as React from 'react';

import Layout from '@/components/layout/Layout';
import ArrowLink from '@/components/links/ArrowLink';
import ButtonLink from '@/components/links/ButtonLink';
import UnstyledLink from '@/components/links/UnstyledLink';
import Accent from '@/components/Accent';
import Seo from '@/components/Seo';

import BanksCard from '@/components/landing-page-components/BanksCard';
import ExpensesCard from '@/components/landing-page-components/ExpensesCard';
import StepCard from '@/components/landing-page-components/StepCard';

import { ThemeContext } from '@/context/ThemeProvider';
import { VscAccount } from 'react-icons/vsc';
import { AiOutlineLineChart } from 'react-icons/ai';

import plaidSvg from '../assets/plaid.png';
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
import { IconType } from 'react-icons';

// !STARTERCONF -> Select !STARTERCONF and CMD + SHIFT + F
// Before you begin editing, follow all comments with `STARTERCONF`,
// to customize the default configuration.

export default function HomePage() {
  const { mode } = React.useContext(ThemeContext);
  // const textColor = mode === 'dark' ? 'text-gray-300' : 'text-gray-800';
  const cardStyle =
    mode === 'dark'
      ? 'border-solid border border-primary-500 shadow-primary-500/30'
      : 'bg-white border-solid border border-gary-50';

  const [card, setCard] = React.useState<string>('Banks');

  return (
    <Layout>
      <Seo templateTitle='Home' />

      <main>
        <div
          className={clsx(
            'flex flex-col items-center',
            'md:flex-row',
            'py-8',
            'px-2',
            'md:px-4',
            'lg:px-8'
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
                  'sm:text-6xl md:text-5xl  xl:text-6xl'
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
                  'sm:text-6xl md:text-5xl  xl:text-6xl'
                )}
              >
                over your money
              </h1>
              <div
                className={clsx(
                  'my-5 h-[2px] w-4/5 rounded',
                  mode === 'light' ? 'bg-gray-700' : 'bg-gray-300'
                )}
              />
              <p className='mt-4 text-2xl'>
                <Accent> PersonalFinance </Accent> will help you organize your
                bank data
              </p>
              <div className='mt-6'>
                <ArrowLink
                  as={ButtonLink}
                  variant={mode === 'light' ? 'dark' : 'light'}
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
              'h-full w-3/4',
              'my-2 flex flex-col-reverse items-center',
              'sm:h-full sm:w-3/4 sm:flex-col'
            )}
          >
            <div
              className={clsx(
                'w-3/4  rounded-md shadow-2xl',
                'sm:h-4/5 sm:w-fit',
                cardStyle
              )}
            >
              <div className={clsx('mb-2 flex', 'px-2 sm:py-2')}>
                {chipsList.map((text) => {
                  return (
                    <Button
                      variant={mode === 'light' ? 'dark' : 'light'}
                      className={clsx('m-[2px] py-[2px] px-2 text-sm')}
                      onClick={() => setCard(text)}
                    >
                      {text}
                    </Button>
                  );
                })}
              </div>

              <div className='my-2 h-[1px] w-full bg-gray-500' />
              <div className='min-h-80 h-full w-full px-4'>
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
          <div
            className={clsx(
              'flex h-full  w-screen flex-col items-center',
              'px-2 py-2',
              'sm:px-4 sm:py-4',
              'md:px-6 md:py-6',
              'lg:px-8 lg:py-8'
            )}
          >
            <h1
              className={clsx(
                'font-extrabold tracking-tight',
                'my-8',
                'text-4xl',
                'md:text-5xl',
                'text-center'
              )}
            >
              Financial tools for your {'  '}
              <span
                className={clsx(
                  'text-white',
                  'text-4xl font-extrabold  tracking-tight md:text-6xl'
                )}
              >
                Goals
              </span>
            </h1>
            <h2
              className={clsx(
                'font-extrabold tracking-tight',
                'text-center',
                'text-2xl',
                'lg:text-3xl'
              )}
            >
              We visualize data provided by Plaid API
            </h2>
          </div>
        </section>

        <section className=' h-full w-screen'>
          <div
            className={clsx(
              'flex flex-col',
              'mt-10 w-full',
              'justify-between',
              'items-center'
            )}
          >
            <div
              className={clsx('m-2', 'flex justify-between', 'max-w-screen-lg group')}
            >
              <StepCard
                text1={'Set Up'}
                text2={'Your Plaid Account '}
                imageSrc={plaidSvg}
                className={clsx()}
              />
              <p
                className={clsx(
                  'h-48 w-3/5 ',
                  'p-2 text-xl font-semibold',
                )}
              >
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                eiusmod tempor incididunt ut labore et dolore magna aliqua.
              </p>
            </div>
            <div
              className={clsx('m-2', 'flex justify-between', 'max-w-screen-lg group')}
            >
              <StepCard
                text1={'Sign Up'}
                text2={'PersonalFinance'}
                icon={<VscAccount />}
                className={clsx()}
              />
              <p
                className={clsx(
                  'h-48 w-3/5 ',
                  'p-2 text-xl font-semibold',
                )}
              >
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                eiusmod tempor incididunt ut labore et dolore magna aliqua.
              </p>
            </div>
            <div
              className={clsx('m-2', 'flex justify-between', 'max-w-screen-lg group')}
            >
              <StepCard
                text1={'Analyze'}
                text2={'Your cash flow'}
                icon={<AiOutlineLineChart />}
                className={clsx()}
              />
              <p
                className={clsx(
                  'h-48 w-3/5 ',
                  'p-2 text-xl font-semibold',
                )}
              >
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                eiusmod tempor incididunt ut labore et dolore magna aliqua.
              </p>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}



const chipsList = ['Banks', 'Transactions', 'Income', 'Expenses', 'Credits'];




