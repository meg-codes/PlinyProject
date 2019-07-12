import * as React from 'react';
import Header from '../components/Header';
import ForceGraph from '../components/ForceGraph';
import ClassDoughnut from '../components/ClassDoughnut';

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
        <p>The follow graph shows the closeness of the various correspondents with Pliny,
          using number of letters written and times referenced in a letter to force weight 
          connections.
        </p>
        <p>Screenreader or keyboard users may use the <code>tab</code> key to enter the 
        graphic and then the up and down arrows to select nodes with their relative weighting.
        Sighted users may hover over a node to see their nomina.</p>
        <ForceGraph id="pliny-graph" width={500} height={500} 
          title="Force-Directed Graph of Pliny's Correspondents"/>
        <h2>Social Class Breakdown</h2>
        <p>The following doughnut chart gives a breakdown of correspondents by their
          highest known social class. Use the dropdown to filter by a specific book.
        </p>
        <ClassDoughnut></ClassDoughnut>
        </main>
      </div>
    )
  }

}