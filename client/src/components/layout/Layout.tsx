import * as React from 'react';
import Header from './Header';
import Footer from './Footer';
import clsx from 'clsx';

import { ThemeContext } from '@/context/ThemeProvider';

export default function Layout({ children }: { children: React.ReactNode }) {
  const { color, mode } = React.useContext(ThemeContext);

  return (
    <div
      className={clsx(mode === 'dark' ? 'bg-zinc-900' : 'bg-gray-50', color)}
    >
      <Header />
      <div
        className={clsx(
          'relative h-full',
          'min-h-[90vh] w-screen',
          'px-3 lg:px-0',
        )}
      >
        {children}
      </div>
      <Footer />
    </div>
  );
}
