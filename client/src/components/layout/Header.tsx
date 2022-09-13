import * as React from 'react';
import LoginForm from '@/components/LoginForm';

import UnstyledLink from '@/components/links/UnstyledLink';
import Logo from '@/components/Logo';
import Button from '../buttons/Button';

const DesktopNav = ({setOpenLogin}:{setOpenLogin:React.Dispatch<React.SetStateAction<boolean>>})=>{
  return (
    <ul className='hidden items-center justify-between space-x-4  lg:flex'>
      {links.map(({ href, label }) => (
        <li key={`${href}${label}`}>
          <UnstyledLink href={href} className='hover:text-gray-600'>
            {label}
          </UnstyledLink>
        </li>
      ))}
        <li key={`login`}>
          <Button variant='light' onClick={()=>setOpenLogin(true)}>Login</Button>
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
              <UnstyledLink href={href} className='rounded-b bg-gray-200 hover:bg-gray-400 py-2 px-4 flex flex-col justify-start whitespace-no-wrap '>
                {label}
              </UnstyledLink>
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

  const [openLogin, setOpenLogin] = React.useState(false);
  return (
    <header className='sticky h-20 top-0 z-50 bg-white shadow-lg'>

      <LoginForm openLogin={openLogin} setOpenLogin={setOpenLogin}/>

      <div className='layout flex pt-2 h-14 content-center justify-between'>
        <Logo/> 
        
        <nav className='mt-2  '>
          <DesktopNav setOpenLogin={setOpenLogin}/>
          <Button 
            variant='light' 
            className='lg:hidden' 
            onClick={()=>setOpenLogin(true)}
          >
            Login
          </Button>
          {/* <MobileNavDropDown/> */}
        </nav>
      </div>
    </header>
  );
}