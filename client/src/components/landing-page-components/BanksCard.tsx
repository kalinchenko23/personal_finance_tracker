import React from 'react'
import clsx from 'clsx';
import LineChart from '../charts/LineChart';
import Chip from '../Chip';

const BanksCard: React.FC = () => {
    return (
      <div className='mb-4 h-full w-full'>
        <div className='flex justify-between'>
          <h4 className={clsx('mx-1 font-mono font-semibold', 'md:text-xl')}>
            Banks:
          </h4>
          <div className='mb-4 inline-flex gap-1'>
            {banks.map((b) => (
              <Chip key={b} text={b} className={'py-[2px] px-1 text-sm'} />
            ))}
          </div>
        </div>
  
        <div
          className={clsx(
            'mb-4 h-1/5 w-full',
            'flex items-center justify-center',
            'relative overflow-hidden',
            'flex flex-col'
          )}
        >
          {/* add chart randomizer */}
          <div className='h-full w-full'>
            <LineChart width={'100%'} height={'100%'} />
          </div>
        </div>
      </div>
    );
  };
  const banks = ['Bank of America', 'Chase', 'Capital One'];
  

export default BanksCard