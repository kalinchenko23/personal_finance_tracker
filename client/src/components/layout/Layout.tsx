import * as React from 'react';
import Header from './Header';
import Footer from './Footer';


export default function Layout({ children }: { children: React.ReactNode }) {

return <div className='h-full relative'>
    <Header/>
    {children}
    <Footer/>
  </div>;
}
