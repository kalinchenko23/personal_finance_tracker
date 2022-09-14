import React from 'react'
import Logo from '@/components/Logo';
import Button from '@/components/buttons/Button';


const LoginForm = ({
    openLogin, 
    setOpenLogin
  }:{
    openLogin:boolean, 
    setOpenLogin:React.Dispatch<React.SetStateAction<boolean>>
  }) => {
  
    const [toggle, setToggle] = React.useState(false)
  
    return (
      <div className={`absolute h-screen w-screen flex justify-center items-center z-50 bg-dark/75 transition duration-500 ease-out ${openLogin ? 'block' : 'hidden '}`}>
  
        <section className='h-3/4 w-full lg:w-96  p-2 
        relative flex shadow-lg shadow-dark/40 bg-white 
        rounded-md flex-col justify-top items-center'
        >
            <button 
                className='absolute right-4 top-2 font-bold text-2xl text-zinc-900' 
                onClick={()=>setOpenLogin(false)}
            >X
            </button>
  
            <p className='mt-4 font-semibold text-lg'>
                Sign in to
            </p>
            <Logo/>

            <div className='flex w-full justify-center mt-4'>
                <Button variant='light' className='w-2/4 flex justify-center shadow-md shawod-slate-800' onClick={()=> setToggle(true) }>Sign In</Button>
                <Button variant='light' className='w-2/4 flex justify-center shadow-md shawod-slate-800' onClick={()=> setToggle(false) }>Sign Up</Button>
            </div>
  
            <form className={`w-full p-2 flex flex-col  ${toggle === false ? 'block' : 'hidden'}`}>
                <h2 className='mt-2 mb-2'>Sign Up</h2>
                <label className='flex-col font-semibold text-lg text-zinc-700'>
                    Enter username:
                </label>
                <input type='text' name='user_name' className='text-dark rounded border-gray-300 shadow-md shawod-slate-800 mb-1'/>
    
                <label className='flex-col font-semibold text-lg text-zinc-700'>
                    Enter your first name:
                </label>
                <input type='text' name='first_name' className='text-dark rounded border-gray-300 shadow-md shawod-slate-800 mb-1'/>
    
                <label className='flex-col font-semibold text-lg text-zinc-700'>
                    Enter your last name:
                </label>
                    <input type='text' name='last_name' className='text-dark rounded border-gray-300 shadow-md shawod-slate-800 mb-1'/>
    
                <label className='flex-col font-semibold text-lg text-zinc-700'>
                    Enter password:
                </label>
                <input type='password' name='password' className='text-dark rounded border-gray-300 shadow-md shawod-slate-800 mb-1'/>
                <Button variant='dark' type='submit' className='flex justify-center mt-2 shadow-md shawod-slate-800'>Submit</Button>
            </form>
  
            <form className={`w-full p-2 flex flex-col  ${toggle === true ? 'block' : 'hidden'}`}>
                <h2 className='mt-2 mb-2'>Sign In</h2>
                <label className='flex-col font-semibold text-lg text-zinc-700'> Enter username:</label>
                <input type='text' name='username' className='text-dark rounded border-gray-300 shadow-md shawod-slate-800 mb-1'/>
    
                <label className='flex-col font-semibold text-lg text-zinc-700'> Enter password: </label>
                <input type='password' name='password' className='text-dark rounded border-gray-300 shadow-md shawod-slate-800 mb-1'/>
                <Button variant='dark' type='submit' className='flex justify-center mt-2 shadow-md shawod-slate-800'>Submit</Button>
            </form>
        </section>
      </div>
    )
};

export default LoginForm