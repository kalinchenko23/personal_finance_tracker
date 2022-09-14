import React from 'react';


const Chip = ({text}:{text:string}) => {
  return (
    <div className='bg-gray-100 border border-slate-400 px-3 py-1 m-1 rounded-xl text-gray-800
    font-semibold tracking-wider
    transition duration-150 ease-out hover:ease-in
    hover:bg-gradient-to-tr from-primary-900 via-primary-600 to-primary-500 hover:border-transparent
    hover:text-white cursor-pointer'>{text}</div>
  )
}

export default Chip