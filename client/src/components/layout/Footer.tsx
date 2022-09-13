import React from 'react'
import UnderlineLink from '@/components/links/UnderlineLink';

const Footer = () => {
  return (
    <footer className='sticky bottom-2 z-50 text-gray-700 flex justify-center'>
        © {new Date().getFullYear()} {''}
        <UnderlineLink href='/' className='pl-1'>
            PersonalFinance
        </UnderlineLink>
    </footer>
  )
}

export default Footer


