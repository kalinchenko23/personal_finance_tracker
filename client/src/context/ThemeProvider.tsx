import React from 'react'



type Color = typeof colorList[number];


export const ThemeContext = React.createContext<{
    color:Color,
    mode:'dark' | 'light';
    // toggleMode:()=>void
    setMode:React.Dispatch<any>
}>({
    color:'sky',
    mode:'light',
    // toggleMode:()=>{}
    setMode:()=>{}
});

const ThemeProvider:React.FC<{children:JSX.Element}>=  ({children}) => {
    const [mode, setMode] = React.useState<'dark' | 'light'>('light');
    const [color, setColor] = React.useState<Color>('sky');

    function toggleMode() {
        return mode === 'dark' ? setMode('light') : setMode('dark');
    }
    return (
        <ThemeContext.Provider value={{
            color, 
            mode, 
            setMode
        }}>
            {children}
        </ThemeContext.Provider>
    )
}

export default ThemeProvider;



export const colorList = [
    'rose',
    'pink',
    'fuchsia',
    'purple',
    'violet',
    'indigo',
    'blue',
    'sky',
    'cyan',
    'teal',
    'emerald',
    'green',
    'lime',
    'yellow',
    'amber',
    'orange',
    'red',
    'slate',
    'gray',
    'zinc',
    'neutral',
    'stone',
  ] as const;
  