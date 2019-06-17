import * as React from 'react';
import Header from '../components/Header';
import ForceGraph from '../components/ForceGraph'

export default class Viz extends React.Component {

  width = 800
  height = 800

  render() {
    return (
      <div>
        <Header />
        <main>
        <h1>Visualizations</h1>
        <h2>Force-Directed Network Graph</h2>
        <ForceGraph id="pliny-graph" width={500} height={500} 
          title="Force-Directed Graph of Pliny's Correspondents"/>
        </main>
      </div>
    )
  }

}