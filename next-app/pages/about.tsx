import * as React from 'react';
import Head from 'next/head';
import { NextFunctionComponent } from 'next';
import Header from '../components/Header';

const About: NextFunctionComponent = () => {
    return (
  <React.Fragment>
    <Head>
      <title>About</title>
    </Head>
    <Header />
    <main>
  <h1>About</h1>
  <p>The Pliny Project is an attempt to make the people behind the letters of 
    Pliny the Younger accessible. Although there is considerable 
    distinguished print scholarship on the people of Pliny, 
    few if any online resources exist to facilitate a simple search 
    for Pliny's correspondents or their own biography when it is known. 
  </p>


  <p>    
    I collected a considerable amount of data from a thorough analysis of Pliny's letters under the auspices of a 
    fellowship at the American Academy in Rome. Subsequently I am now mining it 
    for conclusions, and attempting to make it available online for other
     scholars to use in their research, with the gracious support of research release time at the 
     <a href="https://cdh.princeton.edu">Center for Digital Humanities</a> at Princeton.
     </p>
     </main>
  </React.Fragment>
    )
}

export default About;