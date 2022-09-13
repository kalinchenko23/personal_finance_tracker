import * as React from 'react';
import Header from './Header';
import Footer from './Footer';
import clsx from 'clsx';
import Vercel from '~/svg/Vercel.svg';

import {ThemeContext} from '@/context/ThemeProvider'

export default function Layout({ children }: { children: React.ReactNode }) {
  const {color, mode} = React.useContext(ThemeContext)

  return (
    <div className={clsx(
      'h-full relative', mode === 'dark' ? 'bg-dark' : 'bg-gray-50', color
    )}>
      <Header/>
      {children}
      <Footer/>
    </div>
  )
}
