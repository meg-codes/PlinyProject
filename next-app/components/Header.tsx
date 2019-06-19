import * as React from 'react';
import Router from 'next/router';

import ActiveLink from './ActiveLink';
import QuickSearch from './QuickSearch'

const Header:React.FC = () =>
<header className='header'>
  <div className='img-banner'>&nbsp;</div>
        <div className='site-header'>The Pliny Project</div>

        <nav class='main-nav' arial-label='main navigation'>
          <ul>
            <li><ActiveLink href='/'><a>Home</a></ActiveLink></li>
            <li><ActiveLink href='/about'><a>About</a></ActiveLink></li>
            <li><ActiveLink href='/viz'><a>Visualization</a></ActiveLink></li>
            <li><ActiveLink href='/people'><a>People</a></ActiveLink></li>
            <li className='form-holder'>
              <QuickSearch action='/people' id='quicksearch' name='nomina' placeholder='Enter nomima...'
              label='Search Correspondents' />
            </li>
          </ul>
        </nav>
</header>

export default Header