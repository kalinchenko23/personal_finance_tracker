import React from 'react';
import Logo from '@/components/Logo'




const LoginPage = () => {
  return (
    <div className='flex'>
        <section className='h-screen w-[50%] bg-slate-400 flex justify-center items-center'>
            <Logo/>
        </section>
        <section className='h-screen w-[50%] bg-slate-800 flex justify-center items-center'>
            
            <form className='flex flex-col text-white bg-slate-600'>
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
                <button type='submit'>Submit</button>
            </form>

            <form className='flex flex-col text-white bg-slate-600'>
                <h2>Log In</h2>
                <label className='flex-col'> Enter username:</label>
                <input type='text' name='username' className='text-dark'/>

                <label className='flex-col'> Enter password: </label>
                <input type='password' name='password' className='text-dark'/>
                <button type='submit'>Submit</button>
            </form>
        </section>
    </div>
  )
};

export default LoginPage;