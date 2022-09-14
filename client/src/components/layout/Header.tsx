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
        <li key={`login`}>
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

const MobileNavDropDown = ()=>{
  return(
    <div className="group relative bg-blue-300 ">
      <Button 
        variant='light'
        className="hidden"
        /* className="hidden bg-gray-300 text-gray-700 
        font-semibold py-2 px-4 rounded inline-flex items-center" */
      >
        <span className="mr-1">Menu</span>
      </Button>
      <ul className="absolute hidden text-gray-700 pt-1 group-hover:block">
        {links.map(({ href, label }) => (
            <li key={`${href}${label}`}>
              <PrimaryLink href={href} className='rounded-b bg-gray-200 hover:bg-gray-400 py-2 px-4 flex flex-col justify-start whitespace-no-wrap '>
                {label}
              </PrimaryLink>
            </li>
          ))}
      </ul>
    </div>
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
          {/* <MobileNavDropDown/> */}
        </nav>
      </div>
    </header>
  );
}