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
  
        <section className='h-3/4 w-80 p-1 relative flex  bg-white rounded flex-col justify-top items-center'>
          <button 
            className='absolute right-4 top-2 font-bold text-2xl' 
            onClick={()=>setOpenLogin(false)}
          >X
          </button>
  
          <p className='mt-4'>Sign in to</p>
          <Logo/>
          <div className='flex w-full justify-center mt-4'>
            <Button variant='light' className='w-2/4 flex justify-center' onClick={()=> setToggle(true) }>Sign In</Button>
            <Button variant='light' className='w-2/4 flex justify-center' onClick={()=> setToggle(false) }>Sign Up</Button>
          </div>
  
          <form className={`w-full p-2 flex flex-col  ${toggle === false ? 'block' : 'hidden'}`}>
            <h2>Sign Up</h2>
            <label className='flex-col'>
                Enter username:
            </label>
            <input type='text' name='user_name' className='text-dark'/>
  
            <label className='flex-col'>
                Enter your first name:
            </label>
            <input type='text' name='first_name' className='text-dark'/>
  
            <label className='flex-col'>
                Enter your last name:
            </label>
                <input type='text' name='last_name' className='text-dark'/>
  
            <label className='flex-col'>
                Enter password:
            </label>
            <input type='password' name='password' className='text-dark'/>
            <Button variant='light' type='submit' className='flex justify-center mt-2'>Submit</Button>
          </form>
  
          <form className={`w-full p-2 flex flex-col  ${toggle === true ? 'block' : 'hidden'}`}>
            <h2>Sign In</h2>
            <label className='flex-col'> Enter username:</label>
            <input type='text' name='username' className='text-dark'/>
  
            <label className='flex-col'> Enter password: </label>
            <input type='password' name='password' className='text-dark'/>
            <Button variant='light' type='submit' className='flex justify-center mt-2'>Submit</Button>
          </form>
        </section>
      </div>
    )
};

export default LoginForm