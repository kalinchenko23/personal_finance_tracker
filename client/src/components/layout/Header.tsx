import * as React from 'react';
import LoginForm from '@/components/LoginForm';
import clsx from 'clsx';
import {FaMoon, FaSun} from "react-icons/fa";

import UnstyledLink from '@/components/links/UnstyledLink';
import PrimaryLink from '@/components/links/PrimaryLink'
import Logo from '@/components/Logo';
import Button from '../buttons/Button';
import { ThemeContext } from '@/context/ThemeProvider';


const DesktopNav:React.FC<{
  mode:'light'|'dark'
  // toggleMode:()=>void
  setMode:React.Dispatch<React.SetStateAction<"dark" | "light">>
  setOpenLogin:React.Dispatch<React.SetStateAction<boolean>>
}> = ({mode, setMode, setOpenLogin})=>{
  return (
    <ul className='hidden items-center justify-between space-x-4  lg:flex '>
      {links.map(({ href, label }) => (
        <li key={`${href}${label}`}>
          <UnstyledLink href={href} className=''>
            {label}
          </UnstyledLink>
        </li>
      ))}
        <li key={`login`}>
          <Button 
            className='rounded-lg'
            variant={mode === 'dark' ? 'light' : 'dark'}
            onClick={()=>setOpenLogin(true)}
          >Login
          </Button>
        </li>
        <li key={`theme`}>
          <Button 
              variant={mode === 'dark' ? 'light' : 'dark'}
              className='rounded-lg text-2xl' 
              onClick={()=>setMode( mode === 'light' ? 'dark': 'light' )}
            >{mode === 'light' ? <FaMoon/> : <FaSun/>}
            </Button>
        </li>
    </ul>
  )
};

const MobileNav:React.FC<{
  mode:'light'|'dark'
  // toggleMode:()=>void
  setMode:React.Dispatch<React.SetStateAction<"dark" | "light">>
  setOpenLogin:React.Dispatch<React.SetStateAction<boolean>>
}> = ({mode, setMode, setOpenLogin})=>{
  return(
    <nav className='lg:hidden flex'>
      <Button 
        className='mx-2 mt-2 text-lg'
        variant={mode === 'dark' ? 'light' : 'dark'}
        onClick={()=>setOpenLogin(true)}
      >
        Login
      </Button>
      <Button 
        className='mx-1 mt-2 text-lg'
        variant={mode === 'dark' ? 'light' : 'dark'}
        onClick={()=>{
          setMode( mode === 'light' ? 'dark': 'light' )
          setOpenLogin(false)
        }}
      >
        {mode === 'light' ? <FaMoon/> : <FaSun/>}
      </Button>
    </nav>
  )
};



const links = [
  { href: '/', label: 'Home' },
  { href: '/', label: 'About' },
];

export default function Header() {
  const { mode, setMode} = React.useContext(ThemeContext);
  // const textColor = mode === 'dark' ? 'text-gray-300' : 'text-gray-900';
  const [openLogin, setOpenLogin] = React.useState(false);
  return (
    <header className={clsx('h-24 top-0 z-50 flex', mode === 'dark' ? 'text-white' : 'text-black' )}>

      <LoginForm openLogin={openLogin} setOpenLogin={setOpenLogin}/>

      <div className='layout flex pt-2 h-14 content-center justify-between'>
        <Logo withText={true} mode={mode}/> 
        <nav className='mt-2'>
          <DesktopNav mode={mode} setMode={setMode} setOpenLogin={setOpenLogin}/>
          <MobileNav mode={mode} setMode={setMode} setOpenLogin={setOpenLogin}/>
        </nav>
      </div>
    </header>
  );
}