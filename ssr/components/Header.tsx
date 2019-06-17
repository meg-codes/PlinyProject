import * as React from 'react';

import ActiveLink from './ActiveLink';

const Header:React.FC = () =>
<div className='header'>
  <div className='img-banner'>&nbsp;</div>
        <div className='site-header'>The Pliny Project</div>
        
        <nav>
          <ul>
            <li><ActiveLink href='/'><a>Home</a></ActiveLink></li>
            <li><ActiveLink href='/about'><a>About</a></ActiveLink></li>
            <li><ActiveLink href='/viz'><a>Visualization</a></ActiveLink></li>
            <li><ActiveLink href='/prosopography/'><a>Prosopography</a></ActiveLink></li>
            <li className='form-holder'>
              <form action='/prosopography' onSubmit={
                e => {
                  e.preventDefault();

                }
              }>
                <label htmlFor='quicksearch'>Search Correspondents</label>
                <input type='text' id='quicksearch' name='nomina' placeholder='Enter a nomina...'></input>
              </form>
           </li>
          </ul>
        </nav>
</div>

export default Header